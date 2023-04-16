from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'BreakoutSessionObject', 'GetBreakoutSessionObject', 'ListMeetingBreakoutSessionsResponse',
           'UpdateMeetingBreakoutSessionsResponse']


class BreakoutSessionObject(ApiModel):
    #: Name for breakout session.
    name: Optional[str]
    #: Invitees for breakout session. Please note that one invitee cannot be assigned to more than one breakout
    #: session.
    invitees: Optional[list[str]]


class GetBreakoutSessionObject(BreakoutSessionObject):
    #: Unique identifier for breakout session.
    id: Optional[str]


class UpdateMeetingBreakoutSessionsBody(ApiModel):
    #: Email address for the meeting host. This parameter is only used if the user or application calling the API has
    #: the admin-level scopes. If set, the admin may specify the email of a user in a site they manage and the API will
    #: return details for a meeting that is hosted by that user.
    host_email: Optional[str]
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    send_email: Optional[bool]
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main session.
    #: Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts
    #: preassign attendees to breakout sessions, the role of attendee will be changed to panelist. Breakout session is
    #: not supported for a meeting with simultaneous interpretation.
    items: Optional[list[BreakoutSessionObject]]


class UpdateMeetingBreakoutSessionsResponse(ApiModel):
    #: Breakout Sessions information for meeting.
    items: Optional[list[GetBreakoutSessionObject]]


class ListMeetingBreakoutSessionsResponse(ApiModel):
    #: Breakout Sessions information for meeting.
    items: Optional[list[GetBreakoutSessionObject]]


class Api(ApiChild, base='meetings/'):
    """

    """

    def update_breakout_sessions(self, meeting_id: str, host_email: str = None, send_email: bool = None, items: BreakoutSessionObject = None) -> list[GetBreakoutSessionObject]:
        """
        Updates breakout sessions of a meeting with a specified meeting ID. This operation applies to meeting series
        and scheduled meetings.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param items: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They
            allow a subset of participants to collaborate and share ideas over audio and video. Use breakout sessions
            for workshops, classrooms, or for when you need a moment to talk privately with a few participants outside
            of the main session. Please note that maximum number of breakout sessions in a meeting or webinar is 100.
            In webinars, if hosts preassign attendees to breakout sessions, the role of attendee will be changed to
            panelist. Breakout session is not supported for a meeting with simultaneous interpretation.
        :type items: BreakoutSessionObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-breakout-sessions
        """
        body = UpdateMeetingBreakoutSessionsBody()
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().put(url=url, data=body.json())
        return parse_obj_as(list[GetBreakoutSessionObject], data["items"])

    def list_breakout_sessions(self, meeting_id: str) -> list[GetBreakoutSessionObject]:
        """
        Lists meeting breakout sessions for a meeting with a specified meetingId.
        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        See the Webex Meetings guide for more information about the types of meetings.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series, scheduled
            meeting and ended or ongoing meeting instance objects. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-breakout-sessions
        """
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().get(url=url)
        return parse_obj_as(list[GetBreakoutSessionObject], data["items"])

    def delete_breakout_sessions(self, meeting_id: str, send_email: bool = None):
        """
        Deletes breakout sessions with a specified meeting ID. The deleted breakout sessions cannot be recovered. The
        value of enabledBreakoutSessions attribute is set to false automatically.
        This operation applies to meeting series and scheduled meetings. It doesn't apply to ended or in-progress
        meeting instances.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-meeting-breakout-sessions
        """
        params = {}
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}/breakoutSessions')
        super().delete(url=url, params=params)
        return

