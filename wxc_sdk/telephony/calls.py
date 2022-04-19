"""
Webex Calling Call Control API and related data types
"""
import datetime
from collections.abc import Generator
from enum import Enum
from typing import Optional, Literal, Union

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..webhook import WebHook

__all__ = ['CallType', 'TelephonyParty', 'RedirectReason', 'Redirection', 'Recall', 'RecordingState',
           'Personality', 'CallState', 'TelephonyCall', 'TelephonyEventData', 'TelephonyEvent', 'DialResponse',
           'RejectAction',
           'HistoryType', 'CallHistoryRecord', 'ParkedAgainst', 'CallInfo',
           'CallsApi']


class CallType(str, Enum):
    """
    Webex Calling call types
    """
    location = 'location'
    organization = 'organization'
    external = 'external'
    emergency = 'emergency'
    repair = 'repair'
    other = 'other'


class TelephonyParty(ApiModel):
    """
    Representation of a calling/called party of a Webex Calling call
    """
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, \*73, user@company.domain
    number: str
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str]
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str]
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: str
    #: The call type for the party.
    call_type: CallType


class RedirectReason(str, Enum):
    """
    reason for Call redirection
    """
    busy = 'busy'
    noAnswer = 'noAnswer'
    unavailable = 'unavailable'
    unconditional = 'unconditional'
    time_of_day = 'timeOfDay'
    divert = 'divert'
    followMe = 'followMe'
    hunt_group = 'huntGroup'
    call_queue = 'callQueue'
    unknown = 'unknown'


class Redirection(ApiModel):
    """
    Single redirection
    """
    #: The reason the incoming call was redirected.
    reason: RedirectReason
    #: The details of a party who redirected the incoming call.
    redirecting_party: TelephonyParty


class Recall(ApiModel):
    """
    call recall
    """
    #: The type of recall the incoming call is for. Park is the only type of recall currently supported but additional
    #: values may be added in the future.
    recall_type: Literal['park'] = Field(alias='type')
    #: If the type is park, contains the details of where the call was parked. For example, if user A parks a call
    #: against user B and A is recalled for the park, then this field contains B's information in A's incoming call
    #: details. Only present when the type is park.
    party: TelephonyParty


class RecordingState(str, Enum):
    """
    recording state of a Webex Calling call
    """
    pending = 'pending'
    started = 'started'
    paused = 'paused'
    stopped = 'stopped'
    failed = 'failed'


class Personality(str, Enum):
    """
    Roles of an entity in a Webex Calling call
    """
    originator = 'originator'
    terminator = 'terminator'
    click_to_dial = 'clickToDial'


class CallState(str, Enum):
    connecting = 'connecting'
    alerting = 'alerting'
    connected = 'connected'
    held = 'held'
    remoteHeld = 'remoteHeld'
    disconnected = 'disconnected'


class TelephonyCall(ApiModel):
    """
    Representation of a Webex Calling call
    """
    # In events the property is "callId"
    id_call_id: Optional[str] = Field(alias='callId')
    # ..while the telephony API uses "id"
    id_id: Optional[str] = Field(alias='id')

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
    appearance: Optional[int]
    #: The date and time the call was created.
    created: datetime.datetime
    #: The date and time the call was answered. Only present when the call has been answered.
    answered: Optional[datetime.datetime]
    #: The list of details for previous redirections of the incoming call ordered from most recent to least recent.
    #: For example, if user B forwards an incoming call to user C, then a redirection entry is present for B's
    #: forwarding in C's incoming call details. Only present when there were previous redirections and the incoming
    #: call's state is alerting.
    redirections: list[Redirection] = Field(default_factory=list)
    #: The recall details for the incoming call. Only present when the incoming call is for a recall.
    recall: Optional[Recall]
    #: The call's current recording state. Only present when the user's call recording has been invoked during the
    #: life of the call.
    recording_state: Optional[RecordingState]
    #: The date and time the call was disconnected
    disconnected: Optional[datetime.datetime]


class TelephonyEventData(TelephonyCall):
    event_type: str
    event_timestamp: datetime.datetime


class TelephonyEvent(WebHook):
    """
    A telephony event on the webhook
    """
    resource: Literal['telephony_calls']
    actor_id: str
    data: TelephonyEventData


class DialResponse(ApiModel):
    """
    Result of call initiation using the dial() method
    """
    call_id: str
    call_session_id: str


class RejectAction(str, Enum):
    """
    The rejection action to apply to the call
    """
    busy = 'busy'
    temporarily_unavailable = 'temporarilyUnavailable'
    ignore = 'ignore'


class HistoryType(str, Enum):
    placed = 'placed'
    missed = 'missed'
    received = 'received'

    @staticmethod
    def history_type_or_str(v: Union[str, 'HistoryType']) -> 'HistoryType':
        if isinstance(v, HistoryType):
            return v
        return HistoryType(v)


class CallHistoryRecord(ApiModel):
    #: The type of call history record.
    call_type: HistoryType = Field(alias='type')
    #: The name of the called/calling party. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The number of the called/calling party. Only present when the number is available and privacy is not enabled.
    #: The number can be digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, \*73,
    #: user@company.domain
    number: Optional[str]
    #: Indicates whether privacy is enabled for the name and number.
    privacy_enabled: bool
    #: The date and time the call history record was created. For a placed call history record, this is when the call
    #: was placed. For a missed call history record, this is when the call was disconnected. For a received call
    #: history record, this is when the call was answered.
    time: datetime.datetime


