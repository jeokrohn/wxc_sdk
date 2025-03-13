"""
Person settings
"""
from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from .agent_caller_id import AgentCallerIdApi
from .app_shared_line import AppSharedLineApi
from .appservices import AppServicesApi
from .available_numbers import AvailableNumbersApi
from .barge import BargeApi
from .call_intercept import CallInterceptApi
from .call_recording import CallRecordingApi
from .call_waiting import CallWaitingApi
from .callbridge import CallBridgeApi
from .caller_id import CallerIdApi
from .calling_behavior import CallingBehaviorApi
from .common import ApiSelector
from .dnd import DndApi
from .ecbn import ECBNApi
from .exec_assistant import ExecAssistantApi
from .forwarding import PersonForwardingApi
from .hoteling import HotelingApi
from .mode_management import ModeManagementApi
from .moh import MusicOnHoldApi
from .monitoring import MonitoringApi
from .msteams import MSTeamsSettingApi
from .numbers import NumbersApi
from .permissions_in import IncomingPermissionsApi
from .permissions_out import OutgoingPermissionsApi
from .personal_assistant import PersonalAssistantApi
from .preferred_answer import PreferredAnswerApi
from .privacy import PrivacyApi
from .push_to_talk import PushToTalkApi
from .receptionist import ReceptionistApi
from .selective_accept import SelectiveAcceptApi
from .selective_forward import SelectiveForwardApi
from .selective_reject import SelectiveRejectApi
from .voicemail import VoicemailApi
from ..api_child import ApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import UserType, PrimaryOrShared, IdAndName, DeviceType
from ..common.schedules import ScheduleApi, ScheduleApiBase
from ..rest import RestSession

__all__ = ['PersonSettingsApi', 'DeviceOwner', 'DeviceActivationState', 'Hoteling', 'TelephonyDevice',
           'DeviceList']


# TODO: UC profile


class DeviceOwner(ApiModel):
    #: unique identifier for user or workspace the device is owned by
    owner_id: str = Field(alias='id', default=None)
    #: last name of device owner.
    last_name: Optional[str] = None
    #: First name of device owner.
    first_name: Optional[str] = None
    #: user or workspace?
    owner_type: UserType = Field(alias='type')
    #: user location
    location: Optional[IdAndName] = None


class DeviceActivationState(str, Enum):
    activating = 'ACTIVATING'
    activated = 'ACTIVATED'
    deactivated = 'DEACTIVATED'


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this
    #: host(workspace device) and use this device
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive
    #: calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool] = None
    #: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
    limit_guest_use: Optional[bool] = None
    #: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
    guest_hours_limit: Optional[int] = None


class TelephonyDevice(ApiModel):
    #: Unique identifier for a device.
    device_id: str = Field(alias='id')
    #: Comma separated array of tags used to describe device.
    description: list[str]
    #: Identifier for device model.
    model: str
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[PrimaryOrShared] = None
    #: Identifier for device model type.
    mod_type: DeviceType = Field(alias='modelType', default=None)
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ip_address: Optional[str] = None
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary
    #: Line/Port of the device.
    primary_owner: bool
    #: Hoteling login settings, which are available when the device is the owner's primary device and device type is
    #: PRIMARY. Hoteling login settings are set at the owner level.
    hoteling: Optional[Hoteling] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    device_type: PrimaryOrShared = Field(alias='type')
    #: Owner of device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of device.
    activation_state: DeviceActivationState
    # location details, only returned in context of virtual lines?
    location: Optional[IdAndName] = None


class DeviceList(ApiModel):
    #: Array of devices available to person.
    devices: list[TelephonyDevice]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: int
    #: Maximum number of devices a person can own.
    max_owned_device_count: Optional[int] = None


