from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Cluster', 'ClusterCollection']


class Cluster(ApiModel):
    #: A unique identifier for the cluster.
    #: example: Y2lZY76123abbb
    id: Optional[str] = None
    #: The ID of the organization to which this hybrid cluster belongs.
    #: example: Y2lzY29zcGFyazovL3
    org_id: Optional[str] = None
    #: The name of the cluster.
    #: example: EMEA Oslo 1
    name: Optional[str] = None
    #: The ID of the resource group this cluster belongs to.
    #: example: Y2lzY29zcGFyazovL3
    resource_group_id: Optional[str] = None


class ClusterCollection(ApiModel):
    #: An array of hybrid cluster objects.
    items: Optional[list[Cluster]] = None


class HybridClustersApi(ApiChild, base='hybrid/clusters'):
    """
    Hybrid Clusters
    
    `Hybrid Clusters
    <https://www.cisco.com/c/en/us/solutions/collaboration/webex-hybrid-services/index.html>`_ are groups of hosts, and the connectors these hosts contain, that are managed as a unit.  All the
    connectors of a single type in a cluster share the same configuration.
    
    Listing and viewing Hybrid Clusters requires an administrator auth token with the
    `spark-admin:hybrid_clusters_read` scope.
    
    Hybrid Clusters are associated with Resource Groups. See the `Resource Groups API
    <https://developer.webex.com/docs/api/v1/resource-groups>`_ for more information.
    """
    ...