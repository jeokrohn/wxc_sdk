from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Floor', 'Location', 'WorkspaceLocationFloorsCollectionResponse', 'WorkspaceLocationFloorsCreationRequest', 'WorkspaceLocationsCollectionResponse', 'WorkspaceLocationsCreationRequest']


class Location(ApiModel):
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9XT1JLU1BBQ0VfTE9DQVRJT04vM2E2ZmYzNzMtNjhhNy00NGU0LTkxZDYtYTI3NDYwZTBhYzVjIzUxOWY2N2E1LTlkOTktNGM2My04YTA5LWI5MTcxY2M2NmJkMQ==
    id: Optional[str] = None
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
    #: example: 41.4066147
    latitude: Optional[int] = None
    #: The location longitude.
    #: example: 2.2007173
    longitude: Optional[int] = None
    #: Notes associated with the location.
    #: example: A note about the location
    notes: Optional[str] = None


class WorkspaceLocationsCreationRequest(ApiModel):
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
    #: example: 41.4066147
    latitude: Optional[int] = None
    #: The location longitude.
    #: example: 2.2007173
    longitude: Optional[int] = None
    #: Notes associated with the location.
    #: example: A note about the location
    notes: Optional[str] = None


class WorkspaceLocationsCollectionResponse(ApiModel):
    #: An array of location objects.
    items: Optional[list[Location]] = None


class Floor(ApiModel):
    #: Unique identifier for the floor.
    #: example: xxx==
    id: Optional[str] = None
    #: Unique identifier for the location.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9XT1JLU1BBQ0VfTE9DQVRJT04vM2E2ZmYzNzMtNjhhNy00NGU0LTkxZDYtYTI3NDYwZTBhYzVjIzUxOWY2N2E1LTlkOTktNGM2My04YTA5LWI5MTcxY2M2NmJkMQ==
    location_id: Optional[str] = None
    #: The floor number.
    #: example: -1.0
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class WorkspaceLocationFloorsCreationRequest(ApiModel):
    #: The floor number.
    #: example: -1.0
    floor_number: Optional[int] = None
    #: The floor display name.
    #: example: The basement
    display_name: Optional[str] = None


class WorkspaceLocationFloorsCollectionResponse(ApiModel):
    #: An array of floor objects.
    items: Optional[list[Floor]] = None
