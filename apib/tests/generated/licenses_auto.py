from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['License', 'LicenseCollectionResponse', 'LicenseSiteType']


class LicenseSiteType(str, Enum):
    #: The site is managed by Webex Control Hub.
    control_hub_managed_site = 'Control Hub managed site'
    #: The site is a linked site.
    linked_site = 'Linked site'
    #: The site is managed by Site Administration.
    site_admin_managed_site = 'Site Admin managed site'


class License(ApiModel):
    #: A unique identifier for the license.
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the licensed feature.
    #: example: Meeting - Webex Meeting Center
    name: Optional[str] = None
    #: Total number of license units allocated.
    #: example: 50.0
    total_units: Optional[int] = None
    #: Total number of license units consumed.
    #: example: 5.0
    consumed_units: Optional[int] = None
    #: The subscription ID associated with this license. This ID is used in other systems, such as Webex Control Hub.
    #: example: Sub-hydraOct26a
    subscription_id: Optional[str] = None
    #: The Webex Meetings site associated with this license.
    #: example: site1-example.webex.com
    site_url: Optional[str] = None
    #: The type of site associated with this license.
    #: example: Control Hub managed site
    site_type: Optional[LicenseSiteType] = None


class LicenseCollectionResponse(ApiModel):
    items: Optional[list[License]] = None
