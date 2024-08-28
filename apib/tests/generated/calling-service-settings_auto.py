from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallingServiceSettingsApi', 'GetVoicemailRulesObject', 'GetVoicemailRulesObjectBlockPreviousPasscodes',
           'GetVoicemailRulesObjectDefaultVoicemailPinRules',
           'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences',
           'GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits',
           'GetVoicemailRulesObjectDefaultVoicemailPinRulesLength', 'GetVoicemailRulesObjectExpirePasscode',
           'GetVoicemailSettingsObject', 'Language']


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockRepeatedDigits(ApiModel):
    #: If enabled, passcode should not contain repeated digits.
    #: example: True
    enabled: Optional[bool] = None
    #: Maximum number of repeaed digits. The minimum value is 1. The maximum value is 6.
    #: example: 3
    max_: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesBlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of ascending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3
    number_of_ascending_digits: Optional[int] = None
    #: Number of descending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: example: 3
    number_of_descending_digits: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRulesLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    #: example: 3
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    #: example: 3
    max_: Optional[int] = None


class GetVoicemailRulesObjectDefaultVoicemailPinRules(ApiModel):
    #: If enabled, the passcode should not contain repeated pattern.
    #: example: True
    block_repeated_patterns_enabled: Optional[bool] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
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
    #: example: 180
    number_of_days: Optional[int] = None


class GetVoicemailRulesObjectBlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of previous passcodes. The minimum value is 1. The maximum value is 10.
    #: example: 3
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
    #: example: 10
    number_of_days_for_message_expiry: Optional[int] = None
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When
    #: disabled, all unread voicemail messages will be kept.
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


class CallingServiceSettingsApi(ApiChild, base='telephony/config'):
    """
    Calling Service Settings
    
    Calling Service Settings supports reading and writing of Webex Calling service settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_announcement_languages(self) -> list[Language]:
        """
        Read the List of Announcement Languages

        List all languages supported by Webex Calling for announcements and voice prompts.

        Retrieving announcement languages requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :rtype: list[Language]
        """
        url = self.ep('announcementLanguages')
        data = super().get(url)
        r = TypeAdapter(list[Language]).validate_python(data['languages'])
        return r

    def get_voicemail_settings(self, org_id: str = None) -> GetVoicemailSettingsObject:
        """
        Get Voicemail Settings

        Retrieve the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Retrieving organization's voicemail settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :rtype: :class:`GetVoicemailSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/settings')
        data = super().get(url, params=params)
        r = GetVoicemailSettingsObject.model_validate(data)
        return r

    def update_voicemail_settings(self, message_expiry_enabled: bool, number_of_days_for_message_expiry: int,
                                  strict_deletion_enabled: bool = None, voice_message_forwarding_enabled: bool = None,
                                  org_id: str = None):
        """
        Update Voicemail Settings

        Update the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Updating an organization's voicemail settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param message_expiry_enabled: Set to `true` to enable voicemail deletion and set the deletion conditions for
            expired messages.
        :type message_expiry_enabled: bool
        :param number_of_days_for_message_expiry: Number of days after which messages expire.
        :type number_of_days_for_message_expiry: int
        :param strict_deletion_enabled: Set to `true` to delete all read and unread voicemail messages based on the
            time frame you set. Set to `false` to keep all the unread voicemail messages.
        :type strict_deletion_enabled: bool
        :param voice_message_forwarding_enabled: Set to `true` to allow people to configure the email forwarding of
            voicemails.
        :type voice_message_forwarding_enabled: bool
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['messageExpiryEnabled'] = message_expiry_enabled
        body['numberOfDaysForMessageExpiry'] = number_of_days_for_message_expiry
        if strict_deletion_enabled is not None:
            body['strictDeletionEnabled'] = strict_deletion_enabled
        if voice_message_forwarding_enabled is not None:
            body['voiceMessageForwardingEnabled'] = voice_message_forwarding_enabled
        url = self.ep('voicemail/settings')
        super().put(url, params=params, json=body)

    def get_voicemail_rules(self, org_id: str = None) -> GetVoicemailRulesObject:
        """
        Get Voicemail Rules

        Retrieve the organization's voicemail rules.

        Organizational voicemail rules specify the default passcode requirements. They are provided for informational
        purposes only and cannot be modified.

        Retrieving the organization's voicemail rules requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve voicemail rules for this organization.
        :type org_id: str
        :rtype: :class:`GetVoicemailRulesObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/rules')
        data = super().get(url, params=params)
        r = GetVoicemailRulesObject.model_validate(data)
        return r

    def update_voicemail_rules(self, expire_passcode: GetVoicemailRulesObjectExpirePasscode,
                               change_passcode: GetVoicemailRulesObjectExpirePasscode,
                               block_previous_passcodes: GetVoicemailRulesObjectBlockPreviousPasscodes,
                               default_voicemail_pin_enabled: bool = None, default_voicemail_pin: str = None,
                               org_id: str = None):
        """
        Update Voicemail Rules

        Update the organization's default voicemail passcode and/or rules.

        Organizational voicemail rules specify the default passcode requirements.

        If you choose to set a default passcode for new people added to your organization, communicate to your people
        what that passcode is, and that it must be reset before they can access their voicemail. If this feature is
        not turned on, each new person must initially set their own passcode.

        Updating an organization's voicemail passcode and/or rules requires a full administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param expire_passcode: Settings for passcode expiry.
        :type expire_passcode: GetVoicemailRulesObjectExpirePasscode
        :param change_passcode: Settings for passcode changes.
        :type change_passcode: GetVoicemailRulesObjectExpirePasscode
        :param block_previous_passcodes: Settings for previous passcode usage.
        :type block_previous_passcodes: GetVoicemailRulesObjectBlockPreviousPasscodes
        :param default_voicemail_pin_enabled: Set to `true` to enable the default voicemail passcode.
        :type default_voicemail_pin_enabled: bool
        :param default_voicemail_pin: Default voicemail passcode.
        :type default_voicemail_pin: str
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if default_voicemail_pin_enabled is not None:
            body['defaultVoicemailPinEnabled'] = default_voicemail_pin_enabled
        if default_voicemail_pin is not None:
            body['defaultVoicemailPin'] = default_voicemail_pin
        body['expirePasscode'] = expire_passcode.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['changePasscode'] = change_passcode.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['blockPreviousPasscodes'] = block_previous_passcodes.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('voicemail/rules')
        super().put(url, params=params, json=body)

    def get_the_organization_music_on_hold_configuration(self, org_id: str = None) -> str:
        """
        Get the organization Music on Hold configuration

        Retrieve the organization's Music on Hold settings.

        :param org_id: Retrieve Music on Hold settings for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('moh/settings')
        data = super().get(url, params=params)
        r = data['defaultOrgMoh']
        return r

    def update_the_organization_music_on_hold_configuration(self, default_org_moh: str, org_id: str = None):
        """
        Update the organization Music on Hold configuration

        Update the organization's Music on Hold settings.

        :param default_org_moh: Default org level Music on Hold option, can be one of two options: Choose between Opus
            Number 1 (Music On Hold used in other Cisco products like UCM) and existing legacy Music On Hold.
        :type default_org_moh: str
        :param org_id: Patch Music on Hold for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['defaultOrgMoh'] = default_org_moh
        url = self.ep('moh/settings')
        super().put(url, params=params, json=body)
