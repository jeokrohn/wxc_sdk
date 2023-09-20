from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetLocationVoicemailGroupObject', 'GetLocationVoicemailGroupObjectEmailCopyOfMessage', 'GetLocationVoicemailGroupObjectFaxMessage', 'GetLocationVoicemailGroupObjectGreeting', 'GetLocationVoicemailGroupObjectMessageStorage', 'GetLocationVoicemailGroupObjectMessageStorageStorageType', 'GetLocationVoicemailGroupObjectNotifications', 'GetLocationVoicemailObject', 'GetVoicePortalObject', 'GetVoicePortalPasscodeRuleObject', 'GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes', 'GetVoicePortalPasscodeRuleObjectBlockRepeatedDigits', 'GetVoicePortalPasscodeRuleObjectExpirePasscode', 'GetVoicePortalPasscodeRuleObjectFailedAttempts', 'GetVoicePortalPasscodeRuleObjectLength', 'GetVoicemailGroupObject', 'PostLocationVoicemailGroupObject', 'PutLocationVoicemailGroupObject', 'PutVoicePortalObject', 'PutVoicePortalObjectPasscode']


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
    storageType: Optional[GetLocationVoicemailGroupObjectMessageStorageStorageType] = None
    #: External email to forward the message.
    #: example: user@flex2.cisco.com
    externalEmail: Optional[str] = None


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
    phoneNumber: Optional[str] = None
    #: Extension to receive fax messages.
    #: example: 23455.0
    extension: Optional[int] = None


class GetLocationVoicemailGroupObjectEmailCopyOfMessage(ApiModel):
    #: Enable/disable to email message copy.
    #: example: True
    enabled: Optional[bool] = None
    #: Email message copy to email address provided.
    #: example: user@flex2.cisco.com
    emailId: Optional[str] = None


class GetLocationVoicemailGroupObject(ApiModel):
    #: UUID of voicemail group of a particular location.
    #: example: a7dd4d39-4a78-4516-955f-7810dbe379cf
    id: Optional[str] = None
    #: Name of the voicemail group.
    #: example: VGName
    name: Optional[str] = None
    #: Voicemail group phone number.
    #: example: +1234234324
    phoneNumber: Optional[str] = None
    #: Voicemail group extension number.
    #: example: 23455.0
    extension: Optional[int] = None
    #: Voicemail group toll free number.
    tollFreeNumber: Optional[bool] = None
    #: Voicemail group caller ID first name.
    #: example: Customer
    firstName: Optional[str] = None
    #: Voicemail group called ID last name.
    #: example: Support
    lastName: Optional[str] = None
    #: Enable/disable voicemail group.
    #: example: True
    enabled: Optional[bool] = None
    #: Language for voicemail group audio announcement.
    #: example: en_us
    languageCode: Optional[str] = None
    #: Set voicemail group greeting type.
    #: example: DEFAULT
    greeting: Optional[GetLocationVoicemailGroupObjectGreeting] = None
    #: Enabled if CUSTOM greeting is previously uploaded.
    #: example: True
    greetingUploaded: Optional[bool] = None
    #: CUSTOM greeting for previously uploaded.
    #: example: short greeting.wav
    greetingDescription: Optional[str] = None
    #: Message storage information
    messageStorage: Optional[GetLocationVoicemailGroupObjectMessageStorage] = None
    #: Message notifications
    notifications: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Fax message receive settings
    faxMessage: Optional[GetLocationVoicemailGroupObjectFaxMessage] = None
    #: Transfer message information
    transferToNumber: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Message copy information
    emailCopyOfMessage: Optional[GetLocationVoicemailGroupObjectEmailCopyOfMessage] = None
    #: Enable/disable to forward voice message.
    #: example: True
    voiceMessageForwardingEnabled: Optional[bool] = None


class GetLocationVoicemailObject(ApiModel):
    #: Set to `true` to enable voicemail transcription.
    #: example: True
    voicemailTranscriptionEnabled: Optional[bool] = None


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
    languageCode: Optional[str] = None
    #: Extension of incoming call.
    #: example: 0007
    extension: Optional[datetime] = None
    #: Phone Number of incoming call.
    #: example: +1345325235
    phoneNumber: Optional[str] = None
    #: Caller ID First Name.
    #: example: firstName
    firstName: Optional[str] = None
    #: Caller ID Last Name.
    #: example: lastName
    lastName: Optional[str] = None


