from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['DeviceConfiguration', 'DeviceConfigurationCollectionResponse', 'DeviceConfigurationConfigurationKey',
           'DeviceConfigurationConfigurationKeySource', 'DeviceConfigurationConfigurationKeySources',
           'DeviceConfigurationConfigurationKeySourcesConfigured',
           'DeviceConfigurationConfigurationKeySourcesConfiguredEditability',
           'DeviceConfigurationConfigurationKeySourcesConfiguredEditabilityReason',
           'DeviceConfigurationConfigurationKeySourcesDefault',
           'DeviceConfigurationConfigurationKeySourcesDefaultEditability', 'DeviceConfigurationsApi', 'Op']


class DeviceConfigurationConfigurationKeySource(str, Enum):
    #: Current value comes from the schema default.
    default = 'default'
    #: Current value comes from configuredValue.
    configured = 'configured'


class DeviceConfigurationConfigurationKeySourcesDefaultEditability(ApiModel):
    #: Whether or not the value is editable on this source (always `false` for `default`).
    is_editable: Optional[bool] = None
    #: The reason value is not editable on this source (always `FACTORY_DEFAULT` for `default`).
    reason: Optional[str] = None


class DeviceConfigurationConfigurationKeySourcesDefault(ApiModel):
    editability: Optional[DeviceConfigurationConfigurationKeySourcesDefaultEditability] = None


class DeviceConfigurationConfigurationKeySourcesConfiguredEditabilityReason(str, Enum):
    #: User is not authorized to edit any values.
    not_authorized = 'NOT_AUTHORIZED'
    #: The configuration is managed by a different authority. For example `CUCM`.
    config_managed_by_different_authority = 'CONFIG_MANAGED_BY_DIFFERENT_AUTHORITY'


class DeviceConfigurationConfigurationKeySourcesConfiguredEditability(ApiModel):
    #: Whether or not the value is editable on this source.
    is_editable: Optional[bool] = None
    #: The reason the value is not editable on this source.
    reason: Optional[DeviceConfigurationConfigurationKeySourcesConfiguredEditabilityReason] = None


class DeviceConfigurationConfigurationKeySourcesConfigured(ApiModel):
    editability: Optional[DeviceConfigurationConfigurationKeySourcesConfiguredEditability] = None


class DeviceConfigurationConfigurationKeySources(ApiModel):
    default: Optional[DeviceConfigurationConfigurationKeySourcesDefault] = None
    configured: Optional[DeviceConfigurationConfigurationKeySourcesConfigured] = None


class DeviceConfigurationConfigurationKey(ApiModel):
    #: The source of the current value that is applied to the device.
    source: Optional[DeviceConfigurationConfigurationKeySource] = None
    sources: Optional[DeviceConfigurationConfigurationKeySources] = None
    #: `JSON Schema
    #: <http://json-schema.org/>`_ describing the data format of the configuration as specified by the device.
    value_space: Optional[dict] = None


class DeviceConfiguration(ApiModel):
    #: Key of the configuration.
    configuration_key: Optional[DeviceConfigurationConfigurationKey] = Field(alias='configuration_key', default=None)


class DeviceConfigurationCollectionResponse(ApiModel):
    #: ID of the device that the configurations are for.
    device_id: Optional[str] = None
    items: Optional[DeviceConfiguration] = None


class Op(str, Enum):
    #: Remove the configured value and revert back to the default from schema, if present.
    remove = 'remove'
    #: Set the configured value.
    replace = 'replace'


class DeviceConfigurationsApi(ApiChild, base='deviceConfigurations'):
    """
    Device Configurations
    
    The Device Configurations API allows developers to view and modify configurations on Webex Rooms devices, as well
    as other devices that use the configuration service.
    
    Viewing the list of all device configurations in an organization requires an administrator auth token with the
    `spark-admin:devices_read` scope. Adding, updating, or deleting configurations for devices in an organization
    requires an administrator auth token with both the `spark-admin:devices_write` and the `spark-admin:devices_read`
    scope.
    """

    def list_device_configurations_for_device(self, device_id: str,
                                              key: str = None) -> DeviceConfigurationCollectionResponse:
        """
        List Device Configurations for device

        Lists all device configurations associated with the given device ID. Administrators can list configurations for
        all devices within an organization.

        :param device_id: List device configurations by device ID.
        :type device_id: str
        :param key: This can optionally be used to filter configurations. Keys are composed of segments. It's possible
            to use absolute paths, wildcards or ranges.

        - **Absolute** gives only one configuration as a result. `Conference.MaxReceiveCallRate` for example gives the
        Conference `MaxReceiveCallRate` configuration.

        + **Wildcards** (\*) can specify multiple configurations with shared segments. `Audio.Ultrasound.*` for example
        will filter on all Audio Ultrasound configurations.

        - **Range**
        (`_number_]) can be used to filter numbered segments. `FacilityService.Service[1].Name` for instance only shows the first `FacilityService` Service Name configuration, `FacilityService.Service[*].Name` shows all, `FacilityService.Service[1..3].Name` shows the first three and `FacilityService.Service[2..n].Name` shows all starting at 2. Note that [RFC 3986 3.2.2
        <https://www.ietf.org/rfc/rfc3986.html#section-3.2.2>`_
        does not allow square brackets in urls outside the host, so to specify range in a configuration key you will
        need to encode them to %5B for [ and %5D for ].
        :type key: str
        :rtype: :class:`DeviceConfigurationCollectionResponse`
        """
        params = {}
        params['deviceId'] = device_id
        if key is not None:
            params['key'] = key
        url = self.ep()
        data = super().get(url, params=params)
        r = DeviceConfigurationCollectionResponse.model_validate(data)
        return r

    def update_device_configurations(self, device_id: str, op: Op = None,
                                     path: str = None) -> DeviceConfigurationCollectionResponse:
        """
        Update Device Configurations

        Edit configurations for the device specified by device ID.

        :param device_id: Update device configurations by device ID.
        :type device_id: str
        :param op: * `remove` - Remove the configured value and revert back to the default from schema, if present.
        :type op: Op
        :param path: Only paths ending in `/sources/configured/value` are supported.
        :type path: str
        :rtype: :class:`DeviceConfigurationCollectionResponse`
        """
        params = {}
        params['deviceId'] = device_id
        body = dict()
        if op is not None:
            body['op'] = enum_str(op)
        if path is not None:
            body['path'] = path
        url = self.ep()
        data = super().patch(url, params=params, json=body)
        r = DeviceConfigurationCollectionResponse.model_validate(data)
        return r
