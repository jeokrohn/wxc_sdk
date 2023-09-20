from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BatchJobError', 'BatchResponse', 'Counts', 'Error', 'ErrorMessage', 'JobExecutionStatus', 'StepExecutionStatuses']


class StepExecutionStatuses(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    startTime: Optional[str] = None
    #: Step execution end time in UTC format.
    endTime: Optional[str] = None
    #: Last updated time for a step in UTC format.
    lastUpdated: Optional[str] = None
    #: Displays status for a step.
    statusMessage: Optional[str] = None
    #: Exit Code for a step.
    exitCode: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    timeElapsed: Optional[str] = None


class JobExecutionStatus(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Job execution start time in UTC format.
    startTime: Optional[str] = None
    #: Job execution end time in UTC format.
    endTime: Optional[str] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: Job creation time in UTC format.
    createdTime: Optional[str] = None
    #: Status of each step within a job.
    stepExecutionStatuses: Optional[list[StepExecutionStatuses]] = None


class Counts(ApiModel):
    #: Indicates the total number of records whose routing prefix update is successful.
    routingPrefixUpdated: Optional[int] = None
    #: Indicates the total number of records whose routing prefix update failed.
    routingPrefixFailed: Optional[int] = None


class BatchResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    trackingId: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    sourceUserId: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    sourceCustomerId: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    targetCustomerId: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instanceId: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    jobExecutionStatus: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Job statistics.
    counts: Optional[Counts] = None


class ErrorMessage(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target location ID.
    locationId: Optional[str] = None


class Error(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessage]] = None


class BatchJobError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    trackingId: Optional[str] = None
    #: row number of failed record.
    itemNumber: Optional[int] = None
    error: Optional[Error] = None
