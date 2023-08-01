from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Acd', 'AcdObjectDevice', 'ActivationStates', 'AtaDtmfMethodObject', 'AtaDtmfModeObject',
           'AtaDtmfModeObject1', 'AtaObject', 'AtaObjectDevice', 'AudioCodecPriorityObjectDevice',
           'AuthenticationMethodObject', 'BackgroundImage', 'BackgroundImageColor', 'BacklightTimer68XX',
           'BacklightTimerObject', 'BacklightTimerObjectDevice', 'BluetoothObject', 'CallForwardExpandedSoftKey',
           'CallHistoryMethod', 'ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse', 'CountObject',
           'CustomizationDeviceLevelObject', 'CustomizationDeviceLevelObjectDevice', 'CustomizationObject',
           'DectDeviceList', 'DectObject', 'DefaultLoggingLevelObject', 'DefaultLoggingLevelObject1',
           'DeviceActivationStates', 'DeviceCallSettingsApi', 'DeviceObject', 'DeviceOwner', 'Devices',
           'DirectoryMethod', 'DisplayCallqueueAgentSoftkeysObject', 'DisplayCallqueueAgentSoftkeysObject1',
           'DisplayNameSelection', 'ErrorMessageObject', 'ErrorObject', 'GetChangeDeviceSettingsJobStatusResponse',
           'GetDeviceMembersResponse', 'GetDeviceSettingsResponse', 'GetLocationDeviceSettingsResponse',
           'GetUserDevicesResponse', 'GetWorkspaceDevicesResponse', 'Hoteling', 'HttpProxyObject', 'ItemObject',
           'JobExecutionStatusObject', 'JobExecutionStatusObject1', 'KemModuleTypeObject', 'LdapObject',
           'LineKeyLEDPattern', 'LineKeyLEDPattern1', 'LineType', 'ListChangeDeviceSettingsJobErrorsResponse',
           'ListChangeDeviceSettingsJobsResponse', 'Location', 'MacStatusObject', 'ManagedByObject',
           'ManufacturerObject', 'MemberObject', 'MemberType', 'Mode', 'Mode1', 'MppObject', 'MppObjectDevice',
           'MppVlanObjectDevice', 'NoiseCancellationObject', 'OnboardingMethodObject', 'PhoneLanguage', 'PlaceDevices',
           'PoeMode', 'PskObject', 'PutMemberObject', 'ReadDECTDeviceTypeListResponse',
           'ReadListOfSupportedDevicesResponse', 'ReaddeviceOverrideSettingsFororganizationResponse',
           'SearchMemberObject', 'SearchMembersResponse', 'SelectionType', 'SnmpObject', 'SoftKeyLayoutObject',
           'SoftKeyMenuObject', 'State', 'Status', 'StepExecutionStatusesObject', 'SupportedForObject', 'TypeObject',
           'UpdateDeviceSettingsBody', 'UsbPortsObject', 'ValidatelistOfMACAddressResponse', 'VlanObjectDevice',
           'VolumeSettingsObject', 'WebAccessObject', 'WifiAudioCodecPriorityObjectDevice', 'WifiNetworkObject',
           'WifiNetworkObjectDevice', 'WifiObject']


class MemberType(ApiModel):
    #: Indicates the associated member is a person.
    people: Optional[str]
    #: Indicates the associated member is a workspace.
    place: Optional[str]


class Location(ApiModel):
    #: Location identifier associated with the members.
    id: Optional[str]
    #: Location name associated with the member.
    name: Optional[str]


class LineType(ApiModel):
    #: Primary line for the member.
    primary: Optional[str]
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance: Optional[str]


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    port: Optional[int]
    #: Unique identifier for the member.
    id: Optional[str]
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of device.
    primary_owner: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Device line label.
    line_label: Optional[str]


class MemberObject(PutMemberObject):
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will
    #: be supported in a future update.
    phone_number: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Registration Host IP address for the line port.
    host_ip: Optional[str]
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str]
    #: SIP username used in SIP signaling, for example, in registration.
    line_port: Optional[str]
    #: Indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location]


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str]
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace.
    phone_number: Optional[str]
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Indicates if member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location]


class SelectionType(ApiModel):
    #: Indicates the regional selection type for audio codec priority.
    regional: Optional[str]
    #: Indicates the custom selection type for audio codec priority.
    custom: Optional[str]


class AudioCodecPriorityObjectDevice(ApiModel):
    #: Indicates the selection of an Audio Codec Priority Object.
    selection: Optional[SelectionType]
    #: Indicates the primary Audio Codec.
    primary: Optional[str]
    #: Indicates the secondary Audio Codec.
    secondary: Optional[str]
    #: Indicates the tertiary Audio Codec.
    tertiary: Optional[str]


class AtaDtmfModeObject(ApiModel):
    #: Normal threshold mode.
    normal: Optional[str]


class AtaDtmfMethodObject(ApiModel):
    #: Audio video transport. Sends DTMF as AVT events.
    avt: Optional[str]
    #: Uses InBand or AVT based on the outcome of codec negotiation.
    auto: Optional[str]


class VlanObjectDevice(ApiModel):
    #: Denotes whether the VLAN object of an ATA is enabled.
    enabled: Optional[bool]
    #: The value of the VLAN Object of an ATA object.
    value: Optional[int]


