from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum

from wxc_sdk.common import SetOrClear

__all__ = ['SettingsType', 'DeviceSettingsGroupTag', 'SettingsGroup', 'DynamicSettingsGroups', 'ValidationRule',
           'DeviceTag', 'DevicePutItem', 'ParentLevel', 'DeviceDynamicTag', 'DeviceDynamicSettings',
           'DevicesDynamicSettingsApi']


class SettingsType(str, Enum):
    tabs = 'TABS'
    groups = 'GROUPS'
    all = 'ALL'


class DeviceSettingsGroupTag(ApiModel):
    #: Array of tags associated with the settings group.
    tag_block: Optional[list[str]] = None


class SettingsGroup(ApiModel):
    #: Path of the settings group. Creates an easily navigable settings hierarchy.
    path: Optional[str] = None
    #: Friendly name of the settings group.
    friendly_name: Optional[str] = None
    #: Tab name associated with the settings group.
    tab: Optional[str] = None
    #: Family or model display name associated with the settings group.
    family_or_model_display_name: Optional[str] = None
    #: List of `tagBlock` objects associated with the settings group.
    tags: Optional[list[DeviceSettingsGroupTag]] = None


class DynamicSettingsGroups(ApiModel):
    #: Array of settings groups defining structure and association of tags.
    settings_groups: Optional[list[SettingsGroup]] = None
    #: Array of settings tabs names. Can be filtered using the `includeSettingsType` parameter.
    settings_tabs: Optional[list[str]] = None


class ValidationRule(ApiModel):
    #: The data type of the setting. Possible values are `string`, `integer`, `boolean`, `enum` , `password` or
    #: `network`.
    type: Optional[str] = None
    #: Possible values for `enum` or `boolean` types.
    values: Optional[list[str]] = None
    #: Minimum value for numeric types.
    min: Optional[int] = None
    #: Maximum value for numeric types.
    max_: Optional[int] = None
    #: Increment value for numeric types.
    increment: Optional[int] = None
    #: Regular expression pattern for string validation.
    regex: Optional[str] = None
    #: Maximum length for string values.
    max_length: Optional[int] = None
    #: Hint to display to users about validation requirements.
    validation_hint: Optional[str] = None


class DeviceTag(ApiModel):
    #: The family or model name of the device to which these settings apply.
    family_or_model_display_name: Optional[str] = None
    #: The unique identifier for the setting.
    tag: Optional[str] = None
    #: A user-friendly name for the setting. It helps to correlate the tag with the UI in settings groups.
    friendly_name: Optional[str] = None
    #: Explanatory text for the setting.
    tooltip: Optional[str] = None
    #: Alert message related to this setting, if applicable.
    alert: Optional[str] = None
    #: The levels at which this setting can be configured. When fetching tags or updating tags, the tag should be
    #: allowed at the level the request is made for.
    level: Optional[list[str]] = None
    validation_rule: Optional[ValidationRule] = None


class DevicePutItem(ApiModel):
    #: The unique identifier for the setting to be updated.
    tag: Optional[str] = None
    action: Optional[SetOrClear] = None
    #: The new value to set for the setting. This field is required when `action` is `SET` and ignored otherwise.
    value: Optional[str] = None


class ParentLevel(str, Enum):
    system_default = 'SYSTEM_DEFAULT'
    regional_default = 'REGIONAL_DEFAULT'
    organization = 'ORGANIZATION'
    location = 'LOCATION'


class DeviceDynamicTag(ApiModel):
    #: The `familyOrModelDisplayName` of the device.
    family_or_model_display_name: Optional[str] = None
    #: The unique identifier for the setting.
    tag: Optional[str] = None
    #: The current value of the setting at `ORGANIZATION` level. If the tag value is not set at the `ORGANIZATION`
    #: level, this field will not be included in the response.
    value: Optional[str] = None
    #: The value inherited from the immediate parent level above `ORGANIZATION`. It can be `SYSTEM_DEFAULT`,
    #: `REGIONAL_DEFAULT`, or `ORGANIZATION`, depending on which level the setting is actually configured at. If there
    #: is no parent level for this tag, this field will not be included in the response.
    parent_value: Optional[str] = None
    parent_level: Optional[ParentLevel] = None


class DeviceDynamicSettings(ApiModel):
    #: Array of device setting values matching the requested tags.
    tags: Optional[list[DeviceDynamicTag]] = None
    #: Timestamp of the last update to these settings.
    last_update_time: Optional[int] = None
    #: Flag indicating if an update to these settings is currently in progress.
    update_in_progress: Optional[bool] = None


