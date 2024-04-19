from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaDeviceCallSettingsWithDeviceSettingsConfigurationApi', 'DeviceObject',
           'DeviceSettingsConfigurationObject', 'KemModuleTypeObject', 'ManagedByObject', 'ManufacturerObject',
           'OnboardingMethodObject', 'SupportedForObject', 'TypeObject']


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
    people = 'PEOPLE'
    place = 'PLACE'


class OnboardingMethodObject(str, Enum):
    mac_address = 'MAC_ADDRESS'
    activation_code = 'ACTIVATION_CODE'
    none_ = 'NONE'


class KemModuleTypeObject(str, Enum):
    kem_14_keys = 'KEM_14_KEYS'
    kem_18_keys = 'KEM_18_KEYS'


class DeviceSettingsConfigurationObject(str, Enum):
    #: Devices which supports Webex Calling Device Settings Configuration.
    webex_calling_device_configuration = 'WEBEX_CALLING_DEVICE_CONFIGURATION'
    #: Devices which supports Webex Device Settings Configuration.
    webex_device_configuration = 'WEBEX_DEVICE_CONFIGURATION'
    #: Devices does not support any configuration.
    none_ = 'NONE'


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
    #: Indicates whether Kem support is enabled or not.
    #: example: True
    kem_support_enabled: Optional[bool] = None
    #: Module count.
    kem_module_count: Optional[int] = None
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleTypeObject]] = None
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool] = None
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str] = None
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool] = None
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool] = None
    #: Enables / disables customized behavior support on devices.
    customized_behaviors_enabled: Optional[bool] = None
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool] = None
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool] = None
    #: Supports touch screen on device.
    touch_screen_phone: Optional[bool] = None
    #: Device settings configuration.
    device_settings_configuration: Optional[DeviceSettingsConfigurationObject] = None


class BetaDeviceCallSettingsWithDeviceSettingsConfigurationApi(ApiChild, base='telephony/config/supportedDevices'):
    """
    Beta Device Call Settings with Device Settings Configuration
    
    These APIs manages Webex Calling settings for devices with are of the Webex Calling type.
    
    Viewing Virtual Lines requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

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
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[DeviceObject]).validate_python(data['devices'])
        return r
