import asyncio
from operator import attrgetter

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.authorizations import Authorization
from wxc_sdk.people import Person


class AuthTest(TestCaseWithLog):
    @async_test
    async def test_list(self):
        """
        list authorizations for all users
        """
        users = await self.async_api.people.list()
        users.sort(key=attrgetter('display_name'))
        auth_lists = await asyncio.gather(*[self.async_api.authorizations.list(person_id=user.person_id)
                                            for user in users],
                                          return_exceptions=True)
        err = None
        for user, authorizations in zip(users, auth_lists):
            user: Person
            if not authorizations:
                continue

            print(f'{user.display_name}', end='')
            if isinstance(authorizations, Exception):
                err = err or authorizations
                print(f'{authorizations}')
            authorizations: list[Authorization]
            print()
            print('\n'.join(f'  {auth.type}, {auth.application_name}' for auth in authorizations))
        if err:
            raise err

    def test_list_params(self):
        """
        Verify list() parameter validation
        """
        f = self.api.authorizations.list
        with self.assertRaises(ValueError):
            f()
        with self.assertRaises(ValueError):
            f(person_id='foo', person_email='bar')

    def test_delete_params(self):
        """
        Verify delete() parameter validation
        """
        f = self.api.authorizations.delete
        with self.assertRaises(ValueError):
            f()
        with self.assertRaises(ValueError):
            f(authorization_id='foo', client_id='bar')
        with self.assertRaises(ValueError):
            f(authorization_id='foo', org_id='bar')
        with self.assertRaises(ValueError):
            f(org_id='foo')
