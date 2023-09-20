from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Event', 'EventCollectionResponse', 'EventData', 'EventDataHost', 'EventResourceEnum', 'EventTypeEnum']


class EventDataHost(ApiModel):
    ...


class EventData(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    roomId: Optional[str] = None
    #: example: group
    roomType: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9jZTg2MWZiYS02ZTJmLTQ5ZjktOWE4NC1iMzU0MDA4ZmFjOWU
    orgId: Optional[str] = None
    #: example: PROJECT UPDATE - A new project plan has been published on Box: http://box.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    personId: Optional[str] = None
    #: example: matt@example.com
    personEmail: Optional[str] = None
    #: example: 16ce696f75844d24b2d4fab04b4419af_I_183979003076423608
    meetingId: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82YWE2ZGE5OS0xYzdlLTQ4MWItODY3YS03MWY2NTIwNDk0MzM
    creatorId: Optional[str] = None
    #: The meeting's host data
    host: Optional[EventDataHost] = None
    #: Common Identity (CI) authenticated meeting attendees
    attendees: Optional[list[str]] = None
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If `true` a transcript should be available a couple minutes after the meeting ended at the [meetingTranscripts resource](/docs/api/v1/meeting-transcripts)
    transcriptionEnabled: Optional[str] = None
    #: indicates if recording was enabled for all or parts of the meeting. If `true` a recording should be available shortly after the meeting ended at the [recordings resource](/docs/api/v1/recordings)
    recordingEnabled: Optional[str] = None
    #: indicates if chat messages were exchanged during the meeting in the meetings client (not the unified client). If `true` these messages can be accessed by a compliance officer at the [postMeetingsChat](/docs/api/v1/meetings-chat) resource. Meetings chat collection must be custom enabled.
    hasPostMeetingsChat: Optional[str] = None
    #: example: 2016-05-16T21:34:59.324Z
    created: Optional[datetime] = None


class EventResourceEnum(str, Enum):
    #: State changed on a messages resource
    messages = 'messages'
    #: State changed on a memberships resource
    memberships = 'memberships'
    #: State change on a meeting ( here combined with type = 'ended' )
    meetings = 'meetings'
    #: State change on a automatic transcript resource for Webex Assistant
    meetingtranscripts = 'meetingTranscripts'
    #: State changed on a meeting message, i.e. message exchanged as part of a meeting
    meetingmessages = 'meetingMessages'
    #: State changed on a room tabs in a space
    tabs = 'tabs'
    #: State changed on a space classification
    rooms = 'rooms'
    #: State changed on a card attachment
    attachmentactions = 'attachmentActions'
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


class Event(ApiModel):
    #: The unique identifier for the event.
    #: example: Y2lzY29zcGFyazovL3VzL0VWRU5UL2JiY2ViMWFkLTQzZjEtM2I1OC05MTQ3LWYxNGJiMGM0ZDE1NAo
    id: Optional[str] = None
    #: The type of resource in the event.
    #: example: messages
    resource: Optional[EventResourceEnum] = None
    #: The action which took place in the event.
    #: example: created
    type: Optional[EventTypeEnum] = None
    #: The ID of the application for the event.
    #: example: null
    appId: Optional[str] = None
    #: The ID of the person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    actorId: Optional[str] = None
    #: The ID of the organization for the event.
    #: example: OTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    orgId: Optional[str] = None
    #: The date and time of the event.
    #: example: 2016-05-16T21:34:59.324Z
    created: Optional[datetime] = None
    #: The event's data representation. This object will contain the event's `resource`, such as [memberships](/docs/api/v1/memberships/get-membership-details), [messages](/docs/api/v1/messages/get-message-details), [meetings](/docs/api/v1/meetings), [tabs](/docs/api/v1/room-tabs), [rooms](/docs/api/v1/space-classifications) or [attachmentActions](/docs/api/v1/attachment-actions) at the time the event took place.
    data: Optional[EventData] = None


class EventCollectionResponse(ApiModel):
    items: Optional[list[Event]] = None
