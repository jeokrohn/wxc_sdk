"""
test organisation VM settings
"""
from wxc_sdk.telephony.organisation_vm import OrganisationVoicemailSettings
from tests.base import TestCaseWithLog


class TestOrgVM(TestCaseWithLog):
    def test_001_read(self):
        settings = self.api.telephony.organisation_voicemail.read()
        print(f'Got settings: {settings}')

    def test_002_update_expiry(self):
        ov = self.api.telephony.organisation_voicemail
        before = ov.read()
        try:
            expiry_enabled = not before.message_expiry_enabled
            settings = OrganisationVoicemailSettings(
                message_expiry_enabled=expiry_enabled,
                number_of_days_for_message_expiry=before.number_of_days_for_message_expiry)
            ov.update(settings=settings)
            after = ov.read()
            self.assertEqual(expiry_enabled, after.message_expiry_enabled)
            after.message_expiry_enabled = before.message_expiry_enabled
            self.assertEqual(before, after)
        finally:
            ov.update(settings=before)
            restored = ov.read()
            self.assertEqual(before, restored)
