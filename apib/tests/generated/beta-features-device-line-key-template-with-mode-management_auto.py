from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ApplyLineKeyTemplateJobDetails', 'ApplyLineKeyTemplateJobDetailsLatestExecutionExitCode',
           'BetaFeaturesDeviceLineKeyTemplatesWithModeManagementApi', 'GetLineKeyTemplateResponse',
           'JobExecutionStatusObject', 'LineKeyTemplateAdvisoryTypes', 'LineKeyType',
           'PostApplyLineKeyTemplateRequestAction', 'ProgrammableLineKeys', 'StepExecutionStatusesObject']


class LineKeyType(str, Enum):
    #: `PRIMARY_LINE` is the user's primary extension. This is the default assignment for `Line Key Index` 1 and cannot
    #: be modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables user and call park monitoring.
    monitor = 'MONITOR'
    #: Enables the configure layout feature in Control Hub to set call park extension implicitly.
    call_park_extension = 'CALL_PARK_EXTENSION'
    #: Allows users to reach a telephone number, extension, or a SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key.
    #: These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'
    #: Allows users to manage call forwarding for features via schedule-based routing.
    mode_management = 'MODE_MANAGEMENT'


class ProgrammableLineKeys(ApiModel):
    #: An index representing a line key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2
    line_key_index: Optional[int] = None
    #: The action that would be performed when the line key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: This is applicable only when the `lineKeyType` is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: This is applicable only when the `lineKeyType` is `SPEED_DIAL` and the value must be a valid telephone number,
    #: ext, or SIP URI (format: user@host using A-Z,a-z,0-9,-_ .+ for user and host).
    #: example: 5646
    line_key_value: Optional[str] = None


class GetLineKeyTemplateResponse(ApiModel):
    #: Unique identifier for the `Line Key Template`.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS81NzVhMWY3Zi03MjRkLTRmZGUtODk4NC1mNjNhNDljMzYxZmQ
    id: Optional[str] = None
    #: Name of the `Line Key Template`.
    #: example: Basic Template
    template_name: Optional[str] = None
    #: The device model for which the `Line Key Template` is applicable.
    #: example: 'DMS Cisco 6821'
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 6821
    model_display_name: Optional[str] = None
    #: Indicates whether the user can reorder the line keys.
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of line keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None


class PostApplyLineKeyTemplateRequestAction(str, Enum):
    #: Used to apply `LinekeyTemplate` to devices.
    apply_template = 'APPLY_TEMPLATE'
    #: Used to reset devices to their default `Linekey Template` configurations.
    apply_default_templates = 'APPLY_DEFAULT_TEMPLATES'


class LineKeyTemplateAdvisoryTypes(ApiModel):
    #: Refine search to apply changes to devices that contain the warning "More shared/virtual line appearances than
    #: shared/virtual lines requested".
    #: example: True
    more_shared_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More shared/virtual lines requested than
    #: shared/virtual line appearances".
    #: example: True
    few_shared_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More monitored line appearances than
    #: monitored lines in the user's monitoring list".
    #: example: True
    more_monitor_appearances_enabled: Optional[bool] = None
    #: Refine search to apply changes to devices that contain the warning "More call park extension line appearances
    #: than call park extensions in user's monitoring list".
    #: example: True
    more_cpeappearances_enabled: Optional[bool] = Field(alias='moreCPEAppearancesEnabled', default=None)
    #: Refine search to apply changes to devices that contain the warning "More mode management lines configured for
    #: the device". The default value is false.
    #: example: True
    more_mode_management_appearances_enabled: Optional[bool] = None


class ApplyLineKeyTemplateJobDetailsLatestExecutionExitCode(str, Enum):
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


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    #: example: 1998857
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T03:58:36.886Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T03:58:48.471Z
    end_time: Optional[datetime] = None
    #: Last updated time for a step in UTC format.
    #: example: 2024-03-13T03:58:48.472Z
    last_updated: Optional[datetime] = None
    #: Displays the status of a step.
    #: example: COMPLETED
    status_message: Optional[str] = None
    #: Exit code for a step.
    #: example: COMPLETED
    exit_code: Optional[str] = None
    #: Name of different steps the job goes through.
    #: example: rebuildphonesProcess
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    #: example: PT11.585S
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    #: example: 436272
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    end_time: Optional[datetime] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    #: example: 2024-03-13T14:57:04.678Z
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    #: example: STARTING
    status_message: Optional[str] = None
    #: Exit code for a job.
    #: example: UNKNOWN
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    created_time: Optional[datetime] = None
    #: Time lapsed since the job execution started.
    #: example: PT0S
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


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
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of
    #: invocation.
    latest_execution_status: Optional[str] = None
    #: Most recent exit code of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_exit_code: Optional[ApplyLineKeyTemplateJobDetailsLatestExecutionExitCode] = None
    #: Indicates the progress of the job.
    percentage_complete: Optional[str] = None
    #: Number of job steps completed.
    updated_count: Optional[str] = None
    #: Number of job steps completed with advisories.
    advisory_count: Optional[str] = None


