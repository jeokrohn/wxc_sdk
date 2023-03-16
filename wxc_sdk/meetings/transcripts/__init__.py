"""
Meeting transcripts API
"""
from collections.abc import Generator
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum

__all__ = ['MeetingTranscriptsApi', 'TranscriptSnippet', 'TranscriptStatus', 'Transcript',
           'UpdateTranscriptSnippetBody', 'DeleteTranscriptBody']


class TranscriptStatus(str, Enum):
    #: Transcript is available.
    available = 'available'
    #: Transcript has been deleted.
    deleted = 'deleted'


class Transcript(ApiModel):
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
    status: Optional[TranscriptStatus]


class TranscriptSnippet(ApiModel):
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

    def list(self, meeting_id: str = None, host_email: str = None, site_url: str = None, from_: str = None,
             to_: str = None, **params) -> Generator[Transcript, None, None]:
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
        return self.session.follow_pagination(url=url, model=Transcript, params=params)

    def list_compliance_officer(self, site_url: str, from_: str = None, to_: str = None,
                                **params) -> Generator[Transcript, None, None]:
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

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts-for
        -compliance-officer
        """
        params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('admin/meetingTranscripts')
        return self.session.follow_pagination(url=url, model=Transcript, params=params)

    def download(self, transcript_id: str, format: str = None, host_email: str = None):
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
        # TODO: fix. Find out what the actual return type is

    def list_snippets(self, transcript_id: str, **params) -> Generator[TranscriptSnippet, None, None]:
        """
        Lists snippets of a meeting transcript specified by transcriptId.
        Use this operation to list snippets of a meeting transcript when they are ready.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippets belong.
        :type transcript_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-snippets-of-a-meeting-transcript
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets')
        return self.session.follow_pagination(url=url, model=TranscriptSnippet, params=params)

    def snippet_detail(self, transcript_id: str, snippet_id: str) -> TranscriptSnippet:
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
        return TranscriptSnippet.parse_obj(data)

    def update_snippet(self, transcript_id: str, snippet_id: str, text: str, reason: str = None) -> TranscriptSnippet:
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
        return TranscriptSnippet.parse_obj(data)

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
