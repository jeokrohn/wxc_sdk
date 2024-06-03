import asyncio
import json
import os
import re
import time
from contextlib import contextmanager
from itertools import chain
from random import choice
from unittest import skip

from dotenv import load_dotenv

from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import RouteType
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.person_settings.numbers import PersonNumbers
from wxc_sdk.rest import RestError
from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import calling_users, create_random_calling_user
from wxc_sdk.telephony.location import TelephonyLocation


@contextmanager
def time_it(message: str = None):
    if message:
        message = f'{message} took: '
    else:
        message = ''
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f'{message}{elapsed * 1000:.3f} ms')


class TestPeople(TestCaseWithLog):

    def test_001_list_all(self):
        with time_it('listing people w/o calling data'):
            people_list = list(self.api.people.list())
        print(f'got {len(people_list)} users')

    def test_002_list_all_w_callingdata(self):
        with time_it('listing people w/ calling data'):
            people_list = list(self.api.people.list(calling_data=True))
        print(f'got {len(people_list)} users')

    def test_003_list_all_compare(self):
        with time_it('listing people w/o calling data'):
            list(self.api.people.list())
        with time_it(' listing people w/ calling data'):
            list(self.api.people.list(calling_data=True))

    @skip('Too slow...')
    def test_004_list_all_w_calling_data_find_max(self):
        people = self.api.people
        users = list(people.list())
        lower = 0
        upper = len(users)
        page_size = upper
        while True:
            try:
                print(f'lower: {lower} page size: {page_size} upper: {upper}')
                list(people.list(calling_data=True, max=page_size))
            except RestError as error:
                if error.response.status_code != 504:
                    raise
                print('--> failed with 504 (timeout)')
                upper = page_size
                if (page_size - lower) < 2:
                    page_size = lower
                    break
                page_size = int((lower + page_size) / 2)
            else:
                print('--> worked')
                lower = page_size
                if (upper - page_size) < 2:
                    break
                page_size = int((page_size + upper) / 2)
        print(f'Maximum page size: {page_size} ')

    def test_005_create_user(self):
        """
        Try to create a test user
        """

        # get all users with emails derived from base email defined in .env
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path=dotenv_path)

        base_email = os.getenv('BASE_EMAIL').split('@')
        # RE to find all emails in the form user+foo@domain
        email_re = re.compile(f'{base_email[0]}\+.+@{base_email[1]}')

        # users with email matching that re
        test_users = [user for user in self.api.people.list()
                      if any(email_re.match(email) for email in user.emails)]

        # set of all used emails
        emails = set(chain.from_iterable(u.emails for u in test_users))

        # get available email and user index
        index, email = next((index, email) for index in range(1, 1000)
                            if (email := f'{base_email[0]}+test{index:03}@{base_email[1]}') not in emails)

        # create user
        settings = Person(first_name='test', last_name=f'foo{index:03}', emails=[email])
        new_user = self.api.people.create(settings=settings)
        print(f'Created new user: {settings.first_name} {settings.last_name} {settings.emails[0]}')
        print(json.dumps(json.loads(new_user.model_dump_json()), indent=2))

        # clean up: delete the user again
        self.api.people.delete_person(person_id=new_user.person_id)

    def test_006_list_by_id_and_check_for_user_name(self):
        users = list(self.api.people.list())
        # pick a random user
        target = choice(users)
        # list by is
        by_id = list(self.api.people.list(id_list=[target.person_id]))
        list_requests = list(self.requests(method='GET', url_filter='https://webexapis.com/v1/people.*'))
        # first list request doesn't have 'userName'
        self.assertTrue(all('userName' not in item for item in list_requests[0].response_body.get('items')),
                        'userName returned in \'regular\' list')
        # second request has 'userName'
        self.assertTrue(all('userName' in item for item in list_requests[1].response_body.get('items')),
                        'list by id doesn\'t return userName')

    @async_test
    async def test_007_get_details_by_uuid(self):
        """
        Get details for all users, but use UUID as user id in the request
        """
        users = list(self.api.people.list())
        details_list = await asyncio.gather(*[self.async_api.people.details(person_id=webex_id_to_uuid(user.person_id))
                                              for user in users])
        print(f'Got details for {len(details_list)} users')


