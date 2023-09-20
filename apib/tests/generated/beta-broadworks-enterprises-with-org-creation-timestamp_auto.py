from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['EnterpriseListResponse', 'EnterpriseListResponseBroadworksDirectorySync', 'EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus', 'EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors', 'TriggerDirectorySyncResponse', 'TriggerDirectorySyncResponseDirectorySyncStatus', 'TriggerUserDirectorySyncResponse', 'TriggerUserDirectorySyncResponseStatus', 'TriggerUserDirectorySyncResponseUserResponse']


class EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors(ApiModel):
    #: An error code that identifies the reason for the error
    #: example: 6003.0
    errorCode: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Broadworks External Directory User Sync failed while trying to connect to Broadworks cluster.
    description: Optional[str] = None


class EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus(ApiModel):
    #: The start date and time of the last sync.
    #: example: 2021-04-01T14:49:50.309640Z
    lastSyncStartTime: Optional[datetime] = None
    #: The end date and time of the last sync.
    #: example: 2021-04-01T14:49:52.667189Z
    lastSyncEndTime: Optional[datetime] = None
    #: The sync status of the enterprise.
    #: example: COMPLETE
    syncStatus: Optional[str] = None
    #: Number of users added to CI in this sync.
    #: example: 44.0
    usersAdded: Optional[int] = None
    #: Number of users updated in CI in this sync.
    #: example: 21.0
    usersUpdated: Optional[int] = None
    #: Number of users deleted from CI in this sync.
    #: example: 34.0
    usersDeleted: Optional[int] = None
    #: Number of machines added to CI in this sync.
    #: example: 24.0
    machinesAdded: Optional[int] = None
    #: Number of machines updated in CI in this sync.
    #: example: 4.0
    machinesUpdated: Optional[int] = None
    #: Number of machines deleted from CI in this sync.
    #: example: 9.0
    machinesDeleted: Optional[int] = None
    #: Number of total external users that have been added to CI across all syncs.
    #: example: 1077.0
    totalExternalUsersInCI: Optional[int] = None
    #: Number of total external machines that have been added to CI across all syncs.
    #: example: 326.0
    totalExternalMachinesInCI: Optional[int] = None
    #: The date and time of the last successful sync.
    #: example: 2021-04-01T14:48:30.502539Z
    lastSuccessfulSyncTime: Optional[datetime] = None
    #: Unique tracking identifier.
    #: example: NA_dde3a13a-bad7-4990-b155-9b4574e545b9
    lastSyncTrackingId: Optional[str] = None
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures errors that occur during a directory sync of the BroadWorks enterprise, after the API has been accepted and a 200 OK response is returned. Any errors that occur during the initial API request validation will be captured directly in the error response with an appropriate HTTP status code.
    errors: Optional[list[EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatusErrors]] = None
    #: Number of user contacts added to Contact service in this sync.
    #: example: 5.0
    userContactsAdded: Optional[int] = None
    #: Number of user contacts updated in Contact service in this sync.
    #: example: 2.0
    userContactsUpdated: Optional[int] = None
    #: Number of user contacts deleted from Contact service in this sync.
    #: example: 1.0
    userContactsDeleted: Optional[int] = None
    #: Number of org contacts added to Contact service in this sync.
    #: example: 5.0
    orgContactsAdded: Optional[int] = None
    #: Number of org contacts updated in Contact service in this sync.
    #: example: 2.0
    orgContactsUpdated: Optional[int] = None
    #: Number of org contacts deleted from Contact service in this sync.
    #: example: 1.0
    orgContactsDeleted: Optional[int] = None
    #: Total number of user contacts in Contact service.
    #: example: 10.0
    totalUserContactsInContactService: Optional[int] = None
    #: Total number of org contacts in Contact service.
    #: example: 2.0
    totalOrgContactsInContactService: Optional[int] = None


class EnterpriseListResponseBroadworksDirectorySync(ApiModel):
    #: The toggle to enable/disable directory sync.
    #: example: True
    enableDirSync: Optional[bool] = None
    #: Directory sync status.
    directorySyncStatus: Optional[EnterpriseListResponseBroadworksDirectorySyncDirectorySyncStatus] = None


class EnterpriseListResponse(ApiModel):
    #: A unique Cisco identifier for the enterprise.
    #: example: Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: The Organization ID for the Webex enterprise.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    orgId: Optional[str] = None
    #: The Provisioning ID associated with the enterprise.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioningId: Optional[str] = None
    #: The date and time of org creation.
    #: example: 2022-03-25T11:33:48.455Z
    orgCreationTimeStamp: Optional[datetime] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Reseller1+example
    spEnterpriseId: Optional[str] = None
    #: BroadWorks Directory sync.
    broadworksDirectorySync: Optional[EnterpriseListResponseBroadworksDirectorySync] = None


class TriggerDirectorySyncResponseDirectorySyncStatus(ApiModel):
    #: The sync status of the enterprise.
    #: example: IN_PROGRESS
    syncStatus: Optional[str] = None


class TriggerDirectorySyncResponse(ApiModel):
    #: The toggle that enabled the directory sync.
    #: example: True
    enableDirSync: Optional[bool] = None
    #: Directory sync status.
    directorySyncStatus: Optional[TriggerDirectorySyncResponseDirectorySyncStatus] = None


class TriggerUserDirectorySyncResponseUserResponse(ApiModel):
    #: The user ID of the user on Broadworks (A non-webex user).
    #: example: john.anderson@example.com
    userId: Optional[str] = None
    #: First Name of the user on Broadworks.
    #: example: John
    firstName: Optional[str] = None
    #: Last Name of the user on Broadworks.
    #: example: Anderson
    lastName: Optional[str] = None
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
    #: External user is added in this sync.
    add = 'ADD'
    #: External user is updated in this sync.
    update = 'UPDATE'
    #: External user is deleted in this sync.
    delete = 'DELETE'
    #: No changes made on the external user in this sync.
    no_operation = 'NO_OPERATION'


class TriggerUserDirectorySyncResponse(ApiModel):
    #: User Directory sync response.
    userResponse: Optional[TriggerUserDirectorySyncResponseUserResponse] = None
    #: The Status of the operation being performed.
    #: example: ADD
    status: Optional[TriggerUserDirectorySyncResponseStatus] = None
