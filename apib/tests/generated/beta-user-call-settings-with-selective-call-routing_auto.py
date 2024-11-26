from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsWithSelectiveCallRoutingApi', 'CallsFrom', 'CallsFromSelectiveReject', 'Criteria',
           'CriteriaForward', 'ScheduleLevel', 'ScheduleType', 'SelectiveForwardCallCriteriaGet',
           'SelectiveForwardCallGet', 'SelectiveRejectCallCriteriaGet', 'SelectiveRejectCallGet', 'Source']


class ScheduleType(str, Enum):
    #: The schedule type that specifies the business or working hours during the day.
    business_hours = 'businessHours'
    #: The schedule type that specifies the day when your organization is not open.
    holidays = 'holidays'


class ScheduleLevel(str, Enum):
    #: The schedule level that specifies that criteria is of People level.
    people = 'PEOPLE'
    #: The schedule level that specifies that criteria is of Group level.
    group = 'GROUP'


class Source(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Criteria applies only for forwarded numbers.
    forwarded = 'FORWARDED'


class CallsFrom(str, Enum):
    #: Criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Criteria only apply for forwarded incoming numbers.
    forwarded = 'FORWARDED'


class CallsFromSelectiveReject(str, Enum):
    #: Criteria apply for any incoming number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria only apply for selected incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: Criteria only apply for any internal incoming numbers.
    any_internal = 'ANY_INTERNAL'
    #: Criteria only apply for any external incoming numbers.
    any_external = 'ANY_EXTERNAL'


class Criteria(ApiModel):
    #: Criteria ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzI5NzA4NzUwMTY4MDI
    id: Optional[str] = None
    #: Name of the Schedule to which the criteria is created.
    #: example: CFS-Criteria-F-2
    schedule_name: Optional[str] = None
    #: Applied Selective reject ring which set of numbers.
    #: example: ALL_NUMBERS
    source: Optional[Source] = None
    #: Boolean field to indicate whether Selective reject enabled.
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallGet(ApiModel):
    #: Boolean to indicate whether Selective reject are enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: Ordered list of criteria that will be evaluated for rejecting the call.
    criteria: Optional[list[Criteria]] = None


class CriteriaForward(ApiModel):
    #: Criteria ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzI5NzA4NzUwMTY4MDI
    id: Optional[str] = None
    #: Name of the Schedule to which the criteria is created.
    #: example: CFS-Criteria-F-2
    schedule_name: Optional[str] = None
    #: Applied Selective reject ring which set of numbers.
    #: example: ALL_NUMBERS
    source: Optional[Source] = None
    #: Boolean flag to enable/disable selective call forward.
    #: example: True
    forward_enabled: Optional[bool] = None


class SelectiveRejectCallCriteriaGet(ApiModel):
    #: Criteria ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzI5NzA4NzUwMTY4MDI
    id: Optional[str] = None
    #: Name of the Schedule to which the criteria is created.
    #: example: CFS-Criteria-F-2
    schedule_name: Optional[str] = None
    #: Schedule Type.
    #: example: holidays
    schedule_type: Optional[ScheduleType] = None
    #: Schedule Level of the criteria.
    #: example: PEOPLE
    schedule_level: Optional[ScheduleLevel] = None
    #: Reject calls selection.
    #: example: ANY_PHONE_NUMBER
    calls_from: Optional[CallsFrom] = None
    #: Calls From custom numbers private number enabled.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: Calls From custom numbers unavailable number enabled.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers. It does not include extensions. In some regions phone numbers are not returned in E.164
    #: format. This will be supported in a future update.
    #: example: ['["+1986751234","+1986751234"]']
    phone_numbers: Optional[list[str]] = None
    #: Boolean flag to enable/disable rejection.
    #: example: True
    reject_enabled: Optional[bool] = None


class SelectiveForwardCallGet(ApiModel):
    #: Boolean to indicate whether Selective forward are enabled or not.
    enabled: Optional[bool] = None
    #: Number to which calls needs to be forwarded
    #: example: +18898988831
    default_phone_number_to_forward: Optional[str] = None
    #: Ring reminder enabled or not.
    ring_reminder_enabled: Optional[bool] = None
    #: Voicemail enabled or disabled.
    send_to_voicemail_enabled: Optional[bool] = None
    #: : Ordered list of criteria that will be evaluated for forwarding the call.
    criteria: Optional[list[CriteriaForward]] = None


class SelectiveForwardCallCriteriaGet(ApiModel):
    #: Criteria ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzI5NzA4NzUwMTY4MDI
    id: Optional[str] = None
    #: Number to which calls needs to be forwarded.
    #: example: +18898988831
    forward_to_phone_number: Optional[str] = None
    #: Voicemail enabled or disabled.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Name of the schedule to which the criteria is created.
    #: example: CFS-Criteria-F-2
    schedule_name: Optional[str] = None
    #: Schedule Type.
    #: example: holidays
    schedule_type: Optional[ScheduleType] = None
    #: Schedule Level of the criteria.
    #: example: PEOPLE
    schedule_level: Optional[ScheduleLevel] = None
    #: Reject calls selection.
    #: example: ANY_PHONE_NUMBER
    calls_from: Optional[CallsFromSelectiveReject] = None
    #: Calls From custom numbers private number enabled.
    #: example: True
    anonymous_callers_enabled: Optional[bool] = None
    #: Calls From custom numbers unavailable number enabled.
    #: example: True
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers. It does not include extensions. In some regions phone numbers are not returned in E.164
    #: format. This will be supported in a future update.
    #: example: ['["+1986751234","+1986751234"]']
    phone_numbers: Optional[list[str]] = None
    #: Boolean flag to enable/disable selective call forward.
    #: example: True
    forward_enabled: Optional[bool] = None


class BetaUserCallSettingsWithSelectiveCallRoutingApi(ApiChild, base='telephony/config/people'):
    """
    Beta User Call Settings with Selective Call Routing
    
    Selective Call Routing APIs create different rules to accept, reject, or forward certain calls based on the phone
    number, who's calling, and/or the time and day of the call. Selective capabilities (accept, reject, forward) of a
    call take precedence over other call settings.
    
    Viewing these read-only user settings requires a full, user, read-only or location administrator auth token with a
    scope of `spark-admin:telephony_config_read`.
    
    Requires a full, user, location, or administrator auth token with a scope of `spark-admin:telephony_config_write`.
    """

    def get_the_user_s_selective_call_rejection_criteria_listing(self, person_id: str,
                                                                 org_id: str = None) -> SelectiveRejectCallGet:
        """
        Get the User’s Selective Call Rejection Criteria Listing

        Retrieve selective call rejection criteria for a user.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveReject')
        data = super().get(url, params=params)
        r = SelectiveRejectCallGet.model_validate(data)
        return r

    def update_user_s_selective_call_rejection_criteria_list(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Update User’s Selective Call Rejection Criteria List

        Modify selective call rejection setting for a user.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the user.
        :type person_id: str
        :param enabled: Boolean to indicate whether Selective reject are enabled or not.
        :type enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{person_id}/selectiveReject')
        super().put(url, params=params, json=body)

    def create_a_criteria_to_the_user_s_selective_call_rejection_service(self, person_id: str, calls_from: CallsFrom,
                                                                         reject_enabled: bool,
                                                                         schedule_name: str = None,
                                                                         schedule_type: ScheduleType = None,
                                                                         schedule_level: ScheduleLevel = None,
                                                                         anonymous_callers_enabled: bool = None,
                                                                         unavailable_callers_enabled: bool = None,
                                                                         phone_numbers: list[str] = None,
                                                                         org_id: str = None) -> str:
        """
        Create a Criteria to the User’s Selective Call Rejection Service

        Add a criteria to the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFrom
        :param reject_enabled: Boolean flag to enable/disable rejection.
        :type reject_enabled: bool
        :param schedule_name: Name of the Schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: Schedule Type.
        :type schedule_type: ScheduleType
        :param schedule_level: Schedule Level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Calls From custom numbers private number enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Calls From custom numbers unavailable number enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'{person_id}/selectiveReject/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_a_criteria_for_the_user_s_selective_call_rejection_service(self, person_id: str, id: str,
                                                                       org_id: str = None) -> SelectiveRejectCallCriteriaGet:
        """
        Get a Criteria for the User’s Selective Call Rejection Service

        Get a criteria for the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveReject/criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveRejectCallCriteriaGet.model_validate(data)
        return r

    def modify_a_criteria_for_the_user_s_selective_call_rejection_service(self, person_id: str, id: str,
                                                                          calls_from: CallsFrom, reject_enabled: bool,
                                                                          schedule_name: str = None,
                                                                          schedule_type: ScheduleType = None,
                                                                          schedule_level: ScheduleLevel = None,
                                                                          anonymous_callers_enabled: bool = None,
                                                                          unavailable_callers_enabled: bool = None,
                                                                          phone_numbers: list[str] = None,
                                                                          org_id: str = None):
        """
        Modify a Criteria for the User’s Selective Call Rejection Service

        Modify a criteria for the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: A unique identifier for the criteria.
        :type id: str
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFrom
        :param reject_enabled: Boolean flag to enable/disable rejection.
        :type reject_enabled: bool
        :param schedule_name: Name of the Schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: Schedule Type.
        :type schedule_type: ScheduleType
        :param schedule_level: Schedule Level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Calls From custom numbers private number enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Calls From custom numbers unavailable number enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
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
        body['rejectEnabled'] = reject_enabled
        url = self.ep(f'{person_id}/selectiveReject/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_a_criteria_from_the_user_s_selective_call_rejection_service(self, person_id: str, id: str,
                                                                           org_id: str = None):
        """
        Delete a Criteria From the User’s Selective Call Rejection Service

        Delete a criteria from the user's selective call rejection service.

        With the Selective Call Rejection feature, you can create different rules to reject specific calls based on the
        phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveReject/criteria/{id}')
        super().delete(url, params=params)

    def get_the_user_s_selective_call_forwarding(self, person_id: str, org_id: str = None) -> SelectiveForwardCallGet:
        """
        Get the User’s Selective Call Forwarding

        Retrieve selective call forwarding criteria for a user.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveForward')
        data = super().get(url, params=params)
        r = SelectiveForwardCallGet.model_validate(data)
        return r

    def update_user_s_selective_call_forwarding_criteria_list(self, person_id: str, enabled: bool,
                                                              default_phone_number_to_forward: str = None,
                                                              ring_reminder_enabled: bool = None,
                                                              send_to_voicemail_enabled: bool = None,
                                                              org_id: str = None):
        """
        Update User’s Selective Call Forwarding Criteria List

        Modify selective call forwarding setting for a user.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the user.
        :type person_id: str
        :param enabled: Boolean to indicate whether Selective forward are enabled or not.
        :type enabled: bool
        :param default_phone_number_to_forward: Forward to default number. This field is mandatory when enabled is true
            and sendToVoicemailEnabled is true.
        :type default_phone_number_to_forward: str
        :param ring_reminder_enabled: Ring reminder enabled or not.
        :type ring_reminder_enabled: bool
        :param send_to_voicemail_enabled: Voicemail enabled or disabled.
        :type send_to_voicemail_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if default_phone_number_to_forward is not None:
            body['defaultPhoneNumberToForward'] = default_phone_number_to_forward
        if ring_reminder_enabled is not None:
            body['ringReminderEnabled'] = ring_reminder_enabled
        if send_to_voicemail_enabled is not None:
            body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
        url = self.ep(f'{person_id}/selectiveForward')
        super().put(url, params=params, json=body)

    def create_a_criteria_to_the_user_s_selective_call_forwarding_service(self, person_id: str,
                                                                          forward_to_phone_number: str,
                                                                          send_to_voicemail_enabled: bool,
                                                                          calls_from: CallsFromSelectiveReject,
                                                                          schedule_name: str = None,
                                                                          schedule_type: ScheduleType = None,
                                                                          schedule_level: ScheduleLevel = None,
                                                                          anonymous_callers_enabled: bool = None,
                                                                          unavailable_callers_enabled: bool = None,
                                                                          phone_numbers: list[str] = None,
                                                                          forward_enabled: bool = None,
                                                                          org_id: str = None) -> str:
        """
        Create a Criteria to the User’s Selective Call Forwarding Service

        Add a criteria to the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param forward_to_phone_number: Number to which calls needs to be forwarded.
        :type forward_to_phone_number: str
        :param send_to_voicemail_enabled: Voicemail enabled or disabled.
        :type send_to_voicemail_enabled: bool
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFromSelectiveReject
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: Schedule Type.
        :type schedule_type: ScheduleType
        :param schedule_level: Schedule Level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Calls From custom numbers private number enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Calls From custom numbers unavailable number enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param forward_enabled: Boolean flag to enable/disable selective call forward.
        :type forward_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['forwardToPhoneNumber'] = forward_to_phone_number
        body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
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
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'{person_id}/selectiveForward/criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_a_criteria_for_the_user_s_selective_call_forwarding_service(self, person_id: str, id: str,
                                                                        org_id: str = None) -> SelectiveForwardCallCriteriaGet:
        """
        Get a Criteria for the User’s Selective Call Forwarding Service

        Get the criteria details for the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: :class:`SelectiveForwardCallCriteriaGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveForward/criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveForwardCallCriteriaGet.model_validate(data)
        return r

    def modify_a_criteria_for_the_user_s_selective_call_forwarding_service(self, person_id: str, id: str,
                                                                           forward_to_phone_number: str,
                                                                           send_to_voicemail_enabled: bool,
                                                                           calls_from: CallsFromSelectiveReject,
                                                                           schedule_name: str = None,
                                                                           schedule_type: ScheduleType = None,
                                                                           schedule_level: ScheduleLevel = None,
                                                                           anonymous_callers_enabled: bool = None,
                                                                           unavailable_callers_enabled: bool = None,
                                                                           phone_numbers: list[str] = None,
                                                                           forward_enabled: bool = None,
                                                                           org_id: str = None):
        """
        Modify a Criteria for the User’s Selective Call Forwarding Service

        Modify a criteria for the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: A unique identifier for the criteria.
        :type id: str
        :param forward_to_phone_number: Number to which calls needs to be forwarded.
        :type forward_to_phone_number: str
        :param send_to_voicemail_enabled: Voicemail enabled or disabled.
        :type send_to_voicemail_enabled: bool
        :param calls_from: Reject calls selection.
        :type calls_from: CallsFromSelectiveReject
        :param schedule_name: Name of the schedule to which the criteria is created.
        :type schedule_name: str
        :param schedule_type: Schedule Type.
        :type schedule_type: ScheduleType
        :param schedule_level: Schedule Level of the criteria.
        :type schedule_level: ScheduleLevel
        :param anonymous_callers_enabled: Calls From custom numbers private number enabled.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Calls From custom numbers unavailable number enabled.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers. It does not include extensions. In some regions phone numbers are
            not returned in E.164 format. This will be supported in a future update.
        :type phone_numbers: list[str]
        :param forward_enabled: Boolean flag to enable/disable selective call forward
        :type forward_enabled: bool
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['forwardToPhoneNumber'] = forward_to_phone_number
        body['sendToVoicemailEnabled'] = send_to_voicemail_enabled
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
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'{person_id}/selectiveForward/criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_a_criteria_from_the_user_s_selective_call_forwarding_service(self, person_id: str, id: str,
                                                                            org_id: str = None):
        """
        Delete a Criteria From the User’s Selective Call Forwarding Service

        Delete a criteria from the user's selective call forwarding service.

        With the Selective Call Forwarding feature, you can create different rules to forward specific calls based on
        the phone number, who's calling, and/or the time and day of the call.

        Requires a full, user, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param id: Criteria ID.
        :type id: str
        :param org_id: Organization in which the user resides.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/selectiveForward/criteria/{id}')
        super().delete(url, params=params)
