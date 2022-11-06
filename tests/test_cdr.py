"""
Test CDR API
"""
from collections import defaultdict
from datetime import datetime
from functools import reduce

from dateutil import tz

from tests.base import TestCaseWithLog
from wxc_sdk.cdr import CDR
from wxc_sdk.rest import RestError


class TestCDR(TestCaseWithLog):
    def test_001(self):
        api = self.api.cdr
        try:
            cdrs = list(api.get_cdr_history())
        except RestError as e:
            print(f'Error: {e}')
            raise
        print(f'Got {len(cdrs)} CDRs')
        call_ids = set(cdr.call_id for cdr in cdrs)
        print(f'{len(call_ids)} different call IDs:')
        print('\n'.join(f'  {c}' for c in sorted(call_ids)))

        by_correlation_id: dict[str, list[CDR]] = reduce(lambda s, el: s[el.correlation_id].append(el) or s,
                                                         cdrs,
                                                         defaultdict(list))
        print(f'{len(by_correlation_id)} correlation IDs')
        for corr_id, records in by_correlation_id.items():
            print(f'  {corr_id}')
            for record in records:
                print(f'    {record.start_time} {record.answer_time} {record.duration} {record.calling_number}'
                      f'->{record.called_number} {record.call_id}')

        foo = 1

    def test_002_pagination(self):
        api = self.api.cdr
        try:
            cdrs = list(api.get_cdr_history(max=5))
        except RestError as e:
            print(f'Error: {e}')
            raise
        print(f'Got {len(cdrs)} CDRs')
