"""
Tests for location voice portals
"""

from tests.base import TestWithLocations
from concurrent.futures import ThreadPoolExecutor


class TestVoicePortal(TestWithLocations):
    def test_001_read_all(self):
        pa = self.api.telephony.voiceportal
        with ThreadPoolExecutor() as pool:
            portals = list(pool.map(lambda loc: pa.read(location_id=loc.location_id),
                                    self.locations))
        print(f'Got voice portal settings for {len(portals)} locations')

    def test_001_all_passcode_rules(self):
        pa = self.api.telephony.voiceportal
        with ThreadPoolExecutor() as pool:
            portals = list(pool.map(lambda loc: pa.passcode_rules(location_id=loc.location_id),
                                    self.locations))
        print(f'Got voice portal passcode rules for {len(portals)} locations')
