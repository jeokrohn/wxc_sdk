import asyncio
from operator import attrgetter
from typing import Union

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.licenses import LicenseUser, License


class TestLicense(TestCaseWithLog):

    def test_001_list(self):
        """
        list licenses
        """
        lic_list = list(self.api.licenses.list())
        lic_list.sort(key=attrgetter('name'))
        print(f'got {len(lic_list)} licenses')
        name_len = max(len(lic.name) for lic in lic_list)
        print('\n'.join(f'{lic.name:{name_len}}/{webex_id_to_uuid(lic.license_id).split(":")[-1].split("_")[0]}'
                        for lic in lic_list))

    def test_002_calling_users_by_license(self):
        calling_license_ids = set(lic.license_id for lic in self.api.licenses.list()
                                  if lic.webex_calling)
        calling_users = [user for user in self.api.people.list()
                         if any(license_id in calling_license_ids for license_id in user.licenses)]
        print(f'Found {len(calling_users)} calling users')

    @async_test
    async def test_003_assigned_users_for_calling_licenses(self):
        calling_licenses = [lic for lic in self.api.licenses.list()
                            if lic.webex_calling and not lic.webex_calling_workspaces]
        users = await asyncio.gather(*[self.async_api.licenses.assigned_users(license_id=lic.license_id,
                                                                              limit=4)
                                       for lic in calling_licenses],
                                     return_exceptions=True)
        users: list[Union[Exception, list[LicenseUser]]]
        for lic, user_list in zip(calling_licenses, users):
            lic: License
            print(f'{lic.name}: ', end='')
            if isinstance(user_list, Exception):
                print(f'{user_list}')
                continue
            print(f'{len(user_list)} users: '
                  f'{", ".join(u.display_name for u in sorted(user_list, key=attrgetter("display_name")))}')
