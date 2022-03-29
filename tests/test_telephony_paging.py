# TODO: test cases

import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import groupby
from typing import ClassVar
from unittest import skip

from wxc_sdk.types import *
from .base import TestCaseWithLog, TestCaseWithUsers

# number of paging groups to create in create many test
PG_MANY = 100


class TestPaging(TestCaseWithLog):

    def test_001_list(self):
        """
        list paging groups
        """
        pgs = list(self.api.telephony.paging.list())
        print(f'Got {len(pgs)} paging groups')

    def test_002_all_details(self):
        """
        get details for all paging groups
        """
        atp = self.api.telephony.paging
        pgs = list(atp.list())
        if not pgs:
            self.skipTest('No existing paging groups')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda pg: atp.details(location_id=pg.location_id,
                                       paging_id=pg.paging_id),
                pgs))
        print(f'Got details for {len(details)} paging groups')


@dataclass(init=False)
class TestCreate(TestCaseWithUsers):
    """
    Test paging group creation
    """

    locations: ClassVar[list[Location]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())

    def test_001_create_simple(self):
        """
        create a simple paging group
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        pgapi = self.api.telephony.paging
        # pick available PG name in location
        pg_list = list(pgapi.list(location_id=target_location.location_id))
        pg_names = set(pg.name for pg in pg_list)
        new_name = next(name for i in range(1000)
                        if (name := f'pg_{i:03}') not in pg_names)
        extension = str(5000 + int(new_name[-3:]))

        # settings for new paging group
        settings = Paging.create(name=new_name, extension=extension)

        # create new paging group
        print(f'Creating new paging group "{new_name}" in "{target_location.name}"')
        new_pg_id = pgapi.create(location_id=target_location.location_id,
                                 settings=settings)

        # and get details of new paging group using the new id
        details = pgapi.details(location_id=target_location.location_id, paging_id=new_pg_id)

        print(json.dumps(json.loads(details.json()), indent=2))

    def test_002_create_many(self):
        """
        Create large number of paging groups and check pagination
        """
        # pick a random location
        target_location = random.choice(self.locations)
        print(f'Target location: {target_location.name}')

        pgapi = self.api.telephony.paging

        # Get names for new paging groups
        pg_list = list(pgapi.list(location_id=target_location.location_id))
        to_create = max(0, PG_MANY - len(pg_list))

        print(f'{len(pg_list)} existing paging groups')
        pg_names = set(pg.name for pg in pg_list)
        new_names = (name for i in range(1000)
                     if (name := f'many_{i:03}') not in pg_names)
        names = [name for name, _ in zip(new_names, range(to_create))]
        print(f'got {len(names)} new names')

        def new_pg(*, pg_name: str):
            """
            Create a new paging group with the given name
            :param pg_name:
            :return:
            """
            extension = str(5000 + int(pg_name[-3:]))
            # pick two targets and originators
            random.shuffle(self.users)
            if len(self.users) < 4:
                self.skipTest('Need at least 4 calling users to run the test')
            targets = self.users[:2]
            originators = self.users[2:4]
            settings = Paging(name=pg_name, extension=extension,
                              originators=[PagingAgent(agent_id=o.person_id) for o in originators],
                              targets=[PagingAgent(agent_id=t.person_id) for t in targets],
                              originator_caller_id_enabled=True)

            # creat new paging group
            new_pg_id = pgapi.create(location_id=target_location.location_id,
                                     settings=settings)
            print(f'Created {pg_name}')
            return new_pg_id

        if names:
            with ThreadPoolExecutor() as pool:
                new_hg_ids = list(pool.map(lambda name: new_pg(pg_name=name),
                                           names))
        print(f'Created {len(new_hg_ids)} paging groups.')
        pg_list = list(pgapi.list(location_id=target_location.location_id))
        print(f'Total number of paging groups: {len(pg_list)}')
        queues_pag = list(pgapi.list(location_id=target_location.location_id, max=50))
        print(f'Total number of paging groups read with pagination: {len(queues_pag)}')
        self.assertEqual(len(pg_list), len(queues_pag))


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):
    """
    Try to update paging groups
    """
    locations: ClassVar[list[Location]]
    pg_list = ClassVar[list[Paging]]
    pg_by_location = dict[str, list[Paging]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = [pg for pg in cls.api.locations.list()
                         if pg.name.startswith('pg_') or pg.name.startswith('many_')]
        cls.pg_list = list(cls.api.telephony.paging.list())
        # paging groups grouped by location
        cls.pg_by_location = {location_id: list(pgi)
                              for location_id, pgi in groupby(sorted(cls.pg_list,
                                                                     key=lambda pg: pg.location_id),
                                                              key=lambda pg: pg.location_id)}

    def setUp(self) -> None:
        super().setUp()
        if not self.pg_list:
            self.skipTest('No target paging groups')

    def get_new_name(self, *, location_id: str) -> str:
        """
        get a new paging group in given location
        """
        pg_names = set(pg.name for pg in self.pg_by_location[location_id])
        new_name = next(name for i in range(1000)
                        if (name := f'hg_{i:03}') not in pg_names)
        return new_name

    @contextmanager
    def random_pg(self) -> HuntGroup:
        target = random.choice(self.pg_list)
        details = self.api.telephony.paging.details(location_id=target.location_id,
                                                    paging_id=target.paging_id)
        details.location_id = target.location_id
        details.location_name = target.location_name
        print(f'Updating paging group "{target.name}" ({target.extension}) in location "{target.location_name}"')
        try:
            yield details
        finally:
            self.api.telephony.paging.update(location_id=target.location_id,
                                             huntgroup_id=target.id, update=details)

    @skip('change to paging group')
    def test_001_update_extension(self):
        """
        try to change the extension of a queue
        """
        with self.random_pg() as target:
            target: HuntGroup
            extensions = set(q.extension for q in self.hg_list
                             if q.extension)
            new_extension = next(ext for i in range(1000)
                                 if (ext := f'{6000 + i:03}') not in extensions)

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

    @skip('change to paging group')
    def test_002_update_name(self):
        """
        try to change the name of a hunt group
        """
        with self.random_pg() as target:
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

    @skip('change to paging group')
    def test_003_enable(self):
        """
        Disable a hunt group
        """
        with self.random_pg() as target:
            target: HuntGroup

            print(f'Toggle enable...')
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

    @skip('change to paging group')
    def test_004_call_policy_policy(self):
        """
        Change call policy
        """
        with self.random_pg() as target:
            target: HuntGroup

            policy = target.call_policies.policy
            other_policies = [p for p in Policy if p != policy]
            new_policy: Policy = random.choice(other_policies)
            print(f'Switch policy from {policy.value} to {new_policy.value}')
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

    @skip('change to paging group')
    def test_005_distinctive_ring(self):
        """
        Change distinctive ring
        """
        with self.random_pg() as target:
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

    @skip('change to paging group')
    def test_060_add_agent(self):
        """
        Add an agent to a hunt group
        """
        with self.random_pg() as target:
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
