from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = []


class MeetingMessagesApi(ApiChild, base='meeting/messages/{meetingMessageId}'):
    """
    Meeting Messages
    
    Meeting messages are how we communicate through text within an active `Webex Suite meeting
    <https://help.webex.com/en-us/article/m61d8eb/Webex-App-%7C-About-the-Webex-Suite-meeting-platform>`_ or space bound meeting.
    
    The meeting messages are stored in the `/events API
    <https://developer.webex.com/docs/api/v1/events/list-events>`_ with the associated resource type: `meetingMessages`
    
    By default direct messages between two participants in a meeting are treated as ephemeral. Public messages will be
    archived in the /events API, but `can be made ephemeral
    <https://help.webex.com/en-us/article/o1rrjk/Save-or-clear-your-organization's-in-meeting-chats-after-a-meeting>`_ as well.
    
    In a Webex meeting, each meeting message is displayed on its own line along with a timestamp and sender
    information.
    
    Message can contain plain text and `rich text
    <https://developer.webex.com/docs/basics#formatting-messages>`_
    """
    ...