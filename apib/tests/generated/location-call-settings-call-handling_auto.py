from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallingPermissionObject', 'CallingPermissionObjectAction', 'CallingPermissionObjectCallType',
            'GeneratePasswordPostResponse', 'GetAutoTransferNumberObject', 'GetLocationAccessCodeObject',
            'GetLocationAccessCodeObjectAccessCodes', 'GetLocationInterceptObject',
            'GetLocationInterceptObjectIncoming', 'GetLocationInterceptObjectIncomingAnnouncements',
            'GetLocationInterceptObjectIncomingAnnouncementsGreeting',
            'GetLocationInterceptObjectIncomingAnnouncementsNewNumber', 'GetLocationInterceptObjectIncomingType',
            'GetLocationInterceptObjectOutgoing', 'GetLocationInterceptObjectOutgoingType',
            'GetLocationOutgoingPermissionResponse', 'InternalDialingGet', 'InternalDialingPut', 'PasswordGenerate',
            'PutAccessCodeLocationObject', 'RouteIdentity', 'RouteType', 'UnknownExtensionRouteIdentity']


class CallingPermissionObjectCallType(str, Enum):
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


class CallingPermissionObjectAction(str, Enum):
    #: Callers at this location can make these types of calls.
    allow = 'ALLOW'
    #: Callers at this location can't make these types of calls.
    block = 'BLOCK'
    #: Callers must enter the authorization code that you set before placing an outgoing call.
    auth_code = 'AUTH_CODE'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber1`.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber2`.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber3`.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermissionObject(ApiModel):
    #: Below are the call type values.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionObjectCallType] = None
    #: Allows to configure settings for each call type.
    #: example: ALLOW
    action: Optional[CallingPermissionObjectAction] = None
    #: If enabled, allow the person to transfer or forward internal calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class GeneratePasswordPostResponse(ApiModel):
    #: Example password.
    #: example: xyz123!
    example_sip_password: Optional[str] = None


class GetAutoTransferNumberObject(ApiModel):
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_1` will be transferred
    #: to this number.
    #: example: 1234456789
    auto_transfer_number1: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_2` will be transferred
    #: to this number.
    #: example: 2234567891
    auto_transfer_number2: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_3` will be transferred
    #: to this number.
    #: example: 3234567891
    auto_transfer_number3: Optional[str] = None


class GetLocationAccessCodeObjectAccessCodes(ApiModel):
    #: Access code number.
    #: example: 123
    code: Optional[datetime] = None
    #: Access code description.
    #: example: Main Access Code
    description: Optional[str] = None


class GetLocationAccessCodeObject(ApiModel):
    #: Access code details
    access_codes: Optional[GetLocationAccessCodeObjectAccessCodes] = None


class GetLocationInterceptObjectIncomingType(str, Enum):
    #: Intercept all inbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow all inbound calls.
    allow_all = 'ALLOW_ALL'


class GetLocationInterceptObjectIncomingAnnouncementsGreeting(str, Enum):
    #: Play default greeting.
    default = 'DEFAULT'
    #: Play custom greeting.
    custom = 'CUSTOM'


class GetLocationInterceptObjectIncomingAnnouncementsNewNumber(ApiModel):
    #: Enable/disable to play new number announcement.
    #: example: True
    enabled: Optional[bool] = None
    #: Incoming destination phone number to be announced.
    #: example: 2147691003
    destination: Optional[str] = None


class GetLocationInterceptObjectIncomingAnnouncements(ApiModel):
    #: Greeting type for location intercept.
    #: example: DEFAULT
    greeting: Optional[GetLocationInterceptObjectIncomingAnnouncementsGreeting] = None
    #: If set to `CUSTOM` for greeting, filename of previously uploaded file.
    #: example: .wav
    file_name: Optional[str] = None
    #: Settings for new number announcement.
    new_number: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None
    #: Transfer number details.
    zero_transfer: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None


class GetLocationInterceptObjectIncoming(ApiModel):
    #: Select inbound call options.
    #: example: INTERCEPT_ALL
    type: Optional[GetLocationInterceptObjectIncomingType] = None
    #: Enable/disable to route voice mail.
    #: example: True
    voicemail_enabled: Optional[bool] = None
    #: Announcements details.
    announcements: Optional[GetLocationInterceptObjectIncomingAnnouncements] = None


class GetLocationInterceptObjectOutgoingType(str, Enum):
    #: Intercept all outbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow local outbound calls.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class GetLocationInterceptObjectOutgoing(ApiModel):
    #: Outbound call modes
    #: example: INTERCEPT_ALL
    type: Optional[GetLocationInterceptObjectOutgoingType] = None
    #: Enable/disable to route all outbound calls to phone number.
    #: example: True
    transfer_enabled: Optional[bool] = None
    #: If enabled, set outgoing destination phone number.
    #: example: 2147691007
    destination: Optional[str] = None


class GetLocationInterceptObject(ApiModel):
    #: Enable/disable location intercept. Enable this feature to override any Location's Call Intercept settings that
    #: person configures.
    #: example: True
    enabled: Optional[bool] = None
    #: Inbound call details.
    incoming: Optional[GetLocationInterceptObjectIncoming] = None
    #: Outbound Call details
    outgoing: Optional[GetLocationInterceptObjectOutgoing] = None


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class RouteIdentity(ApiModel):
    #: ID of the route type.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: A unique name for the route identity.
    #: example: route_identity_name
    name: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class InternalDialingGet(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    #: example: True
    enable_unknown_extension_route_policy: Optional[bool] = None
    #: The selected route group/trunk as premises calls.
    unknown_extension_route_identity: Optional[RouteIdentity] = None


class UnknownExtensionRouteIdentity(ApiModel):
    #: ID of the route type.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class InternalDialingPut(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    #: example: True
    enable_unknown_extension_route_policy: Optional[bool] = None
    #: Type associated with the identity.
    unknown_extension_route_identity: Optional[UnknownExtensionRouteIdentity] = None


class PasswordGenerate(str, Enum):
    #: SIP password setting
    sip = 'SIP'


class PutAccessCodeLocationObject(ApiModel):
    #: Array of string to delete access codes. For example, ["1234","2345"]
    delete_codes: Optional[list[str]] = None


class GetLocationOutgoingPermissionResponse(ApiModel):
    #: Array of calling permissions.
    calling_permissions: Optional[list[CallingPermissionObject]] = None


class LocationCallSettingsCallHandlingApi(ApiChild, base='telephony/config/locations/{locationId}'):
    """
    Location Call Settings:  Call Handling
    
    Location Call Settings: Call Handling supports reading and writing of Webex
    Calling Location settings involving permissions and intercepting of inbound and
    outbound calls for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """
    ...