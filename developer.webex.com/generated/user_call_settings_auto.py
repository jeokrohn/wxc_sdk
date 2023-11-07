from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Action', 'Action2', 'AddNewEventForPersonsScheduleResponse', 'Always', 'Announcements', 'Announcements1',
           'AvailableSharedLineMemberItem', 'BehaviorType', 'Busy', 'CallForwarding', 'CallQueueObject', 'CallType',
           'CallerIdSelectedType', 'CallingPermissions', 'Callparkextension',
           'ConfigureCallRecordingSettingsForPersonBody', 'ConfigureCallerIDSettingsForPersonBody',
           'ConfigurepersonsCallingBehaviorBody', 'CreateScheduleForPersonBody', 'CreateScheduleForPersonResponse',
           'DeviceType', 'EffectiveBehaviorType', 'EmailCopyOfMessage', 'Endpoints', 'EventLongDetails',
           'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'FaxMessage', 'FetchEventForpersonsScheduleResponse',
           'GetListOfPhoneNumbersForPersonResponse', 'GetMessageSummaryResponse', 'GetMonitoredElementsObject',
           'GetPreferredAnswerEndpointResponse', 'GetScheduleDetailsResponse',
           'GetSharedLineAppearanceMembersResponse', 'GetSharedLineMemberItem', 'GetpersonsPrivacySettingsResponse',
           'Greeting', 'Incoming', 'LineType', 'ListMessagesResponse', 'ListOfSchedulesForPersonResponse', 'Member',
           'MessageStorage', 'ModifypersonsApplicationServicesSettingsBody', 'MonitoredMemberObject',
           'MonitoredNumberObject', 'MonitoredPersonObject', 'NewNumber', 'NoAnswer', 'Notification', 'Outgoing',
           'PeopleOrPlaceOrVirtualLineType', 'PhoneNumber', 'PhoneNumbers', 'PushToTalkAccessType',
           'PushToTalkConnectionType', 'PutSharedLineMemberItem', 'ReadBargeInSettingsForPersonResponse',
           'ReadCallInterceptSettingsForPersonResponse', 'ReadCallRecordingSettingsForPersonResponse',
           'ReadCallWaitingSettingsForPersonResponse', 'ReadCallerIDSettingsForPersonResponse',
           'ReadDoNotDisturbSettingsForPersonResponse', 'ReadForwardingSettingsForPersonResponse',
           'ReadHotelingSettingsForPersonResponse', 'ReadIncomingPermissionSettingsForPersonResponse',
           'ReadPersonsCallingBehaviorResponse', 'ReadPushtoTalkSettingsForPersonResponse',
           'ReadReceptionistClientSettingsForPersonResponse', 'ReadVoicemailSettingsForPersonResponse', 'Record',
           'RecurWeekly', 'Recurrence', 'Repeat', 'RetrieveCallQueueAgentsCallerIDInformationResponse',
           'RetrieveExecutiveAssistantSettingsForPersonResponse', 'RetrieveListOfCallQueueCallerIDInformationResponse',
           'RetrievepersonsApplicationServicesSettingsResponse', 'RetrievepersonsMonitoringSettingsResponse',
           'RetrievepersonsOutgoingCallingPermissionsSettingsResponse', 'RingPattern', 'ScheduleShortDetails',
           'ScheduleType', 'SearchSharedLineAppearanceMembersResponse', 'SelectedQueue', 'SendAllCalls',
           'SendBusyCalls', 'SendBusyCalls1', 'SendUnansweredCalls', 'StartStopAnnouncement', 'StorageType', 'Type',
           'Type1', 'Type4', 'Type5', 'Type6', 'UpdateEventForpersonsScheduleResponse', 'UpdateScheduleResponse',
           'UserCallSettingsApi', 'UserType', 'VoiceMailPartyInformation', 'VoiceMessageDetails']


class ModifypersonsApplicationServicesSettingsBody(ApiModel):
    #: When true, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool]
    #: When true, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool]
    #: When true, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool]
    #: Indicates that the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool]
    #: Indicates that the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool]
    #: Indicates that the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool]
    #: Indicates that the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool]


