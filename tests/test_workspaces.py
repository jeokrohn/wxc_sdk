"""
Test for workspaces API
"""
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
