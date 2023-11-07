from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Address', 'Customer', 'CustomerListResponse', 'CustomerProvisioningPrecheckResponse',
            'CustomerProvisioningPrecheckResponseInfo', 'CustomerStatus', 'Error', 'Package', 'PackageName',
            'PackageStatus', 'PrecheckAWholesaleCustomerProvisioningCustomerInfo',
            'PrecheckAWholesaleSubscriberProvisioningCustomerInfo', 'ProvisionAWholesaleCustomerCustomerInfo',
            'ProvisionAWholesaleCustomerProvisioningParameters',
            'ProvisionAWholesaleCustomerProvisioningParametersCalling',
            'ProvisionAWholesaleCustomerProvisioningParametersCallingLocation',
            'ProvisionAWholesaleCustomerProvisioningParametersMeetings',
            'ProvisionAWholesaleSubscriberProvisioningParameters', 'ResourceDetails', 'ResourceURL', 'SubPartner',
            'SubPartnerProvisioningState', 'SubPartnersListResponse', 'Subscriber', 'SubscriberListResponse',
            'SubscriberPackage', 'SubscriberStatus', 'UpdateAWholesaleSubscriberProvisioningParameters']


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
    #: example: 10022.0
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
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    warnings: Optional[list[Error]] = None
    #: List of errors that occurred during that last attempt to provision/update this customer.
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
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
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer,
    #: *after* the API has been accepted and 202 response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None


class CustomerListResponse(ApiModel):
    #: An array of Customer objects.
    items: Optional[list[Customer]] = None


class CustomerProvisioningPrecheckResponseInfo(ApiModel):
    #: Provisioning Precheck `infoCode`.
    #: example: 100.0
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


class ResourceURL(ApiModel):
    #: A URL which points to the `Get a Wholesale Customer
    #: <https://developer.webex.com/docs/api/v1/wholesale-provisioning/get-a-wholesale-customer>`_ endpoint for the provisioned customer.
    #: example: "https://webexapis.com/v1/wholesale/customers/Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvNTJjZjU3NmQtNjBhOC00MDdhLWIyMmMtNDY3YzUxNTkxOTA4"
    url: Optional[str] = None


class SubPartnerProvisioningState(str, Enum):
    _active_ = 'active'
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


class SubPartnersListResponse(ApiModel):
    #: An array of `SubPartner` objects.
    items: Optional[list[SubPartner]] = None


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
    #: *Note:*
    #: + This list captures errors that occurred during provisioning of the subscriber.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None
    #: The date and time the subscriber was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the provisioning status of the subscriber last changed.
    #: example: 2020-03-18T16:05:34.000Z
    last_status_change: Optional[datetime] = None


class SubscriberListResponse(ApiModel):
    #: An array of Subscriber objects.
    items: Optional[list[Subscriber]] = None


class ProvisionAWholesaleCustomerCustomerInfo(ApiModel):
    #: The name of the Wholesale customer.
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
    #: List of numbers to be assigned to the location.
    #: example: ['+17205557878', '+17205557879', '+17205557880', '+17205557881']
    numbers: Optional[list[str]] = None
    #: Main number of the Wholesale customer.
    #: example: +17205557878
    main_number: Optional[str] = None


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
    extension: Optional[datetime] = None
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
    ...