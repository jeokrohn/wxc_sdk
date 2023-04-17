from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['AnswerForCustomizedQuestion', 'AnswerObject', 'AnswerSummaryItem', 'Answers', 'AttendeePrivileges',
           'Audio', 'AudioConnectionOptions', 'AudioConnectionType', 'AudioType',
           'BatchRegisterMeetingRegistrantsResponse', 'BreakoutSessionObject', 'CallInNumbers', 'CallType',
           'ChatObject', 'ClosedCaptionObject', 'CoHosts', 'Condition', 'CreateInvitationSourcesResponse',
           'CreateInviteesItemObject', 'CreateMeetingBody', 'CreateMeetingInterpreterBody',
           'CreateMeetingInviteesResponse', 'CreateMeetingResponse', 'CreatePersonBody', 'CreateTrackingCodeBody',
           'CreateWebhookBody', 'CustomizedQuestionForCreateMeeting', 'CustomizedQuestionForGetMeeting',
           'CustomizedRegistrant', 'DefaultAudioType', 'DeleteTranscriptBody', 'Device', 'EntryAndExitTone', 'Event',
           'Format', 'GetBreakoutSessionObject', 'GetInviteeObject', 'GetMeetingControlStatusResponse',
           'GetMeetingPollResultsResponse', 'GetMeetingPreferenceDetailsResponse', 'GetMeetingQualitiesResponse',
           'GetMeetingSurveyResponse', 'GetMeetingTemplateResponse', 'GetPersonalMeetingRoomOptionsResponse',
           'GetRecordingDetailsResponse', 'GetRegistrationFormFormeetingResponse', 'GetSiteListResponse',
           'GetTrackingCodeItemForUserObject', 'GetTrackingCodeObject', 'GetUserTrackingCodesResponse',
           'GetVideoOptionsResponse', 'GetmeetingRegistrantsDetailInformationResponse', 'HostProfileCode',
           'InProgressDevice', 'InputMode', 'InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting',
           'InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting', 'InvitationSourceCreateObject',
           'InvitationSourceObject', 'InviteeObjectForCreateMeeting', 'JoinMeetingResponse', 'Link', 'Links',
           'ListAnswersOfQuestionResponse', 'ListInvitationSourcesResponse', 'ListMeetingAttendeeReportsResponse',
           'ListMeetingBreakoutSessionsResponse', 'ListMeetingChatsResponse',
           'ListMeetingClosedCaptionSnippetsResponse', 'ListMeetingClosedCaptionsResponse',
           'ListMeetingInterpretersResponse', 'ListMeetingInviteesResponse', 'ListMeetingParticipantsResponse',
           'ListMeetingPollsResponse', 'ListMeetingQAndAResponse', 'ListMeetingRegistrantsResponse',
           'ListMeetingSessionTypesResponse', 'ListMeetingSurveyResultsResponse', 'ListMeetingTemplatesResponse',
           'ListMeetingTrackingCodesResponse', 'ListMeetingTranscriptsForComplianceOfficerResponse',
           'ListMeetingTranscriptsResponse', 'ListMeetingUsageReportsResponse', 'ListMeetingsOfMeetingSeriesResponse',
           'ListMeetingsResponse', 'ListPeopleResponse', 'ListRecordingsForAdminOrComplianceOfficerResponse',
           'ListRecordingsResponse', 'ListRespondentsOfQuestionResponse', 'ListSiteSessionTypesResponse',
           'ListSnippetsOfMeetingTranscriptResponse', 'ListTrackingCodesResponse', 'ListUserSessionTypeResponse',
           'ListWebhooksResponse', 'MediaSessionQuality', 'MeetingAttendeeReportObject', 'MeetingChatsApi',
           'MeetingClosedCaptionsApi', 'MeetingInviteesApi', 'MeetingMessagesApi', 'MeetingOptions',
           'MeetingParticipantsApi', 'MeetingPollsApi', 'MeetingPreferencesApi', 'MeetingQandAApi',
           'MeetingQualitiesApi', 'MeetingSeriesObjectForListMeeting', 'MeetingSessionTypeObject',
           'MeetingTranscriptsApi', 'MeetingType', 'MeetingUsageReportObject', 'MeetingsApi',
           'MeetingsSummaryReportApi', 'MoveRecordingsIntoRecycleBinBody', 'NetworkType', 'NoteType', 'OfficeNumber',
           'Option', 'Options', 'OptionsForTrackingCodeObject', 'OrderBy', 'OrderType', 'Participant',
           'ParticipantType', 'PatchMeetingBody', 'PatchMeetingResponse', 'PeopleApi', 'Person', 'PersonalMeetingRoom',
           'PhoneNumbers', 'Poll', 'PollResult', 'QAObject', 'QueryMeetingParticipantsWithEmailResponse',
           'QueryMeetingRegistrantsResponse', 'Question', 'Question1', 'QuestionObject', 'QuestionResult',
           'QuestionWithAnswersObject', 'RecordingObject', 'RecordingsApi', 'RegisterMeetingRegistrantBody',
           'RegisterMeetingRegistrantResponse', 'Registration', 'Registration1', 'Resource', 'Resources', 'Respondent',
           'RespondentsReferenceLinks', 'Result', 'Rules', 'ScheduleStartCodeObject', 'ScheduledMeetingObject',
           'ScheduledType', 'SchedulingOptionsObject', 'Sender', 'Service', 'ServiceType', 'SessionType',
           'SessionTypesApi', 'SimultaneousInterpretation', 'SimultaneousInterpretation1', 'SipAddressesType',
           'SiteSessionType', 'Sites', 'SnippetObject', 'SnippetObject1', 'StandardRegistrationApproveRule', 'State',
           'State3', 'State4', 'Status', 'Status16', 'Status2', 'Status8', 'SurveyResultObject', 'Telephony',
           'Telephony6', 'TemplateObject', 'TemplateType', 'TemporaryDirectDownloadLinks',
           'TrackingCodeItemForCreateMeetingObject', 'TrackingCodesApi', 'TranscriptObject', 'TransportType', 'Type',
           'Type11', 'Type13', 'Type14', 'Type19', 'Type2', 'Type6', 'UnlockedMeetingJoinSecurity',
           'UpdateMeetingBreakoutSessionsResponse', 'UpdateParticipantResponse',
           'UpdatePersonalMeetingRoomOptionsBody', 'UpdateVideoOptionsResponse', 'UserSessionTypes', 'Video', 'Video4',
           'VideoDevices', 'VideoIn', 'Webhook', 'WebhooksApi']


class CoHosts(ApiModel):
    #: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room Options API.
    #: Possible values: john.andersen@example.com
    email: Optional[str]
    #: Display name for cohost. This attribute can be modified with the Update Personal Meeting Room Options API.
    #: Possible values: John Andersen
    display_name: Optional[str]


class Sender(CoHosts):
    #: A unique identifier for the sender.
    person_id: Optional[str]
    #: The ID of the organization to which the sender belongs.
    org_id: Optional[str]


class ChatObject(ApiModel):
    #: A unique identifier for the chat snippet.
    id: Optional[str]
    #: Chat time for the chat snippet in ISO 8601 compliant format.
    chat_time: Optional[str]
    #: The text of the chat snippet.
    text: Optional[str]
    #: A unique identifier for the meeting instance to which the chat belongs.
    meeting_id: Optional[str]
    #: Whether the type of the chat is private, public or group. Private chat is for the 1:1 chat. Public chat is for
    #: the message which is sent to all the people in the meeting. Group chat is for the message which is sent to a
    #: small group of people, like a message to "host and presenter".
    type: Optional[str]
    #: Information of the sender of the chat snippet.
    sender: Optional[Sender]
    #: Information of the receivers of the chat snippet.
    receivers: Optional[list[Sender]]


class ListMeetingChatsResponse(ApiModel):
    #: Chat array
    items: Optional[list[ChatObject]]


class MeetingChatsApi(ApiChild, base='meetings/postMeetingChats'):
    """
    Chats are content captured in a meeting when chat messages are sent between the participants within a meeting. This
    feature allows a Compliance Officer to access the in-meeting chat content.
    The Compliance Officer can use the Meeting Chats API to retrieve the chats of a meeting and to delete all chats
    associated with a meeting. private chats are text messages between two people. group chats are for larger breakout
    spaces. Meeting chats are different from room messages in that there is no catch-up propagation. For example, if a
    user joins a meeting late only, chat messages that are created from then on, will be propagated to this user. To
    understand which user saw which message if they joined late, you have to query the meetingParticipants REST
    resource for the joined/left times and compare to the meetingsChat chatTime field.
    The Webex meetings chat functionality and API endpoint described here is "upon-request" and not enabled by default.
    If you need it enabled for your org, or if you need help, please contact the Webex Developer Support team at
    devsupport@webex.com.
    """

    def list_chats(self, meeting_id: str, offset: int = None, **params) -> Generator[ChatObject, None, None]:
        """
        Lists the meeting chats of a finished meeting instance specified by meetingId. You can set a maximum number of
        chats to return.
        Use this operation to list the chats of a finished meeting instance when they are ready. Please note that only
        meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and
        in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. The meeting ID of a
            scheduled personal room meeting is not supported.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int

        documentation: https://developer.webex.com/docs/api/v1/meeting-chats/list-meeting-chats
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ChatObject, params=params)

    def delete_chats(self, meeting_id: str):
        """
        Deletes the meeting chats of a finished meeting instance specified by meetingId.
        Use this operation to delete the chats of a finished meeting instance when they are ready. Please note that
        only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and
        in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. Meeting IDs of a
            scheduled personal room meeting are not supported.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-chats/delete-meeting-chats
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        super().delete(url=url, params=params)
        return

class ClosedCaptionObject(ApiModel):
    #: A unique identifier for the closed caption.
    id: Optional[str]
    #: Unique identifier for the meeting instance which the closed captions belong to.
    meeting_id: Optional[str]
    #: The download link for the closed caption vtt file.
    vtt_download_link: Optional[str]
    #: The download link for the closed caption txt file.
    txt_download_link: Optional[str]
    #: Start time for the meeting closed caption in ISO 8601 compliant format.
    start: Optional[str]


class SnippetObject1(ApiModel):
    #: A unique identifier for the snippet.
    id: Optional[str]
    #: Text for the snippet.
    text: Optional[str]
    #: Name of the person generating the speech for the snippet.
    person_name: Optional[str]
    #: Email address of the person generating the speech for the snippet.
    person_email: Optional[str]
    #: Offset from the beginning of the parent transcript in milliseconds indicating the start time of the snippet.
    offset_millisecond: Optional[int]
    #: Duration of the snippet in milliseconds.
    duration_millisecond: Optional[int]


class SnippetObject(SnippetObject1):
    #: Unique identifier for the meeting instance which the closed captions belong to.
    meeting_id: Optional[str]
    #: The unique identifier for the person speaking.
    people_id: Optional[str]
    #: Start time for the snippet.
    start: Optional[str]
    #: Original language of the snippet.
    language: Optional[str]


class ListMeetingClosedCaptionsResponse(ApiModel):
    #: Closed caption array
    items: Optional[list[ClosedCaptionObject]]


class ListMeetingClosedCaptionSnippetsResponse(ApiModel):
    #: Closed caption snippet array
    items: Optional[list[SnippetObject]]


class MeetingClosedCaptionsApi(ApiChild, base='meetingClosedCaptions'):
    """
    Meeting Closed Captions APIs are enabled upon request, and are not available by default. Please contact the Webex
    Developer Support team at devsupport@webex.com if you would like to enable this feature for your organization.
    Meeting closed captions are the automatic transcriptions of what is being said during a meeting in real-time.
    Closed captions appear after being enabled during a meeting and can be translated to a participant's language.
    A closed caption snippet is a short text snippet from a meeting closed caption which was spoken by a particular
    participant in the meeting. A meeting's closed captions consists of many snippets.
    The Closed Captions API manages meeting closed captions and snippets. You can list meeting closed captions, as well
    as list and download snippets. Closed captions can be retrieved in either Web Video Text Tracks (VTT) or plain text
    (TXT) format via the download links provided by the vttDownloadLink and txtDownloadlink response properties,
    respectively.
    Refer to the Meetings API Scopes section of Meetings Overview guide for the scopes required for each API.
    Notes:
    Currently, closed caption APIs are only supported for the Compliance Officer role.
    Closed captions will be available 15 minutes after the meeting is finished.
    """

    def list_closed_captions(self, meeting_id: str) -> list[ClosedCaptionObject]:
        """
        Lists closed captions of a finished meeting instance specified by meetingId.

        :param meeting_id: Unique identifier for the meeting instance which the closed captions belong to. This
            parameter only applies to ended meeting instnaces. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-closed-captions/list-meeting-closed-captions
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        data = super().get(url=url, params=params)
        return parse_obj_as(list[ClosedCaptionObject], data["items"])

    def list_closed_caption_snippets(self, closed_caption_id: str, meeting_id: str) -> list[SnippetObject]:
        """
        Lists snippets of a meeting closed caption specified by closedCaptionId.

        :param closed_caption_id: Unique identifier for the meeting closed caption which the snippets belong to.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-closed-captions/list-meeting-closed-caption-snippets
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/snippets')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[SnippetObject], data["items"])

    def download_closed_caption_snippets(self, closed_caption_id: str, meeting_id: str, format: str = None):
        """
        Download meeting closed caption snippets from the meeting closed caption specified by closedCaptionId formatted
        either as a Video Text Track (.vtt) file or plain text (.txt) file.

        :param closed_caption_id: Unique identifier for the meeting closed caption.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to meeting instances in the ended state. It does not apply to meeting series,
            scheduled meetings or scheduled personal room meetings.
        :type meeting_id: str
        :param format: Format for the downloaded meeting closed caption snippets. Possible values: vtt, txt
        :type format: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-closed-captions/download-meeting-closed-caption-snippets
        """
        params = {}
        params['meetingId'] = meeting_id
        if format is not None:
            params['format'] = format
        url = self.ep(f'{closed_caption_id}/download')
        super().get(url=url, params=params)
        return $!$!$!   # this is weird. Check the spec at https://developer.webex.com/docs/api/v1/meeting-closed-captions/download-meeting-closed-caption-snippets

class GetInviteeObject(CoHosts):
    #: Unique identifier for meeting invitee.
    id: Optional[str]
    #: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate Hosts for Cisco Webex
    #: Meetings for more details.
    co_host: Optional[bool]
    #: Unique identifier for the meeting for which invitees are being requested. The meeting can be a meeting series, a
    #: scheduled meeting, or a meeting instance which has ended or is ongoing.
    meeting_id: Optional[str]
    #: If true, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool]


class CreateInviteesItemObject(CoHosts):
    #: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate Hosts for Cisco Webex
    #: Meetings for more details.
    co_host: Optional[bool]
    #: If true, send an email to the invitee.
    send_email: Optional[bool]
    #: If true, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool]


class ListMeetingInviteesResponse(ApiModel):
    #: Array of meeting invitees.
    items: Optional[list[GetInviteeObject]]


class CreateMeetingInviteeBody(CoHosts):
    #: Unique identifier for the meeting to which a person is being invited. This attribute only applies to meeting
    #: series and scheduled meeting. If it's a meeting series, the meeting invitee is invited to the entire meeting
    #: series; if it's a scheduled meeting, the meeting invitee is invited to this individual scheduled meeting. It
    #: doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled personal room meeting is
    #: not supported for this API.
    meeting_id: Optional[str]
    #: Whether or not the invitee is a designated alternate host for the meeting. See Add Alternate Hosts for Cisco
    #: Webex Meetings for more details.
    co_host: Optional[bool]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]
    #: If true, send an email to the invitee.
    send_email: Optional[bool]
    #: If true, the invitee is a designated panelist for the event meeting.
    panelist: Optional[bool]


class CreateMeetingInviteesBody(ApiModel):
    #: Unique identifier for the meeting to which the people are being invited. This attribute only applies to meeting
    #: series and scheduled meetings. If it's a meeting series, the meeting invitees are invited to the entire meeting
    #: series; if it's a scheduled meeting, the meeting invitees are invited to this individual scheduled meeting. It
    #: doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled personal room meeting is
    #: not supported for this API.
    meeting_id: Optional[str]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]
    #: Meeting invitees to be inserted.
    items: Optional[list[CreateInviteesItemObject]]


class CreateMeetingInviteesResponse(ApiModel):
    #: Meeting invitees inserted.
    items: Optional[list[GetInviteeObject]]


class UpdateMeetingInviteeBody(CreateInviteesItemObject):
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]


