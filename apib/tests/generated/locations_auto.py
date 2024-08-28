from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Floor', 'Location', 'LocationAddress', 'LocationsApi']


class LocationAddress(ApiModel):
    #: Address 1
    #: example: 123 Some St.
    address1: Optional[str] = None
    #: Address 2
    #: example: Suite 456
    address2: Optional[str] = None
    #: City
    #: example: Supercity
    city: Optional[str] = None
    #: State code
    #: example: Goodstate
    state: Optional[str] = None
    #: ZIP/Postal Code
    #: example: 12345
    postal_code: Optional[str] = None
    #: ISO-3166 2-Letter Country Code.
    #: example: US
    country: Optional[str] = None


class Location(ApiModel):
    #: A unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2M5N2VlMDQ5LTM1OWItNGM3OC04NDU0LTA1OGMyZWRlMjU2Mw
    id: Optional[str] = None
    #: The name of the location.
    #: example: Denver
    name: Optional[str] = None
    #: The ID of the organization to which this location belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: Time zone associated with this location.
    #: example: 'America/Chicago'
    time_zone: Optional[str] = None
    #: The address of the location.
    address: Optional[LocationAddress] = None
    #: Latitude
    #: example: 12.935784
    latitude: Optional[datetime] = None
    #: Longitude
    #: example: 77.697332
    longitude: Optional[datetime] = None
    #: Notes
    #: example: 123 Some St. Denver Location
    notes: Optional[str] = None


