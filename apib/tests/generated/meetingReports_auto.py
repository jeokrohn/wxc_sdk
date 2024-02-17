from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['MeetingAttendeeReportObject', 'MeetingAttendeeReportObjectParticipantType', 'MeetingUsageReportObject',
           'MeetingUsageReportObjectScheduledType', 'MeetingUsageReportObjectServiceType',
           'MeetingUsageReportTrackingCodeObject', 'MeetingsSummaryReportApi']


class MeetingUsageReportObjectScheduledType(str, Enum):
    #: Regular meeting.
    meeting = 'meeting'
    #: Webinar meeting.
    webinar = 'webinar'


class MeetingUsageReportObjectServiceType(str, Enum):
    #: The service type for the usage report is meeting.
    meeting_center = 'MeetingCenter'
    #: The service type for the usage report is the event.
    event_center = 'EventCenter'
    #: The service type for the usage report is the training session.
    training_center = 'TrainingCenter'
    #: The service type for the usage report is the support meeting.
    support_center = 'SupportCenter'


class MeetingUsageReportTrackingCodeObject(ApiModel):
    #: Name of the tracking code.
    #: example: Department
    name: Optional[str] = None
    #: Value of the tracking code.
    #: example: Engineering
    value: Optional[str] = None


class MeetingUsageReportObject(ApiModel):
    #: Unique identifier for the meeting.
    #: example: 089b137c3cf34b578896941e2d49dfe8_I_146987372776523573
    meeting_id: Optional[str] = None
    #: Meeting number.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title.
    #: example: John's Meeting
    meeting_title: Optional[str] = None
    #: The date and time when the meeting was started. It's in the timezone specified in the request header or in the
    #: `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:26:30+08:00
    start: Optional[datetime] = None
    #: The date and time when the meeting was ended. It's in the timezone specified in the request header or in the
    #: `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:46:30+08:00
    end: Optional[datetime] = None
    #: Duration of the meeting in minutes.
    #: example: 20
    duration: Optional[int] = None
    #: Scheduled type for the meeting.
    #: example: meeting
    scheduled_type: Optional[MeetingUsageReportObjectScheduledType] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Aggregated attendee minutes.
    #: example: 60
    total_people_minutes: Optional[int] = None
    #: Aggregated attendee PSTN call-in minutes.
    #: example: 60
    total_call_in_minutes: Optional[int] = None
    #: Aggregated attendee domestic PSTN call-out minutes.
    #: example: 60
    total_call_out_domestic: Optional[int] = None
    #: Aggregated attendee toll-free PSTN call-in minutes.
    #: example: 60
    total_call_in_toll_free_minutes: Optional[int] = None
    #: Aggregated attendee international PSTN call-out minutes.
    #: example: 60
    total_call_out_international: Optional[int] = None
    #: Aggregated attendee VoIP minutes.
    #: example: 60
    total_voip_minutes: Optional[int] = None
    #: Total number of participants of the meeting.
    #: example: 30
    total_participants: Optional[int] = None
    #: Total number of VoIP participants of the meeting.
    #: example: 10
    total_participants_voip: Optional[int] = None
    #: Total number of PSTN call-in participants of the meeting.
    #: example: 10
    total_participants_call_in: Optional[int] = None
    #: Total number of PSTN call-out participants of the meeting.
    #: example: 10
    total_participants_call_out: Optional[int] = None
    #: Peak number of attendees throughout the meeting.
    #: example: 30
    peak_attendee: Optional[int] = None
    #: Total number of registrants of the meeting.
    #: example: 30
    total_registered: Optional[int] = None
    #: Total number of invitees of the meeting.
    #: example: 30
    total_invitee: Optional[int] = None
    #: The service type for the meeting usage report.
    #: example: MeetingCenter
    service_type: Optional[MeetingUsageReportObjectServiceType] = None
    #: Tracking codes of the meeting.
    tracking_codes: Optional[list[MeetingUsageReportTrackingCodeObject]] = None


