import json

from tests.base import TestCaseWithLog


class TestMsTeams(TestCaseWithLog):
    def test_read(self):
        """
        read org level ms teams settings
        """
        settings = self.api.telephony.ms_teams.read()
        print(settings)
        print(json.dumps(settings.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
