from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BandwidthTest', 'BlrClusterDetails', 'BlrNode1', 'BlrNodeLocation', 'BulkUpdateEventThresholdResponse', 'ClientTypeDistributionCollectionForOrg', 'ClientTypeDistributionForOrg', 'ClientTypeDistributionTrend1', 'CloudOverflowTrend1', 'ClusterAvailability', 'ClusterAvailabilityCollection', 'ClusterAvailableTimeline', 'ClusterClientTypeDistributionBlr1', 'ClusterClientTypeDistributionDetailsBlr1a', 'ClusterDetails', 'ClusterDetailsCollection', 'ClusterRedirectBlr1', 'ClusterRedirectDetailsBlr1a', 'ClusterUpgradeScheduleBlr', 'ClusterUtilizationCollection', 'ClusterUtilizationT1SJ', 'ClusterUtilizationTrend1', 'ClustersAvailability', 'ClustersUtilization', 'ConnectivityTestResultsClustersObject1', 'ConnectivityTestResultsForNode', 'ConnectivityTestResultsObject', 'EventThresholdBody', 'EventThresholdBodyEventName', 'FailureDetails3', 'GetEntityThresholdConfig1', 'GetEventThresholdResponse', 'MediaHealthMonitoringClusters', 'MediaHealthMonitoringForFirstCluster', 'MediaHealthMonitoringResultsCollectionForOrganization', 'MediaHealthMonitoringResultsForOrganization', 'MediaHealthMonitoringSecondNode', 'MediaHealthMonitoringTestResultsFailure', 'MediaHealthMonitoringTestResultsSuccess', 'MediaSignallingTestResultFailure', 'MediaSignallingTestResultSuccess', 'NodeAvailability', 'NodeAvailabilityCollection', 'NodeAvailableTimeline', 'NodeStatusList1', 'NodeStatusList1Status', 'NodesAvailability', 'OverflowDetails1', 'OverflowToCloud', 'OverflowToCloudCollection', 'PerClusterConnectivityResult1', 'PerNodeConnectivityResult1', 'ReachabilityTestResults', 'ReachabilityTestResultsCluster', 'ReachabilityTestResultsDestinationCluster', 'ReachabilityTestResultsFirstNode', 'ReachabilityTestResultsForCluster', 'ReachabilityTestResultsForFirstCluster', 'ReachabilityTestResultsForOrganization', 'ReachabilityTestResultsStunResults1', 'ReachabilityTestResultsSuccess', 'RedirectCollectionForOrg', 'RedirectForOrg', 'RedirectTrend1', 'ServiceTypeResult2', 'ServiceTypeResult4', 'SingleNodeAvailability', 'SingleNodeAvailabilityCollection', 'SingleNodeAvailableTimeline', 'TriggerOn-DemandBody', 'TriggerOn-DemandBodyCluster', 'TriggerOn-DemandBodyType', 'TriggeredTestResult', 'TriggeredTestStatus1', 'UpdateEventThresholdConfig1', 'UtilizationMetricsT1SJ', 'WebSocketConnectivityTest']


class ClusterAvailableTimeline(ApiModel):
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segmentStartTime: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segmentEndTime: Optional[datetime] = None
    #: Availability information of the Video Mesh cluster.
    #: example: Available
    availability: Optional[str] = None
    #: Number of nodes that are online.
    #: example: 1.0
    noOfOnlineNodes: Optional[int] = None
    #: Number of nodes that are offline.
    #: example: 1.0
    noOfOfflineNodes: Optional[int] = None
    #: Total number of nodes in the Video Mesh cluster.
    #: example: 2.0
    totalNodes: Optional[int] = None


