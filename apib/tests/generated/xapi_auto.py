from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['NoneArguments', 'NoneResult', 'NoneResultAudio', 'NoneResultBooking', 'NoneResultBookingOrganizer', 'NoneResultBookingTime']


class NoneResultAudio(ApiModel):
    #: example: 75.0
    volume: Optional[int] = Field(alias='Volume', default=None)


class NoneResultBookingTime(ApiModel):
    #: example: 2020-07-01T13:00:00Z
    start_time: Optional[datetime] = Field(alias='StartTime', default=None)
    #: example: 60.0
    duration: Optional[int] = Field(alias='Duration', default=None)


class NoneResultBookingOrganizer(ApiModel):
    #: example: John Doe
    name: Optional[str] = Field(alias='Name', default=None)


class NoneResultBooking(ApiModel):
    #: example: foo
    id: Optional[str] = Field(alias='Id', default=None)
    #: example: Booking Title
    title: Optional[str] = Field(alias='Title', default=None)
    #: example: SIP
    protocol: Optional[str] = Field(alias='Protocol', default=None)
    time: Optional[NoneResultBookingTime] = Field(alias='Time', default=None)
    organizer: Optional[NoneResultBookingOrganizer] = Field(alias='Organizer', default=None)
    #: example: number@example.com
    number: Optional[str] = Field(alias='Number', default=None)


class NoneResult(ApiModel):
    booking: Optional[NoneResultBooking] = Field(alias='Booking', default=None)


class NoneArguments(ApiModel):
    #: example: 50.0
    level: Optional[int] = Field(alias='Level', default=None)
