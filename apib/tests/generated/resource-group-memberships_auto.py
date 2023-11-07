from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ResourceGroupMembership', 'ResourceGroupMembershipCollectionResponse', 'ResourceGroupMembershipStatus']


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


class ResourceGroupMembershipCollectionResponse(ApiModel):
    items: Optional[list[ResourceGroupMembership]] = None


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
    ...