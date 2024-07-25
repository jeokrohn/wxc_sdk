"""
Jobs API
"""
import json
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union

from pydantic import Field, TypeAdapter

from ...api_child import ApiChild
from ...base import ApiModel, enum_str
from ...common import DeviceCustomization, ApplyLineKeyTemplateAction
from ...rest import RestSession

__all__ = ['StepExecutionStatus', 'JobExecutionStatus', 'StartJobResponse', 'JobErrorMessage', 'JobError',
           'JobErrorItem', 'JobsApi', 'DeviceSettingsJobsApi', 'NumberItem', 'MoveNumberCounts', 'NumberJob',
           'ErrorMessageObject', 'ErrorObject', 'ManageNumberErrorItem', 'ManageNumbersJobsApi',
           'InitiateMoveNumberJobsBody', 'ApplyLineKeyTemplatesJobsApi', 'LineKeyTemplateAdvisoryTypes',
           'ApplyLineKeyTemplateJobDetails', 'RebuildPhonesJobsApi', 'UpdateRoutingPrefixJobsApi',
           'RoutingPrefixCounts', 'MoveCounts', 'MoveUser', 'MoveUsersList',
           'MoveUserJobDetails', 'MoveUsersJobsApi', 'StartMoveUsersJobResponse']


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


class MoveCounts(ApiModel):
    #: Indicates the total number of user moves requested.
    total_moves: Optional[int] = None
    #: Indicates the total number of user moves completed.
    moved: Optional[int] = None
    #: Indicates the total number of user moves that failed.
    failed: Optional[int] = None


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
    counts: Optional[Union[RoutingPrefixCounts, MoveCounts]] = None


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
    item: Optional[str] = None
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
    more_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for Fewer shared appearances than shared users.
    few_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for More monitor appearances than monitors.
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


class MoveUser(ApiModel):
    #: User ID to be moved.
    user_id: Optional[str] = None
    #: Extension to be moved.
    extension: Optional[str] = None
    #: Phone number to be moved.
    phone_number: Optional[str] = None


class MoveUsersList(ApiModel):
    #: The target location for the user move.
    location_id: Optional[str] = None
    #: When `true`, validate the user move. When `false`, perform the user move.
    validate_only: Optional[bool] = Field(alias='validate', default=None)
    #: A list of users to be moved.
    users: Optional[list[MoveUser]] = None


class MoveUserJobDetails(ApiModel):
    #: Job name
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
    #: Indicates the most recent status (`STARTING`,`STARTED`,`COMPLETED`,`FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Job statistics.
    counts: Optional[MoveCounts] = None
    #: Reference ID for the file that holds the errors and impacts.
    csv_file: Optional[str] = None
    #: The date and time with seconds, the file expires in UTC format.
    csv_file_expiry_time: Optional[str] = None
    #: 'text/csv',  Format of the file generated.
    file_format: Optional[str] = None
    #: URL to the CSV file containing errors and impacts.
    csv_file_download_url: Optional[str] = None


class MoveUserCodeAndMessage(ApiModel):
    code: Optional[int] = None
    message: Optional[str] = None


class MoveUserItem(ApiModel):
    user_id: Optional[str] = None
    errors: Optional[list[MoveUserCodeAndMessage]] = None
    impacts: Optional[list[MoveUserCodeAndMessage]] = None


class StartMoveUsersJobResponse(ApiModel):
    users_list: Optional[list[MoveUserItem]] = None
    job_details: Optional[StartJobResponse] = None


