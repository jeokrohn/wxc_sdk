from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['MeetingRecordingArchiveChat', 'MeetingRecordingArchiveParticipant', 'MeetingRecordingArchivePoll',
           'MeetingRecordingArchivePollAnswerSummary', 'MeetingRecordingArchivePollContent',
           'MeetingRecordingArchivePollQuestion', 'MeetingRecordingArchivePollQuestionQuestion',
           'MeetingRecordingArchivePollRespondent', 'MeetingRecordingArchiveQA', 'MeetingRecordingArchiveQAAnswer',
           'MeetingRecordingArchiveSystemInfo', 'MeetingRecordingArchiveUser', 'RecordingAchriveSummaryObject',
           'RecordingAchriveSummaryObjectServiceType', 'RecordingArchiveReportObject', 'RecordingReportApi',
           'RecordingReportObject', 'RecordingReportSummaryObject', 'SystemInfoCatalog']


class RecordingReportSummaryObject(ApiModel):
    #: A unique identifier for the recording.
    #: example: 4f914b1dfe3c4d11a61730f18c0f5387
    recording_id: Optional[str] = None
    #: The recording's topic.
    #: example: John's Meeting
    topic: Optional[str] = None
    #: The date and time the recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. the time is the record button was clicked
    #: in the meeting.
    #: example: 2019-01-27T17:40:20Z
    time_recorded: Optional[datetime] = None
    #: Site URL for the recording.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: The number of times the recording was viewed.
    #: example: 7
    view_count: Optional[int] = None
    #: The number of times the recording was downloaded.
    #: example: 20
    download_count: Optional[int] = None


class RecordingReportObject(ApiModel):
    #: A unique identifier for the recording.
    #: example: 4f914b1dfe3c4d11a61730f18c0f5387
    recording_id: Optional[str] = None
    #: The recording's topic.
    #: example: John's Meeting
    topic: Optional[str] = None
    #: The name of the person who accessed the recording.
    #: example: John Andersen
    name: Optional[str] = None
    #: The email address of the person who accessed the recording.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: The date and time the recording was accessed in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2019-01-27T17:40:20Z
    access_time: Optional[datetime] = None
    #: Whether or not the recording was viewed by the person.
    #: example: True
    viewed: Optional[bool] = None
    #: Whether or not the recording was downloaded by the person.
    #: example: True
    downloaded: Optional[bool] = None


class RecordingAchriveSummaryObjectServiceType(str, Enum):
    meeting_center = 'MeetingCenter'
    event_center = 'EventCenter'
    training_center = 'TrainingCenter'
    support_center = 'SupportCenter'


class RecordingAchriveSummaryObject(ApiModel):
    #: A unique identifier for the meeting archive summary.
    #: example: 7d7ea5f42b921eace05386ca24ad730e_R_1000634462
    archive_id: Optional[str] = None
    #: Recording achrive summary's service-type.
    #: example: MeetingCenter
    service_type: Optional[RecordingAchriveSummaryObjectServiceType] = None
    #: Meeting title.
    #: example: John's Meeting
    title: Optional[str] = None
    #: The date and time in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format that when the archive was created by the system.
    #: example: 2019-01-27T17:43:24Z
    create_time: Optional[datetime] = None


class MeetingRecordingArchiveParticipant(ApiModel):
    #: An internal ID that is associated with each join.
    #: example: 28208023
    correlation_id: Optional[int] = None
    #: Display name for the meeting participant.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The time the participant joined the meeting.
    #: example: 2022-07-20T07:01:31Z
    joined_time: Optional[datetime] = None
    #: The time the participant left the meeting.
    #: example: 2022-07-20T07:01:31Z
    left_time: Optional[datetime] = None
    #: Email address for the meeting participant.
    #: example: john.andersen@example.com
    email: Optional[str] = None


class MeetingRecordingArchiveChat(ApiModel):
    #: Whether the type of the chat is private, public or group. Private chat is for the 1:1 chat. Public chat is for
    #: the message which is sent to all the people in the meeting. Group chat is for the message which is sent to a
    #: small group of people, like a message to the "host and presenter".
    #: example: private
    type: Optional[str] = None
    #: Display name for the sender of the chat snippet.
    #: example: John Andersen
    sender_name: Optional[str] = None
    #: Chat time for the chat snippet in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:22:34Z
    chat_time: Optional[datetime] = None
    #: Information of the receivers of the chat snippet.
    #: example: All Participants
    target: Optional[str] = None
    #: The text of the chat snippet.
    #: example: It's nice to meet you
    text: Optional[str] = None


