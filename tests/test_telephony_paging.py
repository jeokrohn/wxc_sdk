import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import groupby
from typing import ClassVar

from wxc_sdk.all_types import *
from tests.base import TestCaseWithLog, TestCaseWithUsers, TestWithLocations

# number of paging groups to create in create many test
PG_MANY = 100


def available_extensions(*, pg_list: list[Paging]):
    extensions = set(hg.extension for hg in pg_list)
    return (extension for i in range(1000)
            if (extension := f'{5000 + i}') not in extensions)


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
class TestCreate(TestCaseWithUsers, TestWithLocations):
    """
    Test paging group creation
    """

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
        extension = next(available_extensions(pg_list=pg_list))

        # settings for new paging group
        settings = Paging.create(name=new_name, extension=extension)

        # create new paging group
        print(f'Creating new paging group "{new_name}" in "{target_location.name}"')
        new_pg_id = pgapi.create(location_id=target_location.location_id,
                                 settings=settings)

        # and get details of new paging group using the new id
        details = pgapi.details(location_id=target_location.location_id, paging_id=new_pg_id)

        print(json.dumps(json.loads(details.model_dump_json()), indent=2))

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
        extensions = available_extensions(pg_list=pg_list)

        def new_pg(*, pg_name: str, extension: str):
            """
            Create a new paging group with the given name
            :param pg_name:
            :param extension:
            :return:
            """
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
                list(pool.map(lambda name: new_pg(pg_name=name, extension=next(extensions)),
                              names))
        print(f'Created {len(names)} paging groups.')
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
                        if (name := f'pg_{i:03}') not in pg_names)
        return new_name

    @contextmanager
    def random_pg(self) -> Paging:
        target = random.choice(self.pg_list)
        details = self.api.telephony.paging.details(location_id=target.location_id,
                                                    paging_id=target.paging_id)
        details.location_id = target.location_id
        details.location_name = target.location_name
        print(f'Updating paging group "{target.name}" ({target.extension}) in location "{target.location_name}"')
        try:
            yield details
        finally:
            # try to restore original settings
            self.api.telephony.paging.update(location_id=details.location_id,
                                             paging_id=details.paging_id, update=details)
            restored = self.api.telephony.paging.details(location_id=details.location_id,
                                                         paging_id=details.paging_id)
            restored.location_id = details.location_id
            restored.location_name = details.location_name
            self.assertEqual(details, restored)

    def test_001_update_extension(self):
        """
        try to change the extension of a paging group
        """
        with self.random_pg() as target:
            target: Paging
            # existing extensions
            with self.no_log():
                extensions = set(ext for pn in self.api.telephony.phone_numbers(location_id=target.location_id)
                                 if (ext := pn.extension))
            new_extension = next(ext for i in range(1000)
                                 if (ext := f'{5000 + i:03}') not in extensions)

            print(f'changing extension to {new_extension}...')
            update = Paging(extension=new_extension)
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        # check the extension after the update
        self.assertEqual(new_extension, details.extension)
        # updating the extension also updates the ESN if a routing prefix exists
        if details.routing_prefix:
            self.assertEqual(f'{details.routing_prefix}{new_extension}', details.esn)
        # ignore some settings that are not part of the comparison
        details.extension = target.extension
        details.esn = target.esn
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_002_update_name(self):
        """
        try to change the name of a paging group
        """
        with self.random_pg() as target:
            target: Paging
            new_name = self.get_new_name(location_id=target.location_id)

            print(f'Changing name to "{new_name}"...')
            update = Paging(name=new_name)
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        self.assertEqual(new_name, details.name)
        details.name = target.name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_003_enable(self):
        """
        Disable a paging group
        """
        with self.random_pg() as target:
            target: Paging

            print('Toggle enable...')
            update = Paging(enabled=not target.enabled)
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        self.assertEqual(update.enabled, details.enabled)
        details.enabled = target.enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_004_language_code(self):
        """
        Change language
        """
        with self.random_pg() as target:
            target: Paging

            update = Paging(language_code='de_de' if target.language_code == 'en_us' else 'en_us')
            print(f'Change language code from {target.language_code} ({target.language}) to {update.language_code}')
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
            print(f'updated language code: {details.language_code} ({details.language})')
        self.assertEqual(update.language_code, details.language_code)
        details.language_code = target.language_code
        details.language = target.language
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_005_first_name(self):
        """
        Change first name
        """
        with self.random_pg() as target:
            target: Paging

            update = Paging(first_name=f'first{random.randint(0, 999):03}')
            print(f'Change first name from "{target.first_name}" to "{update.first_name}"')
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        self.assertEqual(update.first_name, details.first_name)
        details.first_name = target.first_name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_006_last_name(self):
        """
        Change last name
        """
        with self.random_pg() as target:
            target: Paging

            update = Paging(last_name=f'last{random.randint(0, 999):03}')
            print(f'Change last name from "{target.last_name}" to "{update.last_name}"')
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        self.assertEqual(update.last_name, details.last_name)
        details.last_name = target.last_name
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_007_originator_caller_id_enabled(self):
        """
        toggle originator_caller_id_enabled
        """
        with self.random_pg() as target:
            target: Paging

            update = Paging(originator_caller_id_enabled=not target.originator_caller_id_enabled)
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        self.assertEqual(update.originator_caller_id_enabled, details.originator_caller_id_enabled)
        details.originator_caller_id_enabled = target.originator_caller_id_enabled
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def available_users(self, *, pg: Paging) -> list[Person]:
        """
        users not ued in originators nor targets
        :param pg: paging group
        :return: list of users
        """
        used = set(agent.agent_id for agent in pg.originators).union(agent.agent_id for agent in pg.targets)
        return [user for user in self.users if user.person_id not in used]

    def test_008_add_originator(self):
        """
        add originator
        """
        with self.random_pg() as target:
            target: Paging
            users = self.available_users(pg=target)
            if not users:
                self.skipTest('No users available to add as originator')
            new_originator = random.choice(users)
            update = Paging(originators=(target.originators or []) + [PagingAgent(agent_id=new_originator.person_id)])
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        # order or originators not necessarily the same as in update, but the set of agent ids should be identical
        self.assertEqual(set(a.agent_id for a in update.originators),
                         set(a.agent_id for a in details.originators))
        details.originators = target.originators
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)

    def test_009_add_target(self):
        """
        add target
        """
        with self.random_pg() as target:
            target: Paging
            users = self.available_users(pg=target)
            if not users:
                self.skipTest('No users available to add as originator')
            new_target = random.choice(users)
            update = Paging(targets=(target.targets or []) + [PagingAgent(agent_id=new_target.person_id)])
            self.api.telephony.paging.update(location_id=target.location_id,
                                             paging_id=target.paging_id,
                                             update=update)
            details = self.api.telephony.paging.details(location_id=target.location_id,
                                                        paging_id=target.paging_id)
        # order or targets not necessarily the same as in update, but the set of agent ids should be identical
        self.assertEqual(set(a.agent_id for a in update.targets),
                         set(a.agent_id for a in details.targets))
        details.targets = target.targets
        details.location_id = target.location_id
        details.location_name = target.location_name
        self.assertEqual(target, details)
