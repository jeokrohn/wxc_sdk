from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DurationMetric', 'RawMetric', 'WorkspaceDurationMetricsResponse',
            'WorkspaceDurationMetricsResponseAggregation', 'WorkspaceDurationMetricsResponseMeasurement',
            'WorkspaceMetricsApi', 'WorkspaceMetricsResponse', 'WorkspaceMetricsResponseAggregation',
            'WorkspaceMetricsResponseMetricName', 'WorkspaceMetricsResponseSortBy', 'WorkspaceMetricsResponseUnit']


class RawMetric(ApiModel):
    #: ID of the device reporting the metric.
    #: example: Y2lzY29zcGFyazovM4dz09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    device_id: Optional[str] = None
    #: Timestamp of the measurement (ISO 8601).
    #: example: 2021-10-21T13:00:00
    timestamp: Optional[datetime] = None
    #: The measurement value.
    #: example: 5
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
    #: example: 13
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

    def workspace_metrics(self, workspace_id: str, metric_name: WorkspaceMetricsResponseMetricName,
                          aggregation: WorkspaceMetricsResponseAggregation = None, from_: Union[str, datetime] = None,
                          to_: Union[str, datetime] = None, unit: WorkspaceMetricsResponseUnit = None,
                          sort_by: WorkspaceMetricsResponseSortBy = None) -> WorkspaceMetricsResponse:
        """
        Workspace Metrics

        Get metric data for the specified workspace and metric name, optionally aggregated over a specified time
        period.

        * The `workspaceId` and `metricName` parameters indicate which workspace to fetch metrics for and what kind of
        metrics to get.

        * When executing an aggregated query, the result bucket start times will be truncated to the start of an hour
        or a day, depending on
        the aggregation interval. However, the buckets will not contain data from outside the requested time range. For
        example, when
        passing `from=2020-10-21T10:34:56.000Z` and `aggregation=hourly`, the first output bucket would start at
        `2020-10-21T10:00:00.000Z`,
        but the bucket would only aggregate data timestamped after `10:34:56`.

        * For aggregation modes `none` and `hourly`, the maximum time span is 48 hours. For aggregation mode `daily`,
        the maximum
        time span is 30 days.

        :param workspace_id: ID of the workspace to get metrics for.
        :type workspace_id: str
        :param metric_name: The type of data to extract.
        :type metric_name: WorkspaceMetricsResponseMetricName
        :param aggregation: Time unit over which to aggregate measurements.
        :type aggregation: WorkspaceMetricsResponseAggregation
        :param from_: List only data points after a specific date and time (ISO 8601 timestamp)
        :type from_: Union[str, datetime]
        :param to_: List data points before a specific date and time (ISO 8601 timestamp)
        :type to_: Union[str, datetime]
        :param unit: Output data unit (only a valid parameter if `metricName` is `temperature`).
        :type unit: WorkspaceMetricsResponseUnit
        :param sort_by: Sort results.
        :type sort_by: WorkspaceMetricsResponseSortBy
        :rtype: :class:`WorkspaceMetricsResponse`
        """
        params = {}
        params['workspaceId'] = workspace_id
        params['metricName'] = metric_name
        if aggregation is not None:
            params['aggregation'] = aggregation
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if unit is not None:
            params['unit'] = unit
        if sort_by is not None:
            params['sortBy'] = sort_by
        url = self.ep('Metrics')
        data = super().get(url, params=params)
        r = WorkspaceMetricsResponse.model_validate(data)
        return r

    def workspace_duration_metrics(self, workspace_id: str,
                                   aggregation: WorkspaceDurationMetricsResponseAggregation = None,
                                   measurement: WorkspaceDurationMetricsResponseMeasurement = None, from_: Union[str,
                                   datetime] = None, to_: Union[str,
                                   datetime] = None) -> WorkspaceDurationMetricsResponse:
        """
        Workspace Duration Metrics

        Get metrics for how much time a workspace has been in the state given by the `measurement` parameter.

        For example, if the measurement is  `timeBooked` then the duration for which the workspace has been booked is
        returned. The `workspaceId` parameter indicates which workspace to fetch metrics for. If no `measurement` is
        given, the default value is `timeUsed`.

        * When executing a query, the result bucket start times will default to the start of an hour or a day,
        depending on
        the aggregation interval. However, the buckets will not contain data from outside the requested time range. For
        example, when
        passing `from=2020-10-21T10:34:56.000Z` and `aggregation=hourly`, the first output bucket would start at
        `2020-10-21T10:00:00.000Z`,
        but the bucket would only aggregate data timestamped after `10:34:56`.

        * For aggregation mode `hourly`, the maximum time span is 48 hours. For aggregation mode `daily`, the maximum
        time span is 30 days.

        :param workspace_id: ID of the workspace to get metrics for.
        :type workspace_id: str
        :param aggregation: Unit of time over which to aggregate measurements.
        :type aggregation: WorkspaceDurationMetricsResponseAggregation
        :param measurement: The measurement to return duration for.
        :type measurement: WorkspaceDurationMetricsResponseMeasurement
        :param from_: Include data points after a specific date and time (ISO 8601 timestamp).
        :type from_: Union[str, datetime]
        :param to_: Include data points before a specific date and time (ISO 8601 timestamp).
        :type to_: Union[str, datetime]
        :rtype: :class:`WorkspaceDurationMetricsResponse`
        """
        params = {}
        params['workspaceId'] = workspace_id
        if aggregation is not None:
            params['aggregation'] = aggregation
        if measurement is not None:
            params['measurement'] = measurement
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep('DurationMetrics')
        data = super().get(url, params=params)
        r = WorkspaceDurationMetricsResponse.model_validate(data)
        return r
