import asyncio
import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import ClassVar

from wxc_sdk.all_types import *
from tests.base import TestCaseWithLog, TestCaseWithUsers, TestWithLocations, async_test
from tests.testutil import available_extensions_gen

# number of huntgroups to create my create many test
HG_MANY = 100


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

    @async_test
    async def test_002_all_details(self):
        """
        get details of all hunt groups
        """
        hapi = self.async_api.telephony.huntgroup
        hg_list = await hapi.list()
        details = await asyncio.gather(*[hapi.details(location_id=hg.location_id,
                                                      huntgroup_id=hg.id)
                                         for hg in hg_list],
                                       return_exceptions=True)
        err = None
        for hg, detail in zip(hg_list, details):
            hg: HuntGroup
            if isinstance(detail, Exception):
                err = err or detail
                print(f'{hg.name}/{hg.location_name}: {detail}')
            detail: HuntGroup
            if detail.address_agents is not None:
                print(f'{hg.name}/{hg.location_name}: unknown attribute address_agents set')
                err = err or ValueError('address_agents set')
        if all(not isinstance(detail, HuntGroup) or detail.address_agents is None for detail in details):
            print('undocumented address_agents attribute not set any more; remove from class definition')
        if err:
            raise err
        print(f'Got details for {len(details)} hunt groups')


class TestCreate(TestWithLocations, TestCaseWithUsers):
    """
    Test hunt group creation
    """

    def test_001_create_simple(self):
        """
        create a simple hunt group
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        hapi = self.api.telephony.huntgroup
        # pick available HG name in location
        hg_list = list(hapi.list(location_id=target_location.location_id))
        hg_names = set(hg.name for hg in hg_list)
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in hg_names)
        extension = next(available_extensions_gen(api=self.api, location_id=target_location.location_id, seed='6000'))

        # pick two calling users
        members = random.sample(self.users, 2)

        # settings for new hunt group
        settings = HuntGroup(name=new_name,
                             extension=extension,
                             agents=[Agent(agent_id=user.person_id) for user in members])

        # creat new hg
        new_hg_id = hapi.create(location_id=target_location.location_id,
                                settings=settings)
        try:
            # and get details of new queue using the queue id
            details = hapi.details(location_id=target_location.location_id, huntgroup_id=new_hg_id)
            print(json.dumps(json.loads(details.model_dump_json()), indent=2))
            self.assertTrue(details.address_agents is None, 'Undocumented address_agents attribute')
            self.assertTrue(details.address_agents is not None,
                            'Undocumented address_agents attribute is gone; remove from class')
        finally:
            # delete the new hunt group
            hapi.delete_huntgroup(location_id=target_location.location_id, huntgroup_id=new_hg_id)

    def test_002_duplicate_hg(self):
        """
        Get hg details and try to create a copy of the hg
        Idea is to test whether the update_or_create() method does the trick of removing details from JSON which
        can't be used in create() call.
        """
        hapi = self.api.telephony.huntgroup
        hg_list = list(hapi.list())
        candidates = [hg for hg in hg_list
                      if hg.name.startswith('hg_')]
        if not candidates:
            self.skipTest('No hunt groups hg_* found')
        target_hg = random.choice(candidates)
        # reduce list to hgs in same location
        hg_list = [hg for hg in hg_list
                   if hg.location_id == target_hg.location_id]
        hg_names = set(hg.name for hg in hg_list)
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in hg_names)
        extension = next(available_extensions_gen(api=self.api, location_id=target_hg.location_id, seed='6000'))

        # prepare settings for new hg
        print(f'Creating copy of hunt group "{target_hg.name}" in location "{target_hg.location_name}" '
              f'as hunt group "{new_name}" ({extension})')
        target_hg_details = hapi.details(location_id=target_hg.location_id, huntgroup_id=target_hg.id)
        settings = target_hg_details.model_copy(deep=True)
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

        print(json.dumps(json.loads(details.model_dump_json()), indent=2))

    def test_003_create_many(self):
        """
        Create large number of hunt groups and check pagination
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        hapi = self.api.telephony.huntgroup

        # Get names for new hunt groups
        hg_list = list(hapi.list(location_id=target_location.location_id))
        to_create = max(0, HG_MANY - len(hg_list))

        print(f'{len(hg_list)} existing hunt groups')
        hg_names = set(hg.name for hg in hg_list)
        new_names = (name for i in range(1000)
                     if (name := f'many_{i:03}') not in hg_names)
        names = [name for name, _ in zip(new_names, range(to_create))]
        print(f'got {len(names)} new names')
        extensions = available_extensions_gen(api=self.api, location_id=target_location.location_id, seed='6000')

        def new_hg(*, hg_name: str, extension: str):
            """
            Create a new call hunt groups with the given name
            :param hg_name:
            :param extension:
            :return:
            """
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
                list(pool.map(lambda name: new_hg(hg_name=name, extension=next(extensions)),
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
    hg_list = ClassVar[list[HuntGroup]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.hg_list = [hg for hg in cls.api.telephony.huntgroup.list()
                       if hg.name.startswith('hg_') or hg.name.startswith('many_')]

    def setUp(self) -> None:
        super().setUp()
        if not self.hg_list:
            self.skipTest('No target hunt groups')

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
            yield details.model_copy(deep=True)
        finally:
            self.api.telephony.huntgroup.update(location_id=target.location_id,
                                                huntgroup_id=target.id, update=details)

    def test_001_update_extension(self):
        """
        try to change the extension of a queue
        """
        with self.random_hg() as target:
            target: HuntGroup
            # get new extension based on extensions already assigned to HGs in location
            new_extension = next(available_extensions_gen(api=self.api,
                                                          location_id=target.location_id, seed='6000'))

            print(f'changing extension to {new_extension}...')
            update = HuntGroup(extension=new_extension)
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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

            print('Toggle enable...')
            update = HuntGroup(enabled=not target.enabled)
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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
            print(f'Switch policy from {policy} to {new_policy.value}')
            update = HuntGroup(call_policies=HGCallPolicies(policy=new_policy))
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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
            self.api.telephony.huntgroup.update(location_id=target.location_id,
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
