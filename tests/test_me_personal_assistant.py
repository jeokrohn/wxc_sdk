"""
Test Personal Assistant settings for me APIs
"""
from contextlib import contextmanager
from random import choice

from tests.base import UserTokens, TestCaseWithUsers
from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import *


class TestMePersonalAssistant(UserTokens, TestCaseWithUsers):
    def random_user(self) -> Person:
        """
        Get a random user except admin
        """
        candidates = [user for user in self.users if not user.emails[0].startswith('admin')]
        return choice(candidates)

    @contextmanager
    def user_api(self, user: Person):
        """
        get user api and set HAR writer
        """
        tokens = self.get_user_tokens(user.person_id)
        with WebexSimpleApi(tokens=tokens) as api:
            self.har_writer.register_webex_api(api)
            yield api

    def test_get(self):
        """
        Test get personal assistant settings
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            me_pa_settings = api.me.personal_assistant.get()
        pa_settings = self.api.person_settings.personal_assistant.get(person_id=user.person_id)
        self.assertEqual(me_pa_settings, pa_settings)
        return

    def test_get_user_tokens(self):
        """
        Get user tokens
        """
        user = self.random_user()
        tokens = self.get_user_tokens(user.person_id)
        print(tokens)
        with WebexSimpleApi(tokens=tokens) as api:
            self.har_writer.register_webex_api(api)
            me = api.people.me()
            print(me.display_name)
            print(user.display_name)
        self.assertEqual(me.display_name, user.display_name)
        return
