from enum import Enum
from typing import Optional

from pydantic import Field

from ..base import ApiModel

__all__ = ['UserType', 'UserBase']


class UserType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'


class UserBase(ApiModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: UserType = Field(alias='type', default=UserType.people)
