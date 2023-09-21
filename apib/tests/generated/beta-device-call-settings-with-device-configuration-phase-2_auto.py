from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BatchJobError', 'BatchResponse', 'Counts', 'Error', 'ErrorMessage', 'GetLineKeyTemplateResponse', 'JobExecutionStatus', 'LineKeyTemplatesResponse', 'LineKeyType', 'PostApplyLineKeyTemplateRequest', 'PostApplyLineKeyTemplateRequestAction', 'PostLineKeyTemplateRequest', 'ProgrammableLineKeys', 'PutLineKeyTemplateRequest', 'StepExecutionStatuses']


class ErrorMessage(ApiModel):
    #: Error message.
    description: Optional[str] = None
    #: Internal error code.
    code: Optional[str] = None
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target location ID.
    location_id: Optional[str] = None


class Error(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessage]] = None


class BatchJobError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str] = None
    error: Optional[Error] = None


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
    step_execution_statuses: Optional[list[StepExecutionStatuses]] = None


class Counts(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int] = None


class BatchResponse(ApiModel):
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
    job_execution_status: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of invocation.
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
    counts: Optional[Counts] = None


class GetLineKeyTemplateResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS81NzVhMWY3Zi03MjRkLTRmZGUtODk4NC1mNjNhNDljMzYxZmQ
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: Basic Template
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: 'DMS Cisco 6821'
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 6821
    model_display_name: Optional[str] = None
    #: Indicates whether user can reorder the line keys.
    user_reorder_enabled: Optional[bool] = None


class LineKeyType(str, Enum):
    #: PRIMARY_LINE is the user's primary extension. This is the default assignment for Line Key Index 1 and cannot be modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables User and Call Park monitoring.
    monitor = 'MONITOR'
    #: Allows users to reach a telephone number, extension or a SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key. These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'


class PostApplyLineKeyTemplateRequestAction(str, Enum):
    #: Used to apply LinekeyTemplate to devices.
    apply_template = 'APPLY_TEMPLATE'
    #: Used to reset devices to its default Linekey Template configurations.
    apply_default_templates = 'APPLY_DEFAULT_TEMPLATES'


class PostApplyLineKeyTemplateRequest(ApiModel):
    #: Line key Template action to perform.
    #: example: APPLY_TEMPLATE
    action: Optional[PostApplyLineKeyTemplateRequestAction] = None
    #: `templateId` is required for `APPLY_TEMPLATE` action.
    #: example: Y2lzY29zcGFyazovL1VTL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS9kNDUzM2MwYi1hZGRmLTRjODUtODk0YS1hZTVkOTAyYzAyMDM=
    template_id: Optional[str] = None
    #: Used to search for devices only in the given locations.
    location_ids: Optional[list[str]] = None
    #: Indicates whether to exclude devices with custom layout.
    exclude_devices_with_custom_layout: Optional[bool] = None
    #: Include devices only with these tags.
    include_device_tags: Optional[list[str]] = None
    #: Exclude devices with these tags.
    exclude_device_tags: Optional[list[str]] = None
    #: Refine search by warnings for More shared appearances than shared users.
    #: example: True
    more_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for Fewer shared appearances than shared users.
    #: example: True
    few_shared_appearances_enabled: Optional[bool] = None
    #: Refine search by warnings for more monitor appearances than monitors.
    #: example: True
    more_monitor_appearances_enabled: Optional[bool] = None


class ProgrammableLineKeys(ApiModel):
    #: An index representing a Line Key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2.0
    line_key_index: Optional[int] = None
    #: The action that would be performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL` and the value must be a valid Telephone Number, Ext, or SIP URI (format: user@host using A-Z,a-z,0-9,-_ .+ for user and host).
    #: example: 5646
    line_key_value: Optional[datetime] = None


class PostLineKeyTemplateRequest(ApiModel):
    #: Name of the Line Key Template.
    #: example: template for 8845
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: DMS Cisco 8845
    device_model: Optional[str] = None
    #: User Customization Enabled.
    #: example: True
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None


class PutLineKeyTemplateRequest(ApiModel):
    #: Indicates whether the user can reorder the line keys.
    #: example: True
    user_reorder_enabled: Optional[bool] = None
    #: List of line keys that are being updated.
    line_keys: Optional[list[ProgrammableLineKeys]] = None


class LineKeyTemplatesResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL1VTL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS9kNDUzM2MwYi1hZGRmLTRjODUtODk0YS1hZTVkOTAyYzAyMDM=
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: template for 8845
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: DMS Cisco 8845
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 8845
    model_display_name: Optional[str] = None
