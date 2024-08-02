from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ResourceGroupMembership', 'ResourceGroupMembershipStatus', 'ResourceGroupMembershipsApi']


class ResourceGroupMembershipStatus(str, Enum):
    #: activation pending
    pending = 'pending'
    #: activated
    activated = 'activated'
    #: error present
    error = 'error'


class ResourceGroupMembership(ApiModel):
    #: A unique identifier for the resource group membership.
    #: example: Y2lzY29zcGFyazovL3VzL1JFU09VUkNFX0dST1VQX01FTUJFUlNISVAvcGVyc29uSWQ6bGljZW5zZUlk
    id: Optional[str] = None
    #: The resource group ID.
    #: example: Y2lzY29zcGFyazovL3VzL1JFU09VUkNFX0dST1VQL2RlZmF1bHQ
    resource_group_id: Optional[str] = None
    #: The license ID.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMWNjYmJjMTctZDYxNi00ZDc0LTg2NGItYjFmM2IwNzAxZmJhOk1TXzAzMDRjMDkzLTFjM2MtNDRlMC1iYjBhLWU1ZDE2NDM2NmQ1OQ
    license_id: Optional[str] = None
    #: The person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The organization ID of the person.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    person_org_id: Optional[str] = None
    #: The activation status of the resource group membership.
    #: example: activated
    status: Optional[ResourceGroupMembershipStatus] = None


class ResourceGroupMembershipsApi(ApiChild, base='resourceGroup/memberships'):
    """
    Resource Group Memberships
    
    Resource Group Memberships represent a person's relationship to a Resource Group for a particular `Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_
    license. Users assigned a new license will be automatically placed in a "default" Resource Group. Use this API to
    list memberships for all people in an organization or update memberships to use a different Resource Group.
    
    Searching and viewing Resource Group Memberships requires an administrator auth token with the
    `spark-admin:resource_group_memberships_read` scope. Updating memberships requires an administrator auth token
    with the `spark-admin:resource_group_memberships_write` scope.
    
    To manage Resource Groups, see the `Resource Groups API
    <https://developer.webex.com/docs/api/v1/resource-groups>`_. For more information about Resource Groups, see the
    `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """

    def list_resource_group_memberships(self, license_id: str = None, person_id: str = None, person_org_id: str = None,
                                        status: ResourceGroupMembershipStatus = None,
                                        **params) -> Generator[ResourceGroupMembership, None, None]:
        """
        List Resource Group Memberships

        Lists all resource group memberships for an organization.

        Use query parameters to filter the response.

        :param license_id: List resource group memberships for a license, by ID.
        :type license_id: str
        :param person_id: List resource group memberships for a person, by ID.
        :type person_id: str
        :param person_org_id: List resource group memberships for an organization, by ID.
        :type person_org_id: str
        :param status: Limit resource group memberships to a specific status.
        :type status: ResourceGroupMembershipStatus
        :return: Generator yielding :class:`ResourceGroupMembership` instances
        """
        if license_id is not None:
            params['licenseId'] = license_id
        if person_id is not None:
            params['personId'] = person_id
        if person_org_id is not None:
            params['personOrgId'] = person_org_id
        if status is not None:
            params['status'] = enum_str(status)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ResourceGroupMembership, item_key='items', params=params)

    def get_resource_group_membership_details(self, resource_group_membership_id: str) -> ResourceGroupMembership:
        """
        Get Resource Group Membership Details

        Shows details for a resource group membership, by ID.

        Specify the resource group membership ID in the `resourceGroupMembershipId` URI parameter.

        :param resource_group_membership_id: The unique identifier for the resource group membership.
        :type resource_group_membership_id: str
        :rtype: :class:`ResourceGroupMembership`
        """
        url = self.ep(f'{resource_group_membership_id}')
        data = super().get(url)
        r = ResourceGroupMembership.model_validate(data)
        return r

    def update_a_resource_group_membership(self, resource_group_membership_id: str, resource_group_id: str,
                                           license_id: str, person_id: str, person_org_id: str,
                                           status: ResourceGroupMembershipStatus) -> ResourceGroupMembership:
        """
        Update a Resource Group Membership

        Updates a resource group membership, by ID.

        Specify the resource group membership ID in the `resourceGroupMembershipId` URI parameter.

        Only the `resourceGroupId` can be changed with this action. Resource group memberships with a `status` of
        "pending" cannot be updated. For more information about resource group memberships, see the
        `Managing Hybrid Services
        <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses#webex-resource-groups>`_ guide.

        :param resource_group_membership_id: The unique identifier for the resource group membership.
        :type resource_group_membership_id: str
        :param resource_group_id: The resource group ID.
        :type resource_group_id: str
        :param license_id: The license ID.
        :type license_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_org_id: The organization ID of the person.
        :type person_org_id: str
        :param status: The activation status of the resource group membership.
        :type status: ResourceGroupMembershipStatus
        :rtype: :class:`ResourceGroupMembership`
        """
        body = dict()
        body['resourceGroupId'] = resource_group_id
        body['licenseId'] = license_id
        body['personId'] = person_id
        body['personOrgId'] = person_org_id
        body['status'] = enum_str(status)
        url = self.ep(f'{resource_group_membership_id}')
        data = super().put(url, json=body)
        r = ResourceGroupMembership.model_validate(data)
        return r
