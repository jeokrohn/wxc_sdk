from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BetaVirtualLineCallSettingsApi', 'CallForwardingInfo', 'CallForwardingInfoCallForwarding',
            'CallForwardingInfoCallForwardingAlways', 'CallForwardingInfoCallForwardingBusy',
            'CallForwardingInfoCallForwardingNoAnswer', 'CallForwardingPutCallForwarding',
            'CallForwardingPutCallForwardingNoAnswer', 'CallInterceptInfo', 'CallInterceptInfoIncoming',
            'CallInterceptInfoIncomingAnnouncements', 'CallInterceptInfoIncomingAnnouncementsGreeting',
            'CallInterceptInfoIncomingAnnouncementsNewNumber', 'CallInterceptInfoIncomingType',
            'CallInterceptInfoOutgoing', 'CallInterceptInfoOutgoingType', 'CallInterceptPutIncoming',
            'CallInterceptPutIncomingAnnouncements', 'CallerIdInfo', 'CallerIdInfoExternalCallerIdNamePolicy',
            'CallerIdSelectedType', 'DectNetwork', 'DeviceActivationStates', 'DeviceObject', 'DeviceObjectLocation',
            'DeviceOwner', 'DevicesObject', 'GetVirtualLineDevicesObject', 'GetVirtualLineNumberObjectPhoneNumber',
            'GetVirtualLineObject', 'GetVirtualLineObjectLocation', 'GetVirtualLineObjectLocationAddress',
            'GetVirtualLineObjectNumber', 'IncomingPermissionSetting', 'IncomingPermissionSettingExternalTransfer',
            'LineType', 'MemberType', 'OutgoingCallingPermissionsSetting',
            'OutgoingCallingPermissionsSettingCallingPermissions',
            'OutgoingCallingPermissionsSettingCallingPermissionsAction',
            'OutgoingCallingPermissionsSettingCallingPermissionsCallType']


class GetVirtualLineObjectNumber(ApiModel):
    #: Phone number of a virtual line.  Either `external` or `extension` is mandatory.
    #: example: +15558675309
    external: Optional[str] = None
    #: Extension of a virtual line.  Either `external` or `extension` is mandatory.
    #: example: 5309
    extension: Optional[str] = None
    #: Number is Primary or Alternative Number.
    #: example: True
    primary: Optional[bool] = None


class GetVirtualLineObjectLocationAddress(ApiModel):
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


class GetVirtualLineObjectLocation(ApiModel):
    #: ID of location associated with virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    #: example: Main Location Test
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
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2J6QjJlRGd6Ym1GeU5rQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Enumeration that indicates if the member is of type `PEOPLE` or `PLACE`.
    type: Optional[MemberType] = None
    #: First name of device owner.
    #: example: Christian
    first_name: Optional[str] = None
    #: Last name of device owner.
    #: example: Smith
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
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RFVklDRS9hNmYwYjhkMi01ZjdkLTQzZDItODAyNi0zM2JkNDg3NjYzMTg=
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    #: example: DMS Cisco 6871
    model: Optional[str] = None
    #: MAC address of device.
    #: example: 123451234502
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
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfTElORS85Y2JmYjYxZi00ZGM0LTQ1NWItYmMzYS00NmI4YmY5YjQzNzk
    id: Optional[str] = None
    #: First name defined for a virtual line. Minimum length is 1. Maximum length is 30.
    #: example: Bob
    first_name: Optional[str] = None
    #: Last name defined for a virtual line. Minimum length is 1. Maximum length is 30.
    #: example: Smith
    last_name: Optional[str] = None
    #: Display name defined for a virtual line.
    #: example: Bob Smith
    display_name: Optional[str] = None
    #: Flag to indicate a directory search.
    #: example: True
    directory_search_enabled: Optional[bool] = None
    #: Virtual Line's announcement language.
    #: example: 'French'
    announcement_language: Optional[str] = None
    #: Time zone defined for the virtual line.
    #: example: Africa/Algiers
    time_zone: Optional[str] = None
    #: Calling details of virtual line.
    number: Optional[GetVirtualLineObjectNumber] = None
    #: List of devices assigned to a virtual line.
    devices: Optional[list[DevicesObject]] = None
    #: Location details of virtual line.
    location: Optional[GetVirtualLineObjectLocation] = None


