"""
Unit test for numbers
"""
import random

from wxc_sdk.all_types import *
from .base import TestCaseWithLog


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


class TestValidateExtensions(TestCaseWithLog):
    def test_001_new_extensions(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions) for _ in range(20)]
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidateExtensionResponseStatus.ok, result.status)

    def test_002_duplicate_extensions(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions) for _ in range(20)]
        to_validate.extend(random.sample(list(extensions), 5))
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidateExtensionResponseStatus.ok, result.status)

    def test_002_duplicate_in_list(self):
        at = self.api.telephony
        extensions = set(n.extension for n in at.phone_numbers(number_type='EXTENSION'))

        new_extensions = (extension for i in range(9000)
                          if (extension := str(1000 + i)) not in extensions)
        to_validate = [next(new_extensions)] * 3
        result = at.validate_extensions(extensions=to_validate)
        print(result)
        self.assertEqual(ValidateExtensionResponseStatus.errors, result.status)
        self.assertTrue(result.extension_status)
        self.assertEqual(len(to_validate), len(result.extension_status))
        for i in range(1, 3):
            self.assertEqual(ValidateExtensionStatusState.DUPLICATE_IN_LIST, result.extension_status[i].state)
