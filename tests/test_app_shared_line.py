import asyncio
import json
import random

from pydantic import TypeAdapter

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.people import Person
from wxc_sdk.telephony.devices import DeviceMembersResponse, AvailableMember


class TestAppSharedLine(TestCaseWithUsers):
    def test_search_members_old(self):
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        apps = self.api.person_settings.appservices.read(target_user.person_id)

        members = list(self.api.person_settings.app_shared_line.search_members_old(
            person_id=target_user.person_id,
            application_id=apps.desktop_client_id))
        print(f'Found {len(members)} members')

    def test_search_members(self):
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        members = list(self.api.person_settings.app_shared_line.search_members(person_id=target_user.person_id))
        print(f'Found {len(members)} members')
        print(json.dumps(TypeAdapter(list[AvailableMember]).dump_python(members, mode='json',
                                                                        exclude_none=True, by_alias=True),
                         indent=2))
        self.assertTrue(all(m.member_id for m in members), 'Member ID should not be empty, WXCAPIBULK-724')

    def test_search_members_location_hartford(self):
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        hartford = next((loc for loc in self.api.locations.list() if loc.name == 'Hartford'), None)
        if hartford is None:
            self.skipTest('Hartford location not found')

        members = list(self.api.person_settings.app_shared_line.search_members(person_id=target_user.person_id,
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
            members = await self.async_api.person_settings.app_shared_line.get_members(user.person_id)
            return members

        members = await asyncio.gather(*[get_members_for_user(user) for user in self.users])
        print(f'Got shared-line appearance members for {len(members)} users')

    def test_update_members(self):
        """
        Update Shared-Line Appearance Members for a user
        """
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        apps = self.api.person_settings.appservices.read(target_user.person_id)

        # Get current members
        members = self.api.person_settings.app_shared_line.get_members(target_user.person_id)

        # get available members
        available_members_old = list(self.api.person_settings.app_shared_line.search_members_old(target_user.person_id,
                                                                                                 apps.desktop_client_id))
        available_members = list(self.api.person_settings.app_shared_line.search_members(target_user.person_id))

        foo = 1
        # pick an available member
        new_member: AvailableMember = random.choice(available_members_old)
        # add member
        member_list = [m for m in members.members]
        member_list.append(new_member)
        self.api.person_settings.app_shared_line.update_members(target_user.person_id, member_list)
        try:
            members_after = self.api.person_settings.app_shared_line.get_members(target_user.person_id)
            # validate that the member is added
            self.assertIsNotNone(next((m for m in members_after.members if m.member_id == new_member.member_id),
                                      None))
        finally:
            # try to restore old settings
            member_list.pop()
            self.api.person_settings.app_shared_line.update_members(target_user.person_id, member_list)
            members_restored = self.api.person_settings.app_shared_line.get_members(target_user.person_id)
            # validate that the member is removed
            self.assertEqual(members, members_restored)
        return
