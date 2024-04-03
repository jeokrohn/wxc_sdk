import asyncio
import re
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar
from unittest import skip

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.prem_pstn.trunk import TrunkType, TrunkDetail, Trunk


class TestListTrunks(TestCaseWithLog):
    """
    test cases for listing trunks
    """

    def test_001_list_all(self):
        """
        list all trunks
        :return:
        """
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        print(f'Got {len(trunks)} trunks')


class TestCreate(TestWithLocations):
    """
    Test cases to create trunks
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.trunks = list(cls.api.telephony.prem_pstn.trunk.list())

    def test_001_create(self):
        """
        create a new trunk in one location
        :return:
        """
        location = choice(self.locations)
        trunk_names = set(t.name for t in self.trunks)
        loc_prefix, _ = re.subn(r'[^\w\d\s]', ' ', location.name[:20])
        trunk_name = next(name for i in range(1000) if (name := f'{loc_prefix} {i:03}') not in trunk_names)
        print(f'Creating "{trunk_name}" in "{location.name}"')
        password = self.api.telephony.location.generate_password(location_id=location.location_id)
        new_trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                 location_id=location.location_id,
                                                                 password=password,
                                                                 trunk_type=TrunkType.registering)
        try:
            trunks = list(self.api.telephony.prem_pstn.trunk.list(location_name=location.name))
            self.assertTrue(any(t.trunk_id == new_trunk_id for t in trunks), 'trunk not found')
        finally:
            self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=new_trunk_id)


class TestDetails(TestCaseWithLog):
    """
    Tests on trunk details
    """

    @async_test
    async def test_001_get_all_details(self):
        api = self.async_api.telephony.prem_pstn.trunk
        trunks = await api.list()
        details = await asyncio.gather(*[api.details(trunk_id=trunk.trunk_id)
                                         for trunk in trunks],
                                       return_exceptions=True)
        err = None
        for trunk, detail in zip(trunks, details):
            trunk: Trunk
            if isinstance(detail, Exception):
                err = err or detail
                print(f'trunk {trunk.name}/{trunk.location.name}: {detail}')
        if err:
            raise err
        print(f'Got details for {len(trunks)} trunks')


class TestUsage(TestCaseWithLog):
    """
    Tests on trunk usage
    """

    def test_001_get_usage_all(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda t: api.usage(trunk_id=t.trunk_id),
                                    trunks))
        print(f'Got usage for {len(trunks)} trunks')

    def test_002_get_usage_dial_plan(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_dial_plan(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got dial plan usage for {len(trunks)} trunks')

    def test_003_get_usage_location_pstn(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_location_pstn(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got location PSTN usage for {len(trunks)} trunks')

    def test_004_get_usage_route_group(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_route_group(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got route group usage for {len(trunks)} trunks')

    def test_004_get_usage_call_to_extension(self):
        api = self.api.telephony.prem_pstn.trunk
        trunks = list(api.list())
        with ThreadPoolExecutor() as pool:
            usage = list(pool.map(lambda t: list(api.usage_call_to_extension(trunk_id=t.trunk_id)),
                                  trunks))
        print(f'Got call to extension usage for {len(trunks)} trunks')


class TestTrunkTypes(TestCaseWithLog):
    def test_001_trunk_types(self):
        """
        get trunk types
        :return:
        """
        trunk_types = self.api.telephony.prem_pstn.trunk.trunk_types()
        print(f'Got {len(trunk_types)} trunk types')
        for tt in trunk_types:
            print(f'type: {tt.trunk_type}')
            for dt in tt.device_types:
                print(f'  device type: {dt.device_type} min; {dt.min_concurrent_calls} max: {dt.max_concurrent_calls}')


AddressTuple = namedtuple('AddressTuple', ['address', 'domain'])


@dataclass(init=False)
class TestValidateFQDNandDomain(TestCaseWithLog):
    verified_domain = 'jkrohn-sandbox.wbx.ai'

    _cert_trunks: ClassVar[list[TrunkDetail]] = field(default=None)

    async def cert_trunks(self) -> list[TrunkDetail]:
        """
        Details of all certificate based trunks
        """
        if self._cert_trunks is None:

            cert_trunks = [t for t in await self.async_api.telephony.prem_pstn.trunk.list()
                           if t.trunk_type == TrunkType.certificate_base]
            if not cert_trunks:
                self.__class__._cert_trunks = []
            else:
                # noinspection PyTypeChecker
                self.__class__._cert_trunks = await asyncio.gather(
                    *[self.async_api.telephony.prem_pstn.trunk.details(trunk_id=t.trunk_id)
                      for t in cert_trunks])
        # noinspection PyTypeChecker
        return self._cert_trunks

    async def cert_trunk_params(self) -> set[AddressTuple]:
        """
        Set of connection parameters of all cert based trunks
        :return:
        """
        return set(AddressTuple(t.address, t.domain) for t in await self.cert_trunks())

    async def available_fqdn(self) -> AddressTuple:
        existing = await self.cert_trunk_params()
        return next(p for i in range(1, 100)
                    if (p := AddressTuple(f'cube_{i:02}', self.verified_domain)) not in existing)

    def test_001_invalid_domain(self):
        """
        Invalid domain
        """
        with self.assertRaises(RestError) as ctx:
            self.api.telephony.prem_pstn.trunk.validate_fqdn_and_domain(address='cube', domain='foo', port=6001)
        rest_error: RestError = ctx.exception
        self.assertTrue(rest_error.code == 25252 and rest_error.response.status_code == 409, f'{rest_error}')

    @async_test
    async def test_002_valid_fqdn(self):
        """
        Valid FQDN
        """
        fqdn = await self.available_fqdn()
        self.api.telephony.prem_pstn.trunk.validate_fqdn_and_domain(address=fqdn.address,
                                                                    domain=fqdn.domain,
                                                                    port=6001)

    @async_test
    async def test_003_valid_srv(self):
        """
        Valid SRV
        """
        fqdn = await self.available_fqdn()
        self.api.telephony.prem_pstn.trunk.validate_fqdn_and_domain(address=fqdn.address, domain=fqdn.domain)

    @async_test
    async def test_004_existing_fqdn_and_port(self):
        """
        Existing FQDN and port
        """
        cert_trunks = [t for t in await self.cert_trunks()
                       if t.port]
        if not cert_trunks:
            self.skipTest('Need a certificate based trunk (FQDN and port) to run test')
        target = choice(cert_trunks)
        with self.assertRaises(RestError) as ctx:
            self.api.telephony.prem_pstn.trunk.validate_fqdn_and_domain(address=target.address, domain=target.domain,
                                                                        port=target.port)
        rest_error: RestError = ctx.exception
        self.assertTrue(rest_error.code == 27571 and rest_error.response.status_code == 409,
                        f'{rest_error}')

    @async_test
    async def test_005_existing_srv(self):
        """
        Existing SRV
        """
        cert_trunks = [t for t in await self.cert_trunks()
                       if t.port is None]
        if not cert_trunks:
            self.skipTest('Need a certificate based trunk (SRV) to run test')
        target = choice(cert_trunks)
        with self.assertRaises(RestError) as ctx:
            self.api.telephony.prem_pstn.trunk.validate_fqdn_and_domain(address=target.address, domain=target.domain)
        rest_error: RestError = ctx.exception
        self.assertTrue(rest_error.code == 27571 and rest_error.response.status_code == 409,
                        f'{rest_error}')


@skip
class TestDeleteTestTrunks(TestCaseWithLog):

    def test_001_delete_test_trunks(self):
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        to_delete = [trunk for trunk in trunks
                     if re.match(r'.+\s\d{2}$', trunk.name)]
        if not to_delete:
            self.skipTest('Nothing to do')
        with ThreadPoolExecutor() as pool:
            list(pool.map(
                lambda trunk: self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=trunk.trunk_id),
                to_delete))
