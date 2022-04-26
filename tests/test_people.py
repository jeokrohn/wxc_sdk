import time
from contextlib import contextmanager
from unittest import skip

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
