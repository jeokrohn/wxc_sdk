from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Actions', 'AdaptiveCard', 'Addresses', 'Attachment', 'AttachmentActionsApi', 'Body',
           'CreateAttachmentActionBody', 'CreateAttachmentActionResponse', 'CreateMembershipBody',
           'CreateMessageResponse', 'CreatePersonBody', 'CreateRoomBody', 'CreateRoomTabBody', 'CreateTeamBody',
           'CreateTeamMembershipBody', 'CreateWebhookBody', 'Data', 'DirectMessage', 'EditMessageBody', 'Event',
           'Event1', 'EventResourceEnum', 'EventTypeEnum', 'EventsApi', 'GetRoomMeetingDetailsResponse', 'Inputs',
           'ListDirectMessagesResponse', 'ListEventsResponse', 'ListMembershipsResponse', 'ListMessage',
           'ListMessagesResponse', 'ListPeopleResponse', 'ListRoomTabsResponse', 'ListRoomsResponse',
           'ListTeamMembershipsResponse', 'ListTeamsResponse', 'ListWebhooksResponse', 'Membership', 'MembershipsApi',
           'MessagesApi', 'PeopleApi', 'Person', 'PhoneNumbers', 'Resource', 'Room', 'RoomTab', 'RoomTabsApi',
           'RoomType', 'RoomsApi', 'SipAddressesType', 'Status', 'Status5', 'Team', 'TeamMembership',
           'TeamMembershipsApi', 'TeamsApi', 'Type', 'Webhook', 'WebhooksApi']


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


class AttachmentActionsApi(ApiChild, base='attachment/actions'):
    """
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a
    card.
    """

    def create_action(self, type_: str, message_id: str, inputs: Inputs) -> CreateAttachmentActionResponse:
        """
        Create a new attachment action.

        :param type_: The type of action to perform.
        :type type_: str
        :param message_id: The ID of the message which contains the attachment.
        :type message_id: str
        :param inputs: The attachment action's inputs.
        :type inputs: Inputs

        documentation: https://developer.webex.com/docs/api/v1/attachment-actions/create-an-attachment-action
        """
        body = CreateAttachmentActionBody()
        if type_ is not None:
            body.type_ = type_
        if message_id is not None:
            body.message_id = message_id
        if inputs is not None:
            body.inputs = inputs
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return CreateAttachmentActionResponse.parse_obj(data)

    def action_details(self, id: str) -> CreateAttachmentActionResponse:
        """
        Shows details for a attachment action, by ID.
        Specify the attachment action ID in the id URI parameter.

        :param id: A unique identifier for the attachment action.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/attachment-actions/get-attachment-action-details
        """
        url = self.ep(f'{id}')
        data = super().get(url=url)
        return CreateAttachmentActionResponse.parse_obj(data)

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
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If true a transcript should be
    #: available a couple minutes after the meeting ended at the meetingTranscripts resource
    transcription_enabled: Optional[str]
    #: indicates if recording was enabled for all or parts of the meeting. If true a recording should be available
    #: shortly after the meeting ended at the recordings resource
    recording_enabled: Optional[str]
    #: indicates i chat messages were exchanged during the meeting in the meetings client (not the unified client). If
    #: true these messages can be accessed by a compliance officer at the postMeetingsChat resource. Meetings chat
    #: collection must be custom enabled.
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
    #: The event's data representation. This object will contain the event's resource, such as memberships, messages,
    #: meetings, tabs, rooms or attachmentActions at the time the event took place.
    data: Optional[Data]


class ListEventsResponse(ApiModel):
    items: Optional[list[Event]]


