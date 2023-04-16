"""
Test resetting VM PIN
"""
from concurrent.futures import ThreadPoolExecutor

from tests.base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_reset_all(self):
        """
        Read numbers all users
        """
        ps = self.api.person_settings

        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda user: ps.reset_vm_pin(person_id=user.person_id),
                          self.users))
        print(f'reset VM PIN for {len(self.users)} users')
