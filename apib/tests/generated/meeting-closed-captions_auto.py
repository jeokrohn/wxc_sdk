from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ClosedCaptionObject', 'DownloadMeetingClosedCaptionSnippetsFormat', 'MeetingClosedCaptionsApi',
           'SnippetObject']


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
    offset_millisecond: Optional[str] = None
    #: Duration of the snippet in milliseconds.
    #: example: 2000
    duration_millisecond: Optional[str] = None
    #: Original language of the snippet.
    #: example: en
    language: Optional[str] = None


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

    def list_meeting_closed_captions(self, meeting_id: str) -> list[ClosedCaptionObject]:
        """
        List Meeting Closed Captions

        Lists closed captions of a finished `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ specified by `meetingId`.

        * Closed captions are ready 15 minutes after the meeting is finished.

        * Only **meeting instances** in state `ended` are supported for `meetingId`. **Meeting series**, **scheduled
        meetings** and `in-progress` **meeting instances** are not supported.

        * Currently, a meeting may have only one closed caption associated with its `meetingId`. The response is a
        closed captions array, which may contain multiple values to allow for future expansion, but currently only one
        closed caption is included in the response.

        :param meeting_id: Unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the closed captions belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meetings.
        :type meeting_id: str
        :rtype: list[ClosedCaptionObject]
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClosedCaptionObject]).validate_python(data['items'])
        return r

    def list_meeting_closed_caption_snippets(self, closed_caption_id: str, meeting_id: str) -> list[SnippetObject]:
        """
        List Meeting Closed Caption Snippets

        Lists snippets of a meeting closed caption specified by `closedCaptionId`.

        :param closed_caption_id: Unique identifier for the meeting closed caption which the snippets belong to.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the closed caption snippets belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meetings.
        :type meeting_id: str
        :rtype: list[SnippetObject]
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/snippets')
        data = super().get(url, params=params)
        r = TypeAdapter(list[SnippetObject]).validate_python(data['items'])
        return r

    def download_meeting_closed_caption_snippets(self, closed_caption_id: str, meeting_id: str,
                                                 format_: DownloadMeetingClosedCaptionSnippetsFormat = None):
        """
        Download Meeting Closed Caption Snippets

        Download meeting closed caption snippets from the meeting closed caption specified by `closedCaptionId`
        formatted either as a Video Text Track (.vtt) file or plain text (.txt) file.

        #### Request Header

        * `timezone`: *`Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.*

        :param closed_caption_id: Unique identifier for the meeting closed caption.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ which the closed caption snippets belong to. This
            parameter only applies to meeting instances in the `ended` state. It does not apply to meeting series,
            scheduled meetings or scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meetings.
        :type meeting_id: str
        :param format_: Format for the downloaded meeting closed caption snippets.
        :type format_: DownloadMeetingClosedCaptionSnippetsFormat
        :rtype: None
        """
        params = {}
        if format_ is not None:
            params['format'] = enum_str(format_)
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/download')
        super().get(url, params=params)
