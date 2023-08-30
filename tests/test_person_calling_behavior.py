"""
Test for calling behavior settings
"""
import random
from asyncio import gather
from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar

from wxc_sdk.all_types import *
from tests.base import TestCaseWithUsers, async_test, TestCaseWithLog
from tests.testutil import calling_users


class TestRead(TestCaseWithUsers):

    @async_test
    async def test_001_read_one(self):
        """
        Read app services settings for one user
        """
        cb = self.async_api.person_settings.calling_behavior
        # pick the 1st user
        target_user = self.users[0]
        print(f'Trying to get calling behavior for {target_user.display_name}({target_user.emails[0]})')
        settings = await cb.read(person_id=target_user.person_id)
        print(f'Got settings: {settings.model_dump_json()}')
        self.assertTrue(settings.effective_behavior_type is not None)

    @async_test
    async def test_002_read_all(self):
        """
        Read app services settings of all users
        """
        cb = self.async_api.person_settings.calling_behavior

        settings = await gather(*[cb.read(person_id=user.person_id) for user in self.users],
                                return_exceptions=True)
        failed: list[tuple[Person, Exception]] = [(user, error) for user, error in zip(self.users, settings)
                                                  if isinstance(error, Exception)]
        if failed:
            print(f'Reading calling behavior failed for {len(failed)} users:')
            print('\n'.join(f'  {user.display_name}: {error}' for user, error in failed))

        settings_ok = [s for s in settings if not isinstance(s, Exception)]
        settings_ok: list[CallingBehavior]

        print(f'Got calling behavior for {len(settings_ok)} users')
        print('\n'.join(s.model_dump_json(exclude_none=False) for s in settings_ok))
        self.assertTrue(all(isinstance(s, CallingBehavior) and s.effective_behavior_type is not None
                            for s in settings),
                        'invalid/incomplete calling behavior for at least one user')


@dataclass(init=False)
class TestUpdate(TestCaseWithLog):
    users: ClassVar[list[Person]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.users = calling_users(api=cls.api)

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.calling_behavior.read(person_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            settings.behavior_type = settings.behavior_type or None
            restore = CallingBehavior(behavior_type=settings.behavior_type)
            self.api.person_settings.calling_behavior.configure(person_id=user.person_id, settings=restore)
            restored = self.api.person_settings.calling_behavior.read(person_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_switch_calling_behavior(self):
        """
        select different calling behavior for user
        """
        with self.target_user() as user:
            cba = self.api.person_settings.calling_behavior
            user: Person
            before = cba.read(person_id=user.person_id)
            self.assertIsNotNone(before.effective_behavior_type, 'Invalid calling behavior')
            behavior_types = list(BehaviorType)
            random.shuffle(behavior_types)
            new_behavior = next((b for b in behavior_types
                                 if before.behavior_type is None or before.behavior_type != b))
            settings = CallingBehavior(behavior_type=new_behavior)
            cba.configure(person_id=user.person_id, settings=settings)
            after = cba.read(person_id=user.person_id)
        self.assertEqual(settings.behavior_type,
                         after.behavior_type)
