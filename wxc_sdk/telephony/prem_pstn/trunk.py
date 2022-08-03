from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import List, Any, Optional

from pydantic import parse_obj_as, Field

from ...api_child import ApiChild
from ...base import to_camel, ApiModel
from ...common import Customer, IdAndName

__all__ = ['TrunkLocation', 'TrunkType', 'Trunk', 'TrunkDeviceType', 'TrunkTypeWithDeviceType', 'DeviceStatus',
           'ResponseStatusType', 'ResponseStatus', 'OutboundProxy', 'TrunkDetail', 'TrunkUsage', 'TrunkApi']


class TrunkLocation(ApiModel):
    location_id: str = Field(alias='id')
    name: str


class TrunkType(str, Enum):
    #: for Cisco CUBE Local Gateway
    registering = 'REGISTERING'
    #: for Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller,
    #:  Ribbon Session Border Controller
    certificate_base = 'CERTIFICATE_BASED'


class Trunk(ApiModel):
    trunk_id: str = Field(alias='id')
    name: str
    location: TrunkLocation
    in_use: bool
    trunk_type: TrunkType


class TrunkDeviceType(ApiModel):
    #: Device type associated with trunk configuration
    device_type: str
    #: Min Concurrent call. Required for static certificate based trunk.
    min_concurrent_calls: int
    #: Max Concurrent call. Required for static certificate based trunk.
    max_concurrent_calls: int


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunk_type: TrunkType
    #: Device types for trunk configuration
    device_types: list[TrunkDeviceType]


class DeviceStatus(str, Enum):
    online = 'online'
    offline = 'offline'
    unknown = 'unknown'


class ResponseStatusType(str, Enum):
    error = 'ERROR'
    warning = 'WARNING'


class ResponseStatus(ApiModel):
    #: Error Code. 25013 for error retrieving the outbound proxy. 25014 for error retrieving the status
    code: int
    response_status_type: ResponseStatusType = Field(alias='type')
    summary_english: str
    detail: list[str]
    tracking_id: str


class OutboundProxy(ApiModel):
    sip_access_service_type: str
    dns_type: str
    outbound_proxy: str
    srv_prefix: str
    cname_records: Any
    attachment_updated: bool


class TrunkDetail(ApiModel):
    trunk_id: str = Field(alias='id')
    name: str
    #: Customer associated with the trunk.
    organization: Customer
    #: Location associated with the trunk.
    location: TrunkLocation
    #: Unique Outgoing and Destination trunk group associated with the dial plan.
    otg_dtg_id: str
    #: The Line/Port identifies a device endpoint in standalone mode or a SIPURI public identity in IMS mode.
    line_port: str
    locations_using_trunk: list[TrunkLocation]
    pilot_user_id: str
    outbound_proxy: OutboundProxy
    #: User's authentication service information.
    sip_authentication_user_name: str
    status: DeviceStatus
    error_codes: list[str] = Field(default_factory=list)
    #: Present partial error/warning status information included when the http response is 206.
    response_status: list[ResponseStatus]
    #: Determines the behavior of the From and PAI headers on outbound calls.
    dual_identity_support_enabled: bool
    #: Trunk Type associated with the trunk.
    trunk_type: TrunkType
    #: Device type assosiated with trunk.
    device_type: str
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    address: Optional[str]
    #: Domain name. Required to create a static certificate based trunk
    domain: Optional[str]
    #: FQDN port. Required to create a static certificate-based trunk.
    port: Optional[int]
    #: Max Concurrent call. Required to create a static certificate based trunk.
    max_concurrent_calls: int


class TrunkUsage(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    pstn_connection_count: int
    #: The count where the given local gateway is used as call to extension setting.
    call_to_extension_count: int
    dial_plan_count: int
    route_group_count: int


@dataclass(init=False)
class TrunkApi(ApiChild, base='telephony/config/premisePstn/trunks'):
    """
    API for everything trunks
    """

    def list(self, *, name: str = None, location_name: str = None, trunk_type: str = None, order: str = None,
             org_id: str = None, **params) -> Generator[Trunk, None, None]:
        """
        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        ebex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: str
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: str
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id:
        :type org_id: str
        :return: generator of Trunk instances
        :rtype: :class:`Trunk`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=Trunk, item_key='trunks')

    def create(self, *, name: str, location_id: str, password: str, trunk_type: TrunkType,
               dual_identity_support_enabled: bool = None, device_type: TrunkDeviceType = None, address: str = None,
               domain: str = None, port: int = None, max_concurrent_calls: int = None, org_id: str = None) -> str:
        """
        Create a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Creating a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param name: A unique name for the trunk.
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param device_type: Device type associated with trunk.
        :type device_type: :class:`TrunkDeviceType`
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id of new trunk
        :rtype: str
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = self.post(url=url, params=params, json=body)
        return data['id']

    def details(self, *, trunk_id: str, org_id: str = None) -> TrunkDetail:
        """
        Get a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving a trunk requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: trunk details
        :rtype: :class:`TrunkDetail`
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return TrunkDetail.parse_obj(data)

    def update(self, *, trunk_id: str, name: str, location_id: str, password: str, trunk_type: TrunkType,
               dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None, org_id: str = None):
        """
        Modify a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Modifying a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id:
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str:return:
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        self.put(url=url, params=params, json=body)

    def delete_trunk(self, *, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Deleting a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url=url, params=params)

    def trunk_types(self, org_id: str = None) -> List[TrunkTypeWithDeviceType]:
        """
        List all TrunkTypes with DeviceTypes for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy. Trunk Types are Registering
        or Certificate Based and are configured in CallManager.

        Retrieving trunk types requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id:
        :return: trunk types
        :rtype: list[:class:`TrunkTypeWithDeviceType`]
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep('trunkTypes')
        data = self.get(url=ep, params=params)
        return parse_obj_as(list[TrunkTypeWithDeviceType], data['trunkTypes'])

    def usage(self, *, trunk_id: str, org_id: str = None) -> TrunkUsage:
        """
        Get Local Gateway Usage Count

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: usage counts
        :rtype: :class:`TrunkUsage`
        """
        url = self.ep(f'{trunk_id}/usage')
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return TrunkUsage.parse_obj(data)

    def usage_dial_plan(self, *, trunk_id: str, org_id: str = None) -> Generator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def usage_location_pstn(self, *, trunk_id: str, org_id: str = None) -> Generator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with
        a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks
        that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def usage_route_group(self, *, trunk_id: str, org_id: str = None) -> Generator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageRouteGroup')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def validate_fqdn_and_domain(self):
        # TODO: implement
        ...

    # TODO: are we missing a usage for trunks used for calls to unknown extensions??
    # TODO: are we missing a usage for route lists??
