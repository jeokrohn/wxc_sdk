from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Address', 'Customer', 'CustomerListResponse', 'CustomerProvisioningPrecheckResponse', 'CustomerProvisioningPrecheckResponseInfo', 'CustomerStatus', 'Error', 'Package', 'PackageName', 'PackageStatus', 'ResourceDetails', 'ResourceURL', 'SubPartner', 'SubPartnerProvisioningState', 'SubPartnersListResponse', 'Subscriber', 'SubscriberListResponse', 'SubscriberPackage', 'SubscriberStatus']


class Address(ApiModel):
    #: Address Line 1.
    #: example: 771 Alder Drive
    addressLine1: Optional[str] = None
    #: Address Line 2.
    #: example: Cisco Site 5
    addressLine2: Optional[str] = None
    #: City of the customer.
    #: example: Milpitas
    city: Optional[str] = None
    #: State or Province of the customer.
    #: example: CA
    stateOrProvince: Optional[str] = None
    #: Postal/Zip code of the customer.
    #: example: 95035
    zipOrPostalCode: Optional[str] = None
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
    errorCode: Optional[int] = None
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
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer, *after* the API has been accepted and 202 response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    warnings: Optional[list[Error]] = None
    #: List of errors that occurred during that last attempt to provision/update this customer.
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer, *after* the API has been accepted and 202 response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    errors: Optional[list[Error]] = None


class ResourceDetails(ApiModel):
    packages: Optional[list[Package]] = None


class Customer(ApiModel):
    #: A unique Cisco identifier for the customer. This value should be used for the `customerId` parameter in the Wholesale Customers and Wholesale Subscribers API.
    #: example: 'Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvNTJjZjU3NmQtNjBhOC00MDdhLWIyMmMtNDY3YzUxNTkxOTA4'
    id: Optional[str] = None
    #: The Organization ID of the enterprise on Cisco Webex, to be used when referencing this customer on other Cisco Webex APIs. Only presented when status is `provisioned`.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    orgId: Optional[str] = None
    #: External ID of the Customer.
    #: example: c1677a16-557a-4fb4-b48f-24adde57ec99
    externalId: Optional[str] = None
    address: Optional[Address] = None
    #: The provisioning status of the customer.
    #: example: provisioned
    status: Optional[CustomerStatus] = None
    #: List of package names provisioned
    #: example: ['common_area_calling', 'webex_calling', 'webex_meetings', 'webex_suite', 'webex_voice']
    packages: Optional[list[str]] = None
    resourceDetails: Optional[ResourceDetails] = None
    #: List of errors that occurred during that last attempt to provision/update this customer.
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the customer, *after* the API has been accepted and 202 response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    errors: Optional[list[Error]] = None


class CustomerListResponse(ApiModel):
    #: An array of Customer objects.
    items: Optional[list[Customer]] = None


class CustomerProvisioningPrecheckResponseInfo(ApiModel):
    #: Provisioning Precheck `infoCode`.
    #: example: 100.0
    infoCode: Optional[int] = None
    #: A textual description of the `infoCode`.
    #: example: Provisioning Precheck validation successful.
    description: Optional[str] = None


class CustomerProvisioningPrecheckResponse(ApiModel):
    #: A textual representation of the Precheck response message containing the `infoCode` object in the case of a success response and the `errorCode` object in the case of failure.
    #: example: success
    message: Optional[str] = None
    #: A list of ProvisioningPreCheckResponseInfo object.
    info: Optional[CustomerProvisioningPrecheckResponseInfo] = None


class ResourceURL(ApiModel):
    #: A URL which points to the [Get a Wholesale Customer](/docs/api/v1/wholesale-provisioning/get-a-wholesale-customer) endpoint for the provisioned customer.
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
    orgId: Optional[str] = None
    #: The Wholesale Subscription ID of the partner.
    #: example: 'Sub23452345'
    subscriptionId: Optional[str] = None
    #: The provisioning status of the sub-partner.
    #: example: 'active'
    provisioningState: Optional[SubPartnerProvisioningState] = None
    #: 02-16T14:10:18.855Z' (string) - The date and time the sub-partner was created.
    #: example: '2023
    created: Optional[datetime] = None
    #: 02-22T13:43:41.117Z' (string) - The date and time from which new billing for the sub-partner started.
    #: example: '2023
    billingStartDate: Optional[datetime] = None


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
    personId: Optional[str] = None
    #: The email address of the subscriber.
    #: example: john.anderson@acme.com
    email: Optional[str] = None
    #: A unique identifier for the customer.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    customerId: Optional[str] = None
    #: External ID of the Wholesale customer.
    #: example: c1677a16-557a-4fb4-b48f-24adde57ec99
    externalCustomerId: Optional[str] = None
    #: The Webex Wholesale Package assigned to the subscriber.
    #: example: webex_calling
    package: Optional[SubscriberPackage] = None
    #: The provisioning status of the user.
    #: example: provisioned
    status: Optional[SubscriberStatus] = None
    #: List of errors that occurred during that last attempt to provision/update this subscriber.
    #: *Note:*
    #: + This list captures errors that occurred during provisioning of the subscriber.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    errors: Optional[list[Error]] = None
    #: The date and time the subscriber was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the provisioning status of the subscriber last changed.
    #: example: 2020-03-18T16:05:34.000Z
    lastStatusChange: Optional[datetime] = None


class SubscriberListResponse(ApiModel):
    #: An array of Subscriber objects.
    items: Optional[list[Subscriber]] = None
