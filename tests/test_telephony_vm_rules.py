"""
Tests for organisation voicemail rules
"""

import json

from wxc_sdk.telephony.vm_rules import VoiceMailRules, BlockPreviousPasscodes
from tests.base import TestCaseWithLog


class TestRules(TestCaseWithLog):
    def test_001_read(self):
        vmr = self.api.telephony.voicemail_rules
        settings = vmr.read()
        print(f'Got VM rules')
        print(json.dumps(json.loads(settings.model_dump_json()), indent=2))

    def test_002_update(self):
        vmr = self.api.telephony.voicemail_rules
        before = vmr.read()
        try:
            settings = VoiceMailRules(block_previous_passcodes=BlockPreviousPasscodes(number_of_passcodes=1))
            vmr.update(settings=settings)
            after = vmr.read()
            self.assertEqual(1, after.block_previous_passcodes.number_of_passcodes)
        finally:
            vmr.update(settings=before)
            restored = vmr.read()
            self.assertEqual(before, restored)
