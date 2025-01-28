from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Action', 'AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
           'AudioAnnouncementFileGetObjectMediaFileType', 'AuthorizationCode', 'CLIDPolicySelection',
           'CallForwardingAlwaysGet', 'CallForwardingBusyGet', 'CallForwardingNoAnswerGet',
           'CallForwardingPlaceSettingGet', 'CallWaiting', 'CallingPermission', 'CallingPermissionAction',
           'CallingPermissionCallType', 'CallsFromTypeForSelectiveForward', 'ExternalCallerIdNamePolicy',
           'GetMusicOnHoldObject', 'InterceptAnnouncementsGet', 'InterceptAnnouncementsGetGreeting',
           'InterceptAnnouncementsPatch', 'InterceptGet', 'InterceptIncomingGet', 'InterceptIncomingGetType',
           'InterceptIncomingPatch', 'InterceptNumberGet', 'InterceptOutGoingGet', 'InterceptOutGoingGetType',
           'ModifyCallingPermission', 'ModifyPlaceCallForwardSettings', 'MonitoredElementCallParkExtension',
           'MonitoredElementItem', 'MonitoredElementUser', 'MonitoredElementUserType', 'MonitoredPersonObject',
           'NumberOwnerObject', 'NumberOwnerType', 'PhoneNumber', 'PhoneNumbers', 'PlaceCallerIdGet',
           'PlaceGetNumbersResponse', 'PlacePriorityAlertCriteriaGet', 'PlaceSelectiveAcceptCallCriteriaGet',
           'PlaceSelectiveForwardCallCriteriaGet', 'PlaceSelectiveRejectCallCriteriaGet', 'PriorityAlertCriteria',
           'PriorityAlertGet', 'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo',
           'RingPattern', 'STATE', 'SelectiveAcceptCallCriteria', 'SelectiveAcceptCallGet',
           'SelectiveForwardCallCriteria', 'SelectiveForwardCallGet', 'SelectiveRejectCallCallsFromType',
           'SelectiveRejectCallGet', 'SelectiveRejectCallSource', 'SelectiveRejectCriteria', 'SequentialRingCriteria',
           'SequentialRingCriteriaGet', 'SequentialRingCriteriaGetCallsFrom',
           'SequentialRingCriteriaGetScheduleLevel', 'SequentialRingCriteriaGetScheduleType', 'SequentialRingGet',
           'SequentialRingNumber', 'SimultaneousRingGet', 'SimultaneousRingNumberGet', 'Source',
           'SourceForSelectiveForward', 'TelephonyType', 'TransferNumberGet', 'UserBargeInGet',
           'UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls', 'UserDoNotDisturbGet',
           'UserInboundPermissionGet', 'UserInboundPermissionGetExternalTransfer', 'UserMonitoringGet',
           'UserNumberItem', 'UserOutgoingPermissionGet', 'VoicemailInfo', 'VoicemailInfoEmailCopyOfMessage',
           'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage', 'VoicemailInfoMessageStorageStorageType',
           'VoicemailInfoSendBusyCalls', 'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls',
           'VoicemailPutSendUnansweredCalls', 'WorkspaceAvailableNumberObject',
           'WorkspaceCallForwardAvailableNumberObject', 'WorkspaceCallSettingsApi', 'WorkspaceDigitPatternObject',
           'WorkspaceECBNAvailableNumberObject', 'WorkspaceECBNAvailableNumberObjectOwner',
           'WorkspaceECBNAvailableNumberObjectOwnerType', 'WorkspaceOutgoingPermissionDigitPatternGetListObject']


class AuthorizationCode(ApiModel):
    #: Access code.
    #: example: 4856
    code: Optional[str] = None
    #: The description of the access code.
    #: example: Marketing's access code
    description: Optional[str] = None


class CLIDPolicySelection(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the value from the customNumber field.
    custom = 'CUSTOM'


class CallForwardingAlwaysGet(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingBusyGet(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: +19075552859
    destination: Optional[str] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingNoAnswerGet(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: +19075552859
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 2
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 20
    system_max_number_of_rings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    #: example: True
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPlaceSettingGet(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingAlwaysGet] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the
    #: workspace is busy.
    busy: Optional[CallForwardingBusyGet] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingNoAnswerGet] = None


class CallWaiting(ApiModel):
    #: Call Waiting state.
    #: example: True
    enabled: Optional[bool] = None


class CallingPermissionCallType(str, Enum):
    #: Internal call type.
    internal_call = 'INTERNAL_CALL'
    #: Toll free call type.
    toll_free = 'TOLL_FREE'
    #: International call type.
    international = 'INTERNATIONAL'
    #: Operator Assisted call type.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Chargeable Directory Assisted call type.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Special Services I call type.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Special Services II call type.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Premium Services I call type.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Premium Services II call type.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: National call type.
    national = 'NATIONAL'


class CallingPermissionAction(str, Enum):
    #: The call type is allowed.
    allow = 'ALLOW'
    #: The call type is blocked.
    block = 'BLOCK'
    #: Access Code action for the specified call type.
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


class CallingPermission(ApiModel):
    #: Type of the outgoing call.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionCallType] = None
    #: Permission for call types.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: If `true`, allows a place to transfer or forward internal calls.
    #: example: True
    transfer_enabled: Optional[bool] = None
    #: The call restriction is enabled for the specific call type.
    #: example: True
    is_call_type_restriction_enabled: Optional[bool] = None


class ExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID shows the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID shows the external caller ID name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID shows the value from the `locationExternalCallerIdName` field.
    other = 'OTHER'


class InterceptAnnouncementsGetGreeting(str, Enum):
    #: A custom greeting is played when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default greeting is played when incoming calls are intercepted.
    default = 'DEFAULT'


class InterceptNumberGet(ApiModel):
    #: If `true`, the caller hears this new number when the call is intercepted.
    #: example: True
    enabled: Optional[bool] = None
    #: New number the caller hears announced.
    #: example: +12225551212
    destination: Optional[str] = None


class InterceptAnnouncementsGet(ApiModel):
    #: System default message places when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Filename of the custom greeting; this is an empty string if no custom greeting has been uploaded.
    #: example: incoming.wav
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call is handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptAnnouncementsPatch(ApiModel):
    #: System default message is placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call is handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptIncomingGetType(str, Enum):
    #: All incoming calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class InterceptIncomingGet(ApiModel):
    #: Incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptIncomingGetType] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsGet] = None


class InterceptOutGoingGetType(str, Enum):
    #: Outgoing calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class InterceptOutGoingGet(ApiModel):
    #: All outgoing calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptOutGoingGetType] = None
    #: If `true`, when the person attempts to make an outbound call, a system default message is played and the call is
    #: made to the destination phone number.
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    #: example: `+12225551212
    destination: Optional[str] = None


class InterceptGet(ApiModel):
    #: `true` if call intercept is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingGet] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptOutGoingGet] = None


class InterceptIncomingPatch(ApiModel):
    #: Incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptIncomingGetType] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    #: example: True
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsPatch] = None


class ModifyCallingPermission(ApiModel):
    #: Types for outgoing calls.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionCallType] = None
    #: Permission for call types.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: Calling Permission for call type enable status.
    #: example: True
    transfer_enabled: Optional[bool] = None


class ModifyPlaceCallForwardSettings(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingGet] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[CallForwardingBusyGet] = None


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: Name of call park extension.
    #: example: CPE1
    name: Optional[str] = None
    #: Extension of call park extension.
    #: example: 8080
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Name of location for call park extension.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of location for call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementUserType(str, Enum):
    #: Object is a user.
    people = 'PEOPLE'
    #: Object is a workspace.
    place = 'PLACE'


class UserNumberItem(ApiModel):
    #: Phone number of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: 8080
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Flag to indicate primary phone.
    #: example: True
    primary: Optional[bool] = None
    #: Flag to indicate toll free number.
    #: example: True
    toll_free_number: Optional[bool] = None


class MonitoredElementUser(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Brown
    last_name: Optional[str] = None
    #: Display name of person or workspace.
    #: example: John Brown
    display_name: Optional[str] = None
    #: Type of the person or workspace.
    #: example: PEOPLE
    type: Optional[MonitoredElementUserType] = None
    #: Email of the person or workspace.
    #: example: john.brown@gmail.com
    email: Optional[str] = None
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumberItem]] = None
    #: Name of location for call park.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of the location for call park.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementItem(ApiModel):
    #: Monitored Call Park extension.
    callparkextension: Optional[MonitoredElementCallParkExtension] = None
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser] = None


