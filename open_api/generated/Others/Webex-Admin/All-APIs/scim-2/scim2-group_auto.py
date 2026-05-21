import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetGroupResponse', 'GetGroupResponseMembersItem',
           'GetGroupResponseUrnscimschemasextensionciscowebexidentity20Group',
           'GetGroupResponseUrnscimschemasextensionciscowebexidentity20GroupMeta', 'GroupInheritancesObject',
           'GroupInheritancesObjectType', 'GroupMemberObject', 'GroupMemberResponse',
           'GroupMemberResponseMembersItem', 'ManagedByObject', 'MetaObject', 'MetaObjectResourceType',
           'PatchGroupOperationsItem', 'PatchGroupOperationsItemOp',
           'PostGroupUrnscimschemasextensionciscowebexidentity20Group',
           'PostGroupUrnscimschemasextensionciscowebexidentity20GroupOwnersItem', 'SCIM2GroupsApi',
           'SearchGroupResponse']


class PatchGroupOperationsItemOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class GroupInheritancesObjectType(str, Enum):
    role = 'role'


class GroupInheritancesObject(ApiModel):
    #: Type of inheritance. Currently, only the `role` type is supported. Only `policy` usage supports inheritance.
    type: Optional[GroupInheritancesObjectType] = None
    #: The value of the inheritance. For the role type, this can be role names such as `id_full_admin`,
    #: `id_user_admin`, etc.
    value: Optional[str] = None
    #: Indicates whether this inheritance is nested.
    nested: Optional[bool] = None
    #: Indicates which types of entities can inherit this property.
    scope: Optional[list[str]] = None


class PatchGroupOperationsItem(ApiModel):
    #: The operation to perform.
    op: Optional[PatchGroupOperationsItemOp] = None
    #: A string containing an attribute path describing the target of the operation.
    path: Optional[str] = None
    #: New value.
    value: Optional[list[GroupInheritancesObject]] = None


class PostGroupUrnscimschemasextensionciscowebexidentity20GroupOwnersItem(ApiModel):
    #: The identifier of the owner of this group.
    value: Optional[str] = None


class ManagedByObject(ApiModel):
    #: The Organization identifier of the resource.
    org_id: Optional[str] = None
    #: The resource type.
    type: Optional[str] = None
    #: The identifier of the resource.
    id: Optional[str] = None
    #: The delegated role.
    role: Optional[str] = None


class PostGroupUrnscimschemasextensionciscowebexidentity20Group(ApiModel):
    #: The identifier of this Group.
    usage: Optional[str] = None
    #: The owners of this group.
    owners: Optional[list[PostGroupUrnscimschemasextensionciscowebexidentity20GroupOwnersItem]] = None
    #: An array of inheritances
    inheritances: Optional[list[GroupInheritancesObject]] = None
    #: A list of delegates of this group.
    managed_by: Optional[list[ManagedByObject]] = None


class GroupMemberObject(ApiModel):
    #: The identifier of the member of this Group.
    value: Optional[str] = None
    #: A label indicating the type of resource, for example user, machine, or group.
    type: Optional[str] = None


class GetGroupResponseMembersItem(ApiModel):
    #: A label indicating the type of resource, for example user, machine, or group.
    type: Optional[str] = None
    #: The identifier of the member of this Group.
    value: Optional[str] = None
    #: A human-readable name for the group member.
    display: Optional[str] = None
    #: The URI corresponding to a SCIM resource that is a member of this Group.
    _ref: Optional[str] = Field(alias='$ref', default=None)


class GetGroupResponseUrnscimschemasextensionciscowebexidentity20GroupMeta(ApiModel):
    #: The ID of the organization to which this group belongs.
    organization_id: Optional[str] = Field(alias='organizationID', default=None)


