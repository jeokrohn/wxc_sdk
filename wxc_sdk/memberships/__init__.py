"""
Membership API
"""
from collections.abc import Generator
from datetime import datetime
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common import RoomType
from wxc_sdk.webhook import WebhookEventData

__all__ = ['Membership', 'MembershipsData', 'MembershipApi']


class Membership(ApiModel):
    #: A unique identifier for the membership.
    id: Optional[str] = None
    #: The room ID.
    room_id: Optional[str] = None
    #: The person ID.
    person_id: Optional[str] = None
    #: The email address of the person.
    person_email: Optional[str] = None
    #: The display name of the person.
    person_display_name: Optional[str] = None
    #: The organization ID of the person.
    person_org_id: Optional[str] = None
    #: Whether or not the participant is a room moderator.
    is_moderator: Optional[bool] = None
    #: Whether or not the direct type room is hidden in the Webex clients.
    is_room_hidden: Optional[bool] = None
    #: The type of room the membership is associated with.
    room_type: Optional[RoomType] = None
    #: Whether or not the participant is a monitoring bot (deprecated).
    is_monitor: Optional[bool] = None
    #: The date and time when the membership was created.
    created: Optional[datetime] = None

    def update(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               include={'is_moderator', 'is_room_hidden'})


class MembershipsData(WebhookEventData, Membership):
    """
    Data in a webhook "memberships" event
    """
    resource = 'memberships'


class MembershipApi(ApiChild, base='memberships'):
    """
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

    def list(self, room_id: str = None, person_id: str = None, person_email: str = None,
             **params) -> Generator[Membership, None, None]:
        """
        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.
        Use query parameters to filter the response.
        Use roomId to list memberships for a room, by ID.
        NOTE: For moderated team spaces, the list of memberships will include only the space moderators if the user
        is a team member but not a direct participant of the space.
        Use either personId or personEmail to filter the results. The roomId parameter is required when using these
        parameters.
        Long result sets will be split into pages.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The roomId parameter is required
            when using this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The roomId parameter
            is required when using this parameter.
        :type person_email: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Membership, params=params)

    def create(self, room_id: str, person_id: str = None, person_email: str = None,
               is_moderator: bool = None) -> Membership:
        """
        Add someone to a room by Person ID or email address, optionally making them a moderator.

        :param room_id: The room ID.
        :type room_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a room moderator.
        :type is_moderator: bool
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = super().post(url=url, json=body)
        return Membership.model_validate(data)

    def details(self, membership_id: str) -> Membership:
        """
        Get details for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = super().get(url=url)
        return Membership.model_validate(data)

    def update(self, update: Membership) -> Membership:
        """
        Updates properties for a membership by ID

        :param update: new settings; ID has to be set in update.

            These can be updated:
                is_moderator: bool: Whether or not the participant is a room moderator.

                is_room_hidden: bool: When set to true, hides direct spaces in the teams client. Any new message will
                make the room visible again.
        :type update: Membership

        """
        if update.id is None:
            raise ValueError('ID has to be set')
        data = update.update()
        url = self.ep(f'{update.id}')
        data = super().put(url=url, json=data)
        return Membership.model_validate(data)

    def delete(self, membership_id: str):
        """
        Deletes a membership by ID.
        Specify the membership ID in the membershipId URI parameter.
        The membership for the last moderator of a Team's General space may not be deleted; promote another user to
        team moderator first.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        super().delete(url=url)
        return