class MeetingRecordingArchiveUser(ApiModel):
    #: An internal ID that is associated with each join.
    #: example: 28208023
    correlation_id: Optional[int] = None
    #: Display name for the meeting participant.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Email address for the meeting participant.
    #: example: john.andersen@example.com
    email: Optional[str] = None


class MeetingRecordingArchivePollQuestionQuestion(ApiModel):
    #: The number of choices in the questions.
    #: example: 3
    choice_count: Optional[int] = None
    #: The type of the question.
    #: example: single
    type: Optional[str] = None
    #: The text of the question.
    #: example: Do you like this API?
    text: Optional[str] = None


class MeetingRecordingArchivePollAnswerSummary(ApiModel):
    #: The total number of people who selected this answer.
    #: example: 10
    total_respondents: Optional[int] = None
    #: Whether the answer is correct.
    #: example: True
    is_correct: Optional[bool] = None
    #: The text of the answer.
    #: example: Yes, I do.
    text: Optional[str] = None
    #: The voters among users.
    vote_users: Optional[list[MeetingRecordingArchiveUser]] = None


class MeetingRecordingArchivePollRespondent(ApiModel):
    #: An internal ID that is associated with the respondent's each join.
    #: example: 28208023
    correlation_id: Optional[int] = None
    #: Display name for the poll respondent.
    #: example: Alex Green
    display_name: Optional[str] = None
    #: Email address for the poll respondent.
    #: example: alex.green@example.com
    email: Optional[str] = None
    #: An array of answers to the question.
    answers: Optional[list[str]] = None


class MeetingRecordingArchivePollQuestion(ApiModel):
    #: The voters among users.
    vote_users: Optional[list[MeetingRecordingArchiveUser]] = None
    #: The poll's question.
    question: Optional[MeetingRecordingArchivePollQuestionQuestion] = None
    #: The answer summary of the archive poll.
    answer_summary: Optional[list[MeetingRecordingArchivePollAnswerSummary]] = None
    #: The question's respondents.
    respondents: Optional[list[MeetingRecordingArchivePollRespondent]] = None


class MeetingRecordingArchivePollContent(ApiModel):
    #: The total number of questions.
    #: example: 10
    question_count: Optional[int] = None
    #: The total number of users.
    #: example: 10
    user_count: Optional[int] = None
    #: The number of voters among users.
    #: example: 3
    voted_user_count: Optional[int] = None
    #: Poll's questions.
    questions: Optional[list[MeetingRecordingArchivePollQuestion]] = None


class MeetingRecordingArchivePoll(ApiModel):
    #: The type of the question.
    #: example: single
    type: Optional[str] = None
    #: The date and time the poll started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:25:34Z
    start_time: Optional[datetime] = None
    #: The date and time the poll ended in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:28:34Z
    end_time: Optional[datetime] = None
    #: The content of the meeting archive poll;
    content: Optional[MeetingRecordingArchivePollContent] = None


class MeetingRecordingArchiveQAAnswer(ApiModel):
    #: The answer's response mode.
    #: example: private
    response_mode: Optional[str] = None
    #: The name of the person who answered the question.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: An internal ID that is associated with the answer's each join.
    #: example: 10947662
    correlation_id: Optional[int] = None
    #: The email of the person who answered the question.
    #: example: alex.green@example.com
    email: Optional[str] = None
    #: The date and time the question answered in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:52:34Z
    answer_time: Optional[datetime] = None
    #: The text of the answer.
    #: example: Yes, I am.
    text: Optional[str] = None


class MeetingRecordingArchiveQA(ApiModel):
    #: The priority of the Q and A.
    #: example: NA
    priority: Optional[str] = None
    #: Whether the type of the Q and A is private, public, or group. Private Q and A is for the 1:1 chat. Public Q and
    #: A are for the message which is sent to all the people in the meeting. Group Q and A are for the message which
    #: is sent to a small group of people, like a Q and A to "host and presenter".
    #: example: private
    type: Optional[str] = None
    #: The email of the user who asked the question.
    #: example: john.andersen@example.com`
    display_name: Optional[str] = None
    #: The date and time the question was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:22:34Z
    question_time: Optional[datetime] = None
    #: Information of the user who asked the question.
    #: example: All Participants
    target: Optional[str] = None
    #: The question that was asked.
    #: example: Are you ok?
    question: Optional[str] = None
    #: Question's answers.
    answers: Optional[list[MeetingRecordingArchiveQAAnswer]] = None


