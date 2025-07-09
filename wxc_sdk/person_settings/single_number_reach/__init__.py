from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.person_settings.available_numbers import AvailableNumber

__all__ = ['SingleNumberReachApi', 'SingleNumberReach', 'SingleNumberReachNumber']


class SingleNumberReachNumber(ApiModel):
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

    def create_update(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json',
                               by_alias=True,
                               exclude_unset=True,
                               exclude={'id'})


class SingleNumberReach(ApiModel):
    #: A flag to enable or disable single Number Reach.
    enabled: Optional[bool] = None
    #: Flag to enable alerting single number reach numbers for click to dial calls.
    alert_all_numbers_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: Array of single number reach number entries.
    numbers: Optional[list[SingleNumberReachNumber]] = None


class SingleNumberReachApi(ApiChild, base='telephony/config'):
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

    def available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                org_id: str = None,
                                **params) -> Generator[AvailableNumber, None, None]:
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
        return self.session.follow_pagination(url=url, model=AvailableNumber,
                                              item_key='phoneNumbers', params=params)

    def read(self, person_id: str) -> SingleNumberReach:
        """
        Get Single Number Reach Settings For A Person

        Retrieve Single Number Reach settings for the given person.

        Single number reach allows you to set up your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Retrieving Single number reach settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: :class:`SingleNumberReach`
        """
        url = self.ep(f'people/{person_id}/singleNumberReach')
        data = super().get(url)
        r = SingleNumberReach.model_validate(data)
        return r

    def update(self, person_id: str,
               alert_all_numbers_for_click_to_dial_calls_enabled: bool = None):
        """
        Update Single number reach settings for a person.

        Single number reach allows you to set up your work calls ring any phone number. This means that your office
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

    def create_snr(self, person_id: str, settings: SingleNumberReachNumber) -> str:
        """
        Create Single Number Reach For a Person

        Create a single number reach for a person in an organization.

        Single number reach allows you to set up your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        Creating a single number reach for a person requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: Settings for new SNR number
        :type settings: SingleNumberReachNumber
        :rtype: str
        """
        body = settings.create_update()
        url = self.ep(f'people/{person_id}/singleNumberReach/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_snr(self, person_id: str, id: str, org_id: str = None):
        """
        Delete A Single Number Reach Number

        Delete Single number reach number for a person.

        Single number reach allows you to setu p your work calls ring any phone number. This means that your office
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

    def update_snr(self, person_id: str, settings: SingleNumberReachNumber) -> str:
        """
        Update Single number reach settings for a number.

        Single number reach allows you to set up your work calls ring any phone number. This means that your office
        phone, mobile phone, or any other designated devices can ring at the same time, ensuring you don't miss
        important calls.

        The response returns an ID that can change if the phoneNumber is modified, as the ID contains base64 encoded
        phone number data.

        Updating a single number reach settings for a number requires a full administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: Settings for new SNR number
        :type settings: SingleNumberReachNumber
        :rtype: str
        """
        body = settings.create_update()
        url = self.ep(f'people/{person_id}/singleNumberReach/numbers/{settings.id}')
        data = super().put(url, json=body)
        return data['id']
