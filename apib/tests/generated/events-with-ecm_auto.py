from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Event', 'EventData', 'EventResourceEnum', 'EventTypeEnum', 'EventsApi']


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
    #: The event's data representation. This object will contain the event's `resource`, such as `memberships
    #: <https://developer.webex.com/docs/api/v1/memberships/get-membership-details>`_ or
    #: `messages
    #: <https://developer.webex.com/docs/api/v1/messages/get-message-details>`_, at the time the event took place.
    data: Optional[EventData] = None


class EventsApi(ApiChild, base='events'):
    """
    Events
    
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    Compliance Officers may use the Events API to retrieve events for all users within an organization. See the
    `Compliance Guide
    <https://developer.webex.com/docs/api/guides/compliance>`_ for more information.
    """

    def list_events(self, has_attachments: bool, resource: EventResourceEnum = None, type: EventTypeEnum = None,
                    actor_id: str = None, from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                    **params) -> Generator[Event, None, None]:
        """
        List Events

        List events in your organization. Several query parameters are available to filter the response.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param has_attachments: If enabled, filters message events to only those that contain the `attachments`
            attribute.
        :type has_attachments: bool
        :param resource: List events with a specific resource type.
        :type resource: EventResourceEnum
        :param type: List events with a specific event type.
        :type type: EventTypeEnum
        :param actor_id: List events performed by this person, by ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: Union[str, datetime]
        :param to_: List events which occurred before a specific date and time.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`Event` instances
        """
        if resource is not None:
            params['resource'] = enum_str(resource)
        if type is not None:
            params['type'] = enum_str(type)
        if actor_id is not None:
            params['actorId'] = actor_id
        params['hasAttachments'] = str(has_attachments).lower()
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Event, item_key='items', params=params)

    def get_event_details(self, event_id: str) -> Event:
        """
        Get Event Details

        Shows details for an event, by event ID.

        Specify the event ID in the `eventId` parameter in the URI.

        :param event_id: The unique identifier for the event.
        :type event_id: str
        :rtype: :class:`Event`
        """
        url = self.ep(f'{event_id}')
        data = super().get(url)
        r = Event.model_validate(data)
        return r
