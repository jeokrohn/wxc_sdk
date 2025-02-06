from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaDeviceCallSettingsWithMultilineSupportApi', 'DeviceLayout', 'DeviceObject',
           'DeviceSettingsConfigurationObject', 'GetLineKeyTemplateResponse', 'KEMKeys', 'KemModuleType',
           'LayoutMode', 'LineKeyType', 'ManagedByObject', 'ManufacturerObject', 'OnboardingMethodObject',
           'ProgrammableLineKeys', 'SupportedForObject', 'SupportsLogCollectionObject', 'TypeObject']


class LayoutMode(str, Enum):
    #: Default layout mode when a new device is added.
    default = 'DEFAULT'
    #: Enables a device to have its custom layout.
    custom = 'CUSTOM'


class LineKeyType(str, Enum):
    #: PRIMARY_LINE is the user's primary extension. This is the default assignment for Line Key Index 1 and cannot be
    #: modified.
    primary_line = 'PRIMARY_LINE'
    #: Shows the appearance of other users on the owner's phone.
    shared_line = 'SHARED_LINE'
    #: Enables User and Call Park monitoring.
    monitor = 'MONITOR'
    #: Enables the configure layout feature in Control Hub to set call park extension implicitly.
    call_park_extension = 'CALL_PARK_EXTENSION'
    #: Allows users to reach a telephone number, extension or a SIP URI.
    speed_dial = 'SPEED_DIAL'
    #: An open key will automatically take the configuration of a monitor button starting with the first open key.
    #: These buttons are also usable by the user to configure speed dial numbers on these keys.
    open = 'OPEN'
    #: Button not usable but reserved for future features.
    closed = 'CLOSED'


class ProgrammableLineKeys(ApiModel):
    #: An index representing a Line Key. Index starts from 1 representing the first key on the left side of the phone.
    #: example: 2
    line_key_index: Optional[int] = None
    #: The action that would be performed when the Line Key is pressed.
    #: example: SPEED_DIAL
    line_key_type: Optional[LineKeyType] = None
    #: This is applicable only when the lineKeyType is `SPEED_DIAL`.
    #: example: Help Line
    line_key_label: Optional[str] = None
    #: Applicable only when the `lineKeyType` is `SPEED_DIAL`. Value must be a valid telephone number, ext, or SIP URI
    #: (format: `user@host` using A-Z,a-z,0-9,-_ .+ for `user` and `host`).
    #: example: 5646
    line_key_value: Optional[str] = None
    #: Shared line index is the line label number of the shared or virtual line assigned in the configured lines. Since
    #: you can add multiple appearances of the same shared or virtual line on a phone, entering the index number
    #: assigns the respective line to a line key. This is applicable only when the `lineKeyType` is SHARED_LINE, If
    #: multiple programmable line keys are configured as shared lines, and If the `sharedLineIndex` is sent for any of
    #: the shared line, then the `sharedLineIndex` should be sent for all other shared lines. When `lineKeyType` is
    #: SHARED_LINE and `sharedLineIndex` is not assigned to any of the configured lines, then `sharedLineIndex` is
    #: assigned by default in the order the shared line appears in the request.
    #: example: 4
    shared_line_index: Optional[int] = None


class KemModuleType(str, Enum):
    #: Extension module has 14 line keys that can be configured.
    kem_14_keys = 'KEM_14_KEYS'
    #: Extension module has 18 line keys that can be configured.
    kem_18_keys = 'KEM_18_KEYS'
    #: Extension module has 20 line keys that can be configured.
    kem_20_keys = 'KEM_20_KEYS'


