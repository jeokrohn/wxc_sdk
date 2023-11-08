from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersWithPattern', 'GetHuntGroupCallPolicyObject',
            'GetHuntGroupCallPolicyObjectBusinessContinuity', 'GetHuntGroupCallPolicyObjectNoAnswer',
            'GetHuntGroupObject', 'GetPersonPlaceVirtualLineHuntGroupObject', 'HuntPolicySelection',
            'ListHuntGroupObject', 'ReadTheListOfHuntGroupsResponse', 'RingPatternObject']


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


class GetHuntGroupCallPolicyObjectNoAnswer(ApiModel):
    #: If enabled, advance to next agent after the `nextAgentRings` has occurred.
    #: example: True
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and `nextAgentEnabled` is true.
    #: example: 3.0
    next_agent_rings: Optional[int] = None
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Destination if `forwardEnabled` is True.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before forwarding calls if `forwardEnabled` is true.
    #: example: 15.0
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15.0
    system_max_number_of_rings: Optional[int] = None
    #: If destinationVoicemailEnabled is true, enables and disables sending incoming to destination number's voicemail
    #: if the destination is an internal phone number and that number has the voicemail service enabled.
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
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341234
    esn: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is `WEIGHTED`.
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
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12347781
    esn: Optional[str] = None
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
    #: People, workspaces and virtual lines that are eligible to  receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineHuntGroupObject]] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None


class ListHuntGroupObject(ApiModel):
    #: A unique identifier for the hunt group.
    #: example: Y2lzY29zcGFyazovL3VzL0hVTlRfR1JPVVAvYUhaaFpUTjJNRzh5YjBBMk5EazBNVEk1Tnk1cGJuUXhNQzVpWTJ4a0xuZGxZbVY0TG1OdmJRPT0
    id: Optional[str] = None
    #: Unique name for the hunt group.
    #: example: 5714328359
    name: Optional[str] = None
    #: Name of the location for the hunt group.
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
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12347781
    esn: Optional[str] = None
    #: Whether or not the hunt group is enabled.
    #: example: True
    enabled: Optional[bool] = None


class ReadTheListOfHuntGroupsResponse(ApiModel):
    #: Array of hunt groups.
    hunt_groups: Optional[list[ListHuntGroupObject]] = None


class BetaFeaturesHuntGroupWithESNFeatureApi(ApiChild, base='telephony/config'):
    """
    Beta Features:  Hunt Group with ESN Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Hunt Group supports reading and writing of Webex Calling Hunt Group settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_hunt_groups(self, org_id: str = None, location_id: str = None, max_: int = None,
                                     start: int = None, name: str = None,
                                     phone_number: str = None) -> list[ListHuntGroupObject]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.
        
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.
        
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: List hunt groups for this organization.
        :type org_id: str
        :param location_id: Only return hunt groups with matching location ID.
        :type location_id: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return hunt groups with the matching name.
        :type name: str
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :type phone_number: str
        :rtype: list[ListHuntGroupObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('huntGroups')
        ...


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
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        ...

    ...