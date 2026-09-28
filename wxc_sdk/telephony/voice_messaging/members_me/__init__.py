from __future__ import annotations

import builtins
from typing import Any

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.telephony.voice_messaging.members import MessageSummary, VoiceMessageDetails, VoiceMessageMembership

__all__ = ['UserVoiceMessagingMembersMeApi']


class UserVoiceMessagingMembersMeApi(ApiChild, base='telephony/voiceMessages/members/me'):
    """
    User Call Settings Members Me

    Voice Messages APIs for the authenticated user in support of Webex Calling. All commands require the
    `spark:calls_read` or `spark:calls_write` scope.

    These APIs support the optional `lineOwnerId` parameter, which allows users to access voicemail for shared lines on
    their devices or for hunt groups, call queues, and auto attendants explicitly shared with them.
    """

    def mark_as_read(self, message_id: str = None, line_owner_id: str = None) -> None:
        """
        Mark As Read

        Update the voicemail message(s) as read for the user.

        If the `messageId` is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the `messageId` is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if message_id is not None:
            body['messageId'] = message_id
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('markAsRead')
        super().post(url, json=body)

    def mark_as_unread(self, message_id: str = None, line_owner_id: str = None) -> None:
        """
        Mark As Unread

        Update the voicemail message(s) as unread for the user.

        If the `messageId` is provided, then only mark that message as unread.  Otherwise, all messages for the user
        are marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the `messageId` is
            not provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if message_id is not None:
            body['messageId'] = message_id
        if line_owner_id is not None:
            body['lineOwnerId'] = line_owner_id
        url = self.ep('markAsUnread')
        super().post(url, json=body)

    def list_voice_message_memberships(self) -> builtins.list[VoiceMessageMembership]:
        """
        List Voice Message Memberships

        Retrieves the list of shared voicemail memberships for the authenticated user. Each membership represents a
        group calling feature (Call Queue, Hunt Group, or Auto Attendant) whose shared voicemail box the user has
        access to.

        A service may have a phoneNumber, an extension, both, or neither, so any of these optional fields may be absent
        from a given entry. These can be used as values for the `lineOwnerId` parameter in other voicemail APIs.

        This API requires the `spark:calls_read` or `spark:calls_write` scope.

        :rtype: list[VoiceMessageMembership]
        """
        url = self.ep('memberships')
        data = super().get(url)
        r = TypeAdapter(list[VoiceMessageMembership]).validate_python(data['memberOf'])
        return r

    def get_message_summary(self, line_owner_id: str = None) -> MessageSummary:
        """
        Get Message Summary

        Get a summary of the voicemail messages for the user.

        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: :class:`MessageSummary`
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep('summary')
        data = super().get(url, params=params)
        r = MessageSummary.model_validate(data)
        return r

    def list_messages(self, line_owner_id: str = None) -> builtins.list[VoiceMessageDetails]:
        """
        List Messages

        Get the list of all voicemail messages for the user.

        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: list[VoiceMessageDetails]
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep('voiceMessages')
        data = super().get(url, params=params)
        r = TypeAdapter(list[VoiceMessageDetails]).validate_python(data['items'])
        return r

    def delete_message(self, message_id: str, line_owner_id: str = None) -> None:
        """
        Delete Message

        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep(f'voiceMessages/{message_id}')
        super().delete(url, params=params)
