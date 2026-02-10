from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Action', 'AnonymousCallRejectionGet', 'AudioAnnouncementFileGetObject',
           'AudioAnnouncementFileGetObjectLevel', 'AudioAnnouncementFileGetObjectMediaFileType', 'CallRecordingInfo',
           'CallRecordingInfoNotification', 'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord',
           'CallRecordingInfoRepeat', 'CallRecordingInfoStartStopAnnouncement', 'CallRecordingPutNotification',
           'CallRecordingPutNotificationType', 'CallsFromTypeForSelectiveForward', 'GetMusicOnHoldObject',
           'GetMusicOnHoldObjectGreeting', 'MonitoredPersonObject', 'NumberOwnerObject', 'NumberOwnerType',
           'PeopleOrPlaceOrVirtualLineType', 'PhoneNumber', 'PlaceDoNotDisturbGet', 'PlacePriorityAlertCriteriaGet',
           'PlaceSelectiveAcceptCallCriteriaGet', 'PlaceSelectiveForwardCallCriteriaGet',
           'PlaceSelectiveRejectCallCriteriaGet', 'PriorityAlertCriteria', 'PriorityAlertGet', 'PrivacyGet',
           'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo', 'PushToTalkNumberObject',
           'RingPattern', 'STATE', 'SelectiveAcceptCallCriteria', 'SelectiveAcceptCallGet',
           'SelectiveForwardCallCriteria', 'SelectiveForwardCallGet', 'SelectiveRejectCallCallsFromType',
           'SelectiveRejectCallGet', 'SelectiveRejectCallSource', 'SelectiveRejectCriteria', 'SequentialRingCriteria',
           'SequentialRingCriteriaGet', 'SequentialRingCriteriaGetCallsFrom',
           'SequentialRingCriteriaGetScheduleLevel', 'SequentialRingCriteriaGetScheduleType', 'SequentialRingGet',
           'SequentialRingNumber', 'SimultaneousRingGet', 'SimultaneousRingNumberGet', 'Source',
           'SourceForSelectiveForward', 'TelephonyType', 'UserBargeInGet',
           'UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls', 'VoicemailInfo',
           'VoicemailInfoEmailCopyOfMessage', 'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage',
           'VoicemailInfoMessageStorageStorageType', 'VoicemailInfoNotifications', 'VoicemailInfoSendBusyCalls',
           'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls', 'VoicemailPutSendUnansweredCalls',
           'WorkspaceAvailableNumberObject', 'WorkspaceCallForwardAvailableNumberObject',
           'WorkspaceCallSettings22Api', 'WorkspaceDigitPatternObject', 'WorkspaceECBNAvailableNumberObject',
           'WorkspaceECBNAvailableNumberObjectOwner', 'WorkspaceECBNAvailableNumberObjectOwnerType',
           'WorkspaceOutgoingPermissionDigitPatternGetListObject',
           'WorkspaceOutgoingPermissionDigitPatternPostObjectAction']


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
    id: Optional[str] = None
    #: Audio announcement file name.
    file_name: Optional[str] = None
    #: Audio announcement file type.
    media_file_type: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class GetMusicOnHoldObjectGreeting(str, Enum):
    #: Play music configured at location level.
    default = 'DEFAULT'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class GetMusicOnHoldObject(ApiModel):
    #: Music on hold enabled or disabled for the workspace.
    moh_enabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location. The music on hold setting returned in the response is used
    #: only when music on hold is enabled at the location level. When `mohLocationEnabled` is false and `mohEnabled`
    #: is true, music on hold is disabled for the workspace. When `mohLocationEnabled` is true and `mohEnabled` is
    #: false, music on hold is turned off for the workspace. In both cases, music on hold will not be played.
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the workspace.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class WorkspaceAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


class WorkspaceECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Line.
    virtual_line = 'VIRTUAL_LINE'
    #: Phone number's owner is a Hunt Group.
    hunt_group = 'HUNT_GROUP'


class WorkspaceECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which the phone number is assigned.
    id: Optional[str] = None
    #: Type of the phone number's owner.
    type: Optional[WorkspaceECBNAvailableNumberObjectOwnerType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE` or
    #: `HUNT_GROUP`.
    display_name: Optional[str] = None


class WorkspaceECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None
    owner: Optional[WorkspaceECBNAvailableNumberObjectOwner] = None


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


class NumberOwnerObject(ApiModel):
    #: Unique identifier of the owner to which the PSTN Phone number is assigned.
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    display_name: Optional[str] = None


class WorkspaceCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Extension for the PSTN phone number.
    extension: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None
    #: Owner details for the phone number.
    owner: Optional[NumberOwnerObject] = None


class AnonymousCallRejectionGet(ApiModel):
    #: `true` if the Anonymous Call Rejection feature is enabled.
    enabled: Optional[bool] = None


class UserBargeInGet(ApiModel):
    #: `true` if the BargeIn feature is enabled.
    enabled: Optional[bool] = None
    #: When `true`, a tone is played when someone barges into a call.
    tone_enabled: Optional[bool] = None


class PlaceDoNotDisturbGet(ApiModel):
    #: `true` if the DoNotDisturb feature is enabled.
    enabled: Optional[bool] = None
    #: When `true`, enables ring reminder when you receive an incoming call while on Do Not Disturb.
    ring_splash_enabled: Optional[bool] = None


class PushToTalkAccessType(str, Enum):
    #: List of people/workspaces that are allowed to use the Push-to-Talk feature to interact with the workspace being
    #: configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people/workspaces that are disallowed to interact using the Push-to-Talk feature with the workspace
    #: being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this workspace but only in one direction. The workspace you enable
    #: Push-to-Talk for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this workspace in a two-way conversation. The workspace you enable
    #: Push-to-Talk for can respond.
    two_way = 'TWO_WAY'


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Person or list of people.
    people = 'PEOPLE'
    #: Workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class PushToTalkNumberObject(ApiModel):
    #: External phone number of the person.
    external: Optional[str] = None
    #: Extension number of the person.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: If `true`, specifies whether the phone number is primary number.
    primary: Optional[bool] = None


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    id: Optional[str] = None
    #: Last name of the person.
    last_name: Optional[str] = None
    #: First name of the person.
    first_name: Optional[str] = None
    #: Display name of the person.
    display_name: Optional[str] = None
    #: Type usually indicates `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Push-to-Talk and Privacy features only supports
    #: `PEOPLE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the person.
    email: Optional[str] = None
    #: List of phone numbers of the person.
    numbers: Optional[list[PushToTalkNumberObject]] = None


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a workspace receives a Push-to-Talk call and
    #: answers the call automatically.
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people/workspaces that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing is enabled.
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name is enabled.
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy is enabled.
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only members specified by `monitoringAgents` can
    #: pickup or barge-in on the call.
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: A custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: A custom greeting has been uploaded
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None


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
    #: Designates optional FAX extension.
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[AnonymousCallRejectionGet] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailInfoSendBusyCalls] = None
    send_unanswered_calls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[VoicemailInfoNotifications] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[VoicemailInfoNotifications] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailInfoEmailCopyOfMessage] = None
    message_storage: Optional[VoicemailInfoMessageStorage] = None
    fax_message: Optional[VoicemailInfoFaxMessage] = None


class VoicemailPutSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail. `numberOfRings` must be between 2 and 20,
    #: inclusive.
    number_of_rings: Optional[int] = None


class SequentialRingCriteriaGetScheduleType(str, Enum):
    #: The Schedule is of type `holidays`.
    holidays = 'holidays'
    #: The Schedule is of type `businessHours`.
    business_hours = 'businessHours'


class SequentialRingCriteriaGetScheduleLevel(str, Enum):
    #: The Schedule specified is of `GROUP` level.
    group = 'GROUP'


class SequentialRingCriteriaGetCallsFrom(str, Enum):
    #: Sequential ring criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Sequential ring criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'


class SequentialRingCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: The type of schedule.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: This indicates the level of the schedule specified by `scheduleName`.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: This indicates if criteria are applicable for calls from any phone number or selected phone numbers.
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true` incoming calls from private numbers are allowed. This is only applicable when `callsFrom` is set to
    #: `SELECT_PHONE_NUMBERS`.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true` incoming calls from unavailable numbers are allowed. This is only applicable when `callsFrom` is set
    #: to `SELECT_PHONE_NUMBERS`.
    unavailable_callers_enabled: Optional[bool] = None
    #: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone numbers for which the
    #: criteria apply.
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls(str, Enum):
    #: Connected line identification is not blocked on redirected calls.
    no_privacy = 'NO_PRIVACY'
    #: Connected line identification is blocked on redirected calls to external numbers.
    privacy_for_external_calls = 'PRIVACY_FOR_EXTERNAL_CALLS'
    #: Connected line identification is blocked on all redirected calls.
    privacy_for_all_calls = 'PRIVACY_FOR_ALL_CALLS'


class SequentialRingNumber(ApiModel):
    #: Phone number set as the sequential number.
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    answer_confirmation_required_enabled: Optional[bool] = None
    #: The number of rings to the specified phone number before the call advances to the subsequent number in the
    #: sequence or goes to voicemail.
    number_of_rings: Optional[int] = None


