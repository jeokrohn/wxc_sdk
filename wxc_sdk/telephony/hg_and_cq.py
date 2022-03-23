"""
common base for Call Queues and Hunt Groups
"""
from base64 import b64decode
from enum import Enum
from typing import Optional, List

from pydantic import Field

from .user_base import UserBase
from ..base import ApiModel, webex_id_to_uuid
from wxc_sdk.common import AlternateNumber

__all__ = ['HGandCQ', 'Policy', 'Agent', 'AlternateNumberSettings']


class HGandCQ(ApiModel):
    name: Optional[str]
    id: Optional[str]
    location_name: Optional[str]  # only returned by list()
    location_id: Optional[str]  # # only returned by list()
    phone_number: Optional[str]
    extension: Optional[str]
    enabled: Optional[bool]
    toll_free_number: Optional[bool]

    @property
    def cpapi_id(self):
        return webex_id_to_uuid(self.id)

    @property
    def bc_id(self) -> Optional[str]:
        bc_id = webex_id_to_uuid(self.id)
        return bc_id and b64decode(bc_id).decode()


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
    alternate_numbers: List[AlternateNumber] = Field(default_factory=list)


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


class Agent(UserBase):
    extension: Optional[str]
    phone_number: Optional[str]
    weight: Optional[int]
    agent_id: str = Field(alias='id')

    @property
    def cpapi_id(self) -> str:
        return webex_id_to_uuid(self.agent_id)
