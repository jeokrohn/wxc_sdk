from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AgentCallerIdType', 'AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
           'AudioAnnouncementFileGetObjectMediaFileType', 'AuthorizationCode', 'AuthorizationCodeLevel',
           'AvailableCallerIdObject', 'BargeInInfo', 'CallForwardingInfo', 'CallForwardingInfoCallForwarding',
           'CallForwardingInfoCallForwardingAlways', 'CallForwardingInfoCallForwardingBusy',
           'CallForwardingInfoCallForwardingNoAnswer', 'CallForwardingPutCallForwarding',
           'CallForwardingPutCallForwardingNoAnswer', 'CallInterceptInfo', 'CallInterceptInfoIncoming',
           'CallInterceptInfoIncomingAnnouncements', 'CallInterceptInfoIncomingAnnouncementsGreeting',
           'CallInterceptInfoIncomingAnnouncementsNewNumber', 'CallInterceptInfoIncomingType',
           'CallInterceptInfoOutgoing', 'CallInterceptInfoOutgoingType', 'CallInterceptPutIncoming',
           'CallInterceptPutIncomingAnnouncements', 'CallRecordingInfo', 'CallRecordingInfoNotification',
           'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord', 'CallRecordingInfoRepeat',
           'CallRecordingInfoStartStopAnnouncement', 'CallRecordingPutNotification',
           'CallRecordingPutNotificationType', 'CallerIdInfo', 'CallerIdInfoSelected', 'DectNetwork',
           'DeviceActivationStates', 'DeviceObject', 'DeviceOwner', 'DevicesObject', 'DirectLineCallerIdNameObject',
           'DirectorySearchObject', 'GetMusicOnHoldObject', 'GetVirtualLineDevicesObject',
           'GetVirtualLineNumberObjectPhoneNumber', 'GetVirtualLineObject', 'GetVirtualLineObjectLocation',
           'GetVirtualLineObjectLocationAddress', 'GetVirtualLineObjectNumber', 'IncomingPermissionSetting',
           'IncomingPermissionSettingExternalTransfer', 'LineType', 'ListVirtualLineObject',
           'ListVirtualLineObjectExternalCallerIdNamePolicy', 'ListVirtualLineObjectLocation',
           'ListVirtualLineObjectNumber', 'MemberType', 'MonitoredPersonObject', 'NumberOwnerType',
           'OutgoingCallingPermissionsSettingGet', 'OutgoingCallingPermissionsSettingGetCallingPermissionsItem',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType',
           'OutgoingCallingPermissionsSettingPutCallingPermissionsItem', 'PeopleOrPlaceOrVirtualLineType',
           'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PushToTalkInfo', 'STATE',
           'TelephonyType', 'TransferNumberGet', 'UserDigitPatternObject',
           'UserOutgoingPermissionDigitPatternGetListObject', 'UserPlaceAuthorizationCodeListGet',
           'UserSelectionObject', 'VirtualLineCallForwardAvailableNumberObject',
           'VirtualLineCallForwardAvailableNumberObjectOwner', 'VirtualLineCallSettingsApi',
           'VirtualLineDoNotDisturbGet', 'VirtualLineECBNAvailableNumberObject',
           'VirtualLineECBNAvailableNumberObjectOwner', 'VirtualLineECBNAvailableNumberObjectOwnerType',
           'VirtualLineFaxMessageAvailableNumberObject', 'VoicemailInfo', 'VoicemailInfoEmailCopyOfMessage',
           'VoicemailInfoFaxMessage', 'VoicemailInfoMessageStorage', 'VoicemailInfoMessageStorageStorageType',
           'VoicemailInfoSendBusyCalls', 'VoicemailInfoSendUnansweredCalls', 'VoicemailPutSendBusyCalls',
           'VoicemailPutSendUnansweredCalls']


class AuthorizationCodeLevel(str, Enum):
    #: Indicates the location level access code.
    location = 'LOCATION'
    #: Indicates the user level access code.
    custom = 'CUSTOM'


class AuthorizationCode(ApiModel):
    #: Indicates an access code.
    code: Optional[str] = None
    #: Indicates the description of the access code.
    description: Optional[str] = None
    #: Indicates the level of each access code.
    level: Optional[AuthorizationCodeLevel] = None


class ListVirtualLineObjectExternalCallerIdNamePolicy(str, Enum):
    #: Shows virtual lines Caller ID name.
    direct_line = 'DIRECT_LINE'
    #: Shows virtual lines location name.
    location = 'LOCATION'
    #: Allow virtual lines first/last name to be configured.
    other = 'OTHER'


class ListVirtualLineObjectNumber(ApiModel):
    #: Virtual Line external.  Either `external` or `extension` is mandatory.
    external: Optional[str] = None
    #: Virtual Line extension.  Either `external` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Number is Primary or Alternative Number.
    primary: Optional[bool] = None


class ListVirtualLineObjectLocation(ApiModel):
    #: ID of location associated with virtual line.
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    name: Optional[str] = None


class ListVirtualLineObject(ApiModel):
    #: A unique identifier for the virtual line.
    id: Optional[str] = None
    #: Last name for virtual line.
    last_name: Optional[str] = None
    #: First name for virtual line.
    first_name: Optional[str] = None
    #: `callerIdLastName` for virtual line.
    caller_id_last_name: Optional[str] = None
    #: `callerIdFirstName` for virtual line.
    caller_id_first_name: Optional[str] = None
    #: `callerIdNumber` for virtual line.
    caller_id_number: Optional[str] = None
    #: `externalCallerIdNamePolicy` for the virtual line.
    external_caller_id_name_policy: Optional[ListVirtualLineObjectExternalCallerIdNamePolicy] = None
    #: `customExternalCallerIdName` for virtual line.
    custom_external_caller_id_name: Optional[str] = None
    #: Calling details of virtual line.
    number: Optional[ListVirtualLineObjectNumber] = None
    #: Location details of virtual line.
    location: Optional[ListVirtualLineObjectLocation] = None
    #: Number of devices assigned to a virtual line.
    number_of_devices_assigned: Optional[int] = None
    #: Type of billing plan.
    billing_plan: Optional[str] = None


class CallRecordingInfoRecord(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (`*44`) has been entered. Pause, resume, and stop
    #: controls are supported.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class CallRecordingInfoNotificationType(str, Enum):
    #: No notification sound played when call recording is paused or resumed.
    none_ = 'None'
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class CallRecordingInfoNotification(ApiModel):
    #: Type of pause/resume notification.
    type: Optional[CallRecordingInfoNotificationType] = None
    #: `true` when the notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class CallRecordingInfoRepeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    interval: Optional[int] = None
    #: `true` when ongoing call recording tone will be played at the designated interval. `false` indicates no warning
    #: tone will be played.
    enabled: Optional[bool] = None


class CallRecordingInfoStartStopAnnouncement(ApiModel):
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for internal calls.
    internal_calls_enabled: Optional[bool] = None
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for PSTN calls.
    pstn_calls_enabled: Optional[bool] = None


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    enabled: Optional[bool] = None
    #: Call recording scenario.
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Name of the service provider providing call recording service.
    service_provider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    external_group: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    external_identifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[CallRecordingInfoStartStopAnnouncement] = None


class CallRecordingPutNotificationType(str, Enum):
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class CallRecordingPutNotification(ApiModel):
    #: Type of pause/resume notification. If `enabled` is `true` and `type` is not provided then `type` is set to
    #: `Beep` by default.
    type: Optional[CallRecordingPutNotificationType] = None
    #: `true` when notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class GetVirtualLineObjectNumber(ApiModel):
    #: Phone number of a virtual line.  Either `external` or `extension` is mandatory.
    external: Optional[str] = None
    #: Extension of a virtual line.  Either `external` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Number is Primary or Alternative Number.
    primary: Optional[bool] = None


class GetVirtualLineObjectLocationAddress(ApiModel):
    #: Address 1 of the location.
    address1: Optional[str] = None
    #: Address 2 of the location.
    address2: Optional[str] = None
    #: City of the location.
    city: Optional[str] = None
    #: State code of the location.
    state: Optional[str] = None
    #: Postal code of the location.
    postal_code: Optional[str] = None
    #: ISO-3166 2-Letter country code of the location.
    country: Optional[str] = None


class GetVirtualLineObjectLocation(ApiModel):
    #: ID of location associated with virtual line.
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    name: Optional[str] = None
    #: The address of the virtual line.
    address: Optional[GetVirtualLineObjectLocationAddress] = None


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


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str] = None
    #: Enumeration that indicates if the member is of type `PEOPLE` or `PLACE`.
    type: Optional[MemberType] = None
    #: First name of device owner.
    first_name: Optional[str] = None
    #: Last name of device owner.
    last_name: Optional[str] = None