class PhoneNumbers(ApiModel):
    #: PSTN phone number in E.164 format.
    #: example: +12055550001
    external: Optional[str] = None
    #: Extension for workspace.
    #: example: 123
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234123
    esn: Optional[str] = None
    #: If `true`, the primary number.
    #: example: True
    primary: Optional[bool] = None


class PlaceCallerIdGet(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CLIDPolicySelection]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    #: example: DIRECT_LINE
    selected: Optional[CLIDPolicySelection] = None
    #: Direct number which is shown if `DIRECT_LINE` is selected.
    #: example: +12815550003
    direct_number: Optional[str] = None
    #: Location number which is shown if `LOCATION_NUMBER` is selected
    #: example: +12815550002
    location_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: Custom number which is shown if CUSTOM is selected. This value must be a number from the workspace's location or
    #: from another location with the same country, PSTN provider, and zone (only applicable for India locations) as
    #: the workspace's location.
    #: example: +12815550003
    custom_number: Optional[str] = None
    #: Workspace's caller ID display name.
    #: example: Clockmaker's shop 7.1
    display_name: Optional[str] = None
    #: Workspace's caller ID display details. Default is `.`.
    #: example: .
    display_detail: Optional[str] = None
    #: Block this workspace's identity when receiving a call.
    #: example: True
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy] = None
    #: Custom external caller ID name which is shown if external caller ID name policy is `OTHER`.
    #: example: Custom external caller name
    custom_external_caller_id_name: Optional[str] = None
    #: Location's external caller ID name which is shown if external caller ID name policy is `LOCATION`.
    #: example: Anna
    location_external_caller_id_name: Optional[str] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outbound permissions.
    #: example: True
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: example: "+1205553650"
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: example: "+1205553651"
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: example: "+1205553652"
    auto_transfer_number3: Optional[str] = None


class UserInboundPermissionGetExternalTransfer(str, Enum):
    #: All external calls are allowed.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only externally transferred external calls are allowed.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: All external calls are blocked.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class UserInboundPermissionGet(ApiModel):
    #: Incoming Permission state. If disabled, the default settings are used.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: Call transfer setting.
    #: example: ALLOW_ALL_EXTERNAL
    external_transfer: Optional[UserInboundPermissionGetExternalTransfer] = None
    #: Flag to indicate if workspace can receive internal calls.
    #: example: True
    internal_calls_enabled: Optional[bool] = None
    #: Flag to indicate if workspace can receive collect calls.
    #: example: True
    collect_calls_enabled: Optional[bool] = None


class UserMonitoringGet(ApiModel):
    #: Call park notification enabled or disabled.
    #: example: True
    call_park_notification_enabled: Optional[bool] = None
    #: Monitored element items.
    monitored_elements: Optional[MonitoredElementItem] = None


class UserOutgoingPermissionGet(ApiModel):
    #: When `true`, indicates that this workspace uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: When `true`, indicates that this workspace uses the specified outgoing calling permissions when placing outbound
    #: calls.
    #: example: True
    use_custom_permissions: Optional[bool] = None
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]] = None


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
    #: Music on hold enabled or disabled for the workspace.
    #: example: True
    moh_enabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location. The music on hold setting returned in the response is used
    #: only when music on hold is enabled at the location level. When `mohLocationEnabled` is false and `mohEnabled`
    #: is true, music on hold is disabled for the workspace. When `mohLocationEnabled` is true and `mohEnabled` is
    #: false, music on hold is turned off for the workspace. In both cases, music on hold will not be played.
    #: example: True
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the workspace.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class WorkspaceAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
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


class WorkspaceECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'


class WorkspaceECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which the phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the phone number's owner.
    #: example: PEOPLE
    type: Optional[WorkspaceECBNAvailableNumberObjectOwnerType] = None
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


class WorkspaceECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
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
    owner: Optional[WorkspaceECBNAvailableNumberObjectOwner] = None


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


class NumberOwnerObject(ApiModel):
    #: Unique identifier of the owner to which the PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class WorkspaceCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for the PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
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
    #: Owner details for the phone number.
    owner: Optional[NumberOwnerObject] = None


class UserBargeInGet(ApiModel):
    #: `true` if the BargeIn feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: When `true`, a tone is played when someone barges into a call.
    tone_enabled: Optional[bool] = None


class UserDoNotDisturbGet(ApiModel):
    #: `true` if the DoNotDisturb feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: When `true`, enables ring reminder when you receive an incoming call while on Do Not Disturb.
    ring_splash_enabled: Optional[bool] = None


class PushToTalkAccessType(str, Enum):
    #: List of people/workspaces that are allowed to use the Push-to-Talk feature to interact with the workspace being
    #: configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people/workspaces that are disallowed to interact using the Push-to-Talk feature with the workspace
    #: being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this workspace but only in one direction. The workspace you enable
    #: Push-to-Talk for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this workspace in a two-way conversation. The workspace you enable
    #: Push-to-Talk for can respond.
    two_way = 'TWO_WAY'


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the person.
    #: example: Little
    last_name: Optional[str] = None
    #: First name of the person.
    #: example: Alice
    first_name: Optional[str] = None
    #: Display name of the person.
    #: example: Alice Little
    display_name: Optional[str] = None
    #: Type usually indicates `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Push-to-Talk and Privacy features only supports
    #: `PEOPLE`.
    type: Optional[WorkspaceECBNAvailableNumberObjectOwnerType] = None
    #: Email address of the person.
    #: example: alice@example.com
    email: Optional[str] = None
    #: List of phone numbers of the person.
    numbers: Optional[list[PhoneNumbers]] = None


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a workspace receives a Push-to-Talk call and
    #: answers the call automatically.
    #: example: True
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people/workspaces that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing is enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name is enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy is enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only members specified by `monitoringAgents` can
    #: pickup or barge-in on the call.
    #: example: True
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: A custom greeting has been uploaded.
    #: example: True
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: A custom greeting has been uploaded
    #: example: True
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
    system_max_number_of_rings: Optional[int] = None


class VoicemailInfoEmailCopyOfMessage(ApiModel):
    #: When `true` copy of new voicemail message audio will be sent to the designated email.
    #: example: True
    enabled: Optional[bool] = None
    #: Email address to which the new voicemail audio will be sent.
    #: example: dummy@example.com
    email_id: Optional[str] = None


class VoicemailInfoMessageStorageStorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the person's email.
    external = 'EXTERNAL'


class VoicemailInfoMessageStorage(ApiModel):
    #: When `true` desktop phone will indicate there are new voicemails.
    #: example: True
    mwi_enabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    #: example: INTERNAL
    storage_type: Optional[VoicemailInfoMessageStorageStorageType] = None
    #: External email address to which the new voicemail audio will be sent.  A value for this field must be provided
    #: in the request if a `storageType` of `EXTERNAL` is given in the request.
    #: example: dummy@example.com
    external_email: Optional[str] = None


class VoicemailInfoFaxMessage(ApiModel):
    #: When `true` FAX messages for new voicemails will be sent to the designated number.
    #: example: True
    enabled: Optional[bool] = None
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage
    #: `enabled` field is given as `true` in the request.
    #: example: 2025551212
    phone_number: Optional[str] = None
    #: Designates optional FAX extension.
    #: example: 1234
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[CallWaiting] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailInfoSendBusyCalls] = None
    send_unanswered_calls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[InterceptNumberGet] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[InterceptNumberGet] = None
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailInfoEmailCopyOfMessage] = None
    message_storage: Optional[VoicemailInfoMessageStorage] = None
    fax_message: Optional[VoicemailInfoFaxMessage] = None


class VoicemailPutSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail.
    #: example: 3
    number_of_rings: Optional[int] = None


class SequentialRingCriteriaGetScheduleType(str, Enum):
    #: The Schedule is of type `holidays`.
    holidays = 'holidays'
    #: The Schedule is of type `businessHours`.
    business_hours = 'businessHours'