class DevicesDynamicSettingsApi(ApiChild, base='telephony/config'):
    """
    Telephony devices API
    """

    def get_settings_groups(self, family_or_model_display_name: str = None,
                            include_settings_type: SettingsType = None,
                            org_id: str = None) -> DynamicSettingsGroups:
        """
        Get Settings Groups

        This API returns the `settingsGroups` that define the structure and association of tags for dynamic device
        settings.

        The `settingsGroups` are used to organize the tags into logical groups, making it easier to manage and
        configure dynamic device settings.

        :param family_or_model_display_name: Device family or model display name to filter the `settingsGroups`.
        :type family_or_model_display_name: str
        :param include_settings_type: To show groups or tabs or both. Query param is case insensitive. Default is
            `ALL`.
        :type include_settings_type: SettingsType
        :param org_id: Settings groups for devices in this organization.
        :type org_id: str
        :rtype: :class:`DynamicSettingsGroups`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if family_or_model_display_name is not None:
            params['familyOrModelDisplayName'] = family_or_model_display_name
        if include_settings_type is not None:
            params['includeSettingsType'] = enum_str(include_settings_type)
        url = self.ep('devices/dynamicSettings/settingsGroups')
        data = super().get(url, params=params)
        r = DynamicSettingsGroups.model_validate(data)
        return r

    def get_validation_schema(self, family_or_model_display_name: str = None, org_id: str = None) -> list[DeviceTag]:
        """
        Get Validation Schema

        This API returns the validation schema for `tags` of all or specific `familyOrModelDisplayName`.

        The schema is used to validate the `tag` for devices in the `Webex Calling` platform. The schema includes
        information about the required fields, data types, and validation rules for each setting.

        :param family_or_model_display_name: Device family or model display name to filter the schema.
        :type family_or_model_display_name: str
        :param org_id: Validation schema for devices in this organization.
        :type org_id: str
        :rtype: list[DeviceTag]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if family_or_model_display_name is not None:
            params['familyOrModelDisplayName'] = family_or_model_display_name
        url = self.ep('devices/dynamicSettings/validationSchema')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DeviceTag]).validate_python(data['tags'])
        return r

    def update_specified_settings_for_the_device(self, device_id: str, tags: list[DevicePutItem] = None,
                                                 org_id: str = None):
        """
        Update specified settings for the device.

        Modify dynamic settings for a specified device.

        This API updates device settings based on the specified `tags`. If the `tags` field is empty, the request has
        no effect.

        This requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param device_id: Device for which to update settings.
        :type device_id: str
        :param tags: Optional array of `tag` identifiers representing specific settings to update. If omitted or
            provided as an empty array, the request will have no effect.
        :type tags: list[DevicePutItem]
        :param org_id: Organization to which the device belongs.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if tags is not None:
            body['tags'] = TypeAdapter(list[DevicePutItem]).dump_python(tags, mode='json', by_alias=True,
                                                                        exclude_none=True)
        url = self.ep(f'devices/{device_id}/dynamicSettings')
        super().put(url, params=params, json=body)

    def get_customer_device_settings(self, family_or_model_display_name: str, tags: list[str] = None,
                                     org_id: str = None) -> DeviceDynamicSettings:
        """
        Get Customer Device Dynamic Settings

        Retrieve dynamic settings for specific device tags at customer level, allowing filters by
        `familyOrModelDisplayName` and `tag` identifier.

        This API lets you request the values of multiple `Device Settings` at once by specifying a list of
        `familyOrModelDisplayName` and tag combinations.

        This requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param family_or_model_display_name: The family or model name for the device. If no tag is specified, all tags
            related to `familyOrModelDisplayName` are returned.
        :type family_or_model_display_name: str
        :param tags: Optional array of device tag identifiers to request settings for. Each identifier must have a
            length between 1 and 64 characters.
        :type tags: list[str]
        :param org_id: List of device dynamic settings in this organization.
        :type org_id: str
        :rtype: :class:`CustomerDeviceDynamicSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        params['familyOrModelDisplayName'] = family_or_model_display_name
        body = dict()
        if tags is not None:
            body['tags'] = tags
        url = self.ep('lists/devices/dynamicSettings/actions/getSettings/invoke')
        data = super().post(url, params=params, json=body)
        r = DeviceDynamicSettings.model_validate(data)
        return r

    def get_device_settings(self, device_id: str, tags: list[str] = None,
                            org_id: str = None) -> DeviceDynamicSettings:
        """
        Get Device Dynamic Settings

        Retrieve settings for a specified device.

        This API retrieves device settings based on the specified `tags`; if the `tags` field is empty or missing, all
        settings for the device are returned.

        This requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Device for which to retrieve settings.
        :type device_id: str
        :param tags: Optional array of tag identifiers representing specific settings to fetch. If omitted or provided
            as an empty array, all settings for the device will be returned.
        :type tags: list[str]
        :param org_id: Organization to which the `device` belongs.
        :type org_id: str
        :rtype: :class:`DeviceDynamicSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if tags is not None:
            body['tags'] = tags
        url = self.ep(f'lists/devices/{device_id}/dynamicSettings/actions/getSettings/invoke')
        data = super().post(url, params=params, json=body)
        r = DeviceDynamicSettings.model_validate(data)
        return r

    def get_location_device_settings(self, location_id: str, family_or_model_display_name: str,
                                     tags: list[str] = None,
                                     org_id: str = None) -> DeviceDynamicSettings:
        """
        Get Location Device Dynamic Settings

        Retrieve dynamic settings for specific device tags at the specified location level, allowing filters by
        `familyOrModelDisplayName` and `tag` identifier.

        This API lets you request the values of multiple `Device Settings` at once by specifying a list of
        `familyOrModelDisplayName` and tag combinations for a specific location.

        This requires a full, device, or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier for the `location`.
        :type location_id: str
        :param family_or_model_display_name: The family or model name for the device. If no tag is specified, all tags
            related to `familyOrModelDisplayName` are returned.
        :type family_or_model_display_name: str
        :param tags: Optional array of device tag identifiers to request settings for. Each identifier must have a
            length between 1 and 64 characters.
        :type tags: list[str]
        :param org_id: Unique identifier for the `organization` to which this location belongs.
        :type org_id: str
        :rtype: :class:`DeviceDynamicSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        params['familyOrModelDisplayName'] = family_or_model_display_name
        body = dict()
        if tags is not None:
            body['tags'] = tags
        url = self.ep(f'lists/locations/{location_id}/devices/dynamicSettings/actions/getSettings/invoke')
        data = super().post(url, params=params, json=body)
        r = DeviceDynamicSettings.model_validate(data)
        return r
