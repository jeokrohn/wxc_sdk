from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
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
    templateName: Optional[str] = None
    #: An array of license strings.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    licenses: Optional[list[str]] = None
    #: Specify the template type to be created. Valid values are `ORG` or `GROUP`.
    templateType: Optional[TemplateTemplateType] = None
    #: An array of group IDs associated with the template.
    #: example: ['Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xOU0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh']
    groups: Optional[list[str]] = None


class TemplateCollectionResponse(ApiModel):
    items: Optional[list[Template]] = None


class GroupMembers(ApiModel):
    #: example: Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xJWU1LWExNTItZmUzNDgxOWNkYsgh
    id: Optional[str] = None
    #: example: Test Group
    displayName: Optional[str] = None


class Groups(ApiModel):
    items: Optional[list[GroupMembers]] = None
