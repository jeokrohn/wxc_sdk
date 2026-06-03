import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Membership', 'MembershipRoomType', 'MembershipsApi']


class MembershipRoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


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
    room_type: Optional[MembershipRoomType] = None
    #: Whether or not the participant is a monitoring bot (deprecated).
    is_monitor: Optional[bool] = None
    #: The date and time when the membership was created.
    created: Optional[datetime] = None


class MembershipsApi(ApiChild, base='memberships'):
    """
    Memberships
    
    Memberships represent a person's relationship to a room. Use this API to list members of any room that you're in or
    create memberships to invite someone to a room. Compliance Officers can now also list memberships for
    `personEmails` where the CO is not part of the room.
    Memberships can also be updated to make someone a moderator, or deleted, to remove someone from the room.
    
    Just like in the Webex client, you must be a member of the room in order to list its memberships or invite people.
    """

    def list_memberships(self, room_id: str = None, person_id: str = None, person_email: str = None,
                         **params: Any) -> Generator[Membership, None, None]:
        """
        List Memberships

        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.

        Use query parameters to filter the response.

        Use `roomId` to list memberships for a room, by ID.

        **NOTE**: For moderated team spaces, the list of memberships will include only the space moderators if the user
        is a team member but not a direct participant of the space.

        Use either `personId` or `personEmail` to filter the results. The `roomId` parameter is required when using
        these parameters.

        When the requester is a compliance officer, they can query by `personId` or `personEmail` **WITHOUT**
        specifying a `roomId`. The response will include **ALL** memberships for the user where a space is owned by an
        org to which the user belongs.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The `roomId` parameter is required when
            using this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The `roomId` parameter is
            required when using this parameter.
        :type person_email: str
        :return: Generator yielding :class:`Membership` instances
        """
        if room_id is not None:
            params['roomId'] = room_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Membership, item_key='items', params=params)

    def create_a_membership(self, room_id: str, person_id: str = None, person_email: str = None,
                            is_moderator: bool = None) -> Membership:
        """
        Create a Membership

        Add someone to a room by Person ID or email address, optionally making them a moderator. Compliance Officers
        cannot add people to empty (team) spaces.

        :param room_id: The room ID.
        :type room_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a room moderator.
        :type is_moderator: bool
        :rtype: :class:`Membership`
        """
        body: dict[str, Any] = dict()
        body['roomId'] = room_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = super().post(url, json=body)
        r = Membership.model_validate(data)
        return r

    def delete_a_membership(self, membership_id: str) -> None:
        """
        Delete a Membership

        Deletes a membership by ID.

        Specify the membership ID in the `membershipId` URI parameter.

        The membership for the last moderator of a `Team
        <https://developer.webex.com/docs/api/v1/teams>`_'s General space may not be deleted; `promote another user
        team moderator first.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        :rtype: None
        """
        url = self.ep(f'{membership_id}')
        super().delete(url)

    def get_membership_details(self, membership_id: str) -> Membership:
        """
        Get Membership Details

        Get details for a membership by ID.

        Specify the membership ID in the `membershipId` URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        :rtype: :class:`Membership`
        """
        url = self.ep(f'{membership_id}')
        data = super().get(url)
        r = Membership.model_validate(data)
        return r

    def update_a_membership(self, membership_id: str, is_moderator: bool, is_room_hidden: bool) -> Membership:
        """
        Update a Membership

        Updates properties for a membership by ID.

        Specify the membership ID in the `membershipId` URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a room moderator.
        :type is_moderator: bool
        :param is_room_hidden: When set to true, hides direct spaces in the teams client. Any new message will make the
            room visible again.
        :type is_room_hidden: bool
        :rtype: :class:`Membership`
        """
        body: dict[str, Any] = dict()
        body['isModerator'] = is_moderator
        body['isRoomHidden'] = is_room_hidden
        url = self.ep(f'{membership_id}')
        data = super().put(url, json=body)
        r = Membership.model_validate(data)
        return r
