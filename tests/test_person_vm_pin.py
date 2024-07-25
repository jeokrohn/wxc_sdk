"""
Test resetting VM PIN
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.people import Person


class TestRead(TestCaseWithUsers):

    def test_001_reset_all(self):
        """
        Reset VM pin for all users
        """
        ps = self.api.person_settings

        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda user: ps.reset_vm_pin(user.person_id),
                          self.users))
        print(f'reset VM PIN for {len(self.users)} users')

    @async_test
    async def test_002_set_pin(self):
        """
        set PIN for all users
        """
        vm_api = self.async_api.person_settings.voicemail
        results = await asyncio.gather(*[vm_api.modify_passcode(user.person_id, passcode='184692')
                                         for user in self.users],
                                       return_exceptions=True)
        err = None
        for user, result in zip(self.users, results):
            user: Person
            if isinstance(result, Exception):
                err = err or result
                print(f'setting passcode for "{user.display_name}" failed: {result}')
        if err:
            raise err
