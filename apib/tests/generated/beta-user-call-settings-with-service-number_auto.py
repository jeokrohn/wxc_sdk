from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsWithServiceNumberApi', 'GetPersonPrimaryAvailablePhoneNumbersLicenseType',
           'NumberOwnerType', 'PersonCallForwardAvailableNumberObject', 'PersonCallForwardAvailableNumberObjectOwner',
           'PersonECBNAvailableNumberObject', 'PersonECBNAvailableNumberObjectOwner',
           'PersonECBNAvailableNumberObjectOwnerType', 'PersonPrimaryAvailableNumberObject',
           'PersonPrimaryAvailableNumberObjectTelephonyType', 'PersonSecondaryAvailableNumberObject', 'STATE',
           'TelephonyType']


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class PersonSecondaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class PersonCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class PersonCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[PersonCallForwardAvailableNumberObjectOwner] = None


class PersonPrimaryAvailableNumberObjectTelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: The object is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class PersonPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[PersonPrimaryAvailableNumberObjectTelephonyType] = None
    #: Mobile Network for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: mobileNetwork
    mobile_network: Optional[str] = None
    #: Routing Profile for the number if the number's `telephonyType` is `MOBILE_NUMBER`.
    #: example: AttRtPf
    routing_profile: Optional[str] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If set to true, it indicates that the `phoneNumber` is classified
    #: as a service number. Otherwise, if the `telephonyType` is `PSTN_NUMBER`, it is considered a standard number, or
    #: if the `telephonyType` is `MOBILE_NUMBER`, it is regarded as a mobile number.
    #: example: True
    is_service_number: Optional[bool] = None


class PersonECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'


class PersonECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the phone number's owner.
    #: example: PEOPLE
    type: Optional[PersonECBNAvailableNumberObjectOwnerType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class PersonECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[PersonECBNAvailableNumberObjectOwner] = None


class GetPersonPrimaryAvailablePhoneNumbersLicenseType(str, Enum):
    var_standard = 'VAR_STANDARD'
    var_basic = 'VAR_BASIC'


class BetaUserCallSettingsWithServiceNumberApi(ApiChild, base='telephony/config/people'):
    """
    Beta User Call Settings with Service Number
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Service numbers are intended to be high-volume regular phone numbers (non-mobile, non toll-free numbers), while
    standard numbers are PSTN numbers that do not fall under this classification.
    With the service number feature, available number APIs for location services or for features like members CLID,
    call forwarding or call intercept will now return service numbers in response.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their settings.
    
    Configuring People settings requires a full or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their settings.
    """

    def get_person_secondary_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                     org_id: str = None,
                                                     **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a person's secondary phone number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{person_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_fax_message_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[PersonSecondaryAvailableNumberObject, None, None]:
        """
        Get Person Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a person's FAX message number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonSecondaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{person_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonSecondaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_call_forward_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                        owner_name: str = None, extension: str = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Forward Available Phone Numbers

        List service and standard numbers that are available to be assigned as a person's call forward number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{person_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_primary_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                                   license_type: GetPersonPrimaryAvailablePhoneNumbersLicenseType = None,
                                                   org_id: str = None,
                                                   **params) -> Generator[PersonPrimaryAvailableNumberObject, None, None]:
        """
        Get Person Primary Available Phone Numbers

        List numbers that are available to be assigned as a person's primary phone number.
        By default, this API returns standard and mobile numbers from all locations that are unassigned. The parameters
        `licenseType` and `locationId` must align with the person's settings to determine the appropriate number for
        assignment.
        Failure to provide these parameters may result in the unsuccessful assignment of the returned number.

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
        :param license_type: This is used to search numbers according to the person's `licenseType` to which the number
            will be assigned. Possible input values
        :type license_type: GetPersonPrimaryAvailablePhoneNumbersLicenseType
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if license_type is not None:
            params['licenseType'] = enum_str(license_type)
        url = self.ep('primary/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_ecbn_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                owner_name: str = None, org_id: str = None,
                                                **params) -> Generator[PersonECBNAvailableNumberObject, None, None]:
        """
        Get Person ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a person's emergency callback number.
        These numbers are associated with the location of the person specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'{person_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_person_call_intercept_available_phone_numbers(self, person_id: str, phone_number: list[str] = None,
                                                          owner_name: str = None, extension: str = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[PersonCallForwardAvailableNumberObject, None, None]:
        """
        Get Person Call Intercept Available Phone Numbers

        List service and standard numbers that are available to be assigned as a person's call intercept number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PersonCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{person_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=PersonCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)
