from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional, List

from pydantic import Field

from .agents import CallQueueAgentsApi
from .announcement import AnnouncementApi
from .policies import CQPolicyApi
from ..forwarding import ForwardingApi, FeatureSelector
from ..hg_and_cq import HGandCQ, Policy, Agent
from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum
from ...common import RingPattern, Greeting, AnnAudioFile, IdAndName, UserNumber, UserType
from ...person_settings.available_numbers import AvailableNumber
from ...rest import RestSession

__all__ = ['CallBounce', 'DistinctiveRing', 'CallQueueCallPolicies', 'OverflowAction', 'OverflowSetting', 'WaitMode',
           'WaitMessageSetting', 'AudioSource', 'WelcomeMessageSetting', 'ComfortMessageSetting', 'MohMessageSetting',
           'ComfortMessageBypass', 'QueueSettings', 'CallQueue', 'CallQueueApi', 'CQRoutingType', 'AvailableAgent',
           'CallQueueSettings']


class CallBounce(ApiModel):
    """
    Settings for when the call into the call queue is not answered.
    """
    #: If enabled, bounce calls after the set number of rings.
    enabled: Optional[bool] = Field(alias='callBounceEnabled', default=None)
    #: Number of rings after which to bounce call, if call bounce is enabled.
    max_rings: Optional[int] = Field(alias='callBounceMaxRings', default=None)
    #: Bounce if agent becomes unavailable.
    agent_unavailable_enabled: Optional[bool] = None
    #: Alert agent if call on hold more than alert_agent_max_seconds.
    alert_agent_enabled: Optional[bool] = None
    #: Number of second after which to alert agent if alertAgentEnabled.
    alert_agent_max_seconds: Optional[int] = None
    #: Bounce if call on hold more than on_hold_max_seconds
    on_hold_enabled: Optional[bool] = Field(alias='callBounceOnHoldEnabled', default=None)
    #: Number of second after which to bounce if on_hold_enabled.
    on_hold_max_seconds: Optional[int] = Field(alias='callBounceOnHoldMaxSeconds', default=None)

    @staticmethod
    def default() -> 'CallBounce':
        return CallBounce(enabled=True,
                          max_rings=8,
                          agent_unavailable_enabled=False,
                          alert_agent_enabled=False,
                          alert_agent_max_seconds=30,
                          on_hold_enabled=False,
                          on_hold_max_seconds=60)


class DistinctiveRing(ApiModel):
    """
    Whether or not the call queue has the distinctive ring option enabled.
    """
    #: Whether or not the distinctive ring is enabled.
    enabled: bool
    #: Ring pattern for when this callqueue is called. Only available when distinctiveRing is enabled for the call
    #: queue.
    ring_pattern: Optional[RingPattern] = None

    @staticmethod
    def default() -> 'DistinctiveRing':
        """
        Default DistinctiveRing
        """
        return DistinctiveRing(enabled=True,
                               ring_pattern=RingPattern.normal)


class CQRoutingType(str, Enum):
    """
    Call routing type to use to dispatch calls to agents.
    """

    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based = 'PRIORITY_BASED'
    #: This option uses skill level as the criteria to route calls to agents. When there are more than one agent with
    #: same skill level, the selected routing policy helps dispatching the calls to the agents.
    skill_based = 'SKILL_BASED'


class CallQueueCallPolicies(ApiModel):
    """
    Policy controlling how calls are routed to agents.
    """
    #: Call routing type to use to dispatch calls to agents.
    routing_type: Optional[CQRoutingType] = None
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[Policy] = None
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[CallBounce] = None
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[DistinctiveRing] = None

    @staticmethod
    def default() -> 'CallQueueCallPolicies':
        """
        Default CallPolicies
        """
        return CallQueueCallPolicies(routing_type=CQRoutingType.priority_based,
                                     policy=Policy.circular,
                                     call_bounce=CallBounce.default(),
                                     distinctive_ring=DistinctiveRing.default())

    @staticmethod
    def simple() -> 'CallQueueCallPolicies':
        return CallQueueCallPolicies(routing_type=CQRoutingType.priority_based,
                                     policy=Policy.circular,
                                     call_bounce=CallBounce.default())


class OverflowAction(str, Enum):
    """
    How to handle new calls when the queue is full.
    """
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: Enter the number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'


