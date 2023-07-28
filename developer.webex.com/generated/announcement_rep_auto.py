from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Action', 'Action13', 'Action3', 'Action9', 'AlternateNumberSettings', 'AlternateNumbersObject',
           'AlternateNumbersWithPattern', 'AlternateNumbersWithPattern1', 'AnnouncementAudioFile', 'AnnouncementMode',
           'AnnouncementsListResponse', 'AudioAnnouncementFileGetObject', 'CallBounce',
           'CallQueueHolidaySchedulesObject', 'CallQueueQueueSettingsObject', 'ComfortMessage', 'ComfortMessageBypass',
           'CreateAutoAttendantBody', 'CreateAutoAttendantResponse', 'CreateCallQueueResponse', 'DistinctiveRing',
           'ExtensionDialing', 'FeatureReferenceObject',
           'FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse',
           'FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse',
           'FetchRepositoryUsageForAnnouncementsFororganizationResponse', 'GetAnnouncementFileInfo',
           'GetDetailsForAutoAttendantResponse', 'GetDetailsForCallQueueForcedForwardResponse',
           'GetDetailsForCallQueueHolidayServiceResponse', 'GetDetailsForCallQueueNightServiceResponse',
           'GetDetailsForCallQueueResponse', 'GetDetailsForCallQueueStrandedCallsResponse', 'GetMusicOnHoldResponse',
           'GetPersonPlaceVirtualLineCallQueueObject', 'Greeting', 'Greeting27', 'HoursMenuGetObject',
           'HoursMenuObject', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'Key', 'KeyConfigurationsGetObject',
           'KeyConfigurationsObject', 'Level', 'Level22', 'LocationObject', 'MediaFileType', 'MediaType',
           'ModifyPersonPlaceVirtualLineCallQueueObject', 'MohMessage', 'NormalSource', 'Overflow',
           'PostCallQueueCallPolicyObject', 'PostPersonPlaceVirtualLineCallQueueObject',
           'ReadListOfCallQueueAnnouncementFilesResponse', 'RingPatternObject', 'Type',
           'UpdateCallQueueStrandedCallsServiceBody', 'UploadbinaryAnnouncementGreetingAtOrganizationLevelResponse',
           'UploadbinaryAnnouncementGreetingAtlocationLevelResponse', 'WaitMessage', 'WaitMode',
           'WebexCallingOrganizationSettingswithAnnouncementsRepositoryFeatureApi', 'WelcomeMessage']


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    id: Optional[str]
    #: Name of the Location.
    name: Optional[str]


class AnnouncementsListResponse(LocationObject):
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str]
    #: Size of the file in kilobytes.
    file_size: Optional[str]
    #: Media file type of the announcement file.
    media_file_type: Optional[str]
    #: LastUpdated timestamp (in UTC format) of the announcement.
    last_updated: Optional[str]
    #: The level at which this announcement exists.
    level: Optional[str]
    #: The details of location at which this announcement exists.
    location: Optional[LocationObject]


class FeatureReferenceObject(LocationObject):
    #: Resource Type of the call feature.
    type: Optional[str]
    #: Unique identifier of the location.
    location_id: Optional[str]
    #: Location name of the announcement file.
    location_name: Optional[str]


class FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse(LocationObject):
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str]
    #: Size of the file in kilobytes.
    file_size: Optional[str]
    #: Media file type of the announcement file.
    media_file_type: Optional[str]
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[str]
    #: Reference count of the call features this announcement is assigned to.
    feature_reference_count: Optional[int]
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]]


class FetchRepositoryUsageForAnnouncementsFororganizationResponse(ApiModel):
    #: Total file size used by announcements in this repository in kilobytes.
    total_file_size_used_kb: Optional[int]
    #: Maximum audio file size allowed to upload in kilobytes.
    max_audio_file_size_allowed_kb: Optional[int]
    #: Maximum video file size allowed to upload in kilobytes.
    max_video_file_size_allowed_kb: Optional[int]
    #: Total file size limit for the repository in megabytes.
    total_file_size_limit_mb: Optional[int]


class HuntRoutingTypeSelection(ApiModel):
    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based: Optional[str]
    #: This option uses skill level as the criteria to route calls to agents. When there is more than one agent with
    #: the same skill level, the selected policy helps dispatch the calls to the agents.
    skill_based: Optional[str]


class HuntPolicySelection(ApiModel):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next
    #: available agent. This is supported for SKILL_BASED.
    circular: Optional[str]
    #: Send the call through the queue of agents in order, starting from the top each time. This is supported for
    #: SKILL_BASED.
    regular: Optional[str]
    #: Sends calls to all agents at once
    simultaneous: Optional[str]
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has
    #: been idle the second longest, and so on until the call is answered. This is supported for SKILL_BASED.
    uniform: Optional[str]
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100%).
    weighted: Optional[str]


