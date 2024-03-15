"""
Test cases for call waiting settings
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

from tests.base import TestCaseWithUsers, async_test


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        read settings for all users
        """
        cw = self.api.person_settings.call_waiting
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda user: cw.read(entity_id=user.person_id),
                                    self.users))
        print(f'Got details for {len(details)} users.')

    @async_test
    async def test_002_read_all_async(self):
        """
        read settings for all users
        """
        cw = self.async_api.person_settings.call_waiting
        details = await asyncio.gather(*[cw.read(entity_id=u.person_id) for u in self.users])
        print(f'Got details for {len(details)} users.')