class SnmpObject(ApiModel):
    #: Denotes whether the Simple Network Management Protocol of an ATA is enabled.
    enabled: Optional[bool]
    #: Trusted IPv4 address and subnet mask in this order: 0.0.0.0/0.0.0.0.
    trusted_ip: Optional[str]
    #: Read-only community string that allows/denies access to other device's statistics. Default value is public.
    get_community: Optional[str]
    #: Read-write community string that protects the device against unauthorized changes. Must never be set to public.
    set_community: Optional[str]
    #: Denotes whether the SNMPv3 security is enabled.
    snmp_v3_enabled: Optional[bool]


class AtaObjectDevice(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObjectDevice]
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
    vlan: Optional[VlanObjectDevice]
    #: Enable/disable user level web access to the local device.
    web_access_enabled: Optional[bool]
    #: Enable/disable the automatic nightly configuration resync of the MPP device.
    nightly_resync_enabled: Optional[bool]
    #: Specify values needed to enable use of the SNMP service from the phone.
    snmp: Optional[SnmpObject]


class BacklightTimerObjectDevice(ApiModel):
    #: Set the phone's backlight to be on for five minutes.
    five_min: Optional[str]
    #: Set the phone's backlight to be on for thirty minutes.
    thirty_min: Optional[str]
    #: Keep the phone's backlight always on.
    always_on: Optional[str]


class BackgroundImage(ApiModel):
    #: Indicates that dark blue background image will be set for the devices.
    dark_blue: Optional[str]
    #: Indicates that Cisco themed dark blue background image will be set for the devices.
    cisco_dark_blue: Optional[str]
    #: Indicates that Cisco Webex dark blue background image will be set for the devices.
    webex_dark_blue: Optional[str]
    #: Indicates that a custom background image will be set for the devices.
    custom_background: Optional[str]
    #: When this option is selected, a field 'Custom Background URL' needs to be added with the image url. URLs
    #: provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url: Optional[str]


class DisplayNameSelection(ApiModel):
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name: Optional[str]
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name: Optional[str]


class DefaultLoggingLevelObject(ApiModel):
    #: Enables detailed debugging logging.
    debugging: Optional[str]


class DisplayCallqueueAgentSoftkeysObject(ApiModel):
    last_page: Optional[str]


class AcdObjectDevice(ApiModel):
    #: Indicates whether the ACD object is enabled.
    enabled: Optional[bool]
    #: Indicates the call queue agent soft key value of an ACD object.
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkeysObject]


class LineKeyLEDPattern(ApiModel):
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


class PoeMode(ApiModel):
    #: Use maximum power consumption.
    maximum: Optional[str]


class UsbPortsObject(ApiModel):
    #: New Control to Enable/Disable the side USB port.
    enabled: Optional[bool]
    #: Enable/disable use of the side USB port on the MPP device. Enabled by default.
    side_usb_enabled: Optional[bool]
    #: Enable/disable use of the rear USB port on the MPP device.
    rear_usb_enabled: Optional[bool]


class MppVlanObjectDevice(VlanObjectDevice):
    #: Indicates the PC port value of a VLAN object for an MPP object.
    pc_port: Optional[int]


class AuthenticationMethodObject(ApiModel):
    #: No authentication.
    none: Optional[str]
    #: Extensible Authentication Protocol-Flexible Authentication via Secure Tunneling. Requires username and password
    #: authentication.
    eap_fast: Optional[str]
    #: Protected Extensible Authentication Protocol - Generic Token Card. Requires username and password
    #: authentication.
    peap_gtc: Optional[str]
    #: Protected Extensible Authentication Protocol - Microsoft Challenge Handshake Authentication Protocol version 2.
    #: Requires username and password authentication.
    peap_mschapv2: Optional[str]
    #: Pre-Shared Key. Requires shared passphrase for authentication.
    psk: Optional[str]
    #: Wired Equivalent Privacy. Requires encryption key for authentication.
    wep: Optional[str]


class WifiNetworkObjectDevice(ApiModel):
    #: Indicates whether the wifi network is enabled.
    enabled: Optional[bool]
    #: Authentication method of the WiFi network.
    authentication_method: Optional[AuthenticationMethodObject]
    #: SSID name of the wifi network.
    ssid_name: Optional[str]
    #: User ID for the WiFi network.
    user_id: Optional[str]


class CallHistoryMethod(ApiModel):
    #: Set call history to use the unified call history from all of the end user's devices.
    webex_unified_call_history: Optional[str]
    #: Set call history to use local device information only.
    local_call_history: Optional[str]


class DirectoryMethod(ApiModel):
    #: Set directory services to use standard XSI query method from the device.
    xsi_directory: Optional[str]
    #: Set directory services to use the Webex Enterprise directory.
    webex_directory: Optional[str]


class VolumeSettingsObject(ApiModel):
    #: Specify a ringer volume level through a numeric value between 0 and 15.
    ringer_volume: Optional[int]
    #: Specify a speaker volume level through a numeric value between 0 and 15.
    speaker_volume: Optional[int]
    #: Specify a handset volume level through a numeric value between 0 and 15.
    handset_volume: Optional[int]
    #: Specify a headset volume level through a numeric value between 0 and 15.
    headset_volume: Optional[int]
    #: Enable/disable the wireless headset hookswitch control.
    e_hook_enabled: Optional[bool]
    #: Enable/disable to preserve the existing values on the phone and not the values defined for the device settings.
    allow_end_user_override_enabled: Optional[bool]


