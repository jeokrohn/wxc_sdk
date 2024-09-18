from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AcdObject', 'ActivationStates', 'ApplyLineKeyTemplateJobDetails', 'ApplyLineKeyTemplateJobErrors',
           'AtaDtmfMethodObject', 'AtaDtmfModeObject', 'AtaObject', 'AudioCodecPriorityObject',
           'AuthenticationMethodObject', 'BackgroundImage', 'BackgroundImageColor', 'BacklightTimer68XX',
           'BacklightTimerObject', 'BluetoothObject', 'BluetoothObjectMode', 'CallForwardExpandedSoftKey',
           'CallHistoryMethod', 'CommSecurityType', 'Compression', 'CountObject', 'CustomizationDeviceLevelObject',
           'CustomizationDeviceLevelObjectDevice', 'CustomizationObject', 'DectDeviceList', 'DectObject',
           'DectVlanObject', 'DefaultLoggingLevelObject', 'DeleteDeviceBackgroundImagesResponse',
           'DeleteImageRequestObject', 'DeleteImageResponseSuccessObject', 'DeleteImageResponseSuccessObjectResult',
           'DeviceActivationStates', 'DeviceCallSettingsApi', 'DeviceLayout', 'DeviceList', 'DeviceObject',
           'DeviceOwner', 'DeviceSettingsConfigurationObject', 'DeviceSettingsObject',
           'DeviceSettingsObjectForDeviceLevel', 'DeviceType', 'Devices', 'DirectoryMethod',
           'DisplayCallqueueAgentSoftkeysObject', 'DisplayNameSelection', 'EnhancedMulticastObject',
           'ErrorMessageObject', 'ErrorObject', 'GetLineKeyTemplateResponse', 'GetMemberResponse',
           'GetThirdPartyDeviceObject', 'GetThirdPartyDeviceObjectOwner', 'GetThirdPartyDeviceObjectProxy',
           'Hoteling', 'HttpProxyObject', 'HttpProxyObjectMode', 'ItemObject', 'JobExecutionStatusObject',
           'JobExecutionStatusObject1', 'JobIdResponseObject', 'KEMKeys', 'KemModuleType', 'LatestExecutionStatus',
           'LayoutMode', 'LdapObject', 'LineKeyLEDPattern', 'LineKeyLabelSelection', 'LineKeyTemplateAdvisoryTypes',
           'LineKeyTemplatesResponse', 'LineKeyType', 'LineType', 'ListBackgroundImagesObject',
           'ListDeviceSettingsObject', 'Location', 'MACAddressResponse', 'MACAddressResponseStatus',
           'MacStatusObject', 'MacStatusObjectState', 'ManagedByObject', 'ManufacturerObject', 'MemberObject',
           'MemberType', 'MppAudioCodecPriorityObject', 'MppObject', 'MppObjectDevice', 'MppVlanObject',
           'MulticastObject', 'NoiseCancellationObject', 'OnboardingMethodObject', 'PhoneLanguage', 'PlaceDeviceList',
           'PlaceDevices', 'PoeMode', 'PostApplyLineKeyTemplateRequestAction', 'ProgrammableLineKeys', 'PskObject',
           'PutMemberObject', 'ReadTheListOfBackgroundImagesResponse', 'RebuildPhonesJob', 'SearchMemberObject',
           'SearchMembersUsageType', 'SelectionType', 'SnmpObject', 'SoftKeyLayoutObject', 'SoftKeyMenuObject',
           'StartJobResponse', 'StartJobResponseLatestExecutionExitCode', 'StepExecutionStatusesObject',
           'SupportedForObject', 'SupportsLogCollectionObject', 'TypeObject', 'UploadADeviceBackgroundImageResponse',
           'UsbPortsObject', 'UserDeviceCount', 'VolumeSettingsObject', 'WebAccessObject', 'WifiNetworkObject',
           'WifiObject', 'WifiObjectDevice']


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
    #: Device is activating using an activation code.
    activating = 'activating'
    #: Device has been activated using an activation code.
    activated = 'activated'
    #: Device has not been activated using an activation code.
    deactivated = 'deactivated'


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
    #: Read-write community string that protects the device against unauthorized changes. Must never be set to
    #: `public`.
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
    #: Enable/disable phone's default behavior regarding the nightly maintenance synchronization with the Webex Calling
    #: platform.
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
    #: When this option is selected, a field 'Custom Background URL' needs to be added with the image url. URLs
    #: provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url = 'customUrl'


class DisplayNameSelection(str, Enum):
    #: Indicates that devices will display the person's phone number, or if a person doesn't have a phone number, the
    #: location number will be displayed.
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
    #: This will display the person extension, or if a person doesn't have an extension, the person's first name will
    #: be displayed.
    person_extension = 'PERSON_EXTENSION'
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name = 'PERSON_FIRST_THEN_LAST_NAME'
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name = 'PERSON_LAST_THEN_FIRST_NAME'


class LineKeyLEDPattern(str, Enum):
    default = 'DEFAULT'
    preset_1 = 'PRESET_1'


class MulticastObject(ApiModel):
    #: Specify the multicast group URL and listening port.
    #: example: 224.0.0.0:22
    host_and_port: Optional[str] = None
    #: Specify whether the multicast group URL has an XML application URL.
    #: example: True
    has_xml_app_url: Optional[bool] = None
    #: Specify the timeout for the XML application.
    #: example: 10
    xml_app_timeout: Optional[int] = None


class EnhancedMulticastObject(ApiModel):
    #: Specify the URL for the XML application.
    #: example: http://127.0.0.1:8080/
    xml_app_url: Optional[str] = None
    #: Specify up to 10 multicast group URLs each with a unique listening port, an XML application URL, and a timeout.
    multicast_list: Optional[list[MulticastObject]] = None


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
    #: example: 1
    value: Optional[int] = None
    #: Indicates the PC port value of a VLAN object for an MPP object.
    #: example: 1
    pc_port: Optional[int] = None


class AuthenticationMethodObject(str, Enum):
    #: No authentication.
    none_ = 'NONE'
    #: Extensible Authentication Protocol-Flexible Authentication via Secure Tunneling. Requires username and password
    #: authentication.
    eap_fast = 'EAP_FAST'
    #: Protected Extensible Authentication Protocol - Generic Token Card. Requires username and password
    #: authentication.
    peap_gtc = 'PEAP_GTC'
    #: Protected Extensible Authentication Protocol - Microsoft Challenge Handshake Authentication Protocol version 2.
    #: Requires username and password authentication.
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
    #: example: 9
    ringer_volume: Optional[int] = None
    #: Specify a speaker volume level through a numeric value between 0 and 15.
    #: example: 11
    speaker_volume: Optional[int] = None
    #: Specify a handset volume level through a numeric value between 0 and 15.
    #: example: 10
    handset_volume: Optional[int] = None
    #: Specify a headset volume level through a numeric value between 0 and 15.
    #: example: 10
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
    port: Optional[str] = None
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
    #: example: 14
    short_interdigit_timer: Optional[int] = None
    #: Indicates the long inter digit timer value..
    #: example: 16
    long_interdigit_timer: Optional[int] = None
    #: Line key labels define the format of what's shown next to line keys.
    #: example: PERSON_EXTENSION
    line_key_label_format: Optional[LineKeyLabelSelection] = None
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not
    #: supported on the MPP 8875
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
    #: Specify the enhanced multicast settings for the MPP device.
    enhanced_multicast: Optional[EnhancedMulticastObject] = None
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    #: example: 30
    off_hook_timer: Optional[int] = None
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
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
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the
    #: device.
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
    #: example: 9
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
    #: Enable/disable monitoring for MPP non-primary device.
    allow_monitor_lines_enabled: Optional[bool] = None
    #: Enable/disable SIP media streams to go directly between phones on the same local network.
    #: example: True
    ice_enabled: Optional[bool] = None


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
    #: example: 8080
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


