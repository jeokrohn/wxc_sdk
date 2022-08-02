"""
Test cases for call waiting settings
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        read settings for all users
        """
        cw = self.api.person_settings.call_waiting
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda user: cw.read(person_id=user.person_id),
                                    self.users))
        print(f'Got details for {len(details)} users.')

    @TestCaseWithUsers.async_test
    async def test_002_read_all_async(self):
        """
        read settings for all users
        """
        cw = self.async_api.person_settings.call_waiting
        details = await asyncio.gather(*[cw.read(person_id=u.person_id) for u in self.users])
        print(f'Got details for {len(details)} users.')
        ...
