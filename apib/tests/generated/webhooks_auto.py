from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Webhook', 'WebhookEvent', 'WebhookResource', 'WebhookStatus', 'WebhooksApi']


class WebhookResource(str, Enum):
    #: The `Attachment Actions
    #: <https://developer.webex.com/docs/api/v1/attachment-actions>`_ resource.
    attachment_actions = 'attachmentActions'
    #: The `Memberships
    #: <https://developer.webex.com/docs/api/v1/memberships>`_ resource.
    memberships = 'memberships'
    #: The `Messages
    #: <https://developer.webex.com/docs/api/v1/messages>`_ resource.
    messages = 'messages'
    #: The `Rooms
    #: <https://developer.webex.com/docs/api/v1/rooms>`_ resource.
    rooms = 'rooms'
    #: The `Meetings
    #: <https://developer.webex.com/docs/api/v1/meetings>`_ resource.
    meetings = 'meetings'
    #: The `Recordings
    #: <https://developer.webex.com/docs/api/v1/recordings>`_ resource.
    recordings = 'recordings'
    #: The `Meeting Participants
    #: <https://developer.webex.com/docs/api/v1/meeting-participants>`_ resource.
    meeting_participants = 'meetingParticipants'
    #: The `Meeting Transcripts
    #: <https://developer.webex.com/docs/api/v1/meeting-transcripts>`_ resource.
    meeting_transcripts = 'meetingTranscripts'


class WebhookEvent(str, Enum):
    #: An object was created.
    created = 'created'
    #: An object was updated.
    updated = 'updated'
    #: An object was deleted.
    deleted = 'deleted'
    #: A meeting was started.
    started = 'started'
    #: A meeting was ended.
    ended = 'ended'
    #: A participant joined.
    joined = 'joined'
    #: A participant left.
    left = 'left'
    #: A room was migrated to a different geography. The roomId has changed.
    migrated = 'migrated'


class WebhookStatus(str, Enum):
    #: The webhook is active.
    active = 'active'
    #: The webhook is inactive.
    inactive = 'inactive'


class Webhook(ApiModel):
    #: A unique identifier for the webhook.
    #: example: Y2lzY29zcGFyazovL3VzL1dFQkhPT0svOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: A user-friendly name for the webhook.
    #: example: My Awesome Webhook
    name: Optional[str] = None
    #: The URL that receives POST requests for each event.
    #: example: https://example.com/mywebhook
    target_url: Optional[str] = None
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    #: example: messages
    resource: Optional[WebhookResource] = None
    #: The event type for the webhook.
    #: example: created
    event: Optional[WebhookEvent] = None
    #: The filter that defines the webhook scope.
    #: example: roomId=Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    filter: Optional[str] = None
    #: The secret used to generate payload signature.
    #: example: 86dacc007724d8ea666f88fc77d918dad9537a15
    secret: Optional[str] = None
    #: The status of the webhook. Use `active` to reactivate a disabled webhook.
    #: example: active
    status: Optional[WebhookStatus] = None
    #: The date and time the webhook was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: Specify `org` when creating an org/admin level webhook. Supported for `meetings`, `recordings`,
    #: `meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`, `controlHubAlerts`, `rooms`, and `messaging`
    #: (for Compliance Officers and messages with file attachments only - see `inline file DLP
    #: <https://developer.webex.com/docs/api/guides/webex-real-time-file-dlp-basics>`_) resources.
    #: example: org
    owned_by: Optional[str] = None


