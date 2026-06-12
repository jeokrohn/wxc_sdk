import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AgentAction', 'AlternateNumbersWithPattern', 'AnnouncementAudioFile', 'AnnouncementAudioFileLevel',
           'AudioAnnouncementFile', 'AudioAnnouncementFileFeatureGetObject',
           'AudioAnnouncementFileFeatureGetObjectMediaFileType', 'AudioAnnouncementFileFeatureObject',
           'AudioAnnouncementFileMediaFileType', 'AudioAnnouncementFileModify', 'AvailableAgentListObject',
           'AvailableAgentObject', 'AvailablePhoneNumber', 'AvailableSupervisorsListObject', 'CallForwardRulesGet',
           'CallForwardRulesSet', 'CallForwardSettingsGetCallForwarding',
           'CallForwardSettingsGetCallForwardingAlways', 'CallForwardSettingsGetCallForwardingOperatingModes',
           'CallForwardSettingsGetCallForwardingOperatingModesExceptionType', 'CallForwardingNumbers',
           'CallForwardingNumbersType', 'CallQueueCallForwardAvailableNumberObject',
           'CallQueueCallForwardAvailableNumberObjectOwner', 'CallQueueHolidaySchedulesObject',
           'CallQueueHolidaySchedulesObjectScheduleLevel', 'CallQueuePrimaryAvailableNumberObject',
           'CallQueueQueueEssentialsSettingsObject', 'CallQueueQueueEssentialsSettingsObjectOverflow',
           'CallQueueQueueSettingsGetObjectOverflowAction', 'CallQueueQueueSettingsGetObjectOverflowGreeting',
           'CallQueueQueueSettingsGetObjectWaitMessage', 'CallQueueQueueSettingsGetObjectWaitMessageWaitMode',
           'CallQueueQueueSettingsObject', 'CallQueueQueueSettingsObjectComfortMessage',
           'CallQueueQueueSettingsObjectComfortMessageBypass', 'CallQueueQueueSettingsObjectMohMessage',
           'CallQueueQueueSettingsObjectMohMessageNormalSource', 'CallQueueQueueSettingsObjectOverflow',
           'CallQueueQueueSettingsObjectWelcomeMessage', 'CallQueueQueueSettingsObjectWhisperMessage',
           'CallQueueSettingsGet', 'CreateCallQueueObjectCallingLineIdPolicy', 'CreateForwardingRuleObjectCallsFrom',
           'CreateForwardingRuleObjectCallsFromCustomNumbers', 'CreateForwardingRuleObjectCallsFromSelection',
           'CreateForwardingRuleObjectCallsTo', 'CreateForwardingRuleObjectForwardTo',
           'CreateForwardingRuleObjectForwardToSelection', 'DirectLineCallerIdNameObject', 'DnisAnnouncementsGet',
           'DnisAnnouncementsGetComfortMessage', 'DnisAnnouncementsGetComfortMessageBypass',
           'DnisAnnouncementsGetMohMessage', 'DnisAnnouncementsGetWelcomeMessage',
           'DnisAnnouncementsGetWhisperMessage', 'DnisAnnouncementsModifyComfortMessage',
           'DnisAnnouncementsModifyComfortMessageBypass', 'DnisAnnouncementsModifyMohMessage',
           'DnisAnnouncementsModifyWelcomeMessage', 'DnisAnnouncementsModifyWhisperMessage', 'DnisObject',
           'DnisSettings', 'FeaturesCallQueueApi', 'GetAnnouncementFileInfo', 'GetCallQueueAgentObject',
           'GetCallQueueAgentObjectAgent', 'GetCallQueueAgentObjectQueuesItem', 'GetCallQueueCallPolicyObject',
           'GetCallQueueCallPolicyObjectCallBounce', 'GetCallQueueCallPolicyObjectDistinctiveRing',
           'GetCallQueueEssentialsCallPolicyObject', 'GetCallQueueEssentialsObject',
           'GetCallQueueForcedForwardObject', 'GetCallQueueHolidayObject', 'GetCallQueueHolidayObjectAction',
           'GetCallQueueNightServiceObject', 'GetCallQueueNightServiceObjectAnnouncementMode',
           'GetCallQueueObjectAlternateNumberSettings', 'GetCallQueueStrandedCallsObject',
           'GetCallQueueStrandedCallsObjectAction', 'GetCallQueueSupervisorResponse', 'GetForwardingRuleObject',
           'GetPersonPlaceObject', 'GetPersonPlaceVirtualLineCallQueueObjectType', 'GetUserNumberItemObject',
           'HuntPolicySelection', 'HuntRoutingTypeSelection', 'ListCallQueueAgentObject',
           'ListCallQueueEssentialsObject', 'ListSupervisorAgentObject', 'ListSupervisorObject', 'LocationObject',
           'MediaType', 'ModesGet', 'ModesGetForwardTo', 'ModesGetForwardToDefaultForwardToSelection', 'ModesGetType',
           'ModesPatch', 'ModesPatchForwardTo', 'ModifyAgentsForCallQueueObjectSettingsItem',
           'ModifyCallForwardingObjectCallForwarding', 'ModifyCallForwardingObjectCallForwardingOperatingModes',
           'ModifyPersonPlaceVirtualLineCallQueueObject', 'MohMessageSource', 'MohMessageSourceGreeting',
           'MohMessageSourceModify', 'NumberOwnerType', 'PostPersonPlaceVirtualLineCallQueueObject',
           'PostPersonPlaceVirtualLineSupervisorObject', 'PutPersonPlaceVirtualLineAgentObject', 'RingPatternObject',
           'STATE', 'SelectionObject', 'TelephonyType']


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


class AnnouncementAudioFileLevel(str, Enum):
    location = 'LOCATION'
    organization = 'ORGANIZATION'
    entity = 'ENTITY'


class AnnouncementAudioFile(ApiModel):
    #: Unique identifier of the Announcement file.
    id: Optional[str] = None
    #: Name of the announcement file. `name`, `mediaFileType`, `level` are mandatory if `id` is not provided for
    #: uploading an announcement.
    name: Optional[str] = None
    #: Media file type of announcement file.
    media_file_type: Optional[str] = None
    #: The level at which this announcement exists.
    level: Optional[AnnouncementAudioFileLevel] = None


class AudioAnnouncementFileFeatureGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    d3_gp = '3GP'


