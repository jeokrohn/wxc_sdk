from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional, List

from pydantic import Field

from ...api_child import ApiChild
from ...base import ApiModel, to_camel
from ...common import RouteType, DialPatternValidate, Customer, PatternAction

__all__ = ['DialPlan', 'CreateResponse', 'PatternAndAction', 'DialPlanApi']


class DialPlan(ApiModel):
    #: Unique identifier for the dial plan.
    dial_plan_id: Optional[str] = Field(alias='id')
    #: A unique name for the dial plan.
    name: str
    #: ID of route type associated with the dial plan.
    route_id: str
    #: Name of route type associated with the dial plan.
    route_name: str
    #: Route Type associated with the dial plan.
    route_type: RouteType
    #: Customer information.
    customer: Optional[Customer]


class CreateResponse(ApiModel):
    dial_plan_id: str = Field(alias='id')
    dial_pattern_errors: list[DialPatternValidate]

    @property
    def ok(self) -> bool:
        return not self.dial_pattern_errors


class PatternAndAction(ApiModel):
    #: A unique dial pattern
    dial_pattern: str
    #: action to add or delete a pattern
    action: PatternAction

    @staticmethod
    def add(pattern: str) -> 'PatternAndAction':
        return PatternAndAction(dial_pattern=pattern,
                                action=PatternAction.add)

    @staticmethod
    def delete(pattern: str) -> 'PatternAndAction':
        return PatternAndAction(dial_pattern=pattern,
                                action=PatternAction.delete)


@dataclass(init=False)
class DialPlanApi(ApiChild, base='telephony/config/premisePstn/dialPlans'):

    def list(self, *, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None,
             order: str = None, org_id: str = None, **params) -> Generator[DialPlan, None, None]:
        """
        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the trunk name.
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return:
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        url = self.ep()
        return self.session.follow_pagination(url=url, model=DialPlan, params=params, item_key='dialPlans')

    def create(self, *, name: str, route_id: str, route_type: RouteType, dial_patterns: List[str] = None,
               org_id: str = None) -> CreateResponse:
        """
        Create a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Creating a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: :class:`wxc_sdk.common.RouteType`
        :param dial_patterns: An Array of dial patterns
        :type dial_patterns: list[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: result of dial plan creation
        :rtype: :class:`CreateResponse`
        """
        url = self.ep()
        params = org_id and {'orgId': org_id} or None
        body = {
            'name': name,
            'routeId': route_id,
            'routeType': route_type.value if isinstance(route_type, RouteType) else route_type,
            'dialPatterns': dial_patterns or []
        }
        data = self.post(url=url, params=params, json=body)
        return CreateResponse.parse_obj(data)

    def details(self, *, dial_plan_id: str, org_id: str = None) -> DialPlan:
        """
        Get a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving a dial plan requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: dial plan details
        :rtype: :class:`DialPlan`
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return DialPlan.parse_obj(data)

    def update(self, *, update: DialPlan, org_id: str = None):
        """
        Modify a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param update: DialPlan objects with updated settings. Only name, route_id and route_type are considered. All
            three need to be set
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(update.dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name', 'route_id', 'route_type'})
        self.put(url=url, params=params, data=body)

    def delete_dial_plan(self, *, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url=url, params=params)

    def patterns(self, *, dial_plan_id: str, org_id: str = None,
                 dial_pattern: str = None, **params) -> Generator[str, None, None]:
        """
        List all Dial Patterns for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: List dial patterns associated with a dial plan.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and
            X (matches a single digit, 0-9).
            The ! wildcard can only occur once at the end and only in an E.164 pattern
        :return: list of patterns
        :rtype: list[str]
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i > 1 and v is not None and p != 'params')
        url = self.ep(f'{dial_plan_id}/dialPatterns')

        return self.session.follow_pagination(url=url, params=params, item_key='dialPatterns')

    def modify_patterns(self, *, dial_plan_id: str, dial_patterns: List[PatternAndAction], org_id: str = None):
        """
        Modify dial patterns for the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the
            request is not modified.
        :type dial_patterns: :class:`PatternAndAction`
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            dial_patterns: list[PatternAndAction]

        body = Body(dial_patterns=dial_patterns).json()
        self.put(url=url, params=params, data=body)

    def delete_all_patterns(self, *, dial_plan_id: str, org_id: str = None):
        """
        Delete all dial patterns from the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllDialPatterns': True}
        self.put(url=url, params=params, json=body)
