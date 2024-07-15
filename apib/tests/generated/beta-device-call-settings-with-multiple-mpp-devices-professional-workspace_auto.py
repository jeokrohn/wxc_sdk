from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActivationStates', 'BetaDeviceCallSettingsWithMultipleMPPDevicesInAProfessionalWorkspaceApi', 'DeviceList',
           'DeviceOwner', 'Devices', 'HotelingRequest', 'LineType', 'MemberType']


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class HotelingRequest(ApiModel):
    #: Enable or disable (hoteling host. Enabling the device for hoteling means that a guest (end user) can log into
    #: this host (workspace device) and use this device.
    #: 
    #: as if it were their own. When traveling to a remote office but still needing to place/receive calls with their
    #: telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool] = None
    #: Limits the time a guest can use the device. The time limit is configured via `guestHoursLimit`.
    limit_guest_use: Optional[bool] = None
    #: Time limit in hours until hoteling is enabled. Mandatory if `limitGuestUse` is enabled.
    guest_hours_limit: Optional[int] = None


class MemberType(str, Enum):
    #: Associated member is a person.
    people = 'PEOPLE'
    #: Associated member is a workspace.
    place = 'PLACE'
    #: Associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str] = None
    #: Enumeration that indicates if the member is of type `PEOPLE` or `PLACE`.
    type: Optional[MemberType] = None
    #: First name of device owner.
    first_name: Optional[str] = None
    #: Last name of device owner.
    last_name: Optional[str] = None


class ActivationStates(str, Enum):
    #: Device is activating.
    activating = 'ACTIVATING'
    #: Device is activated.
    activated = 'ACTIVATED'
    #: Device is deactivated.
    deactivated = 'DEACTIVATED'


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ip_address: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device and points to a primary line/port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Hoteling settings available when the device is the user's primary device and the device type is PRIMARY.
    hoteling: Optional[HotelingRequest] = None
    #: Owner of device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of device.
    activation_state: Optional[ActivationStates] = None


class DeviceList(ApiModel):
    #: Array of devices available to a person.
    devices: Optional[list[Devices]] = None
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int] = None
    #: Maximum number of devices a person can own.
    max_owned_device_count: Optional[int] = None


class BetaDeviceCallSettingsWithMultipleMPPDevicesInAProfessionalWorkspaceApi(ApiChild, base='telephony/config'):
    """
    Beta Device Call Settings with Multiple MPP Devices in a Professional Workspace
    
    These APIs manage Webex Calling settings for Webex Calling devices and have been enhanced to return device counts.
    
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def get_user_devices(self, person_id: str, org_id: str = None) -> DeviceList:
        """
        Get User Devices

        Get all devices for a person.

        Requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str
        :rtype: :class:`DeviceList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices')
        data = super().get(url, params=params)
        r = DeviceList.model_validate(data)
        return r

    def get_workspace_devices(self, workspace_id: str, org_id: str = None) -> DeviceList:
        """
        Get Workspace Devices

        Get all devices for a workspace.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :rtype: :class:`DeviceList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices')
        data = super().get(url, params=params)
        r = DeviceList.model_validate(data)
        return r
