from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BroadWorksEnterprisesApi', 'Enterprise', 'EnterpriseBroadworksDirectorySync',
           'EnterpriseBroadworksDirectorySyncDirectorySyncStatus',
           'EnterpriseBroadworksDirectorySyncDirectorySyncStatusErrors', 'TriggerUserDirectorySyncResponse',
           'TriggerUserDirectorySyncResponseStatus', 'TriggerUserDirectorySyncResponseUserResponse',
           'UpdateDirectorySyncResponse', 'UpdateDirectorySyncResponseDirectorySyncStatus']


class EnterpriseBroadworksDirectorySyncDirectorySyncStatusErrors(ApiModel):
    #: An error code that identifies the reason for the error
    #: example: 6003
    error_code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Broadworks External Directory User Sync failed while trying to connect to Broadworks cluster.
    description: Optional[str] = None


class EnterpriseBroadworksDirectorySyncDirectorySyncStatus(ApiModel):
    #: The start date and time of the last sync.
    #: example: 2021-04-01T14:49:50.309640Z
    last_sync_start_time: Optional[datetime] = None
    #: The end date and time of the last sync.
    #: example: 2021-04-01T14:49:52.667189Z
    last_sync_end_time: Optional[datetime] = None
    #: The sync status of the enterprise.
    #: example: COMPLETE
    sync_status: Optional[str] = None
    #: The number of users added to Common Identity (CI) in this sync.
    #: example: 44
    users_added: Optional[int] = None
    #: The number of users updated in Common Identity (CI) in this sync.
    #: example: 21
    users_updated: Optional[int] = None
    #: The number of users deleted from Common Identity (CI) in this sync.
    #: example: 34
    users_deleted: Optional[int] = None
    #: The number of machines added to Common Identity (CI) in this sync.
    #: example: 24
    machines_added: Optional[int] = None
    #: The number of machines updated in Common Identity (CI) in this sync.
    #: example: 4
    machines_updated: Optional[int] = None
    #: The number of machines deleted from Common Identity (CI) in this sync.
    #: example: 9
    machines_deleted: Optional[int] = None
    #: The number of total external users that have been added to CI across all syncs.
    #: example: 1077
    total_external_users_in_ci: Optional[int] = Field(alias='totalExternalUsersInCI', default=None)
    #: The number of total external machines that have been added to Common Identity (CI) across all syncs.
    #: example: 326
    total_external_machines_in_ci: Optional[int] = Field(alias='totalExternalMachinesInCI', default=None)
    #: The date and time of the last successful sync.
    #: example: 2021-04-01T14:48:30.502539Z
    last_successful_sync_time: Optional[datetime] = None
    #: Unique tracking identifier.
    #: example: NA_dde3a13a-bad7-4990-b155-9b4574e545b9
    last_sync_tracking_id: Optional[str] = None
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures
    #: errors that occurred during *directory sync* of the BroadWorks enterprise, *after* the API has been accepted
    #: and 200 OK response returned. Any errors that occur during initial API request validation will be captured
    #: directly in error response with appropriate HTTP status code.
    errors: Optional[list[EnterpriseBroadworksDirectorySyncDirectorySyncStatusErrors]] = None
    #: The number of user contacts added to Contact service in this sync.
    #: example: 5
    user_contacts_added: Optional[int] = None
    #: The number of user contacts updated in Contact service in this sync.
    #: example: 2
    user_contacts_updated: Optional[int] = None
    #: The number of user contacts deleted from Contact service in this sync.
    #: example: 1
    user_contacts_deleted: Optional[int] = None
    #: The number of org contacts added to Contact service in this sync.
    #: example: 5
    org_contacts_added: Optional[int] = None
    #: The number of org contacts updated in Contact service in this sync.
    #: example: 2
    org_contacts_updated: Optional[int] = None
    #: The number of org contacts deleted from Contact service in this sync.
    #: example: 1
    org_contacts_deleted: Optional[int] = None
    #: The total number of user contacts in Contact service.
    #: example: 10
    total_user_contacts_in_contact_service: Optional[int] = None
    #: The total number of org contacts in Contact service.
    #: example: 2
    total_org_contacts_in_contact_service: Optional[int] = None


class EnterpriseBroadworksDirectorySync(ApiModel):
    #: The toggle to enable/disable directory sync.
    #: example: True
    enable_dir_sync: Optional[bool] = None
    #: Directory sync status
    directory_sync_status: Optional[EnterpriseBroadworksDirectorySyncDirectorySyncStatus] = None


class Enterprise(ApiModel):
    #: A unique Cisco identifier for the enterprise.
    #: example: Y2lzY29zcGFyazovL3VzL0VOVEVSUFJJU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: The Organization ID of the enterprise on Webex.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The Provisioning ID associated with the enterprise.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioning_id: Optional[str] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Reseller1+acme
    sp_enterprise_id: Optional[str] = None
    #: BroadWorks Directory sync
    broadworks_directory_sync: Optional[EnterpriseBroadworksDirectorySync] = None


class UpdateDirectorySyncResponseDirectorySyncStatus(ApiModel):
    #: The sync status of the enterprise.
    #: example: NOT_SYNCED
    sync_status: Optional[str] = None


