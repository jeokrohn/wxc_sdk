from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallParkSettingsObject', 'CallParkSettingsObjectRingPattern', 'CreateACallParkResponse', 'GetAvailableAgentsFromCallParksResponse', 'GetAvailableRecallHuntGroupsFromCallParksResponse', 'GetAvailableRecallHuntGroupsObject', 'GetCallParkExtensionObject', 'GetCallParkObject', 'GetCallParkSettingsObject', 'GetPersonPlaceVirtualLineCallParksObject', 'GetPersonPlaceVirtualLineCallParksObjectType', 'GetRecallHuntGroupObject', 'GetRecallHuntGroupObjectOption', 'GetUserNumberItemObject', 'ListCPCallParkExtensionObject', 'ListCallParkExtensionObject', 'ListCallParkObject', 'ModifyCallExtensionParkObject', 'ModifyCallParkObject', 'ModifyCallParkSettingsObject', 'PutRecallHuntGroupObject', 'ReadTheListOfCallParkExtensionsResponse', 'ReadTheListOfCallParksResponse']


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
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up within the set time, then the call will be recalled based on the Call Park Recall setting.
    #: example: 60.0
    recall_time: Optional[int] = None
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call will revert back to the hunt group (after the person who parked the call is alerted).
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
