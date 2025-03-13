from collections.abc import Generator
from datetime import datetime
from typing import Optional, Any, Union

from dateutil.parser import isoparse

from ..api_child import ApiChild
from ..base import ApiModel, dt_iso_str, enum_str
from ..base import SafeEnum as Enum

__all__ = ['EventData', 'ComplianceEvent', 'EventResource', 'EventType', 'Recipient', 'EventsApi']


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
    #: A user sent or received a SMS message
    business_texts = 'businessTexts'
    #: A Webex call was made to/from a user
    call_records = 'call_records'


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
    all = 'all'


class Recipient(ApiModel):
    #: The personId of the recipient
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lOGYwOTIwOC00ZjUxLTExZWYtOTQ4My1iYTA3NjE2MzY4NmQ
    person_id: Optional[str] = None
    #: The personEmail
    #: example: johndoe@simplistic.com
    person_email: Optional[str] = None
    #: Guests, who are unauthenticated users, have a guestDisplayName
    #: example: John Wayne
    guest_display_name: Optional[str] = None
    #: Guests, who are unauthenticated users, have a guestEmail
    #: example: jwayne@mailinator.com
    guest_email: Optional[str] = None


class EventData(ApiModel):
    title: Optional[str] = None
    type: Optional[str] = None
    is_room_hidden: Optional[bool] = None
    files: Optional[list[str]] = None
    person_org_id: Optional[str] = None
    person_display_name: Optional[str] = None
    is_moderator: Optional[bool] = None
    is_monitor: Optional[bool] = None
    updated: Optional[datetime] = None
    markdown: Optional[str] = None
    html: Optional[str] = None
    mentioned_people: Optional[list[str]] = None
    file_content_url: Optional[str] = None
    file_id: Optional[str] = None
    page_number: Optional[int] = None
    title_encryption_key_url: Optional[str] = None
    is_locked: Optional[bool] = None
    is_public: Optional[bool] = None
    made_public: Optional[datetime] = None
    is_announcement_only: Optional[bool] = None
    id: Optional[str] = None
    room_id: Optional[str] = None
    room_type: Optional[str] = None
    org_id: Optional[str] = None
    #: this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    attachments: Optional[list[Any]] = None
    person_id: Optional[str] = None
    person_email: Optional[str] = None
    meeting_id: Optional[str] = None
    creator_id: Optional[str] = None
    #: The meeting's host data
    host: Optional[Any] = None
    #: Common Identity (CI) authenticated meeting attendees
    attendees: Optional[list[str]] = None
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If `true` a transcript should be
    #: available a couple minutes after the meeting ended at the `meetingTranscripts resource
    #: <https://developer.webex.com/docs/api/v1/meeting-transcripts>`_
    transcription_enabled: Optional[str] = None
    #: indicates if recording was enabled for all or parts of the meeting. If `true` a recording should be available
    #: shortly after the meeting ended at the `recordings resource
    #: <https://developer.webex.com/docs/api/v1/recordings>`_
    recording_enabled: Optional[str] = None
    #: indicates if chat messages were exchanged during the meeting in the meetings client (not the unified client). If
    #: `true` these messages can be accessed by a compliance officer at the `postMeetingsChat
    #: <https://developer.webex.com/docs/api/v1/meetings-chat>`_ resource. Meetings chat
    #: collection must be custom enabled.
    has_post_meetings_chat: Optional[str] = None
    #: Telephony; corelation id
    correlation_id: Optional[str] = None
    #: Telephony; call types (examples
    #: `VIDEO_DIALIN`,`VIDEO_DIALOUT`,`CASCADE`,`HYBRID_CASCADE`,`PSTN_SIP`,`PSTN_DIALIN`,`PSTN_DIALOUT`,
    #: `PSTN_ONLY_DIALIN`,`PSTN_ONLY_DIALOUT`,`H323`,`H323_IP`,`SIP_ENTERPRISE`,`SIP_MOBILE`,`SIP_NATIONAL`,
    #: `SIP_INTERNATIONAL`,`SIP_EMERGENCY`,`SIP_OPERATOR`,`SIP_SHORTCODE`,`SIP_TOLLFREE`,`SIP_PREMIUM`,`SIP_URI`,
    #: `SIP_INBOUND`,`UNKNOWN`,`ZTM`,`SIP_MEETING`)
    call_type: Optional[str] = None
    #: Telephony; user id of the CDR owner
    user_id: Optional[str] = None
    #: Telephony; type of user
    #: (`User`,`Anchor`,`AutomatedAttendantBasic`,`AutomatedAttendantStandard`,`AutomatedAttendantVideo`,
    #: `BroadworksAnywhere`,`CallCenterBasic`,`CallCenterPremium`,`CallCenterStandard`,`CollaborateBridge`,
    #: `ContactCenterAdaptor`,`FindMeFollowMe`,`FlexibleSeatingHost`,`GroupCall`,`GroupPaging`,`HuntGroup`,
    #: `LocalGateway`,`MeetMeConference`,`Place`,`RoutePoint`,`SystemVoicePortal`,`VoiceMailGroup`,
    #: `VoiceMailRetrieval`,`VoiceXML`,`VirtualLine`,`Unknown`)
    user_type: Optional[str] = None
    #: Telephony; `ORIGINATING` or `TERMINATING`
    call_direction: Optional[str] = None
    #: Telephony; indicates if the call was answered
    is_call_answered: Optional[bool] = None
    #: Telephony; duration of call in seconds
    call_duration_seconds: Optional[datetime] = None
    #: Telephony; ISO 8601
    call_start_time: Optional[datetime] = None
    #: Telephony; ISO 8601
    call_answer_time: Optional[datetime] = None
    #: Telephony; ISO 8601
    call_transfer_time: Optional[datetime] = None
    #: Telephony; originating number
    calling_number: Optional[str] = None
    #: Telephony
    calling_line_id: Optional[str] = None
    #: Telephony; destination number
    called_number: Optional[str] = None
    #: Telephony
    called_line_id: Optional[str] = None
    #: Telephony
    dialed_digits: Optional[str] = None
    #: Telephony
    call_redirecting_number: Optional[str] = None
    #: Telephony
    call_redirected_reason: Optional[str] = None
    created: Optional[datetime] = None
    #: Message type `direct` or `group` message.
    type: Optional[str] = None
    #: The breakout session Id in cases where the action happened in a meeting's brakout session, for example a
    #: `meetingMessage`.
    breakout_session_id: Optional[str] = None
    #: the recipients list for directed meetingMessages.
    recipients: Optional[list[Recipient]] = None
    content_url: Optional[str] = None


