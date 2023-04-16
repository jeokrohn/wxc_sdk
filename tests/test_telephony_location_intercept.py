"""
Test cases for location intercept
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.locations import Location
from wxc_sdk.person_settings.call_intercept import InterceptSetting
from tests.base import TestWithLocations


class TestIntercept(TestWithLocations):
    @contextmanager
    def context(self):
        li = self.api.telephony.location.intercept
        target = random.choice(self.locations)
        before = li.read(location_id=target.location_id)
        try:
            yield target
        finally:
            li.configure(location_id=target.location_id, settings=before)
            after = li.read(location_id=target.location_id)
            self.assertEqual(before, after)

    def test_001_read_all(self):
        li = self.api.telephony.location.intercept
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: li.read(location_id=loc.location_id),
                                     self.locations))
        print(f'Got call intercept settings for {len(settings)} locations')

    def test_002_enable(self):
        """
        enable call intercept for a location
        """
        li = self.api.telephony.location.intercept
        with self.context() as target_location:
            target_location: Location
            before = li.read(location_id=target_location.location_id)
            enable = not before.enabled
            settings = InterceptSetting(enabled=enable)
            li.configure(location_id=target_location.location_id, settings=settings)
            after = li.read(location_id=target_location.location_id)
            self.assertEqual(enable, after.enabled)
            after.enabled = before.enabled
            self.assertEqual(before, after)
