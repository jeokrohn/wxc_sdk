from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetMeetingConfigurationCommonSettingObject',
            'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions',
            'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone',
            'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport',
            'GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions',
            'GetMeetingConfigurationCommonSettingObjectSecurityOptions',
            'GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria',
            'GetMeetingConfigurationCommonSettingObjectSiteOptions',
            'GetMeetingConfigurationCommonSettingObjectTelephonyConfig',
            'UpdateMeetingConfigurationCommonSettingObject']


class GetMeetingConfigurationCommonSettingObjectSiteOptions(ApiModel):
    #: Allow hosts to change their Personal Room URLs.
    allow_custom_personal_room_url: Optional[bool] = Field(alias='allowCustomPersonalRoomURL', default=None)


class GetMeetingConfigurationCommonSettingObjectTelephonyConfig(ApiModel):
    #: Whether call-in teleconferencing for sessions was enabled.
    allow_call_in: Optional[bool] = None
    #: Whether call-back teleconferencing for sessions was enabled.
    allow_call_back: Optional[bool] = None
    #: Whether other teleconferencing for sessions was enabled.
    allow_other_teleconf: Optional[bool] = None
    #: Whether toll-free call-in teleconferencing was enabled.
    allow_toll_free_callin: Optional[bool] = None
    #: Whether international call-in teleconferencing was enabled.
    allow_international_callin: Optional[bool] = None
    #: Whether international call-back teleconferencing was enabled.
    allow_international_callback: Optional[bool] = None
    #: Whether Voice Over IP functionality using the attendee computer's speakers and microphones was enabled.
    vo_ip: Optional[bool] = Field(alias='VoIP', default=None)


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone(str, Enum):
    #: No tone.
    no_tone = 'NoTone'
    #: Beep.
    beep = 'Beep'
    #: Announce name.
    announce_name = 'AnnounceName'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport(str, Enum):
    #: None.
    none_ = 'None'
    #: Webex teleconferencing.
    webex_teleconferencing = 'WebexTeleconferencing'
    #: Other Teleconferencing.
    other = 'Other'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions(ApiModel):
    #: Determines if a sound is made when someone enters or exits.
    #: example: Beep
    entry_and_exit_tone: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone] = None
    #: Specifies whether or not joining teleconference without pressing 1 is checked by default.
    join_teleconf_not_press1: Optional[bool] = None
    #: Specifies the type of teleconference support for meetings.
    #: example: WebexTeleconferencing
    telephony_support: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport] = None
    #: Specifies whether toll-free call-in is available.
    toll_free: Optional[bool] = None
    #: Denotes if VoIP protocols are being used.
    vo_ip: Optional[bool] = Field(alias='VoIP', default=None)


class GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions(ApiModel):
    #: Determines if email reminders are to be sent out.
    email_reminders: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria(ApiModel):
    #: Determines if a password requires mixed case.
    mixed_case: Optional[bool] = None
    #: Sets the minimum password length.
    #: example: 8.0
    min_length: Optional[int] = None
    #: Sets the minimum number of numeric characters in the password.
    #: example: 2.0
    min_numeric: Optional[int] = None
    #: Sets the minimum number of alphabetical characters in the password.
    #: example: 4.0
    min_alpha: Optional[int] = None
    #: Sets the minimum number of special characters in the password.
    #: example: 1.0
    min_special: Optional[int] = None
    #: Do not allow dynamic web page text for meeting passwords (like site name, host's name, username, meeting topic).
    disallow_dynamic_web_text: Optional[bool] = None
    #: Specifies if passwords from the `disallowValues` list are to be allowed.
    disallow_list: Optional[bool] = None
    #: Sets password values that are not allowed.
    disallow_values: Optional[list[str]] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptions(ApiModel):
    #: Allow attendees or panelists to join before the host.
    join_before_host: Optional[bool] = None
    #: Allows attendees or panelists to join the teleconference before the host.
    audio_before_host: Optional[bool] = None
    #: Allows first attendee or panelist as the presenter.
    first_attendee_as_presenter: Optional[bool] = None
    #: Specifies that all meetings must be unlisted.
    unlist_all_meetings: Optional[bool] = None
    #: Determines if a user must login before getting site access.
    require_login_before_access: Optional[bool] = None
    #: Allow screen capture (Android devices only).
    allow_mobile_screen_capture: Optional[bool] = None
    #: Determines if strict passwords are required for meetings.
    require_strong_password: Optional[bool] = None
    #: Criteria of a strong password.
    password_criteria: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria] = None


class GetMeetingConfigurationCommonSettingObject(ApiModel):
    #: Site Options on Webex Administration.
    site_options: Optional[GetMeetingConfigurationCommonSettingObjectSiteOptions] = None
    #: Telephony Configuration on WebEx Super Admin (These options are read-only, unable to update by Update Common
    #: Settings API).
    telephony_config: Optional[GetMeetingConfigurationCommonSettingObjectTelephonyConfig] = None
    #: Default Scheduler Options on Webex Administration (These options are applied to the site as defaults, but
    #: individual users can change them).
    default_scheduler_options: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions] = None
    #: Schedule Meeting Options on Webex Administration.
    schedule_meeting_options: Optional[GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions] = None
    #: Security Options on Webex Administration.
    security_options: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptions] = None


class UpdateMeetingConfigurationCommonSettingObject(ApiModel):
    #: Site Options on Webex Administration.
    site_options: Optional[GetMeetingConfigurationCommonSettingObjectSiteOptions] = None
    #: Default Scheduler Options on Webex Administration (These options are applied to the site as defaults, but
    #: individual users can change them).
    default_scheduler_options: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions] = None
    #: Schedule Meeting Options on Webex Administration.
    schedule_meeting_options: Optional[GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions] = None
    #: Security Options on Webex Administration.
    security_options: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptions] = None
