"""
Numbers API for Workspaces
"""
from typing import Optional

from pydantic import TypeAdapter

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import IdAndName, UserNumber, IdOnly, PatternAction, RingPattern

__all__ = ['WorkspaceNumbers', 'UpdateWorkspacePhoneNumber', 'WorkspaceNumbersApi']


class WorkspaceNumbers(ApiModel):
    distinctive_ring_enabled: Optional[bool] = None
    #: Array of numbers (primary/alternate).
    phone_numbers: list[UserNumber]
    #: workspace object having a unique identifier for the Workspace.
    workspace: IdOnly
    #: location object having a unique identifier for the location and its name.
    location: IdAndName
    #: organization object having a unique identifier for the organization and its name.
    organization: IdAndName


class UpdateWorkspacePhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[PatternAction] = None
    #: Phone numbers that are assigned.
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern] = None


class WorkspaceNumbersApi(ApiChild, base='workspaces'):

    # noinspection PyMethodOverriding
    def ep(self, workspace_id: str, path: str = None):
        """

        :meta private:
        """
        path = path and '/path' or ''
        return super().ep(path=f'{workspace_id}/features/numbers/{path}')

    def read(self, workspace_id: str, org_id: str = None) -> WorkspaceNumbers:
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
        :rtype: WorkspaceNumbers
        """
        params = org_id and {'org_id': org_id} or None
        url = self.ep(workspace_id=workspace_id)
        data = self.get(url=url, params=params)
        return TypeAdapter(WorkspaceNumbers).validate_python(data)

    def update(self, workspace_id: str,
               phone_numbers: list[UpdateWorkspacePhoneNumber],
               distinctive_ring_enabled: bool = None,
               org_id: str = None):
        """
        Assign or Unassign numbers associated with a specific workspace

        Assign or unassign alternate phone numbers associated with a specific workspace.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write` to
        update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: list[UpdateWorkspacePhoneNumber]
        :param distinctive_ring_enabled: Enables a distinctive ring pattern for the person.
        :type distinctive_ring_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if distinctive_ring_enabled is not None:
            body['distinctiveRingEnabled'] = distinctive_ring_enabled
        body['phoneNumbers'] = TypeAdapter(list[UpdateWorkspacePhoneNumber]).dump_python(phone_numbers, mode='json',
                                                                                         by_alias=True,
                                                                                         exclude_none=True)
        url = self.session.ep(f'telephony/config/workspaces/{workspace_id}/numbers')
        super().put(url, params=params, json=body)
