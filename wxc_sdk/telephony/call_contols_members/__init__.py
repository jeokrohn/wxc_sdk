from typing import List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['CallControlsMembersApi']

from wxc_sdk.telephony.calls import CallInfo, TelephonyCall


class CallControlsMembersApi(ApiChild, base='telephony/calls/members'):
    """
    Call Controls Members

    Call Control Members APIs in support of Webex Calling. All `GET` commands require the `spark-admin:calls_read`
    scope while all other commands require the `spark-admin:calls_write` scope.

    **Notes:**

    These APIs support 3rd Party Call Control only.

    The Call Control APIs are only for use by Webex Calling Multi Tenant users and not applicable for users hosted on
    UCM, including Dedicated Instance users.
    """

    def answer(self, member_id: str, call_id: str, endpoint_id: str = None, org_id: str = None):
        """
        Answer by Member ID

        Answer an incoming call. When no endpointId is specified, the call is answered on the user's primary device.
        When an endpointId is specified, the call is answered on the device or application identified by the
        endpointId. The answer API is rejected if the device is not alerting for the call or the device does not
        support answer via API.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        :param endpoint_id: The ID of the device or application to answer the call on. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['callId'] = call_id
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep(f'{member_id}/answer')
        super().post(url, params=params, json=body)

    def list_calls(self, member_id: str, org_id: str = None) -> List[TelephonyCall]:
        """
        List Calls by Member ID

        Get the list of details for all active calls associated with the member.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: list[TelephonyCall]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/calls')
        data = super().get(url, params=params)
        r = TypeAdapter(list[TelephonyCall]).validate_python(data['items'])
        return r

    def get_call_details(self, member_id: str, call_id: str, org_id: str = None) -> TelephonyCall:
        """
        Get Call Details by Member ID

        Get the details of the specified active call for the member.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`TelephonyCall`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/calls/{call_id}')
        data = super().get(url, params=params)
        r = TelephonyCall.model_validate(data)
        return r

    def dial(self, member_id: str, destination: str, endpoint_id: str = None,
                          org_id: str = None) -> CallInfo:
        """
        Dial by Member ID

        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts occur on all the devices belonging to a user unless an optional endpointId is specified
        in which case only the device or application identified by the endpointId is alerted. When a user answers an
        alerting device, an outbound call is placed from that device to the destination.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: `1234`, `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`,
            `user@company.domain`, and `sip:user@company.domain`.
        :type destination: str
        :param endpoint_id: The ID of the device or application to use for the call. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['destination'] = destination
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep(f'{member_id}/dial')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def hangup(self, member_id: str, call_id: str, org_id: str = None):
        """
        Hangup by Member ID

        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['callId'] = call_id
        url = self.ep(f'{member_id}/hangup')
        super().post(url, params=params, json=body)
