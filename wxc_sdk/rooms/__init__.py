"""
Rooms API
"""

from collections.abc import Generator
from datetime import datetime
from typing import Any, Optional, Union

from dateutil.parser import isoparse

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.common import RoomType

__all__ = ['Room', 'RoomsApi']


class Room(ApiModel):
    #: A unique identifier for the room.
    id: Optional[str] = None
    #: A user-friendly name for the room.
    title: Optional[str] = None
    #: The room type.
    type: Optional[RoomType] = None
    #: Whether the room is moderated (locked) or not.
    is_locked: Optional[bool] = None
    #: The ID for the team with which this room is associated.
    team_id: Optional[str] = None
    #: The date and time of the room's last activity.
    last_activity: Optional[datetime] = None
    #: The ID of the person who created this room.
    creator_id: Optional[str] = None
    #: The date and time the room was created.
    created: Optional[datetime] = None
    #: The ID of the organization which owns this room. See `Webex Data
    #: <https://developer.webex.com/docs/api/guides/compliance#webex-teams-data>`_ in the `Compliance Guide
    owner_id: Optional[str] = None
    #: Space classification ID represents the space's current classification.  It can be attached during space creation
    #: time, and can be modified at the request of an authorized user.
    classification_id: Optional[str] = None
    #: Indicates when a space is in Announcement Mode where only moderators can post messages
    is_announcement_only: Optional[bool] = None
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in
    #: this space, while maintaing historical data.
    is_read_only: Optional[bool] = None
    #: The room is public and therefore discoverable within the org. Anyone can find and join that room.
    is_public: Optional[bool] = None
    #: Date and time when the room was made public.
    made_public: Optional[datetime] = None
    #: The description of the space.
    description: Optional[str] = None


class RoomsApi(ApiChild, base='rooms'):
    """
    Rooms are virtual meeting places where people post messages and collaborate to get work done. This API is used to
    manage the rooms themselves. Rooms are created and deleted with this API. You can also update a room to change
    its title, for example.
    To create a team room, specify the a teamId in the POST payload. Note that once a room is added to a team,
    it cannot be moved. To learn more about managing teams, see the Teams API.
    To manage people in a room see the Memberships API.
    To post content see the Messages API.
    """

    def list(
        self,
        team_id: str = None,
        type_: RoomType = None,
        org_public_spaces: bool = None,
        from_: Union[str, datetime] = None,
        to_: Union[str, datetime] = None,
        sort_by: str = None,
        **params: Any,
    ) -> Generator[Room, None, None]:
        """
        List rooms.

        The title of the room for 1:1 rooms will be the display name of the other person.
        By default, lists rooms to which the authenticated user belongs.

        Long result sets will be split into pages.

        Known Limitations:

        The underlying database does not support natural sorting by lastactivity and will only sort on limited set of
        results, which are pulled from the database in order of roomId. For users or bots in more than 3000 spaces
        this can result in anomalies such as spaces that have had recent activity not being returned in the results
        when sorting by lastacivity.

        :param team_id: List rooms associated with a team, by ID.
        :type team_id: str
        :param type_: List rooms by type.
            Possible values: direct, group
        :type type_: RoomType
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted
            by the madePublic timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See madePublic timestamp
        :type from_: Union[str, datetime]
        :param to_: Filters rooms, that were made public before this time. See maePublic timestamp
        :type to_: Union[str, datetime]
        :param sort_by: Sort results.
            Possible values: id, lastactivity, created
        :type sort_by: str
        :return: Generator yielding :class:`Room` instances
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type_ is not None:
            params['type'] = enum_str(type_)
        if sort_by is not None:
            params['sortBy'] = sort_by
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = org_public_spaces
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Room, params=params)

    def create(
        self,
        title: str,
        team_id: str = None,
        classification_id: str = None,
        is_locked: bool = None,
        is_public: bool = None,
        description: str = None,
        is_announcement_only: bool = None,
    ) -> Room:
        """
        Create a Room

        Creates a room. The authenticated user is automatically added as a member of the room. See the `Memberships API
        <https://developer.webex.com/docs/api/v1/memberships>`_
        to learn how to add more people to the room.

        To create a 1:1 room, use the `Create Messages
        <https://developer.webex.com/docs/api/v1/messages/create-a-message>`_ endpoint to send a message directly to
        another person by using the `toPersonId` or `toPersonEmail` parameters.

        Bots are not able to create and simultaneously classify a room. A bot may update a space classification after
        a person of the same owning organization joined the space as the first human user.
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
            room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool
        :rtype: :class:`Room`
        """
        body: dict[str, Any] = {}
        if title is not None:
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
        data = super().post(url=url, json=body)
        return Room.model_validate(data)

    def details(self, room_id: str) -> Room:
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
        data = super().get(url=url)
        return Room.model_validate(data)

    def update(self, update: Room) -> Room:
        """
        Updates details for a room, by ID.

        Specify the room ID in the `roomId` parameter in the URI.

        A space can only be put into announcement mode when it is locked.

        Any space participant or compliance officer can convert a space from public to private. Only a compliance
        officer can convert a space from private to public and only if the space is classified with the lowest
        category (usually `public`), and the space has a description.

        To remove a `description` please use a space character ` ` by itself.

        When using this method for moving a space under a team, ensure that all moderators in
        the space are also team members. If a moderator is not part of the team, demote or remove them as a moderator.
        Alternatively, add the non-team moderators to the team. This ensures compliance with the requirement that all
        space moderators must be team members for successful operation execution.

        :update: update to apply. ID and title have to be set. Only can update:
        :rtype: :class:`Room`
        """
        data = update.model_dump(
            mode='json',
            by_alias=True,
            exclude_none=True,
            include={
                'title',
                'classification_id',
                'team_id',
                'is_locked',
                'is_public',
                'description',
                'is_announcement_only',
                'is_read_only',
            },
        )
        if update.id is None:
            raise ValueError('ID has to be set')
        url = self.ep(f'{update.id}')
        data = super().put(url=url, json=data)  # type: ignore[assignment]
        return Room.model_validate(data)

    def delete(self, room_id: str) -> None:  # type: ignore[override]
        """
        Delete a Room

        Deletes a room, by ID. Deleted rooms cannot be recovered.
        As a security measure to prevent accidental deletion, when a non moderator deletes the room they are removed
        from the room instead.

        Deleting a room that is part of a team will archive the room instead.

        A Compliance Officer has no special privileges, i.e. they cannot delete rooms they are not part of.

        Specify the room ID in the `roomId` parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :rtype: None
        """
        url = self.ep(f'{room_id}')
        super().delete(url=url)
        return
