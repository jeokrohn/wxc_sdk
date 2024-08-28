from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AlternateNumbersWithPattern', 'AnnouncementAudioFileGet', 'AnnouncementAudioFileGetLevel',
           'AudioAnnouncementFileFeatureGetObject', 'AudioAnnouncementFileFeatureGetObjectMediaFileType',
           'AvailableAgentObject', 'CallForwardRulesGet', 'CallForwardRulesSet',
           'CallForwardSettingsGetCallForwarding', 'CallForwardSettingsGetCallForwardingAlways',
           'CallForwardingNumbers', 'CallForwardingNumbersType', 'CallQueueCallForwardAvailableNumberObject',
           'CallQueueCallForwardAvailableNumberObjectOwner', 'CallQueueHolidaySchedulesObject',
           'CallQueueHolidaySchedulesObjectScheduleLevel', 'CallQueuePrimaryAvailableNumberObject',
           'CallQueueQueueSettingsGetObject', 'CallQueueQueueSettingsGetObjectComfortMessage',
           'CallQueueQueueSettingsGetObjectComfortMessageBypass', 'CallQueueQueueSettingsGetObjectMohMessage',
           'CallQueueQueueSettingsGetObjectMohMessageNormalSource', 'CallQueueQueueSettingsGetObjectOverflow',
           'CallQueueQueueSettingsGetObjectOverflowAction', 'CallQueueQueueSettingsGetObjectOverflowGreeting',
           'CallQueueQueueSettingsGetObjectWaitMessage', 'CallQueueQueueSettingsGetObjectWaitMessageWaitMode',
           'CallQueueQueueSettingsGetObjectWelcomeMessage', 'CreateCallQueueObjectCallingLineIdPolicy',
           'CreateForwardingRuleObjectCallsFrom', 'CreateForwardingRuleObjectCallsFromCustomNumbers',
           'CreateForwardingRuleObjectCallsFromSelection', 'CreateForwardingRuleObjectCallsTo',
           'CreateForwardingRuleObjectForwardTo', 'CreateForwardingRuleObjectForwardToSelection',
           'FeaturesCallQueueApi', 'GetAnnouncementFileInfo', 'GetCallQueueCallPolicyObject',
           'GetCallQueueCallPolicyObjectCallBounce', 'GetCallQueueCallPolicyObjectDistinctiveRing',
           'GetCallQueueForcedForwardObject', 'GetCallQueueHolidayObject', 'GetCallQueueHolidayObjectAction',
           'GetCallQueueNightServiceObject', 'GetCallQueueNightServiceObjectAnnouncementMode', 'GetCallQueueObject',
           'GetCallQueueObjectAlternateNumberSettings', 'GetCallQueueStrandedCallsObject',
           'GetCallQueueStrandedCallsObjectAction', 'GetForwardingRuleObject',
           'GetPersonPlaceVirtualLineCallQueueObject', 'GetPersonPlaceVirtualLineCallQueueObjectType',
           'GetUserNumberItemObject', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'ListCallQueueObject',
           'LocationObject', 'MediaType', 'ModifyCallForwardingObjectCallForwarding',
           'ModifyPersonPlaceVirtualLineCallQueueObject', 'NumberOwnerType',
           'PostPersonPlaceVirtualLineCallQueueObject', 'RingPatternObject', 'STATE', 'TelephonyType']


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
    #: example: +12225555309
    phone_number: Optional[str] = None
    #: Ring pattern for when this alternate number is called. Only available when `distinctiveRing` is enabled for the
    #: hunt group.
    #: example: NORMAL
    ring_pattern: Optional[RingPatternObject] = None


class AnnouncementAudioFileGetLevel(str, Enum):
    location = 'LOCATION'
    organization = 'ORGANIZATION'
    entity = 'ENTITY'


class AnnouncementAudioFileGet(ApiModel):
    #: Unique identifier of the Announcement file.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8zMjAxNjRmNC1lNWEzLTQxZmYtYTMyNi02N2MwOThlNDFkMWQ
    id: Optional[str] = None
    #: Name of the announcement file.
    #: example: Public_Announcement.wav
    name: Optional[str] = None
    #: Media file type of announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: The level at which this announcement exists.
    #: example: LOCATION
    level: Optional[AnnouncementAudioFileGetLevel] = None


class AudioAnnouncementFileFeatureGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    d3_gp = '3GP'


class AudioAnnouncementFileFeatureGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    file_name: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    media_file_type: Optional[AudioAnnouncementFileFeatureGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    #: example: ORGANIZATION
    level: Optional[AnnouncementAudioFileGetLevel] = None


class CallForwardRulesGet(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: Unique name of rule.
    #: example: My Rule
    name: Optional[str] = None
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use `Any private Number` in the comma-separated value to indicate rules that match incoming calls
    #: from a private number. Use `Any unavailable number` in the comma-separated value to match incoming calls from
    #: an unavailable number.
    #: example: Any private Number,2025551212
    call_from: Optional[str] = None
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    #: example: Primary
    calls_to: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    #: example: 2025557736
    forward_to: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None


class CallForwardRulesSet(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None


class CallForwardSettingsGetCallForwardingAlways(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
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


class CallForwardSettingsGetCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesGet]] = None


class CallForwardingNumbersType(str, Enum):
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is a primary
    #: number or extension.
    primary = 'PRIMARY'
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is an
    #: alternate number or extension.
    alternate = 'ALTERNATE'


class CallForwardingNumbers(ApiModel):
    #: Only return call queues with matching primary phone number or extension.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue.
    #: example: 7781
    extension: Optional[str] = None
    #: Type of
    #: example: PRIMARY
    type: Optional[CallForwardingNumbersType] = None


class CallQueueHolidaySchedulesObjectScheduleLevel(str, Enum):
    #: Specifies this Schedule is configured across location.
    location = 'LOCATION'
    #: Specifies this Schedule is configured across organization.
    organization = 'ORGANIZATION'


class CallQueueHolidaySchedulesObject(ApiModel):
    #: Name of the schedule configured for a holiday service.
    #: example: 2022 All Holidays
    schedule_name: Optional[str] = None
    #: Specifies whether the schedule mentioned in `scheduleName` is org or location specific.
    #: example: LOCATION
    schedule_level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None


class CallQueueQueueSettingsGetObjectOverflowAction(str, Enum):
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class CallQueueQueueSettingsGetObjectOverflowGreeting(str, Enum):
    #: Play the custom announcement specified by the `fileName` field.
    custom = 'CUSTOM'
    #: Play default announcement.
    default = 'DEFAULT'


class CallQueueQueueSettingsGetObjectOverflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    #: example: PERFORM_BUSY_TREATMENT
    action: Optional[CallQueueQueueSettingsGetObjectOverflowAction] = None
    #: When `true`, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external `transferNumber` is entered.
    send_to_voicemail: Optional[bool] = None
    #: Destination number for overflow calls when `action` is set to `TRANSFER_TO_PHONE_NUMBER`.
    #: example: +15555551212
    transfer_number: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    #: example: True
    overflow_after_wait_enabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. The minimum
    #: value 0, The maximum value is 7200 seconds.
    #: example: 20
    overflow_after_wait_time: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by
    #: a user.
    #: example: True
    play_overflow_greeting_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `overflow` greetings. These files are from the list of announcement
    #: files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is mandatory, and the
    #: maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFileGet]] = None


class CallQueueQueueSettingsGetObjectWelcomeMessage(ApiModel):
    #: If enabled play entrance message. The default value is `true`.
    #: example: True
    enabled: Optional[bool] = None
    #: Mandatory entrance message. The default value is `false`.
    always_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `welcomeMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFileGet]] = None


class CallQueueQueueSettingsGetObjectWaitMessageWaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class CallQueueQueueSettingsGetObjectWaitMessage(ApiModel):
    #: If enabled play Wait Message.
    #: example: True
    enabled: Optional[bool] = None
    #: Estimated wait message operating mode. Supported values `TIME` and `POSITION`.
    #: example: POSITION
    wait_mode: Optional[CallQueueQueueSettingsGetObjectWaitMessageWaitMode] = None
    #: The number of minutes for which the estimated wait is played. The minimum time is 10 minutes. The maximum time
    #: is 100 minutes.
    #: example: 100
    handling_time: Optional[int] = None
    #: The default number of call handling minutes. The minimum time is 1 minutes, The maximum time is 100 minutes.
    #: example: 100
    default_handling_time: Optional[int] = None
    #: The number of the position for which the estimated wait is played. The minimum positions are 10, The maximum
    #: positions are 100.
    #: example: 100
    queue_position: Optional[int] = None
    #: Play time / Play position High Volume.
    high_volume_message_enabled: Optional[bool] = None
    #: The number of estimated waiting times in seconds. The minimum time is 10 seconds. The maximum time is 600
    #: seconds.
    #: example: 600
    estimated_waiting_time: Optional[int] = None
    #: Callback options enabled/disabled. Default value is false.
    callback_option_enabled: Optional[bool] = None
    #: The minimum estimated callback times in minutes. The default value is 30.
    #: example: 10
    minimum_estimated_callback_time: Optional[int] = None
    #: The international numbers for callback is enabled/disabled. The default value is `false`.
    international_callback_enabled: Optional[bool] = None
    #: Play updated estimated wait message.
    #: example: True
    play_updated_estimated_wait_message: Optional[bool] = None


class CallQueueQueueSettingsGetObjectComfortMessage(ApiModel):
    #: If enabled play periodic comfort message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    #: example: 10
    time_between_messages: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFileGet]] = None


class CallQueueQueueSettingsGetObjectComfortMessageBypass(ApiModel):
    #: If enabled play comfort bypass message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The
    #: minimum time is 1 seconds. The maximum time is 120 seconds.
    #: example: 10
    call_waiting_age_threshold: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessageBypass` greetings. These files are from the list of
    #: announcements files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFileGet]] = None


class CallQueueQueueSettingsGetObjectMohMessageNormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `mohMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFileGet]] = None


class CallQueueQueueSettingsGetObjectMohMessage(ApiModel):
    normal_source: Optional[CallQueueQueueSettingsGetObjectMohMessageNormalSource] = None
    alternate_source: Optional[CallQueueQueueSettingsGetObjectMohMessageNormalSource] = None


class CallQueueQueueSettingsGetObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the `overflow` settings are
    #: triggered.
    #: example: 50
    queue_size: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    #: example: True
    call_offer_tone_enabled: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsGetObjectOverflow] = None
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call
    #: queue while there is an available agent, the caller will not hear this announcement and is transferred to an
    #: agent. The welcome message feature is enabled by default.
    welcome_message: Optional[CallQueueQueueSettingsGetObjectWelcomeMessage] = None
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[CallQueueQueueSettingsGetObjectWaitMessage] = None
    #: Play a message after the welcome message and before hold music. This is typically a `CUSTOM` announcement that
    #: plays information, such as current promotions or information about products and services.
    comfort_message: Optional[CallQueueQueueSettingsGetObjectComfortMessage] = None
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that
    #: should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort
    #: message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[CallQueueQueueSettingsGetObjectComfortMessageBypass] = None
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[CallQueueQueueSettingsGetObjectMohMessage] = None
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces
    #: the identity of the call queue from which the call is coming.
    whisper_message: Optional[CallQueueQueueSettingsGetObjectMohMessageNormalSource] = None


class CreateCallQueueObjectCallingLineIdPolicy(str, Enum):
    #: Calling Line ID Policy will show the caller's direct line number.
    direct_line = 'DIRECT_LINE'
    #: Calling Line ID Policy will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Calling Line ID Policy will show the value from the `callingLineIdPhoneNumber` field.
    custom = 'CUSTOM'


class HuntRoutingTypeSelection(str, Enum):
    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based = 'PRIORITY_BASED'
    #: This option uses skill level as the criteria to route calls to agents. When there is more than one agent with
    #: the same skill level, the selected `policy` helps dispatch the calls to the agents.
    skill_based = 'SKILL_BASED'


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


class GetCallQueueCallPolicyObjectCallBounce(ApiModel):
    #: If enabled, bounce calls after the set number of rings.
    #: example: True
    call_bounce_enabled: Optional[bool] = None
    #: Number of rings after which to bounce call, if call bounce is enabled.
    #: example: 5
    call_bounce_max_rings: Optional[int] = None
    #: Bounce if agent becomes unavailable.
    #: example: True
    agent_unavailable_enabled: Optional[bool] = None
    #: Alert agent if call on hold more than `alertAgentMaxSeconds`.
    #: example: True
    alert_agent_enabled: Optional[bool] = None
    #: Number of second after which to alert agent if `alertAgentEnabled`.
    #: example: 20
    alert_agent_max_seconds: Optional[int] = None
    #: Bounce if call on hold more than `callBounceMaxSeconds`.
    #: example: True
    call_bounce_on_hold_enabled: Optional[bool] = None
    #: Number of second after which to bounce if `callBounceEnabled`.
    #: example: 20
    call_bounce_on_hold_max_seconds: Optional[int] = None


class GetCallQueueCallPolicyObjectDistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Ring pattern for when this call queue is called. Only available when `distinctiveRing` is enabled for the call
    #: queue.
    #: example: NORMAL
    ring_pattern: Optional[RingPatternObject] = None


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents.
    #: example: PRIORITY_BASED
    routing_type: Optional[HuntRoutingTypeSelection] = None
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class PostPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is `SKILL_BASED`.
    #: example: 1
    skill_level: Optional[int] = None


class CreateForwardingRuleObjectForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination for the hunt group.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class CreateForwardingRuleObjectForwardTo(ApiModel):
    #: Controls what happens when the rule matches.
    #: example: FORWARD_TO_DEFAULT_NUMBER
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: Phone number used if selection is `FORWARD_TO_SPECIFIED_NUMBER`.
    #: example: 5558675309
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
    #: example: CUSTOM
    selection: Optional[CreateForwardingRuleObjectCallsFromSelection] = None
    #: Custom rules for matching incoming caller ID information.
    custom_numbers: Optional[CreateForwardingRuleObjectCallsFromCustomNumbers] = None


class CreateForwardingRuleObjectCallsTo(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardingNumbers]] = None


class MediaType(str, Enum):
    #: WMA File Extension.
    wma = 'WMA'
    #: WAV File Extension.
    wav = 'WAV'
    #: 3GP File Extension.
    gp = 'GP'
    #: MOV File Extension.
    mov = 'MOV'


class GetAnnouncementFileInfo(ApiModel):
    #: ID of the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9kODc5YWZlZC1jNTRhLTQyOTctOGY0Mi02ZmEyMDJjN2E1M2E
    id: Optional[str] = None
    #: Name of greeting file.
    #: example: Greeting-1.wav
    file_name: Optional[str] = None
    #: Size of greeting file in kilo-bytes.
    #: example: 33456
    file_size: Optional[str] = None
    #: Media file type of the announcement.
    #: example: WAV
    media_file_type: Optional[MediaType] = None
    #: Level where the announcement is created.
    #: example: ORGANIZATION
    level: Optional[AnnouncementAudioFileGetLevel] = None


class GetCallQueueForcedForwardObject(ApiModel):
    #: Whether or not the call queue forced forward routing policy setting is enabled.
    #: example: True
    forced_forward_enabled: Optional[bool] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    #: example: 1235557890
    transfer_phone_number: Optional[str] = None
    #: Specifies if an announcement plays to callers before applying the action.
    #: example: True
    play_announcement_before_enabled: Optional[bool] = None
    #: Specifies what type of announcement to be played.
    #: example: DEFAULT
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None


class GetCallQueueHolidayObjectAction(str, Enum):
    #: The caller hears a fast-busy tone.
    busy = 'BUSY'
    #: Transfers the call to number specified in `transferPhoneNumber`.
    transfer = 'TRANSFER'


class GetCallQueueHolidayObject(ApiModel):
    #: Whether or not the call queue holiday service routing policy is enabled.
    #: example: True
    holiday_service_enabled: Optional[bool] = None
    #: Specifies call processing action type.
    #: example: BUSY
    action: Optional[GetCallQueueHolidayObjectAction] = None
    #: Specifies whether the schedule mentioned in `holidayScheduleName` is org or location specific. (Must be from
    #: `holidaySchedules` list)
    #: example: LOCATION
    holiday_schedule_level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None
    #: Name of the schedule configured for a holiday service as one of from `holidaySchedules` list.
    #: example: 2022 Holidays Period
    holiday_schedule_name: Optional[str] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    #: example: 1235557890
    transfer_phone_number: Optional[str] = None
    #: Specifies if an announcement plays to callers before applying the action.
    #: example: True
    play_announcement_before_enabled: Optional[bool] = None
    #: Specifies what type of announcement to be played.
    #: example: DEFAULT
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None
    #: Lists the pre-configured holiday schedules.
    holiday_schedules: Optional[list[CallQueueHolidaySchedulesObject]] = None


class GetCallQueueNightServiceObjectAnnouncementMode(str, Enum):
    #: Plays announcement as per `audioMessageSelection`.
    normal = 'NORMAL'
    #: Plays announcement as per `manualAudioMessageSelection`.
    manual = 'MANUAL'


class GetCallQueueNightServiceObject(ApiModel):
    #: Whether or not the call queue night service routing policy is enabled.
    #: example: True
    night_service_enabled: Optional[bool] = None
    #: Specifies call processing action type.
    #: example: TRANSFER
    action: Optional[GetCallQueueHolidayObjectAction] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    #: example: 1234
    transfer_phone_number: Optional[str] = None
    #: Specifies if an announcement plays to callers before applying the action.
    #: example: True
    play_announcement_before_enabled: Optional[bool] = None
    #: Specifies the type of announcements to played.
    #: example: NORMAL
    announcement_mode: Optional[GetCallQueueNightServiceObjectAnnouncementMode] = None
    #: Specifies what type of announcements to be played when `announcementMode` is `NORMAL`.
    #: example: DEFAULT
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None
    #: Name of the schedule configured for a night service as one of from `businessHourSchedules` list.
    #: example: Working Hour
    business_hours_name: Optional[str] = None
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from
    #: `businessHourSchedules` list).
    #: example: ORGANIZATION
    business_hours_level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: Optional[list[CallQueueHolidaySchedulesObject]] = None
    #: Force night service regardless of business hour schedule.
    #: example: True
    force_night_service_enabled: Optional[bool] = None
    #: Specifies what type of announcement to be played when `announcementMode` is `MANUAL`.
    #: example: DEFAULT
    manual_audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List Of Audio Files.
    manual_audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for the Alternate Numbers.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None


class GetPersonPlaceVirtualLineCallQueueObjectType(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81ZTk3MzFlNy1iOWQ0LTRmMWQtYjYyMi05NDgwMDhhMjkzMzM
    id: Optional[str] = None
    #: Name of the location.
    #: example: RCDN
    name: Optional[str] = None


class GetPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPersonPlaceVirtualLineCallQueueObjectType] = None
    #: First name of person, workspace or virtual line.
    #: example: Hakim
    first_name: Optional[str] = None
    #: First name of person, workspace or virtual line.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone number of person, workspace or virtual line.
    #: example: +12225555309
    phone_number: Optional[str] = None
    #: Extension of person, workspace or virtual line.
    #: example: 5309
    extension: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when the call `routingType` is `SKILL_BASED`.
    #: example: 1
    skill_level: Optional[int] = None
    #: Indicates the join status of the agent for this queue. The default value while creating call queue is `true`.
    #: example: True
    join_enabled: Optional[bool] = None
    #: Location of the call queue.
    location: Optional[LocationObject] = None


class GetCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: CallQueue-1
    name: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Language for the call queue.
    #: example: English
    language: Optional[str] = None
    #: Language code.
    #: example: en-US
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to `.`.
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the `phoneNumber` if set,
    #: otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Time zone for the call queue.
    #: example: America/Chicago
    time_zone: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: +12225555309
    phone_number: Optional[str] = None
    #: Extension of the call queue.
    #: example: 5309
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12345309
    esn: Optional[str] = None
    #: Indicate if the number is toll free.
    toll_free_number: Optional[bool] = None
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    #: example: True
    phone_number_for_outgoing_calls_enabled: Optional[bool] = None
    #: Which type of Calling Line ID Policy Selected for Call Queue.
    #: example: DIRECT_LINE
    calling_line_id_policy: Optional[CreateCallQueueObjectCallingLineIdPolicy] = None
    #: Calling line ID Phone number which will be shown if CUSTOM is selected.
    #: example: +12072342368
    calling_line_id_phone_number: Optional[str] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Policy controlling how calls are routed to `agents`.
    call_policies: Optional[GetCallQueueCallPolicyObject] = None
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsGetObject] = None
    #: Flag to indicate whether call waiting is enabled for `agents`.
    allow_call_waiting_for_agents_enabled: Optional[bool] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallQueueObject]] = None
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool] = None


class GetCallQueueStrandedCallsObjectAction(str, Enum):
    #: Call remains in the queue.
    none_ = 'NONE'
    #: Calls are removed from the queue and are provided with the Busy treatment. If the queue is configured with the
    #: Call Forwarding Busy or the Voice Messaging service, then the call is handled accordingly.
    busy = 'BUSY'
    #: Calls are removed from the queue and are transferred to the configured `transferPhoneNumber`.
    transfer = 'TRANSFER'
    #: Calls are handled according to the Night Service configuration. If the Night Service action is set to `none`,
    #: then this is equivalent to this policy being set to `none` (that is, calls remain in the queue).
    night_service = 'NIGHT_SERVICE'
    #: Calls are removed from the queue and are provided with ringing until the caller releases the call. The ringback
    #: tone played to the caller is localized according to the country code of the caller.
    ringing = 'RINGING'
    #: Calls are removed from the queue and are provided with an announcement that is played in a loop until the caller
    #: releases the call.
    announcement = 'ANNOUNCEMENT'


class GetCallQueueStrandedCallsObject(ApiModel):
    #: Specifies call processing action type.
    #: example: BUSY
    action: Optional[GetCallQueueStrandedCallsObjectAction] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    #: example: 1235557890
    transfer_phone_number: Optional[str] = None
    #: Specifies what type of announcement to be played.
    #: example: DEFAULT
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None


class GetForwardingRuleObject(ApiModel):
    #: Unique name for the selective rule in the hunt group.
    #: example: New Selective Rule
    name: Optional[str] = None
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    #: example: HolidayScheduleOne
    holiday_schedule: Optional[str] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    #: example: BusinessScheduleTwo
    business_schedule: Optional[str] = None
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CreateForwardingRuleObjectForwardTo] = None
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CreateForwardingRuleObjectCallsFrom] = None
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CreateForwardingRuleObjectCallsTo] = None


class ListCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: 5714328359
    name: Optional[str] = None
    #: Name of location for call queue.
    #: example: WXCSIVDKCPAPIC4S1
    location_name: Optional[str] = None
    #: ID of location for call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    location_id: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: +12225555309
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue.
    #: example: 5309
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12345309
    esn: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None


class ModifyCallForwardingObjectCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesSet]] = None


class ModifyPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzgzYjQ0OTIyLWZlOWYtMTFlYi1hNGI4LTMzNjI3YmVkNjdiNQ
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is `SKILL_BASED`.
    #: example: 1
    skill_level: Optional[int] = None
    #: Indicates the join status of the agent for this queue. The default value for newly added agents is `true`.
    #: example: True
    join_enabled: Optional[bool] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class CallQueuePrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
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


class CallQueueCallForwardAvailableNumberObjectOwner(ApiModel):
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


class CallQueueCallForwardAvailableNumberObject(ApiModel):
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
    owner: Optional[CallQueueCallForwardAvailableNumberObjectOwner] = None


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person, workspace or virtual line.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of a person, workspace or virtual line.
    #: example: 8080
    extension: Optional[str] = None


class AvailableAgentObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    #: example: Brown
    last_name: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    #: example: johnBrown
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPersonPlaceVirtualLineCallQueueObjectType] = None
    #: Email of a person, workspace or virtual line.
    #: example: john.brown@example.com
    email: Optional[str] = None
    #: Person has the CX Essentials license.
    #: example: True
    has_cx_essentials: Optional[bool] = None
    #: List of phone numbers of a person, workspace or virtual line.
    numbers: Optional[list[GetUserNumberItemObject]] = None


class FeaturesCallQueueApi(ApiChild, base='telephony/config'):
    """
    Features:  Call Queue
    
    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_call_queues(self, location_id: str = None, name: str = None, phone_number: str = None,
                                     org_id: str = None, **params) -> Generator[ListCallQueueObject, None, None]:
        """
        Read the List of Call Queues

        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param phone_number: Only return call queues with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List call queues for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallQueueObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('queues')
        return self.session.follow_pagination(url=url, model=ListCallQueueObject, item_key='queues', params=params)

    def create_a_call_queue(self, location_id: str, name: str, call_policies: GetCallQueueCallPolicyObject,
                            queue_settings: CallQueueQueueSettingsGetObject,
                            agents: list[PostPersonPlaceVirtualLineCallQueueObject], phone_number: str = None,
                            extension: str = None, language_code: str = None, first_name: str = None,
                            last_name: str = None, time_zone: str = None,
                            calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy = None,
                            calling_line_id_phone_number: str = None, allow_agent_join_enabled: bool = None,
                            phone_number_for_outgoing_calls_enabled: bool = None, org_id: str = None) -> str:
        """
        Create a Call Queue

        Create new Call Queues for the given location.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Creating a call queue requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param name: Unique name for the call queue.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to `agents`.
        :type call_policies: GetCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsGetObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineCallQueueObject]
        :param phone_number: Primary phone number of the call queue. Either a `phoneNumber` or `extension` is
            mandatory.
        :type phone_number: str
        :param extension: Primary phone extension of the call queue. Either a `phoneNumber` or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to
            `phoneNumber` if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the call queue.
        :type time_zone: str
        :param calling_line_id_policy: Which type of Calling Line ID Policy Selected for Call Queue.
        :type calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy
        :param calling_line_id_phone_number: Calling line ID Phone number which will be shown if CUSTOM is selected.
        :type calling_line_id_phone_number: str
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them
            to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        :param org_id: Create the call queue for this organization.
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
        body['queueSettings'] = queue_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineCallQueueObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        if calling_line_id_policy is not None:
            body['callingLineIdPolicy'] = enum_str(calling_line_id_policy)
        if calling_line_id_phone_number is not None:
            body['callingLineIdPhoneNumber'] = calling_line_id_phone_number
        if allow_agent_join_enabled is not None:
            body['allowAgentJoinEnabled'] = allow_agent_join_enabled
        if phone_number_for_outgoing_calls_enabled is not None:
            body['phoneNumberForOutgoingCallsEnabled'] = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_call_queue(self, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete a Call Queue

        Delete the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Deleting a call queue requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().delete(url, params=params)

    def get_details_for_a_call_queue(self, location_id: str, queue_id: str, org_id: str = None) -> GetCallQueueObject:
        """
        Get Details for a Call Queue

        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url, params=params)
        r = GetCallQueueObject.model_validate(data)
        return r

    def update_a_call_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsGetObject,
                            enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None,
                            last_name: str = None, time_zone: str = None, phone_number: str = None,
                            extension: str = None,
                            alternate_number_settings: GetCallQueueObjectAlternateNumberSettings = None,
                            call_policies: GetCallQueueCallPolicyObject = None,
                            calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy = None,
                            calling_line_id_phone_number: str = None,
                            allow_call_waiting_for_agents_enabled: bool = None,
                            agents: list[ModifyPersonPlaceVirtualLineCallQueueObject] = None,
                            allow_agent_join_enabled: bool = None,
                            phone_number_for_outgoing_calls_enabled: bool = None, org_id: str = None):
        """
        Update a Call Queue

        Update the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Updating a call queue requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsGetObject
        :param enabled: Whether or not the call queue is enabled.
        :type enabled: bool
        :param name: Unique name for the call queue.
        :type name: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to `.`.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the
            `phoneNumber` if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param phone_number: Primary phone number of the call queue.
        :type phone_number: str
        :param extension: Extension of the call queue.
        :type extension: str
        :param alternate_number_settings: The alternate numbers feature allows you to assign multiple phone numbers or
            extensions to a call queue. Each number will reach the same greeting and each menu will function
            identically to the main number. The alternate numbers option enables you to have up to ten (10) phone
            numbers ring into the call queue.
        :type alternate_number_settings: GetCallQueueObjectAlternateNumberSettings
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: GetCallQueueCallPolicyObject
        :param calling_line_id_policy: Which type of Calling Line ID Policy Selected for Call Queue.
        :type calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy
        :param calling_line_id_phone_number: Calling line ID Phone number which will be shown if CUSTOM is selected.
        :type calling_line_id_phone_number: str
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[ModifyPersonPlaceVirtualLineCallQueueObject]
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When `true`, indicates that the agent's configuration allows
            them to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        :param org_id: Update call queue settings from this organization.
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
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if alternate_number_settings is not None:
            body['alternateNumberSettings'] = alternate_number_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        if call_policies is not None:
            body['callPolicies'] = call_policies.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calling_line_id_policy is not None:
            body['callingLineIdPolicy'] = enum_str(calling_line_id_policy)
        if calling_line_id_phone_number is not None:
            body['callingLineIdPhoneNumber'] = calling_line_id_phone_number
        body['queueSettings'] = queue_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        if allow_call_waiting_for_agents_enabled is not None:
            body['allowCallWaitingForAgentsEnabled'] = allow_call_waiting_for_agents_enabled
        if agents is not None:
            body['agents'] = TypeAdapter(list[ModifyPersonPlaceVirtualLineCallQueueObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        if allow_agent_join_enabled is not None:
            body['allowAgentJoinEnabled'] = allow_agent_join_enabled
        if phone_number_for_outgoing_calls_enabled is not None:
            body['phoneNumberForOutgoingCallsEnabled'] = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url, params=params, json=body)

    def read_the_list_of_call_queue_announcement_files(self, location_id: str, queue_id: str,
                                                       org_id: str = None) -> list[GetAnnouncementFileInfo]:
        """
        Read the List of Call Queue Announcement Files

        List file info for all Call Queue announcement files associated with this Call Queue.

        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.

        Retrieving this list of files requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve anouncement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str
        :rtype: list[GetAnnouncementFileInfo]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetAnnouncementFileInfo]).validate_python(data['announcements'])
        return r

    def delete_a_call_queue_announcement_file(self, location_id: str, queue_id: str, file_name: str,
                                              org_id: str = None):
        """
        Delete a Call Queue Announcement File

        Delete an announcement file for the designated Call Queue.

        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.

        Deleting an announcement file for a call queue requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Delete an announcement for a call queue in this location.
        :type location_id: str
        :param queue_id: Delete an announcement for the call queue with this identifier.
        :type queue_id: str
        :type file_name: str
        :param org_id: Delete call queue announcement from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements/{file_name}')
        super().delete(url, params=params)

    def get_call_forwarding_settings_for_a_call_queue(self, location_id: str, queue_id: str,
                                                      org_id: str = None) -> CallForwardSettingsGetCallForwarding:
        """
        Get Call Forwarding Settings for a Call Queue

        Retrieve Call Forwarding settings for the designated Call Queue including the list of call forwarding rules.

        Retrieving call forwarding settings for a call queue requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve the call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Retrieve call queue forwarding settings from this organization.
        :type org_id: str
        :rtype: CallForwardSettingsGetCallForwarding
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardSettingsGetCallForwarding.model_validate(data['callForwarding'])
        return r

    def update_call_forwarding_settings_for_a_call_queue(self, location_id: str, queue_id: str,
                                                         call_forwarding: ModifyCallForwardingObjectCallForwarding = None,
                                                         org_id: str = None):
        """
        Update Call Forwarding Settings for a Call Queue

        Update Call Forwarding settings for the designated Call Queue.

        Updating call forwarding settings for a call queue requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update call forwarding settings for this call queue.
        :type queue_id: str
        :param call_forwarding: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
        :type call_forwarding: ModifyCallForwardingObjectCallForwarding
        :param org_id: Update call queue forwarding settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        super().put(url, params=params, json=body)

    def create_a_selective_call_forwarding_rule_for_a_call_queue(self, location_id: str, queue_id: str, name: str,
                                                                 calls_from: CreateForwardingRuleObjectCallsFrom,
                                                                 calls_to: CreateForwardingRuleObjectCallsTo,
                                                                 enabled: bool = None, holiday_schedule: str = None,
                                                                 business_schedule: str = None,
                                                                 forward_to: CreateForwardingRuleObjectForwardTo = None,
                                                                 org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule for a Call Queue

        Create a Selective Call Forwarding Rule for the designated Call Queue.

        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.

        Creating a selective call forwarding rule for a call queue requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param queue_id: Create the rule for this call queue.
        :type queue_id: str
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
        :param org_id: Create the call queue rule for this organization.
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_selective_call_forwarding_rule_for_a_call_queue(self, location_id: str, queue_id: str, rule_id: str,
                                                            org_id: str = None) -> GetForwardingRuleObject:
        """
        Get Selective Call Forwarding Rule for a Call Queue

        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.

        Retrieving a selective call forwarding rule's settings for a call queue requires a full or read-only
        administrator or location administrator auth token with a scope of `spark-admin:telephony_config_read`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which to call queue exists.
        :type location_id: str
        :param queue_id: Retrieve setting for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve call queue rule settings for this organization.
        :type org_id: str
        :rtype: :class:`GetForwardingRuleObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url, params=params)
        r = GetForwardingRuleObject.model_validate(data)
        return r

    def update_a_selective_call_forwarding_rule_for_a_call_queue(self, location_id: str, queue_id: str, rule_id: str,
                                                                 name: str = None, enabled: bool = None,
                                                                 holiday_schedule: str = None,
                                                                 business_schedule: str = None,
                                                                 forward_to: CreateForwardingRuleObjectForwardTo = None,
                                                                 calls_from: CreateForwardingRuleObjectCallsFrom = None,
                                                                 calls_to: CreateForwardingRuleObjectCallsTo = None,
                                                                 org_id: str = None) -> str:
        """
        Update a Selective Call Forwarding Rule for a Call Queue

        Update a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.

        Updating a selective call forwarding rule's settings for a call queue requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update settings for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are updating settings for.
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
        :param org_id: Update call queue rule settings for this organization.
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_selective_call_forwarding_rule_for_a_call_queue(self, location_id: str, queue_id: str, rule_id: str,
                                                                 org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for a Call Queue

        Delete a Selective Call Forwarding Rule for the designated Call Queue.

        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.

        Deleting a selective call forwarding rule for a call queue requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Delete the rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are deleting.
        :type rule_id: str
        :param org_id: Delete call queue rule from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url, params=params)

    def get_details_for_a_call_queue_holiday_service(self, location_id: str, queue_id: str,
                                                     org_id: str = None) -> GetCallQueueHolidayObject:
        """
        Get Details for a Call Queue Holiday Service

        Retrieve Call Queue Holiday Service details.

        Configure the call queue to route calls differently during the holidays.

        Retrieving call queue holiday service details requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueHolidayObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        data = super().get(url, params=params)
        r = GetCallQueueHolidayObject.model_validate(data)
        return r

    def update_a_call_queue_holiday_service(self, location_id: str, queue_id: str, holiday_service_enabled: bool,
                                            action: GetCallQueueHolidayObjectAction,
                                            holiday_schedule_level: CallQueueHolidaySchedulesObjectScheduleLevel,
                                            play_announcement_before_enabled: bool,
                                            audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                            holiday_schedule_name: str = None, transfer_phone_number: str = None,
                                            audio_files: list[AudioAnnouncementFileFeatureGetObject] = None,
                                            org_id: str = None):
        """
        Update a Call Queue Holiday Service

        Update the designated Call Queue Holiday Service.

        Configure the call queue to route calls differently during the holidays.

        Updating a call queue holiday service requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param holiday_service_enabled: Enable or Disable the call queue holiday service routing policy.
        :type holiday_service_enabled: bool
        :param action: Specifies call processing action type.
        :type action: GetCallQueueHolidayObjectAction
        :param holiday_schedule_level: Specifies whether the schedule mentioned in `holidayScheduleName` is org or
            location specific. (Must be from `holidaySchedules` list)
        :type holiday_schedule_level: CallQueueHolidaySchedulesObjectScheduleLevel
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param holiday_schedule_name: Name of the schedule configured for a holiday service as one of from
            `holidaySchedules` list.
        :type holiday_schedule_name: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureGetObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['holidayServiceEnabled'] = holiday_service_enabled
        body['action'] = enum_str(action)
        body['holidayScheduleLevel'] = enum_str(holiday_schedule_level)
        if holiday_schedule_name is not None:
            body['holidayScheduleName'] = holiday_schedule_name
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureGetObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        super().put(url, params=params, json=body)

    def get_details_for_a_call_queue_night_service(self, location_id: str, queue_id: str,
                                                   org_id: str = None) -> GetCallQueueNightServiceObject:
        """
        Get Details for a Call Queue Night Service

        Retrieve Call Queue Night service details.

        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.

        Retrieving call queue details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueNightServiceObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        data = super().get(url, params=params)
        r = GetCallQueueNightServiceObject.model_validate(data)
        return r

    def update_a_call_queue_night_service(self, location_id: str, queue_id: str, night_service_enabled: bool,
                                          play_announcement_before_enabled: bool,
                                          announcement_mode: GetCallQueueNightServiceObjectAnnouncementMode,
                                          audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                          force_night_service_enabled: bool,
                                          manual_audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                          action: GetCallQueueHolidayObjectAction = None,
                                          transfer_phone_number: str = None,
                                          audio_files: list[AudioAnnouncementFileFeatureGetObject] = None,
                                          business_hours_name: str = None,
                                          business_hours_level: CallQueueHolidaySchedulesObjectScheduleLevel = None,
                                          manual_audio_files: list[AudioAnnouncementFileFeatureGetObject] = None,
                                          org_id: str = None):
        """
        Update a Call Queue Night Service

        Update Call Queue Night Service details.

        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.

        Updating call queue night service details requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Update settings for the call queue night service with this identifier.
        :type queue_id: str
        :param night_service_enabled: Enable or disable call queue night service routing policy.
        :type night_service_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param announcement_mode: Specifies the type of announcements to played.
        :type announcement_mode: GetCallQueueNightServiceObjectAnnouncementMode
        :param audio_message_selection: Specifies what type of announcements to be played when `announcementMode` is
            `NORMAL`.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param force_night_service_enabled: Force night service regardless of business hour schedule.
        :type force_night_service_enabled: bool
        :param manual_audio_message_selection: Specifies what type of announcement to be played when `announcementMode`
            is `MANUAL`.
        :type manual_audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param action: Specifies call processing action type.
        :type action: GetCallQueueHolidayObjectAction
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureGetObject]
        :param business_hours_name: Name of the schedule configured for a night service as one of from
            `businessHourSchedules` list.
        :type business_hours_name: str
        :param business_hours_level: Specifies whether the above mentioned schedule is org or location specific. (Must
            be from `businessHourSchedules` list)
        :type business_hours_level: CallQueueHolidaySchedulesObjectScheduleLevel
        :param manual_audio_files: List Of pre-configured Audio Files.
        :type manual_audio_files: list[AudioAnnouncementFileFeatureGetObject]
        :param org_id: Update call queue night service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['nightServiceEnabled'] = night_service_enabled
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        body['announcementMode'] = enum_str(announcement_mode)
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureGetObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        if business_hours_name is not None:
            body['businessHoursName'] = business_hours_name
        if business_hours_level is not None:
            body['businessHoursLevel'] = enum_str(business_hours_level)
        body['forceNightServiceEnabled'] = force_night_service_enabled
        body['manualAudioMessageSelection'] = enum_str(manual_audio_message_selection)
        if manual_audio_files is not None:
            body['manualAudioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureGetObject]).dump_python(manual_audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        super().put(url, params=params, json=body)

    def get_details_for_a_call_queue_forced_forward(self, location_id: str, queue_id: str,
                                                    org_id: str = None) -> GetCallQueueForcedForwardObject:
        """
        Get Details for a Call Queue Forced Forward

        Retrieve Call Queue policy Forced Forward details.

        This policy allows calls to be temporarily diverted to a configured destination.

        Retrieving call queue Forced Forward details requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueForcedForwardObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        data = super().get(url, params=params)
        r = GetCallQueueForcedForwardObject.model_validate(data)
        return r

    def update_a_call_queue_forced_forward_service(self, location_id: str, queue_id: str, forced_forward_enabled: bool,
                                                   play_announcement_before_enabled: bool,
                                                   audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                                   transfer_phone_number: str = None,
                                                   audio_files: list[AudioAnnouncementFileFeatureGetObject] = None,
                                                   org_id: str = None):
        """
        Update a Call Queue Forced Forward service

        Update the designated Forced Forward Service.

        If the option is enabled, then incoming calls to the queue are forwarded to the configured destination. Calls
        that are already in the queue remain queued.
        The policy can be configured to play an announcement prior to proceeding with the forward.

        Updating a call queue Forced Forward service requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param forced_forward_enabled: Enable or disable call forced forward service routing policy.
        :type forced_forward_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureGetObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['forcedForwardEnabled'] = forced_forward_enabled
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureGetObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        super().put(url, params=params, json=body)

    def get_details_for_a_call_queue_stranded_calls(self, location_id: str, queue_id: str,
                                                    org_id: str = None) -> GetCallQueueStrandedCallsObject:
        """
        Get Details for a Call Queue Stranded Calls

        Allow admin to view default/configured Stranded Calls settings.

        Stranded-All agents logoff Policy: If the last agent staffing a queue “unjoins” the queue or signs out, then
        all calls in the queue become stranded.
        Stranded-Unavailable Policy: This policy allows for the configuration of the processing of calls that are in a
        staffed queue when all agents are unavailable.

        Retrieving call queue Stranded Calls details requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueStrandedCallsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        data = super().get(url, params=params)
        r = GetCallQueueStrandedCallsObject.model_validate(data)
        return r

    def update_a_call_queue_stranded_calls_service(self, location_id: str, queue_id: str,
                                                   action: GetCallQueueStrandedCallsObjectAction,
                                                   audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                                   transfer_phone_number: str = None,
                                                   audio_files: list[AudioAnnouncementFileFeatureGetObject] = None,
                                                   org_id: str = None):
        """
        Update a Call Queue Stranded Calls service

        Update the designated Call Stranded Calls Service.

        Allow admin to modify configured Stranded Calls settings.

        Updating a call queue stranded calls requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param action: Specifies call processing action type.
        :type action: GetCallQueueStrandedCallsObjectAction
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureGetObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureGetObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        super().put(url, params=params, json=body)

    def get_call_queue_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
        """
        Get Call Queue Primary Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the call queue's primary phone
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
        :return: Generator yielding :class:`CallQueuePrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/queues/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueuePrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_call_queue_alternate_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
        """
        Get Call Queue Alternate Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the call queue's alternate
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
        :return: Generator yielding :class:`CallQueuePrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/queues/alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueuePrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_call_queue_call_forward_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                            owner_name: str = None, extension: str = None,
                                                            org_id: str = None,
                                                            **params) -> Generator[CallQueueCallForwardAvailableNumberObject, None, None]:
        """
        Get Call Queue Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the call queue's call forward
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
        :return: Generator yielding :class:`CallQueueCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'locations/{location_id}/queues/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueueCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_call_queue_available_agents(self, location_id: str, name: str = None, phone_number: str = None,
                                        order: str = None, org_id: str = None,
                                        **params) -> Generator[AvailableAgentObject, None, None]:
        """
        Get Call Queue Available Agents

        List all available users, workspaces, or virtual lines that can be assigned as call queue agents.

        Available agents are users (excluding users with Webex Calling Standard license), workspaces, or virtual lines
        that can be assigned to a call queue.
        Calls from the call queue are routed to assigned agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID of the call queue. Temporary mandatory query parameter, used for
            performance reasons only and not a filter.
        :type location_id: str
        :param name: Search based on name (user first and last name combination).
        :type name: str
        :param phone_number: Search based on number or extension.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three comma-separated sort
            order fields may be specified. Available sort fields are: `userId`, `fname`, `firstname`, `lname`,
            `lastname`, `dn`, and `extension`. Sort order can be added together with each field using a hyphen, `-`.
            Available sort orders are: `asc`, and `desc`.
        :type order: str
        :param org_id: List available agents for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAgentObject` instances
        """
        params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep('queues/agents/availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgentObject, item_key='agents', params=params)
