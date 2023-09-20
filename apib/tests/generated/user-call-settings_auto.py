from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Action', 'AgentAvaliableCallQueueIdList', 'AgentCallQueueId', 'ApplicationsSetting', 'ApplicationsSettingPut', 'AvailableSharedLineMemberItem', 'AvailableSharedLineMemberList', 'BargeInInfo', 'CallForwardingInfo', 'CallForwardingInfoCallForwarding', 'CallForwardingInfoCallForwardingAlways', 'CallForwardingInfoCallForwardingBusy', 'CallForwardingInfoCallForwardingNoAnswer', 'CallForwardingPut', 'CallForwardingPutCallForwarding', 'CallForwardingPutCallForwardingNoAnswer', 'CallInterceptInfo', 'CallInterceptInfoIncoming', 'CallInterceptInfoIncomingAnnouncements', 'CallInterceptInfoIncomingAnnouncementsGreeting', 'CallInterceptInfoIncomingAnnouncementsNewNumber', 'CallInterceptInfoIncomingType', 'CallInterceptInfoOutgoing', 'CallInterceptInfoOutgoingType', 'CallInterceptPut', 'CallInterceptPutIncoming', 'CallInterceptPutIncomingAnnouncements', 'CallQueueObject', 'CallRecordingInfo', 'CallRecordingInfoNotification', 'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord', 'CallRecordingInfoRepeat', 'CallRecordingInfoStartStopAnnouncement', 'CallRecordingPut', 'CallWaitingInfo', 'CallerIdInfo', 'CallerIdInfoExternalCallerIdNamePolicy', 'CallerIdPut', 'CallerIdSelectedType', 'DeviceType', 'DoNotDisturbInfo', 'EndpointIdType', 'EndpointInformation', 'Endpoints', 'EventLongDetails', 'EventLongDetailsRecurrence', 'EventLongDetailsRecurrenceRecurDaily', 'EventLongDetailsRecurrenceRecurWeekly', 'EventPutResponseWithId', 'GetCallingBehaviorObject', 'GetCallingBehaviorObjectBehaviorType', 'GetCallingBehaviorObjectEffectiveBehaviorType', 'GetEvent', 'GetMonitoredElementsObject', 'GetMonitoredElementsObjectCallparkextension', 'GetMonitoredElementsObjectMember', 'GetNumbers', 'GetNumbersPhoneNumbers', 'GetNumbersPhoneNumbersRingPattern', 'GetSharedLineMemberItem', 'GetSharedLineMemberList', 'IncomingPermissionSetting', 'IncomingPermissionSettingExternalTransfer', 'LineType', 'MonitoredMemberObject', 'MonitoredNumberObject', 'MonitoringSettings', 'MonitoringSettingsPut', 'NoneType', 'OutgoingCallingPermissionsSetting', 'OutgoingCallingPermissionsSettingCallingPermissions', 'OutgoingCallingPermissionsSettingCallingPermissionsAction', 'OutgoingCallingPermissionsSettingCallingPermissionsCallType', 'PatchCallingBehaviorObject', 'PeopleOrPlaceOrVirtualLineType', 'PhoneNumber', 'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo', 'PushToTalkPut', 'PutAgentCallQueueId', 'PutAgentCallQueueIdSelectedQueue', 'PutEvent', 'PutSharedLineMemberItem', 'PutSharedLineMemberList', 'ReceptionInfo', 'ReceptionPut', 'ScheduleCollectionRequest', 'ScheduleCollectionResponse', 'ScheduleLongDetails', 'ScheduleShortDetails', 'ScheduleType', 'ScheduleUpdateRequest', 'UserNumbersPatch', 'UserType', 'VoiceMailPartyInformation', 'VoiceMessageDetails', 'VoicemailInfo', 'VoicemailInfoEmailCopyOfMessage', 'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage', 'VoicemailInfoMessageStorageStorageType', 'VoicemailInfoSendBusyCalls', 'VoicemailInfoSendUnansweredCalls', 'VoicemailInfoTransferToNumber', 'VoicemailPut', 'VoicemailPutSendBusyCalls', 'VoicemailPutSendUnansweredCalls']


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class CallQueueObject(ApiModel):
    #: Indicates the Call Queue's unique identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvMjE3ZDU3YmEtOTMxYi00ZjczLTk1Y2EtOGY3MWFhYzc4MTE5
    id: Optional[str] = None
    #: Indicates the Call Queue's name.
    #: example: SalesQueue
    name: Optional[str] = None
    #: When not null, indicates the Call Queue's phone number.
    #: example: 4255558100
    phoneNumber: Optional[str] = None
    #: When not null, indicates the Call Queue's extension number.
    #: example: 8100
    extension: Optional[datetime] = None


