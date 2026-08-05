from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog
from wxc_sdk.base import webex_id_to_uuid


@dataclass(init=False, repr=False)
class TestDomainManagement(TestCaseWithLog):
    org_id: ClassVar[str]
    proxy = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        me = cls.api.people.me()
        cls.org_id = webex_id_to_uuid(me.org_id)

    def test_get_token(self):
        api = self.api.domain_management
        token = api.get_domain_verification_token(self.org_id, domain='example.com')
