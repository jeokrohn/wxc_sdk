from random import choice

from tests.base import TestCaseWithLog


class TestPassword(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())

    def test_001(self):
        location = choice(self.locations)
        pwd = self.api.telephony.location.generate_password(location_id=location.location_id)
        print(pwd)
