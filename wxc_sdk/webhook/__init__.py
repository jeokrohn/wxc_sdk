"""
Webhook types and API
"""
import datetime
import json
from collections.abc import Generator
from typing import Optional, Union, ClassVar

from pydantic import Field, Extra, model_validator

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, webex_id_to_uuid
from ..base import SafeEnum as Enum

__all__ = ['WebhookEventType', 'WebhookResource', 'WebhookStatus', 'Webhook', 'WebhookEventData',
           'WebhookEvent', 'WebhookApi', 'WebhookCreate']


class WebhookEventType(str, Enum):
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
    #: A room was migrated to a different geography. The roomId has changed.
    migrated = 'migrated'
    #: A Service App was authorized.
    authorized = 'authorized'
    #: A Service App was deauthorized.
    deauthorized = 'deauthorized'

    all = 'all'


class WebhookResource(str, Enum):
    """
    The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    """
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
    #: The `CallRecordings
    #: <https://developer.webex.com/docs/api/v1/converged-recordings>`_ resource.
    converged_recordings = 'convergedRecordings'
    #: The `Meeting Participants
    #: <https://developer.webex.com/docs/api/v1/meeting-participants>`_ resource.
    meeting_participants = 'meetingParticipants'
    #: The `Meeting Transcripts
    #: <https://developer.webex.com/docs/api/v1/meeting-transcripts>`_ resource.
    meeting_transcripts = 'meetingTranscripts'
    #: Service App authorization notification.
    service_app = 'serviceApp'
    telephony_calls = 'telephony_calls'
    telephony_mwi = 'telephony_mwi'
    all = 'all'


class WebhookCreate(ApiModel):
    """
    Body for a webhook create call
    """
    name: str
    target_url: str
    resource: WebhookResource
    event: WebhookEventType
    filter: Optional[str] = None
    secret: Optional[str] = None
    owned_by: Optional[str] = None


class WebhookStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'


class Webhook(ApiModel):
    #: The unique identifier for the webhook.
    webhook_id: Optional[str] = Field(alias='id', default=None)
    #: A user-friendly name for the webhook.
    name: str
    #: The URL that receives POST requests for each event.
    target_url: str
    #: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[WebhookResource] = None
    #: The event type for the Webhook.
    event: Optional[WebhookEventType] = None
    #: The filter that defines the webhook scope.
    filter: Optional[str] = None
    #: The secret used to generate payload signature.
    secret: Optional[str] = None
    #: The status of the webhook. Use active to reactivate a disabled webhook.
    status: WebhookStatus
    #: The date and time the webhook was created.
    created: datetime.datetime
    org_id: Optional[str] = None
    created_by: Optional[str] = None
    app_id: Optional[str] = None
    #: Specify `org` when creating an org/admin level webhook. Supported for `meetings`, `recordings`,
    #: `convergedRecordings`, `meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`, `controlHubAlerts`,
    #: `rooms`, and `messaging` (for Compliance Officers and messages with file attachments only - see
    #: `inline file DLP
    #: <https://developer.webex.com/docs/api/guides/webex-real-time-file-dlp-basics>`_) resources.
    owned_by: Optional[str] = None

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


class WebhookEventDataForbid(ApiModel):
    resource: ClassVar = None
    _registry: ClassVar = dict()

    class Config:
        extra = Extra.forbid

    def __init_subclass__(cls: 'WebhookEventDataForbid', **kwargs):
        """

        :meta private:
        """
        if cls.resource is None and cls.__name__ != 'WebhookEventData':
            raise KeyError(f'{cls.__name__}: resource needs to be defined')
        WebhookEventDataForbid._registry[cls.resource] = cls

    @classmethod
    def registered_subclass(cls, resource: str):
        """

        :meta private:
        """
        return cls._registry.get(resource)


class WebhookEventData(WebhookEventDataForbid):
    """
    base class for data components of a webhook event.
    Subclasses of this base implement the actual data models

    Examples:
        .. list-table::
           :header-rows: 1

           * - resource
             - class
           * - telephony_calls
             - :class:`wxc_sdk.telephony.calls.TelephonyEventData`
           * - messages
             - :class:`wxc_sdk.messages.MessagesData`
           * - memberships
             - :class:`wxc_sdk.memberships.MembershipsData`
           * - attachmentActions
             - :class:`wxc_sdk.attachment_actions.AttachmentActionsApi`
    """

    class Config:
        extra = Extra.allow


class WebhookEvent(Webhook):
    """
    A webhook event. Can be used in to parse data posted to a webhook handler
    """
    actor_id: Optional[str] = None
    #: resource specific event data; for registered subclasses of :class:`wwx_sdk.webhook.WebhookEventData` an
    #: instance of this subclass is returned. If no class is registered for the given resource, then data is returned as
    #: generic WebhookEventData instance
    data: Union[WebhookEventDataForbid, dict]

    @model_validator(mode='before')
    def parse_data(cls, values):
        """
        Parse 'data' component with the correct registered Subclass

        :meta private:
        """
        if (v_data := values.get('data')) and (v_resource := values.get('resource')):
            if target_class := WebhookEventDataForbid.registered_subclass(v_resource):
                parsed = target_class.model_validate(v_data)
                values['data'] = parsed
        return values


class WebhookApi(ApiChild, base='webhooks'):
    """
    API for webhook management
    """

    def list(self) -> Generator[Webhook, None, None]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Webhook)

    def create(self, name: str, target_url: str, resource: WebhookResource, event: WebhookEventType, filter: str = None,
               secret: str = None,
               owned_by: str = None) -> Webhook:
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
        body = json.loads(WebhookCreate(**params).model_dump_json())
        ep = self.ep()
        data = self.post(ep, json=body)
        result = Webhook.model_validate(data)
        return result

    def details(self, webhook_id: str) -> Webhook:
        """
        Get Webhook Details
        Shows details for a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: Webhook details
        """
        url = self.ep(webhook_id)
        return Webhook.model_validate(self.get(url))

    def update(self, webhook_id: str, update: Webhook) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that
        was auto deactivated. The fields that can be updated are name, targetURL, secret and status. All other fields,
        if supplied, are ignored.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param update: The webhook update
        :type update: Webhook
        :return: updated :class:`Webhook` object
        """
        url = self.ep(webhook_id)
        webhook_data = update.model_dump_json(include={'name', 'target_url', 'secret', 'owned_by', 'status'})
        return Webhook.model_validate(self.put(url, data=webhook_data))

    def webhook_delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: None
        """
        ep = self.ep(f'{webhook_id}')
        self.delete(ep)