class CallForwardExpandedSoftKey(ApiModel):
    #: Set the default call forward expanded soft key behavior to single option.
    only_the_call_forward_all: Optional[str]
    #: Set the default call forward expanded soft key behavior to multiple menu option.
    all_call_forwards: Optional[str]


class Mode(str, Enum):
    off = 'OFF'
    auto = 'AUTO'
    manual = 'MANUAL'


class HttpProxyObject(ApiModel):
    #: Mode of the HTTP proxy.
    mode: Optional[Mode]
    #: Enable/disable auto discovery of the URL.
    auto_discovery_enabled: Optional[bool]
    #: Specify the host URL if the HTTP mode is set to MANUAL.
    host: Optional[str]
    #: Specify the port if the HTTP mode is set to MANUAL.
    port: Optional[str]
    #: Specify PAC URL if auto discovery is disabled.
    pack_url: Optional[str]
    #: Enable/disable authentication settings.
    auth_settings_enabled: Optional[bool]
    #: Specify a username if authentication settings are enabled.
    username: Optional[str]
    #: Specify a password if authentication settings are enabled.
    password: Optional[str]


class Mode1(str, Enum):
    phone = 'PHONE'
    hands_free = 'HANDS_FREE'
    both = 'BOTH'


class BluetoothObject(ApiModel):
    #: Enable/disable Bluetooth.
    enabled: Optional[bool]
    #: Select a Bluetooth mode.
    mode: Optional[Mode1]


class NoiseCancellationObject(ApiModel):
    #: Enable/disable the Noise Cancellation.
    enabled: Optional[bool]
    #: Enable/disable to preserve the existing values on the phone and not the value defined for the device setting.
    allow_end_user_override_enabled: Optional[bool]


class SoftKeyMenuObject(ApiModel):
    #: Specify the idle key list.
    idle_key_list: Optional[str]
    #: Specify the off hook key list.
    off_hook_key_list: Optional[str]
    #: Specify the dialing input key list.
    dialing_input_key_list: Optional[str]
    #: Specify the progressing key list.
    progressing_key_list: Optional[str]
    #: Specify the connected key list.
    connected_key_list: Optional[str]
    #: Specify the connected video key list.
    connected_video_key_list: Optional[str]
    #: Start the transfer key list.
    start_transfer_key_list: Optional[str]
    #: Start the conference key list.
    start_conference_key_list: Optional[str]
    #: Specify the conferencing key list.
    conferencing_key_list: Optional[str]
    #: Specify the releasing key list.
    releasing_key_list: Optional[str]
    #: Specify the hold key list.
    hold_key_list: Optional[str]
    #: Specify the ringing key list.
    ringing_key_list: Optional[str]
    #: Specify the shared active key list.
    shared_active_key_list: Optional[str]
    #: Specify the shared held key list.
    shared_held_key_list: Optional[str]


class PskObject(ApiModel):
    #: Specify PSK1.
    psk1: Optional[str]
    #: Specify PSK2.
    psk2: Optional[str]
    #: Specify PSK3.
    psk3: Optional[str]
    #: Specify PSK4.
    psk4: Optional[str]
    #: Specify PSK5.
    psk5: Optional[str]
    #: Specify PSK6.
    psk6: Optional[str]
    #: Specify PSK7.
    psk7: Optional[str]
    #: Specify PSK8.
    psk8: Optional[str]
    #: Specify PSK9.
    psk9: Optional[str]
    #: Specify PSK10.
    psk10: Optional[str]
    #: Specify PSK11.
    psk11: Optional[str]
    #: Specify PSK12.
    psk12: Optional[str]
    #: Specify PSK13.
    psk13: Optional[str]
    #: Specify PSK14.
    psk14: Optional[str]
    #: Specify PSK15.
    psk15: Optional[str]
    #: Specify PSK16.
    psk16: Optional[str]


class SoftKeyLayoutObject(ApiModel):
    #: Customize SoftKey menu settings.
    soft_key_menu: Optional[SoftKeyMenuObject]
    #: Customize PSK.
    psk: Optional[PskObject]
    #: Default SoftKey menu settings.
    soft_key_menu_defaults: Optional[SoftKeyMenuObject]
    #: Default PSK.
    psk_defaults: Optional[PskObject]


class BackgroundImageColor(ApiModel):
    #: Indicates that dark cyan background image will be set for the devices.
    cyan_dark: Optional[str]
    #: Indicates the dark purple background image will be set for the devices.
    purple_dark: Optional[str]
    #: Indicates the dark blue background image will be set for the devices.
    blue_dark: Optional[str]
    #: Indicates the dark violet background image will be set for the devices.
    violet_dark: Optional[str]
    #: Indicates the light blue background image will be set for the devices.
    blue_light: Optional[str]
    #: Indicates the light violet background image will be set for the devices.
    violet_light: Optional[str]


