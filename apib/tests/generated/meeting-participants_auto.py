from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AdmitParticipantsObject', 'Device', 'DeviceAudioType', 'DeviceCallType', 'InProgressDevice', 'InProgressParticipant', 'InProgressParticipantState', 'ListMeetingParticipantsResponse', 'Participant', 'ParticipantID', 'ParticipantState', 'ParticipantVideo']


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
    #: The time the device joined the meeting. If the field is non-existent or shows `1970-01-    01T00:00:00.000Z` the meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need real-time joined     events, please refer to the webhooks guide.
    #: example: 2019-04-23T17:31:00.000Z
    joined_time: Optional[datetime] = None
    #: The time the device left the meeting, `leftTime` is the exact moment when a specific devi    ce left the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the `leftTime` will     be filled in after the meeting ended. If you need real-time left events, please refer to the webhooks guide.
    #: example: 2019-04-23T17:32:00.000Z
    left_time: Optional[datetime] = None
    #: The duration in seconds the device stayed in the meeting.
    #: example: 60.0
    duration_second: Optional[int] = None
    #: The PSTN call type in which the device joined the meeting.
    #: example: callIn
    call_type: Optional[DeviceCallType] = None
    #: The PSTN phone number from which the device joined the meeting. Only [compliance officer](/docs/compliance#compliance) can retrieve the `phoneNumber`. The meeting host and admin users cannot retrieve it. NOTE: The `phoneNumber` will be returned after the meeting ends; it is not returned while the meeting is in progress.
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
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated with a Webex space.
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
    #: The status of the participant in the meeting. The value of `state` is `breakoutSession` which is only returned when the meeting is in progress and the breakout session is enabled.
    #: example: lobby
    state: Optional[ParticipantState] = None
    #: The ID of the breakout session including the participant.
    #: example: 2e373567-465b-8530-a18a-7025e1871d40
    breakout_session_id: Optional[str] = None
    #: The time the participant joined the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need real-time join events, please refer to the webhooks guide.
    #: example: 2022-10-25T09:00:00Z
    joined_time: Optional[datetime] = None
    #: The time the participant left the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the `leftTime` will be filled in after the meeting ended. If you need real-time left events, please refer to the webhooks guide.
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
    #: The source ID of the participant. The `sourceId` is from the [Create Invitation Sources](/docs/api/v1/meetings/create-invitation-sources) API.
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
    #: The time the device joined the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the `joinedTime` will be filled in after the meeting ended. If you need real-time joined events, please refer to the webhooks guide.
    #: example: 2019-04-23T17:31:00.000Z
    joined_time: Optional[datetime] = None
    #: The time the device left the meeting, `leftTime` is the exact moment when a specific device left the meeting. If the field is non-existent or shows `1970-01-01T00:00:00.000Z` the meeting may be still ongoing and the `leftTime` will be filled in after the meeting ended. If you need real-time left events, please refer to the webhooks guide.
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
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated with a Webex space.
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


class ParticipantID(ApiModel):
    #: The ID that identifies the meeting participant.
    #: example: 560d7b784f5143e3be2fc3064a5c4999_I_204252993233618782_23e16d67-17f3-3ef1-b830-f33d17c0232e
    participant_id: Optional[str] = None


class AdmitParticipantsObject(ApiModel):
    items: Optional[list[ParticipantID]] = None


class ListMeetingParticipantsResponse(ApiModel):
    items: Optional[list[Participant]] = None
