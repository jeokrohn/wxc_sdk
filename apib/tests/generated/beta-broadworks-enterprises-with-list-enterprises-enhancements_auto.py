from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['EnterpriseListResponse', 'EnterpriseListResponseBroadworksDirectorySync', 'EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus', 'EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors', 'TriggerDirectorySyncResponse', 'TriggerDirectorySyncResponseDirectorySyncStatus', 'TriggerUserDirectorySyncResponse', 'TriggerUserDirectorySyncResponseStatus', 'TriggerUserDirectorySyncResponseUserResponse']


class EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors(ApiModel):
    #: An error code that identifies the reason for the error
    #: example: 6003.0
    error_code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Broadworks External Directory User Sync failed while trying to connect to Broadworks cluster.
    description: Optional[str] = None


class EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus(ApiModel):
    #: The start date and time of the last sync.
    #: example: 2021-04-01T14:49:50.309640Z
    last_sync_start_time: Optional[datetime] = None
    #: The end date and time of the last sync.
    #: example: 2021-04-01T14:49:52.667189Z
    last_sync_end_time: Optional[datetime] = None
    #: The sync status of the enterprise.
    #: example: COMPLETE
    sync_status: Optional[str] = None
    #: The number of users added to CI in this sync.
    #: example: 44.0
    users_added: Optional[int] = None
    #: The number of users updated in CI in this sync.
    #: example: 21.0
    users_updated: Optional[int] = None
    #: The number of users deleted from CI in this sync.
    #: example: 34.0
    users_deleted: Optional[int] = None
    #: The number of machines added to CI in this sync.
    #: example: 24.0
    machines_added: Optional[int] = None
    #: The number of machines updated in CI in this sync.
    #: example: 4.0
    machines_updated: Optional[int] = None
    #: The number of machines deleted from CI in this sync.
    #: example: 9.0
    machines_deleted: Optional[int] = None
    #: The number of total external users that have been added to CI across all syncs.
    #: example: 1077.0
    total_external_users_in_ci: Optional[int] = Field(alias='totalExternalUsersInCI', default=None)
    #: The number of total external machines that have been added to CI across all syncs.
    #: example: 326.0
    total_external_machines_in_ci: Optional[int] = Field(alias='totalExternalMachinesInCI', default=None)
    #: The date and time of the last successful sync.
    #: example: 2021-04-01T14:48:30.502539Z
    last_successful_sync_time: Optional[datetime] = None
    #: Unique tracking identifier.
    #: example: NA_dde3a13a-bad7-4990-b155-9b4574e545b9
    last_sync_tracking_id: Optional[str] = None
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures errors that occur during a directory sync of the BroadWorks enterprise, after the API has been accepted and a 200 OK response is returned. Any errors that occur during the initial API request validation will be captured directly in the error response with an appropriate HTTP status code.
    errors: Optional[list[EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors]] = None
    #: The number of user contacts added to Contact service in this sync.
    #: example: 5.0
    user_contacts_added: Optional[int] = None
    #: The number of user contacts updated in Contact service in this sync.
    #: example: 2.0
    user_contacts_updated: Optional[int] = None
    #: The number of user contacts deleted from Contact service in this sync.
    #: example: 1.0
    user_contacts_deleted: Optional[int] = None
    #: The number of org contacts added to Contact service in this sync.
    #: example: 5.0
    org_contacts_added: Optional[int] = None
    #: The number of org contacts updated in Contact service in this sync.
    #: example: 2.0
    org_contacts_updated: Optional[int] = None
    #: The number of org contacts deleted from Contact service in this sync.
    #: example: 1.0
    org_contacts_deleted: Optional[int] = None
    #: The total number of user contacts in Contact service.
    #: example: 10.0
    total_user_contacts_in_contact_service: Optional[int] = None
    #: The total number of org contacts in Contact service.
    #: example: 2.0
    total_org_contacts_in_contact_service: Optional[int] = None


class EnterpriseListResponseBroadworksDirectorySync(ApiModel):
    #: The toggle to enable/disable directory sync.
    #: example: True
    enable_dir_sync: Optional[bool] = None
    #: Directory sync status
    directory_sync_status: Optional[EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus] = None


class EnterpriseListResponse(ApiModel):
    #: Unique Cisco identifier for the enterprise.
    #: example: Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: The Organization ID of the enterprise on Cisco Webex.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The Provisioning ID associated with the enterprise.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioning_id: Optional[str] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Reseller1+acme
    sp_enterprise_id: Optional[str] = None
    #: BroadWorks Directory sync
    broadworks_directory_sync: Optional[EnterpriseListResponseBroadworksDirectorySync] = None


class TriggerDirectorySyncResponseDirectorySyncStatus(ApiModel):
    #: The sync status of the enterprise.
    #: example: IN_PROGRESS
    sync_status: Optional[str] = None


class TriggerDirectorySyncResponse(ApiModel):
    #: The toggle that enabled the directory sync.
    #: example: True
    enable_dir_sync: Optional[bool] = None
    #: Directory sync status.
    directory_sync_status: Optional[TriggerDirectorySyncResponseDirectorySyncStatus] = None


class TriggerUserDirectorySyncResponseUserResponse(ApiModel):
    #: The user ID of the non-Webex user on Broadworks.
    #: example: john.anderson@acme.com
    user_id: Optional[str] = None
    #: First Name of the user on Broadworks.
    #: example: John
    first_name: Optional[str] = None
    #: Last Name of the user on Broadworks.
    #: example: Anderson
    last_name: Optional[str] = None
    #: Extension of the user on Broadworks.
    #: example: 4653
    extension: Optional[datetime] = None
    #: Phone number of the user on Broadworks.
    #: example: +35391884653
    number: Optional[str] = None
    #: Mobile number of the user on Broadworks.
    #: example: +188-(2323)-(343)
    mobile: Optional[str] = None


class TriggerUserDirectorySyncResponseStatus(str, Enum):
    #: An external user is added in this sync.
    add = 'ADD'
    #: An external user is updated in this sync.
    update = 'UPDATE'
    #: An external user is deleted in this sync.
    delete = 'DELETE'
    #: No changes made on the external user in this sync.
    no_operation = 'NO_OPERATION'


class TriggerUserDirectorySyncResponse(ApiModel):
    #: User Directory sync response.
    user_response: Optional[TriggerUserDirectorySyncResponseUserResponse] = None
    #: The Status of the operation being performed.
    #: example: ADD
    status: Optional[TriggerUserDirectorySyncResponseStatus] = None
