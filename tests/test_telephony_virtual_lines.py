import asyncio
import base64
import json
import time
from collections.abc import Generator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from itertools import chain
from math import ceil
from random import choice
from typing import ClassVar

from tests.base import async_test, TestWithLocations, TestCaseWithLog
from tests.testutil import as_available_extensions_gen
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import Greeting
from wxc_sdk.locations import Location
from wxc_sdk.person_settings import TelephonyDevice
from wxc_sdk.person_settings.call_recording import CallRecordingSetting
from wxc_sdk.person_settings.caller_id import ExternalCallerIdNamePolicy
from wxc_sdk.person_settings.forwarding import CallForwardingAlways
from wxc_sdk.person_settings.permissions_out import OutgoingPermissions, Action, CallTypePermission
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.virtual_line import VirtualLine, VirtualLineDevices


class VirtualLineTest(TestWithLocations):
    """
    Base class for tests that require some test virtual lines
    """

    @staticmethod
    async def create_test_vl(api: AsWebexSimpleApi, location: Location, extension: str) -> str:
        """
        Create a virtual line
        """
        return await api.telephony.virtual_lines.create(first_name='VL', last_name=extension,
                                                        display_name=f"VL {extension}-{location.name}",
                                                        extension=extension,
                                                        location_id=location.location_id)

    @asynccontextmanager
    async def assert_virtual_lines(self, min_count: int, min_create: int = 0, delete_after_test: bool = True):
        """
        Guarantee that we have "enough" virtual lines for the test
        yields a VirtualLineContext instance
        """
        with self.no_log():
            vl_list = await self.async_api.telephony.virtual_lines.list()
        locations = self.locations
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
            yield None
        finally:
            if not new_vl_ids or not delete_after_test:
                return
            # delete all virtual lines we created temporarily
            with self.no_log():
                await asyncio.gather(*[as_delete_vl(api=self.async_api, vl_id=vl_id)
                                       for vl_id in new_vl_ids])


async def create_virtual_lines(api: AsWebexSimpleApi, location_id: str, vl_count: int = 1) -> list[str]:
    extensions = await as_available_extensions_gen(api=api, location_id=location_id)

    # create virtual lines
    async def create_vl(extension: str):
        r = await api.telephony.virtual_lines.create(first_name='VL', last_name=extension,
                                                     location_id=location_id, extension=extension)
        return r

    result = await asyncio.gather(*[create_vl(extension=next(extensions))
                                    for _ in range(vl_count)])
    return result


def delete_vl(api: WebexSimpleApi, vl_id: str):
    """
    Delete a VL; retry if needed
    """
    err = None
    for _ in range(10):
        try:
            api.telephony.virtual_lines.delete(virtual_line_id=vl_id)
        except RestError as e:
            err = e
            time.sleep(1)
        else:
            err = None
            break
    if err:
        raise err


async def as_delete_vl(api: AsWebexSimpleApi, vl_id: str):
    """
    Delete a VL; retry if needed
    """
    err = None
    for _ in range(10):
        try:
            await api.telephony.virtual_lines.delete(virtual_line_id=vl_id)
        except AsRestError as e:
            err = e
            await asyncio.sleep(1)
        else:
            err = None
            break
    if err:
        raise err


