from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Action', 'AgentCallerIdType', 'ApplicationsSetting', 'AudioAnnouncementFileGetObject',
           'AudioAnnouncementFileGetObjectLevel', 'AudioAnnouncementFileGetObjectMediaFileType',
           'AvailableCallerIdObject', 'AvailableSharedLineMemberItem', 'BargeInInfo', 'CallForwardingInfo',
           'CallForwardingInfoCallForwarding', 'CallForwardingInfoCallForwardingAlways',
           'CallForwardingInfoCallForwardingBusy', 'CallForwardingInfoCallForwardingNoAnswer',
           'CallForwardingPutCallForwarding', 'CallForwardingPutCallForwardingNoAnswer', 'CallInterceptInfo',
           'CallInterceptInfoIncoming', 'CallInterceptInfoIncomingAnnouncements',
           'CallInterceptInfoIncomingAnnouncementsGreeting', 'CallInterceptInfoIncomingAnnouncementsNewNumber',
           'CallInterceptInfoIncomingType', 'CallInterceptInfoOutgoing', 'CallInterceptInfoOutgoingType',
           'CallInterceptPutIncoming', 'CallInterceptPutIncomingAnnouncements', 'CallRecordingInfo',
           'CallRecordingInfoCallRecordingAccessSettings', 'CallRecordingInfoNotification',
           'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord', 'CallRecordingInfoRepeat',
           'CallRecordingInfoStartStopAnnouncement', 'CallWaitingInfo', 'CallerIdInfo',
           'CallerIdInfoExternalCallerIdNamePolicy', 'CallerIdInfoSelected', 'CountObject', 'DeviceType',
           'DoNotDisturbInfo', 'EndpointInformation', 'Endpoints', 'ErrorMessageObject', 'ErrorObject',
           'EventLongDetails', 'EventLongDetailsRecurrence', 'EventLongDetailsRecurrenceRecurDaily',
           'EventLongDetailsRecurrenceRecurWeekly', 'GetCallingBehaviorObject',
           'GetCallingBehaviorObjectBehaviorType', 'GetCallingBehaviorObjectEffectiveBehaviorType', 'GetEvent',
           'GetMessageSummaryResponse', 'GetMonitoredElementsObject', 'GetMonitoredElementsObjectCallparkextension',
           'GetMonitoredElementsObjectMember', 'GetMusicOnHoldObject', 'GetNumbers', 'GetNumbersPhoneNumbers',
           'GetNumbersPhoneNumbersRingPattern', 'GetPersonPrimaryAvailablePhoneNumbersLicenseType',
           'GetSharedLineMemberItem', 'GetSharedLineMemberList', 'GetUserMSTeamsSettingsObject',
           'IncomingPermissionSetting', 'IncomingPermissionSettingExternalTransfer', 'ItemObject',
           'JobDetailsResponse', 'JobDetailsResponseById', 'JobDetailsResponseLatestExecutionExitCode',
           'JobExecutionStatusObject', 'LineType', 'Location', 'ModifyUserMSTeamsSettingsObjectSettingName',
           'MonitoredMemberObject', 'MonitoredNumberObject', 'MonitoringSettings', 'NumberOwnerType',
           'OutgoingCallingPermissionsSetting', 'OutgoingCallingPermissionsSettingCallingPermissions',
           'OutgoingCallingPermissionsSettingCallingPermissionsAction',
           'OutgoingCallingPermissionsSettingCallingPermissionsCallType', 'PeopleOrPlaceOrVirtualLineType',
           'PersonCallForwardAvailableNumberObject', 'PersonCallForwardAvailableNumberObjectOwner',
           'PersonECBNAvailableNumberObject', 'PersonECBNAvailableNumberObjectOwner',
           'PersonPrimaryAvailableNumberObject', 'PersonPrimaryAvailableNumberObjectTelephonyType',
           'PersonSecondaryAvailableNumberObject', 'PhoneNumber', 'PrivacyGet', 'PushToTalkAccessType',
           'PushToTalkConnectionType', 'PushToTalkInfo', 'PutSharedLineMemberItem', 'ReceptionInfo',
           'RetrieveExecutiveAssistantSettingsForAPersonResponseType', 'STATE', 'ScheduleLongDetails',
           'ScheduleShortDetails', 'ScheduleType', 'SettingsObject', 'SettingsObjectLevel',
           'SettingsObjectSettingName', 'StartJobExecutionStatusObject', 'StartJobExecutionStatusObjectExitCode',
           'StartJobResponseObject', 'StartJobResponseObjectLatestExecutionStatus', 'StepExecutionStatusesObject',
           'TelephonyType', 'UserCallSettingsApi', 'UserItem', 'UsersListItem', 'VoiceMailPartyInformation',
           'VoiceMessageDetails', 'VoicemailInfo', 'VoicemailInfoEmailCopyOfMessage', 'VoicemailInfoFaxMessage',
           'VoicemailInfoMessageStorage', 'VoicemailInfoMessageStorageStorageType', 'VoicemailInfoSendBusyCalls',
           'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls', 'VoicemailPutSendUnansweredCalls']


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class ApplicationsSetting(ApiModel):
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    #: example: True
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    #: example: True
    ring_devices_for_group_page_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    #: example: True
    ring_devices_for_call_park_enabled: Optional[bool] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    #: example: True
    browser_client_enabled: Optional[bool] = None
    #: Device ID of WebRTC client. Returns only if `browserClientEnabled` is true.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzQyNDM3YzY5LTBlNmYtNGMxZS1iMTJhLTFjNGYxZTk5NDRjMA
    browser_client_id: Optional[str] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    #: example: True
    desktop_client_enabled: Optional[bool] = None
    #: Device ID of Desktop client. Returns only if `desktopClientEnabled` is true.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2IwOWYzMDlhLTY0NDItNDRiYi05OGI2LWEzNTEwYjFhNTJmZg
    desktop_client_id: Optional[str] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    #: example: True
    tablet_client_enabled: Optional[bool] = None
    #: Indicates that the mobile Webex Calling application is enabled for use.
    #: example: True
    mobile_client_enabled: Optional[bool] = None
    #: Number of available device licenses for assigning devices/apps.
    #: example: 35
    available_line_count: Optional[int] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class Location(ApiModel):
    #: Location identifier associated with the members.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzJiNDkyZmZkLTRjNGItNGVmNS04YzAzLWE1MDYyYzM4NDA5Mw
    id: Optional[str] = None
    #: Location name associated with the member.
    #: example: MainOffice
    name: Optional[str] = None


