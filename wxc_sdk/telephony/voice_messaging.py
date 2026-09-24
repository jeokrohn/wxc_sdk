"""
Voice messaging API

Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling. The
APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope,
while the other commands require the spark:calls_write scope
"""

import builtins
from collections.abc import Generator
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = [
    'MessageSummary',
    'VoiceMailPartyInformation',
    'VoiceMessageDetails',
    'VoiceMessageMembership',
    'VoiceMessagingApi',
]


# noinspection DuplicatedCode
class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, and user@company.domain.
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str] = None
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool] = None


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str] = None
    #:  The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    duration: Optional[int] = None
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation] = None
    #: true if the voicemail message is urgent.
    urgent: Optional[bool] = None
    #: true if the voicemail message is confidential.
    confidential: Optional[bool] = None
    #: true if the voicemail message has been read.
    read: Optional[bool] = None
    #: Number of pages for the FAX.  Only set for a FAX.
    fax_page_count: Optional[int] = None
    #: The date and time the voicemail message was created.
    created: Optional[str] = None


class MessageSummary(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int] = None
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int] = None
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int] = None
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int] = None


class VoiceMessageMembership(ApiModel):
    #: Unique identifier for the membership.
    id: Optional[str] = None
    #: Type of the membership. One of CALL_QUEUE, HUNT_GROUP, or AUTO_ATTENDANT.
    type: Optional[str] = None
    #: Display name of the call queue, hunt group, or auto attendant.
    name: Optional[str] = None
    #: Phone number in E.164 format. Omitted when the service has no phone number.
    phone_number: Optional[str] = None
    #: Extension number. Omitted when the service has no extension.
    extension: Optional[str] = None
    #: Location dialing code (routing prefix). Omitted when not set.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Number, the concatenation of routingPrefix and extension. Omitted when not set.
    esn: Optional[str] = None


class VoiceMessagingApi(ApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling.  The
    APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while
    the other commands require the spark:calls_write scope.
    """

    def summary(self, line_owner_id: str = None) -> MessageSummary:
        """
        Get a summary of the voicemail messages for the user.

        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the user invoking the API, or that was shared with
            the user invoking the API.
        :type line_owner_id: str
        """
        params = {}
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep('summary')
        data = super().get(url=url, params=params)
        return MessageSummary.model_validate(data)

    def list(self, line_owner_id: str = None, **params) -> Generator[VoiceMessageDetails, None, None]:
        """
        Get the list of all voicemail messages for the user.

        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the user invoking the API, or that was shared with
            the user invoking the API.
        :type line_owner_id: str
        """
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoiceMessageDetails, params=params)

    def delete(self, message_id: str, line_owner_id: str = None):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifier of the voicemail message to delete
        :type message_id: str
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the user invoking the API, or that was shared with
            the user invoking the API.
        :type line_owner_id: str
        """
        params = {}
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep(f'{message_id}')
        super().delete(url=url, params=params)
        return

    def mark_as_read(self, message_id: str, line_owner_id: str = None):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the messageId is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the user invoking the API, or that was shared with
            the user invoking the API.
        :type line_owner_id: str
        """
        body = {'messageId': message_id}
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('markAsRead')
        super().post(url=url, json=body)
        return

    def mark_as_unread(self, message_id: str, line_owner_id: str = None):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread.  Otherwise, all messages for the user are
        marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the messageId is not
            provided, then all voicemail messages for the user are marked as unread.
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the user invoking the API, or that was shared with
            the user invoking the API.
        :type line_owner_id: str
        :type message_id: str
        """
        body = {'messageId': message_id}
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('markAsUnread')
        super().post(url=url, json=body)
        return

    def memberships(self) -> builtins.list[VoiceMessageMembership]:
        """
        List Voice Message Memberships

        Retrieves the list of shared voicemail memberships for the authenticated user. Each membership represents a
        group calling feature (Call Queue, Hunt Group, or Auto Attendant) whose shared voicemail box the user has
        access to.

        A service may have a phoneNumber, an extension, both, or neither, so any of these optional fields may be absent
        from a given entry. These can be used as values for the `lineOwnerId` parameter in other voicemail APIs.

        This API requires a full, user, or read-only administrator auth token with a scope of `spark-admin:people_read`
        or a user auth token with `spark:people_read` scope.

        :rtype: list[VoiceMessageMembership]
        """
        url = self.ep('memberships')
        data = super().get(url)
        r = TypeAdapter(list[VoiceMessageMembership]).validate_python(data['memberOf'])
        return r
