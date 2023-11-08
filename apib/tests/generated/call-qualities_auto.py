from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AudioIn', 'AudioInType', 'CallsQualitiesResponse', 'MediaSessionQuality', 'VideoIn']


class VideoIn(ApiModel):
    #: The sampling interval of the downstream video quality data
    #: example: 60.0
    sampling_interval: Optional[int] = None
    #: The date and time when this video session started.
    #: example: 2016-04-18T17:00:00.000Z
    start_time: Optional[datetime] = None
    #: The date and time when this video session ended.
    #: example: 2016-04-18T17:00:00.000Z
    end_time: Optional[datetime] = None
    #: The percentage of video packet loss, in float between 0.0 and 100.0, during each sampling interval.
    #: example: [0.01, 0.1, 0.05]
    packet_loss: Optional[list[float]] = None
    #: The average latency, in milliseconds, during each sampling interval.
    #: example: [60.0, 5.0, 10.0]
    latency: Optional[list[float]] = None


class AudioInType(str, Enum):
    ip = 'IP'


class AudioIn(ApiModel):
    #: The type of audio in this media session.
    #: example: IP
    type: Optional[AudioInType] = None
    #: The sampling interval of the downstream audio quality data
    #: example: 60.0
    sampling_interval: Optional[int] = None
    #: The date and time when this audio session started.
    #: example: 2016-04-18T17:00:00.000Z
    start_time: Optional[datetime] = None
    #: The date and time when this audio session ended.
    #: example: 2016-04-18T17:00:00.000Z
    end_time: Optional[datetime] = None
    #: The percentage of audio packet loss, in float between 0.0 and 100.0, during each sampling interval. This applies
    #: to IP type only.
    #: example: [0.02, 0.1, 0.07]
    packet_loss: Optional[list[float]] = None
    #: The average latency, in milliseconds, during each sampling interval. This applies to IP type only.
    #: example: [30.0, 10.0, 5.0]
    latency: Optional[list[float]] = None
    #: The mean opinion score, in float between 0.0 and 5.0, during each sampling interval. This applies to PSTN type
    #: only.
    #: example: [1.2, 3.4, 4.9]
    mean_opinion_score: Optional[list[float]] = None


class MediaSessionQuality(ApiModel):
    #: The back references to the call where this media session belongs.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    call_id: Optional[str] = None
    #: The display name of the participant of this media session.
    #: example: John Doe
    display_name: Optional[str] = None
    #: The email address of the participant of this media session.
    #: example: jdoe@acme.com
    email: Optional[str] = None
    #: The date and time when this media session joined to the call.
    #: example: 2016-04-18T17:00:00.000Z
    joined: Optional[datetime] = None
    #: The total amount of time, in milliseconds, it takes for this media session to join the call.
    #: example: 500.0
    joining_time: Optional[int] = None
    #: The total amount of time, in seconds, that this media session has joined the call.
    #: example: 180.0
    joined_duration: Optional[int] = None
    #: The type of the client (and OS) used by this media session.
    #: example: Teams_Mobile_Client (iOS)
    client: Optional[str] = None
    #: The collection of downstream video quality data.
    video_in: Optional[list[VideoIn]] = None
    #: The collection of downstream audio quality data.
    audio_in: Optional[list[AudioIn]] = None


class CallsQualitiesResponse(ApiModel):
    items: Optional[list[MediaSessionQuality]] = None


class CallQualitiesApi(ApiChild, base='call/qualities'):
    """
    Call Qualities
    
    After a meeting has ended, meeting quality information is available for review by organization administrators.
    Quality information is available 30 minutes after a meeting has ended and may be retrieved for up to 30 days. To
    retrieve quality information, you must use an administrator API access token with the
    `spark-admin:call_qualities_read` `scope
    <https://developer.webex.com/docs/integrations#scopes>`_.
    
    For more information, see the `Calls
    <https://developer.webex.com/docs/api/guides/calls>`_ guide.
    """

    def get_call_qualities(self, call_id: str, max_: int = None) -> list[MediaSessionQuality]:
        """
        Get Call Qualities

        Provides quality data for a meeting, by `callId`. Only organization administrators can retrieve meeting quality
        data. Quality information is available 30 minutes after a meeting has ended and may be retrieved for up to 30
        days.

        :param call_id: The identifier of the call.
        :type call_id: str
        :param max_: Limit the maximum number of media sessions in the response
        :type max_: int
        :rtype: list[MediaSessionQuality]
        """
        params = {}
        params['callId'] = call_id
        if max_ is not None:
            params['max'] = max_
        url = self.ep()
        ...

    ...