class KEMKeys(ApiModel):
    #: An index representing a KEM Module. The Index starts from 1 representing the first KEM Module.
    #: example: 1
    kem_module_index: Optional[int] = None
    #: An index representing a KEM Key. The Index starts from 1 representing the first key on the left side of the
    #: phone.
    #: example: 1
    kem_key_index: Optional[int] = None
    #: The action that would be performed when the KEM Key is pressed.
    #: example: SPEED_DIAL
    kem_key_type: Optional[LineKeyType] = None
    #: Applicable only when the kemKeyType is `SPEED_DIAL`.
    #: example: Office
    kem_key_label: Optional[str] = None
    #: Applicable only when the `lineKeyType` is `SPEED_DIAL`. Value must be a valid telephone number, ext, or SIP URI
    #: (format: `user@host` using A-Z,a-z,0-9,-_ .+ for `user` and `host`).
    #: example: 213457
    kem_key_value: Optional[str] = None
    #: Shared line index is the line label number of the shared or virtual line assigned in the configured lines. Since
    #: you can add multiple appearances of the same shared or virtual line on a phone, entering the index number
    #: assigns the respective line to a line key. This is applicable only when the `lineKeyType` is SHARED_LINE, If
    #: multiple programmable line keys are configured as shared lines, and If the `sharedLineIndex` is sent for any of
    #: the shared line, then the `sharedLineIndex` should be sent for all other shared lines. When `lineKeyType` is
    #: SHARED_LINE and `sharedLineIndex` is not assigned to any of the configured lines, then `sharedLineIndex` is
    #: assigned by default in the order the shared line appears in the request.
    #: example: 4
    shared_line_index: Optional[int] = None


class DeviceLayout(ApiModel):
    #: Defines the layout mode of the device, for example, `DEFAULT` or `CUSTOM`.
    layout_mode: Optional[LayoutMode] = None
    #: If `true`, user customization is enabled.
    #: example: True
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None
    #: Type of KEM module.
    kem_module_type: Optional[KemModuleType] = None
    #: Contains a mapping of KEM Keys and their corresponding actions.
    kem_keys: Optional[list[KEMKeys]] = None


class TypeObject(str, Enum):
    #: Cisco Multiplatform Phone.
    mpp = 'MPP'
    #: Analog Telephone Adapters.
    ata = 'ATA'
    #: GENERIC Session Initiation Protocol.
    generic_sip = 'GENERIC_SIP'
    #: Esim Supported Webex Go.
    esim = 'ESIM'
    #: Desk Phone.
    desk_phone = 'DESK_PHONE'


class ManufacturerObject(str, Enum):
    #: Devices manufactured by Cisco.
    cisco = 'CISCO'
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for
    #: provisioning in the control hub.
    third_party = 'THIRD_PARTY'


class ManagedByObject(str, Enum):
    #: Devices managed by Cisco.
    cisco = 'CISCO'
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the
    #: control hub.
    customer = 'CUSTOMER'


class SupportedForObject(str, Enum):
    #: Devices supported for people.
    people = 'PEOPLE'
    #: Devices supported for place.
    place = 'PLACE'


class OnboardingMethodObject(str, Enum):
    #: Devices onboarding method using MAC Address.
    mac_address = 'MAC_ADDRESS'
    #: Devices onboarding method using Activation Code.
    activation_code = 'ACTIVATION_CODE'
    #: Devices onboarding method using none.
    none_ = 'NONE'


class DeviceSettingsConfigurationObject(str, Enum):
    #: Devices which supports Webex Calling Device Settings Configuration.
    webex_calling_device_configuration = 'WEBEX_CALLING_DEVICE_CONFIGURATION'
    #: Devices which supports Webex Device Settings Configuration.
    webex_device_configuration = 'WEBEX_DEVICE_CONFIGURATION'
    #: Devices does not support any configuration.
    none_ = 'NONE'


class SupportsLogCollectionObject(str, Enum):
    #: Devices which does not support log collection.
    none_ = 'NONE'
    #: Devices which supports Cisco PRT log collection.
    cisco_prt = 'CISCO_PRT'
    #: Devices which supports Cisco RoomOS log collection.
    cisco_roomos = 'CISCO_ROOMOS'


