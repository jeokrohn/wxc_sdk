"""
Telephony devices
"""
import json
from collections.abc import Generator
from typing import Optional, Union, Any

from pydantic import TypeAdapter, Field, field_validator

from ...api_child import ApiChild
from ...base import ApiModel, plus1, to_camel, enum_str
from ...base import SafeEnum as Enum

__all__ = ['DectDevice', 'MemberCommon', 'DeviceMember', 'DeviceMembersResponse', 'AvailableMember', 'MACState',
           'MACStatus', 'MACValidationResponse', 'TelephonyDevicesApi', 'LineKeyType', 'ProgrammableLineKey',
           'LineKeyTemplate']

from ...common import PrimaryOrShared, UserType, ValidationStatus, DeviceCustomization, IdAndName, \
    ApplyLineKeyTemplateAction


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
    first_name: Optional[str] = None
    #: Last name of a person or workspace.
    last_name: Optional[str] = None
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This
    #: will be supported in a future update.
    phone_number: Optional[str] = None
    #: Extension of a person or workspace.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routingPrefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: PrimaryOrShared = Field(default=PrimaryOrShared.primary)
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool] = Field(default=True)
    location: Optional[IdAndName] = None

    @field_validator('phone_number', mode='before')
    def e164(cls, v):
        """
        :meta private:
        """
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
    #: Device line label.
    line_label: Optional[str] = None
    #: Registration Host IP address for the line port.
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: bool = Field(default=False)
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str] = None

    @staticmethod
    def from_available(available: 'AvailableMember') -> 'DeviceMember':
        data = json.loads(available.model_dump_json())
        return DeviceMember.model_validate(data)


class DeviceMembersResponse(ApiModel):
    """
    Get Device Members response
    """
    model: str
    members: list[DeviceMember]
    max_line_count: int

    # assert that members are always sorted by port number
    @field_validator('members', mode='after')
    def sort_members(cls, v):
        """
        :meta private:
        """
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
    error_code: Optional[int] = None
    #: Provides a status message about the MAC address.
    message: Optional[str] = None


class MACValidationResponse(ApiModel):
    #: Status of MAC address.
    status: ValidationStatus
    #: Contains an array of all the MAC address provided and their statuses.
    mac_status: Optional[list[MACStatus]] = None


class LineKeyType(str, Enum):
    #: PRIMARY_LINE is the user's primary extension. This is the default assignment for Line Key Index 1 and cannot be
    #: modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables User and Call Park monitoring.
    monitor = 'MONITOR'
    #: Allows users to reach a telephone number, extension or a SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key.
    #: These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'


class ProgrammableLineKey(ApiModel):
    #: An index representing a Line Key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2
    line_key_index: Optional[int] = None
    #: The action that would be performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL` and the value must be a valid Telephone Number,
    #: Ext, or SIP URI (format: user@host using A-Z,a-z,0-9,-_ .+ for user and host).
    #: example: 5646
    line_key_value: Optional[str] = None

    @classmethod
    def standard_plk_list(cls, lines: int = 10) -> list['ProgrammableLineKey']:
        """
        get a standard list of programmable line keys of given length.
        1st line key is primary line and all other are "open"

        :param lines: number of programmable line keys
        :return: list of programmable line keys
        """
        r = [ProgrammableLineKey(line_key_index=i, line_key_type=LineKeyType.open) for i in range(1, lines+1)]
        r[0].line_key_type = LineKeyType.primary_line
        return r


