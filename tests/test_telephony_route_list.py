import asyncio
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test
from tests.testutil import us_location_info, LocationInfo
from wxc_sdk.common import RouteType
from wxc_sdk.locations import Location
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import OwnerType, NumberListPhoneNumber, NumberType
from wxc_sdk.telephony.prem_pstn.route_group import RouteGroup, RGTrunk
from wxc_sdk.telephony.prem_pstn.route_list import NumberAndAction, RouteList
from wxc_sdk.telephony.prem_pstn.trunk import Trunk, TrunkType


class TestList(TestCaseWithLog):
    def test_001_list_all(self):
        rgs = list(self.api.telephony.prem_pstn.route_list.list())
        print(f'Got {len(rgs)} route list')


@dataclass(init=False)
class TestCreate(TestCaseWithLog):
    _locations: list[LocationInfo] = field(default=None)
    _route_groups: list[RouteGroup] = field(default=None)
    _trunks: list[Trunk] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.route_lists = list(cls.api.telephony.prem_pstn.route_list.list())

    def get_target_location(self) -> Location:
        """
        Pick a random location ... in the US
        """
        if self._locations is None:
            with self.no_log():
                self._locations = us_location_info(api=self.api)
        location = choice(self._locations).location
        print(f'target location: "{location.name}"')
        return location

    @contextmanager
    def get_trunk(self, *, location: Location) -> str:
        """
        get or create a trunk in given location
        :param location:
        :return: trunk id
        """
        if self._trunks is None:
            with self.no_log():
                self._trunks = list(self.api.telephony.prem_pstn.trunk.list())
        trunks_in_location = [trunk for trunk in self._trunks
                              if trunk.location.location_id == location.location_id]
        if trunks_in_location:
            trunk = choice(trunks_in_location)
            print(f'Existing trunk: "{trunk.name}"')
            with self.with_log():
                yield trunk.trunk_id
            return

        # temporarily create a trunk
        existing_names = set(t.name for t in self._trunks)
        trunk_name = next(name for i in range(1, 100)
                          if (name := f'{location.name} {i:02}') not in existing_names)
        print(f'Creating trunk "{trunk_name}" in location "{location.name}"')
        with self.no_log():
            pwd = self.api.telephony.location.generate_password(location_id=location.location_id)
            trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name, location_id=location.location_id,
                                                                 password=pwd,
                                                                 trunk_type=TrunkType.registering)
        try:
            with self.with_log():
                yield trunk_id
        finally:
            with self.no_log():
                print(f'Deleting trunk "{trunk_name}" in location "{location.name}"')
                self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=trunk_id)

    @contextmanager
    def get_route_group(self, *, location: Location) -> str:
        """
        Get (or create) a route group
        :return: route group id
        """
        if self._route_groups is None:
            with self.no_log():
                self._route_groups = list(self.api.telephony.prem_pstn.route_group.list())
        if self._route_groups:
            rg = choice(self._route_groups)
            print(f'existing route group: "{rg.name}"')
            yield rg.rg_id
            return

        # temporarily create one with a trunk in the location
        existing_names = set(rg.name for rg in self._route_groups)
        rg_name = next(name for i in range(1, 100)
                       if (name := f'{location.name} {i:02}') not in existing_names)

        with self.get_trunk(location=location) as trunk_id:
            print(f'creating route group: "{rg_name}"')
            with self.no_log():
                rg_id = self.api.telephony.prem_pstn.route_group.create(
                    route_group=RouteGroup(name=rg_name,
                                           local_gateways=[RGTrunk(trunk_id=trunk_id,
                                                                   priority=1)]))
            try:
                with self.with_log():
                    yield rg_id
            finally:
                with self.no_log():
                    print(f'deleting route group: "{rg_name}"')
                    self.api.telephony.prem_pstn.route_group.delete_route_group(rg_id=rg_id)

    def test_001_create_and_remove(self):
        """
        create and remove a route list
        """
        location = self.get_target_location()
        with self.get_route_group(location=location) as rg_id:

            # get a name for the new route list
            rl_name = next(name for i in range(1, 100)
                           if (name := f'{location.name} {i:02}') not in set(rl.name for rl in self.route_lists))

            print(f'creating route list: "{rl_name}"')
            rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name,
                                                                   location_id=location.location_id,
                                                                   rg_id=rg_id)
            try:
                details = self.api.telephony.prem_pstn.route_list.details(rl_id=rl_id)
                self.assertEqual(location.location_id, details.location.id)
                self.assertEqual(rg_id, details.route_group.id)
                # new list has to be in list of route lists
                rl_list = list(self.api.telephony.prem_pstn.route_list.list())
                self.assertIsNotNone(next((rl for rl in rl_list if rl.name == rl_name), None))
            finally:
                # clean up: delete the route list again
                print(f'deleting route list: "{rl_name}"')
                self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=rl_id)

    def test_002_create_two_route_lists_in_one_location(self):
        """
        Create two route lists in the same location
        """
        location = self.get_target_location()
        with self.get_route_group(location=location) as rg_id:
            rg_id: str
            # get a name for the new route list
            new_rl_names = (name for i in range(1, 100)
                            if (name := f'{location.name} {i:02}') not in set(rl.name for rl in self.route_lists))
            rl_names = [next(new_rl_names) for _ in range(2)]
            rl_ids = []
            try:
                for rl_name in rl_names:
                    print(f'creating route list: "{rl_name}"')
                    rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name,
                                                                           location_id=location.location_id,
                                                                           rg_id=rg_id)
                    rl_ids.append(rl_id)
            finally:
                for rl_id, rl_name in zip(rl_ids, rl_names):
                    print(f'deleting route list: "{rl_name}"')
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


