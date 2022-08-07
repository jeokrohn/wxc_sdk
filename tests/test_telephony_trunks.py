import re
from concurrent.futures import ThreadPoolExecutor
from random import choice
from unittest import skip

from tests.base import TestCaseWithLog
from wxc_sdk.telephony.prem_pstn.trunk import TrunkType


class TestListTrunks(TestCaseWithLog):
    """
    test cases for listing trunks
    """

    def test_001_list_all(self):
        """
        list all trunks
        :return:
        """
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        print(f'Got {len(trunks)} trunks')


class TestCreate(TestCaseWithLog):
    """
    Test cases to create trunks
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())
        cls.trunks = list(cls.api.telephony.prem_pstn.trunk.list())

    def test_001_create(self):
        """
        create a new trunk in one location
        :return:
        """
        location = choice(self.locations)
        trunk_names = set(t.name for t in self.trunks)
        trunk_name = next(name for i in range(1000) if (name := f'{location.name} {i}') not in trunk_names)
        print(f'Creating "{trunk_name}" in "{location.name}"')
        password = self.api.telephony.location.generate_password(location_id=location.location_id)
        new_trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                 location_id=location.location_id,
                                                                 password=password,
                                                                 trunk_type=TrunkType.registering)
        try:
            trunks = list(self.api.telephony.prem_pstn.trunk.list(location_name=location.name))
            self.assertTrue(any(t.trunk_id == new_trunk_id for t in trunks), 'trunk not found')
        finally:
            self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=new_trunk_id)


class TestDetails(TestCaseWithLog):
    """
    Tests on trunk details
    """

    def test_001_get_all_details(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda t: api.details(trunk_id=t.trunk_id),
                                    trunks))
        print(f'Got details for {len(trunks)} trunks')


class TestUsage(TestCaseWithLog):
    """
    Tests on trunk usage
    """

    def test_001_get_usage_all(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda t: api.usage(trunk_id=t.trunk_id),
                                    trunks))
        print(f'Got usage for {len(trunks)} trunks')

    def test_002_get_usage_dial_plan(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_dial_plan(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got dial plan usage for {len(trunks)} trunks')

    def test_003_get_usage_location_pstn(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_location_pstn(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got location PSTN usage for {len(trunks)} trunks')

    def test_004_get_usage_route_group(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_route_group(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got route group usage for {len(trunks)} trunks')


class TestTrunkTypes(TestCaseWithLog):
    def test_001_trunk_types(self):
        """
        get trunk types
        :return:
        """
        trunk_types = self.api.telephony.prem_pstn.trunk.trunk_types()
        print(f'Got {len(trunk_types)} trunk types')
        for tt in trunk_types:
            print(f'type: {tt.trunk_type.name}')
            for dt in tt.device_types:
                print(f'  device type: {dt.device_type} min; {dt.min_concurrent_calls} max: {dt.max_concurrent_calls}')


@skip
class TestDeleteTestTrunks(TestCaseWithLog):
    def test_001_delete_test_trunks(self):
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        to_delete = [trunk for trunk in trunks
                     if re.match(r'.+\s\d{2}$', trunk.name)]
        if not to_delete:
            self.skipTest('Nothing to do')
        with ThreadPoolExecutor() as pool:
            list(pool.map(
                lambda trunk: self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=trunk.trunk_id),
                to_delete))
