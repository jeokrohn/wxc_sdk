"""
Person settings
"""

from .barge import BargeApi
from .call_intercept import CallInterceptApi
from .call_recording import CallRecordingApi
from .caller_id import CallerIdApi
from .forwarding import PersonForwardingApi
from .voicemail import VoicemailApi
from .dnd import DndApi
from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['PersonSettingsApi']

# TODO: UC profile
# TODO: schedules
# TODO: schedule events
# TODO: call waiting
# TODO: monitoring
# TODO: list of phone numbers
# TODO: application settings
# TODO: privacy settings
# TODO: exec assistant settings
# TODO: receptionist client settings
# TODO: push to talk
# TODO: hoteling
# TODO: reset VM PIN
# TODO: incoming permissions
# TODO: outgoing permissions

class PersonSettingsApi(ApiChild, base='people'):
    """
    API for all user level settings

    :ivar caller_id: caller id API :class:`caller_id.CallerIdApi`
    :ivar call_recording: call recording API :class:`call_recording.CallRecordingApi`
    :ivar call_intercept: call intercept API :class:`call_intercept.CallInterceptApi`
    :ivar forwarding: call forwarding API :class:`forwarding.ForwardingApi`
    :ivar barge: barge API :class:`barge.BargeApi`
    :ivar dnd: DND API :class:`dnd.DndApi`
    :ivar voicemail: Voicemail API: :class:`voicemail.VoicemailApi`
    """

    def __init__(self, session: RestSession):
        super().__init__(session)
        self.caller_id = CallerIdApi(session)
        self.call_recording = CallRecordingApi(session)
        self.call_intercept = CallInterceptApi(session)
        self.forwarding = PersonForwardingApi(session)
        self.barge = BargeApi(session)
        self.dnd = DndApi(session)
        self.voicemail = VoicemailApi(session)
