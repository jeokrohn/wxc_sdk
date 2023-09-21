from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['License', 'LicenseCollectionResponse', 'LicenseProperties', 'LicenseRequest', 'LicenseRequestOperation', 'LicenseSiteType', 'LicenseWithUsers', 'PatchUserLicenses', 'SiteResponse', 'SiteResponseAccountType', 'SiteUrlsRequest', 'SiteUrlsRequestAccountType', 'UserLicensesResponse', 'Users', 'UsersType']


class LicenseSiteType(str, Enum):
    #: The site is managed by Webex Control Hub.
    control_hub_managed_site = 'Control Hub managed site'
    #: The site is a linked site.
    linked_site = 'Linked site'
    #: The site is managed by Site Administration.
    site_admin_managed_site = 'Site Admin managed site'


class License(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the licensed feature.
    #: example: Meeting - Webex Meeting Center
    name: Optional[str] = None
    #: Total number of license units allocated.
    #: example: 50.0
    total_units: Optional[int] = None
    #: Total number of license units consumed.
    #: example: 5.0
    consumed_units: Optional[int] = None
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    #: example: Sub-hydraOct26a
    subscription_id: Optional[str] = None
    #: The Webex Meetings site associated with this license.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None
    #: The type of site associated with this license.
    #: example: Control Hub managed site
    site_type: Optional[LicenseSiteType] = None


class LicenseCollectionResponse(ApiModel):
    items: Optional[list[License]] = None


class UsersType(str, Enum):
    #: User resides in the license-owned organization.
    internal = 'INTERNAL'
    #: User resides outside the license-owned organization.
    external = 'EXTERNAL'


class Users(ApiModel):
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    id: Optional[str] = None
    #: Indicates if the user is internal or external to the organization.
    #: example: INTERNAL
    type: Optional[UsersType] = None
    #: The full name of the user.
    #: example: John Andersen
    display_name: Optional[str] = None


class LicenseWithUsers(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the licensed feature.
    #: example: Meeting - Webex Meeting Center
    name: Optional[str] = None
    #: Total number of license units allocated.
    #: example: 50.0
    total_units: Optional[int] = None
    #: Total number of license units consumed.
    #: example: 5.0
    consumed_units: Optional[int] = None
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    #: example: Sub-hydraOct26a
    subscription_id: Optional[str] = None
    #: The Webex Meetings site associated with this license.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None
    #: The type of site associated with this license.
    #: example: Control Hub managed site
    site_type: Optional[LicenseSiteType] = None
    #: A list of users to whom the license is assigned to.
    users: Optional[list[Users]] = None


class LicenseRequestOperation(str, Enum):
    #: Remove the license from the user
    remove = 'remove'
    #: Assign the license to the user
    add = 'add'


class LicenseProperties(ApiModel):
    #: The ID of the location for this user. Applicable to Webex Calling license.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzYzNzE1
    location_id: Optional[str] = None
    #: Work phone number for the user. Applicable to Webex Calling license.
    #: example: 14085267209
    phone_number: Optional[str] = None
    #: Webex Calling extension of the user. Applicable to Webex Calling license.
    #: example: 133
    extension: Optional[datetime] = None


class LicenseRequest(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[LicenseRequestOperation] = None
    #: Properties for the license. Either `phoneNumber` or `extension` are mandatory for assigning Webex Calling licenses. If `phoneNumber` is not provided then `locationId` is mandatory.
    properties: Optional[LicenseProperties] = None


class SiteUrlsRequestAccountType(str, Enum):
    #: Attendee role on the siteUrl
    attendee = 'attendee'


class SiteUrlsRequest(ApiModel):
    #: Attendee access on the site.
    #: example: mysite.webex.com
    site_url: Optional[str] = None
    #: Account type. Only `attendee` type is supported. For host account, remove attendee and assign the license on that site.
    #: example: attendee
    account_type: Optional[SiteUrlsRequestAccountType] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[LicenseRequestOperation] = None


class PatchUserLicenses(ApiModel):
    #: Email address of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The ID of the organization to which the licenses and siteUrls belong. If not specified, the organization ID from the OAuth token is used.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: An array of licenses to be assigned to the user.
    licenses: Optional[list[LicenseRequest]] = None
    #: An array of siteUrls to be assigned to the user.
    site_urls: Optional[list[SiteUrlsRequest]] = None


class SiteResponseAccountType(str, Enum):
    #: Attendee account on the site.
    attendee = 'attendee'
    #: Host account on the site.
    host = 'host'


class SiteResponse(ApiModel):
    #: `siteUrl` assigned to the user.
    #: example: mysite.webex.com
    site_url: Optional[str] = None
    #: Account Type of the site.
    #: example: attendee
    account_type: Optional[SiteResponseAccountType] = None


class UserLicensesResponse(ApiModel):
    #: The ID of the organization to which this user belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of this user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: An array of license strings that are assigned to this user.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LTIzNDItMGY0NTU2YWRlZXJm']
    licenses: Optional[list[str]] = None
    #: An array of `siteUrls` and their `accountType` that are assigned to this user.
    site_urls: Optional[list[SiteResponse]] = None
    #: An array of license strings that are in pending state. This is only applicable to users outside the organization.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYWJj', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWFiY2Rl']
    pending_licenses: Optional[list[str]] = None
    #: An array of `siteUrls` and their `accountType` that are in pending state. This is only applicable to users outside the organization.
    pending_site_urls: Optional[list[SiteResponse]] = None
