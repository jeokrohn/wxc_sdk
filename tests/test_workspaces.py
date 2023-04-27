"""
Test for workspaces API
"""
import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.all_types import *
from wxc_sdk.rest import RestError
from wxc_sdk.workspaces import WorkspaceCalling, WorkspaceWebexCalling, WorkspaceSupportedDevices
from tests.base import TestCaseWithLog, TestWithLocations
from tests.testutil import available_extensions_gen, new_workspace_names, TEST_WORKSPACES_PREFIX, \
    create_workspace_with_webex_calling


class TestList(TestCaseWithLog):
    def test_001_list(self):
        workspaces = list(self.api.workspaces.list())
        print(f'got {len(workspaces)} workspaces')
        print('\n'.join(w.json() for w in workspaces))


class TestDetails(TestCaseWithLog):
    def test_001_all(self):
        """
        details for all workspaces
        """
        ws = self.api.workspaces
        ws_list = ws.list()
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda w: ws.details(workspace_id=w.workspace_id),
                                    ws_list))
        print(f'got details for {len(details)} workspaces')


class TestOutgoingPermissionsAutoTransferNumbers(TestCaseWithLog):

    def test_001_get_all(self):
        """
        get outgoing permissions auto transfer numbers for all workspaces
        """
        wsa = self.api.workspaces
        tna = self.api.workspace_settings.permissions_out.transfer_numbers
        targets = [ws for ws in wsa.list()
                   if ws.calling == CallingType.webex]
        if not targets:
            self.skipTest('Need some WxC enabled workspaces to run this test')
        with ThreadPoolExecutor() as pool:
            _ = list(pool.map(lambda ws: tna.read(person_id=ws.workspace_id),
                              targets))
        print(f'outgoing permissions auto transfer numbers for {len(targets)} workspaces')

    @contextmanager
    def target_ws_context(self, use_custom_enabled: bool = True) -> Workspace:
        """
        pick a random workspace and make sure that the outgoing permission settings are restored

        :return:
        """
        po = self.api.workspace_settings.permissions_out
        targets = [ws for ws in self.api.workspaces.list()
                   if ws.calling == CallingType.webex]
        if not targets:
            self.skipTest('Need some WxC enabled workspaces to run this test')
        random.shuffle(targets)
        # if enable == False then we need a workspace where custom_enabled is not set. Else setting it to False
        # will clear all existing customer settings and we want to avoid that side effect of the test
        po_settings = None
        target_ws = next((ws for ws in targets
                          if use_custom_enabled or
                          not (po_settings := po.read(person_id=ws.workspace_id)).use_custom_enabled),
                         None)
        if target_ws is None:
            self.skipTest('No WxC enabled workspace with use_custom_enabled==False')
        if po_settings is None:
            po_settings = po.read(person_id=target_ws.workspace_id)
        try:
            if use_custom_enabled:
                # enable custom settings: else auto transfer numbers can't be set
                po.configure(person_id=target_ws.workspace_id,
                             settings=OutgoingPermissions(use_custom_enabled=use_custom_enabled))
            yield target_ws
        finally:
            # restore old settings
            if use_custom_enabled:
                po.configure(person_id=target_ws.workspace_id, settings=po_settings)
            po_restored = po.read(person_id=target_ws.workspace_id)
            self.assertEqual(po_settings, po_restored)

    def test_002_update_wo_custom_enabled(self):
        """
        updating auto transfer numbers requires use_custom_enabled to be set
        :return:
        """
        tna = self.api.workspace_settings.permissions_out.transfer_numbers
        with self.target_ws_context(use_custom_enabled=False) as target_ws:
            target_ws: Workspace
            numbers = tna.read(person_id=target_ws.workspace_id)
            try:
                # change auto transfer number 1
                update = numbers.copy(deep=True)
                transfer = f'+4961007739{random.randint(0, 999):03}'
                update.auto_transfer_number1 = transfer
                tna.configure(person_id=target_ws.workspace_id, settings=update)

                # verify update
                updated = tna.read(person_id=target_ws.workspace_id)
                # update should not work with use_custom_enabled == False
                self.assertEqual(numbers, updated)
            finally:
                # restore old settings
                tna.configure(person_id=target_ws.workspace_id, settings=numbers.configure_unset_numbers)
                restored = tna.read(person_id=target_ws.workspace_id)
                self.assertEqual(numbers, restored)
            # try
        # with

    def test_003_update_one_number(self):
        """
        try to update auto transfer numbers for a workspace
        """
        tna = self.api.workspace_settings.permissions_out.transfer_numbers
        with self.target_ws_context() as target_ws:
            target_ws: Workspace
            numbers = tna.read(person_id=target_ws.workspace_id)
            try:
                # change auto transfer number 1
                update = numbers.copy(deep=True)
                transfer = f'+496100773{random.randint(0, 9999):03}'
                update.auto_transfer_number1 = transfer
                tna.configure(person_id=target_ws.workspace_id, settings=update)

                # verify update
                updated = tna.read(person_id=target_ws.workspace_id)
                # number should be equal; ignore hyphens in number returned by API
                self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
                # other than that the updated numbers should be identical to the numbers before
                updated.auto_transfer_number1 = numbers.auto_transfer_number1
                self.assertEqual(numbers, updated)
            finally:
                # restore old settings
                tna.configure(person_id=target_ws.workspace_id, settings=numbers.configure_unset_numbers)
                restored = tna.read(person_id=target_ws.workspace_id)
                self.assertEqual(numbers, restored)
            # try
        # with

    def test_002_update_one_number_no_effect_on_other_numbers(self):
        """
        try to update auto transfer numbers for a workspace. Verify that updating a single number doesn't affect the
        other numbers
        """
        tna = self.api.workspace_settings.permissions_out.transfer_numbers
        with self.target_ws_context() as target_ws:
            target_ws: Workspace
            numbers = tna.read(person_id=target_ws.workspace_id)
            try:
                all_numbers_set = AutoTransferNumbers(auto_transfer_number1='+4961007738001',
                                                      auto_transfer_number2='+4961007738002',
                                                      auto_transfer_number3='+4961007738003')
                tna.configure(person_id=target_ws.workspace_id, settings=all_numbers_set)
                all_numbers_set = tna.read(person_id=target_ws.workspace_id)

                # change auto transfer number 1
                transfer = f'+496100773{random.randint(0, 9999):03}'
                update = AutoTransferNumbers(auto_transfer_number1=transfer)
                tna.configure(person_id=target_ws.workspace_id, settings=update)

                # verify update
                updated = tna.read(person_id=target_ws.workspace_id)
                # number should be equal; ignore hyphens in number returned by API
                self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
                # other than that the updated numbers should be identical to the numbers before
                updated.auto_transfer_number1 = all_numbers_set.auto_transfer_number1
                self.assertEqual(all_numbers_set, updated)
            finally:
                # restore old settings
                tna.configure(person_id=target_ws.workspace_id, settings=numbers.configure_unset_numbers)
                restored = tna.read(person_id=target_ws.workspace_id)
                self.assertEqual(numbers, restored)
            # try
        # with


