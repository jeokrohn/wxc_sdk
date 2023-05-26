from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateDeviceActivationCodeBody', 'CreateDeviceActivationCodeResponse', 'Device', 'DeviceConnectionStatus',
           'DeviceswithWXCDevicesDisplayedApi', 'ListDevicesResponse', 'NetworkConnectivtyType', 'Op']


class DeviceConnectionStatus(ApiModel):
    connected: Optional[str]
    disconnected: Optional[str]


class NetworkConnectivtyType(ApiModel):
    wired: Optional[str]


class Device(ApiModel):
    #: A unique identifier for the device.
    id: Optional[str]
    #: A friendly name for the device.
    display_name: Optional[str]
    #: The placeId field has been deprecated. Please use workspaceId instead.
    place_id: Optional[str]
    #: The workspace associated with the device.
    workspace_id: Optional[str]
    #: The person associated with the device.
    person_id: Optional[str]
    #: The organization associated with the device.
    org_id: Optional[str]
    #: The capabilities of the device.
    capabilities: Optional[list[xapi]]
    #: The permissions the user has for this device. For example, xapi means this user is entitled to using the xapi
    #: against this device.
    permissions: Optional[list[xapi]]
    #: The connection status of the device.
    connection_status: Optional[DeviceConnectionStatus]
    #: The product name. A display friendly version of the device's model.
    product: Optional[str]
    #: The product type.
    type: Optional[str]
    #: Tags assigned to the device.
    tags: Optional[list[str]]
    #: The current IP address of the device.
    ip: Optional[str]
    #: The current network connectivty for the device.
    active_interface: Optional[NetworkConnectivtyType]
    #: The unique address for the network adapter.
    mac: Optional[str]
    #: The primary SIP address to dial this device.
    primary_sip_url: Optional[str]
    #: All SIP addresses to dial this device.
    sip_urls: Optional[list[str]]
    #: Serial number for the device.
    serial: Optional[str]
    #: The operating system name data and version tag.
    software: Optional[str]
    #: The upgrade channel the device is assigned to.
    upgrade_channel: Optional[str]
    #: The date and time that the device was registered, in ISO8601 format.
    created: Optional[str]
    #: The date and time that the device was first seen, in ISO8601 format.
    first_seen: Optional[str]
    #: The date and time that the device was last seen, in ISO8601 format.
    last_seen: Optional[str]


class Op(str, Enum):
    #: Add a new tags list to the device.
    add = 'add'
    #: Remove all tags from the device.
    remove = 'remove'
    #: Replace the tags list on the device.
    replace = 'replace'


class CreateDeviceActivationCodeBody(ApiModel):
    #: The ID of the workspace where the device will be activated.
    workspace_id: Optional[str]
    #: The ID of the person who will own the device once activated.
    person_id: Optional[str]
    #: The model of the device being created.
    model: Optional[str]


class ListDevicesResponse(ApiModel):
    items: Optional[list[Device]]


class ModifyDeviceTagsBody(ApiModel):
    op: Optional[Op]
    #: Only the tags path is supported to patch.
    path: Optional[str]
    #: Possible values: First Tag, Second Tag
    value: Optional[list[str]]


class CreateDeviceActivationCodeResponse(ApiModel):
    #: The activation code.
    code: Optional[str]
    #: The date and time the activation code expires.
    expiry_time: Optional[str]


class CreateDeviceByMACAddressBody(CreateDeviceActivationCodeBody):
    #: The MAC address of the device being created.
    mac: Optional[str]
    #: SIP password to be configured for the phone, only required with third party devices.
    password: Optional[str]


