"""
Test for outgoing permissions settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.all_types import *
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

    def test_002_missing_auto_transfer_numbers(self):
        """
        apparently we are missing an API for person auto transfer numbers for outgoing permissions.
        This API exists for workspaces though
        """
        po = self.api.person_settings.permissions_out

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: po.read(person_id=user.person_id),
                                     self.users))
        print(f'Got outgoing permissions for {len(self.users)} users')
        print('\n'.join(f'{user.display_name}: {s.json()}' for user, s in zip(self.users, settings)))

        def get_numbers(person: Person):
            # /v1/workspaces/{workspaceId}/features/outgoingPermission/autoTransferNumbers
            url = f'https://webexapis.com/v1/people/{person.person_id}/features/outgoingPermission/autoTransferNumbers'
            return self.api.session.rest_get(url)

        with ThreadPoolExecutor() as pool:
            _ = list(pool.map(lambda user: get_numbers(user),
                              self.users))


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
            # enable custom settings
            settings.use_custom_enabled = True
            # toggle transfer enabled for toll calls
            toll_transfer_enabled = not settings.calling_permissions.toll.transfer_enabled
            print(f'Setting toll transfer enabled to {toll_transfer_enabled}')
            settings.calling_permissions.toll.transfer_enabled = toll_transfer_enabled
            print(f'Toll settings: {settings.calling_permissions.toll}')
            po.configure(person_id=user.person_id, settings=settings)
            after = po.read(person_id=user.person_id)
            self.assertTrue(after.use_custom_enabled)
            self.assertEqual(toll_transfer_enabled, after.calling_permissions.toll.transfer_enabled,
                             'Apparently permissions for call type local can\'t be set individually?')
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

    def test_005_local_transfer_enabled_false_all_call_types_individually(self):
        """
        set transfer_enabled to False for all call types one by one
        """
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(person_id=user.person_id)
            last_error = None
            for call_type in OutgoingPermissionCallType:
                settings: OutgoingPermissions = before.copy(deep=True)
                settings.use_custom_enabled = True
                permissions = settings.calling_permissions.for_call_type(call_type)
                permissions.transfer_enabled = False
                po.configure(person_id=user.person_id, settings=settings)
                after = po.read(person_id=user.person_id)
                try:
                    self.assertEqual(settings, after)
                except AssertionError as e:
                    last_error = e
                    result = 'fail'
                else:
                    result = 'ok'
                print(f'Setting transfer_enabled to False for call type "{call_type}": {result}')
                po.configure(person_id=user.person_id, settings=before)
        if last_error:
            raise last_error
