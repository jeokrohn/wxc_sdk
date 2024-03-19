"""
Workspace settings, mostly identical to user settings

"""
from dataclasses import dataclass

from .devices import WorkspaceDevicesApi
from .numbers import WorkspaceNumbersApi
from ..api_child import ApiChild
from ..person_settings.callbridge import CallBridgeApi
from ..person_settings.call_intercept import CallInterceptApi
from ..person_settings.call_waiting import CallWaitingApi
from ..person_settings.caller_id import CallerIdApi
from ..person_settings.common import ApiSelector
from ..person_settings.forwarding import PersonForwardingApi
from ..person_settings.monitoring import MonitoringApi
from ..person_settings.permissions_in import IncomingPermissionsApi
from ..person_settings.permissions_out import OutgoingPermissionsApi
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
    call_bridge: CallBridgeApi
    call_intercept: CallInterceptApi
    call_waiting: CallWaitingApi
    caller_id: CallerIdApi
    devices: WorkspaceDevicesApi
    forwarding: PersonForwardingApi
    monitoring: MonitoringApi
    numbers: WorkspaceNumbersApi
    permissions_in: IncomingPermissionsApi
    permissions_out: OutgoingPermissionsApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.call_bridge = CallBridgeApi(session=session, selector=ApiSelector.workspace)
        self.call_intercept = CallInterceptApi(session=session, selector=ApiSelector.workspace)
        self.call_waiting = CallWaitingApi(session=session, selector=ApiSelector.workspace)
        self.caller_id = CallerIdApi(session=session, selector=ApiSelector.workspace)
        self.devices = WorkspaceDevicesApi(session=session)
        self.forwarding = PersonForwardingApi(session=session, selector=ApiSelector.workspace)
        self.monitoring = MonitoringApi(session=session, selector=ApiSelector.workspace)
        self.numbers = WorkspaceNumbersApi(session=session)
        self.permissions_in = IncomingPermissionsApi(session=session, selector=ApiSelector.workspace)
        self.permissions_out = OutgoingPermissionsApi(session=session, selector=ApiSelector.workspace)
