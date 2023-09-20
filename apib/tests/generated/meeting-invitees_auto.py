from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateInviteeObject', 'CreateInviteesItemObject', 'CreateInviteesObject', 'CreateInviteesResponse', 'GetInviteeObject', 'UpdateInviteeObject']


class UpdateInviteeObject(ApiModel):
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In the Webex app, if the email has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`. In a Webex site, if `displayName` is specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`.
    #: If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName` associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName` which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    displayName: Optional[str] = None
    #: Whether or not the invitee is a designated alternate host for the meeting. See [Add Alternate Hosts for Cisco Webex Meetings](https://help.webex.com/b5z6he/) for more details.
    coHost: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: brenda.song@example.com
    hostEmail: Optional[str] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    sendEmail: Optional[bool] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteeObject(ApiModel):
    #: Unique identifier for the meeting to which a person is being invited. This attribute only applies to meeting series and scheduled meeting. If it's a meeting series, the meeting invitee is invited to the entire meeting series; if it's a scheduled meeting, the meeting invitee is invited to this individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings) meeting is not supported for this API.
    #: example: 870f51ff287b41be84648412901e0402
    meetingId: Optional[str] = None
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In the Webex app, if the email has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`. In a Webex site, if `displayName` is specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`.
    #: If the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName` associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName` which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    displayName: Optional[str] = None
    #: Whether or not the invitee is a designated alternate host for the meeting. See [Add Alternate Hosts for Cisco Webex Meetings](https://help.webex.com/b5z6he/) for more details.
    coHost: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: brenda.song@example.com
    hostEmail: Optional[str] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    sendEmail: Optional[bool] = None
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
    displayName: Optional[str] = None
    #: Whether or not invitee is a designated alternate host for the meeting. See [Add Alternate Hosts for Cisco Webex Meetings](https://help.webex.com/b5z6he/) for more details.
    coHost: Optional[bool] = None
    #: Unique identifier for the meeting for which invitees are being requested. The meeting can be a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing.
    #: example: 870f51ff287b41be84648412901e0402
    meetingId: Optional[str] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteesItemObject(ApiModel):
    #: Email address for meeting invitee.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for meeting invitee. The maximum length of `displayName` is 128 characters. In Webex App, if the email has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`. In Webex site, if `displayName` is specified, it will show `displayName`. If `displayName` is not specified, and the `email` has been associated with an existing Webex account, the display name associated with the Webex account will be used; otherwise, the `email` will be used as `displayName`.
    #: Please note that if the invitee has an existing Webex account, the `displayName` shown in the meeting will be the `displayName` associated with the Webex account; otherwise, `displayName` shown in the meeting will be the `displayName` which is specified by the invitee who does not have a Webex account.
    #: example: John Andersen
    displayName: Optional[str] = None
    #: Whether or not invitee is a designated alternate host for the meeting. See [Add Alternate Hosts for Cisco Webex Meetings](https://help.webex.com/b5z6he/) for more details.
    coHost: Optional[bool] = None
    #: If `true`, send an email to the invitee.
    #: example: True
    sendEmail: Optional[bool] = None
    #: If `true`, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool] = None


class CreateInviteesObject(ApiModel):
    #: Unique identifier for the meeting to which the people are being invited. This attribute only applies to meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are invited to the entire meeting series; if it's a scheduled meeting, the meeting invitees are invited to this individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings) meeting is not supported for this API.
    #: example: 870f51ff287b41be84648412901e0402
    meetingId: Optional[str] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: brenda.song@example.com
    hostEmail: Optional[str] = None
    #: Meeting invitees to be inserted.
    items: Optional[list[CreateInviteesItemObject]] = None


class CreateInviteesResponse(ApiModel):
    #: Meeting invitees inserted.
    items: Optional[list[GetInviteeObject]] = None
