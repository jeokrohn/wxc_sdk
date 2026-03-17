from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.person_settings.ecbn import ECBNDependencies

__all__ = [
    'OrgEmergencyServicesApi',
    'OrgEmergencyCallNotification',
    'OrgPrefixObject',
    'RedSkyAccount',
    'ComplianceStatus',
    'LoginResponse',
    'LocationCallNotification',
    'RedSkyOrgStatus',
    'RedSkyComplianceStatus',
    'ComplianceLocationStatus',
    'RedSkyLocationParameters',
    'RedSkyLocationState',
    'RedSkyClientLocation',
]


class OrgEmergencyCallNotification(ApiModel):
    #: When true sends an email to the specified email address when a call is made to emergency services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None

    def update(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True)


class OrgPrefixObject(str, Enum):
    #: The customer is Webex calling.
    wxc = 'wxc'
    #: The customer is a wholesale.
    wxc_whs = 'wxc-whs'


class RedSkyAccount(ApiModel):
    #: `true` if the service is enabled.
    enabled: Optional[bool] = None
    #: The RedSky company ID, which can be retrieved from the RedSky portal.
    company_id: Optional[str] = None
    #: The company secret key, which can be found in the RedSky portal. It will be displayed with data masked.
    secret: Optional[str] = None
    #: `true` if RedSky is enabled for any location.
    locations_enabled: Optional[bool] = None


class RedSkyOrgStatus(str, Enum):
    #: RedSky account configuration process is in progress.
    initialise = 'INITIALISE'
    #: RedSky account configuration process is complete.
    enabled = 'ENABLED'
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'


class ComplianceStatus(str, Enum):
    #: Customer has opted out of the E911 service.
    opted_out = 'OPTED_OUT'
    #: RedSky account compliance status has been exempted.
    exempted = 'EXEMPTED'
    #: RedSky account is non-compliant.
    non_compliant = 'NON_COMPLIANT'
    #: RedSky account is compliant.
    compliant = 'COMPLIANT'


class RedSkyLocationState(str, Enum):
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


