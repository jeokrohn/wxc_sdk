import asyncio

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.people import Person


class TestRoles(TestCaseWithLog):
    def test_list(self):
        """
        list all roles
        """
        roles = self.api.roles.list()
        print(f'got {len(roles)} roles')
        for role in roles:
            print(role)

    @async_test
    async def test_details(self):
        """
        Get details for all roles
        """
        roles = self.api.roles.list()
        details_list = await asyncio.gather(*[self.async_api.roles.details(role.id) for role in roles])
        print(f'got {len(details_list)} role details')
        for details in details_list:
            print(details)

    def test_toggle_full_admin(self):
        """
        Test to promote a user to a full admin
        """
        target = next(self.api.people.list(display_name='Heidi Harper'))
        target = self.api.people.details(target.person_id)
        role = next(role for role in self.api.roles.list() if role.name == 'Full Administrator')
        roles = set(target.roles)
        if role.id in roles:
            print(f'{target.display_name} is already a full admin. Removing role')
            roles.remove(role.id)
        else:
            print(f'Adding full admin role to {target.display_name}')
            roles.add(role.id)
        settings = Person(roles=list(roles), id=target.person_id, display_name=target.display_name,
                          licenses=target.licenses)
        self.api.people.update(settings)
        after = self.api.people.details(target.person_id)

        # roles change, so we don't compare them
        target.roles = after.roles
        # site urls can change, so we don't compare them
        target.site_urls = after.site_urls
        # last_modified changes, so we don't compare them
        target.last_modified = after.last_modified
        self.assertEqual(target, after)
