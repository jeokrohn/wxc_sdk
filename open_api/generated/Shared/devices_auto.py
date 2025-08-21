from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActivationCode', 'Device', 'DeviceCapabilities', 'DeviceConnectionStatus', 'DevicePermissions',
           'DevicePlatform', 'DevicesApi', 'MaintenanceMode', 'ManagedBy', 'NetworkConnectivityType', 'Op', 'Product',
           'Type']


class ActivationCode(ApiModel):
    #: The activation code.
    code: Optional[str] = None
    #: The date and time the activation code expires.
    expiry_time: Optional[datetime] = None


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


class DevicePlatform(str, Enum):
    cisco = 'cisco'
    microsoft_teams_room = 'microsoftTeamsRoom'


class MaintenanceMode(str, Enum):
    off = 'off'
    on = 'on'
    upcoming = 'upcoming'


class Device(ApiModel):
    #: A unique identifier for the device.
    id: Optional[str] = None
    #: A unique identifier for the device specifically for use with Webex Calling APIs.
    calling_device_id: Optional[str] = None
    #: A unique identifier for the device specifically for use with Webex Devices APIs.
    webex_device_id: Optional[str] = None
    #: A friendly name for the device.
    display_name: Optional[str] = None
    #: The placeId field has been deprecated. Please use workspaceId instead.
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
    device_platform: Optional[DevicePlatform] = None
    planned_maintenance: Optional[MaintenanceMode] = None


class Product(str, Enum):
    dx_80 = 'DX-80'
    room_kit = 'RoomKit'
    sx_80 = 'SX-80'


class Type(str, Enum):
    roomdesk = 'roomdesk'
    phone = 'phone'
    accessory = 'accessory'
    webexgo = 'webexgo'
    unknown = 'unknown'


class Op(str, Enum):
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
                     connection_status: str = None, product: Product = None, type: Type = None, serial: str = None,
                     tag: str = None, software: str = None, upgrade_channel: str = None, error_code: str = None,
                     capability: DeviceCapabilities = None, permission: str = None, location_id: str = None,
                     workspace_location_id: str = None, mac: str = None, device_platform: DevicePlatform = None,
                     planned_maintenance: MaintenanceMode = None, org_id: str = None,
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
        :type product: Product
        :param type:
        List devices with this type.
        :type type: Type
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
        :param planned_maintenance:
        List devices with this planned maintenance.
        :type planned_maintenance: MaintenanceMode
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
        if planned_maintenance is not None:
            params['plannedMaintenance'] = enum_str(planned_maintenance)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, item_key='items', params=params)

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

    def modify_device_tags(self, device_id: str, op: Op = None, path: str = None, value: list[str] = None,
                           org_id: str = None) -> Device:
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
        :param op: * `add` - Add all specified tags to the existing device tags list.
        :type op: Op
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
