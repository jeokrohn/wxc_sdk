"""
Test for person numbers
"""
import asyncio
import functools
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass, field
from functools import reduce
from operator import attrgetter
from random import choice
from time import sleep
from typing import ClassVar

from tests.base import TestCaseWithUsers, async_test, TestWithLocations, TestCaseWithLog
from tests.testutil import LocationInfo, us_location_info, available_tns, random_users, as_available_tns, \
    get_calling_license, available_extensions
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import PatternAction, RingPattern, OwnerType
from wxc_sdk.licenses import LicenseRequest, LicenseProperties
from wxc_sdk.locations import Location
from wxc_sdk.people import Person, PhoneNumber, PhoneNumberType
from wxc_sdk.person_settings.available_numbers import AvailablePhoneNumberLicenseType
from wxc_sdk.person_settings.numbers import UpdatePersonNumbers, UpdatePersonPhoneNumber, PersonNumbers
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.location import TelephonyLocation


class TestRead(TestCaseWithUsers):

    @async_test
    async def test_001_read_all(self):
        """
        Read numbers all users
        """
        nu = self.async_api.person_settings.numbers

        numbers = await asyncio.gather(*[nu.read(person_id=user.person_id) for user in self.users])
        print(f'Got numbers for {len(self.users)} users')

    @async_test
    async def test_002_direct_number_format(self):
        """
        Read numbers all users, verify number format for direct number
        """
        nu = self.async_api.person_settings.numbers

        numbers = await asyncio.gather(*[nu.read(person_id=user.person_id) for user in self.users])

        # validate by looking at the actual response data, b/c +E.164 is enforced in the model
        requests = list(self.requests(method='GET', url_filter=r'.+people/(?P<user_id>\w+)/features/numbers'))
        err = False
        user_dict = {user.person_id: user for user in self.users}
        for request in requests:
            user = user_dict[request.url_dict['user_id']]
            direct_numbers = [dn for pn in request.response_body['phoneNumbers']
                              if (dn := pn.get('directNumber'))]
            non_e14 = [n for n in direct_numbers
                       if not n.startswith('+')]
            if non_e14:
                err = True
                print(f'{user.display_name}: {", ".join(direct_numbers)}')
        self.assertFalse(err, 'Some direct numbers are not +E.164')

    @async_test
    async def test_003_test_prefer_e164(self):
        """
        Does the prefer_e164_format actually have any impact?
        """
        nu = self.async_api.person_settings.numbers

        numbers_no_preference, numbers_e164_false, numbers_e164_true = await asyncio.gather(
            asyncio.gather(*[nu.read(person_id=user.person_id) for user in self.users]),
            asyncio.gather(*[nu.read(person_id=user.person_id, prefer_e164_format=False) for user in self.users]),
            asyncio.gather(*[nu.read(person_id=user.person_id, prefer_e164_format=True) for user in self.users]))
        numbers_no_preference: list[PersonNumbers]
        numbers_e164_false: list[PersonNumbers]
        numbers_e164_true: list[PersonNumbers]
        diffs = [(user, n, n_true, n_false) for user, n, n_true, n_false in
                 zip(self.users, numbers_no_preference, numbers_e164_true, numbers_e164_false)
                 if n != n_true or n != n_false]
        self.assertFalse(not diffs, 'apparently prefer_e164_format does not change anything?')


