from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any, List

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Call', 'CallControlsMembersApi', 'CallPersonalityEnum', 'CallStateEnum', 'CallTypeEnum',
           'DialByMemberIdResponse', 'PartyInformation', 'RecallInformation', 'RecallTypeEnum', 'RecordingStateEnum',
           'RedirectionInformation', 'RedirectionReasonEnum']


class CallPersonalityEnum(str, Enum):
    #: An outgoing call originated by the user.
    originator = 'originator'
    #: An incoming call received by the user.
    terminator = 'terminator'
    #: A call that is alerting the user's devices for a Click to Dial action. When the user answers on one of these
    #: alerting devices, the call's personality is updated to originator.
    click_to_dial = 'clickToDial'


class CallStateEnum(str, Enum):
    #: The remote party is being alerted.
    connecting = 'connecting'
    #: The user's devices are alerting for the incoming or Click to Dial call.
    alerting = 'alerting'
    #: The call is connected.
    connected = 'connected'
    #: The user has placed the call on hold.
    held = 'held'
    #: The remote party within the same organization has placed the call on hold.
    remote_held = 'remoteHeld'
    #: The call has been disconnected.
    disconnected = 'disconnected'


class CallTypeEnum(str, Enum):
    #: The party is within the same location.
    location = 'location'
    #: The party is within the same organization but not within the same location.
    organization = 'organization'
    #: The party is outside the organization.
    external = 'external'
    #: The party is an emergency call destination.
    emergency = 'emergency'
    #: The party is a repair call destination.
    repair = 'repair'
    #: The party does not belong to one of the defined call types. For example, a call to a Call Forwarding Always
    #: feature activation code.
    other = 'other'


class PartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`,
    #: `user@company.domain`
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str] = None
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool] = None
    #: The call type for the party.
    call_type: Optional[CallTypeEnum] = None


class RedirectionReasonEnum(str, Enum):
    #: The call was redirected on a busy condition. For example, the call was forwarded by Call Forwarding Busy.
    busy = 'busy'
    #: The call was redirected on a no answer condition. For example, the call was forwarded by Call Forwarding No
    #: Answer.
    no_answer = 'noAnswer'
    #: The call was redirected on an unavailable condition. For example, the call was forwarded by Business Continuity.
    unavailable = 'unavailable'
    #: The call was redirected unconditionally. For example, the call was forwarded by Call Forwarding Always.
    unconditional = 'unconditional'
    #: The call was redirected by a service schedule. For example, the call was forwarded by Selective Call Forwarding.
    time_of_day = 'timeOfDay'
    #: The call was redirected by divert action.
    divert = 'divert'
    #: The call was redirected by a follow me service. For example, the call was redirected by Simultaneous Ring.
    follow_me = 'followMe'
    #: The call was redirected by Hunt Group routing.
    hunt_group = 'huntGroup'
    #: The call was redirected by Call Queue routing.
    call_queue = 'callQueue'
    #: The call was redirected on an unknown condition.
    unknown = 'unknown'


class RedirectionInformation(ApiModel):
    #: The reason the incoming call was redirected.
    reason: Optional[RedirectionReasonEnum] = None
    #: The details of a party who redirected the incoming call.
    redirecting_party: Optional[PartyInformation] = None


class RecallTypeEnum(str, Enum):
    #: The user is being recalled for a call park they initiated.
    park = 'park'


class RecallInformation(ApiModel):
    #: The type of recall the incoming call is for. Park is the only type of recall currently supported but additional
    #: values may be added in the future.
    type: Optional[RecallTypeEnum] = None
    #: If the type is park, contains the details of where the call was parked. For example, if user A parks a call
    #: against user B and A is recalled for the park, then this field contains B's information in A's incoming call
    #: details. Only present when the type is park.
    party: Optional[PartyInformation] = None


class RecordingStateEnum(str, Enum):
    #: Recording has been requested for the call but has not yet started.
    pending = 'pending'
    #: Recording is active for the call.
    started = 'started'
    #: Recording has been paused for the call.
    paused = 'paused'
    #: Recording has been stopped for the call.
    stopped = 'stopped'
    #: Recording failed for the call.
    failed = 'failed'


class Call(ApiModel):
    #: The call identifier of the call.
    id: Optional[str] = None
    #: The call session identifier of the call session the call belongs to. This can be used to correlate multiple
    #: calls that are part of the same call session.
    call_session_id: Optional[str] = None
    #: The personality of the call.
    personality: Optional[CallPersonalityEnum] = None
    #: The current state of the call.
    state: Optional[CallStateEnum] = None
    #: The remote party's details. For example, if user A calls user B then B is the remote party in A's outgoing call
    #: details and A is the remote party in B's incoming call details.
    remote_party: Optional[PartyInformation] = None
    #: The appearance value for the call. The appearance value can be used to display the user's calls in an order
    #: consistent with the user's devices. Only present when the call has an appearance value assigned.
    appearance: Optional[int] = None
    #: The date and time the call was created.
    created: Optional[datetime] = None
    #: The date and time the call was answered. Only present when the call has been answered.
    answered: Optional[datetime] = None
    #: The list of details for previous redirections of the incoming call ordered from most recent to least recent. For
    #: example, if user B forwards an incoming call to user C, then a redirection entry is present for B's forwarding
    #: in C's incoming call details. Only present when there were previous redirections and the incoming call's state
    #: is alerting.
    redirections: Optional[list[RedirectionInformation]] = None
    #: The recall details for the incoming call. Only present when the incoming call is for a recall.
    recall: Optional[RecallInformation] = None
    #: The call's current recording state. Only present when the user's call recording has been invoked during the life
    #: of the call.
    recording_state: Optional[RecordingStateEnum] = None
    #: Indicates whether the call is capable of using the `mute
    #: <https://developer.webex.com/docs/api/v1/call-controls/mute>`_ and `unmute
    mute_capable: Optional[bool] = None
    #: Indicates whether the call is currently muted.
    muted: Optional[bool] = None


class DialByMemberIdResponse(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for the same call.
    call_id: Optional[str] = None
    #: A unique identifier for the call session the call belongs to. This can be used to correlate multiple calls that
    #: are part of the same call session.
    call_session_id: Optional[str] = None


class CallControlsMembersApi(ApiChild, base='telephony/calls/members'):
    """
    Call Controls Members
    
    Call Control Members APIs in support of Webex Calling. All `GET` commands require the `spark-admin:calls_read`
    scope while all other commands require the `spark-admin:calls_write` scope.
    
    **Notes:**
    
    - These APIs support 3rd Party Call Control only.
    
    - The Call Control APIs are only for use by Webex Calling Multi Tenant users and not applicable for users hosted on
    UCM, including Dedicated Instance users.
    """

    def answer_by_member_id(self, member_id: str, call_id: str, endpoint_id: str = None, org_id: str = None):
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

    def list_calls_by_member_id(self, member_id: str, org_id: str = None) -> List[Call]:
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
        :rtype: list[Call]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/calls')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Call]).validate_python(data['items'])
        return r

    def get_call_details_by_member_id(self, member_id: str, call_id: str, org_id: str = None) -> Call:
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
        :rtype: :class:`Call`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/calls/{call_id}')
        data = super().get(url, params=params)
        r = Call.model_validate(data)
        return r

    def dial_by_member_id(self, member_id: str, destination: str, endpoint_id: str = None,
                          org_id: str = None) -> DialByMemberIdResponse:
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
        :rtype: :class:`DialByMemberIdResponse`
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
        r = DialByMemberIdResponse.model_validate(data)
        return r

    def hangup_by_member_id(self, member_id: str, call_id: str, org_id: str = None):
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