class TestCreate(TestWithLocations):

    def test_001_trivial(self):
        """
        create workspace with minimal settings
        This workspace doesn't have a location and is for room devices
        """
        ws = self.api.workspaces
        name = next(new_workspace_names(api=self.api))
        settings = Workspace.create(display_name=name)
        settings.notes = 'test_001_trivial: no calling location, room devices'
        workspace = ws.create(settings=settings)
        print(f'new workspace:')
        print(json.dumps(json.loads(workspace.json()), indent=2))
        self.assertEqual(name, workspace.display_name)

    def test_002_edge_for_devices(self):
        """
        create workspace with edge_for_devices
        """
        ws = self.api.workspaces
        name = next(new_workspace_names(api=self.api))
        settings = Workspace(display_name=name, calling=WorkspaceCalling(type=CallingType.edge_for_devices),
                             notes='test_002_edge_for_devices: edge for devices')
        workspace = ws.create(settings=settings)
        print(f'new workspace:')
        print(json.dumps(json.loads(workspace.json()), indent=2))
        self.assertEqual(name, workspace.display_name)

    def test_003_create_workspace_with_webex_calling(self):
        """
        create a workspace with webex calling for phones
        """
        # get a calling location
        target_location = random.choice(self.locations)
        target_location: Location

        workspace = create_workspace_with_webex_calling(api=self.api,
                                                        target_location=target_location,
                                                        supported_devices=WorkspaceSupportedDevices.phones,
                                                        notes=f'test_003_create_workspace_with_webex_calling: phones, '
                                                              f'location "{target_location.name}"')
        print(f'Created workspace "{workspace.display_name}" in location "{target_location.name}" ')
        print(json.dumps(json.loads(workspace.json()), indent=2))
        # due to a limitation the workspace object returned does not have 'webex_calling' populated
        # let's check nonetheless which extension got assigned
        numbers = list(self.api.telephony.phone_numbers(owner_id=workspace.workspace_id))
        self.assertEqual(1, len(numbers))
        number = numbers[0]
        self.assertIsNotNone(number.extension)
        print(f'extension: {number.extension}')

        # ... another option to get the number
        workspace_numbers = self.api.workspace_settings.numbers.read(workspace_id=workspace.workspace_id)
        self.assertIsNotNone(workspace_numbers.phone_numbers)
        self.assertEqual(1, len(workspace_numbers.phone_numbers))
        p_number = workspace_numbers.phone_numbers[0]
        self.assertIsNotNone(p_number.extension)
        self.assertEqual(number.extension, p_number.extension)

    def test_004_create_workspace_wo_calling_and_upgrade_to_webex_calling(self):
        """
        create a workspace w/o calling for room devices and upgrade to WxC later
        """
        # get a calling location
        target_location = random.choice(self.locations)
        target_location: Location

        # get an extension in location
        extension = next(available_extensions_gen(api=self.api,
                                                  location_id=target_location.location_id))

        # get a name for new workspace
        name = next(new_workspace_names(api=self.api))

        # create workspace w/o calling 1st
        print(f'Creating workspace "{name}"')

        new_workspace = Workspace(
            display_name=name,
            # supported_devices=WorkspaceSupportedDevices.phones,
            notes=f'test_004_create_workspace_wo_calling_and_upgrade_to_webex_calling: room devices, created w/o '
                  f'calling, tried to upgrade to calling in location "{target_location.name}"')
        workspace = self.api.workspaces.create(settings=new_workspace)
        print(f'new workspace:')
        print(json.dumps(json.loads(workspace.json()), indent=2))

        # get details and try to upgrade to calling
        details = self.api.workspaces.details(workspace_id=workspace.workspace_id)
        update = details.copy(deep=True)
        update.calling = WorkspaceCalling(
            type=CallingType.webex,
            webex_calling=WorkspaceWebexCalling(
                extension=extension,
                location_id=target_location.location_id))
        print(f'Updating workspace "{name}" in location "{target_location.name}" to WxC w/ extension {extension}')
        update_result = self.api.workspaces.update(workspace_id=workspace.workspace_id,
                                                   settings=update)
        print(f'after update:')
        print(json.dumps(json.loads(update_result.json()), indent=2))

    def test_005_no_calling_phones(self):
        """
        create workspace w/o calling for phones; this should not work
        """
        # get a name for new workspace
        name = next(new_workspace_names(api=self.api))

        print(f'Creating workspace "{name}"')

        new_workspace = Workspace(
            display_name=name,
            supported_devices=WorkspaceSupportedDevices.phones)
        # this expected to fail witj
        with self.assertRaises(RestError) as ctx:
            _ = self.api.workspaces.create(settings=new_workspace)
        self.assertEqual(400, ctx.exception.response.status_code)
        print('Failed as expected')

    def test_006_create_workspace_with_webex_calling_room(self):
        """
        create a workspace with webex calling for room devices
        """
        # get a calling location
        target_location = random.choice(self.locations)
        target_location: Location

        workspace = create_workspace_with_webex_calling(
            api=self.api,
            target_location=target_location,
            supported_devices=WorkspaceSupportedDevices.collaboration_devices,
            notes=f'test_006_create_workspace_with_webex_calling_room: room devices, '
                  f'location "{target_location.name}"')
        print(f'Created workspace "{workspace.display_name}" in location "{target_location.name}" ')
        print(json.dumps(json.loads(workspace.json()), indent=2))
        # due to a limitation the workspace object returned does not have 'webex_calling' populated
        # let's check nonetheless which extension got assigned
        numbers = list(self.api.telephony.phone_numbers(owner_id=workspace.workspace_id))
        self.assertEqual(1, len(numbers))
        number = numbers[0]
        self.assertIsNotNone(number.extension)
        print(f'extension: {number.extension}')

        # ... another option to get the number
        workspace_numbers = self.api.workspace_settings.numbers.read(workspace_id=workspace.workspace_id)
        self.assertIsNotNone(workspace_numbers.phone_numbers)
        self.assertEqual(1, len(workspace_numbers.phone_numbers))
        p_number = workspace_numbers.phone_numbers[0]
        self.assertIsNotNone(p_number.extension)
        self.assertEqual(number.extension, p_number.extension)


