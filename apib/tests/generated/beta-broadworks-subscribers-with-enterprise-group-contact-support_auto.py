from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Error', 'Subscriber', 'SubscriberListResponse', 'SubscriberPackage', 'SubscriberStatus']


class Error(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 10022.0
    errorCode: Optional[int] = None
    #: A description of the error.
    #: example: The BroadWorks UserID is already associated with an existing user.
    description: Optional[str] = None


class SubscriberPackage(str, Enum):
    #: Softphone package
    softphone = 'softphone'
    #: Basic package
    basic = 'basic'
    #: Standard package
    standard = 'standard'
    #: Premium package
    premium = 'premium'


class SubscriberStatus(str, Enum):
    #: Subscriber provisioning is paused, pending input of an email address.
    pending_email_input = 'pending_email_input'
    #: Subscriber provisioning is paused. The subscriber has entered an email address but has yet to complete validation.
    pending_email_validation = 'pending_email_validation'
    #: Subscriber provisioning is paused. An automated email has been sent to the subscriber; waiting for the subscriber's consent.
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
    personId: Optional[str] = None
    #: The user ID of the subscriber on BroadWorks.
    #: example: 95547321@sp.com
    userId: Optional[str] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Enterprise1
    spEnterpriseId: Optional[str] = None
    #: The group name under the enterprise in Broadworks. Only applicable to Enterprise mode.
    #: example: BroadworksEnterpriseGroup
    spEnterpriseGroupId: Optional[str] = None
    #: The first name of the subscriber.
    #: example: John
    firstName: Optional[str] = None
    #: The last name of the subscriber.
    #: example: Andersen
    lastName: Optional[str] = None
    #: The email address of the subscriber.
    #: example: john.anderson@acme.com
    email: Optional[str] = None
    #: The primary phone number configured against the subscriber on BroadWorks.
    #: example: +1-240-555-1212
    primaryPhoneNumber: Optional[str] = None
    #: The mobile phone number configured against the subscriber on BroadWorks.
    #: example: +1-818-279-1234
    mobilePhoneNumber: Optional[str] = None
    #: The ISO 639-1 language code associated with the subscriber. Reserved for future use. Any value returned should be ignored. Currently set to "en" in all responses.
    #: example: en
    language: Optional[str] = None
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
    lastStatusChange: Optional[datetime] = None
    #: This Provisioning ID associated with this subscriber.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioningId: Optional[str] = None
    #: Indicates if the subscriber was self activated, rather than provisioned via these APIs.
    selfActivated: Optional[bool] = None


class SubscriberListResponse(ApiModel):
    #: An array of Subscriber objects.
    items: Optional[list[Subscriber]] = None
