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
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9jZTg2MWZiYS02ZTJmLTQ5ZjktOWE4NC1iMzU0MDA4ZmFjOWU
    org_id: Optional[str] = None
    #: example: PROJECT UPDATE - A new project plan has been published on Box: http://box.com/s/lf5vj. The PM for this project is Mike C. and the Engineering Manager is Jane W.
    text: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: example: matt@example.com
    person_email: Optional[str] = None
    #: example: 16ce696f75844d24b2d4fab04b4419af_I_183979003076423608
    meeting_id: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82YWE2ZGE5OS0xYzdlLTQ4MWItODY3YS03MWY2NTIwNDk0MzM
    creator_id: Optional[str] = None
    #: The meeting's host data
    host: Optional[Any] = None
    #: Common Identity (CI) authenticated meeting attendees
    attendees: Optional[list[str]] = None
    #: indicates whether or not the Voice Assistant was enabled during the meeting. If `true` a transcript should be
    #: available a couple minutes after the meeting ended at the `meetingTranscripts resource
    #: <https://developer.webex.com/docs/api/v1/meeting-transcripts>`_
    #: example: yes
    transcription_enabled: Optional[str] = None
    #: indicates if recording was enabled for all or parts of the meeting. If `true` a recording should be available
    #: shortly after the meeting ended at the `recordings resource
    #: <https://developer.webex.com/docs/api/v1/recordings>`_
    #: example: yes
    recording_enabled: Optional[str] = None
    #: indicates if chat messages were exchanged during the meeting in the meetings client (not the unified client). If
    #: `true` these messages can be accessed by a compliance officer at the `postMeetingsChat
    #: <https://developer.webex.com/docs/api/v1/meetings-chat>`_ resource. Meetings chat
    #: collection must be custom enabled.
    #: example: yes
    has_post_meetings_chat: Optional[str] = None
    #: telephony; corelation id
    #: example: fdda8613-d34b-424c-8c6a-44ff2e19379c
    corelation_id: Optional[str] = None
    #: telephony; call types (examples
    #: `VIDEO_DIALIN`,`VIDEO_DIALOUT`,`CASCADE`,`HYBRID_CASCADE`,`PSTN_SIP`,`PSTN_DIALIN`,`PSTN_DIALOUT`,`PSTN_ONLY_DIALIN`,`PSTN_ONLY_DIALOUT`,`H323`,`H323_IP`,`SIP_ENTERPRISE`,`SIP_MOBILE`,`SIP_NATIONAL`,`SIP_INTERNATIONAL`,`SIP_EMERGENCY`,`SIP_OPERATOR`,`SIP_SHORTCODE`,`SIP_TOLLFREE`,`SIP_PREMIUM`,`SIP_URI`,`SIP_INBOUND`,`UNKNOWN`,`ZTM`,`SIP_MEETING`)
    #: example: SIP_ENTERPRISE
    call_type: Optional[str] = None
    #: telephony; user id of the CDR owner
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zZjEwMTU1NC04ZGJjLTQyMmUtOGEzZC1kYTk1YTI3NWZlNzU
    user_id: Optional[str] = None
    #: telephony; type of user
    #: (`User`,`Anchor`,`AutomatedAttendantBasic`,`AutomatedAttendantStandard`,`AutomatedAttendantVideo`,`BroadworksAnywhere`,`CallCenterBasic`,`CallCenterPremium`,`CallCenterStandard`,`CollaborateBridge`,`ContactCenterAdaptor`,`FindMeFollowMe`,`FlexibleSeatingHost`,`GroupCall`,`GroupPaging`,`HuntGroup`,`LocalGateway`,`MeetMeConference`,`Place`,`RoutePoint`,`SystemVoicePortal`,`VoiceMailGroup`,`VoiceMailRetrieval`,`VoiceXML`,`VirtualLine`,`Unknown`)
    #: example: User
    user_type: Optional[str] = None
    #: telephony; `ORIGINATING` or `TERMINATING`
    #: example: ORIGINTATING
    call_direction: Optional[str] = None
    #: telephony; indicates if the call was answered
    #: example: True
    is_call_answered: Optional[bool] = None
    #: telephony; duration of call in seconds
    #: example: 192
    call_duration_seconds: Optional[str] = None
    #: telephony; ISO 8601
    #: example: 2023-02-08T06:12:43.976Z
    call_start_time: Optional[datetime] = None
    #: telephony; ISO 8601
    #: example: 2023-02-08T06:12:47.012Z
    call_answer_time: Optional[datetime] = None
    #: telephony; ISO 8601
    #: example: 2023-02-08T06:15:19.112Z
    call_transfer_time: Optional[datetime] = None
    #: telephony; originating number
    #: example: 910481234
    calling_number: Optional[str] = None
    #: telephony
    #: example: 211
    calling_line_id: Optional[str] = None
    #: telephony; destination number
    #: example: 4089671221
    called_number: Optional[str] = None
    #: telephony
    #: example: 219
    called_line_id: Optional[str] = None
    #: telephony
    #: example: 123
    dialed_digits: Optional[str] = None
    #: telephony
    call_redirecting_number: Optional[str] = None
    #: telephony
    call_redirected_reason: Optional[str] = None
    #: example: 2016-05-16T21:34:59.324Z
    created: Optional[datetime] = None


class EventResourceEnum(str, Enum):
    #: State changed on a card attachment
    attachment_actions = 'attachmentActions'
    #: A user sent or received a SMS message
    business_texts = 'businessTexts'
    #: A Webex call was made to/from a user
    call_records = 'call_records'
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
    #: <https://developer.webex.com/docs/api/v1/memberships/get-membership-details>`_, `messages
    #: `meetings
    #: <https://developer.webex.com/docs/api/v1/meetings>`_, `tabs
    data: Optional[EventData] = None


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
                    **params) -> Generator[Event, None, None]:
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
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the
            future, lists events up to the present.
        :type to_: Union[str, datetime]
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
