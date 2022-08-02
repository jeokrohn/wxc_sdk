from concurrent.futures import ThreadPoolExecutor
from random import choice

from tests.base import TestCaseWithLog
from wxc_sdk.telephony.prem_pstn.route_group import RGTrunk, RouteGroup


class TestList(TestCaseWithLog):
    def test_001_list_all(self):
        rgs = list(self.api.telephony.prem_pstn.route_group.list())
        print(f'Got {len(rgs)} route groups')


class TestCreate(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.route_groups = list(cls.api.telephony.prem_pstn.route_group.list())

    def test_001_create(self):

        # pick a trunk
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        trunk = choice(trunks)

        # get a name for the new route group
        rg_name = next(name for i in range(1000)
                       if (name := f'{trunk.location.name} {i}') not in set(rg.name for rg in self.route_groups))

        # create a rg with a single trunk
        print(f'Creating route group "{rg_name}" in location "{trunk.location.name}"')
        rg = RouteGroup(name=rg_name,
                        local_gateways=[RGTrunk(trunk_id=trunk.trunk_id,
                                                priority=1, name='ff', location_id='sas')])
        rg_id = self.api.telephony.prem_pstn.route_group.create(route_group=rg)
        try:
            ...
        finally:
            # clean up: delete the route group again
            self.api.telephony.prem_pstn.route_group.delete_route_group(rg_id=rg_id)


class TestDetail(TestCaseWithLog):
    def test_001_detail_all(self):
        rgs = list(self.api.telephony.prem_pstn.route_group.list())
        if not rgs:
            self.skipTest('No route groups')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda rg: self.api.telephony.prem_pstn.route_group.details(rg_id=rg.rg_id),
                                    rgs))
        print(f'Got details for {len(rgs)} route groups')


class TestUsage(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.route_groups = list(cls.api.telephony.prem_pstn.route_group.list())

    def setUp(self) -> None:
        super().setUp()
        if not self.route_groups:
            self.skipTest('No route groups to run the test')

    def test_001_usage_all(self):
        """
        get usage for all route groups
        """
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda rg: self.api.telephony.prem_pstn.route_group.usage(rg_id=rg.rg_id),
                                  self.route_groups))
        print(f'Got usage for {len(self.route_groups)} route groups')

    def test_002_usage_call_to_extension(self):
        """
        get usage_call_to_extension for all route groups
        """
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(
                lambda rg: list(self.api.telephony.prem_pstn.route_group.usage_call_to_extension(rg_id=rg.rg_id)),
                self.route_groups))
        print(f'Got usage_call_to_extension for {len(self.route_groups)} route groups')

    def test_003_usage_dial_plan(self):
        """
        get usage_dial_plan for all route groups
        """
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(
                lambda rg: list(self.api.telephony.prem_pstn.route_group.usage_dial_plan(rg_id=rg.rg_id)),
                self.route_groups))
        print(f'Got usage_dial_plan for {len(self.route_groups)} route groups')

    def test_004_usage_location_pstn(self):
        """
        get usage_location_pstn for all route groups
        """
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(
                lambda rg: list(self.api.telephony.prem_pstn.route_group.usage_location_pstn(rg_id=rg.rg_id)),
                self.route_groups))
        print(f'Got usage_location_pstn for {len(self.route_groups)} route groups')

    def test_005_usage_route_lists(self):
        """
        get usage_route_lists for all route groups
        """
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(
                lambda rg: list(self.api.telephony.prem_pstn.route_group.usage_route_lists(rg_id=rg.rg_id)),
                self.route_groups))
        print(f'Got usage_route_lists for {len(self.route_groups)} route groups')
