"""
Test cases for location access codes
"""
import random
from concurrent.futures import ThreadPoolExecutor

from tests.base import TestWithLocations

from wxc_sdk.common import AuthCode


class Test(TestWithLocations):

    def test_001_read_all(self):
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda location: self.api.telephony.access_codes.read(location_id=location.location_id),
                self.locations))
        print(f'Got access codes for {len(details)} locations')

    def test_002_create_delete(self):
        """
        create some codes and clean up after
        """
        target_location = random.choice(self.locations)
        ac = self.api.telephony.access_codes
        access_codes = ac.read(location_id=target_location.location_id)
        ac_set_before = set(c.code for c in access_codes)
        try:
            new_codes = (code for i in range(999)
                         if (code := str(1000 + i)) not in ac_set_before)
            new_access_codes = [AuthCode(code=next(new_codes), description=f'New code {i}') for i in range(10)]
            ac_set_new = set(ac.code for ac in new_access_codes)
            ac.create(location_id=target_location.location_id, access_codes=new_access_codes)
            access_codes_after = ac.read(location_id=target_location.location_id)
            # make sure that all old and new codes are in there
            ac_set_after = set(ac.code for ac in access_codes_after)
            self.assertTrue(ac_set_before <= ac_set_after, 'Not all access codes that existed before are still there')
            self.assertTrue(ac_set_new <= ac_set_after, 'Not all new access codes show up in list')
        finally:
            # restore old settings
            ac_codes = ac.read(location_id=target_location.location_id)
            # delete all existing
            ac.delete_codes(location_id=target_location.location_id, access_codes=ac_codes)
            if access_codes:
                # recreate the access codes that existed before
                ac.create(location_id=target_location.location_id, access_codes=access_codes)
            cleaned = ac.read(location_id=target_location.location_id)
            self.assertEqual(access_codes, cleaned)
