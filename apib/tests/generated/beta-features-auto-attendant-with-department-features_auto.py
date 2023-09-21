from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersObject', 'AlternateNumbersObjectRingPattern', 'GetAutoAttendantObject', 'GetAutoAttendantObjectDepartment', 'GetAutoAttendantObjectExtensionDialing', 'HoursMenuObject', 'HoursMenuObjectGreeting', 'KeyConfigurationsObject', 'KeyConfigurationsObjectAction', 'KeyConfigurationsObjectKey', 'ListAutoAttendantObject', 'ListAutoAttendantObjectDepartment', 'ModifyAutoAttendantObject']


class AlternateNumbersObjectRingPattern(str, Enum):
    _0 = '0'
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
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '9'
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
    extension: Optional[datetime] = None
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
    extension: Optional[datetime] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: Specifies the department information.
    department: Optional[ListAutoAttendantObjectDepartment] = None


class ModifyAutoAttendantObject(ApiModel):
    #: Unique name for the auto attendant.
    #: example: Main Line IA - Test
    name: Optional[str] = None
    #: Auto attendant phone number. Either phone number or extension should be present as mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension. Either phone number or extension should be present as mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: First name defined for an auto attendant.
    #: example: Main Line AA
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant.
    #: example: Test
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]] = None
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
