from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ListRoomsSortBy', 'Room', 'RoomMeetingDetails', 'RoomType', 'RoomsApi']


class RoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class Room(ApiModel):
    #: A unique identifier for the room.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    id: Optional[str] = None
    #: A user-friendly name for the room.
    #: example: Project Unicorn - Sprint 0
    title: Optional[str] = None
    #: The room type.
    #: example: group
    type: Optional[RoomType] = None
    #: Whether the room is moderated (locked) or not.
    #: example: True
    is_locked: Optional[bool] = None
    #: The ID for the team with which this room is associated.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNjRlNDVhZTAtYzQ2Yi0xMWU1LTlkZjktMGQ0MWUzNDIxOTcz
    team_id: Optional[str] = None
    #: The date and time of the room's last activity.
    #: example: 2016-04-21T19:12:48.920Z
    last_activity: Optional[datetime] = None
    #: The ID of the person who created this room.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creator_id: Optional[str] = None
    #: The date and time the room was created.
    #: example: 2016-04-21T19:01:55.966Z
    created: Optional[datetime] = None
    #: The ID of the organization which owns this room. See `Webex Data
    #: <https://developer.webex.com/docs/api/guides/compliance#webex-teams-data>`_ in the `Compliance Guide
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    owner_id: Optional[str] = None
    #: Space classification ID represents the space's current classification.  It can be attached during space creation
    #: time, and can be modified at the request of an authorized user.
    #: example: Y2lzY29zcGFyazovL3VzL0NMQVNTSUZJQ0FUSU9OL2YyMDUyZTgyLTU0ZjgtMTFlYS1hMmUzLTJlNzI4Y2U4ODEyNQ
    classification_id: Optional[str] = None
    #: Indicates when a space is in Announcement Mode where only moderators can post messages
    is_announcement_only: Optional[bool] = None
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in
    #: this space, while maintaing historical data.
    is_read_only: Optional[bool] = None
    #: The room is public and therefore discoverable within the org. Anyone can find and join that room.
    #: example: True
    is_public: Optional[bool] = None
    #: Date and time when the room was made public.
    #: example: 2022-10-10T17:24:19.388Z
    made_public: Optional[datetime] = None
    #: The description of the space.
    #: example: Company Announcements
    description: Optional[str] = None


class RoomMeetingDetails(ApiModel):
    #: A unique identifier for the room.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The Webex meeting URL for the room.
    #: example: https://cisco.webex.com/m/37a7d3a8-6563-487f-9577-cd029101c087
    meeting_link: Optional[str] = None
    #: The SIP address for the room.
    #: example: 201632887@cisco.webex.com
    sip_address: Optional[str] = None
    #: The Webex meeting number for the room.
    #: example: 201632887
    meeting_number: Optional[str] = None
    #: The Webex meeting ID for the room.
    #: example: c1c30b52501b4d34aa75a57bdb867853
    meeting_id: Optional[str] = None
    #: The toll-free PSTN number for the room.
    #: example: +1-866-432-9903
    call_in_toll_free_number: Optional[str] = None
    #: The toll (local) PSTN number for the room.
    #: example: +1-408-525-6800
    call_in_toll_number: Optional[str] = None


class ListRoomsSortBy(str, Enum):
    id = 'id'
    lastactivity = 'lastactivity'
    created = 'created'


