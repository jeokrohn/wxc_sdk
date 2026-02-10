from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CountObject', 'ErrorMessageObject', 'ErrorObject', 'ItemObject', 'JobExecutionStatusObject',
           'JobExecutionStatusObject1', 'JobExecutionStatusObjectExitCode', 'JobExecutionStatusObjectStatusMessage',
           'JobIdResponseObject', 'JobListResponseObject', 'Number', 'NumberItem', 'NumberObject',
           'NumberObjectLocation', 'NumberObjectOwner', 'NumberObjectPhoneNumberType', 'NumberOwnerType',
           'NumberState', 'NumberStateOptions', 'NumberType', 'NumberTypeOptions', 'NumberUsageTypeOptions',
           'NumbersApi', 'NumbersRequestAction', 'OwnerType', 'StartJobResponse', 'Status',
           'StepExecutionStatusesObject', 'TelephonyType', 'ValidateNumbersResponse']


class NumberItem(ApiModel):
    #: The source location of the numbers on which to execute the operation.
    location_id: Optional[str] = None
    #: The numbers on which to execute the operation.
    numbers: Optional[list[str]] = None


class CountObject(ApiModel):
    #: The total number of phone numbers requested to be moved.
    total_numbers: Optional[int] = None
    #: The total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int] = None
    #: The total number of phone numbers successfully moved.
    numbers_moved: Optional[int] = None
    #: The total number of phone numbers failed.
    numbers_failed: Optional[int] = None
    #: Count of phone numbers for which usage changed.
    numbers_usage_changed: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    #: location ID.
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


class JobExecutionStatusObjectStatusMessage(str, Enum):
    #: Job has started.
    starting = 'STARTING'
    #: Job is in progress.
    started = 'STARTED'
    #: Job has completed.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'
    #: Job status is unknown.
    unknown = 'UNKNOWN'
    #: Job has been abandoned (manually stopped).
    abandoned = 'ABANDONED'


class JobExecutionStatusObjectExitCode(str, Enum):
    #: Job is in progress.
    unknown = 'UNKNOWN'
    #: Job has completed successfully.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'
    #: Job has been stopped.
    stopped = 'STOPPED'
    #: Job has completed with errors.
    completed_with_errors = 'COMPLETED_WITH_ERRORS'
    #: Job has completed with pending number orders.
    completed_with_pending_orders = 'COMPLETED_WITH_PENDING_ORDERS'


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    end_time: Optional[datetime] = None
    #: Last updated time for a step in UTC format.
    last_updated: Optional[datetime] = None
    #: Displays status for a step.
    status_message: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Exit Code for a step.
    exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: The date and time, including seconds, the job has started in UTC format.
    start_time: Optional[datetime] = None
    #: The date and time, including seconds, the job has started in UTC format.
    end_time: Optional[datetime] = None
    #: Last updated time (in UTC format) for the step completion.
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Exit Code for a job.
    exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: Job creation time in UTC format.
    created_time: Optional[datetime] = None
    #: Time elapsed since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Exit Code for a job.
    exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: Job creation time in UTC format.
    created_time: Optional[datetime] = None
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None


class JobListResponseObject(ApiModel):
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Most recent status of the job at the time of invocation.
    latest_execution_status: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: The operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class NumberState(str, Enum):
    #: The phone number is available.
    available = 'Available'
    #: Duplicate phone number.
    duplicate = 'Duplicate'
    #: Duplicate phone number in the list.
    duplicate_in_list = 'Duplicate In List'
    #: The phone number is invalid.
    invalid = 'Invalid'
    #: The phone number is unavailable and cannot be used.
    unavailable = 'Unavailable'


class Number(ApiModel):
    #: Phone numbers that need to be validated.
    number: Optional[str] = None
    #: The state of the number.
    state: Optional[NumberState] = None
    #: If `true`, it's a toll-free number.
    toll_free_number: Optional[bool] = None
    #: Error details if the number is unavailable.
    detail: Optional[list[str]] = None


class NumberObjectPhoneNumberType(str, Enum):
    #: Filter the results to include only primary phone numbers.
    primary = 'PRIMARY'
    #: Filter the results to include only alternate phone numbers.
    alternate = 'ALTERNATE'
    #: Filter the results to include only FAX phone numbers.
    fax = 'FAX'
    #: Filter the results to include only Dialed Number Identification Service (DNIS) phone numbers.
    dnis = 'DNIS'
    #: Filter the results to include all numbers.
    default = 'Default'


