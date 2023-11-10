from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActionOnRouteList', 'CallSourceInfo', 'CallSourceType', 'Customer', 'DestinationType', 'DeviceStatus',
            'DeviceType', 'DialPattern', 'DialPatternPut', 'DialPatternStatus', 'DialPatternValidate',
            'DialPatternValidateResult', 'DialPatternValidationStatus', 'DialPlan', 'DialPlanGet', 'DialPlanPost',
            'DialPlanPut', 'Emergency', 'FeatureAccessCode', 'GetLocalGatewayDialPlanUsageForATrunkResponse',
            'GetLocationsUsingTheLocalGatewayAsPstnConnectionRoutingResponse',
            'GetRouteGroupsUsingTheLocalGatewayResponse', 'HostedAgent', 'HostedAgentType', 'HostedFeature',
            'LocalGatewayUsageCount', 'LocalGateways', 'ModifyNumbersForRouteListResponse', 'NumberStatus',
            'OriginatorType', 'PbxUser', 'PostResponse', 'PstnNumber', 'ReadTheListOfDialPlansResponse',
            'ReadTheListOfRouteListsResponse', 'ReadTheListOfRoutingGroupsResponse', 'ReadTheListOfTrunksResponse',
            'ReadTheRouteListsOfARoutingGroupResponse', 'ReadTheUsageOfARoutingGroupResponse', 'ResponseStatus',
            'ResponseStatusType', 'RouteGroup', 'RouteGroupGet', 'RouteGroupPatch', 'RouteGroupUsageRouteListGet',
            'RouteGroupUsageRouteListItem', 'RouteList', 'RouteListGet', 'RouteListNumberListGet',
            'RouteListNumberPatch', 'RouteListNumberPatchResponse', 'RouteListPatch', 'RouteListPost', 'RouteType',
            'ServiceType', 'TestCallRoutingPostResponse', 'Trunk', 'TrunkFQDNValidatePost', 'TrunkGet',
            'TrunkGetOutboundProxy', 'TrunkPost', 'TrunkPut', 'TrunkType', 'TrunkTypeGetList',
            'TrunkTypeWithDeviceType', 'VirtualExtension', 'VirtualExtensionRange']


class ActionOnRouteList(str, Enum):
    #: Add a phone number to the Route List.
    add = 'ADD'
    #: Delete a phone number from the Route List.
    delete = 'DELETE'


class CallSourceType(str, Enum):
    #: Indicates that the call source is a route list.
    route_list = 'ROUTE_LIST'
    #: Indicates that the call source is a dial pattern.
    dial_pattern = 'DIAL_PATTERN'
    #: Indicates that the call source extension is unknown.
    unkown_extension = 'UNKOWN_EXTENSION'
    #: Indicates that the call source phone number is unknown.
    unkown_number = 'UNKOWN_NUMBER'


class CallSourceInfo(ApiModel):
    #: The type of call source.
    call_source_type: Optional[CallSourceType] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk, this trunk belongs to a route group which is
    #: assigned to a route list with the name routeListA and `originatorNumber` is a number assigned to routeListA.
    #: routeListA is returned here. This element is returned when `callSourceType` is `ROUTE_LIST`.
    #: example: routeList1
    route_list_name: Optional[str] = None
    #: Foute list ID.
    #: example: NTJiZmUxNDAtYjIwMS00NTUzLWI1OGQtMmVkNDU1NTFmYTUy
    route_list_id: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with name trunkA, trunkA belongs to a route
    #: group which is assigned to a route list with name routeListA,  trunkA is also assigned to dialPlanA as routing
    #: choice, dialPlanA has dialPattern xxxx assigned. If the `originatorNumber` matches the `dialPattern` `xxxx`,
    #: dialPlanA is returned. This element is returned when `callSourceType` is `DIAL_PATTERN`.
    #: example: dialPlan1
    dial_plan_name: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with the name trunkA, trunkA belongs to a
    #: route group which is assigned to a route list with the name routeListA,  trunkA is also assigned to dialPlanA
    #: as routing choice, dialPlanA has `dialPattern` `xxxx` assigned. If the `originatorNumber` matches the
    #: `dialPattern` `xxxx`, `dialPattern` `xxxx` is returned. This element is returned when `callSourceType` is
    #: `DIAL_PATTERN`.
    #: example: *888
    dial_pattern: Optional[str] = None
    #: Dial plan ID.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    dial_plan_id: Optional[str] = None