class MoveUsersJobsApi(ApiChild, base='telephony/config/jobs/person/moveLocation'):
    def validate_or_initiate(self, users_list: list[MoveUsersList],
                             org_id: str = None) -> StartMoveUsersJobResponse:
        """
        Validate or Initiate Move Users Job

        This API allows the user to perform any one of the following operations:

            * When the `validate` attribute is true, this validates the user move from one location to another location.

            * When the `validate` attribute is false, this performs the user move from one location to another location.

        In order to validate or move a user,

            * Maximum of one calling user can be moved at a time.

            * The target location must be a calling location.

            * Only one new extension can be moved to the target location, which is optional. An empty value will
            remove the
              already configured extension. If not provided, the existing extension will be retained to the user.

            * Only one new phone number belonging to the target location can be assigned to the user, which is optional.
              Phone number must follow E.164 format. An empty value will remove the already configured phone number.
              If not
              provided, the existing phone number of the user will be moved to the target location.

        Any errors that occur during initial API request validation will be captured directly in error response with
        appropriate HTTP status code.

        List of possible Errors:

            + 1026005 - Request is supported only for single user.

            + 1026006 - Attribute 'Location ID' is required.

            + 1026006 - Attribute 'User ID' is required.

            + 1026006 - Attribute 'Validate' is required.

            + 1026010 - User is not a valid Calling User.

            + 1026011 - Users list should not be empty.

            + 1026012 - Users should not be empty.

            + 1026013 - The source and the target location cannot be the same.

            + 1026014 - Error occurred while processing the move users request.

            + 1026015 - Error occurred while moving user number to target location.

            + 1026016 - User should have either phone number or extension.

            + 1026017 - Phone number is not in e164 format.

        When the `validate` is set to be true, the errors and impacts associated with the user move will be identified
        and returned in the response.

        List of possible Errors:

            + 4003 - `User Not Found`

            + 4007 - `User Not Found`

            + 4152 - `Location Not Found`

            + 5620 - `Location Not Found`

            + 4202 - `The extension is not available. It is already assigned to a user : {0}`

            + 8264 - `Routing profile is different with new group: {0}`

            + 19600 - `User has to be within an enterprise to be moved.`

            + 19601 - `User can only be moved to a different group within the same enterprise.`

            + 19602 - `Only regular end user can be moved. Service instance virtual user cannot be moved.`

            + 19603 - `New group already reaches maximum number of user limits.`

            + 19604 - `The {0} number of the user is the same as the calling line ID of the group.`

            + 19605 - `User is assigned services not authorized to the new group: {0}.`

            + 19606 - `User is in an active hoteling/flexible seating association.`

            + 19607 - `User is pilot user of a trunk group.`

            + 19608 - `User is using group level device profiles which is used by other users in current group.
            Following
              are the device profiles shared with other users: {0}.`

            + 19609 - `Following device profiles cannot be moved to the new group because there are already devices with
              the same name defined in the new group: {0}.`

            + 19610 - `The extension of the user is used as transfer to operator number for following Auto Attendent :
              {0}.`

            + 19611 - `Fail to move announcement file from {0} to {1}.`

            + 19612 - `Fail to move device management file from {0} to {1}.`

            + 19613 - `User is assigned service packs not authorized to the new group: {0}.`

            + 25008 - `Missing Mandatory field name: {0}`

            + 25110 - `{fieldName} cannot be less than {0} or greater than {1} characters.`

            + 25378 - `Target location is same as user's current location.`

            + 25379 - `Error Occurred while Fetching User's Current Location Id.`

            + 25381 - `Error Occurred while rolling back to Old Location Call recording Settings`

            + 25382 - `Error Occurred while Disabling Call Recording for user which is required Before User can be
            Moved`

            + 25383 - `OCI Error while moving user`

            + 25384 - `Error Occurred while checking for Possible Call Recording Impact.`

            + 25385 - `Error Occurred while getting Call Recording Settings`

            + 27559 - `The groupExternalId search criteria contains groups with different calling zone.`

            + 27960 - `Parameter isWebexCalling, newPhoneNumber, or newExtension can only be set in Webex Calling
              deployment mode.`

            + 27961 - `Parameter isWebexCalling shall be set if newPhoneNumber or newExtension is set.`

            + 27962 - `Work space cannot be moved.`

            + 27963 - `Virtual profile user cannot be moved.`

            + 27965 - `The user's phone number: {0}, is same as the current group charge number.`

            + 27966 - `The phone number, {0}, is not available in the new group.`

            + 27967 - `User is configured as the ECBN user for another user in the current group.`

            + 27968 - `User is configured as the ECBN user for the current group.`

            + 27969 - `User is associated with DECT handset(s): {0}`

            + 27970 - `User is using a customer managed device: {0}`

            + 27971 - `User is using an ATA device: {0}`

            + 27972 - `User is in an active hotdesking association.`

            + 27975 - `Need to unassign CLID number from group before moving the number to the new group. Phone number:
              {0}`

            + 27976 - `Local Gateway configuration is different with new group. Phone number: {0}`

            + 1026015 - `Error occurred while moving user number to target location`

            + 10010000 - `Total numbers exceeded maximum limit allowed`

            + 10010001 - `to-location and from-location cannot be same`

            + 10010002 - `to-location and from-location should belong to same customer`

            + 10010003 - `to-location must have a carrier`

            + 10010004 - `from-location must have a carrier`

            + 10010005 - `Different Carrier move is not supported for non-Cisco PSTN carriers.`

            + 10010006 - `Number move not supported for WEBEX_DIRECT carriers.`

            + 10010007 - `Numbers out of sync, missing on CPAPI`

            + 10010008 - `from-location not found or pstn connection missing in CPAPI`

            + 10010010 - `from-location is in transition`

            + 10010009 - `to-location not found or pstn connection missing in CPAPI`

            + 10010011 - `to-location is in transition`

            + 10010012 - `Numbers don't have a carrier Id`

            + 10010013 - `Location less numbers don't have a carrier Id`

            + 10010014 - `Different Carrier move is not supported for numbers with different country or region.`

            + 10010015 - `Numbers contain mobile and non-mobile types.`

            + 10010016 - `To/From location carriers must be same for mobile numbers.`

            + 10010017 - `Move request for location less number not supported`

            + 10010200 - `Move request for more than one block number is not supported`

            + 10010201 - `Cannot move block number as few numbers not from the block starting %s to %s`

            + 10010202 - `Cannot move block number as few numbers failed VERIFICATION from the block %s to %s`

            + 10010203 - `Cannot move block number as few numbers missing from the block %s to %s`

            + 10010204 - `Cannot move number as it is NOT a part of the block %s to %s`

            + 10010205 - `Move request for Cisco PSTN block order not supported.`

            + 10010299 - `Move order couldn't be created as no valid number to move`

            + 10030000 - `Number not found`

            + 10030001 - `Number does not belong to from-location`

            + 10030002 - `Number is not present in CPAPI`

            + 10030003 - `Number assigned to an user or device`

            + 10030004 - `Number not in Active status`

            + 10030005 - `Number is set as main number of the location`

            + 10030006 - `Number has pending order associated with it`

            + 10030007 - `Number belongs to a location but a from-location was not set`

            + 10030008 - `Numbers from multiple carrier ids are not supported`

            + 10030009 - `Location less number belongs to a location. from-location value is set to null or no
            location id`

            + 10030010 - `One or more numbers are not portable.`

            + 10030011 - `Mobile number carrier was not set`

            + 10030012 - `Number must be assigned for assigned move`

            + 10050000 - `Failed to update customer reference for phone numbers on carrier`

            + 10050001 - `Failed to update customer reference`

            + 10050002 - `Order is not of operation type MOVE`

            + 10050003 - `CPAPI delete call failed`

            + 10050004 - `Not found in database`

            + 10050005 - `Error sending notification to WxcBillingService`

            + 10050006 - `CPAPI provision number as active call failed with status %s ,reason %s`

            + 10050007 - `Failed to update E911 Service`

            + 10050008 - `Target location does not have Inbound Toll Free license`

            + 10050009 - `Source location or Target location subscription found cancelled or suspended`

            + 10050010 - `Moving On Premises or Non Integrated CCP numbers from one location to another is not
            supported.`

            + 10099999 - `{Error Code} - {Error Message}`

        List of possible Impacts:

            + 19701 - `The identity/device profile the user is using is moved to the new group: {0}.`

            + 19702 - `The user level customized incoming digit string setting is removed from the user. User is set
            to use
              the new group setting.`

            + 19703 - `The user level customized outgoing digit plan setting is removed from the user. User is set to
            use
              the new group setting.`

            + 19704 - `The user level customized enhanced outgoing calling plan setting is removed from the user.
            User is
              set to use the new group setting.`

            + 19705 - `User is removed from following group services: {0}.`

            + 19706 - `The current group schedule used in any criteria is removed from the service settings.`

            + 19707 - `User is removed from the department of the old group.`

            + 19708 - `User is changed to use the default communication barring profile of the new group.`

            + 19709 - `The communication barring profile of the user is assigned to the new group: {0}.`

            + 19710 - `The charge number for the user is removed.`

            + 19711 - `The disabled FACs for the user are removed because they are not available in the new group.`

            + 19712 - `User is removed from trunk group.`

            + 19713 - `The extension of the user is reset to empty due to either the length is out of bounds of the new
              group, or the extension is already taken in new group.`

            + 19714 - `The extension of the following alternate number is reset to empty due to either the length out of
              bounds of the new group or the extension is already taken in new group: {0}.`

            + 19715 - `The collaborate room using current group default collaborate bridge is moved to the default
              collaborate bridge of the new group.`

            + 19716 - `Previously stored voice messages of the user are no longer available. The new voice message
              will be stored on the mail server of the new group.`

            + 19717 - `The primary number, alternate numbers or fax messaging number of the user are assigned to the new
              group: {0}.`

            + 19718 - `Following domains are assigned to the new group: {0}.`

            + 19719 - `The NCOS of the user is assigned to the new group: {0}.`

            + 19720 - `The office zone of the user is assigned to the new group: {0}.`

            + 19721 - `The announcement media files are relocated to the new group directory.`

            + 19722 - `User CLID number is set to use the new group CLID number: {0}.`

            + 19723 - `New group CLID number is not configured.`

            + 19724 - `The group level announcement file(s) are removed from the user's music on hold settings.`

            + 25388 - `Target Location Does not Have Vendor Configured. Call Recording for user will be disabled`

            + 25389 - `Call Recording Vendor for user will be changed from:{0} to:{1}`

            + 25390 - `Dub point of user is moved to new external group`

            + 25391 - `Error Occurred while moving Call recording Settings to new location`

            + 25392 - `Error Occurred while checking for Possible Call Recording Impact.`

            + 25393 - `Sending Billing Notification Failed`

        This API requires a full administrator auth token with a scope
        of `spark-admin:telephony_config_write`, `spark-admin:people_write` and `identity:groups_rw`.

        :param users_list: The user to be moved from the source location.
        :type users_list: list[MoveUsersList]
        :param org_id: Create Move Users job for this organization.
        :type org_id: str
        :rtype: StartJobResponse
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['usersList'] = TypeAdapter(list[MoveUsersList]).dump_python(users_list, mode='json', by_alias=True,
                                                                         exclude_none=True)
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = StartMoveUsersJobResponse.model_validate(data['response'])
        return r

    def list(self, org_id: str = None, **params) -> Generator[MoveUserJobDetails, None, None]:
        """
        List Move Users Jobs

        Lists all the Move Users jobs for the given organization in order of most recent job to oldest job irrespective
        of its status.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of Move Users jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`JobDetailsResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('')
        return self.session.follow_pagination(url=url, model=MoveUserJobDetails, item_key='items', params=params)

    def status(self, job_id: str, org_id: str = None) -> MoveUserJobDetails:
        """
        Get Move Users Job Status

        Returns the status and other details of the job.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve job details for this organization.
        :type org_id: str
        :rtype: :class:`MoveUserJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(job_id)
        data = super().get(url, params=params)
        r = MoveUserJobDetails.model_validate(data)
        return r

    def abandon(self, job_id: str, org_id: str = None):
        """
        Abandon the Move Users Job.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Abandon the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Abandon the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/actions/abandon/invoke')
        super().post(url, params=params)

    def pause(self, job_id: str, org_id: str = None):
        """
        Pause the Move Users Job

        Pause the running Move Users Job. A paused job can be resumed or abandoned.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Pause the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Pause the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/actions/pause/invoke')
        super().post(url, params=params)

    def resume(self, job_id: str, org_id: str = None):
        """
        Resume the Move Users Job

        Resume the paused Move Users Job that is in paused status.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param job_id: Resume the Move Users job for this `jobId`.
        :type job_id: str
        :param org_id: Resume the Move Users job for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/actions/resume/invoke')
        super().post(url, params=params)

    def errors(self, job_id: str, org_id: str = None,
               **params) -> Generator[JobErrorItem, None, None]:
        """
        List Move Users Job errors

        Lists all error details of Move Users job. This will not list any errors if `exitCode` is `COMPLETED`. If the
        status is `COMPLETED_WITH_ERRORS` then this lists the cause of failures.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param job_id: Retrieve the error details for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        :return: Generator yielding :class:`JobErrorItem` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{job_id}/errors')
        return self.session.follow_pagination(url=url, model=JobErrorItem, item_key='items', params=params)


@dataclass(init=False)
class JobsApi(ApiChild, base='telephony/config/jobs'):
    """
    Jobs API
    """
    #: API for apply line key template jobs
    apply_line_key_templates: ApplyLineKeyTemplatesJobsApi
    #: API for device settings jobs
    device_settings: DeviceSettingsJobsApi
    #: API for manage numbers jobs
    manage_numbers: ManageNumbersJobsApi
    # ; API for move users jobs
    move_users: MoveUsersJobsApi
    #: API for rebuild phone jobs
    rebuild_phones: RebuildPhonesJobsApi
    #: API for update routing prefix jobs
    update_routing_prefix: UpdateRoutingPrefixJobsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.apply_line_key_templates = ApplyLineKeyTemplatesJobsApi(session=session)
        self.device_settings = DeviceSettingsJobsApi(session=session)
        self.manage_numbers = ManageNumbersJobsApi(session=session)
        self.move_users = MoveUsersJobsApi(session=session)
        self.rebuild_phones = RebuildPhonesJobsApi(session=session)
        self.update_routing_prefix = UpdateRoutingPrefixJobsApi(session=session)
