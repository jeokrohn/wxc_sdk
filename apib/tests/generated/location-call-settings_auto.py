from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
           'AudioAnnouncementFileGetObjectMediaFileType', 'BatchJobError', 'BatchResponse',
           'BatchResponseLatestExecutionExitCode', 'CallBackEffectiveLevel', 'CallBackMemberType', 'CallBackQuality',
           'CallBackSelected', 'Counts', 'Error', 'ErrorMessage', 'ExtensionStatusObject',
           'ExtensionStatusObjectState', 'GetLocationCallBackNumberObject',
           'GetLocationCallBackNumberObjectLocationInfo', 'GetLocationCallBackNumberObjectLocationMemberInfo',
           'GetMusicOnHoldObject', 'GetMusicOnHoldObjectGreeting',
           'GetPrivateNetworkConnectObjectNetworkConnectionType', 'GetTelephonyLocationObject',
           'GetTelephonyLocationObjectCallingLineId', 'GetTelephonyLocationObjectConnection', 'JobExecutionStatus',
           'ListLocationObject', 'LocationAvailableNumberObject', 'LocationCallInterceptAvailableNumberObject',
           'LocationCallSettingsApi', 'LocationECBNAvailableNumberObject', 'LocationECBNAvailableNumberObjectOwner',
           'LocationObject', 'LocationPUTResponse', 'NumberObject', 'NumberObjectOwner', 'NumberOwnerType',
           'PostLocationCallingRequestAddress', 'PostValidateExtensionResponse',
           'PostValidateExtensionResponseStatus', 'RouteIdentity', 'RouteType', 'State', 'StepExecutionStatuses',
           'TelephonyType', 'WebexGoAvailableNumberObject']


class CallBackEffectiveLevel(str, Enum):
    #: Location TN.
    location_number = 'LOCATION_NUMBER'
    #: Assigned number of a user or workspace in the location.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    none_ = 'NONE'


class CallBackMemberType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    virtual_line = 'VIRTUAL_LINE'


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
    #: example: 9495
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
    d3_gp = '3GP'


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
    #: PSTN connection ID given for locations with a PSTN subscription.
    #: example: 'trial'
    subscription_id: Optional[str] = None
    #: External Caller ID Name value. Unicode characters.
    #: example: 'Big Corp Denver'
    external_caller_id_name: Optional[str] = None
    #: Limit on the number of people at the location. Read-Only.
    #: example: 500000
    user_limit: Optional[int] = None
    #: Emergency Location Identifier for a location. Set this field to provide the SIP access network information to
    #: the provider which will be used to populate the SIP P-Access-Network-Info header. This is helpful to establish
    #: the location of a device when you make an emergency call.
    #: example: 'Rcdn'
    p_access_network_info: Optional[str] = None
    #: Must dial to reach an outside line, default is None.
    #: example: 'Rcdn'
    outside_dial_digit: Optional[str] = None
    #: True when enforcing outside dial digit at location level to make PSTN calls.
    #: example: True
    enforce_outside_dial_digit: Optional[bool] = None
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
    #: True when enforcing outside dial digit at location level to make PSTN calls.
    #: example: True
    enforce_outside_dial_digit: Optional[bool] = None
    #: Must dial a prefix when calling between locations having the same extension within the same location.
    #: example: '2'
    routing_prefix: Optional[datetime] = None
    #: Location calling line information.
    calling_line_id: Optional[GetTelephonyLocationObjectCallingLineId] = None
    #: True if E911 setup is required.
    #: example: True
    e911_setup_required: Optional[bool] = None


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


class PostValidateExtensionResponseStatus(str, Enum):
    #: Validated succesfully.
    ok = 'OK'
    #: Validated with errors.
    errors = 'ERRORS'


class PostValidateExtensionResponse(ApiModel):
    #: OK , ERRORS
    status: Optional[PostValidateExtensionResponseStatus] = None
    extension_status: Optional[list[ExtensionStatusObject]] = None


