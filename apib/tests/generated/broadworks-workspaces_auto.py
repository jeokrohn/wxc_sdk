from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BroadWorksWorkspacesApi', 'WorkspaceResponse']


class WorkspaceResponse(ApiModel):
    #: Provisioning ID that defines how this workspace is to be provisioned for Cisco Webex Services. Each Customer
    #: Template will have their own unique Provisioning ID. This ID will be displayed under the chosen Customer
    #: Template on Cisco Webex Control Hub.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioning_id: Optional[str] = None
    #: The user ID of the workspace on BroadWorks.
    #: example: 95547321@sp.com
    user_id: Optional[str] = None
    #: The Service Provider supplied unique identifier for the workspace's enterprise.
    #: example: Reseller1+acme
    sp_enterprise_id: Optional[str] = None
    #: The display name of the workspace.
    #: example: Conference Room
    display_name: Optional[str] = None
    #: The primary phone number configured against the workspace on BroadWorks.
    #: example: +1-240-555-1212
    primary_phone_number: Optional[str] = None
    #: The extension number configured against the workspace on BroadWorks.
    #: example: 51212
    extension: Optional[str] = None
    #: A unique Cisco identifier for the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFL2RkMjJlZGZlLTlmZWYtNDdmOS05ODFkLWYxYjA3MWFmMDcwYw
    id: Optional[str] = None
    #: The date and time the workspace was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None


class BroadWorksWorkspacesApi(ApiChild, base='broadworks/workspaces'):
    """
    BroadWorks Workspaces
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. They enable Service Providers to provision Cisco Webex Services for their workspaces. Please
    note these APIs require a
    functional BroadWorks system configured for Webex for BroadWorks. Read more about using this API at
    https://www.cisco.com/go/WebexBroadworksAPI.
    
    Provisioning, updating, and removing workspaces requires an administrator auth token with the
    `spark-admin:places_write` scope.
    """

    def provision_a_broad_works_workspace(self, provisioning_id: str, user_id: str, sp_enterprise_id: str,
                                          display_name: str, primary_phone_number: str = None,
                                          extension: str = None) -> WorkspaceResponse:
        """
        Provision a BroadWorks Workspace

        Provision a new BroadWorks workspace for Cisco Webex services.

        This API allows a Service Provider to provision a workspace for an existing customer.

        :param provisioning_id: Provisioning ID that defines how this workspace is to be provisioned for Cisco Webex
            Services. Each Customer Template will have their own unique Provisioning ID. This ID will be displayed
            under the chosen Customer Template on Cisco Webex Control Hub.
        :type provisioning_id: str
        :param user_id: The user ID of the workspace on BroadWorks.
        :type user_id: str
        :param sp_enterprise_id: The Service Provider supplied unique identifier for the workspace's enterprise.
        :type sp_enterprise_id: str
        :param display_name: The display name of the workspace.
        :type display_name: str
        :param primary_phone_number: The primary phone number configured against the workspace on BroadWorks.
        :type primary_phone_number: str
        :param extension: The extension number configured against the workspace on BroadWorks.
        :type extension: str
        :rtype: :class:`WorkspaceResponse`
        """
        body = dict()
        body['provisioningId'] = provisioning_id
        body['userId'] = user_id
        body['spEnterpriseId'] = sp_enterprise_id
        body['displayName'] = display_name
        if primary_phone_number is not None:
            body['primaryPhoneNumber'] = primary_phone_number
        if extension is not None:
            body['extension'] = extension
        url = self.ep()
        data = super().post(url, json=body)
        r = WorkspaceResponse.model_validate(data)
        return r

    def update_a_broadworks_workspace(self, workspace_id: str, user_id: str = None, primary_phone_number: str = None,
                                      extension: str = None) -> WorkspaceResponse:
        """
        Update a Broadworks Workspace

        Update certain details of a provisioned BroadWorks workspace on Cisco Webex.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str
        :param user_id: The user ID of the workspace on BroadWorks.
        :type user_id: str
        :param primary_phone_number: The primary phone number configured against the workspace on BroadWorks.
        :type primary_phone_number: str
        :param extension: The extension number configured against the workspace on BroadWorks.
        :type extension: str
        :rtype: :class:`WorkspaceResponse`
        """
        body = dict()
        if user_id is not None:
            body['userId'] = user_id
        if primary_phone_number is not None:
            body['primaryPhoneNumber'] = primary_phone_number
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'{workspace_id}')
        data = super().put(url, json=body)
        r = WorkspaceResponse.model_validate(data)
        return r

    def remove_a_broad_works_workspace(self, workspace_id: str):
        """
        Remove a BroadWorks Workspace

        Remove the mapping between a BroadWorks workspace and Cisco Webex device.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str
        :rtype: None
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url)
