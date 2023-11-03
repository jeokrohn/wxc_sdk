from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AdaptiveCard', 'AdaptiveCardActions', 'AdaptiveCardBody', 'Attachment', 'DirectMessage',
            'DirectMessageCollectionResponse', 'ListMessage', 'ListMessageCollectionResponse', 'Message',
            'MessageCollectionResponse', 'MessageRoomType']


class MessageRoomType(str, Enum):
    #: 1:1 room
    direct = 'direct'
    #: group room
    group = 'group'


class AdaptiveCardBody(ApiModel):
    #: example: TextBlock
    type: Optional[str] = None
    #: example: Adaptive Cards
    text: Optional[str] = None
    #: example: large
    size: Optional[str] = None


class AdaptiveCardActions(ApiModel):
    #: example: Action.OpenUrl
    type: Optional[str] = None
    #: example: http://adaptivecards.io
    url: Optional[str] = None
    #: example: Learn More
    title: Optional[str] = None


class AdaptiveCard(ApiModel):
    #: Must be `AdaptiveCard`.
    #: example: AdaptiveCard
    type: Optional[str] = None
    #: Adaptive Card schema version.
    #: example: 1.0
    version: Optional[datetime] = None
    #: The card's elements.
    body: Optional[list[AdaptiveCardBody]] = None
    #: The card's actions.
    actions: Optional[list[AdaptiveCardActions]] = None


class Attachment(ApiModel):
    #: The content type of the attachment.
    #: example: application/vnd.microsoft.card.adaptive
    content_type: Optional[str] = None
    #: Adaptive Card content.
    content: Optional[AdaptiveCard] = None


class Message(ApiModel):
    #: The unique identifier for the message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: The unique identifier for the parent message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    parent_id: Optional[str] = None
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
    #: example: PROJECT UPDATE - A new project plan has been published om http://example.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: The message, in Markdown format.
    #: example: **PROJECT UPDATE** A new project plan has been published on <http://box.com/s/lf5vj>. The PM for this project is <@personEmail:mike@example.com> and the Engineering Manager is <@personEmail:jane@example.com>.
    markdown: Optional[str] = None
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    #: example: <p><strong>PROJECT UPDATE</strong> A new project plan has been published <a href=\"http://example.com/s/lf5vj\" rel=\"nofollow\">here</a>. The PM for this project is mike@example.com and the Engineering Manager is jane@example.com.</p>
    html: Optional[str] = None
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see [Message Attachments](/docs/basics#message-attachments).
    #: example: ['http://www.example.com/images/media.png']
    files: Optional[list[str]] = None
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
    #: Message content attachments attached to the message. See the [Cards Guide](/docs/api/guides/cards) for more
    #: information.
    attachments: Optional[list[Attachment]] = None
    #: The date and time the message was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    #: example: 2015-10-18T14:27:16+00:00
    updated: Optional[datetime] = None
    #: True if the audio file is a voice clip recorded by the client; false if the audio file is a standard audio file
    #: not posted using the voice clip feature.
    is_voice_clip: Optional[bool] = None


class ListMessage(ApiModel):
    #: The unique identifier for the message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: The unique identifier for the parent message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    parent_id: Optional[str] = None
    #: The room ID of the message.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The type of room.
    #: example: group
    room_type: Optional[MessageRoomType] = None
    #: The message, in plain text. If `markdown` is specified this parameter may be *optionally* used to provide
    #: alternate text for UI clients that do not support rich text.
    #: example: PROJECT UPDATE - A new project plan has been published on http://example.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: The message, in Markdown format.
    #: example: **PROJECT UPDATE** A new project plan has been published on <http://example.com/s/lf5vj>. The PM for this project is <@personEmail:mike@example.com> and the Engineering Manager is <@personEmail:jane@example.com>.
    markdown: Optional[str] = None
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    #: example: <p><strong>PROJECT UPDATE</strong> A new project plan has been published <a href=\"http://example.com/s/lf5vj\" rel=\"nofollow\">here</a>. The PM for this project is mike@example.com and the Engineering Manager is jane@example.com.</p>
    html: Optional[str] = None
    #: Public URLs for files attached to the message. For the supported media types and the behavior of file uploads,
    #: see [Message Attachments](/docs/basics#message-attachments).
    #: example: ['http://www.example.com/images/media.png']
    files: Optional[list[str]] = None
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
    #: Message content attachments attached to the message. See the [Cards Guide](/docs/api/guides/cards) for more
    #: information.
    attachments: Optional[list[Attachment]] = None
    #: The date and time the message was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    #: example: 2015-10-18T14:27:16+00:00
    updated: Optional[datetime] = None
    #: `true` if the audio file is a voice clip recorded by the client; `false` if the audio file is a standard audio
    #: file not posted using the voice clip feature.
    is_voice_clip: Optional[bool] = None


class DirectMessage(ApiModel):
    #: The unique identifier for the message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: The unique identifier for the parent message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    parent_id: Optional[str] = None
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
    #: The text content of the message, in HTML format. This read-only property is used by the Webex clients.
    #: example: <p>Hey there, what do you think of <a href=\"http://sharepoint.example.com/presentation.pptx\" rel=\"nofollow\">this project update presentation</a>?</p>
    html: Optional[str] = None
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
    #: Message content attachments attached to the message. See the [Cards Guide](/docs/api/guides/cards) for more
    #: information.
    attachments: Optional[list[Attachment]] = None
    #: The date and time the message was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The date and time that the message was last edited by the author. This field is only present when the message
    #: contents have changed.
    #: example: 2015-10-18T14:27:16+00:00
    updated: Optional[datetime] = None
    #: True if the audio file is a voice clip recorded by the client; false if the audio file is a standard audio file
    #: not posted using the voice clip feature.
    is_voice_clip: Optional[bool] = None


class MessageCollectionResponse(ApiModel):
    items: Optional[list[Message]] = None


class ListMessageCollectionResponse(ApiModel):
    items: Optional[list[ListMessage]] = None


class DirectMessageCollectionResponse(ApiModel):
    items: Optional[list[DirectMessage]] = None
