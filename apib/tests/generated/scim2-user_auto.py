from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['EmailObject', 'EmailObjectType', 'GetUserResponse', 'GetUserResponseUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'ManagedGroupObject', 'ManagedOrgsObject', 'ManagedSitesObject', 'ManagerResponseObject', 'NameObject', 'PatchUser', 'PatchUserOperations', 'PatchUserOperationsOp', 'PhotoObject', 'PhotoObjectType', 'PostUser', 'PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:UserManager', 'PostUserUrn:scim:schemas:extension:cisco:webexidentity:2.0:User', 'PutUser', 'PutUserAddresses', 'PutUserPhoneNumbers', 'PutUserPhoneNumbersType', 'RoleObject', 'RoleObjectType', 'SearchUserResponse', 'SipAddressObject', 'SipAddressObjectType', 'UserTypeObject']


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


class PatchUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:PatchOp']
    schemas: Optional[list[str]] = None
    #: A list of patch operations.
    Operations: Optional[list[PatchUserOperations]] = None


class PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:UserManager(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None


class PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    costCenter: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an organization.
    #: example: 518-8888-888
    employeeNumber: Optional[str] = None
    #: The user's manager.
    manager: Optional[PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:UserManager] = None


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
    orgId: Optional[str] = None
    #: Role in the target organization for the user.
    #: example: id_full_admin
    role: Optional[str] = None


class ManagedGroupObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    #: example: 153ced48-d2d1-4369-86fd-9b9fade218ff
    orgId: Optional[str] = None
    #: A unique identifier for the group.
    #: example: 1929effd-b750-43d6-be0d-7dcdaac38e92
    groupId: Optional[str] = None
    #: Role in the target organization for the user.
    #: example: location_full_admin
    role: Optional[str] = None


class ManagedSitesObject(ApiModel):
    #: Managed site name.
    #: example: admintrainSiteName1.webex.com
    siteName: Optional[str] = None
    #: Role in the managed site for the user.
    #: example: full_admin
    role: Optional[str] = None


class PostUserUrn:scim:schemas:extension:cisco:webexidentity:2.0:User(ApiModel):
    #: Account status of the user.
    #: example: ['element='string' content='active' attributes={'typeAttributes': ApibArray(element='array', content=[ApibString(element='string', content='fixed', attributes=None, meta=None)], attributes=None, meta=None)} meta=None']
    accountStatus: Optional[list[str]] = None
    #: sipAddress values for the user.
    sipAddresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managedOrgs: Optional[list[ManagedOrgsObject]] = None
    #: Groups that the user can manage.
    managedGroups: Optional[list[ManagedGroupObject]] = None
    #: Sites that the user can manage.
    managedSites: Optional[list[ManagedSitesObject]] = None


class UserTypeObject(str, Enum):
    user = 'user'
    room = 'room'
    external_calling = 'external_calling'
    calling_service = 'calling_service'


class NameObject(ApiModel):
    #: The given name of the user, or first name in most Western languages (e.g., "Sarah" given the full name "Ms. Sarah J Henderson, III").
    #: example: Sarah
    givenName: Optional[str] = None
    #: The family name of the user, or last name in most Western languages (e.g., "Henderson" given the full name "Ms. Sarah J Henderson, III").
    #: example: Henderson
    familyName: Optional[str] = None
    #: The middle name(s) of the user (e.g., "Jane" given the full name "Ms. Sarah J Henderson, III").
    #: example: Jane
    middleName: Optional[str] = None
    #: The honorific prefix(es) of the user, or title in most Western languages (e.g., "Ms." given the full name "Ms. Sarah J Henderson, III").
    #: example: Mr.
    honorificPrefix: Optional[str] = None
    #: The honorific suffix(es) of the user, or suffix in most Western languages (e.g., "III" given the full name "Ms. Sarah J Henderson, III").
    #: example: III
    honorificSuffix: Optional[str] = None


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
    #: We support the following types of phone numbers: 'mobile', 'work', 'fax', 'work_extension', 'alternate1', 'alternate2'.  Alternate 1 and Alternate 2 are types inherited from Webex meeting sites.
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
    #: The full street address component, which may include house number, street name, P.O. box, and multi-line extended street address information. This attribute MAY contain newlines.
    #: example: 100 Universal City Plaza
    streetAddress: Optional[str] = None
    #: The city or locality component.
    #: example: Hollywood
    locality: Optional[str] = None
    #: The state or region component.
    #: example: CA
    region: Optional[str] = None
    #: The zip code or postal code component.
    #: example: 91608
    postalCode: Optional[str] = None
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
    #: A Boolean value indicating the email status. If the type is work and primary is true, the value must equal "userName".
    primary: Optional[bool] = None


class RoleObjectType(str, Enum):
    #: Webex Identity roles: "id_full_admin", "id_user_admin", "id_readonly_admin", "id_device_admin".
    cirole = 'cirole'
    #: service registered role.
    servicerole = 'servicerole'


class RoleObject(ApiModel):
    #: The role value.
    #: example: id_full_admin
    value: Optional[str] = None
    #: The type of the role.
    #: example: cirole
    type: Optional[RoleObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: role description
    display: Optional[str] = None


class PostUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to the user's primary email address.  No other user in Webex may have the same userName value and thus this value is required to be unique within Webex.
    #: example: user1@example.com
    userName: Optional[str] = None
    #: The type of the user.
    #: example: user
    userType: Optional[UserTypeObject] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    #: example: en_US
    preferredLanguage: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.  Acceptable values for this field are based on the [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: The user's time zone specified in the [IANA timezone](https://nodatime.org/timezones) timezone format, for example, "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profileUrl: Optional[str] = None
    #: External identity.
    #: example: externalIdValue
    externalId: Optional[str] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    displayName: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nickName: Optional[str] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phoneNumbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: A list of roles for the user that collectively represent who the user is.
    roles: Optional[list[RoleObject]] = None
    #: SCIM2 enterprise extension
    urn:ietf:params:scim:schemas:extension:enterprise:2.0:User: Optional[PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User] = None
    #: The Cisco extension of SCIM 2.
    urn:scim:schemas:extension:cisco:webexidentity:2.0:User: Optional[PostUserUrn:scim:schemas:extension:cisco:webexidentity:2.0:User] = None


class PutUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to the user's primary email address.  No other user in Webex may have the same userName value and thus this value is required to b unique within Webex.
    #: example: user1Changed@example.com
    userName: Optional[str] = None
    #: The type of the user.
    #: example: user
    userType: Optional[UserTypeObject] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United States, fr_FR: for french spoken in France.
    #: example: en_US
    preferredLanguage: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.  Acceptable values for this field are based on the  [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States, or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: The user's time zone specified in the [IANA timezone](https://nodatime.org/timezones) timezone format. e.g: "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profileUrl: Optional[str] = None
    #: External identity.
    #: example: externalIdNewValue
    externalId: Optional[str] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    displayName: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nickName: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the users main number.
    phoneNumbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: A physical mailing address of user.
    addresses: Optional[list[PutUserAddresses]] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: A list of roles for the user that collectively represent who the user is.
    roles: Optional[list[RoleObject]] = None
    #: SCIM2 enterprise extention
    urn:ietf:params:scim:schemas:extension:enterprise:2.0:User: Optional[PostUserUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User] = None
    #: cisco extention of SCIM 2
    urn:scim:schemas:extension:cisco:webexidentity:2.0:User: Optional[PostUserUrn:scim:schemas:extension:cisco:webexidentity:2.0:User] = None


class ManagerResponseObject(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None
    #: The value to display or show the manager's name in Webex.
    #: example: Identity Administrator
    displayName: Optional[str] = None
    #: The URI corresponding to a SCIM user that is the manager.
    #: example: http://integration.webexapis.com/identity/scim/0ae87ade-8c8a-4952-af08-318798958d0c/v2/Users/b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    $ref: Optional[str] = None


class GetUserResponseUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    costCenter: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an organization.
    #: example: 518-8888-888
    employeeNumber: Optional[str] = None
    #: The user's manager.
    manager: Optional[ManagerResponseObject] = None


class GetUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    #: example: 3426a8e3-d414-4bf0-a493-4f6787632a13
    id: Optional[str] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to the user's primary email address.  No other user in Webex may have the same userName value and thus this value is required to be unique within Webex.
    #: example: user1@example.com
    userName: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: A list of roles for the user that collectively represent who the user is.
    roles: Optional[list[RoleObject]] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    displayName: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nickName: Optional[str] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: The type of the user.
    #: example: user
    userType: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profileUrl: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    #: example: en_US
    preferredLanguage: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.  Acceptable values for this field are based on the [ISO-696](http://www.loc.gov/standards/iso639-2/php/code_list.php) and [ISO-3166](https://www.iso.org/obp/ui/#search) with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: External identity.
    #: example: externalIdValue
    externalId: Optional[str] = None
    #: The user's time zone specified in the [IANA timezone](https://nodatime.org/timezones) timezone format, for example, "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phoneNumbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: SCIM2 enterprise extension
    urn:ietf:params:scim:schemas:extension:enterprise:2.0:User: Optional[GetUserResponseUrn:ietf:params:scim:schemas:extension:enterprise:2.0:User] = None
    #: The Cisco extension of SCIM 2.
    urn:scim:schemas:extension:cisco:webexidentity:2.0:User: Optional[PostUserUrn:scim:schemas:extension:cisco:webexidentity:2.0:User] = None


class SearchUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:ListResponse']
    schemas: Optional[list[str]] = None
    #: Total number of users in search results.
    #: example: 2.0
    totalResults: Optional[int] = None
    #: The total number of items in a paged result.
    #: example: 2.0
    itemsPerPage: Optional[int] = None
    #: Start at the one-based offset in the list of matching users.
    #: example: 1.0
    startIndex: Optional[int] = None
    #: A list of users with details.
    Resources: Optional[list[GetUserResponse]] = None
