from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AggregatedMetric', 'DurationMetric', 'RawMetric', 'WorkspaceDurationMetricsResponse', 'WorkspaceDurationMetricsResponseAggregation', 'WorkspaceDurationMetricsResponseMeasurement', 'WorkspaceMetricsResponse', 'WorkspaceMetricsResponseAggregation', 'WorkspaceMetricsResponseMetricName', 'WorkspaceMetricsResponseSortBy', 'WorkspaceMetricsResponseUnit']


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
    max: Optional[int] = None


class RawMetric(ApiModel):
    #: ID of the device reporting the metric.
    #: example: Y2lzY29zcGFyazovM4dz09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    deviceId: Optional[str] = None
    #: Timestamp of the measurement (ISO 8601).
    #: example: 2021-10-21T13:00:00
    timestamp: Optional[datetime] = None
    #: The measurement value.
    #: example: 5.1
    value: Optional[int] = None


class WorkspaceMetricsResponseMetricName(str, Enum):
    soundlevel = 'soundLevel'
    ambientnoise = 'ambientNoise'
    temperature = 'temperature'
    humidity = 'humidity'
    tvoc = 'tvoc'
    peoplecount = 'peopleCount'


class WorkspaceMetricsResponseAggregation(str, Enum):
    none_ = 'none'
    hourly = 'hourly'
    daily = 'daily'


class WorkspaceMetricsResponseUnit(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'


class WorkspaceMetricsResponseSortBy(str, Enum):
    newestfirst = 'newestFirst'
    oldestfirst = 'oldestFirst'


class WorkspaceMetricsResponse(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    workspaceId: Optional[str] = None
    #: example: temperature
    metricName: Optional[WorkspaceMetricsResponseMetricName] = None
    #: example: hourly
    aggregation: Optional[WorkspaceMetricsResponseAggregation] = None
    #: example: 2020-10-21T13:33:37.789Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: example: 2020-10-31T16:00:00.532Z
    to: Optional[datetime] = None
    #: Output data unit (only present if `metricName` is `temperature`).
    #: example: celsius
    unit: Optional[WorkspaceMetricsResponseUnit] = None
    #: example: newestFirst
    sortBy: Optional[WorkspaceMetricsResponseSortBy] = None
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
    timeused = 'timeUsed'
    timebooked = 'timeBooked'


class WorkspaceDurationMetricsResponse(ApiModel):
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    workspaceId: Optional[str] = None
    #: example: hourly
    aggregation: Optional[WorkspaceDurationMetricsResponseAggregation] = None
    #: example: timeBooked
    measurement: Optional[WorkspaceDurationMetricsResponseMeasurement] = None
    #: example: 2020-10-21T13:33:37.789Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: example: 2020-10-31T16:00:00.532Z
    to: Optional[datetime] = None
    #: The time unit.
    #: example: minutes
    unit: Optional[str] = None
    items: Optional[list[DurationMetric]] = None
