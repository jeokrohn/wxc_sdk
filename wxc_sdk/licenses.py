"""
Licenses

An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
partners manage the amount of licenses provided to administrators and users. This license resource can be accessed
only by an admin.
"""
from collections.abc import Generator
from enum import Enum
from typing import Optional

from pydantic import Field

from .api_child import ApiChild
from .base import ApiModel

__all__ = ['SiteType', 'License', 'LicensesApi']


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
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    subscription_id: Optional[str]
    #: The Webex Meetings site associated with this license.
    site_url: Optional[str]
    #: The type of site associated with this license.
    site_type: Optional[SiteType]

    @property
    def webex_calling(self) -> bool:
        """
        is this a Webex Calling license
        """
        return any((self.webex_calling_professional, self.webex_calling_workspaces, self.webex_calling_basic))

    @property
    def webex_calling_professional(self) -> bool:
        return self.name == 'Webex Calling - Professional'

    @property
    def webex_calling_basic(self) -> bool:
        return self.name == 'Webex Calling - Basic'

    @property
    def webex_calling_workspaces(self) -> bool:
        return self.name == 'Webex Calling - Workspaces'


class LicensesApi(ApiChild, base='licenses'):
    """
    Licenses

    An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
    partners manage the amount of licenses provided to administrators and users. This license resource can be accessed
    only by an admin.
    """

    def list(self, org_id: str = None) -> Generator[License, None, None]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=License, params=params)

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
        return License.parse_obj(self.get(ep))
