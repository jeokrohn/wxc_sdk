from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BandwidthTest', 'BlrClusterDetails', 'BlrNode1', 'BlrNodeLocation', 'BulkUpdateEventThresholdResponse',
           'ClientTypeDistributionTrend1', 'ClienttypedistributionCollectionforOrg', 'CloudOverflowTrend1',
           'ClusterAvailability', 'ClusterAvailabilityCollection', 'ClusterAvailableTimeline',
           'ClusterClientTypeDistributionBlr1', 'ClusterClientTypeDistributionDetailsBlr1a',
           'ClusterDetailsCollection', 'ClusterRedirectBlr1', 'ClusterRedirectDetailsBlr1a',
           'ClusterUpgradeScheduleBlr', 'ClusterUtilizationCollection', 'ClusterUtilizationT1SJ',
           'ClusterUtilizationTrend1', 'ConnectivityTestResultsClustersObject1', 'ConnectivityTestResultsForNode',
           'ConnectivityTestResultsObject', 'FailureDetails3', 'GetEntityThresholdConfig1',
           'GetEventThresholdResponse', 'ListEventThresholdConfigurationEventName',
           'ListEventThresholdConfigurationEventScope', 'ListMediaHealthMonitoringToolTestResultsV2TriggerType',
           'MediaHealthMonitoringResultsCollectionfororganization', 'MediaHealthMonitoringTestResultsFailure',
           'MediaHealthMonitoringclusters', 'MediaHealthMonitoringforfirstcluster', 'MediaHealthMonitoringsecondnode',
           'MediaSignallingtestResultFailure', 'NodeAvailability', 'NodeAvailabilityCollection',
           'NodeAvailableTimeline', 'NodeStatusList1', 'NodeStatusList1Status', 'OverflowDetails1',
           'OverflowtoCloudCollection', 'PerClusterConnectivityResult1', 'PerNodeConnectivityResult1',
           'ReachabilityTestResultsforcluster', 'ReachabilityTestResultsforfirstcluster',
           'ReachabilityTestresultsStunresults1', 'ReachabilityTestresultsSuccess',
           'ReachabilityTestresultsdestinationcluster', 'ReachabilityTestresultsfirstnode',
           'ReachabilityTestresultsfororganization', 'RedirectCollectionForOrg', 'RedirectTrend1',
           'ServiceTypeResult4', 'SingleNodeAvailability1', 'SingleNodeAvailabilityCollection',
           'SingleNodeAvailableTimeline', 'TriggerOnDemandBodyType', 'TriggeredTestResult', 'TriggeredTestStatus1',
           'UpdateEventThresholdConfig1', 'UpdateEventThresholdConfigurationEventThresholds',
           'UpdateEventThresholdConfigurationEventThresholdsThresholdConfig', 'UtilizationMetricsT1SJ',
           'VideoMeshApi']


class ClusterAvailableTimeline(ApiModel):
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segment_start_time: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segment_end_time: Optional[datetime] = None
    #: Availability information of the Video Mesh cluster.
    #: example: Available
    availability: Optional[str] = None
    #: Number of nodes that are online.
    #: example: 1
    no_of_online_nodes: Optional[int] = None
    #: Number of nodes that are offline.
    #: example: 1
    no_of_offline_nodes: Optional[int] = None
    #: Total number of nodes in the Video Mesh cluster.
    #: example: 2
    total_nodes: Optional[int] = None


