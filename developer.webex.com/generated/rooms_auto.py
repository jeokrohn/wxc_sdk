from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateRoomBody', 'GetRoomMeetingDetailsResponse', 'ListRoomsResponse', 'Room', 'RoomsApi', 'Type']


class Type(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class CreateRoomBody(ApiModel):
    #: A user-friendly name for the room.
    title: Optional[str]
    #: The ID for the team with which this room is associated.
    team_id: Optional[str]
    #: The classificationId for the room.
    classification_id: Optional[str]
    #: Set the space as locked/moderated and the creator becomes a moderator
    is_locked: Optional[bool]
    #: The room is public and therefore discoverable within the org. Anyone can find and join that room. When true the
    #: description must be filled in.
    is_public: Optional[bool]
    #: The description of the space.
    description: Optional[str]
    #: Sets the space into announcement Mode.
    is_announcement_only: Optional[bool]


class Room(CreateRoomBody):
    #: A unique identifier for the room.
    id: Optional[str]
    #: The room type.
    type: Optional[Type]
    #: The date and time of the room's last activity.
    last_activity: Optional[str]
    #: The ID of the person who created this room.
    creator_id: Optional[str]
    #: The date and time the room was created.
    created: Optional[str]
    #: The ID of the organization which owns this room. See Webex Data in the Compliance Guide for more information.
    owner_id: Optional[str]
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in
    #: this space, while maintaing historical data.
    is_read_only: Optional[bool]
    #: Date and time when the room was made public.
    made_public: Optional[str]


class ListRoomsResponse(ApiModel):
    items: Optional[list[Room]]


class GetRoomMeetingDetailsResponse(ApiModel):
    #: A unique identifier for the room.
    room_id: Optional[str]
    #: The Webex meeting URL for the room.
    meeting_link: Optional[str]
    #: The SIP address for the room.
    sip_address: Optional[str]
    #: The Webex meeting number for the room.
    meeting_number: Optional[str]
    #: The Webex meeting ID for the room.
    meeting_id: Optional[str]
    #: The toll-free PSTN number for the room.
    call_in_toll_free_number: Optional[str]
    #: The toll (local) PSTN number for the room.
    call_in_toll_number: Optional[str]


class UpdateRoomBody(CreateRoomBody):
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in
    #: this space, while maintaing historical data.
    is_read_only: Optional[bool]


class RoomsApi(ApiChild, base='rooms'):
    """
    Rooms are virtual meeting places where people post messages and collaborate to get work done. This API is used to
    manage the rooms themselves. Rooms are created and deleted with this API. You can also update a room to change its
    title or make it public, for example.
    To create a team room, specify the a teamId in the POST payload. Note that once a room is added to a team, it
    cannot be moved. To learn more about managing teams, see the Teams API.
    To manage people in a room see the Memberships API.
    To post content see the Messages API.
    """

    def list(self, team_id: str = None, type_: str = None, org_public_spaces: bool = None, from_: str = None, to_: str = None, sort_by: str = None, **params) -> Generator[Room, None, None]:
        """
        List rooms.
        The title of the room for 1:1 rooms will be the display name of the other person. When a Compliance Officer
        lists 1:1 rooms, the "other" person cannot be determined. This means that the room's title may not be filled
        in. Please use the memberships API to list the people in the space.
        By default, lists rooms to which the authenticated user belongs.
        Long result sets will be split into pages.
        Known Limitations:
        The underlying database does not support natural sorting by lastactivity and will only sort on limited set of
        results, which are pulled from the database in order of roomId. For users or bots in more than 3000 spaces this
        can result in anomalies such as spaces that have had recent activity not being returned in the results when
        sorting by lastacivity.

        :param team_id: List rooms associated with a team, by ID. Cannot be set in combination with orgPublicSpaces.
        :type team_id: str
        :param type_: List rooms by type. Cannot be set in combination with orgPublicSpaces. Possible values: direct,
            group
        :type type_: str
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted
            by the madePublic timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See madePublic timestamp
        :type from_: str
        :param to_: Filters rooms, that were made public before this time. See maePublic timestamp
        :type to_: str
        :param sort_by: Sort results. Cannot be set in combination with orgPublicSpaces. Possible values: id,
            lastactivity, created
        :type sort_by: str

        documentation: https://developer.webex.com/docs/api/v1/rooms/list-rooms
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type_ is not None:
            params['type'] = type_
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = str(org_public_spaces).lower()
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if sort_by is not None:
            params['sortBy'] = sort_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Room, params=params)

    def create(self, title: str, team_id: str = None, classification_id: str = None, is_locked: bool = None, is_public: bool = None, description: str = None, is_announcement_only: bool = None) -> Room:
        """
        Creates a room. The authenticated user is automatically added as a member of the room. See the Memberships API
        to learn how to add more people to the room.
        To create a 1:1 room, use the Create Messages endpoint to send a message directly to another person by using
        the toPersonId or toPersonEmail parameters.
        Bots are not able to create and simultaneously classify a room. A bot may update a space classification after a
        person of the same owning organization joined the space as the first human user.
        A space can only be put into announcement mode when it is locked.

        :param title: A user-friendly name for the room.
        :type title: str
        :param team_id: The ID for the team with which this room is associated.
        :type team_id: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that
            room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool

        documentation: https://developer.webex.com/docs/api/v1/rooms/create-a-room
        """
        body = CreateRoomBody()
        if title is not None:
            body.title = title
        if team_id is not None:
            body.team_id = team_id
        if classification_id is not None:
            body.classification_id = classification_id
        if is_locked is not None:
            body.is_locked = is_locked
        if is_public is not None:
            body.is_public = is_public
        if description is not None:
            body.description = description
        if is_announcement_only is not None:
            body.is_announcement_only = is_announcement_only
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Room.parse_obj(data)

    def details(self, room_id: str) -> Room:
        """
        Shows details for a room, by ID.
        The title of the room for 1:1 rooms will be the display name of the other person.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str

        documentation: https://developer.webex.com/docs/api/v1/rooms/get-room-details
        """
        url = self.ep(f'{room_id}')
        data = super().get(url=url)
        return Room.parse_obj(data)

    def meeting_details(self, room_id: str) -> GetRoomMeetingDetailsResponse:
        """
        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in
        numbers.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str

        documentation: https://developer.webex.com/docs/api/v1/rooms/get-room-meeting-details
        """
        url = self.ep(f'{room_id}/meetingInfo')
        data = super().get(url=url)
        return GetRoomMeetingDetailsResponse.parse_obj(data)

    def update(self, room_id: str, title: str, team_id: str = None, classification_id: str = None, is_locked: bool = None, is_public: bool = None, description: str = None, is_announcement_only: bool = None, is_read_only: bool = None) -> Room:
        """
        Updates details for a room, by ID.
        Specify the room ID in the roomId parameter in the URI.
        A space can only be put into announcement mode when it is locked.
        Any space participant or compliance officer can convert a space from public to private. Only a compliance
        officer can convert a space from private to public and only if the space is classified with the lowest category
        (usually public), and the space has a description.
        To remove a description please use a space character by itself.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :param title: A user-friendly name for the room.
        :type title: str
        :param team_id: The ID for the team with which this room is associated.
        :type team_id: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that
            room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool
        :param is_read_only: A compliance officer can set a direct room as read-only, which will disallow any new
            information exchanges in this space, while maintaing historical data.
        :type is_read_only: bool

        documentation: https://developer.webex.com/docs/api/v1/rooms/update-a-room
        """
        body = UpdateRoomBody()
        if title is not None:
            body.title = title
        if team_id is not None:
            body.team_id = team_id
        if classification_id is not None:
            body.classification_id = classification_id
        if is_locked is not None:
            body.is_locked = is_locked
        if is_public is not None:
            body.is_public = is_public
        if description is not None:
            body.description = description
        if is_announcement_only is not None:
            body.is_announcement_only = is_announcement_only
        if is_read_only is not None:
            body.is_read_only = is_read_only
        url = self.ep(f'{room_id}')
        data = super().put(url=url, data=body.json())
        return Room.parse_obj(data)

    def delete(self, room_id: str):
        """
        Deletes a room, by ID. Deleted rooms cannot be recovered.
        As a security measure to prevent accidental deletion, when a non moderator deletes the room they are removed
        from the room instead.
        Deleting a room that is part of a team will archive the room instead.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str

        documentation: https://developer.webex.com/docs/api/v1/rooms/delete-a-room
        """
        url = self.ep(f'{room_id}')
        super().delete(url=url)
        return
