"""
Test for person numbers
"""
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar

from wxc_sdk.common import PatternAction, RingPattern
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.person_settings.numbers import UpdatePersonNumbers, UpdatePersonPhoneNumber, PersonNumbers
from .base import TestCaseWithUsers
from .testutil import LocationInfo, us_location_info, available_tns


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read numbers all users
        """
        nu = self.api.person_settings.numbers

        with ThreadPoolExecutor() as pool:
            _ = list(pool.map(lambda user: nu.read(person_id=user.person_id),
                              self.users))
        print(f'Got numbers for {len(self.users)} users')

    def test_002_direct_number_format(self):
        """
        Read numbers all users, verify number format for direct number
        """
        nu = self.api.person_settings.numbers

        with ThreadPoolExecutor() as pool:
            numbers = list(pool.map(lambda user: nu.read(person_id=user.person_id),
                                    self.users))

        # find all users and their direct numbers not starting with '+'
        direct_number_issues = [(user, direct_numbers) for user, numbers in zip(self.users, numbers)
                                if (direct_numbers := [number.direct_number
                                                       for number in numbers.phone_numbers
                                                       if number.direct_number and not
                                                       number.direct_number.startswith('+')])]
        print('\n'.join(f'{user.display_name}: {", ".join(numbers)}' for user, numbers in direct_number_issues))
        self.assertTrue(not direct_number_issues), 'Some direct numbers are not +E.164'


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):
    """
    Assign and unassign numbers to person
    """
    us_locations: ClassVar[list[LocationInfo]]
    us_users: list[Person] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.us_locations = us_location_info(api=cls.api)

    def setUp(self) -> None:
        super().setUp()
        if not self.us_locations:
            self.skipTest('Need US locations with numbers to run the test')
        us_location_ids = set(loc.location.location_id for loc in self.us_locations)
        self.us_users = [u for u in self.users
                         if u.location_id in us_location_ids]
        if not self.us_users:
            self.skipTest('Need some US calling users to run the test')

    @contextmanager
    def update_user_context(self):
        # pick a US calling user
        user = choice(self.users)
        location_info = next((loc_info for loc_info in self.us_locations
                              if loc_info.location.location_id == user.location_id), None)
        self.assertIsNotNone(location_info)
        print(f'Testing with user {user.display_name}({user.emails[0]}) in location "{location_info.location.name}"')

        # current numbers of the user
        numbers = self.api.person_settings.numbers.read(person_id=user.person_id)

        # some available TNs in the location
        available_tns_in_location = [n.phone_number for n in location_info.numbers
                                     if not n.owner and not n.main_number]
        new_tn = None
        if not available_tns_in_location:
            new_tn = available_tns(api=self.api, tn_prefix=location_info.main_number[:5], tns_requested=3)[0]
            tn = new_tn
        else:
            # pick a random TN
            tn = choice(available_tns_in_location)
        if new_tn:
            print(f'Temporarily adding new number to location "{location_info.location.name}": {tn}')
            self.api.telephony.location.number.add(location_id=location_info.location.location_id,
                                                   phone_numbers=[new_tn])
        try:
            try:
                yield location_info.location, user, numbers, tn
            finally:
                # remove TN again
                print(f'Removing {tn} from user {user.display_name}({user.emails[0]}) '
                      f'in location "{location_info.location.name}"')
                update = UpdatePersonNumbers(enable_distinctive_ring_pattern=numbers.distinctive_ring_enabled,
                                             phone_numbers=[
                                                 UpdatePersonPhoneNumber(action=PatternAction.delete,
                                                                         external=tn)])
                self.api.person_settings.numbers.update(person_id=user.person_id,
                                                        update=update)
                numbers_after = self.api.person_settings.numbers.read(person_id=user.person_id)
                self.assertEqual(numbers, numbers_after)
        finally:
            # remove new TN (if needed)
            if new_tn:
                print(f'Removing number from location "{location_info.location.name}": {tn}')
                self.api.telephony.location.number.remove(location_id=location_info.location.location_id,
                                                          phone_numbers=[new_tn])

    def test_001_update_add_tn(self):
        """
        Try to add an alternate TN to a user
        """
        with self.update_user_context() as ctx:
            location, user, numbers, tn = ctx
            location: Location
            user: Person
            numbers: PersonNumbers
            tn: str

            print(f'Adding {tn} to user {user.display_name}({user.emails[0]}) '
                  f'in location "{location.name}"')
            ring_pattern = RingPattern.short_short_long
            update = UpdatePersonNumbers(enable_distinctive_ring_pattern=True,
                                         phone_numbers=[
                                             UpdatePersonPhoneNumber(action=PatternAction.add,
                                                                     external=tn,
                                                                     ring_pattern=ring_pattern)])
            self.api.person_settings.numbers.update(person_id=user.person_id,
                                                    update=update)
            # validation
            numbers_after = self.api.person_settings.numbers.read(person_id=user.person_id)
            self.assertEqual(True, numbers_after.distinctive_ring_enabled)
            for i, pn in enumerate(numbers.phone_numbers):
                self.assertEqual(pn, numbers_after.phone_numbers[i])
            pn = numbers_after.phone_numbers[-1]
            self.assertEqual(False, pn.primary)
            self.assertIsNone(pn.extension)
            self.assertEqual(tn, pn.direct_number)
            self.assertEqual(ring_pattern, pn.ring_pattern)
