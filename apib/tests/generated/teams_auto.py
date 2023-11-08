from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Team', 'TeamCollectionResponse']


class Team(ApiModel):
    #: A unique identifier for the team.
    #: example: Y2lzY29zcGFyazovL3VzL1RFQU0vMTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5
    id: Optional[str] = None
    #: A user-friendly name for the team.
    #: example: Build Squad
    name: Optional[str] = None
    #: The teams description.
    #: example: The A Team
    description: Optional[str] = None
    #: The date and time the team was created.
    #: example: 2015-10-18T14:26:16.000Z
    created: Optional[datetime] = None


class TeamCollectionResponse(ApiModel):
    items: Optional[list[Team]] = None


class TeamsApi(ApiChild, base='teams'):
    """
    Teams
    
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to
    manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its
    name, for example.
    
    To manage people in a team see the `Team Memberships API
    <https://developer.webex.com/docs/api/v1/team-memberships>`_.
    
    To manage team rooms see the `Rooms API
    <https://developer.webex.com/docs/api/v1/rooms>`_.
    """

    def list_teams(self, max_: int = None) -> list[Team]:
        """
        List Teams

        Lists teams to which the authenticated user belongs.

        :param max_: Limit the maximum number of teams in the response.
        :type max_: int
        :rtype: list[Team]
        """
        params = {}
        if max_ is not None:
            params['max'] = max_
        url = self.ep()
        ...


    def create_a_team(self, name: str, description: str = None) -> Team:
        """
        Create a Team

        Creates a team.
        
        The authenticated user is automatically added as a member of the team. See the `Team Memberships API
        <https://developer.webex.com/docs/api/v1/team-memberships>`_ to learn
        how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str
        :rtype: :class:`Team`
        """
        url = self.ep()
        ...


    def get_team_details(self, team_id: str, description: str = None) -> Team:
        """
        Get Team Details

        Shows details for a team, by ID.
        
        Specify the team ID in the `teamId` parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param description: The teams description.
        :type description: str
        :rtype: :class:`Team`
        """
        params = {}
        if description is not None:
            params['description'] = description
        url = self.ep(f'{team_id}')
        ...


    def update_a_team(self, team_id: str, name: str, description: str = None) -> Team:
        """
        Update a Team

        Updates details for a team, by ID.
        
        Specify the team ID in the `teamId` parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str
        :rtype: :class:`Team`
        """
        url = self.ep(f'{team_id}')
        ...


    def delete_a_team(self, team_id: str):
        """
        Delete a Team

        Deletes a team, by ID.
        
        Specify the team ID in the `teamId` parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :rtype: None
        """
        url = self.ep(f'{team_id}')
        ...

    ...