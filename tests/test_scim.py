"""
* SCIM users
* SCIM groups
* SCIM bulk operations
* organization contacts
"""
import asyncio
import base64
import json
import os
import random
import re
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import reduce
from json import JSONDecodeError
from operator import attrgetter
from time import sleep
from typing import Optional, ClassVar
from unittest import skip

import yaml
from dotenv import load_dotenv
from pydantic import TypeAdapter
from test_helper.randomuser import User

from tests.base import TestCaseWithLog, async_test, TestWithLocations, TestCaseWithUsers, WithIntegrationTokens
from tests.testutil import random_users, available_extensions_gen
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import OwnerType
from wxc_sdk.groups import Group
from wxc_sdk.integration import Integration
from wxc_sdk.licenses import LicenseRequest, LicenseRequestOperation, LicenseProperties
from wxc_sdk.org_contacts import Contact, PrimaryContactMethod, ContactEmail, EmailType, ContactPhoneNumber, \
    ContactAddress
from wxc_sdk.people import Person, PhoneNumberType
from wxc_sdk.scim.bulk import BulkOperation, BulkMethod, BulkResponseOperation
from wxc_sdk.scim.groups import ScimGroup, ScimGroupMember
from wxc_sdk.scim.users import ScimUser, NameObject, EmailObject, EmailObjectType, UserTypeObject, UserPhoneNumber, \
    ScimPhoneNumberType, UserAddress, PatchUserOperation, PatchUserOperationOp
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.tokens import Tokens

TEST_GROUPS = 'Test Group'


def external_id() -> str:
    """
    Create a random external id
    """
    return f'test_{uuid.uuid4()}'


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

    @property
    def org_id(self) -> str:
        return webex_id_to_uuid(self.me.org_id)


