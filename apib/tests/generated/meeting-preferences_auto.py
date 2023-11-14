from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DefaultSiteObject', 'MeetingPreferenceObject', 'MeetingPreferenceObjectAudio', 'MeetingPreferenceObjectAudioDefaultAudioType', 'MeetingPreferenceObjectAudioOfficeNumber', 'MeetingPreferenceObjectPersonalMeetingRoom', 'MeetingPreferenceObjectPersonalMeetingRoomCoHosts', 'MeetingPreferenceObjectPersonalMeetingRoomTelephony', 'MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbers', 'MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbersTollType', 'MeetingPreferenceObjectPersonalMeetingRoomTelephonyLinks', 'MeetingPreferenceObjectSites', 'MeetingPreferenceObjectVideo', 'MeetingPreferenceObjectVideoVideoDevices', 'SchedulingOptionsObject', 'SitesObject', 'UpdatePMRObject']


class MeetingPreferenceObjectPersonalMeetingRoomCoHosts(ApiModel):
    #: Email address for cohost. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for cohost. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    #: example: John Andersen
    display_name: Optional[str] = None


class MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbersTollType(str, Enum):
    toll = 'toll'
    toll_free = 'tollFree'


class MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbers(ApiModel):
    #: Label for call-in number.
    #: example: Call-in toll-free number (US/Canada)
    label: Optional[str] = None
    #: Call-in number to join teleconference from a phone.
    #: example: 123456789
    call_in_number: Optional[str] = None
    #: Type of toll for the call-in number.
    #: example: tollFree
    toll_type: Optional[MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbersTollType] = None


class MeetingPreferenceObjectPersonalMeetingRoomTelephonyLinks(ApiModel):
    #: Link relation describing how the target resource is related to the current context (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: globalCallinNumbers
    rel: Optional[str] = None
    #: Target resource URI (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: /api/v1/meetings/2c87cf8ece4e414a9fe5516e4a0aac76/globalCallinNumbers
    href: Optional[str] = None
    #: Target resource method (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: GET
    method: Optional[str] = None


class MeetingPreferenceObjectPersonalMeetingRoomTelephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or the global call-in number, followed by the value of the `accessCode`.
    #: example: 1234567890
    access_code: Optional[str] = None
    #: Array of call-in numbers for joining teleconference from a phone.
    call_in_numbers: Optional[list[MeetingPreferenceObjectPersonalMeetingRoomTelephonyCallInNumbers]] = None
    #: [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) information of global call-in numbers for joining teleconference from a phone.
    links: Optional[MeetingPreferenceObjectPersonalMeetingRoomTelephonyLinks] = None


class MeetingPreferenceObjectPersonalMeetingRoom(ApiModel):
    #: Personal Meeting Room topic. The length of `topic` must be between 1 and 128 characters. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    #: example: John's PMR
    topic: Optional[str] = None
    #: PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The predefined length for host PIN can be viewed in user's `My Personal Room` page. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    #: example: 4325
    host_pin: Optional[datetime] = None
    #: Personal Meeting Room link. It cannot be empty. ***Note***: This is a read-only attribute.
    #: example: https://site4-example.webex.com/meet/john
    personal_meeting_room_link: Optional[str] = None
    #: Option to automatically lock the Personal Room a number of minutes after a meeting starts. When a room is locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked is defined by `autoLockMinutes`. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    enabled_auto_lock: Optional[bool] = None
    #: Number of minutes after which the Personal Room is locked if `enabledAutoLock` is enabled. Valid options are 0, 5, 10, 15 and 20. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    auto_lock_minutes: Optional[int] = None
    #: Flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby while the owner is not in the room. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    enabled_notify_host: Optional[bool] = None
    #: Flag allowing other invitees to host a meeting in the Personal Room without the owner. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    support_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the Personal Room. The target site is user's preferred site. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    support_anyone_as_co_host: Optional[bool] = None
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when joining the Personal Room. The target site is user's preferred site. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting without a prompt. This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    allow_authenticated_devices: Optional[bool] = None
    #: Array defining cohosts for the room if both `supportAnyoneAsCoHost` and `allowFirstUserToBeCoHost` are `false` This attribute can be modified with the [Update Personal Meeting Room Options](/docs/api/v1/meeting-preferences/update-personal-meeting-room-options) API.
    co_hosts: Optional[list[MeetingPreferenceObjectPersonalMeetingRoomCoHosts]] = None
    #: SIP address for callback from a video system.
    #: example: john.andersen@example.com
    sip_address: Optional[str] = None
    #: IP address for callback from a video system.
    #: example: 192.168.100.100
    dial_in_ip_address: Optional[str] = None
    #: Information for callbacks from meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingPreferenceObjectPersonalMeetingRoomTelephony] = None


