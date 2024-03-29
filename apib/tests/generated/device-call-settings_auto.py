from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AcdObject', 'ActivationStates', 'AdminBatchStartJobObjectLocationCustomizations', 'AtaDtmfMethodObject', 'AtaDtmfModeObject', 'AtaObject', 'AudioCodecPriorityObject', 'AuthenticationMethodObject', 'BackgroundImage', 'BackgroundImageColor', 'BacklightTimer68XX', 'BacklightTimerObject', 'BluetoothObject', 'BluetoothObjectMode', 'CallForwardExpandedSoftKey', 'CallHistoryMethod', 'CommSecurityType', 'CountObject', 'CustomizationDeviceLevelObject', 'CustomizationDeviceLevelObjectDevice', 'CustomizationObject', 'DectDeviceList', 'DectObject', 'DectVlanObject', 'DefaultLoggingLevelObject', 'DeviceList', 'DeviceObject', 'DeviceOwner', 'DeviceSettingsObject', 'DeviceSettingsObjectForDeviceLevel', 'Devices', 'DirectoryMethod', 'DisplayCallqueueAgentSoftkeysObject', 'DisplayNameSelection', 'ErrorMessageObject', 'ErrorObject', 'ErrorResponseObject', 'GetMemberResponse', 'Hoteling', 'HttpProxyObject', 'HttpProxyObjectMode', 'ItemObject', 'JobExecutionStatusObject', 'JobExecutionStatusObject1', 'JobIdResponseObject', 'JobListResponse', 'KemModuleTypeObject', 'LdapObject', 'LineKeyLEDPattern', 'LineKeyLabelSelection', 'LineType', 'ListDectDeviceType', 'ListDeviceSettingsObject', 'Location', 'MACAddressResponse', 'MACAddressResponseStatus', 'MacStatusObject', 'MacStatusObjectState', 'ManagedByObject', 'ManufacturerObject', 'MemberObject', 'MemberType', 'MppAudioCodecPriorityObject', 'MppObject', 'MppObjectDevice', 'MppVlanObject', 'NoiseCancellationObject', 'OnboardingMethodObject', 'PhoneLanguage', 'PlaceDeviceList', 'PlaceDevices', 'PoeMode', 'PskObject', 'PutDeviceSettingsRequest', 'PutMemberObject', 'PutMembersRequest', 'SearchMemberObject', 'SearchMemberResponse', 'SelectionType', 'SnmpObject', 'SoftKeyLayoutObject', 'SoftKeyMenuObject', 'StartJobResponse', 'StepExecutionStatusesObject', 'SupportedDevicesObject', 'TypeObject', 'UsbPortsObject', 'ValidateMACRequest', 'VolumeSettingsObject', 'WebAccessObject', 'WifiNetworkObject', 'WifiObject', 'WifiObjectDevice']


class DisplayCallqueueAgentSoftkeysObject(str, Enum):
    front_page = 'FRONT_PAGE'
    last_page = 'LAST_PAGE'


class AcdObject(ApiModel):
    #: Indicates whether the ACD object is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Indicates the call queue agent soft key value of an ACD object.
    #: example: LAST_PAGE
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkeysObject] = None


class ActivationStates(str, Enum):
    #: Indicates a device is activating.
    activating = 'ACTIVATING'
    #: Indicates a device is activated.
    activated = 'ACTIVATED'
    #: Indicates a device is deactivated.
    deactivated = 'DEACTIVATED'


class SelectionType(str, Enum):
    #: Indicates the regional selection type for audio codec priority.
    regional = 'REGIONAL'
    #: Indicates the custom selection type for audio codec priority.
    custom = 'CUSTOM'


class AudioCodecPriorityObject(ApiModel):
    #: Indicates the selection of an Audio Codec Priority Object.
    #: example: REGIONAL
    selection: Optional[SelectionType] = None
    #: Indicates the primary Audio Codec.
    #: example: G711a
    primary: Optional[str] = None
    #: Indicates the secondary Audio Codec.
    #: example: G711u
    secondary: Optional[str] = None
    #: Indicates the tertiary Audio Codec.
    #: example: G729a
    tertiary: Optional[str] = None


class AtaDtmfModeObject(str, Enum):
    #: A DTMF digit requires an extra hold time after detection and the DTMF level threshold is raised to -20 dBm.
    strict = 'STRICT'
    #: Normal threshold mode.
    normal = 'NORMAL'


class AtaDtmfMethodObject(str, Enum):
    #: Sends DTMF by using the audio path.
    inband = 'INBAND'
    #: Audio video transport. Sends DTMF as AVT events.
    avt = 'AVT'
    #: Uses InBand or AVT based on the outcome of codec negotiation.
    auto = 'AUTO'


class DectVlanObject(ApiModel):
    #: Denotes whether the VLAN object of DECT is enabled.
    enabled: Optional[bool] = None
    #: Value of the VLAN Object of DECT.
    value: Optional[int] = None


class SnmpObject(ApiModel):
    #: Denotes whether the Simple Network Management Protocol of an ATA is enabled.
    enabled: Optional[bool] = None
    #: Trusted IPv4 address and subnet mask in this order: 0.0.0.0/0.0.0.0.
    #: example: 10.0.0.45
    trusted_ip: Optional[str] = Field(alias='trustedIP', default=None)
    #: Read-only community string that allows/denies access to other device's statistics. Default value is `public`.
    #: example: public
    get_community: Optional[str] = None
    #: Read-write community string that protects the device against unauthorized changes. Must never be set to `public`.
    #: example: private
    set_community: Optional[str] = None
    #: Denotes whether the SNMPv3 security is enabled.
    snmp_v3_enabled: Optional[bool] = None


class AtaObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject] = None
    #: DTMF Detection Tx Mode selection for Cisco ATA devices.
    ata_dtmf_mode: Optional[AtaDtmfModeObject] = None
    #: Method for transmitting DTMF signals to the far end.
    #: example: AVT
    ata_dtmf_method: Optional[AtaDtmfMethodObject] = None
    #: Enable/disable Cisco Discovery Protocol for local devices.
    #: example: True
    cdp_enabled: Optional[bool] = None
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    #: example: True
    lldp_enabled: Optional[bool] = None
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    #: example: True
    qos_enabled: Optional[bool] = None
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[DectVlanObject] = None
    #: Enable/disable user level web access to the local device.
    #: example: True
    web_access_enabled: Optional[bool] = None
    #: Enable/disable the automatic nightly configuration resync of the MPP device.
    #: example: True
    nightly_resync_enabled: Optional[bool] = None
    #: Specify values needed to enable use of the SNMP service from the phone.
    snmp: Optional[SnmpObject] = None


class DectObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject] = None
    #: Enable/disable Cisco Discovery Protocol for local devices.
    #: example: True
    cdp_enabled: Optional[bool] = None
    #: Specify the destination number to be dialled from the DECT Handset top button when pressed.
    dect6825_handset_emergency_number: Optional[str] = None
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    #: example: True
    lldp_enabled: Optional[bool] = None
    #: Specify up to 3 multicast group URLs each with a unique listening port.
    multicast: Optional[str] = None
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    #: example: True
    qos_enabled: Optional[bool] = None
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[DectVlanObject] = None
    #: Enable/disable user level web access to the local device.
    #: example: True
    web_access_enabled: Optional[bool] = None
    #: Enable/disable phone's default behavior regarding the nightly maintenance synchronization with the Webex Calling platform.
    #: example: True
    nightly_resync_enabled: Optional[bool] = None


class MppAudioCodecPriorityObject(ApiModel):
    #: Indicates the selection of the Audio Codec Priority Object for an MPP object.
    #: example: CUSTOM
    selection: Optional[str] = None
    #: Indicates the primary Audio Codec for an MPP object.
    #: example: OPUS
    primary: Optional[str] = None
    #: Indicates the secondary Audio Codec for an MPP object.
    #: example: G722
    secondary: Optional[str] = None
    #: Indicates the tertiary Audio Codec for an MPP object.
    #: example: G711u
    tertiary: Optional[str] = None


class BacklightTimerObject(str, Enum):
    #: Set the phone's backlight to be on for one minute.
    one_min = 'ONE_MIN'
    #: Set the phone's backlight to be on for five minutes.
    five_min = 'FIVE_MIN'
    #: Set the phone's backlight to be on for thirty minutes.
    thirty_min = 'THIRTY_MIN'
    #: Keep the phone's backlight always on.
    always_on = 'ALWAYS_ON'


class BackgroundImage(str, Enum):
    #: Indicates that there will be no background image set for the devices.
    none_ = 'NONE'
    #: Indicates that dark blue background image will be set for the devices.
    dark_blue = 'DARK_BLUE'
    #: Indicates that Cisco themed dark blue background image will be set for the devices.
    cisco_dark_blue = 'CISCO_DARK_BLUE'
    #: Indicates that Cisco Webex dark blue background image will be set for the devices.
    webex_dark_blue = 'WEBEX_DARK_BLUE'
    #: Indicates that a custom background image will be set for the devices.
    custom_background = 'CUSTOM_BACKGROUND'
    #: When this option is selected, a field 'Custom Background URL' needs to be added with the image url. URLs provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url = 'customUrl'


class DisplayNameSelection(str, Enum):
    #: Indicates that devices will display the person's phone number, or if a person doesn't have a phone number, the location number will be displayed.
    person_number = 'PERSON_NUMBER'
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name = 'PERSON_FIRST_THEN_LAST_NAME'
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name = 'PERSON_LAST_THEN_FIRST_NAME'


class DefaultLoggingLevelObject(str, Enum):
    #: Enables standard logging.
    standard = 'STANDARD'
    #: Enables detailed debugging logging.
    debugging = 'DEBUGGING'


class LineKeyLabelSelection(str, Enum):
    #: This will display the person extension, or if a person doesn't have an extension, the person's first name will be displayed.
    person_extension = 'PERSON_EXTENSION'
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name = 'PERSON_FIRST_THEN_LAST_NAME'
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name = 'PERSON_LAST_THEN_FIRST_NAME'


class LineKeyLEDPattern(str, Enum):
    default = 'DEFAULT'
    preset_1 = 'PRESET_1'


class PhoneLanguage(str, Enum):
    #: Indicates a person's announcement language.
    person_language = 'PERSON_LANGUAGE'
    arabic = 'ARABIC'
    bulgarian = 'BULGARIAN'
    catalan = 'CATALAN'
    chinese_simplified = 'CHINESE_SIMPLIFIED'
    chinese_traditional = 'CHINESE_TRADITIONAL'
    croatian = 'CROATIAN'
    czech = 'CZECH'
    danish = 'DANISH'
    dutch = 'DUTCH'
    english_united_states = 'ENGLISH_UNITED_STATES'
    english_united_kingdom = 'ENGLISH_UNITED_KINGDOM'
    finnish = 'FINNISH'
    french_canada = 'FRENCH_CANADA'
    french_france = 'FRENCH_FRANCE'
    german = 'GERMAN'
    greek = 'GREEK'
    hebrew = 'HEBREW'
    hungarian = 'HUNGARIAN'
    italian = 'ITALIAN'
    japanese = 'JAPANESE'
    korean = 'KOREAN'
    norwegian = 'NORWEGIAN'
    polish = 'POLISH'
    portuguese_portugal = 'PORTUGUESE_PORTUGAL'
    russian = 'RUSSIAN'
    spanish_colombia = 'SPANISH_COLOMBIA'
    spanish_spain = 'SPANISH_SPAIN'
    slovak = 'SLOVAK'
    swedish = 'SWEDISH'
    slovenian = 'SLOVENIAN'
    turkish = 'TURKISH'
    ukraine = 'UKRAINE'


