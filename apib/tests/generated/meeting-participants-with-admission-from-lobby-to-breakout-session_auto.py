from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AdmitParticipant', 'Device', 'DeviceAudioType', 'DeviceCallType', 'InProgressDevice',
           'InProgressParticipant', 'InProgressParticipantState',
           'MeetingParticipantsWithAdmissionFromLobbyToBreakoutSessionApi', 'Participant', 'ParticipantState',
           'ParticipantVideo']


class ParticipantVideo(str, Enum):
    #: The video is turned on.
    on = 'on'
    #: The video is turned off.
    off = 'off'


class ParticipantState(str, Enum):
    #: The participant is waiting in the meeting lobby.
    lobby = 'lobby'
    #: The participant has left the meeting.
    end = 'end'
    #: The participant has joined the meeting and is in the main session.
    joined = 'joined'
    #: The participant has joined a breakout session.
    breakout_session = 'breakoutSession'


class DeviceAudioType(str, Enum):
    #: `PSTN`
    pstn = 'pstn'
    #: `VoIP`
    voip = 'voip'
    #: The participant is not connected to audio.
    inactive = 'inactive'


class DeviceCallType(str, Enum):
    #: Connect audio by dialing a toll or toll-free phone number provided by the meeting.
    call_in = 'callIn'
    #: Connect audio by dialing out a phone number from the meeting.
    call_back = 'callBack'


class Device(ApiModel):
    #: An internal ID that is associated with each join.
    #: example: 8ccced6c-b812-4dff-a5dd-4c5c28f8d47d
    correlation_id: Optional[str] = None
    #: The type of the device.
    #: example: webex_meeting_center_mac
    device_type: Optional[str] = None
    #: The audio type that the participant is using.
    #: example: pstn
    audio_type: Optional[DeviceAudioType] = None
    #: The time the device joined the meeting. If the field is non-existent or shows `1970-01-    01T00:00:00.000Z` the
    #: meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need
    #: real-time joined     events, please refer to the webhooks guide.
    #: example: 2019-04-23T17:31:00.000Z
    joined_time: Optional[datetime] = None
    #: The time the device left the meeting, `leftTime` is the exact moment when a specific devi    ce left the
    #: meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and
    #: the `leftTime` will     be filled in after the meeting ended. If you need real-time left events, please refer
    #: to the webhooks guide.
    #: example: 2019-04-23T17:32:00.000Z
    left_time: Optional[datetime] = None
    #: The duration in seconds the device stayed in the meeting.
    #: example: 60
    duration_second: Optional[int] = None
    #: The PSTN call type in which the device joined the meeting.
    #: example: callIn
    call_type: Optional[DeviceCallType] = None
    #: The PSTN phone number from which the device joined the meeting. Only `compliance officer
    #: <https://developer.webex.com/docs/compliance#compliance>`_ can retrieve the
    #: `phoneNumber`. The meeting host and admin users cannot retrieve it. NOTE: The `phoneNumber` will be returned
    #: after the meeting ends; it is not returned while the meeting is in progress.
    #: example: 745273328
    phone_number: Optional[str] = None


