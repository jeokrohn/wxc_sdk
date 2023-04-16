"""
Tests for location PNC settings
"""
import random
from concurrent.futures import ThreadPoolExecutor

from wxc_sdk.telephony.pnc import NetworkConnectionType
from tests.base import TestWithLocations


class TestPNC(TestWithLocations):
    def test_001_read_all(self):
        pnc = self.api.telephony.pnc
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: pnc.read(location_id=loc.location_id),
                                     self.locations))
        print(f'got PNC settings for {len(settings)} locations')

    def test_002_update(self):
        target = random.choice(self.locations)
        pnc = self.api.telephony.pnc
        before = pnc.read(location_id=target.location_id)
        try:
            new_connection_type = next(ct for ct in NetworkConnectionType if ct != before)
            pnc.update(location_id=target.location_id, connection_type=new_connection_type)
            after = pnc.read(location_id=target.location_id)
            self.assertEqual(new_connection_type, after)
        finally:
            pnc.update(location_id=target.location_id, connection_type=before)
            after = pnc.read(location_id=target.location_id)
            self.assertEqual(before, after)
