from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CapabilityMap', 'CapabilityResponse', 'SupportAndConfiguredInfo', 'Workspace', 'WorkspaceCalendar', 'WorkspaceCalendarType', 'WorkspaceCalling', 'WorkspaceCallingHybridCalling', 'WorkspaceCallingType', 'WorkspaceCollectionResponse', 'WorkspaceCreationRequest', 'WorkspaceCreationRequestCalendar', 'WorkspaceCreationRequestCalling', 'WorkspaceCreationRequestCallingWebexCalling', 'WorkspaceCreationRequestHotdeskingStatus', 'WorkspaceDeviceHostedMeetings', 'WorkspaceHotdeskingStatus', 'WorkspaceSupportedDevices', 'WorkspaceType', 'WorkspaceUpdateRequest', 'WorkspaceUpdateRequestType']


class WorkspaceType(str, Enum):
    #: No workspace type set.
    notset = 'notSet'
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meetingroom = 'meetingRoom'
    #: Unstructured agile.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'
    none_ = 'none'


class WorkspaceCallingType(str, Enum):
    #: Free Calling.
    freecalling = 'freeCalling'
    #: Hybrid Calling.
    hybridcalling = 'hybridCalling'
    #: Webex Calling.
    webexcalling = 'webexCalling'
    #: Webex Edge For Devices.
    webexedgefordevices = 'webexEdgeForDevices'
    #: Third-party SIP URI.
    thirdpartysipcalling = 'thirdPartySipCalling'
    #: No Calling.
    none_ = 'none'


class WorkspaceCallingHybridCalling(ApiModel):
    #: End user email address in Cisco Unified CM.
    #: example: workspace@example.com
    emailAddress: Optional[str] = None


class WorkspaceCalling(ApiModel):
    #: Calling.
    #: example: hybridCalling
    type: Optional[WorkspaceCallingType] = None
    #: The `hybridCalling` object only applies when calling type is `hybridCalling`.
    hybridCalling: Optional[WorkspaceCallingHybridCalling] = None


class WorkspaceHotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'
    none_ = 'none'


class WorkspaceSupportedDevices(str, Enum):
    #: Workspace supports collaboration devices.
    collaborationdevices = 'collaborationDevices'
    #: Workspace supports MPP phones.
    phones = 'phones'


class WorkspaceCalendarType(str, Enum):
    #: No calendar.
    none_ = 'none'
    #: Google Calendar.
    google = 'google'
    #: Microsoft Exchange or Office 365.
    microsoft = 'microsoft'


class WorkspaceCalendar(ApiModel):
    #: example: microsoft
    type: Optional[WorkspaceCalendarType] = None
    #: Workspace email address. Will not be set when the calendar type is `none`.
    #: example: workspace@example.com
    emailAddress: Optional[str] = None


class WorkspaceDeviceHostedMeetings(ApiModel):
    #: `true` if enabled or `false` otherwise.
    #: example: True
    enabled: Optional[bool] = None
    #: The Webex site for the device hosting meetings.
    #: example: 'example.webex.com'
    siteUrl: Optional[str] = None


class Workspace(ApiModel):
    #: Unique identifier for the Workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFUy81MTAxQjA3Qi00RjhGLTRFRjctQjU2NS1EQjE5QzdCNzIzRjc
    id: Optional[str] = None
    #: `OrgId` associate with the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY
    orgId: Optional[str] = None
    #: Location associated with the workspace.
    #: example: YL34GrT...
    workspaceLocationId: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floorId: Optional[str] = None
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    displayName: Optional[str] = None
    #: How many people the workspace is suitable for.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The workspace type.
    type: Optional[WorkspaceType] = None
    #: `SipUrl` to call all the devices associated with the workspace.
    #: example: test_workspace_1@trialorg.room.ciscospark.com
    sipAddress: Optional[str] = None
    #: The date and time that the workspace was registered, in ISO8601 format.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None
    #: Calling type.
    calling: Optional[WorkspaceCalling] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    hotdeskingStatus: Optional[WorkspaceHotdeskingStatus] = None
    #: The supported devices for the workspace. Default is `collaborationDevices`.
    #: example: collaborationDevices
    supportedDevices: Optional[WorkspaceSupportedDevices] = None
    #: Calendar type. Calendar of type `none` does not include an `emailAddress` field.
    calendar: Optional[WorkspaceCalendar] = None
    #: Device hosted meetings configuration.
    deviceHostedMeetings: Optional[WorkspaceDeviceHostedMeetings] = None


class WorkspaceCreationRequestCallingWebexCalling(ApiModel):
    #: End user phone number.
    #: example: +12145654032
    phoneNumber: Optional[str] = None
    #: End user extension.
    #: example: 28278
    extension: Optional[str] = None
    #: Calling location ID.
    #: example: Y2lzY29g4...
    locationId: Optional[str] = None


