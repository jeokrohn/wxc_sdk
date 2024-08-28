import json

from tests.base import TestCaseWithLog
from wxc_sdk.telephony import MoHTheme


class TestMoHConfig(TestCaseWithLog):
    def test_read(self):
        config = self.api.telephony.read_moh()
        print(json.dumps(config.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))

    def test_update(self):
        config = self.api.telephony.read_moh()
        updated_config = config.model_copy(deep=True)
        updated_config.default_org_moh = (MoHTheme.OPUS if config.default_org_moh == MoHTheme.LEGACY
                                          else MoHTheme.LEGACY)
        try:
            self.api.telephony.update_moh(updated_config)
            after = self.api.telephony.read_moh()
            self.assertEqual(after, updated_config)
        finally:
            self.api.telephony.update_moh(config)
            self.assertEqual(self.api.telephony.read_moh(), config)