"""
Messages API
"""
import mimetypes
import os.path
from collections.abc import Generator
from datetime import datetime
from typing import List, Optional, Union

from requests_toolbelt import MultipartEncoder

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.common import RoomType

__all__ = ['AdaptiveCardAction', 'AdaptiveCard', 'MessageAttachment', 'AdaptiveCardBody',
           'Message', 'MessagesData', 'MessagesApi']

from wxc_sdk.webhook import WebhookEventData


class AdaptiveCardBody(ApiModel):
    #: Possible values: TextBlock
    type: Optional[str]
    #: Possible values: Adaptive Cards
    text: Optional[str]
    #: Possible values: large
    size: Optional[str]


class AdaptiveCardAction(ApiModel):
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
    body: Optional[list[AdaptiveCardBody]]
    #: The card's actions.
    actions: Optional[list[AdaptiveCardAction]]


class MessageAttachment(ApiModel):
    #: The content type of the attachment.
    content_type: Optional[str]
    #: Adaptive Card content.
    content: Optional[AdaptiveCard]


class Message(ApiModel):
    #: The unique identifier for the message.
    id: Optional[str]
    #: The unique identifier for the parent message.
    parent_id: Optional[str]
    #: The room ID of the message.
    room_id: Optional[str]
    #: The type of room.
    room_type: Optional[RoomType]
    #: The message, in plain text. If markdown is specified this parameter may be optionally used to provide
    #: alternate text for UI clients that do not support rich text. The maximum message length is 7439 bytes.
    text: Optional[str]
    #: The message, in Markdown format. If this attribute is set ensure that the request does NOT contain an html
    #: attribute.
    markdown: Optional[str]
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    html: Optional[str]
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see Message Attachments.
    files: Optional[list[str]]
    #: The person ID of the message author.
    person_id: Optional[str]
    #: The email address of the message author.
    person_email: Optional[str]
    #: The person ID of the recipient when sending a private 1:1 message.
    to_person_id: Optional[str]
    #: The email address of the recipient when sending a private 1:1 message.
    to_person_email: Optional[str]
    #: People IDs for anyone mentioned in the message.
    mentioned_people: Optional[list[str]]
    #: Group names for the groups mentioned in the message.
    mentioned_groups: Optional[list[str]]
    #: Message content attachments attached to the message. See the Cards Guide for more information.
    attachments: Optional[list[MessageAttachment]]
    #: The date and time the message was created.
    created: Optional[datetime]
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    updated: Optional[datetime]
    #: true if the audio file is a voice clip recorded by the client; false if the audio file is a standard audio
    #: file not posted using the voice clip feature.
    is_voice_clip: Optional[bool]


class MessagesData(WebhookEventData):
    """
    Data in a webhook "messages" event
    """
    resource = 'messages'
    id: str
    room_id: str
    room_type: Optional[RoomType]
    person_id: Optional[str]
    person_email: Optional[str]
    created: Optional[datetime]


