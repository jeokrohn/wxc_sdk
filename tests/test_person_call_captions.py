import asyncio
import random

from tests.base import TestCaseWithUsers, async_test


class Test(TestCaseWithUsers):
    proxy = True

    @async_test
    async def test_read_all(self):
        """
        Read person call captions settings for all users
        """
        settings = await asyncio.gather(
            *[self.async_api.person_settings.get_call_captions_settings(person_id=user.person_id)
              for user in self.users],
            return_exceptions=True)
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                print(f'Error getting call captions settings for user {user.display_name}: {setting}')

    def test_update(self):
        """
        try to update the call captions setting of a user
        """
        target = random.choice(self.users)
        print(f'Testing update of call captions settings for user "{target.display_name}"')
        api = self.api.person_settings
        before = api.get_call_captions_settings(person_id=target.person_id)
        try:
            update = before.model_copy(deep=True)
            update.user_closed_captions_enabled = not before.user_closed_captions_enabled
            update.use_location_settings_enabled = False
            api.update_call_captions_settings(person_id=target.person_id, settings=update)
            after = api.get_call_captions_settings(person_id=target.person_id)
            self.assertEqual(update, after)
        finally:
            # restore original settings
            api.update_call_captions_settings(person_id=target.person_id, settings=before)
            restored = api.get_call_captions_settings(person_id=target.person_id)
            self.assertEqual(before, restored)
        return