class ClusterAvailability(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    cluster_name: Optional[str] = None
    availability_segments: Optional[list[ClusterAvailableTimeline]] = None


class ClusterAvailabilityCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    org_id: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[ClusterAvailability]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to_: Optional[datetime] = None


class NodeAvailableTimeline(ApiModel):
    #: Number of nodes that are online.
    #: example: 1
    no_of_online_nodes: Optional[int] = None
    #: Number of nodes that are offline.
    no_of_offline_nodes: Optional[int] = None
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segment_start_time: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segment_end_time: Optional[datetime] = None
    #: Availability information of the Video Mesh node.
    #: example: Available
    availability: Optional[str] = None
    #: Reason for the Video Mesh node being unavailable (if any).
    #: example: NA
    un_availability_reason: Optional[str] = None
    #: Total number of nodes in the Video Mesh cluster.
    #: example: 1
    total_nodes: Optional[int] = None


class NodeAvailability(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    cluster_name: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    host_name_or_ip: Optional[str] = None
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMWViNjVmZGYtOTY0My00MTdmLTk5NzQtYWQ3MmNhZTBlMTBmOmMyNTk0YmY2NDFmZTRkNTFiZDg3YThiMjYxYzg3NWY1
    node_id: Optional[str] = None
    availability_segments: Optional[list[NodeAvailableTimeline]] = None


class NodeAvailabilityCollection(ApiModel):
    #: Unique ID for a Video Mesh organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    org_id: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[NodeAvailability]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to_: Optional[datetime] = None


class SingleNodeAvailableTimeline(ApiModel):
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segment_start_time: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segment_end_time: Optional[datetime] = None
    #: Availability information of the Video Mesh node.
    #: example: Available
    availability: Optional[str] = None
    #: Reason for the Video Mesh node being unavailable (if any).
    #: example: NA
    un_availability_reason: Optional[str] = None


class SingleNodeAvailability1(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    cluster_name: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    host_name_or_ip: Optional[str] = None
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMWViNjVmZGYtOTY0My00MTdmLTk5NzQtYWQ3MmNhZTBlMTBmOmMyNTk0YmY2NDFmZTRkNTFiZDg3YThiMjYxYzg3NWY1
    node_id: Optional[str] = None
    availability_segments: Optional[list[SingleNodeAvailableTimeline]] = None


class SingleNodeAvailabilityCollection(ApiModel):
    #: Unique ID for a Video Mesh organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    org_id: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[SingleNodeAvailability1]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to_: Optional[datetime] = None


class MediaSignallingtestResultFailure(ApiModel):
    #: The name of the test.
    #: example: Media Signalling
    test_name: Optional[str] = None
    #: Test results(Success/Failed).
    #: example: Failed
    test_result: Optional[str] = None
    #: Reason for test failure.
    #: example: An internal error occurred in monitoring tool [Error Code:1003]. If the issue persists, please contact Cisco Support.
    failure_reason: Optional[str] = None


class MediaHealthMonitoringTestResultsFailure(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    id: Optional[str] = None
    #: Test results of Media Signalling, SIP Signalling, Media Cascade runs.
    test_results: Optional[list[MediaSignallingtestResultFailure]] = None


class MediaHealthMonitoringsecondnode(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    node_id: Optional[str] = None
    #: Host name or the IP of the Video Mesh node.
    #: example: abc.company.com
    host_name_or_ip: Optional[str] = Field(alias='hostNameOrIP', default=None)
    #: The Media Health Monitoring Tool test results for a single Video Mesh node.
    mhm_test_results: Optional[list[MediaHealthMonitoringTestResultsFailure]] = None


class MediaHealthMonitoringforfirstcluster(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: banglore
    cluster_name: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[MediaHealthMonitoringsecondnode]] = None


class MediaHealthMonitoringclusters(ApiModel):
    #: The list of Video Mesh clusters.
    clusters: Optional[list[MediaHealthMonitoringforfirstcluster]] = None


class MediaHealthMonitoringResultsCollectionfororganization(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    org_id: Optional[str] = None
    #: Start date and time (inclusive) of the Media Health Monitoring Tool data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the Media Health Monitoring Tool data.
    #: example: 2023-01-20T15:53:00Z
    to_: Optional[datetime] = None
    #: Media Health Monitoring Tool test results.
    items: Optional[list[MediaHealthMonitoringclusters]] = None


class OverflowDetails1(ApiModel):
    #: The reason for this overflow.
    #: example: Capacity exceeded
    overflow_reason: Optional[str] = None
    #: Number of overflows.
    #: example: 25
    overflow_count: Optional[int] = None
    #: Any possible remediations for this overflow.
    #: example: Video Mesh exceeded its capacity. If this happens frequently, consider adding more nodes to your clusters.
    possible_remediation: Optional[str] = None


class CloudOverflowTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    #: Overflow Details.
    overflow_details: Optional[list[OverflowDetails1]] = None


class OverflowtoCloudCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    org_id: Optional[str] = None
    #: Start date and time (inclusive) for the Overflow to Cloud data.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) for the Overflow to Cloud data.
    #: example: 2022-03-24T04:22:03Z
    to_: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregation_interval: Optional[datetime] = None
    #: Overflow data for the organization.
    items: Optional[list[CloudOverflowTrend1]] = None


class ClusterRedirectDetailsBlr1a(ApiModel):
    #: The reason for the redirect.
    #: example: Capacity exceeded
    redirect_reason: Optional[str] = None
    #: Number of Call Redirects.
    #: example: 10
    redirect_count: Optional[int] = None
    #: Any possible remediations for this overflow.
    #: example: Video Mesh exceeded its capacity. If this happens frequently, consider adding more nodes to your clusters.
    possible_remediation: Optional[str] = None


class ClusterRedirectBlr1(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOWZkOTg
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: bangalore
    cluster_name: Optional[str] = None
    #: Call Redirect Details.
    redirect_details: Optional[list[ClusterRedirectDetailsBlr1a]] = None


class RedirectTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterRedirectBlr1]] = None


class RedirectCollectionForOrg(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    org_id: Optional[str] = None
    #: Start date and time (inclusive) for the Call Redirect details.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the Call Redirect details.
    #: example: 2022-03-24T10:22:03Z
    to_: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregation_interval: Optional[datetime] = None
    #: Redirect details for the organization.
    items: Optional[list[RedirectTrend1]] = None


class UtilizationMetricsT1SJ(ApiModel):
    #: Peak CPU usage during the time interval.
    #: example: 54
    peak_cpu: Optional[int] = None
    #: Average CPU usage during the time interval.
    #: example: 4
    avg_cpu: Optional[int] = None
    #: Maximum active calls at a point in the time interval.
    #: example: 5
    active_calls: Optional[int] = None
    #: Maximum active private calls at a point in the time interval.
    #: example: 1
    active_private_calls: Optional[int] = None


class ClusterUtilizationT1SJ(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOTEyMzQ=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: sanjose
    cluster_name: Optional[str] = None
    #: Utilization details for the cluster in the time interval.
    utilization_metrics: Optional[UtilizationMetricsT1SJ] = None


class ClusterUtilizationTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterUtilizationT1SJ]] = None


class ClusterUtilizationCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    org_id: Optional[str] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregation_interval: Optional[datetime] = None
    #: Start date and time (inclusive) of the utilization data.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the utilization data.
    #: example: 2022-03-24T10:22:03Z
    to_: Optional[datetime] = None
    #: Utilization details of the Video Mesh cluster
    items: Optional[list[ClusterUtilizationTrend1]] = None


class ReachabilityTestresultsSuccess(ApiModel):
    #: Destination IP address.
    #: example: 1.1.1.1
    ip_address: Optional[str] = None
    #: Port number.
    #: example: 5004
    port: Optional[int] = None
    #: Port reachability information.
    #: example: True
    reachable: Optional[bool] = None


class ReachabilityTestresultsStunresults1(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: The type of the test being executed. Can be either `OnDemand` or `Periodic`.
    #: example: OnDemand
    trigger_type: Optional[str] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    id: Optional[str] = None
    #: List of UDP ports being checked in Reachability test.
    udp: Optional[list[ReachabilityTestresultsSuccess]] = None
    #: List of TCP ports being checked in Reachability test.
    tcp: Optional[list[ReachabilityTestresultsSuccess]] = None


class ReachabilityTestresultsdestinationcluster(ApiModel):
    #: Cloud Webex cluster against which Reachability test is being executed.
    #: example: Amsterdam Cluster
    destination_cluster: Optional[str] = None
    #: STUN test results for a Video Mesh cluster.
    stun_results: Optional[list[ReachabilityTestresultsStunresults1]] = None


class ReachabilityTestresultsfirstnode(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    node_id: Optional[str] = None
    #: Host name or the IP of the Video Mesh node.
    #: example: xyz.company.com
    host_name_or_ip: Optional[str] = Field(alias='hostNameOrIP', default=None)
    #: Reachability test results for a single Video Mesh node.
    test_results: Optional[list[ReachabilityTestresultsdestinationcluster]] = None


class ReachabilityTestResultsforfirstcluster(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: banglore
    cluster_name: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[ReachabilityTestresultsfirstnode]] = None


class ReachabilityTestResultsforcluster(ApiModel):
    #: List of Video Mesh clusters.
    clusters: Optional[list[ReachabilityTestResultsforfirstcluster]] = None


class ReachabilityTestresultsfororganization(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    org_id: Optional[str] = None
    #: Start date and time (inclusive) of the Reachability test results data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the Reachability test results data.
    #: example: 2023-01-20T15:53:00Z
    to_: Optional[datetime] = None
    #: Reachability test results data.
    items: Optional[list[ReachabilityTestResultsforcluster]] = None


class BlrNodeLocation(ApiModel):
    #: Country code of the Location where the Video Mesh node is deployed.
    #: example: IN
    country_code: Optional[str] = None
    #: City where Video Mesh node is deployed.
    #: example: Bangalore
    city: Optional[str] = None
    #: Time zone in which the Video Mesh node is deployed.
    #: example: Asia/Kolkata
    time_zone: Optional[str] = None


class BlrNode1(ApiModel):
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo0NjdiNGIxZC1jZWI2LTQwN2EtYWZmOC1mMjIxZmFiNzhjNzI
    node_id: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    host_name_or_ip: Optional[str] = None
    #: Deployment Type of the Video Mesh node.
    #: example: Video Mesh Node Lite
    deployment_type: Optional[str] = None
    #: Location details of the Video Mesh node.
    location: Optional[BlrNodeLocation] = None


class ClusterUpgradeScheduleBlr(ApiModel):
    #: Days of the week when scheduled upgrades will occur for the Video Mesh cluster.
    #: example: ['sunday', 'monday', 'tuesday']
    schedule_days: Optional[list[str]] = None
    #: Time when scheduled upgrade will occur for the Video Mesh cluster.
    #: example: 02:00
    schedule_time: Optional[datetime] = None
    #: Timezone of the scheduled upgrade of Video Mesh cluster.
    #: example: Asia/Kolkata
    schedule_time_zone: Optional[str] = None
    #: Upgrade Pending information.
    #: example: True
    upgrade_pending: Optional[bool] = None
    #: Time when the next upgrade is scheduled for the Video Mesh cluster.
    #: example: 2020-03-25T20:30:00Z
    next_upgrade_time: Optional[datetime] = None


class BlrClusterDetails(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: Bangalore
    cluster_name: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[BlrNode1]] = None
    #: Release Channel of the Video Mesh cluster.
    #: example: alpha
    release_channel: Optional[str] = None
    #: Upgrade Schedule details of the Video Mesh cluster.
    upgrade_schedule: Optional[ClusterUpgradeScheduleBlr] = None


class ClusterDetailsCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    org_id: Optional[str] = None
    #: Details of all the clusters of the organization.
    items: Optional[list[BlrClusterDetails]] = None


class TriggeredTestResult(ApiModel):
    #: Test type of the command ID.
    #: example: MediaHealthMonitorTest
    type: Optional[str] = None
    #: The unique ID for the test being executed.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    command_id: Optional[str] = None
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    org_id: Optional[str] = None
    results: Optional[list[MediaHealthMonitoringclusters]] = None


class NodeStatusList1Status(str, Enum):
    dispatched = 'Dispatched'
    completed = 'Completed'
    errored = 'Errored'


class NodeStatusList1(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    node_id: Optional[str] = None
    #: Status of the test triggered.
    #: example: Dispatched
    status: Optional[NodeStatusList1Status] = None


class TriggeredTestStatus1(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    org_id: Optional[str] = None
    #: The unique ID of the test being executed.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    command_id: Optional[str] = None
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    cluster_id: Optional[str] = None
    nodes: Optional[list[NodeStatusList1]] = None


class TriggerOnDemandBodyType(str, Enum):
    #: Used to test whether the media ports within the Video Mesh node are open, and whether the Video Mesh node is
    #: able to reach the cloud clusters pertaining to the media containers via those ports.
    reachability_test = 'ReachabilityTest'
    #: Used to test the network environment of the Video Mesh node by running various connectivity, bandwidth, and DNS
    #: resolution tests against Webex Cloud and ThirdParty Cloud (Docker) services.
    network_test = 'NetworkTest'
    #: Used to test the meetings and call health of Video Mesh nodes using signalling and cascading methods.
    media_health_monitor_test = 'MediaHealthMonitorTest'


class FailureDetails3(ApiModel):
    #: Possible reasons for failure for the test.
    #: example: ['Degraded Network Bandwidth speed detected in the Video Mesh Node connectivity to the Webex Cloud [Error Code: 1402,1405].']
    possible_failure_reason: Optional[list[str]] = None
    #: Possible fixes for the failures mentioned above.
    #: example: ['Please refer to Video Mesh deployment guide to ensure the network settings are configured correctly, and the minimum internet speed requirements are met. If the issue persists, please contact Cisco Support.']
    possible_remediation: Optional[list[str]] = None


class ServiceTypeResult4(ApiModel):
    #: Service for which the test was executed.
    #: example: WebexCloud
    service_type: Optional[str] = None
    #: Result of the test executed.
    #: example: Failed
    test_result: Optional[str] = None
    failure_details: Optional[FailureDetails3] = None


class BandwidthTest(ApiModel):
    #: The type of test result.
    #: example: BandwidthTest
    type: Optional[str] = None
    #: Test Results from different services.
    results: Optional[list[ServiceTypeResult4]] = None


class ConnectivityTestResultsForNode(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: The type of the test being executed. Can be either `OnDemand` or `Periodic`.
    #: example: OnDemand
    trigger_type: Optional[str] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0NPTU1BTkRJRC8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY6YWRlODhhNjAtMzk5Mi0xMWVkLTlhYmQtYzUyMjRiZjNjMzQ4
    id: Optional[str] = None
    result: Optional[list[BandwidthTest]] = None


class PerNodeConnectivityResult1(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    node_id: Optional[str] = None
    #: Host name or IP Address of the Video Mesh node.
    #: example: abc.company.com
    host_name_or_ip: Optional[str] = Field(alias='hostNameOrIP', default=None)
    test_results: Optional[list[ConnectivityTestResultsForNode]] = None


class PerClusterConnectivityResult1(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    cluster_id: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: sanjose
    cluster_name: Optional[str] = None
    nodes: Optional[list[PerNodeConnectivityResult1]] = None


class ConnectivityTestResultsClustersObject1(ApiModel):
    #: List of Video Mesh clusters.
    clusters: Optional[list[PerClusterConnectivityResult1]] = None


class ConnectivityTestResultsObject(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    org_id: Optional[str] = None
    #: Start date and time (inclusive) of the Network Test data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = None
    #: End date and time (inclusive) of the Network Test data.
    #: example: 2023-01-20T15:53:00Z
    to_: Optional[datetime] = None
    #: Network test results.
    items: Optional[list[ConnectivityTestResultsClustersObject1]] = None


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


class UpdateEventThresholdConfig1(ApiModel):
    #: Threshold value (in percentage) to trigger an event.
    #: example: 40
    min_threshold: Optional[int] = None
    #: Deafault Threshold value (in percentage) to trigger an event.
    #: example: 10
    default_min_threshold: Optional[int] = None


class GetEntityThresholdConfig1(ApiModel):
    #: Name of the event.
    #: example: clusterCallsRedirected
    event_name: Optional[str] = None
    #: Unique ID of the event threshold configuration.
    #: example: Y2lzY29zcGFyazovL3VzL0VWRU5ULzQyN2U5ZTk2LTczYTctNDYwYS04MGZhLTcyNWU4MWE2MDg3Zjo2YzJhZGRmMS0wYjAzLTRiZWEtYjIxYy0xYzFjYzdiY2UwOWQ
    event_threshold_id: Optional[str] = None
    #: The `eventScope` is scope of event.
    #: example: CLUSTER
    event_scope: Optional[str] = None
    #: The `entityId` is the unique ID of the Organization or the unique ID of the Video Mesh Cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzRiNTk5NzkwLWVlMzctMTFlZC1hMDViLTAyNDJhYzEyMDAwMzo2NjMxOTMyNC1lZTM3LTExZWQtYTA1Yi0wMjQyYWMxMjAwMDM
    entity_id: Optional[str] = None
    #: Threshold configuration of an `entityId`.
    threshold_config: Optional[UpdateEventThresholdConfig1] = None


class GetEventThresholdResponse(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ
    org_id: Optional[str] = None
    event_thresholds: Optional[list[GetEntityThresholdConfig1]] = None


class BulkUpdateEventThresholdResponse(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ
    org_id: Optional[str] = None
    #: List of successful updated response
    event_thresholds: Optional[list[GetEntityThresholdConfig1]] = None
    #: List of failed or invalid event threshold IDs.
    #: example: ['Y2lzY29zcGFyazovL3VzL0VWRU5ULzQyN2U5ZTk2LTczYTctNDYwYS04MGZhLTcyNWU4MWE2MDg3ZjowM2ZkYjkzZC1jNTllLTQzMjQtODIwNS1lNDIyYzA3NGQ5Mzg']
    failed_event_threshold_ids: Optional[list[str]] = None


class ListMediaHealthMonitoringToolTestResultsV2TriggerType(str, Enum):
    on_demand = 'OnDemand'
    periodic = 'Periodic'
    all = 'All'


class ListEventThresholdConfigurationEventName(str, Enum):
    cluster_calls_redirected = 'clusterCallsRedirected'
    org_calls_overflowed = 'orgCallsOverflowed'


class ListEventThresholdConfigurationEventScope(str, Enum):
    cluster = 'CLUSTER'
    org = 'ORG'


class UpdateEventThresholdConfigurationEventThresholdsThresholdConfig(ApiModel):
    min_threshold: Optional[int] = None


class UpdateEventThresholdConfigurationEventThresholds(ApiModel):
    event_threshold_id: Optional[str] = None
    threshold_config: Optional[UpdateEventThresholdConfigurationEventThresholdsThresholdConfig] = None


class VideoMeshApi(ApiChild, base='videoMesh'):
    """
    Video Mesh
    
    The Video Mesh Developer APIs provide the ability for organization admins to retrieve analytics and monitoring
    data, trigger on-demand troubleshooting tests (Media Health Monitoring Tool, Network, and Reachability), and
    getting and setting thresholds for Webhook events from the Developer Portal or their own monitoring applications,
    which can help in quickly isolating and identifying root cause of issues affecting the normal functioning of a
    customer's Video Mesh Deployment.
    
    <br/>
    
    <b>NOTE:</b> The Media Health Monitor Test and Reachability Test can be triggered only on clusters that are not
    reserved for private meetings.
    
    <br>
    
    To obtain the Organization ID needed for these APIs, use the `Organizations API
    <https://developer.webex.com/docs/api/v1/organizations/list-organizations>`_
    """

    def list_clusters_availability(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                   org_id: str) -> list[ClusterAvailabilityCollection]:
        """
        List Clusters Availability

        Returns the availability details for all Video Mesh clusters in an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique ID for the organization.
        :type org_id: str
        :rtype: list[ClusterAvailabilityCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('clusters/availability')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClusterAvailabilityCollection]).validate_python(data['items'])
        return r

    def get_cluster_availability(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                 cluster_id: str) -> list[ClusterAvailabilityCollection]:
        """
        Get Cluster Availability

        Returns the availability details of a single Video Mesh cluster in an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh clusterID
        :type cluster_id: str
        :rtype: list[ClusterAvailabilityCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        url = self.ep(f'clusters/availability/{cluster_id}')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClusterAvailabilityCollection]).validate_python(data['items'])
        return r

    def list_node_availability(self, from_: Union[str, datetime], to_: Union[str, datetime],
                               cluster_id: str) -> list[NodeAvailabilityCollection]:
        """
        List Node Availability

        Returns the availability details of all nodes in a Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh cluster ID.
        :type cluster_id: str
        :rtype: list[NodeAvailabilityCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['clusterId'] = cluster_id
        url = self.ep('nodes/availability')
        data = super().get(url, params=params)
        r = TypeAdapter(list[NodeAvailabilityCollection]).validate_python(data['items'])
        return r

    def get_node_availability(self, from_: Union[str, datetime], to_: Union[str, datetime],
                              node_id: str) -> list[SingleNodeAvailabilityCollection]:
        """
        Get Node Availability

        Returns the availability details of a single node in a Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param node_id: The unique Video Mesh node ID.
        :type node_id: str
        :rtype: list[SingleNodeAvailabilityCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        url = self.ep(f'nodes/availability/{node_id}')
        data = super().get(url, params=params)
        r = TypeAdapter(list[SingleNodeAvailabilityCollection]).validate_python(data['items'])
        return r

    def list_media_health_monitoring_tool_results(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                                  org_id: str) -> list[MediaHealthMonitoringResultsCollectionfororganization]:
        """
        List Media Health Monitoring Tool results

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `List Media Health Monitoring Tool Test results V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/list-media-health-monitoring-tool-test-results-v2>`_ for all future projects.</Callout></div>

        Returns the test results of the Media Health Monitoring Tool tests for an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`. `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique Video Mesh organization ID.
        :type org_id: str
        :rtype: list[MediaHealthMonitoringResultsCollectionfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('mediaHealthMonitor')
        data = super().get(url, params=params)
        r = TypeAdapter(list[MediaHealthMonitoringResultsCollectionfororganization]).validate_python(data['items'])
        return r

    def list_media_health_monitoring_tool_test_results_v2(self, org_id: str, from_: Union[str, datetime],
                                                          to_: Union[str, datetime],
                                                          trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> MediaHealthMonitoringResultsCollectionfororganization:
        """
        List Media Health Monitoring Tool Test results V2

        Returns the test results of the Media Health Monitoring Tool tests for an organization.

        <br/>

        Changes in V2:

        <br/>

        On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        :param org_id: Unique ID of the organization.
        :type org_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`MediaHealthMonitoringResultsCollectionfororganization`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/mediaHealthMonitorTest')
        data = super().get(url, params=params)
        r = MediaHealthMonitoringResultsCollectionfororganization.model_validate(data)
        return r

    def get_media_health_monitoring_tool_cluster_results(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                                         cluster_id: str) -> list[MediaHealthMonitoringResultsCollectionfororganization]:
        """
        Get Media Health Monitoring Tool Cluster results

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `Get Media Health Monitoring Tool Test results for clusters V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/get-media-health-monitoring-tool-test-results-for-cluster-v2>`_ for all future
        projects.</Callout></div>

        Returns the test results of the Media Health Monitoring Tool tests for a single Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`. `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh Cluster ID.
        :type cluster_id: str
        :rtype: list[MediaHealthMonitoringResultsCollectionfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['clusterId'] = cluster_id
        url = self.ep('mediaHealthMonitor/clusters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[MediaHealthMonitoringResultsCollectionfororganization]).validate_python(data['items'])
        return r

    def get_media_health_monitoring_tool_test_results_for_clusters_v2(self, cluster_id: str, from_: Union[str,
                                                                      datetime], to_: Union[str, datetime],
                                                                      trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> MediaHealthMonitoringResultsCollectionfororganization:
        """
        Get Media Health Monitoring Tool Test results for clusters V2

        Returns the test results of the Media Health Monitoring Tool tests for a single Video Mesh cluster.

        <br/>

        Changes in V2:

        <br/>

        On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        :param cluster_id: Unique ID of the Video Mesh cluster.
        :type cluster_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`MediaHealthMonitoringResultsCollectionfororganization`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/mediaHealthMonitorTest/clusters')
        data = super().get(url, params=params)
        r = MediaHealthMonitoringResultsCollectionfororganization.model_validate(data)
        return r

    def get_media_health_monitoring_tool_node_results(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                                      node_id: str) -> list[MediaHealthMonitoringResultsCollectionfororganization]:
        """
        Get Media Health Monitoring Tool Node results

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `Get Media Health Monitoring Tool Test results for node V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/get-media-health-monitoring-tool-test-results-for-node-v2>`_ for all future
        projects.</Callout></div>

        Returns the test results of the Media Health Monitoring Tool tests for a single Video Mesh node.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`. `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param node_id: The unique Video Mesh Node ID.
        :type node_id: str
        :rtype: list[MediaHealthMonitoringResultsCollectionfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['nodeId'] = node_id
        url = self.ep('mediaHealthMonitor/nodes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[MediaHealthMonitoringResultsCollectionfororganization]).validate_python(data['items'])
        return r

    def get_media_health_monitoring_tool_test_results_for_node_v2(self, node_id: str, from_: Union[str, datetime],
                                                                  to_: Union[str, datetime],
                                                                  trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> MediaHealthMonitoringResultsCollectionfororganization:
        """
        Get Media Health Monitoring Tool Test results for node V2

        Returns the test results of the Media Health Monitoring Tool tests for a single Video Mesh node.

        <br/>

        Changes in V2:

        <br/>

        On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        :param node_id: Unique ID of the Video Mesh node.
        :type node_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`MediaHealthMonitoringResultsCollectionfororganization`
        """
        params = {}
        params['nodeId'] = node_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['triggerType'] = trigger_type
        url = self.ep('testResults/mediaHealthMonitorTest/nodes')
        data = super().get(url, params=params)
        r = MediaHealthMonitoringResultsCollectionfororganization.model_validate(data)
        return r

    def list_overflow_to_cloud_details(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                       org_id: str) -> list[OverflowtoCloudCollection]:
        """
        List Overflow to Cloud details

        Returns details of overflows to the cloud in an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique Video Mesh organization ID.
        :type org_id: str
        :rtype: list[OverflowtoCloudCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('cloudOverflow')
        data = super().get(url, params=params)
        r = TypeAdapter(list[OverflowtoCloudCollection]).validate_python(data['items'])
        return r

    def list_cluster_redirect_details(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                      org_id: str) -> list[RedirectCollectionForOrg]:
        """
        List Cluster Redirect details

        Returns the redirect details of all Video Mesh clusters in an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique Video Mesh organization ID.
        :type org_id: str
        :rtype: list[RedirectCollectionForOrg]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('callRedirects')
        data = super().get(url, params=params)
        r = TypeAdapter(list[RedirectCollectionForOrg]).validate_python(data['items'])
        return r

    def get_cluster_redirect_details(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                     cluster_id: str) -> list[RedirectCollectionForOrg]:
        """
        Get Cluster Redirect details

        Returns details of cluster redirects for a single Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh Cluster ID.
        :type cluster_id: str
        :rtype: list[RedirectCollectionForOrg]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['clusterId'] = cluster_id
        url = self.ep('clusters/callRedirects')
        data = super().get(url, params=params)
        r = TypeAdapter(list[RedirectCollectionForOrg]).validate_python(data['items'])
        return r

    def list_clusters_utilization(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                  org_id: str) -> list[ClusterUtilizationCollection]:
        """
        List Clusters Utilization

        Returns the utilization details of all Video Mesh clusters in an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique ID for the organization.
        :type org_id: str
        :rtype: list[ClusterUtilizationCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('utilization')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClusterUtilizationCollection]).validate_python(data['items'])
        return r

    def get_cluster_utilization_details(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                        cluster_id: str) -> list[ClusterUtilizationCollection]:
        """
        Get Cluster Utilization details

        Returns the utilization details for a single Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh Cluster ID.
        :type cluster_id: str
        :rtype: list[ClusterUtilizationCollection]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['clusterId'] = cluster_id
        url = self.ep('clusters/utilization')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClusterUtilizationCollection]).validate_python(data['items'])
        return r

    def list_reachability_test_results(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                       org_id: str) -> list[ReachabilityTestresultsfororganization]:
        """
        List Reachability Test results

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `List Reachability Test results V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/list-reachability-test-results-v2>`_ for all future projects.</Callout></div>

        Returns the test results of the Reachability tests for an organization.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`.  `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param org_id: The unique ID for the organization.
        :type org_id: str
        :rtype: list[ReachabilityTestresultsfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['orgId'] = org_id
        url = self.ep('reachabilityTest')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ReachabilityTestresultsfororganization]).validate_python(data['items'])
        return r

    def list_reachability_test_results_v2(self, org_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
                                          trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ReachabilityTestresultsfororganization:
        """
        List Reachability Test results V2

        Returns the test results of the Reachability tests for an organization.

        <br/>

        Changes in V2:

        <br/>

        1. On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        <br/>

        2. You can now view the destination IP address of the destination cluster in the JSON response.

        :param org_id: Unique ID of the organization.
        :type org_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ReachabilityTestresultsfororganization`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/reachabilityTest')
        data = super().get(url, params=params)
        r = ReachabilityTestresultsfororganization.model_validate(data)
        return r

    def get_reachability_test_results_for_cluster(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                                  cluster_id: str) -> list[ReachabilityTestresultsfororganization]:
        """
        Get Reachability Test results for Cluster

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `Get Reachability Test results for cluster V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/get-reachability-test-results-for-cluster-v2>`_ for all future projects.</Callout></div>

        Returns the test results of the Reachability tests for a single Video Mesh cluster.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`. `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param cluster_id: The unique Video Mesh Cluster ID.
        :type cluster_id: str
        :rtype: list[ReachabilityTestresultsfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['clusterId'] = cluster_id
        url = self.ep('reachabilityTest/clusters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ReachabilityTestresultsfororganization]).validate_python(data['items'])
        return r

    def get_reachability_test_results_for_cluster_v2(self, cluster_id: str, from_: Union[str, datetime],
                                                     to_: Union[str, datetime],
                                                     trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ReachabilityTestresultsfororganization:
        """
        Get Reachability Test results for cluster V2

        Returns the test results of the Reachability tests for a single Video Mesh cluster.

        <br/>

        Changes in V2:

        <br/>

        1. On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        <br/>

        2. You can now view the destination IP address of the destination cluster in the JSON response.

        :param cluster_id: Unique ID of the Video Mesh cluster.
        :type cluster_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ReachabilityTestresultsfororganization`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/reachabilityTest/clusters')
        data = super().get(url, params=params)
        r = ReachabilityTestresultsfororganization.model_validate(data)
        return r

    def get_reachability_test_results_for_node(self, from_: Union[str, datetime], to_: Union[str, datetime],
                                               node_id: str) -> list[ReachabilityTestresultsfororganization]:
        """
        Get Reachability Test results for Node

        <div><Callout type="warning"> This API is EOL and will be decommissioned soon. Please start using the
        replacement `Get Reachability Test results for node V2 API
        <https://developer.webex.com/docs/api/v1/video-mesh/get-reachability-test-results-for-node-v2>`_ for all future projects.</Callout></div>

        Returns the test results of the Reachability tests for a single Video Mesh node.

        :param from_: The starting date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot
            be after `to`. `from` must not be older than 1 week.
        :type from_: Union[str, datetime]
        :param to_: The ending date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param node_id: The unique Video Mesh node ID.
        :type node_id: str
        :rtype: list[ReachabilityTestresultsfororganization]
        """
        params = {}
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['nodeId'] = node_id
        url = self.ep('reachabilityTest/nodes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ReachabilityTestresultsfororganization]).validate_python(data['items'])
        return r

    def get_reachability_test_results_for_node_v2(self, node_id: str, from_: Union[str, datetime], to_: Union[str,
                                                  datetime],
                                                  trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ReachabilityTestresultsfororganization:
        """
        Get Reachability Test results for node V2

        Returns the test results of the Reachability tests for a single Video Mesh node.

        <br/>

        Changes in V2:

        <br/>

        1. On-demand test results can be obtained along with the periodic tests that are executed on Video Mesh nodes.

        <br/>

        2. You can now view the destination IP address of the destination cluster in the JSON response.

        :param node_id: Unique ID of the Video Mesh node.
        :type node_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ReachabilityTestresultsfororganization`
        """
        params = {}
        params['nodeId'] = node_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['triggerType'] = trigger_type
        url = self.ep('testResults/reachabilityTest/nodes')
        data = super().get(url, params=params)
        r = ReachabilityTestresultsfororganization.model_validate(data)
        return r

    def list_cluster_details(self, org_id: str) -> list[ClusterDetailsCollection]:
        """
        List Cluster Details

        Returns the cluster details of all Video Mesh clusters in an organization.

        :param org_id: The unique ID for the organization.
        :type org_id: str
        :rtype: list[ClusterDetailsCollection]
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep('clusters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClusterDetailsCollection]).validate_python(data['items'])
        return r

    def get_cluster_details(self, cluster_id: str) -> list[ClusterDetailsCollection]:
        """
        Get Cluster Details

        Returns the cluster details for a single Video Mesh cluster.

        :param cluster_id: The unique Video Mesh Cluster ID.
        :type cluster_id: str
        :rtype: list[ClusterDetailsCollection]
        """
        url = self.ep(f'clusters/{cluster_id}')
        data = super().get(url)
        r = TypeAdapter(list[ClusterDetailsCollection]).validate_python(data['items'])
        return r

    def trigger_on_demand_test_for_cluster(self, cluster_id: str, type: TriggerOnDemandBodyType,
                                           nodes: list[str] = None) -> TriggeredTestStatus1:
        """
        Trigger on-demand test for cluster

        Triggers an on-demand test for a cluster.
        The test is run on a maximum of 10 nodes present in the cluster, chosen at random, or based on input from the
        user.

        :param cluster_id: Unique ID of the Video Mesh cluster.
        :type cluster_id: str
        :param type: Test type to trigger on node.
        :type type: TriggerOnDemandBodyType
        :param nodes: List of nodes to test.
        :type nodes: list[str]
        :rtype: :class:`TriggeredTestStatus1`
        """
        body = dict()
        body['type'] = enum_str(type)
        if nodes is not None:
            body['nodes'] = nodes
        url = self.ep(f'triggerTest/clusters/{cluster_id}')
        data = super().post(url, json=body)
        r = TriggeredTestStatus1.model_validate(data)
        return r

    def trigger_on_demand_test_for_node(self, node_id: str, type: TriggerOnDemandBodyType) -> TriggeredTestStatus1:
        """
        Trigger on-demand test for node

        Triggers an on-demand test for a node.

        :param node_id: Unique ID of the Video Mesh node.
        :type node_id: str
        :param type: Test type to trigger on node.
        :type type: TriggerOnDemandBodyType
        :rtype: :class:`TriggeredTestStatus1`
        """
        body = dict()
        body['type'] = enum_str(type)
        url = self.ep(f'triggerTest/nodes/{node_id}')
        data = super().post(url, json=body)
        r = TriggeredTestStatus1.model_validate(data)
        return r

    def get_triggered_test_status(self, command_id: str) -> TriggeredTestStatus1:
        """
        Get Triggered test status

        Returns the status of the test triggered using the Trigger on-demand test API.

        :param command_id: The unique command ID generated from Trigger on-demand test API.
        :type command_id: str
        :rtype: :class:`TriggeredTestStatus1`
        """
        params = {}
        params['commandId'] = command_id
        url = self.ep('testStatus')
        data = super().get(url, params=params)
        r = TriggeredTestStatus1.model_validate(data)
        return r

    def get_triggered_test_results(self, command_id: str) -> TriggeredTestResult:
        """
        Get Triggered test results

        Returns the results of the test triggered using the command ID.<br/>
        <b>NOTE:</b> The response format depends on the type of test triggered and it is the same as that of
        `NetworkTest API
        <https://developer.webex.com/docs/api/v1/video-mesh/list-network-test-results>`_, `MediaHealthMonitorTest API

        :param command_id: The unique command ID generated from Trigger on-demand test API.
        :type command_id: str
        :rtype: :class:`TriggeredTestResult`
        """
        params = {}
        params['commandId'] = command_id
        url = self.ep('testResults')
        data = super().get(url, params=params)
        r = TriggeredTestResult.model_validate(data)
        return r

    def list_network_test_results(self, org_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
                                  trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ConnectivityTestResultsObject:
        """
        List Network Test results

        Returns the test results of the Network tests triggered for an organization. The tests listed below are run as
        a part of the Network Test execution on the node.

        <b>Bandwidth Test</b> - Tests the bandwidth parameters of the Video Mesh node's network. The test is run
        between the Video Mesh node and cloud services.<br/>
        <b>DNS Resolution Test</b> - Tests the resolution of IP addresses related to cloud services, against the DNS
        servers configured on the Video Mesh node's network.<br/>
        <b>HTTPS Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to cloud services via
        HTTPS protocol.<br/>
        <b>Websocket Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to Webex cloud
        services via Websocket.<br/>

        :param org_id: Unique ID of the organization.
        :type org_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ConnectivityTestResultsObject`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/networkTest')
        data = super().get(url, params=params)
        r = ConnectivityTestResultsObject.model_validate(data)
        return r

    def get_network_test_results_for_cluster(self, cluster_id: str, from_: Union[str, datetime], to_: Union[str,
                                             datetime],
                                             trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ConnectivityTestResultsObject:
        """
        Get Network Test results for cluster

        Returns the test results of the Network tests triggered for a single Video Mesh cluster. The tests listed below
        are run as a part of the Network Test execution on the node.

        <b>Bandwidth Test</b> - Tests the bandwidth parameters of the Video Mesh node's network. The test is run
        between the Video Mesh node and cloud services.<br/>
        <b>DNS Resolution Test</b> - Tests the resolution of IP addresses related to cloud services, against the DNS
        servers configured on the Video Mesh node's network.<br/>
        <b>HTTPS Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to cloud services via
        HTTPS protocol.<br/>
        <b>Websocket Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to Webex cloud
        services via Websocket.<br/>

        :param cluster_id: Unique ID of the Video Mesh cluster.
        :type cluster_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ConnectivityTestResultsObject`
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
        params['triggerType'] = trigger_type
        url = self.ep('testResults/networkTest/clusters')
        data = super().get(url, params=params)
        r = ConnectivityTestResultsObject.model_validate(data)
        return r

    def get_network_test_results_for_node(self, node_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
                                          trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType) -> ConnectivityTestResultsObject:
        """
        Get Network Test results for node

        Returns the test results of the Network tests triggered for a single Video Mesh node. The tests listed below
        are run as a part of the Network Test execution on the node.

        <b>Bandwidth Test</b> - Tests the bandwidth parameters of the Video Mesh node's network. The test is run
        between the Video Mesh node and cloud services.<br/>
        <b>DNS Resolution Test</b> - Tests the resolution of IP addresses related to cloud services, against the DNS
        servers configured on the Video Mesh node's network.<br/>
        <b>HTTPS Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to cloud services via
        HTTPS protocol.<br/>
        <b>Websocket Connectivity Test</b> - Tests whether the Video Mesh node is able to connect to Webex cloud
        services via Websocket.<br/>

        :param node_id: Unique ID of the Video Mesh node.
        :type node_id: str
        :param from_: The start date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. The `from`
            parameter cannot have date and time values that exceed `to`.
        :type from_: Union[str, datetime]
        :param to_: The end date and time of the requested data in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
        :type to_: Union[str, datetime]
        :param trigger_type: Trigger type.
        :type trigger_type: ListMediaHealthMonitoringToolTestResultsV2TriggerType
        :rtype: :class:`ConnectivityTestResultsObject`
        """
        params = {}
        params['nodeId'] = node_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        params['triggerType'] = trigger_type
        url = self.ep('testResults/networkTest/nodes')
        data = super().get(url, params=params)
        r = ConnectivityTestResultsObject.model_validate(data)
        return r

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
        url = self.ep('clientTypeDistribution')
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
        url = self.ep('clientTypeDistribution/clusters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ClienttypedistributionCollectionforOrg]).validate_python(data['items'])
        return r

    def list_event_threshold_configuration(self, cluster_id: str = None,
                                           event_name: ListEventThresholdConfigurationEventName = None,
                                           event_scope: ListEventThresholdConfigurationEventScope = None,
                                           org_id: str = None) -> GetEventThresholdResponse:
        """
        List Event Threshold Configuration

        Returns the event threshold configurations for `orgId` or `clusterId`, with optional filters `eventName` and
        `eventScope`.

        :param cluster_id: Unique ID of the Video Mesh Cluster.
        :type cluster_id: str
        :param event_name: Event name to fetch threshold details.
        :type event_name: ListEventThresholdConfigurationEventName
        :param event_scope: Scope name to filter events.
        :type event_scope: ListEventThresholdConfigurationEventScope
        :param org_id: Unique ID of the Organization.
        :type org_id: str
        :rtype: :class:`GetEventThresholdResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if cluster_id is not None:
            params['clusterId'] = cluster_id
        if event_name is not None:
            params['eventName'] = event_name
        if event_scope is not None:
            params['eventScope'] = event_scope
        url = self.ep('eventThresholds')
        data = super().get(url, params=params)
        r = GetEventThresholdResponse.model_validate(data)
        return r

    def get_event_threshold_configuration(self, event_threshold_id: str) -> GetEventThresholdResponse:
        """
        Get Event Threshold Configuration

        Returns the event threshold configurations for `eventThresholdId`.

        :param event_threshold_id: Unique ID of the event threshold configuration.
        :type event_threshold_id: str
        :rtype: :class:`GetEventThresholdResponse`
        """
        url = self.ep(f'eventThresholds/{event_threshold_id}')
        data = super().get(url)
        r = GetEventThresholdResponse.model_validate(data)
        return r

    def update_event_threshold_configuration(self,
                                             event_thresholds: list[UpdateEventThresholdConfigurationEventThresholds]) -> BulkUpdateEventThresholdResponse:
        """
        Update Event Threshold Configuration

        Updates an existing event threshold configuration for given Event Threshold IDs.

        :type event_thresholds: list[UpdateEventThresholdConfigurationEventThresholds]
        :rtype: :class:`BulkUpdateEventThresholdResponse`
        """
        body = dict()
        body['eventThresholds'] = TypeAdapter(list[UpdateEventThresholdConfigurationEventThresholds]).dump_python(event_thresholds, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('eventThresholds')
        data = super().patch(url, json=body)
        r = BulkUpdateEventThresholdResponse.model_validate(data)
        return r

    def reset_event_threshold_configuration(self, event_threshold_ids: list[str]) -> BulkUpdateEventThresholdResponse:
        """
        Reset Event Threshold Configuration

        Resets the existing event threshold configuration for given Event Threshold IDs to default value. To stop
        receiving webhook events, use the `Webhooks API
        <docs/api/v1/webhooks>`_ to delete the webhook in question.

        :type event_threshold_ids: list[str]
        :rtype: :class:`BulkUpdateEventThresholdResponse`
        """
        body = dict()
        body['eventThresholdIds'] = event_threshold_ids
        url = self.ep('eventThresholds/reset')
        data = super().post(url, json=body)
        r = BulkUpdateEventThresholdResponse.model_validate(data)
        return r
