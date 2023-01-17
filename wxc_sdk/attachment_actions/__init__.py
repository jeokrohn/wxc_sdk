"""
Attachment actions API
"""
from datetime import datetime
from typing import Optional, Literal

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.webhook import WebhookEventData

__all__ = ['AttachmentActionsApi', 'AttachmentAction', 'AttachmentActionData']


class AttachmentAction(ApiModel):
    #: A unique identifier for the action.
    id: Optional[str]
    #: The ID of the person who performed the action.
    person_id: Optional[str]
    #: The ID of the room in which the action was performed.
    room_id: Optional[str]
    #: the type of action performed.
    type: Literal['submit']
    #: The ID of the message which contains the attachment.
    message_id: Optional[str]
    #: The attachment action's inputs.
    inputs: dict
    #: The date and time the action was created.
    created: Optional[datetime]


class AttachmentActionData(WebhookEventData):
    """
    Data in a webhook "attachmentActions" event
    """
    resource = 'attachmentActions'
    id: str
    type: Literal['submit']
    message_id: str
    person_id: str
    room_id: str
    created: datetime


class AttachmentActionsApi(ApiChild, base='attachment/actions'):
    """
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a
    card.
    """

    def details(self, action_id: str) -> AttachmentAction:
        """
        Shows details for a attachment action, by ID.
        Specify the attachment action ID in the id URI parameter.

        :param action_id: A unique identifier for the attachment action.
        :type action_id: str
        """
        url = self.ep(f'{action_id}')
        data = super().get(url=url)
        return AttachmentAction.parse_obj(data)
