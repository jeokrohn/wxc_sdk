"""
Person settings
"""
from dataclasses import dataclass

from .appservices import AppServicesApi
from .barge import BargeApi
from .call_intercept import CallInterceptApi
from .call_recording import CallRecordingApi
from .call_waiting import CallWaitingApi
from .caller_id import CallerIdApi
from .calling_behavior import CallingBehaviorApi
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
from .push_to_talk import PushToTalkApi
from ..common.schedules import ScheduleApi, ScheduleApiBase

__all__ = ['PersonSettingsApi']


# TODO: UC profile
# TODO: what about auto transfer numbers? These seem to exist in workspace settings

@dataclass(init=False)
class PersonSettingsApi(ApiChild, base='people'):
    """
    API for all user level settings
    """
    appservices: AppServicesApi
    barge: BargeApi
    dnd: DndApi
    call_intercept: CallInterceptApi
    call_recording: CallRecordingApi
    call_waiting: CallWaitingApi
    caller_id: CallerIdApi
    calling_behavior: CallingBehaviorApi
    exec_assistant: ExecAssistantApi
    forwarding: PersonForwardingApi
    hoteling: HotelingApi
    monitoring: MonitoringApi
    numbers: NumbersApi
    permissions_in: IncomingPermissionsApi
    permissions_out: OutgoingPermissionsApi
    privacy: PrivacyApi
    push_to_talk: PushToTalkApi
    receptionist: ReceptionistApi
    schedules: ScheduleApi
    voicemail: VoicemailApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.appservices = AppServicesApi(session=session)
        self.barge = BargeApi(session=session)
        self.dnd = DndApi(session=session)
        self.call_intercept = CallInterceptApi(session=session)
        self.call_recording = CallRecordingApi(session=session)
        self.call_waiting = CallWaitingApi(session=session)
        self.calling_behavior = CallingBehaviorApi(session=session)
        self.caller_id = CallerIdApi(session=session)
        self.exec_assistant = ExecAssistantApi(session=session)
        self.forwarding = PersonForwardingApi(session=session)
        self.hoteling = HotelingApi(session=session)
        self.monitoring = MonitoringApi(session=session)
        self.numbers = NumbersApi(session=session)
        self.permissions_in = IncomingPermissionsApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session)
        self.privacy = PrivacyApi(session=session)
        self.push_to_talk = PushToTalkApi(session=session)
        self.receptionist = ReceptionistApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.people)
        self.voicemail = VoicemailApi(session=session)

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
