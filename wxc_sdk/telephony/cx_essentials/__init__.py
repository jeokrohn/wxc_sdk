from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.rest import RestSession

__all__ = ['CustomerExperienceEssentialsApi', 'ScreenPopConfiguration']

from wxc_sdk.telephony.callqueue import AvailableAgent
from wxc_sdk.telephony.cx_essentials.callqueue_recording import QueueCallRecordingSettingsApi
from wxc_sdk.telephony.cx_essentials.wrapup_reasons import WrapupReasonApi


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


@dataclass(init=False, repr=False)
class CustomerExperienceEssentialsApi(ApiChild, base='telephony/config'):
    """
    Features: Customer Assist
    Features: Customer Assist

    Webex Customer Assist APIs provide the core capabilities of the Webex Contact Center solution. These APIs allow you
    to
    manage Customer Assist features such as supervisor configuration, agent configuration, and call queue
    configuration, which are distinct from the Customer Experience Basic suite.

    `Learn more about the Customer Assist suite.
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_

    Viewing the read-only Customer Assist APIs requires a full, device or read-only administrator auth token with a
    scope of
    `spark-admin:telephony_config_read`.

    Modifying the Customer Assist APIs requires a full or device administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    Webex Customer Experience Basic is an offering available as part of the Webex Suite or Webex Calling Professional
    license at no additional cost.
    It includes a simple and powerful set of features which are bundled together to deliver the call center
    functionalities.
    The features such as Voice Queues, skill-based routing, call queue monitoring and analytics, multi call window, and
    more, help users to engage with customers efficiently.
    Also, with our Webex Calling for Microsoft Teams integration, the Microsoft Teams users can access the features
    directly from Teams.

    Webex Customer Assist provides the fundamental capabilities of the Webex Contact Center solution.
    It includes all the Webex Calling professional capabilities, Customer Experience Basic features, and some
    additional key features accessible through the Webex App for both agents and supervisors.
    The features like screen pop, supervisor experience in Webex App, and real-time and historical agent and queue view
    make the Customer Assist distinct from Customer Experience Basic.

    Webex Customer Assist APIs allows you to manage Customer Assist features such as supervisor configuration, agent
    configuration, and call queue configuration, which are distinct from Customer Experience Basic.

    `Learn more about the Customer Assist suite
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_
    `Learn more about the customer Experience Basic suite
    <https://help.webex.com/en-us/article/nzkg083/Webex-Customer-Experience-Basic>`_
    """

    callqueue_recording: QueueCallRecordingSettingsApi
    wrapup_reasons: WrapupReasonApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.callqueue_recording = QueueCallRecordingSettingsApi(session=session)
        self.wrapup_reasons = WrapupReasonApi(session=session)

    def get_screen_pop_configuration(
        self, location_id: str = None, queue_id: str = None, org_id: str = None
    ) -> ScreenPopConfiguration:
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        data = super().get(url, params=params)
        return ScreenPopConfiguration.model_validate(data)

    def modify_screen_pop_configuration(
        self, location_id: str, queue_id: str, settings: ScreenPopConfiguration, org_id: str = None
    ):
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        super().put(url, params=params, json=body)

    def available_agents(
        self, location_id: str, has_cx_essentials: bool = None, org_id: str = None
    ) -> Generator[AvailableAgent, None, None]:
        """
        List Available Agents

        Return a list of available agents with Customer Assist license in a location.

        Retrieving the list of available agents requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the list of avaiilable agents in this location.
        :type location_id: str
        :param has_cx_essentials: Returns only the list of available agents with Customer Assist license when `true`,
            otherwise returns the list of available agents with Customer Experience Basic license.
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
        url = self.ep(f'locations/{location_id}/cxEssentials/agents/availableAgents')
        return self.session.follow_pagination(url=url, model=AvailableAgent, item_key='agents', params=params)
