import asyncio
import json

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.devices import ProductType, ConnectionStatus
from wxc_sdk.xapi import ExecuteCommandResponse


class TestXAPI(TestCaseWithLog):

    def assert_reboot_success(self, results: list[ExecuteCommandResponse]):
        self.assertTrue(all(r.result == {
            "Action": "Restart",
            "Description": "Restarting"
        }
                            for r in results))

    @async_test
    async def test_reboot_mpps(self):
        """
        Test rebooting an MPP using xapi.execute_command for all connected MPPs
        """
        # get all MPPS
        targets = list(self.api.devices.list(product_type=ProductType.phone,
                                             connection_status=ConnectionStatus.connected))
        if not targets:
            self.skipTest('No connected MPPs found')
        for target in targets:
            print(f'{target.device_id=}, {target.last_seen=}')
        # execute reboot command for all of them
        results = await asyncio.gather(*[self.async_api.xapi.execute_command('SystemUnit.Boot',
                                                                             device_id=target.device_id,
                                                                             arguments={'Force': 'True'})
                                         for target in targets],
                                       return_exceptions=True)
        print(json.dumps(TypeAdapter(list[ExecuteCommandResponse]).dump_python(results, by_alias=True,
                                                                               exclude_unset=True),
                         indent=2))
        self.assert_reboot_success(results)

    @async_test
    async def test_system_unit_boot(self):
        """
        Test xapi.system_unit_boot for all connected MPPs
        """
        # get all MPPS
        targets = list(self.api.devices.list(product_type=ProductType.phone,
                                             connection_status=ConnectionStatus.connected))
        if not targets:
            self.skipTest('No connected MPPs found')
        for target in targets:
            print(f'{target.device_id=}, {target.last_seen=}')
        # execute reboot command for all of them
        results = await asyncio.gather(*[self.async_api.xapi.system_unit_boot(device_id=target.device_id, force=True)
                                         for target in targets],
                                       return_exceptions=True)
        print(json.dumps(TypeAdapter(list[ExecuteCommandResponse]).dump_python(results, by_alias=True,
                                                                               exclude_unset=True),
                         indent=2))
        self.assert_reboot_success(results)
