from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateALocationResponse', 'Floor', 'FloorCollectionResponse', 'FloorCreationRequest', 'Location', 'LocationAddress', 'LocationsCollectionResponse', 'PostCommonLocationObject', 'PutCommonLocationObject']


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


class PutCommonLocationObject(ApiModel):
    #: The name of the location.
    #: example: 'Denver'
    name: Optional[str] = None
    #: Time zone associated with this location, refer to this link (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone) for format.
    #: example: 'America/Chicago'
    time_zone: Optional[str] = None
    #: Default email language.
    #: example: 'en_us'
    preferred_language: Optional[str] = None
    #: The address of the location.
    address: Optional[LocationAddress] = None


class PostCommonLocationObject(ApiModel):
    #: The name of the location.
    #: example: 'Denver'
    name: Optional[str] = None
    #: Time zone associated with this location, refer to this link (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone) for format.
    #: example: 'America/Chicago'
    time_zone: Optional[str] = None
    #: Default email language.
    #: example: 'en_us'
    preferred_language: Optional[str] = None
    #: Location's phone announcement language.
    #: example: 'fr_fr'
    announcement_language: Optional[str] = None
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


class LocationsCollectionResponse(ApiModel):
    items: Optional[list[Location]] = None


class Floor(ApiModel):
    #: Unique identifier for the floor.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL1dPUktTUEFDRV9MT0NBVElPTl9GTE9PUi83NDhkZDNmMS1iYmE5LTQxMDItODk5NC00M2IyOTM2MzNlNjY
    id: Optional[str] = None
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4NjczZDIwLWM0M2EtNDQ5Ni1iYWIxLTNiMjhhZGJjMjViYQ
    location_id: Optional[str] = None
    #: The floor number.
    #: example: -1.0
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class FloorCreationRequest(ApiModel):
    #: The floor number.
    #: example: -1.0
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class FloorCollectionResponse(ApiModel):
    #: An array of floor objects.
    items: Optional[list[Floor]] = None


class CreateALocationResponse(ApiModel):
    #: ID of the newly created location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzljYTNhZmQ3LTE5MjYtNGQ0ZS05ZDA3LTk5ZDJjMGU4OGFhMA
    id: Optional[str] = None
