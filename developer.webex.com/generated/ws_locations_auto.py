from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateWorkspaceLocationBody', 'CreateWorkspaceLocationFloorBody', 'Floor',
           'ListWorkspaceLocationFloorsResponse', 'ListWorkspaceLocationsResponse', 'Location',
           'WorkspaceLocationsApi']


class CreateWorkspaceLocationBody(ApiModel):
    #: A friendly name for the location.
    display_name: Optional[str]
    #: The location address.
    address: Optional[str]
    #: The location country code (ISO 3166-1).
    country_code: Optional[str]
    #: The location city name.
    city_name: Optional[str]
    #: The location latitude.
    latitude: Optional[int]
    #: The location longitude.
    longitude: Optional[int]
    #: Notes associated with the location.
    notes: Optional[str]


class Location(CreateWorkspaceLocationBody):
    #: Unique identifier for the location.
    id: Optional[str]
    #: Unique identifier for the location org ID.
    org_id: Optional[str]


class CreateWorkspaceLocationFloorBody(ApiModel):
    #: The floor number.
    floor_number: Optional[int]
    #: The floor display name.
    display_name: Optional[str]


class Floor(CreateWorkspaceLocationFloorBody):
    #: Unique identifier for the location.
    id: Optional[str]
    #: Unique identifier for the location org ID.
    location_id: Optional[str]


class ListWorkspaceLocationsResponse(ApiModel):
    #: An array of location objects.
    items: Optional[list[Location]]


class UpdateWorkspaceLocationBody(CreateWorkspaceLocationBody):
    #: Unique identifier for the location.
    id: Optional[str]


class ListWorkspaceLocationFloorsResponse(ApiModel):
    #: An array of floor objects.
    items: Optional[list[Floor]]


class WorkspaceLocationsApi(ApiChild, base='workspaceLocations'):
    """
    A Workspace Location is a physical location with a name, address, country, city, latitude and longitude.
    Viewing the list of locations in an organization requires an administrator auth token with the
    spark-admin:workspace_locations_read scope. Adding, updating, or deleting workspace locations in an organization
    requires an administrator auth token with the spark-admin:workspace_locations_write scope.
    The Workspace Locations API can also be used by partner administrators acting as administrators of a different
    organization than their own. In those cases an orgId value must be supplied, as indicated in the reference
    documentation for the relevant endpoints.
    """

    def list_locations(self, display_name: str = None, address: str = None, country_code: str = None, city_name: str = None) -> list[Location]:
        """
        List workspace locations.

        :param display_name: Location display name.
        :type display_name: str
        :param address: Location address.
        :type address: str
        :param country_code: Location country code (ISO 3166-1).
        :type country_code: str
        :param city_name: Location city name.
        :type city_name: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/list-workspace-locations
        """
        params = {}
        if display_name is not None:
            params['displayName'] = display_name
        if address is not None:
            params['address'] = address
        if country_code is not None:
            params['countryCode'] = country_code
        if city_name is not None:
            params['cityName'] = city_name
        url = self.ep()
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Location], data["items"])

    def create_location(self, display_name: str, address: str, country_code: str, latitude: int, longitude: int, city_name: str = None, notes: str = None) -> Location:
        """
        Create a location. The cityName and notes parameters are optional, and omitting them will result in the
        creation of a location without values for those attributes.

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

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/create-a-workspace-location
        """
        body = CreateWorkspaceLocationBody()
        if display_name is not None:
            body.display_name = display_name
        if address is not None:
            body.address = address
        if country_code is not None:
            body.country_code = country_code
        if latitude is not None:
            body.latitude = latitude
        if longitude is not None:
            body.longitude = longitude
        if city_name is not None:
            body.city_name = city_name
        if notes is not None:
            body.notes = notes
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Location.parse_obj(data)

    def location_details(self, location_id: str) -> Location:
        """
        Shows details for a location, by ID. Specify the location ID in the locationId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/get-a-workspace-location-details
        """
        url = self.ep(f'{location_id}')
        data = super().get(url=url)
        return Location.parse_obj(data)

    def update_location(self, location_id: str, display_name: str, address: str, country_code: str, latitude: int, longitude: int, city_name: str = None, notes: str = None, id: str = None) -> Location:
        """
        Updates details for a location, by ID. Specify the location ID in the locationId parameter in the URI. The
        request should include all details for the location returned in a previous call to Get Workspace Location
        Details. Omitting the optional cityName or notes fields will result in those fields no longer being defined for
        the location.

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
        :param city_name: The location city name.
        :type city_name: str
        :param notes: Notes associated with the location.
        :type notes: str
        :param id: Unique identifier for the location.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/update-a-workspace-location
        """
        body = UpdateWorkspaceLocationBody()
        if display_name is not None:
            body.display_name = display_name
        if address is not None:
            body.address = address
        if country_code is not None:
            body.country_code = country_code
        if latitude is not None:
            body.latitude = latitude
        if longitude is not None:
            body.longitude = longitude
        if city_name is not None:
            body.city_name = city_name
        if notes is not None:
            body.notes = notes
        if id is not None:
            body.id = id
        url = self.ep(f'{location_id}')
        data = super().put(url=url, data=body.json())
        return Location.parse_obj(data)

    def delete_location(self, location_id: str):
        """
        Deletes a location, by ID. The workspaces associated to that location will no longer have a location, but a new
        location can be reassigned to them.

        :param location_id: A unique identifier for the location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/delete-a-workspace-location
        """
        url = self.ep(f'{location_id}')
        super().delete(url=url)
        return

    def list_location_floors(self, location_id: str) -> list[Floor]:
        """
        List workspace location floors.

        :param location_id: A unique identifier for the location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/list-workspace-location-floors
        """
        url = self.ep(f'{location_id}/floors')
        data = super().get(url=url)
        return parse_obj_as(list[Floor], data["items"])

    def create_location_floor(self, location_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Create a new floor in the given location. The displayName parameter is optional, and omitting it will result in
        the creation of a floor without that value set.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/create-a-workspace-location-floor
        """
        body = CreateWorkspaceLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors')
        data = super().post(url=url, data=body.json())
        return Floor.parse_obj(data)

    def location_floor_details(self, location_id: str, floor_id: str) -> Floor:
        """
        Shows details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/get-a-workspace-location-floor-details
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().get(url=url)
        return Floor.parse_obj(data)

    def update_location_floor(self, location_id: str, floor_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all
        details for the floor returned by a previous call to Get Workspace Location Floor Details. Omitting the
        optional displayName field will result in that field no longer being defined for the floor.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/update-a-workspace-location-floor
        """
        body = CreateWorkspaceLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().put(url=url, data=body.json())
        return Floor.parse_obj(data)

    def delete_location_floor(self, location_id: str, floor_id: str):
        """
        Deletes a floor, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspace-locations/delete-a-workspace-location-floor
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        super().delete(url=url)
        return
