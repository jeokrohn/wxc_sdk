from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['RoomTab', 'RoomTabRoomType', 'RoomTabsApi']


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


class RoomTabsApi(ApiChild, base='room/tabs'):
    """
    Room Tabs
    
    A Room Tab represents a URL shortcut that is added as a persistent tab to a Webex room (space) tab row. Use this
    API to list tabs of any Webex room that you belong to. Room Tabs can also be updated to point to a different
    content URL, or deleted to remove the tab from the room.
    
    Just like in the Webex app, you must be a member of the room in order to list its Room Tabs.
    """

    def list_room_tabs(self, room_id: str) -> list[RoomTab]:
        """
        List Room Tabs

        Lists all Room Tabs of a room specified by the `roomId` query parameter.

        :param room_id: ID of the room for which to list room tabs.
        :type room_id: str
        :rtype: list[RoomTab]
        """
        params = {}
        params['roomId'] = room_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[RoomTab]).validate_python(data['items'])
        return r

    def create_a_room_tab(self, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Create a Room Tab

        Add a tab with a specified URL to a room.

        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the Room Tab. Must use `https` protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        :rtype: :class:`RoomTab`
        """
        body = dict()
        body['roomId'] = room_id
        body['contentUrl'] = content_url
        body['displayName'] = display_name
        url = self.ep()
        data = super().post(url, json=body)
        r = RoomTab.model_validate(data)
        return r

    def get_room_tab_details(self, id: str) -> RoomTab:
        """
        Get Room Tab Details

        Get details for a Room Tab with the specified room tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str
        :rtype: :class:`RoomTab`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = RoomTab.model_validate(data)
        return r

    def update_a_room_tab(self, id: str, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Update a Room Tab

        Updates the content URL of the specified Room Tab ID.

        :param id: The unique identifier for the Room Tab.
        :type id: str
        :param room_id: ID of the room that contains the room tab in question.
        :type room_id: str
        :param content_url: Content URL of the Room Tab. URL must use `https` protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        :rtype: :class:`RoomTab`
        """
        body = dict()
        body['roomId'] = room_id
        body['contentUrl'] = content_url
        body['displayName'] = display_name
        url = self.ep(f'{id}')
        data = super().put(url, json=body)
        r = RoomTab.model_validate(data)
        return r

    def delete_a_room_tab(self, id: str):
        """
        Delete a Room Tab

        Deletes a Room Tab with the specified ID.

        :param id: The unique identifier for the Room Tab to delete.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'{id}')
        super().delete(url)