class MeetingInviteesApi(ApiChild, base='meetingInvitees'):
    """
    This API manages invitees' relationships to a meeting.
    You can use the Meeting Invitees API to list, create, update, and delete invitees.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_invitees(self, meeting_id: str, host_email: str = None, panelist: str = None, **params) -> Generator[GetInviteeObject, None, None]:
        """
        Lists meeting invitees for a meeting with a specified meetingId. You can set a maximum number of invitees to
        return.
        This operation can be used for meeting series, scheduled meetings, and ended or ongoing meeting instance
        objects. If the specified meetingId is for a meeting series, the invitees for the series will be listed; if the
        meetingId is for a scheduled meeting, the invitees for the particular scheduled meeting will be listed; if the
        meetingId is for an ended or ongoing meeting instance, the invitees for the particular meeting instance will be
        listed. See the Webex Meetings guide for more information about the types of meetings.
        The list returned is sorted in ascending order by email address.
        Long result sets are split into pages.

        :param meeting_id: Unique identifier for the meeting for which invitees are being requested. The meeting can be
            a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing. The meeting ID
            of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return meeting invitees that are hosted by that user.
        :type host_email: str
        :param panelist: Filter invitees or attendees for webinars only. If true, returns invitees. If false, returns
            attendees. If null, returns both invitees and attendees.
        :type panelist: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/list-meeting-invitees
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if panelist is not None:
            params['panelist'] = panelist
        url = self.ep()
        return self.session.follow_pagination(url=url, model=GetInviteeObject, params=params)

    def create_invitee(self, meeting_id: str, email: str = None, display_name: str = None, co_host: bool = None, host_email: str = None, send_email: bool = None, panelist: bool = None) -> GetInviteeObject:
        """
        Invite a person to attend a meeting.
        Identify the invitee in the request body, by email address.

        :param meeting_id: Unique identifier for the meeting to which a person is being invited. This attribute only
            applies to meeting series and scheduled meeting. If it's a meeting series, the meeting invitee is invited
            to the entire meeting series; if it's a scheduled meeting, the meeting invitee is invited to this
            individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param email: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room
            Options API. Possible values: john.andersen@example.com
        :type email: str
        :param display_name: Display name for cohost. This attribute can be modified with the Update Personal Meeting
            Room Options API. Possible values: John Andersen
        :type display_name: str
        :param co_host: Whether or not the invitee is a designated alternate host for the meeting. See Add Alternate
            Hosts for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/create-a-meeting-invitee
        """
        body = CreateMeetingInviteeBody()
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if co_host is not None:
            body.co_host = co_host
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        if panelist is not None:
            body.panelist = panelist
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return GetInviteeObject.parse_obj(data)

    def create_invitees(self, meeting_id: str, host_email: str = None, items: CreateInviteesItemObject = None) -> list[GetInviteeObject]:
        """
        Invite people to attend a meeting in bulk.
        Identify each invitee by the email address of each item in the items of the request body.
        Each invitee should have a unique email.
        This API limits the maximum size of items in the request body to 100.

        :param meeting_id: Unique identifier for the meeting to which the people are being invited. This attribute only
            applies to meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are
            invited to the entire meeting series; if it's a scheduled meeting, the meeting invitees are invited to this
            individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param items: Meeting invitees to be inserted.
        :type items: CreateInviteesItemObject

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/create-meeting-invitees
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
        return parse_obj_as(list[GetInviteeObject], data["items"])

    def invitee(self, meeting_invitee_id: str, host_email: str = None) -> GetInviteeObject:
        """
        Retrieve details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee whose details are being requested.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for a meeting invitee that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/get-a-meeting-invitee
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_invitee_id}')
        data = super().get(url=url, params=params)
        return GetInviteeObject.parse_obj(data)

    def update_invitee(self, meeting_invitee_id: str, email: str = None, display_name: str = None, co_host: bool = None, send_email: bool = None, panelist: bool = None, host_email: str = None) -> GetInviteeObject:
        """
        Update details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee to be updated. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param email: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room
            Options API. Possible values: john.andersen@example.com
        :type email: str
        :param display_name: Display name for cohost. This attribute can be modified with the Update Personal Meeting
            Room Options API. Possible values: John Andersen
        :type display_name: str
        :param co_host: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate Hosts
            for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/update-a-meeting-invitee
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
        return GetInviteeObject.parse_obj(data)

    def delete_invitee(self, meeting_invitee_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting invitee identified by a meetingInviteeId specified in the URI. The deleted meeting invitee
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
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meeting-invitees/delete-a-meeting-invitee
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_invitee_id}')
        super().delete(url=url, params=params)
        return

class MeetingMessagesApi(ApiChild, base='meeting/messages/'):
    """
    Meeting Messages are how we communicate through text within an active unified meeting
    Meeting Messages are also how we communicate through text within a space bound meeting.
    In a Webex meeting, each meeting message is displayed on its own line along with a timestamp and sender
    information.
    Message can contain plain text and rich text
    """

    def delete_meeting_message(self, meeting_message_id: str):
        """
        Deletes a Meeting Message from the In Meeting Chat, using its ID.
        This ID can be retrieved by a Compliance Officer using the events API filtering on the meetingMessages resource
        type.
        Specify the meetingMessage ID in the meetingMessageId parameter in the URI.

        :param meeting_message_id: The unique identifier for the message.
        :type meeting_message_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-messages/delete-a-meeting-message
        """
        url = self.ep(f'{meeting_message_id}')
        super().delete(url=url)
        return

class Video(str, Enum):
    #: The video is turned on.
    on = 'on'
    #: The video is turned off.
    off = 'off'


class State3(str, Enum):
    #: The participant is waiting in the meeting lobby.
    lobby = 'lobby'
    #: The participant has joined the meeting.
    joined = 'joined'


class State(State3):
    #: The participant has left the meeting.
    end = 'end'


class CallType(str, Enum):
    #: Connect audio by dialing a toll or toll-free phone number provided by the meeting.
    call_in = 'callIn'
    #: Connect audio by dialing out a phone number from the meeting.
    call_back = 'callBack'


class AudioType(str, Enum):
    #: PSTN
    pstn = 'pstn'
    #: VoIP
    voip = 'voip'
    #: The participant is not connected to audio.
    inactive = 'inactive'


class InProgressDevice(ApiModel):
    #: An internal ID that is associated with each join.
    correlation_id: Optional[str]
    #: The type of device.
    device_type: Optional[str]
    #: The audio type that the participant is using.
    audio_type: Optional[AudioType]
    #: The time the device joined the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the joinedTime will be filled in after the meeting ended. If you need real-time
    #: joined events, please refer to the webhooks guide.
    joined_time: Optional[str]
    #: The time the device left the meeting, leftTime is the exact moment when a specific device left the meeting. If
    #: the field is non-existent or shows 1970-01-01T00:00:00.000Z the meeting may be still ongoing and the leftTime
    #: will be filled in after the meeting ended. If you need real-time left events, please refer to the webhooks
    #: guide.
    left_time: Optional[str]


class Device(InProgressDevice):
    #: The duration in seconds the device stayed in the meeting.
    duration_second: Optional[int]
    #: The PSTN call type in which the device joined the meeting.
    call_type: Optional[CallType]
    #: The PSTN phone number from which the device joined the meeting. Only compliance officer can retrieve the
    #: phoneNumber. The meeting host and admin users cannot retrieve it. NOTE: The phoneNumber will be returned after
    #: the meeting ends; it is not returned while the meeting is in progress.
    phone_number: Optional[str]


class Participant(CoHosts):
    #: The ID that identifies the meeting and the participant.
    id: Optional[str]
    #: The ID that identifies the organization. It only applies to participants of ongoing meetings.
    org_id: Optional[str]
    #: Whether or not the participant is the host of the meeting.
    host: Optional[bool]
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool]
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool]
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool]
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool]
    #: The status of the participant's video.
    video: Optional[Video]
    #: The status of the participant in the meeting.
    state: Optional[State]
    #: The time the participant joined the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the joinedTime will be filled in after the meeting ended. If you need real-time
    #: join events, please refer to the webhooks guide.
    joined_time: Optional[str]
    #: The time the participant left the meeting. If the field is non-existent or shows 1970-01-01T00:00:00.000Z the
    #: meeting may be still ongoing and the leftTime will be filled in after the meeting ended. If you need real-time
    #: left events, please refer to the webhooks guide.
    left_time: Optional[str]
    #: The site URL.
    site_url: Optional[str]
    #: A unique identifier for the meeting which the participant belongs to.
    meeting_id: Optional[str]
    #: The email address of the host.
    host_email: Optional[str]
    devices: Optional[list[Device]]
    #: The source ID of the participant. The sourceId is from the Create Invitation Sources API.
    source_id: Optional[str]


class ListMeetingParticipantsResponse(ApiModel):
    items: Optional[list[Participant]]


class QueryMeetingParticipantsWithEmailBody(ApiModel):
    #: Participants email list
    #: Possible values: a@example.com
    emails: Optional[list[str]]


class QueryMeetingParticipantsWithEmailResponse(ApiModel):
    items: Optional[list[Participant]]


class UpdateParticipantBody(ApiModel):
    #: The value is true or false, and means to mute or unmute the audio of a participant.
    muted: Optional[bool]
    #: The value can be true or false. The value of true is to admit a participant to the meeting if the participant is
    #: in the lobby, No-Op if the participant is not in the lobby or when the value is set to false.
    admit: Optional[bool]
    #: The attribute is exclusive and its value can be true or false. The value of true means that the participant will
    #: be expelled from the meeting, the value of false means No-Op.
    expel: Optional[bool]


class UpdateParticipantResponse(CoHosts):
    #: The participant ID that identifies the meeting and the participant.
    id: Optional[str]
    #: The ID that identifies the organization.
    org_id: Optional[str]
    #: Whether or not the participant is the host of the meeting.
    host: Optional[bool]
    #: Whether or not the participant has host privilege in the meeting.
    co_host: Optional[bool]
    #: Whether or not the participant is the team space moderator. This field returns only if the meeting is associated
    #: with a Webex space.
    space_moderator: Optional[bool]
    #: Whether or not the participant is invited to the meeting.
    invitee: Optional[bool]
    #: The status of the participant's video.
    video: Optional[Video]
    #: Whether or not the participant's audio is muted.
    muted: Optional[bool]
    #: The status of the participant in the meeting.
    state: Optional[State3]
    #: The site URL.
    site_url: Optional[str]
    #: A unique identifier for the meeting which the participant belongs to.
    meeting_id: Optional[str]
    #: The email address of the host.
    host_email: Optional[str]
    devices: Optional[list[InProgressDevice]]


class AdmitParticipantsBody(ApiModel):
    #: The ID that identifies the meeting participant.
    items: Optional[list[ParticipantID]]


class MeetingParticipantsApi(ApiChild, base='meetingParticipants'):
    """
    This API manages meeting participants.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_participants(self, meeting_id: str, host_email: str = None, join_time_from: str = None, join_time_to: str = None, **params) -> Generator[Participant, None, None]:
        """
        List all participants in a live or post meeting. The meetingId parameter is required, which is the unique
        identifier for the meeting.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-participants/list-meeting-participants
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Participant, params=params)

    def query_participants_with_email(self, meeting_id: str, host_email: str = None, join_time_from: str = None, join_time_to: str = None, emails: List[str] = None, **params) -> Generator[Participant, None, None]:
        """
        Query participants in a live meeting, or after the meeting, using participant's email. The meetingId parameter
        is the unique identifier for the meeting and is required.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        :param emails: Participants email list Possible values: a@example.com
        :type emails: List[str]

        documentation: https://developer.webex.com/docs/api/v1/meeting-participants/query-meeting-participants-with-email
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        body = QueryMeetingParticipantsWithEmailBody()
        if emails is not None:
            body.emails = emails
        url = self.ep('query')
        return self.session.follow_pagination(url=url, model=Participant, params=params, data=body.json())

    def participant_details(self, participant_id: str, host_email: str = None) -> Participant:
        """
        Get a meeting participant details of a live or post meeting. The participantId is required to identify the
        meeting and the participant.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-participants/get-meeting-participant-details
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{participant_id}')
        data = super().get(url=url, params=params)
        return Participant.parse_obj(data)

    def update_participant(self, participant_id: str, muted: bool = None, admit: bool = None, expel: bool = None) -> UpdateParticipantResponse:
        """
        To mute, un-mute, expel, or admit a participant in a live meeting. The participantId is required to identify
        the meeting and the participant.
        Notes:

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param muted: The value is true or false, and means to mute or unmute the audio of a participant.
        :type muted: bool
        :param admit: The value can be true or false. The value of true is to admit a participant to the meeting if the
            participant is in the lobby, No-Op if the participant is not in the lobby or when the value is set to
            false.
        :type admit: bool
        :param expel: The attribute is exclusive and its value can be true or false. The value of true means that the
            participant will be expelled from the meeting, the value of false means No-Op.
        :type expel: bool

        documentation: https://developer.webex.com/docs/api/v1/meeting-participants/update-a-participant
        """
        body = UpdateParticipantBody()
        if muted is not None:
            body.muted = muted
        if admit is not None:
            body.admit = admit
        if expel is not None:
            body.expel = expel
        url = self.ep(f'{participant_id}')
        data = super().put(url=url, data=body.json())
        return UpdateParticipantResponse.parse_obj(data)

    def admit_participants(self, items: List[ParticipantID] = None):
        """
        To admit participants into a live meeting in bulk.
        This API limits the maximum size of items in the request body to 100.
        Each participantId of items in the request body should have the same prefix of meetingId.

        :param items: The ID that identifies the meeting participant.
        :type items: List[ParticipantID]

        documentation: https://developer.webex.com/docs/api/v1/meeting-participants/admit-participants
        """
        body = AdmitParticipantsBody()
        if items is not None:
            body.items = items
        url = self.ep('admit')
        super().post(url=url, data=body.json())
        return

class Type(str, Enum):
    #: A single-answer question.
    single = 'single'
    #: A multiple-answer question.
    multiple = 'multiple'
    #: A text answer.
    short = 'short'


class Option(ApiModel):
    #: The order of the option.
    order: Optional[str]
    #: The value of the option.
    value: Optional[str]
    #: Whether or not the option is correct.
    is_correct: Optional[bool]


class Question(ApiModel):
    #: A unique identifier for the question.
    id: Optional[str]
    #: The order of the question.
    order: Optional[str]
    #: The question.
    title: Optional[str]
    #: The type of the question.
    type: Optional[Type]
    #: Question's options.
    options: Optional[list[Option]]


class Poll(CoHosts):
    #: A unique identifier for the poll.
    id: Optional[str]
    #: A unique identifier for the meeting instance to which the poll belongs.
    meeting_id: Optional[str]
    #: The date and time the poll started in ISO 8601 compliant format.
    start_time: Optional[str]
    #: The date and time the poll ended in ISO 8601 compliant format.
    end_time: Optional[str]
    #: The length of time in the alarm box, in seconds.
    timer_duration: Optional[int]
    #: The ID of the polling coordinator.
    person_id: Optional[str]
    #: Poll's questions.
    questions: Optional[list[Question]]


class AnswerSummaryItem(Option):
    #: The total number of people who selected this answer.
    total_respondents: Optional[int]


class Link(ApiModel):
    #: Link to the previous question's respondents.
    prev: Optional[str]
    #: Link to the current question's respondents.
    self: Optional[str]
    #: Link to the next page question's respondents.
    next: Optional[str]


class Respondent(CoHosts):
    #: An array of answers. If it is a single-answer question or text answer, there is at most one; if it is a
    #: multiple-answer question, there may be more than one.
    answers: Optional[list[str]]


class RespondentsReferenceLinks(ApiModel):
    #: The pagination links of this question's respondent.
    links: Optional[Link]
    #: An array of answers.
    items: Optional[list[Respondent]]


class QuestionResult(ApiModel):
    #: A unique identifier of the question.
    id: Optional[str]
    #: The order of the question in the poll.
    order: Optional[str]
    #: The question.
    title: Optional[str]
    #: The type of the question.
    type: Optional[Type]
    #: Summary of all answers.
    answer_summary: Optional[list[AnswerSummaryItem]]
    #: Question's respondents.
    respondents: Optional[RespondentsReferenceLinks]


class PollResult(CoHosts):
    #: A unique identifier for the poll.
    id: Optional[str]
    #: A unique identifier for the meeting instance to which the poll belongs.
    meeting_id: Optional[str]
    #: The total number of attendees in the meeting.
    total_attendees: Optional[int]
    #: The total number of respondents in the poll.
    total_respondents: Optional[int]
    #: The date and time the poll started in ISO 8601 compliant format.
    start_time: Optional[str]
    #: The date and time the poll ended in ISO 8601 compliant format.
    end_time: Optional[str]
    #: The duration of the poll, in seconds.
    timer_duration: Optional[int]
    #: The ID of the the poll coordinator.
    person_id: Optional[str]
    #: An array of questions in this poll.
    questions: Optional[list[QuestionResult]]


class ListMeetingPollsResponse(ApiModel):
    items: Optional[list[Poll]]


class GetMeetingPollResultsResponse(ApiModel):
    items: Optional[list[PollResult]]


class ListRespondentsOfQuestionResponse(ApiModel):
    items: Optional[list[Respondent]]


class MeetingPollsApi(ApiChild, base='meetings/poll'):
    """
    As a presenter, you can use a poll to create and share questionnaires. Polls can be useful for gathering feedback,
    taking votes, or testing knowledge.
    You can use the Meeting Poll API to list meeting polls, the poll's questions, and answers.
    Currently, these APIs are available to users with one of the meeting host, admin or Compliance Officer roles.
    The Webex meetings poll functionality and API endpoint described here is "upon-request" and not enabled by default.
    If you need it enabled for your org, or if you need help, please contact the Webex Developer Support team at
    devsupport@webex.com.
    """

    def list_meeting_polls(self, meeting_id: str) -> list[Poll]:
        """
        Lists all the polls and the poll questions in a meeting when ready.

        :param meeting_id: A unique identifier for the meeting instance to which the polls belong.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-polls/list-meeting-polls
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep('s')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Poll], data["items"])

    def meeting_poll_results(self, meeting_id: str, **params) -> Generator[PollResult, None, None]:
        """
        List the meeting polls, the poll's questions, and answers from the meeting when ready.

        :param meeting_id: A unique identifier for the meeting instance to which the polls belong.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-polls/get-meeting-pollresults
        """
        params['meetingId'] = meeting_id
        url = self.ep('Results')
        return self.session.follow_pagination(url=url, model=PollResult, params=params)

    def list_respondents_of_question(self, poll_id: str, question_id: str, meeting_id: str, **params) -> Generator[Respondent, None, None]:
        """
        Lists the respondents to a specific questions in a poll.

        :param poll_id: A unique identifier for the poll to which the respondents belong.
        :type poll_id: str
        :param question_id: A unique identifier for the question to which the respondents belong.
        :type question_id: str
        :param meeting_id: A unique identifier for the meeting instance to which the respondents belong.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-polls/list-respondents-of-a-question
        """
        params['meetingId'] = meeting_id
        url = self.ep(f's/{poll_id}/questions/{question_id}/respondents')
        return self.session.follow_pagination(url=url, model=Respondent, params=params)

class CallInNumbers(ApiModel):
    #: Label for call-in number.
    #: Possible values: Call-in toll-free number (US/Canada)
    label: Optional[str]
    #: Call-in number to join teleconference from a phone.
    #: Possible values: 123456789
    call_in_number: Optional[str]
    #: Type of toll for the call-in number.
    #: Possible values: toll, tollFree
    toll_type: Optional[str]


class Links(ApiModel):
    #: Link relation describing how the target resource is related to the current context (conforming with RFC5998).
    rel: Optional[str]
    #: Target resource URI (conforming with RFC5998).
    href: Optional[str]
    #: Target resource method (conforming with RFC5998).
    method: Optional[str]


class Telephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumbers]]
    #: HATEOAS information of global call-in numbers for joining teleconference from a phone.
    links: Optional[Links]


class PersonalMeetingRoom(ApiModel):
    #: Personal Meeting Room topic. The length of topic must be between 1 and 128 characters. This attribute can be
    #: modified with the Update Personal Meeting Room Options API.
    topic: Optional[str]
    #: PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot
    #: contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The
    #: predefined length for host PIN can be viewed in user's My Personal Room page. This attribute can be modified
    #: with the Update Personal Meeting Room Options API.
    host_pin: Optional[str]
    #: PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It cannot
    #: contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as 1111. The
    #: predefined length for host PIN can be viewed in user's My Personal Room page. This attribute can be modified
    #: with the Update Personal Meeting Room Options API.
    host_pin: Optional[str]
    #: Personal Meeting Room link. It cannot be empty. Note: This is a read-only attribute.
    personal_meeting_room_link: Optional[str]
    #: Option to automatically lock the Personal Room a number of minutes after a meeting starts. When a room is
    #: locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked is
    #: defined by autoLockMinutes. This attribute can be modified with the Update Personal Meeting Room Options API.
    enabled_auto_lock: Optional[bool]
    #: Number of minutes after which the Personal Room is locked if enabledAutoLock is enabled. Valid options are 0, 5,
    #: 10, 15 and 20. This attribute can be modified with the Update Personal Meeting Room Options API.
    auto_lock_minutes: Optional[int]
    #: Flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby while the
    #: owner is not in the room. This attribute can be modified with the Update Personal Meeting Room Options API.
    enabled_notify_host: Optional[bool]
    #: Flag allowing other invitees to host a meeting in the Personal Room without the owner. This attribute can be
    #: modified with the Update Personal Meeting Room Options API.
    support_co_host: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: Personal Room. The target site is user's preferred site. This attribute can be modified with the Update Personal
    #: Meeting Room Options API.
    support_anyone_as_co_host: Optional[bool]
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when
    #: joining the Personal Room. The target site is user's preferred site. This attribute can be modified with the
    #: Update Personal Meeting Room Options API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting
    #: without a prompt. This attribute can be modified with the Update Personal Meeting Room Options API.
    allow_authenticated_devices: Optional[bool]
    #: Array defining cohosts for the room if both supportAnyoneAsCoHost and allowFirstUserToBeCoHost are false This
    #: attribute can be modified with the Update Personal Meeting Room Options API.
    co_hosts: Optional[list[CoHosts]]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Information for callbacks from meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]


class DefaultAudioType(str, Enum):
    #: Webex audio. This supports telephony and VoIP.
    webex_audio = 'webexAudio'
    #: Support only VoIP.
    voip_only = 'voipOnly'
    #: Other teleconference service. Details are defined in the otherTeleconferenceDescription parameter.
    other_teleconference_service = 'otherTeleconferenceService'
    #: No audio.
    none = 'none'


class OfficeNumber(ApiModel):
    #: Country code for the phone number. This attribute can be modified with the with the Update Audio Options API.
    country_code: Optional[str]
    #: Phone number. It cannot be longer than 30 characters. This attribute can be modified with the with the Update
    #: Audio Options API.
    number: Optional[str]
    #: Flag identifying the phone number as the one that will be used to dial into a teleconference. This attribute can
    #: be modified with the with the Update Audio Options API.
    enabled_call_in_authentication: Optional[bool]
    #: Flag to enable/disable Call Me number display on the meeting client. This attribute can be modified with the
    #: with the Update Audio Options API. Note: This feature is only effective if the site supports the Call Me
    #: feature.
    enabled_call_me: Optional[bool]


class Audio(ApiModel):
    #: Default audio type. This attribute can be modified with the with the Update Audio Options API.
    default_audio_type: Optional[DefaultAudioType]
    #: Phone number and other information for the teleconference provider to be used, along with instructions for
    #: invitees. This attribute can be modified with the with the Update Audio Options API.
    other_teleconference_description: Optional[str]
    #: Flag to enable/disable global call ins. Note: If the site does not support global call-ins, you cannot set this
    #: option. This attribute can be modified with the with the Update Audio Options API.
    enabled_global_call_in: Optional[bool]
    #: Flag to enable/disable call-ins from toll-free numbers. Note: If the site does not support calls from toll-free
    #: numbers, you cannot set this option. This attribute can be modified with the with the Update Audio Options API.
    enabled_toll_free: Optional[bool]
    #: Flag to enable/disable automatically connecting to audio using a computer. The meeting host can enable/disable
    #: this option. When this option is set to true, the user is automatically connected to audio via a computer when
    #: they start or join a Webex Meetings meeting on a desktop. `This attribute can be modified with the with the
    #: Update Audio Options API.
    enabled_auto_connection: Optional[bool]
    #: PIN to provide a secondary level of authentication for calls where the host is using the phone and may need to
    #: invite additional invitees. It must be exactly 4 digits. It cannot contain sequential digits, such as 1234 or
    #: 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with the with the Update Audio
    #: Options API.
    audio_pin: Optional[str]
    #: Office phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This
    #: attribute can be modified with the with the Update Audio Options API.
    office_number: Optional[OfficeNumber]
    #: Mobile phone number. We recommend that phone numbers be specified to facilitate connecting via audio. This
    #: attribute can be modified with the with the Update Audio Options API.
    mobile_number: Optional[OfficeNumber]


class VideoDevices(ApiModel):
    #: Video system name. It cannot be empty. This attribute can be modified with the Update Video Options API.
    #: Possible values: device1
    device_name: Optional[str]
    #: Video address. It cannot be empty and must be in valid email format. This attribute can be modified with the
    #: Update Video Options API.
    #: Possible values: device1@example.com
    device_address: Optional[str]
    #: Flag identifying the device as the default video device. If user's video device list is not empty, one and only
    #: one device must be set as default. This attribute can be modified with the Update Video Options API.
    #: Possible values:
    is_default: Optional[bool]


class Video4(ApiModel):
    #: Array of video devices. This attribute can be modified with the Update Video Options API.
    video_devices: Optional[list[VideoDevices]]


class SchedulingOptionsObject(ApiModel):
    #: Flag to enable/disable Join Before Host. The period during which invitees can join before the start time is
    #: defined by autoLockMinutes. This attribute can be modified with the Update Scheduling Options API. Note: This
    #: feature is only effective if the site supports the Join Before Host feature. This attribute can be modified with
    #: the Update Scheduling Options API.
    enabled_join_before_host: Optional[bool]
    #: Number of minutes before the start time that an invitee can join a meeting if enabledJoinBeforeHost is true.
    #: Valid options are 0, 5, 10 and 15. This attribute can be modified with the Update Scheduling Options API.
    join_before_host_minutes: Optional[int]
    #: Flag to enable/disable the automatic sharing of the meeting recording with invitees when it is available. This
    #: attribute can be modified with the Update Scheduling Options API.
    enabled_auto_share_recording: Optional[bool]
    #: Flag to automatically enable Webex Assistant whenever you start a meeting. This attribute can be modified with
    #: the Update Scheduling Options API.
    enabled_webex_assistant_by_default: Optional[bool]


class Sites(ApiModel):
    #: Access URL for the site. Note: This is a read-only attribute. The value can be assigned as user's default site
    #: with the Update Default Site API.
    #: Possible values: site1-example.webex.com
    site_url: Optional[str]
    #: Flag identifying the site as the default site. Users can list meetings and recordings, and create meetings on
    #: the default site.
    #: Possible values:
    default: Optional[bool]


class UpdatePersonalMeetingRoomOptionsBody(ApiModel):
    #: Personal Meeting Room topic to be updated.
    topic: Optional[str]
    #: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length, e.g. 4 digits. It
    #: cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the predefined length, such as
    #: 1111. The predefined length for host PIN can be viewed in user's My Personal Room page and it can only be
    #: changed by site administrator.
    host_pin: Optional[str]
    #: Update for option to automatically lock the Personal Room a number of minutes after a meeting starts. When a
    #: room is locked, invitees cannot enter until the owner admits them. The period after which the meeting is locked
    #: is defined by autoLockMinutes.
    enabled_auto_lock: Optional[bool]
    #: Updated number of minutes after which the Personal Room is locked if enabledAutoLock is enabled. Valid options
    #: are 0, 5, 10, 15 and 20.
    auto_lock_minutes: Optional[int]
    #: Update for flag to enable notifying the owner of a Personal Room when someone enters the Personal Room lobby
    #: while the owner is not in the room.
    enabled_notify_host: Optional[bool]
    #: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room without the owner.
    support_co_host: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: Personal Room. The target site is user's preferred site.
    support_anyone_as_co_host: Optional[bool]
    #: Whether or not to allow the first attendee with a host account on the target site to become a cohost when
    #: joining the Personal Room. The target site is user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the user's organization to start or join the meeting
    #: without a prompt.
    allow_authenticated_devices: Optional[bool]
    #: Updated array defining cohosts for the room if both supportAnyoneAsCoHost and allowFirstUserToBeCoHost are false
    co_hosts: Optional[list[CoHosts]]


class GetPersonalMeetingRoomOptionsResponse(UpdatePersonalMeetingRoomOptionsBody):
    #: Personal Meeting Room link. It cannot be empty. Note: This is a read-only attribute.
    personal_meeting_room_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Information for callbacks from meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]


class GetMeetingPreferenceDetailsResponse(ApiModel):
    #: Personal Meeting Room options.
    personal_meeting_room: Optional[PersonalMeetingRoom]
    #: Audio Preferences. Note: These audio settings do not apply to Personal Room meetings
    audio: Optional[Audio]
    #: Information for video conferencing systems used to connect to Webex meetings. Note: The Call My Video System
    #: feature is available only if it has been purchased for your site and your administrator has enabled it.
    video: Optional[Video4]
    #: Meeting scheduling options.
    scheduling_options: Optional[SchedulingOptionsObject]
    #: List of user's Webex meeting sites including default site.
    sites: Optional[list[Sites]]


