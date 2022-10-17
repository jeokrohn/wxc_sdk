"""
Tests on agent caller IDs
"""
import asyncio
from dataclasses import dataclass
from random import choice
from typing import ClassVar, NamedTuple

from tests.base import TestCaseWithLog
from tests.testutil import calling_users
from wxc_sdk.people import Person
from wxc_sdk.person_settings.agent_caller_id import AgentQueue, QueueCallerId


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

    @TestCaseWithLog.async_test
    async def test_001_available_queues(self):
        """
        get available queues for all calling users
        """
        available_queues = await asyncio.gather(
            *[self.async_api.person_settings.agent_caller_id.available_queues(person_id=user.person_id)
              for user in self.users])
        print(f'Got available queues for {len(available_queues)} users')

    @TestCaseWithLog.async_test
    async def test_002_read(self):
        """
        read agent caller id settings for all calling users
        """
        settings = await asyncio.gather(
            *[self.async_api.person_settings.agent_caller_id.read(person_id=user.person_id)
              for user in self.users])
        print(f'Agent caller id settings for {len(settings)} users')

    @TestCaseWithLog.async_test
    async def test_003_modify(self):
        """
        modify agent caller id settings for a calling users
        """

        class UserInfo(NamedTuple):
            user: Person
            queues: list[AgentQueue]
            agent_caller_id: QueueCallerId

        with self.no_log():
            user_infos = (UserInfo(user, queues, agent_caller_id)
                          for user, (queues, agent_caller_id) in zip(
                self.users,
                await asyncio.gather(*[
                    asyncio.gather(
                        self.async_api.person_settings.agent_caller_id.available_queues(
                            person_id=user.person_id),
                        self.async_api.person_settings.agent_caller_id.read(
                            person_id=user.person_id))
                    for user in self.users])))
        # we are looking for users for which agent caller id is available and not set
        candidate_users = [user_info for user_info in user_infos
                           if user_info.queues and not user_info.agent_caller_id.queue_caller_id_enabled]
        if not candidate_users:
            self.skipTest('Couldn\'t find any user with available agent caller id and agent caller id not set')
        # pick a target user
        target: UserInfo = choice(candidate_users)

        # pick a random queue from the queues available for this user
        queue = choice(target.queues)

        api = self.api.person_settings.agent_caller_id

        # get current settings for selected user to put in the log
        before = api.read(person_id=target.user.person_id)

        def agent_queue_number(agent_queue: AgentQueue) -> str:
            """
            String representing the numbers of an agent queue
            """
            return '/'.join(s
                            for s in (agent_queue.phone_number, agent_queue.extension)
                            if s)

        print(f'Setting agent caller id for "{target.user.display_name}" to {queue.name} ({agent_queue_number(queue)})')

        # update the caller id settings for this user
        update = QueueCallerId(queue_caller_id_enabled=True,
                               selected_queue=queue)

        api.update(person_id=target.user.person_id,
                   update=update)
        after = api.read(person_id=target.user.person_id)
        try:
            self.assertEqual(update.for_update(), after.for_update())
        finally:
            # restore old settings again
            self.api.person_settings.agent_caller_id.update(person_id=target.user.person_id,
                                                            update=before)
            restored = api.read(person_id=target.user.person_id)
            self.assertEqual(before.for_update(), restored.for_update())