class SystemInfoCatalog(ApiModel):
    #: System summary.
    #: example: User Name: John{*}Operating System: Mac OS X 12.6{*}User Home Directory: /Users/John{*}Date and Time: Tue Oct 18 10:38:17 CST 2022{*}
    system_summary: Optional[str] = None
    #: The browser user agent of the person who acted.
    #: example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
    browser: Optional[str] = None
    #: The type of hardware that the user used to attend the meeting.
    #: example: mac book
    hardware: Optional[str] = None
    #: The software that the user used to attend the meeting.
    #: example: webex
    installed_software: Optional[str] = None
    #: The software the user used that is running.
    #: example: webex
    running_software: Optional[str] = None
    #: Startup Programs.
    #: example: Macintosh HD
    startup_programs: Optional[str] = None
    #: The storage information of the user's device.
    #: example: 16 GB 2667 MHz DDR4
    storage: Optional[str] = None
    #: The video of the user's device.
    #: example: AirPlay
    video: Optional[str] = None
    #: The network of the user's device.
    #: example: Wi-Fi
    network: Optional[str] = None
    #: The operating system of the user's device.
    #: example: Mac OS X 10.0
    operating_system: Optional[str] = None
    #: The environment variables of the user's device.
    #: example: /usr/local/bin:$PATH
    environment_variables: Optional[str] = None
    #: The processes of the user's device.
    #: example: 2.6 GHz 6-Core Intel Core i7
    processes: Optional[str] = None
    #: The logical drives of the user's device.
    #: example: webapp
    logical_drives: Optional[str] = None
    #: The device of the user.
    #: example: device1
    devices: Optional[str] = None
    #: The service of the user's device.
    #: example: Firewall
    services: Optional[str] = None
    #: The system driver of the user's device.
    #: example: 32drivers
    system_drivers: Optional[str] = None
    #: The sign driver system of the user's device.
    #: example: 32drivers
    signed_drivers: Optional[str] = None
    #: The event viewer of the user's device.
    #: example: Screen Sharing
    event_viewer: Optional[str] = None
    #: The basic input and output system.
    #: example: AwardBIOS
    bios: Optional[str] = None


class MeetingRecordingArchiveSystemInfo(ApiModel):
    #: The name of the person who accessed the meeting archive.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The catalogs of system information.
    catalogs: Optional[list[SystemInfoCatalog]] = None


class RecordingArchiveReportObject(ApiModel):
    #: A unique identifier for the meeting archive summary.
    #: example: 7d7ea5f42b921eace05386ca24ad730e_R_1000634462
    archive_id: Optional[str] = None
    #: Recording achrive report's service-type.
    #: example: MeetingCenter
    service_type: Optional[RecordingAchriveSummaryObjectServiceType] = None
    #: Meeting title.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Start time for meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in ISO 8601 compliant format.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: The participants of the meeting archive.
    participants: Optional[list[MeetingRecordingArchiveParticipant]] = None
    #: The chats of the meeting archive.
    chats: Optional[list[MeetingRecordingArchiveChat]] = None
    #: The polls of the meeting archive.
    polls: Optional[list[MeetingRecordingArchivePoll]] = None
    #: Meeting meeting archive's Q and A.
    qas: Optional[list[MeetingRecordingArchiveQA]] = None
    #: The system Information of the meeting archive, which can be only supported when serviceType is `SupportCenter`.
    system_infos: Optional[list[MeetingRecordingArchiveSystemInfo]] = None