class GetVideoOptionsResponse(ApiModel):
    #: Array of video devices. This attribute can be modified with the Update Video Options API.
    video_devices: Optional[list[VideoDevices]]


class UpdateVideoOptionsBody(ApiModel):
    #: Array of video devices. If the array is not empty, one device and no more than one devices must be set as
    #: default device.
    video_devices: Optional[list[VideoDevices]]


class UpdateVideoOptionsResponse(ApiModel):
    #: Array of video devices. This attribute can be modified with the Update Video Options API.
    video_devices: Optional[list[VideoDevices]]


class GetSiteListResponse(ApiModel):
    #: Array of sites for the user. Users can have one site or multiple sites. This concept is specific to Webex
    #: Meetings. Any siteUrl in the site list can be assigned as user's default site with the Update Default Site API.
    sites: Optional[list[Sites]]


class UpdateDefaultSiteBody(ApiModel):
    #: Access URL for the site.
    site_url: Optional[str]


class MeetingPreferencesApi(ApiChild, base='meetingPreferences'):
    """
    This API manages a user's meeting preferences, including Personal Meeting Room settings, video and audio settings,
    meeting scheduling options, and site settings.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def meeting_preference_details(self, user_email: str = None, site_url: str = None) -> GetMeetingPreferenceDetailsResponse:
        """
        Retrieves meeting preferences for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the required admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details of the meeting preferences for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-meeting-preference-details
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
        data = super().get(url=url, params=params)
        return GetMeetingPreferenceDetailsResponse.parse_obj(data)

    def personal_meeting_room_options(self, user_email: str = None, site_url: str = None) -> GetPersonalMeetingRoomOptionsResponse:
        """
        Retrieves the Personal Meeting Room options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-personal-meeting-room-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('personalMeetingRoom')
        data = super().get(url=url, params=params)
        return GetPersonalMeetingRoomOptionsResponse.parse_obj(data)

    def update_personal_meeting_room_options(self, topic: str, host_pin: str, enabled_auto_lock: bool, auto_lock_minutes: int, enabled_notify_host: bool, support_co_host: bool, co_hosts: CoHosts, user_email: str = None, site_url: str = None, support_anyone_as_co_host: bool = None, allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None) -> GetPersonalMeetingRoomOptionsResponse:
        """
        Update a single meeting

        :param topic: Personal Meeting Room topic to be updated.
        :type topic: str
        :param host_pin: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length,
            e.g. 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the
            predefined length, such as 1111. The predefined length for host PIN can be viewed in user's My Personal
            Room page and it can only be changed by site administrator.
        :type host_pin: str
        :param enabled_auto_lock: Update for option to automatically lock the Personal Room a number of minutes after a
            meeting starts. When a room is locked, invitees cannot enter until the owner admits them. The period after
            which the meeting is locked is defined by autoLockMinutes.
        :type enabled_auto_lock: bool
        :param auto_lock_minutes: Updated number of minutes after which the Personal Room is locked if enabledAutoLock
            is enabled. Valid options are 0, 5, 10, 15 and 20.
        :type auto_lock_minutes: int
        :param enabled_notify_host: Update for flag to enable notifying the owner of a Personal Room when someone
            enters the Personal Room lobby while the owner is not in the room.
        :type enabled_notify_host: bool
        :param support_co_host: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room
            without the owner.
        :type support_co_host: bool
        :param co_hosts: Updated array defining cohosts for the room if both supportAnyoneAsCoHost and
            allowFirstUserToBeCoHost are false
        :type co_hosts: CoHosts
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param support_anyone_as_co_host: Whether or not to allow any attendee with a host account on the target site
            to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type support_anyone_as_co_host: bool
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee with a host account on the
            target site to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the user's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/update-personal-meeting-room-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = UpdatePersonalMeetingRoomOptionsBody()
        if topic is not None:
            body.topic = topic
        if host_pin is not None:
            body.host_pin = host_pin
        if enabled_auto_lock is not None:
            body.enabled_auto_lock = enabled_auto_lock
        if auto_lock_minutes is not None:
            body.auto_lock_minutes = auto_lock_minutes
        if enabled_notify_host is not None:
            body.enabled_notify_host = enabled_notify_host
        if support_co_host is not None:
            body.support_co_host = support_co_host
        if co_hosts is not None:
            body.co_hosts = co_hosts
        if support_anyone_as_co_host is not None:
            body.support_anyone_as_co_host = support_anyone_as_co_host
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        url = self.ep('personalMeetingRoom')
        data = super().put(url=url, params=params, data=body.json())
        return GetPersonalMeetingRoomOptionsResponse.parse_obj(data)

    def audio_options(self, user_email: str = None, site_url: str = None) -> Audio:
        """
        Retrieves audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-audio-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('audio')
        data = super().get(url=url, params=params)
        return Audio.parse_obj(data)

    def update_audio_options(self, user_email: str = None, site_url: str = None, default_audio_type: DefaultAudioType = None, other_teleconference_description: str = None, enabled_global_call_in: bool = None, enabled_toll_free: bool = None, enabled_auto_connection: bool = None, audio_pin: str = None, office_number: OfficeNumber = None, mobile_number: OfficeNumber = None) -> Audio:
        """
        Updates audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param default_audio_type: Default audio type. This attribute can be modified with the with the Update Audio
            Options API.
        :type default_audio_type: DefaultAudioType
        :param other_teleconference_description: Phone number and other information for the teleconference provider to
            be used, along with instructions for invitees. This attribute can be modified with the with the Update
            Audio Options API.
        :type other_teleconference_description: str
        :param enabled_global_call_in: Flag to enable/disable global call ins. Note: If the site does not support
            global call-ins, you cannot set this option. This attribute can be modified with the with the Update Audio
            Options API.
        :type enabled_global_call_in: bool
        :param enabled_toll_free: Flag to enable/disable call-ins from toll-free numbers. Note: If the site does not
            support calls from toll-free numbers, you cannot set this option. This attribute can be modified with the
            with the Update Audio Options API.
        :type enabled_toll_free: bool
        :param enabled_auto_connection: Flag to enable/disable automatically connecting to audio using a computer. The
            meeting host can enable/disable this option. When this option is set to true, the user is automatically
            connected to audio via a computer when they start or join a Webex Meetings meeting on a desktop. `This
            attribute can be modified with the with the Update Audio Options API.
        :type enabled_auto_connection: bool
        :param audio_pin: PIN to provide a secondary level of authentication for calls where the host is using the
            phone and may need to invite additional invitees. It must be exactly 4 digits. It cannot contain sequential
            digits, such as 1234 or 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with
            the with the Update Audio Options API.
        :type audio_pin: str
        :param office_number: Office phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type office_number: OfficeNumber
        :param mobile_number: Mobile phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type mobile_number: OfficeNumber

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/update-audio-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = Audio()
        if default_audio_type is not None:
            body.default_audio_type = default_audio_type
        if other_teleconference_description is not None:
            body.other_teleconference_description = other_teleconference_description
        if enabled_global_call_in is not None:
            body.enabled_global_call_in = enabled_global_call_in
        if enabled_toll_free is not None:
            body.enabled_toll_free = enabled_toll_free
        if enabled_auto_connection is not None:
            body.enabled_auto_connection = enabled_auto_connection
        if audio_pin is not None:
            body.audio_pin = audio_pin
        if office_number is not None:
            body.office_number = office_number
        if mobile_number is not None:
            body.mobile_number = mobile_number
        url = self.ep('audio')
        data = super().put(url=url, params=params, data=body.json())
        return Audio.parse_obj(data)

    def video_options(self, user_email: str = None, site_url: str = None) -> list[VideoDevices]:
        """
        Retrieves video options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved using Get Site List.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-video-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('video')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[VideoDevices], data["videoDevices"])

    def update_video_options(self, video_devices: VideoDevices, user_email: str = None, site_url: str = None) -> list[VideoDevices]:
        """
        Updates video options for the authenticated user.

        :param video_devices: Array of video devices. If the array is not empty, one device and no more than one
            devices must be set as default device.
        :type video_devices: VideoDevices
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/update-video-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = UpdateVideoOptionsBody()
        if video_devices is not None:
            body.video_devices = video_devices
        url = self.ep('video')
        data = super().put(url=url, params=params, data=body.json())
        return parse_obj_as(list[VideoDevices], data["videoDevices"])

    def scheduling_options(self, user_email: str = None, site_url: str = None) -> SchedulingOptionsObject:
        """
        Retrieves scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-scheduling-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('schedulingOptions')
        data = super().get(url=url, params=params)
        return SchedulingOptionsObject.parse_obj(data)

    def update_scheduling_options(self, user_email: str = None, site_url: str = None, enabled_join_before_host: bool = None, join_before_host_minutes: int = None, enabled_auto_share_recording: bool = None, enabled_webex_assistant_by_default: bool = None) -> SchedulingOptionsObject:
        """
        Updates scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param enabled_join_before_host: Flag to enable/disable Join Before Host. The period during which invitees can
            join before the start time is defined by autoLockMinutes. This attribute can be modified with the Update
            Scheduling Options API. Note: This feature is only effective if the site supports the Join Before Host
            feature. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_join_before_host: bool
        :param join_before_host_minutes: Number of minutes before the start time that an invitee can join a meeting if
            enabledJoinBeforeHost is true. Valid options are 0, 5, 10 and 15. This attribute can be modified with the
            Update Scheduling Options API.
        :type join_before_host_minutes: int
        :param enabled_auto_share_recording: Flag to enable/disable the automatic sharing of the meeting recording with
            invitees when it is available. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_auto_share_recording: bool
        :param enabled_webex_assistant_by_default: Flag to automatically enable Webex Assistant whenever you start a
            meeting. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_webex_assistant_by_default: bool

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/update-scheduling-options
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = SchedulingOptionsObject()
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if enabled_auto_share_recording is not None:
            body.enabled_auto_share_recording = enabled_auto_share_recording
        if enabled_webex_assistant_by_default is not None:
            body.enabled_webex_assistant_by_default = enabled_webex_assistant_by_default
        url = self.ep('schedulingOptions')
        data = super().put(url=url, params=params, data=body.json())
        return SchedulingOptionsObject.parse_obj(data)

    def site_list(self, user_email: str = None) -> list[Sites]:
        """
        Retrieves the list of Webex sites that the authenticated user is set up to use.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user and the API will
            return the list of Webex sites for that user.
        :type user_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        url = self.ep('sites')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Sites], data["sites"])

    def update_default_site(self, default_site: bool, site_url: str, user_email: str = None) -> Sites:
        """
        Updates the default site for the authenticated user.

        :param default_site: Whether or not to change user's default site. Note: defaultSite should be set to true for
            the user's single default site
        :type default_site: bool
        :param site_url: Access URL for the site.
        :type site_url: str
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update default site for that user.
        :type user_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-preferences/update-default-site
        """
        params = {}
        params['defaultSite'] = str(default_site).lower()
        if user_email is not None:
            params['userEmail'] = user_email
        body = UpdateDefaultSiteBody()
        if site_url is not None:
            body.site_url = site_url
        url = self.ep('sites')
        data = super().put(url=url, params=params, data=body.json())
        return Sites.parse_obj(data)

class AnswerObject(CoHosts):
    #: The ID of the person who answered the question. Only present for authenticated users.
    person_id: Optional[str]
    #: The content of the answer.
    answer: Optional[list[str]]
    #: Whether or not the question was answered.
    answered: Optional[bool]


class Answers(ApiModel):
    #: The pagination links of the question's answers.
    links: Optional[Link]
    #: An array of answer objects for this question.
    items: Optional[list[AnswerObject]]


class QAObject(CoHosts):
    #: A unique identifier for the question.
    id: Optional[str]
    #: A unique identifier for the meeting instance to which the Q&A belongs.
    meeting_id: Optional[str]
    #: The total number of attendees in the meeting.
    total_attendees: Optional[int]
    #: The total number of respondents in the meeting.
    total_respondents: Optional[int]
    #: The question that was asked.
    question: Optional[str]
    #: Question's answers.
    answers: Optional[Answers]


class ListMeetingQAndAResponse(ApiModel):
    #: An array of Q&A objects.
    items: Optional[list[QAObject]]


class ListAnswersOfQuestionResponse(ApiModel):
    #: An array of answers to a specific question.
    items: Optional[list[AnswerObject]]


class MeetingQandAApi(ApiChild, base='meetings/q_and_a'):
    """
    During a Question and Answer (Q&A) session, attendees can pose questions to hosts, co-hosts, and presenters, who
    can answer and moderate those questions. You use the Meeting Q&A API to retrieve the questions and the answers in a
    meeting.
    Currently, these APIs are available to users with one of the meeting host, admin or Compliance Officer roles.
    The features and APIs described here are available upon-request and is not enabled by default. If would like this
    feature enabled for your organization please contact the Webex Developer Support team at devsupport@webex.com.
    """

    def list_meeting_q_and_a(self, meeting_id: str, **params) -> Generator[QAObject, None, None]:
        """
        Lists questions and answers from a meeting, when ready.
        Notes:

        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-meeting-q-and-a
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=QAObject, params=params)

    def list_answers_of_question(self, question_id: str, meeting_id: str, **params) -> Generator[AnswerObject, None, None]:
        """
        Lists the answers to a specific question asked in a meeting.

        :param question_id: The ID of a question.
        :type question_id: str
        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-answers-of-a-question
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{question_id}/answers')
        return self.session.follow_pagination(url=url, model=AnswerObject, params=params)

class NetworkType(str, Enum):
    wifi = 'wifi'
    cellular = 'cellular'
    ethernet = 'ethernet'
    unknown = 'unknown'


class TransportType(str, Enum):
    udp = 'UDP'
    tcp = 'TCP'


class VideoIn(ApiModel):
    #: The sampling interval, in seconds, of the downstream video quality data.
    sampling_interval: Optional[int]
    #: The date and time when this video session started.
    start_time: Optional[str]
    #: The date and time when this video session ended.
    end_time: Optional[str]
    #: The percentage of video packet loss, as a float between 0.0 and 100.0, during each sampling interval.
    packet_loss: Optional[list[int]]
    #: The average latency, in milliseconds, during each sampling interval.
    latency: Optional[list[int]]
    #: The pixel height of the incoming video.
    resolution_height: Optional[list[int]]
    #: The frames per second of the incoming video.
    frame_rate: Optional[list[int]]
    #: The bit rate of the incoming video.
    media_bit_rate: Optional[list[int]]
    #: The incoming video codec.
    codec: Optional[str]
    #: The incoming video jitter.
    jitter: Optional[list[int]]
    #: The network protocol used for video transmission.
    transport_type: Optional[TransportType]


class Resources(ApiModel):
    #: The average percent CPU for the process.
    process_average_cpu: Optional[list[int]]
    #: The max percent CPU for the process.
    process_max_cpu: Optional[list[int]]
    #: The average percent CPU for the system.
    system_average_cpu: Optional[list[int]]
    #: The max percent CPU for the system.
    system_max_cpu: Optional[list[int]]


class MediaSessionQuality(ApiModel):
    #: The meeting identifier for the specific meeting instance.
    meeting_instance_id: Optional[str]
    #: The display name of the participant of this media session.
    webex_user_name: Optional[str]
    #: The email address of the participant of this media session.
    webex_user_email: Optional[str]
    #: The date and time when this participant joined the meeting.
    join_time: Optional[str]
    #: The date and time when this participant left the meeting.
    leave_time: Optional[str]
    #: The join meeting time of the participant.
    join_meeting_time: Optional[str]
    #: The type of the client (and OS) used by this media session.
    client_type: Optional[str]
    #: The version of the client used by this media session.
    client_version: Optional[str]
    #: The operating system used for the client.
    os_type: Optional[str]
    #: The version of the operating system used for the client.
    os_version: Optional[str]
    #: The type of hardware used to attend the meeting
    hardware_type: Optional[str]
    #: A description of the speaker used in the meeting.
    speaker_name: Optional[str]
    #: The type of network.
    network_type: Optional[NetworkType]
    #: The local IP address of the client.
    local_ip: Optional[str]
    #: The public IP address of the client.
    public_ip: Optional[str]
    #: The masked local IP address of the client.
    masked_local_ip: Optional[str]
    #: The masked public IP address of the client.
    masked_public_ip: Optional[str]
    #: A description of the camera used in the meeting.
    camera: Optional[str]
    #: A description of the microphone used in the meeting.
    microphone: Optional[str]
    #: The server region.
    server_region: Optional[str]
    #: The video mesh cluster name.
    video_mesh_cluster: Optional[str]
    #: The video mesh server name.
    video_mesh_server: Optional[str]
    #: Identifies the participant.
    participant_id: Optional[str]
    #: Identifies a specific session the participant has in a given meeting.
    participant_session_id: Optional[str]
    #: The collection of downstream (sent to the client) video quality data.
    video_in: Optional[list[VideoIn]]
    #: The collection of upstream (sent from the client) video quality data.
    video_out: Optional[list[VideoIn]]
    #: The collection of downstream (sent to the client) audio quality data.
    audio_in: Optional[list[VideoIn]]
    #: The collection of upstream (sent from the client) audio quality data.
    audio_out: Optional[list[VideoIn]]
    #: The collection of downstream (sent to the client) share quality data.
    share_in: Optional[list[VideoIn]]
    #: The collection of upstream (sent from the client) share quality data.
    share_out: Optional[list[VideoIn]]
    #: Device resources such as CPU and memory.
    resources: Optional[list[Resources]]


class GetMeetingQualitiesResponse(ApiModel):
    items: Optional[list[MediaSessionQuality]]


class MeetingQualitiesApi(ApiChild, base=''):
    """
    To retrieve quality information, you must use an administrator token with the analytics:read_all scope. The
    authenticated user must be a read-only or full administrator of the organization to which the meeting belongs and
    must not be an external administrator.
    To use this endpoint, the org needs to be licensed for the Webex Pro Pack.
    For CI-Native site, no additional settings are required.
    For CI-linked site, the admin must also be set as the Full/ReadOnly Site Admin of the site.
    A minimum Webex and Teams client version is required. For details, see Troubleshooting Help Doc.
    Quality information is available 10 minutes after a meeting has started and may be retrieved for up to 7 days.
    A rate limit of 1 API call every 5 minutes for the same meeting instance ID applies.
    """

    def meeting_qualities(self, meeting_id: str, offset: int = None, **params) -> Generator[MediaSessionQuality, None, None]:
        """
        Get quality data for a meeting, by meetingId. Only organization administrators can retrieve meeting quality
        data.

        :param meeting_id: Unique identifier for the specific meeting instance. Note: The meetingId can be obtained via
            the Meeting List API when meetingType=meeting. The id attribute in the Meeting List Response is what is
            needed, for example, e5dba9613a9d455aa49f6ffdafb6e7db_I_191395283063545470.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int

        documentation: https://developer.webex.com/docs/api/v1/meeting-qualities/get-meeting-qualities
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep('https://analytics.webexapis.com/v1/meeting/qualities')
        return self.session.follow_pagination(url=url, model=MediaSessionQuality, params=params)

class Status(str, Enum):
    #: Transcript is available.
    available = 'available'
    #: Transcript has been deleted.
    deleted = 'deleted'


class TranscriptObject(ApiModel):
    #: A unique identifier for the transcript.
    id: Optional[str]
    #: URL of the Webex site from which the API lists meeting transcripts.
    site_url: Optional[str]
    #: Start time for the meeting transcript in ISO 8601 compliant format.
    start_time: Optional[str]
    #: The meeting's topic.
    meeting_topic: Optional[str]
    #: Unique identifier for the meeting instance to which the transcripts belong.
    meeting_id: Optional[str]
    #: Unique identifier for scheduled meeting with which the current meeting is associated. Only apples to a meeting
    #: instance which is happening or has happened. This is the id of the scheduled meeting with which the instance is
    #: associated.
    scheduled_meeting_id: Optional[str]
    #: Unique identifier for the parent meeting series to which the recording belongs.
    meeting_series_id: Optional[str]
    #: Unique identifier for the meeting host.
    host_user_id: Optional[str]
    #: The download link for the transcript vtt file.
    vtt_download_link: Optional[str]
    #: The download link for the transcript txt file.
    txt_download_link: Optional[str]
    status: Optional[Status]


class ListMeetingTranscriptsResponse(ApiModel):
    #: Transcript array.
    items: Optional[list[TranscriptObject]]


class ListMeetingTranscriptsForComplianceOfficerResponse(ApiModel):
    #: Transcript array
    items: Optional[list[TranscriptObject]]


class ListSnippetsOfMeetingTranscriptResponse(ApiModel):
    #: Transcript snippet array
    items: Optional[list[SnippetObject1]]


class UpdateTranscriptSnippetBody(ApiModel):
    #: Reason for snippet update; only required for Compliance Officers.
    reason: Optional[str]
    #: Text for the snippet.
    text: Optional[str]


class DeleteTranscriptBody(ApiModel):
    #: Reason for deleting a transcript. Only required when a Compliance Officer is operating on another user's
    #: transcript.
    reason: Optional[str]
    #: Explanation for deleting a transcript. The comment can be a maximum of 255 characters long.
    comment: Optional[str]


class MeetingTranscriptsApi(ApiChild, base=''):
    """
    Not supported for Webex for Government (FedRAMP)
    A meeting transcript is the automatic transcription of a meeting's recordings by our industry-leading
    speech-to-text engine to capture of what was discussed and decided during the meeting, in text form.
    A transcript snippet is a short text snippet from a meeting transcript which was spoken by a particular participant
    in the meeting. A meeting transcript consists of many snippets.
    This API manages meeting transcripts and snippets. You can use the Transcript API to list meeting transcripts,
    list, get and update transcript snippets. Transcripts may be retrieved via download link defined by vttDownloadLink
    or txtDownloadlink in the response body.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    NOTE:
    """

    def list_meeting(self, meeting_id: str = None, host_email: str = None, site_url: str = None, from_: str = None, to_: str = None, **params) -> Generator[TranscriptObject, None, None]:
        """
        Lists available transcripts of an ended meeting instance.
        Use this operation to list transcripts of an ended meeting instance when they are ready. Please note that only
        meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and
        in-progress meeting instances are not supported.

        :param meeting_id: Unique identifier for the meeting instance to which the transcript belongs. Please note that
            currently the meeting ID of a scheduled personal room meeting is not supported for this API. If meetingId
            is not specified, the operation returns an array of transcripts for all meetings of the current user.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user. If meetingId is not
            specified, it can not support hostEmail.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists transcripts. If not specified, the API lists
            transcripts from user's preferred site. All available Webex sites and the preferred site of the user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts
        """
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('meetingTranscripts')
        return self.session.follow_pagination(url=url, model=TranscriptObject, params=params)

    def list_meeting_for_compliance_officer(self, site_url: str, from_: str = None, to_: str = None, **params) -> Generator[TranscriptObject, None, None]:
        """
        Lists available or deleted transcripts of an ended meeting instance for a specific site.
        The returned list is sorted in descending order by the date and time that the transcript was created.

        :param site_url: URL of the Webex site from which the API lists transcripts.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts-for-compliance-officer
        """
        params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('admin/meetingTranscripts')
        return self.session.follow_pagination(url=url, model=TranscriptObject, params=params)

    def download_meeting(self, transcript_id: str, format: str = None, host_email: str = None):
        """
        Download a meeting transcript from the meeting transcript specified by transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript.
        :type transcript_id: str
        :param format: Format for the downloaded meeting transcript. Possible values: vtt, txt
        :type format: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/download-a-meeting-transcript
        """
        params = {}
        if format is not None:
            params['format'] = format
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'meetingTranscripts/{transcript_id}/download')
        super().get(url=url, params=params)
        return $!$!$!   # this is weird. Check the spec at https://developer.webex.com/docs/api/v1/meeting-transcripts/download-a-meeting-transcript

    def list_snippets_of_meeting(self, transcript_id: str, **params) -> Generator[SnippetObject1, None, None]:
        """
        Lists snippets of a meeting transcript specified by transcriptId.
        Use this operation to list snippets of a meeting transcript when they are ready.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippets belong.
        :type transcript_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-snippets-of-a-meeting-transcript
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets')
        return self.session.follow_pagination(url=url, model=SnippetObject1, params=params)

    def snippet(self, transcript_id: str, snippet_id: str) -> SnippetObject1:
        """
        Retrieves details for a transcript snippet specified by snippetId from the meeting transcript specified by
        transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript to which the requested snippet belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being requested.
        :type snippet_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/get-a-transcript-snippet
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = super().get(url=url)
        return SnippetObject1.parse_obj(data)

    def update_snippet(self, transcript_id: str, snippet_id: str, text: str, reason: str = None) -> SnippetObject1:
        """
        Updates details for a transcript snippet specified by snippetId from the meeting transcript specified by
        transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippet to be updated belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being updated.
        :type snippet_id: str
        :param text: Text for the snippet.
        :type text: str
        :param reason: Reason for snippet update; only required for Compliance Officers.
        :type reason: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/update-a-transcript-snippet
        """
        body = UpdateTranscriptSnippetBody()
        if text is not None:
            body.text = text
        if reason is not None:
            body.reason = reason
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = super().put(url=url, data=body.json())
        return SnippetObject1.parse_obj(data)

    def delete(self, transcript_id: str, reason: str = None, comment: str = None):
        """
        Removes a transcript with a specified transcript ID. The deleted transcript cannot be recovered. If a
        Compliance Officer deletes another user's transcript, the transcript will be inaccessible to regular users
        (host, attendees), but will be still available to the Compliance Officer.

        :param transcript_id: Unique identifier for the meeting transcript.
        :type transcript_id: str
        :param reason: Reason for deleting a transcript. Only required when a Compliance Officer is operating on
            another user's transcript.
        :type reason: str
        :param comment: Explanation for deleting a transcript. The comment can be a maximum of 255 characters long.
        :type comment: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/delete-a-transcript
        """
        body = DeleteTranscriptBody()
        if reason is not None:
            body.reason = reason
        if comment is not None:
            body.comment = comment
        url = self.ep(f'meetingTranscripts/{transcript_id}')
        super().delete(url=url, data=body.json())
        return

class TemplateType(str, Enum):
    #: Webex meeting.
    meeting = 'meeting'
    #: Webex webinar.
    webinar = 'webinar'


class ScheduledType(TemplateType):
    #: Set the value of scheduledType attribute to personalRoomMeeting for creating a meeting in the user's personal
    #: room. Please note that templateId, roomId, integrationTags, enabledWebcastView, enabledAutoRecordMeeting and
    #: registration are not supported when creating a personal room meeting.
    personal_room_meeting = 'personalRoomMeeting'


class InviteeObjectForCreateMeeting(CoHosts):
    #: Whether or not invitee is allowed to be a cohost for the meeting. coHost for each invitee is true by default if
    #: roomId is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a cohost
    #: will be invited as a non-cohost invitee.
    co_host: Optional[bool]
    #: Whether or not an invitee is allowed to be a panelist. Only applies to webinars.
    panelist: Optional[bool]


class Type2(str, Enum):
    #: Single line text box.
    single_line_text_box = 'singleLineTextBox'
    #: Multiple line text box.
    multi_line_text_box = 'multiLineTextBox'
    #: Check box which requires options.
    checkbox = 'checkbox'
    #: Drop down list box which requires options.
    dropdown_list = 'dropdownList'
    #: Single radio button which requires options.
    radio_buttons = 'radioButtons'


class Condition(str, Enum):
    #: The content of the answer contains the value.
    contains = 'contains'
    #: The content of the answer does not contain the value
    not_contains = 'notContains'
    #: The content of the answer begins with the value.
    begins_with = 'beginsWith'
    #: The content of the answer ends with the value.
    ends_with = 'endsWith'
    #: The content of the answer is the same as the value.
    equals = 'equals'
    #: The content of the answer is not the same as the value.
    not_equals = 'notEquals'


class Result(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class Rules(ApiModel):
    #: Judgment expression for approval rules.
    condition: Optional[Condition]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    result: Optional[Result]
    #: Whether to check the case of values.
    match_case: Optional[bool]


class CustomizedQuestionForCreateMeeting(ApiModel):
    #: Title of the customized question.
    question: Optional[str]
    #: Whether or not the customized question is required to be answered by participants.
    required: Optional[bool]
    #: Type of the question being asked.
    type: Optional[Type2]
    #: The maximum length of a string that can be entered by the user, ranging from 0 to 999. Only required by
    #: singleLineTextBox and multiLineTextBox.
    max_length: Optional[int]
    #: The content of options. Required if the question type is one of checkbox, dropdownList, or radioButtons.
    #: The content of the option.
    options: Optional[list[object]]
    #: The automatic approval rules for customized questions.
    rules: Optional[list[Rules]]


class Question1(str, Enum):
    #: If the value is lastName, this approval rule applies to the standard question of "Last Name".
    last_name = 'lastName'
    #: If the value is email, this approval rule applies to the standard question of "Email".
    email = 'email'
    #: If the value is jobTitle, this approval rule applies to the standard question of "Job Title".
    job_title = 'jobTitle'
    #: If the value is companyName, this approval rule applies to the standard question of "Company Name".
    company_name = 'companyName'
    #: If the value is address1, this approval rule applies to the standard question of "Address 1".
    address1 = 'address1'
    #: If the value is address2, this approval rule applies to the standard question of "Address 2".
    address2 = 'address2'
    #: If the value is city, this approval rule applies to the standard question of "City".
    city = 'city'
    #: If the value is state, this approval rule applies to the standard question of "State".
    state = 'state'
    #: If the value is zipCode, this approval rule applies to the standard question of "Zip/Post Code".
    zip_code = 'zipCode'
    #: If the value is countryRegion, this approval rule applies to the standard question of "Country Region".
    country_region = 'countryRegion'
    #: If the value is workPhone, this approval rule applies to the standard question of "Work Phone".
    work_phone = 'workPhone'
    #: If the value is fax, this approval rule applies to the standard question of "Fax".
    fax = 'fax'


class StandardRegistrationApproveRule(Rules):
    #: Name for standard question.
    question: Optional[Question1]
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    order: Optional[int]


class Registration1(ApiModel):
    #: Whether or not meeting registration requests are accepted automatically.
    auto_accept_request: Optional[bool]
    #: Whether or not a registrant's first name is required for meeting registration.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is required for meeting registration.
    require_fax: Optional[bool]
    #: The maximum number of meeting registrations. Only applies to meetings. Webinars use a default value of 10000. If
    #: the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000, then at most 3000 registrants can
    #: join this webinar.
    max_register_num: Optional[int]


class Registration(Registration1):
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]]
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting(CoHosts):
    #: Forms a set of simultaneous interpretation channels together with languageCode2. Standard language format from
    #: ISO 639-1 code. Read ISO 639-1 for details.
    language_code1: Optional[str]
    #: Forms a set of simultaneous interpretation channels together with languageCode1. Standard language format from
    #: ISO 639-1 code. Read ISO 639-1 for details.
    language_code2: Optional[str]


class SimultaneousInterpretation(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool]
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]]


class BreakoutSessionObject(ApiModel):
    #: Name for breakout session.
    name: Optional[str]
    #: Invitees for breakout session. Please note that one invitee cannot be assigned to more than one breakout
    #: session.
    invitees: Optional[list[str]]


class UnlockedMeetingJoinSecurity(str, Enum):
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoin, people can join the unlocked meeting
    #: directly.
    allow_join = 'allowJoin'
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoinWithLobby, people will wait in the lobby until
    #: the host admits them.
    allow_join_with_lobby = 'allowJoinWithLobby'
    #: If the value of unlockedMeetingJoinSecurity attribute is blockFromJoin, people can't join the unlocked meeting.
    block_from_join = 'blockFromJoin'


class NoteType(str, Enum):
    #: If the value of noteType attribute is allowAll, all participants can take notes.
    allow_all = 'allowAll'
    #: If the value of noteType attribute is allowOne, only a single note taker is allowed.
    allow_one = 'allowOne'


class MeetingOptions(ApiModel):
    #: Whether or not to allow any attendee to chat in the meeting. Also depends on the session type.
    enabled_chat: Optional[bool]
    #: Whether or not to allow any attendee to have video in the meeting. Also depends on the session type.
    enabled_video: Optional[bool]
    #: Whether or not to allow any attendee to poll in the meeting. Can only be set true for a webinar. The value of
    #: this attribute depends on the session type for a meeting. Please contact your site admin if this attribute is
    #: not available.
    enabled_polling: Optional[bool]
    #: Whether or not to allow any attendee to take notes in the meeting. The value of this attribute also depends on
    #: the session type.
    enabled_note: Optional[bool]
    #: Whether note taking is enabled. If the value of enabledNote is false, users can not set this attribute and get
    #: default value allowAll.
    note_type: Optional[NoteType]
    #: Whether or not to allow any attendee to have closed captions in the meeting. The value of this attribute also
    #: depends on the session type.
    enabled_closed_captions: Optional[bool]
    #: Whether or not to allow any attendee to transfer files in the meeting. The value of this attribute also depends
    #: on the session type.
    enabled_file_transfer: Optional[bool]
    #: Whether or not to allow any attendee to share Universal Communications Format media files in the meeting. The
    #: value of this attribute also depends on the sessionType.
    enabled_ucf_rich_media: Optional[bool]


class AttendeePrivileges(ApiModel):
    #: Whether or not to allow any attendee to share content in the meeting.
    enabled_share_content: Optional[bool]
    #: Whether or not to allow any attendee to save shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_save_document: Optional[bool]
    #: Whether or not to allow any attendee to print shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_print_document: Optional[bool]
    #: Whether or not to allow any attendee to annotate shared documents, slides, or whiteboards when they are shared
    #: as files in the content viewer instead of in a window or application.
    enabled_annotate: Optional[bool]
    #: Whether or not to allow any attendee to view participants.
    enabled_view_participant_list: Optional[bool]
    #: Whether or not to allow any attendee to see a small preview image of any page of shared documents or slides when
    #: they are shared as files in the content viewer instead of in a window or application.
    enabled_view_thumbnails: Optional[bool]
    #: Whether or not to allow any attendee to control applications, web browsers, or desktops remotely.
    enabled_remote_control: Optional[bool]
    #: Whether or not to allow any attendee to view any shared documents or slides when they are shared as files in the
    #: content viewer instead of in a window or application.
    enabled_view_any_document: Optional[bool]
    #: Whether or not to allow any attendee to scroll through any page of shared documents or slides when they are
    #: shared as files in the content viewer instead of in a window or application.
    enabled_view_any_page: Optional[bool]
    #: Whether or not to allow any attendee to contact the operator privately.
    enabled_contact_operator_privately: Optional[bool]
    #: Whether or not to allow any attendee to chat with the host in private.
    enabled_chat_host: Optional[bool]
    #: Whether or not to allow any attendee to chat with the presenter in private.
    enabled_chat_presenter: Optional[bool]
    #: Whether or not to allow any attendee to chat with other participants in private.
    enabled_chat_other_participants: Optional[bool]


class TrackingCodeItemForCreateMeetingObject(ApiModel):
    #: Name of the tracking code. The name cannot be empty and the maximum size is 120 characters.
    name: Optional[str]
    #: Value for the tracking code. value cannot be empty and the maximum size is 120 characters.
    value: Optional[str]


class AudioConnectionType(str, Enum):
    #: Provide a hybrid audio option, allowing attendees to join using their computer audio or a phone.
    webex_audio = 'webexAudio'
    #: Only restricts attendees to join the audio portion of the meeting using their computer instead of a telephone
    #: option.
    vo_ip = 'VoIP'
    #: Other teleconference services.
    other = 'other'
    #: The way of attendees join the audio portion of the meeting is the default value.
    none = 'none'


class EntryAndExitTone(str, Enum):
    #: All call-in users joining the meeting will hear the beep.
    beep = 'beep'
    #: All call-in users joining the meeting will hear their names.
    announce_name = 'announceName'
    #: Turn off beeps and name announcements.
    no_tone = 'noTone'


class AudioConnectionOptions(ApiModel):
    #: Choose how meeting attendees join the audio portion of the meeting.
    audio_connection_type: Optional[AudioConnectionType]
    #: Whether or not to show toll-free call-in numbers.
    enabled_toll_free_call_in: Optional[bool]
    #: Whether or not to show global call-in numbers to attendees.
    enabled_global_call_in: Optional[bool]
    #: Whether or not to allow attendees to receive a call-back and call-in is available. Can only be set true for a
    #: webinar.
    enabled_audience_call_back: Optional[bool]
    #: Select the sound you want users who have a phone audio connection to hear when someone enters or exits the
    #: meeting.
    entry_and_exit_tone: Optional[EntryAndExitTone]
    #: Whether or not to allow the host to unmute participants.
    allow_host_to_unmute_participants: Optional[bool]
    #: Whether or not to allow attendees to unmute themselves.
    allow_attendee_to_unmute_self: Optional[bool]
    #: Whether or not to auto-mute attendees when attendees enter meetings.
    mute_attendee_upon_entry: Optional[bool]


class PatchMeetingBody(ApiModel):
    #: Meeting title. The title can be a maximum of 128 characters long.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    agenda: Optional[str]
    #: Meeting password. Must conform to the site's password complexity settings. Read password management for details.
    password: Optional[str]
    #: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before current date and
    #: time or after end. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Refer to the Webex Meetings guide for more information about restrictions on updating date and time for a
    #: meeting. Please note that when a meeting is being updated, start of the meeting will be accurate to minutes, not
    #: seconds or milliseconds. Therefore, if start is within the same minute as the current time, start will be
    #: adjusted to the upcoming minute; otherwise, start will be adjusted with seconds and milliseconds stripped off.
    #: For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of 2022-03-01T10:32:28.076+08:00 or
    #: 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00, and start of
    #: 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to 2022-03-01T11:32:00+08:00.
    start: Optional[str]
    #: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current date and
    #: time or before start. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Refer to the Webex Meetings guide for more information about restrictions on updating date and time for a
    #: meeting. Please note that when a meeting is being updated, end of the meeting will be accurate to minutes, not
    #: seconds or milliseconds. Therefore, end will be adjusted with seconds and milliseconds stripped off. For
    #: instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00 will be adjusted to
    #: 2022-03-01T11:52:00+08:00.
    end: Optional[str]
    #: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone database).
    timezone: Optional[str]
    #: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Multiple days or dates for monthly or yearly recurrence rule are
    #: not supported, only the first day or date specified is taken. For example,
    #: "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as
    #: "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    recurrence: Optional[str]
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's
    #: user's preferred site.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true.
    enable_connect_audio_before_host: Optional[bool]
    #: The number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. Valid options are 0, 5, 10
    #: and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required while scheduling webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved by List Meeting Session Types
    #: API.
    session_type_id: Optional[int]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's
    #: user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt.
    allow_authenticated_devices: Optional[bool]
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    send_email: Optional[bool]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the
    #: meeting host.
    host_email: Optional[str]
    #: URL of the Webex site which the meeting is updated on. If not specified, the meeting is created on user's
    #: preferred site. All available Webex sites and preferred site of the user can be retrieved by Get Site List API.
    site_url: Optional[str]
    #: Meeting Options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The
    #: maximum size of integrationTags is 3 and each item of integrationTags can be a maximum of 64 characters long.
    #: Please note that an empty or null integrationTags will delete all existing integration tags for the meeting
    #: implicitly. Developer can update integration tags for a meetingSeries but he cannot update it for a
    #: scheduledMeeting or a meeting instance.
    integration_tags: Optional[list[str]]
    #: Whether or not breakout sessions are enabled. If the value of enabledBreakoutSessions is false, users can not
    #: set breakout sessions. If the value of enabledBreakoutSessions is true, users can update breakout sessions using
    #: the Update Breakout Sessions API. Updating breakout sessions are not supported by this API.
    enabled_breakout_sessions: Optional[bool]
    #: Tracking codes information. All available tracking codes and their options for the specified site can be
    #: retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing from the trackingCodes
    #: array and there's a default option for this tracking code, the default option is assigned automatically. If the
    #: inputMode of a tracking code is select, its value must be one of the site-level options or the user-level value.
    #: Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class MeetingType(str, Enum):
    #: Primary instance of a scheduled series of meetings which consists of one or more scheduled meetings based on a
    #: recurrence rule. When a non-recurring meeting is scheduled with no recurrence, its meetingType is also
    #: meetingSeries which is a meeting series with only one occurrence in Webex meeting modeling.
    meeting_series = 'meetingSeries'
    #: Instance from a primary meeting series.
    scheduled_meeting = 'scheduledMeeting'
    #: Meeting instance that is in progress or has completed.
    meeting = 'meeting'


class State4(str, Enum):
    #: Only applies to a meeting series. Indicates that one or more future scheduled meetings exist for this meeting
    #: series.
    active = 'active'
    #: Only applies to scheduled meeting. Indicates that the meeting is scheduled in the future.
    scheduled = 'scheduled'
    #: Only applies to scheduled meeting. Indicates that this scheduled meeting is ready to start or join immediately.
    ready = 'ready'
    #: Only applies to meeting instances. Indicates that a locked meeting has been joined by participants, but no hosts
    #: have joined.
    lobby = 'lobby'
    #: Applies to meeting series and meeting instances. For a meeting series, indicates that an instance of this series
    #: is happening now. For a meeting instance, indicates that the meeting has been joined and unlocked.
    in_progress = 'inProgress'
    #: Applies to scheduled meetings and meeting instances. For scheduled meetings, indicates that the meeting was
    #: started and is now over. For meeting instances, indicates that the meeting instance has concluded.
    ended = 'ended'
    #: This state only applies to scheduled meetings. Indicates that the meeting was scheduled in the past but never
    #: happened.
    missed = 'missed'
    #: This state only applies to a meeting series. Indicates that all scheduled meetings of this series have passed.
    expired = 'expired'


class InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting(InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting):
    #: Unique identifier for meeting interpreter.
    id: Optional[str]


class SimultaneousInterpretation1(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool]
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]]


class MeetingSeriesObjectForListMeeting(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the id is used to identify the entire series. For scheduled
    #: meetings from a series, the id is used to identify that scheduled meeting. For a meeting instance that is in
    #: progress or has concluded, the id is used to identify that instance.
    id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the Update a Meeting API.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the Update a Meeting API.
    agenda: Optional[str]
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the Update
    #: a Meeting API.
    password: Optional[str]
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    phone_and_video_system_password: Optional[str]
    #: Meeting type.
    meeting_type: Optional[MeetingType]
    #: Meeting state.
    state: Optional[State4]
    #: Time zone of start and end, conforming with the IANA time zone database.
    timezone: Optional[str]
    #: Start time for meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, start is
    #: the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, start is the date and time the upcoming or ongoing meeting of the series starts. If the
    #: meetingType of a meeting is scheduledMeeting, start is the scheduled start time of this occurrence. If the
    #: meetingType of a meeting is meeting, start is the actual start time of the meeting instance. Can be modified for
    #: a meeting series or a scheduled meeting using the Update a Meeting API.
    start: Optional[str]
    #: End time for a meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, end is
    #: the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, end is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is scheduledMeeting, end is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is meeting, end is the actual end time of the meeting instance. If a meeting instance
    #: is in progress, end is not available. Can be modified for a meeting series or a scheduled meeting using the
    #: Update a Meeting API.
    end: Optional[str]
    #: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Can be modified for a meeting series using the Update a Meeting
    #: API. Multiple days or dates for monthly or yearly recurrence rule are not supported, only the first day or date
    #: specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it
    #: will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    recurrence: Optional[str]
    #: Unique identifier for the meeting host.
    host_user_id: Optional[str]
    #: Display name for the meeting host.
    host_display_name: Optional[str]
    #: Email address for the meeting host.
    host_email: Optional[str]
    #: Key for joining the meeting as host.
    host_key: Optional[str]
    #: Site URL for the meeting.
    site_url: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    room_id: Optional[str]
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the Update a Meeting API.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a siteUrl parameter when creating the meeting. If not specified, it's a
    #: user's preferred site. The allowAnyUserToBeCoHost attribute can be modified for a meeting series or a scheduled
    #: meeting using the Update a Meeting API.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: enabledJoinBeforeHost attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the enabledJoinBeforeHost attribute is set to true. The enableConnectAudioBeforeHost attribute can be modified
    #: for a meeting series or a scheduled meeting using the Update a Meeting API.
    enable_connect_audio_before_host: Optional[bool]
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the enabledJoinBeforeHost attribute is set to true. The joinBeforeHostMinutes attribute can be
    #: modified for a meeting series or a scheduled meeting using the Update a Meeting API. Valid options are 0, 5, 10
    #: and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the List Meeting
    #: Session Types API.
    session_type_id: Optional[int]
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's personal
    #: room.
    scheduled_type: Optional[ScheduledType]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    phone_and_video_system_panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the siteUrl parameter when creating the meeting. If not specified, it's
    #: a user's preferred site. The allowFirstUserToBeCoHost attribute can be modified for a meeting series or a
    #: scheduled meeting uisng the Update a Meeting API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    allow_authenticated_devices: Optional[bool]
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]
    #: Meeting options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details.
    registration: Optional[Registration1]
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]]
    #: Simultaneous interpretation information for the meeting.
    simultaneous_interpretation: Optional[SimultaneousInterpretation1]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class CreateMeetingResponse(MeetingSeriesObjectForListMeeting):
    #: If true, the meeting is ad-hoc.
    adhoc: Optional[bool]


class Telephony6(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumbers]]
    #: HATEOAS information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[list[Links]]


class ScheduledMeetingObject(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the id is used to identify the entire series. For scheduled
    #: meetings from a series, the id is used to identify that scheduled meeting. For a meeting instance that is in
    #: progress or has concluded, the id is used to identify that instance.
    id: Optional[str]
    #: Unique identifier for meeting series. It only apples to scheduled meeting and meeting instance. If it's a
    #: scheduled meeting from a series or a meeting instance that is happening or has happened, the meetingSeriesId is
    #: the id of the primary series.
    meeting_series_id: Optional[str]
    #: Unique identifier for scheduled meeting which current meeting is associated with. It only apples to meeting
    #: instance which is happening or has happened. It's the id of the scheduled meeting this instance is associated
    #: with.
    scheduled_meeting_id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the Update a Meeting API.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the Update a Meeting API.
    agenda: Optional[str]
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the Update
    #: a Meeting API.
    password: Optional[str]
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    phone_and_video_system_password: Optional[str]
    #: Meeting type.
    meeting_type: Optional[MeetingType]
    #: Meeting state.
    state: Optional[State4]
    #: This state only applies to scheduled meeting. Flag identifying whether or not the scheduled meeting has been
    #: modified.
    is_modified: Optional[bool]
    #: Time zone of start and end, conforming with the IANA time zone database.
    timezone: Optional[str]
    #: Start time for meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, start is
    #: the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, start is the date and time the upcoming or ongoing meeting of the series starts. If the
    #: meetingType of a meeting is scheduledMeeting, start is the scheduled start time of this occurrence. If the
    #: meetingType of a meeting is meeting, start is the actual start time of the meeting instance. Can be modified for
    #: a meeting series or a scheduled meeting using the Update a Meeting API.
    start: Optional[str]
    #: End time for a meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, end is
    #: the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, end is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is scheduledMeeting, end is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is meeting, end is the actual end time of the meeting instance. If a meeting instance
    #: is in progress, end is not available. Can be modified for a meeting series or a scheduled meeting using the
    #: Update a Meeting API.
    end: Optional[str]
    #: Unique identifier for the meeting host.
    host_user_id: Optional[str]
    #: Display name for the meeting host.
    host_display_name: Optional[str]
    #: Email address for the meeting host.
    host_email: Optional[str]
    #: Key for joining the meeting as host.
    host_key: Optional[str]
    #: Site URL for the meeting.
    site_url: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    room_id: Optional[str]
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the Update a Meeting API.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a siteUrl parameter when creating the meeting. If not specified, it's a
    #: user's preferred site. The allowAnyUserToBeCoHost attribute can be modified for a meeting series or a scheduled
    #: meeting using the Update a Meeting API.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: enabledJoinBeforeHost attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the enabledJoinBeforeHost attribute is set to true. The enableConnectAudioBeforeHost attribute can be modified
    #: for a meeting series or a scheduled meeting using the Update a Meeting API.
    enable_connect_audio_before_host: Optional[bool]
    #: The number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. The joinBeforeHostMinutes
    #: attribute can be modified for meeting series or scheduled meeting by Update a Meeting API. Valid options are 0,
    #: 5, 10 and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the List Meeting
    #: Session Types API.
    session_type_id: Optional[int]
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's personal
    #: room.
    scheduled_type: Optional[ScheduledType]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: 8-digit numeric panelist password to join webinar meeting from audio and video devices.
    phone_and_video_system_panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the siteUrl parameter when creating the meeting. If not specified, it's
    #: a user's preferred site. The allowFirstUserToBeCoHost attribute can be modified for a meeting series or a
    #: scheduled meeting uisng the Update a Meeting API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    allow_authenticated_devices: Optional[bool]
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony6]
    #: Meeting Options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information to join
    #: the meeting. Meeting invitees will receive an email with a registration link for the registration. When the
    #: registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details. +
    #: autoAcceptRequest: false (boolean,optional) - Whether or not meeting registration requests are accepted
    #: automatically.
    registration: Optional[Registration1]
    #: External keys created by an integration application in its domain, for example, Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]]
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: HATEOAS Breakout Sessions information for meeting.
    links: Optional[list[Links]]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class PatchMeetingResponse(MeetingSeriesObjectForListMeeting):
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: HATEOAS Breakout Sessions information for meeting.
    links: Optional[list[Links]]


class TemplateObject(ApiModel):
    #: Unique identifier for meeting template.
    id: Optional[str]
    #: Meeting template name.
    name: Optional[str]
    #: Meeting template locale.
    locale: Optional[str]
    #: Site URL for the meeting template.
    site_url: Optional[str]
    #: Meeting template type.
    template_type: Optional[TemplateType]
    #: Whether or not the meeting template is a default template.
    is_default: Optional[bool]
    #: Whether or not the meeting template is a standard template.
    is_standard: Optional[bool]


class CreateMeetingBody(PatchMeetingBody):
    #: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is required.
    adhoc: Optional[bool]
    #: Unique identifier for the Webex space which the meeting is to be associated with. It can be retrieved by List
    #: Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter hostEmail will be ignored.
    room_id: Optional[str]
    #: Unique identifier for meeting template. Please note that start and end are optional when templateId is
    #: specified. The list of meeting templates that is available for the authenticated user can be retrieved from List
    #: Meeting Templates. This parameter is ignored for an ad-hoc meeting.
    template_id: Optional[str]
    #: When set as an attribute in a POST request body, specifies whether it's a regular meeting, a webinar, or a
    #: meeting scheduled in the user's personal room. If not specified, it's a regular meeting by default. The default
    #: value for an ad-hoc meeting is meeting and the user's input value will be ignored.
    scheduled_type: Optional[ScheduledType]
    #: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and invitees is missing, all
    #: the members in the space are invited implicitly. If both roomId and invitees are specified, only those in the
    #: invitees list are invited. coHost for each invitee is true by default if roomId is specified when creating a
    #: meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as a non-cohost
    #: invitee. The user's input value will be ignored for an ad-hoc meeting and the the members of the room specified
    #: by roomId except "me" will be used by default.
    invitees: Optional[list[InviteeObjectForCreateMeeting]]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information to join
    #: the meeting. Meeting invitees will receive an email with a registration link for the registration. When the
    #: registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details. This
    #: parameter is ignored for an ad-hoc meeting.
    registration: Optional[Registration]
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[SimultaneousInterpretation]
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main session.
    #: Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts
    #: preassign attendees to breakout sessions, the role of attendee will be changed to panelist. Breakout session is
    #: not supported for a meeting with simultaneous interpretation.
    breakout_sessions: Optional[list[BreakoutSessionObject]]


class GetMeetingControlStatusResponse(ApiModel):
    #: Whether the meeting is locked or not.
    locked: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording started or not.
    recording_started: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording paused or not.
    recording_paused: Optional[bool]


class Type6(TemplateType):
    #: Meeting session type for a private meeting.
    private_meeting = 'privateMeeting'


class MeetingSessionTypeObject(ApiModel):
    #: Unique identifier for the meeting session type.
    id: Optional[str]
    #: Name of the meeting session type.
    name: Optional[str]
    #: Meeting session type.
    type: Optional[Type6]
    #: The maximum number of attendees for the meeting session type.
    attendees_capacity: Optional[int]


class CustomizedQuestionForGetMeeting(CustomizedQuestionForCreateMeeting):
    #: Unique identifier for the question.
    id: Optional[int]


class GetRegistrationFormFormeetingResponse(ApiModel):
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForGetMeeting]]
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class AnswerForCustomizedQuestion(ApiModel):
    #: Unique identifier for the option.
    option_id: Optional[int]
    #: The content of the answer or the option for this question.
    answer: Optional[str]


class CustomizedRegistrant(ApiModel):
    #: Unique identifier for the customized questions retrieved from the registration form.
    question_id: Optional[int]
    #: The answers for customized questions. If the question type is checkbox, more than one answer can be set.
    answers: Optional[list[AnswerForCustomizedQuestion]]


class Status2(str, Enum):
    #: Registrant has been approved.
    approved = 'approved'
    #: Registrant is in a pending list waiting for host or cohost approval.
    pending = 'pending'
    #: Registrant has been rejected by the host or cohost.
    rejected = 'rejected'


class RegisterMeetingRegistrantBody(Question1):
    #: The registrant's first name.
    first_name: Optional[str]
    #: If true send email to the registrant. Default: true.
    send_email: Optional[bool]
    #: The registrant's answers for customized questions. Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class RegisterMeetingRegistrantResponse(Question1):
    #: New registrant's ID.
    id: Optional[str]
    #: New registrant's status.
    status: Optional[Status2]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class GetmeetingRegistrantsDetailInformationResponse(Question1):
    #: New registrant's ID.
    registrant_id: Optional[str]
    #: New registrant's status.
    status: Optional[Status2]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]
    #: Registrant's source id.The sourceId is from Create Invitation Sources API.
    source_id: Optional[str]


class OrderType(str, Enum):
    desc = 'DESC'
    asc = 'ASC'


class OrderBy(str, Enum):
    #: Registrant's first name.
    first_name = 'firstName'
    #: Registrant's last name.
    last_name = 'lastName'
    #: Registrant's status.
    status = 'status'
    #: registrant's email.
    email = 'email'


class CreateMeetingInterpreterBody(InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting):
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]
    #: If true, send email to the interpreter.
    send_email: Optional[bool]


class GetBreakoutSessionObject(BreakoutSessionObject):
    #: Unique identifier for breakout session.
    id: Optional[str]


class Type11(str, Enum):
    #: Text input.
    text = 'text'
    #: Rating.
    rating = 'rating'
    #: Check box which requires options.
    checkbox = 'checkbox'
    #: Drop down list box which requires options.
    single_dropdown = 'singleDropdown'
    #: Single radio button which requires options.
    single_radio = 'singleRadio'


class Options(ApiModel):
    #: The unique id of options.
    #: Possible values: 1
    id: Optional[int]
    #: The content of the option.
    #: Possible values: green
    value: Optional[str]


class QuestionObject(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[Type11]
    #: The lowest score of the rating question. This attribute will be ingnored, if the value of type attribute is not
    #: rating.
    from_score: Optional[int]
    #: The lowest score label of the rating question. This attribute will be ingnored, if the value of type attribute
    #: is not rating.
    from_label: Optional[str]
    #: The highest score of the rating question. This attribute will be ingnored, if the value of type attribute is not
    #: rating.
    to_score: Optional[int]
    #: The highest score label of the rating question. This attribute will be ingnored, if the value of type attribute
    #: is not rating.
    to_label: Optional[str]
    #: Options for the question. This attribute will be ingnored, if the value of type attribute is text or rating.
    options: Optional[list[Options]]


class QuestionWithAnswersObject(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[Type11]
    #: The user's answers for the question.
    answers: Optional[list[AnswerForCustomizedQuestion]]


class SurveyResultObject(CoHosts):
    #: Unique identifier for the survey result.
    id: Optional[str]
    #: Name for the survey.
    survey_name: Optional[str]
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: The time when the user submits the survey.
    create_time: Optional[str]
    #: User's answers for the questions
    questions: Optional[list[QuestionWithAnswersObject]]


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


class OptionsForTrackingCodeObject(ApiModel):
    #: The value of a tracking code option. value cannot be empty and the maximum size is 120 characters.
    value: Optional[str]
    #: Whether or not the option is the default option of a tracking code.
    default_value: Optional[bool]


class InputMode(str, Enum):
    #: Text input.
    text = 'text'
    #: Drop down list which requires options.
    select = 'select'
    #: Both text input and select from list.
    editable_select = 'editableSelect'
    #: An input method which is only available for the host profile and sign-up pages.
    host_profile_select = 'hostProfileSelect'


class ServiceType(str, Enum):
    #: Recording service-type is MeetingCenter.
    meeting_center = 'MeetingCenter'
    #: Recording service-type is EventCenter.
    event_center = 'EventCenter'
    #: Recording service-type is SupportCenter.
    support_center = 'SupportCenter'
    #: Recording service-type is TrainingCenter.
    training_center = 'TrainingCenter'


class Service(ServiceType):
    #: Tracking codes apply to all services.
    all = 'All'


class HostProfileCode(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'


class Type13(HostProfileCode):
    #: This value only applies to the service of All. When the type of All for a tracking code is notApplicable, there
    #: are different types for different services. For example, required for MeetingCenter, optional for EventCenter
    #: and notUsed for others.
    not_applicable = 'notApplicable'


class ScheduleStartCodeObject(ApiModel):
    #: Service for schedule or sign up pages
    service: Optional[Service]
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[Type13]


class ListMeetingsResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[MeetingSeriesObjectForListMeeting]]


class ListMeetingsOfMeetingSeriesResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[ScheduledMeetingObject]]


class JoinMeetingBody(CoHosts):
    #: Unique identifier for the meeting. This parameter applies to meeting series and scheduled meetings. It doesn't
    #: apply to ended or in-progress meeting instances. Please note that currently meeting ID of a scheduled personal
    #: room meeting is also supported for this API.
    meeting_id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: Whether or not to redirect to joinLink. It is an optional field and default value is true.
    join_directly: Optional[bool]
    #: It's required when the meeting is protected by a password and the current user is not privileged to view it if
    #: they are not a host, cohost or invitee of the meeting.
    password: Optional[str]
    #: Expiration duration of joinLink in minutes. Must be between 1 and 60.
    expiration_minutes: Optional[int]


class JoinMeetingResponse(ApiModel):
    #: The link can directly join or host the meeting.
    join_link: Optional[str]
    #: Expiration time of joinLink.
    expiration: Optional[str]


class ListMeetingTemplatesResponse(ApiModel):
    #: Meeting templates array.
    items: Optional[list[TemplateObject]]


class GetMeetingTemplateResponse(TemplateObject):
    #: Meeting object which is used to create a meeting by the meeting template. Please note that the meeting object
    #: should be used to create a meeting immediately after retrieval since the start and end may be invalid quickly
    #: after generation.
    meeting: Optional[CreateMeetingBody]


class ListMeetingSessionTypesResponse(ApiModel):
    #: Meeting session type array
    items: Optional[list[MeetingSessionTypeObject]]


class UpdateMeetingRegistrationFormBody(ApiModel):
    host_email: Optional[str]
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: The maximum number of meeting registrations. Only applies to meetings. Webinars use a default value of 10000. If
    #: the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000, then at most 3000 registrants can
    #: join this webinar.
    max_register_num: Optional[int]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]]
    #: The approval rule for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class BatchRegisterMeetingRegistrantsBody(ApiModel):
    #: Registrants array.
    items: Optional[list[RegisterMeetingRegistrantBody]]


class BatchRegisterMeetingRegistrantsResponse(ApiModel):
    items: Optional[list[RegisterMeetingRegistrantResponse]]


class ListMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class QueryMeetingRegistrantsBody(ApiModel):
    #: Registrant's status.
    status: Optional[Status2]
    #: Sort order for the registrants.
    order_type: Optional[OrderType]
    #: Registrant ordering field. Ordered by registrationTime by default.
    order_by: Optional[OrderBy]
    #: List of registrant email addresses.
    #: Possible values: bob@example.com
    emails: Optional[list[str]]


class QueryMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class BatchUpdateMeetingRegistrantsStatusBody(ApiModel):
    #: If true send email to registrants. Default: true.
    send_email: Optional[bool]
    #: Registrants array.
    #: Registrant ID.
    registrants: Optional[list[Registrants]]


class ListMeetingInterpretersResponse(ApiModel):
    #: Array of meeting interpreters.
    items: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]]


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


class GetMeetingSurveyResponse(ApiModel):
    #: Unique identifier for the survey.
    id: Optional[str]
    #: Name for the survey.
    survey_name: Optional[str]
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: Description for the survey.
    description: Optional[str]
    #: Whether the survey allows attendees to submit anonymously.
    allow_anonymous_submit: Optional[bool]
    #: Questions for the survey.
    questions: Optional[list[QuestionObject]]


class ListMeetingSurveyResultsResponse(ApiModel):
    #: SurveyResult array
    items: Optional[list[SurveyResultObject]]


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


class ListMeetingTrackingCodesResponse(ScheduleStartCodeObject):
    #: Unique identifier for the tracking code.
    id: Optional[str]
    #: Name for the tracking code.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list. The options here differ from those in the site-level tracking codes and the
    #: user-level tracking codes. It is the result of a selective combination of the two. If there's user-level value
    #: for a tracking code, the user-level value becomes the default option for the tracking code, and the site-level
    #: default value becomes non-default.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: The input mode in which the tracking code value can be assigned.
    input_mode: Optional[InputMode]


class MeetingsApi(ApiChild, base='meetings'):
    """
    Meetings are virtual conferences where users can collaborate in real time using audio, video, content sharing,
    chat, online whiteboards, and to collaborate.
    This API focuses primarily on the scheduling and management of meetings. You can use the Meetings API to list,
    create, get, update, and delete meetings.
    Several types of meeting objects are supported by this API, such as meeting series, scheduled meeting, and ended or
    in-progress meeting instances. See the Meetings Overview for more information about the types of meetings.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def create(self, title: str = None, agenda: str = None, password: str = None, start: str = None, end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None, allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None, enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None, exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None, unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None, enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None, automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None, site_url: str = None, meeting_options: MeetingOptions = None, attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None, enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None, audio_connection_options: AudioConnectionOptions = None, adhoc: bool = None, room_id: str = None, template_id: str = None, scheduled_type: ScheduledType = None, invitees: InviteeObjectForCreateMeeting = None, registration: Registration = None, simultaneous_interpretation: SimultaneousInterpretation = None, breakout_sessions: BreakoutSessionObject = None) -> CreateMeetingResponse:
        """
        Creates a new meeting. Regular users can schedule up to 100 meetings in 24 hours and admin users up to 3000.

        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions
        :param adhoc: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is
            required.
        :type adhoc: bool
        :param room_id: Unique identifier for the Webex space which the meeting is to be associated with. It can be
            retrieved by List Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter
            hostEmail will be ignored.
        :type room_id: str
        :param template_id: Unique identifier for meeting template. Please note that start and end are optional when
            templateId is specified. The list of meeting templates that is available for the authenticated user can be
            retrieved from List Meeting Templates. This parameter is ignored for an ad-hoc meeting.
        :type template_id: str
        :param scheduled_type: When set as an attribute in a POST request body, specifies whether it's a regular
            meeting, a webinar, or a meeting scheduled in the user's personal room. If not specified, it's a regular
            meeting by default. The default value for an ad-hoc meeting is meeting and the user's input value will be
            ignored.
        :type scheduled_type: ScheduledType
        :param invitees: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and
            invitees is missing, all the members in the space are invited implicitly. If both roomId and invitees are
            specified, only those in the invitees list are invited. coHost for each invitee is true by default if
            roomId is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a
            cohost will be invited as a non-cohost invitee. The user's input value will be ignored for an ad-hoc
            meeting and the the members of the room specified by roomId except "me" will be used by default.
        :type invitees: InviteeObjectForCreateMeeting
        :param registration: Meeting registration. When this option is enabled, meeting invitees must register personal
            information to join the meeting. Meeting invitees will receive an email with a registration link for the
            registration. When the registration form has been submitted and approved, an email with a real meeting link
            will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting
            registration does not apply to a meeting when it's a recurring meeting with a recurrence field or no
            password, or the Join Before Host option is enabled for the meeting. See Register for a Meeting in Cisco
            Webex Meetings for details. This parameter is ignored for an ad-hoc meeting.
        :type registration: Registration
        :param simultaneous_interpretation: Simultaneous interpretation information for a meeting.
        :type simultaneous_interpretation: SimultaneousInterpretation
        :param breakout_sessions: Breakout sessions are smaller groups that are split off from the main meeting or
            webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use
            breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few
            participants outside of the main session. Please note that maximum number of breakout sessions in a meeting
            or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of attendee
            will be changed to panelist. Breakout session is not supported for a meeting with simultaneous
            interpretation.
        :type breakout_sessions: BreakoutSessionObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting
        """
        body = CreateMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        if adhoc is not None:
            body.adhoc = adhoc
        if room_id is not None:
            body.room_id = room_id
        if template_id is not None:
            body.template_id = template_id
        if scheduled_type is not None:
            body.scheduled_type = scheduled_type
        if invitees is not None:
            body.invitees = invitees
        if registration is not None:
            body.registration = registration
        if simultaneous_interpretation is not None:
            body.simultaneous_interpretation = simultaneous_interpretation
        if breakout_sessions is not None:
            body.breakout_sessions = breakout_sessions
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return CreateMeetingResponse.parse_obj(data)

    def get(self, meeting_id: str, current: bool = None, host_email: str = None) -> CreateMeetingResponse:
        """
        Retrieves details for a meeting with a specified meeting ID.

        :param meeting_id: Unique identifier for the meeting being requested.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's true, return details
            for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start or the
            upcoming scheduled meeting of the meeting series. If it's false or not specified, return details for the
            entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}')
        data = super().get(url=url, params=params)
        return CreateMeetingResponse.parse_obj(data)

    def list(self, meeting_number: str = None, web_link: str = None, room_id: str = None, meeting_type: str = None, state: str = None, scheduled_type: str = None, current: bool = None, from_: str = None, to_: str = None, host_email: str = None, site_url: str = None, integration_tag: str = None, **params) -> Generator[MeetingSeriesObjectForListMeeting, None, None]:
        """
        Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that
        there are various products in the Webex Suite such as Meetings and Events. Currently, only meetings of the
        Meetings product are supported by this API, meetings of others in the suite are not supported. Ad-hoc meetings
        created by Create a Meeting with adhoc of true and a roomId will not be listed, but the ended and ongoing
        ad-hoc meeting instances will be listed.

        :param meeting_number: Meeting number for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive. If it's an exceptional meeting from a meeting series, the exceptional
            meeting instead of the primary meeting series is returned.
        :type meeting_number: str
        :param web_link: URL encoded link to information page for the meeting objects being requested. meetingNumber,
            webLink and roomId are mutually exclusive.
        :type web_link: str
        :param room_id: Associated Webex space ID for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive.
        :type room_id: str
        :param meeting_type: Meeting type for the meeting objects being requested. This parameter will be ignored if
            meetingNumber, webLink or roomId is specified. Possible values: meetingSeries, scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meeting objects being requested. If not specified, return meetings of all
            states. This parameter will be ignored if meetingNumber, webLink or roomId is specified. Details of an
            ended meeting will only be available 15 minutes after the meeting has ended. inProgress meetings are not
            fully supported. The API will try to return details of an inProgress meeting 15 minutes after the meeting
            starts. However, it may take longer depending on the traffic. See the Webex Meetings guide for more
            information about the states of meetings. Possible values: active, scheduled, ready, lobby, inProgress,
            ended, missed, expired
        :type state: str
        :param scheduled_type: Scheduled type for the meeting objects being requested. Possible values: meeting,
            webinar, personalRoomMeeting
        :type scheduled_type: str
        :param current: Flag identifying to retrieve the current scheduled meeting of the meeting series or the entire
            meeting series. This parameter only applies to scenarios where meetingNumber is specified and the meeting
            is not an exceptional meeting from a meeting series. If it's true, return the scheduled meeting of the
            meeting series which is ready to join or start or the upcoming scheduled meeting of the meeting series; if
            it's false, return the entire meeting series.
        :type current: bool
        :param from_: Start date and time (inclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. from cannot be after to. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type from_: str
        :param to_: End date and time (exclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. to cannot be before from. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type to_: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for meetings that are hosted by that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meetings from. If not specified, the API lists
            meetings from user's all sites. All available Webex sites of the user can be retrieved by Get Site List
            API.
        :type site_url: str
        :param integration_tag: External key created by an integration application. This parameter is used by the
            integration application to query meetings by a key in its own domain such as a Zendesk ticket ID, a Jira
            ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings
        """
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if web_link is not None:
            params['webLink'] = web_link
        if room_id is not None:
            params['roomId'] = room_id
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if scheduled_type is not None:
            params['scheduledType'] = scheduled_type
        if current is not None:
            params['current'] = str(current).lower()
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        url = self.ep()
        return self.session.follow_pagination(url=url, model=MeetingSeriesObjectForListMeeting, params=params)

    def list_of_series(self, meeting_series_id: str, from_: str = None, to_: str = None, meeting_type: str = None, state: str = None, is_modified: bool = None, host_email: str = None, **params) -> Generator[ScheduledMeetingObject, None, None]:
        """
        Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId. Scheduled
        meetings of an ad-hoc meeting created by Create a Meeting with adhoc of true and a roomId will not be listed,
        but the ended and ongoing meeting instances of it will be listed.
        Each scheduled meeting or meeting instance of a meeting series has its own start, end, etc. Thus, for example,
        when a daily meeting has been scheduled from 2019-04-01 to 2019-04-10, there are 10 scheduled meeting instances
        in this series, one instance for each day, and each one has its own attributes. When a scheduled meeting has
        been started and ended or is happening, there are even more ended or in-progress meeting instances.
        Use this operation to list scheduled meeting and meeting instances of a meeting series within a specific date
        range.
        Long result sets are split into pages.
        trackingCodes is not supported for ended meeting instances.

        :param meeting_series_id: Unique identifier for the meeting series. Please note that currently meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_series_id: str
        :param from_: Start date and time (inclusive) for the range for which meetings are to be returned in any ISO
            8601 compliant format. from cannot be after to.
        :type from_: str
        :param to_: End date and time (exclusive) for the range for which meetings are to be returned in any ISO 8601
            compliant format. to cannot be before from.
        :type to_: str
        :param meeting_type: Meeting type for the meeting objects being requested. If not specified, return meetings of
            all types. Possible values: scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meetings being requested. If not specified, return meetings of all states.
            Details of an ended meeting will only be available 15 minutes after the meeting has ended. inProgress
            meetings are not fully supported. The API will try to return details of an inProgress meeting 15 minutes
            after the meeting starts. However, it may take longer depending on the traffic. See the Webex Meetings
            guide for more information about the states of meetings. Possible values: scheduled, ready, lobby,
            inProgress, ended, missed
        :type state: str
        :param is_modified: Flag identifying whether or not only to retrieve scheduled meeting instances which have
            been modified. This parameter only applies to scheduled meetings. If it's true, only return modified
            scheduled meetings; if it's false, only return unmodified scheduled meetings; if not specified, all
            scheduled meetings will be returned.
        :type is_modified: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings-of-a-meeting-series
        """
        params['meetingSeriesId'] = meeting_series_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if is_modified is not None:
            params['isModified'] = str(is_modified).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ScheduledMeetingObject, params=params)

    def patch(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None, end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None, allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None, enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None, exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None, unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None, enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None, automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None, site_url: str = None, meeting_options: MeetingOptions = None, attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None, enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None, audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/patch-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = super().patch(url=url, data=body.json())
        return PatchMeetingResponse.parse_obj(data)

    def update(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None, end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None, allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None, enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None, exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None, unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None, enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None, automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None, site_url: str = None, meeting_options: MeetingOptions = None, attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None, enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None, audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = super().put(url=url, data=body.json())
        return PatchMeetingResponse.parse_obj(data)

    def delete(self, meeting_id: str, host_email: str = None, send_email: bool = None):
        """
        Deletes a meeting with a specified meeting ID. The deleted meeting cannot be recovered. This operation applies
        to meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc
        meetings created by Create a Meeting with adhoc of true and a roomId cannot be deleted.

        :param meeting_id: Unique identifier for the meeting to be deleted. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will delete a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}')
        super().delete(url=url, params=params)
        return

    def join(self, email: str = None, display_name: str = None, meeting_id: str = None, meeting_number: str = None, web_link: str = None, join_directly: bool = None, password: str = None, expiration_minutes: int = None) -> JoinMeetingResponse:
        """
        Retrieves a meeting join link for a meeting with a specified meetingId, meetingNumber, or webLink that allows
        users to join the meeting directly without logging in and entering a password.

        :param email: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room
            Options API. Possible values: john.andersen@example.com
        :type email: str
        :param display_name: Display name for cohost. This attribute can be modified with the Update Personal Meeting
            Room Options API. Possible values: John Andersen
        :type display_name: str
        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances. Please note that currently meeting ID
            of a scheduled personal room meeting is also supported for this API.
        :type meeting_id: str
        :param meeting_number: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but
            not to meeting instances which have ended.
        :type meeting_number: str
        :param web_link: Link to a meeting information page where the meeting client is launched if the meeting is
            ready to start or join.
        :type web_link: str
        :param join_directly: Whether or not to redirect to joinLink. It is an optional field and default value is
            true.
        :type join_directly: bool
        :param password: It's required when the meeting is protected by a password and the current user is not
            privileged to view it if they are not a host, cohost or invitee of the meeting.
        :type password: str
        :param expiration_minutes: Expiration duration of joinLink in minutes. Must be between 1 and 60.
        :type expiration_minutes: int

        documentation: https://developer.webex.com/docs/api/v1/meetings/join-a-meeting
        """
        body = JoinMeetingBody()
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if meeting_number is not None:
            body.meeting_number = meeting_number
        if web_link is not None:
            body.web_link = web_link
        if join_directly is not None:
            body.join_directly = join_directly
        if password is not None:
            body.password = password
        if expiration_minutes is not None:
            body.expiration_minutes = expiration_minutes
        url = self.ep('join')
        data = super().post(url=url, data=body.json())
        return JoinMeetingResponse.parse_obj(data)

    def list_templates(self, template_type: str = None, locale: str = None, is_default: bool = None, is_standard: bool = None, host_email: str = None, site_url: str = None) -> list[TemplateObject]:
        """
        Retrieves the list of meeting templates that is available for the authenticated user.
        There are separate lists of meeting templates for different templateType, locale and siteUrl.

        :param template_type: Meeting template type for the meeting template objects being requested. If not specified,
            return meeting templates of all types. Possible values: meeting, webinar
        :type template_type: str
        :param locale: Locale for the meeting template objects being requested. If not specified, return meeting
            templates of the default en_US locale. Refer to Meeting Template Locales for all the locales supported by
            Webex.
        :type locale: str
        :param is_default: The value is true or false. If it's true, return the default meeting templates; if it's
            false, return the non-default meeting templates. If it's not specified, return both default and non-default
            meeting templates.
        :type is_default: bool
        :param is_standard: The value is true or false. If it's true, return the standard meeting templates; if it's
            false, return the non-standard meeting templates. If it's not specified, return both standard and
            non-standard meeting templates.
        :type is_standard: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meeting templates that are available for that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meeting templates from. If not specified, the API
            lists meeting templates from user's preferred site. All available Webex sites and preferred site of the
            user can be retrieved by Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-templates
        """
        params = {}
        if template_type is not None:
            params['templateType'] = template_type
        if locale is not None:
            params['locale'] = locale
        if is_default is not None:
            params['isDefault'] = str(is_default).lower()
        if is_standard is not None:
            params['isStandard'] = str(is_standard).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('templates')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[TemplateObject], data["items"])

    def template(self, template_id: str, host_email: str = None) -> GetMeetingTemplateResponse:
        """
        Retrieves details for a meeting template with a specified meeting template ID.

        :param template_id: Unique identifier for the meeting template being requested.
        :type template_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return the meeting template that is available for that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-template
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'templates/{template_id}')
        data = super().get(url=url, params=params)
        return GetMeetingTemplateResponse.parse_obj(data)

    def control_status(self, meeting_id: str) -> GetMeetingControlStatusResponse:
        """
        Get the meeting control of a live meeting, which is consisted of meeting control status on "locked" and
        "recording" to reflect whether the meeting is currently locked and there is recording in progress.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep('controls')
        data = super().get(url=url, params=params)
        return GetMeetingControlStatusResponse.parse_obj(data)

    def update_control_status(self, meeting_id: str, locked: bool = None, recording_started: bool = None, recording_paused: bool = None) -> GetMeetingControlStatusResponse:
        """
        To start, pause, resume, or stop a meeting recording; To lock or unlock an on-going meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param locked: Whether the meeting is locked or not.
        :type locked: bool
        :param recording_started: The value can be true or false, it indicates the meeting recording started or not.
        :type recording_started: bool
        :param recording_paused: The value can be true or false, it indicates the meeting recording paused or not.
        :type recording_paused: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        body = GetMeetingControlStatusResponse()
        if locked is not None:
            body.locked = locked
        if recording_started is not None:
            body.recording_started = recording_started
        if recording_paused is not None:
            body.recording_paused = recording_paused
        url = self.ep('controls')
        data = super().put(url=url, params=params, data=body.json())
        return GetMeetingControlStatusResponse.parse_obj(data)

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
        url = self.ep('sessionTypes')
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
        url = self.ep(f'sessionTypes/{session_type_id}')
        data = super().get(url=url, params=params)
        return MeetingSessionTypeObject.parse_obj(data)

    def registration_form_formeeting(self, meeting_id: str) -> GetRegistrationFormFormeetingResponse:
        """
        Get a meeting's registration form to understand which fields are required.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-registration-form-for-a-meeting
        """
        url = self.ep(f'{meeting_id}/registration')
        data = super().get(url=url)
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def update_registration_form(self, meeting_id: str, host_email: str = None, require_first_name: bool = None, require_last_name: bool = None, require_email: bool = None, require_job_title: bool = None, require_company_name: bool = None, require_address1: bool = None, require_address2: bool = None, require_city: bool = None, require_state: bool = None, require_zip_code: bool = None, require_country_region: bool = None, require_work_phone: bool = None, require_fax: bool = None, max_register_num: int = None, customized_questions: CustomizedQuestionForCreateMeeting = None, rules: StandardRegistrationApproveRule = None) -> GetRegistrationFormFormeetingResponse:
        """
        Enable or update a registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str
        :param host_email: 
        :type host_email: str
        :param require_first_name: Whether or not a registrant's first name is required for meeting registration. This
            option must always be true.
        :type require_first_name: bool
        :param require_last_name: Whether or not a registrant's last name is required for meeting registration. This
            option must always be true.
        :type require_last_name: bool
        :param require_email: Whether or not a registrant's email is required for meeting registration. This option
            must always be true.
        :type require_email: bool
        :param require_job_title: Whether or not a registrant's job title is shown or required for meeting
            registration.
        :type require_job_title: bool
        :param require_company_name: Whether or not a registrant's company name is shown or required for meeting
            registration.
        :type require_company_name: bool
        :param require_address1: Whether or not a registrant's first address field is shown or required for meeting
            registration.
        :type require_address1: bool
        :param require_address2: Whether or not a registrant's second address field is shown or required for meeting
            registration.
        :type require_address2: bool
        :param require_city: Whether or not a registrant's city is shown or required for meeting registration.
        :type require_city: bool
        :param require_state: Whether or not a registrant's state is shown or required for meeting registration.
        :type require_state: bool
        :param require_zip_code: Whether or not a registrant's postal code is shown or required for meeting
            registration.
        :type require_zip_code: bool
        :param require_country_region: Whether or not a registrant's country or region is shown or required for meeting
            registration.
        :type require_country_region: bool
        :param require_work_phone: Whether or not a registrant's work phone number is shown or required for meeting
            registration.
        :type require_work_phone: bool
        :param require_fax: Whether or not a registrant's fax number is shown or required for meeting registration.
        :type require_fax: bool
        :param max_register_num: The maximum number of meeting registrations. Only applies to meetings. Webinars use a
            default value of 10000. If the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000,
            then at most 3000 registrants can join this webinar.
        :type max_register_num: int
        :param customized_questions: Customized questions for meeting registration.
        :type customized_questions: CustomizedQuestionForCreateMeeting
        :param rules: The approval rule for standard questions.
        :type rules: StandardRegistrationApproveRule

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-registration-form
        """
        body = UpdateMeetingRegistrationFormBody()
        if host_email is not None:
            body.host_email = host_email
        if require_first_name is not None:
            body.require_first_name = require_first_name
        if require_last_name is not None:
            body.require_last_name = require_last_name
        if require_email is not None:
            body.require_email = require_email
        if require_job_title is not None:
            body.require_job_title = require_job_title
        if require_company_name is not None:
            body.require_company_name = require_company_name
        if require_address1 is not None:
            body.require_address1 = require_address1
        if require_address2 is not None:
            body.require_address2 = require_address2
        if require_city is not None:
            body.require_city = require_city
        if require_state is not None:
            body.require_state = require_state
        if require_zip_code is not None:
            body.require_zip_code = require_zip_code
        if require_country_region is not None:
            body.require_country_region = require_country_region
        if require_work_phone is not None:
            body.require_work_phone = require_work_phone
        if require_fax is not None:
            body.require_fax = require_fax
        if max_register_num is not None:
            body.max_register_num = max_register_num
        if customized_questions is not None:
            body.customized_questions = customized_questions
        if rules is not None:
            body.rules = rules
        url = self.ep(f'{meeting_id}/registration')
        data = super().put(url=url, data=body.json())
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def delete_registration_form(self, meeting_id: str):
        """
        Disable the registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-meeting-registration-form
        """
        url = self.ep(f'{meeting_id}/registration')
        super().delete(url=url)
        return

    def register_registrant(self, meeting_id: str, first_name: str, last_name: str = None, email: str = None, job_title: str = None, company_name: str = None, address1: str = None, address2: str = None, city: str = None, state: str = None, zip_code: str = None, country_region: str = None, work_phone: str = None, fax: str = None, send_email: bool = None, customized_questions: CustomizedRegistrant = None) -> RegisterMeetingRegistrantResponse:
        """
        Register a new registrant for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param first_name: The registrant's first name.
        :type first_name: str
        :param last_name: If the value is lastName, this approval rule applies to the standard question of "Last Name".
        :type last_name: str
        :param email: If the value is email, this approval rule applies to the standard question of "Email".
        :type email: str
        :param job_title: If the value is jobTitle, this approval rule applies to the standard question of "Job Title".
        :type job_title: str
        :param company_name: If the value is companyName, this approval rule applies to the standard question of
            "Company Name".
        :type company_name: str
        :param address1: If the value is address1, this approval rule applies to the standard question of "Address 1".
        :type address1: str
        :param address2: If the value is address2, this approval rule applies to the standard question of "Address 2".
        :type address2: str
        :param city: If the value is city, this approval rule applies to the standard question of "City".
        :type city: str
        :param state: If the value is state, this approval rule applies to the standard question of "State".
        :type state: str
        :param zip_code: If the value is zipCode, this approval rule applies to the standard question of "Zip/Post
            Code".
        :type zip_code: str
        :param country_region: If the value is countryRegion, this approval rule applies to the standard question of
            "Country Region".
        :type country_region: str
        :param work_phone: If the value is workPhone, this approval rule applies to the standard question of "Work
            Phone".
        :type work_phone: str
        :param fax: If the value is fax, this approval rule applies to the standard question of "Fax".
        :type fax: str
        :param send_email: If true send email to the registrant. Default: true.
        :type send_email: bool
        :param customized_questions: The registrant's answers for customized questions. Registration options define
            whether or not this is required.
        :type customized_questions: CustomizedRegistrant

        documentation: https://developer.webex.com/docs/api/v1/meetings/register-a-meeting-registrant
        """
        body = RegisterMeetingRegistrantBody()
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if email is not None:
            body.email = email
        if job_title is not None:
            body.job_title = job_title
        if company_name is not None:
            body.company_name = company_name
        if address1 is not None:
            body.address1 = address1
        if address2 is not None:
            body.address2 = address2
        if city is not None:
            body.city = city
        if state is not None:
            body.state = state
        if zip_code is not None:
            body.zip_code = zip_code
        if country_region is not None:
            body.country_region = country_region
        if work_phone is not None:
            body.work_phone = work_phone
        if fax is not None:
            body.fax = fax
        if send_email is not None:
            body.send_email = send_email
        if customized_questions is not None:
            body.customized_questions = customized_questions
        url = self.ep(f'{meeting_id}/registrants')
        data = super().post(url=url, data=body.json())
        return RegisterMeetingRegistrantResponse.parse_obj(data)

    def batch_register_registrants(self, meeting_id: str, items: RegisterMeetingRegistrantBody = None) -> list[RegisterMeetingRegistrantResponse]:
        """
        Bulk register new registrants for a meeting.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param items: Registrants array.
        :type items: RegisterMeetingRegistrantBody

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-register-meeting-registrants
        """
        body = BatchRegisterMeetingRegistrantsBody()
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/registrants/bulkInsert')
        data = super().post(url=url, data=body.json())
        return parse_obj_as(list[RegisterMeetingRegistrantResponse], data["items"])

    def getmeeting_registrants_detail_information(self, meeting_id: str, registrant_id: str) -> GetmeetingRegistrantsDetailInformationResponse:
        """
        Retrieves details for a meeting registrant with a specified registrant Id.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-registrant's-detail-information
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        data = super().get(url=url)
        return GetmeetingRegistrantsDetailInformationResponse.parse_obj(data)

    def list_registrants(self, meeting_id: str, email: str = None, register_time_from: str = None, register_time_to: str = None, **params) -> Generator[GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can retrieve the list of registrants for a meeting with a specified meeting Id.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param email: Registrant's email to filter registrants.
        :type email: str
        :param register_time_from: The time registrants register a meeting starts from the specified date and time
            (inclusive) in any ISO 8601 compliant format. If registerTimeFrom is not specified, it equals
            registerTimeTo minus 7 days.
        :type register_time_from: str
        :param register_time_to: The time registrants register a meeting before the specified date and time (exclusive)
            in any ISO 8601 compliant format. If registerTimeTo is not specified, it equals registerTimeFrom plus 7
            days. The interval between registerTimeFrom and registerTimeTo must be within 90 days.
        :type register_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-registrants
        """
        if email is not None:
            params['email'] = email
        if register_time_from is not None:
            params['registerTimeFrom'] = register_time_from
        if register_time_to is not None:
            params['registerTimeTo'] = register_time_to
        url = self.ep(f'{meeting_id}/registrants')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse, params=params)

    def query_registrants(self, meeting_id: str, emails: List[str], status: Status2 = None, order_type: OrderType = None, order_by: OrderBy = None, **params) -> Generator[GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can query the list of registrants for a meeting with a specified meeting ID and
        registrants email.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param emails: List of registrant email addresses. Possible values: bob@example.com
        :type emails: List[str]
        :param status: Registrant's status.
        :type status: Status2
        :param order_type: Sort order for the registrants.
        :type order_type: OrderType
        :param order_by: Registrant ordering field. Ordered by registrationTime by default.
        :type order_by: OrderBy

        documentation: https://developer.webex.com/docs/api/v1/meetings/query-meeting-registrants
        """
        body = QueryMeetingRegistrantsBody()
        if emails is not None:
            body.emails = emails
        if status is not None:
            body.status = status
        if order_type is not None:
            body.order_type = order_type
        if order_by is not None:
            body.order_by = order_by
        url = self.ep(f'{meeting_id}/registrants/query')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse, params=params, data=body.json())

    def batch_update_registrants_status(self, meeting_id: str, status_op_type: str, send_email: bool = None, registrants: List[Registrants] = None):
        """
        Meeting's host or cohost can update the set of registrants for a meeting. cancel means the registrant(s) will
        be moved back to the registration list. bulkDelete means the registrant(s) will be deleted.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param status_op_type: Update registrant's status. Possible values: approve, reject, cancel, bulkDelete
        :type status_op_type: str
        :param send_email: If true send email to registrants. Default: true.
        :type send_email: bool
        :param registrants: Registrants array. Registrant ID.
        :type registrants: List[Registrants]

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-update-meeting-registrants-status
        """
        body = BatchUpdateMeetingRegistrantsStatusBody()
        if send_email is not None:
            body.send_email = send_email
        if registrants is not None:
            body.registrants = registrants
        url = self.ep(f'{meeting_id}/registrants/{status_op_type}')
        super().post(url=url, data=body.json())
        return

    def delete_registrant(self, meeting_id: str, registrant_id: str):
        """
        Meeting's host or cohost can delete a registrant with a specified registrant ID.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant.
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-registrant
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        super().delete(url=url)
        return

    def update_simultaneous_interpretation(self, meeting_id: str, enabled: bool, interpreters: InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting = None) -> SimultaneousInterpretation1:
        """
        Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to
        meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param enabled: Whether or not simultaneous interpretation is enabled.
        :type enabled: bool
        :param interpreters: Interpreters for meeting.
        :type interpreters: InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-simultaneous-interpretation
        """
        body = SimultaneousInterpretation()
        if enabled is not None:
            body.enabled = enabled
        if interpreters is not None:
            body.interpreters = interpreters
        url = self.ep(f'{meeting_id}/simultaneousInterpretation')
        data = super().put(url=url, data=body.json())
        return SimultaneousInterpretation1.parse_obj(data)

    def create_interpreter(self, meeting_id: str, language_code1: str, language_code2: str, email: str = None, display_name: str = None, host_email: str = None, send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Assign an interpreter to a bi-directional simultaneous interpretation language channel for a meeting.

        :param meeting_id: Unique identifier for the meeting to which the interpreter is to be assigned.
        :type meeting_id: str
        :param language_code1: Forms a set of simultaneous interpretation channels together with languageCode2.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code1: str
        :param language_code2: Forms a set of simultaneous interpretation channels together with languageCode1.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code2: str
        :param email: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room
            Options API. Possible values: john.andersen@example.com
        :type email: str
        :param display_name: Display name for cohost. This attribute can be modified with the Update Personal Meeting
            Room Options API. Possible values: John Andersen
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().post(url=url, data=body.json())
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Retrieves details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting to which the interpreter has been assigned.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for an interpreter of the meeting that is hosted by that
            user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().get(url=url, params=params)
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def list_interpreters(self, meeting_id: str, host_email: str = None) -> list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]:
        """
        Lists meeting interpreters for a meeting with a specified meetingId.
        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        If the specified meetingId is for a meeting series, the interpreters for the series will be listed; if the
        meetingId is for a scheduled meeting, the interpreters for the particular scheduled meeting will be listed; if
        the meetingId is for an ended or ongoing meeting instance, the interpreters for the particular meeting instance
        will be listed. See the Webex Meetings guide for more information about the types of meetings.
        The list returned is sorted in descending order by when interpreters were created.

        :param meeting_id: Unique identifier for the meeting for which interpreters are being requested. The meeting
            can be meeting series, scheduled meeting or meeting instance which has ended or is ongoing. Please note
            that currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return interpreters of the meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-interpreters
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting], data["items"])

    def update_interpreter(self, meeting_id: str, interpreter_id: str, language_code1: str, language_code2: str, email: str = None, display_name: str = None, host_email: str = None, send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Updates details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param language_code1: Forms a set of simultaneous interpretation channels together with languageCode2.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code1: str
        :param language_code2: Forms a set of simultaneous interpretation channels together with languageCode1.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code2: str
        :param email: Email address for cohost. This attribute can be modified with the Update Personal Meeting Room
            Options API. Possible values: john.andersen@example.com
        :type email: str
        :param display_name: Display name for cohost. This attribute can be modified with the Update Personal Meeting
            Room Options API. Possible values: John Andersen
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().put(url=url, data=body.json())
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def delete_interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting interpreter identified by meetingId and interpreterId in the URI. The deleted meeting
        interpreter cannot be recovered.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter to be removed.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete an interpreter of the meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        super().delete(url=url, params=params)
        return

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

    def survey(self, meeting_id: str) -> GetMeetingSurveyResponse:
        """
        Retrieves details for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-survey
        """
        url = self.ep(f'{meeting_id}/survey')
        data = super().get(url=url)
        return GetMeetingSurveyResponse.parse_obj(data)

    def list_survey_results(self, meeting_id: str, meeting_start_time_from: str = None, meeting_start_time_to: str = None, **params) -> Generator[SurveyResultObject, None, None]:
        """
        Retrieves results for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Start date and time (inclusive) in any ISO 8601 compliant format for the
            meeting objects being requested. meetingStartTimeFrom cannot be after meetingStartTimeTo. This parameter
            will be ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is
            not the unique identifier for the specific meeting instance, the meetingStartTimeFrom, if not specified,
            equals meetingStartTimeTo minus 1 month; if meetingStartTimeTo is also not specified, the default value for
            meetingStartTimeFrom is 1 month before the current date and time.
        :type meeting_start_time_from: str
        :param meeting_start_time_to: End date and time (exclusive) in any ISO 8601 compliant format for the meeting
            objects being requested. meetingStartTimeTo cannot be prior to meetingStartTimeFrom. This parameter will be
            ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is not the
            unique identifier for the specific meeting instance, if meetingStartTimeFrom is also not specified, the
            default value for meetingStartTimeTo is the current date and time;For example,if meetingStartTimeFrom is a
            month ago, the default value for meetingStartTimeTo is 1 month after meetingStartTimeFrom.Otherwise it is
            the current date and time.
        :type meeting_start_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-survey-results
        """
        if meeting_start_time_from is not None:
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return self.session.follow_pagination(url=url, model=SurveyResultObject, params=params)

    def create_invitation_sources(self, meeting_id: str, host_email: str = None, person_id: str = None, items: InvitationSourceCreateObject = None) -> list[InvitationSourceObject]:
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

    def list_invitation_sources(self, meeting_id: str) -> list[InvitationSourceObject]:
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

    def list_tracking_codes(self, service: str, site_url: str = None, host_email: str = None) -> ListMeetingTrackingCodesResponse:
        """
        Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options
        can be used to create or update a meeting on the specified site.

        :param service: Service for schedule or sign-up pages.
        :type service: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by Get Site List API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes
        """
        params = {}
        params['service'] = service
        if site_url is not None:
            params['siteUrl'] = site_url
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('trackingCodes')
        data = super().get(url=url, params=params)
        return ListMeetingTrackingCodesResponse.parse_obj(data)

class MeetingUsageReportObject(ApiModel):
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: Meeting number.
    meeting_number: Optional[str]
    #: Meeting title.
    meeting_title: Optional[str]
    #: The date and time when the meeting was started. It's in the timezone specified in the request header or in the
    #: UTC timezone if timezone is not specified.
    start: Optional[str]
    #: The date and time when the meeting was ended. It's in the timezone specified in the request header or in the UTC
    #: timezone if timezone is not specified.
    end: Optional[str]
    #: Duration of the meeting in minutes.
    duration: Optional[int]
    #: Scheduled type for the meeting.
    scheduled_type: Optional[TemplateType]
    #: Display name for the meeting host.
    host_display_name: Optional[str]
    #: Email address for the meeting host.
    host_email: Optional[str]
    #: Aggregated attendee minutes.
    total_people_minutes: Optional[int]
    #: Aggregated attendee PSTN call-in minutes.
    total_call_in_minutes: Optional[int]
    #: Aggregated attendee domestic PSTN call-out minutes.
    total_call_out_domestic: Optional[int]
    #: Aggregated attendee toll-free PSTN call-in minutes.
    total_call_in_toll_free_minutes: Optional[int]
    #: Aggregated attendee international PSTN call-out minutes.
    total_call_out_international: Optional[int]
    #: Aggregated attendee VoIP minutes.
    total_voip_minutes: Optional[int]
    #: Total number of participants of the meeting.
    total_participants: Optional[int]
    #: Total number of VoIP participants of the meeting.
    total_participants_voip: Optional[int]
    #: Total number of PSTN call-in participants of the meeting.
    total_participants_call_in: Optional[int]
    #: Total number of PSTN call-out participants of the meeting.
    total_participants_call_out: Optional[int]
    #: Peak number of attendees throughout the meeting.
    peak_attendee: Optional[int]
    #: Total number of registrants of the meeting.
    total_registered: Optional[int]
    #: Total number of invitees of the meeting.
    total_invitee: Optional[int]
    #: Tracking codes of the meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]


class ParticipantType(str, Enum):
    #: Meeting host.
    host = 'host'
    #: Meeting attendee.
    attendee = 'attendee'


class MeetingAttendeeReportObject(CoHosts):
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: Meeting number.
    meeting_number: Optional[int]
    #: Meeting title.
    meeting_title: Optional[str]
    #: The date and time when the attendee joined the meeting. It's in the timezone specified in the request header or
    #: in the UTC timezone if timezone is not specified.
    joined_time: Optional[str]
    #: The date and time when the attendee left the meeting. It's in the timezone specified in the request header or in
    #: the UTC timezone if timezone is not specified.
    left_time: Optional[str]
    #: Duration of the attendee in the meeting in minutes.
    duration: Optional[int]
    #: The attendee's role in the meeting.
    participant_type: Optional[ParticipantType]
    #: IP address of the attendee when he attended the meeting.
    ip_address: Optional[str]
    #: Information of the attendee's operating system and application when he attended the meeting.
    client_agent: Optional[str]
    #: Attendee's company.
    company: Optional[str]
    #: Attendee's phone number.
    phone_number: Optional[str]
    #: Attendee's address, part one.
    address1: Optional[str]
    #: Attendee's address, part two.
    address2: Optional[str]
    #: Attendee's city.
    city: Optional[str]
    #: Attendee's state.
    state: Optional[str]
    #: Attendee's country.
    country: Optional[str]
    #: Attendee's zip code.
    zip_code: Optional[str]
    #: Whether or not the attendee has registered the meeting.
    registered: Optional[bool]
    #: Whether or not the attendee has been invited to the meeting.
    invited: Optional[bool]


class ListMeetingUsageReportsResponse(ApiModel):
    #: An array of meeting usage report objects.
    items: Optional[list[MeetingUsageReportObject]]


class ListMeetingAttendeeReportsResponse(ApiModel):
    #: An array of meeting attendee report objects.
    items: Optional[list[MeetingAttendeeReportObject]]


class MeetingsSummaryReportApi(ApiChild, base='meetingReports/'):
    """
    The meeting usage report API is used to retrieve aggregated meeting usage information, like totalCallInMinutes,
    totalParticipants, etc. It also includes the meeting trackingCodes.
    The meeting attendee report API is used to retrieve aggregated meeting attendee information, like joinedTime,
    leftTime, duration, etc.
    The report data for a meeting should be available within 24 hours after the meeting ended.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_meeting_usage_reports(self, site_url: str, from_: str = None, to_: str = None, **params) -> Generator[MeetingUsageReportObject, None, None]:
        """
        List meeting usage reports of all the users on the specified site by an admin. You can specify a date range and
        the maximum number of meeting usage reports to return.
        The list returned is sorted in descending order by the date and time the meetings were started.
        Long result sets are split into pages.

        :param site_url: URL of the Webex site which the API lists meeting usage reports from. All available Webex
            sites can be retrieved by the Get Site List API.
        :type site_url: str
        :param from_: Starting date and time for meeting usage reports to return, in any ISO 8601 compliant format.
            from cannot be after to. The interval between to and from cannot exceed 30 days and from cannot be earlier
            than 90 days ago.
        :type from_: str
        :param to_: Ending date and time for meeting usage reports to return, in any ISO 8601 compliant format. to
            cannot be before from. The interval between to and from cannot exceed 30 days.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meetings-summary-report/list-meeting-usage-reports
        """
        params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('usage')
        return self.session.follow_pagination(url=url, model=MeetingUsageReportObject, params=params)

    def list_meeting_attendee_reports(self, site_url: str, meeting_id: str = None, meeting_number: str = None, meeting_title: str = None, from_: str = None, to_: str = None, **params) -> Generator[MeetingAttendeeReportObject, None, None]:
        """
        Lists of meeting attendee reports by a date range, the maximum number of meeting attendee reports, a meeting
        ID, a meeting number or a meeting title.
        If the requesting user is an admin, the API returns meeting attendee reports of the meetings hosted by all the
        users on the specified site filtered by meeting ID, meeting number or meeting title.
        If it's a normal meeting host, the API returns meeting attendee reports of the meetings hosted by the user
        himself on the specified site filtered by meeting ID, meeting number or meeting title.
        The list returned is grouped by meeting instances. Both the groups and items of each group are sorted in
        descending order of joinedTime. For example, if meetingId is specified and it's a meeting series ID, the
        returned list is grouped by meeting instances of that series. The groups are sorted in descending order of
        joinedTime, and within each group the items are also sorted in descending order of joinedTime. Please refer to
        Meetings Overview for details of meeting series, scheduled meeting and meeting instance.
        Long result sets are split into pages.

        :param site_url: URL of the Webex site which the API lists meeting attendee reports from. All available Webex
            sites can be retrieved by the Get Site List API.
        :type site_url: str
        :param meeting_id: Meeting ID for the meeting attendee reports to return. If specified, return meeting attendee
            reports of the specified meeting; otherwise, return meeting attendee reports of all meetings. Currently,
            only ended meeting instance IDs are supported. IDs of meeting series, scheduled meetings or personal room
            meetings are not supported.
        :type meeting_id: str
        :param meeting_number: Meeting number for the meeting attendee reports to return. If specified, return meeting
            attendee reports of the specified meeting; otherwise, return meeting attendee reports of all meetings.
        :type meeting_number: str
        :param meeting_title: Meeting title for the meeting attendee reports to return. If specified, return meeting
            attendee reports of the specified meeting; otherwise, return meeting attendee reports of all meetings.
        :type meeting_title: str
        :param from_: Starting date and time for the meeting attendee reports to return, in any ISO 8601 compliant
            format. from cannot be after to. The interval between to and from cannot exceed 30 days and from cannot be
            earlier than 90 days ago.
        :type from_: str
        :param to_: Ending date and time for the meeting attendee reports to return, in any ISO 8601 compliant format.
            to cannot be before from. The interval between to and from cannot exceed 30 days.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meetings-summary-report/list-meeting-attendee-reports
        """
        params['siteUrl'] = site_url
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if meeting_title is not None:
            params['meetingTitle'] = meeting_title
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('attendees')
        return self.session.follow_pagination(url=url, model=MeetingAttendeeReportObject, params=params)

class PhoneNumbers(ApiModel):
    #: The type of phone number.
    #: Possible values: work, mobile, fax
    type: Optional[str]
    #: The phone number.
    #: Possible values: +1 408 526 7209
    value: Optional[str]


class SipAddressesType(PhoneNumbers):
    primary: Optional[bool]


class Status16(str, Enum):
    #: The webhook is active.
    active = 'active'
    #: The webhook is inactive.
    inactive = 'inactive'


class Status8(Status16):
    #: The user is in a call
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: The user is in a meeting
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined
    pending = 'pending'
    #: The user is sharing content
    presenting = 'presenting'
    #: The user’s status could not be determined
    unknown = 'unknown'


class Type14(str, Enum):
    #: Account belongs to a person
    person = 'person'
    #: Account is a bot user
    bot = 'bot'
    #: Account is a guest user
    appuser = 'appuser'


class CreatePersonBody(ApiModel):
    #: The email addresses of the person. Only one email address is allowed per person.
    #: Possible values: john.andersen@example.com
    emails: Optional[list[str]]
    #: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling license.
    phone_numbers: Optional[list[PhoneNumbers]]
    #: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license.
    extension: Optional[str]
    #: The ID of the location for this person.
    location_id: Optional[str]
    #: The full name of the person.
    display_name: Optional[str]
    #: The first name of the person.
    first_name: Optional[str]
    #: The last name of the person.
    last_name: Optional[str]
    #: The URL to the person's avatar in PNG format.
    avatar: Optional[str]
    #: The ID of the organization to which this person belongs.
    org_id: Optional[str]
    #: An array of role strings representing the roles to which this admin user belongs.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    licenses: Optional[list[str]]
    #: The business department the user belongs to.
    department: Optional[str]
    #: A manager identifier.
    manager: Optional[str]
    #: Person Id of the manager
    manager_id: Optional[str]
    #: the person's title
    title: Optional[str]
    #: Person's address
    #: Possible values: , country: `US`, locality: `Charlotte`, region: `North Carolina`, streetAddress: `1099 Bird
    #: Ave.`, type: `work`, postalCode: `99212`
    addresses: Optional[list[object]]
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg:
    #: mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]]


