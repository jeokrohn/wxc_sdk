from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AdminBatchStartJobObject', 'CountObject', 'ErrorMessageObject', 'ErrorObject', 'ErrorResponseObject', 'GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType', 'ItemObject', 'JobExecutionStatusObject', 'JobExecutionStatusObject1', 'JobIdResponseObject', 'JobListResponse', 'MoveNumberValidationError', 'Number', 'NumberItem', 'NumberListGetObject', 'NumberListGetObjectLocation', 'NumberListGetObjectOwner', 'NumberState', 'NumbersDelete', 'NumbersPost', 'StartJobResponse', 'State', 'Status', 'StepExecutionStatusesObject', 'ValidateNumbersResponse']


class NumberItem(ApiModel):
    #: The source location of the numbers to be moved.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzUyMjNiYmVkLTQyYzktNDU0ZC1hMWYzLTdmYWQ1Y2M3ZTZlMw
    location_id: Optional[str] = None
    #: Indicates the numbers to be moved from one location to another location.
    numbers: Optional[list[str]] = None


class AdminBatchStartJobObject(ApiModel):
    #: Indicates the kind of operation to be carried out.
    #: example: MOVE
    operation: Optional[str] = None
    #: The target location within organization where the unassigned numbers will be moved from the source location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    target_location_id: Optional[str] = None
    #: Indicates the numbers to be moved from source to target locations.
    number_list: Optional[list[NumberItem]] = None


class CountObject(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target location ID.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[ErrorObject] = None


class ErrorResponseObject(ApiModel):
    items: Optional[list[ItemObject]] = None


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    start_time: Optional[str] = None
    #: Step execution end time in UTC format.
    end_time: Optional[str] = None
    #: Last updated time for a step in UTC format.
    last_updated: Optional[str] = None
    #: Displays status for a step.
    status_message: Optional[str] = None
    #: Exit Code for a step.
    exit_code: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None


class StartJobResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    job_type: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Indicates operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class JobListResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[StartJobResponse]] = None


class MoveNumberValidationError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
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
    toll_free_number: Optional[bool] = None
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
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner
    #: example: Zand
    last_name: Optional[str] = None


class NumberListGetObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 000
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[str] = None
    #: Type of phone number.
    #: example: PRIMARY
    phone_number_type: Optional[str] = None
    #: Indicates if the phone number is used as location clid.
    #: example: True
    main_number: Optional[bool] = None
    #: Indicates if a phone number is a toll free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    location: Optional[NumberListGetObjectLocation] = None
    owner: Optional[NumberListGetObjectOwner] = None


class NumbersDelete(ApiModel):
    #: List of phone numbers that need to be deleted.
    phone_numbers: Optional[list[str]] = None


class State(str, Enum):
    #: Active state.
    _active_ = 'ACTIVE'
    #: Inactive state
    _inactive_ = 'INACTIVE'


class NumbersPost(ApiModel):
    #: List of phone numbers that need to be added.
    phone_numbers: Optional[list[str]] = None
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
    job_type: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Indicates the operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: The location name for which the job was run.
    source_location_name: Optional[str] = None
    #: The location name for which the numbers have been moved.
    target_location_name: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    auto_attendant = 'AUTO_ATTENDANT'
    call_queue = 'CALL_QUEUE'
    group_paging = 'GROUP_PAGING'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    contact_center_link = 'CONTACT_CENTER_LINK'
    route_list = 'ROUTE_LIST'
    voicemail_group = 'VOICEMAIL_GROUP'
