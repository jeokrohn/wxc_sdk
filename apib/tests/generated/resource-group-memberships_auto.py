from datetime import datetime
from typing import Optional

from pydantic import Field

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
    resourceGroupId: Optional[str] = None
    #: The license ID.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMWNjYmJjMTctZDYxNi00ZDc0LTg2NGItYjFmM2IwNzAxZmJhOk1TXzAzMDRjMDkzLTFjM2MtNDRlMC1iYjBhLWU1ZDE2NDM2NmQ1OQ
    licenseId: Optional[str] = None
    #: The person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    personId: Optional[str] = None
    #: The organization ID of the person.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    personOrgId: Optional[str] = None
    #: The activation status of the resource group membership.
    #: example: activated
    status: Optional[ResourceGroupMembershipStatus] = None


class ResourceGroupMembershipCollectionResponse(ApiModel):
    items: Optional[list[ResourceGroupMembership]] = None
