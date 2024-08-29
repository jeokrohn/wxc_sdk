import asyncio
import json
import random
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import Union

from tests.base import TestWithLocations, async_test, TestCaseWithUsers
from wxc_sdk.common import OwnerType
from wxc_sdk.people import Person
from wxc_sdk.person_settings.ecbn import PersonECBN, ECBNDependencies, SelectedECBN
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.telephony.location.emergency_services import LocationEmergencyCallNotification


class TestEmergencyServices(TestWithLocations):

    def test_get_org_settings(self):
        """
        read org level settings
        """
        settings = self.api.telephony.emergency_services.read_emergency_call_notification()
        print(json.dumps(settings.model_dump(mode='json', by_alias=True),
                         indent=2))

    async def get_all_location_settings(self,
                                        return_exceptions: bool = True) -> list[
        Union[Exception, LocationEmergencyCallNotification]]:
        """
        Get all location level settings
        """

        api = self.async_api.telephony.location.emergency_services
        settings_list = await asyncio.gather(*[api.read_emergency_call_notification(location_id=loc.location_id)
                                               for loc in self.locations],
                                             return_exceptions=return_exceptions)
        return settings_list

    @async_test
    async def test_read_all_locations(self):
        """
        Get all location level settings
        """
        settings_list = await self.get_all_location_settings()
        err = None
        for location, setting in zip(self.locations, settings_list):
            location: TelephonyLocation
            print(f'Location "{location.name}"')
            if isinstance(setting, Exception):
                print(f'  !!Error: {setting}')
                err = err or setting
                continue
            setting: LocationEmergencyCallNotification
            print('\n'.join(f'  {line}'
                            for line in json.dumps(setting.model_dump(mode='json',
                                                                      by_alias=True),
                                                   indent=2).splitlines()))
        if err:
            raise err

    @async_test
    async def test_update_location_enable(self):
        """
        Try to enable a location
        """
        with self.no_log():
            settings_list = await self.get_all_location_settings(return_exceptions=False)
        candidates = [(loc, setting) for loc, setting in zip(self.locations, settings_list)
                      if setting.emergency_call_notification_enabled == False]
        if not candidates:
            self.skipTest('No locations with emergency call notification disabled')
        target, setting = random.choice(candidates)
        target: TelephonyLocation
        print(f'Testing in location "{target.name}"')
        setting: LocationEmergencyCallNotification
        update = LocationEmergencyCallNotification(emergency_call_notification_enabled=True,
                                                   email_address='jkrohn@cisco.com')
        api = self.api.telephony.location.emergency_services
        api.update_emergency_call_notification(location_id=target.location_id, setting=update)
        try:
            after = api.read_emergency_call_notification(location_id=target.location_id)
            self.assertEqual(update.emergency_call_notification_enabled,
                             after.emergency_call_notification_enabled)
            self.assertEqual(update.email_address,
                             after.email_address)
        finally:
            setting.email_address = setting.email_address or None
            api.update_emergency_call_notification(location_id=target.location_id, setting=setting)
            restored = api.read_emergency_call_notification(location_id=target.location_id)
            self.assertEqual(setting, restored)


