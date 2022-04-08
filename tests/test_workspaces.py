"""
Test for workspaces API
"""
# TODO: tests for authorization codes
import random
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.rest import RestError
from wxc_sdk.types import *
from .base import TestCaseWithLog

TEST_WORKSPACES_PREFIX = 'workspace test '


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


class TestCreateUpdate(TestCaseWithLog):
    def new_names(self) -> Generator[str, None, None]:
        ws_list = list(self.api.workspaces.list())
        ws_names = set(w.display_name for w in ws_list)
        new_gen = (name for i in range(1000)
                   if (name := f'{TEST_WORKSPACES_PREFIX}{i:03}') not in ws_names)
        return new_gen

    @contextmanager
    def target(self, no_edge: bool = False):
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

    def test_001_trivial(self):
        """
        create workspace with minimal settings
        """
        ws = self.api.workspaces
        name = next(self.new_names())
        settings = Workspace.create(display_name=name)
        workspace = ws.create(settings=settings)
        print(f'new worksspace: {workspace.json()}')
        self.assertEqual(name, workspace.display_name)

    def test_002_edge_for_devices(self):
        """
        create workspace with edge_for_devices
        """
        ws = self.api.workspaces
        name = next(self.new_names())
        settings = Workspace(display_name=name, calling=CallingType.edge_for_devices)
        workspace = ws.create(settings=settings)
        print(f'new worksspace: {workspace.json()}')
        self.assertEqual(name, workspace.display_name)

    def test_003_change_name_full(self):
        """
        change name of a workspace, full settings
        """
        ws = self.api.workspaces
        with self.target(no_edge=True) as target_ws:
            target_ws: Workspace
            settings: Workspace = target_ws.copy(deep=True)
            new_name = next(self.new_names())
            settings.display_name = new_name
            after = ws.update(workspace_id=target_ws.workspace_id,
                              settings=settings)
        self.assertEqual(new_name, after.display_name)

    def test_004_change_name_name_only(self):
        """
        change name of a workspace, only name update
        """
        ws = self.api.workspaces
        with self.target(no_edge=True) as target_ws:
            target_ws: Workspace
            new_name = next(self.new_names())
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