class EventsApi(ApiChild, base='events'):
    """
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    The Events API can only be used by a Compliance Officer with an API access token that contains the
    spark-compliance:events_read scope. See the Compliance Guide for more information.
    """

    def list_events(self, resource: str = None, type_: str = None, actor_id: str = None, from_: str = None, to_: str = None, **params) -> Generator[Event, None, None]:
        """
        List events in your organization. Several query parameters are available to filter the events returned in the
        response.
        Long result sets will be split into pages.

        :param resource: List events with a specific resource type. Possible values: messages, memberships, meetings,
            meetingMessages, meetingTranscripts, tabs, rooms, attachmentActions, files, file_transcodings
        :type resource: str
        :param type_: List events with a specific event type. Possible values: created, updated, deleted, ended
        :type type_: str
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the
            future, lists events up to the present.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/events/list-events
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

        documentation: https://developer.webex.com/docs/api/v1/events/get-event-details
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
    Memberships represent a person's relationship to a room. Use this API to list members of any room that you're in or
    create memberships to invite someone to a room. Compliance Officers can now also list memberships for personEmails
    where the CO is not part of the room.
    Memberships can also be updated to make someone a moderator, or deleted, to remove someone from the room.
    Just like in the Webex client, you must be a member of the room in order to list its memberships or invite people.
    """

    def list(self, room_id: str = None, person_id: str = None, person_email: str = None, **params) -> Generator[Membership, None, None]:
        """
        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.
        Use query parameters to filter the response.
        Use roomId to list memberships for a room, by ID.
        NOTE: For moderated team spaces, the list of memberships will include only the space moderators if the user is
        a team member but not a direct participant of the space.
        Use either personId or personEmail to filter the results. The roomId parameter is required when using these
        parameters.
        Long result sets will be split into pages.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The roomId parameter is required when using
            this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The roomId parameter is
            required when using this parameter.
        :type person_email: str

        documentation: https://developer.webex.com/docs/api/v1/memberships/list-memberships
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

        documentation: https://developer.webex.com/docs/api/v1/memberships/create-a-membership
        """
        body = CreateMembershipBody()
        if room_id is not None:
            body.room_id = room_id
        if person_id is not None:
            body.person_id = person_id
        if person_email is not None:
            body.person_email = person_email
        if is_moderator is not None:
            body.is_moderator = is_moderator
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Membership.parse_obj(data)

    def details(self, membership_id: str) -> Membership:
        """
        Get details for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str

        documentation: https://developer.webex.com/docs/api/v1/memberships/get-membership-details
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
        :param is_room_hidden: When set to true, hides direct spaces in the teams client. Any new message will make the
            room visible again.
        :type is_room_hidden: bool

        documentation: https://developer.webex.com/docs/api/v1/memberships/update-a-membership
        """
        body = UpdateMembershipBody()
        if is_moderator is not None:
            body.is_moderator = is_moderator
        if is_room_hidden is not None:
            body.is_room_hidden = is_room_hidden
        url = self.ep(f'{membership_id}')
        data = super().put(url=url, data=body.json())
        return Membership.parse_obj(data)

    def delete(self, membership_id: str):
        """
        Deletes a membership by ID.
        Specify the membership ID in the membershipId URI parameter.
        The membership for the last moderator of a Team's General space may not be deleted; promote another user to
        team moderator first.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str

        documentation: https://developer.webex.com/docs/api/v1/memberships/delete-a-membership
        """
        url = self.ep(f'{membership_id}')
        super().delete(url=url)
        return

class Body(ApiModel):
    #: Possible values: TextBlock
    type: Optional[str]
    #: Possible values: Adaptive Cards
    text: Optional[str]
    #: Possible values: large
    size: Optional[str]


class Actions(ApiModel):
    #: Possible values: Action.OpenUrl
    type: Optional[str]
    #: Possible values: http://adaptivecards.io
    url: Optional[str]
    #: Possible values: Learn More
    title: Optional[str]


class AdaptiveCard(ApiModel):
    #: Must be AdaptiveCard.
    type: Optional[str]
    #: Adaptive Card schema version.
    version: Optional[str]
    #: The card's elements.
    body: Optional[list[Body]]
    #: The card's actions.
    actions: Optional[list[Actions]]


class Attachment(ApiModel):
    #: The content type of the attachment.
    content_type: Optional[str]
    #: Adaptive Card content.
    content: Optional[AdaptiveCard]


class EditMessageBody(ApiModel):
    #: The room ID of the message.
    room_id: Optional[str]
    #: The message, in plain text. If markdown is specified this parameter may be optionally used to provide alternate
    #: text for UI clients that do not support rich text. The maximum message length is 7439 bytes.
    text: Optional[str]
    #: The message, in Markdown format. If this attribute is set ensure that the request does NOT contain an html
    #: attribute.
    markdown: Optional[str]


