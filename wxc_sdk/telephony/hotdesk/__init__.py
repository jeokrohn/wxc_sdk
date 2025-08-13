from datetime import datetime
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['HotDesk', 'HotDeskApi']


class HotDesk(ApiModel):
    #: A unique identifier for a hot desk session.
    session_id: Optional[str] = None
    #: The workspace where the hot desk session is active.
    workspace_id: Optional[str] = None
    #: The id of the person who initiated the hot desk session.
    person_id: Optional[str] = None
    #: The start time of the booking.
    booking_start_time: Optional[datetime] = None
    #: The end time of the booking.
    booking_end_time: Optional[datetime] = None


class HotDeskApi(ApiChild, base='hotdesk/sessions'):
    """
    Hot Desk

    """

    def list_sessions(self, person_id: str = None, workspace_id: str = None, org_id: str = None) -> list[HotDesk]:
        """
        List Sessions

        List hot desk sessions.

        Use query parameters to filter the response.
        The `orgId` parameter is for use by partner administrators acting on a managed organization.
        The `personId` and `workspaceId` parameters are optional and are used to filter the response to only include
        sessions for a specific person or workspace.
        When used together they are used as an AND filter.

        :param person_id: List sessions for this person.
        :type person_id: str
        :param workspace_id: List sessions for this workspace.
        :type workspace_id: str
        :param org_id: List sessions in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :rtype: list[HotDesk]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if person_id is not None:
            params['personId'] = person_id
        if workspace_id is not None:
            params['workspaceId'] = workspace_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[HotDesk]).validate_python(data['items'])
        return r

    def delete_session(self, session_id: str):
        """
        Delete Session

        Delete a hot desk session.

        :param session_id: The unique identifier for the hot desk session.
        :type session_id: str
        :rtype: None
        """
        url = self.ep(f'{session_id}')
        super().delete(url)
