from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from .announcement import AnnouncementApi
from .policies import CQPolicyApi
from ..forwarding import ForwardingApi, FeatureSelector
from ..hg_and_cq import HGandCQ, Policy, Agent
from ...base import SafeEnum as Enum
from ...base import to_camel, ApiModel
from ...common import RingPattern, Greeting
from ...rest import RestSession

__all__ = ['CallBounce', 'DistinctiveRing', 'CallQueueCallPolicies', 'OverflowAction', 'OverflowSetting', 'WaitMode',
           'WaitMessageSetting', 'AudioSource', 'WelcomeMessageSetting', 'ComfortMessageSetting', 'MohMessageSetting',
           'ComfortMessageBypass', 'QueueSettings', 'CallQueue', 'CallQueueApi', 'CQRoutingType']


class CallBounce(ApiModel):
    """
    Settings for when the call into the call queue is not answered.
    """
    #: If enabled, bounce calls after the set number of rings.
    enabled: Optional[bool] = Field(alias='callBounceEnabled')
    #: Number of rings after which to bounce call, if call bounce is enabled.
    max_rings: Optional[int] = Field(alias='callBounceMaxRings')
    #: Bounce if agent becomes unavailable.
    agent_unavailable_enabled: Optional[bool]
    #: Alert agent if call on hold more than alert_agent_max_seconds.
    alert_agent_enabled: Optional[bool]
    #: Number of second after which to alert agent if alertAgentEnabled.
    alert_agent_max_seconds: Optional[int]
    #: Bounce if call on hold more than on_hold_max_seconds
    on_hold_enabled: Optional[bool] = Field(alias='callBounceOnHoldEnabled')
    #: Number of second after which to bounce if on_hold_enabled.
    on_hold_max_seconds: Optional[int] = Field(alias='callBounceOnHoldMaxSeconds')

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
    ring_pattern: Optional[RingPattern]

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
    routing_type: Optional[CQRoutingType]
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[Policy]
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[DistinctiveRing]

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
    action: Optional[OverflowAction]
    #: When true, forward all calls to a voicemail service of an internal number. This option is ignored when an
    #: external transfer_number is entered.
    send_to_voicemail: Optional[bool]
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str]
    #: True: transfer number is set
    is_transfer_number_set: Optional[bool]
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment
    #: is triggered.
    overflow_after_wait_enabled: Optional[bool]
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    overflow_after_wait_time: Optional[int]
    #: Indicate overflow audio to be played, otherwise callers will hear the hold music until the call is answered
    #: by a user.
    play_overflow_greeting_enabled: Optional[bool]
    #: How to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement file name strings to be played as overflow greetings. These files must be from the list
    #: of announcements files associated with this call queue.
    audio_files: Optional[list[str]]

    @staticmethod
    def default() -> 'OverflowSetting':
        return OverflowSetting(action=OverflowAction.perform_busy_treatment,
                               send_to_voicemail=False,
                               is_transfer_number_set=False,
                               overflow_after_wait_enabled=False,
                               overflow_after_wait_time=30,
                               play_overflow_greeting_enabled=False,
                               greeting=Greeting.default,
                               audio_files=list())


class WaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class WaitMessageSetting(ApiModel):
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
    audio_files: list[str] = Field(default_factory=list)


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
    call_offer_tone_enabled: Optional[bool]
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool]
    #: Settings for incoming calls exceed queue_size.
    overflow: Optional[OverflowSetting]
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[WaitMessageSetting]
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the
    #: call queue while there is an available agent, the caller will not hear this announcement and is transferred to
    #: an agent. The welcome message feature is enabled by default.
    welcome_message: Optional[WelcomeMessageSetting]
    #: Play a message after the welcome message and before hold music. This is typically a CUSTOM announcement that
    #:  plays information, such as current promotions or information about products and services.
    comfort_message: Optional[ComfortMessageSetting]
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[MohMessageSetting]
    #: Comfort message bypass settings
    comfort_message_bypass: Optional[ComfortMessageBypass]
    #: whisper message to identify the queue for incoming calls.
    whisper_message: Optional[AudioSource]

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
    call_policies: Optional[CallQueueCallPolicies]
    #: Overall call queue settings.
    queue_settings: Optional[QueueSettings]
    #: whether ot not call waiting for agents is enabled
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: Whether or not to allow agents to join or unjoin a queue
    allow_agent_join_enabled: Optional[bool]
    #: Allow queue phone number for outgoing calls
    phone_number_for_outgoing_calls_enabled: Optional[bool]

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
                                      {'is_transfer_number_set': True}}})
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
        params = {k: v for k, v in locals().items()
                  if v is not None and k != 'queue_size'}
        return CallQueue(**params)


@dataclass(init=False)
class CallQueueApi:
    """
    Call Queue APÍ
    """
    forwarding: ForwardingApi
    announcement: AnnouncementApi
    policy: CQPolicyApi

    def __init__(self, session: RestSession):
        self._session = session
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.queues)
        self.announcement = AnnouncementApi(session=session)
        self.policy = CQPolicyApi(session=session)

    def _endpoint(self, *, location_id: str = None, queue_id: str = None):
        """
        Helper to get URL for API endpoints

        :meta private:
        :param location_id:
        :param queue_id:
        :return:
        """
        if location_id is None:
            return self._session.ep('telephony/config/queues')
        else:
            ep = self._session.ep(f'telephony/config/locations/{location_id}/queues')
            if queue_id:
                ep = f'{ep}/{queue_id}'
            return ep

    @staticmethod
    def update_or_create(*, queue: CallQueue) -> str:
        """
        Get JSON for update or create

        :param queue:
        :return:
        :meta private:
        """
        return queue.json(
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

    def list(self, location_id: str = None, name: str = None,
             org_id: str = None, **params) -> Generator[CallQueue, None, None]:
        """
        Read the List of Call Queues
        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param org_id: List call queues for this organization
        :type org_id: str
        :param params: dict of additional parameters passed directly to endpoint
        :type params: dict
        :return: yields :class:`CallQueue` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=CallQueue, params=params)

    def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[CallQueue]:
        """
        Get queue info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((cq for cq in self.list(location_id=location_id, org_id=org_id, name=name)
                     if cq.name == name), None)

    def create(self, location_id: str, settings: CallQueue, org_id: str = None) -> str:
        """
        Create a Call Queue
        Create new Call Queues for the given location.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Creating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param settings: parameters for queue creation.
        :type settings: :class:`CallQueue`
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
        cq_data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = self._session.rest_post(url, data=cq_data, params=params)
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
        self._session.rest_delete(url=url, params=params)

    def details(self, location_id: str, queue_id: str, org_id: str = None) -> CallQueue:
        """
        Get Details for a Call Queue
        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned anvinternal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :return: call queue details
        :rtype: :class:`CallQueue`
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = {'orgId': org_id} if org_id is not None else {}
        data = self._session.rest_get(url, params=params)
        result = CallQueue.parse_obj(data)
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
        self._session.rest_put(url=url, data=cq_data, params=params)
