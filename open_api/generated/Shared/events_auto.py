from __future__ import annotations

import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Event', 'EventData', 'EventResourceEnum', 'EventTypeEnum', 'EventsApi', 'Recipient', 'ServiceType']


class Recipient(ApiModel):
    #: The personId of the recipient
    person_id: Optional[str] = None
    #: The personEmail
    person_email: Optional[str] = None
    #: Guests, who are unauthenticated users, have a guestDisplayName
    guest_display_name: Optional[str] = None
    #: Guests, who are unauthenticated users, have a guestEmail
    guest_email: Optional[str] = None


class EventData(ApiModel):
    id: Optional[str] = None
    room_id: Optional[str] = None
    room_type: Optional[str] = None
    org_id: Optional[str] = None
    text: Optional[str] = None
    person_id: Optional[str] = None
    person_email: Optional[str] = None
    meeting_id: Optional[str] = None
    creator_id: Optional[str] = None
    #: The meeting's host data.
    host: Optional[dict] = None
    #: Common Identity (CI) authenticated meeting attendees.
    attendees: Optional[list[Any]] = None
    #: Indicates whether or not the Voice Assistant was enabled during the meeting. If `true` a transcript should be
    #: available a couple minutes after the meeting ended at the `meetingTranscripts resource
    #: <https://developer.webex.com/docs/api/v1/meeting-transcripts>`_.
    transcription_enabled: Optional[str] = None
    #: Indicates if recording was enabled for all or parts of the meeting. If `true` a recording should be available
    #: shortly after the meeting ended at the `recordings resource
    #: <https://developer.webex.com/docs/api/v1/recordings>`_.
    recording_enabled: Optional[str] = None
    #: Indicates if chat messages were exchanged during the meeting in the meetings client (not the unified client). If
    #: `true` these messages can be accessed by a compliance officer at the `postMeetingsChat
    #: <https://developer.webex.com/docs/api/v1/meetings-chat>`_ resource. Meetings chat
    #: collection must be custom enabled.
    has_post_meetings_chat: Optional[str] = None
    #: Telephony; The corelation id.
    corelation_id: Optional[str] = None
    #: Telephony; call types (examples
    #: `VIDEO_DIALIN`,`VIDEO_DIALOUT`,`CASCADE`,`HYBRID_CASCADE`,`PSTN_SIP`,`PSTN_DIALIN`,`PSTN_DIALOUT`,`PSTN_ONLY_DIALIN`,`PSTN_ONLY_DIALOUT`,`H323`,`H323_IP`,`SIP_ENTERPRISE`,`SIP_MOBILE`,`SIP_NATIONAL`,`SIP_INTERNATIONAL`,`SIP_EMERGENCY`,`SIP_OPERATOR`,`SIP_SHORTCODE`,`SIP_TOLLFREE`,`SIP_PREMIUM`,`SIP_URI`,`SIP_INBOUND`,`UNKNOWN`,`ZTM`,`SIP_MEETING`).
    call_type: Optional[str] = None
    #: Telephony; user id of the CDR owner.
    user_id: Optional[str] = None
    #: Telephony; The type of user
    #: (`User`,`Anchor`,`AutomatedAttendantBasic`,`AutomatedAttendantStandard`,`AutomatedAttendantVideo`,`BroadworksAnywhere`,`CallCenterBasic`,`CallCenterPremium`,`CallCenterStandard`,`CollaborateBridge`,`ContactCenterAdaptor`,`FindMeFollowMe`,`FlexibleSeatingHost`,`GroupCall`,`GroupPaging`,`HuntGroup`,`LocalGateway`,`MeetMeConference`,`Place`,`RoutePoint`,`SystemVoicePortal`,`VoiceMailGroup`,`VoiceMailRetrieval`,`VoiceXML`,`VirtualLine`,`Unknown`).
    user_type: Optional[str] = None
    #: Telephony; `ORIGINATING` or `TERMINATING`.
    call_direction: Optional[str] = None
    #: Telephony; indicates if the call was answered.
    is_call_answered: Optional[str] = None
    #: Telephony; duration of call in seconds.
    call_duration_seconds: Optional[str] = None
    #: Telephony; ISO 8601.
    call_start_time: Optional[datetime] = None
    #: Telephony; ISO 8601.
    call_answer_time: Optional[datetime] = None
    #: Telephony; ISO 8601.
    call_transfer_time: Optional[datetime] = None
    #: Telephony; originating number.
    calling_number: Optional[str] = None
    #: Telephony.
    calling_line_id: Optional[str] = None
    #: Telephony; destination number.
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
    #: The recipients list for directed meetingMessages.
    recipients: Optional[list[Recipient]] = None


