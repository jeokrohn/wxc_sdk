from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateInviteeObject', 'CreateInviteesItemObject', 'CreateInviteesObject', 'CreateInviteesResponse',
            'GetInviteeObject', 'UpdateInviteeObject']


class UpdateInviteeObject(ApiModel):
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In the Webex app, if
    #: the email has been associated with an existing Webex account, the display name associated with the Webex
    #: account will be used; otherwise, the `email` will be used as `displayName`. In a Webex site, if `displayName`
    #: is specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been
    #: associated with an existing Webex account, the display name associated with the Webex account will be used;
    #: otherwise, the `email` will be used as `displayName`.
    #: If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName`
    #: associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName`
    #: which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Whether or not the invitee is a designated alternate host for the meeting. See
    #: `Add Alternate Hosts for Cisco Webex Meetings
    #: <https://help.webex.com/b5z6he/>`_ for more details.
    co_host: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage
    #: to be the meeting host.
    #: example: brenda.song@example.com
    host_email: Optional[str] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    send_email: Optional[bool] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteeObject(ApiModel):
    #: Unique identifier for the meeting to which a person is being invited. This attribute only applies to meeting
    #: series and scheduled meeting. If it's a meeting series, the meeting invitee is invited to the entire meeting
    #: series; if it's a scheduled meeting, the meeting invitee is invited to this individual scheduled meeting. It
    #: doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is
    #: not supported for this API.
    #: example: 870f51ff287b41be84648412901e0402
    meeting_id: Optional[str] = None
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In the Webex app, if
    #: the email has been associated with an existing Webex account, the display name associated with the Webex
    #: account will be used; otherwise, the `email` will be used as `displayName`. In a Webex site, if `displayName`
    #: is specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been
    #: associated with an existing Webex account, the display name associated with the Webex account will be used;
    #: otherwise, the `email` will be used as `displayName`.
    #: If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName`
    #: associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName`
    #: which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Whether or not the invitee is a designated alternate host for the meeting. See
    #: `Add Alternate Hosts for Cisco Webex Meetings
    #: <https://help.webex.com/b5z6he/>`_ for more details.
    co_host: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage
    #: to be the meeting host.
    #: example: brenda.song@example.com
    host_email: Optional[str] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    send_email: Optional[bool] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class GetInviteeObject(ApiModel):
    #: Unique identifier for meeting invitee.
    #: example: 870f51ff287b41be84648412901e0402_2628962
    id: Optional[str] = None
    #: Email address for meeting invitee. This attribute can be modified by `Update a Meeting Invitee` API.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. This attribute can be modified by `Update a Meeting Invitee` API.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Whether or not invitee is a designated alternate host for the meeting. See
    #: `Add Alternate Hosts for Cisco Webex Meetings
    #: <https://help.webex.com/b5z6he/>`_ for more details.
    co_host: Optional[bool] = None
    #: Unique identifier for the meeting for which invitees are being requested. The meeting can be a meeting series, a
    #: scheduled meeting, or a meeting instance which has ended or is ongoing.
    #: example: 870f51ff287b41be84648412901e0402
    meeting_id: Optional[str] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteesItemObject(ApiModel):
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In Webex App, if the
    #: email has been associated with an existing Webex account, the display name associated with the Webex account
    #: will be used; otherwise, the `email` will be used as `displayName`. In Webex site, if `displayName` is
    #: specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been associated
    #: with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the
    #: `email` will be used as `displayName`.
    #: Please note that if the invitee has an existing Webex account, the `displayName` shown in the meeting will be
    #: the `displayName` associated with the Webex account; otherwise, `displayName` shown in the meeting will be the
    #: `displayName` which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Whether or not invitee is a designated alternate host for the meeting. See
    #: `Add Alternate Hosts for Cisco Webex Meetings
    #: <https://help.webex.com/b5z6he/>`_ for more details.
    co_host: Optional[bool] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    send_email: Optional[bool] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteesObject(ApiModel):
    #: Unique identifier for the meeting to which the people are being invited. This attribute only applies to meeting
    #: series and scheduled meetings. If it's a meeting series, the meeting invitees are invited to the entire meeting
    #: series; if it's a scheduled meeting, the meeting invitees are invited to this individual scheduled meeting. It
    #: doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is
    #: not supported for this API.
    #: example: 870f51ff287b41be84648412901e0402
    meeting_id: Optional[str] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage
    #: to be the meeting host.
    #: example: brenda.song@example.com
    host_email: Optional[str] = None
    #: Meeting invitees to be inserted.
    items: Optional[list[CreateInviteesItemObject]] = None


class CreateInviteesResponse(ApiModel):
    #: Meeting invitees inserted.
    items: Optional[list[GetInviteeObject]] = None


