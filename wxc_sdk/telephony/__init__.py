"""
Telephony types and API (location and organisation settings)
"""
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from pydantic import Field, TypeAdapter, field_validator

from .access_codes import LocationAccessCodesApi
from .announcements_repo import AnnouncementsRepositoryApi
from .autoattendant import AutoAttendantApi
from .call_recording import CallRecordingSettingsApi
from .call_routing import CallRoutingApi
from .callpark import CallParkApi
from .callpark_extension import CallparkExtensionApi
from .callpickup import CallPickupApi
from .callqueue import CallQueueApi
from .calls import CallsApi
from .conference import ConferenceControlsApi
from .dect_devices import DECTDevicesApi
from .devices import TelephonyDevicesApi
from .huntgroup import HuntGroupApi
from .jobs import JobsApi
from .location import TelephonyLocationApi
from .location.intercept import LocationInterceptApi
from .org_access_codes import OrganisationAccessCodesApi
from .organisation_vm import OrganisationVoicemailSettingsAPI
from .paging import PagingApi
from .playlists import PlayListApi
from .pnc import PrivateNetworkConnectApi
from .prem_pstn import PremisePstnApi
from .supervisor import SupervisorApi
from .virtual_line import VirtualLinesApi
from .vm_rules import VoicemailRulesApi
from .voice_messaging import VoiceMessagingApi
from .voicemail_groups import VoicemailGroupsApi
from .voiceportal import VoicePortalApi
from ..api_child import ApiChild
from ..base import ApiModel, to_camel, plus1, enum_str
from ..base import SafeEnum as Enum
from ..common import UserType, RouteIdentity, NumberState, ValidateExtensionsResponse, ValidatePhoneNumbersResponse, \
    DeviceCustomization, IdAndName, OwnerType, NumberOwner
from ..common.schedules import ScheduleApi, ScheduleApiBase
from ..person_settings.common import ApiSelector
from ..person_settings.permissions_out import OutgoingPermissionsApi, Action
from ..rest import RestSession

__all__ = ['NumberListPhoneNumberType', 'TelephonyType',
           'NumberListPhoneNumber',
           'NumberType', 'NumberDetails', 'UCMProfile',
           'TestCallRoutingResult', 'OriginatorType', 'CallSourceType', 'CallSourceInfo', 'DestinationType',
           'LocationAndNumbers', 'HostedUserDestination', 'ServiceType', 'HostedFeatureDestination',
           'TrunkDestination', 'PbxUserDestination', 'PstnNumberDestination', 'VirtualExtensionDestination',
           'RouteListDestination', 'FeatureAccessCodeDestination', 'EmergencyDestination',
           'TranslationPatternConfigurationLevel', 'AppliedServiceTranslationPattern', 'ConfigurationLevel',
           'CallInterceptDetailsPermission', 'CallInterceptDetails', 'CallingPlanReason',
           'OutgoingCallingPlanPermissionsByType', 'OutgoingCallingPlanPermissionsByDigitPattern', 'AppliedService',
           'DeviceType', 'DeviceManufacturer', 'DeviceManagedBy', 'OnboardingMethod', 'DeviceSettingsConfiguration',
           'SupportedDevice', 'AnnouncementLanguage', 'SupportedDevices', 'TelephonyApi']


class NumberListPhoneNumberType(str, Enum):
    primary = 'PRIMARY'
    alternate = 'ALTERNATE'
    fax = 'FAX'
    dnis = 'DNIS'


class TelephonyType(str, Enum):
    #: Object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: Object is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class NumberListPhoneNumber(ApiModel):
    """
    Phone Number
    """
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Phone number's state.
    state: Optional[NumberState] = None
    #: Type of phone number.
    phone_number_type: Optional[NumberListPhoneNumberType] = None
    #: Indicates if the phone number is used as location clid.
    main_number: bool
    #: Indicates if a phone number is a toll-free number.
    toll_free_number: bool
    #: Indicates Telephony type for the number.
    included_telephony_types: Optional[TelephonyType] = None
    #: Mobile Network for the number if number is MOBILE_NUMBER.
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if number is MOBILE_NUMBER.
    routing_profile: Optional[str] = None
    location: IdAndName
    owner: Optional[NumberOwner] = None


class NumberType(str, Enum):
    extension = 'EXTENSION'
    number = 'NUMBER'


