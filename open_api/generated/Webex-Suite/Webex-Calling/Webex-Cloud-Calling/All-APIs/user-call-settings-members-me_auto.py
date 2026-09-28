from __future__ import annotations

import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetMessageSummaryResponse', 'ListVoiceMessageMembershipsResponseMemberOfItem',
           'ListVoiceMessageMembershipsResponseMemberOfItemType', 'UserCallSettingsMembersMeApi',
           'VoiceMailPartyInformation', 'VoiceMessageDetails']


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str] = None
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: `1234`, `2223334444`, `+12223334444`, `*73`, and
    #: `user@company.domain`.
    number: Optional[str] = None
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str] = None
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str] = None
    #: if `true`, denotes privacy is enabled for the name, number and `personId`/`placeId`.
    privacy_enabled: Optional[bool] = None


class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str] = None
    #: The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    duration: Optional[int] = None
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation] = None
    #: `true` if the voicemail message is urgent.
    urgent: Optional[bool] = None
    #: `true` if the voicemail message is confidential.
    confidential: Optional[bool] = None
    #: `true` if the voicemail message has been read.
    read: Optional[bool] = None
    #: Number of pages for the FAX.  Only set for a FAX.
    fax_page_count: Optional[int] = None
    #: The date and time the voicemail message was created.
    created: Optional[datetime] = None


class ListVoiceMessageMembershipsResponseMemberOfItemType(str, Enum):
    call_queue = 'CALL_QUEUE'
    hunt_group = 'HUNT_GROUP'
    auto_attendant = 'AUTO_ATTENDANT'


class ListVoiceMessageMembershipsResponseMemberOfItem(ApiModel):
    #: Unique identifier for the membership.
    id: Optional[str] = None
    #: Type of the membership. One of CALL_QUEUE, HUNT_GROUP, or AUTO_ATTENDANT.
    type: Optional[ListVoiceMessageMembershipsResponseMemberOfItemType] = None
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


class GetMessageSummaryResponse(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int] = None
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int] = None
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int] = None
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int] = None


class UserCallSettingsMembersMeApi(ApiChild, base='telephony/voiceMessages/members/me'):
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

    def list_voice_message_memberships(self) -> builtins.list[ListVoiceMessageMembershipsResponseMemberOfItem]:
        """
        List Voice Message Memberships

        Retrieves the list of shared voicemail memberships for the authenticated user. Each membership represents a
        group calling feature (Call Queue, Hunt Group, or Auto Attendant) whose shared voicemail box the user has
        access to.

        A service may have a phoneNumber, an extension, both, or neither, so any of these optional fields may be absent
        from a given entry. These can be used as values for the `lineOwnerId` parameter in other voicemail APIs.

        This API requires the `spark:calls_read` or `spark:calls_write` scope.

        :rtype: list[ListVoiceMessageMembershipsResponseMemberOfItem]
        """
        url = self.ep('memberships')
        data = super().get(url)
        r = TypeAdapter(list[ListVoiceMessageMembershipsResponseMemberOfItem]).validate_python(data['memberOf'])
        return r

    def get_message_summary(self, line_owner_id: str = None) -> GetMessageSummaryResponse:
        """
        Get Message Summary

        Get a summary of the voicemail messages for the user.

        :param line_owner_id: The ID of a user, workspace, virtual line, auto attendant, hunt group, or call queue for
            which there is a secondary line on a device owned by the authenticated user, or that was shared with the
            authenticated user.
        :type line_owner_id: str
        :rtype: :class:`GetMessageSummaryResponse`
        """
        params: dict[str, Any] = dict()
        if line_owner_id is not None:
            params['lineOwnerId'] = line_owner_id
        url = self.ep('summary')
        data = super().get(url, params=params)
        r = GetMessageSummaryResponse.model_validate(data)
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
