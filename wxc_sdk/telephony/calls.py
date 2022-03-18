"""
Webex Calling Call Control API and related data types
"""
import datetime
from collections.abc import Generator
from enum import Enum
from typing import Optional, Literal, List, Union

from pydantic import Field

from ..webhook import WebHook
from ..api_child import ApiChild
from ..base import ApiModel

__all__ = ['CallType', 'TelephonyParty', 'RedirectReason', 'Redirection', 'Recall', 'RecordingState',
           'Personality', 'CallState', 'TelephonyCall', 'TelephonyEventData', 'TelephonyEvent', 'DialResponse',
           'HistoryType', 'CallHistoryRecord',
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
    redirections: List[Redirection] = Field(default_factory=list)
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

    def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        """
        ep = self.ep('hangup')
        self.post(ep, json={'callId': call_id})

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
        :rtype: TelephonyCall
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

    # TODO: implement missing endpoints
    #   * reject
    #   * hold
    #   * resume
    #   * divert
    #   * transfer
    #   * park
    #   * retrieve
    #   * start/stop/pause/resume recording
    #   * transmit DTMF
    #   * push
    #   * pickup
    #   * barge in