class TestUpdate(TestCaseWithLog):
    @contextmanager
    def target(self, no_edge: bool = False):
        """
        Yield a random workspace for updates and restore previous settings after test
        """
        ws = self.api.workspaces
        ws_list = list(ws.list())
        if no_edge:
            ws_list = [ws for ws in ws_list
                       if ws.calling != CallingType.edge_for_devices]
        targat_ws = random.choice(ws_list)
        targat_ws = ws.details(workspace_id=targat_ws.workspace_id)
        try:
            yield targat_ws
        finally:
            ws.update(workspace_id=targat_ws.workspace_id, settings=targat_ws)
            restored = ws.details(workspace_id=targat_ws.workspace_id)
            self.assertEqual(targat_ws, restored)

    def test_001_change_name_full(self):
        """
        change name of a workspace, full settings
        """
        ws = self.api.workspaces
        with self.target(no_edge=True) as target_ws:
            target_ws: Workspace
            settings: Workspace = target_ws.copy(deep=True)
            new_name = next(new_workspace_names(api=self.api))
            settings.display_name = new_name
            after = ws.update(workspace_id=target_ws.workspace_id,
                              settings=settings)
        self.assertEqual(new_name, after.display_name)

    def test_002_change_name_name_only(self):
        """
        change name of a workspace, only name update
        """
        ws = self.api.workspaces
        with self.target(no_edge=True) as target_ws:
            target_ws: Workspace
            new_name = next(new_workspace_names(api=self.api))
            settings = Workspace(display_name=new_name)
            after = ws.update(workspace_id=target_ws.workspace_id,
                              settings=settings)
        self.assertEqual(new_name, after.display_name)


class TestDelete(TestCaseWithLog):
    def test_001_delete_one(self):
        """
        delete a random workspace
        """
        ws = self.api.workspaces
        ws_list = list(ws.list(display_name=TEST_WORKSPACES_PREFIX))
        if not ws_list:
            self.skipTest('No test workspace to delete')
        target = random.choice(ws_list)
        ws.delete_workspace(workspace_id=target.workspace_id)
        with self.assertRaises(RestError) as exc:
            ws.details(workspace_id=target.workspace_id)
        rest_error: RestError = exc.exception
        self.assertEqual(404, rest_error.response.status_code)
