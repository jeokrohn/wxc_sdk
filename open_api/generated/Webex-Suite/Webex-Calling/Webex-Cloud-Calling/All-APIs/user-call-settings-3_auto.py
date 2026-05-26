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


__all__ = ['HotDeskingAvailableMember', 'HotDeskingLineType', 'HotDeskingMember', 'HotDeskingMembers',
           'HotDeskingPutMember', 'HotDeskingPutMemberType', 'HotDeskingResponseMemberType', 'Location',
           'PersonCallsFromType', 'PersonScheduleLevel', 'PersonScheduleType', 'PersonSimultaneousRingCriteriaGet',
           'PersonSimultaneousRingCriteriaSummary', 'PersonSimultaneousRingGet', 'PersonSimultaneousRingNumber',
           'PersonSimultaneousRingSource', 'UserCallSettings33Api']


class PersonSimultaneousRingNumber(ApiModel):
    #: Phone number set for simultaneous ring.
    phone_number: Optional[str] = None
    #: When set to `true`, the called party is required to press 1 on the keypad to confirm answer for the call.
    answer_confirmation_enabled: Optional[bool] = None


class PersonSimultaneousRingSource(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class PersonSimultaneousRingCriteriaSummary(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule which determines when the simultaneous ring is in effect.
    schedule_name: Optional[str] = None
    source: Optional[PersonSimultaneousRingSource] = None
    #: When set to `true` simultaneous ringing is enabled for calls that meet this criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class PersonSimultaneousRingGet(ApiModel):
    #: When set to `true`, simultaneous ring is enabled for this person.
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when you are on a call.
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    criterias_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when you receive an incoming call.
    phone_numbers: Optional[list[PersonSimultaneousRingNumber]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[PersonSimultaneousRingCriteriaSummary]] = None


class PersonScheduleType(str, Enum):
    #: The Schedule type that specifies the business or working hours during the day.
    business_hours = 'businessHours'
    #: The Schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class PersonScheduleLevel(str, Enum):
    #: Indicates the schedule is configured at the location level.
    location = 'LOCATION'
    #: Indicates the schedule is configured at the person level.
    people = 'PEOPLE'


class PersonCallsFromType(str, Enum):
    #: The Schedule applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Indicates the schedule applies to select phone number defined in the `phoneNumbers` property.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'


class PersonSimultaneousRingCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule which determines when the simultaneous ring is in effect.
    schedule_name: Optional[str] = None
    schedule_type: Optional[PersonScheduleType] = None
    schedule_level: Optional[PersonScheduleLevel] = None
    calls_from: Optional[PersonCallsFromType] = None
    #: When `true`, the criteria applies to calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, the criteria applies to calls from unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: The list of phone numbers that will be checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` simultaneous ringing is enabled for calls that meet this criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class HotDeskingLineType(str, Enum):
    #: Primary hot desking guest profile line.
    hotdesking_guest = 'HOTDESKING_GUEST'
    #: Shared line assigned to the hot desking guest profile.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'
    #: Primary line.
    primary = 'PRIMARY'
    #: Mobility line.
    mobility = 'MOBILITY'


class HotDeskingResponseMemberType(str, Enum):
    #: The member is a person.
    people = 'PEOPLE'
    #: The member is a workspace.
    place = 'PLACE'
    #: The member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class Location(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None


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
    line_type: Optional[HotDeskingLineType] = None
    member_type: Optional[HotDeskingResponseMemberType] = None
    location: Optional[Location] = None


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
    line_type: Optional[HotDeskingLineType] = None
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
    member_type: Optional[HotDeskingResponseMemberType] = None
    location: Optional[Location] = None


class HotDeskingMembers(ApiModel):
    #: Name of the hot desking guest profile endpoint.
    model: Optional[str] = None
    #: List of primary and shared-line members assigned to the person's hot desking guest profile.
    members: Optional[list[HotDeskingMember]] = None
    #: Maximum number of lines that can be configured on the hot desking guest profile endpoint.
    max_line_count: Optional[int] = None


class HotDeskingPutMemberType(str, Enum):
    #: The member is a person.
    user = 'USER'
    #: The member is a workspace.
    place = 'PLACE'
    #: The member is a virtual line.
    virtual_profile = 'VIRTUAL_PROFILE'


class HotDeskingPutMember(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str] = None
    #: Port to assign to the member.
    port: Optional[int] = None
    #: Indicates whether this member is the hot desking guest profile owner.
    primary_owner: Optional[bool] = None
    line_type: Optional[HotDeskingLineType] = None
    #: Number of lines to configure for the member on the hot desking guest profile endpoint.
    line_weight: Optional[int] = None
    #: T.38 fax compression setting for the member line.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Whether this line automatically calls a predefined number when taken off-hook.
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required when `hotlineEnabled` is `true`.
    hotline_destination: Optional[str] = None
    #: When enabled, a call decline request is extended to all endpoints on the line. When disabled, the call is
    #: declined only at the current endpoint.
    allow_call_decline_enabled: Optional[bool] = None
    member_type: Optional[HotDeskingPutMemberType] = None


class UserCallSettings33Api(ApiChild, base='telephony/config/people'):
    """
    User Call Settings (3/3)
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their own settings.
    
    Configuring People settings requires a full or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their own settings.
    
    Call Settings API access can be restricted via Control Hub by a full administrator. Restricting access causes the
    APIs to throw a `403 Access Forbidden` error.
    
    See details about `features available by license type for Webex Calling
    <https://help.webex.com/en-us/article/n1qbbp7/Features-available-by-license-type-for-Webex-Calling>`_.
    """

    def get_person_anonymous_call_reject_settings(self, person_id: str, org_id: str = None) -> bool:
        """
        Get Anonymous Call Rejection Settings for a person.

        Anonymous Call Rejection allows people to automatically reject incoming calls from callers who have blocked
        their caller ID information.

        Viewing requires a full, read-only, user, or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: bool
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/anonymousCallReject')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def update_person_anonymous_call_reject_settings(self, person_id: str, enabled: bool, org_id: str = None) -> None:
        """
        Update Anonymous Call Rejection Settings for a person.

        Configure whether to automatically reject incoming calls from anonymous callers. When Anonymous Call Rejection
        is enabled, calls from callers who have blocked their caller ID will be rejected.

        Modifying requires a full, user, or location administrator auth token with a scope of
        `spark-admin:people_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: Enable or disable Anonymous Call Rejection. When set to true, incoming calls from callers who
            have blocked their caller ID will be automatically rejected.
        :type enabled: bool
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep(f'{person_id}/anonymousCallReject')
        super().put(url, params=params, json=body)

    def search_available_hot_desking_members(self, person_id: str, location_id: str = None, member_name: str = None,
                                             phone_number: str = None, extension: str = None, order: list[str] = None,
                                             org_id: str = None,
                                             **params: Any) -> Generator[HotDeskingAvailableMember, None, None]:
        """
        Search Available Hot Desking Members

        Retrieve members available for assignment to a person's hot desking guest profile.

        Available members can include people, workspaces, and virtual lines that can be added as shared lines on the
        hot desking profile.

        This API requires a full, user, device, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
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
        url = self.ep(f'{person_id}/features/hotDesking/availableMembers')
        return self.session.follow_pagination(url=url, model=HotDeskingAvailableMember, item_key='members', params=params)

    def get_hot_desking_members(self, person_id: str, org_id: str = None) -> HotDeskingMembers:
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
        url = self.ep(f'{person_id}/features/hotDesking/members')
        data = super().get(url, params=params)
        r = HotDeskingMembers.model_validate(data)
        return r

    def update_hot_desking_members(self, person_id: str, members: list[HotDeskingPutMember],
                                   org_id: str = None) -> None:
        """
        Update Hot Desking Members

        Modify the primary and shared-line members assigned to a person's hot desking guest profile.

        The request replaces the hot desking profile member list with the members supplied in the request body.

        This API requires a full, user, device, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param members: Members to assign to the person's hot desking guest profile.
        :type members: list[HotDeskingPutMember]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['members'] = TypeAdapter(list[HotDeskingPutMember]).dump_python(members, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/hotDesking/members')
        super().put(url, params=params, json=body)

    def get_person_calling_services(self, person_id: str, org_id: str = None) -> builtins.list[str]:
        """
        List Enabled Calling Services for a Person

        Retrieves the list of enabled calling services for a person.

        Calling services are designed to improve call handling and ensure that people can manage their communications
        effectively.

        Viewing requires a full, read-only, user, or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: list[str]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/services')
        data = super().get(url, params=params)
        r = data['services']
        return r

    def get_person_simultaneous_ring_settings(self, person_id: str, org_id: str = None) -> PersonSimultaneousRingGet:
        """
        Retrieve simultaneous ring settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the day or days of
        the week.

        Viewing requires a full, read-only, user, or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: :class:`PersonSimultaneousRingGet`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/simultaneousRing')
        data = super().get(url, params=params)
        r = PersonSimultaneousRingGet.model_validate(data)
        return r

    def update_person_simultaneous_ring_settings(self, person_id: str, enabled: bool = None,
                                                 do_not_ring_if_on_call_enabled: bool = None,
                                                 criterias_enabled: bool = None,
                                                 phone_numbers: list[PersonSimultaneousRingNumber] = None,
                                                 org_id: str = None) -> None:
        """
        Modify Simultaneous Ring Settings for a Person

        Modifies simultaneous ring settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the day or days of
        the week.

        Modifying requires a full, user, or location administrator auth token with a scope of
        `spark-admin:people_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When set to `true`, simultaneous ring is enabled for this person.
        :type enabled: bool
        :param do_not_ring_if_on_call_enabled: When set to `true`, the configured phone numbers won't ring when you are
            on a call.
        :type do_not_ring_if_on_call_enabled: bool
        :param criterias_enabled: When `true`, enables the selected schedule for simultaneous ring.
        :type criterias_enabled: bool
        :param phone_numbers: Enter up to 10 phone numbers to ring simultaneously when you receive an incoming call.
        :type phone_numbers: list[PersonSimultaneousRingNumber]
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if do_not_ring_if_on_call_enabled is not None:
            body['doNotRingIfOnCallEnabled'] = do_not_ring_if_on_call_enabled
        if criterias_enabled is not None:
            body['criteriasEnabled'] = criterias_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[PersonSimultaneousRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/simultaneousRing')
        super().put(url, params=params, json=body)

    def create_person_simultaneous_ring_criteria(self, person_id: str, calls_from: PersonCallsFromType,
                                                 ring_enabled: bool, schedule_name: str = None,
                                                 schedule_type: PersonScheduleType = None,
                                                 schedule_level: PersonScheduleLevel = None,
                                                 anonymous_callers_enabled: bool = None,
                                                 unavailable_callers_enabled: bool = None,
                                                 phone_numbers: list[str] = None, org_id: str = None) -> str:
        """
        Create Simultaneous Ring Criteria for a Person

        Create simultaneous ring criteria settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Modifying requires a full, user, or location administrator auth token with a scope of
        `spark-admin:people_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param calls_from: -
        :type calls_from: PersonCallsFromType
        :param ring_enabled: When set to `true` simultaneous ringing is enabled for calls that meet this criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param schedule_name: Name of the schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: PersonScheduleType
        :param schedule_level: -
        :type schedule_level: PersonScheduleLevel
        :param anonymous_callers_enabled: When `true`, the criteria applies to calls from anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, the criteria applies to calls from unavailable callers. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that will be checked against incoming calls for a match. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep(f'{person_id}/simultaneousRing/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_person_simultaneous_ring_criteria(self, person_id: str, id: str, org_id: str = None) -> None:
        """
        Delete Simultaneous Ring Criteria for a Person

        Delete simultaneous ring criteria settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Modifying requires a full, user, or location administrator auth token with a scope of
        `spark-admin:people_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/simultaneousRing/criteria/{id}')
        super().delete(url, params=params)

    def get_person_simultaneous_ring_criteria(self, person_id: str, id: str,
                                              org_id: str = None) -> PersonSimultaneousRingCriteriaGet:
        """
        Retrieve Simultaneous Ring Criteria for a Person

        Retrieve simultaneous ring criteria settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Viewing requires a full, read-only, user, or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: :class:`PersonSimultaneousRingCriteriaGet`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/simultaneousRing/criteria/{id}')
        data = super().get(url, params=params)
        r = PersonSimultaneousRingCriteriaGet.model_validate(data)
        return r

    def update_person_simultaneous_ring_criteria(self, person_id: str, id: str, schedule_name: str = None,
                                                 schedule_type: PersonScheduleType = None,
                                                 schedule_level: PersonScheduleLevel = None,
                                                 calls_from: PersonCallsFromType = None,
                                                 anonymous_callers_enabled: bool = None,
                                                 unavailable_callers_enabled: bool = None,
                                                 phone_numbers: list[str] = None, ring_enabled: bool = None,
                                                 org_id: str = None) -> None:
        """
        Modify Simultaneous Ring Criteria for a Person

        Modify simultaneous ring criteria settings for a person.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Modifying requires a full, user, or location administrator auth token with a scope of
        `spark-admin:people_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: PersonScheduleType
        :param schedule_level: -
        :type schedule_level: PersonScheduleLevel
        :param calls_from: -
        :type calls_from: PersonCallsFromType
        :param anonymous_callers_enabled: When `true`, the criteria applies to calls from anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, the criteria applies to calls from unavailable callers. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that will be checked against incoming calls for a match. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` simultaneous ringing is enabled for calls that meet this criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'{person_id}/simultaneousRing/criteria/{id}')
        super().put(url, params=params, json=body)