@dataclass(init=False)
class PhoneNumbersAndExtensions(TestCaseWithUsers, TestWithLocations):
    target_location: Location = None
    new_tn: str = None
    new_extension: str = None
    routing_prefix: str = None
    new_user: Person = None

    def setUp(self) -> None:
        """
        Create a calling user with TN and extension
        """

        async def as_setup():
            async with AsWebexSimpleApi(tokens=self.api.access_token) as as_api:
                # pick random calling location
                self.target_location = choice(self.locations)
                print(f'Target location "{self.target_location.name}"')

                # figure out the NPA of the existing phone numbers
                with self.no_log():
                    existing_tns = self.api.telephony.phone_numbers(location_id=self.target_location.location_id,
                                                                    number_type=NumberType.number)

                # take the NPA from the 1st phone number
                npa = next((n.phone_number[2:5] for n in existing_tns), None)
                if npa is None:
                    self.skipTest(
                        f'Couldn\'t figure out the NPA for target location "{self.target_location.name}": no existing '
                        f'TNs')

                with self.no_log():
                    # get random user
                    random_user = (await random_users(api=as_api, user_count=1))[0]

                    # determine calling license id
                    calling_license_id = get_calling_license(api=self.api)

                    # we also need a new extension
                    self.new_extension = \
                        available_extensions(api=self.api, location_id=self.target_location.location_id)[0]

                    # need routing prefix
                    self.routing_prefix = self.api.telephony.location.details(
                        location_id=self.target_location.location_id).routing_prefix

                # create user
                self.new_user = self.api.people.create(
                    settings=Person(emails=[random_user.email],
                                    display_name=random_user.display_name,
                                    first_name=random_user.name.first,
                                    last_name=random_user.name.last))
                print(f'Created new user "{self.new_user.display_name}"')

                # add a new TN to the calling location (inactive)
                with self.no_log():
                    self.new_tn = (await as_available_tns(as_api=as_api, tn_prefix=npa))[0]
                self.api.telephony.location.number.add(location_id=self.target_location.location_id,
                                                       phone_numbers=[self.new_tn])
                print(f'Added {self.new_tn} to "{self.target_location.name}"')

                # update user: add calling license and set work phone number
                self.new_user.licenses.append(calling_license_id)
                self.new_user.location_id = self.target_location.location_id
                self.new_user.phone_numbers = [
                    PhoneNumber(type=PhoneNumberType.work,
                                value=self.new_tn[2:])]
                self.new_user.extension = f'{self.new_extension}'
                self.new_user = self.api.people.update(person=self.new_user, calling_data=True)
                print(f'Enabled "{self.new_user.display_name}" for calling with TN {self.new_tn} '
                      f'and extension {self.new_extension}')

        super().setUp()
        asyncio.run(as_setup())

    def tearDown(self) -> None:
        """
        cleanup after test
        """
        try:
            if self.new_user:
                self.api.people.delete_person(person_id=self.new_user.person_id)
                print(f'Deleted user "{self.new_user.display_name}"')

            if self.new_tn:
                # after deleting the user it might take some time until we can delete the TN again
                for i in range(3):
                    try:
                        self.api.telephony.location.number.remove(location_id=self.target_location.location_id,
                                                                  phone_numbers=[self.new_tn])
                    except RestError as e:
                        if e.response.status_code == 502:
                            print(f'Removing {self.new_tn} failed. Wait for some time and retry...')
                            sleep(10)
                            continue
                    else:
                        print(f'Removed {self.new_tn} from "{self.target_location.name}"')
                        break
                else:
                    raise e
        finally:
            super().tearDown()

    def assert_tn_and_extension(self, work: str, extension: str):
        """
        Validate work number and extension of user
        """
        details = self.api.people.details(person_id=self.new_user.person_id)
        number = next((pn.value for pn in details.phone_numbers
                       if pn.number_type == PhoneNumberType.work), None)
        self.assertEqual(work, number, 'work number wrong')
        number = next((pn.value for pn in details.phone_numbers
                       if pn.number_type == PhoneNumberType.work_extension), None)
        if extension:
            self.assertEqual(f'{self.routing_prefix}{extension}', number, 'Unexpected work extension')
        else:
            self.assertIsNone(number, 'Unexpected work extension')

        person_numbers = self.api.person_settings.numbers.read(person_id=self.new_user.person_id)
        primary = next((pn for pn in person_numbers.phone_numbers if pn.primary), None)
        self.assertIsNotNone(primary, 'No primary number present for user')
        self.assertEqual(extension, primary.extension, 'Unexpected extension in person numbers')
        self.assertEqual(work, primary.direct_number, 'Unexpected TN in person numbers')

    def test_001_create_new_calling_user(self):
        """
        Create a new calling enabled user with a TN in an existing location
        """
        self.assert_tn_and_extension(work=self.new_tn, extension=self.new_extension)

    def test_002_remove_work_number(self):
        """
        Try to remove TN from user
        """
        # try to remove work number from user
        details = self.api.people.details(person_id=self.new_user.person_id)
        update = details.model_copy(deep=True)
        update.phone_numbers = None
        update.extension = self.new_extension
        after = self.api.people.update(person=update, calling_data=True)
        self.assertFalse(after.errors)
        print(f'removed TN {self.new_tn} from user "{self.new_user.display_name}"')

        # work number should be gone
        self.assert_tn_and_extension(work=None, extension=self.new_extension)


