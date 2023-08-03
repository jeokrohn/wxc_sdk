import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from itertools import chain
from math import log, ceil
from typing import Union

from tests.base import TestCaseWithLog
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.events import EventResource, ComplianceEvent
from wxc_sdk.rest import RestError


class TestEvents(TestCaseWithLog):
    def test_001_list(self):
        events = list(self.api.events.list(resource=EventResource.messages, max=1000))
        events.sort(key=lambda e: e.created)
        print(f'{len(events)} message events from {events and events[0].created or None} to '
              f'{events and events[-1].created or None}')

    @TestCaseWithLog.async_test
    async def test_002_list_events_for_all_resources(self):
        start = datetime.utcnow() - timedelta(days=3)
        events_list = await asyncio.gather(*[self.async_api.events.list(resource=r.value, from_=start, max=500)
                                             for r in EventResource])
        events_list: list[list[ComplianceEvent]]
        res_len = max(map(len, (e.name for e in EventResource)))
        if not any(events_list):
            self.skipTest('No events found')
        ev_width = ceil(log(max(map(len, events_list))) / log(10))
        for resource, events in zip(EventResource, events_list):
            events.sort(key=lambda e: e.created)
            print(
                f'{resource.name:{res_len}}: {len(events):{ev_width}} events, {events and events[0].created or None} - '
                f'{events and events[-1].created or None}')

    @TestCaseWithLog.async_test
    async def test_003_details_all_events(self):
        """
        Get details for all events
        """
        async with AsWebexSimpleApi(tokens=self.tokens, concurrent_requests=30) as api:
            start = datetime.utcnow() - timedelta(minutes=60)
            events_list = await asyncio.gather(*[api.events.list(resource=r.value, from_=start, max=500)
                                                 for r in EventResource])
            details = await asyncio.gather(*[api.events.details(event_id=e.id)
                                             for e in chain.from_iterable(events_list)], return_exceptions=True)
        failed = sum(isinstance(d, Exception) for d in details)
        print(f'Tried to get details for {sum(map(len, events_list))} events, {failed} exceptions')
        if failed:
            print('Failed to get details for:')
        failed_events = [e for e, detail in zip(chain.from_iterable(events_list), details)
                         if isinstance(detail, Exception)]
        print('\n'.join(f'{e}' for e in failed_events))
        self.print_request_stats()

    def test_004_details_all_events_threads(self):
        """
        Get details for all events; threading
        """
        start = datetime.utcnow() - timedelta(minutes=60)

        def details(event: ComplianceEvent) -> Union[RestError, ComplianceEvent]:
            try:
                return self.api.events.details(event_id=event.id)
            except RestError as e:
                return e

        with ThreadPoolExecutor() as pool:
            events_list = list(pool.map(lambda r: list(self.api.events.list(resource=r.value,
                                                                            from_=start, max=500)),
                                        EventResource))
            details = list(pool.map(lambda e: details(e),
                                    chain.from_iterable(events_list)))
        failed = sum(isinstance(d, Exception) for d in details)
        print(f'Tried to get details for {sum(map(len, events_list))} events, {failed} exceptions')
        if failed:
            print('Failed to get details for:')
        failed_events = [e for e, detail in zip(list(chain.from_iterable(events_list)), details)
                         if isinstance(detail, Exception)]
        print('\n'.join(f'{e}' for e in failed_events))
        self.print_request_stats()
