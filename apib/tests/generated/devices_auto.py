from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActivationCode', 'Device', 'DeviceCapabilities', 'DeviceConnectionStatus', 'DevicePlatform', 'DevicesApi',
           'ListDevicesProduct', 'ListDevicesType', 'ManagedBy', 'ModifyDeviceTagsOp', 'NetworkConnectivityType']


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


class ManagedBy(str, Enum):
    cisco = 'CISCO'
    customer = 'CUSTOMER'
    partner = 'PARTNER'


class DevicePlatform(str, Enum):
    cisco = 'cisco'
    microsoft_teams_room = 'microsoftTeamsRoom'


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
    #: The permissions the user has for this device. For example, `xapi` means this user is entitled to using the
    #: `xapi` against this device.
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
    #: The location associated with the device.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    location_id: Optional[str] = None
    #: The workspace location associated with the device. Deprecated, prefer `locationId`.
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
    #: Entity managing the device configuration.
    #: example: CISCO
    managed_by: Optional[ManagedBy] = None
    #: The device platform.
    #: example: cisco
    device_platform: Optional[DevicePlatform] = None


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


class DevicesApi(ApiChild, base='devices'):
    """
    Devices
    
    Devices represent cloud-registered Webex RoomOS devices and Webex Calling phones. Devices may be associated with
    `Workspaces
    <https://developer.webex.com/docs/api/v1/workspaces>`_.
    
    The following scopes are required for performing the specified actions:
    
    * Searching and viewing details for devices requires an auth token with the `spark:devices_read` scope.
    
    * Updating or deleting your devices requires an auth token with the `spark:devices_write` scope.
    
    * Viewing the list of all devices in an organization requires an administrator auth token with the
    `spark-admin:devices_read` scope.
    
    * Adding, updating, or deleting all devices in an organization requires an administrator auth token with the
    `spark-admin:devices_write` scope.
    
    * Generating an activation code requires an auth token with the `spark-admin:devices_write` scope, and one of the
    `identity:placeonetimepassword_create` or `identity:one_time_password` scopes.
    
    These APIs cannot be used with Cisco 98xx devices that are not yet Webex
    Aware. Use Webex Control Hub to manage these devices.
    
    """

    def list_devices(self, display_name: str = None, person_id: str = None, workspace_id: str = None,
                     connection_status: str = None, product: ListDevicesProduct = None, type: ListDevicesType = None,
                     serial: str = None, tag: str = None, software: str = None, upgrade_channel: str = None,
                     error_code: str = None, capability: DeviceCapabilities = None, permission: str = None,
                     location_id: str = None, workspace_location_id: str = None, mac: str = None,
                     device_platform: DevicePlatform = None, org_id: str = None,
                     **params) -> Generator[Device, None, None]:
        """
        List Devices

        Lists all active Webex devices associated with the authenticated user, such as devices activated in personal
        mode. This requires the `spark:devices_read` scope. Administrators can list all devices within their
        organization. This requires an administrator auth token with the `spark-admin:devices_read` scope.

        :param display_name:
        List devices with this display name.
        :type display_name: str
        :param person_id:
        List devices by person ID.
        :type person_id: str
        :param workspace_id:
        List devices by workspace ID.
        :type workspace_id: str
        :param connection_status:
        List devices with this connection status.
        :type connection_status: str
        :param product:
        List devices with this product name.
        :type product: ListDevicesProduct
        :param type:
        List devices with this type.
        :type type: ListDevicesType
        :param serial:
        List devices with this serial number.
        :type serial: str
        :param tag:
        List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma separating the
        `tag` values or adding several `tag` parameters.
        :type tag: str
        :param software:
        List devices with this software version.
        :type software: str
        :param upgrade_channel:
        List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code:
        List devices with this error code.
        :type error_code: str
        :param capability:
        List devices with this capability.
        :type capability: DeviceCapabilities
        :param permission:
        List devices with this permission.
        :type permission: str
        :param location_id:
        List devices by location ID.
        :type location_id: str
        :param workspace_location_id:
        List devices by workspace location ID. Deprecated, prefer `locationId`.
        :type workspace_location_id: str
        :param mac:
        List devices with this MAC address.
        :type mac: str
        :param device_platform:
        List devices with this device platform.
        :type device_platform: DevicePlatform
        :param org_id:
        List devices in this organization. Only admin users of another organization (such as partners) may use this
        parameter.
        :type org_id: str
        :return: Generator yielding :class:`Device` instances
        """
        if display_name is not None:
            params['displayName'] = display_name
        if person_id is not None:
            params['personId'] = person_id
        if workspace_id is not None:
            params['workspaceId'] = workspace_id
        if org_id is not None:
            params['orgId'] = org_id
        if connection_status is not None:
            params['connectionStatus'] = connection_status
        if product is not None:
            params['product'] = enum_str(product)
        if type is not None:
            params['type'] = enum_str(type)
        if serial is not None:
            params['serial'] = serial
        if tag is not None:
            params['tag'] = tag
        if software is not None:
            params['software'] = software
        if upgrade_channel is not None:
            params['upgradeChannel'] = upgrade_channel
        if error_code is not None:
            params['errorCode'] = error_code
        if capability is not None:
            params['capability'] = enum_str(capability)
        if permission is not None:
            params['permission'] = permission
        if location_id is not None:
            params['locationId'] = location_id
        if workspace_location_id is not None:
            params['workspaceLocationId'] = workspace_location_id
        if mac is not None:
            params['mac'] = mac
        if device_platform is not None:
            params['devicePlatform'] = enum_str(device_platform)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, item_key='items', params=params)

    def get_device_details(self, device_id: str, org_id: str = None) -> Device:
        """
        Get Device Details

        Shows details for a device, by ID. This requires an auth token with the `spark:devices_read` scope to see your
        own device, or `spark-admin:devices_read` to see any other device in your organization.

        Specify the device ID in the `deviceId` parameter in the URI.

        :param device_id:
        A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :rtype: :class:`Device`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        data = super().get(url, params=params)
        r = Device.model_validate(data)
        return r

    def delete_a_device(self, device_id: str, org_id: str = None):
        """
        Delete a Device

        Deletes a device, by ID. Deleting your own device requires an auth token with the `spark:devices_write` scope.
        Deleting any other device in the organization will require an administrator auth token with the
        `spark-admin:devices_write` scope.

        Specify the device ID in the `deviceId` parameter in the URI.

        <div><Callout type="warning">Deleting a device from a person with a Webex Calling Standard license will enable
        Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        super().delete(url, params=params)

    def modify_device_tags(self, device_id: str, op: ModifyDeviceTagsOp = None, path: str = None,
                           value: list[str] = None, org_id: str = None) -> Device:
        """
        Modify Device Tags

        Create, delete or update tags on a device. For your own device, this requires an auth token with the
        `spark:devices_write` scope. An auth token with the `spark-admin:devices_write` scope is required to operate
        on other devices within the organization.

        Specify the device ID in the `deviceId` parameter in the URI.

        Include only the tag array in the request body, no other device attributes can be changed. This action will
        overwrite any previous tags. A common approach is to first `GET the devices's details
        <https://developer.webex.com/docs/api/v1/devices/get-device-details>`_, make changes to the
        `tags` array, and then PATCH the new complete array with this endpoint.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :type op: ModifyDeviceTagsOp
        :param path: Only the tags path is supported to patch.
        :type path: str
        :type value: list[str]
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :rtype: :class:`Device`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if op is not None:
            body['op'] = enum_str(op)
        if path is not None:
            body['path'] = path
        if value is not None:
            body['value'] = value
        url = self.ep(f'{device_id}')
        data = super().patch(url, params=params, json=body)
        r = Device.model_validate(data)
        return r

    def create_a_device_activation_code(self, workspace_id: str = None, person_id: str = None, model: str = None,
                                        org_id: str = None) -> ActivationCode:
        """
        Create a Device Activation Code

        Generate an activation code for a device in a specific workspace by `workspaceId` or for a person by
        `personId`. This requires an auth token with the `spark-admin:devices_write` scope, and either
        `identity:placeonetimepassword_create` (allows creating activation codes for workspaces only) or
        `identity:one_time_password` (allows creating activation codes for workspaces or persons).

        * Adding a device to a workspace with calling type `none` or `thirdPartySipCalling` will reset the workspace
        calling type to `freeCalling`.

        * Either `workspaceId` or `personId` should be provided. If both are supplied, the request will be invalid.

        * If no `model` is supplied, the `code` returned will only be accepted on RoomOS devices.

        * If your device is a phone, you must provide the `model` as a field. You can get the `model` from the
        `supported devices
        <https://developer.webex.com/docs/api/v1/device-call-settings/read-the-list-of-supported-devices>`_ API.

        <div><Callout type="warning">Adding a device to a person with a Webex Calling Standard license will disable
        Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created. The corresponding device model display name sometimes
            called the product name, can also be used to specify the model.
        :type model: str
        :param org_id: The organization associated with the activation code generated. If left empty, the organization
            associated with the caller will be used.
        :type org_id: str
        :rtype: :class:`ActivationCode`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if model is not None:
            body['model'] = model
        url = self.ep('activationCode')
        data = super().post(url, params=params, json=body)
        r = ActivationCode.model_validate(data)
        return r

    def create_a_device_by_mac_address(self, mac: str, model: str, workspace_id: str = None, person_id: str = None,
                                       password: str = None, org_id: str = None) -> Device:
        """
        Create a Device by MAC Address

        Create a phone by its MAC address in a specific workspace or for a person.

        Specify the `mac`, `model` and either `workspaceId` or `personId`.

        * You can get the `model` from the `supported devices
        <https://developer.webex.com/docs/api/v1/device-call-settings/read-the-list-of-supported-devices>`_ API.

        * Either `workspaceId` or `personId` should be provided. If both are supplied, the request will be invalid.

        * The `password` field is only required for third party devices. You can obtain the required third party phone
        configuration from `here
        <https://developer.webex.com/docs/api/v1/beta-device-call-settings-with-third-party-device-support/get-third-party-device>`_.

        <div><Callout type="warning">Adding a device to a person with a Webex Calling Standard license will disable
        Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

        :param mac: The MAC address of the device being created.
        :type mac: str
        :param model: The model of the device being created. The corresponding device model display name sometimes
            called the product name, can also be used to specify the model.
        :type model: str
        :param workspace_id: The ID of the workspace where the device will be created.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once created.
        :type person_id: str
        :param password: SIP password to be configured for the phone, only required with third party devices.
        :type password: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :rtype: :class:`Device`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['mac'] = mac
        body['model'] = model
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if password is not None:
            body['password'] = password
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = Device.model_validate(data)
        return r
