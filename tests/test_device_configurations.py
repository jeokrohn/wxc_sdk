import asyncio
from operator import attrgetter
from random import choice

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.device_configurations import DeviceConfigurationOperation
from wxc_sdk.devices import Device, ProductType


class TestDeviceConfigurations(TestCaseWithLog):

    @async_test
    async def test_001_list_all(self):
        devices = [device for device in self.api.devices.list()
                   if device.product_type == ProductType.roomdesk]
        if not devices:
            self.skipTest('No devices')
        devices.sort(key=attrgetter('display_name'))
        configurations = await asyncio.gather(*[self.async_api.device_configurations.list(device_id=d.device_id)
                                                for d in devices],
                                              return_exceptions=True)
        err = None
        for device, configuration in zip(devices, configurations):
            device: Device
            if not isinstance(configuration, Exception):
                print(f'{device.display_name}: ok')
                continue
            print(f'{device.display_name}: {configuration}')
            err = err or configuration
        print(f'{len(devices)} devices, {sum(isinstance(c, Exception) for c in configurations)} failures')
        if err:
            raise err

    def test_002_system_unit_name(self):
        devices = [device for device in self.api.devices.list()
                   if device.product_type == ProductType.roomdesk]
        if not devices:
            self.skipTest('No devices')
        target_device = choice(devices)
        key = 'SystemUnit.Name'
        config_before = self.api.device_configurations.list(device_id=target_device.device_id,
                                                            key=key)
        name_before = config_before.items[key].value
        self.api.device_configurations.update(device_id=target_device.device_id,
                                              operations=[DeviceConfigurationOperation(op='replace',
                                                                                       key=key,
                                                                                       value='new_name')])
        config_after = self.api.device_configurations.list(device_id=target_device.device_id,
                                                           key=key)
        name_after = config_after.items[key].value
        self.assertEqual('new_name', name_after)
        self.api.device_configurations.update(device_id=target_device.device_id,
                                              operations=[DeviceConfigurationOperation(op='remove',
                                                                                       key=key)])
        config_removed = self.api.device_configurations.list(device_id=target_device.device_id,
                                                             key=key)
        name_removed = config_removed.items[key].value
        self.assertEqual('', name_removed)
