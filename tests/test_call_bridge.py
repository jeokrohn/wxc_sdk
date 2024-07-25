"""
Test call bridge settings
"""
import random
from unittest import skip

from tests.base import TestLocationsUsersWorkspacesVirtualLines
from wxc_sdk.people import Person
from wxc_sdk.telephony.virtual_line import VirtualLine
from wxc_sdk.workspaces import Workspace


class TestCallBridge(TestLocationsUsersWorkspacesVirtualLines):
    """
    test call bridge settings for locations, users, workspaces, virtual lines
    """
    def test_read_user(self):
        target_user = random.choice(self.users)
        target_user: Person
        self.api.person_settings.call_bridge.read(target_user.person_id)

    def test_read_virtual_line(self):
        target = random.choice(self.virtual_lines)
        target: VirtualLine
        self.api.telephony.virtual_lines.call_bridge.read(target.id)

    @skip('Redundant; tested in test_workspace_settings')
    def test_read_workspace(self):
        # TODO: promote workspace to professional before testing this
        target = random.choice(self.workspaces)
        target: Workspace
        self.api.workspace_settings.call_bridge.read(target.workspace_id)

    def test_upadate_user(self):
        ...


