import asyncio
import random

from tests.base import TestWithLocations, async_test


class Test(TestWithLocations):
    proxy = True

    @async_test
    async def test_read_all(self):
        """
        get call captions settings for all locations
        """
        settings = await asyncio.gather(
            *[self.async_api.telephony.location.get_call_captions_settings(location_id=loc.location_id)
              for loc in self.telephony_locations], return_exceptions=True)
        for loc, setting in zip(self.telephony_locations, settings):
            if isinstance(setting, Exception):
                self.fail(f'Failed to get call captions settings for location "{loc.name}": {setting}')
        return

    def test_update(self):
        """
        try to update the call captions setting of a location
        """
        target = random.choice(self.telephony_locations)
        print(f'Testing update of call captions settings for location "{target.name}"')
        api = self.api.telephony.location
        before = api.get_call_captions_settings(location_id=target.location_id)
        try:
            update = before.model_copy(deep=True)
            update.location_closed_captions_enabled = not before.location_closed_captions_enabled
            update.use_org_settings_enabled = False
            api.update_call_captions_settings(location_id=target.location_id, settings=update)
            after = api.get_call_captions_settings(location_id=target.location_id)
            self.assertEqual(update, after)
        finally:
            # restore original settings
            api.update_call_captions_settings(location_id=target.location_id, settings=before)
            restored = api.get_call_captions_settings(location_id=target.location_id)
            self.assertEqual(before, restored)
        return