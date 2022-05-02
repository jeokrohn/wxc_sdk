from .base import TestCaseWithLog
from wxc_sdk.as_api import AsWebexSimpleApi
import asyncio


class TestPeople(TestCaseWithLog):

    @TestCaseWithLog.async_test
    async def test_001_all_details(self):
        me = await self.async_api.people.me()
        users = [u async for u in self.async_api.people.list_gen()]
        # try to provoke 429
        detail_tasks = [self.async_api.people.details(person_id=user.person_id)
                        for user in users*10]
        details = await asyncio.gather(*detail_tasks)
        print(f'got details for {len(details)} users')
