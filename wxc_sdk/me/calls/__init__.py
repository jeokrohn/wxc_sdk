import builtins
from typing import Any

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.telephony.calls import CallInfo, TelephonyCall

__all__ = ['MeCallControlApi']


class MeCallControlApi(ApiChild, base='telephony/calls/members/me'):
    """
    Call Controls Members Me

    Call Control Me APIs in support of Webex Calling. All `GET` commands require the `spark:calls_read` scope while all
    other commands require the `spark:calls_write` scope.

    **Notes:**

    - These APIs support 3rd Party Call Control only.

    - The Call Control APIs are only for use by Webex Calling Multi Tenant users and not applicable for users hosted on
    UCM, including Dedicated Instance users.

    - The Call Control APIs are not supported by Service Apps. Please see Call Control Members APIs for Service Apps
    support.
    """

    def answer(self, call_id: str, endpoint_id: str = None, line_owner_id: str = None) -> None:
        """
        Answer

        Answer an incoming call. When no endpointId is specified, the call is answered on the user's primary device.
        When an endpointId is specified, the call is answered on the device or application identified by the
        endpointId. The answer API is rejected if the device is not alerting for the call or the device does not
        support answer via API.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        :param endpoint_id: The ID of the device or application to answer the call on. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :param line_owner_id: The ID of a user, workspace, or virtual line for which there is a secondary line on a
            device owned by the user invoking the API.
        :type line_owner_id: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('answer')
        super().post(url, json=body)

    def list_calls(self, line_owner_id: str = None) -> builtins.list[TelephonyCall]:
        """
        List Calls

        Get the list of details for all active calls associated with the user.

        :param line_owner_id: The ID of a user, workspace, or virtual line for which there is a secondary line on a
            device owned by the user invoking the API.
        :type line_owner_id: str
        :rtype: list[TelephonyCall]
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep('calls')
        data = super().get(url, params=params)
        r = TypeAdapter(list[TelephonyCall]).validate_python(data['items'])
        return r

    def call_details(self, call_id: str, line_owner_id: str = None) -> TelephonyCall:
        """
        Get Call Details

        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        :param line_owner_id: The ID of a user, workspace, or virtual line for which there is a secondary line on a
            device owned by the user invoking the API.
        :type line_owner_id: str
        :rtype: :class:`TelephonyCall`
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep(f'calls/{call_id}')
        data = super().get(url, params=params)
        r = TelephonyCall.model_validate(data)
        return r

    def dial(
        self,
        destination: str,
        endpoint_id: str = None,
        single_number_reach_phone_number: str = None,
        line_owner_id: str = None,
    ) -> CallInfo:
        """
        Dial

        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts occur on all the devices belonging to a user unless an optional endpointId is specified
        in which case only the device or application identified by the endpointId is alerted. When a user answers an
        alerting device, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: `1234`, `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`,
            `user@company.domain`, and `sip:user@company.domain`.
        :type destination: str
        :param endpoint_id: The ID of the device or application to use for the call. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
            Mutually exclusive with
            `singleNumberReachPhoneNumber`.
        :type endpoint_id: str
        :param single_number_reach_phone_number: The Single Number Reach phone number to use for the call. Mutually
            exclusive with `endpointId`.
        :type single_number_reach_phone_number: str
        :param line_owner_id: The ID of a user, workspace, or virtual line for which there is a secondary line on a
            device owned by the user invoking the API.
        :type line_owner_id: str
        :rtype: :class:`CallInfo`
        """
        body: dict[str, Any] = dict()
        body['destination'] = destination
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        if single_number_reach_phone_number is not None:
            body['singleNumberReachPhoneNumber'] = single_number_reach_phone_number
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('dial')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def hangup(self, call_id: str, line_owner_id: str = None) -> None:
        """
        Hangup

        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        :param line_owner_id: The ID of a user, workspace, or virtual line for which there is a secondary line on a
            device owned by the user invoking the API.
        :type line_owner_id: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('hangup')
        super().post(url, json=body)
