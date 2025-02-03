from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['TeamMembership', 'TeamMembershipsApi']


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


class TeamMembershipsApi(ApiChild, base='team/memberships'):
    """
    Team Memberships
    
    Manipulating Team Memberships as a Compliance Officer
    
    As a Compliance Officer, you can indirectly manage the memberships of a team to which you do not belong.
    Individuals added to the team's general space are automatically considered team members. Therefore, you can
    utilize your standard privilege of adding individuals to a space or room by adding them to the team's general
    space.
    
    The team ID contains the general room ID with a different prefix. To locate the general room ID of a team, you need
    to decode and recode the team ID using the new prefix. Below is a command-line example for this process. Note that
    the final sed replacement is used to remove padding characters.
    
    Example: echo "Y2lzY29zcGFyazovL3VzL1RFQU0vYjQ5ODhmODAtN2QzMS0xMWVkLTk4Y2MtNWY5MTFhZWU1OTA0" | base64 -d | sed
    's/TEAM/ROOM/' | base64 | sed 's/\=.//'
    """

    def list_team_memberships(self, team_id: str, **params) -> Generator[TeamMembership, None, None]:
        """
        List Team Memberships

        Lists all team memberships for a given team, specified by the `teamId` query parameter.

        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str
        :return: Generator yielding :class:`TeamMembership` instances
        """
        params['teamId'] = team_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TeamMembership, item_key='items', params=params)

    def create_a_team_membership(self, team_id: str, person_id: str = None, person_email: str = None,
                                 is_moderator: bool = None) -> TeamMembership:
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
        :type is_moderator: bool
        :rtype: :class:`TeamMembership`
        """
        body = dict()
        body['teamId'] = team_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = super().post(url, json=body)
        r = TeamMembership.model_validate(data)
        return r

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
        data = super().get(url)
        r = TeamMembership.model_validate(data)
        return r

    def update_a_team_membership(self, membership_id: str, is_moderator: bool) -> TeamMembership:
        """
        Update a Team Membership

        Updates a team membership, by ID.

        Specify the team membership ID in the `membershipId` URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: bool
        :rtype: :class:`TeamMembership`
        """
        body = dict()
        body['isModerator'] = is_moderator
        url = self.ep(f'{membership_id}')
        data = super().put(url, json=body)
        r = TeamMembership.model_validate(data)
        return r

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
        super().delete(url)