class UpdateDirectorySyncResponse(ApiModel):
    #: The toggle to enable/disable directory sync.
    #: example: True
    enable_dir_sync: Optional[bool] = None
    #: Directory sync status
    directory_sync_status: Optional[UpdateDirectorySyncResponseDirectorySyncStatus] = None


class TriggerUserDirectorySyncResponseUserResponse(ApiModel):
    #: The UserID of the user on Broadworks (A non-webex user).
    #: example: john.anderson@acme.com
    user_id: Optional[str] = None
    #: First name of the user on Broadworks.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of the user on Broadworks.
    #: example: Anderson
    last_name: Optional[str] = None
    #: Extension of the user on Broadworks.
    #: example: 4653
    extension: Optional[str] = None
    #: Phone number of the user on Broadworks.
    #: example: +35391884653
    number: Optional[str] = None
    #: Mobile number of the user on Broadworks.
    #: example: +188-(2323)-(343)
    mobile: Optional[str] = None


class TriggerUserDirectorySyncResponseStatus(str, Enum):
    #: The external user is added in this sync
    add = 'ADD'
    #: The external user is updated in this sync
    update = 'UPDATE'
    #: The external user is deleted in this sync
    delete = 'DELETE'
    #: No changes made on the external user in this sync
    no_operation = 'NO_OPERATION'


class TriggerUserDirectorySyncResponse(ApiModel):
    #: User Directory sync response
    user_response: Optional[TriggerUserDirectorySyncResponseUserResponse] = None
    #: The Status of the operation being performed.
    #: example: ADD
    status: Optional[TriggerUserDirectorySyncResponseStatus] = None


class BroadWorksEnterprisesApi(ApiChild, base='broadworks/enterprises'):
    """
    BroadWorks Enterprises
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. They enable Service Providers to provision Webex Services for their subscribers. Please note
    these APIs require a functional BroadWorks system configured for Webex for BroadWorks. Read more about using this
    API
    at https://www.cisco.com/go/WebexBroadworksAPI.
    
    Viewing Webex for BroadWorks enterprise information requires an administrator auth token with
    `spark-admin:broadworks_enterprises_read` scope.
    Updating directory sync configuration or trigger directory sync for a Webex for BroadWorks enterprise require an
    administrator auth token with `spark-admin:broadworks_enterprises_write` scope.
    """

    def list_broad_works_enterprises(self, sp_enterprise_id: str = None, starts_with: str = None,
                                     **params) -> Generator[Enterprise, None, None]:
        """
        List BroadWorks Enterprises

        List the provisioned enterprises for a Service Provider. This API also lets a Service Provider search for their
        provisioned enterprises on Webex. A search on enterprises can be performed by either a full or partial
        enterprise identifier.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        :return: Generator yielding :class:`Enterprise` instances
        """
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Enterprise, item_key='items', params=params)

    def update_directory_sync_for_a_broad_works_enterprise(self, id: str,
                                                           enable_dir_sync: bool) -> UpdateDirectorySyncResponse:
        """
        Update Directory Sync for a BroadWorks Enterprise

        This API lets a Partner Admin enable or disable directory sync for the customer's Broadworks enterprise on
        Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool
        :rtype: :class:`UpdateDirectorySyncResponse`
        """
        body = dict()
        body['enableDirSync'] = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url, json=body)
        r = UpdateDirectorySyncResponse.model_validate(data)
        return r

    def trigger_directory_sync_for_an_enterprise(self, id: str, sync_status: str) -> UpdateDirectorySyncResponse:
        """
        Trigger Directory Sync for an Enterprise

        This API lets a Partner Admin trigger a directory sync for the customer's Broadworks enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param sync_status: At this time, the only value allowed for this attribute is `SYNC_NOW` which will trigger
            the directory sync for the BroadWorks enterprise.
        :type sync_status: str
        :rtype: :class:`UpdateDirectorySyncResponse`
        """
        body = dict()
        body['syncStatus'] = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url, json=body)
        r = UpdateDirectorySyncResponse.model_validate(data)
        return r

    def get_directory_sync_status_for_an_enterprise(self, id: str) -> EnterpriseBroadworksDirectorySync:
        """
        Get Directory Sync Status for an Enterprise

        This API lets a Partner Admin get the most recent directory sync status for a customer's Broadworks enterprise
        on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :rtype: :class:`EnterpriseBroadworksDirectorySync`
        """
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().get(url)
        r = EnterpriseBroadworksDirectorySync.model_validate(data)
        return r

    def trigger_directory_sync_for_a_user(self, id: str, user_id: str = None) -> TriggerUserDirectorySyncResponse:
        """
        Trigger Directory Sync for a User

        This API lets a Partner Admin trigger a directory sync for an external user (real or virtual user) on
        Broadworks enterprise with Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param user_id: The user ID of the Broadworks user to be synced (A non-webex user).
        :type user_id: str
        :rtype: :class:`TriggerUserDirectorySyncResponse`
        """
        body = dict()
        if user_id is not None:
            body['userId'] = user_id
        url = self.ep(f'{id}/broadworksDirectorySync/externalUser')
        data = super().post(url, json=body)
        r = TriggerUserDirectorySyncResponse.model_validate(data)
        return r
