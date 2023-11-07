from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ClientTypeDistributionTrend1', 'ClienttypedistributionCollectionforOrg', 'ClienttypedistributionforOrg',
            'ClusterClientTypeDistributionBlr1', 'ClusterClientTypeDistributionDetailsBlr1a']


class ClusterClientTypeDistributionDetailsBlr1a(ApiModel):
    #: The type of device.
    #: example: sipEndpoint
    device_type: Optional[str] = None
    #: The description of the device type.
    #: example: SIP Devices
    description: Optional[str] = None
    #: The count of the device type.
    #: example: 10.0
    count: Optional[int] = None


class ClusterClientTypeDistributionBlr1(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOWZkOTg
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: Bangalore
    cluster_name: Optional[str] = None
    #: Client Type Distribution Details.
    client_type_distribution_details: Optional[list[ClusterClientTypeDistributionDetailsBlr1a]] = None


class ClientTypeDistributionTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterClientTypeDistributionBlr1]] = None


class ClienttypedistributionCollectionforOrg(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    org_id: Optional[str] = None
    #: Start date and time (inclusive) for the Client Type Distribution details.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the Client Type Distribution details.
    #: example: 2022-03-24T10:22:03Z
    to_: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregation_interval: Optional[datetime] = None
    #: Client Type Distribution details for the organization.
    items: Optional[list[ClientTypeDistributionTrend1]] = None


class ClienttypedistributionforOrg(ApiModel):
    items: Optional[list[ClienttypedistributionCollectionforOrg]] = None
