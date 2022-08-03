from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from ...api_child import ApiChild
from ...base import to_camel, ApiModel
from ...common import Customer, IdAndName

__all__ = ['RGTrunk', 'RouteGroup', 'RouteGroupUsage', 'UsageRouteLists', 'RouteGroupApi']


class RGTrunk(ApiModel):
    trunk_id: str = Field(alias='id')
    name: Optional[str]
    location_id: Optional[str]
    priority: int


class RouteGroup(ApiModel):
    # only returned in list() not in detail
    rg_id: Optional[str] = Field(alias='id')
    name: str
    # TODO: doc defect not listed at https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read
    #  -the-list-of-routing-groups
    #: only returned by list() not as part of detail
    in_use: Optional[bool]
    #: only returned by detail()
    organization: Optional[Customer]
    #: only returned by detail()
    local_gateways: Optional[list[RGTrunk]]


class RouteGroupUsage(ApiModel):
    #: Number of PSTN connection locations associated to this route group.
    pstn_connection_count: int
    #: Number of call to extension locations associated to this route group.
    call_to_extension_count: int
    #: Number of dial plan locations associated to this route group.
    dial_plan_count: int
    #: Number of route list locations associated to this route group.
    route_list_count: int


class UsageRouteLists(ApiModel):
    rl_id: str = Field(alias='id')
    rl_name: str = Field(alias='name')
    location_id: str
    location_name: str


@dataclass(init=False)
class RouteGroupApi(ApiChild, base='telephony/config/premisePstn/routeGroups'):
    """
    API for everything route groups
    """

    def list(self, *, name: str = None, order: str = None,
             org_id: str = None, **params) -> Generator[RouteGroup, None, None]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of route groups matching the route group name.
        :type name: st
        :param order: Order the route groups according to designated fields. Available sort orders: asc, desc.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: generator of :class:`RouteGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteGroup)

    def create(self, *, route_group: RouteGroup, org_id: str = None) -> str:
        """
        Creates a Route Group for the organization.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Creating a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param route_group: settings for new route group. name and local_gateways need to be set. For each LGW
            id and priority need to be set.
            Example:

            .. code-block:: python

                rg = RouteGroup(name=rg_name,
                        local_gateways=[RGTrunk(trunk_id=trunk.trunk_id,
                                                priority=1)])
                rg_id = api.telephony.prem_pstn.route_group.create(route_group=rg)
        :type route_group: :class:`RouteGroup`
        :param org_id:
        :type org_id: str
        :return: id of new route group
        :rtype: str
        """
        # TODO: doc defect. wrong URL at https://developer.webex.com/docs/api/v1/webex-calling-organization-settings
        #  /create-route-group-for-a-organization
        params = org_id and {'orgId': org_id} or None
        body = route_group.json(include={'name': True,
                                         'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep()
        data = self.post(url=url, params=params, data=body)
        return data['id']

    def details(self, *, rg_id: str, org_id: str = None) -> RouteGroup:
        """
        Reads a Route Group for the organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Reading a Route Group requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route Group for which details are being requested.
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: route group details
        :rtype: :class:`RouteGroup`
        """
        # TODO: wrong data structure at
        #  https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-a-route-group-for-a
        #  -organization
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        data = self.get(url=url, params=params)
        return RouteGroup.parse_obj(data)

    def update(self, *, rg_id: str, update: RouteGroup, org_id: str = None):
        """
        Modifies an existing Route Group for an organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Modifying a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: route group to be modified
        :type rg_id: str
        :param update: new settings
        :type update: :class:`RouteGroup`
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name': True,
                                    'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep(rg_id)
        data = self.post(url=url, params=params, data=body)
        self.put(url=url, params=params, data=data)

    def delete_route_group(self, *, rg_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Removing a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: Route Group to be deleted
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        # TODO: doc defect. wrong URL
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        self.delete(url=url, params=params)

    def usage(self, *, rg_id: str, org_id: str = None) -> RouteGroupUsage:
        """
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
        specific Route Group. Users within Call to Extension locations are registered to a PBX which allows you to
        route unknown extensions (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route
        Group. PSTN Connections may be cisco PSTN, cloud-connected PSTN, or premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group. Route Lists are
        a list of numbers that can be reached via a route group. It can be used to provide cloud PSTN connectivity to
        Webex Calling Dedicated Instance.

        Retrieving usage information requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :type rg_id: str
        :param org_id: Organization associated with specific route group
        :type org_id: str
        :return: usage information
        :rtype: :class:`RouteGroupUsage`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{rg_id}/usage')
        data = self.get(url=url, params=params)
        return RouteGroupUsage.parse_obj(data)

    def usage_call_to_extension(self, rg_id: str, org_id: str = None, **params) -> Generator[IdAndName, None, None]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to
        the PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageCallToExtension')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def usage_dial_plan(self, rg_id: str, org_id: str = None, **params) -> Generator[IdAndName, None, None]:
        """
        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location. A Dial Plan also
        specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def usage_location_pstn(self, rg_id: str, org_id: str = None, **params) -> Generator[IdAndName, None, None]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    def usage_route_lists(self, rg_id: str, org_id: str = None, **params) -> Generator[UsageRouteLists, None, None]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a
        Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageRouteList')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=UsageRouteLists, params=params)