class ComplianceEvent(ApiModel):
    #: The unique identifier for the event.
    id: Optional[str] = None
    #: The type of resource in the event.
    resource: Optional[EventResource] = None
    #: The action which took place in the event.
    type: Optional[EventType] = None
    #: The ID of the application for the event.
    app_id: Optional[str] = None
    #: The ID of the person who performed the action.
    actor_id: Optional[str] = None
    #: The ID of the organization for the event.
    org_id: Optional[str] = None
    #: The date and time of the event.
    created: Optional[datetime] = None
    #: The event's data representation. This object will contain the event's resource, such as memberships, messages,
    #: meetings, tabs, rooms or attachmentActions at the time the event took place.
    data: Optional[EventData] = None


class EventsApi(ApiChild, base='events'):
    """
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    The Events API can only be used by a Compliance Officer with an API access token that contains the
    spark-compliance:events_read scope. See the Compliance Guide for more information.
    """

    def list(self, resource: EventResource = None, type_: EventType = None, actor_id: str = None,
             from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
             **params) -> Generator[ComplianceEvent, None, None]:
        """
        List events in your organization. Several query parameters are available to filter the response.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param resource: List events with a specific resource type.
        :type resource: EventResource
        :param type_: List events with a specific event type.
        :type type_: EventType
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events that occurred before a specific date and time. If not specified, events up to the
            present time will be listed. Cannot be set to a future date relative to the current time.
        :type to_: str
        """
        if resource is not None:
            params['resource'] = enum_str(resource)
        if type_ is not None:
            params['type'] = enum_str(type_)
        if actor_id is not None:
            params['actorId'] = actor_id
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
        return ComplianceEvent.model_validate(data)
