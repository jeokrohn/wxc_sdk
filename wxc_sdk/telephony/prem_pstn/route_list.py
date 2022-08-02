from collections.abc import Generator
from dataclasses import dataclass
from typing import List

from pydantic import Field, parse_obj_as

from ...api_child import ApiChild
from ...base import to_camel, ApiModel
from ...common import IdAndName, PatternAction

__all__ = ['RouteListDetail', 'RouteList', 'NumberAndAction', 'UpdateNumbersResponse', 'RouteListApi']


class RouteListDetail(ApiModel):
    rl_id: str = Field(alias='id')
    name: str
    location: IdAndName
    route_group: IdAndName


class RouteList(ApiModel):
    rl_id: str = Field(alias='id')
    name: str
    location_id: str
    location_name: str
    rg_id: str = Field(alias='routeGroupId')
    rg_name: str = Field(alias='routeGroupName')


class NumberAndAction(ApiModel):
    #: A unique dial pattern
    number: str
    #: action to add or delete a pattern
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
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteList)

    def create(self, *, name: str, location_id: str, rg_id: str, org_id: str = None) -> str:
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'locationId': location_id,
                'routeGroupId': rg_id}
        url = self.ep()
        data = self.post(url=url, params=params, json=body)
        return data['id']

    def details(self, *, rl_id: str, org_id: str = None) -> RouteListDetail:
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        data = self.get(url=url, params=params)
        return RouteListDetail.parse_obj(data)

    def update(self, *, rl_id: str, name: str, location_id: str, rg_id: str, org_id: str = None) -> str:
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'locationId': location_id,
                'routeGroupId': rg_id}
        url = self.ep(rl_id)
        self.put(url=url, params=params, json=body)

    def delete_route_list(self, *, rl_id: str, org_id: str = None):
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        self.delete(url=url, params=params)

    def numbers(self, *, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> Generator[str, None, None]:
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        return self.session.follow_pagination(url=url, params=params)

    def update_numbers(self, *, rl_id: str, numbers: List[NumberAndAction],
                       org_id: str = None) -> List[UpdateNumbersResponse]:
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
