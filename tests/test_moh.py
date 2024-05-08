"""
Test for MOH settings for persons, virtual lines, ...
"""
import asyncio
import json
import random

from tests.base import TestLocationsUsersWorkspacesVirtualLines, async_test
from wxc_sdk.as_api import AsMusicOnHoldApi
from wxc_sdk.people import Person


class TestMohSettings(TestLocationsUsersWorkspacesVirtualLines):

    @staticmethod
    async def read(entity: str, entity_id: str, api: AsMusicOnHoldApi):
        moh = await api.read(entity_id=entity_id)
        print(f'MoH settings for {entity}/{entity_id}:')
        print(json.dumps(moh.model_dump(mode='json'), indent=2))

    @async_test
    async def test_user_moh_settings(self):
        """
        Read MoH settings for all users
        """
        await asyncio.gather(*[self.read('user', user.person_id, self.async_api.person_settings.music_on_hold)
                               for user in self.users])

    def test_user_disable_moh(self):
        """
        Configure MoH settings for one user
        """
        target_user: Person = random.choice(self.users)
        api = self.api.person_settings.music_on_hold
        before = api.read(entity_id=target_user.person_id)
        update = before.model_copy(deep=True)
        update.moh_enabled = not update.moh_enabled
        print(f'Setting moh_enabvled for "{target_user.display_name}" to: {update.moh_enabled}')
        api.configure(entity_id=target_user.person_id, settings=update)
        try:
            after = api.read(entity_id=target_user.person_id)
            self.assertEqual(update, after)
        finally:
            api.configure(entity_id=target_user.person_id, settings=before)

    @async_test
    async def test_vl_moh_settings(self):
        """
        Read MoH settings for all virtual lines
        """
        await asyncio.gather(*[self.read('virtual line', vl.id,
                                         self.async_api.telephony.virtual_lines.music_on_hold)
                               for vl in self.virtual_lines])