class Compression(str, Enum):
    #: Minimize data use during compression.
    on = 'ON'
    #: Ignore data use during compression.
    off = 'OFF'


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
    #: example: 14
    short_interdigit_timer: Optional[int] = None
    #: Indicates the long inter digit timer value..
    #: example: 16
    long_interdigit_timer: Optional[int] = None
    #: Line key labels define the format of what's shown next to line keys.
    #: example: PERSON_EXTENSION
    line_key_label_format: Optional[LineKeyLabelSelection] = None
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not
    #: supported on the MPP 8875
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
    #: Specify the enhanced multicast settings for the MPP device.
    enhanced_multicast: Optional[EnhancedMulticastObject] = None
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    #: example: 30
    off_hook_timer: Optional[int] = None
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
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
    #: By default the Side USB port is enabled to support KEMs and other peripheral devices. Use the option to disable
    #: use of this port.
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
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the
    #: device.
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
    #: example: 9
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
    #: Enable/disable monitoring for MPP non-primary device.
    allow_monitor_lines_enabled: Optional[bool] = None
    #: Enable/disable SIP media streams to go directly between phones on the same local network.
    #: example: True
    ice_enabled: Optional[bool] = None


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
    #: example: 250
    number_of_base_stations: Optional[int] = None
    #: Indicates number of port lines,
    #: example: 1000
    number_of_line_ports: Optional[int] = None
    #: Indicates number of supported registrations.
    #: example: 30
    number_of_registrations_supported: Optional[int] = None


class DeviceActivationStates(str, Enum):
    #: Indicates a device is activating.
    activating = 'ACTIVATING'
    #: Indicates a device is activated.
    activated = 'ACTIVATED'
    #: Indicates a device is deactivated.
    deactivated = 'DEACTIVATED'


class TypeObject(str, Enum):
    #: Cisco Multiplatform Phone
    mpp = 'MPP'
    #: Analog Telephone Adapters
    ata = 'ATA'
    #: GENERIC Session Initiation Protocol
    generic_sip = 'GENERIC_SIP'
    #: Esim Supported Webex Go
    esim = 'ESIM'
    #: Desk Phone
    desk_phone = 'DESK_PHONE'


class ManufacturerObject(str, Enum):
    #: Devices manufactured by Cisco.
    cisco = 'CISCO'
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for
    #: provisioning in the control hub.
    third_party = 'THIRD_PARTY'


class ManagedByObject(str, Enum):
    #: Devices managed by Cisco.
    cisco = 'CISCO'
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the
    #: control hub.
    customer = 'CUSTOMER'


class SupportedForObject(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'


class OnboardingMethodObject(str, Enum):
    mac_address = 'MAC_ADDRESS'
    activation_code = 'ACTIVATION_CODE'
    none_ = 'NONE'


class KemModuleType(str, Enum):
    #: Extension module has 14 line keys that can be configured.
    kem_14_keys = 'KEM_14_KEYS'
    #: Extension module has 18 line keys that can be configured.
    kem_18_keys = 'KEM_18_KEYS'
    #: Extension module has 20 line keys that can be configured.
    kem_20_keys = 'KEM_20_KEYS'


class DeviceSettingsConfigurationObject(str, Enum):
    #: Devices which supports Webex Calling Device Settings Configuration.
    webex_calling_device_configuration = 'WEBEX_CALLING_DEVICE_CONFIGURATION'
    #: Devices which supports Webex Device Settings Configuration.
    webex_device_configuration = 'WEBEX_DEVICE_CONFIGURATION'
    #: Devices does not support any configuration.
    none_ = 'NONE'


class SupportsLogCollectionObject(str, Enum):
    #: Devices which does not support log collection.
    none_ = 'NONE'
    #: Devices which supports Cisco PRT log collection.
    cisco_prt = 'CISCO_PRT'
    #: Devices which supports Cisco RoomOS log collection.
    cisco_roomos = 'CISCO_ROOMOS'


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
    supported_for: Optional[list[SupportedForObject]] = None
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
    #: Enables / disables Kem lines support.
    kem_lines_support_enabled: Optional[bool] = None
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleType]] = None
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
    #: Enables / disables support line port reordering.
    supports_line_port_reordering_enabled: Optional[bool] = None
    #: Enables / disables port number support.
    port_number_support_enabled: Optional[bool] = None
    #: Enables / disables T.38.
    t38_enabled: Optional[bool] = None
    #: Enables / disables call declined.
    call_declined_enabled: Optional[bool] = None
    #: Supports touch screen on device.
    touch_screen_phone: Optional[bool] = None
    #: Number of line key buttons for a device.
    number_of_line_key_buttons: Optional[int] = None
    #: Device settings configuration.
    device_settings_configuration: Optional[DeviceSettingsConfigurationObject] = None
    #: Enables / disables hoteling host.
    allow_hoteling_host_enabled: Optional[bool] = None
    #: Device log collection configuration.
    supports_log_collection: Optional[SupportsLogCollectionObject] = None
    #: Enables / disables apply changes.
    supports_apply_changes_enabled: Optional[bool] = None
    #: Enables / disables configure lines.
    allow_configure_lines_enabled: Optional[bool] = None
    #: Enables / disables configure phone settings.
    allow_configure_phone_settings_enabled: Optional[bool] = None
    #: Enables / disables hotline support.
    supports_hotline_enabled: Optional[bool] = None


class DeviceSettingsObject(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObject] = None
    #: Indicates if customization is allowed at a location level. If `true`, customized at a location level. If
    #: `false`, not customized; uses customer-level configuration.
    #: example: True
    custom_enabled: Optional[bool] = None
    #: Customer devices setting update status. If `true`, an update is in progress (no further changes are allowed).
    #: `If false`, no update in progress (changes are allowed).
    #: example: True
    update_in_progress: Optional[bool] = None
    #: Number of devices that will be updated.
    #: example: 9
    device_count: Optional[int] = None
    #: Indicates the last updated time.
    #: example: 1659624763665
    last_update_time: Optional[int] = None


