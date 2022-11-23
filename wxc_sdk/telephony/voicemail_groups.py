"""
Voicemail groups API
"""
from collections.abc import Generator
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import to_camel, ApiModel
from ..common import Greeting, VoicemailMessageStorage, VoicemailNotifications, VoicemailFax, \
    VoicemailTransferToNumber, \
    VoicemailCopyOfMessage, StorageType

__all__ = ['VoicemailGroup', 'VoicemailGroupDetail', 'VoicemailGroupsApi']


class VoicemailGroup(ApiModel):
    #: Voicemail Group ID.
    group_id: str = Field(alias='id')
    #: Voicemail Group Name.
    name: str
    #: Location Name.
    location_name: str
    #: location id
    location_id: str
    #: Extension of the voicemail group.
    extension: Optional[str]
    #: Phone number of the voicemail group.
    phone_number: Optional[str]
    #: If enabled, incoming calls are sent to voicemail.
    enabled: bool
    #: Flag to indicate if the number is toll free.
    toll_free_number: bool = Field(default=False)


class VoicemailGroupDetail(ApiModel):
    #: UUID of voicemail group of a particular location.
    group_id: Optional[str] = Field(alias='id')
    #: Name of the voicemail group.
    name: Optional[str]
    #: Voicemail group phone number.
    phone_number: Optional[str]
    #: Voicemail group extension number.
    extension: Optional[str]
    #: Voicemail group toll free number.
    toll_free_number: Optional[bool]
    #: Voicemail group caller id first name.
    first_name: Optional[str]
    #: Voicemail group called id last name.
    last_name: Optional[str]
    #: passcode
    passcode: Optional[int]
    #: Enable/disable voicemail group.
    enabled: Optional[bool]
    #: Language for voicemail group audio announcement.
    language_code: Optional[str]
    #: Set voicemail group greeting typ
    greeting: Optional[Greeting]
    #: Enabled if CUSTOM greeting is previously uploaded.
    greeting_uploaded: Optional[bool]
    #: CUSTOM greeting for previously uploaded.
    greeting_description: Optional[str]
    #: Message storage information
    message_storage: Optional[VoicemailMessageStorage]
    #: Message notifications
    notifications: Optional[VoicemailNotifications]
    #: Fax message receive settings
    fax_message: Optional[VoicemailFax]
    #: Transfer message information
    transfer_to_number: Optional[VoicemailTransferToNumber]
    #: Message copy information
    email_copy_of_message: Optional[VoicemailCopyOfMessage]
    #: Enable/disable to forward voice message.
    voice_message_forwarding_enabled: Optional[bool]

    @staticmethod
    def create(name: str, extension: str, first_name: str, last_name: str, passcode: int, language_code: str = 'en_us',
               phone_number: str = None) -> 'VoicemailGroupDetail':
        """
        VoiceMailGroupDetail for create() call

        :param name: Name of the voicemail group.
        :param extension: Voicemail group extension number.
        :param first_name: Voicemail group caller id first name.
        :param last_name: Voicemail group called id last name.
        :param passcode: passcode
        :param language_code: Language for voicemail group audio announcement.
        :param phone_number: Voicemail group phone number.
        :return: Voicemail group details which can be used in :meth:`VoicemailGroupsApi.create`
        :rtype: :class:`VoicemailGroupDetail`
        """
        return VoicemailGroupDetail(name=name, phone_number=phone_number, extension=extension, first_name=first_name,
                                    last_name=last_name, passcode=passcode, language_code=language_code,
                                    message_storage=VoicemailMessageStorage(storage_type=StorageType.internal),
                                    notifications=VoicemailNotifications(enabled=False),
                                    fax_message=VoicemailFax(enabled=False),
                                    transfer_to_number=VoicemailTransferToNumber(enabled=False),
                                    email_copy_of_message=VoicemailCopyOfMessage(enabled=False))

    def json_for_create(self) -> str:
        return self.json(exclude_none=True,
                         include={'name', 'phone_number', 'extension', 'first_name', 'last_name', 'passcode',
                                  'language_code', 'message_storage', 'notifications', 'fax_message',
                                  'transfer_to_number', 'email_copy_of_message'})

    def json_for_update(self) -> str:
        return self.json(exclude_none=True,
                         include={'name', 'phone_number', 'extension', 'first_name', 'last_name', 'enabled', 'passcode',
                                  'language_code', 'greeting', 'greeting_description', 'message_storage',
                                  'notifications', 'fax_message',
                                  'transfer_to_number', 'email_copy_of_message'})