class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of member.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of member.
    #: example: Doe
    last_name: Optional[str] = None
    #: Phone number of member. Currently, E.164 format is not supported.
    #: example: 1234567890
    phone_number: Optional[str] = None
    #: Phone extension of member.
    #: example: 0000
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12340000
    esn: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class BargeInInfo(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an
    #: internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
    system_max_number_of_rings: Optional[int] = None
    #: Indicates the enabled or disabled state of sending incoming calls to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled.
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
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3
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
    #: example: True
    enabled: Optional[bool] = None
    #: New number caller will hear announced.
    #: example: 2225551212
    destination: Optional[str] = None


class CallInterceptInfoIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Filename of custom greeting; will be an empty string if no custom greeting has been uploaded.
    #: example: incoming.wav
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptInfoIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
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
    #: example: INTERCEPT_ALL
    type: Optional[CallInterceptInfoOutgoingType] = None
    #: If `true`, when the person attempts to make an outbound call, a system default message is played and the call is
    #: made to the destination phone number
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    #: example: 2225551212
    destination: Optional[str] = None


class CallInterceptInfo(ApiModel):
    #: `true` if call intercept is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[CallInterceptInfoIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[CallInterceptInfoOutgoing] = None


class CallInterceptPutIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptPutIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
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
    #: example: None
    type: Optional[CallRecordingInfoNotificationType] = None
    #: `true` when the notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class CallRecordingInfoRepeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    #: example: 15
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
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
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
    #: example: WSWYZ25455
    service_provider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    #: example: WSWYZ25455L31161
    external_group: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    #: example: a34iidrh5o@64941297.int10.bcld.webex.com
    external_identifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[CallRecordingInfoStartStopAnnouncement] = None
    #: Settings related to call recording access.
    call_recording_access_settings: Optional[CallRecordingInfoCallRecordingAccessSettings] = None


class CallWaitingInfo(ApiModel):
    #: `true` if the Call Waiting feature is enabled.
    #: example: True
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


class CallerIdInfo(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CallerIdInfoSelected]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    #: example: DIRECT_LINE
    selected: Optional[CallerIdInfoSelected] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    #: example: 2025551212
    direct_number: Optional[str] = None
    #: Extension number of the person.
    #: example: 3456
    extension_number: Optional[str] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected.
    #: example: 2025551212
    location_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: Custom number which will be shown if CUSTOM is selected. This value must be a number from the person's location
    #: or from another location with the same country, PSTN provider, and zone (only applicable for India locations)
    #: as the person's location.
    #: example: 2025551212
    custom_number: Optional[str] = None
    #: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Hakim
    first_name: Optional[str] = None
    #: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Gonzales
    last_name: Optional[str] = None
    #: Block this person's identity when receiving a call.
    #: example: True
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[CallerIdInfoExternalCallerIdNamePolicy] = None
    #: Custom external caller ID name which will be shown if external caller ID name policy is `OTHER`.
    #: example: Hakim custom
    custom_external_caller_id_name: Optional[str] = None
    #: Location's external caller ID name which will be shown if external caller ID name policy is `LOCATION`.
    #: example: Hakim location
    location_external_caller_id_name: Optional[str] = None
    #: Flag to indicate the person's direct line number is available as an additional external caller ID for the
    #: person.
    #: example: True
    additional_external_caller_id_direct_line_enabled: Optional[bool] = None
    #: Flag to indicate the location main number is available as an additional external caller ID for the person.
    additional_external_caller_id_location_number_enabled: Optional[bool] = None
    #: The custom number available as an additional external caller ID for the person. This value must be a number from
    #: the person's location or from another location with the same country, PSTN provider, and zone (only applicable
    #: for India locations) as the person's location.
    #: example: 2025552000
    additional_external_caller_id_custom_number: Optional[str] = None


class DeviceType(str, Enum):
    #: Indicates the endpoint is a device.
    device = 'DEVICE'
    #: Indicates the endpoint is a application.
    application = 'APPLICATION'


class DoNotDisturbInfo(ApiModel):
    #: `true` if the Do Not Disturb feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: Optional[bool] = None


class EventLongDetailsRecurrenceRecurDaily(ApiModel):
    #: Recurring interval in days. The number of days after the start when an event will repeat.  Repetitions cannot
    #: overlap.
    #: example: 1
    recur_interval: Optional[int] = None


class EventLongDetailsRecurrenceRecurWeekly(ApiModel):
    #: Specifies the number of weeks between the start of each recurrence.
    #: example: 1
    recur_interval: Optional[int] = None
    #: Indicates event occurs weekly on Sunday.
    sunday: Optional[bool] = None
    #: Indicates event occurs weekly on Monday.
    monday: Optional[bool] = None
    #: Indicates event occurs weekly on Tuesday.
    tuesday: Optional[bool] = None
    #: Indicates event occurs weekly on Wednesday.
    #: example: True
    wednesday: Optional[bool] = None
    #: Indicates event occurs weekly on Thursday.
    thursday: Optional[bool] = None
    #: Indicates event occurs weekly on Friday.
    friday: Optional[bool] = None
    #: Indicates event occurs weekly on Saturday.
    saturday: Optional[bool] = None


class EventLongDetailsRecurrence(ApiModel):
    #: True if the event repeats forever. Requires either `recurDaily` or `recurWeekly` to be specified.
    #: example: True
    recur_for_ever: Optional[bool] = None
    #: End date for the recurring event in the format of `YYYY-MM-DD`. Requires either `recurDaily` or `recurWeekly` to
    #: be specified.
    #: example: 2020-03-18
    recur_end_date: Optional[datetime] = None
    #: End recurrence after the event has repeated the specified number of times. Requires either `recurDaily` or
    #: `recurWeekly` to be specified.
    #: example: 1
    recur_end_occurrence: Optional[int] = None
    #: Specifies the number of days between the start of each recurrence. Not allowed with `recurWeekly`.
    recur_daily: Optional[EventLongDetailsRecurrenceRecurDaily] = None
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with `recurDaily`.
    recur_weekly: Optional[EventLongDetailsRecurrenceRecurWeekly] = None


class EventLongDetails(ApiModel):
    #: Name for the event.
    #: example: Day_Shift
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is
    #: required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    start_date: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required
    #: if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    end_date: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the
    #: `allDayEnabled` field is false or omitted.
    #: example: 08:00
    start_time: Optional[datetime] = None
    #: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled`
    #: field is false or omitted.
    #: example: 17:00
    end_time: Optional[datetime] = None
    #: True if it is all-day event.
    all_day_enabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class GetSharedLineMemberItem(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Doe
    last_name: Optional[str] = None
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the
    #: future update.
    #: example: 2056852221
    phone_number: Optional[str] = None
    #: Phone extension of a person or workspace.
    #: example: 1111
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341111
    esn: Optional[str] = None
    #: Device port number assigned to a person or workspace.
    #: example: 1
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled__true_: Optional[bool] = Field(alias='t38FaxCompressionEnabled `true`', default=None)
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
    line_weight: Optional[int] = None
    #: Registration home IP for the line port.
    #: example: 198.168.0.1
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP for the line port.
    #: example: 198.168.0.2
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    #: example: 1234
    hotline_destination: Optional[str] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None
    #: Indicates if the member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class GetSharedLineMemberList(ApiModel):
    #: Model name of device.
    #: example: Business Communicator - PC
    model: Optional[str] = None
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]] = None
    #: Maximum number of device ports.
    #: example: 10
    max_line_count: Optional[int] = None


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
    #: example: CALL_WITH_APP_REGISTERED_FOR_CISCOTEL
    behavior_type: Optional[GetCallingBehaviorObjectBehaviorType] = None
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if
    #: the user's `behaviorType` is set to `null`.
    #: example: NATIVE_WEBEX_TEAMS_CALLING
    effective_behavior_type: Optional[GetCallingBehaviorObjectEffectiveBehaviorType] = None
    #: The UC Manager Profile ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    profile_id: Optional[str] = None


class GetEvent(ApiModel):
    #: Identifier for a event.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEVfRVZFTlQvUkdGNVgxTm9hV1ow
    id: Optional[str] = None
    #: Name for the event.
    #: example: Day_Shift
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is
    #: required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    start_date: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required
    #: if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    end_date: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the
    #: `allDayEnabled` field is false or omitted.
    #: example: 08:00
    start_time: Optional[datetime] = None
    #: End time of the event in the format of `HH:MM `(24 hours format).  This field is required if the `allDayEnabled`
    #: field is false or omitted.
    #: example: 17:00
    end_time: Optional[datetime] = None
    #: True if it is all-day event.
    all_day_enabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class MonitoredNumberObject(ApiModel):
    #: External phone number of the monitored person, workspace or virtual line.
    #: example: +19845551088
    external: Optional[str] = None
    #: Extension number of the monitored person, workspace or virtual line.
    #: example: 1088
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341088
    esn: Optional[str] = None
    #: Indicates whether phone number is a primary number.
    #: example: True
    primary: Optional[bool] = None


class GetMonitoredElementsObjectMember(ApiModel):
    #: The identifier of the monitored person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
    id: Optional[str] = None
    #: The last name of the monitored person, place or virtual line.
    #: example: Nelson
    last_name: Optional[str] = None
    #: The first name of the monitored person, place or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: The display name of the monitored person, place or virtual line.
    #: example: John Nelson
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE` or `VIRTUAL_LINE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: The email address of the monitored person, place or virtual line.
    #: example: john.nelson@gmail.com
    email: Optional[str] = None
    #: The list of phone numbers of the monitored person, place or virtual line.
    numbers: Optional[list[MonitoredNumberObject]] = None
    #: The location name where the call park extension is.
    #: example: Dallas
    location: Optional[str] = None
    #: The ID for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    location_id: Optional[str] = None


class GetMonitoredElementsObjectCallparkextension(ApiModel):
    #: The identifier of the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vZTdlZDdiMDEtN2E4Ni00NDEwLWFlODMtOWJmODMzZGEzNzQy
    id: Optional[str] = None
    #: The name used to describe the call park extension.
    #: example: Dallas-Test
    name: Optional[str] = None
    #: The extension number for the call park extension.
    #: example: 4001
    extension: Optional[str] = None
    #: The location name where the call park extension is.
    #: example: Dallas
    location: Optional[str] = None
    #: The ID for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    location_id: Optional[str] = None


class GetMonitoredElementsObject(ApiModel):
    member: Optional[GetMonitoredElementsObjectMember] = None
    callparkextension: Optional[GetMonitoredElementsObjectCallparkextension] = None


class GetNumbersPhoneNumbersRingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a long ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class GetNumbersPhoneNumbers(ApiModel):
    #: Flag to indicate if the number is primary or not.
    #: example: True
    primary: Optional[bool] = None
    #: Phone number.
    #: example: 2143456789
    direct_number: Optional[str] = None
    #: Extension.
    #: example: 1234
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341234
    esn: Optional[str] = None
    #: Optional ring pattern. Applicable only for alternate numbers.
    #: example: NORMAL
    ring_pattern: Optional[GetNumbersPhoneNumbersRingPattern] = None