class ReadBargeInSettingsForPersonResponse(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    enabled: Optional[bool]
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: Optional[bool]


class NewNumber(ApiModel):
    #: If true, the caller will hear this new number when the call is intercepted.
    enabled: Optional[bool]
    #: New number caller will hear announced.
    destination: Optional[str]


class Always(NewNumber):
    #: If true, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class Busy(NewNumber):
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an
    #: internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class NoAnswer(Busy):
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class CallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person
    #: is busy.
    busy: Optional[Busy]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[NoAnswer]


class ReadForwardingSettingsForPersonResponse(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwarding]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[Busy]


class Type(str, Enum):
    #: Incoming calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class Greeting(str, Enum):
    #: A custom greeting is played when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default greeting will be played when incoming calls are intercepted.
    default = 'DEFAULT'


class Announcements1(ApiModel):
    #: DEFAULT indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[Greeting]
    #: Information about the new number announcement.
    new_number: Optional[NewNumber]
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[NewNumber]


class Announcements(Announcements1):
    #: Filename of custom greeting; will be an empty string if no custom greeting has been uploaded.
    filename: Optional[str]


class Incoming(ApiModel):
    #: INTERCEPT_ALL indicated incoming calls are intercepted.
    type: Optional[Type]
    #: If true, the destination will be the person's voicemail.
    voicemail_enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[Announcements]


class Type1(str, Enum):
    #: Outgoing calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class Outgoing(ApiModel):
    #: INTERCEPT_ALL indicated all outgoing calls are intercepted.
    type: Optional[Type1]
    #: If true, when the person attempts to make an outbound call, a system default message is played and the call is
    #: made to the destination phone number
    transfer_enabled: Optional[bool]
    #: Number to which the outbound call be transferred.
    destination: Optional[str]


class ReadCallInterceptSettingsForPersonResponse(ApiModel):
    #: true if call intercept is enabled.
    enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[Incoming]
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[Outgoing]


class SelectedQueue(ApiModel):
    #: Indicates the Call Queue's unique identifier.
    id: Optional[str]
    #: Indicates the Call Queue's name.
    name: Optional[str]


class CallQueueObject(SelectedQueue):
    #: When not null, indicates the Call Queue's phone number.
    phone_number: Optional[str]
    #: When not null, indicates the Call Queue's extension number.
    extension: Optional[str]


class Record(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (*44) has been entered. Pause, resume, and stop
    #: controls are supported.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class Type5(str, Enum):
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class Type4(Type5):
    #: No notification sound played when call recording is paused or resumed.
    none = 'None'


class Notification(ApiModel):
    #: Type of pause/resume notification.
    type: Optional[Type4]
    #: true when the notification feature is in effect. false indicates notification is disabled.
    enabled: Optional[bool]


class Repeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    interval: Optional[int]
    #: true when ongoing call recording tone will be played at the designated interval. false indicates no warning tone
    #: will be played.
    enabled: Optional[bool]


class StartStopAnnouncement(ApiModel):
    #: When true, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for internal calls.
    internal_calls_enabled: Optional[bool]
    #: When true, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for PSTN calls.
    pstn_calls_enabled: Optional[bool]


class ConfigureCallRecordingSettingsForPersonBody(ApiModel):
    #: true if call recording is enabled.
    enabled: Optional[bool]
    #: Call recording scenario.
    record: Optional[Record]
    #: When true, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool]
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends.
    start_stop_announcement_enabled: Optional[bool]
    #: Pause/resume notification settings.
    notification: Optional[Notification]
    #: Beep sound plays periodically.
    repeat: Optional[Repeat]
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[StartStopAnnouncement]


class CallerIdSelectedType(ApiModel):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line: Optional[str]
    #: Outgoing caller ID will show the main number for the location.
    location_number: Optional[str]
    #: Outgoing caller ID will show the mobile number for this person.
    mobile_number: Optional[str]
    #: Outgoing caller ID will show the value from the customNumber field.
    custom: Optional[str]


class ExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the customExternalCallerIdName field.
    other = 'OTHER'


class ConfigureCallerIDSettingsForPersonBody(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    #: Possible values: DIRECT_LINE
    selected: Optional[CallerIdSelectedType]
    #: This value must be an assigned number from the person's location.
    custom_number: Optional[str]
    #: Person's Caller ID first name. Characters of %, +, ``, " and Unicode characters are not allowed.
    first_name: Optional[str]
    #: Person's Caller ID last name. Characters of %, +, ``, " and Unicode characters are not allowed.
    last_name: Optional[str]
    #: true if person's identity has to be blocked when receiving a transferred or forwarded call.
    block_in_forward_calls_enabled: Optional[bool]
    #: Designates which type of External Caller Id Name policy is used. Default is DIRECT_LINE.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: Person's custom External Caller ID last name. Characters of %, +, ``, " and Unicode characters are not allowed.
    custom_external_caller_id_name: Optional[str]


class EffectiveBehaviorType(str, Enum):
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


class BehaviorType(EffectiveBehaviorType):
    #: Using the non-string value of null results in the organization-wide default calling behavior being in effect.
    null = 'null'


class ConfigurepersonsCallingBehaviorBody(ApiModel):
    #: The new Calling Behavior setting for the person (case-insensitive). If null, the effective Calling Behavior will
    #: be the Organization's current default.
    behavior_type: Optional[BehaviorType]
    #: The UC Manager Profile ID. Specifying null results in the organizational default being applied.
    profile_id: Optional[str]


class ReadDoNotDisturbSettingsForPersonResponse(ApiModel):
    #: true if the Do Not Disturb feature is enabled.
    enabled: Optional[bool]
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: Optional[bool]


class Type6(str, Enum):
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class UserType(ApiModel):
    #: The associated member is a person.
    people: Optional[str]
    #: The associated member is a workspace.
    place: Optional[str]


class PeopleOrPlaceOrVirtualLineType(UserType):
    #: Indicates a virtual line or list of virtual lines.
    virtual_line: Optional[str]


class MonitoredNumberObject(ApiModel):
    #: External phone number of the monitored person, workspace or virtual line.
    external: Optional[str]
    #: Extension number of the monitored person, workspace or virtual line.
    extension: Optional[str]
    #: Indicates whether phone number is a primary number.
    primary: Optional[bool]


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    id: Optional[str]
    #: Last name of the monitored person, workspace or virtual line.
    last_name: Optional[str]
    #: First name of the monitored person, workspace or virtual line.
    first_name: Optional[str]
    #: Display name of the monitored person, workspace or virtual line.
    display_name: Optional[str]
    #: Indicates whether type is person, workspace or virtual line.
    type: Optional[PeopleOrPlaceOrVirtualLineType]
    #: Email address of the monitored person, workspace or virtual line.
    email: Optional[str]
    #: List of phone numbers of the monitored person, workspace or virtual line.
    numbers: Optional[list[MonitoredNumberObject]]


class Member(MonitoredMemberObject):
    #: The location name where the call park extension is.
    location: Optional[str]
    #: The ID for the location.
    location_id: Optional[str]


class Callparkextension(SelectedQueue):
    #: The extension number for the call park extension.
    extension: Optional[str]
    #: The location name where the call park extension is.
    location: Optional[str]
    #: The ID for the location.
    location_id: Optional[str]


class GetMonitoredElementsObject(ApiModel):
    member: Optional[Member]
    callparkextension: Optional[Callparkextension]


class ExternalTransfer(str, Enum):
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class ReadIncomingPermissionSettingsForPersonResponse(ApiModel):
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather
    #: than the organizational defaults.
    use_custom_enabled: Optional[bool]
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: Optional[ExternalTransfer]
    #: Internal calls are allowed to be received.
    internal_calls_enabled: Optional[bool]
    #: Collect calls are allowed to be received.
    collect_calls_enabled: Optional[bool]


class CallType(str, Enum):
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


class Action(str, Enum):
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


class CallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[CallType]
    #: Action on the given callType.
    action: Optional[Action]
    #: Allow the person to transfer or forward a call of the specified call type.
    #: Possible values:
    transfer_enabled: Optional[bool]


class RetrievepersonsOutgoingCallingPermissionsSettingsResponse(ApiModel):
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    use_custom_enabled: Optional[bool]
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[CallingPermissions]]


class RingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a long ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class PhoneNumbers(ApiModel):
    #: Flag to indicate if the number is primary or not.
    #: Possible values:
    primary: Optional[bool]
    #: Phone number.
    #: Possible values: 2143456789
    direct_number: Optional[str]
    #: Extension.
    #: Possible values: 1234
    extension: Optional[str]
    #: Optional ring pattern. Applicable only for alternate numbers.
    ring_pattern: Optional[RingPattern]


class Action2(ApiModel):
    #: Add action.
    add: Optional[str]
    #: Delete action.
    delete: Optional[str]


class PhoneNumber(ApiModel):
    #: If true marks the phone number as primary.
    primary: Optional[bool]
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action2]
    #: Phone numbers that are assigned.
    direct_number: Optional[str]
    #: Extension that is assigned.
    extension: Optional[str]
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern]


class DeviceType(ApiModel):
    #: Indicates the endpoint is a device.
    device: Optional[str]
    #: Indicates the endpoint is a application.
    application: Optional[str]


class Endpoints(SelectedQueue):
    #: Enumeration that indicates if the endpoint is of type DEVICE or APPLICATION.
    type: Optional[DeviceType]


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    id: Optional[str]
    #: Last name of the person.
    last_name: Optional[str]
    #: First name of the person.
    first_name: Optional[str]
    #: Display name of the person.
    display_name: Optional[str]
    #: Type usually indicates PEOPLE, PLACE or VIRTUAL_LINE. Push-to-Talk and Privacy features only supports PEOPLE.
    type: Optional[PeopleOrPlaceOrVirtualLineType]
    #: Email address of the person.
    email: Optional[str]
    #: List of phone numbers of the person.
    numbers: Optional[list[MonitoredNumberObject]]


class PushToTalkConnectionType(ApiModel):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way: Optional[str]
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk
    #: for can respond.
    two_way: Optional[str]


class PushToTalkAccessType(ApiModel):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members: Optional[str]
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members: Optional[str]


class ScheduleType(ApiModel):
    #: Indicates the schedule type that specifies the business or working hours during the day.
    business_hours: Optional[str]
    #: Indicates the schedule type that specifies the day when your organization is not open.
    holidays: Optional[str]


class ScheduleShortDetails(SelectedQueue):
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[ScheduleType]


class RecurWeekly(ApiModel):
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int]
    #: Indicates event occurs weekly on Sunday.
    sunday: Optional[bool]
    #: Indicates event occurs weekly on Monday.
    monday: Optional[bool]
    #: Indicates event occurs weekly on Tuesday.
    tuesday: Optional[bool]
    #: Indicates event occurs weekly on Wednesday.
    wednesday: Optional[bool]
    #: Indicates event occurs weekly on Thursday.
    thursday: Optional[bool]
    #: Indicates event occurs weekly on Friday.
    friday: Optional[bool]
    #: Indicates event occurs weekly on Saturday.
    saturday: Optional[bool]


