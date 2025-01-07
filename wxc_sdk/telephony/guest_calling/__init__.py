from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['GuestCallingApi', 'DestinationMember', 'GuestCallingSettings']

from wxc_sdk.common import IdAndName, OwnerType


class GuestCallingSettings(ApiModel):
    #: When enabled, click-to-call calling is allowed.
    enabled: Optional[bool] = None
    #: When enabled, privacy mode is enabled.
    privacy_enabled: Optional[bool] = None
    video_enabled: Optional[bool] = None


class DestinationMember(ApiModel):
    #: ID of the destination member.
    id: Optional[str] = None
    #: First name of the destination member.
    first_name: Optional[str] = None
    #: Last name of the destination member.
    last_name: Optional[str] = None
    #: Phone number of the destination member.
    phone_number: Optional[str] = None
    #: Extension of the destination member.
    extension: Optional[str] = None
    #: Routing prefix of the destination member.
    routing_prefix: Optional[str] = None
    #: ESN of the destination member.
    esn: Optional[str] = None
    #: Type of the destination member.
    type: Optional[OwnerType] = None
    #: Location of the destination member.
    location: Optional[IdAndName] = None


class GuestCallingApi(ApiChild, base='telephony/config/guestCalling'):
    """
    Guest Calling Settings with Click-to-call

    Calling Service Settings supports reading and writing of Webex Calling service settings for a specific
    organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read(self, org_id: str = None) -> GuestCallingSettings:
        """
        Read the Click-to-call Settings

        Retrieve the organization's click-to-call calling settings.

        Click-to-call settings determine whether click-to-call is enabled and whether privacy mode is enabled.

        Retrieving click-to-call settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: :class:`GuestCallingSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = GuestCallingSettings.model_validate(data)
        return r

    def update(self, enabled: bool, privacy_enabled: bool, destination_members: list[str],
               org_id: str = None):
        """
        Update the Click-to-call Settings

        Update the organization's click-to-call settings.

        Click-to-call settings determine whether click-to-call is enabled and whether privacy mode is enabled.

        Updating an organization's click-to-call settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param enabled: Set to `true` to allow click-to-call calling.
        :type enabled: bool
        :param privacy_enabled: Set to `true` to enable privacy mode.
        :type privacy_enabled: bool
        :param destination_members: List of destination member IDs. Supported destination types are Auto Attendant,
            Call Queue, Hunt Group, and Virtual Line.
        :type destination_members: list[str]
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        body['privacyEnabled'] = privacy_enabled
        body['destinationMembers'] = destination_members
        url = self.ep()
        super().put(url, params=params, json=body)

    def members(self, member_name: str = None, phone_number: str = None, extension: str = None,
                org_id: str = None, **params) -> Generator[DestinationMember, None, None]:
        """
        Read the Click-to-call Members

        Retrieve the organization's click-to-call members.

        Click-to-call members are the destination members that click-to-call callers can call.

        Retrieving click-to-call members requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :return: Generator yielding :class:`DestinationMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep('members')
        return self.session.follow_pagination(url=url, model=DestinationMember, item_key='destinationMembers',
                                              params=params)

    def available_members(self, member_name: str = None, phone_number: str = None,
                          extension: str = None, org_id: str = None,
                          **params) -> Generator[DestinationMember, None, None]:
        """
        Read the Click-to-call Available Members

        Retrieve the organization's click-to-call available members.

        Click-to-call available members are the members that can be added as destination members for click-to-call
        callers.

        Retrieving click-to-call available members requires a full or read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :return: Generator yielding :class:`DestinationMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep('availableMembers')
        return self.session.follow_pagination(url=url, model=DestinationMember, item_key='availableDestinationMembers',
                                              params=params)
