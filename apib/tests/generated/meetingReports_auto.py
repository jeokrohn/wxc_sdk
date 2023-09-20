from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['MeetingAttendeeReportObject', 'MeetingAttendeeReportObjectParticipantType', 'MeetingUsageReportObject', 'MeetingUsageReportObjectScheduledType', 'MeetingUsageReportObjectServiceType', 'MeetingUsageReportTrackingCodeObject']


class MeetingUsageReportObjectScheduledType(str, Enum):
    #: Regular meeting.
    meeting = 'meeting'
    #: Webinar meeting.
    webinar = 'webinar'


class MeetingUsageReportObjectServiceType(str, Enum):
    #: The service type for the usage report is meeting.
    meetingcenter = 'MeetingCenter'
    #: The service type for the usage report is the event.
    eventcenter = 'EventCenter'
    #: The service type for the usage report is the training session.
    trainingcenter = 'TrainingCenter'
    #: The service type for the usage report is the support meeting.
    supportcenter = 'SupportCenter'


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
    meetingId: Optional[str] = None
    #: Meeting number.
    #: example: 123456789
    meetingNumber: Optional[str] = None
    #: Meeting title.
    #: example: John's Meeting
    meetingTitle: Optional[str] = None
    #: The date and time when the meeting was started. It's in the timezone specified in the request header or in the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:26:30+08:00
    start: Optional[datetime] = None
    #: The date and time when the meeting was ended. It's in the timezone specified in the request header or in the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:46:30+08:00
    end: Optional[datetime] = None
    #: Duration of the meeting in minutes.
    #: example: 20.0
    duration: Optional[int] = None
    #: Scheduled type for the meeting.
    #: example: meeting
    scheduledType: Optional[MeetingUsageReportObjectScheduledType] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    hostDisplayName: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    hostEmail: Optional[str] = None
    #: Aggregated attendee minutes.
    #: example: 60.0
    totalPeopleMinutes: Optional[int] = None
    #: Aggregated attendee PSTN call-in minutes.
    #: example: 60.0
    totalCallInMinutes: Optional[int] = None
    #: Aggregated attendee domestic PSTN call-out minutes.
    #: example: 60.0
    totalCallOutDomestic: Optional[int] = None
    #: Aggregated attendee toll-free PSTN call-in minutes.
    #: example: 60.0
    totalCallInTollFreeMinutes: Optional[int] = None
    #: Aggregated attendee international PSTN call-out minutes.
    #: example: 60.0
    totalCallOutInternational: Optional[int] = None
    #: Aggregated attendee VoIP minutes.
    #: example: 60.0
    totalVoipMinutes: Optional[int] = None
    #: Total number of participants of the meeting.
    #: example: 30.0
    totalParticipants: Optional[int] = None
    #: Total number of VoIP participants of the meeting.
    #: example: 10.0
    totalParticipantsVoip: Optional[int] = None
    #: Total number of PSTN call-in participants of the meeting.
    #: example: 10.0
    totalParticipantsCallIn: Optional[int] = None
    #: Total number of PSTN call-out participants of the meeting.
    #: example: 10.0
    totalParticipantsCallOut: Optional[int] = None
    #: Peak number of attendees throughout the meeting.
    #: example: 30.0
    peakAttendee: Optional[int] = None
    #: Total number of registrants of the meeting.
    #: example: 30.0
    totalRegistered: Optional[int] = None
    #: Total number of invitees of the meeting.
    #: example: 30.0
    totalInvitee: Optional[int] = None
    #: The service type for the meeting usage report.
    #: example: MeetingCenter
    serviceType: Optional[MeetingUsageReportObjectServiceType] = None
    #: Tracking codes of the meeting.
    trackingCodes: Optional[list[MeetingUsageReportTrackingCodeObject]] = None


class MeetingAttendeeReportObjectParticipantType(str, Enum):
    #: Meeting host.
    host = 'host'
    #: Meeting attendee.
    attendee = 'attendee'


class MeetingAttendeeReportObject(ApiModel):
    #: Unique identifier for the meeting.
    #: example: 089b137c3cf34b578896941e2d49dfe8_I_146987372776523573
    meetingId: Optional[str] = None
    #: Meeting number.
    #: example: 123456789.0
    meetingNumber: Optional[int] = None
    #: Meeting title.
    #: example: John's Meeting
    meetingTitle: Optional[str] = None
    #: Attendee's display name.
    #: example: John Andersen
    displayName: Optional[str] = None
    #: Attendee's email.
    #: example: John Andersen
    email: Optional[str] = None
    #: The date and time when the attendee joined the meeting. It's in the timezone specified in the request header or in the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:26:30+08:00
    joinedTime: Optional[datetime] = None
    #: The date and time when the attendee left the meeting. It's in the timezone specified in the request header or in the `UTC` timezone if timezone is not specified.
    #: example: 2023-01-18T10:46:30+08:00
    leftTime: Optional[datetime] = None
    #: Duration of the attendee in the meeting in minutes.
    #: example: 20.0
    duration: Optional[int] = None
    #: The attendee's role in the meeting.
    #: example: host
    participantType: Optional[MeetingAttendeeReportObjectParticipantType] = None
    #: IP address of the attendee when he attended the meeting.
    #: example: 172.16.244.151
    ipAddress: Optional[str] = None
    #: Information of the attendee's operating system and application when he attended the meeting.
    #: example: WINDOWS,IE
    clientAgent: Optional[str] = None
    #: Attendee's company.
    #: example: ExampleCompany
    company: Optional[str] = None
    #: Attendee's phone number.
    #: example: 85763644
    phoneNumber: Optional[str] = None
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
    zipCode: Optional[str] = None
    #: Whether or not the attendee has registered the meeting.
    registered: Optional[bool] = None
    #: Whether or not the attendee has been invited to the meeting.
    invited: Optional[bool] = None