class OverflowSetting(ApiModel):
    """
    Settings for incoming calls exceed queueSize.
    """
    #: How to handle new calls when the queue is full.
    action: Optional[OverflowAction] = None
    #: When true, forward all calls to a voicemail service of an internal number. This option is ignored when an
    #: external transfer_number is entered.
    send_to_voicemail: Optional[bool] = None
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str] = None
    #: True: transfer number is set
    is_transfer_number_set: Optional[bool] = None
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment
    #: is triggered.
    overflow_after_wait_enabled: Optional[bool] = None
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    overflow_after_wait_time: Optional[int] = None
    #: Indicate overflow audio to be played, otherwise callers will hear the hold music until the call is answered
    #: by a user.
    play_overflow_greeting_enabled: Optional[bool] = None
    #: How to handle new calls when the queue is full.
    greeting: Optional[Greeting] = None
    #: Array of announcement files to be played as overflow greetings. These files are from the list of announcement
    #: files associated with this call queue. For CUSTOM announcement, a minimum of 1 file is mandatory,
    #: and the maximum is 4.
    audio_announcement_files: Optional[list[AnnAudioFile]] = None

    @staticmethod
    def default() -> 'OverflowSetting':
        return OverflowSetting(action=OverflowAction.perform_busy_treatment,
                               send_to_voicemail=False,
                               is_transfer_number_set=False,
                               overflow_after_wait_enabled=False,
                               overflow_after_wait_time=30,
                               play_overflow_greeting_enabled=False,
                               greeting=Greeting.default,
                               audio_announcement_files=list())


class WaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class WaitMessageSetting(ApiModel):
    #: If enabled play Wait Message.
    enabled: Optional[bool] = None
    #: Estimated wait message operating mode. Supported values TIME and POSITION.
    wait_mode: Optional[WaitMode] = None
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
    #: The international numbers for callback is enabled/disabled. The default value is false.
    international_callback_enabled: Optional[bool] = None
    #: Play updated estimated wait message.
    play_updated_estimated_wait_message: Optional[bool] = None

    @staticmethod
    def default():
        return WaitMessageSetting(enabled=False,
                                  wait_mode=WaitMode.position,
                                  handling_time=100,
                                  queue_position=100,
                                  high_volume_message_enabled=False,
                                  default_handling_time=5)


class AudioSource(ApiModel):
    enabled: bool = Field(default=True)
    greeting: Greeting = Field(default=Greeting.default)
    audio_announcement_files: list[AnnAudioFile] = Field(default_factory=list)


class WelcomeMessageSetting(AudioSource):
    always_enabled: bool = Field(default=False)


class ComfortMessageSetting(AudioSource):
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    time_between_messages: int = Field(default=10)

    @staticmethod
    def default() -> 'ComfortMessageSetting':
        return ComfortMessageSetting(enabled=False)


class MohMessageSetting(ApiModel):
    normal_source: AudioSource
    alternate_source: AudioSource

    @staticmethod
    def default() -> 'MohMessageSetting':
        return MohMessageSetting(normal_source=AudioSource(enabled=True),
                                 alternate_source=AudioSource(enabled=False))


class ComfortMessageBypass(AudioSource):
    """
    Comfort message bypass settings
    """
    call_waiting_age_threshold: int = Field(default=30)
    play_announcement_after_ringing: bool = Field(default=False)
    ring_time_before_playing_announcement: int = Field(default=10)


class QueueSettings(ApiModel):
    """
    Overall call queue settings.
    """
    #: maximum number of calls for this call queue. Once this number is reached, the overflow settings are triggered
    # (max 50).
    queue_size: int
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool] = None
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool] = None
    #: Settings for incoming calls exceed queue_size.
    overflow: Optional[OverflowSetting] = None
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[WaitMessageSetting] = None
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the
    #: call queue while there is an available agent, the caller will not hear this announcement and is transferred to
    #: an agent. The welcome message feature is enabled by default.
    welcome_message: Optional[WelcomeMessageSetting] = None
    #: Play a message after the welcome message and before hold music. This is typically a CUSTOM announcement that
    #:  plays information, such as current promotions or information about products and services.
    comfort_message: Optional[ComfortMessageSetting] = None
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[MohMessageSetting] = None
    #: Comfort message bypass settings
    comfort_message_bypass: Optional[ComfortMessageBypass] = None
    #: whisper message to identify the queue for incoming calls.
    whisper_message: Optional[AudioSource] = None
    use_enterprise_play_tone_to_agent_settings_enabled: Optional[bool] = None
    play_tone_to_agent_for_barge_in_enabled: Optional[bool] = None
    play_tone_to_agent_for_silent_monitoring_enabled: Optional[bool] = None
    play_tone_to_agent_for_supervisor_coaching_enabled: Optional[bool] = None

    @staticmethod
    def default(*, queue_size: int) -> 'QueueSettings':
        """
        Simple queue settings

        :param queue_size: queue size
        :type queue_size: int
        """
        return QueueSettings(queue_size=queue_size,
                             overflow=OverflowSetting.default())