class PoeMode(str, Enum):
    #: Use normal power consumption.
    normal = 'NORMAL'
    #: Use maximum power consumption.
    maximum = 'MAXIMUM'


class MppVlanObject(ApiModel):
    #: Indicates whether the VLAN object of an MPP is enabled.
    enabled: Optional[bool] = None
    #: Indicates the value of a VLAN object for an MPP object.
    #: example: 1.0
    value: Optional[int] = None
    #: Indicates the PC port value of a VLAN object for an MPP object.
    #: example: 1.0
    pc_port: Optional[int] = None


class AuthenticationMethodObject(str, Enum):
    #: No authentication.
    none_ = 'NONE'
    #: Extensible Authentication Protocol-Flexible Authentication via Secure Tunneling. Requires username and password authentication.
    eap_fast = 'EAP_FAST'
    #: Protected Extensible Authentication Protocol - Generic Token Card. Requires username and password authentication.
    peap_gtc = 'PEAP_GTC'
    #: Protected Extensible Authentication Protocol - Microsoft Challenge Handshake Authentication Protocol version 2. Requires username and password authentication.
    peap_mschapv2 = 'PEAP_MSCHAPV2'
    #: Pre-Shared Key. Requires shared passphrase for authentication.
    psk = 'PSK'
    #: Wired Equivalent Privacy. Requires encryption key for authentication.
    wep = 'WEP'


class WifiNetworkObject(ApiModel):
    #: Indicates whether the wifi network is enabled.
    enabled: Optional[bool] = None
    #: Authentication method of wifi network.
    authentication_method: Optional[AuthenticationMethodObject] = None
    #: SSID name of the wifi network.
    #: example: my_wifi_network
    ssid_name: Optional[str] = None
    #: User Id of the wifi network.
    #: example: test-user
    user_id: Optional[str] = None


class CallHistoryMethod(str, Enum):
    #: Set call history to use the unified call history from all of the end user's devices.
    webex_unified_call_history = 'WEBEX_UNIFIED_CALL_HISTORY'
    #: Set call history to use local device information only.
    local_call_history = 'LOCAL_CALL_HISTORY'


class DirectoryMethod(str, Enum):
    #: Set directory services to use standard XSI query method from the device.
    xsi_directory = 'XSI_DIRECTORY'
    #: Set directory services to use the Webex Enterprise directory.
    webex_directory = 'WEBEX_DIRECTORY'


class VolumeSettingsObject(ApiModel):
    #: Specify a ringer volume level through a numeric value between 0 and 15.
    #: example: 9.0
    ringer_volume: Optional[int] = None
    #: Specify a speaker volume level through a numeric value between 0 and 15.
    #: example: 11.0
    speaker_volume: Optional[int] = None
    #: Specify a handset volume level through a numeric value between 0 and 15.
    #: example: 10.0
    handset_volume: Optional[int] = None
    #: Specify a headset volume level through a numeric value between 0 and 15.
    #: example: 10.0
    headset_volume: Optional[int] = None
    #: Enable/disable the wireless headset hookswitch control.
    #: example: True
    e_hook_enabled: Optional[bool] = None
    #: Enable/disable to preserve the existing values on the phone and not the values defined for the device settings.
    #: example: True
    allow_end_user_override_enabled: Optional[bool] = None


class CallForwardExpandedSoftKey(str, Enum):
    #: Set the default call forward expanded soft key behavior to single option.
    only_the_call_forward_all = 'ONLY_THE_CALL_FORWARD_ALL'
    #: Set the default call forward expanded soft key behavior to multiple menu option.
    all_call_forwards = 'ALL_CALL_FORWARDS'


class HttpProxyObjectMode(str, Enum):
    off = 'OFF'
    auto = 'AUTO'
    manual = 'MANUAL'


class HttpProxyObject(ApiModel):
    #: Mode of the HTTP proxy.
    #: example: OFF
    mode: Optional[HttpProxyObjectMode] = None
    #: Enable/disable auto discovery of the URL.
    #: example: True
    auto_discovery_enabled: Optional[bool] = None
    #: Specify the host URL if the HTTP mode is set to `MANUAL`.
    #: example: www.example.wxc
    host: Optional[str] = None
    #: Specify the port if the HTTP mode is set to `MANUAL`.
    #: example: 3128
    port: Optional[datetime] = None
    #: Specify PAC URL if auto discovery is disabled.
    #: example: www.example.wxc
    pack_url: Optional[str] = None
    #: Enable/disable authentication settings.
    #: example: True
    auth_settings_enabled: Optional[bool] = None
    #: Specify a username if authentication settings are enabled.
    #: example: john
    username: Optional[str] = None
    #: Specify a password if authentication settings are enabled.
    #: example: private
    password: Optional[str] = None


class BluetoothObjectMode(str, Enum):
    phone = 'PHONE'
    hands_free = 'HANDS_FREE'
    both = 'BOTH'


class BluetoothObject(ApiModel):
    #: Enable/disable Bluetooth.
    #: example: True
    enabled: Optional[bool] = None
    #: Select a Bluetooth mode.
    #: example: PHONE
    mode: Optional[BluetoothObjectMode] = None


class NoiseCancellationObject(ApiModel):
    #: Enable/disable the Noise Cancellation.
    #: example: True
    enabled: Optional[bool] = None
    #: Enable/disable to preserve the existing values on the phone and not the value defined for the device setting.
    #: example: True
    allow_end_user_override_enabled: Optional[bool] = None


