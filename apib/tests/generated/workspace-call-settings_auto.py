from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AuthorizationCode', 'CLIDPolicySelection', 'CallForwardingBusyGet', 'CallForwardingNoAnswerGet', 'CallForwardingPlaceSettingGet', 'CallWaiting', 'CallingPermission', 'CallingPermissionAction', 'CallingPermissionCallType', 'ExternalCallerIdNamePolicy', 'InterceptAnnouncementsGet', 'InterceptAnnouncementsGetGreeting', 'InterceptAnnouncementsPatch', 'InterceptGet', 'InterceptIncomingGet', 'InterceptIncomingGetType', 'InterceptIncomingPatch', 'InterceptNumberGet', 'InterceptOutGoingGet', 'InterceptOutGoingGetType', 'InterceptPatch', 'ListNumbersAssociatedWithASpecificWorkspaceResponse', 'Location', 'ModifyPlaceCallForwardSettings', 'ModifyPlaceCallerIdGet', 'MonitoredElementCallParkExtension', 'MonitoredElementItem', 'MonitoredElementUser', 'MonitoredElementUserType', 'PhoneNumbers', 'PlaceCallerIdGet', 'TransferNumberGet', 'UserInboundPermissionGet', 'UserInboundPermissionGetExternalTransfer', 'UserMonitoringGet', 'UserMonitoringPatch', 'UserNumberItem', 'UserOutgoingPermissionGet', 'UserPlaceAuthorizationCodeListGet', 'UserPlaceAuthorizationCodeListPatch', 'Workspace']


class AuthorizationCode(ApiModel):
    #: Indicates an access code.
    #: example: 4856
    code: Optional[datetime] = None
    #: Indicates the description of the access code.
    #: example: Marketing's access code
    description: Optional[str] = None


