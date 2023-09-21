from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Webhook', 'WebhookCollectionResponse', 'WebhookEvent', 'WebhookResource', 'WebhookStatus']


class WebhookResource(str, Enum):
    #: The [Attachment Actions](/docs/api/v1/attachment-actions) resource.
    attachment_actions = 'attachmentActions'
    #: The [Memberships](/docs/api/v1/memberships) resource.
    memberships = 'memberships'
    #: The [Messages](/docs/api/v1/messages) resource.
    messages = 'messages'
    #: The [Rooms](/docs/api/v1/rooms) resource.
    rooms = 'rooms'
    #: The [Meetings](/docs/api/v1/meetings) resource.
    meetings = 'meetings'
    #: The [Recordings](/docs/api/v1/recordings) resource.
    recordings = 'recordings'
    #: The [Meeting Participants](/docs/api/v1/meeting-participants) resource.
    meeting_participants = 'meetingParticipants'
    #: The [Meeting Transcripts](/docs/api/v1/meeting-transcripts) resource.
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
    #: Specified when creating an org/admin level webhook.
    #: example: org
    owned_by: Optional[str] = None


class WebhookCollectionResponse(ApiModel):
    items: Optional[list[Webhook]] = None
