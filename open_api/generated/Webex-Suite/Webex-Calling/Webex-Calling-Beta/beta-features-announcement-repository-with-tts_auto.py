import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnnouncementResponse', 'AnnouncementResponseWithPlaylist', 'AnnouncementsListResponse',
           'AnnouncementsListResponseLevel', 'BetaFeaturesAnnouncementRepositoryWithTTSApi', 'FeatureReferenceObject',
           'LocationId', 'LocationObject', 'TtsStatusResponse', 'TtsStatusResponseStatus', 'TtsUsageResponse',
           'TtsVoice']


class FeatureReferenceObject(ApiModel):
    #: Unique identifier of the call feature referenced. The call Feature can be Auto Attendant, Call Queue or Music On
    #: hold.
    id: Optional[str] = None
    #: Name of the call feature referenced.
    name: Optional[str] = None
    #: Resource Type of the call feature.
    type: Optional[str] = None
    #: Unique identifier of the location.
    location_id: Optional[str] = None
    #: Location name of the announcement file.
    location_name: Optional[str] = None


class AnnouncementResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str] = None
    #: Name of the announcement.
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime] = None
    #: Reference count of the call features this announcement is assigned to.
    feature_reference_count: Optional[int] = None
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]] = None
    #: Indicates whether the announcement is text-to-speech.
    is_text_to_speech: Optional[bool] = None
    #: Voice used for text-to-speech announcement.
    voice: Optional[str] = None
    #: Language code for text-to-speech announcement.
    language: Optional[str] = None
    #: Text content for text-to-speech announcement.
    text: Optional[str] = None


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    id: Optional[str] = None
    #: Name of the Location.
    name: Optional[str] = None


class AnnouncementResponseWithPlaylist(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str] = None
    #: Name of the announcement.
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime] = None
    #: Reference count of the call features this announcement is assigned to.
    feature_reference_count: Optional[int] = None
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]] = None
    #: List of playlist available for selection.
    playlists: Optional[list[LocationObject]] = None
    #: Indicates whether the announcement is text-to-speech.
    is_text_to_speech: Optional[bool] = None
    #: Voice used for text-to-speech announcement.
    voice: Optional[str] = None
    #: Language code for text-to-speech announcement.
    language: Optional[str] = None
    #: Text content for text-to-speech announcement.
    text: Optional[str] = None


class AnnouncementsListResponseLevel(str, Enum):
    location = 'LOCATION'
    organization = 'ORGANIZATION'


class AnnouncementsListResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str] = None
    #: Name of the announcement.
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    media_file_type: Optional[str] = None
    #: LastUpdated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime] = None
    #: The level at which this announcement exists.
    level: Optional[AnnouncementsListResponseLevel] = None
    #: The details of location at which this announcement exists.
    location: Optional[LocationObject] = None
    #: Indicates whether the announcement is text-to-speech.
    is_text_to_speech: Optional[bool] = None


class TtsUsageResponse(ApiModel):
    #: The number of text-to-speech API calls made in the current time window.
    no_of_api_calls: Optional[int] = None
    #: The maximum number of text-to-speech API calls allowed in the current time window.
    max_allowed_api_calls: Optional[int] = None
    #: The timestamp when the usage counter will reset. It will be returned when reaching the maximum allowed API calls
    #: in the time window.
    usage_reset_timestamp: Optional[datetime] = None


class TtsStatusResponseStatus(str, Enum):
    in_progress = 'IN_PROGRESS'
    success = 'SUCCESS'
    failure = 'FAILURE'


class TtsStatusResponse(ApiModel):
    #: Unique identifier of the text-to-speech generation request.
    id: Optional[str] = None
    #: The voice ID used to generate the audio prompt.
    voice: Optional[str] = None
    #: The input text used to generate the audio prompt.
    text: Optional[str] = None
    #: The language code used to generate the audio prompt.
    language_code: Optional[str] = None
    #: The status of the text-to-speech generation request.
    status: Optional[TtsStatusResponseStatus] = None
    #: A URL to download the encrypted audio prompt. Only available when status is `SUCCESS`.
    prompt_url: Optional[str] = None
    #: The KMS key URI required to decrypt the prompt downloaded from `promptUrl`. Only available when status is
    #: `SUCCESS`.
    kms_key_uri: Optional[str] = None
    #: A file URI you can use when configuring an announcement. Only available when status is `SUCCESS`.
    file_uri: Optional[str] = None
    #: A detailed message describing why generation failed. Only present when status is `FAILURE`.
    error_message: Optional[str] = None


