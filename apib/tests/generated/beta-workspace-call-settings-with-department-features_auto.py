from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaWorkspaceCallSettingsWithDepartmentFeaturesApi', 'GetPersonOrWorkspaceDetailsObjectDepartment',
           'PutPersonOrWorkspaceDetailsObjectDepartment']


class GetPersonOrWorkspaceDetailsObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class PutPersonOrWorkspaceDetailsObjectDepartment(ApiModel):
    #: Unique identifier of the department.  Set to null to remove entity from department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class BetaWorkspaceCallSettingsWithDepartmentFeaturesApi(ApiChild, base='telephony/config/workspaces'):
    """
    Beta Workspace Call Settings with Department Features
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def read_department_of_a_workspace(self, workspace_id: str,
                                       org_id: str = None) -> GetPersonOrWorkspaceDetailsObjectDepartment:
        """
        Read Department of a Workspace

        Retrieve a workspace's department membership.

        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Retrieve department membership of this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization.
        :type org_id: str
        :rtype: GetPersonOrWorkspaceDetailsObjectDepartment
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}')
        data = super().get(url, params=params)
        r = GetPersonOrWorkspaceDetailsObjectDepartment.model_validate(data['department'])
        return r

    def update_department_of_a_workspace(self, workspace_id: str,
                                         department: PutPersonOrWorkspaceDetailsObjectDepartment = None,
                                         org_id: str = None):
        """
        Update Department of a Workspace

        Modify a workspace's department membership. A department can only be assigned to WxC workspace.

        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.

        This API requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Modify department membership of this workspace.
        :type workspace_id: str
        :param department: Specifies the department information.
        :type department: PutPersonOrWorkspaceDetailsObjectDepartment
        :param org_id: Workspace is in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if department is not None:
            body['department'] = department.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}')
        super().put(url, params=params, json=body)
