import asyncio
import json

from tests.base import TestWithLocations, async_test
from wxc_sdk.locations import Location


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
        if err:
            raise err
