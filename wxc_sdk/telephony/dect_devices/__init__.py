from collections.abc import Generator
from typing import Optional

from pydantic import TypeAdapter, Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import IdAndName, UserType, AssignedDectNetwork
from wxc_sdk.telephony.devices import AvailableMember

__all__ = ['DECTNetworkModel', 'DECTNetworkDetail', 'BaseStationResult', 'BaseStationResponse', 'BaseStationsResponse',
           'DECTHandsetLine', 'Handset', 'BaseStationDetail', 'DECTHandsetItem', 'DECTHandsetList', 'UsageType',
           'DECTDevicesApi']


class DECTNetworkModel(str, Enum):
    #: Supports 1 base station and 30 line ports.
    dms_cisco_dbs110 = 'DMS Cisco DBS110'
    #: Supports 250 base stations and 1000 line ports.
    dms_cisco_dbs210 = 'DMS Cisco DBS210'


class DECTNetworkDetail(ApiModel):
    #: Unique identifier for the DECT network.
    id: Optional[str] = None
    #: Name of the DECT network. This should be unique across the location.
    name: Optional[str] = None
    #: DECT network name that will be displayed on the handset.
    display_name: Optional[str] = None
    #: Chain ID of the DECT network.
    chain_id: Optional[int] = None
    #: Indicates the base station model deployed in the DECT network.
    model: Optional[DECTNetworkModel] = None
    #: Default access code is enabled. If true, the default access code is mandatory. If false, auto-generated access
    #: code is used.
    default_access_code_enabled: Optional[bool] = None
    #: Default access code for the DECT network. The default access code should be unique within the same location to
    #: avoid the handset accidentally registering with base stations from different DECT networks in range. This is
    #: mandatory when `defaultAccessCodeEnabled` is true.
    default_access_code: Optional[str] = None
    #: Number of base stations in the DECT network.
    number_of_base_stations: Optional[int] = None
    #: Number of handsets assigned to the DECT network.
    number_of_handsets_assigned: Optional[int] = None
    #: Number of lines in the DECT network.
    number_of_lines: Optional[int] = None
    #: Location of the DECT network.
    location: Optional[IdAndName] = None

    def update(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json',
                               exclude_none=True,
                               include={'display_name', 'default_access_code_enabled', 'default_access_code'})


class BaseStationResult(ApiModel):
    #: HTTP status code indicating the creation of base station. 201 status code indicates the successful creation of
    #: base stations
    status: Optional[int] = None
    #: Unique identifier of the base station.
    id: Optional[str] = None


class BaseStationResponse(ApiModel):
    #: MAC Address added to the base station.
    mac: Optional[str] = None
    #: Object with base station POST Result.
    result: Optional[BaseStationResult] = None


class BaseStationsResponse(ApiModel):
    #: Unique identifier of the base station.
    id: Optional[str] = None
    #: Mac address of the DECT base station device.
    mac: Optional[str] = None
    #: Number of handset member lines registered with the base station.
    number_of_lines_registered: Optional[int] = None


class DECTHandsetLine(ApiModel):
    #: ID of the member on line1 of the handset. Members can be PEOPLE or PLACE.
    member_id: Optional[str] = None
    #: Line members's first name.
    first_name: Optional[str] = None
    #: Line members's last name.
    last_name: Optional[str] = None
    #: Line members primary number.
    external: Optional[str] = None
    #: Line members extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension
    esn: Optional[str] = None
    #: Last registration timestamp.
    last_registration_time: Optional[str] = None
    #: Registration host IP address for the line port.
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP address for the line port.
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Location object having a unique identifier for the location and its name.
    location: Optional[IdAndName] = None
    #: Indicates member type.
    member_type: Optional[UserType] = None


class Handset(ApiModel):
    #: Unique identifier of the DECT handset.
    #: example:
    # Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5RG
    id: Optional[str] = None
    #: Display name of the DECT handset.
    display_name: Optional[str] = None
    #: Access code for the DECT handset.
    access_code: Optional[str] = None
    #: Details of the handset member lines registered with the base station. The maximum number of lines supported is
    #: 2.
    lines: Optional[list[DECTHandsetLine]] = None


