from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateTeamBody', 'ListTeamsResponse', 'Team', 'TeamsApi']


class CreateTeamBody(ApiModel):
    #: A user-friendly name for the team.
    name: Optional[str]
    #: The teams description.
    description: Optional[str]


class Team(CreateTeamBody):
    #: A unique identifier for the team.
    id: Optional[str]
    #: The date and time the team was created.
    created: Optional[str]


class ListTeamsResponse(ApiModel):
    items: Optional[list[Team]]


class TeamsApi(ApiChild, base='teams'):
    """
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to
    manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its
    name, for example.
    To manage people in a team see the Team Memberships API.
    To manage team rooms see the Rooms API.
    """

    def list(self, **params) -> Generator[Team, None, None]:
        """
        Lists teams to which the authenticated user belongs.

        documentation: https://developer.webex.com/docs/api/v1/teams/list-teams
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Team, params=params)

    def create(self, name: str, description: str = None) -> Team:
        """
        Creates a team.
        The authenticated user is automatically added as a member of the team. See the Team Memberships API to learn
        how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/teams/create-a-team
        """
        body = CreateTeamBody()
        if name is not None:
            body.name = name
        if description is not None:
            body.description = description
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Team.parse_obj(data)

    def details(self, team_id: str, description: str = None) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param description: The teams description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/teams/get-team-details
        """
        params = {}
        if description is not None:
            params['description'] = description
        url = self.ep(f'{team_id}')
        data = super().get(url=url, params=params)
        return Team.parse_obj(data)

    def update(self, team_id: str, name: str, description: str = None) -> Team:
        """
        Updates details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/teams/update-a-team
        """
        body = CreateTeamBody()
        if name is not None:
            body.name = name
        if description is not None:
            body.description = description
        url = self.ep(f'{team_id}')
        data = super().put(url=url, data=body.json())
        return Team.parse_obj(data)

    def delete(self, team_id: str):
        """
        Deletes a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str

        documentation: https://developer.webex.com/docs/api/v1/teams/delete-a-team
        """
        url = self.ep(f'{team_id}')
        super().delete(url=url)
        return
