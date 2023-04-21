"""
Webex Calling Workspace settings
"""
import asyncio

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.workspace_settings.devices import WorkspaceDevice
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers
from wxc_sdk.workspaces import Workspace


class TestWorkspaceSettings(TestCaseWithLog):

    @async_test
    async def test_001_list_devices(self):
        """
        Get list of devices in all workspaces
        """
        workspaces = list(self.api.workspaces.list())
        if not workspaces:
            self.skipTest('No workspaces')
        device_lists = await asyncio.gather(*[self.async_api.workspace_settings.devices.list(ws.workspace_id)
                                              for ws in workspaces],
                                            return_exceptions=True)
        for ws, devices in zip(workspaces, device_lists):
            ws: Workspace
            print(f'workspace "{ws.display_name}"')
            if isinstance(devices, Exception):
                print(f'  failed to get device list: {devices}')
                continue
            devices: list[WorkspaceDevice]
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
        if not workspaces:
            self.skipTest('No workspaces')
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
