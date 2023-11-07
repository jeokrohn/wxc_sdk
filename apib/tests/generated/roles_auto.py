from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Role', 'RoleCollectionResponse']


class Role(ApiModel):
    #: A unique identifier for the role.
    #: example: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: The name of the role.
    #: example: Full Administrator
    name: Optional[str] = None


class RoleCollectionResponse(ApiModel):
    items: Optional[list[Role]] = None


class RolesApi(ApiChild, base='roles'):
    """
    Roles
    
    A persona for an authenticated user, corresponding to a set of privileges within an organization. This roles
    resource can be accessed only by an admin and shows only roles relevant to an admin.
    """
    ...