from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Organization', 'OrganizationCollectionResponse', 'OrganizationSupportedContentType']


class OrganizationSupportedContentType(str, Enum):
    #: Only Webex content storage.
    native = 'native'
    #: Only ECM storage.
    external = 'external'
    #: Both Webex and ECM storage.
    hybrid = 'hybrid'


class Organization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    id: Optional[str] = None
    #: Full name of the organization.
    #: example: Acme, Inc.
    display_name: Optional[str] = None
    #: The current Enterprise Content Management setting for the organization.
    #: example: hybrid
    supported_content_type: Optional[OrganizationSupportedContentType] = None
    #: The date and time the organization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None


class OrganizationCollectionResponse(ApiModel):
    items: Optional[list[Organization]] = None
