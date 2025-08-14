from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BulkActivationEmailResendJobCounts', 'BulkActivationEmailResendJobDetails',
           'BulkActivationEmailResendJobDetailsLatestExecutionExitCode', 'ErrorMessageObject', 'ErrorObject',
           'ExecutionStatus', 'ItemObject', 'SendActivationEmailApi', 'StepExecutionStatus']


class BulkActivationEmailResendJobDetailsLatestExecutionExitCode(str, Enum):
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


class ExecutionStatus(str, Enum):
    #: Step or job has completed.
    completed = 'COMPLETED'
    #: Step or job is starting.
    starting = 'STARTING'
    #: Step or job is running.
    started = 'STARTED'
    #: Step or job is stopping.
    stopping = 'STOPPING'
    #: Step or job has failed with an error.
    failed = 'FAILED'
    #: Step or job has been abandone (manually stopped).
    abandoned = 'ABANDONED'
    #: Step or job status is unknown.
    unknown = 'UNKNOWN'


class StepExecutionStatus(ApiModel):
    #: Unique identifier of the step
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    start_time: Optional[str] = None
    #: Step execution end time in UTC format.
    end_time: Optional[str] = None
    #: Last time the step's execution status was updated in UTC format.
    last_updated: Optional[str] = None
    #: Displays the most recent execution status of the step.
    status_message: Optional[ExecutionStatus] = None
    #: Final execution status of the step.
    exit_code: Optional[ExecutionStatus] = None
    #: Step name.
    name: Optional[str] = None
    #: Time elapsed since the step execution started.
    time_elapsed: Optional[str] = None


class BulkActivationEmailResendJobCounts(ApiModel):
    #: Count of users sent an invitation.
    user_resend_invite_sent: Optional[int] = None
    #: Count of users who failed to receive an invitation.
    user_resend_invite_failed: Optional[int] = None
    #: Count of users who were skipped.
    user_resend_invite_skipped: Optional[int] = None
    #: Total count of users processed.
    total_users: Optional[int] = None


class BulkActivationEmailResendJobDetails(ApiModel):
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
    #: Contains the execution statuses of all the steps involved in the execution of the job.
    job_execution_status: Optional[list[StepExecutionStatus]] = None
    #: Indicates the most recent status of the job at the time of invocation.
    latest_execution_status: Optional[ExecutionStatus] = None
    #: Most recent exit code of the job at the time of invocation.
    latest_execution_exit_code: Optional[BulkActivationEmailResendJobDetailsLatestExecutionExitCode] = None
    #: Summary of statuses.
    counts: Optional[BulkActivationEmailResendJobCounts] = None
    #: Indicates if the org allows admin invite emails to be sent.
    allow_admin_invite_emails: Optional[bool] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Not used.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP status code.
    key: Optional[str] = None
    #: List of error messages.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Index of error.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP request.
    tracking_id: Optional[str] = None
    #: Error details.
    error: Optional[ErrorObject] = None


class SendActivationEmailApi(ApiChild, base='identity/organizations'):
    """
    Send Activation Email
    
    APIs allowing an admin to send activation emails to users.
    """

    def initiate_bulk_activation_email_resend_job(self, org_id: str) -> BulkActivationEmailResendJobDetails:
        """
        Initiate Bulk Activation Email Resend Job

        Initiate a bulk activation email resend job that sends an activation email to all eligible users in an
        organization. Only a single instance of the job can be running for an organization.

        Requires a full or user administrator auth token with a scope of `spark-admin:people_write`.

        :param org_id: Initiate job for this organization.
        :type org_id: str
        :rtype: :class:`BulkActivationEmailResendJobDetails`
        """
        url = self.ep(f'{org_id}/jobs/sendActivationEmails')
        data = super().post(url)
        r = BulkActivationEmailResendJobDetails.model_validate(data)
        return r

    def get_bulk_activation_email_resend_job_errors(self, org_id: str, job_id: str,
                                                    **params) -> Generator[ItemObject, None, None]:
        """
        Get Bulk Activation Email Resend Job Errors

        Get errors of an activation email resend job by its job ID.

        Requires a full or user administrator auth token with a scope of `spark-admin:people_write` or read-only
        administrator auth token with a scope of `spark-admin:people_read`.

        :param org_id: Check job status for this organization.
        :type org_id: str
        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        url = self.ep(f'{org_id}/jobs/sendActivationEmails/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def get_bulk_activation_email_resend_job_status(self, org_id: str,
                                                    job_id: str) -> BulkActivationEmailResendJobDetails:
        """
        Get Bulk Activation Email Resend Job Status

        Get the details of an activation email resend job by its job ID.

        Requires a full or user administrator auth token with a scope of `spark-admin:people_write` or read-only
        administrator auth token with a scope of `spark-admin:people_read`.

        :param org_id: Check job status for this organization.
        :type org_id: str
        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :rtype: :class:`BulkActivationEmailResendJobDetails`
        """
        url = self.ep(f'{org_id}/jobs/sendActivationEmails/{job_id}/status')
        data = super().get(url)
        r = BulkActivationEmailResendJobDetails.model_validate(data)
        return r
