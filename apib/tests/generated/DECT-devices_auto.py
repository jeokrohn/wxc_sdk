from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AvailableMember', 'BaseStationDetailResponse', 'BaseStationPostResult', 'BaseStationResponse',
           'BaseStationType', 'BaseStationsResponse', 'CreateDECTNetworkModel', 'DECTDevicesSettingsApi',
           'DECTHandsetGet', 'DECTHandsetItem', 'DECTHandsetLineResponse', 'DECTHandsetList', 'DECTNetworkDetail',
           'DECTNetworkItem', 'HandsetsResponse', 'LineType', 'Lines', 'Location', 'MemberType',
           'SearchAvailableMembersUsageType']


class CreateDECTNetworkModel(str, Enum):
    #: Model name supporting 1 base station and 30 line ports.
    dms_cisco_dbs110 = 'DMS Cisco DBS110'
    #: Alternate product/display name which also specifies the model `DMS Cisco DBS110`.
    cisco_dect_110_base = 'Cisco DECT 110 Base'
    #: Supports 250 base stations and 1000 line ports.
    dms_cisco_dbs210 = 'DMS Cisco DBS210'
    #: Alternate product/display name which also specifies the model `DMS Cisco DBS210`.
    cisco_dect_210_base = 'Cisco DECT 210 Base'


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


class AvailableMember(ApiModel):
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


class Lines(ApiModel):
    #: ID of the member on line1 of the handset. Members can be PEOPLE or PLACE.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    member_id: Optional[str] = None
    #: Line members's first name.
    #: example: John
    first_name: Optional[str] = None
    #: Line members's last name.
    #: example: Smith
    last_name: Optional[str] = None
    #: Line members primary number.
    #: example: +14088571272
    external: Optional[str] = None
    #: Line members extension.
    #: example: 3459
    extension: Optional[str] = None
    #: Last registration timestamp.
    #: example: 1611229671234
    last_registration_time: Optional[str] = None
    #: Registration host IP address for the line port.
    #: example: 10.0.0.45
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP address for the line port.
    #: example: 76.102.12.84
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Location object including a unique identifier for the location and its name.
    location: Optional[Location] = None
    #: Indicates member type.
    #: example: PEOPLE
    member_type: Optional[MemberType] = None


class DECTHandsetGet(ApiModel):
    #: Unique identifier of the handset.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX05FVC81NmRiMjRkMy03YTdhLTQwYTItOWFjOS1iMjMzMjc3OTIxTrd
    id: Optional[str] = None
    #: Index of the handset.
    #: example: 1
    index: Optional[str] = None
    #: Custom display name for the handset.
    #: example: Demo_Handset
    custom_display_name: Optional[str] = None
    #: Default display name for the handset.
    #: example: Demo_Handset
    default_display_name: Optional[str] = None
    #: Unique identifier of the associated base station.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX1NUQVRJT04vYzRhMTQxN2ItZGNiYi00MGMzLWE3YWQtNTY1MGZkZGRkNTNj
    base_station_id: Optional[str] = None
    #: MAC Address associated with the handset.
    #: example: 1357D4A1B492
    mac: Optional[str] = None
    #: Access code used to pair handsets to the DECT Network for the first time or if a handset becomes disconnected.
    #: example: 4788
    access_code: Optional[str] = None
    #: Array of lines associated with the handset. Maximum: 2 lines.
    lines: Optional[list[Lines]] = None


class DECTHandsetItem(ApiModel):
    #: Unique identifier of the handset.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX0hBTkRTRVQvYjE0MDYyOWUtZTExMy00ODQyLWIxMmMtMDVjODEwYTRjYjIz
    id: Optional[str] = None
    #: Index of the handset.
    #: example: 1
    index: Optional[str] = None
    #: Default display name for the handset.
    #: example: Demo_Handset
    default_display_name: Optional[str] = None
    #: Custom display name on the handset.
    #: example: Demo_Handset
    custom_display_name: Optional[str] = None
    #: Access code is used to pair handsets to the DECT Network for the first time or if a handset becomes
    #: disconnected.
    #: example: 4788
    access_code: Optional[str] = None
    #: Flags the handset as a primary line if `true`.
    #: example: True
    primary_enabled: Optional[bool] = None
    #: Array of lines associated to the handset up to a maximum of 2.
    lines: Optional[list[Lines]] = None


