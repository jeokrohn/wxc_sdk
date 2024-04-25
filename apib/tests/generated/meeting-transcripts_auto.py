from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['DownloadAMeetingTranscriptFormat', 'MeetingTranscriptsApi', 'SnippetObject', 'TranscriptObject',
           'TranscriptObjectStatus']


class TranscriptObjectStatus(str, Enum):
    #: Transcript is available.
    available = 'available'
    #: Transcript has been deleted.
    deleted = 'deleted'


class TranscriptObject(ApiModel):
    #: A unique identifier for the transcript.
    #: example: 195d64646ad14be2924ea50f541fd91d
    id: Optional[str] = None
    #: URL of the Webex site from which the API lists meeting transcripts.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Start time for the meeting transcript in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2020-06-01T20:30:15.042Z
    start_time: Optional[datetime] = None
    #: The meeting's topic.
    #: example: John's Meeting
    meeting_topic: Optional[str] = None
    #: Unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the transcripts belong.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_I_166022169160077044
    meeting_id: Optional[str] = None
    #: Unique identifier for scheduled meeting with which the current meeting is associated. Only apples to a meeting
    #: instance which is happening or has happened. This is the `id` of the scheduled meeting with which the instance
    #: is associated.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_20210401T232500Z
    scheduled_meeting_id: Optional[str] = None
    #: Unique identifier for the parent meeting series to which the recording belongs.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae
    meeting_series_id: Optional[str] = None
    #: Unique identifier for the meeting host.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83QkFCQkU5OS1CNDNFLTREM0YtOTE0Ny1BMUU5RDQ2QzlDQTA
    host_user_id: Optional[str] = None
    #: The download link for the transcript vtt file.
    #: example: http://site-example.webex.com/v1/meetingTranscripts/195d64646ad14be2924ea50f541fd91d/download?format=vtt
    vtt_download_link: Optional[str] = None
    #: The download link for the transcript txt file.
    #: example: http://site-example.webex.com/v1/meetingTranscripts/195d64646ad14be2924ea50f541fd91d/download?format=txt
    txt_download_link: Optional[str] = None
    status: Optional[TranscriptObjectStatus] = None


class SnippetObject(ApiModel):
    #: A unique identifier for the snippet.
    #: example: 195d64646ad14be2924ea50f541fd91d_00001
    id: Optional[str] = None
    #: Text for the snippet.
    #: example: Hello everyone
    text: Optional[str] = None
    #: Name of the person generating the speech for the snippet.
    #: example: John Andersen
    person_name: Optional[str] = None
    #: Email address of the person generating the speech for the snippet.
    #: example: john.andersen@example.com
    person_email: Optional[str] = None
    #: Offset from the beginning of the parent transcript in milliseconds indicating the start time of the snippet.
    #: example: 1000
    offset_millisecond: Optional[int] = None
    #: Duration of the snippet in milliseconds.
    #: example: 2000
    duration_millisecond: Optional[int] = None


class DownloadAMeetingTranscriptFormat(str, Enum):
    vtt = 'vtt'
    txt = 'txt'


