"""
Test cases UCM profiles
"""

from tests.base import TestCaseWithLog


class Test(TestCaseWithLog):

    def test_001_read_all(self):
        profiles = self.api.telephony.ucm_profiles()
        print(f'Got {len(profiles)} UCM profiles')