class TestCreateCallingUser(TestWithLocations):
    """
    Two tests around calling users
        * create calling user w/ extension
        * create calling user w/ extension and then update extension
    """

    @asynccontextmanager
    async def generate_temp_user_with_extension(self) -> tuple[Location, str, Person]:
        """
        Generate a temp test user, enable that user for calling with extension in location and validate
        yields target location, extension, and generated user
        """
        # pick random calling location
        target_location = choice(self.locations)
        print(f'Target location "{target_location.name}"')
        target_location_calling = self.api.telephony.location.details(location_id=target_location.location_id)

        with self.no_log():
            # we need an extension for the new user
            extension = available_extensions(api=self.api, location_id=target_location.location_id)[0]

            # get random user
            random_user = (await random_users(api=self.async_api, user_count=1))[0]

            # determine calling license id
            calling_license_id = get_calling_license(api=self.api)

        # create user
        new_user = self.api.people.create(
            settings=Person(emails=[random_user.email],
                            display_name=random_user.display_name,
                            first_name=random_user.name.first,
                            last_name=random_user.name.last))
        print(f'Created new user "{new_user.display_name}"')
        try:
            license_response = self.api.licenses.assign_licenses_to_users(
                person_id=new_user.person_id,
                licenses=[LicenseRequest(id=calling_license_id,
                                         properties=LicenseProperties(location_id=target_location.location_id,
                                                                      extension=extension))])
            print(f'Enabled "{new_user.display_name}" for calling with extension {extension}')
            print('License response')
            print(json.dumps(license_response.model_dump(mode='json', exclude_none=True, by_alias=True), indent=2))

            # get user details to check phone number setting
            user_after = self.api.people.details(person_id=new_user.person_id, calling_data=True)

            # calling license has to be present
            self.assertTrue(calling_license_id in user_after.licenses,
                            'Calling license not present in user after update')
            # user should only have one phone number
            self.assertEqual(1, len(user_after.phone_numbers),
                             'Expected exactly one user phone number')
            # .. a work extension
            self.assertEqual(PhoneNumberType.work_extension, user_after.phone_numbers[0].number_type,
                             'Phone number type should be work extension')
            # .. where the value is the concatenation of the site code and the extension
            pn_value = user_after.phone_numbers[0].value

            if target_location_calling.routing_prefix:
                self.assertEqual(f'{target_location_calling.routing_prefix}{extension}', pn_value,
                                 'wrong ESN')
            else:
                self.assertEqual(extension, pn_value,
                                 'wrong extension')

            # .. the phone number should be the primary number
            self.assertTrue(user_after.phone_numbers[0].primary,
                            'phone number should be primary')

            # also the extension should now exist as number in the location
            numbers_after = list(self.api.telephony.phone_numbers(location_id=target_location.location_id,
                                                                  extension=extension))

            self.assertEqual(1, len(numbers_after),
                             'Expected exactly one result when searching for extension on location')
            number = numbers_after[0]
            self.assertEqual(extension, number.extension,
                             'Wrong extension')
            self.assertIsNotNone(number.owner,
                                 'number has to have an owner')
            owner = number.owner
            self.assertEqual(OwnerType.people, owner.owner_type)
            self.assertEqual(new_user.person_id, owner.owner_id)

            self.assertEqual(target_location.location_id, number.location.id,
                             'Unexpected location id')
            yield target_location, extension, user_after, target_location_calling

        finally:
            self.api.people.delete_person(person_id=new_user.person_id)
            print(f'deleted "{new_user.display_name}"')
            # extension should not exist any more
            numbers_after = list(self.api.telephony.phone_numbers(location_id=target_location.location_id,
                                                                  extension=extension))
            self.assertEqual(0, len(numbers_after))

    @async_test
    async def test_create_user_and_update_license(self):
        """
        Create a user, update the calling license, set extension and check consistency
        """
        async with self.generate_temp_user_with_extension():
            pass

    @async_test
    async def test_create_calling_user_and_change_extension(self):
        """
        create a calling user with an extension, change extension and check consistency
        :return:
        """
        async with self.generate_temp_user_with_extension() as ctx:
            target_location, extension, new_user, telephony_location = ctx
            target_location: Location
            extension: str
            new_user: Person
            telephony_location: TelephonyLocation
            # get an available extension in location
            with self.no_log():
                new_extension = available_extensions(api=self.api, location_id=target_location.location_id)[0]
            new_work_extension = new_extension
            if telephony_location.routing_prefix:
                new_work_extension = f'{telephony_location.routing_prefix}{new_work_extension}'

            # try to assign the new extension
            person_settings = new_user.model_copy(deep=True)
            person_settings.phone_numbers = [PhoneNumber(type=PhoneNumberType.work_extension,
                                                         value=new_work_extension,
                                                         primary=True)]
            person_settings.extension = new_extension
            updated_user = self.api.people.update(person=person_settings, calling_data=True)

            # user should only have one phone number
            self.assertEqual(1, len(updated_user.phone_numbers),
                             'Expected exactly one user phone number')
            # .. a work extension
            self.assertEqual(PhoneNumberType.work_extension, updated_user.phone_numbers[0].number_type,
                             'Phone number type should be work extension')
            # .. where the value is the concatenation of the site code and the extension
            pn_value = updated_user.phone_numbers[0].value

            if telephony_location.routing_prefix:
                self.assertEqual(new_work_extension, pn_value,
                                 'wrong ESN')
            else:
                self.assertEqual(new_extension, pn_value,
                                 'wrong extension')

            self.assertEqual(new_extension, updated_user.extension, 'wrong extension')
            # .. the phone number should be the primary number
            self.assertTrue(updated_user.phone_numbers[0].primary,
                            'phone number should be primary')

            # old extension does not exist in location any more
            numbers = list(self.api.telephony.phone_numbers(location_id=target_location.location_id,
                                                            number_type=NumberType.extension))
            self.assertIsNone(next((n for n in numbers if n.extension == extension), None))
            # new extension should exist in location
            number = next((n for n in numbers if n.extension == new_extension), None)
            self.assertIsNotNone(number)
            self.assertIsNotNone(number.owner)
            self.assertEqual(new_user.person_id, number.owner.owner_id)


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):
    """
    Assign and un-assign alternate numbers to person
    """
    us_locations: ClassVar[list[LocationInfo]]
    us_users: list[Person] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.us_locations = us_location_info(api=cls.api)

    def setUp(self) -> None:
        super().setUp()
        if not self.us_locations:
            self.skipTest('Need US locations with numbers to run the test')
        us_location_ids = set(loc.location.location_id for loc in self.us_locations)
        self.us_users = [u for u in self.users
                         if u.location_id in us_location_ids]
        if not self.us_users:
            self.skipTest('Need some US calling users to run the test')

    @contextmanager
    def update_user_context(self):
        # pick a US calling user
        user = choice(self.users)
        location_info = next((loc_info for loc_info in self.us_locations
                              if loc_info.location.location_id == user.location_id), None)
        self.assertIsNotNone(location_info)
        print(f'Testing with user {user.display_name}({user.emails[0]}) in location "{location_info.location.name}"')

        # current numbers of the user
        numbers = self.api.person_settings.numbers.read(person_id=user.person_id)

        # some available TNs in the location
        available_tns_in_location = [n.phone_number for n in location_info.numbers
                                     if not n.owner and not n.main_number]
        new_tn = None
        if not available_tns_in_location:
            new_tn = available_tns(api=self.api, tn_prefix=location_info.main_number[:5], tns_requested=3)[0]
            tn = new_tn
        else:
            # pick a random TN
            tn = choice(available_tns_in_location)
        if new_tn:
            print(f'Temporarily adding new number to location "{location_info.location.name}": {tn}')
            self.api.telephony.location.number.add(location_id=location_info.location.location_id,
                                                   phone_numbers=[new_tn])
        try:
            try:
                yield location_info.location, user, numbers, tn
            finally:
                # remove TN again
                print(f'Removing {tn} from user {user.display_name}({user.emails[0]}) '
                      f'in location "{location_info.location.name}"')
                update = UpdatePersonNumbers(enable_distinctive_ring_pattern=numbers.distinctive_ring_enabled,
                                             phone_numbers=[
                                                 UpdatePersonPhoneNumber(action=PatternAction.delete,
                                                                         external=tn)])
                self.api.person_settings.numbers.update(person_id=user.person_id,
                                                        update=update)
                numbers_after = self.api.person_settings.numbers.read(person_id=user.person_id)
                self.assertEqual(numbers, numbers_after)
        finally:
            # remove new TN (if needed)
            if new_tn:
                print(f'Removing number from location "{location_info.location.name}": {tn}')
                self.api.telephony.location.number.remove(location_id=location_info.location.location_id,
                                                          phone_numbers=[new_tn])

    def test_001_update_add_tn(self):
        """
        Try to add an alternate TN to a user
        """
        with self.update_user_context() as ctx:
            location, user, numbers, tn = ctx
            location: Location
            user: Person
            numbers: PersonNumbers
            tn: str

            print(f'Adding {tn} to user {user.display_name}({user.emails[0]}) '
                  f'in location "{location.name}"')
            ring_pattern = RingPattern.short_short_long
            update = UpdatePersonNumbers(enable_distinctive_ring_pattern=True,
                                         phone_numbers=[
                                             UpdatePersonPhoneNumber(action=PatternAction.add,
                                                                     external=tn,
                                                                     ring_pattern=ring_pattern)])
            self.api.person_settings.numbers.update(person_id=user.person_id,
                                                    update=update)
            # validation
            numbers_after = self.api.person_settings.numbers.read(person_id=user.person_id)
            self.assertEqual(True, numbers_after.distinctive_ring_enabled)
            for i, pn in enumerate(numbers.phone_numbers):
                self.assertEqual(pn, numbers_after.phone_numbers[i])
            pn = numbers_after.phone_numbers[-1]
            self.assertEqual(False, pn.primary)
            self.assertIsNone(pn.extension)
            self.assertEqual(tn, pn.direct_number)
            self.assertEqual(ring_pattern, pn.ring_pattern)