class RecordingReportApi(ApiChild, base='recordingReport'):
    """
    Recording Report
    
    The recording report API is used to retrieve reports of recording.
    
    Refer to the `Meetings API Scopes` section of `Meetings Overview
    <https://developer.webex.com/docs/meetings>`_ for scopes required for each API.
    """

    def list_of_recording_audit_report_summaries(self, from_: Union[str, datetime] = None, to_: Union[str,
                                                 datetime] = None, host_email: str = None, site_url: str = None,
                                                 **params) -> Generator[RecordingReportSummaryObject, None, None]:
        """
        List of Recording Audit Report Summaries

        Lists of recording audit report summaries. You can specify a date range and the maximum number of recording
        audit report summaries to return.

        Only recording audit report summaries of meetings hosted by or shared with the authenticated user will be
        listed.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * If `siteUrl` is specified, the recording audit report summaries of the specified site will be listed;
        otherwise, recording audit report summaries of the user's preferred site will be listed. All available Webex
        sites and the preferred site of the user can be retrieved by the `Get Site List` API.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param from_: Starting date and time (inclusive) for recording audit report summaries to return, in any
            `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot be after `to`. Please note that the interval between `to` and
            `from` cannot exceed 90 days and the interval between the current time and `from` cannot exceed 365 days.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for recording audit report summaries to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. `to` cannot be before `from`. Please note that the interval between `to` and `from`
            cannot exceed 90 days and the interval between the current time and `from` cannot exceed 365 days.
        :type to_: Union[str, datetime]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return recording audit report summaries of that user. If a special value
            of `all` is set for `hostEmail`, the admin can list recording audit report summaries of all users on the
            target site, not of a single user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists recording audit report summaries from. If not
            specified, the API lists summary audit report for recordings from the user's preferred site. All available
            Webex sites and the preferred site of the user can be retrieved by `Get Site List` API.
        :type site_url: str
        :return: Generator yielding :class:`RecordingReportSummaryObject` instances
        """
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('accessSummary')
        return self.session.follow_pagination(url=url, model=RecordingReportSummaryObject, item_key='items', params=params)

    def get_recording_audit_report_details(self, recording_id: str, host_email: str = None,
                                           **params) -> Generator[RecordingReportObject, None, None]:
        """
        Get Recording Audit Report Details

        Retrieves details for a recording audit report with a specified recording ID.

        Only recording audit report details of meetings hosted by or shared with the authenticated user may be
        retrieved.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return recording details of that user.
        :type host_email: str
        :return: Generator yielding :class:`RecordingReportObject` instances
        """
        params['recordingId'] = recording_id
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('accessDetail')
        return self.session.follow_pagination(url=url, model=RecordingReportObject, item_key='items', params=params)

    def list_meeting_archive_summaries(self, from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                                       site_url: str = None,
                                       **params) -> Generator[RecordingAchriveSummaryObject, None, None]:
        """
        List Meeting Archive Summaries

        Lists of meeting archive summaries. You can specify a date range and the maximum number of meeting archive
        summaries to return.

        Meeting archive summaries are only available to full administrators, not even the meeting host.

        The list returned is sorted in descending order by the date and time that the archives were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * If `siteUrl` is specified, the meeting archive summaries of the specified site will be listed; otherwise,
        meeting archive summaries of the user's preferred site will be listed. All available Webex sites and the
        preferred site of the user can be retrieved by the `Get Site List` API.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param from_: Starting date and time (inclusive) for meeting archive summaries to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. `from` cannot be after `to`. Please note that the interval between `to` and `from`
            cannot exceed 30 days.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for meeting archive summaries to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant
            format. `to` cannot be before `from`. Please note that the interval between `to` and `from` cannot exceed
            30 days.
        :type to_: Union[str, datetime]
        :param site_url: URL of the Webex site which the API lists meeting archive summaries from. If not specified,
            the API lists meeting archive summaries for recordings from the user's preferred site. All available Webex
            sites and the preferred site of the user can be retrieved by `Get Site List` API.
        :type site_url: str
        :return: Generator yielding :class:`RecordingAchriveSummaryObject` instances
        """
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('meetingArchiveSummaries')
        return self.session.follow_pagination(url=url, model=RecordingAchriveSummaryObject, item_key='items', params=params)

    def get_meeting_archive_details(self, archive_id: str) -> RecordingArchiveReportObject:
        """
        Get Meeting Archive Details

        Retrieves details for a meeting archive report with a specified archive ID, which contains recording metadata.

        Meeting archive details are only available to full administrators, not even the meeting host.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param archive_id: A unique identifier for the meeting archive summary.
        :type archive_id: str
        :rtype: :class:`RecordingArchiveReportObject`
        """
        url = self.ep(f'meetingArchives/{archive_id}')
        data = super().get(url)
        r = RecordingArchiveReportObject.model_validate(data)
        return r
