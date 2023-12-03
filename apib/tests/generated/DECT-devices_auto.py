from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AvailableMembersResponse', 'BaseStationPostResult', 'BaseStationResponse', 'CreateDECTNetworkModel',
            'DECTDevicesSettingsApi', 'LineType', 'Location', 'MemberType']


class CreateDECTNetworkModel(str, Enum):
    #: Supports 1 base station and 30 line ports.
    dms_cisco_dbs110 = 'DMS Cisco DBS110'
    #: Supports 250 base stations and 1000 line ports.
    dms_cisco_dbs210 = 'DMS Cisco DBS210'


class BaseStationPostResult(ApiModel):
    #: HTTP status code indicating the creation of base station. 201 status code indicates the successful creation of
    #: base stations.
    #: example: 201
    status: Optional[int] = None
    #: Unique identifier of the base station.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX1NUQVRJT04vYzRhMTQxN2ItZGNiYi00MGMzLWE3YWQtNTY1MGZkZGRkNTNj
    id: Optional[str] = None


class BaseStationResponse(ApiModel):
    #: MAC Address added to the base station.
    #: example: 6DDE9EBDE1C9
    mac: Optional[str] = None
    #: Object with base station POST Result.
    result: Optional[BaseStationPostResult] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'
    #: Indicates the associated member is a virtual profile.
    virtual_line = 'VIRTUAL_LINE'


class Location(ApiModel):
    #: Location identifier associated with the member.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX05FVC81NmRiMjRkMy03YTdhLTQwYTItOWFjOS1iMjMzMjc3OTIxTrd
    id: Optional[str] = None
    #: Location name associated with the member.
    #: example: MainOffice
    name: Optional[str] = None


class AvailableMembersResponse(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: First name of the member.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of the member.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone Number of the member.
    #: example: +12055552221
    phone_number: Optional[str] = None
    #: Extension of the member.
    #: example: 1234
    extension: Optional[str] = None
    #: Line type indicates if the associated line is a primary line or a shared line.
    line_type: Optional[LineType] = None
    #: Indicates the type of the member.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class DECTDevicesSettingsApi(ApiChild, base='telephony/config'):
    """
    DECT Devices Settings
    
    DECT APIs allow the admin to create a DECT network, and add base stations and handsets to the DECT network. People,
    places and virtual lines member types are supported on handset lines in the DECT network. Currently, APIs support
    Cisco DECT device models only.
    
    Viewing and searching  DECT settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Adding and modifying these DECT settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def create_a_dect_network(self, location_id: str, name: str, model: CreateDECTNetworkModel,
                              default_access_code_enabled: bool, default_access_code: str, display_name: str = None,
                              org_id: str = None) -> str:
        """
        Create a DECT Network

        Create a multi-cell DECT network for a given location.

        Creating a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create a DECT network in this location.
        :type location_id: str
        :param name: Name of the DECT network. Min and max length supported for the DECT network name are 1 and 40
            respectively.
        :type name: str
        :param model: Select a device model type depending on the number of base stations and handset lines needed in
            the DECT network.
        :type model: CreateDECTNetworkModel
        :param default_access_code_enabled: If set to true, need to provide a default access code that will be shared
            for all users in this network to pair their lines to the next available handset. Otherwise, each user will
            get a unique 4-digit access code that will be auto-generated. Note: There is currently no public API to
            retrieve the auto generated access codes for handsets. Use Control Hub instead.
        :type default_access_code_enabled: bool
        :param default_access_code: If `defaultAccessCodeEnabled` is set to true, then provide a default access code
            that needs to be a 4-numeric digit. The access code should be unique to the DECT network for the location.
        :type default_access_code: str
        :param display_name: Add a default name (11 characters max) to display for all handsets. If left blank, the
            default name will be an indexed number followed by the DECT network name.
        :type display_name: str
        :param org_id: Create a DECT network in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if display_name is not None:
            body['displayName'] = display_name
        body['model'] = enum_str(model)
        body['defaultAccessCodeEnabled'] = default_access_code_enabled
        body['defaultAccessCode'] = default_access_code
        url = self.ep(f'locations/{location_id}/dectNetworks')
        data = super().post(url, params=params, json=body)
        r = data['dectNetworkId']
        return r

    def create_multiple_base_stations(self, location_id: str, dect_network_id: str, base_station_macs: list[str],
                                      org_id: str = None) -> list[BaseStationResponse]:
        """
        Create Multiple Base Stations

        This API is used to create multiple base stations in a DECT network in an organization.

        Creating base stations in a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create a base station in this location.
        :type location_id: str
        :param dect_network_id: Create a base station for the DECT network.
        :type dect_network_id: str
        :param base_station_macs: Array of base station MAC addresses.
        :type base_station_macs: list[str]
        :param org_id: Create a base station for a DECT network in this organization.
        :type org_id: str
        :rtype: list[BaseStationResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['baseStationMacs'] = base_station_macs
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[BaseStationResponse]).validate_python(data['baseStations'])
        return r

    def add_a_handset_to_a_dect_network(self, location_id: str, dect_network_id: str, line1_member_id: str,
                                        custom_display_name: str, line2_member_id: str = None, org_id: str = None):
        """
        Add a Handset to a DECT Network

        Add a handset to a DECT network in a location in an organization.

        Adding a handset to a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Add handset in this location.
        :type location_id: str
        :param dect_network_id: A unique identifier for the DECT network.
        :type dect_network_id: str
        :param line1_member_id: ID of the member on line1 of the handset. Members can be PEOPLE or PLACE.
        :type line1_member_id: str
        :param custom_display_name: Custom display name on the handset. Min and max length supported for the custom
            display name is 1 and 16 respectively.
        :type custom_display_name: str
        :param line2_member_id: ID of the member on line2 of the handset. Members can be PEOPLE, PLACE, or
            VIRTUAL_LINE.
        :type line2_member_id: str
        :param org_id: Add handset in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['line1MemberId'] = line1_member_id
        if line2_member_id is not None:
            body['line2MemberId'] = line2_member_id
        body['customDisplayName'] = custom_display_name
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets')
        super().post(url, params=params, json=body)

    def search_available_members(self, start: int = None, max_: int = None, member_name: str = None,
                                 phone_number: str = None, extension: str = None, location_id: str = None,
                                 order: str = None, exclude_virtual_line: bool = None,
                                 org_id: str = None) -> AvailableMembersResponse:
        """
        Search Available Members

        List the members that are available to be assigned to DECT handset lines.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param max_: Specifies the maximum number of records that you want to fetch.
        :type max_: int
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param location_id: List members for the location ID.
        :type location_id: str
        :param order: Sort the list of available members on the device in ascending order by name, using either last
            name `lname` or first name `fname`. Default sort is the last name in ascending order.
        :type order: str
        :param exclude_virtual_line: If true, search results will exclude virtual lines in the member list. NOTE:
            Virtual lines cannot be assigned as the primary line.
        :type exclude_virtual_line: bool
        :param org_id: Search members in this organization.
        :type org_id: str
        :rtype: :class:`AvailableMembersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        if max_ is not None:
            params['max'] = max_
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if exclude_virtual_line is not None:
            params['excludeVirtualLine'] = str(exclude_virtual_line).lower()
        url = self.ep('devices/availableMembers')
        data = super().get(url, params=params)
        r = AvailableMembersResponse.model_validate(data)
        return r