class DeviceObject(ApiModel):
    #: Model name of the device.
    #: example: 2N Customer Managed
    model: Optional[str] = None
    #: Display name of the device.
    #: example: 2N Customer Managed
    display_name: Optional[str] = None
    #: Type of the device.
    #: example: GENERIC_SIP
    type: Optional[TypeObject] = None
    #: Manufacturer of the device.
    #: example: THIRD_PARTY
    manufacturer: Optional[ManufacturerObject] = None
    #: Users who manage the device.
    #: example: CUSTOMER
    managed_by: Optional[ManagedByObject] = None
    #: List of places the device is supported for.
    supported_for: Optional[list[SupportedForObject]] = None
    #: Onboarding method.
    onboarding_method: Optional[list[OnboardingMethodObject]] = None
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: Optional[bool] = None
    #: Number of port lines.
    number_of_line_ports: Optional[int] = None
    #: If `true`, KEM is supported.
    #: example: True
    kem_support_enabled: Optional[bool] = None
    #: Module count.
    kem_module_count: Optional[int] = None
    #: Enables / disables Kem lines support.
    kem_lines_support_enabled: Optional[bool] = None
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleType]] = None
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool] = None
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str] = None
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool] = None
    #: Enables / disables the additional shared line appearances.
    additional_secondary_line_appearances_enabled: Optional[bool] = None
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool] = None
    #: Enables / disables customized behavior support on devices.
    customized_behaviors_enabled: Optional[bool] = None
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool] = None
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool] = None
    #: Enables / disables support line port reordering.
    supports_line_port_reordering_enabled: Optional[bool] = None
    #: Enables / disables port number support.
    port_number_support_enabled: Optional[bool] = None
    #: Enables / disables T.38.
    t38_enabled: Optional[bool] = None
    #: Enables / disables call declined.
    call_declined_enabled: Optional[bool] = None
    #: Supports touch screen on device.
    touch_screen_phone: Optional[bool] = None
    #: Number of line key buttons for a device.
    number_of_line_key_buttons: Optional[int] = None
    #: Device settings configuration.
    device_settings_configuration: Optional[DeviceSettingsConfigurationObject] = None
    #: Enables / disables hoteling host.
    allow_hoteling_host_enabled: Optional[bool] = None
    #: Device log collection configuration.
    supports_log_collection: Optional[SupportsLogCollectionObject] = None
    #: Enables / disables apply changes.
    supports_apply_changes_enabled: Optional[bool] = None
    #: Enables / disables configure lines.
    allow_configure_lines_enabled: Optional[bool] = None
    #: Enables / disables configure phone settings.
    allow_configure_phone_settings_enabled: Optional[bool] = None
    #: Enables / disables hotline support.
    supports_hotline_enabled: Optional[bool] = None


class GetLineKeyTemplateResponse(ApiModel):
    #: Unique identifier for the Line Key Template.
    #: example: Y2lzY29zcGFyazovL3VzL0RFVklDRV9MSU5FX0tFWV9URU1QTEFURS81NzVhMWY3Zi03MjRkLTRmZGUtODk4NC1mNjNhNDljMzYxZmQ
    id: Optional[str] = None
    #: Name of the Line Key Template.
    #: example: Basic Template
    template_name: Optional[str] = None
    #: The Device Model for which the Line Key Template is applicable.
    #: example: 'DMS Cisco 6821'
    device_model: Optional[str] = None
    #: The friendly display name used to represent the device model in Control Hub.
    #: example: Cisco 6821
    model_display_name: Optional[str] = None
    #: Indicates whether user can reorder the line keys.
    user_reorder_enabled: Optional[bool] = None
    #: Contains a mapping of Line Keys and their corresponding actions.
    line_keys: Optional[list[ProgrammableLineKeys]] = None


