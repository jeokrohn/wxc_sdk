from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetPagingGroupAgentObject', 'GetPagingGroupAgentObjectType', 'GetPagingGroupObject', 'GetPagingGroupObjectDepartment', 'ListPagingGroupObject', 'UpdatePagingGroupObject', 'UpdatePagingGroupObjectDepartment']


class GetPagingGroupAgentObjectType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Indicates that this object is a workspace, formerly known as a place.
    place = 'PLACE'


class GetPagingGroupAgentObject(ApiModel):
    #: Agents ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YTc2ZmVmNC1mZjlmLTExZWItYWYwZC00M2YwZjY1NTdjYWI
    id: Optional[str] = None
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    #: example: John
    firstName: Optional[str] = None
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    #: example: Doe
    lastName: Optional[str] = None
    #: Type of the person or workspace.
    #: example: PEOPLE
    type: Optional[GetPagingGroupAgentObjectType] = None
    #: Agents phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    #: example: +15558675309
    phoneNumber: Optional[str] = None
    #: Agents extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None


class GetPagingGroupObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class GetPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    #: example: Y2lzY29zcGFyazovL3VzL1BBR0lOR19HUk9VUC85ZTgzZmEzYy0yYjEzLTQ2MzEtOWE1Mi0zZjg2M2NjYWVlYzg
    id: Optional[str] = None
    #: Whether or not the paging group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    #: example: +15558675309
    phoneNumber: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Paging language. Minimum length is 1. Maximum length is 40.
    #: example: English
    language: Optional[str] = None
    #: Language code.
    #: example: en_us
    languageCode: Optional[str] = None
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Paging
    firstName: Optional[str] = None
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Group
    lastName: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    #: example: True
    originatorCallerIdEnabled: Optional[bool] = None
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[GetPagingGroupAgentObject]] = None
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[GetPagingGroupAgentObject]] = None
    #: Specifies the department information.
    department: Optional[GetPagingGroupObjectDepartment] = None


class ListPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    #: example: Y2lzY29zcGFyazovL3VzL1BBR0lOR19HUk9VUC85ZTgzZmEzYy0yYjEzLTQ2MzEtOWE1Mi0zZjg2M2NjYWVlYzg
    id: Optional[str] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    #: example: +15558675309
    phoneNumber: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Name of location for paging group.
    #: example: Alaska
    locationName: Optional[str] = None
    #: ID of location for paging group.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    locationId: Optional[str] = None
    #: Specifies the department information.
    department: Optional[GetPagingGroupObjectDepartment] = None


class UpdatePagingGroupObjectDepartment(ApiModel):
    #: Unique identifier of the department.  Set to null to remove entity from department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class UpdatePagingGroupObject(ApiModel):
    #: Whether or not the paging group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    #: example: +15558675309
    phoneNumber: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Language code.
    #: example: en_us
    languageCode: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this paging group. Defaults to ".".
    #: example: Hakim
    firstName: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this paging group. Defaults to the phone number if set, otherwise defaults to call group name.
    #: example: Smith
    lastName: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    #: example: True
    originatorCallerIdEnabled: Optional[bool] = None
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[str]] = None
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[str]] = None
    #: Specifies the department information.
    department: Optional[UpdatePagingGroupObjectDepartment] = None
