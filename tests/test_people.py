import json
import os
import re
import time
import uuid
from contextlib import contextmanager
from itertools import chain
from unittest import skip

from dotenv import load_dotenv

from wxc_sdk.people import Person
from wxc_sdk.rest import RestError
from .base import TestCaseWithLog


@contextmanager
def time_it(message: str = None):
    if message:
        message = f'{message} took: '
    else:
        message = ''
    try:
        start_time = time.perf_counter()
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

        # get all users with emails derived from base email defined in .eenv
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
        print(json.dumps(json.loads(new_user.json()), indent=2))

        # clean up: delete the user again
        self.api.people.delete_person(person_id=new_user.person_id)
