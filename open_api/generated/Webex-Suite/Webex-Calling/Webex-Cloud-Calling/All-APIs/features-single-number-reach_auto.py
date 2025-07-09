from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['FeaturesSingleNumberReachApi', 'GetSingleNumberReachObject', 'GetSingleNumberReachObjectNumbersItem',
           'STATE', 'SingleNumberReachPrimaryAvailableNumberObject', 'TelephonyType']


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class SingleNumberReachPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


class GetSingleNumberReachObjectNumbersItem(ApiModel):
    #: ID of Single number reach. Note that this ID contains base64 encoded phoneNumber data and can change if the
    #: phone number is modified.
    id: Optional[str] = None
    #: The phone number that will ring when a call is received. The number should be in E.164 format.
    phone_number: Optional[str] = None
    #: A flag to enable or disable this single Number Reach phone number.
    enabled: Optional[bool] = None
    #: Name of the single number reach phone number entry.
    name: Optional[str] = None
    #: If enabled, the call forwarding settings of provided phone Number will not be applied.
    do_not_forward_calls_enabled: Optional[bool] = None
    #: If enabled, the call recipient will be prompted to press a key before being connected.
    answer_confirmation_enabled: Optional[bool] = None


class GetSingleNumberReachObject(ApiModel):
    #: A flag to enable or disable single Number Reach.
    enabled: Optional[bool] = None
    #: Flag to enable alerting single number reach numbers for click to dial calls.
    alert_all_numbers_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: Array of single number reach number entries.
    numbers: Optional[list[GetSingleNumberReachObjectNumbersItem]] = None


class FeaturesSingleNumberReachApi(ApiChild, base='telephony/config'):
    """
    Features: Single Number Reach
    
    Features: Single Number Reach APIs support reading and writing of Webex Calling Single Number Reach settings for a
    specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_single_number_reach_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                                org_id: str = None,
                                                                **params) -> Generator[SingleNumberReachPrimaryAvailableNumberObject, None, None]:
        """
        Get Single Number Reach Primary Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the single number reach's
        primary phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`SingleNumberReachPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/singleNumberReach/availableNumbers')
        return self.session.follow_pagination(url=url, model=SingleNumberReachPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_single_number_reach_settings_for_a_person(self, person_id: str) -> GetSingleNumberReachObject:
        """
        Get Single Number Reach Settings For A Person

        Retrieve Single Number Reach settings for the given person.

        Single number reach allows you to setup your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Retrieving Single number reach settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: :class:`GetSingleNumberReachObject`
        """
        url = self.ep(f'people/{person_id}/singleNumberReach')
        data = super().get(url)
        r = GetSingleNumberReachObject.model_validate(data)
        return r

    def update_single_number_reach_settings_for_a_person(self, person_id: str,
                                                         alert_all_numbers_for_click_to_dial_calls_enabled: bool = None):
        """
        Update Single number reach settings for a person.

        Single number reach allows you to setup your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Updating a single number reach settings for a person requires a full administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param alert_all_numbers_for_click_to_dial_calls_enabled: Flag to enable alerting single number reach numbers
            for click to dial calls.
        :type alert_all_numbers_for_click_to_dial_calls_enabled: bool
        :rtype: None
        """
        body = dict()
        if alert_all_numbers_for_click_to_dial_calls_enabled is not None:
            body['alertAllNumbersForClickToDialCallsEnabled'] = alert_all_numbers_for_click_to_dial_calls_enabled
        url = self.ep(f'people/{person_id}/singleNumberReach')
        super().put(url, json=body)

    def create_single_number_reach_for_a_person(self, person_id: str, phone_number: str, enabled: bool, name: str,
                                                do_not_forward_calls_enabled: bool = None,
                                                answer_confirmation_enabled: bool = None) -> str:
        """
        Create Single Number Reach For a Person

        Create a single number reach for a person in an organization.

        Single number reach allows you to setup your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Creating a single number reach for a person requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Personal phone number used as single Number Reach.
        :type phone_number: str
        :param enabled: A flag to enable or disable single Number Reach.
        :type enabled: bool
        :param name: Name of the single number reach phone number entry.
        :type name: str
        :param do_not_forward_calls_enabled: If enabled, the call forwarding settings of provided phone Number will not
            be applied.
        :type do_not_forward_calls_enabled: bool
        :param answer_confirmation_enabled: If enabled, the call recepient will be prompted to press a key before being
            connected.
        :type answer_confirmation_enabled: bool
        :rtype: str
        """
        body = dict()
        body['phoneNumber'] = phone_number
        body['enabled'] = enabled
        body['name'] = name
        if do_not_forward_calls_enabled is not None:
            body['doNotForwardCallsEnabled'] = do_not_forward_calls_enabled
        if answer_confirmation_enabled is not None:
            body['answerConfirmationEnabled'] = answer_confirmation_enabled
        url = self.ep(f'people/{person_id}/singleNumberReach/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_a_single_number_reach_number(self, person_id: str, id: str, org_id: str = None):
        """
        Delete A Single Number Reach Number

        Delete Single number reach number for a person.

        Single number reach allows you to setup your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Deleting a Single number reach number requires a full administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: Unique identifier for single number reach.
        :type id: str
        :param org_id: Unique identifier for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/singleNumberReach/numbers/{id}')
        super().delete(url, params=params)

    def update_single_number_reach_settings_for_a_number(self, person_id: str, id: str, phone_number: str,
                                                         enabled: bool, name: str,
                                                         do_not_forward_calls_enabled: bool = None,
                                                         answer_confirmation_enabled: bool = None) -> str:
        """
        Update Single number reach settings for a number.

        Single number reach allows you to setup your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        The response returns an ID that can change if the phoneNumber is modified, as the ID contains base64 encoded
        phone number data.

        Updating a single number reach settings for a number requires a full administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param id: Unique identifier for single number reach.
        :type id: str
        :param phone_number: Personal phone number used as single Number Reach.
        :type phone_number: str
        :param enabled: A flag to enable or disable single Number Reach phone number.
        :type enabled: bool
        :param name: Name of the single number reach phone number entry.
        :type name: str
        :param do_not_forward_calls_enabled: If enabled, the call forwarding settings of provided phone Number will not
            be applied.
        :type do_not_forward_calls_enabled: bool
        :param answer_confirmation_enabled: If enabled, the call recepient will be prompted to press a key before being
            connected.
        :type answer_confirmation_enabled: bool
        :rtype: str
        """
        body = dict()
        body['phoneNumber'] = phone_number
        body['enabled'] = enabled
        body['name'] = name
        if do_not_forward_calls_enabled is not None:
            body['doNotForwardCallsEnabled'] = do_not_forward_calls_enabled
        if answer_confirmation_enabled is not None:
            body['answerConfirmationEnabled'] = answer_confirmation_enabled
        url = self.ep(f'people/{person_id}/singleNumberReach/numbers/{id}')
        data = super().put(url, json=body)
        r = data['id']
        return r
