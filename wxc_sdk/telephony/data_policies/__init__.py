from __future__ import annotations

import builtins
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['CustomerDataPolicies', 'DataPolicyRegion', 'DataPoliciesApi', 'LocationDataPolicies']


class CustomerDataPolicies(ApiModel):
    #: (ISO 3166-1 alpha-2) Country Code configured as the storage region for the data policy of the Organization.
    org_data_region: Optional[str] = None
    #: If `true`, the storage region for the data policy of the Organization can be modified.
    allow_edit_enabled: Optional[bool] = None


class DataPolicyRegion(ApiModel):
    #: (ISO 3166-1 alpha-2) Country Code.
    code: Optional[str] = None
    #: Name of the country corresponding to the (ISO 3166-1 alpha-2) Country Code.
    name: Optional[str] = None
    #: Indicates whether voicemail storage restriction is enabled for this region.
    is_voicemail_storage_restriction_enabled: Optional[bool] = None


class LocationDataPolicies(ApiModel):
    #: (ISO 3166-1 alpha-2) Country Code indicating the data policy region configured for the organization to which the
    #: location belongs to.
    org_data_region: Optional[str] = None
    #: (ISO 3166-1 alpha-2) Country Code indicating the data policy region configured for the location.
    location_data_region: Optional[str] = None
    #: Indicates whether the location is configured to use configuration same as the Organization's configuration for
    #: data (storage) policy region settings.
    use_org_data_region_enabled: Optional[bool] = None
    #: If `true`, the storage region for the data policy of the Location can be modified.
    allow_edit_enabled: Optional[bool] = None


class DataPoliciesApi(ApiChild, base='telephony/config'):
    """
    Features Data Policies

    The APIs allow a person to read or modify settings related to data (storage) policy region for an organization or
    organization's location.

    Viewing settings requires a user auth token with a scope of `spark-admin:telephony_config_read`.

    Configuring settings requires a user auth token with a scope of `spark-admin:telephony_config_write`.
    """

    def read_data_policy_settings(self, org_id: str = None) -> CustomerDataPolicies:
        """
        Get the Data (Storage) Policy Settings for the Organization

        Retrieve the settings for data (storage) policy region of the organization.

        Data policies allow administrators to configure the storage region for organization data at the organization or
        location level.

        Retrieving data policy settings requires a user auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve data policy settings from this organization.
        :type org_id: str
        :rtype: :class:`CustomerDataPolicies`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('dataPolicies')
        data = super().get(url, params=params)
        r = CustomerDataPolicies.model_validate(data)
        return r

    def modify_data_policy_settings(self, org_data_region: str = None, org_id: str = None) -> None:
        """
        Update the Data (Storage) Policy Settings for the Organization

        Modify the configurations for data (storage) policy region of the organization.

        Data policies allow administrators to configure the storage region for organization data at the organization or
        location level.

        Configuring data policy settings requires a user auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param org_data_region: (ISO 3166-1 alpha-2) Country Code to be configured as the storage region for the data
            policy of the Organization.
        :type org_data_region: str
        :param org_id: Modify data policy settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if org_data_region is not None:
            body['orgDataRegion'] = org_data_region
        url = self.ep('dataPolicies')
        super().put(url, params=params, json=body)

    def get_available_data_policy_regions(self, org_id: str = None) -> builtins.list[DataPolicyRegion]:
        """
        Get All the Storage Regions Available for Configuring as Data Policy Region

        Retrieve all the storage regions available for configuring data (storage) policy of an organization or
        organization's location.

        Data policies allow administrators to configure the storage region for organization data at the organization or
        location level.

        Retrieving available data policy regions requires a user auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve available data policy regions for this organization.
        :type org_id: str
        :rtype: list[DataPolicyRegion]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('dataPolicies/regions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DataPolicyRegion]).validate_python(data['regions'])
        return r

    def get_location_data_policy_settings(self, location_id: str, org_id: str = None) -> LocationDataPolicies:
        """
        Get the Data (Storage) Policy Settings for the Organization's Location

        Retrieve the settings for data (storage) policy region of the organization's location.

        Data policies allow administrators to configure the storage region for organization data at the organization or
        location level.

        Retrieving location data policy settings requires a user auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Fetch the data policy for this location.
        :type location_id: str
        :param org_id: Retrieve location data policy settings from this organization.
        :type org_id: str
        :rtype: :class:`LocationDataPolicies`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dataPolicies')
        data = super().get(url, params=params)
        r = LocationDataPolicies.model_validate(data)
        return r

    def modify_location_data_policy_settings(
        self,
        location_id: str,
        location_data_region: str = None,
        use_org_data_region_enabled: bool = None,
        org_id: str = None,
    ) -> None:
        """
        Update the Data (Storage) Policy Settings for the Organization's Location

        Modify the configurations for data (storage) policy region of the organization's location.

        Data policies allow administrators to configure the storage region for organization data at the organization or
        location level.

        Configuring location data policy settings requires a user auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Modify the data policy for this location.
        :type location_id: str
        :param location_data_region: (ISO 3166-1 alpha-2) Country Code to be configured as the data policy region for
            the location.
        :type location_data_region: str
        :param use_org_data_region_enabled: Whether location's data (storage) policy region to be used same as the one
            configured at the Organization's level.
        :type use_org_data_region_enabled: bool
        :param org_id: Modify location data policy settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if location_data_region is not None:
            body['locationDataRegion'] = location_data_region
        if use_org_data_region_enabled is not None:
            body['useOrgDataRegionEnabled'] = use_org_data_region_enabled
        url = self.ep(f'locations/{location_id}/dataPolicies')
        super().put(url, params=params, json=body)
