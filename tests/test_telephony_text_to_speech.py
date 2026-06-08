import json
from pathlib import Path
from time import sleep

from jwcrypto.jwe import JWE
from pydantic import TypeAdapter
from webex_kms_sdk import ThreadedWebexClient

from tests.base import TestCaseWithLog
from wxc_sdk.telephony import AnnouncementLanguage
from wxc_sdk.telephony.text_to_speech import TtsVoice


class TestTTS(TestCaseWithLog):
    def test_usage(self):
        api = self.api.telephony.text_to_speech
        r = api.usage()
        print(json.dumps(r.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))

    def test_voices(self):
        api = self.api.telephony.text_to_speech
        voices = api.voices()
        print(json.dumps(TypeAdapter(list[TtsVoice]).dump_python(voices, mode='json', by_alias=True), indent=2))

    def test_languages(self):
        languages = self.api.telephony.read_list_of_announcement_languages()
        print(
            json.dumps(
                TypeAdapter(list[AnnouncementLanguage]).dump_python(languages, mode='json', by_alias=True), indent=2
            )
        )

    def test_generate(self):
        """
        Generate a TTS prompt, poll for completion, download the encrypted prompt, decrypt it, and write to a WAV file.
        """
        api = self.api.telephony.text_to_speech
        voices = api.voices()
        voice = voices[0].id
        usage = api.usage()
        print(f'Usage before: {usage}')
        tts_id = api.generate(
            voice=voice, language_code='en_us', text="Sorry, we can't take your call right now. Please try again later"
        )
        print(f'Usage after: {usage}')
        while True:
            status = api.status(tts_id)
            print(json.dumps(status.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))
            if status.status not in {'FAILURE', 'SUCCESS'}:
                sleep(2)
                continue
            break
        print(f'Usage after: {usage}')
        kms_uri = status.kms_key_uri
        prompt_url = status.prompt_url

        # download encrypted file (JWE token)
        with self.api.session.get(prompt_url, headers={'Authorization': f'Bearer {self.api.access_token}'}) as resp:
            resp.raise_for_status()
            prompt = resp.text

        # get encryption key from KMS
        with ThreadedWebexClient(self.api.access_token) as client:
            key = client.get_key(kms_uri)
        print(f'got encryption key: {key}')

        # deserialize and decrypt JWE token
        jwe = JWE()
        jose_key = key.jwk.jwcrypto_key()
        jwe.deserialize(prompt, jose_key)

        # write WAV file
        wav_path = Path(__file__).parent / 'prompt.wav'
        with open(wav_path, 'wb') as f:
            f.write(jwe.payload)
        print(f'Wrote prompt to: {wav_path}')
        return
