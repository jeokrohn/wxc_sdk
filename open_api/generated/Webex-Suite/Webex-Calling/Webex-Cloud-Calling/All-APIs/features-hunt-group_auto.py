from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AlternateNumbersWithPattern', 'CallForwardRulesGet', 'CallForwardRulesSet',
           'CallForwardSettingsGetCallForwarding', 'CallForwardSettingsGetCallForwardingAlways',
           'CallForwardSettingsGetCallForwardingOperatingModes',
           'CallForwardSettingsGetCallForwardingOperatingModesExceptionType', 'CallForwardingNumbers',
           'CallForwardingNumbersType', 'CreateForwardingRuleObjectCallsFrom',
           'CreateForwardingRuleObjectCallsFromCustomNumbers', 'CreateForwardingRuleObjectCallsFromSelection',
           'CreateForwardingRuleObjectCallsTo', 'CreateForwardingRuleObjectForwardTo',
           'CreateForwardingRuleObjectForwardToSelection', 'DirectLineCallerIdNameObject', 'FeaturesHuntGroupApi',
           'GetForwardingRuleObject', 'GetHuntGroupCallPolicyObject', 'GetHuntGroupCallPolicyObjectBusyRedirect',
           'GetHuntGroupCallPolicyObjectNoAnswer', 'GetHuntGroupObject', 'GetPersonPlaceVirtualLineHuntGroupObject',
           'HuntGroupCallForwardAvailableNumberObject', 'HuntGroupCallForwardAvailableNumberObjectOwner',
           'HuntGroupPrimaryAvailableNumberObject', 'HuntPolicySelection', 'ListHuntGroupObject', 'ModesGet',
           'ModesGetForwardTo', 'ModesGetForwardToDefaultForwardToSelection', 'ModesGetLevel', 'ModesGetType',
           'ModesPatch', 'ModesPatchForwardTo', 'ModifyCallForwardingObjectCallForwarding', 'NumberOwnerType',
           'PostHuntGroupCallPolicyObject', 'PostHuntGroupCallPolicyObjectNoAnswer',
           'PostPersonPlaceVirtualLineHuntGroupObject', 'RingPatternObject', 'STATE', 'SelectionObject',
           'TelephonyType']


class RingPatternObject(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumbersWithPattern(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str] = None
    #: Ring pattern for when this alternate number is called. Only available when `distinctiveRing` is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPatternObject] = None


class CallForwardRulesGet(ApiModel):
    #: Unique ID for the rule.
    id: Optional[str] = None
    #: Unique name of rule.
    name: Optional[str] = None
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use `Any private Number` in the comma-separated value to indicate rules that match incoming calls
    #: from a private number. Use `Any unavailable number` in the comma-separated value to match incoming calls from
    #: an unavailable number.
    call_from: Optional[str] = None
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str] = None
    #: Reflects if rule is enabled.
    enabled: Optional[bool] = None


class CallForwardRulesSet(ApiModel):
    #: Unique ID for the rule.
    id: Optional[str] = None
    #: Reflects if rule is enabled.
    enabled: Optional[bool] = None


