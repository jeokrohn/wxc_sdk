import asyncio
import random

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.people import Person
from wxc_sdk.telephony.devices import DeviceMembersResponse


class TestAppSharedLine(TestCaseWithUsers):
    def test_search_members(self):
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        apps = self.api.person_settings.appservices.read(target_user.person_id)

        members = list(self.api.person_settings.app_shared_line.search_members(person_id=target_user.person_id,
                                                                               application_id=apps.desktop_client_id))
        print(f'Found {len(members)} members')

    def test_search_members_location_hartford(self):
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        apps = self.api.person_settings.appservices.read(target_user.person_id)

        hartford = next((loc for loc in self.api.locations.list() if loc.name == 'Hartford'), None)
        if hartford is None:
            self.skipTest('Hartford location not found')

        members = list(self.api.person_settings.app_shared_line.search_members(person_id=target_user.person_id,
                                                                               application_id=apps.desktop_client_id,
                                                                               location=hartford.location_id,
                                                                               max=2))
        print(f'Found {len(members)} members')
        self.assertTrue(all(m for m in members if m.location.id == hartford.location_id))

    @async_test
    async def test_get_members(self):
        """
        Get Shared-Line Appearance Members for all users
        """

        async def get_members_for_user(user: Person) -> DeviceMembersResponse:
            apps = await self.async_api.person_settings.appservices.read(user.person_id)
            members = await self.async_api.person_settings.app_shared_line.get_members(user.person_id,
                                                                                       apps.desktop_client_id)
            return members

        members = await asyncio.gather(*[get_members_for_user(user) for user in self.users])
        print(f'Got shared-line appearance members for {len(members)} users')
