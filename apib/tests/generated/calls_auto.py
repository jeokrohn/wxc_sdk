from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
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
    room_id: Optional[str] = None
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


class CallsApi(ApiChild, base='calls'):
    """
    Calls
    
    The Calls functionality and API endpoints described here are currently pre-
    release features which are not available to all Webex users. If you have any
    questions, or if you need help, please contact the Webex Developer Support
    team at devsupport@webex.com.
    
    
    
    Calls represent real-time, collaborative meetings between two or more people. Calls take place in permanent or
    temporary Webex `Spaces (rooms)
    <https://developer.webex.com/docs/api/v1/rooms>`_. To see the participants of a call, use the `Call Memberships API
    
    For more information about Calls, see the `Calls
    <https://developer.webex.com/docs/api/guides/calls>`_ guide.
    """
    ...