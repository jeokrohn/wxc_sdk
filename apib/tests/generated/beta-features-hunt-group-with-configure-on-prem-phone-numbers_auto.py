from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AddressAgentHuntGroupObject', 'AlternateNumbersWithPattern',
           'BetaFeaturesHuntGroupWithConfigureOnpremPhoneNumbersApi', 'GetHuntGroupCallPolicyObject',
           'GetHuntGroupCallPolicyObjectBusinessContinuity', 'GetHuntGroupCallPolicyObjectNoAnswer',
           'GetHuntGroupObject', 'GetPersonPlaceVirtualLineHuntGroupObject', 'HuntPolicySelection',
           'PostHuntGroupCallPolicyObject', 'PostHuntGroupCallPolicyObjectNoAnswer',
           'PostPersonPlaceVirtualLineHuntGroupObject', 'RingPatternObject']


class AddressAgentHuntGroupObject(ApiModel):
    #: numeric address for the Hunt Group agent.
    #: example: 1234567890
    address: Optional[str] = None


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
    #: example: True
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and `nextAgentEnabled` is true.
    #: example: 3
    next_agent_rings: Optional[int] = None
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Number of rings before forwarding calls if `forwardEnabled` is true.
    #: example: 15
    number_of_rings: Optional[int] = None
    #: Destination if `forwardEnabled` is True.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `forwardEnabled` is true, enables and disables sending incoming to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class GetHuntGroupCallPolicyObjectBusinessContinuity(ApiModel):
    #: Divert calls when unreachable, unanswered calls divert to a defined phone number. This could apply to phone
    #: calls that aren't answered due to a network outage, or all agents of the hunt group are busy and the Advance
    #: when the busy option is also enabled. For persons only using a mobile device, calls won't be diverted, if there
    #: is a network outage.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for Business Continuity.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if
    #: the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class PostHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: If false, then the option is treated as "Advance when busy": the hunt group won't ring agents when they're on a
    #: call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is
    #: advanced to them, then the call will wait until that hunt group agent isn't busy.
    #: example: True
    waiting_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[PostHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[GetHuntGroupCallPolicyObjectBusinessContinuity] = None


class PostPersonPlaceVirtualLineHuntGroupObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None


class GetHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the `nextAgentRings` has occurred.
    #: example: True
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and `nextAgentEnabled` is true.
    #: example: 3
    next_agent_rings: Optional[int] = None
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Destination if `forwardEnabled` is True.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before forwarding calls if `forwardEnabled` is true.
    #: example: 15
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
    system_max_number_of_rings: Optional[int] = None
    #: If destinationVoicemailEnabled is true, enables and disables sending incoming to destination number's voicemail
    #: if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class GetHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: If false, then the option is treated as "Advance when busy": the hunt group won't ring `agents` when they're on
    #: a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is
    #: advanced to them, then the call will wait until that hunt group agent isn't busy.
    #: example: True
    waiting_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[GetHuntGroupCallPolicyObjectNoAnswer] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[GetHuntGroupCallPolicyObjectBusinessContinuity] = None


class GetPersonPlaceVirtualLineHuntGroupObject(ApiModel):
    #: ID of person, workspace or virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE1NmE
    id: Optional[str] = None
    #: First name of person, workspace or virtual line.
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name of person, workspace or virtual line.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone number of person, workspace or virtual line.
    #: example: +15555551234
    phone_number: Optional[str] = None
    #: Extension of person, workspace or virtual line.
    #: example: 1234
    extension: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
    #: example: 50
    weight: Optional[str] = None


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
    extension: Optional[str] = None
    #: Whether or not the hunt group has the distinctive ring option enabled.
    #: example: True
    distinctive_ring: Optional[bool] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None
    #: Language for hunt group.
    #: example: English
    language: Optional[str] = None
    #: Language code for hunt group.
    #: example: en-US
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to `.`.
    #: example: Hakim
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to phone number if set,
    #: otherwise defaults to call group name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Time zone for the hunt group.
    #: example: America/Chicago
    time_zone: Optional[str] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[GetHuntGroupCallPolicyObject] = None
    #: Determines wether to use the Policy Server for this Hunt Group
    use_policy_server_enabled: Optional[bool] = None
    #: People, workspaces and virtual lines that are eligible to  receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineHuntGroupObject]] = None
    #: Numeric addresses of people, workspaces and virtual lines that are eligible to  receive calls.
    address_agents: Optional[list[AddressAgentHuntGroupObject]] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None


class BetaFeaturesHuntGroupWithConfigureOnpremPhoneNumbersApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features:  Hunt Group with Configure On-prem Phone Numbers
    
    Features: Hunt Group supports reading and writing of Webex Calling Hunt Group settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def create_a_hunt_group(self, location_id: str, name: str, call_policies: PostHuntGroupCallPolicyObject,
                            agents: list[PostPersonPlaceVirtualLineHuntGroupObject],
                            address_agents: list[AddressAgentHuntGroupObject], enabled: bool,
                            phone_number: str = None, extension: str = None, language_code: str = None,
                            first_name: str = None, last_name: str = None, time_zone: str = None,
                            use_hosted_agent_enabled: bool = None, use_policy_server_enabled: bool = None,
                            org_id: str = None) -> str:
        """
        Create a Hunt Group

        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Creating a hunt group requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param name: Unique name for the hunt group.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, workspaces and virtual lines that are eligible to  receive calls.
        :type agents: list[PostPersonPlaceVirtualLineHuntGroupObject]
        :param address_agents: People, workspaces and virtual lines that are eligible to  receive calls, on-prem.
        :type address_agents: list[AddressAgentHuntGroupObject]
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param phone_number: Primary phone number of the hunt group. Either phone number or extension are required.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group. Either phone number or extension are required.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to `.`.
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param use_hosted_agent_enabled: Determines whether hosted or numeric Hunt Group agents are used for this Hunt
            Group
        :type use_hosted_agent_enabled: bool
        :param use_policy_server_enabled: Determines wether to use the Policy Server for this Hunt Group
        :type use_policy_server_enabled: bool
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
        if use_hosted_agent_enabled is not None:
            body['useHostedAgentEnabled'] = use_hosted_agent_enabled
        if use_policy_server_enabled is not None:
            body['usePolicyServerEnabled'] = use_policy_server_enabled
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineHuntGroupObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        body['addressAgents'] = TypeAdapter(list[AddressAgentHuntGroupObject]).dump_python(address_agents, mode='json', by_alias=True, exclude_none=True)
        body['enabled'] = enabled
        url = self.ep(f'{location_id}/huntGroups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_details_for_a_hunt_group(self, location_id: str, hunt_group_id: str,
                                     org_id: str = None) -> GetHuntGroupObject:
        """
        Get Details for a Hunt Group

        Retrieve Hunt Group details.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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
        url = self.ep(f'{location_id}/huntGroups/{hunt_group_id}')
        data = super().get(url, params=params)
        r = GetHuntGroupObject.model_validate(data)
        return r

    def update_a_hunt_group(self, location_id: str, hunt_group_id: str,
                            agents: list[PostPersonPlaceVirtualLineHuntGroupObject],
                            address_agents: list[AddressAgentHuntGroupObject], name: str = None,
                            phone_number: str = None, extension: str = None, distinctive_ring: bool = None,
                            alternate_numbers: list[AlternateNumbersWithPattern] = None, language_code: str = None,
                            first_name: str = None, last_name: str = None, time_zone: str = None,
                            call_policies: PostHuntGroupCallPolicyObject = None,
                            use_policy_server_enabled: bool = None, enabled: bool = None, org_id: str = None):
        """
        Update a Hunt Group

        Update the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Updating a hunt group requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param hunt_group_id: Update settings for the hunt group with the matching ID.
        :type hunt_group_id: str
        :param agents: People, workspaces and virtual lines that are eligible to  receive calls.
        :type agents: list[PostPersonPlaceVirtualLineHuntGroupObject]
        :param address_agents: People, workspaces and virtual lines that are eligible to  receive calls, on-prem.
        :type address_agents: list[AddressAgentHuntGroupObject]
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
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param use_policy_server_enabled: Determines wether to use the Policy Server for this Hunt Group
        :type use_policy_server_enabled: bool
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param org_id: Update hunt group settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        if use_policy_server_enabled is not None:
            body['usePolicyServerEnabled'] = use_policy_server_enabled
        body['agents'] = TypeAdapter(list[PostPersonPlaceVirtualLineHuntGroupObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        body['addressAgents'] = TypeAdapter(list[AddressAgentHuntGroupObject]).dump_python(address_agents, mode='json', by_alias=True, exclude_none=True)
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'{location_id}/huntGroups/{hunt_group_id}')
        super().put(url, params=params, json=body)
