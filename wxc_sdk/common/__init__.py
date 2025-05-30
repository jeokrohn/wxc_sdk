"""
Common date types and APIs
"""
from datetime import datetime
from typing import Optional, Any, Union

from pydantic import Field, field_validator, model_validator

from ..base import ApiModel, webex_id_to_uuid
from ..base import SafeEnum as Enum

__all__ = ['UserType', 'UserBase', 'RingPattern', 'AlternateNumber', 'Greeting', 'UserNumber', 'PersonPlaceAgent',
           'MonitoredMember', 'CallParkExtension', 'AuthCodeLevel', 'AuthCode', 'RouteType', 'DialPatternValidate',
           'DialPatternStatus',
           'RouteIdentity', 'Customer', 'IdOnly', 'IdAndName', 'PatternAction', 'NumberState', 'ValidationStatus',
           'ValidateExtensionStatusState', 'ValidateExtensionStatus', 'ValidateExtensionsResponse',
           'ValidatePhoneNumberStatusState', 'ValidatePhoneNumberStatus', 'ValidatePhoneNumbersResponse', 'StorageType',
           'VoicemailMessageStorage', 'VoicemailEnabled', 'VoicemailNotifications', 'VoicemailFax',
           'VoicemailTransferToNumber', 'VoicemailCopyOfMessage', 'AudioCodecPriority', 'AtaDtmfMode', 'AtaDtmfMethod',
           'VlanSetting', 'AtaCustomization', 'DeviceCustomizations', 'DeviceCustomization',
           'CommonDeviceCustomization', 'BacklightTimer', 'Background', 'BackgroundSelection', 'DisplayNameSelection',
           'LoggingLevel', 'DisplayCallqueueAgentSoftkey', 'AcdCustomization', 'LineKeyLabelSelection',
           'LineKeyLedPattern', 'PhoneLanguage', 'EnabledAndValue', 'WifiNetwork', 'MppCustomization',
           'PrimaryOrShared',
           'MediaFileType', 'AnnAudioFile', 'WifiCustomization', 'RoomType', 'LinkRelation', 'AnnouncementLevel',
           'UsbPortsObject', 'WifiAuthenticationMethod', 'DirectoryMethod', 'CallHistoryMethod', 'MppVlanDevice',
           'VolumeSettings', 'CallForwardExpandedSoftKey', 'HttpProxy', 'HttpProxyMode', 'BluetoothMode',
           'BluetoothSetting', 'NoiseCancellation', 'SoftKeyLayout', 'SoftKeyMenu', 'PskObject', 'BackgroundImageColor',
           'BacklightTimer68XX78XX', 'DectCustomization', 'OwnerType', 'NumberOwner', 'ApplyLineKeyTemplateAction',
           'AssignedDectNetwork', 'DevicePlatform', 'Multicast', 'EnhancedMulticast', 'DeviceType', 'UserLicenseType']


class IdOnly(ApiModel):
    id: str


class IdAndName(IdOnly):
    name: Optional[str] = None


class LinkRelation(ApiModel):
    #: Link relation describing how the target resource is related to the current context (conforming with RFC5998).
    rel: Optional[str] = None
    #: Target resource URI (conforming with RFC5998).
    href: Optional[str] = None
    #: Target resource method (conforming with RFC5998).
    method: Optional[str] = None


class RoomType(str, Enum):
    #: 1:1 room.
    direct = 'direct'
    #: Group room.
    group = 'group'


class UserType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    virtual_line = 'VIRTUAL_LINE'


class UserLicenseType(str, Enum):
    #: Member is a Webex Calling standard user
    basic_user = 'BASIC_USER'
    #: Member is a Webex Calling professional user
    professional_user = 'PROFESSIONAL_USER'
    #: Member is a Webex Calling Common area workspace
    workspace = 'WORKSPACE'
    #: Member is a Webex Calling professional workspace
    professional_workspace = 'PROFESSIONAL_WORKSPACE'
    #: Member is a Webex Calling virtual line
    virtual_profile = 'VIRTUAL_PROFILE'


class UserBase(ApiModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[UserType] = Field(alias='type', default=None)


class RingPattern(str, Enum):
    """
    Ring Pattern
    """
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumber(ApiModel):
    """
    Hunt group or call queue alternate number
    """
    #: Alternate phone number for the hunt group or call queue
    phone_number: Optional[str] = None
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPattern] = None
    #: Flag: phone_number is a toll free number
    toll_free_number: Optional[bool] = None


