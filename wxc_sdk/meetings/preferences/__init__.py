"""
Meetings preferences API
"""

from typing import Optional

from pydantic import parse_obj_as

from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum
from ...common import LinkRelation

__all__ = ['Audio', 'CallInNumber', 'CoHost', 'DefaultAudioType', 'MeetingPreferenceDetails',
           'PersonalMeetingRoomOptions', 'VideoOptions',
           'MeetingPreferencesApi', 'OfficeNumber', 'PersonalMeetingRoom', 'SchedulingOptions', 'MeetingsSite',
           'Telephony', 'UpdatePersonalMeetingRoomOptionsBody', 'Video', 'VideoDevice', 'UpdateDefaultSiteBody']


class CoHost(ApiModel):
    #: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room Options API.
    #: Possible values: john.andersen@example.com
    email: Optional[str]
    #: Display name for cohost. This attribute can be modified with the Update Personal Meeting Room Options API.
    #: Possible values: John Andersen
    display_name: Optional[str]


class CallInNumber(ApiModel):
    #: Label for call-in number.
    #: Possible values: Call-in toll-free number (US/Canada)
    label: Optional[str]
    #: Call-in number to join teleconference from a phone.
    #: Possible values: 123456789
    call_in_number: Optional[str]
    #: Type of toll for the call-in number.
    #: Possible values: toll, tollFree
    toll_type: Optional[str]


class Telephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumber]]
    #: HATEOAS information of global call-in numbers for joining teleconference from a phone.
    links: Optional[list[LinkRelation]]


class PersonalMeetingRoom(ApiModel):
    #: Personal Meeting Room topic. The length of topic must be between 1 and 128 characters. This attribute can be
    #: modified with the Update Personal Meeting Room Options API.
    topic: Optional[str]
    #: PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot
    #: contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The
    #: predefined length for host PIN can be viewed in user's My Personal Room page. This attribute can be modified
    #: with the Update Personal Meeting Room Options API.
    host_pin: Optional[str]
    #: PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot
    #: contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The
    #: predefined length for host PIN can be viewed in user's My Personal Room page. This attribute can be modified
    #: with the Update Personal Meeting Room Options API.
    host_pin: Optional[str]
    #: Personal Meeting Room link. It cannot be empty. Note: This is a read-only attribute.
    personal_meeting_room_link: Optional[str]
    #: Option to automatically lock the Personal Room a number of minutes after a meeting starts. When a room is
    #: locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked is
    #: defined by autoLockMinutes. This attribute can be modified with the Update Personal Meeting Room Options API.
    enabled_auto_lock: Optional[bool]
    #: Number of minutes after which the Personal Room is locked if enabledAutoLock is enabled. Valid options are 0, 5,
    #: 10, 15 and 20. This attribute can be modified with the Update Personal Meeting Room Options API.
    auto_lock_minutes: Optional[int]
    #: Flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby while the
    #: owner is not in the room. This attribute can be modified with the Update Personal Meeting Room Options API.
    enabled_notify_host: Optional[bool]
    #: Flag allowing other invitees to host a meeting in the Personal Room without the owner. This attribute can be
    #: modified with the Update Personal Meeting Room Options API.
    support_co_host: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: Personal Room. The target site is user's preferred site. This attribute can be modified with the Update Personal
    #: Meeting Room Options API.
    support_anyone_as_co_host: Optional[bool]
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when
    #: joining the Personal Room. The target site is user's preferred site. This attribute can be modified with the
    #: Update Personal Meeting Room Options API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting
    #: without a prompt. This attribute can be modified with the Update Personal Meeting Room Options API.
    allow_authenticated_devices: Optional[bool]
    #: Array defining cohosts for the room if both supportAnyoneAsCoHost and allowFirstUserToBeCoHost are false This
    #: attribute can be modified with the Update Personal Meeting Room Options API.
    co_hosts: Optional[list[CoHost]]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Information for callbacks from meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]


class DefaultAudioType(str, Enum):
    #: Webex audio. This supports telephony and VoIP.
    webex_audio = 'webexAudio'
    #: Support only VoIP.
    voip_only = 'voipOnly'
    #: Other teleconference service. Details are defined in the otherTeleconferenceDescription parameter.
    other_teleconference_service = 'otherTeleconferenceService'
    #: No audio.
    none = 'none'


