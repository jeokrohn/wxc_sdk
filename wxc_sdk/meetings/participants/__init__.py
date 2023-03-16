from collections.abc import Generator
from typing import List, Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum

__all__ = ['AudioType', 'MeetingCallType', 'MeetingDevice', 'InProgressDevice', 'MeetingParticipantsApi', 'Participant',
           'ParticipantState',
           'UpdateParticipantResponse', 'VideoState', 'QueryMeetingParticipantsWithEmailBody', 'UpdateParticipantBody',
           'AdmitParticipantsBody']


class VideoState(str, Enum):
    #: The video is turned on.
    on = 'on'
    #: The video is turned off.
    off = 'off'


class ParticipantState(str, Enum):
    #: The participant is waiting in the meeting lobby.
    lobby = 'lobby'
    #: The participant has joined the meeting.
    joined = 'joined'
    #: The participant has left the meeting.
    end = 'end'


class MeetingCallType(str, Enum):
    #: Connect audio by dialing a toll or toll-free phone number provided by the meeting.
    call_in = 'callIn'
    #: Connect audio by dialing out a phone number from the meeting.
    call_back = 'callBack'


class AudioType(str, Enum):
    #: PSTN
    pstn = 'pstn'
    #: VoIP
    voip = 'voip'
    #: The participant is not connected to audio.
    inactive = 'inactive'


class InProgressDevice(ApiModel):
    #: An internal ID that is associated with each join.
    correlation_id: Optional[str]
    #: The type of device.
    device_type: Optional[str]
    #: The audio type that the participant is using.
    audio_type: Optional[AudioType]
    #: The time the device joined the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the joinedTime will be filled in after the meeting ended. If you need real-time
    #: joined events, please refer to the webhooks guide.
    joined_time: Optional[str]
    #: The time the device left the meeting, leftTime is the exact moment when a specific device left the meeting. If
    #: the field is non-existent or shows 1970-01-01T00:00:00.000Z the meeting may be still ongoing and the leftTime
    #: will be filled in after the meeting ended. If you need real-time left events, please refer to the webhooks
    #: guide.
    left_time: Optional[str]


class MeetingDevice(InProgressDevice):
    #: The duration in seconds the device stayed in the meeting.
    duration_second: Optional[int]
    #: The PSTN call type in which the device joined the meeting.
    call_type: Optional[MeetingCallType]
    #: The PSTN phone number from which the device joined the meeting. Only compliance officer can retrieve the
    #: phoneNumber. The meeting host and admin users cannot retrieve it. NOTE: The phoneNumber will be returned after
    #: the meeting ends; it is not returned while the meeting is in progress.
    phone_number: Optional[str]


class Participant(ApiModel):
    #: The ID that identifies the meeting and the participant.
    id: Optional[str]
    #: The ID that identifies the organization. It only applies to participants of ongoing meetings.
    org_id: Optional[str]
    #: Whether or not the participant is the host of the meeting.
    host: Optional[bool]
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool]
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool]
    #: The email address of the participant.
    email: Optional[str]
    #: The name of the participant.
    display_name: Optional[str]
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool]
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool]
    #: The status of the participant's video.
    video: Optional[VideoState]
    #: The status of the participant in the meeting.
    state: Optional[ParticipantState]
    #: The time the participant joined the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the joinedTime will be filled in after the meeting ended. If you need real-time
    #: join events, please refer to the webhooks guide.
    joined_time: Optional[str]
    #: The time the participant left the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the leftTime will be filled in after the meeting ended. If you need real-time
    #: left events, please refer to the webhooks guide.
    left_time: Optional[str]
    #: The site URL.
    site_url: Optional[str]
    #: A unique identifier for the meeting which the participant belongs to.
    meeting_id: Optional[str]
    #: The email address of the host.
    host_email: Optional[str]
    devices: Optional[list[MeetingDevice]]
    #: The source ID of the participant. The sourceId is from the Create Invitation Sources API.
    source_id: Optional[str]


class QueryMeetingParticipantsWithEmailBody(ApiModel):
    #: Participants email list
    #: Possible values: a@example.com
    emails: Optional[list[str]]


class UpdateParticipantBody(ApiModel):
    #: The value is true or false, and means to mute or unmute the audio of a participant.
    muted: Optional[bool]
    #: The value can be true or false. The value of true is to admit a participant to the meeting if the participant is
    #: in the lobby, No-Op if the participant is not in the lobby or when the value is set to false.
    admit: Optional[bool]
    #: The attribute is exclusive and its value can be true or false. The value of true means that the participant will
    #: be expelled from the meeting, the value of false means No-Op.
    expel: Optional[bool]


