from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Call', 'CallHistoryRecord', 'CallHistoryRecordTypeEnum', 'CallPersonalityEnum', 'CallStateEnum',
            'CallTypeEnum', 'DialResponse', 'ListCallHistoryResponse', 'ListCallsResponse', 'ParkResponse',
            'PartyInformation', 'RecallInformation', 'RecallTypeEnum', 'RecordingStateEnum', 'RedirectionInformation',
            'RedirectionReasonEnum', 'RejectActionEnum']


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
    #: example: John Smith
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`,
    #: `user@company.domain`
    #: example: +12223334444
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9hMTlkODJhMi00ZTY5LTU5YWEtOWYyZi1iY2E2MzEwMTNhNjg=
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFL2ExOWQ4MmEyLTRlNjktNTlhYS05ZjJmLWJjYTYzMTAxM2E2OA==
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
    #: example: Y2lzY29zcGFyazovL3VzL0NBTEwvQkNMRC9jYWxsaGFsZi00ODg6MA
    id: Optional[str] = None
    #: The call session identifier of the call session the call belongs to. This can be used to correlate multiple
    #: calls that are part of the same call session.
    #: example: MmFmNThiZjktYWE3Ny00NWE5LThiMDEtYzI4NDMxZWYwNzRm
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
    #: example: 1.0
    appearance: Optional[int] = None
    #: The date and time the call was created.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None
    #: The date and time the call was answered. Only present when the call has been answered.
    #: example: 2016-04-21T17:00:00.000Z
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


class CallHistoryRecordTypeEnum(str, Enum):
    #: A call history record for an outgoing call placed by the user.
    placed = 'placed'
    #: A call history record for an incoming call to the user that was not answered.
    missed = 'missed'
    #: A call history record for an incoming call to the user that was answered.
    received = 'received'


class CallHistoryRecord(ApiModel):
    #: The type of call history record.
    type: Optional[CallHistoryRecordTypeEnum] = None
    #: The name of the called/calling party. Only present when the name is available and privacy is not enabled.
    #: example: John Smith
    name: Optional[str] = None
    #: The number of the called/calling party. Only present when the number is available and privacy is not enabled.
    #: The number can be digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`,
    #: `*73`, `user@company.domain`
    #: example: +12225554444
    number: Optional[str] = None
    #: Indicates whether privacy is enabled for the name and number.
    privacy_enabled: Optional[bool] = None
    #: The date and time the call history record was created. For a placed call history record, this is when the call
    #: was placed. For a missed call history record, this is when the call was disconnected. For a received call
    #: history record, this is when the call was answered.
    #: example: 2016-04-21T17:00:00.000Z
    time: Optional[datetime] = None


class RejectActionEnum(str, Enum):
    #: Send the call to busy.
    busy = 'busy'
    #: Send the call to temporarily unavailable.
    temporarily_unavailable = 'temporarilyUnavailable'
    #: Ignore the call by continuing ringback to the caller while no longer alerting the called user's devices.
    ignore = 'ignore'


class DialResponse(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for the same call.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTEwvQkNMRC9jYWxsaGFsZi00ODg6MA
    call_id: Optional[str] = None
    #: A unique identifier for the call session the call belongs to. This can be used to correlate multiple calls that
    #: are part of the same call session.
    #: example: MmFmNThiZjktYWE3Ny00NWE5LThiMDEtYzI4NDMxZWYwNzRm
    call_session_id: Optional[str] = None


class ParkResponse(ApiModel):
    #: The details of where the call has been parked.
    parked_against: Optional[PartyInformation] = None


class ListCallsResponse(ApiModel):
    items: Optional[list[Call]] = None


class ListCallHistoryResponse(ApiModel):
    items: Optional[list[CallHistoryRecord]] = None