class ListMessage(EditMessageBody):
    #: The unique identifier for the message.
    id: Optional[str]
    #: The unique identifier for the parent message.
    parent_id: Optional[str]
    #: The type of room.
    room_type: Optional[RoomType]
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    html: Optional[str]
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see Message Attachments.
    files: Optional[list[str]]
    #: The person ID of the message author.
    person_id: Optional[str]
    #: The email address of the message author.
    person_email: Optional[str]
    #: People IDs for anyone mentioned in the message.
    mentioned_people: Optional[list[str]]
    #: Group names for the groups mentioned in the message.
    mentioned_groups: Optional[list[str]]
    #: Message content attachments attached to the message. See the Cards Guide for more information.
    attachments: Optional[list[Attachment]]
    #: The date and time the message was created.
    created: Optional[str]
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    updated: Optional[str]
    #: true if the audio file is a voice clip recorded by the client; false if the audio file is a standard audio file
    #: not posted using the voice clip feature.
    is_voice_clip: Optional[bool]


class DirectMessage(EditMessageBody):
    #: The unique identifier for the message.
    id: Optional[str]
    #: The unique identifier for the parent message.
    parent_id: Optional[str]
    #: The type of room. Will always be direct.
    room_type: Optional[str]
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    html: Optional[str]
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see Message Attachments.
    files: Optional[list[str]]
    #: The person ID of the message author.
    person_id: Optional[str]
    #: The email address of the message author.
    person_email: Optional[str]
    #: Message content attachments attached to the message. See the Cards Guide for more information.
    attachments: Optional[list[Attachment]]
    #: The date and time the message was created.
    created: Optional[str]
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    updated: Optional[str]
    #: True if the audio file is a voice clip recorded by the client; false if the audio file is a standard audio file
    #: not posted using the voice clip feature.
    is_voice_clip: Optional[bool]


class ListMessagesResponse(ApiModel):
    items: Optional[list[ListMessage]]


class ListDirectMessagesResponse(ApiModel):
    items: Optional[list[DirectMessage]]


class CreateMessageBody(EditMessageBody):
    #: The parent message to reply to.
    parent_id: Optional[str]
    #: The person ID of the recipient when sending a private 1:1 message.
    to_person_id: Optional[str]
    #: The email address of the recipient when sending a private 1:1 message.
    to_person_email: Optional[str]
    #: The public URL to a binary file to be posted into the room. Only one file is allowed per message. Uploaded files
    #: are automatically converted into a format that all Webex clients can render. For the supported media types and
    #: the behavior of uploads, see the Message Attachments Guide.
    #: Possible values: http://www.example.com/images/media.png
    files: Optional[list[str]]
    #: Content attachments to attach to the message. Only one card per message is supported. See the Cards Guide for
    #: more information.
    attachments: Optional[list[Attachment]]


class CreateMessageResponse(ListMessage):
    #: The person ID of the recipient when sending a private 1:1 message.
    to_person_id: Optional[str]
    #: The email address of the recipient when sending a private 1:1 message.
    to_person_email: Optional[str]


