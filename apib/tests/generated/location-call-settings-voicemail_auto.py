from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetLocationVoicemailGroupObject', 'GetLocationVoicemailGroupObjectEmailCopyOfMessage',
           'GetLocationVoicemailGroupObjectFaxMessage', 'GetLocationVoicemailGroupObjectGreeting',
           'GetLocationVoicemailGroupObjectMessageStorage',
           'GetLocationVoicemailGroupObjectMessageStorageStorageType', 'GetLocationVoicemailGroupObjectNotifications',
           'GetVoicePortalObject', 'GetVoicePortalPasscodeRuleObject',
           'GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes', 'GetVoicePortalPasscodeRuleObjectExpirePasscode',
           'GetVoicePortalPasscodeRuleObjectFailedAttempts', 'GetVoicePortalPasscodeRuleObjectLength',
           'GetVoicemailGroupObject', 'LocationCallSettingsVoicemailApi', 'PutVoicePortalObjectPasscode', 'STATE',
           'TelephonyType', 'VoicePortalAvailableNumberObject']


class GetLocationVoicemailGroupObjectGreeting(str, Enum):
    #: Default voicemail group greeting.
    default = 'DEFAULT'
    #: Custom voicemail group greeting.
    custom = 'CUSTOM'


class GetLocationVoicemailGroupObjectMessageStorageStorageType(str, Enum):
    #: Store messages in internal mailbox.
    internal = 'INTERNAL'
    #: Send messages to the email address provided.
    external = 'EXTERNAL'


class GetLocationVoicemailGroupObjectMessageStorage(ApiModel):
    #: Message storage type
    #: example: EXTERNAL
    storage_type: Optional[GetLocationVoicemailGroupObjectMessageStorageStorageType] = None
    #: External email to forward the message.
    #: example: user@flex2.cisco.com
    external_email: Optional[str] = None


class GetLocationVoicemailGroupObjectNotifications(ApiModel):
    #: Enable/disable messages notification
    #: example: True
    enabled: Optional[bool] = None
    #: Notifications to be sent to provided email to SMS gateway.
    #: example: user@flex2.cisco.com
    destination: Optional[str] = None


class GetLocationVoicemailGroupObjectFaxMessage(ApiModel):
    #: Enable/disable fax messaging.
    #: example: True
    enabled: Optional[bool] = None
    #: Phone number to receive fax messages.
    #: example: +1234234324
    phone_number: Optional[str] = None
    #: Extension to receive fax messages.
    #: example: 23455
    extension: Optional[int] = None


class GetLocationVoicemailGroupObjectEmailCopyOfMessage(ApiModel):
    #: Enable/disable to email message copy.
    #: example: True
    enabled: Optional[bool] = None
    #: Email message copy to email address provided.
    #: example: user@flex2.cisco.com
    email_id: Optional[str] = None


class GetLocationVoicemailGroupObject(ApiModel):
    #: UUID of voicemail group of a particular location.
    #: example: a7dd4d39-4a78-4516-955f-7810dbe379cf
    id: Optional[str] = None
    #: Name of the voicemail group.
    #: example: VGName
    name: Optional[str] = None
    #: Voicemail group phone number.
    #: example: +1234234324
    phone_number: Optional[str] = None
    #: Voicemail group extension number.
    #: example: 23455
    extension: Optional[int] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 123423455
    esn: Optional[str] = None
    #: Voicemail group toll free number.
    toll_free_number: Optional[bool] = None
    #: Voicemail group caller ID first name.
    #: example: Customer
    first_name: Optional[str] = None
    #: Voicemail group called ID last name.
    #: example: Support
    last_name: Optional[str] = None
    #: Enable/disable voicemail group.
    #: example: True
    enabled: Optional[bool] = None
    #: Language for voicemail group audio announcement.
    #: example: en_us
    language_code: Optional[str] = None
    #: Set voicemail group greeting type.
    #: example: DEFAULT
    greeting: Optional[GetLocationVoicemailGroupObjectGreeting] = None
    #: Enabled if CUSTOM greeting is previously uploaded.
    #: example: True
    greeting_uploaded: Optional[bool] = None
    #: CUSTOM greeting for previously uploaded.
    #: example: short greeting.wav
    greeting_description: Optional[str] = None
    #: Message storage information
    message_storage: Optional[GetLocationVoicemailGroupObjectMessageStorage] = None
    #: Message notifications
    notifications: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Fax message receive settings
    fax_message: Optional[GetLocationVoicemailGroupObjectFaxMessage] = None
    #: Transfer message information
    transfer_to_number: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Message copy information
    email_copy_of_message: Optional[GetLocationVoicemailGroupObjectEmailCopyOfMessage] = None
    #: Enable/disable to forward voice message.
    #: example: True
    voice_message_forwarding_enabled: Optional[bool] = None


