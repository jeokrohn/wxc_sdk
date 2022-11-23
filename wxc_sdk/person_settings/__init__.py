"""
Person settings
"""
from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from .agent_caller_id import AgentCallerIdApi
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
from .permissions_in import IncomingPermissionsApi
from .permissions_out import OutgoingPermissionsApi
from .privacy import PrivacyApi
from .push_to_talk import PushToTalkApi
from .receptionist import ReceptionistApi
from .voicemail import VoicemailApi
from ..api_child import ApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import UserType, PrimaryOrShared
from ..common.schedules import ScheduleApi, ScheduleApiBase
from ..rest import RestSession

__all__ = ['PersonSettingsApi', 'DeviceOwner', 'DeviceActivationState', 'TelephonyDevice', 'PersonDevicesResponse']


# TODO: UC profile


class DeviceOwner(ApiModel):
    #: unique identifier for user or workspace the device is owned by
    owner_id: str = Field(alias='id')
    #: last name of device owner.
    last_name: str
    #: First name of device owner.
    first_name: str
    #: user or workspace?
    owner_type: UserType = Field(alias='type')


class DeviceActivationState(str, Enum):
    activating = 'ACTIVATING'
    activated = 'ACTIVATED'
    deactivated = 'DEACTIVATED'


class TelephonyDevice(ApiModel):
    #: Unique identifier for a device.
    device_id: str = Field(alias='id')
    #: Comma separated array of tags used to describe device.
    description: list[str]
    #: Identifier for device model.
    model: str
    #: MAC address of device.
    mac: Optional[str]
    #: IP address of device.
    ip_address: Optional[str]
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary
    #: Line/Port of the device.
    primary_owner: bool
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    device_type: PrimaryOrShared = Field(alias='type')
    #: Owner of device.
    owner: DeviceOwner
    #: Activation state of device.
    activation_state: DeviceActivationState


class PersonDevicesResponse(ApiModel):
    #: Array of devices available to person.
    devices: list[TelephonyDevice]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: int


@dataclass(init=False)
class PersonSettingsApi(ApiChild, base='people'):
    """
    API for all user level settings
    """

    #: agent caller id Api
    agent_caller_id: AgentCallerIdApi
    #: Person's Application Services Settings
    appservices: AppServicesApi
    #: Barge In Settings for a Person
    barge: BargeApi
    #: Do Not Disturb Settings for a Person
    dnd: DndApi
    #: Call Intercept Settings for a Person
    call_intercept: CallInterceptApi
    #: Call Recording Settings for a Person
    call_recording: CallRecordingApi
    #: Call Waiting Settings for a Person
    call_waiting: CallWaitingApi
    #: Caller ID Settings for a Person
    caller_id: CallerIdApi
    #: Person's Calling Behavior
    calling_behavior: CallingBehaviorApi
    #: Executive Assistant Settings for a Person
    exec_assistant: ExecAssistantApi
    #: Forwarding Settings for a Person
    forwarding: PersonForwardingApi
    #: Hoteling Settings for a Person
    hoteling: HotelingApi
    #: Person's Monitoring Settings
    monitoring: MonitoringApi
    #: Phone Numbers for a Person
    numbers: NumbersApi
    #: Incoming Permission Settings for a Person
    permissions_in: IncomingPermissionsApi
    #: Person's Outgoing Calling Permissions Settings
    permissions_out: OutgoingPermissionsApi
    #: Person's Privacy Settings
    privacy: PrivacyApi
    #: Push-to-Talk Settings for a Person
    push_to_talk: PushToTalkApi
    #: Receptionist Client Settings for a Person
    receptionist: ReceptionistApi
    #: Schedules for a Person
    schedules: ScheduleApi
    #: Voicemail Settings for a Person
    voicemail: VoicemailApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.agent_caller_id = AgentCallerIdApi(session=session)
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

    def devices(self, person_id: str, org_id: str = None) -> PersonDevicesResponse:
        """
        Get all devices for a person.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person to retrieve devices for
        :type person_id: str
        :param org_id: organization that person belongs to
        :type org_id: str
        :return: device info for user
        :rtype: PersonDevicesResponse
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/people/{person_id}/devices')
        data = self.get(url=url, params=params)
        return PersonDevicesResponse.parse_obj(data)
