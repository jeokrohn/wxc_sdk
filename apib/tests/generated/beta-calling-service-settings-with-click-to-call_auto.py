from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaCallingServiceSettingsWithClicktocallApi', 'DestinationMember', 'GuestCallingSettingsGet',
           'LocationObject', 'ServiceType']


class GuestCallingSettingsGet(ApiModel):
    #: When enabled, click-to-call calling is allowed.
    #: example: True
    enabled: Optional[bool] = None
    #: When enabled, privacy mode is enabled.
    privacy_enabled: Optional[bool] = None


class ServiceType(str, Enum):
    #: The destination a an Auto Attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: The destination is a Call Queue.
    call_queue = 'CALL_QUEUE'
    #: The destination is a Hunt Group.
    hunt_group = 'HUNT_GROUP'
    #: The destination is a Virtual Line.
    virtual_line = 'VIRTUAL_LINE'


class LocationObject(ApiModel):
    #: ID of the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2M2MDliOGE1LTAxNmQtNDAwNy1hN2E0LTJhMThiZmZjY2FmNg
    id: Optional[str] = None
    #: Name of the location.
    #: example: Richardson
    name: Optional[str] = None


class DestinationMember(ApiModel):
    #: ID of the destination member.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzUxZmIyMDhiLWQ2ZTAtNDNjNS1hZDYyLTkxNmJkMDhmZDY4Zg
    id: Optional[str] = None
    #: First name of the destination member.
    #: example: Main Line AA
    first_name: Optional[str] = None
    #: Last name of the destination member.
    #: example: Test
    last_name: Optional[str] = None
    #: Phone number of the destination member.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Extension of the destination member.
    #: example: 28
    extension: Optional[str] = None
    #: Routing prefix of the destination member.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: ESN of the destination member.
    #: example: 12340028
    esn: Optional[str] = None
    #: Type of the destination member.
    #: example: AUTO_ATTENDANT
    type: Optional[ServiceType] = None
    #: Location of the destination member.
    location: Optional[LocationObject] = None


class BetaCallingServiceSettingsWithClicktocallApi(ApiChild, base='telephony/config/guestCalling'):
    """
    Beta Calling Service Settings with Click-to-call
    
    Calling Service Settings supports reading and writing of Webex Calling service settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_click_to_call_settings(self, org_id: str = None) -> GuestCallingSettingsGet:
        """
        Read the Click-to-call Settings

        Retrieve the organization's click-to-call calling settings.

        Click-to-call settings determine whether click-to-call is enabled and whether privacy mode is enabled.

        Retrieving click-to-call settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: :class:`GuestCallingSettingsGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = GuestCallingSettingsGet.model_validate(data)
        return r

    def read_the_click_to_call__members(self, member_name: str = None, phone_number: str = None, extension: str = None,
                                        org_id: str = None, **params) -> Generator[DestinationMember, None, None]:
        """
        Read the Click-to-call  Members

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
        return self.session.follow_pagination(url=url, model=DestinationMember, item_key='destinationMembers', params=params)

    def read_the_click_to_call_available_members(self, member_name: str = None, phone_number: str = None,
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
        return self.session.follow_pagination(url=url, model=DestinationMember, item_key='availableDestinationMembers', params=params)

    def update_the_click_to_call_settings(self, enabled: bool, privacy_enabled: bool, destination_members: list[str],
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
