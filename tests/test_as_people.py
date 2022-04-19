from .base import TestCaseWithLog
from wxc_sdk.as_api import AsWebexSimpleApi
import asyncio


class TestPeople(TestCaseWithLog):

    @TestCaseWithLog.async_test
    async def test_001(self):
        async def test():
            async with AsWebexSimpleApi(tokens=self.tokens,
                                        concurrent_requests=1000) as api:
                me = await api.people.me()
                foo = 1
                users = [u async for u in api.people.list()]
                # try to provoke 429
                detail_tasks = [api.people.details(person_id=user.person_id)
                                for user in users]
                details = await asyncio.gather(*detail_tasks)
            print(f'got {len(users)} users')
            ...

        asyncio.run(test())
