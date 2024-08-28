from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallParkSettingsObject', 'CallParkSettingsObjectRingPattern', 'FeaturesCallParkApi',
           'GetAvailableRecallHuntGroupsObject', 'GetCallParkExtensionObject', 'GetCallParkObject',
           'GetCallParkSettingsObject', 'GetPersonPlaceVirtualLineCallParksObject',
           'GetPersonPlaceVirtualLineCallParksObjectType', 'GetRecallHuntGroupObject',
           'GetRecallHuntGroupObjectOption', 'GetUserNumberItemObject', 'ListCPCallParkExtensionObject',
           'ListCallParkExtensionObject', 'ListCallParkObject', 'PutRecallHuntGroupObject']


class CallParkSettingsObjectRingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class CallParkSettingsObject(ApiModel):
    #: Ring pattern for when this callpark is called.
    #: example: NORMAL
    ring_pattern: Optional[CallParkSettingsObjectRingPattern] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up within the
    #: set time, then the call will be recalled based on the Call Park Recall setting.
    #: example: 60
    recall_time: Optional[int] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call
    #: will revert back to the hunt group (after the person who parked the call is alerted).
    #: example: 60
    hunt_wait_time: Optional[int] = None


class GetAvailableRecallHuntGroupsObject(ApiModel):
    #: A unique identifier for the hunt group.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvZEdWamFHNXBZMkZzTFhOMWNIQnZjblF0TlRVMU9EWTNOVE13T1VCbmJXRnBiQzVqYjIwPQ
    id: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: Technical Support Group - 5558675309
    name: Optional[str] = None


class GetCallParkExtensionObject(ApiModel):
    #: The extension for the call park extension.
    #: example: 1415
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341415
    esn: Optional[str] = None
    #: Unique name for the call park extension.
    #: example: 14159265
    name: Optional[str] = None


class GetRecallHuntGroupObjectOption(str, Enum):
    #: Alert parking user only.
    alert_parking_user_only = 'ALERT_PARKING_USER_ONLY'
    #: Alert parking user first, then hunt group.
    alert_parking_user_first_then_hunt_group = 'ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP'
    #: Alert hunt group only.
    alert_hunt_group_only = 'ALERT_HUNT_GROUP_ONLY'


class GetRecallHuntGroupObject(ApiModel):
    #: Alternate user which is a hunt group ID for call park recall alternate destination.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvZEdWamFHNXBZMkZzTFhOMWNIQnZjblF0TlRVMU9EWTNOVE13T1VCbmJXRnBiQzVqYjIwPQ
    hunt_group_id: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: Technical Support Group - 5558675309
    hunt_group_name: Optional[str] = None
    #: Call park recall options.
    #: example: ALERT_PARKING_USER_ONLY
    option: Optional[GetRecallHuntGroupObjectOption] = None


class GetPersonPlaceVirtualLineCallParksObjectType(str, Enum):
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


class GetPersonPlaceVirtualLineCallParksObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
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
    type: Optional[GetPersonPlaceVirtualLineCallParksObjectType] = None
    #: Email of a person or workspace.
    #: example: john.brown@example.com
    email: Optional[str] = None
    #: List of phone numbers of a person, workspace or virtual line.
    numbers: Optional[list[GetUserNumberItemObject]] = None


class ListCPCallParkExtensionObject(ApiModel):
    #: Unique identifier for the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vMGYzZTkwNGItYzliNC00ODNmLWI4MWItZmI0ZjkyMWcxNDUzCg
    id: Optional[str] = None
    #: The extension for the call park.
    #: example: 1415
    extension: Optional[str] = None
    #: A unique name for the call park extension.
    #: example: 14159265
    name: Optional[str] = None


class GetCallParkObject(ApiModel):
    #: A unique identifier for the call park.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSSy9kR1ZqYUc1cFkyRnNJSE4xY0hCdmNuUWdMU0JwYm5OMWNtRnVZMlVnTFNCamRYTjBiMjFsY2lBeA==
    id: Optional[str] = None
    #: Unique name for the call park. The maximum length is 80.
    #: example: technical support - insurance - customer 1
    name: Optional[str] = None
    #: Recall options that are added to call park.
    recall: Optional[GetRecallHuntGroupObject] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallParksObject]] = None
    #: Whether or not the calls will be parked on agents as a destination.
    park_on_agents_enabled: Optional[bool] = None
    #: Array of call park extensions assigned to a call park.
    call_park_extensions: Optional[list[ListCPCallParkExtensionObject]] = None


