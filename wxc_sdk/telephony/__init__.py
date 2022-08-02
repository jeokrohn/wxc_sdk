"""
Telephony types and API (location and organisation settings)
"""
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import Field, parse_obj_as

from .access_codes import AccessCodesApi
from .autoattendant import AutoAttendantApi
from .callpark import CallParkApi
from .callpark_extension import CallparkExtensionApi
from .callpickup import CallPickupApi
from .callqueue import CallQueueApi
from .calls import CallsApi
from .huntgroup import HuntGroupApi
from .location import TelephonyLocationApi
from .organisation_vm import OrganisationVoicemailSettingsAPI
from .paging import PagingApi
from .pnc import PrivateNetworkConnectApi
from .prem_pstn import PremisePstnApi
from .vm_rules import VoicemailRulesApi
from .voicemail_groups import VoicemailGroupsApi
from .voiceportal import VoicePortalApi
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..common import UserType, RouteIdentity, NumberState, ValidateExtensionsResponse, ValidatePhoneNumbersResponse
from ..common.schedules import ScheduleApi, ScheduleApiBase
from ..person_settings.permissions_out import OutgoingPermissionsApi
from ..rest import RestSession

__all__ = ['OwnerType', 'NumberLocation', 'NumberOwner', 'NumberListPhoneNumberType',
           'NumberListPhoneNumber',
           'NumberType', 'NumberDetails', 'UCMProfile',
           'TestCallRoutingResult', 'OriginatorType', 'CallSourceType', 'CallSourceInfo', 'DestinationType',
           'LocationAndNumbers', 'HostedAgentDestination', 'ServiceType', 'HostedFeatureDestination',
           'TrunkDestination', 'PbxUserDestination', 'PstnNumberDestination', 'VirtualExtensionDestination',
           'RouteListDestination', 'FeatureAccessCodeDestination', 'EmergencyDestination', 'TelephonyApi']


class OwnerType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    auto_attendant = 'AUTO_ATTENDANT'
    call_center = 'CALL_CENTER'
    group_paging = 'GROUP_PAGING'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    contact_center_link = 'CONTACT_CENTER_LINK'
    route_list = 'ROUTE_LIST'
    voicemail_group = 'VOICEMAIL_GROUP'


class NumberLocation(ApiModel):
    """
    Location of a phone number
    """
    #: ID of location for phone number.
    location_id: str = Field(alias='id')
    #: Name of the location for phone number
    name: str


class NumberOwner(ApiModel):
    """
    Owner of a phone number
    """
    #: ID of the owner to which PSTN Phone number is assigned.
    owner_id: Optional[str] = Field(alias='id')
    #: Type of the PSTN phone number's owner
    owner_type: Optional[OwnerType] = Field(alias='type')
    #: Last name of the PSTN phone number's owner
    last_name: Optional[str]
    #: First name of the PSTN phone number's owner
    first_name: Optional[str]


class NumberListPhoneNumberType(str, Enum):
    primary = 'PRIMARY'
    alternate = 'ALTERNATE'


class NumberListPhoneNumber(ApiModel):
    """
    Phone Number
    """
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str]
    #: Extension for a PSTN phone number.
    extension: Optional[str]
    #: Phone number's state.
    state: Optional[NumberState]
    #: Type of phone number.
    phone_number_type: Optional[NumberListPhoneNumberType]
    #: Indicates if the phone number is used as location clid.
    main_number: bool
    #: Indicates if a phone number is a toll free number.
    toll_free_number: bool
    location: NumberLocation
    owner: Optional[NumberOwner]


class NumberType(str, Enum):
    extension = 'EXTENSION'
    number = 'NUMBER'


class NumberDetails(ApiModel):
    assigned: int
    un_assigned: int
    in_active: int
    extension_only: int
    toll_free_numbers: int
    total: int


