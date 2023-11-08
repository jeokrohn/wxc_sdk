from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BatchJobError', 'BatchResponse', 'Counts', 'Error', 'ErrorMessage', 'JobExecutionStatus',
            'StepExecutionStatuses']


class StepExecutionStatuses(ApiModel):
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


class JobExecutionStatus(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Job execution start time in UTC format.
    start_time: Optional[str] = None
    #: Job execution end time in UTC format.
    end_time: Optional[str] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit Code for a job.
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    created_time: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatuses]] = None


class Counts(ApiModel):
    #: Indicates the total number of records whose routing prefix update is successful.
    routing_prefix_updated: Optional[int] = None
    #: Indicates the total number of records whose routing prefix update failed.
    routing_prefix_failed: Optional[int] = None


class BatchResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
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
    job_execution_status: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Job statistics.
    counts: Optional[Counts] = None


class ErrorMessage(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    #: location ID.
    location_id: Optional[str] = None


class Error(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessage]] = None


class BatchJobError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    #: row number of failed record.
    item_number: Optional[int] = None
    error: Optional[Error] = None


class BetaCallRoutingWithRoutingPrefixUpdateApi(ApiChild, base='telephony/config/jobs/updateRoutingPrefix'):
    """
    Beta Call Routing with Routing Prefix Update
    
    """

    def get_a_list_of_update_routing_prefix_jobs(self, org_id: str = None) -> list[BatchResponse]:
        """
        Get a List of Update Routing Prefix jobs

        Get the list of all update routing prefix jobs in an organization.
        
        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to retrieve all the update routing prefix jobs in an organization.
        
        Retrieving the list of update routing prefix jobs in an organization requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of update routing prefix jobs in this organization.
        :type org_id: str
        :rtype: list[BatchResponse]
        """
        ...


    def get_the_job_status_of_update_routing_prefix_job(self, job_id: str, org_id: str = None) -> BatchResponse:
        """
        Get the job status of Update Routing Prefix job

        Get the status of the update routing prefix job by its job ID.
        
        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to check the status of update routing prefix job by job ID in an organization.
        
        Checking the status of the update routing prefix job in an organization requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check update routing prefix job status in this organization.
        :type org_id: str
        :rtype: :class:`BatchResponse`
        """
        ...


    def get_job_errors_for_update_routing_prefix_job(self, job_id: str, org_id: str = None) -> BatchJobError:
        """
        Get job errors for update routing prefix job

        GET job errors for the update routing prefix job in an organization.
        
        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to retrieve all the errors of the update routing prefix job by job ID in an organization.
        
        Retrieving all the errors of the update routing prefix job in an organization requires a full, user, or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for update routing prefix job in this organization.
        :type org_id: str
        :rtype: :class:`BatchJobError`
        """
        ...

    ...