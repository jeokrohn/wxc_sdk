from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Event', 'EventCollectionResponse', 'EventData', 'EventResourceEnum', 'EventTypeEnum']


class EventData(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk
    id: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: example: group
    room_type: Optional[str] = None
    #: example: PROJECT UPDATE - A new project plan has been published: http://example.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: example: matt@example.com
    person_email: Optional[str] = None
    #: example: 2016-05-16T21:34:59.324Z
    created: Optional[datetime] = None


class EventResourceEnum(str, Enum):
    #: State changed on the messages resource.
    messages = 'messages'
    #: State changed on the memberships resource.
    memberships = 'memberships'


class EventTypeEnum(str, Enum):
    #: The resource has been created.
    created = 'created'
    #: A property on the resource has been updated.
    updated = 'updated'
    #: The resource has been deleted.
    deleted = 'deleted'


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
    app_id: Optional[str] = None
    #: The ID of the person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    actor_id: Optional[str] = None
    #: The ID of the organization for the event.
    #: example: OTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    org_id: Optional[str] = None
    #: The date and time of the event.
    #: example: 2016-05-16T21:34:59.324Z
    created: Optional[datetime] = None
    #: The event's data representation. This object will contain the event's `resource`, such as
    #: [memberships](/docs/api/v1/memberships/get-membership-details) or
    #: [messages](/docs/api/v1/messages/get-message-details), at the time the event took place.
    data: Optional[EventData] = None


class EventCollectionResponse(ApiModel):
    items: Optional[list[Event]] = None
