from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListRoomsSortBy', 'Room', 'RoomCollectionResponse', 'RoomMeetingDetails', 'RoomType']


class RoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class Room(ApiModel):
    #: A unique identifier for the room.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    id: Optional[str] = None
    #: A user-friendly name for the room.
    #: example: Project Unicorn - Sprint 0
    title: Optional[str] = None
    #: The room type.
    #: example: group
    type: Optional[RoomType] = None
    #: Whether the room is moderated (locked) or not.
    #: example: True
    is_locked: Optional[bool] = None
    #: The ID for the team with which this room is associated.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNjRlNDVhZTAtYzQ2Yi0xMWU1LTlkZjktMGQ0MWUzNDIxOTcz
    team_id: Optional[str] = None
    #: The date and time of the room's last activity.
    #: example: 2016-04-21T19:12:48.920Z
    last_activity: Optional[datetime] = None
    #: The ID of the person who created this room.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creator_id: Optional[str] = None
    #: The date and time the room was created.
    #: example: 2016-04-21T19:01:55.966Z
    created: Optional[datetime] = None
    #: The ID of the organization which owns this room. See [Webex Data](/docs/api/guides/compliance#webex-teams-data)
    #: in the [Compliance Guide](/docs/api/guides/compliance) for more information.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    owner_id: Optional[str] = None
    #: Space classification ID represents the space's current classification.  It can be attached during space creation
    #: time, and can be modified at the request of an authorized user.
    #: example: Y2lzY29zcGFyazovL3VzL0NMQVNTSUZJQ0FUSU9OL2YyMDUyZTgyLTU0ZjgtMTFlYS1hMmUzLTJlNzI4Y2U4ODEyNQ
    classification_id: Optional[str] = None
    #: Indicates when a space is in Announcement Mode where only moderators can post messages
    is_announcement_only: Optional[bool] = None
    #: A compliance officer can set a direct room as read-only, which will disallow any new information exchanges in
    #: this space, while maintaing historical data.
    is_read_only: Optional[bool] = None
    #: The room is public and therefore discoverable within the org. Anyone can find and join that room.
    #: example: True
    is_public: Optional[bool] = None
    #: Date and time when the room was made public.
    #: example: 2022-10-10T17:24:19.388Z
    made_public: Optional[datetime] = None
    #: The description of the space.
    #: example: Company Announcements
    description: Optional[str] = None


class RoomCollectionResponse(ApiModel):
    items: Optional[list[Room]] = None


class RoomMeetingDetails(ApiModel):
    #: A unique identifier for the room.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The Webex meeting URL for the room.
    #: example: https://cisco.webex.com/m/37a7d3a8-6563-487f-9577-cd029101c087
    meeting_link: Optional[str] = None
    #: The SIP address for the room.
    #: example: 201632887@cisco.webex.com
    sip_address: Optional[str] = None
    #: The Webex meeting number for the room.
    #: example: 201632887
    meeting_number: Optional[str] = None
    #: The Webex meeting ID for the room.
    #: example: c1c30b52501b4d34aa75a57bdb867853
    meeting_id: Optional[str] = None
    #: The toll-free PSTN number for the room.
    #: example: +1-866-432-9903
    call_in_toll_free_number: Optional[str] = None
    #: The toll (local) PSTN number for the room.
    #: example: +1-408-525-6800
    call_in_toll_number: Optional[str] = None


class ListRoomsSortBy(str, Enum):
    id = 'id'
    lastactivity = 'lastactivity'
    created = 'created'
