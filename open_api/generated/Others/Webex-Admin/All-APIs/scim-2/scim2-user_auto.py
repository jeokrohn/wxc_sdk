import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AccountStatusObject', 'EmailObject', 'EmailObjectType', 'ExternalAttributeObject', 'GetUserResponse',
           'GetUserResponseUrnietfparamsscimschemasextensionenterprise20User', 'GroupObject', 'ManagedGroupsObject',
           'ManagedOrgsObject', 'ManagerResponseObject', 'MetaObject', 'NameObject', 'PatchUserOperationsItem',
           'PatchUserOperationsItemOp', 'PhotoObject', 'PhotoObjectType',
           'PostUserUrnietfparamsscimschemasextensionenterprise20User',
           'PostUserUrnietfparamsscimschemasextensionenterprise20UserManager',
           'PostUserUrnscimschemasextensionciscowebexidentity20User', 'PutUserAddressesItem',
           'PutUserPhoneNumbersItem', 'PutUserPhoneNumbersItemType', 'RoleObject', 'SCIM2UsersApi',
           'SearchGetUserResponse', 'SearchUserResponse', 'SipAddressObject', 'SipAddressObjectType',
           'UserTypeObject']


class PatchUserOperationsItemOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class RoleObject(ApiModel):
    #: CI Role
    value: Optional[str] = None
    #: name
    type: Optional[str] = None
    #: A human-readable name, primarily used for display purposes.
    display: Optional[str] = None


class PatchUserOperationsItem(ApiModel):
    #: The operation to perform.
    op: Optional[PatchUserOperationsItemOp] = None
    #: A string containing an attribute path describing the target of the operation.
    path: Optional[str] = None
    #: New value.
    value: Optional[list[RoleObject]] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20UserManager(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must belong to the same org as the
    #: user.
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Name of a cost center.
    cost_center: Optional[str] = None
    #: Name of an organization.
    organization: Optional[str] = None
    #: Name of a division.
    division: Optional[str] = None
    #: Name of a department.
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on the order of hire or association
    #: with an organization.
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20UserManager] = None


class AccountStatusObject(str, Enum):
    active = 'active'
    pending = 'pending'
    transient = 'transient'
    disabled = 'disabled'
    fraud = 'fraud'
    fraud_transient = 'fraud_transient'
    compliance_transient = 'compliance_transient'
    pending_transient = 'pending_transient'


class SipAddressObjectType(str, Enum):
    enterprise = 'enterprise'


