import asyncio
import json
import os.path
import random
from typing import List, Tuple, Union

from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError


class TestMeVoicemail(TestWithRandomUserApi):
    # proxy = True

    @async_test
    async def test_get_settings(self):
        """
        Get voicemail settings for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.voicemail.settings()
                    except AsRestError as e:
                        raise e
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error voicemail settings for {user.display_name}: {result}")
            elif result is not None:
                result: VoicemailSettings
                print(f"voicemail settings for {user.display_name}: ")

                print(json.dumps(result.model_dump(mode='json', exclude_unset=True,
                                                   exclude_none=True),
                                 indent=2))
        if err:
            raise err

    @async_test
    async def test_upload_busy_greeting(self):
        """
        upload busy greeting for a random user
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.voicemail.settings()
                    except AsRestError as e:
                        raise e
            return

        # get settings for all users
        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        settings = await asyncio.gather(*[get_settings(user)
                                          for user in users])
        settings: List[VoicemailSettings]

        # pick a random user
        users_and_settings = list(zip(users, settings))
        user, setting = random.choice(users_and_settings)
        user: Person
        setting: VoicemailSettings

        print(f'Test upload busy greeting for {user.display_name}')
        with self.user_api(user) as api:
            vm_api = api.me.voicemail
            before = vm_api.settings()
            try:
                wav_path = os.path.join(os.path.dirname(__file__), 'sample.wav')
                with open(wav_path, 'rb') as f:
                    vm_api.upload_busy_greeting(content=f, upload_as='sample.wav')
                new_settings = VoicemailSettings(
                    send_busy_calls=VoicemailEnabledWithGreeting(enabled=True, greeting=Greeting.custom))
                vm_api.configure(new_settings)
                after = vm_api.settings()
                print(f'Before:')
                print(json.dumps(before.model_dump(mode='json', exclude_none=True, by_alias=True),
                                 indent=2))
                print(f'After:')
                print(json.dumps(after.model_dump(mode='json', exclude_none=True, by_alias=True),
                                 indent=2))
                self.assertTrue(after.send_busy_calls.greeting_uploaded)
                self.assertTrue(after.send_busy_calls.greeting == Greeting.custom)
                self.assertEqual(after.send_busy_calls.audio_file.media_type, 'WAV')
                self.assertTrue(after.send_busy_calls.enabled)
            finally:
                vm_api.configure(before)

    @async_test
    async def test_upload_busy_greeting_async(self):
        """
        upload busy greeting for a random user
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.voicemail.settings()
                    except AsRestError as e:
                        raise e
            return

        # get settings for all users
        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        settings = await asyncio.gather(*[get_settings(user)
                                          for user in users])
        settings: List[VoicemailSettings]

        # pick a random user
        users_and_settings = list(zip(users, settings))
        user, setting = random.choice(users_and_settings)
        user: Person
        setting: VoicemailSettings

        print(f'Test upload busy greeting for {user.display_name}')
        with self.user_api(user) as api:
            vm_api = api.me.voicemail
            before = vm_api.settings()
            try:
                wav_path = os.path.join(os.path.dirname(__file__), 'sample.wav')
                async with AsWebexSimpleApi(tokens=api.access_token) as as_api:
                    with open(wav_path, 'rb') as f:
                        await as_api.me.voicemail.upload_busy_greeting(content=f, upload_as='sample.wav')
                new_settings = VoicemailSettings(
                    send_busy_calls=VoicemailEnabledWithGreeting(enabled=True, greeting=Greeting.custom))
                vm_api.configure(new_settings)
                after = vm_api.settings()
                print(f'Before:')
                print(json.dumps(before.model_dump(mode='json', exclude_none=True, by_alias=True),
                                 indent=2))
                print(f'After:')
                print(json.dumps(after.model_dump(mode='json', exclude_none=True, by_alias=True),
                                 indent=2))
                self.assertTrue(after.send_busy_calls.greeting_uploaded)
                self.assertTrue(after.send_busy_calls.greeting == Greeting.custom)
                self.assertEqual(after.send_busy_calls.audio_file.media_type, 'WAV')
                self.assertTrue(after.send_busy_calls.enabled)
            finally:
                vm_api.configure(before)