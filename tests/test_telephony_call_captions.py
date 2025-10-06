"""
test org level telephony call captions settings
"""
import json

from tests.base import TestCaseWithLog


class TestCallCaptions(TestCaseWithLog):
    """
    test org level telephony call captions settings
    """
    proxy = True

    def test_get_call_captions_settings(self):
        """
        test get call captions settings
        """
        settings = self.api.telephony.get_call_captions_settings()
        print(json.dumps(settings.model_dump(mode='json', by_alias=True), indent=2))

    def test_update_call_captions_settings(self):
        """
        test update call captions settings
        """
        before = self.api.telephony.get_call_captions_settings()
        try:
            update = before.model_copy(deep=True)
            update.org_closed_captions_enabled = not before.org_closed_captions_enabled
            self.api.telephony.update_call_captions_settings(update)
            after = self.api.telephony.get_call_captions_settings()
            self.assertEqual(update, after)
        finally:
            self.api.telephony.update_call_captions_settings(before)
            restored = self.api.telephony.get_call_captions_settings()
            self.assertEqual(before, restored)
