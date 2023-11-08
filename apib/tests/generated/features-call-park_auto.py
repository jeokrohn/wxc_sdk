from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallParkSettingsObject', 'CallParkSettingsObjectRingPattern', 'CreateACallParkResponse',
            'GetAvailableAgentsFromCallParksResponse', 'GetAvailableRecallHuntGroupsFromCallParksResponse',
            'GetAvailableRecallHuntGroupsObject', 'GetCallParkExtensionObject', 'GetCallParkObject',
            'GetCallParkSettingsObject', 'GetPersonPlaceVirtualLineCallParksObject',
            'GetPersonPlaceVirtualLineCallParksObjectType', 'GetRecallHuntGroupObject',
            'GetRecallHuntGroupObjectOption', 'GetUserNumberItemObject', 'ListCPCallParkExtensionObject',
            'ListCallParkExtensionObject', 'ListCallParkObject', 'ModifyCallExtensionParkObject',
            'ModifyCallParkObject', 'ModifyCallParkSettingsObject', 'PutRecallHuntGroupObject',
            'ReadTheListOfCallParkExtensionsResponse', 'ReadTheListOfCallParksResponse']


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
    #: example: 60.0
    recall_time: Optional[int] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call
    #: will revert back to the hunt group (after the person who parked the call is alerted).
    #: example: 60.0
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
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
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


class ModifyCallExtensionParkObject(ApiModel):
    #: Name for the call park extension. The maximum length is 30.
    #: example: Illinois, Call Park Extension
    name: Optional[str] = None
    #: Unique extension which will be assigned to call park extension. The minimum length is 2, maximum length is 6.
    #: example: 407721
    extension: Optional[str] = None


class PutRecallHuntGroupObject(ApiModel):
    #: Alternate user which is a hunt group ID for call park recall alternate destination.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvZEdWamFHNXBZMkZzTFhOMWNIQnZjblF0TlRVMU9EWTNOVE13T1VCbmJXRnBiQzVqYjIwPQ
    hunt_group_id: Optional[str] = None
    #: Call park recall options.
    #: example: ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP
    option: Optional[GetRecallHuntGroupObjectOption] = None


class ModifyCallParkObject(ApiModel):
    #: Unique name for the call park. The maximum length is 80.
    #: example: technical support - insurance - customer 1
    name: Optional[str] = None
    #: Recall options that are added to call park.
    recall: Optional[PutRecallHuntGroupObject] = None
    #: Array of ID strings of people, workspaces and virtual lines that are added to call park.
    agents: Optional[list[str]] = None


class ModifyCallParkSettingsObject(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[PutRecallHuntGroupObject] = None
    #: Setting controlling call park behavior.
    call_park_settings: Optional[CallParkSettingsObject] = None


class ReadTheListOfCallParksResponse(ApiModel):
    #: Array of call parks.
    call_parks: Optional[list[ListCallParkObject]] = None


class CreateACallParkResponse(ApiModel):
    #: ID of the newly created call park.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSSy9WR1Z6ZEMxRFVFY3RNZz09
    id: Optional[str] = None


class GetAvailableAgentsFromCallParksResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceVirtualLineCallParksObject]] = None


class GetAvailableRecallHuntGroupsFromCallParksResponse(ApiModel):
    #: Array of available recall hunt groups.
    hunt_groups: Optional[list[GetAvailableRecallHuntGroupsObject]] = None


class ReadTheListOfCallParkExtensionsResponse(ApiModel):
    #: Array of call park extensions.
    call_park_extensions: Optional[list[ListCallParkExtensionObject]] = None


class FeaturesCallParkApi(ApiChild, base='telephony/config'):
    """
    Features:  Call Park
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Call Park supports reading and writing of Webex Calling Call Park settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_call_parks(self, location_id: str, org_id: str = None, max_: int = None, start: int = None,
                                    order: str = None, name: str = None,
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
        :param org_id: List call parks for this organization.
        :type org_id: str
        :param max_: Limit the number of call parks returned to this maximum count. Default is 2000.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching call parks. Default is 0.
        :type start: int
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :return: Generator yielding :class:`ListCallParkObject` instances
        """
        ...


    def create_a_call_park(self, location_id: str, name: str, recall: PutRecallHuntGroupObject, agents: list[str],
                           org_id: str = None) -> str:
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
        :param org_id: Create the call park for this organization.
        :type org_id: str
        :rtype: str
        """
        ...


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
        ...


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
        ...


    def update_a_call_park(self, location_id: str, call_park_id: str, name: str, recall: PutRecallHuntGroupObject,
                           agents: list[str], org_id: str = None) -> str:
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
        :param agents: Array of ID strings of people, workspaces and virtual lines that are added to call park.
        :type agents: list[str]
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :rtype: str
        """
        ...


    def get_available_agents_from_call_parks(self, location_id: str, org_id: str = None, call_park_name: str = None,
                                             max_: int = None, start: int = None, name: str = None,
                                             phone_number: str = None, order: str = None,
                                             **params) -> Generator[GetPersonPlaceVirtualLineCallParksObject, None, None]:
        """
        Get available agents from Call Parks

        Retrieve available agents from call parks for a given location.
        
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        
        Retrieving available agents from call parks requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param max_: Limit the number of available agents returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching available agents.
        :type start: int
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :return: Generator yielding :class:`GetPersonPlaceVirtualLineCallParksObject` instances
        """
        ...


    def get_available_recall_hunt_groups_from_call_parks(self, location_id: str, org_id: str = None, max_: int = None,
                                                         start: int = None, name: str = None, order: str = None,
                                                         **params) -> Generator[GetAvailableRecallHuntGroupsObject, None, None]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.
        
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        
        Retrieving available recall hunt groups from call parks requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :param max_: Limit the number of available recall hunt groups returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching available recall hunt groups.
        :type start: int
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort fields:
            lname.
        :type order: str
        :return: Generator yielding :class:`GetAvailableRecallHuntGroupsObject` instances
        """
        ...


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
        ...


    def update_call_park_settings(self, location_id: str, call_park_recall: PutRecallHuntGroupObject,
                                  call_park_settings: CallParkSettingsObject, org_id: str = None):
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
        ...


    def read_the_list_of_call_park_extensions(self, org_id: str = None, max_: int = None, start: int = None,
                                              extension: Union[str, datetime] = None, name: str = None,
                                              location_id: str = None, location_name: str = None, order: str = None,
                                              **params) -> Generator[ListCallParkExtensionObject, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.
        
        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.
        
        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param extension: Only return call park extensions with the matching extension.
        :type extension: Union[str, datetime]
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with the matching extension.
        :type location_name: str
        :param order: Order the available agents according to the designated fields.  Available sort fields:
            `groupName`, `callParkExtension`, `callParkExtensionName`, `callParkExtensionExternalId`.
        :type order: str
        :return: Generator yielding :class:`ListCallParkExtensionObject` instances
        """
        ...


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
        ...


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
            maximum length is 6.
        :type extension: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :rtype: str
        """
        ...


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
        ...


    def update_a_call_park_extension(self, location_id: str, call_park_extension_id: str, name: str, extension: str,
                                     org_id: str = None):
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
            maximum length is 6.
        :type extension: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        :rtype: None
        """
        ...

    ...