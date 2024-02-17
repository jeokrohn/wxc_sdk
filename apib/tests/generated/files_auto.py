from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['File', 'FileExternalContent', 'FilesApi']


class FileExternalContent(ApiModel):
    #: example: Screen Shot 2019-02-08 at 8.55.10 AM.png
    original_filename: Optional[str] = None
    #: example: 39164
    original_file_size: Optional[str] = None
    #: example: image/png
    mime_type: Optional[str] = None
    #: example: ecm
    link_type: Optional[str] = None
    #: example: oneDriveForBusiness
    ecm_type: Optional[str] = None
    #: example: 2019-04-11T18:22:18.626Z
    created: Optional[datetime] = None


class File(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL0ZJTEUvMTk1ZmY1MDAtNGYzOS0xMWU5LWI0ZDMtZjE1YWVjOWVjYWRiLzA
    id: Optional[str] = None
    #: example: https://example-my.sharepoint.com/:i:/p/jandersen/ERIEW6cL4DlDrAoUHM6_K1cBvRNcNEood98f2EgCFpbdSA
    content_url: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNWEzZTI4YzAtMzUzNi0xMWU5LTgyN2QtZTMyNWFhYmU1Y2M5
    room_id: Optional[str] = None
    #: example: group
    room_type: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL01FU1NBR0UvMTk1ZmY1MDAtNGYzOS0xMWU5LWI0ZDMtZjE1YWVjOWVjYWRi
    message_id: Optional[str] = None
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wMGZhZTA2My02ODEyLTQ3ZmQtYmJjNi1hNzVlMjlhNWM1ZjA
    person_id: Optional[str] = None
    #: example: external
    content_type: Optional[str] = None
    external_content: Optional[FileExternalContent] = None


class FilesApi(ApiChild, base='files'):
    """
    Files
    
    """

    def get_file_details(self, file_id: str) -> File:
        """
        Get File Details

        :param file_id: The unique identifier for the file.
        :type file_id: str
        :rtype: :class:`File`
        """
        url = self.ep(f'{file_id}')
        data = super().get(url)
        r = File.model_validate(data)
        return r