class OfficeNumber(ApiModel):
    #: Country code for the phone number. This attribute can be modified with the with the Update Audio Options API.
    country_code: Optional[str]
    #: Phone number. It cannot be longer than 30 characters. This attribute can be modified with the with the Update
    #: Audio Options API.
    number: Optional[str]
    #: Flag identifying the phone number as the one that will be used to dial into a teleconference. This attribute can
    #: be modified with the with the Update Audio Options API.
    enabled_call_in_authentication: Optional[bool]
    #: Flag to enable/disable Call Me number display on the meeting client. This attribute can be modified with the
    #: with the Update Audio Options API. Note: This feature is only effective if the site supports the Call Me
    #: feature.
    enabled_call_me: Optional[bool]


class Audio(ApiModel):
    #: Default audio type. This attribute can be modified with the with the Update Audio Options API.
    default_audio_type: Optional[DefaultAudioType]
    #: Phone number and other information for the teleconference provider to be used, along with instructions for
    #: invitees. This attribute can be modified with the with the Update Audio Options API.
    other_teleconference_description: Optional[str]
    #: Flag to enable/disable global call ins. Note: If the site does not support global call-ins, you cannot set this
    #: option. This attribute can be modified with the with the Update Audio Options API.
    enabled_global_call_in: Optional[bool]
    #: Flag to enable/disable call-ins from toll-free numbers. Note: If the site does not support calls from toll-free
    #: numbers, you cannot set this option. This attribute can be modified with the with the Update Audio Options API.
    enabled_toll_free: Optional[bool]
    #: Flag to enable/disable automatically connecting to audio using a computer. The meeting host can enable/disable
    #: this option. When this option is set to true, the user is automatically connected to audio via a computer when
    #: they start or join a Webex Meetings meeting on a desktop. This attribute can be modified with the
    #: Update Audio Options API.
    enabled_auto_connection: Optional[bool]
    #: PIN to provide a secondary level of authentication for calls where the host is using the phone and may need to
    #: invite additional invitees. It must be exactly 4 digits. It cannot contain sequential digits, such as 1234 or
    #: 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with the with the Update Audio
    #: Options API.
    audio_pin: Optional[str]
    #: Office phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This
    #: attribute can be modified with the with the Update Audio Options API.
    office_number: Optional[OfficeNumber]
    #: Mobile phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This
    #: attribute can be modified with the with the Update Audio Options API.
    mobile_number: Optional[OfficeNumber]


class VideoDevice(ApiModel):
    #: Video system name. It cannot be empty. This attribute can be modified with the Update Video Options API.
    #: Possible values: device1
    device_name: Optional[str]
    #: Video address. It cannot be empty and must be in valid email format. This attribute can be modified with the
    #: Update Video Options API.
    #: Possible values: device1@example.com
    device_address: Optional[str]
    #: Flag identifying the device as the default video device. If user's video device list is not empty, one and only
    #: one device must be set as default. This attribute can be modified with the Update Video Options API.
    #: Possible values:
    is_default: Optional[bool]


class Video(ApiModel):
    #: Array of video devices. This attribute can be modified with the Update Video Options API.
    video_devices: Optional[list[VideoDevice]]


class SchedulingOptions(ApiModel):
    #: Flag to enable/disable Join Before Host. The period during which invitees can join before the start time is
    #: defined by autoLockMinutes. This attribute can be modified with the Update Scheduling Options API. Note: This
    #: feature is only effective if the site supports the Join Before Host feature. This attribute can be modified with
    #: the Update Scheduling Options API.
    enabled_join_before_host: Optional[bool]
    #: Number of minutes before the start time that an invitee can join a meeting if enabledJoinBeforeHost is true.
    #: Valid options are 0, 5, 10 and 15. This attribute can be modified with the Update Scheduling Options API.
    join_before_host_minutes: Optional[int]
    #: Flag to enable/disable the automatic sharing of the meeting recording with invitees when it is available. This
    #: attribute can be modified with the Update Scheduling Options API.
    enabled_auto_share_recording: Optional[bool]
    #: Flag to automatically enable Webex Assistant whenever you start a meeting. This attribute can be modified with
    #: the Update Scheduling Options API.
    enabled_webex_assistant_by_default: Optional[bool]


