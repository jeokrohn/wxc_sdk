from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaCallRoutingWithWxGoMNOFeatureApi', 'CallDestinationType', 'CallSourceInfo', 'CallSourceType',
           'Emergency', 'FeatureAccessCode', 'HostedAgent', 'HostedAgentType', 'HostedFeature', 'OriginatorType',
           'PbxUser', 'PstnNumber', 'RouteList', 'ServiceType', 'TestCallRoutingPostResponse', 'VirtualExtension',
           'VirtualExtensionRange']


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
    #: Indicates the type of call source.
    #: example: DIAL_PATTERN
    call_source_type: Optional[CallSourceType] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk and the trunk belongs to a route group which
    #: is assigned to a route list with the name `routeListA` and also `originatorNumber` is a number assigned to
    #: `routeListA`, then `routeListA` is returned here. This element is returned when `callSourceType` is
    #: `ROUTE_LIST`.
    #: example: routeList1
    route_list_name: Optional[str] = None
    #: Unique identifier for the route list.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0xJU1QvZDA2YWQ5M2QtY2NkOC00MzI1LTg0YzUtMDA2NThhYTdhMDBj
    route_list_id: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with name `trunkA`, `trunkA` belongs to a
    #: route group which is assigned to a route list with name `routeListA`, `trunkA` is also assigned to `dialPlanA`
    #: as routing choice, `dialPlanA` has `dialPattern` xxxx assigned. If the `originatorNumber` matches the
    #: `dialPattern` `xxxx`, `dialPlanA` is returned. This element is returned when `callSourceType` is
    #: `DIAL_PATTERN`.
    #: example: dialPlan1
    dial_plan_name: Optional[str] = None
    #: When `originatorType` is `trunk`, `originatorId` is a valid trunk with the name `trunkA`, `trunkA` belongs to a
    #: route group which is assigned to a route list with the name `routeListA`, `trunkA` is also assigned to
    #: `dialPlanA` as routing choice, `dialPlanA` has `dialPattern` `xxxx` assigned. If the `originatorNumber` matches
    #: the `dialPattern` `xxxx`, `dialPattern` `xxxx` is returned. This element is returned when `callSourceType` is
    #: `DIAL_PATTERN`.
    #: example: *888
    dial_pattern: Optional[str] = None
    #: Unique identifier for dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    dial_plan_id: Optional[str] = None


class CallDestinationType(str, Enum):
    #: Destination is a person or workspace with details in the `hostedAgent` field.
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


class Emergency(ApiModel):
    #: Indicates if `RedSky` is in use.
    #: example: True
    is_red_sky: Optional[bool] = None
    #: Name of the trunk.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1RSVU5LLzA4Yjc2MmZlLWJmYWItNGFmYi04ODQ1LTNhNzJjNGQ0NjZiOQ
    trunk_id: Optional[str] = None
    #: Name of the route group that is associated with trunk specified by `trunkId`.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Unique identifier of the location of the trunk; required if `trunkName` is returned.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    trunk_location_id: Optional[str] = None


class FeatureAccessCode(ApiModel):
    #: Feature access code to which the call is directed to.
    #: example: *70
    code: Optional[str] = None
    #: Name of the feature associated with `code`.
    #: example: Cancel Call Waiting
    name: Optional[str] = None


class HostedAgentType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'


class HostedAgent(ApiModel):
    #: Unique identifier for the person or workspace agent identified as call destination.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mMjU4YjhmZi1lODIxLTQ3MDktYTI2My1mMmI4OWZjN2FlYmQ
    id: Optional[str] = None
    #: Type of agent for call destination.
    #: example: PEOPLE
    type: Optional[HostedAgentType] = None
    #: First name for the hosted agent specified by `id`.
    #: example: firstName
    first_name: Optional[str] = None
    #: Last name for the hosted agent specified by `id`.
    #: example: lastName
    last_name: Optional[str] = None
    #: Name of hosted agent's location.
    #: example: locationName
    location_name: Optional[str] = None
    #: Unique identifier for hosted agent's location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    location_id: Optional[str] = None
    #: Phone number for the hosted agent.
    #: example: 9874531287
    phone_number: Optional[str] = None
    #: Extension for the hosted agent.
    #: example: 111
    extension: Optional[str] = None


class ServiceType(str, Enum):
    #: Indicates that this destination is an auto attendant.
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
    #: Type of the service identified as call destination.
    #: example: AUTO_ATTENDANT
    type: Optional[ServiceType] = None
    #: Name of the service identified as call destination.
    #: example: name1
    name: Optional[str] = None
    #: Unique identifier of the service identified as call destination.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QyRXdhV2R5TVRCamIwQTJORGswTVRJNU55NXBiblF4TUM1aVkyeGtMbmRsWW1WNExtTnZiUT09
    id: Optional[str] = None
    #: Name of the location with which service is associated.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Unique identifier for the location of the service.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    location_id: Optional[str] = None
    #: Phone number of the service.
    #: example: 9874531287
    phone_number: Optional[str] = None
    #: Extension of the service.
    #: example: 111
    extension: Optional[str] = None


class OriginatorType(str, Enum):
    #: Indicates that this object is a person.
    people = 'PEOPLE'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class PbxUser(ApiModel):
    #: Dial plan name that the called string matches.
    #: example: dialPlan1
    dial_plan_name: Optional[str] = None
    #: Unique identifier for the dial plan.
    #: example: Y2lzY29zcGFyazovL3VzL0RJQUxfUExBTi8wNTlhMjczZS1iYmIwLTExZWMtODQyMi0wMjQyYWMxMjAwMDI
    dial_plan_id: Optional[str] = None
    #: Dial pattern that the called string matches.
    #: example: 442xxx
    dial_pattern: Optional[str] = None
    #: Name of the trunk.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1RSVU5LLzA4Yjc2MmZlLWJmYWItNGFmYi04ODQ1LTNhNzJjNGQ0NjZiOQ
    trunk_id: Optional[str] = None
    #: Name of the route group.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    trunk_location_id: Optional[str] = None