class TelephonyType(str, Enum):
    #: The number is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: The number is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class NumberObjectLocation(ApiModel):
    #: ID of location in which phone number exists.
    id: Optional[str] = None
    #: Name of the location for phone number.
    name: Optional[str] = None


class NumberOwnerType(str, Enum):
    #: The PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: The phone number's owner is a person.
    people = 'PEOPLE'
    #: The PSTN phone number's owner is a virtual line.
    virtual_line = 'VIRTUAL_LINE'
    #: The PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: The PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: The PSTN phone number's owner is a paging group.
    paging_group = 'PAGING_GROUP'
    #: The PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: The PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: The PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: The PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: The PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: The PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: The PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: The PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class NumberObjectOwner(ApiModel):
    #: ID of the owner to which phone number is assigned.
    id: Optional[str] = None
    #: Type of the phone number's owner.
    type: Optional[NumberOwnerType] = None
    #: First name of the phone number's owner.
    first_name: Optional[str] = None
    #: Last name of the phone number's owner.
    last_name: Optional[str] = None


class NumberObject(ApiModel):
    #: A unique identifier for the phone number.
    phone_number: Optional[str] = None
    #: Extension for a phone number.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Phone number's state.
    state: Optional[str] = None
    #: Returns the filtered list of phone numbers of the given `phoneNumberType`. Response excludes any extensions
    #: without numbers. Possible input values:
    phone_number_type: Optional[NumberObjectPhoneNumberType] = None
    #: If `true`, the phone number is used as location CLID.
    main_number: Optional[bool] = None
    #: The telephony type for the number.
    included_telephony_types: Optional[TelephonyType] = None
    #: Mobile Network for the number if the number is MOBILE_NUMBER.
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if the number is MOBILE_NUMBER.
    routing_profile: Optional[str] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number.
    is_service_number: Optional[bool] = None
    location: Optional[NumberObjectLocation] = None
    owner: Optional[NumberObjectOwner] = None


class NumberTypeOptions(str, Enum):
    #: A toll-free PSTN number.
    tollfree = 'TOLLFREE'
    #: A normal Direct Inward Dial (DID) PSTN number.
    did = 'DID'
    #: A mobile number.
    mobile = 'MOBILE'


class NumberUsageTypeOptions(str, Enum):
    #: Standard/user number usage (default).
    none_ = 'NONE'
    #: The number will be used in high-volume service, for example, Contact Center.
    service = 'SERVICE'


class NumberStateOptions(str, Enum):
    #: The number is activated and has calling capability.
    active = 'ACTIVE'
    #: A number is not yet activated and has no calling capability.
    inactive = 'INACTIVE'


class NumbersRequestAction(str, Enum):
    activate = 'ACTIVATE'
    deactivate = 'DEACTIVATE'


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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]] = None
    #: Most recent status of the job at the time of invocation.
    latest_execution_status: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: The operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class Status(str, Enum):
    #: Everything is good.
    ok = 'OK'
    #: Validation has failed with errors.
    errors = 'ERRORS'


class ValidateNumbersResponse(ApiModel):
    #: The status of the numbers.
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Most recent status of the job at the time of invocation.
    latest_execution_status: Optional[JobExecutionStatusObjectStatusMessage] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[JobExecutionStatusObjectExitCode] = None
    #: The operation type that was carried out.
    operation_type: Optional[str] = None
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class OwnerType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    auto_attendant = 'AUTO_ATTENDANT'
    call_queue = 'CALL_QUEUE'
    paging_group = 'PAGING_GROUP'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    contact_center_link = 'CONTACT_CENTER_LINK'
    route_list = 'ROUTE_LIST'
    voicemail_group = 'VOICEMAIL_GROUP'
    virtual_line = 'VIRTUAL_LINE'


class NumberType(str, Enum):
    number = 'NUMBER'
    extension = 'EXTENSION'