class MeetingPreferenceObjectAudioDefaultAudioType(str, Enum):
    #: Webex audio. This supports telephony and VoIP.
    webex_audio = 'webexAudio'
    #: Support only VoIP.
    voip_only = 'voipOnly'
    #: Other teleconference service. Details are defined in the `otherTeleconferenceDescription` parameter.
    other_teleconference_service = 'otherTeleconferenceService'
    #: No audio.
    none_ = 'none'
    none_ = 'none'


class MeetingPreferenceObjectAudioOfficeNumber(ApiModel):
    #: Country code for the phone number. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    country_code: Optional[str] = None
    #: Phone number. It cannot be longer than 30 characters. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    number: Optional[str] = None
    #: Flag identifying the phone number as the one that will be used to dial into a teleconference. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    enabled_call_in_authentication: Optional[bool] = None
    #: Flag to enable/disable Call Me number display on the meeting client. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API. ***Note***: This feature is only effective if the site supports the ***Call Me*** feature.
    enabled_call_me: Optional[bool] = None


class MeetingPreferenceObjectAudio(ApiModel):
    #: Default audio type. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    default_audio_type: Optional[MeetingPreferenceObjectAudioDefaultAudioType] = None
    #: Phone number and other information for the teleconference provider to be used, along with instructions for invitees. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    other_teleconference_description: Optional[str] = None
    #: Flag to enable/disable global call ins. ***Note***: If the site does not support global call-ins, you cannot set this option. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    enabled_global_call_in: Optional[bool] = None
    #: Flag to enable/disable call-ins from toll-free numbers.  ***Note***: If the site does not support calls from toll-free numbers, you cannot set this option. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    enabled_toll_free: Optional[bool] = None
    #: Flag to enable/disable automatically connecting to audio using a computer. The meeting host can enable/disable this option. When this option is set to `true`, the user is automatically connected to audio via a computer when they start or join a Webex Meetings meeting on a desktop. `This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    enabled_auto_connection: Optional[bool] = None
    #: PIN to provide a secondary level of authentication for calls where the host is using the phone and may need to invite additional invitees. It must be exactly 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    audio_pin: Optional[str] = None
    #: Office phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    office_number: Optional[MeetingPreferenceObjectAudioOfficeNumber] = None
    #: Mobile phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This attribute can be modified with the with the [Update Audio Options](/docs/api/v1/meeting-preferences/update-audio-options) API.
    mobile_number: Optional[MeetingPreferenceObjectAudioOfficeNumber] = None


class MeetingPreferenceObjectVideoVideoDevices(ApiModel):
    #: Video system name. It cannot be empty. This attribute can be modified with the [Update Video Options](/docs/api/v1/meeting-preferences/update-video-options) API.
    #: example: device1
    device_name: Optional[str] = None
    #: Video address. It cannot be empty and must be in valid email format. This attribute can be modified with the [Update Video Options](/docs/api/v1/meeting-preferences/update-video-options) API.
    #: example: device1@example.com
    device_address: Optional[str] = None
    #: Flag identifying the device as the default video device. If user's video device list is not empty, one and only one device must be set as default. This attribute can be modified with the [Update Video Options](/docs/api/v1/meeting-preferences/update-video-options) API.
    #: example: True
    is_default: Optional[bool] = None


class MeetingPreferenceObjectVideo(ApiModel):
    #: Array of video devices. This attribute can be modified with the [Update Video Options](/docs/api/v1/meeting-preferences/update-video-options) API.
    video_devices: Optional[list[MeetingPreferenceObjectVideoVideoDevices]] = None


