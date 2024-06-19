from datetime import datetime
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['ConferenceControlsApi', 'ConferenceDetails', 'ConferenceParticipant', 'ConferenceState',
           'ConferenceTypeEnum']


class ConferenceState(str, Enum):
    #: The controller is an active participant.
    connected = 'connected'
    #: The controller has held the conference and so is no longer an active participant.
    held = 'held'
    #: The conference has been released.
    disconnected = 'disconnected'


class ConferenceTypeEnum(str, Enum):
    barge_in = 'bargeIn'
    silent_monitoring = 'silentMonitoring'
    coaching = 'coaching'


class ConferenceParticipant(ApiModel):
    #: The callId of the call.
    call_id: Optional[str] = None
    #: Indicates if the participant has been muted.
    muted: Optional[bool] = None
    #: Indicates if the participant has been deafened (i.e. media stream is not being transmitting to the participant)
    deafened: Optional[bool] = None


class ConferenceDetails(ApiModel):
    #: The state of the conference.
    state: Optional[ConferenceState] = None
    #: The appearance index for the conference leg. Only present when the conference has an appearance value assigned.
    appearance: Optional[int] = None
    #: The conference start time in ISO 8601 format.
    created: Optional[datetime] = None
    #: Indicates if the host of the conference has been muted.
    muted: Optional[bool] = None
    #: The type of conference for a non-standard conference.
    type: Optional[ConferenceTypeEnum] = None
    #: The participants in the conference.
    participants: Optional[list[ConferenceParticipant]] = None


class ConferenceControlsApi(ApiChild, base='telephony/conference'):
    """
    Conference Controls

    Not supported for Webex for Government (FedRAMP)

    Conference Control APIs in support of Webex Calling.

    All `GET` commands require the `spark:calls_read` scope while all other commands require the `spark:calls_write`
    scope.
    """

    def start_conference(self, call_ids: list[str]):
        """
        Start Conference

        Join the user's calls into a conference.  A minimum of two call IDs are required. Each call ID identifies an
        existing call between the user
        and a participant to be added to the conference.

        :param call_ids: List of call identifiers of the participants to join into the conference. A minimum of two
            call IDs are required.
        :type call_ids: list[str]
        :rtype: None
        """
        body = dict()
        body['callIds'] = call_ids
        url = self.ep()
        super().post(url, json=body)

    def release_conference(self):
        """
        Release Conference

        Release the conference (the host and all participants). Note that for a 3WC (three-way call) the `Transfer API
        <https://developer.webex.com/docs/api/v1/call-controls/transfer>`_
        can be used to perform an attended transfer so that the participants remain connected.

        :rtype: None
        """
        url = self.ep()
        super().delete(url)

    def get_conference_details(self) -> ConferenceDetails:
        """
        Get Conference Details

        Get the details of the conference.  An empty JSON object body is returned if there is no conference.

        :rtype: :class:`ConferenceDetails`
        """
        url = self.ep()
        data = super().get(url)
        r = ConferenceDetails.model_validate(data)
        return r

    def add_participant(self, call_id: str):
        """
        Add Participant

        Adds a participant to an existing conference.  The request body contains the participant's call ID.

        :param call_id: The call identifier of the participant to add.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('addParticipant')
        super().post(url, json=body)

    def mute(self, call_id: str = None):
        """
        Mute

        Mutes the host or a participant. Mutes the host when no request body is provided (i.e. media stream from the
        host will not be transmitted to the conference).  Mutes a participant when the request body contains the
        participant's call ID (i.e. media stream from the participant will not be transmitted to the conference).

        :param call_id: The call identifier of the participant to mute. The conference host is muted when this
            attribute is not provided.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('mute')
        super().post(url, json=body)

    def unmute(self, call_id: str = None):
        """
        Unmute

        Unmutes the host or a participant. Unmutes the host when no request body is provided (i.e. media stream from
        the host will be transmitted to the conference).  Unmutes a participant when the request body contains the
        participant's call ID (i.e. media stream from the participant will be transmitted to the conference).

        :param call_id: The call identifier of the participant to unmute. The conference host is unmuted when this
            attribute is not provided.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('unmute')
        super().post(url, json=body)

    def deafen_participant(self, call_id: str):
        """
        Deafen Participant

        Deafens a participant (i.e. media stream will not be transmitted to the participant).
        The request body contains the call ID of the participant to deafen

        :param call_id: The call identifier of the participant to deafen.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('deafen')
        super().post(url, json=body)

    def undeafen_participant(self, call_id: str):
        """
        Undeafen Participant

        Undeafens a participant (i.e. resume transmitting the conference media stream to the participant).
        The request body contains the call ID of the participant to undeafen.

        :param call_id: The call identifier of the participant to undeafen.
        :type call_id: str
        :rtype: None
        """
        body = dict()
        body['callId'] = call_id
        url = self.ep('undeafen')
        super().post(url, json=body)

    def hold(self):
        """
        Hold

        Hold the conference host.  There is no request body.

        :rtype: None
        """
        url = self.ep('hold')
        super().post(url)

    def resume(self):
        """
        Resume

        Resumes the held conference host.  There is no request body.

        :rtype: None
        """
        url = self.ep('resume')
        super().post(url)
