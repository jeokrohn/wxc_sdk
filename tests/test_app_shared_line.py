import asyncio
import json
import random

from pydantic import TypeAdapter

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.people import Person
from wxc_sdk.telephony.devices import AvailableMember, DeviceMembersResponse


class TestAppSharedLine(TestCaseWithUsers):
    """
    Read and statefully update person application shared-line appearance settings.
    """

    def test_search_members(self):
        """
        Search shared-line member candidates for one user and verify candidate IDs are populated.
        """
        # Pick a real calling user to exercise the member search endpoint.
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        # Search all available shared-line members for the target user.
        members = list(self.api.person_settings.app_shared_line.search_members(person_id=target_user.person_id))
        print(f'Found {len(members)} members')
        print(
            json.dumps(
                TypeAdapter(list[AvailableMember]).dump_python(members, mode='json', exclude_none=True, by_alias=True),
                indent=2,
            )
        )

        # Every returned candidate must include the member identifier required for updates.
        self.assertTrue(all(m.member_id for m in members), 'Member ID should not be empty, WXCAPIBULK-724')

    def test_search_members_location_hartford(self):
        """
        Search shared line appearance members limited to location Hartford
        """
        # Pick a real calling user to scope the search request.
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        # Resolve the optional Hartford fixture location, skipping if this org lacks it.
        hartford = next((loc for loc in self.api.locations.list() if loc.name == 'Hartford'), None)
        if hartford is None:
            self.skipTest('Hartford location not found')

        # Search available shared-line members filtered to the Hartford location.
        members = list(
            self.api.person_settings.app_shared_line.search_members(
                person_id=target_user.person_id, location=hartford.location_id, max=2
            )
        )
        print(f'Found {len(members)} members')

        # Confirm the API honored the location filter.
        self.assertTrue(all(m for m in members if m.location.id == hartford.location_id))

    @async_test
    async def test_get_members(self):
        """
        Get Shared-Line Appearance Members for all users
        """

        async def get_members_for_user(user: Person) -> DeviceMembersResponse:
            # Read current shared-line members for one user.
            members = await self.async_api.person_settings.app_shared_line.get_members(user.person_id)
            return members

        # Read member assignments concurrently for broad list coverage.
        members = await asyncio.gather(*[get_members_for_user(user) for user in self.users])
        print(f'Got shared-line appearance members for {len(members)} users')

    def test_update_members(self):
        """
        Update Shared-Line Appearance Members for a user
        """
        # Pick a real calling user and snapshot their current member list for later restore.
        target_user = random.choice(self.users)
        target_user: Person
        print(f'Target user: {target_user.display_name}')

        members = self.api.person_settings.app_shared_line.get_members(target_user.person_id)

        # Find a candidate member that is not already assigned.
        available_members = list(self.api.person_settings.app_shared_line.search_members(target_user.person_id))
        current_member_ids = {m.member_id for m in members.members or []}
        available_members = [m for m in available_members if m.member_id not in current_member_ids]
        if not available_members:
            self.skipTest(f'No available shared-line member candidate for "{target_user.display_name}"')

        # Add one available member to validate the update/list add path.
        new_member: AvailableMember = random.choice(available_members)
        print(f'Adding member: "{new_member.first_name}.{new_member.last_name}" ({new_member.member_id})')
        member_list = list(members.members or [])
        member_list.append(new_member)
        self.api.person_settings.app_shared_line.update_members(target_user.person_id, member_list)
        try:
            # Read members after the update and verify the added candidate is visible.
            members_after = self.api.person_settings.app_shared_line.get_members(target_user.person_id)
            self.assertIsNotNone(
                next((m for m in members_after.members or [] if m.member_id == new_member.member_id), None)
            )

            # Remove the candidate again to cover delete semantics on the member list.
            restored_member_list = [m for m in member_list if m.member_id != new_member.member_id]
            self.api.person_settings.app_shared_line.update_members(target_user.person_id, restored_member_list)
            members_after_delete = self.api.person_settings.app_shared_line.get_members(target_user.person_id)
            self.assertIsNone(
                next((m for m in members_after_delete.members or [] if m.member_id == new_member.member_id), None)
            )
        finally:
            # Always restore the exact original member list to avoid side effects.
            self.api.person_settings.app_shared_line.update_members(target_user.person_id, list(members.members or []))
            members_restored = self.api.person_settings.app_shared_line.get_members(target_user.person_id)
            self.assertEqual(members, members_restored)
        return
