from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'ListMeetingSessionTypesResponse', 'MeetingSessionTypeObject', 'Type']


class Type(str, Enum):
    #: Meeting session type for a meeting.
    meeting = 'meeting'
    #: Meeting session type for a webinar.
    webinar = 'webinar'
    #: Meeting session type for a private meeting.
    private_meeting = 'privateMeeting'


class MeetingSessionTypeObject(ApiModel):
    #: Unique identifier for the meeting session type.
    id: Optional[str]
    #: Name of the meeting session type.
    name: Optional[str]
    #: Meeting session type.
    type: Optional[Type]
    #: The maximum number of attendees for the meeting session type.
    attendees_capacity: Optional[int]


class ListMeetingSessionTypesResponse(ApiModel):
    #: Meeting session type array
    items: Optional[list[MeetingSessionTypeObject]]


class Api(ApiChild, base='meetings/sessionTypes'):
    """

    """

    def list_session_types(self, host_email: str = None, site_url: str = None) -> list[MeetingSessionTypeObject]:
        """
        List all the meeting session types enabled for a given user.

        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will list all the meeting session types enabled for the user.
        :type host_email: str
        :param site_url: Webex site URL to query. If siteUrl is not specified, the users' preferred site will be used.
            If the authorization token has the admin-level scopes, the admin can set the Webex site URL on behalf of
            the user specified in the hostEmail parameter.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
        data = super().get(url=url, params=params)
        return parse_obj_as(list[MeetingSessionTypeObject], data["items"])

    def session_type(self, session_type_id: int, host_email: str = None, site_url: str = None) -> MeetingSessionTypeObject:
        """
        Retrieves details for a meeting session type with a specified session type ID.

        :param session_type_id: A unique identifier for the sessionType.
        :type session_type_id: int
        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will get a meeting session type with the specified session type ID enabled for the user.
        :type host_email: str
        :param site_url: Webex site URL to query. If siteUrl is not specified, the users' preferred site will be used.
            If the authorization token has the admin-level scopes, the admin can set the Webex site URL on behalf of
            the user specified in the hostEmail parameter.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-session-type
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'{session_type_id}')
        data = super().get(url=url, params=params)
        return MeetingSessionTypeObject.parse_obj(data)

