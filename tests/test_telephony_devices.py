"""
All tests around telephony devices
"""
import asyncio
import json
import random
import time
from collections import defaultdict
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain, zip_longest
from json import dumps, loads
from typing import ClassVar
from unittest import skip

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from tests.testutil import calling_users, available_mac_address
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import UserType, ValidationStatus, DeviceCustomization, DisplayNameSelection, PrimaryOrShared
from wxc_sdk.devices import Device, ProductType
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.person_settings import DeviceList, TelephonyDevice
from wxc_sdk.telephony import DeviceManagedBy
from wxc_sdk.telephony.devices import MACState, DeviceMembersResponse, AvailableMember, DeviceMember, \
    MACValidationResponse, DeviceLayout, LayoutMode, ProgrammableLineKey, LineKeyType, UserDeviceCount
from wxc_sdk.telephony.jobs import StartJobResponse
from wxc_sdk.workspaces import Workspace, CallingType


class TestSupportedDevices(TestCaseWithLog):
    def test_001_supported(self):
        """
        list of supported devices
        """
        supported_devices = self.api.telephony.supported_devices()
        print(f'Got {len(supported_devices.devices)} supported devices')
        print('\n'.join(f'{sd}' for sd in supported_devices.devices))


class DeviceSettings(TestWithLocations):
    def test_001_org_level(self):
        """
        Get org level device settings
        """
        settings = self.api.telephony.device_settings()
        print('Got org level settings')
        print(dumps(loads(settings.model_dump_json()), indent=2))

    @TestCaseWithLog.async_test
    async def test_002_location_level(self):
        locations = self.locations
        customizations = await asyncio.gather(
            *[self.async_api.telephony.location.device_settings(location_id=loc.location_id)
              for loc in locations])
        customizations: list[DeviceCustomization]
        print(f'Got {len(customizations)} location level device customization settings')


class UserDevices(TestCaseWithLog):
    @TestCaseWithLog.async_test
    async def test_001_devices_all_users(self):
        """
        get devices for all users
        """
        users = calling_users(api=self.api)
        devices = await asyncio.gather(*[self.async_api.person_settings.devices(person_id=user.person_id)
                                         for user in users])
        devices: list[TelephonyDevice]
        print(f'Got devices for {len(devices)} users')

    @async_test
    async def test_002_device_counts(self):
        """
        get device counts for all users
        """
        users = calling_users(api=self.api)
        api = self.async_api.telephony.devices
        device_counts = await asyncio.gather(*[api.user_devices_count(person_id=user.person_id)
                                               for user in users])
        print(f'Got device counts for {len(device_counts)} users')
        for user, device_count in zip(users, device_counts):
            user: Person
            device_count: UserDeviceCount
            print(f'{user.display_name}')
            print(json.dumps(device_count.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))
            print()


