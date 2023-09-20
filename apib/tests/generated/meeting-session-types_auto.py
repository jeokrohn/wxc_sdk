from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['SessionType', 'SiteSessionType', 'SiteSessionTypeType', 'UpdateUserSessionType', 'UserSessionTypes']


class SiteSessionTypeType(str, Enum):
    #: Meeting Center.
    meeting = 'meeting'
    #: Webinar meeting.
    webinar = 'webinar'
    #: Private meeting.
    privatemeeting = 'privateMeeting'
    #: Event Center.
    eventcenter = 'EventCenter'
    #: Support Center.
    supportcenter = 'SupportCenter'
    #: Training Center.
    traincenter = 'TrainCenter'


class SiteSessionType(ApiModel):
    #: The ID of the session type.
    #: example: 3
    id: Optional[datetime] = None
    #: The short name of the session type.
    #: example: PRO
    shortName: Optional[str] = None
    #: Site URL for the session type.
    #: example: example.webex.com
    siteUrl: Optional[str] = None
    #: The name of the session type.
    #: example: Pro Meeting
    name: Optional[str] = None
    #: The meeting type of meeting that you can create with the session type.
    #: example: meeting
    type: Optional[SiteSessionTypeType] = None


class SessionType(ApiModel):
    #: The ID of the session type.
    #: example: 3
    id: Optional[datetime] = None
    #: The short name of the session type.
    #: example: PRO
    shortName: Optional[str] = None
    #: The name of the session type.
    #: example: Pro Meeting
    name: Optional[str] = None
    #: The meeting type of meeting that you can create with the session type.
    #: example: meeting
    type: Optional[SiteSessionTypeType] = None


class UserSessionTypes(ApiModel):
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yNWJiZjgzMS01YmU5LTRjMjUtYjRiMC05YjU5MmM4YTA4NmI
    personId: Optional[str] = None
    #: The email of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Site URL for the user.
    #: example: example.webex.com
    siteUrl: Optional[str] = None
    #: All session types are supported by the user on the site.
    sessionTypes: Optional[list[SessionType]] = None


class UpdateUserSessionType(ApiModel):
    #: Site URL for the session type.
    #: example: example.webex.com
    siteUrl: Optional[str] = None
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yNWJiZjgzMS01YmU5LTRjMjUtYjRiMC05YjU5MmM4YTA4NmI
    personId: Optional[str] = None
    #: The email of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: An array of the session type ID.
    #: example: ['3', '9']
    sessionTypeIds: Optional[list[str]] = None