class TestScimRead(TestWithScimToken):
    def test_search(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        users = self.api.scim.users.search(org_id=org_id)

        print(f'total results: {users.total_results}')
        print(f'start index: {users.start_index}')
        print(f'Items per page: {users.items_per_page}')
        print(f'resources: {len(users.resources)}')

    def test_search_users_with_work_extensions(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        users = self.api.scim.users.search(org_id=org_id, filter='phoneNumbers [ type eq "work_extension"]')

        print(f'total results: {users.total_results}')
        print(f'start index: {users.start_index}')
        print(f'Items per page: {users.items_per_page}')
        print(f'resources: {len(users.resources)}')

    def test_search_all(self):
        """
        test search_all()
        """
        users = list(self.api.scim.users.search_all(org_id=self.org_id))
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

    def test_with_groups(self):
        """
        Get users with groups
        """
        api = self.api.scim.users
        users = list(api.search_all(org_id=self.org_id, return_groups=True))
        users_with_groups = [u for u in users if u.groups]
        print(f'Users with groups: {len(users_with_groups)}')
        print(json.dumps(TypeAdapter(list[ScimUser]).dump_python(users_with_groups, mode='json', exclude_unset=True),
                         indent=2))

    def test_with_group_details(self):
        """
        Get users with groups
        """
        api = self.api.scim.users
        users = list(api.search_all(org_id=self.org_id, include_group_details=True))
        users_with_groups = [u for u in users if u.groups]
        print(f'Users with groups: {len(users_with_groups)}')
        print(json.dumps(TypeAdapter(list[ScimUser]).dump_python(users_with_groups, mode='json', exclude_unset=True),
                         indent=2))


def us_e164(tn: str) -> str:
    """
    Convert formatted US phone numbers to regular +E.164 numbers
    """
    tn, _ = re.subn('[^0-9]', '', tn)
    return f'+1{tn}'


class TestScimCreate(TestWithScimToken):

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
                UserPhoneNumber(value=us_e164(new_user.phone), type=ScimPhoneNumberType.work,
                                display=new_user.phone, primary=True),
                UserPhoneNumber(value=us_e164(new_user.cell), type=ScimPhoneNumberType.mobile,
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
        print(f'org: id {me.org_id}, base64 decoded {base64.b64decode(me.org_id + "==")}')
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
            work_phone = next(pn for pn in details_after_update.phone_numbers if pn.type == 'work')
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
            new_user = (await random_users(api=self.async_api, user_count=1,
                                           inc=['name', 'location', 'phone', 'cell']))[0]
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
            self.assertEqual(standard_license.consumed_by_users + 1, license_after.consumed_by_users)

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


@dataclass(init=False)
class TestScimAndCalling(TestWithScimToken, TestCaseWithUsers):
    """
    tests to validate number information in CI (and people API) for calling users

    """

    @async_test
    async def test_numbers(self):
        """
        for all calling users look at number information in
            * people API
            * numbers API
            * scim
        """
        # for all locations we have users in we also need the site prefix
        location_ids = set(user.location_id for user in self.users)
        telephony_location_details = {loc.location_id: loc
                                      for loc in await asyncio.gather(
                *[self.async_api.telephony.location.details(location_id=loc_id) for loc_id in location_ids])}
        telephony_location_details: dict[str, TelephonyLocation]

        # get all primary numbers owned by users
        numbers = {number.owner.owner_id: number
                   for number in self.api.telephony.phone_numbers(owner_type=OwnerType.people)}

        # get all scim user details
        scim_details = await asyncio.gather(
            *[self.async_api.scim.users.details(org_id=self.org_id,
                                                user_id=webex_id_to_uuid(user.person_id))
              for user in self.users])
        scim_users = list(
            self.api.scim.users.search_all(org_id=self.org_id, return_groups='true', include_group_details='true'))
        foo = 1
        for user, scim_user in zip(self.users, scim_details):
            user: Person
            scim_user: ScimUser
            print(f'User: {user.display_name}({user.emails[0]})')
            print(user.phone_numbers)
            print(scim_user.phone_numbers)
            number = numbers.get(user.person_id)
            print(f'Number: {number}')
            location = telephony_location_details.get(user.location_id)
            print(f'Location "{location.name}", prefix: {location.routing_prefix}')

            # check phone number
            work = next((pn.value for pn in user.phone_numbers if pn.number_type == 'work'), None)
            if work != number.phone_number:
                print(f'************ phone number mismatch!!')

            # check extension
            work_extension = next((pn.value for pn in user.phone_numbers if pn.number_type == 'work_extension'), None)
            if work_extension != number.esn:
                print('************ work extension mismatch!!')
                # set correct extension in SCIM
                self.api.scim.users.patch(org_id=self.org_id,
                                          user_id=scim_user.id,
                                          operations=[
                                              PatchUserOperation(op=PatchUserOperationOp.replace,
                                                                 path='phoneNumbers[type eq "work_extension"].value',
                                                                 value=number.esn)])
                after_update = self.api.scim.users.details(org_id=self.org_id, user_id=scim_user.id)
                print(f'SCIM numbers after update: {after_update.phone_numbers}')

                # try to update user via people API
                people_update = user.model_copy(deep=True)
                people_update.extension = number.extension
                self.api.people.update(person=people_update, calling_data=True)
                people_details = self.api.people.details(person_id=user.person_id, calling_data=True)
                after_details = self.api.scim.users.details(org_id=self.org_id, user_id=scim_user.id)
                print(f'numbers after details: {after_details.phone_numbers}')
            print()

    def test_locations(self):
        """
        Check consistency between location and SCIM groups
        """
        scim_users = {scim_user.id: scim_user
                      for scim_user in self.api.scim.users.search_all(org_id=self.org_id,
                                                                      return_groups='true',
                                                                      include_group_details='true')}
        locations = {loc.location_id: loc for loc in self.api.locations.list()}
        err = False
        for user in self.users:
            scim_user = scim_users.get(webex_id_to_uuid(user.person_id))
            print(f'user: {user.display_name}({user.emails[0]})')
            if not scim_user:
                print('******** no SCIM user')
                err = True
                continue
            location = locations.get(user.location_id)
            if not location:
                print('******** no location')
                err = True
                continue
            location_name = location.name
            print(f'Location: {location_name}')
            scim_group_name = scim_user.groups[0].display
            print(f'SCIM group name: {scim_group_name}')
            if location_name != scim_group_name:
                print('******** location inconsistency')
                err = True
            print()
        self.assertFalse(err, 'Inconsistencies found')


@dataclass(init=False)
class TestScimGroups(TestWithScimToken):
    def test_search(self):
        """
        search groups
        """
        groups = self.api.scim.groups.search(org_id=self.org_id, include_members=True)
        print(f'total results: {groups.total_results}')
        print(f'start index: {groups.start_index}')
        print(f'Items per page: {groups.items_per_page}')
        print(f'resources: {len(groups.resources)}')

    def test_search_all(self):
        """
        search all
        """
        groups = list(self.api.scim.groups.search_all(org_id=self.org_id, include_members=True))
        print(f'{len(groups)} groups')
        print(json.dumps(TypeAdapter(list[ScimGroup]).dump_python(groups, mode='json', by_alias=True), indent=2))

    @async_test
    async def test_as_search_all(self):
        """
        search all, async variant
        """
        groups = await self.async_api.scim.groups.search_all(org_id=self.org_id)
        print(f'{len(groups)} groups')

    def test_members(self):
        """
        members
        """
        groups = list(self.api.scim.groups.search_all(org_id=self.org_id, include_members=True))
        group = groups[1]
        members = self.api.scim.groups.members(org_id=self.org_id, group_id=group.id)
        print(f'total results: {members.member_size}')
        print(f'start index: {members.start_index}')
        print(f'Items per page: {members.items_per_page}')
        print(f'members: {len(members.members)}')
        print(f'display name: {members.display_name}')
        print(json.dumps(TypeAdapter(list[ScimGroupMember]).dump_python(members.members, mode='json', by_alias=True),
                         indent=2))

    def test_members_all(self):
        """
        members_all
        """
        groups = list(self.api.scim.groups.search_all(org_id=self.org_id, include_members=True))
        group = groups[1]
        members = list(self.api.scim.groups.members_all(org_id=self.org_id, group_id=group.id, count=2))
        print(f'{len(members)} members')
        print(json.dumps(TypeAdapter(list[ScimGroupMember]).dump_python(members, mode='json', by_alias=True), indent=2))

    @async_test
    async def test_as_members_all(self):
        """
        members_all
        """
        groups = list(self.api.scim.groups.search_all(org_id=self.org_id, include_members=True))
        group = groups[1]
        members = await self.async_api.scim.groups.members_all(org_id=self.org_id, group_id=group.id, count=2)
        print(f'{len(members)} members')
        print(json.dumps(TypeAdapter(list[ScimGroupMember]).dump_python(members, mode='json', by_alias=True), indent=2))

    def test_create_group(self):
        """
        create a group
        """
        api = self.api.scim
        new_group = api.groups.create(org_id=self.org_id, group=ScimGroup(display_name='Test Group',
                                                                          external_id=external_id()))
        print(json.dumps(new_group.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        groups = list(api.groups.search_all(org_id=self.org_id))
        groups_by_usage: dict[str, list[ScimGroup]] = reduce(
            lambda acc, group: acc[group.webex_group.usage].append(group) or acc,
            groups,
            defaultdict(list))

    def test_delete_group(self):
        """
        Delete a random test group
        """
        api = self.api.scim
        groups = [group for group in api.groups.search_all(org_id=self.org_id)
                  if group.display_name.startswith(TEST_GROUPS) and group.external_id]
        if not groups:
            self.skipTest('No test groups')
        target = random.choice(groups)
        api.groups.delete(org_id=self.org_id, group_id=target.id)
        after = [group for group in api.groups.search_all(org_id=self.org_id)
                 if group.display_name.startswith(TEST_GROUPS)]
        self.assertEqual(len(groups) - 1, len(after), 'Group not deleted')

    def test_scim_wx_group_consistency(self):
        """
        Check consistency between SCIM groups and Webex groups
        """
        scim_groups: dict[str, ScimGroup] = {group.id: group
                                             for group in self.api.scim.groups.search_all(org_id=self.org_id,
                                                                                          include_members=True)}
        # bsse46 decoded webex group ids are something like:
        # ciscospark://us/SCIM_GROUP/3a137ef5-d527-4576-8445-eb394e66d2b4:36818b6f-ef07-43d1-b76f-ced79ab2e3e7
        # .. where the 1st UUID seems to correspond to SCIM group id and the 2nd is the org id
        wx_groups = list(self.test_api.groups.list())
        with ThreadPoolExecutor() as pool:
            wx_groups = list(pool.map(lambda group: self.test_api.groups.details(group.group_id, include_members=True),
                                      wx_groups))
        webex_groups: dict[str, Group] = {webex_id_to_uuid(group.group_id).split(':')[0]: group
                                          for group in wx_groups}
        scim_not_in_webex = set(scim_groups.keys()) - set(webex_groups.keys())
        webex_not_in_scim = set(webex_groups.keys()) - set(scim_groups.keys())

        # we expect all scim groups to be in Webex ... with the exception of the "All Org Users" group
        self.assertEqual(1, len(scim_not_in_webex))
        scim_id = next(iter(scim_not_in_webex))
        self.assertEqual('All Org Users', scim_groups[scim_id].display_name)

        # we expect all Webex groups to be in SCIM
        self.assertFalse(webex_not_in_scim,
                         f'Webex groups not in SCIM: '
                         f'{", ".join(webex_groups[id].display_name for id in webex_not_in_scim)}')
        # now look at member consistency
        for group_uuid, wx_group in webex_groups.items():
            scim_group = scim_groups.get(group_uuid)
            wx_members = wx_group.members or list()
            scim_members = scim_group.members or list()
            self.assertEqual(len(wx_members), len(scim_members))
            scim_member_ids = {member.value for member in scim_members}
            wx_member_ids = {webex_id_to_uuid(member.member_id) for member in wx_members}
            self.assertEqual(scim_member_ids, wx_member_ids)
        return


class TestUsersAndGroups(TestScimCreate):
    """
    Tests for SCIM users and groups
    """

    def user_and_group_consistency(self):
        # get all users and groups
        users: dict[str, ScimUser] = {user.id: user
                                      for user in self.api.scim.users.search_all(org_id=self.org_id,
                                                                                 include_group_details=True)
                                      if user.external_id and user.groups}
        groups: dict[str, ScimGroup] = {group.id: group
                                        for group in self.api.scim.groups.search_all(org_id=self.org_id,
                                                                                     include_members=True)
                                        if group.external_id and group.members}
        err = None
        for user in sorted(users.values(), key=attrgetter('display_name')):
            user: ScimUser
            print(f'{user.display_name}({user.emails[0].value})')
            print(f'  groups: {", ".join(g.display for g in sorted(user.groups, key=attrgetter("display")))}')
            for user_group in user.groups:
                group = groups.get(user_group.value)
                try:
                    self.assertIsNotNone(group,
                                         f'Group {user_group.value}/{user_group.display} not found for '
                                         f'user {user.display_name}')
                    self.assertTrue(any(m.value == user.id for m in group.members),
                                    f'User {user.display_name} not in group {group.display_name}')
                except AssertionError as e:
                    print(f'  {e}')
                    err = err or e
        for group in sorted(groups.values(), key=attrgetter('display_name')):
            group: ScimGroup
            print(f'{group.display_name}')
            print(f'  members: {", ".join(m.display for m in sorted(group.members, key=attrgetter("display")))}')
            for member in group.members:
                user = users.get(member.value)
                try:
                    self.assertIsNotNone(user,
                                         f'User {member.value}/{member.display} not found for '
                                         f'group {group.display_name}')
                    self.assertTrue(any(g.value == group.id for g in user.groups),
                                    f'Group {group.display_name} not in user {user.display_name}')
                except AssertionError as e:
                    print(f'  {e}')
                    err = err or e
        return err

    def test_consistency(self):
        """
        Check consistency between users and groups
        """
        err = self.user_and_group_consistency()
        if err:
            raise

    @async_test
    async def test_create_groups_with_users(self):
        """
        Create some users and add them to a few groups
        """
        users_to_create = 50
        groups_to_create = 10
        with self.no_log():
            new_users = await random_users(api=self.async_api, user_count=users_to_create,
                                           inc=['name', 'location', 'phone', 'cell'])
        new_scim_users = list(map(self.scim_user_from_random_user, new_users))

        # bulk operations to create a bunch of ScimUser instances
        operations = [BulkOperation(method=BulkMethod.post, path='/Users', bulk_id=str(uuid.uuid4()),
                                    data=scim_user.create_update())
                      for scim_user in new_scim_users]
        print(f'Creating {len(new_scim_users)} users')
        bulk_response = self.api.scim.bulk.bulk_request(org_id=self.org_id, fail_on_errors=1, operations=operations)
        for scim_user, operation in zip(new_scim_users, bulk_response.operations):
            scim_user: ScimUser
            operation: BulkResponseOperation
            scim_user.id = operation.user_id
        users_for_groups = [list() for _ in range(groups_to_create)]
        for user in new_scim_users:
            groups_for_user = random.sample(range(groups_to_create), random.randint(1, groups_to_create))
            for g in groups_for_user:
                users_for_groups[g].append(user)
        async with AsWebexSimpleApi(tokens=self.api.access_token) as as_api:
            tasks = [as_api.scim.groups.create(org_id=self.org_id,
                                               group=ScimGroup(display_name=f'{TEST_GROUPS} {uuid.uuid4()}',
                                                               external_id=external_id(),
                                                               members=[ScimGroupMember(value=scim_user.id,
                                                                                        type='user')
                                                                        for scim_user in users_for_groups[i]]))
                     for i in range(groups_to_create)]
            groups = await asyncio.gather(*tasks)
        print(json.dumps(TypeAdapter(list[ScimGroup]).dump_python(groups, mode='json', by_alias=True), indent=2))
        err_round = None
        for i in range(1, 6):
            err = self.user_and_group_consistency()
            if err:
                print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Inconsistencies found in round {i}')
                err_round = i
                if i == 5:
                    raise err
                sleep(5)
        if err_round:
            self.fail(f'Inconsistencies found in round {err_round}')

    def test_remove_user_from_group_by_updating_group(self):
        """
        Try to remove a user from a group by updating the user
        """
        candidates = [user for user in self.api.scim.users.search_all(org_id=self.org_id, include_group_details=True)
                      if user.external_id and user.groups]
        if not candidates:
            self.skipTest('No users with external id and groups')
        target = random.choice(candidates)
        target: ScimUser

        print(f'Target user: {target.display_name}({target.emails[0].value})')
        print(f'Groups: {", ".join(g.display for g in sorted(target.groups, key=attrgetter("display")))}')

        remove_group = target.groups[0]
        print(f'Removing group: {remove_group.display}')
        group_before = self.api.scim.groups.details(org_id=self.org_id, group_id=remove_group.value)
        print('group before:')
        print(json.dumps(group_before.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        # prepare group update
        group_update = group_before.model_copy(deep=True)
        # ... without the member we want to remove
        group_update.members = [m for m in group_update.members if m.value != target.id]
        self.api.scim.groups.update(org_id=self.org_id, group=group_update)

        # user after with group info can only be fetched by searching
        user_after = next(self.api.scim.users.search_all(org_id=self.org_id, filter=f'id eq "{target.id}"',
                                                         include_group_details=True))
        print(f'Updated user')
        print(json.dumps(user_after.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        # get updated group
        group_after = self.api.scim.groups.details(org_id=self.org_id, group_id=remove_group.value)
        print('group after:')
        print(json.dumps(group_after.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

        self.assertTrue(user_after.groups is None or remove_group.value not in {g.value for g in user_after.groups},
                        'Group still present in user')
        self.assertTrue(group_after.members is None or target.id not in {m.value for m in group_after.members},
                        'User still present in group')


class TestOrgContacts(TestWithScimToken, WithIntegrationTokens):
    """
    tests for org contacts
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.int_api = WebexSimpleApi(tokens=cls.integration_tokens)

    def contact_from_random_user(self, new_user: User, address_as_str: bool = True) -> Contact:
        """
        Create a SCIMv2 user object from random user data
        """
        contact = Contact(
            display_name=new_user.display_name,
            first_name=new_user.name.first,
            last_name=new_user.name.last,
            company_name='Test Company',
            title='',

            primary_contact_method=PrimaryContactMethod.phone,
            emails=[ContactEmail(value=new_user.email, type=EmailType.work, primary=True)],
            phone_numbers=[
                ContactPhoneNumber(value=us_e164(new_user.phone), type=ScimPhoneNumberType.work,
                                   primary=True),
                ContactPhoneNumber(value=us_e164(new_user.cell), type=ScimPhoneNumberType.mobile)],
            source='CH'
        )
        if address_as_str:
            contact.address = (f'{new_user.location.street.number} {new_user.location.street.name}, '
                               f'{new_user.location.postcode} {new_user.location.city}')
        else:
            contact.address_info = ContactAddress(city=new_user.location.city, country=new_user.location.country,
                                                  state=new_user.location.state,
                                                  street=f'{new_user.location.street.number} '
                                                         f'{new_user.location.street.name}',
                                                  zip_code=str(new_user.location.postcode))
        return contact

    @async_test
    async def test_001_create_single_contact_address_as_str(self):
        """
        create a contact and provide address as string
        """
        with self.no_log():
            new_user = \
                (await random_users(api=self.async_api, user_count=1, inc=['name', 'location', 'phone', 'cell']))[0]
        contact = self.contact_from_random_user(new_user)
        api = self.int_api.org_contacts
        org_id = webex_id_to_uuid(self.me.org_id)
        created = api.create(org_id=org_id,
                             contact=contact)
        print('Created contact:')
        print(json.dumps(created.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
        self.assertEqual(contact.address, created.address)
        self.assertIsNone(created.address_info)

    @async_test
    async def test_002_create_single_contact_address_info(self):
        """
        create a contact and provide address as ContactAddress in address_info
        """
        with self.no_log():
            new_user = \
                (await random_users(api=self.async_api, user_count=1, inc=['name', 'location', 'phone', 'cell']))[0]
        contact = self.contact_from_random_user(new_user, address_as_str=False)
        api = self.int_api.org_contacts
        org_id = webex_id_to_uuid(self.me.org_id)
        created = api.create(org_id=org_id,
                             contact=contact)
        print('Created contact:')
        print(json.dumps(created.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
        self.assertTrue(created.address)
        try:
            deserialized_address = json.loads(created.address)
        except JSONDecodeError:
            self.fail('Address not JSON')
        address = ContactAddress.model_validate(deserialized_address)
        self.assertEqual(created.address_info, address)

    @async_test
    async def test_003_create_bulk_20(self):
        """
        Create 20 contacts in bulk
        """
        count = 20
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.int_api.org_contacts
        with self.no_log():
            new_users = await random_users(api=self.async_api, user_count=count,
                                           inc=['name', 'location', 'phone', 'cell'])
        contacts = list(map(self.contact_from_random_user, new_users))
        result = api.bulk_create_or_update(org_id=org_id, contacts=contacts)
        print(json.dumps(result.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))

    @async_test
    async def test_004_create_bulk_with_errors(self):
        """
        Create 100 contacts in bulk
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.int_api.org_contacts
        with self.no_log():
            new_users = await random_users(api=self.async_api, user_count=2,
                                           inc=['name', 'location', 'phone', 'cell'])
        contacts = [self.contact_from_random_user(user, address_as_str=False)
                    for user in new_users]
        err_contact = Contact(display_name='foo')
        contacts.append(err_contact)
        result = api.bulk_create_or_update(org_id=org_id, contacts=contacts)
        print(json.dumps(result.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
        self.assertEqual(2, sum(1 for r in result.contacts if r is not None))
        self.assertEqual(1, len(result.failed_contacts))
        self.assertEqual(2, result.failed_contacts[0].id)

    def test_005_list(self):
        """
        List contacts
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        contacts = list(self.int_api.org_contacts.list(org_id=org_id))
        print(f'Got {len(contacts)} contacts')

    def test_006_list_pagination(self):
        """
        List contacts and check whether pagination works
        """
        limit = 5
        org_id = webex_id_to_uuid(self.me.org_id)
        contacts = list(self.int_api.org_contacts.list(org_id=org_id, limit=limit))
        requests = list(self.requests())
        first_body = requests[0].response_body
        contacts = TypeAdapter(list[Contact]).validate_python(first_body['result'])
        print(f'Got {len(contacts)} contacts')
        if len(contacts) == first_body['total']:
            self.skipTest('Not enough contacts to run test')
        self.assertEqual(limit, len(contacts))
        self.assertTrue(len(requests) > 1, 'No pagination')

    def test_007_delete_contact(self):
        """
        delete a contact
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.int_api.org_contacts
        contacts = [contact for contact in api.list(org_id=org_id)
                    if contact.company_name == 'Test Company']
        target = random.choice(contacts)
        before = list(api.list(org_id=org_id, keyword=target.display_name))
        self.assertTrue(len(before) > 0, 'Contact not found')
        print(f'Deleting contact: {target.display_name}')
        api.delete(org_id=org_id, contact_id=target.contact_id)
        after = list(api.list(org_id=org_id, keyword=target.display_name))
        self.assertEqual(len(before) - 1, len(after), 'Contact not deleted')

    def test_008_bulk_delete(self):
        """
        Bulk delete test contacts
        """
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.int_api.org_contacts
        while True:
            contacts = [contact for contact in api.list(org_id=org_id)
                        if contact.company_name == 'Test Company']
            if not contacts:
                break
            api.bulk_delete(org_id=org_id, object_ids=[contact.contact_id for contact in contacts])
