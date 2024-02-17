from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Organization', 'OrganizationsWithXsiApi']


class Organization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Full name of the organization.
    #: example: Acme, Inc.
    display_name: Optional[str] = None
    #: The date and time the organization was created.
    #: example: 2019-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The base path to xsi-actions.
    #: example: https://api-us.bcld.webex.com/com.broadsoft.xsi-actions
    xsi_actions_endpoint: Optional[str] = None
    #: The base path to xsi-events.
    #: example: https://api-us.bcld.webex.com/com.broadsoft.xsi-events
    xsi_events_endpoint: Optional[str] = None
    #: The base path to xsi-events-channel.
    #: example: https://api-us.bcld.webex.com/com.broadsoft.async/com.broadsoft.xsi-events
    xsi_events_channel_endpoint: Optional[str] = None
    #: `api-` prepended to the `bcBaseDomain` value for the organization.
    #: example: api-us.bcld.webex.com
    xsi_domain: Optional[str] = None


class OrganizationsWithXsiApi(ApiChild, base='organizations'):
    """
    Organizations with Xsi
    
    A set of people in Webex. Organizations may manage other organizations or be managed themselves. This organizations
    resource can be accessed only by an admin.
    """

    def list_organizations(self, calling_data: bool = None) -> list[Organization]:
        """
        List Organizations

        List all organizations visible by your account.

        If the `callingData` parameter is set to `true` and the base domain (region where the organization is
        provisioned) is non-null, then the XSI endpoint values will be included in the organization details.

        :param calling_data: Include XSI endpoint values in the response (if applicable) for the organization.
        :type calling_data: bool
        :rtype: list[Organization]
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Organization]).validate_python(data['items'])
        return r

    def get_organization_details(self, org_id: str, calling_data: bool = None) -> Organization:
        """
        Get Organization Details

        Shows details for an organization, by ID.

        Specify the org ID in the `orgId` parameter in the URI.

        If the `callingData` parameter is set to `true` and the base domain (region where the organization is
        provisioned) is non-null, then the XSI endpoint values will be included in the organization details.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :param calling_data: Include XSI endpoint values in the response (if applicable) for the organization.
        :type calling_data: bool
        :rtype: :class:`Organization`
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{org_id}')
        data = super().get(url, params=params)
        r = Organization.model_validate(data)
        return r
