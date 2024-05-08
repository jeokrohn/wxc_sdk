from itertools import zip_longest
from operator import attrgetter

from tests.base import TestCaseWithLog, LoggedRequest, async_test
from wxc_sdk.common import AuthCode
from wxc_sdk.rest import RestError


class TestOrgAccessCodes(TestCaseWithLog):

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
        access_codes =  list(self.api.telephony.organisation_access_codes.list())
        print(f'{len(access_codes)} access codes')
        self.print_requests()

    def test_create(self):
        """
        Create some access codes
        """
        api = self.api.telephony.organisation_access_codes

        existing = set(ac.code for ac in self.api.telephony.organisation_access_codes.list())
        new_codes = (AuthCode(code=c, description=f'auth code {c}')
                     for i in range(1, 110000)
                     if (c := f'1{i:06}') not in existing)

        to_create = [next(new_codes) for i in range(1000)]
        api.create(access_codes=to_create)
        access_codes_after = list(self.api.telephony.organisation_access_codes.list())
        self.assertEqual(len(existing) + len(to_create), len(access_codes_after))
        codes = set(map(attrgetter('code'), access_codes_after))
        missing = [ac for ac in to_create if ac.code not in codes]
        if missing:
            print('Missing codes:')
            print('\n'.join(f'* {m.code}' for m in missing))
        self.assertFalse(missing)

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

        existing = set(ac.code for ac in api.list())
        new_codes = (AuthCode(code=c, description=f'auth code {c}')
                     for i in range(1, 200000)
                     if (c := f'1{i:06}') not in existing)
        to_create = [next(new_codes) for _ in range(100000 - len(existing))]
        nci = iter(to_create)
        batches = [b for b in zip_longest(*([nci] * 10000))]
        for batch in batches:
            api.create(access_codes=[ac for ac in batch if ac is not None])
        try:
            list(api.list())
            requests = self.print_requests()
            self.assertFalse(not requests)
        finally:
            # cleanup
            for batch in batches:
                api.delete(delete_codes=[ac.code for ac in batch if ac is not None])

    def test_delete_all(self):
        api = self.api.telephony.organisation_access_codes
        existing = list(api.list())
        ex_iter = iter(existing)
        batch_size = 2000
        batches = [b for b in zip_longest(*([ex_iter] * 2000))]
        for batch in batches:
            api.delete([ac.code for ac in batch if ac])
        after = list(api.list())
        self.assertTrue(not after)

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
