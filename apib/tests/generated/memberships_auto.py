from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Membership', 'MembershipCollectionResponse', 'MembershipRoomType']


class MembershipRoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class Membership(ApiModel):
    #: A unique identifier for the membership.
    #: example: Y2lzY29zcGFyazovL3VzL01FTUJFUlNISVAvMGQwYzkxYjYtY2U2MC00NzI1LWI2ZDAtMzQ1NWQ1ZDExZWYzOmNkZTFkZDQwLTJmMGQtMTFlNS1iYTljLTdiNjU1NmQyMjA3Yg
    id: Optional[str] = None
    #: The room ID.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of the person.
    #: example: john.andersen@example.com
    person_email: Optional[str] = None
    #: The display name of the person.
    #: example: John Andersen
    person_display_name: Optional[str] = None
    #: The organization ID of the person.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    person_org_id: Optional[str] = None
    #: Whether or not the participant is a room moderator.
    #: example: True
    is_moderator: Optional[bool] = None
    #: Whether or not the direct type room is hidden in the Webex clients.
    is_room_hidden: Optional[bool] = None
    #: The type of room the membership is associated with.
    #: example: direct
    room_type: Optional[MembershipRoomType] = None
    #: Whether or not the participant is a monitoring bot (deprecated).
    is_monitor: Optional[bool] = None
    #: The date and time when the membership was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class MembershipCollectionResponse(ApiModel):
    items: Optional[list[Membership]] = None
