from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetMeetingConfigurationCommonSettingObject', 'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions', 'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone', 'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport', 'GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions', 'GetMeetingConfigurationCommonSettingObjectSecurityOptions', 'GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria', 'GetMeetingConfigurationCommonSettingObjectSiteOptions', 'GetMeetingConfigurationCommonSettingObjectTelephonyConfig', 'UpdateMeetingConfigurationCommonSettingObject']


class GetMeetingConfigurationCommonSettingObjectSiteOptions(ApiModel):
    #: Allow hosts to change their Personal Room URLs.
    allowCustomPersonalRoomURL: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectTelephonyConfig(ApiModel):
    #: Whether call-in teleconferencing for sessions was enabled.
    allowCallIn: Optional[bool] = None
    #: Whether call-back teleconferencing for sessions was enabled.
    allowCallBack: Optional[bool] = None
    #: Whether other teleconferencing for sessions was enabled.
    allowOtherTeleconf: Optional[bool] = None
    #: Whether toll-free call-in teleconferencing was enabled.
    allowTollFreeCallin: Optional[bool] = None
    #: Whether international call-in teleconferencing was enabled.
    allowInternationalCallin: Optional[bool] = None
    #: Whether international call-back teleconferencing was enabled.
    allowInternationalCallback: Optional[bool] = None
    #: Whether Voice Over IP functionality using the attendee computer's speakers and microphones was enabled.
    VoIP: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone(str, Enum):
    #: No tone.
    notone = 'NoTone'
    #: Beep.
    beep = 'Beep'
    #: Announce name.
    announcename = 'AnnounceName'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport(str, Enum):
    #: None.
    none_ = 'None'
    #: Webex teleconferencing.
    webexteleconferencing = 'WebexTeleconferencing'
    #: Other Teleconferencing.
    other = 'Other'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions(ApiModel):
    #: Determines if a sound is made when someone enters or exits.
    #: example: Beep
    entryAndExitTone: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone] = None
    #: Specifies whether or not joining teleconference without pressing 1 is checked by default.
    joinTeleconfNotPress1: Optional[bool] = None
    #: Specifies the type of teleconference support for meetings.
    #: example: WebexTeleconferencing
    telephonySupport: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport] = None
    #: Specifies whether toll-free call-in is available.
    tollFree: Optional[bool] = None
    #: Denotes if VoIP protocols are being used.
    VoIP: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions(ApiModel):
    #: Determines if email reminders are to be sent out.
    emailReminders: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria(ApiModel):
    #: Determines if a password requires mixed case.
    mixedCase: Optional[bool] = None
    #: Sets the minimum password length.
    #: example: 8.0
    minLength: Optional[int] = None
    #: Sets the minimum number of numeric characters in the password.
    #: example: 2.0
    minNumeric: Optional[int] = None
    #: Sets the minimum number of alphabetical characters in the password.
    #: example: 4.0
    minAlpha: Optional[int] = None
    #: Sets the minimum number of special characters in the password.
    #: example: 1.0
    minSpecial: Optional[int] = None
    #: Do not allow dynamic web page text for meeting passwords (like site name, host's name, username, meeting topic).
    disallowDynamicWebText: Optional[bool] = None
    #: Specifies if passwords from the `disallowValues` list are to be allowed.
    disallowList: Optional[bool] = None
    #: Sets password values that are not allowed.
    disallowValues: Optional[list[str]] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptions(ApiModel):
    #: Allow attendees or panelists to join before the host.
    joinBeforeHost: Optional[bool] = None
    #: Allows attendees or panelists to join the teleconference before the host.
    audioBeforeHost: Optional[bool] = None
    #: Allows first attendee or panelist as the presenter.
    firstAttendeeAsPresenter: Optional[bool] = None
    #: Specifies that all meetings must be unlisted.
    unlistAllMeetings: Optional[bool] = None
    #: Determines if a user must login before getting site access.
    requireLoginBeforeAccess: Optional[bool] = None
    #: Allow screen capture (Android devices only).
    allowMobileScreenCapture: Optional[bool] = None
    #: Determines if strict passwords are required for meetings.
    requireStrongPassword: Optional[bool] = None
    #: Criteria of a strong password.
    passwordCriteria: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria] = None


class GetMeetingConfigurationCommonSettingObject(ApiModel):
    #: Site Options on Webex Administration.
    siteOptions: Optional[GetMeetingConfigurationCommonSettingObjectSiteOptions] = None
    #: Telephony Configuration on WebEx Super Admin (These options are read-only, unable to update by Update Common Settings API).
    telephonyConfig: Optional[GetMeetingConfigurationCommonSettingObjectTelephonyConfig] = None
    #: Default Scheduler Options on Webex Administration (These options are applied to the site as defaults, but individual users can change them).
    defaultSchedulerOptions: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions] = None
    #: Schedule Meeting Options on Webex Administration.
    scheduleMeetingOptions: Optional[GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions] = None
    #: Security Options on Webex Administration.
    securityOptions: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptions] = None


class UpdateMeetingConfigurationCommonSettingObject(ApiModel):
    #: Site Options on Webex Administration.
    siteOptions: Optional[GetMeetingConfigurationCommonSettingObjectSiteOptions] = None
    #: Default Scheduler Options on Webex Administration (These options are applied to the site as defaults, but individual users can change them).
    defaultSchedulerOptions: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions] = None
    #: Schedule Meeting Options on Webex Administration.
    scheduleMeetingOptions: Optional[GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions] = None
    #: Security Options on Webex Administration.
    securityOptions: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptions] = None
