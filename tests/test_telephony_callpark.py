import json
import random
from concurrent.futures import ThreadPoolExecutor
from itertools import chain, groupby
from typing import List

from wxc_sdk.types import *
from .base import TestWithLocations


class TestRead(TestWithLocations):
    """
    Test cases for list(), details()
    """

    def test_001_list_all_locations(self):
        """
        List call parks in all locations
        """
        with ThreadPoolExecutor() as pool:
            lists = list(pool.map(
                lambda location: list(self.api.telephony.callpark.list(location_id=location.location_id)),
                self.locations))
            call_parks = list(chain.from_iterable(lists))
        print(f'Got {len(call_parks)} call parks.')

    def test_002_list_by_name(self):
        """
        List call parks by name
        """
        with ThreadPoolExecutor() as pool:
            lists = list(pool.map(
                lambda location: list(self.api.telephony.callpark.list(location_id=location.location_id)),
                self.locations))
            call_parks = list(chain.from_iterable(lists))
        # find a location with multiple call parks and then check that list by name only returns a subset
        by_location = {location_id: callparks
                       for location_id, cpi in groupby(sorted(call_parks, key=lambda cp: cp.location_id),
                                                       key=lambda cp: cp.location_id)
                       if len(callparks := list(cpi)) > 1}
        by_location: dict[str, List[CallPark]]
        if not by_location:
            self.skipTest('Need at least one location with multipla call parks')
        target_location_id = random.choice(list(by_location))
        parks = by_location[target_location_id]
        cq_list = list(self.api.telephony.callpark.list(location_id=target_location_id,
                                                        name=parks[0].name))
        matching_parks = [cp for cp in parks
                          if cp.name.startswith(parks[0].name)]
        self.assertEqual(len(matching_parks), len(cq_list))

    def test_003_all_details(self):
        """
        Get details for all call parks
        """
        with ThreadPoolExecutor() as pool:
            lists = list(pool.map(
                lambda location: list(self.api.telephony.callpark.list(location_id=location.location_id)),
                self.locations))
            call_parks = list(chain.from_iterable(lists))
            if not call_parks:
                self.skipTest('No existing call parks.')
            details = list(pool.map(
                lambda cp: self.api.telephony.callpark.details(location_id=cp.location_id,
                                                               callpark_id=cp.callpark_id),
                call_parks))
        print(f'Got details for {len(details)} call parks.')


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
        print(json.dumps(json.loads(details.json()), indent=2))

    def test_002_many(self):
        """
        create many call parks and test pagination
        """
        CP_NUMBER = 300
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        tcp = self.api.telephony.callpark

        # Get names for new call parks
        parks = list(tcp.list(location_id=target_location.location_id))
        print(f'{len(parks)} existing call parks')
        park_names = set(park.name for park in parks)
        new_names = (name for i in range(1000)
                     if (name := f'many_{i:03}') not in park_names)
        names = [name for name, _ in zip(new_names, range(CP_NUMBER))]
        print(f'got {len(names)} new names')

        def new_park(*, park_name: str):
            """
            Create a new call park with the given name
            :param park_name:
            :return:
            """
            settings = CallPark.default(name=park_name)
            # creat new call park
            new_park = tcp.create(location_id=target_location.location_id, settings=settings)
            print(f'Created {park_name}')
            return new_park

        with ThreadPoolExecutor() as pool:
            new_parks = list(pool.map(lambda name: new_park(park_name=name),
                                       names))
        print(f'Created {len(new_parks)} call parks.')
        parks = list(self.api.telephony.callpark.list(location_id=target_location.location_id))
        print(f'Total number of call parks: {len(parks)}')
        parks_pag = list(self.api.telephony.callpark.list(location_id=target_location.location_id, max=50))
        print(f'Total number of call parks read with pagination: {len(parks_pag)}')
        self.assertEqual(len(parks), len(parks_pag))
       

class TestUpdate(TestWithLocations):
    """
    Test call park updates
    """

    def test_001_name(self):
        """
        change name
        """
        # TODO: implement
        raise NotImplementedError

    def test_002_recall_hg_id(self):
        """
        change recall hunt group id
        """
        # TODO: implement
        raise NotImplementedError

    def test_003_recall_option(self):
        """
        change recall option
        """
        # TODO: implement
        raise NotImplementedError

    def test_004_from_details(self):
        """
        get details and user details for update
        """
        # TODO: implement
        raise NotImplementedError

    def test_005_add_agent(self):
        """
        add an agent to a call park
        """
        # TODO: implement
        raise NotImplementedError

    def test_006_remove_agent(self):
        """
        remove an agent from a call park
        """
        # TODO: implement
        raise NotImplementedError


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
                  f' {", ".join(f"{agent.display_name} ({agent.user_type.name})" for agent in agents)}')

    def test_002_cp_name(self):
        """
        available agents for call parks with matching name for all locations
        """
        # TODO: implement
        raise NotImplementedError

    def test_003_name(self):
        """
        available agents by name for all locations
        """
        # TODO: implement
        raise NotImplementedError


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

    def test_002_cp_name(self):
        """
        available recalls by name for call parks with matching name for all locations
        """
        # TODO: implement
        raise NotImplementedError


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
        print(f'Got call park locaation settings for {len(settings)} locations')

    def test_002_update_all(self):
        """
        get settings and use fill settings for update
        """
        # TODO: implement
        raise NotImplementedError

    def test_003_recall_hg_id(self):
        """
        change recall hunt group id
        """
        # TODO: implement
        raise NotImplementedError

    def test_004_recall_hg_option(self):
        """
        change recall hunt group option
        """
        # TODO: implement
        raise NotImplementedError

    def test_005_cp_settings_ring_pattern(self):
        """
        change ring_pattern
        """
        # TODO: implement
        raise NotImplementedError

    def test_006_cp_settings_recall_time(self):
        """
        change recall_time
        """
        # TODO: implement
        raise NotImplementedError

    def test_007_cp_settings_hunt_wait_time(self):
        """
        change hunt_wait_time
        """
        # TODO: implement
        raise NotImplementedError
