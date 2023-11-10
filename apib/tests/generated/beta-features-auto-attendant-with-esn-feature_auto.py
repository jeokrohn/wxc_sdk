from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersObject', 'AlternateNumbersObjectRingPattern', 'AudioFileObject',
            'AudioFileObjectMediaType', 'GetAutoAttendantObject', 'GetAutoAttendantObjectExtensionDialing',
            'HoursMenuObject', 'HoursMenuObjectGreeting', 'KeyConfigurationsObject', 'KeyConfigurationsObjectAction',
            'KeyConfigurationsObjectKey', 'ListAutoAttendantObject', 'ReadTheListOfAutoAttendantsResponse']


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


class AudioFileObjectMediaType(str, Enum):
    #: WMA File Extension.
    wma = 'WMA'
    #: WAV File Extension.
    wav = 'WAV'
    #: 3GP File Extension.
    _3_gp = '3GP'


class AudioFileObject(ApiModel):
    #: Announcement audio file name.
    #: example: AUDIO_FILE.wav
    name: Optional[str] = None
    #: Announcement audio file media type.
    #: example: WAV
    media_type: Optional[AudioFileObjectMediaType] = None


class GetAutoAttendantObjectExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


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
    #: Announcement Audio File details.
    audio_file: Optional[AudioFileObject] = None
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsObject] = None


class GetAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Flag to indicate if auto attendant number is enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341001
    esn: Optional[datetime] = None
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
    #: Business hours defined for the auto attendant.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    business_schedule: Optional[str] = None
    #: Holiday defined for the auto attendant.
    #: example: AUTOATTENDANT-HOLIDAY
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    extension_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    name_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Time zone defined for the auto attendant.
    #: example: America/Los_Angeles
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuObject] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuObject] = None


class ListAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
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
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341001
    esn: Optional[datetime] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None


class ReadTheListOfAutoAttendantsResponse(ApiModel):
    #: Array of auto attendants.
    auto_attendants: Optional[list[ListAutoAttendantObject]] = None


class BetaFeaturesAutoAttendantWithESNFeatureApi(ApiChild, base='telephony/config'):
    """
    Beta Features:  Auto Attendant with ESN Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Auto Attendant support reading and writing of Webex Calling Auto Attendant settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_auto_attendants(self, location_id: str = None, start: int = None, name: str = None,
                                         phone_number: str = None, org_id: str = None,
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
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListAutoAttendantObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('autoAttendants')
        return self.session.follow_pagination(url=url, model=ListAutoAttendantObject, item_key='autoAttendants', params=params)

    def get_details_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                          org_id: str = None) -> GetAutoAttendantObject:
        """
        Get Details for an Auto Attendant

        Retrieve an Auto Attendant details.

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
