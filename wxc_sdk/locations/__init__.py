"""
Locations

Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub may be
used to define new locations.

Searching and viewing locations in your organization requires an administrator auth token with the
spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_writescope
combinations.
"""

from collections.abc import Generator
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, webex_id_to_uuid

__all__ = ['LocationAddress', 'Location', 'LocationsApi']


class LocationAddress(ApiModel):
    """
    Address of a :class:`Location`
    """

    #: address line 1
    address1: str
    #: address line 2
    address2: Optional[str]
    #: city
    city: str
    #: state
    state: str
    #: ZIP/Postal code
    postal_code: str
    #: country
    country: Optional[str]


class Location(ApiModel):
    """
    Webex location

    """
    #: A unique identifier for the location.
    location_id: Optional[str] = Field(alias='id')
    #: The name of the location.
    name: Optional[str]
    #: The ID of the organization to which this location belongs.
    org_id: Optional[str]
    #: The address of the location, :class:`LocationAddress`
    address: Optional[LocationAddress]
    time_zone: Optional[str]
    preferred_language: Optional[str]

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


class LocationsApi(ApiChild, base='locations'):
    """
    Location API

    Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub
    may be used to define new locations.

    Searching and viewing locations in your organization requires an administrator auth token with the
    spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_write
    scope combinations.
    """

    def list(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> Generator[Location, None, None]:
        """
        List locations for an organization.

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

    def details(self, location_id) -> Location:
        """
        Shows details for a location, by ID.

        This API only works for Customer administrators and for Partner administrators to query their own organization.
        Partner administrators looking to query customer organizations should use the List Locations endpoint to
        retrieve information about locations.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :return: location details
        :rtype: :class:`Location`
        """
        ep = self.ep(location_id)
        return Location.parse_obj(self.get(ep))

    def create(self, name: str, time_zone: str, preferred_language: str, announcement_language: str, address1: str,
               city: str, state: str, postal_code: str, country: str, address2: str = None, org_id: str = None) -> str:
        """
        Create a new Location for a given organization. Only an admin in a Webex Calling licensed organization can
        create a new Location.

        The following body parameters are required to create a new location: name, timeZone, preferredLanguage,
        address, announcementLanguage.

        Creating a location in your organization requires an administrator auth token with
        the spark-admin:locations_write.

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
        :type org_id: str
        :return: ID of new location
        :rtype: :class:`Location`
        """
        # TODO: unit tests
        body = {}
        address = {}
        for p, v in list(locals().items()):
            if p in {'address', 'body', 'self'} or v is None:
                continue
            p = to_camel(p)
            if p == 'address1' or address:
                address[p] = v
            else:
                body[p] = v
        body['address'] = address
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = self.post(url=url, json=body, params=params)
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
        settings_copy = settings.copy(deep=True)
        if settings_copy.address and not settings_copy.address.address2:
            settings_copy.address.address2 = None

        data = settings_copy.json(exclude={'location_id', 'org_id'}, exclude_none=False, exclude_unset=True)
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)
        self.put(url=url, data=data, params=params)
