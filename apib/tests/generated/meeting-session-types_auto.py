from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['SessionType', 'SessionTypesApi', 'SiteSessionType', 'SiteSessionTypeType', 'UserSessionTypes']


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
    id: Optional[str] = None
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
    id: Optional[str] = None
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


class SessionTypesApi(ApiChild, base='admin/meeting'):
    """
    Session Types
    
    Session types define the features and options that are available to users for scheduled meetings.
    
    The API allows getting site-level session types and modifying user-level session types.
    
    Viewing the list of site session types and user session types requires an administrator auth token with
    `meeting:admin_schedule_read` or `meeting:admin_config_read`. Updating user session types requires an
    administrator auth token with the `meeting:admin_schedule_write` or `meeting:admin_config_write` scope.
    """

    def list_site_session_types(self, site_url: str = None) -> list[SiteSessionType]:
        """
        List Site Session Types

        List session types for a specific site.

        :param site_url: URL of the Webex site to query. If siteUrl is not specified, the query will use the default
            site for the admin's authorization token used to make the call.
        :type site_url: str
        :rtype: list[SiteSessionType]
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('config/sessionTypes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[SiteSessionType]).validate_python(data['items'])
        return r

    def list_user_session_type(self, site_url: str = None, person_id: str = None) -> list[UserSessionTypes]:
        """
        List User Session Type

        List session types for a specific user.

        :param site_url: URL of the Webex site to query.
        :type site_url: str
        :param person_id: A unique identifier for the user.
        :type person_id: str
        :rtype: list[UserSessionTypes]
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep('userconfig/sessionTypes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[UserSessionTypes]).validate_python(data['items'])
        return r

    def update_user_session_types(self, site_url: str, session_type_ids: list[str], person_id: str = None,
                                  email: str = None) -> UserSessionTypes:
        """
        Update User Session Types

        Assign session types to specific users.

        * At least one of the following body parameters is required to update a specific user session type: `personId`,
        `email`.

        :param site_url: Site URL for the session type.
        :type site_url: str
        :param session_type_ids: An array of the session type ID.
        :type session_type_ids: list[str]
        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param email: The email of the user.
        :type email: str
        :rtype: :class:`UserSessionTypes`
        """
        body = dict()
        body['siteUrl'] = site_url
        if person_id is not None:
            body['personId'] = person_id
        if email is not None:
            body['email'] = email
        body['sessionTypeIds'] = session_type_ids
        url = self.ep('userconfig/sessionTypes')
        data = super().put(url, json=body)
        r = UserSessionTypes.model_validate(data)
        return r