class Recurrence(ApiModel):
    #: True if the event repeats forever. Requires either recurDaily or recurWeekly to be specified.
    recur_for_ever: Optional[bool]
    #: End date for the recurring event in the format of YYYY-MM-DD. Requires either recurDaily or recurWeekly to be
    #: specified.
    recur_end_date: Optional[str]
    #: End recurrence after the event has repeated the specified number of times. Requires either recurDaily or
    #: recurWeekly to be specified.
    recur_end_occurrence: Optional[int]
    #: Specifies the number of days between the start of each recurrence. Not allowed with recurWeekly.
    #: Recurring interval in days. The number of days after the start when an event will repeat. Repetitions cannot
    #: overlap.
    recur_daily: Optional[object]
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with recurDaily.
    recur_weekly: Optional[RecurWeekly]


class EventLongDetails(ApiModel):
    #: Name for the event.
    name: Optional[str]
    #: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This field is required
    #: if the allDayEnabled field is present.
    start_date: Optional[str]
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This field is required if
    #: the allDayEnabled field is present.
    end_date: Optional[str]
    #: Start time of the event in the format of HH:MM (24 hours format). This field is required if the allDayEnabled
    #: field is false or omitted.
    start_time: Optional[str]
    #: End time of the event in the format of HH:MM (24 hours format). This field is required if the allDayEnabled
    #: field is false or omitted.
    end_time: Optional[str]
    #: True if it is all-day event.
    all_day_enabled: Optional[bool]
    #: Recurrance scheme for an event.
    recurrence: Optional[Recurrence]


class CreateScheduleForPersonBody(ApiModel):
    #: Name for the schedule.
    name: Optional[str]
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[ScheduleType]
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class LineType(ApiModel):
    #: Primary line for the member.
    primary: Optional[str]
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance: Optional[str]


class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    id: Optional[str]
    #: First name of member.
    first_name: Optional[str]
    #: Last name of member.
    last_name: Optional[str]
    #: Phone number of member. Currently, E.164 format is not supported.
    phone_number: Optional[str]
    #: Phone extension of member.
    extension: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[SelectedQueue]


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    id: Optional[str]
    #: Device port number assigned to person or workspace.
    port: Optional[int]
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: If true the person or the workspace is the owner of the device. Points to primary line/port of the device.
    primary_owner: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: Preconfigured number for the hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a device behaves when a call is declined. When set to true, a call decline request is extended to all
    #: the endpoints on the device. When set to false, a call decline request is only declined at the current endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Device line label.
    line_label: Optional[str]


class GetSharedLineMemberItem(PutSharedLineMemberItem):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the
    #: future update.
    phone_number: Optional[str]
    #: Phone extension of a person or workspace.
    extension: Optional[str]
    #: Registration home IP for the line port.
    host_ip: Optional[str]
    #: Registration remote IP for the line port.
    remote_ip: Optional[str]
    #: Indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[UserType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[SelectedQueue]


class SendAllCalls(ApiModel):
    #: All calls will be sent to voicemail.
    enabled: Optional[bool]


class SendBusyCalls1(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool]
    #: DEFAULT indicates the default greeting will be played. CUSTOM indicates a custom .wav file will be played.
    greeting: Optional[Greeting]


class SendBusyCalls(SendBusyCalls1):
    #: Indicates a custom greeting has been uploaded.
    greeting_uploaded: Optional[bool]


class SendUnansweredCalls(SendBusyCalls):
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class EmailCopyOfMessage(ApiModel):
    #: When true copy of new voicemail message audio will be sent to the designated email.
    enabled: Optional[bool]
    #: Email address to which the new voicemail audio will be sent.
    email_id: Optional[str]


class StorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class MessageStorage(ApiModel):
    #: When true desktop phone will indicate there are new voicemails.
    mwi_enabled: Optional[bool]
    #: Designates which type of voicemail message storage is used.
    storage_type: Optional[StorageType]
    #: External email address to which the new voicemail audio will be sent. A value for this field must be provided in
    #: the request if a storageType of EXTERNAL is given in the request.
    external_email: Optional[str]


class FaxMessage(ApiModel):
    #: When true FAX messages for new voicemails will be sent to the designated number.
    enabled: Optional[bool]
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage
    #: enabled field is given as true in the request.
    phone_number: Optional[str]
    #: Designates optional extension for the FAX.
    extension: Optional[str]


class ReadVoicemailSettingsForPersonResponse(ApiModel):
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool]
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[SendAllCalls]
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[SendBusyCalls]
    send_unanswered_calls: Optional[SendUnansweredCalls]
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[NewNumber]
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[NewNumber]
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[EmailCopyOfMessage]
    message_storage: Optional[MessageStorage]
    fax_message: Optional[FaxMessage]


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, *73, and user@company.domain.
    number: Optional[str]
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str]
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str]
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool]


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str]
    #: The duration (in seconds) of the voicemail message. Duration is not present for a FAX message.
    duration: Optional[int]
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation]
    #: true if the voicemail message is urgent.
    urgent: Optional[bool]
    #: true if the voicemail message is confidential.
    confidential: Optional[bool]
    #: true if the voicemail message has been read.
    read: Optional[bool]
    #: Number of pages for the FAX. Only set for a FAX.
    fax_page_count: Optional[int]
    #: The date and time the voicemail message was created.
    created: Optional[str]


class RetrievepersonsApplicationServicesSettingsResponse(ModifypersonsApplicationServicesSettingsBody):
    #: Device ID of WebRTC client. Returns only if browserClientEnabled is true.
    browser_client_id: Optional[str]
    #: Device ID of Desktop client. Returns only if desktopClientEnabled is true.
    desktop_client_id: Optional[str]
    #: Number of available device licenses for assigning devices/apps.
    available_line_count: Optional[int]


class RetrieveListOfCallQueueCallerIDInformationResponse(ApiModel):
    #: Indicates a list of Call Queues that the agent belongs and are available to be selected as the Caller ID for
    #: outgoing calls. It is empty when the agent's Call Queues have disabled the Call Queue outgoing phone number
    #: setting to be used as Caller ID. In the case where this setting is enabled the array will be populated.
    available_queues: Optional[list[CallQueueObject]]


class RetrieveCallQueueAgentsCallerIDInformationResponse(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it
    #: is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when
    #: queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[CallQueueObject]


class ModifyCallQueueAgentsCallerIDInformationBody(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it
    #: is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when
    #: queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[SelectedQueue]


class ReadCallRecordingSettingsForPersonResponse(ConfigureCallRecordingSettingsForPersonBody):
    #: Name of the service provider providing call recording service.
    service_provider: Optional[str]
    #: Group utilized by the service provider providing call recording service.
    external_group: Optional[str]
    #: Unique person identifier utilized by the service provider providing call recording service.
    external_identifier: Optional[str]


class ReadCallWaitingSettingsForPersonResponse(ApiModel):
    #: true if the Call Waiting feature is enabled.
    enabled: Optional[bool]


class ConfigureCallWaitingSettingsForPersonBody(ApiModel):
    #: true if the Call Waiting feature is enabled.
    enabled: Optional[bool]


class ReadCallerIDSettingsForPersonResponse(ConfigureCallerIDSettingsForPersonBody):
    #: Allowed types for the selected field.
    types: Optional[list[CallerIdSelectedType]]
    #: Direct number which will be shown if DIRECT_LINE is selected.
    direct_number: Optional[str]
    #: Extension number which will be shown if DIRECT_LINE is selected.
    extension_number: Optional[str]
    #: Location number which will be shown if LOCATION_NUMBER is selected.
    location_number: Optional[str]
    #: Mobile number which will be shown if MOBILE_NUMBER is selected.
    mobile_number: Optional[str]
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool]
    #: Location's caller ID.
    location_external_caller_id_name: Optional[str]


class ReadPersonsCallingBehaviorResponse(ConfigurepersonsCallingBehaviorBody):
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if
    #: the user's behaviorType is set to null.
    effective_behavior_type: Optional[EffectiveBehaviorType]


class RetrieveExecutiveAssistantSettingsForPersonResponse(ApiModel):
    #: Indicates the Executive Assistant type.
    type: Optional[Type6]


class ModifyExecutiveAssistantSettingsForPersonBody(ApiModel):
    #: executive assistant type
    type: Optional[Type6]


class ReadHotelingSettingsForPersonResponse(ApiModel):
    #: When true, allow this person to connect to a Hoteling host device.
    enabled: Optional[bool]


class ConfigureHotelingSettingsForPersonBody(ApiModel):
    #: When true, allow this person to connect to a Hoteling host device.
    enabled: Optional[bool]


class RetrievepersonsMonitoringSettingsResponse(ApiModel):
    #: Call park notification is enabled or disabled.
    call_park_notification_enabled: Optional[bool]
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[GetMonitoredElementsObject]]