class BacklightTimer68XX(ApiModel):
    #: Keep the phone's backlight always on.
    always_on: Optional[str]
    #: Set the phone's backlight to be on for ten seconds.
    ten_sec: Optional[str]
    #: Set the phone's backlight to be on for twenty seconds.
    twenty_sec: Optional[str]
    #: Set the phone's backlight to be on for thirty seconds.
    thirty_sec: Optional[str]
    #: Keep the phone's backlight off.
    off: Optional[str]


class MppObjectDevice(ApiModel):
    #: Indicates whether the PNAC of MPP object is enabled or not.
    pnac_enabled: Optional[bool]
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObjectDevice]
    #: Choose the length of time (in minutes) for the phone's backlight to remain on.
    backlight_timer: Optional[BacklightTimerObjectDevice]
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage]
    #: The display name that appears on the phone screen.
    display_name_format: Optional[DisplayNameSelection]
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool]
    #: Choose the desired logging level for an MPP devices.
    default_logging_level: Optional[DefaultLoggingLevelObject]
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    dnd_services_enabled: Optional[bool]
    #: Holds the Acd object value.
    acd: Optional[AcdObjectDevice]
    #: Indicates the short inter digit timer value.
    short_interdigit_timer: Optional[int]
    #: Indicates the long inter digit timer value..
    long_interdigit_timer: Optional[int]
    #: Line key labels define the format of what's shown next to line keys.
    line_key_label_format: Optional[DisplayNameSelection]
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not
    #: supported on the MPP 8875
    line_key_led_pattern: Optional[LineKeyLEDPattern]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: Optional[bool]
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]]
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: Optional[int]
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
    phone_language: Optional[PhoneLanguage]
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[PoeMode]
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify the amount of inactive time needed (in seconds) before the phone's screen saver activates.
    screen_timeout: Optional[VlanObjectDevice]
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    usb_ports_enabled: Optional[bool]
    #: By default the Side USB port is enabled to support KEMs and other peripheral devices. Use the option to disable
    #: use of this port.
    usb_ports: Optional[UsbPortsObject]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObjectDevice]
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObjectDevice]
    #: Specify the call history information to use. Only applies to user devices.
    call_history: Optional[CallHistoryMethod]
    #: Specify the directory services to use.
    contacts: Optional[DirectoryMethod]
    #: Enable/disable the availability of the webex meetings functionality from the phone.
    webex_meetings_enabled: Optional[bool]
    #: Specify all volume level values on the phone.
    volume_settings: Optional[VolumeSettingsObject]
    #: Specify the call forward expanded soft key behavior.
    cf_expanded_soft_key: Optional[CallForwardExpandedSoftKey]
    #: Specify HTTP Proxy values.
    http_proxy: Optional[HttpProxyObject]
    #: Enable/disable the visibility of the bluetooth menu on the MPP device.
    bluetooth: Optional[BluetoothObject]
    #: Enable/disable the use of the PC passthrough ethernet port on supported phone models.
    pass_through_port_enabled: Optional[bool]
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the
    #: device.
    user_password_override_enabled: Optional[bool]
    #: Enable/disable the default screen behavior when inbound calls are received.
    active_call_focus_enabled: Optional[bool]
    #: Enable/disable peer firmware sharing.
    peer_firmware_enabled: Optional[bool]
    #: Enable/disable local noise cancellation on active calls from the device.
    noise_cancellation: Optional[NoiseCancellationObject]
    #: Enable/disable visibility of the Accessibility Voice Feedback menu on the MPP device.
    voice_feedback_accessibility_enabled: Optional[bool]
    #: Enable/disable availability of dial assist feature on the phone.
    dial_assist_enabled: Optional[bool]
    #: Specify the number of calls per unique line appearance on the phone.
    calls_per_line: Optional[int]
    #: Enable/disable automatic nightly configuration resync of the MPP device.
    nightly_resync_enabled: Optional[bool]
    #: Enable/disable the visual indication of missed calls.
    missed_call_notification_enabled: Optional[bool]
    #: Specify the softkey layout per phone menu state.
    soft_key_layout: Optional[SoftKeyLayoutObject]
    #: Specify the image option for the MPP 8875 phone background.
    background_image8875: Optional[BackgroundImageColor]
    #: Specify the use of the backlight feature on 6800 nad 7800 series devices.
    backlight_timer68_xx78_xx: Optional[BacklightTimer68XX]


class WifiAudioCodecPriorityObjectDevice(ApiModel):
    #: Indicates the selection of the Audio Codec Priority Object for an WiFi object.
    selection: Optional[str]
    #: Indicates the primary Audio Codec for an WiFi object.
    primary: Optional[str]
    #: Indicates the secondary Audio Codec for an WiFi object.
    secondary: Optional[str]
    #: Indicates the tertiary Audio Codec for an WiFi object.
    tertiary: Optional[str]


class LdapObject(ApiModel):
    #: Sets the values needed to enable use of the LDAP service on the phone.
    enabled: Optional[bool]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    server_address: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    server_port: Optional[int]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    comm_security_type: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    bind_dn: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    bind_pw: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    base_dn: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    primary_email_attribute: Optional[str]
    #: Sets the values needed to enable use of the LDAP service on the phone.
    alternate_email_attribute: Optional[str]


class WebAccessObject(ApiModel):
    #: Ability to enable or disable the web browser access for the 840/860.
    enabled: Optional[bool]
    #: Ability to set a Web Server Password.
    password: Optional[str]


class WifiObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[WifiAudioCodecPriorityObjectDevice]
    #: Set the values needed to enable use of the LDAP service on the phone.
    ldap: Optional[LdapObject]
    #: Set the availability of the local end user web access for an 840/860 WiFi phone.
    web_access: Optional[WebAccessObject]
    #: Set the local security password on an 840/860 WiFi phone.
    phone_security_pwd: Optional[str]


class CustomizationDeviceLevelObjectDevice(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObjectDevice]
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObjectDevice]
    #: Applicable device settings for a WiFi device.
    wifi: Optional[WifiObject]


class UpdateDeviceSettingsBody(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObjectDevice]
    #: Indicates if customization is allowed at a device level. If true, customized at a device level. If false, not
    #: customized; uses customer-level configuration.
    custom_enabled: Optional[bool]


class AtaDtmfModeObject1(ApiModel):
    #: Normal threshold mode.
    normal: Optional[str]


class AtaObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObjectDevice]
    #: DTMF Detection Tx Mode selection for Cisco ATA devices.
    ata_dtmf_mode: Optional[AtaDtmfModeObject1]
    #: Method for transmitting DTMF signals to the far end.
    ata_dtmf_method: Optional[AtaDtmfMethodObject]
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: Optional[bool]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[VlanObjectDevice]


class BacklightTimerObject(ApiModel):
    five_m: Optional[str]
    thirty_m: Optional[str]
    always_on: Optional[str]
    off: Optional[str]
    ten_s: Optional[str]
    twenty_s: Optional[str]
    thirty_s: Optional[str]


class DefaultLoggingLevelObject1(ApiModel):
    #: Enables detailed debugging logging.
    debugging: Optional[str]


class DisplayCallqueueAgentSoftkeysObject1(ApiModel):
    last_page: Optional[str]


class Acd(ApiModel):
    #: Indicates whether the ACD object is enabled.
    enabled: Optional[bool]
    #: Indicates the call queue agent soft key value of an ACD object.
    display_callqueue_agent_softkeys: Optional[str]


class LineKeyLEDPattern1(ApiModel):
    preset_1: Optional[str]


class WifiNetworkObject(ApiModel):
    #: Indicates whether the wifi network is enabled.
    enabled: Optional[bool]
    #: Authentication method of wifi network.
    authentication_method: Optional[str]
    #: SSID name of the wifi network.
    ssid_name: Optional[str]
    #: User Id of the wifi network.
    user_id: Optional[str]


class MppObject(ApiModel):
    #: Indicates whether the PNAC of MPP object is enabled or not.
    pnac_enabled: Optional[bool]
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[WifiAudioCodecPriorityObjectDevice]
    #: Choose the length of time (in minutes) for the phone's backlight to remain on.
    backlight_timer: Optional[BacklightTimerObject]
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage]
    #: The display name that appears on the phone screen.
    display_name_format: Optional[DisplayNameSelection]
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool]
    #: Choose the desired logging level for an MPP devices.
    default_logging_level: Optional[DefaultLoggingLevelObject1]
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    dnd_services_enabled: Optional[bool]
    #: Chooses the location of the Call Queue Agent Login/Logout softkey on Multi-Platform Phones.
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkeysObject1]
    #: Choose the duration (in hours) of Hoteling guest login.
    hoteling_guest_association_timer: Optional[int]
    #: Holds the Acd object value.
    acd: Optional[Acd]
    #: Indicates the short inter digit timer value.
    short_interdigit_timer: Optional[int]
    #: Indicates the long inter digit timer value..
    long_interdigit_timer: Optional[int]
    #: Line key labels define the format of what's shown next to line keys.
    line_key_label_format: Optional[DisplayNameSelection]
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not
    #: supported on the MPP 8875
    line_key_led_pattern: Optional[LineKeyLEDPattern1]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: Optional[bool]
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]]
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: Optional[int]
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
    phone_language: Optional[PhoneLanguage]
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[str]
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify the amount of inactive time needed (in seconds) before the phone's screen saver activates.
    screen_timeout: Optional[VlanObjectDevice]
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    usb_ports_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObjectDevice]
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObject]


class CustomizationDeviceLevelObject(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObject]
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObject]


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str]
    #: Enumeration that indicates if the member is of type PEOPLE or PLACE.
    type: Optional[MemberType]
    #: First name of device owner.
    first_name: Optional[str]
    #: Last name of device owner.
    last_name: Optional[str]


class DeviceActivationStates(ApiModel):
    #: Indicates a device is activated.
    activated: Optional[str]
    #: Indicates a device is deactivated.
    deactivated: Optional[str]


class ActivationStates(DeviceActivationStates):
    #: Indicates a device is activating.
    activating: Optional[str]


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str]
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]]
    #: Identifier for device model.
    model: Optional[str]
    #: MAC address of device.
    mac: Optional[str]
    #: IP address of device.
    ip_address: Optional[str]
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType]
    #: Owner of device.
    owner: Optional[DeviceOwner]
    #: Activation state of device.
    activation_state: Optional[ActivationStates]


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this
    #: host(workspace device) and use this device
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive
    #: calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool]
    #: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
    limit_guest_use: Optional[bool]
    #: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
    guest_hours_limit: Optional[int]