class GetGroupResponseUrnscimschemasextensionciscowebexidentity20Group(ApiModel):
    #: The identifier of this group.
    usage: Optional[str] = None
    #: The owners of this group.
    owners: Optional[list[PostGroupUrnscimschemasextensionciscowebexidentity20GroupOwnersItem]] = None
    #: A list of delegates of this group.
    managed_by: Optional[list[ManagedByObject]] = None
    #: The identifier of the source.
    provision_source: Optional[str] = None
    #: An array of inheritances
    inheritances: Optional[list[GroupInheritancesObject]] = None
    #: Response metadata.
    meta: Optional[GetGroupResponseUrnscimschemasextensionciscowebexidentity20GroupMeta] = None


class MetaObjectResourceType(str, Enum):
    group = 'group'
    user = 'user'


class MetaObject(ApiModel):
    resource_type: Optional[MetaObjectResourceType] = None
    #: The date and time the group was created.
    created: Optional[datetime] = None
    #: The date and time the group was last changed.
    last_modified: Optional[datetime] = None
    #: The version of the group.
    version: Optional[str] = None
    #: The resource itself.
    location: Optional[str] = None


class GetGroupResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    display_name: Optional[str] = None
    #: A unique identifier for the group.
    id: Optional[str] = None
    #: An identifier for the resource as defined by the provisioning client.
    external_id: Optional[str] = None
    #: A list of members of this group.
    members: Optional[list[GetGroupResponseMembersItem]] = None
    #: Response metadata.
    meta: Optional[MetaObject] = None
    #: The Cisco extention of SCIM 2
    urn_scim_schemas_extension_cisco_webexidentity_2_0_group: Optional[GetGroupResponseUrnscimschemasextensionciscowebexidentity20Group] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:Group', default=None)


class SearchGroupResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Total number of groups in search results.
    member_size: Optional[int] = None
    #: The total number of items in a paged result.
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching contacts.
    start_index: Optional[int] = None
    #: An array of group objects.
    resources: Optional[list[GetGroupResponse]] = Field(alias='Resources', default=None)


class GroupMemberResponseMembersItem(ApiModel):
    #: A label indicating the type of resource, for example user, machine, or group.
    type: Optional[str] = None
    #: The identifier of the member of this Group.
    value: Optional[str] = None
    #: A human-readable name for the group member.
    display: Optional[str] = None


class GroupMemberResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    display_name: Optional[str] = None
    #: Total number of groups in search results.
    total_results: Optional[int] = None
    #: The total number of items in a paged result.
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching groups.
    start_index: Optional[int] = None
    #: A list of members of this group.
    members: Optional[list[GroupMemberResponseMembersItem]] = None


