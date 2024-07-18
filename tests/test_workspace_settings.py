"""
Webex Calling Workspace settings
"""
import asyncio
import random
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import create_workspace_with_webex_calling
from wxc_sdk.licenses import License
from wxc_sdk.person_settings import TelephonyDevice
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers
from wxc_sdk.workspaces import Workspace, CallingType, WorkspaceSupportedDevices


class TestWorkspaceSettings(TestCaseWithLog):

    @async_test
    async def test_001_list_devices(self):
        """
        Get list of devices in all workspaces
        """
        workspaces = list(self.api.workspaces.list())
        workspaces = [ws for ws in workspaces if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No workspaces with calling type webex')
        device_lists = await asyncio.gather(*[self.async_api.workspace_settings.devices.list(ws.workspace_id)
                                              for ws in workspaces],
                                            return_exceptions=True)
        for ws, devices in zip(workspaces, device_lists):
            ws: Workspace
            print(f'workspace "{ws.display_name}", calling type: {ws.calling.type}')
            if isinstance(devices, Exception):
                print(f'  failed to get device list: {devices}')
                continue
            devices: list[TelephonyDevice]
            if not devices:
                print('  no devices')
                continue
            for device in devices:
                print(f'  - {device.model} {device.activation_state} {device.mac or "no MAC"} '
                      f'{device.ip_address or "no ip address"}')
        self.assertFalse(any(isinstance(dl, Exception) for dl in device_lists))

    @async_test
    async def test_002_numbers(self):
        """
        Get numbers for all workspaces
        """
        workspaces = list(self.api.workspaces.list())
        workspaces = [ws for ws in workspaces if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No workspaces with calling type webex')
        number_lists = await asyncio.gather(*[self.async_api.workspace_settings.numbers.read(ws.workspace_id)
                                              for ws in workspaces],
                                            return_exceptions=True)

        for ws, numbers in zip(workspaces, number_lists):
            ws: Workspace
            print(f'workspace "{ws.display_name}"')
            if isinstance(numbers, Exception):
                print(f'  failed to get number list: {numbers}')
                continue
            numbers: WorkspaceNumbers
            if not numbers.phone_numbers:
                print('  no phone numbers')
                continue
            for pn in numbers.phone_numbers:
                print(f'  - {pn.extension or "no extension"} {pn.external or "no TN"}')
        self.assertFalse(any(isinstance(nl, Exception) for nl in number_lists))


@dataclass(init=False)
class TestWithProfessionalWorkspace(TestWithLocations):
    """
    Tests for workspace settings using a temporary professional workspace
    """
    # temporary workspace with professional license
    workspace: ClassVar[Workspace] = None

    @classmethod
    def create_temp_workspace(cls):
        """
        Create a temporary workspace with professional license
        """
        # get pro license
        pro_license = next((lic
                            for lic in cls.api.licenses.list()
                            if lic.webex_calling_professional and lic.consumed_units < lic.total_units),
                           None)
        if pro_license:
            pro_license: License
            # create WS in random location
            location = random.choice(cls.locations)
            workspace = create_workspace_with_webex_calling(api=cls.api,
                                                            target_location=location,
                                                            # workspace_location_id=wsl.id,
                                                            supported_devices=WorkspaceSupportedDevices.phones,
                                                            notes=f'temp location for professional workspace tests, '
                                                                  f'location "{location.name}"',
                                                            license=pro_license)
            cls.workspace = workspace

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.create_temp_workspace()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.workspace:
            cls.api.workspaces.delete_workspace(cls.workspace.workspace_id)

    def setUp(self) -> None:
        super().setUp()
        self.assertIsNotNone(self.workspace, 'No professional workspace created')

    def test_read_anon_calls(self):
        api = self.api.workspace_settings.anon_calls
        api.read(self.workspace.workspace_id)

    def test_configure_anon_calls(self):
        api = self.api.workspace_settings.anon_calls
        r = api.read(self.workspace.workspace_id)
        api.configure(self.workspace.workspace_id, not r)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(not r, after)

    def test_read_dnd(self):
        api = self.api.workspace_settings.dnd
        api.read(self.workspace.workspace_id)

    def test_configure_dnd(self):
        api = self.api.workspace_settings.dnd
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.enabled = not r.enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_read_call_bridge(self):
        api = self.api.workspace_settings.call_bridge
        api.read(self.workspace.workspace_id)

    def test_configure_call_bridge(self):
        api = self.api.workspace_settings.call_bridge
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.warning_tone_enabled = not r.warning_tone_enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_read_ptt(self):
        api = self.api.workspace_settings.push_to_talk
        api.read(self.workspace.workspace_id)

    def test_configure_ptt(self):
        api = self.api.workspace_settings.push_to_talk
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.allow_auto_answer = not r.allow_auto_answer
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)
