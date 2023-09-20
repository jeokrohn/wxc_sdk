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
    locationId: Optional[str] = None


class Error(ApiModel):
    #: HTTP error code.
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessage]] = None


class BatchJobError(ApiModel):
    #: Unique identifier to track the HTTP requests.
    trackingId: Optional[str] = None
    error: Optional[Error] = None


class StepExecutionStatuses(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    startTime: Optional[str] = None
    #: Step execution end time in UTC format.
    endTime: Optional[str] = None
    #: Last updated time for a step in UTC format.
    lastUpdated: Optional[str] = None
    #: Displays status for a step.
    statusMessage: Optional[str] = None
    #: Exit Code for a step.
    exitCode: Optional[str] = None
    #: Step name.
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    timeElapsed: Optional[str] = None


class JobExecutionStatus(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    lastUpdated: Optional[str] = None
    #: Displays status for overall steps that are part of the job.
    statusMessage: Optional[str] = None
    #: Exit Code for a job.
    exitCode: Optional[str] = None
    #: Job creation time in UTC format.
    createdTime: Optional[str] = None
    #: Time lapsed since the job execution started.
    timeElapsed: Optional[str] = None
    #: Status of each step within a job.
    stepExecutionStatuses: Optional[list[StepExecutionStatuses]] = None


class Counts(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    totalNumbers: Optional[int] = None
    #: Indicates the total number of phone numbers successfully deleted.
    numbersDeleted: Optional[int] = None
    #: Indicates the total number of phone numbers successfully moved.
    numbersMoved: Optional[int] = None
    #: Indicates the total number of phone numbers failed.
    numbersFailed: Optional[int] = None


class BatchResponse(ApiModel):
    #: Job name.
    name: Optional[str] = None
    #: Unique identifier of the job.
    id: Optional[str] = None
    #: Job type.
    jobType: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    trackingId: Optional[str] = None
    #: Unique identifier to identify which user has run the job.
    sourceUserId: Optional[str] = None
    #: Unique identifier to identify the customer who has run the job.
    sourceCustomerId: Optional[str] = None
    #: Unique identifier to identify the customer for which the job was run.
    targetCustomerId: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    instanceId: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the execution of the job.
    jobExecutionStatus: Optional[list[JobExecutionStatus]] = None
    #: Indicates the most recent status (`STARTING`, `STARTED`, `COMPLETED`, `FAILED`) of the job at the time of invocation.
    latestExecutionStatus: Optional[str] = None
    #: Indicates the operation type that was carried out.
    operationType: Optional[str] = None
    #: Unique location identifier for which the job was run.
    sourceLocationId: Optional[str] = None
    #: Unique location identifier for which the numbers have been moved.
    targetLocationId: Optional[str] = None
    #: The location name for which the job was run.
    sourceLocationName: Optional[str] = None
    #: The location name for which the numbers have been moved.
    targetLocationName: Optional[str] = None
    #: Job statistics.
    counts: Optional[Counts] = None


class GetLineKeyTemplateResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS81NzVhMWY3Zi03MjRkLTRmZGUtODk4NC1mNjNhNDljMzYxZmQ
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: Basic Template
    templateName: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: 'DMS Cisco 6821'
    deviceModel: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 6821
    modelDisplayName: Optional[str] = None
    #: Indicates whether user can reorder the line keys.
    userReorderEnabled: Optional[bool] = None


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
    templateId: Optional[str] = None
    #: Used to search for devices only in the given locations.
    locationIds: Optional[list[str]] = None
    #: Indicates whether to exclude devices with custom layout.
    excludeDevicesWithCustomLayout: Optional[bool] = None
    #: Include devices only with these tags.
    includeDeviceTags: Optional[list[str]] = None
    #: Exclude devices with these tags.
    excludeDeviceTags: Optional[list[str]] = None
    #: Refine search by warnings for More shared appearances than shared users.
    #: example: True
    moreSharedAppearancesEnabled: Optional[bool] = None
    #: Refine search by warnings for Fewer shared appearances than shared users.
    #: example: True
    fewSharedAppearancesEnabled: Optional[bool] = None
    #: Refine search by warnings for more monitor appearances than monitors.
    #: example: True
    moreMonitorAppearancesEnabled: Optional[bool] = None


class ProgrammableLineKeys(ApiModel):
    #: An index representing a Line Key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2.0
    lineKeyIndex: Optional[int] = None
    #: The action that would be performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    lineKeyType: Optional[LineKeyType] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL`.
    #: example: Help Line
    lineKeyLabel: Optional[str] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL` and the value must be a valid Telephone Number, Ext, or SIP URI (format: user@host using A-Z,a-z,0-9,-_ .+ for user and host).
    #: example: 5646
    lineKeyValue: Optional[datetime] = None


class PostLineKeyTemplateRequest(ApiModel):
    #: Name of the Line Key Template.
    #: example: template for 8845
    templateName: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: DMS Cisco 8845
    deviceModel: Optional[str] = None
    #: User Customization Enabled.
    #: example: True
    userReorderEnabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    lineKeys: Optional[list[ProgrammableLineKeys]] = None


class PutLineKeyTemplateRequest(ApiModel):
    #: Indicates whether the user can reorder the line keys.
    #: example: True
    userReorderEnabled: Optional[bool] = None
    #: List of line keys that are being updated.
    lineKeys: Optional[list[ProgrammableLineKeys]] = None


class LineKeyTemplatesResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL1VTL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS9kNDUzM2MwYi1hZGRmLTRjODUtODk0YS1hZTVkOTAyYzAyMDM=
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: template for 8845
    templateName: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: DMS Cisco 8845
    deviceModel: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 8845
    modelDisplayName: Optional[str] = None