class Person(CreatePersonBody):
    #: A unique identifier for the person.
    id: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    nick_name: Optional[str]
    #: The date and time the person was created.
    created: Optional[str]
    #: The date and time the person was last changed.
    last_modified: Optional[str]
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user has
    #: disabled status sharing.
    last_activity: Optional[str]
    #: The users sip addresses
    sip_addresses: Optional[list[SipAddressesType]]
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has disabled status
    #: sharing.
    status: Optional[Status8]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    type: Optional[Type14]


class ListPeopleResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]]
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]]


class UpdatePersonBody(CreatePersonBody):
    #: The nickname of the person if configured. Set to the firstName automatically in update request.
    nick_name: Optional[str]
    #: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is
    #: an admin user for the person's organization.
    login_enabled: Optional[bool]


class PeopleApi(ApiChild, base='people'):
    """
    People are registered users of Webex. Searching and viewing People requires an auth token with a scope of
    spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token with
    spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token with the
    spark-admin:people_write and spark-admin:people_read scope.
    A person's call settings are for Webex Calling and necessitate Webex Calling licenses.
    To learn more about managing people in a room see the Memberships API. For information about how to allocate Hybrid
    Services licenses to people, see the Managing Hybrid Services guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, roles: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=
        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.
        Lookup by roles is only supported for Admin users for the people within the same org.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required. With the exception of partner admins and a managed org relationship, people lookup by email is
            only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided
            then presence information (such as the lastActivity or status properties) will not be included in the
            response.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/list-people
        """
        if email is not None:
            params['email'] = email
        if display_name is not None:
            params['displayName'] = display_name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        if roles is not None:
            params['roles'] = roles
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Person, params=params)

    def create(self, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: List[object] = None, site_urls: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.
        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.
        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        When doing attendee management, append #attendee to the siteUrl parameter (e.g. mysite.webex.com#attendee) to
        make the new user an attendee for a site.

        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address Possible values: , country: `US`, locality: `Charlotte`, region: `North
            Carolina`, streetAddress: `1099 Bird Ave.`, type: `work`, postalCode: `99212`
        :type addresses: List[object]
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]

        documentation: https://developer.webex.com/docs/api/v1/people/create-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        body = CreatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-person-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, emails: List[str], calling_data: bool = None, show_all_types: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: List[object] = None, site_urls: List[str] = None, nick_name: str = None, login_enabled: bool = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is
        already an existing calling user.
        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to
        the respective siteUrl and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the siteurl parameter.
        To remove the attendee privilege for a user on a meeting site, remove the sitename#attendee from the siteUrls
        array. The showAllTypes parameter must be set to true.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address Possible values: , country: `US`, locality: `Charlotte`, region: `North
            Carolina`, streetAddress: `1099 Bird Ave.`, type: `work`, postalCode: `99212`
        :type addresses: List[object]
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        :param nick_name: The nickname of the person if configured. Set to the firstName automatically in update
            request.
        :type nick_name: str
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the
            authenticated user is an admin user for the person's organization.
        :type login_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/people/update-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        body = UpdatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        if nick_name is not None:
            body.nick_name = nick_name
        if login_enabled is not None:
            body.login_enabled = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def delete(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/delete-a-person
        """
        url = self.ep(f'{person_id}')
        super().delete(url=url)
        return

    def my_own_details(self, calling_data: bool = None) -> Person:
        """
        Get profile details for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-my-own-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

class Format(str, Enum):
    #: Recording file format is MP4.
    mp4 = 'MP4'
    #: Recording file format is ARF, a private format of Webex recordings. This format requires the Cisco ARF recording
    #: player.
    arf = 'ARF'


class RecordingObject(ApiModel):
    #: A unique identifier for the recording.
    id: Optional[str]
    #: Unique identifier for the parent ended meeting instance which the recording belongs to.
    meeting_id: Optional[str]
    #: Unique identifier for the parent scheduled meeting which the recording belongs to.
    scheduled_meeting_id: Optional[str]
    #: Unique identifier for the parent meeting series which the recording belongs to.
    meeting_series_id: Optional[str]
    #: The recording's topic.
    topic: Optional[str]
    #: The date and time recording was created in ISO 8601 compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    create_time: Optional[str]
    #: The date and time recording started in ISO 8601 compliant format. It indicates when the record button was
    #: clicked in the meeting.
    time_recorded: Optional[str]
    #: Site URL for the recording.
    site_url: Optional[str]
    #: The download link for recording. This attribute is not available if Prevent downloading has been turned on for
    #: the recording being requested. The Prevent downloading option can be viewed and set by a site admin on Control
    #: Hub.
    download_url: Optional[str]
    #: The playback link for recording.
    playback_url: Optional[str]
    #: The recording's password.
    password: Optional[str]
    format: Optional[Format]
    service_type: Optional[ServiceType]
    #: The duration of the recording, in seconds.
    duration_seconds: Optional[int]
    #: The size of the recording file, in bytes.
    size_bytes: Optional[int]
    #: Whether or not the recording has been shared to the current user.
    share_to_me: Optional[bool]
    #: External keys of the parent meeting created by an integration application. They could be Zendesk ticket IDs,
    #: Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries recordings by a key in its own
    #: domain.
    integration_tags: Optional[list[str]]
    status: Optional[Status]


class TemporaryDirectDownloadLinks(ApiModel):
    #: The download link for recording MP4 file without HTML page rendering in browser or HTTP redirect. Expires 3
    #: hours after the API request.
    recording_download_link: Optional[str]
    #: The download link for recording audio file without HTML page rendering in browser or HTTP redirect. Expires 3
    #: hours after the API request.
    audio_download_link: Optional[str]
    #: The download link for recording transcript file without HTML page rendering in browser or HTTP redirect. Expires
    #: 3 hours after the API request.
    transcript_download_link: Optional[str]
    #: The date and time when recordingDownloadLink, audioDownloadLink, and transcriptDownloadLink expire in ISO 8601
    #: compliant format.
    expiration: Optional[str]


class MoveRecordingsIntoRecycleBinBody(ApiModel):
    #: Recording IDs for removing recordings into the recycle bin in batch. Please note that all the recording IDs
    #: should belong to the site of siteUrl or the user's preferred site if siteUrl is not specified.
    recording_ids: Optional[list[str]]
    #: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes recordings from
    #: the user's preferred site. All available Webex sites and preferred sites of a user can be retrieved by the Get
    #: Site List API.
    site_url: Optional[str]


class ListRecordingsResponse(ApiModel):
    #: An array of recording objects.
    items: Optional[list[RecordingObject]]


class ListRecordingsForAdminOrComplianceOfficerResponse(ApiModel):
    #: An array of recording objects.
    items: Optional[list[RecordingObject]]


class GetRecordingDetailsResponse(RecordingObject):
    #: The download links for MP4, audio, and transcript of the recording without HTML page rendering in browser or
    #: HTTP redirect. This attribute is not available if Prevent Downloading has been turned on for the recording being
    #: requested. The Prevent Downloading option can be viewed and set on page when editing a recording. Note that
    #: there are various products in Webex Suite such as "Webex Meetings", "Webex Training" and "Webex Events".
    #: Currently, this attribute is only available for Webex Meetings.
    temporary_direct_download_links: Optional[TemporaryDirectDownloadLinks]


class RestoreRecordingsFromRecycleBinBody(MoveRecordingsIntoRecycleBinBody):
    #: If not specified or false, restores the recordings specified by recordingIds. If true, restores all recordings
    #: from the recycle bin.
    restore_all: Optional[bool]


class PurgeRecordingsFromRecycleBinBody(MoveRecordingsIntoRecycleBinBody):
    #: If not specified or false, purges the recordings specified by recordingIds. If true, purges all recordings from
    #: the recycle bin.
    purge_all: Optional[bool]


class RecordingsApi(ApiChild, base=''):
    """
    Recordings are meeting content captured in a meeting or files uploaded via the upload page for your Webex site.
    This API manages recordings. Recordings may be retrieved via download or playback links defined by downloadUrl or
    playbackUrl in the response body.
    When the recording function is paused in the meeting the recording will not contain the pause. If the recording
    function is stopped and restarted in the meeting, several recordings will be created. These recordings will be
    consolidate and available all at once.
    Refer to the Meetings API Scopes for the specific scopes required for each API.
    """

    def list(self, from_: str = None, to_: str = None, meeting_id: str = None, host_email: str = None, site_url: str = None, integration_tag: str = None, topic: str = None, format: str = None, service_type: str = None, status: str = None, **params) -> Generator[RecordingObject, None, None]:
        """
        Lists recordings. You can specify a date range, a parent meeting ID, and the maximum number of recordings to
        return.
        Only recordings of meetings hosted by or shared with the authenticated user will be listed.
        The list returned is sorted in descending order by the date and time that the recordings were created.
        Long result sets are split into pages.

        :param from_: Starting date and time (inclusive) for recordings to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List recordings to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str
        :param meeting_id: Unique identifier for the parent meeting series, scheduled meeting, or meeting instance for
            which recordings are being requested. If a meeting series ID is specified, the operation returns an array
            of recordings for the specified meeting series. If a scheduled meeting ID is specified, the operation
            returns an array of recordings for the specified scheduled meeting. If a meeting instance ID is specified,
            the operation returns an array of recordings for the specified meeting instance. If no ID is specified, the
            operation returns an array of recordings for all meetings of the current user. When meetingId is specified,
            the siteUrl parameter is ignored.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the required admin-level meeting scopes. If set, the admin may specify the email of a
            user in a site they manage and the API will return recordings of that user.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists recordings. If not specified, the API lists
            recordings from all of a user's sites. All available Webex sites and the preferred site of the user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param integration_tag: External key of the parent meeting created by an integration application. This
            parameter is used by the integration application to query recordings by a key in its own domain, such as a
            Zendesk ticket ID, a Jira ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str
        :param topic: Recording's topic. If specified, the API filters recordings by topic in a case-insensitive
            manner.
        :type topic: str
        :param format: Recording's file format. If specified, the API filters recordings by format. Valid values are
            MP4 or ARF.
        :type format: str
        :param service_type: Recording's service-type. If this item is specified, the API filters recordings by
            service-type. Valid values:
        :type service_type: str
        :param status: Recording's status. If not specified or available, retrieves recordings that are available.
            Otherwise, if specified as deleted, retrieves recordings that have been moved into the recycle bin.
            Possible values: available, deleted
        :type status: str

        documentation: https://developer.webex.com/docs/api/v1/recordings/list-recordings
        """
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        if topic is not None:
            params['topic'] = topic
        if format is not None:
            params['format'] = format
        if service_type is not None:
            params['serviceType'] = service_type
        if status is not None:
            params['status'] = status
        url = self.ep('recordings')
        return self.session.follow_pagination(url=url, model=RecordingObject, params=params)

    def list_for_admin_or_compliance_officer(self, from_: str = None, to_: str = None, meeting_id: str = None, site_url: str = None, integration_tag: str = None, topic: str = None, format: str = None, service_type: str = None, status: str = None, **params) -> Generator[RecordingObject, None, None]:
        """
        List recordings for an admin or compliance officer. You can specify a date range, a parent meeting ID, and the
        maximum number of recordings to return.
        The list returned is sorted in descending order by the date and time that the recordings were created.
        Long result sets are split into pages.

        :param from_: Starting date and time (inclusive) for recordings to return, in any ISO 8601 compliant format.
            from cannot be after to. The interval between from and to must be within 30 days.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List recordings to return, in any ISO 8601 compliant format.
            to cannot be before from. The interval between from and to must be within 30 days.
        :type to_: str
        :param meeting_id: Unique identifier for the parent meeting series, scheduled meeting, or meeting instance for
            which recordings are being requested. If a meeting series ID is specified, the operation returns an array
            of recordings for the specified meeting series. If a scheduled meeting ID is specified, the operation
            returns an array of recordings for the specified scheduled meeting. If a meeting instance ID is specified,
            the operation returns an array of recordings for the specified meeting instance. If not specified, the
            operation returns an array of recordings for all the current user's meetings. When meetingId is specified,
            the siteUrl parameter is ignored.
        :type meeting_id: str
        :param site_url: URL of the Webex site which the API lists recordings from. If not specified, the API lists
            recordings from user's preferred site. All available Webex sites and preferred site of the user can be
            retrieved by Get Site List API.
        :type site_url: str
        :param integration_tag: External key of the parent meeting created by an integration application. This
            parameter is used by the integration application to query recordings by a key in its own domain such as a
            Zendesk ticket ID, a Jira ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str
        :param topic: Recording topic. If specified, the API filters recordings by topic in a case-insensitive manner.
        :type topic: str
        :param format: Recording's file format. If specified, the API filters recordings by format. Valid values: MP4
            or ARF.
        :type format: str
        :param service_type: Recording's service-type. If specified, the API filters recordings by service-type. Valid
            values:
        :type service_type: str
        :param status: Recording's status. If not specified or available, retrieves recordings that are available.
            Otherwise, if specified as deleted, retrieves recordings that have been moved to the recycle bin. Possible
            values: available, deleted
        :type status: str

        documentation: https://developer.webex.com/docs/api/v1/recordings/list-recordings-for-an-admin-or-compliance-officer
        """
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        if topic is not None:
            params['topic'] = topic
        if format is not None:
            params['format'] = format
        if service_type is not None:
            params['serviceType'] = service_type
        if status is not None:
            params['status'] = status
        url = self.ep('admin/recordings')
        return self.session.follow_pagination(url=url, model=RecordingObject, params=params)

    def recording_details(self, recording_id: str, host_email: str = None) -> GetRecordingDetailsResponse:
        """
        Retrieves details for a recording with a specified recording ID.
        Only recordings of meetings hosted by or shared with the authenticated user may be retrieved.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            required admin-level meeting scopes. If set, the admin may specify the email of a user in a site they
            manage, and the API will return recording details of that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/recordings/get-recording-details
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'recordings/{recording_id}')
        data = super().get(url=url, params=params)
        return GetRecordingDetailsResponse.parse_obj(data)

    def delete_recording(self, recording_id: str, host_email: str = None, reason: str = None, comment: str = None):
        """
        Removes a recording with a specified recording ID. The deleted recording cannot be recovered. If a Compliance
        Officer deletes another user's recording, the recording will be inaccessible to regular users (host, attendees
        and shared), but will be still available to the Compliance Officer.
        Only recordings of meetings hosted by the authenticated user can be deleted.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required admin-level meeting scopes. If set, the admin may specify the email of a user in a site they
            manage and the API will delete a recording of that user.
        :type host_email: str
        :param reason: Reason for deleting a transcript. Only required when a Compliance Officer is operating on
            another user's transcript.
        :type reason: str
        :param comment: Explanation for deleting a transcript. The comment can be a maximum of 255 characters long.
        :type comment: str

        documentation: https://developer.webex.com/docs/api/v1/recordings/delete-a-recording
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = DeleteTranscriptBody()
        if reason is not None:
            body.reason = reason
        if comment is not None:
            body.comment = comment
        url = self.ep(f'recordings/{recording_id}')
        super().delete(url=url, params=params, data=body.json())
        return

    def move_into_recycle_bin(self, recording_ids: List[str], host_email: str = None, site_url: str = None):
        """
        Move recordings into the recycle bin with recording IDs. Recordings in the recycle bin can be recovered by
        Restore Recordings from Recycle Bin API. If you'd like to empty recordings from the recycle bin, you can use
        Purge Recordings from Recycle Bin API to purge all or some of them.
        Only recordings of meetings hosted by the authenticated user can be moved into the recycle bin.

        :param recording_ids: Recording IDs for removing recordings into the recycle bin in batch. Please note that all
            the recording IDs should belong to the site of siteUrl or the user's preferred site if siteUrl is not
            specified.
        :type recording_ids: List[str]
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required admin-level meeting scopes. If set, the admin may specify the email of a user in a site they
            manage and the API will move recordings into recycle bin of that user
        :type host_email: str
        :param site_url: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes
            recordings from the user's preferred site. All available Webex sites and preferred sites of a user can be
            retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/recordings/move-recordings-into-the-recycle-bin
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = MoveRecordingsIntoRecycleBinBody()
        if recording_ids is not None:
            body.recording_ids = recording_ids
        if site_url is not None:
            body.site_url = site_url
        url = self.ep('recordings/softDelete')
        super().post(url=url, params=params, data=body.json())
        return

    def restore_from_recycle_bin(self, recording_ids: List[str], host_email: str = None, site_url: str = None, restore_all: bool = None):
        """
        Restore all or some recordings from the recycle bin. Only recordings of meetings hosted by the authenticated
        user can be restored from recycle bin.

        :param recording_ids: Recording IDs for removing recordings into the recycle bin in batch. Please note that all
            the recording IDs should belong to the site of siteUrl or the user's preferred site if siteUrl is not
            specified.
        :type recording_ids: List[str]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the required admin-level meeting scopes. If set, the admin may specify the email of a
            user in a site they manage and the API will restore recordings of that user.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes
            recordings from the user's preferred site. All available Webex sites and preferred sites of a user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param restore_all: If not specified or false, restores the recordings specified by recordingIds. If true,
            restores all recordings from the recycle bin.
        :type restore_all: bool

        documentation: https://developer.webex.com/docs/api/v1/recordings/restore-recordings-from-recycle-bin
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = RestoreRecordingsFromRecycleBinBody()
        if recording_ids is not None:
            body.recording_ids = recording_ids
        if site_url is not None:
            body.site_url = site_url
        if restore_all is not None:
            body.restore_all = restore_all
        url = self.ep('recordings/restore')
        super().post(url=url, params=params, data=body.json())
        return

    def purge_from_recycle_bin(self, recording_ids: List[str], host_email: str = None, site_url: str = None, purge_all: bool = None):
        """
        Purge recordings from recycle bin with recording IDs or purge all the recordings that are in the recycle bin.
        Only recordings of meetings hosted by the authenticated user can be purged from recycle bin.

        :param recording_ids: Recording IDs for removing recordings into the recycle bin in batch. Please note that all
            the recording IDs should belong to the site of siteUrl or the user's preferred site if siteUrl is not
            specified.
        :type recording_ids: List[str]
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required admin-level meeting scopes. If set, the admin may specify the email of a user in a site they
            manage and the API will purge recordings from recycle bin of that user.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes
            recordings from the user's preferred site. All available Webex sites and preferred sites of a user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param purge_all: If not specified or false, purges the recordings specified by recordingIds. If true, purges
            all recordings from the recycle bin.
        :type purge_all: bool

        documentation: https://developer.webex.com/docs/api/v1/recordings/purge-recordings-from-recycle-bin
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = PurgeRecordingsFromRecycleBinBody()
        if recording_ids is not None:
            body.recording_ids = recording_ids
        if site_url is not None:
            body.site_url = site_url
        if purge_all is not None:
            body.purge_all = purge_all
        url = self.ep('recordings/purge')
        super().post(url=url, params=params, data=body.json())
        return

class SiteSessionType(ApiModel):
    #: Site URL for the session type.
    site_url: Optional[str]


class Type19(Type6):
    #: Event Center.
    event_center = 'EventCenter'
    #: Support Center.
    support_center = 'SupportCenter'
    #: Training Center.
    train_center = 'TrainCenter'


class SessionType(ApiModel):
    #: The ID of the session type.
    id: Optional[str]
    #: The short name of the session type.
    short_name: Optional[str]
    #: The name of the session type.
    name: Optional[str]
    #: The meeting type of meeting that you can create with the session type.
    type: Optional[Type19]


class UserSessionTypes(ApiModel):
    #: A unique identifier for the user.
    person_id: Optional[str]
    #: The email of the user.
    email: Optional[str]
    #: Site URL for the user.
    site_url: Optional[str]
    #: All session types are supported by the user on the site.
    session_types: Optional[list[SessionType]]


class ListSiteSessionTypesResponse(ApiModel):
    #: An array of the site's session types.
    items: Optional[list[SiteSessionType]]


class ListUserSessionTypeResponse(ApiModel):
    #: An array of the user's session types.
    items: Optional[list[UserSessionTypes]]


class UpdateUserSessionTypesBody(ApiModel):
    #: Site URL for the session type.
    site_url: Optional[str]
    #: A unique identifier for the user.
    person_id: Optional[str]
    #: The email of the user.
    email: Optional[str]
    #: An array of the session type ID.
    #: Possible values: 3, 9
    session_type_ids: Optional[list[str]]


class SessionTypesApi(ApiChild, base='admin/meeting/'):
    """
    Session types define the features and options that are available to users for scheduled meetings.
    The API allows getting site-level session types and modifying user-level session types.
    Viewing the list of site session types and user session types requires an administrator auth token with
    meeting:admin_schedule_read or meeting:admin_config_read. Updating user session types requires an administrator
    auth token with the meeting:admin_schedule_write or meeting:admin_config_write scope.
    """

    def list_site_types(self, site_url: str = None) -> list[SiteSessionType]:
        """
        List session types for a specific site.

        :param site_url: URL of the Webex site to query. If siteUrl is not specified, the query will use the default
            site for the admin's authorization token used to make the call.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/session-types/list-site-session-types
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('config/sessionTypes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[SiteSessionType], data["items"])

    def list_user_type(self, site_url: str = None, person_id: str = None) -> list[UserSessionTypes]:
        """
        List session types for a specific user.

        :param site_url: URL of the Webex site to query.
        :type site_url: str
        :param person_id: A unique identifier for the user.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/session-types/list-user-session-type
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep('userconfig/sessionTypes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[UserSessionTypes], data["items"])

    def update_user_types(self, site_url: str, session_type_ids: List[str], person_id: str = None, email: str = None) -> UserSessionTypes:
        """
        Assign session types to specific users.

        :param site_url: Site URL for the session type.
        :type site_url: str
        :param session_type_ids: An array of the session type ID. Possible values: 3, 9
        :type session_type_ids: List[str]
        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param email: The email of the user.
        :type email: str

        documentation: https://developer.webex.com/docs/api/v1/session-types/update-user-session-types
        """
        body = UpdateUserSessionTypesBody()
        if site_url is not None:
            body.site_url = site_url
        if session_type_ids is not None:
            body.session_type_ids = session_type_ids
        if person_id is not None:
            body.person_id = person_id
        if email is not None:
            body.email = email
        url = self.ep('userconfig/sessionTypes')
        data = super().put(url=url, data=body.json())
        return UserSessionTypes.parse_obj(data)

class GetTrackingCodeObject(ApiModel):
    #: Unique identifier for tracking code.
    id: Optional[str]
    #: Name for tracking code.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: An option for how an admin user can provide a code value.
    input_mode: Optional[InputMode]
    #: Type for the host profile.
    host_profile_code: Optional[HostProfileCode]
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]]


class CreateTrackingCodeBody(ApiModel):
    #: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list. The maximum size of options is 500.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: Select an option for how users can provide a code value. Please note that if users set inputMode as
    #: hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only applies to "Host
    #: Profile".
    input_mode: Optional[InputMode]
    #: Type for the host profile.
    host_profile_code: Optional[HostProfileCode]
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages. The
    #: maximum size of scheduleStartCodes is 5.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]]


class GetTrackingCodeItemForUserObject(TrackingCodeItemForCreateMeetingObject):
    #: Unique identifier for tracking code.
    id: Optional[str]


class GetUserTrackingCodesResponse(ApiModel):
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Unique identifier for the user.
    person_id: Optional[str]
    #: Email address for the user.
    email: Optional[str]
    #: Tracking code information.
    tracking_codes: Optional[list[GetTrackingCodeItemForUserObject]]


class ListTrackingCodesResponse(ApiModel):
    #: Tracking codes information.
    items: Optional[list[GetTrackingCodeObject]]


class UpdateUserTrackingCodesBody(ApiModel):
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Unique identifier for the user. At least one parameter of personId or email is required. personId must precede
    #: email if both are specified.
    person_id: Optional[str]
    #: Email address for the user. At least one parameter of personId or email is required. personId must precede email
    #: if both are specified.
    email: Optional[str]
    #: Tracking code information for updates.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]


class TrackingCodesApi(ApiChild, base=''):
    """
    Tracking codes are alphanumeric codes that identify categories of users on a Webex site. With tracking codes, you
    can analyze usage by various groups within an organization.
    The authenticated user calling this API must have an Administrator role with the meeting:admin_schedule_write and
    meeting:admin_schedule_read scopes.
    """

    def list_codes(self, site_url: str = None) -> list[GetTrackingCodeObject]:
        """
        Lists tracking codes on a site by an admin user.

        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/list-tracking-codes
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[GetTrackingCodeObject], data["items"])

    def code(self, tracking_code_id: str, site_url: str = None) -> GetTrackingCodeObject:
        """
        Retrieves details for a tracking code by an admin user.

        :param tracking_code_id: Unique identifier for the tracking code whose details are being requested.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and the preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/get-a-tracking-code
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{tracking_code_id}')
        data = super().get(url=url, params=params)
        return GetTrackingCodeObject.parse_obj(data)

    def create_code(self, name: str, site_url: str, options: OptionsForTrackingCodeObject, input_mode: InputMode, host_profile_code: HostProfileCode, schedule_start_codes: ScheduleStartCodeObject) -> GetTrackingCodeObject:
        """
        Create a new tracking code by an admin user.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of options is 500.
        :type options: OptionsForTrackingCodeObject
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            inputMode as hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only
            applies to "Host Profile".
        :type input_mode: InputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: HostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of scheduleStartCodes is 5.
        :type schedule_start_codes: ScheduleStartCodeObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/create-a-tracking-code
        """
        body = CreateTrackingCodeBody()
        if name is not None:
            body.name = name
        if site_url is not None:
            body.site_url = site_url
        if options is not None:
            body.options = options
        if input_mode is not None:
            body.input_mode = input_mode
        if host_profile_code is not None:
            body.host_profile_code = host_profile_code
        if schedule_start_codes is not None:
            body.schedule_start_codes = schedule_start_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes')
        data = super().post(url=url, data=body.json())
        return GetTrackingCodeObject.parse_obj(data)

    def update_code(self, name: str, site_url: str, options: OptionsForTrackingCodeObject, input_mode: InputMode, host_profile_code: HostProfileCode, schedule_start_codes: ScheduleStartCodeObject) -> GetTrackingCodeObject:
        """
        Updates details for a tracking code by an admin user.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of options is 500.
        :type options: OptionsForTrackingCodeObject
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            inputMode as hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only
            applies to "Host Profile".
        :type input_mode: InputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: HostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of scheduleStartCodes is 5.
        :type schedule_start_codes: ScheduleStartCodeObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/update-a-tracking-code
        """
        body = CreateTrackingCodeBody()
        if name is not None:
            body.name = name
        if site_url is not None:
            body.site_url = site_url
        if options is not None:
            body.options = options
        if input_mode is not None:
            body.input_mode = input_mode
        if host_profile_code is not None:
            body.host_profile_code = host_profile_code
        if schedule_start_codes is not None:
            body.schedule_start_codes = schedule_start_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{trackingCodeId}')
        data = super().put(url=url, data=body.json())
        return GetTrackingCodeObject.parse_obj(data)

    def delete_code(self, tracking_code_id: str, site_url: str):
        """
        Deletes a tracking code by an admin user.

        :param tracking_code_id: Unique identifier for the tracking code to be deleted.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site from which the API deletes the tracking code. All available Webex sites
            and preferred sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/delete-a-tracking-code
        """
        params = {}
        params['siteUrl'] = site_url
        url = self.ep(f'https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{tracking_code_id}')
        super().delete(url=url, params=params)
        return

    def user_codes(self, site_url: str = None, person_id: str = None) -> GetUserTrackingCodesResponse:
        """
        Lists user's tracking codes by an admin user.

        :param site_url: URL of the Webex site from which the API retrieves the tracking code. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str
        :param person_id: Unique identifier for the user whose tracking codes are being retrieved. The admin user can
            specify the personId of a user on a site they manage and the API returns details for the user's tracking
            codes. At least one parameter of personId or email is required.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/get-user-tracking-codes
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep('https: //webexapis.com/v1/admin/meeting/userconfig/trackingCodes')
        data = super().get(url=url, params=params)
        return GetUserTrackingCodesResponse.parse_obj(data)

    def update_user_codes(self, site_url: str, person_id: str = None, email: str = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None) -> GetUserTrackingCodesResponse:
        """
        Updates tracking codes for a specified user by an admin user.

        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param person_id: Unique identifier for the user. At least one parameter of personId or email is required.
            personId must precede email if both are specified.
        :type person_id: str
        :param email: Email address for the user. At least one parameter of personId or email is required. personId
            must precede email if both are specified.
        :type email: str
        :param tracking_codes: Tracking code information for updates.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/update-user-tracking-codes
        """
        body = UpdateUserTrackingCodesBody()
        if site_url is not None:
            body.site_url = site_url
        if person_id is not None:
            body.person_id = person_id
        if email is not None:
            body.email = email
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/userconfig/trackingCodes')
        data = super().put(url=url, data=body.json())
        return GetUserTrackingCodesResponse.parse_obj(data)