class SequentialRingCriteriaGetScheduleLevel(str, Enum):
    #: The Schedule specified is of `GROUP` level.
    group = 'GROUP'


class SequentialRingCriteriaGetCallsFrom(str, Enum):
    #: Sequential ring criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Sequential ring criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'


class SequentialRingCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: The type of schedule.
    #: example: holidays
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: This indicates the level of the schedule specified by `scheduleName`.
    #: example: GROUP
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: This indicates if criteria are applicable for calls from any phone number or selected phone numbers.
    #: example: SELECT_PHONE_NUMBERS
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true` incoming calls from private numbers are allowed. This is only applicable when `callsFrom` is set to
    #: `SELECT_PHONE_NUMBERS`.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true` incoming calls from unavailable numbers are allowed. This is only applicable when `callsFrom` is set
    #: to `SELECT_PHONE_NUMBERS`.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone numbers for which the
    #: criteria apply.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    #: example: True
    ring_enabled: Optional[bool] = None


class UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls(str, Enum):
    #: Connected line identification is not blocked on redirected calls.
    no_privacy = 'NO_PRIVACY'
    #: Connected line identification is blocked on redirected calls to external numbers.
    privacy_for_external_calls = 'PRIVACY_FOR_EXTERNAL_CALLS'
    #: Connected line identification is blocked on all redirected calls.
    privacy_for_all_calls = 'PRIVACY_FOR_ALL_CALLS'


class SequentialRingNumber(ApiModel):
    #: Phone number set as the sequential number.
    #: example: +442071838750
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    #: example: True
    answer_confirmation_required_enabled: Optional[bool] = None
    #: The number of rings to the specified phone number before the call advances to the subsequent number in the
    #: sequence or goes to voicemail.
    #: example: 2
    number_of_rings: Optional[int] = None


class Source(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class SequentialRingCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: If criterias are applicable for calls from any phone number or specific phone number.
    source: Optional[Source] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    #: example: True
    ring_enabled: Optional[bool] = None


class SequentialRingGet(ApiModel):
    #: When set to `true` sequential ring is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: When set to `true`, the webex calling primary line will ring first.
    #: example: True
    ring_base_location_first_enabled: Optional[bool] = None
    #: The number of times the primary line will ring.
    #: example: 2
    base_location_number_of_rings: Optional[str] = None
    #: When set to `true` and the primary line is busy, the system redirects calls to the numbers configured for
    #: sequential ringing.
    #: example: True
    continue_if_base_location_is_busy_enabled: Optional[bool] = None
    #: When set to `true` calls are directed to voicemail.
    #: example: True
    calls_to_voicemail_enabled: Optional[bool] = None
    #: A list of up to five phone numbers to which calls will be directed.
    phone_numbers: Optional[list[SequentialRingNumber]] = None
    #: A list of criteria specifying conditions when sequential ringing is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None


class SimultaneousRingNumberGet(ApiModel):
    #: Phone number set as the sequential number.
    #: example: +19075552859
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    #: example: True
    answer_confirmation_required_enabled: Optional[bool] = None


class SimultaneousRingGet(ApiModel):
    #: Simultaneous Ring is enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when on a call.
    #: example: True
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when a workspace phone receives an incoming call.
    phone_numbers: Optional[list[SimultaneousRingNumberGet]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SequentialRingCriteria]] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    #: example: True
    criterias_enabled: Optional[bool] = None


class CallsFromTypeForSelectiveForward(str, Enum):
    #: The schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The schedule applies to any internal phone number.
    any_internal = 'ANY_INTERNAL'
    #: The schedule applies to any external phone number.
    any_external = 'ANY_EXTERNAL'


class SelectiveRejectCallSource(str, Enum):
    #: Selective reject criteria applies for all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Selective reject criteria applies for calls from specific numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Selective reject criteria applies for all forwarded calls.
    forwarded = 'FORWARDED'


class SelectiveRejectCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to reject or not to reject the calls that fit within these parameters.
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallGet(ApiModel):
    #: `true` if the Selective Reject feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective reject is in effect.
    criteria: Optional[list[SelectiveRejectCriteria]] = None


class SelectiveRejectCallCallsFromType(str, Enum):
    #: The Schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The Schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The Schedule applies to the forwarded calls only.
    forwarded = 'FORWARDED'


class PlaceSelectiveRejectCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective reject criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective reject to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective reject to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be rejected (if rejectEnabled = `true`) or
    #: not (if rejectEnabled = `false`).
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveAcceptCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective reject is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number, specific phone number or forwarded ones.
    source: Optional[SelectiveRejectCallSource] = None
    #: This setting specifies to choose to accept or not to accept the calls that fit within these parameters.
    #: example: True
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallGet(ApiModel):
    #: `true` if the Selective Accept feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective accept is in effect.
    criteria: Optional[list[SelectiveAcceptCallCriteria]] = None


class PlaceSelectiveAcceptCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective accept is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective accept criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[SelectiveRejectCallCallsFromType] = None
    #: When `true`, enables selective accept to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective accept to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be accepted (if acceptEnabled = `true`) or
    #: not (if acceptEnabled = `false`).
    #: example: True
    accept_enabled: Optional[bool] = None


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class RingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    #: example: True
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    #: example: +12145553567
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    #: example: 1234
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern] = None


class PlaceGetNumbersResponse(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]] = None


class PriorityAlertCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: If criteria are applicable for calls from any phone number or specific phone number.
    #: example: ALL_NUMBERS
    source: Optional[Source] = None
    #: When set to `true` notification is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    #: example: True
    notification_enabled: Optional[bool] = None


class PriorityAlertGet(ApiModel):
    #: `true` if the Priority Alert feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when priority alert is in effect.
    criteria: Optional[list[PriorityAlertCriteria]] = None


class PlacePriorityAlertCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the priority alert is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e. Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone Numbers.
    calls_from: Optional[SequentialRingCriteriaGetCallsFrom] = None
    #: When `true`, enables calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables calls even if callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` priority alerting criteria is enabled for calls that meet the current criteria. Criteria with
    #: `notificationEnabled` set to `false` take priority.
    #: example: True
    notification_enabled: Optional[bool] = None


class SourceForSelectiveForward(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Criteria applies to all internal incoming numbers.
    any_internal = 'ANY_INTERNAL'
    #: Criteria applies to all external incoming numbers.
    any_external = 'ANY_EXTERNAL'


class SelectiveForwardCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: Criteria are applicable for calls from any phone number or a specific phone number.
    source: Optional[SourceForSelectiveForward] = None
    #: When set to `true` sequential ringing is enabled for calls that meet the current criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    #: example: True
    ring_enabled: Optional[bool] = None


class SelectiveForwardCallGet(ApiModel):
    #: `true` if the Selective Forward feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Enter the phone number to forward calls to during this schedule.
    #: example: +1934898988
    default_phone_number_to_forward: Optional[str] = None
    #: When `true`, enables a ring reminder for such calls.
    #: example: True
    ring_reminder_enabled: Optional[bool] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    destination_voicemail_enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective forward feature is in effect.
    criteria: Optional[list[SelectiveForwardCallCriteria]] = None


class PlaceSelectiveForwardCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBLzg2NTAxZDFlLTg1MWMtNDgwYi1hZmE2LTA5MTU4NzQ3NzdmZQ
    id: Optional[str] = None
    #: Phone number to forward calls to during this schedule.
    #: example: +1934898988
    forward_to_phone_number: Optional[str] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Name of the location's schedule which determines when the selective forward is in effect.
    #: example: Business Vacation
    schedule_name: Optional[str] = None
    #: The Schedule type whether `businessHours` or `holidays`.
    schedule_type: Optional[SequentialRingCriteriaGetScheduleType] = None
    #: The Schedule level i.e, Group.
    schedule_level: Optional[SequentialRingCriteriaGetScheduleLevel] = None
    #: Indicates whether to apply the selective forward criteria for calls from Any Phone Number, Select Phone Numbers
    #: or Forwarded ones.
    calls_from: Optional[CallsFromTypeForSelectiveForward] = None
    #: When `true`, enables selective forward to calls from anonymous callers.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective forward to calls if the callers are unavailable.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers checked against incoming calls for a match.
    #: example: ['[ "+19075552859"', '"+19186663950" ]']
    numbers: Optional[list[str]] = None
    #: Indicates whether the calls, that fit within these parameters, will be forwarded (if forwardEnabled = `true`) or
    #: not (if forwardEnabled = `false`).
    #: example: True
    forward_enabled: Optional[bool] = None


class WorkspaceDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFL1FWVlVUMEZVVkVWT1JFRk9WQzFDVlZOSlRrVlRVeTFJVDFWU1V3
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    #: example: DigitPattern1
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    #: example: 1XXX
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches the digit pattern.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: Option to allow or disallow transfer of calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class WorkspaceOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[WorkspaceDigitPatternObject]] = None