class BetaFeaturesDeviceLineKeyTemplatesWithModeManagementApi(ApiChild, base='telephony/config'):
    """
    Beta Features: Device Line Key Templates with Mode Management
    
    Device Call Settings
    
    These APIs manage Webex Calling settings for devices of the Webex Calling type.
    
    Viewing these read-only device settings requires a full, device, or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def create_a_line_key_template(self, template_name: str, device_model: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None) -> str:
        """
        Create a Line Key Template

        Create a `Line Key Template` in this organization.

        Line keys, also known as programmable line keys (PLK), are the keys found on either side of a typical desk
        phone display. A `Line Key Template` is a definition of actions that will be performed by each of the line
        keys for a particular device model. This API allows customers to create a `Line Key Template` for a device
        model.

        Creating a `Line Key Template` requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_name: Name of the `Line Key Template`.
        :type template_name: str
        :param device_model: The model of the device for which the `Line Key Template` is applicable. The corresponding
            device model display name, sometimes called the product name, can also be used to specify the model.
        :type device_model: str
        :param line_keys: Contains a mapping of line keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: User customization enabled.
        :type user_reorder_enabled: bool
        :param org_id: `Organization` to which the line key template belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['templateName'] = template_name
        body['deviceModel'] = device_model
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/lineKeyTemplates')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_details_of_a_line_key_template(self, template_id: str, org_id: str = None) -> GetLineKeyTemplateResponse:
        """
        Get Details of a Line Key Template

        Get detailed information about a `Line Key Template` by `template ID` in an organization.

        Line keys, also known as programmable line keys (PLK), are the keys found on either side of a typical desk
        phone display. A `Line Key Template` is a definition of actions that will be performed by each of the line
        keys for a particular device model. This API allows users to retrieve a line key template by its ID in an
        organization.

        Retrieving a line key template requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param template_id: Get line key template for this `template ID`.
        :type template_id: str
        :param org_id: Retrieve a line key template for this `organization`.
        :type org_id: str
        :rtype: :class:`GetLineKeyTemplateResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        data = super().get(url, params=params)
        r = GetLineKeyTemplateResponse.model_validate(data)
        return r

    def modify_a_line_key_template(self, template_id: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None):
        """
        Modify a Line Key Template

        Modify a `Line Key Template` by its `template ID` in an organization.

        Line keys, also known as programmable line keys (PLK), are the keys found on either side of a typical desk
        phone display. A `Line Key Template` is a definition of actions that will be performed by each of the line
        keys for a particular device model. This API allows users to modify an existing `Line Key Template` by its ID
        in an organization.

        Modifying an existing `Line Key Template` requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_id: Modify line key template with this `template ID`.
        :type template_id: str
        :param line_keys: List of line keys that are being updated.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: Indicates whether the user can reorder the line keys.
        :type user_reorder_enabled: bool
        :param org_id: Modify a line key template for this `organization`.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        super().put(url, params=params, json=body)

    def preview_apply_line_key_template(self, action: PostApplyLineKeyTemplateRequestAction, template_id: str,
                                        location_ids: list[str] = None,
                                        exclude_devices_with_custom_layout: bool = None,
                                        include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
                                        advisory_types: LineKeyTemplateAdvisoryTypes = None,
                                        org_id: str = None) -> int:
        """
        Preview Apply Line Key Template

        Preview the number of devices that will be affected by the application of a `Line Key Template` or when
        resetting devices to their factory line key settings.

        Line keys, also known as programmable line keys (PLK), are the keys found on either side of a typical desk
        phone display. A `Line Key Template` is a definition of actions that will be performed by each of the line
        keys for a particular device model. This API allows users to preview the number of devices that will be
        affected if a customer were to apply a `Line Key Template` or apply factory default line key settings to
        devices.

        Retrieving the number of devices affected requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param action: Line key template action to perform.
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
        :param org_id: Preview `Line Key Template` for this `organization`.
        :type org_id: str
        :rtype: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
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
            body['advisoryTypes'] = advisory_types.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/actions/previewApplyLineKeyTemplate/invoke')
        data = super().post(url, params=params, json=body)
        r = data['deviceCount']
        return r

    def apply_a_line_key_template(self, action: PostApplyLineKeyTemplateRequestAction, template_id: str,
                                  location_ids: list[str] = None, exclude_devices_with_custom_layout: bool = None,
                                  include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
                                  advisory_types: LineKeyTemplateAdvisoryTypes = None,
                                  org_id: str = None) -> ApplyLineKeyTemplateJobDetails:
        """
        Apply a Line Key Template

        Apply a `Line Key Template` or reset devices to their factory line key settings.

        Line keys, also known as programmable line keys (PLK), are the keys found on either side of a typical desk
        phone display. A `Line Key Template` is a definition of actions that will be performed by each of the line
        keys for a particular device model. This API allows users to apply a line key template or apply factory
        default line key settings to devices in a set of locations or across all locations in the organization.

        Applying a `Line Key Template` or resetting devices to their default line key configuration requires a full
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param action: Line key template action to perform.
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
        :param org_id: Apply `Line Key Template` for this `organization`.
        :type org_id: str
        :rtype: :class:`ApplyLineKeyTemplateJobDetails`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
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
            body['advisoryTypes'] = advisory_types.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('jobs/devices/applyLineKeyTemplate')
        data = super().post(url, params=params, json=body)
        r = ApplyLineKeyTemplateJobDetails.model_validate(data)
        return r
