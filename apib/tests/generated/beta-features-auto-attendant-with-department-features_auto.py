from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AlternateNumbersObject', 'AlternateNumbersObjectRingPattern',
           'BetaFeaturesAutoAttendantWithDepartmentFeaturesApi', 'GetAutoAttendantObject',
           'GetAutoAttendantObjectDepartment', 'GetAutoAttendantObjectExtensionDialing', 'HoursMenuObject',
           'HoursMenuObjectGreeting', 'KeyConfigurationsObject', 'KeyConfigurationsObjectAction',
           'KeyConfigurationsObjectKey', 'ListAutoAttendantObject', 'ListAutoAttendantObjectDepartment']


class AlternateNumbersObjectRingPattern(str, Enum):
    d0 = '0'
    normal = 'NORMAL'
    long_long = 'LONG_LONG'
    short_short_long = 'SHORT_SHORT_LONG'
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumbersObject(ApiModel):
    #: Phone number defined as alternate number.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: Ring pattern that will be used for the alternate number.
    #: example: 0
    ring_pattern: Optional[AlternateNumbersObjectRingPattern] = None


class GetAutoAttendantObjectExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class GetAutoAttendantObjectDepartment(ApiModel):
    #: Unique identifier of the department.  Set to null to remove entity from department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class HoursMenuObjectGreeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'


class KeyConfigurationsObjectKey(str, Enum):
    d0 = '0'
    d1 = '1'
    d2 = '2'
    d3 = '3'
    d4 = '4'
    d5 = '5'
    d6 = '6'
    d7 = '7'
    d8 = '8'
    d9 = '9'
    none_ = 'none'
    _ = '#'


class KeyConfigurationsObjectAction(str, Enum):
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    name_dialing = 'NAME_DIALING'
    extension_dialing = 'EXTENSION_DIALING'
    repeat_menu = 'REPEAT_MENU'
    exit = 'EXIT'
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    return_to_previous_menu = 'RETURN_TO_PREVIOUS_MENU'


class KeyConfigurationsObject(ApiModel):
    #: Key assigned to specific menu configuration.
    #: example: 0
    key: Optional[KeyConfigurationsObjectKey] = None
    #: Action assigned to specific menu key configuration.
    #: example: EXIT
    action: Optional[KeyConfigurationsObjectAction] = None
    #: The description of each menu key.
    #: example: Exit the menu
    description: Optional[str] = None
    #: Value based on actions.
    #: example: +19705550006
    value: Optional[str] = None


class HoursMenuObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    #: example: DEFAULT
    greeting: Optional[HoursMenuObjectGreeting] = None
    #: Flag to indicate if auto attendant extension is enabled or not.
    #: example: True
    extension_enabled: Optional[bool] = None
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsObject] = None


class GetAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzUxZmIyMDhiLWQ2ZTAtNDNjNS1hZDYyLTkxNmJkMDhmZDY4Zg
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Flag to indicate if auto attendant number is enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: Auto attendant phone number. Either phone number or extension should be present as mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension. Either phone number or extension should be present as mandatory.
    #: example: 1001
    extension: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: First name defined for an auto attendant.
    #: example: Main Line AA
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant.
    #: example: Test
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]] = None
    #: Language for the auto attendant.
    #: example: English
    language: Optional[str] = None
    #: Language code for the auto attendant.
    #: example: en_us
    language_code: Optional[str] = None
    #: Business hours for the auto attendant.
    #: example: Peak Season Hours
    business_schedule: Optional[str] = None
    #: Holiday schedule for the auto attendant.
    #: example: Corporate Holidays
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    #: example: ENTERPRISE
    extension_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    #: example: ENTERPRISE
    name_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Time zone defined for the auto attendant.
    #: example: America/Los_Angeles
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuObject] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuObject] = None
    #: Specifies the department information.
    department: Optional[GetAutoAttendantObjectDepartment] = None


class ListAutoAttendantObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class ListAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5ULzUxZmIyMDhiLWQ2ZTAtNDNjNS1hZDYyLTkxNmJkMDhmZDY4Zg
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Name of location for auto attendant.
    #: example: Houston
    location_name: Optional[str] = None
    #: ID of location for auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzI2NDE1MA
    location_id: Optional[str] = None
    #: Auto attendant phone number. Either phone number or extension should be present as mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension. Either phone number or extension should be present as mandatory.
    #: example: 1001
    extension: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[ListAutoAttendantObjectDepartment] = None


class BetaFeaturesAutoAttendantWithDepartmentFeaturesApi(ApiChild, base='telephony/config'):
    """
    Beta Features:  Auto Attendant with Department Features
    
    Features: Auto Attendant support reading and writing of Webex Calling Auto Attendant settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_auto_attendants(self, location_id: str = None, name: str = None, phone_number: str = None,
                                         department_id: str = None, department_name: str = None, org_id: str = None,
                                         **params) -> Generator[ListAutoAttendantObject, None, None]:
        """
        Read the List of Auto Attendants

        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :param department_id: Return only auto attendants with the matching departmentId.
        :type department_id: str
        :param department_name: Return only auto attendants with the matching departmentName.
        :type department_name: str
        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListAutoAttendantObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if department_id is not None:
            params['departmentId'] = department_id
        if department_name is not None:
            params['departmentName'] = department_name
        url = self.ep('autoAttendants')
        return self.session.follow_pagination(url=url, model=ListAutoAttendantObject, item_key='autoAttendants', params=params)

    def get_details_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                          org_id: str = None) -> GetAutoAttendantObject:
        """
        Get Details for an Auto Attendant

        Retrieve an Auto Attendant's details.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        :rtype: :class:`GetAutoAttendantObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        data = super().get(url, params=params)
        r = GetAutoAttendantObject.model_validate(data)
        return r

    def update_an_auto_attendant(self, location_id: str, auto_attendant_id: str, business_schedule: str,
                                 name: str = None, phone_number: str = None, extension: str = None,
                                 first_name: str = None, last_name: str = None,
                                 alternate_numbers: list[AlternateNumbersObject] = None, language_code: str = None,
                                 holiday_schedule: str = None,
                                 extension_dialing: GetAutoAttendantObjectExtensionDialing = None,
                                 name_dialing: GetAutoAttendantObjectExtensionDialing = None, time_zone: str = None,
                                 business_hours_menu: HoursMenuObject = None,
                                 after_hours_menu: HoursMenuObject = None,
                                 department: GetAutoAttendantObjectDepartment = None, org_id: str = None):
        """
        Update an Auto Attendant

        Update the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Updating an auto attendant requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param business_schedule: Business hours for the auto attendant.
        :type business_schedule: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param phone_number: Auto attendant phone number. Either phone number or extension should be present as
            mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension. Either phone number or extension should be present as mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: list[AlternateNumbersObject]
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday schedule for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            ENTERPRISE.
        :type extension_dialing: GetAutoAttendantObjectExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: GetAutoAttendantObjectExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject
        :param department: Specifies the department information.
        :type department: GetAutoAttendantObjectDepartment
        :param org_id: Update an auto attendant from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if alternate_numbers is not None:
            body['alternateNumbers'] = TypeAdapter(list[AlternateNumbersObject]).dump_python(alternate_numbers, mode='json', by_alias=True, exclude_none=True)
        if language_code is not None:
            body['languageCode'] = language_code
        body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if extension_dialing is not None:
            body['extensionDialing'] = enum_str(extension_dialing)
        if name_dialing is not None:
            body['nameDialing'] = enum_str(name_dialing)
        if time_zone is not None:
            body['timeZone'] = time_zone
        if business_hours_menu is not None:
            body['businessHoursMenu'] = business_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        if after_hours_menu is not None:
            body['afterHoursMenu'] = after_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        if department is not None:
            body['department'] = department.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().put(url, params=params, json=body)
