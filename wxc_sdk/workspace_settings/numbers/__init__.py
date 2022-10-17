"""
Numbers API for Workspaces
"""
from typing import Optional

from pydantic import parse_obj_as

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import IdAndName

__all__ = ['WorkSpaceNumber', 'WorkspaceNumbersApi']


class WorkSpaceNumber(ApiModel):
    #: PSTN phone number in E.164 format.
    external: Optional[str]
    #: Extension for workspace.
    extension: Optional[str]
    #: primary or not primary .
    primary: bool
    workspace: IdAndName
    location: IdAndName
    organization: IdAndName


class WorkspaceNumbersApi(ApiChild, base='workspaces'):

    def ep(self, workspace_id: str, path: str = None):
        """
        :meta private:
        """
        path = path and '/path' or ''
        return super().ep(path=f'{workspace_id}/features/numbers/{path}')

    def read(self, workspace_id: str, org_id: str = None) -> list[WorkSpaceNumber]:
        """
        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and Organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:workspaces_read.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: List numbers for a workspace within this organization.
        :type org_id: str
        :return: Array of numbers (primary/alternate).
        :rtype: list[WorkSpaceNumber]
        """
        params = org_id and {'org_id': org_id} or None
        url = self.ep(workspace_id=workspace_id)
        data = self.get(url=url, params=params)
        return parse_obj_as(list[WorkSpaceNumber], data['phoneNumbers'])
