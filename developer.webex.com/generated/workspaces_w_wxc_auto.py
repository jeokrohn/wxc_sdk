from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Calendar1', 'Calling1', 'CapabilityMap', 'GetWorkspaceCapabilitiesResponse', 'HotdeskingStatus',
           'ListWorkspacesResponse', 'SupportAndConfiguredInfo', 'SupportedDevices', 'Type', 'UpdateWorkspaceBody',
           'WebexCalling', 'Workspace', 'WorkspaceswithWXCIncludedApi']


class SupportedDevices(str, Enum):
    #: Workspace supports collaborationDevices.
    collaboration_devices = 'collaborationDevices'
    #: Workspace supports MPP phones.
    phones = 'phones'


class Type(str, Enum):
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


class Calendar1(ApiModel):
    type: Optional[str]
    #: Workspace email address. Will not be set when the calendar type is none.
    email_address: Optional[str]


class WebexCalling(ApiModel):
    #: End user phone number.
    phone_number: Optional[str]
    #: End user extension.
    extension: Optional[str]
    #: Calling location ID.
    location_id: Optional[str]


class Calling1(ApiModel):
    #: Calling.
    type: Optional[str]
    #: The webexCalling object only applies when calling type is webexCalling.
    webex_calling: Optional[WebexCalling]


class HotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'


class UpdateWorkspaceBody(ApiModel):
    #: A friendly name for the workspace.
    display_name: Optional[str]
    #: Location associated with the workspace. Must be provided when the floorId is set.
    workspace_location_id: Optional[str]
    #: Floor associated with the workspace.
    floor_id: Optional[str]
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    capacity: Optional[int]
    #: The type that best describes the workspace.
    type: Optional[Type]
    #: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or none) and an
    #: emailAddress. Removing calendar is done by setting the none type, and setting none type does not require an
    #: emailAddress.
    calendar: Optional[Calendar1]
    #: The sipAddress field can only be provided when calling type is thirdPartySipCalling
    sip_address: Optional[str]
    #: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
    calling: Optional[Calling1]
    #: Notes associated with the workspace.
    notes: Optional[str]
    #: Hot desking status of the workspace.
    hotdesking_status: Optional[HotdeskingStatus]


class Workspace(UpdateWorkspaceBody):
    #: Unique identifier for the Workspace.
    id: Optional[str]
    #: OrgId associate with the workspace.
    org_id: Optional[str]
    #: The date and time that the workspace was registered, in ISO8601 format.
    created: Optional[str]
    #: The supported devices for the workspace. Default is collaborationDevices.
    supported_devices: Optional[SupportedDevices]


class SupportAndConfiguredInfo(ApiModel):
    #: Is the workspace capability supported or not.
    supported: Optional[bool]
    #: Is the workspace capability configured or not.
    configured: Optional[bool]


class CapabilityMap(ApiModel):
    #: Occupancy detection.
    occupancy_detection: Optional[SupportAndConfiguredInfo]
    #: Presence detection.
    presence_detection: Optional[SupportAndConfiguredInfo]
    #: Ambient noise.
    ambient_noise: Optional[SupportAndConfiguredInfo]
    #: Sound level.
    sound_level: Optional[SupportAndConfiguredInfo]
    #: Temperature.
    temperature: Optional[SupportAndConfiguredInfo]
    #: Air quality.
    air_quality: Optional[SupportAndConfiguredInfo]
    #: Relative humidity.
    relative_humidity: Optional[SupportAndConfiguredInfo]


class ListWorkspacesResponse(ApiModel):
    #: An array of workspace objects.
    items: Optional[list[Workspace]]


class CreateWorkspaceBody(UpdateWorkspaceBody):
    #: OrgId associated with the workspace. Only admin users of another organization (such as partners) may use this
    #: parameter.
    org_id: Optional[str]
    #: The supported devices for the workspace. Default is collaborationDevices.
    supported_devices: Optional[SupportedDevices]


