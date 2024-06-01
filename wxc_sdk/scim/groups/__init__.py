from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional

from pydantic import Field, TypeAdapter

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.scim.child import ScimApiChild
from wxc_sdk.scim.users import PatchUserOperation

__all__ = ['ScimGroup', 'ScimGroupMember',
           'WebexGroup',
           'WebexGroupMeta', 'GroupMemberObject',
           'GroupMemberResponse', 'ManagedBy', 'GroupMeta',
           'MetaObjectResourceType',
           'WebexGroupOwner', 'SCIM2GroupsApi', 'SearchGroupResponse']

SCHEMAS = [
    "urn:ietf:params:scim:schemas:core:2.0:Group",
    "urn:scim:schemas:extension:cisco:webexidentity:2.0:Group"
]


class WebexGroupOwner(ApiModel):
    #: The identifier of the owner of this group.
    value: Optional[str] = None


class ManagedBy(ApiModel):
    #: The Organization identifier of the resource.
    org_id: Optional[str] = None
    #: The resource type.
    type: Optional[str] = None
    #: The identifier of the resource.
    id: Optional[str] = None
    #: The delegated role.
    role: Optional[str] = None


class GroupMemberObject(ApiModel):
    #: The identifier of the member of this Group.
    value: Optional[str] = None
    #: A label indicating the type of resource, for example user, machine, or group.
    type: Optional[str] = None


class ScimGroupMember(ApiModel):
    #: A label indicating the type of resource, for example user, machine, or group.
    type: Optional[str] = None
    #: The identifier of the member of this Group.
    value: Optional[str] = None
    #: A human-readable name for the group member.
    display: Optional[str] = None
    #: The URI corresponding to a SCIM resource that is a member of this Group.
    ref: Optional[str] = Field(alias='$ref', default=None)


class WebexGroupMeta(ApiModel):
    #: The ID of the organization to which this group belongs.
    organization_id: Optional[str] = None


class WebexGroup(ApiModel):
    #: The identifier of this group.
    usage: Optional[str] = None
    #: The owners of this group.
    owners: Optional[list[WebexGroupOwner]] = None
    #: A list of delegates of this group.
    managed_by: Optional[list[ManagedBy]] = None
    #: The identifier of the source.
    provision_source: Optional[str] = None
    #: Response metadata.
    meta: Optional[WebexGroupMeta] = None


class MetaObjectResourceType(str, Enum):
    group = 'Group'
    user = 'User'


class GroupMeta(ApiModel):
    resource_type: Optional[MetaObjectResourceType] = None
    #: The date and time the group was created.
    created: Optional[datetime] = None
    #: The date and time the group was last changed.
    last_modified: Optional[datetime] = None
    #: The version of the group.
    version: Optional[str] = None
    #: The resource itself.
    location: Optional[str] = None