class BaseStationDetail(ApiModel):
    #: Unique identifier of the base station.
    #: example:
    # Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Mac address of the DECT base station device.
    mac: Optional[str] = None
    #: List of handset and member line details registered with the base station.
    handsets: Optional[list[Handset]] = None


class DECTHandsetItem(ApiModel):
    #: Unique identifier of the handset.
    id: Optional[str] = None
    #: Index of the handset.
    index: Optional[int] = None
    #: Default display name for the handset.
    default_display_name: Optional[str] = None
    #: Custom display name on the handset.
    custom_display_name: Optional[str] = None
    #: Unique identifier of the associated base station.
    base_station_id: Optional[str] = None
    #: MAC Address associated with the handset.
    mac: Optional[str] = None
    #: Access code is used to pair handsets to the DECT Network for the first time or if a handset becomes
    #: disconnected.
    access_code: Optional[str] = None
    #: Flags the handset as a primary line if `true`.
    primary_enabled: Optional[bool] = None
    #: Array of lines associated to the handset.Maximum: 2 lines.
    lines: Optional[list[DECTHandsetLine]] = None


class DECTHandsetList(ApiModel):
    #: Number of handsets associated.
    number_of_handsets_assigned: Optional[int] = None
    #: Total number of lines assigned.
    number_of_lines_assigned: Optional[int] = None
    #: Array of `DECTHandsetItem` objects, each representing a handset with its associated details and lines.
    handsets: Optional[list[DECTHandsetItem]] = None


class UsageType(str, Enum):
    device_owner = 'DEVICE_OWNER'
    shared_line = 'SHARED_LINE'