class MeetingsSite(ApiModel):
    #: Access URL for the site. Note: This is a read-only attribute. The value can be assigned as user's default site
    #: with the Update Default Site API.
    #: Possible values: site1-example.webex.com
    site_url: Optional[str]
    #: Flag identifying the site as the default site. Users can list meetings and recordings, and create meetings on
    #: the default site.
    #: Possible values:
    default: Optional[bool]


class UpdatePersonalMeetingRoomOptionsBody(ApiModel):
    #: Personal Meeting Room topic to be updated.
    topic: Optional[str]
    #: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It
    #: cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as
    #: 1111. The predefined length for host PIN can be viewed in user's My Personal Room page and it can only be
    #: changed by site administrator.
    host_pin: Optional[str]
    #: Update for option to automatically lock the Personal Room a number of minutes after a meeting starts. When a
    #: room is locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked
    #: is defined by autoLockMinutes.
    enabled_auto_lock: Optional[bool]
    #: Updated number of minutes after which the Personal Room is locked if enabledAutoLock is enabled. Valid options
    #: are 0, 5, 10, 15 and 20.
    auto_lock_minutes: Optional[int]
    #: Update for flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby
    #: while the owner is not in the room.
    enabled_notify_host: Optional[bool]
    #: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room without the owner.
    support_co_host: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: Personal Room. The target site is user's preferred site.
    support_anyone_as_co_host: Optional[bool]
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when
    #: joining the Personal Room. The target site is user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting
    #: without a prompt.
    allow_authenticated_devices: Optional[bool]
    #: Updated array defining cohosts for the room if both supportAnyoneAsCoHost and allowFirstUserToBeCoHost are false
    co_hosts: Optional[list[CoHost]]


class PersonalMeetingRoomOptions(UpdatePersonalMeetingRoomOptionsBody):
    #: Personal Meeting Room link. It cannot be empty. Note: This is a read-only attribute.
    personal_meeting_room_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Information for callbacks from meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]


class MeetingPreferenceDetails(ApiModel):
    #: Personal Meeting Room options.
    personal_meeting_room: Optional[PersonalMeetingRoom]
    #: Audio Preferences. Note: These audio settings do not apply to Personal Room meetings
    audio: Optional[Audio]
    #: Information for video conferencing systems used to connect to Webex meetings. Note: The Call My Video System
    #: feature is available only if it has been purchased for your site and your administrator has enabled it.
    video: Optional[Video]
    #: Meeting scheduling options.
    scheduling_options: Optional[SchedulingOptions]
    #: List of user's Webex meeting sites including default site.
    sites: Optional[list[MeetingsSite]]


class VideoOptions(ApiModel):
    #: Array of video devices. This attribute can be modified with the Update Video Options API.
    video_devices: Optional[list[VideoDevice]]


class UpdateDefaultSiteBody(ApiModel):
    #: Access URL for the site.
    site_url: Optional[str]


