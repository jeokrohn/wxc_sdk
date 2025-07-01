"""
Webex Calling Call Control API and related data types
"""
import datetime
from typing import Optional

from pydantic import Field, TypeAdapter

from ..api_child import ApiChild
from ..base import ApiModel, enum_str
from ..base import SafeEnum as Enum
from ..webhook import WebhookEvent, WebhookEventData

__all__ = ['CallType', 'TelephonyParty', 'RedirectReason', 'Redirection', 'Recall', 'RecordingState',
           'Personality', 'CallState', 'TelephonyCall', 'TelephonyEventData', 'TelephonyEvent', 'DialResponse',
           'RejectAction', 'HistoryType', 'CallHistoryRecord', 'CallInfo', 'CallsApi', 'RecallType']


class RejectAction(str, Enum):
    #: Send the call to busy.
    busy = 'busy'
    #: Send the call to temporarily unavailable.
    temporarily_unavailable = 'temporarilyUnavailable'
    #: Ignore the call by continuing ringback to the caller while no longer alerting the called user's devices.
    ignore = 'ignore'


class Personality(str, Enum):
    #: An outgoing call originated by the user.
    originator = 'originator'
    #: An incoming call received by the user.
    terminator = 'terminator'
    #: A call that is alerting the user's devices for a Click to Dial action. When the user answers on one of these
    #: alerting devices, the call's personality is updated to originator.
    click_to_dial = 'clickToDial'


class CallState(str, Enum):
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


class CallType(str, Enum):
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


class TelephonyParty(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, \*73, user@company.domain
    number: str
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str] = None
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool] = None
    #: The call type for the party.
    call_type: Optional[CallType] = None


class RedirectReason(str, Enum):
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


class Redirection(ApiModel):
    #: The reason the incoming call was redirected.
    reason: Optional[RedirectReason] = None
    #: The details of a party who redirected the incoming call.
    redirecting_party: Optional[TelephonyParty] = None


class RecallType(str, Enum):
    #: The user is being recalled for a call park they initiated.
    park = 'park'


class Recall(ApiModel):
    """
    call recall
    """
    #: The type of recall the incoming call is for. Park is the only type of recall currently supported but additional
    #: values may be added in the future.
    recall_type: RecallType = Field(alias='type')
    #: If the type is park, contains the details of where the call was parked. For example, if user A parks a call
    #: against user B and A is recalled for the park, then this field contains B's information in A's incoming call
    #: details. Only present when the type is park.
    party: TelephonyParty


class RecordingState(str, Enum):
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


class TelephonyCall(ApiModel):
    # In events the property is "callId"
    id_call_id: Optional[str] = Field(alias='callId', default=None)
    # ..while the telephony API uses "id"
    id_id: Optional[str] = Field(alias='id', default=None)

    # .. but this should handle that
    @property
    def call_id(self) -> Optional[str]:
        """
        The call identifier of the call.
        """
        return self.id_id or self.id_call_id

    #: The call session identifier of the call session the call belongs to. This can be used to correlate multiple
    #: calls that are part of the same call session.
    call_session_id: str
    #: The personality of the call.
    personality: Personality
    #: The current state of the call.
    state: CallState
    #: The remote party's details. For example, if user A calls user B then B is the remote party in A's outgoing call
    #: details and A is the remote party in B's incoming call details.
    remote_party: TelephonyParty
    #: The appearance value for the call. The appearance value can be used to display the user's calls in an order
    #: consistent with the user's devices. Only present when the call has an appearance value assigned.
    appearance: Optional[int] = None
    #: The date and time the call was created.
    created: datetime.datetime
    #: The date and time the call was answered. Only present when the call has been answered.
    answered: Optional[datetime.datetime] = None
    #: The list of details for previous redirections of the incoming call ordered from most recent to least recent.
    #: For example, if user B forwards an incoming call to user C, then a redirection entry is present for B's
    #: forwarding in C's incoming call details. Only present when there were previous redirections and the incoming
    #: call's state is alerting.
    redirections: list[Redirection] = Field(default_factory=list)
    #: The recall details for the incoming call. Only present when the incoming call is for a recall.
    recall: Optional[Recall] = None
    #: The call's current recording state. Only present when the user's call recording has been invoked during the
    #: life of the call.
    recording_state: Optional[RecordingState] = None
    #: The date and time the call was disconnected
    disconnected: Optional[datetime.datetime] = None
    #: Indicates whether the call is capable of using the `mute
    #: <https://developer.webex.com/docs/api/v1/call-controls/mute>`_ and `unmute
    mute_capable: Optional[bool] = None
    #: Indicates whether the call is currently muted.
    muted: Optional[bool] = None


