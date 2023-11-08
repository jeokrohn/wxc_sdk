from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetLocationVoicemailGroupObject', 'GetLocationVoicemailGroupObjectEmailCopyOfMessage',
            'GetLocationVoicemailGroupObjectFaxMessage', 'GetLocationVoicemailGroupObjectGreeting',
            'GetLocationVoicemailGroupObjectMessageStorage',
            'GetLocationVoicemailGroupObjectMessageStorageStorageType',
            'GetLocationVoicemailGroupObjectNotifications', 'GetVoicemailGroupObject', 'ListVoicemailGroupResponse']


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
    #: example: 23455.0
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
    #: example: 23455.0
    extension: Optional[int] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
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
    #: example: 0007
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
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


class ListVoicemailGroupResponse(ApiModel):
    #: Array of VoicemailGroups.
    voicemail_groups: Optional[list[GetVoicemailGroupObject]] = None


class BetaLocationCallSettingsVoicemailWithESNFeatureApi(ApiChild, base='telephony/config'):
    """
    Beta Location Call Settings:  Voicemail with ESN Feature
    
    Location Call Settings: Voicemail supports reading and writing of Webex
    Calling Location Voicemail settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list_voicemail_group(self, location_id: str = None, org_id: str = None, max_: int = None, start: int = None,
                             name: str = None, phone_number: str = None,
                             **params) -> Generator[GetVoicemailGroupObject, None, None]:
        """
        List VoicemailGroup

        List the voicemail group information for the organization.
        
        You can create a shared voicemail box and inbound FAX box to
        assign to users or call routing features like an auto attendant, call queue, or hunt group.
        
        Retrieving a voicemail group for the organization requires a full read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :param max_: Limit the maximum number of events in the response. The maximum value is `200`.
        :type max_: int
        :param start: Offset from the first result that you want to fetch.
        :type start: int
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
        :return: Generator yielding :class:`GetVoicemailGroupObject` instances
        """
        ...


    def get_location_voicemail_group(self, location_id: str, voicemail_group_id: str,
                                     org_id: str = None) -> GetLocationVoicemailGroupObject:
        """
        Get Location Voicemail Group

        Retrieve voicemail group details for a location.
        
        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active,
        message storage settings, and how you would like to be notified of new voicemail messages.
        
        Retrieving voicemail group details requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str
        :rtype: :class:`GetLocationVoicemailGroupObject`
        """
        ...

    ...