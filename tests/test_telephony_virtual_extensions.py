import asyncio
from collections import defaultdict
from collections.abc import Generator
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from random import choice
from typing import ClassVar

from tests.base import TestWithLocations, WithIntegrationTokens, async_test
from wxc_sdk.all_types import *


@dataclass(init=False)
class TestVirtualExtensionsBase(TestWithLocations, WithIntegrationTokens):
    """
    Base class for virtual extension tests
    """
    available_external_phone_numbers: ClassVar[Generator[str, None, None]] = None
    available_extensions: ClassVar[Generator[str, None, None]] = None
    existing_patterns: ClassVar[set[str]] = set()
    available_patterns: ClassVar[Generator[str, None, None]] = None
    available_range_names: ClassVar[Generator[str, None, None]] = None

    @classmethod
    def setUpClass(cls) -> None:
        # use integration tokens for all tests; we need the Identity:contact scope
        super().setUpClass()
        cls.tokens.access_token = cls.integration_tokens.access_token

        # virtual extensions
        existing_virtual_extensions = list(cls.api.telephony.virtual_extensions.list_extensions())
        phone_numbers = set(ve.phone_number for ve in existing_virtual_extensions)
        cls.available_external_phone_numbers = (pn for i in range(1, 1000)
                                                if (pn := f'+4961007739{i:03}') not in phone_numbers)
        extensions = set(ve.extension for ve in existing_virtual_extensions)
        cls.available_extensions = (str(i) for i in range(3000, 4000) if str(i) not in extensions)

        # ranges
        ve_ranges = list(cls.api.telephony.virtual_extensions.list_range())
        range_names = set(ve_range.name for ve_range in ve_ranges)
        cls.available_range_names = (n for i in range(1, 10000) if (n := f'test_range_{i:04}') not in range_names)
        with ThreadPoolExecutor() as pool:
            ve_range_details = list(
                pool.map(lambda r: cls.api.telephony.virtual_extensions.details_range(r.id), ve_ranges))
        ve_range_details: list[VirtualExtensionRange]
        cls.existing_patterns = set(chain.from_iterable(ve_range.patterns for ve_range in ve_range_details))
        cls.available_patterns = (p for i in range(1, 1000) if (p := f'998{i:03}X') not in cls.existing_patterns)

    @contextmanager
    def dummy_virtual_extensions(self, count: int = 0, assert_count: int = 0) -> Generator[None, None, None]:
        """
        Context manager to create dummy virtual extensions for testing.
        Creates `count` virtual extensions with unique phone numbers and extensions.
        Cleans up by deleting the created extensions after use.
        """
        vapi = self.api.telephony.virtual_extensions

        def create_one() -> str:
            pn = next(self.available_external_phone_numbers)
            ext = next(self.available_extensions)
            display_name = f'test {pn}'
            return vapi.create_extension(display_name=display_name, phone_number=pn,
                                         extension=ext, first_name='test', last_name=ext)

        created = None
        if assert_count:
            with self.no_log():
                ve_list = list(vapi.list_extensions(orgLevelOnly=True))
            if len(ve_list) >= assert_count:
                yield
                return
            count = assert_count - len(ve_list)
        try:
            with self.no_log():
                if count:
                    with ThreadPoolExecutor() as executor:
                        created = list(executor.map(lambda _: create_one(), range(count)))
            yield
        finally:
            with self.no_log():
                if created:
                    with ThreadPoolExecutor() as executor:
                        list(executor.map(lambda ve: vapi.delete_extension(ve), created))
        return


