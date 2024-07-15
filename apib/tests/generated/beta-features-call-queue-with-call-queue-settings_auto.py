from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallQueueWithCallQueueSettingsApi', 'CallQueueSettingsGet']


class CallQueueSettingsGet(ApiModel):
    #: Modify the optimized simultaneous ring algorithm setting.
    maintain_queue_position_for_sim_ring_enabled: Optional[bool] = None
    #: Enable this setting to change the status of an agent to unavailable in case of bounced calls.
    force_agent_unavailable_on_bounced_enabled: Optional[bool] = None


class BetaFeaturesCallQueueWithCallQueueSettingsApi(ApiChild, base='telephony/config/queues/settings'):
    """
    Beta Features: Call Queue with Call Queue Settings
    
    Webex Calling Organization Settings supports reading and writing of Webex Calling settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full, user, or read-only administrator auth token with a
    scope of ```spark-admin:telephony_config_read```, as the current set of APIs are designed to provide supplemental
    information for administrators utilizing People Webex calling APIs.
    """

    def get_call_queue_settings(self, org_id: str = None) -> CallQueueSettingsGet:
        """
        Get Call Queue Settings

        Retrieve Call Queue Settings for a specific organization.

        Call Queue Settings are used to enable the Simultaneous Ringing algorithm that maintains queue positions for
        customers.

        Retrieving Call Queue Settings requires a full, user, or read-only administrator auth token with a scope of
        ```spark-admin:telephony_config_read```.

        :param org_id: Call Queue Settings for this organization.
        :type org_id: str
        :rtype: :class:`CallQueueSettingsGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = CallQueueSettingsGet.model_validate(data)
        return r

    def update_call_queue_settings(self, maintain_queue_position_for_sim_ring_enabled: bool = None,
                                   force_agent_unavailable_on_bounced_enabled: bool = None, org_id: str = None):
        """
        Update Call Queue Settings

        Update Call Queue Settings for a specific organization.

        Call Queue Settings are used to enable the Simultaneous Ringing algorithm that maintains queue positions for
        customers.

        Updating Call Queue Settings requires a full or user administrator auth token with a scope of
        ```spark-admin:telephony_config_write```.

        :param maintain_queue_position_for_sim_ring_enabled: Modify the optimized simultaneous ring algorithm setting.
        :type maintain_queue_position_for_sim_ring_enabled: bool
        :param force_agent_unavailable_on_bounced_enabled: Enable this setting to change the status of an agent to
            unavailable in case of bounced calls.
        :type force_agent_unavailable_on_bounced_enabled: bool
        :param org_id: Call Queue Settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if maintain_queue_position_for_sim_ring_enabled is not None:
            body['maintainQueuePositionForSimRingEnabled'] = maintain_queue_position_for_sim_ring_enabled
        if force_agent_unavailable_on_bounced_enabled is not None:
            body['forceAgentUnavailableOnBouncedEnabled'] = force_agent_unavailable_on_bounced_enabled
        url = self.ep()
        super().put(url, params=params, json=body)