class NumbersApi(ApiChild, base='telephony/config'):
    """
    Numbers
    
    Numbers supports reading and writing of Webex Calling phone numbers for a
    specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def validate_phone_numbers(self, phone_numbers: list[str], org_id: str = None) -> ValidateNumbersResponse:
        """
        Validate phone numbers

        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Validating a phone number in an organization requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: :class:`ValidateNumbersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        url = self.ep('actions/validateNumbers/invoke')
        data = super().post(url, params=params, json=body)
        r = ValidateNumbersResponse.model_validate(data)
        return r

    def list_manage_numbers_jobs(self, org_id: str = None, **params) -> Generator[JobListResponseObject, None, None]:
        """
        List Manage Numbers Jobs

        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one irrespective
        of its status.

        The public API only supports initiating jobs which move numbers between locations.

        Via Control Hub they can initiate both the move and delete, so this listing can show both.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`JobListResponseObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/numbers/manageNumbers')
        return self.session.follow_pagination(url=url, model=JobListResponseObject, item_key='items', params=params)

    def initiate_number_jobs(self, operation: str, number_list: list[NumberItem], target_location_id: str = None,
                             number_usage_type: str = None) -> StartJobResponse:
        """
        Initiate Number Jobs

        Starts the execution of an operation on a set of numbers. Supported operations are: `MOVE`,
        `NUMBER_USAGE_CHANGE`.

        Up to 1000 numbers can be given in `MOVE` operation type and `NUMBER_USAGE_CHANGE` operation type per request.
        If another move number job request is initiated while a move job is in progress, the API call will receive a
        `409` HTTP status code.

        In order to move a number the following is required:

        * The number must be unassigned.

        * Both locations must have the same PSTN Connection Type.

        * Both locations must have the same PSTN Provider.

        * Both locations have to be in the same country.

        For example, you can move from Cisco Calling Plan to Cisco Calling Plan, but you cannot move from Cisco Calling
        Plan to a location with Cloud Connected PSTN.

        In order to change the number usage the following is required:

        * The number must be unassigned.

        * Number Usage Type can be set to `NONE` if carrier has the PSTN service `GEOGRAPHIC_NUMBERS`.

        * Number Usage Type can be set to `SERVICE` if carrier has the PSTN service `SERVICE_NUMBERS`.

        For example, you can initiate a `NUMBER_USAGE_CHANGE` job to change the number type from Standard number to
        Service number, or the other way around.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param operation: The kind of operation to be carried out.
        :type operation: str
        :param number_list: Numbers on which to execute the operation.
        :type number_list: list[NumberItem]
        :param target_location_id: Mandatory for a `MOVE` operation. The target location within organization where the
            unassigned numbers will be moved from the source location.
        :type target_location_id: str
        :param number_usage_type: The number usage type. Mandatory for `NUMBER_USAGE_CHANGE` operation.
        :type number_usage_type: str
        :rtype: :class:`StartJobResponse`
        """
        body = dict()
        body['operation'] = operation
        if target_location_id is not None:
            body['targetLocationId'] = target_location_id
        if number_usage_type is not None:
            body['numberUsageType'] = number_usage_type
        body['numberList'] = TypeAdapter(list[NumberItem]).dump_python(number_list, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('jobs/numbers/manageNumbers')
        data = super().post(url, json=body)
        r = StartJobResponse.model_validate(data)
        return r

    def get_manage_numbers_job_status(self, job_id: str) -> JobIdResponseObject:
        """
        Get Manage Numbers Job Status

        Returns the status and other details of the job.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :rtype: :class:`JobIdResponseObject`
        """
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}')
        data = super().get(url)
        r = JobIdResponseObject.model_validate(data)
        return r

    def pause_the_manage_numbers_job(self, job_id: str, org_id: str = None):
        """
        Pause the Manage Numbers Job

        Pause the running Manage Numbers Job. A paused job can be resumed.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Pause the Manage Numbers job for this `jobId`.
        :type job_id: str
        :param org_id: Pause the Manage Numbers job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke')
        super().post(url, params=params)

    def resume_the_manage_numbers_job(self, job_id: str, org_id: str = None):
        """
        Resume the Manage Numbers Job

        Resume the paused Manage Numbers Job. A paused job can be resumed.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Resume the Manage Numbers job for this `jobId`.
        :type job_id: str
        :param org_id: Resume the Manage Numbers job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke')
        super().post(url, params=params)

    def list_manage_numbers_job_errors(self, job_id: str, org_id: str = None,
                                       **params) -> Generator[ItemObject, None, None]:
        """
        List Manage Numbers Job errors

        Lists all error details of Manage Numbers job. This will not list any errors if `exitCode` is `COMPLETED`. If
        the status is `COMPLETED_WITH_ERRORS` then this lists the cause of failures.

        List of possible Errors:

        + BATCH-1017021 - Failed to move because it is an inactive number.

        + BATCH-1017022 - Failed to move because the source location and target location have different CCP providers.

        + BATCH-1017023 - Failed because it is not an unassigned number.

        + BATCH-1017024 - Failed because it is a main number.

        + BATCH-1017027 - Manage Numbers Move Operation is not supported.

        + BATCH-1017031 - Hydra request is supported only for single number move job.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve the error details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def remove_phone_numbers_from_a_location(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove phone numbers from a location

        Remove the specified set of phone numbers from a location for an organization.

        Phone numbers must follow the E.164 format.

        Removing a mobile number may require more time depending on mobile carrier capabilities.

        Removing a phone number from a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        A location's main number cannot be removed.

        <br/>

        <div><Callout type="warning">This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco Calling Plans or Integrated CCP because backend data issues may occur.</Callout></div>

        :param location_id: `LocationId` to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be deleted. The maximum limit is 5.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        url = self.ep(f'locations/{location_id}/numbers')
        super().delete(url, params=params, json=body)

    def add_phone_numbers_to_a_location(self, location_id: str, phone_numbers: list[str],
                                        number_type: NumberTypeOptions = None,
                                        number_usage_type: NumberUsageTypeOptions = None,
                                        state: NumberStateOptions = None, subscription_id: str = None,
                                        carrier_id: str = None, org_id: str = None):
        """
        Add Phone Numbers to a location

        Adds a specified set of phone numbers to a location for an organization. Phone numbers must follow the E.164
        format.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Active phone
        numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        Phone numbers included in the request that already exist in the location will simply be ignored.

        <br/>

        <div><Callout type="warning">This API is only supported for adding DID and Toll-free numbers to non-integrated
        PSTN connection types such as Local Gateway (LGW) and Non-integrated CPP. It should never be used for
        locations with integrated PSTN connection types like Cisco Calling Plans or Integrated CCP because backend
        data issues may occur.
        </Callout></div>
        <div><Callout type="warning">Mobile numbers can be added to any location that has PSTN connection setup. Only
        20 mobile numbers can be added per request.
        </Callout></div>

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param number_type: The type of the number. Required for `MOBILE` number type.
        :type number_type: NumberTypeOptions
        :param number_usage_type: The type of usage expected for the number.
        :type number_usage_type: NumberUsageTypeOptions
        :param state: The state of the number. By default, the state of a number is set to `ACTIVE` for DID and
            toll-free numbers only. Mobile numbers will be activated upon assignment to a user.
        :type state: NumberStateOptions
        :param subscription_id: The `subscriptionId` to be used for the mobile number order.
        :type subscription_id: str
        :param carrier_id: The `carrierId` to be used for the mobile number order.
        :type carrier_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        if number_type is not None:
            body['numberType'] = enum_str(number_type)
        if number_usage_type is not None:
            body['numberUsageType'] = enum_str(number_usage_type)
        if state is not None:
            body['state'] = enum_str(state)
        if subscription_id is not None:
            body['subscriptionId'] = subscription_id
        if carrier_id is not None:
            body['carrierId'] = carrier_id
        url = self.ep(f'locations/{location_id}/numbers')
        super().post(url, params=params, json=body)

    def manage_number_state_in_a_location(self, location_id: str, phone_numbers: list[str],
                                          action: NumbersRequestAction = None, org_id: str = None):
        """
        Manage Number State in a location

        Activate or deactivate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format.

        Active phone numbers are in service. A mobile number is activated when assigned to a user. This API will not
        activate or deactivate mobile numbers.

        Managing phone number state in a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <br/>

        <div><Callout type="warning">This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CCP.</Callout></div>

        :param location_id: `LocationId` to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers whose activation state will be modified according to the specified
            action.
        :type phone_numbers: list[str]
        :param action: Specifies the action to execute on the provided phone numbers. If no action is specified, the
            default is set to ACTIVATE.
        For DEACTIVATE action here are few limitations: 1) a maximum of 500 phone numbers can be processed, 2) the
        numbers must be unassigned, 3) the numbers cannot serve as ECBN (Emergency Callback Number), 4) the numbers
        must not be mobile numbers, and 5) this action is only applicable to non-integrated PSTN connection types,
        specifically Local Gateway (LGW) and Non-integrated CCP
        :type action: NumbersRequestAction
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        if action is not None:
            body['action'] = enum_str(action)
        url = self.ep(f'locations/{location_id}/numbers')
        super().put(url, params=params, json=body)

    def get_phone_numbers_for_an_organization_with_given_criteria(self, location_id: str = None,
                                                                  phone_number: str = None, available: bool = None,
                                                                  order: str = None, owner_name: str = None,
                                                                  owner_id: str = None, owner_type: OwnerType = None,
                                                                  extension: str = None,
                                                                  number_type: NumberType = None,
                                                                  phone_number_type: NumberObjectPhoneNumberType = None,
                                                                  state: NumberStateOptions = None,
                                                                  details: bool = None,
                                                                  toll_free_numbers: bool = None,
                                                                  restricted_non_geo_numbers: bool = None,
                                                                  included_telephony_types: str = None,
                                                                  service_number: bool = None, org_id: str = None,
                                                                  **params) -> Generator[NumberObject, None, None]:
        """
        Get Phone Numbers for an Organization with Given Criteria

        List all the phone numbers for the given organization along with the status and owner (if any).

        Numbers can be standard, service, or mobile. Both standard and service numbers are PSTN numbers.
        Service numbers are considered high-utilization or high-concurrency phone numbers and can be assigned to
        features like auto-attendants, call queues, and hunt groups.
        Phone numbers can be linked to a specific location, be active or inactive, and be assigned or unassigned.
        The owner of a number is the person, workspace, or feature to which the number is assigned.
        Only a person can own a mobile number.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Search for this `phoneNumber`.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with
            `ownerType` parameter when set to `true`.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:`lastName`,`dn`,`extension`. Sorted by
            number and extension in ascending order.
        :type order: str
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with the specified
            UUID or `broadsoftId`.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers of the given `ownerType`. Possible input values:
        :type owner_type: OwnerType
        :param extension: Returns the list of phone numbers with the given extension.
        :type extension: str
        :param number_type: Returns the filtered list of phone numbers that contain a given type of number. `available`
            or `state` query parameters cannot be used when `numberType=EXTENSION`. Possible input values:
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of phone numbers of the given `phoneNumberType`. Response
            excludes any extensions without numbers. Possible input values:
        :type phone_number_type: NumberObjectPhoneNumberType
        :param state: Returns the list of phone numbers with the matching state. Response excludes any extensions
            without numbers. Possible input values:
        :type state: NumberStateOptions
        :param details: Returns the overall count of the phone numbers along with other details for a given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll-free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non-geographical numbers.
        :type restricted_non_geo_numbers: bool
        :param included_telephony_types: Returns the list of phone numbers that are of given `includedTelephonyTypes`.
            By default, if this query parameter is not provided, it will list both PSTN and Mobile Numbers. Possible
            input values are PSTN_NUMBER or MOBILE_NUMBER.
        :type included_telephony_types: str
        :param service_number: Returns the list of service phone numbers.
        :type service_number: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`NumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if available is not None:
            params['available'] = str(available).lower()
        if order is not None:
            params['order'] = order
        if owner_name is not None:
            params['ownerName'] = owner_name
        if owner_id is not None:
            params['ownerId'] = owner_id
        if owner_type is not None:
            params['ownerType'] = enum_str(owner_type)
        if extension is not None:
            params['extension'] = extension
        if number_type is not None:
            params['numberType'] = enum_str(number_type)
        if phone_number_type is not None:
            params['phoneNumberType'] = enum_str(phone_number_type)
        if state is not None:
            params['state'] = enum_str(state)
        if details is not None:
            params['details'] = str(details).lower()
        if toll_free_numbers is not None:
            params['tollFreeNumbers'] = str(toll_free_numbers).lower()
        if restricted_non_geo_numbers is not None:
            params['restrictedNonGeoNumbers'] = str(restricted_non_geo_numbers).lower()
        if included_telephony_types is not None:
            params['includedTelephonyTypes'] = included_telephony_types
        if service_number is not None:
            params['serviceNumber'] = str(service_number).lower()
        url = self.ep('numbers')
        return self.session.follow_pagination(url=url, model=NumberObject, item_key='phoneNumbers', params=params)
