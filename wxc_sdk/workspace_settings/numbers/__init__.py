"""
Numbers API for Workspaces
"""

from pydantic import parse_obj_as

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import IdAndName, UserNumber, IdOnly

__all__ = ['WorkSpaceNumbers', 'WorkspaceNumbersApi']


class WorkSpaceNumbers(ApiModel):
    #: Array of numbers (primary/alternate).
    phone_numbers: list[UserNumber]
    #: workspace object having a unique identifier for the Workspace.
    workspace: IdOnly
    #: location object having a unique identifier for the location and its name.
    location: IdAndName
    #: organization object having a unique identifier for the organization and its name.
    organization: IdAndName


class WorkspaceNumbersApi(ApiChild, base='workspaces'):

    # noinspection PyMethodOverriding
    def ep(self, workspace_id: str, path: str = None):
        """
        :meta private:
        """
        path = path and '/path' or ''
        return super().ep(path=f'{workspace_id}/features/numbers/{path}')

    def read(self, workspace_id: str, org_id: str = None) -> WorkSpaceNumbers:
        """
        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and Organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:workspaces_read.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: List numbers for a workspace within this organization.
        :type org_id: str
        :return: Workspace numbers
        :rtype: WorkSpaceNumbers
        """
        params = org_id and {'org_id': org_id} or None
        url = self.ep(workspace_id=workspace_id)
        data = self.get(url=url, params=params)
        return parse_obj_as(WorkSpaceNumbers, data)
