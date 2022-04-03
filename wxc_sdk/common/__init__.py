"""
Common date types and APIs
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from ..base import webex_id_to_uuid

__all__ = ['UserType', 'UserBase', 'RingPattern', 'AlternateNumber', 'Greeting', 'UserNumber', 'PersonPlaceAgent',
           'MonitoredMember']


class UserType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'


class UserBase(ApiModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: Optional[UserType] = Field(alias='type')


class RingPattern(str, Enum):
    """
    Ring Pattern
    """
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumber(ApiModel):
    """
    Hunt group or call queue alternate number
    """
    #: Alternate phone number for the hunt group or call queue
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPattern]
    #: Flag: phone_number is a toll free number
    toll_free_number: Optional[bool]


class Greeting(str, Enum):
    """
    DEFAULT indicates that a system default message will be placed when incoming calls are intercepted.
    """
    #: A custom will be placed when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default message will be placed when incoming calls are intercepted.
    default = 'DEFAULT'


class UserNumber(ApiModel):
    """
    phone number of the person or workspace.
    """
    #: Phone number of person or workspace. Either phoneNumber or extension is mandatory
    external: Optional[str]
    #: Extension of person or workspace. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Flag to indicate primary phone.
    primary: Optional[bool]


class PersonPlaceAgent(UserBase):
    """
    Agent (person or place)
    """
    #: ID of person or workspace.
    agent_id: str = Field(alias='id')
    #: Display name of person or workspace.
    display_name: Optional[str]
    #: Email of the person or workspace.
    email: Optional[str]
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumber]]


class MonitoredMember(ApiModel):
    """
    a monitored user or place
    """
    #: The identifier of the monitored person.
    member_id: Optional[str] = Field(alias='id')
    #: The last name of the monitored person or place.
    last_name: Optional[str]
    #: The first name of the monitored person or place.
    first_name: Optional[str]
    #: The display name of the monitored person or place.
    display_name: Optional[str]
    #: Indicates whether type is PEOPLE or PLACE.
    member_type: Optional[UserType] = Field(alias='type')
    #: The email address of the monitored person or place.
    email: Optional[str]
    #: The list of phone numbers of the monitored person or place.
    numbers: Optional[list[UserNumber]]

    @property
    def ci_member_id(self) -> Optional[str]:
        return self.member_id and webex_id_to_uuid(self.member_id)
