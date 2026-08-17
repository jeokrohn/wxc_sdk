from __future__ import annotations

import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallSettingsForMe33Api', 'OrganizationLocation', 'SpeedDialAvailableMember', 'SpeedDialItem',
           'SpeedDialItemType', 'SpeedDialPutItem', 'SpeedDialsGetResponse']


class SpeedDialItemType(str, Enum):
    #: The speed dial is a person.
    people = 'PEOPLE'
    #: The speed dial is a workspace.
    place = 'PLACE'
    #: The speed dial is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class SpeedDialItem(ApiModel):
    #: The identifier of the person, place or virtual line. See type for the resource type (PEOPLE, PLACE, or
    #: VIRTUAL_LINE). Only present for org speed dials.
    id: Optional[str] = None
    #: The last name of the person or virtual line.
    last_name: Optional[str] = None
    #: The first name of the person or virtual line.
    first_name: Optional[str] = None
    #: The display name of the person, place or virtual line.
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Only present for org speed dials.
    type: Optional[SpeedDialItemType] = None
    #: The phone number of the person, place or virtual line.
    phone_number: Optional[str] = None
    #: The extension number for the person, place or virtual line.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: The location name where the speed dial is. Only present for org speed dials.
    location_name: Optional[str] = None
    #: The ID for the location. Only present for org speed dials.
    location_id: Optional[str] = None
    #: This is a custom label configured for the speed dial on the device.
    line_key_label: Optional[str] = None


class SpeedDialsGetResponse(ApiModel):
    #: List of speed dial entries configured for the person.
    speed_dials: Optional[list[SpeedDialItem]] = None
    #: This is the number of additional entries that can be stored (more than the number of entries listed).
    available_entries_count: Optional[int] = None


class SpeedDialPutItem(ApiModel):
    #: The identifier of the person (PEOPLE), place (PLACE), or virtual line (VIRTUAL_LINE) to add as a speed dial. Use
    #: this field when adding a speed dial for an existing member in the organization. Either `id` or `phoneNumber`
    #: must be provided.
    id: Optional[str] = None
    #: The phone number to add as a speed dial. Use this field when adding a speed dial for an external contact or
    #: custom number. Either `id` or `phoneNumber` must be provided.
    phone_number: Optional[str] = None
    #: This is a custom label configured for the speed dial on the device.
    line_key_label: Optional[str] = None


class SpeedDialAvailableMember(ApiModel):
    #: The identifier of the person, place or virtual line. See type for the resource type.
    id: Optional[str] = None
    #: The last name of the person or virtual line.
    last_name: Optional[str] = None
    #: The first name of the person or virtual line.
    first_name: Optional[str] = None
    #: The display name of the person, place or virtual line.
    display_name: Optional[str] = None
    #: The phone number of the person, place or virtual line.
    phone_number: Optional[str] = None
    #: The extension number for the person, place or virtual line.
    extension: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `VIRTUAL_LINE` or `PLACE`.
    type: Optional[SpeedDialItemType] = None
    #: The ID for the location.
    location_id: Optional[str] = None
    #: The location name where the member is.
    location_name: Optional[str] = None


class OrganizationLocation(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None
    #: Location's routing prefix.
    routing_prefix: Optional[str] = None


class CallSettingsForMe33Api(ApiChild, base='telephony/config/people/me'):
    """
    Call Settings for Me (3/3)
    
    Call settings for me APIs allow a person to read or modify their settings.
    
    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.
    
    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """

    def get_my_organization_large_org_status(self) -> bool:
        """
        Get Large Organization Status

        Get whether the authenticated person's organization is considered as a large organization.

        Large organization status is used to determine how certain Webex Calling features behave, such as pagination
        limits and search capabilities, to optimize performance for organizations with many people.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: bool
        """
        url = self.ep('organization/largeOrgStatus')
        data = super().get(url)
        r = data['isLargeOrg']
        return r

    def get_my_organization_locations(self, name: list[str] = None, order: str = None,
                                      **params: Any) -> Generator[OrganizationLocation, None, None]:
        """
        Get Location List for My Organization

        Get the list of locations for the authenticated person's organization.

        Locations are used to organize Webex Calling resources such as people, workspaces, and features within an
        organization. Each location can have its own settings and configurations for calling services.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param name: Search (Contains) based on location name. Multiple values are logically OR-ed.
        :type name: list[str]
        :param order: Sort by location name (`name`). Sort directions asc or desc.
        * `asc` - Sort in ascending order.
        * `desc` - Sort in descending order.
        :type order: str
        :return: Generator yielding :class:`OrganizationLocation` instances
        """
        if name is not None:
            params['name'] = ','.join(name)
        if order is not None:
            params['order'] = order
        url = self.ep('organization/locations')
        return self.session.follow_pagination(url=url, model=OrganizationLocation, item_key='locations', params=params)

    def get_speed_dials(self) -> SpeedDialsGetResponse:
        """
        Get Speed Dials

        Get the Speed Dials settings for the authenticated user. This API returns all configured speed dials (no
        pagination).

        Speed Dials allow Webex Calling users to quickly dial frequently contacted people, places, or virtual lines by
        assigning them to dedicated keys on their desk phones or soft clients.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SpeedDialsGetResponse`
        """
        url = self.ep('settings/speedDials')
        data = super().get(url)
        r = SpeedDialsGetResponse.model_validate(data)
        return r

    def modify_speed_dials(self, speed_dials: list[SpeedDialPutItem]) -> None:
        """
        Modify Speed Dials

        Modify the Speed Dials settings for the authenticated user. This is a replacement list for speed dials.

        Speed Dials allow Webex Calling users to quickly dial frequently contacted people, places, or virtual lines by
        assigning them to dedicated keys on their desk phones or soft clients.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param speed_dials: List of speed dial entries to be configured for the person. This is a replacement list.
        :type speed_dials: list[SpeedDialPutItem]
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['speedDials'] = TypeAdapter(list[SpeedDialPutItem]).dump_python(speed_dials, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/speedDials')
        super().put(url, json=body)

    def get_speed_dial_available_members(self, location_id: str = None, name: list[str] = None,
                                         phone_number: list[str] = None, order: str = None,
                                         **params: Any) -> Generator[SpeedDialAvailableMember, None, None]:
        """
        Get Speed Dial Available Members

        Get the available members which can be configured as Speed Dials for the authenticated user.

        Speed Dials allow Webex Calling users to quickly dial frequently contacted people, places, or virtual lines by
        assigning them to dedicated keys on their desk phones or soft clients.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param location_id: Return the members list available in this location.
        :type location_id: str
        :param name: Search (Contains) based on first name and last name.
        :type name: list[str]
        :param phone_number: Search (Contains) based on number and extension.
        :type phone_number: list[str]
        :param order: Sort by first name (`firstName`) or last name (`lastName`). Sort directions asc or desc.
        * `asc` - Sort in ascending order.
        * `desc` - Sort in descending order.
        :type order: str
        :return: Generator yielding :class:`SpeedDialAvailableMember` instances
        """
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = ','.join(name)
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if order is not None:
            params['order'] = order
        url = self.ep('settings/speedDials/availableMembers')
        return self.session.follow_pagination(url=url, model=SpeedDialAvailableMember, item_key='members', params=params)