class TestPeoplePhoneNumbers(TestCaseWithLog):
    """
    Take a look at people phone numbers
    """

    @async_test
    async def test_001_show_numbers(self):
        users = calling_users(api=self.api)

        async def user_info(user: Person) -> tuple[Person, PersonNumbers]:
            return await asyncio.gather(self.async_api.people.details(person_id=user.person_id, calling_data=True),
                                        self.async_api.person_settings.numbers.read(person_id=user.person_id))

        numbers, details_and_number_list = await asyncio.gather(
            self.async_api.telephony.phone_numbers(),
            asyncio.gather(*[user_info(user) for user in users]))
        user_details, user_numbers = zip(*details_and_number_list)
        err = False
        for person, person_numbers in zip(user_details, user_numbers):
            person: Person
            person_numbers: PersonNumbers
            person_error = False
            print(f'{person.display_name}:', end='')
            if len(person.phone_numbers) != len(person_numbers.phone_numbers):
                person_error = True
                print(f' different # of phone numbers via person API and person_settings '
                      f'({len(person.phone_numbers)} != {len(person_numbers.phone_numbers)})')
                extensions = [pn.extension for pn in person_numbers.phone_numbers
                              if pn.extension]
                direct_numbers = [pn.direct_number for pn in person_numbers.phone_numbers
                                  if pn.direct_number]
                person_phone_numbers = [pn.value for pn in person.phone_numbers]
                extensions_not_in_person = [ext for ext in extensions
                                            if ext not in person_phone_numbers]
                if extensions_not_in_person:
                    print(f' extensions not in person data: {", ".join(extensions_not_in_person)}')
                direct_numbers_not_in_person = [dn for dn in direct_numbers
                                                if dn not in person_phone_numbers]
                if direct_numbers_not_in_person:
                    print(f' direct numbers no in person data: {", ".join(direct_numbers_not_in_person)}')
                person_phone_number_not_in_person_settings = [p for p in person_phone_numbers
                                                              if p not in extensions and p not in direct_numbers]
                if person_phone_number_not_in_person_settings:
                    print(f'  person phone numbers not an extension or direct number: '
                          f'{", ".join(person_phone_number_not_in_person_settings)}', end='')

                    # some numbers might actually end with an extension: these probably are ESN?
                    person_phone_numbers_esn = [p for p in person_phone_number_not_in_person_settings
                                                if any(p.endswith(ext) for ext in extensions)]
                    if len(person_phone_numbers_esn) == len(person_phone_number_not_in_person_settings):
                        print(', all of them seem to be ESN?')
                    else:
                        print(f', some seem to be not an ESN: '
                              f'{", ".join(p for p in person_phone_number_not_in_person_settings if p not in person_phone_numbers_esn)}')

            if not person_error:
                print(f' ok: {", ".join(pn.value for pn in person.phone_numbers)}')
            err = err or person_error
        self.assertFalse(err, 'Some number issues...')


@skip('Enable if needed to create some random calling users')
class TestCallingUser(TestWithLocations):
    def test_create_random_calling_user(self):
        t_loc: TelephonyLocation
        lgw_locations = [loc for loc, t_loc in zip(self.locations, self.telephony_locations)
                         if t_loc.connection and t_loc.connection.type in {RouteType.trunk, RouteType.route_group}]
        target_location: Location = choice(lgw_locations)
        print(f'Creating new random user in location "{target_location.name}"')
        new_user = create_random_calling_user(api=self.api, location_id=target_location.location_id,
                                              with_tn=True)
        print(new_user)
        print(f'created "{new_user.display_name}"')
        print(json.dumps(new_user.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
