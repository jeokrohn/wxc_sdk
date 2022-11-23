from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, Enum
from typing import List, Optional
from pydantic import Field


__all__ = ['AttachmentActionsApi', 'CreateAttachmentActionBody', 'CreateAttachmentActionResponse', 'CreateMembershipBody', 'CreateRoomBody', 'CreateRoomTabBody', 'CreateTeamBody', 'CreateTeamMembershipBody', 'CreateWebhookBody', 'Data', 'Event', 'Event2', 'EventResourceEnum', 'EventTypeEnum', 'EventsApi', 'GetAttachmentActionDetailsResponse', 'GetRoomMeetingDetailsResponse', 'Inputs', 'ListEventsResponse', 'ListMembershipsResponse', 'ListRoomTabsResponse', 'ListRoomsResponse', 'ListTeamMembershipsResponse', 'ListTeamsResponse', 'ListWebhooksResponse', 'Membership', 'MembershipsApi', 'Resource', 'Room', 'RoomTab', 'RoomTabsApi', 'RoomType', 'RoomsApi', 'Status', 'Team', 'TeamMembership', 'TeamMembershipsApi', 'TeamsApi', 'Webhook', 'WebhooksApi']


class Inputs(ApiModel):
    name: Optional[str]
    url: Optional[str]
    email: Optional[str]
    tel: Optional[str]


class CreateAttachmentActionBody(ApiModel):
    #: The type of action to perform.
    type: Optional[str]
    #: The ID of the message which contains the attachment.
    message_id: Optional[str]
    #: The attachment action's inputs.
    inputs: Optional[Inputs]


class CreateAttachmentActionResponse(CreateAttachmentActionBody):
    #: A unique identifier for the action.
    id: Optional[str]
    #: The ID of the person who performed the action.
    person_id: Optional[str]
    #: The ID of the room in which the action was performed.
    room_id: Optional[str]
    #: The date and time the action was created.
    created: Optional[str]


class GetAttachmentActionDetailsResponse(CreateAttachmentActionBody):
    #: A unique identifier for the action.
    id: Optional[str]
    #: The ID of the person who performed the action.
    person_id: Optional[str]
    #: The ID of the room in which the action was performed.
    room_id: Optional[str]
    #: The date and time the action was created.
    created: Optional[str]


class AttachmentActionsApi(ApiChild, base='attachment/actions'):
    """
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a card.
    """

    def create_action(self, type_: str, message_id: str, inputs: object) -> CreateAttachmentActionResponse:
        """
        Create a new attachment action.

        :param type_: The type of action to perform.

        :type type_: str
        :param message_id: The ID of the message which contains the attachment.
        :type message_id: str
        :param inputs: The attachment action's inputs.
        :type inputs: object
        """
        body = {}
        if type_ is not None:
            body['type'] = type_
        if message_id is not None:
            body['messageId'] = message_id
        if inputs is not None:
            body['inputs'] = inputs
        url = self.ep()
        data = super().post(url=url, json=body)
        return CreateAttachmentActionResponse.parse_obj(data)

    def action_details(self, id: str) -> GetAttachmentActionDetailsResponse:
        """
        Shows details for a attachment action, by ID.
        Specify the attachment action ID in the id URI parameter.

        :param id: A unique identifier for the attachment action.
        :type id: str
        """
        url = self.ep(f'{id}')
        data = super().get(url=url)
        return GetAttachmentActionDetailsResponse.parse_obj(data)

class EventResourceEnum(str, Enum):
    #: State changed on a messages resource
    messages = 'messages'
    #: State changed on a memberships resource
    memberships = 'memberships'
    #: State change on a meeting ( here combined with type = 'ended' )
    meetings = 'meetings'
    #: State change on a automatic transcript resource for Webex Assistant
    meeting_transcripts = 'meetingTranscripts'
    #: State changed on a meeting message, i.e. message exchanged as part of a meeting
    meeting_messages = 'meetingMessages'
    #: State changed on a room tabs in a space
    tabs = 'tabs'
    #: State changed on a space classification
    rooms = 'rooms'
    #: State changed on a card attachment
    attachment_actions = 'attachmentActions'
    #: State changed on a file download
    files = 'files'
    #: State change on a file preview
    file_transcodings = 'file_transcodings'


