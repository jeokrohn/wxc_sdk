"""
Locations

Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub may be
used to define new locations.

Searching and viewing locations in your organization requires an administrator auth token with the
spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_writescope
combinations.
"""
from collections.abc import Generator
from typing import Optional, List

from pydantic import Field, TypeAdapter

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, webex_id_to_uuid

__all__ = ['LocationAddress', 'Location', 'Floor', 'LocationsApi']


class LocationAddress(ApiModel):
    #: Address 1 of the location.
    address1: Optional[str] = None
    #: Address 2 of the location.
    address2: Optional[str] = None
    #: City of the location.
    city: Optional[str] = None
    #: State code of the location.
    state: Optional[str] = None
    #: Postal code of the location.
    postal_code: Optional[str] = None
    #: ISO-3166 2-Letter country code of the location.
    country: Optional[str] = None


class Location(ApiModel):
    """
    Webex location
    """
    #: A unique identifier for the location.
    location_id: Optional[str] = Field(alias='id', default=None)
    #: The name of the location.
    name: Optional[str] = None
    #: The ID of the organization to which this location belongs.
    org_id: Optional[str] = None
    #: The address of the location, :class:`LocationAddress`
    address: Optional[LocationAddress] = None
    #: Time zone associated with this location. Refer to this link (
    #: https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone)
    #: for the format.
    time_zone: Optional[str] = None
    #: Default email language.
    preferred_language: Optional[str] = None
    #: Location's phone announcement language. This attribute is required when enabling a location for Webex Calling
    announcement_language: Optional[str] = None
    #: Latitude
    latitude: Optional[float] = None
    #: Longitude
    longitude: Optional[float] = None
    #: Notes
    notes: Optional[str] = None

    def update(self) -> dict:
        """
        get data for update call

        :meta private:
        """
        return self.model_dump(mode='json', exclude_unset=True, exclude_none=False, by_alias=True,
                               exclude={'location_id', 'org_id'})

    @property
    def location_id_uuid(self) -> str:
        """
        location id as UUID
        """
        return webex_id_to_uuid(self.location_id)

    @property
    def org_id_uuid(self) -> str:
        """
        org id as UUID
        """
        return webex_id_to_uuid(self.org_id)


