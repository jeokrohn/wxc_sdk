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


__all__ = ['AttachmentActionsApi', 'AttachmentActivity', 'SubmitCardActionInputs', 'SubmitCardActionType']


class SubmitCardActionType(str, Enum):
    submit = 'submit'


class SubmitCardActionInputs(ApiModel):
    name: Optional[str] = Field(alias='Name', default=None)
    url: Optional[str] = Field(alias='Url', default=None)
    email: Optional[str] = Field(alias='Email', default=None)
    tel: Optional[str] = Field(alias='Tel', default=None)


class AttachmentActivity(ApiModel):
    #: A unique identifier for the action.
    id: Optional[str] = None
    #: The ID of the person who performed the action.
    person_id: Optional[str] = None
    #: The ID of the room in which the action was performed.
    room_id: Optional[str] = None
    #: The type of action performed.
    type: Optional[SubmitCardActionType] = None
    #: The parent message on which the attachment action was performed.
    message_id: Optional[str] = None
    #: The action's inputs.
    inputs: Optional[SubmitCardActionInputs] = None
    #: The date and time the action was created.
    created: Optional[datetime] = None


class AttachmentActionsApi(ApiChild, base='attachment/actions'):
    """
    Attachment Actions
    
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a
    `card
    <https://developer.webex.com/docs/api/guides/cards>`_.
    """

    def create_an_attachment_action(self, type: SubmitCardActionType, message_id: str,
                                    inputs: SubmitCardActionInputs) -> AttachmentActivity:
        """
        Create an Attachment Action

        Create a new attachment action.

        :param type: The type of action to perform.
        :type type: SubmitCardActionType
        :param message_id: The ID of the message which contains the attachment.
        :type message_id: str
        :param inputs: The attachment action's inputs.
        :type inputs: SubmitCardActionInputs
        :rtype: :class:`AttachmentActivity`
        """
        body: dict[str, Any] = dict()
        body['type'] = enum_str(type)
        body['messageId'] = message_id
        body['inputs'] = inputs.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        data = super().post(url, json=body)
        r = AttachmentActivity.model_validate(data)
        return r

    def get_attachment_action_details(self, id: str) -> AttachmentActivity:
        """
        Get Attachment Action Details

        Shows details for a attachment action, by ID.

        Specify the attachment action ID in the `id` URI parameter.

        :param id: A unique identifier for the attachment action.
        :type id: str
        :rtype: :class:`AttachmentActivity`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = AttachmentActivity.model_validate(data)
        return r
