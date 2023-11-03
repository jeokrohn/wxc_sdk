from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DeleteTranscriptObject', 'DownloadAMeetingTranscriptFormat', 'ListMeetingTranscriptsResponse',
            'ListSnippetsOfAMeetingTranscriptResponse', 'SnippetObject', 'TranscriptObject', 'TranscriptObjectStatus',
            'UpdateSnippetObject']


class TranscriptObjectStatus(str, Enum):
    #: Transcript is available.
    available = 'available'
    #: Transcript has been deleted.
    deleted = 'deleted'
    none_ = 'none'


class TranscriptObject(ApiModel):
    #: A unique identifier for the transcript.
    #: example: 195d64646ad14be2924ea50f541fd91d
    id: Optional[str] = None
    #: URL of the Webex site from which the API lists meeting transcripts.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Start time for the meeting transcript in https://en.wikipedia.org/wiki/ISO_8601 compliant format.
    #: example: 2020-06-01T20:30:15.042Z
    start_time: Optional[datetime] = None
    #: The meeting's topic.
    #: example: John's Meeting
    meeting_topic: Optional[str] = None
    #: Unique identifier for the [meeting
    #: instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) to which the transcripts
    #: belong.
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
    #: example: 1000.0
    offset_millisecond: Optional[int] = None
    #: Duration of the snippet in milliseconds.
    #: example: 2000.0
    duration_millisecond: Optional[int] = None


class UpdateSnippetObject(ApiModel):
    #: Reason for snippet update; only required for Compliance Officers.
    #: example: audit
    reason: Optional[str] = None
    #: Text for the snippet.
    #: example: Hello everybody
    text: Optional[str] = None


class DeleteTranscriptObject(ApiModel):
    #: Reason for deleting a transcript. Only required when a Compliance Officer is operating on another user's
    #: transcript.
    #: example: audit
    reason: Optional[str] = None
    #: Explanation for deleting a transcript. The comment can be a maximum of 255 characters long.
    #: example: Maintain data privacy
    comment: Optional[str] = None


class ListMeetingTranscriptsResponse(ApiModel):
    #: Transcript array.
    items: Optional[list[TranscriptObject]] = None


class DownloadAMeetingTranscriptFormat(str, Enum):
    vtt = 'vtt'
    txt = 'txt'


class ListSnippetsOfAMeetingTranscriptResponse(ApiModel):
    #: Transcript snippet array
    items: Optional[list[SnippetObject]] = None
