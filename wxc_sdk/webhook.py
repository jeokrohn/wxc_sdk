"""
Webhook types and API
"""
import datetime
import json
from collections.abc import Generator
from enum import Enum
from typing import Optional

from pydantic import Field

from .api_child import ApiChild
from .base import ApiModel, to_camel, webex_id_to_uuid

__all__ = ['WebHookEvent', 'WebHookResource', 'WebHookCreate', 'WebHookStatus', 'WebHook', 'WebhookApi']


class WebHookEvent(str, Enum):
    """
    The event type for the webhook.
    """
    #: an object was created
    created = 'created'
    #: an object was updated
    updated = 'updated'
    #: an object was deleted
    deleted = 'deleted'
    #: a meeting was started
    started = 'started'
    #: a meeting was ended
    ended = 'ended'
    #: a participant joined
    joined = 'joined'
    #: a participant left
    left = 'left'
    all = 'all'


class WebHookResource(str, Enum):
    """
    The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    """
    attachment_actions = 'attachmentActions'
    memberships = 'memberships'
    messages = 'messages'
    rooms = 'rooms'
    telephony_calls = 'telephony_calls'
    telephony_mwi = 'telephony_mwi'
    meetings = 'meetings'
    recordings = 'recordings'
    meeting_participants = 'meetingParticipants'
    meeting_transcripts = 'meetingTranscripts'


class WebHookCreate(ApiModel):
    name: str
    target_url: str
    resource: WebHookResource
    event: WebHookEvent
    filter: Optional[str]
    secret: Optional[str]
    owned_by: Optional[str]


class WebHookStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'


class WebHook(ApiModel):
    #: The unique identifier for the webhook.
    webhook_id: Optional[str] = Field(alias='id')
    #: A user-friendly name for the webhook.
    name: str
    #: The URL that receives POST requests for each event.
    target_url: str
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[WebHookResource]
    #: The event type for the webhook.
    event: Optional[WebHookEvent]
    #: The filter that defines the webhook scope.
    filter: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: WebHookStatus
    #: The date and time the webhook was created.
    created: datetime.datetime
    org_id: Optional[str]
    created_by: Optional[str]
    app_id: Optional[str]
    owned_by: Optional[str]

    @property
    def app_id_uuid(self) -> str:
        return webex_id_to_uuid(self.app_id)

    @property
    def webhook_id_uuid(self) -> str:
        return webex_id_to_uuid(self.webhook_id)

    @property
    def org_id_uuid(self) -> str:
        return webex_id_to_uuid(self.org_id)

    @property
    def created_by_uuid(self) -> str:
        return webex_id_to_uuid(self.created_by)


class WebhookApi(ApiChild, base='webhooks'):
    """
    API for webhook management
    """

    def list(self) -> Generator[WebHook, None, None]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=WebHook)

    def create(self, *, name: str, target_url: str, resource: WebHookResource, event: WebHookEvent, filter: str = None,
               secret: str = None,
               owned_by: str = None) -> WebHook:
        """
        Creates a webhook.

        :param name: A user-friendly name for the webhook.
        :param target_url: The URL that receives POST requests for each event.
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :param event: The event type for the webhook.
        :param filter: The filter that defines the webhook scope.
        :param secret: The secret used to generate payload signature.
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings and
            meetingParticipants resources for now.

        :return: the new webhook
        """
        params = {to_camel(param): value for i, (param, value) in enumerate(locals().items())
                  if i and value is not None}
        body = json.loads(WebHookCreate(**params).json())
        ep = self.ep()
        data = self.post(ep, json=body)
        result = WebHook.parse_obj(data)
        return result

    def details(self, *, webhook_id: str) -> WebHook:
        """
        Get Webhook Details
        Shows details for a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: Webhook details
        """
        url = self.ep(webhook_id)
        return WebHook.parse_obj(self.get(url))

    def update(self, *, webhook_id: str, update: WebHook) -> WebHook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that
        was auto deactivated. The fields that can be updated are name, targetURL, secret and status. All other fields,
        if supplied, are ignored.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param update: The webhook update
        :type update: WebHook
        :return: updated :class:`WebHook` object
        """
        url = self.ep(webhook_id)
        webhook_data = update.json(include={'name', 'target_url', 'secret', 'owned_by', 'status'})
        return WebHook.parse_obj(self.put(url, data=webhook_data))

    def webhook_delete(self, *, webhook_id: str):
        """
        Deletes a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: None
        """
        ep = self.ep(f'{webhook_id}')
        self.delete(ep)
