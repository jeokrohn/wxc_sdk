"""
Test for outgoing permissions settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.types import *
from .base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read outgoing permissions settings of all users
        """
        po = self.api.person_settings.permissions_out

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: po.read(person_id=user.person_id),
                                     self.users))
        print(f'Got outgoing permissions for {len(self.users)} users')
        print('\n'.join(f'{user.display_name}: {s.json()}' for user, s in zip(self.users, settings)))


class TestUpdate(TestCaseWithUsers):

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.permissions_out.read(person_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            # makes sure to clear list of monitored elements
            self.api.person_settings.permissions_out.configure(person_id=user.person_id, settings=settings)
            restored = self.api.person_settings.permissions_out.read(person_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_enabled(self):
        """
        toggle enabled
        """
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(person_id=user.person_id)
            settings: OutgoingPermissions = before.copy(deep=True)
            settings.use_custom_enabled = not settings.use_custom_enabled
            po.configure(person_id=user.person_id, settings=settings)
            after = po.read(person_id=user.person_id)
        self.assertEqual(settings, after)

    def test_002_toggle_local_transfer_enabled(self):
        """
        toggle transfer_enabled for toll local calls
        """
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(person_id=user.person_id)
            settings: OutgoingPermissions = before.copy(deep=True)
            settings.use_custom_enabled = True
            settings.calling_permissions.toll.transfer_enabled = not settings.calling_permissions.toll.transfer_enabled
            po.configure(person_id=user.person_id, settings=settings)
            after = po.read(person_id=user.person_id)
            self.assertEqual(settings, after)

    def test_003_local_transfer_enabled_false_all_call_types(self):
        """
        set transfer_enabled to False for all call types
        """
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(person_id=user.person_id)
            settings: OutgoingPermissions = before.copy(deep=True)
            settings.use_custom_enabled = True
            for call_type in OutgoingPermissionCallType:
                permissions = settings.calling_permissions.for_call_type(call_type)
                permissions.transfer_enabled = False
            po.configure(person_id=user.person_id, settings=settings)
            after = po.read(person_id=user.person_id)
            self.assertEqual(settings, after)

    def test_004_block_all_call_types(self):
        """
        set action to block for all call types
        """
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(person_id=user.person_id)
            settings: OutgoingPermissions = before.copy(deep=True)
            settings.use_custom_enabled = True
            for call_type in OutgoingPermissionCallType:
                permissions = settings.calling_permissions.for_call_type(call_type)
                permissions.action = Action.block
            po.configure(person_id=user.person_id, settings=settings)
            after = po.read(person_id=user.person_id)
            self.assertEqual(settings, after)
