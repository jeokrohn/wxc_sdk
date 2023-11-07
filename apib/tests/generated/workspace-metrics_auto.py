from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AggregatedMetric', 'DurationMetric', 'RawMetric', 'WorkspaceDurationMetricsResponse',
            'WorkspaceDurationMetricsResponseAggregation', 'WorkspaceDurationMetricsResponseMeasurement',
            'WorkspaceMetricsResponse', 'WorkspaceMetricsResponseAggregation', 'WorkspaceMetricsResponseMetricName',
            'WorkspaceMetricsResponseSortBy', 'WorkspaceMetricsResponseUnit']


class AggregatedMetric(ApiModel):
    #: Timestamp indicating the start of the aggregation bucket (ISO 8601).
    #: example: 2021-10-21T12:00:00
    start: Optional[datetime] = None
    #: Timestamp indicating the end of the aggregation bucket (ISO 8601).
    #: example: 2021-10-21T13:00:00
    end: Optional[datetime] = None
    #: The mean measurement value in the bucket.
    #: example: 12.3
    mean: Optional[int] = None
    #: The lowest measurement value in the bucket.
    #: example: 5.1
    min: Optional[int] = None
    #: The highest measurement value in the bucket.
    #: example: 8.8
    max_: Optional[int] = None


class RawMetric(ApiModel):
    #: ID of the device reporting the metric.
    #: example: Y2lzY29zcGFyazovM4dz09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    device_id: Optional[str] = None
    #: Timestamp of the measurement (ISO 8601).
    #: example: 2021-10-21T13:00:00
    timestamp: Optional[datetime] = None
    #: The measurement value.
    #: example: 5.1
    value: Optional[int] = None


class WorkspaceMetricsResponseMetricName(str, Enum):
    sound_level = 'soundLevel'
    ambient_noise = 'ambientNoise'
    temperature = 'temperature'
    humidity = 'humidity'
    tvoc = 'tvoc'
    people_count = 'peopleCount'


class WorkspaceMetricsResponseAggregation(str, Enum):
    none_ = 'none'
    hourly = 'hourly'
    daily = 'daily'


class WorkspaceMetricsResponseUnit(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'


class WorkspaceMetricsResponseSortBy(str, Enum):
    newest_first = 'newestFirst'
    oldest_first = 'oldestFirst'


class WorkspaceMetricsResponse(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    workspace_id: Optional[str] = None
    #: example: temperature
    metric_name: Optional[WorkspaceMetricsResponseMetricName] = None
    #: example: hourly
    aggregation: Optional[WorkspaceMetricsResponseAggregation] = None
    #: example: 2020-10-21T13:33:37.789Z
    from_: Optional[datetime] = None
    #: example: 2020-10-31T16:00:00.532Z
    to_: Optional[datetime] = None
    #: Output data unit (only present if `metricName` is `temperature`).
    #: example: celsius
    unit: Optional[WorkspaceMetricsResponseUnit] = None
    #: example: newestFirst
    sort_by: Optional[WorkspaceMetricsResponseSortBy] = None
    items: Optional[list[RawMetric]] = None


class DurationMetric(ApiModel):
    #: Timestamp indicating the start of the aggregation bucket (ISO 8601).
    #: example: 2021-10-21T12:00:00Z
    start: Optional[datetime] = None
    #: Timestamp indicating the end of the aggregation bucket (ISO 8601).
    #: example: 2021-10-21T13:00:00Z
    end: Optional[datetime] = None
    #: The time duration (in a given state) in the bucket.
    #: example: 13.0
    duration: Optional[int] = None


class WorkspaceDurationMetricsResponseAggregation(str, Enum):
    hourly = 'hourly'
    daily = 'daily'


class WorkspaceDurationMetricsResponseMeasurement(str, Enum):
    time_used = 'timeUsed'
    time_booked = 'timeBooked'


class WorkspaceDurationMetricsResponse(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    workspace_id: Optional[str] = None
    #: example: hourly
    aggregation: Optional[WorkspaceDurationMetricsResponseAggregation] = None
    #: example: timeBooked
    measurement: Optional[WorkspaceDurationMetricsResponseMeasurement] = None
    #: example: 2020-10-21T13:33:37.789Z
    from_: Optional[datetime] = None
    #: example: 2020-10-31T16:00:00.532Z
    to_: Optional[datetime] = None
    #: The time unit.
    #: example: minutes
    unit: Optional[str] = None
    items: Optional[list[DurationMetric]] = None


class WorkspaceMetricsApi(ApiChild, base='workspace'):
    """
    Workspace Metrics
    
    Workspace metrics contain various measurements, such as sound level or temperature, collected by devices in a
    workspace.
    
    Getting the workspace metrics in an organization requires an administrator auth token with the
    `spark-admin:workspace_metrics_read` scope.
    """
    ...