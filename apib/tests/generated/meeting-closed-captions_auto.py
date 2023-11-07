from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ClosedCaptionObject', 'DownloadMeetingClosedCaptionSnippetsFormat',
            'ListMeetingClosedCaptionSnippetsResponse', 'ListMeetingClosedCaptionsResponse', 'SnippetObject']


class ClosedCaptionObject(ApiModel):
    #: A unique identifier for the closed caption.
    #: example: 195d64646ad14be2924ea50f541fd91d
    id: Optional[str] = None
    #: Unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the closed captions belong to.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_I_166022169160077044
    meeting_id: Optional[str] = None
    #: The download link for the closed caption vtt file.
    #: example: http://site-example.webex.com/v1/meetingClosedCaptions/195d64646ad14be2924ea50f541fd91d/download?format=vtt
    vtt_download_link: Optional[str] = None
    #: The download link for the closed caption txt file.
    #: example: http://site-example.webex.com/v1/meetingClosedCaptions/195d64646ad14be2924ea50f541fd91d/download?format=txt
    txt_download_link: Optional[str] = None
    #: Start time for the meeting closed caption in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2020-06-01T20:30:15.042Z
    start: Optional[datetime] = None


class SnippetObject(ApiModel):
    #: A unique identifier for the closed caption snippet.
    #: example: 195d64646ad14be2924ea50f541fd91d_00001
    id: Optional[str] = None
    #: Unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the closed captions belong to.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_I_166022169160077044
    meeting_id: Optional[str] = None
    #: Text for the snippet.
    #: example: Hello everyone
    text: Optional[str] = None
    #: Name of the person who spoke.
    #: example: John Andersen
    person_name: Optional[str] = None
    #: Email address of the person who spoke.
    #: example: john.andersen@example.com
    person_email: Optional[str] = None
    #: The unique identifier for the person speaking.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    people_id: Optional[str] = None
    #: Start time for the snippet.
    #: example: 2019-11-01T12:30:05Z
    start: Optional[datetime] = None
    #: Offset from the beginning of the closed captions in milliseconds indicating the start time of the snippet.
    #: example: 1000
    offset_millisecond: Optional[datetime] = None
    #: Duration of the snippet in milliseconds.
    #: example: 2000
    duration_millisecond: Optional[datetime] = None
    #: Original language of the snippet.
    #: example: en
    language: Optional[str] = None


class ListMeetingClosedCaptionsResponse(ApiModel):
    #: Closed caption array
    items: Optional[list[ClosedCaptionObject]] = None


class ListMeetingClosedCaptionSnippetsResponse(ApiModel):
    #: Closed caption snippet array
    items: Optional[list[SnippetObject]] = None


class DownloadMeetingClosedCaptionSnippetsFormat(str, Enum):
    vtt = 'vtt'
    txt = 'txt'


class MeetingClosedCaptionsApi(ApiChild, base='meetingClosedCaptions'):
    """
    Meeting Closed Captions
    
    Meeting Closed Captions APIs are enabled upon request, and are not available
    by default. Please contact the Webex Developer Support team at
    devsupport@webex.com if you would like to enable this feature for your
    organization.
    
    
    
    Meeting closed captions are the automatic transcriptions of what is being said during a meeting in real-time.
    Closed captions appear after being enabled during a meeting and can be translated to a participant's language.
    
    A closed caption snippet is a short text snippet from a meeting closed caption which was spoken by a particular
    participant in the meeting. A meeting's closed captions consists of many snippets.
    
    The Closed Captions API manages meeting closed captions and snippets. You can list meeting closed captions, as well
    as list and download snippets. Closed captions can  be retrieved in either Web Video Text Tracks (VTT) or plain
    text (TXT) format via the download links provided by the `vttDownloadLink` and `txtDownloadlink` response
    properties, respectively.
    
    Refer to the `Meetings API Scopes
    <https://developer.webex.com/docs/meetings#meetings-api-scopes>`_ section of `Meetings Overview
    
    **Notes:**
    
    * Currently, closed caption APIs are only supported for the `Compliance Officer
    <https://developer.webex.com/docs/compliance#compliance>`_ role.
    
    * Closed captions will be available 15 minutes after the meeting is finished.
    """
    ...