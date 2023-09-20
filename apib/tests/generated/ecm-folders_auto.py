from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ECMFolder', 'ECMFolderCollectionResponse', 'ECMFolderRoomType']


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
    roomId: Optional[str] = None
    #: The room type.
    #: example: group
    roomType: Optional[ECMFolderRoomType] = None
    #: Sharepoint or OneDrive drive id. It can be queried via MS Graph APIs.
    #: example: 123
    driveId: Optional[datetime] = None
    #: Sharepoint or OneDrive item id. It can be queried via MS Graph APIs.
    #: example: 456
    itemId: Optional[datetime] = None
    #: Indicates if this is the default content storage for the room.
    #: example: false
    defaultFolder: Optional[str] = None
    #: This should match the folder name in the ECM backend.
    #: example: OneDrive folder for shared documents
    displayName: Optional[str] = None
    #: Folder's content URL.
    #: example: https://cisco-my.sharepoint.com/personal/naalluri/123
    contentUrl: Optional[str] = None
    #: The person ID of the person who created this folder link.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creatorId: Optional[str] = None
    #: The date and time when the folder link was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class ECMFolderCollectionResponse(ApiModel):
    items: Optional[list[ECMFolder]] = None
