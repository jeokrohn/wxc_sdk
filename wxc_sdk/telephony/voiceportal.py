"""
Voice portal API
"""
import json
from collections.abc import Generator
from typing import Optional

from pydantic import Field

from .vm_rules import BlockPreviousPasscodes, BlockRepeatedDigits, BlockContiguousSequences, PinLength
from ..api_child import ApiChild
from ..base import ApiModel

__all__ = ['VoicePortalSettings', 'FailedAttempts', 'ExpirePasscode', 'PasscodeRules', 'VoicePortalApi']

from ..person_settings.available_numbers import AvailableNumber


class VoicePortalSettings(ApiModel):
    #: Voice Portal ID
    portal_id: Optional[str] = Field(alias='id', default=None)
    #: Voice Portal Name.
    name: str
    #: Language for audio announcements.
    language: str
    #: Language code for voicemail group audio announcement
    language_code: str
    #: Extension of incoming call.
    extension: Optional[str] = None
    #: Phone Number of incoming call.
    phone_number: Optional[str] = None
    #: Caller ID First Name.
    first_name: str
    #: Caller ID Last Name
    last_name: str


class FailedAttempts(ApiModel):
    """
    Number of failed attempts allowed.
    """
    #: If enabled, allows specified number of attempts before locking voice portal access.
    enabled: bool
    #: Number of failed attempts allowed.
    attempts: int


class ExpirePasscode(ApiModel):
    enabled: bool
    days: int


class PasscodeRules(ApiModel):
    #: Settings for passcode expiry.
    expire_passcode: Optional[ExpirePasscode] = None
    #: Number of failed attempts allowed.
    failed_attempts: FailedAttempts
    #: Settings for previous passcode usage.
    block_previous_passcodes: BlockPreviousPasscodes
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
    block_repeated_digits: BlockRepeatedDigits
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    block_contiguous_sequences: BlockContiguousSequences
    #: Allowed length of the passcode.
    length: PinLength
    #: If enabled, the passcode do not allow revered phone number or extension.
    block_reversed_user_number_enabled: bool
    #: If enabled, the passcode do not allow user phone number or extension.
    block_user_number_enabled: bool
    #: If enabled, the passcode do not contain repeated pattern.
    block_repeated_patterns_enabled: bool
    #: If enabled, the passcode do not allow setting reversed old passcode.
    block_reversed_old_passcode_enabled: bool


class VoicePortalApi(ApiChild, base='telephony/config/locations'):
    """
    location voice portal API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicePortal

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicePortal{path}')
        return ep

    def read(self, location_id: str, org_id: str = None) -> VoicePortalSettings:
        """

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        :return: location voice portal settings
        :rtype: VoicePortalSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        return VoicePortalSettings.model_validate(self.get(url, params=params))

    def update(self, location_id: str, settings: VoicePortalSettings, passcode: str = None, org_id: str = None):
        """
        Update VoicePortal

        Update Voice portal information for the location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements.

        Updating voice portal information for organization and/or rules requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param settings: new settings
        :type settings: VoicePortalSettings
        :param passcode: new passcode
        :type passcode: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        """
        data = json.loads(settings.model_dump_json(exclude={'portal_id': True,
                                                            'language': True}))
        if passcode is not None:
            data['passcode'] = {'newPasscode': passcode,
                                'confirmPasscode': passcode}
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        self.put(url, params=params, json=data)

    def passcode_rules(self, location_id: str, org_id: str = None) -> PasscodeRules:
        """
        Get VoicePortal Passcode Rule

        Retrieve the voice portal passcode rule for a location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements

        Retrieving the voice portal passcode rule requires a full read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str
        :return: passcode rules
        :rtype: PasscodeRules
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='passcodeRules')
        return PasscodeRules.model_validate(self.get(url, params=params))

    def available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                org_id: str = None,
                                **params) -> Generator[AvailableNumber, None, None]:
        """
        Get VoicePortal Available Phone Numbers

        List service and standard numbers that are available to be assigned as the location voice portal's phone
        number.
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
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)
