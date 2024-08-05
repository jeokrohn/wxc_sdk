from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AgentAction', 'AvailableAgentListObject', 'AvailableSupervisorsListObject',
           'BetaFeaturesCallQueueWithSupervisorsApi', 'GetSupervisorDetailsResponse', 'ListSupervisorAgentObject',
           'ListSupervisorAgentStatusObject', 'ListSupervisorObject', 'PostPersonPlaceVirtualLineSupervisorObject',
           'PutPersonPlaceVirtualLineAgentObject', 'UserType']


class ListSupervisorObject(ApiModel):
    #: A unique identifier for the supervisor.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81OGVkZTIwNi0yNTM5LTQ1ZjQtODg4Ny05M2E3ZWIwZWI3ZDI
    id: Optional[str] = None
    #: First name of the supervisor.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    #: example: Smith
    last_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    #: example: +19845550186
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    #: example: 12554
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 3412554
    esn: Optional[str] = None
    #: Number of agents managed by supervisor. A supervisor must manage at least one agent.
    #: example: 2
    agent_count: Optional[str] = None


class PostPersonPlaceVirtualLineSupervisorObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzE3NzczMWRiLWE1YzEtNGI2MC05ZTMwLTNhM2MxMGFiM2IxMQ
    id: Optional[str] = None


class AvailableSupervisorsListObject(ApiModel):
    #: A unique identifier for the supervisor.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YzVlODRhMS0wZmEwLTQzNDAtODVkZC1mMzM1ZGQ4MTkxMmI
    id: Optional[str] = None
    #: First name of the supervisor.
    #: example: Adam
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    #: example: Sandler
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the supervisor.
    #: example: Adam Sandler
    display_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    #: example: +19845550200
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34543
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 345430020
    esn: Optional[str] = None


class ListSupervisorAgentObject(ApiModel):
    #: ID of person, workspace or virtual line. **WARNING**: The `id` returned is always of type `PEOPLE` even if the
    #: agent is a workspace or virtual line. The `type` of the agent `id` can be found by using GET available agents
    #: api with agent name as a query param. The `type` of the agent `id` will be corrected in a future release.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85NTA4OTc4ZC05YmFkLTRmYWEtYTljNC0wOWQ4NWQ4ZmRjZTY
    id: Optional[str] = None
    #: Last name of the agent.
    #: example: user
    last_name: Optional[str] = None
    #: First name of the agent.
    #: example: test
    first_name: Optional[str] = None
    #: Primary phone extension of the agent.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix + extension of a agent.
    #: example: 20
    esn: Optional[str] = None
    #: Primary phone number of the agent.
    #: example: +1972998998
    phone_number: Optional[str] = None


class AgentAction(str, Enum):
    #: Assign an agent to a supervisor.
    add = 'ADD'
    #: Remove an agent from a supervisor.
    delete = 'DELETE'


class PutPersonPlaceVirtualLineAgentObject(ApiModel):
    #: ID of person, workspace or virtual line. **WARNING**: The `id` returned is always of type `PEOPLE` even if the
    #: agent is a workspace or virtual line. The `type` of the agent `id` will be corrected in a future release.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81OGVkZTIwNi0yNTM5LTQ1ZjQtODg4Ny05M2E3ZWIwZWI3ZDI
    id: Optional[str] = None
    #: Enumeration that indicates whether an agent needs to be added (`ADD`) or deleted (`DELETE`) from a supervisor.
    action: Optional[AgentAction] = None


class ListSupervisorAgentStatusObject(ApiModel):
    #: ID of person, workspace or virtual line. **WARNING**: The `id` returned is in UUID format, since we don't have
    #: agentType from OCI response. This will be converting to Hydra type in future release.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85NTA4OTc4ZC05YmFkLTRmYWEtYTljNC0wOWQ4NWQ4ZmRjZTY
    id: Optional[str] = None
    #: status of the agent.
    #: example: DUPLICATE
    status: Optional[str] = None
    #: Detailed message for the status.
    #: example: [Error 6612] Agent 9508978d-9bad-4faa-a9c4-09d85d8fdce6 is already assigned to the supervisor.
    message: Optional[str] = None


class UserType(str, Enum):
    #: Associated type is a person.
    people = 'PEOPLE'
    #: Associated type is a workspace.
    place = 'PLACE'
    #: Associated type is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class AvailableAgentListObject(ApiModel):
    #: A unique identifier for the agent. **WARNING**: The `id` returned is always of type `PEOPLE` even if the agent
    #: is a workspace or virtual line. The `type` of the agent `id` will be corrected in a future release.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YzVlODRhMS0wZmEwLTQzNDAtODVkZC1mMzM1ZGQ4MTkxMmI
    id: Optional[str] = None
    #: First name of the agent.
    #: example: Adam
    first_name: Optional[str] = None
    #: Last name of the agent.
    #: example: Sandler
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the agent.
    #: example: Adam Sandler
    display_name: Optional[str] = None
    #: Primary phone number of the agent.
    #: example: +19845550200
    phone_number: Optional[str] = None
    #: Primary phone extension of the agent.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34543
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 345430020
    esn: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[UserType] = None


