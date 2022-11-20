"""
Telephony devices
"""
import json
from collections.abc import Generator
from typing import Optional, Union

from pydantic import parse_obj_as, Field, validator

from ...api_child import ApiChild
from ...base import ApiModel, plus1, to_camel
from ...base import SafeEnum as Enum

__all__ = ['DectDevice', 'MemberCommon', 'DeviceMember', 'DeviceMembersResponse', 'AvailableMember', 'MACState',
           'MACStatus', 'MACValidationResponse', 'TelephonyDevicesApi']

from ...common import PrimaryOrShared, UserType, ValidationStatus, DeviceCustomization


class DectDevice(ApiModel):
    #: Model name of the device.
    model: str
    #: Display name of the device.
    display_name: str
    #: Indicates number of base stations.
    number_of_base_stations: int
    #: Indicates number of port lines,
    number_of_line_ports: int
    #: Indicates number of supported registrations.
    number_of_registrations_supported: int


class MemberCommon(ApiModel):
    #: Unique identifier for the member.
    member_id: str = Field(alias='id')
    member_type: UserType = Field(default=UserType.people)
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This
    #: will be supported in a future update.
    phone_number: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: PrimaryOrShared = Field(default=PrimaryOrShared.primary)
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool] = Field(default=True)

    @validator('phone_number', pre=True)
    def e164(cls, v):
        return plus1(v)


class DeviceMember(MemberCommon):
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary
    #: Line/Port of the device.
    primary_owner: bool = Field(default=False)
    #: Port number assigned to person or workspace.
    port: int = Field(default=1)
    #: Number of lines that have been configured for the person on the device. Can only be larger than one for primary
    #: owner
    line_weight: int = Field(default=1)
    #: Registration Host IP address for the line port.
    host_ip: Optional[str] = Field(alias='hostIP')
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str] = Field(alias='remoteIP')
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: bool = Field(default=False)
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]

    @staticmethod
    def from_available(available: 'AvailableMember') -> 'DeviceMember':
        data = json.loads(available.json())
        return DeviceMember.parse_obj(data)


class DeviceMembersResponse(ApiModel):
    """
    Get Device Members response
    """
    model: str
    members: list[DeviceMember]
    max_line_count: int

    # assert that members are always sorted by port number
    @validator('members', pre=False)
    def sort_members(cls, v):
        v.sort(key=lambda dm: dm.port)
        return v


class AvailableMember(MemberCommon):
    ...


class MACState(str, Enum):
    """
    State of the MAC address.
    """
    #: The requested MAC address is available.
    available = 'AVAILABLE'
    #: The requested MAC address is unavailable.
    unavailable = 'UNAVAILABLE'
    #: The requested MAC address is duplicated.
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    #: The requested MAC address is invalid.
    invalid = 'INVALID'


class MACStatus(ApiModel):
    #: MAC address.
    mac: str
    #: State of the MAC address.
    state: MACState
    #: MAC address validation error code.
    error_code: Optional[int]
    #: Provides a status message about the MAC address.
    message: Optional[str]


class MACValidationResponse(ApiModel):
    #: Status of MAC address.
    status: ValidationStatus
    #: Contains an array of all the MAC address provided and their statuses.
    mac_status: Optional[list[MACStatus]]


