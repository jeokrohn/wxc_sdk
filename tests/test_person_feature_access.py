import asyncio
import json
import random

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.person_settings.feature_access import FeatureAccessLevel, FeatureAccessSettings, UserFeatureAccessSettings


class TestPersonFeatureAccess(TestCaseWithUsers):
    # proxy = True

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class with a Webex API instance and a list of users.
        """
        super().setUpClass()
        # Set the access token for the API session; apparently the API has challenges with integration tokens?
        # cls.api.session._tokens.access_token = \
        #     'OTMzNmIyODUtMjEzMi00ZTEwLThiODQtYWIzNWMwODRkM2JhM2RkZTU3NDYtMTBl_P0A1_36818b6f-ef07-43d1-b76f
        #     -ced79ab2e3e7'

    def test_read_default(self):
        """
        Read default feature access settings
        """
        api = self.api.person_settings.feature_access
        settings = api.read_default()
        self.assertIsNotNone(settings)
        print(json.dumps(settings.model_dump(mode='json', by_alias=True), indent=2))

    def test_update_default(self):
        """
        Update default feature access settings
        """
        api = self.api.person_settings.feature_access
        before = api.read_default()
        fields = before.__class__.model_fields
        field_to_modify = random.choice(list(fields))
        current_value = before.__getattribute__(field_to_modify)
        new_value = FeatureAccessLevel.full_access if current_value != FeatureAccessLevel.full_access else (
            FeatureAccessLevel.no_access)
        update_settings = FeatureAccessSettings(**{field_to_modify: new_value})
        try:
            print(f'Update {field_to_modify} from {current_value} to {new_value}')
            api.update_default(update_settings)
            after = api.read_default()
            self.assertEqual(getattr(after, field_to_modify), new_value)
            print(f'Updated {field_to_modify} from {current_value} to {new_value}')
        finally:
            # Restore the original settings
            api.update_default(before)
            after = api.read_default()
            self.assertEqual(after, before)
            print(f'Restored {field_to_modify} to {current_value}')

    @async_test
    async def test_update_default_and_check_impact_on_user(self):
        """
        Update default feature access settings and check impact on users
        Turns out that updating the oreg level settings does not update the values returned by the API for users
        """

        async def verify_users_have_defaults(defaults: FeatureAccessSettings):
            """
            Rad user level access settings for all users and verify that they match the default settings.
            """
            # get person settings for all users
            settings = await asyncio.gather(*[api.read(u.person_id) for u in self.users])
            settings: list[UserFeatureAccessSettings]

            # verify that person settings for users that user default settings match the default settings
            mismatched_users = [(u, s) for u, s in zip(self.users, settings)
                                if
                                s.user_org_settings_permission_enabled and s.user_settings_permissions != defaults]
            for user, setting in mismatched_users:
                print(f'User {user.display_name} has mismatched settings:')
                print('\n'.join(f'  {l}'
                                for l in json.dumps(setting.user_settings_permissions.model_dump(mode='json',
                                                                                                 by_alias=True),
                                                    indent=2).splitlines()))
            self.assertTrue(not mismatched_users)
            return

        api = self.async_api.person_settings.feature_access

        # get default settings
        default_settings = await api.read_default()

        try:
            # verify that all users have default settings
            try:
                await verify_users_have_defaults(default_settings)
            except AssertionError:
                # ignore mismatched users, as user level settings are not updated
                pass

            # update default settings
            fields = default_settings.__class__.model_fields
            field_to_modify = random.choice(list(fields))
            current_value = default_settings.__getattribute__(field_to_modify)
            new_value = FeatureAccessLevel.full_access if current_value != FeatureAccessLevel.full_access else (
                FeatureAccessLevel.no_access)
            new_value: FeatureAccessLevel
            update = FeatureAccessSettings(**{field_to_modify: new_value})
            print(f'Update {field_to_modify} from {current_value} to {new_value.value}')
            await api.update_default(update)

            # verify that all users have updated default settings
            updated_defaults = await api.read_default()
            self.assertEqual(getattr(updated_defaults, field_to_modify), new_value)
            try:
                await verify_users_have_defaults(updated_defaults)
            except AssertionError:
                # ignore mismatched users, as user level settings are not updated
                pass
        finally:
            # restore default settings
            await api.update_default(default_settings)

    @async_test
    async def test_read_all_users(self):
        """
        Read feature access settings for all calling users in the organization.
        """
        api = self.async_api.person_settings.feature_access
        print(f'Reading feature access settings for {len(self.users)} users...')
        # Read feature access settings for all users in parallel
        settings = await asyncio.gather(*[api.read(u.person_id) for u in self.users],
                                        return_exceptions=True)
        err = None
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                err = err or setting
                print(f'Error reading feature access for {user.display_name}: {setting}')
            setting: UserFeatureAccessSettings
            if setting.user_settings_permissions:
                print(user.display_name)
                print('\n'.join(f'  {l}' for l in json.dumps(setting.model_dump(mode='json',
                                                                                by_alias=True),
                                                             indent=2).splitlines()))
            else:
                print(f'{user.display_name} has no user settings permissions.')
                err = err or ValueError(f'User {user.display_name} has no user settings permissions.')
        if err:
            raise err

    def test_update_user(self):
        """
        Update feature access settings for a specific user.
        """
        api = self.api.person_settings.feature_access

        # test configuration
        target_display_name = 'Dustin Harris'

        if target_display_name is None:
            # Select a random user from the test users, excluding the admin user
            candidates = [u for u in self.users if u.display_name != 'admin@jkrohn-sandbox.wbx.ai']
            target_user = random.choice(candidates)
        else:
            # Find the user with the specified display name
            target_user = next((u for u in self.users if u.display_name == target_display_name), None)
            if not target_user:
                raise ValueError(f'User with display name {target_display_name} not found in test users.')

        default_settings = api.read_default()

        # pick a random field to modify
        fields = default_settings.__class__.model_fields
        field_to_modify = random.choice(list(fields))

        # toggle the feature access level
        current_value = default_settings.__getattribute__(field_to_modify)
        new_value = FeatureAccessLevel.full_access if current_value != FeatureAccessLevel.full_access else (
            FeatureAccessLevel.no_access)
        new_value: FeatureAccessLevel
        update_settings = FeatureAccessSettings(**{field_to_modify: new_value})

        print(f'Update {field_to_modify} for {target_user.display_name} from {current_value} to {new_value.value}')
        api.update(target_user.person_id, update_settings)
        after = api.read(target_user.person_id)
        try:
            self.assertEqual(getattr(after.user_settings_permissions, field_to_modify), new_value,
                             'modified field value does not match')
            self.assertTrue(all(getattr(after.user_settings_permissions, field) == getattr(default_settings, field)
                                for field in default_settings.__class__.model_fields
                                if field != field_to_modify),
                            'other fields should not be modified')
        finally:
            api.reset(target_user.person_id)
            restored = api.read(target_user.person_id)
            self.assertTrue(restored.user_org_settings_permission_enabled)
            self.assertEqual(restored.user_settings_permissions, default_settings)

    @async_test
    async def test_reset_all(self):
        """
        Reset feature access settings for all users in the organization.
        """
        api = self.async_api.person_settings.feature_access
        print(f'Resetting feature access settings for {len(self.users)} users...')
        # Reset feature access settings for all users in parallel
        results = await asyncio.gather(*[api.reset(u.person_id) for u in self.users],
                                       return_exceptions=True)
        print('All user feature access settings have been reset.')
        err = None
        for user, result in zip(self.users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f'Error resetting feature access for {user.display_name}: {result}')
        if err:
            raise err
