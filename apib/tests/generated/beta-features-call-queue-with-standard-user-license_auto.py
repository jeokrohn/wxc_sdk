from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AvailableAgentObject', 'AvailableAgentObjectType', 'BetaFeaturesCallQueueWithStandardUserLicenseApi',
           'GetUserNumberItemObject']


class AvailableAgentObjectType(str, Enum):
    #: Object is a user.
    people = 'PEOPLE'
    #: Object is a place.
    place = 'PLACE'
    #: Object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person or workspace.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 8080
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Phone number is Primary or Alternative Number.
    #: example: True
    primary: Optional[bool] = None


class AvailableAgentObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    #: example: Brown
    last_name: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    #: example: johnBrown
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[AvailableAgentObjectType] = None
    #: Email of a person, workspace or virtual line.
    #: example: john.brown@example.com
    email: Optional[str] = None
    #: Person has the CX Essentials license.
    #: example: True
    has_cx_essentials: Optional[bool] = None
    #: List of phone numbers of a person, workspace or virtual line.
    phone_number: Optional[list[GetUserNumberItemObject]] = None


class BetaFeaturesCallQueueWithStandardUserLicenseApi(ApiChild, base='telephony/config/queues/agents/availableAgents'):
    """
    Beta Features:  Call Queue with Standard User License
    
    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_call_queue_available_agents(self, location_id: str, name: str = None, phone_number: str = None,
                                        order: str = None, org_id: str = None,
                                        **params) -> Generator[AvailableAgentObject, None, None]:
        """
        Get Call Queue Available Agents

        List all available users, workspaces, or virtual lines that can be assigned as call queue agents.

        Available agents are users (excluding users with Webex Calling Standard license), workspaces, or virtual lines
        that can be assigned to a call queue.
        Calls from the call queue are routed to assigned agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID of the call queue. Temporary mandatory query parameter, used for
            performance reasons only and not a filter.
        :type location_id: str
        :param name: Search based on name (user first and last name combination).
        :type name: str
        :param phone_number: Search based on number or extension.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three comma-separated sort
            order fields may be specified. Available sort fields are: `userId`, `fname`, `firstname`, `lname`,
            `lastname`, `dn`, and `extension`. Sort order can be added together with each field using a hyphen, `-`.
            Available sort orders are: `asc`, and `desc`.
        :type order: str
        :param org_id: List available agents for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAgentObject` instances
        """
        params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep()
        return self.session.follow_pagination(url=url, model=AvailableAgentObject, item_key='agents', params=params)