class MeetingPreferencesApi(ApiChild, base='meetingPreferences'):
    """
    This API manages a user's meeting preferences, including Personal Meeting Room settings, video and audio settings,
    meeting scheduling options, and site settings.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def details(self, user_email: str = None, site_url: str = None) -> MeetingPreferenceDetails:
        """
        Retrieves meeting preferences for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the required admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details of the meeting preferences for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
        data = super().get(url=url, params=params)
        return MeetingPreferenceDetails.parse_obj(data)

    def personal_meeting_room_options(self, user_email: str = None, site_url: str = None) -> PersonalMeetingRoomOptions:
        """
        Retrieves the Personal Meeting Room options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('personalMeetingRoom')
        data = super().get(url=url, params=params)
        return PersonalMeetingRoomOptions.parse_obj(data)

    def update_personal_meeting_room_options(self, topic: str, host_pin: str, enabled_auto_lock: bool,
                                             auto_lock_minutes: int, enabled_notify_host: bool, support_co_host: bool,
                                             co_hosts: CoHost, user_email: str = None, site_url: str = None,
                                             support_anyone_as_co_host: bool = None,
                                             allow_first_user_to_be_co_host: bool = None,
                                             allow_authenticated_devices: bool = None) -> PersonalMeetingRoomOptions:
        """
        Update a single meeting

        :param topic: Personal Meeting Room topic to be updated.
        :type topic: str
        :param host_pin: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length,
            e.g. 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the
            predefined length, such as 1111. The predefined length for host PIN can be viewed in user's My Personal
            Room page and it can only be changed by site administrator.
        :type host_pin: str
        :param enabled_auto_lock: Update for option to automatically lock the Personal Room a number of minutes after a
            meeting starts. When a room is locked, invitees cannot enter until the owner admits them. The period after
            which the meeting is locked is defined by autoLockMinutes.
        :type enabled_auto_lock: bool
        :param auto_lock_minutes: Updated number of minutes after which the Personal Room is locked if enabledAutoLock
            is enabled. Valid options are 0, 5, 10, 15 and 20.
        :type auto_lock_minutes: int
        :param enabled_notify_host: Update for flag to enable notifying the owner of a Personal Room when someone
            enters the Personal Room lobby while the owner is not in the room.
        :type enabled_notify_host: bool
        :param support_co_host: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room
            without the owner.
        :type support_co_host: bool
        :param co_hosts: Updated array defining cohosts for the room if both supportAnyoneAsCoHost and
            allowFirstUserToBeCoHost are false
        :type co_hosts: CoHost
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param support_anyone_as_co_host: Whether or not to allow any attendee with a host account on the target site
            to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type support_anyone_as_co_host: bool
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee with a host account on the
            target site to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the user's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = UpdatePersonalMeetingRoomOptionsBody()
        if topic is not None:
            body.topic = topic
        if host_pin is not None:
            body.host_pin = host_pin
        if enabled_auto_lock is not None:
            body.enabled_auto_lock = enabled_auto_lock
        if auto_lock_minutes is not None:
            body.auto_lock_minutes = auto_lock_minutes
        if enabled_notify_host is not None:
            body.enabled_notify_host = enabled_notify_host
        if support_co_host is not None:
            body.support_co_host = support_co_host
        if co_hosts is not None:
            body.co_hosts = co_hosts
        if support_anyone_as_co_host is not None:
            body.support_anyone_as_co_host = support_anyone_as_co_host
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        url = self.ep('personalMeetingRoom')
        data = super().put(url=url, params=params, data=body.json())
        return PersonalMeetingRoomOptions.parse_obj(data)

    def audio_options(self, user_email: str = None, site_url: str = None) -> Audio:
        """
        Retrieves audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('audio')
        data = super().get(url=url, params=params)
        return Audio.parse_obj(data)

    def update_audio_options(self, user_email: str = None, site_url: str = None,
                             default_audio_type: DefaultAudioType = None, other_teleconference_description: str = None,
                             enabled_global_call_in: bool = None, enabled_toll_free: bool = None,
                             enabled_auto_connection: bool = None, audio_pin: str = None,
                             office_number: OfficeNumber = None, mobile_number: OfficeNumber = None) -> Audio:
        """
        Updates audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved
            from /meetingPreferences/sites.
        :type site_url: str
        :param default_audio_type: Default audio type. This attribute can be modified with the with the Update Audio
            Options API.
        :type default_audio_type: DefaultAudioType
        :param other_teleconference_description: Phone number and other information for the teleconference provider to
            be used, along with instructions for invitees. This attribute can be modified with the with the Update
            Audio Options API.
        :type other_teleconference_description: str
        :param enabled_global_call_in: Flag to enable/disable global call ins. Note: If the site does not support
            global call-ins, you cannot set this option. This attribute can be modified with the with the Update Audio
            Options API.
        :type enabled_global_call_in: bool
        :param enabled_toll_free: Flag to enable/disable call-ins from toll-free numbers. Note: If the site does not
            support calls from toll-free numbers, you cannot set this option. This attribute can be modified with the
            with the Update Audio Options API.
        :type enabled_toll_free: bool
        :param enabled_auto_connection: Flag to enable/disable automatically connecting to audio using a computer. The
            meeting host can enable/disable this option. When this option is set to true, the user is automatically
            connected to audio via a computer when they start or join a Webex Meetings meeting on a desktop. This
            attribute can be modified with the Update Audio Options API.
        :type enabled_auto_connection: bool
        :param audio_pin: PIN to provide a secondary level of authentication for calls where the host is using the
            phone and may need to invite additional invitees. It must be exactly 4 digits. It cannot contain sequential
            digits, such as 1234 or 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with
            the with the Update Audio Options API.
        :type audio_pin: str
        :param office_number: Office phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type office_number: OfficeNumber
        :param mobile_number: Mobile phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type mobile_number: OfficeNumber
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = Audio()
        if default_audio_type is not None:
            body.default_audio_type = default_audio_type
        if other_teleconference_description is not None:
            body.other_teleconference_description = other_teleconference_description
        if enabled_global_call_in is not None:
            body.enabled_global_call_in = enabled_global_call_in
        if enabled_toll_free is not None:
            body.enabled_toll_free = enabled_toll_free
        if enabled_auto_connection is not None:
            body.enabled_auto_connection = enabled_auto_connection
        if audio_pin is not None:
            body.audio_pin = audio_pin
        if office_number is not None:
            body.office_number = office_number
        if mobile_number is not None:
            body.mobile_number = mobile_number
        url = self.ep('audio')
        data = super().put(url=url, params=params, data=body.json())
        return Audio.parse_obj(data)

    def video_options(self, user_email: str = None, site_url: str = None) -> list[VideoDevice]:
        """
        Retrieves video options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved using Get Site List.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('video')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[VideoDevice], data["videoDevices"])

    def update_video_options(self, video_devices: VideoDevice, user_email: str = None,
                             site_url: str = None) -> list[VideoDevice]:
        """
        Updates video options for the authenticated user.

        :param video_devices: Array of video devices. If the array is not empty, one device and no more than one
            devices must be set as default device.
        :type video_devices: VideoDevice
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = VideoOptions()
        if video_devices is not None:
            body.video_devices = video_devices
        url = self.ep('video')
        data = super().put(url=url, params=params, data=body.json())
        return parse_obj_as(list[VideoDevice], data["videoDevices"])

    def scheduling_options(self, user_email: str = None, site_url: str = None) -> SchedulingOptions:
        """
        Retrieves scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('schedulingOptions')
        data = super().get(url=url, params=params)
        return SchedulingOptions.parse_obj(data)

    def update_scheduling_options(self, user_email: str = None, site_url: str = None,
                                  enabled_join_before_host: bool = None, join_before_host_minutes: int = None,
                                  enabled_auto_share_recording: bool = None,
                                  enabled_webex_assistant_by_default: bool = None) -> SchedulingOptions:
        """
        Updates scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param enabled_join_before_host: Flag to enable/disable Join Before Host. The period during which invitees can
            join before the start time is defined by autoLockMinutes. This attribute can be modified with the Update
            Scheduling Options API. Note: This feature is only effective if the site supports the Join Before Host
            feature. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_join_before_host: bool
        :param join_before_host_minutes: Number of minutes before the start time that an invitee can join a meeting if
            enabledJoinBeforeHost is true. Valid options are 0, 5, 10 and 15. This attribute can be modified with the
            Update Scheduling Options API.
        :type join_before_host_minutes: int
        :param enabled_auto_share_recording: Flag to enable/disable the automatic sharing of the meeting recording with
            invitees when it is available. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_auto_share_recording: bool
        :param enabled_webex_assistant_by_default: Flag to automatically enable Webex Assistant whenever you start a
            meeting. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_webex_assistant_by_default: bool
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = SchedulingOptions()
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if enabled_auto_share_recording is not None:
            body.enabled_auto_share_recording = enabled_auto_share_recording
        if enabled_webex_assistant_by_default is not None:
            body.enabled_webex_assistant_by_default = enabled_webex_assistant_by_default
        url = self.ep('schedulingOptions')
        data = super().put(url=url, params=params, data=body.json())
        return SchedulingOptions.parse_obj(data)

    def site_list(self, user_email: str = None) -> list[MeetingsSite]:
        """
        Retrieves the list of Webex sites that the authenticated user is set up to use.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user and the API will
            return the list of Webex sites for that user.
        :type user_email: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        url = self.ep('sites')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[MeetingsSite], data["sites"])

    def update_default_site(self, default_site: bool, site_url: str, user_email: str = None) -> MeetingsSite:
        """
        Updates the default site for the authenticated user.

        :param default_site: Whether or not to change user's default site. Note: defaultSite should be set to true for
            the user's single default site
        :type default_site: bool
        :param site_url: Access URL for the site.
        :type site_url: str
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update default site for that user.
        :type user_email: str
        """
        params = {}
        params['defaultSite'] = str(default_site).lower()
        if user_email is not None:
            params['userEmail'] = user_email
        body = UpdateDefaultSiteBody()
        if site_url is not None:
            body.site_url = site_url
        url = self.ep('sites')
        data = super().put(url=url, params=params, data=body.json())
        return MeetingsSite.parse_obj(data)
