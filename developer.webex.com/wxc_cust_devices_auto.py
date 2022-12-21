from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field


__all__ = ['AcdObject', 'ActivationStates', 'AtaDtmfMethodObject', 'AtaDtmfModeObject', 'AtaObject', 'AudioCodecPriorityObject', 'BackgroundImage', 'BacklightTimerObject', 'ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse', 'CustomizationDeviceLevelObject', 'CustomizationObject', 'DectDeviceList', 'DectObject', 'DefaultLoggingLevelObject', 'DeviceObject', 'DeviceOwner', 'DeviceSettingsObjectForJob', 'Devices', 'DisplayCallqueueAgentSoftkeysObject', 'DisplayNameSelection', 'ErrorMessageObject', 'ErrorObject', 'GetChangeDeviceSettingsJobStatusResponse', 'GetDeviceMembersResponse', 'GetDeviceSettingsResponse', 'GetUserDevicesResponse', 'ItemObject', 'JobExecutionStatusObject', 'KemModuleTypeObject', 'LineKeyLEDPattern', 'LineKeyLabelSelection', 'LineType', 'ListChangeDeviceSettingsJobErrorsResponse', 'ListChangeDeviceSettingsJobsResponse', 'MacStatusObject', 'ManagedByObject', 'ManufacturerObject', 'MemberObject', 'MemberType', 'MppAudioCodecPriorityObject', 'MppObject', 'MppVlanObject', 'OnboardingMethodObject', 'PhoneLanguage', 'PutMemberObject', 'ReadDECTDeviceTypeListResponse', 'ReadListOfSupportedDevicesResponse', 'ReaddeviceOverrideSettingsFororganizationResponse', 'SearchMemberObject', 'SearchMembersResponse', 'SelectionType', 'State', 'Status', 'StepExecutionStatusesObject', 'TypeObject', 'UpdateDeviceSettingsBody', 'ValidatelistOfMACAddressResponse', 'VlanObject', 'WebexCallingOrganizationSettingswithCustomerManagedDevicesFeaturesApi', 'WifiNetworkObject']


class MemberType(ApiModel):
    #: Associated member is a person.
    people: Optional[str]
    #: Associated member is a workspace.
    place: Optional[str]


class LineType(ApiModel):
    #: Primary line for the member.
    primary: Optional[str]
    #: Shared line for the member. Shared line appearance allows users to receive and place calls to and from another user's extension, using their device.
    shared_call_appearance: Optional[str]


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    port: Optional[int]
    #: Unique identifier for the member.
    id: Optional[str]
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Choose T.38 fax compression if the device requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of the device.
    primary_owner: Optional[bool]
    #: Used to differentiate Primary or Share Call Appearance line, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a person's device behaves when a call is declined. When true, a call decline request is extended to all the endpoints on the device. When false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Device line label.
    line_label: Optional[str]


class MemberObject(PutMemberObject):
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will be supported in a future update.
    phone_number: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Registration Host IP address for the line port.
    host_ip: Optional[str]
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str]
    #: Device line port.
    line_port: Optional[str]
    #: Indicates if the member is PEOPLE or PLACE.
    member_type: Optional[MemberType]


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str]
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace.
    phone_number: Optional[str]
    #: T.38 Fax Compression setting. Only valid for ATA Devices. Choose T.38 fax compression if the device requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Used to differentiate Primary or Share Call Appearance line, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Set how a person's device behaves when a call is declined. When true, a call decline request is extended to all the endpoints on the device. When false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Indicates if member is PEOPLE or PLACE.
    member_type: Optional[MemberType]


class SelectionType(ApiModel):
    #: Indicates the regional selection type for audio codec priority.
    regional: Optional[str]
    #: Indicates the custom selection type for audio codec priority.
    custom: Optional[str]


class AudioCodecPriorityObject(ApiModel):
    #: Indicates the selection of an Audio Code Priority Object.
    selection: Optional[SelectionType]
    #: Primary Audio Code.
    primary: Optional[str]
    #: Secondary Audio Code.
    secondary: Optional[str]
    #: Tertiary Audio Code.
    tertiary: Optional[str]


