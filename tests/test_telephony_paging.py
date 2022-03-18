# TODO: test cases

from concurrent.futures import ThreadPoolExecutor

from .base import TestCaseWithLog


class TestPaging(TestCaseWithLog):

    def test_001_list(self):
        """
        list paging groups
        """
        pgs = list(self.api.telephony.paging.list())

    def test_002_all_details(self):
        """
        get details for all paging groups
        """
        atp = self.api.telephony.paging
        pgs = list(atp.list())
        if not pgs:
            self.skipTest('Not existing paging groups')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda pg: atp.details(location_id=pg.location_id, paging_id=pg.paging_id),
                                    pgs))
        foo = 1
