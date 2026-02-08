from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AddressObject', 'AgentACDStateType', 'Assistant', 'AvailableAssistant', 'BargeInInfo',
           'CallForwardingInfo', 'CallForwardingInfoCallForwarding', 'CallForwardingInfoCallForwardingAlways',
           'CallForwardingInfoCallForwardingBusy', 'CallForwardingInfoCallForwardingNoAnswer',
           'CallForwardingPutCallForwarding', 'CallForwardingPutCallForwardingNoAnswer', 'CallParkMember',
           'CallPickupGroupMember', 'CallPickupGroupSettingsGet', 'CallQueueGet', 'CallQueuePut',
           'CallQueueSettingsGetResponseObject', 'CallSettingsForMe12Api', 'CallerIdSettingsGet', 'CallerIdType',
           'DeviceActivationState', 'DeviceType', 'DeviceTypeObject', 'DoNotDisturbGet', 'Endpoint',
           'EndpointMobilitySettings', 'EndpointType', 'Endpoints', 'Executive', 'ExecutiveAlertGet',
           'ExecutiveAlertGetAlertingMode', 'ExecutiveAlertGetClidNameMode', 'ExecutiveAlertGetClidPhoneNumberMode',
           'ExecutiveAlertGetRolloverAction', 'ExecutiveAssignedAssistantsGet', 'ExecutiveAssistantSettingsGet',
           'ExecutiveCallFilteringCriteriaGet', 'ExecutiveCallFilteringCriteriaGetCallsToNumbersItem',
           'ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType',
           'ExecutiveCallFilteringCriteriaGetScheduleLevel', 'ExecutiveCallFilteringCriteriaGetScheduleType',
           'ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem',
           'ExecutiveCallFilteringCriteriaPatchCallsToNumbersItemType', 'ExecutiveCallFilteringGet',
           'ExecutiveCallFilteringGetCriteriaItem', 'ExecutiveCallFilteringGetCriteriaItemSource',
           'ExecutiveCallFilteringGetFilterType', 'ExecutiveCallFilteringPatchCriteriaActivationItem', 'ExecutivePut',
           'ExecutiveScreeningGet', 'ExecutiveScreeningGetAlertType', 'FeatureAccessCode',
           'GetAnnouncementLanguagesForMeResponseLanguagesItem', 'GetCountryTelephonyConfigRequirementsResponse',
           'GetSingleNumberReachObject', 'GetUserCallCaptionsObject', 'HostObject', 'Location', 'LocationObject',
           'MemberType', 'ModifyEndpointObjectMobilitySettings', 'MonitoredElementItem', 'MonitoredElementItemType',
           'MonitoringSettingsGetResponseObject', 'Numbers', 'OwnerObject', 'PauseResumeNotifyMethodType',
           'PersonalAssistantGet', 'PersonalAssistantGetAlerting', 'PersonalAssistantGetPresence',
           'PreferredAnswerEndpoint', 'RecordingModeType', 'SecondaryLine', 'SelectedCallerIdSettingsGetSelected',
           'SelectedCallerIdSettingsPutSelected', 'ServicesEnum', 'SingleNumberReachNumber',
           'UserCallParkSettingsGetResponseObject', 'UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls',
           'UserCallRecordingGetResponseObject', 'UserCallRecordingGetResponseObjectVendor', 'UserDevice',
           'UserNumber', 'UserProfileGetResponseObject', 'VoicemailInfo', 'VoicemailInfoEmailCopyOfMessage',
           'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage', 'VoicemailInfoMessageStorageStorageType',
           'VoicemailInfoNotifications', 'VoicemailInfoSendAllCalls', 'VoicemailInfoSendBusyCalls',
           'VoicemailInfoSendBusyCallsAudioFile', 'VoicemailInfoSendBusyCallsGreeting',
           'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls', 'VoicemailPutSendUnansweredCalls']


class AgentACDStateType(str, Enum):
    #: Agent has signed in.
    sign_in = 'SIGN_IN'
    #: Agent has signed out.
    sign_out = 'SIGN_OUT'
    #: Agent is available.
    available = 'AVAILABLE'
    #: Agent is unavailable.
    unavailable = 'UNAVAILABLE'
    #: Agent has wrapped up.
    wrap_up = 'WRAP_UP'


class CallQueuePut(ApiModel):
    #: Unique call queue identifier.
    id: Optional[str] = None
    #: When `true`, the agent has joined the call center.
    available: Optional[bool] = None


class CallQueueGet(ApiModel):
    #: Unique call queue identifier.
    id: Optional[str] = None
    #: Indicates if the call queue is `normal` or `CxEssentials`.
    has_cx_essentials: Optional[bool] = None
    #: When `true` it indicates agent has joined the call center.
    available: Optional[bool] = None
    #: Call center skill level.
    skill_level: Optional[int] = None
    #: Call center phone number.
    phone_number: Optional[str] = None
    #: Call center extension.
    extension: Optional[str] = None
    #: Determines whether a queue can be joined or not.
    allow_log_off_enabled: Optional[bool] = None


class CallQueueSettingsGetResponseObject(ApiModel):
    agent_acdstate: Optional[AgentACDStateType] = Field(alias='agentACDState', default=None)
    #: Indicates a list of call centers the agent has joined or may join.
    queues: Optional[list[CallQueueGet]] = None


class MonitoredElementItemType(str, Enum):
    #: The monitored element is a user.
    people = 'PEOPLE'
    #: The monitored element is a workspace.
    place = 'PLACE'
    #: The monitored element is a virtual line.
    virtual_line = 'VIRTUAL_LINE'
    #: The monitored element is a call park extension.
    call_park_extension = 'CALL_PARK_EXTENSION'