class WorkspaceCreationRequestCalling(ApiModel):
    #: Calling.
    #: example: webexCalling
    type: Optional[str] = None
    #: The `webexCalling` object only applies when calling type is `webexCalling`.
    webexCalling: Optional[WorkspaceCreationRequestCallingWebexCalling] = None


class WorkspaceCreationRequestCalendar(ApiModel):
    #: example: microsoft
    type: Optional[str] = None
    #: Workspace email address. Will not be set when the calendar type is `none`.
    #: example: workspace@example.com
    emailAddress: Optional[str] = None


class WorkspaceCreationRequestHotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'


class WorkspaceCreationRequest(ApiModel):
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    displayName: Optional[str] = None
    #: `OrgId` associated with the workspace. Only admin users of another organization (such as partners) may use this parameter.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY
    orgId: Optional[str] = None
    #: Location associated with the workspace. Must be provided when the `floorId` is set.
    #: example: YL34GrT...
    workspaceLocationId: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floorId: Optional[str] = None
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The type that best describes the workspace.
    type: Optional[WorkspaceType] = None
    #: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`
    sipAddress: Optional[str] = None
    #: Calling types supported on create are `freeCalling`, `webexEdgeForDevices`, `thirdPartySipCalling`, `webexCalling` and `none`. Default is `freeCalling`.
    calling: Optional[WorkspaceCreationRequestCalling] = None
    #: Workspace calendar configuration. Provide a type (`microsoft`, `google` or `none`) and an `emailAddress`. Default is `none`.
    calendar: Optional[WorkspaceCreationRequestCalendar] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    #: example: on
    hotdeskingStatus: Optional[WorkspaceCreationRequestHotdeskingStatus] = None
    #: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag to `true`.
    deviceHostedMeetings: Optional[WorkspaceDeviceHostedMeetings] = None
    #: The supported devices for the workspace. Default is `collaborationDevices`.
    #: example: collaborationDevices
    supportedDevices: Optional[WorkspaceSupportedDevices] = None


class WorkspaceUpdateRequestType(str, Enum):
    #: No workspace type set.
    notset = 'notSet'
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meetingroom = 'meetingRoom'
    #: Unstructured agile.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'


class WorkspaceUpdateRequest(ApiModel):
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    displayName: Optional[str] = None
    #: Location associated with the workspace. Must be provided when the `floorId` is set.
    #: example: YL34GrT...
    workspaceLocationId: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floorId: Optional[str] = None
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The type that best describes the workspace.
    #: example: focus
    type: Optional[WorkspaceUpdateRequestType] = None
    #: An empty/null calendar field will not cause any changes. Provide a type (`microsoft`, `google` or `none`) and an `emailAddress`. Removing calendar is done by setting the `none` type, and setting `none` type does not require an `emailAddress`.
    calendar: Optional[WorkspaceCreationRequestCalendar] = None
    #: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`
    sipAddress: Optional[str] = None
    #: Calling types supported on update are `freeCalling`, `thirdPartySipCalling`, `webexCalling` and `none`.
    calling: Optional[WorkspaceCreationRequestCalling] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    #: example: on
    hotdeskingStatus: Optional[WorkspaceCreationRequestHotdeskingStatus] = None
    #: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag to `true`.
    deviceHostedMeetings: Optional[WorkspaceDeviceHostedMeetings] = None


class WorkspaceCollectionResponse(ApiModel):
    #: An array of workspace objects.
    items: Optional[list[Workspace]] = None


class SupportAndConfiguredInfo(ApiModel):
    #: Is the workspace capability supported or not.
    #: example: True
    supported: Optional[bool] = None
    #: Is the workspace capability configured or not.
    #: example: True
    configured: Optional[bool] = None


class CapabilityMap(ApiModel):
    #: Occupancy detection.
    occupancyDetection: Optional[SupportAndConfiguredInfo] = None
    #: Presence detection.
    presenceDetection: Optional[SupportAndConfiguredInfo] = None
    #: Ambient noise.
    ambientNoise: Optional[SupportAndConfiguredInfo] = None
    #: Sound level.
    soundLevel: Optional[SupportAndConfiguredInfo] = None
    #: Temperature.
    temperature: Optional[SupportAndConfiguredInfo] = None
    #: Air quality.
    airQuality: Optional[SupportAndConfiguredInfo] = None
    #: Relative humidity.
    relativeHumidity: Optional[SupportAndConfiguredInfo] = None


class CapabilityResponse(ApiModel):
    #: The map of workspace capabilities.
    capabilities: Optional[CapabilityMap] = None