class VoicemailGroupsApi(ApiChild, base='telephony/config/voicemailGroups'):
    """
    API for voicemail groups
    """

    def ep(self, location_id: str = None, path: str = None):
        """
        :param location_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        if location_id is None:
            return super().ep(path)
        return self.session.ep(f'telephony/config/locations/{location_id}/voicemailGroups{path}')

    def list(self, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> Generator[VoicemailGroup, None, None]:
        """
        List the voicemail group information for the organization.

        You can create a shared voicemail box and inbound fax box to assign to users or call routing features like an
        auto attendant, call queue, or hunt group.

        Retrieving voicemail Group for the organization requires a full read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :return: yields ::class::`VoicemailGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items() if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoicemailGroup, params=params, item_key='voicemailGroups')

    def details(self, location_id: str, voicemail_group_id: str, org_id: str = None) -> VoicemailGroupDetail:
        """
        Retrieve voicemail group details for a location.

        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active,
        message storage settings, and how you would like to be notified of new voicemail messages.

        Retrieving voicemail group details requires a full, user or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str
        :return: Voicemail group settings
        :type: :class:`VoicemailGroupDetail`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id, voicemail_group_id)
        data = self.get(url=url, params=params)
        return VoicemailGroupDetail.parse_obj(data)

    def update(self, location_id: str, voicemail_group_id: str, settings: VoicemailGroupDetail, org_id: str = None):
        """
        Modifies the voicemail group location details for a particular location for a customer.

        Manage your voicemail settings, like when you want your voicemail to be active, message storage settings, and
        how you would like to be notified of new voicemail messages.

        Modifying the voicemail group location details requires a full, user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Modifies the voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Modifies the voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param settings: New settings
        :type settings: :class:`VoicemailGroupDetail`
        :param org_id: Modifies the voicemail group details for a customer location.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id, voicemail_group_id)
        body = settings.json_for_update()
        self.put(url=url, data=body, params=params)

    def create(self, location_id: str, settings: VoicemailGroupDetail, org_id: str = None) -> str:
        """
        Create new voicemail group for the given location for a customer.

        Voicemail group can be created for given location for a customer.

        Creating voicemail group for the given location requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create new voice mail group for this location.
        :type location_id: str
        :param settings: settings for new voicemail group
            Example:

            .. code-block:: python

                settings = VoicemailGroupDetail.create(
                                        name=vmg_name, extension=extension,
                                        first_name='first', last_name='last',
                                        passcode=740384)
                vmg_id = api.telephony.voicemail_groups.create(location_id=location_id,
                                                               settings=settings)

        :type settings: :class:`VoicemailGroupDetail`
        :param org_id: Create new voice mail group for this organization.
        :type org_id: str
        :return: UUID of the newly created voice mail group.
        :rtype: str
        """
        body = settings.json_for_create()
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)
        data = self.post(url=url, data=body, params=params)
        return data['id']

    def delete(self, location_id: str, voicemail_group_id: str, org_id: str = None):
        """
        Delete the designated voicemail group.

        Deleting a voicemail group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a voicemail group.
        :type location_id: str
        :param voicemail_group_id: Delete the voicemail group with the matching ID.
        :type voicemail_group_id: str
        :param org_id: Delete the voicemail group from this organization.
        :type org_id: str
        """
        url = self.ep(location_id, voicemail_group_id)
        super().delete(url=url)
