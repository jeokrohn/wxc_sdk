from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallMembership', 'CallMembershipAudio', 'CallMembershipStatus', 'CallMembershipsApi',
           'ListCallMembershipsCallStatus', 'ListCallMembershipsIsHost']


class CallMembershipStatus(str, Enum):
    notified = 'notified'
    joined = 'joined'
    declined = 'declined'
    left = 'left'
    waiting = 'waiting'


class CallMembershipAudio(str, Enum):
    on = 'on'
    off = 'off'


class CallMembership(ApiModel):
    #: A unique identifier for the call membership.
    #: example: Y2lzY29zcGFyazovL3VzL01FTUJFUlNISVAvMGQwYzkxYjYtY2U2MC00NzI1LWI2ZDAtMzQ1NWQ1ZDExZWYzOmNkZTFkZDQwLTJmMGQtMTFlNS1iYTljLTdiNjU1NmQyMjA3Yg
    id: Optional[str] = None
    #: The status of the call membership.
    #: example: joined
    status: Optional[CallMembershipStatus] = None
    #: The call ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    call_id: Optional[str] = None
    #: Whether or not the person referenced by this membership hosted the call.
    #: example: True
    is_host: Optional[bool] = None
    #: The fully qualified SIP address of the participant, if not a known Webex user.
    #: example: sip:john.andersen@example.com
    sip_url: Optional[str] = None
    #: The E.164 PSTN address of the participant, if not a known Webex user.
    #: example: +14155551212
    phone_number: Optional[str] = None
    #: The room ID of the call.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: List of device IDs associated to the participant.
    #: example: ['22ecb593-8408-4fe5-81bb-0d92d568f93f', '2345aea8-7a8b-4861-982a-26c792e21c17']
    device_ids: Optional[list[str]] = None
    #: Whether or not the participant is in the same organization.
    is_guest: Optional[bool] = None
    #: The organization ID of the participant if they are a guest.
    #: example: ``
    org_id: Optional[str] = None
    #: The total amount of time, in seconds, that the membership was in a "joined" state.
    #: example: 180
    joined_duration: Optional[int] = None
    #: The current status of the audio stream.
    #: example: on
    audio: Optional[CallMembershipAudio] = None
    #: The current status of the video stream.
    #: example: on
    video: Optional[CallMembershipAudio] = None
    #: The current status of the whiteboard stream.
    #: example: off
    slide: Optional[CallMembershipAudio] = None
    #: The date and time when the call membership was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class ListCallMembershipsCallStatus(str, Enum):
    initializing = 'initializing'
    lobby = 'lobby'
    connected = 'connected'
    terminating = 'terminating'
    disconnected = 'disconnected'


class ListCallMembershipsIsHost(str, Enum):
    true = 'true'


class CallMembershipsApi(ApiChild, base='call/memberships'):
    """
    Call Memberships
    
    The Call Memberships functionality and API endpoints described here are
    currently pre-release features which are not available to all Webex users. If
    you have any questions, or if you need help, please contact the Webex
    Developer Support team at devsupport@webex.com.
    
    
    
    Call Memberships represent a person's relationship to a call. Use this API to list members of any call that you're
    in or have been invited to.
    
    To see information about calls, use the `Calls API
    <https://developer.webex.com/docs/api/v1/calls>`_.
    
    For more information about Calls and Call Memberships, see the `Calls
    <https://developer.webex.com/docs/api/guides/calls>`_ guide.
    """

    def list_call_memberships(self, call_status: ListCallMembershipsCallStatus, call_id: str = None,
                              is_host: ListCallMembershipsIsHost = None, person_id: str = None,
                              status: CallMembershipStatus = None, from_: Union[str, datetime] = None, to_: Union[str,
                              datetime] = None, **params) -> Generator[CallMembership, None, None]:
        """
        List call memberships.

        By default, lists call memberships for all calls in which the authenticated user is an active participant.
        Viewing all call memberships in your Organization requires an administrator auth token with the
        `spark-admin:call_memberships_read` scope.

        Use query parameters to filter the result set. Results are in descending `created` order.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param call_status: Limit results to call memberships for calls with the specified status.
        :type call_status: ListCallMembershipsCallStatus
        :param call_id: Limit results to call memberships for a call, by call ID.
        :type call_id: str
        :param is_host: Limit results to call memberships for calls hosted by the authenticated user.
        :type is_host: ListCallMembershipsIsHost
        :param person_id: Limit results to call memberships belonging to a person, by person ID.
        :type person_id: str
        :param status: Limit to call memberships with the specified status.
        :type status: CallMembershipStatus
        :param from_: Limit results to call memberships for calls that started from the inclusive start date, in
            ISO8601 format.
        :type from_: Union[str, datetime]
        :param to_: Limit results to call memberships for calls that ended before the exclusive end date, in ISO8601
            format.
        :type to_: Union[str, datetime]
        :return: Generator yielding :class:`CallMembership` instances
        """
        params['callStatus'] = enum_str(call_status)
        if call_id is not None:
            params['callId'] = call_id
        if is_host is not None:
            params['isHost'] = enum_str(is_host)
        if person_id is not None:
            params['personId'] = person_id
        if status is not None:
            params['status'] = enum_str(status)
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
        return self.session.follow_pagination(url=url, model=CallMembership, item_key='items', params=params)

    def get_call_membership_details(self, call_membership_id: str) -> CallMembership:
        """
        Get Call Membership Details

        Shows details for a call, by call ID.

        Specify the call ID in the `callId` parameter in the URI.

        :param call_membership_id: The unique identifier for the call membership.
        :type call_membership_id: str
        :rtype: :class:`CallMembership`
        """
        url = self.ep(f'{call_membership_id}')
        data = super().get(url)
        r = CallMembership.model_validate(data)
        return r
