import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from random import choice

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.prem_pstn.route_group import RGTrunk, RouteGroup
from wxc_sdk.telephony.prem_pstn.trunk import Trunk, TrunkType


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
                        local_gateways=[RGTrunk(id=trunk.trunk_id,
                                                priority=1, name='ff', location_id='sas')])
        rg_id = self.api.telephony.prem_pstn.route_group.create(route_group=rg)
        try:
            pass
        finally:
            # clean up: delete the route group again
            self.api.telephony.prem_pstn.route_group.delete_route_group(rg_id=rg_id)


class TestTrunksPerRouteGroup(TestWithLocations):

    @async_test
    async def test_001_trunks_per_route_group(self):
        """
        How many trunks can we add to a given route group?
        """
        # pick a target location
        target_location = choice(self.locations)

        # get existing trunks and route groups
        trunks, route_groups = await asyncio.gather(
            self.async_api.telephony.prem_pstn.trunk.list(),
            self.async_api.telephony.prem_pstn.route_group.list()
        )
        trunks: list[Trunk]
        route_groups: list[RouteGroup]

        # names for new trunks
        loc_prefix, _ = re.subn(r'[^\w\d\s]', ' ', target_location.name[:20])
        new_trunk_names = (name for i in range(1000)
                           if (name := f'{loc_prefix} {i:03}') not in set(t.name for t in trunks))

        # list of ids of created trunks
        created_trunk_ids = []

        # create a trunk in target location
        def create_trunk() -> str:
            trunk_name = next(new_trunk_names)
            password = self.api.telephony.location.generate_password(location_id=target_location.location_id)
            new_trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                     location_id=target_location.location_id,
                                                                     password=password,
                                                                     trunk_type=TrunkType.registering)
            print(f'created trunk "{trunk_name}" in location "{target_location.name}"')
            created_trunk_ids.append(new_trunk_id)
            return new_trunk_id

        trunk_id = create_trunk()
        rg_id = None
        trunk_count = None
        with self.assertRaises(RestError) as exc:
            try:
                # create a route group with that trunk
                rg_name = next(name for i in range(1, 1000)
                               if (name := f'{target_location.name} {i:03}') not in set(rg.name for rg in route_groups))

                rg = RouteGroup(name=rg_name,
                                local_gateways=[RGTrunk(id=trunk_id,
                                                        priority=1)])
                rg_id = self.api.telephony.prem_pstn.route_group.create(route_group=rg)
                print(f'Created RG "{rg_name}": 1 trunk')

                # continue adding trunks (up to 25) to RG until that fails
                for trunk_count in range(2, 26):
                    create_trunk()
                    rg = RouteGroup(name=rg_name,
                                    local_gateways=[RGTrunk(id=trunk_id,
                                                            priority=1)
                                                    for trunk_id in created_trunk_ids])
                    self.api.telephony.prem_pstn.route_group.update(rg_id=rg_id, update=rg)
                    print(f'Updated RG "{rg_name}": {len(created_trunk_ids)} trunks')
            finally:
                # clean up

                # delete route group
                if rg_id:
                    self.api.telephony.prem_pstn.route_group.delete_route_group(rg_id=rg_id)

                # delete all trunks we created
                await asyncio.gather(*[self.async_api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=trunk_id)
                                       for trunk_id in created_trunk_ids])

        rest_error: RestError = exc.exception
        self.assertEqual(400, rest_error.response.status_code, 'unexpected status code')
        self.assertEqual(25043, rest_error.code, 'unexpected error code')
        self.assertEqual('10', rest_error.description.split()[-1][:-1], 'unexpected error description')

        self.assertEqual(trunk_count, 11, 'expected to be able to assign 10 trunks exactly')


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
