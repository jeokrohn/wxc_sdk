"""
Test for outgoing permissions settings
"""
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.all_types import *
from wxc_sdk.rest import RestError
from .base import TestCaseWithUsers


class PermissionsOutMixin(TestCaseWithUsers):
    async def get_permissions_and_unknown_call_types(self) -> tuple[list[OutgoingPermissions], set[str]]:
        """
        Get outgoing permissions for all users and the set of unsupported call types
        """
        po = self.async_api.person_settings.permissions_out
        tasks = [po.read(person_id=user.person_id) for user in self.users]
        settings: list[OutgoingPermissions] = await asyncio.gather(*tasks)

        # explicitly defined call types are the defined attributes of CallingPermissions
        explicit_call_types = set(CallingPermissions.__fields__)

        # identify unknown call types: attributes of returned settings that are no explicitly defined
        unknown_call_types = set()
        for setting in settings:
            unknown_call_types.update(set(setting.calling_permissions.__dict__) - explicit_call_types)

        return settings, unknown_call_types

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


class TestRead(PermissionsOutMixin):

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

    @TestCaseWithUsers.async_test
    async def test_002_check_unknown_call_types(self):
        """
        API might return some unknown call types. Check for them and raise an exception so that we can update class
        definitions
        """
        settings, unknown_call_types = await self.get_permissions_and_unknown_call_types()

        print(f'Unknown call types: {", ".join(sorted(unknown_call_types))}')

        # tolerable call_types: call types we know are returned but should not be supported anymore
        tolerable_call_types = {'unknown', 'url_dialing', 'casual'}

        unexpected = unknown_call_types - tolerable_call_types
        self.assertTrue(not unexpected, f'Unexpected unknown call types: {", ".join(sorted(unexpected))}')

    def test_003_missing_auto_transfer_numbers(self):
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


class TestUnknownCallTypes(PermissionsOutMixin):
    """
    Try to figure out which unsupported call types exist and can't be used for an updates
    """

    @TestRead.async_test
    async def test_002_check_update(self):
        """
        determine which call types can be used in updates
        """
        # get unknown call types by reading person outgoing permission settings
        with self.no_log():
            _, call_types = await self.get_permissions_and_unknown_call_types()
        call_types |= set(CallingPermissions.__fields__)
        with self.target_user() as user:
            user: Person
            po = self.api.person_settings.permissions_out

            # try updates with each individual unknown call type
            ctp = CallTypePermission(action=Action.allow, transfer_enabled=False)
            cant_update = set()
            for call_type in sorted(call_types):
                setting = OutgoingPermissions(use_custom_enabled=True,
                                              calling_permissions=CallingPermissions(**{call_type: ctp}))
                try:
                    po.configure(person_id=user.person_id, settings=setting, drop_call_types={})
                except RestError as e:
                    if e.code == 25024:
                        cant_update.add(call_type)
                    else:
                        raise
            after = po.read(person_id=user.person_id)
        # after applying all the updates verify setting for all call types
        self.assertTrue(all(call_type in cant_update or permission == ctp
                            for call_type, permission in after.calling_permissions.__dict__.items()),
                        'Some permissions not set')
        # verify the expected set of un-settable call types
        self.assertEqual({'casual', 'unknown', 'url_dialing'}, cant_update)


class TestUpdate(PermissionsOutMixin):

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
