"""
Webhook types and API
"""
import datetime
from collections.abc import Generator
from typing import Optional, Union, ClassVar

from pydantic import Field, Extra, model_validator

from ..api_child import ApiChild
from ..base import ApiModel, webex_id_to_uuid, enum_str
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
    #: Status of admin batch job was changed.
    status_changed = 'statusChanged'

    all = 'all'


class WebhookResource(str, Enum):
    """
    The resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    """
    #: The `Attachment Actions
    #: <https://developer.webex.com/docs/api/v1/attachment-actions>`_ resource.
    attachment_actions = 'attachmentActions'
    #: `data sources
    #: <https://developer.webex.com/docs/api/v1/data-sources>`_ resource.
    data_sources = 'dataSources'
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
    #: Performance counter for a dedicated instance.
    uc_counters = 'uc_counters'
    #: Admin Batch Jobs notification.
    admin_batch_jobs = 'adminBatchJobs'
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
    #: Webhook is active.
    active = 'active'
    #: Webhook is inactive.
    inactive = 'inactive'


class Webhook(ApiModel):
    #: The unique identifier for the webhook.
    webhook_id: Optional[str] = Field(alias='id', default=None)
    #: A user-friendly name for the webhook.
    name: str
    #: URL that receives POST requests for each event.
    target_url: str
    #: Resource type for the webhook. Creating a webhook requires 'read' scope on the resource the webhook is for.
    resource: Optional[WebhookResource] = None
    #: Event type for the Webhook.
    event: Optional[WebhookEventType] = None
    #: Filter that defines the webhook scope.
    filter: Optional[str] = None
    #: Secret used to generate payload signature.
    secret: Optional[str] = None
    #: Status of the webhook. Use active to reactivate a disabled webhook.
    status: WebhookStatus
    #: Date and time the webhook was created.
    created: datetime.datetime
    org_id: Optional[str] = None
    created_by: Optional[str] = None
    app_id: Optional[str] = None
    #: Specify `org` when creating an org/admin level webhook. Supported for `meetings`, `recordings`,
    #: `convergedRecordings`, `meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`, `controlHubAlerts`,
    #: `rooms`, `messaging` and `adminBatchJobs`  (for Compliance Officers and messages with file attachments only -
    #: see `inline file DLP
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
        extra = 'forbid'

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

    def list(self, owned_by: str = None, **params) -> Generator[Webhook, None, None]:
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
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Webhook, item_key='items', params=params)

    def create(self, name: str, target_url: str, resource: WebhookResource, event: WebhookEventType, filter: str = None,
               secret: str = None,
               owned_by: str = None) -> Webhook:
        """
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
        :param filter: Filter that defines the webhook scope. See `Filtering Webhooks
            <https://developer.webex.com/docs/api/guides/webhooks#filtering-webhooks>`_ for more information. Please note
            that if a filter of `hostEmail`, `hostUserId`, `ownerEmail` or `ownerId` is specified, `ownedBy` must be
            set to `org`.
        :type filter: str
        :param secret: The secret used to generate payload signature.
        :param secret: str
        :param owned_by: Specify `org` when creating an org/admin level webhook. Supported for `meetings`,
            `recordings`, `convergedRecordings`,`meetingParticipants`, `meetingTranscripts`, `videoMeshAlerts`,
            `controlHubAlerts`, `rooms`, `messaging` and `adminBatchJobs` (for Compliance Officers and messages with
            file attachments only - see `inline file DLP
            <https://developer.webex.com/docs/api/guides/webex-real-time-file-dlp-basics>`_) resources.
        :param owned_by: str
        :return: the new webhook
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
        webhook_data = update.model_dump(mode='json', include={'name', 'target_url', 'secret', 'owned_by', 'status'},
                                         exclude_unset=True)
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
