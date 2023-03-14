__all__ = ['ClosedCaption', 'CCSnippet', 'MeetingClosedCaptionsApi']

from collections.abc import Generator
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel


class ClosedCaption(ApiModel):
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


class CCSnippet(ApiModel):
    #: A unique identifier for the closed caption snippet.
    id: Optional[str]
    #: Unique identifier for the meeting instance which the closed captions belong to.
    meeting_id: Optional[str]
    #: Text for the snippet.
    text: Optional[str]
    #: Name of the person who spoke.
    person_name: Optional[str]
    #: Email address of the person who spoke.
    person_email: Optional[str]
    #: The unique identifier for the person speaking.
    people_id: Optional[str]
    #: Start time for the snippet.
    start: Optional[str]
    #: Offset from the beginning of the closed captions in milliseconds indicating the start time of the snippet.
    offset_millisecond: Optional[str]
    #: Duration of the snippet in milliseconds.
    duration_millisecond: Optional[str]
    #: Original language of the snippet.
    language: Optional[str]


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

    def list(self, meeting_id: str, **params) -> Generator[ClosedCaption, None, None]:
        """
        Lists closed captions of a finished meeting instance specified by meetingId.

        :param meeting_id: Unique identifier for the meeting instance which the closed captions belong to. This
            parameter only applies to ended meeting instnaces. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ClosedCaption, params=params)

    def list_snippets(self, closed_caption_id: str, meeting_id: str, **params) -> Generator[CCSnippet, None, None]:
        """
        Lists snippets of a meeting closed caption specified by closedCaptionId.

        :param closed_caption_id: Unique identifier for the meeting closed caption which the snippets belong to.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/snippets')
        return self.session.follow_pagination(url=url, model=CCSnippet, params=params)

    def download_snippets(self, closed_caption_id: str, meeting_id: str, format: str = None):
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
        """
        # TODO: verify return and adapt
        params = {}
        params['meetingId'] = meeting_id
        if format is not None:
            params['format'] = format
        url = self.ep(f'{closed_caption_id}/download')
        super().get(url=url, params=params)
        return