class AtaDtmfModeObject(ApiModel):
    #: A DTMF digit requires extra hold time after detection, and the DTMF level threshold is raised to -20 dBm.
    strict: Optional[str]
    #: Normal threshold mode.
    normal: Optional[str]


class AtaDtmfMethodObject(ApiModel):
    #: Sends DTMF by using the audio path.
    inband: Optional[str]
    #: Audio video transport. Sends DTMF as AVT events.
    avt: Optional[str]
    #: Uses InBand or AVT based on the outcome of codec negotiation.
    auto: Optional[str]


class VlanObject(ApiModel):
    #: If true, the VLAN object of an ATA is enabled.
    enabled: Optional[bool]
    #: The value of the VLAN Object of DECT.
    value: Optional[int]


class AtaObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject]
    #: DTMF Detection Tx Mode selection for Cisco ATA devices.
    ata_dtmf_mode: Optional[AtaDtmfModeObject]
    #: Method for transmitting DTMF signals to the far end.
    ata_dtmf_method: Optional[AtaDtmfMethodObject]
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: Optional[bool]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[VlanObject]


class MppAudioCodecPriorityObject(ApiModel):
    #: Selection of the Audio Code Priority Object for an MPP object.
    selection: Optional[str]
    #: Primary Audio Code for an MPP object.
    primary: Optional[str]
    #: Secondary Audio Code for an MPP object.
    secondary: Optional[str]
    #: Tertiary Audio Code for an MPP object.
    tertiary: Optional[str]


class BacklightTimerObject(ApiModel):
    one_m: Optional[str]
    five_m: Optional[str]
    thirty_m: Optional[str]
    always_on: Optional[str]
    off: Optional[str]
    ten_s: Optional[str]
    twenty_s: Optional[str]
    thirty_s: Optional[str]


class BackgroundImage(ApiModel):
    #: No background image is set for the devices.
    none: Optional[str]
    #: A dark blue background image is set for the devices.
    dark_blue: Optional[str]
    #: The Cisco-themed dark blue background image is set for the devices.
    cisco_dark_blue: Optional[str]
    #: The Cisco Webex dark blue background image is set for the devices.
    webex_dark_blue: Optional[str]
    #: A custom background image is set for the devices.
    custom_background: Optional[str]
    #: When this option is selected, a field 'Custom Background URL' needs to be added with an image URL. URLs provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url: Optional[str]


class DisplayNameSelection(ApiModel):
    #: Devices display the person’s phone number, or if the person doesn’t have a phone number, the location number.
    person_number: Optional[str]
    #: Devices display the name in first name/last name format.
    person_first_then_last_name: Optional[str]
    #: Devices display the name in last name/first name format.
    person_last_then_first_name: Optional[str]


class DefaultLoggingLevelObject(ApiModel):
    #: Enables standard logging.
    standard: Optional[str]
    #: Enables detailed debugging logging.
    debugging: Optional[str]


class DisplayCallqueueAgentSoftkeysObject(ApiModel):
    front_page: Optional[str]
    last_page: Optional[str]


class AcdObject(ApiModel):
    #: If true the ACD object is enabled.
    enabled: Optional[bool]
    #: Call queue agent soft key value of an ACD object.
    display_callqueue_agent_softkeys: Optional[str]


class LineKeyLabelSelection(ApiModel):
    #: Displays the person's extension, or if the person doesn’t have an extension, the person’s first name.
    person_extension: Optional[str]
    #: Devices display the name in first name/last name format.
    person_first_then_last_name: Optional[str]
    #: Devices display the name in last name/first name format.
    person_last_then_first_name: Optional[str]


class LineKeyLEDPattern(ApiModel):
    default: Optional[str]
    preset_1: Optional[str]