class GetNumbers(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: Information about the number.
    phone_numbers: Optional[list[GetNumbersPhoneNumbers]] = None


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
    #: example: ALLOW_ALL_EXTERNAL
    external_transfer: Optional[IncomingPermissionSettingExternalTransfer] = None
    #: Internal calls are allowed to be received.
    #: example: True
    internal_calls_enabled: Optional[bool] = None
    #: Collect calls are allowed to be received.
    #: example: True
    collect_calls_enabled: Optional[bool] = None


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the monitored person, workspace or virtual line.
    #: example: Little
    last_name: Optional[str] = None
    #: First name of the monitored person, workspace or virtual line.
    #: example: Alice
    first_name: Optional[str] = None
    #: Display name of the monitored person, workspace or virtual line.
    #: example: Alice Little
    display_name: Optional[str] = None
    #: Indicates whether type is person, workspace or virtual line.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the monitored person, workspace or virtual line.
    #: example: alice@example.com
    email: Optional[str] = None
    #: List of phone numbers of the monitored person, workspace or virtual line.
    numbers: Optional[list[MonitoredNumberObject]] = None


class MonitoringSettings(ApiModel):
    #: Call park notification is enabled or disabled.
    #: example: True
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[GetMonitoredElementsObject]] = None


class OutgoingCallingPermissionsSettingCallingPermissionsCallType(str, Enum):
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
    #: Controls calls that are National.
    national = 'NATIONAL'


class OutgoingCallingPermissionsSettingCallingPermissionsAction(str, Enum):
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


class OutgoingCallingPermissionsSettingCallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: example: INTERNAL_CALL
    call_type: Optional[OutgoingCallingPermissionsSettingCallingPermissionsCallType] = None
    #: Action on the given `callType`.
    #: example: ALLOW
    action: Optional[OutgoingCallingPermissionsSettingCallingPermissionsAction] = None
    #: Allow the person to transfer or forward a call of the specified call type.
    transfer_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSetting(ApiModel):
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[OutgoingCallingPermissionsSettingCallingPermissions]] = None


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    #: example: True
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    #: example: +12145553567
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    #: example: 1234
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[GetNumbersPhoneNumbersRingPattern] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dailing by first or last name will be enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only members specified by `monitoringAgents` can
    #: pickup or barge-in on the call.
    #: example: True
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
    #: example: True
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredMemberObject]] = None


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: Device port number assigned to person or workspace.
    #: example: 1
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled__true_: Optional[bool] = Field(alias='t38FaxCompressionEnabled `true`', default=None)
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
    line_weight: Optional[int] = None
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in `hotlineDestination`.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    #: example: 1234
    hotline_destination: Optional[str] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None


class ReceptionInfo(ApiModel):
    #: Set to `true` to enable the Receptionist Client feature.
    #: example: True
    reception_enabled: Optional[bool] = None
    #: List of people, workspaces or virtual lines to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]] = None


class ScheduleType(str, Enum):
    #: Indicates the schedule type that specifies the business or working hours during the day.
    business_hours = 'businessHours'
    #: Indicates the schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class ScheduleShortDetails(ApiModel):
    #: Identifier for a schedule.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEUvUkdGc2JHRnpYMDltWm1salpWOUliM1Z5Y3c9PQ
    id: Optional[str] = None
    #: Name for the schedule.
    #: example: Dallas_Office_Hours
    name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None


