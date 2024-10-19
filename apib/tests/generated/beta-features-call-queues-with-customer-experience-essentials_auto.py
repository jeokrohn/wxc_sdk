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
           'AvailableAgentListObject', 'AvailableSupervisorsListObject',
           'BetaFeaturesCallQueuesWithCustomerExperienceEssentialsApi', 'CallQueueQueueSettingsObject',
           'CallQueueQueueSettingsObjectOverflow', 'CallQueueQueueSettingsObjectOverflowAction',
           'CallQueueQueueSettingsObjectOverflowGreeting', 'CallQueueSettingsObject',
           'CallQueueSettingsObjectComfortMessage', 'CallQueueSettingsObjectComfortMessageBypass',
           'CallQueueSettingsObjectMohMessage', 'CallQueueSettingsObjectMohMessageNormalSource',
           'CallQueueSettingsObjectOverflow', 'CallQueueSettingsObjectWaitMessage',
           'CallQueueSettingsObjectWaitMessageWaitMode', 'CallQueueSettingsObjectWelcomeMessage',
           'CreateCallQueueObjectCallingLineIdPolicy', 'GetCallQueueCallPolicyObject',
           'GetCallQueueCallPolicyObjectCallBounce', 'GetCallQueueCallPolicyObjectDistinctiveRing',
           'GetCallQueueObject', 'GetCallQueueObjectAlternateNumberSettings', 'GetPersonPlaceObject',
           'GetSupervisorDetailsResponse', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'ListCallQueueObject',
           'ListCallQueueObjectDepartment', 'ListSupervisorAgentObject', 'ListSupervisorAgentStatusObject',
           'ListSupervisorObject', 'PostCallQueueCallPolicyObject', 'PostPersonPlaceVirtualLineCallQueueObject',
           'PostPersonPlaceVirtualLineSupervisorObject', 'PutPersonPlaceVirtualLineAgentObject', 'RingPatternObject',
           'UserType']


class ListCallQueueObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class ListCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvNTU1MzY4Y2QtZDg5Mi00YzFlLTk0YjYtNzdjNjRiYWQ3NWMx
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: 5714328359
    name: Optional[str] = None
    #: Denotes if the call queue has Customer Experience Essentials license.
    #: example: True
    has_cx_essentials: Optional[bool] = None
    #: Name of location for call queue.
    #: example: WXCSIVDKCPAPIC4S1
    location_name: Optional[str] = None
    #: ID of location for call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    location_id: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Primary phone extension of the call queue.
    #: example: 7781
    extension: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[ListCallQueueObjectDepartment] = None


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
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Ring pattern for when this alternate number is called. Only available when `distinctiveRing` is enabled for the
    #: hunt group.
    #: example: NORMAL
    ring_pattern: Optional[RingPatternObject] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for Alternate Number.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None


class HuntPolicySelection(str, Enum):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next
    #: available agent.
    circular = 'CIRCULAR'
    #: Send the call through the queue of agents in order, starting from the top each time.
    regular = 'REGULAR'
    #: Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has
    #: been idle the second longest, and so on until the call is answered.
    uniform = 'UNIFORM'
    #: Sends call to idle agents based on percentages you assign to each agent (up to 100%).
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
    #: Alert agent if call on hold more than alertAgentMaxSeconds.
    #: example: True
    alert_agent_enabled: Optional[bool] = None
    #: Number of second after which to alert agent if alertAgentEnabled.
    #: example: 20
    alert_agent_max_seconds: Optional[int] = None
    #: Bounce if call on hold more than callBounceMaxSeconds.
    #: example: True
    call_bounce_on_hold_enabled: Optional[bool] = None
    #: Number of second after which to bounce if callBounceEnabled.
    #: example: 20
    call_bounce_on_hold_max_seconds: Optional[int] = None


class GetCallQueueCallPolicyObjectDistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Ring pattern for when this callqueue is called. Only available when `distinctiveRing` is enabled for the call
    #: queue.
    #: example: NORMAL
    ring_pattern: Optional[RingPatternObject] = None


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class CallQueueQueueSettingsObjectOverflowAction(str, Enum):
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class CallQueueQueueSettingsObjectOverflowGreeting(str, Enum):
    #: Play the custom announcement specified by the `fileName` field.
    custom = 'CUSTOM'
    #: Play default announcement.
    default = 'DEFAULT'


class CallQueueQueueSettingsObjectOverflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    #: example: PERFORM_BUSY_TREATMENT
    action: Optional[CallQueueQueueSettingsObjectOverflowAction] = None
    #: When `true`, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external `transferNumber` is entered.
    send_to_voicemail: Optional[bool] = None
    #: Destination number for overflow calls when `action` is set to `TRANSFER_TO_PHONE_NUMBER`.
    #: example: +15553331212
    transfer_number: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    #: example: True
    overflow_after_wait_enabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    #: example: 20
    overflow_after_wait_time: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise callers will hear the hold music until the call is answered by a
    #: user.
    #: example: True
    play_overflow_greeting_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement file name strings to be played as overflow greetings. These files are from the list of
    #: announcements files associated with this call queue.
    audio_files: Optional[list[str]] = None


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are
    #: triggered.
    #: example: 50
    queue_size: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled__true_: Optional[bool] = Field(alias='callOfferToneEnabled `true`', default=None)
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsObjectOverflow] = None


class GetPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: Hakim
    first_name: Optional[str] = None
    #: First name of person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone number of person or workspace.
    #: example: +15555551234
    phone_number: Optional[str] = None
    #: Extension of person or workspace.
    #: example: 1234
    extension: Optional[str] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None


class GetCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvNTU1MzY4Y2QtZDg5Mi00YzFlLTk0YjYtNzdjNjRiYWQ3NWMx
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: CallQueue-1
    name: Optional[str] = None
    #: Denotes if the call queue has Customer Experience Essentials license.
    #: example: True
    has_cx_essentials: Optional[bool] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set,
    #: otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Extension of the call queue.
    #: example: 7781
    extension: Optional[str] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Language for call queue.
    #: example: English
    language: Optional[str] = None
    #: Language code for call queue.
    #: example: en-US
    language_code: Optional[str] = None
    #: Time zone for the call queue.
    #: example: America/Chicago
    time_zone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[GetCallQueueCallPolicyObject] = None
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject] = None
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool] = None
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceObject]] = None
    #: Specifies the department information.
    department: Optional[ListCallQueueObjectDepartment] = None


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


class PostCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents. The routing type should be `SKILL_BASED` if you want to
    #: assign skill level to `agents`. Only certain `policy` are allowed in `SKILL_BASED` type.
    #: example: PRIORITY_BASED
    routing_type: Optional[HuntRoutingTypeSelection] = None
    #: Call routing policy to use to dispatch calls to `agents`.
    #: example: CIRCULAR
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the hunt group is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the `distinctiveRing` option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class AnnouncementAudioFileLevel(str, Enum):
    location = 'LOCATION'
    organization = 'ORGANIZATION'
    entity = 'ENTITY'


class AnnouncementAudioFile(ApiModel):
    #: Unique identifier of the Announcement file.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8zMjAxNjRmNC1lNWEzLTQxZmYtYTMyNi02N2MwOThlNDFkMWQ
    id: Optional[str] = None
    #: Name of the announcement file. `name`, `mediaFileType`, `level` are mandatory if `id` is not provided for
    #: uploading an announcement.
    #: example: Public_Announcement.wav
    name: Optional[str] = None
    #: Media file type of announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: The level at which this announcement exists.
    #: example: LOCATION
    level: Optional[AnnouncementAudioFileLevel] = None


class CallQueueSettingsObjectOverflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    #: example: PERFORM_BUSY_TREATMENT
    action: Optional[CallQueueQueueSettingsObjectOverflowAction] = None
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
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `overflow` greetings. These files are from the list of announcement
    #: files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is mandatory, and the
    #: maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueSettingsObjectWelcomeMessage(ApiModel):
    #: If enabled play entrance message. The default value is `true`.
    #: example: True
    enabled: Optional[bool] = None
    #: Mandatory entrance message. The default value is `false`.
    always_enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `welcomeMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueSettingsObjectWaitMessageWaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class CallQueueSettingsObjectWaitMessage(ApiModel):
    #: If enabled play Wait Message.
    #: example: True
    enabled: Optional[bool] = None
    #: Estimated wait message operating mode. Supported values `TIME` and `POSITION`.
    #: example: POSITION
    wait_mode: Optional[CallQueueSettingsObjectWaitMessageWaitMode] = None
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


class CallQueueSettingsObjectComfortMessage(ApiModel):
    #: If enabled play periodic comfort message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    #: example: 10
    time_between_messages: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueSettingsObjectComfortMessageBypass(ApiModel):
    #: If enabled play comfort bypass message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The
    #: minimum time is 1 seconds. The maximum time is 120 seconds.
    #: example: 10
    call_waiting_age_threshold: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `comfortMessageBypass` greetings. These files are from the list of
    #: announcements files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueSettingsObjectMohMessageNormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement files to be played as `mohMessage` greetings. These files are from the list of
    #: announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 file is
    #: mandatory, and the maximum is 4.
    audio_announcement_files: Optional[list[AnnouncementAudioFile]] = None


class CallQueueSettingsObjectMohMessage(ApiModel):
    normal_source: Optional[CallQueueSettingsObjectMohMessageNormalSource] = None
    alternate_source: Optional[CallQueueSettingsObjectMohMessageNormalSource] = None


class CallQueueSettingsObject(ApiModel):
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
    overflow: Optional[CallQueueSettingsObjectOverflow] = None
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call
    #: queue while there is an available agent, the caller will not hear this announcement and is transferred to an
    #: agent. The welcome message feature is enabled by default.
    welcome_message: Optional[CallQueueSettingsObjectWelcomeMessage] = None
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[CallQueueSettingsObjectWaitMessage] = None
    #: Play a message after the welcome message and before hold music. This is typically a `CUSTOM` announcement that
    #: plays information, such as current promotions or information about products and services.
    comfort_message: Optional[CallQueueSettingsObjectComfortMessage] = None
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that
    #: should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort
    #: message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[CallQueueSettingsObjectComfortMessageBypass] = None
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[CallQueueSettingsObjectMohMessage] = None
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces
    #: the identity of the call queue from which the call is coming.
    whisper_message: Optional[CallQueueSettingsObjectMohMessageNormalSource] = None


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


class AvailableSupervisorsListObject(ApiModel):
    #: A unique identifier for the supervisor.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YzVlODRhMS0wZmEwLTQzNDAtODVkZC1mMzM1ZGQ4MTkxMmI
    id: Optional[str] = None
    #: First name of the supervisor.
    #: example: Adam
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    #: example: Sandler
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the supervisor.
    #: example: Adam Sandler
    display_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    #: example: +19845550200
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34543
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 345430020
    esn: Optional[str] = None


class ListSupervisorObject(ApiModel):
    #: A unique identifier for the supervisor.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81OGVkZTIwNi0yNTM5LTQ1ZjQtODg4Ny05M2E3ZWIwZWI3ZDI
    id: Optional[str] = None
    #: First name of the supervisor.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of the supervisor.
    #: example: Smith
    last_name: Optional[str] = None
    #: Primary phone number of the supervisor.
    #: example: +19845550186
    phone_number: Optional[str] = None
    #: Primary phone extension of the supervisor.
    #: example: 12554
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 3412554
    esn: Optional[str] = None
    #: Number of agents managed by supervisor. A supervisor must manage at least one agent.
    #: example: 2
    agent_count: Optional[str] = None


class ListSupervisorAgentObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85NTA4OTc4ZC05YmFkLTRmYWEtYTljNC0wOWQ4NWQ4ZmRjZTY
    id: Optional[str] = None
    #: Last name of the agent.
    #: example: user
    last_name: Optional[str] = None
    #: First name of the agent.
    #: example: test
    first_name: Optional[str] = None
    #: Primary phone extension of the agent.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix + extension of a agent.
    #: example: 20
    esn: Optional[str] = None
    #: Primary phone number of the agent.
    #: example: +1972998998
    phone_number: Optional[str] = None


class AgentAction(str, Enum):
    #: Assign an agent to a supervisor.
    add = 'ADD'
    #: Remove an agent from a supervisor.
    delete = 'DELETE'


class PutPersonPlaceVirtualLineAgentObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81OGVkZTIwNi0yNTM5LTQ1ZjQtODg4Ny05M2E3ZWIwZWI3ZDI
    id: Optional[str] = None
    #: Enumeration that indicates whether an agent needs to be added (`ADD`) or deleted (`DELETE`) from a supervisor.
    action: Optional[AgentAction] = None


class UserType(str, Enum):
    #: Associated type is a person.
    people = 'PEOPLE'
    #: Associated type is a workspace.
    place = 'PLACE'
    #: Associated type is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class AvailableAgentListObject(ApiModel):
    #: A unique identifier for the agent.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80YzVlODRhMS0wZmEwLTQzNDAtODVkZC1mMzM1ZGQ4MTkxMmI
    id: Optional[str] = None
    #: First name of the agent.
    #: example: Adam
    first_name: Optional[str] = None
    #: Last name of the agent.
    #: example: Sandler
    last_name: Optional[str] = None
    #: (string, optional) - Display name of the agent.
    #: example: Adam Sandler
    display_name: Optional[str] = None
    #: Primary phone number of the agent.
    #: example: +19845550200
    phone_number: Optional[str] = None
    #: Primary phone extension of the agent.
    #: example: 20
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 34543
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person.
    #: example: 345430020
    esn: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[UserType] = None


class ListSupervisorAgentStatusObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85NTA4OTc4ZC05YmFkLTRmYWEtYTljNC0wOWQ4NWQ4ZmRjZTY
    id: Optional[str] = None
    #: status of the agent.
    #: example: DUPLICATE
    status: Optional[str] = None
    #: Detailed message for the status.
    #: example: [Error 6612] Agent 9508978d-9bad-4faa-a9c4-09d85d8fdce6 is already assigned to the supervisor.
    message: Optional[str] = None


class PostPersonPlaceVirtualLineSupervisorObject(ApiModel):
    #: Identifier of the person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzE3NzczMWRiLWE1YzEtNGI2MC05ZTMwLTNhM2MxMGFiM2IxMQ
    id: Optional[str] = None


class GetSupervisorDetailsResponse(ApiModel):
    #: unique identifier of the supervisor
    id: Optional[str] = None
    #: Array of agents assigned to a specific supervisor.
    agents: Optional[list[ListSupervisorAgentObject]] = None


class BetaFeaturesCallQueuesWithCustomerExperienceEssentialsApi(ApiChild, base='telephony/config'):
    """
    Beta Features: Call Queues with Customer Experience Essentials
    
    Webex Customer Experience Essentials APIs provide the core capabilities of the Webex Contact Center solution. These
    APIs allows you to
    manage Customer Experience Essentials features such as supervisor configuration, agent configuration, and call
    queue configuration, which are distinct from Customer Experience Basic.
    
    `Learn more about the customer Experience Essentials suite
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_
    
    Viewing the read-only customer Experience Essentials APIs requires a full, device or read-only administrator auth
    token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying the customer Experience Essentials APIs requires a full or device administrator auth token with a scope
    of
    `spark-admin:telephony_config_write`.
    """

    def read_the_list_of_call_queues(self, location_id: str = None, name: str = None, phone_number: str = None,
                                     department_id: str = None, department_name: str = None,
                                     has_cx_essentials: bool = None, org_id: str = None,
                                     **params) -> Generator[ListCallQueueObject, None, None]:
        """
        Read the List of Call Queues

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
        :param has_cx_essentials: Returns only the list of call queues with Customer Experience Essentials license when
            `true`, otherwise returns the list of Customer Experience Basic call queues.
        :type has_cx_essentials: bool
        :param org_id: Returns the list of call queues in this organization.
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
        if department_id is not None:
            params['departmentId'] = department_id
        if department_name is not None:
            params['departmentName'] = department_name
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep('queues')
        return self.session.follow_pagination(url=url, model=ListCallQueueObject, item_key='queues', params=params)

    def get_details_for_a_call_queue(self, location_id: str, queue_id: str, has_cx_essentials: bool = None,
                                     org_id: str = None) -> GetCallQueueObject:
        """
        Get Details for a Call Queue

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
        :param has_cx_essentials: Must be set to `true`, to view the details of a call queue with Customer Experience
            Essentials license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Retrieves the details of a call queue in this organization.
        :type org_id: str
        :rtype: :class:`GetCallQueueObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url, params=params)
        r = GetCallQueueObject.model_validate(data)
        return r

    def create_a_call_queue(self, location_id: str, name: str, call_policies: PostCallQueueCallPolicyObject,
                            queue_settings: CallQueueSettingsObject,
                            agents: list[PostPersonPlaceVirtualLineCallQueueObject], has_cx_essentials: bool = None,
                            phone_number: str = None, extension: str = None, language_code: str = None,
                            first_name: str = None, last_name: str = None, time_zone: str = None,
                            calling_line_id_policy: CreateCallQueueObjectCallingLineIdPolicy = None,
                            calling_line_id_phone_number: str = None, allow_agent_join_enabled: bool = None,
                            phone_number_for_outgoing_calls_enabled: bool = None, org_id: str = None) -> str:
        """
        Create a Call Queue

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
        :type call_policies: PostCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueSettingsObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineCallQueueObject]
        :param has_cx_essentials: Creates a Customer Experience Essentials call queue, when `true`. This requires
            Customer Experience Essentials licensed agents.
        :type has_cx_essentials: bool
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
        :param phone_number_for_outgoing_calls_enabled: When `true`, indicates that the agent's configuration allows
            them to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        :param org_id: The organization ID where the call queue needs to be created.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
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

    def create_a_supervisor(self, id: str, agents: list[PostPersonPlaceVirtualLineSupervisorObject],
                            has_cx_essentials: bool = None,
                            org_id: str = None) -> list[ListSupervisorAgentStatusObject]:
        """
        Create a Supervisor

        Create a new supervisor. The supervisor must be created with at least one agent.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param id: A unique identifier for the supervisor.
        :type id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PostPersonPlaceVirtualLineSupervisorObject]
        :param has_cx_essentials: Creates a Customer Experience Essentials queue supervisor, when `true`. Customer
            Experience Essentials queue supervisors must have a Customer Experience Essentials license.
        :type has_cx_essentials: bool
        :param org_id: The organization ID where the supervisor needs to be created.
        :type org_id: str
        :rtype: list[ListSupervisorAgentStatusObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body = dict()
        body['id'] = id
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineSupervisorObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('supervisors')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[ListSupervisorAgentStatusObject]).validate_python(data['supervisorAgentStatus'])
        return r

    def get_list_of_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                has_cx_essentials: bool = None, org_id: str = None,
                                **params) -> Generator[ListSupervisorObject, None, None]:
        """
        Get List of Supervisors

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
        :param has_cx_essentials: Returns only the list of supervisors with Customer Experience Essentials license,
            when `true`. Otherwise returns the list of supervisors with Customer Experience Basic license.
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

    def list_available_supervisors(self, name: str = None, phone_number: str = None, order: str = None,
                                   has_cx_essentials: bool = None, org_id: str = None,
                                   **params) -> Generator[AvailableSupervisorsListObject, None, None]:
        """
        List Available Supervisors

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
        :param has_cx_essentials: Returns only the list of available supervisors with Customer Experience Essentials
            license, when `true`. When ommited or set to 'false', will return the list of available supervisors with
            Customer Experience Basic license.
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

    def get_supervisor_details(self, supervisor_id: str, max_: int = None, start: int = None, name: str = None,
                               phone_number: str = None, order: str = None, has_cx_essentials: bool = None,
                               org_id: str = None) -> GetSupervisorDetailsResponse:
        """
        GET Supervisor Details

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
        :param has_cx_essentials: Must be set to `true`, to view the details of a supervisor with Customer Experience
            Essentials license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: List the agents assigned to a supervisor in this organization.
        :type org_id: str
        :rtype: :class:`GetSupervisorDetailsResponse`
        """
        params = {}
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
        r = GetSupervisorDetailsResponse.model_validate(data)
        return r

    def assign_or_unassign_agents_to_supervisor(self, supervisor_id: str,
                                                agents: list[PutPersonPlaceVirtualLineAgentObject],
                                                has_cx_essentials: bool = None,
                                                org_id: str = None) -> list[ListSupervisorAgentStatusObject]:
        """
        Assign or Unassign Agents to Supervisor

        Assign or unassign agents to the supervisor for an organization.

        Agents in a call queue can be associated with a supervisor who can silently monitor, coach, barge in or to take
        over calls that their assigned agents are currently handling.

        This operation requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param supervisor_id: Identifier of the supervisor to be updated.
        :type supervisor_id: str
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: list[PutPersonPlaceVirtualLineAgentObject]
        :param has_cx_essentials: Must be set to `true` to modify a supervisor with Customer Experience Essentials
            license. This can otherwise be ommited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Assign or unassign agents to a supervisor in this organization.
        :type org_id: str
        :rtype: list[ListSupervisorAgentStatusObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        body = dict()
        body['agents'] = TypeAdapter(list[PutPersonPlaceVirtualLineAgentObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'supervisors/{supervisor_id}')
        data = super().put(url, params=params, json=body)
        r = TypeAdapter(list[ListSupervisorAgentStatusObject]).validate_python(data['supervisorAgentStatus'])
        return r

    def list_available_agents(self, name: str = None, phone_number: str = None, order: str = None,
                              has_cx_essentials: bool = None, org_id: str = None,
                              **params) -> Generator[AvailableAgentListObject, None, None]:
        """
        List Available Agents

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
        :param has_cx_essentials: Returns only the list of available agents with Customer Experience Essentials
            license, when `true`. When ommited or set to `false`, will return the list of available agents with
            Customer Experience Basic license.
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