class Customer(ApiModel):
    #: ID of the customer/organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Name of the customer/organization.
    #: example: test_org
    name: Optional[str] = None


class DestinationType(str, Enum):
    #: Matching destination is a person or workspace with details in the `hostedAgent` field.
    hosted_agent = 'HOSTED_AGENT'
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the `hostedFeature`
    #: field.
    hosted_feature = 'HOSTED_FEATURE'
    #: Matching destination routes into a separate PBX with details in the `pbxUser` field.
    pbx_user = 'PBX_USER'
    #: Matching destination routes into a PSTN phone number with details in the `pstnNumber` field.
    pstn_number = 'PSTN_NUMBER'
    #: Matching destination routes into a virtual extension with details in the `virtualExtension` field.
    virtual_extension = 'VIRTUAL_EXTENSION'
    #: Matching destination routes into a virtual extension range with details in the `virtualExtensionRange` field.
    virtual_extension_range = 'VIRTUAL_EXTENSION_RANGE'
    #: Matching destination routes into a route list with details in the `routeList` field.
    route_list = 'ROUTE_LIST'
    #: Matching destination routes into a feature access code (FAC) with details in the `featureAccessCode` field.
    fac = 'FAC'
    #: Matching destination routes into an emergency service like Red Sky, with details in the `emergency` field.
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
    #: example: Cisco Unified Border Element
    device_type: Optional[str] = None
    #: Minimum number of concurrent calls. Required for static certificate based trunk.
    #: example: 250
    min_concurrent_calls: Optional[int] = None
    #: Maximum number of concurrent calls. Required for static certificate based trunk.
    #: example: 1000
    max_concurrent_calls: Optional[int] = None


class DialPattern(ApiModel):
    #: A unique dial pattern.
    #: example: +5555
    dial_pattern: Optional[str] = None
    #: Action to add or delete a pattern.
    action: Optional[ActionOnRouteList] = None


class DialPatternPut(ApiModel):
    #: Array of dial patterns to add or delete. Dial Pattern that is not present in the request is not modified.
    dial_patterns: Optional[list[DialPattern]] = None
    #: Delete all the dial patterns for a dial plan.
    #: example: True
    delete_all_dial_patterns: Optional[bool] = None


class DialPatternStatus(str, Enum):
    #: Invalid pattern
    invalid = 'INVALID'
    #: Duplicate pattern
    duplicate = 'DUPLICATE'
    #: Duplicate in input
    duplicate_in_list = 'DUPLICATE_IN_LIST'


class DialPatternValidate(ApiModel):
    #: Input dial pattern that is being validated.
    #: example: +4555
    dial_pattern: Optional[str] = None
    #: Validation status.
    pattern_status: Optional[DialPatternStatus] = None
    #: Failure details.
    #: example: invalid format for premises dial pattern +4555
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
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    id: Optional[str] = None
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    route_id: Optional[str] = None
    #: Name of route type associated with the dial plan.
    #: example: routeName
    route_name: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None


class DialPlanGet(ApiModel):
    #: Unique identifier for the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    id: Optional[str] = None
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    route_id: Optional[str] = None
    #: Name of route type associated with the dial plan.
    #: example: routeName
    route_name: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None
    #: Customer information.
    customer: Optional[Customer] = None


