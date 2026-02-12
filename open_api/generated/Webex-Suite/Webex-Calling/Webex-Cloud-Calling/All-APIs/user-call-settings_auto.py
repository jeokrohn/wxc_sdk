from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ApplicationsSetting', 'BargeInInfo', 'CallForwardingInfo', 'CallForwardingInfoCallForwarding',
           'CallForwardingInfoCallForwardingAlways', 'CallForwardingInfoCallForwardingBusy',
           'CallForwardingInfoCallForwardingNoAnswer', 'CallForwardingPutCallForwarding',
           'CallForwardingPutCallForwardingNoAnswer', 'CallInterceptInfo', 'CallInterceptInfoIncoming',
           'CallInterceptInfoIncomingAnnouncements', 'CallInterceptInfoIncomingAnnouncementsGreeting',
           'CallInterceptInfoIncomingAnnouncementsNewNumber', 'CallInterceptInfoIncomingType',
           'CallInterceptInfoOutgoing', 'CallInterceptInfoOutgoingType', 'CallInterceptPutIncoming',
           'CallInterceptPutIncomingAnnouncements', 'CallRecordingInfo',
           'CallRecordingInfoCallRecordingAccessSettings', 'CallRecordingInfoNotification',
           'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord', 'CallRecordingInfoRepeat',
           'CallRecordingInfoStartStopAnnouncement', 'CallRecordingPutNotification',
           'CallRecordingPutNotificationType', 'CallWaitingInfo', 'CallerIdInfo',
           'CallerIdInfoExternalCallerIdNamePolicy', 'CallerIdInfoSelected', 'DirectLineCallerIdNameObject',
           'DoNotDisturbInfo', 'EventLongDetails', 'EventLongDetailsRecurrence',
           'EventLongDetailsRecurrenceRecurDaily', 'EventLongDetailsRecurrenceRecurWeekly',
           'GetCallingBehaviorObject', 'GetCallingBehaviorObjectBehaviorType',
           'GetCallingBehaviorObjectEffectiveBehaviorType', 'GetEvent', 'GetMonitoredElementsObject',
           'GetMonitoredElementsObjectCallparkextension', 'GetMonitoredElementsObjectMember', 'GetNumbers',
           'GetNumbersPhoneNumbersItem', 'GetNumbersPhoneNumbersItemRingPattern', 'IncomingPermissionSetting',
           'IncomingPermissionSettingExternalTransfer', 'MonitoredMemberObject', 'MonitoredNumberObject',
           'MonitoringSettings', 'OutgoingCallingPermissionsSettingGet',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsItem',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType',
           'OutgoingCallingPermissionsSettingPutCallingPermissionsItem', 'PeopleOrPlaceOrVirtualLineType',
           'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo', 'ReceptionInfo',
           'RetrieveExecutiveAssistantSettingsForAPersonResponseType', 'ScheduleLevel', 'ScheduleLongDetails',
           'ScheduleShortDetails', 'ScheduleType', 'UserCallSettings12Api', 'UserSelectionObject', 'VoicemailInfo',
           'VoicemailInfoEmailCopyOfMessage', 'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage',
           'VoicemailInfoMessageStorageStorageType', 'VoicemailInfoSendBusyCalls', 'VoicemailInfoSendUnansweredCalls',
           'VoicemailPutSendBusyCalls', 'VoicemailPutSendUnansweredCalls']


class ApplicationsSetting(ApiModel):
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool] = None
    #: If `true`, the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool] = None
    #: Device ID of WebRTC client. Returns only if `browserClientEnabled` is true.
    browser_client_id: Optional[str] = None
    #: If `true`, the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool] = None
    #: Device ID of Desktop client. Returns only if `desktopClientEnabled` is true.
    desktop_client_id: Optional[str] = None
    #: If `true`, the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool] = None
    #: If `true`, the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool] = None
    #: Number of available device licenses for assigning devices/apps.
    available_line_count: Optional[int] = None


class BargeInInfo(ApiModel):
    #: If `true`, the Barge In feature is enabled.
    enabled: Optional[bool] = None
    #: If `true`, a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    destination: Optional[str] = None
    #: The enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None
    #: Enabled or disabled state of sending incoming calls to destination number's voicemail if the destination is an
    #: internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person
    #: is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingInfoCallForwardingNoAnswer] = None


class CallForwardingInfo(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwardingInfoCallForwarding] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[CallForwardingInfoCallForwardingBusy] = None


class CallForwardingPutCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered. `numberOfRings` must be between 2 and 20,
    #: inclusive.
    number_of_rings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPutCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person
    #: is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingPutCallForwardingNoAnswer] = None


class CallInterceptInfoIncomingType(str, Enum):
    #: Incoming calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class CallInterceptInfoIncomingAnnouncementsGreeting(str, Enum):
    #: A custom greeting is played when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default greeting will be played when incoming calls are intercepted.
    default = 'DEFAULT'


class CallInterceptInfoIncomingAnnouncementsNewNumber(ApiModel):
    #: If `true`, the caller will hear this new number when the call is intercepted.
    enabled: Optional[bool] = None
    #: New number caller will hear announced.
    destination: Optional[str] = None


class CallInterceptInfoIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Filename of custom greeting; will be an empty string if no custom greeting has been uploaded.
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptInfoIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the person's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptInfoIncomingAnnouncements] = None


class CallInterceptInfoOutgoingType(str, Enum):
    #: Outgoing calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class CallInterceptInfoOutgoing(ApiModel):
    #: `INTERCEPT_ALL` indicated all outgoing calls are intercepted.
    type: Optional[CallInterceptInfoOutgoingType] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    destination: Optional[str] = None