class PlaceDevices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str]
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]]
    #: Identifier for device model.
    model: Optional[str]
    #: MAC address of device.
    mac: Optional[str]
    #: IP address of device.
    ip_address: Optional[str]
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType]
    #: Indicates Hoteling details of a device.
    hoteling: Optional[Hoteling]
    #: Owner of the device.
    owner: Optional[DeviceOwner]
    #: Activation state of a device.
    activation_state: Optional[DeviceActivationStates]


class TypeObject(ApiModel):
    #: Analog Telephone Adapters
    ata: Optional[str]
    #: GENERIC Session Initiation Protocol
    generic_sip: Optional[str]
    #: Esim Supported Webex Go
    esim: Optional[str]


class ManufacturerObject(ApiModel):
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for
    #: provisioning in the control hub.
    third_party: Optional[str]


class ManagedByObject(ApiModel):
    #: Devices managed by Cisco.
    cisco: Optional[str]
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the
    #: control hub.
    customer: Optional[str]


class SupportedForObject(ApiModel):
    place: Optional[str]


class OnboardingMethodObject(ApiModel):
    activation_code: Optional[str]
    none: Optional[str]


class KemModuleTypeObject(ApiModel):
    kem_18_keys: Optional[str]


class DeviceObject(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Display name of the device.
    display_name: Optional[str]
    #: Type of the device.
    type: Optional[TypeObject]
    #: Manufacturer of the device.
    manufacturer: Optional[ManufacturerObject]
    #: Users who manage the device.
    managed_by: Optional[ManagedByObject]
    #: List of places the device is supported for.
    supported_for: Optional[list[SupportedForObject]]
    #: Onboarding method.
    onboarding_method: Optional[list[OnboardingMethodObject]]
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: Optional[bool]
    #: Number of port lines.
    number_of_line_ports: Optional[int]
    #: Indicates whether Kem support is enabled or not.
    kem_support_enabled: Optional[bool]
    #: Module count.
    kem_module_count: Optional[int]
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleTypeObject]]
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool]
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str]
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool]
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool]
    #: Enables / disables customized behavior support on devices.
    customized_behaviors_enabled: Optional[bool]
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool]
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool]


class DectObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObjectDevice]
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
    vlan: Optional[VlanObjectDevice]


class CustomizationObject(CustomizationDeviceLevelObject):
    #: Settings that are applicable to DECT devices.
    dect: Optional[DectObject]


class DectDeviceList(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Display name of the device.
    display_name: Optional[str]
    #: Indicates number of base stations.
    number_of_base_stations: Optional[int]
    #: Indicates number of port lines,
    number_of_line_ports: Optional[int]
    #: Indicates number of supported registrations.
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
    #: MAC address validation error code.
    error_code: Optional[int]
    #: Provides a status message about the MAC address.
    message: Optional[str]


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int]
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str]
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str]
    #: Exit Code for a job.
    exit_code: Optional[str]
    #: Job creation time in UTC format.
    created_time: Optional[str]
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str]


class CountObject(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int]
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int]
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int]
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse(Location):
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: Indicates operation type that was carried out.
    operation_type: Optional[str]
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str]
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str]
    #: Job statistics.
    counts: Optional[CountObject]


class StepExecutionStatusesObject(Location):
    #: Step execution start time in UTC format.
    start_time: Optional[str]
    #: Step execution end time in UTC format.
    end_time: Optional[str]
    #: Last updated time for a step in UTC format.
    last_updated: Optional[str]
    #: Displays status for a step.
    status_message: Optional[str]
    #: Exit Code for a step.
    exit_code: Optional[str]
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str]


class JobExecutionStatusObject(JobExecutionStatusObject1):
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]]


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str]
    #: Internal error code.
    code: Optional[str]
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    #: location ID.
    location_id: Optional[str]


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str]
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]]


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str]
    #: Index of error number.
    item_number: Optional[int]
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str]
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


class GetDeviceSettingsResponse(UpdateDeviceSettingsBody):
    #: Customer devices setting update status. If true, an update is in progress (no further changes are allowed). If
    #: false, no update in progress (changes are allowed).
    update_in_progress: Optional[bool]
    #: Number of devices that will be updated.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class GetLocationDeviceSettingsResponse(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObject]
    #: Indicates if customization is allowed at a location level. If true, customized at a location level. If false,
    #: not customized; uses customer-level configuration.
    custom_enabled: Optional[bool]
    #: Customer devices setting update status. If true, an update is in progress (no further changes are allowed). If
    #: false, no update in progress (changes are allowed).
    update_in_progress: Optional[bool]
    #: Number of devices that will be updated.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class GetUserDevicesResponse(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int]


class GetWorkspaceDevicesResponse(ApiModel):
    #: Array of devices associated to a workspace.
    devices: Optional[list[PlaceDevices]]
    #: Maximum number of devices a workspace can be assigned to.
    max_device_count: Optional[int]


class ReadListOfSupportedDevicesResponse(ApiModel):
    #: List of supported devices.
    devices: Optional[list[DeviceObject]]


class ReaddeviceOverrideSettingsFororganizationResponse(ApiModel):
    #: Customization object of the device settings.
    customizations: Optional[CustomizationObject]
    #: Progress of the device update.
    update_in_progress: Optional[bool]
    #: Device count.
    device_count: Optional[int]
    #: Last updated time.
    last_update_time: Optional[int]


