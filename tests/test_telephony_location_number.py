import asyncio
import functools
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from tests.testutil import us_location_info, available_tns, LocationInfo
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import NumberState, OwnerType
from wxc_sdk.locations import Location
from wxc_sdk.person_settings.available_numbers import AvailableNumber
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
        # this used to be the response
        # self.assertEqual(400, rest_error.exception.response.status_code)
        # self.assertEqual(25089, rest_error.exception.code)

        self.assertEqual(502, rest_error.exception.response.status_code)
        spark_error = rest_error.exception.response.headers.get('cisco-spark-error-codes')
        self.assertEqual('4251', spark_error)


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
        self.assertEqual(8363, rest_error.exception.code)
        self.assertEqual(25223, rest_error.exception.detail.error_code)


@dataclass(init=False)
class TestAvailable(TestWithLocations):
    validated_owners: ClassVar[set[str]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.validated_owner_ids = set()

    async def validate_owners(self, numbers: list[AvailableNumber], location_id: str):
        """
        Validate owners of numbers with owner
        """

        validators = {'PEOPLE': self.async_api.people.details,
                      'AUTO_ATTENDANT': functools.partial(self.async_api.telephony.auto_attendant.details,
                                                          location_id),
                      'CALL_QUEUE': functools.partial(self.async_api.telephony.callqueue.details,
                                                      location_id),
                      'VIRTUAL_LINE': self.async_api.telephony.virtual_lines.details,
                      'PAGING_GROUP': functools.partial(self.async_api.telephony.paging.details, location_id),
                      'HUNT_GROUP': functools.partial(self.async_api.telephony.huntgroup.details, location_id),
                      'PLACE': self.async_api.workspaces.details,
                      }

        async def validate_owner(number: AvailableNumber):
            """
            Validate owner of one number
            """
            if not number.owner:
                return
            owner_type = number.owner.owner_type
            owner_id = number.owner.owner_id

            if owner_type == OwnerType.voice_messaging:
                # voice messaging is not validated
                return

            # figure out the validator for the owner type
            validator = validators.get(owner_type, None)
            if not validator:
                raise ValueError(f'No validator for owner type "{owner_type}"')

            if owner_id in self.validated_owner_ids:
                # already validated or validating this owner
                return
            # note that we are validating this owner
            self.validated_owner_ids.add(owner_id)

            try:
                await validator(owner_id)
            except AsRestError as e:
                print(f'Error validating owner "{owner_type}/{owner_id}/{webex_id_to_uuid(owner_id)}": {e}')
                raise
            return

        results = await asyncio.gather(*[validate_owner(number)
                                         for number in numbers],
                                       return_exceptions=True)
        err = next((r for r in results if isinstance(r, Exception)),
                   None)
        return err

    async def for_all_locations(self, call: Callable, raise_error: bool = True):
        """
        Execute one number list method for all calling locations
        """
        results = await asyncio.gather(*[call(location_id=location.location_id) for location in self.locations],
                                       return_exceptions=True)
        err = None
        validate_tasks = []
        for location, result in zip(self.locations, results):
            location: Location
            if isinstance(result, Exception):
                print(f'{call.__name__}:!!! Error for location "{location.name}": {result}')
                err = err or result
                continue
            print(f'{call.__name__}: Location "{location.name}": {len(result)}')
            result: list[AvailableNumber]
            validate_tasks.append(self.validate_owners(numbers=result, location_id=location.location_id))
        if validate_tasks:
            validate_results = await asyncio.gather(*validate_tasks, return_exceptions=True)
            err = err or next((r for r in validate_results if isinstance(r, Exception)), None)

        if raise_error and err:
            raise err
        return err

    @async_test
    async def test_external_caller_id(self):
        """
        Get phone numbers available for external caller id
        """
        lapi = self.async_api.telephony.location
        await self.for_all_locations(lapi.phone_numbers_available_for_external_caller_id)

    @async_test
    async def test_all_available_phone_numbers(self):
        """
        Test all available phone number methods for all locations
        """
        lapi = self.async_api.telephony.location
        methods = [lapi.phone_numbers_available_for_external_caller_id,
                   lapi.phone_numbers,
                   lapi.webex_go_available_phone_numbers,
                   lapi.ecbn_available_phone_numbers,
                   lapi.call_intercept_available_phone_numbers]
        results = await asyncio.gather(*[self.for_all_locations(method, raise_error=True) for method in methods],
                                       return_exceptions=True)
        err = next((r for r in results if isinstance(r, Exception)), None)
        if err:
            raise err
