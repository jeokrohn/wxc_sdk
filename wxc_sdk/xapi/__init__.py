from typing import Optional, Union

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['ExecuteCommandResponse', 'QueryStatusResponse', 'XApi']


class QueryStatusResponse(ApiModel):
    #: The unique identifier for the Webex RoomOS Device.
    device_id: Optional[str] = None
    #: xAPI status result
    result: Optional[dict] = None


class ExecuteCommandResponse(ApiModel):
    #: The unique identifier for the Webex RoomOS Device.
    device_id: Optional[str] = None
    #: xAPI command arguments
    arguments: Optional[dict] = None
    #: xAPI command results
    result: Optional[dict] = None


class XApi(ApiChild, base='xapi'):
    """
    xAPI

    The xAPI allows developers to programmatically invoke commands and query the status of devices that run Webex
    RoomOS software.

    Executing commands requires an auth token with the `spark:xapi_commands` scope. Querying devices requires an auth
    token with the `spark:xapi_statuses` scope.

    All xAPI requests require a `deviceId` which can be obtained using the `Devices API
    <https://developer.webex.com/docs/api/v1/devices>`_. xAPI commands and statuses are
    described in the `Cisco Collaboration Endpoint Software API Reference Guide
    <https://www.cisco.com/c/en/us/support/collaboration-endpoints/spark-room-kit-series/products-command-reference
    -list.html>`_. For more information about developing
    applications for cloud connected devices, see the `Device Developers Guide
    <https://developer.webex.com/docs/api/guides/device-developers-guide>`_.
    """

    def query_status(self, device_id: str, name: list[str]) -> QueryStatusResponse:
        """
        Query Status

        Query the current status of the Webex RoomOS Device. You specify the target device in the `deviceId` parameter
        in the URI. The target device is queried for statuses according to the expression in the `name` parameter.

        See the `xAPI section of the Device Developers Guide
        <https://developer.webex.com/docs/api/guides/device-developers-guide#xapi>`_ for a description of status
        expressions.

        :param device_id: The unique identifier for the Webex RoomOS Device.
        :type device_id: str
        :param name: A list of status expressions used to query the Webex RoomOS Device. See the
            `xAPI section of the Device Developers Guide
            <https://developer.webex.com/docs/api/guides/device-developers-guide#xapi>`_ for a description of status
            expressions. A request can contain
            at most 10 different status expressions.
        :type name: list[str]
        """
        params = {}
        params['deviceId'] = device_id
        params['name'] = ','.join(name)
        url = self.ep('status')
        data = super().get(url, params=params)
        r = QueryStatusResponse.model_validate(data)
        return r

    def execute_command(self, command_name: str, device_id: str, arguments: dict = None,
                        body: Union[dict, str] = None) -> ExecuteCommandResponse:
        """
        Execute Command

        Executes a command on the Webex RoomOS Device. Specify the command to execute in the `commandName` URI
        parameter.

        See the `xAPI section of the Device Developers Guide <https://developer.webex.com/docs/devices#xapi>`_ for a
        description of command expressions.

        :param command_name: Command to execute on the Webex RoomOS Device.
        :type command_name: str
        :param device_id: The unique identifier for the Webex RoomOS Device.
        :type device_id: str
        :param arguments: xAPI command arguments
        :type arguments: dict
        :param body: xAPI command body, as a complex JSON object or as a string
        :type body: ExecuteCommandBody
        :rtype: :class:`ExecuteCommandResponse`
        """
        json_body = dict()
        json_body['deviceId'] = device_id
        if arguments is not None:
            json_body['arguments'] = arguments
        if body is not None:
            json_body['body'] = body
        url = self.ep(f'command/{command_name}')
        data = super().post(url, json=json_body)
        r = ExecuteCommandResponse.model_validate(data)
        return r

    def system_unit_boot(self, device_id: str, force: bool = False) -> ExecuteCommandResponse:
        """
        Reboot the device

        :param device_id: The unique identifier for the Webex RoomOS Device.
        :type device_id: str
        :param force: If True, the device will be rebooted immediately. If False, the device will wait for a period of time before rebooting.
        :type force: bool
        """
        return self.execute_command('SystemUnit.Boot', device_id, arguments={'Force': str(force)})
