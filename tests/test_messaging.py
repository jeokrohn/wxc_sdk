"""
Tests for messaging APIs
"""
import asyncio
import json
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain, combinations
from random import choice, sample, shuffle
from typing import ClassVar
from unittest import skip

from pydantic import TypeAdapter

from tests.base import TestCaseWithUsersAndSpaces, TestCaseWithLog
from wxc_sdk.common import RoomType
from wxc_sdk.messages import MessageAttachment
from wxc_sdk.people import Person
from wxc_sdk.rooms import Room
from wxc_sdk.teams import Team

TEST_NAME = re.compile(r'Test Space \d{3}')


class TestMessages(TestCaseWithUsersAndSpaces):

    def test_001_create_message(self):
        """
        """
        api = self.api.messages
        with self.target_space() as target:
            target: Room
            messages = list(api.list(room_id=target.id))
            new_message = api.create(room_id=target.id, text=f'Random message {uuid.uuid4()}')

    def test_002_create_direct_message(self):
        api = self.api.messages
        # pick a random user
        target_user = choice(self.users)
        new_message = api.create(to_person_id=target_user.person_id, text=f'Random message {uuid.uuid4()}')
        # now a space has to exist with that user
        self.assertEqual(RoomType.direct, new_message.room_type)
        direct_by_id = list(api.list_direct(person_id=target_user.person_id))
        direct_by_email = list(api.list_direct(person_email=target_user.emails[0]))

    def test_003_create_direct_message_local_file(self):
        api = self.api.messages
        # pick a random user
        target_user = choice(self.users)
        new_message = api.create(to_person_id=target_user.person_id,
                                 text=f'Random message {uuid.uuid4()} with attachment',
                                 files=[__file__])
        # now a space has to exist with that user
        self.assertEqual(RoomType.direct, new_message.room_type)

    @TestCaseWithUsersAndSpaces.async_test
    async def test_004_reate_direct_message_local_file_async_sdk(self):
        api = self.async_api.messages
        target_user = choice(self.users)
        new_message = await api.create(to_person_id=target_user.person_id,
                                       text=f'Random message {uuid.uuid4()} with attachment',
                                       files=[__file__])

    def test_005_attachment(self):
        attachments = [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Sample Adaptive Card",
                            "size": "large"
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "url": "http://adaptivecards.io",
                            "title": "Learn More"
                        }
                    ]
                }
            }
        ]
        atts = TypeAdapter(list[MessageAttachment]).validate_python(attachments)
        foo = 1


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


class TestRooms(TestCaseWithLog):
    def test_001_list(self):
        rooms = list(self.api.rooms.list())
        print(f'Got {len(rooms)} rooms')

    def test_002_create(self):
        rooms = list(self.api.rooms.list())
        new_names = (name for i in range(1000)
                     if (name := f'Test Space {i:03}') not in set(r.title for r in rooms))
        title = next(new_names)
        new_room = self.api.rooms.create(title=title)
        print(f'Created space "{title}"')
        print(json.dumps(json.loads(new_room.model_dump_json(by_alias=True)), indent=2))

    def test_003_details(self):
        """
        details for all spaces
        """
        rooms = list(self.api.rooms.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda r: self.api.rooms.details(room_id=r.id), rooms))
        print(f'got details for {len(details)} rooms')

    def test_004_meeting_details(self):
        """
        meeting details for all spaces
        """
        # there are no meeting details for announcement only spaces
        rooms = [room for room in self.api.rooms.list()
                 if not room.is_announcement_only]
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda r: self.api.rooms.meeting_details(room_id=r.id), rooms))
        print(f'got meeting details for {len(details)} rooms')

    @contextmanager
    def target_space(self):
        with self.no_log():
            rooms = [r for r in self.api.rooms.list()
                     if TEST_NAME.match(r.title)]
        if not rooms:
            self.skipTest('No targets')
        target = choice(rooms)
        details = self.api.rooms.details(room_id=target.id)
        try:
            yield details
        finally:
            after = self.api.rooms.update(update=details)
            self.assertEqual(details, after)

    def test_005_update_title(self):
        """
        meeting details for all spaces
        """
        with self.target_space() as room:
            room: Room
            title = f'{room.title}-XXX'
            update = Room(id=room.id, title=title)
            after = self.api.rooms.update(update)
            self.assertEqual(title, after.title)
            after.title = room.title
            self.assertEqual(room, after)


