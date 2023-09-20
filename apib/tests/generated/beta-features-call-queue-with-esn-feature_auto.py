from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersWithPattern', 'CallQueueQueueSettingsObject', 'CallQueueQueueSettingsObjectComfortMessage', 'CallQueueQueueSettingsObjectComfortMessageBypass', 'CallQueueQueueSettingsObjectMohMessage', 'CallQueueQueueSettingsObjectMohMessageNormalSource', 'CallQueueQueueSettingsObjectOverflow', 'CallQueueQueueSettingsObjectOverflowAction', 'CallQueueQueueSettingsObjectOverflowGreeting', 'CallQueueQueueSettingsObjectWaitMessage', 'CallQueueQueueSettingsObjectWaitMessageWaitMode', 'CallQueueQueueSettingsObjectWelcomeMessage', 'GetCallQueueCallPolicyObject', 'GetCallQueueCallPolicyObjectCallBounce', 'GetCallQueueCallPolicyObjectDistinctiveRing', 'GetCallQueueObject', 'GetCallQueueObjectAlternateNumberSettings', 'GetPersonPlaceVirtualLineCallQueueObject', 'GetPersonPlaceVirtualLineCallQueueObjectType', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'ListCallQueueObject', 'RingPatternObject']


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
    phoneNumber: Optional[str] = None
    #: Ring pattern for when this alternate number is called. Only available when `distinctiveRing` is enabled for the hunt group.
    #: example: NORMAL
    ringPattern: Optional[RingPatternObject] = None


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
    #: When `true`, forwards all calls to a voicemail service of an internal number. This option is ignored when an external `transferNumber` is entered.
    sendToVoicemail: Optional[bool] = None
    #: Destination number for overflow calls when `action` is set to `TRANSFER_TO_PHONE_NUMBER`.
    #: example: +15555551212
    transferNumber: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is triggered.
    #: example: True
    overflowAfterWaitEnabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. The minimum value 0, The maximum value is 7200 seconds.
    #: example: 20.0
    overflowAfterWaitTime: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by a user.
    #: example: True
    playOverflowGreetingEnabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement `fileName` strings to be played as overflow greetings. These files are from the list of announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 `fileName` is mandatory, and the maximum is 4.
    #: example: ['[\"Greeting-1.wav\"]']
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObjectWelcomeMessage(ApiModel):
    #: If enabled play entrance message. The default value is `true`.
    #: example: True
    enabled: Optional[bool] = None
    #: Mandatory entrance message. The default value is `false`.
    alwaysEnabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement `fileName` strings to be played as `welcomeMessage` greetings. These files are from the list of announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 `fileName` is mandatory, and the maximum is 4.
    #: example: ['[\"Greeting-1.wav\"]']
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObjectWaitMessageWaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class CallQueueQueueSettingsObjectWaitMessage(ApiModel):
    #: If enabled play Wait Message.
    #: example: True
    enabled: Optional[bool] = None
    #: Estimated wait message operating mode. Supported values `TIME` and `POSITION`.
    #: example: POSITION
    waitMode: Optional[CallQueueQueueSettingsObjectWaitMessageWaitMode] = None
    #: The number of minutes for which the estimated wait is played. The minimum time is 10 minutes. The maximum time is 100 minutes.
    #: example: 100.0
    handlingTime: Optional[int] = None
    #: The default number of call handling minutes. The minimum time is 1 minutes, The maximum time is 100 minutes.
    #: example: 100.0
    defaultHandlingTime: Optional[int] = None
    #: The number of the position for which the estimated wait is played. The minimum positions are 10, The maximum positions are 100.
    #: example: 100.0
    queuePosition: Optional[int] = None
    #: Play time / Play position High Volume.
    highVolumeMessageEnabled: Optional[bool] = None
    #: The number of estimated waiting times in seconds. The minimum time is 10 seconds. The maximum time is 600 seconds.
    #: example: 600.0
    estimatedWaitingTime: Optional[int] = None
    #: Callback options enabled/disabled. Default value is false.
    callbackOptionEnabled: Optional[bool] = None
    #: The minimum estimated callback times in minutes. The default value is 30.
    #: example: 10.0
    minimumEstimatedCallbackTime: Optional[int] = None
    #: The international numbers for callback is enabled/disabled. The default value is `false`.
    internationalCallbackEnabled: Optional[bool] = None
    #: Play updated estimated wait message.
    #: example: true
    playUpdatedEstimatedWaitMessage: Optional[str] = None


