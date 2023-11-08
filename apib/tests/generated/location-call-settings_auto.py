from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
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


class LocationCallSettingsApi(ApiChild, base='telephony/config'):
    """
    Location Call Settings
    
    Location Call Settings  supports reading and writing of Webex Calling Location settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list_locations_webex_calling_details(self, org_id: str = None, max_: int = None, start: int = None,
                                             name: str = None, order: str = None) -> list[ListLocationObject]:
        """
        List Locations Webex Calling Details

        Lists Webex Calling locations for an organization with Webex Calling details.
        
        Searching and viewing locations with Webex Calling details in your
        organization require an administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param org_id: List locations for this organization.
        :type org_id: str
        :param max_: Limit the maximum number of locations in the response.
        :type max_: int
        :param start: Specify the offset from the first result that you want to fetch.
        :type start: int
        :param name: List locations whose name contains this string.
        :type name: str
        :param order: Sort the list of locations based on `name`, either asc or desc.
        :type order: str
        :rtype: list[ListLocationObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('locations')
        ...


    def enable_a_location_for_webex_calling(self, id: str, name: str, time_zone: str, preferred_language: str,
                                            announcement_language: str, address: PostLocationCallingRequestAddress,
                                            org_id: str = None) -> str:
        """
        Enable a Location for Webex Calling

        Enable a location by adding it to Webex Calling. This add Webex Calling support to a
        location created created using the POST /v1/locations API.
        
        Locations are used to support calling features which can be defined at the location level.
        
        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param id: A unique identifier for the location.
        :type id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location. Refer to this `link
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_ for the format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param address: The address of the location.
        :type address: PostLocationCallingRequestAddress
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('locations')
        ...


    def get_location_webex_calling_details(self, location_id: str, org_id: str = None) -> GetTelephonyLocationObject:
        """
        Get Location Webex Calling Details

        Shows Webex Calling details for a location, by ID.
        
        Specifies the location ID in the locationId parameter in the URI.
        
        Searching and viewing locations in your organization requires an administrator auth token with the
        spark-admin:telephony_config_read scope.

        :param location_id: Retrieve Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Webex Calling location attributes for this organization.
        :type org_id: str
        :rtype: :class:`GetTelephonyLocationObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}')
        ...


    def update_location_webex_calling_details(self, location_id: str, announcement_language: str,
                                              calling_line_id: GetTelephonyLocationObjectCallingLineId,
                                              connection: GetTelephonyLocationObjectConnection,
                                              external_caller_id_name: str, p_access_network_info: str,
                                              outside_dial_digit: Union[str, datetime], routing_prefix: Union[str,
                                              datetime], charge_number: str, org_id: str = None):
        """
        Update Location Webex Calling Details

        Update Webex Calling details for a location, by ID.
        
        Specifies the location ID in the `locationId` parameter in the URI.
        
        Modifying the `connection` via API is only supported for the local PSTN types of `TRUNK` and `ROUTE_GROUP`.
        
        Updating a location in your organization requires an administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param location_id: Updating Webex Calling location attributes for this location.
        :type location_id: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param calling_line_id: Location calling line information.
        :type calling_line_id: GetTelephonyLocationObjectCallingLineId
        :param connection: Connection details can only be modified to and from local PSTN types of `TRUNK` and
            `ROUTE_GROUP`.
        :type connection: GetTelephonyLocationObjectConnection
        :param external_caller_id_name: Denve' (string) - External Caller ID Name value. Unicode characters.
        :type external_caller_id_name: str
        :param p_access_network_info: Location Identifier.
        :type p_access_network_info: str
        :param outside_dial_digit: Must dial to reach an outside line. Default is None.
        :type outside_dial_digit: Union[str, datetime]
        :param routing_prefix: Must dial a prefix when calling between locations having same extension within same
            location; should be numeric.
        :type routing_prefix: Union[str, datetime]
        :param charge_number: Chargeable number for the line placing the call. When this is set, all calls placed from
            this location will include a P-Charge-Info header with the selected number in the SIP INVITE.
        :type charge_number: str
        :param org_id: Updating Webex Calling location attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}')
        ...


    def change_announcement_language(self, location_id: str, agent_enabled: bool, service_enabled: bool,
                                     announcement_language_code: str, org_id: str = None):
        """
        Change Announcement Language

        Change announcement language for the given location.
        
        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.
        
        Changing the announcement language for the given location requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param agent_enabled: Set to `true` to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to `true` to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param announcement_language_code: Language code.
        :type announcement_language_code: str
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        ...


    def read_the_list_of_dial_patterns(self, dial_plan_id: str, org_id: str = None, dial_pattern: str = None,
                                       max_: int = None, start: int = None, order: str = None) -> list[str]:
        """
        Read the List of Dial Patterns

        List all Dial Patterns for the organization.
        
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: ID of the organization to which the dial patterns belong.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters.
        Valid wildcard characters are `!` (matches any sequence of digits) and `X` (matches a single digit, 0-9).
        The `!` wildcard can only occur once at the end and only in an E.164 pattern
        :type dial_pattern: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the dial patterns according to the designated fields.  Available sort fields:
            `dialPattern`.
        :type order: str
        :rtype: list[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if dial_pattern is not None:
            params['dialPattern'] = dial_pattern
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        ...


    def get_a_location_emergency_callback_number(self, location_id: str,
                                                 location_info: GetLocationCallBackNumberObjectLocationInfo,
                                                 location_member_info: GetLocationCallBackNumberObjectLocationMemberInfo,
                                                 selected: CallBackSelected, org_id: str = None):
        """
        Get a Location Emergency callback number

        Get location emergency callback number.
        
        * To retrieve location callback number requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Update location attributes for this location.
        :type location_id: str
        :param location_info: Data relevant to this location.
        :type location_info: GetLocationCallBackNumberObjectLocationInfo
        :param location_member_info: Data relevant to the user/place (member) selected for ECBN.
        :type location_member_info: GetLocationCallBackNumberObjectLocationMemberInfo
        :param selected: Selected number type to configure emergency call back.
        :type selected: CallBackSelected
        :param org_id: Update location attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/features/emergencyCallbackNumber')
        ...


    def update_a_location_emergency_callback_number(self, location_id: str, selected: CallBackSelected,
                                                    location_member_id: str, org_id: str = None):
        """
        Update a Location Emergency callback number

        Update details for a location emergency callback number.
        
        * Updating a location callback number requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param location_id: Update location attributes for this location.
        :type location_id: str
        :param selected: Selected number type to configure emergency call back.
        :type selected: CallBackSelected
        :param location_member_id: Member ID of user/place within the location. Required if `LOCATION_MEMBER_NUMBER` is
            selected.
        :type location_member_id: str
        :param org_id: Update location attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/features/emergencyCallbackNumber')
        ...


    def validate_the_list_of_extensions(self, extensions: list[str],
                                        org_id: str = None) -> PostValidateExtensionResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions.
        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param extensions: Array of Strings of IDs of the Extensions.
        :type extensions: list[str]
        :param org_id: Validate Extension for this organization.
        :type org_id: str
        :rtype: :class:`PostValidateExtensionResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('actions/validateExtensions/invoke')
        ...


    def validate_extensions(self, location_id: str, extensions: list[str],
                            org_id: str = None) -> StatusOfExtensionsObject:
        """
        Validate Extensions

        Validate extensions for a specific location.
        
        Validating extensions requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Validate extensions for this location.
        :type location_id: str
        :param extensions: Array of extensions that will be validated.
        :type extensions: list[str]
        :param org_id: Validate extensions for this organization.
        :type org_id: str
        :rtype: :class:`StatusOfExtensionsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/actions/validateExtensions/invoke')
        ...


    def update_music_on_hold(self, location_id: str, call_hold_enabled: bool, call_park_enabled: bool,
                             greeting: GetMusicOnHoldObjectGreeting, audio_file: AudioAnnouncementFileGetObject,
                             org_id: str = None):
        """
        Update Music On Hold

        Update the location's music on hold settings.
        
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        
        Updating a location's music on hold settings requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        :param greeting: Greeting type for the location.
        :type greeting: GetMusicOnHoldObjectGreeting
        :param audio_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_file: AudioAnnouncementFileGetObject
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/musicOnHold')
        ...


    def get_music_on_hold(self, location_id: str, org_id: str = None) -> GetMusicOnHoldObject:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.
        
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        
        Retrieving a location's music on hold settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve music on hold settings for this location.
        :type location_id: str
        :param org_id: Retrieve music on hold settings for this organization.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/musicOnHold')
        ...


    def get_private_network_connect(self, location_id: str,
                                    org_id: str = None) -> GetPrivateNetworkConnectObjectNetworkConnectionType:
        """
        Get Private Network Connect

        Retrieve the location's network connection type.
        
        Network Connection Type determines if the location's network connection is public or private.
        
        Retrieving a location's network connection type requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve the network connection type for this organization.
        :type org_id: str
        :rtype: GetPrivateNetworkConnectObjectNetworkConnectionType
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        ...


    def update_private_network_connect(self, location_id: str,
                                       network_connection_type: GetPrivateNetworkConnectObjectNetworkConnectionType,
                                       org_id: str = None):
        """
        Update Private Network Connect

        Update the location's network connection type.
        
        Network Connection Type determines if the location's network connection is public or private.
        
        Updating a location's network connection type requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update the network connection type for this location.
        :type location_id: str
        :param network_connection_type: Network Connection Type for the location.
        :type network_connection_type: GetPrivateNetworkConnectObjectNetworkConnectionType
        :param org_id: Update network connection type for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        ...


    def read_the_list_of_routing_choices(self, org_id: str = None, route_group_name: str = None,
                                         trunk_name: str = None, max_: int = None, start: int = None,
                                         order: str = None) -> list[RouteIdentity]:
        """
        Read the List of Routing Choices

        List all Routes for the organization.
        
        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.
        
        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: List route identities for this organization.
        :type org_id: str
        :param route_group_name: Return the list of route identities matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of route identities matching the Trunk name..
        :type trunk_name: str
        :param max_: Limit the number of objects returned to this maximum count.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the route identities according to the designated fields.  Available sort fields:
            `routeName`, `routeType`.
        :type order: str
        :rtype: list[RouteIdentity]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('routeChoices')
        ...

    ...