from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Error', 'PrecheckABroadworksSubscriberProvisioningCustomerInfo', 'Subscriber', 'SubscriberListResponse', 'SubscriberPackage', 'SubscriberProvisioningPrecheckResponse', 'SubscriberProvisioningPrecheckResponseInfo', 'SubscriberStatus']


class Error(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 10022.0
    error_code: Optional[int] = None
    #: A description of the error.
    #: example: The BroadWorks UserID is already associated with an existing user.
    description: Optional[str] = None


class SubscriberPackage(str, Enum):
    #: Softphone package.
    softphone = 'softphone'
    #: Basic package.
    basic = 'basic'
    #: Standard package.
    standard = 'standard'
    #: Premium package.
    premium = 'premium'


class SubscriberStatus(str, Enum):
    #: Subscriber Provisioning is paused, pending input of email address.
    pending_email_input = 'pending_email_input'
    #: Subscriber Provisioning is paused. The subscriber has entered an email address but has yet to complete validation.
    pending_email_validation = 'pending_email_validation'
    #: Subscriber Provisioning is paused. An automated email is sent to the subscriber, waiting for the subscriber's consent.
    pending_user_migration = 'pending_user_migration'
    #: Subscriber provisioning is in progress.
    provisioning = 'provisioning'
    #: The subscriber is fully provisioned on Webex.
    provisioned = 'provisioned'
    #: An update is in progress for a provisioned subscriber.
    updating = 'updating'
    #: An error occurred provisioning the subscriber on Webex.
    error = 'error'


class Subscriber(ApiModel):
    #: A unique Cisco identifier for the subscriber.
    #: example: 'Y2lzY29zcGFyazovL3VzL1NVQlNDUklCRVIvNjk3MGU2YmItNzQzOS00ZmZiLWFkMzQtZDNmZjAxNjdkZGFk'
    id: Optional[str] = None
    #: The Person Id of the subscriber on Webex. To be used when referencing this subscriber on other Webex APIs. Only presented when status is `provisioned`.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The user ID of the subscriber on BroadWorks.
    #: example: 95547321@sp.com
    user_id: Optional[str] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Reseller1+acme
    sp_enterprise_id: Optional[str] = None
    #: The first name of the subscriber.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the subscriber.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The email address of the subscriber.
    #: example: john.anderson@acme.com
    email: Optional[str] = None
    #: The primary phone number configured against the subscriber on BroadWorks.
    #: example: +1-240-555-1212
    primary_phone_number: Optional[str] = None
    #: The mobile phone number configured against the subscriber on BroadWorks.
    #: example: +1-818-279-1234
    mobile_phone_number: Optional[str] = None
    #: The extension number configured against the subscriber on BroadWorks.
    #: example: 1212
    extension: Optional[datetime] = None
    #: The Webex for BroadWorks Package assigned to the subscriber.
    #: example: standard
    package: Optional[SubscriberPackage] = None
    #: The provisioning status of the user.
    #: example: provisioned
    status: Optional[SubscriberStatus] = None
    #: List of errors that occurred during that last attempt to provision/update this subscriber.
    #: *Note:*
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the subscriber, *after* the API has been accepted and 200 OK response returned.
    #: + Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    errors: Optional[list[Error]] = None
    #: The date and time the subscriber was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the provisioning status of the subscriber last changed.
    #: example: 2020-03-18T16:05:34.000Z
    last_status_change: Optional[datetime] = None
    #: This Provisioning ID associated with this subscriber.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioning_id: Optional[str] = None
    #: Indicates if the subscriber was self activated, rather than provisioned via these APIs.
    self_activated: Optional[bool] = None


class SubscriberListResponse(ApiModel):
    #: An array of Subscriber objects.
    items: Optional[list[Subscriber]] = None


class SubscriberProvisioningPrecheckResponseInfo(ApiModel):
    #: Provisioning Precheck `infoCode`.
    #: example: 100.0
    info_code: Optional[int] = None
    #: A textual description of the `infoCode`.
    #: example: Provisioning Precheck validation successful.
    description: Optional[str] = None


class SubscriberProvisioningPrecheckResponse(ApiModel):
    #: A textual representation of the Precheck response message containing the `infoCode` object in the case of a success response and the `errorCode` object in the case of failure.
    #: example: success
    message: Optional[str] = None
    #: A list of `ProvisioningPreCheckResponseInfo` objects.
    info: Optional[SubscriberProvisioningPrecheckResponseInfo] = None


class PrecheckABroadworksSubscriberProvisioningCustomerInfo(ApiModel):
    #: Email address of the customer org user to be provisioned.
    #: example: "john.anderson@example.com"
    primary_email: Optional[str] = None
