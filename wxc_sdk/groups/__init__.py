"""
Groups API
"""
import datetime
from collections.abc import Generator
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel

__all__ = ['GroupMember', 'Group', 'GroupsApi']


class GroupMember(ApiModel):
    #: Person ID of the group member.
    member_id: Optional[str] = Field(alias='id')
    #: Member type.
    member_type: Optional[str] = Field(alias='type')
    display_name: Optional[str]
    # only used in updates. 'delete' to delete a member
    operation: Optional[str]


class Group(ApiModel):
    #: A unique identifier for the group.
    group_id: Optional[str] = Field(alias='id')
    #: The name of the group.
    display_name: Optional[str]
    #: An array of members
    members: Optional[list[GroupMember]]
    #: The ID of the organization to which this group belongs.
    org_id: Optional[str]
    description: Optional[str]
    #: The timestamp indicating creation date/time of group
    created: Optional[datetime.datetime]
    #: The timestamp indicating lastModification time of group
    last_modified: Optional[datetime.datetime]
    member_size: Optional[int]
    usage: Optional[str]


class GroupsApi(ApiChild, base='groups'):
    """
    Groups contain a collection of members in Webex. A member represents a Webex user. A group is used to assign
    templates and settings to the set of members contained in a group. To create and manage a group, including adding
    and removing members from a group, an auth token containing the identity:groups_rw is required. Searching and
    viewing members of a group requires an auth token with a scope of identity:groups_read.
    To learn more about managing people to use as members in the /groups API please refer to the People API.
    """

    def list(self, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> Generator[Group, None, None]:
        """
        List groups in your organization.

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: List groups in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param list_filter: Searches the group by displayName with an operator and a value. The available operators
            are eq (equal) and sw (starts with). Only displayName can be used to filter results.
        :type list_filter: str
        :param params:
        :return: generator of :class:`Group` objects
        """
        params.update((to_camel(k), v) for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        for k, v in params.items():
            if isinstance(v, bool):
                params[k] = 'true' if v else 'false'
        if lf := params.pop('listFilter', None):
            params['filter'] = lf
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Group, item_key='groups', params=params)

    def create(self, settings: Group) -> Group:
        """
        Create a new group using the provided settings. Only display_name is mandatory

        :param settings: settings for new group
        :type settings: Group
        :return: new group
        :rtype: :class:`Group`
        """
        url = self.ep()
        body = settings.json(exclude={'group_id': True,
                                      'members': {'__all__': {'member_type': True,
                                                              'display_name': True,
                                                              'operation': True}},
                                      'created': True,
                                      'last_modified': True})
        data = self.post(url, data=body)
        return Group.parse_obj(data)

    def details(self, group_id: str, include_members: bool = None) -> Group:
        """
        Get group details

        :param group_id: group id
        :type group_id: str
        :param include_members: return members in response
        :type include_members: bool
        :return: group details
        :rtype: Group
        """
        url = self.ep(group_id)
        params = dict()
        if include_members is not None:
            params['includeMembers'] = 'true' if include_members else 'false'
        data = self.get(url, params=params)
        return Group.parse_obj(data)

    def members(self, group_id: str, **params) -> Generator[GroupMember, None, None]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')

    def update(self, group_id: str, settings: Group = None, remove_all: bool = None) -> Group:
        """
        update group information.

        Options: change displayName, add new members, remove some or all members, replace all members

        :param group_id:
        :param settings:
        :param remove_all:
        :return:
        """
        if not any((settings, remove_all)):
            raise ValueError('settings or remove_all have to be present')
        url = self.ep(group_id)
        if settings:
            body = settings.json(exclude={'group_id': True,
                                          'members': {'__all__': {'member_type': True,
                                                                  'display_name': True}},
                                          'created': True,
                                          'last_modified': True})
        else:
            body = 'purgeAllValues:{"attributes":["members"]}'
        data = self.patch(url, data=body)
        return Group.parse_obj(data)

    def delete_group(self, group_id: str):
        """
        Delete a group

        :param group_id: group id
        :type group_id: str
        """
        url = self.ep(group_id)
        self.delete(url)