class CLIDPolicySelection(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the value from the `customNumber` field.
    custom = 'CUSTOM'


class CallForwardingBusyGet(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: +19075552859
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingNoAnswerGet(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: +19075552859
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 2.0
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 20.0
    system_max_number_of_rings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    #: example: True
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPlaceSettingGet(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the workspace is busy.
    busy: Optional[CallForwardingBusyGet] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingNoAnswerGet] = None


class CallWaiting(ApiModel):
    #: Call Waiting state.
    #: example: True
    enabled: Optional[bool] = None


class CallingPermissionCallType(str, Enum):
    #: Indicates the internal call type.
    internal_call = 'INTERNAL_CALL'
    #: Indicates the toll free call type.
    toll_free = 'TOLL_FREE'
    #: Indicates the international call type.
    international = 'INTERNATIONAL'
    #: Indicates the operator assisted call type.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Indicates the chargeable directory assisted call type.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Indicates the special services I call type.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Indicates the special services II call type.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Indicates the premium services I call type.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Indicates the premium services II call type.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Indicates the national call type.
    national = 'NATIONAL'


class CallingPermissionAction(str, Enum):
    #: The call type is allowed.
    allow = 'ALLOW'
    #: The call type is blocked.
    block = 'BLOCK'
    #: Indicates access code action for the specified call type.
    auth_code = 'AUTH_CODE'
    #: Indicates transfer number 1 for the specified call type.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Indicates transfer number 2 for the specified call type.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Indicates transfer number 3 for the specified call type.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermission(ApiModel):
    #: Type of the outgoing call.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionCallType] = None
    #: Indicates permission for call types.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: Indicate calling permission for call type enable status.
    #: example: True
    transfer_enabled: Optional[bool] = None


class ExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the `locationExternalCallerIdName` field.
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
    #: Indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Filename of the custom greeting; this is an empty string if no custom greeting has been uploaded.
    #: example: incoming.wav
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptAnnouncementsPatch(ApiModel):
    #: Indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptIncomingGetType(str, Enum):
    #: All incoming calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class InterceptIncomingGet(ApiModel):
    #: Indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptIncomingGetType] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsGet] = None


class InterceptOutGoingGetType(str, Enum):
    #: Outgoing calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class InterceptOutGoingGet(ApiModel):
    #: Indicated all outgoing calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptOutGoingGetType] = None
    #: If `true`, when the person attempts to make an outbound call, a system default message is played and the call is made to the destination phone number.
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
    #: Indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[InterceptIncomingGetType] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    #: example: True
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsPatch] = None


class InterceptPatch(ApiModel):
    #: `true` if call interception is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingPatch] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptOutGoingGet] = None


class ModifyPlaceCallForwardSettings(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingGet] = None


class ModifyPlaceCallerIdGet(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    #: example: DIRECT_LINE
    selected: Optional[CLIDPolicySelection] = None
    #: This value must be an assigned number from the workspace's location.
    #: example: +12815550003
    custom_number: Optional[str] = None
    #: Workspace's caller ID display name.
    #: example: Clockmaker's shop 7.1
    display_name: Optional[str] = None
    #: Workspace's caller ID display details.
    #: example: .
    display_detail: Optional[str] = None
    #: Flag to block call forwarding.
    #: example: True
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy] = None
    #: Custom External Caller Name, which will be shown if External Caller ID Name is `OTHER`.
    #: example: Custom external caller name
    custom_external_caller_id_name: Optional[str] = None
    #: External Caller Name, which will be shown if External Caller ID Name is `OTHER`.
    #: example: Anna
    location_external_caller_id_name: Optional[str] = None


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: Name of call park extension.
    #: example: CPE1
    name: Optional[str] = None
    #: Extension of call park extension.
    #: example: 8080
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
    #: If `true`, the primary number.
    #: example: True
    primary: Optional[bool] = None


class PlaceCallerIdGet(ApiModel):
    #: Allowed types for the `selected` field.
    types: Optional[list[CLIDPolicySelection]] = None
    #: Which type of outgoing Caller ID will be used.
    #: example: DIRECT_LINE
    selected: Optional[CLIDPolicySelection] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    #: example: +12815550003
    direct_number: Optional[str] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected
    #: example: +12815550002
    location_number: Optional[str] = None
    #: Flag for specifying a toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: This value must be an assigned number from the person's location.
    #: example: +12815550003
    custom_number: Optional[str] = None
    #: Workspace's caller ID display name.
    #: example: Clockmaker's shop 7.1
    display_name: Optional[str] = None
    #: Workspace's caller ID display details. Default is `.`.
    #: example: .
    display_detail: Optional[str] = None
    #: Flag to block call forwarding.
    #: example: True
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy] = None
    #: Custom External Caller Name, which will be shown if External Caller ID Name is `OTHER`.
    #: example: Custom external caller name
    custom_external_caller_id_name: Optional[str] = None
    #: External Caller Name, which will be shown if External Caller ID Name is `OTHER`.
    #: example: Anna
    location_external_caller_id_name: Optional[str] = None


class TransferNumberGet(ApiModel):
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
    #: Indicate call transfer setting.
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


class UserMonitoringPatch(ApiModel):
    #: Call park notification is enabled or disabled.
    #: example: True
    enable_call_park_notification: Optional[bool] = None
    #: Array of ID strings of monitored elements.
    monitored_elements: Optional[list[str]] = None


class UserOutgoingPermissionGet(ApiModel):
    #: Outgoing Permission state. If disabled, the default settings are used.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]] = None


class UserPlaceAuthorizationCodeListGet(ApiModel):
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]] = None


class UserPlaceAuthorizationCodeListPatch(ApiModel):
    #: Indicates access codes to delete.
    delete_codes: Optional[list[str]] = None


class Location(ApiModel):
    #: Location identifier associated with the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    id: Optional[str] = None
    #: Location name associated with the workspace.
    #: example: MainOffice
    name: Optional[str] = None


class Workspace(ApiModel):
    #: Workspace ID associated with the list of numbers.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzg0MjkzOGQ1LTkyNzMtNGJjNi1hYTNhLTA1Njc3MmRiMzE2NQ
    id: Optional[str] = None


class ListNumbersAssociatedWithASpecificWorkspaceResponse(ApiModel):
    #: Array of numbers primary followed by alternate numbers.
    phone_numbers: Optional[list[PhoneNumbers]] = None
    #: Workspace object having a unique identifier for the Workspace.
    workspace: Optional[Workspace] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None
    #: Organization object having a unique identifier for the organization and its name.
    organization: Optional[Location] = None