class BetaDeviceCallSettingsWithMultilineSupportApi(ApiChild, base='telephony/config'):
    """
    Beta Device Call Settings With Multiline Support
    
    These APIs manage Webex Calling settings for devices of the Webex Calling type.
    
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def get_device_layout_by_device_id(self, device_id: str, org_id: str = None) -> DeviceLayout:
        """
        Get Device Layout by Device ID

        Get layout information of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Get device layout for this device ID.
        :type device_id: str
        :param org_id: Retrieve a device layout for the device in this organization.
        :type org_id: str
        :rtype: :class:`DeviceLayout`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/layout')
        data = super().get(url, params=params)
        r = DeviceLayout.model_validate(data)
        return r

    def modify_device_layout_by_device_id(self, device_id: str, layout_mode: LayoutMode,
                                          line_keys: list[ProgrammableLineKeys], user_reorder_enabled: bool = None,
                                          kem_module_type: KemModuleType = None, kem_keys: list[KEMKeys] = None,
                                          org_id: str = None):
        """
        Modify Device Layout by Device ID

        Modify the layout of a device by device ID in an organization.

        Device layout customizes a user’s programmable line keys (PLK) on the phone and any attached Key Expansion
        Modules (KEM) with the existing configured line members and the user’s monitoring list.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Modify device layout for this device ID.
        :type device_id: str
        :param layout_mode: Defines the layout mode of the device, for example, `DEFAULT` or `CUSTOM`.
        :type layout_mode: LayoutMode
        :param line_keys: Contains a mapping of Line Keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: If `true`, user customization is enabled.
        :type user_reorder_enabled: bool
        :param kem_module_type: Type of KEM module.
        :type kem_module_type: KemModuleType
        :param kem_keys: Contains a mapping of KEM Keys and their corresponding actions.
        :type kem_keys: list[KEMKeys]
        :param org_id: Modify a device layout for the device in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['layoutMode'] = enum_str(layout_mode)
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        if kem_module_type is not None:
            body['kemModuleType'] = enum_str(kem_module_type)
        if kem_keys is not None:
            body['kemKeys'] = TypeAdapter(list[KEMKeys]).dump_python(kem_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/{device_id}/layout')
        super().put(url, params=params, json=body)

    def create_a_line_key_template(self, template_name: str, device_model: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None) -> str:
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

        :param template_name: Name of the Line Key Template.
        :type template_name: str
        :param device_model: The model of the device for which the Line Key Template is applicable. The corresponding
            device model display name sometimes called the product name, can also be used to specify the model.
        :type device_model: str
        :param line_keys: Contains a mapping of Line Keys and their corresponding actions.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: User Customization Enabled.
        :type user_reorder_enabled: bool
        :param org_id: Organization to which line key template belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['templateName'] = template_name
        body['deviceModel'] = device_model
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('devices/lineKeyTemplates')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def read_the_list_of_supported_devices(self, allow_configure_layout_enabled: bool = None, type: str = None,
                                           org_id: str = None) -> list[DeviceObject]:
        """
        Read the List of Supported Devices

        Gets the list of supported devices for an organization.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param allow_configure_layout_enabled: List supported devices that allow the user to configure the layout.
        :type allow_configure_layout_enabled: bool
        :param type: List supported devices of a specific type. To excluded device types from a request or query, add
            `type=not:DEVICE_TYPE`. For example, `type=not:MPP`.
        :type type: str
        :param org_id: List supported devices for an organization.
        :type org_id: str
        :rtype: list[DeviceObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if allow_configure_layout_enabled is not None:
            params['allowConfigureLayoutEnabled'] = str(allow_configure_layout_enabled).lower()
        if type is not None:
            params['type'] = type
        url = self.ep('supportedDevices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DeviceObject]).validate_python(data['devices'])
        return r

    def get_details_of_a_line_key_template(self, template_id: str, org_id: str = None) -> GetLineKeyTemplateResponse:
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
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        data = super().get(url, params=params)
        r = GetLineKeyTemplateResponse.model_validate(data)
        return r

    def modify_a_line_key_template(self, template_id: str, line_keys: list[ProgrammableLineKeys],
                                   user_reorder_enabled: bool = None, org_id: str = None):
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

        :param template_id: Modify line key template with this template ID.
        :type template_id: str
        :param line_keys: List of line keys that are being updated.
        :type line_keys: list[ProgrammableLineKeys]
        :param user_reorder_enabled: Indicates whether the user can reorder the line keys.
        :type user_reorder_enabled: bool
        :param org_id: Modify a line key template for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if user_reorder_enabled is not None:
            body['userReorderEnabled'] = user_reorder_enabled
        body['lineKeys'] = TypeAdapter(list[ProgrammableLineKeys]).dump_python(line_keys, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'devices/lineKeyTemplates/{template_id}')
        super().put(url, params=params, json=body)
