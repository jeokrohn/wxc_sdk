from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetGroupResponse', 'GetGroupResponseMembers', 'GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group', 'GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupMeta', 'GroupMemberObject', 'GroupMemberResponse', 'GroupMemberResponseMembers', 'ManagedByObject', 'MetaObject', 'MetaObjectResourceType', 'PatchGroup', 'PatchGroupOperations', 'PatchGroupOperationsOp', 'PostGroup', 'PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group', 'PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupOwners', 'SearchGroupResponse']


class PatchGroupOperationsOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class PatchGroupOperations(ApiModel):
    #: The operation to perform.
    #: example: add
    op: Optional[PatchGroupOperationsOp] = None
    #: A string containing an attribute path describing the target of the operation.
    #: example: displayName
    path: Optional[str] = None
    #: New value.
    #: example: new attribute value
    value: Optional[str] = None


class PatchGroup(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:PatchOp']
    schemas: Optional[list[str]] = None
    #: A list of patch operations.
    Operations: Optional[list[PatchGroupOperations]] = None


class PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupOwners(ApiModel):
    #: The identifier of the owner of this group.
    #: example: c5349664-9f3d-410b-8bd3-6c31f181f13d
    value: Optional[str] = None


class ManagedByObject(ApiModel):
    #: The Organization identifier of the resource.
    #: example: d1349664-9f3d-410b-8bd3-6c31f181f14e
    orgId: Optional[str] = None
    #: The resource type.
    #: example: user
    type: Optional[str] = None
    #: The identifier of the resource.
    #: example: c5349664-9f3d-410b-8bd3-6c31f181f13d
    id: Optional[str] = None
    #: The delegated role.
    #: example: location_full_admin
    role: Optional[str] = None


class PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group(ApiModel):
    #: The identifier of this Group.
    #: example: policy
    usage: Optional[str] = None
    #: The owners of this group.
    owners: Optional[list[PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupOwners]] = None
    #: A list of delegates of this group.
    managedBy: Optional[list[ManagedByObject]] = None


class GroupMemberObject(ApiModel):
    #: The identifier of the member of this Group.
    #: example: c5349664-9f3d-410b-8bd3-6c31f181f13d
    value: Optional[str] = None
    #: A label indicating the type of resource, for example user, machine, or group.
    #: example: user
    type: Optional[str] = None


class PostGroup(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:Group', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:Group']
    schemas: Optional[list[str]] = None
    #: A human-readable name for the Group.
    #: example: group1@example.com
    displayName: Optional[str] = None
    #: An identifier for the resource as defined by the provisioning client.
    #: example: test
    externalId: Optional[str] = None
    #: A list of members of this group.
    members: Optional[list[GroupMemberObject]] = None
    #: The Cisco extension of SCIM 2.
    urn:scim:schemas:extension:cisco:webexidentity:2.0:Group: Optional[PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group] = None


class GetGroupResponseMembers(ApiModel):
    #: A label indicating the type of resource, for example user, machine, or group.
    #: example: user
    type: Optional[str] = None
    #: The identifier of the member of this Group.
    #: example: c5349664-9f3d-410b-8bd3-6c31f181f13d
    value: Optional[str] = None
    #: A human-readable name for the group member.
    #: example: A user
    display: Optional[str] = None
    #: The URI corresponding to a SCIM resource that is a member of this Group.
    #: example: https://example.com/v2/Users/c5349664-9f3d-410b-8bd3-6c31f181f13d
    $ref: Optional[str] = None


class GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupMeta(ApiModel):
    #: The ID of the organization to which this group belongs.
    #: example: e9f9ab27-0459-4cd0-bd72-089bde5a7da6
    organizationID: Optional[str] = None


class GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group(ApiModel):
    #: The identifier of this group.
    #: example: location
    usage: Optional[str] = None
    #: The owners of this group.
    owners: Optional[list[PostGroupUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupOwners]] = None
    #: A list of delegates of this group.
    managedBy: Optional[list[ManagedByObject]] = None
    #: The identifier of the source.
    #: example: AD
    provisionSource: Optional[str] = None
    #: Response metadata.
    meta: Optional[GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:GroupMeta] = None


class MetaObjectResourceType(str, Enum):
    group = 'group'
    user = 'user'


class MetaObject(ApiModel):
    #: example: group
    resourceType: Optional[MetaObjectResourceType] = None
    #: The date and time the group was created.
    #: example: 2011-08-01T21:32:44.882Z
    created: Optional[datetime] = None
    #: The date and time the group was last changed.
    #: example: 2011-08-01T21:32:44.882Z
    lastModified: Optional[datetime] = None
    #: The version of the group.
    #: example: "W\/\"e180ee84f0671b1\""
    version: Optional[str] = None
    #: The resource itself.
    #: example: https://example.com/v2/Groups/e9e30dba-f08f-4109-8486-d5c6a331660a
    location: Optional[str] = None


class GetGroupResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:Group', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:Group']
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    #: example: group1@example.com
    displayName: Optional[str] = None
    #: A unique identifier for the group.
    #: example: cb8f48e4-5db2-496b-b43d-83d8d5a2a4b3
    id: Optional[str] = None
    #: An identifier for the resource as defined by the provisioning client.
    #: example: test
    externalId: Optional[str] = None
    #: A list of members of this group.
    members: Optional[list[GetGroupResponseMembers]] = None
    #: Response metadata.
    meta: Optional[MetaObject] = None
    #: The Cisco extention of SCIM 2
    urn:scim:schemas:extension:cisco:webexidentity:2.0:Group: Optional[GetGroupResponseUrn:scim:schemas:extension:cisco:webexidentity:2.0:Group] = None


class SearchGroupResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:scim:schemas:extension:cisco:webexidentity:2.0:GroupMembers']
    schemas: Optional[list[str]] = None
    #: Total number of groups in search results.
    #: example: 2.0
    memberSize: Optional[int] = None
    #: The total number of items in a paged result.
    #: example: 2.0
    itemsPerPage: Optional[int] = None
    #: Start at the one-based offset in the list of matching contacts.
    #: example: 1.0
    startIndex: Optional[int] = None
    #: An array of group objects.
    Resources: Optional[list[GetGroupResponse]] = None


class GroupMemberResponseMembers(ApiModel):
    #: A label indicating the type of resource, for example user, machine, or group.
    #: example: user
    type: Optional[str] = None
    #: The identifier of the member of this Group.
    #: example: c5349664-9f3d-410b-8bd3-6c31f181f13d
    value: Optional[str] = None
    #: A human-readable name for the group member.
    #: example: A user
    display: Optional[str] = None


class GroupMemberResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:ListResponse']
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    #: example: group1@example.com
    displayName: Optional[str] = None
    #: Total number of groups in search results.
    #: example: 2.0
    totalResults: Optional[int] = None
    #: The total number of items in a paged result.
    #: example: 2.0
    itemsPerPage: Optional[int] = None
    #: Start at the one-based offset in the list of matching groups.
    #: example: 1.0
    startIndex: Optional[int] = None
    #: A list of members of this group.
    members: Optional[list[GroupMemberResponseMembers]] = None