class TestVirtualExtensions(TestVirtualExtensionsBase):

    def test_ext_validate_external_phone_number_errors(self):
        """
        Validate an external phone number that is not available for virtual extensions.
        """
        vapi = self.api.telephony.virtual_extensions
        result = vapi.validate_external_phone_number(['098765678', next(self.available_external_phone_numbers)])
        self.assertEqual(ValidateVirtualExtensionStatus.errors, result.status)
        self.assertEqual(VirtualExtensionValidationStatus.invalid, result.phone_number_status[0].state)
        self.assertEqual(VirtualExtensionValidationStatus.valid, result.phone_number_status[1].state)

    def test_ext_validate_external_phone_number_ok(self):
        """
        Validate an external phone number that is available for virtual extensions.
        """
        vapi = self.api.telephony.virtual_extensions
        result = vapi.validate_external_phone_number([next(self.available_external_phone_numbers)])
        self.assertEqual(ValidateVirtualExtensionStatus.ok, result.status)
        self.assertEqual(0, len(result.phone_number_status))

    def test_ext_org_list(self):
        """
        List all virtual extensions in the organization.
        """
        with self.dummy_virtual_extensions(10):
            virtual_extensions = list(self.api.telephony.virtual_extensions.list_extensions())
            virtual_extensions_max5 = list(self.api.telephony.virtual_extensions.list_extensions(max=5))
        print(f'got {len(virtual_extensions)} virtual extensions')
        print(f'got {len(virtual_extensions_max5)} virtual extensions (max 5)')
        self.assertEqual(len(virtual_extensions_max5), len(virtual_extensions))

    def test_ext_org_create(self):
        """
        Create a virtual extension in the organization.
        """
        vapi = self.api.telephony.virtual_extensions
        phone_number = next(self.available_external_phone_numbers)
        extension = next(self.available_extensions)
        result = vapi.create_extension(display_name=f'test {phone_number}', phone_number=phone_number,
                                       extension=extension,
                                       first_name='test', last_name=extension)
        print(f'created virtual extension: {result}')

    @async_test
    async def test_ext_org_create_async(self):
        """
        Create a bunch of virtual extension asynchronously.
        """
        vapi = self.async_api.telephony.virtual_extensions
        tasks = []
        for _ in range(100):
            pn = next(self.available_external_phone_numbers)
            ext = next(self.available_extensions)
            tasks.append(vapi.create_extension(display_name=f'test {pn}',
                                               phone_number=pn,
                                               extension=ext,
                                               first_name='test', last_name=ext))
        results = await asyncio.gather(*tasks)
        print(f'created {len(results)} virtual extensions')

        requests = list(self.record_log_handler.requests(method='POST'))
        requests_429 = [r for r in requests if r.status == 429]
        err = False
        for request in requests_429:
            headers = list(map(str.lower, request.response_headers))
            if 'retry-after' not in headers:
                err = True
                print(f'got 429 response without Retry-After header: {request.response_headers["Date"]}, {request.url}')
        if err:
            self.fail('got 429 response without Retry-After header')

    def test_ext_create_duplicate_at_location(self):
        """
        Create a duplicate of an org virtual extension at the location level
        """
        # we need at least one org level virtual extension to test this
        with self.dummy_virtual_extensions(0, asssert_count=1):
            vapi = self.api.telephony.virtual_extensions
            ve_list = list(vapi.list_extensions(orgLevelOnly=True))
            org_ve = choice(ve_list)
            location = choice(self.telephony_locations)
            pn = next(self.available_external_phone_numbers)
            try:
                vapi.create_extension(display_name=f'test {pn}',
                                      phone_number=pn,
                                      extension=org_ve.extension, first_name=org_ve.first_name,
                                      last_name=org_ve.last_name,
                                      location_id=location.location_id)
            except:
                raise
        return

    @async_test
    async def test_ext_all_details(self):
        """
        get details of all virtual extensions in the organization
        """
        with self.dummy_virtual_extensions(assert_count=5):
            vapi = self.async_api.telephony.virtual_extensions
            ve_list = await vapi.list_extensions()
            tasks = [vapi.details_extension(ve.id) for ve in ve_list]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        print(f'got details for {len(results)} virtual extensions')
        err = False
        for ve in results:
            if isinstance(ve, Exception):
                err = True
                print(f'Error getting details for virtual extension: {ve}')
            else:
                ve: VirtualExtension
                print(f'Virtual Extension: {ve.display_name}, Phone Number: {ve.phone_number}, '
                      f'Extension: {ve.extension}, Location: {ve.location_name}')
        if err:
            raise Exception('Error getting details for some virtual extensions')
        return

    @async_test
    async def test_ext_zzz_delete_test_virtual_extensions_async(self):
        """
        Delete all test virtual extensions that start with 'test '.
        """
        vapi = self.async_api.telephony.virtual_extensions
        ve_list = await vapi.list_extensions()
        tasks = [vapi.delete_extension(ve.id) for ve in ve_list if ve.display_name.startswith('test ')]
        results = await asyncio.gather(*tasks)
        print(f'deleted {len(results)} virtual extensions')

    @async_test
    async def test_ext_loc_list(self):
        """
        list virtual extensions in all locations
        """
        vapi = self.async_api.telephony.virtual_extensions
        results = await asyncio.gather(*[vapi.list_extensions(location_id=location.location_id)
                                         for location in self.telephony_locations],
                                       return_exceptions=True)
        err = None
        for location, result in zip(self.locations, results):
            location: Location
            if isinstance(result, Exception):
                err = err or result
                print(f'Error for location "{location.name}": {result}')
            else:
                print(f'Location "{location.name}": {len(result)}')
        if err:
            raise err

    @async_test
    async def test_ext_loc_create(self):
        """
        Create some virtual extensions in some locations
        """
        vapi = self.async_api.telephony.virtual_extensions
        tasks = []
        for _ in range(100):
            location = choice(self.locations)
            phone_number = next(self.available_external_phone_numbers)
            extension = next(self.available_extensions)
            tasks.append(vapi.create_extension(display_name=f'test {phone_number}', phone_number=phone_number,
                                               extension=extension,
                                               first_name='test', last_name=extension,
                                               location_id=location.location_id))
        results = await asyncio.gather(*tasks)
        print(f'created {len(results)} virtual extensions')
        ve_list = await vapi.list_extensions()
        print(f'got {len(ve_list)} virtual extensions')

        # group the virtual extensions by location
        ve_by_location: dict[str, list[VirtualExtension]] = reduce(lambda d, ve: d[ve.location_name].append(ve) or d,
                                                                   ve_list, defaultdict(list))
        for location in sorted(map(str, ve_by_location.keys())):
            ves = ve_by_location[location]
            print(f'got {len(ves)} virtual extensions in location "{location}"')

    def test_range_org_list(self):
        """
        List all virtual extension ranges in the organization
        """
        vapi = self.api.telephony.virtual_extensions
        ve_range_list = list(vapi.list_range())
        print(f'got {len(ve_range_list)} virtual extension ranges')

    @async_test
    async def test_range_all_details(self):
        """
        Get details of all virtual extension ranges in the organization
        """
        vapi = self.async_api.telephony.virtual_extensions
        ve_range_list = await vapi.list_range()
        tasks = [vapi.details_range(ve_range.id) for ve_range in ve_range_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(f'got details for {len(results)} virtual extension ranges')
        err = False
        for ve_range in results:
            if isinstance(ve_range, Exception):
                err = True
                print(f'Error getting details for virtual extension range: {ve_range}')
            else:
                ve_range: VirtualExtensionRange
                print(f'Virtual Extension Range: {ve_range.name}, Prefix: {ve_range.prefix}, '
                      f'{len(ve_range.patterns)} Patterns')
        if err:
            raise Exception('Error getting details for some virtual extension ranges')

    def test_range_validate_prefix_not_e164(self):
        """
        Validate a prefix that is not in E.164 format.
        """
        vapi = self.api.telephony.virtual_extensions
        result = vapi.validate_range(name='foo', prefix='100', patterns=[next(self.available_patterns)])
        self.assertEqual(ValidateVirtualExtensionStatus.errors, result.status)
        self.assertEqual(1, len(result.validation_status))

    def test_range_validate_existing_pattern(self):
        """
        Validate a prefix that has an existing pattern.
        """
        if not self.existing_patterns:
            self.skipTest('No existing patterns found for testing')
        vapi = self.api.telephony.virtual_extensions
        result = vapi.validate_range(name='foo', prefix='+496100773', patterns=[list(self.existing_patterns)[0]])
        self.assertEqual(ValidateVirtualExtensionStatus.errors, result.status)

    def test_range_validate_ok(self):
        """
        Validate a prefix that is in E.164 format.
        """
        vapi = self.api.telephony.virtual_extensions
        result = vapi.validate_range(name='foo', prefix='+496100773', patterns=[next(self.available_patterns)])
        self.assertEqual(ValidateVirtualExtensionStatus.ok, result.status)
        self.assertIsNone(result.validation_status)

    def test_range_org_create(self):
        """
        Create a virtual extension range in the organization.
        """
        vapi = self.api.telephony.virtual_extensions
        result = vapi.create_range(name=next(self.available_range_names), prefix='+496100773',
                                   patterns=[next(self.available_patterns) for _ in range(100)])
        print(f'created virtual extension range: {result}')

    @async_test
    async def test_range_zzz_delete(self):
        """
        Delete all test virtual extension ranges that start with 'test '.
        """
        vapi = self.async_api.telephony.virtual_extensions
        ve_range_list = await vapi.list_range()
        tasks = [vapi.delete_range(ve_range.id) for ve_range in ve_range_list if ve_range.name.startswith('test_')]
        results = await asyncio.gather(*tasks)
        print(f'deleted {len(results)} virtual extension ranges')
