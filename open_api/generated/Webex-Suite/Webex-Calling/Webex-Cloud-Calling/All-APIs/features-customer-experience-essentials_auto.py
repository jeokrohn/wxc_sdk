from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['FeaturesCustomerExperienceEssentialsApi', 'GetAvailableAgentsCallQueueObject',
           'GetAvailableAgentsCallQueueObjectPhoneNumbers', 'GetScreenPopConfigurationObject', 'QueryParamsObject',
           'QueueObject', 'QueueObjectWithDefaultEnabled', 'QueueWrapUpReasonObject',
           'ReadWrapUpReasonSettingsResponse', 'UserType', 'WrapUpReasonDetailsObject', 'WrapUpReasonObject']


class QueryParamsObject(ApiModel):
    #: An example key-value pair that will be sent to the agent.
    example_param_1: Optional[str] = Field(alias='example_param_1', default=None)
    #: Another example key-value pair that will be sent to the agent.
    example_param_2: Optional[str] = Field(alias='example_param_2', default=None)
    #: Another example key-value pair that will be sent to the agent.
    example_param_3: Optional[str] = Field(alias='example_param_3', default=None)


class GetScreenPopConfigurationObject(ApiModel):
    #: Enable/disable screen pop.
    enabled: Optional[bool] = None
    #: The screen pop URL that integrates Webex calls with other business apps like CRM, ticketing tools, and order
    #: entry systems.
    screen_pop_url: Optional[str] = None
    #: A label for the screen pop configuration.
    desktop_label: Optional[str] = None
    #: The additional user-defined key-value pairs that must be sent to the agent.
    query_params: Optional[QueryParamsObject] = None


class GetAvailableAgentsCallQueueObjectPhoneNumbers(ApiModel):
    #: External phoneNumber of the agent.
    external: Optional[str] = None
    #: Extension of the agent.
    extension: Optional[str] = None


class UserType(str, Enum):
    #: Associated entity is a person.
    people = 'PEOPLE'
    #: Associated entity is a workspace.
    place = 'PLACE'
    #: Associated entity is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetAvailableAgentsCallQueueObject(ApiModel):
    #: Unique agent identifier.
    id: Optional[str] = None
    #: Last name of the agent assigned to the particular location.
    last_name: Optional[str] = None
    #: First name of the agent assigned to the particular location. Defaults to ".".
    first_name: Optional[str] = None
    #: (string, optional) - Display name of the agent.
    display_name: Optional[str] = None
    #: Type of the person, workspace or virtual line.
    type: Optional[UserType] = None
    #: Email of the agent.
    email: Optional[str] = None
    #: Denotes whether the agent has Customer Experience Essentials license.
    has_cx_essentials: Optional[bool] = None
    #: Phone number and extension of the agent.
    phone_numbers: Optional[GetAvailableAgentsCallQueueObjectPhoneNumbers] = None


class WrapUpReasonObject(ApiModel):
    #: Unique wrap-up identifier.
    id: Optional[str] = None
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Number of queues assigned to the wrap-up reason.
    number_of_queues_assigned: Optional[int] = None


class QueueObjectWithDefaultEnabled(ApiModel):
    #: Unique queue identifier.
    id: Optional[str] = None
    #: Name of the queue.
    name: Optional[str] = None
    #: Name of the location.
    location_name: Optional[str] = None
    #: Unique location identifier.
    location_id: Optional[str] = None
    #: Phone number of the queue.
    phone_number: Optional[str] = None
    #: Extension of the queue.
    extension: Optional[int] = None
    #: Denotes whether the default wrap-up is enabled for the queue.
    default_wrapup_enabled: Optional[bool] = None


class WrapUpReasonDetailsObject(ApiModel):
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Number of queues assigned to the wrap-up reason.
    default_wrapup_queues_count: Optional[int] = None
    #: List of queues assigned to the wrap-up reason.
    queues: Optional[list[QueueObjectWithDefaultEnabled]] = None


