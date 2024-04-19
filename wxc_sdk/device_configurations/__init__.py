from typing import Literal, Any, Optional, NamedTuple, List

from wxc_sdk.api_child import ApiChild

__all__ = ['DeviceConfigurationsApi', 'DeviceConfiguration', 'DeviceConfigurationSourceEditability',
           'DeviceConfigurationSources', 'DeviceConfigurationSource', 'DeviceConfigurationResponse',
           'DeviceConfigurationOperation']

from wxc_sdk.base import ApiModel


class DeviceConfigurationSourceEditability(ApiModel):
    #: Whether or not the value is editable on this source (always false for default).
    is_editable: bool
    #: The reason value is not editable on this source (always FACTORY_DEFAULT for default).
    #: The reason the value is not editable on this source.
    #: * NOT_AUTHORIZED - User is not authorized to edit any values.
    #: * CONFIG_MANAGED_BY_DIFFERENT_AUTHORITY - The configuration is managed by a different authority. For example
    #: CUCM.
    reason: Optional[str] = None


class DeviceConfigurationSource(ApiModel):
    value: Any
    editability: DeviceConfigurationSourceEditability
    level: str
    enforced: Optional[bool] = None


class DeviceConfigurationSources(ApiModel):
    default: DeviceConfigurationSource
    configured: DeviceConfigurationSource


class DeviceConfiguration(ApiModel):
    value: Optional[Any] = None
    #: The source of the current value that is applied to the device.
    source: Literal['default', 'configured']
    sources: DeviceConfigurationSources
    #: JSON Schema describing the data format of the configuration as specified by the device.
    value_space: Any


class DeviceConfigurationResponse(ApiModel):
    #: ID of the device that the configurations are for.
    device_id: str
    items: dict[str, DeviceConfiguration]


class DeviceConfigurationOperation(NamedTuple):
    #: remove - Remove the configured value and revert back to the default from schema, if present.
    #: replace - Set the configured value.
    op: Literal['remove', 'replace']
    #: device configuration key
    key: str
    #: value, only required for 'replace'
    value: Optional[Any] = None

    def for_update(self):
        """

        :meta private:
        """
        r = {'op': self.op,
             'path': f'{self.key}/sources/configured/value'}
        if self.value is not None:
            r['value'] = self.value
        return r


class DeviceConfigurationsApi(ApiChild, base='deviceConfigurations'):
    """
    The Device Configurations API allows developers to view and modify configurations on Webex Rooms devices, as well as
    other devices that use the configuration service.

    Viewing the list of all device configurations in an organization requires an administrator auth token with the
    spark-admin:devices_read scope. Adding, updating, or deleting configurations for devices in an organization requires
    an administrator auth token with both the spark-admin:devices_write and the spark-admin:devices_read scope.
    """

    def list(self, device_id: str, key: str = None) -> DeviceConfigurationResponse:
        """
        Lists all device configurations associated with the given device ID. Administrators can list configurations
        for all devices within an organization.

        :param device_id: List device configurations by device ID.
        :type device_id: str
        :param key: This can optionally be used to filter configurations. Keys are composed of segments. It's
            possible to use absolute paths, wildcards or ranges.

            Absolute gives only one configuration as a result. Conference.MaxReceiveCallRate for example gives the
            ConferenceMaxReceiveCallRate configuration.

            Wildcards (*) can specify multiple configurations with shared segments. Audio.Ultrasound.* for example
            will filter on all Audio Ultrasound configurations.

            Range ([number]) can be used to filter numbered segments. FacilityService.Service[1].Name for instance
            only shows the first FacilityService Service Name configuration, FacilityService.Service[*].Name shows all,
            FacilityService.Service[1..3].Name shows the first three and FacilityService.Service[2..n].Name shows all
            starting at 2.
        :type key: str

        :return: device configurations
        """
        params = key and {'key': key} or dict()
        params['deviceId'] = device_id
        data = self.get(self.ep(), params=params)
        return DeviceConfigurationResponse.model_validate(data)

    def update(self, device_id: str, operations: List[DeviceConfigurationOperation]) -> DeviceConfigurationResponse:
        """
        Update Device Configurations

        :param device_id: Update device configurations by device ID.
        :param operations: list if operations to apply
        """
        body = [op.for_update() for op in operations]
        data = self.patch(self.ep(), json=body, content_type='application/json-patch+json',
                          params={'deviceId': device_id})
        return DeviceConfigurationResponse.model_validate(data)