class PhoneLanguage(ApiModel):
    #: Indicates a person's announcement language.
    person_language: Optional[str]
    arabic: Optional[str]
    bulgarian: Optional[str]
    catalan: Optional[str]
    chinese_simplified: Optional[str]
    chinese_traditional: Optional[str]
    croatian: Optional[str]
    czech: Optional[str]
    danish: Optional[str]
    dutch: Optional[str]
    english_united_states: Optional[str]
    english_united_kingdom: Optional[str]
    finnish: Optional[str]
    french_canada: Optional[str]
    french_france: Optional[str]
    german: Optional[str]
    greek: Optional[str]
    hebrew: Optional[str]
    hungarian: Optional[str]
    italian: Optional[str]
    japanese: Optional[str]
    korean: Optional[str]
    norwegian: Optional[str]
    polish: Optional[str]
    portuguese_portugal: Optional[str]
    russian: Optional[str]
    spanish_colombia: Optional[str]
    spanish_spain: Optional[str]
    slovak: Optional[str]
    swedish: Optional[str]
    slovenian: Optional[str]
    turkish: Optional[str]
    ukraine: Optional[str]


class MppVlanObject(VlanObject):
    #: PC port value of a VLAN object for an MPP object.
    pc_port: Optional[int]


class WifiNetworkObject(ApiModel):
    #: If true, the wifi network is enabled.
    enabled: Optional[bool]
    #: Authentication method of wifi network.
    authentication_method: Optional[str]
    #: SSID name of the wifi network.
    ssid_name: Optional[str]
    #: User ID for the wifi network.
    user_id: Optional[str]


class MppObject(ApiModel):
    #: Indicates whether PNAC of MPP object is enabled or not.
    pnac_enabled: Optional[bool]
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[MppAudioCodecPriorityObject]
    #: Choose the length of time (in minutes) for the phone’s backlight to remain on.
    backlight_timer: Optional[BacklightTimerObject]
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage]
    #: The display name that appears on the phone screen.
    display_name_selection: Optional[DisplayNameSelection]
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool]
    #: Choose the desired logging level for an MPP devices.
    default_logging_level: Optional[DefaultLoggingLevelObject]
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    dnd_services_enabled: Optional[bool]
    #: Chooses the location of the Call Queue Agent Login/Logout softkey on Multi-Platform Phones.
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkeysObject]
    #: Choose the duration (in hours) of Hoteling guest login.
    hoteling_guest_association_timer: Optional[int]
    #: Holds Acd object value.
    acd: Optional[AcdObject]
    #: Indicates the short inter digit timer value.
    short_interdigit_timer: Optional[int]
    #: Indicates the long inter digit timer value..
    long_interdigit_timer: Optional[int]
    #: Line key labels define the format of what’s shown next to line keys.
    line_key_label_format: Optional[LineKeyLabelSelection]
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note – This parameter is not supported on the MPP 8875
    line_key_led_pattern: Optional[LineKeyLEDPattern]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: Optional[bool]
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]]
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: Optional[int]
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your provisioned location.
    phone_language: Optional[PhoneLanguage]
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[str]
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify the amount of inactive time needed (in seconds) before the phone’s screen saver activates.
    screen_timeout: Optional[VlanObject]
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    usb_ports_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObject]
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObject]


class CustomizationDeviceLevelObject(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObject]
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObject]


class UpdateDeviceSettingsBody(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObject]
    #: Indicates if customization is allowed at a location level. If true, customization is allowed at a location level. If false, the customer-level configuration is used.
    customization_enabled: Optional[bool]


class GetDeviceSettingsResponse(UpdateDeviceSettingsBody):
    #: Customer devices setting update status. If true, an update is in progress (no further changes are allowed). If false, no update in progress (changes are allowed).
    update_in_progress: Optional[bool]
    #: Number of devices that will be updated.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class DeviceOwner(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str]
    #: Enumeration that indicates if the member is of type PEOPLE or PLACE.
    type: Optional[MemberType]
    #: First name of the device owner.
    first_name: Optional[str]
    #: Last name of the device owner.
    last_name: Optional[str]


