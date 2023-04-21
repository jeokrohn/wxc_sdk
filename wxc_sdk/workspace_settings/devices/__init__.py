from collections.abc import Generator
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.person_settings import TelephonyDevice

__all__ = ['Hoteling', 'WorkspaceDevice', 'WorkspaceDevicesApi']


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this
    #: host(workspace device) and use this device
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive
    #: calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool]
    #: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
    limit_guest_use: Optional[bool]
    #: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
    guest_hours_limit: Optional[int]


class WorkspaceDevice(TelephonyDevice):
    #: Indicates Hoteling details of a device.
    hoteling: Optional[Hoteling]


class WorkspaceDevicesApi(ApiChild, base='telephony/config/workspaces'):
    def list(self, workspace_id: str, org_id: str = None) -> Generator[WorkspaceDevice, None, None]:
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
        return self.session.follow_pagination(url=url, model=WorkspaceDevice, params=params, item_key='devices')

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

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        super().put(url=url, params=params, data=hoteling.json())
