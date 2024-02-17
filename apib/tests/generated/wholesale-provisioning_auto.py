from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Address', 'Customer', 'CustomerProvisioningPrecheckResponse', 'CustomerProvisioningPrecheckResponseInfo',
           'CustomerStatus', 'Error', 'Package', 'PackageName', 'PackageStatus',
           'PrecheckAWholesaleCustomerProvisioningCustomerInfo',
           'PrecheckAWholesaleSubscriberProvisioningCustomerInfo', 'ProvisionAWholesaleCustomerCustomerInfo',
           'ProvisionAWholesaleCustomerProvisioningParameters',
           'ProvisionAWholesaleCustomerProvisioningParametersCalling',
           'ProvisionAWholesaleCustomerProvisioningParametersCallingLocation',
           'ProvisionAWholesaleCustomerProvisioningParametersMeetings',
           'ProvisionAWholesaleSubscriberProvisioningParameters', 'ResourceDetails', 'SubPartner',
           'SubPartnerProvisioningState', 'Subscriber', 'SubscriberPackage', 'SubscriberStatus',
           'UpdateAWholesaleSubscriberProvisioningParameters', 'WholesaleProvisioningApi']


class Address(ApiModel):
    #: Address Line 1.
    #: example: 771 Alder Drive
    address_line1: Optional[str] = None
    #: Address Line 2.
    #: example: Cisco Site 5
    address_line2: Optional[str] = None
    #: City of the customer.
    #: example: Milpitas
    city: Optional[str] = None
    #: State or Province of the customer.
    #: example: CA
    state_or_province: Optional[str] = None
    #: Postal/Zip code of the customer.
    #: example: 95035
    zip_or_postal_code: Optional[str] = None
    #: ISO2 country code of the customer size = 2.
    #: example: `US`:
    country: Optional[str] = None


class CustomerStatus(str, Enum):
    #: Customer is fully provisioned on Cisco Webex.
    provisioned = 'provisioned'
    #: Customer is provisioned with errors.
    provisioned_with_errors = 'provisioned_with_errors'
    #: Customer is provisioning.
    provisioning = 'provisioning'
    #: Customer is updating.
    updating = 'updating'
    #: Customer is being deleted.
    deleting = 'deleting'
    #: An error occurred provisioning the customer on Cisco Webex.
    error = 'error'
    #: The customer is pending a Denied Party List compliance check.
    pending_rpl_review = 'pending_rpl_review'


class PackageName(str, Enum):
    #: Webex Common Area Calling Package.
    common_area_calling = 'common_area_calling'
    #: Webex Calling Package.
    webex_calling = 'webex_calling'
    #: Webex Meetings Package.
    webex_meetings = 'webex_meetings'
    #: Webex Suite Package.
    webex_suite = 'webex_suite'
    #: Webex Voice Package.
    webex_voice = 'webex_voice'


class PackageStatus(str, Enum):
    #: Customer is fully provisioned on Cisco Webex.
    provisioned = 'provisioned'
    #: Customer is provisioning.
    provisioning = 'provisioning'
    #: Customer is being deleted.
    deleting = 'deleting'
    #: An error occurred provisioning the customer on Cisco Webex.
    error = 'error'


