from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Attachment', 'DirectMessage', 'DirectMessageCollectionResponse', 'File', 'FileType', 'Message',
            'MessageCollectionResponse', 'MessageRoomType']


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
    #: see [Message Attachments](/docs/api/basics#message-attachments).
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
    #: see [Message Attachments](/docs/api/basics#message-attachments).
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


class MessageCollectionResponse(ApiModel):
    items: Optional[list[Message]] = None


class DirectMessageCollectionResponse(ApiModel):
    items: Optional[list[DirectMessage]] = None
