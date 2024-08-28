from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AgentStats', 'AgentStatsChannel', 'AgentStatsChannelChannelType', 'AgentStatsResponse', 'Artifact',
           'ArtifactAttributes', 'ContactCenterApi', 'GetAgentsStatisticsInterval', 'ListCapturesQuery',
           'ListCapturesResponse', 'Meta', 'QueueStats', 'QueueStatsResponse', 'Recording', 'RecordingStatus', 'Task',
           'TaskAttributes', 'TaskAttributesStatus', 'TaskOwner', 'TaskWithCaptures', 'TasksResponse']


class Meta(ApiModel):
    #: Organization ID.
    #: example: e767c439-08bf-48fa-a03c-ac4a09eeee8f
    org_id: Optional[str] = None


class TaskOwner(ApiModel):
    #: ID of the agent last assigned to this task.
    #: example: e0c7611b-8035-443a-b7a8-dca9f8b8289b
    id: Optional[str] = None
    #: Name of the agent last assigned to this task.
    #: example: Joseph Lambert
    name: Optional[str] = None


class TaskAttributesStatus(str, Enum):
    created = 'created'
    queued = 'queued'
    offered = 'offered'
    assigned = 'assigned'
    abandoned = 'abandoned'
    completed = 'completed'


class TaskAttributes(ApiModel):
    #: Channel type on which the task is performed (e.g. email, telephony, chat, etc.).
    #: example: email
    channel_type: Optional[str] = None
    #: Created time of the task (epoch milliseconds).
    #: example: 1591702170000
    created_time: Optional[int] = None
    #: Last updated time of the task (epoch milliseconds). Updates whenever the underlying data is modified, even if
    #: the Task view of the data is the same. May also update after task "closure", so not suitable for finding a
    #: task's "closed time".
    #: example: 1591712170099
    last_updated_time: Optional[int] = None
    owner: Optional[TaskOwner] = None
    queue: Optional[TaskOwner] = None
    context: Optional[Any] = None
    #: Customer's channel-specific identifier. For telephony, this is the phone number. For email and chat, this is the
    #: email address.
    #: example: chatuser@email.com
    origin: Optional[str] = None
    #: Destination the customer contacted. For telephony, this is the number the contact called. For chat, this is the
    #: URL of the page where the chat takes place. For email, it is the email address contacted.
    #: example: +18005555555
    destination: Optional[str] = None
    #: Indicates which party initiated the Task. If "inbound", call was initated by customer. If "outbound", was
    #: initiated by system as part of campaign. If "outdial", was initiated by an agent.
    #: example: inbound
    direction: Optional[str] = None
    #: Reason code specified by customer to indicate main aim of the task.
    #: example: Credit
    reason_code: Optional[str] = None
    #: Whether a capture has been requested for this Task. If this is true, a capture should eventually be available.
    #: False indicates no capture will be made available. If null, it is not yet known whether a capture has been
    #: requested.
    capture_requested: Optional[bool] = None
    #: Current status of the task.
    #: example: assigned
    status: Optional[TaskAttributesStatus] = None


class Task(ApiModel):
    #: ID of the task.
    #: example: 93912f11-6017-404b-bf14-5331890b1797
    id: Optional[str] = None
    attributes: Optional[TaskAttributes] = None


class TasksResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    #: List of tasks retrieved according to query parameters.
    data: Optional[list[Task]] = None


class AgentStatsChannelChannelType(str, Enum):
    telephony = 'telephony'
    chat = 'chat'
    email = 'email'
    social = 'social'


class AgentStatsChannel(ApiModel):
    #: Channel GUID
    #: example: 91fada7d-6be8-46e8-b6af-8598e71b7e27
    channel_id: Optional[str] = None
    #: example: telephony
    channel_type: Optional[AgentStatsChannelChannelType] = None
    #: Number of assigned tasks within this channel during the agent's session.
    #: example: 3
    total_assigned_tasks: Optional[int] = None
    #: Number of accepted tasks that were assigned to the agent.
    #: example: 3
    total_accepted_tasks: Optional[int] = None
    #: Number of rejected tasks that were assigned to the agent.
    total_rejected_tasks: Optional[int] = None
    #: Number of tasks the agent transferred to another agent.
    total_transferred_tasks: Optional[int] = None
    #: Amount of time the agent was engaged with a customer (in milliseconds).
    #: example: 40302
    total_engaged_duration: Optional[int] = None
    #: Amount of time the customer(s) was put on hold (in milliseconds).
    #: example: 10198
    total_hold_duration: Optional[int] = None
    #: Amount of time the agent spent wrapping-up customer interactions (in milliseconds).
    #: example: 3552
    total_wrap_up_duration: Optional[int] = None