class SoftKeyMenuObject(ApiModel):
    #: Specify the idle key list.
    #: example: guestin|;guestout|;acd_login|;acd_logout|;astate|;redial|;newcall|;cfwd|;recents|;dnd|;unpark|;psk1|;gpickup|;pickup|;dir|4;miss|5;selfview|;messages
    idle_key_list: Optional[str] = None
    #: Specify the off hook key list.
    #: example: endcall|1;redial|2;dir|3;lcr|4;unpark|5;pickup|6;gpickup|7
    off_hook_key_list: Optional[str] = None
    #: Specify the dialing input key list.
    #: example: dial|1;cancel|2;delchar|3;left|5;right|6
    dialing_input_key_list: Optional[str] = None
    #: Specify the progressing key list.
    #: example: endcall|2
    progressing_key_list: Optional[str] = None
    #: Specify the connected key list.
    #: example: hold;endcall;xfer;conf;xferLx;confLx;bxfer;phold;redial;dir;park;crdstart;crdstop;crdpause;crdresume
    connected_key_list: Optional[str] = None
    #: Specify the connected video key list.
    #: example: hold;endcall;xfer;conf;xferLx;confLx;bxfer;phold;redial;dir;park;crdstart;crdstop;crdpause;crdresume
    connected_video_key_list: Optional[str] = None
    #: Start the transfer key list.
    #: example: endcall|2;xfer|3
    start_transfer_key_list: Optional[str] = None
    #: Start the conference key list.
    #: example: endcall|2;conf|3
    start_conference_key_list: Optional[str] = None
    #: Specify the conferencing key list.
    #: example: endcall;join;crdstart;crdstop;crdpause;crdresume
    conferencing_key_list: Optional[str] = None
    #: Specify the releasing key list.
    #: example: endcall|2
    releasing_key_list: Optional[str] = None
    #: Specify the hold key list.
    #: example: resume|1;endcall|2;newcall|3;redial|4;dir|5
    hold_key_list: Optional[str] = None
    #: Specify the ringing key list.
    #: example: answer|1;ignore|2
    ringing_key_list: Optional[str] = None
    #: Specify the shared active key list.
    #: example: newcall|1;psk1|2;dir|3;back|4
    shared_active_key_list: Optional[str] = None
    #: Specify the shared held key list.
    #: example: resume|1;dir|4
    shared_held_key_list: Optional[str] = None


class PskObject(ApiModel):
    #: Specify PSK1.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk1: Optional[str] = None
    #: Specify PSK2.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk2: Optional[str] = None
    #: Specify PSK3.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk3: Optional[str] = None
    #: Specify PSK4.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk4: Optional[str] = None
    #: Specify PSK5.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk5: Optional[str] = None
    #: Specify PSK6.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk6: Optional[str] = None
    #: Specify PSK7.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk7: Optional[str] = None
    #: Specify PSK8.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk8: Optional[str] = None
    #: Specify PSK9.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk9: Optional[str] = None
    #: Specify PSK10.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk10: Optional[str] = None
    #: Specify PSK11.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk11: Optional[str] = None
    #: Specify PSK12.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk12: Optional[str] = None
    #: Specify PSK13.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk13: Optional[str] = None
    #: Specify PSK14.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk14: Optional[str] = None
    #: Specify PSK15.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk15: Optional[str] = None
    #: Specify PSK16.
    #: example: fnc=sd;ext=*11;nme=Call Pull
    psk16: Optional[str] = None


class SoftKeyLayoutObject(ApiModel):
    #: Customize SoftKey menu settings.
    soft_key_menu: Optional[SoftKeyMenuObject] = None
    #: Customize PSK.
    psk: Optional[PskObject] = None
    #: Default SoftKey menu settings.
    soft_key_menu_defaults: Optional[SoftKeyMenuObject] = None
    #: Default PSK.
    psk_defaults: Optional[PskObject] = None


class BackgroundImageColor(str, Enum):
    #: Indicates that dark cyan background image will be set for the devices.
    cyan_dark = 'CYAN_DARK'
    #: Indicates the dark purple background image will be set for the devices.
    purple_dark = 'PURPLE_DARK'
    #: Indicates the dark blue background image will be set for the devices.
    blue_dark = 'BLUE_DARK'
    #: Indicates the dark violet background image will be set for the devices.
    violet_dark = 'VIOLET_DARK'
    #: Indicates the light blue background image will be set for the devices.
    blue_light = 'BLUE_LIGHT'
    #: Indicates the light violet background image will be set for the devices.
    violet_light = 'VIOLET_LIGHT'


class BacklightTimer68XX(str, Enum):
    #: Keep the phone's backlight always on.
    always_on = 'ALWAYS_ON'
    #: Set the phone's backlight to be on for ten seconds.
    ten_sec = 'TEN_SEC'
    #: Set the phone's backlight to be on for twenty seconds.
    twenty_sec = 'TWENTY_SEC'
    #: Set the phone's backlight to be on for thirty seconds.
    thirty_sec = 'THIRTY_SEC'
    #: Keep the phone's backlight off.
    off = 'OFF'


