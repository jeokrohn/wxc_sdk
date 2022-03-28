import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import ClassVar, List

from wxc_sdk.types import *
from .base import TestCaseWithLog, TestCaseWithUsers


class TestList(TestCaseWithLog):

    def test_001_list_all(self):
        """
        list all hunt groups
        """
        hapi = self.api.telephony.huntgroup
        hg_list = list(hapi.list())
        print(f'Got {len(hg_list)} hunt groups')
        queues_pag = list(hapi.list(max=50))
        print(f'Total number of queues read with pagination: {len(queues_pag)}')
        self.assertEqual(len(hg_list), len(queues_pag))

    def test_002_all_details(self):
        """
        get details of all hunt groups
        """
        hapi = self.api.telephony.huntgroup
        hg_list = list(hapi.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda hg: hapi.details(location_id=hg.location_id, huntgroup_id=hg.id),
                hg_list))
        print(f'Got details for {len(hg_list)} hunt groups')


class TestCreate(TestCaseWithUsers):
    """
    Test hunt group creation
    """
    locations: ClassVar[List[Location]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())

    def test_001_create_simple(self):
        """
        create a simple hunt group
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        hapi = self.api.telephony.huntgroup
        # pick available HG name in location
        hgs = list(hapi.list(location_id=target_location.location_id))
        hg_names = set(hg.name for hg in hgs)
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in hg_names)
        extension = str(6000 + int(new_name[-3:]))

        # pick two calling users
        members = random.sample(self.users, 2)

        # settings for new hunt group
        settings = HuntGroup(name=new_name,
                             extension=extension,
                             agents=[Agent(agent_id=user.person_id) for user in members])

        # creat new hg
        new_hg_id = hapi.create(location_id=target_location.location_id,
                                settings=settings)

        # and get details of new queue using the queue id
        details = hapi.details(location_id=target_location.location_id, huntgroup_id=new_hg_id)
        print(json.dumps(json.loads(details.json()), indent=2))

    def test_002_duplicate_hg(self):
        """
        Get hg details and try to create a copy of the hg
        Idea is to test whether the update_or_create() method does the trick of removing details from JSON which
        can't be used in create() call.
        """
        hapi = self.api.telephony.huntgroup
        hg_list = list(hapi.list(name='hg_'))
        if not hg_list:
            self.skipTest('No hunr groups hg_* found')
        target_hg = random.choice(hg_list)
        hg_names = set(hg.name for hg in hg_list)
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in hg_names)
        extension = str(6000 + int(new_name[-3:]))

        # prepare settings for new hg
        print(f'Creating copy of hunt group "{target_hg.name}" in location "{target_hg.location_name}"'
              f'as hunt group "{new_name}" ({extension})')
        target_hg_details = hapi.details(location_id=target_hg.location_id, huntgroup_id=target_hg.id)
        settings = target_hg_details.copy(deep=True)
        settings.extension = extension
        settings.phone_number = ''
        settings.name = new_name
        new_id = hapi.create(location_id=target_hg.location_id,
                             settings=settings)
        # details of new HG should be identical to existing with a few exceptions
        details = hapi.details(location_id=target_hg.location_id, huntgroup_id=new_id)
        details.name = target_hg_details.name
        details.phone_number = target_hg_details.phone_number
        details.extension = target_hg_details.extension
        details.id = target_hg_details.id
        self.assertEqual(target_hg_details, details)

        print(json.dumps(json.loads(details.json()), indent=2))

    def test_003_create_many(self):
        """
        Create large number of hunt groups and check pagination
        """
        HG_NUMBER = 300
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        hapi = self.api.telephony.huntgroup

        # Get names for new hunt groups
        hg_list = list(hapi.list(location_id=target_location.location_id))
        to_create = max(0, HG_NUMBER - len(hg_list))

        print(f'{len(hg_list)} existing hunt groups')
        queue_names = set(queue.name for queue in hg_list)
        new_names = (name for i in range(1000)
                     if (name := f'many_{i:03}') not in queue_names)
        names = [name for name, _ in zip(new_names, range(to_create))]
        print(f'got {len(names)} new names')

        def new_hg(*, hg_name: str):
            """
            Create a new call hunt groups with the given name
            :param hg_name:
            :return:
            """
            extension = str(6000 + int(hg_name[-3:]))
            # pick two calling users
            members = random.sample(self.users, 2)

            # settings for new call hunt group
            settings = HuntGroup(name=hg_name,
                                 extension=extension,
                                 call_policies=HGCallPolicies.default(),
                                 agents=[Agent(agent_id=user.person_id) for user in members])
            # creat new hunt group
            new_hg_id = hapi.create(location_id=target_location.location_id,
                                    settings=settings)
            print(f'Created {hg_name}')
            return new_hg_id

        if names:
            with ThreadPoolExecutor() as pool:
                new_hg_ids = list(pool.map(lambda name: new_hg(hg_name=name),
                                           names))
        print(f'Created {len(names)} call hunt groups.')
        hg_list = list(hapi.list(location_id=target_location.location_id))
        print(f'Total number of hunt groups: {len(hg_list)}')
        queues_pag = list(hapi.list(location_id=target_location.location_id, max=50))
        print(f'Total number of hunt groups read with pagination: {len(queues_pag)}')
        self.assertEqual(len(hg_list), len(queues_pag))


class TestUpdate(TestCaseWithUsers):
    """
    Try to update hunt groups
    """
    hg_list = ClassVar[List[HuntGroup]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.hg_list = list(cls.api.telephony.huntgroup.list(name='hg_'))

    def setUp(self) -> None:
        super().setUp()
        if not self.hg_list:
            self.skipTest('No hunt groups hg_*')

    def get_new_name(self) -> str:
        """
        get a new hg name
        """
        hg_names = set(queue.name for queue in self.hg_list)
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in hg_names)
        return new_name

    @contextmanager
    def random_hg(self) -> HuntGroup:
        target = random.choice(self.hg_list)
        details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                       huntgroup_id=target.id)
        details.location_id = target.location_id
        details.location_name = target.location_name
        print(f'Updating hunt group "{target.name}" ({target.extension}) in location "{target.location_name}"')
        try:
            yield details.copy(deep=True)
        finally:
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id, update=details)

    def test_001_update_extension(self):
        """
        try to change the extension of a queue
        """
        with self.random_hg() as target:
            target: HuntGroup
            extensions = set(q.extension for q in self.hg_list
                             if q.extension)
            new_extension = next(ext for i in range(1000)
                                 if (ext := f'{6000 + i:03}') not in extensions)

            print(f'changing extension to {new_extension}...')
            update = HuntGroup(extension=new_extension)
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        self.assertEqual(new_extension, details.extension)
        details.extension = target.extension
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_002_update_name(self):
        """
        try to change the name of a hunt group
        """
        with self.random_hg() as target:
            target: HuntGroup
            new_name = self.get_new_name()

            print(f'Changing name to "{new_name}"...')
            update = HuntGroup(name=new_name)
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        self.assertEqual(new_name, details.name)
        details.name = target.name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_003_enable(self):
        """
        Disable a hunt group
        """
        with self.random_hg() as target:
            target: HuntGroup

            print(f'Toggle enable...')
            update = HuntGroup(enabled=not target.enabled)
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        self.assertEqual(not target.enabled, details.enabled)
        details.enabled = target.enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_004_call_policy_policy(self):
        """
        Change call policy
        """
        with self.random_hg() as target:
            target: HuntGroup

            policy = target.call_policies.policy
            other_policies = [p for p in Policy if p != policy]
            new_policy: Policy = random.choice(other_policies)
            print(f'Switch policy from {policy.value} to {new_policy.value}')
            update = HuntGroup(call_policies=HGCallPolicies(policy=new_policy))
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        self.assertEqual(new_policy, details.call_policies.policy)
        details.call_policies.policy = policy
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_005_distinctive_ring(self):
        """
        Change distinctive ring
        """
        with self.random_hg() as target:
            target: HuntGroup

            distinctive_ring = target.alternate_number_settings.distinctive_ring_enabled
            print(f'Switch distinctive ring from {distinctive_ring} to {not distinctive_ring}')
            update = HuntGroup(
                alternate_number_settings=AlternateNumberSettings(distinctive_ring_enabled=not distinctive_ring))
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        self.assertEqual(not distinctive_ring, details.alternate_number_settings.distinctive_ring_enabled)
        details.alternate_number_settings.distinctive_ring_enabled = distinctive_ring
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_060_add_agent(self):
        """
        Add an agent to a hunt group
        """
        with self.random_hg() as target:
            target: HuntGroup
            agents_in_target = set(agent.agent_id for agent in target.agents)
            available_agents = [user for user in self.users
                                if user.person_id not in agents_in_target]
            if not available_agents:
                self.skipTest('No available agents')
            new_agent = random.choice(available_agents)

            print(f'Adding agent "{new_agent.display_name}"')
            new_agents = target.agents + [Agent(agent_id=new_agent.person_id)]

            update = HuntGroup(agents=new_agents)
            self.api.telephony.huntgroup.update_huntgroup(location_id=target.location_id,
                                                          huntgroup_id=target.id,
                                                          update=update)
            details = self.api.telephony.huntgroup.details(location_id=target.location_id,
                                                           huntgroup_id=target.id)
        new_agent_ids = set(agent.agent_id for agent in new_agents)
        agent_ids = set(agent.agent_id for agent in details.agents)
        self.assertEqual(new_agent_ids, agent_ids)
        details.agents = target.agents
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)