class MessagesApi(ApiChild, base='messages'):
    """
    Messages are how you communicate in a room. In Webex, each message is displayed on its own line along with a
    timestamp and sender information. Use this API to list, create, update, and delete messages.
    Message can contain plain text, rich text, and a file attachment.
    Just like in the Webex app, you must be a member of the room in order to target it with this API.
    """

    def list(self, room_id: str, parent_id: str = None, mentioned_people: List[str] = None, before: str = None, before_message: str = None, **params) -> Generator[ListMessage, None, None]:
        """
        Lists all messages in a room. Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.
        Long result sets will be split into pages.

        :param room_id: List messages in a room, by ID.
        :type room_id: str
        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param mentioned_people: List messages with these people mentioned, by ID. Use me as a shorthand for the
            current API user. Only me or the person ID of the current user may be specified. Bots must include this
            parameter to list messages in group rooms (spaces).
        :type mentioned_people: List[str]
        :param before: List messages sent before a date and time.
        :type before: str
        :param before_message: List messages sent before a message, by ID.
        :type before_message: str

        documentation: https://developer.webex.com/docs/api/v1/messages/list-messages
        """
        params['roomId'] = room_id
        if parent_id is not None:
            params['parentId'] = parent_id
        if mentioned_people is not None:
            params['mentionedPeople'] = mentioned_people
        if before is not None:
            params['before'] = before
        if before_message is not None:
            params['beforeMessage'] = before_message
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListMessage, params=params)

    def list_direct(self, parent_id: str = None, person_id: str = None, person_email: str = None) -> list[DirectMessage]:
        """
        List all messages in a 1:1 (direct) room. Use the personId or personEmail query parameter to specify the room.
        Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.

        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param person_id: List messages in a 1:1 room, by person ID.
        :type person_id: str
        :param person_email: List messages in a 1:1 room, by person email.
        :type person_email: str

        documentation: https://developer.webex.com/docs/api/v1/messages/list-direct-messages
        """
        params = {}
        if parent_id is not None:
            params['parentId'] = parent_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep('direct')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[DirectMessage], data["items"])

    def create(self, room_id: str, text: str = None, markdown: str = None, parent_id: str = None, to_person_id: str = None, to_person_email: str = None, files: List[str] = None, attachments: Attachment = None) -> CreateMessageResponse:
        """
        Post a plain text or rich text message, and optionally, a file attachment attachment, to a room.
        The files parameter is an array, which accepts multiple values to allow for future expansion, but currently
        only one file may be included with the message. File previews are only rendered for attachments of 1MB or less.

        :param room_id: The room ID of the message.
        :type room_id: str
        :param text: The message, in plain text. If markdown is specified this parameter may be optionally used to
            provide alternate text for UI clients that do not support rich text. The maximum message length is 7439
            bytes.
        :type text: str
        :param markdown: The message, in Markdown format. If this attribute is set ensure that the request does NOT
            contain an html attribute.
        :type markdown: str
        :param parent_id: The parent message to reply to.
        :type parent_id: str
        :param to_person_id: The person ID of the recipient when sending a private 1:1 message.
        :type to_person_id: str
        :param to_person_email: The email address of the recipient when sending a private 1:1 message.
        :type to_person_email: str
        :param files: The public URL to a binary file to be posted into the room. Only one file is allowed per message.
            Uploaded files are automatically converted into a format that all Webex clients can render. For the
            supported media types and the behavior of uploads, see the Message Attachments Guide. Possible values:
            http://www.example.com/images/media.png
        :type files: List[str]
        :param attachments: Content attachments to attach to the message. Only one card per message is supported. See
            the Cards Guide for more information.
        :type attachments: Attachment

        documentation: https://developer.webex.com/docs/api/v1/messages/create-a-message
        """
        body = CreateMessageBody()
        if room_id is not None:
            body.room_id = room_id
        if text is not None:
            body.text = text
        if markdown is not None:
            body.markdown = markdown
        if parent_id is not None:
            body.parent_id = parent_id
        if to_person_id is not None:
            body.to_person_id = to_person_id
        if to_person_email is not None:
            body.to_person_email = to_person_email
        if files is not None:
            body.files = files
        if attachments is not None:
            body.attachments = attachments
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return CreateMessageResponse.parse_obj(data)

    def edit(self, message_id: str, room_id: str, text: str = None, markdown: str = None) -> ListMessage:
        """
        Update a message you have posted not more than 10 times.
        Specify the messageId of the message you want to edit.
        Edits of messages containing files or attachments are not currently supported.
        If a user attempts to edit a message containing files or attachments a 400 Bad Request will be returned by the
        API with a message stating that the feature is currently unsupported.
        There is also a maximum number of times a user can edit a message. The maximum currently supported is 10 edits
        per message.
        If a user attempts to edit a message greater that the maximum times allowed the API will return 400 Bad Request
        with a message stating the edit limit has been reached.
        While only the roomId and text or markdown attributes are required in the request body, a common pattern for
        editing message is to first call GET /messages/{id} for the message you wish to edit and to then update the
        text or markdown attribute accordingly, passing the updated message object in the request body of the PUT
        /messages/{id} request.
        When this pattern is used on a message that included markdown, the html attribute must be deleted prior to
        making the PUT request.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        :param room_id: The room ID of the message.
        :type room_id: str
        :param text: The message, in plain text. If markdown is specified this parameter may be optionally used to
            provide alternate text for UI clients that do not support rich text. The maximum message length is 7439
            bytes.
        :type text: str
        :param markdown: The message, in Markdown format. If this attribute is set ensure that the request does NOT
            contain an html attribute.
        :type markdown: str

        documentation: https://developer.webex.com/docs/api/v1/messages/edit-a-message
        """
        body = EditMessageBody()
        if room_id is not None:
            body.room_id = room_id
        if text is not None:
            body.text = text
        if markdown is not None:
            body.markdown = markdown
        url = self.ep(f'{message_id}')
        data = super().put(url=url, data=body.json())
        return ListMessage.parse_obj(data)

    def details(self, message_id: str) -> ListMessage:
        """
        Show details for a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/messages/get-message-details
        """
        url = self.ep(f'{message_id}')
        data = super().get(url=url)
        return ListMessage.parse_obj(data)

    def delete(self, message_id: str):
        """
        Delete a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/messages/delete-a-message
        """
        url = self.ep(f'{message_id}')
        super().delete(url=url)
        return