class MppObject(ApiModel):
    #: Indicates whether the PNAC of MPP object is enabled or not.
    #: example: True
    pnac_enabled: Optional[bool] = None
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[MppAudioCodecPriorityObject] = None
    #: Choose the length of time (in minutes) for the phone's backlight to remain on.
    #: example: ONE_MIN
    backlight_timer: Optional[BacklightTimerObject] = None
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage] = None
    #: The display name that appears on the phone screen.
    #: example: PERSON_NUMBER
    display_name_format: Optional[DisplayNameSelection] = None
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool] = None
    #: Choose the desired logging level for an MPP devices.
    #: example: STANDARD
    default_logging_level: Optional[DefaultLoggingLevelObject] = None
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    #: example: True
    dnd_services_enabled: Optional[bool] = None
    #: Holds the Acd object value.
    acd: Optional[AcdObject] = None
    #: Indicates the short inter digit timer value.
    #: example: 14.0
    short_interdigit_timer: Optional[int] = None
    #: Indicates the long inter digit timer value..
    #: example: 16.0
    long_interdigit_timer: Optional[int] = None
    #: Line key labels define the format of what's shown next to line keys.
    #: example: PERSON_EXTENSION
    line_key_label_format: Optional[LineKeyLabelSelection] = None
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not supported on the MPP 8875
    #: example: DEFAULT
    line_key_ledpattern: Optional[LineKeyLEDPattern] = Field(alias='lineKeyLEDPattern', default=None)
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool] = None
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    #: example: True
    mpp_user_web_access_enabled: Optional[bool] = None
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    #: example: ['["192.86.108.226:22"]']
    multicast: Optional[list[str]] = None
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    #: example: 30.0
    off_hook_timer: Optional[int] = None
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your provisioned location.
    #: example: RUSSIAN
    phone_language: Optional[PhoneLanguage] = None
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[PoeMode] = None
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    #: example: True
    qos_enabled: Optional[bool] = None
    #: Specify the amount of inactive time needed (in seconds) before the phone's screen saver activates.
    screen_timeout: Optional[DectVlanObject] = None
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    #: example: True
    usb_ports_enabled: Optional[bool] = None
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObject] = None
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObject] = None
    #: Specify the call history information to use. Only applies to user devices.
    call_history: Optional[CallHistoryMethod] = None
    #: Specify the directory services to use.
    contacts: Optional[DirectoryMethod] = None
    #: Enable/disable the availability of the webex meetings functionality from the phone.
    #: example: True
    webex_meetings_enabled: Optional[bool] = None
    #: Specify all volume level values on the phone.
    volume_settings: Optional[VolumeSettingsObject] = None
    #: Specify the call forward expanded soft key behavior.
    cf_expanded_soft_key: Optional[CallForwardExpandedSoftKey] = None
    #: Specify HTTP Proxy values.
    http_proxy: Optional[HttpProxyObject] = None
    #: Enable/disable the visibility of the bluetooth menu on the MPP device.
    bluetooth: Optional[BluetoothObject] = None
    #: Enable/disable the use of the PC passthrough ethernet port on supported phone models.
    #: example: True
    pass_through_port_enabled: Optional[bool] = None
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the device.
    #: example: True
    user_password_override_enabled: Optional[bool] = None
    #: Enable/disable the default screen behavior when inbound calls are received.
    #: example: True
    active_call_focus_enabled: Optional[bool] = None
    #: Enable/disable peer firmware sharing.
    #: example: True
    peer_firmware_enabled: Optional[bool] = None
    #: Enable/disable local noise cancellation on active calls from the device.
    noise_cancellation: Optional[NoiseCancellationObject] = None
    #: Enable/disable visibility of the Accessibility Voice Feedback menu on the MPP device.
    #: example: True
    voice_feedback_accessibility_enabled: Optional[bool] = None
    #: Enable/disable availability of dial assist feature on the phone.
    #: example: True
    dial_assist_enabled: Optional[bool] = None
    #: Specify the number of calls per unique line appearance on the phone.
    #: example: 9.0
    calls_per_line: Optional[int] = None
    #: Enable/disable automatic nightly configuration resync of the MPP device.
    #: example: True
    nightly_resync_enabled: Optional[bool] = None
    #: Enable/disable the visual indication of missed calls.
    #: example: True
    missed_call_notification_enabled: Optional[bool] = None
    #: Specify the softkey layout per phone menu state.
    soft_key_layout: Optional[SoftKeyLayoutObject] = None
    #: Specify the image option for the MPP 8875 phone background.
    background_image8875: Optional[BackgroundImageColor] = None
    #: Specify the use of the backlight feature on 6800 nad 7800 series devices.
    backlight_timer68_xx78_xx: Optional[BacklightTimer68XX] = Field(alias='backlightTimer68XX78XX', default=None)


class CommSecurityType(str, Enum):
    #: Sets the LDAP server security protocol to None.
    none_ = 'NONE'
    #: Sets the LDAP server security protocol to SSL.
    ssl = 'SSL'
    #: Sets the LDAP server security protocol to STARTTLS.
    starttls = 'STARTTLS'


class LdapObject(ApiModel):
    #: Sets the values needed to enable use of the LDAP service on the phone.
    enabled: Optional[bool] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: localhost
    server_address: Optional[str] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: 8080.0
    server_port: Optional[int] = None
    #: Indicates the selection of the protocol for LDAP service on the phone.
    #: example: SSL
    comm_security_type: Optional[CommSecurityType] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: bindDn
    bind_dn: Optional[str] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: bindPw
    bind_pw: Optional[str] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: baseDn
    base_dn: Optional[str] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: primaryEmailAttribute
    primary_email_attribute: Optional[str] = None
    #: Sets the values needed to enable use of the LDAP service on the phone.
    #: example: alternateEmailAttribute
    alternate_email_attribute: Optional[str] = None


class WebAccessObject(ApiModel):
    #: Ability to enable or disable the web browser access for the 840/860.
    enabled: Optional[bool] = None
    #: Ability to set a Web Server Password.
    #: example: password
    password: Optional[str] = None


class WifiObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject] = None
    #: Set the values needed to enable use of the LDAP service on the phone.
    ldap: Optional[LdapObject] = None
    #: Set the availability of the local end user web access for an 840/860 WiFi phone.
    web_access: Optional[WebAccessObject] = None
    #: Set the local security password on an 840/860 WiFi phone.
    #: example: phoneSecurityPwd
    phone_security_pwd: Optional[str] = None


