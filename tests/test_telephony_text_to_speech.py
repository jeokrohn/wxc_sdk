import json
from time import sleep

from pydantic import TypeAdapter

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
        return
