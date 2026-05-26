from collections.abc import Generator
from typing import Any, Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.common import IdAndName, PrimaryOrShared, UserType
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['HotDeskingApi', 'HotDeskingAvailableMember', 'HotDeskingMember', 'HotDeskingMembers']


class HotDeskingAvailableMember(ApiModel):
    #: Unique identifier for the available member.
    id: Optional[str] = None
    #: First name of the available member.
    first_name: Optional[str] = None
    #: Last name of the available member.
    last_name: Optional[str] = None
    #: Phone number of the available member.
    phone_number: Optional[str] = None
    #: Extension of the available member.
    extension: Optional[str] = None
    #: Routing prefix of the member's location.
    routing_prefix: Optional[str] = None
    #: Enterprise significant number for the available member.
    esn: Optional[str] = None
    line_type: Optional[PrimaryOrShared] = None
    member_type: Optional[UserType] = None
    location: Optional[IdAndName] = None


class HotDeskingMember(ApiModel):
    #: Unique identifier for the assigned member.
    id: Optional[str] = None
    #: First name of the assigned member.
    first_name: Optional[str] = None
    #: Last name of the assigned member.
    last_name: Optional[str] = None
    #: Phone number of the assigned member.
    phone_number: Optional[str] = None
    #: Extension of the assigned member.
    extension: Optional[str] = None
    #: Routing prefix of the member's location.
    routing_prefix: Optional[str] = None
    #: Enterprise significant number for the assigned member.
    esn: Optional[str] = None
    #: Indicates whether this member is the hot desking guest profile owner.
    primary_owner: Optional[bool] = None
    #: Port assigned to the member.
    port: Optional[int] = None
    #: T.38 fax compression setting for the member line.
    t38_fax_compression_enabled: Optional[bool] = None
    line_type: Optional[PrimaryOrShared] = None
    #: Number of lines configured for the member on the hot desking guest profile endpoint.
    line_weight: Optional[int] = None
    #: Registration home IP address for the line port.
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP address for the line port.
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Whether this line automatically calls a predefined number when taken off-hook.
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required when `hotlineEnabled` is `true`.
    hotline_destination: Optional[str] = None
    #: When enabled, a call decline request is extended to all endpoints on the line. When disabled, the call is
    #: declined only at the current endpoint.
    allow_call_decline_enabled: Optional[bool] = None
    member_type: Optional[UserType] = None
    location: Optional[IdAndName] = None

    def update(self) -> dict[str, Any]:
        """
        Data for update_members()

        :meta private:
        """
        data = self.model_dump(
            mode='json',
            by_alias=True,
            exclude_none=True,
            include={
                'id',
                'port',
                'primary_owner',
                'line_type',
                'line_weight',
                't38_fax_compression_enabled',
                'hotline_enabled',
                'hotline_destination',
                'allow_call_decline_enabled',
                'member_type',
            },
        )

        return data

    @classmethod
    def from_available_member(cls, available_member: HotDeskingAvailableMember) -> 'HotDeskingMember':
        """
        Create a HotDeskingMember instance from a HotDeskingAvailableMember instance.

        :param available_member: The available member to convert.
        :type available_member: HotDeskingAvailableMember
        :return: A new HotDeskingMember instance with data copied from the available member.
        :rtype: HotDeskingMember
        """
        return cls(
            id=available_member.id,
            first_name=available_member.first_name,
            last_name=available_member.last_name,
            phone_number=available_member.phone_number,
            extension=available_member.extension,
            routing_prefix=available_member.routing_prefix,
            esn=available_member.esn,
            line_type=available_member.line_type,
            member_type=available_member.member_type,
            location=available_member.location,
        )


class HotDeskingMembers(ApiModel):
    #: Name of the hot desking guest profile endpoint.
    model: Optional[str] = None
    #: List of primary and shared-line members assigned to the person's hot desking guest profile.
    members: Optional[list[HotDeskingMember]] = None
    #: Maximum number of lines that can be configured on the hot desking guest profile endpoint.
    max_line_count: Optional[int] = None


class HotDeskingApi(PersonSettingsApiChild):
    """
    API for hot desking settings; so far only used for persons
    """

    feature = 'hotDesking'

    def available_members(
        self,
        person_id: str,
        location_id: str = None,
        member_name: str = None,
        phone_number: str = None,
        extension: str = None,
        order: list[str] = None,
        org_id: str = None,
        **params: Any,
    ) -> Generator[HotDeskingAvailableMember, None, None]:
        """
        Search Available Hot Desking Members

        Retrieve members available for assignment to a person's hot desking guest profile.

        Available members can include people, workspaces, and virtual lines that can be added as shared lines on the
        hot desking profile.

        This API requires a full, user, device, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the entity.
        :type person_id: str
        :param location_id: Return only available members in this location.
        :type location_id: str
        :param member_name: Search for available members by name.
        :type member_name: str
        :param phone_number: Search for available members by phone number.
        :type phone_number: str
        :param extension: Search for available members by extension.
        :type extension: str
        :param order: Sort order for the available member list. Multiple order values may be provided.
        :type order: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :return: Generator yielding :class:`HotDeskingAvailableMember` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if order is not None:
            params['order'] = ','.join(order)
        url = self.f_ep(person_id, 'availableMembers')
        return self.session.follow_pagination(
            url=url, model=HotDeskingAvailableMember, item_key='members', params=params
        )

    def get_members(self, person_id: str, org_id: str = None) -> HotDeskingMembers:
        """
        Get Hot Desking Members

        Retrieve the primary and shared-line members assigned to a person's hot desking guest profile.

        This API requires a full, user, device, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :rtype: :class:`HotDeskingMembers`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(person_id, 'members')
        data = super().get(url, params=params)
        r = HotDeskingMembers.model_validate(data)
        return r

    def update_members(self, person_id: str, members: list[HotDeskingMember], org_id: str = None) -> None:
        """
        Update Hot Desking Members

        Modify the primary and shared-line members assigned to a person's hot desking guest profile.

        The request replaces the hot desking profile member list with the members supplied in the request body.

        This API requires a full, user, device, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param members: Members to assign to the person's hot desking guest profile.
        :type members: list[HotDeskingMember]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['members'] = [m.update() for m in members]
        # assert that all members have "port" and "lineWeight" set, as required by the API, and set default values if
        # not provided
        port = 1
        for m in body['members']:
            if m.get('port') is None:
                m['port'] = port
            # default lineWeight is 1
            w = m.get('lineWeight', 1)
            m['lineWeight'] = w
            port += w
            m['primaryOwner'] = m['id'] == person_id
        url = self.f_ep(person_id, 'members')
        super().put(url, params=params, json=body)
