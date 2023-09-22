from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ExecuteCommandArguments', 'ExecuteCommandBody', 'ExecuteCommandBodyBooking', 'ExecuteCommandBodyBookingOrganizer', 'ExecuteCommandBodyBookingTime']


class ExecuteCommandArguments(ApiModel):
    #: example: 50.0
    level: Optional[int] = Field(alias='Level', default=None)


class ExecuteCommandBodyBookingTime(ApiModel):
    #: example: 2020-07-01T13:00:00Z
    start_time: Optional[datetime] = Field(alias='StartTime', default=None)
    #: example: 60.0
    duration: Optional[int] = Field(alias='Duration', default=None)


class ExecuteCommandBodyBookingOrganizer(ApiModel):
    #: example: John Doe
    name: Optional[str] = Field(alias='Name', default=None)


class ExecuteCommandBodyBooking(ApiModel):
    #: example: foo
    id: Optional[str] = Field(alias='Id', default=None)
    #: example: Booking Title
    title: Optional[str] = Field(alias='Title', default=None)
    #: example: SIP
    protocol: Optional[str] = Field(alias='Protocol', default=None)
    time: Optional[ExecuteCommandBodyBookingTime] = Field(alias='Time', default=None)
    organizer: Optional[ExecuteCommandBodyBookingOrganizer] = Field(alias='Organizer', default=None)
    #: example: number@example.com
    number: Optional[str] = Field(alias='Number', default=None)


class ExecuteCommandBody(ApiModel):
    booking: Optional[ExecuteCommandBodyBooking] = Field(alias='Booking', default=None)
