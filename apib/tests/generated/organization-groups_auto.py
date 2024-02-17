from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GroupMembers', 'OrganizationGroupsApi']


class GroupMembers(ApiModel):
    #: example: Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xJWU1LWExNTItZmUzNDgxOWNkYsgh
    id: Optional[str] = None
    #: example: Test Group
    display_name: Optional[str] = None


class OrganizationGroupsApi(ApiChild, base='organization/groups?orgId={orgId}&displayName={displayName}'):
    """
    Organization Groups
    
    """

    def list_organization_groups(self, org_id: str) -> list[GroupMembers]:
        """
        List Organization Groups

        List the policy groups at an organization level based on a display name pattern.

        Specify the organization's ID in the `orgId` URI parameter and the group's display name pattern in the
        `displayName` URI parameter.

        :param org_id: A unique identifier for an org
        :type org_id: str
        :rtype: list[GroupMembers]
        """
        url = self.ep(f'')
        data = super().get(url)
        r = TypeAdapter(list[GroupMembers]).validate_python(data['items'])
        return r
