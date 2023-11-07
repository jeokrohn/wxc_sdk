from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['WorkspaceResponse']


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
    ...