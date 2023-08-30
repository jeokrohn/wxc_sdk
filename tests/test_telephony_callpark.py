import asyncio
import json
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain, groupby
from re import match
from typing import ClassVar
from unittest import skip

from wxc_sdk.all_types import *
from tests.base import TestWithLocations, async_test
from tests.testutil import create_call_park_extension

# Number of call parks to create by create many test
CP_MANY = 100


class TestRead(TestWithLocations):
    """
    Test cases for list(), details()
    """

    @async_test
    async def test_001_list_all_locations(self):
        """
        List call parks in all locations
        """
        lists = await asyncio.gather(*[self.async_api.telephony.callpark.list(location_id=location.location_id)
                                       for location in self.locations])
        call_parks: list[CallPark] = list(chain.from_iterable(lists))
        print(f'Got {len(call_parks)} call parks.')

    @async_test
    async def test_002_list_by_name(self):
        """
        List call parks by name
        """
        lists = await asyncio.gather(*[self.async_api.telephony.callpark.list(location_id=location.location_id)
                                       for location in self.locations])
        call_parks: list[CallPark] = list(chain.from_iterable(lists))

        # find a location with multiple call parks and then check that list by name only returns a subset
        by_location = {location_id: callparks
                       for location_id, cpi in groupby(sorted(call_parks, key=lambda cp: cp.location_id),
                                                       key=lambda cp: cp.location_id)
                       if len(callparks := list(cpi)) > 1}
        by_location: dict[str, list[CallPark]]
        if not by_location:
            self.skipTest('Need at least one location with multipla call parks')
        target_location_id = random.choice(list(by_location))
        parks = by_location[target_location_id]
        cq_list = list(self.api.telephony.callpark.list(location_id=target_location_id,
                                                        name=parks[0].name))
        matching_parks = [cp for cp in parks
                          if cp.name.startswith(parks[0].name)]
        self.assertEqual(len(matching_parks), len(cq_list))

    @async_test
    async def test_003_all_details(self):
        """
        Get details for all call parks
        """
        lists = await asyncio.gather(*[self.async_api.telephony.callpark.list(location_id=location.location_id)
                                       for location in self.locations])
        call_parks: list[CallPark] = list(chain.from_iterable(lists))

        if not call_parks:
            self.skipTest('No existing call parks.')
        details = await asyncio.gather(*[self.async_api.telephony.callpark.details(location_id=cp.location_id,
                                                                                   callpark_id=cp.callpark_id)
                                         for cp in call_parks])
        details: list[CallPark]
        with_cpe = [d for d in details
                    if d.call_park_extensions]
        print(f'Got details for {len(details)} call parks.')
        print(f'{len(with_cpe)} call parks with call park extension(s)')