class ParkedAgainst(ApiModel):
    """
    The details of where the call has been parked.
    """
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, \*73, user@company.domain
    number: Optional[str]
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str]
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str]
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool]
    #: The call type for the party.
    call_type: CallType


class CallInfo(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for this call.
    call_id: str
    #: A unqiue identifier for the call session the call belongs to. This can be used to correlate multiple calls
    #: that are part of the same call session.
    call_session_id: str


class CallsApi(ApiChild, base='telephony/calls'):

    def dial(self, destination: str) -> DialResponse:
        """
        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts on all the devices belonging to the user. When the user answers on one of these alerting
        devices, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :type destination: str
        :return: Call id and call session id
        """
        ep = self.ep('dial')
        data = self.post(ep, json={'destination': destination})
        return DialResponse.parse_obj(data)

    def answer(self, call_id: str):
        """
        Answer an incoming call on the user's primary device.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        """
        ep = self.ep('answer')
        self.post(ep, json={'callId': call_id})

    def reject(self, call_id: str, action: RejectAction = None):
        """
        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('reject')
        self.post(ep, json=data)

    def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        """
        ep = self.ep('hangup')
        self.post(ep, json={'callId': call_id})

    def hold(self, call_id: str):
        """
        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('hold')
        self.post(ep, json=data)

    def resume(self, call_id: str):
        """
        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resume')
        self.post(ep, json=data)

    def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert a call to a destination or a user's voicemail. This is also commonly referred to as Blind Transfer

        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the
            call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the
            specified user's voicemail.
        :type to_voicemail: bool
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('divert')
        self.post(ep, json=data)

    def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None):
        """
        Transfer two calls together. Unanswered incoming calls cannot be transferred but can be diverted using the
        divert API. If the user has only two calls and wants to transfer them together, the callId1 and callId2
        parameters are optional and when not provided the calls are automatically selected and transferred. If the
        user has more than two calls and wants to transfer two of them together, the callId1 and callId2 parameters
        are mandatory to specify which calls are being transferred. These are also commonly referred to as Attended
        Transfer, Consultative Transfer, or Supervised Transfer and will return a 204 response. If the user wants to
        transfer one call to a new destination but only when the destination responds, the callId1 and destination
        parameters are mandatory to specify the call being transferred and the destination. This is referred to as a
        Mute Transfer and is similar to the divert API with the difference of waiting for the destination to respond
        prior to transferring the call. If the destination does not respond, the call is not transferred. This will
        return a 201 response.

        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either
            call_id2 or destination is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the first call to transfer. This parameter is mandatory if either
            callId2 or destination is provided.
        :type call_id1: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some
            examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain.
            This parameter is mandatory if call_id1 is provided and call_id2 is not provided.
        :type destination: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transfer')
        self.post(ep, json=data)

    def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> ParkedAgainst:
        """
        Park a connected call. The number field in the response can be used as the destination for the retrieve
        command to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifies where the call is to be parked. If not provided, the call is parked against the
            parking user.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param is_group_park: If set to true, the call is parked against an automatically selected member of the
            user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        :return: The details of where the call has been parked.
        :rtype: :class:`ParkedAgainst`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('park')
        data = self.post(ep, json=data)
        return ParkedAgainst.parse_obj(data)

    def retrieve(self, destination: str) -> CallInfo:
        """
        :param destination: Identifies where the call is parked. The number field from the park command response can
            be used as the destination for the retrieve command. If not provided, the call parked against the
            retrieving user is retrieved. The destination can be digits or a URI. Some examples for destination
            include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :return: call id and call session id of retreived call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('retrieve')
        data = self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    def start_recording(self, call_id: str):
        """
        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('startRecording')
        self.post(ep, json=data)

    def stop_recording(self, call_id: str):
        """
        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('stopRecording')
        self.post(ep, json=data)

    def pause_recording(self, call_id: str):
        """
        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pauseRecording')
        self.post(ep, json=data)

    def resume_recording(self, call_id: str):
        """
        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resumeRecording')
        self.post(ep, json=data)

    def transmit_dtmf(self, call_id: str, dtmf: str):
        """
        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, \*, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transmitDtmf')
        self.post(ep, json=data)

    def push(self, call_id: str):
        """
        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant’s call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('push')
        self.post(ep, json=data)

    def pickup(self, target: str) -> CallInfo:
        """
        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner
        to the dial command. When target is not present, the API pickups up a call from the user’s call pickup group.
        When target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user’s call pickup group is picked up. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pickup')
        data = self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    def barge_in(self, target: str):
        """
        Barge-in on another user’s answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('bargeIn')
        data = self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    def list_calls(self) -> Generator[TelephonyCall, None, None]:
        """
        Get the list of details for all active calls associated with the user.

        :return: yield :class:`TelephonyCall`
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=TelephonyCall)

    def call_details(self, call_id: str) -> TelephonyCall:
        """
        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        :return: call details
        :rtype: :class:`TelephonyCall`
        """
        ep = self.ep(call_id)
        data = self.get(ep)
        return TelephonyCall.parse_obj(data)

    def call_history(self, history_type: Union[str, HistoryType] = None) -> Generator[CallHistoryRecord, None, None]:
        """
        List Call History
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history
            records are retrieved.
            Possible values: placed, missed, received
        :type history_type: HistoryType or str
        :return: yields :class:`CallHistoryRecord` objects
        """
        history_type = history_type and HistoryType.history_type_or_str(history_type)
        params = history_type and {'type': history_type.value} or None
        url = self.ep('history')
        return self.session.follow_pagination(url=url, model=CallHistoryRecord, params=params)