@dataclass(init=False, repr=False)
class PersonSettingsApi(ApiChild, base='people'):
    """
    API for all user level settings
    """

    #: agent caller id Api
    agent_caller_id: AgentCallerIdApi
    app_shared_line: AppSharedLineApi
    #: Person's Application Services Settings
    appservices: AppServicesApi
    #: Available numbers for a person
    available_numbers: AvailableNumbersApi
    #: Barge In Settings for a Person
    barge: BargeApi
    #: Call bridge settings for a person
    call_bridge: CallBridgeApi
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
    #: Do Not Disturb Settings for a Person
    dnd: DndApi
    #: ECBN settings
    ecbn: ECBNApi
    #: Executive Assistant Settings for a Person
    exec_assistant: ExecAssistantApi
    #: Forwarding Settings for a Person
    forwarding: PersonForwardingApi
    #: Hoteling Settings for a Person
    hoteling: HotelingApi
    #: Person's mode management settings
    mode_management: ModeManagementApi
    #: Person's Monitoring Settings
    monitoring: MonitoringApi
    # ; MS Teams settings
    ms_teams: MSTeamsSettingApi
    #: music on hold settings
    music_on_hold: MusicOnHoldApi
    #: Phone Numbers for a Person
    numbers: NumbersApi
    #: Incoming Permission Settings for a Person
    permissions_in: IncomingPermissionsApi
    #: Person's Outgoing Calling Permissions Settings
    permissions_out: OutgoingPermissionsApi
    #: Personal Assistant Settings
    personal_assistant: PersonalAssistantApi
    #: Preferred answer endpoint settings
    preferred_answer: PreferredAnswerApi
    #: Person's Privacy Settings
    privacy: PrivacyApi
    #: Push-to-Talk Settings for a Person
    push_to_talk: PushToTalkApi
    #: Receptionist Client Settings for a Person
    receptionist: ReceptionistApi
    #: Schedules for a Person
    schedules: ScheduleApi
    #: selective accept settings
    selective_accept: SelectiveAcceptApi
    #: selective forward settings
    selective_forward: SelectiveForwardApi
    #: selective reject settings
    selective_reject: SelectiveRejectApi

    #: Voicemail Settings for a Person
    voicemail: VoicemailApi

    def __init__(self, session: RestSession):
        """

        :meta private:
        """
        super().__init__(session=session)
        self.agent_caller_id = AgentCallerIdApi(session=session)
        self.app_shared_line = AppSharedLineApi(session=session)
        self.appservices = AppServicesApi(session=session)
        self.available_numbers = AvailableNumbersApi(session=session)
        self.barge = BargeApi(session=session)
        self.call_bridge = CallBridgeApi(session=session)
        self.call_intercept = CallInterceptApi(session=session)
        self.call_recording = CallRecordingApi(session=session)
        self.call_waiting = CallWaitingApi(session=session)
        self.calling_behavior = CallingBehaviorApi(session=session)
        self.caller_id = CallerIdApi(session=session)
        self.dnd = DndApi(session=session)
        self.ecbn = ECBNApi(session=session)
        self.exec_assistant = ExecAssistantApi(session=session)
        self.forwarding = PersonForwardingApi(session=session)
        self.hoteling = HotelingApi(session=session)
        self.mode_management = ModeManagementApi(session=session)
        self.monitoring = MonitoringApi(session=session)
        self.ms_teams = MSTeamsSettingApi(session=session)
        self.music_on_hold = MusicOnHoldApi(session=session)
        self.numbers = NumbersApi(session=session)
        self.permissions_in = IncomingPermissionsApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session)
        self.personal_assistant = PersonalAssistantApi(session=session)
        self.preferred_answer = PreferredAnswerApi(session=session)
        self.privacy = PrivacyApi(session=session)
        self.push_to_talk = PushToTalkApi(session=session)
        self.receptionist = ReceptionistApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.people)
        self.selective_accept = SelectiveAcceptApi(session=session, selector=ApiSelector.person)
        self.selective_forward = SelectiveForwardApi(session=session, selector=ApiSelector.person)
        self.selective_reject = SelectiveRejectApi(session=session, selector=ApiSelector.person)

        self.voicemail = VoicemailApi(session=session)

    # This endpoint is also available in the voicemail API and is only kept here for backward compatibility.
    def reset_vm_pin(self, person_id: str, org_id: str = None):
        """
        Reset Voicemail PIN

        Reset a voicemail PIN for a person.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        This endpoint is also available in the voicemail API and is only kept here for backward compatibility.

        :param person_id: Unique identifier for the person.
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{person_id}/features/voicemail/actions/resetPin/invoke')
        self.post(url, params=params)

    def devices(self, person_id: str, org_id: str = None) -> DeviceList:
        """
        Get all devices for a person.

        This requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Person to retrieve devices for
        :type person_id: str
        :param org_id: organization that person belongs to
        :type org_id: str
        :return: device info for user
        :rtype: DeviceList
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/people/{person_id}/devices')
        data = self.get(url=url, params=params)
        return DeviceList.model_validate(data)

    def modify_hoteling_settings_primary_devices(self, person_id: str, hoteling: Hoteling,
                                                 org_id: str = None):
        """
        Modify Hoteling Settings for a Person's Primary Devices

        Modify hoteling login configuration on a person's Webex Calling Devices which are in effect when the device is
        the user's primary device and device type is PRIMARY. To view the current hoteling login settings, see the
        `hoteling` field in `Get Person Devices
        <https://developer.webex.com/docs/api/v1/device-call-settings/get-person-devices>`_.

        Modifying devices for a person requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param person_id: ID of the person associated with the device.
        :type person_id: str
        :param hoteling: Modify person Device Hoteling Setting.
        :type hoteling: Hoteling
        :param org_id: Organization to which the person belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['hoteling'] = hoteling.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/devices/settings/hoteling')
        super().put(url, params=params, json=body)
