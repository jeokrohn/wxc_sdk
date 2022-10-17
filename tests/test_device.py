import uuid
from concurrent.futures import ThreadPoolExecutor
from random import choice

from tests.base import TestCaseWithLog
from wxc_sdk.devices import TagOp


class TestDevice(TestCaseWithLog):
    def test_001_list(self):
        """
        list all devices
        """
        devices = list(self.api.devices.list())
        print(f'Got {len(devices)} devices.')

    def test_002_list_validate_workspace_id(self):
        """
        List all devices and get workspace details
        """
        devices = [d for d in self.api.devices.list()
                   if d.workspace_id]
        print(f'Got {len(devices)} devices with workspace IDs')
        if not devices:
            self.skipTest('No devices with workspace ids')
        workspace_ids = set(d.workspace_id for d in devices)
        with ThreadPoolExecutor() as pool:
            workspaces = list(pool.map(lambda ws: self.api.workspaces.details(workspace_id=ws),
                                       workspace_ids))
        print(f'Got details for {len(workspaces)} workspaces.')

    def test_003_details(self):
        """
        Get details for all devices
        """
        devices = list(self.api.devices.list())
        if not devices:
            self.skipTest('No devices')
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda d: self.api.devices.details(device_id=d.device_id),
                                    devices))
        print(f'Got details for {len(details)} devices')

    def test_004_patch_tags(self):
        """
        try to patch tags
        """
        with self.no_log():
            devices = list(self.api.devices.list())
        if not devices:
            self.skipTest('No devices')
        target = choice(devices)
        target = self.api.devices.details(device_id=target.device_id)
        tags = target.tags
        new_tags = [str(uuid.uuid4()) for _ in range(3)]
        self.api.devices.modify_device_tags(device_id=target.device_id,
                                            op=TagOp.add, value=new_tags)
        details = self.api.devices.details(device_id=target.device_id)
        tags_after = details.tags
        try:
            self.assertEqual(set(tags + new_tags), set(tags_after))
        finally:
            self.api.devices.modify_device_tags(device_id=target.device_id,
                                                op=TagOp.remove,
                                                value=new_tags)
            details = self.api.devices.details(device_id=target.device_id)
            self.assertEqual(tags, details.tags)

    def test_005_activation_code(self):
        """
        Try to create an activation code
        """
        workspaces = list(self.api.workspaces.list())
        if not workspaces:
            self.skipTest('No workspaces')
        target = choice(workspaces)
        ac_result = self.api.devices.activation_code(workspace_id=target.workspace_id)
        print(f'Activation code "{ac_result.code}" valid until {ac_result.expiry_time}')