class NumberDetails(ApiModel):
    #: Count of phone numbers that are in the assigned state.
    assigned: Optional[int] = None
    #: Count of phone numbers which are in the un-assigned state.
    un_assigned: Optional[int] = None
    #: Count of phone numbers which are inactive.
    in_active: Optional[int] = None
    #: Count of extensions only without phone number.
    extension_only: Optional[int] = None
    #: Count of the toll free numbers.
    toll_free_numbers: Optional[int] = None
    #: Total phone numbers and extensions available.
    total: Optional[int] = None
    #: Count of phone numbers of type `MOBILE_NUMBER` only without `PSTN_NUMBER` and extension.
    mobile_number: Optional[int] = None


class UCMProfile(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    profile_id: str = Field(alias='id')
    #: Unique name for the calling UC Manager Profile.
    name: str


class OriginatorType(str, Enum):
    #: User
    user = 'USER'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class CallSourceType(str, Enum):
    """
    The type of call source.
    """
    #: Indicates that the call source is a route list
    route_list = 'ROUTE_LIST'
    #: Indicates that the call source is a dial pattern.
    dial_pattern = 'DIAL_PATTERN'
    #: Indicates that the call source extension is unknown.
    unknown_extension = 'UNKNOWN_EXTENSION'
    #: Indicates that the call source phone number is unknown.
    unknown_number = 'UNKNOWN_NUMBER'


class CallSourceInfo(ApiModel):
    """
    This data object is only returned when originatorNumber is specified in the request.
    """
    #: The type of call source.
    call_source_type: CallSourceType
    #: When originatorType is "trunk", originatorId is a valid trunk, this trunk belongs to a route group which is
    #: assigned to a route list with the name routeListA, and originatorNumber is a number assigned to routeListA.
    #: routeListA is returned here. This element is returned when callSourceType is ROUTE_LIST.
    route_list_name: Optional[str] = None
    #: route list id
    route_list_id: Optional[str] = None
    #: When originatorType is "trunk", originatorId is a valid trunk with name trunkA, trunkA belongs to a route group
    #: which is assigned to a route list with name routeListA, trunkA is also assigned to dialPlanA as routing choice,
    #: dialPlanA has dialPattern xxxx assigned. If the originatorNumber match the dialPattern xxxx, dialPlanA is
    #: returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_plan_name: Optional[str] = None
    #: When originatorType is "trunk", originatorId is a valid trunk with the name trunkA, trunkA belongs to a route
    #: group which is assigned to a route list with the name routeListA, trunkA is also assigned to dialPlanA as routing
    #: choice, dialPlanA has dialPattern xxxx assigned. If the originatorNumber match the dialPattern xxxx, dialPattern
    #: xxxx is returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_pattern: Optional[str] = None
    #: dial plan id
    dial_plan_id: Optional[str] = None


class DestinationType(str, Enum):
    """
    Matching destination type for the call.
    """
    #: Matching destination is a person or workspace with details in the hosted_user field.
    hosted_agent = 'HOSTED_AGENT'
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the hostedFeature
    #: field.
    hosted_feature = 'HOSTED_FEATURE'
    #: Matching destination routes into a separate PBX with details in the pbxUser field.
    pbx_user = 'PBX_USER'
    #: Matching destination routes into a PSTN phone number with details in the pstnNumber field.
    pstn_number = 'PSTN_NUMBER'
    #: Matching destination routes into a virtual extension with details in the virtualExtension field.
    virtual_extension = 'VIRTUAL_EXTENSION'
    #: Matching destination routes into a virtual extension range with details in the virtualExtensionRange field.
    virtual_extension_range = 'VIRTUAL_EXTENSION_RANGE'
    #: Matching destination routes into a route list with details in the routeList field.
    route_list = 'ROUTE_LIST'
    #: Matching destination routes into a feature access code (FAC) with details in the featureAccessCode field.
    fac = 'FAC'
    #: Matching destination routes into an emergency service like Red Sky, with details in the emergency field.
    emergency = 'EMERGENCY'
    #: The route is in a repair state with routing choice details in the repair field.
    repair = 'REPAIR'
    #: Target extension is unknown with routing choice details in the unknownExtension field.
    unknown_extension = 'UNKNOWN_EXTENSION'
    #: The target phone number is unknown with routing choice details in the unknownNumber field.
    unknown_number = 'UNKNOWN_NUMBER'


class LocationAndNumbers(ApiModel):
    @field_validator('phone_number', mode='before')
    def e164(cls, v):
        """
        :meta private:
        """
        return plus1(v)

    location_name: str
    location_id: str
    phone_number: Optional[str] = None
    extension: Optional[str] = None


class HostedUserDestination(LocationAndNumbers):
    """
    This data object is returned when destinationType is HOSTED_USER.
    """
    #: person/workspace's id
    hu_id: str = Field(alias='id')
    #: Type of agent for call destination.
    hu_type: UserType = Field(alias='type')
    #: Person or workspace's first name.
    first_name: str
    #: Person or workspace's last name.
    last_name: str


class ServiceType(str, Enum):
    #: Indicates that this destination is an auto attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: Indicates that this destination is the Office (Broadworks) Anywhere feature.
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    #: Indicates that this destination is the Call Queue feature.
    call_queue = 'CALL_QUEUE'
    #: Indicates that this destination is the Contact Center Link feature.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: Indicates that this destination is the Group Paging feature.
    group_paging = 'GROUP_PAGING'
    #: Indicates that this destination is the Hunt Group feature.
    hunt_group = 'HUNT_GROUP'
    #: Indicates that this destination is the Voice Messaging feature.
    voice_messaging = 'VOICE_MESSAGING'
    #: Indicates that this destination is the Voice Mail Group feature.
    voice_mail_group = 'VOICE_MAIL_GROUP'


class HostedFeatureDestination(LocationAndNumbers):
    """
    This data object is returned when destinationType is HOSTED_FEATURE
    """
    service_type: ServiceType = Field(alias='type')
    #: service instance name
    name: str
    #: service instance id
    service_instance_id: str = Field(alias='id')


class TrunkDestination(ApiModel):
    trunk_name: Optional[str] = None
    trunk_id: Optional[str] = None
    route_group_name: Optional[str] = None
    route_group_id: Optional[str] = None
    #: location of the trunk, required if trunkName is returned
    trunk_location_name: Optional[str] = None
    #: location id of the trunk, required if trunkName is returned
    trunk_location_id: Optional[str] = None


class PbxUserDestination(TrunkDestination):
    """
    This data object is returned when destinationType is PBX_USER.
    """
    #: the dial plan name that the called string matches
    dial_plan_name: str
    dial_plan_id: str
    #: the dial pattern that the called string matches
    dial_pattern: str


class PstnNumberDestination(TrunkDestination):
    pass


class VirtualExtensionDestination(LocationAndNumbers, TrunkDestination):
    #: Virtual extension ID.
    virtual_extension_id: str = Field(alias='id')
    #: Virtual extension display first name.
    first_name: str
    #: Virtual extension display last name.
    last_name: str
    #: Virtual extension display name.
    display_name: str


class VirtualExtensionRange(LocationAndNumbers, TrunkDestination):
    #: Virtual extension range ID.
    id: Optional[str] = None
    #: Virtual extension range name.
    name: Optional[str] = None
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix;
    #: BCD/Enhanced mode can have any valid prefix).
    prefix: Optional[str] = None
    #: Pattern associated with the virtual extension range.
    pattern: Optional[str] = None


class RouteListDestination(ApiModel):
    """
    This data object is returned when destinationType is ROUTE_LIST.
    """
    route_list_id: str = Field(alias='id')
    name: str
    route_group_name: str
    route_group_id: str
    location_name: str
    location_id: str


class FeatureAccessCodeDestination(ApiModel):
    """
    This data object is returned when destinationType is FAC.
    """
    code: str
    name: str


class EmergencyDestination(TrunkDestination):
    """
    This data object is returned when destinationType is EMERGENCY.
    """
    is_red_sky: bool


class TranslationPatternConfigurationLevel(str, Enum):
    #: The applied services of location level.
    location = 'LOCATION'
    #: The applied services of the organization level.
    organization = 'ORGANIZATION'


class AppliedServiceTranslationPattern(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[TranslationPatternConfigurationLevel] = None
    #: Name given to a translation pattern.
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern.
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern.
    replacement_pattern: Optional[str] = None
    #: The original called number.
    matched_number: Optional[str] = None
    #: The modified number after matching against `matchingPattern` and replacing with corresponding
    #: `replacementPattern`.
    translated_number: Optional[str] = None


class ConfigurationLevel(str, Enum):
    #: The applied services at the location level.
    location = 'LOCATION'
    #: The applied services at the user level.
    # user = 'USER' - seems like this is actually PEOPLE?; issue # 178
    #: The applied services at the place level.
    place = 'PLACE'
    #: The applied services at the virtual line level.
    virtual_line = 'VIRTUAL_LINE'
    people = 'PEOPLE'


class CallInterceptDetailsPermission(str, Enum):
    #: Call intercept is disabled.
    disallow = 'DISALLOW'
    #: Call intercept is transferred to a number.
    transfer = 'TRANSFER'


class CallInterceptDetails(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevel] = None
    #: The choices that indicate call intercept permissions.
    permission: Optional[CallInterceptDetailsPermission] = None
    #: The number to which the outgoing permission by type is to be transferred.
    transfer_number: Optional[str] = None


class CallingPlanReason(str, Enum):
    #: Calling plan gives the Fraud Containment reason.
    fraud_containment = 'FRAUD_CONTAINMENT'
    #: The Cisco calling plan reason.
    cisco_calling_plan = 'CISCO_CALLING_PLAN'
    #: The reason if the transfer number 1 is not configured.
    transfer_number_1_not_configured = 'TRANSFER_NUMBER_1_NOT_CONFIGURED'
    #: The reason if the transfer number 2 is not configured.
    transfer_number_2_not_configured = 'TRANSFER_NUMBER_2_NOT_CONFIGURED'
    #: The reason if the transfer number 3 is not configured.
    transfer_number_3_not_configured = 'TRANSFER_NUMBER_3_NOT_CONFIGURED'
    #: The reason for Webex mobile international transfer forward.
    webex_mobile_premium_international_transfer_forward = 'WEBEX_MOBILE_PREMIUM_INTERNATIONAL_TRANSFER_FORWARD'


class OutgoingCallingPlanPermissionsByType(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevel] = None
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[str] = None
    #: Action to be performed on the input number that matches with the OCP.
    permission: Optional[Action] = None
    #: The number to which the outgoing permission by type is to be transferred.
    transfer_number: Optional[str] = None
    #: The reason for the result reported for non-standard OCP service.
    reason: Optional[CallingPlanReason] = None
    #: A transfer number is present in case it gets transferred to some other number.
    number: Optional[str] = None


class OutgoingCallingPlanPermissionsByDigitPattern(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevel] = None
    #: Name given to a digit pattern.
    name: Optional[str] = None
    #: Action to be performed on the input number that matches with the digit pattern.
    permission: Optional[Action] = None
    transfer_number: Optional[str] = None
    #: Pattern is given to a digit pattern.
    pattern: Optional[str] = None
    #: The reason for the result reported for non-standard OCP service.
    reason: Optional[CallingPlanReason] = None
    #: A transfer number is present in case it gets transferred to some other number.
    number: Optional[str] = None


class AppliedService(ApiModel):
    #: Returns the details of the Translation Pattern if applied.
    translation_pattern: Optional[AppliedServiceTranslationPattern] = None
    #: Returns the details of call intercept if applied.
    intercept_details: Optional[CallInterceptDetails] = None
    #: Returns the details of permissions by type configuration if applied under OCP.
    outgoing_calling_plan_permissions_by_type: Optional[OutgoingCallingPlanPermissionsByType] = None
    #: Returns the details of digit pattern configuration if applied under OCP.
    outgoing_calling_plan_permissions_by_digit_pattern: Optional[OutgoingCallingPlanPermissionsByDigitPattern] = None


class TestCallRoutingResult(ApiModel):
    #: Language for call queue.
    language: Optional[str] = None
    #: Time zone for the call queue.
    time_zone: Optional[str] = None
    #: This data object is only returned when originatorNumber is specified in the request.
    call_source_info: Optional[CallSourceInfo] = None
    #: Matching destination type for the call.
    destination_type: DestinationType
    #: FAC code if destinationType is FAC. The routing address will be returned for all other destination types.
    routing_address: str
    #: Outside access code.
    outside_access_code: Optional[str] = None
    #: true if the call would be rejected.
    is_rejected: bool
    #: Calling line ID (CLID) configured for the calling user.
    calling_line_id: Optional[str] = Field(alias='callingLineID', default=None)
    #: Routing profile that is used to route network calls.
    routing_profile: Optional[str] = None
    #: This data object is returned when destinationType is HOSTED_USER.
    hosted_user: Optional[HostedUserDestination] = Field(alias='hostedAgent', default=None)
    #: This data object is returned when destinationType is HOSTED_FEATURE.
    hosted_feature: Optional[HostedFeatureDestination] = None
    #: This data object is returned when destinationType is PBX_USER.
    pbx_user: Optional[PbxUserDestination] = None
    #: This data object is returned when destinationType is PSTN_NUMBER.
    pstn_number: Optional[PstnNumberDestination] = None
    #: This data object is returned when destinationType is VIRTUAL_EXTENSION.
    virtual_extension: Optional[VirtualExtensionDestination] = None
    #: Returned when destinationType is VIRTUAL_EXTENSION_RANGE.
    virtual_extension_range: Optional[VirtualExtensionRange] = None
    #: This data object is returned when destinationType is ROUTE_LIST.
    route_list: Optional[RouteListDestination] = None
    #: This data object is returned when destinationType is FAC.
    feature_access_code: Optional[FeatureAccessCodeDestination] = None
    #: This data object is returned when destinationType is EMERGENCY.
    emergency: Optional[EmergencyDestination] = None
    #: This data object is returned when destinationType is REPAIR.
    repair: Optional[TrunkDestination] = None
    #: This data object is returned when destinationType is UNKNOWN_EXTENSION.
    unknown_extension: Optional[TrunkDestination] = None
    #: This data object is returned when destinationType is UNKNOWN_NUMBER.
    unknown_number: Optional[TrunkDestination] = None
    #: Returned if any origin is configured with intercept details, outgoing permissions by type, digit pattern, or
    #: translation pattern.
    applied_services: Optional[list[AppliedService]] = None


class DeviceType(str, Enum):
    mpp = 'MPP'
    ata = 'ATA'
    generic_sip = 'GENERIC_SIP'
    esim = 'ESIM'
    desk_phone = 'DESK_PHONE'


class DeviceManufacturer(str, Enum):
    cisco = 'CISCO'
    third_party = 'THIRD_PARTY'


class DeviceManagedBy(str, Enum):
    cisco = 'CISCO'
    customer = 'CUSTOMER'
    partner = 'PARTNER'


class OnboardingMethod(str, Enum):
    mac_address = 'MAC_ADDRESS'
    activation_code = 'ACTIVATION_CODE'
    no_method = 'NONE'


class DeviceSettingsConfiguration(str, Enum):
    #: Devices which supports Webex Calling Device Settings Configuration.
    webex_calling_device_configuration = 'WEBEX_CALLING_DEVICE_CONFIGURATION'
    #: Devices which supports Webex Device Settings Configuration.
    webex_device_configuration = 'WEBEX_DEVICE_CONFIGURATION'
    #: Devices does not support any configuration.
    none_ = 'NONE'


class SupportedDevice(ApiModel):
    #: Model name of the device.
    model: str
    #: Display name of the device.
    display_name: str
    #: Type of the device.
    device_type: DeviceType = Field(alias='type')
    #: Manufacturer of the device.
    manufacturer: DeviceManufacturer
    #: Users who manage the device.
    managed_by: DeviceManagedBy
    #: List of places the device is supported for.
    supported_for: list[UserType]
    #: Onboarding method.
    onboarding_method: list[OnboardingMethod]
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: bool
    #: Number of port lines.
    number_of_line_ports: int
    #: Indicates whether Kem support is enabled or not.
    kem_support_enabled: bool
    #: Module count.
    kem_module_count: Optional[int] = None
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[str]] = None
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool] = None
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str] = None
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool] = None
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool] = None
    #: Enables / disables customized behavior support on devices
    customized_behaviors_enabled: Optional[bool] = None
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool] = None
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool] = None
    #: Supports touch screen on device.
    touch_screen_phone: Optional[bool] = None
    supports_line_port_reordering_enabled: Optional[bool] = None
    port_number_support_enabled: Optional[bool] = None
    t38_enabled: Optional[bool] = None
    call_declined_enabled: Optional[bool] = None
    #: Device settings configuration.
    device_settings_configuration: Optional[DeviceSettingsConfiguration] = None


