from collections.abc import Generator
from typing import Optional, List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common import PatternAction, UserType

__all__ = ['SupervisorApi', 'IdAndAction',
           'SupervisorAgentStatus',
           'AgentOrSupervisor']


class AgentOrSupervisor(ApiModel):
    #: A unique identifier for the supervisor.
    id: Optional[str] = None
    #: First name of the supervisor.
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    esn: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[UserType] = None
    #: Denotes if the agent or supervisor has Customer Experience Essentials license.
    has_cx_essentials: Optional[bool] = None
    #: Number of agents managed by supervisor. A supervisor must manage at least one agent.
    agent_count: Optional[int] = None


class SupervisorAgentStatus(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: status of the agent.
    status: Optional[str] = None
    #: Detailed message for the status.
    message: Optional[str] = None
    #: TODO: undocumented, issue 202
    type: Optional[UserType] = None


class IdAndAction(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str]
    #: Enumeration that indicates whether an agent needs to be added (`ADD`) or deleted (`DELETE`) from a supervisor.
    action: PatternAction


class SupervisorApi(ApiChild, base='telephony/config/supervisors'):
    """
    Supervisors

    Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

    Viewing these read-only device settings requires a full, device or
    read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

    Modifying these device settings requires a full or device
    administrator auth token with a scope of `spark-admin:telephony_config_write`.
    """

    def list(self, name: str = None, phone_number: str = None, order: str = None,
             has_cx_essentials: bool = None, org_id: str = None,
             **params) -> Generator[AgentOrSupervisor, None, None]:
        """
        Get List of Supervisors

        Get list of supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full, location, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return the supervisors that match the given name.
        :type name: str
        :param phone_number: Only return the supervisors that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of supervisors with Customer Experience Essentials license,
            when `true`. Otherwise returns the list of supervisors with Customer Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: List the supervisors in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AgentOrSupervisor` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=AgentOrSupervisor, item_key='supervisors',
                                              params=params)

    def create(self, id: str, agents: List[str],
               has_cx_essentials: bool = None,
               org_id: str = None):
        """
        Create a Supervisor

        Create a new supervisor. The supervisor must be created with at least one agent.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param id: A unique identifier for the supervisor.
        :type id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[str]
        :param has_cx_essentials: Creates a Customer Experience Essentials queue supervisor, when `true`. Customer
            Experience Essentials queue supervisors must have a Customer Experience Essentials license.
        :type has_cx_essentials: bool
        :param org_id: The organization ID where the supervisor needs to be created.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body = dict()
        body['id'] = id
        body['agents'] = [{'id': agent_id} for agent_id in agents]
        url = self.ep()
        super().post(url, params=params, json=body)

    def delete(self, supervisor_id: str, org_id: str = None):
        """
        Delete A Supervisor

        Deletes the supervisor from an organization.

        Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Delete the specified supervisor.
        :type supervisor_id: str
        :param org_id: Delete the supervisor in the specified organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(supervisor_id)
        super().delete(url, params=params)

    def delete_bulk(self, supervisors_ids: List[str], delete_all: bool = None, org_id: str = None):
        """
        Delete Bulk supervisors

        Deletes supervisors in bulk from an organization.

        Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisors_ids: Array of supervisors IDs to be deleted.
        :type supervisors_ids: list[str]
        :param delete_all: If present the `supervisorIds` array is ignored, and all supervisors in the context are
            deleted. **WARNING**: This will remove all supervisors from the organization.
        :type delete_all: bool
        :param org_id: Delete supervisors in bulk for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['supervisorsIds'] = supervisors_ids
        if delete_all is not None:
            body['deleteAll'] = delete_all
        url = self.ep()
        super().delete(url, params=params, json=body)

    def available_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                              has_cx_essentials: bool = None, org_id: str = None,
                              **params) -> Generator[AgentOrSupervisor, None, None]:
        """
        List Available Supervisors

        Get list of available supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return the supervisors that match the given name.
        :type name: str
        :param phone_number: Only return the supervisors that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of available supervisors with Customer Experience Essentials
            license, when `true`. When ommited or set to 'false', will return the list of available supervisors with
            Customer Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: List the available supervisors in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AgentOrSupervisor` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('availableSupervisors')
        return self.session.follow_pagination(url=url, model=AgentOrSupervisor, item_key='supervisors',
                                              params=params)

    def details(self, supervisor_id: str, name: str = None,
                phone_number: str = None, order: str = None, has_cx_essentials: bool = None,
                org_id: str = None, **additional_params) -> Generator[AgentOrSupervisor, None, None]:
        """
        GET Supervisor Details

        Get details of a specific supervisor, which includes the agents associated agents with the supervisor, in an
        organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param supervisor_id: List the agents assigned to this supervisor.
        :type supervisor_id: str
        :param name: Only return the agents that match the given name.
        :type name: str
        :param phone_number: Only return agents that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Must be set to `true`, to view the details of a supervisor with Customer Experience
            Essentials license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: List the agents assigned to a supervisor in this organization.
        :type org_id: str
        :return: Generator yieldig :class:`AgentOtSupervisor` instances
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        params.update(additional_params)
        url = self.ep(supervisor_id)
        return self.session.follow_pagination(url=url, model=AgentOrSupervisor, params=params, item_key='agents')

    def assign_unassign_agents(self, supervisor_id: str, agents: List[IdAndAction],
                               has_cx_essentials: bool = None,
                               org_id: str = None) -> Optional[List[SupervisorAgentStatus]]:
        """
        Assign or Unassign Agents to Supervisor

        Assign or unassign agents to the supervisor for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Identifier of the supervisor to be updated.
        :type supervisor_id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PutPersonPlaceVirtualLineAgentObject]
        :param has_cx_essentials: Must be set to `true` to modify a supervisor with Customer Experience Essentials
            license. This can otherwise be omitted or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Assign or unassign agents to a supervisor in this organization.
        :type org_id: str
        :rtype: list[SupervisorAgentStatus]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body = dict()
        body['agents'] = TypeAdapter(list[IdAndAction]).dump_python(agents, mode='json', by_alias=True)
        url = self.ep(supervisor_id)
        data = super().put(url, params=params, json=body)
        if not data:
            return None
        r = TypeAdapter(List[SupervisorAgentStatus]).validate_python(data['supervisorAgentStatus'])
        return r

    def available_agents(self, name: str = None, phone_number: str = None, order: str = None,
                         has_cx_essentials: bool = None, org_id: str = None,
                         **params) -> Generator[AgentOrSupervisor, None, None]:
        """
        List Available Agents

        Get list of available agents for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Returns only the agents that match the given name.
        :type name: str
        :param phone_number: Returns only the agents that match the phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of available agents with Customer Experience Essentials
            license, when `true`. When ommited or set to `false`, will return the list of available agents with
            Customer Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: List of available agents in a supervisor's list for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AgentOrSupervisor` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('availableAgents')
        return self.session.follow_pagination(url=url, model=AgentOrSupervisor, item_key='agents',
                                              params=params)
