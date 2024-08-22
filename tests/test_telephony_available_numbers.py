import asyncio
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test, TestCaseWithUsers
from wxc_sdk.telephony.virtual_line import VirtualLine
from wxc_sdk.workspaces import CallingType, Workspace


class TestUser(TestCaseWithUsers):
    """
    Available number tests for users
    """

    @async_test
    async def test_cfwd(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.call_forward(entity_id=user.person_id)
                                              for user in self.users])

    @async_test
    async def test_ecbn(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.ecbn(entity_id=user.person_id)
                                              for user in self.users])

    @async_test
    async def test_fax(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.fax_message(entity_id=user.person_id)
                                              for user in self.users])

    @async_test
    async def test_available(self):
        api = self.async_api.person_settings.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.available(entity_id=user.person_id)
                                                  for user in self.users])
        print(f'got expected:{exc.exception}')

    @async_test
    async def test_call_intercept(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.call_intercept(entity_id=user.person_id)
                                              for user in self.users])

    @async_test
    async def test_primary(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.primary(location_id=user.location_id)
                                              for user in self.users])

    @async_test
    async def test_secondary(self):
        api = self.async_api.person_settings.available_numbers
        number_lists = await asyncio.gather(*[api.secondary(entity_id=user.person_id)
                                              for user in self.users])


@dataclass(init=False)
class TestWorkspace(TestCaseWithLog):
    workspaces: ClassVar[list[Workspace]]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.workspaces = [ws for ws in cls.api.workspaces.list()
                          if ws.calling.type == CallingType.webex]

    def setUp(self) -> None:
        super().setUp()
        if not self.workspaces:
            self.skipTest('Need at least one WebexCalling enabled workspace to run this test')

    @async_test
    async def test_cfwd(self):
        api = self.async_api.workspace_settings.available_numbers
        number_lists = await asyncio.gather(*[api.call_forward(entity_id=workspace.workspace_id)
                                              for workspace in self.workspaces])

    @async_test
    async def test_ecbn(self):
        api = self.async_api.workspace_settings.available_numbers
        number_lists = await asyncio.gather(*[api.ecbn(entity_id=workspace.workspace_id)
                                              for workspace in self.workspaces])

    @async_test
    async def test_fax(self):
        api = self.async_api.workspace_settings.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.fax_message(entity_id=workspace.workspace_id)
                                                  for workspace in self.workspaces])
        print(f'got expected:{exc.exception}')

    @async_test
    async def test_available(self):
        api = self.async_api.workspace_settings.available_numbers
        number_lists = await asyncio.gather(*[api.available(entity_id=workspace.workspace_id)
                                              for workspace in self.workspaces])

    @async_test
    async def test_intercept(self):
        api = self.async_api.workspace_settings.available_numbers
        number_lists = await asyncio.gather(*[api.call_intercept(entity_id=workspace.workspace_id)
                                              for workspace in self.workspaces])

    @async_test
    async def test_primary(self):
        api = self.async_api.workspace_settings.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.primary(entity_id=workspace.workspace_id)
                                                  for workspace in self.workspaces])
        print(f'got expected:{exc.exception}')

    @async_test
    async def test_secondary(self):
        api = self.async_api.workspace_settings.available_numbers
        number_lists = await asyncio.gather(*[api.secondary(entity_id=workspace.workspace_id)
                                              for workspace in self.workspaces])


@dataclass(init=False)
class TestVirtualLines(TestCaseWithLog):
    virtual_lines: list[VirtualLine] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.virtual_lines = list(cls.api.telephony.virtual_lines.list())

    def setUp(self) -> None:
        super().setUp()
        if not self.virtual_lines:
            self.skipTest('Need at least one virtual line to run this test')

    @async_test
    async def test_cfwd(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        number_lists = await asyncio.gather(*[api.call_forward(entity_id=vl.id)
                                              for vl in self.virtual_lines])

    @async_test
    async def test_ecbn(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        number_lists = await asyncio.gather(*[api.ecbn(entity_id=vl.id)
                                              for vl in self.virtual_lines])

    @async_test
    async def test_fax(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        number_lists = await asyncio.gather(*[api.fax_message(entity_id=vl.id)
                                              for vl in self.virtual_lines])

    @async_test
    async def test_available(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        number_lists = await asyncio.gather(*[api.available(entity_id=vl.id)
                                              for vl in self.virtual_lines])

    @async_test
    async def test_intercept(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.call_intercept(entity_id=vl.id)
                                                  for vl in self.virtual_lines])
        print(f'got expected:{exc.exception}')

    @async_test
    async def test_primary(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.primary(entity_id=vl.id)
                                                  for vl in self.virtual_lines])
        print(f'got expected:{exc.exception}')

    @async_test
    async def test_secondary(self):
        api = self.async_api.telephony.virtual_lines.available_numbers
        with self.assertRaises(ValueError) as exc:
            number_lists = await asyncio.gather(*[api.secondary(entity_id=vl.id)
                                                  for vl in self.virtual_lines])
        print(f'got expected:{exc.exception}')
