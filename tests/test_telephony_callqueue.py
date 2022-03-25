import json
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar, List
from contextlib import contextmanager

from .base import TestCaseWithLog, TestCaseWithUsers
from wxc_sdk.types import Location, CallQueue, CallPolicies, QueueSettings, Agent, Policy, CallBounce


class TestList(TestCaseWithLog):

    def test_001_list_all(self):
        """
        list all queues
        """
        queues = list(self.api.telephony.callqueue.list())
        print(f'Got {len(queues)} call queues')

    def test_002_all_details(self):
        """
        get details of all call queues
        """
        atq = self.api.telephony.callqueue
        queues = list(atq.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda q: atq.details(location_id=q.location_id, queue_id=q.id),
                queues))
        print(f'Got details for {len(queues)} call queues')


class TestCreate(TestCaseWithUsers):
    """
    Test call queue creation
    """
    locations: ClassVar[List[Location]]

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
        queues = list(tcq.list(location_id=target_location.location_id))
        queue_names = set(queue.name for queue in queues)
        new_name = next(name for i in range(1000)
                        if (name := f'cq_{i:03}') not in queue_names)
        extension = str(8000 + int(new_name[-3:]))

        # pick two calling users
        members = random.sample(self.users, 2)

        # settings for new call queue
        settings = CallQueue(name=new_name,
                             extension=extension,
                             call_policies=CallPolicies.default(),
                             queue_settings=QueueSettings.default(queue_size=10),
                             agents=[Agent(agent_id=user.person_id) for user in members])
        # creat new queue
        new_queue = tcq.create(location_id=target_location.location_id,
                               queue=settings)

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
        queues = list(tcq.list(name='cq_'))
        if not queues:
            self.skipTest('No queues cq_* found')
        target_queue = random.choice(queues)
        queue_names = set(queue.name for queue in queues)
        new_name = next(name for i in range(1000)
                        if (name := f'cq_{i:03}') not in queue_names)
        extension = str(8000 + int(new_name[-3:]))

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
                            queue=settings)
        details = tcq.details(location_id=target_queue.location_id, queue_id=new_id)
        print(json.dumps(json.loads(details.json()), indent=2))


class TestUpdate(TestCaseWithLog):
    """
    Try to update call queues
    """
    queues = ClassVar[List[CallQueue]]

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
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
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
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
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
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
                                                          queue_id=target.id,
                                                          update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(new_name, details.name)
        details.name = target.name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def xxx(self):
        from wxc_sdk import WebexSimpleApi
        from wxc_sdk.types import CallQueue, CallPolicies, CallBounce, Policy

        api = WebexSimpleApi()

        # shortcut
        cq = api.telephony.callqueue

        # disable a call queue
        update = CallQueue(enabled=False)
        cq.update_callqueue(location_id=...,
                            queue_id=...,
                            update=update)

        # set the call routing policy to SIMULTANEOUS
        update = CallQueue(call_policies=CallPolicies(policy=Policy.simultaneous))
        cq.update_callqueue(location_id=...,
                            queue_id=...,
                            update=update)
        # don't bounce calls after the set number of rings.
        update = CallQueue(
            call_policies=CallPolicies(
                call_bounce=CallBounce(
                    enabled=False)))
        cq.update_callqueue(location_id=...,
                            queue_id=...,
                            update=update)

        details = cq.details(location_id=...,
                             queue_id=...)
        details.call_policies.call_bounce.agent_unavailable_enabled=False
        details.call_policies.call_bounce.on_hold_enabled=False
        cq.update_callqueue(location_id=...,
                            queue_id=...,
                            update=details)

    def test_003_enable(self):
        """
        Disable a call queue
        """
        with self.random_queue() as target:
            target: CallQueue

            print(f'Toggle enable...')
            update = CallQueue(enabled=not target.enabled)
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
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
            update = CallQueue(call_policies=CallPolicies(policy=new_policy))
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
                                                          queue_id=target.id,
                                                          update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(new_policy, details.call_policies.policy)
        details.call_policies.policy = policy
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_005_call_bounce_enabled(self):
        """
        Toggle call bounce enabled
        """
        with self.random_queue() as target:
            target: CallQueue

            bounce_enabled = target.call_policies.call_bounce.enabled
            update = CallQueue(
                call_policies=CallPolicies(
                    call_bounce=CallBounce(
                        enabled=not bounce_enabled)))
            print(f' Switch bounce enabled from {bounce_enabled} to {not bounce_enabled}')
            self.api.telephony.callqueue.update_callqueue(location_id=target.location_id,
                                                          queue_id=target.id,
                                                          update=update)
            details = self.api.telephony.callqueue.details(location_id=target.location_id,
                                                           queue_id=target.id)
        self.assertEqual(not bounce_enabled, details.call_policies.call_bounce.enabled)
        details.call_policies.call_bounce.enabled = bounce_enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)
