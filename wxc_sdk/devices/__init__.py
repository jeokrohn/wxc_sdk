"""
Devices represent cloud-registered Webex RoomOS devices and Webex Calling phones.
"""
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, List

from pydantic import Field, model_validator, field_validator

from ..api_child import ApiChild
from ..base import SafeEnum as Enum, enum_str
from ..base import to_camel, ApiModel
from ..common import DevicePlatform
from ..rest import RestSession
from ..telephony import DeviceManagedBy
from ..telephony.jobs import DeviceSettingsJobsApi

__all__ = ['DevicesApi', 'Device', 'TagOp', 'ActivationCodeResponse', 'ProductType', 'ConnectionStatus', 'Lifecycle']


class ProductType(str, Enum):
    phone = 'phone'
    roomdesk = 'roomdesk'


class ConnectionStatus(str, Enum):
    connected = 'connected'
    disconnected = 'disconnected'
    connected_with_issues = 'connected_with_issues'
    offline_expired = 'offline_expired'
    activating = 'activating'
    unknown = 'unknown'
    offline_deep_sleep = 'offline_deep_sleep'


class Lifecycle(str, Enum):
    unknown = 'UNKNOWN'
    active = 'ACTIVE'
    end_of_sale = 'END_OF_SALE'
    end_of_maintenance = 'END_OF_MAINTENANCE'
    end_of_service = 'END_OF_SERVICE'
    upcoming_end_of_support = 'UPCOMING_END_OF_SUPPORT'
    end_of_support = 'END_OF_SUPPORT'


class Device(ApiModel):
    #: A unique identifier for the device.
    device_id: str = Field(alias='id')
    calling_device_id: Optional[str]
    webex_device_id: Optional[str]
    #: A friendly name for the device
    display_name: str
    #: The workspace associated with the device.
    workspace_id: Optional[str] = None
    #: The person associated with the device.
    person_id: Optional[str] = None
    #: The organization associated with the device
    org_id: str
    #: The capabilities of the device.
    capabilities: list[str]
    #: The permissions the user has for this device. For example, xapi means this user is entitled to using the xapi
    #: against this device.
    permissions: list[str]
    #: The connection status of the device.
    connection_status: Optional[ConnectionStatus] = None
    #: The product name. A display friendly version of the device's model.
    product: str
    #: The product type.
    product_type: ProductType = Field(alias='type')
    #: Tags assigned to the device.
    tags: list[str]
    #: The current IP address of the device.
    ip: Optional[str] = None
    #: The current network connectivity for the device.
    active_interface: Optional[str] = None
    #: The unique address for the network adapter.
    mac: Optional[str] = None
    #: The primary SIP address to dial this device.
    primary_sip_url: Optional[str] = None
    #: All SIP addresses to dial this device.
    sip_urls: list[Any]
    error_codes: Optional[list[Any]] = None
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
    #: The workspace location associated with the device.
    workspace_location_id: Optional[str] = None
    #: The date and time that the device was first seen, in ISO8601 format.
    first_seen: Optional[datetime] = None
    #: The date and time that the device was last seen, in ISO8601 format.
    last_seen: Optional[datetime] = None
    #: Entity managing the device configuration.
    managed_by: Optional[DeviceManagedBy] = None
    #: Manufacturer of the device
    #: only for 3rd party devices
    manufacturer: Optional[str] = None
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode
    #: only for 3rd party devices
    line_port: Optional[str] = None
    #: Contains the body of the HTTP response received following the request to the Console API
    #: Not set if the response has no body
    #: only for 3rd party devices
    outbound_proxy: Optional[str] = None
    #: SIP authentication user ame for the owner of the device
    #: only for 3rd party devices
    sip_user_name: Optional[str] = None
    #: The device platform.
    device_platform: Optional[DevicePlatform] = None
    #: TODO: undocumented, WXCAPIBULK-719
    lifecycle: Optional[Lifecycle] = None
    #: TODO: undocumented, WXCAPIBULK-719
    planned_maintenance: Optional[str] = None

    @model_validator(mode='before')
    def pop_place_id(cls, values):
        """
        :meta private:
        """
        values.pop('placeId', None)
        return values

    @field_validator('mac')
    def mac_no_colon(cls, v: str) -> str:
        """
        :meta private:
        """
        return v.replace(':', '')


class TagOp(str, Enum):
    add = 'add'
    remove = 'remove'
    replace = 'replace'


class ActivationCodeResponse(ApiModel):
    #: The activation code.
    code: str
    #: The date and time the activation code expires.
    expiry_time: datetime