class DECTDevicesApi(ApiChild, base='telephony/config'):
    """
    DECT Devices Settings

    Not supported for Webex for Government (FedRAMP)

    DECT APIs allow the admin to create a DECT network, and add base stations and handsets to the DECT network. People,
    places and virtual lines member types are supported on handset lines in the DECT network. Currently, APIs support
    Cisco DECT device models only.

    Viewing and searching  DECT settings requires a full or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.

    Adding and modifying these DECT settings requires a full administrator auth token with a scope
    of `spark-admin:telephony_config_write`.
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

    def list_dect_networks(self, name: str = None, location_id: str = None,
                           org_id: str = None) -> list[DECTNetworkDetail]:
        """
        Get the List of DECT Networks for an organization

        Retrieves the list of DECT networks for an organization.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param name: List of DECT networks with this name.
        :type name: str
        :param location_id: List of DECT networks at this location.
        :type location_id: str
        :param org_id: List of DECT networks in this organization.
        :type org_id: str
        :rtype: list[DECTNetworkDetail]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep('dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DECTNetworkDetail]).validate_python(data['dectNetworks'])
        return r

    def dect_network_details(self, location_id: str, dect_network_id: str,
                             org_id: str = None) -> DECTNetworkDetail:
        """
        Get DECT Network Details

        Retrieves the details of a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param location_id: Details of the DECT network at this location.
        :type location_id: str
        :param dect_network_id: Details of the specified DECT network.
        :type dect_network_id: str
        :param org_id: Details of the DECT network in this organization.
        :type org_id: str
        :rtype: :class:`DECTNetworkDetail`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}')
        data = super().get(url, params=params)
        r = DECTNetworkDetail.model_validate(data)
        return r

    def update_dect_network(self, location_id: str, dect_network_id: str, name: str, default_access_code_enabled: bool,
                            default_access_code: str = None, display_name: str = None, org_id: str = None):
        """
        Update DECT Network

        Update the details of a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Update DECT network details in the specified location.
        :type location_id: str
        :param dect_network_id: Update DECT network details in the specified DECT network.
        :type dect_network_id: str
        :param name: Name of the DECT network. This should be unique across the location.
        :type name: str
        :param default_access_code_enabled: Default access code is enabled. If true, the default access code is
            mandatory. If false, an auto-generated access code is used.
        :type default_access_code_enabled: bool
        :param default_access_code: Default access code for the DECT network. The default access code should be unique
            within the same location to avoid the handset accidentally registering with base stations from different
            DECT networks in range. This is mandatory when `defaultAccessCodeEnabled` is true.
        :type default_access_code: str
        :param display_name: DECT network name that will be displayed on the handset.
        :type display_name: str
        :param org_id: Update DECT network details in the specified organization.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = dict()
        body['name'] = name
        if display_name is not None:
            body['displayName'] = display_name
        body['defaultAccessCodeEnabled'] = default_access_code_enabled
        if default_access_code is not None:
            body['defaultAccessCode'] = default_access_code or None
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}')
        super().put(url, params=params, json=body)

    def update_dect_network_settings(self, settings: DECTNetworkDetail, org_id: str = None):
        """
        Update DECT Network from settings

        Update the details of a DECT network from settings.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param settings: DECT Network to update. location.id and id are used to address the DECT network to be
            updated. Only name, display_name, default_access_code_enabled, default_access_code are considered for the
            update

        :param org_id: Update DECT network details in the specified organization.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = settings.model_dump(mode='json', by_alias=True,
                                   include={'name', 'display_name', 'default_access_code_enabled',
                                            'default_access_code'})
        url = self.ep(f'locations/{settings.location.id}/dectNetworks/{settings.id}')
        super().put(url, params=params, json=body)

    def delete_dect_network(self, location_id: str, dect_network_id: str, org_id: str = None):
        """
        Delete DECT Network

        Delete a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Delete the DECT network in the specified location.
        :type location_id: str
        :param dect_network_id: Delete the specified DECT network.
        :type dect_network_id: str
        :param org_id: Delete the DECT network in the specified organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}')
        super().delete(url, params=params)

    def create_base_stations(self, location_id: str, dect_id: str, base_station_macs: list[str],
                             org_id: str = None) -> list[BaseStationResponse]:
        """
        Create Multiple Base Stations

        This API is used to create multiple base stations in a DECT network in an organization.

        Creating base stations in a DECT network requires a full administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

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
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_id}/baseStations')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[BaseStationResponse]).validate_python(data['baseStations'])
        return r

    def list_base_stations(self, location_id: str, dect_network_id: str,
                           org_id: str = None) -> list[BaseStationsResponse]:
        """
        Get a list of DECT Network Base Stations

        Retrieve a list of base stations in a DECT Network.

        A DECT network supports 2 types of base stations, DECT DBS-110 Single-Cell and DECT DBS-210 Multi-Cell.
        A DECT DBS-110 allows up to 30 lines of registration and supports 1 base station only. A DECT DBS-210 can have
        up to 254 base stations and supports up to 1000 lines of registration.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Retrieve the list of base stations in the specified DECT network ID.
        :type dect_network_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: list[BaseStationsResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations')
        data = super().get(url, params=params)
        r = TypeAdapter(list[BaseStationsResponse]).validate_python(data['baseStations'])
        return r

    def base_station_details(self, location_id: str, dect_network_id: str,
                             base_station_id: str,
                             org_id: str = None) -> BaseStationDetail:
        """
        Get the details of a specific DECT Network Base Station

        Retrieve details of a specific base station in the DECT Network.

        A DECT network supports 2 types of base stations, DECT DBS-110 Single-Cell and DECT DBS-210 Multi-Cell.
        A DECT DBS-110 allows up to 30 lines of registration and supports 1 base station only. A DECT DBS-210 can have
        up to 254 base stations and supports up to 1000 lines of registration.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Retrieve details of a specific base station in the specified DECT network ID.
        :type dect_network_id: str
        :param base_station_id: Retrieve details of the specific DECT base station ID.
        :type base_station_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: :class:`BaseStationDetail`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}')
        data = super().get(url, params=params)
        r = BaseStationDetail.model_validate(data)
        return r

    def delete_bulk_base_stations(self, location_id: str, dect_network_id: str, org_id: str = None):
        """
        Delete bulk DECT Network Base Stations

        Delete all the base stations in the DECT Network.

        A DECT network supports 2 types of base stations, DECT DBS-110 Single-Cell and DECT DBS-210 Multi-Cell.
        A DECT DBS-110 allows up to 30 lines of registration and supports 1 base station only. A DECT DBS-210 can have
        up to 254 base stations and supports up to 1000 lines of registration.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Delete all the base stations in the specified DECT network ID.
        :type dect_network_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations')
        super().delete(url, params=params)

    def delete_base_station(self, location_id: str, dect_network_id: str, base_station_id: str,
                            org_id: str = None):
        """
        Delete a specific DECT Network Base Station

        Delete a specific base station in the DECT Network.

        A DECT network supports 2 types of base stations, DECT DBS-110 Single-Cell and DECT DBS-210 Multi-Cell.
        A DECT DBS-110 allows up to 30 lines of registration and supports 1 base station only. A DECT DBS-210 can have
        up to 254 base stations and supports up to 1000 lines of registration.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Delete a specific base station in the specified DECT network ID.
        :type dect_network_id: str
        :param base_station_id: Delete the specific DECT base station ID.
        :type base_station_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}')
        super().delete(url, params=params)

    def add_a_handset(self, location_id: str, dect_network_id: str, line1_member_id: str,
                      line2_member_id: str = None, custom_display_name: str = None, org_id: str = None):
        """
        Add a Handset to a DECT Network

        Add a handset to a DECT network in a location in an organization.

        Adding a handset to a DECT network requires a full administrator auth token with a scope
        of `spark-admin:telephony_config_write`

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
            display name is 1 and 16 respectively. Mandatory parameter.
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
        if line2_member_id is not None:
            body['line2MemberId'] = line2_member_id
        if custom_display_name is None:
            raise ValueError('custom_display_name cannot be None')
        body['customDisplayName'] = custom_display_name
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets')
        super().post(url, params=params, json=body)

    def list_handsets(self, location_id: str, dect_network_id: str,
                      basestation_id: str = None, member_id: str = None,
                      org_id: str = None) -> DECTHandsetList:
        """
        Get List of Handsets for a DECT Network ID

        List all the handsets associated with a DECT Network ID.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Search handset details in the specified DECT network ID.
        :type dect_network_id: str
        :param basestation_id: Search handset details in the specified DECT base station ID.
        :type basestation_id: str
        :param member_id: ID of the member of the handset. Members can be of type PEOPLE, PLACE, or VIRTUAL_LINE.
        :type member_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: :class:`DECTHandsetList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if basestation_id is not None:
            params['basestationId'] = basestation_id
        if member_id is not None:
            params['memberId'] = member_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets')
        data = super().get(url, params=params)
        r = DECTHandsetList.model_validate(data)
        return r

    def handset_details(self, location_id: str, dect_network_id: str, handset_id: str,
                        org_id: str = None) -> DECTHandsetItem:
        """
        Get Specific DECT Network Handset Details

        List the specific DECT Network handset details.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Search handset details in the specified DECT network ID.
        :type dect_network_id: str
        :param handset_id: A unique identifier for the handset.
        :type handset_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: :class:`DECTHandsetGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}')
        data = super().get(url, params=params)
        r = DECTHandsetItem.model_validate(data)
        return r

    def update_handset(self, location_id: str, dect_network_id: str, handset_id: str,
                       line1_member_id: str, custom_display_name: str, line2_member_id: str = None,
                       org_id: str = None):
        """
        Update DECT Network Handset

        Update the line assignment on a handset.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        Updating a DECT Network handset requires a full administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Update handset details in the specified DECT network.
        :type dect_network_id: str
        :param handset_id: A unique identifier for the handset.
        :type handset_id: str
        :param line1_member_id: ID of the member on line1 of the handset. Members can be PEOPLE or PLACE.
        :type line1_member_id: str
        :param custom_display_name: Custom display name on the handset.
        :type custom_display_name: str
        :param line2_member_id: ID of the member on line2 of the handset. Members can be PEOPLE, PLACE, or
            VIRTUAL_LINE.
        :type line2_member_id: str
        :param org_id: Organization containing the DECT network.
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
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}')
        super().put(url, params=params, json=body)

    def delete_handset(self, location_id: str, dect_network_id: str, handset_id: str,
                       org_id: str = None):
        """
        Delete specific DECT Network Handset Details

        Delete a specific DECT Network handset.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Delete handset details in the specified DECT network ID.
        :type dect_network_id: str
        :param handset_id: A unique identifier for the handset.
        :type handset_id: str
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}')
        super().delete(url, params=params)

    def delete_handsets(self, location_id: str, dect_network_id: str, handset_ids: list[str],
                        delete_all: bool = None, org_id: str = None):
        """
        Delete multiple handsets

        Delete multiple handsets or all of them.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location containing the DECT network.
        :type location_id: str
        :param dect_network_id: Delete handset details in the specified DECT network ID.
        :type dect_network_id: str
        :param handset_ids: Array of the handset IDs to be deleted.
        :type handset_ids: list[str]
        :param delete_all: If present the items array is ignored and all items in the context are deleted.
        :type delete_all: bool
        :param org_id: Organization containing the DECT network.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['handsetIds'] = handset_ids
        if delete_all is not None:
            body['deleteAll'] = delete_all
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets')
        super().delete(url, params=params, json=body)

    def dect_networks_associated_with_person(self, person_id: str,
                                             org_id: str = None) -> list[AssignedDectNetwork]:
        """
        GET List of DECT networks associated with a Person

        Retrieves the list of DECT networks for a person in an organization.

        DECT Network provides roaming voice services via base stations and wireless handsets. DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param person_id: List of DECT networks associated with this person.
        :type person_id: str
        :param org_id: List of DECT networks associated with a person in this organization.
        :type org_id: str
        :rtype: list[AssignedDectNetwork]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AssignedDectNetwork]).validate_python(data['dectNetworks'])
        return r

    def dect_networks_associated_with_workspace(self, workspace_id: str,
                                                org_id: str = None) -> list[AssignedDectNetwork]:
        """
        GET List of DECT networks associated with a workspace

        Retrieves the list of DECT networks for a workspace in an organization.

        DECT Network provides roaming voice services via base stations and wireless handsets. DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: List of DECT networks associated with this workspace.
        :type workspace_id: str
        :param org_id: List of DECT networks associated with a workspace in this organization.
        :type org_id: str
        :rtype: list[AssignedDectNetwork]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AssignedDectNetwork]).validate_python(data['dectNetworks'])
        return r

    def dect_networks_associated_with_virtual_line(self, virtual_line_id: str,
                                                   org_id: str = None) -> list[AssignedDectNetwork]:
        """
        Get List of Dect Networks Handsets for a Virtual Line

        Retrieve DECT Network details assigned for a virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving the assigned device detials for a virtual line requires a full or user or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: list[AssignedDectNetwork]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id

        url = self.ep(f'virtualLines/{virtual_line_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AssignedDectNetwork]).validate_python(data['dectNetworks'])
        return r

    def available_members(self, member_name: str = None, phone_number: str = None, extension: str = None,
                          location_id: str = None, order: str = None, exclude_virtual_line: bool = None,
                          usage_type: UsageType = None, org_id: str = None,
                          **params) -> Generator[AvailableMember, None, None]:
        """
        Search Available Members

        List the members that are available to be assigned to DECT handset lines.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

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
        :param usage_type: Search for members eligible to become the owner of the device, or share line on the device.
        :type usage_type: UsageType
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
        if extension is not None:
            params['extension'] = extension
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if exclude_virtual_line is not None:
            params['excludeVirtualLine'] = str(exclude_virtual_line).lower()
        if usage_type is not None:
            params['usageType'] = enum_str(usage_type)
        url = self.ep('devices/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableMember, item_key='members', params=params)