class SCIM2GroupsApi(ApiChild, base='identity/scim'):
    """
    SCIM 2 Groups
    
    Implementation of the SCIM 2.0 group part for group management in a standards based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition with detailed in
    `SCIM 2.0 schema
    <https://datatracker.ietf.org/doc/html/rfc7643>`_ and `SCIM 2.0 Protocol
    """

    def search_groups(self, org_id: str, filter: str = None, attributes: str = None, excluded_attributes: str = None,
                      sort_by: str = None, sort_order: str = None, start_index: int = None, count: int = None,
                      include_members: bool = None, member_type: str = None) -> SearchGroupResponse:
        """
        Search groups

        Retrieve a list of groups in the organization.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        <br/>

        **Authorization**

        An OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param filter: The url encoded filter. The example content is 'displayName Eq "group1@example.com" or
            displayName Eq "group2@example.com"'.
        For more filter patterns, see https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2. If the value is
        empty, the API returns all groups under the organization.
        :type filter: str
        :param attributes: The attributes to return.
        :type attributes: str
        :param excluded_attributes: Attributes to be excluded from the return.
        :type excluded_attributes: str
        :param sort_by: A string indicating the attribute whose value be used to order the returned responses. Now we
            only allow `displayName, id, meta.lastModified` to sort.
        :type sort_by: str
        :param sort_order: A string indicating the order in which the `sortBy` parameter is applied. Allowed values are
            `ascending` and `descending`.
        :type sort_order: str
        :param start_index: An integer indicating the 1-based index of the first query result. The default is 1.
        :type start_index: int
        :param count: An integer indicating the desired maximum number of query results per page. The default is 100.
        :type count: int
        :param include_members: Default "false". If false, no members returned.
        :type include_members: bool
        :param member_type: Filter the members by member type. Sample data: `user`, `machine`, `group`.
        :type member_type: str
        :rtype: :class:`SearchGroupResponse`
        """
        params: dict[str, Any] = dict()
        if filter is not None:
            params['filter'] = filter
        if attributes is not None:
            params['attributes'] = attributes
        if excluded_attributes is not None:
            params['excludedAttributes'] = excluded_attributes
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_order is not None:
            params['sortOrder'] = sort_order
        if start_index is not None:
            params['startIndex'] = start_index
        if count is not None:
            params['count'] = count
        if include_members is not None:
            params['includeMembers'] = str(include_members).lower()
        if member_type is not None:
            params['memberType'] = member_type
        url = self.ep(f'{org_id}/v2/Groups')
        data = super().get(url, params=params)
        r = SearchGroupResponse.model_validate(data)
        return r

    def create_a_group(self, org_id: str, schemas: list[str], display_name: str, external_id: str = None,
                       members: list[GroupMemberObject] = None,
                       urn_scim_schemas_extension_cisco_webexidentity_2_0_group: PostGroupUrnscimschemasextensionciscowebexidentity20Group = None) -> GetGroupResponse:
        """
        Create a group

        Create a new group for a given organization. The group may optionally be created with group members.

        <br/>

        **Authorization**

        OAuth token returned by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        <br/>

        **Usage**:

        1. The input JSON must conform to one of the following schemas:
        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        1. Unrecognized schemas (ID/section) are ignored.

        1. Read-only attributes provided as input values are ignored.

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param display_name: A human-readable name for the Group.
        :type display_name: str
        :param external_id: An identifier for the resource as defined by the provisioning client.
        :type external_id: str
        :param members: A list of members of this group.
        :type members: list[GroupMemberObject]
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_group: The Cisco extension of SCIM 2.
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_group: PostGroupUrnscimschemasextensionciscowebexidentity20Group
        :rtype: :class:`GetGroupResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['displayName'] = display_name
        if external_id is not None:
            body['externalId'] = external_id
        if members is not None:
            body['members'] = TypeAdapter(list[GroupMemberObject]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        if urn_scim_schemas_extension_cisco_webexidentity_2_0_group is not None:
            body['urn:scim:schemas:extension:cisco:webexidentity:2.0:Group'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_group.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Groups')
        data = super().post(url, json=body)
        r = GetGroupResponse.model_validate(data)
        return r

    def delete_a_group(self, org_id: str, group_id: str) -> None:
        """
        Delete a group

        Remove a group from the system.

        Specify the group ID in the `groupId` parameter in the URI.

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group_id: A unique identifier for the group.
        :type group_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        super().delete(url)

    def get_a_group(self, org_id: str, group_id: str, excluded_attributes: str = None) -> GetGroupResponse:
        """
        Get a group

        Retrieve details for a group, by ID.

        Optionally, members can be retrieved with this request. The maximum number of members returned is 500.

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param excluded_attributes: Attributes to be excluded from the return.
        :type excluded_attributes: str
        :rtype: :class:`GetGroupResponse`
        """
        params: dict[str, Any] = dict()
        if excluded_attributes is not None:
            params['excludedAttributes'] = excluded_attributes
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        data = super().get(url, params=params)
        r = GetGroupResponse.model_validate(data)
        return r

    def update_a_group_with_patch(self, org_id: str, group_id: str, schemas: list[str],
                                  operations: list[PatchGroupOperationsItem]) -> GetGroupResponse:
        """
        Update a group with PATCH

        Update group attributes with PATCH.

        Specify the group ID in the `groupId` parameter in the URI.

        <br/>

        **Authorization**

        OAuth token returned by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        <br/>

        **Usage**:

        1. The input JSON must conform to one of the following schemas:
        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        1. Unrecognized schemas (ID/section) are ignored.

        1. Read-only attributes provided as input values are ignored.

        1. Each operation on an attribute must be compatible with the attribute's mutability.

        1. Each PATCH operation represents a single action to be applied to the
        same SCIM resource specified by the request URI. Operations are
        applied sequentially in the order they appear in the array. Each
        operation in the sequence is applied to the target resource; the
        resulting resource becomes the target of the next operation.
        Evaluation continues until all operations are successfully applied or
        until an error condition is encountered.

        <br/>

        **Add operations**:

        The `add` operation is used to add a new attribute value to an existing resource. The operation must contain a
        `value` member whose content specifies the value to be added. The value may be a quoted value, or it may be a
        JSON object containing the sub-attributes of the complex attribute specified in the operation's `path`. The
        result of the add operation depends upon the target location indicated by `path` references:

        <br/>

        - If omitted, the target location is assumed to be the resource itself. The `value` parameter contains a set of
        attributes to be added to the resource.

        - If the target location does not exist, the attribute and value are added.

        - If the target location specifies a complex attribute, a set of sub-attributes shall be specified in the
        `value` parameter.

        - If the target location specifies a multi-valued attribute, a new value is added to the attribute.

        - If the target location specifies a single-valued attribute, the existing value is replaced.

        - If the target location specifies an attribute that does not exist (has no value), the attribute is added with
        the new value.

        - If the target location exists, the value is replaced.

        - If the target location already contains the value specified, no changes should be made to the resource.

        <br/>

        **Replace operations**:

        The `replace` operation replaces the value at the target location specified by the `path`. The operation
        performs the following functions, depending on the target location specified by `path`:

        <br/>

        - If the `path` parameter is omitted, the target is assumed to be the resource itself. In this case, the
        `value` attribute shall contain a list of one or more attributes that are to be replaced.

        - If the target location is a single-value attribute, the value of the attribute is replaced.

        - If the target location is a multi-valued attribute and no filter is specified, the attribute and all values
        are replaced.

        - If the target location path specifies an attribute that does not exist, the service provider shall treat the
        operation as an "add".

        - If the target location specifies a complex attribute, a set of sub-attributes SHALL be specified in the
        `value` parameter, which replaces any existing values or adds where an attribute did not previously exist.
        Sub-attributes that are not specified in the `value` parameters are left unchanged.

        - If the target location is a multi-valued attribute and a value selection ("valuePath") filter is specified
        that matches one or more values of the multi-valued attribute, then all matching record values will be
        replaced.

        - If the target location is a complex multi-valued attribute with a value selection filter ("valuePath") and a
        specific sub-attribute (e.g., "addresses[type eq "work"].streetAddress"), the matching sub-attribute of all
        matching records is replaced.

        - If the target location is a multi-valued attribute for which a value selection filter ("valuePath") has been
        supplied and no record match was made, the service provider will indicate the failure by returning HTTP status
        code 400 and a `scimType` error code of `noTarget`.

        <br/>

        **Remove operations**:

        The `remove` operation removes the value at the target location specified by the required attribute `path`. The
        operation performs the following functions, depending on the target location specified by `path`:

        <br/>

        - If `path` is unspecified, the operation fails with HTTP status code 400 and a "scimType" error code of
        "noTarget".

        - If the target location is a single-value attribute, the attribute and its associated value is removed, and
        the attribute will be considered unassigned.

        - If the target location is a multi-valued attribute and no filter is specified, the attribute and all values
        are removed, and the attribute SHALL be considered unassigned.

        - If the target location is a multi-valued attribute and a complex filter is specified comparing a `value`, the
        values matched by the filter are removed. If no other values remain after the removal of the selected values,
        the multi-valued attribute will be considered unassigned.

        - If the target location is a complex multi-valued attribute and a complex filter is specified based on the
        attribute`s sub-attributes, the matching records are removed. Sub-attributes whose values have been removed
        will be considered unassigned. If the complex multi-valued attribute has no remaining records, the attribute
        will be considered unassigned.

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param operations: A list of patch operations.
        :type operations: list[PatchGroupOperationsItem]
        :rtype: :class:`GetGroupResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['Operations'] = TypeAdapter(list[PatchGroupOperationsItem]).dump_python(operations, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        data = super().patch(url, json=body)
        r = GetGroupResponse.model_validate(data)
        return r

    def update_a_group_with_put(self, org_id: str, group_id: str, schemas: list[str], display_name: str,
                                external_id: str = None, members: list[GroupMemberObject] = None,
                                urn_scim_schemas_extension_cisco_webexidentity_2_0_group: PostGroupUrnscimschemasextensionciscowebexidentity20Group = None) -> GetGroupResponse:
        """
        Update a group with PUT

        Replace the contents of the Group.

        Specify the group ID in the `groupId` parameter in the URI.

        <br/>

        **Authorization**

        OAuth token returned by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        <br/>

        **Usage**:

        1. The input JSON must conform to one of the following schemas:
        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        1. Unrecognized schemas (ID/section) are ignored.

        1. Read-only attributes provided as input values are ignored.

        1. The group `id` is not changed.

        1. All attributes are cleaned up if a new value is not provided by the client.

        1. The values, `meta` and `created` are not changed.

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param display_name: A human-readable name for the group.
        :type display_name: str
        :param external_id: An identifier for the resource as defined by the provisioning client.
        :type external_id: str
        :param members: A list of members of this group.
        :type members: list[GroupMemberObject]
        :param urn_scim_schemas_extension_cisco_webexidentity_2_0_group: The Cisco extension of SCIM 2.
        :type urn_scim_schemas_extension_cisco_webexidentity_2_0_group: PostGroupUrnscimschemasextensionciscowebexidentity20Group
        :rtype: :class:`GetGroupResponse`
        """
        body: dict[str, Any] = dict()
        body['schemas'] = schemas
        body['displayName'] = display_name
        if external_id is not None:
            body['externalId'] = external_id
        if members is not None:
            body['members'] = TypeAdapter(list[GroupMemberObject]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        if urn_scim_schemas_extension_cisco_webexidentity_2_0_group is not None:
            body['urn:scim:schemas:extension:cisco:webexidentity:2.0:Group'] = urn_scim_schemas_extension_cisco_webexidentity_2_0_group.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        data = super().put(url, json=body)
        r = GetGroupResponse.model_validate(data)
        return r

    def get_group_members(self, org_id: str, group_id: str, start_index: int = None, count: int = None,
                          member_type: str = None) -> GroupMemberResponse:
        """
        Get Group Members

        Returns the members of a group.

        - The default maximum number of members returned is 500.

        - Control parameters are available to page through the members and to control the size of the results.

        - Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        **Note**
        Location groups are different from SCIM groups. You cannot search for identities in a location via groups.

        <br/>

        **Authorization**

        OAuth token returned by the Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        - `identity:people_read`

        <br/>

        The following administrators can use this API:

        - `id_full_admin`

        - `id_group_admin`

        - `id_readonly_admin`

        - `id_device_admin`

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param start_index: The index to start for group pagination.
        :type start_index: int
        :param count: Non-negative integer that specifies the desired number of search results per page. The maximum
            value for the count is 500.
        :type count: int
        :param member_type: Filter the members by member type. Sample data: `user`, `machine`, `group`.
        :type member_type: str
        :rtype: :class:`GroupMemberResponse`
        """
        params: dict[str, Any] = dict()
        if start_index is not None:
            params['startIndex'] = start_index
        if count is not None:
            params['count'] = count
        if member_type is not None:
            params['memberType'] = member_type
        url = self.ep(f'{org_id}/v2/Groups/{group_id}/Members')
        data = super().get(url, params=params)
        r = GroupMemberResponse.model_validate(data)
        return r
