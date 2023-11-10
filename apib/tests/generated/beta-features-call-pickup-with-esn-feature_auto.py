from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetAvailableAgentsFromCallPickupsResponse', 'GetCallPickupObject',
            'GetPersonPlaceVirtualLineCallPickupObject', 'GetPersonPlaceVirtualLineCallPickupObjectType',
            'GetUserNumberItemObject']


class GetPersonPlaceVirtualLineCallPickupObjectType(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person or workspace.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 8080
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Flag to indicate a primary phone.
    #: example: True
    primary: Optional[bool] = None


class GetPersonPlaceVirtualLineCallPickupObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    #: example: Brown
    last_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    #: example: johnBrown
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPersonPlaceVirtualLineCallPickupObjectType] = None
    #: Email of a person, workspace or virtual line.
    #: example: john.brown@example.com
    email: Optional[str] = None
    #: List of phone numbers of a person, workspace or virtual line.
    phone_number: Optional[list[GetUserNumberItemObject]] = None


class GetCallPickupObject(ApiModel):
    #: A unique identifier for the call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: Unique name for the call pickup. The maximum length is 80.
    #: example: North Alaska-Group
    name: Optional[str] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]] = None


class GetAvailableAgentsFromCallPickupsResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]] = None


class BetaFeaturesCallPickupWithESNFeatureApi(ApiChild, base='telephony/config/locations/{locationId}/callPickups'):
    """
    Beta Features:  Call Pickup with ESN Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Call Pickup supports reading and writing of Webex Calling Call Pickup settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_details_for_a_call_pickup(self, location_id: str, call_pickup_id: str,
                                      org_id: str = None) -> GetCallPickupObject:
        """
        Get Details for a Call Pickup

        Retrieve Call Pickup details.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Retrieving call pickup details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param call_pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallPickupObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{call_pickup_id}')
        data = super().get(url, params=params)
        r = GetCallPickupObject.model_validate(data)
        return r

    def get_available_agents_from_call_pickups(self, location_id: str, call_pickup_name: str = None, start: int = None,
                                               name: str = None, phone_number: str = None, order: str = None,
                                               org_id: str = None,
                                               **params) -> Generator[GetPersonPlaceVirtualLineCallPickupObject, None, None]:
        """
        Get available agents from Call Pickups

        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param start: Start at the zero-based offset in the list of matching available agents.
        :type start: int
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: `fname`, `lname`, `extension`,
            `number`.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: Generator yielding :class:`GetPersonPlaceVirtualLineCallPickupObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if call_pickup_name is not None:
            params['callPickupName'] = call_pickup_name
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'availableUsers')
        return self.session.follow_pagination(url=url, model=GetPersonPlaceVirtualLineCallPickupObject, item_key='agents', params=params)
