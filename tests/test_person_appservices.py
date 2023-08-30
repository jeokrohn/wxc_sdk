"""
Test for app services settings
"""
import asyncio
import random
from contextlib import contextmanager
from dataclasses import dataclass
from unittest import skip

from wxc_sdk.all_types import Person, AppServicesSettings
from tests.base import TestCaseWithUsers, async_test


class TestRead(TestCaseWithUsers):

    @async_test
    async def test_001_read_all(self):
        """
        Read app services settings of all users
        """
        asa = self.async_api.person_settings.appservices
        settings = await asyncio.gather(*[asa.read(person_id=user.person_id)
                                          for user in self.users], return_exceptions=True)
        err = next((setting for setting in settings if isinstance(setting, Exception)), None)
        if err:
            raise err
        print(f'Got app services settings for {len(self.users)} users')
        print('\n'.join(s.model_dump_json() for s in settings))


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.appservices.read(person_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            self.api.person_settings.appservices.configure(person_id=user.person_id, settings=settings)
            restored = self.api.person_settings.appservices.read(person_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_ring_devices_for_click_to_dial_calls_enabled(self):
        """
        Toggle ring_devices_for_click_to_dial_calls_enabled on random user
        """
        with self.target_user() as user:
            asa = self.api.person_settings.appservices
            user: Person
            before = asa.read(person_id=user.person_id)
            settings = AppServicesSettings(
                ring_devices_for_click_to_dial_calls_enabled=not before.ring_devices_for_click_to_dial_calls_enabled)
            asa.configure(person_id=user.person_id, settings=settings)
            after = asa.read(person_id=user.person_id)
        self.assertEqual(settings.ring_devices_for_click_to_dial_calls_enabled,
                         after.ring_devices_for_click_to_dial_calls_enabled)
        after.ring_devices_for_click_to_dial_calls_enabled = before.ring_devices_for_click_to_dial_calls_enabled
        self.assertEqual(before, after)

    @skip('available_line_count cannot be changed')
    def test_002_available_line_count(self):
        """
        change available_line_count
        """
        with self.target_user() as user:
            asa = self.api.person_settings.appservices
            user: Person
            before = asa.read(person_id=user.person_id)
            settings = before.model_copy(deep=True)
            settings.available_line_count = settings.available_line_count - 1
            asa.configure(person_id=user.person_id, settings=settings)
            after = asa.read(person_id=user.person_id)
        self.assertEqual(settings.available_line_count, after.available_line_count)
        after.available_line_count = before.available_line_count
        self.assertEqual(before, after)