class ClusterAvailability(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    clusterName: Optional[str] = None
    availabilitySegments: Optional[list[ClusterAvailableTimeline]] = None


class ClusterAvailabilityCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    orgId: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[ClusterAvailability]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to: Optional[datetime] = None


class ClustersAvailability(ApiModel):
    items: Optional[list[ClusterAvailabilityCollection]] = None


class NodeAvailableTimeline(ApiModel):
    #: Number of nodes that are online.
    #: example: 1.0
    noOfOnlineNodes: Optional[int] = None
    #: Number of nodes that are offline.
    noOfOfflineNodes: Optional[int] = None
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segmentStartTime: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segmentEndTime: Optional[datetime] = None
    #: Availability information of the Video Mesh node.
    #: example: Available
    availability: Optional[str] = None
    #: Reason for the Video Mesh node being unavailable (if any).
    #: example: NA
    unAvailabilityReason: Optional[str] = None
    #: Total number of nodes in the Video Mesh cluster.
    #: example: 1.0
    totalNodes: Optional[int] = None


class NodeAvailability(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    clusterName: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    hostNameOrIp: Optional[str] = None
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMWViNjVmZGYtOTY0My00MTdmLTk5NzQtYWQ3MmNhZTBlMTBmOmMyNTk0YmY2NDFmZTRkNTFiZDg3YThiMjYxYzg3NWY1
    nodeId: Optional[str] = None
    availabilitySegments: Optional[list[NodeAvailableTimeline]] = None


class NodeAvailabilityCollection(ApiModel):
    #: Unique ID for a Video Mesh organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    orgId: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[NodeAvailability]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to: Optional[datetime] = None


class NodesAvailability(ApiModel):
    items: Optional[list[NodeAvailabilityCollection]] = None


class SingleNodeAvailableTimeline(ApiModel):
    #: Start date and time of the segment of availability data.
    #: example: 2021-09-15T15:53:00Z
    segmentStartTime: Optional[datetime] = None
    #: End date and time of the segment of availability data.
    #: example: 2021-09-15T16:53:00Z
    segmentEndTime: Optional[datetime] = None
    #: Availability information of the Video Mesh node.
    #: example: Available
    availability: Optional[str] = None
    #: Reason for the Video Mesh node being unavailable (if any).
    #: example: NA
    unAvailabilityReason: Optional[str] = None


class SingleNodeAvailability(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: San Jose
    clusterName: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    hostNameOrIp: Optional[str] = None
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMWViNjVmZGYtOTY0My00MTdmLTk5NzQtYWQ3MmNhZTBlMTBmOmMyNTk0YmY2NDFmZTRkNTFiZDg3YThiMjYxYzg3NWY1
    nodeId: Optional[str] = None
    availabilitySegments: Optional[list[SingleNodeAvailableTimeline]] = None


class SingleNodeAvailabilityCollection(ApiModel):
    #: Unique ID for a Video Mesh organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    orgId: Optional[str] = None
    #: Availability details of the Video Mesh cluster.
    items: Optional[list[SingleNodeAvailability]] = None
    #: Start date and time (inclusive) of the availability data.
    #: example: 2021-09-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the availability data.
    #: example: 2021-09-15T17:53:00Z
    to: Optional[datetime] = None


class MediaSignallingTestResultFailure(ApiModel):
    #: The name of the test.
    #: example: Media Signalling
    testName: Optional[str] = None
    #: Test results(Success/Failed).
    #: example: Failed
    testResult: Optional[str] = None
    #: Reason for test failure.
    #: example: An internal error occurred in monitoring tool [Error Code:1003]. If the issue persists, please contact Cisco Support.
    failureReason: Optional[str] = None


class MediaHealthMonitoringTestResultsFailure(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    id: Optional[str] = None
    #: Test results of Media Signalling, SIP Signalling, Media Cascade runs.
    testResults: Optional[list[MediaSignallingTestResultFailure]] = None


class MediaHealthMonitoringSecondNode(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    nodeId: Optional[str] = None
    #: Host name or the IP of the Video Mesh node.
    #: example: abc.company.com
    hostNameOrIP: Optional[str] = None
    #: The Media Health Monitoring Tool test results for a single Video Mesh node.
    mhmTestResults: Optional[list[MediaHealthMonitoringTestResultsFailure]] = None


class MediaHealthMonitoringForFirstCluster(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: banglore
    clusterName: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[MediaHealthMonitoringSecondNode]] = None


class MediaHealthMonitoringClusters(ApiModel):
    #: The list of Video Mesh clusters.
    clusters: Optional[list[MediaHealthMonitoringForFirstCluster]] = None


class MediaHealthMonitoringResultsCollectionForOrganization(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    orgId: Optional[str] = None
    #: Start date and time (inclusive) of the Media Health Monitoring Tool data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the Media Health Monitoring Tool data.
    #: example: 2023-01-20T15:53:00Z
    to: Optional[datetime] = None
    #: Media Health Monitoring Tool test results.
    items: Optional[list[MediaHealthMonitoringClusters]] = None


class MediaHealthMonitoringResultsForOrganization(ApiModel):
    items: Optional[list[MediaHealthMonitoringResultsCollectionForOrganization]] = None


class MediaSignallingTestResultSuccess(ApiModel):
    #: The name of the test.
    #: example: Media Signalling
    testName: Optional[str] = None
    #: The result, either `Success` or `Failed`.
    #: example: Success
    testResult: Optional[str] = None


class MediaHealthMonitoringTestResultsSuccess(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    id: Optional[str] = None
    #: Test results of Media Signalling, SIP Signalling, Media Cascade runs.
    testResults: Optional[list[MediaSignallingTestResultSuccess]] = None


class OverflowDetails1(ApiModel):
    #: The reason for this overflow.
    #: example: Capacity exceeded
    overflowReason: Optional[str] = None
    #: Number of overflows.
    #: example: 25.0
    overflowCount: Optional[int] = None
    #: Any possible remediations for this overflow.
    #: example: Video Mesh exceeded its capacity. If this happens frequently, consider adding more nodes to your clusters.
    possibleRemediation: Optional[str] = None


class CloudOverflowTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    #: Overflow Details.
    overflowDetails: Optional[list[OverflowDetails1]] = None


class OverflowToCloudCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    orgId: Optional[str] = None
    #: Start date and time (inclusive) for the Overflow to Cloud data.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) for the Overflow to Cloud data.
    #: example: 2022-03-24T04:22:03Z
    to: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregationInterval: Optional[datetime] = None
    #: Overflow data for the organization.
    items: Optional[list[CloudOverflowTrend1]] = None


class OverflowToCloud(ApiModel):
    items: Optional[list[OverflowToCloudCollection]] = None


class ClusterRedirectDetailsBlr1a(ApiModel):
    #: The reason for the redirect.
    #: example: Capacity exceeded
    redirectReason: Optional[str] = None
    #: Number of Call Redirects.
    #: example: 10.0
    redirectCount: Optional[int] = None
    #: Any possible remediations for this overflow.
    #: example: Video Mesh exceeded its capacity. If this happens frequently, consider adding more nodes to your clusters.
    possibleRemediation: Optional[str] = None


class ClusterRedirectBlr1(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOWZkOTg
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: bangalore
    clusterName: Optional[str] = None
    #: Call Redirect Details.
    redirectDetails: Optional[list[ClusterRedirectDetailsBlr1a]] = None


class RedirectTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterRedirectBlr1]] = None


class RedirectCollectionForOrg(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    orgId: Optional[str] = None
    #: Start date and time (inclusive) for the Call Redirect details.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the Call Redirect details.
    #: example: 2022-03-24T10:22:03Z
    to: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregationInterval: Optional[datetime] = None
    #: Redirect details for the organization.
    items: Optional[list[RedirectTrend1]] = None


class RedirectForOrg(ApiModel):
    items: Optional[list[RedirectCollectionForOrg]] = None


class UtilizationMetricsT1SJ(ApiModel):
    #: Peak CPU usage during the time interval.
    #: example: 54.54
    peakCpu: Optional[int] = None
    #: Average CPU usage during the time interval.
    #: example: 4.27
    avgCpu: Optional[int] = None
    #: Maximum active calls at a point in the time interval.
    #: example: 5.0
    activeCalls: Optional[int] = None
    #: Maximum active private calls at a point in the time interval.
    #: example: 1.0
    activePrivateCalls: Optional[int] = None


class ClusterUtilizationT1SJ(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOTEyMzQ=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: sanjose
    clusterName: Optional[str] = None
    #: Utilization details for the cluster in the time interval.
    utilizationMetrics: Optional[UtilizationMetricsT1SJ] = None


class ClusterUtilizationTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterUtilizationT1SJ]] = None


class ClusterUtilizationCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ=
    orgId: Optional[str] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregationInterval: Optional[datetime] = None
    #: Start date and time (inclusive) of the utilization data.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the utilization data.
    #: example: 2022-03-24T10:22:03Z
    to: Optional[datetime] = None
    #: Utilization details of the Video Mesh cluster
    items: Optional[list[ClusterUtilizationTrend1]] = None


class ClustersUtilization(ApiModel):
    items: Optional[list[ClusterUtilizationCollection]] = None


class ReachabilityTestResultsSuccess(ApiModel):
    #: Destination IP address.
    #: example: 1.1.1.1
    ipAddress: Optional[str] = None
    #: Port number.
    #: example: 5004.0
    port: Optional[int] = None
    #: Port reachability information.
    #: example: True
    reachable: Optional[bool] = None


class ReachabilityTestResultsStunResults1(ApiModel):
    #: The timestamp of the test run.
    #: example: 2022-03-15T15:53:00Z
    timestamp: Optional[datetime] = None
    #: The type of the test being executed. Can be either `OnDemand` or `Periodic`.
    #: example: OnDemand
    triggerType: Optional[str] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    id: Optional[str] = None
    #: List of UDP ports being checked in Reachability test.
    udp: Optional[list[ReachabilityTestResultsSuccess]] = None
    #: List of TCP ports being checked in Reachability test.
    tcp: Optional[list[ReachabilityTestResultsSuccess]] = None


class ReachabilityTestResultsDestinationCluster(ApiModel):
    #: Cloud Webex cluster against which Reachability test is being executed.
    #: example: Amsterdam Cluster
    destinationCluster: Optional[str] = None
    #: STUN test results for a Video Mesh cluster.
    stunResults: Optional[list[ReachabilityTestResultsStunResults1]] = None


class ReachabilityTestResultsFirstNode(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    nodeId: Optional[str] = None
    #: Host name or the IP of the Video Mesh node.
    #: example: xyz.company.com
    hostNameOrIP: Optional[str] = None
    #: Reachability test results for a single Video Mesh node.
    testResults: Optional[list[ReachabilityTestResultsDestinationCluster]] = None


class ReachabilityTestResultsForFirstCluster(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: banglore
    clusterName: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[ReachabilityTestResultsFirstNode]] = None


class ReachabilityTestResultsForCluster(ApiModel):
    #: List of Video Mesh clusters.
    clusters: Optional[list[ReachabilityTestResultsForFirstCluster]] = None


class ReachabilityTestResultsForOrganization(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    orgId: Optional[str] = None
    #: Start date and time (inclusive) of the Reachability test results data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the Reachability test results data.
    #: example: 2023-01-20T15:53:00Z
    to: Optional[datetime] = None
    #: Reachability test results data.
    items: Optional[list[ReachabilityTestResultsForCluster]] = None


class ReachabilityTestResults(ApiModel):
    items: Optional[list[ReachabilityTestResultsForOrganization]] = None


class ReachabilityTestResultsCluster(ApiModel):
    items: Optional[list[ReachabilityTestResultsForCluster]] = None


class BlrNodeLocation(ApiModel):
    #: Country code of the Location where the Video Mesh node is deployed.
    #: example: IN
    countryCode: Optional[str] = None
    #: City where Video Mesh node is deployed.
    #: example: Bangalore
    city: Optional[str] = None
    #: Time zone in which the Video Mesh node is deployed.
    #: example: Asia/Kolkata
    timeZone: Optional[str] = None


class BlrNode1(ApiModel):
    #: ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo0NjdiNGIxZC1jZWI2LTQwN2EtYWZmOC1mMjIxZmFiNzhjNzI
    nodeId: Optional[str] = None
    #: Host Name or the IP of the Video Mesh node.
    #: example: xyz.abc.com
    hostNameOrIp: Optional[str] = None
    #: Deployment Type of the Video Mesh node.
    #: example: Video Mesh Node Lite
    deploymentType: Optional[str] = None
    #: Location details of the Video Mesh node.
    location: Optional[BlrNodeLocation] = None


class ClusterUpgradeScheduleBlr(ApiModel):
    #: Days of the week when scheduled upgrades will occur for the Video Mesh cluster.
    #: example: ['sunday', 'monday', 'tuesday']
    scheduleDays: Optional[list[str]] = None
    #: Time when scheduled upgrade will occur for the Video Mesh cluster.
    #: example: 02:00
    scheduleTime: Optional[datetime] = None
    #: Timezone of the scheduled upgrade of Video Mesh cluster.
    #: example: Asia/Kolkata
    scheduleTimeZone: Optional[str] = None
    #: Upgrade Pending information.
    #: example: True
    upgradePending: Optional[bool] = None
    #: Time when the next upgrade is scheduled for the Video Mesh cluster.
    #: example: 2020-03-25T20:30:00Z
    nextUpgradeTime: Optional[datetime] = None


class BlrClusterDetails(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZjpiMzdmNTgzYy1kZGRjLTQyOGItODJlNS1jYmU2ODFkYjQ5NjI
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: Bangalore
    clusterName: Optional[str] = None
    #: The Video Mesh nodes in the cluster.
    nodes: Optional[list[BlrNode1]] = None
    #: Release Channel of the Video Mesh cluster.
    #: example: alpha
    releaseChannel: Optional[str] = None
    #: Upgrade Schedule details of the Video Mesh cluster.
    upgradeSchedule: Optional[ClusterUpgradeScheduleBlr] = None


class ClusterDetailsCollection(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    orgId: Optional[str] = None
    #: Details of all the clusters of the organization.
    items: Optional[list[BlrClusterDetails]] = None


class ClusterDetails(ApiModel):
    items: Optional[list[ClusterDetailsCollection]] = None


class TriggeredTestResult(ApiModel):
    #: Test type of the command ID.
    #: example: MediaHealthMonitorTest
    type: Optional[str] = None
    #: The unique ID for the test being executed.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    commandId: Optional[str] = None
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    orgId: Optional[str] = None
    results: Optional[list[MediaHealthMonitoringClusters]] = None


class NodeStatusList1Status(str, Enum):
    dispatched = 'Dispatched'
    completed = 'Completed'
    errored = 'Errored'


class NodeStatusList1(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    nodeId: Optional[str] = None
    #: Status of the test triggered.
    #: example: Dispatched
    status: Optional[NodeStatusList1Status] = None


class TriggeredTestStatus1(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    orgId: Optional[str] = None
    #: The unique ID of the test being executed.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT01NQU5EX0lELzJjM2M5ZjllLTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhYzo2NTJmNmMxMC01NjgxLTExZWQtOTkyZS1kNTY5YzlkMDlhNzU
    commandId: Optional[str] = None
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    clusterId: Optional[str] = None
    nodes: Optional[list[NodeStatusList1]] = None


class TriggerOn-DemandBodyType(str, Enum):
    #: Used to test whether the media ports within the Video Mesh node are open, and whether the Video Mesh node is able to reach the cloud clusters pertaining to the media containers via those ports.
    reachabilitytest = 'ReachabilityTest'
    #: Used to test the network environment of the Video Mesh node by running various connectivity, bandwidth, and DNS resolution tests against Webex Cloud and ThirdParty Cloud (Docker) services.
    networktest = 'NetworkTest'
    #: Used to test the meetings and call health of Video Mesh nodes using signalling and cascading methods.
    mediahealthmonitortest = 'MediaHealthMonitorTest'


class TriggerOn-DemandBody(ApiModel):
    #: Test type to trigger on node.
    #: example: ReachabilityTest
    type: Optional[TriggerOn-DemandBodyType] = None


class TriggerOn-DemandBodyCluster(ApiModel):
    #: Test type to trigger on node.
    #: example: ReachabilityTest
    type: Optional[TriggerOn-DemandBodyType] = None
    #: List of nodes to test.
    #: example: ['Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOWUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFjOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGU5OTc4Zjk5MDJk', 'Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOWUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFjOjE1NmRmNzg5Yzg1NTRhYmNhZGVmZ2U5OTc4Zjk5MDJk']
    nodes: Optional[list[str]] = None


class FailureDetails3(ApiModel):
    #: Possible reasons for failure for the test.
    #: example: ['Degraded Network Bandwidth speed detected in the Video Mesh Node connectivity to the Webex Cloud [Error Code: 1402,1405].']
    possibleFailureReason: Optional[list[str]] = None
    #: Possible fixes for the failures mentioned above.
    #: example: ['Please refer to Video Mesh deployment guide to ensure the network settings are configured correctly, and the minimum internet speed requirements are met. If the issue persists, please contact Cisco Support.']
    possibleRemediation: Optional[list[str]] = None


class ServiceTypeResult4(ApiModel):
    #: Service for which the test was executed.
    #: example: WebexCloud
    serviceType: Optional[str] = None
    #: Result of the test executed.
    #: example: Failed
    testResult: Optional[str] = None
    failureDetails: Optional[FailureDetails3] = None


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
    triggerType: Optional[str] = None
    #: Unique ID of the test.
    #: example: Y2lzY29zcGFyazovL3VzL0NPTU1BTkRJRC8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY6YWRlODhhNjAtMzk5Mi0xMWVkLTlhYmQtYzUyMjRiZjNjMzQ4
    id: Optional[str] = None
    result: Optional[list[BandwidthTest]] = None


class PerNodeConnectivityResult1(ApiModel):
    #: Unique ID of the Video Mesh node.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DT05ORUNUT1IvMmMzYzlmOTUtNzNkOS00NDYwLWE2NjgtMDQ3MTYyZmYxYmFkOjE1NmRmNzg5Yzg1NTRkNTVhMjc1ZGY5OTc4Zjk5MDJk
    nodeId: Optional[str] = None
    #: Host name or IP Address of the Video Mesh node.
    #: example: abc.company.com
    hostNameOrIP: Optional[str] = None
    testResults: Optional[list[ConnectivityTestResultsForNode]] = None


class PerClusterConnectivityResult1(ApiModel):
    #: Unique ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzJjM2M5Zjk1LTczZDktNDQ2MC1hNjY4LTA0NzE2MmZmMWJhZDpmMWJmMGI1MC0yMDUyLTQ3ZmUtYjg3ZC01MTFjMmZlNzQ3MWI=
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: sanjose
    clusterName: Optional[str] = None
    nodes: Optional[list[PerNodeConnectivityResult1]] = None


class ConnectivityTestResultsClustersObject1(ApiModel):
    #: List of Video Mesh clusters.
    clusters: Optional[list[PerClusterConnectivityResult1]] = None


class ConnectivityTestResultsObject(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ=
    orgId: Optional[str] = None
    #: Start date and time (inclusive) of the Network Test data.
    #: example: 2023-01-15T15:53:00Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the Network Test data.
    #: example: 2023-01-20T15:53:00Z
    to: Optional[datetime] = None
    #: Network test results.
    items: Optional[list[ConnectivityTestResultsClustersObject1]] = None


class ServiceTypeResult2(ApiModel):
    #: Service for which the test was executed.
    #: example: ThirdPartyCloud
    serviceType: Optional[str] = None
    #: Result of the test executed.
    #: example: Success
    testResult: Optional[str] = None


class WebSocketConnectivityTest(ApiModel):
    #: The type of test result.
    #: example: WebSocketConnectivityTest
    type: Optional[str] = None
    #: Test Results from different services.
    results: Optional[list[ServiceTypeResult2]] = None


class ClusterClientTypeDistributionDetailsBlr1a(ApiModel):
    #: The type of device.
    #: example: sipEndpoint
    deviceType: Optional[str] = None
    #: The description of the device type.
    #: example: SIP Devices
    description: Optional[str] = None
    #: The count of the device type.
    #: example: 10.0
    count: Optional[int] = None


class ClusterClientTypeDistributionBlr1(ApiModel):
    #: ID of the Video Mesh cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzM2ZDg5NGY3LTJiNTctNDNjMS1hY2VlLWQ0N2U2Nzc2MTQxNDo1ODJhMWFlYy03YTMwLTQ2MDItYTI2NS02YTE5NDcwOWZkOTg
    clusterId: Optional[str] = None
    #: Name of the Video Mesh cluster.
    #: example: Bangalore
    clusterName: Optional[str] = None
    #: Client Type Distribution Details.
    clientTypeDistributionDetails: Optional[list[ClusterClientTypeDistributionDetailsBlr1a]] = None


class ClientTypeDistributionTrend1(ApiModel):
    #: Timestamp.
    #: example: 2022-03-23T10:30:00Z
    timestamp: Optional[datetime] = None
    clusters: Optional[list[ClusterClientTypeDistributionBlr1]] = None


class ClientTypeDistributionCollectionForOrg(ApiModel):
    #: The unique ID for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNmQ4OTRmNy0yYjU3LTQzYzEtYWNlZS1kNDdlNjc3NjE0MTQ
    orgId: Optional[str] = None
    #: Start date and time (inclusive) for the Client Type Distribution details.
    #: example: 2022-03-23T10:22:03Z
    from_: Optional[datetime] = Field(alias='from', default=None)
    #: End date and time (inclusive) of the Client Type Distribution details.
    #: example: 2022-03-24T10:22:03Z
    to: Optional[datetime] = None
    #: The aggregation period of the trend data.
    #: example: 10m
    aggregationInterval: Optional[datetime] = None
    #: Client Type Distribution details for the organization.
    items: Optional[list[ClientTypeDistributionTrend1]] = None


class ClientTypeDistributionForOrg(ApiModel):
    items: Optional[list[ClientTypeDistributionCollectionForOrg]] = None


class UpdateEventThresholdConfig1(ApiModel):
    #: Threshold value (in percentage) to trigger an event.
    #: example: 40.0
    minThreshold: Optional[int] = None
    #: Deafault Threshold value (in percentage) to trigger an event.
    #: example: 10.0
    defaultMinThreshold: Optional[int] = None


class GetEntityThresholdConfig1(ApiModel):
    #: Name of the event.
    #: example: clusterCallsRedirected
    eventName: Optional[str] = None
    #: Unique ID of the event threshold configuration.
    #: example: Y2lzY29zcGFyazovL3VzL0VWRU5ULzQyN2U5ZTk2LTczYTctNDYwYS04MGZhLTcyNWU4MWE2MDg3Zjo2YzJhZGRmMS0wYjAzLTRiZWEtYjIxYy0xYzFjYzdiY2UwOWQ
    eventThresholdId: Optional[str] = None
    #: The `eventScope` is scope of event.
    #: example: CLUSTER
    eventScope: Optional[str] = None
    #: The `entityId` is the unique ID of the Organization or the unique ID of the Video Mesh Cluster.
    #: example: Y2lzY29zcGFyazovL3VzL0hZQlJJRF9DTFVTVEVSLzRiNTk5NzkwLWVlMzctMTFlZC1hMDViLTAyNDJhYzEyMDAwMzo2NjMxOTMyNC1lZTM3LTExZWQtYTA1Yi0wMjQyYWMxMjAwMDM
    entityId: Optional[str] = None
    #: Threshold configuration of an `entityId`.
    thresholdConfig: Optional[UpdateEventThresholdConfig1] = None


class GetEventThresholdResponse(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ
    orgId: Optional[str] = None
    eventThresholds: Optional[list[GetEntityThresholdConfig1]] = None


class BulkUpdateEventThresholdResponse(ApiModel):
    #: Unique ID of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8yYzNjOWY5NS03M2Q5LTQ0NjAtYTY2OC0wNDcxNjJmZjFiYWQ
    orgId: Optional[str] = None
    #: List of successful updated response
    eventThresholds: Optional[list[GetEntityThresholdConfig1]] = None
    #: List of failed or invalid event threshold IDs.
    #: example: ['Y2lzY29zcGFyazovL3VzL0VWRU5ULzQyN2U5ZTk2LTczYTctNDYwYS04MGZhLTcyNWU4MWE2MDg3ZjowM2ZkYjkzZC1jNTllLTQzMjQtODIwNS1lNDIyYzA3NGQ5Mzg']
    failedEventThresholdIds: Optional[list[str]] = None


class EventThresholdBodyEventName(str, Enum):
    #: Event name for cluster call redirects.
    clustercallsredirected = 'clusterCallsRedirected'
    #: Event name for organization call overflows.
    orgcallsoverflowed = 'orgCallsOverflowed'
    none_ = 'none'


class EventThresholdBody(ApiModel):
    #: The name of the event corresponding to the `entitiyId`.
    eventName: Optional[EventThresholdBodyEventName] = None
