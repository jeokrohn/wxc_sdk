from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Action', 'AnonymousCallRejectionGet', 'BetaWorkspaceCallSettingsWithProfessionalLicenseApi',
           'MonitoredPersonObject', 'PeopleOrPlaceOrVirtualLineType', 'PhoneNumber', 'PlaceGetNumbersResponse',
           'PlacePriorityAlertCriteriaGet', 'PlaceSelectiveAcceptCallCriteriaGet',
           'PlaceSelectiveForwardCallCriteriaGet', 'PlaceSelectiveRejectCallCriteriaGet', 'PriorityAlertCriteria',
           'PriorityAlertGet', 'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo',
           'PushToTalkNumberObject', 'RingPattern', 'SelectiveAcceptCallCriteria', 'SelectiveAcceptCallGet',
           'SelectiveForwardCallGet', 'SelectiveRejectCallCallsFromType', 'SelectiveRejectCallGet',
           'SelectiveRejectCallSource', 'SelectiveRejectCriteria', 'SequentialRingCriteria',
           'SequentialRingCriteriaGet', 'SequentialRingCriteriaGetCallsFrom',
           'SequentialRingCriteriaGetScheduleLevel', 'SequentialRingCriteriaGetScheduleType', 'SequentialRingGet',
           'SequentialRingNumber', 'SimultaneousRingGet', 'SimultaneousRingNumber', 'Source', 'UserBargeInGet',
           'UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls', 'UserDoNotDisturbGet', 'VoicemailInfo',
           'VoicemailInfoEmailCopyOfMessage', 'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage',
           'VoicemailInfoMessageStorageStorageType', 'VoicemailInfoNotifications', 'VoicemailInfoSendBusyCalls',
           'VoicemailInfoSendBusyCallsGreeting', 'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls',
           'VoicemailPutSendUnansweredCalls']


class AnonymousCallRejectionGet(ApiModel):
    #: `true` if the Anonymous Call Rejection feature is enabled.
    #: example: True
    enabled: Optional[bool] = None


class UserBargeInGet(ApiModel):
    #: `true` if the BargeIn feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: When `true`, a tone is played when someone barges into a call.
    tone_enabled: Optional[bool] = None


class UserDoNotDisturbGet(ApiModel):
    #: `true` if the DoNotDisturb feature is enabled.
    #: example: True
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
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class PushToTalkNumberObject(ApiModel):
    #: External phone number of the person.
    #: example: +19845551088
    external: Optional[str] = None
    #: Extension number of the person.
    #: example: 1088
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341088
    esn: Optional[str] = None
    #: Indicates whether phone number is primary number.
    #: example: True
    primary: Optional[bool] = None


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the person.
    #: example: Little
    last_name: Optional[str] = None
    #: First name of the person.
    #: example: Alice
    first_name: Optional[str] = None
    #: Display name of the person.
    #: example: Alice Little
    display_name: Optional[str] = None
    #: Type usually indicates `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Push-to-Talk and Privacy features only supports
    #: `PEOPLE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the person.
    #: example: alice@example.com
    email: Optional[str] = None
    #: List of phone numbers of the person.
    numbers: Optional[list[PushToTalkNumberObject]] = None


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a workspace receives a Push-to-Talk call and
    #: answers the call automatically.
    #: example: True
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people/workspaces that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing is enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name is enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy is enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class VoicemailInfoSendBusyCallsGreeting(str, Enum):
    #: The default greeting will be played.
    default = 'DEFAULT'
    #: Designates that a custom `.wav` file will be played.
    custom = 'CUSTOM'


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: Indicates a custom greeting has been uploaded.
    #: example: True
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: Indicates a custom greeting has been uploaded
    #: example: True
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
    system_max_number_of_rings: Optional[int] = None