class AgentAvaliableCallQueueIdList(ApiModel):
    #: Indicates a list of Call Queues that the agent belongs and are available to be selected as the Caller ID for outgoing calls. It is empty when the agent's Call Queues have disabled the Call Queue outgoing phone number setting to be used as Caller ID. In the case where this setting is enabled the array will be populated.
    availableQueues: Optional[list[CallQueueObject]] = None


class AgentCallQueueId(ApiModel):
    #: When true, indicates that this agent is using the `selectedQueue` for its Caller ID. When false, indicates that it is using the agent's configured Caller ID.
    #: example: True
    queueCallerIdEnabled: Optional[bool] = None
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when `queueCallerIdEnabled` is false. When `queueCallerIdEnabled` is true this data must be populated.
    selectedQueue: Optional[CallQueueObject] = None


class ApplicationsSetting(ApiModel):
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    #: example: True
    ringDevicesForClickToDialCallsEnabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    #: example: True
    ringDevicesForGroupPageEnabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    #: example: True
    ringDevicesForCallParkEnabled: Optional[bool] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    #: example: True
    browserClientEnabled: Optional[bool] = None
    #: Device ID of WebRTC client. Returns only if `browserClientEnabled` is true.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzQyNDM3YzY5LTBlNmYtNGMxZS1iMTJhLTFjNGYxZTk5NDRjMA
    browserClientId: Optional[str] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    #: example: True
    desktopClientEnabled: Optional[bool] = None
    #: Device ID of Desktop client. Returns only if `desktopClientEnabled` is true.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2IwOWYzMDlhLTY0NDItNDRiYi05OGI2LWEzNTEwYjFhNTJmZg
    desktopClientId: Optional[str] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    #: example: True
    tabletClientEnabled: Optional[bool] = None
    #: Indicates that the mobile Webex Calling application is enabled for use.
    #: example: True
    mobileClientEnabled: Optional[bool] = None
    #: Number of available device licenses for assigning devices/apps.
    #: example: 35.0
    availableLineCount: Optional[int] = None


class ApplicationsSettingPut(ApiModel):
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    #: example: True
    ringDevicesForClickToDialCallsEnabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    #: example: True
    ringDevicesForGroupPageEnabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    #: example: True
    ringDevicesForCallParkEnabled: Optional[bool] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    #: example: True
    browserClientEnabled: Optional[bool] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    #: example: True
    desktopClientEnabled: Optional[bool] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    #: example: True
    tabletClientEnabled: Optional[bool] = None
    #: Indicates that the mobile Webex Calling application is enabled for use.
    #: example: True
    mobileClientEnabled: Optional[bool] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class PutAgentCallQueueIdSelectedQueue(ApiModel):
    #: Indicates the Call Queue's unique identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvMjE3ZDU3YmEtOTMxYi00ZjczLTk1Y2EtOGY3MWFhYzc4MTE5
    id: Optional[str] = None
    #: Indicates the Call Queue's name.
    #: example: SalesQueue
    name: Optional[str] = None