class ModifypersonsMonitoringSettingsBody(ApiModel):
    #: Enable or disable call park notification.
    enable_call_park_notification: Optional[bool]
    #: Identifiers of monitored elements whose monitoring settings will be modified.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
    monitored_elements: Optional[list[str]]


class GetListOfPhoneNumbersForPersonResponse(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    distinctive_ring_enabled: Optional[bool]
    #: Information about the number.
    phone_numbers: Optional[list[PhoneNumbers]]


class AssignOrUnassignNumbersTopersonBody(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    enable_distinctive_ring_pattern: Optional[bool]
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]]


class GetPreferredAnswerEndpointResponse(ApiModel):
    #: Person’s preferred answer endpoint.
    preferred_answer_endpoint_id: Optional[str]
    #: Array of endpoints available to the person.
    endpoints: Optional[list[Endpoints]]


class ModifyPreferredAnswerEndpointBody(ApiModel):
    #: Person’s preferred answer endpoint.
    preferred_answer_endpoint_id: Optional[str]


class GetpersonsPrivacySettingsResponse(ApiModel):
    #: When true auto attendant extension dialing will be enabled.
    aa_extension_dialing_enabled: Optional[bool]
    #: When true auto attendant dailing by first or last name will be enabled.
    aa_naming_dialing_enabled: Optional[bool]
    #: When true phone status directory privacy will be enabled.
    enable_phone_status_directory_privacy: Optional[bool]
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]]


class ConfigurepersonsPrivacySettingsBody(ApiModel):
    #: When true auto attendant extension dialing is enabled.
    aa_extension_dialing_enabled: Optional[bool]
    #: When true auto attendant dailing by first or last name is enabled.
    aa_naming_dialing_enabled: Optional[bool]
    #: When true phone status directory privacy is enabled.
    enable_phone_status_directory_privacy: Optional[bool]
    #: List of monitoring person IDs.
    monitoring_agents: Optional[list[str]]


class ReadPushtoTalkSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Push-to-Talk feature. When enabled, a person receives a Push-to-Talk call and answers
    #: the call automatically.
    allow_auto_answer: Optional[bool]
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType]
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType]
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]]


class ConfigurePushtoTalkSettingsForPersonBody(ApiModel):
    #: true if Push-to-Talk feature is enabled.
    allow_auto_answer: Optional[bool]
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType]
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType]
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    members: Optional[list[str]]


class ReadReceptionistClientSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Receptionist Client feature.
    reception_enabled: Optional[bool]
    #: List of people, workspaces or virtual lines to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]]


class ConfigureReceptionistClientSettingsForPersonBody(ApiModel):
    #: true if the Receptionist Client feature is enabled.
    reception_enabled: Optional[bool]
    #: List of members' unique identifiers to monitor.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    monitored_members: Optional[list[str]]


class ListOfSchedulesForPersonResponse(ApiModel):
    #: Indicates a list of schedules.
    schedules: Optional[list[ScheduleShortDetails]]


class CreateScheduleForPersonResponse(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class GetScheduleDetailsResponse(ScheduleShortDetails):
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class UpdateScheduleBody(CreateScheduleForPersonBody):
    #: New name for the schedule.
    new_name: Optional[str]


class UpdateScheduleResponse(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class FetchEventForpersonsScheduleResponse(EventLongDetails):
    #: Identifier for a event.
    id: Optional[str]


class AddNewEventForPersonsScheduleResponse(ApiModel):
    #: Identifier for a event.
    id: Optional[str]


class UpdateEventForpersonsScheduleBody(EventLongDetails):
    #: New name for the event.
    new_name: Optional[str]


class UpdateEventForpersonsScheduleResponse(ApiModel):
    #: Identifier for a event.
    id: Optional[str]


class SearchSharedLineAppearanceMembersBody(ApiModel):
    #: Number of records per page.
    max: Optional[int]
    #: Page number.
    start: Optional[int]
    #: Location ID for the user.
    location: Optional[str]
    #: Search for users with names that match the query.
    name: Optional[str]
    #: Search for users with numbers that match the query.
    number: Optional[str]
    #: Sort by first name (fname) or last name (lname).
    order: Optional[str]
    #: Search for users with extensions that match the query.
    extension: Optional[str]


class SearchSharedLineAppearanceMembersResponse(ApiModel):
    members: Optional[list[AvailableSharedLineMemberItem]]


class GetSharedLineAppearanceMembersResponse(ApiModel):
    #: Model name of device.
    model: Optional[str]
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]]
    #: Maximum number of device ports.
    max_line_count: Optional[int]


class PutSharedLineAppearanceMembersBody(ApiModel):
    members: Optional[list[PutSharedLineMemberItem]]


class GetMessageSummaryResponse(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int]
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int]
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int]
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int]


class ListMessagesResponse(ApiModel):
    items: Optional[list[VoiceMessageDetails]]


class MarkAsReadBody(ApiModel):
    #: The voicemail message identifier of the message to mark as read. If the messageId is not provided, then all
    #: voicemail messages for the user are marked as read.
    message_id: Optional[str]


class MarkAsUnreadBody(ApiModel):
    #: The voicemail message identifier of the message to mark as unread. If the messageId is not provided, then all
    #: voicemail messages for the user are marked as unread.
    message_id: Optional[str]