class ActivationStates(ApiModel):
    #: Indicates a device is activating.
    activating: Optional[str]
    #: Indicates a device is activated.
    activated: Optional[str]
    #: Indicates a device is deactivated.
    deactivated: Optional[str]


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str]
    #: Comma separated array of tags used to describe device.
    descriptions: Optional[list[str]]
    #: Identifier for device model.
    model: Optional[str]
    #: MAC address of device.
    mac: Optional[str]
    #: IP address of device.
    ip_address: Optional[str]
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of the device.
    primary_owner: Optional[bool]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType]
    #: Owner of the device.
    owner: Optional[DeviceOwner]
    #: Activation state of device.
    activation_state: Optional[ActivationStates]


class TypeObject(ApiModel):
    #: Cisco Multiplatform Phone
    mpp: Optional[str]
    #: Analog Telephone Adapters
    ata: Optional[str]
    #: GENERIC Session Initiation Protocol
    generic_sip: Optional[str]
    #: Esim Supported Webex Go
    esim: Optional[str]


class ManufacturerObject(ApiModel):
    #: Devices manufactured by Cisco
    cisco: Optional[str]
    #: Devices manufactured by third-party that are approved by Cisco account manager to be enabled for provisioning in the control hub.
    third_party: Optional[str]


class ManagedByObject(ApiModel):
    #: Devices managed by Cisco.
    cisco: Optional[str]
    #: Devices managed by customer that are approved by Cisco account manager to be enabled for provisioning in the control hub.
    customer: Optional[str]


class OnboardingMethodObject(ApiModel):
    mac_address: Optional[str]
    activation_code: Optional[str]
    none: Optional[str]


class KemModuleTypeObject(ApiModel):
    kem_14_keys: Optional[str]
    kem_18_keys: Optional[str]


class DeviceObject(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Indicates the display name of the device.
    display_name: Optional[str]
    #: Indicates the type of the device.
    type: Optional[TypeObject]
    #: Indicates the manufacturer of the device.
    manufacturer: Optional[ManufacturerObject]
    #: Indicates the users by whom the device is managed by.
    managed_by: Optional[ManagedByObject]
    #: Indicates the list of places the device is supported for.
    supported_for: Optional[list[MemberType]]
    #: Indicates the onboarding method.
    onboarding_method: Optional[list[OnboardingMethodObject]]
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: Optional[bool]
    #: Indicates the number of port lines.
    number_of_line_ports: Optional[int]
    #: Indicates whether Kem support is enabled or not.
    kem_support_enabled: Optional[bool]
    #: Indicates the module count.
    kem_module_count: Optional[int]
    #: Indicates the key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleTypeObject]]
    #: Enables / Disables upgrade channel.
    upgrade_channel_enabled: Optional[bool]
    #: Indicates the default upgrade channel.
    default_upgrade_channel: Optional[str]
    #: Enables / disables additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool]
    #: Enables / disables basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool]
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool]
    #: Indicates whether the line port reordering is supported or not. If true line port reordering is supported.
    supports_line_port_reordering_enabled: Optional[bool]


class DectObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[MppAudioCodecPriorityObject]
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: Optional[bool]
    #: Specify the destination number to be dialled from the DECT Handset top button when pressed.
    dect6825_handset_emergency_number: Optional[str]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Specify up to 3 multicast group URLs each with a unique listening port.
    multicast: Optional[str]
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[VlanObject]


class CustomizationObject(CustomizationDeviceLevelObject):
    #: Indicates the settings that are applicable to DECT devices.
    dect: Optional[DectObject]