class RouteIdentity(ApiModel):
    #: ID of the route type.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: A unique name for the route identity.
    #: example: route_identity_name
    name: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class LocationPUTResponse(ApiModel):
    #: Admin Batch Job ID returned if a routing prefix change occurs.
    #: example: Y2lzY29zcGFyazovL3VzL0pPQl9JRC84MWU3ODFjOC1kMDI3LTQ1ZjMtODIyZi05OTRiMmYzZTA0MzA
    batch_job_id: Optional[str] = None
    #: Error message if the admin batch job is not triggered if a routing prefix change occurs.
    #: example: UpdateRoutingPrefix batch job not triggered for Location
    failure_reason: Optional[str] = None


class BatchResponseLatestExecutionExitCode(str, Enum):
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


class StepExecutionStatuses(ApiModel):
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


class JobExecutionStatus(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Job execution start time in UTC format.
    start_time: Optional[str] = None
    #: Job execution end time in UTC format.
    end_time: Optional[str] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatuses]] = None


class Counts(ApiModel):
    #: Indicates the total number of records whose routing prefix update is successful.
    routing_prefix_updated: Optional[int] = None
    #: Indicates the total number of records whose routing prefix update failed.
    routing_prefix_failed: Optional[int] = None


class BatchResponse(ApiModel):
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
    job_execution_status: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[BatchResponseLatestExecutionExitCode] = None
    #: Job statistics.
    counts: Optional[Counts] = None


class ErrorMessage(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location ID in which the error occurs. For a move operation this is the target
    #: location ID.
    location_id: Optional[str] = None


class Error(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessage]] = None


class BatchJobError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    #: row number of failed record.
    item_number: Optional[int] = None
    error: Optional[Error] = None


class State(str, Enum):
    #: The number is active.
    active = 'ACTIVE'
    #: The number is inactive.
    inactive = 'INACTIVE'


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzkzZmQ1ZDMyLTRmYmItNGNjMS04ZTYxLTE0YTA1ZDhhMTIzMw
    id: Optional[str] = None
    #: Name of the location.
    #: example: RCDN
    name: Optional[str] = None


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice portal.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voice mail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class NumberObjectOwner(ApiModel):
    #: ID of the owner to which the number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfTElORS82MGQxZGJlMC02MmNjLTQxZTEtOWE2MC1mZWQ1YmJkODUxZGQ
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner and will only be returned when the owner type is PEOPLE or PLACE or
    #: VIRTUAL_PROFILE.
    #: example: Mark
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner and will only be returned when the owner type is PEOPLE or PLACE or
    #: VIRTUAL_PROFILE.
    #: example: Zand
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: Mark Zand
    display_name: Optional[str] = None


class NumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Defines whether the number is active or not.
    #: example: ACTIVE
    state: Optional[State] = None
    #: Flag to indicate if the number is used as the location's main number.
    is_main_number: Optional[bool] = None
    #: Flag to indicate if the number is toll free.
    toll_free_number: Optional[bool] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    #: The details of this number's location.
    location: Optional[LocationObject] = None
    owner: Optional[NumberObjectOwner] = None


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class LocationAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[State] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[NumberObjectOwner] = None


class WebexGoAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[State] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None


class LocationECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the phone number's owner.
    #: example: PEOPLE
    type: Optional[CallBackMemberType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class LocationECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[State] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[LocationECBNAvailableNumberObjectOwner] = None


class LocationCallInterceptAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[State] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[NumberObjectOwner] = None


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

    def list_locations_webex_calling_details(self, name: str = None, order: str = None, org_id: str = None,
                                             **params) -> Generator[ListLocationObject, None, None]:
        """
        List Locations Webex Calling Details

        Lists Webex Calling locations for an organization with Webex Calling details.

        Searching and viewing locations with Webex Calling details in your
        organization require an administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param name: List locations whose name contains this string.
        :type name: str
        :param order: Sort the list of locations based on `name`, either asc or desc.
        :type order: str
        :param org_id: List locations for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListLocationObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('locations')
        return self.session.follow_pagination(url=url, model=ListLocationObject, item_key='locations', params=params)

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
        body = dict()
        body['id'] = id
        body['name'] = name
        body['timeZone'] = time_zone
        body['preferredLanguage'] = preferred_language
        body['announcementLanguage'] = announcement_language
        body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('locations')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

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
        data = super().get(url, params=params)
        r = GetTelephonyLocationObject.model_validate(data)
        return r

    def update_location_webex_calling_details(self, location_id: str, announcement_language: str,
                                              calling_line_id: GetTelephonyLocationObjectCallingLineId,
                                              connection: GetTelephonyLocationObjectConnection,
                                              external_caller_id_name: str, p_access_network_info: str,
                                              outside_dial_digit: str, routing_prefix: str, charge_number: str,
                                              enforce_outside_dial_digit: bool = None,
                                              org_id: str = None) -> LocationPUTResponse:
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
        :param external_caller_id_name: External caller ID name value. Unicode characters.
        :type external_caller_id_name: str
        :param p_access_network_info: Emergency Location Identifier for a location. The `pAccessNetworkInfo` is set
            only when the location's country is Belgium(`BE`), Germany(`DE`), or France(`FR`).
        :type p_access_network_info: str
        :param outside_dial_digit: Must dial to reach an outside line. Default is none.
        :type outside_dial_digit: str
        :param routing_prefix: Must dial a prefix when calling between locations having same extension within same
            location, should be numeric.
        :type routing_prefix: str
        :param charge_number: Chargeable number for the line placing the call. When this is set, all calls placed from
            this location will include a P-Charge-Info header with the selected number in the SIP INVITE.
        :type charge_number: str
        :param enforce_outside_dial_digit: True when enforcing outside dial digit at location level to make PSTN calls.
        :type enforce_outside_dial_digit: bool
        :param org_id: Updating Webex Calling location attributes for this organization.
        :type org_id: str
        :rtype: :class:`LocationPUTResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['announcementLanguage'] = announcement_language
        body['callingLineId'] = calling_line_id.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['connection'] = connection.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['externalCallerIdName'] = external_caller_id_name
        body['pAccessNetworkInfo'] = p_access_network_info
        body['outsideDialDigit'] = outside_dial_digit
        if enforce_outside_dial_digit is not None:
            body['enforceOutsideDialDigit'] = enforce_outside_dial_digit
        body['routingPrefix'] = routing_prefix
        body['chargeNumber'] = charge_number
        url = self.ep(f'locations/{location_id}')
        data = super().put(url, params=params, json=body)
        r = LocationPUTResponse.model_validate(data)
        return r

    def get_a_list_of_update_routing_prefix_jobs(self, org_id: str = None) -> list[BatchResponse]:
        """
        Get a List of Update Routing Prefix jobs

        Get the list of all update routing prefix jobs in an organization.

        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to retrieve all the update routing prefix jobs in an organization.

        Retrieving the list of update routing prefix jobs in an organization requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of update routing prefix jobs in this organization.
        :type org_id: str
        :rtype: list[BatchResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/updateRoutingPrefix')
        data = super().get(url, params=params)
        r = TypeAdapter(list[BatchResponse]).validate_python(data)
        return r

    def get_the_job_status_of_update_routing_prefix_job(self, job_id: str, org_id: str = None) -> BatchResponse:
        """
        Get the job status of Update Routing Prefix job

        Get the status of the update routing prefix job by its job ID.

        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to check the status of update routing prefix job by job ID in an organization.

        Checking the status of the update routing prefix job in an organization requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check update routing prefix job status in this organization.
        :type org_id: str
        :rtype: :class:`BatchResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/updateRoutingPrefix/{job_id}')
        data = super().get(url, params=params)
        r = BatchResponse.model_validate(data)
        return r

    def get_job_errors_for_update_routing_prefix_job(self, job_id: str, org_id: str = None) -> BatchJobError:
        """
        Get job errors for update routing prefix job

        GET job errors for the update routing prefix job in an organization.

        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to retrieve all the errors of the update routing prefix job by job ID in an organization.

        Retrieving all the errors of the update routing prefix job in an organization requires a full, user, or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for update routing prefix job in this organization.
        :type org_id: str
        :rtype: :class:`BatchJobError`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/updateRoutingPrefix/{job_id}/errors')
        data = super().get(url, params=params)
        r = BatchJobError.model_validate(data)
        return r

    def change_announcement_language(self, location_id: str, announcement_language_code: str,
                                     agent_enabled: bool = None, service_enabled: bool = None, org_id: str = None):
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
        :param announcement_language_code: Language code.
        :type announcement_language_code: str
        :param agent_enabled: Set to `true` to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to `true` to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        body['announcementLanguageCode'] = announcement_language_code
        url = self.ep(f'locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        super().post(url, params=params, json=body)

    def read_the_list_of_dial_patterns(self, dial_plan_id: str, dial_pattern: str = None, order: str = None,
                                       org_id: str = None, **params) -> Generator[str, None, None]:
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
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters.
        Valid wildcard characters are `!` (matches any sequence of digits) and `X` (matches a single digit, 0-9).
        The `!` wildcard can only occur once at the end and only in an E.164 pattern
        :type dial_pattern: str
        :param order: Order the dial patterns according to the designated fields.  Available sort fields:
            `dialPattern`.
        :type order: str
        :param org_id: ID of the organization to which the dial patterns belong.
        :type org_id: str
        :return: Array of dial patterns. An enterprise dial pattern is represented by a sequence of digits (1-9),
            followed by optional wildcard characters.
        """
        if org_id is not None:
            params['orgId'] = org_id
        if dial_pattern is not None:
            params['dialPattern'] = dial_pattern
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        return self.session.follow_pagination(url=url, model=None, item_key='dialPatterns', params=params)

    def get_a_location_emergency_callback_number(self, location_id: str,
                                                 org_id: str = None) -> GetLocationCallBackNumberObject:
        """
        Get a Location Emergency callback number

        Get location emergency callback number.

        * To retrieve location callback number requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Update location attributes for this location.
        :type location_id: str
        :param org_id: Update location attributes for this organization.
        :type org_id: str
        :rtype: :class:`GetLocationCallBackNumberObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/features/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = GetLocationCallBackNumberObject.model_validate(data)
        return r

    def update_a_location_emergency_callback_number(self, location_id: str, selected: CallBackSelected,
                                                    location_member_id: str = None, org_id: str = None):
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
        body = dict()
        body['selected'] = enum_str(selected)
        if location_member_id is not None:
            body['locationMemberId'] = location_member_id
        url = self.ep(f'locations/{location_id}/features/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def validate_the_list_of_extensions(self, extensions: list[str] = None,
                                        org_id: str = None) -> PostValidateExtensionResponse:
        """
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
        body = dict()
        if extensions is not None:
            body['extensions'] = extensions
        url = self.ep('actions/validateExtensions/invoke')
        data = super().post(url, params=params, json=body)
        r = PostValidateExtensionResponse.model_validate(data)
        return r

    def validate_extensions(self, location_id: str, extensions: list[str],
                            org_id: str = None) -> PostValidateExtensionResponse:
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
        :rtype: :class:`PostValidateExtensionResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['extensions'] = extensions
        url = self.ep(f'locations/{location_id}/actions/validateExtensions/invoke')
        data = super().post(url, params=params, json=body)
        r = PostValidateExtensionResponse.model_validate(data)
        return r

    def update_music_on_hold(self, location_id: str, greeting: GetMusicOnHoldObjectGreeting,
                             call_hold_enabled: bool = None, call_park_enabled: bool = None,
                             audio_file: AudioAnnouncementFileGetObject = None, org_id: str = None):
        """
        Update Music On Hold

        Update the location's music on hold settings.

        Location music on hold settings allows you to play music when a call is placed on hold or parked.

        Updating a location's music on hold settings requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param greeting: Greeting type for the location.
        :type greeting: GetMusicOnHoldObjectGreeting
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        :param audio_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_file: AudioAnnouncementFileGetObject
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_hold_enabled is not None:
            body['callHoldEnabled'] = call_hold_enabled
        if call_park_enabled is not None:
            body['callParkEnabled'] = call_park_enabled
        body['greeting'] = enum_str(greeting)
        if audio_file is not None:
            body['audioFile'] = audio_file.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/musicOnHold')
        super().put(url, params=params, json=body)

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
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

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
        data = super().get(url, params=params)
        r = GetPrivateNetworkConnectObjectNetworkConnectionType.model_validate(data['networkConnectionType'])
        return r

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
        body = dict()
        body['networkConnectionType'] = enum_str(network_connection_type)
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        super().put(url, params=params, json=body)

    def read_the_list_of_routing_choices(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                                         org_id: str = None, **params) -> Generator[RouteIdentity, None, None]:
        """
        Read the List of Routing Choices

        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param route_group_name: Return the list of route identities matching the Route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of route identities matching the Trunk name.
        :type trunk_name: str
        :param order: Order the route identities according to the designated fields.  Available sort fields:
            `routeName`, `routeType`.
        :type order: str
        :param org_id: List route identities for this organization.
        :type org_id: str
        :return: Generator yielding :class:`RouteIdentity` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if order is not None:
            params['order'] = order
        url = self.ep('routeChoices')
        return self.session.follow_pagination(url=url, model=RouteIdentity, item_key='routeIdentities', params=params)

    def get_the_list_of_phone_numbers_available_for_external_caller_id(self, location_id: str,
                                                                       phone_number: list[str] = None,
                                                                       owner_name: str = None, person_id: str = None,
                                                                       org_id: str = None,
                                                                       **params) -> Generator[NumberObject, None, None]:
        """
        Get the List of Phone Numbers Available for External Caller ID

        Get the list of phone numbers available for external caller ID usage by a Webex Calling entity (such as a
        person, virtual line, or workspace) within the specified location.
        Numbers from the specified location are returned and cross location numbers are returned as well where the
        number's location has the same country, PSTN provider, and zone (only applicable for India locations) as the
        specified location.
        When `personId` is specified, and the person belongs to a cisco PSTN location, has a mobile number assigned as
        primary DN, and does not have a billing plan, only the assigned mobile number is returned as the available
        number for caller ID.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve available external caller ID numbers for this location.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the provided list in the `phoneNumber` array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param person_id: Retrieve available external caller ID numbers for this person. If `personId` is not provided
            it may result in the unsuccessful assignment of the returned number. This parameter has no effect when
            workspace or virtual line ID is used.
        :type person_id: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`NumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep(f'locations/{location_id}/externalCallerId/availableNumbers')
        return self.session.follow_pagination(url=url, model=NumberObject, item_key='phoneNumbers', params=params)

    def get_available_phone_numbers_for_a_location_with_given_criteria(self, location_id: str,
                                                                       phone_number: list[str] = None,
                                                                       owner_name: str = None, org_id: str = None,
                                                                       **params) -> Generator[LocationAvailableNumberObject, None, None]:
        """
        Get Available Phone Numbers for a Location with Given Criteria

        List the service and standard PSTN numbers that are available to be assigned as the location's main number.
        These numbers are associated with the location specified in the request URL and can be active/inactive and
        assigned to an owning entity or unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`LocationAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'locations/{location_id}/availableNumbers')
        return self.session.follow_pagination(url=url, model=LocationAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_webex_go_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                             org_id: str = None,
                                             **params) -> Generator[WebexGoAvailableNumberObject, None, None]:
        """
        Get Webex Go Available Phone Numbers

        List standard numbers that are available to be assigned as the webex go phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WebexGoAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/webexGo/availableNumbers')
        return self.session.follow_pagination(url=url, model=WebexGoAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_location_ecbn_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                  owner_name: str = None, org_id: str = None,
                                                  **params) -> Generator[LocationECBNAvailableNumberObject, None, None]:
        """
        Get Location ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as the location's emergency callback number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`LocationECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'locations/{location_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=LocationECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_location_call_intercept_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                            owner_name: str = None, extension: str = None,
                                                            org_id: str = None,
                                                            **params) -> Generator[LocationCallInterceptAvailableNumberObject, None, None]:
        """
        Get Location Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the location's call intercept
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`LocationCallInterceptAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'locations/{location_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=LocationCallInterceptAvailableNumberObject, item_key='phoneNumbers', params=params)