class TestCreate(TestWithLocations):
    """
    call park creation
    """

    def test_001_trivial(self):
        """
        create the most trivial call park
        """
        # pick random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        # get available call park name in location
        cpa = self.api.telephony.callpark
        call_parks = list(cpa.list(location_id=target_location.location_id, name='cp_'))
        names = set(cp.name for cp in call_parks)
        new_names = (name for i in range(1000) if (name := f'cp_{i:03}') not in names)
        new_name = next(new_names)
        # create call park
        settings = CallPark.default(name=new_name)
        new_id = cpa.create(location_id=target_location.location_id, settings=settings)
        print(f'new call park id: {new_id}')

        details = cpa.details(location_id=target_location.location_id, callpark_id=new_id)
        print('New call park')
        print(json.dumps(json.loads(details.model_dump_json()), indent=2))

    @async_test
    async def test_002_many(self):
        """
        create many call parks and test pagination
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        # shortcut for callpark API
        api = self.async_api.telephony.callpark

        # Get names for new call parks
        parks = await api.list(location_id=target_location.location_id)
        print(f'{len(parks)} existing call parks')

        if len(parks) < CP_MANY:
            park_names = set(park.name for park in parks)
            new_names = (name for i in range(1000)
                         if (name := f'many_{i:03}') not in park_names)
            names = [name for name, _ in zip(new_names, range(CP_MANY))]
            print(f'got {len(names)} new names')

            async def new_park(*, park_name: str):
                """
                Create a new call park with the given name
                :param park_name:
                :return: ID of new call park
                """
                settings = CallPark.default(name=park_name)
                # creat new call park
                new_park_id = await api.create(location_id=target_location.location_id, settings=settings)
                print(f'Created {park_name}')
                return new_park_id

            new_parks = await asyncio.gather(*[new_park(park_name=name) for name in names])
            print(f'Created {len(new_parks)} call parks.')
        parks = await api.list(location_id=target_location.location_id)
        print(f'Total number of call parks: {len(parks)}')
        parks_pag = await api.list(location_id=target_location.location_id, max=20)
        print(f'Total number of call parks read with pagination: {len(parks_pag)}')
        self.assertEqual(len(parks), len(parks_pag))

        park_ids = set(p.callpark_id for p in parks)
        park_ids_paginated = set(p.callpark_id for p in parks_pag)
        self.assertEqual(park_ids, park_ids_paginated)

        # also check the link headers of the collected requests
        paginated_requests = [request
                              for request in self.requests(method='GET',
                                                           url_filter=r'.+/config/locations/('
                                                                      r'?P<location_id>\w+)/callParks\?')
                              if request.url_query.get('max')]
        pagination_link_error = False
        for i, request in enumerate(paginated_requests, 1):
            start = (start := request.url_query.get('start')) and int(start[0])
            items = len(request.response_body['callParks'])
            print(f'page {i}: start={start}, items={items}')
            link_header = request.response_headers.get('Link')
            if link_header and (link_match := match(r'<(?P<link>\S+)>;rel="(?P<rel>\w+)"', link_header)):
                print(f'  {link_match["rel"]}: {link_match["link"]}')
                if link_match['link'].startswith('https,'):
                    pagination_link_error = True
        self.assertFalse(pagination_link_error)

    @async_test
    async def test_003_with_call_park_extension(self):
        """
        Create a call park with a call park extension
        """
        # TODO: locations.list() is broken and returns locations without calling entitlement
        #  ... which breaks all tests relying on calling
        # pick random location
        target_location = next(self.api.locations.list(name='Hartford'), None)
        # TODO: revert to random location selection asap (see above)
        # target_location: Location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        # new name for call park
        cpa = self.api.telephony.callpark
        call_parks = list(cpa.list(location_id=target_location.location_id, name='cp_'))
        names = set(cp.name for cp in call_parks)
        new_names = (name for i in range(1000) if (name := f'cp_{i:03}') not in names)
        new_name = next(new_names)

        # we need a call park extension in that location that can be assigned
        # .. get list of call park groups and collect CPE IDs for all CPEs used in these CPGs
        call_park_groups = list(cpa.list(location_id=target_location.location_id))
        cpg_details = await asyncio.gather(
            *[self.async_api.telephony.callpark.details(location_id=target_location.location_id,
                                                        callpark_id=cpg.callpark_id)
              for cpg in call_park_groups])
        cpg_details: list[CallPark]
        used_call_park_extension_ids = set(
            chain.from_iterable((cpe.cpe_id for cpe in cpg_detail.call_park_extensions)
                                for cpg_detail in cpg_details
                                if cpg_detail.call_park_extensions))

        # we can only use a call park extension that is not yet assigned to a call park group
        available_cpes = [cpe
                          for cpe in self.api.telephony.callpark_extension.list(location_id=target_location.location_id)
                          if cpe.cpe_id not in used_call_park_extension_ids]
        if available_cpes:
            cpe: CallParkExtension = random.choice(available_cpes)
            cpe_id = cpe.cpe_id
        else:
            cpe_id = create_call_park_extension(api=self.api, location_id=target_location.location_id)

        # create call park
        settings = CallPark.default(name=new_name)
        settings.agents = []
        settings.park_on_agents_enabled = False
        settings.call_park_extensions = [CallParkExtension(cpe_id=cpe_id)]
        new_id = cpa.create(location_id=target_location.location_id, settings=settings)
        print(f'new call park id: {new_id}')

        details = cpa.details(location_id=target_location.location_id, callpark_id=new_id)
        print('New call park')
        print(json.dumps(json.loads(details.model_dump_json()), indent=2))


@dataclass(init=False)
class TestUpdate(TestWithLocations):
    """
    Test call park updates
    """
    # list of all call parks
    cp_list: ClassVar[list[CallPark]]
    # lists of call parks per location
    cp_by_location: ClassVar[dict[str, list[CallPark]]]
    target: CallPark = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:

        super().setUpClass()
        with ThreadPoolExecutor() as pool:
            cp_lists = list(pool.map(
                lambda location: cls.api.telephony.callpark.list(location_id=location.location_id),
                cls.locations))
        cls.cp_list = list(chain.from_iterable(cp_lists))
        cls.cp_by_location = reduce(lambda red, cp: red[cp.location_id].append(cp) or red,
                                    cls.cp_list,
                                    defaultdict(list))

    def setUp(self) -> None:
        """
        chose a random call park target and save settings
        """
        super().setUp()
        if not self.cp_list:
            self.skipTest('No existing call parks to mess with')
        target = random.choice(self.cp_list)
        print(f'target call park: "{target.name}" in "{target.location_name}"')
        self.target = self.api.telephony.callpark.details(location_id=target.location_id,
                                                          callpark_id=target.callpark_id)
        # also set location id and name (not returned by details())
        self.target.location_id = target.location_id
        self.target.location_name = target.location_name

    def tearDown(self) -> None:
        """
        Restore settings to original after test
        :return:
        """
        try:
            if self.target:
                print('tearDown: restore settings')
                self.api.telephony.callpark.update(location_id=self.target.location_id,
                                                   callpark_id=self.target.callpark_id,
                                                   settings=self.target)
        finally:
            super().tearDown()

    def test_001_name(self):
        """
        change name
        """
        names = set(cp.name for cp in self.cp_list
                    if cp.location_id == self.target.location_id)
        new_name = next(name
                        for i in range(1000)
                        if (name := f'cp_{i:03}') not in names)
        settings = CallPark(name=new_name)
        cpa = self.api.telephony.callpark
        new_id = cpa.update(location_id=self.target.location_id,
                            callpark_id=self.target.callpark_id,
                            settings=settings)
        self.target.callpark_id = new_id
        details = cpa.details(location_id=self.target.location_id,
                              callpark_id=new_id)
        self.assertEqual(new_name, details.name)
        # .. other than that the updated details should be identical
        details.location_id = self.target.location_id
        details.location_name = self.target.location_name
        details.name = self.target.name
        self.assertEqual(self.target, details)

    def test_002_recall_hg_id(self):
        """
        change recall hunt group id
        """
        # we are not actually using the target chosen by setuo()
        self.target = None
        cpa = self.api.telephony.callpark
        with ThreadPoolExecutor() as pool:
            recall_lists = list(pool.map(
                lambda location: list(cpa.available_recalls(location_id=location.location_id)),
                self.locations))
        # look for locations with existing call parks and available recall hunt groups
        location_candidates = {location.location_id: recall_list for location, recall_list in
                               zip(self.locations, recall_lists)
                               if recall_list and location.location_id in self.cp_by_location}
        location_candidates: dict[str, list[AvailableRecallHuntGroup]]
        if not location_candidates:
            self.skipTest('No location with call parks and available recall hunt groups')
        location_id = random.choice(list(location_candidates))
        recall_list = location_candidates[location_id]
        target = random.choice(self.cp_by_location[location_id])
        print(f'Target call park: "{target.name}" in "{target.location_name}"')
        target_details = cpa.details(location_id=target.location_id,
                                     callpark_id=target.callpark_id)
        target_details.location_id = target.location_id
        target_details.location_name = target.location_name
        recall_hunt_group_id = target_details.recall.hunt_group_id
        if not recall_hunt_group_id:
            new_recall = random.choice(recall_list)
            print(f'Changing recall from None to {new_recall.name}')
            new_recall_id = new_recall.huntgroup_id
            new_recall_name = new_recall.name
        else:
            print(f'Changing recall from {target_details.recall.hunt_group_name} to None')
            new_recall_id = ''
            new_recall_name = None
        settings = CallPark(recall=RecallHuntGroup(hunt_group_id=new_recall_id, option=CallParkRecall.hunt_group_only))
        try:
            cpa.update(location_id=location_id, callpark_id=target_details.callpark_id,
                       settings=settings)
            details_after = cpa.details(location_id=location_id, callpark_id=target_details.callpark_id)
            self.assertEqual(new_recall_id, details_after.recall.hunt_group_id or '')
            self.assertEqual(new_recall_name, details_after.recall.hunt_group_name)
            self.assertEqual(CallParkRecall.hunt_group_only, details_after.recall.option)
        finally:
            # restore old settings
            target_details.recall.hunt_group_id = recall_hunt_group_id
            cpa.update(location_id=location_id,
                       callpark_id=target_details.callpark_id,
                       settings=target_details)
            details = cpa.details(location_id=location_id,
                                  callpark_id=target_details.callpark_id)
            self.assertEqual(target_details.recall.hunt_group_id, details.recall.hunt_group_id)

    def test_004_from_details(self):
        """
        get details and use details for update
        """
        cpa = self.api.telephony.callpark
        new_id = cpa.update(location_id=self.target.location_id,
                            callpark_id=self.target.callpark_id,
                            settings=self.target)
        details = cpa.details(location_id=self.target.location_id,
                              callpark_id=new_id)
        details.location_id = self.target.location_id
        details.location_name = self.target.location_name
        self.assertEqual(self.target, details)

    @skip('Not implemented')
    def test_005_add_agent(self):
        """
        add an agent to a call park
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_006_remove_agent(self):
        """
        remove an agent from a call park
        """
        # TODO: implement
        pass


