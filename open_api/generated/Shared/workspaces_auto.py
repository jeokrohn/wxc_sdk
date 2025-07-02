from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CapabilityMap', 'Device', 'DeviceCapabilities', 'DeviceConnectionStatus', 'DevicePermissions', 'ManagedBy',
           'NetworkConnectivityType', 'SupportAndConfiguredInfo', 'Workspace', 'WorkspaceCalendar',
           'WorkspaceCalendarType', 'WorkspaceCalling', 'WorkspaceCallingHybridCalling', 'WorkspaceCallingType',
           'WorkspaceCallingWebexCalling', 'WorkspaceDeviceHostedMeetings', 'WorkspaceDevicePlatform',
           'WorkspaceHealth', 'WorkspaceHealthLevel', 'WorkspaceHotdeskingStatus', 'WorkspaceIndoorNavigation',
           'WorkspaceIssue', 'WorkspaceIssueLevel', 'WorkspaceIssueLevelMembers', 'WorkspaceSupportedDevices',
           'WorkspaceType', 'WorkspaceType1', 'WorkspacesApi']


class WorkspaceType(str, Enum):
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meeting_room = 'meetingRoom'
    #: Unstructured agile.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'


class WorkspaceIssueLevelMembers(str, Enum):
    error = 'error'
    warning = 'warning'
    info = 'info'


class WorkspaceIssueLevel(ApiModel):
    members: Optional[WorkspaceIssueLevelMembers] = Field(alias='Members', default=None)


class WorkspaceIssue(ApiModel):
    #: Issue id.
    id: Optional[str] = None
    #: Issue created timestamp.
    created_at: Optional[str] = None
    #: Issue title.
    title: Optional[str] = None
    #: Issue description.
    description: Optional[str] = None
    #: Recommended action to mitigate issue.
    recommended_action: Optional[str] = None
    #: Issue level.
    level: Optional[WorkspaceIssueLevel] = None


class WorkspaceType1(str, Enum):
    #: No workspace type set.
    not_set = 'notSet'
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meeting_room = 'meetingRoom'
    #: Unstructured agile.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'


class WorkspaceCallingType(str, Enum):
    #: Free Calling.
    free_calling = 'freeCalling'
    #: Hybrid Calling.
    hybrid_calling = 'hybridCalling'
    #: Webex Calling.
    webex_calling = 'webexCalling'
    #: Webex Edge For Devices.
    webex_edge_for_devices = 'webexEdgeForDevices'
    #: Third-party SIP URI.
    third_party_sip_calling = 'thirdPartySipCalling'
    #: No Calling.
    none_ = 'none'


class WorkspaceCallingHybridCalling(ApiModel):
    #: End user email address in Cisco Unified CM.
    email_address: Optional[str] = None


class WorkspaceCallingWebexCalling(ApiModel):
    #: The Webex Calling license associated with this workspace.
    licenses: Optional[list[str]] = None


class WorkspaceCalling(ApiModel):
    #: Calling.
    type: Optional[WorkspaceCallingType] = None
    #: The `hybridCalling` object only applies when calling type is `hybridCalling`.
    hybrid_calling: Optional[WorkspaceCallingHybridCalling] = None
    #: The `webexCalling` object only applies when calling type is `webexCalling`.
    webex_calling: Optional[WorkspaceCallingWebexCalling] = None


class WorkspaceCalendarType(str, Enum):
    #: No calendar.
    none_ = 'none'
    #: Google Calendar.
    google = 'google'
    #: Microsoft Exchange or Office 365.
    microsoft = 'microsoft'


class WorkspaceCalendar(ApiModel):
    #: * `none` - No calendar.
    type: Optional[WorkspaceCalendarType] = None
    #: Workspace email address. Will not be set when the calendar type is `none`.
    email_address: Optional[str] = None


class WorkspaceHotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'


class WorkspaceSupportedDevices(str, Enum):
    #: Workspace supports collaboration devices.
    collaboration_devices = 'collaborationDevices'
    #: Workspace supports MPP phones.
    phones = 'phones'


class WorkspaceDeviceHostedMeetings(ApiModel):
    #: `true` if enabled or `false` otherwise.
    enabled: Optional[bool] = None
    #: The Webex site for the device hosting meetings.
    site_url: Optional[str] = None