class GetVoicePortalObject(ApiModel):
    #: Voice Portal ID
    #: example: Y2lzY29zcGFyazovL3VzL1ZPSUNFTUFJTF9HUk9VUC8yZmQzZGMwMy0yZWRhLTQ4NmUtODdhYS0xODY1ZDI5YWExZWI
    id: Optional[str] = None
    #: Voice Portal Name.
    #: example: test voicePortal
    name: Optional[str] = None
    #: Language for audio announcements.
    #: example: English
    language: Optional[str] = None
    #: Language code for voicemail group audio announcement.
    #: example: en_us
    language_code: Optional[str] = None
    #: Extension of incoming call.
    #: example: 7
    extension: Optional[str] = None
    #: Phone Number of incoming call.
    #: example: +1345325235
    phone_number: Optional[str] = None
    #: Caller ID First Name.
    #: example: firstName
    first_name: Optional[str] = None
    #: Caller ID Last Name.
    #: example: lastName
    last_name: Optional[str] = None


class GetVoicePortalPasscodeRuleObjectExpirePasscode(ApiModel):
    #: If enabled, passcode expires after the number of days specified.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of days for passcode expiry. The minimum value is 15. The maximum value is 100.
    #: example: 180
    number_of_days: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectFailedAttempts(ApiModel):
    #: If enabled, allows specified number of attempts before locking voice portal access.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of failed attempts allowed.
    #: example: 3
    attempts: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes(ApiModel):
    #: If enabled, the specified number of passcode changes must occur before a passcode can be re-used.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of required passcodes changes. The minimum value is 1. The maximum value is 10.
    #: example: 3
    number_of_passcodes: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    #: example: 3
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    #: example: 3
    max_: Optional[int] = None


class GetVoicePortalPasscodeRuleObject(ApiModel):
    #: Settings for passcode expiry.
    expire_passcode: Optional[GetVoicePortalPasscodeRuleObjectExpirePasscode] = None
    #: Number of failed attempts allowed.
    failed_attempts: Optional[GetVoicePortalPasscodeRuleObjectFailedAttempts] = None
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
    #: 
    #: + enabled: true (boolean) - If enabled, passcode should not contain repeated digits.
    #: + max: `3` (number) - Maximum number of digits to be considered as a repeated sequence. The minimum value is 1.
    #: The maximum value is 6.
    block_repeated_digits: Optional[Any] = None
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    #: 
    #: + enabled: true (boolean) - If enabled, do not allow the specified number of ascending or descending digits in a
    #: row.
    #: + numberOfAscendingDigits: `3` (number) -  Number of ascending digits in sequence. The minimum value is 2. The
    #: maximum value is 5.
    #: + numberOfDescendingDigits: `3` (number) -  Number of descending digits in sequence. The minimum value is 2. The
    #: maximum value is 5.
    block_contiguous_sequences: Optional[Any] = None
    #: Allowed length of the passcode.
    length: Optional[GetVoicePortalPasscodeRuleObjectLength] = None
    #: If enabled, the passcode do not contain repeated pattern.
    #: example: True
    block_repeated_patterns_enabled: Optional[bool] = None
    #: If enabled, the passcode do not allow user phone number or extension.
    #: example: True
    block_user_number_enabled: Optional[bool] = None
    #: If enabled, the passcode do not allow revered phone number or extension.
    #: example: True
    block_reversed_user_number_enabled: Optional[bool] = None
    #: If enabled, the passcode do not allow setting reversed old passcode.
    #: example: True
    block_reversed_old_passcode_enabled: Optional[bool] = None


