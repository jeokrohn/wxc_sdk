"""
Jobs API
"""
import json
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from pydantic import Field, TypeAdapter

from ...base import ApiModel, enum_str
from ...common import DeviceCustomization, ApplyLineKeyTemplateAction
from ...rest import RestSession
from ...api_child import ApiChild

__all__ = ['StepExecutionStatus', 'JobExecutionStatus', 'StartJobResponse', 'JobErrorMessage', 'JobError',
           'JobErrorItem', 'JobsApi', 'DeviceSettingsJobsApi', 'NumberItem', 'MoveNumberCounts', 'NumberJob',
           'ErrorMessageObject', 'ErrorObject', 'ManageNumberErrorItem', 'ManageNumbersJobsApi',
           'InitiateMoveNumberJobsBody', 'ApplyLineKeyTemplatesJobsApi', 'LineKeyTemplateAdvisoryTypes',
           'ApplyLineKeyTemplateJobDetails', 'RebuildPhonesJobsApi', 'UpdateRoutingPrefixJobsApi',
           'RoutingPrefixCounts']


class StepExecutionStatus(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: int
    #: Step execution start time.
    start_time: datetime
    #: Step execution end time.
    end_time: Optional[datetime] = None
    #: Last updated time for a step.
    last_updated: datetime
    #: Displays status for a step.
    status_message: str
    #: ExitCode for a step.
    exit_code: str
    #: Step name.
    name: str
    #: Time lapsed since the step execution started.
    time_elapsed: str


class JobExecutionStatus(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: int
    #: Step execution start time.
    start_time: Optional[datetime] = None
    #: Step execution end time.
    end_time: Optional[datetime] = None
    #: Last updated time post one of the step execution completion.
    last_updated: datetime
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str] = None
    #: Exit code for a job.
    exit_code: Optional[str] = None
    #: Job creation time.
    created_time: datetime
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: list[StepExecutionStatus] = Field(default_factory=list)

class RoutingPrefixCounts(ApiModel):
    #: Indicates the total number of records whose routing prefix update is successful.
    routing_prefix_updated: Optional[int] = None
    #: Indicates the total number of records whose routing prefix update failed.
    routing_prefix_failed: Optional[int] = None

class StartJobResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: str
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: str
    #: Unique identifier to identify which user has run the job.
    source_user_id: str
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: str
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: str
    #: Unique identifier to identify the instance of the job.
    instance_id: int
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involve in the
    #: execution of the job.
    job_execution_status: list[JobExecutionStatus]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, or FAILED) of the job at the time of invocation.
    latest_execution_status: str
    #: indicates if all the devices within this location will be customized with new requested customizations(if set to
    #: true) or will be overridden with the one at organization level (if set to false or any other value). This field
    #: has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool] = None
    #: Indicates if the job was run at organization level ('CUSTOMER') or location ('LOCATION') level.
    target: Optional[str] = None
    #: Unique location identifier for which the job was run.
    location_id: Optional[str] = None
    #: name of location for which the job was run, only present for target LOCATION
    location_name: Optional[str] = None
    #: Displays job completion percentage
    percentage_complete: Optional[int] = None
    #: Count of number of devices rebuilt.
    device_count: Optional[int] = None
    #: Job statistics.
    counts: Optional[RoutingPrefixCounts] = None


class JobErrorMessage(ApiModel):
    #: Error message.
    description: str
    #: Internal error code.
    code: Optional[str] = None
    #: Message describing the location or point of failure.
    location: Optional[str] = None
    location_id: Optional[str] = None


class JobError(ApiModel):
    #: HTTP error code.
    key: str
    message: list[JobErrorMessage]


class JobErrorItem(ApiModel):
    #: Index of error number.
    item_number: int
    #: Unique identifier to track the HTTP requests.
    tracking_id: str
    error: JobError


