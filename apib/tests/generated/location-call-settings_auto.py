from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ArrayOfExtensionsObject', 'AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
            'AudioAnnouncementFileGetObjectMediaFileType', 'CallBackEffectiveLevel', 'CallBackMemberType',
            'CallBackQuality', 'CallBackSelected', 'ExtensionStatusObject', 'ExtensionStatusObjectState',
            'ExtentionStatusObject', 'GetLocationCallBackNumberObject', 'GetLocationCallBackNumberObjectLocationInfo',
            'GetLocationCallBackNumberObjectLocationMemberInfo', 'GetMusicOnHoldObject',
            'GetMusicOnHoldObjectGreeting', 'GetPrivateNetworkConnectObject',
            'GetPrivateNetworkConnectObjectNetworkConnectionType', 'GetTelephonyLocationObject',
            'GetTelephonyLocationObjectCallingLineId', 'GetTelephonyLocationObjectConnection', 'ListLocationObject',
            'ListLocationsWebexCallingDetailsResponse', 'LocationCallingResponseWithId',
            'PostLocationAnnouncementLanguageObject', 'PostLocationCallingRequest',
            'PostLocationCallingRequestAddress', 'PostValidateExtensionResponse',
            'PostValidateExtensionResponseStatus', 'PutLocationCallBackNumberObject', 'PutTelephonyLocationObject',
            'ReadTheListOfDialPatternsResponse', 'ReadTheListOfRoutingChoicesResponse', 'RouteIdentity', 'RouteType',
            'StatusOfExtensionsObject']


class ArrayOfExtensionsObject(ApiModel):
    #: Array of extensions that will be validated.
    extensions: Optional[list[str]] = None


class CallBackEffectiveLevel(str, Enum):
    #: Location TN.
    location_number = 'LOCATION_NUMBER'
    #: Assigned number of a user or workspace in the location.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    _none_ = 'NONE'


class CallBackMemberType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'


class CallBackQuality(str, Enum):
    recommended = 'RECOMMENDED'
    not_recommended = 'NOT_RECOMMENDED'
    invalid = 'INVALID'


class CallBackSelected(str, Enum):
    #: Location TN.
    location_number = 'LOCATION_NUMBER'
    #: Assigned number of a user or workspace in the location.
    location_member_number = 'LOCATION_MEMBER_NUMBER'


class ExtensionStatusObjectState(str, Enum):
    #: Extension is valid.
    valid = 'VALID'
    #: Extension already assigned to another group.
    duplicate = 'DUPLICATE'
    #: Extension already exists in the request body and was already verified.
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    #: Extension is invalid.
    invalid = 'INVALID'


class ExtensionStatusObject(ApiModel):
    #: Unique extension which will be validated at the location level.
    #: example: 407721
    extension: Optional[str] = None
    #: State of the extension after it was validated.
    #: example: VALID
    state: Optional[ExtensionStatusObjectState] = None
    #: Error code of the state in case extension is not valid.
    #: example: 9495.0
    error_code: Optional[int] = None
    #: Message assigned to the error code.
    #: example: [Error 9495] The extension is not available. It is already assigned as a Call Park Extension: 407721.
    message: Optional[str] = None


class GetLocationCallBackNumberObjectLocationInfo(ApiModel):
    #: The location DN.
    #: example: +12145551767
    phone_number: Optional[str] = None
    #: The name of the location.
    #: example: CPAPI_Dev_Test_Location_DND
    name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: LOCATION_NUMBER
    effective_level: Optional[CallBackEffectiveLevel] = None
    #: Location calling line ID (CLID) number. Avaliable only when number is present and quality would be invalid.
    #: example: +12145551767
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[CallBackQuality] = None


class GetLocationCallBackNumberObjectLocationMemberInfo(ApiModel):
    #: The member DN.
    #: example: +12145551767
    phone_number: Optional[str] = None
    #: The member first name.
    #: example: Jim
    first_name: Optional[str] = None
    #: The member last name. Always contains `.` if the member is a place.
    #: example: Grey
    last_name: Optional[str] = None
    #: Member ID of user/place within the location.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MmQ3YTY3MS00YmVlLTQ2MDItOGVkOC1jOTFmNjU5NjcxZGI
    member_id: Optional[str] = None
    #: Member Type.
    #: example: PEOPLE
    member_type: Optional[CallBackMemberType] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: LOCATION_MEMBER_NUMBER
    effective_level: Optional[CallBackEffectiveLevel] = None
    #: Location CLID number. Avaliable only when number is present and quality would be invalid.
    #: example: +12145551767
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[CallBackQuality] = None


class GetLocationCallBackNumberObject(ApiModel):
    #: Data relevant to this location.
    location_info: Optional[GetLocationCallBackNumberObjectLocationInfo] = None
    #: Data relevant to the user/place (member) selected for ECBN.
    location_member_info: Optional[GetLocationCallBackNumberObjectLocationMemberInfo] = None
    #: Selected number type to configure emergency call back.
    #: example: LOCATION_MEMBER_NUMBER
    selected: Optional[CallBackSelected] = None


