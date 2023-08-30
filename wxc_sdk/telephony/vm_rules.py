"""
API for voicemail rules
"""

from typing import Optional

from ..api_child import ApiChild
from ..base import ApiModel

__all__ = ['BlockRepeatedDigits', 'BlockContiguousSequences', 'PinLength', 'DefaultVoicemailPinRules',
           'EnabledAndNumberOfDays', 'BlockPreviousPasscodes', 'VoiceMailRules', 'VoicemailRulesApi']


class BlockRepeatedDigits(ApiModel):
    """
    Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
    """
    #: If enabled, passcode should not contain repeated digits.
    enabled: Optional[bool] = None
    #: Maximum number of repeated digits. Min 1, Max 6.
    max: Optional[int] = None


class BlockContiguousSequences(ApiModel):
    """
    Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    """
    #: If enabled, passcode should not contain a numerical sequence.
    enabled: Optional[bool] = None
    #: Number of ascending digits in sequence. Min 2, Max 5.
    number_of_ascending_digits: Optional[int] = None
    #: Number of descending digits in sequence. Min 2, Max 5.
    number_of_descending_digits: Optional[int] = None


class PinLength(ApiModel):
    """
    Length of the passcode.
    """
    #: Min 2, Max 15.
    min: Optional[int] = None
    #: Min 3, Max 30.
    max: Optional[int] = None


class DefaultVoicemailPinRules(ApiModel):
    """
    Default voicemail passcode requirements.
    """
    #: If enabled, the passcode should not contain repeated pattern.
    block_repeated_patterns_enabled: Optional[bool] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
    block_repeated_digits: Optional[BlockRepeatedDigits] = None
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    block_contiguous_sequences: Optional[BlockContiguousSequences] = None
    #: Length of the passcode.
    length: Optional[PinLength] = None
    #: If enabled, default voicemail passcode can be set.
    default_voicemail_pin_enabled: Optional[bool] = None

    @staticmethod
    def default() -> 'DefaultVoicemailPinRules':
        return DefaultVoicemailPinRules(block_repeated_patterns_enabled=True,
                                        block_repeated_digits=BlockRepeatedDigits(enabled=True, max=3),
                                        block_contiguous_sequences=BlockContiguousSequences(
                                            enabled=True,
                                            number_of_descending_digits=3,
                                            number_of_ascending_digits=3),
                                        length=PinLength(min=6, max=30),
                                        default_voicemail_pin_enabled=False)


class BlockPreviousPasscodes(ApiModel):
    """
    Settings for previous passcode usage.
    """
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    enabled: Optional[bool] = None
    #: Number of previous passcodes. Min 1, Max 10.
    number_of_passcodes: Optional[int] = None


class EnabledAndNumberOfDays(ApiModel):
    """
    Settings for passcode expiry or passcode changes
    """
    enabled: Optional[bool] = None
    number_of_days: Optional[int] = None


class VoiceMailRules(ApiModel):
    #: Default voicemail passcode requirements.
    default_voicemail_pin_rules: Optional[DefaultVoicemailPinRules] = None
    #: Set to true to enable default voicemail passcode; only used in update()
    default_voicemail_pin_enabled: Optional[bool] = None
    #: Default voicemail passcode; only used in update()
    default_voicemail_pin: Optional[str] = None
    #: Settings for passcode expiry.
    expire_passcode: Optional[EnabledAndNumberOfDays] = None
    #: Settings for passcode changes.
    change_passcode: Optional[EnabledAndNumberOfDays] = None
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[BlockPreviousPasscodes] = None

    @staticmethod
    def default() -> 'VoiceMailRules':
        return VoiceMailRules(default_voicemail_pin_rules=DefaultVoicemailPinRules.default(),
                              expire_passcode=EnabledAndNumberOfDays(enabled=True, number_of_days=180),
                              change_passcode=EnabledAndNumberOfDays(enabled=False, number_of_days=1),
                              block_previous_passcodes=BlockPreviousPasscodes(enabled=True, number_of_passcodes=10))


class VoicemailRulesApi(ApiChild, base='telephony/config/voicemail/rules'):
    """
    API for voicemail rules settings
    """

    def read(self, org_id: str = None) -> VoiceMailRules:
        """
        Get Voicemail Rules

        Retrieve the organization's voicemail rules.

        Organizational voicemail rules specify the default passcode requirements.

        Retrieving the organization's voicemail rules requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return VoiceMailRules.model_validate(self.get(url, params=params))

    def update(self, settings: VoiceMailRules, org_id: str = None):
        """
        Update Voicemail Rules

        Update the organization's default voicemail passcode and/or rules.

        Organizational voicemail rules specify the default passcode requirements.

        If you choose to set default passcode for new people added to your organization, communicate to your people
        what that passcode is, and that it must be reset before they can access their voicemail. If this feature is
        not turned on, each new person must initially set their own passcode.

        Updating organization's voicemail passcode and/or rules requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: VoiceMailRules
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.model_dump_json(exclude={'default_voicemail_pin_rules': True})
        self.put(url, params=params, data=data)
