"""
Test for incoming permissions settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.all_types import *
from tests.base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read incoming permissions settings of all users
        """
        pi = self.api.person_settings.permissions_in

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: pi.read(entity_id=user.person_id),
                                     self.users))
        print(f'Got incoming permissions for {len(self.users)} users')
        print('\n'.join(f'{user.display_name}: {s.model_dump_json()}' for user, s in zip(self.users, settings)))


class TestUpdate(TestCaseWithUsers):

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.permissions_in.read(entity_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            # makes sure to clear list of monitored elements
            self.api.person_settings.permissions_in.configure(entity_id=user.person_id, settings=settings)
            restored = self.api.person_settings.permissions_in.read(entity_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_enabled(self):
        """
        toggle enabled
        """
        with self.target_user() as user:
            pi = self.api.person_settings.permissions_in
            user: Person
            before = pi.read(entity_id=user.person_id)
            settings: IncomingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = not settings.use_custom_enabled
            pi.configure(entity_id=user.person_id, settings=settings)
            after = pi.read(entity_id=user.person_id)
        self.assertEqual(settings, after)

    def test_002_external_transfer(self):
        """
        try all external_transfer options
        """
        with self.target_user() as user:
            pi = self.api.person_settings.permissions_in
            user: Person
            before = pi.read(entity_id=user.person_id)
            settings: IncomingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = True
            et = before.external_transfer
            for v in ExternalTransfer:
                if v == et:
                    continue
                settings.external_transfer = v
                pi.configure(entity_id=user.person_id, settings=settings)
                after = pi.read(entity_id=user.person_id)
                self.assertEqual(settings, after)
