import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AddressObject', 'CallBackSelectedPatch', 'ComplianceStatusLocationStatusObject',
           'ComplianceStatusRequestEnum', 'ComplianceStatusResponse', 'ComplianceStatusResponseEnum',
           'ComplianceStatusResponseLocationStatusObject', 'ComplianceStatusResponseRedSkyClientLocation',
           'ECBNDirectLineEffectiveLevelType', 'ECBNQualityType', 'ECBNSelectionType', 'EmergencyServicesSettingsApi',
           'GetComplianceStatusResponse', 'GetComplianceStatusResponseLocationStateEnum',
           'GetComplianceStatusResponseLocationStatusObject', 'GetComplianceStatusResponseRedSkyClientLocation',
           'GetLocationCallNotificationObject', 'GetLocationCallingParamtersResponse',
           'GetLocationComplianceStatusResponse', 'LocationMemberInfoEffectiveLevelType', 'LoginResponse',
           'MemberType', 'OrgCallNotificationObject', 'OrgPrefixObject', 'OrgStatusEnum', 'RedSkyGetObject',
           'UpdateComplianceStatusResponseLocationStateEnum', 'VirtualLinesECBNDependenciesObject',
           'VirtualLinesECBNObject', 'VirtualLinesECBNObjectDefaultInfo', 'VirtualLinesECBNObjectDirectLineInfo',
           'VirtualLinesECBNObjectLocationMemberInfo']


class OrgPrefixObject(str, Enum):
    #: The customer is Webex calling.
    wxc = 'wxc'
    #: The customer is a wholesale.
    wxc_whs = 'wxc-whs'


class RedSkyGetObject(ApiModel):
    #: `true` if the service is enabled.
    enabled: Optional[bool] = None
    #: The RedSky company ID, which can be retrieved from the RedSky portal.
    company_id: Optional[str] = None
    #: The company secret key, which can be found in the RedSky portal. It will be displayed with data masked.
    secret: Optional[str] = None
    #: `true` if RedSky is enabled for any location.
    locations_enabled: Optional[bool] = None


class ComplianceStatusRequestEnum(str, Enum):
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'
    #: Building and locations stage of the RedSky account creation has been completed.
    location_setup = 'LOCATION_SETUP'
    #: Email notification configuration stage of the RedSky account creation has been completed.
    alerts = 'ALERTS'
    #: Network wire map configuration stage of the RedSky account creation process has been completed and Webex Calling
    #: will begin routing emergency test number calls (933) to RedSky.
    network_elements = 'NETWORK_ELEMENTS'
    #: Emergency calls for devices in the specified locations will begin to route to RedSky.
    routing_enabled = 'ROUTING_ENABLED'


class OrgStatusEnum(str, Enum):
    #: RedSky account configuration process is in progress.
    initialise = 'INITIALISE'
    #: RedSky account configuration process is complete.
    enabled = 'ENABLED'
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'


class ComplianceStatusResponseEnum(str, Enum):
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'
    #: RedSky account compliance status has been exempted.
    exempted = 'EXEMPTED'
    #: RedSky account is non-compliant.
    non_compliant = 'NON_COMPLIANT'
    #: RedSky account is compliant.
    compliant = 'COMPLIANT'


class UpdateComplianceStatusResponseLocationStateEnum(str, Enum):
    #: RedSky account is pending location setup.
    location_setup = 'LOCATION_SETUP'
    #: RedSky account is pending email notification configuration.
    alerts = 'ALERTS'
    #: RedSky account is pending network element setup.
    network_elements = 'NETWORK_ELEMENTS'
    #: RedSky account is pending the routing enable setup stage.
    routing_enable = 'ROUTING_ENABLE'


