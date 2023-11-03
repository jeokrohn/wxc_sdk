from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListNumbersAssociatedWithASpecificWorkspaceResponse', 'Location', 'MonitoredElementCallParkExtension', 'MonitoredElementItem', 'MonitoredElementUser', 'MonitoredElementUserType', 'PhoneNumbers', 'UserMonitoringGet', 'UserNumberItem', 'Workspace']


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: Name of call park extension.
    #: example: CPE1
    name: Optional[str] = None
    #: Extension of call park extension.
    #: example: 8080
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Name of location for call park extension.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of location for call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementUserType(str, Enum):
    #: Object is a user.
    people = 'PEOPLE'
    #: Object is a workspace.
    place = 'PLACE'


class UserNumberItem(ApiModel):
    #: Phone number of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: 8080
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Flag to indicate primary phone.
    #: example: True
    primary: Optional[bool] = None
    #: Flag to indicate toll free number.
    #: example: True
    toll_free_number: Optional[bool] = None


class MonitoredElementUser(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Brown
    last_name: Optional[str] = None
    #: Display name of person or workspace.
    #: example: John Brown
    display_name: Optional[str] = None
    #: Type of the person or workspace.
    #: example: PEOPLE
    type: Optional[MonitoredElementUserType] = None
    #: Email of the person or workspace.
    #: example: john.brown@gmail.com
    email: Optional[str] = None
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumberItem]] = None
    #: Name of location for call park.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of the location for call park.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementItem(ApiModel):
    #: Monitored Call Park extension.
    callparkextension: Optional[MonitoredElementCallParkExtension] = None
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser] = None


class PhoneNumbers(ApiModel):
    #: PSTN phone number in E.164 format.
    #: example: +12055550001
    external: Optional[str] = None
    #: Extension for workspace.
    #: example: 123
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234123
    esn: Optional[str] = None
    #: If `true`, the primary number.
    #: example: True
    primary: Optional[bool] = None


class UserMonitoringGet(ApiModel):
    #: Call park notification enabled or disabled.
    #: example: True
    call_park_notification_enabled: Optional[bool] = None
    #: Monitored element items.
    monitored_elements: Optional[MonitoredElementItem] = None


class Location(ApiModel):
    #: Location identifier associated with the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    id: Optional[str] = None
    #: Location name associated with the workspace.
    #: example: MainOffice
    name: Optional[str] = None


class Workspace(ApiModel):
    #: Workspace ID associated with the list of numbers.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9QTEFDRS8xNzdmNTNlZC1hNzY2LTRkYTAtOGQ3OC03MjE0MjhjMmFjZTQ=
    id: Optional[str] = None


class ListNumbersAssociatedWithASpecificWorkspaceResponse(ApiModel):
    #: Array of numbers (primary/alternate).
    phone_numbers: Optional[list[PhoneNumbers]] = None
    #: Workspace object having a unique identifier for the Workspace.
    workspace: Optional[Workspace] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None
    #: Organization object having a unique identifier for the organization and its name.
    organization: Optional[Location] = None
