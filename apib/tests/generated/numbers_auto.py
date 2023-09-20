from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AdminBatchStartJobObject', 'CountObject', 'ErrorMessageObject', 'ErrorObject', 'ErrorResponseObject', 'ItemObject', 'JobExecutionStatusObject', 'JobExecutionStatusObject1', 'JobIdResponseObject', 'JobListResponse', 'MoveNumberValidationError', 'Number', 'NumberItem', 'NumberListGetObject', 'NumberListGetObjectLocation', 'NumberListGetObjectOwner', 'NumberState', 'NumbersDelete', 'NumbersPost', 'StartJobResponse', 'State', 'Status', 'StepExecutionStatusesObject', 'ValidateNumbersResponse']


class NumberItem(ApiModel):
    #: The source location of the numbers to be moved.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzUyMjNiYmVkLTQyYzktNDU0ZC1hMWYzLTdmYWQ1Y2M3ZTZlMw
    locationId: Optional[str] = None
    #: Indicates the numbers to be moved from one location to another location.
    numbers: Optional[list[str]] = None


class AdminBatchStartJobObject(ApiModel):
    #: Indicates the kind of operation to be carried out.
    #: example: MOVE
    operation: Optional[str] = None
    #: The target location within organization where the unassigned numbers will be moved from the source location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    targetLocationId: Optional[str] = None
    #: Indicates the numbers to be moved from source to target locations.
    numberList: Optional[list[NumberItem]] = None


class CountObject(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    totalNumbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbersDeleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbersMoved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbersFailed: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target location ID.
    locationId: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


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


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: Job creation time in UTC format.
    createdTime: Optional[str] = None
    #: Time lapsed since the job execution started.
    timeElapsed: Optional[str] = None
    #: Status of each step within a job.
    stepExecutionStatuses: Optional[list[StepExecutionStatusesObject]] = None


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: Job creation time in UTC format.
    createdTime: Optional[str] = None
    #: Time lapsed since the job execution started.
    timeElapsed: Optional[str] = None


class StartJobResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    jobType: Optional[str] = None
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
    jobExecutionStatus: Optional[list[JobExecutionStatusObject1]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Indicates operation type that was carried out.
    operationType: Optional[str] = None
    #: Unique location identifier for which the job was run.
    sourceLocationId: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    targetLocationId: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class JobListResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[StartJobResponse]] = None


class MoveNumberValidationError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    trackingId: Optional[str] = None
    error: Optional[ErrorObject] = None


class NumberState(str, Enum):
    #: Phone number is available.
    available = 'AVAILABLE'
    #: Duplicate phone number.
    duplicate = 'DUPLICATE'
    #: Duplicate phone number in the list.
    duplicateinlist = 'DUPLICATEINLIST'
    #: Phone number is invalid.
    invalid = 'INVALID'
    #: Phone number is unavailable and cannot be used.
    unavailable = 'UNAVAILABLE'


class Number(ApiModel):
    #: Phone numbers that need to be validated.
    #: example: +2145557901
    number: Optional[str] = None
    #: Indicates the state of the number.
    state: Optional[NumberState] = None
    #: Indicates whether it's a toll-free number.
    tollFreeNumber: Optional[bool] = None
    #: Error details if the number is unavailable.
    detail: Optional[list[str]] = None


class NumberListGetObjectLocation(ApiModel):
    #: ID of location for phone number.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    id: Optional[str] = None
    #: Name of the location for phone number
    #: example: Banglore
    name: Optional[str] = None


class NumberListGetObjectOwner(ApiModel):
    #: ID of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner
    #: example: PEOPLE
    type: Optional[str] = None
    #: First name of the PSTN phone number's owner
    #: example: Mark
    firstName: Optional[str] = None
    #: Last name of the PSTN phone number's owner
    #: example: Zand
    lastName: Optional[str] = None


class NumberListGetObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phoneNumber: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 000
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[str] = None
    #: Type of phone number.
    #: example: PRIMARY
    phoneNumberType: Optional[str] = None
    #: Indicates if the phone number is used as location clid.
    #: example: True
    mainNumber: Optional[bool] = None
    #: Indicates if a phone number is a toll free number.
    #: example: True
    tollFreeNumber: Optional[bool] = None
    location: Optional[NumberListGetObjectLocation] = None
    owner: Optional[NumberListGetObjectOwner] = None


class NumbersDelete(ApiModel):
    #: List of phone numbers that need to be deleted.
    phoneNumbers: Optional[list[str]] = None


class State(str, Enum):
    #: Active state.
    _active_ = 'ACTIVE'
    #: Inactive state
    _inactive_ = 'INACTIVE'


class NumbersPost(ApiModel):
    #: List of phone numbers that need to be added.
    phoneNumbers: Optional[list[str]] = None
    #: State of the phone numbers.
    state: Optional[State] = None


class Status(str, Enum):
    #: Everything is good.
    ok = 'OK'
    #: Validation has failed with errors.
    errors = 'ERRORS'


class ValidateNumbersResponse(ApiModel):
    #: Indicates the status of the numbers.
    status: Optional[Status] = None
    #: An array of number objects with number details.
    numbers: Optional[list[Number]] = None


class JobIdResponseObject(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    jobType: Optional[str] = None
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
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Indicates the operation type that was carried out.
    operationType: Optional[str] = None
    #: Unique location identifier for which the job was run.
    sourceLocationId: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    targetLocationId: Optional[str] = None
    #: The location name for which the job was run.
    sourceLocationName: Optional[str] = None
    #: The location name for which the numbers have been moved.
    targetLocationName: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None
