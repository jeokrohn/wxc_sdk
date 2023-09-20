from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AgentStats', 'AgentStatsChannel', 'AgentStatsChannelChannelType', 'AgentStatsResponse', 'Artifact', 'ArtifactAttributes', 'FieldValidationError', 'ListCapturesResponse', 'Meta', 'QueueStats', 'QueueStatsResponse', 'Recording', 'RecordingStatus', 'Task', 'TaskAttributes', 'TaskAttributesContext', 'TaskAttributesStatus', 'TaskOwner', 'TaskWithCaptures', 'TasksResponse', 'TasksValidationError']


class Meta(ApiModel):
    #: Organization ID.
    #: example: e767c439-08bf-48fa-a03c-ac4a09eeee8f
    orgId: Optional[str] = None


class TaskOwner(ApiModel):
    #: ID of the agent last assigned to this task.
    #: example: e0c7611b-8035-443a-b7a8-dca9f8b8289b
    id: Optional[str] = None
    #: Name of the agent last assigned to this task.
    #: example: Joseph Lambert
    name: Optional[str] = None


class TaskAttributesContext(ApiModel):
    ...


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
    channelType: Optional[str] = None
    #: Created time of the task (epoch milliseconds).
    #: example: 1591702170000.0
    createdTime: Optional[int] = None
    #: Last updated time of the task (epoch milliseconds). Updates whenever the underlying data is modified, even if the Task view of the data is the same. May also update after task "closure", so not suitable for finding a task's "closed time".
    #: example: 1591712170099.0
    lastUpdatedTime: Optional[int] = None
    owner: Optional[TaskOwner] = None
    queue: Optional[TaskOwner] = None
    context: Optional[TaskAttributesContext] = None
    #: Customer's channel-specific identifier. For telephony, this is the phone number. For email and chat, this is the email address.
    #: example: chatuser@email.com
    origin: Optional[str] = None
    #: Destination the customer contacted. For telephony, this is the number the contact called. For chat, this is the URL of the page where the chat takes place. For email, it is the email address contacted.
    #: example: +18005555555
    destination: Optional[str] = None
    #: Indicates which party initiated the Task. If "inbound", call was initated by customer. If "outbound", was initiated by system as part of campaign. If "outdial", was initiated by an agent.
    #: example: inbound
    direction: Optional[str] = None
    #: Reason code specified by customer to indicate main aim of the task.
    #: example: Credit
    reasonCode: Optional[str] = None
    #: Whether a capture has been requested for this Task. If this is true, a capture should eventually be available. False indicates no capture will be made available. If null, it is not yet known whether a capture has been requested.
    captureRequested: Optional[bool] = None
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


class FieldValidationError(ApiModel):
    #: example: pageSize
    field: Optional[str] = None
    #: example: Invalid pageSize parameter
    message: Optional[str] = None


class TasksValidationError(ApiModel):
    fieldErrors: Optional[list[FieldValidationError]] = None
    #: example: INTEGRATION-9bcdc696-57fa-4e91-b5aa-57a66a347c23
    trackingId: Optional[str] = None
    #: example: The request was not processed
    message: Optional[str] = None
    #: example: 400.0
    code: Optional[int] = None


class AgentStatsChannelChannelType(str, Enum):
    telephony = 'telephony'
    chat = 'chat'
    email = 'email'
    social = 'social'


class AgentStatsChannel(ApiModel):
    #: Channel GUID
    #: example: 91fada7d-6be8-46e8-b6af-8598e71b7e27
    channelId: Optional[str] = None
    #: example: telephony
    channelType: Optional[AgentStatsChannelChannelType] = None
    #: Number of assigned tasks within this channel during the agent's session.
    #: example: 3.0
    totalAssignedTasks: Optional[int] = None
    #: Number of accepted tasks that were assigned to the agent.
    #: example: 3.0
    totalAcceptedTasks: Optional[int] = None
    #: Number of rejected tasks that were assigned to the agent.
    totalRejectedTasks: Optional[int] = None
    #: Number of tasks the agent transferred to another agent.
    totalTransferredTasks: Optional[int] = None
    #: Amount of time the agent was engaged with a customer (in milliseconds).
    #: example: 40302.0
    totalEngagedDuration: Optional[int] = None
    #: Amount of time the customer(s) was put on hold (in milliseconds).
    #: example: 10198.0
    totalHoldDuration: Optional[int] = None
    #: Amount of time the agent spent wrapping-up customer interactions (in milliseconds).
    #: example: 3552.0
    totalWrapUpDuration: Optional[int] = None


class AgentStats(ApiModel):
    #: Time in GMT
    #: example: 1591702200000.0
    intervalStartTime: Optional[int] = None
    #: Agent GUID
    #: example: 06ce7234-dd3e-49e2-8763-d93766739d3
    agentId: Optional[str] = None
    #: example: Jim Bob
    agentName: Optional[str] = None
    #: Team GUID
    #: example: fbf80248-b328-4c37-9ea5-4c2ec8b4d52c
    teamId: Optional[str] = None
    #: Name of team to which the agent belongs.
    #: example: Ghost Riders
    teamName: Optional[str] = None
    #: Time that the agent's status was set to 'Available'.
    #: example: 54052.0
    totalAvailableTime: Optional[int] = None
    #: Time that the agent's status was set to 'Unavailable'.
    totalUnavailableTime: Optional[int] = None
    channel: Optional[list[AgentStatsChannel]] = None


class AgentStatsResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    #: List of agent stats for each queried agent.
    data: Optional[list[AgentStats]] = None


class QueueStats(ApiModel):
    #: Time in GMT (milliseconds).
    #: example: 1591702200000.0
    intervalStartTime: Optional[int] = None
    #: Queue ID
    #: example: 06ce7234-dd3e-49e2-8763-d93766739d3
    queueId: Optional[str] = None
    #: example: MainInbound
    queueName: Optional[str] = None
    #: example: telephony
    channelType: Optional[AgentStatsChannelChannelType] = None
    #: example: 7.0
    totalOfferedTasks: Optional[int] = None
    #: example: 7.0
    totalEnqueuedTasks: Optional[int] = None
    #: example: 7.0
    totalAssignedTasks: Optional[int] = None
    #: example: 7.0
    totalAcceptedTasks: Optional[int] = None
    totalRejectedTasks: Optional[int] = None
    totalAbandonedTasks: Optional[int] = None
    #: example: 20349.0
    averageEnqueuedTime: Optional[int] = None
    #: example: 93729.0
    averageHandleTime: Optional[int] = None


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
    fileName: Optional[str] = None
    #: Capture download url.
    #: example: https://cjp-ccone-devus1-media-storage-recording.s3.amazonaws.com/9e4895c9-787b-4615-b15f-f1b3b12c3091/
    filePath: Optional[str] = None
    #: Begin time of capture
    #: example: 1591804052000.0
    startTime: Optional[int] = None
    #: End time of capture
    #: example: 1591804562000.0
    stopTime: Optional[int] = None
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
    taskId: Optional[str] = None
    recording: Optional[Recording] = None


class ListCapturesResponse(ApiModel):
    #: Response metadata.
    meta: Optional[Meta] = None
    data: Optional[list[TaskWithCaptures]] = None
