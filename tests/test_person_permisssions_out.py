"""
Test for outgoing permissions settings
"""

import asyncio
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from tests.base import TestCaseWithUsers, TestWithTempCallingUser
from wxc_sdk.all_types import *
from wxc_sdk.rest import RestError


class PermissionsOutMixin(TestCaseWithUsers):
    """
    Shared helpers for person outgoing permission tests.
    """

    async def get_permissions_and_unknown_call_types(self) -> tuple[list[OutgoingPermissions], set[str]]:
        """
        Get outgoing permissions for all users and the set of unsupported call types
        """
        po = self.async_api.person_settings.permissions_out

        # Read outgoing permissions for every user concurrently.
        tasks = [po.read(entity_id=user.person_id) for user in self.users]
        settings: list[OutgoingPermissions] = await asyncio.gather(*tasks)

        # explicitly defined call types are the defined attributes of CallingPermissions
        explicit_call_types = set(CallingPermissions.model_fields)

        # identify unknown call types: attributes of returned settings that are not explicitly defined
        unknown_call_types = set()
        for setting in settings:
            unknown_call_types.update(set(cp for cp, _ in setting.calling_permissions) - explicit_call_types)

        return settings, unknown_call_types

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        # Pick a real calling user and snapshot their permission settings.
        user = random.choice(self.users)
        settings = self.api.person_settings.permissions_out.read(entity_id=user.person_id)
        try:
            yield user
        finally:
            # Restore old settings and verify no permission change remains.
            self.api.person_settings.permissions_out.configure(entity_id=user.person_id, settings=settings)
            restored = self.api.person_settings.permissions_out.read(entity_id=user.person_id)
            self.assertEqual(settings, restored)


class TestRead(PermissionsOutMixin):
    """
    Read-only coverage for person outgoing permission settings and model compatibility.
    """

    def test_001_read_all(self):
        """
        Read outgoing permissions settings of all users
        """
        po = self.api.person_settings.permissions_out

        # Read each user's outgoing permission settings in parallel.
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: po.read(entity_id=user.person_id), self.users))
        settings: list[OutgoingPermissions]

        # Print the settings for live-test diagnostics.
        print(f'Got outgoing permissions for {len(self.users)} users')
        print('\n'.join(f'{user.display_name}: {s.model_dump_json()}' for user, s in zip(self.users, settings)))

    @TestCaseWithUsers.async_test
    async def test_002_check_unknown_call_types(self):
        """
        API might return some unknown call types. Check for them and raise an exception so that we can update class
        definitions
        """
        # Read all permissions and collect any call types missing from the SDK model.
        settings, unknown_call_types = await self.get_permissions_and_unknown_call_types()

        print(f'Unknown call types: {", ".join(sorted(unknown_call_types))}')

        # tolerable call_types: call types we know are returned but should not be supported anymore
        tolerable_call_types = {'unknown', 'url_dialing', 'casual'}

        # Fail only for unknown call types that are not already tolerated by the SDK tests.
        unexpected = unknown_call_types - tolerable_call_types
        self.assertTrue(not unexpected, f'Unexpected unknown call types: {", ".join(sorted(unexpected))}')


class TestUnknownCallTypes(PermissionsOutMixin):
    """
    Try to figure out which unsupported call types exist and can't be used for an updates
    """

    @TestRead.async_test
    async def test_002_check_update(self):
        """
        determine which call types can be used in updates
        """
        ignore_call_types = {'toll', 'local'}

        # get unknown call types by reading person outgoing permission settings
        with self.no_log():
            _, call_types = await self.get_permissions_and_unknown_call_types()
        call_types |= set(CallingPermissions.model_fields)
        call_types -= ignore_call_types

        # Pick a random user whose settings will be restored by the context manager.
        with self.target_user() as user:
            user: Person
            print(f'testing with user "{user.display_name}"')
            po = self.api.person_settings.permissions_out

            # Try updates with each individual unknown or known call type.
            ctp = CallTypePermission(action=Action.allow, transfer_enabled=False)
            cant_update = set()
            for call_type in sorted(call_types):
                setting = OutgoingPermissions(
                    use_custom_enabled=True, calling_permissions=CallingPermissions(**{call_type: ctp})
                )
                try:
                    po.configure(entity_id=user.person_id, settings=setting, drop_call_types={})
                except RestError as e:
                    if e.code in {25321, 25024}:
                        print(f'Can\'t update call type "{call_type}": {e}')
                        cant_update.add(call_type)
                    else:
                        raise
            after = po.read(entity_id=user.person_id)

        # after applying all the updates verify setting for all call types
        err = False
        for call_type, permission in after.calling_permissions.__dict__.items():
            if call_type in ignore_call_types:
                continue
            print(f'Call type "{call_type}": {permission}')
            if call_type in cant_update:
                print('  was not updated')
                continue
            if permission == ctp:
                continue
            err = True
        self.assertFalse(err, 'Some permissions not set')

        # some permissions can't be updated b/c we are in a trial org
        cant_update -= {'premium_services_i', 'premium_services_ii', 'international'}
        self.assertFalse(cant_update)


