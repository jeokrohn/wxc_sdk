"""
Webex Meetings APIs
"""
from dataclasses import dataclass

from .chats import MeetingChatsApi
from .closed_captions import MeetingClosedCaptionsApi
from .invitees import MeetingInviteesApi
from .participants import MeetingParticipantsApi
from .preferences import MeetingPreferencesApi
from .qanda import MeetingQandAApi
from .qualities import MeetingQualitiesApi
from .transcripts import MeetingTranscriptsApi
from ..api_child import ApiChild
from ..rest import RestSession


@dataclass(init=False)
class MeetingsApi(ApiChild, base=''):
    #: meeting chats API
    chats: MeetingChatsApi
    #: closed captions API
    closed_captions: MeetingClosedCaptionsApi
    #: meeting invitees API
    invitees: MeetingInviteesApi
    #: meeting participants API
    participants: MeetingParticipantsApi
    #: preferences API
    preferences: MeetingPreferencesApi
    #: Q and A API
    qanda: MeetingQandAApi
    #: qualities API
    qualities: MeetingQualitiesApi
    #: transcripts
    transcripts: MeetingTranscriptsApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.chats = MeetingChatsApi(session=session)
        self.closed_captions = MeetingClosedCaptionsApi(session=session)
        self.invitees = MeetingInviteesApi(session=session)
        self.participants = MeetingParticipantsApi(session=session)
        self.preferences = MeetingPreferencesApi(session=session)
        self.qanda = MeetingQandAApi(session=session)
        self.qualities = MeetingQualitiesApi(session=session)
        self.transcripts = MeetingTranscriptsApi(session=session)
