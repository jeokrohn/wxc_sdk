from __future__ import annotations

import builtins
from datetime import datetime
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = [
    'MessageSummary',
    'VoiceMessageMembership',
    'UserVoiceMessagingMembersApi',
    'VoiceMailPartyInformation',
    'VoiceMessageDetails',
]


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


class MessageSummary(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int] = None
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int] = None
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int] = None
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int] = None


class UserVoiceMessagingMembersApi(ApiChild, base='telephony/voiceMessages/members'):
    """
    User Call Settings Members

    Voice Messages APIs for members (person, workspace, virtual line, hunt group, call queue, or auto attendant) in
    support of Webex Calling. All `GET` commands require the `spark-admin:calls_read` scope while all other commands
    require the `spark-admin:calls_write` scope.
    """

    def mark_as_read(self, member_id: str, message_id: str = None, org_id: str = None) -> None:
        """
        Mark As Read by Member ID

        Update the voicemail message(s) as read for the user.

        If the `messageId` is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param message_id: The voicemail message identifier of the message to mark as read.  If the `messageId` is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep(f'{member_id}/markAsRead')
        super().post(url, params=params, json=body)

    def mark_as_unread(self, member_id: str, message_id: str = None, org_id: str = None) -> None:
        """
        Mark As Unread by Member ID

        Update the voicemail message(s) as unread for the user.

        If the `messageId` is provided, then only mark that message as unread.  Otherwise, all messages for the user
        are marked as unread.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param message_id: The voicemail message identifier of the message to mark as unread.  If the `messageId` is
            not provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep(f'{member_id}/markAsUnread')
        super().post(url, params=params, json=body)

    def memberships(self, member_id: str, org_id: str = None) -> builtins.list[VoiceMessageMembership]:
        """
        List Voice Message Memberships

        Retrieves the list of shared voicemail memberships for the specified member. Each membership represents a group
        calling feature (Call Queue, Hunt Group, or Auto Attendant) whose shared voicemail box the member has access
        to.

        A service may have a phoneNumber, an extension, both, or neither, so any of these optional fields may be absent
        from a given entry.

        This API requires the `spark-admin:calls_read` or `spark-admin:calls_write` scope.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: list[VoiceMessageMembership]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/memberships')
        data = super().get(url, params=params)
        r = TypeAdapter(list[VoiceMessageMembership]).validate_python(data['memberOf'])
        return r

    def summary(self, member_id: str, org_id: str = None) -> MessageSummary:
        """
        Get Message Summary by Member ID

        Get a summary of the voicemail messages for the user.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: :class:`MessageSummary`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/summary')
        data = super().get(url, params=params)
        r = MessageSummary.model_validate(data)
        return r

    def list(self, member_id: str, org_id: str = None) -> builtins.list[VoiceMessageDetails]:
        """
        List Messages by Member ID

        Get the list of all voicemail messages for the user.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: list[VoiceMessageDetails]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/voiceMessages')
        data = super().get(url, params=params)
        r = TypeAdapter(list[VoiceMessageDetails]).validate_python(data['items'])
        return r

    def delete(self, member_id: str, message_id: str, org_id: str = None) -> None:  # type: ignore[override]
        """
        Delete Message by Member ID

        Delete a specfic voicemail message for the user.

        :param member_id: Unique identifier for the member. Member ID can be one of the following: person, workspace,
            virtual line, hunt group, call queue, or auto attendant
        :type member_id: str
        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        :param org_id: Id of the organization to which the member belongs. If not provided, the orgId of the Service
            App is used. If provided, the organization must be the same as or managed by the Service App's
            organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{member_id}/voiceMessages/{message_id}')
        super().delete(url, params=params)
