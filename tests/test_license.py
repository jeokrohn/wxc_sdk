from .base import TestCaseWithLog


class TestLicense(TestCaseWithLog):

    def test_001_list(self):
        """
        list licenses
        """
        lic_list = list(self.api.licenses.list())
        print(f'got {len(lic_list)} licenses')

    def test_002_calling_users_by_license(self):
        calling_license_ids = set(lic.license_id for lic in self.api.licenses.list()
                                  if lic.webex_calling)
        calling_users = [user for user in self.api.people.list()
                         if any(license_id in calling_license_ids for license_id in user.licenses)]
        print(f'Found {len(calling_users)} calling users')