class MessagesApi(ApiChild, base='messages'):
    """

    """

    def list(self, room_id: str, parent_id: str = None, mentioned_people: List[str] = None, before: datetime = None,
             before_message: str = None, **params) -> Generator[Message, None, None]:
        """
        Lists all messages in a room.  Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.
        Long result sets will be split into pages.

        :param room_id: List messages in a room, by ID.
        :type room_id: str
        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param mentioned_people: List messages with these people mentioned, by ID. Use me as a shorthand
            for the current API user. Only me or the person ID of the current user may be specified. Bots must include
            this parameter to list messages in group rooms (spaces).
        :type mentioned_people: List[str]
        :param before: List messages sent before a date and time.
        :type before: str
        :param before_message: List messages sent before a message, by ID.
        :type before_message: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if parent_id is not None:
            params['parentId'] = parent_id
        if mentioned_people is not None:
            params['mentionedPeople'] = mentioned_people
        if before is not None:
            params['before'] = dt_iso_str(before)
        if before_message is not None:
            params['beforeMessage'] = before_message
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Message, params=params)

    def list_direct(self, parent_id: str = None, person_id: str = None, person_email: str = None,
                    **params) -> Generator[Message, None, None]:
        """
        List all messages in a 1:1 (direct) room. Use the personId or personEmail query parameter to specify the
        room. Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.

        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param person_id: List messages in a 1:1 room, by person ID.
        :type person_id: str
        :param person_email: List messages in a 1:1 room, by person email.
        :type person_email: str
        """
        if parent_id is not None:
            params['parentId'] = parent_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep('direct')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Message, params=params)

    def create(self, room_id: str = None, parent_id: str = None, to_person_id: str = None, to_person_email: str = None,
               text: str = None, markdown: str = None, files: List[str] = None,
               attachments: List[Union[dict, MessageAttachment]] = None) -> Message:
        """
        Post a plain text or rich text message, and optionally, a file attachment, to a room.
        The files parameter is an array, which accepts multiple values to allow for future expansion, but currently
        only one file may be included with the message. File previews are only rendered for attachments of 1MB or less.

        :param room_id: The room ID of the message.
        :type room_id: str
        :param parent_id: The parent message to reply to.
        :type parent_id: str
        :param to_person_id: The person ID of the recipient when sending a private 1:1 message.
        :type to_person_id: str
        :param to_person_email: The email address of the recipient when sending a private 1:1 message.
        :type to_person_email: str
        :param text: The message, in plain text. If markdown is specified this parameter may be optionally used
            to provide alternate text for UI clients that do not support rich text. The maximum message length is 7439
            bytes.
        :type text: str
        :param markdown: The message, in Markdown format. The maximum message length is 7439 bytes.
        :type markdown: str
        :param files: The public URL to a binary file or a path to a local file to be posted into the room.
            Only one file is allowed
            per message. Uploaded files are automatically converted into a format that all Webex clients can render. For
            the supported media types and the behavior of uploads, see the Message Attachments Guide.
        :type files: List[str]
        :param attachments: Content attachments to attach to the message. Only one card per message
            is supported. See the Cards Guide for more information.
        :type attachments: List[Attachment]
        :rtype: Message
        """
        # TODO: handle local files for attachments
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if parent_id is not None:
            body['parentId'] = parent_id
        if to_person_id is not None:
            body['toPersonId'] = to_person_id
        if to_person_email is not None:
            body['toPersonEmail'] = to_person_email
        if text is not None:
            body['text'] = text
        if markdown is not None:
            body['markdown'] = markdown
        if attachments is not None:
            body['attachments'] = [a.dict(by_alias=True) if isinstance(a, MessageAttachment) else a
                                   for a in attachments]
        if files is not None:
            body['files'] = files

        url = self.ep()
        if files and os.path.isfile(files[0]):
            # this is a local file
            open_file = open(files[0], mode='rb')
            try:
                c_type = mimetypes.guess_type(files[0])[0] or 'text/plain'
                body['files'] = (os.path.basename(files[0]),
                                 open_file,
                                 c_type)
                multipart = MultipartEncoder(body)
                headers = {'Content-type': multipart.content_type}
                data = super().post(url=url, headers=headers, data=multipart)
            finally:
                open_file.close()
        else:
            data = super().post(url=url, json=body)
        return Message.parse_obj(data)

    def edit(self, message: Message) -> Message:
        """
        Update a message you have posted not more than 10 times.
        Specify the messageId of the message you want to edit.
        Edits of messages containing files or attachments are not currently supported.
        If a user attempts to edit a message containing files or attachments a 400 Bad Request will be returned by
        the API with a message stating that the feature is currently unsupported.
        There is also a maximum number of times a user can edit a message. The maximum currently supported is 10
        edits per message.
        If a user attempts to edit a message greater that the maximum times allowed the API will return 400 Bad
        Request with a message stating the edit limit has been reached.
        While only the roomId and text or markdown attributes are required in the request body, a common pattern for
        editing message is to first call GET /messages/{id} for the message you wish to edit and to then update the
        text or markdown attribute accordingly, passing the updated message object in the request body of the PUT
        /messages/{id} request.

        :param message: the updated message, id has to be set in the message
            attributes supported for update:

                * room_id: str: The room ID of the message.
                * text: str: The message, in plain text. If markdown is specified this parameter may be optionally used
                  to provide alternate text for UI clients that do not support rich text. The maximum message length
                  is 7439 bytes.
                * markdown: str: The message, in Markdown format. If this attribute is set ensure that the request does
                  NOT contain an html attribute.
        """
        data = message.json(include={'room_id', 'text', 'markdown'})
        if not message.id:
            raise ValueError('ID has to be set')
        url = self.ep(f'{message.id}')
        data = super().put(url=url, data=data)
        return Message.parse_obj(data)

    def details(self, message_id: str) -> Message:
        """
        Show details for a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        data = super().get(url=url)
        return Message.parse_obj(data)

    def delete(self, message_id: str):
        """
        Delete a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        super().delete(url=url)
        return