class ScimGroup(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    display_name: Optional[str] = None
    #: A unique identifier for the group.
    id: Optional[str] = None
    #: An identifier for the resource as defined by the provisioning client.
    external_id: Optional[str] = None
    #: A list of members of this group.
    members: Optional[list[ScimGroupMember]] = None
    #: Response metadata.
    meta: Optional[GroupMeta] = None
    #: The Cisco extention of SCIM 2
    webex_group: Optional[WebexGroup] = Field(
        alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:Group', default=None)

    def create_update(self) -> dict:
        """

        :meta private:
        """
        data = self.model_dump(mode='json',
                               exclude_none=True,
                               by_alias=True,
                               exclude={'id': True,
                                        'schemas': True,
                                        'meta': True,
                                        'webex_group': {'meta': True}})
        data['schemas'] = SCHEMAS
        return data


class SearchGroupResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: Total number of groups in search results.
    total_results: Optional[int] = None
    #: The total number of items in a paged result.
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching contacts.
    start_index: Optional[int] = None
    #: An array of group objects.
    resources: Optional[list[ScimGroup]] = Field(alias='Resources', default=None)


class GroupMemberResponse(ApiModel):
    #: Input JSON schemas.
    schemas: Optional[list[str]] = None
    #: A human-readable name for the group.
    display_name: Optional[str] = None
    #: Total number of groups in search results.
    member_size: Optional[int] = None
    #: The total number of items in a paged result.
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching groups.
    start_index: Optional[int] = None
    #: A list of members of this group.
    members: Optional[list[ScimGroupMember]] = None


class SCIM2GroupsApi(ScimApiChild, base='identity/scim'):
    """
    SCIM 2 Groups

    Implementation of the SCIM 2.0 group part for group management in a standards based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition with
    detailed in
    `SCIM 2.0 schema
    <https://datatracker.ietf.org/doc/html/rfc7643>`_ and `SCIM 2.0 Protocol
    """

    def create(self, org_id: str, group: ScimGroup) -> ScimGroup:
        """
        Create a group

        Create a new group for a given organization. The group may optionally be created with group members.

        **Authorization**

        OAuth token returned by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        The following administrators can use this API:

        - `id_full_admin`
        - `id_group_admin`

        **Usage**:

        1. The input JSON must conform to one of the following schemas:

        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        2. Unrecognized schemas (ID/section) are ignored.

        3. Read-only attributes provided as input values are ignored.

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param group: Group settings
        :type group: ScimGroup
        :rtype: :class:`ScimGroup`
        """
        body = group.create_update()
        url = self.ep(f'{org_id}/v2/Groups')
        data = super().post(url, json=body)
        r = ScimGroup.model_validate(data)
        return r

    def details(self, org_id: str, group_id: str, excluded_attributes: str = None) -> ScimGroup:
        """
        Get a group

        Retrieve details for a group, by ID.

        Optionally, members can be retrieved with this request. The maximum number of members returned is 500.

        **Authorization**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`
        - `identity:people_read`

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
        :rtype: :class:`ScimGroup`
        """
        params = {}
        if excluded_attributes is not None:
            params['excludedAttributes'] = excluded_attributes
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        data = super().get(url, params=params)
        r = ScimGroup.model_validate(data)
        return r

    def search(self, org_id: str, filter: str = None, excluded_attributes: str = None, attributes: str = None,
               start_index: int = None, count: int = None, sort_by: str = None, sort_order: str = None,
               include_members: bool = None, member_type: str = None) -> SearchGroupResponse:
        """
        Search groups

        Retrieve a list of groups in the organization.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        **Authorization**

        An OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`
        - `identity:people_read`

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
        :param excluded_attributes: Attributes to be excluded from the return.
        :type excluded_attributes: str
        :param attributes: The attributes to return.
        :type attributes: str
        :param start_index: An integer indicating the 1-based index of the first query result. The default is 1.
        :type start_index: int
        :param count: An integer indicating the desired maximum number of query results per page. The default is 100.
        :type count: int
        :param sort_by: A string indicating the attribute whose value be used to order the returned responses. Now we
            only allow `displayName, id, meta.lastModified` to sort.
        :type sort_by: str
        :param sort_order: A string indicating the order in which the `sortBy` parameter is applied. Allowed values are
            `ascending` and `descending`.
        :type sort_order: str
        :param include_members: Default "false". If false, no members returned.
        :type include_members: bool
        :param member_type: Filter the members by member type. Sample data: `user`, `machine`, `group`.
        :type member_type: str
        :rtype: :class:`SearchGroupResponse`
        """
        params = {}
        if filter is not None:
            params['filter'] = filter
        if excluded_attributes is not None:
            params['excludedAttributes'] = excluded_attributes
        if attributes is not None:
            params['attributes'] = attributes
        if start_index is not None:
            params['startIndex'] = start_index
        if count is not None:
            params['count'] = count
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_order is not None:
            params['sortOrder'] = sort_order
        if include_members is not None:
            params['includeMembers'] = str(include_members).lower()
        if member_type is not None:
            params['memberType'] = member_type
        url = self.ep(f'{org_id}/v2/Groups')
        data = super().get(url, params=params)
        r = SearchGroupResponse.model_validate(data)
        return r

    def search_all(self, org_id: str, filter: str = None, excluded_attributes: str = None, attributes: str = None,
                   count: int = None, sort_by: str = None, sort_order: str = None,
                   include_members: bool = None, member_type: str = None) -> Generator[ScimGroup, None, None]:
        """
        Same operation as search() but returns a generator of ScimGroups instead of paginated resources

        See :meth:`SCIM2GroupsApi.search` for parameter documentation

        :param org_id:
        :param filter:
        :param excluded_attributes:
        :param attributes:
        :param count:
        :param sort_by:
        :param sort_order:
        :param include_members:
        :param member_type:
        :return:
        """
        '''async
    async def search_all_gen(self, org_id: str, filter: str = None, excluded_attributes: str = None, attributes: str 
    = None,
                             count: int = None, sort_by: str = None, sort_order: str = None,
                             include_members: bool = None, member_type: str = None) -> AsyncGenerator[ScimGroup, 
                             None, None]:
        params = {k: v for k, v in locals().items()
                  if k not in {'self', 'count'} and v is not None}
        start_index = None
        while True:
            paginated_result = await self.search(**params, start_index=start_index, count=count)
            for r in paginated_result.resources:
                yield r
            # prepare getting the next page
            count = paginated_result.items_per_page
            start_index = paginated_result.start_index + paginated_result.items_per_page
            if start_index > paginated_result.total_results:
                break
        return

    async def search_all(self, org_id: str, filter: str = None, excluded_attributes: str = None, attributes: str = None,
                         count: int = None, sort_by: str = None, sort_order: str = None,
                         include_members: bool = None, member_type: str = None) -> list[ScimGroup]:
        params = {k: v for k, v in locals().items()
                  if k not in {'self'} and v is not None}
        return [u async for u in self.search_all_gen(**params)]
        '''
        params = {k: v for k, v in locals().items()
                  if k not in {'self', 'count'} and v is not None}
        start_index = None
        while True:
            paginated_result = self.search(**params, start_index=start_index, count=count)
            yield from paginated_result.resources
            # prepare getting the next page
            count = paginated_result.items_per_page
            start_index = paginated_result.start_index + paginated_result.items_per_page
            if start_index > paginated_result.total_results:
                break
        return

    def members(self, org_id: str, group_id: str, start_index: int = None, count: int = None,
                member_type: str = None) -> GroupMemberResponse:
        """
        Get Group Members

        Returns the members of a group.

        - The default maximum number of members returned is 500.
        - Control parameters are available to page through the members and to control the size of the results.
        - Long result sets are split into `pages <https://developer.webex.com/docs/basics#pagination>`_.

        **Note**

        Location groups are different from SCIM groups. You cannot search for identities in a location via groups.

        **Authorization**

        OAuth token returned by the Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`
        - `identity:people_read`

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
        params = {}
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

    def members_all(self, org_id: str, group_id: str, start_index: int = None, count: int = None,
                    member_type: str = None) -> Generator[ScimGroupMember, None, None]:
        """
        Same operation as members() but returns a generator of ScimGroupMembers instead of paginated resources

        See :meth:`SCIM2GroupsApi.members` for parameter documentation

        :param org_id:
        :param group_id:
        :param start_index:
        :param count:
        :param member_type:
        :return:
        """
        '''async
    async def members_all_gen(self, org_id: str, group_id: str, start_index: int = None, count: int = None,
                              member_type: str = None) -> AsyncGenerator[ScimGroupMember, None, None]:
        params = {k: v for k, v in locals().items()
                  if k not in {'self', 'count'} and v is not None}
        start_index = None
        while True:
            paginated_result = await self.members(**params, start_index=start_index, count=count)
            for r in paginated_result.members:
                yield r
            # prepare getting the next page
            count = paginated_result.items_per_page
            start_index = paginated_result.start_index + paginated_result.items_per_page
            if start_index > paginated_result.member_size:
                break
        return

    async def members_all(self, org_id: str, group_id: str, start_index: int = None, count: int = None,
                          member_type: str = None) -> list[ScimGroupMember]:
        params = {k: v for k, v in locals().items()
                  if k not in {'self'} and v is not None}
        return [u async for u in self.members_all_gen(**params)]
        '''

        params = {k: v for k, v in locals().items()
                  if k not in {'self', 'count'} and v is not None}
        start_index = None
        while True:
            paginated_result = self.members(**params, start_index=start_index, count=count)
            yield from paginated_result.members
            # prepare getting the next page
            count = paginated_result.items_per_page
            start_index = paginated_result.start_index + paginated_result.items_per_page
            if start_index > paginated_result.member_size:
                break
        return

    def update(self, org_id: str, group: ScimGroup) -> ScimGroup:
        """
        Update a group with PUT

        Replace the contents of the Group.

        **Authorization**

        OAuth token returned by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        The following administrators can use this API:

        - `id_full_admin`
        - `id_group_admin`

        **Usage**:

        1. The input JSON must conform to one of the following schemas:

        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        2. Unrecognized schemas (ID/section) are ignored.

        3. Read-only attributes provided as input values are ignored.

        4. The group `id` is not changed.

        5. All attributes are cleaned up if a new value is not provided by the client.

        6. The values, `meta` and `created` are not changed.

        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :rtype: :class:`ScimGroup`
        """
        body = group.create_update()
        url = self.ep(f'{org_id}/v2/Groups/{group.id}')
        data = super().put(url, json=body)
        r = ScimGroup.model_validate(data)
        return r

    def patch(self, org_id: str, group_id: str, schemas: list[str],
              operations: list[PatchUserOperation]) -> ScimGroup:
        """
        Update a group with PATCH

        Update group attributes with PATCH.

        **Authorization**

        OAuth token returned by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        The following administrators can use this API:

        - `id_full_admin`
        - `id_group_admin`

        **Usage**:

        1. The input JSON must conform to one of the following schemas:

        - `urn:ietf:params:scim:schemas:core:2.0:Group`
        - `urn:scim:schemas:extension:cisco:webexidentity:2.0:Group`

        2. Unrecognized schemas (ID/section) are ignored.

        3. Read-only attributes provided as input values are ignored.

        4. Each operation on an attribute must be compatible with the attribute's mutability.

        5. Each PATCH operation represents a single action to be applied to the
        same SCIM resource specified by the request URI. Operations are
        applied sequentially in the order they appear in the array. Each
        operation in the sequence is applied to the target resource; the
        resulting resource becomes the target of the next operation.
        Evaluation continues until all operations are successfully applied or
        until an error condition is encountered.

        **Add operations**:

        The `add` operation is used to add a new attribute value to an existing resource. The operation must contain a
        `value` member whose content specifies the value to be added. The value may be a quoted value, or it may be a
        JSON object containing the sub-attributes of the complex attribute specified in the operation's `path`. The
        result of the add operation depends upon the target location indicated by `path` references:

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

        **Replace operations**:

        The `replace` operation replaces the value at the target location specified by the `path`. The operation
        performs the following functions, depending on the target location specified by `path`:

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

        **Remove operations**:

        The `remove` operation removes the value at the target location specified by the required attribute `path`. The
        operation performs the following functions, depending on the target location specified by `path`:

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
        :type operations: list[PatchGroupOperations]
        :rtype: :class:`ScimGroup`
        """
        body = dict()
        body['schemas'] = schemas
        body['Operations'] = TypeAdapter(list[PatchUserOperation]).dump_python(operations, mode='json', by_alias=True,
                                                                               exclude_none=True)
        url = self.ep(f'{org_id}/v2/Groups/{group_id}')
        data = super().patch(url, json=body)
        r = ScimGroup.model_validate(data)
        return r

    def delete(self, org_id: str, group_id: str):
        """
        Delete a group

        Remove a group from the system.

        **Authorization**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

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
