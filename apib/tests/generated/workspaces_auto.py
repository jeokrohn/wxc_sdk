from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CapabilityMap', 'CapabilityResponse', 'SupportAndConfiguredInfo', 'Workspace', 'WorkspaceCalendar', 'WorkspaceCalendarType', 'WorkspaceCalling', 'WorkspaceCallingHybridCalling', 'WorkspaceCallingType', 'WorkspaceCollectionResponse', 'WorkspaceCreationRequest', 'WorkspaceCreationRequestCalendar', 'WorkspaceCreationRequestCalling', 'WorkspaceCreationRequestCallingWebexCalling', 'WorkspaceCreationRequestHotdeskingStatus', 'WorkspaceDeviceHostedMeetings', 'WorkspaceHotdeskingStatus', 'WorkspaceSupportedDevices', 'WorkspaceType', 'WorkspaceType1', 'WorkspaceUpdateRequest', 'WorkspaceUpdateRequestType']


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
    none_ = 'none'


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
    #: example: workspace@example.com
    email_address: Optional[str] = None


class WorkspaceCalling(ApiModel):
    #: Calling.
    #: example: hybridCalling
    type: Optional[WorkspaceCallingType] = None
    #: The `hybridCalling` object only applies when calling type is `hybridCalling`.
    hybrid_calling: Optional[WorkspaceCallingHybridCalling] = None


class WorkspaceHotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'
    none_ = 'none'


class WorkspaceSupportedDevices(str, Enum):
    #: Workspace supports collaboration devices.
    collaboration_devices = 'collaborationDevices'
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
    email_address: Optional[str] = None


class WorkspaceDeviceHostedMeetings(ApiModel):
    #: `true` if enabled or `false` otherwise.
    #: example: True
    enabled: Optional[bool] = None
    #: The Webex site for the device hosting meetings.
    #: example: 'example.webex.com'
    site_url: Optional[str] = None


class Workspace(ApiModel):
    #: Unique identifier for the Workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFUy81MTAxQjA3Qi00RjhGLTRFRjctQjU2NS1EQjE5QzdCNzIzRjc
    id: Optional[str] = None
    #: `OrgId` associate with the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY
    org_id: Optional[str] = None
    #: Location associated with the workspace.
    #: example: YL34GrT...
    workspace_location_id: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floor_id: Optional[str] = None
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    display_name: Optional[str] = None
    #: How many people the workspace is suitable for.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The workspace type.
    type: Optional[WorkspaceType1] = None
    #: `SipUrl` to call all the devices associated with the workspace.
    #: example: test_workspace_1@trialorg.room.ciscospark.com
    sip_address: Optional[str] = None
    #: The date and time that the workspace was registered, in ISO8601 format.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None
    #: Calling type.
    calling: Optional[WorkspaceCalling] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    hotdesking_status: Optional[WorkspaceHotdeskingStatus] = None
    #: The supported devices for the workspace. Default is `collaborationDevices`.
    #: example: collaborationDevices
    supported_devices: Optional[WorkspaceSupportedDevices] = None
    #: Calendar type. Calendar of type `none` does not include an `emailAddress` field.
    calendar: Optional[WorkspaceCalendar] = None
    #: Device hosted meetings configuration.
    device_hosted_meetings: Optional[WorkspaceDeviceHostedMeetings] = None


class WorkspaceCreationRequestCallingWebexCalling(ApiModel):
    #: End user phone number.
    #: example: +12145654032
    phone_number: Optional[str] = None
    #: End user extension.
    #: example: 28278
    extension: Optional[str] = None
    #: Calling location ID.
    #: example: Y2lzY29g4...
    location_id: Optional[str] = None


class WorkspaceCreationRequestCalling(ApiModel):
    #: Calling.
    #: example: webexCalling
    type: Optional[str] = None
    #: The `webexCalling` object only applies when calling type is `webexCalling`.
    webex_calling: Optional[WorkspaceCreationRequestCallingWebexCalling] = None


class WorkspaceCreationRequestCalendar(ApiModel):
    #: example: microsoft
    type: Optional[str] = None
    #: Workspace email address. Will not be set when the calendar type is `none`.
    #: example: workspace@example.com
    email_address: Optional[str] = None


class WorkspaceCreationRequestHotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'


class WorkspaceCreationRequest(ApiModel):
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    display_name: Optional[str] = None
    #: `OrgId` associated with the workspace. Only admin users of another organization (such as partners) may use this parameter.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY
    org_id: Optional[str] = None
    #: Location associated with the workspace. Must be provided when the `floorId` is set.
    #: example: YL34GrT...
    workspace_location_id: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floor_id: Optional[str] = None
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The type that best describes the workspace.
    type: Optional[WorkspaceType1] = None
    #: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`
    sip_address: Optional[str] = None
    #: Calling types supported on create are `freeCalling`, `webexEdgeForDevices`, `thirdPartySipCalling`, `webexCalling` and `none`. Default is `freeCalling`.
    calling: Optional[WorkspaceCreationRequestCalling] = None
    #: Workspace calendar configuration. Provide a type (`microsoft`, `google` or `none`) and an `emailAddress`. Default is `none`.
    calendar: Optional[WorkspaceCreationRequestCalendar] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    #: example: on
    hotdesking_status: Optional[WorkspaceCreationRequestHotdeskingStatus] = None
    #: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag to `true`.
    device_hosted_meetings: Optional[WorkspaceDeviceHostedMeetings] = None
    #: The supported devices for the workspace. Default is `collaborationDevices`.
    #: example: collaborationDevices
    supported_devices: Optional[WorkspaceSupportedDevices] = None


class WorkspaceUpdateRequestType(str, Enum):
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


class WorkspaceUpdateRequest(ApiModel):
    #: A friendly name for the workspace.
    #: example: SFO-12 Capanina
    display_name: Optional[str] = None
    #: Location associated with the workspace. Must be provided when the `floorId` is set.
    #: example: YL34GrT...
    workspace_location_id: Optional[str] = None
    #: Floor associated with the workspace.
    #: example: Y2lzY29z...
    floor_id: Optional[str] = None
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    #: example: 5.0
    capacity: Optional[int] = None
    #: The type that best describes the workspace.
    #: example: focus
    type: Optional[WorkspaceUpdateRequestType] = None
    #: An empty/null calendar field will not cause any changes. Provide a type (`microsoft`, `google` or `none`) and an `emailAddress`. Removing calendar is done by setting the `none` type, and setting `none` type does not require an `emailAddress`.
    calendar: Optional[WorkspaceCreationRequestCalendar] = None
    #: The `sipAddress` field can only be provided when calling type is `thirdPartySipCalling`
    sip_address: Optional[str] = None
    #: Calling types supported on update are `freeCalling`, `thirdPartySipCalling`, `webexCalling` and `none`.
    calling: Optional[WorkspaceCreationRequestCalling] = None
    #: Notes associated to the workspace.
    #: example: this is a note
    notes: Optional[str] = None
    #: Hot desking status of the workspace.
    #: example: on
    hotdesking_status: Optional[WorkspaceCreationRequestHotdeskingStatus] = None
    #: To enable device hosted meetings, set a Webex `siteUrl` and the `enabled` flag to `true`.
    device_hosted_meetings: Optional[WorkspaceDeviceHostedMeetings] = None


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


class CapabilityResponse(ApiModel):
    #: The map of workspace capabilities.
    capabilities: Optional[CapabilityMap] = None
