from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['EmailObject', 'EmailObjectType', 'ExternalAttributeObject', 'GetUserResponse',
           'GetUserResponseUrnietfparamsscimschemasextensionenterprise20User',
           'GetUserResponseUrnscimschemasextensionciscowebexidentity20User', 'ManagedGroupsObject',
           'ManagedOrgsObject', 'ManagerResponseObject', 'NameObject', 'PatchUserOperations', 'PatchUserOperationsOp',
           'PhotoObject', 'PhotoObjectType', 'PostUserUrnietfparamsscimschemasextensionenterprise20User',
           'PostUserUrnietfparamsscimschemasextensionenterprise20UserManager',
           'PostUserUrnscimschemasextensionciscowebexidentity20User', 'PutUserAddresses', 'PutUserPhoneNumbers',
           'PutUserPhoneNumbersType', 'SCIM2UsersApi', 'SearchUserResponse', 'SipAddressObject',
           'SipAddressObjectType', 'UserTypeObject']


class PatchUserOperationsOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class PatchUserOperations(ApiModel):
    #: The operation to perform.
    #: example: add
    op: Optional[PatchUserOperationsOp] = None
    #: A string containing an attribute path describing the target of the operation.
    #: example: displayName
    path: Optional[str] = None
    #: New value.
    #: example: new displayName value
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20UserManager(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    #: example: 518-8888-888
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20UserManager] = None


class SipAddressObjectType(str, Enum):
    enterprise = 'enterprise'