class WorkspaceDevicePlatform(str, Enum):
    #: Cisco.
    cisco = 'cisco'
    #: Microsoft Teams Room.
    microsoft_teams_room = 'microsoftTeamsRoom'


class WorkspaceIndoorNavigation(ApiModel):
    #: URL of a map locating the workspace.
    url: Optional[str] = None


class WorkspaceHealthLevel(str, Enum):
    error = 'error'
    warning = 'warning'
    info = 'info'
    ok = 'ok'


class WorkspaceHealth(ApiModel):
    #: Health level. The level is based on the list of issues associated with the workspace.
    level: Optional[WorkspaceHealthLevel] = None
    #: A list of workspace issues.
    issues: Optional[list[WorkspaceIssue]] = None


class DeviceCapabilities(str, Enum):
    xapi = 'xapi'


class DevicePermissions(str, Enum):
    xapi_readonly = 'xapi:readonly'
    xapi_all = 'xapi:all'


class DeviceConnectionStatus(str, Enum):
    connected = 'connected'
    disconnected = 'disconnected'
    connected_with_issues = 'connected_with_issues'
    offline_expired = 'offline_expired'
    activating = 'activating'
    unknown = 'unknown'
    offline_deep_sleep = 'offline_deep_sleep'


class NetworkConnectivityType(str, Enum):
    wired = 'wired'


class ManagedBy(str, Enum):
    cisco = 'CISCO'
    customer = 'CUSTOMER'
    partner = 'PARTNER'


class Device(ApiModel):
    #: A unique identifier for the device.
    id: Optional[str] = None
    #: A friendly name for the device.
    display_name: Optional[str] = None
    #: The `placeId` field has been deprecated. Please use `workspaceId` instead.
    place_id: Optional[str] = None
    #: The workspace associated with the device.
    workspace_id: Optional[str] = None
    #: The person associated with the device.
    person_id: Optional[str] = None
    #: The organization associated with the device.
    org_id: Optional[str] = None
    #: The capabilities of the device.
    capabilities: Optional[list[DeviceCapabilities]] = None
    #: The permissions the user has for this device. For example, `xapi` means this user is entitled to using the
    #: `xapi` against this device.
    permissions: Optional[list[DevicePermissions]] = None
    #: The connection status of the device.
    connection_status: Optional[DeviceConnectionStatus] = None
    #: The product name. A display friendly version of the device's `model`.
    product: Optional[str] = None
    #: The product type.
    type: Optional[str] = None
    #: Tags assigned to the device.
    tags: Optional[list[str]] = None
    #: The current IP address of the device.
    ip: Optional[str] = None
    #: The current network connectivity for the device.
    active_interface: Optional[NetworkConnectivityType] = None
    #: The unique address for the network adapter.
    mac: Optional[str] = None
    #: The primary SIP address to dial this device.
    primary_sip_url: Optional[str] = None
    #: All SIP addresses to dial this device.
    sip_urls: Optional[list[str]] = None
    #: Serial number for the device.
    serial: Optional[str] = None
    #: The operating system name data and version tag.
    software: Optional[str] = None
    #: The upgrade channel the device is assigned to.
    upgrade_channel: Optional[str] = None
    #: The date and time that the device was registered, in ISO8601 format.
    created: Optional[datetime] = None
    #: The location associated with the device.
    location_id: Optional[str] = None
    #: The workspace location associated with the device. Deprecated, prefer `locationId`.
    workspace_location_id: Optional[str] = None
    #: Error codes coming from the device.
    error_codes: Optional[list[str]] = None
    #: Timestamp of the first time device sent a status post.
    first_seen: Optional[datetime] = None
    #: Timestamp of the last time device sent a status post.
    last_seen: Optional[datetime] = None
    #: Entity managing the device configuration.
    managed_by: Optional[ManagedBy] = None
    #: The device platform.
    device_platform: Optional[WorkspaceDevicePlatform] = None


