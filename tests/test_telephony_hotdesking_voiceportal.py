"""
Tests for Hot Desking Sign-in via Voice Portal
"""
import asyncio
from random import choice

from tests.base import TestCaseWithUsers, TestWithLocations, async_test


class TestHotDeskingSigninViaVoicePortal(TestCaseWithUsers, TestWithLocations):
    @async_test
    async def test_user_get_all(self):
        """
        Get hotdesking signin setting for all usere
        """
        results = await asyncio.gather(
            *[self.async_api.telephony.hotdesking_voiceportal.user_get(person_id=user.person_id)
              for user in self.users],
            return_exceptions=True)
        err = next((r for r in results if isinstance(r, Exception)), None)
        if err:
            raise err
        print(f'Got hotdesking signin settings for {len(self.users)} users')

    def test_user_update(self):
        """
        Update hotdesking signin setting for a user
        """
        user = choice(self.users)
        before = self.api.telephony.hotdesking_voiceportal.user_get(person_id=user.person_id)
        try:
            setting = before.model_copy(deep=True)
            setting.enabled = not setting.enabled
            self.api.telephony.hotdesking_voiceportal.user_update(person_id=user.person_id,
                                                                  setting=setting)
            after = self.api.telephony.hotdesking_voiceportal.user_get(person_id=user.person_id)
            self.assertEqual(setting, after)
        finally:
            # restore old setting
            self.api.telephony.hotdesking_voiceportal.user_update(person_id=user.person_id, setting=before)

    @async_test
    async def test_location_get_all(self):
        """
        Get hotdesking signin setting for all locations
        """
        results = await asyncio.gather(
            *[self.async_api.telephony.hotdesking_voiceportal.location_get(location_id=location.location_id)
              for location in self.telephony_locations],
            return_exceptions=True)
        err = next((r for r in results if isinstance(r, Exception)), None)
        if err:
            raise err
        print(f'Got hotdesking signin settings for {len(self.locations)} locations')

    def test_location_update(self):
        """
        Update hotdesking signin setting for a location
        """
        location = choice(self.telephony_locations)
        before = self.api.telephony.hotdesking_voiceportal.location_get(location_id=location.location_id)
        try:
            setting = before.model_copy(deep=True)
            setting.enabled = not setting.enabled
            self.api.telephony.hotdesking_voiceportal.location_update(location_id=location.location_id,
                                                                      setting=setting)
            after = self.api.telephony.hotdesking_voiceportal.location_get(location_id=location.location_id)
            self.assertEqual(setting, after)
        finally:
            # restore old setting
            self.api.telephony.hotdesking_voiceportal.location_update(location_id=location.location_id, setting=before)
