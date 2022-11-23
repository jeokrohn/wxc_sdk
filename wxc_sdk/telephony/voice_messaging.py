"""
Voice messaging API

Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling. The
APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope,
while the other commands require the spark:calls_write scope
"""

from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['MessageSummary', 'VoiceMailPartyInformation', 'VoiceMessageDetails',
           'VoiceMessagingApi']


# noinspection DuplicatedCode
class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, and user@company.domain.
    number: Optional[str]
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str]
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str]
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool]


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str]
    #:  The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    duration: Optional[int]
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation]
    #: true if the voicemail message is urgent.
    urgent: Optional[bool]
    #: true if the voicemail message is confidential.
    confidential: Optional[bool]
    #: true if the voicemail message has been read.
    read: Optional[bool]
    #: Number of pages for the FAX.  Only set for a FAX.
    fax_page_count: Optional[int]
    #: The date and time the voicemail message was created.
    created: Optional[str]


class MessageSummary(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int]
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int]
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int]
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int]


class VoiceMessagingApi(ApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling.  The
    APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while
    the other commands require the spark:calls_write scope.
    """

    def summary(self) -> MessageSummary:
        """
        Get a summary of the voicemail messages for the user.
        """
        url = self.ep('summary')
        data = super().get(url=url)
        return MessageSummary.parse_obj(data)

    def list(self, **params) -> Generator[VoiceMessageDetails, None, None]:
        """
        Get the list of all voicemail messages for the user.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoiceMessageDetails, params=params)

    def delete(self, message_id: str):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        super().delete(url=url)
        return

    def mark_as_read(self, message_id: str):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the messageId is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        """
        body = {'messageId': message_id}
        url = self.ep('markAsRead')
        super().post(url=url, json=body)
        return

    def mark_as_unread(self, message_id: str):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread.  Otherwise, all messages for the user are
        marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the messageId is not
            provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        """
        body = {'messageId': message_id}
        url = self.ep('markAsUnread')
        super().post(url=url, json=body)
        return
