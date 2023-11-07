from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
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
    ...