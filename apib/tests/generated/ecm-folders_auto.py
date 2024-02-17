from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ECMFolder', 'ECMFolderLinkingApi', 'ECMFolderRoomType']


class ECMFolderRoomType(str, Enum):
    #: 1:1 room
    direct = 'direct'
    #: group room
    group = 'group'


class ECMFolder(ApiModel):
    #: A unique identifier for the folder.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL1RBQlMvZDg1ZTYwNj
    id: Optional[str] = None
    #: A unique identifier for the room to which the folder should be linked to.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The room type.
    #: example: group
    room_type: Optional[ECMFolderRoomType] = None
    #: Sharepoint or OneDrive drive id. It can be queried via MS Graph APIs.
    #: example: 123
    drive_id: Optional[str] = None
    #: Sharepoint or OneDrive item id. It can be queried via MS Graph APIs.
    #: example: 456
    item_id: Optional[str] = None
    #: Indicates if this is the default content storage for the room.
    default_folder: Optional[bool] = None
    #: This should match the folder name in the ECM backend.
    #: example: OneDrive folder for shared documents
    display_name: Optional[str] = None
    #: Folder's content URL.
    #: example: https://cisco-my.sharepoint.com/personal/naalluri/123
    content_url: Optional[str] = None
    #: The person ID of the person who created this folder link.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creator_id: Optional[str] = None
    #: The date and time when the folder link was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class ECMFolderLinkingApi(ApiChild, base='room/linkedFolders'):
    """
    ECM folder linking
    
    Enterprise Content Management folder-linking in Webex is how users configure existing OneDrive and SharePoint
    online folders as the (default or reference) storage backend for spaces. This configuration can be done in our
    native clients and via API.
    A space participant will be able to configure an ECM folder for a space. Only one ECM folder per space and only
    OneDrive and SharePoint online are currently supported.
    """

    def list_ecm_folder(self, room_id: str) -> list[ECMFolder]:
        """
        List ECM folder

        Lists the ECM folder of a room specified by the `roomId` query parameter.

        :param room_id: ID of the room for which to list the ECM folder.
        :type room_id: str
        :rtype: list[ECMFolder]
        """
        params = {}
        params['roomId'] = room_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ECMFolder]).validate_python(data['items'])
        return r

    def create_an_ecm_folder_configuration(self, room_id: str, content_url: str, display_name: str, drive_id: str,
                                           item_id: str, default_folder: str) -> ECMFolder:
        """
        Create an ECM folder configuration

        Adds an existing ECM folder to a room as (default or reference) file storage. There is no data validation
        happening for the request. Please ensure the correct `driveId` and `itemId.` These can be collected from the
        MS Graph API. The `contentUrl` and `displayName` are used only for user convenience. The folder will be
        configured with the MS folder name as `displayName`, and the `contentURL` may be updated or corrected as
        needed. To assess final configuration, please make a GET request on the linkedFolder.

        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the ECM folder.
        :type content_url: str
        :param display_name: This should match the folder name in the ECM backend.
        :type display_name: str
        :param drive_id: Sharepoint or OneDrive drive id. It can be queried via MS Graph APIs.
        :type drive_id: str
        :param item_id: Sharepoint or OneDrive item id. It can be queried via MS Graph APIs.
        :type item_id: str
        :param default_folder: Makes the folder the default storage for the space.
        :type default_folder: str
        :rtype: :class:`ECMFolder`
        """
        body = dict()
        body['roomId'] = room_id
        body['contentUrl'] = content_url
        body['displayName'] = display_name
        body['driveId'] = drive_id
        body['itemId'] = item_id
        body['defaultFolder'] = default_folder
        url = self.ep()
        data = super().post(url, json=body)
        r = ECMFolder.model_validate(data)
        return r

    def get_ecm_folder_details(self, id: str) -> ECMFolder:
        """
        Get ECM Folder Details

        Get details for a room ECM folder with the specified folder id.

        :param id: The unique identifier for the folder.
        :type id: str
        :rtype: :class:`ECMFolder`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = ECMFolder.model_validate(data)
        return r

    def update_an_ecm_linked_folder(self, id: str, room_id: str, content_url: str, display_name: str, drive_id: str,
                                    item_id: str, default_folder: str) -> ECMFolder:
        """
        Update an ECM Linked Folder

        Updates the configuration of the specified Room folder. There is no data validation happening for the request.
        Please ensure the correct `driveId` and `itemId.` These can be collected from the MS Graph API. The
        `contentUrl` and `displayName` are used only for user convenience. The folder will be configured with the MS
        folder name as `displayName`, and the `contentURL` may be updated or corrected as needed. To assess final
        configuration, please make a GET request on the linkedFolder.

        :param id: The unique identifier for the room folder.
        :type id: str
        :param room_id: ID of the room that contains the room tab in question.
        :type room_id: str
        :param content_url: Content URL of the folder.
        :type content_url: str
        :param display_name: This should match the folder name in the ECM backend.
        :type display_name: str
        :param drive_id: Sharepoint or OneDrive drive id. It can be queried via MS Graph APIs.
        :type drive_id: str
        :param item_id: Sharepoint or OneDrive item id. It can be queried via MS Graph APIs.
        :type item_id: str
        :param default_folder: Makes the folder the default storage for the space.
        :type default_folder: str
        :rtype: :class:`ECMFolder`
        """
        body = dict()
        body['roomId'] = room_id
        body['contentUrl'] = content_url
        body['displayName'] = display_name
        body['driveId'] = drive_id
        body['itemId'] = item_id
        body['defaultFolder'] = default_folder
        url = self.ep(f'{id}')
        data = super().put(url, json=body)
        r = ECMFolder.model_validate(data)
        return r

    def unlink_an_ecm_linked_folder(self, id: str):
        """
        Unlink an ECM linked folder

        Unlinks the room-linked folder with the specified ID from the space.

        :param id: The unique identifier for the folder to disassociate from the space.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'{id}')
        super().delete(url)
