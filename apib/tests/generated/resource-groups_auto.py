from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ResourceGroup', 'ResourceGroupsApi']


class ResourceGroup(ApiModel):
    #: A unique identifier for the resource group.
    #: example: Y2lzY29zcGFyazovL3VzL1JFU09VUkNFX0dST1VQL2RlZmF1bHQ
    id: Optional[str] = None
    #: A user-friendly name for the resource group.
    #: example: Resource Group 1
    name: Optional[str] = None
    #: The ID of the organization to which this resource group belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None


class ResourceGroupsApi(ApiChild, base='resourceGroups'):
    """
    Resource Groups
    
    Resource Groups are collections of on-premise clusters which provide `Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ to a particular subset of
    people in an organization. If a person has a Hybrid Services license associated with their account, they will be
    associated with a resource group to use specific on-premise clusters for that service.
    
    Searching and viewing Resource Groups requires an administrator auth token with a scope of
    `spark-admin:resource_groups_read`.
    
    To manage the people associated with Resource Groups, see the `Resource Group Memberships API
    <https://developer.webex.com/docs/api/v1/resource-group-memberships>`_. For more information
    about Resource Groups, see the `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """

    def list_resource_groups(self, org_id: str = None) -> list[ResourceGroup]:
        """
        List resource groups.

        Use query parameters to filter the response.

        :param org_id: List resource groups in this organization. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :rtype: list[ResourceGroup]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ResourceGroup]).validate_python(data['items'])
        return r

    def get_resource_group_details(self, resource_group_id: str) -> ResourceGroup:
        """
        Get Resource Group Details

        Shows details for a resource group, by ID.

        Specify the resource group ID in the `resourceGroupId` parameter in the URI.

        :param resource_group_id: The unique identifier for the resource group.
        :type resource_group_id: str
        :rtype: :class:`ResourceGroup`
        """
        url = self.ep(f'{resource_group_id}')
        data = super().get(url)
        r = ResourceGroup.model_validate(data)
        return r