class EventTypeEnum(str, Enum):
    #: The resource has been created
    created = 'created'
    #: A property on the resource has been updated
    updated = 'updated'
    #: The resource has been deleted
    deleted = 'deleted'
    #: The meeting has ended
    ended = 'ended'


class Data(ApiModel):
    id: Optional[str]
    room_id: Optional[str]
    room_type: Optional[str]
    org_id: Optional[str]
    text: Optional[str]
    person_id: Optional[str]
    person_email: Optional[str]
    meeting_id: Optional[str]
    creator_id: Optional[str]
    #: The meeting's host data
    host: Optional[object]
    #: Common Identity (CI) authenticated meeting attendees
    attendees: Optional[list[]]
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If true a transcript should be available a couple minutes after the meeting ended at the meetingTranscripts resource
    transcription_enabled: Optional[str]
    #: indicates if recording was enabled for all or parts of the meeting. If true a recording should be available shortly after the meeting ended at the recordings resource
    recording_enabled: Optional[str]
    #: indicates i chat messages were exchanged during the meeting in the meetings client (not the unified client). If true these messages can be accessed by a compliance officer at the postMeetingsChat resource. Meetings chat collection must be custom enabled.
    has_post_meetings_chat: Optional[str]
    created: Optional[str]


class Event(ApiModel):
    #: The unique identifier for the event.
    id: Optional[str]
    #: The type of resource in the event.
    resource: Optional[EventResourceEnum]
    #: The action which took place in the event.
    type: Optional[EventTypeEnum]
    #: The ID of the application for the event.
    app_id: Optional[str]
    #: The ID of the person who performed the action.
    actor_id: Optional[str]
    #: The ID of the organization for the event.
    org_id: Optional[str]
    #: The date and time of the event.
    created: Optional[str]
    #: The event's data representation. This object will contain the event's resource, such as memberships, messages, meetings, tabs, rooms or attachmentActions at the time the event took place.
    data: Optional[Data]


class ListEventsResponse(ApiModel):
    items: Optional[list[Event]]


class EventsApi(ApiChild, base='events'):
    """
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    The Events API can only be used by a Compliance Officer with an API access token that contains the spark-compliance:events_read scope. See the Compliance Guide for more information.
    """

    def list_events(self, resource: str = None, type_: str = None, actor_id: str = None, from_: str = None, to_: str = None, **params) -> Generator[Event, None, None]:
        """
        List events in your organization. Several query parameters are available to filter the events returned in the response.
        Long result sets will be split into pages.

        :param resource: List events with a specific resource type.
Possible values: messages, memberships, meetings, meetingMessages, meetingTranscripts, tabs, rooms, attachmentActions, files, file_transcodings
        :type resource: str
        :param type_: List events with a specific event type.
Possible values: created, updated, deleted, ended
        :type type_: str
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the future, lists events up to the present.
        :type to_: str
        """
        if resource is not None:
            params['resource'] = resource
        if type_ is not None:
            params['type'] = type_
        if actor_id is not None:
            params['actorId'] = actor_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Event, params=params)

    def event_details(self, event_id: str) -> Event:
        """
        Shows details for an event, by event ID.
        Specify the event ID in the eventId parameter in the URI.

        :param event_id: The unique identifier for the event.
        :type event_id: str
        """
        url = self.ep(f'{event_id}')
        data = super().get(url=url)
        return Event.parse_obj(data)

class RoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class CreateMembershipBody(ApiModel):
    #: The room ID.
    room_id: Optional[str]
    #: The person ID.
    person_id: Optional[str]
    #: The email address of the person.
    person_email: Optional[str]
    #: Whether or not the participant is a room moderator.
    is_moderator: Optional[bool]


class Membership(CreateMembershipBody):
    #: A unique identifier for the membership.
    id: Optional[str]
    #: The display name of the person.
    person_display_name: Optional[str]
    #: The organization ID of the person.
    person_org_id: Optional[str]
    #: Whether or not the direct type room is hidden in the Webex clients.
    is_room_hidden: Optional[bool]
    #: The type of room the membership is associated with.
    room_type: Optional[RoomType]
    #: Whether or not the participant is a monitoring bot (deprecated).
    is_monitor: Optional[bool]
    #: The date and time when the membership was created.
    created: Optional[str]