class MeetingTranscriptsApi(ApiChild, base=''):
    """
    Meeting Transcripts
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    A meeting transcript is the automatic transcription of a meeting's recordings by our industry-leading
    speech-to-text engine to capture of what was discussed and decided during the meeting, in text form.
    
    A transcript snippet is a short text snippet from a meeting transcript which was spoken by a particular participant
    in the meeting. A meeting transcript consists of many snippets.
    
    This API manages meeting transcripts and snippets. You can use the Transcript API to list meeting transcripts,
    list, get and update transcript snippets. Transcripts may be retrieved via download link defined by
    `vttDownloadLink` or `txtDownloadlink` in the response body.
    
    Refer to the `Meetings API Scopes` section of `Meetings Overview
    <https://developer.webex.com/docs/meetings>`_ for scopes required for each API.
    
    **NOTE:**
    1. Listing/Getting/Updating meeting transcript snippets function do not support Admin role.
    2. The meeting transcript can not be recorded until you turn on the meeting recording. Since August 1, 2023, you
    also need to turn on the `Webex Assistant
    <https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/at-a-glance-c45-744053.html>`_ or the `Closed Captions
    """

    def list_meeting_transcripts(self, meeting_id: str = None, host_email: str = None, site_url: str = None,
                                 from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                                 **params) -> Generator[TranscriptObject, None, None]:
        """
        List Meeting Transcripts

        Lists available transcripts of an ended `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_.

        Use this operation to list transcripts of an ended `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ when they are ready. Please note that only
        **meeting instances** in state `ended` are supported for `meetingId`. **Meeting series**, **scheduled
        meetings** and `in-progress` **meeting instances** are not supported.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param meeting_id: Unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the transcript belongs. Please note that
            currently the meeting ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API. If
            `meetingId` is not specified, the operation returns an array of transcripts for all meetings of the
            current user.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the `admin-level` scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user. If `meetingId` is
            not specified, it can not support `hostEmail`.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists transcripts. If not specified, the API lists
            transcripts from user's preferred site. All available Webex sites and the preferred site of the user can
            be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`TranscriptObject` instances
        """
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
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
        url = self.ep('meetingTranscripts')
        return self.session.follow_pagination(url=url, model=TranscriptObject, item_key='items', params=params)

    def list_meeting_transcripts_for_compliance_officer(self, site_url: str, from_: Union[str, datetime] = None,
                                                        to_: Union[str, datetime] = None,
                                                        **params) -> Generator[TranscriptObject, None, None]:
        """
        List Meeting Transcripts For Compliance Officer

        Lists available or deleted transcripts of an ended `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for a specific site.

        The returned list is sorted in descending order by the date and time that the transcript was created.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.

        :param site_url: URL of the Webex site from which the API lists transcripts.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`TranscriptObject` instances
        """
        params['siteUrl'] = site_url
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
        url = self.ep('admin/meetingTranscripts')
        return self.session.follow_pagination(url=url, model=TranscriptObject, item_key='items', params=params)

    def download_a_meeting_transcript(self, transcript_id: str, format_: DownloadAMeetingTranscriptFormat = None,
                                      host_email: str = None):
        """
        Download a Meeting Transcript

        Download a meeting transcript from the meeting transcript specified by `transcriptId`.

        :param transcript_id: Unique identifier for the meeting transcript.
        :type transcript_id: str
        :param format_: Format for the downloaded meeting transcript.
        :type format_: DownloadAMeetingTranscriptFormat
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the `admin-level` scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :rtype: None
        """
        params = {}
        if format_ is not None:
            params['format'] = enum_str(format_)
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'meetingTranscripts/{transcript_id}/download')
        super().get(url, params=params)

    def list_snippets_of_a_meeting_transcript(self, transcript_id: str,
                                              **params) -> Generator[SnippetObject, None, None]:
        """
        List Snippets of a Meeting Transcript

        Lists snippets of a meeting transcript specified by `transcriptId`.

        Use this operation to list snippets of a meeting transcript when they are ready.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippets belong.
        :type transcript_id: str
        :return: Generator yielding :class:`SnippetObject` instances
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets')
        return self.session.follow_pagination(url=url, model=SnippetObject, item_key='items', params=params)

    def get_a_transcript_snippet(self, transcript_id: str, snippet_id: str) -> SnippetObject:
        """
        Get a Transcript Snippet

        Retrieves details for a transcript snippet specified by `snippetId` from the meeting transcript specified by
        `transcriptId`.

        :param transcript_id: Unique identifier for the meeting transcript to which the requested snippet belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being requested.
        :type snippet_id: str
        :rtype: :class:`SnippetObject`
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = super().get(url)
        r = SnippetObject.model_validate(data)
        return r

    def update_a_transcript_snippet(self, transcript_id: str, snippet_id: str, text: str,
                                    reason: str = None) -> SnippetObject:
        """
        Update a Transcript Snippet

        Updates details for a transcript snippet specified by `snippetId` from the meeting transcript specified by
        `transcriptId`.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippet to be updated belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being updated.
        :type snippet_id: str
        :param text: Text for the snippet.
        :type text: str
        :param reason: Reason for snippet update; only required for Compliance Officers.
        :type reason: str
        :rtype: :class:`SnippetObject`
        """
        body = dict()
        if reason is not None:
            body['reason'] = reason
        body['text'] = text
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = super().put(url, json=body)
        r = SnippetObject.model_validate(data)
        return r

    def delete_a_transcript(self, transcript_id: str, reason: str = None, comment: str = None):
        """
        Delete a Transcript

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
        :rtype: None
        """
        body = dict()
        if reason is not None:
            body['reason'] = reason
        if comment is not None:
            body['comment'] = comment
        url = self.ep(f'meetingTranscripts/{transcript_id}')
        super().delete(url, json=body)
