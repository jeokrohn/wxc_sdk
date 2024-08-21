import asyncio
import base64
import random

from tests.base import TestWithLocations, async_test
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import UserType, OwnerType
from wxc_sdk.locations import Location
from wxc_sdk.person_settings.available_numbers import AvailableNumber
from wxc_sdk.telephony.location import CallBackSelected, LocationECBN


class Test(TestWithLocations):

    @async_test
    async def test_read_all(self):
        """
        get ECBN settings for all locations
        """
        settings = await asyncio.gather(*[self.async_api.telephony.location.read_ecbn(location_id=loc.location_id)
                                          for loc in self.locations])

    @async_test
    async def test_get_all_available(self):
        """
        get all available ECBN numbers
        """
        available_numbers = await asyncio.gather(
            *[self.async_api.telephony.location.ecbn_available_phone_numbers(location_id=loc.location_id)
              for loc in self.locations])

    @async_test
    async def test_update_ecbn(self):
        """
        try to update the ECBN setting of a location
        """
        with self.no_log():
            available_numbers = await asyncio.gather(
                *[self.async_api.telephony.location.ecbn_available_phone_numbers(location_id=loc.location_id)
                  for loc in self.locations])
        locations_and_numbers = [(loc, an) for loc, an in zip(self.locations, available_numbers) if an]
        if not locations_and_numbers:
            self.skipTest('No locations with available numbers')
        location, numbers = random.choice(locations_and_numbers)
        location: Location
        numbers: list[AvailableNumber]
        api = self.api.telephony.location
        before = api.read_ecbn(location_id=location.location_id)
        if before.selected == CallBackSelected.location_number:
            number = random.choice(numbers)
            number: AvailableNumber
            api.update_ecbn(location_id=location.location_id,
                            selected=CallBackSelected.location_member_number,
                            location_member_id=number.owner.owner_id)
            try:
                after = api.read_ecbn(location_id=location.location_id)
                self.assertEqual(after.selected, CallBackSelected.location_member_number)
                self.assertEqual(after.location_member_info.member_type, number.owner.owner_type)
                try:
                    self.assertEqual(after.location_member_info.member_id, number.owner.owner_id)
                except AssertionError:
                    print(f'Expected {webex_id_to_uuid(number.owner.owner_id)} got '
                          f'{webex_id_to_uuid(after.location_member_info.member_id)}')
                    raise
            finally:
                api.update_ecbn(location_id=location.location_id,
                                selected=CallBackSelected.location_number)
        else:
            api.update_ecbn(location_id=location.location_id,
                            selected=CallBackSelected.location_number)
            try:
                after = api.read_ecbn(location_id=location.location_id)
                self.assertEqual(after.selected, CallBackSelected.location_number)
            finally:
                api.update_ecbn(location_id=location.location_id,
                                selected=CallBackSelected.location_member_number,
                                location_member_id=before.location_member_info.member_id)

    @async_test
    async def test_update_ecbn_non_user(self):
        """
        try to update the ECBN setting of a location to number not assigned to user
        """
        with self.no_log():
            available_numbers, settings = await asyncio.gather(asyncio.gather(
                *[self.async_api.telephony.location.ecbn_available_phone_numbers(location_id=loc.location_id)
                  for loc in self.locations]),
                asyncio.gather(*[self.async_api.telephony.location.read_ecbn(location_id=loc.location_id)
                                 for loc in self.locations]))
        setting: LocationECBN
        an: list[AvailableNumber]
        locations_and_numbers = [(loc, ann)
                                 for loc, an, setting in zip(self.locations, available_numbers, settings)
                                 if ((ann := [n for n in an if n.owner.owner_type != OwnerType.people]) and
                                     setting.selected==CallBackSelected.location_number)]
        if not locations_and_numbers:
            self.skipTest('No locations with available numbers (non user) and ECBN set to location main number')
        location, numbers = random.choice(locations_and_numbers)
        location: Location
        numbers: list[AvailableNumber]
        api = self.api.telephony.location
        before = api.read_ecbn(location_id=location.location_id)
        number = random.choice(numbers)
        number: AvailableNumber
        api.update_ecbn(location_id=location.location_id,
                        selected=CallBackSelected.location_member_number,
                        location_member_id=number.owner.owner_id)
        try:
            after = api.read_ecbn(location_id=location.location_id)
            self.assertEqual(after.selected, CallBackSelected.location_member_number)
            err = None
            try:
                self.assertEqual(after.location_member_info.member_type, number.owner.owner_type)
            except AssertionError as e:
                print(f'Expected {number.owner.owner_type} got {after.location_member_info.member_type}')
                err = err or e
            try:
                self.assertEqual(after.location_member_info.member_id, number.owner.owner_id)
            except AssertionError:
                print(f'Expected {base64.b64decode(number.owner.owner_id+"==").decode()} got '
                      f'{base64.b64decode(after.location_member_info.member_id+"==").decode()}')
                err = err or e
            if err:
                raise err
        finally:
            api.update_ecbn(location_id=location.location_id,
                            selected=CallBackSelected.location_number)
