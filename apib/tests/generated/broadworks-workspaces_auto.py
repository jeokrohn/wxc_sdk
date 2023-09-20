from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['WorkspaceResponse']


class WorkspaceResponse(ApiModel):
    #: Provisioning ID that defines how this workspace is to be provisioned for Cisco Webex Services. Each Customer Template will have their own unique Provisioning ID. This ID will be displayed under the chosen Customer Template on Cisco Webex Control Hub.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioningId: Optional[str] = None
    #: The user ID of the workspace on BroadWorks.
    #: example: 95547321@sp.com
    userId: Optional[str] = None
    #: The Service Provider supplied unique identifier for the workspace's enterprise.
    #: example: Reseller1+acme
    spEnterpriseId: Optional[str] = None
    #: The display name of the workspace.
    #: example: Conference Room
    displayName: Optional[str] = None
    #: The primary phone number configured against the workspace on BroadWorks.
    #: example: +1-240-555-1212
    primaryPhoneNumber: Optional[str] = None
    #: The extension number configured against the workspace on BroadWorks.
    #: example: 51212
    extension: Optional[str] = None
    #: A unique Cisco identifier for the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFL2RkMjJlZGZlLTlmZWYtNDdmOS05ODFkLWYxYjA3MWFmMDcwYw
    id: Optional[str] = None
    #: The date and time the workspace was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