class GetVoicePortalPasscodeRuleObjectExpirePasscode(ApiModel):
    #: If enabled, passcode expires after the number of days specified.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of days for passcode expiry. The minimum value is 15. The maximum value is 100.
    #: example: 180.0
    numberOfDays: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectFailedAttempts(ApiModel):
    #: If enabled, allows specified number of attempts before locking voice portal access.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of failed attempts allowed.
    #: example: 3.0
    attempts: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes(ApiModel):
    #: If enabled, the specified number of passcode changes must occur before a passcode can be re-used.
    #: example: True
    enabled: Optional[bool] = None
    #: Number of required passcodes changes. The minimum value is 1. The maximum value is 10.
    #: example: 3.0
    numberOfPasscodes: Optional[int] = None


class GetVoicePortalPasscodeRuleObjectBlockRepeatedDigits(ApiModel):
    ...


class GetVoicePortalPasscodeRuleObjectLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    #: example: 3.0
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    #: example: 3.0
    max: Optional[int] = None


class GetVoicePortalPasscodeRuleObject(ApiModel):
    #: Settings for passcode expiry.
    expirePasscode: Optional[GetVoicePortalPasscodeRuleObjectExpirePasscode] = None
    #: Number of failed attempts allowed.
    failedAttempts: Optional[GetVoicePortalPasscodeRuleObjectFailedAttempts] = None
    #: Settings for previous passcode usage.
    blockPreviousPasscodes: Optional[GetVoicePortalPasscodeRuleObjectBlockPreviousPasscodes] = None
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
    #: + enabled: true (boolean) - If enabled, passcode should not contain repeated digits.
    #: + max: `3` (number) - Maximum number of digits to be considered as a repeated sequence. The minimum value is 1. The maximum value is 6.
    blockRepeatedDigits: Optional[GetVoicePortalPasscodeRuleObjectBlockRepeatedDigits] = None
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    #: + enabled: true (boolean) - If enabled, do not allow the specified number of ascending or descending digits in a row.
    #: + numberOfAscendingDigits: `3` (number) -  Number of ascending digits in sequence. The minimum value is 2. The maximum value is 5.
    #: + numberOfDescendingDigits: `3` (number) -  Number of descending digits in sequence. The minimum value is 2. The maximum value is 5.
    blockContiguousSequences: Optional[GetVoicePortalPasscodeRuleObjectBlockRepeatedDigits] = None
    #: Allowed length of the passcode.
    length: Optional[GetVoicePortalPasscodeRuleObjectLength] = None
    #: If enabled, the passcode do not contain repeated pattern.
    #: example: True
    blockRepeatedPatternsEnabled: Optional[bool] = None
    #: If enabled, the passcode do not allow user phone number or extension.
    #: example: True
    blockUserNumberEnabled: Optional[bool] = None
    #: If enabled, the passcode do not allow revered phone number or extension.
    #: example: True
    blockReversedUserNumberEnabled: Optional[bool] = None
    #: If enabled, the passcode do not allow setting reversed old passcode.
    #: example: True
    blockReversedOldPasscodeEnabled: Optional[bool] = None


class GetVoicemailGroupObject(ApiModel):
    #: Voicemail Group ID.
    #: example: Y2lzY29zcGFyazovL3VzL1ZPSUNFTUFJTF9HUk9VUC8yZmQzZGMwMy0yZWRhLTQ4NmUtODdhYS0xODY1ZDI5YWExZWI
    id: Optional[str] = None
    #: Voicemail Group Name.
    #: example: test
    name: Optional[str] = None
    #: Location Name.
    #: example: San Jose
    locationName: Optional[str] = None
    #: Location ID.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    locationId: Optional[str] = None
    #: Extension of the voicemail group.
    #: example: 0007
    extension: Optional[datetime] = None
    #: Phone number of the voicemail group.
    #: example: +1345325235
    phoneNumber: Optional[str] = None
    #: If enabled, incoming calls are sent to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: Flag to indicate if the number is toll free.
    #: example: True
    tollFreeNumber: Optional[bool] = None