class GetCallParkSettingsObject(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[GetRecallHuntGroupObject] = None
    #: Setting controlling call park behavior.
    call_park_settings: Optional[CallParkSettingsObject] = None


class ListCallParkExtensionObject(ApiModel):
    #: Unique identifier for the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vMGYzZTkwNGItYzliNC00ODNmLWI4MWItZmI0ZjkyMWcxNDUzCg
    id: Optional[str] = None
    #: The extension for the call park extension.
    #: example: 1415
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341415
    esn: Optional[str] = None
    #: A unique name for the call park extension.
    #: example: 14159265
    name: Optional[str] = None
    #: ID of location for call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    location_id: Optional[str] = None
    #: Name of location for call park extension.
    #: example: WXCSIVDKCPAPIC4S1
    location_name: Optional[str] = None


class ListCallParkObject(ApiModel):
    #: Unique name for the call park. The maximum length is 80.
    #: example: technical support - insurance - customer 1
    name: Optional[str] = None
    #: A unique identifier for the call park.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSSy9kR1ZqYUc1cFkyRnNJSE4xY0hCdmNuUWdMU0JwYm5OMWNtRnVZMlVnTFNCamRYTjBiMjFsY2lBeA==
    id: Optional[str] = None
    #: Name of the location for the call park.
    #: example: Alaska
    location_name: Optional[str] = None
    #: ID of the location for the call park.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class PutRecallHuntGroupObject(ApiModel):
    #: Alternate user which is a hunt group ID for call park recall alternate destination.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvZEdWamFHNXBZMkZzTFhOMWNIQnZjblF0TlRVMU9EWTNOVE13T1VCbmJXRnBiQzVqYjIwPQ
    hunt_group_id: Optional[str] = None
    #: Call park recall options.
    #: example: ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP
    option: Optional[GetRecallHuntGroupObjectOption] = None


class FeaturesCallParkApi(ApiChild, base='telephony/config'):
    """
    Features:  Call Park
    
    Features: Call Park supports reading and writing of Webex Calling Call Park settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_call_parks(self, location_id: str, order: str = None, name: str = None, org_id: str = None,
                                    **params) -> Generator[ListCallParkObject, None, None]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        **NOTE**: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallParkObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'locations/{location_id}/callParks')
        return self.session.follow_pagination(url=url, model=ListCallParkObject, item_key='callParks', params=params)

    def create_a_call_park(self, location_id: str, name: str, recall: PutRecallHuntGroupObject,
                           agents: list[str] = None, park_on_agents_enabled: bool = None,
                           call_park_extensions: list[str] = None, org_id: str = None) -> str:
        """
        Create a Call Park

        Create new Call Parks for the given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Creating a call park requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param name: Unique name for the call park. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to the call park.
        :type recall: PutRecallHuntGroupObject
        :param agents: Array of ID strings of people, workspaces and virtual lines that are added to the call park.
        :type agents: list[str]
        :param park_on_agents_enabled: Whether or not the calls will be parked on agents as a destination.
        :type park_on_agents_enabled: bool
        :param call_park_extensions: Array of ID strings of call park extensions assigned to a call park.
        :type call_park_extensions: list[str]
        :param org_id: Create the call park for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['recall'] = recall.model_dump(mode='json', by_alias=True, exclude_none=True)
        if agents is not None:
            body['agents'] = agents
        if park_on_agents_enabled is not None:
            body['parkOnAgentsEnabled'] = park_on_agents_enabled
        if call_park_extensions is not None:
            body['callParkExtensions'] = call_park_extensions
        url = self.ep(f'locations/{location_id}/callParks')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_call_park(self, location_id: str, call_park_id: str, org_id: str = None):
        """
        Delete a Call Park

        Delete the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Deleting a call park requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param call_park_id: Delete the call park with the matching ID.
        :type call_park_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        super().delete(url, params=params)

    def get_details_for_a_call_park(self, location_id: str, call_park_id: str,
                                    org_id: str = None) -> GetCallParkObject:
        """
        Get Details for a Call Park

        Retrieve Call Park details.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving call park details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        **NOTE**: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param call_park_id: Retrieve settings for a call park with the matching ID.
        :type call_park_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallParkObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().get(url, params=params)
        r = GetCallParkObject.model_validate(data)
        return r

    def update_a_call_park(self, location_id: str, call_park_id: str, name: str = None,
                           recall: PutRecallHuntGroupObject = None, agents: list[str] = None,
                           park_on_agents_enabled: bool = None, call_park_extensions: list[str] = None,
                           org_id: str = None) -> str:
        """
        Update a Call Park

        Update the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating a call park requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location in which this call park exists.
        :type location_id: str
        :param call_park_id: Update settings for a call park with the matching ID.
        :type call_park_id: str
        :param name: Unique name for the call park. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to call park.
        :type recall: PutRecallHuntGroupObject
        :param agents: Array of ID strings of people, workspaces and virtual lines that are added to call park. The new
            list of `agents` will replace any existing call park agents list.
        :type agents: list[str]
        :param park_on_agents_enabled: Whether or not the calls will be parked on agents as a destination.
        :type park_on_agents_enabled: bool
        :param call_park_extensions: Array of ID strings of call park extensions assigned to a call park.
        :type call_park_extensions: list[str]
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if recall is not None:
            body['recall'] = recall.model_dump(mode='json', by_alias=True, exclude_none=True)
        if agents is not None:
            body['agents'] = agents
        if park_on_agents_enabled is not None:
            body['parkOnAgentsEnabled'] = park_on_agents_enabled
        if call_park_extensions is not None:
            body['callParkExtensions'] = call_park_extensions
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def get_available_agents_from_call_parks(self, location_id: str, call_park_name: str = None, name: str = None,
                                             phone_number: str = None, order: str = None, org_id: str = None,
                                             **params) -> Generator[GetPersonPlaceVirtualLineCallParksObject, None, None]:
        """
        Get available agents from Call Parks

        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: Generator yielding :class:`GetPersonPlaceVirtualLineCallParksObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if call_park_name is not None:
            params['callParkName'] = call_park_name
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableUsers')
        return self.session.follow_pagination(url=url, model=GetPersonPlaceVirtualLineCallParksObject, item_key='agents', params=params)

    def get_available_recall_hunt_groups_from_call_parks(self, location_id: str, name: str = None, order: str = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[GetAvailableRecallHuntGroupsObject, None, None]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort fields:
            lname.
        :type order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: Generator yielding :class:`GetAvailableRecallHuntGroupsObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableRecallHuntGroups')
        return self.session.follow_pagination(url=url, model=GetAvailableRecallHuntGroupsObject, item_key='huntGroups', params=params)

    def get_call_park_settings(self, location_id: str, org_id: str = None) -> GetCallParkSettingsObject:
        """
        Get Call Park Settings

        Retrieve Call Park Settings from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving settings from call parks requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str
        :rtype: :class:`GetCallParkSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/settings')
        data = super().get(url, params=params)
        r = GetCallParkSettingsObject.model_validate(data)
        return r

    def update_call_park_settings(self, location_id: str, call_park_recall: PutRecallHuntGroupObject = None,
                                  call_park_settings: CallParkSettingsObject = None, org_id: str = None):
        """
        Update Call Park settings

        Update Call Park settings for the designated location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating call park settings requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param call_park_recall: Recall options that are added to call park.
        :type call_park_recall: PutRecallHuntGroupObject
        :param call_park_settings: Setting controlling call park behavior.
        :type call_park_settings: CallParkSettingsObject
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_park_recall is not None:
            body['callParkRecall'] = call_park_recall.model_dump(mode='json', by_alias=True, exclude_none=True)
        if call_park_settings is not None:
            body['callParkSettings'] = call_park_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/callParks/settings')
        super().put(url, params=params, json=body)

    def read_the_list_of_call_park_extensions(self, location_id: str = None, extension: str = None,
                                              location_name: str = None, name: str = None, order: str = None,
                                              org_id: str = None,
                                              **params) -> Generator[ListCallParkExtensionObject, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param location_name: Only return call park extensions with the matching extension.
        :type location_name: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param order: Order the available agents according to the designated fields.  Available sort fields:
            `groupName`, `callParkExtension`, `callParkExtensionName`, `callParkExtensionExternalId`.
        :type order: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallParkExtensionObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if extension is not None:
            params['extension'] = extension
        if location_name is not None:
            params['locationName'] = location_name
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('callParkExtensions')
        return self.session.follow_pagination(url=url, model=ListCallParkExtensionObject, item_key='callParkExtensions', params=params)

    def get_details_for_a_call_park_extension(self, location_id: str, call_park_extension_id: str,
                                              org_id: str = None) -> GetCallParkExtensionObject:
        """
        Get Details for a Call Park Extension

        Retrieve Call Park Extension details.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.

        Retrieving call park extension details requires a full or read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param call_park_extension_id: Retrieve details for a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Retrieve call park extension details from this organization.
        :type org_id: str
        :rtype: :class:`GetCallParkExtensionObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        data = super().get(url, params=params)
        r = GetCallParkExtensionObject.model_validate(data)
        return r

    def create_a_call_park_extension(self, location_id: str, name: str, extension: str, org_id: str = None) -> str:
        """
        Create a Call Park Extension

        Create new Call Park Extensions for the given location.

        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.

        Creating a call park extension requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Create the call park extension for this location.
        :type location_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 10.
        :type extension: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['extension'] = extension
        url = self.ep(f'locations/{location_id}/callParkExtensions')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_call_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None):
        """
        Delete a Call Park Extension

        Delete the designated Call Park Extension.

        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.

        Deleting a call park extension requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a call park extension.
        :type location_id: str
        :param call_park_extension_id: Delete the call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Delete the call park extension from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().delete(url, params=params)

    def update_a_call_park_extension(self, location_id: str, call_park_extension_id: str, name: str = None,
                                     extension: str = None, org_id: str = None):
        """
        Update a Call Park Extension

        Update the designated Call Park Extension.

        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.

        Updating a call park extension requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call park extension exists.
        :type location_id: str
        :param call_park_extension_id: Update a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 10.
        :type extension: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().put(url, params=params, json=body)