class SipAddressObject(ApiModel):
    #: The sip address value.
    #: example: sipAddress value1
    value: Optional[str] = None
    #: The type of the sipAddress.
    #: example: enterprise
    type: Optional[SipAddressObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: sipAddress1 description
    display: Optional[str] = None
    #: Designate the primary sipAddress.
    #: example: True
    primary: Optional[bool] = None


class ManagedOrgsObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    #: example: 75fe2995-24f5-4831-8d2c-1c2f8255912e
    org_id: Optional[str] = None
    #: Role in the target organization for the user.
    #: example: id_full_admin
    role: Optional[str] = None


class ExternalAttributeObject(ApiModel):
    #: Source of external attribute.
    #: example: Source.1_7ddf1f2c-2985-4c37-a450-d58bbc201750
    source: Optional[str] = None
    #: Value of external attribute.
    #: example: externalAttribute1_value
    value: Optional[str] = None


class PostUserUrnscimschemasextensionciscowebexidentity20User(ApiModel):
    #: Account status of the user.
    #: example: ['element='string' content='active' attributes={'typeAttributes': ApibArray(element='array', content=[ApibString(element='string', content='fixed', attributes=None, meta=None)], attributes=None, meta=None)} meta=None']
    account_status: Optional[list[str]] = None
    #: sipAddress values for the user.
    sip_addresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managed_orgs: Optional[list[ManagedOrgsObject]] = None
    #: The extension attributes of the user. Postfix support from 1 to 15, for example,
    #: "extensionAttribute1","extensionAttribute2"..."extensionAttribute15".
    extension_attribute_: Optional[list[str]] = Field(alias='extensionAttribute*', default=None)
    #: The external attributes of the user. Postfix support from 1 to 15, for example,
    #: "externalAttribute1","externalAttribute2"..."externalAttribute15".
    external_attribute_: Optional[list[ExternalAttributeObject]] = Field(alias='externalAttribute*', default=None)


class UserTypeObject(str, Enum):
    user = 'user'
    room = 'room'
    external_calling = 'external_calling'
    calling_service = 'calling_service'


class NameObject(ApiModel):
    #: The given name of the user, or first name in most Western languages (e.g., "Sarah" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Sarah
    given_name: Optional[str] = None
    #: The family name of the user, or last name in most Western languages (e.g., "Henderson" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Henderson
    family_name: Optional[str] = None
    #: The middle name(s) of the user (e.g., "Jane" given the full name "Ms. Sarah J Henderson, III").
    #: example: Jane
    middle_name: Optional[str] = None
    #: The honorific prefix(es) of the user, or title in most Western languages (e.g., "Ms." given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Mr.
    honorific_prefix: Optional[str] = None
    #: The honorific suffix(es) of the user, or suffix in most Western languages (e.g., "III" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: III
    honorific_suffix: Optional[str] = None


class PutUserPhoneNumbersType(str, Enum):
    work = 'work'
    home = 'home'
    mobile = 'mobile'
    work_extension = 'work_extension'
    fax = 'fax'
    pager = 'pager'
    other = 'other'


class PutUserPhoneNumbers(ApiModel):
    #: phone number.
    #: example: 400 123 1234
    value: Optional[str] = None
    #: We support the following types of phone numbers: 'mobile', 'work', 'fax', 'work_extension', 'alternate1',
    #: 'alternate2'.  Alternate 1 and Alternate 2 are types inherited from Webex meeting sites.
    #: example: work
    type: Optional[PutUserPhoneNumbersType] = None
    #: A human-readable name, primarily used for display purposes.
    #: example: work phone number
    display: Optional[str] = None
    #: A Boolean value indicating the phone number premary status.
    #: example: True
    primary: Optional[bool] = None


class PhotoObjectType(str, Enum):
    photo = 'photo'
    thumbnail = 'thumbnail'
    resizable = 'resizable'


class PhotoObject(ApiModel):
    #: photo link.
    #: example: https://photos.example.com/profilephoto/72930000000Ccne/F
    value: Optional[str] = None
    #: The type of the photo
    #: example: photo
    type: Optional[PhotoObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: photo description
    display: Optional[str] = None
    #: A Boolean value indicating the photo usage status.
    #: example: True
    primary: Optional[bool] = None


class PutUserAddresses(ApiModel):
    #: address type
    #: example: work
    type: Optional[str] = None
    #: The full street address component, which may include house number, street name, P.O. box, and multi-line
    #: extended street address information. This attribute MAY contain newlines.
    #: example: 100 Universal City Plaza
    street_address: Optional[str] = None
    #: The city or locality component.
    #: example: Hollywood
    locality: Optional[str] = None
    #: The state or region component.
    #: example: CA
    region: Optional[str] = None
    #: The zip code or postal code component.
    #: example: 91608
    postal_code: Optional[str] = None
    #: The country name component.
    #: example: US
    country: Optional[str] = None


class EmailObjectType(str, Enum):
    work = 'work'
    home = 'home'
    room = 'room'
    other = 'other'


class EmailObject(ApiModel):
    #: The email address.
    #: example: user1@example.home.com
    value: Optional[str] = None
    #: The type of the email.
    #: example: home
    type: Optional[EmailObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: home email description
    display: Optional[str] = None
    #: A Boolean value indicating the email status. If the type is work and primary is true, the value must equal
    #: "userName".
    primary: Optional[bool] = None


class ManagerResponseObject(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None
    #: The value to display or show the manager's name in Webex.
    #: example: Identity Administrator
    display_name: Optional[str] = None
    #: The URI corresponding to a SCIM user that is the manager.
    #: example: http://integration.webexapis.com/identity/scim/0ae87ade-8c8a-4952-af08-318798958d0c/v2/Users/b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    _ref: Optional[str] = Field(alias='$ref', default=None)


class GetUserResponseUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    #: example: 518-8888-888
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[ManagerResponseObject] = None


class ManagedGroupsObject(ApiModel):
    #: Webex Identity assigned group identifier.
    #: example: 3936af3e-15ff-43d1-9ef5-66c569ef34f5
    group_id: Optional[str] = None
    #: Role in the target group for the user.
    #: example: location_admin
    role: Optional[str] = None


class GetUserResponseUrnscimschemasextensionciscowebexidentity20User(ApiModel):
    #: Account status of the user.
    #: example: ['element='string' content='active' attributes={'typeAttributes': ApibArray(element='array', content=[ApibString(element='string', content='fixed', attributes=None, meta=None)], attributes=None, meta=None)} meta=None']
    account_status: Optional[list[str]] = None
    #: sipAddress values for the user.
    sip_addresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managed_orgs: Optional[list[ManagedOrgsObject]] = None
    #: Groups that the user can manage.
    managed_groups: Optional[list[ManagedGroupsObject]] = None
    #: The extension attributes of the user. Postfix support from 1 to 15, for example,
    #: "extensionAttribute1","extensionAttribute2"..."extensionAttribute15".
    extension_attribute_: Optional[list[str]] = Field(alias='extensionAttribute*', default=None)
    #: The external attributes of the user. Postfix support from 1 to 15, for example,
    #: "externalAttribute1","externalAttribute2"..."externalAttribute15".
    external_attribute_: Optional[list[ExternalAttributeObject]] = Field(alias='externalAttribute*', default=None)


class GetUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    #: example: 3426a8e3-d414-4bf0-a493-4f6787632a13
    id: Optional[str] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to
    #: the user's primary email address.  No other user in Webex may have the same userName value and thus this value
    #: is required to be unique within Webex.
    #: example: user1@example.com
    user_name: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    display_name: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nick_name: Optional[str] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email
    #: address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: The type of the user.
    #: example: user
    user_type: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profile_url: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: 
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    #: example: en_US
    preferred_language: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.
    #: Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: followed by an _ and then the 2 letter country code.  Examples are:
    #: 
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: External identity.
    #: example: externalIdValue
    external_id: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: SCIM2 enterprise extension
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[GetUserResponseUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[GetUserResponseUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)


class SearchUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:ListResponse']
    schemas: Optional[list[str]] = None
    #: Total number of users in search results.
    #: example: 2
    total_results: Optional[int] = None
    #: The total number of items in a paged result.
    #: example: 2
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching users.
    #: example: 1
    start_index: Optional[int] = None
    #: A list of users with details.
    resources: Optional[list[GetUserResponse]] = Field(alias='Resources', default=None)


class SCIM2UsersApi(ApiChild, base='identity/scim'):
    """
    SCIM 2 Users
    
    Implementation of the SCIM 2.0 user part for user management in a standards based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition with detailed in
    `SCIM 2.0 schema
    <https://datatracker.ietf.org/doc/html/rfc7643>`_ and `SCIM 2.0 Protocol
    """

    def create_a_user(self, org_id: str, schemas: list[str], user_name: str, user_type: UserTypeObject, title: str,
                      active: bool, preferred_language: str, locale: str, timezone: str, profile_url: str,
                      external_id: str, display_name: str, nick_name: str, name: NameObject,
                      phone_numbers: list[PutUserPhoneNumbers], photos: list[PhotoObject],
                      addresses: list[PutUserAddresses], emails: list[EmailObject],
                      urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User,
                      urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User) -> GetUserResponse:
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
        :type phone_numbers: list[PutUserPhoneNumbers]
        :param photos: A list of photos for the user that represent a thing the user has.
        :type photos: list[PhotoObject]
        :param addresses: User's physical mailing address.
        :type addresses: list[PutUserAddresses]
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.  The
            primary email address must be the same value as the user's userName.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extension
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: The Cisco extension of SCIM 2.
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User
        :rtype: :class:`GetUserResponse`
        """
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
        body['name'] = name.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['phoneNumbers'] = TypeAdapter(list[PutUserPhoneNumbers]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        body['photos'] = TypeAdapter(list[PhotoObject]).dump_python(photos, mode='json', by_alias=True, exclude_none=True)
        body['addresses'] = TypeAdapter(list[PutUserAddresses]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        body['emails'] = TypeAdapter(list[EmailObject]).dump_python(emails, mode='json', by_alias=True, exclude_none=True)
        body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users')
        data = super().post(url, json=body)
        r = GetUserResponse.model_validate(data)
        return r

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
        :param filter: The url encoded filter. If the value is empty, the API will return all users under the
            organization.

        The examples below show some search filters:

        - userName eq "user1@example.com"

        - userName sw "user1@example"

        - userName ew "example"

        - phoneNumbers [ type eq "mobile" and value eq "14170120"]

        - urn:scim:schemas:extension:cisco:webexidentity:2.0:User:meta.organizationId eq
        "0ae87ade-8c8a-4952-af08-318798958d0c"

        - More filter patterns, please check `filtering
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
                               nick_name: str, phone_numbers: list[PutUserPhoneNumbers], photos: list[PhotoObject],
                               addresses: list[PutUserAddresses], emails: list[EmailObject],
                               urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User,
                               urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User) -> GetUserResponse:
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
        :type phone_numbers: list[PutUserPhoneNumbers]
        :param photos: A list of photos for the user that represent a thing the user has.
        :type photos: list[PhotoObject]
        :param addresses: A physical mailing address of user.
        :type addresses: list[PutUserAddresses]
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.  The
            primary email address must be the same value as the user's userName.
        :type emails: list[EmailObject]
        :param urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: SCIM2 enterprise extention
        :type urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: PostUserUrnietfparamsscimschemasextensionenterprise20User
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_user: cisco extention of SCIM 2
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_user: PostUserUrnscimschemasextensionciscowebexidentity20User
        :rtype: :class:`GetUserResponse`
        """
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
        body['phoneNumbers'] = TypeAdapter(list[PutUserPhoneNumbers]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        body['photos'] = TypeAdapter(list[PhotoObject]).dump_python(photos, mode='json', by_alias=True, exclude_none=True)
        body['addresses'] = TypeAdapter(list[PutUserAddresses]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        body['emails'] = TypeAdapter(list[EmailObject]).dump_python(emails, mode='json', by_alias=True, exclude_none=True)
        body['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = urn_ietf_params_scim_schemas_extension_enterprise_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['urn:scim:schemas:extension:cisco:webexidentity:2.0:User'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_user.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().put(url, json=body)
        r = GetUserResponse.model_validate(data)
        return r

    def update_a_user_with_patch(self, org_id: str, user_id: str, schemas: list[str],
                                 operations: list[PatchUserOperations]) -> GetUserResponse:
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

        1. The PATCH API replaces individual attributes of the user's data in the request body.
        The PATCH api supports `add`, `remove` and `replace` operations on any individual
        attribute allowing only specific attributes of the user's object to be modified.

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
        :type operations: list[PatchUserOperations]
        :rtype: :class:`GetUserResponse`
        """
        body = dict()
        body['schemas'] = schemas
        body['Operations'] = TypeAdapter(list[PatchUserOperations]).dump_python(operations, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Users/{user_id}')
        data = super().patch(url, json=body)
        r = GetUserResponse.model_validate(data)
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