class DeviceActivationStates(str, Enum):
    #: Indicates a device is activating.
    activating = 'ACTIVATING'
    #: Indicates a device is activated.
    activated = 'ACTIVATED'
    #: Indicates a device is deactivated.
    deactivated = 'DEACTIVATED'


class DevicesObject(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Owner of the device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of a device.
    activation_state: Optional[DeviceActivationStates] = None


class GetVirtualLineObject(ApiModel):
    #: A unique identifier for the virtual line.
    id: Optional[str] = None
    #: First name defined for a virtual line. Minimum length is 1. Maximum length is 64.
    first_name: Optional[str] = None
    #: Last name defined for a virtual line. Minimum length is 1. Maximum length is 64.
    last_name: Optional[str] = None
    #: Display name defined for a virtual line.
    display_name: Optional[str] = None
    #: Flag to indicate a directory search.
    directory_search_enabled: Optional[bool] = None
    #: Virtual Line's announcement language.
    announcement_language: Optional[str] = None
    #: Time zone defined for the virtual line.
    time_zone: Optional[str] = None
    #: Calling details of virtual line.
    number: Optional[GetVirtualLineObjectNumber] = None
    #: List of devices assigned to a virtual line.
    devices: Optional[list[DevicesObject]] = None
    #: Location details of virtual line.
    location: Optional[GetVirtualLineObjectLocation] = None


class GetVirtualLineNumberObjectPhoneNumber(ApiModel):
    #: Phone number that is assigned to a virtual line.
    direct_number: Optional[str] = None
    #: Extension that is assigned to a virtual line.
    extension: Optional[str] = None
    #: If `true` marks the phone number as primary.
    primary: Optional[bool] = None


class DirectorySearchObject(ApiModel):
    #: Whether or not the directory search for a virtual line is enabled.
    enabled: Optional[bool] = None


class DeviceObject(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Owner of the device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of a device.
    activation_state: Optional[DeviceActivationStates] = None
    #: Location details of virtual line.
    location: Optional[ListVirtualLineObjectLocation] = None


class GetVirtualLineDevicesObject(ApiModel):
    #: List of devices assigned to a virtual line.
    devices: Optional[list[DeviceObject]] = None
    #: Indicates to which line a device can be assigned.
    available_endpoint_type: Optional[LineType] = None
    #: Maximum number of devices a virtual line can be assigned to.
    max_device_count: Optional[int] = None


class DectNetwork(ApiModel):
    #: Unique identifier for a DECT network.
    id: Optional[str] = None
    #: Identifier for device DECT network.
    name: Optional[str] = None
    #: Indicates whether the virtual profile is the primary line.
    primary_enabled: Optional[bool] = None
    #: Number of DECT handsets assigned to the virtual profile.
    number_of_handsets_assigned: Optional[int] = None
    #: Location details of virtual line.
    location: Optional[ListVirtualLineObjectLocation] = None


class CallerIdInfoSelected(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the value from the customNumber field.
    custom = 'CUSTOM'


class UserSelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this virtual line.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `firstName` and `lastName` are to be shown for this virtual line.
    first_name_last_name = 'FIRST_NAME_LAST_NAME'
    #: When this option is selected, `lastName` and `firstName` are to be shown for this virtual line.
    last_name_first_name = 'LAST_NAME_FIRST_NAME'
    #: When this option is selected, `displayName` is to be shown for this virtual line.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `FIRST_NAME_LAST_NAME`.
    selection: Optional[UserSelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class CallerIdInfo(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CallerIdInfoSelected]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    selected: Optional[CallerIdInfoSelected] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    direct_number: Optional[str] = None
    #: Extension number of the virtual line.
    extension_number: Optional[str] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected.
    location_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: Custom number which will be shown if CUSTOM is selected. This value must be a number from the virtual line's
    #: location or from another location with the same country, PSTN provider, and zone (only applicable for India
    #: locations) as the virtual line's location.
    custom_number: Optional[str] = None
    #: Virtual line's Caller ID first name. The characters `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: This field has been deprecated. Please use `directLineCallerIdName` and `dialByFirstName` instead.
    first_name: Optional[str] = None
    #: Virtual line's Caller ID last name. The characters `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: This field has been deprecated. Please use `directLineCallerIdName` and `dialByLastName` instead.
    last_name: Optional[str] = None
    #: Block this virtual line's identity when receiving a call.
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    external_caller_id_name_policy: Optional[ListVirtualLineObjectExternalCallerIdNamePolicy] = None
    #: Custom external caller ID name which will be shown if external caller ID name policy is `OTHER`.
    custom_external_caller_id_name: Optional[str] = None
    #: Location's external caller ID name which will be shown if external caller ID name policy is `LOCATION`.
    location_external_caller_id_name: Optional[str] = None
    #: Flag to indicate the virtual line's direct line number is available as an additional external caller ID for the
    #: virtual line.
    additional_external_caller_id_direct_line_enabled: Optional[bool] = None
    #: Flag to indicate the location main number is available as an additional external caller ID for the virtual line.
    additional_external_caller_id_location_number_enabled: Optional[bool] = None
    #: The custom number available as an additional external caller ID for the virtual line. This value must be a
    #: number from the virtual line's location or from another location with the same country, PSTN provider, and zone
    #: (only applicable for India locations) as the virtual line's location.
    additional_external_caller_id_custom_number: Optional[str] = None
    #: Settings for the direct line caller ID name to be shown for this virtual line.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The first name to be used for dial-by-name functions.
    dial_by_first_name: Optional[str] = None
    #: The last name to be used for dial-by-name functions.
    dial_by_last_name: Optional[str] = None


class CallForwardingInfoCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the virtual line's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an
    #: internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None
    #: Indicates the enabled or disabled state of sending incoming calls to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the virtual
    #: line is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingInfoCallForwardingNoAnswer] = None


class CallForwardingInfo(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwardingInfoCallForwarding] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[CallForwardingInfoCallForwardingBusy] = None


class CallForwardingPutCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered. `numberOfRings` must be between 2 and 20,
    #: inclusive.
    number_of_rings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPutCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingInfoCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the virtual
    #: line is busy.
    busy: Optional[CallForwardingInfoCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingPutCallForwardingNoAnswer] = None


class IncomingPermissionSettingExternalTransfer(str, Enum):
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class IncomingPermissionSetting(ApiModel):
    #: When true, indicates that this virtual line uses the specified calling permissions for receiving inbound calls
    #: rather than the organizational defaults.
    use_custom_enabled: Optional[bool] = None
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: Optional[IncomingPermissionSettingExternalTransfer] = None
    #: Internal calls are allowed to be received.
    internal_calls_enabled: Optional[bool] = None
    #: Collect calls are allowed to be received.
    collect_calls_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the
    #: originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before
    #: the number is dialed.
    international = 'INTERNATIONAL'
    #: Controls calls requiring Operator Assistance.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Controls calls to Directory Assistant companies that require a charge to connect the call.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Controls calls that are within your country of origin, both within and outside of your local area code.
    national = 'NATIONAL'


class OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction(str, Enum):
    #: Allow the designated call type.
    allow = 'ALLOW'
    #: Block the designated call type.
    block = 'BLOCK'
    #: Allow only via Authorization Code.
    auth_code = 'AUTH_CODE'
    #: Transfer to Auto Transfer Number 1. The answering virtual line can then approve the call and send it through or
    #: reject the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering virtual line can then approve the call and send it through or
    #: reject the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering virtual line can then approve the call and send it through or
    #: reject the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class OutgoingCallingPermissionsSettingGetCallingPermissionsItem(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType] = None
    #: Action on the given `callType`.
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Indicates if the restriction is enforced by the system for the corresponding call type and cannot be changed.
    #: For example, certain call types (such as `INTERNATIONAL`) may be permanently blocked and this field will be
    #: `true` to reflect that the restriction is system-controlled and not editable.
    is_call_type_restriction_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSettingGet(ApiModel):
    #: When true, indicates that this user uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    use_custom_enabled: Optional[bool] = None
    #: When true, indicates that this user uses the specified outgoing calling permissions when placing outbound calls.
    use_custom_permissions: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[OutgoingCallingPermissionsSettingGetCallingPermissionsItem]] = None


class OutgoingCallingPermissionsSettingPutCallingPermissionsItem(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemCallType] = None
    #: Action on the given `callType`.
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction] = None
    #: Allow the virtual line to transfer or forward a call of the specified call type.
    transfer_enabled: Optional[bool] = None


class CallInterceptInfoIncomingType(str, Enum):
    #: Incoming calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class CallInterceptInfoIncomingAnnouncementsGreeting(str, Enum):
    #: A custom greeting is played when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default greeting will be played when incoming calls are intercepted.
    default = 'DEFAULT'


class CallInterceptInfoIncomingAnnouncementsNewNumber(ApiModel):
    #: If `true`, the caller will hear this new number when the call is intercepted.
    enabled: Optional[bool] = None
    #: New number caller will hear announced.
    destination: Optional[str] = None


class CallInterceptInfoIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Filename of custom greeting; will be an empty string if no custom greeting has been uploaded.
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptInfoIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the virtual line's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptInfoIncomingAnnouncements] = None


class CallInterceptInfoOutgoingType(str, Enum):
    #: Outgoing calls are routed as the destination and voicemail specify.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class CallInterceptInfoOutgoing(ApiModel):
    #: `INTERCEPT_ALL` indicated all outgoing calls are intercepted.
    type: Optional[CallInterceptInfoOutgoingType] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    destination: Optional[str] = None


class CallInterceptInfo(ApiModel):
    #: `true` if call intercept is enabled.
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[CallInterceptInfoIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[CallInterceptInfoOutgoing] = None


class CallInterceptPutIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptPutIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the virtual line's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptPutIncomingAnnouncements] = None


class AgentCallerIdType(str, Enum):
    #: A call queue has been selected for the agent's caller ID.
    call_queue = 'CALL_QUEUE'
    #: A hunt group has been selected for the agent's caller ID.
    hunt_group = 'HUNT_GROUP'


class AvailableCallerIdObject(ApiModel):
    #: Call queue or hunt group's unique identifier.
    id: Optional[str] = None
    #: Member is of type `CALL_QUEUE` or `HUNT_GROUP`.
    type: Optional[AgentCallerIdType] = None
    #: Call queue or hunt group's name.
    name: Optional[str] = None
    #: When not null, it is call queue or hunt group's phone number.
    phone_number: Optional[str] = None
    #: When not null, it is call queue or hunt group's extension number.
    extension: Optional[str] = None


class VoicemailInfoSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Indicates a custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None


class VoicemailInfoSendUnansweredCalls(ApiModel):
    #: Enables and disables sending unanswered calls to voicemail.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Indicates a custom greeting has been uploaded.
    greeting_uploaded: Optional[bool] = None
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None


class VoicemailInfoEmailCopyOfMessage(ApiModel):
    #: When `true` copy of new voicemail message audio will be sent to the designated email.
    enabled: Optional[bool] = None
    #: Email address to which the new voicemail audio will be sent.
    email_id: Optional[str] = None


class VoicemailInfoMessageStorageStorageType(str, Enum):
    #: For message access via phone or the Calling User Portal.
    internal = 'INTERNAL'
    #: For sending all messages to the virtual line's email.
    external = 'EXTERNAL'


class VoicemailInfoMessageStorage(ApiModel):
    #: When `true` desktop phone will indicate there are new voicemails.
    mwi_enabled: Optional[bool] = None
    #: Designates which type of voicemail message storage is used.
    storage_type: Optional[VoicemailInfoMessageStorageStorageType] = None
    #: External email address to which the new voicemail audio will be sent.  A value for this field must be provided
    #: in the request if a `storageType` of `EXTERNAL` is given in the request.
    external_email: Optional[str] = None


class VoicemailInfoFaxMessage(ApiModel):
    #: When `true` FAX messages for new voicemails are sent to the designated number.
    enabled: Optional[bool] = None
    #: Designates a phone number for the FAX. A value for this field must be provided in the request if the faxMessage
    #: `enabled` field is given as `true` in the request.
    phone_number: Optional[str] = None
    #: Designates optional extension for the FAX.
    extension: Optional[str] = None


class VoicemailInfo(ApiModel):
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[DirectorySearchObject] = None
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[VoicemailInfoSendBusyCalls] = None
    send_unanswered_calls: Optional[VoicemailInfoSendUnansweredCalls] = None
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Settings for sending a copy of the new voicemail message audio via email.
    email_copy_of_message: Optional[VoicemailInfoEmailCopyOfMessage] = None
    message_storage: Optional[VoicemailInfoMessageStorage] = None
    fax_message: Optional[VoicemailInfoFaxMessage] = None
    #: Disable the user-level control when set to `false`.
    voice_message_forwarding_enabled: Optional[bool] = None
    #: Language code.
    announcement_language_code: Optional[str] = None


class VoicemailPutSendBusyCalls(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None


class VoicemailPutSendUnansweredCalls(ApiModel):
    #: Unanswered call sending to voicemail is enabled or disabled.
    enabled: Optional[bool] = None
    #: `DEFAULT` indicates the default greeting will be played. `CUSTOM` indicates a custom `.wav` file will be played.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Number of rings before an unanswered call will be sent to voicemail. `numberOfRings` must be between 2 and 20,
    #: inclusive.
    number_of_rings: Optional[int] = None


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies that this audio file is configured across the organization.
    organization = 'ORGANIZATION'
    #: Specifies that this audio file is configured across the location.
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


class GetMusicOnHoldObject(ApiModel):
    #: Music on hold is enabled or disabled for the virtual line.
    moh_enabled: Optional[bool] = None
    #: Music on hold is enabled or disabled for the location. The music on hold setting returned in the response is
    #: used only when music on hold is enabled at the location level. When `mohLocationEnabled` is `false` and
    #: `mohEnabled` is `true`, music on hold is disabled for the user. When `mohLocationEnabled` is `true` and
    #: `mohEnabled` is `false`
    #: 
    #: , music on hold is turned off for the virtual line. In both cases, music on hold will not be played.
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the virtual line.
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Announcement Audio File details when greeting is set to CUSTOM.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class PushToTalkAccessType(str, Enum):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the virtual line being
    #: configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the virtual line being
    #: configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk
    #: for can respond.
    two_way = 'TWO_WAY'


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    id: Optional[str] = None
    #: Last name of the person.
    last_name: Optional[str] = None
    #: First name of the person.
    first_name: Optional[str] = None
    #: Display name of the person.
    display_name: Optional[str] = None
    #: Type usually indicates `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Push-to-Talk and Privacy features only supports
    #: `PEOPLE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the person.
    email: Optional[str] = None
    #: List of phone numbers of the person.
    numbers: Optional[list[ListVirtualLineObjectNumber]] = None


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a person receives a Push-to-Talk call and
    #: answers the call automatically.
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]] = None


class BargeInInfo(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    enabled: Optional[bool] = None
    #: Indicates that a stutter dial tone will be played when a virtual line is barging in on the active call.
    tone_enabled: Optional[bool] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name will be enabled.
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only members specified by `monitoringAgents` can
    #: pickup or barge-in on the call.
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class VirtualLineFaxMessageAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
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


class VirtualLineCallForwardAvailableNumberObjectOwner(ApiModel):
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


class VirtualLineCallForwardAvailableNumberObject(ApiModel):
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
    owner: Optional[VirtualLineCallForwardAvailableNumberObjectOwner] = None


class VirtualLineECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Line.
    virtual_line = 'VIRTUAL_LINE'
    #: Phone number's owner is a Hunt Group.
    hunt_group = 'HUNT_GROUP'


class VirtualLineECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which phone number is assigned.
    id: Optional[str] = None
    #: Type of the phone number's owner.
    type: Optional[VirtualLineECBNAvailableNumberObjectOwnerType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE` or
    #: `HUNT_GROUP`.
    display_name: Optional[str] = None


class VirtualLineECBNAvailableNumberObject(ApiModel):
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
    owner: Optional[VirtualLineECBNAvailableNumberObjectOwner] = None


class UserPlaceAuthorizationCodeListGet(ApiModel):
    #: When `true`, use custom settings for the access codes category of outbound permissions.
    use_custom_access_codes: Optional[bool] = None
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]] = None


class UserDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches the digit pattern.
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class UserOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[UserDigitPatternObject]] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outbound permissions.
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber1` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_1`.
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber2` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_2`.
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber3` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_3`.
    auto_transfer_number3: Optional[str] = None


class VirtualLineDoNotDisturbGet(ApiModel):
    #: `true` if the DoNotDisturb feature is enabled.
    enabled: Optional[bool] = None
    #: When `true`, enables ring reminder when you receive an incoming call while on Do Not Disturb.
    ring_splash_enabled: Optional[bool] = None


class VirtualLineCallSettingsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Virtual Line Call Settings
    
    A virtual line allows administrators to configure multiple lines for Webex Calling users. Virtual Lines Settings
    support reading and writing of Webex Calling Virtual Lines and its configuration for a specific organization.
    
    Viewing these read-only organization settings requires a full, user, or read-only administrator auth token with a
    scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full or user administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_virtual_lines(self, location_id: list[str] = None, id: list[str] = None,
                                       owner_name: list[str] = None, phone_number: list[str] = None,
                                       location_name: list[str] = None, order: list[str] = None,
                                       has_device_assigned: bool = None, has_extension_assigned: bool = None,
                                       has_dn_assigned: bool = None, org_id: str = None,
                                       **params) -> Generator[ListVirtualLineObject, None, None]:
        """
        Read the List of Virtual Lines

        List all Virtual Lines for the organization.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            `?locationId=locId1&locationId=locId2`.
        :type location_id: list[str]
        :param id: Return the list of virtual lines matching these virtualLineIds. Example for multiple values -
            `?id=id1&id=id2`.
        :type id: list[str]
        :param owner_name: Return the list of virtual lines matching these owner names. Example for multiple values -
            `?ownerName=name1&ownerName=name2`.
        :type owner_name: list[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers. Example for multiple values
            - `?phoneNumber=number1&phoneNumber=number2`.
        :type phone_number: list[str]
        :param location_name: Return the list of virtual lines matching the location names. Example for multiple values
            - `?locationName=loc1&locationName=loc2`.
        :type location_name: list[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time. Example for multiple values - `?order=order1&order=order2`.
        :type order: list[str]
        :param has_device_assigned: If `true`, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If `true`, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If `true`, includes only virtual lines with an assigned directory number, also known as
            a Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListVirtualLineObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = ','.join(location_id)
        if id is not None:
            params['id'] = ','.join(id)
        if owner_name is not None:
            params['ownerName'] = ','.join(owner_name)
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if location_name is not None:
            params['locationName'] = ','.join(location_name)
        if order is not None:
            params['order'] = ','.join(order)
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = str(has_device_assigned).lower()
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = str(has_extension_assigned).lower()
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = str(has_dn_assigned).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListVirtualLineObject, item_key='virtualLines', params=params)

    def create_a_virtual_line(self, first_name: str, last_name: str, location_id: str, display_name: str = None,
                              phone_number: str = None, extension: str = None, caller_id_last_name: str = None,
                              caller_id_first_name: str = None, caller_id_number: str = None,
                              org_id: str = None) -> str:
        """
        Create a Virtual Line

        Create new Virtual Line for the given location.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Creating a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param first_name: First name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type first_name: str
        :param last_name: Last name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type last_name: str
        :param location_id: ID of location for virtual line.
        :type location_id: str
        :param display_name: Display name defined for a virtual line.
        :type display_name: str
        :param phone_number: Phone number of a virtual line. Minimum length is 1. Maximum length is 23. Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 10. Either `phoneNumber`
            or `extension` is mandatory.
        :type extension: str
        :param caller_id_last_name: Last name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_last_name: str
        :param caller_id_first_name: First name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_first_name: str
        :param caller_id_number: Phone number to appear as the CLID for all calls. Minimum length is 1. Maximum length
            is 23.
        :type caller_id_number: str
        :param org_id: Create the virtual line for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['firstName'] = first_name
        body['lastName'] = last_name
        if display_name is not None:
            body['displayName'] = display_name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        body['locationId'] = location_id
        if caller_id_last_name is not None:
            body['callerIdLastName'] = caller_id_last_name
        if caller_id_first_name is not None:
            body['callerIdFirstName'] = caller_id_first_name
        if caller_id_number is not None:
            body['callerIdNumber'] = caller_id_number
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_virtual_line_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                                 org_id: str = None,
                                                 **params) -> Generator[VirtualLineFaxMessageAvailableNumberObject, None, None]:
        """
        Get Virtual Line Available Phone Numbers

        List standard numbers that are available to be assigned as a virtual line's phone number.
        By default, this API returns unassigned numbers from all locations. To select the suitable number for
        assignment, ensure the virtual line's location ID is provided as the `locationId` request parameter.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`VirtualLineFaxMessageAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep('availableNumbers')
        return self.session.follow_pagination(url=url, model=VirtualLineFaxMessageAvailableNumberObject, item_key='phoneNumbers', params=params)

    def delete_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Delete a Virtual Line

        Delete the designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Deleting a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `identity:contacts_rw`.

        :param virtual_line_id: Delete the virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Delete the virtual line from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}')
        super().delete(url, params=params)

    def get_details_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> GetVirtualLineObject:
        """
        Get Details for a Virtual Line

        Retrieve Virtual Line details.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving virtual line details requires a full or user or read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: :class:`GetVirtualLineObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}')
        data = super().get(url, params=params)
        r = GetVirtualLineObject.model_validate(data)
        return r

    def update_a_virtual_line(self, virtual_line_id: str, first_name: str = None, last_name: str = None,
                              display_name: str = None, phone_number: str = None, extension: str = None,
                              announcement_language: str = None, caller_id_last_name: str = None,
                              caller_id_first_name: str = None, caller_id_number: str = None, time_zone: str = None,
                              org_id: str = None):
        """
        Update a Virtual Line

        Update the designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating a virtual line requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `identity:contacts_rw`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param first_name: First name defined for a virtual line. Minimum length is 1. Maximum length is 64.
        :type first_name: str
        :param last_name: Last name defined for a virtual line. Minimum length is 1. Maximum length is 64.
        :type last_name: str
        :param display_name: Display name defined for a virtual line.
        :type display_name: str
        :param phone_number: Phone number of a virtual line. Minimum length is 1. Maximum length is 23. Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 10. Either `phoneNumber`
            or `extension` is mandatory.
        :type extension: str
        :param announcement_language: Virtual Line's announcement language.
        :type announcement_language: str
        :param caller_id_last_name: Last name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 64.
        :type caller_id_last_name: str
        :param caller_id_first_name: First name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 128.
        :type caller_id_first_name: str
        :param caller_id_number: Phone number to appear as the CLID for all calls. Minimum length is 1. Maximum length
            is 23.
        :type caller_id_number: str
        :param time_zone: Time zone defined for the virtual line.
        :type time_zone: str
        :param org_id: Update virtual line settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if display_name is not None:
            body['displayName'] = display_name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if announcement_language is not None:
            body['announcementLanguage'] = announcement_language
        if caller_id_last_name is not None:
            body['callerIdLastName'] = caller_id_last_name
        if caller_id_first_name is not None:
            body['callerIdFirstName'] = caller_id_first_name
        if caller_id_number is not None:
            body['callerIdNumber'] = caller_id_number
        if time_zone is not None:
            body['timeZone'] = time_zone
        url = self.ep(f'{virtual_line_id}')
        super().put(url, params=params, json=body)

    def retrieve_agent_s_list_of_available_caller_ids(self, virtual_line_id: str,
                                                      org_id: str = None) -> list[AvailableCallerIdObject]:
        """
        Retrieve Agent's List of Available Caller IDs

        Get the list of call queues and hunt groups available for caller ID use by this virtual line as an agent.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param virtual_line_id: Unique identifier for the Virtual Line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the Virtual Line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: list[AvailableCallerIdObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/agent/availableCallerIds')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AvailableCallerIdObject]).validate_python(data['availableCallerIds'])
        return r

    def retrieve_agent_s_caller_id_information(self, virtual_line_id: str) -> AvailableCallerIdObject:
        """
        Retrieve Agent's Caller ID Information

        Retrieve the Agent's Caller ID Information.

        Each agent will be able to set their outgoing Caller ID as either the Call Queue's Caller ID, Hunt Group's
        Caller ID or their own configured Caller ID.

        This API requires a full admin or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the Virtual Line.
        :type virtual_line_id: str
        :rtype: AvailableCallerIdObject
        """
        url = self.ep(f'{virtual_line_id}/agent/callerId')
        data = super().get(url)
        r = AvailableCallerIdObject.model_validate(data['selectedCallerId'])
        return r

    def modify_agent_s_caller_id_information(self, virtual_line_id: str, selected_caller_id: str):
        """
        Modify Agent's Caller ID Information.

        Each Agent is able to set their outgoing Caller ID as either the designated Call Queue's Caller ID or the Hunt
        Group's Caller ID or their own configured Caller ID.
        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the Virtual Line.
        :type virtual_line_id: str
        :param selected_caller_id: The unique identifier of the call queue or hunt group to use for the agent's caller
            ID. Set to null to use the agent's own caller ID.
        :type selected_caller_id: str
        :rtype: None
        """
        body = dict()
        body['selectedCallerId'] = selected_caller_id
        url = self.ep(f'{virtual_line_id}/agent/callerId')
        super().put(url, json=body)

    def read_barge_in_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> BargeInInfo:
        """
        Read Barge In Settings for a Virtual Line

        Retrieve a virtual line's barge in settings.

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        Retrieving the barge in settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`BargeInInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/bargeIn')
        data = super().get(url, params=params)
        r = BargeInInfo.model_validate(data)
        return r

    def configure_barge_in_settings_for_a_virtual_line(self, virtual_line_id: str, enabled: bool = None,
                                                       tone_enabled: bool = None, org_id: str = None):
        """
        Configure Barge In Settings for a Virtual Line

        Configure a virtual line's barge in settings.

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        Updating the barge in settings for a virtual line requires a full or user administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param enabled: Set to enable or disable the Barge In feature.
        :type enabled: bool
        :param tone_enabled: Set to enable or disable a stutter dial tone being played when a virtual line is barging
            in on the active call.
        :type tone_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep(f'{virtual_line_id}/bargeIn')
        super().put(url, params=params, json=body)

    def read_call_bridge_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> bool:
        """
        Read Call Bridge Settings for a Virtual Line

        Retrieve a virtual line's call bridge settings.

        Retrieving the call bridge settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/callBridge')
        data = super().get(url, params=params)
        r = data['warningToneEnabled']
        return r

    def configure_call_bridge_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                          warning_tone_enabled: bool = None, org_id: str = None):
        """
        Configure Call Bridge Settings for a Virtual Line

        Configure a virtual line's call bridge settings.

        Updating the call bridge settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param warning_tone_enabled: Set to enable or disable a stutter dial tone being played to all the participants
            when a virtual line is bridged on the active shared line call.
        :type warning_tone_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if warning_tone_enabled is not None:
            body['warningToneEnabled'] = warning_tone_enabled
        url = self.ep(f'{virtual_line_id}/callBridge')
        super().put(url, params=params, json=body)

    def read_call_forwarding_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                         org_id: str = None) -> CallForwardingInfo:
        """
        Read Call Forwarding Settings for a Virtual Line

        Retrieve a virtual line's Call Forwarding settings.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the virtual
        line is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        Retrieving the call forwarding settings for a virtual line requires a full, user, or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`CallForwardingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardingInfo.model_validate(data)
        return r

    def configure_call_forwarding_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                              call_forwarding: CallForwardingPutCallForwarding = None,
                                                              business_continuity: CallForwardingInfoCallForwardingBusy = None,
                                                              org_id: str = None):
        """
        Configure Call Forwarding Settings for a Virtual Line

        Configure a virtual line's Call Forwarding settings.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the virtual
        line is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        Updating the call forwarding settings for a virtual line requires a full or user administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwardingPutCallForwarding
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingInfoCallForwardingBusy
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        if business_continuity is not None:
            body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{virtual_line_id}/callForwarding')
        super().put(url, params=params, json=body)

    def get_virtual_line_call_forward_available_phone_numbers(self, virtual_line_id: str,
                                                              phone_number: list[str] = None, owner_name: str = None,
                                                              extension: str = None, org_id: str = None,
                                                              **params) -> Generator[VirtualLineCallForwardAvailableNumberObject, None, None]:
        """
        Get Virtual Line Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a virtual line's call forward
        number.
        These numbers are associated with the location of the virtual line specified in the request URL, can be active
        or inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
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
        :return: Generator yielding :class:`VirtualLineCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{virtual_line_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=VirtualLineCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_virtual_line_call_intercept_available_phone_numbers(self, virtual_line_id: str,
                                                                phone_number: list[str] = None,
                                                                owner_name: str = None, extension: str = None,
                                                                org_id: str = None,
                                                                **params) -> Generator[VirtualLineCallForwardAvailableNumberObject, None, None]:
        """
        Get Virtual Line Call Intercept Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a virtual line's call intercept
        number.
        These numbers are associated with the location of the virtual line specified in the request URL, can be active
        or inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
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
        :return: Generator yielding :class:`VirtualLineCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{virtual_line_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=VirtualLineCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def read_call_recording_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                        org_id: str = None) -> CallRecordingInfo:
        """
        Read Call Recording Settings for a Virtual Line

        Retrieve Virtual Line's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_read` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def configure_call_recording_settings_for_a_virtual_line(self, virtual_line_id: str, enabled: bool = None,
                                                             record: CallRecordingInfoRecord = None,
                                                             record_voicemail_enabled: bool = None,
                                                             notification: CallRecordingPutNotification = None,
                                                             repeat: CallRecordingInfoRepeat = None,
                                                             start_stop_announcement: CallRecordingInfoStartStopAnnouncement = None,
                                                             org_id: str = None):
        """
        Configure Call Recording Settings for a Virtual Line

        Configure virtual line's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param enabled: `true` if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: CallRecordingInfoRecord
        :param record_voicemail_enabled: When `true`, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: CallRecordingPutNotification
        :param repeat: Beep sound plays periodically.
        :type repeat: CallRecordingInfoRepeat
        :param start_stop_announcement: Call Recording starts and stops announcement settings.
        :type start_stop_announcement: CallRecordingInfoStartStopAnnouncement
        :param org_id: ID of the organization in which the virtual profile resides. Only admin users of another
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
        if record is not None:
            body['record'] = enum_str(record)
        if record_voicemail_enabled is not None:
            body['recordVoicemailEnabled'] = record_voicemail_enabled
        if notification is not None:
            body['notification'] = notification.model_dump(mode='json', by_alias=True, exclude_none=True)
        if repeat is not None:
            body['repeat'] = repeat.model_dump(mode='json', by_alias=True, exclude_none=True)
        if start_stop_announcement is not None:
            body['startStopAnnouncement'] = start_stop_announcement.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{virtual_line_id}/callRecording')
        super().put(url, params=params, json=body)

    def read_call_waiting_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> bool:
        """
        Read Call Waiting Settings for a Virtual Line

        Retrieve a virtual line's Call Waiting settings.

        With this feature, a virtual line can place an active call on hold and answer an incoming call.  When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        Retrieving the call waiting settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/callWaiting')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def configure_call_waiting_settings_for_a_virtual_line(self, virtual_line_id: str, enabled: bool,
                                                           org_id: str = None):
        """
        Configure Call Waiting Settings for a Virtual Line

        Configure a virtual line's Call Waiting settings.

        With this feature, a virtual line can place an active call on hold and answer an incoming call.  When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        Updating the call waiting settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param enabled: `true` if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/callWaiting')
        super().put(url, params=params, json=body)

    def read_caller_id_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> CallerIdInfo:
        """
        Read Caller ID Settings for a Virtual Line

        Retrieve a virtual line's Caller ID settings.

        Caller ID settings control how a virtual line's information is displayed when making outgoing calls.

        Retrieving the caller ID settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, `dialByFirstName`, and
        `dialByLastName` are not supported in Webex for Government (FedRAMP). Instead, administrators must use the
        `firstName` and `lastName` fields to configure and view both caller ID and dial-by-name
        settings.</Callout></div>

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter, as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`CallerIdInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/callerId')
        data = super().get(url, params=params)
        r = CallerIdInfo.model_validate(data)
        return r

    def configure_caller_id_settings_for_a_virtual_line(self, virtual_line_id: str, selected: CallerIdInfoSelected,
                                                        custom_number: str = None, first_name: str = None,
                                                        last_name: str = None,
                                                        block_in_forward_calls_enabled: bool = None,
                                                        external_caller_id_name_policy: ListVirtualLineObjectExternalCallerIdNamePolicy = None,
                                                        custom_external_caller_id_name: str = None,
                                                        additional_external_caller_id_direct_line_enabled: bool = None,
                                                        additional_external_caller_id_location_number_enabled: bool = None,
                                                        additional_external_caller_id_custom_number: str = None,
                                                        direct_line_caller_id_name: DirectLineCallerIdNameObject = None,
                                                        dial_by_first_name: str = None, dial_by_last_name: str = None,
                                                        org_id: str = None):
        """
        Configure Caller ID Settings for a Virtual Line

        Configure a virtual line's Caller ID settings.

        Caller ID settings control how a virtual line's information is displayed when making outgoing calls.

        Updating the caller ID settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, `dialByFirstName`, and
        `dialByLastName` are not supported in Webex for Government (FedRAMP). Instead, administrators must use the
        `firstName` and `lastName` fields to configure and view both caller ID and dial-by-name
        settings.</Callout></div>

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CallerIdInfoSelected
        :param custom_number: Custom number which will be shown if CUSTOM is selected. This value must be a number from
            the virtual line's location or from another location with the same country, PSTN provider, and zone (only
            applicable for India locations) as the virtual line's location.
        :type custom_number: str
        :param first_name: Virtual line's Caller ID first name. The characters `%`,  `+`, ``, `"` and Unicode
            characters are not allowed. This field has been deprecated. Please use `directLineCallerIdName` and
            `dialByFirstName` instead.
        :type first_name: str
        :param last_name: Virtual line's Caller ID last name. The characters `%`,  `+`, ``, `"` and Unicode characters
            are not allowed. This field has been deprecated. Please use `directLineCallerIdName` and `dialByLastName`
            instead.
        :type last_name: str
        :param block_in_forward_calls_enabled: Block this virtual line's identity when receiving a call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is DIRECT_LINE.
        :type external_caller_id_name_policy: ListVirtualLineObjectExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom external caller ID name which will be shown if external caller ID
            name policy is `OTHER`.
        :type custom_external_caller_id_name: str
        :param additional_external_caller_id_direct_line_enabled: Set the virtual line's direct line number as
            additional external caller ID.
        :type additional_external_caller_id_direct_line_enabled: bool
        :param additional_external_caller_id_location_number_enabled: Set the Location main number as additional
            external caller ID for the virtual line.
        :type additional_external_caller_id_location_number_enabled: bool
        :param additional_external_caller_id_custom_number: To set a custom number as additional external caller ID for
            the virtual line. This value must be a number from the virtual line's location or from another location
            with the same country, PSTN provider, and zone (only applicable for India locations) as the virtual line's
            location.
        :type additional_external_caller_id_custom_number: str
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this virtual
            line.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_first_name: Sets or clears the first name to be used for dial-by-name functions. To clear the
            `dialByFirstName`, the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"`
            and Unicode characters are not allowed.
        :type dial_by_first_name: str
        :param dial_by_last_name: Sets or clears the last name to be used for dial-by-name functions. To clear the
            `dialByLastName`, the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_last_name: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter, as the default is the same organization as the
            token used to access the API.
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
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if block_in_forward_calls_enabled is not None:
            body['blockInForwardCallsEnabled'] = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body['externalCallerIdNamePolicy'] = enum_str(external_caller_id_name_policy)
        if custom_external_caller_id_name is not None:
            body['customExternalCallerIdName'] = custom_external_caller_id_name
        if additional_external_caller_id_direct_line_enabled is not None:
            body['additionalExternalCallerIdDirectLineEnabled'] = additional_external_caller_id_direct_line_enabled
        if additional_external_caller_id_location_number_enabled is not None:
            body['additionalExternalCallerIdLocationNumberEnabled'] = additional_external_caller_id_location_number_enabled
        if additional_external_caller_id_custom_number is not None:
            body['additionalExternalCallerIdCustomNumber'] = additional_external_caller_id_custom_number
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_first_name is not None:
            body['dialByFirstName'] = dial_by_first_name
        if dial_by_last_name is not None:
            body['dialByLastName'] = dial_by_last_name
        url = self.ep(f'{virtual_line_id}/callerId')
        super().put(url, params=params, json=body)

    def get_list_of_dect_networks_handsets_for_a_virtual_line(self, virtual_line_id: str,
                                                              org_id: str = None) -> list[DectNetwork]:
        """
        Get List of DECT Networks Handsets for a Virtual Line

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Retrieve DECT Network details assigned for a virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving the assigned device detials for a virtual line requires a full or user or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: list[DectNetwork]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DectNetwork]).validate_python(data['dectNetworks'])
        return r

    def get_list_of_devices_assigned_for_a_virtual_line(self, virtual_line_id: str,
                                                        org_id: str = None) -> GetVirtualLineDevicesObject:
        """
        Get List of Devices assigned for a Virtual Line

        Retrieve Device details assigned for a virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving the assigned device detials for a virtual line requires a full or user or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: :class:`GetVirtualLineDevicesObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/devices')
        data = super().get(url, params=params)
        r = GetVirtualLineDevicesObject.model_validate(data)
        return r

    def update_directory_search_for_a_virtual_line(self, virtual_line_id: str, enabled: bool, org_id: str = None):
        """
        Update Directory search for a Virtual Line

        Update the directory search for a designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating Directory search for a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write` and `identity:contacts_rw`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param enabled: Whether or not the directory search for a virtual line is enabled.
        :type enabled: bool
        :param org_id: Update virtual line settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{virtual_line_id}/directorySearch')
        super().put(url, params=params, json=body)

    def get_virtual_line_do_not_disturb(self, virtual_line_id: str, org_id: str = None) -> VirtualLineDoNotDisturbGet:
        """
        Retrieve DoNotDisturb Settings for a Virtual Line.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, read-only or location administrator auth token with a scope of
        `telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization within which the virtual line resides.
        :type org_id: str
        :rtype: :class:`VirtualLineDoNotDisturbGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/doNotDisturb')
        data = super().get(url, params=params)
        r = VirtualLineDoNotDisturbGet.model_validate(data)
        return r

    def put_virtual_line_do_not_disturb(self, virtual_line_id: str, enabled: bool = None,
                                        ring_splash_enabled: bool = None, org_id: str = None):
        """
        Modify DoNotDisturb Settings for a Virtual Line.

        Silence incoming calls with the Do Not Disturb feature.
        When enabled, callers hear the busy signal.

        This API requires a full, user or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param enabled: `true` if the DoNotDisturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: When `true`, enables ring reminder when you receive an incoming call while on Do
            Not Disturb.
        :type ring_splash_enabled: bool
        :param org_id: ID of the organization within which the virtual line resides.
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
        url = self.ep(f'{virtual_line_id}/doNotDisturb')
        super().put(url, params=params, json=body)

    def get_virtual_line_ecbn_available_phone_numbers(self, virtual_line_id: str, phone_number: list[str] = None,
                                                      owner_name: str = None, org_id: str = None,
                                                      **params) -> Generator[VirtualLineECBNAvailableNumberObject, None, None]:
        """
        Get Virtual Line ECBN Available Phone Numbers

        List standard numbers that can be assigned as a virtual line's call forward number.
        These numbers are associated with the location of the virtual line specified in the request URL, can be active
        or inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`VirtualLineECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'{virtual_line_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=VirtualLineECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_virtual_line_fax_message_available_phone_numbers(self, virtual_line_id: str,
                                                             phone_number: list[str] = None, org_id: str = None,
                                                             **params) -> Generator[VirtualLineFaxMessageAvailableNumberObject, None, None]:
        """
        Get Virtual Line Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a virtual line's FAX message number.
        These numbers are associated with the location of the virtual line specified in the request URL, can be active
        or inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`VirtualLineFaxMessageAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{virtual_line_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=VirtualLineFaxMessageAvailableNumberObject, item_key='phoneNumbers', params=params)

    def read_incoming_permission_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                             org_id: str = None) -> IncomingPermissionSetting:
        """
        Read Incoming Permission Settings for a Virtual Line

        Retrieve a virtual line's Incoming Permission settings.

        You can change the incoming calling permissions for a virtual line if you want them to be different from your
        organization's default.

        Retrieving the incoming permission settings for a virtual line requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`IncomingPermissionSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/incomingPermission')
        data = super().get(url, params=params)
        r = IncomingPermissionSetting.model_validate(data)
        return r

    def configure_incoming_permission_settings_for_a_virtual_line(self, virtual_line_id: str, use_custom_enabled: bool,
                                                                  external_transfer: IncomingPermissionSettingExternalTransfer,
                                                                  internal_calls_enabled: bool,
                                                                  collect_calls_enabled: bool, org_id: str = None):
        """
        Configure Incoming Permission Settings for a Virtual Line

        Configure a virtual line's Incoming Permission settings.

        You can change the incoming calling permissions for a virtual line if you want them to be different from your
        organization's default.

        Updating the incoming permission settings for a virtual line requires a full or user administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param use_custom_enabled: When true, indicates that this virtual line uses the specified calling permissions
            for receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: IncomingPermissionSettingExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['useCustomEnabled'] = use_custom_enabled
        body['externalTransfer'] = enum_str(external_transfer)
        body['internalCallsEnabled'] = internal_calls_enabled
        body['collectCallsEnabled'] = collect_calls_enabled
        url = self.ep(f'{virtual_line_id}/incomingPermission')
        super().put(url, params=params, json=body)

    def read_call_intercept_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                        org_id: str = None) -> CallInterceptInfo:
        """
        Read Call Intercept Settings for a Virtual Line

        Retrieves Virtual Line's Call Intercept settings.

        The intercept feature gracefully takes a virtual line's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified virtual line are intercepted. Also depending on the service
        configuration, outgoing calls are intercepted or rerouted to another location.

        Retrieving the intercept settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallInterceptInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/intercept')
        data = super().get(url, params=params)
        r = CallInterceptInfo.model_validate(data)
        return r

    def configure_call_intercept_settings_for_a_virtual_line(self, virtual_line_id: str, enabled: bool = None,
                                                             incoming: CallInterceptPutIncoming = None,
                                                             outgoing: CallInterceptInfoOutgoing = None,
                                                             org_id: str = None):
        """
        Configure Call Intercept Settings for a Virtual Line

        Configures a virtual line's Call Intercept settings.

        The intercept feature gracefully takes a virtual line's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified virtual line are intercepted. Also depending on the service
        configuration, outgoing calls are intercepted or rerouted to another location.

        Updating the intercept settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param enabled: `true` if the intercept feature is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: CallInterceptPutIncoming
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: CallInterceptInfoOutgoing
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
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming.model_dump(mode='json', by_alias=True, exclude_none=True)
        if outgoing is not None:
            body['outgoing'] = outgoing.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{virtual_line_id}/intercept')
        super().put(url, params=params, json=body)

    def configure_call_intercept_greeting_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Configure Call Intercept Greeting for a Virtual Line

        Configure a virtual line's Call Intercept Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        Uploading the intercept greeting announcement for a virtual line requires a full or user administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/intercept/actions/announcementUpload/invoke')
        super().post(url, params=params)

    def retrieve_music_on_hold_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                           org_id: str = None) -> GetMusicOnHoldObject:
        """
        Retrieve Music On Hold Settings for a Virtual Line

        Retrieve the virtual line's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving the music on hold settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

    def configure_music_on_hold_settings_for_a_virtual_line(self, virtual_line_id: str, moh_enabled: bool = None,
                                                            greeting: CallInterceptInfoIncomingAnnouncementsGreeting = None,
                                                            audio_announcement_file: AudioAnnouncementFileGetObject = None,
                                                            org_id: str = None):
        """
        Configure Music On Hold Settings for a Virtual Line

        Configure a virtual line's music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold settings for a virtual line, music on hold setting must be enabled for this
        location.

        Updating the music on hold settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param moh_enabled: Music on hold is enabled or disabled for the virtual line.
        :type moh_enabled: bool
        :param greeting: Greeting type for the virtual line.
        :type greeting: CallInterceptInfoIncomingAnnouncementsGreeting
        :param audio_announcement_file: Announcement Audio File details when greeting is set to CUSTOM.
        :type audio_announcement_file: AudioAnnouncementFileGetObject
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/musicOnHold')
        super().put(url, params=params, json=body)

    def get_phone_number_assigned_for_a_virtual_line(self, virtual_line_id: str,
                                                     org_id: str = None) -> GetVirtualLineNumberObjectPhoneNumber:
        """
        Get Phone Number assigned for a Virtual Line

        Get details on the assigned phone number and extension for the virtual line.

        Retrieving virtual line phone number details requires a full or user or read-only administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: GetVirtualLineNumberObjectPhoneNumber
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/number')
        data = super().get(url, params=params)
        r = GetVirtualLineNumberObjectPhoneNumber.model_validate(data['phoneNumber'])
        return r

    def retrieve_a_virtual_line_s_outgoing_calling_permissions_settings(self, virtual_line_id: str,
                                                                        org_id: str = None) -> OutgoingCallingPermissionsSettingGet:
        """
        Retrieve a virtual line's Outgoing Calling Permissions settings.

        Outgoing calling permissions regulate behavior for calls placed to various destinations and default to the
        local level settings. You can change the outgoing calling permissions for a virtual line if you want them to
        be different from your organization's default.

        Retrieving the outgoing permission settings for a virtual line requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`OutgoingCallingPermissionsSettingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
        data = super().get(url, params=params)
        r = OutgoingCallingPermissionsSettingGet.model_validate(data)
        return r

    def modify_a_virtual_line_s_outgoing_calling_permissions_settings(self, virtual_line_id: str,
                                                                      calling_permissions: list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem],
                                                                      use_custom_enabled: bool = None,
                                                                      use_custom_permissions: bool = None,
                                                                      org_id: str = None):
        """
        Modify a virtual line's Outgoing Calling Permissions settings.

        Outgoing calling permissions regulate behavior for calls placed to various destinations and default to the
        local level settings. You can change the outgoing calling permissions for a virtual line if you want them to
        be different from your organization's default.

        Updating the outgoing permission settings for a virtual line requires a full or user administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem]
        :param use_custom_enabled: When true, indicates that this user uses the shared control that applies to all
            outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When true, indicates that this user uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
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
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if use_custom_permissions is not None:
            body['useCustomPermissions'] = use_custom_permissions
        body['callingPermissions'] = TypeAdapter(list[OutgoingCallingPermissionsSettingPutCallingPermissionsItem]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
        super().put(url, params=params, json=body)

    def delete_access_codes_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Delete Access Codes for a Virtual Line

        Deletes all access codes for the virtual line.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def retrieve_access_codes_for_a_virtual_line(self, virtual_line_id: str,
                                                 org_id: str = None) -> UserPlaceAuthorizationCodeListGet:
        """
        Retrieve Access Codes for a Virtual Line

        Retrieve the virtual line's access codes.

        Access codes are used to bypass permissions.

        This API requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserPlaceAuthorizationCodeListGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = UserPlaceAuthorizationCodeListGet.model_validate(data)
        return r

    def create_access_codes_for_a_virtual_line(self, virtual_line_id: str, code: str, description: str,
                                               org_id: str = None):
        """
        Create Access Codes for a Virtual Line

        Create a new access codes for the virtual line.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
        :type description: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def modify_access_codes_for_a_virtual_line(self, virtual_line_id: str, use_custom_access_codes: bool = None,
                                               delete_codes: list[str] = None, org_id: str = None):
        """
        Modify Access Codes for a Virtual Line

        Modify a virtual line's access codes.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_access_codes: When `true`, use custom settings for the access codes category of outbound
            permissions.
        :type use_custom_access_codes: bool
        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def retrieve_transfer_numbers_for_a_virtual_line(self, virtual_line_id: str,
                                                     org_id: str = None) -> TransferNumberGet:
        """
        Retrieve Transfer Numbers for a Virtual Line

        Retrieve the virtual line's transfer numbers.

        When calling a specific call type, this virtual line will be automatically transferred to another number. The
        virtual line assigned to the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`TransferNumberGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = TransferNumberGet.model_validate(data)
        return r

    def modify_transfer_numbers_for_a_virtual_line(self, virtual_line_id: str, use_custom_transfer_numbers: bool,
                                                   auto_transfer_number1: str = None,
                                                   auto_transfer_number2: str = None,
                                                   auto_transfer_number3: str = None, org_id: str = None):
        """
        Modify Transfer Numbers for a Virtual Line

        Modify a virtual line's transfer numbers.

        When calling a specific call type, this virtual line will be automatically transferred to another number. The
        virtual line assigned the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_transfer_numbers: When `true`, use custom settings for the transfer numbers category of
            outbound permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber1` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_1`.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber2` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_2`.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber3` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_3`.
        :type auto_transfer_number3: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def delete_all_digit_patterns_for_a_virtual_profile(self, virtual_line_id: str, org_id: str = None):
        """
        Delete all digit patterns for a virtual profile.

        Digit patterns are used to bypass permissions.

        Deleting the digit patterns requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

    def retrieve_digit_patterns_for_a_virtual_profile(self, virtual_line_id: str,
                                                      org_id: str = None) -> UserOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve Digit Patterns for a Virtual Profile

        Get list of digit patterns for the virtual profile.

        Digit patterns are used to bypass permissions.

        Retrieving this list requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = UserOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def create_digit_pattern_for_a_virtual_profile(self, virtual_line_id: str, name: str, pattern: str,
                                                   action: OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction,
                                                   transfer_enabled: bool, org_id: str = None) -> str:
        """
        Create Digit Pattern for a Virtual Profile

        Create a new digit pattern for a virtual profile.

        Digit patterns are used to bypass permissions.

        Creating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_the_digit_pattern_category_control_settings_for_a_virtual_profile(self, virtual_line_id: str,
                                                                                 use_custom_digit_patterns: bool = None,
                                                                                 org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for a Virtual Profile

        Modifies whether this virtual profile uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or user or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def delete_a_digit_pattern_for_a_virtual_profile(self, virtual_line_id: str, digit_pattern_id: str,
                                                     org_id: str = None):
        """
        Delete a digit pattern for a virtual profile.

        Digit patterns are used to bypass permissions.

        Deleting the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def retrieve_specified_digit_pattern_details_for_a_virtual_profile(self, virtual_line_id: str,
                                                                       digit_pattern_id: str,
                                                                       org_id: str = None) -> UserDigitPatternObject:
        """
        Retrieve Specified Digit Pattern Details for a Virtual Profile

        Get the specified digit pattern for the virtual profile​.

        Digit patterns are used to bypass permissions.

        Retrieving the digit pattern details requires a full, user or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = UserDigitPatternObject.model_validate(data)
        return r

    def modify_a_digit_pattern_for_a_virtual_profile(self, virtual_line_id: str, digit_pattern_id: str,
                                                     name: str = None, pattern: str = None,
                                                     action: OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction = None,
                                                     transfer_enabled: bool = None, org_id: str = None):
        """
        Modify a Digit Pattern for a Virtual Profile

        Modify a digit patterns for a virtual profile.

        Digit patterns are used to bypass permissions.

        Updating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: OutgoingCallingPermissionsSettingGetCallingPermissionsItemAction
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def get_a_virtual_line_s_privacy_settings(self, virtual_line_id: str, org_id: str = None) -> PrivacyGet:
        """
        Get a Virtual Line's Privacy Settings

        Get a virtual line's privacy settings for the specified virtual line ID.

        The privacy feature enables the virtual line's line to be monitored by others and determine if they can be
        reached by Auto Attendant services.

        Retrieving the privacy settings for a virtual line requires a full, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def configure_a_virtual_line_s_privacy_settings(self, virtual_line_id: str,
                                                    aa_extension_dialing_enabled: bool = None,
                                                    aa_naming_dialing_enabled: bool = None,
                                                    enable_phone_status_directory_privacy: bool = None,
                                                    enable_phone_status_pickup_barge_in_privacy: bool = None,
                                                    monitoring_agents: list[str] = None, org_id: str = None):
        """
        Configure a Virtual Line's Privacy Settings

        Configure a virtual line's privacy settings for the specified virtual line ID.

        The privacy feature enables the virtual line's line to be monitored by others and determine if they can be
        reached by Auto Attendant services.

        Updating the privacy settings for a virtual line requires a full or user administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
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
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/privacy')
        super().put(url, params=params, json=body)

    def read_push_to_talk_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                      org_id: str = None) -> PushToTalkInfo:
        """
        Read Push-to-Talk Settings for a Virtual Line

        Retrieve a virtual line's Push-to-Talk settings.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        Retrieving the Push-to-Talk settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/pushToTalk')
        data = super().get(url, params=params)
        r = PushToTalkInfo.model_validate(data)
        return r

    def configure_push_to_talk_settings_for_a_virtual_line(self, virtual_line_id: str, allow_auto_answer: bool = None,
                                                           connection_type: PushToTalkConnectionType = None,
                                                           access_type: PushToTalkAccessType = None,
                                                           members: list[str] = None, org_id: str = None):
        """
        Configure Push-to-Talk Settings for a Virtual Line

        Configure a virtual line's Push-to-Talk settings.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        Updating the Push-to-Talk settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param allow_auto_answer: `true` if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
        :type members: list[str]
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/pushToTalk')
        super().put(url, params=params, json=body)

    def read_voicemail_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> VoicemailInfo:
        """
        Read Voicemail Settings for a Virtual Line

        Retrieve a virtual line's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        Retrieving the voicemail settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`VoicemailInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/voicemail')
        data = super().get(url, params=params)
        r = VoicemailInfo.model_validate(data)
        return r

    def configure_voicemail_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                        notifications: CallInterceptInfoIncomingAnnouncementsNewNumber,
                                                        transfer_to_number: CallInterceptInfoIncomingAnnouncementsNewNumber,
                                                        announcement_language_code: str, enabled: bool = None,
                                                        send_all_calls: DirectorySearchObject = None,
                                                        send_busy_calls: VoicemailPutSendBusyCalls = None,
                                                        send_unanswered_calls: VoicemailPutSendUnansweredCalls = None,
                                                        email_copy_of_message: VoicemailInfoEmailCopyOfMessage = None,
                                                        message_storage: VoicemailInfoMessageStorage = None,
                                                        fax_message: VoicemailInfoFaxMessage = None,
                                                        org_id: str = None):
        """
        Configure Voicemail Settings for a Virtual Line

        Configure a virtual line's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        Updating the voicemail settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: CallInterceptInfoIncomingAnnouncementsNewNumber
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: CallInterceptInfoIncomingAnnouncementsNewNumber
        :param announcement_language_code: Language code.
        :type announcement_language_code: str
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: DirectorySearchObject
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: VoicemailPutSendBusyCalls
        :type send_unanswered_calls: VoicemailPutSendUnansweredCalls
        :param email_copy_of_message: Settings for sending a copy of the new voicemail message audio via email.
        :type email_copy_of_message: VoicemailInfoEmailCopyOfMessage
        :type message_storage: VoicemailInfoMessageStorage
        :type fax_message: VoicemailInfoFaxMessage
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        body['announcementLanguageCode'] = announcement_language_code
        url = self.ep(f'{virtual_line_id}/voicemail')
        super().put(url, params=params, json=body)

    def reset_voicemail_pin_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Reset Voicemail PIN for a Virtual Line

        Reset a voicemail PIN for a virtual line.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail.  A voicemail PIN is used to retrieve your voicemail messages.

        Updating the voicemail pin for a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: This API is expected to have an empty request body and Content-Type header should be set to
        `application/json`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/voicemail/actions/resetPin/invoke')
        super().post(url, params=params)

    def configure_busy_voicemail_greeting_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Virtual Line

        Configure a virtual line's Busy Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`, encoded
        audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        Uploading the voicemail busy greeting announcement for a virtual line requires a full or user administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url, params=params)

    def configure_no_answer_voicemail_greeting_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Virtual Line

        Configure a virtual line's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, `.wav`,
        encoded audio file.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        Uploading the voicemail no answer greeting announcement for a virtual line requires a full or user
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **WARNING:** This API is not callable using the developer portal web interface due to the lack of support for
        multipart POST. This API can be utilized using other tools that support multipart POST, such as Postman.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url, params=params)

    def modify_a_virtual_line_s_voicemail_passcode(self, virtual_line_id: str, passcode: str, org_id: str = None):
        """
        Modify a virtual line's voicemail passcode.

        Modifying a virtual line's voicemail passcode requires a full administrator, user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Modify voicemail passcode for this virtual line.
        :type virtual_line_id: str
        :param passcode: Voicemail access passcode. The minimum length of the passcode is 6 and the maximum length is
            30.
        :type passcode: str
        :param org_id: Modify voicemail passcode for a virtual line in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['passcode'] = passcode
        url = self.ep(f'{virtual_line_id}/voicemail/passcode')
        super().put(url, params=params, json=body)
