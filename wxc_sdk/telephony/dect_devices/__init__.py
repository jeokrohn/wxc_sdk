from collections.abc import Generator
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['DECTNetworkModel', 'BaseStationResult', 'BaseStationResponse', 'DECTDevicesApi']

from wxc_sdk.telephony.devices import AvailableMember


class DECTNetworkModel(str, Enum):
    #: Supports 1 base station and 30 line ports.
    dms_cisco_dbs110 = 'DMS Cisco DBS110'
    #: Supports 250 base stations and 1000 line ports.
    dms_cisco_dbs210 = 'DMS Cisco DBS210'


class BaseStationResult(ApiModel):
    #: HTTP status code indicating the creation of base station. 201 status code indicates the successful creation of
    #: base stations
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
    result: Optional[BaseStationResult] = None


class DECTDevicesApi(ApiChild, base='telephony/config'):
    """
    DECT Devices Settings

    Not supported for Webex for Government (FedRAMP)

    DECT APIs allow the admin to create a DECT network, and add base stations and handsets to the DECT network. People,
    places and virtual lines member types are supported on handset lines in the DECT network. Currently, APIs support
    Cisco DECT device models only.

    Viewing and searching  DECT settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Adding and modifying these DECT settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def create_dect_network(self, location_id: str, name: str, display_name: str, model: DECTNetworkModel,
                            default_access_code_enabled: bool, default_access_code: str,
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
        :param display_name: Add a default name (11 characters max) to display for all handsets. If left blank, the
            default name will be an indexed number followed by the DECT network name.
        :type display_name: str
        :param model: Select a device model type depending on the number of base stations and handset lines needed in
            the DECT network.
        :type model: DECTNetworkModel
        :param default_access_code_enabled: If set to true, need to provide a default access code that will be shared
            for all users in this network to pair their lines to the next available handset. Otherwise, each user will
            get a unique 4-digit access code that will be auto-generated. Note: There is currently no public API to
            retrieve the auto generated access codes for handsets. Use Control Hub instead.
        :type default_access_code_enabled: bool
        :param default_access_code: If `defaultAccessCodeEnabled` is set to true, then provide a default access code
            that needs to be a 4-numeric digit. The access code should be unique to the DECT network for the location.
        :type default_access_code: str
        :param org_id: Create a DECT network in this organization
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['displayName'] = display_name
        body['model'] = enum_str(model)
        body['defaultAccessCodeEnabled'] = default_access_code_enabled
        body['defaultAccessCode'] = default_access_code
        url = self.ep(f'locations/{location_id}/dectNetworks')
        data = super().post(url, params=params, json=body)
        r = data['dectNetworkId']
        return r

    def create_base_stations(self, location_id: str, dect_id: str, base_station_macs: list[str],
                             org_id: str = None) -> list[BaseStationResponse]:
        """
        Create Multiple Base Stations

        This API is used to create multiple base stations in a DECT network in an organization.

        Creating base stations in a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create a base station in this location.
        :type location_id: str
        :param dect_id: Create a base station for the DECT network.
        :type dect_id: str
        :param base_station_macs: Array of base stations.
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
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_id}/basestations')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[BaseStationResponse]).validate_python(data['baseStationMacs'])
        return r

    def add_a_handset(self, location_id: str, dect_network_id: str, line1_member_id: str,
                      line2_member_id: str, custom_display_name: str, org_id: str = None):
        """
        Add a Handset to a DECT Network

        Add a handset to a DECT network in a location in an organization.

        Adding a handset to a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`

        :param location_id: Add handset in this location.
        :type location_id: str
        :param dect_network_id: A unique identifier for the DECT network.
        :type dect_network_id: str
        :param line1_member_id: ID of the member on line1 of the handset. Members can be PEOPLE or PLACE.
        :type line1_member_id: str
        :param line2_member_id: ID of the member on line2 of the handset. Members can be PEOPLE, PLACE, or
            VIRTUAL_LINE.
        :type line2_member_id: str
        :param custom_display_name: Custom display name on the handset. Min and max length supported for the custom
            display name is 1 and 16 respectively
        :type custom_display_name: str
        :param org_id: Add handset in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['line1MemberId'] = line1_member_id
        body['line2MemberId'] = line2_member_id
        body['customDisplayName'] = custom_display_name
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets')
        super().post(url, params=params, json=body)

    def available_members(self, member_name: str = None, phone_number: str = None, order: str = None,
                          exclude_virtual_profile: bool = None, org_id: str = None,
                          **params) -> Generator[AvailableMember, None, None]:
        """
        Search Available Members

        List the members that are available to be assigned to DECT handset lines.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`

        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param order: Sort the list of available members on the device in ascending order by name, using either last
            name `lname` or first name `fname`. Default sort is the last name in ascending order.
        :type order: str
        :param exclude_virtual_profile: If true, search results will exclude virtual lines in the member list. NOTE:
            Virtual lines cannot be assigned as the primary line.
        :type exclude_virtual_profile: bool
        :param org_id: Search members in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        if exclude_virtual_profile is not None:
            params['excludeVirtualProfile'] = str(exclude_virtual_profile).lower()
        url = self.ep('devices/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableMember, item_key='members', params=params)
