import builtins
from typing import Any

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import enum_str
from wxc_sdk.telephony.calls import (
    CallHistoryRecord,
    CallInfo,
    ExternalVoicemailMwiAction,
    HistoryType,
    RejectAction,
    TelephonyCall,
    TelephonyParty,
)

__all__ = ['CallControlsMembersApi']


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

    def barge_in(
        self,
        member_id: str,
        target: str,
        endpoint_id: str = None,
        single_number_reach_phone_number: str = None,
        org_id: str = None,
    ) -> CallInfo:
        """
        Barge In by Member ID

        Barge-in on another user's answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: `1234`, `2223334444`, `+12223334444`, `tel:+12223334444`, `user@company.domain`,
            `sip:user@company.domain`
        :type target: str
        :param endpoint_id: The ID of the device or application to use for the barge-in. The `endpointId` must be one
            of the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
            Mutually exclusive with
            `singleNumberReachPhoneNumber`.
        :type endpoint_id: str
        :param single_number_reach_phone_number: The Single Number Reach phone number to use for the barge-in. Mutually
            exclusive with `endpointId`.
        :type single_number_reach_phone_number: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['target'] = target
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        if single_number_reach_phone_number is not None:
            body['singleNumberReachPhoneNumber'] = single_number_reach_phone_number
        url = self.ep(f'{member_id}/bargeIn')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def list_calls(self, member_id: str, org_id: str = None) -> list[TelephonyCall]:
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

    def dial(
        self,
        member_id: str,
        destination: str,
        endpoint_id: str = None,
        single_number_reach_phone_number: str = None,
        org_id: str = None,
    ) -> CallInfo:
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
            Mutually exclusive with
            `singleNumberReachPhoneNumber`.
        :type endpoint_id: str
        :param single_number_reach_phone_number: The Single Number Reach phone number to use for the call. Mutually
            exclusive with `endpointId`.
        :type single_number_reach_phone_number: str
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
        if single_number_reach_phone_number is not None:
            body['singleNumberReachPhoneNumber'] = single_number_reach_phone_number
        url = self.ep(f'{member_id}/dial')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def divert(
        self, member_id: str, call_id: str, destination: str = None, to_voicemail: bool = None, org_id: str = None
    ) -> None:
        """
        Divert by Member ID

        Divert a call to a destination or a user's voicemail. This is also commonly referred to as a Blind Transfer.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required.
            The destination can be digits or a URI. Some examples for destination include: `1234`, `2223334444`,
            `+12223334444`, `*73`, `tel:+12223334444`, `user@company.domain`, `sip:user@company.domain`
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the
            call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the
            specified user's voicemail.
        :type to_voicemail: bool
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if to_voicemail is not None:
            body['toVoicemail'] = to_voicemail
        url = self.ep(f'{member_id}/divert')
        super().post(url, params=params, json=body)

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

    def call_history(
        self, member_id: str, type_: HistoryType = None, org_id: str = None
    ) -> builtins.list[CallHistoryRecord]:
        """
        List Call History by Member ID

        Get the list of call history records for the user. A maximum of 20 call history records per type (`placed`,
        `missed`, `received`) are returned.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param type_: The type of call history records to retrieve. If not specified, then all call history records are
            retrieved.
        :type type_: HistoryType
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: list[CallHistoryRecord]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if type_ is not None:
            params['type'] = enum_str(type_)
        url = self.ep(f'{member_id}/history')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CallHistoryRecord]).validate_python(data['items'])
        return r

    def hold(self, member_id: str, call_id: str, org_id: str = None) -> None:
        """
        Hold by Member ID

        Hold a connected call.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        url = self.ep(f'{member_id}/hold')
        super().post(url, params=params, json=body)

    def mute(self, member_id: str, call_id: str, org_id: str = None) -> None:
        """
        Mute by Member ID

        Mute a call. This API can only be used for a call that reports itself as mute capable via the muteCapable field
        in the call details.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to mute.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        url = self.ep(f'{member_id}/mute')
        super().post(url, params=params, json=body)

    def park(
        self, member_id: str, call_id: str, destination: str = None, is_group_park: bool = None, org_id: str = None
    ) -> TelephonyParty:
        """
        Park by Member ID

        Park a connected call. The number field in the response can be used as the destination for the retrieve command
        to retrieve the parked call.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifes where the call is to be parked. If not provided, the call is parked against the
            parking user. The destination can be digits or a URI. Some examples for destination include: `1234`,
            `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`, `user@company.domain`, `sip:user@company.domain`
        :type destination: str
        :param is_group_park: If set to`true`, the call is parked against an automatically selected member of the
            user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: TelephonyParty
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if is_group_park is not None:
            body['isGroupPark'] = is_group_park
        url = self.ep(f'{member_id}/park')
        data = super().post(url, params=params, json=body)
        r = TelephonyParty.model_validate(data['parkedAgainst'])
        return r

    def pause_recording(self, member_id: str, call_id: str = None, org_id: str = None) -> None:
        """
        Pause Recording by Member ID

        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep(f'{member_id}/pauseRecording')
        super().post(url, params=params, json=body)

    def pickup(
        self,
        member_id: str,
        target: str = None,
        endpoint_id: str = None,
        single_number_reach_phone_number: str = None,
        org_id: str = None,
    ) -> CallInfo:
        """
        Pickup by Member ID

        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner to
        the dial command. When target is not present, the API pickups up a call from the user's call pickup group.
        When target is present, the API pickups an incoming call from the specified target user.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user's call pickup group is picked up. The target can be digits or a URI. Some examples for target
            include: `1234`, `2223334444`, `+12223334444`, `tel:+12223334444`, `user@company.domain`,
            `sip:user@company.domain`
        :type target: str
        :param endpoint_id: The ID of the device or application to use for the pickup. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
            Mutually exclusive with
            `singleNumberReachPhoneNumber`.
        :type endpoint_id: str
        :param single_number_reach_phone_number: The Single Number Reach phone number to use for the pickup. Mutually
            exclusive with `endpointId`.
        :type single_number_reach_phone_number: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if target is not None:
            body['target'] = target
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        if single_number_reach_phone_number is not None:
            body['singleNumberReachPhoneNumber'] = single_number_reach_phone_number
        url = self.ep(f'{member_id}/pickup')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def pull(self, member_id: str, endpoint_id: str = None, org_id: str = None) -> CallInfo:
        """
        Pull by Member ID

        Pull a call from one device to another. A temporary new call is initiated to perform the call pull in a similar
        manner to the dial command. When a user answers an alerting device, the device is connected to the pulled call
        and the new call created for the call pull is released.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param endpoint_id: The ID of the device or application to use for the retrieval. The `endpointId` must be one
            of the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep(f'{member_id}/pull')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def push(self, member_id: str, call_id: str = None, org_id: str = None) -> None:
        """
        Push by Member ID

        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant's call is associated with an executive.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to push.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep(f'{member_id}/push')
        super().post(url, params=params, json=body)

    def reject(self, member_id: str, call_id: str, action: RejectAction = None, org_id: str = None) -> None:
        """
        Reject by Member ID

        Reject an unanswered incoming call.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        :type action: RejectAction
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        if action is not None:
            body['action'] = enum_str(action)
        url = self.ep(f'{member_id}/reject')
        super().post(url, params=params, json=body)

    def resume(self, member_id: str, call_id: str, org_id: str = None) -> None:
        """
        Resume by Member ID

        Resume a held call.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        url = self.ep(f'{member_id}/resume')
        super().post(url, params=params, json=body)

    def resume_recording(self, member_id: str, call_id: str = None, org_id: str = None) -> None:
        """
        Resume Recording by Member ID

        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep(f'{member_id}/resumeRecording')
        super().post(url, params=params, json=body)

    def retrieve(
        self,
        member_id: str,
        destination: str = None,
        endpoint_id: str = None,
        single_number_reach_phone_number: str = None,
        org_id: str = None,
    ) -> CallInfo:
        """
        Retrieve by Member ID

        Retrieve a parked call. A new call is initiated to perform the retrieval in a similar manner to the dial
        command. The number field from the park command response can be used as the destination for the retrieve
        command.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param destination: Identifies where the call is parked. The number field from the park command response can be
            used as the destination for the retrieve command. If not provided, the call parked against the retrieving
            user is retrieved. The destination can be digits or a URI. Some examples for destination include: `1234`,
            `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`, `user@company.domain`, `sip:user@company.domain`
        :type destination: str
        :param endpoint_id: The ID of the device or application to use for the retrieval. The `endpointId` must be one
            of the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
            Mutually exclusive with
            `singleNumberReachPhoneNumber`.
        :type endpoint_id: str
        :param single_number_reach_phone_number: The Single Number Reach phone number to use for the retrieval.
            Mutually exclusive with `endpointId`.
        :type single_number_reach_phone_number: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if destination is not None:
            body['destination'] = destination
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        if single_number_reach_phone_number is not None:
            body['singleNumberReachPhoneNumber'] = single_number_reach_phone_number
        url = self.ep(f'{member_id}/retrieve')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def start_recording(self, member_id: str, call_id: str = None, org_id: str = None) -> None:
        """
        Start Recording by Member ID

        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On
        Demand".

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep(f'{member_id}/startRecording')
        super().post(url, params=params, json=body)

    def stop_recording(self, member_id: str, call_id: str = None, org_id: str = None) -> None:
        """
        Stop Recording by Member ID

        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep(f'{member_id}/stopRecording')
        super().post(url, params=params, json=body)

    def transfer(
        self, member_id: str, call_id1: str = None, call_id2: str = None, destination: str = None, org_id: str = None
    ) -> CallInfo:
        """
        Transfer by Member ID

        Transfer two calls together.

        Unanswered incoming calls cannot be transferred but can be diverted using the divert API.

        If the user has only two calls and wants to transfer them together, the `callId1` and `callId2` parameters are
        optional and when not provided the calls are automatically selected and transferred.

        If the user has more than two calls and wants to transfer two of them together, the `callId1` and `callId2`
        parameters are mandatory to specify which calls are being transferred. Those are also commonly referred to as
        Attended Transfer, Consultative Transfer, or Supervised Transfer and will return a `204` response.

        If the user wants to transfer one call to a new destination but only when the destination responds, the
        `callId1` and destination parameters are mandatory to specify the call being transferred and the destination.

        This is referred to as a Mute Transfer and is similar to the divert API with the difference of waiting for the
        destination to respond prior to transferring the call. If the destination does not respond, the call is not
        transferred. This will return a `201` response.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either
            `callId2` or `destination` is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the second call to transfer. This parameter is mandatory if `callId1`
            is provided and `destination` is not provided.
        :type call_id2: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some examples
            for destination include: `1234`, `2223334444`, `+12223334444`, `tel:+12223334444`, `user@company.domain`,
            `sip:user@company.domain`. This parameter is mandatory if `callId1` is provided and `callId2` is not
            provided.
        :type destination: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`CallInfo`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id1 is not None:
            body['callId1'] = call_id1
        if call_id2 is not None:
            body['callId2'] = call_id2
        if destination is not None:
            body['destination'] = destination
        url = self.ep(f'{member_id}/transfer')
        data = super().post(url, params=params, json=body)
        r = CallInfo.model_validate(data)
        return r

    def transmit_dtmf(self, member_id: str, call_id: str = None, dtmf: str = None, org_id: str = None) -> None:
        """
        Transmit DTMF by Member ID

        Transmit DTMF digits to a call.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to transmit DTMF digits for.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: `[0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, *, #, A, B, C, D]`. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        :type dtmf: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if call_id is not None:
            body['callId'] = call_id
        if dtmf is not None:
            body['dtmf'] = dtmf
        url = self.ep(f'{member_id}/transmitDtmf')
        super().post(url, params=params, json=body)

    def unmute(self, member_id: str, call_id: str, org_id: str = None) -> None:
        """
        Unmute by Member ID

        Unmute a call. This API can only be used for a call that reports itself as mute capable via the muteCapable
        field in the call details.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param call_id: The call identifier of the call to unmute.
        :type call_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['callId'] = call_id
        url = self.ep(f'{member_id}/unmute')
        super().post(url, params=params, json=body)

    def set_wrapup_reasons(self, member_id: str, wrapup_reasons: list[str] = None, org_id: str = None) -> None:
        """
        Set Wrap-up Reasons by Member ID

        Sets wrap-up reasons for the specified member's last completed call. This API is for admins/service apps to
        perform actions on behalf of a user. The request must provide wrapupReasons.

        :param member_id: Unique identifier for the member.
        :type member_id: str
        :param wrapup_reasons: Array of wrap-up reason names to apply to the agent's last completed call.
        :type wrapup_reasons: list[str]
        :param org_id: Organization ID.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if wrapup_reasons is not None:
            body['wrapupReasons'] = wrapup_reasons
        url = self.ep(f'{member_id}/wrapupreasons')
        super().post(url, params=params, json=body)

    def update_external_voicemail_mwi(
        self, member_id: str, action: ExternalVoicemailMwiAction, org_id: str = None
    ) -> None:
        """
        Set or Clear Message Waiting Indicator (MWI) Status by Member ID

        Enables an external voicemail service to SET or CLEAR the Message Waiting Indicator (MWI) for a person or
        workspace.

        Invoke the API using a bearer token from a Service App in the target organization, created by a full admin with
        the scope `spark-admin:calls_write`.

        Specify the target user or workspace with the required `id` query parameter.

        Optionally, use the orgId parameter to indicate the organization; if omitted, the Service App's organization is
        used.

        If `orgId` is provided, it must match the Service App's organization or be a managed organization.

        Set the desired action (SET or CLEAR) in the message body's action field.

        Learn more about `using Webex Service Apps
        <https://developer.webex.com/messaging/docs/service-apps>`_.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            or virtual line
        :type member_id: str
        :param action: Indicates whether to SET or CLEAR the MWI status.
        :type action: ExternalVoicemailMwiAction
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['action'] = enum_str(action)
        url = self.session.ep(f'telephony/externalVoicemail/members/{member_id}/mwi')
        super().post(url, params=params, json=body)
