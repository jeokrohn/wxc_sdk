from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['FeaturesCallPickupApi', 'GetCallPickupObject', 'GetCallPickupObjectNotificationType',
           'GetPersonPlaceVirtualLineCallPickupObject', 'GetPersonPlaceVirtualLineCallPickupObjectType',
           'GetUserNumberItemObject', 'ListCallPickupObject']


class GetCallPickupObjectNotificationType(str, Enum):
    #: Notification is not sent to any member of the call pickup group.
    none_ = 'NONE'
    #: When the `notificationDelayTimerSeconds` number of seconds has elapsed, play an audio notification for each call
    #: pickup group member.
    audio_only = 'AUDIO_ONLY'
    #: When the `notificationDelayTimerSeconds` number of seconds has elapsed, provide a visual notification to every
    #: call pickup group member.
    visual_only = 'VISUAL_ONLY'
    #: When the `notificationDelayTimerSeconds` number of seconds has elapsed, provide an audio and visual notification
    #: to every call pickup group member.
    audio_and_visual = 'AUDIO_AND_VISUAL'


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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
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
    #: Type of the notification when an incoming call is unanswered. The call pickup group notifies all of its members.
    #: Default: NONE.
    #: example: NONE
    notification_type: Optional[GetCallPickupObjectNotificationType] = None
    #: After the number of seconds given by the `notificationDelayTimerSeconds` has elapsed, notify every member of the
    #: call pickup group when an incoming call goes unanswered. The `notificationType` field specifies the
    #: notification method. Default: 6.
    #: example: 6
    notification_delay_timer_seconds: Optional[int] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]] = None


class ListCallPickupObject(ApiModel):
    #: Unique name for the call pickup. The maximum length is 80.
    #: example: North Alaska-Group
    name: Optional[str] = None
    #: A unique identifier for the call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: Name of the location for call pickup.
    #: example: Alaska
    location_name: Optional[str] = None
    #: ID of the location for call pickup.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class FeaturesCallPickupApi(ApiChild, base='telephony/config/locations'):
    """
    Features:  Call Pickup
    
    Features: Call Pickup supports reading and writing of Webex Calling Call Pickup settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_call_pickups(self, location_id: str, order: str = None, name: str = None, org_id: str = None,
                                      **params) -> Generator[ListCallPickupObject, None, None]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallPickupObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'{location_id}/callPickups')
        return self.session.follow_pagination(url=url, model=ListCallPickupObject, item_key='callPickups', params=params)

    def create_a_call_pickup(self, location_id: str, name: str,
                             notification_type: GetCallPickupObjectNotificationType = None,
                             notification_delay_timer_seconds: int = None, agents: list[str] = None,
                             org_id: str = None) -> str:
        """
        Create a Call Pickup

        Create new Call Pickups for the given location.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Creating a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param notification_type: Type of the notification when an incoming call is unanswered. The call pickup group
            notifies all of its members. Default: NONE.
        :type notification_type: GetCallPickupObjectNotificationType
        :param notification_delay_timer_seconds: After the number of seconds given by the
            `notificationDelayTimerSeconds` has elapsed, notify every member of the call pickup group when an incoming
            call goes unanswered. The `notificationType` field specifies the notification method. Default: 6.
        :type notification_delay_timer_seconds: int
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: list[str]
        :param org_id: Create the call pickup for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if notification_type is not None:
            body['notificationType'] = enum_str(notification_type)
        if notification_delay_timer_seconds is not None:
            body['notificationDelayTimerSeconds'] = notification_delay_timer_seconds
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'{location_id}/callPickups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_call_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None):
        """
        Delete a Call Pickup

        Delete the designated Call Pickup.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Deleting a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param call_pickup_id: Delete the call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/callPickups/{call_pickup_id}')
        super().delete(url, params=params)

    def get_details_for_a_call_pickup(self, location_id: str, call_pickup_id: str,
                                      org_id: str = None) -> GetCallPickupObject:
        """
        Get Details for a Call Pickup

        Retrieve the designated Call Pickup details.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Retrieving call pickup details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

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
        url = self.ep(f'{location_id}/callPickups/{call_pickup_id}')
        data = super().get(url, params=params)
        r = GetCallPickupObject.model_validate(data)
        return r

    def update_a_call_pickup(self, location_id: str, call_pickup_id: str, name: str = None,
                             notification_type: GetCallPickupObjectNotificationType = None,
                             notification_delay_timer_seconds: int = None, agents: list[str] = None,
                             org_id: str = None) -> str:
        """
        Update a Call Pickup

        Update the designated Call Pickup.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Updating a call pickup requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param call_pickup_id: Update settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param notification_type: Type of the notification when an incoming call is unanswered. The call pickup group
            notifies all of its members. Default: NONE.
        :type notification_type: GetCallPickupObjectNotificationType
        :param notification_delay_timer_seconds: After the number of seconds given by the
            `notificationDelayTimerSeconds` has elapsed, notify every member of the call pickup group when an incoming
            call goes unanswered. The `notificationType` field specifies the notification method. Default: 6.
        :type notification_delay_timer_seconds: int
        :param agents: An array of people, workspace, and virtual lines IDs, that are added to call pickup.
        :type agents: list[str]
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if notification_type is not None:
            body['notificationType'] = enum_str(notification_type)
        if notification_delay_timer_seconds is not None:
            body['notificationDelayTimerSeconds'] = notification_delay_timer_seconds
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'{location_id}/callPickups/{call_pickup_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def get_available_agents_from_call_pickups(self, location_id: str, call_pickup_name: str = None, name: str = None,
                                               phone_number: str = None, order: str = None, org_id: str = None,
                                               **params) -> Generator[GetPersonPlaceVirtualLineCallPickupObject, None, None]:
        """
        Get available agents from Call Pickups

        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
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
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'{location_id}/callPickups/availableUsers')
        return self.session.follow_pagination(url=url, model=GetPersonPlaceVirtualLineCallPickupObject, item_key='agents', params=params)