class GetVirtualLineNumberObjectPhoneNumber(ApiModel):
    #: Phone number that is assigned to a virtual line.
    #: example: +15558675309
    direct_number: Optional[str] = None
    #: Extension that is assigned to a virtual line.
    #: example: 5309
    extension: Optional[str] = None
    #: If `true` marks the phone number as primary.
    #: example: True
    primary: Optional[bool] = None


class DeviceObjectLocation(ApiModel):
    #: ID of location associated with virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    #: example: Main Location Test
    name: Optional[str] = None


class DeviceObject(ApiModel):
    #: Unique identifier for a device.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RFVklDRS9hNmYwYjhkMi01ZjdkLTQzZDItODAyNi0zM2JkNDg3NjYzMTg=
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    #: example: DMS Cisco 6871
    model: Optional[str] = None
    #: MAC address of device.
    #: example: 123451234502
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
    location: Optional[DeviceObjectLocation] = None


class GetVirtualLineDevicesObject(ApiModel):
    #: List of devices assigned to a virtual line.
    devices: Optional[list[DeviceObject]] = None
    #: Indicates to which line a device can be assigned.
    available_endpoint_type: Optional[LineType] = None
    #: Maximum number of devices a virtual line can be assigned to.
    #: example: 35
    max_device_count: Optional[int] = None


class DectNetwork(ApiModel):
    #: Unique identifier for a dect network.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RFVklDRS9hNmYwYjhkMi01ZjdkLTQzZDItODAyNi0zM2JkNDg3NjYzMTg=
    id: Optional[str] = None
    #: Identifier for device DECT network.
    #: example: Dect Network1
    name: Optional[str] = None
    #: Indicates whether the virtual profile is the primary line.
    primary_enabled: Optional[bool] = None
    #: Number of dect handsets assigned to the virtual profile.
    #: example: 1
    number_of_handsets_assigned: Optional[int] = None
    #: Location details of virtual line.
    location: Optional[DeviceObjectLocation] = None


class CallerIdInfoExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the `customExternalCallerIdName` field.
    other = 'OTHER'


