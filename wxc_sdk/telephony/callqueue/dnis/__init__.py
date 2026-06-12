import builtins
from collections.abc import Generator
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.common import (
    AudioSource,
    ComfortMessageBypass,
    ComfortMessageSetting,
    MohMessageSetting,
    RingPattern,
    WaitMessageSetting,
    WelcomeMessageSetting,
)
from wxc_sdk.person_settings.available_numbers import AvailableNumber

__all__ = ['CallQueueDnisApi', 'Dnis', 'DnisSettings', 'DnisAnnouncements']


class Dnis(ApiModel):
    #: Unique identifier for the DNIS.
    id: Optional[str] = None
    #: Name of the DNIS.
    name: Optional[str] = None
    #: Phone number of the DNIS.
    phone_number: Optional[str] = None
    #: Extension of the DNIS.
    extension: Optional[str] = None
    #: Routing prefix (location dialing code) of the DNIS.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Number (ESN) of the DNIS.
    esn: Optional[str] = None
    #: Ring pattern of the DNIS.
    ring_pattern: Optional[RingPattern] = None
    #: Use custom announcement settings for the DNIS. Enable custom announcement settings using Modify DNIS API. Modify
    #: custom announcement settings using Modify DNIS announcements API.
    custom_dnis_announcement_settings_enabled: Optional[bool] = None

    def update(self) -> dict[str, Any]:
        """
        Data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True, exclude={'routing_prefix', 'esn'})


class DnisSettings(ApiModel):
    #: Whether distinctive ringing is enabled for the queue.
    distinctive_ringing_enabled: Optional[bool] = None
    #: Whether the DNIS name and number is displayed to agents.
    display_dnis_name_and_number_enabled: Optional[bool] = None


class DnisAnnouncements(ApiModel):
    #: Whether custom DNIS announcement settings are enabled for this DNIS.
    custom_dnis_announcement_settings_enabled: Optional[bool] = None
    #: Welcome message settings.
    welcome_message: Optional[WelcomeMessageSetting] = None
    #: Comfort message settings.
    comfort_message: Optional[ComfortMessageSetting] = None
    #: Comfort message bypass settings.
    comfort_message_bypass: Optional[ComfortMessageBypass] = None
    #: Music on hold message settings.
    moh_message: Optional[MohMessageSetting] = None
    #: Wait message settings.
    wait_message: Optional[WaitMessageSetting] = None
    #: Whisper message settings.
    whisper_message: Optional[AudioSource] = None

    def update(self) -> dict[str, Any]:
        """
        Data for update

        :meta private:
        :return:
        """
        return self.model_dump(
            mode='json',
            by_alias=True,
            exclude_none=True,
            exclude={
                'welcome_message': {
                    'audio_playlist_id': True,
                    'audio_playlist_name': True,
                    'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                },
                'comfort_message': {
                    'audio_playlist_id': True,
                    'audio_playlist_name': True,
                    'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                },
                'comfort_message_bypass': {
                    'audio_playlist_id': True,
                    'audio_playlist_name': True,
                    'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                },
                'moh_message': {
                    'normal_source': {
                        'audio_playlist_name': True,
                        'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                    },
                    'alternate_source': {
                        'audio_playlist_name': True,
                        'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                    },
                },
                'wait_message': False,
                'whisper_message': {
                    'audio_playlist_id': True,
                    'audio_playlist_name': True,
                    'audio_announcement_files': {'__all__': {'file_size': True, 'is_text_to_speech': True}},
                },
            },
        )


class CallQueueDnisApi(ApiChild, base='telephony/config'):
    def available_phone_numbers(
        self, location_id: str, phone_number: str = None, org_id: str = None, **params: Any
    ) -> Generator[AvailableNumber, None, None]:
        """
        Get Available Phone Numbers for DNIS

        Get the list of available phone numbers that can be assigned to a DNIS for call queues at a location.

        Retrieving available numbers requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID.
        :type location_id: str
        :param phone_number: Filter by phone number.
        :type phone_number: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep(f'locations/{location_id}/queues/dnis/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def bulk_delete(self, location_id: str, queue_id: str, items: list[str], org_id: str = None) -> None:
        """
        Bulk Delete DNIS for a Call Queue

        Bulk delete a list of DNIS (Dialed Number Identification Service) entries for a call queue.

        A maximum of 99 DNIS entries can be deleted in a single request.

        Deleting DNIS entries requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param items: Array of DNIS IDs to be deleted.
        :type items: list[str]
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['items'] = items
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        super().delete(url, params=params, json=body)

    def list(self, location_id: str, queue_id: str, org_id: str = None) -> builtins.list[Dnis]:
        """
        Get List of DNIS for a Call Queue

        Get the list of DNIS (Dialed Number Identification Service) entries for a call queue.

        DNIS allows call queues to distinguish between primary and alternate numbers when delivering calls to agents.
        Each DNIS entry can have its own name, phone number, extension, ring pattern, and custom announcement
        settings.

        The maximum number of DNIS entries per call queue is 100.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: list[Dnis]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Dnis]).validate_python(data['dnisList'])
        return r

    def create(
        self,
        location_id: str,
        queue_id: str,
        name: str,
        ring_pattern: RingPattern,
        phone_number: str = None,
        extension: str = None,
        org_id: str = None,
    ) -> str:
        """
        Create a DNIS for a Call Queue

        Create a new DNIS (Dialed Number Identification Service) entry for a call queue.

        DNIS allows call queues to distinguish between primary and alternate numbers when delivering calls to agents.

        The maximum number of DNIS entries per call queue is 100. Either `phoneNumber` or `extension` is required.

        Creating a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param name: Name of the DNIS. Must be unique across the call queue.
        :type name: str
        :param ring_pattern: Ring pattern of the DNIS.
        :type ring_pattern: RingPattern
        :param phone_number: Phone number of the DNIS. Must be a valid phone number from the same location. Either
            phoneNumber or extension is required.
        :type phone_number: str
        :param extension: Extension of the DNIS. Either phoneNumber or extension is required.
        :type extension: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        body['ringPattern'] = enum_str(ring_pattern)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_settings(self, location_id: str, queue_id: str, org_id: str = None) -> DnisSettings:
        """
        Get DNIS Settings for a Call Queue

        Get DNIS (Dialed Number Identification Service) settings for a call queue.

        Retrieving DNIS settings requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`DnisSettings`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/settings')
        data = super().get(url, params=params)
        r = DnisSettings.model_validate(data)
        return r

    def modify_settings(self, location_id: str, queue_id: str, settings: DnisSettings, org_id: str = None) -> None:
        """
        Modify DNIS Settings for a Call Queue

        Modify DNIS (Dialed Number Identification Service) settings for a call queue.

        Modifying DNIS settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param settings: DNIS settings for this call queue.
        :type settings: :class:`DnisSettings`
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/settings')
        super().put(url, params=params, json=body)

    def delete(  # type: ignore[override]
        self,
        location_id: str,
        queue_id: str,
        dnis_id: str,
        org_id: str = None,
    ) -> None:
        """
        Delete a DNIS for a Call Queue

        Delete a DNIS (Dialed Number Identification Service) entry for a call queue.

        Deleting a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        super().delete(url, params=params)

    def details(self, location_id: str, queue_id: str, dnis_id: str, org_id: str = None) -> Dnis:
        """
        Get a DNIS for a Call Queue

        Get details of a specific DNIS (Dialed Number Identification Service) entry for a call queue.

        Retrieving DNIS details requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`Dnis`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        data = super().get(url, params=params)
        r = Dnis.model_validate(data)
        return r

    def modify(self, location_id: str, queue_id: str, dnis_id: str, settings: Dnis, org_id: str = None) -> None:
        """
        Modify a DNIS for a Call Queue

        Modify a DNIS (Dialed Number Identification Service) entry for a call queue.

        To remove a phone number or extension from the DNIS, set the field to `null`.

        Modifying a DNIS requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param settings: Settings for the DNIS.
        :type settings: :class:`Dnis`
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}')
        super().put(url, params=params, json=body)

    def get_announcements(self, location_id: str, queue_id: str, dnis_id: str, org_id: str = None) -> DnisAnnouncements:
        """
        Get DNIS Announcements for a Call Queue

        Get the announcement settings for a specific DNIS (Dialed Number Identification Service) entry in a call queue.

        This includes welcome message, comfort message, music on hold, wait message, and whisper message settings.

        Retrieving DNIS announcements requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: :class:`DnisAnnouncements`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}/announcements')
        data = super().get(url, params=params)
        r = DnisAnnouncements.model_validate(data)
        return r

    def modify_announcements(
        self, location_id: str, queue_id: str, dnis_id: str, settings: DnisAnnouncements, org_id: str = None
    ) -> None:
        """
        Modify DNIS Announcements for a Call Queue

        Modify the announcement settings for a specific DNIS (Dialed Number Identification Service) entry in a call
        queue.

        This includes welcome message, comfort message, music on hold, wait message, and whisper message settings.

        Modifying DNIS announcements requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: The location ID where the call queue exists.
        :type location_id: str
        :param queue_id: The call queue ID.
        :type queue_id: str
        :param dnis_id: The DNIS ID.
        :type dnis_id: str
        :param settings: Announcement settings for the DNIS.
        :type settings: :class:`DnisAnnouncements`
        :param org_id: The organization ID of the customer.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/dnis/{dnis_id}/announcements')
        super().put(url, params=params, json=body)
