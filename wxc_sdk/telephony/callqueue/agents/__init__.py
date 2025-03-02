from collections.abc import Generator
from typing import Optional, List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common import IdAndName

__all__ = ['CallQueueAgent', 'CallQueueAgentQueue', 'CallQueueAgentDetail', 'AgentCallQueueSetting',
           'CallQueueAgentsApi']


class CallQueueAgent(ApiModel):
    #: Unique call queue agent identifier.
    id: Optional[str] = None
    #: First name for the call queue agent.
    first_name: Optional[str] = None
    #: Last name for the call queue agent.
    last_name: Optional[str] = None
    #: Primary phone number of the call queue agent.
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue agent.
    extension: Optional[str] = None
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a agent.
    esn: Optional[str] = None
    #: Denotes the queue count for call queue agent.
    queue_count: Optional[int] = None
    #: Denotes the location count for call queue agent.
    location_count: Optional[int] = None
    #: Denotes the join count for call queue agent.
    join_count: Optional[int] = None
    #: Denotes unjoin count for call queue agent.
    unjoin_count: Optional[int] = None
    #: Specifies the location information.
    location: Optional[IdAndName] = None
    #: Specifies the type of the call queue agent.
    type: Optional[str] = None


class CallQueueAgentQueue(ApiModel):
    #: Unique identifier of the call queue.
    id: Optional[str] = None
    #: Unique name for the call queue.
    name: Optional[str] = None
    #: Primary phone number of the call queue.
    phone_number: Optional[str] = None
    #: Specifies the routing prefix for the call queue.
    routing_prefix: Optional[str] = None
    #: The location identifier of the call queue.
    location_id: Optional[str] = None
    #: The location name where the call queue resides.
    location_name: Optional[str] = None
    #: Whether or not the call queue is enabled.
    join_enabled: Optional[bool] = None


class CallQueueAgentDetail(ApiModel):
    agent: Optional[CallQueueAgent] = None
    queues: Optional[list[CallQueueAgentQueue]] = None


class AgentCallQueueSetting(ApiModel):
    #: Unique call queue identifier.
    queue_id: Optional[str] = None
    #: Whether or not the call queue is enabled.
    join_enabled: Optional[bool] = None


class CallQueueAgentsApi(ApiChild, base='telephony/config/queues/agents'):
    """
    Call Queue Agents API
    """

    def list(self, location_id: str = None, queue_id: str = None, name: str = None,
             phone_number: str = None, join_enabled: bool = None,
             has_cx_essentials: bool = None, order: str = None, org_id: str = None,
             **params) -> Generator[CallQueueAgent, None, None]:
        """
        Read the List of Call Queue Agents

        List all Call Queues Agents for the organization.

        Agents can be users, workplace or virtual lines assigned to a call queue. Calls from the call queue are routed
        to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **Note**: The decoded value of the agent's `id`, and the `type` returned in the response, are always returned
        as `PEOPLE`, even when the agent is a workspace or virtual line. This will be addressed in a future release.

        :param location_id: Return only the call queue agents in this location.
        :type location_id: str
        :param queue_id: Only return call queue agents with the matching queue ID.
        :type queue_id: str
        :param name: Returns only the list of call queue agents that match the given name.
        :type name: str
        :param phone_number: Returns only the list of call queue agents that match the given phone number or extension.
        :type phone_number: str
        :param join_enabled: Returns only the list of call queue agents that match the given `joinEnabled` value.
        :type join_enabled: bool
        :param has_cx_essentials: Returns only the list of call queues with Customer Experience Essentials license when
            `true`, otherwise returns the list of Customer Experience Basic call queues.
        :type has_cx_essentials: bool
        :param order: Sort results alphabetically by call queue agent's name, in ascending or descending order.
        :type order: str
        :param org_id: List call queues agents in this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallQueueAgentObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if queue_id is not None:
            params['queueId'] = queue_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if join_enabled is not None:
            params['joinEnabled'] = str(join_enabled).lower()
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        if order is not None:
            params['order'] = order
        url = self.ep()
        return self.session.follow_pagination(url=url, model=CallQueueAgent, item_key='agents', params=params)

    def details(self, id: str, has_cx_essentials: bool = None,
                org_id: str = None) -> CallQueueAgentDetail:
        """
        Get Details for a Call Queue Agent

        Retrieve details of a particular Call queue agent based on the agent ID.

        Agents can be users, workplace or virtual lines assigned to a call queue. Calls from the call queue are routed
        to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving a call queue agent's details require a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **Note**: The agent's `type` returned in the response and in the decoded value of the agent's `id`, is always
        of type `PEOPLE`, even if the agent is a workspace or virtual line. This` will be corrected in a future
        release.

        :param id: Retrieve call queue agents with this identifier.
        :type id: str
        :param has_cx_essentials: Must be set to `true` to view the details of an agent with Customer Experience
            Essentials license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Retrieve call queue agents from this organization.
        :type org_id: str
        :rtype: :class:`CallQueueAgent`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'{id}')
        data = super().get(url, params=params)
        r = CallQueueAgent.model_validate(data)
        return r

    def update_call_queue_settings(self, id: str, settings: List[AgentCallQueueSetting],
                                   has_cx_essentials: bool = None, org_id: str = None):
        """
        Update an Agent's Settings of One or More Call Queues

        Modify an agent's call queue settings for an organization.

        Calls from the call queue are routed to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        This operation requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param id: Identifier of the agent to be updated.
        :type id: str
        :type settings: list[ModifyAgentsForCallQueueObjectSettings]
        :param has_cx_essentials: Must be set to `true` to modify an agent that has Customer Experience Essentials
            license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Update the settings of an agent in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body = dict()
        body['settings'] = TypeAdapter(list[AgentCallQueueSetting]).dump_python(settings, mode='json',
                                                                                by_alias=True,
                                                                                exclude_none=True)
        url = self.ep(f'{id}/settings')
        super().put(url, params=params, json=body)
