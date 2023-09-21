from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActivationCode', 'Device', 'DeviceCapabilities', 'DeviceCollectionResponse', 'DeviceConnectionStatus', 'DevicePermissions', 'ListDevicesProduct', 'ListDevicesType', 'ModifyDeviceTagsOp', 'NetworkConnectivityType']


class ActivationCode(ApiModel):
    #: The activation code.
    #: example: 5414011256173816
    code: Optional[str] = None
    #: The date and time the activation code expires.
    #: example: 2017-11-16T23:38:03.215Z
    expiry_time: Optional[datetime] = None


class DeviceConnectionStatus(str, Enum):
    connected = 'connected'
    disconnected = 'disconnected'
    connected_with_issues = 'connected_with_issues'
    offline_expired = 'offline_expired'
    activating = 'activating'
    unknown = 'unknown'


class NetworkConnectivityType(str, Enum):
    wired = 'wired'


class Device(ApiModel):
    #: A unique identifier for the device.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9ERVZJQ0UvNTEwMUIwN0ItNEY4Ri00RUY3LUI1NjUtREIxOUM3QjcyM0Y3
    id: Optional[str] = None
    #: A friendly name for the device.
    #: example: SFO12-3-PanHandle
    display_name: Optional[str] = None
    #: The placeId field has been deprecated. Please use workspaceId instead.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZWQtOGZjYS05ZGY0YjRmNDE3ZjU
    place_id: Optional[str] = None
    #: The workspace associated with the device.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZWQtOGZjYS05ZGY0YjRmNDE3ZjU
    workspace_id: Optional[str] = None
    #: The person associated with the device.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZWQtOGZjYS05ZGY0YjRmNDE3ZjU
    person_id: Optional[str] = None
    #: The organization associated with the device.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The capabilities of the device.
    #: example: ['xapi']
    capabilities: Optional[list[str]] = None
    #: The permissions the user has for this device. For example, `xapi` means this user is entitled to using the `xapi` against this device.
    #: example: ['xapi']
    permissions: Optional[list[str]] = None
    #: The connection status of the device.
    #: example: connected
    connection_status: Optional[DeviceConnectionStatus] = None
    #: The product name. A display friendly version of the device's `model`.
    #: example: Cisco Webex DX80
    product: Optional[str] = None
    #: The product type.
    #: example: roomdesk
    type: Optional[str] = None
    #: Tags assigned to the device.
    #: example: ['First Tag', 'Second Tag']
    tags: Optional[list[str]] = None
    #: The current IP address of the device.
    #: example: 100.110.120.130
    ip: Optional[str] = None
    #: The current network connectivty for the device.
    #: example: wired
    active_interface: Optional[NetworkConnectivityType] = None
    #: The unique address for the network adapter.
    #: example: 11:22:33:44:AA:FF
    mac: Optional[str] = None
    #: The primary SIP address to dial this device.
    #: example: sample_device@sample_workspacename.orgname.org
    primary_sip_url: Optional[str] = None
    #: All SIP addresses to dial this device.
    #: example: ['sample_device@sample_workspacename.orgname.org', 'another_device@sample_workspacename.orgname.org']
    sip_urls: Optional[list[str]] = None
    #: Serial number for the device.
    #: example: FOC1923NVVN
    serial: Optional[str] = None
    #: The operating system name data and version tag.
    #: example: RoomOS 2018-06-01 608dcdbb6e1
    software: Optional[str] = None
    #: The upgrade channel the device is assigned to.
    #: example: beta
    upgrade_channel: Optional[str] = None
    #: The date and time that the device was registered, in ISO8601 format.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None
    #: The workspace location associated with the device.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    workspace_location_id: Optional[str] = None
    #: Error codes coming from the device.
    #: example: ['sipprofileregistration']
    error_codes: Optional[list[str]] = None
    #: Timestamp of the first time device sent a status post.
    #: example: 2021-02-24T09:08:38.822Z
    first_seen: Optional[datetime] = None
    #: Timestamp of the last time device sent a status post.
    #: example: 2023-08-15T14:04:00.444Z
    last_seen: Optional[datetime] = None


class DeviceCollectionResponse(ApiModel):
    items: Optional[list[Device]] = None


class DevicePermissions(str, Enum):
    xapi_readonly = 'xapi:readonly'
    xapi_all = 'xapi:all'


class DeviceCapabilities(str, Enum):
    xapi = 'xapi'


class ListDevicesProduct(str, Enum):
    dx_80 = 'DX-80'
    room_kit = 'RoomKit'
    sx_80 = 'SX-80'


class ListDevicesType(str, Enum):
    roomdesk = 'roomdesk'
    phone = 'phone'
    accessory = 'accessory'
    webexgo = 'webexgo'
    unknown = 'unknown'


class ModifyDeviceTagsOp(str, Enum):
    #: Add all specified tags to the existing device tags list.
    add = 'add'
    #: Remove all tags that the device currently has.
    remove = 'remove'
    #: Replace the tags currently on the device with the specified list.
    replace = 'replace'
