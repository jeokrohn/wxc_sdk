"""
Test cases for workspace numbers
"""
import asyncio
import random

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.common import PatternAction
from wxc_sdk.person_settings.available_numbers import AvailableNumber
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers, UpdateWorkspacePhoneNumber
from wxc_sdk.workspaces import CallingType, Workspace


class TestWorkspaceNumbers(TestCaseWithLog):
    @async_test
    async def test_numbers_all_workspaces(self):
        """
        Get numbers for all workspoces
        """
        workspaces = [ws for ws in await self.async_api.workspaces.list()
                      if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No WxC enabled workspaces found. Can\'t run test.')
        numbers = await asyncio.gather(*[self.async_api.workspace_settings.numbers.read(workspace_id=ws.workspace_id)
                                         for ws in workspaces])
        print(f'Got numbers for {len(numbers)} workspaces')

    @async_test
    async def test_update_numbers(self):
        """
        Try to add a phone number to a workspace
        """
        with self.no_log():
            workspaces = [ws for ws in await self.async_api.workspaces.list()
                          if ws.calling and ws.calling.type == CallingType.webex]
            if not workspaces:
                self.skipTest('No WxC enabled workspaces found. Can\'t run test.')
            numbers_list, available_numbers_list = await asyncio.gather(
                asyncio.gather(*[self.async_api.workspace_settings.numbers.read(workspace_id=ws.workspace_id)
                                 for ws in workspaces]),
                asyncio.gather(
                    *[self.async_api.workspace_settings.available_numbers.secondary(entity_id=ws.workspace_id)
                      for ws in workspaces]))
        numbers_list: list[WorkspaceNumbers]
        available_numbers_list: list[list[AvailableNumber]]
        candidates = [(ws, numbers, available_numbers) for ws, numbers, available_numbers in
                      zip(workspaces, numbers_list, available_numbers_list)
                      if available_numbers]

        if not candidates:
            self.skipTest('No workspaces with available numbers found. Can\'t run test.')
        workspace, numbers, available_numbers = random.choice(candidates)
        workspace: Workspace
        numbers: WorkspaceNumbers
        available_numbers: list[AvailableNumber]
        # try iot add the number
        number = random.choice(available_numbers)
        number: AvailableNumber
        napi = self.api.workspace_settings.numbers
        napi.update(workspace_id=workspace.workspace_id,
                    phone_numbers=[UpdateWorkspacePhoneNumber(
                        action=PatternAction.add,
                        direct_number=number.phone_number,
                        extension=number.extension,
                        primary=False)])
        try:
            after = napi.read(workspace_id=workspace.workspace_id)
            new_number = next((n for n in after.phone_numbers if n.external == number.phone_number), None)
            self.assertIsNotNone(new_number, 'Number not added')
        finally:
            # remove the number again
            napi.update(workspace_id=workspace.workspace_id,
                        phone_numbers=[UpdateWorkspacePhoneNumber(
                            action=PatternAction.delete,
                            direct_number=number.phone_number,
                            extension=number.extension,
                            primary=False)])