class ReadDECTDeviceTypeListResponse(ApiModel):
    #: Contains a list of devices.
    devices: Optional[list[DectDeviceList]]


class ValidatelistOfMACAddressBody(ApiModel):
    #: MAC addresses to be validated.
    #: Possible values: {["ab125678cdef", "00005E0053B4"]}
    macs: Optional[list[str]]


class ValidatelistOfMACAddressResponse(ApiModel):
    #: Status of MAC address.
    status: Optional[Status]
    #: Contains an array of all the MAC address provided and their statuses.
    mac_status: Optional[list[MacStatusObject]]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobBody(ApiModel):
    #: Location within an organization where changes of device setings will be applied to all the devices within it.
    location_id: Optional[str]
    #: Indicates if all the devices within this location will be customized with new requested customizations(if set to
    #: true) or will be overridden with the one at organization level (if set to false or any other value). This field
    #: has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates the settings for ATA devices, DECT devices and MPP devices.
    customizations: Optional[CustomizationObject]


class ListChangeDeviceSettingsJobsResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse]]


class GetChangeDeviceSettingsJobStatusResponse(Location):
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: Indicates the operation type that was carried out.
    operation_type: Optional[str]
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str]
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str]
    #: The location name for which the job was run.
    source_location_name: Optional[str]
    #: The location name for which the numbers have been moved.
    target_location_name: Optional[str]
    #: Job statistics.
    counts: Optional[CountObject]


class ListChangeDeviceSettingsJobErrorsResponse(ApiModel):
    items: Optional[list[ItemObject]]