class Floor(ApiModel):
    #: Unique identifier for the floor.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL1dPUktTUEFDRV9MT0NBVElPTl9GTE9PUi83NDhkZDNmMS1iYmE5LTQxMDItODk5NC00M2IyOTM2MzNlNjY
    id: Optional[str] = None
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4NjczZDIwLWM0M2EtNDQ5Ni1iYWIxLTNiMjhhZGJjMjViYQ
    location_id: Optional[str] = None
    #: The floor number.
    #: example: -1
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class LocationsApi(ApiChild, base='locations'):
    """
    Locations
    
    Locations allow you to organize users and workspaces based on a physical location. You can configure both calling
    and workspace management functions into the same location. To enable a location for Webex Calling, use the
    `Enable a Location for Webex Calling
    <https://developer.webex.com/docs/api/v1/location-call-settings/enable-a-location-for-webex-calling>`_ API.
    You can also create and inspect locations in Webex Control Hub. See `Locations on Control Hub
    <https://help.webex.com/en-us/article/ajh6iy/Locations-in-Control-Hub>`_ for more information.
    """

    def list_locations(self, name: str = None, id: str = None, org_id: str = None,
                       **params) -> Generator[Location, None, None]:
        """
        List Locations

        List locations for an organization.

        * Use query parameters to filter the result set by location name, ID, or organization.

        * Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * Searching and viewing locations in your organization requires an administrator or location administrator auth
        token with any of the following scopes: `spark-admin:locations_read`, `spark-admin:people_read` or
        `spark-admin:device_read`.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param id: List locations by ID.
        :type id: str
        :param org_id: List locations in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Location` instances
        """
        if name is not None:
            params['name'] = name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Location, item_key='items', params=params)

    def get_location_details(self, location_id: str, org_id: str = None) -> Location:
        """
        Get Location Details

        Shows details for a location, by ID.

        * Specify the location ID in the `locationId` parameter in the URI.

        * Use query parameter `orgId` to filter the result set by organization(optional).

        * Searching and viewing location in your organization requires an administrator or location administrator auth
        token with any of the following scopes:

        * `spark-admin:locations_read`
        * `spark-admin:people_read`
        * `spark-admin:device_read`

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id: Get location common attributes for this organization.
        :type org_id: str
        :rtype: :class:`Location`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}')
        data = super().get(url, params=params)
        r = Location.model_validate(data)
        return r

    def create_a_location(self, name: str, time_zone: str, preferred_language: str, announcement_language: str,
                          address: LocationAddress, latitude: Union[str, datetime] = None, longitude: Union[str,
                          datetime] = None, notes: str = None, org_id: str = None) -> str:
        """
        Create a Location

        Create a new Location for a given organization. Only an admin in the organization can create a new Location.

        * Creating a location in your organization requires a full administrator auth token with a scope of
        `spark-admin:locations_write`.

        * Partners may specify `orgId` query parameter to create location in managed organization.

        * The following body parameters are required to create a new location:
        * `name`
        * `timeZone`
        * `preferredLanguage`
        * `address`
        * `announcementLanguage`.

        * `latitude`, `longitude` and `notes` are optional parameters to create a new location.

        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this `link
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_ for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param address: The address of the location.
        :type address: LocationAddress
        :param latitude: Latitude
        :type latitude: Union[str, datetime]
        :param longitude: Longitude
        :type longitude: Union[str, datetime]
        :param notes: Notes
        :type notes: str
        :param org_id: Create a location common attribute for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['timeZone'] = time_zone
        body['preferredLanguage'] = preferred_language
        body['announcementLanguage'] = announcement_language
        body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        if latitude is not None:
            body['latitude'] = latitude
        if longitude is not None:
            body['longitude'] = longitude
        if notes is not None:
            body['notes'] = notes
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def update_a_location(self, location_id: str, name: str = None, time_zone: str = None,
                          preferred_language: str = None, address: LocationAddress = None, org_id: str = None):
        """
        Update a Location

        Update details for a location, by ID.

        * Updating a location in your organization requires a full administrator or location administrator auth token
        with a scope of `spark-admin:locations_write`.

        * Specify the location ID in the `locationId` parameter in the URI.

        * Partners may specify `orgId` query parameter to update location in managed organization.

        :param location_id: Update location common attributes for this location.
        :type location_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this `link
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_ for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param address: The address of the location.
        :type address: LocationAddress
        :param org_id: Update location common attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if preferred_language is not None:
            body['preferredLanguage'] = preferred_language
        if address is not None:
            body['address'] = address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}')
        super().put(url, params=params, json=body)

    def list_location_floors(self, location_id: str) -> list[Floor]:
        """
        List location floors.
        Requires an administrator auth token with the `spark-admin:locations_read` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :rtype: list[Floor]
        """
        url = self.ep(f'{location_id}/floors')
        data = super().get(url)
        r = TypeAdapter(list[Floor]).validate_python(data['items'])
        return r

    def create_a_location_floor(self, location_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Create a Location Floor

        Create a new floor in the given location. The `displayName` parameter is optional, and omitting it will result
        in the creation of a floor without that value set.
        Requires an administrator auth token with the `spark-admin:locations_write` scope.

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

    def get_location_floor_details(self, location_id: str, floor_id: str) -> Floor:
        """
        Get Location Floor Details

        Shows details for a floor, by ID. Specify the floor ID in the `floorId` parameter in the URI.
        Requires an administrator auth token with the `spark-admin:locations_read` scope.

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

    def update_a_location_floor(self, location_id: str, floor_id: str, floor_number: int,
                                display_name: str = None) -> Floor:
        """
        Update a Location Floor

        Updates details for a floor, by ID. Specify the floor ID in the `floorId` parameter in the URI. Include all
        details for the floor returned by a previous call to `Get Location Floor Details
        <https://developer.webex.com/docs/api/v1/locations/get-location-floor-details>`_. Omitting the optional
        `displayName` field will result in that field no longer being defined for the floor.
        Requires an administrator auth token with the `spark-admin:locations_write` scope.

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

    def delete_a_location_floor(self, location_id: str, floor_id: str):
        """
        Delete a Location Floor

        Deletes a floor, by ID.
        Requires an administrator auth token with the `spark-admin:locations_write` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :rtype: None
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        super().delete(url)