class Participant(ApiModel):
    #: The ID that identifies the meeting and the participant.
    #: example: 560d7b784f5143e3be2fc3064a5c4999_3c2e2338-e950-43bf-b588-573773ee43d1
    id: Optional[str] = None
    #: The ID that identifies the organization. It only applies to participants of ongoing meetings.
    #: example: 1eb65fdf-9643-417f-9974-ad72cae0e10f
    org_id: Optional[str] = None
    #: Whether or not the participant is the host of the meeting.
    #: example: True
    host: Optional[bool] = None
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool] = None
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool] = None
    #: The email address of the participant.
    #: example: joeDoe@cisco.com
    email: Optional[str] = None
    #: The name of the participant.
    #: example: Joe Doe
    display_name: Optional[str] = None
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool] = None
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool] = None
    #: The time the meeting started.
    #: example: 2020-10-02T17:31:00Z
    meeting_start_time: Optional[datetime] = None
    #: The status of the participant's video.
    #: example: on
    video: Optional[ParticipantVideo] = None
    #: The status of the participant in the meeting. The value of `state` is `breakoutSession` which is only returned
    #: when the meeting is in progress and the breakout session is enabled.
    #: example: lobby
    state: Optional[ParticipantState] = None
    #: The time the participant joined the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z`
    #: the meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need
    #: real-time join events, please refer to the webhooks guide.
    #: example: 2022-10-25T09:00:00Z
    joined_time: Optional[datetime] = None
    #: The time the participant left the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the
    #: meeting may be still ongoing and the `leftTime` will be filled in after the meeting ended. If you need
    #: real-time left events, please refer to the webhooks guide.
    #: example: 2022-10-25T09:30:00Z
    left_time: Optional[datetime] = None
    #: The site URL.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: A unique identifier for the meeting which the participant belongs to.
    #: example: 3a688f62840346e8b87dde2b50703511_I_197977258267247872
    meeting_id: Optional[str] = None
    #: The email address of the host.
    #: example: janeDoe@cisco.com
    host_email: Optional[str] = None
    devices: Optional[list[Device]] = None
    #: The source ID of the participant. The `sourceId` is from the `Create Invitation Sources
    #: <https://developer.webex.com/docs/api/v1/meetings/create-invitation-sources>`_ API.
    #: example: cisco
    source_id: Optional[str] = None


class InProgressParticipantState(str, Enum):
    #: The participant is waiting in the meeting lobby.
    lobby = 'lobby'
    #: The participant has joined the meeting.
    joined = 'joined'


class InProgressDevice(ApiModel):
    #: An internal ID that is associated with each join.
    #: example: 8ccced6c-b812-4dff-a5dd-4c5c28f8d47d
    correlation_id: Optional[str] = None
    #: The type of device.
    #: example: mac
    device_type: Optional[str] = None
    #: The audio type that the participant is using.
    #: example: pstn
    audio_type: Optional[DeviceAudioType] = None
    #: The time the device joined the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the
    #: meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need
    #: real-time joined events, please refer to the webhooks guide.
    #: example: 2019-04-23T17:31:00.000Z
    joined_time: Optional[datetime] = None
    #: The time the device left the meeting, `leftTime` is the exact moment when a specific device left the meeting. If
    #: the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the
    #: `leftTime` will be filled in after the meeting ended. If you need real-time left events, please refer to the
    #: webhooks guide.
    #: example: 2019-04-23T17:32:00.000Z
    left_time: Optional[datetime] = None


class InProgressParticipant(ApiModel):
    #: The participant ID that identifies the meeting and the participant.
    #: example: 560d7b784f5143e3be2fc3064a5c4999_3c2e2338-e950-43bf-b588-573773ee43d1
    id: Optional[str] = None
    #: The ID that identifies the organization.
    #: example: 1eb65fdf-9643-417f-9974-ad72cae0e10f
    org_id: Optional[str] = None
    #: Whether or not the participant is the host of the meeting.
    #: example: True
    host: Optional[bool] = None
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool] = None
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool] = None
    #: The email address of the participant.
    #: example: joeDoe@cisco.com
    email: Optional[str] = None
    #: The name of the participant.
    #: example: Joe Doe
    display_name: Optional[str] = None
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool] = None
    #: The status of the participant's video.
    #: example: on
    video: Optional[ParticipantVideo] = None
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool] = None
    #: The status of the participant in the meeting.
    #: example: lobby
    state: Optional[InProgressParticipantState] = None
    #: The site URL.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: A unique identifier for the meeting which the participant belongs to.
    #: example: 3a688f62840346e8b87dde2b50703511_I_197977258267247872
    meeting_id: Optional[str] = None
    #: The email address of the host.
    #: example: janeDoe@cisco.com
    host_email: Optional[str] = None
    devices: Optional[list[InProgressDevice]] = None