class CallForwardSettingsGetCallForwardingAlways(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardSettingsGetCallForwardingOperatingModesExceptionType(str, Enum):
    #: The mode was switched to or extended by the user for manual switch back and runs as an exception until the user
    #: manual switches the feature back to normal operation or a different mode.
    manual_switch_back = 'MANUAL_SWITCH_BACK'
    #: The mode was switched to by the user before its start time and runs as an exception until its end time is
    #: reached at which point it automatically switches the feature back to normal operation.
    automatic_switch_back_early_start = 'AUTOMATIC_SWITCH_BACK_EARLY_START'
    #: The current mode was extended by the user before its end time and runs as an exception until the extension end
    #: time (mode's end time + extension of up to 12 hours) is reached at which point it automatically switches the
    #: feature back to normal operation.
    automatic_switch_back_extension = 'AUTOMATIC_SWITCH_BACK_EXTENSION'
    #: The mode will remain the current operating mode for the feature until its normal end time is reached.
    automatic_switch_back_standard = 'AUTOMATIC_SWITCH_BACK_STANDARD'


class ModesGetType(str, Enum):
    #: The operating mode is not scheduled.
    none_ = 'NONE'
    #: Single time duration for Monday-Friday and single time duration for Saturday-Sunday.
    same_hours_daily = 'SAME_HOURS_DAILY'
    #: Individual time durations for every day of the week.
    different_hours_daily = 'DIFFERENT_HOURS_DAILY'
    #: Holidays which have date durations spanning multiple days, as well as an optional yearly recurrence by day or
    #: date.
    holiday = 'HOLIDAY'


class ModesGetLevel(str, Enum):
    #: The operating mode is at the location level.
    location = 'LOCATION'
    #: The operating mode is at the organization level.
    organization = 'ORGANIZATION'


class CreateForwardingRuleObjectForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination for the hunt group.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardToDefaultForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardTo(ApiModel):
    #: The selection for forwarding.
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    destination: Optional[str] = None
    #: Sending incoming calls to voicemail is enabled/disabled when the destination is an internal phone number and
    #: that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's destination.
    default_destination: Optional[str] = None
    #: The operating mode's destination voicemail enabled.
    default_destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's forward to selection.
    default_forward_to_selection: Optional[ModesGetForwardToDefaultForwardToSelection] = None


class ModesGet(ApiModel):
    #: Normal operation is enabled or disabled.
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    id: Optional[str] = None
    #: The name of the operating mode.
    name: Optional[str] = None
    #: The type of the operating mode.
    type: Optional[ModesGetType] = None
    #: The level of the operating mode.
    level: Optional[ModesGetLevel] = None
    #: Forward to settings.
    forward_to: Optional[ModesGetForwardTo] = None


class CallForwardSettingsGetCallForwardingOperatingModes(ApiModel):
    #: Operating modes are enabled or disabled.
    enabled: Optional[bool] = None
    #: The ID of the current operating mode.
    current_operating_mode_id: Optional[str] = None
    #: The exception type.
    exception_type: Optional[CallForwardSettingsGetCallForwardingOperatingModesExceptionType] = None
    #: Operating modes.
    modes: Optional[list[ModesGet]] = None


class CallForwardSettingsGetCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesGet]] = None
    #: Settings related to operating modes.
    operating_modes: Optional[CallForwardSettingsGetCallForwardingOperatingModes] = None


class CallForwardingNumbersType(str, Enum):
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is a primary
    #: number or extension.
    primary = 'PRIMARY'
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is an
    #: alternate number or extension.
    alternate = 'ALTERNATE'


class CallForwardingNumbers(ApiModel):
    #: Only return call queues with matching primary phone number or extension.
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue.
    extension: Optional[str] = None
    #: Type of
    type: Optional[CallForwardingNumbersType] = None


class CreateForwardingRuleObjectForwardTo(ApiModel):
    #: Controls what happens when the rule matches.
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: Phone number used if selection is `FORWARD_TO_SPECIFIED_NUMBER`.
    phone_number: Optional[str] = None


class CreateForwardingRuleObjectCallsFromSelection(str, Enum):
    #: Rule matches for calls from any number.
    any = 'ANY'
    #: Rule matches based on the numbers and options in `customNumbers`.
    custom = 'CUSTOM'


class CreateForwardingRuleObjectCallsFromCustomNumbers(ApiModel):
    #: Match if caller ID indicates the call is from a private number.
    private_number_enabled: Optional[bool] = None
    #: Match if caller ID is unavailable.
    unavailable_number_enabled: Optional[bool] = None
    #: Array of number strings to be matched against incoming caller ID.
    numbers: Optional[list[str]] = None


class CreateForwardingRuleObjectCallsFrom(ApiModel):
    #: If `CUSTOM`, use `customNumbers` to specify which incoming caller ID values cause this rule to match. `ANY`
    #: means any incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[CreateForwardingRuleObjectCallsFromSelection] = None
    #: Custom rules for matching incoming caller ID information.
    custom_numbers: Optional[CreateForwardingRuleObjectCallsFromCustomNumbers] = None


