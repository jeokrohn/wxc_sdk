from enum import Enum
from typing import List, Optional

from pydantic import Field

from .announcement import AnnouncementAPI
from ..hg_and_cq import HGandCQ, AlternateNumber, Policy, Agent, RingPattern, AlternateNumberSettings, ForwardingAPI, \
    FeatureSelector
from collections.abc import Generator
from ...rest import RestSession
from ...base import to_camel, ApiModel

__all__ = ['CallQueueAPI', 'CallQueue', 'CallQueueDetail',
           'AlternateNumber', 'AlternateNumberSettings', 'CallBounce', 'DistinctiveRing', 'Policy',
           'CallPolicies', 'OverflowSetting', 'WaitMessageSetting', 'WelcomeMessageSetting', 'AudioSource',
           'ComfortMessageSetting', 'MohMessageSetting', 'QueueSettings', 'Agent']


class CallQueue(HGandCQ):
    """
    A Call Queue object
    """
    pass


class CallBounce(ApiModel):
    """
    Call bounce settings
    """
    enabled: bool = Field(alias='callBounceEnabled')
    max_rings: Optional[int] = Field(alias='callBounceMaxRings')
    agent_unavailable_enabled: bool
    alert_agent_enabled: Optional[bool]
    alert_agent_max_seconds: Optional[int]
    on_hold_enabled: bool = Field(alias='callBounceOnHoldEnabled')
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
    Distinctive ring settings
    """
    enabled: Optional[bool]
    ring_pattern: Optional[RingPattern]

    @staticmethod
    def default() -> 'DistinctiveRing':
        return DistinctiveRing(enabled=True,
                               ring_pattern=RingPattern.normal)


class CallPolicies(ApiModel):
    """
    Policy controlling how calls are routed to agents.
    """
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[Policy]
    #: Settings for when the call into the call queue is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[DistinctiveRing]

    @staticmethod
    def default() -> 'CallPolicies':
        return CallPolicies(policy=Policy.circular,
                            call_bounce=CallBounce.default(),
                            distinctive_ring=DistinctiveRing.default())

    @staticmethod
    def simple() -> 'CallPolicies':
        return CallPolicies(policy=Policy.circular)


class OverflowAction(str, Enum):
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'

class Greeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'

class OverflowSetting(ApiModel):
    action: Optional[OverflowAction]
    send_to_voicemail: Optional[bool]
    transfer_number: Optional[str]
    is_transfer_number_set: Optional[bool]
    overflow_after_wait_enabled: Optional[bool]
    overflow_after_wait_time: Optional[int]
    play_overflow_greeting_enabled: Optional[bool]
    greeting: Optional[Greeting]
    audio_files: Optional[List[str]]

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
    time = 'TIME'
    position = 'POSITION'


class WaitMessageSetting(ApiModel):
    enabled: Optional[bool]
    wait_mode: Optional[WaitMode]
    handling_time: Optional[int]
    queue_position: Optional[int]
    high_volume_message_enabled: Optional[bool]
    default_handling_time: Optional[int]

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
    audio_files: List[str] = Field(default_factory=list)


class WelcomeMessageSetting(AudioSource):
    always_enabled: bool = Field(default=False)


class ComfortMessageSetting(AudioSource):
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


class QueueSettings(ApiModel):
    queue_size: int
    call_offer_tone_enabled: bool = Field(default=True)
    reset_call_statistics_enabled: bool = Field(default=True)
    overflow: OverflowSetting = Field(default_factory=OverflowSetting)
    wait_message: WaitMessageSetting = Field(default_factory=WaitMessageSetting)
    welcome_message: WelcomeMessageSetting = Field(default_factory=WelcomeMessageSetting)
    comfort_message: ComfortMessageSetting = Field(default_factory=ComfortMessageSetting.default)
    moh_message: MohMessageSetting = Field(default_factory=MohMessageSetting.default)


class CallQueueDetail(HGandCQ):
    """
    Call queue details
    """
    #: Language for call queue.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[CallPolicies]
    queue_settings: Optional[QueueSettings]
    allow_call_waiting_for_agents_enabled: Optional[bool]
    agents: List[Agent] = Field(default_factory=list)

    @staticmethod
    def create(name: str,
               agents: List[Agent],
               queue_size: int = None,
               enabled: bool = None,
               language_code: str = None,
               first_name: str = None,
               last_name: str = None,
               time_zone: str = None,
               phone_number: str = None,
               extension: str = None,
               call_policies: CallPolicies = None,
               queue_settings: QueueSettings = None,
               allow_call_waiting_for_agents_enabled: bool = None) -> 'CallQueueDetail':
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
        return CallQueueDetail(**params)


class CallQueueAPI:
    """
    Call Queue APÍ

    :ivar forwarding: forwarding API :class:`wxc_sdk.telephony.hg_and_cq.ForwardingAPI`
    :ivar announcement: announcement API :class:`announcement.AnnouncementAPI`

    """
    def __init__(self, session: RestSession):
        self._session = session
        self.forwarding = ForwardingAPI(session=session, feature_selector=FeatureSelector.queues)
        self.announcement = AnnouncementAPI(session=session)

    def _endpoint(self, location_id: str = None, queue_id: str = None):
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

    def list(self, location_id: str = None, name: str = None, org_id: str = None) -> Generator[CallQueue]:
        """
        Read the List of Call Queues
        :param location_id: Only return call queues with matching location ID.
        :param name: Only return call queues with the matching name.
        :param org_id: List call queues for this organization
        :return:
        """
        params = {to_camel(k): v
                  for i, (k, v) in enumerate(locals().items())
                  if i and v is not None}
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
                     if cq.name==name), None)

    def create(self, location_id: str, queue: CallQueueDetail, org_id: str = None) -> str:
        """
        Create a Call Queue
        :param location_id:
        :param queue:
        :param org_id:
        :return: queue id
        """
        params = org_id and {'orgId': org_id} or {}
        if not queue.call_policies:
            queue.call_policies = CallPolicies.simple()
        cq_data = queue.json()
        url = self._endpoint(location_id=location_id)
        data = self._session.rest_post(url, data=cq_data, params=params)
        return data['id']

    def delete_queue(self, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete queue
        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or None
        self._session.delete(url=url, params=params)

    def details(self, location_id: str, queue_id: str, org_id: str = None) -> CallQueueDetail:
        """
        Read Settings for a Call Queue
        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = {'orgId': org_id} if org_id is not None else {}
        data = self._session.rest_get(url, params=params)
        result = CallQueueDetail.parse_obj(data)
        # noinspection PyTypeChecker
        return result

    def update_callqueue(self, location_id: str, queue_id: str, queue: CallQueueDetail, org_id: str = None):
        """
        Configure a Call Queue

        :param location_id:
        :param queue_id:
        :param queue:
        :param org_id:
        :return: queue id
        """
        params = org_id and {'orgId': org_id} or None
        cq_data = queue.json(exclude={'id', 'language', 'location_name', 'location_id', 'toll_free_number'})

        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        self._session.rest_put(url=url, data=cq_data, params=params)
