import asyncio
import json
import time

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.devices import ProductType, ConnectionStatus, Device
from wxc_sdk.xapi import ExecuteCommandResponse


class TestXAPI(TestCaseWithLog):

    def assert_reboot_success(self, results: list[ExecuteCommandResponse]):
        self.assertTrue(all(r.result == {
            "Action": "Restart",
            "Description": "Restarting"
        }
                            for r in results))

    async def monitor_reboot(self, device: Device):
        """
        Monitor the reboot of a device
        - wait for the device to get disconnected
        - wait for the device to come back online
        :param device:
        """
        max_duration = 120
        async def wait_for_connection_state(state: ConnectionStatus):
            while True:
                details = await self.async_api.devices.details(device_id=device.device_id)
                now = time.time()
                if details.connection_status==state:
                    print(f'{device.display_name}({int(now-start)}): reached target state {details.connection_status}')
                    break
                print(f'{device.display_name}({int(now-start)}): waiting for {state}, got {details.connection_status}')
                if now-start > max_duration:
                    raise TimeoutError(f'{device.display_name} did not reach {state} in {max_duration} seconds')
                await asyncio.sleep(5)

        start = time.time()
        await wait_for_connection_state(ConnectionStatus.disconnected)
        await wait_for_connection_state(ConnectionStatus.connected)

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
        r = await asyncio.gather(*[self.monitor_reboot(target) for target in targets],
                                return_exceptions=True)
        err = next((e for e in r if isinstance(e, Exception)), None)
        if err is not None:
            raise err
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
        r = await asyncio.gather(*[self.monitor_reboot(target) for target in targets],
                                 return_exceptions=True)
        err = next((e for e in r if isinstance(e, Exception)), None)
        if err is not None:
            raise err
        self.assert_reboot_success(results)
