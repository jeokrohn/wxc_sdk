import asyncio
import json
from dataclasses import dataclass
from typing import ClassVar

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, async_test
from tests.testutil import calling_users
from wxc_sdk.people import Person
from wxc_sdk.person_settings.mode_management import AvailableFeature, ModeManagementFeature


@dataclass(init=False, repr=False)
class TestPersonModeManagement(TestCaseWithLog):
    """
    person mode management tests
    """

    _calling_users: ClassVar[list[Person]] = None

    @property
    def users(self) -> list[Person]:
        # Cache calling users once so each test uses the same org snapshot.
        if not self._calling_users:
            with self.no_log():
                self.__class__._calling_users = calling_users(api=self.api)
        return self._calling_users

    @async_test
    async def test_available_features(self):
        """
        get available features for all calling users
        """
        # Read available mode-management features concurrently for broad read coverage.
        available_features = await asyncio.gather(
            *[
                self.async_api.person_settings.mode_management.available_features(person_id=user.person_id)
                for user in self.users
            ]
        )
        available_features: list[list[AvailableFeature]]

        # Print the returned features to make live-test fixture state easy to inspect.
        for user, features in zip(self.users, available_features):
            print(f'Available features for {user.display_name}({user.emails[0]}):')
            print(
                json.dumps(
                    TypeAdapter(list[AvailableFeature]).dump_python(
                        features, mode='json', by_alias=True, exclude_unset=True
                    ),
                    indent=2,
                )
            )

    @async_test
    async def test_assigned_features(self):
        """
        get assigned features for all calling users
        """
        # Read assigned mode-management features concurrently for broad read coverage.
        assigned_features = await asyncio.gather(
            *[
                self.async_api.person_settings.mode_management.assigned_features(person_id=user.person_id)
                for user in self.users
            ]
        )
        assigned_features: list[list[ModeManagementFeature]]

        # Print the returned assignments to make live-test fixture state easy to inspect.
        for user, features in zip(self.users, assigned_features):
            print(f'Assigned features for {user.display_name}({user.emails[0]}):')
            print(
                json.dumps(
                    TypeAdapter(list[ModeManagementFeature]).dump_python(
                        features, mode='json', by_alias=True, exclude_unset=True
                    ),
                    indent=2,
                )
            )

    def test_assign_features_to_user(self):
        """
        assign features to a user
        """
        api = self.api.person_settings.mode_management

        # Find a calling user with at least one feature that can be assigned.
        target = None
        available = []
        for user in self.users:
            available = list(api.available_features(person_id=user.person_id))
            if available:
                target = user
                break
        if target is None:
            self.skipTest('No user has mode-management features available for assignment')

        # Snapshot assigned feature IDs so the test can restore them exactly.
        before = api.assigned_features(person_id=target.person_id)
        before_ids = [feature.id for feature in before if feature.id]
        feature_id = next(feature.id for feature in available if feature.id)
        try:
            # Assign one available feature and verify it appears in the assigned list.
            api.assign_features(person_id=target.person_id, feature_ids=[feature_id])
            after = api.assigned_features(person_id=target.person_id)
            self.assertIn(feature_id, {feature.id for feature in after})
        finally:
            # Restore the original assignments and verify the feature set matches the snapshot.
            api.assign_features(person_id=target.person_id, feature_ids=before_ids)
            restored = api.assigned_features(person_id=target.person_id)
            self.assertEqual(set(before_ids), {feature.id for feature in restored})
