import asyncio

from tests.base import TestCaseWithUsers, async_test


class TestMsTeams(TestCaseWithUsers):
    @async_test
    async def test_read(self):
        """
        Test reading MS Teams settings
        """
        settings = await asyncio.gather(*[self.async_api.person_settings.ms_teams.read(person_id=user.person_id)
                                          for user in self.users])
        print(f'Read MS Teams settings for {len(settings)} users')