class DeviceSettingsObjectForDeviceLevel(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObjectDevice] = None
    #: Indicates if customization is allowed at a device level. If `true`, customized at a device level. If `false`,
    #: not customized; uses customer-level configuration.
    #: example: True
    custom_enabled: Optional[bool] = None
    #: Customer devices setting update status. If `true`, an update is in progress (no further changes are allowed).
    #: `If false`, no update in progress (changes are allowed).
    #: example: True
    update_in_progress: Optional[bool] = None
    #: Number of devices that will be updated.
    #: example: 9
    device_count: Optional[int] = None
    #: Indicates the last updated time.
    #: example: 1659624763665
    last_update_time: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    #: location ID.
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


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'
    #: Indicates the associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


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
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will
    #: be supported in a future update.
    #: example: 2055552221
    phone_number: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 000
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234000
    esn: Optional[str] = None
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary
    #: Line/Port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Port number assigned to person or workspace.
    #: example: 1
    port: Optional[int] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
    line_weight: Optional[int] = None
    #: Registration Host IP address for the line port.
    #: example: 10.0.0.45
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration Remote IP address for the line port.
    #: example: 192.102.12.84
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: The preconfigured number for Hotline. Required only if `hotlineEnabled` is set to true.
    #: example: +12055552222
    hotline_destination: Optional[str] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
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
    #: example: 10
    max_line_count: Optional[int] = None


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this
    #: host(workspace device) and use this device
    #: 
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive
    #: calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool] = None
    #: Enable limiting the time a guest can use the device. The time limit is configured via `guestHoursLimit`.
    limit_guest_use: Optional[bool] = None
    #: Time Limit in hours until hoteling is enabled. Mandatory if `limitGuestUse` is enabled.
    guest_hours_limit: Optional[int] = None


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    #: example: 1998857
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T03:58:36.886Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T03:58:48.471Z
    end_time: Optional[datetime] = None
    #: Last updated time for a step in UTC format.
    #: example: 2024-03-13T03:58:48.472Z
    last_updated: Optional[datetime] = None
    #: Displays the status of a step.
    #: example: COMPLETED
    status_message: Optional[str] = None
    #: Exit Code for a step.
    #: example: COMPLETED
    exit_code: Optional[str] = None
    #: Name of different steps the job goes through.
    #: example: rebuildphonesProcess
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    #: example: PT11.585S
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    #: example: 436272
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    end_time: Optional[datetime] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    #: example: 2024-03-13T14:57:04.678Z
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    #: example: STARTING
    status_message: Optional[str] = None
    #: Exit Code for a job.
    #: example: UNKNOWN
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    created_time: Optional[datetime] = None
    #: Time lapsed since the job execution started.
    #: example: PT0S
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


class StartJobResponseLatestExecutionExitCode(str, Enum):
    #: Job is in progress.
    unknown = 'UNKNOWN'
    #: Job has completed successfully.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'
    #: Job has been stopped.
    stopped = 'STOPPED'
    #: Job has completed with errors.
    completed_with_errors = 'COMPLETED_WITH_ERRORS'


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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[StartJobResponseLatestExecutionExitCode] = None
    #: Indicates operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class ListDeviceSettingsObject(ApiModel):
    #: Customization object of the device settings.
    customizations: Optional[CustomizationObject] = None
    #: Progress of the device update.
    update_in_progress: Optional[bool] = None
    #: Device count.
    #: example: 22
    device_count: Optional[int] = None
    #: Last updated time.
    #: example: 1659624763665
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
    #: example: 5675
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


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    #: example: 1
    port: Optional[int] = None
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
    line_weight: Optional[int] = None
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: The preconfigured number for Hotline. Required only if `hotlineEnabled` is set to true.
    #: example: +12055552222
    hotline_destination: Optional[str] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None


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
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Indicates if member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class DeviceType(str, Enum):
    #: Cisco Multiplatform Phone
    mpp = 'MPP'
    #: Analog Telephone Adapters
    ata = 'ATA'
    #: GENERIC Session Initiation Protocol
    generic_sip = 'GENERIC_SIP'
    #: Esim Supported Webex Go
    esim = 'ESIM'
    #: Cisco Webex Room OS and the Room Series device
    room_os = 'ROOM_OS'
    #: Mobile
    mobile = 'MOBILE'
    #: Desk Phone
    desk_phone = 'DESK_PHONE'


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
    #: Identifier for device model type.
    model_type: Optional[DeviceType] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ip_address: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Hoteling login settings, which are available when the device is the owner's primary device and device type is
    #: PRIMARY. Hoteling login settings are set at the owner level.
    hoteling: Optional[Hoteling] = None
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[StartJobResponseLatestExecutionExitCode] = None
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
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Indicates Hoteling details of a device.
    hoteling: Optional[Hoteling] = None
    #: Owner of the device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of a device.
    activation_state: Optional[DeviceActivationStates] = None


class PlaceDeviceList(ApiModel):
    #: Array of devices associated with a workspace.
    devices: Optional[list[PlaceDevices]] = None
    #: Maximum number of devices a workspace can be assigned to.
    max_device_count: Optional[int] = None


class LineKeyType(str, Enum):
    #: PRIMARY_LINE is the user's primary extension. This is the default assignment for Line Key Index 1 and cannot be
    #: modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables User and Call Park monitoring.
    monitor = 'MONITOR'
    #: Enables the configure layout feature in Control Hub to set call park extension implicitly.
    call_park_extension = 'CALL_PARK_EXTENSION'
    #: Allows users to reach a telephone number, extension or a SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key.
    #: These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'


class ProgrammableLineKeys(ApiModel):
    #: An index representing a Line Key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2
    line_key_index: Optional[int] = None
    #: The action that would be performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL` and the value must be a valid Telephone Number,
    #: Ext, or SIP URI (format: user@host using A-Z,a-z,0-9,-_ .+ for user and host).
    #: example: 5646
    line_key_value: Optional[str] = None


class GetLineKeyTemplateResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS81NzVhMWY3Zi03MjRkLTRmZGUtODk4NC1mNjNhNDljMzYxZmQ
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: Basic Template
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: 'DMS Cisco 6821'
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 6821
    model_display_name: Optional[str] = None
    #: Indicates whether user can reorder the line keys.
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None