class CallBounce(ApiModel):
    #: If enabled, bounce calls after the set number of rings.
    call_bounce_enabled: Optional[bool]
    #: Number of rings after which to bounce call, if callBounce is enabled.
    call_bounce_max_rings: Optional[int]
    #: Bounce if agent becomes unavailable.
    agent_unavailable_enabled: Optional[bool]
    #: Alert agent if call on hold more than alertAgentMaxSeconds.
    alert_agent_enabled: Optional[bool]
    #: Number of second after which to alert agent if alertAgentEnabled.
    alert_agent_max_seconds: Optional[int]
    #: Bounce if call on hold more than callBounceMaxSeconds.
    call_bounce_on_hold_enabled: Optional[bool]
    #: Number of second after which to bounce if callBounceEnabled.
    call_bounce_on_hold_max_seconds: Optional[int]


class RingPatternObject(ApiModel):
    #: Normal incoming ring pattern.
    normal: Optional[str]
    #: Incoming ring pattern of two long rings.
    long_long: Optional[str]
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long: Optional[str]
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short: Optional[str]


class DistinctiveRing(ApiModel):
    #: Whether or not the distinctiveRing is enabled.
    enabled: Optional[bool]
    #: Ring pattern for when this call queue is called. Only available when distinctiveRing is enabled for the call
    #: queue.
    ring_pattern: Optional[RingPatternObject]


class PostCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents. The routing type should be SKILL_BASED if you want to
    #: assign skill level to agents. Only certain policy are allowed in SKILL_BASED type.
    routing_type: Optional[HuntRoutingTypeSelection]
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: Settings for when the call into the hunt group is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctiveRing option enabled.
    distinctive_ring: Optional[DistinctiveRing]


class Action(str, Enum):
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class Greeting(str, Enum):
    #: Play the custom announcement specified by the fileName field.
    custom = 'CUSTOM'
    #: Play default announcement.
    default = 'DEFAULT'


class Level22(str, Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'


class Level(Level22):
    entity = 'ENTITY'


class AnnouncementAudioFile(LocationObject):
    #: Media file type of announcement file.
    media_file_type: Optional[str]
    #: The level at which this announcement exists.
    level: Optional[Level]


class Overflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[Action]
    #: When true, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external transferNumber is entered.
    send_to_voicemail: Optional[bool]
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str]
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    overflow_after_wait_enabled: Optional[bool]
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. The minimum
    #: value 0, The maximum value is 7200 seconds.
    overflow_after_wait_time: Optional[int]
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by
    #: a user.
    play_overflow_greeting_enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement files to be played as overflow greetings. These files are from the list of announcement
    #: files associated with this call queue. For CUSTOM announcement, a minimum of 1 file is mandatory, and the
    #: maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]]


class NormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement files to be played as mohMessage greetings. These files are from the list of announcement
    #: files associated with this call queue. For CUSTOM announcement, a minimum of 1 file is mandatory, and the
    #: maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]]


class WelcomeMessage(NormalSource):
    #: Mandatory entrance message. The default value is false.
    always_enabled: Optional[bool]


class WaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class WaitMessage(ApiModel):
    #: If enabled play Wait Message.
    enabled: Optional[bool]
    #: Estimated wait message operating mode. Supported values TIME and POSITION.
    wait_mode: Optional[WaitMode]
    #: The number of minutes for which the estimated wait is played. The minimum time is 10 minutes. The maximum time
    #: is 100 minutes.
    handling_time: Optional[int]
    #: The default number of call handling minutes. The minimum time is 1 minutes, The maximum time is 100 minutes.
    default_handling_time: Optional[int]
    #: The number of the position for which the estimated wait is played. The minimum positions are 10, The maximum
    #: positions are 100.
    queue_position: Optional[int]
    #: Play time / Play position High Volume.
    high_volume_message_enabled: Optional[bool]
    #: The number of estimated waiting times in seconds. The minimum time is 10 seconds. The maximum time is 600
    #: seconds.
    estimated_waiting_time: Optional[int]
    #: Callback options enabled/disabled. Default value is false.
    callback_option_enabled: Optional[bool]
    #: The minimum estimated callback times in minutes. The default value is 30.
    minimum_estimated_callback_time: Optional[int]
    #: The international numbers for callback is enabled/disabled. The default value is false.
    international_callback_enabled: Optional[bool]
    #: Play updated estimated wait message.
    play_updated_estimated_wait_message: Optional[str]


class ComfortMessage(NormalSource):
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    time_between_messages: Optional[int]


class ComfortMessageBypass(NormalSource):
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The
    #: minimum time is 1 seconds. The maximum time is 120 seconds.
    call_waiting_age_threshold: Optional[int]


class MohMessage(ApiModel):
    normal_source: Optional[NormalSource]
    alternate_source: Optional[NormalSource]


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are
    #: triggered.
    queue_size: Optional[int]
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool]
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool]
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[Overflow]
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call
    #: queue while there is an available agent, the caller will not hear this announcement and is transferred to an
    #: agent. The welcome message feature is enabled by default.
    welcome_message: Optional[WelcomeMessage]
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[WaitMessage]
    #: Play a message after the welcome message and before hold music. This is typically a CUSTOM announcement that
    #: plays information, such as current promotions or information about products and services.
    comfort_message: Optional[ComfortMessage]
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that
    #: should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort
    #: message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[ComfortMessageBypass]
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[MohMessage]
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces
    #: the identity of the call queue from which the call is coming.
    whisper_message: Optional[NormalSource]


class PostPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str]
    #: Weight of person, workspace or virtual line. Only applied when call policy is WEIGHTED.
    weight: Optional[str]
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is SKILL_BASED.
    skill_level: Optional[int]


class AlternateNumbersWithPattern(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPatternObject]


class AlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for the Alternate Numbers.
    distinctive_ring_enabled: Optional[bool]
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]


class Type(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetPersonPlaceVirtualLineCallQueueObject(PostPersonPlaceVirtualLineCallQueueObject):
    #: Type of the person, workspace or virtual line.
    type: Optional[Type]
    #: First name of person, workspace or virtual line.
    first_name: Optional[str]
    #: First name of person, workspace or virtual line.
    last_name: Optional[str]
    #: Phone number of person, workspace or virtual line.
    phone_number: Optional[str]
    #: Extension of person, workspace or virtual line.
    extension: Optional[str]
    #: Indicates the join status of the agent for this queue. The default value while creating call queue is true.
    join_enabled: Optional[bool]


class ModifyPersonPlaceVirtualLineCallQueueObject(PostPersonPlaceVirtualLineCallQueueObject):
    #: Indicates the join status of the agent for this queue. The default value for newly added agents is true.
    join_enabled: Optional[bool]


class MediaType(ApiModel):
    #: WMA File Extension.
    wma: Optional[str]
    #: WAV File Extension.
    wav: Optional[str]
    #: 3GP File Extension.
    gp: Optional[str]
    #: MOV File Extension.
    mov: Optional[str]


class GetAnnouncementFileInfo(ApiModel):
    #: ID of the announcement.
    id: Optional[str]
    #: Name of greeting file.
    file_name: Optional[str]
    #: Size of greeting file in kilo-bytes.
    file_size: Optional[str]
    #: Media file type of the announcement.
    media_file_type: Optional[MediaType]
    #: Level where the announcement is created.
    level: Optional[Level]


class AlternateNumbersWithPattern1(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPatternObject]


class AlternateNumbersObject(AlternateNumbersWithPattern1):
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]


class ExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class MediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    three_gp = '3GP'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    id: Optional[str]
    #: Audio announcement file name.
    file_name: Optional[str]
    #: Audio announcement file type.
    media_file_type: Optional[MediaFileType]
    #: Audio announcement file type location.
    level: Optional[Level22]


class Key(str, Enum):
    digit_0 = 'digit_0'
    digit_1 = 'digit_1'
    digit_2 = 'digit_2'
    digit_3 = 'digit_3'
    digit_4 = 'digit_4'
    digit_5 = 'digit_5'
    digit_6 = 'digit_6'
    digit_7 = 'digit_7'
    digit_8 = 'digit_8'
    digit_9 = 'digit_9'
    hash = 'hash'


class Action3(str, Enum):
    #: Plays the message and then transfers the call to the specified number.
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    #: Transfers the call to the specified number, without playing a transfer prompt.
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    #: Plays the message and then transfers the call to the specified operator number.
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    #: Brings the user into the automated name directory.
    name_dialing = 'NAME_DIALING'
    #: Prompts the user for an extension, and transfers the user.
    extension_dialing = 'EXTENSION_DIALING'
    #: Replays the Auto Attendant greeting.
    repeat_menu = 'REPEAT_MENU'
    #: Terminates the call.
    exit = 'EXIT'
    #: Prompts the user for an extension, and transfers the user to voice mailbox of the dialed extension.
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    #: Return back to the previous menu.
    return_to_previous_menu = 'RETURN_TO_PREVIOUS_MENU'
    #: Plays a recorded message and then returns to the current Auto Attendant menu.
    play_announcement = 'PLAY_ANNOUNCEMENT'


class KeyConfigurationsGetObject(ApiModel):
    #: Key assigned to specific menu configuration.
    key: Optional[Key]
    #: Action assigned to specific menu key configuration.
    action: Optional[Action3]
    #: The description of each menu key.
    description: Optional[str]
    #: Value based on actions.
    value: Optional[str]
    #: Pre-configured announcement audio files when PLAY_ANNOUNCEMENT is set.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject]


class HoursMenuGetObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    greeting: Optional[Greeting]
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: Optional[bool]
    #: Announcement Audio File details.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject]
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsGetObject]


class KeyConfigurationsObject(ApiModel):
    #: Key assigned to specific menu configuration.
    key: Optional[Key]
    #: Action assigned to specific menu key configuration.
    action: Optional[Action3]
    #: The description of each menu key.
    description: Optional[str]
    #: Value based on actions.
    value: Optional[str]
    #: Pre-configured announcement audio files when PLAY_ANNOUNCEMENT is set.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject]


class HoursMenuObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    greeting: Optional[Greeting]
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: Optional[bool]
    #: Announcement Audio File details.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject]
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsObject]


class CreateAutoAttendantBody(ApiModel):
    #: Unique name for the auto attendant.
    name: Optional[str]
    #: Auto attendant phone number. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Auto attendant extension. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: First name defined for an auto attendant.
    first_name: Optional[str]
    #: Last name defined for an auto attendant.
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[ExtensionDialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[ExtensionDialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuObject]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuObject]


class Greeting27(str, Enum):
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets
    #: the customer know they are still connected.
    system = 'SYSTEM'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class CallQueueHolidaySchedulesObject(ApiModel):
    #: Name of the schedule configured for a holiday service.
    schedule_name: Optional[str]
    #: Specifies whether the schedule mentioned in scheduleName is org or location specific.
    schedule_level: Optional[Level22]


class Action9(str, Enum):
    #: The caller hears a fast-busy tone.
    busy = 'BUSY'
    #: Transfers the call to number specified in transferPhoneNumber.
    transfer = 'TRANSFER'


class Action13(Action9):
    #: Call remains in the queue.
    none = 'NONE'
    #: Calls are handled according to the Night Service configuration. If the Night Service action is set to none, then
    #: this is equivalent to this policy being set to none (that is, calls remain in the queue).
    night_service = 'NIGHT_SERVICE'
    #: Calls are removed from the queue and are provided with ringing until the caller releases the call. The ringback
    #: tone played to the caller is localized according to the country code of the caller.
    ringing = 'RINGING'
    #: Calls are removed from the queue and are provided with an announcement that is played in a loop until the caller
    #: releases the call.
    announcement = 'ANNOUNCEMENT'


class GetDetailsForCallQueueStrandedCallsResponse(ApiModel):
    #: Specifies call processing action type.
    action: Optional[Action13]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class UpdateCallQueueStrandedCallsServiceBody(ApiModel):
    #: Specifies call processing action type.
    action: Optional[Action13]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class AnnouncementMode(str, Enum):
    #: Plays announcement as per audioMessageSelection.
    normal = 'NORMAL'
    #: Plays announcement as per manualAudioMessageSelection.
    manual = 'MANUAL'


class UploadbinaryAnnouncementGreetingAtOrganizationLevelResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str]


class FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse(ApiModel):
    #: Array of announcements.
    announcements: Optional[list[AnnouncementsListResponse]]


class UploadbinaryAnnouncementGreetingAtlocationLevelResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str]


class CreateCallQueueBody(ApiModel):
    #: Unique name for the call queue.
    name: Optional[str]
    #: Primary phone number of the call queue. Either a phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Primary phone extension of the call queue. Either a phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to phoneNumber if set, otherwise
    #: defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class CreateCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class GetDetailsForCallQueueResponse(LocationObject):
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]
    #: Language for the call queue.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phoneNumber if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Extension of the call queue.
    extension: Optional[str]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]


class UpdateCallQueueBody(ApiModel):
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]
    #: Unique name for the call queue.
    name: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phoneNumber if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Extension of the call queue.
    extension: Optional[str]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[ModifyPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class ReadListOfCallQueueAnnouncementFilesResponse(ApiModel):
    #: Array of announcements for this call queue.
    announcements: Optional[list[GetAnnouncementFileInfo]]


class GetDetailsForAutoAttendantResponse(LocationObject):
    #: Flag to indicate if auto attendant number is enabled or not.
    enabled: Optional[bool]
    #: Auto attendant phone number. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Auto attendant extension. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]
    #: First name defined for an auto attendant.
    first_name: Optional[str]
    #: Last name defined for an auto attendant.
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]]
    #: Language for the auto attendant.
    language: Optional[str]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[ExtensionDialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[ExtensionDialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuGetObject]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuGetObject]


class CreateAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant.
    id: Optional[str]


