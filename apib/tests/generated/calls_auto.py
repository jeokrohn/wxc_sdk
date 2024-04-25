from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Call', 'CallStatus', 'CallsApi']


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
    #: example: 180
    duration: Optional[int] = None
    #: The date and time when the call was created.
    #: example: 2016-04-21T17:00:00.000Z
    created: Optional[datetime] = None


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

    def list_calls(self, status: CallStatus, room_id: str = None, from_: Union[str, datetime] = None, to_: Union[str,
                   datetime] = None, **params) -> Generator[Call, None, None]:
        """
        List Calls

        Lists all calls that the authenticated user either initiated or was invited to.

        To list currently active calls, use `connected` for the `status` query parameter; for call history, use
        `disconnected`. Use the `from` and `to` parameters to specify a time period. By default, call information is
        kept for 90 days.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param status: List calls with this state.
        :type status: CallStatus
        :param room_id: List calls placed in the specified room.
        :type room_id: str
        :param from_: Limit to calls that started from the inclusive start date, in ISO8601 format.
        :type from_: Union[str, datetime]
        :param to_: Limit to calls that ended before the exclusive end date, in ISO8601 format.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`Call` instances
        """
        params['status'] = enum_str(status)
        if room_id is not None:
            params['roomId'] = room_id
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Call, item_key='items', params=params)

    def get_call_details(self, call_id: str) -> Call:
        """
        Get Call Details

        Shows details for a call, by call ID.

        Specify the call ID in the `callId` parameter in the URI.

        :param call_id: The unique identifier for the call.
        :type call_id: str
        :rtype: :class:`Call`
        """
        url = self.ep(f'{call_id}')
        data = super().get(url)
        r = Call.model_validate(data)
        return r