class PhoneNumbers(ApiModel):
    #: The type of phone number.
    #: Possible values: work, mobile, fax
    type: Optional[str]
    #: The phone number.
    #: Possible values: +1 408 526 7209
    value: Optional[str]


class SipAddressesType(PhoneNumbers):
    primary: Optional[bool]


class Status5(str, Enum):
    #: The webhook is active.
    active = 'active'
    #: The webhook is inactive.
    inactive = 'inactive'


class Status(Status5):
    #: The user is in a call
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: The user is in a meeting
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined
    pending = 'pending'
    #: The user is sharing content
    presenting = 'presenting'
    #: The user’s status could not be determined
    unknown = 'unknown'


class Type(str, Enum):
    #: Account belongs to a person
    person = 'person'
    #: Account is a bot user
    bot = 'bot'
    #: Account is a guest user
    appuser = 'appuser'


class Addresses(ApiModel):
    #: The type of address
    #: Possible values: work
    type: Optional[str]
    #: The user's country
    #: Possible values: US
    country: Optional[str]
    #: the user's locality, often city
    #: Possible values: Milpitas
    locality: Optional[str]
    #: the user's region, often state
    #: Possible values: California
    region: Optional[str]
    #: the user's street
    #: Possible values: 1099 Bird Ave.
    street_address: Optional[str]
    #: the user's postal or zip code
    #: Possible values: 99212
    postal_code: Optional[str]


class CreatePersonBody(ApiModel):
    #: The email addresses of the person. Only one email address is allowed per person.
    #: Possible values: john.andersen@example.com
    emails: Optional[list[str]]
    #: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling license.
    phone_numbers: Optional[list[PhoneNumbers]]
    #: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license.
    extension: Optional[str]
    #: The ID of the location for this person.
    location_id: Optional[str]
    #: The full name of the person.
    display_name: Optional[str]
    #: The first name of the person.
    first_name: Optional[str]
    #: The last name of the person.
    last_name: Optional[str]
    #: The URL to the person's avatar in PNG format.
    avatar: Optional[str]
    #: The ID of the organization to which this person belongs.
    org_id: Optional[str]
    #: An array of role strings representing the roles to which this admin user belongs.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    licenses: Optional[list[str]]
    #: The business department the user belongs to.
    department: Optional[str]
    #: A manager identifier.
    manager: Optional[str]
    #: Person Id of the manager
    manager_id: Optional[str]
    #: the person's title
    title: Optional[str]
    #: Person's address
    addresses: Optional[list[Addresses]]
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg:
    #: mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]]


class Person(CreatePersonBody):
    #: A unique identifier for the person.
    id: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    nick_name: Optional[str]
    #: The date and time the person was created.
    created: Optional[str]
    #: The date and time the person was last changed.
    last_modified: Optional[str]
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user has
    #: disabled status sharing.
    last_activity: Optional[str]
    #: The users sip addresses. Read-only.
    sip_addresses: Optional[list[SipAddressesType]]
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has disabled status
    #: sharing.
    status: Optional[Status]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    type: Optional[Type]


class ListPeopleResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]]
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]]


class UpdatePersonBody(CreatePersonBody):
    #: The nickname of the person if configured. Set to the firstName automatically in update request.
    nick_name: Optional[str]
    #: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is
    #: an admin user for the person's organization.
    login_enabled: Optional[bool]


