from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['NoneMetrics', 'NoneMetricsParticipantsByJoinMethods', 'NoneMetricsParticipantsByLocation', 'NoneMetricsParticipantsByRoles', 'NoneMetricsSharing']


class NoneMetricsSharing(ApiModel):
    #: example: [1,1]
    localsharingcable_usage_duration: Optional[str] = None
    #: example: [2,2]
    localsharingwireless_usage_duration: Optional[str] = None


class NoneMetricsParticipantsByJoinMethods(ApiModel):
    #: example: 123.0
    web_app: Optional[int] = None
    #: example: 123.0
    cloud_video_device: Optional[int] = None
    #: example: 123.0
    mobile_meetings_app: Optional[int] = None


class NoneMetricsParticipantsByRoles(ApiModel):
    #: example: 123.0
    host: Optional[int] = None
    #: example: 123.0
    attendee: Optional[int] = None


class NoneMetricsParticipantsByLocation(ApiModel):
    #: example: United States
    country: Optional[str] = None
    #: example: 123.0
    total_participants: Optional[int] = None


class NoneMetrics(ApiModel):
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
    participants_by_join_methods: Optional[NoneMetricsParticipantsByJoinMethods] = None
    #: Participant Count for each Role
    participants_by_roles: Optional[NoneMetricsParticipantsByRoles] = None
    #: Participant Count for each Location. This is a json array of countries
    participants_by_location: Optional[list[NoneMetricsParticipantsByLocation]] = None
