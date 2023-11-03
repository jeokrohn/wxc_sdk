from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersWithPattern', 'GetHuntGroupCallPolicyObject', 'GetHuntGroupCallPolicyObjectBusinessContinuity', 'GetHuntGroupCallPolicyObjectNoAnswer', 'GetHuntGroupObject', 'GetHuntGroupObjectDepartment', 'GetPersonPlaceObject', 'HuntPolicySelection', 'ListHuntGroupObject', 'ModifyHuntGroupObject', 'ModifyHuntGroupObjectDepartment', 'PostHuntGroupCallPolicyObject', 'PostHuntGroupCallPolicyObjectNoAnswer', 'PostPersonPlaceObject', 'ReadTheListOfHuntGroupsResponse', 'RingPatternObject']


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
    #: Ring pattern for when this alternate number is called. Only available when `distinctiveRing` is enabled for the hunt group.
    #: example: NORMAL
    ring_pattern: Optional[RingPatternObject] = None


class GetHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the nextAgentRings has occurred.
    #: example: True
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and nextAgentEnabled is true.
    #: example: 3.0
    next_agent_rings: Optional[int] = None
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Destination if forwardEnabled is True.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before forwarding calls if forwardEnabled is true.
    #: example: 15.0
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15.0
    system_max_number_of_rings: Optional[int] = None
    #: If destinationVoicemailEnabled is true, enables and disables sending incoming to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class GetHuntGroupCallPolicyObjectBusinessContinuity(ApiModel):
    #: Divert calls when unreachable, unanswered calls divert to a defined phone number. This could apply to phone calls that aren't answered due to a network outage, or all agents of the hunt group are busy and the Advance when the busy option is also enabled. For persons only using a mobile device, calls won't be diverted, if there is a network outage.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for Business Continuity.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


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


class GetHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: If false, then the option is treated as "Advance when busy": the hunt group won’t ring agents when they’re on a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is advanced to them, then the call will wait until that hunt group agent isn’t busy.
    #: example: True
    waiting_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[GetHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[GetHuntGroupCallPolicyObjectBusinessContinuity] = None


class GetHuntGroupObjectDepartment(ApiModel):
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
    first_name: Optional[str] = None
    #: First name of person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone number of person or workspace.
    #: example: +15555551234
    phone_number: Optional[str] = None
    #: Extension of person or workspace.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[datetime] = None


class GetHuntGroupObject(ApiModel):
    #: A unique identifier for the hunt group.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: 5558675309-Group
    name: Optional[str] = None
    #: Primary phone number of the hunt group.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Extension of the hunt group.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Whether or not the hunt group has the distinctive ring option enabled.
    #: example: True
    distinctive_ring: Optional[bool] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None
    #: Language for hunt group.
    #: example: English
    language: Optional[str] = None
    #: Language code for hunt group.
    #: example: en-US
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ".".
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to phone number if set, otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Time zone for the hunt group.
    #: example: America/Chicago
    time_zone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[GetHuntGroupCallPolicyObject] = None
    #: People, including workspaces, that are eligible to  receive calls.
    agents: Optional[list[GetPersonPlaceObject]] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[GetHuntGroupObjectDepartment] = None


class ListHuntGroupObject(ApiModel):
    #: A unique identifier for the hunt group.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: 5714328359
    name: Optional[str] = None
    #: Name of location for hunt group.
    #: example: WXCSIVDKCPAPIC4S1
    location_name: Optional[str] = None
    #: ID of location for hunt group.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    location_id: Optional[str] = None
    #: Primary phone number of the hunt group.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Primary phone extension of the hunt group.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[GetHuntGroupObjectDepartment] = None


class ModifyHuntGroupObjectDepartment(ApiModel):
    #: ID of department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class PostHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the nextAgentRings has occurred.
    #: example: True
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and nextAgentEnabled is true.
    #: example: 3.0
    next_agent_rings: Optional[int] = None
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Number of rings before forwarding calls if forwardEnabled is true.
    #: example: 15.0
    number_of_rings: Optional[int] = None
    #: Destination if forwardEnabled is True.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If forwardEnabled is true, enables and disables sending incoming to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class PostHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: If false, then the option is treated as "Advance when busy": the hunt group won’t ring agents when they’re on a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is advanced to them, then the call will wait until that hunt group agent isn’t busy.
    #: example: True
    waiting_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[PostHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[GetHuntGroupCallPolicyObjectBusinessContinuity] = None


class PostPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Weight of person or workspace. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[datetime] = None


class ModifyHuntGroupObject(ApiModel):
    #: Unique name for the hunt group.
    #: example: 5558675309-Group
    name: Optional[str] = None
    #: Primary phone number of the hunt group.
    #: example: 5558675309
    phone_number: Optional[str] = None
    #: Primary phone extension of the hunt group.
    #: example: 7781
    extension: Optional[datetime] = None
    #: Whether or not the hunt group has the distinctive ring option enabled.
    #: example: True
    distinctive_ring: Optional[bool] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None
    #: Language code.
    #: example: en-US
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ".".
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set, otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Time zone for the hunt group.
    #: example: America/Chicago
    time_zone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject] = None
    #: People, including workspaces, that are eligible to  receive calls.
    agents: Optional[list[PostPersonPlaceObject]] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Department the huntgroup is assigned to.
    department: Optional[ModifyHuntGroupObjectDepartment] = None


class ReadTheListOfHuntGroupsResponse(ApiModel):
    #: Array of hunt groups.
    hunt_groups: Optional[list[ListHuntGroupObject]] = None
