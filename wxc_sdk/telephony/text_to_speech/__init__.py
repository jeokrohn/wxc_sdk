import builtins
from datetime import datetime
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['TtsUsageResponse', 'TtsStatusResponse', 'TtsVoice', 'TextToSpeechApi']


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


class TextToSpeechApi(ApiChild, base='telephony/config'):
    def generate(self, voice: str, text: str, language_code: str, org_id: str = None) -> str:
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

    def usage(self, org_id: str = None) -> TtsUsageResponse:
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

    def voices(self, org_id: str = None) -> builtins.list[TtsVoice]:
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

    def status(self, tts_id: str, org_id: str = None) -> TtsStatusResponse:
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
