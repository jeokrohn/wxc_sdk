"""
A Workspace Location is a physical location with a name, address, country, city, latitude and longitude.

Viewing the list of locations in an organization requires an administrator auth token with
the spark-admin:workspace_locations_read scope. Adding, updating, or deleting workspace locations in an organization
requires an administrator auth token with the spark-admin:workspace_locations_write scope.

The Workspace Locations API can also be used by partner administrators acting as administrators of a different
organization than their own. In those cases an orgId value must be supplied, as indicated in the reference
documentation for the relevant endpoints.
"""

__all__ = ['WorkspaceLocationApi', 'WorkspaceLocationFloorApi', 'WorkspaceLocation', 'WorkspaceLocationFloor']

from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from ..api_child import ApiChild
from ..base import to_camel, ApiModel
from ..rest import RestSession


class WorkspaceLocation(ApiModel):
    #: Unique identifier for the location.
    id: str
    #: A friendly name for the location.
    display_name: str
    #: The location address.
    address: str
    #: The location country code (ISO 3166-1).
    country_code: str
    #: The location city name.
    city_name: str
    #: The location longitude.
    longitude: float
    #: The location latitude.
    latitude: float
    #: Notes associated to the location.
    notes: Optional[str]


class WorkspaceLocationFloor(ApiModel):
    id: str
    location_id: str
    floor_number: int
    display_name: str


class WorkspaceLocationFloorApi(ApiChild, base='workspaceLocations'):
    # noinspection PyMethodOverriding
    def ep(self, location_id: str, floor_id: str = None):
        path = f'{location_id}/floors'
        if floor_id:
            path = f'{path}/{floor_id}'
        return super().ep(path=path)

    def list(self, location_id: str, org_id: str = None) -> Generator[WorkspaceLocationFloor, None, None]:
        """

        :param location_id:
        :param org_id:
        :return:
        """
        url = self.ep(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return self.session.follow_pagination(url=url, model=WorkspaceLocationFloor, params=params, item_key='items')

    def create(self, location_id: str, floor_number: int, display_name: str = None,
               org_id: str = None) -> WorkspaceLocationFloor:
        """
        Create a Workspace Location Floor

        Create a new floor in the given location. The displayName parameter is optional, and omitting it will result
        in the creation of a floor without that value set.

        :param location_id: A unique identifier for the location.
        :param floor_number:
        :param display_name:
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: new workspace location floor
        :rtype: WorkspaceLocationFloor
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'location_id', 'org_id'} and v is not None}
        url = self.ep(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = self.post(url=url, params=params, json=body)
        return WorkspaceLocationFloor.parse_obj(data)

    def details(self, location_id: str, floor_id: str, org_id: str = None) -> WorkspaceLocationFloor:
        """
        Get a Workspace Location Floor Details

        Shows details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param org_id:
        :type org_id: str
        :return: workspace location floor details
        :rtype: WorkspaceLocationFloor
        """
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return WorkspaceLocationFloor.parse_obj(data)

    def update(self, location_id: str, floor_id: str, settings: WorkspaceLocationFloor,
               org_id: str = None) -> WorkspaceLocationFloor:
        """
        Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all
        details for the floor that are present in a Get Workspace Location Floor Details. Not including the optional
        displayName field will result in the field no longer being defined for the floor.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param settings: new settings
        :type settings: WorkspaceLocationFloor
        :param org_id:
        :type org_id: str
        :return: updated workspace location floor
        """
        data = settings.json(exclude_none=True, exclude_unset=True, exclude={'id', 'location_id'})
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        data = self.put(url=url, data=data, params=params)
        return WorkspaceLocationFloor.parse_obj(data)

    def delete(self, location_id: str, floor_id: str, org_id: str = None):
        """
        Delete a Workspace Location Floor
        Deletes a floor, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param org_id:
        :type org_id: str
        """
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        super().delete(url=url, params=params)


@dataclass(init=False)
class WorkspaceLocationApi(ApiChild, base='workspaceLocations'):
    #: Workspace location floor API :class:`WorkspaceLocationFloorApi`
    floors: WorkspaceLocationFloorApi

    def __init__(self, *, session: RestSession, base: str = None):
        super().__init__(session=session, base=base)
        self.floors = WorkspaceLocationFloorApi(session=session)

    def ep(self, location_id: str = None):
        return super().ep(path=location_id)

    def list(self, display_name: str = None, address: str = None, country_code: str = None, city_name: str = None,
             org_id: str = None, **params) -> Generator[WorkspaceLocation, None, None]:
        """
        List workspace locations

        :param display_name: Location display name.
        :type display_name: str
        :param address: Location address
        :type address: str
        :param country_code: Location country code (ISO 3166-1).
        :type country_code: str
        :param city_name: Location city name.
        :type city_name: str
        :param org_id: Organization id
        :type org_id: str
        :param params: addtl. parameters
        :return: generator of :class:`WorkspaceLocation` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=WorkspaceLocation, params=params, item_key='items')

    def create(self, display_name: str, address: str, country_code: str, latitude: float, longitude: float,
               city_name: str = None, notes: str = None, org_id: str = None) -> WorkspaceLocation:
        """
        Create a location. The cityName and notes parameters are optional, and omitting them will result in the
        creation of a location without these values set.

        :param display_name: A friendly name for the location.
        :param address: The location address.
        :param country_code: The location country code (ISO 3166-1).
        :param latitude: The location latitude.
        :param longitude: The location longitude.
        :param city_name: The location city name.
        :param notes: Notes associated to the location.
        :param org_id:
        :return: created workspace location
        :rtype: WorkspaceLocation
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = self.post(url=url, json=body, params=params)
        return WorkspaceLocation.parse_obj(data)

    def details(self, location_id: str, org_id: str = None) -> WorkspaceLocation:
        """
        Get a Workspace Location Details
        Shows details for a location, by ID. Specify the location ID in the locationId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: Workspace location details
        :rtype: WorkspaceLocation
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        data = self.get(url=url, params=params)
        return WorkspaceLocation.parse_obj(data)

    def update(self, location_id: str, settings: WorkspaceLocation, org_id: str = None):
        """
        Update a Workspace Location
        Updates details for a location, by ID. Specify the location ID in the locationId parameter in the URI.
        Include all details for the location that are present in a Get Workspace Location Details. Not including the
        optional cityName or notes fields (setting them to None) will result in the fields no longer being defined for
        the location.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param settings: new settings
        :type settings: WorkspaceLocation
        :param org_id:
        :type org_id: str
        :return: updated workspace location
        :rtype: WorkspaceLocation
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        body = settings.json(exclude_none=True, exclude_unset=True, exclude={'id'})
        data = self.put(url=url, data=body, params=params)
        return WorkspaceLocation.parse_obj(data)

    def delete(self, location_id: str, org_id: str = None):
        """
        Delete a Workspace Location
        Deletes a location, by ID. The workspaces associated to that location will no longer have a location, but a new
        location can be reassigned to them.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        super().delete(url=url, params=params)
