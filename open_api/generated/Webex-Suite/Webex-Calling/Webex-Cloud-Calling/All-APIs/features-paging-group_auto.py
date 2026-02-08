from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['DirectLineCallerIdNameObject', 'FeaturesPagingGroupApi', 'GetPagingGroupAgentObject',
           'GetPagingGroupAgentObjectType', 'GetPagingGroupObject', 'ListPagingGroupObject',
           'PagingGroupPrimaryAvailableNumberObject', 'STATE', 'SelectionObject', 'TelephonyType']


class GetPagingGroupAgentObjectType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Indicates that this object is a workspace, formerly known as a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetPagingGroupAgentObject(ApiModel):
    #: Agents ID.
    id: Optional[str] = None
    #: Agent's first name. Minimum length is 1. Maximum length is 64.
    first_name: Optional[str] = None
    #: Agent's last name. Minimum length is 1. Maximum length is 64.
    last_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[GetPagingGroupAgentObjectType] = None
    #: Agent's phone number. Minimum length is 1. Maximum length is 23.  Either `phoneNumber` or `extension` is
    #: mandatory.
    phone_number: Optional[str] = None
    #: Agent's extension. Minimum length is 2. Maximum length is 10.  Either `phoneNumber` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None


class SelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this paging group.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `name` is to be shown for this paging group.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `DISPLAY_NAME`.
    selection: Optional[SelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class GetPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    id: Optional[str] = None
    #: Whether or not the paging group is enabled.
    enabled: Optional[bool] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is
    #: mandatory.
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 10. Either `phoneNumber` or `extension` is
    #: mandatory.
    extension: Optional[str] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None
    #: Paging language. Minimum length is 1. Maximum length is 40.
    language: Optional[str] = None
    #: Language code.
    language_code: Optional[str] = None
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 64. This field
    #: has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
    first_name: Optional[str] = None
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 64. This field
    #: has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
    last_name: Optional[str] = None
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator
    #: ID.
    originator_caller_id_enabled: Optional[bool] = None
    #: An array of people, workspaces and virtual lines ID's who may originate pages to this paging group.
    originators: Optional[list[GetPagingGroupAgentObject]] = None
    #: An array of people, workspaces and virtual lines ID's that are added to paging group as paging call targets.
    targets: Optional[list[GetPagingGroupAgentObject]] = None
    #: Settings for the direct line caller ID name to be shown for this Group Paging.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The name to be used for dial by name functions.
    dial_by_name: Optional[str] = None


class ListPagingGroupObject(ApiModel):
    #: A unique identifier for the paging group.
    id: Optional[str] = None
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    name: Optional[str] = None
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either `phoneNumber` or `extension` is
    #: mandatory.
    phone_number: Optional[str] = None
    #: Paging group extension. Minimum length is 2. Maximum length is 10. Either `phoneNumber` or `extension` is
    #: mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Name of location for paging group.
    location_name: Optional[str] = None
    #: Id of location for paging group.
    location_id: Optional[str] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class PagingGroupPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


class FeaturesPagingGroupApi(ApiChild, base='telephony/config'):
    """
    Features:  Paging Group
    
    Features: Paging Group supports reading and writing of Webex Calling Paging Group settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def create_a_new_paging_group(self, location_id: str, name: str, phone_number: str = None, extension: str = None,
                                  language_code: str = None, first_name: str = None, last_name: str = None,
                                  originator_caller_id_enabled: bool = None, originators: list[str] = None,
                                  targets: list[str] = None,
                                  direct_line_caller_id_name: DirectLineCallerIdNameObject = None,
                                  dial_by_name: str = None, org_id: str = None) -> str:
        """
        Create a new Paging Group

        Create a new Paging Group for the given location.

        Group Paging allows a one-way call or group page to up to 75 people, workspaces and virtual lines by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Creating a paging group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param name: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Paging group extension. Minimum length is 2. Maximum length is 10.  Either `phoneNumber` or
            `extension` is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 64. This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 64. This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller ID when a group page is
            performed. If true shows page originator ID.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people, workspace, and virtual lines IDs who can originate pages to this paging
            group.
        :type originators: list[str]
        :param targets: An array of people, workspaces and virtual lines IDs will add to a paging group as paging call
            targets.
        :type targets: list[str]
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this paging
            group.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: The name to be used for dial by name functions.  Characters of `%`,  `+`, `\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_name: str
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if originator_caller_id_enabled is not None:
            body['originatorCallerIdEnabled'] = originator_caller_id_enabled
        if originators is not None:
            body['originators'] = originators
        if targets is not None:
            body['targets'] = targets
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/paging')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_paging_group_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[PagingGroupPrimaryAvailableNumberObject, None, None]:
        """
        Get Paging Group Primary Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the paging group's primary
        phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PagingGroupPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/paging/availableNumbers')
        return self.session.follow_pagination(url=url, model=PagingGroupPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def delete_a_paging_group(self, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete a Paging Group

        Delete the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Deleting a paging group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :type paging_id: str
        :param org_id: Delete the paging group from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        super().delete(url, params=params)

    def get_details_for_a_paging_group(self, location_id: str, paging_id: str,
                                       org_id: str = None) -> GetPagingGroupObject:
        """
        Get Details for a Paging Group

        Retrieve Paging Group details.

        Group Paging allows a person, place or virtual line a one-way call or group page to up to 75 people and/or
        workspaces and/or virtual line by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving paging group details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

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

    def update_a_paging_group(self, location_id: str, paging_id: str, enabled: bool = None, name: str = None,
                              phone_number: str = None, extension: str = None, language_code: str = None,
                              first_name: str = None, last_name: str = None,
                              originator_caller_id_enabled: bool = None, originators: list[str] = None,
                              targets: list[str] = None,
                              direct_line_caller_id_name: DirectLineCallerIdNameObject = None,
                              dial_by_name: str = None, org_id: str = None):
        """
        Update a Paging Group

        Update the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people, workspaces and virtual
        lines by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Updating a paging group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param enabled: Whether or not the paging group is enabled.
        :type enabled: bool
        :param name: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Paging group extension. Minimum length is 2. Maximum length is 10.  Either `phoneNumber` or
            `extension` is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this paging group. Defaults to ".".
            This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this paging group. Defaults to the
            phone number if set, otherwise defaults to call group name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller ID when a group page is
            performed. If true shows page originator ID.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people and/or workspaces, who may originate pages to this paging group.
        :type originators: list[str]
        :param targets: People, including workspaces, that are added to paging group as paging call targets.
        :type targets: list[str]
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this paging
            group.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: Sets or clears the name to be used for dial by name functions. To clear the `dialByName`,
            the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and Unicode
            characters are not allowed.
        :type dial_by_name: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if originator_caller_id_enabled is not None:
            body['originatorCallerIdEnabled'] = originator_caller_id_enabled
        if originators is not None:
            body['originators'] = originators
        if targets is not None:
            body['targets'] = targets
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        super().put(url, params=params, json=body)

    def read_the_list_of_paging_groups(self, location_id: str = None, name: str = None, phone_number: str = None,
                                       org_id: str = None, **params) -> Generator[ListPagingGroupObject, None, None]:
        """
        Read the List of Paging Groups

        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

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