class VoicemailInfoNotifications(ApiModel):
    #: Send of unanswered calls to voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Email address to which the notification will be sent. For text messages, use an email to text message gateway
    #: like `2025551212@txt.example.net`.
    #: example: 2025551212@txt.att.net
    destination: Optional[str] = None


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
    #: Designates optional FAX extension.
    #: example: 1234
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    #: example: True
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
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[VoicemailInfoSendBusyCallsGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None


class SequentialRingCriteriaGetScheduleType(str, Enum):
    #: Indicates schedule is of type `holidays`.
    holidays = 'holidays'
    #: Indicates schedule is of type `businessHours`.
    business_hours = 'businessHours'


class SequentialRingCriteriaGetScheduleLevel(str, Enum):
    #: Indicates schedule specified is of `GROUP` level.
    group = 'GROUP'


class SequentialRingCriteriaGetCallsFrom(str, Enum):
    #: Indicates sequential ring criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Indicates that sequential ring criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'


class SequentialRingCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: This indicates the type of schedule.
    #: example: holidays
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: This indicates the level of the schedule specified by `scheduleName`.
    #: example: GROUP
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: This indicates if criteria are applicable for calls from any phone number or selected phone numbers.
    #: example: SELECT_PHONE_NUMBERS
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true` incoming calls from private numbers are allowed. This is only applicable when `callsFrom` is set to
    #: `SELECT_PHONE_NUMBERS`.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true` incoming calls from unavailable numbers are allowed. This is only applicable when `callsFrom` is set
    #: to `SELECT_PHONE_NUMBERS`.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone numbers for which the
    #: criteria apply.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    #: example: True
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
    #: example: +442071838750
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    #: example: True
    answer_confirmation_required_enabled: Optional[bool] = None
    #: The number of rings to the specified phone number before the call advances to the subsequent number in the
    #: sequence or goes to voicemail.
    #: example: 2
    number_of_rings: Optional[int] = None


class Source(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class SequentialRingCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates if criteria are applicable for calls from any phone number or specific phone number.
    source: Optional[Source] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    #: example: True
    ring_enabled: Optional[bool] = None


class SequentialRingGet(ApiModel):
    #: When set to `true` sequential ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: When set to `true`, the webex calling primary line will ring first.
    #: example: True
    ring_base_location_first_enabled: Optional[bool] = None
    #: The number of times the primary line will ring.
    #: example: 2
    base_location_number_of_rings: Optional[str] = None
    #: When set to `true` and the primary line is busy, the system redirects calls to the numbers configured for
    #: sequential ringing.
    #: example: True
    continue_if_base_location_is_busy_enabled: Optional[bool] = None
    #: When set to `true` calls are directed to voicemail.
    #: example: True
    calls_to_voicemail_enabled: Optional[bool] = None
    #: A list of up to five phone numbers to which calls will be directed.
    phone_numbers: Optional[list[SequentialRingNumber]] = None
    #: A list of criteria specifying conditions when sequential ringing is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None


class SimultaneousRingNumber(ApiModel):
    #: Phone number set as the sequential number.
    #: example: +19075552859
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    #: example: True
    answer_confirmation_required_enabled: Optional[bool] = None


class SimultaneousRingGet(ApiModel):
    #: Simultaneous Ring is enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when on a call.
    #: example: True
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when workspace phone receives an incoming call.
    phone_numbers: Optional[list[SimultaneousRingNumber]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    #: example: True
    criterias_enabled: Optional[bool] = None


class SelectiveRejectCallSource(str, Enum):
    #: indicates that selective reject criteria applies for all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: indicates that selective reject criteria applies for calls from specific numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: indicates that selective reject criteria applies for all forwarded calls.
    forwarded = 'FORWARDED'


class SelectiveRejectCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates if criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to reject or not to reject the calls that fit within these parameters.
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallGet(ApiModel):
    #: `true` if the Selective Reject feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective reject is in effect.
    criteria: Optional[list[SelectiveRejectCriteria]] = None


class SelectiveRejectCallCallsFromType(str, Enum):
    #: Indicates the schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Indicates the schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Indicates the schedule applies to the forwarded calls only.
    forwarded = 'FORWARDED'


class PlaceSelectiveRejectCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: Indicates the schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective reject criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective reject to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective reject to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be rejected (if rejectEnabled = `true`) or
    #: not (if rejectEnabled = `false`).
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveAcceptCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates if criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to accept or not to accept the calls that fit within these parameters.
    #: example: True
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallGet(ApiModel):
    #: `true` if the Selective Accept feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective accept is in effect.
    criteria: Optional[list[SelectiveAcceptCallCriteria]] = None


class PlaceSelectiveAcceptCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective accept is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: Indicates the schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective accept criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective accept to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective accept to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be accepted (if acceptEnabled = `true`) or
    #: not (if acceptEnabled = `false`).
    #: example: True
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
    ring_pattern: Optional[RingPattern] = None


class PlaceGetNumbersResponse(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]] = None


class PriorityAlertCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates if criteria are applicable for calls from any phone number or specific phone number.
    #: example: ALL_NUMBERS
    source: Optional[Source] = None
    #: When set to `true` notification is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    #: example: True
    notification_enabled: Optional[bool] = None


class PriorityAlertGet(ApiModel):
    #: `true` if the Priority Alert feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when priority alert is in effect.
    criteria: Optional[list[PriorityAlertCriteria]] = None


class PlacePriorityAlertCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: Indicates the schedule level i.e. Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone Numbers.
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true`, enables calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables calls even if callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` priority alerting criteria is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    #: example: True
    notification_enabled: Optional[bool] = None


class SelectiveForwardCallGet(ApiModel):
    #: `true` if the Selective Forward feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Enter the phone number to forward calls to during this schedule.
    #: example: +1934898988
    default_phone_number_to_forward: Optional[str] = None
    #: When `true`, enables a ring reminder for such calls.
    #: example: True
    ring_reminder_enabled: Optional[bool] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    destination_voicemail_enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective forward feature is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None


class PlaceSelectiveForwardCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Phone number to forward calls to during this schedule.
    #: example: +1934898988
    forward_to_phone_number: Optional[str] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Name of the location's schedule which determines when the selective forward is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Indicates the schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: Indicates the schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective forward criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true`, enables selective forward to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective forward to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be forwarded (if forwardEnabled = `true`) or
    #: not (if forwardEnabled = `false`).
    #: example: True
    forward_enabled: Optional[bool] = None


class BetaWorkspaceCallSettingsWithProfessionalLicenseApi(ApiChild, base=''):
    """
    Beta Workspace Call Settings with Professional License
    
    The Professional Workspace will provide access to all applicable configurations for a Workspace which is like a
    Professional User.
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

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
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/anonymousCallReject')
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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/anonymousCallReject')
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
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserBargeInGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/bargeIn')
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/bargeIn')
        super().put(url, params=params, json=body)

    def retrieve_do_not_disturb_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> UserDoNotDisturbGet:
        """
        Retrieve DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserDoNotDisturbGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/doNotDisturb')
        data = super().get(url, params=params)
        r = UserDoNotDisturbGet.model_validate(data)
        return r

    def modify_do_not_disturb_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                       ring_splash_enabled: bool = None, org_id: str = None):
        """
        Modify DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the DoNotDisturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: When `true`, enables ring reminder when you receive an incoming call while on Do
            Not Disturb.
        :type ring_splash_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/doNotDisturb')
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
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callBridge')
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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callBridge')
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
            access API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/pushToTalk')
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/pushToTalk')
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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def modify_privacy_settings_for_a_workspace(self, workspace_id: str, aa_extension_dialing_enabled: bool = None,
                                                aa_naming_dialing_enabled: bool = None,
                                                enable_phone_status_directory_privacy: bool = None,
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
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if monitoring_agents is not None:
            body['monitoringAgents'] = monitoring_agents
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/privacy')
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
            access API.
        :type org_id: str
        :rtype: :class:`VoicemailInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail')
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
            body['sendAllCalls'] = loads(send_all_calls.model_dump_json())
        if send_busy_calls is not None:
            body['sendBusyCalls'] = loads(send_busy_calls.model_dump_json())
        if send_unanswered_calls is not None:
            body['sendUnansweredCalls'] = loads(send_unanswered_calls.model_dump_json())
        body['notifications'] = loads(notifications.model_dump_json())
        body['transferToNumber'] = loads(transfer_to_number.model_dump_json())
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = loads(email_copy_of_message.model_dump_json())
        if message_storage is not None:
            body['messageStorage'] = loads(message_storage.model_dump_json())
        if fax_message is not None:
            body['faxMessage'] = loads(fax_message.model_dump_json())
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
        super().put(url, params=params, json=body)

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
            access API.
        :type org_id: str
        :rtype: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callPolicies')
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
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callPolicies')
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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail/actions/uploadBusyGreeting/invoke')
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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
        super().delete(url, params=params)

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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing')
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing')
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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SimultaneousRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing')
        data = super().get(url, params=params)
        r = SimultaneousRingGet.model_validate(data)
        return r

    def modify_simultaneous_ring_settings_for_a_workspace(self, workspace_id: str, criterias_enabled: bool,
                                                          enabled: bool = None,
                                                          do_not_ring_if_on_call_enabled: bool = None,
                                                          phone_numbers: list[SimultaneousRingNumber] = None,
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
        :param phone_numbers: Enter up to 10 phone numbers to ring simultaneously when workspace phone receives an
            incoming call.
        :type phone_numbers: list[SimultaneousRingNumber]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
            body['phoneNumbers'] = TypeAdapter(list[SimultaneousRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        body['criteriasEnabled'] = criterias_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        super().delete(url, params=params)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject')
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
        :param enabled: indicates whether selective reject is enabled or not.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveRejectCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveRejectCallCriteriaGet.model_validate(data)
        return r

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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        super().put(url, params=params, json=body)

    def list_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> PlaceGetNumbersResponse:
        """
        List numbers associated with a specific workspace

        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:workspaces_read`.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            can use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceGetNumbersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/numbers')
        data = super().get(url, params=params)
        r = PlaceGetNumbersResponse.model_validate(data)
        return r

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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/numbers')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        super().delete(url, params=params)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveAcceptCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept')
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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveAcceptCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveAcceptCallCriteriaGet.model_validate(data)
        return r

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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        super().delete(url, params=params)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PriorityAlertGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert')
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
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlacePriorityAlertCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        data = super().get(url, params=params)
        r = PlacePriorityAlertCriteriaGet.model_validate(data)
        return r

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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e. Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
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
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e. Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        super().delete(url, params=params)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward')
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveForwardCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveForwardCallCriteriaGet.model_validate(data)
        return r

    def create_selective_forward_criteria_for_a_workspace(self, workspace_id: str,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom,
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
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom,
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
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: Indicates the schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: Indicates the schedule level i.e, Group.
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
            token used to access API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        super().put(url, params=params, json=body)

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
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        super().delete(url, params=params)
