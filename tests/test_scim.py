import asyncio
import base64
import json
import os
import random
import re
import uuid
from dataclasses import dataclass
from time import sleep
from typing import Optional, ClassVar
from unittest import skip

import yaml
from dotenv import load_dotenv
from pydantic import TypeAdapter
from test_helper.randomuser import User

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import random_users, available_extensions_gen
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.integration import Integration
from wxc_sdk.licenses import LicenseRequest, LicenseRequestOperation, LicenseProperties
from wxc_sdk.people import Person, PhoneNumberType
from wxc_sdk.scim.bulk import BulkOperation, BulkMethod
from wxc_sdk.scim.users import ScimUser, NameObject, EmailObject, EmailObjectType, UserTypeObject, UserPhoneNumber, \
    ScimPhoneNumberType, UserAddress, PatchUserOperation, PatchUserOperationOp
from wxc_sdk.tokens import Tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens to run a test

    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: Tokens
    """

    def env_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scim_service_app.env')
        return path

    def yml_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scim_service_app.yml')
        return path

    def read_tokens_from_file() -> Optional[Tokens]:
        """
        Get service app tokens from cache file, return None if cache does not exist
        """
        path = yml_path()
        if not os.path.isfile(path):
            return None
        try:
            with open(path, mode='r') as f:
                data = yaml.safe_load(f)
            tokens = Tokens.model_validate(data)
        except Exception:
            return None
        return tokens

    def write_tokens_to_file(tokens: Tokens):
        """
        Write tokens to cache
        """
        with open(yml_path(), mode='w') as f:
            yaml.safe_dump(tokens.model_dump(exclude_none=True), f)

    def get_access_token() -> Tokens:
        """
        Get a new access token using refresh token, service app client id, service app client secret
        """
        tokens = Tokens(refresh_token=os.getenv('SCIM_SERVICE_APP_REFRESH_TOKEN'))
        integration = Integration(client_id=os.getenv('SCIM_SERVICE_APP_CLIENT_ID'),
                                  client_secret=os.getenv('SCIM_SERVICE_APP_CLIENT_SECRET'),
                                  scopes=[], redirect_url=None)
        integration.refresh(tokens=tokens)
        write_tokens_to_file(tokens)
        return tokens

    load_dotenv(dotenv_path=env_path())
    # try to read from file
    tokens = read_tokens_from_file()
    # .. or create new access token using refresh token
    if tokens is None:
        tokens = get_access_token()
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


@dataclass(init=False)
class TestWithScimToken(TestCaseWithLog):

    test_api: ClassVar[WebexSimpleApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get service app tokens
        tokens = get_tokens()

        # create API with standard token
        cls.test_api = WebexSimpleApi(tokens=cls.api.access_token)
        # replace session access token with service app access token
        cls.api.session._tokens.access_token = tokens.access_token


class TestScimRead(TestWithScimToken):
    def test_search(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        users = self.api.scim.users.search(org_id=org_id)

        print(f'total results: {users.total_results}')
        print(f'start index: {users.start_index}')
        print(f'Items per page: {users.items_per_page}')
        print(f'resources: {len(users.resources)}')

    def test_search_all(self):
        """
        test search_all()
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        users = list(self.api.scim.users.search_all(org_id=org_id))
        print(f'Got {len(users)} users')
        requests = [r for r in self.requests(method='GET', url_filter=r'.+scim/.+/v2/Users')]
        for i, r in enumerate(requests):
            print(f'{i} - {r.url}')
            print(f'  start index: {r.response_body["startIndex"]}')
            print(f'  total results: {r.response_body["totalResults"]}')
            print(f'  items per page: {r.response_body["itemsPerPage"]}')

    def test_search_emails(self):
        """
        Apparently no emails are returned?
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim.users
        users = list(api.search_all(org_id=org_id))
        with_emails = [user for user in users if user.emails]
        self.assertFalse(not with_emails, 'No users with email addresses returned')

    def test_search_attrs(self):
        """
        Searching with attributes list
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim.users
        users_attrs = list(api.search_all(org_id=org_id, attributes='id,userName,displayName'))
        # we exp that all returned users have exactly these three attributes
        issues = [user for user in users_attrs
                  if set(user.model_dump(exclude_none=True)) != {'schemas', 'id', 'user_name', 'display_name'}]
        if issues:
            print(json.dumps(TypeAdapter(list[ScimUser]).dump_python(issues, mode='json', exclude_none=True), indent=2))
        self.assertTrue(not issues)

    def test_search_external_id(self):
        """
        search users with external_id
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim.users
        users = list(api.search_all(org_id=org_id, filter='externalId pr'))
        foo = 1

    @async_test
    async def test_async_search_all(self):
        """
        test search_all()
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.async_api.scim.users
        users = await api.search_all(org_id=org_id)
        print(f'Got {len(users)} users')
        requests = [r for r in self.requests(method='GET', url_filter=r'.+scim/.+/v2/Users')]
        for i, r in enumerate(requests):
            print(f'{i} - {r.url}')
            print(f'  start index: {r.response_body["startIndex"]}')
            print(f'  total results: {r.response_body["totalResults"]}')
            print(f'  items per page: {r.response_body["itemsPerPage"]}')

    def test_with_external_id(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        users = list(self.api.scim.users.search_all(org_id=org_id))
        with_external_id = [u for u in users if u.external_id]
        print(f'{len(users)} users')
        print(f'with_external_id: {len(with_external_id)}')
        print('\n'.join(sorted(f'  - {u.display_name}' for u in with_external_id)))

    @async_test
    async def test_details(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.async_api.scim.users
        users = await api.search(org_id=org_id)
        details = await asyncio.gather(*[api.details(org_id=org_id, user_id=u.id)
                                         for u in users.resources], return_exceptions=True)

    @async_test
    async def test_sip_uris(self):
        """
        Verify that SCIM returns SIP URIs for users
        """
        users_with_uris = [user for user in self.api.people.list() if user.sip_addresses]
        if not users_with_uris:
            self.skipTest("No users with SIP addresses")

        # get SCIM details for all these users
        org_id = webex_id_to_uuid(self.me.org_id)
        scim_details = await asyncio.gather(
            *[self.async_api.scim.users.details(org_id=org_id, user_id=webex_id_to_uuid(u.person_id))
              for u in users_with_uris])
        scim_details: list[ScimUser]
        err = 0
        display_name_len = max(len(user.display_name) for user in users_with_uris)
        for user, scim_user in zip(users_with_uris, scim_details):
            user: Person
            scim_user: ScimUser
            if not scim_user.webex_user.sip_addresses:
                err += 1
                print(f'Webex user {user.display_name:{display_name_len}}: no SIP addresses in SCIMv2 info')

        self.assertFalse(err, f'{err}/{len(users_with_uris)} SCIMv2 users are missing SIP addresses')


class TestScimCreate(TestWithScimToken):

    @staticmethod
    def us_e164(tn: str) -> str:
        """
        Convert formatted US phone numbers to regular +E.164 numbers
        """
        tn, _ = re.subn('[^0-9]', '', tn)
        return f'+1{tn}'

    def scim_user_from_random_user(self, new_user: User) -> ScimUser:
        """
        Create a SCIMv2 user object from random user data
        """
        return ScimUser(
            active=False,
            user_name=new_user.email,
            name=NameObject(given_name=new_user.name.first, family_name=new_user.name.last),
            display_name=new_user.display_name,
            emails=[EmailObject(value=new_user.email, type=EmailObjectType.work, primary=True)],
            user_type=UserTypeObject.user, external_id=f'test_{uuid.uuid4()}',
            phone_numbers=[
                UserPhoneNumber(value=self.us_e164(new_user.phone), type=ScimPhoneNumberType.work,
                                display=new_user.phone, primary=True),
                UserPhoneNumber(value=self.us_e164(new_user.cell), type=ScimPhoneNumberType.mobile,
                                display=new_user.cell, primary=False)],
            addresses=[
                UserAddress(type='work',
                            street_address=f'{new_user.location.street.number} {new_user.location.street.name}',
                            postal_code=f'{new_user.location.postcode}', country='US',
                            locality=new_user.location.city)])

    @async_test
    async def test_create_user(self):
        """
        Create a random user using SCIMv2
        - apparently meta is returned for created user, but not as part of user details
        """
        new_user = (await random_users(api=self.async_api, user_count=1, inc=['name', 'location', 'phone', 'cell']))[0]
        scim_user = self.scim_user_from_random_user(new_user)
        api = self.api.scim.users
        org_id = webex_id_to_uuid(self.me.org_id)
        created_user = api.create(org_id=org_id,
                                  user=scim_user)
        print(f'Created user: {created_user.display_name}({created_user.emails[0].value})')
        print('\n'.join(f'  {line}' for line in json.dumps(created_user.model_dump(mode='json',
                                                                                   exclude_none=True,
                                                                                   by_alias=True),
                                                           indent=2).splitlines()))
        details = api.details(org_id=org_id, user_id=created_user.id)

        # when creating a user we get webex.meta while this seems to be missing from details

        def print_meta(user):
            if user is None:
                print('  No webex user')
            elif user.meta:
                print('\n'.join(l for l in json.dumps(user.meta.model_dump(mode='json', by_alias=True,
                                                                           exclude_none=True),
                                                      indent=2).splitlines()))
            else:
                print('  None')

        print('webex.meta of created user:')
        print_meta(created_user.webex_user)
        print('webex.meta of details:')
        print_meta(details.webex_user)

        self.assertTrue(created_user.webex_user and details.webex_user, 'webex_user missing')
        self.assertEqual(created_user.webex_user.meta, details.webex_user.meta, 'meta not matching')

    @skip('Creating multiple users seems to be broken')
    @async_test
    async def test_create_multiple_users(self):
        """
        Create multiple random users
        """
        users_to_create = 10
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.async_api.scim.users
        users_before = await api.search_all(org_id=org_id)
        new_users = await random_users(api=self.async_api, user_count=users_to_create,
                                       inc=['name', 'location', 'phone', 'cell'])
        new_scim_users = list(map(self.scim_user_from_random_user, new_users))
        create = self.async_api.scim.users.create
        created_users = await asyncio.gather(*[create(org_id=org_id,
                                                      user=scim_user)
                                               for scim_user in new_scim_users],
                                             return_exceptions=True)
        err = None
        for i, (scim_user, created_user) in enumerate(zip(new_scim_users, created_users)):
            scim_user: ScimUser
            if isinstance(created_user, Exception):
                created_user: AsRestError
                err = err or created_user
                print(f'failed to create: {i}, {scim_user.display_name}({scim_user.emails[0].value}), {created_user}')
                print('\n'.join(f'  {l}' for l in json.dumps(created_user.detail, indent=2).splitlines()))
        users_after = await api.search_all(org_id=org_id)
        print(f'tried to create {users_to_create} users, before: {len(users_before)}, after: {len(users_after)} ')
        if err is not None:
            raise err
        self.assertTrue(len(users_after) == users_to_create + len(users_before),
                        f'User count doesn\'t reflect {users_to_create} new users')

    @async_test
    async def test_create_bulk(self):
        """
        Create a bunch of users using bulk operations
        """
        users_to_create = 20
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim
        users_before = list(api.users.search_all(org_id=org_id))
        new_users = await random_users(api=self.async_api, user_count=users_to_create,
                                       inc=['name', 'location', 'phone', 'cell'])
        new_scim_users = list(map(self.scim_user_from_random_user, new_users))

        # bulk operations to create a bunch of ScimUser instances
        operations = [BulkOperation(method=BulkMethod.post, path='/Users', bulk_id=str(uuid.uuid4()),
                                    data=scim_user.create_update())
                      for scim_user in new_scim_users]
        print(f'Creating {len(new_scim_users)} users')
        bulk_response = self.api.scim.bulk.bulk_request(org_id=org_id, fail_on_errors=1, operations=operations)
        users_after = list(api.users.search_all(org_id=org_id))
        err = False
        if not all(o.status == 201 for o in bulk_response.operations):
            err = True
            print(f'Some users not created. {sum(1 for o in bulk_response.operations if o.status != 201)} failed')
        if not all(o.user_id is not None for o in bulk_response.operations if o.status == 201):
            err = True
            print(f'Some user ids missing. '
                  f'{sum(1 for o in bulk_response.operations if o.status == 201 and not o.user_id)} missing')
        if len(users_after) != users_to_create + len(users_before):
            err = True
            print(f'before: {len(users_before)}, after: {len(users_after)}')
        self.assertFalse(err, 'Something went wrong; check output')


@dataclass(init=False)
class TestScimUpdate(TestWithScimToken):
    target_user: ClassVar[ScimUser]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        org_id = webex_id_to_uuid(cls.me.org_id)
        api = cls.api.scim.users
        test_users = [user for user in api.search_all(org_id=org_id)
                      if user.external_id]
        if not test_users:
            cls.target_user = None
            return
        target_user = random.choice(test_users)
        cls.target_user = api.details(org_id=org_id, user_id=target_user.id)

    def setUp(self) -> None:
        if not self.target_user:
            self.skipTest('No test users')
        super().setUp()

    def test_update(self):
        """
        Pick a random SCIM generated user, update something anc check
        """
        api = self.api.scim.users
        org_id = webex_id_to_uuid(self.me.org_id)
        target_details = self.target_user
        update = target_details.model_copy(deep=True)
        update.title = 'Dr.'
        api.update(org_id=org_id, user=update)
        try:
            details_after_update = api.details(org_id=org_id, user_id=self.target_user.id)
            # title has to be updated
            self.assertEqual('Dr.', details_after_update.title)
            # last_modified has to be changed
            self.assertTrue(details_after_update.meta.last_modified != target_details.meta.last_modified)
            # but other than meta and title everything else should be the same
            details_after_update.meta = target_details.meta
            details_after_update.title = target_details.title
            self.assertEqual(target_details, details_after_update)
        finally:
            api.update(org_id=org_id, user=target_details)
            restored_details = api.details(org_id=org_id, user_id=self.target_user.id)
            restored_details.meta = target_details.meta
            self.assertEqual(target_details, restored_details)

    def test_patch(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim.users
        target_details = api.details(org_id=org_id, user_id=self.target_user.id)
        patched = api.patch(org_id=org_id, user_id=self.target_user.id,
                            operations=[PatchUserOperation(op=PatchUserOperationOp.replace,
                                                           path='title',
                                                           value='Dr.')])
        try:
            details_after_update = api.details(org_id=org_id, user_id=target_details.id)
            # title has to be updated
            self.assertEqual('Dr.', details_after_update.title)
            # last_modified has to be changed
            self.assertTrue(details_after_update.meta.last_modified != target_details.meta.last_modified)
            # but other than meta and title everything else should be the same
            details_after_update.meta = target_details.meta
            details_after_update.title = target_details.title
            self.assertEqual(target_details, details_after_update)

        finally:
            api.update(org_id=org_id, user=target_details)
            restored_details = api.details(org_id=org_id, user_id=self.target_user.id)
            restored_details.meta = target_details.meta
            self.assertEqual(target_details, restored_details)

    def test_patch_phone_number(self):
        """
        Try to update a phone number of a user
        """
        me = self.api.people.me()
        print(f'org: id {me.org_id}, base64 decoded {base64.b64decode(me.org_id+"==")}')
        org_id = webex_id_to_uuid(me.org_id)
        api = self.api.scim.users
        target_details = api.details(org_id=org_id, user_id=self.target_user.id)
        new_phone_number = '+14085550123'
        patched = api.patch(org_id=org_id, user_id=self.target_user.id,
                            operations=[PatchUserOperation(op=PatchUserOperationOp.replace,
                                                           path='phoneNumbers[type eq "work"].value',
                                                           value=new_phone_number)])
        try:
            details_after_update = api.details(org_id=org_id, user_id=target_details.id)
            work_phone = next(pn for pn in details_after_update.phone_numbers if pn.type=='work')
            self.assertEqual(new_phone_number, work_phone.value)
            # last_modified has to be changed
            self.assertTrue(details_after_update.meta.last_modified != target_details.meta.last_modified)

        finally:
            api.update(org_id=org_id, user=target_details)
            restored_details = api.details(org_id=org_id, user_id=self.target_user.id)
            restored_details.meta = target_details.meta
            self.assertEqual(target_details, restored_details)


class TestScimDelete(TestWithScimToken):

    @skip('skipping to keep test users .. for now')
    @async_test
    async def test_delete_users_with_external_id(self):
        """
        Delete all users with external id
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        users = list(self.api.scim.users.search_all(org_id=org_id))
        with_external_id = [u for u in users if u.external_id]
        if not with_external_id:
            self.skipTest('No users with external id')
        print(f'Deleting {len(with_external_id)} users with external id')
        await asyncio.gather(*[self.async_api.scim.users.delete(org_id=org_id, user_id=u.id)
                               for u in with_external_id])

    def test_bulk_delete(self):
        """
        try to bulk delete some users
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.api.scim
        targets = list(user
                       for user, _ in zip((user for user in api.users.search_all(org_id=org_id)
                                           if user.external_id),
                                          range(10))
                       if user)
        if not targets:
            self.skipTest('No users with external id to delete')
        operations = [BulkOperation(method=BulkMethod.delete, path=f'/Users/{user.id}', bulk_id=str(uuid.uuid4()))
                      for user in targets]
        response = api.bulk.bulk_request(org_id=org_id, fail_on_errors=1, operations=operations)
        self.assertTrue(all(o.status == 204 for o in response.operations), 'Some users not deleted')


class TestScimAndPeople(TestScimCreate, TestWithLocations):
    """
    Tests combining SCIMv2 with people API calls
    """

    @async_test
    async def test_create_scim_calling_delete(self):
        """
        * create a user using SCIM
        * enable user for calling
        * delete user using SCIM
        * are calling licenses counted properly
        """
        with self.no_log():
            # create a user using SCIM
            new_user = (await random_users(api=self.async_api, user_count=1, inc=['name', 'location', 'phone', 'cell']))[0]
            scim_user = self.scim_user_from_random_user(new_user)
            standard_license = next(lic for lic in self.test_api.licenses.list() if lic.webex_calling_basic)
            standard_license = self.test_api.licenses.details(license_id=standard_license.license_id)
            # pick a calling location
            target_location = random.choice(self.locations)
            # get extension in location
            extension = next(available_extensions_gen(api=self.api,
                                                      location_id=target_location.location_id))

        api = self.api.scim.users
        org_id = webex_id_to_uuid(self.me.org_id)
        scim_user = api.create(org_id=org_id,
                               user=scim_user)
        with self.no_log():
            webex_user = next(user for user in self.test_api.people.list(email=new_user.email))
        webex_user = self.test_api.people.details(person_id=webex_user.person_id, calling_data=True)
        try:
            # enable user for calling (standard license)
            # try to add standard license to user
            self.test_api.licenses.assign_licenses_to_users(
                person_id=webex_user.person_id,
                licenses=[LicenseRequest(
                    operation=LicenseRequestOperation.add,
                    id=standard_license.license_id,
                    properties=LicenseProperties(
                        location_id=target_location.location_id,
                        extension=extension))])
            license_after = self.test_api.licenses.details(license_id=standard_license.license_id)
            scim_user_after = api.details(org_id=org_id, user_id=scim_user.id)
            webex_user_after = self.test_api.people.details(person_id=webex_user.person_id, calling_data=True)
            self.assertEqual(standard_license.consumed_by_users+1, license_after.consumed_by_users)

            # work phone number should be gone
            scim_work_phone = next((pn for pn in scim_user_after.phone_numbers
                                    if pn.type == ScimPhoneNumberType.work), None)
            self.assertIsNone(scim_work_phone)
            webex_work_phone = next((pn for pn in webex_user_after.phone_numbers
                                     if pn.number_type == PhoneNumberType.work), None)
            self.assertIsNone(webex_work_phone)

            # work extension should exist
            scim_work_phone = next((pn for pn in scim_user_after.phone_numbers
                                    if pn.type == ScimPhoneNumberType.work_extension),
                                   None)
            self.assertIsNotNone(scim_work_phone)
            self.assertTrue(scim_work_phone.value.endswith(extension))
            webex_work_phone = next((pn for pn in webex_user_after.phone_numbers
                                     if pn.number_type == PhoneNumberType.work_extension), None)
            self.assertIsNotNone(webex_work_phone)
            self.assertTrue(webex_work_phone.value.endswith(extension))
        finally:
            self.api.scim.users.delete(org_id=org_id, user_id=scim_user.id)
            # self.test_api.people.delete_person(person_id=webex_user.person_id)
            for i in range(3):
                license_after = self.test_api.licenses.details(license_id=standard_license.license_id)
                try:
                    self.assertEqual(standard_license.consumed_by_users, license_after.consumed_by_users)
                except AssertionError:
                    if i == 2:
                        raise
                    print('License not updated. Retry, waiting for 5 seconds')
                    sleep(3)
                else:
                    break
