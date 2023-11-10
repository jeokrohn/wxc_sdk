from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GroupMembers', 'Groups', 'Template', 'TemplateCollectionResponse', 'TemplateTemplateType']


class TemplateTemplateType(str, Enum):
    org = 'ORG'
    group = 'GROUP'


class Template(ApiModel):
    #: A unique identifier for a license template.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the organization-level template.
    #: example: Default
    template_name: Optional[str] = None
    #: An array of license strings.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    licenses: Optional[list[str]] = None
    #: Specify the template type to be created. Valid values are `ORG` or `GROUP`.
    template_type: Optional[TemplateTemplateType] = None
    #: An array of group IDs associated with the template.
    #: example: ['Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xOU0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh']
    groups: Optional[list[str]] = None


class TemplateCollectionResponse(ApiModel):
    items: Optional[list[Template]] = None


class GroupMembers(ApiModel):
    #: example: Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xJWU1LWExNTItZmUzNDgxOWNkYsgh
    id: Optional[str] = None
    #: example: Test Group
    display_name: Optional[str] = None


class Groups(ApiModel):
    items: Optional[list[GroupMembers]] = None


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
