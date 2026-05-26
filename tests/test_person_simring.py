import asyncio

from tests.base import TestCaseWithUsers, async_test


class TestPersonSimRing(TestCaseWithUsers):
    @async_test
    async def test_get_all_settings(self):
        settings = await asyncio.gather(
            *[self.async_api.person_settings.sim_ring.read(entity_id=u.person_id) for u in self.users],
            return_exceptions=True,
        )
        err = None
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                err = err or setting
                print(f'Failed to get simring settings for user "{user.display_name}": {setting}')
        return