class CallQueue(HGandCQ):
    """
    Call queue details
    """
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[CallQueueCallPolicies] = None
    #: Overall call queue settings.
    queue_settings: Optional[QueueSettings] = None
    #: whether ot not call waiting for agents is enabled
    allow_call_waiting_for_agents_enabled: Optional[bool] = None
    #: Whether or not to allow agents to join or unjoin a queue
    allow_agent_join_enabled: Optional[bool] = None
    #: Allow queue phone number for outgoing calls
    phone_number_for_outgoing_calls_enabled: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[IdAndName] = None
    #: Denotes if the call queue has Customer Experience Essentials license.
    has_cx_essentials: Optional[bool] = None

    @staticmethod
    def exclude_update_or_create() -> dict:
        """
        Exclude dict for update or create calls
        :return: dict

        :meta private:
        """
        base_exclude = HGandCQ.exclude_update_or_create()
        base_exclude.update({'queue_settings':
                                 {'overflow':
                                      {'is_transfer_number_set': True}},
                             'department': {'name': True},
                             'has_cx_essentials': True})
        return base_exclude

    @staticmethod
    def create(*, name: str,
               agents: list[Agent],
               queue_size: int = None,
               enabled: bool = None,
               language_code: str = None,
               first_name: str = None,
               last_name: str = None,
               time_zone: str = None,
               phone_number: str = None,
               extension: str = None,
               department_id: str = None,
               has_cx_essentials: bool = None,
               call_policies: CallQueueCallPolicies = None,
               queue_settings: QueueSettings = None,
               allow_call_waiting_for_agents_enabled: bool = None,
               allow_agent_join_enabled: bool = None,
               phone_number_for_outgoing_calls_enabled: bool = None) -> 'CallQueue':
        """
        Get an instance which can be uses for a create() call. Allows simplified creation of default queue settings
        based on queue_size

        :param name:
        :param agents:
        :param queue_size:
        :param enabled:
        :param language_code:
        :param first_name:
        :param last_name:
        :param time_zone:
        :param phone_number:
        :param extension:
        :param department_id:
        :param has_cx_essentials:
        :param call_policies:
        :param queue_settings:
        :param allow_call_waiting_for_agents_enabled:
        :param allow_agent_join_enabled:
        :param phone_number_for_outgoing_calls_enabled:
        :return:
        """
        if not (queue_size or queue_settings):
            raise ValueError('One of queue_size and queue_settings has to be given')
        if queue_size and queue_settings:
            raise ValueError('Only one of queue_size and queue_settings can be given')
        if not (phone_number or extension):
            raise ValueError('One of phone_number and extension has to be given')
        if queue_size:
            queue_settings = QueueSettings(queue_size=queue_size)
        call_policies = call_policies or CallQueueCallPolicies.default()
        params = {k: v for k, v in locals().items()
                  if v is not None and k != 'queue_size'}
        if department_id:
            params.pop('department_id')
            params['department'] = {'id': department_id}

        return CallQueue(**params)


class CallQueueSettings(ApiModel):
    #: Modify the optimized simultaneous ring algorithm setting.
    maintain_queue_position_for_sim_ring_enabled: Optional[bool] = None
    #: Enable this setting to change the status of an agent to unavailable in case of bounced calls.
    force_agent_unavailable_on_bounced_enabled: Optional[bool] = None
    play_tone_to_agent_for_barge_in_enabled: Optional[bool] = None
    play_tone_to_agent_for_silent_monitoring_enabled: Optional[bool] = None
    play_tone_to_agent_for_supervisor_coaching_enabled: Optional[bool] = None