class TestAvailableNumbers(TestCaseWithUsers):
    @async_test
    async def test_primary_license_type(self):
        api = self.async_api.person_settings.available_numbers
        await asyncio.gather(*[api.primary(license_type=lt) for
                               lt in AvailablePhoneNumberLicenseType])


@dataclass(init=False)
class TestUserLocationConsistency(TestCaseWithLog):
    numbers: ClassVar[list[NumberListPhoneNumber]]
    numbers_by_owner_id: ClassVar[dict[str, list[NumberListPhoneNumber]]]
    users: ClassVar[dict[str, Person]]
    locations: ClassVar[dict[str, Location]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.numbers = list(cls.api.telephony.phone_numbers(owner_type=OwnerType.people))
        cls.numbers_by_owner_id = reduce(lambda acc, n: acc[n.owner.owner_id].append(n) or acc,
                                         cls.numbers, defaultdict(list))
        # get all users that have numbers
        owner_ids = {n.owner.owner_id for n in cls.numbers}
        with ThreadPoolExecutor() as pool:
            users = list(pool.map(functools.partial(cls.api.people.details, calling_data=True), owner_ids))
        cls.users = {u.person_id: u for u in users}
        cls.locations = {l.location_id: l for l in cls.api.locations.list()}

    """
    See if location information at the user level is consistent with location info on primary numbers of users
    """
    @staticmethod
    def user_str(u: Person) -> str:
        return f'{u.display_name}({u.emails[0]})'

    def test_single_location_per_user_in_numbers(self):
        """
        Make sure that all number owned by a user are in the same location
        """
        location_ids_by_owner_id: dict[str, set[str]] = reduce(
            lambda acc, n: acc[n.owner.owner_id].add(n.location.id) or acc,
            self.numbers, defaultdict(set))

        user_len = max(len(self.user_str(user)) for user in self.users.values())
        for user_id in sorted(location_ids_by_owner_id, key=lambda k: self.users[k].display_name):
            user = self.users[user_id]
            numbers = self.numbers_by_owner_id[user_id]
            location_ids = location_ids_by_owner_id[user_id]
            print(f'{self.user_str(user):{user_len}}: {len(numbers)} number(s) in location(s) '
                  f'{", ".join(self.locations[l].name for l in location_ids)}')
            self.assertEqual(location_ids, {n.location.id for n in numbers}, 'Inconsistent location IDs')
            self.assertEqual(1, len(location_ids), 'User has numbers in multiple locations')

    def test_consistent_location_in_user_info(self):
        err = None
        user_len = max(len(self.user_str(user)) for user in self.users.values())
        for user in sorted(self.users.values(), key=attrgetter('display_name')):
            try:
                user_location = self.locations[user.location_id]
            except KeyError as e:
                print(f'{self.user_str(user):{user_len}}: location not found, id: '
                      f'{user.location_id}/{webex_id_to_uuid(user.location_id)}')
                err = err or e
                continue
            numbers = self.numbers_by_owner_id[user.person_id]
            # use the 1st location id. Technically, if a user has multiple numbers, they should all be in the same
            # location (see other test)
            number_location_id = next(n.location.id for n in numbers)
            if number_location_id == user.location_id:
                continue
            number_location = self.locations[number_location_id]
            print(f'{self.user_str(user):{user_len}}: '
                  f'user location: "{user_location.name}", number location: "{number_location.name}"')
            try:
                self.assertEqual(user_location, number_location, 'Different location information')
            except AssertionError as e:
                err = err or e
        if err:
            raise err
