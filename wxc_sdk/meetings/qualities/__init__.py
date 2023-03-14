"""
Mesting qualities API
"""
from collections.abc import Generator
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum

__all__ = ['MediaSessionQuality', 'MeetingQualitiesApi', 'NetworkType',
           'QualityResources',
           'TransportType', 'VideoIn']


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


class QualityResources(ApiModel):
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
    resources: Optional[list[QualityResources]]


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

    def meeting_qualities(self, meeting_id: str, offset: int = None,
                          **params) -> Generator[MediaSessionQuality, None, None]:
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
