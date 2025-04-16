import asyncio
import json

from pydantic import TypeAdapter

from tests.base import TestWithLocations, async_test, TestCaseWithLog
from wxc_sdk.locations import Location
from wxc_sdk.telephony.call_recording import CallRecordingRegion, LocationComplianceAnnouncement


class TestCallRecording(TestWithLocations):

    def test_read_recording_info(self):
        info = self.api.telephony.call_recording.read()
        print(json.dumps(info.model_dump(mode='json'), indent=2))

    def test_read_terms_of_service(self):
        info = self.api.telephony.call_recording.read()
        tos = self.api.telephony.call_recording.read_terms_of_service(vendor_id=info.vendor_id)
        print(json.dumps(tos.model_dump(mode='json'), indent=2))

    def test_read_org_compliance_announcement(self):
        ca = self.api.telephony.call_recording.read_org_compliance_announcement()
        print(json.dumps(ca.model_dump(mode='json'), indent=2))

    @async_test
    async def test_read_location_compliance_announcement(self):
        results = await asyncio.gather(
            *[self.async_api.telephony.call_recording.read_location_compliance_announcement(location_id=loc.location_id)
              for loc in self.locations],
            return_exceptions=True)
        err = None
        for location, result in zip(self.locations, results):
            location: Location
            if isinstance(result, Exception):
                err = err or result
                print(f'failed to get location compliance announcement for "{location.name}": {err}')
            else:
                result: LocationComplianceAnnouncement
                print(f'location compliance announcement for "{location.name}":')
                print(json.dumps(result.model_dump(mode='json', exclude_unset=True), indent=2))
                print()
        if err:
            raise err


class TestSettings(TestCaseWithLog):
    def test_list_regions(self):
        regions = self.api.telephony.call_recording.get_call_recording_regions()
        print(f'got {len(regions)} regions')
        print(json.dumps(TypeAdapter(list[CallRecordingRegion]).dump_python(regions, mode='json'), indent=2))

    def test_get_org_vendors(self):
        vendors = self.api.telephony.call_recording.get_org_vendors()
        print(json.dumps(vendors.model_dump(mode='json', by_alias=True), indent=2))

    def test_get_org_vendor_id(self):
        vendor_id = self.api.telephony.call_recording.get_org_vendor_id()
        print(f'got vendor id: {vendor_id}')

    def test_org_users(self):
        users = list(self.api.telephony.call_recording.list_org_users())
        print(f'got {len(users)} users')

    @async_test
    async def location_vendor(self):
        ...