class DectDeviceList(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Display name of the device.
    display_name: Optional[str]
    #: Number of base stations.
    number_of_base_stations: Optional[int]
    #: Number of port lines.
    number_of_line_ports: Optional[int]
    #: Number of supported registrations.
    number_of_registrations_supported: Optional[int]


class Status(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class State(str, Enum):
    #: The requested MAC address is available.
    available = 'AVAILABLE'
    #: The requested MAC address is unavailable.
    unavailable = 'UNAVAILABLE'
    #: The requested MAC address is duplicated.
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    #: The requested MAC address is invalid.
    invalid = 'INVALID'


class MacStatusObject(ApiModel):
    #: MAC address.
    mac: Optional[str]
    #: State of the MAC address.
    state: Optional[State]
    #: Error code of the MAC address validation.
    error_code: Optional[int]
    #: Provides a status message about the MAC address.
    message: Optional[str]


class DeviceSettingsObjectForJob(ApiModel):
    #: Background image settings for the devices. Only works on phones that have an 800x480 screen size
    background_image: Optional[BackgroundImage]
    #: The display name that appears on the phone screen.
    display_name_selection: Optional[DisplayNameSelection]
    #: Line key labels define the format of what’s shown next to line keys.
    line_key_label_selection: Optional[LineKeyLabelSelection]
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note – This parameter is not supported on the MPP 8875.
    line_key_led_pattern: Optional[LineKeyLEDPattern]


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier for a step in the job.
    id: Optional[int]
    #: Step execution start time.
    start_time: Optional[str]
    #: Step execution end time.
    end_time: Optional[str]
    #: Last updated time for a step.
    last_updated: Optional[str]
    #: Displays status for a step.
    status_message: Optional[str]
    #: Exit code for a step.
    exit_code: Optional[str]
    #: Step name.
    name: Optional[str]
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str]


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int]
    #: Last updated time post one of the step execution completion.
    last_updated: Optional[str]
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str]
    #: Exit code for a job.
    exit_code: Optional[str]
    #: Job creation time.
    created_time: Optional[str]
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str]
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse(ApiModel):
    #: Job name.
    name: Optional[str]
    #: Unique identifier of the job.
    id: Optional[str]
    #: Job type.
    job_type: Optional[str]
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str]
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str]
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str]
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str]
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int]
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involve in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, or FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: If true, all the devices within this location will be customized with new requested customizations. If false, devices are customized at the organization level. No effect when the job is triggered at the organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates if the job was run at an organization level or location level.
    target: Optional[str]
    #: Unique location identifier for which the job was run.
    location_id: Optional[str]
    #: Displays job completion percentage.
    percentage_complete: Optional[str]


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str]
    #: Internal error code.
    code: Optional[str]
    #: Error message describing the location or point of failure.
    location: Optional[str]


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str]
    #: An error message with further details.
    message: Optional[list[ErrorMessageObject]]


class ItemObject(ApiModel):
    #: Index of the item number.
    item_number: Optional[int]
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str]
    #: An error object.
    error: Optional[ErrorObject]


class GetDeviceMembersResponse(ApiModel):
    #: Model type of the device.
    model: Optional[str]
    #: List of members that appear on the device.
    members: Optional[list[MemberObject]]
    #: Maximum number of lines available for the device.
    max_line_count: Optional[int]


class UpdateMembersOndeviceBody(ApiModel):
    #: If the member's list is missing then all the users are removed except the primary user.
    members: Optional[list[PutMemberObject]]


class SearchMembersResponse(ApiModel):
    #: List of members available for the device.
    members: Optional[list[SearchMemberObject]]


class GetUserDevicesResponse(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int]


class ReadListOfSupportedDevicesResponse(ApiModel):
    #: List of supported devices.
    devices: Optional[list[DeviceObject]]


class ReaddeviceOverrideSettingsFororganizationResponse(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationObject]
    #: Indicates the progress of the device update.
    update_in_progress: Optional[bool]
    #: Indicates the device count.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class ReadDECTDeviceTypeListResponse(ApiModel):
    #: Contains a list of devices.
    devices: Optional[list[DectDeviceList]]


class ValidatelistOfMACAddressResponse(ApiModel):
    #: Status of the MAC address.
    status: Optional[Status]
    #: Contains array of all the MAc address provided and their statuses.
    mac_status: Optional[list[MacStatusObject]]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobBody(ApiModel):
    #: ID of the location in which the devices reside.
    location_id: Optional[str]
    #: If 'true', all the devices within this location will be customized with new requested customizations. If 'false', devices are customized at the organization level. No effect when the job is triggered at the organization level.
    location_customizations_enabled: Optional[bool]
    #: 'deviceSettings' properties for the devices.
    device_settings: Optional[DeviceSettingsObjectForJob]
    #: Settings for ATA, DECT, and MPP devices.
    customizations: Optional[CustomizationObject]


