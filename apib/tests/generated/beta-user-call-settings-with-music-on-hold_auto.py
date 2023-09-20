from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel', 'AudioAnnouncementFileGetObjectMediaFileType', 'GetMusicOnHoldObject', 'GetMusicOnHoldObjectGreeting', 'PutMusicOnHoldObject']


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across the organization.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across the location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    fileName: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    mediaFileType: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file location.
    #: example: ORGANIZATION
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class GetMusicOnHoldObjectGreeting(str, Enum):
    #: Play music configured at location level.
    default = 'DEFAULT'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class GetMusicOnHoldObject(ApiModel):
    #: Music on hold enabled or disabled for the person.
    #: example: True
    audioEnabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location.
    #: example: True
    mohLocationEnabled: Optional[bool] = None
    #: Greeting type for the person.
    #: example: DEFAULT
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audioAnnouncementFile: Optional[AudioAnnouncementFileGetObject] = None


class PutMusicOnHoldObject(ApiModel):
    #: Music on hold is enabled or disabled for the person.
    #: example: True
    audioEnabled: Optional[bool] = None
    #: Greeting type for the person.
    #: example: DEFAULT
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audioAnnouncementFile: Optional[AudioAnnouncementFileGetObject] = None
