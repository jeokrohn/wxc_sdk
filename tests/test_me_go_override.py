"""
Test Personal Assistant settings for me APIs
"""

from tests.base import TestWithRandomUserApi
from wxc_sdk import WebexSimpleApi


class TestMeGoOverride(TestWithRandomUserApi):

    def test_get(self):
        """
        Test get Webex Go Override settings
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            me_go_settings = api.me.go_override.get()
        dnd_settings = self.api.person_settings.dnd.read(entity_id=user.person_id)
        self.assertEqual(me_go_settings, dnd_settings.webex_go_override_enabled)
        return