class GetVoicemailGroupObject(ApiModel):
    #: Voicemail Group ID.
    #: example: Y2lzY29zcGFyazovL3VzL1ZPSUNFTUFJTF9HUk9VUC8yZmQzZGMwMy0yZWRhLTQ4NmUtODdhYS0xODY1ZDI5YWExZWI
    id: Optional[str] = None
    #: Voicemail Group Name.
    #: example: test
    name: Optional[str] = None
    #: Location Name.
    #: example: San Jose
    location_name: Optional[str] = None
    #: Location ID.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    location_id: Optional[str] = None
    #: Extension of the voicemail group.
    #: example: 7
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12340007
    esn: Optional[str] = None
    #: Phone number of the voicemail group.
    #: example: +1345325235
    phone_number: Optional[str] = None
    #: If enabled, incoming calls are sent to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: Flag to indicate if the number is toll free.
    #: example: True
    toll_free_number: Optional[bool] = None


class PutVoicePortalObjectPasscode(ApiModel):
    #: New passcode.
    #: example: testPass123
    new_passcode: Optional[str] = None
    #: Confirm new passcode.
    #: example: testPass123
    confirm_passcode: Optional[str] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class VoicePortalAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    #: example: True
    is_service_number: Optional[bool] = None


class LocationCallSettingsVoicemailApi(ApiChild, base='telephony/config'):
    """
    Location Call Settings:  Voicemail
    
    Location Call Settings: Voicemail supports reading and writing of Webex
    Calling Location Voicemail settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_location_voicemail(self, location_id: str, org_id: str = None) -> bool:
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving a location's voicemail settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve voicemail settings for this location.
        :type location_id: str
        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemail')
        data = super().get(url, params=params)
        r = data['voicemailTranscriptionEnabled']
        return r

    def update_location_voicemail(self, location_id: str, voicemail_transcription_enabled: bool, org_id: str = None):
        """
        Update Location Voicemail

        Update the voicemail settings for a specific location.

        Location voicemail settings allows you to enable voicemail transcription for a specific location.

        Updating a location's voicemail settings requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update voicemail settings for this location.
        :type location_id: str
        :param voicemail_transcription_enabled: Set to `true` to enable voicemail transcription.
        :type voicemail_transcription_enabled: bool
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['voicemailTranscriptionEnabled'] = voicemail_transcription_enabled
        url = self.ep(f'locations/{location_id}/voicemail')
        super().put(url, params=params, json=body)

    def get_voice_portal(self, location_id: str, org_id: str = None) -> GetVoicePortalObject:
        """
        Get VoicePortal

        Retrieve Voice portal information for the location.

        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant announcements.

        Retrieving voice portal information for an organization requires a full read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        :rtype: :class:`GetVoicePortalObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicePortal')
        data = super().get(url, params=params)
        r = GetVoicePortalObject.model_validate(data)
        return r

    def update_voice_portal(self, location_id: str, name: str, language_code: str, first_name: str, last_name: str,
                            passcode: PutVoicePortalObjectPasscode, extension: str = None, phone_number: str = None,
                            org_id: str = None):
        """
        Update VoicePortal

        Update Voice portal information for the location.

        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant anouncements.

        Updating voice portal information for an organization and/or rules requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param name: Voice Portal Name.
        :type name: str
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param first_name: Caller ID First Name.
        :type first_name: str
        :param last_name: Caller ID Last Name.
        :type last_name: str
        :param passcode: Voice Portal Admin Passcode.
        :type passcode: PutVoicePortalObjectPasscode
        :param extension: Extension of incoming call.
        :type extension: str
        :param phone_number: Phone Number of incoming call.
        :type phone_number: str
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['languageCode'] = language_code
        if extension is not None:
            body['extension'] = extension
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        body['firstName'] = first_name
        body['lastName'] = last_name
        body['passcode'] = passcode.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/voicePortal')
        super().put(url, params=params, json=body)

    def get_voice_portal_passcode_rule(self, location_id: str, org_id: str = None) -> GetVoicePortalPasscodeRuleObject:
        """
        Get VoicePortal Passcode Rule

        Retrieve the voice portal passcode rule for a location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        anouncements

        Retrieving the voice portal passcode rule requires a full read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str
        :rtype: :class:`GetVoicePortalPasscodeRuleObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicePortal/passcodeRules')
        data = super().get(url, params=params)
        r = GetVoicePortalPasscodeRuleObject.model_validate(data)
        return r

    def list_voicemail_group(self, location_id: str = None, name: str = None, phone_number: str = None,
                             org_id: str = None, **params) -> Generator[GetVoicemailGroupObject, None, None]:
        """
        List VoicemailGroup

        List the voicemail group information for the organization.

        You can create a shared voicemail box and inbound FAX box to
        assign to users or call routing features like an auto attendant, call queue, or hunt group.

        Retrieving a voicemail group for the organization requires a full read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :return: Generator yielding :class:`GetVoicemailGroupObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('voicemailGroups')
        return self.session.follow_pagination(url=url, model=GetVoicemailGroupObject, item_key='voicemailGroups', params=params)

    def get_location_voicemail_group(self, location_id: str, voicemail_group_id: str,
                                     org_id: str = None) -> GetLocationVoicemailGroupObject:
        """
        Get Location Voicemail Group

        Retrieve voicemail group details for a location.

        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active,
        message storage settings, and how you would like to be notified of new voicemail messages.

        Retrieving voicemail group details requires a full, user or read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str
        :rtype: :class:`GetLocationVoicemailGroupObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        data = super().get(url, params=params)
        r = GetLocationVoicemailGroupObject.model_validate(data)
        return r

    def modify_location_voicemail_group(self, location_id: str, voicemail_group_id: str,
                                        message_storage: GetLocationVoicemailGroupObjectMessageStorage,
                                        notifications: GetLocationVoicemailGroupObjectNotifications,
                                        fax_message: GetLocationVoicemailGroupObjectFaxMessage,
                                        transfer_to_number: GetLocationVoicemailGroupObjectNotifications,
                                        email_copy_of_message: GetLocationVoicemailGroupObjectEmailCopyOfMessage,
                                        name: str = None, phone_number: str = None, extension: int = None,
                                        first_name: str = None, last_name: str = None, enabled: bool = None,
                                        passcode: int = None, language_code: str = None,
                                        greeting: GetLocationVoicemailGroupObjectGreeting = None,
                                        greeting_description: str = None, org_id: str = None):
        """
        Modify Location Voicemail Group

        Modifies the voicemail group location details for a particular location for a customer.

        Manage your voicemail settings, like when you want your voicemail to be active, message storage settings, and
        how you would like to be notified of new voicemail messages.

        Modifying the voicemail group location details requires a full, user administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Modifies the voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Modifies the voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param message_storage: Message storage information
        :type message_storage: GetLocationVoicemailGroupObjectMessageStorage
        :param notifications: Message notifications
        :type notifications: GetLocationVoicemailGroupObjectNotifications
        :param fax_message: Fax message receive settings
        :type fax_message: GetLocationVoicemailGroupObjectFaxMessage
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: GetLocationVoicemailGroupObjectNotifications
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: GetLocationVoicemailGroupObjectEmailCopyOfMessage
        :param name: Set the name of the voicemail group.
        :type name: str
        :param phone_number: Set voicemail group phone number.
        :type phone_number: str
        :param extension: Set unique voicemail group extension number.
        :type extension: int
        :param first_name: Set the voicemail group caller ID first name.
        :type first_name: str
        :param last_name: Set the voicemail group called ID last name.
        :type last_name: str
        :param enabled: Set to `true` to enable the voicemail group.
        :type enabled: bool
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for the voicemail group audio announcement.
        :type language_code: str
        :param greeting: Voicemail group greeting type.
        :type greeting: GetLocationVoicemailGroupObjectGreeting
        :param greeting_description: CUSTOM greeting for previously uploaded.
        :type greeting_description: str
        :param org_id: Modifies the voicemail group details for a customer location.
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
        if enabled is not None:
            body['enabled'] = enabled
        if passcode is not None:
            body['passcode'] = passcode
        if language_code is not None:
            body['languageCode'] = language_code
        if greeting is not None:
            body['greeting'] = enum_str(greeting)
        if greeting_description is not None:
            body['greetingDescription'] = greeting_description
        body['messageStorage'] = message_storage.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['notifications'] = notifications.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['faxMessage'] = fax_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['transferToNumber'] = transfer_to_number.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['emailCopyOfMessage'] = email_copy_of_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().put(url, params=params, json=body)

    def create_a_new_voicemail_group_for_a_location(self, location_id: str, name: str, extension: int, passcode: int,
                                                    language_code: str,
                                                    message_storage: GetLocationVoicemailGroupObjectMessageStorage,
                                                    notifications: GetLocationVoicemailGroupObjectNotifications,
                                                    fax_message: GetLocationVoicemailGroupObjectFaxMessage,
                                                    transfer_to_number: GetLocationVoicemailGroupObjectNotifications,
                                                    email_copy_of_message: GetLocationVoicemailGroupObjectEmailCopyOfMessage,
                                                    phone_number: str = None, first_name: str = None,
                                                    last_name: str = None, org_id: str = None) -> str:
        """
        Create a new Voicemail Group for a Location

        Create a new voicemail group for the given location for a customer.

        A voicemail group can be created for given location for a customer.

        Creating a voicemail group for the given location requires a full or user administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Create a new voice mail group for this location.
        :type location_id: str
        :param name: Set name to create new voicemail group for a particular location for a customer.
        :type name: str
        :param extension: Set unique voicemail group extension number for this particular location.
        :type extension: int
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param message_storage: Message storage information
        :type message_storage: GetLocationVoicemailGroupObjectMessageStorage
        :param notifications: Message notifications
        :type notifications: GetLocationVoicemailGroupObjectNotifications
        :param fax_message: Fax message information
        :type fax_message: GetLocationVoicemailGroupObjectFaxMessage
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: GetLocationVoicemailGroupObjectNotifications
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: GetLocationVoicemailGroupObjectEmailCopyOfMessage
        :param phone_number: Set voicemail group phone number for this particular location.
        :type phone_number: str
        :param first_name: Set voicemail group caller ID first name.
        :type first_name: str
        :param last_name: Set voicemail group called ID last name.
        :type last_name: str
        :param org_id: Create a new voice mail group for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        body['passcode'] = passcode
        body['languageCode'] = language_code
        body['messageStorage'] = message_storage.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['notifications'] = notifications.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['faxMessage'] = fax_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['transferToNumber'] = transfer_to_number.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['emailCopyOfMessage'] = email_copy_of_message.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/voicemailGroups')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_voicemail_group_for_a_location(self, location_id: str, voicemail_group_id: str, org_id: str = None):
        """
        Delete a Voicemail Group for a Location

        Delete the designated voicemail group.

        Deleting a voicemail group requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a voicemail group.
        :type location_id: str
        :param voicemail_group_id: Delete the voicemail group with the matching ID.
        :type voicemail_group_id: str
        :param org_id: Delete the voicemail group from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().delete(url, params=params)

    def get_voicemail_group_fax_message_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                                org_id: str = None,
                                                                **params) -> Generator[VoicePortalAvailableNumberObject, None, None]:
        """
        Get Voicemail Group Fax Message Available Phone Numbers

        List the standard and service PSTN numbers that are available to be assigned as a voicemail group's FAX message
        phone number.
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
        :return: Generator yielding :class:`VoicePortalAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/voicemailGroups/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=VoicePortalAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_voicemail_group_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                    org_id: str = None,
                                                    **params) -> Generator[VoicePortalAvailableNumberObject, None, None]:
        """
        Get Voicemail Group Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as a voicemail group's phone
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
        :return: Generator yielding :class:`VoicePortalAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/voicemailGroups/availableNumbers')
        return self.session.follow_pagination(url=url, model=VoicePortalAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_voice_portal_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                 org_id: str = None,
                                                 **params) -> Generator[VoicePortalAvailableNumberObject, None, None]:
        """
        Get VoicePortal Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the location voice portal's
        phone number.
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
        :return: Generator yielding :class:`VoicePortalAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/voicePortal/availableNumbers')
        return self.session.follow_pagination(url=url, model=VoicePortalAvailableNumberObject, item_key='phoneNumbers', params=params)
