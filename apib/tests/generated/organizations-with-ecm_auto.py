from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Organization', 'OrganizationSupportedContentType', 'OrganizationsWithECMApi']


class OrganizationSupportedContentType(str, Enum):
    #: Only Webex content storage.
    native = 'native'
    #: Only ECM storage.
    external = 'external'
    #: Both Webex and ECM storage.
    hybrid = 'hybrid'


class Organization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Full name of the organization.
    #: example: Acme, Inc.
    display_name: Optional[str] = None
    #: The current Enterprise Content Management setting for the organization.
    #: example: hybrid
    supported_content_type: Optional[OrganizationSupportedContentType] = None
    #: The date and time the organization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class OrganizationsWithECMApi(ApiChild, base='organizations'):
    """
    Organizations with ECM
    
    A set of people in Webex. Organizations may manage other organizations or be managed themselves. Organizations
    resources can be accessed only by an admin.
    """

    def list_organizations(self) -> list[Organization]:
        """
        List Organizations

        List all organizations visible by your account. The results will not be `paginated
        <https://developer.webex.com/docs/basics#pagination>`_.

        :rtype: list[Organization]
        """
        url = self.ep()
        data = super().get(url)
        r = TypeAdapter(list[Organization]).validate_python(data['items'])
        return r

    def get_organization_details(self, org_id: str) -> Organization:
        """
        Get Organization Details

        Shows details for an organization, by ID.

        Specify the org ID in the `orgId` parameter in the URI.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`Organization`
        """
        url = self.ep(f'{org_id}')
        data = super().get(url)
        r = Organization.model_validate(data)
        return r
