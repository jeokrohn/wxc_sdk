from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AdminBatchStartJobObject', 'CountObject', 'ErrorMessageObject', 'ErrorObject', 'ErrorResponseObject',
            'GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType', 'ItemObject', 'JobExecutionStatusObject',
            'JobExecutionStatusObject1', 'JobIdResponseObject', 'JobListResponse', 'MoveNumberValidationError',
            'Number', 'NumberItem', 'NumberListGetObject', 'NumberObject', 'NumberObjectLocation',
            'NumberObjectOwner', 'NumberState', 'NumbersDelete', 'NumbersPost', 'StartJobResponse', 'State', 'Status',
            'StepExecutionStatusesObject', 'ValidateNumbersResponse']


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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
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


class NumberObjectLocation(ApiModel):
    #: ID of location for phone number.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    id: Optional[str] = None
    #: Name of the location for phone number
    #: example: Banglore
    name: Optional[str] = None


class NumberObjectOwner(ApiModel):
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


class NumberObject(ApiModel):
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
    location: Optional[NumberObjectLocation] = None
    owner: Optional[NumberObjectOwner] = None


class NumberListGetObject(ApiModel):
    #: Array of phone numbers.
    phone_numbers: Optional[list[NumberObject]] = None


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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
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

    def add_phone_numbers_to_a_location(self, location_id: str, phone_numbers: list[str], state: State,
                                        org_id: str = None):
        """
        Add Phone Numbers to a location

        Adds a specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <br/>

        <div><Callout type="warning">This API is only supported for Local Gateway (LGW) connected locations. It is not
        supported and should not be used for non-LGW connected locations because backend data issues may
        occur.</Callout></div>

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param state: State of the phone numbers.
        :type state: State
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['phoneNumbers'] = phone_numbers
        body['state'] = enum_str(state)
        url = self.ep(f'locations/{location_id}/numbers')
        super().post(url, params=params, json=body)

    def activate_phone_numbers_in_a_location(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate Phone Numbers in a location

        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Activating a phone number in a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <br/>

        <div><Callout type="warning">This API is only supported for Local Gateway (LGW) connected locations. It is not
        supported and should not be used for non-LGW connected locations because backend data issues may
        occur.</Callout></div>

        :param location_id: `LocationId` to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
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
        super().put(url, params=params, json=body)

    def remove_phone_numbers_from_a_location(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove phone numbers from a location

        Remove the specified set of phone numbers from a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Removing a phone number from a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <br/>

        <div><Callout type="warning">This API is only supported for Local Gateway (LGW) connected locations. It is not
        supported and should not be used for non-LGW connected locations because backend data issues may
        occur.</Callout></div>

        :param location_id: `LocationId` to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be deleted.
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

    def validate_phone_numbers_(self, phone_numbers: list[str], org_id: str = None) -> ValidateNumbersResponse:
        """
        Validate phone numbers.

        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

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

    def get_phone_numbers_for_an_organization_with_given_criterias(self, location_id: str = None, start: int = None,
                                                                   phone_number: str = None, available: bool = None,
                                                                   order: str = None, owner_name: str = None,
                                                                   owner_id: str = None,
                                                                   owner_type: GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType = None,
                                                                   extension: str = None, number_type: str = None,
                                                                   phone_number_type: str = None, state: str = None,
                                                                   details: bool = None,
                                                                   toll_free_numbers: bool = None,
                                                                   restricted_non_geo_numbers: bool = None,
                                                                   org_id: str = None,
                                                                   **params) -> Generator[NumberObject, None, None]:
        """
        Get Phone Numbers for an Organization with Given Criterias

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param start: Start at the zero-based offset in the list of matching phone numbers. Default is 0.
        :type start: int
        :param phone_number: Search for this `phoneNumber`.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with
            `ownerType` parameter when set to `true`.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:`lastName`,`dn`,`extension`. Default sort
            will be based on number and extension in an ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given `ownerName`. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given `ownerType`. Possible input values
        :type owner_type: GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType
        :param extension: Returns the list of PSTN phone numbers with the given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers. This
            parameter cannot be used along with `available` or `state`.
        :type number_type: str
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given `phoneNumberType`.
        :type phone_number_type: str
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: str
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`NumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if start is not None:
            params['start'] = start
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
            params['ownerType'] = owner_type
        if extension is not None:
            params['extension'] = extension
        if number_type is not None:
            params['numberType'] = number_type
        if phone_number_type is not None:
            params['phoneNumberType'] = phone_number_type
        if state is not None:
            params['state'] = state
        if details is not None:
            params['details'] = str(details).lower()
        if toll_free_numbers is not None:
            params['tollFreeNumbers'] = str(toll_free_numbers).lower()
        if restricted_non_geo_numbers is not None:
            params['restrictedNonGeoNumbers'] = str(restricted_non_geo_numbers).lower()
        url = self.ep('numbers')
        return self.session.follow_pagination(url=url, model=NumberObject, item_key='phoneNumbers', params=params)

    def list_manage_numbers_jobs(self, start: int = None, org_id: str = None,
                                 **params) -> Generator[StartJobResponse, None, None]:
        """
        List Manage Numbers Jobs

        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one irrespective
        of its status.

        The public API only supports initiating jobs which move numbers between locations.

        Via Control Hub they can initiate both the move and delete, so this listing can show both.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param start: Start at the zero-based offset in the list of jobs. Default is 0.
        :type start: int
        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`StartJobResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        url = self.ep('jobs/numbers/manageNumbers')
        return self.session.follow_pagination(url=url, model=StartJobResponse, item_key='items', params=params)

    def initiate_move_number_jobs(self, operation: str, target_location_id: str,
                                  number_list: list[NumberItem]) -> StartJobResponse:
        """
        Initiate Move Number Jobs

        Starts the numbers move from one location to another location. Although jobs can do both MOVE and DELETE
        actions internally, only MOVE is supported publicly.

        <br/>

        In order to move a number,

        <br/>

        * The number must be unassigned.

        * Both locations must have the same PSTN Connection Type.

        * Both locations must have the same PSTN Provider.

        * Both locations have to be in the same country.

        <br/>

        For example, you can move from Cisco PSTN to Cisco PSTN, but you cannot move from Cisco PSTN to a location with
        Cloud Connected PSTN.

        <br/>

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param operation: Indicates the kind of operation to be carried out.
        :type operation: str
        :param target_location_id: The target location within organization where the unassigned numbers will be moved
            from the source location.
        :type target_location_id: str
        :param number_list: Indicates the numbers to be moved from source to target locations.
        :type number_list: list[NumberItem]
        :rtype: :class:`StartJobResponse`
        """
        body = dict()
        body['operation'] = operation
        body['targetLocationId'] = target_location_id
        body['numberList'] = loads(TypeAdapter(list[NumberItem]).dump_json(number_list, by_alias=True, exclude_none=True))
        url = self.ep('jobs/numbers/manageNumbers')
        data = super().post(url, json=body)
        r = StartJobResponse.model_validate(data)
        return r

    def get_manage_numbers_job_status(self, job_id: str = None) -> JobIdResponseObject:
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

    def pause_the_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Pause the Manage Numbers Job

        Pause the running Manage Numbers Job. A paused job can be resumed or abandoned.

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

    def resume_the_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Resume the Manage Numbers Job

        Resume the paused Manage Numbers Job. A paused job can be resumed or abandoned.

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

    def abandon_the_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Abandon the Manage Numbers Job

        Abandon the Manage Numbers Job.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Abandon the Manage Numbers job for this `jobId`.
        :type job_id: str
        :param org_id: Abandon the Manage Numbers job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke')
        super().post(url, params=params)

    def list_manage_numbers_job_errors(self, job_id: str = None, start: int = None, org_id: str = None,
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
        :param start: Specifies the error offset from the first result that you want to fetch.
        :type start: int
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)
