from collections.abc import Generator
from typing import List, Optional

from ...api_child import ApiChild
from ...base import ApiModel

__all__ = ['CreateInviteesItem', 'Invitee', 'MeetingInviteesApi', 'CreateMeetingInviteeBody',
           'UpdateMeetingInviteeBody', 'CreateMeetingInviteesBody']


class Invitee(ApiModel):
    #: Unique identifier for meeting invitee.
    id: Optional[str]
    #: Email address for meeting invitee. This attribute can be modified by Update a Meeting Invitee API.
    email: Optional[str]
    #: Display name for meeting invitee. This attribute can be modified by Update a Meeting Invitee API.
    display_name: Optional[str]
    # : Whether or not invitee is a designated alternate host for the meeting. See Add Alternate Hosts for Cisco
    #: Webex Meetings for more details.
    co_host: Optional[bool]
    # : Unique identifier for the meeting for which invitees are being requested. The meeting can be a meeting
    #: series, a scheduled meeting, or a meeting instance which has ended or is ongoing.
    meeting_id: Optional[str]
    #: If true, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool]


class CreateInviteesItem(ApiModel):
    #: Email address for meeting invitee.
    email: Optional[str]
    #: Display name for meeting invitee. The maximum length of displayName is 128 characters. In Webex App,
    #: if the email has been associated with an existing Webex account, the display name associated with the Webex
    #: account will be used; otherwise, the email will be used as displayName. In Webex site, if displayName is
    #: specified, it will show displayName. If displayName is not specified, and the email has been associated with an
    #: existing Webex account, the display name associated with the Webex account will be used; otherwise,
    #: the email will be used as displayName. : Please note that if the invitee has an existing Webex account,
    #: the displayName shown in the meeting will be the displayName associated with the Webex account; otherwise,
    #: displayName shown in the meeting will be the displayName which is specified by the invitee who does not have a
    #: Webex account.
    display_name: Optional[str]
    #: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate Hosts for Cisco
    #: Webex Meetings for more details.
    co_host: Optional[bool]
    #: If true, send an email to the invitee.
    send_email: Optional[bool]
    #: If true, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool]


class CreateMeetingInviteeBody(CreateInviteesItem):
    #: Unique identifier for the meeting to which a person is being invited. This attribute only applies to meeting
    #: series and scheduled meeting. If it's a meeting series, the meeting invitee is invited to the entire meeting
    #: series; if it's a scheduled meeting, the meeting invitee is invited to this individual scheduled meeting. It
    #: doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled personal room meeting is
    #: not supported for this API.
    meeting_id: Optional[str]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the
    #: API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they
    #: manage to be the meeting host.
    host_email: Optional[str]


class CreateMeetingInviteesBody(ApiModel):
    #: Unique identifier for the meeting to which the people are being invited. This attribute only applies to
    #: meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are invited to the entire
    #: meeting series; if it's a scheduled meeting, the meeting invitees are invited to this individual scheduled
    #: meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled personal room
    #: meeting is not supported for this API.
    meeting_id: Optional[str]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the
    #: API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they
    #: manage to be the meeting host.
    host_email: Optional[str]
    #: Meeting invitees to be inserted.
    items: Optional[list[CreateInviteesItem]]


class UpdateMeetingInviteeBody(CreateInviteesItem):
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the
    #: API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they
    #: manage to be the meeting host.
    host_email: Optional[str]