class GetSupervisorDetailsResponse(ApiModel):
    #: unique identifier of the supervisor
    id: Optional[str] = None
    #: Array of agents assigned to a specific supervisor.
    agents: Optional[list[ListSupervisorAgentObject]] = None


class BetaFeaturesCallQueueWithSupervisorsApi(ApiChild, base='telephony/config/supervisors'):
    """
    Beta Features: Call Queue with Supervisors
    
    Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.
    
    Viewing these read-only device settings requires a full, device or
    read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def get_list_of_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                org_id: str = None, **params) -> Generator[ListSupervisorObject, None, None]:
        """
        Get List of Supervisors

        Get list of supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full, location, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return supervisors with the matching name.
        :type name: str
        :param phone_number: Only return supervisors with matching primary phone number.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param org_id: List the supervisors for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListSupervisorObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListSupervisorObject, item_key='supervisors', params=params)

    def create_a_supervisor(self, id: str, agents: list[PostPersonPlaceVirtualLineSupervisorObject],
                            org_id: str = None) -> list[ListSupervisorAgentStatusObject]:
        """
        Create a Supervisor

        Create a new supervisor. The supervisor must be created with atleast one agent.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full or location administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param id: A unique identifier for the supervisor.
        :type id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineSupervisorObject]
        :param org_id: Create supervisor for this organization.
        :type org_id: str
        :rtype: list[ListSupervisorAgentStatusObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['id'] = id
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineSupervisorObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[ListSupervisorAgentStatusObject]).validate_python(data['supervisorAgentStatus'])
        return r

    def delete_a_supervisor(self, supervisor_id: str, org_id: str = None):
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
        url = self.ep(f'{supervisor_id}')
        super().delete(url, params=params)

    def delete_bulk_supervisors(self, supervisor_ids: list[str], delete_all: bool = None, org_id: str = None):
        """
        Delete Bulk supervisors

        Deletes supervisors in bulk from an organization.

        Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_ids: Array of supervisors IDs to be deleted.
        :type supervisor_ids: list[str]
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
        body['supervisorIds'] = supervisor_ids
        if delete_all is not None:
            body['deleteAll'] = delete_all
        url = self.ep()
        super().delete(url, params=params, json=body)

    def list_available_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                   org_id: str = None,
                                   **params) -> Generator[AvailableSupervisorsListObject, None, None]:
        """
        List Available Supervisors

        Get list of available supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return supervisors with the matching name.
        :type name: str
        :param phone_number: Only return supervisors with matching primary phone number.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param org_id: List available supervisors of this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableSupervisorsListObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep('availableSupervisors')
        return self.session.follow_pagination(url=url, model=AvailableSupervisorsListObject, item_key='supervisors', params=params)

    def get_supervisor_details(self, supervisor_id: str, max_: int = None, start: int = None, name: str = None,
                               phone_number: str = None, order: str = None,
                               org_id: str = None) -> GetSupervisorDetailsResponse:
        """
        GET Supervisor Details

        Get details of a specific supervisor as well as the associated agents for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling. The agent `id` returned is always of type
        `PEOPLE` even if the agent is a workspace or virtual line. The `type` of the agent `id` can be found by using
        GET available agents api with agent name as a query param. The `type` of the agent `id` will be corrected in a
        future release.

        Requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param supervisor_id: List the agents assigned to specific supervisor.
        :type supervisor_id: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return agents with the matching name.
        :type name: str
        :param phone_number: Only return agents with matching primary phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param org_id: List the agents assigned to specific supervisor for this organization.
        :type org_id: str
        :rtype: :class:`GetSupervisorDetailsResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'{supervisor_id}')
        data = super().get(url, params=params)
        r = GetSupervisorDetailsResponse.model_validate(data)
        return r

    def assign_or_unassign_agents_to_supervisor(self, supervisor_id: str,
                                                agents: list[PutPersonPlaceVirtualLineAgentObject],
                                                org_id: str = None) -> list[ListSupervisorAgentStatusObject]:
        """
        Assign or Unassign Agents to Supervisor

        Assign or unassign agents to the supervisor for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Identifier of the superviser to be updated.
        :type supervisor_id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls. **WARNING**: The `id`
            returned is in UUID format, since we don't have agentType from OCI response. This will be converting to
            Hydra type in future release.
        :type agents: list[PutPersonPlaceVirtualLineAgentObject]
        :param org_id: Assign or unassign agents to a supervisor for this organization.
        :type org_id: str
        :rtype: list[ListSupervisorAgentStatusObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['agents'] = TypeAdapter(list[PutPersonPlaceVirtualLineAgentObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{supervisor_id}')
        data = super().put(url, params=params, json=body)
        r = TypeAdapter(list[ListSupervisorAgentStatusObject]).validate_python(data['supervisorAgentStatus'])
        return r

    def list_available_agents(self, name: str = None, phone_number: str = None, order: str = None, org_id: str = None,
                              **params) -> Generator[AvailableAgentListObject, None, None]:
        """
        List Available Agents

        Get list of available agents for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return agents with the matching name.
        :type name: str
        :param phone_number: Only return agents with matching primary phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param org_id: List of agents in a supervisor's list for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAgentListObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep('availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgentListObject, item_key='agents', params=params)
