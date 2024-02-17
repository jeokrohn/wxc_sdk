from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Floor', 'Location', 'WorkspaceLocationsApi']


class Location(ApiModel):
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9XT1JLU1BBQ0VfTE9DQVRJT04vM2E2ZmYzNzMtNjhhNy00NGU0LTkxZDYtYTI3NDYwZTBhYzVjIzUxOWY2N2E1LTlkOTktNGM2My04YTA5LWI5MTcxY2M2NmJkMQ==
    id: Optional[str] = None
    #: The ID to use for this location in the `/locations API
    #: <https://developer.webex.com/docs/api/v1/locations>`_
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzA2OWEzMDY2LTgwNjMtNDI0Zi05YmE0LTBhZDdhMmYxMzNjNQ
    location_id: Optional[str] = None
    #: A friendly name for the location.
    #: example: Cisco Barcelona
    display_name: Optional[str] = None
    #: The location address.
    #: example: Carrer de Pere IV, Barcelona, Spain
    address: Optional[str] = None
    #: The location country code (ISO 3166-1).
    #: example: ES
    country_code: Optional[str] = None
    #: The location city name.
    #: example: Barcelona
    city_name: Optional[str] = None
    #: The location latitude.
    #: example: 41
    latitude: Optional[int] = None
    #: The location longitude.
    #: example: 2
    longitude: Optional[int] = None
    #: Notes associated with the location.
    #: example: A note about the location
    notes: Optional[str] = None


