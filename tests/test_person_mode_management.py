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
        if not self._calling_users:
            with self.no_log():
                self.__class__._calling_users = calling_users(api=self.api)
        return self._calling_users

    @async_test
    async def test_available_features(self):
        """
        get available features for all calling users
        """
        available_features = await asyncio.gather(
            *[self.async_api.person_settings.mode_management.available_features(person_id=user.person_id)
              for user in self.users])
        available_features: list[list[AvailableFeature]]
        for user, features in zip(self.users, available_features):
            print(f'Available features for {user.display_name}({user.emails[0]}):')
            print(json.dumps(TypeAdapter(list[AvailableFeature]).dump_python(features, mode='json',
                                                                             by_alias=True,
                                                                             exclude_unset=True),
                             indent=2))

    @async_test
    async def test_assigned_features(self):
        """
        get assigned features for all calling users
        """
        assigned_features = await asyncio.gather(
            *[self.async_api.person_settings.mode_management.assigned_features(person_id=user.person_id)
              for user in self.users])
        assigned_features: list[list[ModeManagementFeature]]
        for user, features in zip(self.users, assigned_features):
            print(f'Assigned features for {user.display_name}({user.emails[0]}):')
            print(json.dumps(TypeAdapter(list[ModeManagementFeature]).dump_python(features, mode='json',
                                                                             by_alias=True,
                                                                             exclude_unset=True),
                             indent=2))

    def test_assign_features_to_user(self):
        """
        assign features to a user
        """
        # get available features for all calling users
        # pick a user with
        ...