class DeviceCallSettingsApi(ApiChild, base='telephony/config/'):
    """
    These APIs manages Webex Calling settings for devices with are of the Webex Calling type.
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    spark-admin:telephony_config_write.
    """

    def members(self, device_id: str, org_id: str = None) -> GetDeviceMembersResponse:
        """
        Get the list of all the members of the device including primary and secondary users.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-device-members
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/members')
        data = super().get(url=url, params=params)
        return GetDeviceMembersResponse.parse_obj(data)

    def update_members_ondevice(self, device_id: str, org_id: str = None, members: PutMemberObject = None):
        """
        Modify member details on the device.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.
        Modifying members on the device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        :param members: If the member's list is missing then all the users are removed except the primary user.
        :type members: PutMemberObject

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/update-members-on-the-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateMembersOndeviceBody()
        if members is not None:
            body.members = members
        url = self.ep(f'devices/{device_id}/members')
        super().put(url=url, params=params, data=body.json())
        return

    def search_members(self, device_id: str, location_id: str, org_id: str = None, member_name: str = None, phone_number: str = None, extension: str = None, order: str = None, **params) -> Generator[SearchMemberObject, None, None]:
        """
        Search members that can be assigned to the device.
        A device member can be either a person or a workspace. A admin can access the list of member details, modify
        member details and
        search for available members on a device.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Retrieves the list of available members on the device in this organization.
        :type org_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param order: Sort the list of available members on the device in ascending order by name, use either last name
            lname or first name fname. Default sort is last name in ascending order.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/search-members
        """
        params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if order is not None:
            params['order'] = order
        url = self.ep(f'devices/{device_id}/availableMembers')
        return self.session.follow_pagination(url=url, model=SearchMemberObject, item_key='members', params=params)

    def apply_changes_forspecific(self, device_id: str, org_id: str = None):
        """
        Issues request to the device to download and apply changes to the configuration.
        Applying changes for a specific device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/apply-changes-for-a-specific-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/actions/applyChanges/invoke')
        super().post(url=url, params=params)
        return

    def settings(self, device_id: str, device_model: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get override settings for a device.
        Device settings lists all the applicable settings for MPP, ATA and Wifi devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-device-settings
        """
        params = {}
        params['deviceModel'] = device_model
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def update_settings(self, device_id: str, customizations: CustomizationDeviceLevelObjectDevice, custom_enabled: bool, org_id: str = None, device_model: str = None):
        """
        Modify override settings for a device.
        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins can
        also modify the settings. NOTE: DECT devices do not support settings at the device level.
        Updating settings on the device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObjectDevice
        :param custom_enabled: Indicates if customization is allowed at a device level. If true, customized at a device
            level. If false, not customized; uses customer-level configuration.
        :type custom_enabled: bool
        :param org_id: Organization in which the device resides..
        :type org_id: str
        :param device_model: Device model name.
        :type device_model: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/update-device-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        body = UpdateDeviceSettingsBody()
        if customizations is not None:
            body.customizations = customizations
        if custom_enabled is not None:
            body.custom_enabled = custom_enabled
        url = self.ep(f'devices/{device_id}/settings')
        super().put(url=url, params=params, data=body.json())
        return

    def location_settings(self, location_id: str, org_id: str = None) -> GetLocationDeviceSettingsResponse:
        """
        Get device override settings for a location.
        This requires a full or read-only administrator or location administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Organization in which the device resides.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-location-device-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/devices/settings')
        data = super().get(url=url, params=params)
        return GetLocationDeviceSettingsResponse.parse_obj(data)

    def user(self, person_id: str, org_id: str = None) -> GetUserDevicesResponse:
        """
        Get all devices for a person.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-user-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices')
        data = super().get(url=url, params=params)
        return GetUserDevicesResponse.parse_obj(data)

    def workspace(self, workspace_id: str, org_id: str = None) -> GetWorkspaceDevicesResponse:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices')
        data = super().get(url=url, params=params)
        return GetWorkspaceDevicesResponse.parse_obj(data)

    def modify_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None, limit_guest_use: bool = None, guest_hours_limit: int = None):
        """
        Modify devices for a workspace.
        Modifying devices for a workspace requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :param enabled: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can
            log into this host(workspace device) and use this device as if it were their own. This is useful when
            traveling to a remote office but still needing to place/receive calls with their telephone number and
            access features normally available to them on their office phone.
        :type enabled: bool
        :param limit_guest_use: Enable limiting the time a guest can use the device. The time limit is configured via
            guestHoursLimit.
        :type limit_guest_use: bool
        :param guest_hours_limit: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
        :type guest_hours_limit: int

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/modify-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = Hoteling()
        if enabled is not None:
            body.enabled = enabled
        if limit_guest_use is not None:
            body.limit_guest_use = limit_guest_use
        if guest_hours_limit is not None:
            body.guest_hours_limit = guest_hours_limit
        url = self.ep(f'workspaces/{workspace_id}/devices')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_supported(self, org_id: str = None) -> list[DeviceObject]:
        """
        Gets the list of supported devices for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/read-the-list-of-supported-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('supportedDevices')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[DeviceObject], data["devices"])

    def readdevice_override_settings_fororganization(self, org_id: str = None) -> ReaddeviceOverrideSettingsFororganizationResponse:
        """
        Get device override settings for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/read-the-device-override-settings-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/settings')
        data = super().get(url=url, params=params)
        return ReaddeviceOverrideSettingsFororganizationResponse.parse_obj(data)

    def read_dect_type_list(self, org_id: str = None) -> list[DectDeviceList]:
        """
        Get DECT device type list with base stations and line ports supported count. This is a static list.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: 
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/read-the-dect-device-type-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/dects/supportedDevices')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[DectDeviceList], data["devices"])

    def validatelist_of_mac_address(self, macs: List[str], org_id: str = None) -> ValidatelistOfMACAddressResponse:
        """
        Validate a list of MAC addresses.
        Validating this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param macs: MAC addresses to be validated. Possible values: {["ab125678cdef", "00005E0053B4"]}
        :type macs: List[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/validate-a-list-of-mac-address
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidatelistOfMACAddressBody()
        if macs is not None:
            body.macs = macs
        url = self.ep('devices/actions/validateMacs/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return ValidatelistOfMACAddressResponse.parse_obj(data)

    def change_settings_across_organization_or_location_job(self, org_id: str = None, location_id: str = None, location_customizations_enabled: bool = None, customizations: CustomizationObject = None) -> ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse:
        """
        Change device settings across organization or locations jobs.
        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system
        admins in a stateful persistent manner. This job will modify the requested device settings across all the
        devices. Whenever a location ID is specified in the request, it will modify the requested device settings only
        for the devices that are part of the provided location within an organization.
        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.
        Only one job per customer can be running at any given time within the same organization. An attempt to run
        multiple jobs at the same time will result in a 409 error response.
        Running a job requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :param location_id: Location within an organization where changes of device setings will be applied to all the
            devices within it.
        :type location_id: str
        :param location_customizations_enabled: Indicates if all the devices within this location will be customized
            with new requested customizations(if set to true) or will be overridden with the one at organization level
            (if set to false or any other value). This field has no effect when the job is being triggered at
            organization level.
        :type location_customizations_enabled: bool
        :param customizations: Indicates the settings for ATA devices, DECT devices and MPP devices.
        :type customizations: CustomizationObject

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/change-device-settings-across-organization-or-location-job
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ChangeDeviceSettingsAcrossOrganizationOrLocationJobBody()
        if location_id is not None:
            body.location_id = location_id
        if location_customizations_enabled is not None:
            body.location_customizations_enabled = location_customizations_enabled
        if customizations is not None:
            body.customizations = customizations
        url = self.ep('jobs/devices/callDeviceSettings')
        data = super().post(url=url, params=params, data=body.json())
        return ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse.parse_obj(data)

    def list_change_settings_jobs(self, org_id: str = None, **params) -> Generator[ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse, None, None]:
        """
        List change device settings jobs.
        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to
        oldest one irrespective of its status.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/list-change-device-settings-jobs
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/callDeviceSettings')
        return self.session.follow_pagination(url=url, model=ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse, params=params)

    def change_settings_job_status(self, job_id: str) -> GetChangeDeviceSettingsJobStatusResponse:
        """
        Get change device settings job status.
        Provides details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/get-change-device-settings-job-status
        """
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}')
        data = super().get(url=url)
        return GetChangeDeviceSettingsJobStatusResponse.parse_obj(data)

    def list_change_settings_job_errors(self, job_id: str, org_id: str = None, **params) -> Generator[ItemObject, None, None]:
        """
        List change device settings job errors.
        Lists all error details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/device-call-settings/list-change-device-settings-job-errors
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, params=params)
