import re
from contextlib import contextmanager
from itertools import zip_longest

from tests.base import TestCaseWithLog, LoggedRequest
from wxc_sdk.common import AuthCode
from wxc_sdk.rest import RestError


class TestOrgAccessCodes(TestCaseWithLog):
    proxy = False

    def create_codes(self, number_of_access_codes: int = 100000, batch_size: int = 10000,
                     with_logging: bool = False) -> list[AuthCode]:
        """
        create org level access codes
        :param number_of_access_codes: target number of access codes.
            If less than zero then create -number_of_access_codes
        :param batch_size: batch size for access code creation
        :param with_logging: w/ or w/o logging
        """

        @contextmanager
        def log_context():
            if with_logging:
                yield None
                return
            with self.no_log():
                yield None

        with log_context():
            codes_before = list(self.api.telephony.organisation_access_codes.list())
            existing_codes = set(ac.code for ac in codes_before)
            if 0 < number_of_access_codes <= len(existing_codes):
                return
            new_codes = (AuthCode(code=c, description=f'auth code {c}')
                         for i in range(1, 110000)
                         if (c := f'1{i:06}') not in existing_codes)
            # these are the access codes we need to create
            if number_of_access_codes < 0:
                missing = - number_of_access_codes
            else:
                missing = number_of_access_codes - len(existing_codes)
            to_create = [next(new_codes) for _ in range(missing)]
            nci = iter(to_create)
            batches = [[ac for ac in b if ac is not None]
                       for b in zip_longest(*([nci] * batch_size))]
            api = self.api.telephony.organisation_access_codes
            for batch in batches:
                api.create(access_codes=[ac for ac in batch if ac is not None])
        return codes_before

    def print_requests(self) -> list[LoggedRequest]:
        requests = list(self.requests(method='GET', url_filter='.*/v1/telephony/config/outgoingPermission/accessCodes'))
        print(f'{len(requests)} requests')
        for request in requests:
            print(f'GET {request.url}, {request.time_ms:.03f} ms, '
                  f'{len(request.response_body["accessCodes"])} access codes')
        return requests

    def test_list(self):
        """
        list access codes and check pagination
        """
        access_codes = list(self.api.telephony.organisation_access_codes.list())
        print(f'{len(access_codes)} access codes')
        self.print_requests()

    def test_create(self):
        """
        Create some access codes
        """
        to_create = 1000
        existing = self.create_codes(number_of_access_codes=-to_create, with_logging=True)
        access_codes_after = list(self.api.telephony.organisation_access_codes.list())
        self.assertEqual(len(existing) + to_create, len(access_codes_after))
        print(f'before: {len(existing)} codes, after: {len(access_codes_after)} codes')

    def test_create_100k(self):
        """
        Create 100k access codes
        """
        self.create_codes(number_of_access_codes=100000, batch_size=10000, with_logging=True)
        codes = list(self.api.telephony.organisation_access_codes.list())
        self.assertEqual(100000, len(codes))

    def test_create_too_many(self):
        """
        Try to create to many access codes in one request
        """
        api = self.api.telephony.organisation_access_codes
        with self.assertRaises(RestError) as re:
            api.create(access_codes=[AuthCode(code=f'9{i:06}', description='foo') for i in range(1, 10002)])
        rest_error: RestError = re.exception
        self.assertEqual(rest_error.response.status_code, 400)
        self.assertEqual(rest_error.code, 25085)

    def test_pagination(self):
        """
        Create access codes and see if we ever get pagination on list()
        """
        api = self.api.telephony.organisation_access_codes
        before = self.create_codes(number_of_access_codes=100000, with_logging=False)
        try:
            if len(before) != 100000:
                list(api.list())
            requests = self.print_requests()
            print(f'{len(requests)} requests')
            self.assertTrue(len(requests) > 1)
        finally:
            ...

    def delete_codes(self, batch_size: int = 10000):
        """
        Delete all auth codes in batche with given size
        :param batch_size:
        :return:
        """
        api = self.api.telephony.organisation_access_codes
        existing = list(api.list())
        ex_iter = iter(existing)
        batches = [b for b in zip_longest(*([ex_iter] * batch_size))]
        for batch in batches:
            api.delete([ac.code for ac in batch if ac])
        after = list(api.list())

        # print summary of delete codes requests
        requests = [r
                    for r in self.requests(method='PUT',
                                           url_filter=re.compile('.*/v1/telephony/config/outgoingPermission/'
                                                                 'accessCodes'))]
        print(f'{len(requests)} requests')
        for request in requests:
            print(f'{request.method} {request.url}, {request.time_ms:.03f} ms, '
                  f'{len(request.request_body["deleteCodes"])} access codes')
        self.assertTrue(not after)

    def test_delete_all_10k_batches(self):
        """
        Delete all access codes in batches of 10k
        """
        self.delete_codes(batch_size=10000)

    def test_delete_all_2k_batches(self):
        """
        Delete all access codes in batches of 2000
        """
        self.delete_codes(batch_size=2000)

    def test_create_conflicting(self):
        """
        create some conflicting access codes
        """
        ...

    def test_delete(self):
        """
        Delete some access codes
        """
        ...

    def test_delete_non_existing(self):
        """
        Delete access codes that dom't exist
        """
        ...

    def test_time_create_max_number_of_access_codes(self):
        """
        Create 10 k access codes and time it
        """
        ...
