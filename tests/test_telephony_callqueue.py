import asyncio
import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import ClassVar

from wxc_sdk.all_types import *
from .base import TestCaseWithLog, TestCaseWithUsers, async_test

# number of call queues to create by create many test
CQ_MANY = 100


def available_extensions(*, cq_list: list[CallQueue]):
    extensions = set(cq.extension for cq in cq_list)
    return (extension for i in range(1000)
            if (extension := f'{8000 + i}') not in extensions)


class TestList(TestCaseWithLog):

    def test_001_list_all(self):
        """
        list all queues
        """
        queues = list(self.api.telephony.callqueue.list())
        print(f'Got {len(queues)} call queues')
        queues_pag = list(self.api.telephony.callqueue.list(max=50))
        print(f'Total number of queues read with pagination: {len(queues_pag)}')
        self.assertEqual(len(queues), len(queues_pag))

    @async_test
    async def test_002_all_details(self):
        """
        get details of all call queues
        """
        atq = self.async_api.telephony.callqueue
        queues = await atq.list()
        details = await asyncio.gather(*[atq.details(location_id=q.location_id, queue_id=q.id) for q in queues])
        print(f'Got details for {len(details)} call queues')


class TestCreate(TestCaseWithUsers):
    """
    Test call queue creation
    """
    locations: ClassVar[list[Location]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())

    def test_001_create_simple(self):
        """
        create a simple call queue
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        tcq = self.api.telephony.callqueue
        # pick available CQ name in location
        cq_list = list(tcq.list(location_id=target_location.location_id))
        queue_names = set(queue.name for queue in cq_list)
        new_name = next(name for i in range(1000)
                        if (name := f'cq_{i:03}') not in queue_names)
        extension = next(available_extensions(cq_list=cq_list))

        # pick two calling users
        members = random.sample(self.users, 2)

        # settings for new call queue
        settings = CallQueue(name=new_name,
                             extension=extension,
                             call_policies=CallQueueCallPolicies.default(),
                             queue_settings=QueueSettings.default(queue_size=10),
                             agents=[Agent(agent_id=user.person_id) for user in members])
        # creat new queue
        new_queue = tcq.create(location_id=target_location.location_id,
                               settings=settings)

        # and get details of new queue using the queue id
        details = tcq.details(location_id=target_location.location_id,
                              queue_id=new_queue)
        print(json.dumps(json.loads(details.json()), indent=2))

    def test_002_duplicate_call_queue(self):
        """
        Get call queue details and try to create a copy of the queue
        Idea is to test whether the update_or_create() method does the trick of removing details from JSON which
        can't be used in create() call.
        """
        tcq = self.api.telephony.callqueue
        cq_list = list(tcq.list(name='cq_'))
        if not cq_list:
            self.skipTest('No queues cq_* found')
        target_queue = random.choice(cq_list)
        queue_names = set(queue.name for queue in cq_list)
        new_name = next(name for i in range(1000)
                        if (name := f'cq_{i:03}') not in queue_names)
        extension = next(available_extensions(cq_list=cq_list))

        # prepare settings for new queue
        print(f'Creating copy of call queue "{target_queue.name}" in location "{target_queue.location_name}"'
              f'as call queue "{new_name}" ({extension})')
        target_queue_details = tcq.details(location_id=target_queue.location_id,
                                           queue_id=target_queue.id)
        settings = target_queue_details.copy(deep=True)
        settings.extension = extension
        settings.phone_number = ''
        settings.name = new_name
        new_id = tcq.create(location_id=target_queue.location_id,
                            settings=settings)
        details = tcq.details(location_id=target_queue.location_id, queue_id=new_id)

        # details of new queue should be identical to existing with a few exceptions
        details.name = target_queue_details.name
        details.phone_number = target_queue_details.phone_number
        details.extension = target_queue_details.extension
        details.id = target_queue_details.id
        self.assertEqual(target_queue_details, details)

        print(json.dumps(json.loads(details.json()), indent=2))

    def test_003_create_many(self):
        """
        Create large number of call queues and check pagination
        # TODO: monitor CALL-68209, WXCAPIBULK-27
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        tcq = self.api.telephony.callqueue

        # Get names for new call queues
        cq_list = list(tcq.list(location_id=target_location.location_id))
        to_create = max(0, CQ_MANY - len(cq_list))

        print(f'{len(cq_list)} existing queues in location')
        queue_names = set(queue.name for queue in cq_list)
        new_names = (name for i in range(1000)
                     if (name := f'many_{i:03}') not in queue_names)
        names = [name for name, _ in zip(new_names, range(to_create))]
        print(f'got {len(names)} new names')
        extensions = available_extensions(cq_list=cq_list)

        def new_queue(queue_name: str, extension: str):
            """
            Create a new call queue with the given name
            :param queue_name:
            :param extension:
            :return:
            """
            # pick two calling users
            members = random.sample(self.users, 2)

            # settings for new call queue
            settings = CallQueue(name=queue_name,
                                 extension=extension,
                                 call_policies=CallQueueCallPolicies.default(),
                                 queue_settings=QueueSettings.default(queue_size=10),
                                 agents=[Agent(agent_id=user.person_id) for user in members])
            # creat new queue
            new_queue = tcq.create(location_id=target_location.location_id,
                                   settings=settings)
            print(f'Created {queue_name}')
            return new_queue

        if names:
            with ThreadPoolExecutor() as pool:
                new_queues = list(pool.map(lambda name: new_queue(name, extension=next(extensions)),
                                           names))
        print(f'Created {len(names)} call queues.')
        cq_list = list(tcq.list(location_id=target_location.location_id))
        print(f'Total number of queues: {len(cq_list)}')
        queues_pag = list(tcq.list(location_id=target_location.location_id, max=50))
        print(f'Total number of queues read with pagination: {len(queues_pag)}')
        self.assertEqual(len(cq_list), len(queues_pag))


