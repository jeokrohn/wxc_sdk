"""
Tests for MembershipAPI
"""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from random import choice

from tests.base import TestCaseWithUsersAndSpaces
from wxc_sdk.people import Person
from wxc_sdk.rooms import Room


@dataclass(init=False)
class TestMembership(TestCaseWithUsersAndSpaces):


    def test_001_list_memberships(self):
        """
        get memberships of all spaces
        """
        spaces = list(self.api.rooms.list())
        spaces.sort(key=lambda s: s.title)
        users_by_id: dict[str, Person] = {user.person_id: user for user in self.users}

        def user_str(user_id: str) -> str:
            user = users_by_id.get(user_id)
            if user is None:
                return f'None ({user_id})'
            return f'{user.display_name}({user.emails[0]})'

        with ThreadPoolExecutor() as pool:
            memberships_list = list(pool.map(lambda space: list(self.api.membership.list(room_id=space.id)), spaces))
        for space, memberships in zip(spaces, memberships_list):
            print(space.title)
            print('\n'.join(f'  {user_str(m.person_id)}, {m.person_email}' for m in memberships))

    def test_002_add_user(self):
        """
        Add bunch of users to space
        """
        with self.target_space() as target_space:
            target_space: Room
            members = list(self.api.membership.list(room_id=target_space.id))
            people_ids = set(m.person_id for m in members)
            candidates = [u for u in self.users if u.person_id not in people_ids]
            # add a user
            to_add = choice(candidates)
            self.api.membership.create(room_id=target_space.id, person_id=to_add.person_id)

            # check if the user has been added
            members_after = list(self.api.membership.list(room_id=target_space.id))
            added_membership = next((m for m in members_after if m.person_id == to_add.person_id), None)
            self.assertIsNotNone(added_membership)

            # remove user again
            self.api.membership.delete(membership_id=added_membership.id)
            members_after = list(self.api.membership.list(room_id=target_space.id))

            # back to before?
            members.sort(key=lambda m: m.id)
            members_after.sort(key=lambda m: m.id)
            self.assertEqual(members, members_after)