class Floor(ApiModel):
    #: Unique identifier for the floor.
    id: Optional[str] = None
    #: Unique identifier for the location.
    location_id: Optional[str] = None
    #: The floor number.
    floor_number: Optional[int] = None
    #: The floor display name.
    display_name: Optional[str] = None

    def update(self) -> dict:
        """
        date for update

        :meta private:
        """
        return self.model_dump(mode='json', exclude_none=True, by_alias=True, exclude={'id', 'location_id'})


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

    def list(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> Generator[Location, None, None]:
        """
        List Locations

        List locations for an organization.

            * Use query parameters to filter the result set by location name, ID, or organization.
            * Long result sets will be split into `pages <https://developer.webex.com/docs/basics#pagination>`_.
            * Searching and viewing locations in your organization requires an administrator or location administrator auth
              token with any of the following scopes: `spark-admin:locations_read`, `spark-admin:people_read` or
              `spark-admin:device_read`.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param location_id: List locations by ID.
        :type location_id: str
        :param org_id: List locations in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Location` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if location_id is not None:
            params.pop('locationId')
            params['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Location, params=params)

    def by_name(self, name: str, org_id: str = None) -> Optional[Location]:
        """
        Get a location by name

        :param name: name of the location to search
        :type name: str
        :param org_id: search in list of locations  in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: locations
        :rtype: Location
        """
        return next((location for location in self.list(name=name, org_id=org_id)
                     if location.name == name), None)

    def details(self, location_id: str, org_id: str = None) -> Location:
        """
        Get Location Details

        Shows details for a location, by ID.

        Specify the location ID in the `locationId` parameter in the URI.

        Use query parameter `orgId` to filter the result set by organization(optional).

        Searching and viewing location in your organization requires an administrator or location administrator auth
        token with any of the following scopes:

            * `spark-admin:locations_read`
            * `spark-admin:people_read`
            * `spark-admin:device_read`

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id: Get location common attributes for this organization.
        :type org_id: str

        :return: location details
        :rtype: :class:`Location`
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(location_id)
        return Location.model_validate(self.get(ep, params=params))

    def create(self, name: str, time_zone: str, preferred_language: str, announcement_language: str, address1: str,
               city: str, state: str, postal_code: str, country: str, address2: str = None, latitude: str = None,
               longitude: str = None, notes: str = None, org_id: str = None) -> str:
        """
        Create a Location

        Create a new Location for a given organization. Only an admin in the organization can create a new Location.

        Creating a location in your organization requires a full administrator auth token with a scope of
        `spark-admin:locations_write`.

        Partners may specify `orgId` query parameter to create location in managed organization.

        The following body parameters are required to create a new location:

            * `name`
            * `timeZone`
            * `preferredLanguage`
            * `address`
            * `announcementLanguage`.

        `latitude`, `longitude` and `notes` are optional parameters to create a new location.

        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param address1: Address 1
        :type address1: str
        :param address2: Address 2
        :type address2: str
        :param city: City
        :type city: str
        :param state: State Code
        :type state: str
        :param postal_code: Postal Code
        :type postal_code: str
        :param country: ISO-3166 2-Letter Country Code.
        :type country: str
        :param org_id: Create a location common attribute for this organization.
        :param latitude: Latitude
        :type latitude: str
        :param longitude: Longitude
        :type longitude: str
        :param notes: Notes
        :type notes: str
        :type org_id: str
        :return: ID of new location
        :rtype: str
        """
        body = {}
        address = {}
        for p, v in list(locals().items()):
            if p in {'address', 'body', 'self'} or v is None:
                continue
            p = to_camel(p)
            if p in {'address1', 'address2', 'city', 'state', 'postalCode', 'country'}:
                # these are actually address parameters
                address[p] = v
            else:
                body[p] = v
        body['address'] = address
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = self.post(url=url, json=body, params=params)
        # TODO: doc issue, looks like this endpoint returns location details, but the doc only mentions "id"
        return data['id']

    def update(self, location_id: str, settings: Location, org_id: str = None):
        """
        Update details for a location, by ID.

        Specify the location ID in the locationId parameter in the URI. Only an admin can update a location details.

        Updating a location in your organization requires an administrator auth token with
        the spark-admin:locations_write.

        :param location_id: Update location common attributes for this location.
        :type location_id: str
        :param settings: new settings for the org:
        :type settings: :class:`Location`
        :param org_id: Update location common attributes for this organization
        :type org_id: str
        """
        settings_copy = settings.model_copy(deep=True)
        if settings_copy.address and not settings_copy.address.address2:
            settings_copy.address.address2 = None

        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)

        data = settings.update()
        self.put(url=url, json=data, params=params)

    def list_floors(self, location_id: str) -> List[Floor]:
        """
        List Location Floors

        Requires an administrator auth token with the `spark-admin:locations_read` scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :rtype: list[Floor]
        """
        url = self.ep(f'{location_id}/floors')
        data = super().get(url)
        r = TypeAdapter(list[Floor]).validate_python(data['items'])
        return r

    def create_floor(self, location_id: str, floor_number: int, display_name: str = None) -> Floor:
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

    def floor_details(self, location_id: str, floor_id: str) -> Floor:
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

    def update_floor(self, floor: Floor) -> Floor:
        """
        Update a Location Floor

        Updates details for a floor, by ID. Specify the floor ID in the `floorId` parameter in the URI. Include all
        details for the floor returned by a previous call to `Get Location Floor Details
        <https://developer.webex.com/docs/api/v1/locations/get-location-floor-details>`_. Omitting the optional
        `displayName` field will result in that field no longer being defined for the floor.
        Requires an administrator auth token with the `spark-admin:locations_write` scope.

        :param floor: new floor settings
        :type floor: Floor
        :rtype: :class:`Floor`
        """
        url = self.ep(f'{floor.location_id}/floors/{floor.id}')
        data = super().put(url, json=floor.update())
        r = Floor.model_validate(data)
        return r

    def delete_floor(self, location_id: str, floor_id: str):
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
