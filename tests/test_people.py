from .base import TestCaseWithLog
import time

from contextlib import contextmanager


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

    def test_002_list_all(self):
        with time_it('listing people w/ calling data'):
            people_list = list(self.api.people.list(calling_data=True))
        print(f'got {len(people_list)} users')

    def test_003_list_all_compare(self):
        with time_it('listing people w/o calling data'):
            list(self.api.people.list())
        with time_it(' listing people w/ calling data'):
            list(self.api.people.list(calling_data=True))
