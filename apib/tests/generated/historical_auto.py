from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['HistoricalAnalyticsAPIsApi', 'HistoricalDataRelatedToMeetingsResponse',
           'HistoricalDataRelatedToMeetingsResponseMetrics',
           'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByJoinMethods',
           'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByLocation',
           'HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByRoles',
           'HistoricalDataRelatedToMessagingResponse', 'HistoricalDataRelatedToMessagingResponseMetrics',
           'HistoricalDataRelatedToMessagingResponseMetricsSharing', 'HistoricalDataRelatedToRoomDevicesResponse',
           'HistoricalDataRelatedToRoomDevicesResponseMetrics',
           'HistoricalDataRelatedToRoomDevicesResponseMetricsSharing']


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
    #: example: 123
    web_app: Optional[int] = None
    #: example: 123
    cloud_video_device: Optional[int] = None
    #: example: 123
    mobile_meetings_app: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByRoles(ApiModel):
    #: example: 123
    host: Optional[int] = None
    #: example: 123
    attendee: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetricsParticipantsByLocation(ApiModel):
    #: example: United States
    country: Optional[str] = None
    #: example: 123
    total_participants: Optional[int] = None


class HistoricalDataRelatedToMeetingsResponseMetrics(ApiModel):
    #: Total number of meetings held over the selected date range. includes Webex Meetings, Webex Events, Webex
    #: Support, and Webex Training sessions
    #: example: 123
    total_meetings: Optional[int] = None
    #: Total number of joins by participant and devices from all Webex meetings over the selected date range
    #: example: 123
    total_participants: Optional[int] = None
    #: Total number of unique hosts who started at least one webex meeting over the selected date range
    #: example: 123
    total_unique_hosts: Optional[int] = None
    #: Total number of minutes for all meetings over selected date range
    #: example: 1234
    total_meeting_minutes: Optional[int] = None
    #: Total number of VoIP and telephony minutes used during meetings over the selected date range
    #: example: 1234
    total_audio_minutes: Optional[int] = None
    #: example: 1234
    total_telephone_minutes: Optional[int] = None
    #: example: 1234
    total_vo_ipminutes: Optional[int] = Field(alias='totalVoIPMinutes', default=None)
    #: Total number of meetings held where at least one participant enabled video for any amount of time
    #: example: 123
    video_meetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enabled sharing for any amount of time
    #: example: 123
    sharing_meetings: Optional[int] = None
    #: Total number of meetings held where at least one participant enable recording for any amount of time
    #: example: 123
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


class HistoricalAnalyticsAPIsApi(ApiChild, base='v1/analytics'):
    """
    Historical Analytics APIs
    
    The base URL for these APIs is **analytics.webexapis.com**, which does not
    work with the **Try It** feature. If you have any questions or need help
    please contact the Webex Developer Support team at devsupport@webex.com.
    
    
    
    These APIs allow an administrator to pull historical analytics data for meetings, messaging and room devices.
    
    This API requires a `Pro Pack for Control Hub
    <https://help.webex.com/article/np3c1rm>`_ license. API requests require an access token representing an
    administrator with either a read-only admin or full-admin role for the associated organization. The token must
    have the `analytics:read_all` scope.
    
    By default, the calls to analytics.webexapis.com for historical data are sent to the closest region servers. The
    other possible region servers are analytics-eu.webexapis.com and analytics-ca.webexapis.com. If the region servers
    host the organization's data, then the data is returned. Otherwise, an HTTP 451 error code ('Unavailable For Legal
    Reasons') is returned. The body of the response in this case contains the end point information from where user
    can get historical data for the user's organization. Below is a sample error message looks in this condition.
    
    ```javascript
    {
    "message": "This server cannot serve the data for this organization. Please use {another region's VIP}",
    "errorCode": 451,
    "trackingId": {trackingId}
    }
    ```
    
    To use this API the org needs to be licensed for pro pack.
    """

    def historical_data_related_to_messaging(self, from_: Union[str, datetime] = None, to_: Union[str,
                                             datetime] = None) -> HistoricalDataRelatedToMessagingResponse:
        """
        Historical Data related to Messaging

        Returns daily aggregates of various metrics related to Webex messaging.

        <div><Callout type="error">The base URL for these APIs is **analytics.webexapis.com**, which does not work with
        the **Try It** feature. </Callout></div>

        :param from_: UTC date starting from which the data needs to be returned.
        :type from_: Union[str, datetime]
        :param to_: UTC date up to which the data needs to be returned
        :type to_: Union[str, datetime]
        :rtype: :class:`HistoricalDataRelatedToMessagingResponse`
        """
        params = {}
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep('messagingMetrics/dailyTotals')
        data = super().get(url, params=params)
        r = HistoricalDataRelatedToMessagingResponse.model_validate(data)
        return r

    def historical_data_related_to_room_devices(self, from_: Union[str, datetime] = None, to_: Union[str,
                                                datetime] = None) -> HistoricalDataRelatedToRoomDevicesResponse:
        """
        Historical Data related to Room Devices

        Returns daily aggregates of various metrics related to Room Devices.

        <div><Callout type="error">The base URL for these APIs is **analytics.webexapis.com**, which does not work with
        the **Try It** feature. </Callout></div>

        :param from_: Starting UTC Date from which historical data should be returned.
        :type from_: Union[str, datetime]
        :param to_: Ending UTC Date for which data should be returned.
        :type to_: Union[str, datetime]
        :rtype: :class:`HistoricalDataRelatedToRoomDevicesResponse`
        """
        params = {}
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep('roomDeviceMetrics/dailyTotals')
        data = super().get(url, params=params)
        r = HistoricalDataRelatedToRoomDevicesResponse.model_validate(data)
        return r

    def historical_data_related_to_meetings(self, site_url: str, from_: Union[str, datetime] = None, to_: Union[str,
                                            datetime] = None) -> HistoricalDataRelatedToMeetingsResponse:
        """
        Historical Data related to Meetings

        Return aggregates of various metrics related to meetings for a given Webex site over a specified time range.

        <div><Callout type="error">The base URL for these APIs is **analytics.webexapis.com**, which does not work with
        the **Try It** feature.</Callout></div>

        :param site_url: URL of the Webex site for which historical data is requested.
        :type site_url: str
        :param from_: UTC Date starting from which the data needs to be returned
        :type from_: Union[str, datetime]
        :param to_: UTC Date up to which the data needs to be returned
        :type to_: Union[str, datetime]
        :rtype: :class:`HistoricalDataRelatedToMeetingsResponse`
        """
        params = {}
        params['siteUrl'] = site_url
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep('meetingsMetrics/aggregates')
        data = super().get(url, params=params)
        r = HistoricalDataRelatedToMeetingsResponse.model_validate(data)
        return r