class UpdateParticipantResponse(ApiModel):
    #: The participant ID that identifies the meeting and the participant.
    id: Optional[str]
    #: The ID that identifies the organization.
    org_id: Optional[str]
    #: Whether or not the participant is the host of the meeting.
    host: Optional[bool]
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool]
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool]
    #: The email address of the participant.
    email: Optional[str]
    #: The name of the participant.
    display_name: Optional[str]
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool]
    #: The status of the participant's video.
    video: Optional[VideoState]
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool]
    #: The status of the participant in the meeting.
    state: Optional[ParticipantState]
    #: The site URL.
    site_url: Optional[str]
    #: A unique identifier for the meeting which the participant belongs to.
    meeting_id: Optional[str]
    #: The email address of the host.
    host_email: Optional[str]
    devices: Optional[list[InProgressDevice]]


class AdmitParticipantsBody(ApiModel):
    #: The ID that identifies the meeting participant.
    items: Optional[list[str]]


class MeetingParticipantsApi(ApiChild, base='meetingParticipants'):
    """
    This API manages meeting participants.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_participants(self, meeting_id: str, host_email: str = None, join_time_from: str = None,
                          join_time_to: str = None, **params) -> Generator[Participant, None, None]:
        """
        List all participants in a live or post meeting. The meetingId parameter is required, which is the unique
        identifier for the meeting.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Participant, params=params)

    def query_participants_with_email(self, meeting_id: str, max: int = None, host_email: str = None,
                                      join_time_from: str = None, join_time_to: str = None,
                                      emails: list[str] = None) -> list[Participant]:
        """
        Query participants in a live meeting, or after the meeting, using participant's email. The meetingId parameter
        is the unique identifier for the meeting and is required.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting.
        :type meeting_id: str
        :param max: Limit the maximum number of participants in the response, up to 1000.
        :type max: int
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        :param emails: Participants email list Possible values: a@example.com
        :type emails: List[str]
        """
        params = {}
        params['meetingId'] = meeting_id
        if max is not None:
            params['max'] = max
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        body = QueryMeetingParticipantsWithEmailBody()
        if emails is not None:
            body.emails = emails
        url = self.ep('query')
        data = super().post(url=url, params=params, data=body.json())
        # TODO: this is wrong -> fix code generation
        return data["items"]

    def participant_details(self, participant_id: str, host_email: str = None) -> Participant:
        """
        Get a meeting participant details of a live or post meeting. The participantId is required to identify the
        meeting and the participant.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{participant_id}')
        data = super().get(url=url, params=params)
        return Participant.parse_obj(data)

    def update_participant(self, participant_id: str, muted: bool = None, admit: bool = None,
                           expel: bool = None) -> UpdateParticipantResponse:
        """
        To mute, un-mute, expel, or admit a participant in a live meeting. The participantId is required to identify
        the meeting and the participant.
        Notes:

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param muted: The value is true or false, and means to mute or unmute the audio of a participant.
        :type muted: bool
        :param admit: The value can be true or false. The value of true is to admit a participant to the meeting if the
            participant is in the lobby, No-Op if the participant is not in the lobby or when the value is set to
            false.
        :type admit: bool
        :param expel: The attribute is exclusive and its value can be true or false. The value of true means that the
            participant will be expelled from the meeting, the value of false means No-Op.
        :type expel: bool
        """
        body = UpdateParticipantBody()
        if muted is not None:
            body.muted = muted
        if admit is not None:
            body.admit = admit
        if expel is not None:
            body.expel = expel
        url = self.ep(f'{participant_id}')
        data = super().put(url=url, data=body.json())
        return UpdateParticipantResponse.parse_obj(data)

    def admit_participants(self, participant_ids: List[str] = None):
        """
        To admit participants into a live meeting in bulk.
        This API limits the maximum size of items in the request body to 100.
        Each participantId of items in the request body should have the same prefix of meetingId.

        :param participant_ids: The ID that identifies the meeting participant.
        :type participant_ids: List[str]
        """
        body = AdmitParticipantsBody()
        if participant_ids is not None:
            body.items = participant_ids
        url = self.ep('admit')
        super().post(url=url, data=body.json())
        return
