import asyncio
import functools
import json
import random
from collections import defaultdict
from itertools import chain
from operator import attrgetter

from pydantic import TypeAdapter

from tests.base import TestWithLocations, async_test
from tests.testutil import available_extensions_gen
from wxc_sdk.all_types import *
from wxc_sdk.rest import RestError


class TestAiReceptionists(TestWithLocations):
    proxy = True

    @async_test
    async def test_templates(self):
        """
        list templates and get details for all of them
        """
        api = self.async_api.telephony.ai_receptionists
        templates = await api.templates()
        template_details_list: list[AIRTemplate] = await asyncio.gather(
            *(api.get_template(template.id) for template in templates), return_exceptions=True
        )
        print('Template list:')
        print(json.dumps(TypeAdapter(list[IdAndName]).dump_python(templates, mode='json', by_alias=True), indent=2))
        print()
        print('Template details:')
        print(
            json.dumps(
                TypeAdapter(list[AIRTemplate]).dump_python(template_details_list, mode='json', by_alias=True), indent=2
            )
        )
        return

    @async_test
    async def test_knowledge_bases(self):
        """
        List knowledge bases and get details for all of them
        """
        api = self.async_api.telephony.ai_receptionists
        kb_list = await api.knowledge_bases()
        kb_details_list: list[KnowledgeBase] = await asyncio.gather(
            *(api.get_knowledge_base(kb.id) for kb in kb_list), return_exceptions=True
        )
        print('Knowledge base list:')
        print(json.dumps(TypeAdapter(list[KnowledgeBase]).dump_python(kb_list, mode='json', by_alias=True), indent=2))
        print()
        print('Knowledge base details:')
        print(
            json.dumps(
                TypeAdapter(list[KnowledgeBase]).dump_python(kb_details_list, mode='json', by_alias=True), indent=2
            )
        )
        return

    @async_test
    async def test_knowledge_base_docs(self):
        """
        List knowledge base documents for all knowledge bases
        """
        api = self.async_api.telephony.ai_receptionists
        kb_list = await api.knowledge_bases()
        kb_docs: list[KnowledgeBaseDocumentDetails] = list(
            chain.from_iterable(
                await asyncio.gather(
                    *(api.list_knowledge_base_documents(kb.id) for kb in kb_list), return_exceptions=False
                )
            )
        )
        kb_doc_details = await asyncio.gather(
            *(api.get_knowledge_base_document(kb_doc.knowledge_base_id, kb_doc.id) for kb_doc in kb_docs),
            return_exceptions=False,
        )
        content_list = await asyncio.gather(
            *(api.download_knowledge_base_document(kb_doc.knowledge_base_id, kb_doc.id) for kb_doc in kb_docs),
            return_exceptions=False,
        )

    def test_list(self):
        """
        list AI receptionists
        """
        api = self.api.telephony.ai_receptionists
        air_list = list(api.list())

    @async_test
    async def test_details(self):
        """
        get details of all AI receptionists
        """
        api = self.async_api.telephony.ai_receptionists
        air_list = await api.list()
        details_list = await asyncio.gather(
            *(api.details(air.location.id, air.id) for air in air_list), return_exceptions=True
        )
        for details in details_list:
            print(details)

    @async_test
    async def test_air_details_and_dependencies(self):
        """
        Get details of all AI receptionists and all dependencies
        """

        async def process_one_air(air: AiReceptionist):
            """
            process one AI receptionist
            """
            air_details = await api.details(air.location.id, air.id)
            foo = 1
            # get knowledge base
            # kb = await.api.kn
            # get intents

            ...

        api = self.async_api.telephony.ai_receptionists
        air_list = await api.list()
        await asyncio.gather(*(process_one_air(air) for air in air_list), return_exceptions=True)
        return

    @async_test
    async def test_list_intents(self):
        """
        list intents for all AI receptionists
        """
        api = self.async_api.telephony.ai_receptionists
        air_list = await api.list()
        intents_list = await asyncio.gather(
            *(api.intents(air.location.id, air.id) for air in air_list), return_exceptions=True
        )

    @async_test
    async def test_intent_details(self):
        """
        Get intent details for all AI receptionists
        """

        async def process_one_air(air: AiReceptionist):
            intents = await api.intents(air.location.id, air.id)
            intents: list[AIRIntent | Exception]

            async def get_intent_details(intent: AIRIntent | Exception) -> AIRIntent | Exception:
                if isinstance(intent, Exception):
                    return intent
                return await api.get_intent(air.location.id, air.id, intent.id)

            return await asyncio.gather(*(get_intent_details(i) for i in intents), return_exceptions=True)

        api = self.async_api.telephony.ai_receptionists
        air_list = await api.list()
        intent_details = await asyncio.gather(*(process_one_air(air) for air in air_list), return_exceptions=True)

    @async_test
    async def test_validate_country(self):
        """
        Validate countries for AI receptionists
        """
        import pycountry

        api = self.async_api.telephony.ai_receptionists
        countries = pycountry.countries
        country_codes = sorted(set(country.alpha_2 for country in countries))
        country_codes.append('ZZ')
        responses = await asyncio.gather(
            *(api.validate_country(country_code) for country_code in country_codes), return_exceptions=True
        )
        err = None
        for country_code, response in zip(country_codes, responses, strict=True):
            if isinstance(response, Exception):
                print(f'{country_code}: {response}')
                err = err or response
        if err:
            raise err
        return

    def test_air_validate_duplicate(self):
        """
        Validate duplicate AI receptionist
        """
        # get list of AIRs
        api = self.api.telephony.ai_receptionists
        air_list = list(api.list())
        # skip if none exists
        if not air_list:
            self.skipTest('No AI receptionists found')
        air: AiReceptionist = random.choice(air_list)
        # validate AIR with existing name; this is supposed to fail
        with self.assertRaises(RestError) as context:
            api.validate(location_id=air.location.id, name=air.name)
        error: RestError = context.exception
        self.assertEqual(409, error.response.status_code)
        self.assertEqual(25495, error.code)
        self.assertEqual('AI Receptionist name is already in use.', error.description)

    def test_voices(self):
        """
        Get and display all voices
        """

        def voice_name(voice: Voice) -> str:
            """
            Voice name w/o leading language code
            """
            if voice.display_name is None:
                return '-'
            dn = voice.display_name
            if dn.startswith(voice.language_code):
                dn = dn[len(voice.language_code) + 1 :]
            if voice.gender == VoiceGender.male:
                dn = f'{dn} (M)'
            else:
                dn = f'{dn} (F)'
            return dn

        api = self.api.telephony.ai_receptionists
        location: Location = random.choice(self.locations)
        engines = api.voices(location_id=location.location_id)
        for engine in engines:
            print(f'Engine: {engine.name} ({len(engine.voices)} voices)')
            voices_by_language: dict[str, list[Voice]] = functools.reduce(
                lambda acc, el: acc[el.language].append(el) or acc, engine.voices, defaultdict(list)
            )
            print(
                f'  Voices: '
                f'{", ".join(f"{l} ({len(voices_by_language[l])})" for l in sorted(voices_by_language.keys()))}'
            )
            for language in sorted(voices_by_language.keys()):
                print(f'  {language} ({len(voices_by_language[language])} voices)')
                lang_voices = voices_by_language[language]
                lang_voices.sort(key=attrgetter('display_name'))
                print(f'    {", ".join(voice_name(lv) for lv in lang_voices)}')
        return

    def available_air_name(self, location_id: str, prefix: str = None) -> str:
        """
        Get available AIR name in given location
        """
        prefix = prefix or 'AIR'
        for index in range(1, 1000):
            name = f'{prefix}_{index:03}'
            try:
                self.api.telephony.ai_receptionists.validate(location_id=location_id, name=name)
                return name
            except RestError as error:
                if error.code != 25495:
                    raise
        raise RuntimeError('No available AIR name found')

    def test_create_AIR(self):
        """
        Create an AIR receptionist
        """
        api = self.api.telephony.ai_receptionists
        # pick random location
        location: Location = random.choice(self.locations)
        print(f'Testing in location {location.name}')
        available_numbers = list(api.available_numbers(location.location_id))
        print(
            f'Available numbers ({len(available_numbers)}): '
            f'{", ".join(sorted(an.phone_number for an in available_numbers if an.phone_number))}'
        )
        new_extension = next(available_extensions_gen(api=self.api, location_id=location.location_id))
        print(f'Available extension: {new_extension}')

        # pick a name for the new AIR
        air_name = self.available_air_name(location_id=location.location_id)
        print(f'Available AIR name: {air_name}')

        voices = api.voices(location_id=location.location_id)
        print(f'Available voices ({len(voices)}): {", ".join(v.name for v in voices)}')

        # create a new AIR
        # we need
        #   * voice
        #   * knowledge base
        #   * guidelines
        # api.create(location_id=location.location_id,
        #            name=air_name,
        #            extension=new_extension,
        #            default_action=DefaultAction(action_type=DefaultActionType.play_message_and_disconnect,
        #                                         audio_message_selection=Greeting.default),
        #            ai_agent=AiAgent())

        foo = 1
