"""
Test cases for workspace numbers
"""
import asyncio
import random
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import create_workspace_with_webex_calling, as_available_tns
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import PatternAction
from wxc_sdk.locations import Location
from wxc_sdk.telephony import NumberType
from wxc_sdk.telephony.pstn import PSTNConnectionOption, PSTNType
from wxc_sdk.workspace_settings.numbers import UpdateWorkspacePhoneNumber
from wxc_sdk.workspaces import CallingType, Workspace, WorkspaceSupportedDevices


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


@dataclass(init=False)
class TestUpdateNumbers(TestWithLocations):
    location: ClassVar[Location] = None
    workspace: ClassVar[Workspace] = None
    available_tn: ClassVar[str] = None

    @classmethod
    def setUpClass(cls) -> None:
        """
        create a new workspace with webex calling
        * in a location that uses a trunk as PSTN
        * and we also need an available TN in that location
        """
        super().setUpClass()

        async def as_setup():
            async with AsWebexSimpleApi(tokens=cls.tokens) as api:
                # get PSTN for each location
                pstn_settings = await asyncio.gather(*[api.telephony.pstn.read(location_id=loc.location_id)
                                                       for loc in cls.locations])

                # we only want to consider locations with a local gateway as PSTN
                pstn: PSTNConnectionOption
                locations = [loc for loc, pstn in zip(cls.locations, pstn_settings)
                             if pstn.pstn_connection_type == PSTNType.local_gateway]
                cls.location = random.choice(locations)
                print(f'Testing in location {cls.location.name}')

                # get TNs in that location
                location_tn_list = list(cls.api.telephony.phone_numbers(location_id=cls.location.location_id,
                                                                        number_type=NumberType.number))
                prefix = location_tn_list[0].phone_number[:5]

                # get a new TN in that location
                available_tn = (await as_available_tns(as_api=api, tn_prefix=prefix))[0]

                # add TN to location
                print(f'Adding TN {available_tn} to location {cls.location.name}')
                cls.api.telephony.location.number.add(location_id=cls.location.location_id,
                                                      phone_numbers=[available_tn])
                cls.available_tn = available_tn

        asyncio.run(as_setup())

        # need  professional license for the workspace
        pro_license = next((lic for lic in cls.api.licenses.list()
                            if lic.webex_calling_professional and lic.consumed_units < lic.total_units),
                           None)
        if pro_license is None:
            return

            # create a workspace with webex calling
        cls.workspace = create_workspace_with_webex_calling(
            api=cls.api,
            license=pro_license,
            target_location=cls.location,
            supported_devices=WorkspaceSupportedDevices.phones,
            notes=f'temp workspace for update number tests, '
                  f'location "{cls.location.name}"')

    def setUp(self) -> None:
        if not self.workspace:
            self.skipTest('No workspace created. Can\'t run test.')
        super().setUp()

    @classmethod
    def tearDownClass(cls):
        """
        clean up, remove the workspace and the TN
        """
        super().tearDownClass()
        if cls.workspace:
            cls.api.workspaces.delete_workspace(cls.workspace.workspace_id)
        if cls.available_tn:
            cls.api.telephony.location.number.remove(location_id=cls.location.location_id,
                                                     phone_numbers=[cls.available_tn])

    @async_test
    async def test_add_tn(self):
        """
        Try to add a phone number to a workspace
        """
        # try to add the number
        napi = self.api.workspace_settings.numbers
        napi.update(workspace_id=self.workspace.workspace_id,
                    phone_numbers=[UpdateWorkspacePhoneNumber(
                        action=PatternAction.add,
                        direct_number=self.available_tn,
                        primary=False)])
        try:
            after = napi.read(workspace_id=self.workspace.workspace_id)
            new_number = next((n for n in after.phone_numbers if n.external == self.available_tn), None)
            self.assertIsNotNone(new_number, 'Number not added')
        finally:
            # remove the number again
            napi.update(workspace_id=self.workspace.workspace_id,
                        phone_numbers=[UpdateWorkspacePhoneNumber(
                            action=PatternAction.delete,
                            direct_number=self.available_tn,
                            primary=False)])