class WorkspaceCallSettingsApi(ApiChild, base=''):
    """
    Workspace Call Settings
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    or location administrator auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def retrieve_call_forwarding_settings_for_a_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> ModifyPlaceCallForwardSettings:
        """
        Retrieve Call Forwarding Settings for a Workspace.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy, forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer, forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`ModifyPlaceCallForwardSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callForwarding')
        data = super().get(url, params=params)
        r = ModifyPlaceCallForwardSettings.model_validate(data)
        return r

    def modify_call_forwarding_settings_for_a_workspace(self, workspace_id: str,
                                                        call_forwarding: CallForwardingPlaceSettingGet,
                                                        business_continuity: CallForwardingBusyGet,
                                                        org_id: str = None):
        """
        Modify call forwarding settings for a Workspace.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy, forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer, forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param call_forwarding: Call forwarding settings for a Workspace.
        :type call_forwarding: CallForwardingPlaceSettingGet
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingBusyGet
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'workspaces/{workspace_id}/features/callForwarding')
        super().put(url, params=params, json=body)

    def retrieve_call_waiting_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Call Waiting Settings for a Workspace.

        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callWaiting')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def modify_call_waiting_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                     org_id: str = None):
        """
        Modify Call Waiting Settings for a Workspace.

        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: Call Waiting state.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'workspaces/{workspace_id}/features/callWaiting')
        super().put(url, params=params, json=body)

    def read_caller_id_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PlaceCallerIdGet:
        """
        Read Caller ID Settings for a Workspace

        Retrieve a workspace's Caller ID settings.

        Caller ID settings control how a workspace's information is displayed when making outgoing calls.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceCallerIdGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callerId')
        data = super().get(url, params=params)
        r = PlaceCallerIdGet.model_validate(data)
        return r

    def configure_caller_id_settings_for_a_workspace(self, workspace_id: str, selected: CLIDPolicySelection,
                                                     custom_number: str = None, display_name: str = None,
                                                     display_detail: str = None,
                                                     block_in_forward_calls_enabled: bool = None,
                                                     external_caller_id_name_policy: ExternalCallerIdNamePolicy = None,
                                                     custom_external_caller_id_name: str = None,
                                                     location_external_caller_id_name: str = None,
                                                     org_id: str = None):
        """
        Configure Caller ID Settings for a Workspace

        Configure workspace's Caller ID settings.

        Caller ID settings control how a workspace's information is displayed when making outgoing calls.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CLIDPolicySelection
        :param custom_number: Custom number which is shown if CUSTOM is selected. This value must be a number from the
            workspace's location or from another location with the same country, PSTN provider, and zone (only
            applicable for India locations) as the workspace's location.
        :type custom_number: str
        :param display_name: Workspace's caller ID display name.
        :type display_name: str
        :param display_detail: Workspace's caller ID display details.
        :type display_detail: str
        :param block_in_forward_calls_enabled: Block this workspace's identity when receiving a call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is `DIRECT_LINE`.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom external caller ID name which is shown if external caller ID name
            policy is `OTHER`.
        :type custom_external_caller_id_name: str
        :param location_external_caller_id_name: Location's external caller ID name which is shown if external caller
            ID name policy is `LOCATION`.
        :type location_external_caller_id_name: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        if custom_number is not None:
            body['customNumber'] = custom_number
        if display_name is not None:
            body['displayName'] = display_name
        if display_detail is not None:
            body['displayDetail'] = display_detail
        if block_in_forward_calls_enabled is not None:
            body['blockInForwardCallsEnabled'] = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body['externalCallerIdNamePolicy'] = enum_str(external_caller_id_name_policy)
        if custom_external_caller_id_name is not None:
            body['customExternalCallerIdName'] = custom_external_caller_id_name
        if location_external_caller_id_name is not None:
            body['locationExternalCallerIdName'] = location_external_caller_id_name
        url = self.ep(f'workspaces/{workspace_id}/features/callerId')
        super().put(url, params=params, json=body)

    def retrieve_monitoring_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> UserMonitoringGet:
        """
        Retrieve Monitoring Settings for a Workspace

        Retrieves Monitoring settings for a Workspace.

        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserMonitoringGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/monitoring')
        data = super().get(url, params=params)
        r = UserMonitoringGet.model_validate(data)
        return r

    def modify_monitoring_settings_for_a_workspace(self, workspace_id: str, enable_call_park_notification: bool = None,
                                                   monitored_elements: list[str] = None, org_id: str = None):
        """
        Modify Monitoring settings for a Workspace.

        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enable_call_park_notification: Call park notification is enabled or disabled.
        :type enable_call_park_notification: bool
        :param monitored_elements: Array of ID strings of monitored elements.
        :type monitored_elements: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enable_call_park_notification is not None:
            body['enableCallParkNotification'] = enable_call_park_notification
        if monitored_elements is not None:
            body['monitoredElements'] = monitored_elements
        url = self.ep(f'workspaces/{workspace_id}/features/monitoring')
        super().put(url, params=params, json=body)

    def retrieve_music_on_hold_settings_for_a_workspace(self, workspace_id: str,
                                                        org_id: str = None) -> GetMusicOnHoldObject:
        """
        Retrieve Music On Hold Settings for a Workspace.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving a workspace's music on hold settings requires a full, device or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

    def modify_music_on_hold_settings_for_a_workspace(self, workspace_id: str, moh_enabled: bool = None,
                                                      greeting: InterceptAnnouncementsGetGreeting = None,
                                                      audio_announcement_file: AudioAnnouncementFileGetObject = None,
                                                      org_id: str = None):
        """
        Modify music on hold settings for a Workspace.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold setting for a workspace, music on hold setting must be enabled for this location.

        This API requires a full or device administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param moh_enabled: Music on hold is enabled or disabled for the workspace.
        :type moh_enabled: bool
        :param greeting: Greeting type for the workspace.
        :type greeting: InterceptAnnouncementsGetGreeting
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/musicOnHold')
        super().put(url, params=params, json=body)

    def list_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> PlaceGetNumbersResponse:
        """
        List numbers associated with a specific workspace

        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:workspaces_read`.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            can use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceGetNumbersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/numbers')
        data = super().get(url, params=params)
        r = PlaceGetNumbersResponse.model_validate(data)
        return r

    def retrieve_incoming_permission_settings_for_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> UserInboundPermissionGet:
        """
        Retrieve Incoming Permission settings for a Workspace.

        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserInboundPermissionGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/incomingPermission')
        data = super().get(url, params=params)
        r = UserInboundPermissionGet.model_validate(data)
        return r

    def modify_incoming_permission_settings_for_a_workspace(self, workspace_id: str, use_custom_enabled: bool = None,
                                                            external_transfer: UserInboundPermissionGetExternalTransfer = None,
                                                            internal_calls_enabled: bool = None,
                                                            collect_calls_enabled: bool = None, org_id: str = None):
        """
        Modify Incoming Permission settings for a Workspace.

        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_enabled: Incoming Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param external_transfer: Call transfer setting.
        :type external_transfer: UserInboundPermissionGetExternalTransfer
        :param internal_calls_enabled: Flag to indicate if the workspace can receive internal calls.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Flag to indicate if the workspace can receive collect calls.
        :type collect_calls_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if external_transfer is not None:
            body['externalTransfer'] = enum_str(external_transfer)
        if internal_calls_enabled is not None:
            body['internalCallsEnabled'] = internal_calls_enabled
        if collect_calls_enabled is not None:
            body['collectCallsEnabled'] = collect_calls_enabled
        url = self.ep(f'workspaces/{workspace_id}/features/incomingPermission')
        super().put(url, params=params, json=body)

    def retrieve_outgoing_permission_settings_for_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> UserOutgoingPermissionGet:
        """
        Retrieve Outgoing Permission settings for a Workspace.

        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        data = super().get(url, params=params)
        r = UserOutgoingPermissionGet.model_validate(data)
        return r

    def modify_outgoing_permission_settings_for_a_workspace(self, workspace_id: str, use_custom_enabled: bool = None,
                                                            use_custom_permissions: bool = None,
                                                            calling_permissions: list[ModifyCallingPermission] = None,
                                                            org_id: str = None):
        """
        Modify Outgoing Permission Settings for a Workspace

        Modify Outgoing Permission settings for a Place.

        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_enabled: When `true`, indicates that this workspace uses the shared control that applies to
            all outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When `true`, indicates that this workspace uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: list[ModifyCallingPermission]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if use_custom_permissions is not None:
            body['useCustomPermissions'] = use_custom_permissions
        if calling_permissions is not None:
            body['callingPermissions'] = TypeAdapter(list[ModifyCallingPermission]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        super().put(url, params=params, json=body)

    def retrieve_access_codes_for_a_workspace(self, workspace_id: str, org_id: str = None) -> list[AuthorizationCode]:
        """
        Retrieve Access codes for a Workspace.

        Access codes are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: list[AuthorizationCode]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AuthorizationCode]).validate_python(data['accessCodes'])
        return r

    def modify_access_codes_for_a_workspace(self, workspace_id: str, delete_codes: list[str] = None,
                                            org_id: str = None):
        """
        Modify Access codes for a workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param delete_codes: Access Codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def create_access_codes_for_a_workspace(self, workspace_id: str, code: str, description: str, org_id: str = None):
        """
        Create Access Codes for a Workspace

        Create new Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param code: An Access code.
        :type code: str
        :param description: The description of the access code.
        :type description: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['code'] = code
        body['description'] = description
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def delete_all_access_codes_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete all Access Codes for a Workspace

        Deletes all Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def retrieve_all_digit_patterns_for_a_workspace(self, workspace_id: str,
                                                    org_id: str = None) -> WorkspaceOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve all digit patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = WorkspaceOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def retrieve_a_digit_pattern_details_for_the_workspace(self, workspace_id: str, digit_pattern_id: str,
                                                           org_id: str = None) -> WorkspaceDigitPatternObject:
        """
        Retrieve a Digit Pattern details for the Workspace

        Retrieve the designated digit pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = WorkspaceDigitPatternObject.model_validate(data)
        return r

    def create_digit_pattern_for_a_workspace(self, workspace_id: str, name: str, pattern: str,
                                             action: CallingPermissionAction, transfer_enabled: bool,
                                             org_id: str = None) -> str:
        """
        Create Digit Pattern for a Workspace

        Create a new digit pattern for the given workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: CallingPermissionAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_the_digit_pattern_category_control_settings_for_the_workspace(self, workspace_id: str,
                                                                             use_custom_digit_patterns: bool = None,
                                                                             org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for the Workspace

        Modifies whether this workspace uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or location administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def modify_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, name: str = None,
                                                 pattern: str = None, action: CallingPermissionAction = None,
                                                 transfer_enabled: bool = None, org_id: str = None):
        """
        Modify a Digit Pattern for the Workspace

        Modify the designated digit pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: CallingPermissionAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def delete_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a Digit Pattern for the Workspace

        Delete a digit pattern for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def delete_all_digit_patterns_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete all digit patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

    def read_call_intercept_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> InterceptGet:
        """
        Read Call Intercept Settings for a Workspace

        Retrieves Workspace's Call Intercept Settings

        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified workspace are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`InterceptGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/intercept')
        data = super().get(url, params=params)
        r = InterceptGet.model_validate(data)
        return r

    def configure_call_intercept_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                          incoming: InterceptIncomingPatch = None,
                                                          outgoing: InterceptOutGoingGet = None, org_id: str = None):
        """
        Configure Call Intercept Settings for a Workspace

        Configures a Workspace's Call Intercept Settings

        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_write` or a user auth token with `spark:workspaces_read` scope can be used by a person
        to read their settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if call interception is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: InterceptIncomingPatch
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: InterceptOutGoingGet
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming.model_dump(mode='json', by_alias=True, exclude_none=True)
        if outgoing is not None:
            body['outgoing'] = outgoing.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'workspaces/{workspace_id}/features/intercept')
        super().put(url, params=params, json=body)

    def retrieve_transfer_numbers_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> TransferNumberGet:
        """
        Retrieve Transfer Numbers Settings for a Workspace.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`TransferNumberGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = TransferNumberGet.model_validate(data)
        return r

    def modify_transfer_numbers_settings_for_a_workspace(self, workspace_id: str, use_custom_transfer_numbers: bool,
                                                         auto_transfer_number1: str = None,
                                                         auto_transfer_number2: str = None,
                                                         auto_transfer_number3: str = None, org_id: str = None):
        """
        Modify Transfer Numbers Settings for a Workspace

        Modify Transfer Numbers Settings for a place.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_transfer_numbers: When `true`, use custom settings for the transfer numbers category of
            outbound permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number3: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def get_workspace_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                              org_id: str = None,
                                              **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's phone number.
        By default, this API returns numbers from all locations that are unassigned. To select the suitable number for
        assignment, ensure the workspace's location ID is provided as the `locationId` request parameter.

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
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep('telephony/config/workspaces/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_ecbn_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                   owner_name: str = None, org_id: str = None,
                                                   **params) -> Generator[WorkspaceECBNAvailableNumberObject, None, None]:
        """
        Get Workspace ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's emergency callback number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_call_forward_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                           owner_name: str = None, extension: str = None,
                                                           org_id: str = None,
                                                           **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a workspace's call forward
        number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
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
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_call_intercept_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                             owner_name: str = None, extension: str = None,
                                                             org_id: str = None,
                                                             **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a workspace's call intercept
        number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
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
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def retrieve_anonymous_call_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Anonymous Call Settings for a Workspace.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/anonymousCallReject')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def modify_anonymous_call_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Anonymous Call Settings for a Workspace.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Anonymous Call Rejection feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/anonymousCallReject')
        super().put(url, params=params, json=body)

    def retrieve_barge_in_call_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> UserBargeInGet:
        """
        Retrieve Barge In Call Settings for a Workspace.

        Barge In, when enabled, allows you to use the Feature Access Code (FAC) on your desk phone to answer someone
        else’s phone call or barge in on a call they’ve already answered.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserBargeInGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/bargeIn')
        data = super().get(url, params=params)
        r = UserBargeInGet.model_validate(data)
        return r

    def modify_barge_in_call_settings_for_a_workspace(self, workspace_id: str, enabled: bool,
                                                      tone_enabled: bool = None, org_id: str = None):
        """
        Modify Barge In Call Settings for a Workspace.

        Barge In, when enabled, allows you to use the Feature Access Code (FAC) on your desk phone to answer someone
        else’s phone call or barge in on a call they’ve already answered.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Barge In feature is enabled.
        :type enabled: bool
        :param tone_enabled: When `true`, a tone is played when someone barges into a call.
        :type tone_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/bargeIn')
        super().put(url, params=params, json=body)

    def retrieve_do_not_disturb_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> UserDoNotDisturbGet:
        """
        Retrieve DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserDoNotDisturbGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/doNotDisturb')
        data = super().get(url, params=params)
        r = UserDoNotDisturbGet.model_validate(data)
        return r

    def modify_do_not_disturb_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                       ring_splash_enabled: bool = None, org_id: str = None):
        """
        Modify DoNotDisturb Settings for a Workspace.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the DoNotDisturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: When `true`, enables ring reminder when you receive an incoming call while on Do
            Not Disturb.
        :type ring_splash_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if ring_splash_enabled is not None:
            body['ringSplashEnabled'] = ring_splash_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/doNotDisturb')
        super().put(url, params=params, json=body)

    def retrieve_call_bridge_warning_tone_settings_for_a_workspace(self, workspace_id: str,
                                                                   org_id: str = None) -> bool:
        """
        Retrieve Call Bridge Warning Tone Settings for a Workspace.

        Call Bridge Warning Tone, when enabled, ensures that users hear a warning tone when other users bridge into an
        active call on the same shared line appearance.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callBridge')
        data = super().get(url, params=params)
        r = data['warningToneEnabled']
        return r

    def modify_call_bridge_warning_tone_settings_for_a_workspace(self, workspace_id: str, warning_tone_enabled: bool,
                                                                 org_id: str = None):
        """
        Modify Call Bridge Warning Tone Settings for a Workspace.

        Call Bridge Warning Tone, when enabled, ensures that users hear a warning tone when other users bridge into an
        active call on the same shared line appearance.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param warning_tone_enabled: `true` if the Call Bridge Warning Tone feature is enabled.
        :type warning_tone_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callBridge')
        super().put(url, params=params, json=body)

    def read_push_to_talk_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PushToTalkInfo:
        """
        Read Push-to-Talk Settings for a Workspace

        Retrieve Push-to-Talk settings for a workspace.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects
        people/workspaces in different parts of your organization.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/pushToTalk')
        data = super().get(url, params=params)
        r = PushToTalkInfo.model_validate(data)
        return r

    def configure_push_to_talk_settings_for_a_workspace(self, workspace_id: str, allow_auto_answer: bool = None,
                                                        connection_type: PushToTalkConnectionType = None,
                                                        access_type: PushToTalkAccessType = None,
                                                        members: list[str] = None, org_id: str = None):
        """
        Configure Push-to-Talk settings for a workspace.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects
        people/workspaces in different parts of your organization.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param allow_auto_answer: `true` if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
        :type members: list[str]
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if allow_auto_answer is not None:
            body['allowAutoAnswer'] = allow_auto_answer
        if connection_type is not None:
            body['connectionType'] = enum_str(connection_type)
        if access_type is not None:
            body['accessType'] = enum_str(access_type)
        if members is not None:
            body['members'] = members
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/pushToTalk')
        super().put(url, params=params, json=body)

    def retrieve_privacy_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PrivacyGet:
        """
        Retrieve Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def modify_privacy_settings_for_a_workspace(self, workspace_id: str, aa_extension_dialing_enabled: bool = None,
                                                aa_naming_dialing_enabled: bool = None,
                                                enable_phone_status_directory_privacy: bool = None,
                                                enable_phone_status_pickup_barge_in_privacy: bool = None,
                                                monitoring_agents: list[str] = None, org_id: str = None):
        """
        Modify Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param aa_extension_dialing_enabled: When `true` auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When `true` auto attendant dialing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When `true` phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param enable_phone_status_pickup_barge_in_privacy: When `true` privacy is enforced for call pickup and
            barge-in. Only members specified by `monitoringAgents` can pickup or barge-in on the call.
        :type enable_phone_status_pickup_barge_in_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if aa_extension_dialing_enabled is not None:
            body['aaExtensionDialingEnabled'] = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body['aaNamingDialingEnabled'] = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body['enablePhoneStatusDirectoryPrivacy'] = enable_phone_status_directory_privacy
        if enable_phone_status_pickup_barge_in_privacy is not None:
            body['enablePhoneStatusPickupBargeInPrivacy'] = enable_phone_status_pickup_barge_in_privacy
        if monitoring_agents is not None:
            body['monitoringAgents'] = monitoring_agents
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/privacy')
        super().put(url, params=params, json=body)

    def read_voicemail_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> VoicemailInfo:
        """
        Read Voicemail Settings for a Workspace

        Retrieve a workspace Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`VoicemailInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail')
        data = super().get(url, params=params)
        r = VoicemailInfo.model_validate(data)
        return r

    def configure_voicemail_settings_for_a_workspace(self, workspace_id: str, notifications: InterceptNumberGet,
                                                     transfer_to_number: InterceptNumberGet, enabled: bool = None,
                                                     send_all_calls: CallWaiting = None,
                                                     send_busy_calls: VoicemailPutSendBusyCalls = None,
                                                     send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                                     email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                                     message_storage: VoicemailInfoMessageStorage = None,
                                                     fax_message: VoicemailInfoFaxMessage = None, org_id: str = None):
        """
        Configure Voicemail Settings for a Workspace

        Configure a workspace Voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, `.wav`, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: InterceptNumberGet
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: InterceptNumberGet
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: CallWaiting
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :type message_storage: VoicemailInfoMessageStorage
        :type fax_message: VoicemailInfoFaxMessage
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if send_all_calls is not None:
            body['sendAllCalls'] = send_all_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        if send_busy_calls is not None:
            body['sendBusyCalls'] = send_busy_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        if send_unanswered_calls is not None:
            body['sendUnansweredCalls'] = send_unanswered_calls.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['notifications'] = notifications.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['transferToNumber'] = transfer_to_number.model_dump(mode='json', by_alias=True, exclude_none=True)
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = email_copy_of_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        if message_storage is not None:
            body['messageStorage'] = message_storage.model_dump(mode='json', by_alias=True, exclude_none=True)
        if fax_message is not None:
            body['faxMessage'] = fax_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail')
        super().put(url, params=params, json=body)

    def modify_voicemail_passcode_for_a_workspace(self, place_id: str, passcode: str, org_id: str = None):
        """
        Modify voicemail passcode for a workspace.

        Modifying the voicemail passcode for a workspace requires a full administrator, device administrator or
        location administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param place_id: Modify voicemail passcode for this workspace.
        :type place_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a workspace in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'telephony/config/workspaces/{place_id}/voicemail/passcode')
        super().put(url, params=params, json=body)

    def retrieve_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                          org_id: str = None) -> SequentialRingCriteriaGet:
        """
        Retrieve sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def modify_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                        schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                        schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                        calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None, ring_enabled: bool = None,
                                                        org_id: str = None):
        """
        Modify sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the sequential ring is in effect.
        :type schedule_name: str
        :param schedule_type: This indicates the type of schedule.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: This indicates the level of the schedule specified by `scheduleName`.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: This indicates if criteria are applicable for calls from any phone number or selected phone
            numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true` incoming calls from private numbers are allowed. This is only
            applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true` incoming calls from unavailable numbers are allowed. This is
            only applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone
            numbers for which the criteria apply.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` sequential ringing is enabled for calls that meet the current criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
        super().put(url, params=params, json=body)

    def read_call_policy_settings_for_a_workspace(self, workspace_id: str,
                                                  org_id: str = None) -> UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls:
        """
        Read Call Policy Settings for a Workspace

        Retrieve a workspace Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callPolicies')
        data = super().get(url, params=params)
        r = UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls.model_validate(data['connectedLineIdPrivacyOnRedirectedCalls'])
        return r

    def configure_call_policy_settings_for_a_workspace(self, workspace_id: str,
                                                       connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls,
                                                       org_id: str = None):
        """
        Configure Call Policy Settings for a Workspace

        Configure a workspace Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param connected_line_id_privacy_on_redirected_calls: Specifies the connection type to be used.
        :type connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/callPolicies')
        super().put(url, params=params, json=body)

    def configure_busy_voicemail_greeting_for_a_place(self, workspace_id: str, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Place

        Configure a workspace's Busy Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url, params=params)

    def configure_no_answer_voicemail_greeting_for_a_place(self, workspace_id: str, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Place

        Configure a workspace's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)

    def delete_sequential_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria/{id}')
        super().delete(url, params=params)

    def create_sequential_ring_criteria_for_a_workspace(self, workspace_id: str,
                                                        calls_from: SequentialRingCriteriaGetCallsFrom,
                                                        ring_enabled: bool, schedule_name: str = None,
                                                        schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                        schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                        anonymous_callers_enabled: bool = None,
                                                        unavailable_callers_enabled: bool = None,
                                                        phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create sequential ring criteria for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param calls_from: This indicates if criteria are applicable for calls from any phone number or selected phone
            numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param ring_enabled: When set to `true` sequential ringing is enabled for calls that meet the current criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the sequential ring is in effect.
        :type schedule_name: str
        :param schedule_type: This indicates the type of schedule.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: This indicates the level of the schedule specified by `scheduleName`.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true` incoming calls from private numbers are allowed. This is only
            applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true` incoming calls from unavailable numbers are allowed. This is
            only applicable when `callsFrom` is set to `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone
            numbers for which the criteria apply.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        body['ringEnabled'] = ring_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def retrieve_sequential_ring_settings_for_a_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> SequentialRingGet:
        """
        Retrieve sequential ring settings for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing')
        data = super().get(url, params=params)
        r = SequentialRingGet.model_validate(data)
        return r

    def modify_sequential_ring_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                        ring_base_location_first_enabled: bool = None,
                                                        base_location_number_of_rings: int = None,
                                                        continue_if_base_location_is_busy_enabled: bool = None,
                                                        calls_to_voicemail_enabled: bool = None,
                                                        phone_numbers: list[SequentialRingNumber] = None,
                                                        org_id: str = None):
        """
        Modify sequential ring settings for a workspace.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: When set to `true` sequential ring is enabled.
        :type enabled: bool
        :param ring_base_location_first_enabled: When set to `true`, the webex calling primary line will ring first.
        :type ring_base_location_first_enabled: bool
        :param base_location_number_of_rings: The number of times the primary line will ring.
        :type base_location_number_of_rings: int
        :param continue_if_base_location_is_busy_enabled: When set to `true` and the primary line is busy, the system
            redirects calls to the numbers configured for sequential ringing.
        :type continue_if_base_location_is_busy_enabled: bool
        :param calls_to_voicemail_enabled: When set to `true` calls are directed to voicemail.
        :type calls_to_voicemail_enabled: bool
        :param phone_numbers: A list of up to five phone numbers to which calls will be directed.
        :type phone_numbers: list[SequentialRingNumber]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if ring_base_location_first_enabled is not None:
            body['ringBaseLocationFirstEnabled'] = ring_base_location_first_enabled
        if base_location_number_of_rings is not None:
            body['baseLocationNumberOfRings'] = base_location_number_of_rings
        if continue_if_base_location_is_busy_enabled is not None:
            body['continueIfBaseLocationIsBusyEnabled'] = continue_if_base_location_is_busy_enabled
        if calls_to_voicemail_enabled is not None:
            body['callsToVoicemailEnabled'] = calls_to_voicemail_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SequentialRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/sequentialRing')
        super().put(url, params=params, json=body)

    def retrieve_simultaneous_ring_settings_for_a_workspace(self, workspace_id: str,
                                                            org_id: str = None) -> SimultaneousRingGet:
        """
        Retrieve Simultaneous Ring Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SimultaneousRingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing')
        data = super().get(url, params=params)
        r = SimultaneousRingGet.model_validate(data)
        return r

    def modify_simultaneous_ring_settings_for_a_workspace(self, workspace_id: str, criterias_enabled: bool,
                                                          enabled: bool = None,
                                                          do_not_ring_if_on_call_enabled: bool = None,
                                                          phone_numbers: list[SimultaneousRingNumberGet] = None,
                                                          org_id: str = None):
        """
        Modify Simultaneous Ring Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure the workspace phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param criterias_enabled: When `true`, enables the selected schedule for simultaneous ring.
        :type criterias_enabled: bool
        :param enabled: Simultaneous Ring is enabled or not.
        :type enabled: bool
        :param do_not_ring_if_on_call_enabled: When set to `true`, the configured phone numbers won't ring when on a
            call.
        :type do_not_ring_if_on_call_enabled: bool
        :param phone_numbers: Enter up to 10 phone numbers to ring simultaneously when a workspace phone receives an
            incoming call.
        :type phone_numbers: list[SimultaneousRingNumberGet]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if do_not_ring_if_on_call_enabled is not None:
            body['doNotRingIfOnCallEnabled'] = do_not_ring_if_on_call_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SimultaneousRingNumberGet]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        body['criteriasEnabled'] = criterias_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing')
        super().put(url, params=params, json=body)

    def retrieve_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                            org_id: str = None) -> SequentialRingCriteriaGet:
        """
        Retrieve Simultaneous Ring Criteria for a Workspace

        Retrieve Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def create_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom,
                                                          ring_enabled: bool, anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Simultaneous Ring Criteria for a Workspace

        Create Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply simultaneously ring for calls from Any Phone Number or Select
            Phone Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param ring_enabled: When set to `true` simultaneous ringing criteria is enabled for calls that meet the
            current criteria. Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None, ring_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Simultaneous Ring Criteria for a Workspace

        Modify Simultaneous Ring Criteria Settings for a Workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply simultaneously ring for calls from Any Phone Number or Select
            Phone Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` simultaneous ringing criteria is enabled for calls that meet the
            current criteria. Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_simultaneous_ring_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Simultaneous Ring Criteria for a Workspace

        Delete simultaneous ring criteria Settings for a workspace.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/simultaneousRing/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_reject_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> SelectiveRejectCallGet:
        """
        Retrieve Selective Reject Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject')
        data = super().get(url, params=params)
        r = SelectiveRejectCallGet.model_validate(data)
        return r

    def modify_selective_reject_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Selective Reject Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: if `true`, selective reject is enabled.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject')
        super().put(url, params=params, json=body)

    def retrieve_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                           org_id: str = None) -> PlaceSelectiveRejectCallCriteriaGet:
        """
        Retrieve Selective Reject Criteria for a Workspace

        Retrieve Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveRejectCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveRejectCallCriteriaGet.model_validate(data)
        return r

    def create_selective_reject_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                         calls_from: SelectiveRejectCallCallsFromType,
                                                         reject_enabled: bool, anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Selective Reject Criteria for a Workspace

        Create Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the selective reject is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective reject criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param reject_enabled: Choose to reject (if `rejectEnabled` = `true`) or not to reject (if `rejectEnabled` =
            `false`) the calls that fit within these parameters.
        :type reject_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                         calls_from: SelectiveRejectCallCallsFromType = None,
                                                         anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, reject_enabled: bool = None,
                                                         org_id: str = None):
        """
        Modify Selective Reject Criteria for a Workspace

        Modify Selective Reject Criteria Settings for a Workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the selective reject is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective reject criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param reject_enabled: Choose to reject (if `rejectEnabled` = `true`) or not to reject (if `rejectEnabled` =
            `false`) the calls that fit within these parameters.
        :type reject_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if reject_enabled is not None:
            body['rejectEnabled'] = reject_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        super().put(url, params=params, json=body)

    def assign_or_unassign_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                                        phone_numbers: list[PhoneNumber],
                                                                        distinctive_ring_enabled: bool = None,
                                                                        org_id: str = None):
        """
        Assign or Unassign numbers associated with a specific workspace

        Assign or unassign alternate phone numbers associated with a specific workspace.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: list[PhoneNumber]
        :param distinctive_ring_enabled: Enables a distinctive ring pattern for the person.
        :type distinctive_ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if distinctive_ring_enabled is not None:
            body['distinctiveRingEnabled'] = distinctive_ring_enabled
        body['phoneNumbers'] = TypeAdapter(list[PhoneNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/numbers')
        super().put(url, params=params, json=body)

    def delete_selective_reject_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Reject Criteria for a Workspace

        Delete Selective Reject criteria Settings for a workspace.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveReject/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_accept_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> SelectiveAcceptCallGet:
        """
        Retrieve Selective Accept Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveAcceptCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept')
        data = super().get(url, params=params)
        r = SelectiveAcceptCallGet.model_validate(data)
        return r

    def modify_selective_accept_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Modify Selective Accept Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: indicates whether selective accept is enabled or not.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept')
        super().put(url, params=params, json=body)

    def retrieve_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                           org_id: str = None) -> PlaceSelectiveAcceptCallCriteriaGet:
        """
        Retrieve Selective Accept Criteria for a Workspace

        Retrieve Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveAcceptCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveAcceptCallCriteriaGet.model_validate(data)
        return r

    def create_selective_accept_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                         calls_from: SelectiveRejectCallCallsFromType,
                                                         accept_enabled: bool, anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Selective Accept Criteria for a Workspace

        Create Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the selective accept is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective accept criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param accept_enabled: Choose to accept (if `acceptEnabled` = `true`) or not to accept (if `acceptEnabled` =
            `false`) the calls that fit within these parameters.
        :type accept_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['acceptEnabled'] = accept_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                         schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                         schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                         calls_from: SelectiveRejectCallCallsFromType = None,
                                                         anonymous_callers_enabled: bool = None,
                                                         unavailable_callers_enabled: bool = None,
                                                         phone_numbers: list[str] = None, accept_enabled: bool = None,
                                                         org_id: str = None):
        """
        Modify Selective Accept Criteria for a Workspace

        Modify Selective Accept Criteria Settings for a Workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the selective accept is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply the selective accept criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: SelectiveRejectCallCallsFromType
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param accept_enabled: Choose to accept (if `acceptEnabled` = `true`) or not to accept (if `acceptEnabled` =
            `false`) the calls that fit within these parameters.
        :type accept_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if accept_enabled is not None:
            body['acceptEnabled'] = accept_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_selective_accept_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Accept Criteria for a Workspace

        Delete Selective Accept criteria Settings for a workspace.

        With the Selective Accept feature, you can accept calls at specific times from specific callers.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveAccept/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_priority_alert_settings_for_a_workspace(self, workspace_id: str,
                                                         org_id: str = None) -> PriorityAlertGet:
        """
        Retrieve Priority Alert Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PriorityAlertGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert')
        data = super().get(url, params=params)
        r = PriorityAlertGet.model_validate(data)
        return r

    def configure_priority_alert_settings_for_a_workspace(self, workspace_id: str, enabled: bool, org_id: str = None):
        """
        Configure Priority Alert Settings for a Workspace

        Configure a workspace Priority Alert Settings.

        The priority alert feature enables administrator to configure priority alert settings for a professional
        workspace.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope that can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Priority Alert feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the workspace resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert')
        super().put(url, params=params, json=body)

    def retrieve_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                         org_id: str = None) -> PlacePriorityAlertCriteriaGet:
        """
        Retrieve Priority Alert Criteria for a Workspace

        Retrieve Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlacePriorityAlertCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        data = super().get(url, params=params)
        r = PlacePriorityAlertCriteriaGet.model_validate(data)
        return r

    def create_priority_alert_criteria_for_a_workspace(self, workspace_id: str, schedule_name: str,
                                                       schedule_type: SequentialRingCriteriaGetScheduleType,
                                                       schedule_level: SequentialRingCriteriaGetScheduleLevel,
                                                       calls_from: SequentialRingCriteriaGetCallsFrom,
                                                       notification_enabled: bool,
                                                       anonymous_callers_enabled: bool = None,
                                                       unavailable_callers_enabled: bool = None,
                                                       phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Priority Alert Criteria for a Workspace

        Create Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param schedule_name: Name of the location's schedule which determines when the priority alert is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e. Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone
            Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param notification_enabled: When set to `true` priority alerting criteria is enabled for calls that meet the
            current criteria. Criteria with `notificationEnabled` set to `false` take priority.
        :type notification_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['notificationEnabled'] = notification_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str, schedule_name: str = None,
                                                       schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                       schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                       calls_from: SequentialRingCriteriaGetCallsFrom = None,
                                                       anonymous_callers_enabled: bool = None,
                                                       unavailable_callers_enabled: bool = None,
                                                       phone_numbers: list[str] = None,
                                                       notification_enabled: bool = None, org_id: str = None):
        """
        Modify Priority Alert Criteria for a Workspace

        Modify Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the location's schedule which determines when the priority alert is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e. Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param calls_from: Indicates whether to apply priority alert for calls from Any Phone Number or Select Phone
            Numbers.
        :type calls_from: SequentialRingCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match.
        :type phone_numbers: list[str]
        :param notification_enabled: When set to `true` priority alerting criteria is enabled for calls that meet the
            current criteria. Criteria with `notificationEnabled` set to `false` take priority.
        :type notification_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_priority_alert_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Priority Alert Criteria for a Workspace

        Delete Priority Alert criteria Settings for a workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.
        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        This API requires a full, user, or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/priorityAlert/criteria/{id}')
        super().delete(url, params=params)

    def retrieve_selective_forward_settings_for_a_workspace(self, workspace_id: str,
                                                            org_id: str = None) -> SelectiveForwardCallGet:
        """
        Retrieve Selective Forward Settings for a Workspace

        Retrieve Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward')
        data = super().get(url, params=params)
        r = SelectiveForwardCallGet.model_validate(data)
        return r

    def modify_selective_forward_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                          default_phone_number_to_forward: str = None,
                                                          ring_reminder_enabled: bool = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Selective Forward Settings for a Workspace

        Modify Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if the Selective Forward feature is enabled.
        :type enabled: bool
        :param default_phone_number_to_forward: Enter the phone number to forward calls to during this schedule.
        :type default_phone_number_to_forward: str
        :param ring_reminder_enabled: When `true`, enables a ring reminder for such calls.
        :type ring_reminder_enabled: bool
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if default_phone_number_to_forward is not None:
            body['defaultPhoneNumberToForward'] = default_phone_number_to_forward
        if ring_reminder_enabled is not None:
            body['ringReminderEnabled'] = ring_reminder_enabled
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward')
        super().put(url, params=params, json=body)

    def retrieve_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                            org_id: str = None) -> PlaceSelectiveForwardCallCriteriaGet:
        """
        Retrieve Selective Forward Criteria for a Workspace

        Retrieve Selective Forward Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PlaceSelectiveForwardCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        data = super().get(url, params=params)
        r = PlaceSelectiveForwardCallCriteriaGet.model_validate(data)
        return r

    def create_selective_forward_criteria_for_a_workspace(self, workspace_id: str,
                                                          calls_from: CallsFromTypeForSelectiveForward,
                                                          forward_to_phone_number: str = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          numbers: list[str] = None, forward_enabled: bool = None,
                                                          org_id: str = None) -> str:
        """
        Create Selective Forward Criteria for a Workspace

        Create Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param calls_from: Indicates whether to apply the selective forward criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: CallsFromTypeForSelectiveForward
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true`, enables selective forward to calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables selective forward to calls if the callers are
            unavailable.
        :type unavailable_callers_enabled: bool
        :param numbers: List of phone numbers checked against incoming calls for a match.
        :type numbers: list[str]
        :param forward_enabled: Indicates whether the calls, that fit within these parameters, will be forwarded (if
            forwardEnabled = `true`) or not (if forwardEnabled = `false`).
        :type forward_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
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
        if numbers is not None:
            body['numbers'] = numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str,
                                                          calls_from: CallsFromTypeForSelectiveForward,
                                                          forward_to_phone_number: str = None,
                                                          destination_voicemail_enabled: bool = None,
                                                          schedule_name: str = None,
                                                          schedule_type: SequentialRingCriteriaGetScheduleType = None,
                                                          schedule_level: SequentialRingCriteriaGetScheduleLevel = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          numbers: list[str] = None, forward_enabled: bool = None,
                                                          org_id: str = None):
        """
        Modify Selective Forward Criteria for a Workspace

        Modify Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param calls_from: Indicates whether to apply the selective forward criteria for calls from Any Phone Number,
            Select Phone Numbers or Forwarded ones.
        :type calls_from: CallsFromTypeForSelectiveForward
        :param forward_to_phone_number: Phone number to forward calls to during this schedule.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Enables forwarding for all calls to voicemail. This option is only
            available for internal phone numbers or extensions.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the location's schedule which determines when the selective forward is in effect.
        :type schedule_name: str
        :param schedule_type: The Schedule type whether `businessHours` or `holidays`.
        :type schedule_type: SequentialRingCriteriaGetScheduleType
        :param schedule_level: The Schedule level i.e, Group.
        :type schedule_level: SequentialRingCriteriaGetScheduleLevel
        :param anonymous_callers_enabled: When `true`, enables selective forward to calls from anonymous callers.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables selective forward to calls if the callers are
            unavailable.
        :type unavailable_callers_enabled: bool
        :param numbers: List of phone numbers checked against incoming calls for a match.
        :type numbers: list[str]
        :param forward_enabled: Indicates whether the calls, that fit within these parameters, will be forwarded (if
            forwardEnabled = `true`) or not (if forwardEnabled = `false`).
        :type forward_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
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
        if numbers is not None:
            body['numbers'] = numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_selective_forward_criteria_for_a_workspace(self, workspace_id: str, id: str, org_id: str = None):
        """
        Delete Selective Forward Criteria for a Workspace

        Delete Selective Forward Call criteria Settings for a workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/selectiveForward/criteria/{id}')
        super().delete(url, params=params)

    def get_workspace_fax_message_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's FAX message number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_secondary_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's secondary number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)