class LineKeyTemplate(ApiModel):
    #: Unique identifier for the Line Key Template
    #: example: Y2lzY29zcGFyazovL1VTL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS9kNDUzM2MwYi1hZGRmLTRjODUtODk0YS1hZTVkOTAyYzAyMDM=
    id: Optional[str] = None
    #: Name of the Line Key Template
    #: example: template for 8845
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable
    #: example: DMS Cisco 8845
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub
    #: example: Cisco 8845
    display_name: Optional[str] = Field(alias='modelDisplayName', default=None)
    #: Indicates whether user can reorder the line keys.
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKey]] = None

    def create_or_update(self) -> dict[str, Any]:
        """
        dict for create or update

        :meta private:
        """
        return self.model_dump(mode='json', exclude_none=True, by_alias=True, exclude={'id', 'display_name'})


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
        return DeviceMembersResponse.model_validate(data)

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
                member = member.model_copy(deep=True)
            members_for_update.append(member)

        if members_for_update:
            # now assign port indices
            port = 1
            for member in members_for_update:
                member.port = port
                port += member.line_weight

        # create body
        if members_for_update:
            members = ','.join(m.model_dump_json(include={'member_id', 'port', 't38_fax_compression_enabled',
                                                          'primary_owner', 'line_type', 'line_weight', 'line_label',
                                                          'hotline_enabled', 'hotline_destination',
                                                          'allow_call_decline_enabled'})
                               for m in members_for_update)
            body = f'{{"members": [{members}]}}'
        else:
            body = None

        url = self.ep(f'{device_id}/members')
        params = org_id and {'orgId': org_id} or None
        self.put(url=url, data=body, params=params)

    def available_members(self, device_id: str, location_id: str = None, member_name: str = None,
                          phone_number: str = None, extension: str = None, org_id: str = None,
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
        return DeviceCustomization.model_validate(data)

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
        body = customization.model_dump_json(include={'customizations', 'custom_enabled'})
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
        return TypeAdapter(list[DectDevice]).validate_python(data['devices'])

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
        return MACValidationResponse.model_validate(data)

    def create_line_key_template(self, template: LineKeyTemplate,
                                 org_id: str = None) -> str:
        """
        Create a Line Key Template

        Create a Line Key Template in this organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows customers to create a Line Key Template for a device model.

        Creating a Line Key Template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template: Line key template to create
        :type template: LineKeyTemplate
        :param org_id: id of organization to create the line key template in
        :type org_id: str
        :return: id of new line key template
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = template.create_or_update()
        url = self.ep('lineKeyTemplates')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def list_line_key_templates(self, org_id: str = None) -> list[LineKeyTemplate]:
        """
        Read the list of Line Key Templates

        List all Line Key Templates available for this organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve the list of Line Key Templates that are available for the organization.

        Retrieving this list requires a full, user or read-only administrator or location administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param org_id: List line key templates for this organization.
        :type org_id: str
        :rtype: list[LineKeyTemplate]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('lineKeyTemplates')
        data = super().get(url, params=params)
        r = TypeAdapter(list[LineKeyTemplate]).validate_python(data['lineKeyTemplates'])
        return r

    def line_key_template_details(self, template_id: str, org_id: str = None) -> LineKeyTemplate:
        """
        Get details of a Line Key Template

        Get detailed information about a Line Key Template by template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to retrieve a line key template by its ID in an organization.

        Retrieving a line key template requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param template_id: Get line key template for this template ID.
        :type template_id: str
        :param org_id: Retrieve a line key template for this organization.
        :type org_id: str
        :rtype: :class:`GetLineKeyTemplateResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'lineKeyTemplates/{template_id}')
        data = super().get(url, params=params)
        r = LineKeyTemplate.model_validate(data)
        return r

    def modify_line_key_template(self, template: LineKeyTemplate, org_id: str = None):
        """
        Modify a Line Key Template

        Modify a line key template by its template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to modify an existing Line Key Template by its ID in an organization.

        Modifying an existing line key template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template: new line key template settings
        :type template: LineKeyTemplate
        :param org_id: Modify a line key template for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'lineKeyTemplates/{template.id}')
        super().put(url, params=params, json=template.create_or_update())

    def delete_line_key_template(self, template_id: str, org_id: str = None):
        """
        Delete a Line Key Template

        Delete a Line Key Template by its template ID in an organization.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to delete an existing Line Key Templates by its ID in an organization.

        Deleting an existing line key template requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param template_id: Delete line key template with this template ID.
        :type template_id: str
        :param org_id: Delete a line key template for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'lineKeyTemplates/{template_id}')
        super().delete(url, params=params)

    def preview_apply_line_key_template(self, action: ApplyLineKeyTemplateAction, template_id: str = None,
                                        location_ids: list[str] = None, exclude_devices_with_custom_layout: bool = None,
                                        include_device_tags: list[str] = None, exclude_device_tags: list[str] = None,
                                        more_shared_appearances_enabled: bool = None,
                                        few_shared_appearances_enabled: bool = None,
                                        more_monitor_appearances_enabled: bool = None, org_id: str = None) -> int:
        """
        Preview Apply Line Key Template

        Preview the number of devices that will be affected by the application of a Line Key Template or when resetting
        devices to their factory Line Key settings.

        Line Keys also known as Programmable Line Keys (PLK) are the keys found on either sides of a typical desk phone
        display.
        A Line Key Template is a definition of actions that will be performed by each of the Line Keys for a particular
        device model.
        This API allows users to preview the number of devices that will be affected if a customer were to apply a Line
        Key Template or apply factory default Line Key settings to devices.

        Retrieving the number of devices affected requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param action: Line key Template action to perform.
        :type action: ApplyLineKeyTemplateAction
        :param template_id: `templateId` is required for `APPLY_TEMPLATE` action.
        :type template_id: str
        :param location_ids: Used to search for devices only in the given locations.
        :type location_ids: list[str]
        :param exclude_devices_with_custom_layout: Indicates whether to exclude devices with custom layout.
        :type exclude_devices_with_custom_layout: bool
        :param include_device_tags: Include devices only with these tags.
        :type include_device_tags: list[str]
        :param exclude_device_tags: Exclude devices with these tags.
        :type exclude_device_tags: list[str]
        :param more_shared_appearances_enabled: Refine search by warnings for More shared appearances than shared
            users.
        :type more_shared_appearances_enabled: bool
        :param few_shared_appearances_enabled: Refine search by warnings for Fewer shared appearances than shared
            users.
        :type few_shared_appearances_enabled: bool
        :param more_monitor_appearances_enabled: Refine search by warnings for more monitor appearances than monitors.
        :type more_monitor_appearances_enabled: bool
        :param org_id: Preview Line Key Template for this organization.
        :type org_id: str
        :rtype: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['action'] = enum_str(action)
        if template_id is not None:
            body['templateId'] = template_id
        if location_ids is not None:
            body['locationIds'] = location_ids
        if exclude_devices_with_custom_layout is not None:
            body['excludeDevicesWithCustomLayout'] = exclude_devices_with_custom_layout
        if include_device_tags is not None:
            body['includeDeviceTags'] = include_device_tags
        if exclude_device_tags is not None:
            body['excludeDeviceTags'] = exclude_device_tags
        if more_shared_appearances_enabled is not None:
            body['moreSharedAppearancesEnabled'] = more_shared_appearances_enabled
        if few_shared_appearances_enabled is not None:
            body['fewSharedAppearancesEnabled'] = few_shared_appearances_enabled
        if more_monitor_appearances_enabled is not None:
            body['moreMonitorAppearancesEnabled'] = more_monitor_appearances_enabled
        url = self.ep('actions/previewApplyLineKeyTemplate/invoke')
        data = super().post(url, params=params, json=body)
        r = data['deviceCount']
        return r