class PstnNumber(ApiModel):
    #: Name of the trunk.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1RSVU5LLzA4Yjc2MmZlLWJmYWItNGFmYi04ODQ1LTNhNzJjNGQ0NjZiOQ
    trunk_id: Optional[str] = None
    #: Name of the route group.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    trunk_location_id: Optional[str] = None


class RouteList(ApiModel):
    #: Unique identifier of the route list.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0xJU1QvZDA2YWQ5M2QtY2NkOC00MzI1LTg0YzUtMDA2NThhYTdhMDBj
    id: Optional[str] = None
    #: Name of the route list.
    #: example: routeListName1
    name: Optional[str] = None
    #: Name of the route group the route list is associated with.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group the route list is associated with.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location name of the route list.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID of the route list.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    location_id: Optional[str] = None


class VirtualExtension(ApiModel):
    #: Unique identifier for the virtual extension.
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfRVhURU5TSU9OL2U4NTU0MGJjLWFiNDMtNGZjOS05ZThlLTkxZjRkN2E3ZjU5Ng
    id: Optional[str] = None
    #: The first name of the virtual extension.
    #: example: firstName1
    first_name: Optional[str] = None
    #: The last name of the virtual extension.
    #: example: lastName1
    last_name: Optional[str] = None
    #: The full name of the virtual extension.
    #: example: displayName1
    display_name: Optional[str] = None
    #: Extension that the virtual extension is associated with.
    #: example: 7
    extension: Optional[str] = None
    #: Phone number that the virtual extension is associated with.
    #: example: 8701278963
    phone_number: Optional[str] = None
    #: Location name if the virtual extension is at the location level, empty if it is at the customer level.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID if the virtual extension is at the location level, empty if it is at customer level.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    location_id: Optional[str] = None
    #: Name of the trunk.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1RSVU5LLzA4Yjc2MmZlLWJmYWItNGFmYi04ODQ1LTNhNzJjNGQ0NjZiOQ
    trunk_id: Optional[str] = None
    #: Name of the route group.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    trunk_location_id: Optional[str] = None


class VirtualExtensionRange(ApiModel):
    #: Unique identifier for virtual extension range.
    #: example: OTI0NzM1OTQtZGU1Mi00ZjViLTk0YjItN2Y5MzRmY2Y2NDk3
    id: Optional[str] = None
    #: Name of the virtual extension range.
    #: example: firstName1
    name: Optional[str] = None
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix;
    #: BCD/Enhanced mode can have any valid prefix).
    #: example: +1214555
    prefix: Optional[str] = None
    #: Pattern associated with the virtual extension range.
    #: example: 2XXX
    pattern: Optional[str] = None
    #: Location name if the virtual extension range is at the location level, empty if it is at the customer level.
    #: example: locationName1
    location_name: Optional[str] = None
    #: Location ID if the virtual extension range is at the location level, empty if it is at customer level.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    location_id: Optional[str] = None
    #: Name of the trunk.
    #: example: trunkName1
    trunk_name: Optional[str] = None
    #: Unique identifier of the trunk.
    #: example: Y2lzY29zcGFyazovL3VzL1RSVU5LLzA4Yjc2MmZlLWJmYWItNGFmYi04ODQ1LTNhNzJjNGQ0NjZiOQ
    trunk_id: Optional[str] = None
    #: Name of the route group.
    #: example: routeGroupName1
    route_group_name: Optional[str] = None
    #: Unique identifier of the route group.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL2YyODkyMTc0LWYxM2YtNDhjYy1iMmJhLWQ4ZmM4Yzg4MzJhYg
    route_group_id: Optional[str] = None
    #: Location of the trunk; required if `trunkName` is returned.
    #: example: trunkLocationName1
    trunk_location_name: Optional[str] = None
    #: Location ID of the trunk; required if `trunkName` is returned.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVlZmI5MTFhLThmNmUtNGU2Ny1iOTZkLWNkM2VmNmRhNDE2OA
    trunk_location_id: Optional[str] = None


class TestCallRoutingPostResponse(ApiModel):
    #: Only returned when `originatorNumber` is specified in the request.
    call_source_info: Optional[CallSourceInfo] = None
    #: Destination type for the call.
    #: example: HOSTED_AGENT
    destination_type: Optional[CallDestinationType] = None
    #: FAC code if `destinationType` is FAC. The routing address will be returned for all other destination types.
    #: example: 7
    routing_address: Optional[str] = None
    #: Outside access code.
    #: example: 1234
    outside_access_code: Optional[str] = None
    #: `true` if the call would be rejected.
    is_rejected: Optional[bool] = None
    #: Calling line ID (CLID) configured for the calling user.
    #: example: +12036680442
    calling_line_id: Optional[str] = Field(alias='callingLineID', default=None)
    #: Routing profile that is used to route network calls.
    #: example: AttRtPf
    routing_profile: Optional[str] = None
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


class BetaCallRoutingWithWxGoMNOFeatureApi(ApiChild, base='telephony/config/actions/testCallRouting/invoke'):
    """
    Beta Call Routing with WxGo-MNO Feature
    
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

    def test_call_routing(self, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, org_id: str = None) -> TestCallRoutingPostResponse:
        """
        Test Call Routing

        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Two new fields, `callingLineID` and `routingProfile`, have been added to the response object as part of the
        WxGo-MNO feature.

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
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = TestCallRoutingPostResponse.model_validate(data)
        return r