class AgentStats(ApiModel):
    #: Time in GMT
    #: example: 1591702200000
    interval_start_time: Optional[int] = None
    #: Agent GUID
    #: example: 06ce7234-dd3e-49e2-8763-d93766739d3
    agent_id: Optional[str] = None
    #: example: Jim Bob
    agent_name: Optional[str] = None
    #: Team GUID
    #: example: fbf80248-b328-4c37-9ea5-4c2ec8b4d52c
    team_id: Optional[str] = None
    #: Name of team to which the agent belongs.
    #: example: Ghost Riders
    team_name: Optional[str] = None
    #: Time that the agent's status was set to 'Available'.
    #: example: 54052
    total_available_time: Optional[int] = None
    #: Time that the agent's status was set to 'Unavailable'.
    total_unavailable_time: Optional[int] = None
    channel: Optional[list[AgentStatsChannel]] = None


class AgentStatsResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    #: List of agent stats for each queried agent.
    data: Optional[list[AgentStats]] = None


class QueueStats(ApiModel):
    #: Time in GMT (milliseconds).
    #: example: 1591702200000
    interval_start_time: Optional[int] = None
    #: Queue ID
    #: example: 06ce7234-dd3e-49e2-8763-d93766739d3
    queue_id: Optional[str] = None
    #: example: MainInbound
    queue_name: Optional[str] = None
    #: example: telephony
    channel_type: Optional[AgentStatsChannelChannelType] = None
    #: example: 7
    total_offered_tasks: Optional[int] = None
    #: example: 7
    total_enqueued_tasks: Optional[int] = None
    #: example: 7
    total_assigned_tasks: Optional[int] = None
    #: example: 7
    total_accepted_tasks: Optional[int] = None
    total_rejected_tasks: Optional[int] = None
    total_abandoned_tasks: Optional[int] = None
    #: example: 20349
    average_enqueued_time: Optional[int] = None
    #: example: 93729
    average_handle_time: Optional[int] = None


class QueueStatsResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    data: Optional[list[QueueStats]] = None


class RecordingStatus(str, Enum):
    completed = 'Completed'
    pending = 'Pending'
    not_found = 'Not Found'
    error = 'Error'


class ArtifactAttributes(ApiModel):
    #: example: recording-1.wav
    file_name: Optional[str] = None
    #: Capture download url.
    #: example: https://cjp-ccone-devus1-media-storage-recording.s3.amazonaws.com/9e4895c9-787b-4615-b15f-f1b3b12c3091/
    file_path: Optional[str] = None
    #: Begin time of capture
    #: example: 1591804052000
    start_time: Optional[int] = None
    #: End time of capture
    #: example: 1591804562000
    stop_time: Optional[int] = None
    #: Comma separated list of agent Ids and masked customer contact email/phone details.
    #: example: ['140e7575-6a21-4599-a929-c407dcf36649,+*******9000']
    participants: Optional[list[str]] = None


class Artifact(ApiModel):
    #: example: 792707a1-6696-4a66-8184-9bab0a769c10
    id: Optional[str] = None
    attributes: Optional[list[ArtifactAttributes]] = None


class Recording(ApiModel):
    #: example: Completed
    status: Optional[RecordingStatus] = None
    artifacts: Optional[list[Artifact]] = None


class TaskWithCaptures(ApiModel):
    #: example: 6a64d539-4653-4c48-98d7-78fb66c1bc1d
    task_id: Optional[str] = None
    recording: Optional[Recording] = None


class ListCapturesResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    data: Optional[list[TaskWithCaptures]] = None


class GetAgentsStatisticsInterval(str, Enum):
    d15 = '15'
    d30 = '30'
    d60 = '60'


class ListCapturesQuery(ApiModel):
    #: Organization ID to use for this operation. If unspecified, inferred from token. Token must have permission to
    #: interact with this organization.
    #: example: 93912f11-6017-404b-bf14-5331890b1797
    org_id: Optional[str] = None
    #: Comma separated list of taskIds to gather captures for. Max of 10 taskIds per request.
    #: example: ['6a64d539-4653-4c48-98d7-78fb66c1bc1d, 9dd4a070-4047-46ac-abec-942f48f5535e']
    task_ids: Optional[list[str]] = None
    #: Expiration time of returned s3 url (in minutes). Max value is 60.
    #: example: 30
    url_expiration: Optional[int] = None


