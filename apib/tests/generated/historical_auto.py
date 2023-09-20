from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['NoneMetrics', 'NoneMetricsParticipantsByJoinMethods', 'NoneMetricsParticipantsByLocation', 'NoneMetricsParticipantsByRoles', 'NoneMetricsSharing']


class NoneMetricsSharing(ApiModel):
    #: example: [1,1]
    localsharingcableUsageDuration: Optional[str] = None
    #: example: [2,2]
    localsharingwirelessUsageDuration: Optional[str] = None


class NoneMetricsParticipantsByJoinMethods(ApiModel):
    #: example: 123.0
    webApp: Optional[int] = None
    #: example: 123.0
    cloudVideoDevice: Optional[int] = None
    #: example: 123.0
    mobileMeetingsApp: Optional[int] = None


class NoneMetricsParticipantsByRoles(ApiModel):
    #: example: 123.0
    host: Optional[int] = None
    #: example: 123.0
    attendee: Optional[int] = None


class NoneMetricsParticipantsByLocation(ApiModel):
    #: example: United States
    country: Optional[str] = None
    #: example: 123.0
    totalParticipants: Optional[int] = None


class NoneMetrics(ApiModel):
    #: Total number of meetings held over the selected date range. includes Webex Meetings, Webex Events, Webex Support, and Webex Training sessions
    #: example: 123.0
    totalMeetings: Optional[int] = None
    #: Total number of joins by participant and devices from all Webex meetings over the selected date range
    #: example: 123.0
    totalParticipants: Optional[int] = None
    #: Total number of unique hosts who started at least one webex meeting over the selected date range
    #: example: 123.0
    totalUniqueHosts: Optional[int] = None
    #: Total number of minutes for all meetings over selected date range
    #: example: 1234.0
    totalMeetingMinutes: Optional[int] = None
    #: Total number of VoIP and telephony minutes used during meetings over the selected date range
    #: example: 1234.0
    totalAudioMinutes: Optional[int] = None
    #: example: 1234.0
    totalTelephoneMinutes: Optional[int] = None
    #: example: 1234.0
    totalVoIPMinutes: Optional[int] = None
    #: Total number of meetings held where at least one participant enabled video for any amount of time
    #: example: 123.0
    videoMeetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enabled sharing for any amount of time
    #: example: 123.0
    sharingMeetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enable recording for any amount of time
    #: example: 123.0
    recordingMeetings: Optional[int] = None
    #: Participant Count for each join/client type. This list is dynamic and can change
    participantsByJoinMethods: Optional[NoneMetricsParticipantsByJoinMethods] = None
    #: Participant Count for each Role
    participantsByRoles: Optional[NoneMetricsParticipantsByRoles] = None
    #: Participant Count for each Location. This is a json array of countries
    participantsByLocation: Optional[list[NoneMetricsParticipantsByLocation]] = None