class CustomizationObject(ApiModel):
    #: Settings that are applicable to ATA devices.
    ata: Optional[AtaObject] = None
    #: Settings that are applicable to DECT devices.
    dect: Optional[DectObject] = None
    #: Settings that are applicable to MPP devices.
    mpp: Optional[MppObject] = None
    #: Settings that are applicable to WiFi.
    wifi: Optional[WifiObject] = None


class AdminBatchStartJobObjectLocationCustomizations(ApiModel):
    #: Location within an organization where changes of device setings will be applied to all the devices within it.
    #: example: 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA'
    location_id: Optional[str] = None
    #: Indicates if all the devices within this location will be customized with new requested customizations(if set to `true`) or will be overridden with the one at organization level (if set to `false` or any other value). This field has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool] = None
    #: Indicates the settings for ATA devices, DECT devices and MPP devices.
    customizations: Optional[CustomizationObject] = None


class CountObject(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int] = None


class CustomizationDeviceLevelObject(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObject] = None
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObject] = None
    #: Applicable device settings for a WiFi device.
    wifi: Optional[WifiObject] = None


class UsbPortsObject(ApiModel):
    #: New Control to Enable/Disable the side USB port.
    enabled: Optional[bool] = None
    #: Enable/disable use of the side USB port on the MPP device. Enabled by default.
    #: example: True
    side_usb_enabled: Optional[bool] = None
    #: Enable/disable use of the rear USB port on the MPP device.
    #: example: True
    rear_usb_enabled: Optional[bool] = None


class MppObjectDevice(ApiModel):
    #: Indicates whether the PNAC of MPP object is enabled or not.
    #: example: True
    pnac_enabled: Optional[bool] = None
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject] = None
    #: Choose the length of time (in minutes) for the phone's backlight to remain on.
    #: example: ONE_MIN
    backlight_timer: Optional[BacklightTimerObject] = None
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage] = None
    #: The display name that appears on the phone screen.
    #: example: PERSON_NUMBER
    display_name_format: Optional[DisplayNameSelection] = None
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool] = None
    #: Choose the desired logging level for an MPP devices.
    #: example: STANDARD
    default_logging_level: Optional[DefaultLoggingLevelObject] = None
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    #: example: True
    dnd_services_enabled: Optional[bool] = None
    #: Holds the Acd object value.
    acd: Optional[AcdObject] = None
    #: Indicates the short inter digit timer value.
    #: example: 14.0
    short_interdigit_timer: Optional[int] = None
    #: Indicates the long inter digit timer value..
    #: example: 16.0
    long_interdigit_timer: Optional[int] = None
    #: Line key labels define the format of what's shown next to line keys.
    #: example: PERSON_EXTENSION
    line_key_label_format: Optional[LineKeyLabelSelection] = None
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not supported on the MPP 8875
    #: example: DEFAULT
    line_key_ledpattern: Optional[LineKeyLEDPattern] = Field(alias='lineKeyLEDPattern', default=None)
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool] = None
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    #: example: True
    mpp_user_web_access_enabled: Optional[bool] = None
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    #: example: ['["192.86.108.226:22"]']
    multicast: Optional[list[str]] = None
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    #: example: 30.0
    off_hook_timer: Optional[int] = None
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your provisioned location.
    #: example: RUSSIAN
    phone_language: Optional[PhoneLanguage] = None
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[PoeMode] = None
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    #: example: True
    qos_enabled: Optional[bool] = None
    #: Specify the amount of inactive time needed (in seconds) before the phone's screen saver activates.
    screen_timeout: Optional[DectVlanObject] = None
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    #: example: True
    usb_ports_enabled: Optional[bool] = None
    #: By default the Side USB port is enabled to support KEMs and other peripheral devices. Use the option to disable use of this port.
    usb_ports: Optional[UsbPortsObject] = None
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObject] = None
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObject] = None
    #: Specify the call history information to use. Only applies to user devices.
    call_history: Optional[CallHistoryMethod] = None
    #: Specify the directory services to use.
    contacts: Optional[DirectoryMethod] = None
    #: Enable/disable the availability of the webex meetings functionality from the phone.
    #: example: True
    webex_meetings_enabled: Optional[bool] = None
    #: Specify all volume level values on the phone.
    volume_settings: Optional[VolumeSettingsObject] = None
    #: Specify the call forward expanded soft key behavior.
    cf_expanded_soft_key: Optional[CallForwardExpandedSoftKey] = None
    #: Specify HTTP Proxy values.
    http_proxy: Optional[HttpProxyObject] = None
    #: Enable/disable the visibility of the bluetooth menu on the MPP device.
    bluetooth: Optional[BluetoothObject] = None
    #: Enable/disable the use of the PC passthrough ethernet port on supported phone models.
    #: example: True
    pass_through_port_enabled: Optional[bool] = None
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the device.
    #: example: True
    user_password_override_enabled: Optional[bool] = None
    #: Enable/disable the default screen behavior when inbound calls are received.
    #: example: True
    active_call_focus_enabled: Optional[bool] = None
    #: Enable/disable peer firmware sharing.
    #: example: True
    peer_firmware_enabled: Optional[bool] = None
    #: Enable/disable local noise cancellation on active calls from the device.
    noise_cancellation: Optional[NoiseCancellationObject] = None
    #: Enable/disable visibility of the Accessibility Voice Feedback menu on the MPP device.
    #: example: True
    voice_feedback_accessibility_enabled: Optional[bool] = None
    #: Enable/disable availability of dial assist feature on the phone.
    #: example: True
    dial_assist_enabled: Optional[bool] = None
    #: Specify the number of calls per unique line appearance on the phone.
    #: example: 9.0
    calls_per_line: Optional[int] = None
    #: Enable/disable automatic nightly configuration resync of the MPP device.
    #: example: True
    nightly_resync_enabled: Optional[bool] = None
    #: Enable/disable the visual indication of missed calls.
    #: example: True
    missed_call_notification_enabled: Optional[bool] = None
    #: Specify the softkey layout per phone menu state.
    soft_key_layout: Optional[SoftKeyLayoutObject] = None
    #: Specify the image option for the MPP 8875 phone background.
    background_image8875: Optional[BackgroundImageColor] = None
    #: Specify the use of the backlight feature on 6800 nad 7800 series devices.
    backlight_timer68_xx78_xx: Optional[BacklightTimer68XX] = Field(alias='backlightTimer68XX78XX', default=None)