class TestUserECBN(TestCaseWithUsers):

    @async_test
    async def test_get_ecbn_all_users(self):
        api = self.async_api.person_settings.ecbn
        settings_list = await asyncio.gather(*[api.read(entity_id=user.person_id) for user in self.users],
                                             return_exceptions=True)
        err = None
        for user, setting in zip(self.users, settings_list):
            user: Person
            print(f'USer "{user.display_name}"')
            if isinstance(setting, Exception):
                print(f'  !!Error: {setting}')
                err = err or setting
                continue
            setting: PersonECBN
            print('\n'.join(f'  {line}'
                            for line in json.dumps(setting.model_dump(mode='json',
                                                                      by_alias=True),
                                                   indent=2).splitlines()))
        if err:
            raise err

    @async_test
    async def test_get_dependencies_all_users(self):
        api = self.async_api.person_settings.ecbn
        dependencies_list = await asyncio.gather(*[api.dependencies(entity_id=user.person_id) for user in self.users],
                                                 return_exceptions=True)
        err = None
        for user, dependencies in zip(self.users, dependencies_list):
            user: Person
            print(f'USer "{user.display_name}"')
            if isinstance(dependencies, Exception):
                print(f'  !!Error: {dependencies}')
                err = err or dependencies
                continue
            dependencies: ECBNDependencies
            print('\n'.join(f'  {line}'
                            for line in json.dumps(dependencies.model_dump(mode='json',
                                                                           by_alias=True),
                                                   indent=2).splitlines()))
        if err:
            raise err

    def test_update_anita_hunt(self):
        """
        Toggle ECBN setting for Anita Hunt between direct line and location number
        """
        api = self.api.person_settings.ecbn
        target = next(user for user in self.users if user.display_name == "Anita Hunt")
        ecbn_settings = api.read(entity_id=target.person_id)
        print(json.dumps(ecbn_settings.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        selected = SelectedECBN.direct_line if ecbn_settings.selected != SelectedECBN.direct_line else (
            SelectedECBN.location_ecbn)
        api.configure(entity_id=target.person_id, selected=selected)
        print()
        ecbn_settings = api.read(entity_id=target.person_id)
        print(json.dumps(ecbn_settings.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        foo = 1
        self.assertEqual(selected, ecbn_settings.selected)

    def test_update_user_location_member(self):
        """

        :return:
        """
        # user phone numbers
        numbers = [number for number in self.api.telephony.phone_numbers(number_type=NumberType.number)
                   if number.owner and number.owner.owner_type == OwnerType.people]
        user_ids_by_location_id: dict[str, set[str]] = reduce(
            lambda r, e: r[e.location.id].add(e.owner.owner_id) or r,
            numbers,
            defaultdict(set))
        user_id_list = list(chain.from_iterable(user_ids
                                                for user_ids in user_ids_by_location_id.values()
                                                if len(user_ids) > 1))
        if not user_id_list:
            self.skipTest('No location with at least two users that have phone numbers')

        # pick a user
        target_user_id = random.choice(user_id_list)
        target_user_id: str
        target = next(user for user in self.users if user.person_id == target_user_id)
        target: Person
        location = self.api.telephony.location.details(location_id=target.location_id)
        print(f'User "{target.display_name}" in location "{location.name}"')

        # see if there are other available numbers
        numbers = list(self.api.telephony.phone_numbers(number_type=NumberType.number, owner_type=OwnerType.people,
                                                         location_id=target.location_id))
        other_numbers = [number for number in numbers if number.owner.owner_id != target.person_id]
        if not other_numbers:
            self.skipTest('No other user phone numbers found in location')

        target_number = random.choice(other_numbers)
        target_number: NumberListPhoneNumber

        # set ECBN to other member of location
        ecbn_api = self.api.person_settings.ecbn

        before = ecbn_api.read(entity_id=target.person_id)
        print('---Before:')
        print(json.dumps(before.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        dependencies_before = ecbn_api.dependencies(entity_id=target_number.owner.owner_id)
        print('---Dependencies before:')
        print(json.dumps(dependencies_before.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        ecbn_api.configure(entity_id=target.person_id, selected=SelectedECBN.location_member_number,
                           location_member_id=target_number.owner.owner_id)
        after = ecbn_api.read(entity_id=target.person_id)
        print('---After:')
        print(json.dumps(after.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        dependencies_after = ecbn_api.dependencies(entity_id=target_number.owner.owner_id)
        print('---Dependencies after:')
        print(json.dumps(dependencies_after.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        try:
            self.assertEqual(after.selected,
                             SelectedECBN.location_member_number)
            self.assertEqual(target_number.owner.owner_id,
                             after.location_member_info.member_id)
            self.assertEqual(dependencies_before.dependent_member_count + 1,
                             dependencies_after.dependent_member_count)
        finally:
            # reset the ECBN
            ecbn_api.configure(entity_id=target.person_id,
                               selected=before.selected,
                               location_member_id=(before.selected == SelectedECBN.location_member_number and
                                                   before.location_member_info.member_id or None))
            restored = ecbn_api.read(entity_id=target.person_id)
            print('---Restored:')
            print(json.dumps(restored.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

            dependencies_restored = ecbn_api.dependencies(entity_id=target_number.owner.owner_id)
            print('---Dependencies restored:')
            print(
                json.dumps(dependencies_restored.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
            self.assertEqual(dependencies_before, dependencies_restored)
            self.assertEqual(before.selected, restored.selected)