class DeviceSettingsJobsApi(ApiChild, base='telephony/config/jobs/devices/callDeviceSettings'):
    """
    API for jobs to update device settings at the location and organization level

    """

    def change(self, location_id: Optional[str], customization: DeviceCustomization,
               org_id: str = None) -> StartJobResponse:
        """
        Change device settings across organization or locations jobs.

        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system
        admins in a stateful persistent manner. This job will modify the requested device settings across all the
        devices. Whenever a location ID is specified in the request, it will modify the requested device settings only
        for the devices that are part of the provided location within an organization.

        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.

        Only one job per customer can be running at any given time within the same organization. An attempt to run
        multiple jobs at the same time will result in a 409 error response.

        Running a job requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location within an organization where changes of device settings will be applied to all the
            devices within it.
        :type location_id: str
        :param customization: customization. Atttribute custom_enabled Indicates if all the devices within this
            location will be customized with new requested customizations(if set to true) or will be overridden with
            the one at organization level (if set to false or any other value). This field has no effect when the job
            is being triggered at organization level.
        :type customization: DeviceCustomization
        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :return: information about the created job
        :rtype: StartJobResponse
        """
        url = self.ep()
        params = org_id and {'prgId': org_id} or None
        body = {}
        if location_id:
            body['locationId'] = location_id
            body['locationCustomizationsEnabled'] = customization.custom_enabled
        if customization.custom_enabled or not location_id:
            body['customizations'] = json.loads(customization.customizations.model_dump_json())
        data = self.post(url=url, params=params, json=body)
        return StartJobResponse.model_validate(data)

    def list(self, org_id: str = None, **params) -> Generator[StartJobResponse, None, None]:
        """
        List change device settings jobs.

        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to
        oldest one irrespective of its status.

        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str
        :param params: optional parameters
        :return: Generator of :class:`StartJobResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=StartJobResponse, params=params)

    def status(self, job_id: str, org_id: str = None) -> StartJobResponse:
        """
        Get change device settings job status.

        Provides details of the job with jobId of jobType calldevicesettings.

        This API requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        :param org_id: Retrieve job details for this org
        :type org_id: str
        :return: job details
        :rtype: StartJobResponse
        """
        url = self.ep(job_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return StartJobResponse.model_validate(data)

    def errors(self, job_id: str, org_id: str = None) -> Generator[JobErrorItem, None, None]:
        """
        List change device settings job errors.

        Lists all error details of the job with jobId of jobType calldevicesettings.

        This API requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :param org_id: Retrieve list of jobs for this organization.
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{job_id}/errors')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=JobErrorItem, params=params)


class NumberItem(ApiModel):
    #: The source location of the numbers to be moved.
    location_id: Optional[str] = None
    #: Indicates the numbers to be moved from one location to another location.
    numbers: Optional[list[str]] = None


class MoveNumberCounts(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int] = None
    numbers_activated: Optional[int] = None
    numbers_usage_changed: Optional[int] = None


class NumberJob(ApiModel):
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: job name
    name: Optional[str] = None
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
    # execution of the job.
    job_execution_status: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str] = None
    #: Indicates operation type that was carried out.
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
    counts: Optional[MoveNumberCounts] = None


class ErrorMessageObject(ApiModel):
    code: Optional[str] = None
    description: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    # location ID.
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    message: Optional[list[ErrorMessageObject]] = None


class ManageNumberErrorItem(ApiModel):
    #: Phone number
    item: Optional[str] = None
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[ErrorObject] = None


class InitiateMoveNumberJobsBody(ApiModel):
    #: Indicates the kind of operation to be carried out.
    operation: Optional[str] = None
    #: The target location within organization where the unassigned numbers will be moved from the source location.
    target_location_id: Optional[str] = None
    #: Indicates the numbers to be moved from source to target locations.
    number_list: Optional[list[NumberItem]] = None


