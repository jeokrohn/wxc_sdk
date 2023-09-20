from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Team', 'TeamCollectionResponse']


class Team(ApiModel):
    #: A unique identifier for the team.
    #: example: Y2lzY29zcGFyazovL3VzL1RFQU0vMTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5
    id: Optional[str] = None
    #: A user-friendly name for the team.
    #: example: Build Squad
    name: Optional[str] = None
    #: The teams description.
    #: example: The A Team
    description: Optional[str] = None
    #: The date and time the team was created.
    #: example: 2015-10-18T14:26:16.000Z
    created: Optional[datetime] = None


class TeamCollectionResponse(ApiModel):
    items: Optional[list[Team]] = None