class ScheduleLongDetails(ApiModel):
    #: Identifier for a schedule.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEUvUkdGc2JHRnpYMDltWm1salpWOUliM1Z5Y3c9PQ
    id: Optional[str] = None
    #: Name for the schedule.
    #: example: Dallas_Office_Hours
    name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]] = None


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    #: example: John Smith
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`, and
    #: `user@company.domain`.
    #: example: +12223334444
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9hMTlkODJhMi00ZTY5LTU5YWEtOWYyZi1iY2E2MzEwMTNhNjg=
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFL2ExOWQ3MWEyLTRlOTItOTFhYi05ZjJmLWJjYTEzNTAxM2ExNA==
    place_id: Optional[str] = None
    #: Indicates whether privacy is enabled for the name, number and `personId`/`placeId`.
    privacy_enabled: Optional[bool] = None


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvNmQ0MTgyMTItZjUwNi00Yzk4LTk5MTItNmI1MmE1ZmU2ODgx
    id: Optional[str] = None
    #: The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    #: example: 38
    duration: Optional[int] = None
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation] = None
    #: `true` if the voicemail message is urgent.
    urgent: Optional[bool] = None
    #: `true` if the voicemail message is confidential.
    confidential: Optional[bool] = None
    #: `true` if the voicemail message has been read.
    #: example: True
    read: Optional[bool] = None
    #: Number of pages for the FAX.  Only set for a FAX.
    #: example: 2
    fax_page_count: Optional[int] = None
    #: The date and time the voicemail message was created.
    #: example: 2021-11-14T17:00:00.000Z
    created: Optional[datetime] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Indicates a custom greeting has been uploaded.
    #: example: True
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Indicates a custom greeting has been uploaded
    #: example: True
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
    system_max_number_of_rings: Optional[int] = None


class VoicemailInfoEmailCopyOfMessage(ApiModel):
    #: When `true` copy of new voicemail message audio will be sent to the designated email.
    #: example: True
    enabled: Optional[bool] = None
    #: Email address to which the new voicemail audio will be sent.
    #: example: dummy@example.com
    email_id: Optional[str] = None


class VoicemailInfoMessageStorageStorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class VoicemailInfoMessageStorage(ApiModel):
    #: When `true` desktop phone will indicate there are new voicemails.
    #: example: True
    mwi_enabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    #: example: INTERNAL
    storage_type: Optional[VoicemailInfoMessageStorageStorageType] = None
    #: External email address to which the new voicemail audio will be sent.  A value for this field must be provided
    #: in the request if a `storageType` of `EXTERNAL` is given in the request.
    #: example: dummy@example.com
    external_email: Optional[str] = None


class VoicemailInfoFaxMessage(ApiModel):
    #: When `true` FAX messages for new voicemails will be sent to the designated number.
    #: example: True
    enabled: Optional[bool] = None
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage
    #: `enabled` field is given as `true` in the request.
    #: example: 2025551212
    phone_number: Optional[str] = None
    #: Designates optional extension for the FAX.
    #: example: 1234
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    #: example: True
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
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None


class Endpoints(ApiModel):
    #: Unique identifier for the endpoint.
    #: example: Y2lzY29z...
    id: Optional[str] = None
    #: Enumeration that indicates if the endpoint is of type `DEVICE` or `APPLICATION`.
    type: Optional[DeviceType] = None
    #: The `name` filed in the response is calculated using device tag. Admins have the ability to set tags for
    #: devices. If a `name=<value>` tag is set, for example “name=home phone“, then the `<value>` is included in the
    #: `name` field of the API response. In this example “home phone”.
    #: example: Cisco 8865 (Phone in reception area)
    name: Optional[str] = None


class EndpointInformation(ApiModel):
    #: Person’s preferred answer endpoint.
    #: example: Y2lzY29z...
    preferred_answer_endpoint_id: Optional[str] = None
    #: Array of endpoints available to the person.
    endpoints: Optional[list[Endpoints]] = None


class CountObject(ApiModel):
    #: Total number of user moves requested.
    #: example: 100
    total_moves: Optional[int] = None
    #: Total number of user moves completed successfully.
    #: example: 50
    moved: Optional[int] = None
    #: Total number of user moves that were completed with failures.
    #: example: 50
    failed: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location ID in which the error occurs. For a move operation, this is the target
    #: location ID.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[ErrorObject] = None


class JobDetailsResponseLatestExecutionExitCode(str, Enum):
    #: Job is in progress.
    unknown = 'UNKNOWN'
    #: Job has completed successfully.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'
    #: Job has been stopped.
    stopped = 'STOPPED'
    #: Job has completed with errors.
    completed_with_errors = 'COMPLETED_WITH_ERRORS'


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: The date and time with seconds, the step execution has started in UTC format.
    start_time: Optional[str] = None
    #: The date and time with seconds, the step execution has ended in UTC format.
    end_time: Optional[str] = None
    #: The date and time with seconds, the step has last updated in UTC format.
    last_updated: Optional[str] = None
    #: Displays status for a step.
    status_message: Optional[str] = None
    #: Exit Code for a step.
    exit_code: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: The date and time with seconds, the job has started in UTC format.
    start_time: Optional[str] = None
    #: The date and time with seconds, the job has ended in UTC format.
    end_time: Optional[str] = None
    #: The date and time with seconds, the job has last updated in UTC format post one of the step execution
    #: completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: The date and time with seconds, the job has created in UTC format.
    created_time: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class JobDetailsResponse(ApiModel):
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csv_file: Optional[str] = None
    #: Date and time with seconds, the file expires in UTC format.
    csv_file_expiry_time: Optional[str] = None
    #: 'text/csv',  Format of the file generated.
    file_format: Optional[str] = None


class JobDetailsResponseById(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csv_file: Optional[str] = None
    #: Date and time with seconds, the file expires in UTC format.
    csv_file_expiry_time: Optional[str] = None
    #: 'text/csv',  Format of the file generated.
    file_format: Optional[str] = None
    #: URL to the CSV file containing errors and impacts.
    csv_file_download_url: Optional[str] = None


class UserItem(ApiModel):
    #: User ID to be moved.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzUyMjNiYmVkLTQyYzktNDU0ZC1hMWYzLTdmYWQ1Y2M3ZTZlMw
    user_id: Optional[str] = None
    #: Extension to be moved. Only one new extension can be moved to the target location for a user. An empty value
    #: will remove the configured extension. If not provided, the existing extension will be retained.
    #: example: 28544
    extension: Optional[str] = None
    #: Phone number to be moved. Only one new phone number belonging to the target location can be assigned to a user.
    #: The phone number must follow the E.164 format. An empty value will remove the configured phone number. If not
    #: provided, the existing phone number will be moved to the target location.
    #: example: +18632520486
    phone_number: Optional[str] = None


class UsersListItem(ApiModel):
    #: Target location for the user moves.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    location_id: Optional[str] = None
    #: Set to `true` to validate the user move; this option is not supported for multiple users. Set to `false` to
    #: perform the user move.
    validate: Optional[bool] = None
    #: List of users to be moved.
    users: Optional[list[UserItem]] = None


class StartJobExecutionStatusObjectExitCode(str, Enum):
    #: Job is in progress.
    unknown = 'UNKNOWN'
    #: Job has completed.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'


class StartJobExecutionStatusObject(ApiModel):
    #: Unique identifier for each instance of the job.
    #: example: 332387
    id: Optional[int] = None
    #: Start date and time of the job in UTC format.
    #: example: 2023-05-30T13:04:00.469Z
    start_time: Optional[datetime] = None
    #: Last update date and time of the job in UTC format after a step execution completion.
    #: example: 2023-05-30T13:04:03.574Z
    last_updated: Optional[datetime] = None
    #: Status for the overall steps that are part of the job.
    #: example: COMPLETED
    status_message: Optional[str] = None
    #: Overall result of the job.
    #: example: COMPLETED
    exit_code: Optional[StartJobExecutionStatusObjectExitCode] = None
    #: Creation date and time of the job in UTC format.
    #: example: 2023-05-30T13:04:00.457Z
    created_time: Optional[datetime] = None
    #: Time elapsed in seconds since the job execution started.
    #: example: PT2.752S
    time_elapsed: Optional[str] = None


class StartJobResponseObjectLatestExecutionStatus(str, Enum):
    #: Job has started.
    starting = 'STARTING'
    #: Job is in progress.
    started = 'STARTED'
    #: Job has completed.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'


class StartJobResponseObject(ApiModel):
    #: Job name.
    #: example: moveusers
    name: Optional[str] = None
    #: Unique identifier of the job.
    #: example: Y2lzY29zcGFyazovL3VzL0pPQl9JRC9mZjBlN2Q2Ni05MDRlLTRkZGItYjJlNS05ZGM0ODk0ZDY5OTk
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    #: example: ROUTER_ebb52b5b-d060-4164-9757-48b383423d73
    tracking_id: Optional[str] = None
    #: Unique identifier of the user who ran the job.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YzJhMDUxMC0wOTUwLTQ1MmYtODFmZi05YTVkMjM2OTJkZTY
    source_user_id: Optional[str] = None
    #: Unique identifier of the customer who ran the job.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8wMjEyNGVlZi04YWY3LTQ4OWMtODA1Yi0zNjNjYzY0MDE4OTM
    source_customer_id: Optional[str] = None
    #: Unique identifier of the customer for whom the job was run.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8wMjEyNGVlZi04YWY3LTQ4OWMtODA1Yi0zNjNjYzY0MDE4OTM
    target_customer_id: Optional[str] = None
    #: Unique identifier of the job instance.
    #: example: 10
    instance_id: Optional[int] = None
    #: Most recent step's execution status, including statuses of all steps in the job execution.
    job_execution_status: Optional[list[StartJobExecutionStatusObject]] = None
    #: Most recent status of the job at the time of invocation.
    #: example: STARTED
    latest_execution_status: Optional[StartJobResponseObjectLatestExecutionStatus] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Statistics of the job.
    counts: Optional[CountObject] = None


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across the organization.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across the location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    file_name: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    media_file_type: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file location.
    #: example: ORGANIZATION
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class GetMusicOnHoldObject(ApiModel):
    #: Music on hold enabled or disabled for the person.
    #: example: True
    moh_enabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location. The music on hold setting returned in the response is used
    #: only when music on hold is enabled at the location level. When `mohLocationEnabled` is false and `mohEnabled`
    #: is true, music on hold is disabled for the user. When `mohLocationEnabled` is true and `mohEnabled` is false,
    #: music on hold is turned off for the user. In both cases, music on hold will not be played.
    #: example: True
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the person.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class AgentCallerIdType(str, Enum):
    #: A call queue has been selected for the agent's caller ID.
    call_queue = 'CALL_QUEUE'
    #: A hunt group has been selected for the agent's caller ID.
    hunt_group = 'HUNT_GROUP'


class AvailableCallerIdObject(ApiModel):
    #: Call queue or hunt group's unique identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvMjE3ZDU3YmEtOTMxYi00ZjczLTk1Y2EtOGY3MWFhYzc4MTE5
    id: Optional[str] = None
    #: Member is of type `CALL_QUEUE` or `HUNT_GROUP`
    #: example: CALL_QUEUE
    type: Optional[AgentCallerIdType] = None
    #: Call queue or hunt group's name.
    #: example: TestCallQueue
    name: Optional[str] = None
    #: When not null, it is call queue or hunt group's phone number.
    #: example: +441234200090
    phone_number: Optional[str] = None
    #: When not null, it is call queue or hunt group's extension number.
    #: example: 6001
    extension: Optional[str] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class PersonSecondaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class PersonCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class PersonCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[PersonCallForwardAvailableNumberObjectOwner] = None


class PersonPrimaryAvailableNumberObjectTelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: The object is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class PersonPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[PersonPrimaryAvailableNumberObjectTelephonyType] = None
    #: Mobile Network for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: mobileNetwork
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: AttRtPf
    routing_profile: Optional[str] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None


class PersonECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class PersonECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[PersonECBNAvailableNumberObjectOwner] = None


class SettingsObjectSettingName(str, Enum):
    #: Webex will continue to run but its windows will be closed by default. Users can still access Webex from the
    #: system tray on Windows or the Menu Bar on Mac.
    hide_webex_app = 'HIDE_WEBEX_APP'
    #: Sync presence status between Microsoft Teams and Webex.
    presence_sync = 'PRESENCE_SYNC'


class SettingsObjectLevel(str, Enum):
    #: `settingName` configured at the `GLOBAL` `level`.
    global_ = 'GLOBAL'
    #: `settingName` configured at the `ORGANIZATION` `level`.
    organization = 'ORGANIZATION'
    #: `settingName` configured at the `GROUP` `level`.
    group = 'GROUP'
    #: `settingName` configured at the `PEOPLE` `level`.
    people = 'PEOPLE'


class SettingsObject(ApiModel):
    #: Name of the setting retrieved.
    #: example: HIDE_WEBEX_APP
    setting_name: Optional[SettingsObjectSettingName] = None
    #: Level at which the `settingName` has been set.
    #: example: ORGANIZATION
    level: Optional[SettingsObjectLevel] = None
    #: Either `true` or `false` for the respective `settingName` to be retrieved.
    #: example: True
    value: Optional[bool] = None
    #: The date and time when the respective `settingName` was last updated.
    #: example: 2024-02-24T07:21:23.494198Z
    last_modified: Optional[datetime] = None


class GetUserMSTeamsSettingsObject(ApiModel):
    #: Unique identifier for the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xMWEzZjk5MC1hNjg5LTQ3N2QtYmU2Yi03MTIwMDI1ZDhhYmI
    person_id: Optional[str] = None
    #: Unique identifier for the organization in which the person resides.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi84NzU2ZjkwZS1iZDg4LTRhOTQtOGZiZC0wMzM2NzhmMDU5ZjM
    org_id: Optional[str] = None
    #: Array of `SettingsObject`.
    settings: Optional[list[SettingsObject]] = None


class ModifyUserMSTeamsSettingsObjectSettingName(str, Enum):
    #: Webex will continue to run but its windows will be closed by default. Users can still access Webex from the
    #: system tray on Windows or the Menu Bar on Mac.
    hide_webex_app = 'HIDE_WEBEX_APP'


class RetrieveExecutiveAssistantSettingsForAPersonResponseType(str, Enum):
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class GetMessageSummaryResponse(ApiModel):
    #: The number of new (unread) voicemail messages.
    #: example: 2
    new_messages: Optional[int] = None
    #: The number of old (read) voicemail messages.
    #: example: 5
    old_messages: Optional[int] = None
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int] = None
    #: The number of old (read) urgent voicemail messages.
    #: example: 1
    old_urgent_messages: Optional[int] = None


class GetPersonPrimaryAvailablePhoneNumbersLicenseType(str, Enum):
    webex_calling_professional = 'Webex Calling Professional'
    webex_calling_standard = 'Webex Calling Standard'


class UserCallSettingsApi(ApiChild, base=''):
    """
    User Call Settings
    
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
        url = self.ep(f'people/{person_id}/features/applications')
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
        :param browser_client_enabled: Indicates that the browser Webex Calling application is enabled for use.
        :type browser_client_enabled: bool
        :param desktop_client_enabled: Indicates that the desktop Webex Calling application is enabled for use.
        :type desktop_client_enabled: bool
        :param tablet_client_enabled: Indicates that the tablet Webex Calling application is enabled for use.
        :type tablet_client_enabled: bool
        :param mobile_client_enabled: Indicates that the mobile Webex Calling application is enabled for use.
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
        url = self.ep(f'people/{person_id}/features/applications')
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
        url = self.ep(f'people/{person_id}/features/bargeIn')
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
        url = self.ep(f'people/{person_id}/features/bargeIn')
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
        url = self.ep(f'people/{person_id}/features/callForwarding')
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
        url = self.ep(f'people/{person_id}/features/callForwarding')
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
        url = self.ep(f'people/{person_id}/features/intercept')
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
        url = self.ep(f'people/{person_id}/features/intercept')
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
        url = self.ep(f'people/{person_id}/features/intercept/actions/announcementUpload/invoke')
        super().post(url, params=params)

    def read_call_recording_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallRecordingInfo:
        """
        Read Call Recording Settings for a Person

        Retrieve a person's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

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
        url = self.ep(f'people/{person_id}/features/callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def configure_call_recording_settings_for_a_person(self, person_id: str, enabled: bool = None,
                                                       record: CallRecordingInfoRecord = None,
                                                       record_voicemail_enabled: bool = None,
                                                       start_stop_announcement_enabled: bool = None,
                                                       notification: CallRecordingInfoNotification = None,
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
        :type notification: CallRecordingInfoNotification
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
        url = self.ep(f'people/{person_id}/features/callRecording')
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
        url = self.ep(f'people/{person_id}/features/callWaiting')
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
        url = self.ep(f'people/{person_id}/features/callWaiting')
        super().put(url, params=params, json=body)

    def read_caller_id_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallerIdInfo:
        """
        Read Caller ID Settings for a Person

        Retrieve a person's Caller ID settings.

        Caller ID settings control how a person's information is displayed when making outgoing calls.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

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
        url = self.ep(f'people/{person_id}/features/callerId')
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
                                                  org_id: str = None):
        """
        Configure Caller ID Settings for a Person

        Configure a person's Caller ID settings.

        Caller ID settings control how a person's information is displayed when making outgoing calls.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CallerIdInfoSelected
        :param custom_number: Custom number which will be shown if CUSTOM is selected. This value must be a number from
            the person's location or from another location with the same country, PSTN provider, and zone (only
            applicable for India locations) as the person's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are
            not allowed.
        :type first_name: str
        :param last_name: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are
            not allowed.
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
        url = self.ep(f'people/{person_id}/features/callerId')
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
        url = self.ep(f'people/{person_id}/features/callingBehavior')
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
        url = self.ep(f'people/{person_id}/features/callingBehavior')
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
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        data = super().get(url, params=params)
        r = DoNotDisturbInfo.model_validate(data)
        return r

    def configure_do_not_disturb_settings_for_a_person(self, person_id: str, enabled: bool = None,
                                                       ring_splash_enabled: bool = None, org_id: str = None):
        """
        Configure Do Not Disturb Settings for a Person

        Configure a person's Do Not Disturb settings.

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope or a user
        auth token with `spark:people_write` scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
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
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
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
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
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
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
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
        url = self.ep(f'people/{person_id}/features/hoteling')
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
        url = self.ep(f'people/{person_id}/features/hoteling')
        super().put(url, params=params, json=body)

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
        url = self.ep(f'people/{person_id}/features/monitoring')
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
        url = self.ep(f'people/{person_id}/features/monitoring')
        super().put(url, params=params, json=body)

    def validate_or_initiate_move_users_job(self, users_list: list[UsersListItem],
                                            org_id: str = None) -> StartJobResponseObject:
        """
        Validate or Initiate Move Users Job

        This API allows the user to perform one of the following operations:

        * Setting the `validate` attribute to `true` validates the user move.

        * Setting the `validate` attribute to `false` performs the user move.

        <br/>

        In order to validate or move a user,

        <br/>

        * The user being moved must be a calling user.

        * A maximum of `100` calling users can be moved at a time.

        * The target location must be a calling location.

        <br/>

        Errors occurring during the initial API request validation are captured directly in the error response, along
        with the appropriate HTTP status code.

        <br/>

        Below is a list of possible error `code` values and their associated `message`, which can be found in the
        `errors` array during initial API request validation, regardless of the `validate` attribute value:

        * BATCH-400 - Attribute 'Location ID' is required.

        * BATCH-400 - Attribute 'User ID' is required.

        * BATCH-400 - Users list should not be empty.

        * BATCH-400 - Users should not be empty.

        * 1026006 - Attribute 'Validate' is required.

        * 1026010 - User is not a valid Calling User.

        * 1026011 - Users list should not be empty.

        * 1026012 - Users should not be empty.

        * 1026013 - The source and the target location cannot be the same.

        * 1026014 - Error occurred while processing the move users request.

        * 1026015 - Error occurred while moving user number to target location.

        * 1026016 - User should have either phone number or extension.

        * 1026017 - Phone number is not in e164 format.

        * 1026018 - Selected Users list exceeds the maximum limit.

        * 1026019 - Duplicate entry for user is not allowed.

        * 1026020 - Validate 'true' is supported only for single user.

        <br/>

        When the `validate` attribute is set to true, the API identifies and returns the `errors` and `impacts`
        associated with the user move in the response.

        <br/>

        Below is a list of possible error `code` values and their associated `message`, which can be found in the
        `errors` array, when `validate` attribute is set to be true:

        * 4003 - `User Not Found`

        * 4007 - `User Not Found`

        * 4152 - `Location Not Found`

        * 5620 - `Location Not Found`

        * 4202 - `The extension is not available. It is already assigned to a user : {0}`

        * 8264 - `Routing profile is different with new group: {0}`

        * 19600 - `User has to be within an enterprise to be moved.`

        * 19601 - `User can only be moved to a different group within the same enterprise.`

        * 19602 - `Only regular end user can be moved. Service instance virtual user cannot be moved.`

        * 19603 - `New group already reaches maximum number of user limits.`

        * 19604 - `The {0} number of the user is the same as the calling line ID of the group.`

        * 19605 - `User is assigned services not authorized to the new group: {0}.`

        * 19606 - `User is in an active hoteling/flexible seating association.`

        * 19607 - `User is pilot user of a trunk group.`

        * 19608 - `User is using group level device profiles which is used by other users in current group. Following
        are the device profiles shared with other users: {0}.`

        * 19609 - `Following device profiles cannot be moved to the new group because there are already devices with
        the same name defined in the new group: {0}.`

        * 19610 - `The extension of the user is used as transfer to operator number for following Auto Attendent :
        {0}.`

        * 19611 - `Fail to move announcement file from {0} to {1}.`

        * 19612 - `Fail to move device management file from {0} to {1}.`

        * 19613 - `User is assigned service packs not authorized to the new group: {0}.`

        * 25008 - `Missing Mandatory field name: {0}`

        * 25110 - `{fieldName} cannot be less than {0} or greater than {1} characters.`

        * 25378 - `Target location is same as user's current location.`

        * 25379 - `Error Occurred while Fetching User's Current Location Id.`

        * 25381 - `Error Occurred while rolling back to Old Location Call recording Settings`

        * 25382 - `Error Occurred while Disabling Call Recording for user which is required Before User can be Moved`

        * 25383 - `OCI Error while moving user`

        * 25384 - `Error Occurred while checking for Possible Call Recording Impact.`

        * 25385 - `Error Occurred while getting Call Recording Settings`

        * 27559 - `The groupExternalId search criteria contains groups with different calling zone.`

        * 27960 - `Parameter isWebexCalling, newPhoneNumber, or newExtension can only be set in Webex Calling
        deployment mode.`

        * 27961 - `Parameter isWebexCalling shall be set if newPhoneNumber or newExtension is set.`

        * 27962 - `Work space cannot be moved.`

        * 27963 - `Virtual profile user cannot be moved.`

        * 27965 - `The user's phone number: {0}, is same as the current group charge number.`

        * 27966 - `The phone number, {0}, is not available in the new group.`

        * 27967 - `User is configured as the ECBN user for another user in the current group.`

        * 27968 - `User is configured as the ECBN user for the current group.`

        * 27969 - `User is associated with DECT handset(s): {0}`

        * 27970 - `User is using a customer managed device: {0}`

        * 27971 - `User is using an ATA device: {0}`

        * 27972 - `User is in an active hotdesking association.`

        * 27975 - `Need to unassign CLID number from group before moving the number to the new group. Phone number:
        {0}`

        * 27976 - `Local Gateway configuration is different with new group. Phone number: {0}`

        * 1026015 - `Error occurred while moving user number to target location`

        * 10010000 - `Total numbers exceeded maximum limit allowed`

        * 10010001 - `to-location and from-location cannot be same`

        * 10010002 - `to-location and from-location should belong to same customer`

        * 10010003 - `to-location must have a carrier`

        * 10010004 - `from-location must have a carrier`

        * 10010005 - `Different Carrier move is not supported for non-Cisco PSTN carriers.`

        * 10010006 - `Number move not supported for WEBEX_DIRECT carriers.`

        * 10010007 - `Numbers out of sync, missing on CPAPI`

        * 10010008 - `from-location not found or pstn connection missing in CPAPI`

        * 10010010 - `from-location is in transition`

        * 10010009 - `to-location not found or pstn connection missing in CPAPI`

        * 10010011 - `to-location is in transition`

        * 10010012 - `Numbers don't have a carrier Id`

        * 10010013 - `Location less numbers don't have a carrier Id`

        * 10010014 - `Different Carrier move is not supported for numbers with different country or region.`

        * 10010015 - `Numbers contain mobile and non-mobile types.`

        * 10010016 - `To/From location carriers must be same for mobile numbers.`

        * 10010017 - `Move request for location less number not supported`

        * 10010200 - `Move request for more than one block number is not supported`

        * 10010201 - `Cannot move block number as few numbers not from the block starting %s to %s`

        * 10010202 - `Cannot move block number as few numbers failed VERIFICATION from the block %s to %s`

        * 10010203 - `Cannot move block number as few numbers missing from the block %s to %s`

        * 10010204 - `Cannot move number as it is NOT a part of the block %s to %s`

        * 10010205 - `Move request for Cisco PSTN block order not supported.`

        * 10010299 - `Move order couldn't be created as no valid number to move`

        * 10030000 - `Number not found`

        * 10030001 - `Number does not belong to from-location`

        * 10030002 - `Number is not present in CPAPI`

        * 10030003 - `Number assigned to an user or device`

        * 10030004 - `Number not in Active status`

        * 10030005 - `Number is set as main number of the location`

        * 10030006 - `Number has pending order associated with it`

        * 10030007 - `Number belongs to a location but a from-location was not set`

        * 10030008 - `Numbers from multiple carrier ids are not supported`

        * 10030009 - `Location less number belongs to a location. from-location value is set to null or no location id`

        * 10030010 - `One or more numbers are not portable.`

        * 10030011 - `Mobile number carrier was not set`

        * 10030012 - `Number must be assigned for assigned move`

        * 10050000 - `Failed to update customer reference for phone numbers on carrier`

        * 10050001 - `Failed to update customer reference`

        * 10050002 - `Order is not of operation type MOVE`

        * 10050003 - `CPAPI delete call failed`

        * 10050004 - `Not found in database`

        * 10050005 - `Error sending notification to WxcBillingService`

        * 10050006 - `CPAPI provision number as active call failed with status %s ,reason %s`

        * 10050007 - `Failed to update E911 Service`

        * 10050008 - `Target location does not have Inbound Toll Free license`

        * 10050009 - `Source location or Target location subscription found cancelled or suspended`

        * 10050010 - `Moving On Premises or Non Integrated CCP numbers from one location to another is not supported.`

        * 10099999 - `{Error Code} - {Error Message}`

        <br/>

        Below is a list of possible impact `code` values and their associated `message`, which can be found in the
        `impacts` array, when `validate` attribute is set to be true:

        * 19701 - `The identity/device profile the user is using is moved to the new group: {0}.`

        * 19702 - `The user level customized incoming digit string setting is removed from the user. User is set to use
        the new group setting.`

        * 19703 - `The user level customized outgoing digit plan setting is removed from the user. User is set to use
        the new group setting.`

        * 19704 - `The user level customized enhanced outgoing calling plan setting is removed from the user. User is
        set to use the new group setting.`

        * 19705 - `User is removed from following group services: {0}.`

        * 19706 - `The current group schedule used in any criteria is removed from the service settings.`

        * 19707 - `User is removed from the department of the old group.`

        * 19708 - `User is changed to use the default communication barring profile of the new group.`

        * 19709 - `The communication barring profile of the user is assigned to the new group: {0}.`

        * 19710 - `The charge number for the user is removed.`

        * 19711 - `The disabled FACs for the user are removed because they are not available in the new group.`

        * 19712 - `User is removed from trunk group.`

        * 19713 - `The extension of the user is reset to empty due to either the length is out of bounds of the new
        group, or the extension is already taken in new group.`

        * 19714 - `The extension of the following alternate number is reset to empty due to either the length out of
        bounds of the new group or the extension is already taken in new group: {0}.`

        * 19715 - `The collaborate room using current group default collaborate bridge is moved to the default
        collaborate bridge of the new group.`

        * 19716 - `Previously stored voice messages of the user are no longer available. The new voice message will be
        stored on the mail server of the new group.`

        * 19717 - `The primary number, alternate numbers or fax messaging number of the user are assigned to the new
        group: {0}.`

        * 19718 - `Following domains are assigned to the new group: {0}.`

        * 19719 - `The NCOS of the user is assigned to the new group: {0}.`

        * 19720 - `The office zone of the user is assigned to the new group: {0}.`

        * 19721 - `The announcement media files are relocated to the new group directory.`

        * 19722 - `User CLID number is set to use the new group CLID number: {0}.`

        * 19723 - `New group CLID number is not configured.`

        * 19724 - `The group level announcement file(s) are removed from the user's music on hold settings.`

        * 25388 - `Target Location Does not Have Vendor Configured. Call Recording for user will be disabled`

        * 25389 - `Call Recording Vendor for user will be changed from:{0} to:{1}`

        * 25390 - `Dub point of user is moved to new external group`

        * 25391 - `Error Occurred while moving Call recording Settings to new location`

        * 25392 - `Error Occurred while checking for Possible Call Recording Impact.`

        * 25393 - `Sending Billing Notification Failed`

        This API requires a full administrator auth token with the scopes `spark-admin:telephony_config_write`,
        `spark-admin:people_write`, and `identity:groups_rw`.

        :param users_list: Specifies the users to be moved from the source location.
        :type users_list: list[UsersListItem]
        :param org_id: Create Move Users job for this organization.
        :type org_id: str
        :rtype: StartJobResponseObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['usersList'] = TypeAdapter(list[UsersListItem]).dump_python(users_list, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('telephony/config/jobs/person/moveLocation')
        data = super().post(url, params=params, json=body)
        r = StartJobResponseObject.model_validate(data['response'])
        return r

    def list_move_users_jobs(self, org_id: str = None, **params) -> Generator[JobDetailsResponse, None, None]:
        """
        List Move Users Jobs

        Lists all the Move Users jobs for the given organization in order of most recent job to oldest job irrespective
        of its status.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of Move Users jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`JobDetailsResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/jobs/person/moveLocation')
        return self.session.follow_pagination(url=url, model=JobDetailsResponse, item_key='items', params=params)

    def get_move_users_job_status(self, job_id: str, org_id: str = None) -> JobDetailsResponseById:
        """
        Get Move Users Job Status

        Returns the status and other details of the job.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve job details for this organization.
        :type org_id: str
        :rtype: :class:`JobDetailsResponseById`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}')
        data = super().get(url, params=params)
        r = JobDetailsResponseById.model_validate(data)
        return r

    def pause_the_move_users_job(self, job_id: str, org_id: str = None):
        """
        Pause the Move Users Job

        Pause the running Move Users Job. A paused job can be resumed.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Pause the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Pause the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke')
        super().post(url, params=params)

    def resume_the_move_users_job(self, job_id: str, org_id: str = None):
        """
        Resume the Move Users Job

        Resume the paused Move Users Job that is in paused status.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Resume the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Resume the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke')
        super().post(url, params=params)

    def list_move_users_job_errors(self, job_id: str, org_id: str = None,
                                   **params) -> Generator[ItemObject, None, None]:
        """
        List Move Users Job errors

        Lists all error details of Move Users job. This will not list any errors if `exitCode` is `COMPLETED`. If the
        status is `COMPLETED_WITH_ERRORS` then this lists the cause of failures.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve the error details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def retrieve_music_on_hold_settings_for_a_person(self, person_id: str, org_id: str = None) -> GetMusicOnHoldObject:
        """
        Retrieve Music On Hold Settings for a Person

        Retrieve the person's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving a person's music on hold settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

    def configure_music_on_hold_settings_for_a_person(self, person_id: str, moh_enabled: bool = None,
                                                      greeting: CallInterceptInfoIncomingAnnouncementsGreeting = None,
                                                      audio_announcement_file: AudioAnnouncementFileGetObject = None,
                                                      org_id: str = None):
        """
        Configure Music On Hold Settings for a Person

        Configure a person's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold settings for a person, music on hold setting must be enabled for this location.

        Updating a person's music on hold settings requires a full or user administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param moh_enabled: Music on hold is enabled or disabled for the person.
        :type moh_enabled: bool
        :param greeting: Greeting type for the person.
        :type greeting: CallInterceptInfoIncomingAnnouncementsGreeting
        :param audio_announcement_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_announcement_file: AudioAnnouncementFileGetObject
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
        if moh_enabled is not None:
            body['mohEnabled'] = moh_enabled
        if greeting is not None:
            body['greeting'] = enum_str(greeting)
        if audio_announcement_file is not None:
            body['audioAnnouncementFile'] = audio_announcement_file.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/musicOnHold')
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
        url = self.ep(f'people/{person_id}/features/incomingPermission')
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
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        super().put(url, params=params, json=body)

    def retrieve_a_person_s_outgoing_calling_permissions_settings(self, person_id: str,
                                                                  org_id: str = None) -> OutgoingCallingPermissionsSetting:
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
            access API.
        :type org_id: str
        :rtype: :class:`OutgoingCallingPermissionsSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        data = super().get(url, params=params)
        r = OutgoingCallingPermissionsSetting.model_validate(data)
        return r

    def modify_a_person_s_outgoing_calling_permissions_settings(self, person_id: str, use_custom_enabled: bool,
                                                                calling_permissions: list[OutgoingCallingPermissionsSettingCallingPermissions],
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
        :param use_custom_enabled: When true, indicates that this user uses the specified calling permissions when
            placing outbound calls.
        :type use_custom_enabled: bool
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: list[OutgoingCallingPermissionsSettingCallingPermissions]
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
        body['callingPermissions'] = TypeAdapter(list[OutgoingCallingPermissionsSettingCallingPermissions]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
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
        url = self.ep(f'people/{person_id}/features/numbers')
        data = super().get(url, params=params)
        r = GetNumbers.model_validate(data)
        return r

    def assign_or_unassign_numbers_to_a_person(self, person_id: str, phone_numbers: list[PhoneNumber],
                                               enable_distinctive_ring_pattern: bool = None, org_id: str = None):
        """
        Assign or Unassign numbers to a person

        Assign or unassign alternate phone numbers to a person.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Assigning or unassigning an alternate phone number to a person requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identitfier of the person.
        :type person_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: list[PhoneNumber]
        :param enable_distinctive_ring_pattern: Enables a distinctive ring pattern for the person.
        :type enable_distinctive_ring_pattern: bool
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enable_distinctive_ring_pattern is not None:
            body['enableDistinctiveRingPattern'] = enable_distinctive_ring_pattern
        body['phoneNumbers'] = TypeAdapter(list[PhoneNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/numbers')
        super().put(url, params=params, json=body)

    def get_preferred_answer_endpoint(self, person_id: str, org_id: str = None) -> EndpointInformation:
        """
        Get Preferred Answer Endpoint

        Get the person's preferred answer endpoint and the list of endpoints available for selection. The preferred
        answer endpoint is null if one has not been selected. The list of endpoints is empty if the person has no
        endpoints assigned which support the preferred answer endpoint functionality. These endpoints can be used by
        the following Call Control API's that allow the person to specify an endpointId to use for the call:<br>

        + `/v1/telephony/calls/dial
        <https://developer.webex.com/docs/api/v1/call-controls/dial>`_<br>

        + `/v1/telephony/calls/retrieve
        <https://developer.webex.com/docs/api/v1/call-controls/retrieve>`_<br>

        + `/v1/telephony/calls/pickup
        <https://developer.webex.com/docs/api/v1/call-controls/pickup>`_<br>

        + `/v1/telephony/calls/barge-in
        <https://developer.webex.com/docs/api/v1/call-controls/barge-in>`_<br>

        + `/v1/telephony/calls/answer
        <https://developer.webex.com/docs/api/v1/call-controls/answer>`_<br>

        This API requires `spark:telephony_config_read` or `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`EndpointInformation`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
        data = super().get(url, params=params)
        r = EndpointInformation.model_validate(data)
        return r

    def modify_preferred_answer_endpoint(self, person_id: str, preferred_answer_endpoint_id: str, org_id: str = None):
        """
        Modify Preferred Answer Endpoint

        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the
        `preferredAnswerEndpointId` attribute must be set to null.<br>
        This API requires `spark:telephony_config_write` or `spark-admin:telephony_config_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param preferred_answer_endpoint_id: Person’s preferred answer endpoint.
        :type preferred_answer_endpoint_id: str
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
        body['preferredAnswerEndpointId'] = preferred_answer_endpoint_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
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
        url = self.ep(f'people/{person_id}/features/privacy')
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
        url = self.ep(f'people/{person_id}/features/privacy')
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
        url = self.ep(f'people/{person_id}/features/pushToTalk')
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
        url = self.ep(f'people/{person_id}/features/pushToTalk')
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
        url = self.ep(f'people/{person_id}/features/reception')
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
        url = self.ep(f'people/{person_id}/features/reception')
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
        url = self.ep(f'people/{person_id}/features/schedules')
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
        :param type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type type: ScheduleType
        :param events: Indicates a list of events.
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
        url = self.ep(f'people/{person_id}/features/schedules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_a_schedule_details(self, person_id: str, schedule_type: ScheduleType, schedule_id: str,
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
        :type schedule_type: ScheduleType
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url, params=params)
        r = ScheduleLongDetails.model_validate(data)
        return r

    def update_a_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, new_name: str,
                          name: str, type: ScheduleType, events: list[EventLongDetails] = None,
                          org_id: str = None) -> str:
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
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param new_name: New name for the schedule.
        :type new_name: str
        :param name: Name for the schedule.
        :type name: str
        :param type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type type: ScheduleType
        :param events: Indicates a list of events.
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, org_id: str = None):
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
        :type schedule_type: ScheduleType
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        super().delete(url, params=params)

    def fetch_event_for_a_person_s_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str,
                                            event_id: str, org_id: str = None) -> GetEvent:
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
        :type schedule_type: ScheduleType
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().get(url, params=params)
        r = GetEvent.model_validate(data)
        return r

    def add_a_new_event_for_person_s_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str,
                                              name: str, start_date: Union[str, datetime], end_date: Union[str,
                                              datetime], start_time: Union[str, datetime], end_time: Union[str,
                                              datetime], all_day_enabled: bool = None,
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
        :type schedule_type: ScheduleType
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
        :type start_time: Union[str, datetime]
        :param end_time: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if
            the `allDayEnabled` field is false or omitted.
        :type end_time: Union[str, datetime]
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
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        body['startTime'] = start_time
        body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def update_an_event_for_a_person_s_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str,
                                                event_id: str, new_name: str, name: str, start_date: Union[str,
                                                datetime], end_date: Union[str, datetime], start_time: Union[str,
                                                datetime], end_time: Union[str, datetime],
                                                all_day_enabled: bool = None,
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
        :type schedule_type: ScheduleType
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
        :type start_time: Union[str, datetime]
        :param end_time: End time of the event in the format of HH:MM (24 hours format).  This field is required if the
            `allDayEnabled` field is false or omitted.
        :type end_time: Union[str, datetime]
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def delete_an_event_for_a_person_s_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str,
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
        :type schedule_type: ScheduleType
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
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        super().delete(url, params=params)

    def search_shared_line_appearance_members(self, person_id: str, application_id: str, max_: str = None,
                                              start: str = None, location: str = None, name: str = None,
                                              number: str = None, order: str = None,
                                              extension: str = None) -> list[AvailableSharedLineMemberItem]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param max_: Number of records per page.
        :type max_: str
        :param start: Page number.
        :type start: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (`fname`) or last name (`lname`).
        :type order: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :rtype: list[AvailableSharedLineMemberItem]
        """
        body = dict()
        if max_ is not None:
            body['max'] = max_
        if start is not None:
            body['start'] = start
        if location is not None:
            body['location'] = location
        if name is not None:
            body['name'] = name
        if number is not None:
            body['number'] = number
        if order is not None:
            body['order'] = order
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/availableMembers')
        data = super().get(url, json=body)
        r = TypeAdapter(list[AvailableSharedLineMemberItem]).validate_python(data['members'])
        return r

    def get_shared_line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineMemberList:
        """
        Get Shared-Line Appearance Members

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :rtype: :class:`GetSharedLineMemberList`
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        data = super().get(url)
        r = GetSharedLineMemberList.model_validate(data)
        return r

    def put_shared_line_appearance_members(self, person_id: str, application_id: str,
                                           members: list[PutSharedLineMemberItem] = None):
        """
        Put Shared-Line Appearance Members

        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :type members: list[PutSharedLineMemberItem]
        :rtype: None
        """
        body = dict()
        if members is not None:
            body['members'] = TypeAdapter(list[PutSharedLineMemberItem]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        super().put(url, json=body)

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
        url = self.ep(f'people/{person_id}/features/voicemail')
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
        url = self.ep(f'people/{person_id}/features/voicemail')
        super().put(url, params=params, json=body)

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
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadBusyGreeting/invoke')
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
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)

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
        url = self.ep(f'people/{person_id}/features/voicemail/actions/resetPin/invoke')
        super().post(url, params=params)

    def modify_a_person_s_voicemail_passcode(self, person_id: str, passcode: str, org_id: str = None):
        """
        Modify a person's voicemail passcode.

        Modifying a person's voicemail passcode requires a full administrator, user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Modify voicemail passcode for this person.
        :type person_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'telephony/config/people/{person_id}/voicemail/passcode')
        super().put(url, params=params, json=body)

    def get_message_summary(self) -> GetMessageSummaryResponse:
        """
        Get Message Summary

        Get a summary of the voicemail messages for the user.

        :rtype: :class:`GetMessageSummaryResponse`
        """
        url = self.ep('telephony/voiceMessages/summary')
        data = super().get(url)
        r = GetMessageSummaryResponse.model_validate(data)
        return r

    def list_messages(self) -> list[VoiceMessageDetails]:
        """
        List Messages

        Get the list of all voicemail messages for the user.

        :rtype: list[VoiceMessageDetails]
        """
        url = self.ep('telephony/voiceMessages')
        data = super().get(url)
        r = TypeAdapter(list[VoiceMessageDetails]).validate_python(data['items'])
        return r

    def delete_message(self, message_id: str):
        """
        Delete Message

        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        :rtype: None
        """
        url = self.ep(f'telephony/voiceMessages/{message_id}')
        super().delete(url)

    def mark_as_read(self, message_id: str = None):
        """
        Mark As Read

        Update the voicemail message(s) as read for the user.

        If the `messageId` is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the `messageId` is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        :rtype: None
        """
        body = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('telephony/voiceMessages/markAsRead')
        super().post(url, json=body)

    def mark_as_unread(self, message_id: str = None):
        """
        Mark As Unread

        Update the voicemail message(s) as unread for the user.

        If the `messageId` is provided, then only mark that message as unread.  Otherwise, all messages for the user
        are marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the `messageId` is
            not provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        :rtype: None
        """
        body = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('telephony/voiceMessages/markAsUnread')
        super().post(url, json=body)

    def retrieve_agent_s_list_of_available_caller_ids(self, person_id: str,
                                                      org_id: str = None) -> list[AvailableCallerIdObject]:
        """
        Retrieve Agent's List of Available Caller IDs

        Get the list of call queues and hunt groups available for caller ID use by this person as an agent.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: list[AvailableCallerIdObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/agent/availableCallerIds')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AvailableCallerIdObject]).validate_python(data['availableCallerIds'])
        return r

    def retrieve_agent_s_caller_id_information(self, person_id: str) -> AvailableCallerIdObject:
        """
        Retrieve Agent's Caller ID Information

        Retrieve the Agent's Caller ID Information.

        Each agent will be able to set their outgoing Caller ID as either the Call Queue's Caller ID, Hunt Group's
        Caller ID or their own configured Caller ID.

        This API requires a full admin or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: AvailableCallerIdObject
        """
        url = self.ep(f'telephony/config/people/{person_id}/agent/callerId')
        data = super().get(url)
        r = AvailableCallerIdObject.model_validate(data['selectedCallerId'])
        return r

    def modify_agent_s_caller_id_information(self, person_id: str, selected_caller_id: str):
        """
        Modify Agent's Caller ID Information.

        Each Agent will be able to set their outgoing Caller ID as either the designated Call Queue's Caller ID or Hunt
        Group's Caller ID or their own configured Caller ID

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected_caller_id: The unique identifier of the call queue or hunt group to use for the agent's caller
            ID. Set to null to use the agent's own caller ID.
        :type selected_caller_id: str
        :rtype: None
        """
        body = dict()
        body['selectedCallerId'] = selected_caller_id
        url = self.ep(f'telephony/config/people/{person_id}/agent/callerId')
        super().put(url, json=body)

    def read_call_bridge_settings_for_a_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Bridge Settings for a Person

        Retrieve a person's Call Bridge settings.

        This API requires a full, user or read-only administrator or location administrator auth token with a scope of
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
        url = self.ep(f'telephony/config/people/{person_id}/features/callBridge')
        data = super().get(url, params=params)
        r = data['warningToneEnabled']
        return r

    def configure_call_bridge_settings_for_a_person(self, person_id: str, warning_tone_enabled: bool = None,
                                                    org_id: str = None):
        """
        Configure Call Bridge Settings for a Person

        Configure a person's Call Bridge settings.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param warning_tone_enabled: Set to enable or disable a stutter dial tone being played to all the participants
            when a person is bridged on the active shared line call.
        :type warning_tone_enabled: bool
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
        if warning_tone_enabled is not None:
            body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'telephony/config/people/{person_id}/features/callBridge')
        super().put(url, params=params, json=body)

    def get_person_secondary_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                     org_id: str = None,
                                                     **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a person's secondary phone number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/people/{person_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_fax_message_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a person's FAX message number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/people/{person_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_call_forward_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                        owner_name: str = None, extension: str = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a person's call forward number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_primary_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                                   license_type: GetPersonPrimaryAvailablePhoneNumbersLicenseType = None,
                                                   org_id: str = None,
                                                   **params) -> Generator[PersonPrimaryAvailableNumberObject, None, None]:
        """
        Get Person Primary Available Phone Numbers

        List numbers that are available to be assigned as a person's primary phone number.
        By default, this API returns standard and mobile numbers from all locations that are unassigned. The parameters
        `licenseType` and `locationId` must align with the person's settings to determine the appropriate number for
        assignment.
        Failure to provide these parameters may result in the unsuccessful assignment of the returned number.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param license_type: Used to search numbers according to the person's `licenseType` to which the number will be
            assigned.
        :type license_type: GetPersonPrimaryAvailablePhoneNumbersLicenseType
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if license_type is not None:
            params['licenseType'] = enum_str(license_type)
        url = self.ep('telephony/config/people/primary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_ecbn_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                owner_name: str = None, org_id: str = None,
                                                **params) -> Generator[PersonECBNAvailableNumberObject, None, None]:
        """
        Get Person ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a person's emergency callback number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'telephony/config/people/{person_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_call_intercept_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                          owner_name: str = None, extension: str = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a person's call intercept
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def retrieve_a_person_s_ms_teams_settings(self, person_id: str,
                                              org_id: str = None) -> GetUserMSTeamsSettingsObject:
        """
        Retrieve a Person's MS Teams Settings

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Retrieve a person's MS Teams settings.

        At a person level, MS Teams settings allow access to retrieving the `HIDE WEBEX APP` and `PRESENCE SYNC`
        settings.

        To retrieve a person's MS Teams settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`GetUserMSTeamsSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/settings/msTeams')
        data = super().get(url, params=params)
        r = GetUserMSTeamsSettingsObject.model_validate(data)
        return r

    def configure_a_person_s_ms_teams_setting(self, person_id: str,
                                              setting_name: ModifyUserMSTeamsSettingsObjectSettingName, value: bool,
                                              org_id: str = None):
        """
        Configure a Person's MS Teams Setting

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Configure a Person's MS Teams setting.

        MS Teams settings can be configured at the person level.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting_name: The enum value to be set to `HIDE_WEBEX_APP`.
        :type setting_name: ModifyUserMSTeamsSettingsObjectSettingName
        :param value: The boolean value to update the `HIDE_WEBEX_APP` setting, either `true` or `false`. Set to `null`
            to delete the `HIDE_WEBEX_APP` setting.
        :type value: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['settingName'] = enum_str(setting_name)
        body['value'] = value
        url = self.ep(f'telephony/config/people/{person_id}/settings/msTeams')
        super().put(url, params=params, json=body)
