from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AttachmentAction', 'AttachmentActivity', 'AttachmentActivityType', 'SubmitCardAction', 'SubmitCardActionInputs', 'SubmitCardActionResponse']


class AttachmentAction(ApiModel):
    ...


class SubmitCardActionInputs(ApiModel):
    #: example: John Andersen
    Name: Optional[str] = None
    #: example: https://example.com
    Url: Optional[str] = None
    #: example: john.andersen@example.com
    Email: Optional[str] = None
    #: example: +1 408 555 7209
    Tel: Optional[str] = None


class AttachmentActivityType(str, Enum):
    submit = 'submit'


class SubmitCardAction(AttachmentAction):
    #: Type of action
    #: example: submit
    type: Optional[AttachmentActivityType] = None
    #: The parent message on which the attachment action was performed.
    #: example: GFyazovL3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI4NC
    messageId: Optional[str] = None
    inputs: Optional[SubmitCardActionInputs] = None


class SubmitCardActionResponse(SubmitCardAction):
    #: The unique identifier of the action.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    id: Optional[str] = None
    #: The person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZ
    personId: Optional[str] = None
    #: The room in which the action was performed.
    #: example: L3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI
    roomId: Optional[str] = None
    #: The timestamp of the action.
    #: example: 2016-05-10T19:41:00.100Z
    created: Optional[datetime] = None


class AttachmentActivity(ApiModel):
    #: A unique identifier for the action.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    id: Optional[str] = None
    #: The ID of the person who performed the action.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTZlOWQxYy1jYTQ0LTRmZ
    personId: Optional[str] = None
    #: The ID of the room in which the action was performed.
    #: example: L3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI
    roomId: Optional[str] = None
    #: The type of action performed.
    #: example: submit
    type: Optional[AttachmentActivityType] = None
    #: The parent message on which the attachment action was performed.
    #: example: GFyazovL3VzL1BFT1BMRS80MDNlZmUwNy02Yzc3LTQyY2UtOWI4NC
    messageId: Optional[str] = None
    #: The action's inputs.
    inputs: Optional[SubmitCardActionInputs] = None
    #: The date and time the action was created.
    #: example: 2016-05-10T19:41:00.100Z
    created: Optional[datetime] = None