class AvailableAgents(TestWithLocations):
    """
    test available_agents()
    """

    def test_001_all(self):
        """
        available agents for all locations
        """
        with ThreadPoolExecutor() as pool:
            available_agents = list(pool.map(
                lambda location: list(self.api.telephony.callpark.available_agents(location_id=location.location_id)),
                self.locations))
        name_len = max(len(location.name) for location in self.locations)
        for location, agents in zip(self.locations, available_agents):
            print(f'Available in {location.name:{name_len}}:'
                  f' {", ".join(f"{agent.display_name} ({agent.user_type})" for agent in agents)}')


class AvailableRecalls(TestWithLocations):
    """
    test available_recalls()
    """

    def test_001_all(self):
        """
        available recalls for all locations
        """
        with ThreadPoolExecutor() as pool:
            available_recalls = list(pool.map(
                lambda location: list(self.api.telephony.callpark.available_recalls(location_id=location.location_id)),
                self.locations))
        name_len = max(len(location.name) for location in self.locations)
        for location, recalls in zip(self.locations, available_recalls):
            print(f'Available in {location.name:{name_len}}:'
                  f' {", ".join(recall.name for recall in recalls)}')


class TestLocationCallParkSettings(TestWithLocations):
    """
    get/update LocationCallParkSettings
    """

    def test_001_get_all(self):
        """
        get LocationCallParkSettings for all locations
        """
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(
                lambda location: self.api.telephony.callpark.call_park_settings(location_id=location.location_id),
                self.locations))
        print(f'Got call park location settings for {len(settings)} locations')

    @skip('Not implemented')
    def test_002_update_all(self):
        """
        get settings and use fill settings for update
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_003_recall_hg_id(self):
        """
        change recall hunt group id
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_004_recall_hg_option(self):
        """
        change recall hunt group option
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_005_cp_settings_ring_pattern(self):
        """
        change ring_pattern
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_006_cp_settings_recall_time(self):
        """
        change recall_time
        """
        # TODO: implement
        pass

    @skip('Not implemented')
    def test_007_cp_settings_hunt_wait_time(self):
        """
        change hunt_wait_time
        """
        # TODO: implement
        pass
