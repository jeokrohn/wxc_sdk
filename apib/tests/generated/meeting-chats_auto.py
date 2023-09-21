from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ChatObject', 'ChatObjectSender']


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
    #: Chat time for the chat snippet in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format.
    #: example: 2021-07-06T09:22:34Z
    chat_time: Optional[datetime] = None
    #: The text of the chat snippet.
    #: example: hi
    text: Optional[str] = None
    #: A unique identifier for the [meeting instance](/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances) to which the chat belongs.
    #: example: a2f95f5073e347489f7611492dbd6ad5_I_199075330905867928
    meeting_id: Optional[str] = None
    #: Whether the type of the chat is private, public or group. Private chat is for the 1:1 chat. Public chat is for the message which is sent to all the people in the meeting. Group chat is for the message which is sent to a small group of people, like a message to "host and presenter".
    #: example: private
    type: Optional[str] = None
    #: Information of the sender of the chat snippet.
    sender: Optional[ChatObjectSender] = None
    #: Information of the receivers of the chat snippet.
    receivers: Optional[list[ChatObjectSender]] = None