class Workspace(ApiModel):
    #: Unique identifier for the Workspace.
    id: Optional[str] = None
    #: `OrgId` associated with the workspace.
    org_id: Optional[str] = None
    #: Location associated with the workspace (ID to use for the `/locations API
    #: <https://developer.webex.com/docs/api/v1/locations>`_).
    location_id: Optional[str] = None
    #: Legacy workspace location ID associated with the workspace. Prefer `locationId`.
    workspace_location_id: Optional[str] = None
    #: Floor associated with the workspace.
    floor_id: Optional[str] = None
    #: A friendly name for the workspace.
    display_name: Optional[str] = None
    #: How many people the workspace is suitable for.
    capacity: Optional[int] = None
    #: The workspace type.
    type: Optional[WorkspaceType] = None
    #: `SipUrl` to call all the devices associated with the workspace.
    sip_address: Optional[str] = None
    #: The date and time that the workspace was registered, in ISO8601 format.
    created: Optional[datetime] = None
    #: Calling type.
    calling: Optional[WorkspaceCalling] = None
    #: Calendar type. Calendar of type `none` does not include an `emailAddress` field.
    calendar: Optional[WorkspaceCalendar] = None
    #: Notes associated to the workspace.
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    hotdesking_status: Optional[WorkspaceHotdeskingStatus] = None
    #: The supported devices for the workspace. Default is `collaborationDevices`.
    supported_devices: Optional[WorkspaceSupportedDevices] = None
    #: Device hosted meetings configuration.
    device_hosted_meetings: Optional[WorkspaceDeviceHostedMeetings] = None
    #: The device platform.
    device_platform: Optional[WorkspaceDevicePlatform] = None
    #: Indoor navigation configuration.
    indoor_navigation: Optional[WorkspaceIndoorNavigation] = None
    #: The health of the workspace.
    health: Optional[WorkspaceHealth] = None
    #: A list of devices associated with the workspace.
    devices: Optional[list[Device]] = None


class SupportAndConfiguredInfo(ApiModel):
    #: Is the workspace capability supported or not.
    supported: Optional[bool] = None
    #: Is the workspace capability configured or not.
    configured: Optional[bool] = None


class CapabilityMap(ApiModel):
    #: Occupancy detection.
    occupancy_detection: Optional[SupportAndConfiguredInfo] = None
    #: Presence detection.
    presence_detection: Optional[SupportAndConfiguredInfo] = None
    #: Ambient noise.
    ambient_noise: Optional[SupportAndConfiguredInfo] = None
    #: Sound level.
    sound_level: Optional[SupportAndConfiguredInfo] = None
    #: Temperature.
    temperature: Optional[SupportAndConfiguredInfo] = None
    #: Air quality.
    air_quality: Optional[SupportAndConfiguredInfo] = None
    #: Relative humidity.
    relative_humidity: Optional[SupportAndConfiguredInfo] = None