class UserCallSettingsApi(ApiChild, base=''):
    """
    Not supported for Webex for Government (FedRAMP)
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    Viewing People requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
    or, for select APIs, a user auth token with spark:people_read scope can be used by a person to read their own
    settings.
    Configuring People settings requires a full or user administrator auth token with the spark-admin:people_write
    scope or, for select APIs, a user auth token with spark:people_write scope can be used by a person to update their
    own settings.
    """

    def retrievepersons_application_services(self, person_id: str, org_id: str = None) -> RetrievepersonsApplicationServicesSettingsResponse:
        """
        Application services let you determine the ringing behavior for calls made to people in certain scenarios. You
        can also specify which devices can download the Webex Calling app.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-a-person's-application-services-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/applications')
        data = super().get(url=url, params=params)
        return RetrievepersonsApplicationServicesSettingsResponse.parse_obj(data)

    def modifypersons_application_services(self, person_id: str, org_id: str = None, ring_devices_for_click_to_dial_calls_enabled: bool = None, ring_devices_for_group_page_enabled: bool = None, ring_devices_for_call_park_enabled: bool = None, browser_client_enabled: bool = None, desktop_client_enabled: bool = None, tablet_client_enabled: bool = None, mobile_client_enabled: bool = None):
        """
        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param ring_devices_for_click_to_dial_calls_enabled: When true, indicates to ring devices for outbound Click to
            Dial calls.
        :type ring_devices_for_click_to_dial_calls_enabled: bool
        :param ring_devices_for_group_page_enabled: When true, indicates to ring devices for inbound Group Pages.
        :type ring_devices_for_group_page_enabled: bool
        :param ring_devices_for_call_park_enabled: When true, indicates to ring devices for Call Park recalled.
        :type ring_devices_for_call_park_enabled: bool
        :param browser_client_enabled: Indicates that the browser Webex Calling application is enabled for use.
        :type browser_client_enabled: bool
        :param desktop_client_enabled: Indicates that the desktop Webex Calling application is enabled for use.
        :type desktop_client_enabled: bool
        :param tablet_client_enabled: Indicates that the tablet Webex Calling application is enabled for use.
        :type tablet_client_enabled: bool
        :param mobile_client_enabled: Indicates that the mobile Webex Calling application is enabled for use.
        :type mobile_client_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-a-person's-application-services-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsApplicationServicesSettingsBody()
        if ring_devices_for_click_to_dial_calls_enabled is not None:
            body.ring_devices_for_click_to_dial_calls_enabled = ring_devices_for_click_to_dial_calls_enabled
        if ring_devices_for_group_page_enabled is not None:
            body.ring_devices_for_group_page_enabled = ring_devices_for_group_page_enabled
        if ring_devices_for_call_park_enabled is not None:
            body.ring_devices_for_call_park_enabled = ring_devices_for_call_park_enabled
        if browser_client_enabled is not None:
            body.browser_client_enabled = browser_client_enabled
        if desktop_client_enabled is not None:
            body.desktop_client_enabled = desktop_client_enabled
        if tablet_client_enabled is not None:
            body.tablet_client_enabled = tablet_client_enabled
        if mobile_client_enabled is not None:
            body.mobile_client_enabled = mobile_client_enabled
        url = self.ep(f'people/{person_id}/features/applications')
        super().put(url=url, params=params, data=body.json())
        return

    def read_barge_in_for_person(self, person_id: str, org_id: str = None) -> ReadBargeInSettingsForPersonResponse:
        """
        Retrieve a person's Barge In settings.
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-barge-in-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/bargeIn')
        data = super().get(url=url, params=params)
        return ReadBargeInSettingsForPersonResponse.parse_obj(data)

    def configure_barge_in_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, tone_enabled: bool = None):
        """
        Configure a person's Barge In settings.
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: Indicates if the Barge In feature is enabled.
        :type enabled: bool
        :param tone_enabled: Indicates that a stutter dial tone will be played when a person is barging in on the
            active call.
        :type tone_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-barge-in-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadBargeInSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if tone_enabled is not None:
            body.tone_enabled = tone_enabled
        url = self.ep(f'people/{person_id}/features/bargeIn')
        super().put(url=url, params=params, data=body.json())
        return

    def read_forwarding_for_person(self, person_id: str, org_id: str = None) -> ReadForwardingSettingsForPersonResponse:
        """
        Retrieve a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-forwarding-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return ReadForwardingSettingsForPersonResponse.parse_obj(data)

    def configure_call_forwarding_for_person(self, person_id: str, org_id: str = None, call_forwarding: CallForwarding = None, business_continuity: Busy = None):
        """
        Configure a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwarding
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: Busy

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-call-forwarding-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadForwardingSettingsForPersonResponse()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        if business_continuity is not None:
            body.business_continuity = business_continuity
        url = self.ep(f'people/{person_id}/features/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def read_call_intercept_for_person(self, person_id: str, org_id: str = None) -> ReadCallInterceptSettingsForPersonResponse:
        """
        Retrieves Person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-call-intercept-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/intercept')
        data = super().get(url=url, params=params)
        return ReadCallInterceptSettingsForPersonResponse.parse_obj(data)

    def configure_call_intercept_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, incoming: Incoming = None, outgoing: Outgoing = None):
        """
        Configures a person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: true if call intercept is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: Incoming
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: Outgoing

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-call-intercept-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadCallInterceptSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if incoming is not None:
            body.incoming = incoming
        if outgoing is not None:
            body.outgoing = outgoing
        url = self.ep(f'people/{person_id}/features/intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def configure_call_intercept_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Call Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-call-intercept-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/intercept/actions/announcementUpload/invoke')
        super().post(url=url, params=params)
        return

    def retrieve_list_of_call_queue_caller_id_information(self, person_id: str) -> list[CallQueueObject]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information.
        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for outgoing
        Caller ID. This API returns a list of Call Queues from which the person must select. If this setting is
        disabled or the Agent does not belong to any queue, this list will be empty.
        This API requires a full admin or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-list-of-call-queue-caller-id-information
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/availableCallerIds')
        data = super().get(url=url)
        return parse_obj_as(list[CallQueueObject], data["availableQueues"])

    def retrieve_call_queue_agents_caller_id_information(self, person_id: str) -> RetrieveCallQueueAgentsCallerIDInformationResponse:
        """
        Retrieve a call queue agent's Caller ID information.
        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone
        number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the
        system.
        This API requires a full admin or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-a-call-queue-agent's-caller-id-information
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        data = super().get(url=url)
        return RetrieveCallQueueAgentsCallerIDInformationResponse.parse_obj(data)

    def modify_call_queue_agents_caller_id_information(self, person_id: str, queue_caller_id_enabled: bool, selected_queue: SelectedQueue):
        """
        Modify a call queue agent's Caller ID information.
        Each Agent in the Call Queue will be able to set their outgoing Caller ID as either the designated Call Queue's
        phone number or their own configured Caller ID. This API modifies the configured Caller ID for the agent in the
        system.
        This API requires a full or user administrator auth token with the spark-admin:telephony_config_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param queue_caller_id_enabled: When true, indicates that this agent is using the selectedQueue for its Caller
            ID. When false, indicates that it is using the agent's configured Caller ID.
        :type queue_caller_id_enabled: bool
        :param selected_queue: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty
            object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
        :type selected_queue: SelectedQueue

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-a-call-queue-agent's-caller-id-information
        """
        body = ModifyCallQueueAgentsCallerIDInformationBody()
        if queue_caller_id_enabled is not None:
            body.queue_caller_id_enabled = queue_caller_id_enabled
        if selected_queue is not None:
            body.selected_queue = selected_queue
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        super().put(url=url, data=body.json())
        return

    def read_call_recording_for_person(self, person_id: str, org_id: str = None) -> ReadCallRecordingSettingsForPersonResponse:
        """
        Retrieve a person's Call Recording settings.
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-call-recording-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callRecording')
        data = super().get(url=url, params=params)
        return ReadCallRecordingSettingsForPersonResponse.parse_obj(data)

    def configure_call_recording_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, record: Record = None, record_voicemail_enabled: bool = None, start_stop_announcement_enabled: bool = None, notification: Notification = None, repeat: Repeat = None, start_stop_announcement: StartStopAnnouncement = None):
        """
        Configure a person's Call Recording settings.
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: true if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: Record
        :param record_voicemail_enabled: When true, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param start_stop_announcement_enabled: When enabled, an announcement is played when call recording starts and
            an announcement is played when call recording ends.
        :type start_stop_announcement_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: Notification
        :param repeat: Beep sound plays periodically.
        :type repeat: Repeat
        :param start_stop_announcement: Call Recording starts and stops announcement settings.
        :type start_stop_announcement: StartStopAnnouncement

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-call-recording-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallRecordingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        if record is not None:
            body.record = record
        if record_voicemail_enabled is not None:
            body.record_voicemail_enabled = record_voicemail_enabled
        if start_stop_announcement_enabled is not None:
            body.start_stop_announcement_enabled = start_stop_announcement_enabled
        if notification is not None:
            body.notification = notification
        if repeat is not None:
            body.repeat = repeat
        if start_stop_announcement is not None:
            body.start_stop_announcement = start_stop_announcement
        url = self.ep(f'people/{person_id}/features/callRecording')
        super().put(url=url, params=params, data=body.json())
        return

    def read_call_waiting_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's Call Waiting settings.
        With this feature, a person can place an active call on hold and answer an incoming call. When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-call-waiting-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_call_waiting_for_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure a person's Call Waiting settings.
        With this feature, a person can place an active call on hold and answer an incoming call. When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-call-waiting-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallWaitingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'people/{person_id}/features/callWaiting')
        super().put(url=url, params=params, data=body.json())
        return

    def read_caller_id_for_person(self, person_id: str, org_id: str = None) -> ReadCallerIDSettingsForPersonResponse:
        """
        Retrieve a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-caller-id-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callerId')
        data = super().get(url=url, params=params)
        return ReadCallerIDSettingsForPersonResponse.parse_obj(data)

    def configure_caller_id_for_person(self, person_id: str, org_id: str = None, selected: CallerIdSelectedType = None, custom_number: str = None, first_name: str = None, last_name: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: ExternalCallerIdNamePolicy = None, custom_external_caller_id_name: str = None):
        """
        Configure a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used. Possible values: DIRECT_LINE
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name. Characters of %, +, ``, " and Unicode characters are not
            allowed.
        :type first_name: str
        :param last_name: Person's Caller ID last name. Characters of %, +, ``, " and Unicode characters are not
            allowed.
        :type last_name: str
        :param block_in_forward_calls_enabled: true if person's identity has to be blocked when receiving a transferred
            or forwarded call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller Id Name policy is used. Default
            is DIRECT_LINE.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Person's custom External Caller ID last name. Characters of %, +, ``, "
            and Unicode characters are not allowed.
        :type custom_external_caller_id_name: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-caller-id-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallerIDSettingsForPersonBody()
        if selected is not None:
            body.selected = selected
        if custom_number is not None:
            body.custom_number = custom_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if block_in_forward_calls_enabled is not None:
            body.block_in_forward_calls_enabled = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body.external_caller_id_name_policy = external_caller_id_name_policy
        if custom_external_caller_id_name is not None:
            body.custom_external_caller_id_name = custom_external_caller_id_name
        url = self.ep(f'people/{person_id}/features/callerId')
        super().put(url=url, params=params, data=body.json())
        return

    def read_persons_calling_behavior(self, person_id: str, org_id: str = None) -> ReadPersonsCallingBehaviorResponse:
        """
        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-person's-calling-behavior
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        data = super().get(url=url, params=params)
        return ReadPersonsCallingBehaviorResponse.parse_obj(data)

    def configurepersons_calling_behavior(self, person_id: str, org_id: str = None, behavior_type: BehaviorType = None, profile_id: str = None):
        """
        Modifies the calling behavior settings for the person which includes calling behavior and UC Manager Profile
        ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param behavior_type: The new Calling Behavior setting for the person (case-insensitive). If null, the
            effective Calling Behavior will be the Organization's current default.
        :type behavior_type: BehaviorType
        :param profile_id: The UC Manager Profile ID. Specifying null results in the organizational default being
            applied.
        :type profile_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-a-person's-calling-behavior
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurepersonsCallingBehaviorBody()
        if behavior_type is not None:
            body.behavior_type = behavior_type
        if profile_id is not None:
            body.profile_id = profile_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        super().put(url=url, params=params, data=body.json())
        return

    def read_do_not_disturb_for_person(self, person_id: str, org_id: str = None) -> ReadDoNotDisturbSettingsForPersonResponse:
        """
        Retrieve a person's Do Not Disturb settings.
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-do-not-disturb-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        data = super().get(url=url, params=params)
        return ReadDoNotDisturbSettingsForPersonResponse.parse_obj(data)

    def configure_do_not_disturb_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, ring_splash_enabled: bool = None):
        """
        Configure a person's Do Not Disturb settings.
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: true if the Do Not Disturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive
            incoming calls.
        :type ring_splash_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-do-not-disturb-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadDoNotDisturbSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if ring_splash_enabled is not None:
            body.ring_splash_enabled = ring_splash_enabled
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_executive_assistant_for_person(self, person_id: str, org_id: str = None) -> Type6:
        """
        Retrieve the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the
        call forward destination and join or leave an executive's pool.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-executive-assistant-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        data = super().get(url=url, params=params)
        return Type6.parse_obj(data["type"])

    def modify_executive_assistant_for_person(self, person_id: str, org_id: str = None, type_: Type6 = None):
        """
        Modify the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the
        call forward destination and join or leave an executive's pool.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param type_: executive assistant type
        :type type_: Type6

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-executive-assistant-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyExecutiveAssistantSettingsForPersonBody()
        if type_ is not None:
            body.type_ = type_
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        super().put(url=url, params=params, data=body.json())
        return

    def read_hoteling_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-hoteling-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/hoteling')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_hoteling_for_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-hoteling-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureHotelingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'people/{person_id}/features/hoteling')
        super().put(url=url, params=params, data=body.json())
        return

    def retrievepersons_monitoring(self, person_id: str, org_id: str = None) -> RetrievepersonsMonitoringSettingsResponse:
        """
        Retrieves the monitoring settings of the person, which shows specified people, places, virtual lines or call
        park extenions that are being monitored.
        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-a-person's-monitoring-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/monitoring')
        data = super().get(url=url, params=params)
        return RetrievepersonsMonitoringSettingsResponse.parse_obj(data)

    def modifypersons_monitoring(self, person_id: str, enable_call_park_notification: bool, monitored_elements: List[str], org_id: str = None):
        """
        Modifies the monitoring settings of the person.
        Monitors the line status of specified people, places, virtual lines or call park extension. The line status
        indicates if a person, place or virtual line is on a call and if a call has been parked on that extension.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
        :type monitored_elements: List[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-a-person's-monitoring-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsMonitoringSettingsBody()
        if enable_call_park_notification is not None:
            body.enable_call_park_notification = enable_call_park_notification
        if monitored_elements is not None:
            body.monitored_elements = monitored_elements
        url = self.ep(f'people/{person_id}/features/monitoring')
        super().put(url=url, params=params, data=body.json())
        return

    def read_incoming_permission_for_person(self, person_id: str, org_id: str = None) -> ReadIncomingPermissionSettingsForPersonResponse:
        """
        Retrieve a person's Incoming Permission settings.
        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-incoming-permission-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        data = super().get(url=url, params=params)
        return ReadIncomingPermissionSettingsForPersonResponse.parse_obj(data)

    def configure_incoming_permission_for_person(self, person_id: str, org_id: str = None, use_custom_enabled: bool = None, external_transfer: ExternalTransfer = None, internal_calls_enabled: bool = None, collect_calls_enabled: bool = None):
        """
        Configure a person's Incoming Permission settings.
        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for
            receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: ExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-incoming-permission-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadIncomingPermissionSettingsForPersonResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if external_transfer is not None:
            body.external_transfer = external_transfer
        if internal_calls_enabled is not None:
            body.internal_calls_enabled = internal_calls_enabled
        if collect_calls_enabled is not None:
            body.collect_calls_enabled = collect_calls_enabled
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrievepersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None) -> RetrievepersonsOutgoingCallingPermissionsSettingsResponse:
        """
        Retrieve a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/retrieve-a-person's-outgoing-calling-permissions-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrievepersonsOutgoingCallingPermissionsSettingsResponse.parse_obj(data)

    def modifypersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None, use_custom_enabled: bool = None, calling_permissions: CallingPermissions = None):
        """
        Modify a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this user uses the specified calling permissions when
            placing outbound calls.
        :type use_custom_enabled: bool
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: CallingPermissions

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-a-person's-outgoing-calling-permissions-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = RetrievepersonsOutgoingCallingPermissionsSettingsResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def list_of_phone_numbers_for_person(self, person_id: str, org_id: str = None, prefer_e164_format: bool = None) -> GetListOfPhoneNumbersForPersonResponse:
        """
        Get a person's phone numbers including alternate numbers.
        A person can have one or more phone numbers and/or extensions via which they can be called.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param prefer_e164_format: Return phone numbers in E.164 format.
        :type prefer_e164_format: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-a-list-of-phone-numbers-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if prefer_e164_format is not None:
            params['preferE164Format'] = str(prefer_e164_format).lower()
        url = self.ep(f'people/{person_id}/features/numbers')
        data = super().get(url=url, params=params)
        return GetListOfPhoneNumbersForPersonResponse.parse_obj(data)

    def assign_or_unassign_numbers_toperson(self, person_id: str, phone_numbers: PhoneNumber, org_id: str = None, enable_distinctive_ring_pattern: bool = None):
        """
        Assign or unassign alternate phone numbers to a person.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.
        Assigning or unassigning an alternate phone number to a person requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.

        :param person_id: Unique identitfier of the person.
        :type person_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: PhoneNumber
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param enable_distinctive_ring_pattern: Enables a distinctive ring pattern for the person.
        :type enable_distinctive_ring_pattern: bool

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/assign-or-unassign-numbers-to-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AssignOrUnassignNumbersTopersonBody()
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if enable_distinctive_ring_pattern is not None:
            body.enable_distinctive_ring_pattern = enable_distinctive_ring_pattern
        url = self.ep(f'telephony/config/people/{person_id}/numbers')
        super().put(url=url, params=params, data=body.json())
        return

    def preferred_answer_endpoint(self, person_id: str, org_id: str = None) -> GetPreferredAnswerEndpointResponse:
        """
        Get the person's preferred answer endpoint (if any) and the list of endpoints available for selection. These
        endpoints can be used by the following Call Control API's that allow the person to specify an endpointId to use
        for the call:
        This API requires spark:telephony_config_read or spark-admin:telephony_config_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-preferred-answer-endpoint
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
        data = super().get(url=url, params=params)
        return GetPreferredAnswerEndpointResponse.parse_obj(data)

    def modify_preferred_answer_endpoint(self, person_id: str, preferred_answer_endpoint_id: str, org_id: str = None):
        """
        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the
        preferredAnswerEndpointId attribute must be set to null.
        This API requires spark:telephony_config_write or spark-admin:telephony_config_write scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param preferred_answer_endpoint_id: Person’s preferred answer endpoint.
        :type preferred_answer_endpoint_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/modify-preferred-answer-endpoint
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyPreferredAnswerEndpointBody()
        if preferred_answer_endpoint_id is not None:
            body.preferred_answer_endpoint_id = preferred_answer_endpoint_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
        super().put(url=url, params=params, data=body.json())
        return

    def getpersons_privacy(self, person_id: str, org_id: str = None) -> GetpersonsPrivacySettingsResponse:
        """
        Get a person's privacy settings for the specified person ID.
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-a-person's-privacy-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/privacy')
        data = super().get(url=url, params=params)
        return GetpersonsPrivacySettingsResponse.parse_obj(data)

    def configurepersons_privacy(self, person_id: str, org_id: str = None, aa_extension_dialing_enabled: bool = None, aa_naming_dialing_enabled: bool = None, enable_phone_status_directory_privacy: bool = None, monitoring_agents: List[str] = None):
        """
        Configure a person's privacy settings for the specified person ID.
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param aa_extension_dialing_enabled: When true auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When true auto attendant dailing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When true phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-a-person's-privacy-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurepersonsPrivacySettingsBody()
        if aa_extension_dialing_enabled is not None:
            body.aa_extension_dialing_enabled = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body.aa_naming_dialing_enabled = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body.enable_phone_status_directory_privacy = enable_phone_status_directory_privacy
        if monitoring_agents is not None:
            body.monitoring_agents = monitoring_agents
        url = self.ep(f'people/{person_id}/features/privacy')
        super().put(url=url, params=params, data=body.json())
        return

    def read_push_to_talk_for_person(self, person_id: str, org_id: str = None) -> ReadPushtoTalkSettingsForPersonResponse:
        """
        Retrieve a person's Push-to-Talk settings.
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-push-to-talk-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        data = super().get(url=url, params=params)
        return ReadPushtoTalkSettingsForPersonResponse.parse_obj(data)

    def configure_push_to_talk_for_person(self, person_id: str, org_id: str = None, allow_auto_answer: bool = None, connection_type: PushToTalkConnectionType = None, access_type: PushToTalkAccessType = None, members: List[str] = None):
        """
        Configure a person's Push-to-Talk settings.
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param allow_auto_answer: true if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
        :type members: List[str]

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-push-to-talk-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurePushtoTalkSettingsForPersonBody()
        if allow_auto_answer is not None:
            body.allow_auto_answer = allow_auto_answer
        if connection_type is not None:
            body.connection_type = connection_type
        if access_type is not None:
            body.access_type = access_type
        if members is not None:
            body.members = members
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        super().put(url=url, params=params, data=body.json())
        return

    def read_receptionist_client_for_person(self, person_id: str, org_id: str = None) -> ReadReceptionistClientSettingsForPersonResponse:
        """
        Retrieve a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-receptionist-client-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/reception')
        data = super().get(url=url, params=params)
        return ReadReceptionistClientSettingsForPersonResponse.parse_obj(data)

    def configure_receptionist_client_for_person(self, person_id: str, reception_enabled: bool, org_id: str = None, monitored_members: List[str] = None):
        """
        Configure a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param reception_enabled: true if the Receptionist Client feature is enabled.
        :type reception_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param monitored_members: List of members' unique identifiers to monitor. Possible values:
            Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
        :type monitored_members: List[str]

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-receptionist-client-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureReceptionistClientSettingsForPersonBody()
        if reception_enabled is not None:
            body.reception_enabled = reception_enabled
        if monitored_members is not None:
            body.monitored_members = monitored_members
        url = self.ep(f'people/{person_id}/features/reception')
        super().put(url=url, params=params, data=body.json())
        return

    def list_of_schedules_for_person(self, person_id: str, org_id: str = None, name: str = None, type_: str = None, **params) -> Generator[ScheduleShortDetails, None, None]:
        """
        List schedules for a person in an organization.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param name: Specifies the case insensitive substring to be matched against the schedule names. The maximum
            length is 40.
        :type name: str
        :param type_: Specifies the schedule event type to be matched on the given type.
        :type type_: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/list-of-schedules-for-a-person
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if type_ is not None:
            params['type'] = type_
        url = self.ep(f'people/{person_id}/features/schedules')
        return self.session.follow_pagination(url=url, model=ScheduleShortDetails, item_key='schedules', params=params)

    def create_schedule_for_person(self, person_id: str, name: str, type_: ScheduleType, org_id: str = None, events: EventLongDetails = None) -> str:
        """
        Create a new schedule for a person.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: ScheduleType
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param events: Indicates a list of events.
        :type events: EventLongDetails

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/create-schedule-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateScheduleForPersonBody()
        if name is not None:
            body.name = name
        if type_ is not None:
            body.type_ = type_
        if events is not None:
            body.events = events
        url = self.ep(f'people/{person_id}/features/schedules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def schedule_details(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, org_id: str = None) -> GetScheduleDetailsResponse:
        """
        Retrieve a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-a-schedule-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url=url, params=params)
        return GetScheduleDetailsResponse.parse_obj(data)

    def update_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, name: str, type_: ScheduleType, new_name: str, org_id: str = None, events: EventLongDetails = None) -> str:
        """
        Modify a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: ScheduleType
        :param new_name: New name for the schedule.
        :type new_name: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param events: Indicates a list of events.
        :type events: EventLongDetails

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/update-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateScheduleBody()
        if name is not None:
            body.name = name
        if type_ is not None:
            body.type_ = type_
        if new_name is not None:
            body.new_name = new_name
        if events is not None:
            body.events = events
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, org_id: str = None):
        """
        Delete a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/delete-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        super().delete(url=url, params=params)
        return

    def fetch_event_forpersons_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, event_id: str, org_id: str = None) -> FetchEventForpersonsScheduleResponse:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/fetch-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().get(url=url, params=params)
        return FetchEventForpersonsScheduleResponse.parse_obj(data)

    def add_new_event_for_persons_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, name: str, start_date: str, end_date: str, start_time: str, end_time: str, org_id: str = None, all_day_enabled: bool = None, recurrence: Recurrence = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format). This field is required if
            the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format). This field is required if the
            allDayEnabled field is false or omitted.
        :type end_time: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: Recurrence

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/add-a-new-event-for-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = EventLongDetails()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_event_forpersons_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, event_id: str, name: str, start_date: str, end_date: str, start_time: str, end_time: str, new_name: str, org_id: str = None, all_day_enabled: bool = None, recurrence: Recurrence = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format). This field is required if
            the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format). This field is required if the
            allDayEnabled field is false or omitted.
        :type end_time: str
        :param new_name: New name for the event.
        :type new_name: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: Recurrence

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/update-an-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateEventForpersonsScheduleBody()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if new_name is not None:
            body.new_name = new_name
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_event_forpersons_schedule(self, person_id: str, schedule_type: ScheduleType, schedule_id: str, event_id: str, org_id: str = None):
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: ScheduleType
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/delete-an-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        super().delete(url=url, params=params)
        return

    def search_shared_line_appearance_members(self, person_id: str, application_id: str, max: int = None, start: int = None, location: str = None, name: str = None, number: str = None, order: str = None, extension: str = None) -> list[AvailableSharedLineMemberItem]:
        """
        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param max: Number of records per page.
        :type max: int
        :param start: Page number.
        :type start: int
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (fname) or last name (lname).
        :type order: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/search-shared-line-appearance-members
        """
        body = SearchSharedLineAppearanceMembersBody()
        if max is not None:
            body.max = max
        if start is not None:
            body.start = start
        if location is not None:
            body.location = location
        if name is not None:
            body.name = name
        if number is not None:
            body.number = number
        if order is not None:
            body.order = order
        if extension is not None:
            body.extension = extension
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/availableMembers')
        data = super().get(url=url, data=body.json())
        return parse_obj_as(list[AvailableSharedLineMemberItem], data["members"])

    def shared_line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineAppearanceMembersResponse:
        """
        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-shared-line-appearance-members
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        data = super().get(url=url)
        return GetSharedLineAppearanceMembersResponse.parse_obj(data)

    def put_shared_line_appearance_members(self, person_id: str, application_id: str, members: PutSharedLineMemberItem = None):
        """
        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param members: 
        :type members: PutSharedLineMemberItem

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/put-shared-line-appearance-members
        """
        body = PutSharedLineAppearanceMembersBody()
        if members is not None:
            body.members = members
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        super().put(url=url, data=body.json())
        return

    def read_voicemail_for_person(self, person_id: str, org_id: str = None) -> ReadVoicemailSettingsForPersonResponse:
        """
        Retrieve a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/read-voicemail-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail')
        data = super().get(url=url, params=params)
        return ReadVoicemailSettingsForPersonResponse.parse_obj(data)

    def configure_voicemail_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, send_all_calls: SendAllCalls = None, send_busy_calls: SendBusyCalls = None, send_unanswered_calls: SendUnansweredCalls = None, notifications: NewNumber = None, transfer_to_number: NewNumber = None, email_copy_of_message: EmailCopyOfMessage = None, message_storage: MessageStorage = None, fax_message: FaxMessage = None):
        """
        Configure a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: SendAllCalls
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: SendBusyCalls
        :param send_unanswered_calls: 
        :type send_unanswered_calls: SendUnansweredCalls
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: NewNumber
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: NewNumber
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: EmailCopyOfMessage
        :param message_storage: 
        :type message_storage: MessageStorage
        :param fax_message: 
        :type fax_message: FaxMessage

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-voicemail-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadVoicemailSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if send_all_calls is not None:
            body.send_all_calls = send_all_calls
        if send_busy_calls is not None:
            body.send_busy_calls = send_busy_calls
        if send_unanswered_calls is not None:
            body.send_unanswered_calls = send_unanswered_calls
        if notifications is not None:
            body.notifications = notifications
        if transfer_to_number is not None:
            body.transfer_to_number = transfer_to_number
        if email_copy_of_message is not None:
            body.email_copy_of_message = email_copy_of_message
        if message_storage is not None:
            body.message_storage = message_storage
        if fax_message is not None:
            body.fax_message = fax_message
        url = self.ep(f'people/{person_id}/features/voicemail')
        super().put(url=url, params=params, data=body.json())
        return

    def configure_busy_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-busy-voicemail-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url=url, params=params)
        return

    def configure_no_answer_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded
        audio file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/configure-no-answer-voicemail-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url=url, params=params)
        return

    def reset_voicemail_pin(self, person_id: str, org_id: str = None):
        """
        Reset a voicemail PIN for a person.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.
        NOTE: This API is expected to have an empty request body and Content-Type header should be set to
        application/json.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/reset-voicemail-pin
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/resetPin/invoke')
        super().post(url=url, params=params)
        return

    def message_summary(self) -> GetMessageSummaryResponse:
        """
        Get a summary of the voicemail messages for the user.

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/get-message-summary
        """
        url = self.ep('telephony/voiceMessages/summary')
        data = super().get(url=url)
        return GetMessageSummaryResponse.parse_obj(data)

    def list_messages(self) -> list[VoiceMessageDetails]:
        """
        Get the list of all voicemail messages for the user.

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/list-messages
        """
        url = self.ep('telephony/voiceMessages')
        data = super().get(url=url)
        return parse_obj_as(list[VoiceMessageDetails], data["items"])

    def delete_message(self, message_id: str):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/delete-message
        """
        url = self.ep(f'telephony/voiceMessages/{message_id}')
        super().delete(url=url)
        return

    def mark_as_read(self, message_id: str = None):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read. Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read. If the messageId is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/mark-as-read
        """
        body = MarkAsReadBody()
        if message_id is not None:
            body.message_id = message_id
        url = self.ep('telephony/voiceMessages/markAsRead')
        super().post(url=url, data=body.json())
        return

    def mark_as_unread(self, message_id: str = None):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread. Otherwise, all messages for the user are
        marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread. If the messageId is not
            provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/user-call-settings/mark-as-unread
        """
        body = MarkAsUnreadBody()
        if message_id is not None:
            body.message_id = message_id
        url = self.ep('telephony/voiceMessages/markAsUnread')
        super().post(url=url, data=body.json())
        return