class HistoryType(str, Enum):
    #: A call history record for an outgoing call placed by the user.
    placed = 'placed'
    #: A call history record for an incoming call to the user that was not answered.
    missed = 'missed'
    #: A call history record for an incoming call to the user that was answered.
    received = 'received'


class CallHistoryRecord(ApiModel):
    #: The type of call history record.
    call_type: HistoryType = Field(alias='type')
    #: The name of the called/calling party. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The number of the called/calling party. Only present when the number is available and privacy is not enabled.
    #: The number can be digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, \*73,
    #: user@company.domain
    number: Optional[str] = None
    #: Indicates whether privacy is enabled for the name and number.
    privacy_enabled: bool
    #: The date and time the call history record was created. For a placed call history record, this is when the call
    #: was placed. For a missed call history record, this is when the call was disconnected. For a received call
    #: history record, this is when the call was answered.
    time: datetime.datetime


class CallInfo(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for this call.
    call_id: str
    #: A unqiue identifier for the call session the call belongs to. This can be used to correlate multiple calls
    #: that are part of the same call session.
    call_session_id: str


DialResponse = CallInfo


class TelephonyEventData(WebhookEventData, TelephonyCall):
    """
    data in a webhook 'telephony_calls' event
    """
    resource = 'telephony_calls'
    event_type: str
    event_timestamp: datetime.datetime


TelephonyEvent = WebhookEvent


class CallsApi(ApiChild, base='telephony/calls'):
    """
    Call Controls

    Call Control APIs in support of Webex Calling. All `GET` commands require the `spark:calls_read` scope while all
    other commands require the `spark:calls_write` scope.

    **Notes:**

    - These APIs support 3rd Party Call Control only.
    - The Call Control APIs are only for use by Webex Calling Multi Tenant users and not applicable for users hosted on
      UCM, including Dedicated Instance users.
    """

    def list_calls(self) -> list[TelephonyCall]:
        """
        List Calls

        Get the list of details for all active calls associated with the user.

        :rtype: list[Call]
        """
        url = self.ep()
        data = super().get(url)
        r = TypeAdapter(list[TelephonyCall]).validate_python(data['items'])
        return r

    def answer(self, call_id: str, endpoint_id: str = None):
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
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep('answer')
        super().post(url, json=body)

    def barge_in(self, target: str, endpoint_id: str = None) -> CallInfo:
        """
        Barge In

        Barge-in on another user's answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: `1234`, `2223334444`, `+12223334444`, `tel:+12223334444`, `user@company.domain`,
            `sip:user@company.domain`
        :type target: str
        :param endpoint_id: The ID of the device or application to use for the barge-in. The `endpointId` must be one
            of the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :rtype: :class:`CallInfo`
        """
        body = dict()
        body['target'] = target
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep('bargeIn')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def dial(self, destination: str, endpoint_id: str = None) -> CallInfo:
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
        :type endpoint_id: str
        :rtype: :class:`CallInfo`
        """
        body = dict()
        body['destination'] = destination
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep('dial')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert

        Divert a call to a destination or a user's voicemail. This is also commonly referred to as a Blind Transfer.

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
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if to_voicemail is not None:
            body['toVoicemail'] = to_voicemail
        url = self.ep('divert')
        super().post(url, json=body)

    def hangup(self, call_id: str):
        """
        Hangup

        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('hangup')
        super().post(url, json=body)

    def call_history(self, history_type: HistoryType = None) -> list[CallHistoryRecord]:
        """
        List Call History

        Get the list of call history records for the user. A maximum of 20 call history records per type (`placed`,
        `missed`, `received`) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history records are
            retrieved.
        :type history_type: CallHistoryRecordTypeEnum
        :rtype: list[CallHistoryRecord]
        """
        params = {}
        if history_type is not None:
            params['type'] = enum_str(history_type)
        url = self.ep('history')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CallHistoryRecord]).validate_python(data['items'])
        return r

    def hold(self, call_id: str):
        """
        Hold

        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('hold')
        super().post(url, json=body)

    def mute(self, call_id: str):
        """
        Mute

        Mute a call. This API can only be used for a call that reports itself as mute capable via the muteCapable field
        in the call details.

        :param call_id: The call identifier of the call to mute.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('mute')
        super().post(url, json=body)

    def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> TelephonyParty:
        """
        Park

        Park a connected call. The number field in the response can be used as the destination for the retrieve command
        to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifes where the call is to be parked. If not provided, the call is parked against the
            parking user. The destination can be digits or a URI. Some examples for destination include: `1234`,
            `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`, `user@company.domain`, `sip:user@company.domain`
        :type destination: str
        :param is_group_park: If set to`true`, the call is parked against an automatically selected member of the
            user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        :rtype: TelephonyParty
        """
        body = dict()
        body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if is_group_park is not None:
            body['isGroupPark'] = is_group_park
        url = self.ep('park')
        data = super().post(url, json=body)
        r = TelephonyParty.model_validate(data['parkedAgainst'])
        return r

    def pause_recording(self, call_id: str = None):
        """
        Pause Recording

        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('pauseRecording')
        super().post(url, json=body)

    def pickup(self, target: str = None, endpoint_id: str = None) -> CallInfo:
        """
        Pickup

        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner to
        the dial command. When target is not present, the API pickups up a call from the user's call pickup group.
        When target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user's call pickup group is picked up. The target can be digits or a URI. Some examples for target
            include: `1234`, `2223334444`, `+12223334444`, `tel:+12223334444`, `user@company.domain`,
            `sip:user@company.domain`
        :type target: str
        :param endpoint_id: The ID of the device or application to use for the pickup. The `endpointId` must be one of
            the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :rtype: :class:`CallInfo`
        """
        body = dict()
        if target is not None:
            body['target'] = target
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep('pickup')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def push(self, call_id: str = None):
        """
        Push

        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant's call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('push')
        super().post(url, json=body)

    def reject(self, call_id: str, action: RejectAction = None):
        """
        Reject

        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        :type action: RejectAction
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        if action is not None:
            body['action'] = enum_str(action)
        url = self.ep('reject')
        super().post(url, json=body)

    def resume(self, call_id: str):
        """
        Resume

        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('resume')
        super().post(url, json=body)

    def resume_recording(self, call_id: str = None):
        """
        Resume Recording

        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('resumeRecording')
        super().post(url, json=body)

    def retrieve(self, destination: str = None, endpoint_id: str = None) -> CallInfo:
        """
        Retrieve

        Retrieve a parked call. A new call is initiated to perform the retrieval in a similar manner to the dial
        command. The number field from the park command response can be used as the destination for the retrieve
        command.

        :param destination: Identifies where the call is parked. The number field from the park command response can be
            used as the destination for the retrieve command. If not provided, the call parked against the retrieving
            user is retrieved. The destination can be digits or a URI. Some examples for destination include: `1234`,
            `2223334444`, `+12223334444`, `*73`, `tel:+12223334444`, `user@company.domain`, `sip:user@company.domain`
        :type destination: str
        :param endpoint_id: The ID of the device or application to use for the retrieval. The `endpointId` must be one
            of the endpointIds returned by the `Get Preferred Answer Endpoint API
            <https://developer.webex.com/docs/api/v1/user-call-settings-2-2/get-preferred-answer-endpoint>`_.
        :type endpoint_id: str
        :rtype: :class:`CallInfo`
        """
        body = dict()
        if destination is not None:
            body['destination'] = destination
        if endpoint_id is not None:
            body['endpointId'] = endpoint_id
        url = self.ep('retrieve')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def start_recording(self, call_id: str = None):
        """
        Start Recording

        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On
        Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('startRecording')
        super().post(url, json=body)

    def stop_recording(self, call_id: str = None):
        """
        Stop Recording

        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('stopRecording')
        super().post(url, json=body)

    def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None) -> CallInfo:
        """
        Transfer

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
        :rtype: :class:`CallInfo`
        """
        body = dict()
        if call_id1 is not None:
            body['callId1'] = call_id1
        if call_id2 is not None:
            body['callId2'] = call_id2
        if destination is not None:
            body['destination'] = destination
        url = self.ep('transfer')
        data = super().post(url, json=body)
        r = CallInfo.model_validate(data)
        return r

    def transmit_dtmf(self, call_id: str = None, dtmf: str = None):
        """
        Transmit DTMF

        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to transmit DTMF digits for.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: `[0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, *, #, A, B, C, D]`. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        :type dtmf: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        if dtmf is not None:
            body['dtmf'] = dtmf
        url = self.ep('transmitDtmf')
        super().post(url, json=body)

    def unmute(self, call_id: str):
        """
        Unmute

        Unmute a call. This API can only be used for a call that reports itself as mute capable via the muteCapable
        field in the call details.

        :param call_id: The call identifier of the call to unmute.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('unmute')
        super().post(url, json=body)

    def call_details(self, call_id: str) -> TelephonyCall:
        """
        Get Call Details

        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        :rtype: :class:`Call`
        """
        url = self.ep(f'{call_id}')
        data = super().get(url)
        r = TelephonyCall.model_validate(data)
        return r