@dataclass(init=False, repr=False)
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

    #: device jobs Api
    settings_jobs: DeviceSettingsJobsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.settings_jobs = DeviceSettingsJobsApi(session=session)

    def list(self, person_id: str = None, workspace_id: str = None, location_id: str = None,
             workspace_location_id: str = None, display_name: str = None, product: str = None,
             product_type: ProductType = None, tag: str = None, connection_status: ConnectionStatus = None,
             serial: str = None, software: str = None, upgrade_channel: str = None, error_code: str = None,
             capability: str = None, permission: str = None, mac: str = None, device_platform: DevicePlatform = None,
             org_id: str = None, **params) -> Generator[Device, None, None]:
        """
        List Devices

        Lists all active Webex devices associated with the authenticated user, such as devices activated in personal
        mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param location_id: List devices by location ID.
        :type location_id: str
        :param workspace_location_id: List devices by workspace location ID. Deprecated, prefer `location_id`.
        :type workspace_location_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name.
        :type product: str
        :param product_type: List devices with this type. Possible values: roomdesk, phone, accessory, webexgo, unknown
        :type product_type: str
        :param tag: List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma
        :type tag: str
            separating the tag values or adding several tag parameters.
        :param connection_status: List devices with this connection statu
        :type connection_status: str
        :param serial: List devices with this serial number.
        :type serial: str
        :param software: List devices with this software version.
        :type software: str
        :param upgrade_channel: List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code: List devices with this error code.
        :type error_code: str
        :param capability: List devices with this capability. For example: xapi
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str
        :param mac: List devices with this MAC address.
        :type mac: str
        :param device_platform: List devices with this device platform.
        :type device_platform: DevicePlatform
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Device` instances
        """
        params.update((to_camel(p), enum_str(v))
                      for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        pt = params.pop('productType', None)
        if pt is not None:
            params['type'] = pt
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, params=params, item_key='items')

    def details(self, device_id: str, org_id: str = None) -> Device:
        """
        Get Device Details
        Shows details for a device, by ID.

        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id:
        :type org_id: str
        :return: Device details
        :rtype: Device
        """
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return Device.model_validate(data)

    def delete(self, device_id: str, org_id: str = None):
        """
        Delete a Device

        Deletes a device, by ID.

        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id:
        :type org_id: str
        """
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        super().delete(url=url, params=params)

    def modify_device_tags(self, device_id: str, op: TagOp, value: List[str] = None, org_id: str = None) -> Device:
        """
        Modify Device Tags

        Update requests use JSON Patch syntax.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param op: tag operation
        :type op: TagOp
        :param value: list of tags
        :type value: list[str]
        :param org_id:
        :type org_id: str
        :return: device details
        :rtype: Device
        """
        body = {'op': op.value if isinstance(op, TagOp) else op,
                'path': 'tags'}
        if value is not None:
            body['value'] = value
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        data = self.patch(url=url, json=body, params=params, content_type='application/json-patch+json')
        return Device.model_validate(data)

    def activation_code(self, workspace_id: str = None, person_id: str = None, model: str = None,
                        org_id: str = None) -> ActivationCodeResponse:
        """
        Create a Device Activation Code

        Generate an activation code for a device in a specific workspace by `workspaceId` or for a person by
        `personId`. This requires an auth token with the `identity:placeonetimepassword_create` and
        `spark-admin:devices_write` scopes.

        * Adding a device to a workspace with calling type `none` or `thirdPartySipCalling` will reset the workspace
          calling type to `freeCalling`.

        * Either `workspaceId` or `personId` should be provided. If both are supplied, the request will be invalid.

        * If no `model` is supplied, the `code` returned will only be accepted on RoomOS devices.

        * If your device is a phone, you must provide the `model` as a field. You can get the `model` from the
          `supported devices
          <https://developer.webex.com/docs/api/v1/device-call-settings/read-the-list-of-supported-devices>`_ API.


        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param org_id: The organization associated with the activation code generated.
        :type org_id: str
        :rtype: ActivationCodeResponse
        """
        params = org_id and {'orgId': org_id} or None
        body = {}
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if model is not None:
            body['model'] = model
        url = self.ep('activationCode')
        data = self.post(url=url, json=body, params=params)
        return ActivationCodeResponse.model_validate(data)

    def create_by_mac_address(self, mac: str, workspace_id: str = None, person_id: str = None,
                              model: str = None, password: str = None, org_id: str = None) -> Optional[Device]:
        """
        Create a phone by it's MAC address in a specific workspace or for a person.
        Specify the mac, model and either workspaceId or personId.

        :param mac: The MAC address of the device being created.
        :type mac: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param password: SIP password to be configured for the phone, only required with third party devices.
        :type password: str
        :param org_id: The organization associated with the device.
        :type org_id: str
        :return: created device information
        :rtype: Device
        """
        params = org_id and {'orgId': org_id} or None
        body = {'mac': mac}
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if model is not None:
            body['model'] = model
        if password is not None:
            body['password'] = password
        url = self.ep()
        data = super().post(url=url, json=body, params=params)
        if not data:
            return None
        return Device.model_validate(data)
