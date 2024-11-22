from collections.abc import Generator
from typing import Optional, Any

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['CustomerExperienceEssentialsApi', 'ScreenPopConfiguration']

from wxc_sdk.telephony.callqueue import AvailableAgent


class ScreenPopConfiguration(ApiModel):
    #: Enable/disable screen pop.
    enabled: Optional[bool] = None
    #: The screen pop URL that integrates Webex calls with other business apps like CRM, ticketing tools, and order
    #: entry systems.
    screen_pop_url: Optional[str] = None
    #: A label for the screen pop configuration.
    desktop_label: Optional[str] = None
    #: The query parameters for the screen pop URL.
    query_params: Optional[dict[str, Any]] = None


class CustomerExperienceEssentialsApi(ApiChild, base='telephony/config/locations'):
    """
    Customer Experience Essentials

    Webex Customer Experience Essentials APIs provide the core capabilities of the Webex Contact Center solution. These
    APIs allow you to
    manage Customer Experience Essentials features such as supervisor configuration, agent configuration, and call
    queue configuration, which are distinct from the Customer Experience Basic suite.

    `Learn more about the customer Experience Essentials suite.
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_

    Viewing the read-only customer Experience Essentials APIs requires a full, device or read-only administrator auth
    token with a scope of `spark-admin:telephony_config_read`.

    Modifying the customer Experience Essentials APIs requires a full or device administrator auth token with a scope
    of `spark-admin:telephony_config_write`.
    """

    def get_screen_pop_configuration(self, location_id: str = None,
                                     queue_id: str = None, org_id: str = None) -> ScreenPopConfiguration:
        """
        Get Screen Pop configuration for a Call Queue in a Location

        Screen pop lets agents view customer-related info in a pop-up window. This API returns the screen pop
        configuration for a call queue in a location.

        :param location_id: The location ID where the call queue resides.
        :type location_id: str
        :param queue_id: The call queue ID for which screen pop configuration is modified.
        :type queue_id: str
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        data = super().get(url, params=params)
        return ScreenPopConfiguration.model_validate(data)

    def modify_screen_pop_configuration(self, location_id: str,
                                        queue_id: str, settings: ScreenPopConfiguration, org_id: str = None):
        """
        Modify Screen Pop configuration for a Call Queue in a Location

        Screen pop lets agents view customer-related info in a pop-up window. This API allows you to modify the screen
        pop configuration for a call queue in a location.

        :param location_id: The location ID where the call queue resides.
        :type location_id: str
        :param queue_id: The call queue ID for which screen pop configuration is modified.
        :type queue_id: str
        :param settings: The screen pop configuration settings.
        :type settings: ScreenPopConfiguration
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.model_dump(mode='json', by_alias=True)
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        super().put(url, params=params, json=body)

    def available_agents(self, location_id: str,
                         has_cx_essentials: bool = None,
                         org_id: str = None) -> Generator[AvailableAgent, None, None]:
        """
        Get List of available agents for Customer Experience Essentials

        Retrieve the list of available agents with Customer Experience Essentials license in a location.

        This operation requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the list of avaiilable agents in this location.
        :type location_id: str
        :param has_cx_essentials: Returns only the list of available agents with Customer Experience Essentials license
            when `true`, otherwise returns the list of available agents with Customer Experience Basic license.
        :type has_cx_essentials: bool
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableAgent` instances
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'{location_id}/cxEssentials/agents/availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgent, item_key='agents',
                                              params=params)
