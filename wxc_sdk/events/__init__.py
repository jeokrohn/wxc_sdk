from collections.abc import Generator
from datetime import datetime
from typing import Optional, Any

from ..api_child import ApiChild
from ..base import ApiModel, dt_iso_str
from ..base import SafeEnum as Enum

__all__ = ['EventData', 'ComplianceEvent', 'EventResource', 'EventType', 'EventsApi']


class EventResource(str, Enum):
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


class EventType(str, Enum):
    #: The resource has been created
    created = 'created'
    #: A property on the resource has been updated
    updated = 'updated'
    #: The resource has been deleted
    deleted = 'deleted'
    #: The meeting has ended
    ended = 'ended'
    read = 'read'


class EventData(ApiModel):
    id: Optional[str]
    room_id: Optional[str]
    type: Optional[str]
    room_type: Optional[str]
    is_room_hidden: Optional[bool]
    org_id: Optional[str]
    text: Optional[str]
    files: Optional[list[str]]
    person_id: Optional[str]
    person_email: Optional[str]
    person_org_id: Optional[str]
    person_display_name: Optional[str]
    is_moderator: Optional[bool]
    is_monitor: Optional[bool]
    meeting_id: Optional[str]
    creator_id: Optional[str]
    #: The meeting's host data
    host: Optional[object]
    #: Common Identity (CI) authenticated meeting attendees
    attendees: Optional[list[Any]]
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If true a transcript should be
    #: available a couple minutes after the meeting ended at the meetingTranscripts resource
    transcription_enabled: Optional[str]
    #: indicates if recording was enabled for all or parts of the meeting. If true a recording should be available
    #: shortly after the meeting ended at the recordings resource
    recording_enabled: Optional[str]
    #: indicates i chat messages were exchanged during the meeting in the meetings client (not the unified client).
    #: If true these messages can be accessed by a compliance officer at the postMeetingsChat resource. Meetings chat
    #: collection must be custom enabled.
    has_post_meetings_chat: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]
    markdown: Optional[str]
    html: Optional[str]
    mentioned_people: Optional[list[str]]
    file_content_url: Optional[str]
    file_id: Optional[str]
    page_number: Optional[int]
    is_locked: Optional[bool]
    is_public: Optional[bool]
    made_public: Optional[datetime]
    is_announcement_only: Optional[bool]


class ComplianceEvent(ApiModel):
    #: The unique identifier for the event.
    id: Optional[str]
    #: The type of resource in the event.
    resource: Optional[EventResource]
    #: The action which took place in the event.
    type: Optional[EventType]
    #: The ID of the application for the event.
    app_id: Optional[str]
    #: The ID of the person who performed the action.
    actor_id: Optional[str]
    #: The ID of the organization for the event.
    org_id: Optional[str]
    #: The date and time of the event.
    created: Optional[datetime]
    #: The event's data representation. This object will contain the event's resource, such as memberships, messages,
    #: meetings, tabs, rooms or attachmentActions at the time the event took place.
    data: Optional[EventData]


class EventsApi(ApiChild, base='events'):
    """
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    The Events API can only be used by a Compliance Officer with an API access token that contains the
    spark-compliance:events_read scope. See the Compliance Guide for more information.
    """

    def list(self, resource: EventResource = None, type_: EventType = None, actor_id: str = None,
             from_: datetime = None, to_: datetime = None, **params) -> Generator[ComplianceEvent, None, None]:
        """
        List events in your organization.
        Several query parameters are available to filter the events returned in
        the response. Long result sets will be split into pages.

        :param resource: List events with a specific resource type.
        :type resource: EventResource
        :param type_: List events with a specific event type.
        :type type_: EventType
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the
            future, lists events up to the present.
        :type to_: str
        """
        if resource is not None:
            params['resource'] = resource
        if type_ is not None:
            params['type'] = type_
        if actor_id is not None:
            params['actorId'] = actor_id
        if from_ is not None:
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ComplianceEvent, params=params)

    def details(self, event_id: str) -> ComplianceEvent:
        """
        Shows details for an event, by event ID.
        Specify the event ID in the eventId parameter in the URI.

        :param event_id: The unique identifier for the event.
        :type event_id: str
        """
        url = self.ep(f'{event_id}')
        data = super().get(url=url)
        return ComplianceEvent.parse_obj(data)
