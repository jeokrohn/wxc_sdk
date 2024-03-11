from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Attachment', 'DirectMessage', 'File', 'FileType', 'Message', 'MessageRoomType', 'MessagesWithECMApi']


class MessageRoomType(str, Enum):
    #: 1:1 room
    direct = 'direct'
    #: group room
    group = 'group'


class FileType(str, Enum):
    #: Attachment stored externally.
    external = 'external'
    #: Attachment stored within the Webex platform.
    native = 'native'


class File(ApiModel):
    #: The `fileId` of the attachment.
    #: example: BFT1BMRS8yNDlmNzRkOS1kYjhhLTQzY2
    file_id: Optional[str] = None
    #: The type of attachment.
    #: example: external
    type: Optional[FileType] = None
    #: The URL for the content.
    #: example: https://testecmwebexteams-my.sharepoint.com/:w:/g/personal/admin_testecmwebexteams_onmicrosoft_com/ESCiJiALU0pBlVm6TVhZ2k0B69XNVB1kWoaa7RIV9GERTg
    content_url: Optional[str] = None


class Attachment(ApiModel):
    #: Enterprise Content Management file.
    content: Optional[File] = None


class Message(ApiModel):
    #: The unique identifier for the message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: The room ID of the message.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The type of room.
    #: example: group
    room_type: Optional[MessageRoomType] = None
    #: The person ID of the recipient when sending a private 1:1 message.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mMDZkNzFhNS0wODMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX
    to_person_id: Optional[str] = None
    #: The email address of the recipient when sending a private 1:1 message.
    #: example: julie@example.com
    to_person_email: Optional[str] = None
    #: The message, in plain text. If `markdown` is specified this parameter may be *optionally* used to provide
    #: alternate text for UI clients that do not support rich text.
    #: example: PROJECT UPDATE - A new project plan has been published on http://example.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: The message, in Markdown format.
    #: example: **PROJECT UPDATE** A new project plan has been published [here](http://example.com/s/lf5vj). The PM for this project is <@personEmail:mike@example.com> and the Engineering Manager is <@personEmail:jane@example.com>.
    markdown: Optional[str] = None
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see `Message Attachments
    #: <https://developer.webex.com/docs/api/basics#message-attachments>`_.
    #: example: ['http://www.example.com/images/media.png']
    files: Optional[list[str]] = None
    #: Content attachments attached to the message.
    attachments: Optional[list[Attachment]] = None
    #: The person ID of the message author.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of the message author.
    #: example: matt@example.com
    person_email: Optional[str] = None
    #: People IDs for anyone mentioned in the message.
    #: example: ['Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yNDlmNzRkOS1kYjhhLTQzY2EtODk2Yi04NzllZDI0MGFjNTM', 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS83YWYyZjcyYy0xZDk1LTQxZjAtYTcxNi00MjlmZmNmYmM0ZDg']
    mentioned_people: Optional[list[str]] = None
    #: Group names for the groups mentioned in the message.
    #: example: ['all']
    mentioned_groups: Optional[list[str]] = None
    #: The date and time the message was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class DirectMessage(ApiModel):
    #: The unique identifier for the message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: The room ID of the message.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vODQxZjY5MjAtNDdlZC00NmE0LWI2YmItZTVjM2M1YTc3Yzgy
    room_id: Optional[str] = None
    #: The type of room. Will always be `direct`.
    #: example: direct
    room_type: Optional[str] = None
    #: The message, in plain text. If `markdown` is specified this parameter may be *optionally* used to provide
    #: alternate text for UI clients that do not support rich text.
    #: example: Hey there, what do you think of this project update presentation (http://sharepoint.example.com/presentation.pptx)?
    text: Optional[str] = None
    #: The message, in Markdown format.
    #: example: Hey there, what do you think of [this project update presentation](http://sharepoint.example.com/presentation.pptx)?
    markdown: Optional[str] = None
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see `Message Attachments
    #: <https://developer.webex.com/docs/api/basics#message-attachments>`_.
    #: example: ['http://www.example.com/images/media.png']
    files: Optional[list[str]] = None
    #: The person ID of the message author.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of the message author.
    #: example: matt@example.com
    person_email: Optional[str] = None
    #: The date and time the message was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class MessagesWithECMApi(ApiChild, base='messages'):
    """
    Messages with ECM
    
    The Enterprise Content Management functionality and API endpoint changes
    described here are currently pre-release features which are not available to
    all Webex users. If you have any questions, or if you need help, please
    contact the Webex Developer Support team at devsupport@webex.com.
    
    
    
    Messages are how we communicate in a room. In Webex, each message is displayed on its own line along with a
    timestamp and sender information. Use this API to list, create, and delete messages.
    
    Message can contain plain text, `rich text
    <https://developer.webex.com/docs/api/basics#formatting-messages>`_, and a `file attachment
    
    Just like in the Webex app, you must be a member of the room in order to target it with this API.
    """

    def list_messages(self, room_id: str, mentioned_people: list[str] = None, before: Union[str, datetime] = None,
                      before_message: str = None, **params) -> Generator[Message, None, None]:
        """
        List Messages

        Lists all messages in a room.

        Each message includes content attachments if present.

        The list sorts the messages in descending order by creation date.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param room_id: List messages in a room, by ID.
        :type room_id: str
        :param mentioned_people: List messages with these people mentioned, by ID. Use `me` as a shorthand for the
            current API user.
        :type mentioned_people: list[str]
        :param before: List messages sent before a date and time.
        :type before: Union[str, datetime]
        :param before_message: List messages sent before a message, by ID.
        :type before_message: str
        :return: Generator yielding :class:`Message` instances
        """
        params['roomId'] = room_id
        if mentioned_people is not None:
            params['mentionedPeople'] = ','.join(mentioned_people)
        if before is not None:
            if isinstance(before, str):
                before = isoparse(before)
            before = dt_iso_str(before)
            params['before'] = before
        if before_message is not None:
            params['beforeMessage'] = before_message
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Message, item_key='items', params=params)

    def list_direct_messages(self, person_id: str = None, person_email: str = None) -> list[DirectMessage]:
        """
        List Direct Messages

        Lists all messages in a 1:1 (direct) room.

        Use the `personId` or `personEmail` query parameter to specify the room. Each message includes content
        attachments if present.

        The list sorts the messages in descending order by creation date.

        :param person_id: List messages in a 1:1 room, by person ID.
        :type person_id: str
        :param person_email: List messages in a 1:1 room, by person email.
        :type person_email: str
        :rtype: list[DirectMessage]
        """
        params = {}
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep('direct')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DirectMessage]).validate_python(data['items'])
        return r

    def create_a_message(self, room_id: str = None, to_person_id: str = None, to_person_email: str = None,
                         text: str = None, markdown: str = None, files: list[str] = None,
                         attachments: list[Attachment] = None) -> Message:
        """
        Create a Message

        Create a plain text or `rich text
        <https://developer.webex.com/docs/api/basics#formatting-messages>`_ message, and optionally, a `file attachment

        The `files` parameter is an array, which accepts multiple values to allow for future expansion, but currently
        only one file may be included with the message.

        :param room_id: The room ID of the message.
        :type room_id: str
        :param to_person_id: The person ID of the recipient when sending a private 1:1 message.
        :type to_person_id: str
        :param to_person_email: The email address of the recipient when sending a private 1:1 message.
        :type to_person_email: str
        :param text: The message, in plain text. If `markdown` is specified this parameter may be *optionally* used to
            provide alternate text for UI clients that do not support rich text. The maximum message length is 7439
            bytes.
        :type text: str
        :param markdown: The message, in Markdown format. The maximum message length is 7439 bytes.
        :type markdown: str
        :param files: The public URL to a binary file to be posted into the room. Only one file is allowed per message.
            Uploaded files are automatically converted into a format that all Webex clients can render. For the
            supported media types and the behavior of uploads, see the `Message Attachments Guide
            <https://developer.webex.com/docs/api/basics#message-attachments>`_.
        :type files: list[str]
        :param attachments: Content attachments to attach to the message.
        :type attachments: list[Attachment]
        :rtype: :class:`Message`
        """
        body = dict()
        if room_id is not None:
            body['roomId'] = room_id
        if to_person_id is not None:
            body['toPersonId'] = to_person_id
        if to_person_email is not None:
            body['toPersonEmail'] = to_person_email
        if text is not None:
            body['text'] = text
        if markdown is not None:
            body['markdown'] = markdown
        if files is not None:
            body['files'] = files
        if attachments is not None:
            body['attachments'] = TypeAdapter(list[Attachment]).dump_python(attachments, mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        data = super().post(url, json=body)
        r = Message.model_validate(data)
        return r

    def get_message_details(self, message_id: str) -> Message:
        """
        Get Message Details

        Shows details for a message, by message ID.

        Specify the message ID in the `messageId` parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        :rtype: :class:`Message`
        """
        url = self.ep(f'{message_id}')
        data = super().get(url)
        r = Message.model_validate(data)
        return r

    def delete_a_message(self, message_id: str):
        """
        Delete a Message

        Deletes a message, by message ID.

        Specify the message ID in the `messageId` parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        :rtype: None
        """
        url = self.ep(f'{message_id}')
        super().delete(url)
