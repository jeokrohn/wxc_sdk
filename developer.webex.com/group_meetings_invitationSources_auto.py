from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'CreateInvitationSourcesResponse', 'InvitationSourceCreateObject', 'InvitationSourceObject',
           'ListInvitationSourcesResponse']


class InvitationSourceCreateObject(ApiModel):
    #: Source ID for the invitation.
    source_id: Optional[str]
    #: Email for invitation source.
    source_email: Optional[str]


class InvitationSourceObject(InvitationSourceCreateObject):
    #: Unique identifier for invitation source.
    id: Optional[str]
    #: The link bound to sourceId can directly join the meeting.If the meeting requires registration,joinLink is not
    #: returned.
    join_link: Optional[str]
    #: The link bound to sourceId can directly register the meeting.If the meeting requires registration,registerLink
    #: is returned.
    register_link: Optional[str]


class CreateInvitationSourcesBody(ApiModel):
    #: Email address for the meeting host. This parameter is only used if a user or application calling the API has the
    #: admin-level scopes. The admin may specify the email of a user on a site they manage and the API will return
    #: meeting participants of the meetings that are hosted by that user.
    host_email: Optional[str]
    #: Unique identifier for the meeting host. Should only be set if the user or application calling the API has the
    #: admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting
    #: host.
    person_id: Optional[str]
    items: Optional[list[InvitationSourceCreateObject]]


class CreateInvitationSourcesResponse(ApiModel):
    #: Invitation source array.
    items: Optional[list[InvitationSourceObject]]


class ListInvitationSourcesResponse(ApiModel):
    #: Invitation source array.
    items: Optional[list[InvitationSourceObject]]


class Api(ApiChild, base='meetings/'):
    """

    """

    def create_sources(self, meeting_id: str, host_email: str = None, person_id: str = None, items: InvitationSourceCreateObject = None) -> list[InvitationSourceObject]:
        """
        Creates one or more invitation sources for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param person_id: Unique identifier for the meeting host. Should only be set if the user or application calling
            the API has the admin-level scopes. When used, the admin may specify the email of a user in a site they
            manage to be the meeting host.
        :type person_id: str
        :param items: 
        :type items: InvitationSourceCreateObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-invitation-sources
        """
        body = CreateInvitationSourcesBody()
        if host_email is not None:
            body.host_email = host_email
        if person_id is not None:
            body.person_id = person_id
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().post(url=url, data=body.json())
        return parse_obj_as(list[InvitationSourceObject], data["items"])

    def list_sources(self, meeting_id: str) -> list[InvitationSourceObject]:
        """
        Lists invitation sources for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-invitation-sources
        """
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().get(url=url)
        return parse_obj_as(list[InvitationSourceObject], data["items"])

