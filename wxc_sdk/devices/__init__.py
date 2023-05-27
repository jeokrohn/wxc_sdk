"""
Devices represent cloud-registered Webex RoomOS devices. Devices may be associated with Workspaces.

Searching and viewing details for your devices requires an auth token with the spark:devices_read scope. Updating or
deleting your devices requires an auth token with the spark:devices_write scope. Viewing the list of all devices in
an organization requires an administrator auth token with the spark-admin:devices_read scope. Adding, updating,
or deleting all devices in an organization requires an administrator auth token with the spark-admin:devices_write
scope. Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
"""

__all__ = ['DevicesApi', 'Device', 'TagOp', 'ActivationCodeResponse']

from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, List

from pydantic import root_validator, Field

from ..api_child import ApiChild
from ..base import SafeEnum as Enum
from ..base import to_camel, ApiModel
from ..rest import RestSession
from ..telephony.jobs import DeviceSettingsJobsApi


class Device(ApiModel):
    #: A unique identifier for the device.
    device_id: str = Field(alias='id')
    #: A friendly name for the device
    display_name: str
    #: The workspace associated with the device.
    workspace_id: Optional[str]
    #: The workspace location associated with the device.
    workspace_location_id: Optional[str]
    #: The person associated with the device.
    person_id: Optional[str]
    #: The organization associated with the device
    org_id: str
    #: The capabilities of the device.
    capabilities: list[str]
    #: The permissions the user has for this device. For example, xapi means this user is entitled to using the xapi
    #: against this device.
    permissions: list[str]
    #: The connection status of the device.
    connection_status: str
    #: The product name. A display friendly version of the device's model.
    product: str
    #: The product type.
    product_type: str = Field(alias='type')
    #: Tags assigned to the device.
    tags: list[str]
    #: The current IP address of the device.
    ip: Optional[str]
    #: The current network connectivty for the device.
    active_interface: Optional[str]
    #: The unique address for the network adapter.
    mac: Optional[str]
    #: The primary SIP address to dial this device.
    primary_sip_url: Optional[str]
    #: All SIP addresses to dial this device.
    sip_urls: list[Any]
    error_codes: Optional[list[Any]]
    #: Serial number for the device.
    serial: Optional[str]
    #: The operating system name data and version tag.
    software: Optional[str]
    #: The upgrade channel the device is assigned to.
    upgrade_channel: Optional[str]
    #: The date and time that the device was registered, in ISO8601 format.
    created: Optional[datetime]
    #: The date and time that the device was first seen, in ISO8601 format.
    first_seen: Optional[datetime]
    #: The date and time that the device was last seen, in ISO8601 format.
    last_seen: Optional[datetime]

    @root_validator(pre=True)
    def pop_place_id(cls, values):
        values.pop('placeId', None)
        return values


class TagOp(str, Enum):
    add = 'add'
    remove = 'remove'
    replace = 'replace'


class ActivationCodeResponse(ApiModel):
    #: The activation code.
    code: str
    #: The date and time the activation code expires.
    expiry_time: datetime


@dataclass(init=False)
class DevicesApi(ApiChild, base='devices'):
    """
    Devices represent cloud-registered Webex RoomOS devices or IP Phones. Devices may be associated with Workspaces
    or People.

    The following scopes are required for performing the specified actions:

    Searching and viewing details for devices requires an auth token with the spark:devices_read scope.

    Updating or deleting your devices requires an auth token with the spark:devices_write scope.

    Viewing the list of all devices in an organization requires an administrator auth token with
    the spark-admin:devices_read scope.

    Adding, updating, or deleting all devices in an organization requires an administrator auth token with
    the spark-admin:devices_write scope.

    Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
    """

    #: device jobs Api
    settings_jobs: DeviceSettingsJobsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.settings_jobs = DeviceSettingsJobsApi(session=session)

    def list(self, person_id: str = None, workspace_id: str = None, workspace_location_id: str = None,
             display_name: str = None, product: str = None,
             product_type: str = None, tag: str = None, connection_status: str = None, serial: str = None,
             software: str = None, upgrade_channel: str = None, error_code: str = None, capability: str = None,
             permission: str = None, org_id: str = None, **params) -> Generator[Device, None, None]:
        """
        List Devices

        Lists all active Webex devices associated with the authenticated user, such as devices activated in personal
        mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param workspace_location_id: List devices by workspace location ID.
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
        :param capability: List devices with this capability.
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Device` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
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
        return Device.parse_obj(data)

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

    def modify_device_tags(self, device_id: str, op: TagOp, value: List[str], org_id: str = None) -> Device:
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
                'path': 'tags',
                'value': value}
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        data = self.patch(url=url, json=body, params=params, content_type='application/json-patch+json')
        return Device.parse_obj(data)

    def activation_code(self, workspace_id: str=None, person_id: str = None, model: str = None,
                        org_id: str = None) -> ActivationCodeResponse:
        """
        Create a Device Activation Code

        Generate an activation code for a device in a specific workspace by workspaceId. Currently, activation codes
        may only be generated for shared workspaces--personal mode is not supported.

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
        return ActivationCodeResponse.parse_obj(data)

    def create_by_mac_address(self, mac: str, workspace_id: str = None, person_id: str = None,
                              model: str = None, password: str = None, org_id: str = None) -> Device:
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
            body.password = password
        url = self.ep()
        data = super().post(url=url, json=body, params=params)
        return Device.parse_obj(data)