class ApplyLineKeyTemplateJobDetails(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[StartJobResponseLatestExecutionExitCode] = None
    #: Indicates the progress of the job.
    percentage_complete: Optional[str] = None
    #: Number of job steps completed.
    updated_count: Optional[str] = None
    #: Number of job steps completed with advisories.
    advisory_count: Optional[str] = None


class ApplyLineKeyTemplateJobErrors(ApiModel):
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    #: Description of errors in the job.
    error: Optional[ErrorMessageObject] = None


class LineKeyTemplateAdvisoryTypes(ApiModel):
    #: Refine search to apply changes to devices that contain the warning "More shared/virtual line appearances than
    #: shared/virtual lines requested".
    #: example: True
    more_shared_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More shared/virtual lines requested than
    #: shared/virtual line appearances".
    #: example: True
    few_shared_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More monitored line appearances than
    #: monitored lines in the user's monitoring list".
    #: example: True
    more_monitor_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More call park extension line appearances
    #: than call park extensions in user's monitoring list".
    #: example: True
    more_cpeappearances_enabled: Optional[bool] = Field(alias='moreCPEAppearancesEnabled', default=None)


class PostApplyLineKeyTemplateRequestAction(str, Enum):
    #: Used to apply LinekeyTemplate to devices.
    apply_template = 'APPLY_TEMPLATE'
    #: Used to reset devices to its default Linekey Template configurations.
    apply_default_templates = 'APPLY_DEFAULT_TEMPLATES'


class LineKeyTemplatesResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL1VTL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS9kNDUzM2MwYi1hZGRmLTRjODUtODk0YS1hZTVkOTAyYzAyMDM=
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: template for 8845
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: DMS Cisco 8845
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 8845
    model_display_name: Optional[str] = None


class GetThirdPartyDeviceObjectOwner(ApiModel):
    #: SIP authentication user name for the owner of the device.
    #: example: 392829
    sip_user_name: Optional[str] = None
    #: Identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    #: example: lg1_sias10_cpapi16004_LGU@64941297.int10.bcld.webex.com
    line_port: Optional[str] = None


class GetThirdPartyDeviceObjectProxy(ApiModel):
    #: Outgoing server which the phone should use for all SIP requests. Not set if the response has no body.
    #: example: hs17.hosted-int.bcld.webex.com
    outbound_proxy: Optional[str] = None


class GetThirdPartyDeviceObject(ApiModel):
    #: Manufacturer of the device.
    #: example: THIRD_PARTY
    manufacturer: Optional[str] = None
    #: Device manager(s).
    #: example: CUSTOMER
    managed_by: Optional[str] = None
    #: A unique identifier for the device.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9ERVZJQ0UvNTEwMUIwN0ItNEY4Ri00RUY3LUI1NjUtREIxOUM3QjcyM0Y3
    id: Optional[str] = None
    #: The current IP address of the device.
    #: example: 100.110.120.130
    ip: Optional[str] = None
    #: The unique address for the network adapter.
    #: example: 11223344AAFF
    mac: Optional[str] = None
    #: A model type of the device.
    #: example: DMS Cisco 8811
    model: Optional[str] = None
    #: Activation state of the device. This field is only populated for a device added by a unique activation code
    #: generated by Control Hub for use with Webex.
    #: example: activated
    activation_state: Optional[ActivationStates] = None
    #: Comma-separated array of tags used to describe the device.
    #: example: ['device description']
    description: Optional[list[str]] = None
    #: Enabled / disabled status of the upgrade channel.
    #: example: True
    upgrade_channel_enabled: Optional[bool] = None
    owner: Optional[GetThirdPartyDeviceObjectOwner] = None
    proxy: Optional[GetThirdPartyDeviceObjectProxy] = None


class LayoutMode(str, Enum):
    #: Default layout mode when a new device is added.
    default = 'DEFAULT'
    #: Enables a device to have its custom layout.
    custom = 'CUSTOM'


class KEMKeys(ApiModel):
    #: An index representing a KEM Module. The Index starts from 1 representing the first KEM Module.
    #: example: 1
    kem_module_index: Optional[int] = None
    #: An index representing a KEM Key. The Index starts from 1 representing the first key on the left side of the
    #: phone.
    #: example: 1
    kem_key_index: Optional[int] = None
    #: The action that would be performed when the KEM Key is pressed.
    #: example: SPEED_DIAL
    kem_key_type: Optional[LineKeyType] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`.
    #: example: Office
    kem_key_label: Optional[str] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`. Value must be a valid Telephone Number, Ext, or SIP URI
    #: (format: `user@host` limited to `A-Z,a-z,0-9,-_ .+` for user and host).
    #: example: 213457
    kem_key_value: Optional[str] = None


class DeviceLayout(ApiModel):
    #: Defines the layout mode of the device, i.e. DEFAULT or CUSTOM.
    layout_mode: Optional[LayoutMode] = None
    #: If `true`, user customization is enabled.
    #: example: True
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None
    #: Type of KEM module.
    kem_module_type: Optional[KemModuleType] = None
    #: Contains a mapping of KEM Keys and their corresponding actions.
    kem_keys: Optional[list[KEMKeys]] = None


class LatestExecutionStatus(str, Enum):
    #: Indicates the job has started.
    starting = 'STARTING'
    #: Indicates the job is in progress.
    started = 'STARTED'
    #: Indicates the job has completed.
    completed = 'COMPLETED'
    #: Indicates the job has failed.
    failed = 'FAILED'


class RebuildPhonesJob(ApiModel):
    #: Name of the job which in this case, is `rebuildphones`.
    #: example: rebuildphones
    name: Optional[str] = None
    #: Unique identifier of the job.
    #: example: Y2lzY29zcGFyazovL3VzL0pPQl9JRC8wNjZkOTQzNC1kODEyLTQzODItODVhMC00MjBlOTFlODg3ZTY
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    #: example: ROUTERGW_1d458245-ee34-48c8-8ed6-92ea16ed48aa
    tracking_id: Optional[str] = None
    #: Unique identifier of the user who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MDRhZmQ1YS0zODRiLTQ0NjYtYTJlNC05Y2ExZjUwMDRlYWQ
    source_user_id: Optional[str] = None
    #: Unique identifier of the customer who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lYTRiZTEyNS00Y2ZjLTQ5OTItOGMwNi00Y2U4Mzc2ZDU4MmE
    source_customer_id: Optional[str] = None
    #: Unique identifier of the customer for which the job was run.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lYTRiZTEyNS00Y2ZjLTQ5OTItOGMwNi00Y2U4Mzc2ZDU4MmE
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    #: example: 428989
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status of the job at the time of invocation.
    #: example: STARTING
    latest_execution_status: Optional[LatestExecutionStatus] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[StartJobResponseLatestExecutionExitCode] = None
    #: Indicates the target entity, i.e. LOCATION.
    #: example: LOCATION
    target: Optional[str] = None
    #: Unique identifier of a location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzQ0Y2UwNDBhLTEzNmMtNDc3NS1hMjIzLTY5OTczYmEyYWNhYw
    location_id: Optional[str] = None
    #: Indicates the progress of the job.
    #: example: 10
    percentage_complete: Optional[str] = None
    #: Count of number of devices rebuilt.
    #: example: 10
    device_count: Optional[int] = None


class ListBackgroundImagesObject(ApiModel):
    #: The URL of the image file.
    #: example: "/dms/Cisco_Phone_Background/background001"
    background_image_url: Optional[str] = None
    #: The name of the image file.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None


class DeleteImageResponseSuccessObjectResult(ApiModel):
    #: The status of the deletion.
    #: example: 200
    status: Optional[int] = None


class DeleteImageResponseSuccessObject(ApiModel):
    #: The name of the image file.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None
    #: The result of the deletion.
    result: Optional[DeleteImageResponseSuccessObjectResult] = None


class DeleteImageRequestObject(ApiModel):
    #: The name of the image file to be deleted.
    #: example: CompanyLogoBlue
    file_name: Optional[str] = None
    #: Flag to force delete the image. When `forceDelete` = true, if any device, location, or org level custom
    #: background URL is configured with the `backgroundImageURL` containing the filename being deleted, the
    #: background image is set to `None`.
    #: example: True
    force_delete: Optional[bool] = None


class UserDeviceCount(ApiModel):
    #: The total count of devices associated with the user as a sum of:
    #: 
    #: - Count of total primary physical devices.
    #: 
    #: - Count of Webex-Team system device endpoints.
    #: 
    #: - Count of 1 for any or all applications present.
    #: example: 3
    total_device_count: Optional[int] = None
    #: The total count of applications associated with the user.
    #: example: 4
    applications_count: Optional[int] = None


class SearchMembersUsageType(str, Enum):
    device_owner = 'DEVICE_OWNER'
    shared_line = 'SHARED_LINE'


class ReadTheListOfBackgroundImagesResponse(ApiModel):
    #: Array of background images.
    background_images: Optional[list[ListBackgroundImagesObject]] = None
    #: The total number of images in the org.
    #: example: 2
    count: Optional[str] = None


class UploadADeviceBackgroundImageResponse(ApiModel):
    #: The name of the uploaded image file.
    #: example: CompanyLogoBlue
    filename: Optional[str] = None
    #: The URL of the uploaded image file.
    #: example: "/dms/Cisco_Phone_Background/background001"
    background_image_url: Optional[str] = None
    #: The total number of images in the org after uploading.
    #: example: 2
    count: Optional[str] = None


class DeleteDeviceBackgroundImagesResponse(ApiModel):
    #: Array of deleted images.
    items: Optional[list[DeleteImageResponseSuccessObject]] = None
    #: The total number of images in the org after deletion.
    #: example: 2
    count: Optional[str] = None


class DeviceCallSettingsApi(ApiChild, base='telephony/config'):
    """
    Device Call Settings
    
    These APIs manage Webex Calling settings for devices of the Webex Calling type.
    
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def get_device_members(self, device_id: str, org_id: str = None) -> GetMemberResponse:
        """
        Get Device Members

        Get the list of all the members of the device including primary and secondary users.

        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this organization.
        :type org_id: str
        :rtype: :class:`GetMemberResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/members')
        data = super().get(url, params=params)
        r = GetMemberResponse.model_validate(data)
        return r

    def update_members_on_the_device(self, device_id: str, members: list[PutMemberObject] = None, org_id: str = None):
        """
        Update Members on the device

        Modify member details on the device.

        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.

        Modifying members on the device requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param members: This specifies the new list of device members, completely replacing the existing device
            members. If the member's list is omitted then all the users are removed except the primary user.
        :type members: list[PutMemberObject]
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if members is not None:
            body['members'] = TypeAdapter(list[PutMemberObject]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/{device_id}/members')
        super().put(url, params=params, json=body)

    def search_members(self, device_id: str, location_id: str, member_name: str = None, phone_number: str = None,
                       extension: str = None, usage_type: SearchMembersUsageType = None, order: str = None,
                       org_id: str = None, **params) -> Generator[SearchMemberObject, None, None]:
        """
        Search Members

        Search members that can be assigned to the device.

        A device member can be either a person or a workspace. A admin can access the list of member details, modify
        member details and
        search for available members on a device.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param usage_type: Search for members eligible to become the owner of the device, or share line on the device.
        :type usage_type: SearchMembersUsageType
        :param order: Sort the list of available members on the device in ascending order by name, use either last name
            `lname` or first name `fname`. Default: last name in ascending order.
        :type order: str
        :param org_id: Retrieves the list of available members on the device in this organization.
        :type org_id: str
        :return: Generator yielding :class:`SearchMemberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        params['locationId'] = location_id
        if extension is not None:
            params['extension'] = extension
        if usage_type is not None:
            params['usageType'] = enum_str(usage_type)
        if order is not None:
            params['order'] = order
        url = self.ep(f'devices/{device_id}/availableMembers')
        return self.session.follow_pagination(url=url, model=SearchMemberObject, item_key='members', params=params)

    def apply_changes_for_a_specific_device(self, device_id: str, org_id: str = None):
        """
        Apply Changes for a specific device

        Issues request to the device to download and apply changes to the configuration.

        Applying changes for a specific device requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/actions/applyChanges/invoke')
        super().post(url, params=params)

    def get_device_settings(self, device_id: str, device_model: str,
                            org_id: str = None) -> DeviceSettingsObjectForDeviceLevel:
        """
        Get Device Settings

        Get override settings for a device.

        Device settings lists all the applicable settings for MPP, ATA and Wifi devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: The model type of the device. The corresponding device model display name sometimes called
            the product name, can also be used to specify the model.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str
        :rtype: :class:`DeviceSettingsObjectForDeviceLevel`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        params['deviceModel'] = device_model
        url = self.ep(f'devices/{device_id}/settings')
        data = super().get(url, params=params)
        r = DeviceSettingsObjectForDeviceLevel.model_validate(data)
        return r

    def update_device_settings(self, device_id: str, customizations: CustomizationDeviceLevelObjectDevice,
                               custom_enabled: bool, device_model: str = None, org_id: str = None):
        """
        Update device settings

        Modify override settings for a device.

        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins can
        also modify the settings. NOTE: DECT devices do not support settings at the device level.

        Updating settings on the device requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObjectDevice
        :param custom_enabled: Indicates if customization is allowed at a device level. If true, customized at a device
            level. If false, not customized; uses customer-level configuration.
        :type custom_enabled: bool
        :param device_model: The model type of the device. The corresponding device model display name sometimes called
            the product name, can also be used to specify the model.
        :type device_model: str
        :param org_id: Organization in which the device resides..
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        body = dict()
        body['customizations'] = customizations.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['customEnabled'] = custom_enabled
        url = self.ep(f'devices/{device_id}/settings')
        super().put(url, params=params, json=body)

    def get_location_device_settings(self, location_id: str, org_id: str = None) -> DeviceSettingsObject:
        """
        Get Location Device Settings

        Get device override settings for a location.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Organization in which the device resides.
        :type org_id: str
        :rtype: :class:`DeviceSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/devices/settings')
        data = super().get(url, params=params)
        r = DeviceSettingsObject.model_validate(data)
        return r

    def get_webex_calling_device_details(self, device_id: str, org_id: str = None) -> GetThirdPartyDeviceObject:
        """
        Get Webex Calling Device Details

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Retrieves Webex Calling device details that include information needed for third-party device management.

        Webex calling devices are associated with a specific user Workspace or Virtual Line. Webex Calling devices
        share the location with the entity that owns them.

        Person or workspace to which the device is assigned. Its fields point to a primary line/port of the device.

        Requires a full, location, user, or read-only admin auth token with the scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization in which the device resides.
        :type org_id: str
        :rtype: :class:`GetThirdPartyDeviceObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}')
        data = super().get(url, params=params)
        r = GetThirdPartyDeviceObject.model_validate(data)
        return r

    def update_third_party_device(self, device_id: str, sip_password: str, org_id: str = None):
        """
        Update Third Party Device

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Modify a device's `sipPassword`.

        Updating `sipPassword` on the device requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param sip_password: Password to be updated.
        :type sip_password: str
        :param org_id: ID of the organization in which the device resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['sipPassword'] = sip_password
        url = self.ep(f'devices/{device_id}')
        super().put(url, params=params, json=body)

    def get_person_devices(self, person_id: str, org_id: str = None) -> DeviceList:
        """
        Get Person Devices

        Get all devices for a person.

        This requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str
        :rtype: :class:`DeviceList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices')
        data = super().get(url, params=params)
        r = DeviceList.model_validate(data)
        return r

    def modify_hoteling_settings_for_a_person_s_primary_devices(self, person_id: str, hoteling: Hoteling,
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
        url = self.ep(f'people/{person_id}/devices/settings/hoteling')
        super().put(url, params=params, json=body)

    def get_workspace_devices(self, workspace_id: str, org_id: str = None) -> PlaceDeviceList:
        """
        Get Workspace Devices

        Get all devices for a workspace.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :rtype: :class:`PlaceDeviceList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices')
        data = super().get(url, params=params)
        r = PlaceDeviceList.model_validate(data)
        return r

    def modify_workspace_devices(self, workspace_id: str, enabled: bool, limit_guest_use: bool = None,
                                 guest_hours_limit: int = None, org_id: str = None):
        """
        Modify Workspace Devices

        Modify devices for a workspace.

        Modifying devices for a workspace requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param enabled: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can
            log into this host(workspace device) and use this device

        as if it were their own. This is useful when traveling to a remote office but still needing to place/receive
        calls with their telephone number and access features normally available to them on their office phone.
        :type enabled: bool
        :param limit_guest_use: Enable limiting the time a guest can use the device. The time limit is configured via
            `guestHoursLimit`.
        :type limit_guest_use: bool
        :param guest_hours_limit: Time Limit in hours until hoteling is enabled. Mandatory if `limitGuestUse` is
            enabled.
        :type guest_hours_limit: int
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if limit_guest_use is not None:
            body['limitGuestUse'] = limit_guest_use
        if guest_hours_limit is not None:
            body['guestHoursLimit'] = guest_hours_limit
        url = self.ep(f'workspaces/{workspace_id}/devices')
        super().put(url, params=params, json=body)

    def read_the_list_of_supported_devices(self, allow_configure_layout_enabled: bool = None, type: str = None,
                                           org_id: str = None) -> list[DeviceObject]:
        """
        Read the List of Supported Devices

        Gets the list of supported devices for an organization.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param allow_configure_layout_enabled: List supported devices that allow the user to configure the layout.
        :type allow_configure_layout_enabled: bool
        :param type: List supported devices of a specific type. To excluded device types from a request or query, add
            `type=not:DEVICE_TYPE`. For example, `type=not:MPP`.
        :type type: str
        :param org_id: List supported devices for an organization.
        :type org_id: str
        :rtype: list[DeviceObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if allow_configure_layout_enabled is not None:
            params['allowConfigureLayoutEnabled'] = str(allow_configure_layout_enabled).lower()
        if type is not None:
            params['type'] = type
        url = self.ep('supportedDevices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DeviceObject]).validate_python(data['devices'])
        return r

    def read_the_device_override_settings_for_a_organization(self, org_id: str = None) -> ListDeviceSettingsObject:
        """
        Read the device override settings for a organization

        Get device override settings for an organization.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: List supported devices for an organization.
        :type org_id: str
        :rtype: :class:`ListDeviceSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/settings')
        data = super().get(url, params=params)
        r = ListDeviceSettingsObject.model_validate(data)
        return r

    def create_a_line_key_template(self, template_name: str, device_model: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None) -> str:
        """
        Create a Line Key Template

        Create a Line Key Template in this organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows customers to create a Line Key Template for a device model.

        Creating a Line Key Template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_name: Name of the Line Key Template.
        :type template_name: str
        :param device_model: The model of the device for which the Line Key Template is applicable. The corresponding
            device model display name sometimes called the product name, can also be used to specify the model.
        :type device_model: str
        :param line_keys: Contains a mapping of Line Keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: User Customization Enabled.
        :type user_reorder_enabled: bool
        :param org_id: Organization to which line key template belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['templateName'] = template_name
        body['deviceModel'] = device_model
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/lineKeyTemplates')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def read_the_list_of_line_key_templates(self, org_id: str = None) -> list[LineKeyTemplatesResponse]:
        """
        Read the list of Line Key Templates

        List all Line Key Templates available for this organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve the list of Line Key Templates that are available for the organization.

        Retrieving this list requires a full, user or read-only administrator or location administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param org_id: List line key templates for this organization.
        :type org_id: str
        :rtype: list[LineKeyTemplatesResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/lineKeyTemplates')
        data = super().get(url, params=params)
        r = TypeAdapter(list[LineKeyTemplatesResponse]).validate_python(data['lineKeyTemplates'])
        return r

    def get_details_of_a_line_key_template(self, template_id: str, org_id: str = None) -> GetLineKeyTemplateResponse:
        """
        Get details of a Line Key Template

        Get detailed information about a Line Key Template by template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve a line key template by its ID in an organization.

        Retrieving a line key template requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param template_id: Get line key template for this template ID.
        :type template_id: str
        :param org_id: Retrieve a line key template for this organization.
        :type org_id: str
        :rtype: :class:`GetLineKeyTemplateResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        data = super().get(url, params=params)
        r = GetLineKeyTemplateResponse.model_validate(data)
        return r

    def modify_a_line_key_template(self, template_id: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None):
        """
        Modify a Line Key Template

        Modify a line key template by its template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to modify an existing Line Key Template by its ID in an organization.

        Modifying an existing line key template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_id: Modify line key template with this template ID.
        :type template_id: str
        :param line_keys: List of line keys that are being updated.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: Indicates whether the user can reorder the line keys.
        :type user_reorder_enabled: bool
        :param org_id: Modify a line key template for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        super().put(url, params=params, json=body)

    def delete_a_line_key_template(self, template_id: str, org_id: str = None):
        """
        Delete a Line Key Template

        Delete a Line Key Template by its template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to delete an existing Line Key Templates by its ID in an organization.

        Deleting an existing line key template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_id: Delete line key template with this template ID.
        :type template_id: str
        :param org_id: Delete a line key template for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        super().delete(url, params=params)

    def preview_apply_line_key_template(self, action: PostApplyLineKeyTemplateRequestAction, template_id: str,
                                        location_ids: list[str] = None,
                                        exclude_devices_with_custom_layout: bool = None,
                                        include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
                                        advisory_types: LineKeyTemplateAdvisoryTypes = None,
                                        org_id: str = None) -> int:
        """
        Preview Apply Line Key Template

        Preview the number of devices that will be affected by the application of a Line Key Template or when resetting
        devices to their factory Line Key settings.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to preview the number of devices that will be affected if a customer were to apply a Line
        Key Template or apply factory default Line Key settings to devices.

        Retrieving the number of devices affected requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param action: Line key Template action to perform.
        :type action: PostApplyLineKeyTemplateRequestAction
        :param template_id: `templateId` is required for `APPLY_TEMPLATE` action.
        :type template_id: str
        :param location_ids: Used to search for devices only in the given locations.
        :type location_ids: list[str]
        :param exclude_devices_with_custom_layout: Indicates whether to exclude devices with custom layout.
        :type exclude_devices_with_custom_layout: bool
        :param include_device_tags: Include devices only with these tags.
        :type include_device_tags: list[str]
        :param exclude_device_tags: Exclude devices with these tags.
        :type exclude_device_tags: list[str]
        :param advisory_types: Refine search with advisories.
        :type advisory_types: LineKeyTemplateAdvisoryTypes
        :param org_id: Preview Line Key Template for this organization.
        :type org_id: str
        :rtype: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
        body['templateId'] = template_id
        if location_ids is not None:
            body['locationIds'] = location_ids
        if exclude_devices_with_custom_layout is not None:
            body['excludeDevicesWithCustomLayout'] = exclude_devices_with_custom_layout
        if include_device_tags is not None:
            body['includeDeviceTags'] = include_device_tags
        if exclude_device_tags is not None:
            body['excludeDeviceTags'] = exclude_device_tags
        if advisory_types is not None:
            body['advisoryTypes'] = advisory_types.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/actions/previewApplyLineKeyTemplate/invoke')
        data = super().post(url, params=params, json=body)
        r = data['deviceCount']
        return r

    def apply_a_line_key_template(self, action: PostApplyLineKeyTemplateRequestAction, template_id: str,
                                  location_ids: list[str] = None, exclude_devices_with_custom_layout: bool = None,
                                  include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
                                  advisory_types: LineKeyTemplateAdvisoryTypes = None,
                                  org_id: str = None) -> ApplyLineKeyTemplateJobDetails:
        """
        Apply a Line key Template

        Apply a Line Key Template or reset devices to their factory Line Key settings.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to apply a line key template or apply factory default Line Key settings to devices in a
        set of locations or across all locations in the organization.

        Applying a Line Key Template or resetting devices to their default Line Key configuration requires a full
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param action: Line key Template action to perform.
        :type action: PostApplyLineKeyTemplateRequestAction
        :param template_id: `templateId` is required for `APPLY_TEMPLATE` action.
        :type template_id: str
        :param location_ids: Used to search for devices only in the given locations.
        :type location_ids: list[str]
        :param exclude_devices_with_custom_layout: Indicates whether to exclude devices with custom layout.
        :type exclude_devices_with_custom_layout: bool
        :param include_device_tags: Include devices only with these tags.
        :type include_device_tags: list[str]
        :param exclude_device_tags: Exclude devices with these tags.
        :type exclude_device_tags: list[str]
        :param advisory_types: Refine search with advisories.
        :type advisory_types: LineKeyTemplateAdvisoryTypes
        :param org_id: Apply Line Key Template for this organization.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
        body['templateId'] = template_id
        if location_ids is not None:
            body['locationIds'] = location_ids
        if exclude_devices_with_custom_layout is not None:
            body['excludeDevicesWithCustomLayout'] = exclude_devices_with_custom_layout
        if include_device_tags is not None:
            body['includeDeviceTags'] = include_device_tags
        if exclude_device_tags is not None:
            body['excludeDeviceTags'] = exclude_device_tags
        if advisory_types is not None:
            body['advisoryTypes'] = advisory_types.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('jobs/devices/applyLineKeyTemplate')
        data = super().post(url, params=params, json=body)
        r = ApplyLineKeyTemplateJobDetails.model_validate(data)
        return r

    def get_list_of_apply_line_key_template_jobs(self, org_id: str = None) -> list[ApplyLineKeyTemplateJobDetails]:
        """
        Get List of Apply Line Key Template jobs

        Get the list of all apply line key templates jobs in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve all the apply line key templates jobs in an organization.

        Retrieving the list of apply line key templates jobs in an organization requires a full, user or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of line key templates jobs in this organization.
        :type org_id: str
        :rtype: list[ApplyLineKeyTemplateJobDetails]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/applyLineKeyTemplate')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ApplyLineKeyTemplateJobDetails]).validate_python(data['items'])
        return r

    def get_the_job_status_of_an_apply_line_key_template_job(self, job_id: str,
                                                             org_id: str = None) -> ApplyLineKeyTemplateJobDetails:
        """
        Get the job status of an Apply Line Key Template job

        Get the status of an apply line key template job by its job ID.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to check the status of an apply line key templates job by job ID in an organization.

        Checking the the status of an apply line key templates job in an organization requires a full, user or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check a line key template job status in this organization.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/applyLineKeyTemplate/{job_id}')
        data = super().get(url, params=params)
        r = ApplyLineKeyTemplateJobDetails.model_validate(data)
        return r

    def get_job_errors_for_an_apply_line_key_template_job(self, job_id: str,
                                                          org_id: str = None) -> ApplyLineKeyTemplateJobErrors:
        """
        Get job errors for an Apply Line Key Template job

        GET job errors for an apply Line Key Template job in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve all the errors of an apply line key templates job by job ID in an
        organization.

        Retrieving all the errors of an apply line key templates job in an organization requires a full, user or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for an apply line key template job in this organization.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobErrors`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/applyLineKeyTemplate/{job_id}/errors')
        data = super().get(url, params=params)
        r = ApplyLineKeyTemplateJobErrors.model_validate(data)
        return r

    def read_the_dect_device_type_list___deprecated(self, org_id: str = None) -> list[DectDeviceList]:
        """
        Read the DECT device type list - Deprecated

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP).</Callout></div>

        <div><Callout type="warning">The REST path for this API has changed to [GET
        /telephony/config/devices/dectNetworks/supportedDevices{?orgId}]. The use of this old REST path is deprecated
        and will be decommissioned on October 10, 2024. Please start using it for all future projects.</Callout></div>

        Get DECT device type list with base stations and line ports supported count. This is a static list.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :type org_id: str
        :rtype: list[DectDeviceList]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/dects/supportedDevices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DectDeviceList]).validate_python(data['devices'])
        return r

    def read_the_dect_device_type_list(self, org_id: str = None) -> list[DectDeviceList]:
        """
        Read the DECT device type list

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP).</Callout></div>

        Get DECT device type list with base stations and line ports supported count. This is a static list.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :type org_id: str
        :rtype: list[DectDeviceList]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/dectNetworks/supportedDevices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DectDeviceList]).validate_python(data['devices'])
        return r

    def validate_a_list_of_mac_address(self, macs: list[str], org_id: str = None) -> MACAddressResponse:
        """
        Validate a list of MAC address

        Validate a list of MAC addresses.

        Validating this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param macs: MAC addresses to be validated.
        :type macs: list[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str
        :rtype: :class:`MACAddressResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['macs'] = macs
        url = self.ep('devices/actions/validateMacs/invoke')
        data = super().post(url, params=params, json=body)
        r = MACAddressResponse.model_validate(data)
        return r

    def change_device_settings_across_organization_or_location_job(self, location_id: str = None,
                                                                   location_customizations_enabled: bool = None,
                                                                   customizations: CustomizationObject = None,
                                                                   org_id: str = None) -> StartJobResponse:
        """
        Change Device Settings Across Organization Or Location Job

        Change device settings across organization or locations jobs.

        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system
        admins in a stateful persistent manner. This job will modify the requested device settings across all
        non-customized devices. Whenever a location ID is specified in the request, it will modify the requested
        device settings only for non-customized devices that are part of the provided location within an organization.

        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.

        Only one job per customer can be running at any given time within the same organization. An attempt to run
        multiple jobs at the same time will result in a 409 error response.

        Running a job requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location within an organization where changes of device setings will be applied to all the
            devices within it.
        :type location_id: str
        :param location_customizations_enabled: Indicates if all the devices within this location will be customized
            with new requested customizations(if set to `true`) or will be overridden with the one at organization
            level (if set to `false` or any other value). This field has no effect when the job is being triggered at
            organization level.
        :type location_customizations_enabled: bool
        :param customizations: Indicates the settings for ATA devices, DECT devices and MPP devices.
        :type customizations: CustomizationObject
        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :rtype: :class:`StartJobResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if location_id is not None:
            body['locationId'] = location_id
        if location_customizations_enabled is not None:
            body['locationCustomizationsEnabled'] = location_customizations_enabled
        if customizations is not None:
            body['customizations'] = customizations.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('jobs/devices/callDeviceSettings')
        data = super().post(url, params=params, json=body)
        r = StartJobResponse.model_validate(data)
        return r

    def list_change_device_settings_jobs(self, org_id: str = None,
                                         **params) -> Generator[StartJobResponse, None, None]:
        """
        List change device settings jobs.

        Lists all the jobs for jobType `calldevicesettings` for the given organization in order of most recent one to
        oldest one irrespective of its status.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`StartJobResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/callDeviceSettings')
        return self.session.follow_pagination(url=url, model=StartJobResponse, item_key='items', params=params)

    def get_change_device_settings_job_status(self, job_id: str) -> JobIdResponseObject:
        """
        Get change device settings job status.

        Provides details of the job with `jobId` of `jobType` `calldevicesettings`.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :rtype: :class:`JobIdResponseObject`
        """
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}')
        data = super().get(url)
        r = JobIdResponseObject.model_validate(data)
        return r

    def list_change_device_settings_job_errors(self, job_id: str, org_id: str = None,
                                               **params) -> Generator[ItemObject, None, None]:
        """
        List change device settings job errors.

        Lists all error details of the job with `jobId` of `jobType` `calldevicesettings`.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def get_device_layout_by_device_id(self, device_id: str, org_id: str = None) -> DeviceLayout:
        """
        Get Device Layout by Device ID

        Get layout information of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Get device layout for this device ID.
        :type device_id: str
        :param org_id: Retrieve a device layout for the device in this organization.
        :type org_id: str
        :rtype: :class:`DeviceLayout`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/layout')
        data = super().get(url, params=params)
        r = DeviceLayout.model_validate(data)
        return r

    def modify_device_layout_by_device_id(self, device_id: str, layout_mode: LayoutMode,
                                          line_keys: list[ProgrammableLineKeys], user_reorder_enabled: bool = None,
                                          kem_module_type: KemModuleType = None, kem_keys: list[KEMKeys] = None,
                                          org_id: str = None):
        """
        Modify Device Layout by Device ID

        Modify the layout of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Modify device layout for this device ID.
        :type device_id: str
        :param layout_mode: Defines the layout mode of the device, i.e. DEFAULT or CUSTOM.
        :type layout_mode: LayoutMode
        :param line_keys: Contains a mapping of Line Keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: If `true`, user customization is enabled.
        :type user_reorder_enabled: bool
        :param kem_module_type: Type of KEM module.
        :type kem_module_type: KemModuleType
        :param kem_keys: Contains a mapping of KEM Keys and their corresponding actions.
        :type kem_keys: list[KEMKeys]
        :param org_id: Modify a device layout for the device in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['layoutMode'] = enum_str(layout_mode)
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        if kem_module_type is not None:
            body['kemModuleType'] = enum_str(kem_module_type)
        if kem_keys is not None:
            body['kemKeys'] = TypeAdapter(list[KEMKeys]).dump_python(kem_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/{device_id}/layout')
        super().put(url, params=params, json=body)

    def rebuild_phones_configuration(self, location_id: str, org_id: str = None) -> RebuildPhonesJob:
        """
        Rebuild Phones Configuration

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>.

        Rebuild all phone configurations for the specified location.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Unique identifier of the location.
        :type location_id: str
        :param org_id: Rebuild phones for this organization.
        :type org_id: str
        :rtype: :class:`RebuildPhonesJob`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['locationId'] = location_id
        url = self.ep('jobs/devices/rebuildPhones')
        data = super().post(url, params=params, json=body)
        r = RebuildPhonesJob.model_validate(data)
        return r

    def list_rebuild_phones_jobs(self, org_id: str = None) -> list[RebuildPhonesJob]:
        """
        List Rebuild Phones Jobs

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>.

        Get the list of all Rebuild Phones jobs in an organization.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: List of rebuild phones jobs in this organization.
        :type org_id: str
        :rtype: list[RebuildPhonesJob]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/rebuildPhones')
        data = super().get(url, params=params)
        r = TypeAdapter(list[RebuildPhonesJob]).validate_python(data['items'])
        return r

    def get_the_job_status_of_a_rebuild_phones_job(self, job_id: str, org_id: str = None) -> RebuildPhonesJob:
        """
        Get the Job Status of a Rebuild Phones Job

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>.

        Get the details of a rebuild phones job by its job ID.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check a rebuild phones job status in this organization.
        :type org_id: str
        :rtype: :class:`RebuildPhonesJob`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/rebuildPhones/{job_id}')
        data = super().get(url, params=params)
        r = RebuildPhonesJob.model_validate(data)
        return r

    def get_job_errors_for_a_rebuild_phones_job(self, job_id: str, org_id: str = None) -> list[ItemObject]:
        """
        Get Job Errors for a Rebuild Phones Job

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>.

        Get errors for a rebuild phones job in an organization.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for a rebuild phones job in this organization.
        :type org_id: str
        :rtype: list[ItemObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/rebuildPhones/{job_id}/errors')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ItemObject]).validate_python(data['items'])
        return r

    def get_device_settings_for_a_person(self, person_id: str, org_id: str = None) -> Compression:
        """
        Get Device Settings for a Person

        Device settings list the compression settings for a person.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: ID of the person for whom to retrieve device settings.
        :type person_id: str
        :param org_id: Retrieves the device settings for a person in this organization.
        :type org_id: str
        :rtype: Compression
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices/settings')
        data = super().get(url, params=params)
        r = Compression.model_validate(data['compression'])
        return r

    def update_device_settings_for_a_person(self, person_id: str, compression: Compression, org_id: str = None):
        """
        Update Device Settings for a Person

        Update device settings modifies the compression settings for a person.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: ID of the person for whom to update device settings.
        :type person_id: str
        :param compression: Toggles compression ON and OFF.
        :type compression: Compression
        :param org_id: Modify device settings for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['compression'] = enum_str(compression)
        url = self.ep(f'people/{person_id}/devices/settings')
        super().put(url, params=params, json=body)

    def get_device_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> Compression:
        """
        Get Device Settings for a Workspace

        Device settings list the compression settings for a workspace.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: ID of the workspace for which to retrieve device settings.
        :type workspace_id: str
        :param org_id: Retrieves the device settings for a workspace in this organization.
        :type org_id: str
        :rtype: Compression
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices/settings')
        data = super().get(url, params=params)
        r = Compression.model_validate(data['compression'])
        return r

    def update_device_settings_for_a_workspace(self, workspace_id: str, compression: Compression, org_id: str = None):
        """
        Update Device Settings for a Workspace

        Update device settings modifies the compression settings for a workspace.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: ID of the workspace for which to update device settings.
        :type workspace_id: str
        :param compression: Toggles compression ON and OFF.
        :type compression: Compression
        :param org_id: Modify the device settings for a workspace in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['compression'] = enum_str(compression)
        url = self.ep(f'workspaces/{workspace_id}/devices/settings')
        super().put(url, params=params, json=body)

    def read_the_list_of_background_images(self, org_id: str = None) -> ReadTheListOfBackgroundImagesResponse:
        """
        Read the List of Background Images

        Gets the list of device background images for an organization.

        Webex Calling supports the upload of up to 100 background image files for each org. These image files can then
        be referenced by MPP phones in that org for use as their background image.

        Retrieving this list requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieves the list of images in this organization.
        :type org_id: str
        :rtype: :class:`ReadTheListOfBackgroundImagesResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/backgroundImages')
        data = super().get(url, params=params)
        r = ReadTheListOfBackgroundImagesResponse.model_validate(data)
        return r

    def upload_a_device_background_image(self, device_id: str,
                                         org_id: str = None) -> UploadADeviceBackgroundImageResponse:
        """
        Upload a Device Background Image

        Configure a device's background image by uploading an image with file format, `.jpeg` or `.png`, encoded image
        file. Maximum image file size allowed to upload is 625 KB.

        The request must be a multipart/form-data request rather than JSON, using the image/jpeg or image/png
        content-type.

        Webex Calling supports the upload of up to 100 background image files for each org. These image files can then
        be referenced by MPP phones in that org for use as their background image.

        Uploading a device background image requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Uploads the image in this organization.
        :type org_id: str
        :rtype: :class:`UploadADeviceBackgroundImageResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/actions/backgroundImageUpload/invoke')
        data = super().post(url, params=params)
        r = UploadADeviceBackgroundImageResponse.model_validate(data)
        return r

    def delete_device_background_images(self, background_images: list[DeleteImageRequestObject],
                                        org_id: str = None) -> DeleteDeviceBackgroundImagesResponse:
        """
        Delete Device Background Images

        Delete the list of designated device background images for an organization. Maximum is 10 images per request.

        Deleting a device background image requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param background_images: Array of images to be deleted.
        :type background_images: list[DeleteImageRequestObject]
        :param org_id: Deletes the list of images in this organization.
        :type org_id: str
        :rtype: :class:`DeleteDeviceBackgroundImagesResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['backgroundImages'] = TypeAdapter(list[DeleteImageRequestObject]).dump_python(background_images, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/backgroundImages')
        data = super().delete(url, params=params, json=body)
        r = DeleteDeviceBackgroundImagesResponse.model_validate(data)
        return r

    def get_user_devices_count(self, person_id: str, org_id: str = None) -> UserDeviceCount:
        """
        Get User Devices Count

        Get the total device and application count for a person.

        The device count can be used to determine if more devices can be added for users with a device count limit. For
        example, users with standard calling licenses can only have one physical device.

        This requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Person for whom to retrieve the device count.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str
        :rtype: :class:`UserDeviceCount`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices/count')
        data = super().get(url, params=params)
        r = UserDeviceCount.model_validate(data)
        return r