class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of member.
    #: example: John
    firstName: Optional[str] = None
    #: Last name of member.
    #: example: Doe
    lastName: Optional[str] = None
    #: Phone number of member. Currently, E.164 format is not supported.
    #: example: 1234567890
    phoneNumber: Optional[str] = None
    #: Phone extension of member.
    #: example: 0000
    extension: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    lineType: Optional[LineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[PutAgentCallQueueIdSelectedQueue] = None


class AvailableSharedLineMemberList(ApiModel):
    members: Optional[list[AvailableSharedLineMemberItem]] = None


class BargeInInfo(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    toneEnabled: Optional[bool] = None


class CallForwardingInfoCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ringReminderEnabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destinationVoicemailEnabled: Optional[bool] = None


class CallForwardingInfoCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destinationVoicemailEnabled: Optional[bool] = None


class CallForwardingInfoCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3.0
    numberOfRings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15.0
    systemMaxNumberOfRings: Optional[int] = None
    #: Indicates the enabled or disabled state of sending incoming calls to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destinationVoicemailEnabled: Optional[bool] = None


class CallForwardingInfoCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    noAnswer: Optional[CallForwardingInfoCallForwardingNoAnswer] = None


class CallForwardingInfo(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    callForwarding: Optional[CallForwardingInfoCallForwarding] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    businessContinuity: Optional[CallForwardingInfoCallForwardingBusy] = None


class CallForwardingPutCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3.0
    numberOfRings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destinationVoicemailEnabled: Optional[bool] = None


class CallForwardingPutCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    noAnswer: Optional[CallForwardingPutCallForwardingNoAnswer] = None


class CallForwardingPut(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    callForwarding: Optional[CallForwardingPutCallForwarding] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring problem.
    businessContinuity: Optional[CallForwardingInfoCallForwardingBusy] = None


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
    newNumber: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zeroTransfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptInfoIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the person's voicemail.
    voicemailEnabled: Optional[bool] = None
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
    #: If `true`, when the person attempts to make an outbound call, a system default message is played and the call is made to the destination phone number
    transferEnabled: Optional[bool] = None
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
    newNumber: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how call will be handled if zero (0) is pressed.
    zeroTransfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptPutIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the person's voicemail.
    voicemailEnabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptPutIncomingAnnouncements] = None


class CallInterceptPut(ApiModel):
    #: `true` if the intercept feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[CallInterceptPutIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[CallInterceptInfoOutgoing] = None


class CallRecordingInfoRecord(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (`*44`) has been entered. Pause, resume, and stop controls are supported.
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
    #: example: 15.0
    interval: Optional[int] = None
    #: `true` when ongoing call recording tone will be played at the designated interval. `false` indicates no warning tone will be played.
    enabled: Optional[bool] = None


class CallRecordingInfoStartStopAnnouncement(ApiModel):
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call recording ends for internal calls.
    internalCallsEnabled: Optional[bool] = None
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call recording ends for PSTN calls.
    pstnCallsEnabled: Optional[bool] = None


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    recordVoicemailEnabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
    startStopAnnouncementEnabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Name of the service provider providing call recording service.
    #: example: WSWYZ25455
    serviceProvider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    #: example: WSWYZ25455L31161
    externalGroup: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    #: example: a34iidrh5o@64941297.int10.bcld.webex.com
    externalIdentifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    startStopAnnouncement: Optional[CallRecordingInfoStartStopAnnouncement] = None


class CallRecordingPut(ApiModel):
    #: `true` if call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    recordVoicemailEnabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
    startStopAnnouncementEnabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Call Recording starts and stops announcement settings.
    startStopAnnouncement: Optional[CallRecordingInfoStartStopAnnouncement] = None


class CallWaitingInfo(ApiModel):
    #: `true` if the Call Waiting feature is enabled.
    #: example: True
    enabled: Optional[bool] = None


class CallerIdInfoExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the `customExternalCallerIdName` field.
    other = 'OTHER'


class CallerIdSelectedType(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the mobile number for this person.
    mobile_number = 'MOBILE_NUMBER'
    #: Outgoing caller ID will show the value from the `customNumber` field.
    custom = 'CUSTOM'
    none_ = 'none'


class CallerIdInfo(ApiModel):
    #: Allowed types for the `selected` field.
    types: Optional[list[CallerIdSelectedType]] = None
    #: Which type of outgoing Caller ID will be used.
    #: example: DIRECT_LINE
    selected: Optional[CallerIdSelectedType] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    #: example: 2025551212
    directNumber: Optional[str] = None
    #: Extension number which will be shown if `DIRECT_LINE` is selected.
    #: example: 3456
    extensionNumber: Optional[datetime] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected.
    #: example: 2025551212
    locationNumber: Optional[str] = None
    #: Mobile number which will be shown if `MOBILE_NUMBER` is selected.
    #: example: 2025552121
    mobileNumber: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    tollFreeLocationNumber: Optional[bool] = None
    #: This value must be an assigned number from the person's location.
    #: example: 2025551212
    customNumber: Optional[str] = None
    #: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Hakim
    firstName: Optional[str] = None
    #: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Gonzales
    lastName: Optional[str] = None
    #: `true` if the person's identity is blocked when receiving a transferred or forwarded call.
    #: example: True
    blockInForwardCallsEnabled: Optional[bool] = None
    #: Designates which type of External Caller Id Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    externalCallerIdNamePolicy: Optional[CallerIdInfoExternalCallerIdNamePolicy] = None
    #: Custom External Caller Name, which will be shown if External Caller Id Name is `OTHER`.
    #: example: Hakim custom
    customExternalCallerIdName: Optional[str] = None
    #: Location's caller ID.
    #: example: Hakim location
    locationExternalCallerIdName: Optional[str] = None


class CallerIdPut(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    #: example: DIRECT_LINE
    selected: Optional[CallerIdSelectedType] = None
    #: This value must be an assigned number from the person's location.
    #: example: 2025551212
    customNumber: Optional[str] = None
    #: Person's Caller ID first name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Hakim
    firstName: Optional[str] = None
    #: Person's Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Gonzales
    lastName: Optional[str] = None
    #: `true` if person's identity has to be blocked when receiving a transferred or forwarded call.
    #: example: True
    blockInForwardCallsEnabled: Optional[bool] = None
    #: Designates which type of External Caller Id Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    externalCallerIdNamePolicy: Optional[CallerIdInfoExternalCallerIdNamePolicy] = None
    #: Person's custom External Caller ID last name.  Characters of `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Hakim Custom
    customExternalCallerIdName: Optional[str] = None


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
    ringSplashEnabled: Optional[bool] = None


class EndpointIdType(ApiModel):
    #: Person’s preferred answer endpoint.
    #: example: Y2lzY29z...
    preferredAnswerEndpointId: Optional[str] = None


class EventLongDetailsRecurrenceRecurDaily(ApiModel):
    #: Recurring interval in days. The number of days after the start when an event will repeat.  Repetitions cannot overlap.
    #: example: 1.0
    recurInterval: Optional[int] = None


class EventLongDetailsRecurrenceRecurWeekly(ApiModel):
    #: Specifies the number of weeks between the start of each recurrence.
    #: example: 1.0
    recurInterval: Optional[int] = None
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
    recurForEver: Optional[bool] = None
    #: End date for the recurring event in the format of `YYYY-MM-DD`. Requires either `recurDaily` or `recurWeekly` to be specified.
    #: example: 2020-03-18
    recurEndDate: Optional[datetime] = None
    #: End recurrence after the event has repeated the specified number of times. Requires either `recurDaily` or `recurWeekly` to be specified.
    #: example: 1.0
    recurEndOccurrence: Optional[int] = None
    #: Specifies the number of days between the start of each recurrence. Not allowed with `recurWeekly`.
    recurDaily: Optional[EventLongDetailsRecurrenceRecurDaily] = None
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with `recurDaily`.
    recurWeekly: Optional[EventLongDetailsRecurrenceRecurWeekly] = None


class EventLongDetails(ApiModel):
    #: Name for the event.
    #: example: Day_Shift
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    startDate: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    endDate: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 08:00
    startTime: Optional[datetime] = None
    #: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 17:00
    endTime: Optional[datetime] = None
    #: True if it is all-day event.
    allDayEnabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class EventPutResponseWithId(ApiModel):
    #: Identifier for a event.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEVfRVZFTlQvUTJWdWRISmhiRjlhYjI1bFgwUmhlVjlUYUdsbWRBPT0
    id: Optional[str] = None


class UserType(str, Enum):
    #: The associated member is a person.
    people = 'PEOPLE'
    #: The associated member is a workspace.
    place = 'PLACE'


class GetSharedLineMemberItem(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    firstName: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Doe
    lastName: Optional[str] = None
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the future update.
    #: example: 2056852221
    phoneNumber: Optional[str] = None
    #: Phone extension of a person or workspace.
    #: example: 1111
    extension: Optional[datetime] = None
    #: Device port number assigned to a person or workspace.
    #: example: 1.0
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    #: example: True
    t38FaxCompressionEnabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: true
    primaryOwner: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    lineType: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1.0
    lineWeight: Optional[int] = None
    #: Registration home IP for the line port.
    #: example: 198.168.0.1
    hostIP: Optional[str] = None
    #: Registration remote IP for the line port.
    #: example: 198.168.0.2
    remoteIP: Optional[str] = None
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotlineEnabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    #: example: 1234
    hotlineDestination: Optional[datetime] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all the endpoints on the device. When set to `false`, a call decline request is only declined at the current endpoint.
    #: example: True
    allowCallDeclineEnabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    lineLabel: Optional[str] = None
    #: Indicates if the member is of type `PEOPLE` or `PLACE`.
    memberType: Optional[UserType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[PutAgentCallQueueIdSelectedQueue] = None


class GetSharedLineMemberList(ApiModel):
    #: Model name of device.
    #: example: Business Communicator - PC
    model: Optional[str] = None
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]] = None
    #: Maximum number of device ports.
    #: example: 10.0
    maxLineCount: Optional[int] = None


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
    #: The current Calling Behavior setting for the person. If `null`, the effective Calling Behavior will be the Organization's current default.
    #: example: CALL_WITH_APP_REGISTERED_FOR_CISCOTEL
    behaviorType: Optional[GetCallingBehaviorObjectBehaviorType] = None
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if the user's `behaviorType` is set to `null`.
    #: example: NATIVE_WEBEX_TEAMS_CALLING
    effectiveBehaviorType: Optional[GetCallingBehaviorObjectEffectiveBehaviorType] = None
    #: The UC Manager Profile ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    profileId: Optional[str] = None


class GetEvent(ApiModel):
    #: Identifier for a event.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEVfRVZFTlQvUkdGNVgxTm9hV1ow
    id: Optional[str] = None
    #: Name for the event.
    #: example: Day_Shift
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    startDate: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    endDate: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 08:00
    startTime: Optional[datetime] = None
    #: End time of the event in the format of `HH:MM `(24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 17:00
    endTime: Optional[datetime] = None
    #: True if it is all-day event.
    allDayEnabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class MonitoredNumberObject(ApiModel):
    #: External phone number of the monitored person, workspace or virtual line.
    #: example: +19845551088
    external: Optional[str] = None
    #: Extension number of the monitored person, workspace or virtual line.
    #: example: 1088
    extension: Optional[datetime] = None
    #: Indicates whether phone number is a primary number.
    #: example: True
    primary: Optional[bool] = None


class GetMonitoredElementsObjectMember(ApiModel):
    #: The identifier of the monitored person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
    id: Optional[str] = None
    #: The last name of the monitored person, place or virtual line.
    #: example: Nelson
    lastName: Optional[str] = None
    #: The first name of the monitored person, place or virtual line.
    #: example: John
    firstName: Optional[str] = None
    #: The display name of the monitored person, place or virtual line.
    #: example: John Nelson
    displayName: Optional[str] = None
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
    locationId: Optional[str] = None


class GetMonitoredElementsObjectCallparkextension(ApiModel):
    #: The identifier of the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vZTdlZDdiMDEtN2E4Ni00NDEwLWFlODMtOWJmODMzZGEzNzQy
    id: Optional[str] = None
    #: The name used to describe the call park extension.
    #: example: Dallas-Test
    name: Optional[str] = None
    #: The extension number for the call park extension.
    #: example: 4001
    extension: Optional[datetime] = None
    #: The location name where the call park extension is.
    #: example: Dallas
    location: Optional[str] = None
    #: The ID for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    locationId: Optional[str] = None


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
    directNumber: Optional[str] = None
    #: Extension.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Optional ring pattern. Applicable only for alternate numbers.
    #: example: NORMAL
    ringPattern: Optional[GetNumbersPhoneNumbersRingPattern] = None


class GetNumbers(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    #: example: True
    distinctiveRingEnabled: Optional[bool] = None
    #: Information about the number.
    phoneNumbers: Optional[list[GetNumbersPhoneNumbers]] = None


class IncomingPermissionSettingExternalTransfer(str, Enum):
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class IncomingPermissionSetting(ApiModel):
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather than the organizational defaults.
    useCustomEnabled: Optional[bool] = None
    #: Specifies the transfer behavior for incoming, external calls.
    #: example: ALLOW_ALL_EXTERNAL
    externalTransfer: Optional[IncomingPermissionSettingExternalTransfer] = None
    #: Internal calls are allowed to be received.
    #: example: True
    internalCallsEnabled: Optional[bool] = None
    #: Collect calls are allowed to be received.
    #: example: True
    collectCallsEnabled: Optional[bool] = None


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the monitored person, workspace or virtual line.
    #: example: Little
    lastName: Optional[str] = None
    #: First name of the monitored person, workspace or virtual line.
    #: example: Alice
    firstName: Optional[str] = None
    #: Display name of the monitored person, workspace or virtual line.
    #: example: Alice Little
    displayName: Optional[str] = None
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
    callParkNotificationEnabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitoredElements: Optional[list[GetMonitoredElementsObject]] = None


class MonitoringSettingsPut(ApiModel):
    #: Enable or disable call park notification.
    #: example: True
    enableCallParkNotification: Optional[bool] = None
    #: Identifiers of monitored elements whose monitoring settings will be modified.
    #: example: ['Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY']
    monitoredElements: Optional[list[str]] = None


class OutgoingCallingPermissionsSettingCallingPermissionsCallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before the number is dialed.
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
    #: Transfer to Auto Transfer Number 1. The answering person can then approve the call and send it through or reject the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering person can then approve the call and send it through or reject the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering person can then approve the call and send it through or reject the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class OutgoingCallingPermissionsSettingCallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: example: INTERNAL_CALL
    callType: Optional[OutgoingCallingPermissionsSettingCallingPermissionsCallType] = None
    #: Action on the given `callType`.
    #: example: ALLOW
    action: Optional[OutgoingCallingPermissionsSettingCallingPermissionsAction] = None
    #: Allow the person to transfer or forward a call of the specified call type.
    transferEnabled: Optional[bool] = None


class OutgoingCallingPermissionsSetting(ApiModel):
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    #: example: True
    useCustomEnabled: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    callingPermissions: Optional[list[OutgoingCallingPermissionsSettingCallingPermissions]] = None


class PatchCallingBehaviorObject(ApiModel):
    #: The new Calling Behavior setting for the person (case-insensitive). If `null`, the effective Calling Behavior will be the Organization's current default.
    #: example: NATIVE_WEBEX_TEAMS_CALLING
    behaviorType: Optional[GetCallingBehaviorObjectBehaviorType] = None
    #: The UC Manager Profile ID. Specifying null results in the organizational default being applied.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    profileId: Optional[str] = None


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    #: example: True
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    #: example: +12145553567
    directNumber: Optional[str] = None
    #: Extension that is assigned.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Ring Pattern of this number.
    ringPattern: Optional[GetNumbersPhoneNumbersRingPattern] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    #: example: True
    aaExtensionDialingEnabled: Optional[bool] = None
    #: When `true` auto attendant dailing by first or last name will be enabled.
    #: example: True
    aaNamingDialingEnabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    #: example: True
    enablePhoneStatusDirectoryPrivacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoringAgents: Optional[list[MonitoredMemberObject]] = None


class PushToTalkAccessType(str, Enum):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk for can respond.
    two_way = 'TWO_WAY'


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a person receives a Push-to-Talk call and answers the call automatically.
    #: example: True
    allowAutoAnswer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connectionType: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    accessType: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredMemberObject]] = None


class PushToTalkPut(ApiModel):
    #: `true` if Push-to-Talk feature is enabled.
    #: example: True
    allowAutoAnswer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connectionType: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    accessType: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    #: example: ['Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE']
    members: Optional[list[str]] = None


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: Device port number assigned to person or workspace.
    #: example: 1.0
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    #: example: True
    t38FaxCompressionEnabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: true
    primaryOwner: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    lineType: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1.0
    lineWeight: Optional[int] = None
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in `hotlineDestination`.
    #: example: True
    hotlineEnabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    #: example: 1234
    hotlineDestination: Optional[datetime] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all the endpoints on the device. When set to `false`, a call decline request is only declined at the current endpoint.
    #: example: True
    allowCallDeclineEnabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    lineLabel: Optional[str] = None


class PutSharedLineMemberList(ApiModel):
    members: Optional[list[PutSharedLineMemberItem]] = None


class PutAgentCallQueueId(ApiModel):
    #: When true, indicates that this agent is using the `selectedQueue` for its Caller ID. When false, indicates that it is using the agent's configured Caller ID.
    #: example: True
    queueCallerIdEnabled: Optional[bool] = None
    #: Use the queue's caller ID for outgoing calls. Optional when queueCallerIdEnabled is false, required when it's true.
    selectedQueue: Optional[PutAgentCallQueueIdSelectedQueue] = None


class PutEvent(ApiModel):
    #: New name for the event.
    #: example: Central_Zone_Day_Shift
    newName: Optional[str] = None
    #: Name for the event.
    #: example: Day_Shift
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    startDate: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the `allDayEnabled` field is present.
    #: example: 2020-03-18
    endDate: Optional[datetime] = None
    #: Start time of the event in the format of HH:MM (24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 08:00
    startTime: Optional[datetime] = None
    #: End time of the event in the format of HH:MM (24 hours format).  This field is required if the `allDayEnabled` field is false or omitted.
    #: example: 17:00
    endTime: Optional[datetime] = None
    #: True if it is all-day event.
    allDayEnabled: Optional[bool] = None
    #: Recurrance scheme for an event.
    recurrence: Optional[EventLongDetailsRecurrence] = None


class ReceptionInfo(ApiModel):
    #: Set to `true` to enable the Receptionist Client feature.
    #: example: True
    receptionEnabled: Optional[bool] = None
    #: List of people, workspaces or virtual lines to monitor.
    monitoredMembers: Optional[list[MonitoredMemberObject]] = None


class ReceptionPut(ApiModel):
    #: `true` if the Receptionist Client feature is enabled.
    #: example: True
    receptionEnabled: Optional[bool] = None
    #: List of members' unique identifiers to monitor.
    #: example: ['Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE']
    monitoredMembers: Optional[list[str]] = None


class ScheduleType(str, Enum):
    #: Indicates the schedule type that specifies the business or working hours during the day.
    businesshours = 'businessHours'
    #: Indicates the schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class ScheduleCollectionRequest(ApiModel):
    #: Name for the schedule.
    #: example: Dallas_Office_Hours
    name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]] = None


class ScheduleShortDetails(ApiModel):
    #: Identifier for a schedule.
    #: example: Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEUvUkdGc2JHRnpYMDltWm1salpWOUliM1Z5Y3c9PQ
    id: Optional[str] = None
    #: Name for the schedule.
    #: example: Dallas_Office_Hours
    name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None


class ScheduleCollectionResponse(ApiModel):
    #: Indicates a list of schedules.
    schedules: Optional[list[ScheduleShortDetails]] = None


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


class ScheduleUpdateRequest(ApiModel):
    #: New name for the schedule.
    #: example: Richardson_Office_Hours
    newName: Optional[str] = None
    #: Name for the schedule.
    #: example: Dallas_Office_Hours
    name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    type: Optional[ScheduleType] = None
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]] = None


class UserNumbersPatch(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    #: example: True
    enableDistinctiveRingPattern: Optional[bool] = None
    #: List of phone numbers that are assigned to a person.
    phoneNumbers: Optional[list[PhoneNumber]] = None


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    #: example: John Smith
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`, and `user@company.domain`.
    #: example: +12223334444
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9hMTlkODJhMi00ZTY5LTU5YWEtOWYyZi1iY2E2MzEwMTNhNjg=
    personId: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFL2ExOWQ3MWEyLTRlOTItOTFhYi05ZjJmLWJjYTEzNTAxM2ExNA==
    placeId: Optional[str] = None
    #: Indicates whether privacy is enabled for the name, number and `personId`/`placeId`.
    privacyEnabled: Optional[bool] = None


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvNmQ0MTgyMTItZjUwNi00Yzk4LTk5MTItNmI1MmE1ZmU2ODgx
    id: Optional[str] = None
    #: The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    #: example: 38.0
    duration: Optional[int] = None
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the calling party.
    callingParty: Optional[VoiceMailPartyInformation] = None
    #: `true` if the voicemail message is urgent.
    urgent: Optional[bool] = None
    #: `true` if the voicemail message is confidential.
    confidential: Optional[bool] = None
    #: `true` if the voicemail message has been read.
    #: example: True
    read: Optional[bool] = None
    #: Number of pages for the FAX.  Only set for a FAX.
    #: example: 2.0
    faxPageCount: Optional[int] = None
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
    greetingUploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Indicates a custom greeting has been uploaded
    #: example: True
    greetingUploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    #: example: 3.0
    numberOfRings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15.0
    systemMaxNumberOfRings: Optional[int] = None


class VoicemailInfoTransferToNumber(ApiModel):
    #: Indicates enable or disabled state of giving caller option to transfer to destination when pressing zero (0).
    #: example: True
    enabled: Optional[bool] = None
    #: Number voicemail caller will be transferred to when they press zero (0).
    #: example: 6527
    destination: Optional[datetime] = None


class VoicemailInfoEmailCopyOfMessage(ApiModel):
    #: When `true` copy of new voicemail message audio will be sent to the designated email.
    #: example: True
    enabled: Optional[bool] = None
    #: Email address to which the new voicemail audio will be sent.
    #: example: dummy@example.com
    emailId: Optional[str] = None


class VoicemailInfoMessageStorageStorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class VoicemailInfoMessageStorage(ApiModel):
    #: When `true` desktop phone will indicate there are new voicemails.
    #: example: True
    mwiEnabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    #: example: INTERNAL
    storageType: Optional[VoicemailInfoMessageStorageStorageType] = None
    #: External email address to which the new voicemail audio will be sent.  A value for this field must be provided in the request if a `storageType` of `EXTERNAL` is given in the request.
    #: example: dummy@example.com
    externalEmail: Optional[str] = None


class VoicemailInfoFaxMessage(ApiModel):
    #: When `true` FAX messages for new voicemails will be sent to the designated number.
    #: example: True
    enabled: Optional[bool] = None
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage `enabled` field is given as `true` in the request.
    #: example: 2025551212
    phoneNumber: Optional[str] = None
    #: Designates optional extension for the FAX.
    #: example: 1234
    extension: Optional[datetime] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    sendAllCalls: Optional[CallWaitingInfo] = None
    #: Settings for sending calls to voicemail when the line is busy.
    sendBusyCalls: Optional[VoicemailInfoSendBusyCalls] = None
    sendUnansweredCalls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transferToNumber: Optional[VoicemailInfoTransferToNumber] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    emailCopyOfMessage: Optional[VoicemailInfoEmailCopyOfMessage] = None
    messageStorage: Optional[VoicemailInfoMessageStorage] = None
    faxMessage: Optional[VoicemailInfoFaxMessage] = None


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
    #: example: 3.0
    numberOfRings: Optional[int] = None


class VoicemailPut(ApiModel):
    #: Voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    sendAllCalls: Optional[CallWaitingInfo] = None
    #: Settings for sending calls to voicemail when the line is busy.
    sendBusyCalls: Optional[VoicemailPutSendBusyCalls] = None
    sendUnansweredCalls: Optional[VoicemailPutSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transferToNumber: Optional[VoicemailInfoTransferToNumber] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    emailCopyOfMessage: Optional[VoicemailInfoEmailCopyOfMessage] = None
    messageStorage: Optional[VoicemailInfoMessageStorage] = None
    faxMessage: Optional[VoicemailInfoFaxMessage] = None


class Endpoints(ApiModel):
    #: Unique identifier for the endpoint.
    #: example: Y2lzY29z...
    id: Optional[str] = None
    #: Enumeration that indicates if the endpoint is of type `DEVICE` or `APPLICATION`.
    type: Optional[DeviceType] = None
    #: The `name` filed in the response is calculated using device tag. Admins have the ability to set tags for devices. If a `name=<value>` tag is set, for example “name=home phone“, then the `<value>` is included in the `name` field of the API response. In this example “home phone”.
    #: example: Cisco 8865 (Phone in reception area)
    name: Optional[str] = None


class EndpointInformation(ApiModel):
    #: Person’s preferred answer endpoint.
    #: example: Y2lzY29z...
    preferredAnswerEndpointId: Optional[str] = None
    #: Array of endpoints available to the person.
    endpoints: Optional[list[Endpoints]] = None


class NoneType(str, Enum):
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'