@dataclass(init=False)
class TestNumbers(TestCaseWithLog):
    """
    Test case to add/remove numbers from a route list
    """
    route_list: ClassVar[list[RouteList]]
    us_locations: ClassVar[list[LocationInfo]]
    route_groups: ClassVar[list[RouteGroup]]
    # available phone numbers in organisation
    numbers: ClassVar[list[NumberListPhoneNumber]]
    # unused phone numbers
    new_numbers: ClassVar[Generator[str, None, None]]
    target_location_info: LocationInfo = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        route_lists = list(cls.api.telephony.prem_pstn.route_list.list())
        cls.route_lists = route_lists
        cls.us_locations = us_location_info(api=cls.api)
        cls.route_groups = list(cls.api.telephony.prem_pstn.route_group.list())
        cls.numbers = list(cls.api.telephony.phone_numbers(available=True))

    def setUp(self) -> None:
        # create a route list
        if not self.route_groups:
            self.skipTest('Need at least one route group to run test')
        location_info = choice(self.us_locations)
        print(f'target location: "{location_info.location.name}"')
        self.target_location_info = location_info
        rg = choice(self.route_groups)

        # get a name for the new route list
        rl_name = next(name for i in range(1000)
                       if (name := f'{location_info.location.name} {i}') not in set(rl.name for rl in self.route_lists))

        print(f'Creating route list "{rl_name}"')
        self.rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name,
                                                                    location_id=location_info.location.location_id,
                                                                    rg_id=rg.rg_id)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        # delete the route list we created
        self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=self.rl_id)

    @contextmanager
    def tns_for_route_list(self, tn_count: int = 5):
        """
        gets some TNs which can be added to test route list
        """
        # get phone numbers in target location
        available_tns = [n.phone_number for n in self.numbers
                         if n.location.id == self.target_location_info.location.location_id
                         and not n.main_number and n.owner is None]
        if len(available_tns) < tn_count:
            with self.no_log():
                new_tns = self.target_location_info.available_tns(api=self.api,
                                                                  tns_requested=tn_count - len(available_tns))
                available_tns.extend(new_tns)
                # add phone numbers to location (temporarily)
                print(f'adding TNs to location: {", ".join(new_tns)}')
                self.api.telephony.location.number.add(location_id=self.target_location_info.location.location_id,
                                                       phone_numbers=new_tns)
        else:
            new_tns = []
        try:
            yield available_tns[:tn_count]
        finally:
            if new_tns:
                with self.no_log():
                    print(f'removing TNs from location: {", ".join(new_tns)}')
                    self.api.telephony.location.number.remove(
                        location_id=self.target_location_info.location.location_id,
                        phone_numbers=new_tns)

    def test_001_add_and_remove_numbers(self):
        """
        add some numbers to a route list and remove them again
        """
        with self.tns_for_route_list() as new_numbers:
            new_numbers: list[str]
            api = self.api.telephony.prem_pstn.route_list

            print(f'Adding numbers to route list: {", ".join(new_numbers)}')
            response = api.update_numbers(rl_id=self.rl_id,
                                          numbers=[NumberAndAction.add(number) for number in new_numbers])
            numbers_after = set(api.numbers(rl_id=self.rl_id))
            try:
                with self.no_log():
                    # validation
                    self.assertFalse(response)
                    self.assertTrue(all(n in numbers_after for n in new_numbers))
                    numbers_in_location = list(self.api.telephony.phone_numbers(
                        location_id=self.target_location_info.location.location_id,
                        number_type=NumberType.number
                    ))
                    err = False
                    for number in new_numbers:
                        # number has to exist in location
                        number_in_location = next((n for n in numbers_in_location
                                                   if n.phone_number == number), None)
                        if number_in_location is None:
                            print(f'new number "{number}": not found in location')
                            continue
                        owner = number_in_location.owner
                        if owner is None \
                                or owner.owner_type != OwnerType.route_list \
                                or owner.owner_id != self.rl_id:
                            print(f'Something is wrong with the owner: {owner}')
                            err = False
                            continue
                    # for
                    self.assertFalse(err, 'Something went wrong')
            finally:
                print(f'Removing numbers from route list: {", ".join(new_numbers)}')
                response = api.update_numbers(rl_id=self.rl_id,
                                              numbers=[NumberAndAction.delete(number) for number in new_numbers])
                self.assertFalse(response)
                numbers_after = set(api.numbers(rl_id=self.rl_id))
                self.assertTrue(all(n not in numbers_after for n in new_numbers), 'Numbers not removed')


