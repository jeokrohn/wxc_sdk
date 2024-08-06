import base64
import random
from contextlib import contextmanager

from tests.base import TestCaseWithLog
from wxc_sdk import WebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import PatternAction, UserType
from wxc_sdk.telephony.supervisor import AgentOrSupervisor, IdAndAction


class AgentsAndSupervisors:
    available_agents: list[AgentOrSupervisor]
    available_supervisors: list[AgentOrSupervisor]

    def __init__(self, api: WebexSimpleApi):
        sapi = api.telephony.supervisors
        self.available_agents = list(sapi.available_agents())
        self.available_supervisors = list(sapi.available_supervisors())

    @property
    def available_supervisors_not_agent(self) -> list[AgentOrSupervisor]:
        agent_ids = set(agent.id for agent in self.available_agents)
        return [supervisor for supervisor in self.available_supervisors
                if supervisor.id not in agent_ids]


class TestTelephonySupervisors(TestCaseWithLog):
    def test_available_agents(self):
        """
        list available agents
        """
        sapi = self.api.telephony.supervisors
        agents = list(sapi.available_agents())
        types = set(agent.type for agent in agents)
        print(f'Agent types: {", ".join(str(t) for t in types)}')
        print(f'Got {len(agents)} agents')

    def test_available_supervisors(self):
        """
        List available supervisors
        """
        sapi = self.api.telephony.supervisors
        supervisors = list(sapi.available_supervisors())
        print(f'Got {len(supervisors)} supervisors')
        dn_len = max(len(sup.display_name) for sup in supervisors)
        for supervisor in supervisors:
            decoded_id = base64.b64decode(f'{supervisor.id}==').decode()
            print(f'{supervisor.display_name:{dn_len}} ({decoded_id})')

        # determine set of VL UUIDs; we suspect that there are multiple supervisor types and some VLs are available
        virtual_lines = list(self.api.telephony.virtual_lines.list())
        virtual_line_uuid_set = set(webex_id_to_uuid(virtual_line.id) for virtual_line in virtual_lines)
        vl_supervisors = [supervisor for supervisor in supervisors if
                          webex_id_to_uuid(supervisor.id) in virtual_line_uuid_set]
        if vl_supervisors:
            print()
            print('Based on their UUIDs, the following supervisors seem to be VLs:')
            dn_len = max(len(sup.display_name) for sup in vl_supervisors)
            print('\n'.join(
                f'{sup.display_name:{dn_len}} ({base64.b64decode(sup.id + "==").decode()})' for sup in vl_supervisors))
        supervisor_types = set(base64.b64decode(f'{supervisor.id}==').decode().split('/')[-2]
                               for supervisor in supervisors)
        self.assertTrue(len(supervisor_types) > 1,
                        'Expected multiple supervisor types (CALL-150914)')

    def test_supervisor_and_not_agent(self):
        """
        Get available supervisors and agents; derive available supervisors that are not agents
        """
        sapi = self.api.telephony.supervisors
        agents = list(sapi.available_agents())
        agent_ids = set(agent.id for agent in agents)
        supervisors = list(sapi.available_supervisors())
        supervisor_not_agent = [supervisor for supervisor in supervisors
                                if supervisor.id not in agent_ids]
        print(f'Got {len(agents)} available agents')
        print(f'Got {len(supervisors)} available supervisors')
        print(f'Got {len(supervisor_not_agent)} available supervisors that are not agents')

    def test_create(self, vl_agent: bool = False):
        """
        create a supervisor with a single agent
        """
        sapi = self.api.telephony.supervisors

        # get an available supervisor that is not an agent
        agents_and_supervisors = AgentsAndSupervisors(api=self.api)
        if not agents_and_supervisors.available_supervisors:
            self.skipTest('No available supervisors')
        supervisor = random.choice(agents_and_supervisors.available_supervisors)
        supervisor: AgentOrSupervisor
        print(f'New Supervisor: {supervisor.display_name}')

        # pick an agent
        if vl_agent:
            available_agents = [agent for agent in agents_and_supervisors.available_agents
                                if agent.type == UserType.virtual_line]
        else:
            available_agents = agents_and_supervisors.available_agents
        if not available_agents:
            self.skipTest('No available agents')
        agent = random.choice(available_agents)

        # create supervisor with that agent
        sapi.create(id=supervisor.id, agents=[agent.id])

        try:
            details = list(sapi.details(supervisor_id=supervisor.id))

            # make sure the agent is in there
            self.assertEqual(1, len(details))
            self.assertEqual(agent.id, details[0].id,
                             f'agent ID mismatch, expected {base64.b64decode(agent.id + "==").decode()}, actual '
                             f'{base64.b64decode(details[0].id + "==").decode()}')

            # list supervisors and make sure we see the supervisor we created
            supervisor_list = list(sapi.list())
            supervisor_in_list = next((sup for sup in supervisor_list if sup.id == supervisor.id), None)
            self.assertIsNotNone(supervisor_in_list)
            self.assertEqual(1, supervisor_in_list.agent_count)

            # verify that created supervisor is not available as supervisor anymore
            agents_and_supervisors_after = AgentsAndSupervisors(api=self.api)
            self.assertIsNone(next((sup for sup in agents_and_supervisors_after.available_supervisors
                                    if sup.id == supervisor.id), None))

        finally:
            # cleanup: delete supervisor again
            sapi.delete(supervisor_id=supervisor.id)
            list_after_delete = list(sapi.list())
            self.assertIsNone(next((sup for sup in list_after_delete if sup.id == supervisor.id), None))

    def test_create_with_vl_as_agent(self):
        """
        create a supervisor with a single agent; the agent is a VL
        """
        self.test_create(vl_agent=True)

    @contextmanager
    def assign_unassign(self):
        """
        Context manager for assign/unassign tests
        """
        sapi = self.api.telephony.supervisors
        agents_and_supervisors = AgentsAndSupervisors(api=self.api)

        # pick a supervisor and three agents
        if not agents_and_supervisors.available_supervisors:
            self.skipTest('No available supervisors')
        if len(agents_and_supervisors.available_agents) < 3:
            self.skipTest('Not enough available agents; need at least 3')
        supervisor = random.choice(agents_and_supervisors.available_supervisors)
        agents = random.sample(agents_and_supervisors.available_agents, 3)
        agents: list[AgentOrSupervisor]

        # create supervisor with two agents (1st and 2nd)
        print(f'Creating supervisor {supervisor.display_name} with agents: '
              f'{", ".join(a.display_name for a in agents[:-1])}')
        sapi.create(supervisor.id, [a.id for a in agents[:-1]])
        try:
            # verify agents
            details = list(sapi.details(supervisor.id))
            self.assertEqual(set(a.id for a in agents[:-1]),
                             set(a.id for a in details),
                             'agent list mismatch after create')
            yield supervisor, agents
        finally:
            # delete supervisor again
            sapi.delete(supervisor.id)

    def test_assign_unassign(self):
        """
        Create supervisor with two agents and then assign and unassign one agent each
        """
        sapi = self.api.telephony.supervisors
        with self.assign_unassign() as (supervisor, agents):
            supervisor: AgentOrSupervisor
            agents: list[AgentOrSupervisor]

            # remove 1st agent and add 3rd agent
            print(f'Removing agent: {agents[0].display_name}, {base64.b64decode(agents[0].id + "==").decode()}')
            print(f'Adding agent: {agents[2].display_name}, {base64.b64decode(agents[2].id + "==").decode()}')
            sapi.assign_un_assign_agents(supervisor_id=supervisor.id,
                                         agents=[IdAndAction(id=agents[0].id,
                                                             action=PatternAction.delete),
                                                 IdAndAction(id=agents[2].id,
                                                             action=PatternAction.add)])

            # verify that the agent list is updated accordingly
            details = list(sapi.details(supervisor.id))
            print('Agents after update:')
            print('\n'.join(f'{a.display_name}, {base64.b64decode(a.id + "==").decode()}' for a in details))

            self.assertEqual(set(a.id for a in agents[1:]),
                             set(a.id for a in details),
                             'agent list mismatch after update')

    def test_assign_unassign_duplicate(self):
        """
        Try to assign already assigned agent --> DUPLICATE
        """
        sapi = self.api.telephony.supervisors
        with self.assign_unassign() as (supervisor, agents):
            supervisor: AgentOrSupervisor
            agents: list[AgentOrSupervisor]

            # try to add 1st agent ... again
            r = sapi.assign_un_assign_agents(supervisor_id=supervisor.id,
                                             agents=[IdAndAction(id=agents[0].id,
                                                                 action=PatternAction.add)])
            self.assertIsNotNone(r)
            self.assertEqual(1, len(r))
            status = r[0]
            self.assertEqual(agents[0].id, status.id)
            self.assertEqual('DUPLICATE', status.status)
