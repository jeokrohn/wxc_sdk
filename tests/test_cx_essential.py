import asyncio
import base64
import random
from contextlib import contextmanager
from itertools import chain
from typing import Optional

from tests.base import TestCaseWithLog, async_test
from tests.testutil import calling_users, create_cxe_queue
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import UserType
from wxc_sdk.licenses import LicenseProperties, LicenseRequest, LicenseRequestOperation
from wxc_sdk.people import Person
from wxc_sdk.telephony import NumberListPhoneNumberType
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.callqueue.agents import CallQueueAgent
from wxc_sdk.telephony.cx_essentials import ScreenPopConfiguration
from wxc_sdk.telephony.hg_and_cq import Agent


class TestTelephonySupervisors(TestCaseWithLog):
    def cx_essentials_licenses(self) -> set[str]:
        """
        Get all licenses of type Customer Experience - Essential
        :return:
        """
        return {lic.license_id for lic in self.api.licenses.list()
                if lic.cx_essentials}

    def available_cx_essential_license(self) -> Optional[str]:
        """
        get CX essenstial license id for license with available units
        :return:
        """
        return next((lic.license_id for lic in self.api.licenses.list()
                     if (lic.cx_essentials and
                         lic.consumed_units < lic.total_units)),
                    None)

    def users_with_cx_essentials(self) -> list[Person]:
        """
        Get all users with CX Essentials license
        """
        licenses = self.cx_essentials_licenses()
        return [user for user in self.api.people.list()
                if set(user.licenses) & licenses]

    @contextmanager
    def assign_cx_essentials(self, user_id: str):
        """
        Temporarily assign CX Essentials license to a user
        """
        license_id = self.available_cx_essential_license()
        if not license_id:
            self.skipTest('No available CX Essentials license')

        # get primary TN or extension of user
        number = next(n
                      for n in self.api.telephony.phone_numbers(owner_id=user_id)
                      if not n.phone_number or n.phone_number_type == NumberListPhoneNumberType.primary)

        # for some reason when adding a CX essentials license, TN and extension have to be provided
        lp = LicenseProperties(location_id=number.location.id)
        if number.extension:
            lp.extension = number.extension
        if number.phone_number:
            lp.phone_number = number.phone_number
        try:
            # add CX Essentials license
            self.api.licenses.assign_licenses_to_users(
                person_id=user_id,
                licenses=[LicenseRequest(id=license_id,
                                         operation=LicenseRequestOperation.add,
                                         properties=lp)])
            yield
        finally:
            # remove CX Essentials license
            self.api.licenses.assign_licenses_to_users(
                person_id=user_id,
                licenses=[LicenseRequest(id=license_id,
                                         operation=LicenseRequestOperation.remove)])
        return

    @contextmanager
    def assert_user_with_cx_essentials(self) -> Person:
        """
        get a user with CX Essentials license for testt
        """
        # all calling users: users with location_id
        users = calling_users(api=self.api)

        # users with CX Essentials license
        cxe_licenses = self.cx_essentials_licenses()
        users_with_cx_essentials = [user for user in users
                                    if set(user.licenses) & cxe_licenses]

        if users_with_cx_essentials:
            user = random.choice(users_with_cx_essentials)
            print(f'existing CX essentials user: {user.display_name}')
            yield user
            return

        # pick a random user and temporarily assign CX Essentials license
        user = random.choice(calling_users)
        with self.assign_cx_essentials(user_id=user.id):
            print(f'Temporary CX essentials user: {user.display_name}')
            yield user

    def test_queues_w_or_wo_cx_essentials(self):
        """
        List call queues with and without CX Essentials
        """

        def print_agents(queue: CallQueue):
            details = self.api.telephony.callqueue.details(location_id=queue.location_id, queue_id=queue.id,
                                                           has_cx_essentials=queue.has_cx_essentials)
            agents = list(self.api.telephony.callqueue.agents.list(queue_id=queue.id,
                                                                   has_cx_essentials=queue.has_cx_essentials))
            print(f'  {len(agents)} agents:')
            for agent in agents:
                print(f'    {agent.first_name} {agent.last_name} - {agent.type}')
            self.assertEqual(len(agents), len(details.agents), 'Agent count mismatch')
            return

        queues = list(self.api.telephony.callqueue.list())
        self.assertTrue(all(q for q in queues if not q.has_cx_essentials),
                        'All queues without CXE should not have CXE')
        print(f'Got {len(queues)} queues')
        for queue in queues:
            print(f'{queue.name} ({queue.id})')
            print_agents(queue)
        print()

        queues_with_cxe = list(self.api.telephony.callqueue.list(has_cx_essentials=True))
        self.assertTrue(all(q for q in queues_with_cxe if q.has_cx_essentials),
                        'All queues with CXE should have CXE')
        print(f'Got {len(queues_with_cxe)} with CX Essentials')
        for queue in queues_with_cxe:
            print(f'{queue.name} ({queue.id})')
            print_agents(queue)

    @async_test
    async def test_agent_lists(self):
        """
        test consistency between agent list in queue details and agent list for queue
        """

        async def test_queues(has_cx_essentials: bool):
            """
            test all queues with or without CX Essentials

            :param has_cx_essentials:
            """
            # get all queues with or without CX Essentials
            queues = await self.async_api.telephony.callqueue.list(has_cx_essentials=has_cx_essentials)
            if not queues:
                print(f'No queues with CX Essentials: {has_cx_essentials}')
                return
            # for all queues get details and agent list agents.list()
            queue_details, agent_lists = await asyncio.gather(
                asyncio.gather(
                    *[self.async_api.telephony.callqueue.details(location_id=queue.location_id,
                                                                 queue_id=queue.id,
                                                                 has_cx_essentials=queue.has_cx_essentials)
                      for queue in queues]),
                asyncio.gather(
                    *[self.async_api.telephony.callqueue.agents.list(queue_id=queue.id,
                                                                     has_cx_essentials=queue.has_cx_essentials)
                      for queue in queues]))
            queue_details: list[CallQueue]
            agent_lists: list[list[CallQueueAgent]]
            err = None
            name_len = max(len(q.name) for q in queues)
            for details, agents in zip(queue_details, agent_lists):
                agents_in_details = details.agents or []
                agents_in_list = agents or []
                print(f'{details.name:{name_len}}, {has_cx_essentials=}: {len(agents_in_details)} agents in details, '
                      f'{len(agents_in_list)} agents in agents.list(): ', end='')
                try:
                    self.assertEqual(len(agents_in_details), len(agents_in_list),
                                     'Agent count mismatch')
                    # only check UUIDs of agent ids b/c agents.list() (for now) returns wrong type
                    self.assertEqual(set(webex_id_to_uuid(a.agent_id) for a in agents_in_details),
                                     set(webex_id_to_uuid(a.id) for a in agents_in_list),
                                     'Agent list mismatch')
                except AssertionError as e:
                    print(f'{e}')
                    err = err or e
                except Exception as e:
                    print(f'{e}')
                    err = err or e
                else:
                    print('OK')

            if err:
                raise err

        # test queues with and without CX Essentials in parallel
        r = await asyncio.gather(
            test_queues(False),
            test_queues(True),
            return_exceptions=True)

        # check for errors
        err = next((e for e in r if e), None)
        if err:
            raise err

    def test_available_agents_with_cx_essentials(self):
        """
        list available agents with and w/o CX Essentials
        """
        sapi = self.api.telephony.supervisors

        def list_agents(has_cx_essentials: bool):
            agents = list(sapi.available_agents(has_cx_essentials=has_cx_essentials))
            types = set(agent.type for agent in agents)
            print(f'Has CX Essentials: {has_cx_essentials}')
            print(f'Agent types: {", ".join(str(t) for t in types)}')
            print(f'Got {len(agents)} agents')
            for agent in agents:
                print(f'{agent.display_name}, {base64.b64decode(agent.id + "==").decode()}')
            print()

        list_agents(has_cx_essentials=False)
        list_agents(has_cx_essentials=True)

    def test_enable_agent_for_cx_essentials(self):
        """
        Enable agent for CX Essentials
        """
        sapi = self.api.telephony.supervisors
        agents = list(sapi.available_agents())
        agents_with_cxe = list(sapi.available_agents(has_cx_essentials=True))

        # both lists should be disjoint
        self.assertFalse({a.id for a in agents} & {a.id for a in agents_with_cxe},
                         'List of agents with and without CXE should be disjoint')

        # pick an agent
        if not agents:
            self.skipTest('No available agents')
        agent = random.choice([a for a in agents if a.type == UserType.people])
        print(f'Enabling agent for CX Essentials: {agent.display_name}')
        with self.assign_cx_essentials(user_id=agent.id):
            agents_after = list(sapi.available_agents())
            agents_with_cxe_after = list(sapi.available_agents(has_cx_essentials=True))
            self.assertIn(agent.id, {a.id for a in agents_with_cxe_after},
                          'Agent should be in list of agents with CXE')
            self.assertNotIn(agent.id, {a.id for a in agents_after},
                             'Agent should not be in list of agents without CXE')

    def test_aa(self):
        agents = list(self.api.telephony.callqueue.agents.list())
        sup_agents = list(self.api.telephony.supervisors.available_agents())
        agents_with_cxe = list(self.api.telephony.callqueue.agents.list(has_cx_essentials=True))
        sup_agents_with_cxe = list(self.api.telephony.supervisors.available_agents(has_cx_essentials=True))
        foo = 1

    def test_users_with_cx_essentials(self):
        users = self.users_with_cx_essentials()
        print(f'Users with CX Essentials: {len(users)}')
        for user in users:
            print(f'{user.display_name}')

    def test_create_cxe_queue(self):
        """
        create a queue with CX Essentials
        """
        queue = create_cxe_queue(api=self.api)
        try:
            self.assertTrue(queue.has_cx_essentials, 'Queue should have CX Essentials')
        finally:
            self.api.telephony.callqueue.delete_queue(location_id=queue.location_id, queue_id=queue.id)

    @async_test
    async def test_cxe_agents(self):
        users_with_license = self.users_with_cx_essentials()
        queues = list(self.api.telephony.callqueue.list())
        queue_details = await asyncio.gather(
            *[self.async_api.telephony.callqueue.details(location_id=queue.location_id, queue_id=queue.id)
              for queue in queues])
        queue_details: list[CallQueue]
        agents: dict[str, Agent] = {webex_id_to_uuid(agent.agent_id): agent for agent in
                                    chain.from_iterable(q.agents for q in queue_details)}
        print('Agents in queues:')
        for agent in sorted(agents.values(), key=lambda a: (a.user_type, a.last_name, a.first_name)):
            print(f'{agent.user_type} {agent.first_name} {agent.last_name}')
        cxe_agents = list(self.api.telephony.callqueue.agents.list(has_cx_essentials=True))
        disp_len = max(len(user.display_name) for user in users_with_license)
        for user in users_with_license:
            print(f'{user.display_name:{disp_len}}: ', end='')
            agent = next((a for a in cxe_agents if a.id == user.person_id), None)
            if agent is None:
                print('not in list of CQ agents')
            else:
                print(f'Agent: {agent.first_name} {agent.last_name}')

    @contextmanager
    def assert_queues_with_cx_essentials(self) -> list[CallQueue]:
        """
        Assert that there are queues with CX Essentials
        """
        queues_with_cxe = list(self.api.telephony.callqueue.list(has_cx_essentials=True))

        if queues_with_cxe:
            print(f'{len(queues_with_cxe)} existing queues with CX Essentials')
            yield queues_with_cxe
            return

        queue = create_cxe_queue(api=self.api)
        try:
            print(f'Created queue with CX Essentials: {queue.name}')
            yield [queue]
        finally:
            # delete queue again
            print(f'deleting queue with CX Essentials: {queue.name}')
            self.api.telephony.callqueue.delete_queue(location_id=queue.location_id, queue_id=queue.id)
        #

    def test_get_screen_pop_configuration(self):
        """
        Test get_screen_pop_configuration
        """
        with self.assert_queues_with_cx_essentials() as queues:
            queue = queues[0]
            screen_pop_configuration = self.api.telephony.cx_essentials.get_screen_pop_configuration(
                location_id=queue.location_id, queue_id=queue.id)
            print(screen_pop_configuration)

    @contextmanager
    def screen_pop_target(self) -> CallQueue:
        with self.assert_queues_with_cx_essentials() as queues:
            queue = queues[0]
            print(f'screen pop target: {queue.name}')
            screen_pop_configuration = self.api.telephony.cx_essentials.get_screen_pop_configuration(
                location_id=queue.location_id, queue_id=queue.id)
            try:
                config = screen_pop_configuration.model_copy(deep=True)
                yield queue, config
            finally:
                self.api.telephony.cx_essentials.modify_screen_pop_configuration(location_id=queue.location_id,
                                                                                 queue_id=queue.id,
                                                                                 settings=screen_pop_configuration)

    def test_update_screen_pop_configuration(self):
        with self.screen_pop_target() as target:
            queue, screen_pop_configuration = target
            screen_pop_configuration: ScreenPopConfiguration
            queue: CallQueue

            settings = ScreenPopConfiguration(enabled=True, screen_pop_url='https://example.com',
                                              desktop_label='foo', query_params={'foo': 'bar'})
            self.api.telephony.cx_essentials.modify_screen_pop_configuration(location_id=queue.location_id,
                                                                             queue_id=queue.id,
                                                                             settings=settings)
            after = self.api.telephony.cx_essentials.get_screen_pop_configuration(location_id=queue.location_id,
                                                                                  queue_id=queue.id)
            self.assertEqual(settings, after)
