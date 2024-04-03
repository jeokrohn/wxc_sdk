"""
Test CDR API
"""
from collections import defaultdict
from datetime import datetime, timedelta
from functools import reduce

from dateutil.tz import tz

from tests.base import TestCaseWithLog
from wxc_sdk.cdr import CDR
from wxc_sdk.rest import RestError


class TestCDR(TestCaseWithLog):
    def test_001(self):
        """
        Get CDRs
        """
        api = self.api.cdr
        try:
            cdrs = list(api.get_cdr_history())
        except RestError as e:
            print(f'Error: {e}')
            print(f'{e.detail}')
            if e.detail.error_code == 404 and e.detail.message == 'No CDRs for requested time range and filters':
                return
            raise
        print(f'Got {len(cdrs)} CDRs')
        call_ids = set(cdr.call_id for cdr in cdrs)
        print(f'{len(call_ids)} different call IDs:')
        print('\n'.join(f'  {c}' for c in sorted(call_ids, key=lambda v: v or '')))

        by_correlation_id: dict[str, list[CDR]] = reduce(lambda s, el: s[el.correlation_id].append(el) or s,
                                                         cdrs,
                                                         defaultdict(list))
        print(f'{len(by_correlation_id)} correlation IDs')
        for corr_id, records in by_correlation_id.items():
            print(f'  {corr_id}')
            for record in records:
                print(f'    {record.start_time} {record.answer_time} {record.duration} {record.calling_number}'
                      f'->{record.called_number} {record.call_id}')

    def test_002_pagination(self):
        """
        GET CDRs w/ pagination
        """
        api = self.api.cdr
        start_time = datetime.now(tz=tz.tzutc()) - timedelta(hours=47, minutes=55)
        end_time = datetime.now(tz=tz.tzutc()) - timedelta(minutes=5, seconds=30)
        try:
            cdrs = list(api.get_cdr_history(max=50, start_time=start_time, end_time=end_time))
        except RestError as e:
            print(f'Error: {e}')
            print(f'{e.detail}')
            if e.detail.error_code == 404 and e.detail.message == 'No CDRs for requested time range and filters':
                return
            raise
        print(f'Got {len(cdrs)} CDRs')

    def test_003_force_429(self):
        """
        Trying to force a 429 response
        """
        start_time = datetime.now(tz=tz.tzutc()) - timedelta(hours=47, minutes=58)
        end_time = datetime.now(tz=tz.tzutc()) - timedelta(minutes=5, seconds=30)
        print(f'Looking for CDRs between {start_time} and {end_time}')
        try:
            cdr1 = list(self.api.cdr.get_cdr_history(start_time=start_time,
                                                     end_time=end_time))
        except RestError as rest_error:
            if (rest_error.detail.error_code == 404
                    and rest_error.detail.message == 'No CDRs for requested time range and filters'):
                self.skipTest('No CDRs')
            else:
                raise
        # this should get us a 429
        with self.assertRaises(RestError) as exc:
            self.api.session.retry_429 = False
            cdr2 = list(self.api.cdr.get_cdr_history(start_time=start_time + timedelta(seconds=2),
                                                     end_time=end_time + timedelta(seconds=2)))
        self.assertEqual(429, exc.exception.response.status_code, f'Unexpected exception: {exc.exception}')
