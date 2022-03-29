# TODO: test cases

import json
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import ClassVar

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
