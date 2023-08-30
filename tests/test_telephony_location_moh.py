"""
Test cases UCM profiles
"""
import asyncio
import random
from contextlib import contextmanager

from tests.base import TestWithLocations, async_test
from wxc_sdk.locations import Location
from wxc_sdk.telephony.location.moh import LocationMoHSetting


class Test(TestWithLocations):

    @contextmanager
    def location_context(self):
        target_location = random.choice(self.locations)
        before = self.api.telephony.location.moh.read(location_id=target_location.location_id)
        try:
            yield target_location
        finally:
            self.api.telephony.location.moh.update(location_id=target_location.location_id,
                                                   settings=before)
            after = self.api.telephony.location.moh.read(location_id=target_location.location_id)
            self.assertEqual(before, after)

    @async_test
    async def test_001_read_all(self):
        moh = self.async_api.telephony.location.moh
        settings = await asyncio.gather(*[moh.read(location_id=loc.location_id) for loc in self.locations])
        print(f'Got {len(settings)} location MoH settings')

    def test_002_update_call_hold(self):
        """
        try to change call hold moh
        """
        moh = self.api.telephony.location.moh
        with self.location_context() as target_location:
            target_location: Location
            before = moh.read(location_id=target_location.location_id)
            call_hold = not before.call_hold_enabled
            settings = LocationMoHSetting(call_hold_enabled=call_hold,
                                          greeting=before.greeting)
            moh.update(location_id=target_location.location_id,
                       settings=settings)
            after = moh.read(location_id=target_location.location_id)
            self.assertEqual(settings.call_hold_enabled, after.call_hold_enabled)
            after.call_hold_enabled = before.call_hold_enabled
            self.assertEqual(before, after)

    def test_003_update_call_park(self):
        """
        try to change call park moh
        """
        moh = self.api.telephony.location.moh
        with self.location_context() as target_location:
            target_location: Location
            before = moh.read(location_id=target_location.location_id)
            call_park = not before.call_park_enabled
            settings = LocationMoHSetting(call_park_enabled=call_park,
                                          greeting=before.greeting)
            moh.update(location_id=target_location.location_id,
                       settings=settings)
            after = moh.read(location_id=target_location.location_id)
            self.assertEqual(settings.call_park_enabled, after.call_park_enabled)
            after.call_park_enabled = before.call_park_enabled
            self.assertEqual(before, after)