class Error(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 10022
    error_code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: The email is already associated with an existing user.
    description: Optional[str] = None


class Package(ApiModel):
    #: The Webex Wholesale Packages assigned to the customer.
    #: example: common_area_calling
    name: Optional[PackageName] = None
    #: The provisioning status of the a particular package.
    #: example: provisioned
    status: Optional[PackageStatus] = None
    #: List of warnings that occurred during that last attempt to provision/update this customer.
    #: 
    #: *Note:*
    #: 
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
    #: 
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    warnings: Optional[list[Error]] = None
    #: List of errors that occurred during that last attempt to provision/update this customer.
    #: 
    #: *Note:*
    #: 
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
    #: 
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None


class ResourceDetails(ApiModel):
    packages: Optional[list[Package]] = None


class Customer(ApiModel):
    #: A unique Cisco identifier for the customer. This value should be used for the `customerId` parameter in the
    #: Wholesale Customers and Wholesale Subscribers API.
    #: example: 'Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvNTJjZjU3NmQtNjBhOC00MDdhLWIyMmMtNDY3YzUxNTkxOTA4'
    id: Optional[str] = None
    #: The Organization ID of the enterprise on Cisco Webex, to be used when referencing this customer on other Cisco
    #: Webex APIs. Only presented when status is `provisioned`.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    org_id: Optional[str] = None
    #: External ID of the Customer.
    #: example: c1677a16-557a-4fb4-b48f-24adde57ec99
    external_id: Optional[str] = None
    address: Optional[Address] = None
    #: The provisioning status of the customer.
    #: example: provisioned
    status: Optional[CustomerStatus] = None
    #: List of package names provisioned
    #: example: ['common_area_calling', 'webex_calling', 'webex_meetings', 'webex_suite', 'webex_voice']
    packages: Optional[list[str]] = None
    resource_details: Optional[ResourceDetails] = None
    #: List of errors that occurred during that last attempt to provision/update this customer.
    #: 
    #: *Note:*
    #: 
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
    #: 
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None


class CustomerProvisioningPrecheckResponseInfo(ApiModel):
    #: Provisioning Precheck `infoCode`.
    #: example: 100
    info_code: Optional[int] = None
    #: A textual description of the `infoCode`.
    #: example: Provisioning Precheck validation successful.
    description: Optional[str] = None


class CustomerProvisioningPrecheckResponse(ApiModel):
    #: A textual representation of the Precheck response message containing the `infoCode` object in the case of a
    #: success response and the `errorCode` object in the case of failure.
    #: example: success
    message: Optional[str] = None
    #: A list of ProvisioningPreCheckResponseInfo object.
    info: Optional[CustomerProvisioningPrecheckResponseInfo] = None


class SubPartnerProvisioningState(str, Enum):
    active = 'active'
    #: Sub-partner can provision new customers and subscribers or update, delete existing ones.
    active = 'active'
    #: Sub-partner cannot provision, update customers and subscribers but can delete existing ones.
    suspended = 'suspended'


class SubPartner(ApiModel):
    #: The Organization ID for the sub-partner.
    #: example: 'Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE'
    org_id: Optional[str] = None
    #: The Wholesale Subscription ID of the partner.
    #: example: 'Sub23452345'
    subscription_id: Optional[str] = None
    #: The provisioning status of the sub-partner.
    #: example: 'active'
    provisioning_state: Optional[SubPartnerProvisioningState] = None
    #: 02-16T14:10:18.855Z' (string) - The date and time the sub-partner was created.
    #: example: '2023
    created: Optional[datetime] = None
    #: 02-22T13:43:41.117Z' (string) - The date and time from which new billing for the sub-partner started.
    #: example: '2023
    billing_start_date: Optional[datetime] = None


class SubscriberPackage(str, Enum):
    #: Calling Basic Package.
    webex_calling = 'webex_calling'
    #: Meetings Package.
    webex_meetings = 'webex_meetings'
    #: Suite Package.
    webex_suite = 'webex_suite'
    #: Voice Package.
    webex_voice = 'webex_voice'


class SubscriberStatus(str, Enum):
    #: The subscriber is fully provisioned on Cisco Webex.
    provisioned = 'provisioned'
    #: The subscriber user migration is pending.
    pending_user_migration = 'pending_user_migration'


class Subscriber(ApiModel):
    #: A unique Cisco identifier for the subscriber.
    #: example: 'Y2lzY29zcGFyazovL3VzL1NVQlNDUklCRVIvNjk3MGU2YmItNzQzOS00ZmZiLWFkMzQtZDNmZjAxNjdkZGFk'
    id: Optional[str] = None
    #: The person id of the subscriber used in the /people API. Only presented when status is `provisioned`.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The email address of the subscriber.
    #: example: john.anderson@acme.com
    email: Optional[str] = None
    #: A unique identifier for the customer.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    customer_id: Optional[str] = None
    #: External ID of the Wholesale customer.
    #: example: c1677a16-557a-4fb4-b48f-24adde57ec99
    external_customer_id: Optional[str] = None
    #: The Webex Wholesale Package assigned to the subscriber.
    #: example: webex_calling
    package: Optional[SubscriberPackage] = None
    #: The provisioning status of the user.
    #: example: provisioned
    status: Optional[SubscriberStatus] = None
    #: List of errors that occurred during that last attempt to provision/update this subscriber.
    #: 
    #: *Note:*
    #: 
    #: + This list captures errors that occurred during provisioning of the subscriber.
    #: 
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None
    #: The date and time the subscriber was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the provisioning status of the subscriber last changed.
    #: example: 2020-03-18T16:05:34.000Z
    last_status_change: Optional[datetime] = None


class ProvisionAWholesaleCustomerCustomerInfo(ApiModel):
    #: The name of the Wholesale customer. Name cannot include the "%" character.
    #: example: John's Pizza
    name: Optional[str] = None
    #: The primary email address of the customer.
    #: example: john.anderson@acme.com
    primary_email: Optional[str] = None
    #: The {ISO-639-1}_{ISO-3166} or {ISO-639-1} locale or language code used as preferred language for organization
    #: and Webex Meeting Sites. Refer to the `help page
    #: <https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cloudCollaboration/wholesale_rtm/wbxbw_b_wholesale-rtm-solution-guide/wbxbw_m_overview-of-webex-wholesale.html#Cisco_Reference.dita_deb994cb-9c48-4488-b352-54495c54ba1e>`_ for more information.
    #: example: 'en'
    language: Optional[str] = None


class ProvisionAWholesaleCustomerProvisioningParametersCallingLocation(ApiModel):
    #: Name of the wholesale customer office.
    #: example: Head Office
    name: Optional[str] = None
    #: Address of the wholesale customer.
    address: Optional[Address] = None
    #: Customer timezone for calling package.
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: Determine language for all generated emails and voice announcements.
    #: example: en_us
    language: Optional[str] = None
    #: SIP Header for any emergency calls from this location.
    #: example: 95547321
    emergency_location_identifier: Optional[str] = None


class ProvisionAWholesaleCustomerProvisioningParametersCalling(ApiModel):
    location: Optional[ProvisionAWholesaleCustomerProvisioningParametersCallingLocation] = None


class ProvisionAWholesaleCustomerProvisioningParametersMeetings(ApiModel):
    #: Customer timezone for meetings package.
    #: example: America/Los_Angeles
    timezone: Optional[str] = None


class ProvisionAWholesaleCustomerProvisioningParameters(ApiModel):
    calling: Optional[ProvisionAWholesaleCustomerProvisioningParametersCalling] = None
    meetings: Optional[ProvisionAWholesaleCustomerProvisioningParametersMeetings] = None


class PrecheckAWholesaleCustomerProvisioningCustomerInfo(ApiModel):
    #: The name of the Wholesale customer.
    #: example: John's Pizza
    name: Optional[str] = None
    #: The primary email address of the Wholesale customer.
    #: example: "john.anderson@acme.com"
    primary_email: Optional[str] = None


class ProvisionAWholesaleSubscriberProvisioningParameters(ApiModel):
    #: The first name of the subscriber.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the subscriber.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The primary phone number configured for the subscriber. A primary phone number, extension, or both must be
    #: supplied when assigning a calling-enabled package, unless the subscriber is an existing Webex Calling entitled
    #: user.
    #: example: +12405551212
    primary_phone_number: Optional[str] = None
    #: The extension configured for the subscriber. An extension, primary phone number or both must be supplied when
    #: assigning a calling-enabled package, unless the subscriber is an existing Webex Calling entitled user.
    #: example: 51212
    extension: Optional[str] = None
    #: A unique identifier for the location. This ID should be retrieved via the `List Locations
    #: <https://developer.webex.com/docs/api/v1/locations/list-locations>`_ API.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzAxMjM0NTY3LTg5YWItY2RlZi0wMTIzLTQ1Njc4OWFiY2RlZg==
    location_id: Optional[str] = None


class UpdateAWholesaleSubscriberProvisioningParameters(ApiModel):
    #: The primary phone number configured for the subscriber. A primary phone number, extension, or both must be
    #: supplied when changing from the webex_meetings package to any calling-enabled package.
    #: example: +1-240-555-1212
    primary_phone_number: Optional[str] = None
    #: The extension configured for the subscriber. An extension, primary phone number or both must be supplied when
    #: changing from the webex_meetings package to any calling-enabled package.
    #: example: 5221
    extension: Optional[str] = None
    #: A unique identifier for the location. This id should be retrieved via the `List Locations
    #: <https://developer.webex.com/docs/api/v1/locations/list-locations>`_ API.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzAxMjM0NTY3LTg5YWItY2RlZi0wMTIzLTQ1Njc4OWFiY2RlZg==
    location_id: Optional[str] = None


class PrecheckAWholesaleSubscriberProvisioningCustomerInfo(ApiModel):
    #: The primary email address of the customer.
    #: example: "john.anderson@acme.com"
    primary_email: Optional[str] = None


class WholesaleProvisioningApi(ApiChild, base='wholesale'):
    """
    Wholesale Provisioning
    
    These are a set of APIs that are specifically targeted at Service Providers who sign up for Webex Wholesale. They
    enable Service Providers to provision Webex Services for their Customers.
    
    Viewing Webex Wholesale customer information requires an administrator API access token with
    `spark-admin:wholesale_customers_read` scope. Provisioning, updating, and removing customers requires an
    administrator API token with the `spark-admin:wholesale_customers_write` scope.
    
    Additional information codes are given for all success cases. To learn more about the error and info codes used in
    Wholesale Customer Provisioning Precheck APIs, see the `Provisioning Precheck API Error Codes
    <https://developer.webex.com/docs/api/guides/webex-for-wholesale#api-error-codes>`_ guide.
    
    Each Webex Developer Sandbox for Webex Wholesale use is limited to a maximum
    of 10 account users for validation and test purposes only. Cisco may from time
    to time audit Webex Developer Sandbox accounts and reserves the right to
    remove users in excess of 10 account users, or terminate the Webex Developer
    Sandbox environment for any Developer resource misuse.
    
    """

    def list_wholesale_customers(self, external_id: str = None, status: list[str] = None, org_id: str = None,
                                 **params) -> Generator[Customer, None, None]:
        """
        List Wholesale Customers

        This API allows a Service Provider to search for their customers. There are a number of filter options, which
        can be combined in a single request.

        :param external_id: Customer external ID.
        :type external_id: str
        :param status: Customer API status.
        :type status: list[str]
        :param org_id: The encoded Organization ID for the customer.
        :type org_id: str
        :return: Generator yielding :class:`Customer` instances
        """
        if external_id is not None:
            params['externalId'] = external_id
        if org_id is not None:
            params['orgId'] = org_id
        if status is not None:
            params['status'] = ','.join(status)
        url = self.ep('customers')
        return self.session.follow_pagination(url=url, model=Customer, item_key='items', params=params)

    def provision_a_wholesale_customer(self, provisioning_id: str, packages: list[str], external_id: str,
                                       address: Address,
                                       customer_info: ProvisionAWholesaleCustomerCustomerInfo = None,
                                       provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters = None,
                                       org_id: str = None) -> str:
        """
        Provision a Wholesale Customer

        Provision a Wholesale customer for Cisco Webex services.

        This API will allow a Service Provider to map the Wholesale customer and assign the required licenses and
        entitlements for Webex, Calling and Meetings.

        The Wholesale customer provisioning is asynchronous and thus a background task is created when this endpoint is
        invoked.

        <div>
        <Callout type='info'>After successful invocation of this endpoint a URL will be returned in the `Location`
        header, which will point to the `Get a Wholesale Customer
        <https://developer.webex.com/docs/api/v1/wholesale-provisioning/get-a-wholesale-customer>`_ endpoint for this customer.</Callout>
        </div>

        :param provisioning_id: This Provisioning ID defines how this customer is to be provisioned for Webex Services.

        Each Customer Template will have their own unique Provisioning ID. This ID will be displayed under the chosen
        Customer Template
        on `Webex Control Hub
        <https://admin.webex.com>`_.
        :type provisioning_id: str
        :param packages: The complete list of Webex Wholesale packages to be assigned to the customer.
        :type packages: list[str]
        :param external_id: External ID of the Wholesale customer.
        :type external_id: str
        :param address: Billing Address of the customer.
        :type address: Address
        :param customer_info: Mandatory for new customer. Optional if Organization ID is provided.
        :type customer_info: ProvisionAWholesaleCustomerCustomerInfo
        :type provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters
        :param org_id: The Organization ID of the enterprise on Webex. Mandatory for existing customer.
        :type org_id: str
        :rtype: str
        """
        body = dict()
        body['provisioningId'] = provisioning_id
        body['packages'] = packages
        if org_id is not None:
            body['orgId'] = org_id
        body['externalId'] = external_id
        body['address'] = loads(address.model_dump_json())
        if customer_info is not None:
            body['customerInfo'] = loads(customer_info.model_dump_json())
        if provisioning_parameters is not None:
            body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        url = self.ep('customers')
        data = super().post(url, json=body)
        r = data['url']
        return r

    def get_a_wholesale_customer(self, customer_id: str) -> Customer:
        """
        Get a Wholesale Customer

        This API will allow a Service Provider to retrieve details of a provisioned Wholesale customer on Cisco Webex.

        :param customer_id: A unique identifier for the customer in question.
        :type customer_id: str
        :rtype: :class:`Customer`
        """
        url = self.ep(f'customers/{customer_id}')
        data = super().get(url)
        r = Customer.model_validate(data)
        return r

    def update_a_wholesale_customer(self, customer_id: str, packages: list[str], external_id: str = None,
                                    address: Address = None,
                                    provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters = None) -> str:
        """
        Update a Wholesale Customer

        This API allows a Service Provider to update certain details of a provisioned Wholesale customer.

        The Wholesale customer provisioning is asynchronous and thus a background task is created when this endpoint is
        invoked.

        <div>
        <Callout type='info'>After successful invocation of this endpoint a URL will be returned in the `Location`
        header, which will point to the `Get a Wholesale Customer
        <https://developer.webex.com/docs/api/v1/wholesale-provisioning/get-a-wholesale-customer>`_ endpoint for this customer.</Callout>
        </div>

        :param customer_id: A unique identifier for the customer to be updated.
        :type customer_id: str
        :param packages: The complete list of Webex Wholesale packages to be assigned to the customer, including any
            packages already provisioned. If a package has already been assigned to this customer and is not present
            in this list, then that package will be removed.
        :type packages: list[str]
        :param external_id: External ID of the Wholesale customer.
        :type external_id: str
        :param address: Billing Address of the customer.
        :type address: Address
        :param provisioning_parameters: Provisioning parameters are required when updating an existing package.
        :type provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters
        :rtype: str
        """
        body = dict()
        if external_id is not None:
            body['externalId'] = external_id
        body['packages'] = packages
        if address is not None:
            body['address'] = loads(address.model_dump_json())
        if provisioning_parameters is not None:
            body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        url = self.ep(f'customers/{customer_id}')
        data = super().put(url, json=body)
        r = data['url']
        return r

    def remove_a_wholesale_customer(self, customer_id: str):
        """
        Remove a Wholesale Customer

        Allows a Service Provider to remove the mapping between a Wholesale Customer and a Cisco Webex organization.

        :param customer_id: A unique identifier for the customer in question.
        :type customer_id: str
        :rtype: None
        """
        url = self.ep(f'customers/{customer_id}')
        super().delete(url)

    def precheck_a_wholesale_customer_provisioning(self, address: Address, provisioning_id: str = None,
                                                   packages: list[str] = None, external_id: str = None,
                                                   customer_info: PrecheckAWholesaleCustomerProvisioningCustomerInfo = None,
                                                   provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters = None,
                                                   org_id: str = None) -> CustomerProvisioningPrecheckResponse:
        """
        Precheck a Wholesale Customer Provisioning

        This API will allow the Partner sales team to verify likely success of provisioning a Wholesale customer.

        <div>
        <Callout type='info'>
        The Prerequisite for using this API is to have `wxc-wholesale` entitlement or `webex-wholesale-partner-testing`
        setting enabled for the Partner Organization. The Provisioning Precheck APIs supports two variants of
        Wholesale Customer Provisioning Precheck Requests. Please refer to `Using the Provisioning Precheck APIs
        <https://developer.webex.com/docs/api/guides/webex-for-wholesale#using-the-precheck-provisioning-api>`_
        section in `Webex for Wholesale
        <https://developer.webex.com/docs/api/guides/webex-for-wholesale>`_ guide for more information.
        </Callout>
        </div>

        :param address: Billing Address of the Wholesale customer.
        :type address: Address
        :param provisioning_id: This Provisioning ID defines how this wholesale customer is to be provisioned for Cisco
            Webex Services.

        Each Customer Template will have its unique Provisioning ID. This ID will be displayed under the chosen
        Customer Template
        on Cisco Webex Control Hub.
        :type provisioning_id: str
        :param packages: The complete list of Webex Wholesale packages to be assigned to the Wholesale customer.
        :type packages: list[str]
        :param external_id: External ID of the Wholesale customer.
        :type external_id: str
        :type customer_info: PrecheckAWholesaleCustomerProvisioningCustomerInfo
        :type provisioning_parameters: ProvisionAWholesaleCustomerProvisioningParameters
        :param org_id: The Organization ID of the enterprise on Cisco Webex.
        :type org_id: str
        :rtype: :class:`CustomerProvisioningPrecheckResponse`
        """
        body = dict()
        if provisioning_id is not None:
            body['provisioningId'] = provisioning_id
        if packages is not None:
            body['packages'] = packages
        if org_id is not None:
            body['orgId'] = org_id
        if external_id is not None:
            body['externalId'] = external_id
        body['address'] = loads(address.model_dump_json())
        if customer_info is not None:
            body['customerInfo'] = loads(customer_info.model_dump_json())
        if provisioning_parameters is not None:
            body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        url = self.ep('customers/validate')
        data = super().post(url, json=body)
        r = CustomerProvisioningPrecheckResponse.model_validate(data)
        return r

    def list_wholesale_sub_partners(self, provisioning_state: str = None,
                                    **params) -> Generator[SubPartner, None, None]:
        """
        List Wholesale Sub-partners

        This API allows a Service Provider to list all of their associated sub-partners. There are a number of filter
        and pagination options that can be combined in a single request.

        :param provisioning_state: Status to filter sub-partners based on provisioning state.
        :type provisioning_state: str
        :return: Generator yielding :class:`SubPartner` instances
        """
        if provisioning_state is not None:
            params['provisioningState'] = provisioning_state
        url = self.ep('subPartners')
        return self.session.follow_pagination(url=url, model=SubPartner, item_key='items', params=params)

    def list_wholesale_subscribers(self, customer_id: str = None, person_id: str = None,
                                   external_customer_id: str = None, email: str = None, status: str = None,
                                   after: str = None, last_status_change: str = None, sort_by: str = None,
                                   sort_order: str = None, **params) -> Generator[Subscriber, None, None]:
        """
        List Wholesale Subscribers

        This API allows a Service Provider to search for their associated subscribers. There are a number of filter
        options, which can be combined in a single request.

        :param customer_id: Wholesale customer ID.
        :type customer_id: str
        :param person_id: The person ID of the subscriber used in the `/v1/people API
            <https://developer.webex.com/docs/api/v1/people>`_.
        :type person_id: str
        :param external_customer_id: Customer external ID.
        :type external_customer_id: str
        :param email: The email address of the subscriber.
        :type email: str
        :param status: The provisioning status of the subscriber.
        :type status: str
        :param after: Only include subscribers created after this date and time. Epoch time (in milliseconds)
            preferred, but ISO 8601 date format also accepted.
        :type after: str
        :param last_status_change: Only include subscribers with a provisioning status change after this date and time.
            Epoch time (in milliseconds) preferred, but ISO 8601 date format also accepted.
        :type last_status_change: str
        :param sort_by: Supported `sortBy` attributes are `created` and `lastStatusChange`. Default is `created`.
        :type sort_by: str
        :param sort_order: Sort by `ASC` (ascending) or `DESC` (descending).
        :type sort_order: str
        :return: Generator yielding :class:`Subscriber` instances
        """
        if customer_id is not None:
            params['customerId'] = customer_id
        if person_id is not None:
            params['personId'] = person_id
        if external_customer_id is not None:
            params['externalCustomerId'] = external_customer_id
        if email is not None:
            params['email'] = email
        if status is not None:
            params['status'] = status
        if after is not None:
            params['after'] = after
        if last_status_change is not None:
            params['lastStatusChange'] = last_status_change
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_order is not None:
            params['sortOrder'] = sort_order
        url = self.ep('subscribers')
        return self.session.follow_pagination(url=url, model=Subscriber, item_key='items', params=params)

    def provision_a_wholesale_subscriber(self, customer_id: str, email: str, package: SubscriberPackage,
                                         provisioning_parameters: ProvisionAWholesaleSubscriberProvisioningParameters) -> Subscriber:
        """
        Provision a Wholesale Subscriber

        Provision a new Wholesale subscriber for Cisco Webex services.

        This API allows a Service Provider to map the Wholesale subscriber to a Cisco Webex Wholesale customer and
        assign the required licenses and entitlements for Webex, Calling and Meetings.

        **Note:**
        If this subscriber is a existing Webex Calling entitled user, the `locationId`, `primaryPhoneNumber` and
        `extension` are optional and if provided are ignored.

        :param customer_id: ID of the Provisioned Customer for Webex Wholesale.
        :type customer_id: str
        :param email: The email address of the subscriber (mandatory for the trusted email provisioning flow).
        :type email: str
        :param package: The Webex Wholesale package to be assigned to the subscriber.
        :type package: SubscriberPackage
        :type provisioning_parameters: ProvisionAWholesaleSubscriberProvisioningParameters
        :rtype: :class:`Subscriber`
        """
        body = dict()
        body['customerId'] = customer_id
        body['email'] = email
        body['package'] = enum_str(package)
        body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        url = self.ep('subscribers')
        data = super().post(url, json=body)
        r = Subscriber.model_validate(data)
        return r

    def get_a_wholesale_subscriber(self, subscriber_id: str) -> Subscriber:
        """
        Get a Wholesale Subscriber

        This API allow a Service Provider to retrieve details of a provisioned Wholesale subscriber on Cisco Webex.

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :rtype: :class:`Subscriber`
        """
        url = self.ep(f'subscribers/{subscriber_id}')
        data = super().get(url)
        r = Subscriber.model_validate(data)
        return r

    def update_a_wholesale_subscriber(self, subscriber_id: str, package: SubscriberPackage,
                                      provisioning_parameters: UpdateAWholesaleSubscriberProvisioningParameters = None) -> Subscriber:
        """
        Update a Wholesale Subscriber

        This API allows a Service Provider to update certain details of a provisioned Wholesale subscriber.

        **Note:**

        * The `provisioningParameters` attributes should only be supplied when changing from the webex_meetings package
        to any calling-enabled package.

        * Even in that scenario, if this subscriber is a existing Webex Calling entitled user, these attributes are
        optional and if provided are ignored.

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :param package: The Webex Wholesale package to be assigned to the subscriber.
        :type package: SubscriberPackage
        :type provisioning_parameters: UpdateAWholesaleSubscriberProvisioningParameters
        :rtype: :class:`Subscriber`
        """
        body = dict()
        body['package'] = enum_str(package)
        if provisioning_parameters is not None:
            body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        url = self.ep(f'subscribers/{subscriber_id}')
        data = super().put(url, json=body)
        r = Subscriber.model_validate(data)
        return r

    def remove_a_wholesale_subscriber(self, subscriber_id: str):
        """
        Remove a Wholesale Subscriber

        This API allows a Service Provider to remove the mapping between Wholesale Subscriber and a Webex user.

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :rtype: None
        """
        url = self.ep(f'subscribers/{subscriber_id}')
        super().delete(url)

    def precheck_a_wholesale_subscriber_provisioning(self, email: str, provisioning_id: str = None,
                                                     customer_id: str = None, package: SubscriberPackage = None,
                                                     provisioning_parameters: ProvisionAWholesaleSubscriberProvisioningParameters = None,
                                                     customer_info: PrecheckAWholesaleSubscriberProvisioningCustomerInfo = None) -> CustomerProvisioningPrecheckResponse:
        """
        Precheck a Wholesale Subscriber Provisioning

        This API will allow the Partner sales team to verify likely success of provisioning a wholesale subscriber.

        <div>
        <Callout type='info'>
        The Prerequisite for using this API is to have `wxc-wholesale` entitlement or `webex-wholesale-partner-testing`
        setting enabled for the Partner Organization. The Provisioning Precheck APIs supports three variants of
        Wholesale Subscriber Provisioning Precheck Requests. Please refer to `Using the Provisioning Precheck API
        <https://developer.webex.com/docs/api/guides/webex-for-wholesale#using-the-precheck-provisioning-api>`_
        section in `Webex for Wholesale
        <https://developer.webex.com/docs/api/guides/webex-for-wholesale>`_ guide for more information.
        </Callout>
        </div>

        :param email: The email address of the subscriber.
        :type email: str
        :param provisioning_id: This Provisioning ID defines how this wholesale subscriber is to be provisioned for
            Cisco Webex Services.

        Each Customer template has its unique provisioning ID. This ID is displayed under the chosen customer template
        on Cisco Webex Control Hub.
        :type provisioning_id: str
        :param customer_id: ID of the Provisioned Customer for Webex Wholesale.
        :type customer_id: str
        :param package: The Webex Wholesale package to be assigned to the subscriber.
        :type package: SubscriberPackage
        :type provisioning_parameters: ProvisionAWholesaleSubscriberProvisioningParameters
        :type customer_info: PrecheckAWholesaleSubscriberProvisioningCustomerInfo
        :rtype: :class:`CustomerProvisioningPrecheckResponse`
        """
        body = dict()
        if provisioning_id is not None:
            body['provisioningId'] = provisioning_id
        if customer_id is not None:
            body['customerId'] = customer_id
        body['email'] = email
        if package is not None:
            body['package'] = enum_str(package)
        if provisioning_parameters is not None:
            body['provisioningParameters'] = loads(provisioning_parameters.model_dump_json())
        if customer_info is not None:
            body['customerInfo'] = loads(customer_info.model_dump_json())
        url = self.ep('subscribers/validate')
        data = super().post(url, json=body)
        r = CustomerProvisioningPrecheckResponse.model_validate(data)
        return r
