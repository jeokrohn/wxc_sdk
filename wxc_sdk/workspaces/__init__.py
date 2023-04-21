"""
Workspaces
Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices may
be associated with workspaces.

Viewing the list of workspaces in an organization requires an administrator auth token with
the spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
administrator auth token with the spark-admin:workspaces_write scope.

The Workspaces API can also be used by partner administrators acting as administrators of a different organization
than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for the
relevant endpoints.
"""
import datetime
import json
from collections.abc import Generator
from typing import Optional

from pydantic import Field, validator

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, enum_str
from ..base import SafeEnum as Enum

__all__ = ['WorkSpaceType', 'CallingType', 'CalendarType', 'WorkspaceEmail', 'Calendar',
           'Workspace', 'CapabilityMap', 'WorkspaceCalling', 'WorkspaceWebexCalling', 'WorkspaceSupportedDevices',
           'WorkspacesApi']


class WorkSpaceType(str, Enum):
    """
    workspace type
    """
    #: No workspace type set.
    notSet = 'notSet'
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meetingRoom = 'meetingRoom'
    #: Dedicated meeting space.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'


class CallingType(str, Enum):
    """
    Calling types: freeCalling, webexEdgeForDevices, thirdPartySipCalling, webexCalling and none.
    """
    #: Free Calling.
    free = 'freeCalling'
    #: Webex Edge For Devices.
    edge_for_devices = 'webexEdgeForDevices'
    #: thirdPartySipCalling
    third_party = 'thirdPartySipCalling'
    #: Webex Calling.
    webex = 'webexCalling'
    none = 'none'


class CalendarType(str, Enum):
    """
    type of calendar integration
    """
    #: No calendar.
    none = 'none'
    #: Google Calendar.
    google = 'google'
    #: Microsoft Exchange or Office 365.
    microsoft = 'microsoft'


class WorkspaceEmail(ApiModel):
    email_address: Optional[str]


class Calendar(WorkspaceEmail):
    #: Calendar type. Calendar of type none does not include an emailAddress field.
    calendar_type: Optional[CalendarType] = Field(alias='type')


class WorkspaceSupportedDevices(str, Enum):
    collaboration_devices = 'collaborationDevices'
    phones = 'phones'


class WorkspaceWebexCalling(ApiModel):
    #: End user phone number in Cisco Unified CM.
    phone_number: Optional[str]
    #: End user extension in Cisco Unified CM.
    extension: Optional[str]
    #: Calling location ID.
    location_id: Optional[str]


class WorkspaceCalling(ApiModel):
    type: Optional[CallingType]
    #: The webexCalling object only applies when calling type is webexCalling.
    #: due to a backend limitation this information is never returned by the workspace API and only has to be used when
    #: creating a workspace
    webex_calling: Optional[WorkspaceWebexCalling]


class Workspace(ApiModel):
    """
    Workspace details
    """
    #: Unique identifier for the Workspace.
    workspace_id: Optional[str] = Field(alias='id')
    #: OrgId associate with the workspace.
    org_id: Optional[str]
    #: Location associated with the workspace.
    workspace_location_id: Optional[str]
    #: Floor associated with the workspace.
    floor_id: Optional[str]
    #: A friendly name for the workspace.
    display_name: Optional[str]
    #: How many people the workspace is suitable for.
    capacity: Optional[int]
    #: The workspace type.
    workspace_type: Optional[WorkSpaceType] = Field(alias='type')
    #: SipUrl to call all the devices associated with the workspace.
    sip_address: Optional[str]
    #: The date and time that the workspace was registered
    created: Optional[datetime.datetime]
    #: Calling type.
    calling: Optional[WorkspaceCalling]
    #: The hybridCalling object only applies when calling type is hybridCalling.
    hybrid_calling: Optional[WorkspaceEmail]
    #: Calendar type. Calendar of type none does not include an emailAddress field.
    calendar: Optional[Calendar]
    #: Notes associated to the workspace.
    notes: Optional[str]
    #: Hot desking status of the workspace.
    hotdesking_status: Optional[bool]
    #: The supported devices for the workspace.
    supported_devices: Optional[WorkspaceSupportedDevices]

    @validator('hotdesking_status', pre=True)
    def validate_hotdesking_status(cls, value):
        """
        hotdesking_status actually is a string: 'on'/'off'

        :meta private:
        """
        if isinstance(value, bool):
            return value
        return value == 'on'

    def json(self, *args, exclude_none=True, by_alias=True, **kwargs) -> str:
        """
        restore calling type

        :meta private:
        """
        j_data = json.loads(super().json(*args, exclude_none=exclude_none, by_alias=by_alias, **kwargs))
        if self.hotdesking_status is not None:
            j_data['hotdeskingStatus'] = 'on' if self.hotdesking_status else 'off'
        return json.dumps(j_data)

    def update_or_create(self, for_update: bool = False) -> str:
        """
        JSON for update ot create

        :meta private:
        """
        # supported device cannot be changed later
        return self.json(exclude={'workspace_id': True,
                                  'sip_address': True,
                                  'created': True,
                                  'hybrid_calling': True,
                                  'supported_devices': for_update})

    @staticmethod
    def create(*, display_name: str) -> 'Workspace':
        """
        minimal settings for a :meth:`WorkspacesApi.create` call
        :return: :class:`Workspace`
        """
        return Workspace(display_name=display_name)


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