@dataclass(init=False)
class TestTeams(TestCaseWithLog):
    users: ClassVar[list[Person]] = None

    TEAMS_TO_CREATE = 5
    USERS_IN_TEAM = 8
    SPACES_IN_TEAM = 10

    async def get_users(self) -> list[Person]:
        if self.users is None:
            with self.no_log():
                me = await self.async_api.people.me()
                self.__class__.users = [user async for user in self.async_api.people.list_gen()
                                        if user.person_id != me.person_id]
        return self.users

    async def get_teams(self) -> list[Team]:
        return [team async for team in self.async_api.teams.list_gen()
                if re.match(r'Team Test \d{3}', team.name)]

    async def create_team(self, team_name, team_members: list[Person] = None) -> tuple[Team, Room]:
        """
        Create a team with some members
        :param team_name:
        :param team_members:
        :return: new team and general space in that team
        """
        # create the team
        team = await self.async_api.teams.create(name=team_name)
        print(f'Created "{team.name}"')
        # add members
        general_space = next(iter(await asyncio.gather(
            self.async_api.rooms.list(team_id=team.id),
            *[self.async_api.team_memberships.create(team_id=team.id,
                                                     person_id=member.person_id)
              for member in team_members])))[0]
        print(f'Added to team "{team.name}": {", ".join(m.display_name for m in team_members)}')
        return team, general_space

    @TestCaseWithLog.async_test
    async def test_001_create(self):
        """
        Create teams and post messages in the teams
        """

        api = self.async_api

        users, teams = await asyncio.gather(self.get_users(), self.get_teams())
        users: list[Person]
        teams: list[Team]
        new_names = (name
                     for i in range(1000)
                     if (name := f'Team Test {i:03}') not in set(team.name for team in teams))

        # create a bunch of teams and add random sets of users to them
        async def create_team():
            team_name = next(new_names)
            team_members = sample(users, self.USERS_IN_TEAM)
            team, general_space = await self.create_team(team_name=team_name, team_members=team_members)

            # create some messages mentioning random people
            tasks = []
            user_lists = list(chain.from_iterable(combinations(team_members, c_len)
                                                  for c_len in range(2, len(team_members))))
            shuffle(user_lists)
            for user_list in user_lists:
                tasks.append(api.messages.create(
                    room_id=general_space.id,
                    markdown=f'Hi, {", ".join(f"<@personId: {u.person_id}>" for u in user_list)}'))
            await asyncio.gather(*tasks)
            return

        await asyncio.gather(*[create_team() for _ in range(self.TEAMS_TO_CREATE)])
        self.print_request_stats()
        return

    @TestCaseWithLog.async_test
    async def test_002_delete(self):
        """
        delete a random team
        """
        api = self.async_api
        teams = await self.get_teams()
        if not teams:
            self.skipTest('No target teams')
        target = choice(teams)
        print(f'Deleting team "{target.name}"')
        await api.teams.delete(team_id=target.id)

    @skip('')
    @TestCaseWithLog.async_test
    async def test_003_delete_all(self):
        """
        delete all test teams
        """
        api = self.async_api
        teams = [team async for team in api.teams.list_gen()
                 if re.match(r'Team Test \d{3}', team.name)]
        await asyncio.gather(*[api.teams.delete(team_id=team.id)
                               for team in teams])

    @TestCaseWithLog.async_test
    async def test_004_teams_with_spaces(self):
        """
        create some teams with a bunch of spaces
        """
        teams, users = await asyncio.gather(self.get_teams(), self.get_users())
        teams: list[Team]
        users: list[Person]

        async def team_with_spaces(name: str, members: list[Person]):
            team, general_space = await self.create_team(team_name=name, team_members=members)
            # add some spaces to the team
            await asyncio.gather(*[self.async_api.rooms.create(title=f'{team.name}-{i:03}',
                                                               team_id=team.id)
                                   for i in range(self.SPACES_IN_TEAM)])

        new_names = (name for i in range(1000)
                     if (name := f'Team Test {i:03}') not in set(team.name for team in teams))
        await asyncio.gather(*[team_with_spaces(name=next(new_names),
                                                members=sample(users, self.USERS_IN_TEAM))
                               for _ in range(self.TEAMS_TO_CREATE)])
