from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['File', 'FileExternalContent']


class FileExternalContent(ApiModel):
    #: example: Screen Shot 2019-02-08 at 8.55.10 AM.png
    originalFilename: Optional[str] = None
    #: example: 39164
    originalFileSize: Optional[str] = None
    #: example: image/png
    mimeType: Optional[str] = None
    #: example: ecm
    linkType: Optional[str] = None
    #: example: oneDriveForBusiness
    ecmType: Optional[str] = None
    #: example: 2019-04-11T18:22:18.626Z
    created: Optional[datetime] = None


class File(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL0ZJTEUvMTk1ZmY1MDAtNGYzOS0xMWU5LWI0ZDMtZjE1YWVjOWVjYWRiLzA
    id: Optional[str] = None
    #: example: https://example-my.sharepoint.com/:i:/p/jandersen/ERIEW6cL4DlDrAoUHM6_K1cBvRNcNEood98f2EgCFpbdSA
    contentUrl: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNWEzZTI4YzAtMzUzNi0xMWU5LTgyN2QtZTMyNWFhYmU1Y2M5
    roomId: Optional[str] = None
    #: example: group
    roomType: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvMTk1ZmY1MDAtNGYzOS0xMWU5LWI0ZDMtZjE1YWVjOWVjYWRi
    messageId: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wMGZhZTA2My02ODEyLTQ3ZmQtYmJjNi1hNzVlMjlhNWM1ZjA
    personId: Optional[str] = None
    #: example: external
    contentType: Optional[str] = None
    externalContent: Optional[FileExternalContent] = None
