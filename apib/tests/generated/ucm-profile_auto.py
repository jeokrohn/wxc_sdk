from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetManagerProfileObject', 'ReadTheListOfUcManagerProfilesResponse']


class GetManagerProfileObject(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    id: Optional[str] = None
    #: Unique name for the calling UC Manager Profile.
    #: example: UC Profile2
    name: Optional[str] = None


class ReadTheListOfUcManagerProfilesResponse(ApiModel):
    #: Array of manager profiles.
    calling_profiles: Optional[list[GetManagerProfileObject]] = None