class DialPlanPost(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    route_id: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None
    #: An Array of dial patterns.
    #: example: ['+5555,+5556']
    dial_patterns: Optional[list[str]] = None


class DialPlanPut(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    route_id: Optional[str] = None
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType] = None


class Emergency(ApiModel):
    #: Indicates if RedSky is in use.
    is_red_sky: Optional[bool] = None
    #: Trunk name.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Trunk id.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunk_id: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunk_location_id: Optional[str] = None


class FeatureAccessCode(ApiModel):
    #: FAC code.
    #: example: *70
    code: Optional[str] = None
    #: FAC name.
    #: example: Cancel Call Waiting
    name: Optional[str] = None


class HostedAgentType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'


class HostedAgent(ApiModel):
    #: Person or workspace's ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mMjU4YjhmZi1lODIxLTQ3MDktYTI2My1mMmI4OWZjN2FlYmQ
    id: Optional[str] = None
    #: Type of agent for call destination.
    type: Optional[HostedAgentType] = None
    #: Person or workspace's first name.
    #: example: firstName
    first_name: Optional[str] = None
    #: Person or workspace's last name.
    #: example: lastName
    last_name: Optional[str] = None
    #: Name of location for a person or workspace.
    #: example: locationName
    location_name: Optional[str] = None
    #: Location ID for a person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL1dLQVBRMjQ4NDczTDI0ODQ3NA
    location_id: Optional[str] = None
    #: Person or workspace's phone number.
    #: example: 9874531287
    phone_number: Optional[str] = None
    #: Person or workspace's extension.
    #: example: 111
    extension: Optional[datetime] = None


class ServiceType(str, Enum):
    #: Destination is an auto attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: Indicates that this destination is the Office (Broadworks) Anywhere feature.
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    #: Indicates that this destination is the Call Center feature.
    call_center = 'CALL_CENTER'
    #: Indicates that this destination is the Contact Center Link feature.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: Indicates that this destination is the Group Paging feature.
    group_paging = 'GROUP_PAGING'
    #: Indicates that this destination is the Hunt Group feature.
    hunt_group = 'HUNT_GROUP'
    #: Indicates that this destination is the Voice Messaging feature.
    voice_messaging = 'VOICE_MESSAGING'
    #: Indicates that this destination is the Voice Mail Group feature.
    voice_mail_group = 'VOICE_MAIL_GROUP'


class HostedFeature(ApiModel):
    #: Service instance type.
    type: Optional[ServiceType] = None
    #: Service instance name.
    #: example: name1
    name: Optional[str] = None
    #: Service instance ID.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    id: Optional[str] = None
    #: Location of the service instance.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID of the service instance.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    location_id: Optional[str] = None
    #: User or place's phone number.
    #: example: 9874531287
    phone_number: Optional[str] = None
    #: User or place's extension.
    #: example: 111
    extension: Optional[datetime] = None


class LocalGatewayUsageCount(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    #: example: 1
    pstn_connection_count: Optional[int] = None
    #: The count where the given local gateway is used as call to extension setting.
    #: example: 1
    call_to_extension_count: Optional[int] = None
    #: The count where the given local gateway is used by the dial plan.
    #: example: 1
    dial_plan_count: Optional[int] = None
    #: The count where the given local gateway is used by the route group.
    #: example: 1
    route_group_count: Optional[int] = None


class LocalGateways(ApiModel):
    #: ID of type local gateway.
    #: example: 'Y2lzY29zcGFyazovL3VzL1RSVU5LLzY1Zjc4YzgxLTcwMTYtNDc0Ny05M2EyLWIxMGVlZjBhMWI1Ng'
    id: Optional[str] = None
    #: Name of the local gateway.
    #: example: 'localGatewayName'
    name: Optional[str] = None
    #: Location ID to which local gateway belongs.
    #: example: 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL1dTV1laMjEyODA2TDIxMjgwNw'
    location_id: Optional[str] = None
    #: Prioritizes local gateways based on these numbers; the lowest number gets the highest priority.
    #: example: 1
    priority: Optional[int] = None


class NumberStatus(str, Enum):
    invalid = 'INVALID'
    duplicate = 'DUPLICATE'
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    unavailable = 'UNAVAILABLE'


class OriginatorType(str, Enum):
    #: User
    user = 'USER'
    #: Connection between Webex Calling and the premises
    trunk = 'TRUNK'


class PbxUser(ApiModel):
    #: Dial plan name that the called string matches.
    #: example: dialPlan1
    dial_plan_name: Optional[str] = None
    #: Dial plan ID.
    #: example: NTZhMmQzZDktZDVhMC00NWQzLWE3NWYtNjY4NDA4Yzc0OWRk
    dial_plan_id: Optional[str] = None
    #: Dial pattern that the called string matches.
    #: example: 442xxx
    dial_pattern: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunk_id: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunk_location_id: Optional[str] = None


class PostResponse(ApiModel):
    #: ID of the Route Group.
    #: example: 'Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzE4YzFhMGRkLWJhMjctNDkwMS1hNGUxLTBlNWIyNzM1YzlkZg'
    id: Optional[str] = None


class PstnNumber(ApiModel):
    #: Trunk name.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunk_id: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunk_location_id: Optional[str] = None


class ResponseStatusType(str, Enum):
    #: Error
    error = 'ERROR'
    #: Warning
    warning = 'WARNING'


class ResponseStatus(ApiModel):
    #: Error Code. 25013 for error retrieving the outbound proxy. 25014 for error retrieving the status
    #: example: 25013
    code: Optional[int] = None
    #: Status type.
    type: Optional[ResponseStatusType] = None
    #: Error summary in English.
    #: example: CPAPI: Error retrieving outboundproxy.
    summary_english: Optional[str] = None
    #: Error Details.
    #: example: ['OCI-P GroupOutboundProxyGetRequest: [Error 26088] Cloud PBX Console is not configured properly., OCI-P Error code: [Error 26088] Cloud PBX Console is not configured properly.']
    detail: Optional[list[str]] = None
    #: Error Tracking ID.
    #: example: CPAPI_2da34568-1e72-4196-b613-905ce45ec592_0
    tracking_id: Optional[str] = None


class RouteGroup(ApiModel):
    #: Route group ID the Route list is associated with.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2ZjN2EzZDU2LTg1OGMtNDVkZC1iZDA1LTE2OWM2NGU1OTRmMQ
    id: Optional[str] = None
    #: Name of the Route group the Route list associated with.
    #: example: Route Group 01
    name: Optional[str] = None
    #: Flag to indicate if the route group is used.
    #: example: True
    in_use: Optional[bool] = None


class RouteGroupGet(ApiModel):
    #: Name of the route group.
    #: example: 'Route Group One'
    name: Optional[str] = None
    #: Organization details.
    organization: Optional[Customer] = None
    #: Local Gateways that are part of this Route Group.
    local_gateways: Optional[list[LocalGateways]] = None


class RouteGroupPatch(ApiModel):
    #: A unique name for the Route Group.
    #: example: routeGroupName
    name: Optional[str] = None
    #: Local Gateways that are part of this Route Group.
    local_gateways: Optional[list[LocalGateways]] = None


class RouteGroupUsageRouteListItem(ApiModel):
    #: Route list ID.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0xJU1QvOTljNjJkMGQtNmFhYi00NGQ0LWE0ZTctZjk0MjQ4OWVhMWJj
    id: Optional[str] = None
    #: Route list name.
    #: example: routeListName
    name: Optional[str] = None
    #: Location ID for route list.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2JjNWUwNWFjLTI5ZmEtNGY0NS05MmM1LWUxZTExMDc0OTIwZg
    location_id: Optional[str] = None
    #: Location name for route list.
    #: example: locationName
    location_name: Optional[str] = None


class RouteGroupUsageRouteListGet(ApiModel):
    #: List of route lists for this route group.
    route_lists: Optional[list[RouteGroupUsageRouteListItem]] = None


class RouteList(ApiModel):
    #: Route list ID.
    #: example: ODRkYmVmMjItYTEwNC00YWZhLTg4ODMtY2QzNjhiMTAxOWZl
    id: Optional[str] = None
    #: Route list name.
    #: example: routeListName1
    name: Optional[str] = None
    #: Name of the route group the route list is associated with.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: ID of the route group the route list is associated with.
    #: example: MjRlNDQwYTUtNzQ5NC00ODg2LWIyNTktMmFiM2I2M2ZiMGY0
    route_group_id: Optional[str] = None
    #: Location name of the route list.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID of the route list.
    #: example: NjY5YmY3ODQtNjMyZS00MTA2LWFmMWItMzYxYWNkY2M1OTFh
    location_id: Optional[str] = None


class RouteListGet(ApiModel):
    #: Route list name.
    #: example: Route List 01
    name: Optional[str] = None
    #: Location associated with the Route List.
    location: Optional[Customer] = None
    #: Route group associated with the Route list.
    route_group: Optional[RouteGroup] = None


class RouteListNumberListGet(ApiModel):
    #: Numbers assigned to the Route list.
    numbers: Optional[list[str]] = None


class RouteListNumberPatch(ApiModel):
    #: Number to be deleted/added.
    #: example: +2147891122
    number: Optional[str] = None
    #: Possible value, `ADD` or `DELETE`.
    #: example: DELETE
    action: Optional[ActionOnRouteList] = None


class RouteListNumberPatchResponse(ApiModel):
    #: Phone Number whose status is being reported.
    #: example: +2147891122
    phone_number: Optional[str] = None
    #: Status of the number. Possible values are `INVALID`, `DUPLICATE`, `DUPLICATE_IN_LIST`, or `UNAVAILABLE`.
    #: example: DUPLICATE
    number_status: Optional[NumberStatus] = None
    #: Message of the number add status.
    #: example: Invalid Number
    message: Optional[str] = None


class RouteListPatch(ApiModel):
    #: Route List new name.
    #: example: New Route List
    name: Optional[str] = None
    #: New route group ID.
    #: example: NTJiZmUxNDAtYjIwMS00NTUzLWI1OGQtMmVkNDU1NTFmYTUy
    route_group_id: Optional[str] = None


class RouteListPost(ApiModel):
    #: Name of the Route List
    #: example: RouteList01
    name: Optional[str] = None
    #: Location associated with the Route List.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2JjNWUwNWFjLTI5ZmEtNGY0NS05MmM1LWUxZTExMDc0OTIwZg
    location_id: Optional[str] = None
    #: ID of the route group associated with Route List.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2ZjN2EzZDU2LTg1OGMtNDVkZC1iZDA1LTE2OWM2NGU1OTRmMQ
    route_group_id: Optional[str] = None


class VirtualExtension(ApiModel):
    #: Virtual extension ID.
    #: example: OTI0NzM1OTQtZGU1Mi00ZjViLTk0YjItN2Y5MzRmY2Y2NDk3
    id: Optional[str] = None
    #: Virtual extension display first name.
    #: example: firstName1
    first_name: Optional[str] = None
    #: Virtual extension display last name.
    #: example: lastName1
    last_name: Optional[str] = None
    #: Virtual extension display name.
    #: example: displayName1
    display_name: Optional[str] = None
    #: Extension that the virtual extension is associated with.
    #: example: 0007
    extension: Optional[datetime] = None
    #: Phone number that the virtual extension is associated with.
    #: example: 8701278963
    phone_number: Optional[str] = None
    #: Location name if the virtual extension is at the location level, empty if it is at customer level.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID if the virtual extension is at the location level, empty if it is at customer level.
    #: example: MWU5ZmEzZmEtYTQ0ZS00MDJhLWExNDItMjJmODQxMjhkOTY4
    location_id: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunk_id: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunk_location_id: Optional[str] = None


class VirtualExtensionRange(ApiModel):
    #: Virtual extension range ID.
    #: example: OTI0NzM1OTQtZGU1Mi00ZjViLTk0YjItN2Y5MzRmY2Y2NDk3
    id: Optional[str] = None
    #: Virtual extension range name.
    #: example: firstName1
    name: Optional[str] = None
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix;
    #: BCD/Enhanced mode can have any valid prefix).
    #: example: +1214555
    prefix: Optional[str] = None
    #: Pattern associated with the virtual extension range.
    #: example: 2XXX
    pattern: Optional[str] = None
    #: Location name if the virtual extension range is at the location level, empty if it is at customer level.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID if the virtual extension range is at the location level, empty if it is at customer level.
    #: example: MWU5ZmEzZmEtYTQ0ZS00MDJhLWExNDItMjJmODQxMjhkOTY4
    location_id: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunk_id: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunk_location_id: Optional[str] = None


class TestCallRoutingPostResponse(ApiModel):
    #: Only returned when `originatorNumber` is specified in the request.
    call_source_info: Optional[CallSourceInfo] = None
    #: Matching destination type for the call.
    destination_type: Optional[DestinationType] = None
    #: FAC code if `destinationType` is FAC. The routing address will be returned for all other destination types.
    #: example: 007
    routing_address: Optional[datetime] = None
    #: Outside access code.
    #: example: 1234
    outside_access_code: Optional[datetime] = None
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


class TrunkType(str, Enum):
    #: For Cisco CUBE Local Gateway.
    registering = 'REGISTERING'
    #: For Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller,
    #: Ribbon Session Border Controller.
    certificate_based = 'CERTIFICATE_BASED'


class Trunk(ApiModel):
    #: Unique identifier for the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    id: Optional[str] = None
    #: A unique name for the trunk.
    #: example: trunkName
    name: Optional[str] = None
    #: Location associated with the trunk.
    location: Optional[Customer] = None
    #: Trunk in use flag.
    #: example: True
    in_use: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None


class TrunkFQDNValidatePost(ApiModel):
    #: FQDN or SRV address of the trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name of the trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port of the trunk.
    #: example: 5000
    port: Optional[int] = None


class TrunkGetOutboundProxy(ApiModel):
    ...


class TrunkGet(ApiModel):
    #: A unique name for the trunk.
    #: example: trunkName
    name: Optional[str] = None
    #: Customer associated with the trunk.
    customer: Optional[Customer] = None
    #: Location associated with the trunk.
    location: Optional[Customer] = None
    #: Unique Outgoing and Destination trunk group associated with the dial plan.
    #: example: lg1_sias10_cpapi12446_lgu
    otg_dtg_id: Optional[str] = None
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    #: example: lg1_sias10_cpapi16004_LGU@64941297.int10.bcld.webex.com
    line_port: Optional[str] = None
    #: Locations using trunk.
    locations_using_trunk: Optional[list[Customer]] = None
    #: User ID.
    #: example: lg1_sias10_cpapi12446_LGU@64941297.int10.bcld.webex.com
    pilot_user_id: Optional[str] = None
    #: Contains the body of the HTTP response received following the request to Console API and will not be set if the
    #: response has no body.
    outbound_proxy: Optional[TrunkGetOutboundProxy] = None
    #: User's authentication service information.
    #: example: lg1_sias10_cpapi12446_LGU
    sip_authentication_user_name: Optional[str] = None
    #: Device status.
    status: Optional[DeviceStatus] = None
    #: Error codes.
    #: example: ['errorCodes']
    error_codes: Optional[list[str]] = None
    #: Present partial error/warning status information included when the http response is 206.
    response_status: Optional[ResponseStatus] = None
    #: Determines the behavior of the From and PAI headers on outbound calls.
    #: example: True
    dual_identity_support_enabled: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Device type assosiated with trunk.
    #: example: Cisco Unified Border Element
    device_type: Optional[str] = None
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name. Required to create a static certificate based trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port. Required to create a static certificate-based trunk.
    #: example: 5000
    port: Optional[int] = None
    #: Max Concurrent call. Required to create a static certificate based trunk.
    #: example: 1000
    max_concurrent_calls: Optional[int] = None


class TrunkPost(ApiModel):
    #: A unique name for the trunk.
    #: example: trunkName
    name: Optional[str] = None
    #: ID of location associated with the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    location_id: Optional[str] = None
    #: A password to use on the trunk.
    #: example: password
    password: Optional[str] = None
    #: Dual Identity Support setting impacts the handling of the From header and P-Asserted-Identity header when
    #: sending an initial SIP `INVITE` to the trunk for an outbound call.
    #: example: True
    dual_identity_support_enabled: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Device type assosiated with trunk.
    #: example: Cisco Unified Border Element
    device_type: Optional[str] = None
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name. Required to create a static certificate based trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port. Required to create a static certificate-based trunk.
    #: example: 5000
    port: Optional[int] = None
    #: Max Concurrent call. Required to create a static certificate based trunk.
    #: example: 1000
    max_concurrent_calls: Optional[int] = None


class TrunkPut(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: A password to use on the trunk.
    #: example: password
    password: Optional[str] = None
    #: Determines the behavior of the From and PAI headers on outbound calls.
    #: example: True
    dual_identity_support_enabled: Optional[bool] = None
    #: Max Concurrent call. Required to create a static certificate-based trunk.
    #: example: 1000
    max_concurrent_calls: Optional[int] = None


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType] = None
    #: Device types for trunk configuration.
    device_types: Optional[list[DeviceType]] = None


class TrunkTypeGetList(ApiModel):
    #: Trunk type with device types.
    trunk_types: Optional[list[TrunkTypeWithDeviceType]] = None


class GetLocalGatewayDialPlanUsageForATrunkResponse(ApiModel):
    #: Array of dial Plans.
    dial_plans: Optional[list[Customer]] = None


class GetLocationsUsingTheLocalGatewayAsPstnConnectionRoutingResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[Customer]] = None


class GetRouteGroupsUsingTheLocalGatewayResponse(ApiModel):
    #: Array of route Groups.
    route_group: Optional[list[RouteGroup]] = None


class ReadTheListOfDialPlansResponse(ApiModel):
    #: Array of dial plans.
    dial_plans: Optional[list[DialPlan]] = None


class ReadTheListOfTrunksResponse(ApiModel):
    #: Array of trunks.
    trunks: Optional[list[Trunk]] = None


class ReadTheListOfRoutingGroupsResponse(ApiModel):
    #: Array of route groups.
    route_groups: Optional[list[RouteGroup]] = None


class ReadTheUsageOfARoutingGroupResponse(ApiModel):
    #: Number of PSTN connection locations associated to this route group.
    #: example: 1
    pstn_connection_count: Optional[datetime] = None
    #: Number of call to extension locations associated to this route group.
    #: example: 1
    call_to_extension_count: Optional[datetime] = None
    #: Number of dial plan locations associated to this route group.
    #: example: 1
    dial_plan_count: Optional[datetime] = None
    #: Number of route list locations associated to this route group.
    #: example: 1
    route_list_count: Optional[datetime] = None


class ReadTheRouteListsOfARoutingGroupResponse(ApiModel):
    #: Array of route lists.
    route_group_usage_route_list_get: Optional[list[RouteGroupUsageRouteListGet]] = None


class ReadTheListOfRouteListsResponse(ApiModel):
    #: Array of route lists.
    route_lists: Optional[list[RouteList]] = None


class ModifyNumbersForRouteListResponse(ApiModel):
    #: Array of number statuses.
    number_status: Optional[list[RouteListNumberPatchResponse]] = None


class CallRoutingApi(ApiChild, base='telephony/config'):
    """
    Call Routing
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Call Routing supports reading and writing of Webex Calling On-premises, also known as Local Gateway, Call
    Routing PSTN settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def test_call_routing(self, originator_id: str, originator_type: OriginatorType, destination: Union[str, datetime],
                          originator_number: str = None, org_id: str = None) -> TestCallRoutingPostResponse:
        """
        Test Call Routing

        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Test call routing requires a full or write-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param originator_id: This element is used to identify the originating party.  It can be user UUID or trunk
            UUID.
        :type originator_id: str
        :param originator_type: `USER` or `TRUNK`.
        :type originator_type: OriginatorType
        :param destination: This element specifies called party.  It can be any dialable string, for example, an ESN
            number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: Union[str, datetime]
        :param originator_number: Only used when originatorType is `TRUNK`. This element could be a phone number or
            URI.
        :type originator_number: str
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
        body['originatorNumber'] = originator_number
        body['destination'] = destination
        url = self.ep('actions/testCallRouting/invoke')
        data = super().post(url, params=params, json=body)
        r = TestCallRoutingPostResponse.model_validate(data)
        return r

    def get_local_gateway_dial_plan_usage_for_a_trunk(self, trunk_id: str, start: int = None, order: str = None,
                                                      name: list[str] = None, org_id: str = None,
                                                      **params) -> Generator[Customer, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk

        Get Local Gateway Dial Plan Usage for a Trunk.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = ','.join(name)
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Customer, item_key='dialPlans', params=params)

    def get_locations_using_the_local_gateway_as_pstn_connection_routing(self, trunk_id: str,
                                                                         org_id: str = None) -> list[Customer]:
        """
        Get Locations Using the Local Gateway as PSTN Connection Routing

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
        Get Route Groups Using the Local Gateway

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

    def get_local_gateway_usage_count(self, trunk_id: str, org_id: str = None) -> LocalGatewayUsageCount:
        """
        Get Local Gateway Usage Count

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

    def modify_dial_patterns(self, dial_plan_id: str, dial_patterns: list[DialPattern], delete_all_dial_patterns: bool,
                             org_id: str = None):
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
        body['dialPatterns'] = loads(TypeAdapter(list[DialPattern]).dump_json(dial_patterns))
        body['deleteAllDialPatterns'] = delete_all_dial_patterns
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        super().put(url, params=params, json=body)

    def validate_a_dial_pattern(self, dial_patterns: list[str], org_id: str = None) -> DialPatternValidateResult:
        """
        Validate a Dial Pattern

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
                                    trunk_name: str = None, start: int = None, order: str = None, org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/dialPlans')
        return self.session.follow_pagination(url=url, model=DialPlan, item_key='dialPlans', params=params)

    def create_a_dial_plan(self, name: str, route_id: str, route_type: RouteType, dial_patterns: list[str],
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
        body['dialPatterns'] = dial_patterns
        url = self.ep('premisePstn/dialPlans')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

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

    def validate_local_gateway_fqdn_and_domain_for_a_trunk(self, address: str, domain: str, port: int,
                                                           org_id: str = None):
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
        body['address'] = address
        body['domain'] = domain
        body['port'] = port
        url = self.ep('premisePstn/trunks/actions/fqdnValidation/invoke')
        super().post(url, params=params, json=body)

    def read_the_list_of_trunks(self, name: list[str] = None, location_name: list[str] = None, trunk_type: str = None,
                                start: int = None, order: str = None, org_id: str = None,
                                **params) -> Generator[Trunk, None, None]:
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/trunks')
        return self.session.follow_pagination(url=url, model=Trunk, item_key='trunks', params=params)

    def create_a_trunk(self, name: str, location_id: str, password: str, dual_identity_support_enabled: bool,
                       trunk_type: TrunkType, device_type: str, address: str, domain: str, port: int,
                       max_concurrent_calls: int, org_id: str = None) -> str:
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
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header and
            P-Asserted-Identity header when sending an initial SIP `INVITE` to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: TrunkType
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
        :param org_id: Organization to which trunk belongs.
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
        body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        body['trunkType'] = enum_str(trunk_type)
        body['deviceType'] = device_type
        body['address'] = address
        body['domain'] = domain
        body['port'] = port
        body['maxConcurrentCalls'] = max_concurrent_calls
        url = self.ep('premisePstn/trunks')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

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

    def modify_a_trunk(self, trunk_id: str, name: str, password: str, dual_identity_support_enabled: bool,
                       max_concurrent_calls: int, org_id: str = None):
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
        body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        body['maxConcurrentCalls'] = max_concurrent_calls
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().put(url, params=params, json=body)

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

    def read_the_list_of_routing_groups(self, name: str = None, start: int = None, order: str = None,
                                        org_id: str = None, **params) -> Generator[RouteGroup, None, None]:
        """
        Read the List of Routing Groups

        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Return the list of route groups matching the Route group name..
        :type name: str
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
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
        body['localGateways'] = loads(TypeAdapter(list[LocalGateways]).dump_json(local_gateways))
        url = self.ep('premisePstn/routeGroups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

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
        body['localGateways'] = loads(TypeAdapter(list[LocalGateways]).dump_json(local_gateways))
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().put(url, params=params, json=body)

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
                                                                start: int = None, order: str = None,
                                                                org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageCallToExtension')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_dial_plan_locations_of_a_routing_group(self, route_group_id: str, location_name: str = None,
                                                        start: int = None, order: str = None, org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_pstn_connection_locations_of_a_routing_group(self, route_group_id: str, location_name: str = None,
                                                              start: int = None, order: str = None,
                                                              org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usagePstnConnection')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)

    def read_the_route_lists_of_a_routing_group(self, route_group_id: str, name: str = None, start: int = None,
                                                order: str = None, org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageRouteList')
        return self.session.follow_pagination(url=url, model=RouteGroupUsageRouteListGet, item_key='routeGroupUsageRouteListGet', params=params)

    def read_the_list_of_route_lists(self, name: list[str] = None, location_id: list[str] = None, start: int = None,
                                     order: str = None, org_id: str = None,
                                     **params) -> Generator[RouteList, None, None]:
        """
        Read the List of Route Lists

        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param name: Return the list of Route List matching the route list name.
        :type name: list[str]
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: list[str]
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the Route List according to the designated fields. Available sort fields are `name`, and
            `locationId`. Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: Generator yielding :class:`RouteList` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = ','.join(name)
        if location_id is not None:
            params['locationId'] = ','.join(location_id)
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
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

    def modify_a_route_list(self, route_list_id: str, name: str, route_group_id: str, org_id: str = None):
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
        body['name'] = name
        body['routeGroupId'] = route_group_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().put(url, params=params, json=body)

    def modify_numbers_for_route_list(self, route_list_id: str, numbers: list[RouteListNumberPatch] = None,
                                      delete_all_numbers: str = None,
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
        :type delete_all_numbers: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :rtype: list[RouteListNumberPatchResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['numbers'] = loads(TypeAdapter(list[RouteListNumberPatch]).dump_json(numbers))
        body['deleteAllNumbers'] = delete_all_numbers
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        data = super().put(url, params=params, json=body)
        r = TypeAdapter(list[RouteListNumberPatchResponse]).validate_python(data['numberStatus'])
        return r

    def get_numbers_assigned_to_a_route_list(self, route_list_id: str, start: int = None, order: str = None,
                                             number: str = None, org_id: str = None,
                                             **params) -> Generator[str, None, None]:
        """
        Get Numbers assigned to a Route List

        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the Route Lists according to number, ascending or descending.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :return: Numbers assigned to the Route list.
        """
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        if number is not None:
            params['number'] = number
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        return self.session.follow_pagination(url=url, model=None, item_key='numbers', params=params)

    def get_local_gateway_call_to_on_premises_extension_usage_for_a_trunk(self, trunk_id: str, start: int = None,
                                                                          order: str = None, name: list[str] = None,
                                                                          org_id: str = None,
                                                                          **params) -> Generator[Customer, None, None]:
        """
        Get Local Gateway Call to On-Premises Extension Usage for a Trunk

        Get local gateway call to on-premises extension usage for a trunk.

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
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
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = ','.join(name)
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageCallToExtension')
        return self.session.follow_pagination(url=url, model=Customer, item_key='locations', params=params)
