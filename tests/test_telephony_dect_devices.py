"""
Testing DECT devices
"""
from random import choice

from tests.base import TestCaseWithLog, TestWithLocations
from wxc_sdk.telephony.dect_devices import DECTNetworkModel


class TestDectDevices(TestWithLocations):
    def test_001_create_network(self):
        api = self.api.telephony.dect_devices
        target_location = choice(self.locations)
        print(f'target location: "{target_location.name}"')
        id = api.create_dect_network(location_id=target_location.location_id,
                                     name='test',
                                     display_name='test',
                                     model=DECTNetworkModel.dms_cisco_dbs110,
                                     default_access_code_enabled=True,
                                     default_access_code='1234')
        print(f'created DECT network, id: {id}')