class DeviceswithWXCDevicesDisplayedApi(ApiChild, base='devices'):
    """
    Devices represent cloud-registered Webex RoomOS devices or IP Phones. Devices may be associated with Workspaces or
    People.
    The following scopes are required for performing the specified actions:
    Searching and viewing details for devices requires an auth token with the spark:devices_read scope.
    Updating or deleting your devices requires an auth token with the spark:devices_write scope.
    Viewing the list of all devices in an organization requires an administrator auth token with the
    spark-admin:devices_read scope.
    Adding, updating, or deleting all devices in an organization requires an administrator auth token with the
    spark-admin:devices_write scope.
    Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
    """

    def list(self, person_id: str = None, workspace_id: str = None, org_id: str = None, display_name: str = None, product: str = None, type_: str = None, tag: str = None, connection_status: str = None, serial: str = None, software: str = None, upgrade_channel: str = None, error_code: str = None, capability: str = None, permission: str = None, **params) -> Generator[Device, None, None]:
        """
        Lists all active Webex RoomOS devices or IP Phones associated with the authenticated user, such as devices
        activated in personal mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name. Possible values: DX-80, RoomKit, SX-80
        :type product: str
        :param type_: List devices with this type. Possible values: roomdesk, phone, accessory, webexgo, unknown
        :type type_: str
        :param tag: List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma
            separating the tag values or adding several tag parameters.
        :type tag: str
        :param connection_status: List devices with this connection status.
        :type connection_status: str
        :param serial: List devices with this serial number.
        :type serial: str
        :param software: List devices with this software version.
        :type software: str
        :param upgrade_channel: List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code: List devices with this error code.
        :type error_code: str
        :param capability: List devices with this capability. Possible values: xapi
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/list-devices
        """
        if person_id is not None:
            params['personId'] = person_id
        if workspace_id is not None:
            params['workspaceId'] = workspace_id
        if org_id is not None:
            params['orgId'] = org_id
        if display_name is not None:
            params['displayName'] = display_name
        if product is not None:
            params['product'] = product
        if type_ is not None:
            params['type'] = type_
        if tag is not None:
            params['tag'] = tag
        if connection_status is not None:
            params['connectionStatus'] = connection_status
        if serial is not None:
            params['serial'] = serial
        if software is not None:
            params['software'] = software
        if upgrade_channel is not None:
            params['upgradeChannel'] = upgrade_channel
        if error_code is not None:
            params['errorCode'] = error_code
        if capability is not None:
            params['capability'] = capability
        if permission is not None:
            params['permission'] = permission
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, params=params)

    def details(self, device_id: str, org_id: str = None) -> Device:
        """
        Shows details for a device, by ID.
        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/get-device-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        data = super().get(url=url, params=params)
        return Device.parse_obj(data)

    def delete(self, device_id: str, org_id: str = None):
        """
        Deletes a device, by ID.
        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/delete-a-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        super().delete(url=url, params=params)
        return

    def modify_tags(self, device_id: str, org_id: str = None, op: Op = None, path: str = None, value: List[str] = None) -> Device:
        """
        Update requests use the JSON Patch syntax.
        The request must include a Content-Type header with the value application/json-patch+json.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :param op: 
        :type op: Op
        :param path: Only the tags path is supported to patch.
        :type path: str
        :param value: Possible values: First Tag, Second Tag
        :type value: List[str]

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/modify-device-tags
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyDeviceTagsBody()
        if op is not None:
            body.op = op
        if path is not None:
            body.path = path
        if value is not None:
            body.value = value
        url = self.ep(f'{device_id}')
        data = super().patch(url=url, params=params, data=body.json())
        return Device.parse_obj(data)

    def create_activation_code(self, org_id: str = None, workspace_id: str = None, person_id: str = None, model: str = None) -> CreateDeviceActivationCodeResponse:
        """
        Generate an activation code for a device in a specific workspace by workspaceId or for a person by personId.

        :param org_id: The organization associated with the activation code generated. If left empty, the organization
            associated with the caller will be used.
        :type org_id: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/create-a-device-activation-code
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateDeviceActivationCodeBody()
        if workspace_id is not None:
            body.workspace_id = workspace_id
        if person_id is not None:
            body.person_id = person_id
        if model is not None:
            body.model = model
        url = self.ep('activationCode')
        data = super().post(url=url, params=params, data=body.json())
        return CreateDeviceActivationCodeResponse.parse_obj(data)

    def create_by_mac_address(self, mac: str, org_id: str = None, workspace_id: str = None, person_id: str = None, model: str = None, password: str = None) -> Device:
        """
        Create a phone by its MAC address in a specific workspace or for a person.
        Specify the mac, model and either workspaceId or personId.

        :param mac: The MAC address of the device being created.
        :type mac: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param password: SIP password to be configured for the phone, only required with third party devices.
        :type password: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/create-a-device-by-mac-address
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateDeviceByMACAddressBody()
        if mac is not None:
            body.mac = mac
        if workspace_id is not None:
            body.workspace_id = workspace_id
        if person_id is not None:
            body.person_id = person_id
        if model is not None:
            body.model = model
        if password is not None:
            body.password = password
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Device.parse_obj(data)
