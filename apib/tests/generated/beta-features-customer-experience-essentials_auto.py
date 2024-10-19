from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCustomerExperienceEssentialsApi', 'GetAvailableAgentsCallQueueObject',
           'GetAvailableAgentsCallQueueObjectPhoneNumbers', 'UserType']


class GetAvailableAgentsCallQueueObjectPhoneNumbers(ApiModel):
    #: External phoneNumber of the agent.
    #: example: 12143456103
    external: Optional[str] = None
    #: Extension of the agent.
    #: example: 23234
    extension: Optional[str] = None


class UserType(str, Enum):
    #: Associated type is a person.
    people = 'PEOPLE'
    #: Associated type is a workspace.
    place = 'PLACE'
    #: Associated type is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetAvailableAgentsCallQueueObject(ApiModel):
    #: Unique agent identifier.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzE3NzczMWRiLWE1YzEtNGI2MC05ZTMwLTNhM2MxMGFiM2IxMQ
    id: Optional[str] = None
    #: Last name of the agent assigned to the particular location.
    #: example: Smith
    last_name: Optional[str] = None
    #: First name of the agent assigned to the particular location. Defaults to ".".
    #: example: John
    first_name: Optional[str] = None
    #: (string, optional) - Display name of the agent.
    #: example: John Smith
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    #: example: PEOPLE
    type: Optional[UserType] = None
    #: Email of the agent.
    #: example: johnSmith@gmail.com
    email: Optional[str] = None
    #: Denotes whether the agent has Customer Experience Essentials license.
    #: example: True
    has_cx_essentials: Optional[bool] = None
    #: Phone number and extension of the agent.
    phone_numbers: Optional[GetAvailableAgentsCallQueueObjectPhoneNumbers] = None


class BetaFeaturesCustomerExperienceEssentialsApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features: Customer Experience Essentials
    
    Webex Customer Experience Essentials APIs provide the core capabilities of the Webex Contact Center solution. These
    APIs allow you to
    manage Customer Experience Essentials features such as supervisor configuration, agent configuration, and call
    queue configuration, which are distinct from the Customer Experience Basic suite.
    
    `Learn more about the customer Experience Essentials suite.
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_
    
    Viewing the read-only customer Experience Essentials APIs requires a full, device or read-only administrator auth
    token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying the customer Experience Essentials APIs requires a full or device administrator auth token with a scope
    of
    `spark-admin:telephony_config_write`.
    """

    def get_screen_pop_configuration_for_a_call_queue_in_a_location(self, location_id: str = None,
                                                                    queue_id: str = None, org_id: str = None):
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
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/screenPop?orgId={org_id}')
        super().get(url)

    def modify_screen_pop_configuration_for_a_call_queue_in_a_location(self, location_id: str = None,
                                                                       queue_id: str = None, enabled: bool = None,
                                                                       screen_pop_url: str = None,
                                                                       desktop_label: str = None,
                                                                       query_params: Any = None, org_id: str = None):
        """
        Modify Screen Pop configuration for a Call Queue in a Location

        Screen pop lets agents view customer-related info in a pop-up window. This API allows you to modify the screen
        pop configuration for a call queue in a location.

        :param location_id: The location ID where the call queue resides.
        :type location_id: str
        :param queue_id: The call queue ID for which screen pop configuration is modified.
        :type queue_id: str
        :param enabled: Enable/disable screen pop.
        :type enabled: bool
        :param screen_pop_url: The screen pop URL that integrates Webex calls with other business apps like CRM,
            ticketing tools, and order entry systems.
        :type screen_pop_url: str
        :param desktop_label: A label for the screen pop configuration.
        :type desktop_label: str
        :param query_params: JSON string containing the query parameters for the screen pop URL.
        :type query_params: Any
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if screen_pop_url is not None:
            body['screenPopUrl'] = screen_pop_url
        if desktop_label is not None:
            body['desktopLabel'] = desktop_label
        if query_params is not None:
            body['queryParams'] = query_params
        url = self.ep(f'{location_id}/queues/{queue_id}/cxEssentials/screenPop?orgId={org_id}')
        super().put(url, json=body)

    def get_list_of_available_agents_for_customer_experience_essentials(self, location_id: str,
                                                                        has_cx_essentials: bool = None,
                                                                        org_id: str = None) -> list[GetAvailableAgentsCallQueueObject]:
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
        :rtype: list[GetAvailableAgentsCallQueueObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if has_cx_essentials is not None:
            params['hasCxEssentials'] = str(has_cx_essentials).lower()
        url = self.ep(f'{location_id}/cxEssentials/agents/availableAgents')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetAvailableAgentsCallQueueObject]).validate_python(data['agents'])
        return r
