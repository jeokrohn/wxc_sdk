from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Call', 'CallStatus', 'CallsCollectionResponse']


class CallStatus(str, Enum):
    #: A scheduled call that may be joined.
    initializing = 'initializing'
    #: An initialized call with at least one participant waiting to join.
    lobby = 'lobby'
    #: An in-progress call with active participants.
    connected = 'connected'
    #: A call that is ending but may still have active participants.
    terminating = 'terminating'
    #: A call that has ended.
    disconnected = 'disconnected'


class Call(ApiModel):
    #: A unique identifier for the call.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    id: Optional[str] = None
    #: The room ID for the call.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    roomId: Optional[str] = None
    #: The current state of the call.
    #: example: connected
    status: Optional[CallStatus] = None
    #: The current duration of the call in seconds.
    #: example: 180.0
    duration: Optional[int] = None
    #: The date and time when the call was created.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None


class CallsCollectionResponse(ApiModel):
    items: Optional[list[Call]] = None