class TtsVoice(ApiModel):
    #: The voice ID used to generate the audio prompt.
    id: Optional[str] = None
    #: The voice label, including the voice name and gender.
    label: Optional[str] = None


class LocationId(str, Enum):
    all = 'all'
    locations = 'locations'
    y2lz_y29zc_gfyazov_l3_vz_l0x_pq0_fusu9_olz_mx_mtyx = 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx'


class BetaFeaturesAnnouncementRepositoryWithTTSApi(ApiChild, base='telephony/config'):
    """
    Beta Features: Announcement Repository with TTS
    
    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator or location administrator
    auth token with a scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list_announcements(self, location_id: LocationId = None, order: str = None, file_name: str = None,
                           file_type: str = None, media_file_type: str = None, name: str = None, org_id: str = None,
                           **params: Any) -> Generator[AnnouncementsListResponse, None, None]:
        """
        List Announcements

        Fetch a list of binary announcement greetings at an organization as well as location level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned.
        :type location_id: LocationId
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str
        :param org_id: Get announcements in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AnnouncementsListResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = enum_str(location_id)
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return self.session.follow_pagination(url=url, model=AnnouncementsListResponse, item_key='announcements', params=params)

    def upload_organization_announcement(self, name: str, file_uri: str, file_name: str, is_text_to_speech: bool,
                                         org_id: str = None) -> str:
        """
        Upload Organization Announcement

        Upload a binary file to the announcement repository at an organization level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        Your request will need to be a JSON request with `application/json` Content-Type, including the announcement
        name, file URI, file name, and text-to-speech flag.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write` .

        :param name: Name of the announcement.
        :type name: str
        :param file_uri: URI of the announcement file.
        :type file_uri: str
        :param file_name: File name of the announcement.
        :type file_name: str
        :param is_text_to_speech: Indicates whether the announcement is text-to-speech.
        :type is_text_to_speech: bool
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['fileUri'] = file_uri
        body['fileName'] = file_name
        body['isTextToSpeech'] = is_text_to_speech
        url = self.ep('announcements')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_organization_announcement_detail(self, announcement_id: str,
                                             org_id: str = None) -> AnnouncementResponseWithPlaylist:
        """
        Get Organization Announcement Detail

        Fetch details of a binary announcement greeting by its ID at an organization level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Get an announcement in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementResponseWithPlaylist`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        data = super().get(url, params=params)
        r = AnnouncementResponseWithPlaylist.model_validate(data)
        return r

    def modify_organization_announcement(self, announcement_id: str, name: str, file_uri: str, file_name: str,
                                         is_text_to_speech: bool, org_id: str = None) -> None:
        """
        Modify Organization Announcement

        Modify an existing announcement greeting at a organization level.

        An admin can upload a file or modify an existing file at an organization level. This file will be uploaded to
        the announcement repository.

        Your request will need to be a JSON request with `application/json` Content-Type, including the announcement
        name, file URI, file name, and text-to-speech flag.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param name: Name of the announcement.
        :type name: str
        :param file_uri: URI of the announcement file.
        :type file_uri: str
        :param file_name: File name of the announcement.
        :type file_name: str
        :param is_text_to_speech: Indicates whether the announcement is text-to-speech.
        :type is_text_to_speech: bool
        :param org_id: Modify an announcement in this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['fileUri'] = file_uri
        body['fileName'] = file_name
        body['isTextToSpeech'] = is_text_to_speech
        url = self.ep(f'announcements/{announcement_id}')
        super().put(url, params=params, json=body)

    def upload_location_announcement(self, location_id: str, name: str, file_uri: str, file_name: str,
                                     is_text_to_speech: bool, org_id: str = None) -> str:
        """
        Upload Location Announcement

        Upload a binary file to the announcement repository at a location level.

        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.

        Your request will need to be a JSON request with `application/json` Content-Type, including the announcement
        name, file URI, file name, and text-to-speech flag.

        This API requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` .

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param name: Name of the announcement.
        :type name: str
        :param file_uri: URI of the announcement file.
        :type file_uri: str
        :param file_name: File name of the announcement.
        :type file_name: str
        :param is_text_to_speech: Indicates whether the announcement is text-to-speech.
        :type is_text_to_speech: bool
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['name'] = name
        body['fileUri'] = file_uri
        body['fileName'] = file_name
        body['isTextToSpeech'] = is_text_to_speech
        url = self.ep(f'locations/{location_id}/announcements')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_location_announcement_detail(self, location_id: str, announcement_id: str,
                                         org_id: str = None) -> AnnouncementResponse:
        """
        Get Location Announcement Detail

        Fetch details of a binary announcement greeting by its ID at a location level.

        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Fetch an announcement for location in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = super().get(url, params=params)
        r = AnnouncementResponse.model_validate(data)
        return r

    def modify_location_announcement(self, location_id: str, announcement_id: str, org_id: str = None) -> None:
        """
        Modify Location Announcement

        Modify an existing announcement greeting at a location level.

        An admin can upload a file or modify an existing file at a location level. This file will be uploaded to the
        announcement repository.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Modify an announcement for location in this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().put(url, params=params)

    def generate_text_to_speech(self, voice: str, text: str, language_code: str, org_id: str = None) -> str:
        """
        Generate a Text-to-Speech Prompt

        Generate a text-to-speech prompt from the provided text, voice, and language.

        Text-to-speech (TTS) efficiently generates prompts, greetings, and announcements by converting written text
        into synthesized audio using the specified voice. The generated audio functions like a recorded WAV file,
        eliminating the need for manual recording.

        This API requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param voice: The voice ID used to generate the audio prompt. Use the List Text-to-Speech Voices API to
            retrieve available voices.
        :type voice: str
        :param text: The text to convert to speech.
        :type text: str
        :param language_code: The language code used to generate the audio prompt. Use the Read the List of
            Announcement Languages API to retrieve supported language codes.
        :type language_code: str
        :param org_id: Generate text-to-speech for this organization.
        :type org_id: str
        :rtype: str
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['voice'] = voice
        body['text'] = text
        body['languageCode'] = language_code
        url = self.ep('textToSpeech/actions/generate/invoke')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_text_to_speech_usage(self, org_id: str = None) -> TtsUsageResponse:
        """
        Get Text-to-Speech Usage

        Retrieve text-to-speech usage information, including the number of API calls made, the maximum allowed within
        the time window, and the timestamp indicating when the usage will reset.

        Text-to-speech (TTS) efficiently generates prompts, greetings, and announcements by converting written text
        into synthesized audio using the specified voice. The generated audio functions like a recorded WAV file,
        eliminating the need for manual recording.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Get text-to-speech usage for this organization.
        :type org_id: str
        :rtype: :class:`TtsUsageResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('textToSpeech/usage')
        data = super().get(url, params=params)
        r = TtsUsageResponse.model_validate(data)
        return r

    def list_text_to_speech_voices(self, org_id: str = None) -> builtins.list[TtsVoice]:
        """
        List Text-to-Speech Voices

        Fetch a list of available text-to-speech voices. Use the returned voice ID in the generation request.

        Text-to-speech (TTS) efficiently generates prompts, greetings, and announcements by converting written text
        into synthesized audio using the specified voice. The generated audio functions like a recorded WAV file,
        eliminating the need for manual recording.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: List text-to-speech voices supported for this organization.
        :type org_id: str
        :rtype: list[TtsVoice]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('textToSpeech/voices')
        data = super().get(url, params=params)
        r = TypeAdapter(list[TtsVoice]).validate_python(data['voices'])
        return r

    def get_text_to_speech_generation_status(self, tts_id: str, org_id: str = None) -> TtsStatusResponse:
        """
        Get Text-to-Speech Generation Status

        Get the status of a text-to-speech generation request by its ID. If the status is SUCCESS, the response
        includes `promptUrl`, `kmsKeyUri`, and `fileUri` to preview or use the audio prompt.

        To preview the audio prompt:

        1. Download the KMS key - use the Webex Node.js SDK and provide `kmsKeyUri` to download the key from KMS.

        2. Download the encrypted audio - The encrypted audio file content is stored in cloud and can be retrieved
        using `promptURL`.

        3. Decrypt the audio content - Use the jose library to decrypt the content downloaded from `promptUrl` using
        the downloaded key.

        Text-to-speech (TTS) efficiently generates prompts, greetings, and announcements by converting written text
        into synthesized audio using the specified voice. The generated audio functions like a recorded WAV file,
        eliminating the need for manual recording.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param tts_id: Unique identifier of the text-to-speech generation request.
        :type tts_id: str
        :param org_id: Get text-to-speech status for this organization.
        :type org_id: str
        :rtype: :class:`TtsStatusResponse`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'textToSpeech/{tts_id}')
        data = super().get(url, params=params)
        r = TtsStatusResponse.model_validate(data)
        return r
