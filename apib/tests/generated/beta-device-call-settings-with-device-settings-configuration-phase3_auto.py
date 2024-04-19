from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActivationStates', 'BetaDeviceCallSettingsWithDeviceSettingsConfigurationPhase3Api', 'Compression',
           'DeviceLayout', 'ErrorMessageObject', 'ErrorObject', 'GetThirdPartyDeviceObject', 'ItemObject',
           'JobExecutionStatusObject', 'KEMKeys', 'KemModuleType', 'LatestExecutionStatus', 'LayoutMode',
           'LineKeyType', 'ProgrammableLineKeys', 'RebuildPhonesJob', 'StepExecutionStatusesObject']


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
    #: Exit Code for a step.
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
    #: Exit Code for a job.
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


class LatestExecutionStatus(str, Enum):
    #: Indicates the job has started.
    starting = 'STARTING'
    #: Indicates the job is in progress.
    started = 'STARTED'
    #: Indicates the job has completed.
    completed = 'COMPLETED'
    #: Indicates the job has failed.
    failed = 'FAILED'


class RebuildPhonesJob(ApiModel):
    #: Name of the job which in this case, is `rebuildphones`.
    #: example: rebuildphones
    name: Optional[str] = None
    #: Unique identifier of the job.
    #: example: Y2lzY29zcGFyazovL3VzL0pPQl9JRC8wNjZkOTQzNC1kODEyLTQzODItODVhMC00MjBlOTFlODg3ZTY
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    #: example: ROUTERGW_1d458245-ee34-48c8-8ed6-92ea16ed48aa
    tracking_id: Optional[str] = None
    #: Unique identifier of the user who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MDRhZmQ1YS0zODRiLTQ0NjYtYTJlNC05Y2ExZjUwMDRlYWQ
    source_user_id: Optional[str] = None
    #: Unique identifier of the customer who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lYTRiZTEyNS00Y2ZjLTQ5OTItOGMwNi00Y2U4Mzc2ZDU4MmE
    source_customer_id: Optional[str] = None
    #: Unique identifier of the customer for which the job was run.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lYTRiZTEyNS00Y2ZjLTQ5OTItOGMwNi00Y2U4Mzc2ZDU4MmE
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    #: example: 428989
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Indicates the most recent status of the job at the time of invocation.
    #: example: STARTING
    latest_execution_status: Optional[LatestExecutionStatus] = None
    #: Indicates the target entity, i.e. LOCATION.
    #: example: LOCATION
    target: Optional[str] = None
    #: Unique identifier of a location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzQ0Y2UwNDBhLTEzNmMtNDc3NS1hMjIzLTY5OTczYmEyYWNhYw
    location_id: Optional[str] = None
    #: Indicates the progress of the job.
    #: example: 10
    percentage_complete: Optional[str] = None
    #: Count of number of devices rebuilt.
    #: example: 10
    device_count: Optional[int] = None


class ErrorMessageObject(ApiModel):
    #: Error message description.
    #: example: Unable to trigger rebuild phones process.
    description: Optional[str] = None
    #: Internal error code.
    #: example: 1014002
    code: Optional[str] = None
    #: Error messages describing the location ID for which the error occurs.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzQ0Y2UwNDBhLTEzNmMtNDc3NS1hMjIzLTY5OTczYmEyYWNhYw
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    #: example: 500
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Index of error number.
    #: example: 1
    item_number: Optional[int] = None
    #: Unique identifier to track the HTTP requests.
    #: example: ROUTERGW_96e745f7-0cd9-421f-a360-b892bfd5ee52
    tracking_id: Optional[str] = None
    #: The error object describes what the error is about.
    error: Optional[ErrorObject] = None


class LayoutMode(str, Enum):
    #: Default layout mode when a new device is added.
    default = 'DEFAULT'
    #: Enables a device to have its custom layout.
    custom = 'CUSTOM'


class LineKeyType(str, Enum):
    #: User's primary extension. This is the default assignment for Line Key Index 1 and cannot be modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables User and Call Park monitoring.
    monitor = 'MONITOR'
    #: Allows users to reach a telephone number, extension, or SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key.
    #: These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'


class ProgrammableLineKeys(ApiModel):
    #: The index starts from 1 representing the first key on the left side of the phone.
    #: example: 2
    line_key_index: Optional[int] = None
    #: Action performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`. Value must be a valid Telephone Number, Ext, or SIP URI
    #: (format: `user@host` limited to `A-Z,a-z,0-9,-_ .+` for user and host).
    #: example: 5646
    line_key_value: Optional[str] = None


class KemModuleType(str, Enum):
    #: Extension module has 14 line keys that can be configured.
    kem_14_keys = 'KEM_14_KEYS'
    #: Extension module has 18 line keys that can be configured.
    kem_18_keys = 'KEM_18_KEYS'
    #: Extension module has 20 line keys that can be configured.
    kem_20_keys = 'KEM_20_KEYS'


