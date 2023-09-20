from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActionOnRouteList', 'CallSourceInfo', 'CallSourceType', 'Customer', 'DestinationType', 'DeviceStatus', 'DeviceType', 'DialPattern', 'DialPatternPut', 'DialPatternStatus', 'DialPatternValidate', 'DialPatternValidateResult', 'DialPatternValidationStatus', 'DialPlan', 'DialPlanGet', 'DialPlanPost', 'DialPlanPut', 'Emergency', 'FeatureAccessCode', 'HostedAgent', 'HostedAgentType', 'HostedFeature', 'LocalGatewayUsageCount', 'LocalGateways', 'LocationUsageGetResponse', 'NumberStatus', 'OriginatorType', 'PbxUser', 'PostResponse', 'PstnNumber', 'ResponseStatus', 'ResponseStatusType', 'RouteGroup', 'RouteGroupGet', 'RouteGroupPatch', 'RouteGroupUsageRouteListGet', 'RouteGroupUsageRouteListItem', 'RouteList', 'RouteListGet', 'RouteListNumberListGet', 'RouteListNumberPatch', 'RouteListNumberPatchResponse', 'RouteListPatch', 'RouteListPost', 'RouteType', 'ServiceType', 'TestCallRoutingPostResponse', 'Trunk', 'TrunkFQDNValidatePost', 'TrunkGet', 'TrunkGetOutboundProxy', 'TrunkPost', 'TrunkPut', 'TrunkType', 'TrunkTypeGetList', 'TrunkTypeWithDeviceType', 'VirtualExtension', 'VirtualExtensionRange']


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
    callSourceType: Optional[CallSourceType] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk, this trunk belongs to a route group which is assigned to a route list with the name routeListA and `originatorNumber` is a number assigned to routeListA. routeListA is returned here. This element is returned when `callSourceType` is `ROUTE_LIST`.
    #: example: routeList1
    routeListName: Optional[str] = None
    #: Foute list ID.
    #: example: NTJiZmUxNDAtYjIwMS00NTUzLWI1OGQtMmVkNDU1NTFmYTUy
    routeListId: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with name trunkA, trunkA belongs to a route group which is assigned to a route list with name routeListA,  trunkA is also assigned to dialPlanA as routing choice, dialPlanA has dialPattern xxxx assigned. If the `originatorNumber` matches the `dialPattern` `xxxx`, dialPlanA is returned. This element is returned when `callSourceType` is `DIAL_PATTERN`.
    #: example: dialPlan1
    dialPlanName: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with the name trunkA, trunkA belongs to a route group which is assigned to a route list with the name routeListA,  trunkA is also assigned to dialPlanA as routing choice, dialPlanA has `dialPattern` `xxxx` assigned. If the `originatorNumber` matches the `dialPattern` `xxxx`, `dialPattern` `xxxx` is returned. This element is returned when `callSourceType` is `DIAL_PATTERN`.
    #: example: *888
    dialPattern: Optional[str] = None
    #: Dial plan ID.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    dialPlanId: Optional[str] = None


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
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the `hostedFeature` field.
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
    deviceType: Optional[str] = None
    #: Minimum number of concurrent calls. Required for static certificate based trunk.
    #: example: 250.0
    minConcurrentCalls: Optional[int] = None
    #: Maximum number of concurrent calls. Required for static certificate based trunk.
    #: example: 1000.0
    maxConcurrentCalls: Optional[int] = None


class DialPattern(ApiModel):
    #: A unique dial pattern.
    #: example: +5555
    dialPattern: Optional[str] = None
    #: Action to add or delete a pattern.
    action: Optional[ActionOnRouteList] = None


class DialPatternPut(ApiModel):
    #: Array of dial patterns to add or delete. Dial Pattern that is not present in the request is not modified.
    dialPatterns: Optional[list[DialPattern]] = None
    #: Delete all the dial patterns for a dial plan.
    #: example: True
    deleteAllDialPatterns: Optional[bool] = None


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
    dialPattern: Optional[str] = None
    #: Validation status.
    patternStatus: Optional[DialPatternStatus] = None
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
    dialPatternStatus: Optional[list[DialPatternValidate]] = None


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
    routeId: Optional[str] = None
    #: Name of route type associated with the dial plan.
    #: example: routeName
    routeName: Optional[str] = None
    #: Route Type associated with the dial plan.
    routeType: Optional[RouteType] = None


