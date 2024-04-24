"""
common base for Call Queues and Hunt Groups
"""
from base64 import b64decode
from typing import Optional

from pydantic import Field

from ..base import ApiModel, webex_id_to_uuid
from ..base import SafeEnum as Enum
from ..common import UserBase, AlternateNumber, IdAndName

__all__ = ['HGandCQ', 'Policy', 'Agent', 'AlternateNumberSettings', 'CallingLineIdPolicy']


class AlternateNumberSettings(ApiModel):
    """
    Alternate number settings for call queue or hunt group

    The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue or hunt
    group. Each
    number will reach the same greeting and each menu will function identically to the main number. The alternate
    numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    """
    #: Distinctive Ringing selected for the alternate numbers in the call queue or hunt group overrides the normal
    #: ringing patterns set for Alternate Number.
    distinctive_ring_enabled: bool = Field(default=True)
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumber]] = None


class Agent(UserBase):
    #: ID of person, workspace or virtual line.
    agent_id: str = Field(alias='id')
    #: Phone number of person or workspace.
    phone_number: Optional[str] = None
    #: Extension of person or workspace.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Weight of person, workspace or virtual line. Only applied when call policy is WEIGHTED.
    weight: Optional[str] = None
    #: Skill level of person, workspace or virtual line. Only applied when the call routingType is SKILL_BASED.
    skill_level: Optional[int] = None
    #: Indicates the join status of the agent for this queue. Only for call queues
    join_enabled: Optional[bool] = None
    location: Optional[IdAndName] = None

    @property
    def cpapi_id(self) -> str:
        return webex_id_to_uuid(self.agent_id)


class CallingLineIdPolicy(str, Enum):
    direct_line = 'DIRECT_LINE'
    location_number = 'LOCATION_NUMBER'
    customer = 'CUSTOM'


class HGandCQ(ApiModel):
    """
    Common attributes of hunt groups and call queues
    """
    #: Unique name
    name: Optional[str] = None
    #: Unique identified
    id: Optional[str] = None
    location_name: Optional[str] = None  # only returned by list()
    location_id: Optional[str] = None  # # only returned by list()
    #: Primary phone number
    phone_number: Optional[str] = None
    #: Extension
    extension: Optional[str] = None
    #: Routing prefix of location.
    routingPrefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Which type of Calling LineID Policy Selected for Call Queue.
    calling_line_id_policy: Optional[CallingLineIdPolicy] = None
    #: Calling line Id Phone number which will be shown if CUSTOM is selected.
    calling_line_id_phone_number: Optional[str] = None
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings] = None
    #: enabled flag
    enabled: Optional[bool] = None
    #: True: phone_number is toll_free
    toll_free_number: Optional[bool] = None
    #: Language for call queue.
    language: Optional[str] = None
    #: Language code.
    language_code: Optional[str] = None
    #: First name to be shown when calls are forwarded out. Defaults to ".".
    first_name: Optional[str] = None
    #: Last name to be shown when calls are forwarded out. Defaults to the phone number if set,
    #: otherwise defaults to name.
    last_name: Optional[str] = None
    #: Time zone for the call queue.
    time_zone: Optional[str] = None
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[Agent]] = None

    @property
    def cpapi_id(self):
        return webex_id_to_uuid(self.id)

    @property
    def bc_id(self) -> Optional[str]:
        bc_id = webex_id_to_uuid(self.id)
        return bc_id and b64decode(bc_id).decode()

    @staticmethod
    def exclude_update_or_create() -> dict:
        """
        Exclude dict for update or create calls

        :meta private:
        :return: dict
        """
        return {'id': True,
                'location_name': True,
                'location_id': True,
                'toll_free_number': True,
                'language': True,
                'routing_prefix': True,
                'esn': True,
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
                              {'toll_free_number': True}}}}

    def create_or_update(self) -> str:
        """
        Get JSON for create or update call

        :return: JSON
        :rtype: str
        """
        return self.model_dump_json(exclude=self.exclude_update_or_create())


class Policy(str, Enum):
    """
    Policy controlling how calls are routed to agents.
    """
    #: (Max 1,000 agents) This option cycles through all agents after the last agent that took a call. It sends calls
    #: to the next available agent.
    circular = 'CIRCULAR'
    #: (Max 1,000 agents) Send the call through the queue of agents in order, starting from the top each time.
    regular = 'REGULAR'
    #: (Max 50 agents) Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: (Max 1,000 agents) Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the
    #: next agent who has been idle the second longest, and so on until the call is answered.
    uniform = 'UNIFORM'
    #: (Max 100 agents) Sends call to idle agents based on percentages you assign to each agent (up to 100%).
    weighted = 'WEIGHTED'
