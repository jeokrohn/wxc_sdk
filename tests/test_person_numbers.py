"""
Test for call monitoring settings
"""
from concurrent.futures import ThreadPoolExecutor

from .base import TestCaseWithUsers


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
        # TODO: defect, direct number are not +E.164, CALL-69213
        """
        nu = self.api.person_settings.numbers

        with ThreadPoolExecutor() as pool:
            numbers = list(pool.map(lambda user: nu.read(person_id=user.person_id),
                                    self.users))
        direct_number_issues = [(user, direct_numbers) for user, numbers in zip(self.users, numbers)
                                if (direct_numbers := [number.direct_number
                                                       for number in numbers.phone_numbers
                                                       if number.direct_number and not
                                                       number.direct_number.startswith('+')])]
        print('\n'.join(f'{user.display_name}: {", ".join(numbers)}' for user, numbers in direct_number_issues))
        self.assertTrue(not direct_number_issues), 'Some direct numbers are not +E.164'