class WifiObjectDevice(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[MppAudioCodecPriorityObject] = None
    #: Set the values needed to enable use of the LDAP service on the phone.
    ldap: Optional[LdapObject] = None
    #: Set the availability of the local end user web access for an 840/860 WiFi phone.
    web_access: Optional[WebAccessObject] = None
    #: Set the local security password on an 840/860 WiFi phone.
    #: example: phoneSecurityPwd
    phone_security_pwd: Optional[str] = None


class CustomizationDeviceLevelObjectDevice(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObject] = None
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObjectDevice] = None
    #: Applicable device settings for a WiFi device.
    wifi: Optional[WifiObjectDevice] = None


class DectDeviceList(ApiModel):
    #: Model name of the device.
    #: example: DMS Cisco DBS110
    model: Optional[str] = None
    #: Display name of the device.
    #: example: Cisco DECT 210 Base
    display_name: Optional[str] = None
    #: Indicates number of base stations.
    #: example: 250.0
    number_of_base_stations: Optional[int] = None
    #: Indicates number of port lines,
    #: example: 1000.0
    number_of_line_ports: Optional[int] = None
    #: Indicates number of supported registrations.
    #: example: 30.0
    number_of_registrations_supported: Optional[int] = None


class TypeObject(str, Enum):
    #: Cisco Multiplatform Phone
    mpp = 'MPP'
    #: Analog Telephone Adapters
    ata = 'ATA'
    #: GENERIC Session Initiation Protocol
    generic_sip = 'GENERIC_SIP'
    #: Esim Supported Webex Go
    esim = 'ESIM'


class ManufacturerObject(str, Enum):
    #: Devices manufactured by Cisco.
    cisco = 'CISCO'
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for provisioning in the control hub.
    third_party = 'THIRD_PARTY'


class ManagedByObject(str, Enum):
    #: Devices managed by Cisco.
    cisco = 'CISCO'
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the control hub.
    customer = 'CUSTOMER'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'


class OnboardingMethodObject(str, Enum):
    mac_address = 'MAC_ADDRESS'
    activation_code = 'ACTIVATION_CODE'
    none_ = 'NONE'


class KemModuleTypeObject(str, Enum):
    kem_14_keys = 'KEM_14_KEYS'
    kem_18_keys = 'KEM_18_KEYS'


class DeviceObject(ApiModel):
    #: Model name of the device.
    #: example: 2N Customer Managed
    model: Optional[str] = None
    #: Display name of the device.
    #: example: 2N Customer Managed
    display_name: Optional[str] = None
    #: Type of the device.
    #: example: GENERIC_SIP
    type: Optional[TypeObject] = None
    #: Manufacturer of the device.
    #: example: THIRD_PARTY
    manufacturer: Optional[ManufacturerObject] = None
    #: Users who manage the device.
    #: example: CUSTOMER
    managed_by: Optional[ManagedByObject] = None
    #: List of places the device is supported for.
    supported_for: Optional[list[MemberType]] = None
    #: Onboarding method.
    onboarding_method: Optional[list[OnboardingMethodObject]] = None
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: Optional[bool] = None
    #: Number of port lines.
    number_of_line_ports: Optional[int] = None
    #: Indicates whether Kem support is enabled or not.
    #: example: True
    kem_support_enabled: Optional[bool] = None
    #: Module count.
    kem_module_count: Optional[int] = None
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleTypeObject]] = None
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool] = None
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str] = None
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool] = None
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool] = None
    #: Enables / disables customized behavior support on devices.
    customized_behaviors_enabled: Optional[bool] = None
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool] = None
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool] = None


class DeviceSettingsObject(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObject] = None
    #: Indicates if customization is allowed at a location level. If `true`, customized at a location level. If `false`, not customized; uses customer-level configuration.
    #: example: True
    custom_enabled: Optional[bool] = None
    #: Customer devices setting update status. If `true`, an update is in progress (no further changes are allowed). `If false`, no update in progress (changes are allowed).
    #: example: True
    update_in_progress: Optional[bool] = None
    #: Number of devices that will be updated.
    #: example: 9.0
    device_count: Optional[int] = None
    #: Indicates the last updated time.
    #: example: 1659624763665.0
    last_update_time: Optional[int] = None


class DeviceSettingsObjectForDeviceLevel(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObjectDevice] = None
    #: Indicates if customization is allowed at a device level. If `true`, customized at a device level. If `false`, not customized; uses customer-level configuration.
    #: example: True
    custom_enabled: Optional[bool] = None
    #: Customer devices setting update status. If `true`, an update is in progress (no further changes are allowed). `If false`, no update in progress (changes are allowed).
    #: example: True
    update_in_progress: Optional[bool] = None
    #: Number of devices that will be updated.
    #: example: 9.0
    device_count: Optional[int] = None
    #: Indicates the last updated time.
    #: example: 1659624763665.0
    last_update_time: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target location ID.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[ErrorObject] = None


