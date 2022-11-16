"""
Teams API
"""
from collections.abc import Generator
from datetime import datetime
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['Team', 'TeamsApi']


class Team(ApiModel):
    #: A unique identifier for the team.
    id: Optional[str]
    #: A user-friendly name for the team.
    name: Optional[str]
    #: id of the creator
    creator_id: Optional[str]
    #: The date and time the team was created.
    created: Optional[datetime]


class TeamsApi(ApiChild, base='teams'):
    """
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to
    manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its
    name, for example.
    To manage people in a team see the Team Memberships API.
    To manage team rooms see the Rooms API.
    """

    def list(self) -> Generator[Team, None, None]:
        """
        Lists teams to which the authenticated user belongs.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Team)

    def create(self, name: str) -> Team:
        """
        Creates a team.
        The authenticated user is automatically added as a member of the team. See the Team Memberships API to learn
        how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        """
        body = {}
        if name is not None:
            body['name'] = name
        url = self.ep()
        data = super().post(url=url, json=body)
        return Team.parse_obj(data)

    def details(self, team_id: str) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        data = super().get(url=url)
        return Team.parse_obj(data)

    def update(self, team_id: str, name: str) -> Team:
        """
        Updates details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param name: A user-friendly name for the team.
        :type name: str
        """
        body = {'name': name}
        url = self.ep(f'{team_id}')
        data = super().put(url=url, json=body)
        return Team.parse_obj(data)

    def delete(self, team_id: str):
        """
        Deletes a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        super().delete(url=url)
        return
