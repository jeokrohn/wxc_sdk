import asyncio
from datetime import datetime, timedelta
from itertools import chain
from math import log, ceil

from dateutil import tz

from tests.base import TestCaseWithLog
from wxc_sdk.events import EventResource, ComplianceEvent


class TestEvents(TestCaseWithLog):
    def test_001_list(self):
        events = list(self.api.events.list(resource=EventResource.messages))
        foo = 1


    @TestCaseWithLog.async_test
    async def test_002_list_events_for_all_resources(self):
        start = datetime.utcnow() - timedelta(days=3)
        events_list = await asyncio.gather(*[self.async_api.events.list(resource=r.value, from_=start, max=500)
                                        for r in EventResource])
        events_list: list[list[ComplianceEvent]]
        res_len = max(map(len, (e.name for e in EventResource)))
        ev_width = ceil(log(max(map(len, events_list)))/log(10))
        for resource, events in zip(EventResource, events_list):
            events.sort(key=lambda e:e.created)
            print(f'{resource.name:{res_len}}: {len(events):{ev_width}} events, {events and events[0].created or None} - '
                  f'{events and events[-1].created or None}')
        foo = 1

    @TestCaseWithLog.async_test
    async def test_003_details_all_events(self):
        start = datetime.utcnow() - timedelta(days=3)
        events_list = await asyncio.gather(*[self.async_api.events.list(resource=r.value, from_=start, max=500)
                                             for r in EventResource])
        details = await asyncio.gather(*[self.async_api.events.details(event_id=e.id)
                                         for e in chain.from_iterable(events_list)], return_exceptions=True)
        failed = sum(isinstance(d, Exception) for d in details)
        print(f'Tried to get details for {sum(map(len, events_list))} events, {failed} exceptions')
        if failed:
            print('Failed to get details for:')
        failed_events = [e for e, detail in zip(chain.from_iterable(events_list), details)
                         if isinstance(detail, Exception)]
        print('\n'.join(f'{e}' for e in failed_events))