class TestUpdate(PermissionsOutMixin):
    """
    Restore-safe update coverage for person outgoing permission category controls.
    """

    def test_001_toggle_enabled(self):
        """
        toggle enabled
        """
        # Use the restore-safe target-user context for a single settings toggle.
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person

            # Toggle the custom outgoing-permissions switch.
            before = po.read(entity_id=user.person_id)
            settings: OutgoingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = not settings.use_custom_enabled
            settings.use_custom_permissions = settings.use_custom_enabled
            po.configure(entity_id=user.person_id, settings=settings)
            after = po.read(entity_id=user.person_id)

        # Verify the changed settings were applied inside the context.
        self.assertEqual(settings, after)

    def test_002_toggle_national_transfer_enabled(self):
        """
        toggle transfer_enabled for national calls
        """
        # Use the restore-safe target-user context for a national-call toggle.
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person

            # Enable custom permissions and toggle national transfer behavior.
            before = po.read(entity_id=user.person_id)
            settings: OutgoingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = True
            settings.use_custom_permissions = True
            national_transfer_enabled = not settings.calling_permissions.national.transfer_enabled
            print(f'Setting national transfer enabled to {national_transfer_enabled}')
            settings.calling_permissions.national.transfer_enabled = national_transfer_enabled
            print(f'National settings: {settings.calling_permissions.national}')
            po.configure(entity_id=user.person_id, settings=settings)

            # Verify custom settings and the national transfer flag were applied.
            after = po.read(entity_id=user.person_id)
            self.assertTrue(after.use_custom_enabled)
            self.assertTrue(after.use_custom_permissions)
            self.assertEqual(
                national_transfer_enabled,
                after.calling_permissions.national.transfer_enabled,
                "Apparently permissions for call type national can't be set individually?",
            )
            self.assertEqual(settings, after)

    def test_003_transfer_enabled_false_all_call_types(self):
        """
        set transfer_enabled to False for all call types
        """
        # Use the restore-safe target-user context for a bulk transfer update.
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person

            # Enable custom permissions and turn off transfer for every modeled call type.
            before = po.read(entity_id=user.person_id)
            settings: OutgoingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = True
            settings.use_custom_permissions = True
            for call_type in OutgoingPermissionCallType:
                permissions = settings.calling_permissions.for_call_type(call_type)
                if permissions is not None:
                    permissions.transfer_enabled = False
            po.configure(entity_id=user.person_id, settings=settings)

            # Verify the full settings model matches the requested update.
            after = po.read(entity_id=user.person_id)
            self.assertEqual(settings, after)

    def test_004_block_all_call_types(self):
        """
        set action to block for all call types
        """
        # Use the restore-safe target-user context for a bulk block update.
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person

            # Enable custom permissions and block every modeled call type.
            before = po.read(entity_id=user.person_id)
            settings: OutgoingPermissions = before.model_copy(deep=True)
            settings.use_custom_enabled = True
            settings.use_custom_permissions = True
            for call_type in OutgoingPermissionCallType:
                permissions = settings.calling_permissions.for_call_type(call_type)
                if permissions is not None:
                    permissions.transfer_enabled = False
                    permissions.action = Action.block
            po.configure(entity_id=user.person_id, settings=settings)
            after = po.read(entity_id=user.person_id)

            # Verify the full settings model matches the requested block update.
            self.assertEqual(settings, after)

    def test_005_local_transfer_enabled_false_all_call_types_individually(self):
        """
        set transfer_enabled to False for all call types one by one
        """
        # Use the restore-safe target-user context for per-call-type updates.
        with self.target_user() as user:
            po = self.api.person_settings.permissions_out
            user: Person
            before = po.read(entity_id=user.person_id)
            last_error = None

            # Apply a single-call-type transfer update for every modeled call type.
            for call_type in OutgoingPermissionCallType:
                settings: OutgoingPermissions = before.model_copy(deep=True)
                settings.use_custom_enabled = True
                settings.use_custom_permissions = True
                permissions = settings.calling_permissions.for_call_type(call_type)
                if permissions is None:
                    continue
                permissions.transfer_enabled = False
                po.configure(entity_id=user.person_id, settings=settings)
                after = po.read(entity_id=user.person_id)
                try:
                    self.assertEqual(settings, after)
                except AssertionError as e:
                    last_error = e
                    result = 'fail'
                else:
                    result = 'ok'
                print(f'Setting transfer_enabled to False for call type "{call_type}": {result}')

                # Restore old settings between call types so each attempt is isolated.
                po.configure(entity_id=user.person_id, settings=before)

        # Raise the last mismatch after all call types were exercised.
        if last_error:
            raise last_error


