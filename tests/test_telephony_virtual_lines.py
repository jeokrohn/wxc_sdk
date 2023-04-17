import asyncio
from contextlib import asynccontextmanager
from itertools import chain
from math import ceil

from tests.base import async_test, TestWithLocations
from tests.testutil import as_available_extensions_gen
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.telephony.virtual_line import VirtualLine


class VirtualLineTest(TestWithLocations):
    """
    Base class for tests that require some test virtual lines
    """

    @staticmethod
    async def create_test_vl(api: AsWebexSimpleApi, org_id: str, location: Location, extension: str) -> str:
        """
        Create a virtual line
        """
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{webex_id_to_uuid(org_id)}/virtualprofiles'
        body = {"firstName": "VL", "lastName": extension, "displayName": f"VL {extension}-{location.name}",
                "extension": extension,
                "outgoingCallsEnabled": None, "locationId": webex_id_to_uuid(location.location_id)}
        r = await api.session.rest_post(url=url, json=body)
        return r['id']

    @staticmethod
    async def delete_vl(api: AsWebexSimpleApi, org_id: str, vl_id: str):
        """
        Delete a virtual line
        """
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{webex_id_to_uuid(org_id)}/virtualprofiles/' \
              f'{vl_id}'
        await api.session.rest_delete(url=url)

    @asynccontextmanager
    async def assert_virtual_lines(self, min_count: int, min_create: int = 0):
        """
        Guarantee that we have "enough" virtual lines for the test
        """
        with self.no_log():
            me, vl_list = await asyncio.gather(self.async_api.people.me(),
                                               self.async_api.telephony.virtual_lines.list())
        locations = self.locations
        me: Person
        vl_list: list[VirtualLine]
        locations: list[Location]

        async def create_virtual_lines(location: Location) -> list[str]:
            """
            create the required number of virtual lines in location and return list of virtual line ids
            """
            # get extensions in location
            extensions = await as_available_extensions_gen(api=self.async_api, location_id=location.location_id)
            # create virtual lines
            new_ids = await asyncio.gather(*[self.create_test_vl(api=self.async_api,
                                                                 org_id=me.org_id,
                                                                 location=location,
                                                                 extension=next(extensions))
                                             for _ in range(virtual_lines_per_location)])
            return new_ids

        if (len(vl_list) < min_count) or min_create:
            virtual_lines_per_location = ceil((min_count - len(vl_list)) / len(locations))
            virtual_lines_per_location = max(virtual_lines_per_location, min_create)
            with self.no_log():
                new_vl_ids = chain.from_iterable(await asyncio.gather(*[create_virtual_lines(loc)
                                                                        for loc in locations]))
        else:
            new_vl_ids = None
        try:
            yield
        finally:
            if not new_vl_ids:
                return
            # delete all virtual lines we created temporarily
            with self.no_log():
                await asyncio.gather(*[self.delete_vl(api=self.async_api, org_id=me.org_id, vl_id=vl_id)
                                       for vl_id in new_vl_ids])


class TestVirtualLines(VirtualLineTest):

    @async_test
    async def test_list_all_async(self):
        """
        list all virtual lines
        """
        vl_api = self.async_api.telephony.virtual_lines
        virtual_lines = await vl_api.list()
        print(f'Got {len(virtual_lines)} virtual lines')

    @async_test
    async def test_display_name(self):
        """
        create a virtual line with display name and see if that value is returned
        """
        async with self.assert_virtual_lines(min_count=1, min_create=1):
            vl_list = await self.async_api.telephony.virtual_lines.list()
        vl_with_custom_name = [vl for vl in vl_list
                               if vl.custom_external_caller_id_name]
        self.assertFalse(not vl_with_custom_name, 'No virtual lines with custom name found')


class TestPagination(VirtualLineTest):
    """
    Test pagination for Virtual Lines
    """

    @async_test
    async def test_pagination(self):
        delete_vls = [vl for vl in await self.async_api.telephony.virtual_lines.list()
                      if vl.caller_id_first_name == 'VL']
        me = await self.async_api.people.me()
        await asyncio.gather(*[self.delete_vl(api=self.async_api,
                                              org_id=me.org_id,
                                              vl_id=webex_id_to_uuid(vl.id))
                               for vl in delete_vls])
        async with self.assert_virtual_lines(min_count=15):
            vl_api = self.api.telephony.virtual_lines
            vl_list = list(vl_api.list())
            vl_list_paginated = list(vl_api.list(max=4))
        # both lists should be equal
        self.assertEqual(vl_list, vl_list_paginated)
