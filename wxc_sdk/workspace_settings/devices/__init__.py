from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings import TelephonyDevice, Hoteling

__all__ = ['WorkspaceDevicesApi']


class WorkspaceDevicesApi(ApiChild, base='telephony/config/workspaces'):
    def list(self, workspace_id: str, org_id: str = None) -> Generator[TelephonyDevice, None, None]:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        return self.session.follow_pagination(url=url, model=TelephonyDevice, params=params, item_key='devices')

    def modify_hoteling(self, workspace_id: str, hoteling: Hoteling, org_id: str = None):
        """
        Modify devices for a workspace.
        Modifying devices for a workspace requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param hoteling: hoteling settings
        :type hoteling: Hoteling
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-workspace
        -devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        super().put(url=url, params=params, data=hoteling.json())