class CallInterceptInfo(ApiModel):
    #: `true` if call intercept is enabled.
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[CallInterceptInfoIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[CallInterceptInfoOutgoing] = None


class CallInterceptPutIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptPutIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the person's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptPutIncomingAnnouncements] = None


class CallRecordingInfoRecord(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (`*44`) has been entered. Pause, resume, and stop
    #: controls are supported.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class CallRecordingInfoNotificationType(str, Enum):
    #: No notification sound played when call recording is paused or resumed.
    none_ = 'None'
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class CallRecordingInfoNotification(ApiModel):
    #: Type of pause/resume notification.
    type: Optional[CallRecordingInfoNotificationType] = None
    #: `true` when the notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class CallRecordingInfoRepeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    interval: Optional[int] = None
    #: `true` when ongoing call recording tone will be played at the designated interval. `false` indicates no warning
    #: tone will be played.
    enabled: Optional[bool] = None


class CallRecordingInfoStartStopAnnouncement(ApiModel):
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for internal calls.
    internal_calls_enabled: Optional[bool] = None
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for PSTN calls.
    pstn_calls_enabled: Optional[bool] = None


class CallRecordingInfoCallRecordingAccessSettings(ApiModel):
    #: When `true`, the person can view and play call recordings.
    view_and_play_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can download call recordings.
    download_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can delete call recordings.
    delete_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can share call recordings.
    share_recordings_enabled: Optional[bool] = None


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    enabled: Optional[bool] = None
    #: Call recording scenario.
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends.
    start_stop_announcement_enabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Name of the service provider providing call recording service.
    service_provider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    external_group: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    external_identifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[CallRecordingInfoStartStopAnnouncement] = None
    #: Settings related to call recording access.
    call_recording_access_settings: Optional[CallRecordingInfoCallRecordingAccessSettings] = None


class CallRecordingPutNotificationType(str, Enum):
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class CallRecordingPutNotification(ApiModel):
    #: Type of pause/resume notification. If `enabled` is `true` and `type` is not provided then `type` is set to
    #: `Beep` by default.
    type: Optional[CallRecordingPutNotificationType] = None
    #: `true` when notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class CallWaitingInfo(ApiModel):
    #: `true` if the Call Waiting feature is enabled.
    enabled: Optional[bool] = None


class CallerIdInfoSelected(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the value from the customNumber field.
    custom = 'CUSTOM'


class CallerIdInfoExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the external caller ID name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the `customExternalCallerIdName` field.
    other = 'OTHER'


class UserSelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this user.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `firstName` and `lastName` are to be shown for this user.
    first_name_last_name = 'FIRST_NAME_LAST_NAME'
    #: When this option is selected, `lastName` and `firstName` are to be shown for this user.
    last_name_first_name = 'LAST_NAME_FIRST_NAME'
    #: When this option is selected, `displayName` is to be shown for this user.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `FIRST_NAME_LAST_NAME`.
    selection: Optional[UserSelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class CallerIdInfo(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CallerIdInfoSelected]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    selected: Optional[CallerIdInfoSelected] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    direct_number: Optional[str] = None
    #: Extension number of the person.
    extension_number: Optional[str] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected.
    location_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: Custom number which will be shown if CUSTOM is selected. This value must be a number from the person's location
    #: or from another location with the same country, PSTN provider, and zone (only applicable for India locations)
    #: as the person's location.
    custom_number: Optional[str] = None
    #: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed. This
    #: field has been deprecated. Please use `directLineCallerIdName` and `dialByFirstName` instead.
    first_name: Optional[str] = None
    #: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed. This
    #: field has been deprecated. Please use `directLineCallerIdName` and `dialByLastName` instead.
    last_name: Optional[str] = None
    #: Block this person's identity when receiving a call.
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    external_caller_id_name_policy: Optional[CallerIdInfoExternalCallerIdNamePolicy] = None
    #: Custom external caller ID name which will be shown if external caller ID name policy is `OTHER`.
    custom_external_caller_id_name: Optional[str] = None
    #: Location's external caller ID name which will be shown if external caller ID name policy is `LOCATION`.
    location_external_caller_id_name: Optional[str] = None
    #: Flag to indicate the person's direct line number is available as an additional external caller ID for the
    #: person.
    additional_external_caller_id_direct_line_enabled: Optional[bool] = None
    #: Flag to indicate the location main number is available as an additional external caller ID for the person.
    additional_external_caller_id_location_number_enabled: Optional[bool] = None
    #: The custom number available as an additional external caller ID for the person. This value must be a number from
    #: the person's location or from another location with the same country, PSTN provider, and zone (only applicable
    #: for India locations) as the person's location.
    additional_external_caller_id_custom_number: Optional[str] = None
    #: Settings for the direct line caller ID name to be shown for this user.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The first name to be used for dial by name functions.
    dial_by_first_name: Optional[str] = None
    #: The last name to be used for dial by name functions.
    dial_by_last_name: Optional[str] = None


class DoNotDisturbInfo(ApiModel):
    #: `true` if the Do Not Disturb feature is enabled.
    enabled: Optional[bool] = None
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: Optional[bool] = None
    #: `true` if a mobile device will still ring even if Do Not Disturb is enabled.
    webex_go_override_enabled: Optional[bool] = None


class EventLongDetailsRecurrenceRecurDaily(ApiModel):
    #: Recurring interval in days. The number of days after the start when an event will repeat.  Repetitions cannot
    #: overlap.
    recur_interval: Optional[int] = None


class EventLongDetailsRecurrenceRecurWeekly(ApiModel):
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int] = None
    #: The Event occurs weekly on Sunday.
    sunday: Optional[bool] = None
    #: The Event occurs weekly on Monday.
    monday: Optional[bool] = None
    #: The Event occurs weekly on Tuesday.
    tuesday: Optional[bool] = None
    #: The Event occurs weekly on Wednesday.
    wednesday: Optional[bool] = None
    #: The Event occurs weekly on Thursday.
    thursday: Optional[bool] = None
    #: The Event occurs weekly on Friday.
    friday: Optional[bool] = None
    #: The Event occurs weekly on Saturday.
    saturday: Optional[bool] = None


class EventLongDetailsRecurrence(ApiModel):
    #: True if the event repeats forever. Requires either `recurDaily` or `recurWeekly` to be specified.
    recur_for_ever: Optional[bool] = None
    #: End date for the recurring event in the format of `YYYY-MM-DD`. Requires either `recurDaily` or `recurWeekly` to
    #: be specified.
    recur_end_date: Optional[datetime] = None
    #: End recurrence after the event has repeated the specified number of times. Requires either `recurDaily` or
    #: `recurWeekly` to be specified.
    recur_end_occurrence: Optional[int] = None
    #: Specifies the number of days between the start of each recurrence. Not allowed with `recurWeekly`.
    recur_daily: Optional[EventLongDetailsRecurrenceRecurDaily] = None
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with `recurDaily`.
    recur_weekly: Optional[EventLongDetailsRecurrenceRecurWeekly] = None


class EventLongDetails(ApiModel):
    #: Name for the event.
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is
    #: required if the `allDayEnabled` field is present.
    start_date: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required
    #: if the `allDayEnabled` field is present.
    end_date: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the
    #: `allDayEnabled` field is false or omitted.
    start_time: Optional[str] = None
    #: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled`
    #: field is false or omitted.
    end_time: Optional[str] = None
    #: True if it is all-day event.
    all_day_enabled: Optional[bool] = None
    #: Recurrence scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class GetCallingBehaviorObjectBehaviorType(str, Enum):
    #: Calling in Webex or Hybrid Calling.
    native_webex_teams_calling = 'NATIVE_WEBEX_TEAMS_CALLING'
    #: Cisco Jabber app
    call_with_app_registered_for_ciscotel = 'CALL_WITH_APP_REGISTERED_FOR_CISCOTEL'
    #: Third-Party app
    call_with_app_registered_for_tel = 'CALL_WITH_APP_REGISTERED_FOR_TEL'
    #: Webex Calling app
    call_with_app_registered_for_webexcalltel = 'CALL_WITH_APP_REGISTERED_FOR_WEBEXCALLTEL'
    #: Calling in Webex (Unified CM)
    native_sip_call_to_ucm = 'NATIVE_SIP_CALL_TO_UCM'
    #: Using the non-string value of `null` results in the organization-wide default calling behavior being in effect.
    null = 'null'


class GetCallingBehaviorObjectEffectiveBehaviorType(str, Enum):
    #: Calling in Webex or Hybrid Calling.
    native_webex_teams_calling = 'NATIVE_WEBEX_TEAMS_CALLING'
    #: Cisco Jabber app
    call_with_app_registered_for_ciscotel = 'CALL_WITH_APP_REGISTERED_FOR_CISCOTEL'
    #: Third-Party app
    call_with_app_registered_for_tel = 'CALL_WITH_APP_REGISTERED_FOR_TEL'
    #: Webex Calling app
    call_with_app_registered_for_webexcalltel = 'CALL_WITH_APP_REGISTERED_FOR_WEBEXCALLTEL'
    #: Calling in Webex (Unified CM)
    native_sip_call_to_ucm = 'NATIVE_SIP_CALL_TO_UCM'


class GetCallingBehaviorObject(ApiModel):
    #: The current Calling Behavior setting for the person. If `null`, the effective Calling Behavior will be the
    #: Organization's current default.
    behavior_type: Optional[GetCallingBehaviorObjectBehaviorType] = None
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if
    #: the user's `behaviorType` is set to `null`.
    effective_behavior_type: Optional[GetCallingBehaviorObjectEffectiveBehaviorType] = None
    #: The UC Manager Profile ID.
    profile_id: Optional[str] = None


class GetEvent(ApiModel):
    #: Identifier for a event.
    id: Optional[str] = None
    #: Name for the event.
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is
    #: required if the `allDayEnabled` field is present.
    start_date: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required
    #: if the `allDayEnabled` field is present.
    end_date: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the
    #: `allDayEnabled` field is false or omitted.
    start_time: Optional[str] = None
    #: End time of the event in the format of `HH:MM `(24 hours format).  This field is required if the `allDayEnabled`
    #: field is false or omitted.
    end_time: Optional[str] = None
    #: True if it is all-day event.
    all_day_enabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Person or list of people.
    people = 'PEOPLE'
    #: Place that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: A Virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class MonitoredNumberObject(ApiModel):
    #: External phone number of the monitored person, workspace or virtual line.
    external: Optional[str] = None
    #: Extension number of the monitored person, workspace or virtual line.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Indicates whether phone number is a primary number.
    primary: Optional[bool] = None


class GetMonitoredElementsObjectMember(ApiModel):
    #: The identifier of the monitored person, workspace or virtual line.
    id: Optional[str] = None
    #: The last name of the monitored person, workspace or virtual line.
    last_name: Optional[str] = None
    #: The first name of the monitored person, workspace or virtual line.
    first_name: Optional[str] = None
    #: The display name of the monitored person, workspace or virtual line.
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE` or `VIRTUAL_LINE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: The email address of the monitored person.
    email: Optional[str] = None
    #: The list of phone numbers containing only the primary number for the monitored person, workspace, or virtual
    #: line.
    numbers: Optional[list[MonitoredNumberObject]] = None
    #: The name of the location where the monitored person, workspace, or virtual line is situated.
    location: Optional[str] = None
    #: The ID for the location.
    location_id: Optional[str] = None


class GetMonitoredElementsObjectCallparkextension(ApiModel):
    #: The identifier of the call park extension.
    id: Optional[str] = None
    #: The name used to describe the call park extension.
    name: Optional[str] = None
    #: The extension number for the call park extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of the call park extension.
    esn: Optional[str] = None
    #: The location name where the call park extension is.
    location: Optional[str] = None
    #: The ID for the location.
    location_id: Optional[str] = None


class GetMonitoredElementsObject(ApiModel):
    member: Optional[GetMonitoredElementsObjectMember] = None
    callparkextension: Optional[GetMonitoredElementsObjectCallparkextension] = None


class GetNumbersPhoneNumbersItemRingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a long ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class GetNumbersPhoneNumbersItem(ApiModel):
    #: Flag to indicate if the number is primary or not.
    primary: Optional[bool] = None
    #: Phone number.
    direct_number: Optional[str] = None
    #: Extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Optional ring pattern. Applicable only for alternate numbers.
    ring_pattern: Optional[GetNumbersPhoneNumbersItemRingPattern] = None


class GetNumbers(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    distinctive_ring_enabled: Optional[bool] = None
    #: Information about the number.
    phone_numbers: Optional[list[GetNumbersPhoneNumbersItem]] = None


class IncomingPermissionSettingExternalTransfer(str, Enum):
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class IncomingPermissionSetting(ApiModel):
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather
    #: than the organizational defaults.
    use_custom_enabled: Optional[bool] = None
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: Optional[IncomingPermissionSettingExternalTransfer] = None
    #: Internal calls are allowed to be received.
    internal_calls_enabled: Optional[bool] = None
    #: Collect calls are allowed to be received.
    collect_calls_enabled: Optional[bool] = None


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    id: Optional[str] = None
    #: Last name of the monitored person, workspace or virtual line.
    last_name: Optional[str] = None
    #: First name of the monitored person, workspace or virtual line.
    first_name: Optional[str] = None
    #: Display name of the monitored person, workspace or virtual line.
    display_name: Optional[str] = None
    #: Indicates whether type is person, workspace or virtual line.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the monitored person, workspace or virtual line.
    email: Optional[str] = None
    #: List of phone numbers of the monitored person, workspace or virtual line.
    numbers: Optional[list[MonitoredNumberObject]] = None


class MonitoringSettings(ApiModel):
    #: Call park notification is enabled or disabled.
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[GetMonitoredElementsObject]] = None


class OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the
    #: originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before
    #: the number is dialed.
    international = 'INTERNATIONAL'
    #: Controls calls requiring Operator Assistance.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Controls calls to Directory Assistant companies that require a charge to connect the call.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Controls calls that are within your country of origin, both within and outside of your local area code.
    national = 'NATIONAL'


class OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction(str, Enum):
    #: Allow the designated call type.
    allow = 'ALLOW'
    #: Block the designated call type.
    block = 'BLOCK'
    #: Allow only via Authorization Code.
    auth_code = 'AUTH_CODE'
    #: Transfer to Auto Transfer Number 1. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class OutgoingCallingPermissionsSettingGetCallingPermissionsItem(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType] = None
    #: Action on the given `callType`.
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Indicates if the restriction is enforced by the system for the corresponding call type and cannot be changed.
    #: For example, certain call types (such as `INTERNATIONAL`) may be permanently blocked and this field will be
    #: `true` to reflect that the restriction is system-controlled and not editable.
    is_call_type_restriction_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSettingGet(ApiModel):
    #: When true, indicates that this user uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    use_custom_enabled: Optional[bool] = None
    #: When true, indicates that this user uses the specified outgoing calling permissions when placing outbound calls.
    use_custom_permissions: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[OutgoingCallingPermissionsSettingGetCallingPermissionsItem]] = None


class OutgoingCallingPermissionsSettingPutCallingPermissionsItem(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType] = None
    #: Action on the given `callType`.
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dailing by first or last name will be enabled.
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only members specified by `monitoringAgents` can
    #: pickup or barge-in on the call.
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredMemberObject]] = None


