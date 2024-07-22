"""
Workspace settings, mostly identical to user settings

"""
from dataclasses import dataclass

from .devices import WorkspaceDevicesApi
from .numbers import WorkspaceNumbersApi
from ..api_child import ApiChild
from ..person_settings.anon_calls import AnonCallsApi
from ..person_settings.available_numbers import AvailableNumbersApi
from ..person_settings.barge import BargeApi
from ..person_settings.callbridge import CallBridgeApi
from ..person_settings.call_intercept import CallInterceptApi
from ..person_settings.call_policy import CallPolicyApi
from ..person_settings.call_waiting import CallWaitingApi
from ..person_settings.caller_id import CallerIdApi
from ..person_settings.common import ApiSelector
from ..person_settings.dnd import DndApi
from ..person_settings.forwarding import PersonForwardingApi
from ..person_settings.monitoring import MonitoringApi
from ..person_settings.moh import MusicOnHoldApi
from ..person_settings.permissions_in import IncomingPermissionsApi
from ..person_settings.permissions_out import OutgoingPermissionsApi
from ..person_settings.priority_alert import PriorityAlertApi
from ..person_settings.privacy import PrivacyApi
from ..person_settings.push_to_talk import PushToTalkApi
from ..person_settings.selective_accept import SelectiveAcceptApi
from ..person_settings.selective_forward import SelectiveForwardApi
from ..person_settings.selective_reject import SelectiveRejectApi
from ..person_settings.sequential_ring import SequentialRingApi
from ..person_settings.sim_ring import SimRingApi
from ..person_settings.voicemail import VoicemailApi
from ..rest import RestSession

__all__ = ['WorkspaceSettingsApi']


@dataclass(init=False)
class WorkspaceSettingsApi(ApiChild, base='workspaces'):
    """
    API for all workspace settings.

    Most of the workspace settings are equivalent to corresponding user settings. For these settings the attributes of
    this class are instances of the respective user settings APIs. When calling endpoints of these APIs workspace IDs
    need to be passed to the ``person_id`` parameter of the called function.
    """
    anon_calls: AnonCallsApi
    available_numbers: AvailableNumbersApi
    barge: BargeApi
    call_bridge: CallBridgeApi
    call_intercept: CallInterceptApi
    call_policy: CallPolicyApi
    call_waiting: CallWaitingApi
    caller_id: CallerIdApi
    dnd: DndApi
    devices: WorkspaceDevicesApi
    forwarding: PersonForwardingApi
    monitoring: MonitoringApi
    music_on_hold: MusicOnHoldApi
    numbers: WorkspaceNumbersApi
    permissions_in: IncomingPermissionsApi
    permissions_out: OutgoingPermissionsApi
    priority_alert: PriorityAlertApi
    privacy: PrivacyApi
    push_to_talk: PushToTalkApi
    selective_accept: SelectiveAcceptApi
    selective_forward: SelectiveForwardApi
    selective_reject: SelectiveRejectApi
    sequential_ring: SequentialRingApi
    sim_ring: SimRingApi
    voicemail: VoicemailApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.anon_calls = AnonCallsApi(session=session, selector=ApiSelector.workspace)
        self.available_numbers = AvailableNumbersApi(session=session, selector=ApiSelector.workspace)
        self.barge = BargeApi(session=session, selector=ApiSelector.workspace)
        self.call_bridge = CallBridgeApi(session=session, selector=ApiSelector.workspace)
        self.call_intercept = CallInterceptApi(session=session, selector=ApiSelector.workspace)
        self.call_policy = CallPolicyApi(session=session, selector=ApiSelector.workspace)
        self.call_waiting = CallWaitingApi(session=session, selector=ApiSelector.workspace)
        self.caller_id = CallerIdApi(session=session, selector=ApiSelector.workspace)
        self.devices = WorkspaceDevicesApi(session=session)
        self.dnd = DndApi(session=session, selector=ApiSelector.workspace)
        self.forwarding = PersonForwardingApi(session=session, selector=ApiSelector.workspace)
        self.monitoring = MonitoringApi(session=session, selector=ApiSelector.workspace)
        self.music_on_hold = MusicOnHoldApi(session=session, selector=ApiSelector.workspace)
        self.numbers = WorkspaceNumbersApi(session=session)
        self.permissions_in = IncomingPermissionsApi(session=session, selector=ApiSelector.workspace)
        self.permissions_out = OutgoingPermissionsApi(session=session, selector=ApiSelector.workspace)
        self.priority_alert = PriorityAlertApi(session=session, selector=ApiSelector.workspace)
        self.privacy = PrivacyApi(session=session, selector=ApiSelector.workspace)
        self.push_to_talk = PushToTalkApi(session=session, selector=ApiSelector.workspace)
        self.selective_accept = SelectiveAcceptApi(session=session, selector=ApiSelector.workspace)
        self.selective_forward = SelectiveForwardApi(session=session, selector=ApiSelector.workspace)
        self.selective_reject = SelectiveRejectApi(session=session, selector=ApiSelector.workspace)
        self.sequential_ring = SequentialRingApi(session=session, selector=ApiSelector.workspace)
        self.sim_ring = SimRingApi(session=session, selector=ApiSelector.workspace)
        self.voicemail = VoicemailApi(session=session, selector=ApiSelector.workspace)
