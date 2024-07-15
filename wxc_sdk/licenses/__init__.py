"""
Licenses

An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
partners manage the amount of licenses provided to administrators and users. This license resource can be accessed
only by an admin.
"""
from collections.abc import Generator
from typing import Optional, List

from pydantic import Field, TypeAdapter

from ..api_child import ApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum

__all__ = ['SiteType', 'License', 'LicensesApi', 'LicenseUser', 'LicenseUserType', 'LicenseRequestOperation',
           'LicenseProperties', 'LicenseRequest', 'SiteAccountType', 'SiteUrlsRequest', 'SiteResponse',
           'UserLicensesResponse']


class SiteType(str, Enum):
    """
    Webex site type
    """
    #: the site is managed by Webex Control Hub
    control_hub = 'Control Hub managed site'
    #: the site is a linked site
    linked = 'Linked site'
    #: the site is managed by Site Administration
    site_admin = 'Site Admin managed site'


class License(ApiModel):
    """
    Webex license
    """
    #: A unique identifier for the license.
    license_id: str = Field(alias='id')
    #: Name of the licensed feature.
    name: str
    #: Total number of license units allocated.
    total_units: int
    #: Total number of license units consumed.
    consumed_units: int
    consumed_by_users: Optional[int] = None
    consumed_by_workspaces: Optional[int] = None
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    subscription_id: Optional[str] = None
    #: The Webex Meetings site associated with this license.
    site_url: Optional[str] = None
    #: The type of site associated with this license.
    site_type: Optional[SiteType] = None

    @property
    def webex_calling(self) -> bool:
        """
        is this a Webex Calling license
        """
        return any((self.webex_calling_professional, self.webex_calling_workspaces, self.webex_calling_basic))

    @property
    def webex_calling_professional(self) -> bool:
        """
        is this a Webex Calling professional license
        """
        return self.name == 'Webex Calling - Professional'

    @property
    def webex_calling_basic(self) -> bool:
        """
        is this a Webex Calling basic license
        """
        return self.name == 'Webex Calling - Basic'

    @property
    def webex_calling_workspaces(self) -> bool:
        """
        is this a Webex Calling workspace license
        """
        return self.name == 'Webex Calling - Workspaces'


class LicenseUserType(str, Enum):
    #: User resides in the license-owned organization.
    internal = 'INTERNAL'
    #: User resides outside the license-owned organization.
    external = 'EXTERNAL'


class LicenseUser(ApiModel):
    #: A unique identifier for the user.
    id: Optional[str] = None
    #: Indicates if the user is internal or external to the organization.
    type: Optional[LicenseUserType] = None
    #: The full name of the user.
    display_name: Optional[str] = None
    #: Email address of the user.
    email: Optional[str] = None


class LicenseRequestOperation(str, Enum):
    #: Remove the license from the user
    remove = 'remove'
    #: Assign the license to the user
    add = 'add'


class LicenseProperties(ApiModel):
    #: The ID of the location for this user. Applicable to Webex Calling license.
    location_id: Optional[str] = None
    #: Work phone number for the user. Applicable to Webex Calling license.
    phone_number: Optional[str] = None
    #: Webex Calling extension of the user. Applicable to Webex Calling license.
    extension: Optional[str] = None


class LicenseRequest(ApiModel):
    #: A unique identifier for the license.
    id: Optional[str] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    operation: Optional[LicenseRequestOperation] = None
    #: Properties for the license. Either `phoneNumber` or `extension` are mandatory for assigning Webex Calling
    #: licenses. If `phoneNumber` is not provided then `locationId` is mandatory.
    properties: Optional[LicenseProperties] = None


class SiteAccountType(str, Enum):
    #: Attendee account on the site.
    attendee = 'attendee'
    #: Host account on the site.
    host = 'host'


class SiteUrlsRequest(ApiModel):
    #: Attendee access on the site.
    site_url: Optional[str] = None
    #: Account type. Only `attendee` type is supported. For host account, remove attendee and assign the license on
    #: that site.
    account_type: Optional[SiteAccountType] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    operation: Optional[LicenseRequestOperation] = None


class SiteResponse(ApiModel):
    #: `siteUrl` assigned to the user.
    site_url: Optional[str] = None
    #: Account Type of the site.
    account_type: Optional[SiteAccountType] = None


class UserLicensesResponse(ApiModel):
    #: The ID of the organization to which this user belongs.
    org_id: Optional[str] = None
    #: A unique identifier for the user.
    person_id: Optional[str] = None
    #: The email address of this user.
    email: Optional[str] = None
    #: An array of license strings that are assigned to this user.
    # 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi',
    # 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LTIzNDItMGY0NTU2YWRlZXJm']
    licenses: Optional[list[str]] = None
    #: An array of `siteUrls` and their `accountType` that are assigned to this user.
    site_urls: Optional[list[SiteResponse]] = None
    #: An array of license strings that are in pending state. This is only applicable to users outside the
    #: organization.
    # 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWFiY2Rl']
    pending_licenses: Optional[list[str]] = None
    #: An array of `siteUrls` and their `accountType` that are in pending state. This is only applicable to users
    #: outside the organization.
    pending_site_urls: Optional[list[SiteResponse]] = None


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

    def list(self, org_id: str = None) -> list[License]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[License]).validate_python(data['items'])
        return r

    def details(self, license_id) -> License:
        """
        Shows details for a license, by ID.

        Response properties that are not applicable to the license will not be present in the response.

        :param license_id: The unique identifier for the license.
        :type license_id: str
        :return: license details
        :rtype: License
        """
        ep = self.ep(license_id)
        return License.model_validate(self.get(ep))

    def assigned_users(self, license_id: str, **params) -> Generator[LicenseUser, None, None]:
        """
        Get users license is assigned to, by license ID.

        Specify the license ID in the `licenseId` parameter in the URI.
        Long result sets will be
        split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param license_id: The unique identifier for the license.
        :type license_id: str
        """
        ep = self.ep(license_id)
        params['includeAssignedTo'] = 'user'
        return self.session.follow_pagination(url=ep, model=LicenseUser, item_key='users',
                                              params=params)

    def assign_licenses_to_users(self, email: str = None, person_id: str = None,
                                 licenses: List[LicenseRequest] = None, site_urls: List[SiteUrlsRequest] = None,
                                 org_id: str = None) -> UserLicensesResponse:
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

        Example:

            .. code-block:: python

                self.api.licenses.assign_licenses_to_users(
                    person_id=new_user.person_id,
                    licenses=[LicenseRequest(id=calling_license_id,
                                             properties=LicenseProperties(location_id=target_location.location_id,
                                                                          extension=extension))])

        """
        body = dict()
        if email is not None:
            body['email'] = email
        if person_id is not None:
            body['personId'] = person_id
        if org_id is not None:
            body['orgId'] = org_id
        if licenses is not None:
            body['licenses'] = TypeAdapter(list[LicenseRequest]).dump_python(licenses, mode='json', by_alias=True,
                                                                             exclude_none=True)
        if site_urls is not None:
            body['siteUrls'] = TypeAdapter(list[SiteUrlsRequest]).dump_python(site_urls, mode='json', by_alias=True,
                                                                              exclude_none=True)
        url = self.ep('users')
        data = super().patch(url, json=body)
        r = UserLicensesResponse.model_validate(data)
        return r