class CreateForwardingRuleObjectCallsTo(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardingNumbers]] = None


class HuntPolicySelection(str, Enum):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next
    #: available agent. This is supported for `SKILL_BASED`.
    circular = 'CIRCULAR'
    #: Send the call through the queue of agents in order, starting from the top each time. This is supported for
    #: `SKILL_BASED`.
    regular = 'REGULAR'
    #: Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has
    #: been idle the second longest, and so on until the call is answered. This is supported for `SKILL_BASED`.
    uniform = 'UNIFORM'
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100%).
    weighted = 'WEIGHTED'


class PostHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the `nextAgentRings` has occurred.
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and `nextAgentEnabled` is true.
    next_agent_rings: Optional[int] = None
    #: If `true`, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Number of rings before forwarding calls if `forwardEnabled` is true.
    number_of_rings: Optional[int] = None
    #: Destination if `forwardEnabled` is True.
    destination: Optional[str] = None
    #: If `forwardEnabled` is true, enables and disables sending incoming to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled. If
    #: `destinationVoicemailEnabled` is enabled, then *55 is added as a prefix for `destination`.
    destination_voicemail_enabled: Optional[bool] = None


class GetHuntGroupCallPolicyObjectBusyRedirect(ApiModel):
    #: If `true`, calls are diverted to a defined phone number when all agents are busy, or when the hunt group busy
    #: status is set to busy.
    enabled: Optional[bool] = None
    #: Destination for busy redirect.
    destination: Optional[str] = None
    #: The enabled or disabled state of sending diverted incoming calls to the `destination` number's voicemail if the
    #: `destination` is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class PostHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy used to dispatch calls to agents.
    policy: Optional[HuntPolicySelection] = None
    #: If `false`, then the option is treated as "Advance when busy". The hunt group won't ring agents when they're on
    #: a call and advances to the next agent. If a hunt group agent has call waiting enabled and the call is advanced
    #: to them, the call waits until that hunt group agent isn't busy.
    waiting_enabled: Optional[bool] = None
    #: If `true`, the hunt group busy status will be set to busy. All new calls will get busy treatment. If
    #: `busyRedirect` is enabled, the calls are routed to the destination specified in `busyRedirect`.
    group_busy_enabled: Optional[bool] = None
    #: If true, agents can change the hunt group busy status.
    allow_members_to_control_group_busy_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[PostHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a specified destination when all agents are busy or when the hunt group busy
    #: status is set to busy.
    busy_redirect: Optional[GetHuntGroupCallPolicyObjectBusyRedirect] = None
    #: Settings for sending calls to a specified destination if the phone is not connected to the network for any
    #: reason, such as a power outage, failed internet connection, or wiring problem.
    business_continuity_redirect: Optional[GetHuntGroupCallPolicyObjectBusyRedirect] = None


class PostPersonPlaceVirtualLineHuntGroupObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    weight: Optional[str] = None


class SelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this hunt group.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `name` is to be shown for this hunt group.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `DISPLAY_NAME`.
    selection: Optional[SelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class GetForwardingRuleObject(ApiModel):
    #: Unique name for the selective rule in the hunt group.
    name: Optional[str] = None
    #: Unique ID for the rule.
    id: Optional[str] = None
    #: Reflects if rule is enabled.
    enabled: Optional[bool] = None
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str] = None
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CreateForwardingRuleObjectForwardTo] = None
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CreateForwardingRuleObjectCallsFrom] = None
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CreateForwardingRuleObjectCallsTo] = None


class GetHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the `nextAgentRings` has occurred.
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and `nextAgentEnabled` is true.
    next_agent_rings: Optional[int] = None
    #: If `true`, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Destination if `forwardEnabled` is True.
    destination: Optional[str] = None
    #: Number of rings before forwarding calls if `forwardEnabled` is true.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None
    #: If `destinationVoicemailEnabled` is true, enables and disables sending incoming to destination number's
    #: voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class GetHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy used to dispatch calls to agents.
    policy: Optional[HuntPolicySelection] = None
    #: If `false`, then the option is treated as "Advance when busy". The hunt group won't ring agents when they're on
    #: a call and advances to the next agent. If a hunt group agent has call waiting enabled and the call is advanced
    #: to them, the call waits until that hunt group agent isn't busy.
    waiting_enabled: Optional[bool] = None
    #: When `true`, the hunt group busy status will be set to busy. All new calls will get busy treatment. If
    #: `busyRedirect` is enabled, the calls are routed to the destination specified in `busyRedirect`.
    group_busy_enabled: Optional[bool] = None
    #: When `true`, agents can change the hunt group busy status.
    allow_members_to_control_group_busy_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[GetHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a specified destination when all agents are busy or when the hunt group busy
    #: status is set to busy.
    busy_redirect: Optional[GetHuntGroupCallPolicyObjectBusyRedirect] = None
    #: Settings for sending calls to a specified destination if the phone is not connected to the network for any
    #: reason, such as a power outage, failed internet connection, or wiring problem.
    business_continuity_redirect: Optional[GetHuntGroupCallPolicyObjectBusyRedirect] = None


class GetPersonPlaceVirtualLineHuntGroupObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: First name of person, workspace or virtual line.
    first_name: Optional[str] = None
    #: Last name of person, workspace or virtual line.
    last_name: Optional[str] = None
    #: Phone number of person, workspace or virtual line.
    phone_number: Optional[str] = None
    #: Extension of person, workspace or virtual line.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    weight: Optional[str] = None


class GetHuntGroupObject(ApiModel):
    #: A unique identifier for the hunt group.
    id: Optional[str] = None
    #: Unique name for the hunt group.
    name: Optional[str] = None
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool] = None
    #: Primary phone number of the hunt group.
    phone_number: Optional[str] = None
    #: Extension of the hunt group.
    extension: Optional[str] = None
    #: Whether or not the hunt group has the distinctive ring option enabled.
    distinctive_ring: Optional[bool] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None
    #: Language for hunt group.
    language: Optional[str] = None
    #: Language code for hunt group.
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to `.`. This field has been
    #: deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to phone number if set,
    #: otherwise defaults to call group name. This field has been deprecated. Please use `directLineCallerIdName` and
    #: `dialByName` instead.
    last_name: Optional[str] = None
    #: Time zone for the hunt group.
    time_zone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[GetHuntGroupCallPolicyObject] = None
    #: People, workspaces and virtual lines that are eligible to  receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineHuntGroupObject]] = None
    #: Whether or not the hunt group can be used as the caller ID when the agent places outgoing calls.
    hunt_group_caller_id_for_outgoing_calls_enabled: Optional[bool] = None
    #: Settings for the direct line caller ID name to be shown for this hunt group.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The name to be used for dial by name functions.
    dial_by_name: Optional[str] = None


class ListHuntGroupObject(ApiModel):
    #: A unique identifier for the hunt group.
    id: Optional[str] = None
    #: Unique name for the hunt group.
    name: Optional[str] = None
    #: Name of the location for the hunt group.
    location_name: Optional[str] = None
    #: ID of location for hunt group.
    location_id: Optional[str] = None
    #: Primary phone number of the hunt group.
    phone_number: Optional[str] = None
    #: Primary phone extension of the hunt group.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool] = None


class ModesPatchForwardTo(ApiModel):
    #: The selection for forwarding.
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    destination: Optional[str] = None
    #: Sending incoming calls to voicemail is enabled/disabled when the destination is an internal phone number and
    #: that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class ModesPatch(ApiModel):
    #: Normal operation is enabled or disabled.
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    id: Optional[str] = None
    #: Forward to settings.
    forward_to: Optional[ModesPatchForwardTo] = None


class ModifyCallForwardingObjectCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesSet]] = None
    #: Configuration for forwarding via Operating modes (Schedule Based Routing).
    modes: Optional[list[ModesPatch]] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class HuntGroupPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
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


class HuntGroupCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
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


class HuntGroupCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
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
    owner: Optional[HuntGroupCallForwardAvailableNumberObjectOwner] = None


class FeaturesHuntGroupApi(ApiChild, base='telephony/config'):
    """
    Features:  Hunt Group
    
    Features: Hunt Group supports reading and writing of Webex Calling Hunt Group settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_hunt_groups(self, location_id: str = None, name: str = None, phone_number: str = None,
                                     org_id: str = None, **params) -> Generator[ListHuntGroupObject, None, None]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Only return hunt groups with matching location ID.
        :type location_id: str
        :param name: Only return hunt groups with the matching name.
        :type name: str
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List hunt groups for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListHuntGroupObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('huntGroups')
        return self.session.follow_pagination(url=url, model=ListHuntGroupObject, item_key='huntGroups', params=params)

    def create_a_hunt_group(self, location_id: str, name: str, call_policies: PostHuntGroupCallPolicyObject,
                            agents: list[PostPersonPlaceVirtualLineHuntGroupObject], enabled: bool,
                            phone_number: str = None, extension: str = None, language_code: str = None,
                            first_name: str = None, last_name: str = None, time_zone: str = None,
                            hunt_group_caller_id_for_outgoing_calls_enabled: bool = None,
                            direct_line_caller_id_name: DirectLineCallerIdNameObject = None, dial_by_name: str = None,
                            org_id: str = None) -> str:
        """
        Create a Hunt Group

        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Creating a hunt group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param name: Unique name for the hunt group.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, workspaces and virtual lines that are eligible to  receive calls.
        :type agents: list[PostPersonPlaceVirtualLineHuntGroupObject]
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param phone_number: Primary phone number of the hunt group. Either phone number or extension are required.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group. Either phone number or extension are required.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to `.`.
            This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param hunt_group_caller_id_for_outgoing_calls_enabled: Enable the hunt group to be used as the caller ID when
            the agent places outgoing calls. When set to true the hunt group's caller ID will be used.
        :type hunt_group_caller_id_for_outgoing_calls_enabled: bool
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this hunt group.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: The name to be used for dial by name functions.  Characters of `%`,  `+`, `\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_name: str
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        body['callPolicies'] = call_policies.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineHuntGroupObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        body['enabled'] = enabled
        if hunt_group_caller_id_for_outgoing_calls_enabled is not None:
            body['huntGroupCallerIdForOutgoingCallsEnabled'] = hunt_group_caller_id_for_outgoing_calls_enabled
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/huntGroups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_hunt_group_alternate_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[HuntGroupPrimaryAvailableNumberObject, None, None]:
        """
        Get Hunt Group Alternate Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the hunt group's alternate
        phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

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
        :return: Generator yielding :class:`HuntGroupPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/huntGroups/alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=HuntGroupPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_hunt_group_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[HuntGroupPrimaryAvailableNumberObject, None, None]:
        """
        Get Hunt Group Primary Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the hunt group's primary phone
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

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
        :return: Generator yielding :class:`HuntGroupPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/huntGroups/availableNumbers')
        return self.session.follow_pagination(url=url, model=HuntGroupPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_hunt_group_call_forward_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                            owner_name: str = None, extension: str = None,
                                                            org_id: str = None,
                                                            **params) -> Generator[HuntGroupCallForwardAvailableNumberObject, None, None]:
        """
        Get Hunt Group Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the hunt group's call forward
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

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
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`HuntGroupCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'locations/{location_id}/huntGroups/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=HuntGroupCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def delete_a_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None):
        """
        Delete a Hunt Group

        Delete the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Deleting a hunt group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param hunt_group_id: Delete the hunt group with the matching ID.
        :type hunt_group_id: str
        :param org_id: Delete the hunt group from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        super().delete(url, params=params)

    def get_details_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                     org_id: str = None) -> GetHuntGroupObject:
        """
        Get Details for a Hunt Group

        Retrieve Hunt Group details.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Retrieving hunt group details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for the hunt group with this identifier.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str
        :rtype: :class:`GetHuntGroupObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        data = super().get(url, params=params)
        r = GetHuntGroupObject.model_validate(data)
        return r

    def update_a_hunt_group(self, location_id: str, hunt_group_id: str, enabled: bool = None, name: str = None,
                            phone_number: str = None, extension: str = None, distinctive_ring: bool = None,
                            alternate_numbers: list[AlternateNumbersWithPattern] = None, language_code: str = None,
                            first_name: str = None, last_name: str = None, time_zone: str = None,
                            call_policies: PostHuntGroupCallPolicyObject = None,
                            agents: list[PostPersonPlaceVirtualLineHuntGroupObject] = None,
                            hunt_group_caller_id_for_outgoing_calls_enabled: bool = None,
                            direct_line_caller_id_name: DirectLineCallerIdNameObject = None, dial_by_name: str = None,
                            org_id: str = None):
        """
        Update a Hunt Group

        Update the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Updating a hunt group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param hunt_group_id: Update settings for the hunt group with the matching ID.
        :type hunt_group_id: str
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param name: Unique name for the hunt group.
        :type name: str
        :param phone_number: Primary phone number of the hunt group.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group.
        :type extension: str
        :param distinctive_ring: Whether or not the hunt group has the distinctive ring option enabled.
        :type distinctive_ring: bool
        :param alternate_numbers: The alternate numbers feature allows you to assign multiple phone numbers or
            extensions to a hunt group. Each number will reach the same greeting and each menu will function
            identically to the main number. The alternate numbers option enables you to have up to ten (10) phone
            numbers ring into the hunt group.
        :type alternate_numbers: list[AlternateNumbersWithPattern]
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to `.`.
            This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, workspaces and virtual lines that are eligible to  receive calls.
        :type agents: list[PostPersonPlaceVirtualLineHuntGroupObject]
        :param hunt_group_caller_id_for_outgoing_calls_enabled: Enable the hunt group to be used as the caller ID when
            the agent places outgoing calls. When set to true the hunt group's caller ID will be used.
        :type hunt_group_caller_id_for_outgoing_calls_enabled: bool
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this hunt group.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: Sets or clears the name to be used for dial by name functions. To clear the `dialByName`,
            the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and Unicode
            characters are not allowed.
        :type dial_by_name: str
        :param org_id: Update hunt group settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if distinctive_ring is not None:
            body['distinctiveRing'] = distinctive_ring
        if alternate_numbers is not None:
            body['alternateNumbers'] = TypeAdapter(list[AlternateNumbersWithPattern]).dump_python(alternate_numbers, mode='json', by_alias=True, exclude_none=True)
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if call_policies is not None:
            body['callPolicies'] = call_policies.model_dump(mode='json', by_alias=True, exclude_none=True)
        if agents is not None:
            body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineHuntGroupObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        if hunt_group_caller_id_for_outgoing_calls_enabled is not None:
            body['huntGroupCallerIdForOutgoingCallsEnabled'] = hunt_group_caller_id_for_outgoing_calls_enabled
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        super().put(url, params=params, json=body)

    def get_call_forwarding_settings_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                                      org_id: str = None) -> CallForwardSettingsGetCallForwarding:
        """
        Get Call Forwarding Settings for a Hunt Group

        Retrieve Call Forwarding settings for the specified Hunt Group including the list of call forwarding rules.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Retrieving call forwarding settings for a hunt group requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Read the call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group forwarding settings from this organization.
        :type org_id: str
        :rtype: CallForwardSettingsGetCallForwarding
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardSettingsGetCallForwarding.model_validate(data['callForwarding'])
        return r

    def update_call_forwarding_settings_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                                         call_forwarding: ModifyCallForwardingObjectCallForwarding = None,
                                                         org_id: str = None):
        """
        Update Call Forwarding Settings for a Hunt Group

        Update Call Forwarding settings for the specified Hunt Group.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Updating call forwarding settings for a hunt group requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location from which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param call_forwarding: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
        :type call_forwarding: ModifyCallForwardingObjectCallForwarding
        :param org_id: Update hunt group forwarding settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        super().put(url, params=params, json=body)

    def switch_mode_for_call_forwarding_settings_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                                                  org_id: str = None):
        """
        Switch Mode for Call Forwarding Settings for a Hunt Group

        Switches the current operating mode of the `Hunt Group` to the mode as per normal operations.

        Switching operating mode for a `hunt group` requires a full, or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: `Location` in which this `hunt group` exists.
        :type location_id: str
        :param hunt_group_id: Switch operating mode to normal operations for this `hunt group`.
        :type hunt_group_id: str
        :param org_id: Switch operating mode as per normal operations for the `hunt group` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/actions/switchMode/invoke')
        super().post(url, params=params)

    def create_a_selective_call_forwarding_rule_for_a_hunt_group(self, location_id: str, hunt_group_id: str, name: str,
                                                                 calls_from: CreateForwardingRuleObjectCallsFrom,
                                                                 calls_to: CreateForwardingRuleObjectCallsTo,
                                                                 enabled: bool = None, holiday_schedule: str = None,
                                                                 business_schedule: str = None,
                                                                 forward_to: CreateForwardingRuleObjectForwardTo = None,
                                                                 org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule for a Hunt Group

        Create a Selective Call Forwarding Rule for the designated Hunt Group.

        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.

        Creating a selective call forwarding rule for a hunt group requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Create the rule for this hunt group.
        :type hunt_group_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CreateForwardingRuleObjectCallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CreateForwardingRuleObjectCallsTo
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CreateForwardingRuleObjectForwardTo
        :param org_id: Create the hunt group rule for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['callsFrom'] = calls_from.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['callsTo'] = calls_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_selective_call_forwarding_rule_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                                                 rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for a Hunt Group

        Delete a Selective Call Forwarding Rule for the designated Hunt Group.

        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.

        Deleting a selective call forwarding rule for a hunt group requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Delete the rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are deleting.
        :type rule_id: str
        :param org_id: Delete hunt group rule from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url, params=params)

    def get_selective_call_forwarding_rule_for_a_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str,
                                                            org_id: str = None) -> GetForwardingRuleObject:
        """
        Get Selective Call Forwarding Rule for a Hunt Group

        Retrieve a Selective Call Forwarding Rule's settings for the designated Hunt Group.

        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.

        Retrieving a selective call forwarding rule's settings for a hunt group requires a full or read-only
        administrator or location administrator auth token with a scope of `spark-admin:telephony_config_read`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve hunt group rule settings for this organization.
        :type org_id: str
        :rtype: :class:`GetForwardingRuleObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url, params=params)
        r = GetForwardingRuleObject.model_validate(data)
        return r

    def update_a_selective_call_forwarding_rule_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                                                 rule_id: str, name: str = None, enabled: bool = None,
                                                                 holiday_schedule: str = None,
                                                                 business_schedule: str = None,
                                                                 forward_to: CreateForwardingRuleObjectForwardTo = None,
                                                                 calls_from: CreateForwardingRuleObjectCallsFrom = None,
                                                                 calls_to: CreateForwardingRuleObjectCallsTo = None,
                                                                 org_id: str = None) -> str:
        """
        Update a Selective Call Forwarding Rule for a Hunt Group

        Update a Selective Call Forwarding Rule's settings for the designated Hunt Group.

        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.

        Updating a selective call forwarding rule's settings for a hunt group requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are updating settings for.
        :type rule_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CreateForwardingRuleObjectForwardTo
        :param calls_from: Settings related the rule matching based on incoming caller ID.
        :type calls_from: CreateForwardingRuleObjectCallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CreateForwardingRuleObjectCallsTo
        :param org_id: Update hunt group rule settings for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calls_from is not None:
            body['callsFrom'] = calls_from.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calls_to is not None:
            body['callsTo'] = calls_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r
