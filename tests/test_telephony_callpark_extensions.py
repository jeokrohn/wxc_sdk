"""
Unit test for call park extensions
"""
from concurrent.futures import ThreadPoolExecutor

from .base import TestCaseWithLog


class TestCPE(TestCaseWithLog):
    def test_001_list_all(self):
        cpe_list = list(self.api.telephony.callpark_extension.list())
        if not cpe_list:
            self.skipTest('No existing call park extensions')
        print(f'Got {len(cpe_list)} call park extensions')

    def test_002_all_details(self):
        cp = self.api.telephony.callpark_extension
        cpe_list = list(cp.list())
        if not cpe_list:
            self.skipTest('No existing call park extensions')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda cpe: cp.details(location_id=cpe.location_id, cpe_id=cpe.cpe_id),
                                    cpe_list))
        print(f'Got details for {len(cpe_list)} call park extensions')
        self.assertTrue(all(cpe.name == detail.name and cpe.extension == detail.extension
                            for cpe, detail in zip(cpe_list, details)))