class ValidateMac(TestCaseWithLog):
    def test_001_validate(self):
        """
        validate a MAC address
        """
        r = self.api.telephony.devices.validate_macs(macs=['AFFEAFFEDEAD'])
        print(r)

    def test_002_validate_w_org_id(self):
        """
        Validate a MAC address and provide org id
        """
        with self.no_log():
            me = self.api.people.me()
        r = self.api.telephony.devices.validate_macs(macs=['00005E0053B4'], org_id=me.org_id)
        print(r)

    def test_003_illegal_mac_address(self):
        """
        Validate an illegal MAC address
        """
        r = self.api.telephony.devices.validate_macs(macs=['kjhgf'])
        self.assertEqual(ValidationStatus.errors, r.status)
        self.assertEqual(1, len(r.mac_status))
        self.assertEqual(25220, r.mac_status[0].error_code)
        self.assertTrue(r.mac_status[0].message.startswith('Invalid'))

    def test_004_duplicate_in_list(self):
        """
        Duplicate in list
        """
        r = self.api.telephony.devices.validate_macs(macs=['affeaffedead', 'affeaffedead'])
        self.assertEqual(ValidationStatus.errors, r.status)
        self.assertEqual(2, len(r.mac_status))
        self.assertEqual(MACState.available, r.mac_status[0].state)
        self.assertEqual(MACState.duplicate_in_list, r.mac_status[1].state)
        self.assertEqual(5676, r.mac_status[1].error_code)

    @async_test
    async def test_005_duplicate(self):
        """
        duplicate MAC address
        """
        # get mac addresses of existing devices
        existing_macs = [mac for device in self.api.devices.list(product_type='phone')
                         if (mac := device.mac)]
        if not existing_macs:
            self.skipTest('No existing device MAC addresses')

        # try to validate an existing MAC address; this has to fail
        r = self.api.telephony.devices.validate_macs(macs=existing_macs[0])

        self.assertEqual(ValidationStatus.errors, r.status)
        self.assertEqual(1, len(r.mac_status))
        self.assertEqual(MACState.unavailable, r.mac_status[0].state)
        self.assertEqual(5675, r.mac_status[0].error_code)

    @skip('Takes too long')
    @async_test
    async def test_006_docker_macs(self):
        """
        scan for Docker mac addresses
        """
        docker_oui = '02423b'
        macs_to_check = 100

        # scan a bunch of macs for each 4th octet
        async def scan_range(index: int) -> str:
            prefix = f'{docker_oui}{index:02x}'
            # we want to check the top and bottom x MACs
            check_macs = [f'{prefix}{i:04x}' for i in range(macs_to_check)]
            check_macs.extend(f'{prefix}{255 - i:04x}' for i in range(macs_to_check))

            validation = await self.async_api.telephony.devices.validate_macs(macs=check_macs)
            if validation.status == ValidationStatus.ok:
                return ''
            return validation

        results = await asyncio.gather(*[scan_range(i) for i in range(256)])

    @skip('Takes too long')
    @async_test
    async def test_007_all_docker_macs(self):
        def batches(seq: Iterable, batch_size: int):
            it = iter(seq)
            itb = [it] * batch_size
            return zip_longest(*itb)

        macs_to_check = (f'02423b{i:06x}' for i in range(0, 2 ** 24, 64))
        tasks = [self.async_api.telephony.devices.validate_macs([m for m in batch if m])
                 for batch in batches(macs_to_check, 200)]
        results = await asyncio.gather(*tasks,
                                       return_exceptions=True)
        results: list[MACValidationResponse]
        nok = [result for result in results if
               isinstance(result, MACValidationResponse) and result.status != ValidationStatus.ok]
        foo = 1


class Details(TestCaseWithLog):

    @async_test
    async def test_details(self):
        """
        Get details for all devices
        """
        devices = [d for d in self.api.devices.list()
                   if d.product_type != ProductType.roomdesk]
        # get all details
        details_list = await asyncio.gather(*[self.async_api.telephony.devices.details(device_id=d.device_id)
                                              for d in devices],
                                            return_exceptions=True)
        err = None
        for device, details in zip(devices, details_list):
            device: Device
            if isinstance(details, Exception):
                err = err or details
        if err:
            raise err


