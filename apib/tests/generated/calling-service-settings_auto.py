from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetVoicemailRulesObject', 'GetVoicemailRulesObjectBlockPreviousPasscodes', 'GetVoicemailRulesObjectDefaultVoicemailPinRules', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesLength', 'GetVoicemailRulesObjectExpirePasscode', 'GetVoicemailSettingsObject', 'Language', 'PutVoicemailRulesObject', 'ReadTheListOfAnnouncementLanguagesResponse']


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits(ApiModel):
    #: If enabled, passcode should not contain repeated digits.
    #: example: True
    enabled: Optional[bool] = None
    #: Maximum number of repeaed digits. The minimum value is 1. The maximum value is 6.
    #: example: 3.0
    max_: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of ascending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3.0
    number_of_ascending_digits: Optional[int] = None
    #: Number of descending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3.0
    number_of_descending_digits: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    #: example: 3.0
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    #: example: 3.0
    max_: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRules(ApiModel):
    #: If enabled, the passcode should not contain repeated pattern.
    #: example: True
    block_repeated_patterns_enabled: Optional[bool] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
    block_repeated_digits: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits] = None
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    block_contiguous_sequences: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences] = None
    #: Length of the passcode.
    length: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesLength] = None
    #: If enabled, the default voicemail passcode can be set.
    #: example: True
    default_voicemail_pin_enabled: Optional[bool] = None


class GetVoicemailRulesObjectExpirePasscode(ApiModel):
    #: If enabled, passcode expires after the number of days specified.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of days for password expiry. The minimum value is 15. The maximum value is 180.
    #: example: 180.0
    number_of_days: Optional[int] = None


class GetVoicemailRulesObjectBlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of previous passcodes. The minimum value is 1. The maximum value is 10.
    #: example: 3.0
    number_of_passcodes: Optional[int] = None


class GetVoicemailRulesObject(ApiModel):
    #: Default voicemail passcode requirements.
    default_voicemail_pin_rules: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRules] = None
    #: Settings for passcode expiry.
    expire_passcode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for passcode changes.
    change_passcode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[GetVoicemailRulesObjectBlockPreviousPasscodes] = None


class GetVoicemailSettingsObject(ApiModel):
    #: When enabled, you can set the deletion conditions for expired messages.
    message_expiry_enabled: Optional[bool] = None
    #: Number of days after which messages expire.
    #: example: 10.0
    number_of_days_for_message_expiry: Optional[int] = None
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When disabled, all unread voicemail messages will be kept.
    strict_deletion_enabled: Optional[bool] = None
    #: When enabled, people in the organization can configure the email forwarding of voicemails.
    #: example: True
    voice_message_forwarding_enabled: Optional[bool] = None


class Language(ApiModel):
    #: Language name.
    #: example: English
    name: Optional[str] = None
    #: Language code.
    #: example: en_us
    code: Optional[str] = None


class PutVoicemailRulesObject(ApiModel):
    #: Set to `true` to enable the default voicemail passcode.
    default_voicemail_pin_enabled: Optional[bool] = None
    #: Default voicemail passcode.
    #: example: 147852
    default_voicemail_pin: Optional[str] = None
    #: Settings for passcode expiry.
    expire_passcode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for passcode changes.
    change_passcode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[GetVoicemailRulesObjectBlockPreviousPasscodes] = None


class ReadTheListOfAnnouncementLanguagesResponse(ApiModel):
    #: Array of Languages.
    languages: Optional[list[Language]] = None
