"""
Person settings
"""

from .appservices import AppServicesApi
from .barge import BargeApi
from .call_intercept import CallInterceptApi
from .call_recording import CallRecordingApi
from .call_waiting import CallWaitingApi
from .caller_id import CallerIdApi
from .dnd import DndApi
from .exec_assistant import ExecAssistantApi
from .forwarding import PersonForwardingApi
from .hoteling import HotelingApi
from .monitoring import MonitoringApi
from .numbers import NumbersApi
from .privacy import PrivacyApi
from .receptionist import ReceptionistApi
from .voicemail import VoicemailApi
from ..api_child import ApiChild
from ..rest import RestSession
from .permissions_in import IncomingPermissionsApi
from .permissions_out import OutgoingPermissionsApi
from ..common.schedules import ScheduleApi, ScheduleApiBase

__all__ = ['PersonSettingsApi']


# TODO: UC profile
# TODO: push to talk
# TODO: what about auto transfer numbers? These seem to exist in workspace settings


class PersonSettingsApi(ApiChild, base='people'):
    """
    API for all user level settings

    :ivar appservices: app services settings API: :class:`appservices.AppServicesApi`
    :ivar barge: barge API :class:`barge.BargeApi`
    :ivar call_intercept: call intercept API :class:`call_intercept.CallInterceptApi`
    :ivar call_recording: call recording API :class:`call_recording.CallRecordingApi`
    :ivar call_waiting: call waiting API: :class:`call_waiting.CallWaitingApi`
    :ivar caller_id: caller id API :class:`caller_id.CallerIdApi`
    :ivar dnd: DND API :class:`dnd.DndApi`
    :ivar exec_assistant: exec assistant settings API: :class:`exec_assistant.ExecAssistantApi`
    :ivar forwarding: call forwarding API :class:`forwarding.ForwardingApi`
    :ivar hoteling: hoteling API: :class:`hoteling.HotelingApi`
    :ivar numbers: numbers API: :class:`numbers.NumbersApi`
    :ivar permissions_in: incoming permission settings API: :class:`permissions_in.IncomingPermissionsApi`
    :ivar permissions_out: outgoing permission settings API: :class:`permissions_out.OutgoingPermissionsApi`
    :ivar privacy: privacy API: :class:`privacy.PrivacyApi`
    :ivar receptionist: receptionist client settings API: :class:`receptionist.ReceptionistApi`
    :ivar voicemail: voicemail API: :class:`voicemail.VoicemailApi`
    """

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.caller_id = CallerIdApi(session=session)
        self.call_recording = CallRecordingApi(session=session)
        self.call_intercept = CallInterceptApi(session=session)
        self.forwarding = PersonForwardingApi(session=session)
        self.barge = BargeApi(session=session)
        self.dnd = DndApi(session=session)
        self.voicemail = VoicemailApi(session=session)
        self.call_waiting = CallWaitingApi(session=session)
        self.monitoring = MonitoringApi(session=session)
        self.hoteling = HotelingApi(session=session)
        self.privacy = PrivacyApi(session=session)
        self.numbers = NumbersApi(session=session)
        self.appservices = AppServicesApi(session=session)
        self.exec_assistant = ExecAssistantApi(session=session)
        self.receptionist = ReceptionistApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.people)
        self.permissions_in = IncomingPermissionsApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session)

    def reset_vm_pin(self, person_id: str, org_id: str = None):
        """
        Reset Voicemail PIN

        Reset a voicemail PIN for a person.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{person_id}/features/voicemail/actions/resetPin/invoke')
        self.post(url, params=params)