class TestUpdate(TestCaseWithLog):
    """
    Try to update call queues
    """
    queues = ClassVar[list[CallQueue]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.queues = list(cls.api.telephony.callqueue.list(name='cq_'))

    def setUp(self) -> None:
        super().setUp()
        if not self.queues:
            self.skipTest('No call queues cq_*')

    def get_new_name(self) -> str:
        """
        get a new cq name
        """
        queue_names = set(queue.name for queue in self.queues)
        new_name = next(name for i in range(1000)
                        if (name := f'cq_{i:03}') not in queue_names)
        return new_name

    @contextmanager
    def random_queue(self) -> CallQueue:
        target = random.choice(self.queues)
        details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                       queue_id=target.id)
        details.location_id = target.location_id
        details.location_name = target.location_name
        print(f'Updating call queue "{target.name}" ({target.extension}) in location "{target.location_name}"')
        try:
            yield details.copy(deep=True)
        finally:
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id, update=details)

    def test_001_update_extension(self):
        """
        try to change the extension of a queue
        """
        with self.random_queue() as target:
            target: CallQueue
            extensions = set(q.extension for q in self.queues
                             if q.extension)
            new_extension = next(ext for i in range(1000)
                                 if (ext := f'{8000 + i:03}') not in extensions)

            print(f'changing extension to {new_extension}...')
            update = CallQueue(extension=new_extension)
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id,
                                                update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(new_extension, details.extension)
        details.extension = target.extension
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_002_update_name(self):
        """
        try to change the name of a queue
        """
        with self.random_queue() as target:
            target: CallQueue
            new_name = self.get_new_name()

            print(f'Changing name to "{new_name}"...')
            update = CallQueue(name=new_name)
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id,
                                                update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(new_name, details.name)
        details.name = target.name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_003_enable(self):
        """
        Disable a call queue
        """
        with self.random_queue() as target:
            target: CallQueue

            print('Toggle enable...')
            update = CallQueue(enabled=not target.enabled)
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id,
                                                update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(not target.enabled, details.enabled)
        details.enabled = target.enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_004_call_policy_policy(self):
        """
        Change call policy
        """
        with self.random_queue() as target:
            target: CallQueue

            policy = target.call_policies.policy
            other_policies = [p for p in Policy if p != policy]
            new_policy: Policy = random.choice(other_policies)
            print(f'Switch policy from {policy.value} to {new_policy.value}')
            update = CallQueue(call_policies=CallQueueCallPolicies(policy=new_policy))
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id,
                                                update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(new_policy, details.call_policies.policy)
        details.call_policies.policy = policy
        details.location_id = target.location_id
        details.location_name = target.location_name
        # when switching to weighted the agent weights also change. We are ignoring that for the equality test
        for details_agent, target_agent in zip(details.agents, target.agents):
            details_agent.weight = target_agent.weight
        self.assertEqual(target, details)

    def test_005_call_bounce_enabled(self):
        """
        Toggle call bounce enabled
        """
        with self.random_queue() as target:
            target: CallQueue

            bounce_enabled = target.call_policies.call_bounce.enabled
            update = CallQueue(
                call_policies=CallQueueCallPolicies(
                    call_bounce=CallBounce(
                        enabled=not bounce_enabled)))
            print(f' Switch bounce enabled from {bounce_enabled} to {not bounce_enabled}')
            self.api.telephony.callqueue.update(location_id=target.location_id,
                                                queue_id=target.id,
                                                update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(not bounce_enabled, details.call_policies.call_bounce.enabled)
        details.call_policies.call_bounce.enabled = bounce_enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)
