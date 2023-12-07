from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BetaFeaturesPagingGroupWithESNFeatureApi', 'GetPagingGroupAgentObject', 'GetPagingGroupAgentObjectType',
            'GetPagingGroupObject', 'ListPagingGroupObject']


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
    #: Agents phone number. Minimum length is 1. Maximum length is 23.  Either `phoneNumber` or `extension` is
    #: mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Agents extension. Minimum length is 2. Maximum length is 6.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 7781
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12347781
    esn: Optional[str] = None


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
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is
    #: mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either `phoneNumber` or `extension` is
    #: mandatory.
    #: example: 7781
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12347781
    esn: Optional[str] = None
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
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator
    #: ID.
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
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is
    #: mandatory.
    #: example: +15558675309
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either `phoneNumber` or `extension` is
    #: mandatory.
    #: example: 7781
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12347781
    esn: Optional[str] = None
    #: Name of location for paging group.
    #: example: Alaska
    location_name: Optional[str] = None
    #: Id of location for paging group.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None


class BetaFeaturesPagingGroupWithESNFeatureApi(ApiChild, base='telephony/config'):
    """
    Beta Features:  Paging Group with ESN Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Paging Group supports reading and writing of Webex Calling Paging Group settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_paging_groups(self, location_id: str = None, name: str = None, phone_number: str = None,
                                       org_id: str = None, **params) -> Generator[ListPagingGroupObject, None, None]:
        """
        Read the List of Paging Groups

        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListPagingGroupObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('paging')
        return self.session.follow_pagination(url=url, model=ListPagingGroupObject, item_key='locationPaging', params=params)

    def get_details_for_a_paging_group(self, location_id: str, paging_id: str,
                                       org_id: str = None) -> GetPagingGroupObject:
        """
        Get Details for a Paging Group

        Retrieve Paging Group details.

        Group Paging allows a person, place or virtual line a one-way call or group page to up to 75 people and/or
        workspaces and/or virtual line by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving paging group details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Retrieve paging group settings from this organization.
        :type org_id: str
        :rtype: :class:`GetPagingGroupObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        data = super().get(url, params=params)
        r = GetPagingGroupObject.model_validate(data)
        return r
