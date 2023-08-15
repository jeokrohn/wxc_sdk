import asyncio

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.organizations import Organization


class TestOrganization(TestCaseWithLog):
    def test_001_list(self):
        orgs = list(self.api.organizations.list())
        me = self.api.people.me()
        my_org = next((org for org in orgs if me.org_id == org.org_id), None)
        self.assertIsNotNone(my_org)

    @async_test
    async def test_002_all_details(self):
        orgs = await self.async_api.organizations.list()
        details = await asyncio.gather(*[self.async_api.organizations.details(org_id=org.org_id,
                                                                              calling_data=True) for org in orgs])
        details: list[Organization]
        self.assertTrue(all(detail.xsi_domain for detail in details), 'Did not get XSI domain for all orgs')
        print(f'got details for {len(details)} orgs')
