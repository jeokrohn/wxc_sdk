from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateANewPagingGroupResponse', 'GetPagingGroupAgentObject', 'GetPagingGroupAgentObjectType', 'GetPagingGroupObject', 'ListPagingGroupObject', 'PostPagingGroupObject', 'ReadTheListOfPagingGroupsResponse', 'UpdatePagingGroupObject']


class GetPagingGroupAgentObjectType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Indicates that this object is a workspace, formerly known as a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetPagingGroupAgentObject(ApiModel):
    #: Agents ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YTc2ZmVmNC1mZjlmLTExZWItYWYwZC00M2YwZjY1NTdjYWI
    id: Optional[str] = None
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    #: example: John
    first_name: Optional[str] = None
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    #: example: Doe
    last_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPagingGroupAgentObjectType] = None
    #: Agents phone number. Minimum length is 1. Maximum length is 23.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Agents extension. Minimum length is 2. Maximum length is 6.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None


class GetPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    #: example: Y2lzY29zcGFyazovL3VzL1BBR0lOR19HUk9VUC9hSFpoWlROMk1HOHliMEEyTkRrME1USTVOeTVwYm5ReE1DNWlZMnhrTG5kbFltVjRMbU52YlE
    id: Optional[str] = None
    #: Whether or not the paging group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None
    #: Paging language. Minimum length is 1. Maximum length is 40.
    #: example: English
    language: Optional[str] = None
    #: Language code.
    #: example: en_us
    language_code: Optional[str] = None
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Paging
    first_name: Optional[str] = None
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Group
    last_name: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    #: example: True
    originator_caller_id_enabled: Optional[bool] = None
    #: An array of people, workspaces and virtual lines ID's who may originate pages to this paging group.
    originators: Optional[list[GetPagingGroupAgentObject]] = None
    #: An array of people, workspaces and virtual lines ID's that are added to paging group as paging call targets.
    targets: Optional[list[GetPagingGroupAgentObject]] = None


class ListPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    #: example: Y2lzY29zcGFyazovL3VzL1BBR0lOR19HUk9VUC9hSFpoWlROMk1HOHliMEEyTkRrME1USTVOeTVwYm5ReE1DNWlZMnhrTG5kbFltVjRMbU52YlE
    id: Optional[str] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Name of location for paging group.
    #: example: Alaska
    location_name: Optional[str] = None
    #: Id of location for paging group.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None


class PostPagingGroupObject(ApiModel):
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: PagingGroup-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Language code.
    #: example: en_us
    language_code: Optional[str] = None
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Paging
    first_name: Optional[str] = None
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    #: example: Group
    last_name: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    #: example: True
    originator_caller_id_enabled: Optional[bool] = None
    #: An array of people, workspace, and virtual lines IDs who can originate pages to this paging group.
    originators: Optional[list[str]] = None
    #: An array of people, workspaces and virtual lines IDs will add to a paging group as paging call targets.
    targets: Optional[list[str]] = None


class UpdatePagingGroupObject(ApiModel):
    #: Whether or not the paging group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    #: example: CallQueue-1
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Language code.
    #: example: en_us
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this paging group. Defaults to ".".
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this paging group. Defaults to the phone number if set, otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    #: example: True
    originator_caller_id_enabled: Optional[bool] = None
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[str]] = None
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[str]] = None


class ReadTheListOfPagingGroupsResponse(ApiModel):
    #: Array of paging groups.
    location_paging: Optional[list[ListPagingGroupObject]] = None


class CreateANewPagingGroupResponse(ApiModel):
    #: ID of the newly created paging group.
    id: Optional[str] = None
