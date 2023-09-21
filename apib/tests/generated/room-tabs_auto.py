from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['RoomTab', 'RoomTabRoomType', 'RoomTabsCollectionResponse']


class RoomTabRoomType(str, Enum):
    #: 1:1 room
    direct = 'direct'
    #: group room
    group = 'group'


class RoomTab(ApiModel):
    #: A unique identifier for the Room Tab.
    #: example: Y2lzY29zcGFyazovL3VzL01FTUJFUlNISVAvMGQwYzkxYjYtY2U2MC00NzI1LWI2ZDAtMzQ1NWQ1ZDExZWYzOmNkZTFkZDQwLTJmMGQtMTFlNS1iYTljLTdiNjU1NmQyMjA3Yg
    id: Optional[str] = None
    #: A unique identifier for the room containing the room tab.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The room type.
    #: example: group
    room_type: Optional[RoomTabRoomType] = None
    #: User-friendly name for the room tab.
    #: example: Cisco HomePage
    display_name: Optional[str] = None
    #: Room Tab's content URL.
    #: example: https://www.cisco.com
    content_url: Optional[str] = None
    #: The person ID of the person who created this Room Tab.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creator_id: Optional[str] = None
    #: The date and time when the Room Tab was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class RoomTabsCollectionResponse(ApiModel):
    items: Optional[list[RoomTab]] = None
