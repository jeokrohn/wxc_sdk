"""
Tests on agent caller IDs
"""
import asyncio
from dataclasses import dataclass
from random import choice
from typing import ClassVar, NamedTuple

from tests.base import TestCaseWithLog, async_test
from tests.testutil import calling_users
from wxc_sdk.people import Person
from wxc_sdk.person_settings.agent_caller_id import AgentCallerId


@dataclass(init=False)
class TestAgentCallerId(TestCaseWithLog):
    users: ClassVar[list[Person]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.users = calling_users(api=cls.api)

    def setUp(self) -> None:
        super().setUp()
        if not self.users:
            self.skipTest('No calling users')

    @async_test
    async def test_001_available_caller_ids(self):
        """
        get available agent caller IDs for all calling users
        """
        available_caller_ids = await asyncio.gather(
            *[self.async_api.person_settings.agent_caller_id.available_caller_ids(entity_id=user.person_id)
              for user in self.users])
        print(f'Got available caller IDs for {len(available_caller_ids)} users')

    @TestCaseWithLog.async_test
    async def test_002_read(self):
        """
        read agent caller id settings for all calling users
        """
        settings = await asyncio.gather(
            *[self.async_api.person_settings.agent_caller_id.read(entity_id=user.person_id)
              for user in self.users])
        print(f'Agent caller id settings for {len(settings)} users')

    @TestCaseWithLog.async_test
    async def test_configure(self):
        """
        modify agent caller id settings for a calling users
        """

        class UserInfo(NamedTuple):
            user: Person
            caller_ids: list[AgentCallerId]
            agent_caller_id: AgentCallerId

        as_api = self.async_api.person_settings.agent_caller_id
        with self.no_log():
            # get available caller ids and configured caller ids
            tasks = []
            for user in self.users:
                tasks.append(as_api.read(entity_id=user.person_id))
                tasks.append(as_api.available_caller_ids(entity_id=user.person_id))
            results = await asyncio.gather(*tasks)
            res_iter = iter(results)
            user_infos = (UserInfo(user, next(res_iter), caller_id) for user, caller_id in zip(self.users, res_iter))
        # we are looking for users for which agent caller id is available and not set
        candidate_users = [user_info for user_info in user_infos
                           if user_info.caller_ids and user_info.agent_caller_id.id is None]
        if not candidate_users:
            self.skipTest('Couldn\'t find any user with available agent caller id and agent caller id not set')
        # pick a target user
        target: UserInfo = choice(candidate_users)

        # pick a random queue from the queues available for this user
        caller_id = choice(target.caller_ids)

        api = self.api.person_settings.agent_caller_id
        # get current settings for selected user to put in the log
        before = api.read(entity_id=target.user.person_id)

        def agent_queue_number(agent_queue: AgentCallerId) -> str:
            """
            String representing the numbers of an agent queue
            """
            return '/'.join(s
                            for s in (agent_queue.phone_number, agent_queue.extension)
                            if s)

        print(f'Setting agent caller id for "{target.user.display_name}" to {caller_id.name} '
              f'({agent_queue_number(caller_id)})')

        # update the caller id settings for this user
        api.configure(entity_id=target.user.person_id, selected_caller_id=caller_id.id)
        after = api.read(entity_id=target.user.person_id)
        try:
            self.assertEqual(after.id, caller_id.id)
        finally:
            # restore old settings again
            api.configure(entity_id=target.user.person_id, selected_caller_id=before.id)
            restored = api.read(entity_id=target.user.person_id)
            self.assertEqual(before.id, restored.id)