class AdmitParticipant(ApiModel):
    #: The ID that identifies the meeting participant.
    #: example: 560d7b784f5143e3be2fc3064a5c4999_I_204252993233618782_23e16d67-17f3-3ef1-b830-f33d17c0232e
    participant_id: Optional[str] = None
    #: The breakout session ID that identifies which breakout session to admit the participant into. Admit into the
    #: main session if the value is empty.
    #: example: 23e16d67-17f3-3ef1-b830-f33d17c0232e
    breakout_session_id: Optional[str] = None


class MeetingParticipantsWithAdmissionFromLobbyToBreakoutSessionApi(ApiChild, base='meetingParticipants'):
    """
    Meeting Participants with Admission from Lobby to Breakout Session
    
    This API manages meeting participants.
    
    Refer to the `Meetings API Scopes
    <https://developer.webex.com/docs/meetings#meetings-api-scopes>`_ section of `Meetings Overview
    """

    def list_meeting_participants(self, meeting_id: str, meeting_start_time_from: Union[str, datetime] = None,
                                  meeting_start_time_to: Union[str, datetime] = None, host_email: str = None,
                                  join_time_from: Union[str, datetime] = None, join_time_to: Union[str,
                                  datetime] = None, **params) -> Generator[Participant, None, None]:
        """
        List Meeting Participants

        List all participants in an in-progress meeting or an ended meeting. The `meetingId` parameter is required,
        which is the unique identifier for the meeting.

        The authenticated user calling this API must either have an Administrator role with the
        `meeting:admin_participants_read` scope, or be the meeting host.

        * If the `meetingId` value specified is for a meeting series, the operation returns participants' details for
        the last instance in the meeting series. If the `meetingStartTimeFrom` value and the `meetingStartTimeTo`
        value are specified, the operation returns participants' details for the last instance in the meeting series
        in the time range.

        * If the `meetingId` value specified is for a scheduled meeting from a meeting series, the operation returns
        participants' details for that scheduled meeting. If the `meetingStartTimeFrom` value and the
        `meetingStartTimeTo` value are specified, the operation returns participants' details for the last instance in
        the scheduled meeting in the time range.

        * If the `meetingId` value specified is for a meeting instance which is in progress or ended, the operation
        returns participants' details for that meeting instance.

        * If the meeting is in progress, the operation returns all the real-time participants. If the meeting is ended,
        the operation returns all the participants that have joined the meeting.

        * The `meetingStartTimeFrom` and `meetingStartTimeTo` only apply when `meetingId` is a series ID or an
        occurrence ID.

        * If the webinar is in progress when the attendee has ever been unmuted to speak in the webinar, this attendee
        becomes a panelist. The operation returns include the people who have been designated as panelists when the
        webinar is created and have joined the webinar, and the attendees who have joined the webinar and are unmuted
        to speak in the webinar temporarily. If the webinar is ended, the operation returns all the participants,
        including all panelists and all attendees who are not panelists.

        #### Request Header

        * `timezone`: Time zone for time stamps in the response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_.

        :param meeting_id: The unique identifier for the meeting. Please note that currently meeting ID of a scheduled
            `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Meetings start from the specified date and time(exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. If `meetingStartTimeFrom` is not specified, it equals `meetingStartTimeTo` minus 1
            month; if `meetingStartTimeTo` is also not specified, the default value for `meetingStartTimeFrom` is 1
            month before current date and time.
        :type meeting_start_time_from: Union[str, datetime]
        :param meeting_start_time_to: Meetings start before the specified date and time(exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. If `meetingStartTimeTo` is not specified, it equals the result of a comparison,
            `meetingStartTimeFrom` plus one month and the current time, and the result is the earlier of the two; if
            `meetingStartTimeFrom` is also not specified, the default value for `meetingStartTimeTo` is current date
            and time minus 1 month.
        :type meeting_start_time_to: Union[str, datetime]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they
            manage and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `joinTimeFrom` is not specified, it equals `joinTimeTo` minus 7 days.
        :type join_time_from: Union[str, datetime]
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `joinTimeTo` is not specified, it equals `joinTimeFrom` plus 7 days. The
            interval between `joinTimeFrom` and `joinTimeTo` must be within 90 days.
        :type join_time_to: Union[str, datetime]
        :return: Generator yielding :class:`Participant` instances
        """
        params['meetingId'] = meeting_id
        if meeting_start_time_from is not None:
            if isinstance(meeting_start_time_from, str):
                meeting_start_time_from = isoparse(meeting_start_time_from)
            meeting_start_time_from = dt_iso_str(meeting_start_time_from)
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            if isinstance(meeting_start_time_to, str):
                meeting_start_time_to = isoparse(meeting_start_time_to)
            meeting_start_time_to = dt_iso_str(meeting_start_time_to)
            params['meetingStartTimeTo'] = meeting_start_time_to
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            if isinstance(join_time_from, str):
                join_time_from = isoparse(join_time_from)
            join_time_from = dt_iso_str(join_time_from)
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            if isinstance(join_time_to, str):
                join_time_to = isoparse(join_time_to)
            join_time_to = dt_iso_str(join_time_to)
            params['joinTimeTo'] = join_time_to
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Participant, item_key='items', params=params)

    def query_meeting_participants_with_email(self, meeting_id: str, meeting_start_time_from: Union[str,
                                              datetime] = None, meeting_start_time_to: Union[str, datetime] = None,
                                              host_email: str = None, emails: list[str] = None,
                                              join_time_from: Union[str, datetime] = None, join_time_to: Union[str,
                                              datetime] = None) -> list[Participant]:
        """
        Query Meeting Participants with Email

        Query participants in a live meeting, or after the meeting, using participant's email. The `meetingId`
        parameter is the unique identifier for the meeting and is required.

        The authenticated user calling this API must either have an Administrator role with the
        `meeting:admin_participants_read` scope, or be the meeting host.

        * If the `meetingId` value specified is for a meeting series, the operation returns participants' details for
        the last instance in the meeting series. If the `meetingStartTimeFrom` value and the `meetingStartTimeTo`
        value are specified, the operation returns participants' details for the last instance in the meeting series
        in the time range.

        * If the `meetingId` value specified is for a scheduled meeting from a meeting series, the operation returns
        participants' details for that scheduled meeting. If the `meetingStartTimeFrom` value and the
        `meetingStartTimeTo` value are specified, the operation returns participants' details for the last instance in
        the scheduled meeting in the time range.

        * If the `meetingId` value specified is for a meeting instance which is in progress or ended, the operation
        returns participants' details for that meeting instance.

        * The `meetingStartTimeFrom` and `meetingStartTimeTo` only apply when `meetingId` is a series ID or an
        occurrence ID.

        #### Request Header

        * `timezone`: Time zone for time stamps in the response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_.

        :param meeting_id: The unique identifier for the meeting.
        :type meeting_id: str
        :param meeting_start_time_from: Meetings start from the specified date and time(exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. If `meetingStartTimeFrom` is not specified, it equals `meetingStartTimeTo` minus 1
            month; if `meetingStartTimeTo` is also not specified, the default value for `meetingStartTimeFrom` is 1
            month before current date and time.
        :type meeting_start_time_from: Union[str, datetime]
        :param meeting_start_time_to: Meetings start before the specified date and time(exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. If `meetingStartTimeTo` is not specified, it equals the result of a comparison,
            `meetingStartTimeFrom` plus one month and the current time, and the result is the earlier of the two; if
            `meetingStartTimeFrom` is also not specified, the default value for `meetingStartTimeTo` is current date
            and time minus 1 month.
        :type meeting_start_time_to: Union[str, datetime]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they
            manage and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param emails: Participants email list
        :type emails: list[str]
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `joinTimeFrom` is not specified, it equals `joinTimeTo` minus 7 days.
        :type join_time_from: Union[str, datetime]
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `joinTimeTo` is not specified, it equals `joinTimeFrom` plus 7 days. The
            interval between `joinTimeFrom` and `joinTimeTo` must be within 90 days.
        :type join_time_to: Union[str, datetime]
        :rtype: list[Participant]
        """
        params = {}
        params['meetingId'] = meeting_id
        if meeting_start_time_from is not None:
            if isinstance(meeting_start_time_from, str):
                meeting_start_time_from = isoparse(meeting_start_time_from)
            meeting_start_time_from = dt_iso_str(meeting_start_time_from)
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            if isinstance(meeting_start_time_to, str):
                meeting_start_time_to = isoparse(meeting_start_time_to)
            meeting_start_time_to = dt_iso_str(meeting_start_time_to)
            params['meetingStartTimeTo'] = meeting_start_time_to
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        if emails is not None:
            body['emails'] = emails
        if join_time_from is not None:
            body['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            body['joinTimeTo'] = join_time_to
        url = self.ep('query')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[Participant]).validate_python(data['items'])
        return r

    def get_meeting_participant_details(self, participant_id: str, host_email: str = None) -> Participant:
        """
        Get Meeting Participant Details

        Get a meeting participant details of a live or post meeting. The `participantId` is required to identify the
        meeting and the participant.

        The authenticated user calling this API must either have an Administrator role with the
        `meeting:admin_participants_read` scope, or be the meeting host.

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they
            manage and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :rtype: :class:`Participant`
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{participant_id}')
        data = super().get(url, params=params)
        r = Participant.model_validate(data)
        return r

    def update_a_participant(self, participant_id: str, muted: str = None, admit: str = None,
                             expel: str = None) -> InProgressParticipant:
        """
        Update a Participant

        To mute, un-mute, expel, or admit a participant in a live meeting. The `participantId` is required to identify
        the meeting and the participant.

        Notes:

        * The owner of the OAuth token calling this API needs to be the meeting host or co-host.

        * The `expel` attribute always takes precedence over `admit` and `muted`. The request can have all `expel`,
        `admit` and `muted` or any of them.

        <div><Callout type="warning">There is an inconsistent behavior in Webex Meetings App when all active meeting
        participants join using Webex Meetings App and the host attempts to change meeting participant status using
        this API. Requests to mute, un-mute, admit, or expel a meeting participant return a successful response and
        update the state in the API, but the changes will not be applied to the Webex Meetings App participants. The
        inconsistent behavior in Webex Meetings App will be corrected in a future release.
        **Workaround**: `Enable closed captions
        <https://help.webex.com/en-us/article/WBX47352/How-Do-I-Enable-Closed-Captions?>`_ or enable the `Webex Assistant

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param muted: The value is true or false, and means to mute or unmute the audio of a participant.
        :type muted: str
        :param admit: The value can be true or false. The value of true is to admit a participant to the meeting if the
            participant is in the lobby, No-Op if the participant is not in the lobby or when the value is set to
            false.
        :type admit: str
        :param expel: The attribute is exclusive and its value can be true or false. The value of true means that the
            participant will be expelled from the meeting, the value of false means No-Op.
        :type expel: str
        :rtype: :class:`InProgressParticipant`
        """
        body = dict()
        if muted is not None:
            body['muted'] = muted
        if admit is not None:
            body['admit'] = admit
        if expel is not None:
            body['expel'] = expel
        url = self.ep(f'{participant_id}')
        data = super().put(url, json=body)
        r = InProgressParticipant.model_validate(data)
        return r

    def admit_participants(self, items: list[AdmitParticipant]):
        """
        Admit Participants

        To admit participants into a live meeting or its breakout sessions in bulk. If `breakoutSessionId` is null for
        all the requested participants, they are admitted into the main session of the meeting. If `breakoutSessionId`
        is not null for all the requested participants, they are admitted into the breakout sessions specified by each
        `breakoutSessionId`. It's not allowed that some requested participants have `breakoutSessionId` and the others
        haven't.

        This API limits the maximum size of `items` in the request body to 100.

        Each `participantId` of `items` in the request body should have the same prefix of `meetingId`.

        :type items: list[AdmitParticipant]
        :rtype: None
        """
        body = dict()
        body['items'] = TypeAdapter(list[AdmitParticipant]).dump_python(items, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('admit')
        super().post(url, json=body)