class AudioAnnouncementFileFeatureGetObject(ApiModel):
    #: A unique identifier for the announcement.
    id: Optional[str] = None
    #: Audio announcement file name.
    file_name: Optional[str] = None
    #: Audio announcement file type.
    media_file_type: Optional[AudioAnnouncementFileFeatureGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    level: Optional[AnnouncementAudioFileLevel] = None
    #: Indicates whether the announcement is a text-to-speech file.
    is_text_to_speech: Optional[bool] = None


class AudioAnnouncementFileFeatureObject(ApiModel):
    #: A unique identifier for the announcement. `name`, `mediaFileType`, `level` are mandatory if `id` is not provided
    #: for uploading an announcement.
    id: Optional[str] = None
    #: Audio announcement file name.
    file_name: Optional[str] = None
    #: Audio announcement file type.
    media_file_type: Optional[AudioAnnouncementFileFeatureGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    level: Optional[AnnouncementAudioFileLevel] = None


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


class CallQueueHolidaySchedulesObjectScheduleLevel(str, Enum):
    #: Schedule is configured across a location.
    location = 'LOCATION'
    #: Schedule is configured across an organization.
    organization = 'ORGANIZATION'


class CreateForwardingRuleObjectForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination for the call queue.
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
    #: Destination voicemail is enabled.
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
    level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None
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


class CallQueueHolidaySchedulesObject(ApiModel):
    #: Name of the schedule configured for a holiday service.
    schedule_name: Optional[str] = None
    #: Indicates whether the schedule in scheduleName is specific to the organization or location.
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


class CallQueueQueueSettingsGetObjectWaitMessageWaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class CallQueueQueueSettingsGetObjectWaitMessage(ApiModel):
    #: If enabled play Wait Message.
    enabled: Optional[bool] = None
    #: Estimated wait message operating mode. Supported values `TIME` and `POSITION`.
    wait_mode: Optional[CallQueueQueueSettingsGetObjectWaitMessageWaitMode] = None
    #: The number of minutes for which the estimated wait is played. The minimum time is 10 minutes. The maximum time
    #: is 100 minutes.
    handling_time: Optional[int] = None
    #: The default number of call handling minutes. The minimum time is 1 minutes, The maximum time is 100 minutes.
    default_handling_time: Optional[int] = None
    #: The number of the position for which the estimated wait is played. The minimum positions are 10, The maximum
    #: positions are 100.
    queue_position: Optional[int] = None
    #: Play time / Play position High Volume.
    high_volume_message_enabled: Optional[bool] = None
    #: The number of estimated waiting times in seconds. The minimum time is 10 seconds. The maximum time is 600
    #: seconds.
    estimated_waiting_time: Optional[int] = None
    #: Callback options enabled/disabled. Default value is false.
    callback_option_enabled: Optional[bool] = None
    #: The minimum estimated callback times in minutes. The default value is 30.
    minimum_estimated_callback_time: Optional[int] = None
    #: The international numbers for callback is enabled/disabled. The default value is `false`.
    international_callback_enabled: Optional[bool] = None
    #: Play updated estimated wait message.
    play_updated_estimated_wait_message: Optional[bool] = None


class CallQueueQueueSettingsObjectOverflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[CallQueueQueueSettingsGetObjectOverflowAction] = None
    #: When `true`, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external `transferNumber` is entered.
    send_to_voicemail: Optional[bool] = None
    #: Destination number for overflow calls when `action` is set to `TRANSFER_TO_PHONE_NUMBER`.
    transfer_number: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    overflow_after_wait_enabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. The minimum
    #: value 0, The maximum value is 7200 seconds.
    overflow_after_wait_time: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by
    #: a user.
    play_overflow_greeting_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `overflow` greetings. These files are from the list of announcement
    #: files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is mandatory, and the
    #: maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueQueueSettingsObjectWelcomeMessage(ApiModel):
    #: If enabled play entrance message. The default value is `true`.
    enabled: Optional[bool] = None
    #: Mandatory entrance message. The default value is `false`.
    always_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `welcomeMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueQueueSettingsObjectComfortMessage(ApiModel):
    #: If enabled play periodic comfort message.
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    time_between_messages: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueQueueSettingsObjectComfortMessageBypass(ApiModel):
    #: If enabled play comfort bypass message.
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The
    #: minimum time is 1 seconds. The maximum time is 120 seconds.
    call_waiting_age_threshold: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessageBypass` greetings. These files are from the list of
    #: announcements files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueQueueSettingsObjectMohMessageNormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `mohMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None
    #: Identifier of the playlist used for this MOH source.
    audio_playlist_id: Optional[str] = None


class CallQueueQueueSettingsObjectMohMessage(ApiModel):
    normal_source: Optional[CallQueueQueueSettingsObjectMohMessageNormalSource] = None
    alternate_source: Optional[CallQueueQueueSettingsObjectMohMessageNormalSource] = None


class CallQueueQueueSettingsObjectWhisperMessage(ApiModel):
    #: If enabled play the Whisper Message.
    enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `whisperMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the `overflow` settings are
    #: triggered.
    queue_size: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsObjectOverflow] = None
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call
    #: queue while there is an available agent, the caller will not hear this announcement and is transferred to an
    #: agent. The welcome message feature is enabled by default.
    welcome_message: Optional[CallQueueQueueSettingsObjectWelcomeMessage] = None
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[CallQueueQueueSettingsGetObjectWaitMessage] = None
    #: Play a message after the welcome message and before hold music. This is typically a `CUSTOM` announcement that
    #: plays information, such as current promotions or information about products and services.
    comfort_message: Optional[CallQueueQueueSettingsObjectComfortMessage] = None
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that
    #: should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort
    #: message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[CallQueueQueueSettingsObjectComfortMessageBypass] = None
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[CallQueueQueueSettingsObjectMohMessage] = None
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces
    #: the identity of the call queue from which the call is coming.
    whisper_message: Optional[CallQueueQueueSettingsObjectWhisperMessage] = None
    #: When `true`, the call queue uses the organization-level play tone settings and ignores the queue-level
    #: `playToneToAgent*` values. When `false`, the queue-level `playToneToAgent*` values are used.
    use_enterprise_play_tone_to_agent_settings_enabled: Optional[bool] = None
    #: Queue-specific setting that plays a tone to agents when a supervisor joins an active call using barge in.
    #: Applies only when `useEnterprisePlayToneToAgentSettingsEnabled` is `false`.
    play_tone_to_agent_for_barge_in_enabled: Optional[bool] = None
    #: Queue-specific setting that plays a tone to agents when a supervisor monitors their active call without joining.
    #: Applies only when `useEnterprisePlayToneToAgentSettingsEnabled` is `false`.
    play_tone_to_agent_for_silent_monitoring_enabled: Optional[bool] = None
    #: Queue-specific setting that plays a tone to agents when a supervisor coaches an agent during an active call.
    #: Applies only when `useEnterprisePlayToneToAgentSettingsEnabled` is `false`.
    play_tone_to_agent_for_supervisor_coaching_enabled: Optional[bool] = None


class CallQueueSettingsGet(ApiModel):
    #: Indicates whether callers keep their queue position when simultaneous ringing routes a call to multiple agents.
    maintain_queue_position_for_sim_ring_enabled: Optional[bool] = None
    #: Indicates whether Customer Assist agents are changed to unavailable after bounced calls.
    force_agent_unavailable_on_bounced_enabled: Optional[bool] = None
    #: Organization-wide default that plays a tone to agents when a supervisor joins an active call using barge in.
    play_tone_to_agent_for_barge_in_enabled: Optional[bool] = None
    #: Organization-wide default that plays a tone to agents when a supervisor monitors their active call without
    #: joining.
    play_tone_to_agent_for_silent_monitoring_enabled: Optional[bool] = None
    #: Organization-wide default that plays a tone to agents when a supervisor coaches an agent during an active call.
    play_tone_to_agent_for_supervisor_coaching_enabled: Optional[bool] = None


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
    call_bounce_enabled: Optional[bool] = None
    #: Number of rings after which to bounce call, if call bounce is enabled.
    call_bounce_max_rings: Optional[int] = None
    #: Bounce if agent becomes unavailable.
    agent_unavailable_enabled: Optional[bool] = None
    #: Alert agent if call on hold more than `alertAgentMaxSeconds`.
    alert_agent_enabled: Optional[bool] = None
    #: Number of second after which to alert agent if `alertAgentEnabled`.
    alert_agent_max_seconds: Optional[int] = None
    #: Bounce if call on hold more than `callBounceMaxSeconds`.
    call_bounce_on_hold_enabled: Optional[bool] = None
    #: Number of second after which to bounce if `callBounceEnabled`.
    call_bounce_on_hold_max_seconds: Optional[int] = None


class GetCallQueueCallPolicyObjectDistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    enabled: Optional[bool] = None
    #: Ring pattern for when this call queue is called. Only available when `distinctiveRing` is enabled for the call
    #: queue.
    ring_pattern: Optional[RingPatternObject] = None


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents.
    routing_type: Optional[HuntRoutingTypeSelection] = None
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class PostPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is `SKILL_BASED`.
    skill_level: Optional[int] = None


class CreateForwardingRuleObjectForwardTo(ApiModel):
    #: Controls what happens when the rule matches.
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: Phone number to forward calls to. Required when selection is `FORWARD_TO_SPECIFIED_NUMBER`.
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
    id: Optional[str] = None
    #: Name of greeting file.
    file_name: Optional[str] = None
    #: Size of greeting file in kilo-bytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement.
    media_file_type: Optional[MediaType] = None
    #: Level where the announcement is created.
    level: Optional[AnnouncementAudioFileLevel] = None
    #: Indicates whether the announcement is a text-to-speech file.
    is_text_to_speech: Optional[bool] = None


class GetCallQueueForcedForwardObject(ApiModel):
    #: Whether or not the call queue forced forward routing policy setting is enabled.
    forced_forward_enabled: Optional[bool] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    transfer_phone_number: Optional[str] = None
    #: Indicates whether an announcement plays to callers before the action is applied.
    play_announcement_before_enabled: Optional[bool] = None
    #: The type of announcement to be played.
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
    holiday_service_enabled: Optional[bool] = None
    #: The call processing action type.
    action: Optional[GetCallQueueHolidayObjectAction] = None
    #: The schedule mentioned in `holidayScheduleName` is org or location specific. (Must be from `holidaySchedules`
    #: list)
    holiday_schedule_level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None
    #: Name of the schedule configured for a holiday service as one of from `holidaySchedules` list.
    holiday_schedule_name: Optional[str] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    transfer_phone_number: Optional[str] = None
    #: Indicates whether an announcement plays to callers before the action is applied.
    play_announcement_before_enabled: Optional[bool] = None
    #: The type of announcement to be played.
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
    night_service_enabled: Optional[bool] = None
    #: The call processing action type.
    action: Optional[GetCallQueueHolidayObjectAction] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    transfer_phone_number: Optional[str] = None
    #: Indicates whether an announcement plays to callers before the action is applied.
    play_announcement_before_enabled: Optional[bool] = None
    #: The type of announcements to played.
    announcement_mode: Optional[GetCallQueueNightServiceObjectAnnouncementMode] = None
    #: The type of announcements to be played when announcementMode is set to `NORMAL`.
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None
    #: Name of the schedule configured for a night service as one of from `businessHourSchedules` list.
    business_hours_name: Optional[str] = None
    #: The above mentioned schedule is org or location specific. (Must be from `businessHourSchedules` list).
    business_hours_level: Optional[CallQueueHolidaySchedulesObjectScheduleLevel] = None
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: Optional[list[CallQueueHolidaySchedulesObject]] = None
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool] = None
    #: The type of announcements to be played when announcementMode is set to NORMAL.`MANUAL`.
    manual_audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List Of Audio Files.
    manual_audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for the Alternate Numbers.
    distinctive_ring_enabled: Optional[bool] = None
    #: Allows up to 10 numbers, each with an optional distinctive ring setting override.
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
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None


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
    #: The call processing action type.
    action: Optional[GetCallQueueStrandedCallsObjectAction] = None
    #: Call gets transferred to this number when action is set to `TRANSFER`. This can also be an extension.
    transfer_phone_number: Optional[str] = None
    #: The type of announcement to be played.
    audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
    audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None


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


class ModesPatchForwardTo(ApiModel):
    #: The selection for forwarding.
    selection: Optional[CreateForwardingRuleObjectForwardToSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    destination: Optional[str] = None
    #: Destination voicemail is enabled.
    destination_voicemail_enabled: Optional[bool] = None


class ModesPatch(ApiModel):
    #: Normal operation is enabled or disabled.
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    id: Optional[str] = None
    #: Forward to settings.
    forward_to: Optional[ModesPatchForwardTo] = None


class ModifyCallForwardingObjectCallForwardingOperatingModes(ApiModel):
    #: Indicates whether operating modes forwarding is enabled.
    enabled: Optional[bool] = None
    #: List of operating mode configurations.
    modes: Optional[list[ModesPatch]] = None


class ModifyCallForwardingObjectCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesSet]] = None
    #: Configuration for forwarding via Operating modes (Schedule Based Routing).
    operating_modes: Optional[ModifyCallForwardingObjectCallForwardingOperatingModes] = None


class ModifyPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is `SKILL_BASED`.
    skill_level: Optional[int] = None
    #: Indicates the join status of the agent for this queue. The default value for newly added agents is `true`.
    join_enabled: Optional[bool] = None


class SelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this call queue.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `name` is to be shown for this call queue.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `DISPLAY_NAME`.
    selection: Optional[SelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


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


class CallQueueCallForwardAvailableNumberObjectOwner(ApiModel):
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


class CallQueueCallForwardAvailableNumberObject(ApiModel):
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
    owner: Optional[CallQueueCallForwardAvailableNumberObjectOwner] = None


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person, workspace or virtual line.
    external: Optional[str] = None
    #: Extension of a person, workspace or virtual line.
    extension: Optional[str] = None


class AvailableAgentObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    id: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    last_name: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    first_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[GetPersonPlaceVirtualLineCallQueueObjectType] = None
    #: Email of a person, workspace or virtual line.
    email: Optional[str] = None
    #: Person has the CX Essentials license.
    has_cx_essentials: Optional[bool] = None
    #: List of phone numbers of a person, workspace or virtual line.
    phone_numbers: Optional[list[GetUserNumberItemObject]] = None


class ListSupervisorObject(ApiModel):
    #: A unique identifier for the supervisor.
    id: Optional[str] = None
    #: First name of the supervisor.
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    last_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    esn: Optional[str] = None
    #: Number of agents managed by supervisor. A supervisor must manage at least one agent.
    agent_count: Optional[int] = None


class PostPersonPlaceVirtualLineSupervisorObject(ApiModel):
    #: Identifier of the person, workspace or virtual line.
    id: Optional[str] = None


class AvailableSupervisorsListObject(ApiModel):
    #: A unique identifier for the supervisor.
    id: Optional[str] = None
    #: First name of the supervisor.
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the supervisor.
    display_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    esn: Optional[str] = None


class ListSupervisorAgentObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str] = None
    #: Last name of the agent.
    last_name: Optional[str] = None
    #: First name of the agent.
    first_name: Optional[str] = None
    #: Primary phone extension of the agent.
    extension: Optional[str] = None
    #: Routing prefix + extension of a agent.
    esn: Optional[str] = None
    #: Primary phone number of the agent.
    phone_number: Optional[str] = None


class AgentAction(str, Enum):
    #: Assign an agent to a supervisor.
    add = 'ADD'
    #: Remove an agent from a supervisor.
    delete = 'DELETE'


class PutPersonPlaceVirtualLineAgentObject(ApiModel):
    #: ID of person, workspace or virtual line. **WARNING**: The `id` returned is always of type `PEOPLE` even if the
    #: agent is a workspace or virtual line. The `type` of the agent `id` will be corrected in a future release.
    id: Optional[str] = None
    #: Enumeration that indicates whether an agent needs to be added (`ADD`) or deleted (`DELETE`) from a supervisor.
    action: Optional[AgentAction] = None


class AvailableAgentListObject(ApiModel):
    #: A unique identifier for the agent.
    id: Optional[str] = None
    #: First name of the agent.
    first_name: Optional[str] = None
    #: Last name of the agent.
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the agent.
    display_name: Optional[str] = None
    #: Primary phone number of the agent.
    phone_number: Optional[str] = None
    #: Primary phone extension of the agent.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    esn: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[GetPersonPlaceVirtualLineCallQueueObjectType] = None


class ListCallQueueAgentObject(ApiModel):
    #: Unique call queue agent identifier.
    id: Optional[str] = None
    #: First name for the call queue agent.
    first_name: Optional[str] = None
    #: Last name for the call queue agent.
    last_name: Optional[str] = None
    #: Primary phone number of the call queue agent.
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue agent.
    extension: Optional[str] = None
    #: Routing prefix of the call queue agent.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a agent.
    esn: Optional[str] = None
    #: Denotes the queue count for call queue agent.
    queue_count: Optional[int] = None
    #: Denotes the location count for call queue agent.
    location_count: Optional[int] = None
    #: Denotes the join count for call queue agent.
    join_count: Optional[int] = None
    #: Denotes unjoin count for call queue agent.
    unjoin_count: Optional[int] = None
    #: The location information.
    location: Optional[LocationObject] = None
    #: The type of the call queue agent.
    type: Optional[str] = None


class GetCallQueueAgentObjectAgent(ApiModel):
    #: A unique identifier for the call queue agent.
    id: Optional[str] = None
    #: First name for the call queue agent.
    first_name: Optional[str] = None
    #: last name for the call queue agent.
    last_name: Optional[str] = None
    #: Primary phone number of the call queue agent.
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue agent.
    extension: Optional[str] = None
    #: Routing prefix + extension of a agent.
    esn: Optional[str] = None
    #: The location information.
    location: Optional[LocationObject] = None
    #: TIMEhe type of the call queue agent.
    type: Optional[str] = None


class GetCallQueueAgentObjectQueuesItem(ApiModel):
    #: Unique identifier of the call queue.
    id: Optional[str] = None
    #: Unique name for the call queue.
    name: Optional[str] = None
    #: Primary phone number of the call queue.
    phone_number: Optional[str] = None
    #: The routing prefix for the call queue.
    routing_prefix: Optional[str] = None
    #: The location identifier of the call queue.
    location_id: Optional[str] = None
    #: The location name where the call queue resides.
    location_name: Optional[str] = None
    #: Whether or not the call queue is enabled.
    join_enabled: Optional[bool] = None


class GetCallQueueAgentObject(ApiModel):
    agent: Optional[GetCallQueueAgentObjectAgent] = None
    queues: Optional[list[GetCallQueueAgentObjectQueuesItem]] = None


class ModifyAgentsForCallQueueObjectSettingsItem(ApiModel):
    #: Unique call queue identifier.
    queue_id: Optional[str] = None
    #: Whether or not the call queue is enabled.
    join_enabled: Optional[bool] = None


class ListCallQueueEssentialsObject(ApiModel):
    #: A unique identifier for the call queue.
    id: Optional[str] = None
    #: Unique name for the call queue.
    name: Optional[str] = None
    #: Denotes if the call queue has Customer Assist license.
    has_cx_essentials: Optional[bool] = None
    #: Name of location for call queue.
    location_name: Optional[str] = None
    #: ID of location for call queue.
    location_id: Optional[str] = None
    #: Primary phone number of the call queue.
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue.
    extension: Optional[str] = None
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool] = None
    #: The department information.
    department: Optional[LocationObject] = None


class GetCallQueueEssentialsCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class CallQueueQueueEssentialsSettingsObjectOverflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[CallQueueQueueSettingsGetObjectOverflowAction] = None
    #: When `true`, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external `transferNumber` is entered.
    send_to_voicemail: Optional[bool] = None
    #: Destination number for overflow calls when `action` is set to `TRANSFER_TO_PHONE_NUMBER`.
    transfer_number: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    overflow_after_wait_enabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    overflow_after_wait_time: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise callers will hear the hold music until the call is answered by a
    #: user.
    play_overflow_greeting_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: Array of announcement file name strings to be played as overflow greetings. These files are from the list of
    #: announcements files associated with this call queue.
    audio_files: Optional[list[str]] = None


class CallQueueQueueEssentialsSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are
    #: triggered.
    queue_size: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueEssentialsSettingsObjectOverflow] = None


class GetPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    id: Optional[str] = None
    #: First name of person or workspace.
    first_name: Optional[str] = None
    #: First name of person or workspace.
    last_name: Optional[str] = None
    #: Phone number of person or workspace.
    phone_number: Optional[str] = None
    #: Extension of person or workspace.
    extension: Optional[str] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    weight: Optional[str] = None


class GetCallQueueEssentialsObject(ApiModel):
    #: A unique identifier for the call queue.
    id: Optional[str] = None
    #: Unique name for the call queue.
    name: Optional[str] = None
    #: Denotes if the call queue has Customer Assist license.
    has_cx_essentials: Optional[bool] = None
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool] = None
    #: Language for call queue.
    language: Optional[str] = None
    #: Language code for call queue.
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str] = None
    #: Time zone for the call queue.
    time_zone: Optional[str] = None
    #: Primary phone number of the call queue.
    phone_number: Optional[str] = None
    #: Extension of the call queue.
    extension: Optional[str] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[GetCallQueueEssentialsCallPolicyObject] = None
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueEssentialsSettingsObject] = None
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool] = None
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceObject]] = None
    #: The department information.
    department: Optional[LocationObject] = None
    #: Settings for the direct line caller ID name to be shown for this call queue.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The name to be used for dial by name functions.
    dial_by_name: Optional[str] = None


class AvailablePhoneNumber(ApiModel):
    #: The phone number.
    phone_number: Optional[str] = None
    #: Defines whether the number is active or not.
    state: Optional[STATE] = None
    #: Flag to indicate if the number is used as location main number.
    is_main_number: Optional[bool] = None
    #: Define type of number. Currently API supports only PSTN_NUMBER.
    telephony_type: Optional[str] = None
    #: Flag to indicate if the number is toll free.
    toll_free_number: Optional[bool] = None
    #: Flag to indicate if the number is a Service Number.
    is_service_number: Optional[bool] = None


class DnisObject(ApiModel):
    #: Unique identifier for the DNIS.
    id: Optional[str] = None
    #: Name of the DNIS.
    name: Optional[str] = None
    #: Phone number of the DNIS.
    phone_number: Optional[str] = None
    #: Extension of the DNIS.
    extension: Optional[str] = None
    #: Routing prefix (location dialing code) of the DNIS.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Number (ESN) of the DNIS.
    esn: Optional[str] = None
    #: Ring pattern of the DNIS.
    ring_pattern: Optional[RingPatternObject] = None
    #: Use custom announcement settings for the DNIS. Enable custom announcement settings using Modify DNIS API. Modify
    #: custom announcement settings using Modify DNIS announcements API.
    custom_dnis_announcement_settings_enabled: Optional[bool] = None


class DnisSettings(ApiModel):
    #: Whether distinctive ringing is enabled for the queue.
    distinctive_ringing_enabled: Optional[bool] = None
    #: Whether the DNIS name and number is displayed to agents.
    display_dnis_name_and_number_enabled: Optional[bool] = None


class AudioAnnouncementFileMediaFileType(str, Enum):
    wav = 'WAV'


class AudioAnnouncementFile(ApiModel):
    #: Announcement file ID.
    id: Optional[str] = None
    #: Name of the announcement file.
    file_name: Optional[str] = None
    #: Media file type of the announcement.
    media_file_type: Optional[AudioAnnouncementFileMediaFileType] = None
    #: Level at which the announcement is defined.
    level: Optional[AnnouncementAudioFileLevel] = None
    #: Whether the file is a text-to-speech file.
    is_text_to_speech: Optional[bool] = None


class MohMessageSourceGreeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'
    playlist = 'PLAYLIST'


class MohMessageSource(ApiModel):
    #: Whether the source is enabled.
    enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[MohMessageSourceGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFile]] = None
    #: Audio playlist ID.
    audio_playlist_id: Optional[str] = None
    #: Audio playlist name.
    audio_playlist_name: Optional[str] = None


class AudioAnnouncementFileModify(ApiModel):
    #: Announcement file ID.
    id: Optional[str] = None
    #: Name of the announcement file.
    file_name: Optional[str] = None
    #: Media file type of the announcement.
    media_file_type: Optional[AudioAnnouncementFileMediaFileType] = None
    #: Level at which the announcement is defined.
    level: Optional[AnnouncementAudioFileLevel] = None


class MohMessageSourceModify(ApiModel):
    #: Whether the source is enabled.
    enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFileModify]] = None
    #: Audio playlist ID.
    audio_playlist_id: Optional[str] = None


class DnisAnnouncementsGetWelcomeMessage(ApiModel):
    #: Whether the welcome message is enabled.
    enabled: Optional[bool] = None
    #: Whether to always play the welcome message.
    always_enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFile]] = None


class DnisAnnouncementsGetComfortMessage(ApiModel):
    #: Whether the comfort message is enabled.
    enabled: Optional[bool] = None
    #: Time between comfort messages in seconds.
    time_between_messages: Optional[int] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFile]] = None


class DnisAnnouncementsGetComfortMessageBypass(ApiModel):
    #: Whether the comfort message bypass is enabled.
    enabled: Optional[bool] = None
    #: Call waiting age threshold in seconds.
    call_waiting_age_threshold: Optional[int] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFile]] = None


class DnisAnnouncementsGetMohMessage(ApiModel):
    normal_source: Optional[MohMessageSource] = None
    alternate_source: Optional[MohMessageSource] = None


class DnisAnnouncementsGetWhisperMessage(ApiModel):
    #: Whether the whisper message is enabled.
    enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFile]] = None


class DnisAnnouncementsGet(ApiModel):
    #: Whether custom DNIS announcement settings are enabled for this DNIS.
    custom_dnis_announcement_settings_enabled: Optional[bool] = None
    #: Welcome message settings.
    welcome_message: Optional[DnisAnnouncementsGetWelcomeMessage] = None
    #: Comfort message settings.
    comfort_message: Optional[DnisAnnouncementsGetComfortMessage] = None
    #: Comfort message bypass settings.
    comfort_message_bypass: Optional[DnisAnnouncementsGetComfortMessageBypass] = None
    #: Music on hold message settings.
    moh_message: Optional[DnisAnnouncementsGetMohMessage] = None
    #: Wait message settings.
    wait_message: Optional[CallQueueQueueSettingsGetObjectWaitMessage] = None
    #: Whisper message settings.
    whisper_message: Optional[DnisAnnouncementsGetWhisperMessage] = None


class DnisAnnouncementsModifyWelcomeMessage(ApiModel):
    #: Whether the welcome message is enabled.
    enabled: Optional[bool] = None
    #: Whether to always play the welcome message.
    always_enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFileModify]] = None


class DnisAnnouncementsModifyComfortMessage(ApiModel):
    #: Whether the comfort message is enabled.
    enabled: Optional[bool] = None
    #: Time between comfort messages in seconds.
    time_between_messages: Optional[int] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFileModify]] = None


class DnisAnnouncementsModifyComfortMessageBypass(ApiModel):
    #: Whether the comfort message bypass is enabled.
    enabled: Optional[bool] = None
    #: Minimum call waiting age in seconds before bypass plays.
    call_waiting_age_threshold: Optional[int] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFileModify]] = None


class DnisAnnouncementsModifyMohMessage(ApiModel):
    normal_source: Optional[MohMessageSourceModify] = None
    alternate_source: Optional[MohMessageSourceModify] = None


class DnisAnnouncementsModifyWhisperMessage(ApiModel):
    #: Whether the whisper message is enabled.
    enabled: Optional[bool] = None
    #: The greeting type.
    greeting: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
    #: List of audio announcement files.
    audio_announcement_files: Optional[list[AudioAnnouncementFileModify]] = None


class GetCallQueueSupervisorResponse(ApiModel):
    #: unique identifier of the supervisor
    id: Optional[str] = None
    #: Array of agents assigned to a specific supervisor.
    agents: Optional[list[ListSupervisorAgentObject]] = None


class FeaturesCallQueueApi(ApiChild, base='telephony/config'):
    """
    Features: Call Queue
    
    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.
    
    Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in another organization using the optional `orgId` query
    parameter.
    
    DNIS (Dialed Number Identification Service) allows call queues to distinguish between primary and alternate numbers
    when delivering calls to agents. Each DNIS entry can have its own name, phone number, extension, ring pattern, and
    custom announcement settings.
    
    The maximum number of DNIS entries per call queue is 100.
    """

    def create_call_queue(self, location_id: str, name: str, call_policies: GetCallQueueCallPolicyObject,
                          queue_settings: CallQueueQueueSettingsObject,
                          agents: list[PostPersonPlaceVirtualLineCallQueueObject], has_cx_essentials: bool = None,
                          phone_number: str = None, extension: str = None, language_code: str = None,
                          first_name: str = None, last_name: str = None, time_zone: str = None,
                          calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy = None,
                          calling_line_id_phone_number: str = None, allow_agent_join_enabled: bool = None,
                          phone_number_for_outgoing_calls_enabled: bool = None,
                          direct_line_caller_id_name: DirectLineCallerIdNameObject = None, dial_by_name: str = None,
                          org_id: str = None) -> str:
        """
        Create a Call Queue with Customer Assist

        Create new Call Queues for the given location.

        Call queues temporarily hold calls in the cloud, when all agents assigned to receive calls from the queue are
        unavailable.
        Queued calls are routed to an available agent, when not on an active call. Each call queue is assigned a lead
        number, which is a telephone
        number that external callers can dial to reach the users assigned to the call queue. Call queues are also
        assigned an internal extension,
        which can be dialed internally to reach the users assigned to the call queue.

        Creating a call queue requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue needs to be created.
        :type location_id: str
        :param name: Unique name for the call queue.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to `agents`.
        :type call_policies: GetCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineCallQueueObject]
        :param has_cx_essentials: Creates a Customer Assist call queue, when `true`. This requires Customer Assist
            licensed agents.
        :type has_cx_essentials: bool
        :param phone_number: Primary phone number of the call queue. Either a `phoneNumber` or `extension` is
            mandatory.
        :type phone_number: str
        :param extension: Primary phone extension of the call queue. Either a `phoneNumber` or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
            This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to
            `phoneNumber` if set, otherwise defaults to call group name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param time_zone: Time zone for the call queue.
        :type time_zone: str
        :param calling_line_id_policy: Which type of Calling Line ID Policy Selected for Call Queue.
        :type calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy
        :param calling_line_id_phone_number: Calling line ID Phone number which will be shown if CUSTOM is selected.
        :type calling_line_id_phone_number: str
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When `true`, indicates that the agent's configuration allows
            them to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this call queue.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: The name to be used for dial by name functions. Characters of `%`,  `+`, `\\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_name: str
        :param org_id: The organization ID where the call queue needs to be created.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body: dict[str, Any] = dict()
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
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/queues')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_call_queue_alternate_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params: Any) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
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

    def get_call_queue_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params: Any) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
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

    def get_call_queue_call_forward_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                            owner_name: str = None, extension: str = None,
                                                            org_id: str = None,
                                                            **params: Any) -> Generator[CallQueueCallForwardAvailableNumberObject, None, None]:
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

    def get_available_phone_numbers_for_dnis(self, location_id: str, phone_number: str = None, org_id: str = None,
                                             **params: Any) -> Generator[AvailablePhoneNumber, None, None]:
        """
        Get Available Phone Numbers for DNIS

        Get the list of available phone numbers that can be assigned to a DNIS for call queues at a location.

        Retrieving available numbers requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID.
        :type location_id: str
        :param phone_number: Filter by phone number.
        :type phone_number: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :return: Generator yielding :class:`AvailablePhoneNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep(f'locations/{location_id}/queues/dnis/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailablePhoneNumber, item_key='phoneNumbers', params=params)

    def delete_call_queue(self, location_id: str, queue_id: str, org_id: str = None) -> None:
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().delete(url, params=params)

    def get_call_queue_with_customer_assist(self, location_id: str, queue_id: str, has_cx_essentials: bool = None,
                                            org_id: str = None) -> GetCallQueueEssentialsObject:
        """
        Get Details for a Call Queue with Customer Assist

        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud, when all agents assigned to receive calls from the queue are
        unavailable.
        Queued calls are routed to an available agent, when not on an active call. Each call queue is assigned a lead
        number, which is a telephone
        number that external callers can dial to reach the users assigned to the call queue. Call queues are also
        assigned an internal extension,
        which can be dialed internally to reach the users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieves the details of a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieves the details of call queue with this identifier.
        :type queue_id: str
        :param has_cx_essentials: Must be set to `true`, to view the details of a call queue with Customer Assist
            license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Retrieves the details of a call queue in this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueEssentialsObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url, params=params)
        r = GetCallQueueEssentialsObject.model_validate(data)
        return r

    def update_call_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsObject,
                          enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None,
                          last_name: str = None, time_zone: str = None, phone_number: str = None,
                          extension: str = None,
                          alternate_number_settings: GetCallQueueObjectAlternateNumberSettings = None,
                          call_policies: GetCallQueueCallPolicyObject = None,
                          calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy = None,
                          calling_line_id_phone_number: str = None,
                          allow_call_waiting_for_agents_enabled: bool = None,
                          agents: list[ModifyPersonPlaceVirtualLineCallQueueObject] = None,
                          allow_agent_join_enabled: bool = None, phone_number_for_outgoing_calls_enabled: bool = None,
                          direct_line_caller_id_name: DirectLineCallerIdNameObject = None, dial_by_name: str = None,
                          org_id: str = None) -> None:
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
        :type queue_settings: CallQueueQueueSettingsObject
        :param enabled: Whether or not the call queue is enabled.
        :type enabled: bool
        :param name: Unique name for the call queue.
        :type name: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to `.`.
            This field has been deprecated. Please use `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the
            `phoneNumber` if set, otherwise defaults to call group name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
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
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this call queue.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: Sets or clears the name to be used for dial by name functions. To clear the `dialByName`,
            the attribute must be set to null or empty string. Characters of `%`,  `+`, `\\`, `"` and Unicode
            characters are not allowed.
        :type dial_by_name: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
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
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url, params=params, json=body)

    def list_call_queue_announcement_files(self, location_id: str, queue_id: str,
                                           org_id: str = None) -> builtins.list[GetAnnouncementFileInfo]:
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetAnnouncementFileInfo]).validate_python(data['announcements'])
        return r

    def delete_call_queue_announcement_file(self, location_id: str, queue_id: str, file_name: str,
                                            org_id: str = None) -> None:
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
        :param file_name: -
        :type file_name: str
        :param org_id: Delete call queue announcement from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements/{file_name}')
        super().delete(url, params=params)

    def get_call_queue_call_forwarding_settings(self, location_id: str, queue_id: str,
                                                org_id: str = None) -> CallForwardSettingsGetCallForwarding:
        """
        Get Call Forwarding Settings for a Call Queue

        Retrieve Call Forwarding settings for the specified Call Queue, including the list of call forwarding rules.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardSettingsGetCallForwarding.model_validate(data['callForwarding'])
        return r

    def update_call_queue_call_forwarding_settings(self, location_id: str, queue_id: str,
                                                   call_forwarding: ModifyCallForwardingObjectCallForwarding = None,
                                                   org_id: str = None) -> None:
        """
        Update Call Forwarding Settings for a Call Queue

        Update Call Forwarding settings for the designated Call Queue.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        super().put(url, params=params, json=body)

    def switch_call_queue_call_forwarding_mode(self, location_id: str, queue_id: str, org_id: str = None) -> None:
        """
        Switch Mode for Call Forwarding Settings for a Call Queue

        Switches the current operating mode of the `Call Queue` to the mode as per normal operations.

        Operating modes allow call forwarding to be configured based on predefined schedules, enabling different
        routing behaviors during business hours, after hours, or holidays.

        Switching operating mode for a `call queue` requires a full, or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: `Location` in which this `call queue` exists.
        :type location_id: str
        :param queue_id: Switch operating mode to normal operations for this `call queue`.
        :type queue_id: str
        :param org_id: Switch operating mode as per normal operations for the `call queue` from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/actions/switchMode/invoke')
        super().post(url, params=params)

    def create_call_queue_selective_call_forwarding_rule(self, location_id: str, queue_id: str, name: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
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

    def delete_call_queue_selective_call_forwarding_rule(self, location_id: str, queue_id: str, rule_id: str,
                                                         org_id: str = None) -> None:
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url, params=params)

    def get_call_queue_selective_call_forwarding_rule(self, location_id: str, queue_id: str, rule_id: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url, params=params)
        r = GetForwardingRuleObject.model_validate(data)
        return r

    def update_call_queue_selective_call_forwarding_rule(self, location_id: str, queue_id: str, rule_id: str,
                                                         name: str = None, enabled: bool = None,
                                                         holiday_schedule: str = None, business_schedule: str = None,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
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

    def bulk_delete_dnis_for_acall_queue(self, location_id: str, queue_id: str, items: list[str],
                                         org_id: str = None) -> None:
        """
        Bulk Delete DNIS for a Call Queue

        Bulk delete a list of DNIS (Dialed Number Identification Service) entries for a call queue.

        A maximum of 99 DNIS entries can be deleted in a single request.

        Deleting DNIS entries requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param items: Array of DNIS IDs to be deleted.
        :type items: list[str]
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['items'] = items
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        super().delete(url, params=params, json=body)

    def get_list_of_dnis_for_acall_queue(self, location_id: str, queue_id: str,
                                         org_id: str = None) -> builtins.list[DnisObject]:
        """
        Get List of DNIS for a Call Queue

        Get the list of DNIS (Dialed Number Identification Service) entries for a call queue.

        DNIS allows call queues to distinguish between primary and alternate numbers when delivering calls to agents.
        Each DNIS entry can have its own name, phone number, extension, ring pattern, and custom announcement
        settings.

        The maximum number of DNIS entries per call queue is 100.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: list[DnisObject]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DnisObject]).validate_python(data['dnisList'])
        return r

    def create_adnis_for_acall_queue(self, location_id: str, queue_id: str, name: str, ring_pattern: RingPatternObject,
                                     phone_number: str = None, extension: str = None, org_id: str = None) -> str:
        """
        Create a DNIS for a Call Queue

        Create a new DNIS (Dialed Number Identification Service) entry for a call queue.

        DNIS allows call queues to distinguish between primary and alternate numbers when delivering calls to agents.

        The maximum number of DNIS entries per call queue is 100. Either `phoneNumber` or `extension` is required.

        Creating a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param name: Name of the DNIS. Must be unique across the call queue.
        :type name: str
        :param ring_pattern: Ring pattern of the DNIS.
        :type ring_pattern: RingPatternObject
        :param phone_number: Phone number of the DNIS. Must be a valid phone number from the same location. Either
            phoneNumber or extension is required.
        :type phone_number: str
        :param extension: Extension of the DNIS. Either phoneNumber or extension is required.
        :type extension: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        body['ringPattern'] = enum_str(ring_pattern)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_dnis_settings_for_acall_queue(self, location_id: str, queue_id: str, org_id: str = None) -> DnisSettings:
        """
        Get DNIS Settings for a Call Queue

        Get DNIS (Dialed Number Identification Service) settings for a call queue.

        Retrieving DNIS settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`DnisSettings`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/settings')
        data = super().get(url, params=params)
        r = DnisSettings.model_validate(data)
        return r

    def modify_dnis_settings_for_acall_queue(self, location_id: str, queue_id: str,
                                             distinctive_ringing_enabled: bool = None,
                                             display_dnis_name_and_number_enabled: bool = None,
                                             org_id: str = None) -> None:
        """
        Modify DNIS Settings for a Call Queue

        Modify DNIS (Dialed Number Identification Service) settings for a call queue.

        Modifying DNIS settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param distinctive_ringing_enabled: Whether distinctive ringing is enabled for the queue.
        :type distinctive_ringing_enabled: bool
        :param display_dnis_name_and_number_enabled: Whether the DNIS name and number is displayed to agents.
        :type display_dnis_name_and_number_enabled: bool
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if distinctive_ringing_enabled is not None:
            body['distinctiveRingingEnabled'] = distinctive_ringing_enabled
        if display_dnis_name_and_number_enabled is not None:
            body['displayDnisNameAndNumberEnabled'] = display_dnis_name_and_number_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/settings')
        super().put(url, params=params, json=body)

    def delete_adnis_for_acall_queue(self, location_id: str, queue_id: str, dnis_id: str, org_id: str = None) -> None:
        """
        Delete a DNIS for a Call Queue

        Delete a DNIS (Dialed Number Identification Service) entry for a call queue.

        Deleting a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        super().delete(url, params=params)

    def get_adnis_for_acall_queue(self, location_id: str, queue_id: str, dnis_id: str,
                                  org_id: str = None) -> DnisObject:
        """
        Get a DNIS for a Call Queue

        Get details of a specific DNIS (Dialed Number Identification Service) entry for a call queue.

        Retrieving DNIS details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`DnisObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        data = super().get(url, params=params)
        r = DnisObject.model_validate(data)
        return r

    def modify_adnis_for_acall_queue(self, location_id: str, queue_id: str, dnis_id: str, name: str = None,
                                     phone_number: str = None, extension: str = None,
                                     ring_pattern: RingPatternObject = None,
                                     custom_dnis_announcement_settings_enabled: bool = None,
                                     org_id: str = None) -> None:
        """
        Modify a DNIS for a Call Queue

        Modify a DNIS (Dialed Number Identification Service) entry for a call queue.

        To remove a phone number or extension from the DNIS, set the field to `null`.

        Modifying a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param name: Name of the DNIS. Must be unique across the call queue.
        :type name: str
        :param phone_number: Phone number of the DNIS. Set to `null` to remove the phone number.
        :type phone_number: str
        :param extension: Extension of the DNIS. Set to `null` to remove the extension.
        :type extension: str
        :param ring_pattern: Ring pattern of the DNIS.
        :type ring_pattern: RingPatternObject
        :param custom_dnis_announcement_settings_enabled: Use custom announcement settings for the DNIS.
        :type custom_dnis_announcement_settings_enabled: bool
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if ring_pattern is not None:
            body['ringPattern'] = enum_str(ring_pattern)
        if custom_dnis_announcement_settings_enabled is not None:
            body['customDnisAnnouncementSettingsEnabled'] = custom_dnis_announcement_settings_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        super().put(url, params=params, json=body)

    def get_dnis_announcements_for_acall_queue(self, location_id: str, queue_id: str, dnis_id: str,
                                               org_id: str = None) -> DnisAnnouncementsGet:
        """
        Get DNIS Announcements for a Call Queue

        Get the announcement settings for a specific DNIS (Dialed Number Identification Service) entry in a call queue.

        This includes welcome message, comfort message, music on hold, wait message, and whisper message settings.

        Retrieving DNIS announcements requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`DnisAnnouncementsGet`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}/announcements')
        data = super().get(url, params=params)
        r = DnisAnnouncementsGet.model_validate(data)
        return r

    def modify_dnis_announcements_for_acall_queue(self, location_id: str, queue_id: str, dnis_id: str,
                                                  custom_dnis_announcement_settings_enabled: bool = None,
                                                  welcome_message: DnisAnnouncementsModifyWelcomeMessage = None,
                                                  comfort_message: DnisAnnouncementsModifyComfortMessage = None,
                                                  comfort_message_bypass: DnisAnnouncementsModifyComfortMessageBypass = None,
                                                  moh_message: DnisAnnouncementsModifyMohMessage = None,
                                                  wait_message: CallQueueQueueSettingsGetObjectWaitMessage = None,
                                                  whisper_message: DnisAnnouncementsModifyWhisperMessage = None,
                                                  org_id: str = None) -> None:
        """
        Modify DNIS Announcements for a Call Queue

        Modify the announcement settings for a specific DNIS (Dialed Number Identification Service) entry in a call
        queue.

        This includes welcome message, comfort message, music on hold, wait message, and whisper message settings.

        Modifying DNIS announcements requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param custom_dnis_announcement_settings_enabled: Whether custom DNIS announcement settings are enabled for
            this DNIS.
        :type custom_dnis_announcement_settings_enabled: bool
        :param welcome_message: Welcome message settings.
        :type welcome_message: DnisAnnouncementsModifyWelcomeMessage
        :param comfort_message: Comfort message settings.
        :type comfort_message: DnisAnnouncementsModifyComfortMessage
        :param comfort_message_bypass: Comfort message bypass settings.
        :type comfort_message_bypass: DnisAnnouncementsModifyComfortMessageBypass
        :param moh_message: Music on hold message settings.
        :type moh_message: DnisAnnouncementsModifyMohMessage
        :param wait_message: Wait message settings.
        :type wait_message: CallQueueQueueSettingsGetObjectWaitMessage
        :param whisper_message: Whisper message settings.
        :type whisper_message: DnisAnnouncementsModifyWhisperMessage
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if custom_dnis_announcement_settings_enabled is not None:
            body['customDnisAnnouncementSettingsEnabled'] = custom_dnis_announcement_settings_enabled
        if welcome_message is not None:
            body['welcomeMessage'] = welcome_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if comfort_message is not None:
            body['comfortMessage'] = comfort_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if comfort_message_bypass is not None:
            body['comfortMessageBypass'] = comfort_message_bypass.model_dump(mode='json', by_alias=True, exclude_none=True)
        if moh_message is not None:
            body['mohMessage'] = moh_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if wait_message is not None:
            body['waitMessage'] = wait_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if whisper_message is not None:
            body['whisperMessage'] = whisper_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}/announcements')
        super().put(url, params=params, json=body)

    def get_call_queue_forced_forward(self, location_id: str, queue_id: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        data = super().get(url, params=params)
        r = GetCallQueueForcedForwardObject.model_validate(data)
        return r

    def update_call_queue_forced_forward(self, location_id: str, queue_id: str, forced_forward_enabled: bool,
                                         play_announcement_before_enabled: bool,
                                         audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                         transfer_phone_number: str = None,
                                         audio_files: list[AudioAnnouncementFileFeatureObject] = None,
                                         org_id: str = None) -> None:
        """
        Update a Call Queue Forced Forward Service

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
        :param play_announcement_before_enabled: Indicates whether an announcement plays to callers before the action
            is applied.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: The type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['forcedForwardEnabled'] = forced_forward_enabled
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        super().put(url, params=params, json=body)

    def get_call_queue_holiday_service(self, location_id: str, queue_id: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        data = super().get(url, params=params)
        r = GetCallQueueHolidayObject.model_validate(data)
        return r

    def update_call_queue_holiday_service(self, location_id: str, queue_id: str, holiday_service_enabled: bool,
                                          action: GetCallQueueHolidayObjectAction,
                                          holiday_schedule_level: CallQueueHolidaySchedulesObjectScheduleLevel,
                                          play_announcement_before_enabled: bool,
                                          audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                          holiday_schedule_name: str = None, transfer_phone_number: str = None,
                                          audio_files: list[AudioAnnouncementFileFeatureObject] = None,
                                          org_id: str = None) -> None:
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
        :param action: The call processing action type.
        :type action: GetCallQueueHolidayObjectAction
        :param holiday_schedule_level: The schedule mentioned in `holidayScheduleName` is org or location specific.
            (Must be from `holidaySchedules` list)
        :type holiday_schedule_level: CallQueueHolidaySchedulesObjectScheduleLevel
        :param play_announcement_before_enabled: Indicates whether an announcement plays to callers before the action
            is applied.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: The type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param holiday_schedule_name: Name of the schedule configured for a holiday service as one of from
            `holidaySchedules` list.
        :type holiday_schedule_name: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
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
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        super().put(url, params=params, json=body)

    def get_call_queue_night_service(self, location_id: str, queue_id: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        data = super().get(url, params=params)
        r = GetCallQueueNightServiceObject.model_validate(data)
        return r

    def update_call_queue_night_service(self, location_id: str, queue_id: str, night_service_enabled: bool,
                                        play_announcement_before_enabled: bool,
                                        announcement_mode: GetCallQueueNightServiceObjectAnnouncementMode,
                                        audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                        force_night_service_enabled: bool,
                                        manual_audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                        action: GetCallQueueHolidayObjectAction = None,
                                        transfer_phone_number: str = None,
                                        audio_files: list[AudioAnnouncementFileFeatureObject] = None,
                                        business_hours_name: str = None,
                                        business_hours_level: CallQueueHolidaySchedulesObjectScheduleLevel = None,
                                        manual_audio_files: list[AudioAnnouncementFileFeatureObject] = None,
                                        org_id: str = None) -> None:
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
        :param play_announcement_before_enabled: Indicates whether an announcement plays to callers before the action
            is applied.
        :type play_announcement_before_enabled: bool
        :param announcement_mode: The type of announcements to played.
        :type announcement_mode: GetCallQueueNightServiceObjectAnnouncementMode
        :param audio_message_selection: The type of announcements to be played when announcementMode is set to
            `NORMAL`.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param force_night_service_enabled: Force night service regardless of business hour schedule.
        :type force_night_service_enabled: bool
        :param manual_audio_message_selection: The type of announcements to be played when announcementMode is set to
            `MANUAL`.
        :type manual_audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param action: The call processing action type.
        :type action: GetCallQueueHolidayObjectAction
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureObject]
        :param business_hours_name: Name of the schedule configured for a night service as one of from
            `businessHourSchedules` list.
        :type business_hours_name: str
        :param business_hours_level: The above mentioned schedule is org or location specific. (Must be from
            `businessHourSchedules` list)
        :type business_hours_level: CallQueueHolidaySchedulesObjectScheduleLevel
        :param manual_audio_files: List Of pre-configured Audio Files.
        :type manual_audio_files: list[AudioAnnouncementFileFeatureObject]
        :param org_id: Update call queue night service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['nightServiceEnabled'] = night_service_enabled
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        body['announcementMode'] = enum_str(announcement_mode)
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        if business_hours_name is not None:
            body['businessHoursName'] = business_hours_name
        if business_hours_level is not None:
            body['businessHoursLevel'] = enum_str(business_hours_level)
        body['forceNightServiceEnabled'] = force_night_service_enabled
        body['manualAudioMessageSelection'] = enum_str(manual_audio_message_selection)
        if manual_audio_files is not None:
            body['manualAudioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureObject]).dump_python(manual_audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        super().put(url, params=params, json=body)

    def get_call_queue_stranded_calls(self, location_id: str, queue_id: str,
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
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        data = super().get(url, params=params)
        r = GetCallQueueStrandedCallsObject.model_validate(data)
        return r

    def update_call_queue_stranded_calls(self, location_id: str, queue_id: str,
                                         action: GetCallQueueHolidayObjectAction,
                                         audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting,
                                         transfer_phone_number: str = None,
                                         audio_files: list[AudioAnnouncementFileFeatureObject] = None,
                                         org_id: str = None) -> None:
        """
        Update a Call Queue Stranded Calls Service

        Update the designated Call Stranded Calls Service.

        Allow admin to modify configured Stranded Calls settings.

        Updating a call queue stranded calls requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param action: The call processing action type.
        :type action: GetCallQueueHolidayObjectAction
        :param audio_message_selection: The type of announcement to be played.
        :type audio_message_selection: CallQueueQueueSettingsGetObjectOverflowGreeting
        :param transfer_phone_number: Call gets transferred to this number when action is set to `TRANSFER`. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
        :type audio_files: list[AudioAnnouncementFileFeatureObject]
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['action'] = enum_str(action)
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        body['audioMessageSelection'] = enum_str(audio_message_selection)
        if audio_files is not None:
            body['audioFiles'] = TypeAdapter(list[AudioAnnouncementFileFeatureObject]).dump_python(audio_files, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        super().put(url, params=params, json=body)

    def list_call_queues(self, location_id: str = None, name: str = None, phone_number: str = None,
                         department_id: str = None, department_name: str = None, has_cx_essentials: bool = None,
                         org_id: str = None, **params: Any) -> Generator[ListCallQueueEssentialsObject, None, None]:
        """
        Read the List of Call Queues with Customer Assist

        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud, when all agents
        assigned to receive calls from the queue are unavailable. Queued calls are routed to
        an available agent, when not on an active call. Each call queue is assigned a lead number, which is a telephone
        number that external callers can dial to reach the users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach the users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Returns the list of call queues in this location.
        :type location_id: str
        :param name: Returns only the call queues matching the given name.
        :type name: str
        :param phone_number: Returns only the call queues matching the given primary phone number or extension.
        :type phone_number: str
        :param department_id: Returns only call queues matching the given department ID.
        :type department_id: str
        :param department_name: Returns only call queues matching the given department name.
        :type department_name: str
        :param has_cx_essentials: Returns only the list of call queues with Customer Assist license when `true`,
            otherwise returns the list of Customer Experience Basic call queues.
        :type has_cx_essentials: bool
        :param org_id: Returns the list of call queues in this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallQueueEssentialsObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if department_id is not None:
            params['departmentId'] = department_id
        if department_name is not None:
            params['departmentName'] = department_name
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('queues')
        return self.session.follow_pagination(url=url, model=ListCallQueueEssentialsObject, item_key='queues', params=params)

    def list_call_queue_agents(self, location_id: str = None, queue_id: str = None, name: str = None,
                               phone_number: str = None, join_enabled: bool = None, has_cx_essentials: bool = None,
                               order: str = None, org_id: str = None,
                               **params: Any) -> Generator[ListCallQueueAgentObject, None, None]:
        """
        Read the List of Call Queue Agents with Customer Assist

        List all Call Queues Agents for the organization.

        Agents can be users, workplace or virtual lines assigned to a call queue. Calls from the call queue are routed
        to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **Note**: The decoded value of the agent's `id`, and the `type` returned in the response, are always returned
        as `PEOPLE`, even when the agent is a workspace or virtual line. This will be addressed in a future release.

        :param location_id: Return only the call queue agents in this location.
        :type location_id: str
        :param queue_id: Only return call queue agents with the matching queue ID.
        :type queue_id: str
        :param name: Returns only the list of call queue agents that match the given name.
        :type name: str
        :param phone_number: Returns only the list of call queue agents that match the given phone number or extension.
        :type phone_number: str
        :param join_enabled: Returns only the list of call queue agents that match the given `joinEnabled` value.
        :type join_enabled: bool
        :param has_cx_essentials: Returns only the list of call queues with Customer Assist license when `true`,
            otherwise returns the list of Customer Experience Basic call queues.
        :type has_cx_essentials: bool
        :param order: Sort results alphabetically by call queue agent's name, in ascending or descending order.
        :type order: str
        :param org_id: List call queues agents in this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListCallQueueAgentObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if queue_id is not None:
            params['queueId'] = queue_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if join_enabled is not None:
            params['joinEnabled'] = str(join_enabled).lower()
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        if order is not None:
            params['order'] = order
        url = self.ep('queues/agents')
        return self.session.follow_pagination(url=url, model=ListCallQueueAgentObject, item_key='agents', params=params)

    def get_call_queue_available_agents(self, location_id: str, name: str = None, phone_number: str = None,
                                        order: str = None, org_id: str = None,
                                        **params: Any) -> Generator[AvailableAgentObject, None, None]:
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

    def get_call_queue_agent(self, id: str, max_: int, start: int, has_cx_essentials: bool = None,
                             org_id: str = None) -> GetCallQueueAgentObject:
        """
        Get Details for a Call Queue Agent with Customer Assist

        Retrieve details of a particular Call queue agent based on the agent ID.

        Agents can be users, workplace or virtual lines assigned to a call queue. Calls from the call queue are routed
        to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        Retrieving a call queue agent's details require a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        **Note**: The agent's `type` returned in the response and in the decoded value of the agent's `id`, is always
        of type `PEOPLE`, even if the agent is a workspace or virtual line. This` will be corrected in a future
        release.

        :param id: Retrieve call queue agents with this identifier.
        :type id: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param has_cx_essentials: Must be set to `true` to view the details of an agent with Customer Assist license.
            This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Retrieve call queue agents from this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueAgentObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        params['max'] = max_
        params['start'] = start
        url = self.ep(f'queues/agents/{id}')
        data = super().get(url, params=params)
        r = GetCallQueueAgentObject.model_validate(data)
        return r

    def update_agent_call_queue_settings(self, id: str, settings: list[ModifyAgentsForCallQueueObjectSettingsItem],
                                         has_cx_essentials: bool = None, org_id: str = None) -> None:
        """
        Update an Agent's Settings of One or More Call Queues with Customer Assist

        Modify an agent's call queue settings for an organization.

        Calls from the call queue are routed to agents based on configuration.
        An agent can be assigned to one or more call queues and can be managed by supervisors.

        This operation requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param id: Identifier of the agent to be updated.
        :type id: str
        :param settings: -
        :type settings: list[ModifyAgentsForCallQueueObjectSettingsItem]
        :param has_cx_essentials: Must be set to `true` to modify an agent that has Customer Assist license. This can
            otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Update the settings of an agent in this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body: dict[str, Any] = dict()
        body['settings'] = TypeAdapter(list[ModifyAgentsForCallQueueObjectSettingsItem]).dump_python(settings, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'queues/agents/{id}/settings')
        super().put(url, params=params, json=body)

    def get_call_queue_settings(self, org_id: str = None) -> CallQueueSettingsGet:
        """
        Get Call Queue Settings

        Retrieve Call Queue Settings for a specific organization.

        Call Queue Settings configure organization-wide defaults for call queues, including supervisor tone
        notifications for barge in, silent monitoring, and coaching; optimized simultaneous-ring handling that
        preserves caller queue position; and bounced-call handling for Customer Assist agents. Individual call queues
        can use the organization-level tone defaults or override them with queue-specific `playToneToAgent*` settings.

        Retrieving Call Queue Settings requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Call Queue Settings for this organization.
        :type org_id: str
        :rtype: :class:`CallQueueSettingsGet`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('queues/settings')
        data = super().get(url, params=params)
        r = CallQueueSettingsGet.model_validate(data)
        return r

    def update_call_queue_settings(self, maintain_queue_position_for_sim_ring_enabled: bool = None,
                                   force_agent_unavailable_on_bounced_enabled: bool = None,
                                   play_tone_to_agent_for_barge_in_enabled: bool = None,
                                   play_tone_to_agent_for_silent_monitoring_enabled: bool = None,
                                   play_tone_to_agent_for_supervisor_coaching_enabled: bool = None,
                                   org_id: str = None) -> None:
        """
        Update Call Queue Settings

        Update Call Queue Settings for a specific organization.

        Call Queue Settings configure organization-wide defaults for call queues, including supervisor tone
        notifications for barge in, silent monitoring, and coaching; optimized simultaneous-ring handling that
        preserves caller queue position; and bounced-call handling for Customer Assist agents. Individual call queues
        can use the organization-level tone defaults or override them with queue-specific `playToneToAgent*` settings.

        Updating Call Queue Settings requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param maintain_queue_position_for_sim_ring_enabled: Indicates whether callers keep their queue position when
            simultaneous ringing routes a call to multiple agents.
        :type maintain_queue_position_for_sim_ring_enabled: bool
        :param force_agent_unavailable_on_bounced_enabled: Indicates whether Customer Assist agents are changed to
            unavailable after bounced calls.
        :type force_agent_unavailable_on_bounced_enabled: bool
        :param play_tone_to_agent_for_barge_in_enabled: Organization-wide default that plays a tone to agents when a
            supervisor joins an active call using barge in.
        :type play_tone_to_agent_for_barge_in_enabled: bool
        :param play_tone_to_agent_for_silent_monitoring_enabled: Organization-wide default that plays a tone to agents
            when a supervisor monitors their active call without joining.
        :type play_tone_to_agent_for_silent_monitoring_enabled: bool
        :param play_tone_to_agent_for_supervisor_coaching_enabled: Organization-wide default that plays a tone to
            agents when a supervisor coaches an agent during an active call.
        :type play_tone_to_agent_for_supervisor_coaching_enabled: bool
        :param org_id: Call Queue Settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if maintain_queue_position_for_sim_ring_enabled is not None:
            body['maintainQueuePositionForSimRingEnabled'] = maintain_queue_position_for_sim_ring_enabled
        if force_agent_unavailable_on_bounced_enabled is not None:
            body['forceAgentUnavailableOnBouncedEnabled'] = force_agent_unavailable_on_bounced_enabled
        if play_tone_to_agent_for_barge_in_enabled is not None:
            body['playToneToAgentForBargeInEnabled'] = play_tone_to_agent_for_barge_in_enabled
        if play_tone_to_agent_for_silent_monitoring_enabled is not None:
            body['playToneToAgentForSilentMonitoringEnabled'] = play_tone_to_agent_for_silent_monitoring_enabled
        if play_tone_to_agent_for_supervisor_coaching_enabled is not None:
            body['playToneToAgentForSupervisorCoachingEnabled'] = play_tone_to_agent_for_supervisor_coaching_enabled
        url = self.ep('queues/settings')
        super().put(url, params=params, json=body)

    def delete_bulk_call_queue_supervisors(self, supervisor_ids: list[str], delete_all: bool = None,
                                           org_id: str = None) -> None:
        """
        Delete Bulk Supervisors

        Deletes supervisors in bulk from an organization.

        Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_ids: Array of supervisors IDs to be deleted.
        :type supervisor_ids: list[str]
        :param delete_all: If present the `supervisorIds` array is ignored, and all supervisors in the context are
            deleted. **WARNING**: This will remove all supervisors from the organization.
        :type delete_all: bool
        :param org_id: Delete supervisors in bulk for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['supervisorIds'] = supervisor_ids
        if delete_all is not None:
            body['deleteAll'] = delete_all
        url = self.ep('supervisors')
        super().delete(url, params=params, json=body)

    def list_call_queue_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                    has_cx_essentials: bool = None, org_id: str = None,
                                    **params: Any) -> Generator[ListSupervisorObject, None, None]:
        """
        Get List of Supervisors with Customer Assist

        Get list of supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        Requires a full, location, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return the supervisors that match the given name.
        :type name: str
        :param phone_number: Only return the supervisors that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of supervisors with Customer Assist license, when `true`.
            Otherwise returns the list of supervisors with Customer Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: List the supervisors in this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListSupervisorObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('supervisors')
        return self.session.follow_pagination(url=url, model=ListSupervisorObject, item_key='supervisors', params=params)

    def create_call_queue_supervisor(self, id: str, agents: list[PostPersonPlaceVirtualLineSupervisorObject],
                                     has_cx_essentials: bool = None, org_id: str = None) -> None:
        """
        Create a Supervisor with Customer Assist

        Create a new supervisor. The supervisor must be created with at least one agent.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param id: A unique identifier for the supervisor.
        :type id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineSupervisorObject]
        :param has_cx_essentials: Creates a Customer Assist queue supervisor, when `true`. Customer Assist queue
            supervisors must have a Customer Assist license.
        :type has_cx_essentials: bool
        :param org_id: The organization ID where the supervisor needs to be created.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body: dict[str, Any] = dict()
        body['id'] = id
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineSupervisorObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('supervisors')
        super().post(url, params=params, json=body)

    def list_available_call_queue_agents(self, name: str = None, phone_number: str = None, order: str = None,
                                         has_cx_essentials: bool = None, org_id: str = None,
                                         **params: Any) -> Generator[AvailableAgentListObject, None, None]:
        """
        List Available Agents with Customer Assist

        Get list of available agents for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Returns only the agents that match the given name.
        :type name: str
        :param phone_number: Returns only the agents that match the phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of available agents with Customer Assist license, when `true`.
            When ommited or set to `false`, will return the list of available agents with Customer Experience Basic
            license.
        :type has_cx_essentials: bool
        :param org_id: List of available agents in a supervisor's list for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAgentListObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('supervisors/availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgentListObject, item_key='agents', params=params)

    def list_available_call_queue_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                              has_cx_essentials: bool = None, org_id: str = None,
                                              **params: Any) -> Generator[AvailableSupervisorsListObject, None, None]:
        """
        List Available Supervisors with Customer Assist

        Get list of available supervisors for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Only return the supervisors that match the given name.
        :type name: str
        :param phone_number: Only return the supervisors that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Returns only the list of available supervisors with Customer Assist license, when
            `true`. When ommited or set to 'false', will return the list of available supervisors with Customer
            Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: List the available supervisors in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableSupervisorsListObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('supervisors/availableSupervisors')
        return self.session.follow_pagination(url=url, model=AvailableSupervisorsListObject, item_key='supervisors', params=params)

    def delete_call_queue_supervisor(self, supervisor_id: str, org_id: str = None) -> None:
        """
        Delete a Supervisor

        Deletes the supervisor from an organization.

        Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Delete the specified supervisor.
        :type supervisor_id: str
        :param org_id: Delete the supervisor in the specified organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'supervisors/{supervisor_id}')
        super().delete(url, params=params)

    def get_call_queue_supervisor(self, supervisor_id: str, max_: int = None, start: int = None, name: str = None,
                                  phone_number: str = None, order: str = None, has_cx_essentials: bool = None,
                                  org_id: str = None) -> GetCallQueueSupervisorResponse:
        """
        Get Supervisor Detail with Customer Assist

        Get details of a specific supervisor, which includes the agents associated agents with the supervisor, in an
        organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param supervisor_id: List the agents assigned to this supervisor.
        :type supervisor_id: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return the agents that match the given name.
        :type name: str
        :param phone_number: Only return agents that match the given phone number, extension, or ESN.
        :type phone_number: str
        :param order: Sort results alphabetically by supervisor name, in ascending or descending order.
        :type order: str
        :param has_cx_essentials: Must be set to `true`, to view the details of a supervisor with Customer Assist
            license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: List the agents assigned to a supervisor in this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueSupervisorResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'supervisors/{supervisor_id}')
        data = super().get(url, params=params)
        r = GetCallQueueSupervisorResponse.model_validate(data)
        return r

    def update_call_queue_supervisor_agents(self, supervisor_id: str,
                                            agents: list[PutPersonPlaceVirtualLineAgentObject],
                                            has_cx_essentials: bool = None, org_id: str = None) -> None:
        """
        Assign or Unassign Agents to Supervisor with Customer Assist

        Assign or unassign agents to the supervisor for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Identifier of the supervisor to be updated.
        :type supervisor_id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls. **WARNING**: The `id`
            returned is in UUID format, since we don't have agentType from OCI response. This will be converting to
            Hydra type in future release.
        :type agents: list[PutPersonPlaceVirtualLineAgentObject]
        :param has_cx_essentials: Must be set to `true` to modify a supervisor with Customer Assist license. This can
            otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Assign or unassign agents to a supervisor in this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body: dict[str, Any] = dict()
        body['agents'] = TypeAdapter(list[PutPersonPlaceVirtualLineAgentObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'supervisors/{supervisor_id}')
        super().put(url, params=params, json=body)
