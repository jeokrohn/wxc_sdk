from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateWebhookBody', 'Event', 'ListWebhooksResponse', 'Resource', 'Status', 'Webhook', 'WebhooksApi']


class Status(str, Enum):
    #: The webhook is active.
    active = 'active'
    #: The webhook is inactive.
    inactive = 'inactive'


class Resource(str, Enum):
    #: The Attachment Actions resource.
    attachment_actions = 'attachmentActions'
    #: The Memberships resource.
    memberships = 'memberships'
    #: The Messages resource.
    messages = 'messages'
    #: The Rooms resource.
    rooms = 'rooms'
    #: The Meetings resource.
    meetings = 'meetings'
    #: The Recordings resource.
    recordings = 'recordings'
    #: The Meeting Participants resource.
    meeting_participants = 'meetingParticipants'
    #: The Meeting Transcripts resource.
    meeting_transcripts = 'meetingTranscripts'


class Event(str, Enum):
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


class CreateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[Resource]
    #: The event type for the webhook.
    event: Optional[Event]
    #: The filter that defines the webhook scope. See Filtering Webhooks for more information.
    filter: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants, and
    #: meetingTranscripts resources.
    owned_by: Optional[str]


class Webhook(CreateWebhookBody):
    #: A unique identifier for the webhook.
    id: Optional[str]
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: Optional[Status]
    #: The date and time the webhook was created.
    created: Optional[str]


class ListWebhooksResponse(ApiModel):
    items: Optional[list[Webhook]]


class UpdateWebhookBody(ApiModel):
    #: A user-friendly name for the webhook.
    name: Optional[str]
    #: The URL that receives POST requests for each event.
    target_url: Optional[str]
    #: The secret used to generate payload signature.
    secret: Optional[str]
    #: Specified when creating an org/admin level webhook. Supported for meetings, recordings, meetingParticipants and
    #: meetingTranscripts resources.
    owned_by: Optional[str]
    #: The status of the webhook. Use "active" to reactivate a disabled webhook.
    status: Optional[Status]


class WebhooksApi(ApiChild, base='webhooks'):
    """
    For Webex for Government (FedRAMP), the following resource types are not available for Webhooks: meetings,
    recordings, meetingParticipants, and meetingTranscripts.
    Webhooks allow your app to be notified via HTTP when a specific event occurs in Webex. For example, your app can
    register a webhook to be notified when a new message is posted into a specific room.
    Events trigger in near real-time allowing your app and backend IT systems to stay in sync with new content and room
    activity.
    Check The Webhooks Guide and our blog regularly for announcements of additional webhook resources and event types.
    Long result sets will be split into pages.
    """

    def list(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
        """
        List all of your webhooks.

        :param owned_by: Limit the result list to org wide webhooks. Only allowed value is org.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/list-webhooks
        """
        if owned_by is not None:
            params['ownedBy'] = owned_by
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Webhook, params=params)

    def create(self, name: str, target_url: str, resource: Resource, event: Event, filter: str = None, secret: str = None, owned_by: str = None) -> Webhook:
        """
        Creates a webhook.
        To learn more about how to create and use webhooks, see The Webhooks Guide.

        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :type resource: Resource
        :param event: The event type for the webhook.
        :type event: Event
        :param filter: The filter that defines the webhook scope. See Filtering Webhooks for more information.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants, and meetingTranscripts resources.
        :type owned_by: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook
        """
        body = CreateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if resource is not None:
            body.resource = resource
        if event is not None:
            body.event = event
        if filter is not None:
            body.filter = filter
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def details(self, webhook_id: str) -> Webhook:
        """
        Shows details for a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/get-webhook-details
        """
        url = self.ep(f'{webhook_id}')
        data = super().get(url=url)
        return Webhook.parse_obj(data)

    def update(self, webhook_id: str, name: str, target_url: str, secret: str = None, owned_by: str = None, status: Status = None) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that was
        auto deactivated.
        The fields that can be updated are name, targetURL, secret and status. All other fields, if supplied, are
        ignored.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param name: A user-friendly name for the webhook.
        :type name: str
        :param target_url: The URL that receives POST requests for each event.
        :type target_url: str
        :param secret: The secret used to generate payload signature.
        :type secret: str
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings,
            meetingParticipants and meetingTranscripts resources.
        :type owned_by: str
        :param status: The status of the webhook. Use "active" to reactivate a disabled webhook.
        :type status: Status

        documentation: https://developer.webex.com/docs/api/v1/webhooks/update-a-webhook
        """
        body = UpdateWebhookBody()
        if name is not None:
            body.name = name
        if target_url is not None:
            body.target_url = target_url
        if secret is not None:
            body.secret = secret
        if owned_by is not None:
            body.owned_by = owned_by
        if status is not None:
            body.status = status
        url = self.ep(f'{webhook_id}')
        data = super().put(url=url, data=body.json())
        return Webhook.parse_obj(data)

    def delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.
        Specify the webhook ID in the webhookId parameter in the URI.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str

        documentation: https://developer.webex.com/docs/api/v1/webhooks/delete-a-webhook
        """
        url = self.ep(f'{webhook_id}')
        super().delete(url=url)
        return
