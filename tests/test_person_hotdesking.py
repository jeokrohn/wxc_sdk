import asyncio

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.person_settings.hotdesking import HotDeskingMember


class TestPersonHotDesking(TestCaseWithUsers):
    @async_test
    async def test_available_members(self):
        settings = await asyncio.gather(
            *[self.async_api.person_settings.hotdesking.available_members(person_id=u.person_id) for u in self.users],
            return_exceptions=True,
        )
        err = None
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                err = err or setting
                print(f'Failed to get hotdesking available members for user "{user.display_name}": {setting}')
        return

    @async_test
    async def test_get_members(self):
        settings = await asyncio.gather(
            *[self.async_api.person_settings.hotdesking.get_members(person_id=u.person_id) for u in self.users],
            return_exceptions=True,
        )
        err = None
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                err = err or setting
                print(f'Failed to get hotdesking available members for user "{user.display_name}": {setting}')
        return

    def test_update_members(self):
        """
        Test updating hotdesking members for a random user
        """
        import random

        # pick random user
        user = random.choice(self.users)
        hotdesking_api = self.api.person_settings.hotdesking

        # get current members
        original_members = hotdesking_api.get_members(person_id=user.person_id)
        print(f'User "{user.display_name}": current hotdesking members: {original_members}')

        # get available members
        available = list(hotdesking_api.available_members(person_id=user.person_id))
        print(f'User "{user.display_name}": available members: {available}')

        # get current member IDs to avoid re-adding
        current_member_ids = {m.id for m in (original_members.members or []) if m.id}

        # pick a random available member that's not already assigned
        random.shuffle(available)
        candidate = next((m for m in available if m.id not in current_member_ids), None)

        if candidate is None:
            self.skipTest(
                f'No suitable hotdesking member available to add for user "{user.display_name}": '
                f'all available members are already assigned'
            )
        try:
            print(
                f'Adding member "{candidate.first_name}/{candidate.last_name}/{candidate.member_type}" '
                f'({candidate.id}) to "{user.display_name}"'
            )

            # add member by updating the members list
            new_members = list(original_members.members or [])
            new_members.append(HotDeskingMember.from_available_member(candidate))
            hotdesking_api.update_members(person_id=user.person_id, members=new_members)

            # get members and verify that member has been added
            updated_members = hotdesking_api.get_members(person_id=user.person_id)
            updated_member_ids = {m.id for m in updated_members.members}

            self.assertIn(
                candidate.id,
                updated_member_ids,
                f'Member ""{candidate.first_name}/{candidate.last_name}/{candidate.member_type}" should have been '
                f'added to "{user.display_name}"',
            )
            print(
                f'Verified: member ""{candidate.first_name}/{candidate.last_name}/{candidate.member_type}" has been '
                f'added to "{user.display_name}"'
            )

        finally:
            # restore previous members
            print(f'Restoring original hotdesking members for "{user.display_name}"')
            try:
                hotdesking_api.update_members(person_id=user.person_id, members=original_members.members or [])
            except Exception as e:
                print(f'Failed to restore hotdesking members for "{user.display_name}": {e}')