class ListChangeDeviceSettingsJobsResponse(ApiModel):
    #: Lists all jobs for jobType 'calldevicesettings' for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse]]


class GetChangeDeviceSettingsJobStatusResponse(ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse):
    #: Count of the number of devices that were modified by the job.
    device_count: Optional[int]


class ListChangeDeviceSettingsJobErrorsResponse(ApiModel):
    items: Optional[list[ItemObject]]


class WebexCallingOrganizationSettingswithCustomerManagedDevicesFeaturesApi(ApiChild, base=''):
    """
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
    Modifying these organization settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query parameter.
    """

    def members(self, device_id: str, org_id: str = None) -> GetDeviceMembersResponse:
        """
        Get the list of all the members of the device including primary and secondary users.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify member details and 
        search for available members on a device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/devices/{device_id}/members')
        data = super().get(url=url, params=params)
        return GetDeviceMembersResponse.parse_obj(data)

    def update_members_ondevice(self, device_id: str, org_id: str = None, members: PutMemberObject = None):
        """
        Modify member details on the device.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify member details and
        search for available members on a device.
        Modifying members on the device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        :param members: If the member's list is missing then all the users are removed except the primary user.
        :type members: PutMemberObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if members is not None:
            body['members'] = members
        url = self.ep(f'telephony/config/devices/{device_id}/members')
        super().put(url=url, params=params, json=body)
        return

    def search_members(self, device_id: str, location_id: str, org_id: str = None, start: int = None, max: int = None, member_name: str = None, phone_number: str = None, extension: str = None) -> List[SearchMemberObject]:
        """
        Search members that can be assigned to the device.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify member details and
        search for available members on a device.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param max: Specifies the maximum number of records that you want to fetch.
        :type max: int
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        """
        params = {}
        if location_id is not None:
            params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        if max is not None:
            params['max'] = max
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/devices/{device_id}/availableMembers')
        data = super().get(url=url, params=params)
        return data["members"]

    def apply_changes_forspecific(self, device_id: str, org_id: str = None):
        """
        Issues request to the device to download and apply changes to the configuration.
        Applying changes for a specific device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/devices/{device_id}/actions/applyChanges/invoke')
        super().post(url=url, params=params)
        return

    def settings(self, device_id: str, org_id: str = None, device_model: str = None) -> GetDeviceSettingsResponse:
        """
        Get override settings for a device.
        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin can also modify the settings. DECT devices do not support settings at the device level.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        url = self.ep(f'telephony/config/devices/{device_id}/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def location_settings(self, location_id: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get device override settings for a location.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location
        :type location_id: str
        :param org_id: ID of the organization to which the location belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/locations/{location_id}/devices/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def update_settings(self, device_id: str, customizations: CustomizationDeviceLevelObject, customization_enabled: bool, org_id: str = None, device_model: str = None):
        """
        Modify override settings for a device.
        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admin can also modify the settings. DECT devices do not support settings at the device level.
        Updating settings on the device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObject
        :param customization_enabled: Indicates if customization is allowed at a location level. If true, customization is allowed at a location level. If false, the customer-level configuration is used.
        :type customization_enabled: bool
        :param org_id: ID of the organization to which the device belongs.
        :type org_id: str
        :param device_model: Device model.
        :type device_model: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        body = {}
        if customizations is not None:
            body['customizations'] = customizations
        if customization_enabled is not None:
            body['customizationEnabled'] = customization_enabled
        url = self.ep(f'telephony/config/devices/{device_id}/settings')
        super().put(url=url, params=params, json=body)
        return

    def user(self, person_id: str, org_id: str = None) -> GetUserDevicesResponse:
        """
        Get all devices for a person.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person to retrieve devices for.
        :type person_id: str
        :param org_id: ID of the organization to which the person belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/devices')
        data = super().get(url=url, params=params)
        return GetUserDevicesResponse.parse_obj(data)

    def read_list_of_supported(self, org_id: str = None) -> List[DeviceObject]:
        """
        Gets the list of supported devices for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: ID of the organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/supportedDevices')
        data = super().get(url=url, params=params)
        return data["devices"]

    def readdevice_override_settings_fororganization(self, org_id: str = None) -> ReaddeviceOverrideSettingsFororganizationResponse:
        """
        Get device override settings for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: ID of the organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/devices/settings')
        data = super().get(url=url, params=params)
        return ReaddeviceOverrideSettingsFororganizationResponse.parse_obj(data)

    def read_dect_type_list(self, org_id: ) -> List[DectDeviceList]:
        """
        Get DECT device type list with base stations and line ports supported count. This is a static list.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: ID of the organization to which the DECT device belongs.
        :type org_id: 
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/devices/dects/supportedDevices')
        data = super().get(url=url, params=params)
        return data["devices"]

    def validatelist_of_mac_address(self, org_id: str = None) -> ValidatelistOfMACAddressResponse:
        """
        Validate a list of MAC addresses.
        Validating this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: ID of the organization to which the MAC addresses validated.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/devices/actions/validateMacs/invoke')
        data = super().post(url=url, params=params)
        return ValidatelistOfMACAddressResponse.parse_obj(data)

    def change_settings_across_organization_or_location_job(self, org_id: str = None, location_id: str = None, location_customizations_enabled: bool = None, device_settings: DeviceSettingsObjectForJob = None, customizations: CustomizationObject = None) -> ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse:
        """
        Change device settings across organizations or locations: Performs bulk and asynchronous processing for all types of device settings initiated by organization and system admins in a stateful persistent manner. The job will modify the requested device settings across all the devices. Whenever the location ID is specified in the request, it modifies the requested device settings only for the devices that are part of the provided location within an organization.
        Returns a unique job id which can then be utilized further to retrieve status and errors for the same.
        Only one job per customer can be running at any given time within the same organization. An attempt to run multiple jobs at the same time will result in a 409 error response.
        Running this job requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: ID of the organization containing the devices for which the settings are to be changed.
        :type org_id: str
        :param location_id: ID of the location in which the devices reside.
        :type location_id: str
        :param location_customizations_enabled: If 'true', all the devices within this location will be customized with new requested customizations. If 'false', devices are customized at the organization level. No effect when the job is triggered at the organization level.
        :type location_customizations_enabled: bool
        :param device_settings: 'deviceSettings' properties for the devices.
        :type device_settings: DeviceSettingsObjectForJob
        :param customizations: Settings for ATA, DECT, and MPP devices.
        :type customizations: CustomizationObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if location_id is not None:
            body['locationId'] = location_id
        if location_customizations_enabled is not None:
            body['locationCustomizationsEnabled'] = location_customizations_enabled
        if device_settings is not None:
            body['deviceSettings'] = device_settings
        if customizations is not None:
            body['customizations'] = customizations
        url = self.ep('telephony/config/jobs/devices/callDeviceSettings')
        data = super().post(url=url, params=params, json=body)
        return ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse.parse_obj(data)

    def list_change_settings_jobs(self, org_id: str = None, **params) -> Generator[ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse, None, None]:
        """
        List change device settings jobs.
        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to oldest one irrespective of its status.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: ID of the organization for which the list of 'calldevicesettings' jobs is retrieved.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/jobs/devices/callDeviceSettings')
        return self.session.follow_pagination(url=url, model=ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse, params=params)

    def change_settings_job_status(self, job_id: str = None) -> int:
        """
        Get change device settings job status.
        Provides details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param job_id: ID of the job for which to retrieve details.
        :type job_id: str
        """
        url = self.ep(f'telephony/config/jobs/devices/callDeviceSettings/{job_id}')
        data = super().get(url=url)
        return data["deviceCount"]

    def list_change_settings_job_errors(self, job_id: str = None, org_id: str = None, **params) -> Generator[ItemObject, None, None]:
        """
        List change device settings job errors.
        Lists all error details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param job_id: ID of the job for which to retrieve errors.
        :type job_id: str
        :param org_id: ID of the organization to which the job belongs.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'v1/telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, params=params)