class UserAndWorkspaceDeviceSettings(TestCaseWithLog):

    @async_test
    async def test_get_person_settings(self):
        """
        Get device settings for all calling users
        """
        with self.no_log():
            users = calling_users(api=self.api)
        settings_list = await asyncio.gather(
            *[self.async_api.telephony.devices.get_person_device_settings(person_id=user.person_id)
              for user in users],
            return_exceptions=True)
        err = None
        for user, settings in zip(users, settings_list):
            user: Person
            if isinstance(settings, Exception):
                err = err or settings
                print(f'Getting device settings for "{user.display_name}" failed: {settings}')
        if err:
            raise err

    def test_update_person_setting(self):
        """
        Update device settings for a random user
        """
        with self.no_log():
            users = calling_users(api=self.api)
        target_user = random.choice(users)
        api = self.api.telephony.devices
        sel = {'person_id': target_user.person_id}
        before = api.get_person_device_settings(**sel)
        try:
            update = before.model_copy(deep=True)
            update.compression = not update.compression
            api.update_person_device_settings(**sel, settings=update)
            after = api.get_person_device_settings(**sel)
            self.assertEqual(update, after)
        finally:
            api.update_person_device_settings(**sel, settings=before)

    @async_test
    async def test_get_workspace_settings(self):
        """
        Get device settings for all calling workspoces
        """
        with self.no_log():
            workspaces = [ws for ws in self.api.workspaces.list()
                          if ws.calling and ws.calling.type and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No calling workspaces to test with')
        settings_list = await asyncio.gather(
            *[self.async_api.telephony.devices.get_workspace_device_settings(workspace_id=ws.workspace_id)
              for ws in workspaces],
            return_exceptions=True)
        err = None
        for workspace, settings in zip(workspaces, settings_list):
            workspace: Workspace
            if isinstance(settings, Exception):
                err = err or settings
                print(f'Getting device settings for "{workspace.display_name}" failed: {settings}')
        if err:
            raise err

    def test_update_workspace_setting(self):
        """
        Update device settings for a random workspace
        """
        with self.no_log():
            workspaces = [ws for ws in self.api.workspaces.list()
                          if ws.calling and ws.calling.type and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No calling workspaces to test with')

        target_workspace: Workspace = random.choice(workspaces)
        api = self.api.telephony.devices
        sel = {'workspace_id': target_workspace.workspace_id}
        before = api.get_workspace_device_settings(**sel)
        try:
            update = before.model_copy(deep=True)
            update.compression = not update.compression
            api.update_workspace_device_settings(**sel, settings=update)
            after = api.get_workspace_device_settings(**sel)
            self.assertEqual(update, after)
        finally:
            api.update_workspace_device_settings(**sel, settings=before)


class TestDeviceLayout(TestCaseWithLog):

    @async_test
    async def test_get_device_layouts(self):
        """
        Get device layouts for all devices
        """
        with self.no_log():
            devices = [d for d in self.api.devices.list()
                       if d.product_type != ProductType.roomdesk and d.managed_by == DeviceManagedBy.cisco]
        if not devices:
            self.skipTest('No devices')
        # get all layouts
        layout_list = await asyncio.gather(*[self.async_api.telephony.devices.get_device_layout(device_id=d.device_id)
                                             for d in devices],
                                           return_exceptions=True)
        err = None
        for device, layout in zip(devices, layout_list):
            device: Device
            if isinstance(layout, Exception):
                err = err or layout
                print(f'Failed to get layout for {device.display_name}: {layout}')
                continue
            layout: DeviceLayout
            if layout.layout_mode == LayoutMode.custom:
                print(f'Layout for {device.display_name}')
                print('\n'.join(f'  {line}'
                                for line in json.dumps(layout.model_dump(mode='json',
                                                                         by_alias=True,
                                                                         exclude_none=True),
                                                       indent=2).splitlines()))
        if err:
            raise err

    def test_set_speed_dial(self):
        """
        Try to set a speed dial foa given phone
        """

        @contextmanager
        def temp_phone():
            with self.no_log():
                # get an available MAC address
                mac = next(available_mac_address(api=self.api))

                # pick a random user
                users = calling_users(api=self.api)
                target_user = random.choice(users)
                print(f'creating temp MPP with mac {mac} for "{target_user.display_name}"')

            # add device by MAC
            result = self.api.devices.create_by_mac_address(mac=mac,
                                                            person_id=target_user.person_id,
                                                            model='DMS Cisco 8851')
            try:
                yield result
            finally:
                self.api.devices.delete(device_id=result.device_id)
            return

        with temp_phone() as device:
            device: Device
            api = self.api.telephony.devices
            line_keys = [ProgrammableLineKey(line_key_index=i, line_key_type=LineKeyType.open)
                         for i in range(1, 11)]
            line_keys[0].line_key_type = LineKeyType.primary_line
            line_keys[1] = ProgrammableLineKey(line_key_index=2, line_key_type=LineKeyType.speed_dial,
                                               line_key_label='6000', line_key_value='6000')
            new_layout = DeviceLayout(layout_mode=LayoutMode.custom, line_keys=line_keys)
            api.modify_device_layout(device_id=device.device_id,
                                     layout=new_layout)
            after = api.get_device_layout(device_id=device.device_id)
            self.assertEqual(new_layout.layout_mode, after.layout_mode)
            self.assertEqual(new_layout.line_keys, after.line_keys)

    def test_set_to_default(self):
        """
        Try to set device layout to default
        """

        device = next(self.api.devices.list(display_name='Jamie Long CP-8865'), None)
        self.assertIsNotNone(device, 'Device not found')
        api = self.api.telephony.devices
        layout = api.get_device_layout(device_id=device.device_id)
        new_layout = DeviceLayout(layout_mode=LayoutMode.default)
        api.modify_device_layout(device_id=device.device_id,
                                 layout=new_layout)
        after = api.get_device_layout(device_id=device.device_id)
        self.assertEqual(new_layout.layout_mode, after.layout_mode)
        self.assertIsNone(after.line_keys)
        self.assertIsNone(after.kem_module_type)
        self.assertIsNone(after.kem_keys)


class Members(TestCaseWithLog):

    @TestCaseWithLog.async_test
    async def test_001_get_members_all_devices(self):
        """
        Get members for all devices
        """
        # get all MPP devices
        phones = [p for p in self.api.devices.list(product_type='phone')
                  if p.product_type == 'phone']

        # get members for all devices
        r = await asyncio.gather(*[self.async_api.telephony.devices.members(device_id=d.device_id) for d in phones],
                                 return_exceptions=True)

        # TODO: figure out new test now, as the devices API supports MPPs
        raise NotImplementedError
        with self.no_log():
            users: dict[str, Person] = {user.person_id: user for user in calling_users(api=self.api)}
            # noinspection PyTypeChecker
            person_devices_responses = await asyncio.gather(*[self.async_api.person_settings.devices(person_id=user_id)
                                                              for user_id in users])
        person_devices_responses: list[DeviceList]

        # dict of device_id sets by user id
        user_devices: dict[str, set[str]] = defaultdict(set)
        for user_id, person_devices_response in zip(users, person_devices_responses):
            user_devices[user_id].update(device.device_id for device in person_devices_response.devices)

        # dict of devices by device id
        devices: dict[str, TelephonyDevice] = dict()
        for response in person_devices_responses:
            for device in response.devices:
                if device.device_id in devices:
                    continue
                devices[device.device_id] = device
        if not devices:
            self.skipTest('No devices belonging to users?')

        # now get members for all these devices
        # noinspection PyTypeChecker
        members_list = await asyncio.gather(*[self.async_api.telephony.devices.members(device_id=device_id)
                                              for device_id in devices])
        members_list: list[DeviceMembersResponse]

        # verify that the member lists are consistent
        error = False
        for device_id, members in zip(devices, members_list):
            device = devices[device_id]
            for member in (m for m in members.members if m.member_type == UserType.people):
                user = users[member.member_id]
                devices_current_user = user_devices.get(member.member_id, set())
                try:
                    self.assertTrue(device_id in devices_current_user)
                except AssertionError:
                    print(f'Looking as device "{device.model}({device.mac})", member "{user.display_name}": '
                          f'device not in device list of user')
                    error = True
                else:
                    print(f'Looking as device "{device.model}({device.mac})", member "{user.display_name}": '
                          f'device in device list of user')
        self.assertFalse(error)

    @TestCaseWithLog.async_test
    async def test_002_available_members(self):
        """
        Get available members for all MPPs
        """
        # TODO: rewrite now that devices API includes MPPs
        with self.no_log():
            users: dict[str, Person] = {user.person_id: user for user in calling_users(api=self.api)}
            person_devices_responses = await asyncio.gather(*[self.async_api.person_settings.devices(person_id=user_id)
                                                              for user_id in users])

        # dict of devices by device id
        devices: dict[str, TelephonyDevice] = dict()
        for response in person_devices_responses:
            for device in response.devices:
                if device.device_id in devices:
                    continue
                devices[device.device_id] = device
        if not devices:
            self.skipTest('No devices belonging to users?')
        # list of users and their primary devices
        users_and_device = [(user, primary)
                            for user, person_devices_response in zip(users.values(), person_devices_responses)
                            if (primary := next((dev for dev in person_devices_response.devices
                                                 if dev.primary_owner),
                                                None)) is not None]

        users_and_device: list[tuple[Person, TelephonyDevice]]
        # get calling details for users (we need the location id)
        with self.no_log():
            user_details = await asyncio.gather(*[self.async_api.people.details(person_id=user.person_id,
                                                                                calling_data=True)
                                                  for user, _ in users_and_device])
        users_and_device = [(user, primary) for user, (_, primary) in zip(user_details, users_and_device)]

        # get list of available members for each device
        available = await asyncio.gather(
            *[self.async_api.telephony.devices.available_members(device_id=device.device_id,
                                                                 location_id=user.location_id)
              for user, device in users_and_device])
        # TODO: add some validation and/or output
        foo = 1


@dataclass(init=False)
class TestsWithDevices(TestCaseWithLog):
    """
    Test cases needing list of devices and owners
    """

    #: all calling enabled users; w/o telephony details
    calling_users: ClassVar[dict[str, Person]]
    #: all MPPs owned by users
    devices: ClassVar[list[TelephonyDevice]]
    #: device owners; w/ telephony details
    device_owners: ClassVar[dict[str, Person]]

    @classmethod
    def setUpClass(cls) -> None:
        async def async_setup():
            async with AsWebexSimpleApi(tokens=cls.tokens) as api:
                users = calling_users(api=cls.api)
                cls.calling_users = {user.person_id: user for user in users}

                # noinspection PyTypeChecker
                person_devices_responses = await asyncio.gather(
                    *[api.person_settings.devices(person_id=user.person_id)
                      for user in users])
                person_devices_responses: list[DeviceList]

                # get list of unique devices
                device_ids = set()
                devices = []
                for device in chain.from_iterable(pdr.devices for pdr in person_devices_responses):
                    if device.device_id in device_ids or device.owner.owner_type != UserType.people:
                        continue
                    devices.append(device)
                    device_ids.add(device.device_id)
                cls.devices = devices

                # get user ids of all owners
                owner_ids = [owner_id for device in devices
                             if (owner_id := device.owner.owner_id) and device.owner.owner_type == UserType.people]

                # get telephony details for owners
                cls.device_owners = {user.person_id: user
                                     for user in await asyncio.gather(*[api.people.details(person_id=oid,
                                                                                           calling_data=True)
                                                                        for oid in owner_ids])}
            return

        super().setUpClass()
        asyncio.run(async_setup())

    def setUp(self) -> None:
        super().setUp()
        if not self.devices:
            self.skipTest('Need some devices to run this test')


class TestAddMember(TestsWithDevices):
    """
    Test related to device members
    """

    # TODO: add virtual lines as members
    # TODO: verify available members semantics; since inter-location line sharing is now allowed I'd like to
    #  understand what actually gets returned as "available". ... or what is "unavailable

    @async_test
    async def test_003_add_member(self):
        def member_equal(a: DeviceMember, b: DeviceMember):
            """
            are both device member entries "equivalent"
            :param a:
            :param b:
            :return:
            """

            def eq_json(dm: DeviceMember) -> str:
                return dm.model_dump_json(exclude={'host_ip', 'remote_ip', 'first_name', 'last_name', 'phone_number',
                                                   'extension'})

            return eq_json(a) == eq_json(b)

        # get available members for each device
        with self.no_log():
            # noinspection PyTypeChecker
            available_members = await asyncio.gather(
                *[self.async_api.telephony.devices.available_members(
                    device_id=device.device_id,
                    location_id=self.device_owners[device.owner.owner_id].location_id)
                    for device in self.devices])
        available_members: list[list[AvailableMember]]

        # pick a device and available members
        if False:
            # statically pick a fixed test phone
            device, available = next(((d, a) for d, a in zip(self.devices, available_members)
                                      if d.mac == '00BF7771EB27'), (None, None))
            self.assertIsNotNone(device)
        else:
            try:
                device, available = random.choice([(d, a) for d, a in zip(self.devices, available_members)
                                                   if a])
            except IndexError:
                self.skipTest('No device with available members')
        device: TelephonyDevice
        available: list[AvailableMember]

        # get current members
        members = (await self.async_api.telephony.devices.members(device_id=device.device_id)).members

        # add a new member randomly from list of available members
        new_member: AvailableMember = random.choice(available)
        members.append(new_member)

        print(f'Adding new member "{new_member.first_name} {new_member.last_name}" to device {device.model} of '
              f'"{device.owner.first_name} {device.owner.last_name}"')
        try:
            await self.async_api.telephony.devices.update_members(device_id=device.device_id,
                                                                  members=members)
            await self.async_api.telephony.devices.apply_changes(device_id=device.device_id)

            after_members = (await self.async_api.telephony.devices.members(device_id=device.device_id)).members
            self.assertEqual(len(members), len(after_members))
            self.assertEqual(new_member.member_id, after_members[-1].member_id)
        finally:
            members = members[:-1]
            await self.async_api.telephony.devices.update_members(device_id=device.device_id,
                                                                  members=members)
            await self.async_api.telephony.devices.apply_changes(device_id=device.device_id)

            members_restored = (await self.async_api.telephony.devices.members(device_id=device.device_id)).members
            self.assertEqual(len(members), len(members_restored))
            self.assertTrue(member_equal(desired, actual) for desired, actual in zip(members, members_restored))


class TestDeviceSettings(TestsWithDevices):

    @TestsWithDevices.async_test
    async def test_001_get_device_settings(self):
        # device settings can only be read for primary devices
        devices = [device for device in self.devices if device.device_type == PrimaryOrShared.primary]
        tasks = [self.async_api.telephony.devices.device_settings(device_id=device.device_id,
                                                                  device_model=device.model)
                 for device in devices]
        settings = await asyncio.gather(*tasks, return_exceptions=True)
        err = None
        for device, setting in zip(self.devices, settings):
            device: TelephonyDevice
            if isinstance(setting, Exception):
                print(f'{device.model}, {device.device_type}: {setting}')
                err = err or setting
        if err:
            raise err

    @TestsWithDevices.async_test
    async def test_002_update(self):
        """
        get device settings of a specific device and update that at the device level
        """
        # get device settings for all devices
        devices = [device for device in self.devices if device.device_type == PrimaryOrShared.primary]
        with self.no_log():
            # noinspection PyTypeChecker
            settings = await asyncio.gather(
                *[self.async_api.telephony.devices.device_settings(device_id=device.device_id,
                                                                   device_model=device.model)
                  for device in devices])
        settings: list[DeviceCustomization]
        # pick a device
        mpps = [device for device, setting in zip(devices, settings)
                if setting.customizations.mpp]
        if not mpps:
            self.skipTest('Need at least one MPP to run the test')
        target_device: TelephonyDevice = random.choice(mpps)

        # get customization for target device
        before = self.api.telephony.devices.device_settings(device_id=target_device.device_id,
                                                            device_model=target_device.model)
        print(f'Updating display name format for {target_device.mac}')
        update = before.model_copy(deep=True)
        update.customizations.mpp.display_name_format = DisplayNameSelection.person_last_then_first_name
        update.custom_enabled = True
        self.api.telephony.devices.update_device_settings(device_id=target_device.device_id,
                                                          device_model=target_device.model,
                                                          customization=update)
        self.api.telephony.devices.apply_changes(device_id=target_device.device_id)
        try:
            after = self.api.telephony.devices.device_settings(device_id=target_device.device_id,
                                                               device_model=target_device.model)
            self.assertTrue(after.custom_enabled)
            after.last_update_time = before.last_update_time
            self.assertEqual(update, after)
        finally:
            self.api.telephony.devices.update_device_settings(device_id=target_device.device_id,
                                                              device_model=target_device.model,
                                                              customization=before)
            self.api.telephony.devices.apply_changes(device_id=target_device.device_id)

    @TestsWithDevices.async_test
    async def test_003_devices_with_device_level_customization(self):
        """
        get devices with device level customizations
        """
        # get device settings for all devices
        devices = [device for device in self.devices if device.device_type == PrimaryOrShared.primary]
        with self.no_log():
            # noinspection PyTypeChecker
            settings = await asyncio.gather(
                *[self.async_api.telephony.devices.device_settings(device_id=device.device_id,
                                                                   device_model=device.model)
                  for device in devices])
        settings: list[DeviceCustomization]

        devices_with_device_level_customization = [(device, setting)
                                                   for device, setting in zip(self.devices, settings)
                                                   if setting.custom_enabled]
        print('Devices with device level customizations')
        print('\n'.join(f'{device.model}: {device.mac}, {device.owner.first_name} {device.owner.last_name}'
                        for device, _ in devices_with_device_level_customization))


class Jobs(TestCaseWithLog):

    def monitor_job_execution(self, job: StartJobResponse):
        """
        monitor a job until its completion
        :return:
        """
        while True:
            print(f'{job.instance_id} {job.target} {job.location_name} '
                  f'{job.device_count} devices {job.latest_execution_status}')
            for status in job.job_execution_status:
                print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
                for step in status.step_execution_statuses:
                    print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')
            if job.latest_execution_status in {'COMPLETED', 'FAILED'}:
                break
            print('not ready; sleep for 2 seconds...')
            time.sleep(2)
            job = self.api.telephony.jobs.device_settings.status(job_id=job.id)
        print(json.dumps(json.loads(job.model_dump_json()), indent=2))
        self.assertEqual('COMPLETED', job.latest_execution_status)

    def test_001_list(self):
        """
        list device setting jobs
        """
        jobs = list(self.api.telephony.jobs.device_settings.list())
        print(f'Got {len(jobs)} device settings jobs')
        if not jobs:
            self.skipTest('No existing jobs')
        for job in jobs:
            print(f'{job.instance_id} {job.target} {job.location_name} '
                  f'{job.device_count} devices')
            for status in job.job_execution_status:
                print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
                for step in status.step_execution_statuses:
                    print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')

    @TestCaseWithLog.async_test
    async def test_002_get_status(self):
        """
        get status for all jobs
        """
        jobs = list(self.api.devices.settings_jobs.list())
        if not jobs:
            self.skipTest('No existing jobs')
        status = await asyncio.gather(*[self.async_api.telephony.jobs.device_settings.status(job_id=job.id)
                                        for job in jobs])
        print(f'Got status for {len(status)} jobs')

    @TestCaseWithLog.async_test
    async def test_003_get_errors(self):
        """
        get errors for all jobs
        # TODO: need to find a way to force some job errors
        """
        jobs = list(self.api.devices.settings_jobs.list())
        if not jobs:
            self.skipTest('No existing jobs')
        status = await asyncio.gather(*[self.async_api.devices.settings_jobs.errors(job_id=job.id)
                                        for job in jobs])
        print(f'Got status for {len(status)} jobs')

    def test_004_update_location_reset_to_org_settings(self):
        """
        reset device settings in a location to org settings
        """
        with self.no_log():
            locations = list(self.api.locations.list())

        # pick a random location
        target_location: Location = random.choice(locations)
        print(f'Target location: "{target_location.name}"')

        # get location level device customization
        location_settings = self.api.telephony.location.device_settings(location_id=target_location.location_id)

        print(f'Location level device customization enabled: {location_settings.custom_enabled}')
        new_settings = location_settings.model_copy(deep=True)
        new_settings.custom_enabled = False
        job = self.api.telephony.jobs.device_settings.change(location_id=target_location.location_id,
                                                             customization=new_settings)
        self.monitor_job_execution(job=job)

    def test_005_update_location_settings(self):
        """
        update device settings across a location
        """
        with self.no_log():
            locations = list(self.api.locations.list())

        # pick a random location
        target_location: Location = random.choice(locations)
        print(f'Target location: "{target_location.name}"')

        # get location level device customization
        location_settings = self.api.telephony.location.device_settings(location_id=target_location.location_id)

        print(f'Location level device customization enabled: {location_settings.custom_enabled}')
        new_settings = location_settings.model_copy(deep=True)
        new_settings.custom_enabled = not new_settings.custom_enabled
        job = self.api.telephony.jobs.device_settings.change(location_id=target_location.location_id,
                                                             customization=new_settings)
        self.monitor_job_execution(job=job)

    def test_006_update_org_settings(self):
        """
        update org level setting
        """
        # get current settings
        settings = self.api.telephony.device_settings()
        # update at org level
        job = self.api.telephony.jobs.device_settings.change(location_id=None, customization=settings)
        self.monitor_job_execution(job=job)