class MeetingPreferenceObjectSites(ApiModel):
    #: Access URL for the site. ***Note***: This is a read-only attribute. The value can be assigned as user's default site with the [Update Default Site](/docs/api/v1/meeting-preferences/update-default-site) API.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None
    #: Flag identifying the site as the default site. Users can list meetings and recordings, and create meetings on the default site.
    default: Optional[bool] = None


class SchedulingOptionsObject(ApiModel):
    #: Flag to enable/disable ***Join Before Host***. The period during which invitees can join before the start time is defined by `autoLockMinutes`. This attribute can be modified with the [Update Scheduling Options](/docs/api/v1/meeting-preferences/update-scheduling-options) API. ***Note***: This feature is only effective if the site supports the ***Join Before Host*** feature. This attribute can be modified with the [Update Scheduling Options](/docs/api/v1/meeting-preferences/update-scheduling-options) API.
    enabled_join_before_host: Optional[bool] = None
    #: Number of minutes before the start time that an invitee can join a meeting if `enabledJoinBeforeHost` is true. Valid options are 0, 5, 10 and 15. This attribute can be modified with the [Update Scheduling Options](/docs/api/v1/meeting-preferences/update-scheduling-options) API.
    join_before_host_minutes: Optional[int] = None
    #: Flag to enable/disable the automatic sharing of the meeting recording with invitees when it is available. This attribute can be modified with the [Update Scheduling Options](/docs/api/v1/meeting-preferences/update-scheduling-options) API.
    enabled_auto_share_recording: Optional[bool] = None
    #: Flag to automatically enable Webex Assistant whenever you start a meeting. This attribute can be modified with the [Update Scheduling Options](/docs/api/v1/meeting-preferences/update-scheduling-options) API.
    enabled_webex_assistant_by_default: Optional[bool] = None


class MeetingPreferenceObject(ApiModel):
    #: Personal Meeting Room options.
    personal_meeting_room: Optional[MeetingPreferenceObjectPersonalMeetingRoom] = None
    #: Audio Preferences. ***Note***: These audio settings do not apply to Personal Room meetings
    audio: Optional[MeetingPreferenceObjectAudio] = None
    #: Information for video conferencing systems used to connect to Webex meetings. ***Note***: The ***Call My Video System*** feature is available only if it has been purchased for your site and your administrator has enabled it.
    video: Optional[MeetingPreferenceObjectVideo] = None
    #: Meeting scheduling options.
    scheduling_options: Optional[SchedulingOptionsObject] = None
    #: List of user's Webex meeting sites including default site.
    sites: Optional[list[MeetingPreferenceObjectSites]] = None


class SitesObject(ApiModel):
    #: Array of sites for the user. Users can have one site or multiple sites. This concept is specific to Webex Meetings. Any `siteUrl` in the site list can be assigned as user's default site with the [Update Default Site](/docs/api/v1/meeting-preferences/update-default-site) API.
    sites: Optional[list[MeetingPreferenceObjectSites]] = None


class DefaultSiteObject(ApiModel):
    #: Access URL for the site.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None


class UpdatePMRObject(ApiModel):
    #: Personal Meeting Room topic to be updated.
    #: example: John's PMR
    topic: Optional[str] = None
    #: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The predefined length for host PIN can be viewed in user's `My Personal Room` page and it can only be changed by site administrator.
    #: example: 4325
    host_pin: Optional[datetime] = None
    #: Update for option to automatically lock the Personal Room a number of minutes after a meeting starts. When a room is locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked is defined by `autoLockMinutes`.
    enabled_auto_lock: Optional[bool] = None
    #: Updated number of minutes after which the Personal Room is locked if `enabledAutoLock` is enabled. Valid options are 0, 5, 10, 15 and 20.
    auto_lock_minutes: Optional[int] = None
    #: Update for flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby while the owner is not in the room.
    #: example: True
    enabled_notify_host: Optional[bool] = None
    #: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room without the owner.
    #: example: True
    support_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the Personal Room. The target site is user's preferred site.
    support_anyone_as_co_host: Optional[bool] = None
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when joining the Personal Room. The target site is user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting without a prompt.
    allow_authenticated_devices: Optional[bool] = None
    #: Updated array defining cohosts for the room if both `supportAnyoneAsCoHost` and `allowFirstUserToBeCoHost` are `false`
    co_hosts: Optional[list[MeetingPreferenceObjectPersonalMeetingRoomCoHosts]] = None