class DialPlanGet(ApiModel):
    #: Unique identifier for the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    id: Optional[str] = None
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    routeId: Optional[str] = None
    #: Name of route type associated with the dial plan.
    #: example: routeName
    routeName: Optional[str] = None
    #: Route Type associated with the dial plan.
    routeType: Optional[RouteType] = None
    #: Customer information.
    customer: Optional[Customer] = None


class DialPlanPost(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    routeId: Optional[str] = None
    #: Route Type associated with the dial plan.
    routeType: Optional[RouteType] = None
    #: An Array of dial patterns.
    #: example: ['+5555,+5556']
    dialPatterns: Optional[list[str]] = None


class DialPlanPut(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: ID of route type associated with the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    routeId: Optional[str] = None
    #: Route Type associated with the dial plan.
    routeType: Optional[RouteType] = None


class Emergency(ApiModel):
    #: Indicates if RedSky is in use.
    isRedSky: Optional[bool] = None
    #: Trunk name.
    #: example: trunkName1
    trunkName: Optional[str] = None
    #: Trunk id.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunkId: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    routeGroupId: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunkLocationName: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunkLocationId: Optional[str] = None


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
    firstName: Optional[str] = None
    #: Person or workspace's last name.
    #: example: lastName
    lastName: Optional[str] = None
    #: Name of location for a person or workspace.
    #: example: locationName
    locationName: Optional[str] = None
    #: Location ID for a person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL1dLQVBRMjQ4NDczTDI0ODQ3NA
    locationId: Optional[str] = None
    #: Person or workspace's phone number.
    #: example: 9874531287
    phoneNumber: Optional[str] = None
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
    locationName: Optional[str] = None
    #: Location ID of the service instance.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    locationId: Optional[str] = None
    #: User or place's phone number.
    #: example: 9874531287
    phoneNumber: Optional[str] = None
    #: User or place's extension.
    #: example: 111
    extension: Optional[datetime] = None


class LocalGatewayUsageCount(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    #: example: 1.0
    pstnConnectionCount: Optional[int] = None
    #: The count where the given local gateway is used as call to extension setting.
    #: example: 1.0
    callToExtensionCount: Optional[int] = None
    #: The count where the given local gateway is used by the dial plan.
    #: example: 1.0
    dialPlanCount: Optional[int] = None
    #: The count where the given local gateway is used by the route group.
    #: example: 1.0
    routeGroupCount: Optional[int] = None


class LocalGateways(ApiModel):
    #: ID of type local gateway.
    #: example: 'Y2lzY29zcGFyazovL3VzL1RSVU5LLzY1Zjc4YzgxLTcwMTYtNDc0Ny05M2EyLWIxMGVlZjBhMWI1Ng'
    id: Optional[str] = None
    #: Name of the local gateway.
    #: example: 'localGatewayName'
    name: Optional[str] = None
    #: Location ID to which local gateway belongs.
    #: example: 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL1dTV1laMjEyODA2TDIxMjgwNw'
    locationId: Optional[str] = None
    #: Prioritizes local gateways based on these numbers; the lowest number gets the highest priority.
    #: example: 1.0
    priority: Optional[int] = None


class LocationUsageGetResponse(ApiModel):
    #: Location associated with the trunk.
    location: Optional[Customer] = None


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
    dialPlanName: Optional[str] = None
    #: Dial plan ID.
    #: example: NTZhMmQzZDktZDVhMC00NWQzLWE3NWYtNjY4NDA4Yzc0OWRk
    dialPlanId: Optional[str] = None
    #: Dial pattern that the called string matches.
    #: example: 442xxx
    dialPattern: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunkName: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunkId: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    routeGroupId: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunkLocationName: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunkLocationId: Optional[str] = None


class PostResponse(ApiModel):
    #: ID of the Route Group.
    #: example: 'Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzE4YzFhMGRkLWJhMjctNDkwMS1hNGUxLTBlNWIyNzM1YzlkZg'
    id: Optional[str] = None


class PstnNumber(ApiModel):
    #: Trunk name.
    #: example: trunkName1
    trunkName: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunkId: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    routeGroupId: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunkLocationName: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunkLocationId: Optional[str] = None


class ResponseStatusType(str, Enum):
    #: Error
    error = 'ERROR'
    #: Warning
    warning = 'WARNING'


class ResponseStatus(ApiModel):
    #: Error Code. 25013 for error retrieving the outbound proxy. 25014 for error retrieving the status
    #: example: 25013.0
    code: Optional[int] = None
    #: Status type.
    type: Optional[ResponseStatusType] = None
    #: Error summary in English.
    #: example: CPAPI: Error retrieving outboundproxy.
    summaryEnglish: Optional[str] = None
    #: Error Details.
    #: example: ['OCI-P GroupOutboundProxyGetRequest: [Error 26088] Cloud PBX Console is not configured properly., OCI-P Error code: [Error 26088] Cloud PBX Console is not configured properly.']
    detail: Optional[list[str]] = None
    #: Error Tracking ID.
    #: example: CPAPI_2da34568-1e72-4196-b613-905ce45ec592_0
    trackingId: Optional[str] = None


class RouteGroup(ApiModel):
    #: Route group ID the Route list is associated with.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2ZjN2EzZDU2LTg1OGMtNDVkZC1iZDA1LTE2OWM2NGU1OTRmMQ
    id: Optional[str] = None
    #: Name of the Route group the Route list associated with.
    #: example: Route Group 01
    name: Optional[str] = None
    #: Flag to indicate if the route group is used.
    #: example: True
    inUse: Optional[bool] = None


class RouteGroupGet(ApiModel):
    #: Name of the route group.
    #: example: 'Route Group One'
    name: Optional[str] = None
    #: Organization details.
    organization: Optional[Customer] = None
    #: Local Gateways that are part of this Route Group.
    localGateways: Optional[list[LocalGateways]] = None


class RouteGroupPatch(ApiModel):
    #: A unique name for the Route Group.
    #: example: routeGroupName
    name: Optional[str] = None
    #: Local Gateways that are part of this Route Group.
    localGateways: Optional[list[LocalGateways]] = None


class RouteGroupUsageRouteListItem(ApiModel):
    #: Route list ID.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0xJU1QvOTljNjJkMGQtNmFhYi00NGQ0LWE0ZTctZjk0MjQ4OWVhMWJj
    id: Optional[str] = None
    #: Route list name.
    #: example: routeListName
    name: Optional[str] = None
    #: Location ID for route list.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2JjNWUwNWFjLTI5ZmEtNGY0NS05MmM1LWUxZTExMDc0OTIwZg
    locationId: Optional[str] = None
    #: Location name for route list.
    #: example: locationName
    locationName: Optional[str] = None


class RouteGroupUsageRouteListGet(ApiModel):
    #: List of route lists for this route group.
    routeLists: Optional[list[RouteGroupUsageRouteListItem]] = None


class RouteList(ApiModel):
    #: Route list ID.
    #: example: ODRkYmVmMjItYTEwNC00YWZhLTg4ODMtY2QzNjhiMTAxOWZl
    id: Optional[str] = None
    #: Route list name.
    #: example: routeListName1
    name: Optional[str] = None
    #: Name of the route group the route list is associated with.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: ID of the route group the route list is associated with.
    #: example: MjRlNDQwYTUtNzQ5NC00ODg2LWIyNTktMmFiM2I2M2ZiMGY0
    routeGroupId: Optional[str] = None
    #: Location name of the route list.
    #: example: locationName1
    locationName: Optional[str] = None
    #: Location ID of the route list.
    #: example: NjY5YmY3ODQtNjMyZS00MTA2LWFmMWItMzYxYWNkY2M1OTFh
    locationId: Optional[str] = None


class RouteListGet(ApiModel):
    #: Route list name.
    #: example: Route List 01
    name: Optional[str] = None
    #: Location associated with the Route List.
    location: Optional[Customer] = None
    #: Route group associated with the Route list.
    routeGroup: Optional[RouteGroup] = None


class RouteListNumberListGet(ApiModel):
    #: Number assigned to the Route list.
    #: example: +2147891122
    phoneNumbers: Optional[str] = None


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
    phoneNumber: Optional[str] = None
    #: Status of the number. Possible values are `INVALID`, `DUPLICATE`, `DUPLICATE_IN_LIST`, or `UNAVAILABLE`.
    #: example: DUPLICATE
    numberStatus: Optional[NumberStatus] = None
    #: Message of the number add status.
    #: example: Invalid Number
    message: Optional[str] = None


class RouteListPatch(ApiModel):
    #: Route List new name.
    #: example: New Route List
    name: Optional[str] = None
    #: New route group ID.
    #: example: NTJiZmUxNDAtYjIwMS00NTUzLWI1OGQtMmVkNDU1NTFmYTUy
    routeGroupId: Optional[str] = None


class RouteListPost(ApiModel):
    #: Name of the Route List
    #: example: RouteList01
    name: Optional[str] = None
    #: Location associated with the Route List.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2JjNWUwNWFjLTI5ZmEtNGY0NS05MmM1LWUxZTExMDc0OTIwZg
    locationId: Optional[str] = None
    #: ID of the route group associated with Route List.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2ZjN2EzZDU2LTg1OGMtNDVkZC1iZDA1LTE2OWM2NGU1OTRmMQ
    routeGroupId: Optional[str] = None


class VirtualExtension(ApiModel):
    #: Virtual extension ID.
    #: example: OTI0NzM1OTQtZGU1Mi00ZjViLTk0YjItN2Y5MzRmY2Y2NDk3
    id: Optional[str] = None
    #: Virtual extension display first name.
    #: example: firstName1
    firstName: Optional[str] = None
    #: Virtual extension display last name.
    #: example: lastName1
    lastName: Optional[str] = None
    #: Virtual extension display name.
    #: example: displayName1
    displayName: Optional[str] = None
    #: Extension that the virtual extension is associated with.
    #: example: 0007
    extension: Optional[datetime] = None
    #: Phone number that the virtual extension is associated with.
    #: example: 8701278963
    phoneNumber: Optional[str] = None
    #: Location name if the virtual extension is at the location level, empty if it is at customer level.
    #: example: locationName1
    locationName: Optional[str] = None
    #: Location ID if the virtual extension is at the location level, empty if it is at customer level.
    #: example: MWU5ZmEzZmEtYTQ0ZS00MDJhLWExNDItMjJmODQxMjhkOTY4
    locationId: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunkName: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunkId: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    routeGroupId: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunkLocationName: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunkLocationId: Optional[str] = None


class VirtualExtensionRange(ApiModel):
    #: Virtual extension range ID.
    #: example: OTI0NzM1OTQtZGU1Mi00ZjViLTk0YjItN2Y5MzRmY2Y2NDk3
    id: Optional[str] = None
    #: Virtual extension range name.
    #: example: firstName1
    name: Optional[str] = None
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix; BCD/Enhanced mode can have any valid prefix).
    #: example: +1214555
    prefix: Optional[str] = None
    #: Pattern associated with the virtual extension range.
    #: example: 2XXX
    pattern: Optional[str] = None
    #: Location name if the virtual extension range is at the location level, empty if it is at customer level.
    #: example: locationName1
    locationName: Optional[str] = None
    #: Location ID if the virtual extension range is at the location level, empty if it is at customer level.
    #: example: MWU5ZmEzZmEtYTQ0ZS00MDJhLWExNDItMjJmODQxMjhkOTY4
    locationId: Optional[str] = None
    #: Trunk name.
    #: example: trunkName1
    trunkName: Optional[str] = None
    #: Trunk ID.
    #: example: MDhmYzI3YTAtZWEwYy00MWQxLWJlMjMtNzg0YWQ3MjZmMmM1
    trunkId: Optional[str] = None
    #: Route group name.
    #: example: routeGroupName1
    routeGroupName: Optional[str] = None
    #: Route group ID.
    #: example: YTcwYTUwOGMtZTdhYy00YzU2LWIyM2ItZTAzMjE5ZGJjMzgy
    routeGroupId: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunkLocationName: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: MjJhZDhiYWUtZTE3NS00YzIxLWFjYTctNWJmYjA2Y2YxZGEw
    trunkLocationId: Optional[str] = None


class TestCallRoutingPostResponse(ApiModel):
    #: Only returned when `originatorNumber` is specified in the request.
    callSourceInfo: Optional[CallSourceInfo] = None
    #: Matching destination type for the call.
    destinationType: Optional[DestinationType] = None
    #: FAC code if `destinationType` is FAC. The routing address will be returned for all other destination types.
    #: example: 007
    routingAddress: Optional[datetime] = None
    #: Outside access code.
    #: example: 1234
    outsideAccessCode: Optional[datetime] = None
    #: `true` if the call would be rejected.
    isRejected: Optional[bool] = None
    #: Returned when `destinationType` is `HOSTED_AGENT`.
    hostedAgent: Optional[HostedAgent] = None
    #: Returned when `destinationType` is `HOSTED_FEATURE`.
    hostedFeature: Optional[HostedFeature] = None
    #: Returned when `destinationType` is `PBX_USER`.
    pbxUser: Optional[PbxUser] = None
    #: Returned when `destinationType` is `PSTN_NUMBER`.
    pstnNumber: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `VIRTUAL_EXTENSION`.
    virtualExtension: Optional[VirtualExtension] = None
    #: Returned when `destinationType` is `VIRTUAL_EXTENSION_RANGE`.
    virtualExtensionRange: Optional[VirtualExtensionRange] = None
    #: Returned when `destinationType` is `ROUTE_LIST`.
    routeList: Optional[RouteList] = None
    #: Returned when `destinationType` is `FAC`.
    featureAccessCode: Optional[FeatureAccessCode] = None
    #: Returned when `destinationType` is `EMERGENCY`.
    emergency: Optional[Emergency] = None
    #: Returned when `destinationType` is `REPAIR`.
    repair: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `UNKNOWN_EXTENSION`.
    unknownExtension: Optional[PstnNumber] = None
    #: Returned when `destinationType` is `UNKNOWN_NUMBER`.
    unknownNumber: Optional[PstnNumber] = None


class TrunkType(str, Enum):
    #: For Cisco CUBE Local Gateway.
    registering = 'REGISTERING'
    #: For Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller, Ribbon Session Border Controller.
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
    inUse: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunkType: Optional[TrunkType] = None


class TrunkFQDNValidatePost(ApiModel):
    #: FQDN or SRV address of the trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name of the trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port of the trunk.
    #: example: 5000.0
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
    otgDtgId: Optional[str] = None
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    #: example: lg1_sias10_cpapi16004_LGU@64941297.int10.bcld.webex.com
    linePort: Optional[str] = None
    #: Locations using trunk.
    locationsUsingTrunk: Optional[list[Customer]] = None
    #: User ID.
    #: example: lg1_sias10_cpapi12446_LGU@64941297.int10.bcld.webex.com
    pilotUserId: Optional[str] = None
    #: Contains the body of the HTTP response received following the request to Console API and will not be set if the response has no body.
    outboundProxy: Optional[TrunkGetOutboundProxy] = None
    #: User's authentication service information.
    #: example: lg1_sias10_cpapi12446_LGU
    sipAuthenticationUserName: Optional[str] = None
    #: Device status.
    status: Optional[DeviceStatus] = None
    #: Error codes.
    #: example: ['errorCodes']
    errorCodes: Optional[list[str]] = None
    #: Present partial error/warning status information included when the http response is 206.
    responseStatus: Optional[ResponseStatus] = None
    #: Determines the behavior of the From and PAI headers on outbound calls.
    #: example: True
    dualIdentitySupportEnabled: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunkType: Optional[TrunkType] = None
    #: Device type assosiated with trunk.
    #: example: Cisco Unified Border Element
    deviceType: Optional[str] = None
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name. Required to create a static certificate based trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port. Required to create a static certificate-based trunk.
    #: example: 5000.0
    port: Optional[int] = None
    #: Max Concurrent call. Required to create a static certificate based trunk.
    #: example: 1000.0
    maxConcurrentCalls: Optional[int] = None


class TrunkPost(ApiModel):
    #: A unique name for the trunk.
    #: example: trunkName
    name: Optional[str] = None
    #: ID of location associated with the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    locationId: Optional[str] = None
    #: A password to use on the trunk.
    #: example: password
    password: Optional[str] = None
    #: Dual Identity Support setting impacts the handling of the From header and P-Asserted-Identity header when sending an initial SIP `INVITE` to the trunk for an outbound call.
    #: example: True
    dualIdentitySupportEnabled: Optional[bool] = None
    #: Trunk Type associated with the trunk.
    trunkType: Optional[TrunkType] = None
    #: Device type assosiated with trunk.
    #: example: Cisco Unified Border Element
    deviceType: Optional[str] = None
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    #: example: lgw1.london
    address: Optional[str] = None
    #: Domain name. Required to create a static certificate based trunk.
    #: example: acme.corp
    domain: Optional[str] = None
    #: FQDN port. Required to create a static certificate-based trunk.
    #: example: 5000.0
    port: Optional[int] = None
    #: Max Concurrent call. Required to create a static certificate based trunk.
    #: example: 1000.0
    maxConcurrentCalls: Optional[int] = None


class TrunkPut(ApiModel):
    #: A unique name for the dial plan.
    #: example: dialPlanName
    name: Optional[str] = None
    #: A password to use on the trunk.
    #: example: password
    password: Optional[str] = None
    #: Determines the behavior of the From and PAI headers on outbound calls.
    #: example: True
    dualIdentitySupportEnabled: Optional[bool] = None
    #: Max Concurrent call. Required to create a static certificate-based trunk.
    #: example: 1000.0
    maxConcurrentCalls: Optional[int] = None


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunkType: Optional[TrunkType] = None
    #: Device types for trunk configuration.
    deviceTypes: Optional[list[DeviceType]] = None


class TrunkTypeGetList(ApiModel):
    #: Trunk type with device types.
    trunkTypes: Optional[list[TrunkTypeWithDeviceType]] = None
