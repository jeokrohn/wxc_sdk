from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['MediaSessionQuality', 'MediaSessionQualityNetworkType', 'MeetingQualitiesResponse', 'Resources', 'VideoIn', 'VideoInTransportType']


class MediaSessionQualityNetworkType(str, Enum):
    wifi = 'wifi'
    cellular = 'cellular'
    ethernet = 'ethernet'
    unknown = 'unknown'


class VideoInTransportType(str, Enum):
    udp = 'UDP'
    tcp = 'TCP'


class VideoIn(ApiModel):
    #: The sampling interval, in seconds, of the downstream video quality data.
    #: example: 60.0
    samplingInterval: Optional[int] = None
    #: The date and time when this video session started.
    #: example: 2020-04-10T17:00:00.000Z
    startTime: Optional[datetime] = None
    #: The date and time when this video session ended.
    #: example: 2020-04-10T18:00:00.000Z
    endTime: Optional[datetime] = None
    #: The percentage of video packet loss, as a float between 0.0 and 100.0, during each sampling interval.
    #: example: [0.01, 0.1, 0.05]
    packetLoss: Optional[list[float]] = None
    #: The average latency, in milliseconds, during each sampling interval.
    #: example: [60.0, 5.0, 10.0]
    latency: Optional[list[float]] = None
    #: The pixel height of the incoming video.
    #: example: [90.0, 90.0, 90.0]
    resolutionHeight: Optional[list[float]] = None
    #: The frames per second of the incoming video.
    #: example: [25.940000534057617, 21.040000915527344, 18.84000015258789]
    frameRate: Optional[list[float]] = None
    #: The bit rate of the incoming video.
    #: example: [51880.0, 74519.0, 55285.0]
    mediaBitRate: Optional[list[float]] = None
    #: The incoming video codec.
    #: example: H.264 BP
    codec: Optional[str] = None
    #: The incoming video jitter.
    #: example: [170.0, 130.0, 40.0]
    jitter: Optional[list[float]] = None
    #: The network protocol used for video transmission.
    #: example: UDP
    transportType: Optional[VideoInTransportType] = None


class Resources(ApiModel):
    #: The average percent CPU for the process.
    #: example: [6.0, 8.0, 6.0]
    processAverageCPU: Optional[list[float]] = None
    #: The max percent CPU for the process.
    #: example: [14.0, 15.0, 14.0]
    processMaxCPU: Optional[list[float]] = None
    #: The average percent CPU for the system.
    #: example: [19.0, 21.0, 18.0]
    systemAverageCPU: Optional[list[float]] = None
    #: The max percent CPU for the system.
    #: example: [27.0, 36.0, 30.0]
    systemMaxCPU: Optional[list[float]] = None


class MediaSessionQuality(ApiModel):
    #: The meeting identifier for the specific meeting instance.
    #: example: e5dba9613a9d455aa49f6ffdafb6e7db_I_191395283063545470
    meetingInstanceId: Optional[str] = None
    #: The display name of the participant of this media session.
    #: example: John Andersen
    webexUserName: Optional[str] = None
    #: The email address of the participant of this media session.
    #: example: john.andersen@example.com
    webexUserEmail: Optional[str] = None
    #: The date and time when this participant joined the meeting.
    #: example: 2020-04-10T17:00:00.000Z
    joinTime: Optional[datetime] = None
    #: The date and time when this participant left the meeting.
    #: example: 2020-04-10T17:02:00.000Z
    leaveTime: Optional[datetime] = None
    #: The join meeting time of the participant.
    #: example: 5.793
    joinMeetingTime: Optional[datetime] = None
    #: The type of the client (and OS) used by this media session.
    #: example: Teams_Mobile_Client (iOS)
    clientType: Optional[str] = None
    #: The version of the client used by this media session.
    #: example: 40.5.0.210
    clientVersion: Optional[str] = None
    #: The operating system used for the client.
    #: example: mac
    osType: Optional[str] = None
    #: The version of the operating system used for the client.
    #: example: Version 10.14.6 (Build 18G3020)
    osVersion: Optional[str] = None
    #: The type of hardware used to attend the meeting
    #: example: mac book
    hardwareType: Optional[str] = None
    #: A description of the speaker used in the meeting.
    #: example: MacBook Pro Speakers
    speakerName: Optional[str] = None
    #: The type of network.
    #: example: wifi
    networkType: Optional[MediaSessionQualityNetworkType] = None
    #: The local IP address of the client.
    #: example: 10.24.72.54
    localIP: Optional[str] = None
    #: The public IP address of the client.
    #: example: 10.24.72.54
    publicIP: Optional[str] = None
    #: The masked local IP address of the client.
    #: example: 10.24.72.54
    maskedLocalIP: Optional[str] = None
    #: The masked public IP address of the client.
    #: example: 10.24.72.54
    maskedPublicIP: Optional[str] = None
    #: A description of the camera used in the meeting.
    #: example: FaceTime HD Camera
    camera: Optional[str] = None
    #: A description of the microphone used in the meeting.
    #: example: External Microphone
    microphone: Optional[str] = None
    #: The server region.
    #: example: San Jose, USA
    serverRegion: Optional[str] = None
    #: The video mesh cluster name.
    #: example: Mesh Cluster One
    videoMeshCluster: Optional[str] = None
    #: The video mesh server name.
    #: example: server.example.com
    videoMeshServer: Optional[str] = None
    #: Identifies the participant.
    #: example: 8635cbf0ca1a4573b27348e560679b25_I_158174534545967299_57
    participantId: Optional[str] = None
    #: Identifies a specific session the participant has in a given meeting.
    #: example: 3324C9D0-9EA7-45A2-B249-5B62A384AFEF
    participantSessionId: Optional[str] = None
    #: The collection of downstream (sent to the client) video quality data.
    videoIn: Optional[list[VideoIn]] = None
    #: The collection of upstream (sent from the client) video quality data.
    videoOut: Optional[list[VideoIn]] = None
    #: The collection of downstream (sent to the client) audio quality data.
    audioIn: Optional[list[VideoIn]] = None
    #: The collection of upstream (sent from the client) audio quality data.
    audioOut: Optional[list[VideoIn]] = None
    #: The collection of downstream (sent to the client) share quality data.
    shareIn: Optional[list[VideoIn]] = None
    #: The collection of upstream (sent from the client) share quality data.
    shareOut: Optional[list[VideoIn]] = None
    #: Device resources such as CPU and memory.
    resources: Optional[list[Resources]] = None


class MeetingQualitiesResponse(ApiModel):
    items: Optional[list[MediaSessionQuality]] = None
