from datetime import datetime
from json import loads
from typing import Optional

from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['EmailObject', 'EmailObjectType', 'ScimUser',
           'EnterpriseUser', 'ManagedOrg',
           'ManagerResponseObject', 'NameObject', 'PatchUserOperation', 'PatchUserOperationOp', 'PhotoObject',
           'PhotoObjectType', 'PostUserUrnietfparamsscimschemasextensionenterprise20User',
           'PostUserUrnietfparamsscimschemasextensionenterprise20UserManager',
           'WebexUser', 'PutUserAddresses', 'UserPhoneNumber',
           'ScimPhoneNumberType', 'SCIM2UsersApi', 'SearchUserResponse', 'SipAddressObject',
           'UserTypeObject']


class PatchUserOperationOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class PatchUserOperation(ApiModel):
    #: The operation to perform.
    op: Optional[PatchUserOperationOp] = None
    #: A string containing an attribute path describing the target of the operation.
    path: Optional[str] = None
    #: New value.
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20UserManager(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Identifies the name of a cost center.
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    organization: Optional[str] = None
    #: Identifies the name of a division.
    division: Optional[str] = None
    #: Identifies the name of a department.
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20UserManager] = None


class SipAddressObject(ApiModel):
    #: The sip address value.
    value: Optional[str] = None
    #: The type of the sipAddress.
    type: Optional[str] = None
    #: A human-readable description, primarily used for display purposes.
    display: Optional[str] = None
    #: Designate the primary sipAddress.
    primary: Optional[bool] = None


class ManagedOrg(ApiModel):
    #: Webex Identity assigned organization identifier.
    org_id: Optional[str] = None
    #: Role in the target organization for the user.
    role: Optional[str] = None


class WebexUser(ApiModel):
    #: Account status of the user.
    account_status: Optional[list[str]] = None
    #: sipAddress values for the user.
    sip_addresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managed_orgs: Optional[list[ManagedOrg]] = None


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


class ScimPhoneNumberType(str, Enum):
    work = 'work'
    home = 'home'
    mobile = 'mobile'
    work_extension = 'work_extension'
    fax = 'fax'
    pager = 'pager'
    other = 'other'


class UserPhoneNumber(ApiModel):
    #: phone number.
    value: Optional[str] = None
    #: We support the following types of phone numbers: 'mobile', 'work', 'fax', 'work_extension', 'alternate1',
    #: 'alternate2'.  Alternate 1 and Alternate 2 are types inherited from Webex meeting sites.
    type: Optional[ScimPhoneNumberType] = None
    #: A human-readable name, primarily used for display purposes.
    display: Optional[str] = None
    #: A Boolean value indicating the phone number premary status.
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
    #: A Boolean value indicating the photo usage status.
    primary: Optional[bool] = None


class PutUserAddresses(ApiModel):
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
    #: A Boolean value indicating the email status. If the type is work and primary is true, the value must equal
    #: "userName".
    primary: Optional[bool] = None