class Resource(str, Enum):
    #: The Attachment Actions resource.
    attachment_actions = 'attachmentActions'
    #: The Memberships resource.
    memberships = 'memberships'
    #: The Messages resource.
    messages = 'messages'
    #: The Rooms resource.
    rooms = 'rooms'
    #: The Meetings resource.
    meetings = 'meetings'
    #: The Recordings resource.
    recordings = 'recordings'
    #: The Meeting Participants resource.
    meeting_participants = 'meetingParticipants'
    #: The Meeting Transcripts resource.
    meeting_transcripts = 'meetingTranscripts'


class Event(str, Enum):
    #: An object was created.
    created = 'created'
    #: An object was updated.
    updated = 'updated'
    #: An object was deleted.
    deleted = 'deleted'
    #: A meeting was started.
    started = 'started'
    #: A meeting was ended.
    ended = 'ended'
    #: A participant joined.
    joined = 'joined'
    #: A participant left.
    left = 'left'


class CreateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[Resource]
    #: The event type for the webhook.
    event: Optional[Event]
    #: The filter that defines the webhook scope. See Filtering Webhooks for more information.
    filter: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants, and
    #: meetingTranscripts resources.
    owned_by: Optional[str]


class Webhook(CreateWebhookBody):
    #: A unique identifier for the webhook.
    id: Optional[str]
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: Optional[Status16]
    #: The date and time the webhook was created.
    created: Optional[str]


