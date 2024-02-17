from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Organization', 'OrganizationsApi']


class Organization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Full name of the organization.
    #: example: Acme, Inc.
    display_name: Optional[str] = None
    #: The date and time the organization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class OrganizationsApi(ApiChild, base='organizations'):
    """
    Organizations
    
    A set of people in Webex. Organizations may manage other organizations or be managed themselves. This organizations
    resource can be accessed only by an admin.
    
    Applications can delete an Organization only after they have been authorized by a user with the
    `Full Administrator Role
    <https://help.webex.com/en-us/fs78p5/Assign-Organization-Account-Roles-in-Cisco-Webex-Control-Hub#id_117864>`_ which may be a user in the customer org or a user in a managing partner organization to
    which the role has been granted. The authorizing admin must grant the `spark-admin:organizations-write` scope.
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

    def delete_organization(self, org_id: str):
        """
        Delete Organization

        Deletes an organization, by ID. It may take up to 10 minutes for the organization to be deleted after the
        response is returned.
        <br/><br/>
        Specify the org ID in the `orgId` parameter in the URI.

        <div><Callout type="warning">Deleting your organization permanently deletes all of the information associated
        with your organization and is irreversible.</Callout></div>

        Deleting an Organization may fail with a HTTP 409 Conflict response and encounter one or more of the errors
        described below. Resolve these conditions to allow the delete to succeed.
        <br/><br/>

        + Org cannot be deleted as it has Linked sites.

        + Org cannot be deleted as it has active subscriptions or licenses.

        + Org cannot be deleted as `Directory Synchronization
        <https://developer.webex.com/docs/api/v1/broadworks-enterprises/get-directory-sync-status-for-an-enterprise>`_ is enabled.

        + Org cannot be deleted as it has more than 1 user.

        + Org cannot be deleted as it has more than 1 managed by relationship.

        + Org cannot be deleted as it has managed orgs.

        <div>
        <Callout type='info'>When deleting a Webex for BroadWorks Organization with BroadWorks Directory
        Synchronization enabled, a prerequisite is to disable BroadWorks Directory Synchronization for the given
        Organization. Refer to the `Organization Deletion
        <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#organization-deletion>`_ section of the `Webex for BroadWorks
        information.</Callout>
        </div>

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}')
        super().delete(url)
