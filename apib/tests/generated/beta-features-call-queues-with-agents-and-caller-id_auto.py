from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallQueuesWithAgentsAndCallerIDApi', 'GetCallQueueAgentObject', 'GetCallQueueAgentObjectAgent',
           'GetCallQueueAgentObjectQueues', 'ListCallQueueAgentObject', 'ListCallQueueAgentObjectLocation',
           'ModifyAgentsForCallQueueObjectSettings']


class ListCallQueueAgentObjectLocation(ApiModel):
    #: The location name where the call queue agent resides.
    #: example: Location2
    name: Optional[str] = None
    #: ID of location for call queue agent.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVmMDI3OGZlLWU4OGMtNDMzNy04MGViLWRjY2NiM2VlMDU1MA
    id: Optional[str] = None


class ListCallQueueAgentObject(ApiModel):
    #: Unique call queue agent identifier.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zYjY4Yjg2YS1hMTZiLTRmNzItOTlmZi01ZDlhZjgyZWNmNTE
    id: Optional[str] = None
    #: First name for the call queue agent.
    #: example: test_301_person_phone_extnsion
    first_name: Optional[str] = None
    #: Last name for the call queue agent.
    #: example: last_nam
    last_name: Optional[str] = None
    #: Primary phone number of the call queue agent.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue agent.
    #: example: 23234
    extension: Optional[str] = None
    #: Routing prefix of the call queue agent.
    #: example: 8002
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a agent.
    #: example: 23234
    esn: Optional[str] = None
    #: Denotes the queue count for call queue agent.
    #: example: 1
    queue_count: Optional[int] = None
    #: Denotes the location count for call queue agent.
    #: example: 1
    location_count: Optional[int] = None
    #: Denotes the join count for call queue agent.
    #: example: 1
    join_count: Optional[int] = None
    #: Denotes unjoin count for call queue agent.
    unjoin_count: Optional[int] = None
    #: Specifies the location information.
    location: Optional[ListCallQueueAgentObjectLocation] = None
    #: Specifies the type of the call queue agent.
    #: example: PEOPLE
    type: Optional[str] = None


class GetCallQueueAgentObjectAgent(ApiModel):
    #: A unique identifier for the call queue agent.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xZmNiMjczZS0wYzdmLTQ1ZGUtYmNlOC0yMWE3YzFlYjVjYmY
    id: Optional[str] = None
    #: First name for the call queue agent.
    #: example: Arthur
    first_name: Optional[str] = None
    #: last name for the call queue agent.
    #: example: Murray
    last_name: Optional[str] = None
    #: Primary phone number of the call queue agent.
    #: example: 19728881234
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue agent.
    #: example: 34543
    extension: Optional[str] = None
    #: Routing prefix + extension of a agent.
    #: example: 34543180
    esn: Optional[str] = None
    #: Specifies the location information.
    location: Optional[ListCallQueueAgentObjectLocation] = None
    #: Specifies the type of the call queue agent.
    #: example: PEOPLE
    type: Optional[str] = None


class GetCallQueueAgentObjectQueues(ApiModel):
    #: Unique identifier of the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvZjM4NDIxZGYtN2MxOC00NGI1LThlNmQtNDFmZTEyMTFlZDFk
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: YU7
    name: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: 12144184002
    phone_number: Optional[str] = None
    #: Specifies the routing prefix for the call queue.
    #: example: 34543
    routing_prefix: Optional[str] = None
    #: The location identifier of the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    location_id: Optional[str] = None
    #: The location name where the call queue resides.
    #: example: RCDN
    location_name: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    join_enabled: Optional[bool] = None


class GetCallQueueAgentObject(ApiModel):
    agent: Optional[GetCallQueueAgentObjectAgent] = None
    queues: Optional[list[GetCallQueueAgentObjectQueues]] = None


class ModifyAgentsForCallQueueObjectSettings(ApiModel):
    #: Unique call queue identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvZjM4NDIxZGYtN2MxOC00NGI1LThlNmQtNDFmZTEyMTFlZDFk
    queue_id: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    join_enabled: Optional[bool] = None


class BetaFeaturesCallQueuesWithAgentsAndCallerIDApi(ApiChild, base='telephony/config/queues/agents'):
    """
    Beta Features: Call Queues with Agents and Caller ID
    
    Webex Customer Experience Basic is an offering available as part of the Webex Suite or Webex Calling Professional
    license at no additional cost.
    It includes a simple and powerful set of features which are bundled together to deliver the call center
    functionalities.
    The features such as Voice Queues, skill-based routing, call queue monitoring and analytics, multi call window, and
    more, help users to engage with customers efficiently.
    Also, with our Webex Calling for Microsoft Teams integration, the Microsoft Teams users can access the features
    directly from Teams.
    
    Webex Customer Experience Essentials provides the fundamental capabilities of the Webex Contact Center solution.
    It includes all the Webex Calling professional capabilities, Customer Experience Basic features, and some
    additional key features accessible through the Webex App for both agents and supervisors.
    The features like screen pop, supervisor experience in Webex App, and real-time and historical agent and queue view
    make the Customer Experience Essentials distinct from Customer Experience Basic.
    
    `Learn more about the customer Experience Basic suite
    <https://help.webex.com/en-us/article/nzkg083/Webex-Customer-Experience-Basic>`_
    `Learn more about the customer Experience Essentials suite
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_
    
    Viewing the read-only customer Experience Basic and Essentials APIs requires a full, device or read-only
    administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying the customer Experience Basic and Essentials APIs requires a full or device administrator auth token with
    a scope of
    `spark-admin:telephony_config_write`.
    """

    def read_the_list_of_call_queue_agents(self, location_id: str = None, queue_id: str = None, name: str = None,
                                           phone_number: str = None, join_enabled: bool = None,
                                           has_cx_essentials: bool = None, order: str = None, org_id: str = None,
                                           **params) -> Generator[ListCallQueueAgentObject, None, None]:
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
        return self.session.follow_pagination(url=url, model=ListCallQueueAgentObject, item_key='agents', params=params)

    def get_details_for_a_call_queue_agent(self, id: str, has_cx_essentials: bool = None,
                                           org_id: str = None) -> GetCallQueueAgentObject:
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
        :rtype: :class:`GetCallQueueAgentObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'{id}')
        data = super().get(url, params=params)
        r = GetCallQueueAgentObject.model_validate(data)
        return r

    def update_an_agent_s_settings_of_one_or_more_call_queues(self, id: str,
                                                              settings: list[ModifyAgentsForCallQueueObjectSettings],
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
        body['settings'] = TypeAdapter(list[ModifyAgentsForCallQueueObjectSettings]).dump_python(settings, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{id}/settings')
        super().put(url, params=params, json=body)
