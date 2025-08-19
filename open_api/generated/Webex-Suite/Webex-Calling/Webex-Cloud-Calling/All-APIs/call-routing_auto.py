from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActionOnRouteList', 'AppliedServices', 'CallDestinationType', 'CallInterceptDetails',
           'CallInterceptDetailsPermission', 'CallRoutingApi', 'CallSourceInfo', 'CallSourceType',
           'CallingPermissionAction', 'CallingPlanReason', 'ConfigurationLevelType', 'Customer', 'DeviceStatus',
           'DeviceType', 'DialPattern', 'DialPatternStatus', 'DialPatternValidate', 'DialPatternValidateResult',
           'DialPatternValidationStatus', 'DialPlan', 'DialPlanGet', 'Emergency', 'FeatureAccessCode', 'HostedAgent',
           'HostedAgentType', 'HostedFeature', 'LocalGatewayUsageCount', 'LocalGateways',
           'LocationTranslationPatternGet', 'NumberStatus', 'OriginatorType',
           'OutgoingCallingPlanPermissionsByDigitPattern', 'OutgoingCallingPlanPermissionsByType',
           'OutgoingCallingPlanPermissionsByTypeCallType', 'PChargeInfoSupportPolicyType', 'PbxUser', 'PstnNumber',
           'ReadTheUsageOfARoutingGroupResponse', 'ResponseStatus', 'ResponseStatusType', 'RouteGroup',
           'RouteGroupGet', 'RouteGroupUsageRouteListGet', 'RouteGroupUsageRouteListItem', 'RouteList',
           'RouteListGet', 'RouteListNumberPatch', 'RouteListNumberPatchResponse', 'RouteType', 'ServiceType',
           'TestCallRoutingPostResponse', 'TranslationPattern', 'TranslationPatternConfigurationLevel',
           'TranslationPatternItem', 'Trunk', 'TrunkGet', 'TrunkType', 'TrunkTypeWithDeviceType', 'VirtualExtension',
           'VirtualExtensionRange']


class ActionOnRouteList(str, Enum):
    #: Add a phone number to the Route List.
    add = 'ADD'
    #: Delete a phone number from the Route List.
    delete = 'DELETE'


class TranslationPatternConfigurationLevel(str, Enum):
    #: The applied services of location level.
    location = 'LOCATION'
    #: The applied services of the organization level.
    organization = 'ORGANIZATION'


