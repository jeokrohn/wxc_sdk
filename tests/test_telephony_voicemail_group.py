"""
test cases for voicemail groups
"""

from .base import TestCaseWithLog


class TestVmGroup(TestCaseWithLog):
    def test_002_list(self):
        vmg = self.api.telephony.voicemail_groups
        groups = list(vmg.list())
        print(f'Got {len(groups)} voicemail groups')
