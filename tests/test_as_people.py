"""
Test async operations on people API and provoke 429 responses
"""
import asyncio
import time
from collections import Counter
from collections.abc import Generator
from unittest import skip

import matplotlib.pyplot as plt

from wxc_sdk.as_api import AsWebexSimpleApi
from tests.base import TestCaseWithLog, async_test, LoggedRequest


class TestPeople(TestCaseWithLog):

    @skip('Protect the backend :-)')
    @async_test
    async def test_001_all_details(self):
        async with AsWebexSimpleApi(tokens=self.tokens, concurrent_requests=30) as api:
            users = [u async for u in self.async_api.people.list_gen()]
            # try to provoke 429
            detail_tasks = [api.people.details(person_id=user.person_id, calling_data=True)
                            for user in users * 50]
            before = time.perf_counter_ns()
            details = await asyncio.gather(*detail_tasks, return_exceptions=True)
            after = time.perf_counter_ns() - before
            print(f'got details for {len(details)} users in {after / 1000000:.3f} ms: '
                  f'{after / len(details) / 1000000:.3f} ms/user')

        def people_details_requests() -> Generator[LoggedRequest, None, None]:
            """
            Get requests for people details
            """
            return self.requests(url_filter=r'.+/v1/people/(?P<person_id>[a-zA-Z0-9]+)\?callingData=true')

        # count response status
        method_and_status = Counter((r.method, r.status) for r in people_details_requests())
        for k in sorted(method_and_status):
            v = method_and_status[k]
            print(f'{k}: {v}')

        # plot response times and 429 retry-after times
        x_200, y_200 = list(), list()
        x_429, y_429 = list(), list()
        for r in people_details_requests():
            if r.status == 200:
                x_200.append(r.record.created)
                y_200.append(r.time_ms)
            elif r.status == 429:
                x_429.append(r.record.created)
                y_429.append(int(r.response_headers['Retry-after']))

        fig, (ax1) = plt.subplots(1, 1)

        ax1.plot(x_200, y_200, linestyle='', marker='x', color='blue')
        if x_429:
            ax_429 = ax1.twinx()
            ax_429.plot(x_429, y_429, linestyle='', marker='+', color='red')
        plt.show()
