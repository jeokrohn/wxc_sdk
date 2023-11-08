from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GroupResponse', 'GroupsCollectionResponse', 'Member', 'PatchGroup', 'PatchMemberWithOperation',
            'PostGroup', 'PostMember']


class Member(ApiModel):
    #: Person ID of the group member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None
    #: Member type.
    #: example: user
    type: Optional[str] = None
    #: example: Jane Smith
    display_name: Optional[str] = None


class PostMember(ApiModel):
    #: Person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None


class PatchMemberWithOperation(ApiModel):
    #: Person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[str] = None


class PostGroup(ApiModel):
    #: The name of the group.
    #: example: Sales Group
    display_name: Optional[str] = None
    #: The ID of the organization to which this group belongs. If not specified, the organization ID from the OAuth
    #: token is used.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDhhZGI4MS0yOGY5LTRhYjUtYjJkNi1lOWI0OTRlNzJhMDY
    org_id: Optional[str] = None
    #: Description of the group.
    #: example: Salas Group in San Jose
    description: Optional[str] = None
    #: An array of members. Maximum of 500 members can be provided. To add more members, use the `Update a Group
    #: <https://developer.webex.com/docs/api/v1/groups/update-a-group>`_ API to
    #: add additional members.
    members: Optional[list[PostMember]] = None


class PatchGroup(ApiModel):
    #: The name of the group.
    #: example: New Sales Group
    display_name: Optional[str] = None
    #: Description of the group.
    #: example: Sales Group in LA
    description: Optional[str] = None
    #: An array of members operations.
    members: Optional[list[PatchMemberWithOperation]] = None


class GroupResponse(ApiModel):
    #: A unique identifier for the group.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvMjUxMDRiZTAtZjg3NC00MzQzLTk2MDctZGYwMmRmMzdiNWMxOjM0OGFkYjgxLTI4ZjktNGFiNS1iMmQ2LWU5YjQ5NGU3MmEwNg
    id: Optional[str] = None
    #: The name of the group.
    #: example: Sales Group
    display_name: Optional[str] = None
    #: The ID of the organization to which this group belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDhhZGI4MS0yOGY5LTRhYjUtYjJkNi1lOWI0OTRlNzJhMDY
    org_id: Optional[str] = None
    #: The timestamp indicating creation date/time of group
    #: example: 2022-02-17T02:13:29.706Z
    created: Optional[datetime] = None
    #: The timestamp indicating lastModification time of group
    #: example: 2022-02-17T02:13:29.706Z
    last_modified: Optional[datetime] = None
    #: example: 1.0
    member_size: Optional[int] = None
    #: An array of members
    members: Optional[list[Member]] = None


class GroupsCollectionResponse(ApiModel):
    #: Total number of groups returned in the response.
    #: example: 3.0
    total_results: Optional[int] = None
    #: example: 1.0
    start_index: Optional[int] = None
    #: example: 10.0
    items_per_page: Optional[int] = None
    #: An array of group objects.
    groups: Optional[list[GroupResponse]] = None


class GroupsApi(ApiChild, base='groups'):
    """
    Groups
    
    Groups contain a collection of members in Webex. A member represents a Webex user. A group is used to assign
    templates and settings to the set of members contained in a group.  To create and manage a group, including adding
    and removing members from a group, an auth token containing the `identity:groups_rw` is required.  Searching and
    viewing members of a group requires an auth token with a scope of `identity:groups_read`.
    
    To learn more about managing people to use as members in the /groups API please refer to the `People API
    <https://developer.webex.com/docs/api/v1/people>`_.
    """

    def create_a_group(self, display_name: str, org_id: str, description: str,
                       members: list[PostMember]) -> GroupResponse:
        """
        Create a Group

        Create a new group for a given organization. The group may optionally be created with group members.

        :param display_name: The name of the group.
        :type display_name: str
        :param org_id: The ID of the organization to which this group belongs. If not specified, the organization ID
            from the OAuth token is used.
        :type org_id: str
        :param description: Description of the group.
        :type description: str
        :param members: An array of members. Maximum of 500 members can be provided. To add more members, use the
            `Update a Group
            <https://developer.webex.com/docs/api/v1/groups/update-a-group>`_ API to add additional members.
        :type members: list[PostMember]
        :rtype: :class:`GroupResponse`
        """
        ...


    def update_a_group(self, group_id: str, display_name: str, description: str,
                       members: list[PatchMemberWithOperation]) -> GroupResponse:
        """
        Update a Group

        Update the group details, by ID.
        
        Specify the group ID in the `groupId` parameter in the URI.

        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param display_name: The name of the group.
        :type display_name: str
        :param description: Description of the group.
        :type description: str
        :param members: An array of members operations.
        :type members: list[PatchMemberWithOperation]
        :rtype: :class:`GroupResponse`
        """
        ...


    def get_group_details(self, group_id: str, include_members: bool = None) -> GroupResponse:
        """
        Get Group Details

        Get details for a group, by ID.
        
        Optionally, the members may be retrieved with this request. The maximum number of members returned is 500.

        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param include_members: Include the members as part of the response.
        :type include_members: bool
        :rtype: :class:`GroupResponse`
        """
        ...


    def list_and_search_groups(self, org_id: str = None, filter: str = None, attributes: str = None,
                               sort_by: str = None, sort_order: str = None, include_members: bool = None,
                               start_index: int = None, count: int = None) -> GroupsCollectionResponse:
        """
        List and Search Groups

        List groups in your organization.
        
        * Set the `includeMembers` parameter to `true` to return group members. The total number of members returned is
        limited to 500.
        
        * Use the `startIndex` and `count` parameters to page through result set.
        
        * To search for a specific group use the `filter` parameter.
        
        * Use `sortBy` parameter to sort the responses by `id` or `displayName`.

        :param org_id: List groups in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param filter: Searches the group by `displayName` with an operator and a value.  The available operators are
            `eq` (equal) and `sw` (starts with).  Only `displayName` can be used to filter results.
        :type filter: str
        :param attributes: The attributes to return.
        :type attributes: str
        :param sort_by: Sort the results based by group `displayName`.
        :type sort_by: str
        :param sort_order: Sort results alphabetically by group display name, in ascending or descending order.
        :type sort_order: str
        :param include_members: Optionally return group members in the response. The maximum number of members returned
            is 500.
        :type include_members: bool
        :param start_index: The index to start for group pagination.
        :type start_index: int
        :param count: Specifies the desired number of search results per page.
        :type count: int
        :rtype: :class:`GroupsCollectionResponse`
        """
        ...


    def get_group_members(self, group_id: str, start_index: int = None, count: int = None) -> GroupResponse:
        """
        Get Group Members

        Gets the members of a group.
        
        * The default maximum members returned is 500.
        
        * Control parameters is available to page through the members and to control the size of the results.

        :param group_id: A unique identifier for the group.
        :type group_id: str
        :param start_index: The index to start for group pagination.
        :type start_index: int
        :param count: Non-negative integer that specifies the desired number of search results per page. Maximum value
            for the count is 500.
        :type count: int
        :rtype: :class:`GroupResponse`
        """
        ...


    def delete_a_group(self, group_id: str):
        """
        Delete a Group

        Remove a group from the system.
        
        Specify the group ID in the `groupId` parameter in the URI.

        :param group_id: A unique identifier for the group.
        :type group_id: str
        :rtype: None
        """
        ...

    ...