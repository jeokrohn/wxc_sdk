from .base import TestCaseWithLog


class TestLocation(TestCaseWithLog):

    def test_001_list_all(self):
        location_list = list(self.api.locations.list())
        print(f'Got {len(location_list)} locations')