class WebhooksApi(ApiChild, base='webhooks'):
    """
    Webhooks
    
    For Webex for Government (FedRAMP), the following resource types are not
    available for Webhooks: meetings, recordings, meetingParticipants, and
    meetingTranscripts.
    
    
    
    Webhooks allow your app to be notified via HTTP when a specific event occurs in Webex. For example, your app can
    register a webhook to be notified when a new message is posted into a specific room.
    
    Events trigger in near real-time allowing your app and backend IT systems to stay in sync with new content and room
    activity.
    
    Check The `Webhooks Guide
    <https://developer.webex.com/docs/api/guides/webhooks>`_ and `our blog
    
    Long result sets will be split into `pages
    <https://developer.webex.com/docs/basics#pagination>`_.
    """

    def list_webhooks(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
        """
        List Webhooks

        List all of your webhooks.

        :param owned_by: Limit the result list to org wide webhooks. Only allowed value is `org`.
        :type owned_by: str
        :return: Generator yielding :class:`Webhook` instances
        """
        if owned_by is not None:
            params['ownedBy'] = owned_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Webhook, item_key='items', params=params)

    def create_a_webhook(self, name: str, target_url: str, resource: WebhookResource, event: WebhookEvent,
                         filter: str = None, secret: str = None, owned_by: str = None) -> Webhook:
        """
        Create a Webhook

        Creates a webhook.

        To learn more about how to create and use webhooks, see The `Webhooks Guide
        <https://developer.webex.com/docs/api/guides/webhooks>`_.

        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :type resource: WebhookResource
        :param event: The event type for the webhook.
        :type event: WebhookEvent
        :param filter: The filter that defines the webhook scope. See `Filtering Webhooks
            <https://developer.webex.com/docs/api/guides/webhooks#filtering-webhooks>`_ for more information.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specify `org` when creating an org/admin level webhook. Supported for `meetings`,
            `recordings`, `meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`, `controlHubAlerts`, `rooms`,
            and `messaging` (for Compliance Officers and messages with file attachments only - see `inline file DLP
            <https://developer.webex.com/docs/api/guides/webex-real-time-file-dlp-basics>`_)
            resources.
        :type owned_by: str
        :rtype: :class:`Webhook`
        """
        body = dict()
        body['name'] = name
        body['targetUrl'] = target_url
        body['resource'] = enum_str(resource)
        body['event'] = enum_str(event)
        if filter is not None:
            body['filter'] = filter
        if secret is not None:
            body['secret'] = secret
        if owned_by is not None:
            body['ownedBy'] = owned_by
        url = self.ep()
        data = super().post(url, json=body)
        r = Webhook.model_validate(data)
        return r

    def get_webhook_details(self, webhook_id: str) -> Webhook:
        """
        Get Webhook Details

        Shows details for a webhook, by ID.

        Specify the webhook ID in the `webhookId` parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :rtype: :class:`Webhook`
        """
        url = self.ep(f'{webhook_id}')
        data = super().get(url)
        r = Webhook.model_validate(data)
        return r

    def update_a_webhook(self, webhook_id: str, name: str, target_url: str, secret: str = None, owned_by: str = None,
                         status: WebhookStatus = None) -> Webhook:
        """
        Update a Webhook

        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that was
        auto deactivated.
        The fields that can be updated are `name`, `targetURL`, `secret` and `status`. All other fields, if supplied,
        are ignored.

        Specify the webhook ID in the `webhookId` parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specify `org` when creating an org/admin level webhook. Supported for `meetings`,
            `recordings`, `meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`, `controlHubAlerts`, `rooms`,
            and `messaging` (for Compliance Officers and messages with file attachments only - see `inline file DLP
            <https://developer.webex.com/docs/api/guides/webex-real-time-file-dlp-basics>`_)
            resources.
        :type owned_by: str
        :param status: The status of the webhook. Use "active" to reactivate a disabled webhook.
        :type status: WebhookStatus
        :rtype: :class:`Webhook`
        """
        body = dict()
        body['name'] = name
        body['targetUrl'] = target_url
        if secret is not None:
            body['secret'] = secret
        if owned_by is not None:
            body['ownedBy'] = owned_by
        if status is not None:
            body['status'] = enum_str(status)
        url = self.ep(f'{webhook_id}')
        data = super().put(url, json=body)
        r = Webhook.model_validate(data)
        return r

    def delete_a_webhook(self, webhook_id: str):
        """
        Delete a Webhook

        Deletes a webhook, by ID.

        Specify the webhook ID in the `webhookId` parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :rtype: None
        """
        url = self.ep(f'{webhook_id}')
        super().delete(url)
