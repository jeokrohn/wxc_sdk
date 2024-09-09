from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetLicenseDetailsIncludeAssignedTo', 'License', 'LicenseProperties', 'LicenseRequest',
           'LicenseRequestOperation', 'LicenseSiteType', 'LicensesApi', 'LicensewithUsers', 'SiteResponse',
           'SiteResponseAccountType', 'SiteUrlsRequest', 'SiteUrlsRequestAccountType', 'UserLicensesResponse',
           'Users', 'UsersType']


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
    #: example: 50
    total_units: Optional[int] = None
    #: Total number of license units consumed.
    #: example: 5
    consumed_units: Optional[int] = None
    #: Total number of license units consumed by users.
    #: example: 5
    consumed_by_users: Optional[int] = None
    #: Total number of license units consumed by workspaces.
    consumed_by_workspaces: Optional[int] = None
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    #: example: Sub-hydraOct26a
    subscription_id: Optional[str] = None
    #: The Webex Meetings site associated with this license.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None
    #: The type of site associated with this license.
    #: example: Control Hub managed site
    site_type: Optional[LicenseSiteType] = None


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
    #: Email address of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None


class LicensewithUsers(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the licensed feature.
    #: example: Meeting - Webex Meeting Center
    name: Optional[str] = None
    #: Total number of license units allocated.
    #: example: 50
    total_units: Optional[int] = None
    #: Total number of license units consumed.
    #: example: 5
    consumed_units: Optional[int] = None
    #: Total number of license units consumed by users.
    #: example: 5
    consumed_by_users: Optional[int] = None
    #: Total number of license units consumed by workspaces.
    consumed_by_workspaces: Optional[int] = None
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
    extension: Optional[str] = None


class LicenseRequest(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[LicenseRequestOperation] = None
    #: Properties for the license. Either `phoneNumber` or `extension` are mandatory for assigning Webex Calling
    #: licenses. If `phoneNumber` is not provided then `locationId` is mandatory.
    properties: Optional[LicenseProperties] = None


class SiteUrlsRequestAccountType(str, Enum):
    #: Attendee role on the siteUrl
    attendee = 'attendee'


class SiteUrlsRequest(ApiModel):
    #: Attendee access on the site.
    #: example: mysite.webex.com
    site_url: Optional[str] = None
    #: Account type. Only `attendee` type is supported. For host account, remove attendee and assign the license on
    #: that site.
    #: example: attendee
    account_type: Optional[SiteUrlsRequestAccountType] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[LicenseRequestOperation] = None


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
    #: An array of license strings that are in pending state. This is only applicable to users outside the
    #: organization.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYWJj', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWFiY2Rl']
    pending_licenses: Optional[list[str]] = None
    #: An array of `siteUrls` and their `accountType` that are in pending state. This is only applicable to users
    #: outside the organization.
    pending_site_urls: Optional[list[SiteResponse]] = None


class GetLicenseDetailsIncludeAssignedTo(str, Enum):
    user = 'user'


class LicensesApi(ApiChild, base='licenses'):
    """
    Licenses
    
    An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
    partners manage the amount of licenses provided to administrators and users. License can be assigned only by
    admins.
    
    Viewing the list of all licenses in your organization and viewing license details requires an administrator auth
    token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of `spark-admin:licenses_read`.
    
    Updating the licenses of users requires an administrator auth token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of `spark-admin:people_write`.
    
    To learn about how to allocate Hybrid Services licenses, see the `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """

    def list_licenses(self, org_id: str = None) -> list[License]:
        """
        List Licenses

        List all licenses for a given organization.  If no `orgId` is specified, the default is the organization of the
        authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :rtype: list[License]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[License]).validate_python(data['items'])
        return r

    def get_license_details(self, license_id: str, include_assigned_to: GetLicenseDetailsIncludeAssignedTo = None,
                            next: str = None, limit: int = None) -> LicensewithUsers:
        """
        Get License Details

        Shows details for a license, by ID.

        Specify the license ID in the `licenseId` parameter in the URI.
        Use the optional query parameter `includeAssignedTo` to get a list of all objects that are assigned with the
        license. The objects include but not limited to, users including external users. Long result sets will be
        split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        Response properties that are not applicable to the license will not be present in the response.

        :param license_id: The unique identifier for the license.
        :type license_id: str
        :param include_assigned_to: The type of object to whom the license is assigned to.
        :type include_assigned_to: GetLicenseDetailsIncludeAssignedTo
        :param next: List the next set of users. Applicable only if `includeAssignedTo` is populated.
        :type next: str
        :param limit: A limit on the number of users to be returned in the response. Applicable only if
            `includeAssignedTo` is populated. limit cannot be more than 300.
        :type limit: int
        :rtype: :class:`LicensewithUsers`
        """
        params = {}
        if include_assigned_to is not None:
            params['includeAssignedTo'] = enum_str(include_assigned_to)
        if next is not None:
            params['next'] = next
        if limit is not None:
            params['limit'] = limit
        url = self.ep(f'{license_id}')
        data = super().get(url, params=params)
        r = LicensewithUsers.model_validate(data)
        return r

    def assign_licenses_to_users(self, email: str = None, person_id: str = None, licenses: list[LicenseRequest] = None,
                                 site_urls: list[SiteUrlsRequest] = None, org_id: str = None) -> UserLicensesResponse:
        """
        Assign Licenses to Users

        Assign licenses and attendee `siteUrls` to existing users. Only an admin can assign licenses. Only existing
        users can be assigned a license. Assign meeting licenses to users outside your organization (Status will be
        pending until the user accepts the invite)

        At least one of the following body parameters is required to assign license to the user: `email`, `personId`.
        For Calling license assignment, properties `phoneNumber` or `extension` are required. If `phoneNumber` is not
        provided then `locationId` is mandatory.

        When assigning licenses and attendee siteUrls to a user who does not belong to the organization, the licenses
        and siteUrls remain in pending state until the user accepts them. The `pendingLicenses` and `pendingSiteUrls`
        are part of the response.

        :param email: Email address of the user.
        :type email: str
        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param licenses: An array of licenses to be assigned to the user.
        :type licenses: list[LicenseRequest]
        :param site_urls: An array of siteUrls to be assigned to the user.
        :type site_urls: list[SiteUrlsRequest]
        :param org_id: The ID of the organization to which the licenses and siteUrls belong. If not specified, the
            organization ID from the OAuth token is used.
        :type org_id: str
        :rtype: :class:`UserLicensesResponse`
        """
        body = dict()
        if email is not None:
            body['email'] = email
        if person_id is not None:
            body['personId'] = person_id
        if org_id is not None:
            body['orgId'] = org_id
        if licenses is not None:
            body['licenses'] = TypeAdapter(list[LicenseRequest]).dump_python(licenses, mode='json', by_alias=True, exclude_none=True)
        if site_urls is not None:
            body['siteUrls'] = TypeAdapter(list[SiteUrlsRequest]).dump_python(site_urls, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('users')
        data = super().patch(url, json=body)
        r = UserLicensesResponse.model_validate(data)
        return r
