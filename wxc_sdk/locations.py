"""
Locations

Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub may be
used to define new locations.

Searching and viewing locations in your organization requires an administrator auth token with the
spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_writescope
combinations.
"""

from collections.abc import Generator
from typing import List, Optional

from pydantic import Field

from .api_child import ApiChild
from .base import ApiModel, to_camel, webex_id_to_uuid

__all__ = ['LocationAddress', 'Location', 'LocationsApi']


class LocationAddress(ApiModel):
    """
    Address of a :class:`Location`

    :ivar address1: address line 1
    :ivar address2: address line 1
    :ivar city:
    :ivar state:
    :ivar postal_code: ZIP/Postal code
    :ivar country:
    """

    address1: str
    address2: str
    city: str
    state: Optional[str]
    postal_code: str
    country: str


class Location(ApiModel):
    """
    Webex location

    :ivar location_id: A unique identifier for the location.
    :ivar name: The name of the location.
    :ivar org_id: The ID of the organization to which this location belongs.
    :ivar address: The address of the location, :class:`LocationAddress`
    """
    location_id: str = Field(alias='id')
    name: str
    org_id: str
    address: LocationAddress

    @property
    def location_id_uuid(self):
        return webex_id_to_uuid(self.location_id)

    @property
    def org_id_uuid(self):
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

    def list(self, name: str = None, location_id: str = None, org_id: str = None) -> Generator[Location, None, None]:
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
        data = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                if i and k != 'self' and v is not None}
        if location_id is not None:
            data.pop('locationId')
            data['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Location, params=data)

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
        :rtype: Location
        """
        ep = self.ep(location_id)
        return Location.parse_obj(self.get(ep))