class DECTHandsetList(ApiModel):
    #: Number of handsets associated.
    #: example: 1
    number_of_handsets_assigned: Optional[int] = None
    #: Total number of lines assigned.
    #: example: 1
    number_of_lines_assigned: Optional[int] = None
    #: Array of `DECTHandsetItem` objects, each representing a handset with its associated details and lines.
    handsets: Optional[list[DECTHandsetItem]] = None


class BaseStationsResponse(ApiModel):
    #: Unique identifier of the base station.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Mac address of the DECT base station device.
    #: example: ABBD45856978
    mac: Optional[str] = None
    #: Number of handset member lines registered with the base station.
    #: example: 2
    number_of_lines_registered: Optional[int] = None


class DECTHandsetLineResponse(ApiModel):
    #: Unique identifier of the handset line member.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5RG
    member_id: Optional[str] = None
    #: First name of handset line member.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of handset line member.
    #: example: Smith
    last_name: Optional[str] = None
    #: Primary number of handset line member.
    #: example: +12555533333
    external: Optional[str] = None
    #: Extension of handset line member.
    #: example: 1551
    extension: Optional[str] = None
    #: Location details of the handset line member.
    location: Optional[Location] = None
    #: Indicates handset line member type.
    member_type: Optional[MemberType] = None


class HandsetsResponse(ApiModel):
    #: Unique identifier of the DECT handset.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5RG
    id: Optional[str] = None
    #: Display name of the DECT handset.
    #: example: Inventory-handset-1
    display_name: Optional[str] = None
    #: Access code for the DECT handset.
    #: example: 1558
    access_code: Optional[str] = None
    #: Details of the handset member lines registered with the base station. The maximum number of lines supported is
    #: 2.
    lines: Optional[list[DECTHandsetLineResponse]] = None


class BaseStationDetailResponse(ApiModel):
    #: Unique identifier of the base station.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Mac address of the DECT base station device.
    #: example: ABBD45856978
    mac: Optional[str] = None
    #: List of handset and member line details registered with the base station.
    handsets: Optional[list[HandsetsResponse]] = None


class BaseStationType(str, Enum):
    #: Cisco DBS210 base station model.
    dms_cisco_dbs210 = 'DMS Cisco DBS210'
    #: Cisco DBS110 base station model.
    dms_cisco_dbs110 = 'DMS Cisco DBS110'


class DECTNetworkDetail(ApiModel):
    #: Unique identifier for the DECT network.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX05FVC81NmRiMjRkMy03YTdhLTQwYTItOWFjOS1iMjMzMjc3OTIxNzf
    id: Optional[str] = None
    #: Name of the DECT network. This should be unique across the location.
    #: example: Demo-DectNetwork
    name: Optional[str] = None
    #: DECT network name displayed on the handset.
    #: example: Demo-DectNetwork
    display_name: Optional[str] = None
    #: Chain ID of the DECT network.
    #: example: 1356802345
    chain_id: Optional[int] = None
    #: Base station model deployed in the DECT network.
    #: example: DMS Cisco DBS210
    model: Optional[BaseStationType] = None
    #: Default access code is enabled. If true, the default access code is mandatory. If false, auto-generated access
    #: code is used.
    #: example: True
    default_access_code_enabled: Optional[bool] = None
    #: Default access code for the DECT network. The default access code should be unique within the same location to
    #: avoid the handset accidentally registering with base stations from different DECT networks in range. This is
    #: mandatory when `defaultAccessCodeEnabled` is true.
    #: example: 1234
    default_access_code: Optional[str] = None
    #: Number of base stations in the DECT network.
    #: example: 2
    number_of_base_stations: Optional[int] = None
    #: Number of handsets assigned to the DECT network.
    #: example: 5
    number_of_handsets_assigned: Optional[int] = None
    #: Number of lines in the DECT network.
    #: example: 2
    number_of_lines: Optional[int] = None
    #: Location of the DECT network.
    location: Optional[Location] = None


