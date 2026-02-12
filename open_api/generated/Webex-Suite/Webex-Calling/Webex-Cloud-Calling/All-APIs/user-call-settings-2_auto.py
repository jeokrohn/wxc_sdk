from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AccessLevel', 'Action', 'AgentCallerIdType', 'ApplicationPutSharedLineMemberItem', 'ApplicationsSetting',
           'Assistant', 'AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
           'AudioAnnouncementFileGetObjectMediaFileType', 'AuthorizationCode', 'AuthorizationCodeLevel',
           'AvailableAssistant', 'AvailableCallerIdObject', 'AvailableSharedLineMemberItem', 'CallsFrom',
           'CallsFromSelectiveAccept', 'CallsFromSelectiveReject', 'CountObject', 'Criteria', 'CriteriaAccept',
           'CriteriaForward', 'DeviceType', 'EndpointInformation', 'Endpoints', 'ErrorMessageObject', 'ErrorObject',
           'ErrorOrImpactItem', 'ExceptionTypeObject', 'Executive', 'ExecutiveAlertGet',
           'ExecutiveAlertGetAlertingMode', 'ExecutiveAlertGetClidNameMode', 'ExecutiveAlertGetClidPhoneNumberMode',
           'ExecutiveAlertGetRolloverAction', 'ExecutiveAssistantSettingsGet', 'ExecutiveCallFilteringCriteriaGet',
           'ExecutiveCallFilteringCriteriaGetCallsToNumbersItem',
           'ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType', 'ExecutiveCallFilteringGet',
           'ExecutiveCallFilteringGetCriteriaItem', 'ExecutiveCallFilteringGetFilterType',
           'ExecutiveCallFilteringPatchCriteriaActivationItem', 'ExecutivePut', 'ExecutiveScreeningGet',
           'ExecutiveScreeningGetAlertType', 'GetMessageSummaryResponse', 'GetMusicOnHoldObject',
           'GetMusicOnHoldObjectGreeting', 'GetSharedLineMemberItem', 'GetSharedLineMemberList',
           'GetUserCallCaptionsObject', 'GetUserMSTeamsSettingsObject', 'ItemObject', 'JobDetailsResponse',
           'JobDetailsResponseById', 'JobDetailsResponseLatestExecutionExitCode',
           'JobDetailsResponseLatestExecutionStatus', 'JobExecutionStatusObject', 'LicenseType', 'LineType',
           'Location', 'ModeManagementFeatureTypeObject', 'ModifyUserMSTeamsSettingsObjectSettingName',
           'NumberOwnerType', 'PersonCallForwardAvailableNumberObject', 'PersonCallForwardAvailableNumberObjectOwner',
           'PersonECBNAvailableNumberObject', 'PersonECBNAvailableNumberObjectOwner',
           'PersonECBNAvailableNumberObjectOwnerType', 'PersonPrimaryAvailableNumberObject',
           'PersonPrimaryAvailableNumberObjectTelephonyType', 'PersonSecondaryAvailableNumberObject',
           'PersonalAssistantGet', 'PersonalAssistantGetAlerting', 'PersonalAssistantGetPresence', 'PhoneNumber',
           'PutSharedLineMemberItem', 'RingPattern', 'STATE', 'ScheduleLevel', 'ScheduleType',
           'SelectiveAcceptCallCriteriaGet', 'SelectiveAcceptCallGet', 'SelectiveForwardCallCriteriaGet',
           'SelectiveForwardCallGet', 'SelectiveRejectCallCriteriaGet', 'SelectiveRejectCallGet', 'SettingsObject',
           'SettingsObjectLevel', 'SettingsObjectSettingName', 'Source', 'SourceSelectiveAccept',
           'StepExecutionStatusesObject', 'TelephonyType', 'TransferNumberGet', 'UserCallSettings22Api',
           'UserDigitPatternObject', 'UserItem', 'UserListItem', 'UserModeManagementAvailableFeaturesObject',
           'UserModeManagementFeatureObject', 'UserOutgoingPermissionDigitPatternGetListObject',
           'UserOutgoingPermissionDigitPatternPostObjectAction', 'UserPlaceAuthorizationCodeListGet',
           'UserSettingsPermissionsGet', 'UserSettingsPermissionsGetDefault', 'UserType', 'UsersListItem',
           'VoiceMailPartyInformation', 'VoiceMessageDetails']


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class AuthorizationCodeLevel(str, Enum):
    #: The location level access code.
    location = 'LOCATION'
    #: The user level access code.
    custom = 'CUSTOM'


class AuthorizationCode(ApiModel):
    #: An access code.
    code: Optional[str] = None
    #: The description of the access code.
    description: Optional[str] = None
    #: The level of each access code.
    level: Optional[AuthorizationCodeLevel] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class Location(ApiModel):
    #: Location identifier associated with the members.
    id: Optional[str] = None
    #: Location name associated with the member.
    name: Optional[str] = None


class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    id: Optional[str] = None
    #: First name of member.
    first_name: Optional[str] = None
    #: Last name of member.
    last_name: Optional[str] = None
    #: Phone number of member. Currently, E.164 format is not supported.
    phone_number: Optional[str] = None
    #: Phone extension of member.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: If the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class DeviceType(str, Enum):
    #: The endpoint is a device.
    device = 'DEVICE'
    #: The endpoint is a application.
    application = 'APPLICATION'


class UserType(str, Enum):
    #: The associated member is a person.
    people = 'PEOPLE'
    #: The associated member is a workspace.
    place = 'PLACE'
    #: The associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetSharedLineMemberItem(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str] = None
    #: First name of person or workspace.
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    last_name: Optional[str] = None
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the
    #: future update.
    phone_number: Optional[str] = None
    #: Phone extension of a person or workspace.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Device port number assigned to a person or workspace.
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    primary_owner: Optional[str] = None
    #: If the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int] = None
    #: Registration home IP for the line port.
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP for the line port.
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    hotline_destination: Optional[str] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    line_label: Optional[str] = None
    #: If the member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[UserType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class GetSharedLineMemberList(ApiModel):
    #: Model name of device.
    model: Optional[str] = None
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]] = None
    #: Maximum number of device ports.
    max_line_count: Optional[int] = None


class RingPattern(str, Enum):
    #: Normal ring pattern.
    normal = 'NORMAL'
    #: Long ring pattern.
    long_long = 'LONG_LONG'
    #: Short and short ring pattern.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Short and long ring pattern.
    short_long_short = 'SHORT_LONG_SHORT'


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern] = None


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    id: Optional[str] = None
    #: Device port number assigned to person or workspace.
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    primary_owner: Optional[str] = None
    #: If the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int] = None
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in `hotlineDestination`.
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    hotline_destination: Optional[str] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    line_label: Optional[str] = None


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`, and
    #: `user@company.domain`.
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str] = None
    #: if `true`, denotes privacy is enabled for the name, number and `personId`/`placeId`.
    privacy_enabled: Optional[bool] = None


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str] = None
    #: The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    duration: Optional[int] = None
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation] = None
    #: `true` if the voicemail message is urgent.
    urgent: Optional[bool] = None
    #: `true` if the voicemail message is confidential.
    confidential: Optional[bool] = None
    #: `true` if the voicemail message has been read.
    read: Optional[bool] = None
    #: Number of pages for the FAX.  Only set for a FAX.
    fax_page_count: Optional[int] = None
    #: The date and time the voicemail message was created.
    created: Optional[datetime] = None


class Endpoints(ApiModel):
    #: Unique identifier for the endpoint.
    id: Optional[str] = None
    #: Enumeration that indicates if the endpoint is of type `DEVICE` or `APPLICATION`.
    type: Optional[DeviceType] = None
    #: The `name` field in the response is calculated using device tag. Admins have the ability to set tags for
    #: devices. If a `name=<value>` tag is set, for example “name=home phone“, then the `<value>` is included in the
    #: `name` field of the API response. In this example “home phone”.
    name: Optional[str] = None


class EndpointInformation(ApiModel):
    #: Person’s preferred answer endpoint.
    preferred_answer_endpoint_id: Optional[str] = None
    #: Array of endpoints available to the person.
    endpoints: Optional[list[Endpoints]] = None


class CountObject(ApiModel):
    #: Total number of user moves requested.
    total_moves: Optional[int] = None
    #: Total number of user moves completed successfully.
    moved: Optional[int] = None
    #: Total number of user moves that were completed with failures.
    failed: Optional[int] = None
    #: Total number of user moves that were pending with number orders.
    pending: Optional[int] = None
    #: Total number of user moves that were skipped.
    skipped: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location ID in which the error occurs. For a move operation, this is the target
    #: location ID.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ErrorOrImpactItem(ApiModel):
    #: Error or Impact code.
    code: Optional[int] = None
    #: Message string with more error or impact information.
    message: Optional[str] = None


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[ErrorObject] = None


class JobDetailsResponseLatestExecutionStatus(str, Enum):
    #: Job has started.
    starting = 'STARTING'
    #: Job is in progress.
    started = 'STARTED'
    #: Job has completed.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'
    #: Job status is unknown.
    unknown = 'UNKNOWN'
    #: Job has been abandoned (manually stopped).
    abandoned = 'ABANDONED'


class JobDetailsResponseLatestExecutionExitCode(str, Enum):
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
    #: Job has completed with pending number orders.
    completed_with_pending_orders = 'COMPLETED_WITH_PENDING_ORDERS'


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: The date and time with seconds, the step execution has started in UTC format.
    start_time: Optional[datetime] = None
    #: The date and time with seconds, the step execution has ended in UTC format.
    end_time: Optional[datetime] = None
    #: The date and time with seconds, the step has last updated in UTC format.
    last_updated: Optional[datetime] = None
    #: Displays status for a step.
    status_message: Optional[JobDetailsResponseLatestExecutionStatus] = None
    #: Exit Code for a step.
    exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: The date and time with seconds, the job has started in UTC format.
    start_time: Optional[datetime] = None
    #: The date and time with seconds, the job has ended in UTC format.
    end_time: Optional[datetime] = None
    #: The date and time with seconds, the job has last updated in UTC format post one of the step execution
    #: completion.
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[JobDetailsResponseLatestExecutionStatus] = None
    #: Exit Code for a job.
    exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: The date and time with seconds, the job has created in UTC format.
    created_time: Optional[datetime] = None
    #: Time lapsed in seconds since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class JobDetailsResponse(ApiModel):
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
    #: Most recent status of the job at the time of invocation.
    latest_execution_status: Optional[JobDetailsResponseLatestExecutionStatus] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csv_file: Optional[str] = None
    #: Date and time with seconds, the file expires in UTC format.
    csv_file_expiry_time: Optional[datetime] = None
    #: Format of the file generated.
    file_format: Optional[str] = None


class JobDetailsResponseById(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: d060-4164-9757-48b383423d73` (string, required) - Unique identifier to track the flow of HTTP requests.
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
    #: Most recent status of the job at the time of invocation.
    latest_execution_status: Optional[JobDetailsResponseLatestExecutionStatus] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[JobDetailsResponseLatestExecutionExitCode] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csv_file: Optional[str] = None
    #: Date and time with seconds, the file expires in UTC format.
    csv_file_expiry_time: Optional[datetime] = None
    #: Format of the file generated.
    file_format: Optional[str] = None
    #: URL to the CSV file containing errors and impacts.
    csv_file_download_url: Optional[str] = None


class UserItem(ApiModel):
    #: User ID to be moved.
    user_id: Optional[str] = None
    #: Extension to be moved. Extension is only supported for calling user. Only one new extension can be moved to the
    #: target location for a user. An empty value will remove the configured extension. If not provided, the existing
    #: extension will be retained.
    extension: Optional[str] = None
    #: Phone number to be moved. Phone number is only supported for calling user. Only one new phone number belonging
    #: to the target location can be assigned to a user. The phone number must follow the E.164 format. An empty value
    #: will remove the configured phone number. If not provided, the existing phone number will be moved to the target
    #: location.
    phone_number: Optional[str] = None


class UsersListItem(ApiModel):
    #: Target location for the user moves.
    location_id: Optional[str] = None
    #: Set to `true` to validate the user move; this option is not supported for multiple users. Set to `false` to
    #: perform the user move.
    validate: Optional[bool] = None
    #: List of users to be moved.
    users: Optional[list[UserItem]] = None


class UserListItem(ApiModel):
    #: User ID associated with the validation response.
    user_id: Optional[str] = None
    #: List of impacts for the user moves.
    impacts: Optional[list[ErrorOrImpactItem]] = None
    #: List of errors for the user moves.
    errors: Optional[list[ErrorOrImpactItem]] = None


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across the organization.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across the location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    id: Optional[str] = None
    #: Audio announcement file name.
    file_name: Optional[str] = None
    #: Audio announcement file type.
    media_file_type: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file location.
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class GetMusicOnHoldObjectGreeting(str, Enum):
    #: Play music configured at location level.
    default = 'DEFAULT'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class GetMusicOnHoldObject(ApiModel):
    #: Music on hold enabled or disabled for the person.
    moh_enabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location. The music on hold setting returned in the response is used
    #: only when music on hold is enabled at the location level. When `mohLocationEnabled` is false and `mohEnabled`
    #: is true, music on hold is disabled for the user. When `mohLocationEnabled` is true and `mohEnabled` is false,
    #: music on hold is turned off for the user. In both cases, music on hold will not be played.
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the person.
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class AgentCallerIdType(str, Enum):
    #: A call queue has been selected for the agent's caller ID.
    call_queue = 'CALL_QUEUE'
    #: A hunt group has been selected for the agent's caller ID.
    hunt_group = 'HUNT_GROUP'


class AvailableCallerIdObject(ApiModel):
    #: Call queue or hunt group's unique identifier.
    id: Optional[str] = None
    #: Member is of type `CALL_QUEUE` or `HUNT_GROUP`
    type: Optional[AgentCallerIdType] = None
    #: Call queue or hunt group's name.
    name: Optional[str] = None
    #: When not null, it is call queue or hunt group's phone number.
    phone_number: Optional[str] = None
    #: When not null, it is call queue or hunt group's extension number.
    extension: Optional[str] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class PersonSecondaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


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
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class PersonCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    display_name: Optional[str] = None


class PersonCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    extension: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None
    owner: Optional[PersonCallForwardAvailableNumberObjectOwner] = None


class PersonPrimaryAvailableNumberObjectTelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: The object is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class PersonPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[PersonPrimaryAvailableNumberObjectTelephonyType] = None
    #: Mobile Network for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    routing_profile: Optional[str] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


class PersonECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Line.
    virtual_line = 'VIRTUAL_LINE'
    #: Phone number's owner is a Hunt Group.
    hunt_group = 'HUNT_GROUP'


class PersonECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which phone number is assigned.
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    type: Optional[PersonECBNAvailableNumberObjectOwnerType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE` or
    #: `HUNT_GROUP`.
    display_name: Optional[str] = None


class PersonECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None
    owner: Optional[PersonECBNAvailableNumberObjectOwner] = None


class SettingsObjectSettingName(str, Enum):
    #: Webex will continue to run but its windows will be closed by default. Users can still access Webex from the
    #: system tray on Windows or the Menu Bar on Mac.
    hide_webex_app = 'HIDE_WEBEX_APP'
    #: Sync presence status between Microsoft Teams and Webex.
    presence_sync = 'PRESENCE_SYNC'


class SettingsObjectLevel(str, Enum):
    #: `settingName` configured at the `GLOBAL` `level`.
    global_ = 'GLOBAL'
    #: `settingName` configured at the `ORGANIZATION` `level`.
    organization = 'ORGANIZATION'
    #: `settingName` configured at the `GROUP` `level`.
    group = 'GROUP'
    #: `settingName` configured at the `PEOPLE` `level`.
    people = 'PEOPLE'


class SettingsObject(ApiModel):
    #: Name of the setting retrieved.
    setting_name: Optional[SettingsObjectSettingName] = None
    #: Level at which the `settingName` has been set.
    level: Optional[SettingsObjectLevel] = None
    #: Either `true` or `false` for the respective `settingName` to be retrieved.
    value: Optional[bool] = None
    #: The date and time when the respective `settingName` was last updated.
    last_modified: Optional[datetime] = None


class GetUserMSTeamsSettingsObject(ApiModel):
    #: Unique identifier for the person.
    person_id: Optional[str] = None
    #: Unique identifier for the organization in which the person resides.
    org_id: Optional[str] = None
    #: Array of `SettingsObject`.
    settings: Optional[list[SettingsObject]] = None


class ModifyUserMSTeamsSettingsObjectSettingName(str, Enum):
    #: Webex will continue to run but its windows will be closed by default. Users can still access Webex from the
    #: system tray on Windows or the Menu Bar on Mac.
    hide_webex_app = 'HIDE_WEBEX_APP'


class UserPlaceAuthorizationCodeListGet(ApiModel):
    #: When `true`, use custom settings for the access codes category of outgoing call permissions.
    use_custom_access_codes: Optional[bool] = None
    #: The set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]] = None


class UserOutgoingPermissionDigitPatternPostObjectAction(str, Enum):
    #: Allow the designated call type.
    allow = 'ALLOW'
    #: Block the designated call type.
    block = 'BLOCK'
    #: Allow only via Authorization Code.
    auth_code = 'AUTH_CODE'
    #: Transfer to Auto Transfer Number 1. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class UserDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches the digit pattern.
    action: Optional[UserOutgoingPermissionDigitPatternPostObjectAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class UserOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[UserDigitPatternObject]] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outgoing call permissions.
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this person will be automatically transferred to another number.
    #: `autoTransferNumber1` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_1`.
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this person will be automatically transferred to another number.
    #: `autoTransferNumber2` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_2`.
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this person will be automatically transferred to another number.
    #: `autoTransferNumber3` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_3`.
    auto_transfer_number3: Optional[str] = None


class PersonalAssistantGetPresence(str, Enum):
    #: User is available.
    none_ = 'NONE'
    #: User is gone for a business trip.
    business_trip = 'BUSINESS_TRIP'
    #: User is gone for the day.
    gone_for_the_day = 'GONE_FOR_THE_DAY'
    #: User is gone for lunch.
    lunch = 'LUNCH'
    #: User is gone for a meeting.
    meeting = 'MEETING'
    #: User is out of office.
    out_of_office = 'OUT_OF_OFFICE'
    #: User is temporarily out.
    temporarily_out = 'TEMPORARILY_OUT'
    #: User is gone for training.
    training = 'TRAINING'
    #: User is unavailable.
    unavailable = 'UNAVAILABLE'
    #: User is gone for vacation.
    vacation = 'VACATION'


class PersonalAssistantGetAlerting(str, Enum):
    #: Ring the recipient first.
    alert_me_first = 'ALERT_ME_FIRST'
    #: Reminder ring the recipient.
    play_ring_reminder = 'PLAY_RING_REMINDER'
    #: No alert.
    none_ = 'NONE'


class PersonalAssistantGet(ApiModel):
    #: Toggles feature.
    enabled: Optional[bool] = None
    #: Person's availability.
    presence: Optional[PersonalAssistantGetPresence] = None
    #: The date until which personal assistant is active.
    until_date_time: Optional[datetime] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Number to transfer to.
    transfer_number: Optional[str] = None
    #: Alert type.
    alerting: Optional[PersonalAssistantGetAlerting] = None
    #: Number of rings for alert type: `ALERT_ME_FIRST`; available range is 2-20
    alert_me_first_number_of_rings: Optional[int] = None


class ModeManagementFeatureTypeObject(str, Enum):
    #: Specifies the feature is an Auto Attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: Specifies the feature is a Call Queue.
    call_queue = 'CALL_QUEUE'
    #: Specifies the feature is a Hunt Group.
    hunt_group = 'HUNT_GROUP'


class UserModeManagementAvailableFeaturesObject(ApiModel):
    #: A unique identifier for the feature.
    id: Optional[str] = None
    #: Unique name for the feature.
    name: Optional[str] = None
    #: Defines the scheduling of the operating mode.
    type: Optional[ModeManagementFeatureTypeObject] = None
    #: The primary phone number configured for the feature.
    phone_number: Optional[str] = None
    #: The extension configured for the feature.
    extension: Optional[str] = None


class ExceptionTypeObject(str, Enum):
    #: The mode was switched to or extended by the user for manual switch back and runs as an exception until the user
    #: manually switches the feature back to normal operation or a different mode.
    manual_switch_back = 'MANUAL_SWITCH_BACK'
    #: The mode was switched to by the user before its start time and runs as an exception until its end time is
    #: reached, at which point it automatically switches the feature back to normal operation.
    automatic_switch_back_early_start = 'AUTOMATIC_SWITCH_BACK_EARLY_START'
    #: The current mode was extended by the user before its end time and runs as an exception until the extension end
    #: time (mode's end time + extension of up to 12 hours) is reached, at which point it automatically switches the
    #: feature back to normal operation.
    automatic_switch_back_extension = 'AUTOMATIC_SWITCH_BACK_EXTENSION'
    #: The mode will remain the current operating mode for the feature until its normal end time is reached.
    automatic_switch_back_standard = 'AUTOMATIC_SWITCH_BACK_STANDARD'


class UserModeManagementFeatureObject(ApiModel):
    #: A unique identifier for the feature.
    id: Optional[str] = None
    #: Unique name for the feature.
    name: Optional[str] = None
    #: Defines the scheduling of the operating mode.
    type: Optional[ModeManagementFeatureTypeObject] = None
    #: The primary phone number configured for the feature.
    phone_number: Optional[str] = None
    #: The extension configured for the feature.
    extension: Optional[str] = None
    #: A flag to indicate whether mode-based call forwarding is enabled for the feature.
    mode_based_forwarding_enabled: Optional[bool] = None
    #: The destination for call forwarding if mode-based call forwarding is enabled.
    forward_destination: Optional[str] = None
    #: Name of the current operating mode.
    current_operating_mode_name: Optional[str] = None
    #: Unique identifier for the current operating mode.
    current_operating_mode_id: Optional[str] = None
    #: Defines the exception through which the current operating mode is set as active for the feature.
    exception_type: Optional[ExceptionTypeObject] = None
    #: Location object that has a unique identifier for the location and its name.
    location: Optional[Location] = None


class ScheduleType(str, Enum):
    #: The schedule type that specifies the business or working hours during the day.
    business_hours = 'businessHours'
    #: The schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class ScheduleLevel(str, Enum):
    #: The schedule level that specifies that criteria is of People level.
    people = 'PEOPLE'
    #: The schedule level that specifies that criteria is of Group level.
    group = 'GROUP'


class Source(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Criteria applies only for forwarded numbers.
    forwarded = 'FORWARDED'


class SourceSelectiveAccept(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class CallsFrom(str, Enum):
    #: Criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Criteria only apply for forwarded incoming numbers.
    forwarded = 'FORWARDED'


class CallsFromSelectiveAccept(str, Enum):
    #: Criteria applies for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria applies for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'


class CallsFromSelectiveReject(str, Enum):
    #: Criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Criteria only apply for any internal incoming numbers.
    any_internal = 'ANY_INTERNAL'
    #: Criteria only apply for any external incoming numbers.
    any_external = 'ANY_EXTERNAL'


class Criteria(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Name of the schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: Indicates the sources for which selective call rejection is applied.
    source: Optional[Source] = None
    #: Boolean field to indicate whether selective reject is enabled or not
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallGet(ApiModel):
    #: Boolean to indicate whether Selective reject are enabled or not.
    enabled: Optional[bool] = None
    #: Ordered list of criteria that will be evaluated for rejecting the call.
    criteria: Optional[list[Criteria]] = None


class CriteriaAccept(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Name of the schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: Denotes if the criteria is set for `ALL_NUMBERS`, or `SELECT_PHONE_NUMBERS`.
    source: Optional[SourceSelectiveAccept] = None
    #: Boolean field to indicate whether selective call accept is enabled or not.
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallGet(ApiModel):
    #: Boolean to indicate whether selective accept is enabled or not.
    enabled: Optional[bool] = None
    #: Ordered list of criteria that will be evaluated for accepting the call.
    criteria: Optional[list[CriteriaAccept]] = None


class CriteriaForward(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Name of the Schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: Indicates the sources for which selective call forward is applied.
    source: Optional[Source] = None
    #: Boolean flag to enable/disable selective call forward.
    forward_enabled: Optional[bool] = None


class SelectiveAcceptCallCriteriaGet(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Name of the Schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: Schedule Type.
    schedule_type: Optional[ScheduleType] = None
    #: Schedule Level of the criteria.
    schedule_level: Optional[ScheduleLevel] = None
    #: Accept calls selection.
    calls_from: Optional[CallsFromSelectiveAccept] = None
    #: Boolean flag indicating if calls from custom numbers, private numbers are enabled.
    anonymous_callers_enabled: Optional[bool] = None
    #: Boolean flag indicating if calls from custom numbers, unavailable numbers are enabled.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers. It does not include extensions. In some regions phone numbers are not returned in E.164
    #: format. This will be supported in a future update.
    phone_numbers: Optional[list[str]] = None
    #: Boolean flag indicating if selective call accept is enabled.
    accept_enabled: Optional[bool] = None


class SelectiveRejectCallCriteriaGet(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Name of the schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: The schedule type.
    schedule_type: Optional[ScheduleType] = None
    #: The schedule level of the criteria.
    schedule_level: Optional[ScheduleLevel] = None
    #: Reject calls selection.
    calls_from: Optional[CallsFrom] = None
    #: Boolean flag indicating if calls from custom numbers, private numbers are enabled.
    anonymous_callers_enabled: Optional[bool] = None
    #: Boolean flag indicating if calls from custom numbers, unavailable numbers are enabled.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers. It does not include extensions. In some regions phone numbers are not returned in E.164
    #: format. This will be supported in a future update.
    phone_numbers: Optional[list[str]] = None
    #: Boolean flag to enable/disable rejection.
    reject_enabled: Optional[bool] = None


class SelectiveForwardCallGet(ApiModel):
    #: Boolean to indicate whether Selective forward are enabled or not.
    enabled: Optional[bool] = None
    #: Number to which calls needs to be forwarded
    default_phone_number_to_forward: Optional[str] = None
    #: Boolean flag indicating whether ring reminder is enabled or not.
    ring_reminder_enabled: Optional[bool] = None
    #: Boolean flag to enable/disable sending calls to voicemail.
    send_to_voicemail_enabled: Optional[bool] = None
    #: : Ordered list of criteria that will be evaluated for forwarding the call.
    criteria: Optional[list[CriteriaForward]] = None


class SelectiveForwardCallCriteriaGet(ApiModel):
    #: Criteria ID.
    id: Optional[str] = None
    #: Number to which calls needs to be forwarded.
    forward_to_phone_number: Optional[str] = None
    #: Boolean flag to enable/disable sending calls to voicemail.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Name of the schedule to which the criteria is created.
    schedule_name: Optional[str] = None
    #: The type of schedule.
    schedule_type: Optional[ScheduleType] = None
    #: Schedule level of the criteria.
    schedule_level: Optional[ScheduleLevel] = None
    #: Reject calls selection.
    calls_from: Optional[CallsFromSelectiveReject] = None
    #: Calls From custom numbers, private number enabled.
    anonymous_callers_enabled: Optional[bool] = None
    #: Calls From custom numbers, unavailable number enabled.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers. It does not include extensions. In some regions phone numbers are not returned in E.164
    #: format. This will be supported in a future update.
    phone_numbers: Optional[list[str]] = None
    #: Boolean flag to enable/disable selective call forward.
    forward_enabled: Optional[bool] = None


class AccessLevel(str, Enum):
    #: User has full access.
    full_access = 'FULL_ACCESS'
    #: User does not have access.
    no_access = 'NO_ACCESS'


class UserSettingsPermissionsGetDefault(ApiModel):
    #: Set whether end users have access to make changes to their `Anonymous call rejection` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    anonymous_call_rejection: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Barge In` feature via User Hub, or other clients
    #: (Webex, IP phone, etc.).
    barge_in: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Block caller ID` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    block_caller_id: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Call forwarding` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    call_forwarding: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Call waiting` feature via User Hub, or other clients
    #: (Webex, IP phone, etc.).
    call_waiting: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Call notify` feature via User Hub, or other clients
    #: (Webex, IP phone, etc.).
    call_notify: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Connected line identity` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    connected_line_identity: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Executive/Executive assistant` feature via User Hub,
    #: or other clients (Webex, IP phone, etc.).
    executive: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Hoteling` feature via User Hub, or other clients
    #: (Webex, IP phone, etc.).
    hoteling: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Priority alert` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    priority_alert: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively accept calls` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_accept_calls: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively reject calls` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_reject_calls: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Selectively forward calls` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    selectively_forward_calls: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Sequential ring` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    sequential_ring: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Simultaneous ring` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    simultaneous_ring: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Single number reach` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    single_number_reach: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Voicemail feature` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Send calls to voicemail` feature via User Hub, or
    #: other clients (Webex, IP phone, etc.).
    send_calls_to_voicemail: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Email a copy of the voicemail message` feature via
    #: User Hub, or other clients (Webex, IP phone, etc.).
    voicemail_email_copy: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Fax messaging` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail_fax_messaging: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Message storage` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail_message_storage: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Notifications` feature via User Hub, or other
    #: clients (Webex, IP phone, etc.).
    voicemail_notifications: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Transfer on '0' to another number.` feature via User
    #: Hub, or other clients (Webex, IP phone, etc.).
    voicemail_transfer_number: Optional[AccessLevel] = None
    #: Set whether end users have access to make changes to their `Allow End User to Generate Activation Codes & Delete
    #: their Phones` feature via User Hub, or other clients (Webex, IP phone, etc.).
    generate_activation_code: Optional[AccessLevel] = None
    #: Set whether end users have access to download voicemail via User Hub, or other clients (Webex, etc.).
    voicemail_download: Optional[AccessLevel] = None


class UserSettingsPermissionsGet(ApiModel):
    #: Set whether end users have organization's settings enabled for the user.
    user_org_settings_permission_enabled: Optional[bool] = None
    user_org_settings_permissions: Optional[UserSettingsPermissionsGetDefault] = None


class ApplicationPutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    id: Optional[str] = None
    #: Device port number assigned to person or workspace.
    port: Optional[int] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    primary_owner: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    line_label: Optional[str] = None


class ApplicationsSetting(ApiModel):
    #: When `true`, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool] = None
    #: When `true`, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool] = None
    #: Indicates that the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool] = None
    #: Device ID of WebRTC client. Returns only if `browserClientEnabled` is true.
    browser_client_id: Optional[str] = None
    #: Indicates that the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool] = None
    #: Device ID of Desktop client. Returns only if `desktopClientEnabled` is true.
    desktop_client_id: Optional[str] = None
    #: Indicates that the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool] = None
    #: Device ID of Tablet client. Returns only if `tabletClientEnabled` is true.
    tablet_client_id: Optional[str] = None
    #: Indicates that the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool] = None
    #: Device ID of Mobile client. Returns only if `mobileClientEnabled` is true.
    mobile_client_id: Optional[str] = None
    #: Number of available device licenses for assigning devices/apps.
    available_line_count: Optional[int] = None


class GetUserCallCaptionsObject(ApiModel):
    #: User-level closed captions are enabled or disabled.
    user_closed_captions_enabled: Optional[bool] = None
    #: User-level transcripts are enabled or disabled.
    user_transcripts_enabled: Optional[bool] = None
    #: Location closed captions are enabled or disabled. If `useOrgSettingsEnabled` is `true`, these are
    #: organization-level settings. Otherwise, location-level settings are used.
    location_closed_captions_enabled: Optional[bool] = None
    #: Location transcripts are enabled or disabled. If `useOrgSettingsEnabled` is `true`, these are organization-level
    #: settings. Otherwise, location-level settings are used.
    location_transcripts_enabled: Optional[bool] = None
    #: If `useLocationSettingsEnabled` is `true`, location settings will control the user's closed captions and
    #: transcripts. Otherwise, user-level settings are used.
    use_location_settings_enabled: Optional[bool] = None


class ExecutiveCallFilteringGetFilterType(str, Enum):
    #: Choose this option to ensure that only specific calls are sent to the executive assistant.
    custom_call_filters = 'CUSTOM_CALL_FILTERS'
    #: Choose this option to send both internal and external calls to the executive assistant.
    all_calls = 'ALL_CALLS'
    #: Choose this option to send all internal calls to the executive assistant.
    all_internal_calls = 'ALL_INTERNAL_CALLS'
    #: Choose this option to send all external calls to the executive assistant.
    all_external_calls = 'ALL_EXTERNAL_CALLS'


class ExecutiveCallFilteringGetCriteriaItem(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    #: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
    source: Optional[CallsFromSelectiveReject] = None
    #: Controls whether this filter criteria is active. When `true`, the criteria is evaluated for incoming calls. When
    #: `false`, the criteria is completely ignored and has no effect on call filtering.
    activation_enabled: Optional[bool] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered and will alert
    #: the executive's assistants. When `false`, matching calls are not filtered and will not alert the executive's
    #: assistants. Criteria with `filterEnabled` as `false` take precedence over other filtering criteria with
    #: `filterEnabled` as `true`, allowing exceptions where certain calls are not filtered to the executive's
    #: assistants.
    filter_enabled: Optional[bool] = None


class ExecutiveCallFilteringGet(ApiModel):
    #: Indicates whether executive call filtering is enabled.
    enabled: Optional[bool] = None
    #: * `CUSTOM_CALL_FILTERS` - Choose this option to ensure that only specific calls are sent to the executive
    #: assistant.
    filter_type: Optional[ExecutiveCallFilteringGetFilterType] = None
    #: The list of call filtering criteria configured for executive call filtering.
    criteria: Optional[list[ExecutiveCallFilteringGetCriteriaItem]] = None


class ExecutiveCallFilteringPatchCriteriaActivationItem(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Controls whether this filter criteria is active. When `true`, the criteria is evaluated for incoming calls. When
    #: `false`, the criteria is completely ignored and has no effect on call filtering.
    activation_enabled: Optional[bool] = None


class ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType(str, Enum):
    #: Number is assigned as primary to executive.
    primary = 'PRIMARY'
    #: Number is assigned as alternate (secondary) to the executive.
    alternate = 'ALTERNATE'


class ExecutiveCallFilteringCriteriaGetCallsToNumbersItem(ApiModel):
    #: * `PRIMARY` - Number is assigned as primary to executive.
    type: Optional[ExecutiveCallFilteringCriteriaGetCallsToNumbersItemType] = None
    #: The phone number assigned to the executive that will be used to match criteria.
    phone_number: Optional[str] = None


class ExecutiveCallFilteringCriteriaGet(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    #: Name of the schedule associated with this criteria.
    schedule_name: Optional[str] = None
    #: * `businessHours` - The schedule type that specifies the business or working hours during the day.
    schedule_type: Optional[ScheduleType] = None
    #: * `PEOPLE` - The schedule level that specifies that criteria is of People level.
    schedule_level: Optional[ScheduleLevel] = None
    #: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
    calls_from: Optional[CallsFromSelectiveReject] = None
    #: Indicates if the criteria applies to anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: Indicates if the criteria applies to unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: The list of phone numbers that this filtering criteria applies to, when `callsFrom` is set to
    #: `SELECT_PHONE_NUMBERS`.
    phone_numbers: Optional[list[str]] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered and will alert
    #: the executive's assistants. When `false`, matching calls are not filtered and will not alert the executive's
    #: assistants. Criteria with `filterEnabled` as `false` take precedence over other filtering criteria with
    #: `filterEnabled` as `true`, allowing exceptions where certain calls are not filtered to the executive's
    #: assistants.
    filter_enabled: Optional[bool] = None
    #: List of numbers for the executive that will match the criteria when called. This may include the executive’s
    #: primary number and/or extension, as well as secondary (alternate) numbers (and associated extensions). If the
    #: list is empty, any number or extension for the executive matches the criteria when called. If the list is not
    #: empty, only the specified numbers and their extensions match the criteria.
    calls_to_numbers: Optional[list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]] = None


class ExecutiveAlertGetAlertingMode(str, Enum):
    #: Alerts assistants one at a time in the defined order.
    sequential = 'SEQUENTIAL'
    #: Alerts all assistants at the same time.
    simultaneous = 'SIMULTANEOUS'


class ExecutiveAlertGetRolloverAction(str, Enum):
    #: The call is sent to the executive's voicemail.
    voice_messaging = 'VOICE_MESSAGING'
    #: The call is sent to no answer processing which may trigger executive services such as call forwarding or
    #: voicemail.
    #: Rollover is always triggered when no assistants remain for a filtered call. If the rollover timer is enabled,
    #: rollover can also be triggered when the timer expires, even if assistants are still available.
    no_answer_processing = 'NO_ANSWER_PROCESSING'
    #: The call is forwarded to the specified destination (`rolloverForwardToPhoneNumber`).
    forward = 'FORWARD'


class ExecutiveAlertGetClidNameMode(str, Enum):
    #: Display executive name followed by caller name.
    executive_originator = 'EXECUTIVE_ORIGINATOR'
    #: Display caller name followed by executive name.
    originator_executive = 'ORIGINATOR_EXECUTIVE'
    #: Display only executive name.
    executive = 'EXECUTIVE'
    #: Display only caller name.
    originator = 'ORIGINATOR'
    #: Display a custom name.
    custom = 'CUSTOM'


class ExecutiveAlertGetClidPhoneNumberMode(str, Enum):
    #: Display executive's phone number.
    executive = 'EXECUTIVE'
    #: Display caller's phone number.
    originator = 'ORIGINATOR'
    #: Display a custom phone number.
    custom = 'CUSTOM'


class ExecutiveAlertGet(ApiModel):
    #: * `SEQUENTIAL` - Alerts assistants one at a time in the defined order.
    alerting_mode: Optional[ExecutiveAlertGetAlertingMode] = None
    #: Number of rings before alerting the next assistant when `alertingMode` is `SEQUENTIAL`.
    next_assistant_number_of_rings: Optional[int] = None
    #: Controls whether the rollover timer (`rolloverWaitTimeInSecs`) is enabled. When set to `true`, rollover will
    #: trigger after the timer expires, even if assistants are still available. When `false`, rollover only occurs
    #: when no assistants remain.
    rollover_enabled: Optional[bool] = None
    #: Specifies what happens when rollover is triggered.
    rollover_action: Optional[ExecutiveAlertGetRolloverAction] = None
    #: Phone number to forward calls to when rollover action is set to `FORWARD`.
    rollover_forward_to_phone_number: Optional[str] = None
    #: Time in seconds to wait before applying the rollover action when `rolloverEnabled` is `true`.
    rollover_wait_time_in_secs: Optional[int] = None
    #: Controls how Caller ID name is displayed on assistant's phone.
    clid_name_mode: Optional[ExecutiveAlertGetClidNameMode] = None
    #: Custom caller ID name to display when `clidNameMode` is set to `CUSTOM` (deprecated).
    custom_clidname: Optional[str] = Field(alias='customCLIDName', default=None)
    #: Unicode Custom caller ID name to display when `clidNameMode` is set to `CUSTOM`.
    custom_clidname_in_unicode: Optional[str] = Field(alias='customCLIDNameInUnicode', default=None)
    #: Controls which Caller ID phone number is displayed on assistant's phone.
    clid_phone_number_mode: Optional[ExecutiveAlertGetClidPhoneNumberMode] = None
    #: Custom caller ID phone number to display on assistant's phone when `clidPhoneNumberMode` is set to `CUSTOM`.
    custom_clidphone_number: Optional[str] = Field(alias='customCLIDPhoneNumber', default=None)


class Assistant(ApiModel):
    #: Unique identifier of the assistant.
    id: Optional[str] = None
    #: Unicode first name of the assistant. Is null if not available or if name is a single '.' or '-'.
    first_name: Optional[str] = None
    #: Unicode last name of the assistant. Is null if not available or if name is a single '.' or '-'.
    last_name: Optional[str] = None
    #: Direct number of the assistant.
    direct_number: Optional[str] = None
    #: Extension number of the assistant.
    extension: Optional[str] = None
    #: If `true`, the assistant has opted in to handle calls for the executive. If `false`, the assistant has not opted
    #: in.
    opt_in_enabled: Optional[bool] = None
    location: Optional[Location] = None


class AvailableAssistant(ApiModel):
    #: Unique identifier of the person.
    id: Optional[str] = None
    #: Unicode first name of the person. Is null if not available or if name is a single '.' or '-'.
    first_name: Optional[str] = None
    #: Unicode last name of the person. Is null if not available or if name is a single '.' or '-'.
    last_name: Optional[str] = None
    #: Direct number of the person.
    direct_number: Optional[str] = None
    #: Extension number of the person.
    extension: Optional[str] = None


class Executive(ApiModel):
    #: Unique identifier of the executive.
    id: Optional[str] = None
    #: Unicode first name of the executive. Is null if not available or if the name is a single ‘.’ or ‘-’.
    first_name: Optional[str] = None
    #: Unicode last name of the executive. Is null if not available or if the name is a single ‘.’ or ‘-’.
    last_name: Optional[str] = None
    #: Direct number of the executive.
    direct_number: Optional[str] = None
    #: Extension number of the executive.
    extension: Optional[str] = None
    #: If `true`, the assistant has opted in to handle calls for the executive.
    opt_in_enabled: Optional[bool] = None


class ExecutiveAssistantSettingsGet(ApiModel):
    #: If `true`, filtered calls to assistant are forwarded to the `forwardToPhoneNumber`.
    forward_filtered_calls_enabled: Optional[bool] = None
    #: Phone number to forward calls to when `forwardFilteredCallsEnabled` is set to `true`.
    forward_to_phone_number: Optional[str] = None
    #: List of executives for whom person is assigned as assistant.
    executives: Optional[list[Executive]] = None


class ExecutivePut(ApiModel):
    #: Unique identifier of the executive.
    person_id: Optional[str] = None
    #: If `true`, the assistant has opted in to handle calls for the executive.
    opt_in_enabled: Optional[bool] = None


class ExecutiveScreeningGetAlertType(str, Enum):
    #: No audible alert is provided for executive screening.
    silent = 'SILENT'
    #: A short ring (splash) is used as an alert for executive screening.
    ring_splash = 'RING_SPLASH'


class ExecutiveScreeningGet(ApiModel):
    #: Indicates if executive screening is enabled.
    enabled: Optional[bool] = None
    #: * `SILENT` - No audible alert is provided for executive screening.
    alert_type: Optional[ExecutiveScreeningGetAlertType] = None
    #: Indicates if alerts are enabled for Single Number Reach locations.
    alert_anywhere_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Webex Go locations.
    alert_mobility_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Shared Call Appearance locations.
    alert_shared_call_appearance_location_enabled: Optional[bool] = None


class LicenseType(str, Enum):
    webex_calling_professional = 'Webex Calling Professional'
    webex_calling_standard = 'Webex Calling Standard'


class GetMessageSummaryResponse(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int] = None
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int] = None
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int] = None
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int] = None


class UserCallSettings22Api(ApiChild, base=''):
    """
    User Call Settings (2/2)
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their own settings.
    
    Configuring People settings requires a full or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their own settings.
    
    Call Settings API access can be restricted via Control Hub by a full administrator. Restricting access causes the
    APIs to throw a `403 Access Forbidden` error.
    
    See details about `features available by license type for Webex Calling
    <https://help.webex.com/en-us/article/n1qbbp7/Features-available-by-license-type-for-Webex-Calling>`_.
    """

    def get_persons_app_services_settings_new(self, person_id: str, org_id: str = None) -> ApplicationsSetting:
        """
        Retrieve a person's Application Services Settings New

        Gets mobile and PC applications settings for a user.

        Application services let you determine the ringing behavior for calls made to people in certain scenarios. You
        can also specify which devices can download the Webex Calling app.

        Requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`ApplicationsSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/applications')
        data = super().get(url, params=params)
        r = ApplicationsSetting.model_validate(data)
        return r

    def list_move_users_jobs(self, org_id: str = None, **params) -> Generator[JobDetailsResponse, None, None]:
        """
        List Move Users Jobs

        Lists all the Move Users jobs for the given organization in order of most recent job to oldest job irrespective
        of its status.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of Move Users jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`JobDetailsResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('telephony/config/jobs/person/moveLocation')
        return self.session.follow_pagination(url=url, model=JobDetailsResponse, item_key='items', params=params)

    def validate_or_initiate_move_users_job(self, users_list: list[UsersListItem],
                                            org_id: str = None) -> list[UserListItem]:
        """
        Validate or Initiate Move Users Job

        This API allows the user to perform one of the following operations:

        * Setting the `validate` attribute to `true` validates the user move.

        * Setting the `validate` attribute to `false` performs the user move.

        <br/>

        Notes:

        * A maximum of `100` users can be moved at a time.

        * Setting the `validate` attribute to `true` only allowed for calling user.

        * When a single non calling user is moved, it will be moved synchronously without creating any job.

        <br/>

        Errors occurring during the initial API request validation are captured directly in the error response, along
        with the appropriate HTTP status code.

        <br/>

        Below is a list of possible error `code` values and their associated `message`, which can be found in the
        `errors` array during initial API request validation, regardless of the `validate` attribute value:

        * BATCH-400 - Attribute 'User ID' is required.

        * BATCH-400 - Users list should not be empty.

        * BATCH-400 - Users should not be empty.

        * 1026006 - Attribute 'Validate' is required.

        * 1026010 - User is not a valid Calling User.

        * 1026011 - Users list should not be empty.

        * 1026012 - Users should not be empty.

        * 1026013 - The source and the target location cannot be the same.

        * 1026014 - Error occurred while processing the move users request.

        * 1026015 - Error occurred while moving user number to target location.

        * 1026016 - User should have either phone number or extension.

        * 1026017 - Phone number is not in e164 format.

        * 1026018 - Selected Users list exceeds the maximum limit.

        * 1026019 - Duplicate entry for user is not allowed.

        * 1026020 - Validate 'true' is supported only for single user.

        * 1026021 - Attribute location id is required for Calling user.

        * 1026022 - Validate 'true' is supported for calling users only.

        * 1026023 - Extension and phone number is supported for calling users only.

        * 2150012 - User was not found

        <br/>

        When the `validate` attribute is set to true, the API identifies and returns the `errors` and `impacts`
        associated with the user move in the response.

        <br/>

        Below is a list of possible error `code` values and their associated `message`, which can be found in the
        `errors` array, when `validate` attribute is set to be true:

        * 4003 - `User Not Found`

        * 4007 - `User Not Found`

        * 4152 - `Location Not Found`

        * 5620 - `Location Not Found`

        * 4202 - `The extension is not available. It is already assigned to a user : {0}`

        * 8264 - `Routing profile is different with new group: {0}`

        * 19600 - `User has to be within an enterprise to be moved.`

        * 19601 - `User can only be moved to a different group within the same enterprise.`

        * 19602 - `Only regular end user can be moved. Service instance virtual user cannot be moved.`

        * 19603 - `New group already reaches maximum number of user limits.`

        * 19604 - `The {0} number of the user is the same as the calling line ID of the group.`

        * 19605 - `User is assigned services not authorized to the new group: {0}.`

        * 19606 - `User is in an active hoteling/flexible seating association.`

        * 19607 - `User is pilot user of a trunk group.`

        * 19608 - `User is using group level device profiles which is used by other users in current group. Following
        are the device profiles shared with other users: {0}.`

        * 19609 - `Following device profiles cannot be moved to the new group because there are already devices with
        the same name defined in the new group: {0}.`

        * 19610 - `The extension of the user is used as transfer to operator number for following Auto Attendent :
        {0}.`

        * 19611 - `Fail to move announcement file from {0} to {1}.`

        * 19612 - `Fail to move device management file from {0} to {1}.`

        * 19613 - `User is assigned service packs not authorized to the new group: {0}.`

        * 25008 - `Missing Mandatory field name: {0}`

        * 25110 - `{fieldName} cannot be less than {0} or greater than {1} characters.`

        * 25378 - `Target location is same as user's current location.`

        * 25379 - `Error Occurred while Fetching User's Current Location Id.`

        * 25381 - `Error Occurred while rolling back to Old Location Call recording Settings`

        * 25382 - `Error Occurred while Disabling Call Recording for user which is required Before User can be Moved`

        * 25383 - `OCI Error while moving user`

        * 25384 - `Error Occurred while checking for Possible Call Recording Impact.`

        * 25385 - `Error Occurred while getting Call Recording Settings`

        * 27559 - `The groupExternalId search criteria contains groups with different calling zone.`

        * 27960 - `Parameter isWebexCalling, newPhoneNumber, or newExtension can only be set in Webex Calling
        deployment mode.`

        * 27961 - `Parameter isWebexCalling shall be set if newPhoneNumber or newExtension is set.`

        * 27962 - `Work space cannot be moved.`

        * 27963 - `Virtual profile user cannot be moved.`

        * 27965 - `The user's phone number: {0}, is same as the current group charge number.`

        * 27966 - `The phone number, {0}, is not available in the new group.`

        * 27967 - `User is configured as the ECBN user for another user in the current group.`

        * 27968 - `User is configured as the ECBN user for the current group.`

        * 27969 - `User is associated with DECT handset(s): {0}`

        * 27970 - `User is using a customer managed device: {0}`

        * 27971 - `User is using an ATA device: {0}`

        * 27972 - `User is in an active hotdesking association.`

        * 27975 - `Need to unassign CLID number from group before moving the number to the new group. Phone number:
        {0}`

        * 27976 - `Local Gateway configuration is different with new group. Phone number: {0}`

        * 1026015 - `Error occurred while moving user number to target location`

        * 10010000 - `Total numbers exceeded maximum limit allowed`

        * 10010001 - `to-location and from-location cannot be same`

        * 10010002 - `to-location and from-location should belong to same customer`

        * 10010003 - `to-location must have a carrier`

        * 10010004 - `from-location must have a carrier`

        * 10010005 - `Different Carrier move is not supported for non-Cisco PSTN carriers.`

        * 10010006 - `Number move not supported for WEBEX_DIRECT carriers.`

        * 10010007 - `Numbers out of sync, missing on CPAPI`

        * 10010008 - `from-location not found or pstn connection missing in CPAPI`

        * 10010010 - `from-location is in transition`

        * 10010009 - `to-location not found or pstn connection missing in CPAPI`

        * 10010011 - `to-location is in transition`

        * 10010012 - `Numbers don't have a carrier Id`

        * 10010013 - `Location less numbers don't have a carrier Id`

        * 10010014 - `Different Carrier move is not supported for numbers with different country or region.`

        * 10010015 - `Numbers contain mobile and non-mobile types.`

        * 10010016 - `To/From location carriers must be same for mobile numbers.`

        * 10010017 - `Move request for location less number not supported`

        * 10010200 - `Move request for more than one block number is not supported`

        * 10010201 - `Cannot move block number as few numbers not from the block starting %s to %s`

        * 10010202 - `Cannot move block number as few numbers failed VERIFICATION from the block %s to %s`

        * 10010203 - `Cannot move block number as few numbers missing from the block %s to %s`

        * 10010204 - `Cannot move number as it is NOT a part of the block %s to %s`

        * 10010205 - `Move request for Cisco PSTN block order not supported.`

        * 10010299 - `Move order couldn't be created as no valid number to move`

        * 10030000 - `Number not found`

        * 10030001 - `Number does not belong to from-location`

        * 10030002 - `Number is not present in CPAPI`

        * 10030003 - `Number assigned to an user or device`

        * 10030004 - `Number not in Active status`

        * 10030005 - `Number is set as main number of the location`

        * 10030006 - `Number has pending order associated with it`

        * 10030007 - `Number belongs to a location but a from-location was not set`

        * 10030008 - `Numbers from multiple carrier ids are not supported`

        * 10030009 - `Location less number belongs to a location. from-location value is set to null or no location id`

        * 10030010 - `One or more numbers are not portable.`

        * 10030011 - `Mobile number carrier was not set`

        * 10030012 - `Number must be assigned for assigned move`

        * 10050000 - `Failed to update customer reference for phone numbers on carrier`

        * 10050001 - `Failed to update customer reference`

        * 10050002 - `Order is not of operation type MOVE`

        * 10050003 - `CPAPI delete call failed`

        * 10050004 - `Not found in database`

        * 10050005 - `Error sending notification to WxcBillingService`

        * 10050006 - `CPAPI provision number as active call failed with status %s ,reason %s`

        * 10050007 - `Failed to update E911 Service`

        * 10050008 - `Target location does not have Inbound Toll Free license`

        * 10050009 - `Source location or Target location subscription found cancelled or suspended`

        * 10050010 - `Moving On Premises or Non Integrated CCP numbers from one location to another is not supported.`

        * 10099999 - `{Error Code} - {Error Message}`

        <br/>

        Below is a list of possible impact `code` values and their associated `message`, which can be found in the
        `impacts` array, when `validate` attribute is set to be true:

        * 19701 - `The identity/device profile the user is using is moved to the new group: {0}.`

        * 19702 - `The user level customized incoming digit string setting is removed from the user. User is set to use
        the new group setting.`

        * 19703 - `The user level customized outgoing digit plan setting is removed from the user. User is set to use
        the new group setting.`

        * 19704 - `The user level customized enhanced outgoing calling plan setting is removed from the user. User is
        set to use the new group setting.`

        * 19705 - `User is removed from following group services: {0}.`

        * 19706 - `The current group schedule used in any criteria is removed from the service settings.`

        * 19707 - `User is removed from the department of the old group.`

        * 19708 - `User is changed to use the default communication barring profile of the new group.`

        * 19709 - `The communication barring profile of the user is assigned to the new group: {0}.`

        * 19710 - `The charge number for the user is removed.`

        * 19711 - `The disabled FACs for the user are removed because they are not available in the new group.`

        * 19712 - `User is removed from trunk group.`

        * 19713 - `The extension of the user is reset to empty due to either the length is out of bounds of the new
        group, or the extension is already taken in new group.`

        * 19714 - `The extension of the following alternate number is reset to empty due to either the length out of
        bounds of the new group or the extension is already taken in new group: {0}.`

        * 19715 - `The collaborate room using current group default collaborate bridge is moved to the default
        collaborate bridge of the new group.`

        * 19716 - `Previously stored voice messages of the user are no longer available. The new voice message will be
        stored on the mail server of the new group.`

        * 19717 - `The primary number, alternate numbers or fax messaging number of the user are assigned to the new
        group: {0}.`

        * 19718 - `Following domains are assigned to the new group: {0}.`

        * 19719 - `The NCOS of the user is assigned to the new group: {0}.`

        * 19720 - `The office zone of the user is assigned to the new group: {0}.`

        * 19721 - `The announcement media files are relocated to the new group directory.`

        * 19722 - `User CLID number is set to use the new group CLID number: {0}.`

        * 19723 - `New group CLID number is not configured.`

        * 19724 - `The group level announcement file(s) are removed from the user's music on hold settings.`

        * 25388 - `Target Location Does not Have Vendor Configured. Call Recording for user will be disabled`

        * 25389 - `Call Recording Vendor for user will be changed from:{0} to:{1}`

        * 25390 - `Dub point of user is moved to new external group`

        * 25391 - `Error Occurred while moving Call recording Settings to new location`

        * 25392 - `Error Occurred while checking for Possible Call Recording Impact.`

        * 25393 - `Sending Billing Notification Failed`

        This API requires a full administrator auth token with the scopes `spark-admin:telephony_config_write`,
        `spark-admin:people_write`, and `identity:groups_rw`.

        :param users_list: Specifies the users to be moved from the source location.
        :type users_list: list[UsersListItem]
        :param org_id: Create Move Users job for this organization.
        :type org_id: str
        :rtype: list[UserListItem]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['usersList'] = TypeAdapter(list[UsersListItem]).dump_python(users_list, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('telephony/config/jobs/person/moveLocation')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[UserListItem]).validate_python(data['response'])
        return r

    def get_move_users_job_status(self, job_id: str, org_id: str = None) -> JobDetailsResponseById:
        """
        Get Move Users Job Status

        Returns the status and other details of the job.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve job details for this organization.
        :type org_id: str
        :rtype: :class:`JobDetailsResponseById`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}')
        data = super().get(url, params=params)
        r = JobDetailsResponseById.model_validate(data)
        return r

    def pause_move_users_job(self, job_id: str, org_id: str = None):
        """
        Pause the Move Users Job

        Pause the running Move Users Job. A paused job can be resumed.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Pause the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Pause the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke')
        super().post(url, params=params)

    def resume_move_users_job(self, job_id: str, org_id: str = None):
        """
        Resume the Move Users Job

        Resume the paused Move Users Job that is in paused status.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Resume the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Resume the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke')
        super().post(url, params=params)

    def list_move_users_job_errors(self, job_id: str, org_id: str = None,
                                   **params) -> Generator[ItemObject, None, None]:
        """
        List Move Users Job errors

        Lists all error details of Move Users job. This will not list any errors if `exitCode` is `COMPLETED`. If the
        status is `COMPLETED_WITH_ERRORS` then this lists the cause of failures.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve the error details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/jobs/person/moveLocation/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def get_person_primary_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                                   license_type: LicenseType = None, org_id: str = None,
                                                   **params) -> Generator[PersonPrimaryAvailableNumberObject, None, None]:
        """
        Get Person Primary Available Phone Numbers

        List numbers that are available to be assigned as a person's primary phone number.
        By default, this API returns standard and mobile numbers from all locations that are unassigned. The parameters
        `licenseType` and `locationId` must align with the person's settings to determine the appropriate number for
        assignment.
        Failure to provide these parameters may result in the unsuccessful assignment of the returned number.

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
        :param license_type: Used to search numbers according to the person's `licenseType` to which the number will be
            assigned.
        :type license_type: LicenseType
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if license_type is not None:
            params['licenseType'] = enum_str(license_type)
        url = self.ep('telephony/config/people/primary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_default_feature_access_settings_person(self) -> UserSettingsPermissionsGetDefault:
        """
        Read Default Feature Access Settings for Person

        Read the default feature access configuration for users in the organization. It allows administrators to review
        the baseline feature availability settings that will be applied to new users by default, ensuring consistency
        in user experience and policy enforcement.

        This API is part of the organizational-level user configuration management for feature access. It is used to
        define the default settings that control which Webex features are enabled or disabled when users are
        provisioned. In Control Hub, this corresponds to the "Default User Settings" under Calling or Telephony,
        providing centralized control over user capabilities across the organization.

        To call this API, an administrator must use a full, or read-only administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :rtype: :class:`UserSettingsPermissionsGetDefault`
        """
        url = self.ep('telephony/config/people/settings/permissions')
        data = super().get(url)
        r = UserSettingsPermissionsGetDefault.model_validate(data)
        return r

    def modify_default_person_feature_access_configuration(self, anonymous_call_rejection: AccessLevel = None,
                                                           barge_in: AccessLevel = None,
                                                           block_caller_id: AccessLevel = None,
                                                           call_forwarding: AccessLevel = None,
                                                           call_waiting: AccessLevel = None,
                                                           call_notify: AccessLevel = None,
                                                           connected_line_identity: AccessLevel = None,
                                                           executive: AccessLevel = None,
                                                           hoteling: AccessLevel = None,
                                                           priority_alert: AccessLevel = None,
                                                           selectively_accept_calls: AccessLevel = None,
                                                           selectively_reject_calls: AccessLevel = None,
                                                           selectively_forward_calls: AccessLevel = None,
                                                           sequential_ring: AccessLevel = None,
                                                           simultaneous_ring: AccessLevel = None,
                                                           single_number_reach: AccessLevel = None,
                                                           voicemail: AccessLevel = None,
                                                           send_calls_to_voicemail: AccessLevel = None,
                                                           voicemail_email_copy: AccessLevel = None,
                                                           voicemail_fax_messaging: AccessLevel = None,
                                                           voicemail_message_storage: AccessLevel = None,
                                                           voicemail_notifications: AccessLevel = None,
                                                           voicemail_transfer_number: AccessLevel = None,
                                                           generate_activation_code: AccessLevel = None,
                                                           voicemail_download: AccessLevel = None):
        """
        Update Default Person Feature Access Configuration

        Updates the default feature access configuration for users in the organization. It allows administrators to
        modify the baseline settings that determine which Webex features are enabled or disabled for users by default,
        ensuring new users are provisioned with consistent access controls.

        This API is part of the organization-level user configuration management for feature access. It supports
        defining and updating default settings that apply automatically to all newly onboarded users. In Control Hub,
        this corresponds to the "Default User Settings" section for Calling or Telephony, enabling centralized and
        scalable configuration of user capabilities.

        To use this API, an administrator must authenticate with a full, or device administrator auth token. The token
        must include the `spark-admin:telephony_config_write` scope.

        :param anonymous_call_rejection: Set whether end users have access to make changes to their `Anonymous call
            rejection` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type anonymous_call_rejection: AccessLevel
        :param barge_in: Set whether end users have access to make changes to their `Barge In` feature via User Hub, or
            other clients (Webex, IP phone, etc.).
        :type barge_in: AccessLevel
        :param block_caller_id: Set whether end users have access to make changes to their `Block caller ID` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type block_caller_id: AccessLevel
        :param call_forwarding: Set whether end users have access to make changes to their `Call forwarding` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type call_forwarding: AccessLevel
        :param call_waiting: Set whether end users have access to make changes to their `Call waiting` feature via User
            Hub, or other clients (Webex, IP phone, etc.).
        :type call_waiting: AccessLevel
        :param call_notify: Set whether end users have access to make changes to their `Call notify` feature via User
            Hub, or other clients (Webex, IP phone, etc.).
        :type call_notify: AccessLevel
        :param connected_line_identity: Set whether end users have access to make changes to their `Connected line
            identity` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type connected_line_identity: AccessLevel
        :param executive: Set whether end users have access to make changes to their `Executive/Executive assistant`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type executive: AccessLevel
        :param hoteling: Set whether end users have access to make changes to their `Hoteling` feature via User Hub, or
            other clients (Webex, IP phone, etc.).
        :type hoteling: AccessLevel
        :param priority_alert: Set whether end users have access to make changes to their `Priority alert` feature via
            User Hub, or other clients (Webex, IP phone, etc.).
        :type priority_alert: AccessLevel
        :param selectively_accept_calls: Set whether end users have access to make changes to their `Selectively accept
            calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_accept_calls: AccessLevel
        :param selectively_reject_calls: Set whether end users have access to make changes to their `Selectively reject
            calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_reject_calls: AccessLevel
        :param selectively_forward_calls: Set whether end users have access to make changes to their `Selectively
            forward calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_forward_calls: AccessLevel
        :param sequential_ring: Set whether end users have access to make changes to their `Sequential ring` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type sequential_ring: AccessLevel
        :param simultaneous_ring: Set whether end users have access to make changes to their `Simultaneous ring`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type simultaneous_ring: AccessLevel
        :param single_number_reach: Set whether end users have access to make changes to their `Single number reach`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type single_number_reach: AccessLevel
        :param voicemail: Set whether end users have access to make changes to their `Voicemail feature` feature via
            User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail: AccessLevel
        :param send_calls_to_voicemail: Set whether end users have access to make changes to their `Send calls to
            voicemail` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type send_calls_to_voicemail: AccessLevel
        :param voicemail_email_copy: Set whether end users have access to make changes to their `Email a copy of the
            voicemail message` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_email_copy: AccessLevel
        :param voicemail_fax_messaging: Set whether end users have access to make changes to their `Fax messaging`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_fax_messaging: AccessLevel
        :param voicemail_message_storage: Set whether end users have access to make changes to their `Message storage`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_message_storage: AccessLevel
        :param voicemail_notifications: Set whether end users have access to make changes to their `Notifications`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_notifications: AccessLevel
        :param voicemail_transfer_number: Set whether end users have access to make changes to their `Transfer on '0'
            to another number.` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_transfer_number: AccessLevel
        :param generate_activation_code: Set whether end users have access to make changes to their `Allow End User to
            Generate Activation Codes & Delete their Phones` feature via User Hub, or other clients (Webex, IP phone,
            etc.).
        :type generate_activation_code: AccessLevel
        :param voicemail_download: Set whether end users have access to download voicemail via User Hub, or other
            clients (Webex, etc.).
        :type voicemail_download: AccessLevel
        :rtype: None
        """
        body = dict()
        if anonymous_call_rejection is not None:
            body['anonymousCallRejection'] = enum_str(anonymous_call_rejection)
        if barge_in is not None:
            body['bargeIn'] = enum_str(barge_in)
        if block_caller_id is not None:
            body['blockCallerId'] = enum_str(block_caller_id)
        if call_forwarding is not None:
            body['callForwarding'] = enum_str(call_forwarding)
        if call_waiting is not None:
            body['callWaiting'] = enum_str(call_waiting)
        if call_notify is not None:
            body['callNotify'] = enum_str(call_notify)
        if connected_line_identity is not None:
            body['connectedLineIdentity'] = enum_str(connected_line_identity)
        if executive is not None:
            body['executive'] = enum_str(executive)
        if hoteling is not None:
            body['hoteling'] = enum_str(hoteling)
        if priority_alert is not None:
            body['priorityAlert'] = enum_str(priority_alert)
        if selectively_accept_calls is not None:
            body['selectivelyAcceptCalls'] = enum_str(selectively_accept_calls)
        if selectively_reject_calls is not None:
            body['selectivelyRejectCalls'] = enum_str(selectively_reject_calls)
        if selectively_forward_calls is not None:
            body['selectivelyForwardCalls'] = enum_str(selectively_forward_calls)
        if sequential_ring is not None:
            body['sequentialRing'] = enum_str(sequential_ring)
        if simultaneous_ring is not None:
            body['simultaneousRing'] = enum_str(simultaneous_ring)
        if single_number_reach is not None:
            body['singleNumberReach'] = enum_str(single_number_reach)
        if voicemail is not None:
            body['voicemail'] = enum_str(voicemail)
        if send_calls_to_voicemail is not None:
            body['sendCallsToVoicemail'] = enum_str(send_calls_to_voicemail)
        if voicemail_email_copy is not None:
            body['voicemailEmailCopy'] = enum_str(voicemail_email_copy)
        if voicemail_fax_messaging is not None:
            body['voicemailFaxMessaging'] = enum_str(voicemail_fax_messaging)
        if voicemail_message_storage is not None:
            body['voicemailMessageStorage'] = enum_str(voicemail_message_storage)
        if voicemail_notifications is not None:
            body['voicemailNotifications'] = enum_str(voicemail_notifications)
        if voicemail_transfer_number is not None:
            body['voicemailTransferNumber'] = enum_str(voicemail_transfer_number)
        if generate_activation_code is not None:
            body['generateActivationCode'] = enum_str(generate_activation_code)
        if voicemail_download is not None:
            body['voicemailDownload'] = enum_str(voicemail_download)
        url = self.ep('telephony/config/people/settings/permissions')
        super().put(url, json=body)

    def retrieve_agents_list_of_available_caller_ids(self, person_id: str,
                                                     org_id: str = None) -> list[AvailableCallerIdObject]:
        """
        Retrieve Agent's List of Available Caller IDs

        Get the list of call queues and hunt groups available for caller ID use by this person as an agent.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: list[AvailableCallerIdObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/agent/availableCallerIds')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AvailableCallerIdObject]).validate_python(data['availableCallerIds'])
        return r

    def retrieve_agents_caller_idinformation(self, person_id: str) -> AvailableCallerIdObject:
        """
        Retrieve Agent's Caller ID Information

        Retrieve the Agent's Caller ID Information.

        Each agent will be able to set their outgoing Caller ID as either the Call Queue's Caller ID, Hunt Group's
        Caller ID or their own configured Caller ID.

        This API requires a full admin or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: AvailableCallerIdObject
        """
        url = self.ep(f'telephony/config/people/{person_id}/agent/callerId')
        data = super().get(url)
        r = AvailableCallerIdObject.model_validate(data['selectedCallerId'])
        return r

    def modify_agent_caller_id_information(self, person_id: str, selected_caller_id: str):
        """
        Modify Agent's Caller ID Information.

        Each Agent will be able to set their outgoing Caller ID as either the designated Call Queue's Caller ID or Hunt
        Group's Caller ID or their own configured Caller ID

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected_caller_id: The unique identifier of the call queue or hunt group to use for the agent's caller
            ID. Set to null to use the agent's own caller ID.
        :type selected_caller_id: str
        :rtype: None
        """
        body = dict()
        body['selectedCallerId'] = selected_caller_id
        url = self.ep(f'telephony/config/people/{person_id}/agent/callerId')
        super().put(url, json=body)

    def search_shared_line_appearance_members_new(self, person_id: str, order: str = None, location: str = None,
                                                  name: str = None, phone_number: str = None, extension: str = None,
                                                  **params) -> Generator[AvailableSharedLineMemberItem, None, None]:
        """
        Search Shared-Line Appearance Members New

        Get members available for shared-line assignment to a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param order: Order the Route Lists according to number, ascending or descending.
        :type order: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param phone_number: Search for users with numbers that match the query.
        :type phone_number: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :return: Generator yielding :class:`AvailableSharedLineMemberItem` instances
        """
        if order is not None:
            params['order'] = order
        if location is not None:
            params['location'] = location
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/applications/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableSharedLineMemberItem, item_key='members', params=params)

    def get_shared_line_appearance_members_new(self, person_id: str) -> GetSharedLineMemberList:
        """
        Get Shared-Line Appearance Members New

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :rtype: :class:`GetSharedLineMemberList`
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/members')
        data = super().get(url)
        r = GetSharedLineMemberList.model_validate(data)
        return r

    def put_shared_line_appearance_members_new(self, person_id: str,
                                               members: list[ApplicationPutSharedLineMemberItem] = None):
        """
        Put Shared-Line Appearance Members New

        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param members: List of members to be added or modified for shared-line assignment to a Webex Calling Apps.
        :type members: list[ApplicationPutSharedLineMemberItem]
        :rtype: None
        """
        body = dict()
        if members is not None:
            body['members'] = TypeAdapter(list[ApplicationPutSharedLineMemberItem]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/applications/members')
        super().put(url, json=body)

    def search_shared_line_appearance_members(self, person_id: str, application_id: str, location: str = None,
                                              name: str = None, number: str = None, order: str = None,
                                              extension: str = None,
                                              **params) -> Generator[AvailableSharedLineMemberItem, None, None]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (`fname`) or last name (`lname`).
        :type order: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :return: Generator yielding :class:`AvailableSharedLineMemberItem` instances
        """
        if location is not None:
            params['location'] = location
        if name is not None:
            params['name'] = name
        if number is not None:
            params['number'] = number
        if order is not None:
            params['order'] = order
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableSharedLineMemberItem, item_key='members', params=params)

    def get_shared_line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineMemberList:
        """
        Get Shared-Line Appearance Members

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :rtype: :class:`GetSharedLineMemberList`
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        data = super().get(url)
        r = GetSharedLineMemberList.model_validate(data)
        return r

    def modify_shared_line_appearance_members(self, person_id: str, application_id: str,
                                              members: list[PutSharedLineMemberItem] = None):
        """
        Put Shared-Line Appearance Members

        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :type members: list[PutSharedLineMemberItem]
        :rtype: None
        """
        body = dict()
        if members is not None:
            body['members'] = TypeAdapter(list[PutSharedLineMemberItem]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        super().put(url, json=body)

    def get_user_call_captions_settings(self, person_id: str, org_id: str = None) -> GetUserCallCaptionsObject:
        """
        Get the user call captions settings

        Retrieve the user's call captions settings.

        **NOTE**: The call captions feature is not supported for Webex Calling Standard users or users assigned to
        locations in India.

        The call caption feature allows the customer to enable and manage closed captions and transcript functionality
        (rolling caption panel) in Webex Calling, without requiring the user to escalate the call to a meeting.

        This API requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: :class:`GetUserCallCaptionsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/callCaptions')
        data = super().get(url, params=params)
        r = GetUserCallCaptionsObject.model_validate(data)
        return r

    def modify_user_call_captions_settings(self, person_id: str, user_closed_captions_enabled: bool = None,
                                           user_transcripts_enabled: bool = None,
                                           use_location_settings_enabled: bool = None, org_id: str = None):
        """
        Update the user call captions settings

        Update the user's call captions settings.

        **NOTE**: The call captions feature is not supported for Webex Calling Standard users or users assigned to
        locations in India.

        The call caption feature allows the customer to enable and manage closed captions and transcript functionality
        (rolling caption panel) in Webex Calling, without requiring the user to escalate the call to a meeting.

        This API requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param user_closed_captions_enabled: Enable or disable user-level closed captions.
        :type user_closed_captions_enabled: bool
        :param user_transcripts_enabled: Enable or disable user-level transcripts.
        :type user_transcripts_enabled: bool
        :param use_location_settings_enabled: If `useLocationSettingsEnabled` is `true`, location settings will control
            the user's closed captions and transcripts. Otherwise, user-level settings are used.
        :type use_location_settings_enabled: bool
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if user_closed_captions_enabled is not None:
            body['userClosedCaptionsEnabled'] = user_closed_captions_enabled
        if user_transcripts_enabled is not None:
            body['userTranscriptsEnabled'] = user_transcripts_enabled
        if use_location_settings_enabled is not None:
            body['useLocationSettingsEnabled'] = use_location_settings_enabled
        url = self.ep(f'telephony/config/people/{person_id}/callCaptions')
        super().put(url, params=params, json=body)

    def get_person_call_forward_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                        owner_name: str = None, extension: str = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a person's call forward number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_call_intercept_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                          owner_name: str = None, extension: str = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a person's call intercept
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_ecbn_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                owner_name: str = None, org_id: str = None,
                                                **params) -> Generator[PersonECBNAvailableNumberObject, None, None]:
        """
        Get Person ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a person's emergency callback number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'telephony/config/people/{person_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_executive_alert_settings(self, person_id: str, org_id: str = None) -> ExecutiveAlertGet:
        """
        Get Person Executive Alert Settings

        Get executive alert settings for the specified person.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: :class:`ExecutiveAlertGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/alert')
        data = super().get(url, params=params)
        r = ExecutiveAlertGet.model_validate(data)
        return r

    def update_person_executive_alert_settings(self, person_id: str,
                                               alerting_mode: ExecutiveAlertGetAlertingMode = None,
                                               next_assistant_number_of_rings: int = None,
                                               rollover_enabled: bool = None,
                                               rollover_action: ExecutiveAlertGetRolloverAction = None,
                                               rollover_forward_to_phone_number: str = None,
                                               rollover_wait_time_in_secs: int = None,
                                               clid_name_mode: ExecutiveAlertGetClidNameMode = None,
                                               custom_clidname: str = None, custom_clidname_in_unicode: str = None,
                                               clid_phone_number_mode: ExecutiveAlertGetClidPhoneNumberMode = None,
                                               custom_clidphone_number: str = None, org_id: str = None):
        """
        Modify Person Executive Alert Settings

        Update executive alert settings for the specified person.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param alerting_mode: * `SEQUENTIAL` - Alerts assistants one at a time in the defined order.
        :type alerting_mode: ExecutiveAlertGetAlertingMode
        :param next_assistant_number_of_rings: Number of rings before alerting the next assistant when `alertingMode`
            is `SEQUENTIAL`.
        :type next_assistant_number_of_rings: int
        :param rollover_enabled: Controls whether the rollover timer (`rolloverWaitTimeInSecs`) is enabled. When set to
            `true`, rollover will trigger after the timer expires, even if assistants are still available. When
            `false`, rollover only occurs when no assistants remain.
        :type rollover_enabled: bool
        :param rollover_action: Specifies what happens when rollover is triggered.
        :type rollover_action: ExecutiveAlertGetRolloverAction
        :param rollover_forward_to_phone_number: Phone number to forward calls to when rollover action is set to
            `FORWARD`.
        :type rollover_forward_to_phone_number: str
        :param rollover_wait_time_in_secs: Time in seconds to wait before applying the rollover action when
            `rolloverEnabled` is `true`.
        :type rollover_wait_time_in_secs: int
        :param clid_name_mode: Controls how Caller ID name is displayed on assistant's phone.
        :type clid_name_mode: ExecutiveAlertGetClidNameMode
        :param custom_clidname: Custom caller ID name to display when `clidNameMode` is set to `CUSTOM` (deprecated).
        :type custom_clidname: str
        :param custom_clidname_in_unicode: Unicode Custom caller ID name to display when `clidNameMode` is set to
            `CUSTOM`.
        :type custom_clidname_in_unicode: str
        :param clid_phone_number_mode: Controls which Caller ID phone number is displayed on assistant's phone.
        :type clid_phone_number_mode: ExecutiveAlertGetClidPhoneNumberMode
        :param custom_clidphone_number: Custom caller ID phone number to display on assistant's phone when
            `clidPhoneNumberMode` is set to `CUSTOM`.
        :type custom_clidphone_number: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if alerting_mode is not None:
            body['alertingMode'] = enum_str(alerting_mode)
        if next_assistant_number_of_rings is not None:
            body['nextAssistantNumberOfRings'] = next_assistant_number_of_rings
        if rollover_enabled is not None:
            body['rolloverEnabled'] = rollover_enabled
        if rollover_action is not None:
            body['rolloverAction'] = enum_str(rollover_action)
        if rollover_forward_to_phone_number is not None:
            body['rolloverForwardToPhoneNumber'] = rollover_forward_to_phone_number
        if rollover_wait_time_in_secs is not None:
            body['rolloverWaitTimeInSecs'] = rollover_wait_time_in_secs
        if clid_name_mode is not None:
            body['clidNameMode'] = enum_str(clid_name_mode)
        if custom_clidname is not None:
            body['customCLIDName'] = custom_clidname
        if custom_clidname_in_unicode is not None:
            body['customCLIDNameInUnicode'] = custom_clidname_in_unicode
        if clid_phone_number_mode is not None:
            body['clidPhoneNumberMode'] = enum_str(clid_phone_number_mode)
        if custom_clidphone_number is not None:
            body['customCLIDPhoneNumber'] = custom_clidphone_number
        url = self.ep(f'telephony/config/people/{person_id}/executive/alert')
        super().put(url, params=params, json=body)

    def get_person_executive_assigned_assistants(self, person_id: str, org_id: str = None) -> list[Assistant]:
        """
        Get Person Executive Assigned Assistants

        Get list of assigned executive assistants for the specified person.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: list[Assistant]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/assignedAssistants')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Assistant]).validate_python(data['assistants'])
        return r

    def modify_person_executive_assigned_assistants(self, person_id: str, assistant_ids: list[str] = None,
                                                    org_id: str = None):
        """
        Modify Person Executive Assigned Assistants

        Update assigned executive assistants for the specified person.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param assistant_ids: List of people to be assigned as assistant. To remove all assigned assistants, set
            `assistantIds` to `null`.
        :type assistant_ids: list[str]
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if assistant_ids is not None:
            body['assistantIds'] = assistant_ids
        url = self.ep(f'telephony/config/people/{person_id}/executive/assignedAssistants')
        super().put(url, params=params, json=body)

    def get_person_executive_assistant_settings(self, person_id: str,
                                                org_id: str = None) -> ExecutiveAssistantSettingsGet:
        """
        Get Person Executive Assistant Settings

        Get executive assistant settings for the specified person when person is configured as executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: :class:`ExecutiveAssistantSettingsGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/assistant')
        data = super().get(url, params=params)
        r = ExecutiveAssistantSettingsGet.model_validate(data)
        return r

    def modify_person_executive_assistant_settings(self, person_id: str, forward_filtered_calls_enabled: bool = None,
                                                   forward_to_phone_number: str = None,
                                                   executives: list[ExecutivePut] = None, org_id: str = None):
        """
        Modify Person Executive Assistant Settings

        Update executive assistant settings for the specified person when person is configured as executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param forward_filtered_calls_enabled: If `true`, filtered calls to assistant are forwarded to the
            `forwardToPhoneNumber`.
        :type forward_filtered_calls_enabled: bool
        :param forward_to_phone_number: Phone number to forward the filtered calls to. Mandatory if
            `forwardFilteredCallsEnabled` is set to true.
        :type forward_to_phone_number: str
        :param executives: List of executives.
        :type executives: list[ExecutivePut]
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if forward_filtered_calls_enabled is not None:
            body['forwardFilteredCallsEnabled'] = forward_filtered_calls_enabled
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if executives is not None:
            body['executives'] = TypeAdapter(list[ExecutivePut]).dump_python(executives, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/executive/assistant')
        super().put(url, params=params, json=body)

    def get_person_executive_available_assistants(self, person_id: str, name: str = None, phone_number: str = None,
                                                  org_id: str = None,
                                                  **params) -> Generator[AvailableAssistant, None, None]:
        """
        Get Person Executive Available Assistants

        Retrieves a list of people available for assignment as executive assistants to the specified person.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param name: Only return people with the matching name (person's first and last name combination).
        :type name: str
        :param phone_number: Only return people with the matching phone number or extension.
        :type phone_number: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAssistant` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep(f'telephony/config/people/{person_id}/executive/availableAssistants')
        return self.session.follow_pagination(url=url, model=AvailableAssistant, item_key='assistants', params=params)

    def get_person_executive_call_filtering_settings(self, person_id: str,
                                                     org_id: str = None) -> ExecutiveCallFilteringGet:
        """
        Get Person Executive Call Filtering Settings

        Retrieve the executive call filtering settings for the specified person.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: :class:`ExecutiveCallFilteringGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering')
        data = super().get(url, params=params)
        r = ExecutiveCallFilteringGet.model_validate(data)
        return r

    def update_person_executive_call_filtering_settings(self, person_id: str, enabled: bool = None,
                                                        filter_type: ExecutiveCallFilteringGetFilterType = None,
                                                        criteria_activation: list[ExecutiveCallFilteringPatchCriteriaActivationItem] = None,
                                                        org_id: str = None):
        """
        Modify Person Executive Call Filtering Settings

        Update the executive call filtering settings for the specified person.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param enabled: Set to `true` to enable executive call filtering or `false` to disable it.
        :type enabled: bool
        :param filter_type: * `CUSTOM_CALL_FILTERS` - Choose this option to ensure that only specific calls are sent to
            the executive assistant.
        :type filter_type: ExecutiveCallFilteringGetFilterType
        :param criteria_activation: The list of criteria activation settings to update for executive call filtering.
        :type criteria_activation: list[ExecutiveCallFilteringPatchCriteriaActivationItem]
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if filter_type is not None:
            body['filterType'] = enum_str(filter_type)
        if criteria_activation is not None:
            body['criteriaActivation'] = TypeAdapter(list[ExecutiveCallFilteringPatchCriteriaActivationItem]).dump_python(criteria_activation, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering')
        super().put(url, params=params, json=body)

    def create_person_executive_call_filtering_criteria(self, person_id: str, filter_name: str, calls_from: CallsFrom,
                                                        filter_enabled: bool, schedule_name: str = None,
                                                        schedule_type: ScheduleType = None,
                                                        schedule_level: ScheduleLevel = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None,
                                                        calls_to_numbers: list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem] = None,
                                                        org_id: str = None) -> str:
        """
        Add Person Executive Call Filtering Criteria

        Create a new executive call filtering criteria configuration for the specified person.

        Executive Call Filtering Criteria in Webex allows you to define detailed filter rules for incoming calls. This
        API creates a new filter rule with the specified configuration, including schedule, phone numbers, and call
        routing preferences.

        This API requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param filter_name: Name of the criteria.
        :type filter_name: str
        :param calls_from: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
        :type calls_from: CallsFrom
        :param filter_enabled: Controls the action when this criteria matches a call. When `true`, matching calls are
            filtered and will alert the executive's assistants. When `false`, matching calls are not filtered and will
            not alert the executive's assistants. Criteria with `filterEnabled` as `false` take precedence over other
            filtering criteria with `filterEnabled` as `true`, allowing exceptions where certain calls are not
            filtered to the executive's assistants.
        :type filter_enabled: bool
        :param schedule_name: Name of the schedule associated with this criteria.
        :type schedule_name: str
        :param schedule_type: * `businessHours` - The schedule type that specifies the business or working hours during
            the day.
        :type schedule_type: ScheduleType
        :param schedule_level: * `PEOPLE` - The schedule level that specifies that criteria is of People level.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Set to enable or disable the criteria for anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Set to enable or disable the criteria for unavailable callers.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that this filtering criteria applies to, when `callsFrom` is
            set to `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param calls_to_numbers: List of numbers for the executive that will match the criteria when called. This may
            include the executive’s primary number and/or extension, as well as secondary (alternate) numbers (and
            associated extensions). If the list is empty, any number or extension for the executive matches the
            criteria when called. If the list is not empty, only the specified numbers and their extensions match the
            criteria.
        :type calls_to_numbers: list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['filterName'] = filter_name
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['filterEnabled'] = filter_enabled
        if calls_to_numbers is not None:
            body['callsToNumbers'] = TypeAdapter(list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]).dump_python(calls_to_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_person_executive_call_filtering_criteria(self, person_id: str, id: str, org_id: str = None):
        """
        Delete Person Executive Call Filtering Criteria

        Delete a specific executive call filtering criteria configuration for the specified person.

        Executive Call Filtering Criteria in Webex allows you to manage detailed filter rules for incoming calls. This
        API removes a specific filter rule by its unique identifier.

        This API requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}')
        super().delete(url, params=params)

    def get_person_executive_call_filtering_criteria(self, person_id: str, id: str,
                                                     org_id: str = None) -> ExecutiveCallFilteringCriteriaGet:
        """
        Get Person Executive Call Filtering Criteria Settings

        Retrieve the executive call filtering criteria settings for the specified person.

        Executive Call Filtering Criteria in Webex allows you to retrieve the detailed configuration for a specific
        filter rule. This includes schedule settings, phone number filters, and call routing preferences for executive
        call filtering.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
        :type id: str
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: :class:`ExecutiveCallFilteringCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}')
        data = super().get(url, params=params)
        r = ExecutiveCallFilteringCriteriaGet.model_validate(data)
        return r

    def update_person_executive_call_filtering_criteria(self, person_id: str, id: str, schedule_name: str = None,
                                                        schedule_type: ScheduleType = None,
                                                        schedule_level: ScheduleLevel = None,
                                                        calls_from: CallsFrom = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None, filter_enabled: bool = None,
                                                        calls_to_numbers: list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem] = None,
                                                        org_id: str = None):
        """
        Modify Person Executive Call Filtering Criteria Settings

        Update the executive call filtering settings for the specified person.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :param schedule_name: Name of the schedule associated with this criteria.
        :type schedule_name: str
        :param schedule_type: * `businessHours` - The schedule type that specifies the business or working hours during
            the day.
        :type schedule_type: ScheduleType
        :param schedule_level: * `PEOPLE` - The schedule level that specifies that criteria is of People level.
        :type schedule_level: ScheduleLevel
        :param calls_from: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
        :type calls_from: CallsFrom
        :param anonymous_callers_enabled: Set to enable or disable the criteria for anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Set to enable or disable the criteria for unavailable callers.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that this filtering criteria applies to, when `callsFrom` is
            set to `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param filter_enabled: Controls the action when this criteria matches a call. When `true`, matching calls are
            filtered and will alert the executive's assistants. When `false`, matching calls are not filtered and will
            not alert the executive's assistants. Criteria with `filterEnabled` as `false` take precedence over other
            filtering criteria with `filterEnabled` as `true`, allowing exceptions where certain calls are not
            filtered to the executive's assistants.
        :type filter_enabled: bool
        :param calls_to_numbers: List of numbers for the executive that will match the criteria when called. This may
            include the executive’s primary number and/or extension, as well as secondary (alternate) numbers (and
            associated extensions). If the list is empty, any number or extension for the executive matches the
            criteria when called. If the list is not empty, only the specified numbers and their extensions match the
            criteria.
        :type calls_to_numbers: list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]
        :param org_id: Organization ID for the user.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if filter_enabled is not None:
            body['filterEnabled'] = filter_enabled
        if calls_to_numbers is not None:
            body['callsToNumbers'] = TypeAdapter(list[ExecutiveCallFilteringCriteriaGetCallsToNumbersItem]).dump_python(calls_to_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}')
        super().put(url, params=params, json=body)

    def get_person_executive_screening_settings(self, person_id: str, org_id: str = None) -> ExecutiveScreeningGet:
        """
        Get Person Executive Screening Settings

        Get executive screening settings for the specified person.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a full, user, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: :class:`ExecutiveScreeningGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/executive/screening')
        data = super().get(url, params=params)
        r = ExecutiveScreeningGet.model_validate(data)
        return r

    def update_person_executive_screening_settings(self, person_id: str, enabled: bool = None,
                                                   alert_type: ExecutiveScreeningGetAlertType = None,
                                                   alert_anywhere_location_enabled: bool = None,
                                                   alert_mobility_location_enabled: bool = None,
                                                   alert_shared_call_appearance_location_enabled: bool = None,
                                                   org_id: str = None):
        """
        Modify Person Executive Screening Settings

        Update executive screening settings for the specified person.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param enabled: Set to enable or disable executive screening.
        :type enabled: bool
        :param alert_type: * `SILENT` - No audible alert is provided for executive screening.
        :type alert_type: ExecutiveScreeningGetAlertType
        :param alert_anywhere_location_enabled: Indicates if alerts are enabled for Single Number Reach locations.
        :type alert_anywhere_location_enabled: bool
        :param alert_mobility_location_enabled: Indicates if alerts are enabled for Webex Go locations.
        :type alert_mobility_location_enabled: bool
        :param alert_shared_call_appearance_location_enabled: Indicates if alerts are enabled for Shared Call
            Appearance locations.
        :type alert_shared_call_appearance_location_enabled: bool
        :param org_id: Organization ID for the person.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if alert_type is not None:
            body['alertType'] = enum_str(alert_type)
        if alert_anywhere_location_enabled is not None:
            body['alertAnywhereLocationEnabled'] = alert_anywhere_location_enabled
        if alert_mobility_location_enabled is not None:
            body['alertMobilityLocationEnabled'] = alert_mobility_location_enabled
        if alert_shared_call_appearance_location_enabled is not None:
            body['alertSharedCallAppearanceLocationEnabled'] = alert_shared_call_appearance_location_enabled
        url = self.ep(f'telephony/config/people/{person_id}/executive/screening')
        super().put(url, params=params, json=body)

    def get_person_fax_message_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a person's FAX message number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/people/{person_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def read_call_bridge_settings_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Bridge Settings for a Person

        Retrieve a person's Call Bridge settings.

        This API requires a full, user or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/features/callBridge')
        data = super().get(url, params=params)
        r = data['warningToneEnabled']
        return r

    def configure_call_bridge_settings_person(self, person_id: str, warning_tone_enabled: bool = None,
                                              org_id: str = None):
        """
        Configure Call Bridge Settings for a Person

        Configure a person's Call Bridge settings.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param warning_tone_enabled: Set to enable or disable a stutter dial tone being played to all the participants
            when a person is bridged on the active shared line call.
        :type warning_tone_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if warning_tone_enabled is not None:
            body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'telephony/config/people/{person_id}/features/callBridge')
        super().put(url, params=params, json=body)

    def get_personal_assistant(self, person_id: str, org_id: str = None) -> PersonalAssistantGet:
        """
        Get Personal Assistant

        Retrieve Personal Assistant details for a specific user.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Retrieving Personal Assistant details requires a full, user, or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Get Personal Assistant details for the organization.
        :type org_id: str
        :rtype: :class:`PersonalAssistantGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/features/personalAssistant')
        data = super().get(url, params=params)
        r = PersonalAssistantGet.model_validate(data)
        return r

    def modify_personal_assistant(self, person_id: str, enabled: bool = None,
                                  presence: PersonalAssistantGetPresence = None, until_date_time: Union[str,
                                  datetime] = None, transfer_enabled: bool = None, transfer_number: str = None,
                                  alerting: PersonalAssistantGetAlerting = None,
                                  alert_me_first_number_of_rings: int = None, org_id: str = None):
        """
        Update Personal Assistant

        Update Personal Assistant details for a specific user.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: Toggles feature.
        :type enabled: bool
        :param presence: Person's availability.
        :type presence: PersonalAssistantGetPresence
        :param until_date_time: The date until which the personal assistant is active.
        :type until_date_time: Union[str, datetime]
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param transfer_number: Number to transfer to.
        :type transfer_number: str
        :param alerting: Alert type.
        :type alerting: PersonalAssistantGetAlerting
        :param alert_me_first_number_of_rings: Number of rings for alert type: ALERT_ME_FIRST; available range is 2-20.
        :type alert_me_first_number_of_rings: int
        :param org_id: Update Personal Assistant details for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if presence is not None:
            body['presence'] = enum_str(presence)
        if until_date_time is not None:
            body['untilDateTime'] = until_date_time
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        if transfer_number is not None:
            body['transferNumber'] = transfer_number
        if alerting is not None:
            body['alerting'] = enum_str(alerting)
        if alert_me_first_number_of_rings is not None:
            body['alertMeFirstNumberOfRings'] = alert_me_first_number_of_rings
        url = self.ep(f'telephony/config/people/{person_id}/features/personalAssistant')
        super().put(url, params=params, json=body)

    def get_list_of_available_features(self, person_id: str, name: str = None, phone_number: str = None,
                                       extension: str = None, order: str = None, org_id: str = None,
                                       **params) -> Generator[UserModeManagementAvailableFeaturesObject, None, None]:
        """
        Retrieve the List of Available Features

        Retrieve a list of feature identifiers that can be assigned to a user for `Mode Management`. Feature
        identifiers reference feature instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.

        Features with mode-based call forwarding enabled can be assigned to a user for `Mode Management`.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param name: List features whose `name` contains this string.
        :type name: str
        :param phone_number: List features whose phoneNumber contains this matching string.
        :type phone_number: str
        :param extension: List features whose `extension` contains this matching string.
        :type extension: str
        :param order: Sort the list of features based on `name`, `phoneNumber`, or `extension`, either `asc`, or
            `desc`.
        :type order: str
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :return: Generator yielding :class:`UserModeManagementAvailableFeaturesObject` instances
        """
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if order is not None:
            params['order'] = order
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/modeManagement/availableFeatures')
        return self.session.follow_pagination(url=url, model=UserModeManagementAvailableFeaturesObject, item_key='features', params=params)

    def get_list_of_features_assigned_to_auser_mode_management(self, person_id: str,
                                                               org_id: str = None) -> list[UserModeManagementFeatureObject]:
        """
        Retrieve the List of Features Assigned to a User for Mode Management

        Retrieve a list of feature identifiers that are already assigned to a user for `Mode Management`. Feature
        identifiers reference feature instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.
        A maximum of 50 features can be assigned to a user for `Mode Management`.

        Features with mode-based call forwarding enabled can be assigned to a user for `Mode Management`.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :rtype: list[UserModeManagementFeatureObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/modeManagement/features')
        data = super().get(url, params=params)
        r = TypeAdapter(list[UserModeManagementFeatureObject]).validate_python(data['features'])
        return r

    def assign_list_of_features_to_auser_mode_management(self, person_id: str, feature_ids: list[str],
                                                         org_id: str = None):
        """
        Assign a List of Features to a User for Mode Management

        Assign a user a list of feature identifiers for `Mode Management`. Feature identifiers reference feature
        instances like `Auto Attendants`, `Call Queues`, and `Hunt Groups`.
        A maximum of 50 features can be assigned to a user for `Mode Management`.

        Updating mode management settings for a user requires a full, or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the user.
        :type person_id: str
        :param feature_ids: Array of feature IDs.
        :type feature_ids: list[str]
        :param org_id: Retrieve features list from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['featureIds'] = feature_ids
        url = self.ep(f'telephony/config/people/{person_id}/modeManagement/features')
        super().put(url, params=params, json=body)

    def retrieve_music_on_hold_settings_for_person(self, person_id: str, org_id: str = None) -> GetMusicOnHoldObject:
        """
        Retrieve Music On Hold Settings for a Person

        Retrieve the person's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving a person's music on hold settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

    def configure_music_on_hold_settings_for_person(self, person_id: str, moh_enabled: bool = None,
                                                    greeting: GetMusicOnHoldObjectGreeting = None,
                                                    audio_announcement_file: AudioAnnouncementFileGetObject = None,
                                                    org_id: str = None):
        """
        Configure Music On Hold Settings for a Person

        Configure a person's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold settings for a person, music on hold setting must be enabled for this location.

        Updating a person's music on hold settings requires a full or user administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param moh_enabled: Music on hold is enabled or disabled for the person.
        :type moh_enabled: bool
        :param greeting: Greeting type for the person.
        :type greeting: GetMusicOnHoldObjectGreeting
        :param audio_announcement_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_announcement_file: AudioAnnouncementFileGetObject
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if moh_enabled is not None:
            body['mohEnabled'] = moh_enabled
        if greeting is not None:
            body['greeting'] = enum_str(greeting)
        if audio_announcement_file is not None:
            body['audioAnnouncementFile'] = audio_announcement_file.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/musicOnHold')
        super().put(url, params=params, json=body)

    def assign_or_unassign_numbers_to_aperson(self, person_id: str, phone_numbers: list[PhoneNumber],
                                              enable_distinctive_ring_pattern: bool = None, org_id: str = None):
        """
        Assign or Unassign numbers to a person

        Assign or unassign alternate phone numbers to a person.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Assigning or unassigning an alternate phone number to a person requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identitfier of the person.
        :type person_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: list[PhoneNumber]
        :param enable_distinctive_ring_pattern: Enables a distinctive ring pattern for the person.
        :type enable_distinctive_ring_pattern: bool
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enable_distinctive_ring_pattern is not None:
            body['enableDistinctiveRingPattern'] = enable_distinctive_ring_pattern
        body['phoneNumbers'] = TypeAdapter(list[PhoneNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/people/{person_id}/numbers')
        super().put(url, params=params, json=body)

    def delete_access_codes_for_person(self, person_id: str, org_id: str = None):
        """
        Delete Access Codes for a Person

        Deletes all Access codes for the person.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def retrieve_access_codes_for_person(self, person_id: str,
                                         org_id: str = None) -> UserPlaceAuthorizationCodeListGet:
        """
        Retrieve Access Codes for a Person

        Retrieve the person's access codes.

        Access codes are used to bypass permissions.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`UserPlaceAuthorizationCodeListGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = UserPlaceAuthorizationCodeListGet.model_validate(data)
        return r

    def create_access_codes_for_person(self, person_id: str, code: str, description: str, org_id: str = None):
        """
        Create Access Codes for a Person

        Create new Access codes for the person.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param code: An access code.
        :type code: str
        :param description: The description of the access code.
        :type description: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['code'] = code
        body['description'] = description
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def modify_access_codes_for_person(self, person_id: str, use_custom_access_codes: bool = None,
                                       delete_codes: list[str] = None, org_id: str = None):
        """
        Modify Access Codes for a Person

        Modify a person's access codes.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param use_custom_access_codes: When `true`, use custom settings for the access codes category of outgoing call
            permissions.
        :type use_custom_access_codes: bool
        :param delete_codes: Access codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_access_codes is not None:
            body['useCustomAccessCodes'] = use_custom_access_codes
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def retrieve_transfer_numbers_for_person(self, person_id: str, org_id: str = None) -> TransferNumberGet:
        """
        Retrieve Transfer Numbers for a Person

        Retrieve the person's transfer numbers.

        When calling a specific call type, this person will be automatically transferred to another number. The person
        assigned the Auto Transfer Number can then approve the call and send it through or reject the call type. You
        can add up to 3 numbers.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`TransferNumberGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = TransferNumberGet.model_validate(data)
        return r

    def modify_transfer_numbers_for_person(self, person_id: str, use_custom_transfer_numbers: bool,
                                           auto_transfer_number1: str = None, auto_transfer_number2: str = None,
                                           auto_transfer_number3: str = None, org_id: str = None):
        """
        Modify Transfer Numbers for a Person

        Modify a person's transfer numbers.

        When calling a specific call type, this person will be automatically transferred to another number. The person
        assigned the Auto Transfer Number can then approve the call and send it through or reject the call type. You
        can add up to 3 numbers.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param use_custom_transfer_numbers: When `true`, use custom settings for the transfer numbers category of
            outgoing call permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this person will be automatically transferred
            to another number. `autoTransferNumber1` will be used when the associated calling permission action is set
            to `TRANSFER_NUMBER_1`.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this person will be automatically transferred
            to another number. `autoTransferNumber2` will be used when the associated calling permission action is set
            to `TRANSFER_NUMBER_2`.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this person will be automatically transferred
            to another number. `autoTransferNumber3` will be used when the associated calling permission action is set
            to `TRANSFER_NUMBER_3`.
        :type auto_transfer_number3: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['useCustomTransferNumbers'] = use_custom_transfer_numbers
        if auto_transfer_number1 is not None:
            body['autoTransferNumber1'] = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body['autoTransferNumber2'] = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body['autoTransferNumber3'] = auto_transfer_number3
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def delete_all_digit_patterns_person(self, person_id: str, org_id: str = None):
        """
        Delete all digit patterns for a Person.

        Digit patterns are used to bypass permissions.

        Deleting the digit patterns requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

    def retrieve_digit_patterns_for_person(self, person_id: str,
                                           org_id: str = None) -> UserOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve Digit Patterns for a Person

        Retrieve the person's digit patterns.

        Digit patterns are used to bypass permissions.

        Retrieving digit patterns requires a full or user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = UserOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def create_digit_patterns_for_person(self, person_id: str, name: str, pattern: str, action: Action,
                                         transfer_enabled: bool, org_id: str = None) -> str:
        """
        Create Digit Patterns for a Person

        Create a new digit pattern for the given person.

        Digit patterns are used to bypass permissions.

        Creating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: Action
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['pattern'] = pattern
        body['action'] = enum_str(action)
        body['transferEnabled'] = transfer_enabled
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_digit_pattern_category_control_settings_for_person(self, person_id: str,
                                                                  use_custom_digit_patterns: bool = None,
                                                                  org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for a Person

        Modifies whether this user uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or user or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def delete_adigit_pattern_person(self, person_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a digit pattern for a Person.

        Digit patterns are used to bypass permissions.

        Deleting the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def retrieve_digit_pattern_details_person(self, person_id: str, digit_pattern_id: str,
                                              org_id: str = None) -> UserDigitPatternObject:
        """
        Retrieve Digit Pattern Details for a Person

        Retrieve the digit pattern details for a person.

        Digit patterns are used to bypass permissions.

        Retrieving the digit pattern details requires a full or user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`UserDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = UserDigitPatternObject.model_validate(data)
        return r

    def modify_digit_pattern_for_person(self, person_id: str, digit_pattern_id: str, name: str = None,
                                        pattern: str = None, action: Action = None, transfer_enabled: bool = None,
                                        org_id: str = None):
        """
        Modify a digit pattern for a Person.

        Digit patterns are used to bypass permissions.

        Updating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: Action
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if pattern is not None:
            body['pattern'] = pattern
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        url = self.ep(f'telephony/config/people/{person_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def get_preferred_answer_endpoint(self, person_id: str, org_id: str = None) -> EndpointInformation:
        """
        Get Preferred Answer Endpoint

        Get the person's preferred answer endpoint and the list of endpoints available for selection. The preferred
        answer endpoint is null if one has not been selected. The list of endpoints is empty if the person has no
        endpoints assigned which support the preferred answer endpoint functionality. These endpoints can be used by
        the following Call Control API's that allow the person to specify an endpointId to use for the call:<br>

        + `/v1/telephony/calls/dial
        <https://developer.webex.com/docs/api/v1/call-controls/dial>`_<br>

        + `/v1/telephony/calls/retrieve
        <https://developer.webex.com/docs/api/v1/call-controls/retrieve>`_<br>

        + `/v1/telephony/calls/pickup
        <https://developer.webex.com/docs/api/v1/call-controls/pickup>`_<br>

        + `/v1/telephony/calls/barge-in
        <https://developer.webex.com/docs/api/v1/call-controls/barge-in>`_<br>

        + `/v1/telephony/calls/answer
        <https://developer.webex.com/docs/api/v1/call-controls/answer>`_<br>

        This API requires `spark:telephony_config_read` or `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`EndpointInformation`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
        data = super().get(url, params=params)
        r = EndpointInformation.model_validate(data)
        return r

    def modify_preferred_answer_endpoint(self, person_id: str, preferred_answer_endpoint_id: str, org_id: str = None):
        """
        Modify Preferred Answer Endpoint

        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the
        `preferredAnswerEndpointId` attribute must be set to null.<br>
        This API requires `spark:telephony_config_write` or `spark-admin:telephony_config_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param preferred_answer_endpoint_id: Person’s preferred answer endpoint.
        :type preferred_answer_endpoint_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['preferredAnswerEndpointId'] = preferred_answer_endpoint_id
        url = self.ep(f'telephony/config/people/{person_id}/preferredAnswerEndpoint')
        super().put(url, params=params, json=body)

    def get_person_secondary_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                     org_id: str = None,
                                                     **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a person's secondary phone number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/people/{person_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_user_selective_call_accept_criteria_list(self, person_id: str,
                                                     org_id: str = None) -> SelectiveAcceptCallGet:
        """
        Get the User’s Selective Call Accept Criteria List

        Retrieve selective call accept criteria list for a user.

        With the selective call accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveAcceptCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept')
        data = super().get(url, params=params)
        r = SelectiveAcceptCallGet.model_validate(data)
        return r

    def update_user_selective_call_accept_criteria(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Update User’s Selective Call Accept Criteria

        Modify selective call accept setting for a user.

        With the Selective Call accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param enabled: Boolean flag to enable/disable selective call accept.
        :type enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept')
        super().put(url, params=params, json=body)

    def create_criteria_to_user_selective_call_accept_service(self, person_id: str,
                                                              calls_from: CallsFromSelectiveAccept,
                                                              accept_enabled: bool, schedule_name: str = None,
                                                              schedule_type: ScheduleType = None,
                                                              schedule_level: ScheduleLevel = None,
                                                              anonymous_callers_enabled: bool = None,
                                                              unavailable_callers_enabled: bool = None,
                                                              phone_numbers: list[str] = None,
                                                              org_id: str = None) -> str:
        """
        Create a Criteria to the User’s Selective Call Accept Service

        Add a criteria to the user's selective call accept service.

        With the Selective Call accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calls_from: Accept calls selection.
        :type calls_from: CallsFromSelectiveAccept
        :param accept_enabled: Boolean flag indicating if selective call accept is enabled.
        :type accept_enabled: bool
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: The schedule type.
        :type schedule_type: ScheduleType
        :param schedule_level: schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Boolean flag indicating if calls from custom numbers, private numbers are
            enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Boolean flag indicating if calls from custom numbers, unavailable numbers
            are enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions, phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['acceptEnabled'] = accept_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_criteria_from_user_selective_call_accept_service(self, person_id: str, id: str, org_id: str = None):
        """
        Delete a Criteria From the User’s Selective Call Accept service

        Delete a criteria from the user's selective call accept criteria list.

        With the Selective Call Accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept/criteria/{id}')
        super().delete(url, params=params)

    def get_criteria_for_user_selective_call_accept_service(self, person_id: str, id: str,
                                                            org_id: str = None) -> SelectiveAcceptCallCriteriaGet:
        """
        Get a Criteria for the User’s Selective Call Accept Service

        Get the criteria details for the user's selective call accept service.

        With the Selective Call accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveAcceptCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept/criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveAcceptCallCriteriaGet.model_validate(data)
        return r

    def modify_criteria_from_user_selective_call_accept_service(self, person_id: str, id: str,
                                                                calls_from: CallsFromSelectiveAccept,
                                                                accept_enabled: bool, schedule_name: str = None,
                                                                schedule_type: ScheduleType = None,
                                                                schedule_level: ScheduleLevel = None,
                                                                anonymous_callers_enabled: bool = None,
                                                                unavailable_callers_enabled: bool = None,
                                                                phone_numbers: list[str] = None, org_id: str = None):
        """
        Modify a Criteria From the User’s Selective Call Accept Service

        Modify a criteria for the user's selective call accept service.

        With the Selective Call Accept feature, you can create different rules to accept specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param calls_from: Accept calls from selected.
        :type calls_from: CallsFromSelectiveAccept
        :param accept_enabled: Boolean flag to enable/disable the selective accept criteria.
        :type accept_enabled: bool
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: Schedule Type.
        :type schedule_type: ScheduleType
        :param schedule_level: schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Boolean flag indicating if calls from custom numbers, private numbers are
            enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Boolean flag indicating if calls from custom numbers, unavailable numbers
            are enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['acceptEnabled'] = accept_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveAccept/criteria/{id}')
        super().put(url, params=params, json=body)

    def get_user_selective_call_forwarding(self, person_id: str, org_id: str = None) -> SelectiveForwardCallGet:
        """
        Get the User’s Selective Call Forwarding

        Retrieve selective call forwarding criteria for a user.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward')
        data = super().get(url, params=params)
        r = SelectiveForwardCallGet.model_validate(data)
        return r

    def update_user_selective_call_forwarding_criteria_list(self, person_id: str, enabled: bool,
                                                            default_phone_number_to_forward: str = None,
                                                            ring_reminder_enabled: bool = None,
                                                            send_to_voicemail_enabled: bool = None,
                                                            org_id: str = None):
        """
        Update User’s Selective Call Forwarding Criteria List

        Modify selective call forwarding setting for a user.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param enabled: Boolean flag to enable/disable selective call forwarding.
        :type enabled: bool
        :param default_phone_number_to_forward: Forward to default number. This field is mandatory when `enabled` is
            true and `sendToVoicemailEnabled` is true.
        :type default_phone_number_to_forward: str
        :param ring_reminder_enabled: Boolean flag to enable/disable ring reminder.
        :type ring_reminder_enabled: bool
        :param send_to_voicemail_enabled: Boolean flag to enable/disable sending calls to voicemail.
        :type send_to_voicemail_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if default_phone_number_to_forward is not None:
            body['defaultPhoneNumberToForward'] = default_phone_number_to_forward
        if ring_reminder_enabled is not None:
            body['ringReminderEnabled'] = ring_reminder_enabled
        if send_to_voicemail_enabled is not None:
            body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward')
        super().put(url, params=params, json=body)

    def create_criteria_to_user_selective_call_forwarding_service(self, person_id: str, forward_to_phone_number: str,
                                                                  send_to_voicemail_enabled: bool,
                                                                  calls_from: CallsFromSelectiveReject,
                                                                  schedule_name: str = None,
                                                                  schedule_type: ScheduleType = None,
                                                                  schedule_level: ScheduleLevel = None,
                                                                  anonymous_callers_enabled: bool = None,
                                                                  unavailable_callers_enabled: bool = None,
                                                                  phone_numbers: list[str] = None,
                                                                  forward_enabled: bool = None,
                                                                  org_id: str = None) -> str:
        """
        Create a Criteria to the User’s Selective Call Forwarding Service

        Add a criteria to the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param forward_to_phone_number: Number to which calls needs to be forwarded.
        :type forward_to_phone_number: str
        :param send_to_voicemail_enabled: Boolean flag to enable/disable sending calls to voicemail.
        :type send_to_voicemail_enabled: bool
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFromSelectiveReject
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: The type of schedule.
        :type schedule_type: ScheduleType
        :param schedule_level: schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Calls From custom numbers, private number enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Calls From custom numbers, unavailable number enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param forward_enabled: Boolean flag to enable/disable selective call forward.
        :type forward_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['forwardToPhoneNumber'] = forward_to_phone_number
        body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_criteria_from_user_selective_call_forwarding_service(self, person_id: str, id: str, org_id: str = None):
        """
        Delete a Criteria From the User’s Selective Call Forwarding Service

        Delete a criteria from the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward/criteria/{id}')
        super().delete(url, params=params)

    def get_criteria_for_user_selective_call_forwarding_service(self, person_id: str, id: str,
                                                                org_id: str = None) -> SelectiveForwardCallCriteriaGet:
        """
        Get a Criteria for the User’s Selective Call Forwarding Service

        Get the criteria details for the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward/criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveForwardCallCriteriaGet.model_validate(data)
        return r

    def modify_criteria_for_user_selective_call_forwarding_service(self, person_id: str, id: str,
                                                                   forward_to_phone_number: str,
                                                                   send_to_voicemail_enabled: bool,
                                                                   calls_from: CallsFromSelectiveReject,
                                                                   schedule_name: str = None,
                                                                   schedule_type: ScheduleType = None,
                                                                   schedule_level: ScheduleLevel = None,
                                                                   anonymous_callers_enabled: bool = None,
                                                                   unavailable_callers_enabled: bool = None,
                                                                   phone_numbers: list[str] = None,
                                                                   forward_enabled: bool = None, org_id: str = None):
        """
        Modify a Criteria for the User’s Selective Call Forwarding Service

        Modify a criteria for the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param forward_to_phone_number: Number to which calls needs to be forwarded.
        :type forward_to_phone_number: str
        :param send_to_voicemail_enabled: Boolean flag to enable/disable sending calls to voicemail.
        :type send_to_voicemail_enabled: bool
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFromSelectiveReject
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: The type of schedule.
        :type schedule_type: ScheduleType
        :param schedule_level: The schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Boolean flag indicating if calls from custom numbers, private numbers are
            enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Boolean flag indicating if calls from custom numbers, unavailable numbers
            are enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param forward_enabled: Boolean flag to enable/disable selective call forwarding.
        :type forward_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['forwardToPhoneNumber'] = forward_to_phone_number
        body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveForward/criteria/{id}')
        super().put(url, params=params, json=body)

    def get_user_selective_call_rejection_criteria_listing(self, person_id: str,
                                                           org_id: str = None) -> SelectiveRejectCallGet:
        """
        Get the User’s Selective Call Rejection Criteria Listing

        Retrieve selective call rejection criteria for a user.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject')
        data = super().get(url, params=params)
        r = SelectiveRejectCallGet.model_validate(data)
        return r

    def update_user_selective_call_rejection_criteria_list(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Update User’s Selective Call Rejection Criteria List

        Modify selective call rejection setting for a user.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param enabled: Boolean flag to enable/disable Selective call reject.
        :type enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject')
        super().put(url, params=params, json=body)

    def create_criteria_to_user_selective_call_rejection_service(self, person_id: str, calls_from: CallsFrom,
                                                                 reject_enabled: bool, schedule_name: str = None,
                                                                 schedule_type: ScheduleType = None,
                                                                 schedule_level: ScheduleLevel = None,
                                                                 anonymous_callers_enabled: bool = None,
                                                                 unavailable_callers_enabled: bool = None,
                                                                 phone_numbers: list[str] = None,
                                                                 org_id: str = None) -> str:
        """
        Create a Criteria to the User’s Selective Call Rejection Service

        Add a criteria to the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFrom
        :param reject_enabled: Boolean flag to enable/disable rejection.
        :type reject_enabled: bool
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: The schedule type.
        :type schedule_type: ScheduleType
        :param schedule_level: schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Boolean flag indicating if calls from custom numbers, private numbers are
            enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Boolean flag indicating if calls from custom numbers, unavailable numbers
            are enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_criteria_from_user_selective_call_rejection_service(self, person_id: str, id: str, org_id: str = None):
        """
        Delete a Criteria From the User’s Selective Call Rejection Service

        Delete a criteria from the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject/criteria/{id}')
        super().delete(url, params=params)

    def get_criteria_for_user_selective_call_rejection_service(self, person_id: str, id: str,
                                                               org_id: str = None) -> SelectiveRejectCallCriteriaGet:
        """
        Get a Criteria for the User’s Selective Call Rejection Service

        Get a criteria for the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject/criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveRejectCallCriteriaGet.model_validate(data)
        return r

    def modify_criteria_for_user_selective_call_rejection_service(self, person_id: str, id: str, calls_from: CallsFrom,
                                                                  reject_enabled: bool, schedule_name: str = None,
                                                                  schedule_type: ScheduleType = None,
                                                                  schedule_level: ScheduleLevel = None,
                                                                  anonymous_callers_enabled: bool = None,
                                                                  unavailable_callers_enabled: bool = None,
                                                                  phone_numbers: list[str] = None,
                                                                  org_id: str = None):
        """
        Modify a Criteria for the User’s Selective Call Rejection Service

        Modify a criteria for the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFrom
        :param reject_enabled: Boolean flag to enable/disable rejection.
        :type reject_enabled: bool
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: schedule type.
        :type schedule_type: ScheduleType
        :param schedule_level: schedule level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Boolean flag indicating if calls from custom numbers, private numbers are
            enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Boolean flag indicating if calls from custom numbers, unavailable numbers
            are enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'telephony/config/people/{person_id}/selectiveReject/criteria/{id}')
        super().put(url, params=params, json=body)

    def get_person_msteams_settings(self, person_id: str, org_id: str = None) -> GetUserMSTeamsSettingsObject:
        """
        Retrieve a Person's MS Teams Settings

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Retrieve a person's MS Teams settings.

        At a person level, MS Teams settings allow access to retrieving the `HIDE WEBEX APP` and `PRESENCE SYNC`
        settings.

        To retrieve a person's MS Teams settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`GetUserMSTeamsSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/settings/msTeams')
        data = super().get(url, params=params)
        r = GetUserMSTeamsSettingsObject.model_validate(data)
        return r

    def configure_person_msteams_setting(self, person_id: str,
                                         setting_name: ModifyUserMSTeamsSettingsObjectSettingName, value: bool,
                                         org_id: str = None):
        """
        Configure a Person's MS Teams Setting

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Configure a Person's MS Teams setting.

        MS Teams settings can be configured at the person level.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting_name: The enum value to be set to `HIDE_WEBEX_APP`.
        :type setting_name: ModifyUserMSTeamsSettingsObjectSettingName
        :param value: The boolean value to update the `HIDE_WEBEX_APP` setting, either `true` or `false`. Set to `null`
            to delete the `HIDE_WEBEX_APP` setting.
        :type value: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['settingName'] = enum_str(setting_name)
        body['value'] = value
        url = self.ep(f'telephony/config/people/{person_id}/settings/msTeams')
        super().put(url, params=params, json=body)

    def get_feature_access_settings_person(self, person_id: str) -> UserSettingsPermissionsGet:
        """
        Read Feature Access Settings for a Person

        Read the feature access configuration for the current user within the organization. It allows administrators to
        read the telephony settings, including device and location configurations, specific to that user’s role and
        access privileges. This API is useful for managing and verifying user-specific feature access within the
        broader telephony system.

        The feature is part of the organization’s telephony configuration management. It provides insight into the
        settings and permissions that control how telephony services are assigned and configured for individual users.
        This functionality is available through the Control Hub and allows for the management of user access to
        various telephony-related features.

        To access this API, the user must possess a full, or read-only administrator role. The authentication token
        used must include the `spark-admin:telephony_config_read` scope, granting the necessary permissions to read
        the telephony configuration for the user in question.

        :param person_id: User ID of the Organization.
        :type person_id: str
        :rtype: :class:`UserSettingsPermissionsGet`
        """
        url = self.ep(f'telephony/config/people/{person_id}/settings/permissions')
        data = super().get(url)
        r = UserSettingsPermissionsGet.model_validate(data)
        return r

    def modify_person_feature_access_configuration(self, person_id: str, anonymous_call_rejection: AccessLevel = None,
                                                   barge_in: AccessLevel = None, block_caller_id: AccessLevel = None,
                                                   call_forwarding: AccessLevel = None,
                                                   call_waiting: AccessLevel = None, call_notify: AccessLevel = None,
                                                   connected_line_identity: AccessLevel = None,
                                                   executive: AccessLevel = None, hoteling: AccessLevel = None,
                                                   priority_alert: AccessLevel = None,
                                                   selectively_accept_calls: AccessLevel = None,
                                                   selectively_reject_calls: AccessLevel = None,
                                                   selectively_forward_calls: AccessLevel = None,
                                                   sequential_ring: AccessLevel = None,
                                                   simultaneous_ring: AccessLevel = None,
                                                   single_number_reach: AccessLevel = None,
                                                   voicemail: AccessLevel = None,
                                                   send_calls_to_voicemail: AccessLevel = None,
                                                   voicemail_email_copy: AccessLevel = None,
                                                   voicemail_fax_messaging: AccessLevel = None,
                                                   voicemail_message_storage: AccessLevel = None,
                                                   voicemail_notifications: AccessLevel = None,
                                                   voicemail_transfer_number: AccessLevel = None,
                                                   generate_activation_code: AccessLevel = None,
                                                   voicemail_download: AccessLevel = None):
        """
        Update a Person’s Feature Access Configuration

        Update the feature access configuration for the current user within the organization. It enables administrators
        to modify the telephony settings, including device and location configurations, specific to the user’s role
        and access privileges. This API is useful for making adjustments to user-specific feature access within the
        telephony system.

        The feature is part of the organization’s telephony configuration management. It provides control over the
        settings and permissions that govern how telephony services are assigned and configured for individual users.
        This functionality is available through the Control Hub and enables the modification of user access to various
        telephony-related features.

        To use this API, an administrator must authenticate with a full, or device administrator auth token. The
        authentication token used must include the `spark-admin:telephony_config_write` scope, granting the necessary
        permissions to update the telephony configuration for the user in question.

        :param person_id: User ID of the Organization.
        :type person_id: str
        :param anonymous_call_rejection: Set whether end users have access to make changes to their `Anonymous call
            rejection` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type anonymous_call_rejection: AccessLevel
        :param barge_in: Set whether end users have access to make changes to their `Barge In` feature via User Hub, or
            other clients (Webex, IP phone, etc.).
        :type barge_in: AccessLevel
        :param block_caller_id: Set whether end users have access to make changes to their `Block caller ID` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type block_caller_id: AccessLevel
        :param call_forwarding: Set whether end users have access to make changes to their `Call forwarding` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type call_forwarding: AccessLevel
        :param call_waiting: Set whether end users have access to make changes to their `Call waiting` feature via User
            Hub, or other clients (Webex, IP phone, etc.).
        :type call_waiting: AccessLevel
        :param call_notify: Set whether end users have access to make changes to their `Call notify` feature via User
            Hub, or other clients (Webex, IP phone, etc.).
        :type call_notify: AccessLevel
        :param connected_line_identity: Set whether end users have access to make changes to their `Connected line
            identity` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type connected_line_identity: AccessLevel
        :param executive: Set whether end users have access to make changes to their `Executive/Executive assistant`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type executive: AccessLevel
        :param hoteling: Set whether end users have access to make changes to their `Hoteling` feature via User Hub, or
            other clients (Webex, IP phone, etc.).
        :type hoteling: AccessLevel
        :param priority_alert: Set whether end users have access to make changes to their `Priority alert` feature via
            User Hub, or other clients (Webex, IP phone, etc.).
        :type priority_alert: AccessLevel
        :param selectively_accept_calls: Set whether end users have access to make changes to their `Selectively accept
            calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_accept_calls: AccessLevel
        :param selectively_reject_calls: Set whether end users have access to make changes to their `Selectively reject
            calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_reject_calls: AccessLevel
        :param selectively_forward_calls: Set whether end users have access to make changes to their `Selectively
            forward calls` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type selectively_forward_calls: AccessLevel
        :param sequential_ring: Set whether end users have access to make changes to their `Sequential ring` feature
            via User Hub, or other clients (Webex, IP phone, etc.).
        :type sequential_ring: AccessLevel
        :param simultaneous_ring: Set whether end users have access to make changes to their `Simultaneous ring`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type simultaneous_ring: AccessLevel
        :param single_number_reach: Set whether end users have access to make changes to their `Single number reach`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type single_number_reach: AccessLevel
        :param voicemail: Set whether end users have access to make changes to their `Voicemail feature` feature via
            User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail: AccessLevel
        :param send_calls_to_voicemail: Set whether end users have access to make changes to their `Send calls to
            voicemail` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type send_calls_to_voicemail: AccessLevel
        :param voicemail_email_copy: Set whether end users have access to make changes to their `Email a copy of the
            voicemail message` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_email_copy: AccessLevel
        :param voicemail_fax_messaging: Set whether end users have access to make changes to their `Fax messaging`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_fax_messaging: AccessLevel
        :param voicemail_message_storage: Set whether end users have access to make changes to their `Message storage`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_message_storage: AccessLevel
        :param voicemail_notifications: Set whether end users have access to make changes to their `Notifications`
            feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_notifications: AccessLevel
        :param voicemail_transfer_number: Set whether end users have access to make changes to their `Transfer on '0'
            to another number.` feature via User Hub, or other clients (Webex, IP phone, etc.).
        :type voicemail_transfer_number: AccessLevel
        :param generate_activation_code: Set whether end users have access to make changes to their `Allow End User to
            Generate Activation Codes & Delete their Phones` feature via User Hub, or other clients (Webex, IP phone,
            etc.).
        :type generate_activation_code: AccessLevel
        :param voicemail_download: Set whether end users have access to download voicemail via User Hub, or other
            clients (Webex, etc.).
        :type voicemail_download: AccessLevel
        :rtype: None
        """
        body = dict()
        if anonymous_call_rejection is not None:
            body['anonymousCallRejection'] = enum_str(anonymous_call_rejection)
        if barge_in is not None:
            body['bargeIn'] = enum_str(barge_in)
        if block_caller_id is not None:
            body['blockCallerId'] = enum_str(block_caller_id)
        if call_forwarding is not None:
            body['callForwarding'] = enum_str(call_forwarding)
        if call_waiting is not None:
            body['callWaiting'] = enum_str(call_waiting)
        if call_notify is not None:
            body['callNotify'] = enum_str(call_notify)
        if connected_line_identity is not None:
            body['connectedLineIdentity'] = enum_str(connected_line_identity)
        if executive is not None:
            body['executive'] = enum_str(executive)
        if hoteling is not None:
            body['hoteling'] = enum_str(hoteling)
        if priority_alert is not None:
            body['priorityAlert'] = enum_str(priority_alert)
        if selectively_accept_calls is not None:
            body['selectivelyAcceptCalls'] = enum_str(selectively_accept_calls)
        if selectively_reject_calls is not None:
            body['selectivelyRejectCalls'] = enum_str(selectively_reject_calls)
        if selectively_forward_calls is not None:
            body['selectivelyForwardCalls'] = enum_str(selectively_forward_calls)
        if sequential_ring is not None:
            body['sequentialRing'] = enum_str(sequential_ring)
        if simultaneous_ring is not None:
            body['simultaneousRing'] = enum_str(simultaneous_ring)
        if single_number_reach is not None:
            body['singleNumberReach'] = enum_str(single_number_reach)
        if voicemail is not None:
            body['voicemail'] = enum_str(voicemail)
        if send_calls_to_voicemail is not None:
            body['sendCallsToVoicemail'] = enum_str(send_calls_to_voicemail)
        if voicemail_email_copy is not None:
            body['voicemailEmailCopy'] = enum_str(voicemail_email_copy)
        if voicemail_fax_messaging is not None:
            body['voicemailFaxMessaging'] = enum_str(voicemail_fax_messaging)
        if voicemail_message_storage is not None:
            body['voicemailMessageStorage'] = enum_str(voicemail_message_storage)
        if voicemail_notifications is not None:
            body['voicemailNotifications'] = enum_str(voicemail_notifications)
        if voicemail_transfer_number is not None:
            body['voicemailTransferNumber'] = enum_str(voicemail_transfer_number)
        if generate_activation_code is not None:
            body['generateActivationCode'] = enum_str(generate_activation_code)
        if voicemail_download is not None:
            body['voicemailDownload'] = enum_str(voicemail_download)
        url = self.ep(f'telephony/config/people/{person_id}/settings/permissions')
        super().put(url, json=body)

    def reset_person_feature_access_config_to_org_default(self, person_id: str):
        """
        Reset a Person’s Feature Access Configuration to the Organization’s Default Settings

        Reset of a user’s feature access configuration to the organization’s default settings. It ensures that any
        specific feature configurations set by an administrator for an individual user are overridden and replaced
        with the global configuration of the organization. This process helps to maintain consistency in feature
        access across all users, especially when administrators want to ensure that a user is subject to the
        organization's global settings rather than personalized settings.

        The overall feature, managed through the organization's Control Hub, involves the configuration and
        customization of feature access for users. Administrators can tailor these settings to individual users based
        on their roles or needs, but sometimes a global reset to the default configuration is necessary. The reset API
        simplifies this by programmatically resetting a user’s feature access, which can be crucial when managing
        large teams or updating organizational policies that affect user privileges across multiple devices or
        locations.

        .To use this API, an administrator must authenticate with a full, or device administrator auth token. This
        ensures the individual has the necessary privileges to make changes to user configurations. Furthermore, the
        authentication token used must include the `spark-admin:telephony_config_write` scope, which grants the
        required permissions to modify the telephony configuration for the user. This combination of roles and scopes
        ensures that only authorized administrators can reset the feature access configuration.

        :param person_id: User ID of the Organization.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'telephony/config/people/{person_id}/settings/permissions/actions/reset/invoke')
        super().post(url)

    def modify_person_voicemail_passcode(self, person_id: str, passcode: str, org_id: str = None):
        """
        Modify a person's voicemail passcode.

        Modifying a person's voicemail passcode requires a full administrator, user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Modify voicemail passcode for this person.
        :type person_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'telephony/config/people/{person_id}/voicemail/passcode')
        super().put(url, params=params, json=body)

    def list_messages(self) -> list[VoiceMessageDetails]:
        """
        List Messages

        Get the list of all voicemail messages for the user.

        :rtype: list[VoiceMessageDetails]
        """
        url = self.ep('telephony/voiceMessages')
        data = super().get(url)
        r = TypeAdapter(list[VoiceMessageDetails]).validate_python(data['items'])
        return r

    def mark_as_read(self, message_id: str = None):
        """
        Mark As Read

        Update the voicemail message(s) as read for the user.

        If the `messageId` is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the `messageId` is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        :rtype: None
        """
        body = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('telephony/voiceMessages/markAsRead')
        super().post(url, json=body)

    def mark_as_unread(self, message_id: str = None):
        """
        Mark As Unread

        Update the voicemail message(s) as unread for the user.

        If the `messageId` is provided, then only mark that message as unread.  Otherwise, all messages for the user
        are marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the `messageId` is
            not provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        :rtype: None
        """
        body = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('telephony/voiceMessages/markAsUnread')
        super().post(url, json=body)

    def get_message_summary(self) -> GetMessageSummaryResponse:
        """
        Get Message Summary

        Get a summary of the voicemail messages for the user.

        :rtype: :class:`GetMessageSummaryResponse`
        """
        url = self.ep('telephony/voiceMessages/summary')
        data = super().get(url)
        r = GetMessageSummaryResponse.model_validate(data)
        return r

    def delete_message(self, message_id: str):
        """
        Delete Message

        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        :rtype: None
        """
        url = self.ep(f'telephony/voiceMessages/{message_id}')
        super().delete(url)
