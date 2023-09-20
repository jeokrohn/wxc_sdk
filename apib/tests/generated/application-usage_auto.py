from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ApplicationUsage', 'ApplicationUsageCollectionResponse', 'ApplicationUsagePolicyAction']


class ApplicationUsagePolicyAction(str, Enum):
    allow = 'allow'
    deny = 'deny'


class ApplicationUsage(ApiModel):
    #: A unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZg
    id: Optional[str] = None
    #: The ID of the organization to which this application belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    orgId: Optional[str] = None
    #: The ID of the policy which permits usage of this application.
    #: example: ``
    policyId: Optional[str] = None
    #: A unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZg
    appId: Optional[str] = None
    #: A descriptive name for the application.
    #: example: My Great App
    appName: Optional[str] = None
    #: The application's Oauth client ID.
    #: example: C1234567890ABCDEF
    appClientId: Optional[str] = None
    #: URL for the application's privacy policy.
    #: example: https://www.example.com/privacy-policy
    appPrivacyUrl: Optional[str] = None
    #: URL for the application's support information.
    #: example: https://help.example.com/
    appSupportUrl: Optional[str] = None
    #: URL for the application's maintainer.
    #: example: https://www.example.com
    appCompanyUrl: Optional[str] = None
    #: Contact name for the application.
    #: example: John Andersen
    appContactName: Optional[str] = None
    #: Contact email for the application.
    #: example: info@example.com
    appContactEmail: Optional[str] = None
    #: How many users use the application.
    #: example: 5.0
    appUserAdoption: Optional[int] = None
    #: Whether or not the application is allowed by policy.
    #: example: allow
    policyAction: Optional[ApplicationUsagePolicyAction] = None
    #: The date and time the application was created.
    #: example: 2017-10-01T07:00:00.000Z
    appCreated: Optional[datetime] = None
    #: The date and time this application's usage was last updated.
    #: example: 2018-10-01T07:00:00.000Z
    lastUpdated: Optional[datetime] = None


class ApplicationUsageCollectionResponse(ApiModel):
    items: Optional[list[ApplicationUsage]] = None