class Greeting(str, Enum):
    """
    DEFAULT indicates that a system default message will be placed when incoming calls are intercepted.
    """
    #: A custom will be placed when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default message will be placed when incoming calls are intercepted.
    default = 'DEFAULT'


class UserNumber(ApiModel):
    """
    phone number of the person or workspace.
    """
    #: Phone number of person or workspace. Either phoneNumber or extension is mandatory
    external: Optional[str] = None
    #: Extension of person or workspace. Either phoneNumber or extension is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routingPrefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Flag to indicate primary phone.
    primary: Optional[bool] = None


class PersonPlaceAgent(UserBase):
    """
    Agent (person or place)
    """
    #: ID of person or workspace.
    agent_id: str = Field(alias='id')
    #: Display name of person or workspace.
    display_name: Optional[str] = None
    #: Email of the person or workspace.
    email: Optional[str] = None
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumber]] = None
    location: Optional[IdAndName] = None


class MonitoredMember(ApiModel):
    """
    a monitored user or place
    """
    #: The identifier of the monitored person.
    member_id: Optional[str] = Field(alias='id', default=None)
    #: The last name of the monitored person or place.
    last_name: Optional[str] = None
    #: The first name of the monitored person or place.
    first_name: Optional[str] = None
    #: The display name of the monitored person or place.
    display_name: Optional[str] = None
    #: Indicates whether type is PEOPLE or PLACE.
    member_type: Optional[UserType] = Field(alias='type', default=None)
    #: The email address of the monitored person or place.
    email: Optional[str] = None
    #: The list of phone numbers of the monitored person or place.
    numbers: Optional[list[UserNumber]] = None
    # location can be either a location name or an id and name instance
    location: Optional[Union[str, IdAndName]] = None

    @property
    def ci_member_id(self) -> Optional[str]:
        return self.member_id and webex_id_to_uuid(self.member_id)

    @property
    def location_name(self) -> str:
        """
        Apparently location attribute is either the location name or an IdAndName instance
        """
        return isinstance(self.location, IdAndName) and self.location.name or self.location


class CallParkExtension(ApiModel):
    #: The identifier of the call park extension.
    cpe_id: Optional[str] = Field(alias='id', default=None)
    #: The name to describe the call park extension.
    name: Optional[str] = None
    #: The extension number for this call park extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routingPrefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: The location name where the call park extension is.
    location_name: Optional[str] = None
    #: The location ID for the location.
    location_id: Optional[str] = None

    @model_validator(mode='before')
    def fix_location_name(cls, values):
        """
        The schema changed at some point: endpoint returns "location" instead of "location_name". For backwards
        compatibility we need to rename it to "location_name" if it is present.

        :meta private:
        :param values:
        :return:
        """
        location = values.pop('location', None)
        if location is not None:
            values['location_name'] = location
        return values

    @property
    def ci_cpe_id(self) -> Optional[str]:
        """
        call park extension ID as UUID
        """
        return self.cpe_id and webex_id_to_uuid(self.cpe_id)


class AuthCodeLevel(str, Enum):
    #: Indicates the location level access code.
    location = 'LOCATION'
    #: Indicates the workspace level access code.
    custom = 'CUSTOM'


