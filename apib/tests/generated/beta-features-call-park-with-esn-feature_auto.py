from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallParkWithESNFeatureApi', 'GetCallParkExtensionObject', 'GetCallParkObject',
           'GetPersonPlaceVirtualLineCallParksObject', 'GetPersonPlaceVirtualLineCallParksObjectType',
           'GetRecallHuntGroupObject', 'GetRecallHuntGroupObjectOption', 'GetUserNumberItemObject',
           'ListCPCallParkExtensionObject', 'ListCallParkExtensionObject']


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
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341415
    esn: Optional[str] = None
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


class BetaFeaturesCallParkWithESNFeatureApi(ApiChild, base='telephony/config'):
    """
    Beta Features:  Call Park with ESN Feature
    
    Features: Call Park supports reading and writing of Webex Calling Call Park settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_details_for_a_call_park(self, location_id: str, call_park_id: str,
                                    org_id: str = None) -> GetCallParkObject:
        """
        Get Details for a Call Park

        Retrieve Call Park details.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving call park details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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

    def get_available_agents_from_call_parks(self, location_id: str, call_park_name: str = None, name: str = None,
                                             phone_number: str = None, order: str = None, org_id: str = None,
                                             **params) -> Generator[GetPersonPlaceVirtualLineCallParksObject, None, None]:
        """
        Get available agents from Call Parks

        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

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

    def read_the_list_of_call_park_extensions(self, extension: str = None, name: str = None, location_id: str = None,
                                              location_name: str = None, order: str = None, org_id: str = None,
                                              **params) -> Generator[ListCallParkExtensionObject, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with the matching extension.
        :type location_name: str
        :param order: Order the available agents according to the designated fields.  Available sort fields:
            `groupName`, `callParkExtension`, `callParkExtensionName`, `callParkExtensionExternalId`.
        :type order: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallParkExtensionObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if extension is not None:
            params['extension'] = extension
        if name is not None:
            params['name'] = name
        if location_id is not None:
            params['locationId'] = location_id
        if location_name is not None:
            params['locationName'] = location_name
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

        Retrieving call park extension details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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
