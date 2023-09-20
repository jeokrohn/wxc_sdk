from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CountObject', 'ErrorMessageObject', 'ErrorObject', 'ErrorOrImpactItem', 'ErrorResponseObject', 'ItemObject', 'JobDetailsResponse', 'JobDetailsResponseById', 'JobExecutionStatusObject', 'JobListResponse', 'MoveUsersErrorResponse', 'MoveUsersStartJobObject', 'MoveUsersStartJobResponse', 'MoveUsersValidationResponse', 'StartJobExecutionStatusObject', 'StartJobResponseObject', 'StepExecutionStatusesObject', 'UserItem', 'UserListItem', 'UsersListItem']


class CountObject(ApiModel):
    #: Indicates the total number of user moves requested.
    totalMoves: Optional[int] = None
    #: Indicates the total number of user moves completed.
    moved: Optional[int] = None
    #: Indicates the total number of user moves that failed.
    failed: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location ID in which the error occurs. For a move operation, this is the target location ID.
    locationId: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ErrorOrImpactItem(ApiModel):
    #: Error or Impact code.
    code: Optional[int] = None
    #: Message string with more error or impact information.
    message: Optional[int] = None


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    itemNumber: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    trackingId: Optional[str] = None
    error: Optional[ErrorObject] = None


class ErrorResponseObject(ApiModel):
    items: Optional[list[ItemObject]] = None


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: The date and time with seconds, the step execution has started in UTC format.
    startTime: Optional[str] = None
    #: The date and time with seconds, the step execution has ended in UTC format.
    endTime: Optional[str] = None
    #: The date and time with seconds, the step has last updated in UTC format.
    lastUpdated: Optional[str] = None
    #: Displays status for a step.
    statusMessage: Optional[str] = None
    #: Exit Code for a step.
    exitCode: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    timeElapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: The date and time with seconds, the job has started in UTC format.
    startTime: Optional[str] = None
    #: The date and time with seconds, the job has ended in UTC format.
    endTime: Optional[str] = None
    #: The date and time with seconds, the job has last updated in UTC format post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: The date and time with seconds, the job has created in UTC format.
    createdTime: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    timeElapsed: Optional[str] = None
    #: Status of each step within a job.
    stepExecutionStatuses: Optional[list[StepExecutionStatusesObject]] = None


class JobDetailsResponse(ApiModel):
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
    jobExecutionStatus: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csvFile: Optional[str] = None
    #: The date and time with seconds, the file expires in UTC format.
    csvFileExpiryTime: Optional[str] = None
    #: 'text/csv',  Format of the file generated.
    fileFormat: Optional[str] = None


class JobDetailsResponseById(ApiModel):
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
    jobExecutionStatus: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
    #: Reference ID for the file that holds the errors and impacts.
    csvFile: Optional[str] = None
    #: The date and time with seconds, the file expires in UTC format.
    csvFileExpiryTime: Optional[str] = None
    #: 'text/csv',  Format of the file generated.
    fileFormat: Optional[str] = None
    #: URL to the CSV file containing errors and impacts.
    csvFileDownloadUrl: Optional[str] = None


class JobListResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[JobDetailsResponse]] = None


class MoveUsersErrorResponse(ApiModel):
    #: List of error items.
    error: Optional[list[ErrorOrImpactItem]] = None


class UserItem(ApiModel):
    #: User ID to be moved.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzUyMjNiYmVkLTQyYzktNDU0ZC1hMWYzLTdmYWQ1Y2M3ZTZlMw
    userId: Optional[str] = None
    #: Extension to be moved.
    #: example: 28544
    extension: Optional[str] = None


class UsersListItem(ApiModel):
    #: The target location for the user move.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    locationId: Optional[str] = None
    #: When `true`, validate the user move. When `false`, perform the user move.
    validate: Optional[bool] = None
    #: A list of users to be moved.
    users: Optional[list[UserItem]] = None


class MoveUsersStartJobObject(ApiModel):
    #: The user to be moved from the source location.
    usersList: Optional[list[UsersListItem]] = None


class StartJobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: The date and time with seconds, the job has started in UTC format.
    startTime: Optional[str] = None
    #: The date and time with seconds, the job has last updated in UTC format post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: The date and time with seconds, the job has been created in UTC format.
    createdTime: Optional[str] = None
    #: Time lapsed in seconds since the job execution started.
    timeElapsed: Optional[str] = None


class StartJobResponseObject(ApiModel):
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
    jobExecutionStatus: Optional[list[StartJobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class MoveUsersStartJobResponse(ApiModel):
    #: Response for the user move.
    response: Optional[StartJobResponseObject] = None


class UserListItem(ApiModel):
    #: Associated user ID for the validation response.
    userId: Optional[str] = None
    #: List of impacts for the user move.
    impacts: Optional[list[ErrorOrImpactItem]] = None
    #: List of errors for the user move.
    errors: Optional[list[ErrorOrImpactItem]] = None


class MoveUsersValidationResponse(ApiModel):
    #: Response for the user move validation.
    response: Optional[list[UserListItem]] = None