class MeetingAttendeeReportObjectParticipantType(str, Enum):
    #: Meeting host.
    host = 'host'
    #: Meeting attendee.
    attendee = 'attendee'


class MeetingAttendeeReportObject(ApiModel):
    #: Unique identifier for the meeting.
    #: example: 089b137c3cf34b578896941e2d49dfe8_I_146987372776523573
    meeting_id: Optional[str] = None
    #: Meeting number.
    #: example: 123456789
    meeting_number: Optional[int] = None
    #: Meeting title.
    #: example: John's Meeting
    meeting_title: Optional[str] = None
    #: Attendee's display name.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: Attendee's email.
    #: example: John Andersen
    email: Optional[str] = None
    #: The date and time when the attendee joined the meeting. It's in the timezone specified in the request header or
    #: in the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:26:30+08:00
    joined_time: Optional[datetime] = None
    #: The date and time when the attendee left the meeting. It's in the timezone specified in the request header or in
    #: the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:46:30+08:00
    left_time: Optional[datetime] = None
    #: Duration of the attendee in the meeting in minutes.
    #: example: 20
    duration: Optional[int] = None
    #: The attendee's role in the meeting.
    #: example: host
    participant_type: Optional[MeetingAttendeeReportObjectParticipantType] = None
    #: IP address of the attendee when he attended the meeting.
    #: example: 172.16.244.151
    ip_address: Optional[str] = None
    #: Information of the attendee's operating system and application when he attended the meeting.
    #: example: WINDOWS,IE
    client_agent: Optional[str] = None
    #: Attendee's company.
    #: example: ExampleCompany
    company: Optional[str] = None
    #: Attendee's phone number.
    #: example: 85763644
    phone_number: Optional[str] = None
    #: Attendee's address, part one.
    #: example: 85763644
    address1: Optional[str] = None
    #: Attendee's address, part two.
    #: example: 85763644
    address2: Optional[str] = None
    #: Attendee's city.
    #: example: 85763644
    city: Optional[str] = None
    #: Attendee's state.
    #: example: 85763644
    state: Optional[str] = None
    #: Attendee's country.
    #: example: 85763644
    country: Optional[str] = None
    #: Attendee's zip code.
    #: example: 85763644
    zip_code: Optional[str] = None
    #: Whether or not the attendee has registered the meeting.
    registered: Optional[bool] = None
    #: Whether or not the attendee has been invited to the meeting.
    invited: Optional[bool] = None


