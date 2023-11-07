from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ExecuteCommandArguments', 'ExecuteCommandBody', 'ExecuteCommandBodyBooking',
            'ExecuteCommandBodyBookingOrganizer', 'ExecuteCommandBodyBookingTime', 'ExecuteCommandResponse',
            'QueryStatusResponse', 'QueryStatusResponseResult', 'QueryStatusResponseResultAudio']


class QueryStatusResponseResultAudio(ApiModel):
    #: example: 75.0
    volume: Optional[int] = Field(alias='Volume', default=None)


class QueryStatusResponseResult(ApiModel):
    audio: Optional[QueryStatusResponseResultAudio] = Field(alias='Audio', default=None)


class QueryStatusResponse(ApiModel):
    #: The unique identifier for the Webex RoomOS Device.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRS8wNTVkYThiNy02NWI2LTQ5NjgtOTg1ZC02ZmFjODcwOWMyMDM
    device_id: Optional[str] = None
    #: xAPI status result
    result: Optional[QueryStatusResponseResult] = None


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


class ExecuteCommandResponse(ApiModel):
    #: The unique identifier for the Webex RoomOS Device.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRS8wNTVkYThiNy02NWI2LTQ5NjgtOTg1ZC02ZmFjODcwOWMyMDM
    device_id: Optional[str] = None
    #: xAPI command arguments
    arguments: Optional[ExecuteCommandArguments] = None
    #: xAPI command results
    result: Optional[ExecuteCommandBody] = None


class XAPIApi(ApiChild, base='xapi'):
    """
    xAPI
    
    The xAPI allows developers to programmatically invoke commands and query the status of devices that run Webex
    RoomOS software.
    
    Executing commands requires an auth token with the `spark:xapi_commands` scope. Querying devices requires an auth
    token with the `spark:xapi_statuses` scope.
    
    All xAPI requests require a `deviceId` which can be obtained using the `Devices API
    <https://developer.webex.com/docs/api/v1/devices>`_. xAPI commands and statuses are
    described in the `Cisco Collaboration Endpoint Software API Reference Guide
    <https://www.cisco.com/c/en/us/support/collaboration-endpoints/spark-room-kit-series/products-command-reference-list.html>`_. For more information about developing
    applications for cloud connected devices, see the `Device Developers Guide
    <https://developer.webex.com/docs/api/guides/device-developers-guide>`_.
    """
    ...