class CallQueueQueueSettingsObjectComfortMessage(ApiModel):
    #: If enabled play periodic comfort message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time is 10 seconds.The maximum time is 600 seconds.
    #: example: 10.0
    timeBetweenMessages: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement `fileName` strings to be played as `comfortMessage` greetings. These files are from the list of announcement files associated with this call queue. These files are from the list of announcements files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 `fileName` is mandatory, and the maximum is 4.
    #: example: ['[\"Greeting-1.wav\"]']
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObjectComfortMessageBypass(ApiModel):
    #: If enabled play comfort bypass message.
    #: example: True
    enabled: Optional[bool] = None
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The minimum time is 1 seconds. The maximum time is 120 seconds.
    #: example: 10.0
    callWaitingAgeThreshold: Optional[int] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement `fileName` strings to be played as `comfortMessageBypass` greetings. These files are from the list of announcements files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 `fileName` is mandatory, and the maximum is 4.
    #: example: ['[\"Greeting-1.wav\"]']
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObjectMohMessageNormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement `fileName` strings to be played as `mohMessage` greetings. These files are from the list of announcement files associated with this call queue. For `CUSTOM` announcement, a minimum of 1 `fileName` is mandatory, and the maximum is 4.
    #: example: ['[\"Greeting-1.wav\"]']
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObjectMohMessage(ApiModel):
    normalSource: Optional[CallQueueQueueSettingsObjectMohMessageNormalSource] = None
    alternateSource: Optional[CallQueueQueueSettingsObjectMohMessageNormalSource] = None


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the `overflow` settings are triggered.
    #: example: 50.0
    queueSize: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    callOfferToneEnabled `true`: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    resetCallStatisticsEnabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsObjectOverflow] = None
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call queue while there is an available agent, the caller will not hear this announcement and is transferred to an agent. The welcome message feature is enabled by default.
    welcomeMessage: Optional[CallQueueQueueSettingsObjectWelcomeMessage] = None
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it plays after the welcome message and before the comfort message. By default, it is not enabled.
    waitMessage: Optional[CallQueueQueueSettingsObjectWaitMessage] = None
    #: Play a message after the welcome message and before hold music. This is typically a `CUSTOM` announcement that plays information, such as current promotions or information about products and services.
    comfortMessage: Optional[CallQueueQueueSettingsObjectComfortMessage] = None
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort message that abruptly ends when they are connected to an agent.
    comfortMessageBypass: Optional[CallQueueQueueSettingsObjectComfortMessageBypass] = None
    #: Play music after the comforting message in a repetitive loop.
    mohMessage: Optional[CallQueueQueueSettingsObjectMohMessage] = None
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces the identity of the call queue from which the call is coming.
    whisperMessage: Optional[CallQueueQueueSettingsObjectMohMessageNormalSource] = None


class GetCallQueueCallPolicyObjectCallBounce(ApiModel):
    #: If enabled, bounce calls after the set number of rings.
    #: example: True
    callBounceEnabled: Optional[bool] = None
    #: Number of rings after which to bounce call, if call bounce is enabled.
    #: example: 5.0
    callBounceMaxRings: Optional[int] = None
    #: Bounce if agent becomes unavailable.
    #: example: True
    agentUnavailableEnabled: Optional[bool] = None
    #: Alert agent if call on hold more than `alertAgentMaxSeconds`.
    #: example: True
    alertAgentEnabled: Optional[bool] = None
    #: Number of second after which to alert agent if `alertAgentEnabled`.
    #: example: 20.0
    alertAgentMaxSeconds: Optional[int] = None
    #: Bounce if call on hold more than `callBounceMaxSeconds`.
    #: example: True
    callBounceOnHoldEnabled: Optional[bool] = None
    #: Number of second after which to bounce if `callBounceEnabled`.
    #: example: 20.0
    callBounceOnHoldMaxSeconds: Optional[int] = None


class GetCallQueueCallPolicyObjectDistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Ring pattern for when this call queue is called. Only available when `distinctiveRing` is enabled for the call queue.
    #: example: NORMAL
    ringPattern: Optional[RingPatternObject] = None


class HuntRoutingTypeSelection(str, Enum):
    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based = 'PRIORITY_BASED'
    #: This option uses skill level as the criteria to route calls to agents. When there is more than one agent with the same skill level, the selected `policy` helps dispatch the calls to the agents.
    skill_based = 'SKILL_BASED'


class HuntPolicySelection(str, Enum):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next available agent. This is supported for `SKILL_BASED`.
    circular = 'CIRCULAR'
    #: Send the call through the queue of agents in order, starting from the top each time. This is supported for `SKILL_BASED`.
    regular = 'REGULAR'
    #: Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has been idle the second longest, and so on until the call is answered. This is supported for `SKILL_BASED`.
    uniform = 'UNIFORM'
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100%).
    weighted = 'WEIGHTED'


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents.
    #: example: PRIORITY_BASED
    routingType: Optional[HuntRoutingTypeSelection] = None
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    callBounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctiveRing: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns set for the Alternate Numbers.
    #: example: True
    distinctiveRingEnabled: Optional[bool] = None
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternateNumbers: Optional[list[AlternateNumbersWithPattern]] = None


class GetPersonPlaceVirtualLineCallQueueObjectType(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetPersonPlaceVirtualLineCallQueueObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[GetPersonPlaceVirtualLineCallQueueObjectType] = None
    #: First name of person, workspace or virtual line.
    #: example: Hakim
    firstName: Optional[str] = None
    #: First name of person, workspace or virtual line.
    #: example: Smith
    lastName: Optional[str] = None
    #: Phone number of person, workspace or virtual line.
    #: example: +12225555309
    phoneNumber: Optional[str] = None
    #: Extension of person, workspace or virtual line.
    #: example: 5309
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12345309
    esn: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[datetime] = None
    #: Skill level of person, workspace or virtual line. Only applied when the call `routingType` is `SKILL_BASED`.
    #: example: 1.0
    skillLevel: Optional[int] = None
    #: Indicates the join status of the agent for this queue. The default value while creating call queue is `true`.
    #: example: True
    joinEnabled: Optional[bool] = None


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
    languageCode: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to `.`.
    #: example: Hakim
    firstName: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the `phoneNumber` if set, otherwise defaults to call group name.
    #: example: Smith
    lastName: Optional[str] = None
    #: Time zone for the call queue.
    #: example: America/Chicago
    timeZone: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: +12225555309
    phoneNumber: Optional[str] = None
    #: Extension of the call queue.
    #: example: 5309
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12345309
    esn: Optional[str] = None
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    #: example: True
    phoneNumberForOutgoingCallsEnabled: Optional[bool] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternateNumberSettings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Policy controlling how calls are routed to `agents`.
    callPolicies: Optional[GetCallQueueCallPolicyObject] = None
    #: Overall call queue settings.
    queueSettings: Optional[CallQueueQueueSettingsObject] = None
    #: Flag to indicate whether call waiting is enabled for `agents`.
    allowCallWaitingForAgentsEnabled: Optional[bool] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallQueueObject]] = None
    #: Whether or not to allow agents to join or unjoin a queue.
    allowAgentJoinEnabled: Optional[bool] = None


class ListCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: 5714328359
    name: Optional[str] = None
    #: Name of location for call queue.
    #: example: WXCSIVDKCPAPIC4S1
    locationName: Optional[str] = None
    #: ID of location for call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    locationId: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: +12225555309
    phoneNumber: Optional[str] = None
    #: Primary phone extension of the call queue.
    #: example: 5309
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12345309
    esn: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