class AvailableAgent(ApiModel):
    #: ID of a person, workspace or virtual line.
    id: Optional[str] = None
    #: Last name of a person, workspace or virtual line.
    last_name: Optional[str] = None
    #: First name of a person, workspace or virtual line.
    first_name: Optional[str] = None
    #: Display name of a person, workspace or virtual line.
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[UserType] = None
    #: Email of a person, workspace or virtual line.
    email: Optional[str] = None
    #: Person has the CX Essentials license.
    has_cx_essentials: Optional[bool] = None
    #: List of phone numbers of a person, workspace or virtual line.
    phone_numbers: Optional[list[UserNumber]] = None


@dataclass(init=False, repr=False)
class CallQueueApi(ApiChild, base=''):
    """
    Features:  Call Queue

    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.

    Supervisors are users who manage agents and who perform functions including monitoring, coaching, and more.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope
    of `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """
    agents: CallQueueAgentsApi
    forwarding: ForwardingApi
    announcement: AnnouncementApi
    policy: CQPolicyApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.agents = CallQueueAgentsApi(session=session)
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.queues)
        self.announcement = AnnouncementApi(session=session)
        self.policy = CQPolicyApi(session=session)

    def _endpoint(self, *, location_id: str = None, queue_id: str = None, path: str = None):
        """
        Helper to get URL for API endpoints

        :meta private:
        :param location_id:
        :param queue_id:
        :return:
        """
        if location_id is None:
            return self.ep('telephony/config/queues')
        else:
            ep = self.ep(f'telephony/config/locations/{location_id}/queues')
            if queue_id:
                ep = f'{ep}/{queue_id}'
            if path:
                ep = f'{ep}/{path}'
            return ep

    @staticmethod
    def update_or_create(*, queue: CallQueue) -> str:
        """
        Get JSON for update or create

        :meta private:
        :param queue:
        :return:
        """
        return queue.model_dump_json(
            exclude={'id': True,
                     'location_name': True,
                     'location_id': True,
                     'toll_free_number': True,
                     'language': True,
                     'agents':
                         {'__all__':
                              {'first_name': True,
                               'last_name': True,
                               'user_type': True,
                               'extension': True,
                               'phone_number': True}},
                     'alternate_number_settings':
                         {'alternate_numbers':
                              {'__all__':
                                   {'toll_free_number': True}}},
                     'queue_settings':
                         {'overflow':
                              {'is_transfer_number_set': True}}})

    def list(self, location_id: str = None, name: str = None, phone_number: str = None,
             department_id: str = None, department_name: str = None,
             has_cx_essentials: bool = None, org_id: str = None,
             **params) -> Generator[CallQueue, None, None]:
        """
        Read the List of Call Queues

        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud, when all agents
        assigned to receive calls from the queue are unavailable. Queued calls are routed to
        an available agent, when not on an active call. Each call queue is assigned a lead number, which is a telephone
        number that external callers can dial to reach the users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach the users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

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
        :return: yields :class:`CallQueue` objects
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
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallQueue, params=params)

    def by_name(self, name: str, location_id: str = None, has_cx_essentials: bool = None,
                org_id: str = None) -> Optional[CallQueue]:
        """
        Get queue info by name

        :param location_id:
        :param has_cx_essentials:
        :param name:
        :param org_id:
        :return:
        """
        return next((cq for cq in self.list(location_id=location_id, has_cx_essentials=has_cx_essentials,
                                            org_id=org_id, name=name)
                     if cq.name == name), None)

    def create(self, location_id: str, settings: CallQueue, has_cx_essentials: bool = None,
               org_id: str = None) -> str:
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

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param settings: parameters for queue creation.
        :type settings: :class:`CallQueue`
        :param has_cx_essentials: Creates a Customer Experience Essentials call queue, when `true`. This requires
            Customer Experience Essentials licensed agents. If this parameter is not set, the `has_cx_essentials`
            attribute of the `settings` object is considered.
        :type has_cx_essentials: bool
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :return: queue id
        :rtype: str

        Example:

            .. code-block:: python

                settings = CallQueue(name=new_name,
                                     extension=extension,
                                     call_policies=CallQueueCallPolicies.default(),
                                     queue_settings=QueueSettings.default(queue_size=10),
                                     agents=[Agent(agent_id=user.person_id) for user in members])

                # create new queue
                queue_id = api.telephony.callqueue.create(location_id=target_location.location_id,
                                                          settings=settings)

        """
        params = org_id and {'orgId': org_id} or {}
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        elif settings.has_cx_essentials:
            params['hasCxEssentials'] = 'true'
        cq_data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = self.post(url, json=cq_data, params=params)
        return data['id']

    def delete_queue(self, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete a Call Queue
        Delete the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Deleting a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url=url, params=params)

    def details(self, location_id: str, queue_id: str, has_cx_essentials: bool = None,
                org_id: str = None) -> CallQueue:
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
            Essentials license. This can otherwise be omited or set to `false`.
        :type has_cx_essentials: bool
        :param org_id: Retrieves the details of a call queue in this organization.
        :type org_id: str
        :return: call queue details
        :rtype: :class:`CallQueue`
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        data = self.get(url, params=params)
        result = CallQueue.model_validate(data)
        result.location_id = location_id
        # noinspection PyTypeChecker
        return result

    def update(self, location_id: str, queue_id: str, update: CallQueue, org_id: str = None):
        """
        Update a Call Queue

        Update the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Updating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: updates
        :type update: :class:`CallQueue`
        :param org_id: Update call queue settings from this organization.

        Examples:

        .. code-block::

            api = WebexSimpleApi()

            # shortcut
            cq = api.telephony.callqueue

            # disable a call queue
            update = CallQueue(enabled=False)
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

            # set the call routing policy to SIMULTANEOUS
            update = CallQueue(call_policies=CallPolicies(policy=Policy.simultaneous))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)
            # don't bounce calls after the set number of rings.
            update = CallQueue(
                call_policies=CallPolicies(
                    call_bounce=CallBounce(
                        enabled=False)))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

        Alternatively you can also read call queue details, update them in place and then call update().

        .. code-block::

            details = cq.details(location_id=...,
                                 queue_id=...)
            details.call_policies.call_bounce.agent_unavailable_enabled=False
            details.call_policies.call_bounce.on_hold_enabled=False
            cq.update(location_id=...,
                      queue_id=...,
                      update=details)

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None or queue_id is None:
            raise ValueError('location_id and queue_id cannot be None')
        cq_data = update.create_or_update()
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        self.put(url=url, json=cq_data, params=params)

    def get_call_queue_settings(self, org_id: str = None) -> CallQueueSettings:
        """
        Get Call Queue Settings

        Retrieve Call Queue Settings for a specific organization.

        Call Queue Settings are used to enable the Simultaneous Ringing algorithm that maintains queue positions for
        customers.

        Retrieving Call Queue Settings requires a full, user, or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param org_id: Call Queue Settings for this organization.
        :type org_id: str
        :rtype: :class:`CallQueueSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/queues/settings')
        data = self.get(url, params=params)
        r = CallQueueSettings.model_validate(data)
        return r

    def update_call_queue_settings(self, settings: CallQueueSettings, org_id: str = None):
        """
        Update Call Queue Settings

        Update Call Queue Settings for a specific organization.

        Call Queue Settings are used to enable the Simultaneous Ringing algorithm that maintains queue positions for
        customers.

        Updating Call Queue Settings requires a full or user administrator auth token with a scope
        `spark-admin:telephony_config_write`.

        :param settings: Call Queue Settings for this organization.
        :param org_id: update Call Queue Settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('telephony/config/queues/settings')
        self.put(url, params=params, json=body)

    def primary_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                        org_id: str = None,
                                        **params) -> Generator[AvailableNumber, None, None]:
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
        url = self._endpoint(location_id=location_id, path='availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def alternate_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                          org_id: str = None,
                                          **params) -> Generator[AvailableNumber, None, None]:
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
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def call_forward_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                             owner_name: str = None, extension: str = None,
                                             org_id: str = None,
                                             **params) -> Generator[AvailableNumber, None, None]:
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
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self._endpoint(location_id=location_id, path='callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def available_agents(self, location_id: str, name: str = None, phone_number: str = None,
                                        order: str = None, org_id: str = None,
                                        **params) -> Generator[AvailableAgent, None, None]:
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
        url = self.ep('telephony/config/queues/agents/availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgent, item_key='agents', params=params)