class GetWorkspaceCapabilitiesResponse(ApiModel):
    #: The map of workspace capabilities.
    capabilities: Optional[CapabilityMap]


class WorkspaceswithWXCIncludedApi(ApiChild, base='workspaces'):
    """
    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.
    Viewing the list of workspaces in an organization requires an administrator auth token with the
    spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the scopes spark-admin:workspaces_write and spark-admin:telephony_config_write.
    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for the
    relevant endpoints.
    """

    def list(self, org_id: str = None, workspace_location_id: str = None, floor_id: str = None, display_name: str = None, capacity: int = None, type_: str = None, calling: str = None, supported_devices: str = None, calendar: str = None, **params) -> Generator[Workspace, None, None]:
        """
        List workspaces.
        Use query parameters to filter the response. The orgId parameter can only be used by admin users of another
        organization (such as partners). The workspaceLocationId, floorId, capacity and type fields will only be
        present for workspaces that have a value set for them. The special values notSet (for filtering on category)
        and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or capacity.

        :param org_id: List workspaces in this organization. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :param workspace_location_id: Location associated with the workspace.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param type_: List workspaces by type. Possible values: notSet, focus, huddle, meetingRoom, open, desk, other
        :type type_: str
        :param calling: List workspaces by calling type. Possible values: freeCalling, hybridCalling, webexCalling,
            webexEdgeForDevices, thirdPartySipCalling, none
        :type calling: str
        :param supported_devices: List workspaces by supported devices. Possible values: collaborationDevices, phones
        :type supported_devices: str
        :param calendar: List workspaces by calendar type. Possible values: none, google, microsoft
        :type calendar: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/list-workspaces
        """
        if org_id is not None:
            params['orgId'] = org_id
        if workspace_location_id is not None:
            params['workspaceLocationId'] = workspace_location_id
        if floor_id is not None:
            params['floorId'] = floor_id
        if display_name is not None:
            params['displayName'] = display_name
        if capacity is not None:
            params['capacity'] = capacity
        if type_ is not None:
            params['type'] = type_
        if calling is not None:
            params['calling'] = calling
        if supported_devices is not None:
            params['supportedDevices'] = supported_devices
        if calendar is not None:
            params['calendar'] = calendar
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Workspace, params=params)

    def create(self, display_name: str = None, workspace_location_id: str = None, floor_id: str = None, capacity: int = None, type_: Type = None, calendar: Calendar1 = None, sip_address: str = None, calling: Calling1 = None, notes: str = None, hotdesking_status: HotdeskingStatus = None, org_id: str = None, supported_devices: SupportedDevices = None) -> Workspace:
        """
        Create a workspace.
        The workspaceLocationId, floorId, capacity, type, notes and hotdeskingStatus parameters are optional, and
        omitting them will result in the creation of a workspace without these values set, or set to their default. A
        workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set for a new
        workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can only be used
        by admin users of another organization (such as partners).

        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param workspace_location_id: Location associated with the workspace. Must be provided when the floorId is set.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type_: The type that best describes the workspace.
        :type type_: Type
        :param calendar: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or
            none) and an emailAddress. Removing calendar is done by setting the none type, and setting none type does
            not require an emailAddress.
        :type calendar: Calendar1
        :param sip_address: The sipAddress field can only be provided when calling type is thirdPartySipCalling
        :type sip_address: str
        :param calling: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
        :type calling: Calling1
        :param notes: Notes associated with the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: HotdeskingStatus
        :param org_id: OrgId associated with the workspace. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param supported_devices: The supported devices for the workspace. Default is collaborationDevices.
        :type supported_devices: SupportedDevices

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/create-a-workspace
        """
        body = CreateWorkspaceBody()
        if display_name is not None:
            body.display_name = display_name
        if workspace_location_id is not None:
            body.workspace_location_id = workspace_location_id
        if floor_id is not None:
            body.floor_id = floor_id
        if capacity is not None:
            body.capacity = capacity
        if type_ is not None:
            body.type_ = type_
        if calendar is not None:
            body.calendar = calendar
        if sip_address is not None:
            body.sip_address = sip_address
        if calling is not None:
            body.calling = calling
        if notes is not None:
            body.notes = notes
        if hotdesking_status is not None:
            body.hotdesking_status = hotdesking_status
        if org_id is not None:
            body.org_id = org_id
        if supported_devices is not None:
            body.supported_devices = supported_devices
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Workspace.parse_obj(data)

    def details(self, workspace_id: str) -> Workspace:
        """
        Shows details for a workspace, by ID.
        The workspaceLocationId, floorId, capacity, type and notes fields will only be present if they have been set
        for the workspace. Specify the workspace ID in the workspaceId parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/get-workspace-details
        """
        url = self.ep(f'{workspace_id}')
        data = super().get(url=url)
        return Workspace.parse_obj(data)

    def update(self, workspace_id: str, display_name: str = None, workspace_location_id: str = None, floor_id: str = None, capacity: int = None, type_: Type = None, calendar: Calendar1 = None, sip_address: str = None, calling: Calling1 = None, notes: str = None, hotdesking_status: HotdeskingStatus = None) -> Workspace:
        """
        Updates details for a workspace by ID.
        Specify the workspace ID in the workspaceId parameter in the URI. Include all details for the workspace that
        are present in a GET request for the workspace details. Not including the optional capacity, type or notes
        fields will result in the fields no longer being defined for the workspace. A workspaceLocationId must be
        provided when the floorId is set. The workspaceLocationId, floorId, supportedDevices, calendar and calling
        fields do not change when omitted from the update request.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param workspace_location_id: Location associated with the workspace. Must be provided when the floorId is set.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type_: The type that best describes the workspace.
        :type type_: Type
        :param calendar: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or
            none) and an emailAddress. Removing calendar is done by setting the none type, and setting none type does
            not require an emailAddress.
        :type calendar: Calendar1
        :param sip_address: The sipAddress field can only be provided when calling type is thirdPartySipCalling
        :type sip_address: str
        :param calling: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
        :type calling: Calling1
        :param notes: Notes associated with the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: HotdeskingStatus

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/update-a-workspace
        """
        body = UpdateWorkspaceBody()
        if display_name is not None:
            body.display_name = display_name
        if workspace_location_id is not None:
            body.workspace_location_id = workspace_location_id
        if floor_id is not None:
            body.floor_id = floor_id
        if capacity is not None:
            body.capacity = capacity
        if type_ is not None:
            body.type_ = type_
        if calendar is not None:
            body.calendar = calendar
        if sip_address is not None:
            body.sip_address = sip_address
        if calling is not None:
            body.calling = calling
        if notes is not None:
            body.notes = notes
        if hotdesking_status is not None:
            body.hotdesking_status = hotdesking_status
        url = self.ep(f'{workspace_id}')
        data = super().put(url=url, data=body.json())
        return Workspace.parse_obj(data)

    def delete(self, workspace_id: str):
        """
        Deletes a workspace by ID.
        Also deletes all devices associated with the workspace. Any deleted devices will need to be reactivated.
        Specify the workspace ID in the workspaceId parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/delete-a-workspace
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url=url)
        return

    def capabilities(self, workspace_id: str) -> CapabilityMap:
        """
        Shows the capabilities for a workspace by ID.
        Returns a set of capabilities, including whether or not the capability is supported by any device in the
        workspace, and if the capability is configured (enabled). For example for a specific capability like
        occupancyDetection, the API will return if the capability is supported and/or configured such that occupancy
        detection data will flow from the workspace (device) to the cloud. Specify the workspace ID in the workspaceId
        parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/get-workspace-capabilities
        """
        url = self.ep(f'{workspace_id}/capabilities')
        data = super().get(url=url)
        return CapabilityMap.parse_obj(data["capabilities"])
