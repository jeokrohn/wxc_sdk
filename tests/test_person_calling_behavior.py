"""
Test for calling behavior settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass

from wxc_sdk.all_types import *
from .base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read app services settings of all users
        """
        cb = self.api.person_settings.calling_behavior

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: cb.read(person_id=user.person_id),
                                     self.users))
        print(f'Got app services settings for {len(self.users)} users')
        print('\n'.join(s.json(exclude_none=False) for s in settings))
        self.assertTrue(all(s.behavior_type is not None and s.effective_behavior_type is not None for s in settings),
                        'invalid/incomplete calling behavior for at least one user (check CALL-36213')


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):

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
            self.api.person_settings.calling_behavior.configure(person_id=user.person_id, settings=settings)
            restored = self.api.person_settings.calling_behavior.read(person_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_switch_calling_behavior(self):
        """
        select different calling behavior for usert
        """
        with self.target_user() as user:
            cba = self.api.person_settings.calling_behavior
            user: Person
            before = cba.read(person_id=user.person_id)
            self.assertIsNotNone(before.behavior_type, 'Invalid calling behavior')
            new_behavior = next((b for b in BehaviorType
                                 if before.behavior_type is None or before.behavior_type != b))
            settings = CallingBehavior(behavior_type=new_behavior)
            cba.configure(person_id=user.person_id, settings=settings)
            after = cba.read(person_id=user.person_id)
        self.assertEqual(settings.behavior_type,
                         after.behavior_type)
        after.behavior_type = before.behavior_type
        self.assertEqual(before, after)