class MonitoredElementItem(ApiModel):
    #: The identifier of the monitored person.
    id: Optional[str] = None
    #: The last name of the monitored person or virtual line.
    last_name: Optional[str] = None
    #: The first name of the monitored person or virtual line.
    first_name: Optional[str] = None
    #: The display name of the monitored place or call park extension.
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE`, `VIRTUAL_LINE` or `CALL_PARK_EXTENSION`.
    type: Optional[MonitoredElementItemType] = None
    #: The email address of the monitored person, place or virtual line.
    email: Optional[str] = None
    #: The list of phone numbers of the monitored person, place or virtual line.
    direct_number: Optional[str] = None
    #: The extension number for the person, place, virtual line or call park extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Numbers (Routing prefix + extension of a person, place, virtual line).
    esn: Optional[str] = None
    #: The location name where the monitored item is.
    location_name: Optional[str] = None
    #: The ID for the location.
    location_id: Optional[str] = None


class MonitoringSettingsGetResponseObject(ApiModel):
    #: Call park notification is enabled or disabled. Only applies to monitored users, workspaces, and virtual lines.
    #: Does not apply to call park extensions.
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[MonitoredElementItem]] = None


class Numbers(ApiModel):
    #: Unique identifier of the phone number.
    id: Optional[str] = None
    #: Phone number which is blocked by user.
    phone_number: Optional[str] = None


class VoicemailInfoSendAllCalls(ApiModel):
    #: All calls will be sent to voicemail.
    enabled: Optional[bool] = None


class VoicemailInfoSendBusyCallsGreeting(str, Enum):
    #: The default greeting will be played.
    default = 'DEFAULT'
    #: Designates that a custom file will be played.
    custom = 'CUSTOM'


class VoicemailInfoSendBusyCallsAudioFile(ApiModel):
    #: File name of the custom greeting uploaded.
    name: Optional[str] = None
    #: Media type of the custom greeting uploaded. Supported media types are `WAV` and `MP3`.
    media_type: Optional[str] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom file will be played.
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: A custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None
    audio_file: Optional[VoicemailInfoSendBusyCallsAudioFile] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates custom file will be played.
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: A custom greeting has been uploaded
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None
    audio_file: Optional[VoicemailInfoSendBusyCallsAudioFile] = None


class VoicemailInfoNotifications(ApiModel):
    #: Send of unanswered calls to voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: Email address to which the notification will be sent. For text messages, use an email to text message gateway
    #: like `2025551212@txt.example.net`.
    destination: Optional[str] = None


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
    send_all_calls: Optional[VoicemailInfoSendAllCalls] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailInfoSendBusyCalls] = None
    #: Settings for sending unanswered calls to voicemail.
    send_unanswered_calls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[VoicemailInfoNotifications] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[VoicemailInfoNotifications] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailInfoEmailCopyOfMessage] = None
    #: Settings for voicemail message storage.
    message_storage: Optional[VoicemailInfoMessageStorage] = None
    #: Settings for sending FAX messages for new voicemails.
    fax_message: Optional[VoicemailInfoFaxMessage] = None
    #: Disable the user-level control when set to "false".
    voice_message_forwarding_enabled: Optional[bool] = None


class VoicemailPutSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom file will be played.
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom file will be played.
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None


class MemberType(str, Enum):
    #: Endpoint owner or secondary line member is a workspace.
    place = 'PLACE'
    #: Endpoint owner or secondary line member is a person.
    people = 'PEOPLE'
    #: Endpoint owner or secondary line member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class CallParkMember(ApiModel):
    #: Unique identifier of the member.
    id: Optional[str] = None
    type: Optional[MemberType] = None
    #: First name of the member.
    first_name: Optional[str] = None
    #: Last name of the member.
    last_name: Optional[str] = None
    #: Display name of the member.
    display_name: Optional[str] = None


class UserCallParkSettingsGetResponseObject(ApiModel):
    #: Unique name for the call park. The maximum length is 80..
    group_name: Optional[str] = None
    #: List of members in the call park group.
    member_list: Optional[list[CallParkMember]] = None


class CallPickupGroupMember(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str] = None
    type: Optional[MemberType] = None
    #: First name of the member.
    first_name: Optional[str] = None
    #: Last name of the member.
    last_name: Optional[str] = None
    #: Department name of the member.
    department_name: Optional[str] = None
    #: Direct number of the member.
    direct_number: Optional[str] = None
    #: Extension of the member.
    extension: Optional[str] = None
    #: Email address of the member.
    email: Optional[str] = None


class CallPickupGroupSettingsGet(ApiModel):
    #: Name of the call pickup group.
    group_name: Optional[str] = None
    #: List of members in the call pickup group.
    member_list: Optional[list[CallPickupGroupMember]] = None


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
    #: Destination for "No Answer" call forwarding. The minimum length is 2, maximum length is 30.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
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


class SingleNumberReachNumber(ApiModel):
    #: Phone number.
    phone_number: Optional[str] = None
    #: Name associated with the phone number.
    name: Optional[str] = None
    #: If `true`, the phone number is enabled.
    enabled: Optional[bool] = None
    #: If `true`, calls are not forwarded.
    do_not_forward_calls_enabled: Optional[bool] = None
    #: If `true`, answer confirmation is enabled.
    answer_confirmation_enabled: Optional[bool] = None


class GetSingleNumberReachObject(ApiModel):
    #: If `true`, the Single Number Reach feature is enabled.
    enabled: Optional[bool] = None
    #: If `true`, all locations will be alerted for click-to-dial calls.
    alert_all_locations_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: If `true`, all locations will be alerted for group paging calls.
    alert_all_locations_for_group_paging_calls_enabled: Optional[bool] = None
    #: List of numbers configured for Single Number Reach.
    numbers: Optional[list[SingleNumberReachNumber]] = None


class ServicesEnum(str, Enum):
    #: When enabled, blocks all incoming calls from unidentified or blocked caller IDs.
    anonymous_call_rejection = 'Anonymous Call Rejection'
    #: Requires the user to enter a password before making a call.
    authentication = 'Authentication'
    #: Forwards all incoming calls to another number.
    call_forwarding_always = 'Call Forwarding Always'
    #: Forwards incoming calls to another number when the user is on another call.
    call_forwarding_busy = 'Call Forwarding Busy'
    #: Forwards incoming calls to another number when the user does not answer.
    call_forwarding_no_answer = 'Call Forwarding No Answer'
    #: Notifies the user of incoming calls.
    call_notify = 'Call Notify'
    #: Blocks the delivery of the user's caller ID to the recipient.
    calling_line_id_delivery_blocking = 'Calling Line ID Delivery Blocking'
    #: Blocks all incoming calls.
    do_not_disturb = 'Do Not Disturb'
    #: Allows the user to intercept another user's calls.
    intercept_user = 'Intercept User'
    #: Redials the last number called.
    last_number_redial = 'Last Number Redial'
    #: Alerts the user of incoming calls with a distinctive ring.
    priority_alert = 'Priority Alert'
    #: Returns the last call received.
    call_return = 'Call Return'
    #: Accepts only calls from a list of pre-approved numbers.
    selective_call_acceptance = 'Selective Call Acceptance'
    #: Forwards calls from a list of pre-approved numbers.
    call_forwarding_selective = 'Call Forwarding Selective'
    #: Rejects calls from a list of pre-approved numbers.
    selective_call_rejection = 'Selective Call Rejection'
    #: Rings multiple numbers at the same time.
    simultaneous_ring_personal = 'Simultaneous Ring Personal'
    #: Allows the user to access voicemail.
    voice_messaging_user = 'Voice Messaging User'
    #: Allows the user to have multiple numbers.
    alternate_numbers = 'Alternate Numbers'
    #: Allows the user to share a call appearance with another user.
    shared_call_appearance_35 = 'Shared Call Appearance 35'
    #: Allows the user to dial a number by pressing a single key.
    speed_dial_100 = 'Speed Dial 100'
    #: Allows the user to pick up a call directed to another user.
    directed_call_pickup = 'Directed Call Pickup'
    #: Allows the user to pick up a call directed to another user and join the call.
    directed_call_pickup_with_barge_in = 'Directed Call Pickup with Barge-in'
    #: Displays the caller's ID on the user's phone.
    external_calling_line_id_delivery = 'External Calling Line ID Delivery'
    #: Displays the caller's ID on the user's phone.
    internal_calling_line_id_delivery = 'Internal Calling Line ID Delivery'
    #: Alerts the user of incoming calls when they are on another call.
    call_waiting = 'Call Waiting'
    #: Prevents other users from barging in on the user's calls.
    barge_in_exempt = 'Barge-in Exempt'
    #: Allows the user to push a button to talk.
    push_to_talk = 'Push to Talk'
    #: Logs the user's call history.
    basic_call_logs = 'Basic Call Logs'
    #: Allows the user to host a hoteling session.
    hoteling_host = 'Hoteling Host'
    #: Allows the user to join a hoteling session.
    hoteling_guest = 'Hoteling Guest'
    #: Allows the user to have multiple calls at the same time.
    multiple_call_arrangement = 'Multiple Call Arrangement'
    #: Allows the user to monitor the status of another user's phone.
    busy_lamp_field = 'Busy Lamp Field'
    #: Allows the user to have a three-way call.
    three_way_call = 'Three-Way Call'
    #: Allows the user to transfer a call.
    call_transfer = 'Call Transfer'
    #: Allows the user to keep their number private.
    privacy = 'Privacy'
    #: Allows the user to send and receive faxes.
    fax_messaging = 'Fax Messaging'
    #: Allows the user to have an N-way call.
    n_way_call = 'N-Way Call'
    #: Forwards calls when the user is not reachable.
    call_forwarding_not_reachable = 'Call Forwarding Not Reachable'
    #: Displays the caller's ID on the user's phone.
    connected_line_identification_presentation = 'Connected Line Identification Presentation'
    #: Prevents the caller's ID from being displayed on the user's phone.
    connected_line_identification_restriction = 'Connected Line Identification Restriction'
    #: Allows the user to make calls from any phone.
    broad_works_anywhere = 'BroadWorks Anywhere'
    #: Allows the user to listen to music while on hold.
    music_on_hold_user = 'Music On Hold User'
    #: Allows the user to monitor a call center.
    call_center_monitoring = 'Call Center Monitoring'
    #: Allows the user to use BroadWorks Mobility.
    broad_works_mobility = 'BroadWorks Mobility'
    #: Allows the user to record calls.
    call_recording = 'Call Recording'
    #: Allows the user to have an executive assistant.
    executive = 'Executive'
    #: Allows the user to use client license 17.
    client_license_17 = 'Client License 17'
    #: Allows the user to use client license 18.
    client_license_18 = 'Client License 18'
    #: Allows the user to be a flexible seating guest.
    flexible_seating_guest = 'Flexible Seating Guest'
    #: Allows the user to have a personal assistant.
    personal_assistant = 'Personal Assistant'
    #: Allows the user to have a sequential ring.
    sequential_ring = 'Sequential Ring'
    #: Allows the user to block calls.
    call_block = 'Call Block'


class Executive(ApiModel):
    #: Unique identifier of the executive.
    id: Optional[str] = None
    #: First name of the executive.
    first_name: Optional[str] = None
    #: Last name of the executive.
    last_name: Optional[str] = None
    #: Direct number of the executive.
    direct_number: Optional[str] = None
    #: Extension number of the executive.
    extension: Optional[str] = None
    #: If `true`, the executive assistant opted in to the executive pool.
    opt_in_enabled: Optional[bool] = None


class ExecutiveAssistantSettingsGet(ApiModel):
    #: If `true`, the executive assistant forwards filtered calls to the forward to phone number.
    forward_filtered_calls_enabled: Optional[bool] = None
    #: Phone number to forward calls to.
    forward_to_phone_number: Optional[str] = None
    #: List of assigned executives.
    executives: Optional[list[Executive]] = None


class ExecutivePut(ApiModel):
    #: Unique identifier of the executive.
    person_id: Optional[str] = None
    #: If `true`, the executive assistant can opt in to the executive assistant pool.
    opt_in_enabled: Optional[bool] = None


class AvailableAssistant(ApiModel):
    #: Unique identifier of the assistant.
    id: Optional[str] = None
    #: First name of the assistant.
    first_name: Optional[str] = None
    #: Last name of the assistant.
    last_name: Optional[str] = None
    #: Direct number of the assistant.
    direct_number: Optional[str] = None
    #: Extension number of the assistant.
    extension: Optional[str] = None


class Location(ApiModel):
    #: Name of the location.
    name: Optional[str] = None
    #: Unique identifier of the location.
    id: Optional[str] = None


class Assistant(ApiModel):
    #: Unique identifier of the assistant.
    id: Optional[str] = None
    #: First name of the assistant.
    first_name: Optional[str] = None
    #: Last name of the assistant.
    last_name: Optional[str] = None
    #: Direct number of the assistant.
    direct_number: Optional[str] = None
    #: Extension number of the assistant.
    extension: Optional[str] = None
    #: If `true`, the assistant can opt in to the executive assistant pool.
    opt_in_enabled: Optional[bool] = None
    location: Optional[Location] = None


class ExecutiveAssignedAssistantsGet(ApiModel):
    #: If `true`, the user can opt in or out of the executive assistant pool.
    allow_opt_in_out_enabled: Optional[bool] = None
    #: List of assigned executive assistants.
    assistants: Optional[list[Assistant]] = None


class FeatureAccessCode(ApiModel):
    #: Feature Access Code name.
    name: Optional[str] = None
    #: Feature Access Code.
    code: Optional[str] = None
    #: Alternate Code for the Feature Access Code.
    alternate_code: Optional[str] = None


class EndpointType(str, Enum):
    #: Endpoint is a calling device.
    calling_device = 'CALLING_DEVICE'
    #: Endpoint is an application.
    application = 'APPLICATION'
    #: Endpoint is a hotdesking guest.
    hotdesking_guest = 'HOTDESKING_GUEST'


class SecondaryLine(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str] = None
    member_type: Optional[MemberType] = None


class EndpointMobilitySettings(ApiModel):
    #: Phone number of the mobile device endpoint.
    phone_number: Optional[str] = None
    #: If `true`, alerting is enabled for the endpoint.
    alerting_enabled: Optional[bool] = None


class HostObject(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    type: Optional[EndpointType] = None
    #: Name of the endpoint.
    name: Optional[str] = None
    #: If `true`, the endpoint can be remotely controlled, allowing actions such as mute, hold, resume and answer.
    auto_and_forced_answer_enabled: Optional[bool] = None
    #: Unique identifier of the endpoint owner.
    owner_id: Optional[str] = None
    owner_type: Optional[MemberType] = None
    #: List of secondary lines. The secondary line information is not returned for the endpoint owned by an entity
    #: other than the authenticated user.
    secondary_lines: Optional[list[SecondaryLine]] = None


class Endpoint(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    type: Optional[EndpointType] = None
    #: Display name of the endpoint.
    name: Optional[str] = None
    #: If `true`, the endpoint can be remotely controlled, allowing actions such as mute, hold, resume and answer.
    auto_and_forced_answer_enabled: Optional[bool] = None
    #: Unique identifier of the endpoint owner.
    owner_id: Optional[str] = None
    owner_type: Optional[MemberType] = None
    #: List of secondary lines. The secondary line information is not returned for the endpoint owned by an entity
    #: other than the authenticated user.
    secondary_lines: Optional[list[SecondaryLine]] = None
    #: Mobility settings of the endpoint.
    mobility_settings: Optional[EndpointMobilitySettings] = None
    host: Optional[HostObject] = None


class ModifyEndpointObjectMobilitySettings(ApiModel):
    #: If `true`, alerting is enabled for the endpoint.
    alerting_enabled: Optional[bool] = None


class UserCallRecordingGetResponseObjectVendor(ApiModel):
    #: Unique identifier of a vendor.
    id: Optional[str] = None
    #: Name of a call recording vendor.
    name: Optional[str] = None
    #: Login URL of the vendor.
    login_url: Optional[str] = None


class RecordingModeType(str, Enum):
    #: Call recording is always enabled.
    always = 'Always'
    #: Call recording is never enabled.
    never = 'Never'
    #: Call recording is started and stopped manually by the user.
    on_demand = 'On Demand'
    #: Call recording is always enabled with the ability to pause and resume.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Call recording is started manually by the user.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class PauseResumeNotifyMethodType(str, Enum):
    #: A beep is played when call recording is paused or resumed.
    beep = 'Beep'
    #: An announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class UserCallRecordingGetResponseObject(ApiModel):
    #: Indicates whether Call Recording is enabled for the user or not.
    enabled: Optional[bool] = None
    #: List of available vendors and their details.
    vendor: Optional[UserCallRecordingGetResponseObjectVendor] = None
    recording_mode: Optional[RecordingModeType] = None
    pause_resume_notify_method: Optional[PauseResumeNotifyMethodType] = None
    #: If `true`, an announcement is played when call recording starts.
    announcement_enabled: Optional[bool] = None
    #: If `true`, a warning tone is played when call recording starts.
    warning_tone_enabled: Optional[bool] = None
    #: Duration of the warning tone in seconds. Duration can be configured between 10 and 1800 seconds.
    warning_tone_duration: Optional[int] = None


class UserNumber(ApiModel):
    #: Direct number of the user.
    direct_number: Optional[str] = None
    #: Enterprise number of the user. This always combines the location routing prefix with the user's extension, and
    #: is only present when both are present. That is, the location has a routing prefix and the user has an
    #: extension.
    enterprise: Optional[str] = None
    #: Extension of the user. This is always the user's extension, only present if the user has an extension.
    extension: Optional[str] = None
    #: Routing prefix of the user.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Number. This combines the location routing prefix and extension when both are set, and
    #: only the extension when the location routing prefix is not set. if the extension is not set, the esn is not
    #: present.
    esn: Optional[str] = None
    #: Indicates if the number is primary or alternate number.
    primary: Optional[bool] = None


class DeviceTypeObject(str, Enum):
    #: Primary line for the user.
    primary = 'PRIMARY'
    #: Shared line for the user. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'
    #: Device is a shared line.
    mobility = 'MOBILITY'


class OwnerObject(ApiModel):
    #: First name of device owner.
    last_name: Optional[str] = None
    #: Last name of device owner.
    first_name: Optional[str] = None
    type: Optional[MemberType] = None


class DeviceActivationState(str, Enum):
    #: Device is activating using an activation code.
    activating = 'ACTIVATING'
    #: Device has been activated using an activation code.
    activated = 'ACTIVATED'
    #: Device has not been activated using an activation code.
    deactivated = 'DEACTIVATED'


class UserDevice(ApiModel):
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of the device.
    mac: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    type: Optional[DeviceTypeObject] = None
    owner: Optional[OwnerObject] = None
    activation_state: Optional[DeviceActivationState] = None


class AddressObject(ApiModel):
    #: Address line 1.
    address1: Optional[str] = None
    #: Address line 2.
    address2: Optional[str] = None
    #: City.
    city: Optional[str] = None
    #: State.
    state: Optional[str] = None
    #: Postal code.
    postal_code: Optional[str] = None
    #: Country.
    country: Optional[str] = None


class LocationObject(ApiModel):
    #: Name of the location.
    name: Optional[str] = None
    address: Optional[AddressObject] = None


class UserProfileGetResponseObject(ApiModel):
    #: Unique identifier of the user.
    id: Optional[str] = None
    #: Last name of the user.
    last_name: Optional[str] = None
    #: First name of the user.
    first_name: Optional[str] = None
    #: The email addresses of the person.
    email: Optional[str] = None
    #: Language for announcements.
    announcement_language: Optional[str] = None
    #: Dialing code for the user's location.
    location_dialing_code: Optional[str] = None
    #: If `true`, the user supports mobility.
    support_mobility: Optional[bool] = None
    #: Emergency callback number for the user.
    emergency_call_back_number: Optional[str] = None
    #: List of numbers associated with the user.
    phone_numbers: Optional[list[UserNumber]] = None
    #: List of devices associated with the user.
    devices: Optional[list[UserDevice]] = None
    location: Optional[LocationObject] = None
    #: URL for the receptionist console.
    receptionist_url: Optional[str] = None
    #: URL for the calling host.
    calling_host_url: Optional[str] = None
    #: URL for the attendant console.
    attendant_console_url: Optional[str] = None


class PersonalAssistantGetPresence(str, Enum):
    #: User is available.
    none_ = 'NONE'
    #: User is gone for a business trip.
    business_trip = 'BUSINESS_TRIP'
    #: User is gone for the day.
    gone_for_the_day = 'GONE_FOR_THE_DAY'
    #: User is gone for lunch.
    lunch = 'LUNCH'
    #: User is gone for a meeting.
    meeting = 'MEETING'
    #: User is out of office.
    out_of_office = 'OUT_OF_OFFICE'
    #: User is temporarily out.
    temporarily_out = 'TEMPORARILY_OUT'
    #: User is gone for training.
    training = 'TRAINING'
    #: User is unavailable.
    unavailable = 'UNAVAILABLE'
    #: User is gone for vacation.
    vacation = 'VACATION'


class PersonalAssistantGetAlerting(str, Enum):
    #: Ring the recipient first.
    alert_me_first = 'ALERT_ME_FIRST'
    #: Reminder ring the recipient.
    play_ring_reminder = 'PLAY_RING_REMINDER'
    #: No alert.
    none_ = 'NONE'


class PersonalAssistantGet(ApiModel):
    #: Toggles feature.
    enabled: Optional[bool] = None
    #: Person's availability.
    presence: Optional[PersonalAssistantGetPresence] = None
    #: The date until which personal assistant is active.
    until_date_time: Optional[datetime] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Number to transfer to.
    transfer_number: Optional[str] = None
    #: Alert type.
    alerting: Optional[PersonalAssistantGetAlerting] = None
    #: Number of rings for alert type: `ALERT_ME_FIRST`; available range is 2-20
    alert_me_first_number_of_rings: Optional[int] = None


class DeviceType(str, Enum):
    #: The endpoint is a device.
    device = 'DEVICE'
    #: The endpoint is an application.
    application = 'APPLICATION'
    #: The endpoint is a hot desking guest device..
    hotdesking_guest = 'HOTDESKING_GUEST'


class Endpoints(ApiModel):
    #: Unique identifier for the endpoint.
    id: Optional[str] = None
    type: Optional[DeviceType] = None
    #: The `name` field in the response is calculated using device tag. Admins have the ability to set tags for
    #: devices. If a `name=<value>` tag is set, for example “name=home phone“, then the `<value>` is included in the
    #: `name` field of the API response. In this example “home phone”.
    name: Optional[str] = None
    #: Indicates if this endpoint has been set as the preferred answer endpoint.
    is_preferred_answer_endpoint: Optional[bool] = None


class PreferredAnswerEndpoint(ApiModel):
    #: Unique identifier for the endpoint.
    id: Optional[str] = None
    type: Optional[DeviceType] = None
    #: The name field is either set to `Webex Desktop Application` or consists of the device model followed by the
    #: device tag in parentheses. For example, when the name is `Cisco 8865 (Phone in reception area)`, `Cisco 8865`
    #: is the device model and `Phone in reception area` is the device tag.
    name: Optional[str] = None


class CallerIdSettingsGet(ApiModel):
    #: If `true`, the user's name and phone number are not shown to people they call.
    calling_line_id_delivery_blocking_enabled: Optional[bool] = None
    #: If `true`, the user's name and phone number are not shown when receiving a call.
    connected_line_identification_restriction_enabled: Optional[bool] = None


class CallerIdType(str, Enum):
    #: Caller ID is the default configured caller ID.
    default_clid = 'DEFAULT_CLID'
    #: Caller ID is an additional number caller ID.
    additional_clid = 'ADDITIONAL_CLID'
    #: Caller ID is associated with a call queue.
    call_queue = 'CALL_QUEUE'
    #: Caller ID is associated with a hunt group.
    hunt_group = 'HUNT_GROUP'


class SelectedCallerIdSettingsGetSelected(ApiModel):
    type: Optional[CallerIdType] = None
    #: Unique identifier of the selected caller ID config. Set for `CALL_QUEUE` & `HUNT_GROUP` caller IDs.
    id: Optional[str] = None
    #: Name of the selected caller ID.
    name: Optional[str] = None
    #: Direct number of the selected caller ID.
    direct_number: Optional[str] = None
    #: Extension of the selected caller ID.
    extension: Optional[str] = None


class SelectedCallerIdSettingsPutSelected(ApiModel):
    type: Optional[CallerIdType] = None
    #: Unique identifier of the selected caller ID config. Mandatory when setting `CALL_QUEUE` or `HUNT_GROUP` caller
    #: IDs.
    id: Optional[str] = None
    #: Direct number of the selected caller ID. Mandatory when setting ADDITIONAL_CLID caller ID.
    direct_number: Optional[str] = None


class UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls(str, Enum):
    #: Caller sees the final destination's identity when call is redirected.
    no_privacy = 'NO_PRIVACY'
    #: Internal callers see the final destination's identity; external callers see the original recipient's identity.
    privacy_for_external_calls = 'PRIVACY_FOR_EXTERNAL_CALLS'
    #: All callers see the original recipient's identity when call is redirected.
    privacy_for_all_calls = 'PRIVACY_FOR_ALL_CALLS'


class ExecutiveScreeningGetAlertType(str, Enum):
    #: No audible alert is provided for executive screening.
    silent = 'SILENT'
    #: A short ring (splash) is used as an alert for executive screening.
    ring_splash = 'RING_SPLASH'


class ExecutiveScreeningGet(ApiModel):
    #: Indicates if executive screening is enabled.
    enabled: Optional[bool] = None
    #: * `SILENT` - No audible alert is provided for executive screening.
    alert_type: Optional[ExecutiveScreeningGetAlertType] = None
    #: Indicates if alerts are enabled for Single Number Reach locations.
    alert_anywhere_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Webex Go locations.
    alert_mobility_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Shared Call Appearance locations.
    alert_shared_call_appearance_location_enabled: Optional[bool] = None


class ExecutiveCallFilteringGetFilterType(str, Enum):
    #: Choose this option to ensure only specific calls are sent to the executive assistant.
    custom_call_filters = 'CUSTOM_CALL_FILTERS'
    #: Choose this option to send both internal and external calls to the executive assistant.
    all_calls = 'ALL_CALLS'
    #: Choose this option to send all the internal calls to the executive assistant.
    all_internal_calls = 'ALL_INTERNAL_CALLS'
    #: Choose this option to send all the external calls to the executive assistant.
    all_external_calls = 'ALL_EXTERNAL_CALLS'


class ExecutiveCallFilteringGetCriteriaItemSource(str, Enum):
    #: The criteria applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The criteria applies to selected phone numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The criteria applies to any internal number.
    any_internal = 'ANY_INTERNAL'
    #: The criteria applies to any external number.
    any_external = 'ANY_EXTERNAL'


class ExecutiveCallFilteringGetCriteriaItem(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    #: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
    source: Optional[ExecutiveCallFilteringGetCriteriaItemSource] = None
    #: Controls whether this filter criteria is active. When `true`, the criteria is evaluated for incoming calls. When
    #: `false`, the criteria is completely ignored and has no effect on call filtering.
    activation_enabled: Optional[bool] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered (blocked). When
    #: `false`, matching calls are allowed through and take precedence over other filtering criteria, creating
    #: exceptions to let specific calls through.
    filter_enabled: Optional[bool] = None


class ExecutiveCallFilteringGet(ApiModel):
    #: Indicates if executive call filtering is enabled.
    enabled: Optional[bool] = None
    #: * `CUSTOM_CALL_FILTERS` - Choose this option to ensure only specific calls are sent to the executive assistant.
    filter_type: Optional[ExecutiveCallFilteringGetFilterType] = None
    #: List of call filtering criteria configured for executive call filtering.
    criteria: Optional[list[ExecutiveCallFilteringGetCriteriaItem]] = None


class ExecutiveCallFilteringPatchCriteriaActivationItem(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Controls whether this filter criteria is active. When `true`, the criteria is evaluated for incoming calls. When
    #: `false`, the criteria is completely ignored and has no effect on call filtering.
    activation_enabled: Optional[bool] = None


class ExecutiveCallFilteringCriteriaGetScheduleType(str, Enum):
    #: The schedule is based on specific times.
    holidays = 'holidays'
    #: The schedule is based on a duration of time.
    business_hours = 'businessHours'


class ExecutiveCallFilteringCriteriaGetScheduleLevel(str, Enum):
    #: The schedule applies to the individual user.
    people = 'PEOPLE'
    #: The schedule applies at the account level, potentially affecting multiple users.
    location = 'LOCATION'


class ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType(str, Enum):
    #: Primary number to call.
    primary = 'PRIMARY'
    #: Secondary number to call, if available.
    secondary = 'SECONDARY'


class ExecutiveCallFilteringCriteriaGetCallsToNumbersItem(ApiModel):
    #: * `PRIMARY` - Primary number to call.
    type: Optional[ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType] = None
    #: The phone number to call.
    phone_number: Optional[str] = None


class ExecutiveCallFilteringCriteriaGet(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    #: Name of the schedule associated with this criteria.
    schedule_name: Optional[str] = None
    #: * `holidays` - The schedule is based on specific times.
    schedule_type: Optional[ExecutiveCallFilteringCriteriaGetScheduleType] = None
    #: * `PEOPLE` - The schedule applies to the individual user.
    schedule_level: Optional[ExecutiveCallFilteringCriteriaGetScheduleLevel] = None
    #: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
    calls_from: Optional[ExecutiveCallFilteringGetCriteriaItemSource] = None
    #: Indicates if the criteria applies to anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: Indicates if the criteria applies to unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers that this filtering criteria applies to.
    phone_numbers: Optional[list[str]] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered (blocked). When
    #: `false`, matching calls are allowed through and take precedence over other filtering criteria, creating
    #: exceptions to let specific calls through.
    filter_enabled: Optional[bool] = None
    #: List of phone numbers to route calls to when this criteria matches.
    calls_to_numbers: Optional[list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]] = None


class ExecutiveCallFilteringCriteriaPatchCallsToNumbersItemType(str, Enum):
    #: Primary number to call.
    primary = 'PRIMARY'
    #: Alternate number to call, if available.
    alternate = 'ALTERNATE'


class ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem(ApiModel):
    #: * `PRIMARY` - Primary number to call.
    type: Optional[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItemType] = None
    #: The phone number to call.
    phone_number: Optional[str] = None


class ExecutiveAlertGetAlertingMode(str, Enum):
    #: Alerts assistants one at a time in the defined order.
    sequential = 'SEQUENTIAL'
    #: Alerts all assistants at the same time.
    simultaneous = 'SIMULTANEOUS'


class ExecutiveAlertGetRolloverAction(str, Enum):
    voice_messaging = 'VOICE_MESSAGING'
    no_answer_processing = 'NO_ANSWER_PROCESSING'
    forward = 'FORWARD'


class ExecutiveAlertGetClidNameMode(str, Enum):
    #: Display executive name followed by caller name.
    executive_originator = 'EXECUTIVE_ORIGINATOR'
    #: Display caller name followed by executive name.
    originator_executive = 'ORIGINATOR_EXECUTIVE'
    #: Display only executive name.
    executive = 'EXECUTIVE'
    #: Display only caller name.
    originator = 'ORIGINATOR'
    #: Display a custom name.
    custom = 'CUSTOM'


class ExecutiveAlertGetClidPhoneNumberMode(str, Enum):
    #: Display executive's phone number.
    executive = 'EXECUTIVE'
    #: Display caller's phone number.
    originator = 'ORIGINATOR'
    #: Display a custom phone number.
    custom = 'CUSTOM'


class ExecutiveAlertGet(ApiModel):
    #: * `SEQUENTIAL` - Alerts assistants one at a time in the defined order.
    alerting_mode: Optional[ExecutiveAlertGetAlertingMode] = None
    #: Number of rings before alerting the next assistant when in sequential mode.
    next_assistant_number_of_rings: Optional[int] = None
    #: Controls whether the rollover timer (`rolloverWaitTimeInSecs`) is enabled. When set to `true`, rollover will
    #: trigger after the timer expires, even if assistants are still available. When `false`, rollover only occurs
    #: when no assistants remain.
    rollover_enabled: Optional[bool] = None
    #: Specifies what happens when rollover is triggered:
    #: - VOICE_MESSAGING: Send to Voicemail—A voicemail is sent to the executive.
    #: - FORWARD: Forward—Calls are forwarded to a specified number.
    #: - NO_ANSWER_PROCESSING: Do nothing—No action is taken.
    #: Rollover is always triggered when no assistants remain for a filtered call. If the rollover timer is enabled,
    #: rollover can also be triggered when the timer expires, even if assistants are still available.
    rollover_action: Optional[ExecutiveAlertGetRolloverAction] = None
    #: Phone number to forward calls to when rollover action is set to FORWARD.
    rollover_forward_to_phone_number: Optional[str] = None
    #: Time in seconds to wait before applying the rollover action.
    rollover_wait_time_in_secs: Optional[int] = None
    #: * `EXECUTIVE_ORIGINATOR` - Display executive name followed by caller name.
    clid_name_mode: Optional[ExecutiveAlertGetClidNameMode] = None
    #: Custom caller ID name to display (deprecated).
    custom_clidname: Optional[str] = Field(alias='customCLIDName', default=None)
    #: Custom caller ID name in Unicode format.
    custom_clidname_in_unicode: Optional[str] = Field(alias='customCLIDNameInUnicode', default=None)
    #: * `EXECUTIVE` - Display executive's phone number.
    clid_phone_number_mode: Optional[ExecutiveAlertGetClidPhoneNumberMode] = None
    #: Custom caller ID phone number to display.
    custom_clidphone_number: Optional[str] = Field(alias='customCLIDPhoneNumber', default=None)


class BargeInInfo(ApiModel):
    #: If true, this user allows other users to barge in on their active calls.
    enabled: Optional[bool] = None
    #: Set to enable or disable a stutter dial tone when this user initiates a barge-in on an active call.
    tone_enabled: Optional[bool] = None


class DoNotDisturbGet(ApiModel):
    #: Indicates if Do Not Disturb is enabled.
    enabled: Optional[bool] = None
    #: Indicates if ring splash is enabled while DND is active.
    ring_splash_enabled: Optional[bool] = None
    #: Indicates if Webex Go override is enabled while DND is active.
    webex_go_override_enabled: Optional[bool] = None


class GetUserCallCaptionsObject(ApiModel):
    #: User closed captions are enabled or disabled.
    user_closed_captions_enabled: Optional[bool] = None
    #: User transcripts are enabled or disabled.
    user_transcripts_enabled: Optional[bool] = None


class GetAnnouncementLanguagesForMeResponseLanguagesItem(ApiModel):
    #: Language Name
    name: Optional[str] = None
    #: Language Code
    code: Optional[str] = None


class GetCountryTelephonyConfigRequirementsResponse(ApiModel):
    #: If `stateRequired` should be a Mandatory field in UI
    state_required: Optional[bool] = None
    #: If `zipCodeRequired` should be a Mandatory field in UI
    zip_code_required: Optional[bool] = None
    states: Optional[list[GetAnnouncementLanguagesForMeResponseLanguagesItem]] = None
    #: List of supported timezones for the country.
    time_zones: Optional[list[str]] = None


class CallSettingsForMe12Api(ApiChild, base='telephony/config/people/me'):
    """
    Call Settings For Me (1/2)
    
    Call settings for me APIs allow a person to read or modify their settings.
    
    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.
    
    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """

    def get_my_own_details(self) -> UserProfileGetResponseObject:
        """
        Get My Own Details

        Get profile details for the authenticated user.

        Profile details include the user's name, email, location and calling details.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`UserProfileGetResponseObject`
        """
        url = self.ep()
        data = super().get(url)
        r = UserProfileGetResponseObject.model_validate(data)
        return r

    def get_announcement_languages_for_me(self) -> list[GetAnnouncementLanguagesForMeResponseLanguagesItem]:
        """
        Get announcement languages for the authenticated user

        Retrieve the list of available announcement languages for the authenticated user's telephony configuration.

        Announcement languages determine the language used for system prompts and announcements during calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[GetAnnouncementLanguagesForMeResponseLanguagesItem]
        """
        url = self.ep('announcementLanguages')
        data = super().get(url)
        r = TypeAdapter(list[GetAnnouncementLanguagesForMeResponseLanguagesItem]).validate_python(data['languages'])
        return r

    def get_country_telephony_config_requirements(self,
                                                  country_code: str) -> GetCountryTelephonyConfigRequirementsResponse:
        """
        Get country-specific telephony configuration requirements

        Retrieve country-specific telephony configuration requirements for the authenticated user.

        Webex Calling supports multiple regions and time zones to validate and present the information using the local
        date and time, as well as localized dialing rules.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param country_code: The ISO country code for which configuration requirements are requested.
        :type country_code: str
        :rtype: :class:`GetCountryTelephonyConfigRequirementsResponse`
        """
        url = self.ep(f'countries/{country_code}')
        data = super().get(url)
        r = GetCountryTelephonyConfigRequirementsResponse.model_validate(data)
        return r

    def get_my_endpoints_list(self) -> list[Endpoint]:
        """
        Read the List of My Endpoints

        Retrieve the list of endpoints associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[Endpoint]
        """
        url = self.ep('endpoints')
        data = super().get(url)
        r = TypeAdapter(list[Endpoint]).validate_python(data['endpoints'])
        return r

    def get_my_endpoint_details(self, endpoint_id: str) -> Endpoint:
        """
        Get My Endpoints Details

        Get details of an endpoint associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param endpoint_id: Unique identifier of the endpoint.
        :type endpoint_id: str
        :rtype: :class:`Endpoint`
        """
        url = self.ep(f'endpoints/{endpoint_id}')
        data = super().get(url)
        r = Endpoint.model_validate(data)
        return r

    def modify_my_endpoint_details(self, endpoint_id: str, mobility_settings: ModifyEndpointObjectMobilitySettings):
        """
        Modify My Endpoints Details

        Update alerting settings of the mobility endpoint associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param endpoint_id: Unique identifier of the endpoint.
        :type endpoint_id: str
        :param mobility_settings: Mobility settings of the endpoint.
        :type mobility_settings: ModifyEndpointObjectMobilitySettings
        :rtype: None
        """
        body = dict()
        body['mobilitySettings'] = mobility_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'endpoints/{endpoint_id}')
        super().put(url, json=body)

    def get_my_available_caller_idlist(self) -> list[SelectedCallerIdSettingsGetSelected]:
        """
        Get My Available Caller ID List

        Get details of available caller IDs of the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        The available caller ID list shows the caller IDs that the user can choose from.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[SelectedCallerIdSettingsGetSelected]
        """
        url = self.ep('settings/availableCallerIds')
        data = super().get(url)
        r = TypeAdapter(list[SelectedCallerIdSettingsGetSelected]).validate_python(data['availableCallerIds'])
        return r

    def get_list_available_preferred_answer_endpoints(self) -> list[Endpoints]:
        """
        Get List Available Preferred Answer Endpoints

        Get the person's preferred answer endpoint and the list of endpoints available for selection. The list of
        endpoints is empty if the person has no endpoints assigned which support the preferred answer endpoint
        functionality.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[Endpoints]
        """
        url = self.ep('settings/availablePreferredAnswerEndpoints')
        data = super().get(url)
        r = TypeAdapter(list[Endpoints]).validate_python(data['endpoints'])
        return r

    def get_barge_in_settings(self) -> BargeInInfo:
        """
        Get Barge-In Settings

        Retrieve Barge-In settings of the user.

        The Barge-In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge-In can be used across locations.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`BargeInInfo`
        """
        url = self.ep('settings/bargeIn')
        data = super().get(url)
        r = BargeInInfo.model_validate(data)
        return r

    def configure_barge_in_settings(self, enabled: bool = None, tone_enabled: bool = None):
        """
        Configure Barge-In Settings

        Configure person's Barge-In settings.

        The Barge-In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge-In can be used across locations.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: If true, this user allows other users to barge in on their active calls.
        :type enabled: bool
        :param tone_enabled: Set to enable or disable a stutter dial tone when this user initiates a barge-in on an
            active call.
        :type tone_enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep('settings/bargeIn')
        super().put(url, json=body)

    def get_my_call_block_settings(self) -> list[Numbers]:
        """
        Get My Call Block Settings

        Get details of call block settings associated with the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[Numbers]
        """
        url = self.ep('settings/callBlock')
        data = super().get(url)
        r = TypeAdapter(list[Numbers]).validate_python(data['numbers'])
        return r

    def add_phone_number_to_my_call_block_list(self, phone_number: str) -> str:
        """
        Add a phone number to user's Call Block List

        Add a phone number to the call block list for the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number: Phone number which is blocked by user.
        :type phone_number: str
        :rtype: str
        """
        body = dict()
        body['phoneNumber'] = phone_number
        url = self.ep('settings/callBlock/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_call_block_number(self, phone_number_id: str):
        """
        Delete User Call Block Number

        Delete call block number settings associated with the authenticated user.

        Call block settings allow you to delete a number from the User Call Block Number List.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: None
        """
        url = self.ep(f'settings/callBlock/numbers/{phone_number_id}')
        super().delete(url)

    def get_my_call_block_state_for_aspecific_number(self, phone_number_id: str) -> bool:
        """
        Get My Call Block State For Specific Number

        Get call block state details for a specific number associated with the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: bool
        """
        url = self.ep(f'settings/callBlock/numbers/{phone_number_id}')
        data = super().get(url)
        r = data['blockCallsEnabled']
        return r

    def get_my_call_captions_settings(self) -> GetUserCallCaptionsObject:
        """
        Get my call captions settings

        Retrieve the effective call captions settings of the authenticated user.

        **NOTE**: The call captions feature is not supported for Webex Calling Standard users or users assigned to
        locations in India.

        The call caption feature allows the customer to enable and manage closed captions and transcript functionality
        (rolling caption panel) in Webex Calling, without requiring the user to escalate the call to a meeting.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`GetUserCallCaptionsObject`
        """
        url = self.ep('settings/callCaptions')
        data = super().get(url)
        r = GetUserCallCaptionsObject.model_validate(data)
        return r

    def get_my_call_forwarding_settings(self) -> CallForwardingInfo:
        """
        Read My Call Forwarding Settings

        Read call forwarding settings associated with the authenticated user.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallForwardingInfo`
        """
        url = self.ep('settings/callForwarding')
        data = super().get(url)
        r = CallForwardingInfo.model_validate(data)
        return r

    def modify_my_call_forwarding_settings(self, call_forwarding: CallForwardingPutCallForwarding = None,
                                           business_continuity: CallForwardingInfoCallForwardingBusy = None):
        """
        Configure My Call Forwarding Settings

        Update call forwarding settings associated with the authenticated user.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwardingPutCallForwarding
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingInfoCallForwardingBusy
        :rtype: None
        """
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        if business_continuity is not None:
            body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/callForwarding')
        super().put(url, json=body)

    def get_my_call_park_settings(self) -> UserCallParkSettingsGetResponseObject:
        """
        Get My Call Park Settings

        Get details of call park settings associated with the authenticated user.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`UserCallParkSettingsGetResponseObject`
        """
        url = self.ep('settings/callPark')
        data = super().get(url)
        r = UserCallParkSettingsGetResponseObject.model_validate(data)
        return r

    def get_my_call_pickup_group_settings(self) -> CallPickupGroupSettingsGet:
        """
        Get My Call Pickup Group Settings

        Get Call Pickup Group Settings for the authenticated user.

        Call pickup group enables a user to answer any ringing line within their pickup group. A call pickup group is
        an administrator-defined set of users within a location, to which the call pickup feature applies.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallPickupGroupSettingsGet`
        """
        url = self.ep('settings/callPickupGroup')
        data = super().get(url)
        r = CallPickupGroupSettingsGet.model_validate(data)
        return r

    def get_my_call_policies_settings(self) -> UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls:
        """
        Get Call Policies Settings for User

        Get call policies settings for the authenticated user.

        Call Policies in Webex allow you to manage how your call information is displayed and handled. You can view
        privacy settings for your connected line ID on redirected calls and review other call-related preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        """
        url = self.ep('settings/callPolicies')
        data = super().get(url)
        r = UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls.model_validate(data['connectedLineIdPrivacyOnRedirectedCalls'])
        return r

    def update_my_call_policies_settings(self,
                                         connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls = None):
        """
        Modify Call Policies Settings for User

        Update call policies settings for the authenticated user.

        Call Policies in Webex allow you to manage how your call information is displayed and handled. You can
        configure privacy settings for your connected line ID on redirected calls and control other call-related
        preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param connected_line_id_privacy_on_redirected_calls: * `NO_PRIVACY` - Caller sees the final destination's
            identity when call is redirected.
        :type connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        :rtype: None
        """
        body = dict()
        if connected_line_id_privacy_on_redirected_calls is not None:
            body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.ep('settings/callPolicies')
        super().put(url, json=body)

    def get_my_call_recording_settings(self) -> UserCallRecordingGetResponseObject:
        """
        Get My Call Recording Settings

        Get details of call recording settings associated with the authenticated user.

        Call recording settings allow you to access and customize options that determine when and how your calls are
        recorded, providing control over recording modes and notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`UserCallRecordingGetResponseObject`
        """
        url = self.ep('settings/callRecording')
        data = super().get(url)
        r = UserCallRecordingGetResponseObject.model_validate(data)
        return r

    def get_my_caller_idsettings(self) -> CallerIdSettingsGet:
        """
        Get My Caller ID Settings

        Get Caller ID Settings for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallerIdSettingsGet`
        """
        url = self.ep('settings/callerId')
        data = super().get(url)
        r = CallerIdSettingsGet.model_validate(data)
        return r

    def modify_my_caller_idsettings(self, calling_line_id_delivery_blocking_enabled: bool = None,
                                    connected_line_identification_restriction_enabled: bool = None):
        """
        Modify My Caller ID Settings

        Update Caller ID Settings for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param calling_line_id_delivery_blocking_enabled: If `true`, the user's name and phone number are not shown to
            people they call.
        :type calling_line_id_delivery_blocking_enabled: bool
        :param connected_line_identification_restriction_enabled: If `true`, the user's name and phone number are not
            shown when receiving a call.
        :type connected_line_identification_restriction_enabled: bool
        :rtype: None
        """
        body = dict()
        if calling_line_id_delivery_blocking_enabled is not None:
            body['callingLineIdDeliveryBlockingEnabled'] = calling_line_id_delivery_blocking_enabled
        if connected_line_identification_restriction_enabled is not None:
            body['connectedLineIdentificationRestrictionEnabled'] = connected_line_identification_restriction_enabled
        url = self.ep('settings/callerId')
        super().put(url, json=body)

    def get_my_do_not_disturb_settings(self) -> DoNotDisturbGet:
        """
        Get Do Not Disturb Settings for User

        Get Do Not Disturb settings for the authenticated user.

        Do Not Disturb (DND) enables users to block or silence incoming calls on their phone. When activated, the phone
        either stops ringing or rejects calls depending on the configured option, but users can still see call
        information and answer calls if desired.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`DoNotDisturbGet`
        """
        url = self.ep('settings/doNotDisturb')
        data = super().get(url)
        r = DoNotDisturbGet.model_validate(data)
        return r

    def update_my_do_not_disturb_settings(self, enabled: bool = None, ring_splash_enabled: bool = None,
                                          webex_go_override_enabled: bool = None):
        """
        Modify Do Not Disturb Settings for User

        Update Do Not Disturb settings for the authenticated user.

        Do Not Disturb (DND) enables users to block or silence incoming calls on their phone. When activated, the phone
        either stops ringing or rejects calls depending on the configured option, but users can still see call
        information and answer calls if desired.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Set to enable or disable Do Not Disturb.
        :type enabled: bool
        :param ring_splash_enabled: Set to enable or disable ring splash while DND is active.
        :type ring_splash_enabled: bool
        :param webex_go_override_enabled: Set to enable or disable Webex Go override while DND is active.
        :type webex_go_override_enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if ring_splash_enabled is not None:
            body['ringSplashEnabled'] = ring_splash_enabled
        if webex_go_override_enabled is not None:
            body['webexGoOverrideEnabled'] = webex_go_override_enabled
        url = self.ep('settings/doNotDisturb')
        super().put(url, json=body)

    def get_my_executive_alert_settings(self) -> ExecutiveAlertGet:
        """
        Get User Executive Alert Settings

        Get executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecutiveAlertGet`
        """
        url = self.ep('settings/executive/alert')
        data = super().get(url)
        r = ExecutiveAlertGet.model_validate(data)
        return r

    def update_my_executive_alert_settings(self, alerting_mode: ExecutiveAlertGetAlertingMode = None,
                                           next_assistant_number_of_rings: int = None, rollover_enabled: bool = None,
                                           rollover_action: ExecutiveAlertGetRolloverAction = None,
                                           rollover_forward_to_phone_number: str = None,
                                           rollover_wait_time_in_secs: int = None,
                                           clid_name_mode: ExecutiveAlertGetClidNameMode = None,
                                           custom_clidname: str = None, custom_clidname_in_unicode: str = None,
                                           clid_phone_number_mode: ExecutiveAlertGetClidPhoneNumberMode = None,
                                           custom_clidphone_number: str = None):
        """
        Modify User Executive Alert Settings

        Update executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param alerting_mode: * `SEQUENTIAL` - Alerts assistants one at a time in the defined order.
        :type alerting_mode: ExecutiveAlertGetAlertingMode
        :param next_assistant_number_of_rings: Number of rings before alerting the next assistant when in sequential
            mode.
        :type next_assistant_number_of_rings: int
        :param rollover_enabled: Controls whether the rollover timer (`rolloverWaitTimeInSecs`) is enabled. When set to
            `true`, rollover will trigger after the timer expires, even if assistants are still available. When
            `false`, rollover only occurs when no assistants remain.
        :type rollover_enabled: bool
        :param rollover_action: Specifies what happens when rollover is triggered:
        - VOICE_MESSAGING: Send to Voicemail—A voicemail is sent to the executive.
        - FORWARD: Forward—Calls are forwarded to a specified number.
        - NO_ANSWER_PROCESSING: Do nothing—No action is taken.
        Rollover is always triggered when no assistants remain for a filtered call. If the rollover timer is enabled,
        rollover can also be triggered when the timer expires, even if assistants are still available.
        :type rollover_action: ExecutiveAlertGetRolloverAction
        :param rollover_forward_to_phone_number: Phone number to forward calls to when rollover action is set to
            FORWARD.
        :type rollover_forward_to_phone_number: str
        :param rollover_wait_time_in_secs: Time in seconds to wait before applying the rollover action.
        :type rollover_wait_time_in_secs: int
        :param clid_name_mode: * `EXECUTIVE_ORIGINATOR` - Display executive name followed by caller name.
        :type clid_name_mode: ExecutiveAlertGetClidNameMode
        :param custom_clidname: Custom caller ID name to display (marked for deprecation in CALL-27214).
        :type custom_clidname: str
        :param custom_clidname_in_unicode: Custom caller ID name in Unicode format.
        :type custom_clidname_in_unicode: str
        :param clid_phone_number_mode: * `EXECUTIVE` - Display executive's phone number.
        :type clid_phone_number_mode: ExecutiveAlertGetClidPhoneNumberMode
        :param custom_clidphone_number: Custom caller ID phone number to display.
        :type custom_clidphone_number: str
        :rtype: None
        """
        body = dict()
        if alerting_mode is not None:
            body['alertingMode'] = enum_str(alerting_mode)
        if next_assistant_number_of_rings is not None:
            body['nextAssistantNumberOfRings'] = next_assistant_number_of_rings
        if rollover_enabled is not None:
            body['rolloverEnabled'] = rollover_enabled
        if rollover_action is not None:
            body['rolloverAction'] = enum_str(rollover_action)
        if rollover_forward_to_phone_number is not None:
            body['rolloverForwardToPhoneNumber'] = rollover_forward_to_phone_number
        if rollover_wait_time_in_secs is not None:
            body['rolloverWaitTimeInSecs'] = rollover_wait_time_in_secs
        if clid_name_mode is not None:
            body['clidNameMode'] = enum_str(clid_name_mode)
        if custom_clidname is not None:
            body['customCLIDName'] = custom_clidname
        if custom_clidname_in_unicode is not None:
            body['customCLIDNameInUnicode'] = custom_clidname_in_unicode
        if clid_phone_number_mode is not None:
            body['clidPhoneNumberMode'] = enum_str(clid_phone_number_mode)
        if custom_clidphone_number is not None:
            body['customCLIDPhoneNumber'] = custom_clidphone_number
        url = self.ep('settings/executive/alert')
        super().put(url, json=body)

    def get_my_executive_assigned_assistants(self) -> ExecutiveAssignedAssistantsGet:
        """
        Get My Executive Assigned Assistants

        Get list of assigned executive assistants for an authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecutiveAssignedAssistantsGet`
        """
        url = self.ep('settings/executive/assignedAssistants')
        data = super().get(url)
        r = ExecutiveAssignedAssistantsGet.model_validate(data)
        return r

    def modify_my_executive_assigned_assistants(self, allow_opt_in_out_enabled: bool = None,
                                                assistant_ids: list[str] = None):
        """
        Modify My Executive Assigned Assistants

        Update assigned executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param allow_opt_in_out_enabled: If `true`, the executive can allow assistants to opt in or out of managing
            calls.
        :type allow_opt_in_out_enabled: bool
        :param assistant_ids: List of unique identifiers for the assistants.
        :type assistant_ids: list[str]
        :rtype: None
        """
        body = dict()
        if allow_opt_in_out_enabled is not None:
            body['allowOptInOutEnabled'] = allow_opt_in_out_enabled
        if assistant_ids is not None:
            body['assistantIds'] = assistant_ids
        url = self.ep('settings/executive/assignedAssistants')
        super().put(url, json=body)

    def get_my_executive_assistant_settings(self) -> ExecutiveAssistantSettingsGet:
        """
        Get My Executive Assistant Settings

        Get settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecutiveAssistantSettingsGet`
        """
        url = self.ep('settings/executive/assistant')
        data = super().get(url)
        r = ExecutiveAssistantSettingsGet.model_validate(data)
        return r

    def modify_my_executive_assistant_settings(self, forward_filtered_calls_enabled: bool = None,
                                               forward_to_phone_number: str = None,
                                               executives: list[ExecutivePut] = None):
        """
        Modify My Executive Assistant Settings

        Update Settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param forward_filtered_calls_enabled: If `true`, the executive assistant forwards filtered calls to the
            forward to phone number.
        :type forward_filtered_calls_enabled: bool
        :param forward_to_phone_number: Phone number to forward the filtered calls to. Mandatory if
            `forwardFilteredCallsEnabled` is set to true.
        :type forward_to_phone_number: str
        :param executives: List of executives.
        :type executives: list[ExecutivePut]
        :rtype: None
        """
        body = dict()
        if forward_filtered_calls_enabled is not None:
            body['forwardFilteredCallsEnabled'] = forward_filtered_calls_enabled
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if executives is not None:
            body['executives'] = TypeAdapter(list[ExecutivePut]).dump_python(executives, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/executive/assistant')
        super().put(url, json=body)

    def get_my_executive_available_assistants(self) -> list[AvailableAssistant]:
        """
        Get My Executive Available Assistants

        Get a list of available executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[AvailableAssistant]
        """
        url = self.ep('settings/executive/availableAssistants')
        data = super().get(url)
        r = TypeAdapter(list[AvailableAssistant]).validate_python(data['assistants'])
        return r

    def get_my_executive_call_filtering_settings(self) -> ExecutiveCallFilteringGet:
        """
        Get User Executive Call Filtering Settings

        Get executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecutiveCallFilteringGet`
        """
        url = self.ep('settings/executive/callFiltering')
        data = super().get(url)
        r = ExecutiveCallFilteringGet.model_validate(data)
        return r

    def update_my_executive_call_filtering_settings(self, enabled: bool = None,
                                                    filter_type: ExecutiveCallFilteringGetFilterType = None,
                                                    criteria_activation: list[ExecutiveCallFilteringPatchCriteriaActivationItem] = None):
        """
        Modify User Executive Call Filtering Settings

        Update executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Set to enable or disable executive call filtering.
        :type enabled: bool
        :param filter_type: * `CUSTOM_CALL_FILTERS` - Choose this option to ensure only specific calls are sent to the
            executive assistant.
        :type filter_type: ExecutiveCallFilteringGetFilterType
        :param criteria_activation: List of criteria activation settings to update for executive call filtering.
        :type criteria_activation: list[ExecutiveCallFilteringPatchCriteriaActivationItem]
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if filter_type is not None:
            body['filterType'] = enum_str(filter_type)
        if criteria_activation is not None:
            body['criteriaActivation'] = TypeAdapter(list[ExecutiveCallFilteringPatchCriteriaActivationItem]).dump_python(criteria_activation, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/executive/callFiltering')
        super().put(url, json=body)

    def create_my_executive_call_filtering_criteria(self, filter_name: str = None, schedule_name: str = None,
                                                    schedule_type: ExecutiveCallFilteringCriteriaGetScheduleType = None,
                                                    schedule_level: ExecutiveCallFilteringCriteriaGetScheduleLevel = None,
                                                    calls_from: ExecutiveCallFilteringGetCriteriaItemSource = None,
                                                    anonymous_callers_enabled: bool = None,
                                                    unavailable_callers_enabled: bool = None,
                                                    phone_numbers: list[str] = None, filter_enabled: bool = None,
                                                    calls_to_numbers: list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem] = None) -> str:
        """
        Add User Executive Call Filtering Criteria

        Create a new executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to define detailed filter rules for incoming calls. This
        API creates a new filter rule with the specified configuration, including schedule, phone numbers, and call
        routing preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param filter_name: Name of the criteria.
        :type filter_name: str
        :param schedule_name: Name of the schedule associated with this criteria.
        :type schedule_name: str
        :param schedule_type: * `holidays` - The schedule is based on holidays.
        :type schedule_type: ExecutiveCallFilteringCriteriaGetScheduleType
        :param schedule_level: * `PEOPLE` - The schedule applies to the individual user.
        :type schedule_level: ExecutiveCallFilteringCriteriaGetScheduleLevel
        :param calls_from: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
        :type calls_from: ExecutiveCallFilteringGetCriteriaItemSource
        :param anonymous_callers_enabled: Set to enable or disable the criteria for anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Set to enable or disable the criteria for unavailable callers.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this filtering criteria.
        :type phone_numbers: list[str]
        :param filter_enabled: Controls the action when this criteria matches a call. When `true`, matching calls are
            filtered (blocked). When `false`, matching calls are allowed through and take precedence over other
            filtering criteria, creating exceptions to let specific calls through.
        :type filter_enabled: bool
        :param calls_to_numbers: List of phone numbers to route calls to when this criteria matches.
        :type calls_to_numbers: list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem]
        :rtype: str
        """
        body = dict()
        if filter_name is not None:
            body['filterName'] = filter_name
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if filter_enabled is not None:
            body['filterEnabled'] = filter_enabled
        if calls_to_numbers is not None:
            body['callsToNumbers'] = TypeAdapter(list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem]).dump_python(calls_to_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/executive/callFiltering/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_executive_call_filtering_criteria(self, id: str):
        """
        Delete User Executive Call Filtering Criteria

        Delete a specific executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to manage detailed filter rules for incoming calls. This
        API removes a specific filter rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        super().delete(url)

    def get_my_executive_call_filtering_criteria(self, id: str) -> ExecutiveCallFilteringCriteriaGet:
        """
        Get User Executive Call Filtering Criteria Settings

        Get executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to retrieve detailed configuration for a specific filter
        rule. This includes schedule settings, phone number filters, and call routing preferences for executive call
        filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: :class:`ExecutiveCallFilteringCriteriaGet`
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().get(url)
        r = ExecutiveCallFilteringCriteriaGet.model_validate(data)
        return r

    def update_my_executive_call_filtering_criteria(self, id: str, filter_name: str = None, schedule_name: str = None,
                                                    schedule_type: ExecutiveCallFilteringCriteriaGetScheduleType = None,
                                                    schedule_level: ExecutiveCallFilteringCriteriaGetScheduleLevel = None,
                                                    calls_from: ExecutiveCallFilteringGetCriteriaItemSource = None,
                                                    anonymous_callers_enabled: bool = None,
                                                    unavailable_callers_enabled: bool = None,
                                                    phone_numbers: list[str] = None, filter_enabled: bool = None,
                                                    calls_to_numbers: list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem] = None) -> str:
        """
        Modify User Executive Call Filtering Criteria Settings

        Update executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to modify detailed configuration for a specific filter
        rule. This includes updating schedule settings, phone number filters, and call routing preferences for
        executive call filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :param filter_name: Name of the criteria.
        :type filter_name: str
        :param schedule_name: Name of the schedule associated with this criteria.
        :type schedule_name: str
        :param schedule_type: * `holidays` - The schedule is based on holidays.
        :type schedule_type: ExecutiveCallFilteringCriteriaGetScheduleType
        :param schedule_level: * `PEOPLE` - The schedule applies to the individual user.
        :type schedule_level: ExecutiveCallFilteringCriteriaGetScheduleLevel
        :param calls_from: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
        :type calls_from: ExecutiveCallFilteringGetCriteriaItemSource
        :param anonymous_callers_enabled: Set to enable or disable the criteria for anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Set to enable or disable the criteria for unavailable callers.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this filtering criteria.
        :type phone_numbers: list[str]
        :param filter_enabled: Controls the action when this criteria matches a call. When `true`, matching calls are
            filtered (blocked). When `false`, matching calls are allowed through and take precedence over other
            filtering criteria, creating exceptions to let specific calls through.
        :type filter_enabled: bool
        :param calls_to_numbers: List of phone numbers to route calls to when this criteria matches.
        :type calls_to_numbers: list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem]
        :rtype: str
        """
        body = dict()
        if filter_name is not None:
            body['filterName'] = filter_name
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if filter_enabled is not None:
            body['filterEnabled'] = filter_enabled
        if calls_to_numbers is not None:
            body['callsToNumbers'] = TypeAdapter(list[ExecutiveCallFilteringCriteriaPatchCallsToNumbersItem]).dump_python(calls_to_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().put(url, json=body)
        r = data['id']
        return r

    def get_my_executive_screening_settings(self) -> ExecutiveScreeningGet:
        """
        Get User Executive Screening Settings

        Get executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecutiveScreeningGet`
        """
        url = self.ep('settings/executive/screening')
        data = super().get(url)
        r = ExecutiveScreeningGet.model_validate(data)
        return r

    def update_my_executive_screening_settings(self, enabled: bool = None,
                                               alert_type: ExecutiveScreeningGetAlertType = None,
                                               alert_anywhere_location_enabled: bool = None,
                                               alert_mobility_location_enabled: bool = None,
                                               alert_shared_call_appearance_location_enabled: bool = None):
        """
        Modify User Executive Screening Settings

        Update executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Set to enable or disable executive screening.
        :type enabled: bool
        :param alert_type: * `SILENT` - No audible alert is provided for executive screening.
        :type alert_type: ExecutiveScreeningGetAlertType
        :param alert_anywhere_location_enabled: Indicates if alerts are enabled for Single Number Reach locations.
        :type alert_anywhere_location_enabled: bool
        :param alert_mobility_location_enabled: Indicates if alerts are enabled for Webex Go locations.
        :type alert_mobility_location_enabled: bool
        :param alert_shared_call_appearance_location_enabled: Indicates if alerts are enabled for Shared Call
            Appearance locations.
        :type alert_shared_call_appearance_location_enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if alert_type is not None:
            body['alertType'] = enum_str(alert_type)
        if alert_anywhere_location_enabled is not None:
            body['alertAnywhereLocationEnabled'] = alert_anywhere_location_enabled
        if alert_mobility_location_enabled is not None:
            body['alertMobilityLocationEnabled'] = alert_mobility_location_enabled
        if alert_shared_call_appearance_location_enabled is not None:
            body['alertSharedCallAppearanceLocationEnabled'] = alert_shared_call_appearance_location_enabled
        url = self.ep('settings/executive/screening')
        super().put(url, json=body)

    def get_my_feature_access_codes(self) -> list[FeatureAccessCode]:
        """
        Get My Feature Access Codes

        Retrieve all Feature Access Codes configured for services that are assigned to the authenticated user. For each
        feature access code, the name and code are returned. If an alternate code is defined, it is also returned.

        Feature access codes (FACs), also known as star codes, give users access to advanced calling features.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[FeatureAccessCode]
        """
        url = self.ep('settings/featureAccessCode')
        data = super().get(url)
        r = TypeAdapter(list[FeatureAccessCode]).validate_python(data['featureAccessCodeList'])
        return r

    def get_my_monitoring_settings(self) -> MonitoringSettingsGetResponseObject:
        """
        Get My Monitoring Settings

        Retrieves the monitoring settings of the logged in person, which shows specified people, places, virtual lines
        or call park extensions that are being monitored.

        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MonitoringSettingsGetResponseObject`
        """
        url = self.ep('settings/monitoring')
        data = super().get(url)
        r = MonitoringSettingsGetResponseObject.model_validate(data)
        return r

    def get_my_personal_assistant(self) -> PersonalAssistantGet:
        """
        Get My Personal Assistant

        Retrieve user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Retrieving Personal Assistant details requires a user auth token with `spark:telephony_config_read` scope.

        :rtype: :class:`PersonalAssistantGet`
        """
        url = self.ep('settings/personalAssistant')
        data = super().get(url)
        r = PersonalAssistantGet.model_validate(data)
        return r

    def modify_my_personal_assistant(self, enabled: bool = None, presence: PersonalAssistantGetPresence = None,
                                     until_date_time: Union[str, datetime] = None, transfer_enabled: bool = None,
                                     transfer_number: str = None, alerting: PersonalAssistantGetAlerting = None,
                                     alert_me_first_number_of_rings: int = None):
        """
        Modify My Personal Assistant

        Update user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a user auth token with the `spark:telephony_config_write` scope.

        :param enabled: Toggles feature.
        :type enabled: bool
        :param presence: Person's availability.
        :type presence: PersonalAssistantGetPresence
        :param until_date_time: The date until which the personal assistant is active.
        :type until_date_time: Union[str, datetime]
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param transfer_number: Number to transfer to.
        :type transfer_number: str
        :param alerting: Alert type.
        :type alerting: PersonalAssistantGetAlerting
        :param alert_me_first_number_of_rings: Number of rings for alert type: ALERT_ME_FIRST; available range is 2-20.
        :type alert_me_first_number_of_rings: int
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if presence is not None:
            body['presence'] = enum_str(presence)
        if until_date_time is not None:
            body['untilDateTime'] = until_date_time
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        if transfer_number is not None:
            body['transferNumber'] = transfer_number
        if alerting is not None:
            body['alerting'] = enum_str(alerting)
        if alert_me_first_number_of_rings is not None:
            body['alertMeFirstNumberOfRings'] = alert_me_first_number_of_rings
        url = self.ep('settings/personalAssistant')
        super().put(url, json=body)

    def get_my_preferred_answer_endpoint(self) -> PreferredAnswerEndpoint:
        """
        Get Preferred Answer Endpoint

        Retrieve the selected preferred answering endpoint for the user. If a preferred endpoint is not set for the
        person, API returns empty

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`PreferredAnswerEndpoint`
        """
        url = self.ep('settings/preferredAnswerEndpoint')
        data = super().get(url)
        r = PreferredAnswerEndpoint.model_validate(data)
        return r

    def modify_my_preferred_answer_endpoint(self, id: str):
        """
        Modify Preferred Answer Endpoint

        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the `id`
        attribute must be set to null.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: Person’s preferred answer endpoint.
        :type id: str
        :rtype: None
        """
        body = dict()
        body['id'] = id
        url = self.ep('settings/preferredAnswerEndpoint')
        super().put(url, json=body)

    def get_my_call_center_settings(self) -> CallQueueSettingsGetResponseObject:
        """
        Get My Call Center Settings

        Retrieves the call center settings and list of all call centers the logged in user belongs to.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        The user must have the call center service assigned.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallQueueSettingsGetResponseObject`
        """
        url = self.ep('settings/queues')
        data = super().get(url)
        r = CallQueueSettingsGetResponseObject.model_validate(data)
        return r

    def modify_my_call_center_settings(self, agent_acdstate: AgentACDStateType = None,
                                       queues: list[CallQueuePut] = None):
        """
        Modify My Call Center Settings

        Modify the call center settings and availability for an agent in one or more call centers to which the logged
        in user belongs.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        Contains a list specifying the desired availability status of one or more call centers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :type agent_acdstate: AgentACDStateType
        :param queues: Indicates a list of call centers the agent has joined or may join.
        :type queues: list[CallQueuePut]
        :rtype: None
        """
        body = dict()
        if agent_acdstate is not None:
            body['agentACDState'] = enum_str(agent_acdstate)
        if queues is not None:
            body['queues'] = TypeAdapter(list[CallQueuePut]).dump_python(queues, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/queues')
        super().put(url, json=body)

    def get_secondary_lines_available_preferred_answer_endpoint_list(self, line_owner_id: str) -> list[Endpoints]:
        """
        Get My Secondary Line Owner's Available Preferred Answer Endpoint List

        Retrieve the list of available preferred answer endpoints for the secondary line owner of the authenticated
        person.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :rtype: list[Endpoints]
        """
        url = self.ep(f'settings/secondaryLines/{line_owner_id}/availablePreferredAnswerEndpoints')
        data = super().get(url)
        r = TypeAdapter(list[Endpoints]).validate_python(data['endpoints'])
        return r

    def get_my_secondary_lines_preferred_answer_endpoint(self, line_owner_id: str) -> PreferredAnswerEndpoint:
        """
        Get My Secondary Line Owner's Preferred Answer Endpoint

        Retrieve the selected preferred answering endpoint for the secondary line owner of the authenticated person. If
        a preferred endpoint is not set for the person, API returns empty

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :rtype: :class:`PreferredAnswerEndpoint`
        """
        url = self.ep(f'settings/secondaryLines/{line_owner_id}/preferredAnswerEndpoint')
        data = super().get(url)
        r = PreferredAnswerEndpoint.model_validate(data)
        return r

    def modify_my_secondary_lines_preferred_answer_endpoint(self, line_owner_id: str, id: str):
        """
        Modify My Secondary Line Owner's Preferred Answer Endpoint

        Sets or clears the preferred answer endpoint for the secondary line owner of the authenticated person. To clear
        the preferred answer endpoint the `id` attribute must be set to null.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :param id: Person’s preferred answer endpoint.
        :type id: str
        :rtype: None
        """
        body = dict()
        body['id'] = id
        url = self.ep(f'settings/secondaryLines/{line_owner_id}/preferredAnswerEndpoint')
        super().put(url, json=body)

    def get_my_secondary_lines_available_caller_idlist(self,
                                                       lineowner_id: str) -> list[SelectedCallerIdSettingsGetSelected]:
        """
        Get My Secondary Line Owner's Available Caller ID List

        Get details of available caller IDs for a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        The available caller ID list shows the caller IDs that the user can choose from.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: list[SelectedCallerIdSettingsGetSelected]
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/availableCallerIds')
        data = super().get(url)
        r = TypeAdapter(list[SelectedCallerIdSettingsGetSelected]).validate_python(data['availableCallerIds'])
        return r

    def get_my_secondary_lines_call_forwarding_settings(self, lineowner_id: str) -> CallForwardingInfo:
        """
        Get My Secondary Line Owner's Call Forwarding Settings

        Get details of call forwarding settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`CallForwardingInfo`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callForwarding')
        data = super().get(url)
        r = CallForwardingInfo.model_validate(data)
        return r

    def modify_my_secondary_lines_call_forwarding_settings(self, lineowner_id: str,
                                                           call_forwarding: CallForwardingPutCallForwarding = None,
                                                           business_continuity: CallForwardingInfoCallForwardingBusy = None):
        """
        Modify My Secondary Line Owner's Call Forwarding Settings

        Update call forwarding settings associated with a secondary line owner of the authenticated user.

        Note that an authenticated user can only modify information for their configured secondary lines.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwardingPutCallForwarding
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingInfoCallForwardingBusy
        :rtype: None
        """
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        if business_continuity is not None:
            body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callForwarding')
        super().put(url, json=body)

    def get_my_secondary_lines_call_park_settings(self, lineowner_id: str) -> UserCallParkSettingsGetResponseObject:
        """
        Get My Secondary Line Owner Call Park Settings

        Get details of call park settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`UserCallParkSettingsGetResponseObject`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callPark')
        data = super().get(url)
        r = UserCallParkSettingsGetResponseObject.model_validate(data)
        return r

    def get_my_secondary_lines_call_pickup_group_settings(self, lineowner_id: str) -> CallPickupGroupSettingsGet:
        """
        Get My Secondary Line Owner Call Pickup Group Settings

        Get Call Pickup Group Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Call pickup group enables a user to answer any ringing line within their pickup group. A call pickup group is
        an administrator-defined set of users within a location, to which the call pickup feature applies.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`CallPickupGroupSettingsGet`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callPickupGroup')
        data = super().get(url)
        r = CallPickupGroupSettingsGet.model_validate(data)
        return r

    def get_my_secondary_lines_call_recording_settings(self, lineowner_id: str) -> UserCallRecordingGetResponseObject:
        """
        Get My Secondary Line Owner's Call Recording Settings

        Get details of call recording settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Call recording settings allow you to access and customize options that determine when and how your calls are
        recorded, providing control over recording modes and notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`UserCallRecordingGetResponseObject`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callRecording')
        data = super().get(url)
        r = UserCallRecordingGetResponseObject.model_validate(data)
        return r

    def get_my_secondary_lines_caller_idsettings(self, lineowner_id: str) -> CallerIdSettingsGet:
        """
        Get My Secondary Line Owner Caller ID Settings

        Get Caller ID Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`CallerIdSettingsGet`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callerId')
        data = super().get(url)
        r = CallerIdSettingsGet.model_validate(data)
        return r

    def modify_my_secondary_lines_caller_idsettings(self, lineowner_id: str,
                                                    calling_line_id_delivery_blocking_enabled: bool = None,
                                                    connected_line_identification_restriction_enabled: bool = None):
        """
        Modify My Secondary Line Owner Caller ID Settings

        Update Caller ID Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param calling_line_id_delivery_blocking_enabled: If `true`, the user's name and phone number are not shown to
            people they call.
        :type calling_line_id_delivery_blocking_enabled: bool
        :param connected_line_identification_restriction_enabled: If `true`, the user's name and phone number are not
            shown when receiving a call.
        :type connected_line_identification_restriction_enabled: bool
        :rtype: None
        """
        body = dict()
        if calling_line_id_delivery_blocking_enabled is not None:
            body['callingLineIdDeliveryBlockingEnabled'] = calling_line_id_delivery_blocking_enabled
        if connected_line_identification_restriction_enabled is not None:
            body['connectedLineIdentificationRestrictionEnabled'] = connected_line_identification_restriction_enabled
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callerId')
        super().put(url, json=body)

    def get_my_secondary_lines_feature_access_codes(self, lineowner_id: str) -> list[FeatureAccessCode]:
        """
        Get My Feature Access Codes For Secondary Line Owner

        Retrieve all Feature Access Codes configured for services that are assigned for the secondary line owner. For
        each feature access code, the name and code are returned. If an alternate code is defined, it is also
        returned.

        Feature access codes (FACs), also known as star codes, give users access to advanced calling features.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: list[FeatureAccessCode]
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/featureAccessCode')
        data = super().get(url)
        r = TypeAdapter(list[FeatureAccessCode]).validate_python(data['featureAccessCodeList'])
        return r

    def get_my_secondary_lines_call_center_settings(self, lineowner_id: str) -> CallQueueSettingsGetResponseObject:
        """
        Get My Secondary Line Owner's Call Center Settings

        Retrieves the call center settings and list of all call centers associated with a secondary line of the
        authenticated user.
        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        The secondary line must have the call center service assigned.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`CallQueueSettingsGetResponseObject`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/queues')
        data = super().get(url)
        r = CallQueueSettingsGetResponseObject.model_validate(data)
        return r

    def modify_my_secondary_lines_call_center_settings(self, lineowner_id: str,
                                                       agent_acdstate: AgentACDStateType = None,
                                                       queues: list[CallQueuePut] = None):
        """
        Modify My Secondary Line Owner's Call Center Settings

        Modify the call center settings and availability for an agent in one or more call centers associated with a
        secondary line owner of the authenticated user.
        Note that an authenticated user can only modify information for their configured secondary lines.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        Contains a list specifying the desired availability status of one or more call centers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :type agent_acdstate: AgentACDStateType
        :param queues: Indicates a list of call centers the agent has joined or may join.
        :type queues: list[CallQueuePut]
        :rtype: None
        """
        body = dict()
        if agent_acdstate is not None:
            body['agentACDState'] = enum_str(agent_acdstate)
        if queues is not None:
            body['queues'] = TypeAdapter(list[CallQueuePut]).dump_python(queues, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/queues')
        super().put(url, json=body)

    def get_my_secondary_lines_selected_caller_idsettings(self,
                                                          lineowner_id: str) -> SelectedCallerIdSettingsGetSelected:
        """
        Get My Secondary Line Owner's Selected Caller ID Settings

        Get details of selected caller ID settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: SelectedCallerIdSettingsGetSelected
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/selectedCallerId')
        data = super().get(url)
        r = SelectedCallerIdSettingsGetSelected.model_validate(data['selected'])
        return r

    def modify_my_secondary_lines_selected_caller_idsettings(self, lineowner_id: str,
                                                             selected: SelectedCallerIdSettingsPutSelected):
        """
        Modify My Secondary Line Owner's Selected Caller ID Settings

        Update selected caller ID settings associated with a secondary line owner of the authenticated user.

        Note that an authenticated user can only modify information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param selected: Selected caller ID settings.
        :type selected: SelectedCallerIdSettingsPutSelected
        :rtype: None
        """
        body = dict()
        body['selected'] = selected.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/selectedCallerId')
        super().put(url, json=body)

    def get_my_secondary_lines_calling_services_list(self, lineowner_id: str) -> list[ServicesEnum]:
        """
        Get My Secondary Line Owner Calling Services List

        Retrieves the list of enabled calling services for the secondary line owner of the authenticated user.

        These services are designed to improve call handling and ensure that users can manage their communications
        effectively. They are commonly found in both personal and business telephony systems.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: list[ServicesEnum]
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/services')
        data = super().get(url)
        r = TypeAdapter(list[ServicesEnum]).validate_python(data['services'])
        return r

    def get_my_secondary_lines_voicemail_settings(self, lineowner_id: str) -> VoicemailInfo:
        """
        Get My Secondary Line Owner's Voicemail Settings

        GET voicemail settings for a secondary line of the authenticated user.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`VoicemailInfo`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/voicemail')
        data = super().get(url)
        r = VoicemailInfo.model_validate(data)
        return r

    def modify_my_secondary_lines_voicemail_settings(self, lineowner_id: str,
                                                     notifications: VoicemailInfoNotifications,
                                                     transfer_to_number: VoicemailInfoNotifications,
                                                     enabled: bool = None,
                                                     send_all_calls: VoicemailInfoSendAllCalls = None,
                                                     send_busy_calls: VoicemailPutSendBusyCalls = None,
                                                     send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                                     email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                                     message_storage: VoicemailInfoMessageStorage = None,
                                                     fax_message: VoicemailInfoFaxMessage = None):
        """
        Modify My Secondary Line Owner's Voicemail Settings

        Update voicemail settings associated with a secondary line owner of the authenticated user.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: VoicemailInfoNotifications
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: VoicemailInfoNotifications
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: VoicemailInfoSendAllCalls
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :param send_unanswered_calls: Settings for sending unanswered calls to voicemail.
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :param message_storage: Settings for voicemail message storage.
        :type message_storage: VoicemailInfoMessageStorage
        :param fax_message: Settings for sending FAX messages for new voicemails.
        :type fax_message: VoicemailInfoFaxMessage
        :rtype: None
        """
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
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/voicemail')
        super().put(url, json=body)

    def get_my_selected_caller_idsettings(self) -> SelectedCallerIdSettingsGetSelected:
        """
        Read My Selected Caller ID Settings

        Read selected caller ID settings associated with the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: SelectedCallerIdSettingsGetSelected
        """
        url = self.ep('settings/selectedCallerId')
        data = super().get(url)
        r = SelectedCallerIdSettingsGetSelected.model_validate(data['selected'])
        return r

    def modify_my_selected_caller_idsettings(self, selected: SelectedCallerIdSettingsPutSelected):
        """
        Configure My Selected Caller ID Settings

        Update selected caller ID settings associated with the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param selected: Selected caller ID settings.
        :type selected: SelectedCallerIdSettingsPutSelected
        :rtype: None
        """
        body = dict()
        body['selected'] = selected.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/selectedCallerId')
        super().put(url, json=body)

    def get_my_calling_services_list(self) -> list[ServicesEnum]:
        """
        Get My Calling Services List

        Retrieves the list of enabled calling services for the authenticated user.

        These services are designed to improve call handling and ensure that users can manage their communications
        effectively. They are commonly found in both personal and business telephony systems.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[ServicesEnum]
        """
        url = self.ep('settings/services')
        data = super().get(url)
        r = TypeAdapter(list[ServicesEnum]).validate_python(data['services'])
        return r

    def get_my_single_number_reach_settings(self) -> GetSingleNumberReachObject:
        """
        Get User's Single Number Reach Settings

        Retrieves all single number reach settings configured for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`GetSingleNumberReachObject`
        """
        url = self.ep('settings/singleNumberReach')
        data = super().get(url)
        r = GetSingleNumberReachObject.model_validate(data)
        return r

    def modify_my_single_number_reach_settings(self, alert_all_locations_for_click_to_dial_calls_enabled: bool = None):
        """
        Modify User's Single Number Reach Settings

        Updates single number reach settings associated with the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param alert_all_locations_for_click_to_dial_calls_enabled: If `true`, all locations will be alerted for
            click-to-dial calls.
        :type alert_all_locations_for_click_to_dial_calls_enabled: bool
        :rtype: None
        """
        body = dict()
        if alert_all_locations_for_click_to_dial_calls_enabled is not None:
            body['alertAllLocationsForClickToDialCallsEnabled'] = alert_all_locations_for_click_to_dial_calls_enabled
        url = self.ep('settings/singleNumberReach')
        super().put(url, json=body)

    def add_phone_number_as_single_number_reach(self, phone_number: str, name: str, enabled: bool,
                                                do_not_forward_calls_enabled: bool = None,
                                                answer_confirmation_enabled: bool = None) -> str:
        """
        Add phone number as User's Single Number Reach

        Add a phone number as a single number reach for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number: Phone number.
        :type phone_number: str
        :param name: Name associated with the phone number.
        :type name: str
        :param enabled: If `true`, the phone number is enabled.
        :type enabled: bool
        :param do_not_forward_calls_enabled: Note that this setting attempts to prevent the Single Number Reach (SNR)
            destination from forwarding the call. The SNR destination may or may not respect the indication provided
            hence, it may still be forwarded, and this setting has no impact on the user's own forwarding services.
        :type do_not_forward_calls_enabled: bool
        :param answer_confirmation_enabled: If `true`, answer confirmation is enabled. The default value is `false`.
        :type answer_confirmation_enabled: bool
        :rtype: str
        """
        body = dict()
        body['phoneNumber'] = phone_number
        body['name'] = name
        body['enabled'] = enabled
        if do_not_forward_calls_enabled is not None:
            body['doNotForwardCallsEnabled'] = do_not_forward_calls_enabled
        if answer_confirmation_enabled is not None:
            body['answerConfirmationEnabled'] = answer_confirmation_enabled
        url = self.ep('settings/singleNumberReach/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_single_number_reach_contact_settings(self, phone_number_id: str):
        """
        Delete User's Single Number Reach Contact Settings

        Delete contact settings associated with the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: None
        """
        url = self.ep(f'settings/singleNumberReach/numbers/{phone_number_id}')
        super().delete(url)

    def modify_my_single_number_reach_contact_settings(self, phone_number_id: str, phone_number: str, name: str,
                                                       enabled: bool, do_not_forward_calls_enabled: bool,
                                                       answer_confirmation_enabled: bool):
        """
        Modify User's Single Number Reach Contact Settings

        Update the contact settings of single number reach for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :param phone_number: Phone number.
        :type phone_number: str
        :param name: Name associated with the phone number.
        :type name: str
        :param enabled: If `true`, the phone number is enabled.
        :type enabled: bool
        :param do_not_forward_calls_enabled: If `true`, calls are not forwarded.
        :type do_not_forward_calls_enabled: bool
        :param answer_confirmation_enabled: If `true`, answer confirmation is enabled.
        :type answer_confirmation_enabled: bool
        :rtype: None
        """
        body = dict()
        body['phoneNumber'] = phone_number
        body['name'] = name
        body['enabled'] = enabled
        body['doNotForwardCallsEnabled'] = do_not_forward_calls_enabled
        body['answerConfirmationEnabled'] = answer_confirmation_enabled
        url = self.ep(f'settings/singleNumberReach/numbers/{phone_number_id}')
        super().put(url, json=body)

    def get_my_voicemail_settings(self) -> VoicemailInfo:
        """
        Read Voicemail Settings for a Person

        Retrieve a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_read`.

        :rtype: :class:`VoicemailInfo`
        """
        url = self.ep('settings/voicemail')
        data = super().get(url)
        r = VoicemailInfo.model_validate(data)
        return r

    def modify_my_voicemail_settings(self, notifications: VoicemailInfoNotifications,
                                     transfer_to_number: VoicemailInfoNotifications, enabled: bool = None,
                                     send_all_calls: VoicemailInfoSendAllCalls = None,
                                     send_busy_calls: VoicemailPutSendBusyCalls = None,
                                     send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                     email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                     message_storage: VoicemailInfoMessageStorage = None,
                                     fax_message: VoicemailInfoFaxMessage = None):
        """
        Configure Voicemail Settings for a Person

        Configure a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: VoicemailInfoNotifications
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: VoicemailInfoNotifications
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: VoicemailInfoSendAllCalls
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :param send_unanswered_calls: Settings for sending unanswered calls to voicemail.
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :param message_storage: Settings for voicemail message storage.
        :type message_storage: VoicemailInfoMessageStorage
        :param fax_message: Settings for sending FAX messages for new voicemails.
        :type fax_message: VoicemailInfoFaxMessage
        :rtype: None
        """
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
        url = self.ep('settings/voicemail')
        super().put(url, json=body)

    def get_my_webex_go_override_settings(self) -> bool:
        """
        Get My WebexGoOverride Settings

        Retrieve "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with `spark:telephony_config_read` scope.

        :rtype: bool
        """
        url = self.ep('settings/webexGoOverride')
        data = super().get(url)
        r = data['enabled']
        return r

    def modify_my_webex_go_override_settings(self, enabled: bool = None):
        """
        Modify My WebexGoOverride Settings

        Update "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with the `spark:telephony_config_write` scope.

        :param enabled: True if the "Mobile User Aware" override setting for Do Not Disturb feature is enabled.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep('settings/webexGoOverride')
        super().put(url, json=body)