class RoomsApi(ApiChild, base='rooms'):
    """
    Rooms
    
    Rooms are virtual meeting places where people post messages and collaborate to get work done. This API is used to
    manage the rooms themselves. Rooms are created and deleted with this API. You can also update a room to change its
    title or make it public, for example.
    
    To create a team room, specify the a `teamId` in the `POST` payload. Note that once a room is added to a team, it
    cannot be moved. To learn more about managing teams, see the `Teams API
    <https://developer.webex.com/docs/api/v1/teams>`_.
    
    To manage people in a room see the `Memberships API
    <https://developer.webex.com/docs/api/v1/memberships>`_.
    
    To post content see the `Messages API
    <https://developer.webex.com/docs/api/v1/messages>`_.
    """

    def list_rooms(self, team_id: str = None, type: RoomType = None, org_public_spaces: bool = None, from_: Union[str,
                   datetime] = None, to_: Union[str, datetime] = None, sort_by: ListRoomsSortBy = None,
                   **params) -> Generator[Room, None, None]:
        """
        List Rooms

        List rooms to which the authenticated user belongs to.

        The `title` of the room for 1:1 rooms will be the display name of the other person. Please use the
        `memberships API
        <https://developer.webex.com/docs/api/v1/memberships>`_ to list the people in the space.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        Known Limitations:
        The underlying database does not support natural sorting by `lastactivity` and will only sort on limited set of
        results, which are pulled from the database in order of `roomId`. For users or bots in more than 3000 spaces
        this can result in anomalies such as spaces that have had recent activity not being returned in the results
        when sorting by `lastacivity`.

        :param team_id: List rooms associated with a team, by ID. Cannot be set in combination with `orgPublicSpaces`.
        :type team_id: str
        :param type: List rooms by type. Cannot be set in combination with `orgPublicSpaces`.
        :type type: RoomType
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted
            by the `madePublic` timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See `madePublic` timestamp
        :type from_: Union[str, datetime]
        :param to_: Filters rooms, that were made public before this time. See `maePublic` timestamp
        :type to_: Union[str, datetime]
        :param sort_by: Sort results. Cannot be set in combination with `orgPublicSpaces`.
        :type sort_by: ListRoomsSortBy
        :return: Generator yielding :class:`Room` instances
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type is not None:
            params['type'] = enum_str(type)
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = str(org_public_spaces).lower()
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if sort_by is not None:
            params['sortBy'] = enum_str(sort_by)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Room, item_key='items', params=params)

    def create_a_room(self, title: str, team_id: str = None, classification_id: str = None, is_locked: bool = None,
                      is_public: bool = None, description: str = None, is_announcement_only: bool = None) -> Room:
        """
        Create a Room

        Creates a room. The authenticated user is automatically added as a member of the room. See the `Memberships API
        <https://developer.webex.com/docs/api/v1/memberships>`_
        to learn how to add more people to the room.

        To create a 1:1 room, use the `Create Messages
        <https://developer.webex.com/docs/api/v1/messages/create-a-message>`_ endpoint to send a message directly to another person by using
        the `toPersonId` or `toPersonEmail` parameters.

        Bots are not able to create and simultaneously classify a room. A bot may update a space classification after a
        person of the same owning organization joined the space as the first human user.
        A space can only be put into announcement mode when it is locked.

        :param title: A user-friendly name for the room.
        :type title: str
        :param team_id: The ID for the team with which this room is associated.
        :type team_id: str
        :param classification_id: The `classificationId` for the room.
        :type classification_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that
            room. When `true` the `description` must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool
        :rtype: :class:`Room`
        """
        body = dict()
        body['title'] = title
        if team_id is not None:
            body['teamId'] = team_id
        if classification_id is not None:
            body['classificationId'] = classification_id
        if is_locked is not None:
            body['isLocked'] = is_locked
        if is_public is not None:
            body['isPublic'] = is_public
        if description is not None:
            body['description'] = description
        if is_announcement_only is not None:
            body['isAnnouncementOnly'] = is_announcement_only
        url = self.ep()
        data = super().post(url, json=body)
        r = Room.model_validate(data)
        return r

    def get_room_details(self, room_id: str) -> Room:
        """
        Get Room Details

        Shows details for a room, by ID.

        The `title` of the room for 1:1 rooms will be the display name of the other person. When a Compliance Officer
        lists 1:1 rooms, the "other" person cannot be determined. This means that the room's title may not be filled
        in and instead shows "Empty Title". Please use the `memberships API
        <https://developer.webex.com/docs/api/v1/memberships>`_ to list the other person in the space.

        Specify the room ID in the `roomId` parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :rtype: :class:`Room`
        """
        url = self.ep(f'{room_id}')
        data = super().get(url)
        r = Room.model_validate(data)
        return r

    def get_room_meeting_details(self, room_id: str) -> RoomMeetingDetails:
        """
        Get Room Meeting Details

        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in
        numbers.

        Specify the room ID in the `roomId` parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :rtype: :class:`RoomMeetingDetails`
        """
        url = self.ep(f'{room_id}/meetingInfo')
        data = super().get(url)
        r = RoomMeetingDetails.model_validate(data)
        return r

    def update_a_room(self, room_id: str, title: str, classification_id: str = None, team_id: str = None,
                      is_locked: bool = None, is_public: bool = None, description: str = None,
                      is_announcement_only: bool = None, is_read_only: bool = None) -> Room:
        """
        Update a Room

        Updates details for a room, by ID.

        Specify the room ID in the `roomId` parameter in the URI.
        A space can only be put into announcement mode when it is locked.
        Any space participant or compliance officer can convert a space from public to private. Only a compliance
        officer can convert a space from private to public and only if the space is classified with the lowest
        category (usually `public`), and the space has a description.
        To remove a `description` please use a space character ` ` by itself.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :param title: A user-friendly name for the room.
        :type title: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param team_id: The teamId to which this space should be assigned. Only unowned spaces can be assigned to a
            team. Assignment between teams is unsupported.
        :type team_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that
            room. When `true` the `description` must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into Announcement Mode or clears the Anouncement Mode (`false`)
        :type is_announcement_only: bool
        :param is_read_only: A compliance officer can set a direct room as read-only, which will disallow any new
            information exchanges in this space, while maintaing historical data.
        :type is_read_only: bool
        :rtype: :class:`Room`
        """
        body = dict()
        body['title'] = title
        if classification_id is not None:
            body['classificationId'] = classification_id
        if team_id is not None:
            body['teamId'] = team_id
        if is_locked is not None:
            body['isLocked'] = is_locked
        if is_public is not None:
            body['isPublic'] = is_public
        if description is not None:
            body['description'] = description
        if is_announcement_only is not None:
            body['isAnnouncementOnly'] = is_announcement_only
        if is_read_only is not None:
            body['isReadOnly'] = is_read_only
        url = self.ep(f'{room_id}')
        data = super().put(url, json=body)
        r = Room.model_validate(data)
        return r

    def delete_a_room(self, room_id: str):
        """
        Delete a Room

        Deletes a room, by ID. Deleted rooms cannot be recovered.
        As a security measure to prevent accidental deletion, when a non moderator deletes the room they are removed
        from the room instead.

        Deleting a room that is part of a team will archive the room instead.

        Specify the room ID in the `roomId` parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :rtype: None
        """
        url = self.ep(f'{room_id}')
        super().delete(url)