class Source(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class SequentialRingCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: If criterias are applicable for calls from any phone number or specific phone number.
    source: Optional[Source] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class SequentialRingGet(ApiModel):
    #: When set to `true` sequential ring is enabled.
    enabled: Optional[bool] = None
    #: When set to `true`, the webex calling primary line will ring first.
    ring_base_location_first_enabled: Optional[bool] = None
    #: The number of times the primary line will ring.
    base_location_number_of_rings: Optional[str] = None
    #: When set to `true` and the primary line is busy, the system redirects calls to the numbers configured for
    #: sequential ringing.
    continue_if_base_location_is_busy_enabled: Optional[bool] = None
    #: When set to `true` calls are directed to voicemail.
    calls_to_voicemail_enabled: Optional[bool] = None
    #: A list of up to five phone numbers to which calls will be directed.
    phone_numbers: Optional[list[SequentialRingNumber]] = None
    #: A list of criteria specifying conditions when sequential ringing is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None


class SimultaneousRingNumberGet(ApiModel):
    #: Phone number set as the sequential number.
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    answer_confirmation_required_enabled: Optional[bool] = None


class SimultaneousRingGet(ApiModel):
    #: Simultaneous Ring is enabled or not.
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when on a call.
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when a workspace phone receives an incoming call.
    phone_numbers: Optional[list[SimultaneousRingNumberGet]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    criterias_enabled: Optional[bool] = None


class CallsFromTypeForSelectiveForward(str, Enum):
    #: The schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The schedule applies to any internal phone number.
    any_internal = 'ANY_INTERNAL'
    #: The schedule applies to any external phone number.
    any_external = 'ANY_EXTERNAL'


class SelectiveRejectCallSource(str, Enum):
    #: Selective reject criteria applies for all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Selective reject criteria applies for calls from specific numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Selective reject criteria applies for all forwarded calls.
    forwarded = 'FORWARDED'


class SelectiveRejectCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to reject or not to reject the calls that fit within these parameters.
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallGet(ApiModel):
    #: `true` if the Selective Reject feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective reject is in effect.
    criteria: Optional[list[SelectiveRejectCriteria]] = None


class SelectiveRejectCallCallsFromType(str, Enum):
    #: The Schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The Schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The Schedule applies to the forwarded calls only.
    forwarded = 'FORWARDED'


class PlaceSelectiveRejectCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective reject criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective reject to calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective reject to calls if the callers are unavailable.
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be rejected (if rejectEnabled = `true`) or
    #: not (if rejectEnabled = `false`).
    reject_enabled: Optional[bool] = None


class SelectiveAcceptCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to accept or not to accept the calls that fit within these parameters.
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallGet(ApiModel):
    #: `true` if the Selective Accept feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective accept is in effect.
    criteria: Optional[list[SelectiveAcceptCallCriteria]] = None


class PlaceSelectiveAcceptCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective accept is in effect.
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective accept criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective accept to calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective accept to calls if the callers are unavailable.
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be accepted (if acceptEnabled = `true`) or
    #: not (if acceptEnabled = `false`).
    accept_enabled: Optional[bool] = None


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class RingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern] = None


class PriorityAlertCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number or specific phone number.
    source: Optional[Source] = None
    #: When set to `true` notification is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    notification_enabled: Optional[bool] = None


class PriorityAlertGet(ApiModel):
    #: `true` if the Priority Alert feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when priority alert is in effect.
    criteria: Optional[list[PriorityAlertCriteria]] = None


class PlacePriorityAlertCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e. Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone Numbers.
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true`, enables calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables calls even if callers are unavailable.
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` priority alerting criteria is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    notification_enabled: Optional[bool] = None


class SourceForSelectiveForward(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Criteria applies to all internal incoming numbers.
    any_internal = 'ANY_INTERNAL'
    #: Criteria applies to all external incoming numbers.
    any_external = 'ANY_EXTERNAL'


class SelectiveForwardCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: Criteria are applicable for calls from any phone number or a specific phone number.
    source: Optional[SourceForSelectiveForward] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class SelectiveForwardCallGet(ApiModel):
    #: `true` if the Selective Forward feature is enabled.
    enabled: Optional[bool] = None
    #: Enter the phone number to forward calls to during this schedule.
    default_phone_number_to_forward: Optional[str] = None
    #: When `true`, enables a ring reminder for such calls.
    ring_reminder_enabled: Optional[bool] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    destination_voicemail_enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective forward feature is in effect.
    criteria: Optional[list[SelectiveForwardCallCriteria]] = None


class PlaceSelectiveForwardCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Phone number to forward calls to during this schedule.
    forward_to_phone_number: Optional[str] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Name of the location's schedule which determines when the selective forward is in effect.
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective forward criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[CallsFromTypeForSelectiveForward] = None
    #: When `true`, enables selective forward to calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective forward to calls if the callers are unavailable.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers checked against incoming calls for a match.
    numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be forwarded (if forwardEnabled = `true`) or
    #: not (if forwardEnabled = `false`).
    forward_enabled: Optional[bool] = None


class WorkspaceOutgoingPermissionDigitPatternPostObjectAction(str, Enum):
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


class WorkspaceDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches the digit pattern.
    action: Optional[WorkspaceOutgoingPermissionDigitPatternPostObjectAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class WorkspaceOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[WorkspaceDigitPatternObject]] = None


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


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    enabled: Optional[bool] = None
    #: Call recording scenario.
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool] = None
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


class WorkspaceCallSettings22Api(ApiChild, base='telephony/config/workspaces'):
    """
    Workspace Call Settings (2/2)
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    or location administrator auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    
    **NOTE**: Hot Desk Only workspace does not support any calling settings.
    """

    def get_workspace_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                              org_id: str = None,
                                              **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's phone number.
        By default, this API returns numbers from all locations that are unassigned. To select the suitable number for
        assignment, ensure the workspace's location ID is provided as the `locationId` request parameter.

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
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep('availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def modify_voicemail_passcode_for_a_workspace(self, place_id: str, passcode: str, org_id: str = None):
        """
        Modify voicemail passcode for a workspace.

        Modifying the voicemail passcode for a workspace requires a full administrator, device administrator or
        location administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param place_id: Modify voicemail passcode for this workspace.
        :type place_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a workspace in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'{place_id}/voicemail/passcode')
        super().put(url, params=params, json=body)

    def retrieve_anonymous_call_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Anonymous Call Settings for a Workspace.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/anonymousCallReject')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def modify_anonymous_call_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Anonymous Call Settings for a Workspace.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Anonymous Call Rejection feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{workspace_id}/anonymousCallReject')
        super().put(url, params=params, json=body)

    def retrieve_barge_in_call_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> UserBargeInGet:
        """
        Retrieve Barge In Call Settings for a Workspace.

        Barge In, when enabled, allows you to use the Feature Access Code (FAC) on your desk phone to answer someone
        else’s phone call or barge in on a call they’ve already answered.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserBargeInGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/bargeIn')
        data = super().get(url, params=params)
        r = UserBargeInGet.model_validate(data)
        return r

    def modify_barge_in_call_settings_for_a_workspace(self, workspace_id: str, enabled: bool,
                                                      tone_enabled: bool = None, org_id: str = None):
        """
        Modify Barge In Call Settings for a Workspace.

        Barge In, when enabled, allows you to use the Feature Access Code (FAC) on your desk phone to answer someone
        else’s phone call or barge in on a call they’ve already answered.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Barge In feature is enabled.
        :type enabled: bool
        :param tone_enabled: When `true`, a tone is played when someone barges into a call.
        :type tone_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep(f'{workspace_id}/bargeIn')
        super().put(url, params=params, json=body)

    def retrieve_call_bridge_warning_tone_settings_for_a_workspace(self, workspace_id: str,
                                                                   org_id: str = None) -> bool:
        """
        Retrieve Call Bridge Warning Tone Settings for a Workspace.

        Call Bridge Warning Tone, when enabled, ensures that users hear a warning tone when other users bridge into an
        active call on the same shared line appearance.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/callBridge')
        data = super().get(url, params=params)
        r = data['warningToneEnabled']
        return r

    def modify_call_bridge_warning_tone_settings_for_a_workspace(self, workspace_id: str, warning_tone_enabled: bool,
                                                                 org_id: str = None):
        """
        Modify Call Bridge Warning Tone Settings for a Workspace.

        Call Bridge Warning Tone, when enabled, ensures that users hear a warning tone when other users bridge into an
        active call on the same shared line appearance.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param warning_tone_enabled: `true` if the Call Bridge Warning Tone feature is enabled.
        :type warning_tone_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'{workspace_id}/callBridge')
        super().put(url, params=params, json=body)

    def get_workspace_call_forward_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                           owner_name: str = None, extension: str = None,
                                                           org_id: str = None,
                                                           **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a workspace's call forward
        number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
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
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{workspace_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_call_intercept_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                             owner_name: str = None, extension: str = None,
                                                             org_id: str = None,
                                                             **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a workspace's call intercept
        number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
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
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{workspace_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def read_call_policy_settings_for_a_workspace(self, workspace_id: str,
                                                  org_id: str = None) -> UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls:
        """
        Read Call Policy Settings for a Workspace

        Retrieve a workspace Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/callPolicies')
        data = super().get(url, params=params)
        r = UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls.model_validate(data['connectedLineIdPrivacyOnRedirectedCalls'])
        return r

    def configure_call_policy_settings_for_a_workspace(self, workspace_id: str,
                                                       connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls,
                                                       org_id: str = None):
        """
        Configure Call Policy Settings for a Workspace

        Configure a workspace Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param connected_line_id_privacy_on_redirected_calls: Specifies the connection type to be used.
        :type connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.ep(f'{workspace_id}/callPolicies')
        super().put(url, params=params, json=body)

    def retrieve_do_not_disturb_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> PlaceDoNotDisturbGet:
        """
        Retrieve DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is available for professional and common area licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceDoNotDisturbGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/doNotDisturb')
        data = super().get(url, params=params)
        r = PlaceDoNotDisturbGet.model_validate(data)
        return r

    def modify_do_not_disturb_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                       ring_splash_enabled: bool = None, org_id: str = None):
        """
        Modify DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional and common area licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the DoNotDisturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: When `true`, enables ring reminder when you receive an incoming call while on Do
            Not Disturb.
        :type ring_splash_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'{workspace_id}/doNotDisturb')
        super().put(url, params=params, json=body)

    def get_workspace_ecbn_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                   owner_name: str = None, org_id: str = None,
                                                   **params) -> Generator[WorkspaceECBNAvailableNumberObject, None, None]:
        """
        Get Workspace ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's emergency callback number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'{workspace_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_fax_message_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's FAX message number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{workspace_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def delete_a_specific_access_code_for_a_workspace(self, workspace_id: str, access_code: str, org_id: str = None):
        """
        Delete a Specific Access Code for a Workspace

        Deletes a specific access code for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full, device or location administrator auth token with the scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param access_code: Access code for outgoing calls.
        :type access_code: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/accessCodes/{access_code}')
        super().delete(url, params=params)

    def retrieve_call_recording_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> CallRecordingInfo:
        """
        Retrieve call recording settings for a workspace.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full, read-only, device or location administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callRecordings')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def modify_call_recording_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                       record: CallRecordingInfoRecord = None,
                                                       record_voicemail_enabled: bool = None,
                                                       notification: CallRecordingPutNotification = None,
                                                       repeat: CallRecordingInfoRepeat = None,
                                                       start_stop_announcement: CallRecordingInfoStartStopAnnouncement = None,
                                                       org_id: str = None):
        """
        Modify Call Recording Settings for a Workspace

        Modify call forwarding settings for a workspace.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        The vendor's terms of service have to be accepted to enable call recording. Vendor details along with the terms
        of service URL are shared when the vendor's terms of service are not accepted yet.

        This API requires a full, device or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: CallRecordingInfoRecord
        :param record_voicemail_enabled: When `true`, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: CallRecordingPutNotification
        :param repeat: Beep sound plays periodically.
        :type repeat: CallRecordingInfoRepeat
        :param start_stop_announcement: Call Recording starts and stops announcement settings.
        :type start_stop_announcement: CallRecordingInfoStartStopAnnouncement
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        if notification is not None:
            body['notification'] = notification.model_dump(mode='json', by_alias=True, exclude_none=True)
        if repeat is not None:
            body['repeat'] = repeat.model_dump(mode='json', by_alias=True, exclude_none=True)
        if start_stop_announcement is not None:
            body['startStopAnnouncement'] = start_stop_announcement.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/features/callRecordings')
        super().put(url, params=params, json=body)

    def upload_call_intercept_announcement_file_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Upload call intercept announcement file for a workspace.

        The upload announcement feature for a call intercept is used to play custom announcements for a workspace.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full, device or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/intercept/actions/announcementUpload/invoke')
        super().post(url, params=params)

    def retrieve_music_on_hold_settings_for_a_workspace(self, workspace_id: str,
                                                        org_id: str = None) -> GetMusicOnHoldObject:
        """
        Retrieve Music On Hold Settings for a Workspace.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving a workspace's music on hold settings requires a full, device or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

    def modify_music_on_hold_settings_for_a_workspace(self, workspace_id: str, moh_enabled: bool = None,
                                                      greeting: GetMusicOnHoldObjectGreeting = None,
                                                      audio_announcement_file: AudioAnnouncementFileGetObject = None,
                                                      org_id: str = None):
        """
        Modify music on hold settings for a Workspace.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold setting for a workspace, music on hold setting must be enabled for this location.

        This API requires a full or device administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param moh_enabled: Music on hold is enabled or disabled for the workspace.
        :type moh_enabled: bool
        :param greeting: Greeting type for the workspace.
        :type greeting: GetMusicOnHoldObjectGreeting
        :param audio_announcement_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_announcement_file: AudioAnnouncementFileGetObject
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
        if moh_enabled is not None:
            body['mohEnabled'] = moh_enabled
        if greeting is not None:
            body['greeting'] = enum_str(greeting)
        if audio_announcement_file is not None:
            body['audioAnnouncementFile'] = audio_announcement_file.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/musicOnHold')
        super().put(url, params=params, json=body)

    def assign_or_unassign_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                                        phone_numbers: list[PhoneNumber],
                                                                        distinctive_ring_enabled: bool = None,
                                                                        org_id: str = None):
        """
        Assign or Unassign numbers associated with a specific workspace

        Assign or unassign alternate phone numbers associated with a specific workspace.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: list[PhoneNumber]
        :param distinctive_ring_enabled: Enables a distinctive ring pattern for the person.
        :type distinctive_ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if distinctive_ring_enabled is not None:
            body['distinctiveRingEnabled'] = distinctive_ring_enabled
        body['phoneNumbers'] = TypeAdapter(list[PhoneNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/numbers')
        super().put(url, params=params, json=body)

    def delete_all_digit_patterns_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete all digit patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

    def retrieve_all_digit_patterns_for_a_workspace(self, workspace_id: str,
                                                    org_id: str = None) -> WorkspaceOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve all digit patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = WorkspaceOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def create_digit_pattern_for_a_workspace(self, workspace_id: str, name: str, pattern: str, action: Action,
                                             transfer_enabled: bool, org_id: str = None) -> str:
        """
        Create Digit Pattern for a Workspace

        Create a new digit pattern for the given workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: Action
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['pattern'] = pattern
        body['action'] = enum_str(action)
        body['transferEnabled'] = transfer_enabled
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_the_digit_pattern_category_control_settings_for_the_workspace(self, workspace_id: str,
                                                                             use_custom_digit_patterns: bool = None,
                                                                             org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for the Workspace

        Modifies whether this workspace uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or location administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def delete_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a Digit Pattern for the Workspace

        Delete a digit pattern for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def retrieve_a_digit_pattern_details_for_the_workspace(self, workspace_id: str, digit_pattern_id: str,
                                                           org_id: str = None) -> WorkspaceDigitPatternObject:
        """
        Retrieve a Digit Pattern details for the Workspace

        Retrieve the designated digit pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = WorkspaceDigitPatternObject.model_validate(data)
        return r

    def modify_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, name: str = None,
                                                 pattern: str = None, action: Action = None,
                                                 transfer_enabled: bool = None, org_id: str = None):
        """
        Modify a Digit Pattern for the Workspace

        Modify the designated digit pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: Action
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if pattern is not None:
            body['pattern'] = pattern
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        url = self.ep(f'{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def retrieve_priority_alert_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> PriorityAlertGet:
        """
        Retrieve Priority Alert Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PriorityAlertGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/priorityAlert')
        data = super().get(url, params=params)
        r = PriorityAlertGet.model_validate(data)
        return r

    def configure_priority_alert_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Configure Priority Alert Settings for a Workspace

        Configure a workspace Priority Alert Settings.

        The priority alert feature enables administrator to configure priority alert settings for a professional
        workspace.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope that can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Priority Alert feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{workspace_id}/priorityAlert')
        super().put(url, params=params, json=body)

    def create_priority_alert_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                       schedule_type: SequentialRingCriteriaGetScheduleType,
                                                       schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                       calls_from: SequentialRingCriteriaGetCallsFrom,
                                                       notification_enabled: bool,
                                                       anonymous_callers_enabled: bool = None,
                                                       unavailable_callers_enabled: bool = None,
                                                       phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Priority Alert Criteria for a Workspace

        Create Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the priority alert is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e. Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone
            Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param notification_enabled: When set to `true` priority alerting criteria is enabled for calls that meet the
            current criteria. Criteria with `notificationEnabled` set to `false` take priority.
        :type notification_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['notificationEnabled'] = notification_enabled
        url = self.ep(f'{workspace_id}/priorityAlert/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Priority Alert Criteria for a Workspace

        Delete Priority Alert criteria Settings for a workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/priorityAlert/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                         org_id: str = None) -> PlacePriorityAlertCriteriaGet:
        """
        Retrieve Priority Alert Criteria for a Workspace

        Retrieve Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlacePriorityAlertCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/priorityAlert/criteria/{id}')
        data = super().get(url, params=params)
        r = PlacePriorityAlertCriteriaGet.model_validate(data)
        return r

    def modify_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                       schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                       schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                       calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                       anonymous_callers_enabled: bool = None,
                                                       unavailable_callers_enabled: bool = None,
                                                       phone_numbers: list[str] = None,
                                                       notification_enabled: bool = None, org_id: str = None):
        """
        Modify Priority Alert Criteria for a Workspace

        Modify Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the priority alert is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e. Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone
            Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param notification_enabled: When set to `true` priority alerting criteria is enabled for calls that meet the
            current criteria. Criteria with `notificationEnabled` set to `false` take priority.
        :type notification_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep(f'{workspace_id}/priorityAlert/criteria/{id}')
        super().put(url, params=params, json=body)

    def retrieve_privacy_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PrivacyGet:
        """
        Retrieve Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def modify_privacy_settings_for_a_workspace(self, workspace_id: str, aa_extension_dialing_enabled: bool = None,
                                                aa_naming_dialing_enabled: bool = None,
                                                enable_phone_status_directory_privacy: bool = None,
                                                enable_phone_status_pickup_barge_in_privacy: bool = None,
                                                monitoring_agents: list[str] = None, org_id: str = None):
        """
        Modify Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param aa_extension_dialing_enabled: When `true` auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When `true` auto attendant dialing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When `true` phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param enable_phone_status_pickup_barge_in_privacy: When `true` privacy is enforced for call pickup and
            barge-in. Only members specified by `monitoringAgents` can pickup or barge-in on the call.
        :type enable_phone_status_pickup_barge_in_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'{workspace_id}/privacy')
        super().put(url, params=params, json=body)

    def read_push_to_talk_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PushToTalkInfo:
        """
        Read Push-to-Talk Settings for a Workspace

        Retrieve Push-to-Talk settings for a workspace.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects
        people/workspaces in different parts of your organization.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/pushToTalk')
        data = super().get(url, params=params)
        r = PushToTalkInfo.model_validate(data)
        return r

    def configure_push_to_talk_settings_for_a_workspace(self, workspace_id: str, allow_auto_answer: bool = None,
                                                        connection_type: PushToTalkConnectionType = None,
                                                        access_type: PushToTalkAccessType = None,
                                                        members: list[str] = None, org_id: str = None):
        """
        Configure Push-to-Talk settings for a workspace.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects
        people/workspaces in different parts of your organization.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param allow_auto_answer: `true` if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
        :type members: list[str]
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
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
        url = self.ep(f'{workspace_id}/pushToTalk')
        super().put(url, params=params, json=body)

    def get_workspace_secondary_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's secondary number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{workspace_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def retrieve_selective_accept_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> SelectiveAcceptCallGet:
        """
        Retrieve Selective Accept Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SelectiveAcceptCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveAccept')
        data = super().get(url, params=params)
        r = SelectiveAcceptCallGet.model_validate(data)
        return r

    def modify_selective_accept_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Selective Accept Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: indicates whether selective accept is enabled or not.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{workspace_id}/selectiveAccept')
        super().put(url, params=params, json=body)

    def create_selective_accept_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                         calls_from: SelectiveRejectCallCallsFromType,
                                                         accept_enabled: bool, anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Selective Accept Criteria for a Workspace

        Create Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the selective accept is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective accept criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param accept_enabled: Choose to accept (if `acceptEnabled` = `true`) or not to accept (if `acceptEnabled` =
            `false`) the calls that fit within these parameters.
        :type accept_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['acceptEnabled'] = accept_enabled
        url = self.ep(f'{workspace_id}/selectiveAccept/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Accept Criteria for a Workspace

        Delete Selective Accept criteria Settings for a workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveAccept/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                           org_id: str = None) -> PlaceSelectiveAcceptCallCriteriaGet:
        """
        Retrieve Selective Accept Criteria for a Workspace

        Retrieve Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveAcceptCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveAccept/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveAcceptCallCriteriaGet.model_validate(data)
        return r

    def modify_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                         calls_from: SelectiveRejectCallCallsFromType = None,
                                                         anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, accept_enabled: bool = None,
                                                         org_id: str = None):
        """
        Modify Selective Accept Criteria for a Workspace

        Modify Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the selective accept is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective accept criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param accept_enabled: Choose to accept (if `acceptEnabled` = `true`) or not to accept (if `acceptEnabled` =
            `false`) the calls that fit within these parameters.
        :type accept_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if accept_enabled is not None:
            body['acceptEnabled'] = accept_enabled
        url = self.ep(f'{workspace_id}/selectiveAccept/criteria/{id}')
        super().put(url, params=params, json=body)

    def retrieve_selective_forward_settings_for_a_workspace(self, workspace_id: str,
                                                            org_id: str = None) -> SelectiveForwardCallGet:
        """
        Retrieve Selective Forward Settings for a Workspace

        Retrieve Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveForward')
        data = super().get(url, params=params)
        r = SelectiveForwardCallGet.model_validate(data)
        return r

    def modify_selective_forward_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                          default_phone_number_to_forward: str = None,
                                                          ring_reminder_enabled: bool = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Selective Forward Settings for a Workspace

        Modify Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Selective Forward feature is enabled.
        :type enabled: bool
        :param default_phone_number_to_forward: Enter the phone number to forward calls to during this schedule.
        :type default_phone_number_to_forward: str
        :param ring_reminder_enabled: When `true`, enables a ring reminder for such calls.
        :type ring_reminder_enabled: bool
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if default_phone_number_to_forward is not None:
            body['defaultPhoneNumberToForward'] = default_phone_number_to_forward
        if ring_reminder_enabled is not None:
            body['ringReminderEnabled'] = ring_reminder_enabled
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        url = self.ep(f'{workspace_id}/selectiveForward')
        super().put(url, params=params, json=body)

    def create_selective_forward_criteria_for_a_workspace(self, workspace_id: str,
                                                          calls_from: CallsFromTypeForSelectiveForward,
                                                          forward_to_phone_number: str = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          numbers: list[str] = None, forward_enabled: bool = None,
                                                          org_id: str = None) -> str:
        """
        Create Selective Forward Criteria for a Workspace

        Create Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param calls_from: Indicates whether to apply the selective forward criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: CallsFromTypeForSelectiveForward
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true`, enables selective forward to calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables selective forward to calls if the callers are
            unavailable.
        :type unavailable_callers_enabled: bool
        :param numbers: List of phone numbers checked against incoming calls for a match.
        :type numbers: list[str]
        :param forward_enabled: Indicates whether the calls, that fit within these parameters, will be forwarded (if
            forwardEnabled = `true`) or not (if forwardEnabled = `false`).
        :type forward_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if numbers is not None:
            body['numbers'] = numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'{workspace_id}/selectiveForward/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Forward Criteria for a Workspace

        Delete Selective Forward Call criteria Settings for a workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveForward/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                            org_id: str = None) -> PlaceSelectiveForwardCallCriteriaGet:
        """
        Retrieve Selective Forward Criteria for a Workspace

        Retrieve Selective Forward Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveForwardCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveForward/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveForwardCallCriteriaGet.model_validate(data)
        return r

    def modify_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                          calls_from: CallsFromTypeForSelectiveForward,
                                                          forward_to_phone_number: str = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          numbers: list[str] = None, forward_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Selective Forward Criteria for a Workspace

        Modify Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param calls_from: Indicates whether to apply the selective forward criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: CallsFromTypeForSelectiveForward
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true`, enables selective forward to calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables selective forward to calls if the callers are
            unavailable.
        :type unavailable_callers_enabled: bool
        :param numbers: List of phone numbers checked against incoming calls for a match.
        :type numbers: list[str]
        :param forward_enabled: Indicates whether the calls, that fit within these parameters, will be forwarded (if
            forwardEnabled = `true`) or not (if forwardEnabled = `false`).
        :type forward_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if numbers is not None:
            body['numbers'] = numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'{workspace_id}/selectiveForward/criteria/{id}')
        super().put(url, params=params, json=body)

    def retrieve_selective_reject_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> SelectiveRejectCallGet:
        """
        Retrieve Selective Reject Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveReject')
        data = super().get(url, params=params)
        r = SelectiveRejectCallGet.model_validate(data)
        return r

    def modify_selective_reject_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Selective Reject Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: if `true`, selective reject is enabled.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{workspace_id}/selectiveReject')
        super().put(url, params=params, json=body)

    def create_selective_reject_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                         calls_from: SelectiveRejectCallCallsFromType,
                                                         reject_enabled: bool, anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Selective Reject Criteria for a Workspace

        Create Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the selective reject is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective reject criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param reject_enabled: Choose to reject (if `rejectEnabled` = `true`) or not to reject (if `rejectEnabled` =
            `false`) the calls that fit within these parameters.
        :type reject_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'{workspace_id}/selectiveReject/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Reject Criteria for a Workspace

        Delete Selective Reject criteria Settings for a workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveReject/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                           org_id: str = None) -> PlaceSelectiveRejectCallCriteriaGet:
        """
        Retrieve Selective Reject Criteria for a Workspace

        Retrieve Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveRejectCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/selectiveReject/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveRejectCallCriteriaGet.model_validate(data)
        return r

    def modify_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                         calls_from: SelectiveRejectCallCallsFromType = None,
                                                         anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, reject_enabled: bool = None,
                                                         org_id: str = None):
        """
        Modify Selective Reject Criteria for a Workspace

        Modify Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the selective reject is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective reject criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param reject_enabled: Choose to reject (if `rejectEnabled` = `true`) or not to reject (if `rejectEnabled` =
            `false`) the calls that fit within these parameters.
        :type reject_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if reject_enabled is not None:
            body['rejectEnabled'] = reject_enabled
        url = self.ep(f'{workspace_id}/selectiveReject/criteria/{id}')
        super().put(url, params=params, json=body)

    def retrieve_sequential_ring_settings_for_a_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> SequentialRingGet:
        """
        Retrieve sequential ring settings for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SequentialRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/sequentialRing')
        data = super().get(url, params=params)
        r = SequentialRingGet.model_validate(data)
        return r

    def modify_sequential_ring_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                        ring_base_location_first_enabled: bool = None,
                                                        base_location_number_of_rings: int = None,
                                                        continue_if_base_location_is_busy_enabled: bool = None,
                                                        calls_to_voicemail_enabled: bool = None,
                                                        phone_numbers: list[SequentialRingNumber] = None,
                                                        org_id: str = None):
        """
        Modify sequential ring settings for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: When set to `true` sequential ring is enabled.
        :type enabled: bool
        :param ring_base_location_first_enabled: When set to `true`, the webex calling primary line will ring first.
        :type ring_base_location_first_enabled: bool
        :param base_location_number_of_rings: The number of times the primary line will ring.
            `baseLocationNumberOfRings` must be between 2 and 20, inclusive.
        :type base_location_number_of_rings: int
        :param continue_if_base_location_is_busy_enabled: When set to `true` and the primary line is busy, the system
            redirects calls to the numbers configured for sequential ringing.
        :type continue_if_base_location_is_busy_enabled: bool
        :param calls_to_voicemail_enabled: When set to `true` calls are directed to voicemail.
        :type calls_to_voicemail_enabled: bool
        :param phone_numbers: A list of up to five phone numbers to which calls will be directed.
        :type phone_numbers: list[SequentialRingNumber]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if ring_base_location_first_enabled is not None:
            body['ringBaseLocationFirstEnabled'] = ring_base_location_first_enabled
        if base_location_number_of_rings is not None:
            body['baseLocationNumberOfRings'] = base_location_number_of_rings
        if continue_if_base_location_is_busy_enabled is not None:
            body['continueIfBaseLocationIsBusyEnabled'] = continue_if_base_location_is_busy_enabled
        if calls_to_voicemail_enabled is not None:
            body['callsToVoicemailEnabled'] = calls_to_voicemail_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SequentialRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/sequentialRing')
        super().put(url, params=params, json=body)

    def create_sequential_ring_criteria_for_a_workspace(self, workspace_id: str,
                                                        calls_from: SequentialRingCriteriaGetCallsFrom,
                                                        ring_enabled: bool, schedule_name: str = None,
                                                        schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                        schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param calls_from: This indicates if criteria are applicable for calls from any phone number or selected phone
            numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param ring_enabled: When set to `true` sequential ringing is enabled for calls that meet the current criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the sequential ring is in effect.
        :type schedule_name: str
        :param schedule_type: This indicates the type of schedule.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: This indicates the level of the schedule specified by `scheduleName`.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true` incoming calls from private numbers are allowed. This is only
            applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true` incoming calls from unavailable numbers are allowed. This is
            only applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone
            numbers for which the criteria apply.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep(f'{workspace_id}/sequentialRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/sequentialRing/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                          org_id: str = None) -> SequentialRingCriteriaGet:
        """
        Retrieve sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/sequentialRing/criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def modify_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                        schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                        schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                        calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None, ring_enabled: bool = None,
                                                        org_id: str = None):
        """
        Modify sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the sequential ring is in effect.
        :type schedule_name: str
        :param schedule_type: This indicates the type of schedule.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: This indicates the level of the schedule specified by `scheduleName`.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: This indicates if criteria are applicable for calls from any phone number or selected phone
            numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true` incoming calls from private numbers are allowed. This is only
            applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true` incoming calls from unavailable numbers are allowed. This is
            only applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone
            numbers for which the criteria apply.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` sequential ringing is enabled for calls that meet the current criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'{workspace_id}/sequentialRing/criteria/{id}')
        super().put(url, params=params, json=body)

    def retrieve_simultaneous_ring_settings_for_a_workspace(self, workspace_id: str,
                                                            org_id: str = None) -> SimultaneousRingGet:
        """
        Retrieve Simultaneous Ring Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SimultaneousRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/simultaneousRing')
        data = super().get(url, params=params)
        r = SimultaneousRingGet.model_validate(data)
        return r

    def modify_simultaneous_ring_settings_for_a_workspace(self, workspace_id: str, criterias_enabled: bool,
                                                          enabled: bool = None,
                                                          do_not_ring_if_on_call_enabled: bool = None,
                                                          phone_numbers: list[SimultaneousRingNumberGet] = None,
                                                          org_id: str = None):
        """
        Modify Simultaneous Ring Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure the workspace phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param criterias_enabled: When `true`, enables the selected schedule for simultaneous ring.
        :type criterias_enabled: bool
        :param enabled: Simultaneous Ring is enabled or not.
        :type enabled: bool
        :param do_not_ring_if_on_call_enabled: When set to `true`, the configured phone numbers won't ring when on a
            call.
        :type do_not_ring_if_on_call_enabled: bool
        :param phone_numbers: Enter up to 10 phone numbers to ring simultaneously when a workspace phone receives an
            incoming call.
        :type phone_numbers: list[SimultaneousRingNumberGet]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if do_not_ring_if_on_call_enabled is not None:
            body['doNotRingIfOnCallEnabled'] = do_not_ring_if_on_call_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SimultaneousRingNumberGet]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        body['criteriasEnabled'] = criterias_enabled
        url = self.ep(f'{workspace_id}/simultaneousRing')
        super().put(url, params=params, json=body)

    def create_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom,
                                                          ring_enabled: bool, anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Simultaneous Ring Criteria for a Workspace

        Create Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply simultaneously ring for calls from Any Phone Number or Select
            Phone Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param ring_enabled: When set to `true` simultaneous ringing criteria is enabled for calls that meet the
            current criteria. Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep(f'{workspace_id}/simultaneousRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Simultaneous Ring Criteria for a Workspace

        Delete simultaneous ring criteria Settings for a workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/simultaneousRing/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                            org_id: str = None) -> SequentialRingCriteriaGet:
        """
        Retrieve Simultaneous Ring Criteria for a Workspace

        Retrieve Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/simultaneousRing/criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def modify_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None, ring_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Simultaneous Ring Criteria for a Workspace

        Modify Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply simultaneously ring for calls from Any Phone Number or Select
            Phone Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` simultaneous ringing criteria is enabled for calls that meet the
            current criteria. Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'{workspace_id}/simultaneousRing/criteria/{id}')
        super().put(url, params=params, json=body)

    def read_voicemail_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> VoicemailInfo:
        """
        Read Voicemail Settings for a Workspace

        Retrieve a workspace Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`VoicemailInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/voicemail')
        data = super().get(url, params=params)
        r = VoicemailInfo.model_validate(data)
        return r

    def configure_voicemail_settings_for_a_workspace(self, workspace_id: str,
                                                     notifications: VoicemailInfoNotifications,
                                                     transfer_to_number: VoicemailInfoNotifications,
                                                     enabled: bool = None,
                                                     send_all_calls: AnonymousCallRejectionGet = None,
                                                     send_busy_calls: VoicemailPutSendBusyCalls = None,
                                                     send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                                     email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                                     message_storage: VoicemailInfoMessageStorage = None,
                                                     fax_message: VoicemailInfoFaxMessage = None, org_id: str = None):
        """
        Configure Voicemail Settings for a Workspace

        Configure a workspace Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: VoicemailInfoNotifications
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: VoicemailInfoNotifications
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: AnonymousCallRejectionGet
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :type message_storage: VoicemailInfoMessageStorage
        :type fax_message: VoicemailInfoFaxMessage
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
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
        url = self.ep(f'{workspace_id}/voicemail')
        super().put(url, params=params, json=body)

    def configure_busy_voicemail_greeting_for_a_place(self, workspace_id: str, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Place

        Configure a workspace's Busy Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url, params=params)

    def configure_no_answer_voicemail_greeting_for_a_place(self, workspace_id: str, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Place

        Configure a workspace's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)
