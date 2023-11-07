from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ResourceGroup', 'ResourceGroupCollectionResponse']


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


class ResourceGroupCollectionResponse(ApiModel):
    items: Optional[list[ResourceGroup]] = None


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
    ...