class MeetingInviteesApi(ApiChild, base='meetingInvitees'):
    """
    This API manages invitees' relationships to a meeting.
    You can use the Meeting Invitees API to list, create, update, and delete invitees.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list(self, meeting_id: str, host_email: str = None, panelist: bool = None,
             **params) -> Generator[Invitee, None, None]:
        """
        Lists meeting invitees for a meeting with a specified meetingId. You can set a maximum number of invitees to
        return. This operation can be used for meeting series, scheduled meetings, and ended or ongoing meeting
        instance objects. If the specified meetingId is for a meeting series, the invitees for the series will be
        listed; if the meetingId is for a scheduled meeting, the invitees for the particular scheduled meeting will
        be listed; if the meetingId is for an ended or ongoing meeting instance, the invitees for the particular
        meeting instance will be listed. See the Webex Meetings guide for more information about the types of
        meetings. The list returned is sorted in ascending order by email address. Long result sets are split into
        pages.

        :param meeting_id: Unique identifier for the meeting for which invitees are being requested. The meeting
            can be a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing. The
            meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or
            application calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of
            a user in a site they manage and the API will return meeting invitees that are hosted by that user.
        :type host_email: str
        :param panelist: Filter invitees or attendees for webinars only. If true,
            returns invitees. If false, returns attendees. If null, returns both invitees and attendees.
        :type panelist: bool
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if panelist is not None:
            params['panelist'] = str(panelist).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Invitee, params=params)

    def create_invitee(self, email: str, meeting_id: str, display_name: str = None, co_host: bool = None,
                       send_email: bool = None, panelist: bool = None, host_email: str = None) -> Invitee:
        """
        Invite a person to attend a meeting.
        Identify the invitee in the request body, by email address.

        :param email: Email address for meeting invitee.
        :type email: str
        :param meeting_id: Unique identifier for the meeting to which a person is being invited. This attribute only
            applies to meeting series and scheduled meeting. If it's a meeting series, the meeting invitee is invited
            to the entire meeting series; if it's a scheduled meeting, the meeting invitee is invited to this individual
            scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str

        :param display_name: Display name for meeting invitee. The maximum length of displayName is 128
            characters. In Webex App, if the email has been associated with an existing Webex account, the display
            name associated with the Webex account will be used; otherwise, the email will be used as displayName. In
            Webex site, if displayName is specified, it will show displayName. If displayName is not specified,
            and the email has been associated with an existing Webex account, the display name associated with the
            Webex account will be used; otherwise, the email will be used as displayName. Please note that if the
            invitee has an existing Webex account, the displayName shown in the meeting will be the displayName
            associated with the Webex account; otherwise, displayName shown in the meeting will be the displayName
            which is specified by the invitee who does not have a Webex account.

        :type display_name: str
        :param co_host: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate
            Hosts for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        """
        body = CreateMeetingInviteeBody()
        if email is not None:
            body.email = email
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if display_name is not None:
            body.display_name = display_name
        if co_host is not None:
            body.co_host = co_host
        if send_email is not None:
            body.send_email = send_email
        if panelist is not None:
            body.panelist = panelist
        if host_email is not None:
            body.host_email = host_email
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Invitee.parse_obj(data)

    def create_invitees(self, meeting_id: str, items: List[CreateInviteesItem],
                        host_email: str = None) -> List[Invitee]:
        """
        Invite people to attend a meeting in bulk.
        Identify each invitee by the email address of each item in the items of the request body.
        Each invitee should have a unique email.
        This API limits the maximum size of items in the request body to 100.

        :param meeting_id: Unique identifier for the meeting to which the people are being invited. This attribute
            only applies to meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are
            invited to the entire meeting series; if it's a scheduled meeting, the meeting invitees are invited to this
            individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        :param items: Meeting invitees to be inserted.
        :type items: CreateInviteesItem
        """
        body = CreateMeetingInviteesBody()
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if host_email is not None:
            body.host_email = host_email
        if items is not None:
            body.items = items
        url = self.ep('bulkInsert')
        data = super().post(url=url, data=body.json())
        return data["items"]

    def invitee_details(self, meeting_invitee_id: str, host_email: str = None) -> Invitee:
        """
        Retrieve details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee whose details are being requested.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for a meeting invitee that is hosted by that user.
        :type host_email: str
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_invitee_id}')
        data = super().get(url=url, params=params)
        return Invitee.parse_obj(data)

    def update(self, meeting_invitee_id: str, email: str, display_name: str = None, co_host: bool = None,
               send_email: bool = None, panelist: bool = None, host_email: str = None) -> Invitee:
        """
        Update details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee to be updated. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param email: Email address for meeting invitee.
        :type email: str
        :param display_name: Display name for meeting invitee. The maximum length of displayName is 128 characters.
            In Webex App, if the email has been associated with an existing Webex account, the display name associated
            with the Webex account will be used; otherwise, the email will be used as displayName. In Webex site,
            if displayName is specified, it will show displayName. If displayName is not specified, and the email has
            been associated with an existing Webex account, the display name associated with the Webex account will be
            used; otherwise, the email will be used as displayName.
            Please note that if the invitee has an existing Webex account, the displayName shown in the meeting will
            be the displayName associated with the Webex account; otherwise, displayName shown in the meeting will be
            the displayName which is specified by the invitee who does not have a Webex account.
        :type display_name: str
        :param co_host: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate
            Hosts for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        """
        body = UpdateMeetingInviteeBody()
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if co_host is not None:
            body.co_host = co_host
        if send_email is not None:
            body.send_email = send_email
        if panelist is not None:
            body.panelist = panelist
        if host_email is not None:
            body.host_email = host_email
        url = self.ep(f'{meeting_invitee_id}')
        data = super().put(url=url, data=body.json())
        return Invitee.parse_obj(data)

    def delete(self, meeting_invitee_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting invitee identified by a meetingInviteeId specified in the URI. The deleted meeting invitee
        cannot be recovered.
        If the meeting invitee is associated with a meeting series, the invitee will be removed from the entire
        meeting series. If the invitee is associated with a scheduled meeting, the invitee will be removed from only
        that scheduled meeting.

        :param meeting_invitee_id: Unique identifier for the invitee to be removed. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete a meeting invitee that is hosted by that user.
        :type host_email: str
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_invitee_id}')
        super().delete(url=url, params=params)
        return