class RedSkyClientLocation(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None
    #: Configuration stage that was last completed for the specified location. The order of precedence is
    #: `LOCATION_SETUP`, `ALERTS`, `NETWORK_ELEMENTS`, `ROUTING_ENABLE`. If at least one location is `LOCATION_SETUP`,
    #: then `locationState` will be set to `LOCATION_SETUP`. Otherwise, `locationState` will check for the next
    #: precedence option and at least one location should have that option.
    state: Optional[RedSkyLocationState] = None


class ComplianceLocationStatus(ApiModel):
    #: Configuration stage that was last completed. The order of precedence is `LOCATION_SETUP`, `ALERTS`,
    #: `NETWORK_ELEMENTS`, `ROUTING_ENABLE`. If at least one location is `LOCATION_SETUP`, then `locationState` will
    #: be set to `LOCATION_SETUP`. Otherwise, `locationState` will check for the next precedence option and at least
    #: one location should have that option.
    state: Optional[RedSkyLocationState] = None
    #: Total count of locations available in the organization.
    count: Optional[int] = None
    #: All the locations available in the organization.
    locations: Optional[list[RedSkyClientLocation]] = None


class RedSkyComplianceStatus(ApiModel):
    #: The RedSky account configuration status for the organization.
    org_status: Optional[RedSkyOrgStatus] = None
    #: The RedSky account's compliance status.
    compliance_status: Optional[ComplianceStatus] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None
    #: The RedSky organization ID for the organization which can be found in the RedSky portal.
    red_sky_org_id: Optional[str] = None
    #: `true` if an Admin has been created in RedSky.
    admin_exists: Optional[bool] = None
    #: Object that contains a list of locations, the `count` for the location list, and the `state` for the location
    #: that has completed the least amount of setup. Available if at least one location is exists.
    locations_status: Optional[ComplianceLocationStatus] = None


class LoginResponse(ApiModel):
    #: `true` if the old `companyId` secret is matched with the new `companyId` secret.
    account_match: Optional[bool] = None
    #: `true` if the RedSky reseller customer is not under a Cisco account.
    external_tenant_enabled: Optional[bool] = None
    #: The RedSky held token from the secret response.
    company_id: Optional[str] = None


class RedSkyLocationParameters(ApiModel):
    #: Enable to allow RedSky to receive network connectivity information and test calls.
    integration_enabled: Optional[bool] = None
    #: Enable to route emergency calls to RedSky.
    routing_enabled: Optional[bool] = None


class RedSkyAddress(ApiModel):
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


class LocationCallNotification(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None
    #: All locations at organization level
    organization: Optional[OrgEmergencyCallNotification] = None


class OrgEmergencyServicesApi(ApiChild, base='telephony/config'):
    """
    Organization Call Settings with Emergency Services

    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known as
    Kari’s Law, any call that's made from within your organization to emergency services must generate an email
    notification.

    Viewing these organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def get_notification(self, org_id: str = None) -> OrgEmergencyCallNotification:
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
        :rtype: :class:`OrgEmergencyCallNotification`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('emergencyCallNotification')
        data = super().get(url, params=params)
        r = OrgEmergencyCallNotification.model_validate(data)
        return r

    def update_notification(self, setting: OrgEmergencyCallNotification, org_id: str = None):
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

        :param setting: updated settings
        :type setting: OrgEmergencyCallNotification
        :param org_id: Update Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = setting.update()
        url = self.ep('emergencyCallNotification')
        super().put(url, params=params, json=body)

    def hunt_group_ecbn_dependencies(self, hunt_group_id: str, org_id: str = None) -> ECBNDependencies:
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
        :rtype: :class:`ECBNDependencies`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'huntGroups/{hunt_group_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = ECBNDependencies.model_validate(data)
        return r

    def get_location_notification(self, location_id: str, org_id: str = None) -> LocationCallNotification:
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
        :rtype: :class:`LocationCallNotification`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/emergencyCallNotification')
        data = super().get(url, params=params)
        r = LocationCallNotification.model_validate(data)
        return r

    def update_location_notification(
        self,
        location_id: str,
        emergency_call_notification_enabled: bool = None,
        email_address: str = None,
        org_id: str = None,
    ):
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
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if emergency_call_notification_enabled is not None:
            body['emergencyCallNotificationEnabled'] = emergency_call_notification_enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep(f'locations/{location_id}/emergencyCallNotification')
        super().put(url, params=params, json=body)

    def get_location_parameters(self, location_id: str, org_id: str = None) -> RedSkyLocationParameters:
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
        :rtype: :class:`RedSkyLocationParameters`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/redSky')
        data = super().get(url, params=params)
        r = RedSkyLocationParameters.model_validate(data)
        return r

    def create_location_address_and_alert_email(
        self, location_id: str, alerting_email: str, address: RedSkyAddress = None, org_id: str = None
    ):
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
        :type address: RedSkyAddress
        :param org_id: The organization in which the location exists.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['alertingEmail'] = alerting_email
        if address is not None:
            body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/redSky/building')
        super().post(url, params=params, json=body)

    def update_location_address(self, location_id: str, address: RedSkyAddress = None, org_id: str = None):
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
        :type address: RedSkyAddress
        :param org_id: The organization in which the location exists.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if address is not None:
            body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/redSky/building')
        super().put(url, params=params, json=body)

    def get_location_compliance_status(self, location_id: str, org_id: str = None) -> RedSkyComplianceStatus:
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
        :rtype: :class:`RedSkyComplianceStatus`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/redSky/status')
        data = super().get(url, params=params)
        r = RedSkyComplianceStatus.model_validate(data)
        return r

    def update_location_compliance_status(
        self, location_id: str, compliance_status: RedSkyLocationState, org_id: str = None
    ) -> ComplianceLocationStatus:
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
        :type compliance_status: RedSkyLocationState
        :param org_id: Update the E911 compliance status for the location in this organization.
        :type org_id: str
        :rtype: ComplianceLocationStatus
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['complianceStatus'] = enum_str(compliance_status)
        url = self.ep(f'locations/{location_id}/redSky/status')
        data = super().put(url, params=params, json=body)
        r = ComplianceLocationStatus.model_validate(data['locationsStatus'])
        return r

    def get_redsky_account_details(self, org_id: str = None) -> RedSkyAccount:
        """
        Retrieve RedSky account details for an organization.

        The Enhanced Emergency (E911) Service for Webex Calling provides dynamic location support and a network that
        routes emergency calls to Public Safety Answering Points (PSAP) around the US, its territories, and Canada.
        E911 services are provided in conjunction with a RedSky account.

        To retrieve the RedSky account details requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve RedSky account for the organization.
        :type org_id: str
        :rtype: :class:`RedSkyAccount`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('redSky')
        data = super().get(url, params=params)
        r = RedSkyAccount.model_validate(data)
        return r

    def create_redsky_account_and_admin(
        self, email: str, org_prefix: OrgPrefixObject = None, partner_redsky_org_id: str = None, org_id: str = None
    ):
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
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if org_prefix is not None:
            body['orgPrefix'] = enum_str(org_prefix)
        body['email'] = email
        if partner_redsky_org_id is not None:
            body['partnerRedskyOrgId'] = partner_redsky_org_id
        url = self.ep('redSky')
        super().post(url, params=params, json=body)

    def login(self, email: str, password: str, red_sky_org_id: str = None, org_id: str = None) -> LoginResponse:
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
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['email'] = email
        body['password'] = password
        if red_sky_org_id is not None:
            body['redSkyOrgId'] = red_sky_org_id
        url = self.ep('redSky/actions/login/invoke')
        data = super().post(url, params=params, json=body)
        r = LoginResponse.model_validate(data)
        return r

    def get_org_compliance(
        self, start: int = None, max_: int = None, order: str = None, org_id: str = None
    ) -> RedSkyComplianceStatus:
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
        :rtype: :class:`RedSkyComplianceStatus`
        """
        params = {}
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
        r = RedSkyComplianceStatus.model_validate(data)
        return r

    def update_service_settings(
        self,
        enabled: bool,
        company_id: str = None,
        secret: str = None,
        external_tenant_enabled: bool = None,
        email: str = None,
        password: str = None,
        org_id: str = None,
    ):
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
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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

    def get_org_compliance_status(self, org_id: str = None) -> RedSkyComplianceStatus:
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
        :rtype: :class:`RedSkyComplianceStatus`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('redSky/status')
        data = super().get(url, params=params)
        r = RedSkyComplianceStatus.model_validate(data)
        return r

    def update_org_compliance_status(
        self, compliance_status: RedSkyLocationState, org_id: str = None
    ) -> RedSkyComplianceStatus:
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
        :type compliance_status: RedSkyLocationState
        :param org_id: Update E911 compliance status for the organization.
        :type org_id: str
        :rtype: :class:`RedSkyComplianceStatus`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['complianceStatus'] = enum_str(compliance_status)
        url = self.ep('redSky/status')
        data = super().put(url, params=params, json=body)
        r = RedSkyComplianceStatus.model_validate(data)
        return r