class MeetingInviteesApi(ApiChild, base='meetingInvitees'):
    """
    Meeting Invitees
    
    This API manages invitees' relationships to a meeting.
    
    You can use the Meeting Invitees API to list, create, update, and delete invitees.
    
    Refer to the `Meetings API Scopes` section of `Meetings Overview
    <https://developer.webex.com/docs/meetings>`_ for scopes required for each API.
    """

    def list_meeting_invitees(self, meeting_id: str, max_: int = None, host_email: str = None, panelist: str = None,
                              **params) -> Generator[GetInviteeObject, None, None]:
        """
        List Meeting Invitees

        Lists meeting invitees for a meeting with a specified `meetingId`. You can set a maximum number of invitees to
        return.
        
        This operation can be used for meeting series, scheduled meetings, and ended or ongoing meeting instance
        objects. If the specified `meetingId` is for a meeting series, the invitees for the series will be listed; if
        the `meetingId` is for a scheduled meeting, the invitees for the particular scheduled meeting will be listed;
        if the `meetingId` is for an ended or ongoing meeting instance, the invitees for the particular meeting
        instance will be listed. See the `Webex Meetings
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ guide for more information about the types of meetings.
        
        The list returned is sorted in ascending order by email address.
        
        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param meeting_id: Unique identifier for the meeting for which invitees are being requested. The meeting can be
            a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing. The meeting ID
            of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param max_: Limit the maximum number of meeting invitees in the response, up to 100.
        :type max_: int
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return meeting invitees that are hosted by that user.
        :type host_email: str
        :param panelist: Filter invitees or attendees for webinars only. If `true`, returns invitees. If `false`,
            returns attendees. If `null`, returns both invitees and attendees.
        :type panelist: str
        :return: Generator yielding :class:`GetInviteeObject` instances
        """
        ...


    def create_a_meeting_invitee(self, meeting_id: str, email: str, display_name: str, co_host: bool, host_email: str,
                                 send_email: bool, panelist: bool) -> GetInviteeObject:
        """
        Create a Meeting Invitee

        Invite a person to attend a meeting.
        
        Identify the invitee in the request body, by email address.

        :param meeting_id: Unique identifier for the meeting to which a person is being invited. This attribute only
            applies to meeting series and scheduled meeting. If it's a meeting series, the meeting invitee is invited
            to the entire meeting series; if it's a scheduled meeting, the meeting invitee is invited to this
            individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of
            a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param email: Email address for meeting invitee.
        :type email: str
        :param display_name: Display name for meeting invitee. The maximum length of `displayName` is 128 characters.
            In the Webex app, if the email has been associated with an existing Webex account, the display name
            associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`. In a
            Webex site, if `displayName` is specified, it will show `displayName`. If `displayName` is not specified,
            and the `email` has been associated with an existing Webex account, the display name associated with the
            Webex account will be used; otherwise, the `email` will be used as `displayName`.
        
        If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName`
        associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName`
        which is specified by the invitee who does not have a Webex account.
        :type display_name: str
        :param co_host: Whether or not the invitee is a designated alternate host for the meeting. See
            `Add Alternate Hosts for Cisco Webex Meetings
            <https://help.webex.com/b5z6he/>`_ for more details.
        :type co_host: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If `true`, send an email to the invitee.
        :type send_email: bool
        :param panelist: If `true`, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :rtype: :class:`GetInviteeObject`
        """
        ...


    def create_meeting_invitees(self, meeting_id: str, host_email: str,
                                items: list[CreateInviteesItemObject]) -> list[GetInviteeObject]:
        """
        Create Meeting Invitees

        Invite people to attend a meeting in bulk.
        
        Identify each invitee by the email address of each item in the `items` of the request body.
        
        Each invitee should have a unique `email`.
        
        This API limits the maximum size of `items` in the request body to 100.

        :param meeting_id: Unique identifier for the meeting to which the people are being invited. This attribute only
            applies to meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are
            invited to the entire meeting series; if it's a scheduled meeting, the meeting invitees are invited to
            this individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting
            ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param items: Meeting invitees to be inserted.
        :type items: list[CreateInviteesItemObject]
        :rtype: list[GetInviteeObject]
        """
        ...


    def get_a_meeting_invitee(self, meeting_invitee_id: str, host_email: str = None) -> GetInviteeObject:
        """
        Get a Meeting Invitee

        Retrieve details for a meeting invitee identified by a `meetingInviteeId` in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee whose details are being requested.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for a meeting invitee that is hosted by that user.
        :type host_email: str
        :rtype: :class:`GetInviteeObject`
        """
        ...


    def update_a_meeting_invitee(self, meeting_invitee_id: str, email: str, display_name: str, co_host: bool,
                                 host_email: str, send_email: bool, panelist: bool) -> GetInviteeObject:
        """
        Update a Meeting Invitee

        Update details for a meeting invitee identified by a `meetingInviteeId` in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee to be updated. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param email: Email address for meeting invitee.
        :type email: str
        :param display_name: Display name for meeting invitee. The maximum length of `displayName` is 128 characters.
            In the Webex app, if the email has been associated with an existing Webex account, the display name
            associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`. In a
            Webex site, if `displayName` is specified, it will show `displayName`. If `displayName` is not specified,
            and the `email` has been associated with an existing Webex account, the display name associated with the
            Webex account will be used; otherwise, the `email` will be used as `displayName`.
        
        If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName`
        associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName`
        which is specified by the invitee who does not have a Webex account.
        :type display_name: str
        :param co_host: Whether or not the invitee is a designated alternate host for the meeting. See
            `Add Alternate Hosts for Cisco Webex Meetings
            <https://help.webex.com/b5z6he/>`_ for more details.
        :type co_host: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If `true`, send an email to the invitee.
        :type send_email: bool
        :param panelist: If `true`, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :rtype: :class:`GetInviteeObject`
        """
        ...


    def delete_a_meeting_invitee(self, meeting_invitee_id: str, host_email: str = None, send_email: bool = None):
        """
        Delete a Meeting Invitee

        Removes a meeting invitee identified by a `meetingInviteeId` specified in the URI. The deleted meeting invitee
        cannot be recovered.
        
        If the meeting invitee is associated with a meeting series, the invitee will be removed from the entire meeting
        series. If the invitee is associated with a scheduled meeting, the invitee will be removed from only that
        scheduled meeting.

        :param meeting_invitee_id: Unique identifier for the invitee to be removed. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete a meeting invitee that is hosted by that user.
        :type host_email: str
        :param send_email: If `true`, send an email to the invitee.
        :type send_email: bool
        :rtype: None
        """
        ...

    ...