class ComplianceStatusResponseRedSkyClientLocation(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None


class ComplianceStatusResponseLocationStatusObject(ApiModel):
    #: Configuration stage that was last completed. The order of precedence is `LOCATION_SETUP`, `ALERTS`,
    #: `NETWORK_ELEMENTS`, `ROUTING_ENABLE`. If at least one location is `LOCATION_SETUP`, then `locationState` will
    #: be set to `LOCATION_SETUP`. Otherwise, `locationState` will check for the next precedence option and at least
    #: one location should have that option.
    state: Optional[UpdateComplianceStatusResponseLocationStateEnum] = None
    #: Total count of locations available in the organization.
    count: Optional[int] = None
    #: List of locations that have completed the least amount of setup. Only 4 locations are included in this list.
    locations: Optional[list[ComplianceStatusResponseRedSkyClientLocation]] = None


class GetComplianceStatusResponseLocationStateEnum(str, Enum):
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'
    #: RedSky account compliance status has been exempted.
    exempted = 'EXEMPTED'
    #: RedSky account is pending location setup.
    location_setup = 'LOCATION_SETUP'
    #: RedSky account is pending email notification configuration.
    alerts = 'ALERTS'
    #: RedSky account is pending network element setup.
    network_elements = 'NETWORK_ELEMENTS'
    #: RedSky account is pending the routing enable setup stage.
    routing_enable = 'ROUTING_ENABLE'
    #: RedSky account is compliant.
    compliant = 'COMPLIANT'


class GetComplianceStatusResponseRedSkyClientLocation(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None
    #: Configuration stage that was last completed for the specified location. The order of precedence is
    #: `LOCATION_SETUP`, `ALERTS`, `NETWORK_ELEMENTS`, `ROUTING_ENABLE`. If at least one location is `LOCATION_SETUP`,
    #: then `locationState` will be set to `LOCATION_SETUP`. Otherwise, `locationState` will check for the next
    #: precedence option and at least one location should have that option.
    state: Optional[GetComplianceStatusResponseLocationStateEnum] = None


class GetComplianceStatusResponseLocationStatusObject(ApiModel):
    #: Total count of locations available in the organization.
    count: Optional[int] = None
    #: All the locations available in the organization.
    locations: Optional[list[GetComplianceStatusResponseRedSkyClientLocation]] = None


class ComplianceStatusResponse(ApiModel):
    #: The RedSky account configuration status for the organization.
    org_status: Optional[OrgStatusEnum] = None
    #: The RedSky account's compliance status.
    compliance_status: Optional[ComplianceStatusResponseEnum] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None
    #: The RedSky organization ID for the organization which can be found in the RedSky portal.
    red_sky_org_id: Optional[str] = None
    #: `true` if an Admin has been created in RedSky.
    admin_exists: Optional[bool] = None
    #: Object that contains a list of locations, the `count` for the location list, and the `state` for the location
    #: that has completed the least amount of setup. Available if at least one location is exists.
    locations_status: Optional[ComplianceStatusResponseLocationStatusObject] = None


class GetComplianceStatusResponse(ApiModel):
    #: The RedSky account configuration status for the organization.
    org_status: Optional[OrgStatusEnum] = None
    #: The RedSky account's compliance status.
    compliance_status: Optional[ComplianceStatusResponseEnum] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None
    #: The RedSky organization ID for the organization which can be found in the RedSky portal.
    red_sky_org_id: Optional[str] = None
    #: `true` if an Admin has been created in RedSky.
    admin_exists: Optional[bool] = None
    #: Object that contains a list of locations and the `count` for the location list. Available if at least one
    #: location is exists.
    locations_status: Optional[GetComplianceStatusResponseLocationStatusObject] = None


class LoginResponse(ApiModel):
    #: `true` if the old `companyId` secret is matched with the new `companyId` secret.
    account_match: Optional[bool] = None
    #: `true` if the RedSky reseller customer is not under a Cisco account.
    external_tenant_enabled: Optional[bool] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None


class GetLocationCallingParamtersResponse(ApiModel):
    #: Enable to allow RedSky to receive network connectivity information and test calls.
    integration_enabled: Optional[bool] = None
    #: Enable to route emergency calls to RedSky.
    routing_enabled: Optional[bool] = None


class ComplianceStatusLocationStatusObject(ApiModel):
    #: Configuration stage that was last completed for the location in the request. The order of precedence is
    #: `LOCATION_SETUP`, `ALERTS`, `NETWORK_ELEMENTS`, `ROUTING_ENABLE`.
    state: Optional[GetComplianceStatusResponseLocationStateEnum] = None
    #: Total count of the `locations` list.
    count: Optional[int] = None
    #: Object that contains the `id` and the `name` for the location in the request.
    locations: Optional[list[ComplianceStatusResponseRedSkyClientLocation]] = None


class GetLocationComplianceStatusResponse(ApiModel):
    #: The RedSky account configuration status for the organization.
    org_status: Optional[OrgStatusEnum] = None
    #: The RedSky account's compliance status.
    compliance_status: Optional[ComplianceStatusResponseEnum] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None
    #: The RedSky organization ID for the organization which can be found in the RedSky portal.
    red_sky_org_id: Optional[str] = None
    #: `true` if an Admin has been created in RedSky.
    admin_exists: Optional[bool] = None
    #: Object that contains the `state`, `id`, and `name` for the `locationId` in the request.
    locations_status: Optional[ComplianceStatusLocationStatusObject] = None


class AddressObject(ApiModel):
    #: First line of the building's address.
    address_line1: Optional[str] = None
    #: Second line of the building's address.
    address_line2: Optional[str] = None
    #: City for the building's address.
    city: Optional[str] = None
    #: State or Province for the building's address.
    state_or_province: Optional[str] = None
    #: Zip or Postal Code for the building's address.
    zip_or_postal_code: Optional[str] = None
    #: Country for the building's address.
    country: Optional[str] = None


class OrgCallNotificationObject(ApiModel):
    #: When true sends an email to the specified email address when a call is made to emergency services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None


class GetLocationCallNotificationObject(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None
    #: All locations at organization level
    organization: Optional[OrgCallNotificationObject] = None


class VirtualLinesECBNDependenciesObject(ApiModel):
    #: `true` if it is the default emergency callback number for the location.
    is_location_ecbn_default: Optional[bool] = None
    #: Default emergency callback number for the virtual line if `true`.
    is_self_ecbn_default: Optional[bool] = None
    #: Number of members using this virtual line as their emergency callback number.
    dependent_member_count: Optional[int] = None


class ECBNSelectionType(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: Configure one user with another user’s telephone number as an ECBN. This option is used in place of a location’s
    #: main number when the location has multiple floors or buildings. This allows the ECBN assigned to have a more
    #: accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class ECBNDirectLineEffectiveLevelType(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: There is no effective level type selected.
    none_ = 'NONE'


class LocationMemberInfoEffectiveLevelType(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: Configure one user with another user’s telephone number as an ECBN. This option is used in place of a location’s
    #: main number when the location has multiple floors or buildings. This allows the ECBN assigned to have a more
    #: accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class ECBNQualityType(str, Enum):
    #: An activated number, associated with a User or Workspace.
    recommended = 'RECOMMENDED'
    #: An activated number, associated with anything else, like Auto Attendant or Hunt Group.
    not_recommended = 'NOT_RECOMMENDED'
    #: An inactive or non-existent number.
    invalid = 'INVALID'


class MemberType(str, Enum):
    #: Associated member is a person.
    people = 'PEOPLE'
    #: Associated member is a workspace.
    place = 'PLACE'
    #: Associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'
    #: Associated member is a hunt group.
    hunt_group = 'HUNT_GROUP'


class VirtualLinesECBNObjectDirectLineInfo(ApiModel):
    #: The callback phone number that is associated with the direct line.
    phone_number: Optional[str] = None
    #: First name of a user.
    first_name: Optional[str] = None
    #: Last name of a user.
    last_name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    effective_level: Optional[ECBNDirectLineEffectiveLevelType] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQualityType] = None


class VirtualLinesECBNObjectLocationMemberInfo(ApiModel):
    #: A unique identifier for the location member's PSTN phone number.
    phone_number: Optional[str] = None
    #: First name for the location member.
    first_name: Optional[str] = None
    #: Last name for the location member. This field will always return "." when `effectiveLevel` is `DIRECT_LINE` or
    #: `LOCATION_MEMBER_NUMBER`, and the selected member is a place.
    last_name: Optional[str] = None
    #: Member ID of user/place/virtual line/hunt group within the location.
    member_id: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    effective_level: Optional[LocationMemberInfoEffectiveLevelType] = None
    #: Contains the location-level emergency callback number if valid. If not, contains the user's main number if
    #: valid.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQualityType] = None
    #: Type of the member.
    member_type: Optional[MemberType] = None


class VirtualLinesECBNObjectDefaultInfo(ApiModel):
    #: The field contains ECBN number.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQualityType] = None


class VirtualLinesECBNObject(ApiModel):
    #: Selected number type to configure emergency call back.
    selected: Optional[ECBNSelectionType] = None
    #: Data relevant to the ECBN for this user/location/virtual line/hunt group.
    direct_line_info: Optional[VirtualLinesECBNObjectDirectLineInfo] = None
    #: Data relevant to the user/place/virtual line/hunt group selected for ECBN for this location.
    location_ecbninfo: Optional[VirtualLinesECBNObjectDirectLineInfo] = Field(alias='locationECBNInfo', default=None)
    location_member_info: Optional[VirtualLinesECBNObjectLocationMemberInfo] = None
    #: Contains the Emergency Callback Number effective value when none of the above parameters are assigned or some
    #: other value is set.
    default_info: Optional[VirtualLinesECBNObjectDefaultInfo] = None


class CallBackSelectedPatch(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: Configure one user with another user’s telephone number as an ECBN. This option is used in place of a location’s
    #: main number when the location has multiple floors or buildings. This allows the ECBN assigned to have a more
    #: accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'


class EmergencyServicesSettingsApi(ApiChild, base='telephony/config'):
    """
    Emergency Services Settings
    
    The enhanced emergency (E911) service for Webex Calling is designed for organizations with a hybrid or nomadic
    workforce. It provides dynamic location support and a network that routes emergency calls to Public Safety
    Answering Points (PSAP) across the US, its territories, and Canada.
    
    Emergency Callback Configurations can be enabled at the organization level. Users without individual telephone
    numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to make
    emergency calls. These users can either use the default ECBN for their location or be assigned another specific
    telephone number from that location for emergency purposes. A virtual line allows administrators to configure
    multiple lines for Webex Calling users. Virtual line settings support reading the dependencies for a given virtual
    line ID.
    
    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive notifications when an emergency call is made. Once activated at the organization level, individual
    locations can configure this setting to direct notifications to specific email addresses. To comply with U.S.
    Public Law 115-127, also known as Kari’s Law, any call made from within your organization to emergency services
    must generate an email notification.
    
    Viewing these organization settings requires a full, user, or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read. Modifying these organization settings requires a full administrator auth token
    with a scope of spark-admin:telephony_config_write.
    """

    def get_an_organization_emergency_call_notification(self, org_id: str = None) -> OrgCallNotificationObject:
        """
        Get an Organization Emergency Call Notification

        Get organization emergency call notification.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known
        as Kari’s Law, any call that's made from within your organization to emergency services must generate an email
        notification.

        To retrieve organization call notifications requires a full, user or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: :class:`OrgCallNotificationObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('emergencyCallNotification')
        data = super().get(url, params=params)
        r = OrgCallNotificationObject.model_validate(data)
        return r

    def update_an_organization_emergency_call_notification(self, emergency_call_notification_enabled: bool = None,
                                                           allow_email_notification_all_location_enabled: bool = None,
                                                           email_address: str = None, org_id: str = None) -> None:
        """
        Update an organization emergency call notification.

        Once settings are enabled at the organization level, the configured email address will receive emergency call
        notifications for all locations.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known
        as Kari’s Law, any call that's made from within your organization to emergency services must generate an email
        notification.

        To update organization call notification requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param emergency_call_notification_enabled: When true sends an email to the specified email address when a call
            is made to emergency services.
        :type emergency_call_notification_enabled: bool
        :param allow_email_notification_all_location_enabled: Send an emergency call notification email for all
            locations.
        :type allow_email_notification_all_location_enabled: bool
        :param email_address: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent
            to the specified email address.
        :type email_address: str
        :param org_id: Update Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if emergency_call_notification_enabled is not None:
            body['emergencyCallNotificationEnabled'] = emergency_call_notification_enabled
        if allow_email_notification_all_location_enabled is not None:
            body['allowEmailNotificationAllLocationEnabled'] = allow_email_notification_all_location_enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep('emergencyCallNotification')
        super().put(url, params=params, json=body)

    def get_dependencies_for_a_hunt_group_emergency_callback_number(self, hunt_group_id: str,
                                                                    org_id: str = None) -> VirtualLinesECBNDependenciesObject:
        """
        Get Dependencies for a Hunt Group Emergency Callback Number

        Retrieves the emergency callback number dependencies for a specific hunt group.

        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.

        Retrieving the dependencies requires a full, user, read-only or location administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param hunt_group_id: Unique identifier for the hunt group.
        :type hunt_group_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for the hunt group under this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNDependenciesObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'huntGroups/{hunt_group_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = VirtualLinesECBNDependenciesObject.model_validate(data)
        return r

    def get_a_location_emergency_call_notification(self, location_id: str,
                                                   org_id: str = None) -> GetLocationCallNotificationObject:
        """
        Get a Location Emergency Call Notification

        Get location emergency call notification.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. Once activated at the organization level,
        individual locations can configure this setting to direct notifications to specific email addresses. To comply
        with U.S. Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to
        emergency services must generate an email notification.

        To retrieve location call notifications requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve Emergency Call Notification attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Emergency Call Notification attributes for the location in this organization.
        :type org_id: str
        :rtype: :class:`GetLocationCallNotificationObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/emergencyCallNotification')
        data = super().get(url, params=params)
        r = GetLocationCallNotificationObject.model_validate(data)
        return r

    def update_a_location_emergency_call_notification(self, location_id: str,
                                                      emergency_call_notification_enabled: bool = None,
                                                      email_address: str = None, org_id: str = None) -> None:
        """
        Update a location emergency call notification.

        Once settings enabled at the organization level, the configured email address will receive emergency call
        notifications for all locations; for specific location customization, users can navigate to Management >
        Locations, select the Calling tab, and update the Emergency Call Notification settings.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. Once activated at the organization level,
        individual locations can configure this setting to direct notifications to specific email addresses. To comply
        with U.S. Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to
        emergency services must generate an email notification.

        To update location call notification requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update Emergency Call Notification attributes for this location.
        :type location_id: str
        :param emergency_call_notification_enabled: When true sends an email to the specified email address when a call
            is made from this location to emergency services.
        :type emergency_call_notification_enabled: bool
        :param email_address: Sends an email to this email address when a call is made from this location to emergency
            services and `emergencyCallNotificationEnabled` is true.
        :type email_address: str
        :param org_id: Update Emergency Call Notification attributes for a location in this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if emergency_call_notification_enabled is not None:
            body['emergencyCallNotificationEnabled'] = emergency_call_notification_enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep(f'locations/{location_id}/emergencyCallNotification')
        super().put(url, params=params, json=body)

    def get_a_location_s_red_sky_emergency_calling_parameters(self, location_id: str,
                                                              org_id: str = None) -> GetLocationCallingParamtersResponse:
        """
        Get a Location's RedSky Emergency Calling Parameters

        Get the Emergency Calling Parameters for a specific location.

        The enhanced emergency (E911) service for Webex Calling provides an emergency service designed for
        organizations with a hybrid or nomadic workforce. It provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.

        To retrieve location calling parameters requires a full, user, or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve Calling Parameters for this location.
        :type location_id: str
        :param org_id: Retrieve Calling Parameters for the location in this organization.
        :type org_id: str
        :rtype: :class:`GetLocationCallingParamtersResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/redSky')
        data = super().get(url, params=params)
        r = GetLocationCallingParamtersResponse.model_validate(data)
        return r

    def create_a_red_sky_building_address_and_alert_email_for_a_location(self, location_id: str, alerting_email: str,
                                                                         address: AddressObject = None,
                                                                         org_id: str = None) -> None:
        """
        Create a RedSky Building Address and Alert Email for a Location

        Add a RedSky building address and alert email for a specified location.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Creating a building address and alert email requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create the building address and alert email for this location.
        :type location_id: str
        :param alerting_email: Email that is used to create alerts in RedSky. At least one email is mandatory.
        :type alerting_email: str
        :param address: Contains address information for the building.
        :type address: AddressObject
        :param org_id: The organization in which the location exists.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['alertingEmail'] = alerting_email
        if address is not None:
            body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/redSky/building')
        super().post(url, params=params, json=body)

    def update_a_red_sky_building_address_for_a_location(self, location_id: str, address: AddressObject = None,
                                                         org_id: str = None) -> None:
        """
        Update a RedSky Building Address for a Location

        Update a RedSky building address for a specified location.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Updating a building address requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the building address for this location.
        :type location_id: str
        :param address: Contains address information for the building.
        :type address: AddressObject
        :param org_id: The organization in which the location exists.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if address is not None:
            body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/redSky/building')
        super().put(url, params=params, json=body)

    def get_a_location_s_red_sky_compliance_status(self, location_id: str,
                                                   org_id: str = None) -> GetLocationComplianceStatusResponse:
        """
        Get a Location's RedSky Compliance Status

        Get RedSky compliance status for a specific location.

        The enhanced emergency (E911) service for Webex Calling provides an emergency service designed for
        organizations with a hybrid or nomadic workforce. It provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.

        Retrieving the location's compliance status requires a full, user, or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the compliance status for this location.
        :type location_id: str
        :param org_id: Retrieve compliance status for the location in this organization.
        :type org_id: str
        :rtype: :class:`GetLocationComplianceStatusResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/redSky/status')
        data = super().get(url, params=params)
        r = GetLocationComplianceStatusResponse.model_validate(data)
        return r

    def update_a_location_s_red_sky_compliance_status(self, location_id: str,
                                                      compliance_status: ComplianceStatusRequestEnum,
                                                      org_id: str = None) -> ComplianceStatusLocationStatusObject:
        """
        Update a Location's RedSky Compliance Status

        Update the compliance status for a specific location.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Updating the RedSky account's compliance status requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the E911 compliance status for this location.
        :type location_id: str
        :param compliance_status: Specifies which stage of the RedSky account creation process has been completed. The
            stages must be completed in the following order: `LOCATION_SETUP`, `ALERTS`, `NETWORK_ELEMENTS`,
            `ROUTING_ENABLED`.
        :type compliance_status: ComplianceStatusRequestEnum
        :param org_id: Update the E911 compliance status for the location in this organization.
        :type org_id: str
        :rtype: ComplianceStatusLocationStatusObject
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['complianceStatus'] = enum_str(compliance_status)
        url = self.ep(f'locations/{location_id}/redSky/status')
        data = super().put(url, params=params, json=body)
        r = ComplianceStatusLocationStatusObject.model_validate(data['locationsStatus'])
        return r

    def get_a_person_s_emergency_callback_number(self, person_id: str, org_id: str = None) -> VirtualLinesECBNObject:
        """
        Get a Person's Emergency Callback Number

        Retrieve a person's emergency callback number settings.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) and
        Emergency Service Addresses to enable them to make emergency calls. These users can either utilize the default
        ECBN for their location or be assigned another specific telephone number from that location for emergency
        purposes.

        To retrieve a person's callback number requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = VirtualLinesECBNObject.model_validate(data)
        return r

    def update_a_person_s_emergency_callback_number(self, person_id: str, selected: CallBackSelectedPatch,
                                                    location_member_id: str = None, org_id: str = None) -> None:
        """
        Update a Person's Emergency Callback Number

        Update a person's emergency callback number settings.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        To update an emergency callback number requires a full, location, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: CallBackSelectedPatch
        :param location_member_id: Member ID of person/workspace/virtual line/hunt group within the location. Required
            when `selected` is `LOCATION_MEMBER_NUMBER`.
        :type location_member_id: str
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['selected'] = enum_str(selected)
        if location_member_id is not None:
            body['locationMemberId'] = location_member_id
        url = self.ep(f'people/{person_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def retrieve_a_person_s_emergency_callback_number_dependencies(self, person_id: str,
                                                                   org_id: str = None) -> VirtualLinesECBNDependenciesObject:
        """
        Retrieve A Person's Emergency Callback Number Dependencies

        Retrieve Emergency Callback Number dependencies for a person.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        Retrieving the dependencies requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNDependenciesObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = VirtualLinesECBNDependenciesObject.model_validate(data)
        return r

    def retrieve_red_sky_account_details_for_an_organization(self, org_id: str = None) -> RedSkyGetObject:
        """
        Retrieve RedSky account details for an organization.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        To retrieve the RedSky account details requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve RedSky account for the organization.
        :type org_id: str
        :rtype: :class:`RedSkyGetObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('redSky')
        data = super().get(url, params=params)
        r = RedSkyGetObject.model_validate(data)
        return r

    def create_an_account_and_admin_in_red_sky(self, email: str, org_prefix: OrgPrefixObject = None,
                                               partner_redsky_org_id: str = None, org_id: str = None) -> None:
        """
        Create an account and admin in RedSky.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Creating a RedSky account requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param email: The email for the RedSky account administrator.
        :type email: str
        :param org_prefix: Represents whether the customer is 'Webex Calling' or not.
        :type org_prefix: OrgPrefixObject
        :param partner_redsky_org_id: New organization is created under this partner organization ID if present,
            otherwise it will be created under a Cisco partner.
        :type partner_redsky_org_id: str
        :param org_id: Create RedSky account for the organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if org_prefix is not None:
            body['orgPrefix'] = enum_str(org_prefix)
        body['email'] = email
        if partner_redsky_org_id is not None:
            body['partnerRedskyOrgId'] = partner_redsky_org_id
        url = self.ep('redSky')
        super().post(url, params=params, json=body)

    def login_to_a_red_sky_admin_account(self, email: str, password: str, red_sky_org_id: str = None,
                                         org_id: str = None) -> LoginResponse:
        """
        Login to a RedSky Admin Account

        Login to Redsky for an existing account admin user to retrieve the `companyId` and verify the status of
        `externalTenantEnabled`. The password provided will not be stored.

        The enhanced emergency (E911) service for Webex Calling provides an emergency service designed for
        organizations with a hybrid or nomadic workforce. It provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.

        Logging in requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param email: Email for the RedSky account.
        :type email: str
        :param password: Password for the RedSky account.
        :type password: str
        :param red_sky_org_id: The RedSky organization ID for the organization which can be found in the RedSky portal.
        :type red_sky_org_id: str
        :param org_id: Login to a RedSky account for the organization.
        :type org_id: str
        :rtype: :class:`LoginResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['email'] = email
        body['password'] = password
        if red_sky_org_id is not None:
            body['redSkyOrgId'] = red_sky_org_id
        url = self.ep('redSky/actions/login/invoke')
        data = super().post(url, params=params, json=body)
        r = LoginResponse.model_validate(data)
        return r

    def get_the_organization_compliance_status_and_the_location_status_list(self, start: int = None, max_: int = None,
                                                                            order: str = None,
                                                                            org_id: str = None) -> GetComplianceStatusResponse:
        """
        Get the Organization Compliance Status and the Location Status List

        Get the organization compliance status and the location status list for a RedSky account.

        The enhanced emergency (E911) service for Webex Calling provides an emergency service designed for
        organizations with a hybrid or nomadic workforce. It provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.

        To retrieve organization compliance status requires a full, user or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param max_: Specifies the maximum number of records that you want to fetch.
        :type max_: int
        :param order: Sort the list of locations in ascending or descending order. To sort in descending order append
            `-desc` to possible sort order values. Possible sort order values are `locationName` and `locationState`.
        :type order: str
        :param org_id: Retrieve the compliance status and the list of location statuses for the organization.
        :type org_id: str
        :rtype: :class:`GetComplianceStatusResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        if max_ is not None:
            params['max'] = max_
        if order is not None:
            params['order'] = order
        url = self.ep('redSky/complianceStatus')
        data = super().get(url, params=params)
        r = GetComplianceStatusResponse.model_validate(data)
        return r

    def update_red_sky_service_settings(self, enabled: bool, company_id: str = None, secret: str = None,
                                        external_tenant_enabled: bool = None, email: str = None, password: str = None,
                                        org_id: str = None) -> None:
        """
        Update RedSky Service Settings

        Update the RedSky service settings.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Updating the RedSky service settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param enabled: `true` if the service is enabled.
        :type enabled: bool
        :param company_id: The RedSky company ID, which can be retrieved from the RedSky portal.
        :type company_id: str
        :param secret: The company secret key, which can be found in the RedSky portal.
        :type secret: str
        :param external_tenant_enabled: `true` if the RedSky reseller customer is not under a Cisco account.
        :type external_tenant_enabled: bool
        :param email: The email for the RedSky account. `email` is required if `externalTenantEnabled` is true.
        :type email: str
        :param password: The password for the RedSky account. `password` is required if `externalTenantEnabled` is
            true.
        :type password: str
        :param org_id: Update E911 settings for the organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if company_id is not None:
            body['companyId'] = company_id
        if secret is not None:
            body['secret'] = secret
        if external_tenant_enabled is not None:
            body['externalTenantEnabled'] = external_tenant_enabled
        if email is not None:
            body['email'] = email
        if password is not None:
            body['password'] = password
        url = self.ep('redSky/serviceSettings')
        super().put(url, params=params, json=body)

    def get_the_organization_compliance_status_for_a_red_sky_account(self,
                                                                     org_id: str = None) -> ComplianceStatusResponse:
        """
        Get the Organization Compliance Status for a RedSky Account

        Get the organization compliance status for a RedSky account. The `locationStatus.state` in the response will
        show the state for the location that is in the earliest stage of configuration.

        The enhanced emergency (E911) service for Webex Calling provides an emergency service designed for
        organizations with a hybrid or nomadic workforce. It provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.

        To retrieve organization compliance status requires a full, user or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve the compliance status for the organization.
        :type org_id: str
        :rtype: :class:`ComplianceStatusResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('redSky/status')
        data = super().get(url, params=params)
        r = ComplianceStatusResponse.model_validate(data)
        return r

    def update_the_organization_red_sky_account_s_compliance_status(self,
                                                                    compliance_status: ComplianceStatusRequestEnum,
                                                                    org_id: str = None) -> ComplianceStatusResponse:
        """
        Update the Organization RedSky Account's Compliance Status

        Update the compliance status for the customer's RedSky account.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        Updating the RedSky account's compliance status requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param compliance_status: Specifies which stage of the RedSky account creation process has been completed. The
            stages must be completed in the following order: `LOCATION_SETUP`, `ALERTS`, `NETWORK_ELEMENTS`,
            `ROUTING_ENABLED`.
        :type compliance_status: ComplianceStatusRequestEnum
        :param org_id: Update E911 compliance status for the organization.
        :type org_id: str
        :rtype: :class:`ComplianceStatusResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['complianceStatus'] = enum_str(compliance_status)
        url = self.ep('redSky/status')
        data = super().put(url, params=params, json=body)
        r = ComplianceStatusResponse.model_validate(data)
        return r

    def get_the_virtual_line_s_emergency_callback_settings(self, virtual_line_id: str,
                                                           org_id: str = None) -> VirtualLinesECBNObject:
        """
        Get the Virtual Line's Emergency Callback settings

        Retrieves the emergency callback number settings for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        Retrieving the dependencies requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualLines/{virtual_line_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = VirtualLinesECBNObject.model_validate(data)
        return r

    def update_a_virtual_line_s_emergency_callback_settings(self, virtual_line_id: str,
                                                            selected: CallBackSelectedPatch,
                                                            location_member_id: str = None,
                                                            org_id: str = None) -> None:
        """
        Update a Virtual Line's Emergency Callback settings

        Update the emergency callback number settings for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        To update virtual line callback number requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: CallBackSelectedPatch
        :param location_member_id: Member ID of person/workspace/virtual line/hunt group within the location. Required
            when `selected` is `LOCATION_MEMBER_NUMBER`.
        :type location_member_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['selected'] = enum_str(selected)
        if location_member_id is not None:
            body['locationMemberId'] = location_member_id
        url = self.ep(f'virtualLines/{virtual_line_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def get_dependencies_for_a_virtual_line_emergency_callback_number(self, virtual_line_id: str,
                                                                      org_id: str = None) -> VirtualLinesECBNDependenciesObject:
        """
        Get Dependencies for a Virtual Line Emergency Callback Number

        Retrieves the emergency callback number dependencies for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        Retrieving the dependencies requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNDependenciesObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'virtualLines/{virtual_line_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = VirtualLinesECBNDependenciesObject.model_validate(data)
        return r

    def get_a_workspace_emergency_callback_number(self, workspace_id: str,
                                                  org_id: str = None) -> VirtualLinesECBNObject:
        """
        Get a Workspace Emergency Callback Number

        Retrieve the emergency callback number setting associated with a specific workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) and
        Emergency Service Addresses to enable them to make emergency calls. These users can either utilize the default
        ECBN for their location or be assigned another specific telephone number from that location for emergency
        purposes.

        To retrieve an emergency callback number, it requires a full, location, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Retrieve Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = VirtualLinesECBNObject.model_validate(data)
        return r

    def update_a_workspace_emergency_callback_number(self, workspace_id: str, selected: CallBackSelectedPatch,
                                                     location_member_id: str = None, org_id: str = None) -> None:
        """
        Update a Workspace Emergency Callback Number

        Update the emergency callback number settings for a workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        To update an emergency callback number requires a full, location, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param workspace_id: Updating Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: CallBackSelectedPatch
        :param location_member_id: Member ID of person/workspace/virtual line/hunt group within the location. Required
            when `selected` is `LOCATION_MEMBER_NUMBER`.
        :type location_member_id: str
        :param org_id: Updating Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['selected'] = enum_str(selected)
        if location_member_id is not None:
            body['locationMemberId'] = location_member_id
        url = self.ep(f'workspaces/{workspace_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def retrieve_workspace_emergency_callback_number_dependencies(self, workspace_id: str,
                                                                  org_id: str = None) -> VirtualLinesECBNDependenciesObject:
        """
        Retrieve Workspace Emergency Callback Number Dependencies

        Retrieve Emergency Callback Number dependencies for a workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        Retrieving the dependencies requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Retrieve Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNDependenciesObject`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = VirtualLinesECBNDependenciesObject.model_validate(data)
        return r
