import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from itertools import chain
from math import ceil
from random import choice, randint
from typing import Optional

from tests.base import async_test, TestWithLocations
from tests.testutil import as_available_extensions_gen
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid, ApiModel, SafeEnum
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.telephony.virtual_line import VirtualLine


@dataclass
class VirtualLineContext:
    org_id: str


class ExternalCallerIdNamePolicy(str, SafeEnum):
    other = 'OTHER'
    direct_line = 'DIRECT_LINE'
    location = 'LOCATION'


class VirtualLineCallerId(ApiModel):
    url: Optional[str] = None
    types: Optional[list[str]] = None
    selected: Optional[str] = None
    direct_number: Optional[str] = None
    custom_number: Optional[str] = None
    extension_number: Optional[str] = None
    location_number: Optional[str] = None
    toll_free_location_number: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    block_in_forward_calls_enabled: Optional[bool] = None
    external_caller_id_name_policy: Optional[str] = None
    custom_external_caller_id_name: Optional[str] = None
    location_external_caller_id_name: Optional[str] = None


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

    @staticmethod
    async def get_vl_caller_id(api: AsWebexSimpleApi, org_id: str, vl_id) -> VirtualLineCallerId:
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{webex_id_to_uuid(org_id)}/virtualprofiles/{vl_id}' \
              f'/features/callerid'
        data = await api.session.rest_get(url=url)
        r = VirtualLineCallerId.model_validate(data)
        return r

    @staticmethod
    async def update_vl_caller_id(api: AsWebexSimpleApi, org_id: str, vl_id, update: VirtualLineCallerId):
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{webex_id_to_uuid(org_id)}/virtualprofiles/{vl_id}' \
              f'/features/callerid'
        data = update.model_dump_json(exclude_none=True, by_alias=True,
                                      include={'block_in_forward_calls_enabled', 'custom_external_caller_id_name',
                                               'external_caller_id_name_policy', 'first_name', 'last_name', 'selected',
                                               'custom_number'})
        await api.session.rest_patch(url=url, data=data)

    @asynccontextmanager
    async def assert_virtual_lines(self, min_count: int, min_create: int = 0):
        """
        Guarantee that we have "enough" virtual lines for the test
        yields a VirtualLineContext instance
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
            vl_context = VirtualLineContext(org_id=me.org_id)
            yield vl_context
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
        async with self.assert_virtual_lines(min_count=1) as vl_context:
            vl_context: VirtualLineContext

            vl_list = await self.async_api.telephony.virtual_lines.list()

            # pick a random VL
            target_vl = choice(vl_list)

            # get current caller id settings
            caller_id = await self.get_vl_caller_id(api=self.async_api,
                                                    org_id=vl_context.org_id,
                                                    vl_id=webex_id_to_uuid(target_vl.id))

            # set a custom display name
            display_name = f'VL {randint(1, 999):03}'
            update = caller_id.model_copy(deep=True)
            update.external_caller_id_name_policy = ExternalCallerIdNamePolicy.other
            update.custom_external_caller_id_name = display_name
            await self.update_vl_caller_id(api=self.async_api,
                                           org_id=vl_context.org_id,
                                           vl_id=webex_id_to_uuid(target_vl.id),
                                           update=update)
            try:
                # check the list for updated vl
                list_after_update = await self.async_api.telephony.virtual_lines.list()
                updated_vl = next((vl for vl in list_after_update if vl.id == target_vl.id), None)
                self.assertIsNotNone(updated_vl, 'Target VL not found in list after update')

                # assert that the list actually returned a custom caller id name
                self.assertEqual(display_name, updated_vl.custom_external_caller_id_name,
                                 'Customer external caller id name not set in target VL')
                self.assertEqual(ExternalCallerIdNamePolicy.other, updated_vl.external_caller_id_name_policy,
                                 'External caller id name policy not set in target vl')
            finally:
                # restore old caller id settings on target VL
                await self.update_vl_caller_id(api=self.async_api,
                                               org_id=vl_context.org_id,
                                               vl_id=webex_id_to_uuid(target_vl.id),
                                               update=caller_id)


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