class CallerIdSelectedType(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the mobile number for this virtual line.
    mobile_number = 'MOBILE_NUMBER'
    #: Outgoing caller ID will show the value from the `customNumber` field. The cross location number is allowed if
    #: the locations are in the same country, use the same PSTN provider and the same zone. The cross location number
    #: is not allowed for India. This field is read-only and cannot be modified.
    custom = 'CUSTOM'
    none_ = 'none'


class CallerIdInfo(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CallerIdSelectedType]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    #: example: DIRECT_LINE
    selected: Optional[CallerIdSelectedType] = None
    #: Direct number which will be shown if `DIRECT_LINE` is selected.
    #: example: 2025551212
    direct_number: Optional[str] = None
    #: Extension number which will be shown if `DIRECT_LINE` is selected.
    #: example: 3456
    extension_number: Optional[str] = None
    #: Location number which will be shown if `LOCATION_NUMBER` is selected.
    #: example: 2025551212
    location_number: Optional[str] = None
    #: Mobile number which will be shown if `MOBILE_NUMBER` is selected.
    #: example: 2025552121
    mobile_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: This value must be an assigned number from the virtual line's location.
    #: example: 2025551212
    custom_number: Optional[str] = None
    #: Person's Caller ID first name. The characters `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Hakim
    first_name: Optional[str] = None
    #: Person's Caller ID last name. The characters `%`,  `+`, ``, `"` and Unicode characters are not allowed.
    #: example: Gonzales
    last_name: Optional[str] = None
    #: `true` if the virtual line's identity is blocked when receiving a transferred or forwarded call.
    #: example: True
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller Id Name policy is used. Default is `DIRECT_LINE`.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[CallerIdInfoExternalCallerIdNamePolicy] = None
    #: Custom External Caller Name, which will be shown if External Caller Id Name is `OTHER`.
    #: example: Hakim custom
    custom_external_caller_id_name: Optional[str] = None
    #: Location's caller ID. This field is read-only and cannot be modified.
    #: example: Hakim location
    location_external_caller_id_name: Optional[str] = None


class CallForwardingInfoCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the virtual line's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an
    #: internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingInfoCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15
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
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3
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
    #: example: ALLOW_ALL_EXTERNAL
    external_transfer: Optional[IncomingPermissionSettingExternalTransfer] = None
    #: Internal calls are allowed to be received.
    #: example: True
    internal_calls_enabled: Optional[bool] = None
    #: Collect calls are allowed to be received.
    #: example: True
    collect_calls_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSettingCallingPermissionsCallType(str, Enum):
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
    #: Controls calls that are National.
    national = 'NATIONAL'


class OutgoingCallingPermissionsSettingCallingPermissionsAction(str, Enum):
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


class OutgoingCallingPermissionsSettingCallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: example: INTERNAL_CALL
    call_type: Optional[OutgoingCallingPermissionsSettingCallingPermissionsCallType] = None
    #: Action on the given `callType`.
    #: example: ALLOW
    action: Optional[OutgoingCallingPermissionsSettingCallingPermissionsAction] = None
    #: Allow the virtual line to transfer or forward a call of the specified call type.
    transfer_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSetting(ApiModel):
    #: When true, indicates that this virtual line uses the specified calling permissions when placing outbound calls.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[OutgoingCallingPermissionsSettingCallingPermissions]] = None


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
    #: example: True
    enabled: Optional[bool] = None
    #: New number caller will hear announced.
    #: example: 2225551212
    destination: Optional[str] = None


class CallInterceptInfoIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Filename of custom greeting; will be an empty string if no custom greeting has been uploaded.
    #: example: incoming.wav
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptInfoIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
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
    #: example: INTERCEPT_ALL
    type: Optional[CallInterceptInfoOutgoingType] = None
    #: If `true`, when the virtual line attempts to make an outbound call, a system default message is played and the
    #: call is made to the destination phone number
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    #: example: 2225551212
    destination: Optional[str] = None


class CallInterceptInfo(ApiModel):
    #: `true` if call intercept is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[CallInterceptInfoIncoming] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[CallInterceptInfoOutgoing] = None


class CallInterceptPutIncomingAnnouncements(ApiModel):
    #: `DEFAULT` indicates that a system default message will be placed when incoming calls are intercepted.
    #: example: DEFAULT
    greeting: Optional[CallInterceptInfoIncomingAnnouncementsGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[CallInterceptInfoIncomingAnnouncementsNewNumber] = None


class CallInterceptPutIncoming(ApiModel):
    #: `INTERCEPT_ALL` indicated incoming calls are intercepted.
    #: example: INTERCEPT_ALL
    type: Optional[CallInterceptInfoIncomingType] = None
    #: If `true`, the destination will be the virtual line's voicemail.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[CallInterceptPutIncomingAnnouncements] = None


class BetaVirtualLineCallSettingsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Beta Virtual Line Call Settings
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Virtual Lines supports reading and writing of Webex Calling Virtual Lines settings for a specific organization.
    
    Viewing these read-only organization settings requires a full, user, or read-only administrator auth token with a
    scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full or user administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

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
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 6. Either `phoneNumber`
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

    def delete_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Delete a Virtual Line

        Delete the designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Deleting a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param first_name: First name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type first_name: str
        :param last_name: Last name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type last_name: str
        :param display_name: Display name defined for a virtual line.
        :type display_name: str
        :param phone_number: Phone number of a virtual line. Minimum length is 1. Maximum length is 23. Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 6. Either `phoneNumber`
            or `extension` is mandatory.
        :type extension: str
        :param announcement_language: Virtual Line's announcement language.
        :type announcement_language: str
        :param caller_id_last_name: Last name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_last_name: str
        :param caller_id_first_name: First name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
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

    def update_directory_search_for_a_virtual_line(self, virtual_line_id: str, enabled: bool, org_id: str = None):
        """
        Update Directory search for a Virtual Line

        Update the directory search for a designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating Directory search for a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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

    def get_list_of_dect_networks_handsets_for_a_virtual_line(self, virtual_line_id: str,
                                                              org_id: str = None) -> list[DectNetwork]:
        """
        Get List of Dect Networks Handsets for a Virtual Line

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
        url = self.ep(f'{virtual_line_id}/dects')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DectNetwork]).validate_python(data['dectNetworks'])
        return r

    def read_caller_id_settings_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None) -> CallerIdInfo:
        """
        Read Caller ID Settings for a Virtual Line

        Retrieve a virtual line's Caller ID settings.

        Caller ID settings control how a virtual line's information is displayed when making outgoing calls.

        Retrieving the caller ID settings for a virtual line requires a full, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

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

    def configure_caller_id_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                        selected: CallerIdSelectedType = None,
                                                        custom_number: str = None, first_name: str = None,
                                                        last_name: str = None,
                                                        block_in_forward_calls_enabled: bool = None,
                                                        external_caller_id_name_policy: CallerIdInfoExternalCallerIdNamePolicy = None,
                                                        custom_external_caller_id_name: str = None,
                                                        org_id: str = None):
        """
        Configure Caller ID Settings for a Virtual Line

        Configure a virtual line's Caller ID settings.

        Caller ID settings control how a virtual line's information is displayed when making outgoing calls.

        Updating the caller ID settings for a virtual line requires a full or user administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the virtual line's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name. The characters `%`,  `+`, ``, `"` and Unicode characters are
            not allowed.
        :type first_name: str
        :param last_name: Person's Caller ID last name. The characters `%`,  `+`, ``, `"` and Unicode characters are
            not allowed.
        :type last_name: str
        :param block_in_forward_calls_enabled: `true` if virtual line's identity has to be blocked when receiving a
            transferred or forwarded call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is DIRECT_LINE.
        :type external_caller_id_name_policy: CallerIdInfoExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Person's custom External Caller ID last name.  Characters of `%`,  `+`,
            ``, `"` and Unicode characters are not allowed.
        :type custom_external_caller_id_name: str
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
        if selected is not None:
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
        url = self.ep(f'{virtual_line_id}/callerId')
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

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
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

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
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
            body['callForwarding'] = loads(call_forwarding.model_dump_json())
        if business_continuity is not None:
            body['businessContinuity'] = loads(business_continuity.model_dump_json())
        url = self.ep(f'{virtual_line_id}/callForwarding')
        super().put(url, params=params, json=body)

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

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
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

    def retrieve_a_virtual_line_s_outgoing_calling_permissions_settings(self, virtual_line_id: str,
                                                                        org_id: str = None) -> OutgoingCallingPermissionsSetting:
        """
        Retrieve a virtual line's Outgoing Calling Permissions Settings

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
        :rtype: :class:`OutgoingCallingPermissionsSetting`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
        data = super().get(url, params=params)
        r = OutgoingCallingPermissionsSetting.model_validate(data)
        return r

    def modify_a_virtual_line_s_outgoing_calling_permissions_settings(self, virtual_line_id: str,
                                                                      use_custom_enabled: bool,
                                                                      calling_permissions: list[OutgoingCallingPermissionsSettingCallingPermissions],
                                                                      org_id: str = None):
        """
        Modify a virtual line's Outgoing Calling Permissions Settings

        Modify a virtual line's Outgoing Calling Permissions settings.

        Outgoing calling permissions regulate behavior for calls placed to various destinations and default to the
        local level settings. You can change the outgoing calling permissions for a virtual line if you want them to
        be different from your organization's default.

        Updating the outgoing permission settings for a virtual line requires a full or user administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param use_custom_enabled: When true, indicates that this virtual line uses the specified calling permissions
            when placing outbound calls.
        :type use_custom_enabled: bool
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: list[OutgoingCallingPermissionsSettingCallingPermissions]
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
        body['useCustomEnabled'] = use_custom_enabled
        body['callingPermissions'] = loads(TypeAdapter(list[OutgoingCallingPermissionsSettingCallingPermissions]).dump_json(calling_permissions, by_alias=True, exclude_none=True))
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
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

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
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
            body['incoming'] = loads(incoming.model_dump_json())
        if outgoing is not None:
            body['outgoing'] = loads(outgoing.model_dump_json())
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

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
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
