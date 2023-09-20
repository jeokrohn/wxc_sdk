from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetCallParkExtensionObject', 'GetCallParkObject', 'GetPersonPlaceVirtualLineCallParksObject', 'GetPersonPlaceVirtualLineCallParksObjectType', 'GetRecallHuntGroupObject', 'GetRecallHuntGroupObjectOption', 'GetUserNumberItemObject', 'ListCPCallParkExtensionObject', 'ListCallParkExtensionObject']


class GetCallParkExtensionObject(ApiModel):
    #: The extension for the call park extension.
    #: example: 1415
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
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
    huntGroupId: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: Technical Support Group - 5558675309
    huntGroupName: Optional[str] = None
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
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
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
    firstName: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    #: example: Brown
    lastName: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    #: example: johnBrown
    displayName: Optional[str] = None
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
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
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
    parkOnAgentsEnabled: Optional[bool] = None
    #: Array of call park extensions assigned to a call park.
    callParkExtensions: Optional[list[ListCPCallParkExtensionObject]] = None


class ListCallParkExtensionObject(ApiModel):
    #: Unique identifier for the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vMGYzZTkwNGItYzliNC00ODNmLWI4MWItZmI0ZjkyMWcxNDUzCg
    id: Optional[str] = None
    #: The extension for the call park extension.
    #: example: 1415
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341415
    esn: Optional[str] = None
    #: A unique name for the call park extension.
    #: example: 14159265
    name: Optional[str] = None
    #: ID of location for call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    locationId: Optional[str] = None
    #: Name of location for call park extension.
    #: example: WXCSIVDKCPAPIC4S1
    locationName: Optional[str] = None
