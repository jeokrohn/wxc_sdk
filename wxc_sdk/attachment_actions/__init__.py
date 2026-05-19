"""
Attachment actions API
"""

from datetime import datetime
from typing import Any, Literal, Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.webhook import WebhookEventData

__all__ = ['AttachmentActionsApi', 'AttachmentAction', 'AttachmentActionData']


class AttachmentAction(ApiModel):
    #: A unique identifier for the action.
    id: Optional[str] = None
    #: The ID of the person who performed the action.
    person_id: Optional[str] = None
    #: The ID of the room in which the action was performed.
    room_id: Optional[str] = None
    #: the type of action performed.
    type: Literal['submit']
    #: The ID of the message which contains the attachment.
    message_id: Optional[str] = None
    #: The attachment action's inputs.
    inputs: dict[str, Any]
    #: The date and time the action was created.
    created: Optional[datetime] = None


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
        return AttachmentAction.model_validate(data)

    def create(self, type: str, message_id: str, inputs: dict[str, Any]) -> AttachmentAction:
        """
        Create an Attachment Action

        Create a new attachment action.

        :param type: The type of action to perform.
        :type type: str
        :param message_id: The ID of the message which contains the attachment.
        :type message_id: str
        :param inputs: The attachment action's inputs.
        :type inputs: SubmitCardActionInputs
        :rtype: :class:`AttachmentAction`
        """
        body: dict[str, Any] = dict()
        body['type'] = type
        body['messageId'] = message_id
        body['inputs'] = inputs
        url = self.ep()
        data = super().post(url, json=body)
        r = AttachmentAction.model_validate(data)
        return r
