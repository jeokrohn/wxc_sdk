"""
Voice messaging API

Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling. The
APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope,
while the other commands require the spark:calls_write scope
"""

import builtins
from collections.abc import Generator
from dataclasses import dataclass

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.rest import RestSession
from wxc_sdk.telephony.voice_messaging.members import (
    MessageSummary,
    UserVoiceMessagingMembersApi,
    VoiceMessageDetails,
    VoiceMessageMembership,
)
from wxc_sdk.telephony.voice_messaging.members_me import UserVoiceMessagingMembersMeApi

__all__ = [
    'VoiceMessagingApi',
]


@dataclass(init=False, repr=False)
class VoiceMessagingApi(ApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling.  The
    APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while
    the other commands require the spark:calls_write scope.
    """

    #: voice messaging members API
    members: UserVoiceMessagingMembersApi
    members_me: UserVoiceMessagingMembersMeApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.members = UserVoiceMessagingMembersApi(session=session)
        self.members_me = UserVoiceMessagingMembersMeApi(session=session)

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
