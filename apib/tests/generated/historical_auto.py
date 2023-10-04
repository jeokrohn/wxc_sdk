from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['HistoricalDataRelatedToMeetingsResponse', 'HistoricalDataRelatedToMeetingsResponseMetrics', 'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByJoinMethods', 'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByLocation', 'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByRoles', 'HistoricalDataRelatedToMessagingResponse', 'HistoricalDataRelatedToMessagingResponseMetrics', 'HistoricalDataRelatedToMessagingResponseMetricsSharing', 'HistoricalDataRelatedToRoomDevicesResponse', 'HistoricalDataRelatedToRoomDevicesResponseMetrics', 'HistoricalDataRelatedToRoomDevicesResponseMetricsSharing']


class HistoricalDataRelatedToMessagingResponseMetricsSharing(ApiModel):
    #: example: [1,2]
    total_files_shared: Optional[str] = None
    #: example: `[6,7]` ## Bytes
    file_share_size: Optional[str] = None


class HistoricalDataRelatedToMessagingResponseMetrics(ApiModel):
    #: An Array containing the UTC dates for which the data is returned.
    #: example: ['2020-08-01','2020-08-02']
    dates: Optional[str] = None
    #: An array containing the aggregated values for each day for which the data is returned.
    #: example: [200, 300]
    daily_active_users: Optional[str] = None
    #: example: [2000, 3000]
    total_messages_sent: Optional[str] = None
    #: example: [289, 456]
    desk_top_messages_sent: Optional[str] = None
    #: example: [122, 233]
    mobile_messages_sent: Optional[str] = None
    #: example: [2,3]
    total_active_spaces: Optional[str] = None
    #: example: [3,4]
    group_active_spaces: Optional[str] = None
    #: example: [5,6]
    one2one_active_spaces: Optional[str] = None
    video: Optional[str] = None
    sharing: Optional[HistoricalDataRelatedToMessagingResponseMetricsSharing] = None
    recording: Optional[str] = None
    audio: Optional[str] = None


class HistoricalDataRelatedToMessagingResponse(ApiModel):
    #: UTC start date of the data set.
    #: example: 2020-08-01
    start_date: Optional[datetime] = None
    #: UTC end date of the data set.
    #: example: 2020-08-03
    end_date: Optional[datetime] = None
    metrics: Optional[HistoricalDataRelatedToMessagingResponseMetrics] = None


class HistoricalDataRelatedToRoomDevicesResponseMetricsSharing(ApiModel):
    #: example: [1,1]
    localsharingcable_usage_duration: Optional[str] = None
    #: example: [2,2]
    localsharingwireless_usage_duration: Optional[str] = None


class HistoricalDataRelatedToRoomDevicesResponseMetrics(ApiModel):
    #: An Array containing the UTC dates for which the data is returned
    #: example: ['2020-08-01','2020-08-02']
    dates: Optional[str] = None
    #: An array containing the aggregated values for each day for which the data is returned.
    #: example: [200,300]
    total_active_devices: Optional[str] = None
    #: example: [2,3]
    total_assistant_commands: Optional[str] = None
    #: example: [100,100]
    total_usage_hours: Optional[str] = None
    #: example: [50,50]
    incall_usage_duration: Optional[str] = None
    #: example: [1,1]
    signage_usage_duration: Optional[str] = None
    #: example: [1,2]
    usbpassthrough_usage_duration: Optional[str] = None
    #: example: [3,4]
    whiteboarding_usage_duration: Optional[str] = None
    video: Optional[str] = None
    sharing: Optional[HistoricalDataRelatedToRoomDevicesResponseMetricsSharing] = None
    recording: Optional[str] = None
    audio: Optional[str] = None


class HistoricalDataRelatedToRoomDevicesResponse(ApiModel):
    #: Data is returned starting from this UTC date.
    #: example: 2020-08-01
    start_date: Optional[datetime] = None
    #: Data is returned up to this UTC date.
    #: example: 2020-08-03
    end_date: Optional[datetime] = None
    metrics: Optional[HistoricalDataRelatedToRoomDevicesResponseMetrics] = None


class HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByJoinMethods(ApiModel):
    #: example: 123.0
    web_app: Optional[int] = None
    #: example: 123.0
    cloud_video_device: Optional[int] = None
    #: example: 123.0
    mobile_meetings_app: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByRoles(ApiModel):
    #: example: 123.0
    host: Optional[int] = None
    #: example: 123.0
    attendee: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByLocation(ApiModel):
    #: example: United States
    country: Optional[str] = None
    #: example: 123.0
    total_participants: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetrics(ApiModel):
    #: Total number of meetings held over the selected date range. includes Webex Meetings, Webex Events, Webex Support, and Webex Training sessions
    #: example: 123.0
    total_meetings: Optional[int] = None
    #: Total number of joins by participant and devices from all Webex meetings over the selected date range
    #: example: 123.0
    total_participants: Optional[int] = None
    #: Total number of unique hosts who started at least one webex meeting over the selected date range
    #: example: 123.0
    total_unique_hosts: Optional[int] = None
    #: Total number of minutes for all meetings over selected date range
    #: example: 1234.0
    total_meeting_minutes: Optional[int] = None
    #: Total number of VoIP and telephony minutes used during meetings over the selected date range
    #: example: 1234.0
    total_audio_minutes: Optional[int] = None
    #: example: 1234.0
    total_telephone_minutes: Optional[int] = None
    #: example: 1234.0
    total_vo_ipminutes: Optional[int] = Field(alias='totalVoIPMinutes', default=None)
    #: Total number of meetings held where at least one participant enabled video for any amount of time
    #: example: 123.0
    video_meetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enabled sharing for any amount of time
    #: example: 123.0
    sharing_meetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enable recording for any amount of time
    #: example: 123.0
    recording_meetings: Optional[int] = None
    #: Participant Count for each join/client type. This list is dynamic and can change
    participants_by_join_methods: Optional[HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByJoinMethods] = None
    #: Participant Count for each Role
    participants_by_roles: Optional[HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByRoles] = None
    #: Participant Count for each Location. This is a json array of countries
    participants_by_location: Optional[list[HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByLocation]] = None


class HistoricalDataRelatedToMeetingsResponse(ApiModel):
    #: Site related to which the data is returned.
    #: example: cisco.webex.com
    site_url: Optional[str] = None
    #: UTC start date of the data set.
    #: example: 2020-08-01
    start_date: Optional[datetime] = None
    #: UTC end date of the data set.
    #: example: 2020-08-03
    end_date: Optional[datetime] = None
    metrics: Optional[HistoricalDataRelatedToMeetingsResponseMetrics] = None
