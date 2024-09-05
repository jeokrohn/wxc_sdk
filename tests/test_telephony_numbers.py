"""
Unit test for numbers
"""
import base64
import random
from dataclasses import dataclass, field
from typing import ClassVar, Optional

from wxc_sdk.all_types import *
from tests.base import TestCaseWithLog, TestCaseWithUsers
from tests.testutil import LocationInfo, us_location_info, available_tns
from wxc_sdk.telephony import TelephonyType


class TestNumbers(TestCaseWithLog):
    """
    Test cases for phone numbers
    """

    def test_001_all_numbers(self):
        numbers = list(self.api.telephony.phone_numbers())
        print(f'Got {len(numbers)} numbers')

    def test_002_active(self):
        numbers = list(self.api.telephony.phone_numbers(state='ACTIVE'))
        print(f'Got {len(numbers)} active numbers')

    def test_003_extensions(self):
        numbers = list(self.api.telephony.phone_numbers(number_type='EXTENSION'))
        print(f'Got {len(numbers)} extensions')

    def test_004_phone_numbers(self):
        numbers = list(self.api.telephony.phone_numbers(number_type='NUMBER'))
        print(f'Got {len(numbers)} TNs')

    def test_005_details(self):
        details = self.api.telephony.phone_number_details()
        print(f'Number details: {details}')

    def test_006_included_pstn(self):
        numbers = list(self.api.telephony.phone_numbers(included_telephony_type=TelephonyType.pstn_number))
        print(f'Got {len(numbers)} PSTN numbers')

    def test_006_included_mobile(self):
        numbers = list(self.api.telephony.phone_numbers(included_telephony_type=TelephonyType.mobile_number))
        print(f'Got {len(numbers)} mobile numbers')


class TestNumberConsistency(TestCaseWithUsers):
    def test_number_consistency(self):
        numbers = self.api.telephony.phone_numbers(owner_type=OwnerType.people)
        locations = {loc.location_id:loc for loc in self.api.locations.list()}
        err = False
        for number in numbers:
            print(f'number: {number.phone_number}/{number.extension}')
            # owner has to be a person
            if not number.owner:
                print(' - no owner')
                err = True
                continue
            if number.owner.owner_type != OwnerType.people:
                print(f' - wrong owner type: {number.owner.owner_type}')
                err = True
                continue
            number_location_id = number.location.id
            person = next(user for user in self.users if user.person_id == number.owner.owner_id)
            if person.location_id != number_location_id:
                print(f'  - person location id ({base64.b64decode(person.location_id+"==").decode()}) does not match'
                      f' number location id ({base64.b64decode(number_location_id+"==").decode()})')
                print(f'    Person: "{person.display_name}" in "{locations[person.location_id].name}"')
                print(f'    Number location: "{locations[number_location_id].name}"')

                err = True
        self.assertFalse(err)

        ...


class TestValidateExtensions(TestCaseWithLog):
    def test_001_new_extensions(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions) for _ in range(20)]
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidationStatus.ok, result.status)

    def test_002_duplicate_extensions(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions) for _ in range(20)]
        to_validate.extend(random.sample(list(extensions), 5))
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidationStatus.ok, result.status)

    def test_002_duplicate_in_list(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions)] * 3
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidationStatus.errors, result.status)
        self.assertTrue(result.extension_status)
        self.assertEqual(len(to_validate), len(result.extension_status))
        for i in range(1, 3):
            self.assertEqual(ValidateExtensionStatusState.duplicate_in_list, result.extension_status[i].state)


@dataclass(init=False)
class TestValidatePhoneNumbers(TestCaseWithLog):
    us_locations: ClassVar[list[LocationInfo]]
    available: Optional[str] = field(default=None)
    target: Optional[LocationInfo] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get US location infos
        cls.us_locations = us_location_info(api=cls.api)

    def setUp(self) -> None:
        if not self.us_locations:
            self.skipTest('Need US locations with numbers to run test')
        self.target = random.choice(self.us_locations)
        self.available = available_tns(api=self.api, tns_requested=1, tn_prefix=self.target.main_number[:5])[0]
        super().setUp()

    def test_001_available(self):
        """
        validate available number
        """
        number = self.available
        result = self.api.telephony.validate_phone_numbers(phone_numbers=[number])
        self.assertEqual(ValidationStatus.ok, result.status)
        self.assertTrue(result.ok)
        self.assertEqual(1, len(result.phone_numbers))
        self.assertEqual([ValidatePhoneNumberStatus(phone_number=number,
                                                    state=ValidatePhoneNumberStatusState.available,
                                                    toll_free_number=False, detail=[])],
                         result.phone_numbers)

    def test_002_duplicate(self):
        """
        Validate a duplicate number
        """
        number = self.target.main_number
        result = self.api.telephony.validate_phone_numbers(phone_numbers=[number])
        self.assertEqual(ValidatePhoneNumbersResponse(
            status=ValidationStatus.errors,
            phone_numbers=[ValidatePhoneNumberStatus(
                phone_number=number,
                state=ValidatePhoneNumberStatusState.duplicate,
                toll_free_number=False,
                detail=[f'[Error 8363] DN is in use : {number}'])]),
            result)

    def test_003_duplicate_in_list_available(self):
        """
        Validate duplicate number in list
        """
        result = self.api.telephony.validate_phone_numbers(phone_numbers=[self.available, self.available])
        self.assertEqual(ValidatePhoneNumbersResponse(
            status=ValidationStatus.errors,
            phone_numbers=[
                ValidatePhoneNumberStatus(phone_number=self.available,
                                          state=ValidatePhoneNumberStatusState.available,
                                          toll_free_number=False,
                                          detail=[]),
                ValidatePhoneNumberStatus(phone_number=self.available,
                                          state=ValidatePhoneNumberStatusState.duplicate_in_list,
                                          toll_free_number=False,
                                          detail=[f'[Error 8360] Duplicate DN in the request : {self.available}'])
            ]),
            result)

    def test_004_invalid(self):
        """
        Validate an invalid number
        """
        result = self.api.telephony.validate_phone_numbers(phone_numbers=['+1800'])
        self.assertEqual(ValidatePhoneNumbersResponse(
            status=ValidationStatus.errors,
            phone_numbers=[ValidatePhoneNumberStatus(
                phone_number='+1800',
                state=ValidatePhoneNumberStatusState.invalid,
                toll_free_number=False,
                detail=['[Error 8362] DN is invalid : +1800'])]),
            result)

    def test_006_unavailable(self):
        """
        Validate an unavailable number
        """
        number = '+17207783411'
        result = self.api.telephony.validate_phone_numbers(phone_numbers=[number])
        self.assertEqual(ValidatePhoneNumbersResponse(
            status=ValidationStatus.errors,
            phone_numbers=[ValidatePhoneNumberStatus(
                phone_number=number,
                state=ValidatePhoneNumberStatusState.unavailable,
                toll_free_number=False,
                detail=[f'[Error 8361] DN is unavailable : {number}'])]),
            result)