class DECTNetworkItem(ApiModel):
    #: Unique identifier for the DECT network.
    #: example: Y2lzY29zcGFyazovL3VzL0RFQ1RfREVWX05FVC81NmRiMjRkMy03YTdhLTQwYTItOWFjOS1iMjMzMjc3OTIxNzf
    id: Optional[str] = None
    #: Name of the DECT network. This should be unique across the location.
    #: example: Demo-DectNetwork
    name: Optional[str] = None
    #: Number of handsets assigned to the DECT network.
    #: example: 5
    number_of_handsets_assigned: Optional[int] = None


class SearchAvailableMembersUsageType(str, Enum):
    device_owner = 'DEVICE_OWNER'
    shared_line = 'SHARED_LINE'


class DECTDevicesSettingsApi(ApiChild, base='telephony/config'):
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
            the DECT network.  The corresponding device model display name sometimes called the product name, can also
            be used to specify the model.
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

    def get_the_list_of_dect_networks_for_an_organization(self, name: str = None, location_id: str = None,
                                                          org_id: str = None) -> list[DECTNetworkDetail]:
        """
        Get the List of DECT Networks for an organization

        Retrieves the list of DECT networks for an organization.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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

    def get_dect_network_details(self, location_id: str, dect_network_id: str,
                                 org_id: str = None) -> DECTNetworkDetail:
        """
        Get DECT Network Details

        Retrieves the details of a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

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
                            default_access_code: str, display_name: str = None, org_id: str = None):
        """
        Update DECT Network

        Update the details of a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if display_name is not None:
            body['displayName'] = display_name
        body['defaultAccessCodeEnabled'] = default_access_code_enabled
        body['defaultAccessCode'] = default_access_code
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}')
        super().put(url, params=params, json=body)

    def delete_dect_network(self, location_id: str, dect_network_id: str, org_id: str = None):
        """
        Delete DECT Network

        Delete a DECT network.

        DECT Networks provide roaming voice services via base stations and wireless handsets. A DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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

    def get_a_list_of_dect_network_base_stations(self, location_id: str, dect_network_id: str,
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

    def get_the_details_of_a_specific_dect_network_base_station(self, location_id: str, dect_network_id: str,
                                                                base_station_id: str,
                                                                org_id: str = None) -> BaseStationDetailResponse:
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
        :rtype: :class:`BaseStationDetailResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}')
        data = super().get(url, params=params)
        r = BaseStationDetailResponse.model_validate(data)
        return r

    def delete_bulk_dect_network_base_stations(self, location_id: str, dect_network_id: str, org_id: str = None):
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

    def delete_a_specific_dect_network_base_station(self, location_id: str, dect_network_id: str, base_station_id: str,
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

    def add_a_handset_to_a_dect_network(self, location_id: str, dect_network_id: str, line1_member_id: str,
                                        custom_display_name: str, line2_member_id: str = None, org_id: str = None):
        """
        Add a Handset to a DECT Network

        Add a handset to a DECT network in a location in an organization.

        Adding a handset to a DECT network requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <div><Callout type="warning">Adding a DECT handset to a person with a Webex Calling Standard license will
        disable Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

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

    def get_list_of_handsets_for_a_dect_network_id(self, location_id: str, dect_network_id: str,
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

    def get_specific_dect_network_handset_details(self, location_id: str, dect_network_id: str, handset_id: str,
                                                  org_id: str = None) -> DECTHandsetGet:
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
        r = DECTHandsetGet.model_validate(data)
        return r

    def update_dect_network_handset(self, location_id: str, dect_network_id: str, handset_id: str,
                                    line1_member_id: str, custom_display_name: str, line2_member_id: str = None,
                                    org_id: str = None):
        """
        Update DECT Network Handset

        Update the line assignment on a handset.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        Updating a DECT Network handset requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        <div><Callout type="warning">Adding a person with a Webex Calling Standard license to the DECT handset line1
        will disable Webex Calling across their Webex mobile, tablet, desktop, and browser applications.
        Removing a person with a Webex Calling Standard license from the DECT handset line1 will enable Webex Calling
        across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

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
        if line2_member_id is not None:
            body['line2MemberId'] = line2_member_id
        body['customDisplayName'] = custom_display_name
        url = self.ep(f'locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}')
        super().put(url, params=params, json=body)

    def delete_specific_dect_network_handset_details(self, location_id: str, dect_network_id: str, handset_id: str,
                                                     org_id: str = None):
        """
        Delete specific DECT Network Handset Details

        Delete a specific DECT Network handset.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        <div><Callout type="warning">Deleting a DECT handset from a person with a Webex Calling Standard license will
        enable Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

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

    def delete_multiple_handsets(self, location_id: str, dect_network_id: str, handset_ids: list[str],
                                 delete_all: bool = None, org_id: str = None):
        """
        Delete multiple handsets

        Delete multiple handsets or all of them.

        A handset can have up to two lines, and a DECT network supports a total of 120 lines across all handsets.
        A member on line1 of a DECT handset can be of type PEOPLE or PLACE while a member on line2 of a DECT handset
        can be of type PEOPLE, PLACE, or VIRTUAL_LINE.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        <div><Callout type="warning">Deleting a DECT handset from a person with a Webex Calling Standard license will
        enable Webex Calling across their Webex mobile, tablet, desktop, and browser applications.</Callout></div>

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

    def get_list_of_dect_networks_associated_with_a_person(self, person_id: str,
                                                           org_id: str = None) -> list[DECTNetworkItem]:
        """
        GET List of DECT networks associated with a Person

        Retrieves the list of DECT networks for a person in an organization.

        DECT Network provides roaming voice services via base stations and wireless handsets. DECT network can be
        provisioned up to 1000 lines across up to 254 base stations.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: List of DECT networks associated with this person.
        :type person_id: str
        :param org_id: List of DECT networks associated with a person in this organization.
        :type org_id: str
        :rtype: list[DECTNetworkItem]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DECTNetworkItem]).validate_python(data['dectNetworks'])
        return r

    def get_list_of_dect_networks_associated_with_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> list[DECTNetworkItem]:
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
        :rtype: list[DECTNetworkItem]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/dectNetworks')
        data = super().get(url, params=params)
        r = TypeAdapter(list[DECTNetworkItem]).validate_python(data['dectNetworks'])
        return r

    def search_available_members(self, member_name: str = None, phone_number: str = None, extension: str = None,
                                 order: str = None, location_id: str = None, exclude_virtual_line: bool = None,
                                 usage_type: SearchAvailableMembersUsageType = None, org_id: str = None,
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
        :param order: Sort the list of available members on the device in ascending order by name, using either last
            name `lname` or first name `fname`. Default sort is the last name in ascending order.
        :type order: str
        :param location_id: List members for the location ID.
        :type location_id: str
        :param exclude_virtual_line: If true, search results will exclude virtual lines in the member list. NOTE:
            Virtual lines cannot be assigned as the primary line.
        :type exclude_virtual_line: bool
        :param usage_type: Search for members eligible to become the owner of the device, or share line on the device.
        :type usage_type: SearchAvailableMembersUsageType
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
        if order is not None:
            params['order'] = order
        if location_id is not None:
            params['locationId'] = location_id
        if exclude_virtual_line is not None:
            params['excludeVirtualLine'] = str(exclude_virtual_line).lower()
        if usage_type is not None:
            params['usageType'] = enum_str(usage_type)
        url = self.ep('devices/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableMember, item_key='members', params=params)