class ErrorResponseObject(ApiModel):
    items: Optional[list[ItemObject]] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class Location(ApiModel):
    #: Location identifier associated with the members.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzJiNDkyZmZkLTRjNGItNGVmNS04YzAzLWE1MDYyYzM4NDA5Mw
    id: Optional[str] = None
    #: Location name associated with the member.
    #: example: MainOffice
    name: Optional[str] = None


class MemberObject(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: First name of a person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will be supported in a future update.
    #: example: 2055552221
    phone_number: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 000
    extension: Optional[str] = None
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Port number assigned to person or workspace.
    #: example: 1.0
    port: Optional[int] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1.0
    line_weight: Optional[int] = None
    #: Registration Host IP address for the line port.
    #: example: 10.0.0.45
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration Remote IP address for the line port.
    #: example: 192.102.12.84
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: The preconfigured number for Hotline. Required only if `hotlineEnabled` is set to true.
    #: example: +12055552222
    hotline_destination: Optional[str] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None
    #: SIP username used in SIP signaling, for example, in registration.
    #: example: evypzco5ds@55552222.int10.bcld.webex.com
    line_port: Optional[str] = None
    #: Indicates if the member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class GetMemberResponse(ApiModel):
    #: Model type of the device.
    #: example: DMS Cisco 192
    model: Optional[str] = None
    #: List of members that appear on the device.
    members: Optional[list[MemberObject]] = None
    #: Maximum number of lines available for the device.
    #: example: 10.0
    max_line_count: Optional[int] = None


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this host(workspace device) and use this device
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool] = None
    #: Enable limiting the time a guest can use the device. The time limit is configured via `guestHoursLimit`.
    limit_guest_use: Optional[bool] = None
    #: Time Limit in hours until hoteling is enabled. Mandatory if `limitGuestUse` is enabled.
    guest_hours_limit: Optional[int] = None


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    start_time: Optional[str] = None
    #: Step execution end time in UTC format.
    end_time: Optional[str] = None
    #: Last updated time for a step in UTC format.
    last_updated: Optional[str] = None
    #: Displays status for a step.
    status_message: Optional[str] = None
    #: Exit Code for a step.
    exit_code: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None


class StartJobResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    job_type: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Indicates operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class JobListResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[StartJobResponse]] = None


class ListDectDeviceType(ApiModel):
    #: Contains a list of devices.
    devices: Optional[list[DectDeviceList]] = None


class ListDeviceSettingsObject(ApiModel):
    #: Customization object of the device settings.
    customizations: Optional[CustomizationObject] = None
    #: Progress of the device update.
    update_in_progress: Optional[bool] = None
    #: Device count.
    #: example: 22.0
    device_count: Optional[int] = None
    #: Last updated time.
    #: example: 1659624763665.0
    last_update_time: Optional[int] = None


class MACAddressResponseStatus(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class MacStatusObjectState(str, Enum):
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
    #: example: 00005E0053B4
    mac: Optional[str] = None
    #: State of the MAC address.
    #: example: UNAVAILABLE
    state: Optional[MacStatusObjectState] = None
    #: MAC address validation error code.
    #: example: 5675.0
    error_code: Optional[int] = None
    #: Provides a status message about the MAC address.
    #: example: [Error 5675] MAC Address is in use.
    message: Optional[str] = None


class MACAddressResponse(ApiModel):
    #: Status of MAC address.
    #: example: ERRORS
    status: Optional[MACAddressResponseStatus] = None
    #: Contains an array of all the MAC address provided and their statuses.
    mac_status: Optional[list[MacStatusObject]] = None


class PutDeviceSettingsRequest(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObjectDevice] = None
    #: Indicates if customization is allowed at a device level. If true, customized at a device level. If false, not customized; uses customer-level configuration.
    #: example: True
    custom_enabled: Optional[bool] = None


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    #: example: 1.0
    port: Optional[int] = None
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1.0
    line_weight: Optional[int] = None
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: The preconfigured number for Hotline. Required only if `hotlineEnabled` is set to true.
    #: example: +12055552222
    hotline_destination: Optional[str] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None


class PutMembersRequest(ApiModel):
    #: If the member's list is missing then all the users are removed except the primary user.
    members: Optional[list[PutMemberObject]] = None


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: First name of a person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone Number of a person or workspace.
    #: example: +12055552221
    phone_number: Optional[str] = None
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Indicates if member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class SearchMemberResponse(ApiModel):
    #: List of members available for the device.
    members: Optional[list[SearchMemberObject]] = None


class ValidateMACRequest(ApiModel):
    #: MAC addresses to be validated.
    #: example: ['{["ab125678cdef"', '"00005E0053B4"]}']
    macs: Optional[list[str]] = None


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str] = None
    #: Enumeration that indicates if the member is of type `PEOPLE` or `PLACE`.
    type: Optional[MemberType] = None
    #: First name of device owner.
    first_name: Optional[str] = None
    #: Last name of device owner.
    last_name: Optional[str] = None


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ip_address: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Owner of device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of device.
    activation_state: Optional[ActivationStates] = None


class DeviceList(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]] = None
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int] = None


class JobIdResponseObject(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    job_type: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Indicates the operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: The location name for which the job was run.
    source_location_name: Optional[str] = None
    #: The location name for which the numbers have been moved.
    target_location_name: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class PlaceDevices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ip_address: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary Line/Port of the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Indicates Hoteling details of a device.
    hoteling: Optional[Hoteling] = None
    #: Owner of the device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of a device.
    activation_state: Optional[ActivationStates] = None


class PlaceDeviceList(ApiModel):
    #: Array of devices associated to a workspace.
    devices: Optional[list[PlaceDevices]] = None
    #: Maximum number of devices a workspace can be assigned to.
    max_device_count: Optional[int] = None


class SupportedDevicesObject(ApiModel):
    #: List of supported devices.
    devices: Optional[list[DeviceObject]] = None