class ListMembershipsResponse(ApiModel):
    items: Optional[list[Membership]]


class UpdateMembershipBody(ApiModel):
    #: Whether or not the participant is a room moderator.
    is_moderator: Optional[bool]
    #: When set to true, hides direct spaces in the teams client. Any new message will make the room visible again.
    is_room_hidden: Optional[bool]


class MembershipsApi(ApiChild, base='memberships'):
    """
    Memberships represent a person's relationship to a room. Use this API to list members of any room that you're in or create memberships to invite someone to a room. Compliance Officers can now also list memberships for personEmails where the CO is not part of the room.
    Memberships can also be updated to make someone a moderator, or deleted, to remove someone from the room.
    Just like in the Webex client, you must be a member of the room in order to list its memberships or invite people.
    """

    def list(self, room_id: str = None, person_id: str = None, person_email: str = None, **params) -> Generator[Membership, None, None]:
        """
        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.
        Use query parameters to filter the response.
        Use roomId to list memberships for a room, by ID.
        NOTE: For moderated team spaces, the list of memberships will include only the space moderators if the user is a team member but not a direct participant of the space.
        Use either personId or personEmail to filter the results. The roomId parameter is required when using these parameters.
        Long result sets will be split into pages.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The roomId parameter is required when using this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The roomId parameter is required when using this parameter.
        :type person_email: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Membership, params=params)

    def create(self, room_id: str, person_id: str = None, person_email: str = None, is_moderator: bool = None) -> Membership:
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
        return Membership.parse_obj(data)

    def details(self, membership_id: str) -> Membership:
        """
        Get details for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = super().get(url=url)
        return Membership.parse_obj(data)

    def update(self, membership_id: str, is_moderator: bool, is_room_hidden: bool) -> Membership:
        """
        Updates properties for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a room moderator.
        :type is_moderator: bool
        :param is_room_hidden: When set to true, hides direct spaces in the teams client. Any new message will make the room visible again.
        :type is_room_hidden: bool
        """
        body = {}
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        if is_room_hidden is not None:
            body['isRoomHidden'] = is_room_hidden
        url = self.ep(f'{membership_id}')
        data = super().put(url=url, json=body)
        return Membership.parse_obj(data)

    def delete(self, membership_id: str):
        """
        Deletes a membership by ID.
        Specify the membership ID in the membershipId URI parameter.
        The membership for the last moderator of a Team's General space may not be deleted; promote another user to team moderator first.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        super().delete(url=url)
        return

class CreateRoomTabBody(ApiModel):
    #: A unique identifier for the room.
    room_id: Optional[str]
    #: URL of the Room Tab. Must use https protocol.
    content_url: Optional[str]
    #: User-friendly name for the room tab.
    display_name: Optional[str]


class RoomTab(CreateRoomTabBody):
    #: A unique identifier for the Room Tab.
    id: Optional[str]
    #: The room type.
    room_type: Optional[RoomType]
    #: The person ID of the person who created this Room Tab.
    creator_id: Optional[str]
    #: The date and time when the Room Tab was created.
    created: Optional[str]


class ListRoomTabsResponse(ApiModel):
    items: Optional[list[RoomTab]]


class RoomTabsApi(ApiChild, base='room/tabs'):
    """
    A Room Tab represents a URL shortcut that is added as a persistent tab to a Webex room (space) tab row. Use this API to list tabs of any Webex room that you belong to. Room Tabs can also be updated to point to a different content URL, or deleted to remove the tab from the room.
    Just like in the Webex app, you must be a member of the room in order to list its Room Tabs.
    """

    def list_tabs(self, room_id: str, **params) -> Generator[ListRoomTabsResponse, None, None]:
        """
        Lists all Room Tabs of a room specified by the roomId query parameter.

        :param room_id: ID of the room for which to list room tabs.
        :type room_id: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListRoomTabsResponse, params=params)

    def create_tab(self, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Add a tab with a specified URL to a room.

        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the Room Tab. Must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if content_url is not None:
            body['contentUrl'] = content_url
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep()
        data = super().post(url=url, json=body)
        return RoomTab.parse_obj(data)

    def tab_details(self, id: str) -> RoomTab:
        """
        Get details for a Room Tab with the specified room tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str
        """
        url = self.ep(f'{id}')
        data = super().get(url=url)
        return RoomTab.parse_obj(data)

    def update_tab(self, id: str, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Updates the content URL of the specified Room Tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str
        :param room_id: ID of the room that contains the room tab in question.
        :type room_id: str
        :param content_url: Content URL of the Room Tab. URL must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if content_url is not None:
            body['contentUrl'] = content_url
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep(f'{id}')
        data = super().put(url=url, json=body)
        return RoomTab.parse_obj(data)

    def delete_tab(self, id: str):
        """
        Deletes a Room Tab with the specified ID.

        :param id: The unique identifier for the Room Tab to delete.
        :type id: str
        """
        url = self.ep(f'{id}')
        super().delete(url=url)
        return

class CreateRoomBody(ApiModel):
    #: A user-friendly name for the room.
    title: Optional[str]
    #: The ID for the team with which this room is associated.
    team_id: Optional[str]
    #: The classificationId for the room.
    classification_id: Optional[str]
    #: Set the space as locked/moderated and the creator becomes a moderator
    is_locked: Optional[bool]
    #: The room is public and therefore discoverable within the org. Anyone can find and join that room. When true the description must be filled in.
    is_public: Optional[bool]
    #: The description of the space.
    description: Optional[str]
    #: Sets the space into announcement Mode.
    is_announcement_only: Optional[bool]


class Room(CreateRoomBody):
    #: A unique identifier for the room.
    id: Optional[str]
    #: The room type.
    type: Optional[RoomType]
    #: The date and time of the room's last activity.
    last_activity: Optional[str]
    #: The ID of the person who created this room.
    creator_id: Optional[str]
    #: The date and time the room was created.
    created: Optional[str]
    #: The ID of the organization which owns this room. See Webex Data in the Compliance Guide for more information.
    owner_id: Optional[str]
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in this space, while maintaing historical data.
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
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in this space, while maintaing historical data.
    is_read_only: Optional[bool]


class RoomsApi(ApiChild, base='rooms'):
    """
    Rooms are virtual meeting places where people post messages and collaborate to get work done. This API is used to manage the rooms themselves. Rooms are created and deleted with this API. You can also update a room to change its title or make it public, for example.
    To create a team room, specify the a teamId in the POST payload. Note that once a room is added to a team, it cannot be moved. To learn more about managing teams, see the Teams API.
    To manage people in a room see the Memberships API.
    To post content see the Messages API.
    """

    def list(self, team_id: str = None, type_: str = None, org_public_spaces: bool = None, from_: str = None, to_: str = None, sort_by: str = None, **params) -> Generator[Room, None, None]:
        """
        List rooms.
        The title of the room for 1:1 rooms will be the display name of the other person.
        By default, lists rooms to which the authenticated user belongs.
        Long result sets will be split into pages.
        Known Limitations:
        The underlying database does not support natural sorting by lastactivity and will only sort on limited set of results, which are pulled from the database in order of roomId. For users or bots in more than 3000 spaces this can result in anomalies such as spaces that have had recent activity not being returned in the results when sorting by lastacivity.

        :param team_id: List rooms associated with a team, by ID. Cannot be set in combination with orgPublicSpaces.
        :type team_id: str
        :param type_: List rooms by type. Cannot be set in combination with orgPublicSpaces.
Possible values: direct, group
        :type type_: str
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted by the madePublic timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See madePublic timestamp
        :type from_: str
        :param to_: Filters rooms, that were made public before this time. See maePublic timestamp
        :type to_: str
        :param sort_by: Sort results. Cannot be set in combination with orgPublicSpaces.
Possible values: id, lastactivity, created
        :type sort_by: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type_ is not None:
            params['type'] = type_
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = org_public_spaces
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
        Creates a room. The authenticated user is automatically added as a member of the room. See the Memberships API to learn how to add more people to the room.
        To create a 1:1 room, use the Create Messages endpoint to send a message directly to another person by using the toPersonId or toPersonEmail parameters.
        Bots are not able to create and classify a room. A bot may update a space classification after a person of the same owning organization joined the space as the first human user.
        A space can only be put into announcement mode when it is locked.

        :param title: A user-friendly name for the room.
        :type title: str
        :param team_id: The ID for the team with which this room is associated.
        :type team_id: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool
        """
        body = {}
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
        return Room.parse_obj(data)

    def details(self, room_id: str) -> Room:
        """
        Shows details for a room, by ID.
        The title of the room for 1:1 rooms will be the display name of the other person.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}')
        data = super().get(url=url)
        return Room.parse_obj(data)

    def meeting_details(self, room_id: str) -> GetRoomMeetingDetailsResponse:
        """
        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in numbers.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}/meetingInfo')
        data = super().get(url=url)
        return GetRoomMeetingDetailsResponse.parse_obj(data)

    def update(self, room_id: str, title: str, classification_id: str = None, team_id: str = None, is_locked: bool = None, is_public: bool = None, description: str = None, is_announcement_only: bool = None, is_read_only: bool = None) -> Room:
        """
        Updates details for a room, by ID.
        Specify the room ID in the roomId parameter in the URI.
        A space can only be put into announcement mode when it is locked.
        Any space participant or compliance officer can convert a space from public to private. Conversion from private to public is currently not supported. To remove a description please use a space character   by itself.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        :param title: A user-friendly name for the room.
        :type title: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param team_id: The teamId to which this space should be assigned. Only unowned spaces can be assigned to a team. Assignment between teams is unsupported.
        :type team_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into Announcement Mode or clears the Anouncement Mode (false)
        :type is_announcement_only: bool
        :param is_read_only: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in this space, while maintaing historical data.
        :type is_read_only: bool
        """
        body = {}
        if title is not None:
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
        data = super().put(url=url, json=body)
        return Room.parse_obj(data)

    def delete(self, room_id: str):
        """
        Deletes a room, by ID. Deleted rooms cannot be recovered.
        As a security measure to prevent accidental deletion, when a non moderator deletes the room they are removed from the room instead.
        Deleting a room that is part of a team will archive the room instead.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}')
        super().delete(url=url)
        return

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
    Team Memberships represent a person's relationship to a team. Use this API to list members of any team that you're in or create memberships to invite someone to a team. Team memberships can also be updated to make someone a moderator or deleted to remove them from the team.
    Just like in the Webex app, you must be a member of the team in order to list its memberships or invite people.
    """

    def list_memberships(self, team_id: str, **params) -> Generator[ListTeamMembershipsResponse, None, None]:
        """
        Lists all team memberships for a given team, specified by the teamId query parameter.
        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListTeamMembershipsResponse, params=params)

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
        """
        body = {}
        if team_id is not None:
            body['teamId'] = team_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = super().post(url=url, json=body)
        return TeamMembership.parse_obj(data)

    def membership_details(self, membership_id: str) -> TeamMembership:
        """
        Shows details for a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
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
        """
        body = {}
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep(f'{membership_id}')
        data = super().put(url=url, json=body)
        return TeamMembership.parse_obj(data)

    def delete_membership(self, membership_id: str):
        """
        Deletes a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.
        The team membership for the last moderator of a team may not be deleted; promote another user to team moderator first.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        super().delete(url=url)
        return

class CreateTeamBody(ApiModel):
    #: A user-friendly name for the team.
    name: Optional[str]
    #: The teams description.
    description: Optional[str]


class Team(CreateTeamBody):
    #: A unique identifier for the team.
    id: Optional[str]
    #: The date and time the team was created.
    created: Optional[str]


class ListTeamsResponse(ApiModel):
    items: Optional[list[Team]]


class TeamsApi(ApiChild, base='teams'):
    """
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its name, for example.
    To manage people in a team see the Team Memberships API.
    To manage team rooms see the Rooms API.
    """

    def list(self) -> Generator[Team, None, None]:
        """
        Lists teams to which the authenticated user belongs.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Team, params=params)

    def create(self, name: str, description: str = None) -> Team:
        """
        Creates a team.
        The authenticated user is automatically added as a member of the team. See the Team Memberships API to learn how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str
        """
        body = {}
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        url = self.ep()
        data = super().post(url=url, json=body)
        return Team.parse_obj(data)

    def details(self, team_id: str, description: str = None) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param description: The teams description.
        :type description: str
        """
        params = {}
        if description is not None:
            params['description'] = description
        url = self.ep(f'{team_id}')
        data = super().get(url=url, params=params)
        return Team.parse_obj(data)

    def update(self, team_id: str, name: str, description: str = None) -> Team:
        """
        Updates details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str
        """
        body = {}
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        url = self.ep(f'{team_id}')
        data = super().put(url=url, json=body)
        return Team.parse_obj(data)

    def delete(self, team_id: str):
        """
        Deletes a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        super().delete(url=url)
        return

