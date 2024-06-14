from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaBroadWorksEnterprisesWithListEnterprisesEnhancementsApi', 'Enterprise',
           'EnterpriseBroadworksDirectorySync', 'EnterpriseBroadworksDirectorySyncDirectorySyncStatus',
           'EnterpriseBroadworksDirectorySyncDirectorySyncStatusErrors', 'TriggerDirectorySyncResponse',
           'TriggerDirectorySyncResponseDirectorySyncStatus', 'TriggerUserDirectorySyncResponse',
           'TriggerUserDirectorySyncResponseStatus', 'TriggerUserDirectorySyncResponseUserResponse']


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
    #: The number of users added to CI in this sync.
    #: example: 44
    users_added: Optional[int] = None
    #: The number of users updated in CI in this sync.
    #: example: 21
    users_updated: Optional[int] = None
    #: The number of users deleted from CI in this sync.
    #: example: 34
    users_deleted: Optional[int] = None
    #: The number of machines added to CI in this sync.
    #: example: 24
    machines_added: Optional[int] = None
    #: The number of machines updated in CI in this sync.
    #: example: 4
    machines_updated: Optional[int] = None
    #: The number of machines deleted from CI in this sync.
    #: example: 9
    machines_deleted: Optional[int] = None
    #: The number of total external users that have been added to CI across all syncs.
    #: example: 1077
    total_external_users_in_ci: Optional[int] = Field(alias='totalExternalUsersInCI', default=None)
    #: The number of total external machines that have been added to CI across all syncs.
    #: example: 326
    total_external_machines_in_ci: Optional[int] = Field(alias='totalExternalMachinesInCI', default=None)
    #: The date and time of the last successful sync.
    #: example: 2021-04-01T14:48:30.502539Z
    last_successful_sync_time: Optional[datetime] = None
    #: Unique tracking identifier.
    #: example: NA_dde3a13a-bad7-4990-b155-9b4574e545b9
    last_sync_tracking_id: Optional[str] = None
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures
    #: errors that occur during a directory sync of the BroadWorks enterprise, after the API has been accepted and a
    #: 200 OK response is returned. Any errors that occur during the initial API request validation will be captured
    #: directly in the error response with an appropriate HTTP status code.
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
    broadworks_directory_sync: Optional[EnterpriseBroadworksDirectorySync] = None


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
    extension: Optional[str] = None
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


class BetaBroadWorksEnterprisesWithListEnterprisesEnhancementsApi(ApiChild, base='broadworks/enterprises'):
    """
    Beta BroadWorks Enterprises with List Enterprises Enhancements
    
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
                                     last_sync_end_time: str = None, sync_status: str = None, after: str = None,
                                     **params) -> Generator[Enterprise, None, None]:
        """
        List BroadWorks Enterprises

        List the provisioned enterprises for a Service Provider.

        This API also allows a Service Provider to search for their provisioned enterprises on Cisco Webex. There are a
        number of filter options which can be combined in a single request.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        :param last_sync_end_time: Only include enterprises last synced after this date and time. Epoch time (in
            milliseconds) preferred, but ISO 8601 date format also accepted.
        :type last_sync_end_time: str
        :param sync_status: The directory sync status of the enterprise. This parameter supports multiple comma
            separated values. For example: status=failed,in_progress,not_synced.
        :type sync_status: str
        :param after: Only include enterprises created after this date and time. Epoch time (in milliseconds)
            preferred, but ISO 8601 date format also accepted.
        :type after: str
        :return: Generator yielding :class:`Enterprise` instances
        """
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        if last_sync_end_time is not None:
            params['lastSyncEndTime'] = last_sync_end_time
        if sync_status is not None:
            params['syncStatus'] = sync_status
        if after is not None:
            params['after'] = after
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Enterprise, item_key='items', params=params)

    def update_directory_sync_for_a_broad_works_enterprise(self, id: str,
                                                           enable_dir_sync: bool) -> TriggerDirectorySyncResponse:
        """
        Update Directory Sync for a BroadWorks Enterprise

        This API allows a Partner Admin to Update enableDirSync for the customer's Broadworks enterprise on Cisco
        Webex.

        :param id: Unique identifier for the enterprise.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool
        :rtype: :class:`TriggerDirectorySyncResponse`
        """
        body = dict()
        body['enableDirSync'] = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url, json=body)
        r = TriggerDirectorySyncResponse.model_validate(data)
        return r

    def trigger_directory_sync_for_an_enterprise(self, id: str, sync_status: str) -> TriggerDirectorySyncResponse:
        """
        Trigger Directory Sync for an Enterprise

        This API allows a Partner Admin to Trigger a directory sync for the customer's Broadworks enterprise on Cisco
        Webex.

        :param id: Unique identifier for the enterprise.
        :type id: str
        :param sync_status: The only option allowed for this attribute is SYNC_NOW which triggers the directory sync
            for the Broadworks enterprise.
        :type sync_status: str
        :rtype: :class:`TriggerDirectorySyncResponse`
        """
        body = dict()
        body['syncStatus'] = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url, json=body)
        r = TriggerDirectorySyncResponse.model_validate(data)
        return r

    def get_directory_sync_status_for_an_enterprise(self, id: str) -> EnterpriseBroadworksDirectorySync:
        """
        Get Directory Sync Status for an Enterprise

        This API allows a Partner Admin to Get the most recent directory sync status for a customer's Broadworks
        enterprise on Cisco Webex.

        :param id: Unique identifier for the enterprise.
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

        This API allows a Partner Admin to Trigger a directory sync for an external user (real or virtual) for a
        customer's Broadworks enterprise on Cisco Webex.

        :param id: Unique identifier for the enterprise.
        :type id: str
        :param user_id: The user ID of the non-Webex Broadworks user to be synced.
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
