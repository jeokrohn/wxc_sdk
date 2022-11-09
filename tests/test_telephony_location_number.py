from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar

from tests.base import TestCaseWithLog
from tests.testutil import us_location_info, available_tns, LocationInfo
from wxc_sdk.common import NumberState
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import NumberType


@dataclass(init=False)
class NumberTest(TestCaseWithLog):
    location_info: ClassVar[list[LocationInfo]]

    @classmethod
    def setUpClass(cls) -> None:
        """
        get US locations with numbers; candidates for test
        """
        super().setUpClass()
        cls.location_info = us_location_info(api=cls.api)


@dataclass(init=False)
class TestAddAndActivate(NumberTest):
    target_location_info: LocationInfo = field(default=None)
    new_numbers: list[str] = field(default=None)

    def setUp(self) -> None:
        """
        Pick a target location and get some available phone numbers for that location
        :return:
        """
        if not self.location_info:
            self.skipTest('At least one US location with numbers required')
        # pick random location
        self.target_location_info = choice(self.location_info)
        print(f'Trying to add numbers to location "{self.target_location_info.location.name}"')
        # get some new numbers for that location
        self.new_numbers = available_tns(api=self.api,
                                         tn_prefix=self.target_location_info.main_number[:5],
                                         tns_requested=3)
        if not self.new_numbers:
            self.skipTest('Couldn\'t get new numbers')
        super().setUp()

    @contextmanager
    def add_context(self):
        """
        Add numbers to the target location and delete them again
        """
        # add numbers to location
        print(f'Adding {", ".join(self.new_numbers)}')
        self.api.telephony.location.number.add(location_id=self.target_location_info.location.location_id,
                                               phone_numbers=self.new_numbers,
                                               state=NumberState.inactive)
        try:
            # get numbers in location and check whether they are there
            numbers_after = list(
                self.api.telephony.phone_numbers(location_id=self.target_location_info.location.location_id,
                                                 number_type=NumberType.number,
                                                 available=True))
            # find all new phone numbers that are not in the numbers after the update
            # also the new numbers shouldn't have an owner and should not be active
            issues = [number for number in self.new_numbers
                      if (pn := next((n for n in numbers_after
                                      if n.phone_number == number), None)) is None
                      or pn.owner
                      or pn.state != NumberState.inactive]
            self.assertFalse(issues, f'Some numbers not added correctly: {", ".join(issues)}')
            try:
                yield
            finally:
                pass
        finally:
            # delete numbers we just added from location
            self.api.telephony.location.number.remove(location_id=self.target_location_info.location.location_id,
                                                      phone_numbers=self.new_numbers)
            numbers_after = list(
                self.api.telephony.phone_numbers(location_id=self.target_location_info.location.location_id,
                                                 number_type=NumberType.number,
                                                 available=True))
            # find new phone numbers that are still there
            issues = [number for number in self.new_numbers
                      if next((n for n in numbers_after
                               if n.phone_number == number), None) is not None]
            self.assertFalse(issues, f'Some numbers not removed correctly: {", ".join(issues)}')

    def test_001_add_and_delete(self):
        """
        Add some numbers to target location and delete them again
        """
        with self.add_context():
            pass

    def test_003_activate_some(self):
        """
        Add some numbers to target location and try to activate them
        """
        with self.add_context():
            # try to activate the numbers
            self.api.telephony.location.number.activate(location_id=self.target_location_info.location.location_id,
                                                        phone_numbers=self.new_numbers)
            numbers_after = list(
                self.api.telephony.phone_numbers(location_id=self.target_location_info.location.location_id,
                                                 number_type=NumberType.number,
                                                 available=True))
            # all new numbers now should be activatedd
            issues = [number for number in self.new_numbers
                      if (pn := next((n for n in numbers_after
                                      if n.phone_number == number), None)) is None
                      or pn.state != NumberState.active]
            self.assertFalse(issues, f'Some numbers not activated correctly: {", ".join(issues)}')

    def test_004_delete_not_existing(self):
        """
        Try to delete not existing numbers
        """
        with self.assertRaises(RestError) as rest_error:
            self.api.telephony.location.number.remove(location_id=self.target_location_info.location.location_id,
                                                      phone_numbers=[self.new_numbers[0]])
        self.assertEqual(400, rest_error.exception.response.status_code)
        self.assertEqual(25089, rest_error.exception.code)


class TestAddExisting(NumberTest):
    """
    Adding and existing number has to fail
    """

    def test_001_add_existing_number(self):
        """
        Adding an already existing number is expected to fail
        """
        if not self.location_info:
            self.skipTest('Need a US location with numbers')
        target = choice(self.location_info)
        with self.assertRaises(RestError) as rest_error:
            self.api.telephony.location.number.add(location_id=target.location.location_id,
                                                   phone_numbers=[target.main_number])
        self.assertEqual(409, rest_error.exception.response.status_code)
        self.assertEqual(25223, rest_error.exception.code)