class TelephonyDevicesApi(ApiChild, base='telephony/config/devices'):
    """
    Telephony devices API
    """

    def members(self, device_id: str, org_id: str = None) -> DeviceMembersResponse:
        """
        Get Device Members

        Get the list of all the members of the device including primary and secondary users.

        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and search for available members on a device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this Organization.
        :type org_id: str
        :return: Device model, line count, and members
        :rtype: DeviceMembersResponse
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{device_id}/members')
        data = self.get(url=url, params=params)
        return DeviceMembersResponse.parse_obj(data)

    def update_members(self, device_id: str, members: Optional[list[Union[DeviceMember, AvailableMember]]],
                       org_id: str = None):
        """
        Modify member details on the device.

        A device member can be either a person or a workspace. An admin can access the list of member details,
        modify member details and search for available members on a device.

        Modifying members on the device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param members: New member details for the device. If the member's list is missing then all the users are
            removed except the primary user.
        :type members: list[Union[DeviceMember, AvailableMember]
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        """
        members_for_update = []
        for member in members:
            if isinstance(member, AvailableMember):
                member = DeviceMember.from_available(member)
            else:
                member = member.copy(deep=True)
            members_for_update.append(member)

        if members_for_update:
            # now assign port indices
            port = 1
            for member in members_for_update:
                member.port = port
                port += member.line_weight

        # create body
        if members_for_update:
            members = ','.join(m.json(include={'member_id', 'port', 't38_fax_compression_enabled', 'primary_owner',
                                               'line_type', 'line_weight', 'hotline_enabled', 'hotline_destination',
                                               'allow_call_decline_enabled'})
                               for m in members_for_update)
            body = f'{{"members": [{members}]}}'
        else:
            body = None

        url = self.ep(f'{device_id}/members')
        params = org_id and {'orgId': org_id} or None
        self.put(url=url, data=body, params=params)

    def available_members(self, device_id: str, location_id: str, member_name: str = None, phone_number: str = None,
                          extension: str = None, org_id: str = None,
                          **params) -> Generator[AvailableMember, None, None]:
        """
        Search members that can be assigned to the device.

        A device member can be either a person or a workspace. A admin can access the list of member details,
        modify member details and search for available members on a device.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Search (Contains) based on number.
        :type location_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param org_id: Retrieves the list of available members on the device in this Organization.
        :type org_id: str
        :return: list of available members
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params', 'device_id'} and v is not None)
        url = self.ep(f'{device_id}/availableMembers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AvailableMember, params=params, item_key='members')

    def apply_changes(self, device_id: str, org_id: str = None):
        """
        Apply Changes for a specific device

        Issues request to the device to download and apply changes to the configuration.

        Applying changes for a specific device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.
        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this Organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{device_id}/actions/applyChanges/invoke')
        self.post(url=url, params=params)

    def device_settings(self, device_id: str, device_model: str, org_id: str = None) -> DeviceCustomization:
        """
        Get override settings for a device.

        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str
        :return: Device settings
        :rtype: DeviceCustomization
        """
        params = {'model': device_model}
        if org_id:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/settings')
        data = self.get(url=url, params=params)
        return DeviceCustomization.parse_obj(data)

    def update_device_settings(self, device_id: str, device_model: str, customization: DeviceCustomization,
                               org_id: str = None):
        """
        Modify override settings for a device.

        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins
        can also modify the settings. NOTE: DECT devices do not support settings at the device level.

        Updating settings on the device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Device model name.
        :type device_model: str
        :param customization: Indicates the customization object of the device settings.
        :type customization: DeviceCustomization
        :param org_id: Organization in which the device resides..
        :type org_id: str

        Example :

            .. code-block:: python

                # target_device is a TelephonyDevice object
                target_device: TelephonyDevice

                # get device level settings
                settings = api.telephony.devices.device_settings(device_id=target_device.device_id,
                                                                 device_model=target_device.model)

                # update settings (display name format) and enable device level customization
                settings.customizations.mpp.display_name_format = DisplayNameSelection.person_last_then_first_name
                settings.custom_enabled = True

                # update the device level settings
                api.telephony.devices.update_device_settings(device_id=target_device.device_id,
                                                             device_model=target_device.model,
                                                             customization=settings)

                # apply changes to device
                api.telephony.devices.apply_changes(device_id=target_device.device_id)

        """
        params = {'model': device_model}
        if org_id:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/settings')
        body = customization.json(include={'customizations', 'custom_enabled'})
        self.put(url=url, params=params, data=body)

    def dect_devices(self, org_id: str = None) -> list[DectDevice]:
        """
        Read the DECT device type list

        Get DECT device type list with base stations and line ports supported count. This is a static list.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id:
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('dects/supportedDevices')
        data = self.get(url=url, params=params)
        return parse_obj_as(list[DectDevice], data['devices'])

    def validate_macs(self, macs: list[str], org_id: str = None) -> MACValidationResponse:
        """
        Validate a list of MAC addresses.

        Validating this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param macs: MAC addresses to be validated.
        :type macs: list[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str
        :return: validation response
        :rtype: :class:`MACValidationResponse`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('actions/validateMacs/invoke')
        data = self.post(url=url, params=params, json={'macs': macs})
        return MACValidationResponse.parse_obj(data)