class Floor(ApiModel):
    #: Unique identifier for the floor.
    #: example: xxx==
    id: Optional[str] = None
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9XT1JLU1BBQ0VfTE9DQVRJT04vM2E2ZmYzNzMtNjhhNy00NGU0LTkxZDYtYTI3NDYwZTBhYzVjIzUxOWY2N2E1LTlkOTktNGM2My04YTA5LWI5MTcxY2M2NmJkMQ==
    location_id: Optional[str] = None
    #: The floor number.
    #: example: -1
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class WorkspaceLocationsApi(ApiChild, base='workspaceLocations'):
    """
    Workspace Locations
    
    The Workspace Locations API is deprecated and will be decommissioned November
    30, 2024. Please use the `/locations API
    <https://developer.webex.com/docs/api/v1/locations>`_ for future
    projects, and use `locationId` instead of `workspaceLocationId` when
    interacting with device or workspace APIs.
    
    
    
    A `Workspace
    <https://developer.webex.com/docs/api/v1/workspaces>`_ Location is a physical location with a name, address, country, city, latitude and longitude.
    
    Viewing the list of locations in an organization requires an administrator auth token with the
    `spark-admin:workspace_locations_read` scope. Adding, updating, or deleting workspace locations in an organization
    requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.
    
    The Workspace Locations API can also be used by partner administrators acting as administrators of a different
    organization than their own. In those cases an `orgId` value must be supplied, as indicated in the reference
    documentation for the relevant endpoints.
    """

    def list_workspace_locations(self, display_name: str = None, address: str = None, country_code: str = None,
                                 city_name: str = None, org_id: str = None) -> list[Location]:
        """
        List Workspace Locations

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        List workspace locations. Use query parameters to filter the response. The `orgId` parameter can only be used
        by admin users of another
        organization (such as partners). The `displayName`, `address`, `countryCode` and `cityName` parameters are all
        optional.
        Requires an administrator auth token with the `spark-admin:workspace_locations_read` scope.

        :param display_name: Location display name.
        :type display_name: str
        :param address: Location address.
        :type address: str
        :param country_code: Location country code (ISO 3166-1).
        :type country_code: str
        :param city_name: Location city name.
        :type city_name: str
        :param org_id: List workspace locations in this organization. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :rtype: list[Location]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if display_name is not None:
            params['displayName'] = display_name
        if address is not None:
            params['address'] = address
        if country_code is not None:
            params['countryCode'] = country_code
        if city_name is not None:
            params['cityName'] = city_name
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Location]).validate_python(data['items'])
        return r

    def create_a_workspace_location(self, display_name: str, address: str, country_code: str, latitude: int,
                                    longitude: int, city_name: str = None, notes: str = None) -> Location:
        """
        Create a Workspace Location

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Create a location. The `cityName` and `notes` parameters are optional, and omitting them will result in the
        creation of a location without values for those attributes.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param display_name: A friendly name for the location.
        :type display_name: str
        :param address: The location address.
        :type address: str
        :param country_code: The location country code (ISO 3166-1).
        :type country_code: str
        :param latitude: The location latitude.
        :type latitude: int
        :param longitude: The location longitude.
        :type longitude: int
        :param city_name: The location city name.
        :type city_name: str
        :param notes: Notes associated with the location.
        :type notes: str
        :rtype: :class:`Location`
        """
        body = dict()
        body['displayName'] = display_name
        body['address'] = address
        body['countryCode'] = country_code
        if city_name is not None:
            body['cityName'] = city_name
        body['latitude'] = latitude
        body['longitude'] = longitude
        if notes is not None:
            body['notes'] = notes
        url = self.ep()
        data = super().post(url, json=body)
        r = Location.model_validate(data)
        return r

    def get_a_workspace_location_details(self, location_id: str) -> Location:
        """
        Get a Workspace Location Details

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Shows details for a location, by ID. Specify the location ID in the `locationId` parameter in the URI.
        Requires an administrator auth token with the `spark-admin:workspace_locations_read` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :rtype: :class:`Location`
        """
        url = self.ep(f'{location_id}')
        data = super().get(url)
        r = Location.model_validate(data)
        return r

    def update_a_workspace_location(self, location_id: str, display_name: str, address: str, country_code: str,
                                    latitude: int, longitude: int, id: str = None, city_name: str = None,
                                    notes: str = None) -> Location:
        """
        Update a Workspace Location

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Updates details for a location, by ID. Specify the location ID in the `locationId` parameter in the URI. The
        request should include all details for the location returned in a previous call to
        `Get Workspace Location Details
        <https://developer.webex.com/docs/api/v1/workspace-locations/get-a-workspace-location-details>`_. Omitting the optional `cityName` or `notes` fields will result in those fields
        no longer being defined for the location.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param display_name: A friendly name for the location.
        :type display_name: str
        :param address: The location address.
        :type address: str
        :param country_code: The location country code (ISO 3166-1).
        :type country_code: str
        :param latitude: The location latitude.
        :type latitude: int
        :param longitude: The location longitude.
        :type longitude: int
        :param id: Unique identifier for the location.
        :type id: str
        :param city_name: The location city name.
        :type city_name: str
        :param notes: Notes associated with the location.
        :type notes: str
        :rtype: :class:`Location`
        """
        body = dict()
        if id is not None:
            body['id'] = id
        body['displayName'] = display_name
        body['address'] = address
        body['countryCode'] = country_code
        if city_name is not None:
            body['cityName'] = city_name
        body['latitude'] = latitude
        body['longitude'] = longitude
        if notes is not None:
            body['notes'] = notes
        url = self.ep(f'{location_id}')
        data = super().put(url, json=body)
        r = Location.model_validate(data)
        return r

    def delete_a_workspace_location(self, location_id: str):
        """
        Delete a Workspace Location

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Deletes a location, by ID. The workspaces associated to that location will no longer have a location, but a new
        location can be reassigned to them.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :rtype: None
        """
        url = self.ep(f'{location_id}')
        super().delete(url)

    def list_workspace_location_floors(self, location_id: str) -> list[Floor]:
        """
        List Workspace Location Floors

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        List workspace location floors.
        Requires an administrator auth token with the `spark-admin:workspace_locations_read` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :rtype: list[Floor]
        """
        url = self.ep(f'{location_id}/floors')
        data = super().get(url)
        r = TypeAdapter(list[Floor]).validate_python(data['items'])
        return r

    def create_a_workspace_location_floor(self, location_id: str, floor_number: int,
                                          display_name: str = None) -> Floor:
        """
        Create a Workspace Location Floor

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Create a new floor in the given location. The `displayName` parameter is optional, and omitting it will result
        in the creation of a floor without that value set.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str
        :rtype: :class:`Floor`
        """
        body = dict()
        body['floorNumber'] = floor_number
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep(f'{location_id}/floors')
        data = super().post(url, json=body)
        r = Floor.model_validate(data)
        return r

    def get_a_workspace_location_floor_details(self, location_id: str, floor_id: str) -> Floor:
        """
        Get a Workspace Location Floor Details

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Shows details for a floor, by ID. Specify the floor ID in the `floorId` parameter in the URI.
        Requires an administrator auth token with the `spark-admin:workspace_locations_read` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :rtype: :class:`Floor`
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().get(url)
        r = Floor.model_validate(data)
        return r

    def update_a_workspace_location_floor(self, location_id: str, floor_id: str, floor_number: int,
                                          display_name: str = None) -> Floor:
        """
        Update a Workspace Location Floor

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Updates details for a floor, by ID. Specify the floor ID in the `floorId` parameter in the URI. Include all
        details for the floor returned by a previous call to `Get Workspace Location Floor Details
        <https://developer.webex.com/docs/api/v1/workspace-locations/get-a-workspace-location-details>`_. Omitting the
        optional `displayName` field will result in that field no longer being defined for the floor.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str
        :rtype: :class:`Floor`
        """
        body = dict()
        body['floorNumber'] = floor_number
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().put(url, json=body)
        r = Floor.model_validate(data)
        return r

    def delete_a_workspace_location_floor(self, location_id: str, floor_id: str):
        """
        Delete a Workspace Location Floor

        <div><Callout type="warning">The Workspace Locations API is deprecated and will be decommissioned November 30,
        2024. Please use the `/locations API
        <https://developer.webex.com/docs/api/v1/locations>`_ for future projects, and use `locationId` instead of `workspaceLocationId`
        when interacting with device or workspace APIs.</Callout></div>

        Deletes a floor, by ID.
        Requires an administrator auth token with the `spark-admin:workspace_locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :rtype: None
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        super().delete(url)
