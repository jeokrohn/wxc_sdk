from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersWithPattern', 'CallQueueQueueSettingsObject', 'CallQueueQueueSettingsObjectOverflow', 'CallQueueQueueSettingsObjectOverflowAction', 'CallQueueQueueSettingsObjectOverflowGreeting', 'GetCallQueueCallPolicyObject', 'GetCallQueueCallPolicyObjectCallBounce', 'GetCallQueueCallPolicyObjectDistinctiveRing', 'GetCallQueueObject', 'GetCallQueueObjectAlternateNumberSettings', 'GetCallQueueObjectDepartment', 'GetPersonPlaceObject', 'HuntPolicySelection', 'ListCallQueueObject', 'ModifyCallQueueObject', 'ModifyCallQueueObjectDepartment', 'PostPersonPlaceObject', 'RingPatternObject']


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
    #: example: +15553331212
    transferNumber: Optional[str] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is triggered.
    #: example: True
    overflowAfterWaitEnabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    #: example: 20.0
    overflowAfterWaitTime: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise callers will hear the hold music until the call is answered by a user.
    #: example: True
    playOverflowGreetingEnabled: Optional[bool] = None
    #: Indicates how to handle new calls when the queue is full.
    #: example: DEFAULT
    greeting: Optional[CallQueueQueueSettingsObjectOverflowGreeting] = None
    #: Array of announcement file name strings to be played as overflow greetings. These files are from the list of announcements files associated with this call queue.
    audioFiles: Optional[list[str]] = None


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are triggered.
    #: example: 50.0
    queueSize: Optional[int] = None
    #: Play ringing tone to callers when their call is set to an available agent.
    callOfferToneEnabled `true`: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    resetCallStatisticsEnabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsObjectOverflow] = None


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
    #: Alert agent if call on hold more than alertAgentMaxSeconds.
    #: example: True
    alertAgentEnabled: Optional[bool] = None
    #: Number of second after which to alert agent if alertAgentEnabled.
    #: example: 20.0
    alertAgentMaxSeconds: Optional[int] = None
    #: Bounce if call on hold more than callBounceMaxSeconds.
    #: example: True
    callBounceOnHoldEnabled: Optional[bool] = None
    #: Number of second after which to bounce if callBounceEnabled.
    #: example: 20.0
    callBounceOnHoldMaxSeconds: Optional[int] = None


class GetCallQueueCallPolicyObjectDistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Ring pattern for when this callqueue is called. Only available when `distinctiveRing` is enabled for the call queue.
    #: example: NORMAL
    ringPattern: Optional[RingPatternObject] = None


class HuntPolicySelection(str, Enum):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next available agent.
    circular = 'CIRCULAR'
    #: Send the call through the queue of agents in order, starting from the top each time.
    regular = 'REGULAR'
    #: Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has been idle the second longest, and so on until the call is answered.
    uniform = 'UNIFORM'
    #: Sends call to idle agents based on percentages you assign to each agent (up to 100%).
    weighted = 'WEIGHTED'


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    callBounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctiveRing: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns set for Alternate Number.
    #: example: True
    distinctiveRingEnabled: Optional[bool] = None
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternateNumbers: Optional[list[AlternateNumbersWithPattern]] = None


class GetCallQueueObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class GetPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: Hakim
    firstName: Optional[str] = None
    #: First name of person or workspace.
    #: example: Smith
    lastName: Optional[str] = None
    #: Phone number of person or workspace.
    #: example: +15555551234
    phoneNumber: Optional[str] = None
    #: Extension of person or workspace.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[datetime] = None


class GetCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvNTU1MzY4Y2QtZDg5Mi00YzFlLTk0YjYtNzdjNjRiYWQ3NWMx
    id: Optional[str] = None
    #: Unique name for the call queue.
    #: example: CallQueue-1
    name: Optional[str] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    #: example: Hakim
    firstName: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
    #: example: Smith
    lastName: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: 5558675309
    phoneNumber: Optional[str] = None
    #: Extension of the call queue.
    #: example: 7781
    extension: Optional[datetime] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternateNumberSettings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Language for call queue.
    #: example: English
    language: Optional[str] = None
    #: Language code for call queue.
    #: example: en-US
    languageCode: Optional[str] = None
    #: Time zone for the call queue.
    #: example: America/Chicago
    timeZone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    callPolicies: Optional[GetCallQueueCallPolicyObject] = None
    #: Overall call queue settings.
    queueSettings: Optional[CallQueueQueueSettingsObject] = None
    #: Flag to indicate whether call waiting is enabled for agents.
    allowCallWaitingForAgentsEnabled: Optional[bool] = None
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceObject]] = None
    #: Specifies the department information.
    department: Optional[GetCallQueueObjectDepartment] = None


class ListCallQueueObject(ApiModel):
    #: A unique identifier for the call queue.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvNTU1MzY4Y2QtZDg5Mi00YzFlLTk0YjYtNzdjNjRiYWQ3NWMx
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
    #: example: 5558675309
    phoneNumber: Optional[str] = None
    #: Primary phone extension of the call queue.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[GetCallQueueObjectDepartment] = None


class ModifyCallQueueObjectDepartment(ApiModel):
    #: Unique identifier of the department.  Set to null to remove entity from department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class PostPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[datetime] = None


class ModifyCallQueueObject(ApiModel):
    #: Whether or not the call queue is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Unique name for the call queue.
    #: example: CallQueue-1
    name: Optional[str] = None
    #: Language code.
    #: example: en-US
    languageCode: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    #: example: Hakim
    firstName: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
    #: example: Smith
    lastName: Optional[str] = None
    #: Time zone for the hunt group.
    #: example: America/Chicago
    timeZone: Optional[str] = None
    #: Primary phone number of the call queue.
    #: example: 5558675309
    phoneNumber: Optional[str] = None
    #: Extension of the call queue.
    #: example: 7781
    extension: Optional[datetime] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternateNumberSettings: Optional[GetCallQueueObjectAlternateNumberSettings] = None
    #: Policy controlling how calls are routed to agents.
    callPolicies: Optional[GetCallQueueCallPolicyObject] = None
    #: Overall call queue settings.
    queueSettings: Optional[CallQueueQueueSettingsObject] = None
    #: Flag to indicate whether call waiting is enabled for agents.
    allowCallWaitingForAgentsEnabled: Optional[bool] = None
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceObject]] = None
    #: Specifies the department information.
    department: Optional[ModifyCallQueueObjectDepartment] = None