class TranslationPattern(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[TranslationPatternConfigurationLevel] = None
    #: Name given to a translation pattern.
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern.
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern.
    replacement_pattern: Optional[str] = None
    #: The original called number.
    matched_number: Optional[str] = None
    #: The modified number after matching against `matchingPattern` and replacing with corresponding
    #: `replacementPattern`.
    translated_number: Optional[str] = None


class ConfigurationLevelType(str, Enum):
    #: The applied services at the location level.
    location = 'LOCATION'
    #: The applied services at the people level.
    people = 'PEOPLE'
    #: The applied services at the place level.
    place = 'PLACE'
    #: The applied services at the virtual line level.
    virtual_line = 'VIRTUAL_LINE'


class CallInterceptDetailsPermission(str, Enum):
    #: Call intercept is disabled.
    disallow = 'DISALLOW'
    #: Call intercept is transferred to a number.
    transfer = 'TRANSFER'


class CallInterceptDetails(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevelType] = None
    #: The choices that indicate call intercept permissions.
    permission: Optional[CallInterceptDetailsPermission] = None
    #: The number to which the outgoing permission by type is to be transferred.
    transfer_number: Optional[str] = None


class OutgoingCallingPlanPermissionsByTypeCallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the
    #: originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the long-distance areas that require an international calling code before
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


class CallingPermissionAction(str, Enum):
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


class CallingPlanReason(str, Enum):
    #: Calling plan gives the Fraud Containment reason.
    fraud_containment = 'FRAUD_CONTAINMENT'
    #: The Cisco calling plan reason.
    cisco_calling_plan = 'CISCO_CALLING_PLAN'
    #: The reason if the transfer number 1 is not configured.
    transfer_number_1_not_configured = 'TRANSFER_NUMBER_1_NOT_CONFIGURED'
    #: The reason if the transfer number 2 is not configured.
    transfer_number_2_not_configured = 'TRANSFER_NUMBER_2_NOT_CONFIGURED'
    #: The reason if the transfer number 3 is not configured.
    transfer_number_3_not_configured = 'TRANSFER_NUMBER_3_NOT_CONFIGURED'
    #: The reason for Webex mobile international transfer forward.
    webex_mobile_premium_international_transfer_forward = 'WEBEX_MOBILE_PREMIUM_INTERNATIONAL_TRANSFER_FORWARD'


class OutgoingCallingPlanPermissionsByType(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevelType] = None
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    call_type: Optional[OutgoingCallingPlanPermissionsByTypeCallType] = None
    #: Action to be performed on the input number that matches with the OCP.
    permission: Optional[CallingPermissionAction] = None
    #: The number to which the outgoing permission by type is to be transferred.
    transfer_number: Optional[str] = None
    #: The reason for the result reported for non-standard OCP service.
    reason: Optional[CallingPlanReason] = None
    #: A transfer number is present in case it gets transferred to some other number.
    number: Optional[str] = None


class OutgoingCallingPlanPermissionsByDigitPattern(ApiModel):
    #: The level from which the configuration is applied.
    configuration_level: Optional[ConfigurationLevelType] = None
    #: Name given to a digit pattern.
    name: Optional[str] = None
    #: Action to be performed on the input number that matches with the digit pattern.
    permission: Optional[CallingPermissionAction] = None
    transfer_number: Optional[str] = None
    #: Pattern for the digit pattern.
    pattern: Optional[str] = None
    #: The reason for the result reported for a non-standard OCP service.
    reason: Optional[CallingPlanReason] = None
    #: A transfer number is present in case of a transfer to another number.
    number: Optional[str] = None


class AppliedServices(ApiModel):
    #: Returns the details of the Translation Pattern if applied.
    translation_pattern: Optional[TranslationPattern] = None
    #: Returns the details of call intercept if applied.
    intercept_details: Optional[CallInterceptDetails] = None
    #: Returns the details of permissions by type configuration if applied under OCP.
    outgoing_calling_plan_permissions_by_type: Optional[OutgoingCallingPlanPermissionsByType] = None
    #: Returns the details of the digit pattern configuration if applied under OCP.
    outgoing_calling_plan_permissions_by_digit_pattern: Optional[OutgoingCallingPlanPermissionsByDigitPattern] = None


class CallSourceType(str, Enum):
    #: Route list is a type of call source.
    route_list = 'ROUTE_LIST'
    #: Dial pattern is a type of call source.
    dial_pattern = 'DIAL_PATTERN'
    #: The call source extension is unknown.
    unkown_extension = 'UNKOWN_EXTENSION'
    #: The call source phone number is unknown.
    unkown_number = 'UNKOWN_NUMBER'


class CallSourceInfo(ApiModel):
    #: Type of call source.
    call_source_type: Optional[CallSourceType] = None
    #: Name of a route list.  When `originatorType` is `trunk`, `originatorId` is a valid trunk and the trunk belongs
    #: to a route group which is assigned to a route list with the name `routeListA` and also `originatorNumber` is a
    #: number assigned to `routeListA`, then `routeListA` is returned here. This element is returned when
    #: `callSourceType` is `ROUTE_LIST`.
    route_list_name: Optional[str] = None
    #: Unique identifier for the route list.
    route_list_id: Optional[str] = None
    #: Name of a dial plan. When `originatorType` is `trunk`, `originatorId` is a valid trunk with the name `trunkA`,
    #: `trunkA` belongs to a route group which is assigned to a route list with the name `routeListA`, `trunkA` is
    #: also assigned to `dialPlanA` as routing choice, `dialPlanA` has `dialPattern` xxxx assigned. If the
    #: `originatorNumber` matches the `dialPattern` `xxxx`, `dialPlanA` is returned. This element is returned when
    #: `callSourceType` is `DIAL_PATTERN`.
    dial_plan_name: Optional[str] = None
    #: Pattern given to a dial plan. When `originatorType` is `trunk`, `originatorId` is a valid trunk with the name
    #: `trunkA`, `trunkA` belongs to a route group which is assigned to a route list with the name `routeListA`,
    #: `trunkA` is also assigned to `dialPlanA` as routing choice, `dialPlanA` has `dialPattern` `xxxx` assigned. If
    #: the `originatorNumber` matches the `dialPattern` `xxxx`, `dialPattern` `xxxx` is returned. This element is
    #: returned when `callSourceType` is `DIAL_PATTERN`.
    dial_pattern: Optional[str] = None
    #: Unique identifier for dial plan.
    dial_plan_id: Optional[str] = None


class Customer(ApiModel):
    #: ID of the customer/organization.
    id: Optional[str] = None
    #: Name of the customer/organization.
    name: Optional[str] = None


class CallDestinationType(str, Enum):
    #: A destination is a person or workspace with details in the `hostedAgent` field.
    hosted_agent = 'HOSTED_AGENT'
    #: Destination is a calling feature like auto-attendant or hunt group with details in the `hostedFeature` field.
    hosted_feature = 'HOSTED_FEATURE'
    #: Destination routes into a separate PBX with details in the `pbxUser` field.
    pbx_user = 'PBX_USER'
    #: Destination routes into a PSTN phone number with details in the `pstnNumber` field.
    pstn_number = 'PSTN_NUMBER'
    #: Destination routes into a virtual extension with details in the `virtualExtension` field.
    virtual_extension = 'VIRTUAL_EXTENSION'
    #: Destination routes into a virtual extension range with details in the `virtualExtensionRange` field.
    virtual_extension_range = 'VIRTUAL_EXTENSION_RANGE'
    #: Destination routes into a route list with details in the `routeList` field.
    route_list = 'ROUTE_LIST'
    #: Destination routes into a feature access code (FAC) with details in the `featureAccessCode` field.
    fac = 'FAC'
    #: Destination routes into an emergency service like Red Sky, with details in the `emergency` field.
    emergency = 'EMERGENCY'
    #: The route is in a repair state with routing choice details in the `repair` field.
    repair = 'REPAIR'
    #: Target extension is unknown with routing choice details in the `unknownExtension` field.
    unknown_extension = 'UNKNOWN_EXTENSION'
    #: The target phone number is unknown with routing choice details in the `unknownNumber` field.
    unknown_number = 'UNKNOWN_NUMBER'


class DeviceStatus(str, Enum):
    #: Device is online
    online = 'ONLINE'
    #: Device is offline
    offline = 'OFFLINE'
    #: Unknown. Default
    unknown = 'UNKNOWN'


class DeviceType(ApiModel):
    #: Device type assosiated with trunk configuration.
    device_type: Optional[str] = None
    #: Minimum number of concurrent calls. Required for static certificate based trunk.
    min_concurrent_calls: Optional[int] = None
    #: Maximum number of concurrent calls. Required for static certificate based trunk.
    max_concurrent_calls: Optional[int] = None


class DialPattern(ApiModel):
    #: A unique dial pattern.
    dial_pattern: Optional[str] = None
    #: Action to add or delete a pattern.
    action: Optional[ActionOnRouteList] = None


class DialPatternStatus(str, Enum):
    #: Invalid pattern
    invalid = 'INVALID'
    #: Duplicate pattern
    duplicate = 'DUPLICATE'
    #: Duplicate in input
    duplicate_in_list = 'DUPLICATE_IN_LIST'


class DialPatternValidate(ApiModel):
    #: Input dial pattern that is being validated.
    dial_pattern: Optional[str] = None
    #: Validation status.
    pattern_status: Optional[DialPatternStatus] = None
    #: Failure details.
    message: Optional[str] = None


class DialPatternValidationStatus(str, Enum):
    #: In case one or more dial pattern validation failed
    errors = 'ERRORS'
    #: If all the patterns are validated successfully
    ok = 'OK'


class DialPatternValidateResult(ApiModel):
    #: Overall validation result status.
    status: Optional[DialPatternValidationStatus] = None
    #: Patterns validation result.
    dial_pattern_status: Optional[list[DialPatternValidate]] = None


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class DialPlan(ApiModel):
    #: Unique identifier for the dial plan.
    id: Optional[str] = None
    #: A unique name for the dial plan.
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    route_id: Optional[str] = None
    #: Name of route type associated with the dial plan.
    route_name: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None


class DialPlanGet(ApiModel):
    #: Unique identifier for the dial plan.
    id: Optional[str] = None
    #: A unique name for the dial plan.
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    route_id: Optional[str] = None
    #: Name of route type associated with the dial plan.
    route_name: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None
    #: Customer information.
    customer: Optional[Customer] = None


class Emergency(ApiModel):
    #: If `RedSky` is in use.
    is_red_sky: Optional[bool] = None
    #: Name of the trunk.
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    trunk_id: Optional[str] = None
    #: Name of the route group that is associated with trunk specified by `trunkId`.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    trunk_location_name: Optional[str] = None
    #: Unique identifier of the location of the trunk; required if `trunkName` is returned.
    trunk_location_id: Optional[str] = None


class FeatureAccessCode(ApiModel):
    #: Feature access code to which the call is directed.
    code: Optional[str] = None
    #: Name of the feature associated with `code`.
    name: Optional[str] = None


class HostedAgentType(str, Enum):
    #: This object is a person.
    people = 'PEOPLE'
    #: A workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'


class HostedAgent(ApiModel):
    #: Unique identifier for the person or workspace agent identified as call destination.
    id: Optional[str] = None
    #: Type of agent for call destination.
    type: Optional[HostedAgentType] = None
    #: First name for the hosted agent specified by `id`.
    first_name: Optional[str] = None
    #: Last name for the hosted agent specified by `id`.
    last_name: Optional[str] = None
    #: Name of hosted agent's location.
    location_name: Optional[str] = None
    #: Unique identifier for hosted agent's location.
    location_id: Optional[str] = None
    #: Phone number for the hosted agent.
    phone_number: Optional[str] = None
    #: Extension for the hosted agent.
    extension: Optional[str] = None


class ServiceType(str, Enum):
    #: The destination is an auto attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: The destination is the Office (Broadworks) Anywhere feature.
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    #: The destination is the Call Queue feature.
    call_queue = 'CALL_QUEUE'
    #: The destination is the Contact Center Link feature.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: The destination is the Group Paging feature.
    group_paging = 'GROUP_PAGING'
    #: The destination is the Hunt Group feature.
    hunt_group = 'HUNT_GROUP'
    #: The destination is the Voice Messaging feature.
    voice_messaging = 'VOICE_MESSAGING'
    #: The destination is the Voice Mail Group feature.
    voice_mail_group = 'VOICE_MAIL_GROUP'


class HostedFeature(ApiModel):
    #: Type of the service identified as call destination.
    type: Optional[ServiceType] = None
    #: Name of the service identified as call destination.
    name: Optional[str] = None
    #: Unique identifier of the service identified as call destination.
    id: Optional[str] = None
    #: Name of the location with which the service is associated.
    location_name: Optional[str] = None
    #: Unique identifier for the location of the service.
    location_id: Optional[str] = None
    #: Phone number of the service.
    phone_number: Optional[str] = None
    #: Extension of the service.
    extension: Optional[str] = None


class LocalGatewayUsageCount(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    pstn_connection_count: Optional[int] = None
    #: The count where the given local gateway is used as call to extension setting.
    call_to_extension_count: Optional[int] = None
    #: The count where the given local gateway is used by the dial plan.
    dial_plan_count: Optional[int] = None
    #: The count where the given local gateway is used by the route group.
    route_group_count: Optional[int] = None


class LocalGateways(ApiModel):
    #: ID of type local gateway.
    id: Optional[str] = None
    #: Name of the local gateway.
    name: Optional[str] = None
    #: Location ID to which local gateway belongs.
    location_id: Optional[str] = None
    #: Prioritizes local gateways based on these numbers; the lowest number gets the highest priority.
    priority: Optional[int] = None


class LocationTranslationPatternGet(ApiModel):
    #: Unique identifier for a translation pattern.
    id: Optional[str] = None
    #: A name given to a translation pattern for a location.
    name: Optional[str] = None
    #: A matching pattern given to a translation pattern for a location.
    matching_pattern: Optional[str] = None
    #: A replacement pattern given to a translation pattern for a location.
    replacement_pattern: Optional[str] = None


class NumberStatus(str, Enum):
    invalid = 'INVALID'
    duplicate = 'DUPLICATE'
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    unavailable = 'UNAVAILABLE'


class OriginatorType(str, Enum):
    #: The originator type object is a person.
    people = 'PEOPLE'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class PbxUser(ApiModel):
    #: Dial plan name that the called string matches.
    dial_plan_name: Optional[str] = None
    #: Unique identifier for the dial plan.
    dial_plan_id: Optional[str] = None
    #: Dial pattern that the called string matches.
    dial_pattern: Optional[str] = None
    #: Name of the trunk.
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    trunk_id: Optional[str] = None
    #: Name of the route group.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    trunk_location_id: Optional[str] = None


class PstnNumber(ApiModel):
    #: Name of the trunk.
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    trunk_id: Optional[str] = None
    #: Name of the route group.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    trunk_location_id: Optional[str] = None


class ResponseStatusType(str, Enum):
    #: Error
    error = 'ERROR'
    #: Warning
    warning = 'WARNING'


class ResponseStatus(ApiModel):
    #: Error Code. 25013 for error retrieving the outbound proxy. 25014 for error retrieving the status
    code: Optional[int] = None
    #: Status type.
    type: Optional[ResponseStatusType] = None
    #: Error summary in English.
    summary_english: Optional[str] = None
    #: Error Details.
    detail: Optional[list[str]] = None
    #: Error Tracking ID.
    tracking_id: Optional[str] = None


class RouteGroup(ApiModel):
    #: Route group ID the Route list is associated with.
    id: Optional[str] = None
    #: Name of the Route group the Route list associated with.
    name: Optional[str] = None
    #: Flag to indicate if the route group is used.
    in_use: Optional[bool] = None


class RouteGroupGet(ApiModel):
    #: Name of the route group.
    name: Optional[str] = None
    #: Organization details.
    organization: Optional[Customer] = None
    #: Local Gateways that are part of this Route Group.
    local_gateways: Optional[list[LocalGateways]] = None


class RouteGroupUsageRouteListItem(ApiModel):
    #: Route list ID.
    id: Optional[str] = None
    #: Route list name.
    name: Optional[str] = None
    #: Location ID for route list.
    location_id: Optional[str] = None
    #: Location name for route list.
    location_name: Optional[str] = None


class RouteGroupUsageRouteListGet(ApiModel):
    #: List of route lists for this route group.
    route_lists: Optional[list[RouteGroupUsageRouteListItem]] = None


class RouteList(ApiModel):
    #: Unique identifier of the route list.
    id: Optional[str] = None
    #: Name of the route list.
    name: Optional[str] = None
    #: Name of the route group the route list is associated with.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group the route list is associated with.
    route_group_id: Optional[str] = None
    #: Location name of the route list.
    location_name: Optional[str] = None
    #: Location ID of the route list.
    location_id: Optional[str] = None


class RouteListGet(ApiModel):
    #: Route list name.
    name: Optional[str] = None
    #: Location associated with the Route List.
    location: Optional[Customer] = None
    #: Route group associated with the Route list.
    route_group: Optional[RouteGroup] = None


class RouteListNumberPatch(ApiModel):
    #: Number to be deleted/added.
    number: Optional[str] = None
    #: Possible value, `ADD` or `DELETE`.
    action: Optional[ActionOnRouteList] = None


class RouteListNumberPatchResponse(ApiModel):
    #: Phone Number whose status is being reported.
    phone_number: Optional[str] = None
    #: Status of the number. Possible values are `INVALID`, `DUPLICATE`, `DUPLICATE_IN_LIST`, or `UNAVAILABLE`.
    number_status: Optional[NumberStatus] = None
    #: Message of the number add status.
    message: Optional[str] = None


class VirtualExtension(ApiModel):
    #: Unique identifier for the virtual extension.
    id: Optional[str] = None
    #: First name of the virtual extension.
    first_name: Optional[str] = None
    #: Last name of the virtual extension.
    last_name: Optional[str] = None
    #: Full name of the virtual extension.
    display_name: Optional[str] = None
    #: Extension that the virtual extension is associated with.
    extension: Optional[str] = None
    #: Phone number that the virtual extension is associated with.
    phone_number: Optional[str] = None
    #: Location name if the virtual extension is at the location level, empty if it is at the customer level.
    location_name: Optional[str] = None
    #: Location ID if the virtual extension is at the location level, empty if it is at the customer level.
    location_id: Optional[str] = None
    #: Name of the trunk.
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    trunk_id: Optional[str] = None
    #: Name of the route group.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    trunk_location_id: Optional[str] = None


class VirtualExtensionRange(ApiModel):
    #: Unique identifier for virtual extension range.
    id: Optional[str] = None
    #: Name of the virtual extension range.
    name: Optional[str] = None
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix;
    #: BCD/Enhanced mode can have any valid prefix).
    prefix: Optional[str] = None
    #: Pattern associated with the virtual extension range.
    pattern: Optional[str] = None
    #: Location name if the virtual extension range is at the location level, empty if it is at the customer level.
    location_name: Optional[str] = None
    #: Location ID if the virtual extension range is at the location level, empty if it is at customer level.
    location_id: Optional[str] = None
    #: Name of the trunk.
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    trunk_id: Optional[str] = None
    #: Name of the route group.
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    trunk_location_id: Optional[str] = None


class TestCallRoutingPostResponse(ApiModel):
    #: Only returned when `originatorNumber` is specified in the request.
    call_source_info: Optional[CallSourceInfo] = None
    #: Destination type for the call.
    destination_type: Optional[CallDestinationType] = None
    #: FAC code if `destinationType` is FAC. The routing address will be returned for all other destination types.
    routing_address: Optional[str] = None
    #: Outside access code.
    outside_access_code: Optional[str] = None
    #: `true` if the call would be rejected.
    is_rejected: Optional[bool] = None
    #: Returned when `destinationType` is `HOSTED_AGENT`.
    hosted_agent: Optional[HostedAgent] = None
    #: Returned when `destinationType` is `HOSTED_FEATURE`.
    hosted_feature: Optional[HostedFeature] = None
    #: Returned when `destinationType` is `PBX_USER`.
    pbx_user: Optional[PbxUser] = None
    #: Returned when `destinationType` is `PSTN_NUMBER`.
    pstn_number: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `VIRTUAL_EXTENSION`.
    virtual_extension: Optional[VirtualExtension] = None
    #: Returned when `destinationType` is `VIRTUAL_EXTENSION_RANGE`.
    virtual_extension_range: Optional[VirtualExtensionRange] = None
    #: Returned when `destinationType` is `ROUTE_LIST`.
    route_list: Optional[RouteList] = None
    #: Returned when `destinationType` is `FAC`.
    feature_access_code: Optional[FeatureAccessCode] = None
    #: Returned when `destinationType` is `EMERGENCY`.
    emergency: Optional[Emergency] = None
    #: Returned when `destinationType` is `REPAIR`.
    repair: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `UNKNOWN_EXTENSION`.
    unknown_extension: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `UNKNOWN_NUMBER`.
    unknown_number: Optional[PstnNumber] = None
    #: Returned if any origin is configured with intercept details, outgoing permissions by type, or translation
    #: pattern.
    applied_services: Optional[list[AppliedServices]] = None


class TranslationPatternItem(ApiModel):
    #: Unique identifier for a translation pattern.
    id: Optional[str] = None
    #: Name given to a translation pattern for an organization.
    name: Optional[str] = None
    #: Matching pattern given to a translation pattern for an organization.
    matching_pattern: Optional[str] = None
    #: Replacement pattern given to a translation pattern for an organization.
    replacement_pattern: Optional[str] = None
    #: Level at which the translation pattern is created. The level can either be `Organization` or `Location`.
    level: Optional[str] = None
    #: Location details for the translation pattern when the level is `Location`.
    location: Optional[Customer] = None


class TrunkType(str, Enum):
    #: For Cisco CUBE Local Gateway.
    registering = 'REGISTERING'
    #: For Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller,
    #: Ribbon Session Border Controller.
    certificate_based = 'CERTIFICATE_BASED'


class Trunk(ApiModel):
    #: Unique identifier for the trunk.
    id: Optional[str] = None
    #: A unique name for the trunk.
    name: Optional[str] = None
    #: Location associated with the trunk.
    location: Optional[Customer] = None
    #: Trunk in use flag.
    in_use: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Flag to indicate if the trunk is restricted to a dedicated instance.
    is_restricted_to_dedicated_instance: Optional[bool] = None


class PChargeInfoSupportPolicyType(str, Enum):
    #: The P-Charge-Info header support policy is disabled.
    disabled = 'DISABLED'
    #: The P-Charge-Info header is always included in outbound PSTN calls using Webex Calling primary number or
    #: location’s main number.
    asserted_identity = 'ASSERTED_IDENTITY'
    #: The P-Charge-Info header is included in outbound PSTN calls using the originating or redirecting Webex Calling
    #: entity's location charge number if set, else the entity's primary number if set and not toll-free, else the
    #: main number of the entity's location if set and not toll-free. If none of these are set or not toll-free, it
    #: uses the same number as the ASSERTED_IDENTITY option.
    configurable_charge_number = 'CONFIGURABLE_CHARGE_NUMBER'


class TrunkGet(ApiModel):
    #: A unique name for the trunk.
    name: Optional[str] = None
    #: Customer associated with the trunk.
    customer: Optional[Customer] = None
    #: Location associated with the trunk.
    location: Optional[Customer] = None
    #: Unique Outgoing and Destination trunk group associated with the dial plan.
    otg_dtg_id: Optional[str] = None
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    line_port: Optional[str] = None
    #: Locations using trunk.
    locations_using_trunk: Optional[list[Customer]] = None
    #: User ID.
    pilot_user_id: Optional[str] = None
    #: Contains the body of the HTTP response received following the request to Console API and will not be set if the
    #: response has no body.
    outbound_proxy: Optional[dict] = None
    #: User's authentication service information.
    sip_authentication_user_name: Optional[str] = None
    #: Device status.
    status: Optional[DeviceStatus] = None
    #: Error codes.
    error_codes: Optional[list[str]] = None
    #: Present partial error/warning status information included when the http response is 206.
    response_status: Optional[ResponseStatus] = None
    #: Determines the behavior of the From and PAI headers on outbound calls.
    dual_identity_support_enabled: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Device type assosiated with trunk.
    device_type: Optional[str] = None
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    address: Optional[str] = None
    #: Domain name. Required to create a static certificate based trunk.
    domain: Optional[str] = None
    #: FQDN port. Required to create a static certificate-based trunk.
    port: Optional[int] = None
    #: Max Concurrent call. Required to create a static certificate based trunk.
    max_concurrent_calls: Optional[int] = None
    #: Flag to indicate if the trunk is restricted to a dedicated instance.
    is_restricted_to_dedicated_instance: Optional[bool] = None
    p_charge_info_support_policy: Optional[PChargeInfoSupportPolicyType] = None


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Device types for trunk configuration.
    device_types: Optional[list[DeviceType]] = None


class ReadTheUsageOfARoutingGroupResponse(ApiModel):
    #: Number of PSTN connection locations associated to this route group.
    pstn_connection_count: Optional[str] = None
    #: Number of call to extension locations associated to this route group.
    call_to_extension_count: Optional[str] = None
    #: Number of dial plan locations associated to this route group.
    dial_plan_count: Optional[str] = None
    #: Number of route list locations associated to this route group.
    route_list_count: Optional[str] = None


class CallRoutingApi(ApiChild, base='telephony/config'):
    """
    Call Routing
    
    Features: Call Routing supports reading and writing of Webex Calling On-premises, also known as Local Gateway, Call
    Routing PSTN settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def test_call_routing(self, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, include_applied_services: bool = None,
                          org_id: str = None) -> TestCallRoutingPostResponse:
        """
        Test Call Routing

        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Test call routing requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param originator_id: This element is used to identify the originating party. It can be a person ID or a trunk
            ID.
        :type originator_id: str
        :param originator_type: This element is used to identify if the `originatorId` is of type `PEOPLE` or `TRUNK`.
        :type originator_type: OriginatorType
        :param destination: This element specifies the called party. It can be any dialable string, for example, an ESN
            number, E.164 number, hosted user DN, extension, extension with location code, URL, or FAC code.
        :type destination: str
        :param originator_number: Only used when `originatorType` is `TRUNK`. The `originatorNumber` can be a phone
            number or URI.
        :type originator_number: str
        :param include_applied_services: This element is used to retrieve if any translation pattern, call intercept,
            permission by type or permission by digit pattern is present for the called party.
        :type include_applied_services: bool
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :rtype: :class:`TestCallRoutingPostResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['originatorId'] = originator_id
        body['originatorType'] = enum_str(originator_type)
        if originator_number is not None:
            body['originatorNumber'] = originator_number
        body['destination'] = destination
        if include_applied_services is not None:
            body['includeAppliedServices'] = include_applied_services
        url = self.ep('actions/testCallRouting/invoke')
        data = super().post(url, params=params, json=body)
        r = TestCallRoutingPostResponse.model_validate(data)
        return r

    def retrieve_the_list_of_translation_patterns(self, limit_to_location_id: str = None,
                                                  limit_to_org_level_enabled: str = None, order: str = None,
                                                  name: str = None, matching_pattern: str = None, org_id: str = None,
                                                  **params) -> Generator[TranslationPatternItem, None, None]:
        """
        Retrieve the list of Translation Patterns

        Retrieve a list of translation patterns for a given organization.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param limit_to_location_id: When a location ID is passed, then return only the corresponding location level
            translation patterns.
        :type limit_to_location_id: str
        :param limit_to_org_level_enabled: When set to be `true`, then return only the organization-level translation
            patterns.
        :type limit_to_org_level_enabled: str
        :param order: Sort the list of translation patterns according to translation pattern name, ascending or
            descending.
        :type order: str
        :param name: Only return translation patterns with the matching `name`.
        :type name: str
        :param matching_pattern: Only return translation patterns with the matching `matchingPattern`.
        :type matching_pattern: str
        :param org_id: ID of the organization containing the translation patterns.
        :type org_id: str
        :return: Generator yielding :class:`TranslationPatternItem` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if limit_to_location_id is not None:
            params['limitToLocationId'] = limit_to_location_id
        if limit_to_org_level_enabled is not None:
            params['limitToOrgLevelEnabled'] = limit_to_org_level_enabled
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        if matching_pattern is not None:
            params['matchingPattern'] = matching_pattern
        url = self.ep('callRouting/translationPatterns')
        return self.session.follow_pagination(url=url, model=TranslationPatternItem, item_key='translationPatterns', params=params)

    def create_a_translation_pattern_for_an_organization(self, name: str, matching_pattern: str,
                                                         replacement_pattern: str, org_id: str = None) -> str:
        """
        Create a Translation Pattern for an Organization

        Create a translation pattern for a given organization.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param name: Name given to a translation pattern for an organization.
        :type name: str
        :param matching_pattern: Matching pattern given to a translation pattern for an organization.
        :type matching_pattern: str
        :param replacement_pattern: Replacement pattern given to a translation pattern for an organization.
        :type replacement_pattern: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['matchingPattern'] = matching_pattern
        body['replacementPattern'] = replacement_pattern
        url = self.ep('callRouting/translationPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_specific_translation_pattern(self, translation_id: str, org_id: str = None):
        """
        Delete a specific Translation Pattern

        Delete a translation pattern for a given organization.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param translation_id: Delete a translation pattern with the matching ID.
        :type translation_id: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRouting/translationPatterns/{translation_id}')
        super().delete(url, params=params)

    def retrieve_a_specific_translation_pattern_for_an_organization(self, translation_id: str,
                                                                    org_id: str = None) -> LocationTranslationPatternGet:
        """
        Retrieve a specific Translation Pattern for an Organization

        Retrieve the details of a translation pattern for a given organization.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param translation_id: Retrieve the translation pattern with the matching ID.
        :type translation_id: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: :class:`LocationTranslationPatternGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRouting/translationPatterns/{translation_id}')
        data = super().get(url, params=params)
        r = LocationTranslationPatternGet.model_validate(data)
        return r

    def modify_a_specific_translation_pattern_for_an_organization(self, translation_id: str, name: str = None,
                                                                  matching_pattern: str = None,
                                                                  replacement_pattern: str = None,
                                                                  org_id: str = None):
        """
        Modify a specific Translation Pattern for an Organization

        Modify a translation pattern for a given organization.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param translation_id: Modify translation pattern with the matching ID.
        :type translation_id: str
        :param name: Name given to a translation pattern for an organization.
        :type name: str
        :param matching_pattern: Matching pattern given to a translation pattern for an organization.
        :type matching_pattern: str
        :param replacement_pattern: Replacement pattern given to a translation pattern for an organization.
        :type replacement_pattern: str
        :param org_id: ID of the organization containing the translation pattern.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if matching_pattern is not None:
            body['matchingPattern'] = matching_pattern
        if replacement_pattern is not None:
            body['replacementPattern'] = replacement_pattern
        url = self.ep(f'callRouting/translationPatterns/{translation_id}')
        super().put(url, params=params, json=body)

    def create_a_translation_pattern_for_a_location(self, location_id: str, name: str, matching_pattern: str,
                                                    replacement_pattern: str, org_id: str = None) -> str:
        """
        Create a Translation Pattern for a Location

        Create a translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param name: A name given to a translation pattern for a location.
        :type name: str
        :param matching_pattern: A matching pattern given to a translation pattern for a location.
        :type matching_pattern: str
        :param replacement_pattern: A replacement pattern given to a translation pattern for a location.
        :type replacement_pattern: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['matchingPattern'] = matching_pattern
        body['replacementPattern'] = replacement_pattern
        url = self.ep(f'locations/{location_id}/callRouting/translationPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                             org_id: str = None):
        """
        Delete a specific Translation Pattern for a Location

        Delete a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRouting/translationPatterns/{translation_id}')
        super().delete(url, params=params)

    def retrieve_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                               org_id: str = None) -> LocationTranslationPatternGet:
        """
        Retrieve a specific Translation Pattern for a Location

        Retrieve a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: :class:`LocationTranslationPatternGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRouting/translationPatterns/{translation_id}')
        data = super().get(url, params=params)
        r = LocationTranslationPatternGet.model_validate(data)
        return r

    def modify_a_specific_translation_pattern_for_a_location(self, location_id: str, translation_id: str,
                                                             name: str = None, matching_pattern: str = None,
                                                             replacement_pattern: str = None, org_id: str = None):
        """
        Modify a specific Translation Pattern for a Location

        Modify a specific translation pattern for a given location.

        A translation pattern lets you manipulate dialed digits before routing a call and applies to outbound calls
        only. See `this article
        <https://help.webex.com/en-us/article/nib9o6h/Translation-patterns-for-outbound-calls>`_ for details about the translation pattern syntax.

        Requires a full administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param translation_id: Unique identifier for the translation pattern.
        :type translation_id: str
        :param name: A name given to a translation pattern for a location.
        :type name: str
        :param matching_pattern: A matching pattern given to a translation pattern for a location.
        :type matching_pattern: str
        :param replacement_pattern: A replacement pattern given to a translation pattern for a location.
        :type replacement_pattern: str
        :param org_id: Only admin users of another organization (such as partners) may use this parameter since the
            default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if matching_pattern is not None:
            body['matchingPattern'] = matching_pattern
        if replacement_pattern is not None:
            body['replacementPattern'] = replacement_pattern
        url = self.ep(f'locations/{location_id}/callRouting/translationPatterns/{translation_id}')
        super().put(url, params=params, json=body)

    def validate_a_dial_pattern(self, dial_patterns: list[str], org_id: str = None) -> DialPatternValidateResult:
        """
        Validate a Dial Pattern.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Validating a dial pattern requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param dial_patterns: Array of dial patterns.
        :type dial_patterns: list[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: :class:`DialPatternValidateResult`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['dialPatterns'] = dial_patterns
        url = self.ep('premisePstn/actions/validateDialPatterns/invoke')
        data = super().post(url, params=params, json=body)
        r = DialPatternValidateResult.model_validate(data)
        return r

    def read_the_list_of_dial_plans(self, dial_plan_name: str = None, route_group_name: str = None,
                                    trunk_name: str = None, order: str = None, org_id: str = None,
                                    **params) -> Generator[DialPlan, None, None]:
        """
        Read the List of Dial Plans

        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan.  Dial plans are
        configured globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the Trunk name..
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields.  Available sort fields: `name`,
            `routeName`, `routeType`. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return: Generator yielding :class:`DialPlan` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if dial_plan_name is not None:
            params['dialPlanName'] = dial_plan_name
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/dialPlans')
        return self.session.follow_pagination(url=url, model=DialPlan, item_key='dialPlans', params=params)

    def create_a_dial_plan(self, name: str, route_id: str, route_type: RouteType, dial_patterns: list[str] = None,
                           org_id: str = None) -> str:
        """
        Create a Dial Plan

        Create a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Creating a dial plan requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        :param dial_patterns: An Array of dial patterns.
        :type dial_patterns: list[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['routeId'] = route_id
        body['routeType'] = enum_str(route_type)
        if dial_patterns is not None:
            body['dialPatterns'] = dial_patterns
        url = self.ep('premisePstn/dialPlans')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_dial_plan(self, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan

        Delete a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Deleting a dial plan requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        super().delete(url, params=params)

    def get_a_dial_plan(self, dial_plan_id: str, org_id: str = None) -> DialPlanGet:
        """
        Get a Dial Plan

        Get a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving a dial plan requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: :class:`DialPlanGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        data = super().get(url, params=params)
        r = DialPlanGet.model_validate(data)
        return r

    def modify_a_dial_plan(self, dial_plan_id: str, name: str, route_id: str, route_type: RouteType,
                           org_id: str = None):
        """
        Modify a Dial Plan

        Modify a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Modifying a dial plan requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['routeId'] = route_id
        body['routeType'] = enum_str(route_type)
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        super().put(url, params=params, json=body)

    def modify_dial_patterns(self, dial_plan_id: str, dial_patterns: list[DialPattern] = None,
                             delete_all_dial_patterns: bool = None, org_id: str = None):
        """
        Modify Dial Patterns

        Modify dial patterns for the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Modifying a dial pattern requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the request
            is not modified.
        :type dial_patterns: list[DialPattern]
        :param delete_all_dial_patterns: Delete all the dial patterns for a dial plan.
        :type delete_all_dial_patterns: bool
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if dial_patterns is not None:
            body['dialPatterns'] = TypeAdapter(list[DialPattern]).dump_python(dial_patterns, mode='json', by_alias=True, exclude_none=True)
        if delete_all_dial_patterns is not None:
            body['deleteAllDialPatterns'] = delete_all_dial_patterns
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        super().put(url, params=params, json=body)

    def read_the_list_of_routing_groups(self, name: str = None, order: str = None, org_id: str = None,
                                        **params) -> Generator[RouteGroup, None, None]:
        """
        Read the List of Routing Groups

        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Return the list of route groups matching the Route group name..
        :type name: str
        :param order: Order the route groups according to designated fields.  Available sort orders are `asc` and
            `desc`.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: Generator yielding :class:`RouteGroup` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/routeGroups')
        return self.session.follow_pagination(url=url, model=RouteGroup, item_key='routeGroups', params=params)

    def create_route_group_for_a_organization(self, name: str, local_gateways: list[LocalGateways],
                                              org_id: str = None) -> str:
        """
        Create Route Group for a Organization

        Creates a Route Group for the organization.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Creating a Route Group requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: list[LocalGateways]
        :param org_id: Organization to which the Route Group belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['localGateways'] = TypeAdapter(list[LocalGateways]).dump_python(local_gateways, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('premisePstn/routeGroups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def remove_a_route_group_from_an_organization(self, route_group_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization

        Remove a Route Group from an Organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Removing a Route Group requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().delete(url, params=params)

    def read_a_route_group_for_a_organization(self, route_group_id: str, org_id: str = None) -> RouteGroupGet:
        """
        Read a Route Group for a Organization

        Reads a Route Group for the organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Reading a Route Group requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: :class:`RouteGroupGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        data = super().get(url, params=params)
        r = RouteGroupGet.model_validate(data)
        return r

    def modify_a_route_group_for_a_organization(self, route_group_id: str, name: str,
                                                local_gateways: list[LocalGateways], org_id: str = None):
        """
        Modify a Route Group for a Organization

        Modifies an existing Route Group for an organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Modifying a Route Group requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: list[LocalGateways]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['localGateways'] = TypeAdapter(list[LocalGateways]).dump_python(local_gateways, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().put(url, params=params, json=body)

    def read_the_usage_of_a_routing_group(self, route_group_id: str,
                                          org_id: str = None) -> ReadTheUsageOfARoutingGroupResponse:
        """
        Read the Usage of a Routing Group

        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
        specific Route Group.
        Users within Call to Extension locations are registered to a PBX which allows you to route unknown extensions
        (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route Group.
        PSTN Connections may be a Cisco PSTN, a cloud-connected PSTN, or a premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group.
        Route Lists are a list of numbers that can be reached via a route group and can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving usage information requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with the specific route group.
        :type org_id: str
        :rtype: :class:`ReadTheUsageOfARoutingGroupResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usage')
        data = super().get(url, params=params)
        r = ReadTheUsageOfARoutingGroupResponse.model_validate(data)
        return r

    def read_the_call_to_extension_locations_of_a_routing_group(self, route_group_id: str, location_name: str = None,
                                                                order: str = None, org_id: str = None,
                                                                **params) -> Generator[Customer, None, None]:
        """
        Read the Call to Extension Locations of a Routing Group

        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to the
        PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields.  Available sort orders are `asc`, and `desc`.
        :type order: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageCallToExtension')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_dial_plan_locations_of_a_routing_group(self, route_group_id: str, location_name: str = None,
                                                        order: str = None, org_id: str = None,
                                                        **params) -> Generator[Customer, None, None]:
        """
        Read the Dial Plan Locations of a Routing Group

        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location.
        A Dial Plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns. Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields.  Available sort orders are `asc`, and `desc`.
        :type order: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_pstn_connection_locations_of_a_routing_group(self, route_group_id: str, location_name: str = None,
                                                              order: str = None, org_id: str = None,
                                                              **params) -> Generator[Customer, None, None]:
        """
        Read the PSTN Connection Locations of a Routing Group

        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields.  Available sort orders are `asc`, and `desc`.
        :type order: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usagePstnConnection')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_route_lists_of_a_routing_group(self, route_group_id: str, name: str = None, order: str = None,
                                                org_id: str = None,
                                                **params) -> Generator[RouteGroupUsageRouteListGet, None, None]:
        """
        Read the Route Lists of a Routing Group

        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a Route
        Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param name: Return the list of locations matching the location name.
        :type name: str
        :param order: Order the locations according to designated fields.  Available sort orders are `asc`, and `desc`.
        :type order: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :return: Generator yielding :class:`RouteGroupUsageRouteListGet` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageRouteList')
        return self.session.follow_pagination(url=url, model=RouteGroupUsageRouteListGet, item_key='routeGroupUsageRouteListGet', params=params)

    def read_the_list_of_route_lists(self, order: str = None, name: list[str] = None, location_id: list[str] = None,
                                     org_id: str = None, **params) -> Generator[RouteList, None, None]:
        """
        Read the List of Route Lists

        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param order: Order the Route List according to the designated fields. Available sort fields are `name`, and
            `locationId`. Sort order is ascending by default
        :type order: str
        :param name: Return the list of Route List matching the route list name.
        :type name: list[str]
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: list[str]
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: Generator yielding :class:`RouteList` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = ','.join(name)
        if location_id is not None:
            params['locationId'] = ','.join(location_id)
        url = self.ep('premisePstn/routeLists')
        return self.session.follow_pagination(url=url, model=RouteList, item_key='routeLists', params=params)

    def create_a_route_list(self, name: str, location_id: str, route_group_id: str, org_id: str = None) -> str:
        """
        Create a Route List

        Create a Route List for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Creating a Route List requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Name of the Route List
        :type name: str
        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param route_group_id: ID of the route group associated with Route List.
        :type route_group_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['locationId'] = location_id
        body['routeGroupId'] = route_group_id
        url = self.ep('premisePstn/routeLists')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_route_list(self, route_list_id: str, org_id: str = None):
        """
        Delete a Route List

        Delete a route list for a customer.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Deleting a Route List requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().delete(url, params=params)

    def get_a_route_list(self, route_list_id: str, org_id: str = None) -> RouteListGet:
        """
        Get a Route List

        Get a rout list details.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: :class:`RouteListGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        data = super().get(url, params=params)
        r = RouteListGet.model_validate(data)
        return r

    def modify_a_route_list(self, route_list_id: str, name: str = None, route_group_id: str = None,
                            org_id: str = None):
        """
        Modify a Route List

        Modify the details for a Route List.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param name: Route List new name.
        :type name: str
        :param route_group_id: New route group ID.
        :type route_group_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if route_group_id is not None:
            body['routeGroupId'] = route_group_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().put(url, params=params, json=body)

    def get_numbers_assigned_to_a_route_list(self, route_list_id: str, number: str = None, order: str = None,
                                             org_id: str = None, **params) -> Generator[str, None, None]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param number: Number assigned to the route list.
        :type number: str
        :param order: Order the Route Lists according to number, ascending or descending.
        :type order: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :return: Numbers assigned to the Route list.
        """
        if org_id is not None:
            params['orgId'] = org_id
        if number is not None:
            params['number'] = number
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        return self.session.follow_pagination(url=url, model=None, item_key='numbers', params=params)

    def modify_numbers_for_route_list(self, route_list_id: str, numbers: list[RouteListNumberPatch] = None,
                                      delete_all_numbers: bool = None,
                                      org_id: str = None) -> list[RouteListNumberPatchResponse]:
        """
        Modify Numbers for Route List

        Modify numbers for a specific Route List of a Customer.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: list[RouteListNumberPatch]
        :param delete_all_numbers: If present, the numbers array is ignored and all numbers in the route list are
            deleted.
        :type delete_all_numbers: bool
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: list[RouteListNumberPatchResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if numbers is not None:
            body['numbers'] = TypeAdapter(list[RouteListNumberPatch]).dump_python(numbers, mode='json', by_alias=True, exclude_none=True)
        if delete_all_numbers is not None:
            body['deleteAllNumbers'] = delete_all_numbers
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        data = super().put(url, params=params, json=body)
        r = TypeAdapter(list[RouteListNumberPatchResponse]).validate_python(data['numberStatus'])
        return r

    def read_the_list_of_trunks(self, name: list[str] = None, location_name: list[str] = None, trunk_type: str = None,
                                order: str = None, org_id: str = None, **params) -> Generator[Trunk, None, None]:
        """
        Read the List of Trunks

        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: list[str]
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: list[str]
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields.  Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id: List trunks for this organization.
        :type org_id: str
        :return: Generator yielding :class:`Trunk` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = ','.join(name)
        if location_name is not None:
            params['locationName'] = ','.join(location_name)
        if trunk_type is not None:
            params['trunkType'] = trunk_type
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/trunks')
        return self.session.follow_pagination(url=url, model=Trunk, item_key='trunks', params=params)

    def create_a_trunk(self, name: str, location_id: str, password: str, trunk_type: TrunkType,
                       dual_identity_support_enabled: bool = None, device_type: str = None, address: str = None,
                       domain: str = None, port: int = None, max_concurrent_calls: int = None,
                       p_charge_info_support_policy: PChargeInfoSupportPolicyType = None, org_id: str = None) -> str:
        """
        Create a Trunk

        Create a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Creating a trunk requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param name: A unique name for the trunk.
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: TrunkType
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header and
            P-Asserted-Identity header when sending an initial SIP `INVITE` to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param device_type: Device type assosiated with trunk.
        :type device_type: str
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :type p_charge_info_support_policy: PChargeInfoSupportPolicyType
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['locationId'] = location_id
        body['password'] = password
        if dual_identity_support_enabled is not None:
            body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        body['trunkType'] = enum_str(trunk_type)
        if device_type is not None:
            body['deviceType'] = device_type
        if address is not None:
            body['address'] = address
        if domain is not None:
            body['domain'] = domain
        if port is not None:
            body['port'] = port
        if max_concurrent_calls is not None:
            body['maxConcurrentCalls'] = max_concurrent_calls
        if p_charge_info_support_policy is not None:
            body['pChargeInfoSupportPolicy'] = enum_str(p_charge_info_support_policy)
        url = self.ep('premisePstn/trunks')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def validate_local_gateway_fqdn_and_domain_for_a_trunk(self, address: str = None, domain: str = None,
                                                           port: int = None, org_id: str = None):
        """
        Validate Local Gateway FQDN and Domain for a Trunk

        Validate Local Gateway FQDN and Domain for the organization trunks.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.

        Validating Local Gateway FQDN and Domain requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param address: FQDN or SRV address of the trunk.
        :type address: str
        :param domain: Domain name of the trunk.
        :type domain: str
        :param port: FQDN port of the trunk.
        :type port: int
        :param org_id: Organization to which trunk types belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if address is not None:
            body['address'] = address
        if domain is not None:
            body['domain'] = domain
        if port is not None:
            body['port'] = port
        url = self.ep('premisePstn/trunks/actions/fqdnValidation/invoke')
        super().post(url, params=params, json=body)

    def read_the_list_of_trunk_types(self, org_id: str = None) -> list[TrunkTypeWithDeviceType]:
        """
        Read the List of Trunk Types

        List all Trunk Types with Device Types for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy. Trunk Types are Registering or Certificate Based and are
        configured in Call Manager.

        Retrieving trunk types requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Organization to which the trunk types belong.
        :type org_id: str
        :rtype: list[TrunkTypeWithDeviceType]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('premisePstn/trunks/trunkTypes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[TrunkTypeWithDeviceType]).validate_python(data['trunkTypes'])
        return r

    def delete_a_trunk(self, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk

        Delete a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.

        Deleting a trunk requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().delete(url, params=params)

    def get_a_trunk(self, trunk_id: str, org_id: str = None) -> TrunkGet:
        """
        Get a Trunk

        Get a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.

        Retrieving a trunk requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :rtype: :class:`TrunkGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        data = super().get(url, params=params)
        r = TrunkGet.model_validate(data)
        return r

    def modify_a_trunk(self, trunk_id: str, name: str, password: str, dual_identity_support_enabled: bool = None,
                       max_concurrent_calls: int = None,
                       p_charge_info_support_policy: PChargeInfoSupportPolicyType = None, org_id: str = None):
        """
        Modify a Trunk

        Modify a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.

        Modifying a trunk requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param trunk_id: ID of the trunk being modified.
        :type trunk_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param password: A password to use on the trunk.
        :type password: str
        :param dual_identity_support_enabled: Determines the behavior of the From and PAI headers on outbound calls.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate-based trunk.
        :type max_concurrent_calls: int
        :type p_charge_info_support_policy: PChargeInfoSupportPolicyType
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['password'] = password
        if dual_identity_support_enabled is not None:
            body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        if max_concurrent_calls is not None:
            body['maxConcurrentCalls'] = max_concurrent_calls
        if p_charge_info_support_policy is not None:
            body['pChargeInfoSupportPolicy'] = enum_str(p_charge_info_support_policy)
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().put(url, params=params, json=body)

    def get_local_gateway_usage_count(self, trunk_id: str, org_id: str = None) -> LocalGatewayUsageCount:
        """
        Get Local Gateway Usage Count

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :rtype: :class:`LocalGatewayUsageCount`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usage')
        data = super().get(url, params=params)
        r = LocalGatewayUsageCount.model_validate(data)
        return r

    def get_local_gateway_call_to_on_premises_extension_usage_for_a_trunk(self, trunk_id: str, order: str = None,
                                                                          name: list[str] = None, org_id: str = None,
                                                                          **params) -> Generator[Customer, None, None]:
        """
        Get local gateway call to on-premises extension usage for a trunk.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param order: Order the trunks according to the designated fields.  Available sort fields are `name`, and
            `locationName`. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: list[str]
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = ','.join(name)
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageCallToExtension')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def get_local_gateway_dial_plan_usage_for_a_trunk(self, trunk_id: str, order: str = None, name: list[str] = None,
                                                      org_id: str = None,
                                                      **params) -> Generator[Customer, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param order: Order the trunks according to the designated fields.  Available sort fields are `name`, and
            `locationName`. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: list[str]
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = ','.join(name)
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Customer, item_key='dialPlans', params=params)

    def get_locations_using_the_local_gateway_as_pstn_connection_routing(self, trunk_id: str,
                                                                         org_id: str = None) -> list[Customer]:
        """
        Get Locations Using the Local Gateway as PSTN Connection Routing.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :rtype: list[Customer]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usagePstnConnection')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Customer]).validate_python(data['locations'])
        return r

    def get_route_groups_using_the_local_gateway(self, trunk_id: str, org_id: str = None) -> list[RouteGroup]:
        """
        Get Route Groups Using the Local Gateway.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :rtype: list[RouteGroup]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageRouteGroup')
        data = super().get(url, params=params)
        r = TypeAdapter(list[RouteGroup]).validate_python(data['routeGroup'])
        return r