class TestVirtualLines(VirtualLineTest):

    def test_list(self):
        virtual_lines = list(self.api.telephony.virtual_lines.list())
        if not virtual_lines:
            self.skipTest('no virtual lines')

        print(f'Got {len(virtual_lines)} virtual lines')

    def test_list_frisco(self):
        virtual_lines = list(self.api.telephony.virtual_lines.list(location_name='Frisco'))
        if not virtual_lines:
            self.skipTest('no virtual lines')

        print(f'Got {len(virtual_lines)} virtual lines')

    def test_list_by_id(self):
        virtual_lines = list(self.api.telephony.virtual_lines.list())
        if not virtual_lines:
            self.skipTest('no virtual lines')

        id_list = [vl.id for vl in virtual_lines]
        id_list = id_list[:2]
        virtual_lines_by_id = list(self.api.telephony.virtual_lines.list(id=id_list))
        print(f'Got {len(virtual_lines_by_id)} virtual lines')
        self.assertEqual(len(id_list), len(virtual_lines_by_id))

    @async_test
    async def test_details(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')

        details = await asyncio.gather(*[api.details(virtual_line_id=vl.id) for vl in virtual_lines],
                                       return_exceptions=True)
        err = None
        for vl, detail in zip(virtual_lines, details):
            if isinstance(detail, Exception):
                err = err or detail
                print(f'Failed to get details for {vl}: {detail}')
        if err:
            raise err

    @async_test
    async def test_get_phone_numbers(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')

        numbers = await asyncio.gather(*[api.get_phone_number(virtual_line_id=vl.id) for vl in virtual_lines],
                                       return_exceptions=True)
        err = None
        for vl, number in zip(virtual_lines, numbers):
            if isinstance(number, Exception):
                err = err or number
                print(f'Failed to get numbers for {vl}: {number}')
        if err:
            raise err

    @async_test
    async def test_get_assigned_devices(self):
        """
        Get assigned devices for all virtual lines and check if all devices have an owner
        """
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        assigned_devices_list = await asyncio.gather(
            *[api.assigned_devices(virtual_line_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None

        def vl_str(vl: VirtualLine) -> str:
            return (f'{vl.first_name=} {vl.last_name=} {vl.custom_external_caller_id_name=} {vl.location.name=} '
                    f'{vl.number.esn=} {vl.number.external=}')

        def device_str(device: TelephonyDevice) -> str:
            r = f'{device.model}'
            if device.owner:
                r = f'{r} {device.owner.owner_type}/{device.owner.last_name}, {device.owner.first_name}'
            else:
                r = f'{r} - no owner! {device.device_id=} {base64.b64decode(device.device_id).decode()}'
            return r
        owner_err = False
        for vl, assigned_devices in zip(virtual_lines, assigned_devices_list):
            vl: VirtualLine
            assigned_devices: VirtualLineDevices
            if isinstance(assigned_devices, Exception):
                err = err or assigned_devices
                print(f'Failed to get assigned for {vl_str(vl)}: {assigned_devices}')
                continue
            print(f'{vl_str(vl)} has {len(assigned_devices.devices)} devices')
            for device in assigned_devices.devices:
                d_str = device_str(device)
                print(f'  {d_str}')
                if 'no owner' in d_str:
                    # this devices doesn't exist
                    try:
                        with self.assertRaises(RestError) as exc:
                            details = self.api.devices.details(device_id=device.device_id)
                        rest_error: RestError = exc.exception
                        self.assertEqual(404, rest_error.response.status_code)
                        print('    Device doesn\'t exist')
                    except AssertionError as ae:
                        print(f'  Assertion error: {ae}')
                        err = err or ae

        self.assertFalse(owner_err, 'devices w/o owner!')
        if err:
            raise err

    @async_test
    async def test_get_dect_networks(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        dect_networks_list = await asyncio.gather(
            *[api.dect_networks(virtual_line_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, dect_networks in zip(virtual_lines, dect_networks_list):
            if isinstance(dect_networks, Exception):
                err = err or dect_networks
                print(f'Failed to get numbers for {vl}: {dect_networks}')
        if err:
            raise err

    @async_test
    async def test_read_caller_id(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        caller_id_settings_list = await asyncio.gather(
            *[api.caller_id.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, caller_id_settings in zip(virtual_lines, caller_id_settings_list):
            if isinstance(caller_id_settings, Exception):
                err = err or caller_id_settings
                print(f'Failed to get numbers for {vl}: {caller_id_settings}')
        if err:
            raise err

    @async_test
    async def test_read_call_waiting(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        caller_waiting_list = await asyncio.gather(
            *[api.call_waiting.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, call_waiting in zip(virtual_lines, caller_waiting_list):
            if isinstance(call_waiting, Exception):
                err = err or call_waiting
                print(f'Failed to get numbers for {vl}: {call_waiting}')
        if err:
            raise err

    @async_test
    async def test_read_call_forwarding(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        call_forwarding_list = await asyncio.gather(
            *[api.forwarding.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, call_forwarding in zip(virtual_lines, call_forwarding_list):
            if isinstance(call_forwarding, Exception):
                err = err or call_forwarding
                print(f'Failed to get numbers for {vl}: {call_forwarding}')
        if err:
            raise err

    @async_test
    async def test_read_incoming_permission(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        incoming_permission_list = await asyncio.gather(
            *[api.permissions_in.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, incoming_permission in zip(virtual_lines, incoming_permission_list):
            if isinstance(incoming_permission, Exception):
                err = err or incoming_permission
                print(f'Failed to get numbers for {vl}: {incoming_permission}')
        if err:
            raise err

    @async_test
    async def test_read_outgoing_permissions(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        outgoing_calling_permissions_list = await asyncio.gather(
            *[api.permissions_out.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, outgoing_calling_permissions in zip(virtual_lines, outgoing_calling_permissions_list):
            if isinstance(outgoing_calling_permissions, Exception):
                err = err or outgoing_calling_permissions
                print(f'Failed to get numbers for {vl}: {outgoing_calling_permissions}')
        if err:
            raise err

    @async_test
    async def test_read_call_intercept(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        call_intercept_list = await asyncio.gather(
            *[api.call_intercept.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, call_intercept in zip(virtual_lines, call_intercept_list):
            if isinstance(call_intercept, Exception):
                err = err or call_intercept
                print(f'Failed to get numbers for {vl}: {call_intercept}')
        if err:
            raise err

    @async_test
    async def test_read_call_recording(self):
        api = self.async_api.telephony.virtual_lines
        virtual_lines = await api.list()
        if not virtual_lines:
            self.skipTest('no virtual lines')
        call_recording_list = await asyncio.gather(
            *[api.call_recording.read(entity_id=vl.id) for vl in virtual_lines],
            return_exceptions=True)
        err = None
        for vl, call_recording in zip(virtual_lines, call_recording_list):
            if isinstance(call_recording, Exception):
                err = err or call_recording
                print(f'Failed to get numbers for {vl}: {call_recording}')
        if err:
            raise err

    @async_test
    async def test_create(self):
        """
        create a new VL
        """
        target_location = choice(self.locations)
        with self.no_log():
            extensions = await as_available_extensions_gen(api=self.async_api, location_id=target_location.location_id)
        new_extension = next(extensions)
        vl_id = self.api.telephony.virtual_lines.create(first_name='VL', last_name=new_extension,
                                                        location_id=target_location.location_id,
                                                        extension=new_extension)
        virtual_line = self.api.telephony.virtual_lines.details(virtual_line_id=vl_id)
        print(f'Created new virtual line in location "{target_location.name}"')
        print(json.dumps(virtual_line.model_dump(mode='json', exclude_none=True), indent=2))
        self.assertEqual('VL', virtual_line.first_name)
        self.assertEqual(new_extension, virtual_line.last_name)
        self.assertEqual(target_location.location_id, virtual_line.location.id)
        self.assertEqual(new_extension, virtual_line.number.extension)

    @async_test
    async def test_create_w_display_name(self):
        """
        create a new VL with display_name
        """
        target_location = choice(self.locations)
        with self.no_log():
            extensions = await as_available_extensions_gen(api=self.async_api, location_id=target_location.location_id)
        new_extension = next(extensions)
        display_name = f'custom VL-{new_extension}'
        vl_id = self.api.telephony.virtual_lines.create(first_name='VL', last_name=new_extension,
                                                        location_id=target_location.location_id,
                                                        extension=new_extension,
                                                        display_name=display_name)
        try:
            virtual_line = self.api.telephony.virtual_lines.details(virtual_line_id=vl_id)
            print(f'Created new virtual line in location "{target_location.name}"')
            print(json.dumps(virtual_line.model_dump(mode='json', exclude_none=True), indent=2))
            self.assertEqual('VL', virtual_line.first_name)
            self.assertEqual(new_extension, virtual_line.last_name)
            self.assertEqual(target_location.location_id, virtual_line.location.id)
            self.assertEqual(new_extension, virtual_line.number.extension)
            self.assertEqual(display_name, virtual_line.display_name)
        finally:
            delete_vl(self.api, vl_id)


@dataclass(init=False, repr=False)
class TestWithTemporaryVirtualLine(VirtualLineTest):
    target_location: ClassVar[Location]
    extensions: ClassVar[Generator[str, None, None]]

    target: VirtualLine = field(default=None)
    target_detail: VirtualLine = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        async def prepare() -> Generator[str, None, None]:
            async with AsWebexSimpleApi(tokens=cls.tokens) as as_api:
                cls.target_location = choice(cls.locations)
                cls.extensions = await as_available_extensions_gen(api=as_api,
                                                                   location_id=cls.target_location.location_id)
            return

        asyncio.run(prepare())

    def setUp(self) -> None:
        super().setUp()

        new_extension = next(self.extensions)
        api = self.api.telephony.virtual_lines
        vl_id = api.create(first_name='VL', last_name=f'last {new_extension}',
                           location_id=self.target_location.location_id,
                           extension=new_extension)
        virtual_lines = list(api.list(id=[vl_id]))
        self.target = virtual_lines[0]
        self.target_detail = api.details(virtual_line_id=vl_id)

    def tearDown(self) -> None:
        if self.target:
            delete_vl(api=self.api, vl_id=self.target.id)
        super().tearDown()


class TestUpdate(TestWithTemporaryVirtualLine):
    """
    Trying some updates
    """

    def test_update_display_name(self):
        """
        create a VL and try to update the display name
        """
        display_name = f'custom VL-{self.target.number.extension}'
        api = self.api.telephony.virtual_lines
        api.update(virtual_line_id=self.target.id, display_name=display_name, first_name=self.target_detail.first_name,
                   last_name=self.target_detail.last_name)
        after_details = api.details(virtual_line_id=self.target.id)
        self.assertEqual(display_name, after_details.display_name)
        after_details.display_name = self.target_detail.display_name
        self.assertEqual(self.target_detail, after_details)

    def test_update_announcement_language(self):
        """
        create a VL and try to update the announcement language
        """
        api = self.api.telephony.virtual_lines
        language = 'Finnish (Finland)'
        api.update(virtual_line_id=self.target.id, announcement_language=language)
        after_details = api.details(virtual_line_id=self.target.id)
        self.assertEqual(language, after_details.announcement_language)
        after_details.announcement_language = self.target_detail.announcement_language
        self.assertEqual(self.target_detail, after_details)

    def test_update_first_name(self):
        """
        create a VL and try to update the first name
        """
        api = self.api.telephony.virtual_lines
        first_name = 'xxx'
        api.update(virtual_line_id=self.target.id, first_name=first_name)
        after_details = api.details(virtual_line_id=self.target.id)
        self.assertEqual(first_name, after_details.first_name)
        after_details.first_name = self.target_detail.first_name
        self.assertEqual(self.target_detail, after_details)

    def test_update_directory_search(self):
        """
        create a VL and try to update directory search
        """
        api = self.api.telephony.virtual_lines
        directory_search_enabled = not self.target_detail.directory_search_enabled
        api.update_directory_search(virtual_line_id=self.target.id, enabled=directory_search_enabled)
        after_details = api.details(virtual_line_id=self.target.id)
        self.assertEqual(directory_search_enabled, after_details.directory_search_enabled)
        after_details.directory_search_enabled = self.target_detail.directory_search_enabled
        self.assertEqual(self.target_detail, after_details)

    def test_update_caller_id_block_in_forward_calls_enabled(self):
        """
        create a VL and try to update block_in_forward_calls_enabled
        """
        api = self.api.telephony.virtual_lines.caller_id

        caller_id_settings = api.read(entity_id=self.target.id)

        block_in_forward_calls_enabled = not caller_id_settings.block_in_forward_calls_enabled
        update = caller_id_settings.model_copy(deep=True)
        update.block_in_forward_calls_enabled = block_in_forward_calls_enabled

        api.configure_settings(entity_id=self.target.id, settings=update)
        after = api.read(entity_id=self.target.id)

        self.assertEqual(block_in_forward_calls_enabled, after.block_in_forward_calls_enabled)
        after.block_in_forward_calls_enabled = caller_id_settings.block_in_forward_calls_enabled
        self.assertEqual(caller_id_settings, after)

    def test_update_caller_id_custom_external_caller_id_name(self):
        """
        create a VL and try to update custom_external_caller_id_name
        """
        api = self.api.telephony.virtual_lines.caller_id

        caller_id_settings = api.read(entity_id=self.target.id)
        custom_external_caller_id_name = 'Joe Doe'

        update = caller_id_settings.model_copy(deep=True)
        update.custom_external_caller_id_name = custom_external_caller_id_name
        update.external_caller_id_name_policy = ExternalCallerIdNamePolicy.other

        api.configure_settings(entity_id=self.target.id, settings=update)
        after = api.read(entity_id=self.target.id)

        self.assertEqual(custom_external_caller_id_name, after.custom_external_caller_id_name)
        self.assertEqual(ExternalCallerIdNamePolicy.other, after.external_caller_id_name_policy)

    def test_update_call_forwarding_always(self):
        """
        create a VL and try to update call forwarding always
        """
        api = self.api.telephony.virtual_lines.forwarding

        forwarding = api.read(entity_id=self.target.id)
        always = CallForwardingAlways(
            enabled=True,
            destination='9999',
            destination_voicemail_enabled=True,
            ring_reminder_enabled=True)
        update = forwarding.model_copy(deep=True)
        update.call_forwarding.always = always
        api.configure(entity_id=self.target.id, forwarding=update)
        after = api.read(entity_id=self.target.id)

        self.assertEqual(always, after.call_forwarding.always)

    def test_update_call_intercept_greeting(self):
        """
        create a VL and try to update call intercept greeting
        """
        api = self.api.telephony.virtual_lines.call_intercept

        call_intercept = api.read(entity_id=self.target.id)

        # upload greeting
        api.greeting(entity_id=self.target.id, content='sample.wav')

        # update call intercept settings
        update = call_intercept.model_copy(deep=True)
        update.incoming.announcements.greeting = Greeting.custom
        api.configure(entity_id=self.target.id,
                      intercept=update)
        after = api.read(entity_id=self.target.id)

        self.assertEqual('sample.wav', after.incoming.announcements.file_name)
        self.assertEqual(Greeting.custom, after.incoming.announcements.greeting)
        call_intercept.incoming.announcements.file_name = after.incoming.announcements.file_name
        call_intercept.incoming.announcements.greeting = after.incoming.announcements.greeting
        self.assertEqual(call_intercept, after)

    def test_update_call_recording(self):
        """
        create a VL and try to update call recording settings
        """
        api = self.api.telephony.virtual_lines.call_recording

        call_recording = api.read(entity_id=self.target.id)

        # update call recording settings
        update = call_recording.model_copy(deep=True)
        update: CallRecordingSetting
        update.enabled = True
        update.record_voicemail_enabled = True
        api.configure(entity_id=self.target.id,
                      recording=update)
        after = api.read(entity_id=self.target.id)
        self.assertEqual(True, after.enabled)
        self.assertEqual(True, after.record_voicemail_enabled)
        call_recording.enabled = True
        call_recording.record_voicemail_enabled = True
        self.assertEqual(call_recording, after)

    def test_read_outgoing_permissions_and_check_allow_extra_permission(self):
        api = self.api.telephony.virtual_lines.permissions_out
        api.read(entity_id=self.target.id)

        # get the request
        request = next(self.requests(method='GET', url_filter=r'.+/outgoingPermission$'))
        response_body = request.response_body

        # add an extra permission
        response_body['callingPermissions'].append({'action': 'BLOCK',
                                                    'callType': 'MADE_UP',
                                                    'transferEnabled': True})
        # should parse w/o an issue
        parsed_response = OutgoingPermissions.model_validate(response_body)
        parsed_response: OutgoingPermissions
        made_up_perm = parsed_response.calling_permissions.made_up
        self.assertIsNotNone(made_up_perm)
        made_up_perm: CallTypePermission
        self.assertEqual(Action.block, made_up_perm.action)
        self.assertTrue(made_up_perm.transfer_enabled)

        # verify that the made up permission is present in the serialized data
        dumped = parsed_response.model_dump()
        self.assertEqual(response_body, dumped)


class TestBulkDelete(TestWithLocations):
    @async_test
    async def test_001_bulk_delete(self):
        target_location = choice(self.locations)
        vl_ids = await create_virtual_lines(api=self.async_api, location_id=target_location.location_id, vl_count=20)
        await asyncio.gather(*[self.async_api.telephony.virtual_lines.delete(virtual_line_id=vl_id)
                               for vl_id in vl_ids])


class TestDeleteAll(TestCaseWithLog):
    """
    Delete all test virtual lines
    """

    @async_test
    async def test_delete_all(self):
        virtual_lines = [vl for vl in self.api.telephony.virtual_lines.list() if vl.first_name == 'VL']
        if not virtual_lines:
            self.skipTest('No virtual lines to delete')
        await asyncio.gather(*[as_delete_vl(api=self.async_api, vl_id=vl.id) for vl in virtual_lines],
                             return_exceptions=True)


class TestPagination(VirtualLineTest):
    """
    Test pagination for Virtual Lines
    """

    @async_test
    async def test_pagination(self):
        delete_vls = [vl for vl in await self.async_api.telephony.virtual_lines.list()
                      if vl.caller_id_first_name == 'VL']
        await asyncio.gather(*[as_delete_vl(api=self.async_api,
                                            vl_id=webex_id_to_uuid(vl.id))
                               for vl in delete_vls])
        async with self.assert_virtual_lines(min_count=15):
            vl_api = self.api.telephony.virtual_lines
            vl_list = list(vl_api.list())
            vl_list_paginated = list(vl_api.list(max=4))
        # both lists should be equal
        self.assertEqual(vl_list, vl_list_paginated)