class ListWebhooksResponse(ApiModel):
    items: Optional[list[Webhook]]


class UpdateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants and
    #: meetingTranscripts resources.
    owned_by: Optional[str]
    #: The status of the webhook. Use "active" to reactivate a disabled webhook.
    status: Optional[Status16]


class WebhooksApi(ApiChild, base='webhooks'):
    """
    For Webex for Government (FedRAMP), the following resource types are not available for Webhooks: meetings,
    recordings, meetingParticipants, and meetingTranscripts.
    Webhooks allow your app to be notified via HTTP when a specific event occurs in Webex. For example, your app can
    register a webhook to be notified when a new message is posted into a specific room.
    Events trigger in near real-time allowing your app and backend IT systems to stay in sync with new content and room
    activity.
    Check The Webhooks Guide and our blog regularly for announcements of additional webhook resources and event types.
    Long result sets will be split into pages.
    """

    def list(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
        """
        List all of your webhooks.

        :param owned_by: Limit the result list to org wide webhooks. Only allowed value is org.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/list-webhooks
        """
        if owned_by is not None:
            params['ownedBy'] = owned_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Webhook, params=params)

    def create(self, name: str, target_url: str, resource: Resource, event: Event, filter: str = None, secret: str = None, owned_by: str = None) -> Webhook:
        """
        Creates a webhook.
        To learn more about how to create and use webhooks, see The Webhooks Guide.

        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :type resource: Resource
        :param event: The event type for the webhook.
        :type event: Event
        :param filter: The filter that defines the webhook scope. See Filtering Webhooks for more information.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants, and meetingTranscripts resources.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook
        """
        body = CreateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if resource is not None:
            body.resource = resource
        if event is not None:
            body.event = event
        if filter is not None:
            body.filter = filter
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def details(self, webhook_id: str) -> Webhook:
        """
        Shows details for a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/get-webhook-details
        """
        url = self.ep(f'{webhook_id}')
        data = super().get(url=url)
        return Webhook.parse_obj(data)

    def update(self, webhook_id: str, name: str, target_url: str, secret: str = None, owned_by: str = None, status: Status16 = None) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that was
        auto deactivated.
        The fields that can be updated are name, targetURL, secret and status. All other fields, if supplied, are
        ignored.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants and meetingTranscripts resources.
        :type owned_by: str
        :param status: The status of the webhook. Use "active" to reactivate a disabled webhook.
        :type status: Status16

        documentation: https://developer.webex.com/docs/api/v1/webhooks/update-a-webhook
        """
        body = UpdateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        if status is not None:
            body.status = status
        url = self.ep(f'{webhook_id}')
        data = super().put(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/delete-a-webhook
        """
        url = self.ep(f'{webhook_id}')
        super().delete(url=url)
        return
