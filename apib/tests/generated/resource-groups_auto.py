from datetime import datetime
from typing import Optional

from pydantic import Field

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