class PushToTalkAccessType(str, Enum):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk
    #: for can respond.
    two_way = 'TWO_WAY'


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a person receives a Push-to-Talk call and
    #: answers the call automatically.
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredMemberObject]] = None


class ReceptionInfo(ApiModel):
    #: Set to `true` to enable the Receptionist Client feature.
    reception_enabled: Optional[bool] = None
    #: List of people, workspaces or virtual lines to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]] = None


class ScheduleType(str, Enum):
    #: The Schedule type that specifies the business or working hours during the day.
    business_hours = 'businessHours'
    #: The Schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class ScheduleLevel(str, Enum):
    #: The Schedule level that specifies it has been configured at the location level.
    location = 'LOCATION'
    #: The Schedule level that specifies it has been configured at the person level.
    people = 'PEOPLE'


class ScheduleShortDetails(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str] = None
    #: Name for the schedule.
    name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None
    #: The Schedule level whether `LOCATION` or `PEOPLE`.
    level: Optional[ScheduleLevel] = None


class ScheduleLongDetails(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str] = None
    #: Name for the schedule.
    name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None
    #: List of events.
    events: Optional[list[EventLongDetails]] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: A custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: A custom greeting has been uploaded
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None


class VoicemailInfoEmailCopyOfMessage(ApiModel):
    #: When `true` copy of new voicemail message audio will be sent to the designated email.
    enabled: Optional[bool] = None
    #: Email address to which the new voicemail audio will be sent.
    email_id: Optional[str] = None


class VoicemailInfoMessageStorageStorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class VoicemailInfoMessageStorage(ApiModel):
    #: When `true` desktop phone will indicate there are new voicemails.
    mwi_enabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    storage_type: Optional[VoicemailInfoMessageStorageStorageType] = None
    #: External email address to which the new voicemail audio will be sent.  A value for this field must be provided
    #: in the request if a `storageType` of `EXTERNAL` is given in the request.
    external_email: Optional[str] = None


class VoicemailInfoFaxMessage(ApiModel):
    #: When `true` FAX messages for new voicemails will be sent to the designated number.
    enabled: Optional[bool] = None
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage
    #: `enabled` field is given as `true` in the request.
    phone_number: Optional[str] = None
    #: Designates optional extension for the FAX.
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[CallWaitingInfo] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailInfoSendBusyCalls] = None
    send_unanswered_calls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailInfoEmailCopyOfMessage] = None
    message_storage: Optional[VoicemailInfoMessageStorage] = None
    fax_message: Optional[VoicemailInfoFaxMessage] = None
    #: Disable the user-level control when set to "false".
    voice_message_forwarding_enabled: Optional[bool] = None


class VoicemailPutSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail. `numberOfRings` must be between 2 and 20,
    #: inclusive.
    number_of_rings: Optional[int] = None


