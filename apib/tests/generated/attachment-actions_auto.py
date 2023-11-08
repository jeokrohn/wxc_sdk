from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AttachmentAction', 'AttachmentActivity', 'AttachmentActivityType', 'SubmitCardAction',
            'SubmitCardActionInputs', 'SubmitCardActionResponse']


class AttachmentAction(ApiModel):
    ...


class SubmitCardActionInputs(ApiModel):
    #: example: John Andersen
    name: Optional[str] = Field(alias='Name', default=None)
    #: example: https://example.com
    url: Optional[str] = Field(alias='Url', default=None)
    #: example: john.andersen@example.com
    email: Optional[str] = Field(alias='Email', default=None)
    #: example: +1 408 555 7209
    tel: Optional[str] = Field(alias='Tel', default=None)


class AttachmentActivityType(str, Enum):
    submit = 'submit'


class SubmitCardAction(AttachmentAction):
    #: Type of action
    #: example: submit
    type: Optional[AttachmentActivityType] = None
    #: The parent message on which the attachment action was performed.
    #: example: GFyazovL3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI4NC
    message_id: Optional[str] = None
    inputs: Optional[SubmitCardActionInputs] = None


class SubmitCardActionResponse(SubmitCardAction):
    #: The unique identifier of the action.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    id: Optional[str] = None
    #: The person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZ
    person_id: Optional[str] = None
    #: The room in which the action was performed.
    #: example: L3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI
    room_id: Optional[str] = None
    #: The timestamp of the action.
    #: example: 2016-05-10T19:41:00.100Z
    created: Optional[datetime] = None


class AttachmentActivity(ApiModel):
    #: A unique identifier for the action.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    id: Optional[str] = None
    #: The ID of the person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZ
    person_id: Optional[str] = None
    #: The ID of the room in which the action was performed.
    #: example: L3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI
    room_id: Optional[str] = None
    #: The type of action performed.
    #: example: submit
    type: Optional[AttachmentActivityType] = None
    #: The parent message on which the attachment action was performed.
    #: example: GFyazovL3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI4NC
    message_id: Optional[str] = None
    #: The action's inputs.
    inputs: Optional[SubmitCardActionInputs] = None
    #: The date and time the action was created.
    #: example: 2016-05-10T19:41:00.100Z
    created: Optional[datetime] = None


class AttachmentActionsApi(ApiChild, base='attachment/actions'):
    """
    Attachment Actions
    
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a
    `card
    <https://developer.webex.com/docs/api/guides/cards>`_.
    """

    def create_an_attachment_action(self, type: AttachmentActivityType, message_id: str,
                                    inputs: SubmitCardActionInputs) -> AttachmentActivity:
        """
        Create an Attachment Action

        Create a new attachment action.

        :param type: The type of action to perform.
        :type type: AttachmentActivityType
        :param message_id: The ID of the message which contains the attachment.
        :type message_id: str
        :param inputs: The attachment action's inputs.
        :type inputs: SubmitCardActionInputs
        :rtype: :class:`AttachmentActivity`
        """
        ...


    def get_attachment_action_details(self, id: str) -> AttachmentActivity:
        """
        Get Attachment Action Details

        Shows details for a attachment action, by ID.
        
        Specify the attachment action ID in the `id` URI parameter.

        :param id: A unique identifier for the attachment action.
        :type id: str
        :rtype: :class:`AttachmentActivity`
        """
        ...

    ...