class KEMKeys(ApiModel):
    #: An index representing a KEM Module. The Index starts from 1 representing the first KEM Module.
    #: example: 1
    kem_module_index: Optional[int] = None
    #: An index representing a KEM Key. The Index starts from 1 representing the first key on the left side of the
    #: phone.
    #: example: 1
    kem_key_index: Optional[int] = None
    #: The action that would be performed when the KEM Key is pressed.
    #: example: SPEED_DIAL
    kem_key_type: Optional[LineKeyType] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`.
    #: example: Office
    kem_key_label: Optional[str] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`. Value must be a valid Telephone Number, Ext, or SIP URI
    #: (format: `user@host` limited to `A-Z,a-z,0-9,-_ .+` for user and host).
    #: example: 213457
    kem_key_value: Optional[str] = None


class DeviceLayout(ApiModel):
    #: Defines the layout mode of the device, i.e. DEFAULT or CUSTOM.
    #: example: CUSTOM
    layout_mode: Optional[LayoutMode] = None
    #: If `true`, user customization is enabled..
    #: example: True
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None
    #: Type of KEM module.
    #: example: KEM_14_KEYS
    kem_module_type: Optional[KemModuleType] = None
    #: Contains a mapping of KEM Keys and their corresponding actions.
    kem_keys: Optional[list[KEMKeys]] = None


class Compression(str, Enum):
    #: Minimize data use during compression.
    on = 'ON'
    #: Ignore data use during compression.
    off = 'OFF'


class ActivationStates(str, Enum):
    #: Indicates a device is activating using an activation code.
    activating = 'activating'
    #: Indicates a device has been activated using an activation code.
    activated = 'activated'
    #: Indicates a device has not been activated using an activation code.
    deactivated = 'deactivated'


class GetThirdPartyDeviceObject(ApiModel):
    #: Manufacturer of the device.
    #: example: THIRD_PARTY
    manufacturer: Optional[str] = None
    #: Identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    #: example: lg1_sias10_cpapi16004_LGU@64941297.int10.bcld.webex.com
    line_port: Optional[str] = None
    #: Outgoing server which the phone should use for all SIP requests. Not set if the response has no body.
    #: example: hs17.hosted-int.bcld.webex.com
    outbound_proxy: Optional[str] = None
    #: Device manager(s).
    #: example: CUSTOMER
    managed_by: Optional[str] = None
    #: SIP authentication user name for the owner of the device.
    #: example: 392829
    sip_user_name: Optional[str] = None
    #: A unique identifier for the device.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9ERVZJQ0UvNTEwMUIwN0ItNEY4Ri00RUY3LUI1NjUtREIxOUM3QjcyM0Y3
    id: Optional[str] = None
    #: The current IP address of the device.
    #: example: 100.110.120.130
    ip: Optional[str] = None
    #: The unique address for the network adapter.
    #: example: 11223344AAFF
    mac: Optional[str] = None
    #: A model type of the device.
    #: example: DMS Cisco 8811
    model: Optional[str] = None
    #: Activation state of the device. This field is only populated for a device added by a unique activation code
    #: generated by Control Hub for use with Webex.
    #: example: ACTIVATED
    activation_state: Optional[ActivationStates] = None
    #: Comma-separated array of tags used to describe the device.
    #: example: ['device description']
    descriptions: Optional[list[str]] = None
    #: Enabled / disabled status of the upgrade channel.
    #: example: True
    upgrade_channel_enabled: Optional[bool] = None


