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
        now = datetime.now(tz = tz.tzutc())
        now = now.replace(tzinfo=None)
        us_time = datetime.now(tz=tz.tzoffset('US', -5*60*60))
        us_time = us_time.astimezone(tz.tzutc())
        iso = now.isoformat(timespec='milliseconds')
        try:
            cdrs = list(api.get_cdr_history())
        except RestError as e:
            foo = 1
            raise
        print(f'Got {len(cdrs)} CDRs')
        by_correlation_id: dict[str, list[CDR]] = reduce(lambda s, el: s[el.correlation_id].append(el) or s,
                                                        cdrs,
                                                        defaultdict(list))
        foo = 1