class EventResourceEnum(str, Enum):
    #: State changed on a card attachment
    attachment_actions = 'attachmentActions'
    #: A user sent or received a SMS message
    business_texts = 'businessTexts'
    #: A Webex call was made to/from a user
    call_records = 'call_records'
    #: A Webex call was recorded for a user
    converged_recordings = 'convergedRecordings'
    #: State change on a file preview
    file_transcodings = 'file_transcodings'
    #: State changed on a file download
    files = 'files'
    #: State changed on a meeting message, i.e. message exchanged as part of a meeting
    meeting_messages = 'meetingMessages'
    #: State change on a meeting ( here combined with type = 'ended' )
    meetings = 'meetings'
    #: State change on a automatic transcript resource for Webex Assistant
    meeting_transcripts = 'meetingTranscripts'
    #: State changed on a memberships resource
    memberships = 'memberships'
    #: State changed on a messages resource
    messages = 'messages'
    #: State changed on a space classification
    rooms = 'rooms'
    #: State changed on a room tabs in a space
    tabs = 'tabs'


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
    id: Optional[str] = None
    #: The type of resource in the event.
    resource: Optional[EventResourceEnum] = None
    #: The action which took place in the event.
    type: Optional[EventTypeEnum] = None
    #: The ID of the application for the event.
    app_id: Optional[str] = None
    #: The ID of the person who performed the action.
    actor_id: Optional[str] = None
    #: The ID of the organization for the event.
    org_id: Optional[str] = None
    #: The date and time of the event.
    created: Optional[datetime] = None
    #: The event's data representation. This object will contain the event's `resource`, such as `memberships
    #: <https://developer.webex.com/docs/api/v1/memberships/get-membership-details>`_, `messages
    #: `meetings
    #: <https://developer.webex.com/docs/api/v1/meetings>`_, `meetingMessages
    data: Optional[EventData] = None


class ServiceType(str, Enum):
    calling = 'calling'


class EventsApi(ApiChild, base='events'):
    """
    Events
    
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    
    The Events API can only be used by a Compliance Officer with an API access token that contains the
    `spark-compliance:events_read` scope. See the `Compliance Guide
    <https://developer.webex.com/docs/compliance#compliance>`_ for more information.
    """

    def list_events(self, resource: EventResourceEnum = None, type: EventTypeEnum = None, actor_id: str = None,
                    from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                    service_type: ServiceType = None, **params: Any) -> Generator[Event, None, None]:
        """
        List Events

        List events in your organization. Several query parameters are available to filter the events returned in the
        response.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param resource: List events with a specific resource type.
        :type resource: EventResourceEnum
        :param type: List events with a specific event type.
        :type type: EventTypeEnum
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: Union[str, datetime]
        :param to_: List events that occurred before a specific date and time. If not specified, events up to the
            present time will be listed. Cannot be set to a future date relative to the current time.
        :type to_: Union[str, datetime]
        :param service_type: List events for a specific service type. This parameter is only applicable and mandatory
            when resource is set to `convergedRecordings`.
        :type service_type: ServiceType
        :return: Generator yielding :class:`Event` instances
        """
        if resource is not None:
            params['resource'] = enum_str(resource)
        if type is not None:
            params['type'] = enum_str(type)
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
        if service_type is not None:
            params['serviceType'] = enum_str(service_type)
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
