from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListSiteSessionTypesResponse', 'ListUserSessionTypeResponse', 'SessionType', 'SiteSessionType',
            'SiteSessionTypeType', 'UpdateUserSessionType', 'UserSessionTypes']


class SiteSessionTypeType(str, Enum):
    #: Meeting Center.
    meeting = 'meeting'
    #: Webinar meeting.
    webinar = 'webinar'
    #: Private meeting.
    private_meeting = 'privateMeeting'
    #: Event Center.
    event_center = 'EventCenter'
    #: Support Center.
    support_center = 'SupportCenter'
    #: Training Center.
    train_center = 'TrainCenter'


class SiteSessionType(ApiModel):
    #: The ID of the session type.
    #: example: 3
    id: Optional[datetime] = None
    #: The short name of the session type.
    #: example: PRO
    short_name: Optional[str] = None
    #: Site URL for the session type.
    #: example: example.webex.com
    site_url: Optional[str] = None
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
    short_name: Optional[str] = None
    #: The name of the session type.
    #: example: Pro Meeting
    name: Optional[str] = None
    #: The meeting type of meeting that you can create with the session type.
    #: example: meeting
    type: Optional[SiteSessionTypeType] = None


class UserSessionTypes(ApiModel):
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yNWJiZjgzMS01YmU5LTRjMjUtYjRiMC05YjU5MmM4YTA4NmI
    person_id: Optional[str] = None
    #: The email of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Site URL for the user.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: All session types are supported by the user on the site.
    session_types: Optional[list[SessionType]] = None


class UpdateUserSessionType(ApiModel):
    #: Site URL for the session type.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: A unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yNWJiZjgzMS01YmU5LTRjMjUtYjRiMC05YjU5MmM4YTA4NmI
    person_id: Optional[str] = None
    #: The email of the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: An array of the session type ID.
    #: example: ['3', '9']
    session_type_ids: Optional[list[str]] = None


class ListSiteSessionTypesResponse(ApiModel):
    #: An array of the site's session types.
    items: Optional[list[SiteSessionType]] = None


class ListUserSessionTypeResponse(ApiModel):
    #: An array of the user's session types.
    items: Optional[list[UserSessionTypes]] = None


class SessionTypesApi(ApiChild, base='admin/meeting'):
    """
    Session Types
    
    Session types define the features and options that are available to users for scheduled meetings.
    
    The API allows getting site-level session types and modifying user-level session types.
    
    Viewing the list of site session types and user session types requires an administrator auth token with
    `meeting:admin_schedule_read` or `meeting:admin_config_read`. Updating user session types requires an
    administrator auth token with the `meeting:admin_schedule_write` or `meeting:admin_config_write` scope.
    """
    ...