class ManageNumbersJobsApi(ApiChild, base='telephony/config/jobs/numbers'):
    """
    API for jobs to manage numbers
    """

    def list(self, org_id: str = None, **params) -> Generator[NumberJob, None, None]:
        """
        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one
        irrespective of its status.
        The public API only supports initiating jobs which move numbers between locations.
        Via Control Hub they can initiate both the move and delete, so this listing can show both.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('manageNumbers')
        return self.session.follow_pagination(url=url, model=NumberJob, params=params)

    def initiate_job(self, operation: str, target_location_id: str,
                     number_list: List[NumberItem]) -> NumberJob:
        """
        Starts the numbers move from one location to another location. Although jobs can do both MOVE and DELETE
        actions internally, only MOVE is supported publicly.
        In order to move a number,
        For example, you can move from Cisco PSTN to Cisco PSTN, but you cannot move from Cisco PSTN to a location
        with Cloud Connected PSTN.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param operation: Indicates the kind of operation to be carried out.
        :type operation: str
        :param target_location_id: The target location within organization where the unassigned numbers will be moved
            from the source location.
        :type target_location_id: str
        :param number_list: Indicates the numbers to be moved from source to target locations.
        :type number_list: list[NumberItem]
        """
        body = InitiateMoveNumberJobsBody(operation=operation,
                                          target_location_id=target_location_id,
                                          number_list=number_list)
        url = self.ep('manageNumbers')
        data = super().post(url=url, data=body.model_dump_json())
        return NumberJob.model_validate(data)

    def status(self, job_id: str = None) -> NumberJob:
        """
        Returns the status and other details of the job.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        """
        url = self.ep(f'manageNumbers/{job_id}')
        data = super().get(url=url)
        return NumberJob.model_validate(data)

    def pause(self, job_id: str = None, org_id: str = None):
        """
        Pause the running Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Pause the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Pause the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/pause/invoke')
        super().post(url=url, params=params)
        return

    def resume(self, job_id: str = None, org_id: str = None):
        """
        Resume the paused Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Resume the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Resume the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/resume/invoke')
        super().post(url=url, params=params)
        return

    def abandon(self, job_id: str = None, org_id: str = None):
        """
        Abandon the Manage Numbers Job.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Abandon the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Abandon the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/abandon/invoke')
        super().post(url=url, params=params)
        return

    def errors(self, job_id: str = None, org_id: str = None,
               **params) -> Generator[ManageNumberErrorItem, None, None]:
        """
        Lists all error details of Manage Numbers job. This will not list any errors if exitCode is COMPLETED. If the
        status is COMPLETED_WITH_ERRORS then this lists the cause of failures.
        List of possible Errors:
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve the error details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ManageNumberErrorItem, params=params)


class LineKeyTemplateAdvisoryTypes(ApiModel):
    #: Refine search by warnings for More shared appearances than shared users.
    #: example: True
    more_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for Fewer shared appearances than shared users.
    #: example: True
    few_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for More monitor appearances than monitors.
    #: example: True
    more_monitor_appearances_enabled: Optional[bool] = None


class ApplyLineKeyTemplateJobDetails(ApiModel):
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
    #: Indicates the progress of the job.
    percentage_complete: Optional[int] = None
    #: Number of job steps completed.
    updated_count: Optional[int] = None
    #: Number of job steps completed with advisories.
    advisory_count: Optional[int] = None


class ApplyLineKeyTemplatesJobsApi(ApiChild, base='telephony/config/jobs/devices/applyLineKeyTemplate'):
    def apply(self, action: ApplyLineKeyTemplateAction, template_id: str = None,
              location_ids: list[str] = None, exclude_devices_with_custom_layout: bool = None,
              include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
              advisory_types: LineKeyTemplateAdvisoryTypes = None,
              org_id: str = None) -> ApplyLineKeyTemplateJobDetails:
        """
        Apply a Line key Template

        Apply a Line Key Template or reset devices to their factory Line Key settings.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to apply a line key template or apply factory default Line Key settings to devices in a
        set of locations or across all locations in the organization.

        Applying a Line Key Template or resetting devices to their default Line Key configuration requires a full
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param action: Line key Template action to perform.
        :type action: PostApplyLineKeyTemplateRequestAction
        :param template_id: `templateId` is required for `APPLY_TEMPLATE` action.
        :type template_id: str
        :param location_ids: Used to search for devices only in the given locations.
        :type location_ids: list[str]
        :param exclude_devices_with_custom_layout: Indicates whether to exclude devices with custom layout.
        :type exclude_devices_with_custom_layout: bool
        :param include_device_tags: Include devices only with these tags.
        :type include_device_tags: list[str]
        :param exclude_device_tags: Exclude devices with these tags.
        :type exclude_device_tags: list[str]
        :param advisory_types: Refine search with advisories.
        :type advisory_types: LineKeyTemplateAdvisoryTypes
        :param org_id: Apply Line Key Template for this organization.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
        if template_id is not None:
            body['templateId'] = template_id
        if location_ids is not None:
            body['locationIds'] = location_ids
        if exclude_devices_with_custom_layout is not None:
            body['excludeDevicesWithCustomLayout'] = exclude_devices_with_custom_layout
        if include_device_tags is not None:
            body['includeDeviceTags'] = include_device_tags
        if exclude_device_tags is not None:
            body['excludeDeviceTags'] = exclude_device_tags
        if advisory_types is not None:
            body['advisoryTypes'] = json.loads(advisory_types.model_dump_json())
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = ApplyLineKeyTemplateJobDetails.model_validate(data)
        return r

    def list(self, org_id: str = None) -> list[ApplyLineKeyTemplateJobDetails]:
        """
        Get List of Apply Line Key Template jobs

        Get the list of all apply line key templates jobs in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve all the apply line key templates jobs in an organization.

        Retrieving the list of apply line key templates jobs in an organization requires a full, user or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of line key templates jobs in this organization.
        :type org_id: str
        :rtype: list[ApplyLineKeyTemplateJobDetails]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ApplyLineKeyTemplateJobDetails]).validate_python(data['items'])
        return r

    def status(self, job_id: str, org_id: str = None) -> ApplyLineKeyTemplateJobDetails:
        """
        Get the job status of an Apply Line Key Template job

        Get the status of an apply line key template job by its job ID.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to check the status of an apply line key templates job by job ID in an organization.

        Checking the the status of an apply line key templates job in an organization requires a full, user or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check a line key template job status in this organization.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(job_id)
        data = super().get(url, params=params)
        r = ApplyLineKeyTemplateJobDetails.model_validate(data)
        return r

    def errors(self, job_id: str, org_id: str = None) -> Generator[JobErrorItem, None, None]:
        """
        Get job errors for an Apply Line Key Template job

        GET job errors for an apply Line Key Template job in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve all the errors of an apply line key templates job by job ID in an
        organization.

        Retrieving all the errors of an apply line key templates job in an organization requires a full, user or
        read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for an apply line key template job in this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/errors')
        return self.session.follow_pagination(url=url, model=JobErrorItem, params=params)


class RebuildPhonesJobsApi(ApiChild, base='telephony/config/jobs/devices/rebuildPhones'):
    def rebuild_phones_configuration(self, location_id: str, org_id: str = None) -> StartJobResponse:
        """
        Rebuild Phones Configuration

        Rebuild all phone configurations for the specified location.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Unique identifier of the location.
        :type location_id: str
        :param org_id: Rebuild phones for this organization.
        :type org_id: str
        :rtype: :class:`RebuildPhonesJob`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['locationId'] = location_id
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = StartJobResponse.model_validate(data)
        return r

    def list(self, org_id: str = None) -> list[StartJobResponse]:
        """
        List Rebuild Phones Jobs

        Get the list of all Rebuild Phones jobs in an organization.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: List of rebuild phones jobs in this organization.
        :type org_id: str
        :rtype: list[RebuildPhonesJob]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[StartJobResponse]).validate_python(data['items'])
        return r

    def status(self, job_id: str, org_id: str = None) -> StartJobResponse:
        """
        Get the Job Status of a Rebuild Phones Job

        Get the details of a rebuild phones job by its job ID.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check a rebuild phones job status in this organization.
        :type org_id: str
        :rtype: :class:`RebuildPhonesJob`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}')
        data = super().get(url, params=params)
        r = StartJobResponse.model_validate(data)
        return r

    def errors(self, job_id: str, org_id: str = None) -> Generator[JobErrorItem, None, None]:
        """
        Get Job Errors for a Rebuild Phones Job

        Get errors for a rebuild phones job in an organization.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of errors for a rebuild phones job in this organization.
        :type org_id: str
        :rtype: list[ItemObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/errors')
        return self.session.follow_pagination(url=url, model=JobErrorItem, params=params)


class UpdateRoutingPrefixJobsApi(ApiChild, base='telephony/config/jobs/updateRoutingPrefix'):
    def list(self, org_id: str = None) -> Generator[StartJobResponse, None, None]:
        """
        Get a List of Update Routing Prefix jobs

        Get the list of all update routing prefix jobs in an organization.

        The routing prefix is associated with a location and is used to route calls belonging to that location.
        This API allows users to retrieve all the update routing prefix jobs in an organization.

        Retrieving the list of update routing prefix jobs in an organization requires a full, user, or read-only
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of update routing prefix jobs in this organization.
        :type org_id: str
        :rtype: list[StartJobResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=StartJobResponse, params=params, item_key='items')

    def status(self, job_id: str, org_id: str = None) -> StartJobResponse:
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
        :rtype: :class:`StartJobResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(job_id)
        data = super().get(url, params=params)
        r = StartJobResponse.model_validate(data)
        return r

    def errors(self, job_id: str, org_id: str = None) -> Generator[JobErrorItem, None, None]:
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
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/errors')
        return self.session.follow_pagination(url=url, model=JobErrorItem, params=params)


@dataclass(init=False)
class JobsApi(ApiChild, base='telephony/config/jobs'):
    """
    Jobs API
    """
    #: API for device settings jobs
    device_settings: DeviceSettingsJobsApi
    #: API for manage numbers jobs
    manage_numbers: ManageNumbersJobsApi
    #: API for apply line key template jobs
    apply_line_key_templates: ApplyLineKeyTemplatesJobsApi
    #: API for rebuild phone jobs
    rebuild_phones: RebuildPhonesJobsApi
    #: API for update routing prefix jobs
    update_routing_prefix: UpdateRoutingPrefixJobsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.device_settings = DeviceSettingsJobsApi(session=session)
        self.manage_numbers = ManageNumbersJobsApi(session=session)
        self.apply_line_key_templates = ApplyLineKeyTemplatesJobsApi(session=session)
        self.rebuild_phones = RebuildPhonesJobsApi(session=session)
        self.update_routing_prefix = UpdateRoutingPrefixJobsApi(session=session)