class QueueObject(ApiModel):
    #: Unique queue identifier.
    id: Optional[str] = None
    #: Name of the queue.
    name: Optional[str] = None
    #: Name of the location.
    location_name: Optional[str] = None
    #: Unique location identifier.
    location_id: Optional[str] = None
    #: Phone number of the queue.
    phone_number: Optional[str] = None
    #: Extension of the queue.
    extension: Optional[int] = None


class QueueWrapUpReasonObject(ApiModel):
    #: Unique wrap-up identifier.
    id: Optional[str] = None
    #: Name of the wrap-up reason.
    name: Optional[str] = None
    #: Description of the wrap-up reason.
    description: Optional[str] = None
    #: Denotes whether the default wrap-up is enabled for the queue.
    is_default_enabled: Optional[bool] = None


class ReadWrapUpReasonSettingsResponse(ApiModel):
    #: Denotes whether the wrap-up timer is enabled.
    wrapup_timer_enabled: Optional[bool] = None
    #: Wrap up timer value in seconds.
    wrapup_timer: Optional[int] = None
    #: List of wrap-up reasons.
    wrapup_reasons: Optional[list[QueueWrapUpReasonObject]] = None


class FeaturesCustomerExperienceEssentialsApi(ApiChild, base='telephony/config'):
    """
    Features: Customer Experience Essentials
    
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
    
    Webex Customer Experience Basic is an offering available as part of the Webex Suite or Webex Calling Professional
    license at no additional cost.
    It includes a simple and powerful set of features which are bundled together to deliver the call center
    functionalities.
    The features such as Voice Queues, skill-based routing, call queue monitoring and analytics, multi call window, and
    more, help users to engage with customers efficiently.
    Also, with our Webex Calling for Microsoft Teams integration, the Microsoft Teams users can access the features
    directly from Teams.
    
    Webex Customer Experience Essentials provides the fundamental capabilities of the Webex Contact Center solution.
    It includes all the Webex Calling professional capabilities, Customer Experience Basic features, and some
    additional key features accessible through the Webex App for both agents and supervisors.
    The features like screen pop, supervisor experience in Webex App, and real-time and historical agent and queue view
    make the Customer Experience Essentials distinct from Customer Experience Basic.
    
    Webex Customer Experience Essentials APIs allows you to manage Customer Experience Essentials features such as
    supervisor configuration, agent configuration, and call queue configuration, which are distinct from Customer
    Experience Basic.
    
    `Learn more about the customer Experience Essentials suite
    <https://help.webex.com/en-us/article/72sb3r/Webex-Customer-Experience-Essentials>`_
    `Learn more about the customer Experience Basic suite
    <https://help.webex.com/en-us/article/nzkg083/Webex-Customer-Experience-Basic>`_
    """

    def read_wrap_up_reason_settings(self, location_id: str, queue_id: str) -> ReadWrapUpReasonSettingsResponse:
        """
        Read Wrap Up Reason Settings

        Return a wrap-up reason by location ID and queue ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the wrap-up reason by location ID and queue ID requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param location_id: The location ID.
        :type location_id: str
        :param queue_id: The queue ID.
        :type queue_id: str
        :rtype: :class:`ReadWrapUpReasonSettingsResponse`
        """
        url = self.ep(f'cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings')
        data = super().get(url)
        r = ReadWrapUpReasonSettingsResponse.model_validate(data)
        return r

    def update_wrap_up_reason_settings(self, location_id: str, queue_id: str, wrapup_reasons: list[str] = None,
                                       default_wrapup_reason_id: str = None, wrapup_timer_enabled: bool = None,
                                       wrapup_timer: int = None):
        """
        Update Wrap Up Reason Settings

        Modify a wrap-up reason by location ID and queue ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Modifying a wrap-up reason by location ID and queue ID requires a full or device administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID.
        :type location_id: str
        :param queue_id: The queue ID.
        :type queue_id: str
        :param wrapup_reasons: List of wrap-up reason IDs.
        :type wrapup_reasons: list[str]
        :param default_wrapup_reason_id: Unique wrap-up identifier.
        :type default_wrapup_reason_id: str
        :param wrapup_timer_enabled: Denotes whether the wrap-up timer is enabled.
        :type wrapup_timer_enabled: bool
        :param wrapup_timer: Wrap up timer value in seconds.
        :type wrapup_timer: int
        :rtype: None
        """
        body = dict()
        if wrapup_reasons is not None:
            body['wrapupReasons'] = wrapup_reasons
        if default_wrapup_reason_id is not None:
            body['defaultWrapupReasonId'] = default_wrapup_reason_id
        if wrapup_timer_enabled is not None:
            body['wrapupTimerEnabled'] = wrapup_timer_enabled
        if wrapup_timer is not None:
            body['wrapupTimer'] = wrapup_timer
        url = self.ep(f'cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings')
        super().put(url, json=body)

    def list_wrap_up_reasons(self) -> list[WrapUpReasonObject]:
        """
        List Wrap Up Reasons

        Return the list of wrap-up reasons configured for a customer.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues. Upon call completion, agents select a
        wrap-up reason from the queue's assigned list. Each wrap-up reason includes a name and description, and can be
        set as the default for a queue. Admins can also configure a timer, which dictates the time agents have to
        select a reason post-call, with a default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the list of wrap-up reasons requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :rtype: list[WrapUpReasonObject]
        """
        url = self.ep('cxEssentials/wrapup/reasons')
        data = super().get(url)
        r = TypeAdapter(list[WrapUpReasonObject]).validate_python(data['wrapupReasons'])
        return r

    def create_wrap_up_reason(self, name: str, description: str = None, queues: list[str] = None,
                              assign_all_queues_enabled: bool = None) -> str:
        """
        Create Wrap Up Reason

        Create a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Creating a wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Name of the wrap-up reason.
        :type name: str
        :param description: Description of the wrap-up reason.
        :type description: str
        :param queues: List of queue IDs assigned to the wrap-up reason.
        :type queues: list[str]
        :param assign_all_queues_enabled: Denotes whether all queues are assigned to the wrap-up reason.
        :type assign_all_queues_enabled: bool
        :rtype: str
        """
        body = dict()
        body['name'] = name
        if description is not None:
            body['description'] = description
        if queues is not None:
            body['queues'] = queues
        if assign_all_queues_enabled is not None:
            body['assignAllQueuesEnabled'] = assign_all_queues_enabled
        url = self.ep('cxEssentials/wrapup/reasons')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def validate_wrap_up_reason(self, name: str):
        """
        Validate Wrap Up Reason

        Validate the wrap-up reason name.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Validating the wrap-up reason name requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Name of the wrap-up reason.
        :type name: str
        :rtype: None
        """
        body = dict()
        body['name'] = name
        url = self.ep('cxEssentials/wrapup/reasons/actions/validateName/invoke')
        super().post(url, json=body)

    def delete_wrap_up_reason(self, wrapup_reason_id: str):
        """
        Delete Wrap Up Reason

        Delete a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Deleting the wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: None
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        super().delete(url)

    def read_wrap_up_reason(self, wrapup_reason_id: str) -> WrapUpReasonDetailsObject:
        """
        Read Wrap Up Reason

        Return the wrap-up reason by ID.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the wrap-up reason by ID requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: :class:`WrapUpReasonDetailsObject`
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        data = super().get(url)
        r = WrapUpReasonDetailsObject.model_validate(data)
        return r

    def update_wrap_up_reason(self, wrapup_reason_id: str, name: str = None, description: str = None,
                              queues_to_assign: list[str] = None, queues_to_unassign: list[str] = None,
                              assign_all_queues_enabled: bool = None, unassign_all_queues_enabled: bool = None):
        """
        Update Wrap Up Reason

        Modify a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Modifying a wrap-up reason requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :param name: Name of the wrap-up reason.
        :type name: str
        :param description: Description of the wrap-up reason.
        :type description: str
        :param queues_to_assign: List of queue IDs to assign to the wrap-up reason.
        :type queues_to_assign: list[str]
        :param queues_to_unassign: List of queue IDs to unassign from the wrap-up reason.
        :type queues_to_unassign: list[str]
        :param assign_all_queues_enabled: Denotes whether all queues are assigned to the wrap-up reason.
        :type assign_all_queues_enabled: bool
        :param unassign_all_queues_enabled: Denotes whether all queues are unassigned from the wrap-up reason.
        :type unassign_all_queues_enabled: bool
        :rtype: None
        """
        body = dict()
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if queues_to_assign is not None:
            body['queuesToAssign'] = queues_to_assign
        if queues_to_unassign is not None:
            body['queuesToUnassign'] = queues_to_unassign
        if assign_all_queues_enabled is not None:
            body['assignAllQueuesEnabled'] = assign_all_queues_enabled
        if unassign_all_queues_enabled is not None:
            body['unassignAllQueuesEnabled'] = unassign_all_queues_enabled
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}')
        super().put(url, json=body)

    def read_available_queues(self, wrapup_reason_id: str) -> list[QueueObject]:
        """
        Read Available Queues

        Return the available queues for a wrap-up reason.

        Agents handling calls use wrap-up reasons to categorize the outcome after a call ends. The control hub admin
        can configure these reasons for customers and assign them to queues.
        Upon call completion, agents select a wrap-up reason from the queue's assigned list. Each wrap-up reason
        includes a name and description, and can be set as the default for a queue.
        Admins can also configure a timer, which dictates the time agents have to select a reason post-call, with a
        default of 60 seconds. This timer can be disabled if necessary.

        Retrieving the available queues for a wrap-up reason requires a full or read-only administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param wrapup_reason_id: Wrap-up reason ID.
        :type wrapup_reason_id: str
        :rtype: list[QueueObject]
        """
        url = self.ep(f'cxEssentials/wrapup/reasons/{wrapup_reason_id}/availableQueues')
        data = super().get(url)
        r = TypeAdapter(list[QueueObject]).validate_python(data['queues'])
        return r

    def list_available_agents(self, location_id: str, has_cx_essentials: bool = None,
                              org_id: str = None) -> list[GetAvailableAgentsCallQueueObject]:
        """
        List Available Agents

        Return a list of available agents with Customer Experience Essentials license in a location.

        Retrieving the list of available agents requires a full or read-only administrator auth token with a scope of
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
        url = self.ep(f'locations/{location_id}/cxEssentials/agents/availableAgents')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetAvailableAgentsCallQueueObject]).validate_python(data['agents'])
        return r

    def read_screen_pop_configuration(self, location_id: str, queue_id: str,
                                      org_id: str = None) -> GetScreenPopConfigurationObject:
        """
        Read Screen Pop Configuration

        Returns the screen pop configuration for a call queue in a location.

        Screen pop lets agents view customer-related info in a pop-up window.

        Retrieving the screen pop configuration requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue resides.
        :type location_id: str
        :param queue_id: The call queue ID for which screen pop configuration is modified.
        :type queue_id: str
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :rtype: :class:`GetScreenPopConfigurationObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        data = super().get(url, params=params)
        r = GetScreenPopConfigurationObject.model_validate(data)
        return r

    def update_screen_pop_configuration(self, location_id: str, queue_id: str, enabled: bool = None,
                                        screen_pop_url: str = None, desktop_label: str = None,
                                        query_params: QueryParamsObject = None, org_id: str = None):
        """
        Update Screen Pop Configuration

        Modifies the screen pop configuration for a call queue in a location.

        Screen pop lets agents view customer-related info in a pop-up window.

        Modifying the screen pop configuration requires a full or device administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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
        :param query_params: The additional user-defined key-value pairs that must be sent to the agent.
        :type query_params: QueryParamsObject
        :param org_id: The organization ID of the customer or partner's organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if screen_pop_url is not None:
            body['screenPopUrl'] = screen_pop_url
        if desktop_label is not None:
            body['desktopLabel'] = desktop_label
        if query_params is not None:
            body['queryParams'] = query_params.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop')
        super().put(url, params=params, json=body)