class GetMusicOnHoldResponse(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    call_hold: Optional[bool]
    #: If enabled, music will be played when call is parked.
    call_park: Optional[bool]
    #: Greeting type for the location.
    greeting: Optional[Greeting27]
    #: Announcement Audio File details when greeting is selected to be CUSTOM.
    audio_file: Optional[AudioAnnouncementFileGetObject]


class UpdateMusicOnHoldBody(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    call_hold_enabled: Optional[bool]
    #: If enabled, music will be played when call is parked.
    call_park_enabled: Optional[bool]
    #: Greeting type for the location.
    greeting: Optional[Greeting27]
    #: Announcement Audio File details when greeting is selected to be CUSTOM.
    audio_file: Optional[AudioAnnouncementFileGetObject]


class GetDetailsForCallQueueForcedForwardResponse(ApiModel):
    #: Whether or not the call queue forced forward routing policy setting is enabled.
    forced_forward_enabled: Optional[bool]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class UpdateCallQueueForcedForwardServiceBody(ApiModel):
    #: Enable or disable call forced forward service routing policy.
    forced_forward_enabled: Optional[bool]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class GetDetailsForCallQueueHolidayServiceResponse(GetDetailsForCallQueueStrandedCallsResponse):
    #: Whether or not the call queue holiday service routing policy is enabled.
    holiday_service_enabled: Optional[bool]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from
    #: holidaySchedules list)
    holiday_schedule_level: Optional[Level22]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Lists the pre-configured holiday schedules.
    holiday_schedules: Optional[list[CallQueueHolidaySchedulesObject]]


class UpdateCallQueueHolidayServiceBody(UpdateCallQueueStrandedCallsServiceBody):
    #: Enable or Disable the call queue holiday service routing policy.
    holiday_service_enabled: Optional[bool]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from
    #: holidaySchedules list)
    holiday_schedule_level: Optional[Level22]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]


class GetDetailsForCallQueueNightServiceResponse(GetDetailsForCallQueueStrandedCallsResponse):
    #: Whether or not the call queue night service routing policy is enabled.
    night_service_enabled: Optional[bool]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules
    #: list).
    business_hours_level: Optional[Level22]
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: Optional[list[CallQueueHolidaySchedulesObject]]
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of Audio Files.
    manual_audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class UpdateCallQueueNightServiceBody(UpdateCallQueueStrandedCallsServiceBody):
    #: Enable or disable call queue night service routing policy.
    night_service_enabled: Optional[bool]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules
    #: list)
    business_hours_level: Optional[Level22]
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of pre-configured Audio Files.
    manual_audio_files: Optional[list[AudioAnnouncementFileGetObject]]


class WebexCallingOrganizationSettingswithAnnouncementsRepositoryFeatureApi(ApiChild, base='telephony/config/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for
    administrators utilizing People Webex Calling APIs.
    Modifying these organization settings requires a full administrator auth token with a scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query
    parameter.
    """

    def uploadbinary_announcement_greeting_at_organization_level(self, org_id: str = None) -> str:
        """
        Upload a binary file to the announcement repository at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write .

        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/upload-a-binary-announcement-greeting-at-organization-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements')
        data = super().post(url=url, params=params)
        return data["id"]

    def fetch_list_of_announcement_greetings_on_location_and_organization_level(self, org_id: str = None, location_id: str = None, order: str = None, file_name: str = None, file_type: str = None, media_file_type: str = None, name: str = None, **params) -> Generator[AnnouncementsListResponse, None, None]:
        """
        Fetch a list of binary announcement greetings at an organization as well as location level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned. Possible values: all, locations,
            Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
        :type location_id: str
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/fetch-list-of-announcement-greetings-on-location-and-organization-level
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return self.session.follow_pagination(url=url, model=AnnouncementsListResponse, item_key='announcements', params=params)

    def fetch_details_ofbinary_announcement_greeting_atorganization_level(self, announcement_id: str, org_id: str = None) -> FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse:
        """
        Fetch details of a binary announcement greeting by its ID at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/fetch-details-of-a-binary-announcement-greeting-at-the-organization-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        data = super().get(url=url, params=params)
        return FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse.parse_obj(data)

    def modifybinary_announcement_greeting(self, announcement_id: str, org_id: str = None):
        """
        Modify an existing announcement greeting at an organization level.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/modify-a-binary-announcement-greeting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        super().put(url=url, params=params)
        return

    def fetch_repository_usage_for_announcements_fororganization(self, org_id: str = None) -> FetchRepositoryUsageForAnnouncementsFororganizationResponse:
        """
        Retrieves repository usage for announcements for an organization.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/fetch-repository-usage-for-announcements-for-an-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements/usage')
        data = super().get(url=url, params=params)
        return FetchRepositoryUsageForAnnouncementsFororganizationResponse.parse_obj(data)

    def deleteannouncement_greeting_oforganization(self, announcement_id: str, org_id: str = None):
        """
        Delete an announcement greeting for an organization.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/delete-an-announcement-greeting-of-the-organization
        """
        params = {}
        params['announcementId'] = announcement_id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements/{announcementsId}')
        super().delete(url=url, params=params)
        return

    def uploadbinary_announcement_greeting_atlocation_level(self, location_id: str, org_id: str = None) -> str:
        """
        Upload a binary file to the announcement repository at a location level.
        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write .

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/upload-a-binary-announcement-greeting-at-the-location-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements')
        data = super().post(url=url, params=params)
        return data["id"]

    def fetch_details_ofbinary_announcement_greeting_at_location_level(self, location_id: str, announcement_id: str, org_id: str = None) -> FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse:
        """
        Fetch details of a binary announcement greeting by its ID at a location level.
        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/fetch-details-of-a-binary-announcement-greeting-at-location-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = super().get(url=url, params=params)
        return FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse.parse_obj(data)

    def modifybinary_announcement_greeting(self, announcement_id: str, org_id: str = None):
        """
        Modify an existing announcement greeting at an organization level.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/modify-a-binary-announcement-greeting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().put(url=url, params=params)
        return

    def fetch_repository_usage_for_announcements_inlocation(self, location_id: str, org_id: str = None) -> FetchRepositoryUsageForAnnouncementsFororganizationResponse:
        """
        Retrieves repository usage for announcements in a location.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/fetch-repository-usage-for-announcements-in-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/usage')
        data = super().get(url=url, params=params)
        return FetchRepositoryUsageForAnnouncementsFororganizationResponse.parse_obj(data)

    def deleteannouncement_greeting_inlocation(self, location_id: str, org_id: str = None):
        """
        Delete an announcement greeting in a location.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Unique identifier of a location where announcement is being created.
        :type location_id: str
        :param org_id: Create a announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/delete-an-announcement-greeting-in-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcements_id}')
        super().delete(url=url, params=params)
        return

    def create_queue(self, location_id: str, name: str, call_policies: PostCallQueueCallPolicyObject, queue_settings: CallQueueQueueSettingsObject, agents: PostPersonPlaceVirtualLineCallQueueObject, org_id: str = None, phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, allow_agent_join_enabled: bool = None, phone_number_for_outgoing_calls_enabled: bool = None) -> str:
        """
        Create new Call Queues for the given location.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Creating a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param name: Unique name for the call queue.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: PostPersonPlaceVirtualLineCallQueueObject
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :param phone_number: Primary phone number of the call queue. Either a phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Primary phone extension of the call queue. Either a phoneNumber or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to
            phoneNumber if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the call queue.
        :type time_zone: str
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them
            to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/create-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallQueueBody()
        if name is not None:
            body.name = name
        if call_policies is not None:
            body.call_policies = call_policies
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if agents is not None:
            body.agents = agents
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if time_zone is not None:
            body.time_zone = time_zone
        if allow_agent_join_enabled is not None:
            body.allow_agent_join_enabled = allow_agent_join_enabled
        if phone_number_for_outgoing_calls_enabled is not None:
            body.phone_number_for_outgoing_calls_enabled = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def details_for_queue(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueResponse:
        """
        Retrieve Call Queue details.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueResponse.parse_obj(data)

    def update_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsObject, org_id: str = None, enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, phone_number: str = None, extension: str = None, alternate_number_settings: AlternateNumberSettings = None, call_policies: PostCallQueueCallPolicyObject = None, allow_call_waiting_for_agents_enabled: bool = None, agents: ModifyPersonPlaceVirtualLineCallQueueObject = None, allow_agent_join_enabled: bool = None, phone_number_for_outgoing_calls_enabled: bool = None):
        """
        Update the designated Call Queue.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Updating a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param enabled: Whether or not the call queue is enabled.
        :type enabled: bool
        :param name: Unique name for the call queue.
        :type name: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the
            phoneNumber if set, otherwise defaults to call group name.
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
        :type alternate_number_settings: AlternateNumberSettings
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: ModifyPersonPlaceVirtualLineCallQueueObject
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them
            to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueBody()
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if enabled is not None:
            body.enabled = enabled
        if name is not None:
            body.name = name
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if time_zone is not None:
            body.time_zone = time_zone
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if alternate_number_settings is not None:
            body.alternate_number_settings = alternate_number_settings
        if call_policies is not None:
            body.call_policies = call_policies
        if allow_call_waiting_for_agents_enabled is not None:
            body.allow_call_waiting_for_agents_enabled = allow_call_waiting_for_agents_enabled
        if agents is not None:
            body.agents = agents
        if allow_agent_join_enabled is not None:
            body.allow_agent_join_enabled = allow_agent_join_enabled
        if phone_number_for_outgoing_calls_enabled is not None:
            body.phone_number_for_outgoing_calls_enabled = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_queue_announcement_files(self, location_id: str, queue_id: str, org_id: str = None, level: enum = None) -> list[GetAnnouncementFileInfo]:
        """
        List file info for all Call Queue announcement files associated with this Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.
        Retrieving this list of files requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve anouncement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str
        :param level: return the Call Queue announcement files list for this level
        :type level: enum

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/read-the-list-of-call-queue-announcement-files
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if level is not None:
            params['level'] = level
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[GetAnnouncementFileInfo], data["announcements"])

    def details_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> GetDetailsForAutoAttendantResponse:
        """
        Retrieve an Auto Attendant details.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForAutoAttendantResponse.parse_obj(data)

    def create_auto_attendant(self, location_id: str, name: str, business_schedule: str, business_hours_menu: HoursMenuObject, after_hours_menu: HoursMenuObject, org_id: str = None, phone_number: str = None, extension: str = None, first_name: str = None, last_name: str = None, alternate_numbers: AlternateNumbersObject = None, language_code: str = None, holiday_schedule: str = None, extension_dialing: ExtensionDialing = None, name_dialing: ExtensionDialing = None, time_zone: str = None) -> str:
        """
        Create new Auto Attendant for the given location.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Creating an auto attendant requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :param phone_number: Auto attendant phone number. Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension. Either phoneNumber or extension is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: AlternateNumbersObject
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            ENTERPRISE.
        :type extension_dialing: ExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: ExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/create-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateAutoAttendantBody()
        if name is not None:
            body.name = name
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if business_hours_menu is not None:
            body.business_hours_menu = business_hours_menu
        if after_hours_menu is not None:
            body.after_hours_menu = after_hours_menu
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if alternate_numbers is not None:
            body.alternate_numbers = alternate_numbers
        if language_code is not None:
            body.language_code = language_code
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if extension_dialing is not None:
            body.extension_dialing = extension_dialing
        if name_dialing is not None:
            body.name_dialing = name_dialing
        if time_zone is not None:
            body.time_zone = time_zone
        url = self.ep(f'locations/{location_id}/autoAttendants')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_auto_attendant(self, location_id: str, auto_attendant_id: str, name: str, business_schedule: str, business_hours_menu: HoursMenuObject, after_hours_menu: HoursMenuObject, org_id: str = None, phone_number: str = None, extension: str = None, first_name: str = None, last_name: str = None, alternate_numbers: AlternateNumbersObject = None, language_code: str = None, holiday_schedule: str = None, extension_dialing: ExtensionDialing = None, name_dialing: ExtensionDialing = None, time_zone: str = None):
        """
        Update the designated Auto Attendant.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Updating an auto attendant requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject
        :param org_id: Update an auto attendant from this organization.
        :type org_id: str
        :param phone_number: Auto attendant phone number. Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension. Either phoneNumber or extension is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: AlternateNumbersObject
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            ENTERPRISE.
        :type extension_dialing: ExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: ExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateAutoAttendantBody()
        if name is not None:
            body.name = name
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if business_hours_menu is not None:
            body.business_hours_menu = business_hours_menu
        if after_hours_menu is not None:
            body.after_hours_menu = after_hours_menu
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if alternate_numbers is not None:
            body.alternate_numbers = alternate_numbers
        if language_code is not None:
            body.language_code = language_code
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if extension_dialing is not None:
            body.extension_dialing = extension_dialing
        if name_dialing is not None:
            body.name_dialing = name_dialing
        if time_zone is not None:
            body.time_zone = time_zone
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def music_on_hold(self, location_id: str, org_id: str = None) -> GetMusicOnHoldResponse:
        """
        Retrieve the location's music on hold settings.
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        Retrieving a location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve music on hold settings for this location.
        :type location_id: str
        :param org_id: Retrieve music on hold settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-music-on-hold
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/musicOnHold')
        data = super().get(url=url, params=params)
        return GetMusicOnHoldResponse.parse_obj(data)

    def update_music_on_hold(self, location_id: str, greeting: Greeting27, org_id: str = None, call_hold_enabled: bool = None, call_park_enabled: bool = None, audio_file: AudioAnnouncementFileGetObject = None):
        """
        Update the location's music on hold settings.
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        Updating a location's music on hold settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param greeting: Greeting type for the location.
        :type greeting: Greeting27
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        :param audio_file: Announcement Audio File details when greeting is selected to be CUSTOM.
        :type audio_file: AudioAnnouncementFileGetObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-music-on-hold
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateMusicOnHoldBody()
        if greeting is not None:
            body.greeting = greeting
        if call_hold_enabled is not None:
            body.call_hold_enabled = call_hold_enabled
        if call_park_enabled is not None:
            body.call_park_enabled = call_park_enabled
        if audio_file is not None:
            body.audio_file = audio_file
        url = self.ep(f'locations/{location_id}/musicOnHold')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_forced_forward(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueForcedForwardResponse:
        """
        Retrieve Call Queue policy Forced Forward details.
        This policy allows calls to be temporarily diverted to a configured destination.
        Retrieving call queue Forced Forward details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-a-call-queue-forced-forward
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueForcedForwardResponse.parse_obj(data)

    def update_queue_forced_forward_service(self, location_id: str, queue_id: str, forced_forward_enabled: bool, play_announcement_before_enabled: bool, audio_message_selection: Greeting, org_id: str = None, transfer_phone_number: str = None, audio_files: AudioAnnouncementFileGetObject = None):
        """
        Update the designated Forced Forward Service.
        If the option is enabled, then incoming calls to the queue are forwarded to the configured destination. Calls
        that are already in the queue remain queued.
        The policy can be configured to play an announcement prior to proceeding with the forward.
        Updating a call queue Forced Forward service requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

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
        :type audio_message_selection: Greeting
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: AudioAnnouncementFileGetObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-a-call-queue-forced-forward-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueForcedForwardServiceBody()
        if forced_forward_enabled is not None:
            body.forced_forward_enabled = forced_forward_enabled
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_files is not None:
            body.audio_files = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_holiday_service(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueHolidayServiceResponse:
        """
        Retrieve Call Queue Holiday Service details.
        Configure the call queue to route calls differently during the holidays.
        Retrieving call queue holiday service details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-a-call-queue-holiday-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueHolidayServiceResponse.parse_obj(data)

    def update_queue_holiday_service(self, location_id: str, queue_id: str, action: Action13, audio_message_selection: Greeting, holiday_service_enabled: bool, holiday_schedule_level: Level22, play_announcement_before_enabled: bool, org_id: str = None, transfer_phone_number: str = None, audio_files: AudioAnnouncementFileGetObject = None, holiday_schedule_name: str = None):
        """
        Update the designated Call Queue Holiday Service.
        Configure the call queue to route calls differently during the holidays.
        Updating a call queue holiday service requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param action: Specifies call processing action type.
        :type action: Action13
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param holiday_service_enabled: Enable or Disable the call queue holiday service routing policy.
        :type holiday_service_enabled: bool
        :param holiday_schedule_level: Specifies whether the schedule mentioned in holidayScheduleName is org or
            location specific. (Must be from holidaySchedules list)
        :type holiday_schedule_level: Level22
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: AudioAnnouncementFileGetObject
        :param holiday_schedule_name: Name of the schedule configured for a holiday service as one of from
            holidaySchedules list.
        :type holiday_schedule_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-a-call-queue-holiday-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueHolidayServiceBody()
        if action is not None:
            body.action = action
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if holiday_service_enabled is not None:
            body.holiday_service_enabled = holiday_service_enabled
        if holiday_schedule_level is not None:
            body.holiday_schedule_level = holiday_schedule_level
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_files is not None:
            body.audio_files = audio_files
        if holiday_schedule_name is not None:
            body.holiday_schedule_name = holiday_schedule_name
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_night_service(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueNightServiceResponse:
        """
        Retrieve Call Queue Night service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-a-call-queue-night-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueNightServiceResponse.parse_obj(data)

    def update_queue_night_service(self, location_id: str, queue_id: str, action: Action13, audio_message_selection: Greeting, night_service_enabled: bool, play_announcement_before_enabled: bool, announcement_mode: AnnouncementMode, force_night_service_enabled: bool, manual_audio_message_selection: Greeting, org_id: str = None, transfer_phone_number: str = None, audio_files: AudioAnnouncementFileGetObject = None, business_hours_name: str = None, business_hours_level: Level22 = None, manual_audio_files: AudioAnnouncementFileGetObject = None):
        """
        Update Call Queue Night Service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Updating call queue night service details requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param action: Specifies call processing action type.
        :type action: Action13
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param night_service_enabled: Enable or disable call queue night service routing policy.
        :type night_service_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param announcement_mode: Specifies the type of announcements to played.
        :type announcement_mode: AnnouncementMode
        :param force_night_service_enabled: Force night service regardless of business hour schedule.
        :type force_night_service_enabled: bool
        :param manual_audio_message_selection: Specifies what type of announcement to be played when announcementMode
            is MANUAL.
        :type manual_audio_message_selection: Greeting
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: AudioAnnouncementFileGetObject
        :param business_hours_name: Name of the schedule configured for a night service as one of from
            businessHourSchedules list.
        :type business_hours_name: str
        :param business_hours_level: Specifies whether the above mentioned schedule is org or location specific. (Must
            be from businessHourSchedules list)
        :type business_hours_level: Level22
        :param manual_audio_files: List Of pre-configured Audio Files.
        :type manual_audio_files: AudioAnnouncementFileGetObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-a-call-queue-night-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueNightServiceBody()
        if action is not None:
            body.action = action
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if night_service_enabled is not None:
            body.night_service_enabled = night_service_enabled
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if announcement_mode is not None:
            body.announcement_mode = announcement_mode
        if force_night_service_enabled is not None:
            body.force_night_service_enabled = force_night_service_enabled
        if manual_audio_message_selection is not None:
            body.manual_audio_message_selection = manual_audio_message_selection
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_files is not None:
            body.audio_files = audio_files
        if business_hours_name is not None:
            body.business_hours_name = business_hours_name
        if business_hours_level is not None:
            body.business_hours_level = business_hours_level
        if manual_audio_files is not None:
            body.manual_audio_files = manual_audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_stranded(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueStrandedCallsResponse:
        """
        Allow admin to view default/configured Stranded Calls settings.
        A stranded call is processed by a queue that has no agents currently staffed.
        Retrieving call queue Stranded Calls details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/get-details-for-a-call-queue-stranded-calls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueStrandedCallsResponse.parse_obj(data)

    def update_queue_stranded_service(self, location_id: str, queue_id: str, action: Action13, audio_message_selection: Greeting, org_id: str = None, transfer_phone_number: str = None, audio_files: AudioAnnouncementFileGetObject = None):
        """
        Update the designated Call Stranded Calls Service.
        Allow admin to modify configured Stranded Calls settings.
        A stranded call is processed by a queue that has no agents currently staffed.
        Updating a call queue stranded calls requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param action: Specifies call processing action type.
        :type action: Action13
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: AudioAnnouncementFileGetObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-announcements-repository-feature/update-a-call-queue-stranded-calls-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueStrandedCallsServiceBody()
        if action is not None:
            body.action = action
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_files is not None:
            body.audio_files = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        super().put(url=url, params=params, data=body.json())
        return