class WorkspacesApi(ApiChild, base='workspaces'):
    """
    Workspaces
    
    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. `Devices
    <https://developer.webex.com/docs/api/v1/devices>`_
    may be associated with workspaces.
    
    Viewing the list of workspaces in an organization requires an administrator auth token with the
    `spark-admin:workspaces_read` scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the scopes `spark-admin:workspaces_write` and `spark-admin:telephony_config_write`.
    
    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an `orgId` value must be supplied, as indicated in the reference documentation for
    the relevant endpoints.
    """

    def list_workspaces(self, location_id: str = None, workspace_location_id: str = None, floor_id: str = None,
                        display_name: str = None, capacity: float = None, type: WorkspaceType1 = None,
                        calling: WorkspaceCallingType = None, supported_devices: WorkspaceSupportedDevices = None,
                        calendar: WorkspaceCalendarType = None, device_hosted_meetings_enabled: bool = None,
                        device_platform: WorkspaceDevicePlatform = None, health_level: WorkspaceHealthLevel = None,
                        include_devices: bool = None, org_id: str = None,
                        **params) -> Generator[Workspace, None, None]:
        """
        List workspaces.

        Use query parameters to filter the response. The `orgId` parameter can only be used by admin users of another
        organization (such as partners). The `locationId`, `workspaceLocationId`, `indoorNavigation`, `floorId`,
        `capacity` and `type` fields will only be present for workspaces that have a value set for them. The special
        values `notSet` (for filtering on category) and `-1` (for filtering on capacity) can be used to filter for
        workspaces without a type and/or capacity.

        :param location_id: Location associated with the workspace. Values must originate from the /locations API and
            not the legacy /workspaceLocations API.
        :type location_id: str
        :param workspace_location_id: Location associated with the workspace. Both values from the /locations API and
            the legacy /workspaceLocations API are supported. This field is deprecated and integrations should prefer
            `locationId` going forward.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: float
        :param type: List workspaces by type.
        :type type: WorkspaceType1
        :param calling: List workspaces by calling type.
        :type calling: WorkspaceCallingType
        :param supported_devices: List workspaces by supported devices.
        :type supported_devices: WorkspaceSupportedDevices
        :param calendar: List workspaces by calendar type.
        :type calendar: WorkspaceCalendarType
        :param device_hosted_meetings_enabled: List workspaces enabled for device hosted meetings.
        :type device_hosted_meetings_enabled: bool
        :param device_platform: List workspaces by device platform.
        :type device_platform: WorkspaceDevicePlatform
        :param health_level: List workspaces by health level.
        :type health_level: WorkspaceHealthLevel
        :param include_devices: Flag identifying whether to include the devices associated with the workspace in the
            response.
        :type include_devices: bool
        :param org_id: List workspaces in this organization. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Workspace` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if workspace_location_id is not None:
            params['workspaceLocationId'] = workspace_location_id
        if floor_id is not None:
            params['floorId'] = floor_id
        if display_name is not None:
            params['displayName'] = display_name
        if capacity is not None:
            params['capacity'] = capacity
        if type is not None:
            params['type'] = enum_str(type)
        if calling is not None:
            params['calling'] = enum_str(calling)
        if supported_devices is not None:
            params['supportedDevices'] = enum_str(supported_devices)
        if calendar is not None:
            params['calendar'] = enum_str(calendar)
        if device_hosted_meetings_enabled is not None:
            params['deviceHostedMeetingsEnabled'] = str(device_hosted_meetings_enabled).lower()
        if device_platform is not None:
            params['devicePlatform'] = enum_str(device_platform)
        if health_level is not None:
            params['healthLevel'] = enum_str(health_level)
        if include_devices is not None:
            params['includeDevices'] = str(include_devices).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Workspace, item_key='items', params=params)

    def create_a_workspace(self, display_name: str, location_id: str = None, workspace_location_id: str = None,
                           floor_id: str = None, capacity: int = None, type: WorkspaceType1 = None,
                           sip_address: str = None, calling: WorkspaceCallingType = None,
                           calendar: WorkspaceCalendarType = None, notes: str = None,
                           hotdesking_status: WorkspaceHotdeskingStatus = None,
                           device_hosted_meetings: WorkspaceDeviceHostedMeetings = None,
                           supported_devices: WorkspaceSupportedDevices = None,
                           indoor_navigation: WorkspaceIndoorNavigation = None, org_id: str = None) -> Workspace:
        """
        Create a workspace.

        The `locationId`, `workspaceLocationId`, `floorId`, `indoorNavigation`, `capacity`, `type`, `notes` and
        `hotdeskingStatus` parameters are optional, and omitting them will result in the creation of a workspace
        without these values set, or set to their default. A `locationId` must be provided when the `floorId` is set.
        Calendar and calling can also be set for a new workspace. Omitting them will default to free calling and no
        calendaring. The `orgId` parameter can only be used by admin users of another organization (such as partners).

        * Information for Webex Calling fields may be found here: `locations
        <https://developer.webex.com/docs/api/v1/locations/list-locations>`_, `available numbers

        * The `locationId` and `supportedDevices` fields cannot be changed once configured.

        * When creating a `webexCalling` workspace that is not hot desk only, a `locationId` and either a `phoneNumber`
        or `extension` or both is required. Furthermore, it is possible to set the `licenses` field with a list of
        Webex Calling license IDs, if desired. If multiple license IDs are provided, the oldest suitable one will be
        applied. If no licenses are supplied, the oldest suitable one from the active subscriptions will be
        automaticaly applied.

        * When creating a hot desk only workspace, `phoneNumber` and `extension` fields are not applicable.
        Furthermore, `deviceHostedMeetingsEnabled`, and `calendar` services are not applicable. If any of these fields
        are provided the API will return an error. The `calling` type is `webexCalling`.

        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param location_id: Location associated with the workspace. Must be provided when the `floorId` is set.
        :type location_id: str
        :param workspace_location_id: Legacy workspace location ID associated with the workspace. Prefer `locationId`.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type: The type that best describes the workspace.
        :type type: WorkspaceType1
        :param sip_address: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`.
        :type sip_address: str
        :param calling: Calling.
        :type calling: WorkspaceCallingType
        :param calendar: Workspace calendar configuration requires a `type` (`microsoft`, `google`, or `none`), an
            `emailAddress`, and a `resourceGroupId`. The default is `none`.
        :type calendar: WorkspaceCalendarType
        :param notes: Notes associated to the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: WorkspaceHotdeskingStatus
        :param device_hosted_meetings: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag
            to `true`.
        :type device_hosted_meetings: WorkspaceDeviceHostedMeetings
        :param supported_devices: The supported devices for the workspace. Default is `collaborationDevices`.
        :type supported_devices: WorkspaceSupportedDevices
        :param indoor_navigation: Indoor navigation configuration.
        :type indoor_navigation: WorkspaceIndoorNavigation
        :param org_id: `OrgId` associated with the workspace. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :rtype: :class:`Workspace`
        """
        body = dict()
        body['displayName'] = display_name
        if org_id is not None:
            body['orgId'] = org_id
        if location_id is not None:
            body['locationId'] = location_id
        if workspace_location_id is not None:
            body['workspaceLocationId'] = workspace_location_id
        if floor_id is not None:
            body['floorId'] = floor_id
        if capacity is not None:
            body['capacity'] = capacity
        if type is not None:
            body['type'] = enum_str(type)
        if sip_address is not None:
            body['sipAddress'] = sip_address
        if calling is not None:
            body['calling'] = enum_str(calling)
        if calendar is not None:
            body['calendar'] = enum_str(calendar)
        if notes is not None:
            body['notes'] = notes
        if hotdesking_status is not None:
            body['hotdeskingStatus'] = enum_str(hotdesking_status)
        if device_hosted_meetings is not None:
            body['deviceHostedMeetings'] = device_hosted_meetings.model_dump(mode='json', by_alias=True, exclude_none=True)
        if supported_devices is not None:
            body['supportedDevices'] = enum_str(supported_devices)
        if indoor_navigation is not None:
            body['indoorNavigation'] = indoor_navigation.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        data = super().post(url, json=body)
        r = Workspace.model_validate(data)
        return r

    def delete_a_workspace(self, workspace_id: str):
        """
        Delete a Workspace

        Deletes a workspace by ID.

        Also deletes all devices associated with the workspace. Any deleted devices will need to be reactivated.
        Specify the workspace ID in the `workspaceId` parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :rtype: None
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url)

    def update_a_workspace(self, workspace_id: str, display_name: str = None, location_id: str = None,
                           workspace_location_id: str = None, floor_id: str = None, capacity: int = None,
                           type: WorkspaceType1 = None, calendar: WorkspaceCalendarType = None,
                           sip_address: str = None, calling: WorkspaceCallingType = None, notes: str = None,
                           hotdesking_status: WorkspaceHotdeskingStatus = None,
                           device_hosted_meetings: WorkspaceDeviceHostedMeetings = None,
                           indoor_navigation: WorkspaceIndoorNavigation = None) -> Workspace:
        """
        Update a Workspace

        Updates details for a workspace by ID.

        Specify the workspace ID in the `workspaceId` parameter in the URI. Include all details for the workspace that
        are present in a `GET request for the workspace details
        <https://developer.webex.com/docs/api/v1/workspaces/get-workspace-details>`_. Not including the optional `capacity`, `type` or
        `notes` fields will result in the fields no longer being defined for the workspace. A `locationId` must be
        provided when the `floorId` is set. The `locationId`, `workspaceLocationId`, `floorId`, `supportedDevices`,
        `calendar` and `calling` fields do not change when omitted from the update request.

        * Information for Webex Calling fields may be found here: `locations
        <https://developer.webex.com/docs/api/v1/locations/list-locations>`_ and `available numbers

        * Updating the `calling` parameter is only supported if the existing `calling` type is `freeCalling`, `none`,
        `thirdPartySipCalling` or `webexCalling`.

        * Updating the `calling` parameter to `none`, `thirdPartySipCalling` or `webexCalling` is not supported if the
        workspace contains any devices.

        * The `locationId` and `supportedDevices` fields cannot be changed once configured.

        * When updating `webexCalling` information on a workspace that is not hot desk only, a `locationId` and either
        a `phoneNumber` or `extension` or both is required. Furthermore, the `licenses` field can be set with a list
        of Webex Calling license IDs, if desired. If multiple license IDs are provided, the oldest suitable one will
        be applied. If a previously applied license ID is omitted, it will be replaced with one from the list
        provided. If the `licenses` field is omitted, the current calling license will be retained.

        * When specifying a hot desk only license on a hot desk only workspace, `deviceHostedMeetingsEnabled`, and
        `calendar` services are not supported and will be automatically disabled. In addition to this, the
        `phoneNumber` and `extension` will be removed from the workspace. Attempting to enable any of these services,
        or provide a `phoneNumber` or `extension` will result in an error. The `calling` type for these requests is
        `webexCalling`.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param location_id: Location associated with the workspace. Must be provided when the `floorId` is set.
        :type location_id: str
        :param workspace_location_id: Legacy workspace location ID associated with the workspace. Prefer `locationId`.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type: The type that best describes the workspace.
        :type type: WorkspaceType1
        :param calendar: An empty or null `calendar` field will not cause any changes. Provide a `type` (`microsoft`,
            `google`, or `none`), an `emailAddress`, and a `resourceGroupId`. To remove a calendar, set the `type` to
            `none`; this does not require an `emailAddress` or `resourceGroupId`.
        :type calendar: WorkspaceCalendarType
        :param sip_address: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`.
        :type sip_address: str
        :param calling: Calling types supported on update are `freeCalling`, `thirdPartySipCalling`, `webexCalling` and
            `none`.
        :type calling: WorkspaceCallingType
        :param notes: Notes associated to the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: WorkspaceHotdeskingStatus
        :param device_hosted_meetings: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag
            to `true`.
        :type device_hosted_meetings: WorkspaceDeviceHostedMeetings
        :param indoor_navigation: Indoor navigation configuration.
        :type indoor_navigation: WorkspaceIndoorNavigation
        :rtype: :class:`Workspace`
        """
        body = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if location_id is not None:
            body['locationId'] = location_id
        if workspace_location_id is not None:
            body['workspaceLocationId'] = workspace_location_id
        if floor_id is not None:
            body['floorId'] = floor_id
        if capacity is not None:
            body['capacity'] = capacity
        if type is not None:
            body['type'] = enum_str(type)
        if calendar is not None:
            body['calendar'] = enum_str(calendar)
        if sip_address is not None:
            body['sipAddress'] = sip_address
        if calling is not None:
            body['calling'] = enum_str(calling)
        if notes is not None:
            body['notes'] = notes
        if hotdesking_status is not None:
            body['hotdeskingStatus'] = enum_str(hotdesking_status)
        if device_hosted_meetings is not None:
            body['deviceHostedMeetings'] = device_hosted_meetings.model_dump(mode='json', by_alias=True, exclude_none=True)
        if indoor_navigation is not None:
            body['indoorNavigation'] = indoor_navigation.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}')
        data = super().put(url, json=body)
        r = Workspace.model_validate(data)
        return r

    def get_workspace_details(self, workspace_id: str, include_devices: bool = None) -> Workspace:
        """
        Get Workspace Details

        Shows details for a workspace, by ID.

        The `locationId`, `workspaceLocationId`, `floorId`, `indoorNavigation`, `capacity`, `type` and `notes` fields
        will only be present if they have been set for the workspace. Specify the workspace ID in the `workspaceId`
        parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param include_devices: Flag identifying whether to include the devices associated with the workspace in the
            response.
        :type include_devices: bool
        :rtype: :class:`Workspace`
        """
        params = {}
        if include_devices is not None:
            params['includeDevices'] = str(include_devices).lower()
        url = self.ep(f'{workspace_id}')
        data = super().get(url, params=params)
        r = Workspace.model_validate(data)
        return r

    def get_workspace_capabilities(self, workspace_id: str) -> CapabilityMap:
        """
        Get Workspace Capabilities

        Shows the capabilities for a workspace by ID.

        Returns a set of capabilities, including whether or not the capability is supported by any device in the
        workspace, and if the capability is configured (enabled). For example for a specific capability like
        `occupancyDetection`, the API will return if the capability is supported and/or configured such that occupancy
        detection data will flow from the workspace (device) to the cloud. Specify the workspace ID in the
        `workspaceId` parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :rtype: CapabilityMap
        """
        url = self.ep(f'{workspace_id}/capabilities')
        data = super().get(url)
        r = CapabilityMap.model_validate(data['capabilities'])
        return r
