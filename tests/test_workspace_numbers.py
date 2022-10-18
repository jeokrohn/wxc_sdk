"""
Test cases for workspace numbers
"""
import asyncio

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.workspaces import CallingType


class TestWorkspaceNumbers(TestCaseWithLog):
    @async_test
    async def test_numbers_all_workspaces(self):
        """
        Get numbers for all workspoces
        """
        workspaces = [ws for ws in await self.async_api.workspaces.list()
                      if ws.calling == CallingType.webex]
        if not workspaces:
            self.skipTest('No WxC enabled workspaces found. Can\'t run test.')
        numbers = await asyncio.gather(*[self.async_api.workspace_settings.numbers.read(workspace_id=ws.workspace_id)
                                         for ws in workspaces])
        print(f'Got numbers for {len(numbers)} workspaces')