class AuthCode(ApiModel):
    """
    authorization code and description.
    """
    #: Indicates an authorization code.
    code: str
    #: Indicates the description of the authorization code.
    description: str
    #: Indicates the level of each access code.
    level: Optional[AuthCodeLevel] = None

    def create(self) -> dict:
        """
        dict for auth code creation

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True, exclude={'level'})


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    # Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class DialPatternStatus(str, Enum):
    """
    validation status.
    """
    #: invalid pattern
    invalid = 'INVALID'
    #: duplicate pattern
    duplicate = 'DUPLICATE'
    #: duplicate in input
    duplicate_in_list = 'DUPLICATE_IN_LIST'


class DialPatternValidate(ApiModel):
    #: input dial pattern that is being validate
    dial_pattern: str
    #: validation status.
    pattern_status: DialPatternStatus
    #: failure details.
    message: str


class RouteIdentity(ApiModel):
    route_id: str = Field(alias='id')
    name: Optional[str] = None
    route_type: RouteType = Field(alias='type')


class Customer(ApiModel):
    """
    Customer information.
    """
    #: ID of the customer/organization.
    customer_id: str = Field(alias='id')
    #: Name of the customer/organization.
    name: str


class PatternAction(str, Enum):
    #: add action, when adding a new dial pattern
    add = 'ADD'
    #: delete action, when deleting an existing dial pattern
    delete = 'DELETE'


class NumberState(str, Enum):
    #: The number is activated and has calling capability.
    active = 'ACTIVE'
    #: A number is not yet activated and has no calling capability.
    inactive = 'INACTIVE'


class ValidationStatus(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class ValidateExtensionStatusState(str, Enum):
    valid = 'VALID'
    duplicate = 'DUPLICATE'
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    invalid = 'INVALID'


class ValidateExtensionStatus(ApiModel):
    #: Indicates the extension id for which the status is about .
    extension: str
    #: Indicate the status for the given extension id .
    state: ValidateExtensionStatusState
    #: Error Code .
    error_code: Optional[int] = None
    message: Optional[str] = None

    @property
    def ok(self):
        return self.state == ValidateExtensionStatusState.valid


class ValidateExtensionsResponse(ApiModel):
    status: ValidationStatus
    extension_status: Optional[list[ValidateExtensionStatus]] = None

    @property
    def ok(self) -> bool:
        return self.status == ValidationStatus.ok


class ValidatePhoneNumberStatusState(str, Enum):
    #: The phone number is available.
    available = 'Available'
    #: Duplicate phone number.
    duplicate = 'Duplicate'
    #: Duplicate phone number in the list.
    duplicate_in_list = 'Duplicate In List'
    #: The phone number is invalid.
    invalid = 'Invalid'
    #: The phone number is unavailable and cannot be used.
    unavailable = 'Unavailable'


class ValidatePhoneNumberStatus(ApiModel):
    #: Phone number that need to be validated.
    phone_number: str
    #: The state of the number.
    state: ValidatePhoneNumberStatusState
    #: If `true`, it's a toll-free number.
    toll_free_number: bool
    #: Error details if the number is unavailable.
    detail: list[str] = Field(default_factory=list)

    @property
    def ok(self):
        return self.state == ValidatePhoneNumberStatusState.available


class ValidatePhoneNumbersResponse(ApiModel):
    #: This indicates the status of the numbers.
    status: ValidationStatus
    #: This is an array of number objects with number details.
    phone_numbers: Optional[list[ValidatePhoneNumberStatus]] = None

    @property
    def ok(self) -> bool:
        return self.status == ValidationStatus.ok


class StorageType(str, Enum):
    """
    Designates which type of voicemail message storage is used.
    """
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class VoicemailMessageStorage(ApiModel):
    """
    Settings for message storage
    """
    #: When true desktop phone will indicate there are new voicemails.
    mwi_enabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    storage_type: Optional[StorageType] = None
    #: External email address to which the new voicemail audio will be sent. A value for this field must be provided
    # in the request if a storageType of EXTERNAL is given in the request.
    external_email: Optional[str] = None


class VoicemailEnabled(ApiModel):
    enabled: bool


class VoicemailNotifications(VoicemailEnabled):
    """
    Settings for notifications when there are any new voicemails.
    """
    #: Email address to which the notification will be sent. For text messages, use an email to text message gateway
    #: like 2025551212@txt.att.net.
    destination: Optional[str] = None


class VoicemailFax(VoicemailEnabled):
    """
    Fax message settings
    """
    #: Designates optional extension for fax.
    extension: Optional[str] = None
    #: Designates phone number for fax. A value for this field must be provided in the request if faxMessage enabled
    #: field is given as true in the request.
    phone_number: Optional[str] = None


class VoicemailTransferToNumber(VoicemailEnabled):
    """
    Settings for voicemail caller to transfer to a different number by pressing zero (0).
    """
    #: Number voicemail caller will be transferred to when they press zero (0).
    destination: Optional[str] = None


class VoicemailCopyOfMessage(VoicemailEnabled):
    """
    Settings for sending a copy of new voicemail message audio via email.
    """
    #: Email address to which the new voicemail audio will be sent.
    email_id: Optional[str] = None


class DeviceType(str, Enum):
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


class AudioCodecPriority(ApiModel):
    """
    Choose up to three predefined codec priority options available for your region.
    """
    #: Indicates the selection of an Audio Code Priority Object.
    selection: str
    #: Indicates the primary Audio Codec.
    primary: Optional[str] = None
    #: Indicates the secondary Audio Codec.
    secondary: Optional[str] = None
    #: Indicates the tertiary Audio Codec.
    tertiary: Optional[str] = None


class AtaDtmfMode(str, Enum):
    """
    DTMF Detection Tx Mode selection for Cisco ATA devices.
    """
    #: It means a) DTMF digit requires an extra hold time after detection and b) DTMF level threshold is raised to
    #: -20 dBm.
    strict = 'STRICT'
    #: It means normal threshold mode.
    normal = 'NORMAL'


class AtaDtmfMethod(str, Enum):
    """
    Method for transmitting DTMF signals to the far end.
    """
    #: Sends DTMF by using the audio path.
    inband = 'INBAND'
    #: Audio video transport. Sends DTMF as AVT events.
    avt = 'AVT'
    auto = 'AUTO'


class VlanSetting(ApiModel):
    #: Denotes whether the VLAN object is enabled
    enabled: bool
    #: The value of the VLAN Object
    value: int
    #: Indicates the PC port value of a VLAN object for an MPP object
    pc_port: Optional[int] = None


class CommonDeviceCustomization(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: AudioCodecPriority
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: bool
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: bool
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: bool
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: VlanSetting
    #: Enable/disable automatic nightly configuration resync of the device.
    nightly_resync_enabled: Optional[bool] = None


class AtaCustomization(CommonDeviceCustomization):
    """
    settings that are applicable to ATA devices.
    """
    #: DTMF Detection Tx Mode selection for Cisco ATA devices.
    ata_dtmf_mode: AtaDtmfMode
    #: Method for transmitting DTMF signals to the far end.
    ata_dtmf_method: AtaDtmfMethod
    snmp: dict
    #: Enable/disable user level web access to the local device.
    web_access_enabled: bool


class DectCustomization(CommonDeviceCustomization):
    #: Enable/disable user level web access to the local device.
    web_access_enabled: bool


class BacklightTimer(str, Enum):
    one_min = 'ONE_MIN'
    five_min = 'FIVE_MIN'
    thirty_min = 'THIRTY_MIN'
    always_on = 'ALWAYS_ON'


class BacklightTimer68XX78XX(str, Enum):
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


class Background(str, Enum):
    #: Indicates that there will be no background image set for the devices.
    no_background = 'NONE'
    #: Indicates that dark blue background image will be set for the devices.
    dark_blue = 'DARK_BLUE'
    #: Indicates that Cisco themed dark blue background image will be set for the devices.
    cisco_dark_blue = 'CISCO_DARK_BLUE'
    #: Indicates that Cisco webex dark blue background image will be set for the devices.
    webex_dark_blue = 'WEBEX_DARK_BLUE'
    #: Indicates that a custom background image will be set for the devices.
    custom_background = 'CUSTOM_BACKGROUND'


class BackgroundSelection(ApiModel):
    """
    Background selection for MPP devices
    """
    image: Background
    custom_url: Optional[str] = None


class DisplayNameSelection(str, Enum):
    #: Indicates that devices will display the person’s phone number, or if a person doesn’t have a phone number, the
    #: location number will be displayed.
    person_number = 'PERSON_NUMBER'
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name = 'PERSON_FIRST_THEN_LAST_NAME'
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name = 'PERSON_LAST_THEN_FIRST_NAME'


class LoggingLevel(str, Enum):
    #: Enables standard logging.
    standard = 'STANDARD'
    #: Enables detailed debugging logging.
    debugging = 'DEBUGGING'


class DisplayCallqueueAgentSoftkey(str, Enum):
    """
    Chooses the location of the Call Queue Agent Login/Logout softkey on Multi-Platform Phones.
    """
    front_page = 'FRONT_PAGE'
    last_page = 'LAST_PAGE'


class AcdCustomization(ApiModel):
    #: Indicates whether the ACD object is enabled.
    enabled: bool
    #: Indicates the call queue agent soft key value of an ACD object.
    display_callqueue_agent_softkeys: str


class LineKeyLabelSelection(str, Enum):
    """
    Line key labels define the format of what’s shown next to line keys.
    """
    #: This will display the person extension, or if a person doesn’t have an extension, the person’s first name will
    #: be displayed.
    person_extension = 'PERSON_EXTENSION'
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name = 'PERSON_FIRST_THEN_LAST_NAME'
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name = 'PERSON_LAST_THEN_FIRST_NAME'


class LineKeyLedPattern(str, Enum):
    default = 'DEFAULT'
    preset_1 = 'PRESET_1'


class PhoneLanguage(str, Enum):
    #: Indicates a person's announcement language.
    person = 'PERSON_LANGUAGE'
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


class EnabledAndValue(ApiModel):
    enabled: bool
    value: int


class WifiNetwork(ApiModel):
    """
    Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    """
    #: Indicates whether the wifi network is enabled.
    enabled: bool
    #: Authentication method of wifi network.
    authentication_method: str
    #: SSID name of the wifi network.
    ssid_name: Optional[str] = None
    #: User ID of the wifi network.
    user_id: Optional[str] = None


class UsbPortsObject(ApiModel):
    #: New Control to Enable/Disable the side USB port.
    enabled: Optional[bool] = None
    #: Enable/disable use of the side USB port on the MPP device. Enabled by default.
    side_usb_enabled: Optional[bool] = None
    #: Enable/disable use of the rear USB port on the MPP device.
    rear_usb_enabled: Optional[bool] = None


class MppVlanDevice(EnabledAndValue):
    #: Indicates the PC port value of a VLAN object for an MPP object.
    pc_port: Optional[int] = None


class WifiAuthenticationMethod(str, Enum):
    #: No authentication.
    none = 'NONE'
    #: Extensible Authentication Protocol-Flexible Authentication via Secure Tunneling. Requires username and
    #: password authentication.
    eap_fast = 'EAP_FAST'
    #: Protected Extensible Authentication Protocol - Generic Token Card. Requires username and password authentication.
    peap_gtc = 'PEAP_GTC'
    #: Protected Extensible Authentication Protocol - Microsoft Challenge Handshake Authentication Protocol version
    #: 2. Requires username and password authentication.
    peap_mschapv2 = 'PEAP_MSCHAPV2'
    #: Pre-Shared Key. Requires shared passphrase for authentication.
    psk = 'PSK'
    #: Wired Equivalent Privacy. Requires encryption key for authentication.
    wep = 'WEP'


class CallHistoryMethod(str, Enum):
    #: Set call history to use the unified call history from all of the end user's devices.
    unified = 'WEBEX_UNIFIED_CALL_HISTORY'
    #: Set call history to use local device information only.
    local = 'LOCAL_CALL_HISTORY'


class DirectoryMethod(str, Enum):
    #: Set directory services to use standard XSI query method from the device.
    xsi_directory = 'XSI_DIRECTORY'
    #: Set directory services to use the Webex Enterprise directory.
    webex_directory = 'WEBEX_DIRECTORY'


class VolumeSettings(ApiModel):
    #: Specify a ringer volume level through a numeric value between 0 and 15.
    ringer_volume: Optional[int] = None
    #: Specify a speaker volume level through a numeric value between 0 and 15.
    speaker_volume: Optional[int] = None
    #: Specify a handset volume level through a numeric value between 0 and 15.
    handset_volume: Optional[int] = None
    #: Specify a headset volume level through a numeric value between 0 and 15.
    headset_volume: Optional[int] = None
    #: Enable/disable the wireless headset hookswitch control.
    e_hook_enabled: Optional[bool] = None
    #: Enable/disable to preserve the existing values on the phone and not the values defined for the device settings.
    allow_end_user_override_enabled: Optional[bool] = None


class CallForwardExpandedSoftKey(str, Enum):
    #: Set the default call forward expanded soft key behavior to single option.
    only_the_call_forward_all = 'ONLY_THE_CALL_FORWARD_ALL'
    #: Set the default call forward expanded soft key behavior to multiple menu option.
    all_call_forwards = 'ALL_CALL_FORWARDS'


class HttpProxyMode(str, Enum):
    off = 'OFF'
    auto = 'AUTO'
    manual = 'MANUAL'


class HttpProxy(ApiModel):
    #: Mode of the HTTP proxy.
    mode: Optional[HttpProxyMode] = None
    #: Enable/disable auto discovery of the URL.
    auto_discovery_enabled: Optional[bool] = None
    #: Specify the host URL if the HTTP mode is set to MANUAL.
    host: Optional[str] = None
    #: Specify the port if the HTTP mode is set to MANUAL.
    port: Optional[str] = None
    #: Specify PAC URL if auto discovery is disabled.
    pack_url: Optional[str] = None
    #: Enable/disable authentication settings.
    auth_settings_enabled: Optional[bool] = None
    #: Specify a username if authentication settings are enabled.
    username: Optional[str] = None
    #: Specify a password if authentication settings are enabled.
    password: Optional[str] = None


class BluetoothMode(str, Enum):
    phone = 'PHONE'
    hands_free = 'HANDS_FREE'
    both = 'BOTH'


class BluetoothSetting(ApiModel):
    #: Enable/disable Bluetooth.
    enabled: Optional[bool] = None
    #: Select a Bluetooth mode.
    mode: Optional[BluetoothMode] = None


class NoiseCancellation(ApiModel):
    #: Enable/disable the Noise Cancellation.
    enabled: Optional[bool] = None
    #: Enable/disable to preserve the existing values on the phone and not the value defined for the device setting.
    allow_end_user_override_enabled: Optional[bool] = None


class SoftKeyMenu(ApiModel):
    #: Specify the idle key list.
    idle_key_list: Optional[str] = None
    #: Specify the off hook key list.
    off_hook_key_list: Optional[str] = None
    #: Specify the dialing input key list.
    dialing_input_key_list: Optional[str] = None
    #: Specify the progressing key list.
    progressing_key_list: Optional[str] = None
    #: Specify the connected key list.
    connected_key_list: Optional[str] = None
    #: Specify the connected video key list.
    connected_video_key_list: Optional[str] = None
    #: Start the transfer key list.
    start_transfer_key_list: Optional[str] = None
    #: Start the conference key list.
    start_conference_key_list: Optional[str] = None
    #: Specify the conferencing key list.
    conferencing_key_list: Optional[str] = None
    #: Specify the releasing key list.
    releasing_key_list: Optional[str] = None
    #: Specify the hold key list.
    hold_key_list: Optional[str] = None
    #: Specify the ringing key list.
    ringing_key_list: Optional[str] = None
    #: Specify the shared active key list.
    shared_active_key_list: Optional[str] = None
    #: Specify the shared held key list.
    shared_held_key_list: Optional[str] = None


class PskObject(ApiModel):
    #: Specify PSK1.
    psk1: Optional[str] = None
    #: Specify PSK2.
    psk2: Optional[str] = None
    #: Specify PSK3.
    psk3: Optional[str] = None
    #: Specify PSK4.
    psk4: Optional[str] = None
    #: Specify PSK5.
    psk5: Optional[str] = None
    #: Specify PSK6.
    psk6: Optional[str] = None
    #: Specify PSK7.
    psk7: Optional[str] = None
    #: Specify PSK8.
    psk8: Optional[str] = None
    #: Specify PSK9.
    psk9: Optional[str] = None
    #: Specify PSK10.
    psk10: Optional[str] = None
    #: Specify PSK11.
    psk11: Optional[str] = None
    #: Specify PSK12.
    psk12: Optional[str] = None
    #: Specify PSK13.
    psk13: Optional[str] = None
    #: Specify PSK14.
    psk14: Optional[str] = None
    #: Specify PSK15.
    psk15: Optional[str] = None
    #: Specify PSK16.
    psk16: Optional[str] = None


class SoftKeyLayout(ApiModel):
    #: Customize SoftKey menu settings.
    soft_key_menu: Optional[SoftKeyMenu] = None
    #: Customize PSK.
    psk: Optional[PskObject] = None
    #: Default SoftKey menu settings.
    soft_key_menu_defaults: Optional[SoftKeyMenu] = None
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


class Multicast(ApiModel):
    #: Specify the multicast group URL and listening port.
    host_and_port: Optional[str] = None
    #: Specify whether the multicast group URL has an XML application URL.
    has_xml_app_url: Optional[bool] = None
    #: Specify the timeout for the XML application.
    xml_app_timeout: Optional[int] = None


class EnhancedMulticast(ApiModel):
    #: Specify the URL for the XML application.
    xml_app_url: Optional[str] = None
    #: Specify up to 10 multicast group URLs each with a unique listening port, an XML application URL, and a timeout.
    multicast_list: Optional[list[Multicast]] = None


class MppCustomization(CommonDeviceCustomization):
    """
    settings that are applicable to MPP devices.
    """
    #: Indicates whether PNAC of MPP object is enabled or not
    pnac_enabled: bool
    #: Choose the length of time (in minutes) for the phone’s backlight to remain on.
    backlight_timer: Optional[BacklightTimer] = None
    #: Holds the background object of MPP Object.
    background: BackgroundSelection
    #: The display name that appears on the phone screen.
    display_name_format: DisplayNameSelection
    #: Choose the desired logging level for an MPP devices
    default_logging_level: LoggingLevel
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    dnd_services_enabled: bool
    #: Chooses the location of the Call Queue Agent Login/Logout softkey on Multi-Platform Phones.
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkey] = None
    #: Choose the duration (in hours) of Hoteling guest login.
    hoteling_guest_association_timer: Optional[int] = None
    #: Holds the Acd object value.
    acd: AcdCustomization
    #: Indicates the short inter digit timer value.
    short_interdigit_timer: int
    #: Indicates the long inter digit timer value.
    long_interdigit_timer: int
    #: Line key labels define the format of what’s shown next to line keys.
    line_key_label_format: LineKeyLabelSelection
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note – This parameter is not
    #: supported on the MPP 8875
    line_key_led_pattern: LineKeyLedPattern = Field(alias='lineKeyLEDPattern')
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: bool
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]] = None
    #: Specify the enhanced multicast settings for the MPP device.
    enhanced_multicast: Optional[EnhancedMulticast] = None
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: int
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
    phone_language: PhoneLanguage
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: str
    #: Specify the amount of inactive time needed (in seconds) before the phone’s screen saver activates.
    screen_timeout: EnabledAndValue
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    usb_ports_enabled: Optional[bool] = None
    #: By default the Side USB port is enabled to support KEMs and other peripheral devices. Use the option to disable
    #: use of this port.
    usb_ports: Optional[UsbPortsObject] = None
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanDevice] = None
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetwork] = None
    migration_url: Optional[str] = None  # TODO: undocumented
    #: Specify the call history information to use. Only applies to user devices.
    call_history: Optional[CallHistoryMethod] = None
    #: Specify the directory services to use.
    contacts: Optional[DirectoryMethod] = None
    #: Enable/disable the availability of the webex meetings functionality from the phone.
    webex_meetings_enabled: Optional[bool] = None
    #: Specify all volume level values on the phone.
    volume_settings: Optional[VolumeSettings] = None
    #: Specify the call forward expanded soft key behavior.
    cf_expanded_soft_key: Optional[CallForwardExpandedSoftKey] = None
    #: Specify HTTP Proxy values.
    http_proxy: Optional[HttpProxy] = None
    #: Enable/disable the visibility of the bluetooth menu on the MPP device.
    bluetooth: Optional[BluetoothSetting] = None
    #: Enable/disable the use of the PC passthrough ethernet port on supported phone models.
    pass_through_port_enabled: Optional[bool] = None
    #: Enable/disable the ability for an end user to set a local password on the phone to restrict local access to the
    #: device.
    user_password_override_enabled: Optional[bool] = None
    #: Enable/disable the default screen behavior when inbound calls are received.
    active_call_focus_enabled: Optional[bool] = None
    #: Enable/disable peer firmware sharing.
    peer_firmware_enabled: Optional[bool] = None
    #: Enable/disable local noise cancellation on active calls from the device.
    noise_cancellation: Optional[NoiseCancellation] = None
    #: Enable/disable visibility of the Accessibility Voice Feedback menu on the MPP device.
    voice_feedback_accessibility_enabled: Optional[bool] = None
    #: Enable/disable availability of dial assist feature on the phone.
    dial_assist_enabled: Optional[bool] = None
    #: Specify the number of calls per unique line appearance on the phone.
    calls_per_line: Optional[int] = None
    #: Enable/disable the visual indication of missed calls.
    missed_call_notification_enabled: Optional[bool] = None
    #: Specify the softkey layout per phone menu state.
    soft_key_layout: Optional[SoftKeyLayout] = None
    #: Specify the image option for the MPP 8875 phone background.
    background_image8875: Optional[BackgroundImageColor] = None
    #: Specify the use of the backlight feature on 6800 nad 7800 series devices.
    backlight_timer_68xx78xx: Optional[BacklightTimer68XX78XX] = Field(alias='backlightTimer68XX78XX', default=None)
    #: Enable/disable monitoring for MPP non-primary device.
    allow_monitor_lines_enabled: Optional[bool] = None
    #: Enable/disable SIP media streams to go directly between phones on the same local network.
    ice_enabled: Optional[bool] = None

    # !!
    # #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    # wifi_network: Optional[WifiNetwork]
    # migration_url: Optional[str]


class WifiCustomization(ApiModel):
    # TODO: implement as soon as properly documented on developer.webex.com

    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: AudioCodecPriority
    ldap: Any
    web_access: Any


class DeviceCustomizations(ApiModel):
    """
    Customization object of the device settings.

    At the device level only one of ata, dect, and mpp is set. At location and org level all three
    customizations are set.
    """
    ata: Optional[AtaCustomization] = None
    dect: Optional[DectCustomization] = None
    mpp: Optional[MppCustomization] = None
    wifi: Optional[WifiCustomization] = None


class DeviceCustomization(ApiModel):
    """
    Device customization
    """

    @field_validator('last_update_time', mode='before')
    def update_time(cls, v):
        """

        :meta private:
        """
        if not v:
            return v
        try:
            v = datetime.fromtimestamp(v / 1000)
        finally:
            pass
        return v

    #: customization object of the device settings.
    customizations: DeviceCustomizations
    #: Indicates if customization is allowed at repective (location or device) level.
    #: If true - customized at this level.
    #: If false - not customized, using higher level config (location or org).
    #: Only present in location and device level customization response
    custom_enabled: Optional[bool] = None
    #: Indicates the progress of the device update. Not present at device level
    update_in_progress: Optional[bool] = None
    #: Indicates the device count. Not present at device level
    device_count: Optional[int] = None
    #: Indicates the last updated time.
    last_update_time: Optional[datetime] = None


class PrimaryOrShared(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'
    #: Device is a shared line.
    mobility = 'MOBILITY'
    #: Device is a hotdesking guest.
    hotdesking_guest = 'HOTDESKING_GUEST'


class MediaFileType(str, Enum):
    """
    Media Type of the audio file.
    """
    #: WMA File Extension.
    wma = 'WMA'
    #: WAV File Extension.
    wav = 'WAV'
    #: 3GP File Extension.
    three_gp = '3GP'


class AnnouncementLevel(Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'
    #: Specifies this audio file is configured on instance level.
    entity = 'ENTITY'


class AnnAudioFile(ApiModel):
    """
    Announcement Audio Files
    """
    #: A unique identifier for the announcement. name, mediaFileType, level are mandatory if id is not provided for
    #: uploading an announcement.
    id: Optional[str] = None
    #: Name of the file.
    file_name: Optional[str] = None
    #: Media Type of the audio file.
    media_file_type: Optional[MediaFileType] = None
    #: Audio announcement file type location.
    level: Optional[AnnouncementLevel] = None


class OwnerType(str, Enum):
    #: The PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: The phone number's owner is a person.
    people = 'PEOPLE'
    #: The PSTN phone number's owner is a virtual line.
    virtual_line = 'VIRTUAL_LINE'
    #: The PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: The PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: The PSTN phone number's owner is a paging group.
    paging_group = 'PAGING_GROUP'
    #: The PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: The PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: The PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Single Number Reach.
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    #: The PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: The PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: The PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: The PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: The PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class NumberOwner(ApiModel):
    """
    Owner of a phone number
    """
    #: ID of the owner to which PSTN Phone number is assigned.
    owner_id: Optional[str] = Field(alias='id', default=None)
    #: Type of the PSTN phone number's owner
    owner_type: Optional[OwnerType] = Field(alias='type', default=None)
    #: Last name of the PSTN phone number's owner
    last_name: Optional[str] = None
    #: First name of the PSTN phone number's owner
    first_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner and will only be returned when the owner type is a Feature.
    display_name: Optional[str] = None


class ApplyLineKeyTemplateAction(str, Enum):
    #: Used to apply LinekeyTemplate to devices.
    apply_template = 'APPLY_TEMPLATE'
    #: Used to reset devices to its default Linekey Template configurations.
    apply_default_templates = 'APPLY_DEFAULT_TEMPLATES'


class AssignedDectNetwork(ApiModel):
    #: Unique identifier for a dect network.
    id: Optional[str] = None
    #: Identifier for device DECT network.
    name: Optional[str] = None
    #: Indicates whether the virtual profile is the primary line.
    primary_enabled: Optional[bool] = None
    #: Number of dect handsets assigned to the virtual profile.
    number_of_handsets_assigned: Optional[int] = None
    #: Location details of virtual line.
    location: Optional[IdAndName] = None


class DevicePlatform(str, Enum):
    cisco = 'cisco'
    microsoft_teams_room = 'microsoftTeamsRoom'
