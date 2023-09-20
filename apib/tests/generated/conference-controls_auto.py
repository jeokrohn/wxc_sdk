from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ConferenceDetails', 'ConferenceParticipant', 'ConferenceStateEnum', 'ConferenceTypeEnum']


class ConferenceStateEnum(str, Enum):
    #: The controller is an active participant.
    connected = 'connected'
    #: The controller has held the conference and so is no longer an active participant.
    held = 'held'
    #: The conference has been released.
    disconnected = 'disconnected'


class ConferenceTypeEnum(str, Enum):
    bargein = 'bargeIn'
    silentmonitoring = 'silentMonitoring'
    coaching = 'coaching'


class ConferenceParticipant(ApiModel):
    #: The callId of the call.
    #: example: Y2lzY29z...
    callId: Optional[str] = None
    #: Indicates if the participant has been muted.
    #: example: True
    muted: Optional[bool] = None
    #: Indicates if the participant has been deafened (i.e. media stream is not being transmitting to the participant)
    #: example: True
    deafened: Optional[bool] = None


class ConferenceDetails(ApiModel):
    #: The state of the conference.
    state: Optional[ConferenceStateEnum] = None
    #: The appearance index for the conference leg. Only present when the conference has an appearance value assigned.
    #: example: 2.0
    appearance: Optional[int] = None
    #: The conference start time in ISO 8601 format.
    #: example: 2023-03-02T15:00:00.000Z
    created: Optional[datetime] = None
    #: Indicates if the host of the conference has been muted.
    muted: Optional[bool] = None
    #: The type of conference for a non-standard conference.
    #: example: bargeIn
    type: Optional[ConferenceTypeEnum] = None
    #: The participants in the conference.
    participants: Optional[list[ConferenceParticipant]] = None