class PeopleApi(ApiChild, base='people'):
    """
    People are registered users of Webex. Searching and viewing People requires an auth token with a scope of
    spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token with
    spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token with the
    spark-admin:people_write and spark-admin:people_read scope.
    A person's call settings are for Webex Calling and necessitate Webex Calling licenses.
    To learn more about managing people in a room see the Memberships API. For information about how to allocate Hybrid
    Services licenses to people, see the Managing Hybrid Services guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, roles: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=
        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.
        Lookup by roles is only supported for Admin users for the people within the same org.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required. With the exception of partner admins and a managed org relationship, people lookup by email is
            only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided
            then presence information (such as the lastActivity or status properties) will not be included in the
            response.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/list-people
        """
        if email is not None:
            params['email'] = email
        if display_name is not None:
            params['displayName'] = display_name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        if roles is not None:
            params['roles'] = roles
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Person, params=params)

    def create(self, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.
        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.
        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        When doing attendee management, append #attendee to the siteUrl parameter (e.g. mysite.webex.com#attendee) to
        make the new user an attendee for a site.

        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]

        documentation: https://developer.webex.com/docs/api/v1/people/create-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        body = CreatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-person-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, emails: List[str], calling_data: bool = None, show_all_types: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None, nick_name: str = None, login_enabled: bool = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is
        already an existing calling user.
        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to
        the respective siteUrl and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the siteurl parameter.
        To remove the attendee privilege for a user on a meeting site, remove the sitename#attendee from the siteUrls
        array. The showAllTypes parameter must be set to true.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        :param nick_name: The nickname of the person if configured. Set to the firstName automatically in update
            request.
        :type nick_name: str
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the
            authenticated user is an admin user for the person's organization.
        :type login_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/people/update-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        body = UpdatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        if nick_name is not None:
            body.nick_name = nick_name
        if login_enabled is not None:
            body.login_enabled = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def delete(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/delete-a-person
        """
        url = self.ep(f'{person_id}')
        super().delete(url=url)
        return

    def my_own_details(self, calling_data: bool = None) -> Person:
        """
        Get profile details for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-my-own-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

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
    A Room Tab represents a URL shortcut that is added as a persistent tab to a Webex room (space) tab row. Use this
    API to list tabs of any Webex room that you belong to. Room Tabs can also be updated to point to a different
    content URL, or deleted to remove the tab from the room.
    Just like in the Webex app, you must be a member of the room in order to list its Room Tabs.
    """

    def list_tabs(self, room_id: str) -> list[RoomTab]:
        """
        Lists all Room Tabs of a room specified by the roomId query parameter.

        :param room_id: ID of the room for which to list room tabs.
        :type room_id: str

        documentation: https://developer.webex.com/docs/api/v1/room-tabs/list-room-tabs
        """
        params = {}
        params['roomId'] = room_id
        url = self.ep()
        data = super().get(url=url, params=params)
        return parse_obj_as(list[RoomTab], data["items"])

    def create_tab(self, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Add a tab with a specified URL to a room.

        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the Room Tab. Must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/room-tabs/create-a-room-tab
        """
        body = CreateRoomTabBody()
        if room_id is not None:
            body.room_id = room_id
        if content_url is not None:
            body.content_url = content_url
        if display_name is not None:
            body.display_name = display_name
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return RoomTab.parse_obj(data)

    def tab_details(self, id: str) -> RoomTab:
        """
        Get details for a Room Tab with the specified room tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/room-tabs/get-room-tab-details
        """
        url = self.ep(f'{id}')
        data = super().get(url=url)
        return RoomTab.parse_obj(data)

    def update_tab(self, id: str, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Updates the content URL of the specified Room Tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str
        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the Room Tab. Must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/room-tabs/update-a-room-tab
        """
        body = CreateRoomTabBody()
        if room_id is not None:
            body.room_id = room_id
        if content_url is not None:
            body.content_url = content_url
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{id}')
        data = super().put(url=url, data=body.json())
        return RoomTab.parse_obj(data)

    def delete_tab(self, id: str):
        """
        Deletes a Room Tab with the specified ID.

        :param id: The unique identifier for the Room Tab to delete.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/room-tabs/delete-a-room-tab
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
    type: Optional[RoomType]
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
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to
    manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its
    name, for example.
    To manage people in a team see the Team Memberships API.
    To manage team rooms see the Rooms API.
    """

    def list(self, **params) -> Generator[Team, None, None]:
        """
        Lists teams to which the authenticated user belongs.

        documentation: https://developer.webex.com/docs/api/v1/teams/list-teams
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Team, params=params)

    def create(self, name: str, description: str = None) -> Team:
        """
        Creates a team.
        The authenticated user is automatically added as a member of the team. See the Team Memberships API to learn
        how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        :param description: The teams description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/teams/create-a-team
        """
        body = CreateTeamBody()
        if name is not None:
            body.name = name
        if description is not None:
            body.description = description
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Team.parse_obj(data)

    def details(self, team_id: str, description: str = None) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param description: The teams description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/teams/get-team-details
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

        documentation: https://developer.webex.com/docs/api/v1/teams/update-a-team
        """
        body = CreateTeamBody()
        if name is not None:
            body.name = name
        if description is not None:
            body.description = description
        url = self.ep(f'{team_id}')
        data = super().put(url=url, data=body.json())
        return Team.parse_obj(data)

    def delete(self, team_id: str):
        """
        Deletes a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str

        documentation: https://developer.webex.com/docs/api/v1/teams/delete-a-team
        """
        url = self.ep(f'{team_id}')
        super().delete(url=url)
        return

class Resource(str, Enum):
    #: The Attachment Actions resource.
    attachment_actions = 'attachmentActions'
    #: The Memberships resource.
    memberships = 'memberships'
    #: The Messages resource.
    messages = 'messages'
    #: The Rooms resource.
    rooms = 'rooms'
    #: The Meetings resource.
    meetings = 'meetings'
    #: The Recordings resource.
    recordings = 'recordings'
    #: The Meeting Participants resource.
    meeting_participants = 'meetingParticipants'
    #: The Meeting Transcripts resource.
    meeting_transcripts = 'meetingTranscripts'


class Event1(EventTypeEnum):
    #: A meeting was started.
    started = 'started'
    #: A participant joined.
    joined = 'joined'
    #: A participant left.
    left = 'left'
    #: A room was migrated to a different geography. The roomId has changed.
    migrated = 'migrated'


class CreateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[Resource]
    #: The event type for the webhook.
    event: Optional[Event1]
    #: The filter that defines the webhook scope. See Filtering Webhooks for more information.
    filter: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants, and
    #: meetingTranscripts resources.
    owned_by: Optional[str]


class Webhook(CreateWebhookBody):
    #: A unique identifier for the webhook.
    id: Optional[str]
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: Optional[Status5]
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
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants and
    #: meetingTranscripts resources.
    owned_by: Optional[str]
    #: The status of the webhook. Use "active" to reactivate a disabled webhook.
    status: Optional[Status5]


class WebhooksApi(ApiChild, base='webhooks'):
    """
    For Webex for Government (FedRAMP), the following resource types are not available for Webhooks: meetings,
    recordings, meetingParticipants, and meetingTranscripts.
    Webhooks allow your app to be notified via HTTP when a specific event occurs in Webex. For example, your app can
    register a webhook to be notified when a new message is posted into a specific room.
    Events trigger in near real-time allowing your app and backend IT systems to stay in sync with new content and room
    activity.
    Check The Webhooks Guide and our blog regularly for announcements of additional webhook resources and event types.
    Long result sets will be split into pages.
    """

    def list(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
        """
        List all of your webhooks.

        :param owned_by: Limit the result list to org wide webhooks. Only allowed value is org.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/list-webhooks
        """
        if owned_by is not None:
            params['ownedBy'] = owned_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Webhook, params=params)

    def create(self, name: str, target_url: str, resource: Resource, event: Event1, filter: str = None, secret: str = None, owned_by: str = None) -> Webhook:
        """
        Creates a webhook.
        To learn more about how to create and use webhooks, see The Webhooks Guide.

        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :type resource: Resource
        :param event: The event type for the webhook.
        :type event: Event1
        :param filter: The filter that defines the webhook scope. See Filtering Webhooks for more information.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants, and meetingTranscripts resources.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook
        """
        body = CreateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if resource is not None:
            body.resource = resource
        if event is not None:
            body.event = event
        if filter is not None:
            body.filter = filter
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def details(self, webhook_id: str) -> Webhook:
        """
        Shows details for a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/get-webhook-details
        """
        url = self.ep(f'{webhook_id}')
        data = super().get(url=url)
        return Webhook.parse_obj(data)

    def update(self, webhook_id: str, name: str, target_url: str, secret: str = None, owned_by: str = None, status: Status5 = None) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that was
        auto deactivated.
        The fields that can be updated are name, targetURL, secret and status. All other fields, if supplied, are
        ignored.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants and meetingTranscripts resources.
        :type owned_by: str
        :param status: The status of the webhook. Use "active" to reactivate a disabled webhook.
        :type status: Status5

        documentation: https://developer.webex.com/docs/api/v1/webhooks/update-a-webhook
        """
        body = UpdateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        if status is not None:
            body.status = status
        url = self.ep(f'{webhook_id}')
        data = super().put(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/delete-a-webhook
        """
        url = self.ep(f'{webhook_id}')
        super().delete(url=url)
        return
