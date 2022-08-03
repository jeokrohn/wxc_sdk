from collections.abc import Generator
from dataclasses import dataclass
from typing import List

from pydantic import Field, parse_obj_as

from ...api_child import ApiChild
from ...base import to_camel, ApiModel
from ...common import IdAndName, PatternAction

__all__ = ['RouteListDetail', 'RouteList', 'NumberAndAction', 'UpdateNumbersResponse', 'RouteListApi']


class RouteListDetail(ApiModel):
    #: UUID of the Route List.
    rl_id: str = Field(alias='id')
    #: Route list name
    name: str
    #: Location associated with the Route List
    location: IdAndName
    #: Route group associated with the Route list.
    route_group: IdAndName


class RouteList(ApiModel):
    #: UUID of the Route List.
    rl_id: str = Field(alias='id')
    #: Name of the Route List.
    name: str
    #: Location associated with the Route List.
    location_id: str
    #: Location associated with the Route List.
    location_name: str
    #: UUID of the route group associated with Route List.
    rg_id: str = Field(alias='routeGroupId')
    #: Name of the Route Group associated with Route List.
    rg_name: str = Field(alias='routeGroupName')


class NumberAndAction(ApiModel):
    #: Number to be deleted/added
    number: str
    #: action to add or delete a number
    action: PatternAction

    @staticmethod
    def add(number: str) -> 'NumberAndAction':
        return NumberAndAction(number=number,
                               action=PatternAction.add)

    @staticmethod
    def delete(number: str) -> 'NumberAndAction':
        return NumberAndAction(number=number,
                               action=PatternAction.delete)


class UpdateNumbersResponse(ApiModel):
    number: str
    number_status: str
    message: str


@dataclass(init=False)
class RouteListApi(ApiChild, base='telephony/config/premisePstn/routeLists'):
    """
    API for everything route lists
    """

    def list(self, *, name: list[str] = None, location_id: list[str] = None, order: str = None,
             org_id: str = None, **params) -> Generator[RouteList, None, None]:
        """
        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of Route List matching the route list name.
        :type name: str
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: str
        :param order: Order the Route List according to the designated fields.Available sort fields: name, locationId.
            Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: generator yielding :class:`RouteList` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteList)

    def create(self, *, name: str, location_id: str, rg_id: str, org_id: str = None) -> str:
        """
        Create a Route List for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Creating a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: Name of the Route List
        :type name: str
        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param rg_id: UUID of the route group associated with Route List.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: ID of the newly route list created.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'locationId': location_id,
                'routeGroupId': rg_id}
        url = self.ep()
        data = self.post(url=url, params=params, json=body)
        return data['id']

    def details(self, *, rl_id: str, org_id: str = None) -> RouteListDetail:
        """
        Get Route List Details.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: route list details
        :rtype: :class:`RouteListDetail`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        data = self.get(url=url, params=params)
        return RouteListDetail.parse_obj(data)

    def update(self, *, rl_id: str, name: str, rg_id: str, org_id: str = None):
        """
        Modify the details for a Route List.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param name: Route List new name.
        :type name: str
        :param rg_id: New route group id.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'routeGroupId': rg_id}
        url = self.ep(rl_id)
        self.put(url=url, params=params, json=body)

    def delete_route_list(self, *, rl_id: str, org_id: str = None):
        """
        Delete Route List for a Customer

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Deleting a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        self.delete(url=url, params=params)

    def numbers(self, *, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> Generator[str, None, None]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param order: Order the Route Lists according to number.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: generator yielding str
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params)

    def update_numbers(self, *, rl_id: str, numbers: List[NumberAndAction],
                       org_id: str = None) -> List[UpdateNumbersResponse]:
        """
        Modify numbers for a specific Route List of a Customer.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: list[:class:`NumberAndAction`]
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: list of update number status
        :rtype: list[:class:`UpdateNumbersResponse`]
        """
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            numbers: list[NumberAndAction]

        body = Body(numbers=numbers).json()
        data = self.put(url=url, params=params, data=body)
        if data:
            return parse_obj_as(list[UpdateNumbersResponse], data['numberStatus'])
        else:
            return []

    def delete_all_numbers(self, *, rl_id: str, org_id: str = None):
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllNumbers': True}
        self.put(url=url, params=params, json=body)
