from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ClientTypeDistributionTrend1', 'ClienttypedistributionCollectionforOrg',
           'ClusterClientTypeDistributionBlr1', 'ClusterClientTypeDistributionDetailsBlr1a',
           'VideoMeshClientTypeDistributionAPIApi']


class ClusterClientTypeDistributionDetailsBlr1a(ApiModel):
    #: The type of device.
    #: example: sipEndpoint
    device_type: Optional[str] = None
    #: The description of the device type.
    #: example: SIP Devices
    description: Optional[str] = None
    #: The count of the device type.
    #: example: 10
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


class VideoMeshClientTypeDistributionAPIApi(ApiChild, base='videoMesh/clientTypeDistribution'):
    """
    Video Mesh Client Type Distribution API
    
    Video Mesh Developer APIs enable organization admins to view Client Type Distribution details from the Developer
    Portal or their own monitoring application.
    
    <br>
    
    <b>NOTE:</b> The APIs will return data for all device types if the "deviceType" request parameter is empty.
    
    <br>
    
    To obtain the Organization ID needed for these APIs, use the `Organizations API
    <https://developer.webex.com/docs/api/v1/organizations/list-organizations>`_.
    """

    def list_cluster_client_type_distribution_details(self, org_id: str, from_: Union[str, datetime], to_: Union[str,
                                                      datetime],
                                                      device_type: str) -> list[ClienttypedistributionCollectionforOrg]:
        """
        List Cluster Client Type Distribution details

        Returns the client type distribution details for all Video Mesh clusters in an organization.

        :param org_id: Unique ID of the organization.
        :type org_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param device_type: Device type(s).

        - Possible values:
        `webexDevices` `webexAppVdi` `webexForMobile` `sipEndpoint` `webexForDesktop`
        :type device_type: str
        :rtype: list[ClienttypedistributionCollectionforOrg]
        """
        params = {}
        params['orgId'] = org_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['deviceType'] = device_type
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClienttypedistributionCollectionforOrg]).validate_python(data['items'])
        return r

    def get_cluster_client_type_distribution_details(self, cluster_id: str, from_: Union[str, datetime],
                                                     to_: Union[str, datetime],
                                                     device_type: str) -> list[ClienttypedistributionCollectionforOrg]:
        """
        Get Cluster Client Type Distribution details

        Returns the client type distribution details for a single Video Mesh cluster.

        :param cluster_id: Unique ID of the Video Mesh cluster.
        :type cluster_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param device_type: Device type(s).

        - Possible values:
        `webexDevices` `webexAppVdi` `webexForMobile` `sipEndpoint` `webexForDesktop`
        :type device_type: str
        :rtype: list[ClienttypedistributionCollectionforOrg]
        """
        params = {}
        params['clusterId'] = cluster_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['deviceType'] = device_type
        url = self.ep('clusters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClienttypedistributionCollectionforOrg]).validate_python(data['items'])
        return r
