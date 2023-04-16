from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Data', 'Event', 'EventResourceEnum', 'EventTypeEnum', 'EventsApi', 'ListEventsResponse']


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