class Status(str, Enum):
    #: The webhook is active.
    active = 'active'
    #: The webhook is inactive.
    inactive = 'inactive'


class Event2(EventTypeEnum):
    #: A meeting is started.
    started = 'started'
    #: A participant joined.
    joined = 'joined'
    #: A participant left.
    left = 'left'


class CreateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[Resource]
    #: The event type for the webhook.
    event: Optional[Event2]
    #: The filter that defines the webhook scope. See Filtering Webhooks for more information.
    filter: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants, and meetingTranscripts resources.
    owned_by: Optional[str]


class Webhook(CreateWebhookBody):
    #: A unique identifier for the webhook.
    id: Optional[str]
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: Optional[Status]
    #: The date and time the webhook was created.
    created: Optional[str]


class ListWebhooksResponse(ApiModel):
    items: Optional[list[Webhook]]


class UpdateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants and meetingTranscripts resources.
    owned_by: Optional[str]
    #: The status of the webhook. Use "active" to reactivate a disabled webhook.
    status: Optional[Status]


class WebhooksApi(ApiChild, base='webhooks'):
    """
    For Webex for Government (FedRAMP), the following resource types are not available for Webhooks: meetings, recordings, meetingParticipants, and meetingTranscripts.
    Webhooks allow your app to be notified via HTTP when a specific event occurs in Webex. For example, your app can register a webhook to be notified when a new message is posted into a specific room.
    Events trigger in near real-time allowing your app and backend IT systems to stay in sync with new content and room activity.
    Check The Webhooks Guide and our blog regularly for announcements of additional webhook resources and event types.
    Long result sets will be split into pages.
    """

    def list(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
        """
        List all of your webhooks.

        :param owned_by: Limit the result list to org wide webhooks. Only allowed value is org.
        :type owned_by: str
        """
        if owned_by is not None:
            params['ownedBy'] = owned_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Webhook, params=params)

    def create(self, name: str, target_url: str, resource: enum, event: enum, filter: str = None, secret: str = None, owned_by: str = None) -> Webhook:
        """
        Creates a webhook.
        To learn more about how to create and use webhooks, see The Webhooks Guide.

        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
        :type resource: enum
        :param event: The event type for the webhook.
        :type event: enum
        :param filter: The filter that defines the webhook scope. See Filtering Webhooks for more information.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants, and meetingTranscripts resources.
        :type owned_by: str
        """
        body = {}
        if name is not None:
            body['name'] = name
        if target_url is not None:
            body['targetUrl'] = target_url
        if resource is not None:
            body['resource'] = resource
        if event is not None:
            body['event'] = event
        if filter is not None:
            body['filter'] = filter
        if secret is not None:
            body['secret'] = secret
        if owned_by is not None:
            body['ownedBy'] = owned_by
        url = self.ep()
        data = super().post(url=url, json=body)
        return Webhook.parse_obj(data)

    def details(self, webhook_id: str) -> Webhook:
        """
        Shows details for a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        """
        url = self.ep(f'{webhook_id}')
        data = super().get(url=url)
        return Webhook.parse_obj(data)

    def update(self, webhook_id: str, name: str, target_url: str, secret: str = None, owned_by: str = None, status: enum = None) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that was auto deactivated. 
        The fields that can be updated are name, targetURL, secret and status. All other fields, if supplied, are ignored.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants and meetingTranscripts resources.
        :type owned_by: str
        :param status: The status of the webhook. Use "active" to reactivate a disabled webhook.
        :type status: enum
        """
        body = {}
        if name is not None:
            body['name'] = name
        if target_url is not None:
            body['targetUrl'] = target_url
        if secret is not None:
            body['secret'] = secret
        if owned_by is not None:
            body['ownedBy'] = owned_by
        if status is not None:
            body['status'] = status
        url = self.ep(f'{webhook_id}')
        data = super().put(url=url, json=body)
        return Webhook.parse_obj(data)

    def delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        """
        url = self.ep(f'{webhook_id}')
        super().delete(url=url)
        return
