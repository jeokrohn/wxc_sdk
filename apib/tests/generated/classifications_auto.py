from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['HydraClassification', 'OrganizationsSpaceClassificationCollectionResponse']


class HydraClassification(ApiModel):
    #: Unique identifier for the org's Space Classification
    #: example: Y2lzY29zcGFyazovL3VzL0NMQVNTSUZJQ0FUSU9OL2YyMDUyZTgyLTU0ZjgtMTFlYS1hMmUzLTJlNzI4Y2U4ODEyNQ
    id: Optional[str] = None
    #: Represents the rank of the classification. A number from 0 to 4, in which 0 usually refers to "public", and is the default whenever a rank cannot be determined.
    rank: Optional[int] = None
    #: Represents the classification title to be displayed in classified spaces for org users.
    #: example: Public
    title: Optional[str] = None
    #: Space Classification enabled state.
    #: example: True
    enabled: Optional[bool] = None
    #: Classification's description.
    #: example: Does not contain private information
    description: Optional[str] = None
    #: The date and time the Space Classification was last changed.
    #: example: 2020-02-22T00:06:42.438Z
    last_modified: Optional[datetime] = None
    #: A unique identifier for the Webex organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None


class OrganizationsSpaceClassificationCollectionResponse(ApiModel):
    items: Optional[list[HydraClassification]] = None
