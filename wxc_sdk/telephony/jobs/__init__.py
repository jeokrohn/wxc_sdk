"""
Jobs API
"""
import json
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ApiModel
from ...common import DeviceCustomization
from ...rest import RestSession
from ...api_child import ApiChild

__all__ = ['StepExecutionStatus', 'JobExecutionStatus', 'StartJobResponse', 'JobErrorMessage', 'JobError',
           'JobErrorItem', 'JobsApi', 'DeviceSettingsJobsApi']


class StepExecutionStatus(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: str
    #: Step execution start time.
    start_time: datetime
    #: Step execution end time.
    end_time: Optional[datetime]
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
    id: str
    #: Step execution start time.
    start_time: Optional[datetime]
    #: Step execution end time.
    end_time: Optional[datetime]
    #: Last updated time post one of the step execution completion.
    last_updated: datetime
    #: Displays status for overall steps that are part of the job.
    status_message: str
    #: Exit code for a job.
    exit_code: str
    #: Job creation time.
    created_time: datetime
    #: Time lapsed since the job execution started.
    time_elapsed: str
    #: Status of each step within a job.
    step_execution_statuses: list[StepExecutionStatus] = Field(default_factory=list)


class StartJobResponse(ApiModel):
    #: Job name.
    name: Optional[str]
    #: Unique identifier of the job.
    id: str
    #: Job type.
    job_type: str
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: str
    #: Unique identifier to identify which user has run the job.
    source_user_id: str
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: str
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: str
    #: Unique identifier to identify the instance of the job.
    instance_id: str
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involve in the
    #: execution of the job.
    job_execution_status: list[JobExecutionStatus]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, or FAILED) of the job at the time of invocation.
    latest_execution_status: str
    #: indicates if all the devices within this location will be customized with new requested customizations(if set to
    #: true) or will be overridden with the one at organization level (if set to false or any other value). This field
    #: has no effect when the job is being triggered at organization level.
    location_customizations_enabled: bool
    #: Indicates if the job was run at organization level ('CUSTOMER') or location ('LOCATION') level.
    target: str
    #: Unique location identifier for which the job was run.
    location_id: str
    #: name of location for which the job was run, only present for target LOCATION
    location_name: Optional[str]
    #: Displays job completion percentage
    percentage_complete: str
    device_count: Optional[int]


class JobErrorMessage(ApiModel):
    #: Error message.
    description: str
    #: Internal error code.
    code: str
    #: Message describing the location or point of failure.
    location: str


class JobError(ApiModel):
    #: HTTP error code.
    key: str
    message: JobErrorMessage


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
            body['customizations'] = json.loads(customization.customizations.json())
        data = self.post(url=url, params=params, json=body)
        return StartJobResponse.parse_obj(data)

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

    def get_status(self, job_id: str, org_id: str = None) -> StartJobResponse:
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
        return StartJobResponse.parse_obj(data)

    def job_errors(self, job_id: str, org_id: str = None) -> Generator[JobErrorItem, None, None]:
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


@dataclass(init=False)
class JobsApi(ApiChild, base='telephony/config/jobs'):
    """
    Jobs API
    """
    #: API for device settings jobs
    device_settings: DeviceSettingsJobsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.device_settings = DeviceSettingsJobsApi(session=session)