class UCMProfile(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    profile_id: str = Field(alias='id')
    #: Unique name for the calling UC Manager Profile.
    name: str


class OriginatorType(str, Enum):
    #: User
    user = 'USER'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class CallSourceType(str, Enum):
    """
    The type of call source.
    """
    #: Indicates that the call source is a route list
    route_list = 'ROUTE_LIST'
    #: Indicates that the call source is a dial pattern.
    dial_pattern = 'DIAL_PATTERN'
    #: Indicates that the call source extension is unknown.
    unknown_extension = 'UNKNOWN_EXTENSION'
    #: Indicates that the call source phone number is unknown.
    unknown_number = 'UNKNOWN_NUMBER'


class CallSourceInfo(ApiModel):
    """
    This data object is only returned when originatorNumber is specified in the request.
    """
    #: The type of call source.
    call_source_type: CallSourceType
    #: When originatorType is "trunk", originatorId is a valid trunk, this trunk belongs to a route group which is
    #: assigned to a route list with the name routeListA, and originatorNumber is a number assigned to routeListA.
    #: routeListA is returned here. This element is returned when callSourceType is ROUTE_LIST.
    route_list_name: Optional[str]
    #: route list id
    route_list_id: Optional[str]
    #: When originatorType is "trunk", originatorId is a valid trunk with name trunkA, trunkA belongs to a route group
    #: which is assigned to a route list with name routeListA, trunkA is also assigned to dialPlanA as routing choice,
    #: dialPlanA has dialPattern xxxx assigned. If the originatorNumber match the dialPattern xxxx, dialPlanA is
    #: returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_plan_name: Optional[str]
    #: When originatorType is "trunk", originatorId is a valid trunk with the name trunkA, trunkA belongs to a route
    #: group which is assigned to a route list with the name routeListA, trunkA is also assigned to dialPlanA as routing
    #: choice, dialPlanA has dialPattern xxxx assigned. If the originatorNumber match the dialPattern xxxx, dialPattern
    #: xxxx is returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_pattern: Optional[str]
    #: dial plan id
    dial_plan_id: Optional[str]


class DestinationType(str, Enum):
    """
    Matching destination type for the call.
    """
    #: Matching destination is a person or workspace with details in the hostedAgent field.
    hosted_agent = 'HOSTED_AGENT'
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the hostedFeature
    #: field.
    hosted_feature = 'HOSTED_FEATURE'
    #: Matching destination routes into a separate PBX with details in the pbxUser field.
    pbx_user = 'PBX_USER'
    #: Matching destination routes into a PSTN phone number with details in the pstnNumber field.
    pstn_number = 'PSTN_NUMBER'
    #: Matching destination routes into a virtual extension with details in the virtualExtension field.
    virtual_extension = 'VIRTUAL_EXTENSION'
    #: Matching destination routes into a route list with details in the routeList field.
    route_list = 'ROUTE_LIST'
    #: Matching destination routes into a feature access code (FAC) with details in the featureAccessCode field.
    fac = 'FAC'
    #: Matching destination routes into an emergency service like Red Sky, with details in the emergency field.
    emergency = 'EMERGENCY'
    #: The route is in a repair state with routing choice details in the repair field.
    repair = 'REPAIR'
    #: Target extension is unknown with routing choice details in the unknownExtension field.
    unknown_extension = 'UNKNOWN_EXTENSION'
    #: The target phone number is unknown with routing choice details in the unknownNumber field.
    unknown_number = 'UNKNOWN_NUMBER'


class LocationAndNumbers(ApiModel):
    location_name: str
    location_id: str
    phone_number: str
    extension: str


class HostedAgentDestination(LocationAndNumbers):
    """
    This data object is returned when destinationType is HOSTED_AGENT.
    """
    #: person/workspace's id
    ha_id: str = Field(alias='id')
    #: Type of agent for call destination.
    ha_type: UserType = Field(alias='type')
    #: Person or workspace's first name.
    first_name: str
    #: Person or workspace's last name.
    last_name: str


class ServiceType(str, Enum):
    auto_attendant = 'AUTO_ATTENDANT'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    call_center = 'CALL_CENTER'
    contact_center_link = 'CONTACT_CENTER_LINK'
    group_paging = 'GROUP_PAGING'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    voicemail_group = 'VOICEMAIL_GROUP'


class HostedFeatureDestination(LocationAndNumbers):
    service_type: ServiceType = Field(alias='tyoe')
    name: str
    service_instance_id: str = Field(alias='id')


class TrunkDestination(ApiModel):
    trunk_name: Optional[str]
    trunk_id: Optional[str]
    route_group_name: Optional[str]
    route_group_id: Optional[str]
    #: location of the trunk, required if trunkName is returned
    trunk_location_name: Optional[str]
    #: location id of the trunk, required if trunkName is returned
    trunk_location_id: Optional[str]


class PbxUserDestination(TrunkDestination):
    """
    This data object is returned when destinationType is PBX_USER.
    """
    #: the dial plan name that the called string matches
    dial_plan_name: str
    dial_plan_id: str
    #: the dial pattern that the called string matches
    dial_pattern: str


class PstnNumberDestination(TrunkDestination):
    pass


class VirtualExtensionDestination(LocationAndNumbers, TrunkDestination):
    virtual_extension_id: str = Field(alias='id')
    first_name: str
    last_name: str
    display_name: str


class RouteListDestination(ApiModel):
    """
    This data object is returned when destinationType is ROUTE_LIST.
    """
    route_list_id: str = Field(alias='id')
    name: str
    route_group_name: str
    route_group_id: str
    location_name: str
    location_id: str


class FeatureAccessCodeDestination(ApiModel):
    """
    This data object is returned when destinationType is FAC.
    """
    code: str
    name: str


class EmergencyDestination(TrunkDestination):
    """
    This data object is returned when destinationType is EMERGENCY.
    """
    is_red_sky: bool


class TestCallRoutingResult(ApiModel):
    #: Language for call queue.
    language: str
    #: Time zone for the call queue.
    time_zone: str
    #: This data object is only returned when originatorNumber is specified in the request.
    call_source_info: Optional[CallSourceInfo]
    #: Matching destination type for the call.
    destination_type: DestinationType
    #: FAC code if destinationType is FAC. The routing address will be returned for all other destination types.
    routing_address: str
    #: Outside access code.
    outside_access_code: str
    #: true if the call would be rejected.
    is_rejected: bool
    #: This data object is returned when destinationType is HOSTED_AGENT.
    hosted_agent: Optional[HostedAgentDestination]
    #: This data object is returned when destinationType is HOSTED_FEATURE.
    hosted_feature: Optional[HostedFeatureDestination]
    #: This data object is returned when destinationType is PBX_USER.
    pbx_user: Optional[PbxUserDestination]
    #: This data object is returned when destinationType is PSTN_NUMBER.
    pstn_number: Optional[PstnNumberDestination]
    #: This data object is returned when destinationType is VIRTUAL_EXTENSION.
    virtual_extension: Optional[VirtualExtensionDestination]
    #: This data object is returned when destinationType is ROUTE_LIST.
    route_list: Optional[RouteListDestination]
    #: This data object is returned when destinationType is FAC.
    feature_access_code: Optional[FeatureAccessCodeDestination]
    #: This data object is returned when destinationType is EMERGENCY.
    emergency: Optional[EmergencyDestination]
    #: This data object is returned when destinationType is REPAIR.
    repair: Optional[TrunkDestination]
    #: This data object is returned when destinationType is UNKNOWN_EXTENSION.
    unknown_extension: Optional[TrunkDestination]
    #: This data object is returned when destinationType is UNKNOWN_NUMBER.
    unknown_number: Optional[TrunkDestination]


@dataclass(init=False)
class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes
    access_codes: AccessCodesApi
    auto_attendant: AutoAttendantApi
    calls: CallsApi
    callpark: CallParkApi
    callpark_extension: CallparkExtensionApi
    callqueue: CallQueueApi
    huntgroup: HuntGroupApi
    #: location specific settings
    location: TelephonyLocationApi
    #: organisation voicemail settings
    organisation_voicemail: OrganisationVoicemailSettingsAPI
    paging: PagingApi
    permissions_out: OutgoingPermissionsApi
    pickup: CallPickupApi
    prem_pstn: PremisePstnApi
    pnc: PrivateNetworkConnectApi
    schedules: ScheduleApi
    voicemail_groups: VoicemailGroupsApi
    voicemail_rules: VoicemailRulesApi
    voiceportal: VoicePortalApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.access_codes = AccessCodesApi(session=session)
        self.auto_attendant = AutoAttendantApi(session=session)
        self.calls = CallsApi(session=session)
        self.callpark = CallParkApi(session=session)
        self.callpark_extension = CallparkExtensionApi(session=session)
        self.callqueue = CallQueueApi(session=session)
        self.huntgroup = HuntGroupApi(session=session)
        self.location = TelephonyLocationApi(session=session)
        self.organisation_voicemail = OrganisationVoicemailSettingsAPI(session=session)
        self.paging = PagingApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session, locations=True)
        self.pickup = CallPickupApi(session=session)
        self.pnc = PrivateNetworkConnectApi(session=session)
        self.prem_pstn = PremisePstnApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.voicemail_groups = VoicemailGroupsApi(session=session)
        self.voicemail_rules = VoicemailRulesApi(session=session)
        self.voiceportal = VoicePortalApi(session=session)

    def phone_numbers(self, *, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> Generator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='config/numbers')
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')

    def phone_number_details(self, *, org_id: str = None) -> NumberDetails:
        """
        get summary (counts) of phone numbers

        :param org_id: detaild for numbers in this organization.
        :type org_id: str
        :return: phone number details
        :rtype: :class:`NumberDetails`
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        params['details'] = 'true'
        params['max'] = 1
        url = self.ep(path='config/numbers')
        data = self.get(url, params=params)
        return NumberDetails.parse_obj(data['count'])

    def validate_extensions(self, *, extensions: list[str]) -> ValidateExtensionsResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions. Retrieving this list requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param extensions: Array of Strings of ID of Extensions.
        :type extensions: list[str]
        :return: validation response
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(path='config/actions/validateExtensions/invoke')
        data = self.post(url, json={'extensions': extensions})
        return ValidateExtensionsResponse.parse_obj(data)

    def validate_phone_numbers(self, phone_numbers: list[str], org_id: str = None) -> ValidatePhoneNumbersResponse:
        """
        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Validating a phone number in an organization requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param phone_numbers: List of phone numbers to be validated.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: validation result
        :rtype: :class:`wxc_sdk.common.ValidatePhoneNumbersResponse`
        """
        url = self.ep('config/actions/validateNumbers/invoke')
        body = {'phoneNumbers': phone_numbers}
        params = org_id and {'orgId': org_id} or None
        data = self.post(url=url, params=params, json=body)
        return ValidatePhoneNumbersResponse.parse_obj(data)

    def ucm_profiles(self, *, org_id: str = None) -> list[UCMProfile]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in
        Webex Teams (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the
        user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :return: list of :class:`UCMProfile`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(path='config/callingProfiles')
        data = self.get(url, params=params)
        return parse_obj_as(list[UCMProfile], data['callingProfiles'])

    def change_announcement_language(self, *, location_id: str, language_code: str, agent_enabled: bool = None,
                                     service_enabled: bool = None, org_id: str = None):
        """
        Change Announcement Language

        Change announcement language for the given location.

        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.

        Changing announcement language for the given location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param language_code: Language code.
        :type language_code: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'announcementLanguageCode': language_code}
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        url = self.session.ep(f'telephony/config/locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        self.put(url, json=body, params=params)

    def route_choices(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> Generator[RouteIdentity, None, None]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('config/routeChoices')
        return self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')

    def test_call_routing(self, *, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, org_id: str = None) -> TestCallRoutingResult:
        """
        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Test call routing requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param originator_id: This element is used to identify the originating party. It can be user UUID or trunk UUID.
        :type originator_id: str
        :param originator_type:
        :type originator_type: :class:`OriginatorType`
        :param destination: This element specifies called party. It can be any dialable string, for example, an
            ESN number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: str
        :param originator_number: Only used when originatorType is TRUNK. This element could be a phone number or URI.
        :type originator_number: str
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :return: call routing test result
        :rtype: :class:`TestCallRoutingResult`
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep('config/actions/testCallRouting/invoke')
        data = self.post(url=url, params=params, json=body)
        return TestCallRoutingResult.parse_obj(data)