class RetrieveExecutiveAssistantSettingsForAPersonResponseType(str, Enum):
    #: The feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: The feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: The feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class UserCallSettings12Api(ApiChild, base='people'):
    """
    User Call Settings (1/2)
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their own settings.
    
    Configuring People settings requires a full or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their own settings.
    
    Call Settings API access can be restricted via Control Hub by a full administrator. Restricting access causes the
    APIs to throw a `403 Access Forbidden` error.
    
    See details about `features available by license type for Webex Calling
    <https://help.webex.com/en-us/article/n1qbbp7/Features-available-by-license-type-for-Webex-Calling>`_.
    """

    def retrieve_a_person_s_application_services_settings(self, person_id: str,
                                                          org_id: str = None) -> ApplicationsSetting:
        """
        Retrieve a person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to people in certain scenarios. You
        can also specify which devices can download the Webex Calling app.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`ApplicationsSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/applications')
        data = super().get(url, params=params)
        r = ApplicationsSetting.model_validate(data)
        return r

    def modify_a_person_s_application_services_settings(self, person_id: str,
                                                        ring_devices_for_click_to_dial_calls_enabled: bool = None,
                                                        ring_devices_for_group_page_enabled: bool = None,
                                                        ring_devices_for_call_park_enabled: bool = None,
                                                        browser_client_enabled: bool = None,
                                                        desktop_client_enabled: bool = None,
                                                        tablet_client_enabled: bool = None,
                                                        mobile_client_enabled: bool = None, org_id: str = None):
        """
        Modify a person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.

        This API requires a full or user administrator or location administrator auth token with the
        spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param ring_devices_for_click_to_dial_calls_enabled: When `true`, indicates to ring devices for outbound Click
            to Dial calls.
        :type ring_devices_for_click_to_dial_calls_enabled: bool
        :param ring_devices_for_group_page_enabled: When `true`, indicates to ring devices for inbound Group Pages.
        :type ring_devices_for_group_page_enabled: bool
        :param ring_devices_for_call_park_enabled: When `true`, indicates to ring devices for Call Park recalled.
        :type ring_devices_for_call_park_enabled: bool
        :param browser_client_enabled: If `true`, the browser Webex Calling application is enabled for use.
        :type browser_client_enabled: bool
        :param desktop_client_enabled: If `true`, the desktop Webex Calling application is enabled for use.
        :type desktop_client_enabled: bool
        :param tablet_client_enabled: If `true`, the tablet Webex Calling application is enabled for use.
        :type tablet_client_enabled: bool
        :param mobile_client_enabled: If `true`, the mobile Webex Calling application is enabled for use.
        :type mobile_client_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if ring_devices_for_click_to_dial_calls_enabled is not None:
            body['ringDevicesForClickToDialCallsEnabled'] = ring_devices_for_click_to_dial_calls_enabled
        if ring_devices_for_group_page_enabled is not None:
            body['ringDevicesForGroupPageEnabled'] = ring_devices_for_group_page_enabled
        if ring_devices_for_call_park_enabled is not None:
            body['ringDevicesForCallParkEnabled'] = ring_devices_for_call_park_enabled
        if browser_client_enabled is not None:
            body['browserClientEnabled'] = browser_client_enabled
        if desktop_client_enabled is not None:
            body['desktopClientEnabled'] = desktop_client_enabled
        if tablet_client_enabled is not None:
            body['tabletClientEnabled'] = tablet_client_enabled
        if mobile_client_enabled is not None:
            body['mobileClientEnabled'] = mobile_client_enabled
        url = self.ep(f'{person_id}/features/applications')
        super().put(url, params=params, json=body)

    def read_barge_in_settings_for_a_person(self, person_id: str, org_id: str = None) -> BargeInInfo:
        """
        Read Barge In Settings for a Person

        Retrieve a person's Barge In settings.

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read` or a user auth token with `spark:people_read` scope can be used by a person to read
        their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`BargeInInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/bargeIn')
        data = super().get(url, params=params)
        r = BargeInInfo.model_validate(data)
        return r

    def configure_barge_in_settings_for_a_person(self, person_id: str, enabled: bool = None, tone_enabled: bool = None,
                                                 org_id: str = None):
        """
        Configure Barge In Settings for a Person

        Configure a person's Barge In settings.

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope or a user auth token with `spark:people_write` scope can be used by a person
        to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: Set to enable or disable the Barge In feature.
        :type enabled: bool
        :param tone_enabled: Set to enable or disable a stutter dial tone being played when a person is barging in on
            the active call.
        :type tone_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep(f'{person_id}/features/bargeIn')
        super().put(url, params=params, json=body)

    def read_forwarding_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallForwardingInfo:
        """
        Read Forwarding Settings for a Person

        Retrieve a person's Call Forwarding settings.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read` or a user auth token with `spark:people_read` scope can be used by a person to read
        their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallForwardingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardingInfo.model_validate(data)
        return r

    def configure_call_forwarding_settings_for_a_person(self, person_id: str,
                                                        call_forwarding: CallForwardingPutCallForwarding = None,
                                                        business_continuity: CallForwardingInfoCallForwardingBusy = None,
                                                        org_id: str = None):
        """
        Configure Call Forwarding Settings for a Person

        Configure a person's Call Forwarding settings.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope or a user auth token with `spark:people_write` scope can be used by a person
        to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwardingPutCallForwarding
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingInfoCallForwardingBusy
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        if business_continuity is not None:
            body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/callForwarding')
        super().put(url, params=params, json=body)

    def read_call_recording_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallRecordingInfo:
        """
        Read Call Recording Settings for a Person

        Retrieve a person's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        <div><Callout type="warning">A person with a Webex Calling Standard license is eligible for the Call Recording
        feature only when the Call Recording vendor is Webex.</Callout></div>

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def configure_call_recording_settings_for_a_person(self, person_id: str, enabled: bool = None,
                                                       record: CallRecordingInfoRecord = None,
                                                       record_voicemail_enabled: bool = None,
                                                       start_stop_announcement_enabled: bool = None,
                                                       notification: CallRecordingPutNotification = None,
                                                       repeat: CallRecordingInfoRepeat = None,
                                                       start_stop_announcement: CallRecordingInfoStartStopAnnouncement = None,
                                                       org_id: str = None):
        """
        Configure Call Recording Settings for a Person

        Configure a person's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        <div><Callout type="warning">A person with a Webex Calling Standard license is eligible for the Call Recording
        feature only when the Call Recording vendor is Webex.</Callout></div>

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: `true` if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: CallRecordingInfoRecord
        :param record_voicemail_enabled: When `true`, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param start_stop_announcement_enabled: When enabled, an announcement is played when call recording starts and
            an announcement is played when call recording ends.
        :type start_stop_announcement_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: CallRecordingPutNotification
        :param repeat: Beep sound plays periodically.
        :type repeat: CallRecordingInfoRepeat
        :param start_stop_announcement: Call Recording starts and stops announcement settings.
        :type start_stop_announcement: CallRecordingInfoStartStopAnnouncement
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if record is not None:
            body['record'] = enum_str(record)
        if record_voicemail_enabled is not None:
            body['recordVoicemailEnabled'] = record_voicemail_enabled
        if start_stop_announcement_enabled is not None:
            body['startStopAnnouncementEnabled'] = start_stop_announcement_enabled
        if notification is not None:
            body['notification'] = notification.model_dump(mode='json', by_alias=True, exclude_none=True)
        if repeat is not None:
            body['repeat'] = repeat.model_dump(mode='json', by_alias=True, exclude_none=True)
        if start_stop_announcement is not None:
            body['startStopAnnouncement'] = start_stop_announcement.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/callRecording')
        super().put(url, params=params, json=body)

    def read_call_waiting_settings_for_a_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Waiting Settings for a Person

        Retrieve a person's Call Waiting settings.

        With this feature, a person can place an active call on hold and answer an incoming call.  When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callWaiting')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def configure_call_waiting_settings_for_a_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a person's Call Waiting settings.

        With this feature, a person can place an active call on hold and answer an incoming call.  When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: `true` if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{person_id}/features/callWaiting')
        super().put(url, params=params, json=body)

    def read_caller_id_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallerIdInfo:
        """
        Read Caller ID Settings for a Person

        Retrieve a person's Caller ID settings.

        Caller ID settings control how a person's information is displayed when making outgoing calls.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.<div><Callout type="warning">The fields `directLineCallerIdName.selection`,
        `directLineCallerIdName.customName`, `dialByFirstName`, and `dialByLastName` are not supported in Webex for
        Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to configure and
        view both caller ID and dial-by-name settings.</Callout></div>

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallerIdInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callerId')
        data = super().get(url, params=params)
        r = CallerIdInfo.model_validate(data)
        return r

    def configure_caller_id_settings_for_a_person(self, person_id: str, selected: CallerIdInfoSelected,
                                                  custom_number: str = None, first_name: str = None,
                                                  last_name: str = None, block_in_forward_calls_enabled: bool = None,
                                                  external_caller_id_name_policy: CallerIdInfoExternalCallerIdNamePolicy = None,
                                                  custom_external_caller_id_name: str = None,
                                                  additional_external_caller_id_direct_line_enabled: bool = None,
                                                  additional_external_caller_id_location_number_enabled: bool = None,
                                                  additional_external_caller_id_custom_number: str = None,
                                                  direct_line_caller_id_name: DirectLineCallerIdNameObject = None,
                                                  dial_by_first_name: str = None, dial_by_last_name: str = None,
                                                  org_id: str = None):
        """
        Configure Caller ID Settings for a Person

        Configure a person's Caller ID settings.

        Caller ID settings control how a person's information is displayed when making outgoing calls.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.<div><Callout type="warning">The fields `directLineCallerIdName.selection`,
        `directLineCallerIdName.customName`, `dialByFirstName`, and `dialByLastName` are not supported in Webex for
        Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to configure and
        view both caller ID and dial-by-name settings.</Callout></div>

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CallerIdInfoSelected
        :param custom_number: Custom number which will be shown if CUSTOM is selected. This value must be a number from
            the person's location or from another location with the same country, PSTN provider, and zone (only
            applicable for India locations) as the person's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are
            not allowed. This field has been deprecated. Please use `directLineCallerIdName` and `dialByFirstName`
            instead.
        :type first_name: str
        :param last_name: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are
            not allowed. This field has been deprecated. Please use `directLineCallerIdName` and `dialByLastName`
            instead.
        :type last_name: str
        :param block_in_forward_calls_enabled: Block this person's identity when receiving a call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller Id Name policy is used. Default
            is `DIRECT_LINE`.
        :type external_caller_id_name_policy: CallerIdInfoExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom external caller ID name which will be shown if external caller ID
            name policy is `OTHER`.
        :type custom_external_caller_id_name: str
        :param additional_external_caller_id_direct_line_enabled: To set the person's direct line number as additional
            external caller ID.
        :type additional_external_caller_id_direct_line_enabled: bool
        :param additional_external_caller_id_location_number_enabled: To set the Location main number as additional
            external caller ID for the person.
        :type additional_external_caller_id_location_number_enabled: bool
        :param additional_external_caller_id_custom_number: To set a custom number as additional external caller ID for
            the person. This value must be a number from the person's location or from another location with the same
            country, PSTN provider, and zone (only applicable for India locations) as the person's location.
        :type additional_external_caller_id_custom_number: str
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this user.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_first_name: Sets or clears the the first name to be used for dial by name functions. To clear
            the `dialByFirstName`, the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`,
            `"` and Unicode characters are not allowed.
        :type dial_by_first_name: str
        :param dial_by_last_name: Sets or clears the the last name to be used for dial by name functions. To clear the
            `dialByLastName`, the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_last_name: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        if custom_number is not None:
            body['customNumber'] = custom_number
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if block_in_forward_calls_enabled is not None:
            body['blockInForwardCallsEnabled'] = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body['externalCallerIdNamePolicy'] = enum_str(external_caller_id_name_policy)
        if custom_external_caller_id_name is not None:
            body['customExternalCallerIdName'] = custom_external_caller_id_name
        if additional_external_caller_id_direct_line_enabled is not None:
            body['additionalExternalCallerIdDirectLineEnabled'] = additional_external_caller_id_direct_line_enabled
        if additional_external_caller_id_location_number_enabled is not None:
            body['additionalExternalCallerIdLocationNumberEnabled'] = additional_external_caller_id_location_number_enabled
        if additional_external_caller_id_custom_number is not None:
            body['additionalExternalCallerIdCustomNumber'] = additional_external_caller_id_custom_number
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_first_name is not None:
            body['dialByFirstName'] = dial_by_first_name
        if dial_by_last_name is not None:
            body['dialByLastName'] = dial_by_last_name
        url = self.ep(f'{person_id}/features/callerId')
        super().put(url, params=params, json=body)

    def read_person_s_calling_behavior(self, person_id: str, org_id: str = None) -> GetCallingBehaviorObject:
        """
        Read Person's Calling Behavior

        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.

        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetCallingBehaviorObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callingBehavior')
        data = super().get(url, params=params)
        r = GetCallingBehaviorObject.model_validate(data)
        return r

    def configure_a_person_s_calling_behavior(self, person_id: str,
                                              behavior_type: GetCallingBehaviorObjectBehaviorType = None,
                                              profile_id: str = None, org_id: str = None):
        """
        Configure a person's Calling Behavior

        Modifies the calling behavior settings for the person which includes calling behavior and UC Manager Profile
        ID.

        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param behavior_type: The new Calling Behavior setting for the person (case-insensitive). If `null`, the
            effective Calling Behavior will be the Organization's current default.
        :type behavior_type: GetCallingBehaviorObjectBehaviorType
        :param profile_id: The UC Manager Profile ID. Specifying null results in the organizational default being
            applied. In addition, when `behaviorType` is set to `CALL_WITH_APP_REGISTERED_FOR_CISCOTEL`, then the
            profile ID value will be cleared irrespective of any value being passed.
        :type profile_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if behavior_type is not None:
            body['behaviorType'] = enum_str(behavior_type)
        if profile_id is not None:
            body['profileId'] = profile_id
        url = self.ep(f'{person_id}/features/callingBehavior')
        super().put(url, params=params, json=body)

    def read_do_not_disturb_settings_for_a_person(self, person_id: str, org_id: str = None) -> DoNotDisturbInfo:
        """
        Read Do Not Disturb Settings for a Person

        Retrieve a person's Do Not Disturb settings.

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read` or a user auth token with `spark:people_read` scope can be used by a person to read
        their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`DoNotDisturbInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/doNotDisturb')
        data = super().get(url, params=params)
        r = DoNotDisturbInfo.model_validate(data)
        return r

    def configure_do_not_disturb_settings_for_a_person(self, person_id: str, webex_go_override_enabled: bool,
                                                       enabled: bool = None, ring_splash_enabled: bool = None,
                                                       org_id: str = None):
        """
        Configure Do Not Disturb Settings for a Person

        Configure a person's Do Not Disturb settings.

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope or a user
        auth token with `spark:people_write` scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param webex_go_override_enabled: `true` if a mobile device will still ring even if Do Not Disturb is enabled.
        :type webex_go_override_enabled: bool
        :param enabled: `true` if the Do Not Disturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive
            incoming calls.
        :type ring_splash_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if ring_splash_enabled is not None:
            body['ringSplashEnabled'] = ring_splash_enabled
        body['webexGoOverrideEnabled'] = webex_go_override_enabled
        url = self.ep(f'{person_id}/features/doNotDisturb')
        super().put(url, params=params, json=body)

    def retrieve_executive_assistant_settings_for_a_person(self, person_id: str,
                                                           org_id: str = None) -> RetrieveExecutiveAssistantSettingsForAPersonResponseType:
        """
        Retrieve Executive Assistant Settings for a Person

        Retrieve the executive assistant settings for the specified `personId`.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: RetrieveExecutiveAssistantSettingsForAPersonResponseType
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/executiveAssistant')
        data = super().get(url, params=params)
        r = RetrieveExecutiveAssistantSettingsForAPersonResponseType.model_validate(data['type'])
        return r

    def modify_executive_assistant_settings_for_a_person(self, person_id: str,
                                                         type: RetrieveExecutiveAssistantSettingsForAPersonResponseType = None,
                                                         org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param type: executive assistant type
        :type type: RetrieveExecutiveAssistantSettingsForAPersonResponseType
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if type is not None:
            body['type'] = enum_str(type)
        url = self.ep(f'{person_id}/features/executiveAssistant')
        super().put(url, params=params, json=body)

    def read_hoteling_settings_for_a_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Hoteling Settings for a Person

        Retrieve a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/hoteling')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def configure_hoteling_settings_for_a_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Hoteling Settings for a Person

        Configure a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When `true`, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{person_id}/features/hoteling')
        super().put(url, params=params, json=body)

    def read_incoming_permission_settings_for_a_person(self, person_id: str,
                                                       org_id: str = None) -> IncomingPermissionSetting:
        """
        Read Incoming Permission Settings for a Person

        Retrieve a person's Incoming Permission settings.

        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`IncomingPermissionSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/incomingPermission')
        data = super().get(url, params=params)
        r = IncomingPermissionSetting.model_validate(data)
        return r

    def configure_incoming_permission_settings_for_a_person(self, person_id: str, use_custom_enabled: bool,
                                                            external_transfer: IncomingPermissionSettingExternalTransfer,
                                                            internal_calls_enabled: bool, collect_calls_enabled: bool,
                                                            org_id: str = None):
        """
        Configure Incoming Permission Settings for a Person

        Configure a person's Incoming Permission settings.

        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for
            receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: IncomingPermissionSettingExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['useCustomEnabled'] = use_custom_enabled
        body['externalTransfer'] = enum_str(external_transfer)
        body['internalCallsEnabled'] = internal_calls_enabled
        body['collectCallsEnabled'] = collect_calls_enabled
        url = self.ep(f'{person_id}/features/incomingPermission')
        super().put(url, params=params, json=body)

    def read_call_intercept_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallInterceptInfo:
        """
        Read Call Intercept Settings for a Person

        Retrieves Person's Call Intercept settings.

        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallInterceptInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/intercept')
        data = super().get(url, params=params)
        r = CallInterceptInfo.model_validate(data)
        return r

    def configure_call_intercept_settings_for_a_person(self, person_id: str, enabled: bool = None,
                                                       incoming: CallInterceptPutIncoming = None,
                                                       outgoing: CallInterceptInfoOutgoing = None,
                                                       org_id: str = None):
        """
        Configure Call Intercept Settings for a Person

        Configures a person's Call Intercept settings.

        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: `true` if the intercept feature is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: CallInterceptPutIncoming
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: CallInterceptInfoOutgoing
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming.model_dump(mode='json', by_alias=True, exclude_none=True)
        if outgoing is not None:
            body['outgoing'] = outgoing.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/intercept')
        super().put(url, params=params, json=body)

    def configure_call_intercept_greeting_for_a_person(self, person_id: str, org_id: str = None):
        """
        Configure Call Intercept Greeting for a Person

        Configure a person's Call Intercept Greeting by uploading a Waveform Audio File Format, `.wav`, encoded audio
        file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope or a user
        auth token with `spark:people_write` scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/intercept/actions/announcementUpload/invoke')
        super().post(url, params=params)

    def retrieve_a_person_s_monitoring_settings(self, person_id: str, org_id: str = None) -> MonitoringSettings:
        """
        Retrieve a person's Monitoring Settings

        Retrieves the monitoring settings of the person, which shows specified people, places, virtual lines or call
        park extenions that are being monitored.
        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`MonitoringSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/monitoring')
        data = super().get(url, params=params)
        r = MonitoringSettings.model_validate(data)
        return r

    def modify_a_person_s_monitoring_settings(self, person_id: str, enable_call_park_notification: bool,
                                              monitored_elements: list[str], org_id: str = None):
        """
        Modify a person's Monitoring Settings

        Modifies the monitoring settings of the person.
        Monitors the line status of specified people, places, virtual lines or call park extension. The line status
        indicates if a person, place or virtual line is on a call and if a call has been parked on that extension.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
        :type monitored_elements: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enableCallParkNotification'] = enable_call_park_notification
        body['monitoredElements'] = monitored_elements
        url = self.ep(f'{person_id}/features/monitoring')
        super().put(url, params=params, json=body)

    def get_a_list_of_phone_numbers_for_a_person(self, person_id: str, prefer_e164_format: bool = None,
                                                 org_id: str = None) -> GetNumbers:
        """
        Get a List of Phone Numbers for a Person

        Get a person's phone numbers including alternate numbers.

        A person can have one or more phone numbers and/or extensions via which they can be called.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        <br/>

        <div><Callout type="warning">The `preferE164Format` query parameter can be used to get phone numbers either in
        E.164 format or in their legacy format. The support for getting phone numbers in non-E.164 format in some
        geographies will be removed in the future.</Callout></div>

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param prefer_e164_format: Return phone numbers in E.164 format.
        :type prefer_e164_format: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetNumbers`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if prefer_e164_format is not None:
            params['preferE164Format'] = str(prefer_e164_format).lower()
        url = self.ep(f'{person_id}/features/numbers')
        data = super().get(url, params=params)
        r = GetNumbers.model_validate(data)
        return r

    def retrieve_a_person_s_outgoing_calling_permissions_settings(self, person_id: str,
                                                                  org_id: str = None) -> OutgoingCallingPermissionsSettingGet:
        """
        Retrieve a person's Outgoing Calling Permissions settings.

        Outgoing calling permissions regulate behavior for calls placed to various destinations and default to the
        local level settings. You can change the outgoing calling permissions for a person if you want them to be
        different from your organization's default.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`OutgoingCallingPermissionsSettingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/outgoingPermission')
        data = super().get(url, params=params)
        r = OutgoingCallingPermissionsSettingGet.model_validate(data)
        return r

    def modify_a_person_s_outgoing_calling_permissions_settings(self, person_id: str,
                                                                calling_permissions: list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem],
                                                                use_custom_enabled: bool = None,
                                                                use_custom_permissions: bool = None,
                                                                org_id: str = None):
        """
        Modify a person's Outgoing Calling Permissions settings.

        Outgoing calling permissions regulate behavior for calls placed to various destinations and default to the
        local level settings. You can change the outgoing calling permissions for a person if you want them to be
        different from your organization's default.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem]
        :param use_custom_enabled: When true, indicates that this user uses the shared control that applies to all
            outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When true, indicates that this user uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if use_custom_permissions is not None:
            body['useCustomPermissions'] = use_custom_permissions
        body['callingPermissions'] = TypeAdapter(list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/outgoingPermission')
        super().put(url, params=params, json=body)

    def get_a_person_s_privacy_settings(self, person_id: str, org_id: str = None) -> PrivacyGet:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person ID.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def configure_a_person_s_privacy_settings(self, person_id: str, aa_extension_dialing_enabled: bool = None,
                                              aa_naming_dialing_enabled: bool = None,
                                              enable_phone_status_directory_privacy: bool = None,
                                              enable_phone_status_pickup_barge_in_privacy: bool = None,
                                              monitoring_agents: list[str] = None, org_id: str = None):
        """
        Configure a person's Privacy Settings

        Configure a person's privacy settings for the specified person ID.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.

        This API requires a full or user administrator or location administrator auth token with the
        spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param aa_extension_dialing_enabled: When `true` auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When `true` auto attendant dailing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When `true` phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param enable_phone_status_pickup_barge_in_privacy: When `true` privacy is enforced for call pickup and
            barge-in. Only members specified by `monitoringAgents` can pickup or barge-in on the call.
        :type enable_phone_status_pickup_barge_in_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if aa_extension_dialing_enabled is not None:
            body['aaExtensionDialingEnabled'] = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body['aaNamingDialingEnabled'] = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body['enablePhoneStatusDirectoryPrivacy'] = enable_phone_status_directory_privacy
        if enable_phone_status_pickup_barge_in_privacy is not None:
            body['enablePhoneStatusPickupBargeInPrivacy'] = enable_phone_status_pickup_barge_in_privacy
        if monitoring_agents is not None:
            body['monitoringAgents'] = monitoring_agents
        url = self.ep(f'{person_id}/features/privacy')
        super().put(url, params=params, json=body)

    def read_push_to_talk_settings_for_a_person(self, person_id: str, org_id: str = None) -> PushToTalkInfo:
        """
        Read Push-to-Talk Settings for a Person

        Retrieve a person's Push-to-Talk settings.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/pushToTalk')
        data = super().get(url, params=params)
        r = PushToTalkInfo.model_validate(data)
        return r

    def configure_push_to_talk_settings_for_a_person(self, person_id: str, allow_auto_answer: bool = None,
                                                     connection_type: PushToTalkConnectionType = None,
                                                     access_type: PushToTalkAccessType = None,
                                                     members: list[str] = None, org_id: str = None):
        """
        Configure Push-to-Talk Settings for a Person

        Configure a person's Push-to-Talk settings.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param allow_auto_answer: `true` if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
        :type members: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if allow_auto_answer is not None:
            body['allowAutoAnswer'] = allow_auto_answer
        if connection_type is not None:
            body['connectionType'] = enum_str(connection_type)
        if access_type is not None:
            body['accessType'] = enum_str(access_type)
        if members is not None:
            body['members'] = members
        url = self.ep(f'{person_id}/features/pushToTalk')
        super().put(url, params=params, json=body)

    def read_receptionist_client_settings_for_a_person(self, person_id: str, org_id: str = None) -> ReceptionInfo:
        """
        Read Receptionist Client Settings for a Person

        Retrieve a person's Receptionist Client settings.

        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`ReceptionInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/reception')
        data = super().get(url, params=params)
        r = ReceptionInfo.model_validate(data)
        return r

    def configure_receptionist_client_settings_for_a_person(self, person_id: str, reception_enabled: bool,
                                                            monitored_members: list[str] = None, org_id: str = None):
        """
        Configure Receptionist Client Settings for a Person

        Configure a person's Receptionist Client settings.

        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param reception_enabled: `true` if the Receptionist Client feature is enabled.
        :type reception_enabled: bool
        :param monitored_members: List of members' unique identifiers to monitor.
        :type monitored_members: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['receptionEnabled'] = reception_enabled
        if monitored_members is not None:
            body['monitoredMembers'] = monitored_members
        url = self.ep(f'{person_id}/features/reception')
        super().put(url, params=params, json=body)

    def list_of_schedules_for_a_person(self, person_id: str, name: str = None, type: str = None, org_id: str = None,
                                       **params) -> Generator[ScheduleShortDetails, None, None]:
        """
        List of Schedules for a Person

        List schedules for a person in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param name: Specifies the case insensitive substring to be matched against the schedule names. The maximum
            length is 40.
        :type name: str
        :param type: Specifies the schedule event type to be matched on the given type.
        :type type: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :return: Generator yielding :class:`ScheduleShortDetails` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if type is not None:
            params['type'] = type
        url = self.ep(f'{person_id}/features/schedules')
        return self.session.follow_pagination(url=url, model=ScheduleShortDetails, item_key='schedules', params=params)

    def create_schedule_for_a_person(self, person_id: str, name: str, type: ScheduleType,
                                     events: list[EventLongDetails] = None, org_id: str = None) -> str:
        """
        Create Schedule for a Person

        Create a new schedule for a person.

        Schedules are used to support calling features and can be defined at the location or person level.
        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type: The Schedule type whether `businessHours` or `holidays`.
        :type type: ScheduleType
        :param events: A list of events.
        :type events: list[EventLongDetails]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['type'] = enum_str(type)
        if events is not None:
            body['events'] = TypeAdapter(list[EventLongDetails]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/schedules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_schedule(self, person_id: str, schedule_type: str, schedule_id: str, org_id: str = None):
        """
        Delete a Schedule

        Delete a schedule by its schedule ID.

        Schedules are used to support calling features and can be defined at the location or person level.
        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        super().delete(url, params=params)

    def get_a_schedule_details(self, person_id: str, schedule_type: str, schedule_id: str,
                               org_id: str = None) -> ScheduleLongDetails:
        """
        Get a Schedule Details

        Retrieve a schedule by its schedule ID.

        Schedules are used to support calling features and can be defined at the location or person level.
        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`ScheduleLongDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url, params=params)
        r = ScheduleLongDetails.model_validate(data)
        return r

    def update_a_schedule(self, person_id: str, schedule_type: str, schedule_id: str, new_name: str, name: str,
                          type: ScheduleType, events: list[EventLongDetails] = None, org_id: str = None) -> str:
        """
        Update a Schedule

        Modify a schedule by its schedule ID.

        Schedules are used to support calling features and can be defined at the location or person level.
        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param new_name: New name for the schedule.
        :type new_name: str
        :param name: Name for the schedule.
        :type name: str
        :param type: The Schedule type whether `businessHours` or `holidays`.
        :type type: ScheduleType
        :param events: List of events.
        :type events: list[EventLongDetails]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['newName'] = new_name
        body['name'] = name
        body['type'] = enum_str(type)
        if events is not None:
            body['events'] = TypeAdapter(list[EventLongDetails]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def add_a_new_event_for_person_s_schedule(self, person_id: str, schedule_type: str, schedule_id: str, name: str,
                                              start_date: Union[str, datetime], end_date: Union[str, datetime],
                                              start_time: str, end_time: str, all_day_enabled: bool = None,
                                              recurrence: EventLongDetailsRecurrence = None,
                                              org_id: str = None) -> str:
        """
        Add a New Event for Person's Schedule

        People can use shared location schedules or define personal schedules containing events.

        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.
            This field is required if the `allDayEnabled` field is present.
        :type start_date: Union[str, datetime]
        :param end_date: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This
            field is required if the `allDayEnabled` field is present.
        :type end_date: Union[str, datetime]
        :param start_time: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required
            if the `allDayEnabled` field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if
            the `allDayEnabled` field is false or omitted.
        :type end_time: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrence scheme for an event.
        :type recurrence: EventLongDetailsRecurrence
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        body['startTime'] = start_time
        body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}/events')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_an_event_for_a_person_s_schedule(self, person_id: str, schedule_type: str, schedule_id: str,
                                                event_id: str, org_id: str = None):
        """
        Delete an Event for a person's Schedule

        People can use shared location schedules or define personal schedules containing events.

        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        super().delete(url, params=params)

    def fetch_event_for_a_person_s_schedule(self, person_id: str, schedule_type: str, schedule_id: str, event_id: str,
                                            org_id: str = None) -> GetEvent:
        """
        Fetch Event for a person's Schedule

        People can use shared location schedules or define personal schedules containing events.

        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetEvent`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().get(url, params=params)
        r = GetEvent.model_validate(data)
        return r

    def update_an_event_for_a_person_s_schedule(self, person_id: str, schedule_type: str, schedule_id: str,
                                                event_id: str, new_name: str, name: str, start_date: Union[str,
                                                datetime], end_date: Union[str, datetime], start_time: str,
                                                end_time: str, all_day_enabled: bool = None,
                                                recurrence: EventLongDetailsRecurrence = None,
                                                org_id: str = None) -> str:
        """
        Update an Event for a person's Schedule

        People can use shared location schedules or define personal schedules containing events.

        `businessHours` schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. `holidays` schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either `businessHours` or `holidays`.
        :type schedule_type: str
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param new_name: New name for the event.
        :type new_name: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.
            This field is required if the `allDayEnabled` field is present.
        :type start_date: Union[str, datetime]
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This
            field is required if the `allDayEnabled` field is present.
        :type end_date: Union[str, datetime]
        :param start_time: Start time of the event in the format of HH:MM (24 hours format).  This field is required if
            the `allDayEnabled` field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format).  This field is required if the
            `allDayEnabled` field is false or omitted.
        :type end_time: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: EventLongDetailsRecurrence
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['newName'] = new_name
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        body['startTime'] = start_time
        body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def read_voicemail_settings_for_a_person(self, person_id: str, org_id: str = None) -> VoicemailInfo:
        """
        Read Voicemail Settings for a Person

        Retrieve a person's Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read` or a user auth token with `spark:people_read` scope can be used by a person to read
        their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`VoicemailInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/voicemail')
        data = super().get(url, params=params)
        r = VoicemailInfo.model_validate(data)
        return r

    def configure_voicemail_settings_for_a_person(self, person_id: str,
                                                  notifications: CallInterceptInfoIncomingAnnouncementsNewNumber,
                                                  transfer_to_number: CallInterceptInfoIncomingAnnouncementsNewNumber,
                                                  enabled: bool = None, send_all_calls: CallWaitingInfo = None,
                                                  send_busy_calls: VoicemailPutSendBusyCalls = None,
                                                  send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                                  email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                                  message_storage: VoicemailInfoMessageStorage = None,
                                                  fax_message: VoicemailInfoFaxMessage = None, org_id: str = None):
        """
        Configure Voicemail Settings for a Person

        Configure a person's Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope or a user auth token with `spark:people_write` scope can be used by a person
        to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: CallInterceptInfoIncomingAnnouncementsNewNumber
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: CallInterceptInfoIncomingAnnouncementsNewNumber
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: CallWaitingInfo
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :type message_storage: VoicemailInfoMessageStorage
        :type fax_message: VoicemailInfoFaxMessage
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if send_all_calls is not None:
            body['sendAllCalls'] = send_all_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        if send_busy_calls is not None:
            body['sendBusyCalls'] = send_busy_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        if send_unanswered_calls is not None:
            body['sendUnansweredCalls'] = send_unanswered_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['notifications'] = notifications.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['transferToNumber'] = transfer_to_number.model_dump(mode='json', by_alias=True, exclude_none=True)
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = email_copy_of_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if message_storage is not None:
            body['messageStorage'] = message_storage.model_dump(mode='json', by_alias=True, exclude_none=True)
        if fax_message is not None:
            body['faxMessage'] = fax_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/voicemail')
        super().put(url, params=params, json=body)

    def reset_voicemail_pin(self, person_id: str, org_id: str = None):
        """
        Reset Voicemail PIN

        Reset a voicemail PIN for a person.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail.  A voicemail PIN is used to retrieve your voicemail messages.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        **NOTE**: This API is expected to have an empty request body and Content-Type header should be set to
        `application/json`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/voicemail/actions/resetPin/invoke')
        super().post(url, params=params)

    def configure_busy_voicemail_greeting_for_a_person(self, person_id: str, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Person

        Configure a person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded audio
        file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope or a user auth token with `spark:people_write` scope can be used by a person
        to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url, params=params)

    def configure_no_answer_voicemail_greeting_for_a_person(self, person_id: str, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Person

        Configure a person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope or a user auth token with `spark:people_write` scope can be used by a person
        to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)
