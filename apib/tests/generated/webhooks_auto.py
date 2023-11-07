from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Webhook', 'WebhookCollectionResponse', 'WebhookEvent', 'WebhookResource', 'WebhookStatus']


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


class WebhookCollectionResponse(ApiModel):
    items: Optional[list[Webhook]] = None


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
    ...