class MeetingsSummaryReportApi(ApiChild, base='meetingReports'):
    """
    Meetings Summary Report
    
    The meeting usage report API is used to retrieve aggregated meeting usage information, like `totalCallInMinutes`,
    `totalParticipants`, etc. It also includes the meeting `trackingCodes`.
    
    The meeting attendee report API is used to retrieve aggregated meeting attendee information, like `joinedTime`,
    `leftTime`, `duration`, etc.
    
    The report data for a meeting should be available within 24 hours after the meeting ended.
    
    Refer to the `Meetings API Scopes` section of `Meetings Overview
    <https://developer.webex.com/docs/meetings>`_ for scopes required for each API.
    """

    def list_meeting_usage_reports(self, site_url: str, service_type: str = None, from_: Union[str, datetime] = None,
                                   to_: Union[str, datetime] = None,
                                   **params) -> Generator[MeetingUsageReportObject, None, None]:
        """
        List Meeting Usage Reports

        List meeting usage reports of all the users on the specified site by an admin. You can specify a date range and
        the maximum number of meeting usage reports to return.

        The list returned is sorted in descending order by the date and time the meetings were started.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * `siteUrl` is required, and the meeting usage reports of the specified site are listed. All available Webex
        sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        defined.

        :param site_url: URL of the Webex site which the API lists meeting usage reports from. All available Webex
            sites can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param service_type: Meeting usage report's service-type. If `serviceType` is specified, the API filters
            meeting usage reports by service-type. If `serviceType` is not specified, the API returns meeting usage
            reports by `MeetingCenter` by default. Valid values:

        + `MeetingCenter`

        + `EventCenter`

        + `SupportCenter`

        + `TrainingCenter`
        :type service_type: str
        :param from_: Starting date and time for meeting usage reports to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`. The interval between `to` and `from` cannot exceed 30 days and `from` cannot
            be earlier than 90 days ago.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time for meeting usage reports to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `to`
            cannot be before `from`. The interval between `to` and `from` cannot exceed 30 days.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`MeetingUsageReportObject` instances
        """
        params['siteUrl'] = site_url
        if service_type is not None:
            params['serviceType'] = service_type
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
        url = self.ep('usage')
        return self.session.follow_pagination(url=url, model=MeetingUsageReportObject, item_key='items', params=params)

    def list_meeting_attendee_reports(self, site_url: str, meeting_id: str = None, meeting_number: str = None,
                                      meeting_title: str = None, from_: Union[str, datetime] = None, to_: Union[str,
                                      datetime] = None,
                                      **params) -> Generator[MeetingAttendeeReportObject, None, None]:
        """
        List Meeting Attendee Reports

        Lists of meeting attendee reports by a date range, the maximum number of meeting attendee reports, a meeting
        ID, a meeting number or a meeting title.

        If the requesting user is an admin, the API returns meeting attendee reports of the meetings hosted by all the
        users on the specified site filtered by meeting ID, meeting number or meeting title.

        If it's a normal meeting host, the API returns meeting attendee reports of the meetings hosted by the user
        himself on the specified site filtered by meeting ID, meeting number or meeting title.

        The list returned is grouped by meeting instances. Both the groups and items of each group are sorted in
        descending order of `joinedTime`. For example, if `meetingId` is specified and it's a meeting series ID, the
        returned list is grouped by meeting instances of that series. The groups are sorted in descending order of
        `joinedTime`, and within each group the items are also sorted in descending order of `joinedTime`. Please
        refer to `Meetings Overview
        <https://developer.webex.com/docs/meetings>`_ for details of meeting series, scheduled meeting and meeting instance.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * `siteUrl` is required, and the meeting attendee reports of the specified site are listed. All available Webex
        sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * `meetingId`, `meetingNumber` and `meetingTitle` are optional parameters to query the meeting attendee
        reports, but at least one of them should be specified. If more than one parameter in the sequence of
        `meetingId`, `meetingNumber`, and `meetingTitle` are specified, the first one in the sequence is used.
        Currently, only ended meeting instance IDs and meeting series IDs are supported for `meetingId`. IDs of
        scheduled meetings or personal room meetings are not supported.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        defined.

        :param site_url: URL of the Webex site which the API lists meeting attendee reports from. All available Webex
            sites can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param meeting_id: Meeting ID for the meeting attendee reports to return. If specified, return meeting attendee
            reports of the specified meeting; otherwise, return meeting attendee reports of all meetings. Currently,
            only ended meeting instance IDs are supported. IDs of meeting series, scheduled meetings or personal room
            meetings are not supported.
        :type meeting_id: str
        :param meeting_number: Meeting number for the meeting attendee reports to return. If specified, return meeting
            attendee reports of the specified meeting; otherwise, return meeting attendee reports of all meetings.
        :type meeting_number: str
        :param meeting_title: Meeting title for the meeting attendee reports to return. If specified, return meeting
            attendee reports of the specified meeting; otherwise, return meeting attendee reports of all meetings.
        :type meeting_title: str
        :param from_: Starting date and time for the meeting attendee reports to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant
            format. `from` cannot be after `to`. The interval between `to` and `from` cannot exceed 30 days and `from`
            cannot be earlier than 90 days ago.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time for the meeting attendee reports to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`. The interval between `to` and `from` cannot exceed 30 days.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`MeetingAttendeeReportObject` instances
        """
        params['siteUrl'] = site_url
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if meeting_title is not None:
            params['meetingTitle'] = meeting_title
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
        url = self.ep('attendees')
        return self.session.follow_pagination(url=url, model=MeetingAttendeeReportObject, item_key='items', params=params)
