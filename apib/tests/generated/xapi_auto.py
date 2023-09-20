from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['NoneArguments', 'NoneResult', 'NoneResultAudio', 'NoneResultBooking', 'NoneResultBookingOrganizer', 'NoneResultBookingTime']


class NoneResultAudio(ApiModel):
    #: example: 75.0
    Volume: Optional[int] = None


class NoneResultBookingTime(ApiModel):
    #: example: 2020-07-01T13:00:00Z
    StartTime: Optional[datetime] = None
    #: example: 60.0
    Duration: Optional[int] = None


class NoneResultBookingOrganizer(ApiModel):
    #: example: John Doe
    Name: Optional[str] = None


class NoneResultBooking(ApiModel):
    #: example: foo
    Id: Optional[str] = None
    #: example: Booking Title
    Title: Optional[str] = None
    #: example: SIP
    Protocol: Optional[str] = None
    Time: Optional[NoneResultBookingTime] = None
    Organizer: Optional[NoneResultBookingOrganizer] = None
    #: example: number@example.com
    Number: Optional[str] = None


class NoneResult(ApiModel):
    Booking: Optional[NoneResultBooking] = None


class NoneArguments(ApiModel):
    #: example: 50.0
    Level: Optional[int] = None
