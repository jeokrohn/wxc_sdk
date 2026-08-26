from __future__ import annotations

import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetWebhookInterestRegistrationResponse', 'Interest', 'InterestActor', 'InterestResource',
           'WebhookInterestRegistrationsApi']


class InterestResource(str, Enum):
    hook_status = 'Hook Status'
    agent = 'Agent'
    services = 'Services'
    agent_monitoring = 'Agent Monitoring'
    queue = 'Queue'
    queue_monitoring = 'Queue Monitoring'


class InterestActor(str, Enum):
    workspaces = 'Workspaces'
    virtual_lines = 'Virtual Lines'


class Interest(ApiModel):
    #: Resource-based interest. Set exactly one of `resource` or `actor` per interest entry.
    #: 
    #: - `Hook Status` - Enables webhook events for the `telephony_hookstatus` resource.
    #: - `Agent` - Enables webhook events for the `telephony_agent` resource.
    #: - `Services` - Enables webhook events for the `telephony_services` resource.
    #: - `Agent Monitoring` - Enables webhook events for the `telephony_agentMonitoring` resource.
    #: - `Queue` - Enables webhook events for the `telephony_queue` resource.
    #: - `Queue Monitoring` - Enables webhook events for the `telephony_queueMonitoring` resource.
    resource: Optional[InterestResource] = None
    #: Actor-based interest. Set exactly one of `resource` or `actor` per interest entry.
    #: 
    #: - `Workspaces` - Enables telephony webhook events associated with workspace actors.
    #: - `Virtual Lines` - Enables telephony webhook events associated with virtual line actors.
    actor: Optional[InterestActor] = None


class GetWebhookInterestRegistrationResponse(ApiModel):
    #: The collection of webhook interests associated with the registration. Each interest is either resource-based or
    #: actor-based. At least one interest is always present in a successful response.
    interests: Optional[list[Interest]] = None
    #: The date/time at which the registration expires.
    expires_at: Optional[datetime] = None


class WebhookInterestRegistrationsApi(ApiChild, base='telephony/webhookInterestRegistrations'):
    """
    Webhook Interest Registrations
    
    Webhook interests enable the emission of Webex Calling webhook events that are not emitted by default, even when a
    webhook is registered for an applicable resource. Clients manage webhook interests through registrations. Once a
    client registers an interest, that interest applies to all applicable webhooks for the organization, not only
    webhooks created by that client. Webhook interests are therefore not intended to filter unwanted events.
    
    Webhook interest registrations expire and should be refreshed periodically. The default expiration period is 60
    days.
    
    There are two types of webhook interests: actor interests and resource interests. Webhook events for actor and
    resource categories without a corresponding interest type do not require an interest registration and are always
    emitted.
    
    **Notes:**
    
    - These APIs are reserved for administrators. Although the `POST` and `DELETE` operations are technically "write"
    operations, they are exceptionally associated with the `spark-admin:calls_read` scope because they are used
    alongside the read-only Webhook APIs.
    
    - The client associated with a registration is derived from the access token and is not supplied by the caller.
    """

    def delete_webhook_interest_registration(self) -> None:
        """
        Delete Webhook Interest Registration

        Deletes the webhook interest registration associated with the authenticated user and the client derived from
        the access token. The client identifier is not supplied by the caller.

        Registrations are managed for a specific user and client, but registered interests apply to all applicable
        webhooks in the organization.

        This API is reserved for administrators and requires the `spark-admin:calls_read` scope.

        :rtype: None
        """
        url = self.ep()
        super().delete(url)

    def get_webhook_interest_registration(self) -> GetWebhookInterestRegistrationResponse:
        """
        Get Webhook Interest Registration

        Returns the webhook interest registration associated with the authenticated user and the client derived from
        the access token, including the list of interests and the date/time at which the registration expires. The
        client identifier is not supplied by the caller.

        Registrations are managed for a specific user and client, but registered interests apply to all applicable
        webhooks in the organization.

        This API is reserved for administrators and requires the `spark-admin:calls_read` scope.

        :rtype: :class:`GetWebhookInterestRegistrationResponse`
        """
        url = self.ep()
        data = super().get(url)
        r = GetWebhookInterestRegistrationResponse.model_validate(data)
        return r

    def create_webhook_interest_registration(self, interests: list[Interest], duration: int = None) -> None:
        """
        Create a Webhook Interest Registration

        Adds or updates a webhook interest registration associated with the authenticated user and the client derived
        from the access token. At least one item in `interests` is required and `duration` is optional. The client
        identifier is not supplied in the request. If a registration does not already exist for the authenticated user
        and client, it is created; otherwise, it is updated with the incoming registration information.

        Registrations are managed for a specific user and client, but registered interests apply to all applicable
        webhooks in the organization.

        This API is reserved for administrators and requires the `spark-admin:calls_read` scope.

        :param interests: The collection of webhook interests for this registration. At least one interest is required.
            Each interest is either resource-based or actor-based (exactly one of `resource` or `actor` is set).
        :type interests: list[Interest]
        :param duration: Optional time, in days, after which the registration expires. When omitted, the registration
            defaults to expire after 60 days.
        :type duration: int
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['interests'] = TypeAdapter(list[Interest]).dump_python(interests, mode='json', by_alias=True, exclude_none=True)
        if duration is not None:
            body['duration'] = duration
        url = self.ep()
        super().post(url, json=body)
