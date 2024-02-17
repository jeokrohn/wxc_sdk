from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ChatObject', 'ChatObjectSender', 'MeetingChatsApi']


class ChatObjectSender(ApiModel):
    #: Email address of the sender of the meeting chat snippet.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Display name for the sender.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: A unique identifier for the sender.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81YmVkZWUyMC1hNjI3LTQ4YTUtODg0Yi04NjVhODhlZmFhNzM
    person_id: Optional[str] = None
    #: The ID of the organization to which the sender belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81OWU2NzUyNy00NjUxLTRjOTAtYjJmMC00Zjg2YzNiYjY2MDg
    org_id: Optional[str] = None


class ChatObject(ApiModel):
    #: A unique identifier for the chat snippet.
    #: example: 1aea8390-e375-4547-b7ff-58ecd9e0b03d
    id: Optional[str] = None
    #: Chat time for the chat snippet in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    #: example: 2021-07-06T09:22:34Z
    chat_time: Optional[datetime] = None
    #: The text of the chat snippet.
    #: example: hi
    text: Optional[str] = None
    #: A unique identifier for the `meeting instance
    #: <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the chat belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: Whether the type of the chat is private, public or group. Private chat is for the 1:1 chat. Public chat is for
    #: the message which is sent to all the people in the meeting. Group chat is for the message which is sent to a
    #: small group of people, like a message to "host and presenter".
    #: example: private
    type: Optional[str] = None
    #: Information of the sender of the chat snippet.
    sender: Optional[ChatObjectSender] = None
    #: Information of the receivers of the chat snippet.
    receivers: Optional[list[ChatObjectSender]] = None


class MeetingChatsApi(ApiChild, base='meetings/postMeetingChats'):
    """
    Meeting Chats
    
    Chats are content captured in a meeting when chat messages are sent between the participants within a meeting. This
    feature allows a Compliance Officer to access the in-meeting chat content.
    
    The Compliance Officer can use the Meeting Chats API to retrieve the chats of a meeting and to delete all chats
    associated with a meeting. `private` chats are text messages between two people. `group` chats are for larger
    breakout spaces. Meeting chats are different from room messages in that there is no catch-up propagation. For
    example, if a user joins a meeting late only, chat messages that are created from then on, will be propagated to
    this user. To understand which user saw which message if they joined late, you have to query the
    `meetingParticipants` REST resource for the joined/left times and compare to the `meetingsChat` `chatTime` field.
    
    The Webex meetings chat functionality and API endpoint described here is
    "upon-request" and not enabled by default. If you need it enabled for your
    org, or if you need help, please contact the Webex Developer Support team at
    devsupport@webex.com.
    
    
    
    Meetings on the Webex Meetings Suite platform rely on enhanced meeting chat
    functionality, powered by a different backend. To access meeting chats in the
    Webex Suite, please see the `meetingMessages
    <https://developer.webex.com/docs/api/v1/meeting-messages>`_
    resource.
    
    """

    def list_meeting_chats(self, meeting_id: str, **params) -> Generator[ChatObject, None, None]:
        """
        List Meeting Chats

        Lists the meeting chats of a finished `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ specified by `meetingId`. You can set a maximum number
        of chats to return.

        Use this operation to list the chats of a finished `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ when they are ready. Please note that only
        **meeting instances** in state `ended` are supported for `meetingId`. **Meeting series**, **scheduled
        meetings** and `in-progress` **meeting instances** are not supported.

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the chats belong. The meeting ID of a
            scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported.
        :type meeting_id: str
        :return: Generator yielding :class:`ChatObject` instances
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ChatObject, item_key='items', params=params)

    def delete_meeting_chats(self, meeting_id: str):
        """
        Delete Meeting Chats

        Deletes the meeting chats of a finished `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ specified by `meetingId`.

        Use this operation to delete the chats of a finished `meeting instance
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ when they are ready. Please note that
        only **meeting instances** in state `ended` are supported for `meetingId`. **Meeting series**, **scheduled
        meetings** and `in-progress` **meeting instances** are not supported.

        :param meeting_id: A unique identifier for the `meeting instance
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ to which the chats belong. Meeting IDs of a
            scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting are not supported.
        :type meeting_id: str
        :rtype: None
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        super().delete(url, params=params)
