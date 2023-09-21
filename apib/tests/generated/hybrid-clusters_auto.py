from datetime import datetime
from typing import Optional

from pydantic import Field

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