class ContactCenterApi(ApiChild, base='contactCenter'):
    """
    Contact Center
    
    The Webex Contact Center functionality and API endpoints described here are
    currently pre-release features which are not available to all Webex users. If
    you have any questions, or if you need help, please contact the Webex
    Developer Support team at devsupport@webex.com.
    
    
    
    The set of WxCC API endpoints below allow developers to view Tasks for insights into the interactions between
    agents and customers, Agents Statistics for details related to specific agents, Queues Statistics for details on
    specific queues, and Captures for the actual media related to an interaction.
    
    These endpoints require an auth token with the `cjp:config_read` scope for organizations with a WxCC license or the
    `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.
    """

    def get_tasks(self, from_: int, to_: int = None, channel_types: list[str] = None, page_size: int = None,
                  org_id: str = None) -> TasksResponse:
        """
        Get Tasks

        A Task represents a request or demand for attention/work from agents. Concretely, a telephony Task is an
        incoming call. For chat, a Task is a chat session. For email, a Task is an email chain. This API returns a
        list of Tasks (open or closed) within a date range.

        :param from_: Filter tasks created after given epoch timestamp (in milliseconds).
        :type from_: int
        :param to_: Filter tasks created before given epoch timestamp (in milliseconds). If unspecified, queries up to
            the present.
        :type to_: int
        :param channel_types: Task channel type(s) permitted in response. Must be lowercase. By default, there is no
            channelType filtering.
        :type channel_types: list[str]
        :param page_size: Maximum page size in response. Max allowable value is 1000.
        :type page_size: int
        :param org_id: Organization ID to use for this operation. If unspecified, inferred from token. Token must have
            permission to interact with this organization.
        :type org_id: str
        :rtype: :class:`TasksResponse`
        """
        params = {}
        params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if channel_types is not None:
            params['channelTypes'] = ','.join(channel_types)
        if org_id is not None:
            params['orgId'] = org_id
        if page_size is not None:
            params['pageSize'] = page_size
        url = self.ep('tasks')
        data = super().get(url, params=params)
        r = TasksResponse.model_validate(data)
        return r

    def get_agents_statistics(self, from_: int, to_: int, interval: GetAgentsStatisticsInterval, agent_ids: str = None,
                              org_id: str = None) -> AgentStatsResponse:
        """
        Get Agents Statistics

        Get Agents statistics given a time range.

        :param from_: Start time for the query (in epoch milliseconds). Must have minutes set to one of the 15 minute
            increments within an hour (i.e. XX:00, XX:15, XX:30, XX:45)(e.g. 12:00, 12:15, 12:30, 12:45)
        :type from_: int
        :param to_: End time for the query (in epoch milliseconds). Max of 36 months allowed between `from` and `to`.
            Must have minutes set to one of the 15 minute increments within an hour (i.e. XX:00, XX:15, XX:30,
            XX:45)(e.g. 12:00, 12:15, 12:30, 12:45)
        :type to_: int
        :param interval: Interval value in minutes.
        :type interval: GetAgentsStatisticsInterval
        :param agent_ids: Comma separated list of agent ids. Maximum 100 values permitted. If not supplied, all agents
            for an organization are returned.
        :type agent_ids: str
        :param org_id: Organization ID to use for this operation. If unspecified, inferred from token. Token must have
            permission to interact with this organization.
        :type org_id: str
        :rtype: :class:`AgentStatsResponse`
        """
        params = {}
        params['from'] = from_
        params['to'] = to_
        if agent_ids is not None:
            params['agentIds'] = agent_ids
        if org_id is not None:
            params['orgId'] = org_id
        params['interval'] = enum_str(interval)
        url = self.ep('agents/statistics')
        data = super().get(url, params=params)
        r = AgentStatsResponse.model_validate(data)
        return r

    def get_queues_statistics(self, from_: int, to_: int, interval: GetAgentsStatisticsInterval, queue_ids: str = None,
                              org_id: str = None) -> QueueStatsResponse:
        """
        Get Queues Statistics

        This API will provide queues statistics given a time duration.

        :param from_: Start time for the query (in epoch milliseconds). Must have minutes set to one of the 15 minute
            increments within an hour (i.e. XX:00, XX:15, XX:30, XX:45)(e.g. 12:00, 12:15, 12:30, 12:45)
        :type from_: int
        :param to_: End time for the query (in epoch milliseconds). Max of 36 months allowed between `from` and `to`.
            Must have minutes set to one of the 15 minute increments within an hour (i.e. XX:00, XX:15, XX:30,
            XX:45)(e.g. 12:00, 12:15, 12:30, 12:45)
        :type to_: int
        :param interval: Interval value in minutes.
        :type interval: GetAgentsStatisticsInterval
        :param queue_ids: Comma separated list of queue ids. Maximum 100 values permitted. If not supplied, all queues
            for an organization are returned.
        :type queue_ids: str
        :param org_id: Organization ID to use for this operation. If unspecified, inferred from token. Token must have
            permission to interact with this organization.
        :type org_id: str
        :rtype: :class:`QueueStatsResponse`
        """
        params = {}
        params['from'] = from_
        params['to'] = to_
        if queue_ids is not None:
            params['queueIds'] = queue_ids
        if org_id is not None:
            params['orgId'] = org_id
        params['interval'] = enum_str(interval)
        url = self.ep('queues/statistics')
        data = super().get(url, params=params)
        r = QueueStatsResponse.model_validate(data)
        return r

    def list_captures(self, query: ListCapturesQuery) -> ListCapturesResponse:
        """
        List Captures

        Retrieve a list of captures given a set of taskIds. A capture is a specific snippet of media.

        :type query: ListCapturesQuery
        :rtype: :class:`ListCapturesResponse`
        """
        body = dict()
        body['query'] = query.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('captures/query')
        data = super().post(url, json=body)
        r = ListCapturesResponse.model_validate(data)
        return r