class PostLocationVoicemailGroupObject(ApiModel):
    #: Set name to create new voicemail group for a particular location for a customer.
    #: example: VGName
    name: Optional[str] = None
    #: Set voicemail group phone number for this particular location.
    #: example: +1234234324
    phoneNumber: Optional[str] = None
    #: Set unique voicemail group extension number for this particular location.
    #: example: 23455.0
    extension: Optional[int] = None
    #: Set voicemail group caller ID first name.
    #: example: Customer
    firstName: Optional[str] = None
    #: Set voicemail group called ID last name.
    #: example: Support
    lastName: Optional[str] = None
    #: Set passcode to access voicemail group when calling.
    #: example: 1234.0
    passcode: Optional[int] = None
    #: Language code for voicemail group audio announcement.
    #: example: en_us
    languageCode: Optional[str] = None
    #: Message storage information
    messageStorage: Optional[GetLocationVoicemailGroupObjectMessageStorage] = None
    #: Message notifications
    notifications: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Fax message information
    faxMessage: Optional[GetLocationVoicemailGroupObjectFaxMessage] = None
    #: Transfer message information
    transferToNumber: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Message copy information
    emailCopyOfMessage: Optional[GetLocationVoicemailGroupObjectEmailCopyOfMessage] = None


class PutLocationVoicemailGroupObject(ApiModel):
    #: Set the name of the voicemail group.
    #: example: VGName
    name: Optional[str] = None
    #: Set voicemail group phone number.
    #: example: +1234234324
    phoneNumber: Optional[str] = None
    #: Set unique voicemail group extension number.
    #: example: 23455.0
    extension: Optional[int] = None
    #: Set the voicemail group caller ID first name.
    #: example: Customer
    firstName: Optional[str] = None
    #: Set the voicemail group called ID last name.
    #: example: Support
    lastName: Optional[str] = None
    #: Set to `true` to enable the voicemail group.
    #: example: True
    enabled: Optional[bool] = None
    #: Set passcode to access voicemail group when calling.
    #: example: 1234.0
    passcode: Optional[int] = None
    #: Language code for the voicemail group audio announcement.
    #: example: en_us
    languageCode: Optional[str] = None
    #: Voicemail group greeting type.
    #: example: DEFAULT
    greeting: Optional[GetLocationVoicemailGroupObjectGreeting] = None
    #: CUSTOM greeting for previously uploaded.
    #: example: short greeting.wav
    greetingDescription: Optional[str] = None
    #: Message storage information
    messageStorage: Optional[GetLocationVoicemailGroupObjectMessageStorage] = None
    #: Message notifications
    notifications: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Fax message receive settings
    faxMessage: Optional[GetLocationVoicemailGroupObjectFaxMessage] = None
    #: Transfer message information
    transferToNumber: Optional[GetLocationVoicemailGroupObjectNotifications] = None
    #: Message copy information
    emailCopyOfMessage: Optional[GetLocationVoicemailGroupObjectEmailCopyOfMessage] = None


class PutVoicePortalObjectPasscode(ApiModel):
    #: New passcode.
    #: example: testPass123
    newPasscode: Optional[str] = None
    #: Confirm new passcode.
    #: example: testPass123
    confirmPasscode: Optional[str] = None


class PutVoicePortalObject(ApiModel):
    #: Voice Portal Name.
    #: example: test voicePortal
    name: Optional[str] = None
    #: Language code for voicemail group audio announcement.
    #: example: en_us
    languageCode: Optional[str] = None
    #: Extension of incoming call.
    #: example: 0007
    extension: Optional[datetime] = None
    #: Phone Number of incoming call.
    #: example: +1345325235
    phoneNumber: Optional[str] = None
    #: Caller ID First Name.
    #: example: firstName
    firstName: Optional[str] = None
    #: Caller ID Last Name.
    #: example: lastName
    lastName: Optional[str] = None
    #: Voice Portal Admin Passcode.
    passcode: Optional[PutVoicePortalObjectPasscode] = None
