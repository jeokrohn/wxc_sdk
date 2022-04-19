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
    member_id: Optional[str] = Field(alias='id')
    member_type: Optional[str] = Field(alias='type')
    display_name: Optional[str]
    # only used in updates. 'delete to delete a member'
    operation: Optional[str]


class Group(ApiModel):
    group_id: Optional[str] = Field(alias='id')
    display_name: Optional[str]
    members: Optional[list[GroupMember]]
    org_id: Optional[str]
    description: Optional[str]
    created: Optional[datetime.datetime]
    last_modified: Optional[datetime.datetime]
    member_size: Optional[int]
    usage: Optional[str]


class GroupsApi(ApiChild, base='groups'):

    def list(self, *, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> Generator[Group, None, None]:
        """
        List groups

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: organisation ID
        :type org_id: str
        :param list_filter: filter expression. Example: displayName eq "test"
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

    def create(self, *, settings: Group) -> Group:
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

    def members(self, *, group_id: str, **params) -> Generator[GroupMember, None, None]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')

    def update(self, *, group_id: str, settings: Group = None, remove_all: bool = None) -> Group:
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
