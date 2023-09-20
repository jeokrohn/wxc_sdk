from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetLocationVoicemailGroupObject', 'GetLocationVoicemailGroupObjectEmailCopyOfMessage', 'GetLocationVoicemailGroupObjectFaxMessage', 'GetLocationVoicemailGroupObjectGreeting', 'GetLocationVoicemailGroupObjectMessageStorage', 'GetLocationVoicemailGroupObjectMessageStorageStorageType', 'GetLocationVoicemailGroupObjectNotifications', 'GetVoicemailGroupObject']


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
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 123423455
    esn: Optional[str] = None
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
    #: Routing prefix of location.
    #: example: 1234
    routingPrefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12340007
    esn: Optional[str] = None
    #: Phone number of the voicemail group.
    #: example: +1345325235
    phoneNumber: Optional[str] = None
    #: If enabled, incoming calls are sent to voicemail.
    #: example: True
    enabled: Optional[bool] = None
    #: Flag to indicate if the number is toll free.
    #: example: True
    tollFreeNumber: Optional[bool] = None
