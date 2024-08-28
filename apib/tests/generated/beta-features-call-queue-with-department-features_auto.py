from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AlternateNumbersWithPattern', 'BetaFeaturesCallQueueWithDepartmentFeaturesApi',
           'CallQueueQueueSettingsObject', 'CallQueueQueueSettingsObjectOverflow',
           'CallQueueQueueSettingsObjectOverflowAction', 'CallQueueQueueSettingsObjectOverflowGreeting',
           'GetCallQueueCallPolicyObject', 'GetCallQueueCallPolicyObjectCallBounce',
           'GetCallQueueCallPolicyObjectDistinctiveRing', 'GetCallQueueObject',
           'GetCallQueueObjectAlternateNumberSettings', 'GetCallQueueObjectDepartment', 'GetPersonPlaceObject',
           'HuntPolicySelection', 'ListCallQueueObject', 'ModifyCallQueueObjectDepartment', 'PostPersonPlaceObject',
           'RingPatternObject']


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
    #: example: True
    call_offer_tone_enabled: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[CallQueueQueueSettingsObjectOverflow] = None


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


class GetCallQueueCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    #: example: UNIFORM
    policy: Optional[HuntPolicySelection] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[GetCallQueueCallPolicyObjectCallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[GetCallQueueCallPolicyObjectDistinctiveRing] = None


class GetCallQueueObjectAlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for Alternate Number.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]] = None


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
    weight: Optional[str] = None


class BetaFeaturesCallQueueWithDepartmentFeaturesApi(ApiChild, base='telephony/config'):
    """
    Beta Features: Call Queue with Department Features
    
    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_call_queues(self, location_id: str = None, name: str = None, phone_number: str = None,
                                     department_id: str = None, department_name: str = None, org_id: str = None,
                                     **params) -> Generator[ListCallQueueObject, None, None]:
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

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param phone_number: Only return call queues with matching primary phone number or extension.
        :type phone_number: str
        :param department_id: Return only call queues with the matching departmentId.
        :type department_id: str
        :param department_name: Return only call queues with the matching departmentName.
        :type department_name: str
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
        if department_id is not None:
            params['departmentId'] = department_id
        if department_name is not None:
            params['departmentName'] = department_name
        url = self.ep('queues')
        return self.session.follow_pagination(url=url, model=ListCallQueueObject, item_key='queues', params=params)

    def get_details_for_a_call_queue(self, location_id: str, queue_id: str, org_id: str = None) -> GetCallQueueObject:
        """
        Get Details for a Call Queue

        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned anvinternal extension, which can be dialed
        internally to reach users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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

    def update_a_call_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsObject,
                            enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None,
                            last_name: str = None, time_zone: str = None, phone_number: str = None,
                            extension: str = None,
                            alternate_number_settings: GetCallQueueObjectAlternateNumberSettings = None,
                            call_policies: GetCallQueueCallPolicyObject = None,
                            allow_call_waiting_for_agents_enabled: bool = None,
                            agents: list[PostPersonPlaceObject] = None,
                            department: ModifyCallQueueObjectDepartment = None, org_id: str = None):
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

        Updating a call queue requires a full administrator auth token with a scope of
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
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone
            number if set, otherwise defaults to call group name.
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
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, including workspaces, that are eligible to receive calls.
        :type agents: list[PostPersonPlaceObject]
        :param department: Specifies the department information.
        :type department: ModifyCallQueueObjectDepartment
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
        body['queueSettings'] = queue_settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        if allow_call_waiting_for_agents_enabled is not None:
            body['allowCallWaitingForAgentsEnabled'] = allow_call_waiting_for_agents_enabled
        if agents is not None:
            body['agents'] = TypeAdapter(list[PostPersonPlaceObject]).dump_python(agents, mode='json', by_alias=True, exclude_none=True)
        if department is not None:
            body['department'] = department.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url, params=params, json=body)
