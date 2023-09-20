from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ClosedCaptionObject', 'SnippetObject']


class ClosedCaptionObject(ApiModel):
    #: A unique identifier for the closed caption.
    #: example: 195d64646ad14be2924ea50f541fd91d
    id: Optional[str] = None
    #: Unique identifier for the [meeting instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) which the closed captions belong to.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_I_166022169160077044
    meetingId: Optional[str] = None
    #: The download link for the closed caption vtt file.
    #: example: http://site-example.webex.com/v1/meetingClosedCaptions/195d64646ad14be2924ea50f541fd91d/download?format=vtt
    vttDownloadLink: Optional[str] = None
    #: The download link for the closed caption txt file.
    #: example: http://site-example.webex.com/v1/meetingClosedCaptions/195d64646ad14be2924ea50f541fd91d/download?format=txt
    txtDownloadLink: Optional[str] = None
    #: Start time for the meeting closed caption in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format.
    #: example: 2020-06-01T20:30:15.042Z
    start: Optional[datetime] = None


class SnippetObject(ApiModel):
    #: A unique identifier for the closed caption snippet.
    #: example: 195d64646ad14be2924ea50f541fd91d_00001
    id: Optional[str] = None
    #: Unique identifier for the [meeting instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) which the closed captions belong to.
    #: example: 0ed74a1c0551494fb7a04e2881bf50ae_I_166022169160077044
    meetingId: Optional[str] = None
    #: Text for the snippet.
    #: example: Hello everyone
    text: Optional[str] = None
    #: Name of the person who spoke.
    #: example: John Andersen
    personName: Optional[str] = None
    #: Email address of the person who spoke.
    #: example: john.andersen@example.com
    personEmail: Optional[str] = None
    #: The unique identifier for the person speaking.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    peopleId: Optional[str] = None
    #: Start time for the snippet.
    #: example: 2019-11-01T12:30:05Z
    start: Optional[datetime] = None
    #: Offset from the beginning of the closed captions in milliseconds indicating the start time of the snippet.
    #: example: 1000
    offsetMillisecond: Optional[datetime] = None
    #: Duration of the snippet in milliseconds.
    #: example: 2000
    durationMillisecond: Optional[datetime] = None
    #: Original language of the snippet.
    #: example: en
    language: Optional[str] = None