class GetMusicOnHoldObjectGreeting(str, Enum):
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets
    #: the customer know they are still connected.
    system = 'SYSTEM'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    _3_gp = '3GP'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    file_name: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    media_file_type: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    #: example: ORGANIZATION
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class GetMusicOnHoldObject(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    #: example: True
    call_hold_enabled: Optional[bool] = None
    #: If enabled, music will be played when call is parked.
    #: example: True
    call_park_enabled: Optional[bool] = None
    #: Greeting type for the location.
    #: example: SYSTEM
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_file: Optional[AudioAnnouncementFileGetObject] = None


class GetPrivateNetworkConnectObjectNetworkConnectionType(str, Enum):
    #: Use public internet for the location's connection type.
    public_internet = 'PUBLIC_INTERNET'
    #: Use private network connect for the location's connection type.
    private_network = 'PRIVATE_NETWORK'


class GetPrivateNetworkConnectObject(ApiModel):
    #: Network Connection Type for the location.
    #: example: PUBLIC_INTERNET
    network_connection_type: Optional[GetPrivateNetworkConnectObjectNetworkConnectionType] = None


class GetTelephonyLocationObjectCallingLineId(ApiModel):
    #: Group calling line ID name. By default the Org name.
    #: example: 'Denver Incoming'
    name: Optional[str] = None
    #: Directory Number / Main number in E.164 Format.
    #: example: '+12145555698'
    phone_number: Optional[str] = None


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class GetTelephonyLocationObjectConnection(ApiModel):
    #: Webex Calling location only suppports `TRUNK` and `ROUTE_GROUP` connection type.
    type: Optional[RouteType] = None
    #: A unique identifier of route type.
    #: example: 'Y2lzY29zcGFyazovL3VzL1RSVU5LL2M1MGIxZjY2LTRjODMtNDAzNy04NjM1LTg2ZjlkM2VkZDQ5MQ'
    id: Optional[str] = None


class GetTelephonyLocationObject(ApiModel):
    #: A unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: The name of the location.
    #: example: 'Denver'
    name: Optional[str] = None
    #: Location's phone announcement language.
    #: example: 'fr_fr'
    announcement_language: Optional[str] = None
    #: Location calling line information.
    calling_line_id: Optional[GetTelephonyLocationObjectCallingLineId] = None
    #: Connection details are only returned for local PSTN types of `TRUNK` or `ROUTE_GROUP`.
    connection: Optional[GetTelephonyLocationObjectConnection] = None
    #: External Caller ID Name value. Unicode characters.
    #: example: 'Big Corp Denver'
    external_caller_id_name: Optional[str] = None
    #: Limit on the number of people at the location, Read-Only.
    #: example: 500000.0
    user_limit: Optional[int] = None
    #: Emergency Location Identifier for a location. Set this field to provide the SIP access network information to
    #: the provider which will be used to populate the SIP P-Access-Network-Info header. This is helpful to establish
    #: the location of a device when you make an emergency call.
    #: example: 'Rcdn'
    p_access_network_info: Optional[str] = None
    #: Must dial to reach an outside line, default is None.
    #: example: 'Rcdn'
    outside_dial_digit: Optional[str] = None
    #: Must dial a prefix when calling between locations having same extension within same location.
    #: example: '2'
    routing_prefix: Optional[datetime] = None
    #: IP Address, hostname, or domain. Read-Only.
    #: example: '98079822.int10.bcld.webex.com'
    default_domain: Optional[str] = None
    #: Chargeable number for the line placing the call. When this is set, all calls placed from this location will
    #: include a P-Charge-Info header with the selected number in the SIP INVITE.
    #: example: '+14158952369'
    charge_number: Optional[str] = None


class ListLocationObject(ApiModel):
    #: A unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzljYTNhZmQ3LTE5MjYtNGQ0ZS05ZDA3LTk5ZDJjMGU4OGFhMA
    id: Optional[str] = None
    #: The name of the location.
    #: example: 'Denver'
    name: Optional[str] = None
    #: Must dial to reach an outside line, default is None.
    #: example: '12'
    outside_dial_digit: Optional[datetime] = None
    #: Must dial a prefix when calling between locations having the same extension within the same location.
    #: example: '2'
    routing_prefix: Optional[datetime] = None
    #: Location calling line information.
    calling_line_id: Optional[GetTelephonyLocationObjectCallingLineId] = None
    #: True if E911 setup is required.
    #: example: True
    e911_setup_required: Optional[bool] = None


class LocationCallingResponseWithId(ApiModel):
    #: A unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzljYTNhZmQ3LTE5MjYtNGQ0ZS05ZDA3LTk5ZDJjMGU4OGFhMA
    id: Optional[str] = None


class PostLocationAnnouncementLanguageObject(ApiModel):
    #: Set to `true` to change announcement language for existing people and workspaces.
    agent_enabled: Optional[bool] = None
    #: Set to `true` to change announcement language for existing feature configurations.
    service_enabled: Optional[bool] = None
    #: Language code.
    #: example: en_us
    announcement_language_code: Optional[str] = None


class PostLocationCallingRequestAddress(ApiModel):
    #: Address 1 of the location.
    #: example: 771 Alder Drive
    address1: Optional[str] = None
    #: Address 2 of the location.
    #: example: Cisco Site 5
    address2: Optional[str] = None
    #: City of the location.
    #: example: Milpitas
    city: Optional[str] = None
    #: State code of the location.
    #: example: CA
    state: Optional[str] = None
    #: Postal code of the location.
    #: example: 95035
    postal_code: Optional[str] = None
    #: ISO-3166 2-Letter country code of the location.
    #: example: US
    country: Optional[str] = None


class PostLocationCallingRequest(ApiModel):
    #: A unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzljYTNhZmQ3LTE5MjYtNGQ0ZS05ZDA3LTk5ZDJjMGU4OGFhMA
    id: Optional[str] = None
    #: The name of the location.
    #: example: 'Denver'
    name: Optional[str] = None
    #: Time zone associated with this location. Refer to this `link
    #: <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_ for the format.
    #: example: 'America/Chicago'
    time_zone: Optional[str] = None
    #: Default email language.
    #: example: 'en_us'
    preferred_language: Optional[str] = None
    #: Location's phone announcement language.
    #: example: 'fr_fr'
    announcement_language: Optional[str] = None
    #: The address of the location.
    address: Optional[PostLocationCallingRequestAddress] = None


class PostValidateExtensionResponseStatus(str, Enum):
    #: Validated succesfully.
    ok = 'OK'
    #: Validated with errors.
    errors = 'ERRORS'


class ExtentionStatusObject(ApiModel):
    #: Indicates the extention ID for the status.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Indicates the status for the given extention id.
    #: example: VALID
    state: Optional[ExtensionStatusObjectState] = None
    #: Error Code.
    #: example: 59475.0
    error_code: Optional[int] = None
    #: example: The extension is not available. It is already assigned to a virtual extension
    message: Optional[str] = None


class PostValidateExtensionResponse(ApiModel):
    #: OK , ERRORS
    status: Optional[PostValidateExtensionResponseStatus] = None
    extension_status: Optional[list[ExtentionStatusObject]] = None


class PutLocationCallBackNumberObject(ApiModel):
    #: Selected number type to configure emergency call back.
    #: example: LOCATION_MEMBER_NUMBER
    selected: Optional[CallBackSelected] = None
    #: Member ID of user/place within the location. Required if `LOCATION_MEMBER_NUMBER` is selected.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9hOTc0MzVjZi0zYTZmLTRmNGYtOWU1OC00OTI2OTQ5MDkwMWY
    location_member_id: Optional[str] = None


class PutTelephonyLocationObject(ApiModel):
    #: Location's phone announcement language.
    #: example: 'fr_fr'
    announcement_language: Optional[str] = None
    #: Location calling line information.
    calling_line_id: Optional[GetTelephonyLocationObjectCallingLineId] = None
    #: Connection details can only be modified to and from local PSTN types of `TRUNK` and `ROUTE_GROUP`.
    connection: Optional[GetTelephonyLocationObjectConnection] = None
    #: Denve' (string) - External Caller ID Name value. Unicode characters.
    #: example: 'Big Corp
    external_caller_id_name: Optional[str] = None
    #: Location Identifier.
    #: example: 'Rcdn'
    p_access_network_info: Optional[str] = None
    #: Must dial to reach an outside line. Default is None.
    #: example: '12'
    outside_dial_digit: Optional[datetime] = None
    #: Must dial a prefix when calling between locations having same extension within same location; should be numeric.
    #: example: '2'
    routing_prefix: Optional[datetime] = None
    #: Chargeable number for the line placing the call. When this is set, all calls placed from this location will
    #: include a P-Charge-Info header with the selected number in the SIP INVITE.
    #: example: '+14158952369'
    charge_number: Optional[str] = None


class RouteIdentity(ApiModel):
    #: ID of the route type.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: A unique name for the route identity.
    #: example: route_identity_name
    name: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class StatusOfExtensionsObject(ApiModel):
    #: Status of the validated array of extensions
    #: example: OK
    status: Optional[PostValidateExtensionResponseStatus] = None
    #: Array of extensions statuses.
    extension_status: Optional[list[ExtensionStatusObject]] = None


class ListLocationsWebexCallingDetailsResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[ListLocationObject]] = None


class ReadTheListOfDialPatternsResponse(ApiModel):
    #: Array of dial patterns. An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
    #: optional wildcard characters.
    dial_patterns: Optional[list[str]] = None


class ReadTheListOfRoutingChoicesResponse(ApiModel):
    #: Array of route identities.
    route_identities: Optional[list[RouteIdentity]] = None
