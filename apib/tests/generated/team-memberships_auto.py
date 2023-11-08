from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['TeamMembership', 'TeamMembershipCollectionResponse']


class TeamMembership(ApiModel):
    #: A unique identifier for the team membership.
    #: example: Y2lzY29zcGFyazovL3VzL1RFQU1fTUVNQkVSU0hJUC8wZmNmYTJiOC1hZGNjLTQ1ZWEtYTc4Mi1lNDYwNTkyZjgxZWY6MTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5
    id: Optional[str] = None
    #: The team ID.
    #: example: Y2lzY29zcGFyazovL3VzL1RFQU0vMTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5
    team_id: Optional[str] = None
    #: The person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of the person.
    #: example: john.andersen@example.com
    person_email: Optional[str] = None
    #: The display name of the person.
    #: example: John Andersen
    person_display_name: Optional[str] = None
    #: The organization ID of the person.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    person_org_id: Optional[str] = None
    #: Whether or not the participant is a team moderator.
    #: example: True
    is_moderator: Optional[bool] = None
    #: The date and time when the team membership was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class TeamMembershipCollectionResponse(ApiModel):
    items: Optional[list[TeamMembership]] = None


class TeamMembershipsApi(ApiChild, base='team/memberships'):
    """
    Team Memberships
    
    Team Memberships represent a person's relationship to a team. Use this API to list members of any team that you're
    in or create memberships to invite someone to a team. Team memberships can also be updated to make someone a
    moderator or deleted to remove them from the team.
    
    Just like in the Webex app, you must be a member of the team in order to list its memberships or invite people.
    """

    def list_team_memberships(self, team_id: str, max_: int = None) -> list[TeamMembership]:
        """
        List Team Memberships

        Lists all team memberships for a given team, specified by the `teamId` query parameter.
        
        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str
        :param max_: Limit the maximum number of team memberships in the response.
        :type max_: int
        :rtype: list[TeamMembership]
        """
        params = {}
        params['teamId'] = team_id
        if max_ is not None:
            params['max'] = max_
        url = self.ep()
        ...


    def create_a_team_membership(self, team_id: str, person_id: str = None, person_email: str = None,
                                 is_moderator: str = None) -> TeamMembership:
        """
        Create a Team Membership

        Add someone to a team by Person ID or email address, optionally making them a moderator.

        :param team_id: The team ID.
        :type team_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: str
        :rtype: :class:`TeamMembership`
        """
        url = self.ep()
        ...


    def get_team_membership_details(self, membership_id: str) -> TeamMembership:
        """
        Get Team Membership Details

        Shows details for a team membership, by ID.
        
        Specify the team membership ID in the `membershipId` URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :rtype: :class:`TeamMembership`
        """
        url = self.ep(f'{membership_id}')
        ...


    def update_a_team_membership(self, membership_id: str, is_moderator: str) -> TeamMembership:
        """
        Update a Team Membership

        Updates a team membership, by ID.
        
        Specify the team membership ID in the `membershipId` URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: str
        :rtype: :class:`TeamMembership`
        """
        url = self.ep(f'{membership_id}')
        ...


    def delete_a_team_membership(self, membership_id: str):
        """
        Delete a Team Membership

        Deletes a team membership, by ID.
        
        Specify the team membership ID in the `membershipId` URI parameter.
        
        The team membership for the last moderator of a team may not be deleted; `promote another user
        <https://developer.webex.com/docs/api/v1/team-memberships/update-a-team-membership>`_ to team moderator
        first.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :rtype: None
        """
        url = self.ep(f'{membership_id}')
        ...

    ...