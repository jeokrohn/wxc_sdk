from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ExecuteCommandArguments', 'ExecuteCommandBody', 'ExecuteCommandBodyBooking',
           'ExecuteCommandBodyBookingOrganizer', 'ExecuteCommandBodyBookingTime', 'ExecuteCommandResponse',
           'QueryStatusResponse', 'QueryStatusResponseResult', 'QueryStatusResponseResultAudio', 'XAPIApi']


class QueryStatusResponseResultAudio(ApiModel):
    #: example: 75
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
    #: example: 50
    level: Optional[int] = Field(alias='Level', default=None)


class ExecuteCommandBodyBookingTime(ApiModel):
    #: example: 2020-07-01T13:00:00Z
    start_time: Optional[datetime] = Field(alias='StartTime', default=None)
    #: example: 60
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

    def query_status(self, device_id: str, name: str) -> QueryStatusResponse:
        """
        Query Status

        Query the current status of the Webex RoomOS Device. You specify the target device in the `deviceId` parameter
        in the URI. The target device is queried for statuses according to the expression in the `name` parameter.

        See the `xAPI section of the Device Developers Guide
        <https://developer.webex.com/docs/api/guides/device-developers-guide#xapi>`_ for a description of status expressions.

        :param device_id: The unique identifier for the Webex RoomOS Device.
        :type device_id: str
        :param name: Status expression used to query the Webex RoomOS Device. See the
            `xAPI section of the Device Developers Guide
            <https://developer.webex.com/docs/api/guides/device-developers-guide#xapi>`_ for a description of status expressions.
        :type name: str
        :rtype: :class:`QueryStatusResponse`
        """
        params = {}
        params['deviceId'] = device_id
        params['name'] = name
        url = self.ep('status')
        data = super().get(url, params=params)
        r = QueryStatusResponse.model_validate(data)
        return r

    def execute_command(self, command_name: str, device_id: str, arguments: ExecuteCommandArguments,
                        body: ExecuteCommandBody = None) -> ExecuteCommandResponse:
        """
        Execute Command

        Executes a command on the Webex RoomOS Device. Specify the command to execute in the `commandName` URI
        parameter.

        See the `xAPI section of the Device Developers Guide
        <https://developer.webex.com/docs/devices#xapi>`_ for a description of command expressions.

        :param command_name: Command to execute on the Webex RoomOS Device.
        :type command_name: str
        :param device_id: The unique identifier for the Webex RoomOS Device.
        :type device_id: str
        :param arguments: xAPI command arguments
        :type arguments: ExecuteCommandArguments
        :param body: xAPI command body, as a complex JSON object or as a string, for example: `import xapi from
            'xapi';\n\nconsole.log('Hello, World!');\n`
        :type body: ExecuteCommandBody
        :rtype: :class:`ExecuteCommandResponse`
        """
        body = dict()
        body['deviceId'] = device_id
        body['arguments'] = arguments.model_dump(mode='json', by_alias=True, exclude_none=True)
        if body is not None:
            body['body'] = body.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'command/{command_name}')
        data = super().post(url, json=body)
        r = ExecuteCommandResponse.model_validate(data)
        return r
