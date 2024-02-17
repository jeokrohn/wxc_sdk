from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['MeetingMessagesApi']


class MeetingMessagesApi(ApiChild, base='meeting/messages'):
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

    def delete_a_meeting_message(self, meeting_message_id: str):
        """
        Delete a Meeting Message

        Deletes a Meeting Message from the In Meeting Chat, using its ID.

        This ID can be retrieved by a Compliance Officer using the `events API
        <https://developer.webex.com/docs/api/v1/events/list-events>`_ filtering on the `meetingMessages`
        resource type.

        NOTE: When viewing the response from the events API, there are 2 `id` fields. The ID to be used here can be
        found under the `data` field in the response.

        Specify the `meetingMessage` ID in the `meetingMessageId` parameter in the URI.

        :param meeting_message_id: The unique identifier for the message.
        :type meeting_message_id: str
        :rtype: None
        """
        url = self.ep(f'{meeting_message_id}')
        super().delete(url)
