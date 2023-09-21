from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DeviceConfiguration', 'DeviceConfigurationCollectionResponse', 'DeviceConfigurationConfiguration_key', 'DeviceConfigurationConfiguration_keySource', 'DeviceConfigurationConfiguration_keySources', 'DeviceConfigurationConfiguration_keySourcesConfigured', 'DeviceConfigurationConfiguration_keySourcesConfiguredEditability', 'DeviceConfigurationConfiguration_keySourcesConfiguredEditabilityReason', 'DeviceConfigurationConfiguration_keySourcesDefault', 'DeviceConfigurationConfiguration_keySourcesDefaultEditability', 'DeviceConfigurationConfiguration_keyValueSpace', 'UpdateDeviceConfigurationsOp']


class DeviceConfigurationConfiguration_keySource(str, Enum):
    #: Current value comes from the schema default.
    default = 'default'
    #: Current value comes from configuredValue.
    configured = 'configured'


class DeviceConfigurationConfiguration_keySourcesDefaultEditability(ApiModel):
    #: Whether or not the value is editable on this source (always `false` for `default`).
    is_editable: Optional[bool] = None
    #: The reason value is not editable on this source (always `FACTORY_DEFAULT` for `default`).
    #: example: FACTORY_DEFAULT
    reason: Optional[str] = None


class DeviceConfigurationConfiguration_keySourcesDefault(ApiModel):
    editability: Optional[DeviceConfigurationConfiguration_keySourcesDefaultEditability] = None


class DeviceConfigurationConfiguration_keySourcesConfiguredEditabilityReason(str, Enum):
    #: User is not authorized to edit any values.
    not_authorized = 'NOT_AUTHORIZED'
    #: The configuration is managed by a different authority. For example `CUCM`.
    config_managed_by_different_authority = 'CONFIG_MANAGED_BY_DIFFERENT_AUTHORITY'


class DeviceConfigurationConfiguration_keySourcesConfiguredEditability(ApiModel):
    #: Whether or not the value is editable on this source.
    #: example: True
    is_editable: Optional[bool] = None
    #: The reason the value is not editable on this source.
    #: example: NOT_AUTHORIZED
    reason: Optional[DeviceConfigurationConfiguration_keySourcesConfiguredEditabilityReason] = None


class DeviceConfigurationConfiguration_keySourcesConfigured(ApiModel):
    editability: Optional[DeviceConfigurationConfiguration_keySourcesConfiguredEditability] = None


class DeviceConfigurationConfiguration_keySources(ApiModel):
    default: Optional[DeviceConfigurationConfiguration_keySourcesDefault] = None
    configured: Optional[DeviceConfigurationConfiguration_keySourcesConfigured] = None


class DeviceConfigurationConfiguration_keyValueSpace(ApiModel):
    ...


class DeviceConfigurationConfiguration_key(ApiModel):
    #: The source of the current value that is applied to the device.
    source: Optional[DeviceConfigurationConfiguration_keySource] = None
    sources: Optional[DeviceConfigurationConfiguration_keySources] = None
    #: [JSON Schema](http://json-schema.org/) describing the data format of the configuration as specified by the device.
    value_space: Optional[DeviceConfigurationConfiguration_keyValueSpace] = None


class DeviceConfiguration(ApiModel):
    #: Key of the configuration.
    configuration_key: Optional[DeviceConfigurationConfiguration_key] = Field(alias='configuration_key', default=None)


class DeviceConfigurationCollectionResponse(ApiModel):
    #: ID of the device that the configurations are for.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RFVklDRS9hNmYwYjhkMi01ZjdkLTQzZDItODAyNi0zM2JkNDg3NjYzMTg=
    device_id: Optional[str] = None
    items: Optional[DeviceConfiguration] = None


class UpdateDeviceConfigurationsOp(str, Enum):
    #: Remove the configured value and revert back to the default from schema, if present.
    remove = 'remove'
    #: Set the configured value.
    replace = 'replace'
