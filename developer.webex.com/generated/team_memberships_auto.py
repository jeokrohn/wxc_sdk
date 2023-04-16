from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateTeamMembershipBody', 'ListTeamMembershipsResponse', 'TeamMembership', 'TeamMembershipsApi']


class CreateTeamMembershipBody(ApiModel):
    #: The team ID.
    team_id: Optional[str]
    #: The person ID.
    person_id: Optional[str]
    #: The email address of the person.
    person_email: Optional[str]
    #: Whether or not the participant is a team moderator.
    is_moderator: Optional[bool]


class TeamMembership(CreateTeamMembershipBody):
    #: A unique identifier for the team membership.
    id: Optional[str]
    #: The display name of the person.
    person_display_name: Optional[str]
    #: The organization ID of the person.
    person_org_id: Optional[str]
    #: The date and time when the team membership was created.
    created: Optional[str]


class ListTeamMembershipsResponse(ApiModel):
    items: Optional[list[TeamMembership]]


class UpdateTeamMembershipBody(ApiModel):
    #: Whether or not the participant is a team moderator.
    is_moderator: Optional[bool]


class TeamMembershipsApi(ApiChild, base='team/memberships'):
    """
    Team Memberships represent a person's relationship to a team. Use this API to list members of any team that you're
    in or create memberships to invite someone to a team. Team memberships can also be updated to make someone a
    moderator or deleted to remove them from the team.
    Just like in the Webex app, you must be a member of the team in order to list its memberships or invite people.
    """

    def list_memberships(self, team_id: str, **params) -> Generator[TeamMembership, None, None]:
        """
        Lists all team memberships for a given team, specified by the teamId query parameter.
        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str

        documentation: https://developer.webex.com/docs/api/v1/team-memberships/list-team-memberships
        """
        params['teamId'] = team_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TeamMembership, params=params)

    def create_membership(self, team_id: str, person_id: str = None, person_email: str = None, is_moderator: bool = None) -> TeamMembership:
        """
        Add someone to a team by Person ID or email address, optionally making them a moderator.

        :param team_id: The team ID.
        :type team_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: bool

        documentation: https://developer.webex.com/docs/api/v1/team-memberships/create-a-team-membership
        """
        body = CreateTeamMembershipBody()
        if team_id is not None:
            body.team_id = team_id
        if person_id is not None:
            body.person_id = person_id
        if person_email is not None:
            body.person_email = person_email
        if is_moderator is not None:
            body.is_moderator = is_moderator
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return TeamMembership.parse_obj(data)

    def membership_details(self, membership_id: str) -> TeamMembership:
        """
        Shows details for a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str

        documentation: https://developer.webex.com/docs/api/v1/team-memberships/get-team-membership-details
        """
        url = self.ep(f'{membership_id}')
        data = super().get(url=url)
        return TeamMembership.parse_obj(data)

    def update_membership(self, membership_id: str, is_moderator: bool) -> TeamMembership:
        """
        Updates a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: bool

        documentation: https://developer.webex.com/docs/api/v1/team-memberships/update-a-team-membership
        """
        body = UpdateTeamMembershipBody()
        if is_moderator is not None:
            body.is_moderator = is_moderator
        url = self.ep(f'{membership_id}')
        data = super().put(url=url, data=body.json())
        return TeamMembership.parse_obj(data)

    def delete_membership(self, membership_id: str):
        """
        Deletes a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.
        The team membership for the last moderator of a team may not be deleted; promote another user to team moderator
        first.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str

        documentation: https://developer.webex.com/docs/api/v1/team-memberships/delete-a-team-membership
        """
        url = self.ep(f'{membership_id}')
        super().delete(url=url)
        return
