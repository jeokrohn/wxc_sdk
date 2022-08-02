from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from random import choice, sample

from tests.base import TestCaseWithLog
from wxc_sdk.telephony import OwnerType
from wxc_sdk.telephony.prem_pstn.route_group import RouteGroup, RGTrunk
from wxc_sdk.telephony.prem_pstn.route_list import NumberAndAction


class TestList(TestCaseWithLog):
    def test_001_list_all(self):
        rgs = list(self.api.telephony.prem_pstn.route_list.list())
        print(f'Got {len(rgs)} route list')


class TestCreate(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.route_lists = list(cls.api.telephony.prem_pstn.route_list.list())
        cls.locations = list(cls.api.locations.list())
        cls.route_groups = list(cls.api.telephony.prem_pstn.route_group.list())

    def setUp(self) -> None:
        super().setUp()
        if not self.route_groups:
            self.skipTest('need a route group to run this test')

    def test_001_create(self):
        location = choice(self.locations)
        rg = choice(self.route_groups)

        # get a name for the new route list
        rl_name = next(name for i in range(1000)
                       if (name := f'{location.name} {i}') not in set(rl.name for rl in self.route_lists))

        rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name, location_id=location.location_id,
                                                               rg_id=rg.rg_id)
        try:
            details = self.api.telephony.prem_pstn.route_list.details(rl_id=rl_id)
            self.assertEqual(location.location_id, details.location.id)
            self.assertEqual(rg.rg_id, details.route_group.id)
        finally:
            # clean up: delete the route list again
            self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=rl_id)


class TestDetail(TestCaseWithLog):
    def test_001_detail_all(self):
        rls = list(self.api.telephony.prem_pstn.route_list.list())
        if not rls:
            self.skipTest('No route lists')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda rl: self.api.telephony.prem_pstn.route_list.details(rl_id=rl.rl_id),
                                    rls))
        print(f'Got details for {len(rls)} route lists')


class TestRouteListSJC(TestCaseWithLog):
    def test_001_create_and_add_numbers(self):
        """
        create a route list in location SJC and add a few of the available numbers
        :return:
        """
        # get location SCJ
        location = list(self.api.locations.list(name='SJC'))[0]
        # all available phone numbers in location SJC
        numbers = list(self.api.telephony.phone_numbers(location_id=location.location_id, available=True))
        self.assertFalse(any(n.owner for n in numbers))
        # get/create route group in location SJC
        prem_api = self.api.telephony.prem_pstn
        rg = next(prem_api.route_group.list(name='SJC'), None)
        if rg is None:
            # find a trunk in location SJC
            sjc_trunk = next(t for t in self.api.telephony.prem_pstn.trunk.list(location_name='SJC'))
            rg_id = prem_api.route_group.create(
                route_group=RouteGroup(name='SJC',
                                       local_gateways=[RGTrunk(trunk_id=sjc_trunk.trunk_id,
                                                               priority=1)]))
            rg = prem_api.route_group.details(rg_id=rg_id)
            rg.rg_id = rg_id
        #  get/create a route list in location SJC
        sjc_rl = next(prem_api.route_list.list(location_id=[location.location_id]), None)
        if not sjc_rl:
            rl_id = prem_api.route_list.create(name='SJC', location_id=location.location_id,
                                               rg_id=rg.rg_id)
            sjc_rl = prem_api.route_list.details(rl_id=rl_id)
            sjc_rl.rl_id = rl_id
        try:
            # pick a few numbers
            rl_numbers = set(n.phone_number for n in sample(numbers, 5))
            # numbers to add
            update_result = prem_api.route_list.update_numbers(rl_id=sjc_rl.rl_id,
                                                               numbers=[NumberAndAction.add(n)
                                                                        for n in rl_numbers])
            self.assertFalse(update_result)
            numbers_after = prem_api.route_list.numbers(rl_id=sjc_rl.rl_id)

            # how does that impact the number ownership?
            sjc_numbers_in_rl = [n for n in self.api.telephony.phone_numbers(location_id=location.location_id)
                                 if n.phone_number in rl_numbers]

            # set of numbers in RL has to be equal to the numbers we wanted to add
            self.assertEqual(rl_numbers, set(numbers_after))

            # all numbers now have to have a route list as owner
            self.assertTrue(all(n.owner and n.owner.owner_type == OwnerType.route_list
                                for n in sjc_numbers_in_rl))
        finally:
            # clean up: delete route list
            prem_api.route_list.delete_route_list(rl_id=sjc_rl.rl_id)


class TestNumbers(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        route_lists = list(cls.api.telephony.prem_pstn.route_list.list())
        cls.route_lists = route_lists
        cls.locations = list(cls.api.locations.list())
        cls.route_groups = list(cls.api.telephony.prem_pstn.route_group.list())

        api = cls.api.telephony.prem_pstn.route_list
        with ThreadPoolExecutor() as pool:
            numbers = list(pool.map(lambda rl: list(api.numbers(rl_id=rl.rl_id)), route_lists))
        cls.existing_numbers = set(chain.from_iterable(numbers))
        cls.numbers = list(cls.api.telephony.phone_numbers(available=True))
        cls.new_numbers = (pattern for i in range(100000)
                           if (pattern := f'+4951007{i:05}') not in cls.existing_numbers)

    def setUp(self) -> None:
        # create a route list
        if not self.route_groups:
            self.skipTest('Need at least one route group to run test')
        location = choice(self.locations)
        rg = choice(self.route_groups)

        # get a name for the new route list
        rl_name = next(name for i in range(1000)
                       if (name := f'{location.name} {i}') not in set(rl.name for rl in self.route_lists))

        self.rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name, location_id=location.location_id,
                                                                    rg_id=rg.rg_id)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        # delete the route list we created
        self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=self.rl_id)

    def test_001_add_numbers(self):
        # TODO: finalize when we have the ability to add phone numbers
        new_numbers = [next(self.new_numbers) for _ in range(50)]
        api = self.api.telephony.prem_pstn.route_list
        response = api.update_numbers(rl_id=self.rl_id,
                                      numbers=[NumberAndAction.add(number) for number in new_numbers])
        numbers_after = api.numbers(rl_id=self.rl_id)
        foo = 1
