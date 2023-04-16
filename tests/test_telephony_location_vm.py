"""
Test cases for location voicemail settings
"""
import random
from concurrent.futures import ThreadPoolExecutor

from wxc_sdk.telephony.location.vm import LocationVoiceMailSettings
from tests.base import TestWithLocations


class Test(TestWithLocations):

    def test_001_read_all(self):
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda location: self.api.telephony.location.voicemail.read(location_id=location.location_id),
                self.locations))
        print(f'Got voicemail settings for {len(details)} locations')

    def test_002_update(self):
        """
        Update VM settings for one locations
        """
        target_location = random.choice(self.locations)
        lvm = self.api.telephony.location.voicemail
        before = lvm.read(location_id=target_location.location_id)
        try:
            new_settings = LocationVoiceMailSettings(
                voicemail_transcription_enabled=not before.voicemail_transcription_enabled)
            lvm.update(location_id=target_location.location_id, settings=new_settings)
            after = lvm.read(location_id=target_location.location_id)
            self.assertEqual(new_settings, after)
        finally:
            # restore old settings
            lvm.update(location_id=target_location.location_id, settings=before)
            after = lvm.read(location_id=target_location.location_id)
            self.assertEqual(before, after)