class WorkspacesApi(ApiChild, base='workspaces'):
    """
    Workspaces API

    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.
    Viewing the list of workspaces in an organization requires an administrator auth token with the
    spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the spark-admin:workspaces_write scope.
    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for the
    relevant endpoints.
    """

    def list(self, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None,
             supported_devices: WorkspaceSupportedDevices = None, calendar: CalendarType = None,
             org_id: str = None, **params) -> Generator[Workspace, None, None]:
        """
        List Workspaces

        List workspaces. Use query parameters to filter the response. The orgId parameter can only be used by admin
        users of another organization (such as partners). The workspaceLocationId, floorId, capacity and type fields
        will only be present for workspaces that have a value set for them. The special values notSet (for filtering
        on category) and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or
        capacity.

        :param workspace_location_id: Location associated with the workspace
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param workspace_type: List workspaces by type. Possible values: notSet, focus, huddle, meetingRoom, open,
            desk, other
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type. Possible values: freeCalling, hybridCalling, webexCalling,
            webexEdgeForDevices, thirdPartySipCalling, none
        :type calling: :class:`CallingType`
        :param supported_devices: List workspaces by supported devices. Possible values: collaborationDevices, phones
        :type supported_devices: str

        :param calendar: List workspaces by calendar type. Possible values: none, google, microsoft
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), enum_str(v))
                      for k, v in locals().items()
                      if k not in {'self', 'params', 'enum_str'} and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Workspace, params=params)

    def create(self, settings: Workspace, org_id: str = None):
        """
        Create a Workspace

        The workspaceLocationId, floorId, capacity, type, notes and hotdeskingStatus parameters are optional,
        and omitting them will result in the creation of a workspace without these values set, or set to their
        default. A workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set
        for a new workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can
        only be used by admin users of another organization (such as partners).

        Information for Webex Calling fields may be found here: locations and available numbers.

        The locationId and supportedDevices fields cannot be changed once configured.

        When creating a webexCalling workspace, a locationId and either a phoneNumber or extension or both is required.

        :param settings: settings for new Workspace
        :type settings: :class:`Workspace`
        :param org_id: OrgId associated with the workspace. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: new workspace
        :rtype: :class:`Workspace`
        """
        if org_id:
            settings.org_id = org_id
        data = settings.update_or_create()
        url = self.ep()
        data = self.post(url, data=data)
        return Workspace.parse_obj(data)

    def details(self, workspace_id) -> Workspace:
        """
        Get Workspace Details

        Shows details for a workspace, by ID. The workspaceLocationId, floorId, capacity, type and notes fields will
        only be present if they have been set for the workspace.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :return: workspace details
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        return Workspace.parse_obj(self.get(url))

    def update(self, workspace_id, settings: Workspace) -> Workspace:
        """
        Updates details for a workspace by ID.

        Specify the workspace ID in the workspaceId parameter in the URI. Include all details for the workspace that
        are present in a GET request for the workspace details. Not including the optional capacity, type or notes
        fields will result in the fields no longer being defined for the workspace. A workspaceLocationId must be
        provided when the floorId is set. The workspaceLocationId, floorId, supportedDevices, calendar and calling
        fields do not change when omitted from the update request.

        Information for Webex Calling fields may be found here: locations and available numbers.

        Updating the calling parameter is only supported if the existing calling type is freeCalling, none,
        thirdPartySipCalling or webexCalling.

        Updating the calling parameter to none, thirdPartySipCalling or webexCalling is not supported if the
        workspace contains any devices.

        The locationId and supportedDevices fields cannot be changed once configured.

        When updating webexCalling information, a locationId and either a phoneNumber or extension or both is required.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param settings: new workspace settings
        :type settings: :class:`Workspace`
        :return: updated workspace
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        j_data = settings.update_or_create(for_update=True)
        data = self.put(url, data=j_data)
        return Workspace.parse_obj(data)

    def delete_workspace(self, workspace_id):
        """
        Delete a Workspace

        Deletes a workspace, by ID. Will also delete all devices associated with the workspace. Any deleted devices
        will need to be reactivated.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        """
        url = self.ep(workspace_id)
        self.delete(url)

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

        """
        url = self.ep(f'{workspace_id}/capabilities')
        data = super().get(url=url)
        return CapabilityMap.parse_obj(data["capabilities"])
