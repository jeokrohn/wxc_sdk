from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetVoicemailRulesObject', 'GetVoicemailRulesObjectBlockPreviousPasscodes', 'GetVoicemailRulesObjectDefaultVoicemailPinRules', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits', 'GetVoicemailRulesObjectDefaultVoicemailPinRulesLength', 'GetVoicemailRulesObjectExpirePasscode', 'GetVoicemailSettingsObject', 'Language', 'PutVoicemailRulesObject']


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits(ApiModel):
    #: If enabled, passcode should not contain repeated digits.
    #: example: True
    enabled: Optional[bool] = None
    #: Maximum number of repeaed digits. The minimum value is 1. The maximum value is 6.
    #: example: 3.0
    max: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of ascending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3.0
    numberOfAscendingDigits: Optional[int] = None
    #: Number of descending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3.0
    numberOfDescendingDigits: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    #: example: 3.0
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    #: example: 3.0
    max: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRules(ApiModel):
    #: If enabled, the passcode should not contain repeated pattern.
    #: example: True
    blockRepeatedPatternsEnabled: Optional[bool] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
    blockRepeatedDigits: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits] = None
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    blockContiguousSequences: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences] = None
    #: Length of the passcode.
    length: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRulesLength] = None
    #: If enabled, the default voicemail passcode can be set.
    #: example: True
    defaultVoicemailPinEnabled: Optional[bool] = None


class GetVoicemailRulesObjectExpirePasscode(ApiModel):
    #: If enabled, passcode expires after the number of days specified.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of days for password expiry. The minimum value is 15. The maximum value is 180.
    #: example: 180.0
    numberOfDays: Optional[int] = None


class GetVoicemailRulesObjectBlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of previous passcodes. The minimum value is 1. The maximum value is 10.
    #: example: 3.0
    numberOfPasscodes: Optional[int] = None


class GetVoicemailRulesObject(ApiModel):
    #: Default voicemail passcode requirements.
    defaultVoicemailPinRules: Optional[GetVoicemailRulesObjectDefaultVoicemailPinRules] = None
    #: Settings for passcode expiry.
    expirePasscode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for passcode changes.
    changePasscode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for previous passcode usage.
    blockPreviousPasscodes: Optional[GetVoicemailRulesObjectBlockPreviousPasscodes] = None


class GetVoicemailSettingsObject(ApiModel):
    #: When enabled, you can set the deletion conditions for expired messages.
    messageExpiryEnabled: Optional[bool] = None
    #: Number of days after which messages expire.
    #: example: 10.0
    numberOfDaysForMessageExpiry: Optional[int] = None
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When disabled, all unread voicemail messages will be kept.
    strictDeletionEnabled: Optional[bool] = None
    #: When enabled, people in the organization can configure the email forwarding of voicemails.
    #: example: True
    voiceMessageForwardingEnabled: Optional[bool] = None


class Language(ApiModel):
    #: Language name.
    #: example: English
    name: Optional[str] = None
    #: Language code.
    #: example: en_us
    code: Optional[str] = None


class PutVoicemailRulesObject(ApiModel):
    #: Set to `true` to enable the default voicemail passcode.
    defaultVoicemailPinEnabled: Optional[bool] = None
    #: Default voicemail passcode.
    #: example: 147852
    defaultVoicemailPin: Optional[str] = None
    #: Settings for passcode expiry.
    expirePasscode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for passcode changes.
    changePasscode: Optional[GetVoicemailRulesObjectExpirePasscode] = None
    #: Settings for previous passcode usage.
    blockPreviousPasscodes: Optional[GetVoicemailRulesObjectBlockPreviousPasscodes] = None