class DeleteAll(TestCaseWithLog):
    def test_001_delete_all(self):
        """
        delete all route lists
        """
        route_lists = list(self.api.telephony.prem_pstn.route_list.list())
        if not route_lists:
            self.skipTest('No route lists to delete')
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda rl: self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=rl.rl_id),
                          route_lists))


class UnlistedRLs(TestCaseWithLog):

    @async_test
    async def test_unlisted(self):
        """
        Some RLs seem to not be listed; but the name still exists
        """
        rl_name_template = '{name} {i:02}'
        calling_locations = list(self.api.telephony.location.list())
        calling_locations = await asyncio.gather(
            *[self.async_api.telephony.location.details(location_id=loc.location_id) for loc in calling_locations])
        calling_locations = [loc for loc in calling_locations
                             if loc.connection and loc.connection.type in {RouteType.trunk, RouteType.route_group}]
        route_group = next((rg for rg in self.api.telephony.prem_pstn.route_group.list()), None)
        if route_group is None:
            self.skipTest('No route group to test with')
        max_index_to_test = 2
        err = None
        existing_rls = list(self.api.telephony.prem_pstn.route_list.list())
        existing_rl_names = set(f'{rl.location_id}/{rl.name}' for rl in existing_rls)
        for test_index in range(1, max_index_to_test + 1):
            for location in calling_locations:
                rl_name = rl_name_template.format(name=location.name, i=test_index)
                if f'{location.location_id}/{rl_name}' in existing_rl_names:
                    print(f'Route list "{rl_name}" already exists')
                    continue
                try:
                    print(f'Creating "{rl_name}"')
                    rl_id = self.api.telephony.prem_pstn.route_list.create(name=rl_name,
                                                                           location_id=location.location_id,
                                                                           rg_id=route_group.rg_id)
                except RestError as e:
                    err = err or e
                    if e.code == 27601:
                        print(f'Route list "{rl_name}" already exists')
                    else:
                        print(f'Error creating "{rl_name}": {e}')
                else:
                    # delete the RL again
                    print(f'Deleting "{rl_name}"')
                    self.api.telephony.prem_pstn.route_list.delete_route_list(rl_id=rl_id)
            # for location
        # for test_index
        if err:
            raise err
        return