class AnnouncementLanguage(ApiModel):
    #: Language name.
    name: Optional[str] = None
    #: Language Code
    code: Optional[str] = None


class SupportedDevices(ApiModel):
    upgrade_channel_list: Optional[list[str]] = None
    devices: Optional[list[SupportedDevice]] = None


@dataclass(init=False)
class TelephonyApi(ApiChild, base='telephony/config'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes at location level
    access_codes: LocationAccessCodesApi
    announcements_repo: AnnouncementsRepositoryApi
    auto_attendant: AutoAttendantApi
    #: location call intercept settings
    call_intercept: LocationInterceptApi
    call_routing: CallRoutingApi
    calls: CallsApi
    callpark: CallParkApi
    callpark_extension: CallparkExtensionApi
    callqueue: CallQueueApi
    call_recording: CallRecordingSettingsApi
    conference: ConferenceControlsApi
    dect_devices: DECTDevicesApi
    #: WxC device operations
    devices: TelephonyDevicesApi
    huntgroup: HuntGroupApi
    jobs: JobsApi
    #: location specific settings
    location: TelephonyLocationApi
    locations: TelephonyLocationApi
    #: organisation access codes
    organisation_access_codes: OrganisationAccessCodesApi
    #: organisation voicemail settings
    organisation_voicemail: OrganisationVoicemailSettingsAPI
    paging: PagingApi
    #: location level outgoing permissions
    permissions_out: OutgoingPermissionsApi
    pickup: CallPickupApi
    playlist: PlayListApi
    pnc: PrivateNetworkConnectApi
    prem_pstn: PremisePstnApi
    schedules: ScheduleApi
    supervisors: SupervisorApi
    virtual_lines: VirtualLinesApi
    # location voicemail groups
    voicemail_groups: VoicemailGroupsApi
    voicemail_rules: VoicemailRulesApi
    voice_messaging: VoiceMessagingApi
    voiceportal: VoicePortalApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.access_codes = LocationAccessCodesApi(session=session)
        self.announcements_repo = AnnouncementsRepositoryApi(session=session)
        self.auto_attendant = AutoAttendantApi(session=session)
        self.call_intercept = LocationInterceptApi(session=session)
        self.call_routing = CallRoutingApi(session=session)
        self.call_recording = CallRecordingSettingsApi(session=session)
        self.calls = CallsApi(session=session)
        self.callpark = CallParkApi(session=session)
        self.callpark_extension = CallparkExtensionApi(session=session)
        self.callqueue = CallQueueApi(session=session)
        self.conference = ConferenceControlsApi(session=session)
        self.dect_devices = DECTDevicesApi(session=session)
        self.devices = TelephonyDevicesApi(session=session)
        self.huntgroup = HuntGroupApi(session=session)
        self.jobs = JobsApi(session=session)
        self.location = TelephonyLocationApi(session=session)
        self.locations = self.location
        self.organisation_access_codes = OrganisationAccessCodesApi(session=session)
        self.organisation_voicemail = OrganisationVoicemailSettingsAPI(session=session)
        self.paging = PagingApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session, selector=ApiSelector.location)
        self.pickup = CallPickupApi(session=session)
        self.playlist = PlayListApi(session=session)
        self.pnc = PrivateNetworkConnectApi(session=session)
        self.prem_pstn = PremisePstnApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.supervisors = SupervisorApi(session=session)
        self.virtual_lines = VirtualLinesApi(session=session)
        self.voicemail_groups = VoicemailGroupsApi(session=session)
        self.voicemail_rules = VoicemailRulesApi(session=session)
        self.voice_messaging = VoiceMessagingApi(session=session)
        self.voiceportal = VoicePortalApi(session=session)

    def phone_numbers(self, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, details: bool = None, toll_free_numbers: bool = None,
                      restricted_non_geo_numbers: bool = None,
                      included_telephony_type: TelephonyType = None,
                      org_id: str = None, **params) -> Generator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool
        :param included_telephony_type: Returns the list of phone numbers that are of given `includedTelephonyType`.
            By default if this query parameter is not provided, it will list both PSTN and Mobile Numbers. Possible
            input values are PSTN_NUMBER, MOBILE_NUMBER.
        :type included_telephony_type: TelephonyType
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        # parameter is actually called included_telephony_types
        if itp := params.pop('includedTelephonyType', None):
            params['includedTelephonyTypes'] = itp
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='numbers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')

    def phone_number_details(self, org_id: str = None) -> NumberDetails:
        """
        get summary (counts) of phone numbers

        :param org_id: detaild for numbers in this organization.
        :type org_id: str
        :return: phone number details
        :rtype: :class:`NumberDetails`
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        params['details'] = 'true'
        params['max'] = 1
        url = self.ep(path='numbers')
        data = self.get(url, params=params)
        return NumberDetails.model_validate(data['count'])

    def validate_extensions(self, extensions: list[str]) -> ValidateExtensionsResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions. Retrieving this list requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param extensions: Array of Strings of ID of Extensions.
        :type extensions: list[str]
        :return: validation response
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(path='actions/validateExtensions/invoke')
        data = self.post(url, json={'extensions': extensions})
        return ValidateExtensionsResponse.model_validate(data)

    def validate_phone_numbers(self, phone_numbers: list[str], org_id: str = None) -> ValidatePhoneNumbersResponse:
        """
        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Validating a phone number in an organization requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param phone_numbers: List of phone numbers to be validated.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: validation result
        :rtype: :class:`wxc_sdk.common.ValidatePhoneNumbersResponse`
        """
        url = self.ep('actions/validateNumbers/invoke')
        body = {'phoneNumbers': phone_numbers}
        params = org_id and {'orgId': org_id} or None
        data = self.post(url=url, params=params, json=body)
        return ValidatePhoneNumbersResponse.model_validate(data)

    def ucm_profiles(self, org_id: str = None) -> list[UCMProfile]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in
        Webex Teams (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the
        user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :return: list of :class:`UCMProfile`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(path='callingProfiles')
        data = self.get(url, params=params)
        return TypeAdapter(list[UCMProfile]).validate_python(data['callingProfiles'])

    def route_choices(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> Generator[RouteIdentity, None, None]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('routeChoices')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')

    def test_call_routing(self, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, include_applied_services: bool = None,
                          org_id: str = None) -> TestCallRoutingResult:
        """
        Test Call Routing

        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Test call routing requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param originator_id: This element is used to identify the originating party. It can be a person ID or a trunk
            ID.
        :type originator_id: str
        :param originator_type: This element is used to identify if the `originatorId` is of type `PEOPLE` or `TRUNK`.
        :type originator_type: OriginatorType
        :param destination: This element specifies the called party. It can be any dialable string, for example, an ESN
            number, E.164 number, hosted user DN, extension, extension with location code, URL, or FAC code.
        :type destination: str
        :param originator_number: Only used when `originatorType` is `TRUNK`. The `originatorNumber` can be a phone
            number or URI.
        :type originator_number: str
        :param include_applied_services: This element is used to retrieve if any translation pattern, call intercept,
            permission by type, or permission by digit pattern is present for the called party.
        :type include_applied_services: bool
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :rtype: :class:`TestCallRoutingResult`
        """
        params = org_id and {'orgId': org_id} or None
        body = dict()
        body['originatorId'] = originator_id
        body['originatorType'] = enum_str(originator_type)
        if originator_number is not None:
            body['originatorNumber'] = originator_number
        body['destination'] = destination
        if include_applied_services is not None:
            body['includeAppliedServices'] = include_applied_services
        url = self.ep('actions/testCallRouting/invoke')
        data = self.post(url=url, params=params, json=body)
        return TestCallRoutingResult.model_validate(data)

    def supported_devices(self, org_id: str = None) -> SupportedDevices:
        """
        Gets the list of supported devices for an organization location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization
        :return: List of supported devices
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('supportedDevices')
        data = self.get(url=url, params=params)
        return SupportedDevices.model_validate(data)

    def device_settings(self, org_id: str = None) -> DeviceCustomization:
        """
        Get device override settings for an organization.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization location.
        :type org_id: str
        :return: device customization response
        :rtype: DeviceCustomization
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('devices/settings')
        data = self.get(url=url, params=params)
        return DeviceCustomization.model_validate(data)

    def read_list_of_announcement_languages(self) -> list[AnnouncementLanguage]:
        """
        List all languages supported by Webex Calling for announcements and voice prompts.
        Retrieving announcement languages requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of
        -announcement-languages
        """
        url = self.ep('announcementLanguages')
        data = super().get(url=url)
        return TypeAdapter(list[AnnouncementLanguage]).validate_python(data["languages"])