class ManagerResponseObject(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    value: Optional[str] = None
    #: The value to display or show the manager's name in Webex.
    display_name: Optional[str] = None
    #: The URI corresponding to a SCIM user that is the manager.
    ref: Optional[str] = Field(alias='$ref', default=None)


class EnterpriseUser(ApiModel):
    #: Identifies the name of a cost center.
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    organization: Optional[str] = None
    #: Identifies the name of a division.
    division: Optional[str] = None
    #: Identifies the name of a department.
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[ManagerResponseObject] = None


class ScimMeta(ApiModel):
    resource_type: Optional[str] = None
    location: Optional[str] = None
    version: Optional[str] = None
    created: Optional[datetime] = None
    last_modified: Optional[datetime] = None


class ScimUser(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    id: Optional[str] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to
    #: the user's primary email address.  No other user in Webex may have the same userName value and thus this value
    #: is required to be unique within Webex.
    user_name: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    active: Optional[bool] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The value to display or show the user's name in Webex.
    display_name: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    nick_name: Optional[str] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email
    #: address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: The type of the user.
    user_type: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    profile_url: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    title: Optional[str] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #:
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    preferred_language: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.
    #: Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: followed by an _ and then the 2 letter country code.  Examples are:
    #:
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    locale: Optional[str] = None
    #: External identity.
    external_id: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    timezone: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[UserPhoneNumber]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: SCIM2 enterprise extension
    enterprise_user: Optional[EnterpriseUser] = Field(
        alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    webex_user: Optional[WebexUser] = Field(
        alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)
    meta: Optional[ScimMeta] = None


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
    resources: Optional[list[ScimUser]] = Field(alias='Resources', default=None)


class SCIM2UsersApi(ApiChild, base='identity/scim'):
    """
    SCIM 2 Users

    Implementation of the SCIM 2.0 user part for user management in a standards based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition with
    detailed in
    `SCIM 2.0 schema
    <https://datatracker.ietf.org/doc/html/rfc7643>`_ and `SCIM 2.0 Protocol
    """

    def ep(self, path: str = None):
        """
        endpoint URL for given path

        :meta private:
        :param path: path after APIChild subclass specific endpoint URI prefix
        :type path: str
        :return: endpoint URL
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return f'https://webexapis.com/{self.base}{path}'

    def create_a_user(self, org_id: str, schemas: list[str], user_name: str, user_type: UserTypeObject, title: str,
                      active: bool, preferred_language: str, locale: str, timezone: str, profile_url: str,
                      external_id: str, display_name: str, nick_name: str, name: NameObject,
                      phone_numbers: list[UserPhoneNumber], photos: list[PhotoObject],
                      addresses: list[PutUserAddresses], emails: list[EmailObject],
                      urn_ietf_params_scim_schemas_extension_enterprise_2_0_user:
                      PostUserUrnietfparamsscimschemasextensionenterprise20User,
                      urn_scim_schemas_extension_cisco_webexidentity_2_0_user: WebexUser) -> ScimUser:
        """
        Create a user

        The SCIM 2 /Users API provides a programmatic way to manage users in Webex Identity using The Internet
        Engineering Task Force standard SCIM 2.0 standard as specified by `RFC 7643 SCIM 2.0 Core Schema
        <https://datatracker.ietf.org/doc/html/rfc7643>`_ and
        `RFC 7644 SCIM 2.0 Core Protocol
        <https://datatracker.ietf.org/doc/html/rfc7644>`_.  The WebEx SCIM 2.0  APIs allow clients supporting the
        SCIM 2.0 standard to
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

        - `Identity:SCIM`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. Input JSON must contain schema: "urn:ietf:params:scim:schemas:core:2.0:User".

        1. Support 3 schemas :
        - "urn:ietf:params:scim:schemas:core:2.0:User"
        - "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
        - "urn:scim:schemas:extension:cisco:webexidentity:2.0:User"

        1. Unrecognized schemas (ID/section) are ignored.

        1. Read-only attributes provided as input values are ignored.

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param user_name: A unique identifier for the user and is used to authenticate the user in Webex.  This
            attribute must be set to the user's primary email address.  No other user in Webex may have the same
            userName value and thus this value is required to be unique within Webex.
        :type user_name: str
        :param user_type: The type of the user.
        :type user_type: UserTypeObject
        :param title: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant",
            "Engineer" etc.
        :type title: str
        :param active: A boolean value of "true" or "false" indicating whether the user is active in Webex.
        :type active: bool
        :param preferred_language: Indicates the user's preferred language.  Acceptable values for this field are based
            on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            code.  Examples are:

        en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
        :type preferred_language: str
        :param locale: The user's locale which is used to represent the user's currency, time format, and numerical
            representations.  Acceptable values for this field are based on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            language code followed by an _ and then the 2 letter country code.  Examples are:

        en_US : for English spoken in the United States or fr_FR: for French spoken in France.
        :type locale: str
        :param timezone: The user's time zone specified in the `IANA timezone
            <https://nodatime.org/timezones>`_ timezone format, for example,
            "America/Los_Angeles".
        :type timezone: str
        :param profile_url: A fully qualified URL pointing to a page representing the user's online profile.
        :type profile_url: str
        :param external_id: External identity.
        :type external_id: str
        :param display_name: The value to display or show the user's name in Webex.
        :type display_name: str
        :param nick_name: A casual name of the user.  The value Bob when the user's formal name is Robert.
        :type nick_name: str
        :param name: The components of the user's real name.
        :type name: NameObject
        :param phone_numbers: A list of user's phone numbers with an indicator of primary to specify the user's main
            number.
        :type phone_numbers: list[UserPhoneNumber]
        :param photos: A list of photos for the user that represent a thing the user has.
        :type photos: list[PhotoObject]
        :param addresses: User's physical mailing address.
        :type addresses: list[PutUserAddresses]
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.  The
            primary email address must be the same value as the user's userName.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extension
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user:
        PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: The Cisco extension of SCIM 2.
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: WebexUser
        :rtype: :class:`ScimUser`
        """
        raise NotImplementedError('SCIM2UsersApi.create_a_user')
        body = dict()
        body['schemas'] = schemas
        body['userName'] = user_name
        body['userType'] = enum_str(user_type)
        body['title'] = title
        body['active'] = active
        body['preferredLanguage'] = preferred_language
        body['locale'] = locale
        body['timezone'] = timezone
        body['profileUrl'] = profile_url
        body['externalId'] = external_id
        body['displayName'] = display_name
        body['nickName'] = nick_name
        body['name'] = loads(name.model_dump_json())
        body['phoneNumbers'] = loads(
            TypeAdapter(list[UserPhoneNumber]).dump_json(phone_numbers, by_alias=True, exclude_none=True))
        body['photos'] = loads(TypeAdapter(list[PhotoObject]).dump_json(photos, by_alias=True, exclude_none=True))
        body['addresses'] = loads(
            TypeAdapter(list[PutUserAddresses]).dump_json(addresses, by_alias=True, exclude_none=True))
        body['emails'] = loads(TypeAdapter(list[EmailObject]).dump_json(emails, by_alias=True, exclude_none=True))
        body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = loads(
            urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump_json())
        body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = loads(
            urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump_json())
        url = self.ep(f'{org_id}/v2/Users')
        data = super().post(url, json=body)
        r = ScimUser.model_validate(data)
        return r

    def details(self, org_id: str, user_id: str) -> ScimUser:
        """
        Get a user

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        - `Identity:SCIM`

        - `Identity:SCIM_read`

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
        :rtype: :class:`ScimUser`
        """
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().get(url)
        r = ScimUser.model_validate(data)
        return r

    def search(self, org_id: str, filter: str = None, attributes: str = None, excluded_attributes: str = None,
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

        - `Identity:SCIM`

        - `Identity:SCIM_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        <br/>

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param filter: The url encoded filter. If the value is empty, the API will return all users under the
            organization.

        The examples below show some search filters:

        - userName eq "user1@example.com"

        - userName sw "user1@example"

        - userName ew "example"

        - phoneNumbers [ type eq "mobile" and value eq "14170120"]

        - urn:scim:schemas:extension:cisco:webexidentity:2.0:User:meta.organizationId eq
        "0ae87ade-8c8a-4952-af08-318798958d0c"

        - More filter patterns, please check <a href="https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2">
        filtering </a>.
        :type filter: str
        :param attributes: A multi-valued list of strings indicating the names of resource attributes to return in the
            response, likes 'userName,department,emails'. It supports the SCIM id
            'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User,userName'. The default is empty, all
            attributes will be returned
        :type attributes: str
        :param excluded_attributes: A multi-valued list of strings indicating the names of resource attributes to be
            removed from the default set of attributes to return. The default is empty, all attributes will be
            returned
        :type excluded_attributes: str
        :param sort_by: A string indicating the attribute whose value be used to order the returned responses. Now we
            only allow 'userName, id, meta.lastModified' to sort.
        :type sort_by: str
        :param sort_order: A string indicating the order in which the 'sortBy' parameter is applied. Allowed values are
            'ascending' and 'descending'.
        :type sort_order: str
        :param start_index: An integer indicating the 1-based index of the first query result. The default is 1.
        :type start_index: str
        :param count: An integer indicating the desired maximum number of query results per page.  The default is 100.
        :type count: str
        :param return_groups: Define whether the group information needs to be returned.  The default is false.
        :type return_groups: str
        :param include_group_details: Define whether the group information with details need been returned. The default
            is false.
        :type include_group_details: str
        :param group_usage_types: Returns groups with details of the specified group type
        :type group_usage_types: str
        :rtype: :class:`SearchUserResponse`
        """
        params = {}
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

    def update_a_user_with_put(self, org_id: str, user_id: str, schemas: list[str], user_name: str,
                               user_type: UserTypeObject, title: str, active: bool, preferred_language: str,
                               locale: str, timezone: str, profile_url: str, external_id: str, display_name: str,
                               nick_name: str, phone_numbers: list[UserPhoneNumber], photos: list[PhotoObject],
                               addresses: list[PutUserAddresses], emails: list[EmailObject],
                               urn_ietf_params_scim_schemas_extension_enterprise_2_0_user:
                               PostUserUrnietfparamsscimschemasextensionenterprise20User,
                               urn_scim_schemas_extension_cisco_webexidentity_2_0_user: WebexUser) -> ScimUser:
        """
        Update a user with PUT

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `Identity:SCIM`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. Input JSON must contain schema: "urn:ietf:params:scim:schemas:core:2.0:User".

        1. Support 3 schemas :
        - "urn:ietf:params:scim:schemas:core:2.0:User"
        - "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
        - "urn:scim:schemas:extension:cisco:webexidentity:2.0:User"

        1. Unrecognized schemas (ID/section) are ignored.

        1. Read-only attributes provided as input values are ignored.

        1. User `id` will not be changed.

        1. `meta`.`created` will not be changed.

        1. The PUT API replaces the contents of the user's data with the data in the request body.  All attributes
        specified in the request body will replace all existing attributes for the userId specified in the URL.
        Should you wish to replace or change some attributes as opposed to all attributes please refer to the SCIM
        PATCH operation https://developer.webex.com/docs/api/v1/scim2-user/update-a-user-with-patch .

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param user_name: A unique identifier for the user and is used to authenticate the user in Webex.  This
            attribute must be set to the user's primary email address.  No other user in Webex may have the same
            userName value and thus this value is required to b unique within Webex.
        :type user_name: str
        :param user_type: The type of the user.
        :type user_type: UserTypeObject
        :param title: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant",
            "Engineer" etc.
        :type title: str
        :param active: A boolean value of "true" or "false" indicating whether the user is active in Webex.
        :type active: bool
        :param preferred_language: Indicates the user's preferred language.  Acceptable values for this field are based
            on the `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            code.  Examples are:

        en_US : for english spoken in the United States, fr_FR: for french spoken in France.
        :type preferred_language: str
        :param locale: The user's locale which is used to represent the user's currency, time format, and numerical
            representations.  Acceptable values for this field are based on the  `ISO-696
            <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
            letter language code followed by an _ and then the 2 letter country code.  Examples are:

        en_US : for English spoken in the United States, or fr_FR: for French spoken in France.
        :type locale: str
        :param timezone: The user's time zone specified in the `IANA timezone
            <https://nodatime.org/timezones>`_ timezone format. e.g:
            "America/Los_Angeles".
        :type timezone: str
        :param profile_url: A fully qualified URL pointing to a page representing the user's online profile.
        :type profile_url: str
        :param external_id: External identity.
        :type external_id: str
        :param display_name: The value to display or show the user's name in Webex.
        :type display_name: str
        :param nick_name: A casual name of the user.  The value Bob when the user's formal name is Robert.
        :type nick_name: str
        :param phone_numbers: A list of user's phone numbers with an indicator of primary to specify the users main
            number.
        :type phone_numbers: list[UserPhoneNumber]
        :param photos: A list of photos for the user that represent a thing the user has.
        :type photos: list[PhotoObject]
        :param addresses: A physical mailing address of user.
        :type addresses: list[PutUserAddresses]
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.  The
            primary email address must be the same value as the user's userName.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extention
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user:
        PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: cisco extention of SCIM 2
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: WebexUser
        :rtype: :class:`ScimUser`
        """
        raise NotImplementedError('SCIM2UsersApi.update_a_user_with_put')
        body = dict()
        body['schemas'] = schemas
        body['userName'] = user_name
        body['userType'] = enum_str(user_type)
        body['title'] = title
        body['active'] = active
        body['preferredLanguage'] = preferred_language
        body['locale'] = locale
        body['timezone'] = timezone
        body['profileUrl'] = profile_url
        body['externalId'] = external_id
        body['displayName'] = display_name
        body['nickName'] = nick_name
        body['phoneNumbers'] = loads(
            TypeAdapter(list[UserPhoneNumber]).dump_json(phone_numbers, by_alias=True, exclude_none=True))
        body['photos'] = loads(TypeAdapter(list[PhotoObject]).dump_json(photos, by_alias=True, exclude_none=True))
        body['addresses'] = loads(
            TypeAdapter(list[PutUserAddresses]).dump_json(addresses, by_alias=True, exclude_none=True))
        body['emails'] = loads(TypeAdapter(list[EmailObject]).dump_json(emails, by_alias=True, exclude_none=True))
        body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = loads(
            urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump_json())
        body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = loads(
            urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump_json())
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().put(url, json=body)
        r = ScimUser.model_validate(data)
        return r

    def update_a_user_with_patch(self, org_id: str, user_id: str, schemas: list[str],
                                 operations: list[PatchUserOperation]) -> ScimUser:
        """
        Update a user with PATCH

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `Identity:SCIM`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_user_admin`

        <br/>

        **Usage**:

        1. The PATCH API replaces individual attributes of the user's data in the request body.
        The PATCH api supports `add`, `remove` and `replace` operations on any individual
        attribute allowing only specific attributes of the user's object to be modified.

        1. Each operation against an attribute must be compatible with the attribute's mutability.

        1. Each PATCH operation represents a single action to be applied to the
        same SCIM resource specified by the request URI.  Operations are
        applied sequentially in the order they appear in the array.  Each
        operation in the sequence is applied to the target resource; the
        resulting resource becomes the target of the next operation.
        Evaluation continues until all operations are successfully applied or
        until an error condition is encountered.

        <br/>

        **Add operations**:

        The `add` operation is used to add a new attribute value to an existing resource.
        The operation must contain a `value` member whose content specifies the value to be added.
        The value may be a quoted value, or it may be a JSON object containing the sub-attributes of the complex
        attribute specified in the operation's `path`.
        The result of the add operation depends upon the target location indicated by `path` references:

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
        `value` attribute shall contain a list of one or more attributes that are to be replaced.

        - If the target location is a single-value attribute, the value of the attribute is replaced.

        - If the target location is a multi-valued attribute and no filter is specified, the attribute and all values
        are replaced.

        - If the target location path specifies an attribute that does not exist, the service provider shall treat the
        operation as an "add".

        - If the target location specifies a complex attribute, a set of sub-attributes SHALL be specified in the
        `value` parameter, which replaces any existing values or adds where an attribute did not previously exist.
        Sub-attributes that are not specified in the `value` parameters are left unchanged.

        - If the target location is a multi-valued attribute and a value selection ("valuePath") filter is specified
        that matches one or more values of the multi-valued attribute, then all matching record values will be
        replaced.

        - If the target location is a complex multi-valued attribute with a value selection filter ("valuePath") and a
        specific sub-attribute (e.g., "addresses[type eq "work"].streetAddress"), the matching sub-attribute of all
        matching records is replaced.

        - If the target location is a multi-valued attribute for which a value selection filter ("valuePath") has been
        supplied and no record match was made, the service provider will indicate the failure by returning HTTP status
        code 400 and a `scimType` error code of "noTarget".

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

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param user_id: Webex Identity assigned user identifier.
        :type user_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param operations: A list of patch operations.
        :type operations: list[PatchUserOperation]
        :rtype: :class:`ScimUser`
        """
        raise NotImplementedError('SCIM2UsersApi.update_a_user_with_patch')
        body = dict()
        body['schemas'] = schemas
        body['Operations'] = loads(
            TypeAdapter(list[PatchUserOperation]).dump_json(operations, by_alias=True, exclude_none=True))
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().patch(url, json=body)
        r = ScimUser.model_validate(data)
        return r

    def delete_a_user(self, org_id: str, user_id: str):
        """
        Delete a user

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `Identity:SCIM`

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
        raise NotImplementedError('SCIM2UsersApi.delete_a_user')
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        super().delete(url)