class BetaDeviceCallSettingsWithDeviceSettingsConfigurationPhase3Api(ApiChild, base='telephony/config'):
    """
    Beta Device Call Settings with Device Settings Configuration Phase 3
    
    """

    def rebuild_phones_configuration(self, location_id: str, org_id: str = None) -> RebuildPhonesJob:
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
        url = self.ep('jobs/devices/rebuildPhones')
        data = super().post(url, params=params, json=body)
        r = RebuildPhonesJob.model_validate(data)
        return r

    def list_rebuild_phones_jobs(self, org_id: str = None) -> list[RebuildPhonesJob]:
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
        url = self.ep('jobs/devices/rebuildPhones')
        data = super().get(url, params=params)
        r = TypeAdapter(list[RebuildPhonesJob]).validate_python(data['items'])
        return r

    def get_the_job_status_of_a_rebuild_phones_job(self, job_id: str, org_id: str = None) -> RebuildPhonesJob:
        """
        Get the Job Status of a Rebuild Phones Job

        Get the details of a rebuild phones job by its job ID.

        Rebuild phones jobs are used when there is a change in the network configuration of phones in a location, i.e.
        a change in the network configuration of devices in a location from public to private and vice-versa.

        This API requires requires a full administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Check a rebuild phones job status in this organization.
        :type org_id: str
        :rtype: :class:`RebuildPhonesJob`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/rebuildPhones/{job_id}')
        data = super().get(url, params=params)
        r = RebuildPhonesJob.model_validate(data)
        return r

    def get_job_errors_for_a_rebuild_phones_job(self, job_id: str, org_id: str = None) -> list[ItemObject]:
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
        url = self.ep(f'jobs/devices/rebuildPhones/{job_id}/errors')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ItemObject]).validate_python(data['items'])
        return r

    def get_webex_calling_device_details(self, device_id: str, org_id: str = None) -> GetThirdPartyDeviceObject:
        """
        Get Webex Calling Device Details

        Retrieves Webex Calling device details that include information needed for third-party device management.

        Webex calling devices are associated with a specific user Workspace or Virtual Line.

        Webex Calling devices share the location with the entity that owns them.

        This API requires a full, location, user, or read-only admin auth token with the scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization in which the device resides.
        :type org_id: str
        :rtype: :class:`GetThirdPartyDeviceObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}')
        data = super().get(url, params=params)
        r = GetThirdPartyDeviceObject.model_validate(data)
        return r

    def get_device_layout_by_device_id(self, device_id: str, org_id: str = None) -> DeviceLayout:
        """
        Get Device Layout by Device ID

        Get layout information of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Get device layout for this device ID.
        :type device_id: str
        :param org_id: Retrieve a device layout for the device in this organization.
        :type org_id: str
        :rtype: :class:`DeviceLayout`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/layout')
        data = super().get(url, params=params)
        r = DeviceLayout.model_validate(data)
        return r

    def modify_device_layout_by_device_id(self, device_id: str, layout_mode: LayoutMode,
                                          line_keys: list[ProgrammableLineKeys], user_reorder_enabled: bool = None,
                                          kem_module_type: KemModuleType = None, kem_keys: list[KEMKeys] = None,
                                          org_id: str = None):
        """
        Modify Device Layout by Device ID

        Modify the layout of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Modify device layout for this device ID.
        :type device_id: str
        :param layout_mode: Defines the layout mode of the device, i.e. DEFAULT or CUSTOM.
        :type layout_mode: LayoutMode
        :param line_keys: Contains a mapping of Line Keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: If `true`, user customization is enabled..
        :type user_reorder_enabled: bool
        :param kem_module_type: Type of KEM module.
        :type kem_module_type: KemModuleType
        :param kem_keys: Contains a mapping of KEM Keys and their corresponding actions.
        :type kem_keys: list[KEMKeys]
        :param org_id: Modify a device layout for the device in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['layoutMode'] = enum_str(layout_mode)
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        if kem_module_type is not None:
            body['kemModuleType'] = enum_str(kem_module_type)
        if kem_keys is not None:
            body['kemKeys'] = TypeAdapter(list[KEMKeys]).dump_python(kem_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/{device_id}/layout')
        super().put(url, params=params, json=body)

    def get_device_settings_for_a_person(self, person_id: str, org_id: str = None) -> Compression:
        """
        Get Device Settings for a Person

        Device settings list the compression settings for a person.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: ID of the person to retrieve device settings.
        :type person_id: str
        :param org_id: Retrieves the device settings for a person in this organization.
        :type org_id: str
        :rtype: Compression
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices/settings')
        data = super().get(url, params=params)
        r = Compression.model_validate(data['compression'])
        return r

    def update_device_settings_for_a_person(self, person_id: str, compression: Compression, org_id: str = None):
        """
        Update Device Settings for a Person

        Update device settings modifies the compression settings for a person.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: ID of the person to update device settings.
        :type person_id: str
        :param compression: Toggles compression ON and OFF.
        :type compression: Compression
        :param org_id: Modify device settings for a person in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['compression'] = enum_str(compression)
        url = self.ep(f'people/{person_id}/devices/settings')
        super().put(url, params=params, json=body)

    def get_device_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> Compression:
        """
        Get Device Settings for a Workspace

        Device settings list the compression settings for a workspace.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, user, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: ID of the workspace for which to retrieve device settings.
        :type workspace_id: str
        :param org_id: Retrieves the device settings for a workspace in this organization.
        :type org_id: str
        :rtype: Compression
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices/settings')
        data = super().get(url, params=params)
        r = Compression.model_validate(data['compression'])
        return r

    def update_device_settings_for_a_workspace(self, workspace_id: str, compression: Compression, org_id: str = None):
        """
        Update Device Settings for a Workspace

        Update device settings modifies the compression settings for a workspace.

        Device settings customize a device's behavior and performance. The compression field optimizes call quality for
        inbound and outbound calls.

        This API requires a full, location, or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: ID of the workspace for which to update device settings.
        :type workspace_id: str
        :param compression: Toggles compression ON and OFF.
        :type compression: Compression
        :param org_id: Modify the device settings for a workspace in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['compression'] = enum_str(compression)
        url = self.ep(f'workspaces/{workspace_id}/devices/settings')
        super().put(url, params=params, json=body)