class TestPersonOutgoingPermissionChildren(TestWithTempCallingUser):
    """
    Focused CRUD tests for person-level outgoing permission child APIs.
    """

    def test_access_codes_create_list_delete_restore(self):
        """
        Create, list, delete, and restore outgoing permission access codes for a disposable user.
        """
        api = self.api.person_settings.permissions_out.access_codes

        # Snapshot current access-code category settings and choose an unused numeric code.
        before = api.read(entity_id=self.user.person_id)
        code = None
        try:
            existing = {ac.code for ac in before.access_codes or []}
            code = next(candidate for i in range(9000, 10000) if (candidate := f'{i}') not in existing)

            # Create the temporary access code and verify it appears in the read response.
            api.create(entity_id=self.user.person_id, code=code, description=f'test_{code}')
            after_create = api.read(entity_id=self.user.person_id)
            created = next((ac for ac in after_create.access_codes or [] if ac.code == code), None)
            self.assertIsNotNone(created)

            # Delete the temporary code and verify it disappears from the read response.
            api.modify(entity_id=self.user.person_id, delete_codes=[code])
            code = None
            after_delete = api.read(entity_id=self.user.person_id)
            self.assertIsNone(next((ac for ac in after_delete.access_codes or [] if ac.code == created.code), None))
        finally:
            # Restore category control and remove the created code if an earlier step failed.
            delete_codes = [code] if code else None
            if delete_codes or before.use_custom_access_codes is not None:
                api.modify(
                    entity_id=self.user.person_id,
                    use_custom_access_codes=before.use_custom_access_codes,
                    delete_codes=delete_codes,
                )

    def test_digit_patterns_create_read_update_delete_restore(self):
        """
        Create, read, update, delete, and restore outgoing permission digit patterns.
        """
        api = self.api.person_settings.permissions_out.digit_patterns

        # Snapshot current digit-pattern category settings and prepare a unique temporary pattern.
        before = api.get_digit_patterns(entity_id=self.user.person_id)
        pattern_id = None
        try:
            suffix = uuid.uuid4().hex[:8]
            pattern = DigitPattern(
                name=f'test_{suffix}',
                pattern=f'77{int(suffix, 16) % 10000:04d}',
                action=Action.block,
                transfer_enabled=False,
            )

            # Create the pattern and verify its details.
            pattern_id = api.create(entity_id=self.user.person_id, pattern=pattern)
            details = api.details(entity_id=self.user.person_id, digit_pattern_id=pattern_id)
            self.assertEqual(pattern.name, details.name)
            self.assertEqual(pattern.action, details.action)

            # Update name/action/transfer settings and verify the detail endpoint reflects them.
            details.name = f'{details.name}_updated'
            details.action = Action.allow
            details.transfer_enabled = True
            api.update(entity_id=self.user.person_id, settings=details)
            after_update = api.details(entity_id=self.user.person_id, digit_pattern_id=pattern_id)
            self.assertEqual(details.name, after_update.name)
            self.assertEqual(details.action, after_update.action)
            self.assertEqual(details.transfer_enabled, after_update.transfer_enabled)

            # Delete the temporary pattern and verify it disappears from the list.
            api.delete(entity_id=self.user.person_id, digit_pattern_id=pattern_id)
            pattern_id = None
            after_delete = api.get_digit_patterns(entity_id=self.user.person_id)
            self.assertNotIn(details.name, {p.name for p in after_delete.digit_patterns or []})
        finally:
            # Clean up the created pattern and restore the category control setting.
            if pattern_id is not None:
                api.delete(entity_id=self.user.person_id, digit_pattern_id=pattern_id)
            api.update_category_control_settings(
                entity_id=self.user.person_id,
                use_custom_digit_patterns=before.use_custom_digit_patterns,
            )

    def test_transfer_numbers_modify_restore(self):
        """
        Modify outgoing permission transfer numbers and restore the original values.
        """
        api = self.api.person_settings.permissions_out.transfer_numbers

        # Snapshot transfer-number settings, or skip if the person endpoint is absent in this org.
        try:
            before = api.read(entity_id=self.user.person_id)
        except RestError as e:
            if e.response.status_code == 404:
                self.skipTest('Person outgoing permission transfer numbers endpoint is not available')
            raise
        try:
            # Configure all three temporary transfer numbers.
            update = AutoTransferNumbers(
                use_custom_transfer_numbers=True,
                auto_transfer_number1='+12025550100',
                auto_transfer_number2='+12025550101',
                auto_transfer_number3='+12025550102',
            )
            api.configure(entity_id=self.user.person_id, settings=update)

            # Verify each configured number is returned by the read endpoint.
            after = api.read(entity_id=self.user.person_id)
            self.assertTrue(after.use_custom_transfer_numbers)
            self.assertEqual(update.auto_transfer_number1, after.auto_transfer_number1)
            self.assertEqual(update.auto_transfer_number2, after.auto_transfer_number2)
            self.assertEqual(update.auto_transfer_number3, after.auto_transfer_number3)
        finally:
            # Restore original transfer-number settings, converting unset numbers to API-clearing empty strings.
            api.configure(entity_id=self.user.person_id, settings=before.configure_unset_numbers)