class SipAddressObject(ApiModel):
    #: The `sipAddress` value.
    value: Optional[str] = None
    #: `sipAddress` type.
    type: Optional[SipAddressObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    display: Optional[str] = None
    #: Designate the primary `sipAddress`.
    primary: Optional[bool] = None


class ManagedOrgsObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    org_id: Optional[str] = None
    #: Role in the target organization for the user.
    role: Optional[str] = None


class ManagedGroupsObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    org_id: Optional[str] = None
    #: Webex Identity assigned group identifier.
    group_id: Optional[str] = None
    #: Role in the target group for the user.
    role: Optional[str] = None


class ExternalAttributeObject(ApiModel):
    #: Source of external attribute.
    source: Optional[str] = None
    #: Value of external attribute.
    value: Optional[str] = None


class PostUserUrnscimschemasextensionciscowebexidentity20User(ApiModel):
    #: An array of additional information about a user's status.
    account_status: Optional[AccountStatusObject] = None
    #: `sipAddress` values for the user.
    sip_addresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managed_orgs: Optional[list[ManagedOrgsObject]] = None
    #: Groups that the user can manage.
    managed_groups: Optional[list[ManagedGroupsObject]] = None
    #: The extension attributes of the user. Postfix support from 1 to 15, for example: "extensionAttribute1",
    #: "extensionAttribute2", ..., "extensionAttribute15".
    extension_attribute_: Optional[list[str]] = Field(alias='extensionAttribute*', default=None)
    #: The external attributes of the user. Postfix support from 1 to 15, for example: "externalAttribute1",
    #: "externalAttribute2", ..., "externalAttribute15".
    external_attribute_: Optional[list[ExternalAttributeObject]] = Field(alias='externalAttribute*', default=None)


class UserTypeObject(str, Enum):
    user = 'user'
    room = 'room'
    external_calling = 'external_calling'
    calling_service = 'calling_service'


class NameObject(ApiModel):
    #: The given name of the user, or first name in most Western languages (e.g., "Sarah" given the full name "Ms.
    #: Sarah J Henderson, III").
    given_name: Optional[str] = None
    #: The family name of the user, or last name in most Western languages (e.g., "Henderson" given the full name "Ms.
    #: Sarah J Henderson, III").
    family_name: Optional[str] = None
    #: The middle name(s) of the user (e.g., "Jane" given the full name "Ms. Sarah J Henderson, III").
    middle_name: Optional[str] = None
    #: The honorific prefix(es) of the user, or title in most Western languages (e.g., "Ms." given the full name "Ms.
    #: Sarah J Henderson, III").
    honorific_prefix: Optional[str] = None
    #: The honorific suffix(es) of the user, or suffix in most Western languages (e.g., "III" given the full name "Ms.
    #: Sarah J Henderson, III").
    honorific_suffix: Optional[str] = None


class PutUserPhoneNumbersItemType(str, Enum):
    work = 'work'
    home = 'home'
    mobile = 'mobile'
    work_extension = 'work_extension'
    fax = 'fax'
    pager = 'pager'
    other = 'other'


class PutUserPhoneNumbersItem(ApiModel):
    #: phone number.
    value: Optional[str] = None
    #: We support the following phone number types: 'mobile', 'work', 'fax', 'work_extension', 'alternate1',
    #: 'alternate2'.  Alternate 1 and Alternate 2 are types inherited from Webex meeting sites.
    type: Optional[PutUserPhoneNumbersItemType] = None
    #: A human-readable name, primarily used for display purposes.
    display: Optional[str] = None
    #: A Boolean value indicating the phone number's primary status.
    primary: Optional[bool] = None


class PhotoObjectType(str, Enum):
    photo = 'photo'
    thumbnail = 'thumbnail'
    resizable = 'resizable'


class PhotoObject(ApiModel):
    #: photo link.
    value: Optional[str] = None
    #: The type of the photo
    type: Optional[PhotoObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    display: Optional[str] = None
    #: A Boolean value for the photo usage status.
    primary: Optional[bool] = None


class PutUserAddressesItem(ApiModel):
    #: address type
    type: Optional[str] = None
    #: The full street address component, which may include house number, street name, P.O. box, and multi-line
    #: extended street address information. This attribute MAY contain newlines.
    street_address: Optional[str] = None
    #: The city or locality component.
    locality: Optional[str] = None
    #: The state or region component.
    region: Optional[str] = None
    #: The zip code or postal code component.
    postal_code: Optional[str] = None
    #: The country name component.
    country: Optional[str] = None


class EmailObjectType(str, Enum):
    work = 'work'
    home = 'home'
    room = 'room'
    other = 'other'


class EmailObject(ApiModel):
    #: The email address.
    value: Optional[str] = None
    #: The type of the email.
    type: Optional[EmailObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    display: Optional[str] = None
    #: Email status boolean value. If the type is work and primary is true, the value must equal `userName`.
    primary: Optional[bool] = None


class ManagerResponseObject(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must belong to the same org as the
    #: user.
    value: Optional[str] = None
    #: The name displayed for the manager in Webex.
    display_name: Optional[str] = None
    #: The URI corresponding to a SCIM user that is the manager.
    _ref: Optional[str] = Field(alias='$ref', default=None)


class GetUserResponseUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Name of a cost center.
    cost_center: Optional[str] = None
    #: Name of an organization.
    organization: Optional[str] = None
    #: Name of a division.
    division: Optional[str] = None
    #: Name of a department.
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on the order of hire or association
    #: with an organization.
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[ManagerResponseObject] = None


class MetaObject(ApiModel):
    resource_type: Optional[str] = None
    organization_id: Optional[str] = Field(alias='organizationID', default=None)
    #: The date and time the group was created.
    created: Optional[datetime] = None
    #: The date and time the group was last changed.
    last_modified: Optional[datetime] = None
    #: The version of the user.
    version: Optional[str] = None
    #: The resource itself.
    location: Optional[str] = None


class GetUserResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    id: Optional[str] = None
    #: A unique identifier for the user and authenticates the user in Webex.  This must be set to the user's primary
    #: email address.  No other user in Webex may have the same `userName` value and thus this value is required to be
    #: unique within Webex.
    user_name: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is allowed to login in Webex.
    active: Optional[bool] = None
    #: List of roles assigned to the user.
    roles: Optional[list[RoleObject]] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The name displayed for the user in Webex.
    display_name: Optional[str] = None
    #: A casual name of the user. For example, Bob when the user's formal name is Robert.
    nick_name: Optional[str] = None
    #: A list of the user's email addresses, including primary and alternative emails. The primary work email address
    #: must match the value of the user's username.
    emails: Optional[list[EmailObject]] = None
    #: User type.
    user_type: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    profile_url: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    title: Optional[str] = None
    #: User's preferred language. Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: 
    #: en_US : for United States English or fr_FR for Parisian French.
    preferred_language: Optional[str] = None
    #: The user's locale which represents the user's currency, time format, and numerical representations.  Acceptable
    #: values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: and then the 2 letter country code.  Examples are:
    #: 
    #: en_US : for United States English or fr_FR for Parisian French.
    locale: Optional[str] = None
    #: User identifier provided by an external provisioning source.
    external_id: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    timezone: Optional[str] = None
    #: A list of user's phone numbers.
    phone_numbers: Optional[list[PutUserPhoneNumbersItem]] = None
    #: A list of photo objects for the user.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddressesItem]] = None
    #: SCIM2 enterprise extension
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[GetUserResponseUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[PostUserUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)
    #: Response metadata.
    meta: Optional[MetaObject] = None


class GroupObject(ApiModel):
    #: A unique identifier for the group.
    value: Optional[str] = None
    #: Display name of the group.
    display: Optional[str] = None
    #: The URI corresponding to a group.
    _ref: Optional[str] = Field(alias='$ref', default=None)


class SearchGetUserResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    id: Optional[str] = None
    #: A unique identifier for the user and authenticates the user in Webex.  This must be set to the user's primary
    #: email address.  No other user in Webex may have the same `userName` value and thus is required to be unique
    #: within Webex.
    user_name: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is allowed to login in Webex.
    active: Optional[bool] = None
    #: List of roles assigned to the user.
    roles: Optional[list[RoleObject]] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The name displayed for the user in Webex.
    display_name: Optional[str] = None
    #: A casual name of the user. For example, Bob when the user's formal name is Robert.
    nick_name: Optional[str] = None
    #: A list of the user's email addresses, including primary and alternative emails. The primary work email address
    #: must match the value of the user's username.
    emails: Optional[list[EmailObject]] = None
    #: User type.
    user_type: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    profile_url: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    title: Optional[str] = None
    #: User's preferred language. Acceptable values are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: code followed by an _ and then the 2 letter country code.  Examples are:
    #: 
    #: en_US : for United States English or fr_FR for Parisian French.
    preferred_language: Optional[str] = None
    #: The user's locale which represents the user's currency, time format, and numerical representations.  Acceptable
    #: values are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: letter country code.  Examples are:
    #: 
    #: en_US : for United States English or fr_FR for Parisian French.
    locale: Optional[str] = None
    #: User identifier provided by an external provisioning source.
    external_id: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    timezone: Optional[str] = None
    #: A list of user's phone numbers.
    phone_numbers: Optional[list[PutUserPhoneNumbersItem]] = None
    #: A list of group details returned only when `includeGroupDetails` or `returnGroups` request parameters are set to
    #: true.
    groups: Optional[list[GroupObject]] = None
    #: A list of photo objects for the user.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddressesItem]] = None
    #: SCIM2 enterprise extension
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[GetUserResponseUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[PostUserUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)
    #: Response metadata.
    meta: Optional[MetaObject] = None


class SearchUserResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Total number of users in search results.
    total_results: Optional[int] = None
    #: The total number of items in a paged result.
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching users.
    start_index: Optional[int] = None
    #: A list of users with details.
    resources: Optional[list[SearchGetUserResponse]] = Field(alias='Resources', default=None)


class SCIM2UsersApi(ApiChild, base='identity/scim'):
    """
    SCIM 2 Users
    
    Implementation of the SCIM 2.0 user part for user management in a standards-based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition detailed in `SCIM 2.0 schema
    and `SCIM 2.0 Protocol
    <https://datatracker.ietf.org/doc/html/rfc7644>`_.
    """

    def get_me(self) -> GetUserResponse:
        """
        Get Me

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The API can be used by any user to retrieve user information using their own access token.

        <br/>

        :rtype: :class:`GetUserResponse`
        """
        url = self.ep('v2/Users/me')
        data = super().get(url)
        r = GetUserResponse.model_validate(data)
        return r

    def search_users(self, org_id: str, filter: str = None, attributes: str = None, excluded_attributes: str = None,
                     sort_by: str = None, sort_order: str = None, start_index: str = None, count: str = None,
                     return_groups: str = None, include_group_details: str = None,
                     group_usage_types: str = None) -> SearchUserResponse:
        """
        Search users

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        <br/>

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param filter: The URL encoded filter. If the value is empty, the API will return all users under the
            organization.

        The examples below show some search filters:

        - `userName` eq "user1@example.com"

        - `userName` sw "user1@example"

        - `userName` ew "example"

        - `phoneNumbers` [ type eq "mobile" and value eq "14170120"]

        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:User:meta.organizationId` eq
        "0ae87ade-8c8a-4952-af08-318798958d0c"

        - For more filter patterns, please check `filtering
        <https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2>`_.

        | **Attributes** | **Operators** |
        |-----|-----|
        | **SCIM Core**
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        | ---- |
        | `id` | eq |
        | `userName` | eq sw ew |
        | `name.familyName` | eq sw ew |
        | `name.givenName` | eq sw |
        | `name.middleName` | eq sw |
        | `name.formatted` | eq sw |
        | `displayName` | eq sw ew |
        | `nickName` | eq sw ew |
        | `emails.display` | eq sw ew |
        | `emails.value` | eq sw ew |
        | `phoneNumbers.value` | eq sw ew |
        | `phoneNumbers.display` | eq sw ew |
        | **Enterprise Extensions** | ---- |
        | `employeeNumber` | eq sw ew |
        | `costCenter` | eq sw ew |
        | `organization` | eq sw ew |
        | `division` | eq sw ew |
        | `department` | eq sw ew |
        | `manager.value` | eq |
        | `manager.displayName` | eq sw ew |
        :type filter: str
        :param attributes: A multi-valued list of string names for resource attributes to return in the response, like
            'userName,department,emails'. It supports the SCIM id
            'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User,userName'. The default is empty, all
            attributes will be returned
        :type attributes: str
        :param excluded_attributes: A multi-valued list of strings names for resource attributes to be removed from the
            default set of attributes to return. The default is empty, all attributes will be returned
        :type excluded_attributes: str
        :param sort_by: A string for the attribute whose value can be used to order the returned responses. Now we only
            allow `userName`, `id`, `meta.lastModified` to sort.
        :type sort_by: str
        :param sort_order: A string for the order in which the 'sortBy' parameter is applied. Allowed values are
            'ascending' and 'descending'.
        :type sort_order: str
        :param start_index: An integer for the 1-based index of the first query result. The default is 1.
        :type start_index: str
        :param count: An integer for the maximum number of query results per page.  The default is 100.
        :type count: str
        :param return_groups: Define whether the group information needs to be returned.  The default is false.
        :type return_groups: str
        :param include_group_details: Define whether the group information with details needs to be returned. The
            default is false.
        :type include_group_details: str
        :param group_usage_types: Returns groups with details of the specified group type.
        :type group_usage_types: str
        :rtype: :class:`SearchUserResponse`
        """
        params: dict[str, Any] = dict()
        if filter is not None:
            params['filter'] = filter
        if attributes is not None:
            params['attributes'] = attributes
        if excluded_attributes is not None:
            params['excludedAttributes'] = excluded_attributes
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_order is not None:
            params['sortOrder'] = sort_order
        if start_index is not None:
            params['startIndex'] = start_index
        if count is not None:
            params['count'] = count
        if return_groups is not None:
            params['returnGroups'] = return_groups
        if include_group_details is not None:
            params['includeGroupDetails'] = include_group_details
        if group_usage_types is not None:
            params['groupUsageTypes'] = group_usage_types
        url = self.ep(f'{org_id}/v2/Users')
        data = super().get(url, params=params)
        r = SearchUserResponse.model_validate(data)
        return r

    def create_a_user(self, org_id: str, schemas: list[str], user_name: str, user_type: UserTypeObject,
                      title: str = None, active: bool = None, roles: list[RoleObject] = None,
                      preferred_language: str = None, locale: str = None, timezone: str = None,
                      profile_url: str = None, external_id: str = None, display_name: str = None,
                      nick_name: str = None, name: NameObject = None,
                      phone_numbers: list[PutUserPhoneNumbersItem] = None, photos: list[PhotoObject] = None,
                      addresses: list[PutUserAddressesItem] = None, emails: list[EmailObject] = None,
                      urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User = None,
                      urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User = None) -> GetUserResponse:
        """
        Create a user

        The SCIM 2 /Users API provides a programmatic way to manage users in Webex Identity using The Internet
        Engineering Task Force standard SCIM 2.0 standard as specified by `RFC 7643 SCIM 2.0 Core Schema 
        <https://datatracker.ietf.org/doc/html/rfc7643>`_ and
        `RFC 7644 SCIM 2.0 Core Protocol
        <https://datatracker.ietf.org/doc/html/rfc7644>`_.  The WebEx SCIM 2.0  APIs allow clients supporting the SCIM 2.0 standard to
        manage users, and groups within Webex.  Webex supports the following SCIM 2.0 Schemas:

        • urn:ietf:params:scim:schemas:core:2.0:User

        • urn:ietf:params:scim:schemas:extension:enterprise:2.0:User

        • urn:scim:schemas:extension:cisco:webexidentity:2.0:User

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. Input JSON must contain schema: "urn:ietf:params:scim:schemas:core:2.0:User".

        2. Support 3 schemas :
        - "urn:ietf:params:scim:schemas:core:2.0:User"
        - "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
        - "urn:scim:schemas:extension:cisco:webexidentity:2.0:User"

        3. Unrecognized schemas (ID/section) are ignored.

        4. Read-only attributes provided as input values are ignored.

        The following roles cannot be assigned to a user:

        1. Location Admin

        2. Webex Site Admin

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param user_name: A unique identifier for the user that authenticates the user in Webex.  This must be set to
            the user's primary email address.  No other user in Webex may have the same `userName` value, so this
            value must be unique within Webex.
        :type user_name: str
        :param user_type: User type.
        :type user_type: UserTypeObject
        :param title: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant",
            "Engineer" etc.
        :type title: str
        :param active: A boolean value of "true" or "false" indicating whether the user is allowed to login to Webex.
        :type active: bool
        :param roles: List of roles assigned to the user.
        :type roles: list[RoleObject]
        :param preferred_language: User's preferred language. Acceptable values are based on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:

        en_US : for United States English or fr_FR for Parisian French.
        :type preferred_language: str
        :param locale: The user's locale which represents the user's currency, time format, and numerical
            representations.  Acceptable values are based on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            followed by an _ and then the 2 letter country code.  Examples are:

        en_US : for United States English or fr_FR for Parisian French.
        :type locale: str
        :param timezone: The user's time zone specified in the `IANA timezone
            <https://nodatime.org/timezones>`_ timezone format, for example,
            "America/Los_Angeles".
        :type timezone: str
        :param profile_url: A fully qualified URL pointing to a page representing the user's online profile.
        :type profile_url: str
        :param external_id: User identifier provided by an external provisioning source.
        :type external_id: str
        :param display_name: The name displayed for the user in Webex.
        :type display_name: str
        :param nick_name: A casual name of the user. For example, Bob when the user's formal name is Robert.
        :type nick_name: str
        :param name: The components of the user's real name.
        :type name: NameObject
        :param phone_numbers: A list of user's phone numbers.
        :type phone_numbers: list[PutUserPhoneNumbersItem]
        :param photos: A list of photo objects for the user.
        :type photos: list[PhotoObject]
        :param addresses: User's physical mailing address.
        :type addresses: list[PutUserAddressesItem]
        :param emails: A list of the user's email addresses, including primary and alternative emails. The primary work
            email address must match the value of the user's username.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extension
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: The Cisco extension of SCIM 2.
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User
        :rtype: :class:`GetUserResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['userName'] = user_name
        body['userType'] = enum_str(user_type)
        if title is not None:
            body['title'] = title
        if active is not None:
            body['active'] = active
        if roles is not None:
            body['roles'] = TypeAdapter(list[RoleObject]).dump_python(roles, mode='json', by_alias=True, exclude_none=True)
        if preferred_language is not None:
            body['preferredLanguage'] = preferred_language
        if locale is not None:
            body['locale'] = locale
        if timezone is not None:
            body['timezone'] = timezone
        if profile_url is not None:
            body['profileUrl'] = profile_url
        if external_id is not None:
            body['externalId'] = external_id
        if display_name is not None:
            body['displayName'] = display_name
        if nick_name is not None:
            body['nickName'] = nick_name
        if name is not None:
            body['name'] = name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[PutUserPhoneNumbersItem]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        if photos is not None:
            body['photos'] = TypeAdapter(list[PhotoObject]).dump_python(photos, mode='json', by_alias=True, exclude_none=True)
        if addresses is not None:
            body['addresses'] = TypeAdapter(list[PutUserAddressesItem]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        if emails is not None:
            body['emails'] = TypeAdapter(list[EmailObject]).dump_python(emails, mode='json', by_alias=True, exclude_none=True)
        if urn_ietf_params_scim_schemas_extension_enterprise_2_0_user is not None:
            body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        if urn_scim_schemas_extension_cisco_webexidentity_2_0_user is not None:
            body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users')
        data = super().post(url, json=body)
        r = GetUserResponse.model_validate(data)
        return r

    def delete_a_user(self, org_id: str, user_id: str) -> None:
        """
        Delete a user

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        super().delete(url)

    def get_a_user(self, org_id: str, user_id: str) -> GetUserResponse:
        """
        Get a user

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        <br/>

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :rtype: :class:`GetUserResponse`
        """
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().get(url)
        r = GetUserResponse.model_validate(data)
        return r

    def update_a_user_with_patch(self, org_id: str, user_id: str, schemas: list[str],
                                 operations: list[PatchUserOperationsItem]) -> GetUserResponse:
        """
        Update a user with PATCH

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. The PATCH API replaces individual attributes and roles of the user's data in the request body.
        The PATCH API supports `add`, `remove`, and `replace` operations on any individual
        attribute or role allowing only specific attributes of the user's object to be modified.

        2. Each operation against an attribute must be compatible with the attribute's mutability.

        3. Each PATCH operation represents a single action to be applied to the
        same SCIM resource specified by the request URI.  Operations are
        applied sequentially in the order they appear in the array.  Each
        operation in the sequence is applied to the target resource; the
        resulting resource becomes the target of the next operation.
        Evaluation continues until all operations are successfully applied or
        until an error condition is encountered.

        <br/>

        **Add operations**:

        The `add` operation adds a new attribute value to an existing resource.
        The operation must contain a `value` member whose content specifies the value to be added.
        The value may be a quoted value, or it may be a JSON object containing the sub-attributes of the complex
        attribute specified in the operation's `path`.
        The result of the add operation depends upon the target `path` reference locations:

        <br/>

        - If omitted, the target location is assumed to be the resource itself.  The `value` parameter contains a set
        of attributes to be added to the resource.

        - If the target location does not exist, the attribute and value are added.

        - If the target location specifies a complex attribute, a set of sub-attributes shall be specified in the
        `value` parameter.

        - If the target location specifies a multi-valued attribute, a new value is added to the attribute.

        - If the target location specifies a single-valued attribute, the existing value is replaced.

        - If the target location specifies an attribute that does not exist (has no value), the attribute is added with
        the new value.

        - If the target location exists, the value is replaced.

        - If the target location already contains the value specified, no changes should be made to the resource.

        <br/>

        **Replace operations**:

        The `replace` operation replaces the value at the target location specified by the `path`.
        The operation performs the following functions, depending on the target location specified by `path`:

        <br/>

        - If the `path` parameter is omitted, the target is assumed to be the resource itself.  In this case, the
        `value` attribute shall contain a list of one or more attributes to be replaced.

        - If the target location is a single-value attribute, the value of the attribute is replaced.

        - If the target location is a multi-valued attribute and no filter is specified, the attribute and all values
        are replaced.

        - If the target location path specifies an attribute that does not exist, the service provider shall treat the
        operation as an "add".

        - If the target location specifies a complex attribute, a set of sub-attributes SHALL be specified in the
        `value` parameter, which replaces any existing values or adds where an attribute did not previously exist.
        Sub-attributes not specified in the `value` parameters are left unchanged.

        - If the target location is a multi-valued attribute and a value selection ("valuePath") filter is specified
        that matches one or more values of the multi-valued attribute, then all matching record values will be
        replaced.

        - If the target location is a complex multi-valued attribute with a value selection filter ("valuePath") and a
        specific sub-attribute (e.g., "addresses[type eq "work"].streetAddress"), the matching sub-attribute of all
        matching records is replaced.

        - If the target location is a multi-valued attribute for which a value selection filter ("valuePath") has been
        supplied and no record match was made, the service provider will return failure as HTTP status code 400 and a
        `scimType` error code of "noTarget".

        <br/>

        **Remove operations**:

        The `remove` operation removes the value at the target location specified by the required attribute `path`.
        The operation performs the following functions, depending on the target location specified by `path`:

        <br/>

        - If `path` is unspecified, the operation fails with HTTP status code 400 and a "scimType" error code of
        "noTarget".

        - If the target location is a single-value attribute, the attribute and its associated value is removed, and
        the attribute will be considered unassigned.

        - If the target location is a multi-valued attribute and no filter is specified, the attribute and all values
        are removed, and the attribute SHALL be considered unassigned.

        - If the target location is a multi-valued attribute and a complex filter is specified comparing a `value`, the
        values matched by the filter are removed.  If no other values remain after the removal of the selected values,
        the multi-valued attribute will be considered unassigned.

        - If the target location is a complex multi-valued attribute and a complex filter is specified based on the
        attribute's sub-attributes, the matching records are removed.  Sub-attributes whose values have been removed
        will be considered unassigned.  If the complex multi-valued attribute has no remaining records, the attribute
        will be considered unassigned.

        The following roles cannot be assigned to a user:

        1. Location Admin

        2. Webex Site Admin

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param operations: A list of patch operations.
        :type operations: list[PatchUserOperationsItem]
        :rtype: :class:`GetUserResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['Operations'] = TypeAdapter(list[PatchUserOperationsItem]).dump_python(operations, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().patch(url, json=body)
        r = GetUserResponse.model_validate(data)
        return r

    def update_a_user_with_put(self, org_id: str, user_id: str, schemas: list[str], user_name: str,
                               user_type: UserTypeObject, title: str = None, active: bool = None,
                               roles: list[RoleObject] = None, preferred_language: str = None, locale: str = None,
                               timezone: str = None, profile_url: str = None, external_id: str = None,
                               display_name: str = None, nick_name: str = None,
                               phone_numbers: list[PutUserPhoneNumbersItem] = None, photos: list[PhotoObject] = None,
                               addresses: list[PutUserAddressesItem] = None, emails: list[EmailObject] = None,
                               urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User = None,
                               urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User = None) -> GetUserResponse:
        """
        Update a user with PUT

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. Input JSON must contain schema: "urn:ietf:params:scim:schemas:core:2.0:User".

        2. Support 3 schemas :
        - "urn:ietf:params:scim:schemas:core:2.0:User"
        - "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
        - "urn:scim:schemas:extension:cisco:webexidentity:2.0:User"

        3. Unrecognized schemas (ID/section) are ignored.

        4. Read-only attributes provided as input values are ignored.

        5. User `id` will not be changed.

        6. `meta`.`created` will not be changed.

        7. The PUT API replaces the contents of the user's data with the data in the request body.  All attributes
        specified in the request body will replace all existing attributes for the `userId` specified in the URL.
        Should you wish to replace or change some attributes as opposed to all attributes please refer to the SCIM
        PATCH operation https://developer.webex.com/docs/api/v1/scim2-user/update-a-user-with-patch.

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param user_name: A unique identifier for the user and authenticates the user in Webex.  This must be set to
            the user's primary email address.  No other user in Webex may have the same `userName` value and thus this
            value is required to be unique within Webex.
        :type user_name: str
        :param user_type: User type.
        :type user_type: UserTypeObject
        :param title: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant",
            "Engineer" etc.
        :type title: str
        :param active: A boolean value of "true" or "false" indicating whether the user is allowed to login to Webex.
        :type active: bool
        :param roles: List of roles assigned to the user.
        :type roles: list[RoleObject]
        :param preferred_language: User's preferred language.  Acceptable values for this field are based on the
            `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            Examples are:

        en_US : for United States English or fr_FR for Parisian French.
        :type preferred_language: str
        :param locale: The user's locale which represents the user's currency, time format, and numerical
            representations.  Acceptable values are based on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            followed by an _ and then the 2 letter country code.  Examples are:

        en_US : for United States English or fr_FR for Parisian French.
        :type locale: str
        :param timezone: The user's time zone specified in the `IANA timezone
            <https://nodatime.org/timezones>`_ timezone format. e.g:
            "America/Los_Angeles".
        :type timezone: str
        :param profile_url: A fully qualified URL pointing to a page representing the user's online profile.
        :type profile_url: str
        :param external_id: User identifier provided by an external provisioning source.
        :type external_id: str
        :param display_name: The name displayed for the user in Webex.
        :type display_name: str
        :param nick_name: A casual name of the user. For example, Bob when the user's formal name is Robert.
        :type nick_name: str
        :param phone_numbers: A list of user's phone numbers.
        :type phone_numbers: list[PutUserPhoneNumbersItem]
        :param photos: A list of photo objects for the user.
        :type photos: list[PhotoObject]
        :param addresses: User's physical mailing address.
        :type addresses: list[PutUserAddressesItem]
        :param emails: A list of the user's email addresses, including primary and alternative emails. The primary work
            email address must match the value of the user's username.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extension
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: cisco extension of SCIM 2
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User
        :rtype: :class:`GetUserResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['userName'] = user_name
        body['userType'] = enum_str(user_type)
        if title is not None:
            body['title'] = title
        if active is not None:
            body['active'] = active
        if roles is not None:
            body['roles'] = TypeAdapter(list[RoleObject]).dump_python(roles, mode='json', by_alias=True, exclude_none=True)
        if preferred_language is not None:
            body['preferredLanguage'] = preferred_language
        if locale is not None:
            body['locale'] = locale
        if timezone is not None:
            body['timezone'] = timezone
        if profile_url is not None:
            body['profileUrl'] = profile_url
        if external_id is not None:
            body['externalId'] = external_id
        if display_name is not None:
            body['displayName'] = display_name
        if nick_name is not None:
            body['nickName'] = nick_name
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[PutUserPhoneNumbersItem]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        if photos is not None:
            body['photos'] = TypeAdapter(list[PhotoObject]).dump_python(photos, mode='json', by_alias=True, exclude_none=True)
        if addresses is not None:
            body['addresses'] = TypeAdapter(list[PutUserAddressesItem]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        if emails is not None:
            body['emails'] = TypeAdapter(list[EmailObject]).dump_python(emails, mode='json', by_alias=True, exclude_none=True)
        if urn_ietf_params_scim_schemas_extension_enterprise_2_0_user is not None:
            body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        if urn_scim_schemas_extension_cisco_webexidentity_2_0_user is not None:
            body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().put(url, json=body)
        r = GetUserResponse.model_validate(data)
        return r
