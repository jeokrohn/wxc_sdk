from collections.abc import Generator
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel

__all__ = ['Sender', 'ChatObject', 'MeetingChatsApi']


class Sender(ApiModel):
    #: Email address for sender.
    #: Possible values: john.andersen@example.com
    email: Optional[str]
    #: Display name for sender.
    #: Possible values: John Andersen
    display_name: Optional[str]
    #: A unique identifier for the sender.
    person_id: Optional[str]
    #: The ID of the organization to which the sender belongs.
    org_id: Optional[str]


class ChatObject(ApiModel):
    #: A unique identifier for the chat snippet.
    id: Optional[str]
    #: Chat time for the chat snippet in ISO 8601 compliant format.
    chat_time: Optional[str]
    #: The text of the chat snippet.
    text: Optional[str]
    #: A unique identifier for the meeting instance to which the chat belongs.
    meeting_id: Optional[str]
    #: Whether the type of the chat is private, public or group. Private chat is for the 1:1 chat. Public chat is for the message which is sent to all the people in the meeting. Group chat is for the message which is sent to a small group of people, like a message to "host and presenter".
    type: Optional[str]
    #: Information of the sender of the chat snippet.
    sender: Optional[Sender]
    #: Information of the receivers of the chat snippet.
    receivers: Optional[list[Sender]]


class MeetingChatsApi(ApiChild, base='meetings/postMeetingChats'):
    """
    Chats are content captured in a meeting when chat messages are sent between the participants within a meeting. This feature allows a Compliance Officer to access the in-meeting chat content.
    The Compliance Officer can use the Meeting Chats API to retrieve the chats of a meeting and to delete all chats associated with a meeting. private chats are text messages between two people. group chats are for larger breakout spaces. Meeting chats are different from room messages in that there is no catch-up propagation. For example, if a user joins a meeting late only, chat messages that are created from then on, will be propagated to this user. To understand which user saw which message if they joined late, you have to query the meetingParticipants REST resource for the joined/left times and compare to the meetingsChat chatTime field.
    The Webex meetings chat functionality and API endpoint described here is "upon-request" and not enabled by default. If you need it enabled for your org, or if you need help, please contact the Webex Developer Support team at devsupport@webex.com.
    """

    def list(self, meeting_id: str, offset: int = None, **params) -> Generator[ChatObject, None, None]:
        """
        Lists the meeting chats of a finished meeting instance specified by meetingId. You can set a maximum number of chats to return.
        Use this operation to list the chats of a finished meeting instance when they are ready. Please note that only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. The meeting ID of a scheduled personal room meeting is not supported.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ChatObject, params=params)

    def delete(self, meeting_id: str):
        """
        Deletes the meeting chats of a finished meeting instance specified by meetingId.
        Use this operation to delete the chats of a finished meeting instance when they are ready. Please note that only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. Meeting IDs of a scheduled personal room meeting are not supported.
        :type meeting_id: str
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        super().delete(url=url, params=params)
        return
