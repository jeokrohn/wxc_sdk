from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field


__all__ = ['AcdObject', 'Action', 'Action3', 'ActivationStates', 'AlternateNumberSettings', 'AlternateNumbersWithPattern', 'AtaDtmfMethodObject', 'AtaDtmfModeObject', 'AtaObject', 'AudioCodecPriorityObject', 'AuthorizationCode', 'AvailableSharedLineMemberItem', 'BackgroundImage', 'BacklightTimerObject', 'BroadWorksEnterprisesWithDeleteOrgImprovementsApi', 'BroadWorksWorkspacesApi', 'BroadworksDirectorySync', 'CDR', 'CLIDPolicySelection', 'CallBounce', 'CallForwardingBusyGet', 'CallForwardingNoAnswerGet', 'CallForwardingPlaceSettingGet', 'CallForwardingPlaceSettingPatch', 'CallQueueQueueSettingsObject', 'CallType', 'CallType1', 'CallingPermission', 'ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse', 'ClientType', 'ComfortMessage', 'ComfortMessageBypass', 'CreateCallQueueResponse', 'CreatePersonBody', 'CustomizationDeviceLevelObject', 'CustomizationObject', 'DectDeviceList', 'DectObject', 'DefaultLoggingLevelObject', 'DeviceObject', 'DeviceOwner', 'Devices', 'Direction', 'DirectorySyncStatus', 'DisplayCallqueueAgentSoftkeysObject', 'DisplayNameSelection', 'DistinctiveRing', 'ErrorMessageObject', 'ErrorObject', 'Errors', 'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'GetAnnouncementFileInfo', 'GetChangeDeviceSettingsJobStatusResponse', 'GetDetailedCallHistoryResponse', 'GetDetailsForCallQueueResponse', 'GetDeviceMembersResponse', 'GetDeviceSettingsResponse', 'GetPersonPlaceCallQueueObject', 'GetSharedLineAppearanceMembersResponse', 'GetSharedLineMemberItem', 'GetUserDevicesResponse', 'GetWorkspaceDevicesResponse', 'Greeting', 'Hoteling', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'InterceptAnnouncementsGet', 'InterceptAnnouncementsPatch', 'InterceptIncomingGet', 'InterceptIncomingPatch', 'InterceptNumberGet', 'InterceptOutGoingGet', 'ItemObject', 'JobExecutionStatusObject', 'KemModuleTypeObject', 'LineKeyLEDPattern', 'LineKeyLabelSelection', 'LineType', 'ListBroadWorksEnterprisesResponse', 'ListChangeDeviceSettingsJobErrorsResponse', 'ListChangeDeviceSettingsJobsResponse', 'ListJobResponse', 'ListPeopleResponse', 'MacStatusObject', 'ManagedByObject', 'ManufacturerObject', 'MemberObject', 'MemberType', 'ModifyPersonPlaceCallQueueObject', 'MohMessage', 'MonitoredElementCallParkExtension', 'MonitoredElementItem', 'MonitoredElementUser', 'MppAudioCodecPriorityObject', 'MppObject', 'MppVlanObject', 'NormalSource', 'OnboardingMethodObject', 'OriginalReason', 'Overflow', 'PeoplewithCallingApi', 'Person', 'PhoneLanguage', 'PhoneNumbers', 'PlaceDevices', 'PostCallQueueCallPolicyObject', 'PostPersonPlaceCallQueueObject', 'ProvisionBroadWorksWorkspaceBody', 'ProvisionBroadWorksWorkspaceResponse', 'PutMemberObject', 'PutSharedLineMemberItem', 'ReadCallInterceptSettingsForWorkspaceResponse', 'ReadDECTDeviceTypeListResponse', 'ReadListOfCallQueueAnnouncementFilesResponse', 'ReadListOfSupportedDevicesResponse', 'ReaddeviceOverrideSettingsFororganizationResponse', 'RedirectReason', 'RelatedReason', 'RetrieveAccessCodesForWorkspaceResponse', 'RetrieveCallForwardingSettingsForWorkspaceResponse', 'RetrieveCallWaitingSettingsForWorkspaceResponse', 'RetrieveCallerIDSettingsForWorkspaceResponse', 'RetrieveIncomingPermissionSettingsForWorkspaceResponse', 'RetrieveMonitoringSettingsForWorkspaceResponse', 'RetrieveOutgoingPermissionSettingsForWorkspaceResponse', 'RetrieveTransferNumbersSettingsForWorkspaceResponse', 'RingPatternObject', 'SearchMemberObject', 'SearchMembersResponse', 'SearchSharedLineAppearanceMembersResponse', 'SelectionType', 'State', 'Status', 'Status1', 'Status6', 'StepExecutionStatusesObject', 'TriggerDirectorySyncForUserResponse', 'Type', 'Type6', 'Type7', 'TypeObject', 'UpdateBroadworksWorkspaceBody', 'UpdateCallQueueBody', 'UpdateDeviceSettingsBody', 'UserNumberItem', 'UserResponse', 'UserType', 'ValidatelistOfMACAddressResponse', 'VlanObject', 'WaitMessage', 'WaitMode', 'WebexCallingDetailedCallHistoryApi', 'WebexCallingOrganizationSettingsWithAgentJoinUnjoinAndAnnouncementFeaturesApi', 'WebexCallingOrganizationSettingswithDevicesFeaturesApi', 'WebexCallingPersonSettingsWithSharedLineApi', 'WebexCallingPersonSettingswithCallingBehaviorApi', 'WebexforBroadworksphonelistsyncApi', 'WelcomeMessage', 'WifiNetworkObject']


class Errors(ApiModel):
    #: An error code that identifies the reason for the error
    #: Possible values: 6003
    error_code: Optional[int]
    #: A textual representation of the error code.
    #: Possible values: Broadworks External Directory User Sync failed while trying to connect to Broadworks cluster.
    description: Optional[str]


class DirectorySyncStatus(ApiModel):
    #: The start date and time of the last sync.
    last_sync_start_time: Optional[str]
    #: The end date and time of the last sync.
    last_sync_end_time: Optional[str]
    #: The sync status of the enterprise.
    sync_status: Optional[str]
    #: The number of users added to CI (Common Identity) in this sync.
    users_added: Optional[int]
    #: The number of users updated in CI (Common Identity)  in this sync.
    users_updated: Optional[int]
    #: The number of users deleted from CI (Common Identity)  in this sync.
    users_deleted: Optional[int]
    #: The number of machines added to CI (Common Identity)  in this sync.
    machines_added: Optional[int]
    #: The number of machines updated in CI (Common Identity)  in this sync.
    machines_updated: Optional[int]
    #: The number of machines deleted from CI (Common Identity)  in this sync.
    machines_deleted: Optional[int]
    #: The number of total external users that have been added to CI across all syncs.
    total_external_users_in_ci: Optional[int]
    #: The number of total external machines that have been added to CI (Common Identity)  across all syncs.
    total_external_machines_in_ci: Optional[int]
    #: The date and time of the last successful sync.
    last_successful_sync_time: Optional[str]
    #: Unique tracking identifier.
    last_sync_tracking_id: Optional[str]
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures errors that occurred during directory sync of the BroadWorks enterprise, after the API has been accepted and 200 OK response returned. Any errors that occur during initial API request validation will be captured directly in error response with appropriate HTTP status code.
    errors: Optional[list[Errors]]
    #: The number of user contacts added to Contact service in this sync.
    user_contacts_added: Optional[int]
    #: The number of user contacts updated in Contact service in this sync.
    user_contacts_updated: Optional[int]
    #: The number of user contacts deleted from Contact service in this sync.
    user_contacts_deleted: Optional[int]
    #: The number of org contacts added to Contact service in this sync.
    org_contacts_added: Optional[int]
    #: The number of org contacts updated in Contact service in this sync.
    org_contacts_updated: Optional[int]
    #: The number of org contacts deleted from Contact service in this sync.
    org_contacts_deleted: Optional[int]
    #: The total number of user contacts in Contact service.
    total_user_contacts_in_contact_service: Optional[int]
    #: The total number of org contacts in Contact service.
    total_org_contacts_in_contact_service: Optional[int]


class BroadworksDirectorySync(ApiModel):
    #: The toggle to enable/disable directory sync.
    enable_dir_sync: Optional[bool]
    #: Directory sync status
    directory_sync_status: Optional[DirectorySyncStatus]


class UserResponse(ApiModel):
    #: The UserID of the user on Broadworks (A non-webex user).
    user_id: Optional[str]
    #: First Name of the user on Broadworks.
    first_name: Optional[str]
    #: Last Name of the user on Broadworks.
    last_name: Optional[str]
    #: Extension of the user on Broadworks.
    extension: Optional[str]
    #: Phone number of the user on Broadworks.
    number: Optional[str]
    #: Mobile number of the user on Broadworks.
    mobile: Optional[str]


class Status(str, Enum):
    #: The external user is added in this sync
    add = 'ADD'
    #: The external user is updated in this sync
    update = 'UPDATE'
    #: The external user is deleted in this sync
    delete = 'DELETE'
    #: No changes made on the external user in this sync
    no_operation = 'NO_OPERATION'


class ListBroadWorksEnterprisesResponse(ApiModel):
    #: A unique Cisco identifier for the enterprise.
    id: Optional[str]
    #: The Organization ID of the enterprise on Cisco Webex.
    org_id: Optional[str]
    #: The Provisioning ID associated with the enterprise.
    provisioning_id: Optional[str]
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    sp_enterprise_id: Optional[str]
    #: BroadWorks Directory sync
    broadworks_directory_sync: Optional[BroadworksDirectorySync]


class UpdateDirectorySyncForBroadWorksEnterpriseBody(ApiModel):
    #: The toggle to enable/disable directory sync.
    enable_dir_sync: Optional[bool]


class TriggerDirectorySyncForEnterpriseBody(ApiModel):
    #: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for the BroadWorks enterprise.
    sync_status: Optional[str]


class TriggerDirectorySyncForUserBody(ApiModel):
    #: The user ID of the Broadworks user to be synced (A non-webex user).
    user_id: Optional[str]


class TriggerDirectorySyncForUserResponse(ApiModel):
    #: User Directory sync response
    user_response: Optional[UserResponse]
    #: The Status of the operation being performed.
    status: Optional[Status]


class BroadWorksEnterprisesWithDeleteOrgImprovementsApi(ApiChild, base='broadworks/enterprises'):
    """

    """

    def list_broad_works_enterprises(self, sp_enterprise_id: str = None, starts_with: str = None, **params) -> Generator[ListBroadWorksEnterprisesResponse, None, None]:
        """
        List the provisioned enterprises for a Service Provider. This API also allows a Service Provider to search for their provisioned enterprises on Webex. A search on enterprises can be performed using either a full or partial enterprise identifier.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        """
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListBroadWorksEnterprisesResponse, params=params)

    def update_sync_for_broad_works_enterprise(self, id: str, enable_dir_sync: bool) -> BroadworksDirectorySync:
        """
        This API allows a Partner Admin to update enableDirSync for the customer's Broadworks enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool
        """
        body = UpdateDirectorySyncForBroadWorksEnterpriseBody()
        if enable_dir_sync is not None:
            body.enable_dir_sync = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_enterprise(self, id: str, sync_status: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to trigger a directory sync for the customer's Broadworks enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param sync_status: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for the BroadWorks enterprise.
        :type sync_status: str
        """
        body = TriggerDirectorySyncForEnterpriseBody()
        if sync_status is not None:
            body.sync_status = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def sync_status_for_enterprise(self, id: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to  get the most recent directory sync status for a customer's Broadworks enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        """
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().get(url=url)
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_user(self, id: str, user_id: str = None) -> TriggerDirectorySyncForUserResponse:
        """
        This API allows a Partner Admin to trigger a directory sync for an external user (real or virtual user) on Broadworks enterprise with Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param user_id: The user ID of the Broadworks user to be synced (A non-webex user).
        :type user_id: str
        """
        body = TriggerDirectorySyncForUserBody()
        if user_id is not None:
            body.user_id = user_id
        url = self.ep(f'{id}/broadworksDirectorySync/externalUser')
        data = super().post(url=url, data=body.json())
        return TriggerDirectorySyncForUserResponse.parse_obj(data)

class UpdateBroadworksWorkspaceBody(ApiModel):
    #: The user ID of the workspace on BroadWorks.
    user_id: Optional[str]
    #: The primary phone number configured against the workspace on BroadWorks.
    primary_phone_number: Optional[str]
    #: The extension number configured against the workspace on BroadWorks.
    extension: Optional[str]


class ProvisionBroadWorksWorkspaceBody(UpdateBroadworksWorkspaceBody):
    #: This Provisioning ID defines how this workspace is to be provisioned for Cisco Webex Services. Each Customer Template will have their own unique Provisioning ID. This ID will be displayed under the chosen Customer Template on Cisco Webex Control Hub.
    provisioning_id: Optional[str]
    #: The Service Provider supplied unique identifier for the workspace's enterprise.
    sp_enterprise_id: Optional[str]
    #: The display name of the workspace.
    display_name: Optional[str]


class ProvisionBroadWorksWorkspaceResponse(ProvisionBroadWorksWorkspaceBody):
    #: A unique Cisco identifier for the workspace.
    id: Optional[str]
    #: The date and time the workspace was provisioned.
    created: Optional[str]


class BroadWorksWorkspacesApi(ApiChild, base='broadworks/workspaces'):
    """

    """

    def provision_broad_works(self, provisioning_id: str, sp_enterprise_id: str, display_name: str, user_id: str = None, primary_phone_number: str = None, extension: str = None) -> ProvisionBroadWorksWorkspaceResponse:
        """
        Provision a new BroadWorks workspace for Cisco Webex services.
        This API will allow a Service Provider to provision a workspace for an existing customer.

        :param provisioning_id: This Provisioning ID defines how this workspace is to be provisioned for Cisco Webex Services. Each Customer Template will have their own unique Provisioning ID. This ID will be displayed under the chosen Customer Template on Cisco Webex Control Hub.
        :type provisioning_id: str
        :param sp_enterprise_id: The Service Provider supplied unique identifier for the workspace's enterprise.
        :type sp_enterprise_id: str
        :param display_name: The display name of the workspace.
        :type display_name: str
        :param user_id: The user ID of the workspace on BroadWorks.
        :type user_id: str
        :param primary_phone_number: The primary phone number configured against the workspace on BroadWorks.
        :type primary_phone_number: str
        :param extension: The extension number configured against the workspace on BroadWorks.
        :type extension: str
        """
        body = ProvisionBroadWorksWorkspaceBody()
        if provisioning_id is not None:
            body.provisioning_id = provisioning_id
        if sp_enterprise_id is not None:
            body.sp_enterprise_id = sp_enterprise_id
        if display_name is not None:
            body.display_name = display_name
        if user_id is not None:
            body.user_id = user_id
        if primary_phone_number is not None:
            body.primary_phone_number = primary_phone_number
        if extension is not None:
            body.extension = extension
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return ProvisionBroadWorksWorkspaceResponse.parse_obj(data)

    def update_broadworks(self, workspace_id: str, user_id: str = None, primary_phone_number: str = None, extension: str = None) -> ProvisionBroadWorksWorkspaceResponse:
        """
        This API will allow a Service Provider to update certain details of a provisioned BroadWorks workspace on Cisco Webex.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str
        :param user_id: The user ID of the workspace on BroadWorks.
        :type user_id: str
        :param primary_phone_number: The primary phone number configured against the workspace on BroadWorks.
        :type primary_phone_number: str
        :param extension: The extension number configured against the workspace on BroadWorks.
        :type extension: str
        """
        body = UpdateBroadworksWorkspaceBody()
        if user_id is not None:
            body.user_id = user_id
        if primary_phone_number is not None:
            body.primary_phone_number = primary_phone_number
        if extension is not None:
            body.extension = extension
        url = self.ep(f'{workspace_id}')
        data = super().put(url=url, data=body.json())
        return ProvisionBroadWorksWorkspaceResponse.parse_obj(data)

    def remove_broad_works(self, workspace_id: str):
        """
        This API will allow a Service Provider to remove the mapping between a BroadWorks workspace and Cisco Webex device.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url=url)
        return

class Status1(str, Enum):
    #: active within the last 10 minutes
    active = 'active'
    #: the user is in a call
    call = 'call'
    #: the user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: last activity occurred more than 10 minutes ago
    inactive = 'inactive'
    #: the user is in a meeting
    meeting = 'meeting'
    #: the user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: the user has never logged in; a status cannot be determined
    pending = 'pending'
    #: the user is sharing content
    presenting = 'presenting'
    #: the user’s status could not be determined
    unknown = 'unknown'


class Type(str, Enum):
    #: account belongs to a person
    person = 'person'
    #: account is a bot user
    bot = 'bot'
    #: account is a guest user
    appuser = 'appuser'


class PhoneNumbers(ApiModel):
    #: The type of phone number.
    #: Possible values: work, mobile, fax
    type: Optional[str]
    #: The phone number.
    #: Possible values: +1 408 526 7209
    value: Optional[str]


class CreatePersonBody(ApiModel):
    #: The email addresses of the person. Only one email address is allowed per person.
    #: Possible values: john.andersen@example.com
    emails: Optional[list[str]]
    #: Phone numbers for the person.
    phone_numbers: Optional[list[PhoneNumbers]]
    #: The extension of the person retrieved from BroadCloud.
    extension: Optional[str]
    #: The ID of the location for this person retrieved from BroadCloud.
    location_id: Optional[str]
    #: The full name of the person.
    display_name: Optional[str]
    #: The first name of the person.
    first_name: Optional[str]
    #: The last name of the person.
    last_name: Optional[str]
    #: The URL to the person's avatar in PNG format.
    avatar: Optional[str]
    #: The ID of the organization to which this person belongs.
    org_id: Optional[str]
    #: An array of role strings representing the roles to which this person belongs.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    licenses: Optional[list[str]]


class Person(CreatePersonBody):
    #: A unique identifier for the person.
    id: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be present.
    nick_name: Optional[str]
    #: The date and time the person was created.
    created: Optional[str]
    #: The date and time the person was last changed.
    last_modified: Optional[str]
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex.
    last_activity: Optional[str]
    #: The current presence status of the person.
    status: Optional[Status1]
    #: Whether or not an invite is pending for the user to complete account activation.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex.
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    type: Optional[Type]


class ListPeopleResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]]
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]]


class PeoplewithCallingApi(ApiChild, base='people'):
    """

    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin users can omit these fields and list all users in their organization.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData parameter as true. Admin users can list all users in a location or with a specific phone number.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are required.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners) may use this parameter.
        :type org_id: str
        :param calling_data: Include BroadCloud user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str
        """
        if email is not None:
            params['email'] = email
        if display_name is not None:
            params['displayName'] = display_name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        if calling_data is not None:
            params['callingData'] = calling_data
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Person, params=params)

    def create(self, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        Admin users can include BroadCloud user details in the response by specifying callingData parameter as true.
        Currently, users may have only one email address associated with their account. The emails parameter is an array, which accepts multiple values to allow for future expansion, but currently only one email address will be used for the new user.

        :param emails: The email addresses of the person. Only one email address is allowed per person.
Possible values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include BroadCloud user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person.
        :type phone_numbers: PhoneNumbers
        :param extension: The extension of the person retrieved from BroadCloud.
        :type extension: str
        :param location_id: The ID of the location for this person retrieved from BroadCloud.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this person belongs.
Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person.
Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        body = CreatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID. Certain fields, such as status or lastActivity, will only be displayed for people within your organization or an organization you manage.
        Admin users can include BroadCloud user details in the response by specifying callingData parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include BroadCloud user details in the response.
        :type calling_data: bool
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include BroadCloud user details in the response by specifying callingData parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is already an existing calling user.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param emails: The email addresses of the person. Only one email address is allowed per person.
Possible values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include BroadCloud user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person.
        :type phone_numbers: PhoneNumbers
        :param extension: The extension of the person retrieved from BroadCloud.
        :type extension: str
        :param location_id: The ID of the location for this person retrieved from BroadCloud.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this person belongs.
Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person.
Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        body = CreatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def delete(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        """
        url = self.ep(f'{person_id}')
        super().delete(url=url)
        return

    def my_own_details(self, calling_data: bool = None) -> Person:
        """
        Show the profile for the authenticated user. This is the same as GET /people/{personId} using the Person ID associated with your Auth token.
        Admin users can include BroadCloud user details in the response by specifying callingData parameter as true.

        :param calling_data: Include BroadCloud user details in the response.
        :type calling_data: bool
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

class CallType(str, Enum):
    sip_meeting = 'SIP_MEETING'
    sip_international = 'SIP_INTERNATIONAL'
    sip_shortcode = 'SIP_SHORTCODE'
    sip_inbound = 'SIP_INBOUND'
    unknown = 'UNKNOWN'
    sip_emergency = 'SIP_EMERGENCY'
    sip_premium = 'SIP_PREMIUM'
    sip_enterprise = 'SIP_ENTERPRISE'
    sip_tollfree = 'SIP_TOLLFREE'
    sip_national = 'SIP_NATIONAL'
    sip_mobile = 'SIP_MOBILE'


class ClientType(str, Enum):
    sip = 'SIP'
    wxc_client = 'WXC_CLIENT'
    wxc_third_party = 'WXC_THIRD_PARTY'
    teams_wxc_client = 'TEAMS_WXC_CLIENT'
    wxc_device = 'WXC_DEVICE'
    wxc_sip_gw = 'WXC_SIP_GW'


class Direction(str, Enum):
    originating = 'ORIGINATING'
    terminating = 'TERMINATING'


class OriginalReason(str, Enum):
    unconditional = 'Unconditional'
    no_answer = 'NoAnswer'
    call_queue = 'CallQueue'
    time_of_day = 'TimeOfDay'
    user_busy = 'UserBusy'
    follow_me = 'FollowMe'
    unrecognised = 'Unrecognised'
    unknown = 'Unknown'


class RedirectReason(str, Enum):
    unconditional = 'Unconditional'
    no_answer = 'NoAnswer'
    call_queue = 'CallQueue'
    time_of_day = 'TimeOfDay'
    user_busy = 'UserBusy'
    follow_me = 'FollowMe'
    hunt_group = 'HuntGroup'
    deflection = 'Deflection'
    unknown = 'Unknown'
    unavailable = 'Unavailable'


class RelatedReason(str, Enum):
    consultative_transfer = 'ConsultativeTransfer'
    call_forward_selective = 'CallForwardSelective'
    call_queue = 'CallQueue'
    unrecognised = 'Unrecognised'
    call_pickup = 'CallPickup'
    call_forward_always = 'CallForwardAlways'
    fax_deposit = 'FaxDeposit'
    hunt_group = 'HuntGroup'
    push_notification_retrieval = 'PushNotificationRetrieval'
    voice_xml_script_termination = 'VoiceXMLScriptTermination'
    call_forward_no_answer = 'CallForwardNoAnswer'
    anywhere_location = 'AnywhereLocation'


class UserType(str, Enum):
    automated_attendant_video = 'AutomatedAttendantVideo'
    anchor = 'Anchor'
    broadworks_anywhere = 'BroadworksAnywhere'
    voice_mail_retrieval = 'VoiceMailRetrieval'
    local_gateway = 'LocalGateway'
    hunt_group = 'HuntGroup'
    group_paging = 'GroupPaging'
    user = 'User'
    voice_mail_group = 'VoiceMailGroup'
    call_center_standard = 'CallCenterStandard'
    voice_xml = 'VoiceXML'
    route_point = 'RoutePoint'


class CDR(ApiModel):
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[str] = Field(alias='Answer time')
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered, and one will be answered.
    answered: Optional[str]
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call if necessary.
    call_id: Optional[str] = Field(alias='Call ID')
    #: Type of call. For example:
    call_type: Optional[CallType] = Field(alias='Call type')
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the called party.
    called_line_id: Optional[str] = Field(alias='Called line ID')
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the called party.
    called_number: Optional[str] = Field(alias='Called number')
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of the user.
    calling_line_id: Optional[str] = Field(alias='Calling line ID')
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number of the user.
    calling_number: Optional[str] = Field(alias='Calling number')
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    client_type: Optional[ClientType] = Field(alias='Client type')
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str] = Field(alias='Client version')
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str] = Field(alias='Correlation ID')
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = Field(alias='Device MAC')
    #: Whether the call was inbound or outbound. The possible values are:
    direction: Optional[Direction]
    #: The length of the call in seconds.
    duration: Optional[int]
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk')
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str] = Field(alias='International country')
    #: Location of the report.
    location: Optional[str]
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str] = Field(alias='Org UUID')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    original_reason: Optional[OriginalReason] = Field(alias='Original reason')
    #: The operating system that the app was running on, if available.
    os_type: Optional[str] = Field(alias='OS type')
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    redirect_reason: Optional[RedirectReason] = Field(alias='Redirect reason')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    related_reason: Optional[RelatedReason] = Field(alias='Related reason')
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str] = Field(alias='Report ID')
    #: The time this report was created. Time is in UTC.
    report_time: Optional[str] = Field(alias='Report time')
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex Calling (dial plan or unknown extension).
    route_group: Optional[str] = Field(alias='Route group')
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str] = Field(alias='Site main number')
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str] = Field(alias='Site timezone')
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC. 
    start_time: Optional[str] = Field(alias='Start time')
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type will show MOBILE_NETWORK.
    sub_client_type: Optional[str] = Field(alias='Sub client type')
    #: The type of user (user or workspace) that made or received the call. For example:
    user_type: Optional[UserType] = Field(alias='User type')
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = Field(alias='User UUID')


class GetDetailedCallHistoryResponse(ApiModel):
    items: Optional[list[CDR]]


class WebexCallingDetailedCallHistoryApi(ApiChild, base=''):
    """

    """

    def detailed_call_history(self, start_time: str, end_time: str, locations: str = None, max: int = None) -> List[CDR]:
        """
        Provides Webex Calling Detailed Call History data for your organization.
        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime parameters specify the start and end of the time period for the Detailed Call History reports you wish to collect. The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished). Note: The specified time must be between 5 minutes ago and 48 hours ago, and be formatted as YYYY-MM-DDTHH:MM:SS.mmmZ.
        :type start_time: str
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than startTime and no earlier than 48 hours ago, and be formatted as YYYY-MM-DDTHH:MM:SS.mmmZ.
        :type end_time: str
        :param locations: Name of the location (as shown in Control Hub). Up to 10 comma-separated locations can be provided. Allows you to query reports by location.
        :type locations: str
        :param max: Limit the maximum number of reports in the response. Range is 1 to 500. When the API has more reports to return than the max value, the API response will be paginated.
        :type max: int
        """
        params = {}
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
            params['endTime'] = end_time
        if locations is not None:
            params['locations'] = locations
        if max is not None:
            params['max'] = max
        url = self.ep('https://analytics.webexapis.com/v1/cdr_feed')
        data = super().get(url=url, params=params)
        return data["items"]

class HuntRoutingTypeSelection(ApiModel):
    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based: Optional[str]
    #: This option uses skill level as the criteria to route calls to agents. When there is more than one agent with the same skill level, the selected policy helps dispatch the calls to the agents.
    skill_based: Optional[str]


class HuntPolicySelection(ApiModel):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next available agent. This is supported in SKILL_BASED.
    circular: Optional[str]
    #: Send the call through the queue of agents in order, starting from the top each time. This is supported in SKILL_BASED.
    regular: Optional[str]
    #: Sends calls to all agents at once
    simultaneous: Optional[str]
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has been idle the second longest, and so on until the call is answered. This is supported in SKILL_BASED.
    uniform: Optional[str]
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100%).
    weighted: Optional[str]


class CallBounce(ApiModel):
    #: If enabled, bounce calls after the set number of rings.
    call_bounce_enabled: Optional[bool]
    #: Number of rings after which to bounce call, if call bounce is enabled.
    call_bounce_max_rings: Optional[int]
    #: Bounce if agent becomes unavailable.
    agent_unavailable_enabled: Optional[bool]
    #: Alert agent if call on hold more than alertAgentMaxSeconds.
    alert_agent_enabled: Optional[bool]
    #: Number of second after which to alert agent if alertAgentEnabled.
    alert_agent_max_seconds: Optional[int]
    #: Bounce if call on hold more than callBounceMaxSeconds.
    call_bounce_on_hold_enabled: Optional[bool]
    #: Number of second after which to bounce if callBounceEnabled.
    call_bounce_on_hold_max_seconds: Optional[int]


class RingPatternObject(ApiModel):
    #: Normal incoming ring pattern.
    normal: Optional[str]
    #: Incoming ring pattern of two long rings.
    long_long: Optional[str]
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long: Optional[str]
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short: Optional[str]


class DistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    enabled: Optional[bool]
    #: Ring pattern for when this call queue is called. Only available when distinctiveRing is enabled for the call queue.
    ring_pattern: Optional[RingPatternObject]


class PostCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents. The routing type should be SKILL_BASED if you want to assign skill level to agents. Only certain policy are allowed in SKILL_BASED type.
    routing_type: Optional[HuntRoutingTypeSelection]
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: Settings for when the call into the hunt group is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[DistinctiveRing]


class Action(str, Enum):
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class Greeting(str, Enum):
    #: Play the custom announcement specified by the fileName field.
    custom = 'CUSTOM'
    #: Play default announcement.
    default = 'DEFAULT'


class Overflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[Action]
    #: When true, forwards all calls to a voicemail service of an internal number. This option is ignored when an external transferNumber is entered.
    send_to_voicemail: Optional[bool]
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str]
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is triggered.
    overflow_after_wait_enabled: Optional[bool]
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. Min 0, Max 7200 seconds.
    overflow_after_wait_time: Optional[int]
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by a user.
    play_overflow_greeting_enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement fileName strings to be played as overflow greetings. These files are from the list of announcement files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class NormalSource(ApiModel):
    #: Enable media on hold for queued calls.
    enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement fileName strings to be played as mohMessage greetings. These files are from the list of announcement files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class WelcomeMessage(NormalSource):
    #: Mandatory entrance message. The default value is false.
    always_enabled: Optional[bool]


class WaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class WaitMessage(ApiModel):
    #: Wait message enable or not.
    enabled: Optional[bool]
    #: Estimated wait message operating mode. Supported values TIME and POSITION.
    wait_mode: Optional[WaitMode]
    #: The number of minutes for which the estimated wait is played. Min 10, Max 100 minutes.
    handling_time: Optional[int]
    #: The default number of call handling minutes. Min 1, Max 100 minutes.
    default_handling_time: Optional[int]
    #: The number of the position for which the estimated wait is played. Min 10, Max 100 positions.
    queue_position: Optional[int]
    #: Play time / Play position High Volume.
    high_volume_message_enabled: Optional[bool]
    #: The number of estimated waiting times in seconds. Min 10, Max 600 seconds.
    estimated_waiting_time: Optional[int]
    #: Callback options enabled/disabled. Default value is false.
    callback_option_enabled: Optional[bool]
    #: The minimum estimated callback times in minutes. The default value is 30.
    minimum_estimated_callback_time: Optional[int]
    #: The international numbers for callback is enabled/disabled. The default value is false.
    international_callback_enabled: Optional[bool]
    #: Play updated estimated wait message.
    play_updated_estimated_wait_message: Optional[str]


class ComfortMessage(NormalSource):
    #: The interval in seconds between each repetition of the comfort message played to queued users. Min 10, Max 600 seconds.
    time_between_messages: Optional[int]


class ComfortMessageBypass(NormalSource):
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. Min 1, Max 120 seconds.
    call_waiting_age_threshold: Optional[int]


class MohMessage(ApiModel):
    normal_source: Optional[NormalSource]
    alternate_source: Optional[NormalSource]


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are triggered.
    queue_size: Optional[int]
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool]
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool]
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[Overflow]
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call queue while there is an available agent, the caller will not hear this announcement and is transferred to an agent. By default, it is enabled with default configurations.
    welcome_message: Optional[WelcomeMessage]
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[WaitMessage]
    #: Play a message after the welcome message and before hold music. This is typically a custom announcement that plays information, such as current promotions or information about products and services.
    comfort_message: Optional[ComfortMessage]
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[ComfortMessageBypass]
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[MohMessage]
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces the identity of the call queue from which the call is coming.
    whisper_message: Optional[NormalSource]


class PostPersonPlaceCallQueueObject(ApiModel):
    #: ID of person or workspace.
    id: Optional[str]
    #: Weight of person or workspace. Only applied when call policy is WEIGHTED.
    weight: Optional[str]
    #: Skill level of person or workspace. Only applied when call routing type is SKILL_BASED.
    skill_level: Optional[int]


class GetPersonPlaceCallQueueObject(PostPersonPlaceCallQueueObject):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: First name of person or workspace.
    last_name: Optional[str]
    #: Phone number of person or workspace.
    phone_number: Optional[str]
    #: Extension of person or workspace.
    extension: Optional[str]
    #: Indicates the join status of the agent for this queue. The default value while creating call queue is true.
    join_enabled: Optional[bool]


class AlternateNumbersWithPattern(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the hunt group.
    ring_pattern: Optional[RingPatternObject]


class AlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns set for the Alternate Number.
    distinctive_ring_enabled: Optional[bool]
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]


class ModifyPersonPlaceCallQueueObject(PostPersonPlaceCallQueueObject):
    #: Indicates the join status of the agent for this queue. The default value for newly added agents is true.
    join_enabled: Optional[bool]


class UpdateCallQueueBody(ApiModel):
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]
    #: Unique name for the call queue.
    name: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Extension of the call queue.
    extension: Optional[str]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[ModifyPersonPlaceCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]


class GetAnnouncementFileInfo(ApiModel):
    #: Name of greeting file.
    file_name: Optional[str]
    #: Size of greeting file in bytes.
    file_size: Optional[str]


class CreateCallQueueBody(ApiModel):
    #: Unique name for the call queue.
    name: Optional[str]
    #: Primary phone number of the call queue. Either phone number or extension is mandatory.
    phone_number: Optional[str]
    #: Primary phone extension of the call queue. Either phone number or extension is mandatory.
    extension: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]


class CreateCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class GetDetailsForCallQueueResponse(UpdateCallQueueBody):
    #: A unique identifier for the call queue.
    id: Optional[str]
    #: Language for the call queue.
    language: Optional[str]
    #: Language for the call queue.
    language: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceCallQueueObject]]


class ReadListOfCallQueueAnnouncementFilesResponse(ApiModel):
    #: Array of announcements for this call queue.
    announcements: Optional[list[GetAnnouncementFileInfo]]


class WebexCallingOrganizationSettingsWithAgentJoinUnjoinAndAnnouncementFeaturesApi(ApiChild, base='telephony/config/locations/{locationId}/queues'):
    """

    """

    def create_queue(self, location_id: str, name: str, call_policies: PostCallQueueCallPolicyObject, queue_settings: CallQueueQueueSettingsObject, agents: PostPersonPlaceCallQueueObject, org_id: str = None, phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, allow_agent_join_enabled: bool = None) -> str:
        """
        Create new Call Queues for the given location.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Creating a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param name: Unique name for the call queue.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param agents: People, including workspaces, that are eligible to receive calls.
        :type agents: PostPersonPlaceCallQueueObject
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :param phone_number: Primary phone number of the call queue. Either phone number or extension is mandatory.
        :type phone_number: str
        :param extension: Primary phone extension of the call queue. Either phone number or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the call queue.
        :type time_zone: str
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallQueueBody()
        if name is not None:
            body.name = name
        if call_policies is not None:
            body.call_policies = call_policies
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if agents is not None:
            body.agents = agents
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if time_zone is not None:
            body.time_zone = time_zone
        if allow_agent_join_enabled is not None:
            body.allow_agent_join_enabled = allow_agent_join_enabled
        url = self.ep(f'')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_queue(self, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete the designated Call Queue.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Deleting a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{queue_id}')
        super().delete(url=url, params=params)
        return

    def details_for_queue(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueResponse:
        """
        Retrieve Call Queue details.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{queue_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueResponse.parse_obj(data)

    def update_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsObject, org_id: str = None, enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, phone_number: str = None, extension: str = None, alternate_number_settings: AlternateNumberSettings = None, call_policies: PostCallQueueCallPolicyObject = None, allow_call_waiting_for_agents_enabled: bool = None, agents: ModifyPersonPlaceCallQueueObject = None, allow_agent_join_enabled: bool = None):
        """
        Update the designated Call Queue.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Updating a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param enabled: Whether or not the call queue is enabled.
        :type enabled: bool
        :param name: Unique name for the call queue.
        :type name: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param phone_number: Primary phone number of the call queue.
        :type phone_number: str
        :param extension: Extension of the call queue.
        :type extension: str
        :param alternate_number_settings: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
        :type alternate_number_settings: AlternateNumberSettings
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, including workspaces, that are eligible to receive calls.
        :type agents: ModifyPersonPlaceCallQueueObject
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueBody()
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if enabled is not None:
            body.enabled = enabled
        if name is not None:
            body.name = name
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if time_zone is not None:
            body.time_zone = time_zone
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if alternate_number_settings is not None:
            body.alternate_number_settings = alternate_number_settings
        if call_policies is not None:
            body.call_policies = call_policies
        if allow_call_waiting_for_agents_enabled is not None:
            body.allow_call_waiting_for_agents_enabled = allow_call_waiting_for_agents_enabled
        if agents is not None:
            body.agents = agents
        if allow_agent_join_enabled is not None:
            body.allow_agent_join_enabled = allow_agent_join_enabled
        url = self.ep(f'{queue_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_queue_announcement_files(self, location_id: str, queue_id: str, org_id: str = None) -> List[GetAnnouncementFileInfo]:
        """
        List file info for all Call Queue announcement files associated with this Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call queue can be configured to play whatever subset of these announcement files is desired.
        Retrieving this list of files requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        Note that uploading of announcement files via API is not currently supported, but is available via Webex Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve announcement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{queue_id}/announcements')
        data = super().get(url=url, params=params)
        return data["announcements"]

    def delete_queue_announcement_file(self, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """
        Delete an announcement file for the designated Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call queue can be configured to play whatever subset of these announcement files is desired.
        Deleting an announcement file for a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Delete an announcement for a call queue in this location.
        :type location_id: str
        :param queue_id: Delete an announcement for the call queue with this identifier.
        :type queue_id: str
        :param file_name: 
        :type file_name: str
        :param org_id: Delete call queue announcement from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{queue_id}/announcements/{file_name}')
        super().delete(url=url, params=params)
        return

class MemberType(ApiModel):
    #: Indicates the associated member is a person.
    people: Optional[str]
    #: Indicates the associated member is a workspace.
    place: Optional[str]


class LineType(ApiModel):
    #: Indicates a Primary line for the member.
    primary: Optional[str]
    #: Indicates a Shared line for the member. Shared line appearance allows users to receive and place calls to and from another user's extension, using their device.
    shared_call_appearance: Optional[str]


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    port: Optional[int]
    #: Unique identifier for the member.
    id: Optional[str]
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of device.
    primary_owner: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool]


class MemberObject(PutMemberObject):
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will be supported in a future update.
    phone_number: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Registration Host IP address for the line port.
    host_ip: Optional[str]
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str]
    #: Indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str]
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace.
    phone_number: Optional[str]
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only declines the current endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Indicates if member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]


class SelectionType(ApiModel):
    #: Indicates the regional selection type for audio codec priority.
    regional: Optional[str]
    #: Indicates the custom selection type for audio codec priority.
    custom: Optional[str]


class AudioCodecPriorityObject(ApiModel):
    #: Indicates the selection of an Audio Codec Priority Object.
    selection: Optional[SelectionType]
    #: Indicates the primary Audio Codec.
    primary: Optional[str]
    #: Indicates the secondary Audio Codec.
    secondary: Optional[str]
    #: Indicates the tertiary Audio Codec.
    tertiary: Optional[str]


class AtaDtmfModeObject(ApiModel):
    #: A DTMF digit requires an extra hold time after detection and the DTMF level threshold is raised to -20 dBm.
    strict: Optional[str]
    #: Normal threshold mode.
    normal: Optional[str]


class AtaDtmfMethodObject(ApiModel):
    #: Sends DTMF by using the audio path.
    inband: Optional[str]
    #: Audio video transport. Sends DTMF as AVT events.
    avt: Optional[str]
    #: Uses InBand or AVT based on the outcome of codec negotiation.
    auto: Optional[str]


class VlanObject(ApiModel):
    #: Denotes whether the VLAN object of an ATA is enabled.
    enabled: Optional[bool]
    #: The value of the VLAN Object of DECT.
    value: Optional[int]


class AtaObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject]
    #: DTMF Detection Tx Mode selection for Cisco ATA devices.
    ata_dtmf_mode: Optional[AtaDtmfModeObject]
    #: Method for transmitting DTMF signals to the far end.
    ata_dtmf_method: Optional[AtaDtmfMethodObject]
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: Optional[bool]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[VlanObject]


class MppAudioCodecPriorityObject(ApiModel):
    #: Indicates the selection of the Audio Codec Priority Object for an MPP object.
    selection: Optional[str]
    #: Indicates the primary Audio Codec for an MPP object.
    primary: Optional[str]
    #: Indicates the secondary Audio Codec for an MPP object.
    secondary: Optional[str]
    #: Indicates the tertiary Audio Codec for an MPP object.
    tertiary: Optional[str]


class BacklightTimerObject(ApiModel):
    one_m: Optional[str]
    five_m: Optional[str]
    thirty_m: Optional[str]
    always_on: Optional[str]
    off: Optional[str]
    ten_s: Optional[str]
    twenty_s: Optional[str]
    thirty_s: Optional[str]


class BackgroundImage(ApiModel):
    #: Indicates that there will be no background image set for the devices.
    none: Optional[str]
    #: Indicates that dark blue background image will be set for the devices.
    dark_blue: Optional[str]
    #: Indicates that Cisco themed dark blue background image will be set for the devices.
    cisco_dark_blue: Optional[str]
    #: Indicates that Cisco Webex dark blue background image will be set for the devices.
    webex_dark_blue: Optional[str]
    #: Indicates that a custom background image will be set for the devices.
    custom_background: Optional[str]
    #: When this option is selected, a field 'Custom Background URL' needs to be added with the image url. URLs provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url: Optional[str]


class DisplayNameSelection(ApiModel):
    #: Indicates that devices will display the person's phone number, or if a person doesn't have a phone number, the location number will be displayed.
    person_number: Optional[str]
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name: Optional[str]
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name: Optional[str]


class DefaultLoggingLevelObject(ApiModel):
    #: Enables standard logging.
    standard: Optional[str]
    #: Enables detailed debugging logging.
    debugging: Optional[str]


class DisplayCallqueueAgentSoftkeysObject(ApiModel):
    front_page: Optional[str]
    last_page: Optional[str]


class AcdObject(ApiModel):
    #: Indicates whether the ACD object is enabled.
    enabled: Optional[bool]
    #: Indicates the call queue agent soft key value of an ACD object.
    display_callqueue_agent_softkeys: Optional[str]


class LineKeyLabelSelection(ApiModel):
    #: This will display the person extension, or if a person doesn't have an extension, the person's first name will be displayed.
    person_extension: Optional[str]
    #: Indicates that devices will display the name in first name then last name format.
    person_first_then_last_name: Optional[str]
    #: Indicates that devices will display the name in last name then first name format.
    person_last_then_first_name: Optional[str]


class LineKeyLEDPattern(ApiModel):
    default: Optional[str]
    preset_1: Optional[str]


class PhoneLanguage(ApiModel):
    #: Indicates a person's announcement language.
    person_language: Optional[str]
    arabic: Optional[str]
    bulgarian: Optional[str]
    catalan: Optional[str]
    chinese_simplified: Optional[str]
    chinese_traditional: Optional[str]
    croatian: Optional[str]
    czech: Optional[str]
    danish: Optional[str]
    dutch: Optional[str]
    english_united_states: Optional[str]
    english_united_kingdom: Optional[str]
    finnish: Optional[str]
    french_canada: Optional[str]
    french_france: Optional[str]
    german: Optional[str]
    greek: Optional[str]
    hebrew: Optional[str]
    hungarian: Optional[str]
    italian: Optional[str]
    japanese: Optional[str]
    korean: Optional[str]
    norwegian: Optional[str]
    polish: Optional[str]
    portuguese_portugal: Optional[str]
    russian: Optional[str]
    spanish_colombia: Optional[str]
    spanish_spain: Optional[str]
    slovak: Optional[str]
    swedish: Optional[str]
    slovenian: Optional[str]
    turkish: Optional[str]
    ukraine: Optional[str]


class MppVlanObject(VlanObject):
    #: Indicates the PC port value of a VLAN object for an MPP object.
    pc_port: Optional[int]


class WifiNetworkObject(ApiModel):
    #: Indicates whether the wifi network is enabled.
    enabled: Optional[bool]
    #: Authentication method of wifi network.
    authentication_method: Optional[str]
    #: SSID name of the wifi network.
    ssid_name: Optional[str]
    #: User Id of the wifi network.
    user_id: Optional[str]


class MppObject(ApiModel):
    #: Indicates whether the PNAC of MPP object is enabled or not.
    pnac_enabled: Optional[bool]
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[MppAudioCodecPriorityObject]
    #: Choose the length of time (in minutes) for the phone's backlight to remain on.
    backlight_timer: Optional[BacklightTimerObject]
    #: Holds the background object of MPP Object.
    background: Optional[BackgroundImage]
    #: The display name that appears on the phone screen.
    display_name_format: Optional[DisplayNameSelection]
    #: Allows you to enable/disable CDP for local devices.
    cdp_enabled: Optional[bool]
    #: Choose the desired logging level for an MPP devices.
    default_logging_level: Optional[DefaultLoggingLevelObject]
    #: Enable/disable Do-Not-Disturb capabilities for Multi-Platform Phones.
    dnd_services_enabled: Optional[bool]
    #: Chooses the location of the Call Queue Agent Login/Logout softkey on Multi-Platform Phones.
    display_callqueue_agent_softkeys: Optional[DisplayCallqueueAgentSoftkeysObject]
    #: Choose the duration (in hours) of Hoteling guest login.
    hoteling_guest_association_timer: Optional[int]
    #: Holds the Acd object value.
    acd: Optional[AcdObject]
    #: Indicates the short inter digit timer value.
    short_interdigit_timer: Optional[int]
    #: Indicates the long inter digit timer value..
    long_interdigit_timer: Optional[int]
    #: Line key labels define the format of what's shown next to line keys.
    line_key_label_format: Optional[LineKeyLabelSelection]
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not supported on the MPP 8875
    line_key_led_pattern: Optional[LineKeyLEDPattern]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: Optional[bool]
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]]
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: Optional[int]
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your provisioned location.
    phone_language: Optional[PhoneLanguage]
    #: Enable/disable the Power-Over-Ethernet mode for Multi-Platform Phones.
    poe_mode: Optional[str]
    #: Allows you to enable/disable tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify the amount of inactive time needed (in seconds) before the phone's screen saver activates.
    screen_timeout: Optional[VlanObject]
    #: Enable/disable the use of the USB ports on Multi-Platform phones.
    usb_ports_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[MppVlanObject]
    #: Specify the Wi-Fi SSID and password for wireless-enabled MPP phones.
    wifi_network: Optional[WifiNetworkObject]


class CustomizationDeviceLevelObject(ApiModel):
    #: Applicable device settings for an ATA device.
    ata: Optional[AtaObject]
    #: Applicable device settings for an MPP device.
    mpp: Optional[MppObject]


class UpdateDeviceSettingsBody(ApiModel):
    #: Indicates the customization object of the device settings.
    customizations: Optional[CustomizationDeviceLevelObject]
    #: Indicates if customization is allowed at a device level. If true, customized at a device level. If false, not customized; uses customer-level configuration.
    custom_enabled: Optional[bool]


class GetDeviceSettingsResponse(UpdateDeviceSettingsBody):
    #: Customer devices setting update status. If true, an update is in progress (no further changes are allowed). If false, no update in progress (changes are allowed).
    update_in_progress: Optional[bool]
    #: Number of devices that will be updated.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str]
    #: Enumeration that indicates if the member is of type PEOPLE or PLACE.
    type: Optional[MemberType]
    #: First name of device owner.
    first_name: Optional[str]
    #: Last name of device owner.
    last_name: Optional[str]


class ActivationStates(ApiModel):
    #: Indicates a device is activating.
    activating: Optional[str]
    #: Indicates a device is activated.
    activated: Optional[str]
    #: Indicates a device is deactivated.
    deactivated: Optional[str]


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str]
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]]
    #: Identifier for device model.
    model: Optional[str]
    #: MAC address of device.
    mac: Optional[str]
    #: IP address of device.
    ip_address: Optional[str]
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of the device.
    primary_owner: Optional[bool]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType]
    #: Owner of device.
    owner: Optional[DeviceOwner]
    #: Activation state of device.
    activation_state: Optional[ActivationStates]


class Hoteling(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this host(workspace device) and use this device
    #: as if it were their own. This is useful when traveling to a remote office but still needing to place/receive calls with their telephone number and access features normally available to them on their office phone.
    enabled: Optional[bool]
    #: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
    limit_guest_use: Optional[bool]
    #: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
    guest_hours_limit: Optional[int]


class PlaceDevices(Devices):
    #: Indicates Hoteling details of a device.
    hoteling: Optional[Hoteling]


class TypeObject(ApiModel):
    #: Cisco Multiplatform Phone
    mpp: Optional[str]
    #: Analog Telephone Adapters
    ata: Optional[str]
    #: GENERIC Session Initiation Protocol
    generic_sip: Optional[str]
    #: Esim Supported Webex Go
    esim: Optional[str]


class ManufacturerObject(ApiModel):
    #: Devices manufactured by Cisco.
    cisco: Optional[str]
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for provisioning in the control hub.
    third_party: Optional[str]


class ManagedByObject(ApiModel):
    #: Devices managed by Cisco.
    cisco: Optional[str]
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the control hub.
    customer: Optional[str]


class OnboardingMethodObject(ApiModel):
    mac_address: Optional[str]
    activation_code: Optional[str]
    none: Optional[str]


class KemModuleTypeObject(ApiModel):
    kem_14_keys: Optional[str]
    kem_18_keys: Optional[str]


class DeviceObject(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Display name of the device.
    display_name: Optional[str]
    #: Type of the device.
    type: Optional[TypeObject]
    #: Manufacturer of the device.
    manufacturer: Optional[ManufacturerObject]
    #: Users who manage the device.
    managed_by: Optional[ManagedByObject]
    #: List of places the device is supported for.
    supported_for: Optional[list[MemberType]]
    #: Onboarding method.
    onboarding_method: Optional[list[OnboardingMethodObject]]
    #: Enables / Disables layout configuration for devices.
    allow_configure_layout_enabled: Optional[bool]
    #: Number of port lines.
    number_of_line_ports: Optional[int]
    #: Indicates whether Kem support is enabled or not.
    kem_support_enabled: Optional[bool]
    #: Module count.
    kem_module_count: Optional[int]
    #: Key expansion module type of the device.
    kem_module_type: Optional[list[KemModuleTypeObject]]
    #: Enables / Disables the upgrade channel.
    upgrade_channel_enabled: Optional[bool]
    #: The default upgrade channel.
    default_upgrade_channel: Optional[str]
    #: Enables / disables the additional primary line appearances.
    additional_primary_line_appearances_enabled: Optional[bool]
    #: Enables / disables Basic emergency nomadic.
    basic_emergency_nomadic_enabled: Optional[bool]
    #: Enables / disables customized behavior support on devices.
    customized_behaviors_enabled: Optional[bool]
    #: Enables / disables configuring port support on device.
    allow_configure_ports_enabled: Optional[bool]


class DectObject(ApiModel):
    #: Choose up to three predefined codec priority options available for your region.
    audio_codec_priority: Optional[AudioCodecPriorityObject]
    #: Enable/disable Cisco Discovery Protocol for local devices.
    cdp_enabled: Optional[bool]
    #: Specify the destination number to be dialled from the DECT Handset top button when pressed.
    dect6825_handset_emergency_number: Optional[str]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Specify up to 3 multicast group URLs each with a unique listening port.
    multicast: Optional[str]
    #: Enable/disable quality of service tagging of packets from the local device to the Webex Calling platform.
    qos_enabled: Optional[bool]
    #: Specify a numeric Virtual LAN ID for devices.
    vlan: Optional[VlanObject]


class CustomizationObject(CustomizationDeviceLevelObject):
    #: Settings that are applicable to DECT devices.
    dect: Optional[DectObject]


class DectDeviceList(ApiModel):
    #: Model name of the device.
    model: Optional[str]
    #: Display name of the device.
    display_name: Optional[str]
    #: Indicates number of base stations.
    number_of_base_stations: Optional[int]
    #: Indicates number of port lines,
    number_of_line_ports: Optional[int]
    #: Indicates number of supported registrations.
    number_of_registrations_supported: Optional[int]


class Status6(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class State(str, Enum):
    #: The requested MAC address is available.
    available = 'AVAILABLE'
    #: The requested MAC address is unavailable.
    unavailable = 'UNAVAILABLE'
    #: The requested MAC address is duplicated.
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    #: The requested MAC address is invalid.
    invalid = 'INVALID'


class MacStatusObject(ApiModel):
    #: MAC address.
    mac: Optional[str]
    #: State of the MAC address.
    state: Optional[State]
    #: MAC address validation error code.
    error_code: Optional[int]
    #: Provides a status message about the MAC address.
    message: Optional[str]


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    id: Optional[int]
    #: Step execution start time.
    start_time: Optional[str]
    #: Step execution end time.
    end_time: Optional[str]
    #: Last updated time for a step.
    last_updated: Optional[str]
    #: Displays status for a step.
    status_message: Optional[str]
    #: ExitCode for a step.
    exit_code: Optional[str]
    #: Step name.
    name: Optional[str]
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str]


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int]
    #: Last updated time post one of the step execution completion.
    last_updated: Optional[str]
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str]
    #: Exit code for a job.
    exit_code: Optional[str]
    #: Job creation time.
    created_time: Optional[str]
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str]
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]]


class ListJobResponse(ApiModel):
    #: Unique identifier of the job.
    id: Optional[str]
    #: Job type.
    job_type: Optional[str]
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str]
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str]
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str]
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str]
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int]
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involve in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, or FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: If present, indicates that the job was executed at location level. Else it means that the job was triggered at organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates if the job was run at organization level or location level.
    target: Optional[str]
    #: If job was run at location level, this field will indicate unique location identifier for which the job was run. Else it will be empty.
    location_id: Optional[str]
    #: If job was run at location level, this field will indicate the location name.
    location_name: Optional[str]
    #: Displays job completion percentage.
    percentage_complete: Optional[str]
    #: Indicates the number of devices affected by the job.
    device_count: Optional[int]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse(ApiModel):
    #: Job name.
    name: Optional[str]
    #: Unique identifier of the job.
    id: Optional[str]
    #: Job type.
    job_type: Optional[str]
    #: Unique identifier to track the flow of HTTP requests.
    tracking_id: Optional[str]
    #: Unique identifier to identify which user has run the job.
    source_user_id: Optional[str]
    #: Unique identifier to identify the customer who has run the job.
    source_customer_id: Optional[str]
    #: Unique identifier to identify the customer for which the job was run.
    target_customer_id: Optional[str]
    #: Unique identifier to identify the instance of the job.
    instance_id: Optional[int]
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involve in the execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, or FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: Indicates if all the devices within this location will be customized with new requested customizations(if set to true) or will be overridden with the one at organization level (if set to false or any other value). This field has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates if the job was run at organization level or location level.
    target: Optional[str]
    #: Unique location identifier for which the job was run.
    location_id: Optional[str]
    #: Displays job completion percentage.
    percentage_complete: Optional[str]


class AuthorizationCode(ApiModel):
    #: Indicates an access code.
    code: Optional[str]
    #: Indicates the description of the access code.
    description: Optional[str]


class ErrorMessageObject(AuthorizationCode):
    #: Message describing the location or point of failure.
    location: Optional[str]


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str]
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]]


class ItemObject(ApiModel):
    #: Index of error number.
    item_number: Optional[int]
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str]
    error: Optional[ErrorObject]


class GetDeviceMembersResponse(ApiModel):
    #: Model type of the device.
    model: Optional[str]
    #: List of members that appear on the device.
    members: Optional[list[MemberObject]]
    #: Maximum number of lines available for the device.
    max_line_count: Optional[int]


class UpdateMembersOndeviceBody(ApiModel):
    #: If the member's list is missing then all the users are removed except the primary user.
    members: Optional[list[PutMemberObject]]


class SearchMembersResponse(ApiModel):
    #: List of members available for the device.
    members: Optional[list[SearchMemberObject]]


class GetUserDevicesResponse(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int]


class GetWorkspaceDevicesResponse(ApiModel):
    #: Array of devices associated to a workspace.
    devices: Optional[list[PlaceDevices]]
    #: Maximum number of devices a workspace can be assigned to.
    max_device_count: Optional[int]


class ReadListOfSupportedDevicesResponse(ApiModel):
    #: List of supported devices.
    devices: Optional[list[DeviceObject]]


class ReaddeviceOverrideSettingsFororganizationResponse(ApiModel):
    #: Customization object of the device settings.
    customizations: Optional[CustomizationObject]
    #: Progress of the device update.
    update_in_progress: Optional[bool]
    #: Device count.
    device_count: Optional[int]
    #: Last updated time.
    last_update_time: Optional[int]


class ReadDECTDeviceTypeListResponse(ApiModel):
    #: Contains a list of devices.
    devices: Optional[list[DectDeviceList]]


class ValidatelistOfMACAddressBody(ApiModel):
    #: MAC addresses to be validated.
    #: Possible values: {["ab125678cdef", "00005E0053B4"]}
    macs: Optional[list[str]]


class ValidatelistOfMACAddressResponse(ApiModel):
    #: Status of MAC address.
    status: Optional[Status6]
    #: Contains an array of all the MAC address provided and their statuses.
    mac_status: Optional[list[MacStatusObject]]


class ChangeDeviceSettingsAcrossOrganizationOrLocationJobBody(ApiModel):
    #: Location within an organization where changes of device setings will be applied to all the devices within it.
    location_id: Optional[str]
    #: Indicates if all the devices within this location will be customized with new requested customizations(if set to true) or will be overridden with the one at organization level (if set to false or any other value). This field has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates the settings for ATA devices, DECT devices and MPP devices.
    customizations: Optional[CustomizationObject]


class ListChangeDeviceSettingsJobsResponse(ApiModel):
    #: Lists all jobs for the job type 'calldevicesettings' for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[ListJobResponse]]


class GetChangeDeviceSettingsJobStatusResponse(ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse):
    #: Count of the number of devices that were modified by the job.
    device_count: Optional[int]


class ListChangeDeviceSettingsJobErrorsResponse(ApiModel):
    items: Optional[list[ItemObject]]


class WebexCallingOrganizationSettingswithDevicesFeaturesApi(ApiChild, base='telephony/config/'):
    """

    """

    def members(self, device_id: str, org_id: str = None) -> GetDeviceMembersResponse:
        """
        Get the list of all the members of the device including primary and secondary users.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify member details and 
        search for available members on a device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/members')
        data = super().get(url=url, params=params)
        return GetDeviceMembersResponse.parse_obj(data)

    def update_members_ondevice(self, device_id: str, org_id: str = None, members: PutMemberObject = None):
        """
        Modify member details on the device.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify member details and
        search for available members on a device.
        Modifying members on the device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        :param members: If the member's list is missing then all the users are removed except the primary user.
        :type members: PutMemberObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateMembersOndeviceBody()
        if members is not None:
            body.members = members
        url = self.ep(f'devices/{device_id}/members')
        super().put(url=url, params=params, data=body.json())
        return

    def search_members(self, device_id: str, location_id: str, org_id: str = None, start: int = None, max: int = None, member_name: str = None, phone_number: str = None, extension: str = None) -> List[SearchMemberObject]:
        """
        Search members that can be assigned to the device.
        A device member can be either a person or a workspace. A admin can access the list of member details, modify member details and
        search for available members on a device.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Retrieves the list of available members on the device in this organization.
        :type org_id: str
        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param max: Specifies the maximum number of records that you want to fetch.
        :type max: int
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        """
        params = {}
        if location_id is not None:
            params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if start is not None:
            params['start'] = start
        if max is not None:
            params['max'] = max
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'devices/{device_id}/availableMembers')
        data = super().get(url=url, params=params)
        return data["members"]

    def apply_changes_forspecific(self, device_id: str, org_id: str = None):
        """
        Issues request to the device to download and apply changes to the configuration.
        Applying changes for a specific device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/actions/applyChanges/invoke')
        super().post(url=url, params=params)
        return

    def settings(self, device_id: str, device_model: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get override settings for a device.
        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin can also modify the settings. DECT devices do not support settings at the device level.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str
        """
        params = {}
        if device_model is not None:
            params['deviceModel'] = device_model
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'devices/{device_id}/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def update_settings(self, device_id: str, customizations: CustomizationDeviceLevelObject, custom_enabled: bool, org_id: str = None, device_model: str = None):
        """
        Modify override settings for a device.
        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins can also modify the settings. NOTE: DECT devices do not support settings at the device level.
        Updating settings on the device requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObject
        :param custom_enabled: Indicates if customization is allowed at a device level. If true, customized at a device level. If false, not customized; uses customer-level configuration.
        :type custom_enabled: bool
        :param org_id: Organization in which the device resides..
        :type org_id: str
        :param device_model: Device model name.
        :type device_model: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        body = UpdateDeviceSettingsBody()
        if customizations is not None:
            body.customizations = customizations
        if custom_enabled is not None:
            body.custom_enabled = custom_enabled
        url = self.ep(f'devices/{device_id}/settings')
        super().put(url=url, params=params, data=body.json())
        return

    def location_settings(self, location_id: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get device override settings for a location.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Organization in which the device resides.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/devices/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def user(self, person_id: str, org_id: str = None) -> GetUserDevicesResponse:
        """
        Get all devices for a person.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/devices')
        data = super().get(url=url, params=params)
        return GetUserDevicesResponse.parse_obj(data)

    def workspace(self, workspace_id: str, org_id: str = None) -> GetWorkspaceDevicesResponse:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/devices')
        data = super().get(url=url, params=params)
        return GetWorkspaceDevicesResponse.parse_obj(data)

    def modify_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None, limit_guest_use: bool = None, guest_hours_limit: int = None):
        """
        Modify devices for a workspace.
        Modifying devices for a workspace requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :param enabled: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this host(workspace device) and use this device
as if it were their own. This is useful when traveling to a remote office but still needing to place/receive calls with their telephone number and access features normally available to them on their office phone.
        :type enabled: bool
        :param limit_guest_use: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
        :type limit_guest_use: bool
        :param guest_hours_limit: Time Limit in hours until hoteling is enabled. Mandatory if limitGuestUse is enabled.
        :type guest_hours_limit: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = Hoteling()
        if enabled is not None:
            body.enabled = enabled
        if limit_guest_use is not None:
            body.limit_guest_use = limit_guest_use
        if guest_hours_limit is not None:
            body.guest_hours_limit = guest_hours_limit
        url = self.ep(f'workspaces/{workspace_id}/devices')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_supported(self, org_id: str = None) -> List[DeviceObject]:
        """
        Gets the list of supported devices for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('supportedDevices')
        data = super().get(url=url, params=params)
        return data["devices"]

    def readdevice_override_settings_fororganization(self, org_id: str = None) -> ReaddeviceOverrideSettingsFororganizationResponse:
        """
        Get device override settings for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/settings')
        data = super().get(url=url, params=params)
        return ReaddeviceOverrideSettingsFororganizationResponse.parse_obj(data)

    def read_dect_type_list(self, org_id: str = None) -> List[DectDeviceList]:
        """
        Get DECT device type list with base stations and line ports supported count. This is a static list.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: 
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/dects/supportedDevices')
        data = super().get(url=url, params=params)
        return data["devices"]

    def validatelist_of_mac_address(self, macs: List[str], org_id: str = None) -> ValidatelistOfMACAddressResponse:
        """
        Validate a list of MAC addresses.
        Validating this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param macs: MAC addresses to be validated.
Possible values: {["ab125678cdef", "00005E0053B4"]}
        :type macs: List[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidatelistOfMACAddressBody()
        if macs is not None:
            body.macs = macs
        url = self.ep('devices/actions/validateMacs/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return ValidatelistOfMACAddressResponse.parse_obj(data)

    def change_settings_across_organization_or_location_job(self, org_id: str = None, location_id: str = None, location_customizations_enabled: bool = None, customizations: CustomizationObject = None) -> ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse:
        """
        Change device settings across organization or locations jobs.
        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system admins in a stateful persistent manner. This job will modify the requested device settings across all the devices. Whenever a location ID is specified in the request, it will modify the requested device settings only for the devices that are part of the provided location within an organization.
        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.
        Only one job per customer can be running at any given time within the same organization. An attempt to run multiple jobs at the same time will result in a 409 error response.
        Running a job requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :param location_id: Location within an organization where changes of device setings will be applied to all the devices within it.
        :type location_id: str
        :param location_customizations_enabled: Indicates if all the devices within this location will be customized with new requested customizations(if set to true) or will be overridden with the one at organization level (if set to false or any other value). This field has no effect when the job is being triggered at organization level.
        :type location_customizations_enabled: bool
        :param customizations: Indicates the settings for ATA devices, DECT devices and MPP devices.
        :type customizations: CustomizationObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ChangeDeviceSettingsAcrossOrganizationOrLocationJobBody()
        if location_id is not None:
            body.location_id = location_id
        if location_customizations_enabled is not None:
            body.location_customizations_enabled = location_customizations_enabled
        if customizations is not None:
            body.customizations = customizations
        url = self.ep('jobs/devices/callDeviceSettings')
        data = super().post(url=url, params=params, data=body.json())
        return ChangeDeviceSettingsAcrossOrganizationOrLocationJobResponse.parse_obj(data)

    def list_change_settings_jobs(self, org_id: str = None, **params) -> Generator[ListJobResponse, None, None]:
        """
        List change device settings jobs.
        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to oldest one irrespective of its status.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/callDeviceSettings')
        return self.session.follow_pagination(url=url, model=ListJobResponse, params=params)

    def change_settings_job_status(self, job_id: str) -> int:
        """
        Get change device settings job status.
        Provides details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        """
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}')
        data = super().get(url=url)
        return data["deviceCount"]

    def list_change_settings_job_errors(self, job_id: str, org_id: str = None, **params) -> Generator[ItemObject, None, None]:
        """
        List change device settings job errors.
        Lists all error details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, params=params)

class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    id: Optional[str]
    #: First name of member.
    first_name: Optional[str]
    #: Last name of member.
    last_name: Optional[str]
    #: Phone Number of member. Currently E.164 format is not supported.
    phone_number: Optional[str]
    #: Phone extension of member.
    extension: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    id: Optional[str]
    #: Device port number assigned to person or workspace.
    port: Optional[int]
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: This field indicates whether the person or the workspace is the owner of the device, this points to primary Line/Port of the device.
    primary_owner: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how person device behaves when a call is declined. When set to true, a call decline request is extended to all the endpoints on the device. When set to false, a call decline request only decline the current endpoint.
    allow_call_decline_enabled: Optional[bool]


class GetSharedLineMemberItem(PutSharedLineMemberItem):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Phone Number of person or workspace. Currently E.164 format is not supported.
    phone_number: Optional[str]
    #: Phone extension of person or workspace.
    extension: Optional[str]
    #: Registration home IP for the line port.
    host_ip: Optional[str]
    #: Registration remote IP for the line port.
    remote_ip: Optional[str]
    #: Enumeration that indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]


class SearchSharedLineAppearanceMembersBody(ApiModel):
    #: Number of records per page.
    max: Optional[int]
    #: Page number.
    start: Optional[int]
    #: Location ID for the user.
    location: Optional[str]
    #: Search users with names that match the query. 
    name: Optional[str]
    #: Search users with numbers that match the query.
    number: Optional[str]
    #: Sort by first name (fname) or last name (lname).
    order: Optional[str]
    #: Search users with extensions that match the query.
    extension: Optional[str]


class SearchSharedLineAppearanceMembersResponse(ApiModel):
    members: Optional[list[AvailableSharedLineMemberItem]]


class GetSharedLineAppearanceMembersResponse(ApiModel):
    #: Model name of device.
    model: Optional[str]
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]]
    #: Maximum number of device ports.
    max_line_count: Optional[int]


class PutSharedLineAppearanceMembersBody(ApiModel):
    members: Optional[list[PutSharedLineMemberItem]]


class WebexCallingPersonSettingsWithSharedLineApi(ApiChild, base='telephony/config/people/{personId}/applications/{applicationId}/'):
    """

    """

    def search_line_appearance_members(self, person_id: str, application_id: str, max: int = None, start: int = None, location: str = None, name: str = None, number: str = None, order: str = None, extension: str = None) -> List[AvailableSharedLineMemberItem]:
        """
        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param max: Number of records per page.
        :type max: int
        :param start: Page number.
        :type start: int
        :param location: Location ID for the user.
        :type location: str
        :param name: Search users with names that match the query. 
        :type name: str
        :param number: Search users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (fname) or last name (lname).
        :type order: str
        :param extension: Search users with extensions that match the query.
        :type extension: str
        """
        body = SearchSharedLineAppearanceMembersBody()
        if max is not None:
            body.max = max
        if start is not None:
            body.start = start
        if location is not None:
            body.location = location
        if name is not None:
            body.name = name
        if number is not None:
            body.number = number
        if order is not None:
            body.order = order
        if extension is not None:
            body.extension = extension
        url = self.ep(f'availableMembers')
        data = super().get(url=url, data=body.json())
        return data["members"]

    def line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineAppearanceMembersResponse:
        """
        Get primary and secondary members assigned to shared-line on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        """
        url = self.ep(f'members')
        data = super().get(url=url)
        return GetSharedLineAppearanceMembersResponse.parse_obj(data)

    def put_line_appearance_members(self, person_id: str, application_id: str, members: PutSharedLineMemberItem = None):
        """
        Add or Modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param members: 
        :type members: PutSharedLineMemberItem
        """
        body = PutSharedLineAppearanceMembersBody()
        if members is not None:
            body.members = members
        url = self.ep(f'members')
        super().put(url=url, data=body.json())
        return

class InterceptNumberGet(ApiModel):
    #: If true, the caller hears this new number when the call is intercepted.
    enabled: Optional[bool]
    #: New number the caller hears announced.
    destination: Optional[str]


class CallForwardingBusyGet(InterceptNumberGet):
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class CallForwardingNoAnswerGet(CallForwardingBusyGet):
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class CallForwardingPlaceSettingGet(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the workspace is busy.
    busy: Optional[CallForwardingBusyGet]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingNoAnswerGet]


class CallForwardingPlaceSettingPatch(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the workspace is busy.
    busy: Optional[CallForwardingBusyGet]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingNoAnswerGet]


class CLIDPolicySelection(ApiModel):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line: Optional[str]
    #: Outgoing caller ID will show the main number for the location.
    location_number: Optional[str]
    #: Outgoing caller ID will show the value from the customNumber field.
    custom: Optional[str]


class ExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID will show the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the Site Name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID will show the value from the customExternalCallerIdName field.
    other = 'OTHER'


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    id: Optional[str]
    #: Name of call park extension.
    name: Optional[str]
    #: Extension of call park extension.
    extension: Optional[str]
    #: Name of location for call park extension.
    location: Optional[str]
    #: ID of location for call park extension.
    location_id: Optional[str]


class UserNumberItem(ApiModel):
    #: Phone number of person or workspace. Either phoneNumber or extension is mandatory.
    external: Optional[str]
    #: Extension of person or workspace. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Flag to indicate primary phone.
    primary: Optional[bool]
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool]


class MonitoredElementUser(ApiModel):
    #: ID of person or workspace.
    id: Optional[str]
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Display name of person or workspace.
    display_name: Optional[str]
    #: Type of the person or workspace.
    type: Optional[MemberType]
    #: Email of the person or workspace.
    email: Optional[str]
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumberItem]]
    #: Name of location for call park.
    location: Optional[str]
    #: ID of the location for call park.
    location_id: Optional[str]


class MonitoredElementItem(ApiModel):
    #: Monitored Call Park extension.
    callparkextension: Optional[MonitoredElementCallParkExtension]
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser]


class ExternalTransfer(str, Enum):
    #: All external calls are allowed.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only externally transferred external calls are allowed.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: All external calls are blocked.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class RetrieveIncomingPermissionSettingsForWorkspaceResponse(ApiModel):
    #: Incoming Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool]
    #: Indicate call transfer setting.
    external_transfer: Optional[ExternalTransfer]
    #: Flag to indicate if workspace can receive internal calls.
    internal_calls_enabled: Optional[bool]
    #: Flag to indicate if workspace can receive collect calls.
    collect_calls_enabled: Optional[bool]


class CallType1(str, Enum):
    #: Indicates the internal call type.
    internal_call = 'INTERNAL_CALL'
    #: Indicates the local call type.
    local = 'LOCAL'
    #: Indicates the toll free call type.
    toll_free = 'TOLL_FREE'
    #: Indicates the toll call type.
    toll = 'TOLL'
    #: Indicates the international call type.
    international = 'INTERNATIONAL'
    #: Indicates the operator assisted call type.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Indicates the chargeable directory assisted call type.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Indicates the special services I call type.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Indicates the special services II call type.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Indicates the premium services I call type.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Indicates the premium services II call type.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Indicates the national call type.
    national = 'NATIONAL'


class Action3(str, Enum):
    #: The call type is allowed.
    allow = 'ALLOW'
    #: The call type is blocked.
    block = 'BLOCK'
    #: Indicates access code action for the specified call type.
    auth_code = 'AUTH_CODE'
    #: Indicates transfer number 1 for the specified call type.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Indicates transfer number 2 for the specified call type.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Indicates transfer number 3 for the specified call type.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermission(ApiModel):
    #: Type of the outgoing call.
    call_type: Optional[CallType1]
    #: Indicates permission for call types.
    action: Optional[Action3]
    #: Indicate calling permission for call type enable status.
    transfer_enabled: Optional[bool]


class Type6(str, Enum):
    #: All incoming calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class InterceptAnnouncementsGet(ApiModel):
    #: Indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[Greeting]
    #: Filename of the custom greeting. Is an empty string if no custom greeting has been uploaded.
    filename: Optional[str]
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet]
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet]


class InterceptIncomingGet(ApiModel):
    #: Indicated incoming calls are intercepted.
    type: Optional[Type6]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsGet]


class Type7(str, Enum):
    #: Outgoing calls are are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class InterceptOutGoingGet(ApiModel):
    #: Indicated all outgoing calls are intercepted.
    type: Optional[Type7]
    #: If true, when the person attempts to make an outbound call, a system default message is played and the call is made to the destination phone number.
    transfer_enabled: Optional[bool]
    #: Number to which the outbound call be transferred.
    destination: Optional[str]


class InterceptAnnouncementsPatch(ApiModel):
    #: Indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[Greeting]
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet]
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet]


class InterceptIncomingPatch(ApiModel):
    #: Indicated incoming calls are intercepted.
    type: Optional[Type6]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsPatch]


class RetrieveTransferNumbersSettingsForWorkspaceResponse(ApiModel):
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number1: Optional[str]
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number2: Optional[str]
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number3: Optional[str]


class RetrieveCallForwardingSettingsForWorkspaceResponse(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingGet]


class ModifyCallForwardingSettingsForWorkspaceBody(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingPatch]


class RetrieveCallWaitingSettingsForWorkspaceResponse(ApiModel):
    #: Call Waiting state.
    enabled: Optional[bool]


class ModifyCallWaitingSettingsForWorkspaceBody(ApiModel):
    #: Call Waiting state.
    enabled: Optional[bool]


class RetrieveCallerIDSettingsForWorkspaceResponse(ApiModel):
    #: Allowed types for the selected field.
    types: Optional[list[CLIDPolicySelection]]
    #: Which type of outgoing Caller ID will be used.
    selected: Optional[CLIDPolicySelection]
    #: Direct number which will be shown if DIRECT_LINE is selected.
    direct_number: Optional[str]
    #: Location number which will be shown if LOCATION_NUMBER is selected
    location_number: Optional[str]
    #: Flag for specifying a toll-free number.
    toll_free_location_number: Optional[bool]
    #: This value must be an assigned number from the person's location.
    custom_number: Optional[str]
    #: Workspace's caller ID display name.
    display_name: Optional[str]
    #: Workspace's caller ID display details. Default is ..
    display_detail: Optional[str]
    #: Flag to block call forwarding.
    block_in_forward_calls_enabled: Optional[bool]
    #: Designates which type of External Caller ID Name policy is used. Default is DIRECT_LINE.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: Custom External Caller Name, which will be shown if External Caller ID Name is OTHER.
    custom_external_caller_id_name: Optional[str]
    #: External Caller Name, which will be shown if External Caller ID Name is OTHER.
    location_external_caller_id_name: Optional[str]


class ModifyCallerIDSettingsForWorkspaceBody(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    selected: Optional[CLIDPolicySelection]
    #: This value must be an assigned number from the workspace's location.
    custom_number: Optional[str]
    #: Workspace's caller ID display name.
    display_name: Optional[str]
    #: Workspace's caller ID display details.
    display_detail: Optional[str]
    #: Flag to block call forwarding.
    block_in_forward_calls_enabled: Optional[bool]
    #: Designates which type of External Caller ID Name policy is used. Default is DIRECT_LINE.
    #: Possible values: DIRECT_LINE
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: Custom External Caller Name, which will be shown if External Caller ID Name is OTHER.
    custom_external_caller_id_name: Optional[str]
    #: External Caller Name, which will be shown if External Caller ID Name is OTHER.
    location_external_caller_id_name: Optional[str]


class RetrieveMonitoringSettingsForWorkspaceResponse(ApiModel):
    #: Call park notification enabled or disabled.
    call_park_notification_enabled: Optional[bool]
    #: Monitored element items.
    monitored_elements: Optional[MonitoredElementItem]


class ModifyMonitoringSettingsForWorkspaceBody(ApiModel):
    #: Call park notification is enabled or disabled.
    enable_call_park_notification: Optional[bool]
    #: Array of ID strings of monitored elements.
    monitored_elements: Optional[list[str]]


class RetrieveOutgoingPermissionSettingsForWorkspaceResponse(ApiModel):
    #: Outgoing Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool]
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]]


class ModifyOutgoingPermissionSettingsForWorkspaceBody(ApiModel):
    #: Outgoing Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool]
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]]


class RetrieveAccessCodesForWorkspaceResponse(ApiModel):
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]]


class ModifyAccessCodesForWorkspaceBody(ApiModel):
    #: Indicates access codes to delete.
    delete_codes: Optional[list[str]]


class ReadCallInterceptSettingsForWorkspaceResponse(ApiModel):
    #: true if call intercept is enabled.
    enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingGet]
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptOutGoingGet]


class ConfigureCallInterceptSettingsForWorkspaceBody(ApiModel):
    #: true if call interception is enabled.
    enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingPatch]
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptOutGoingGet]


class WebexCallingPersonSettingswithCallingBehaviorApi(ApiChild, base='workspaces/{workspaceId}/features/'):
    """

    """

    def retrieve_callwarding_settings_workspace(self, workspace_id: str, org_id: str = None) -> CallForwardingPlaceSettingGet:
        """
        Retrieve Call Forwarding Settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callForwarding')
        data = super().get(url=url, params=params)
        return data["callForwarding"]

    def modify_callwarding_settings_workspace(self, workspace_id: str, call_forwarding: CallForwardingPlaceSettingPatch, org_id: str = None):
        """
        Modify call forwarding settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param call_forwarding: Call forwarding settings for a Workspace.
        :type call_forwarding: CallForwardingPlaceSettingPatch
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallForwardingSettingsForWorkspaceBody()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_call_waiting_settings_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can place a call on hold to answer or initiate another call.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def modify_call_waiting_settings_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None):
        """
        Modify Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can place a call on hold to answer or initiate another call.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: Call Waiting state.
        :type enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallWaitingSettingsForWorkspaceBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'callWaiting')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_caller_id_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveCallerIDSettingsForWorkspaceResponse:
        """
        Retrieve Caller ID Settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callerId')
        data = super().get(url=url, params=params)
        return RetrieveCallerIDSettingsForWorkspaceResponse.parse_obj(data)

    def modify_caller_id_settings_workspace(self, workspace_id: str, selected: CLIDPolicySelection, org_id: str = None, custom_number: str = None, display_name: str = None, display_detail: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: ExternalCallerIdNamePolicy = None, custom_external_caller_id_name: str = None, location_external_caller_id_name: str = None):
        """
        Modify Caller ID settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CLIDPolicySelection
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param custom_number: This value must be an assigned number from the workspace's location.
        :type custom_number: str
        :param display_name: Workspace's caller ID display name.
        :type display_name: str
        :param display_detail: Workspace's caller ID display details.
        :type display_detail: str
        :param block_in_forward_calls_enabled: Flag to block call forwarding.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default is DIRECT_LINE.
Possible values: DIRECT_LINE
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller ID Name is OTHER.
        :type custom_external_caller_id_name: str
        :param location_external_caller_id_name: External Caller Name, which will be shown if External Caller ID Name is OTHER.
        :type location_external_caller_id_name: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallerIDSettingsForWorkspaceBody()
        if selected is not None:
            body.selected = selected
        if custom_number is not None:
            body.custom_number = custom_number
        if display_name is not None:
            body.display_name = display_name
        if display_detail is not None:
            body.display_detail = display_detail
        if block_in_forward_calls_enabled is not None:
            body.block_in_forward_calls_enabled = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body.external_caller_id_name_policy = external_caller_id_name_policy
        if custom_external_caller_id_name is not None:
            body.custom_external_caller_id_name = custom_external_caller_id_name
        if location_external_caller_id_name is not None:
            body.location_external_caller_id_name = location_external_caller_id_name
        url = self.ep(f'callerId')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_monitoring_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveMonitoringSettingsForWorkspaceResponse:
        """
        Retrieves Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the monitored call park extension.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'monitoring')
        data = super().get(url=url, params=params)
        return RetrieveMonitoringSettingsForWorkspaceResponse.parse_obj(data)

    def modify_monitoring_settings_workspace(self, workspace_id: str, org_id: str = None, enable_call_park_notification: bool = None, monitored_elements: List[str] = None):
        """
        Modify Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the monitored call park extension.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enable_call_park_notification: Call park notification is enabled or disabled.
        :type enable_call_park_notification: bool
        :param monitored_elements: Array of ID strings of monitored elements.
        :type monitored_elements: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyMonitoringSettingsForWorkspaceBody()
        if enable_call_park_notification is not None:
            body.enable_call_park_notification = enable_call_park_notification
        if monitored_elements is not None:
            body.monitored_elements = monitored_elements
        url = self.ep(f'monitoring')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_incoming_permission_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveIncomingPermissionSettingsForWorkspaceResponse:
        """
        Retrieve Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the organization's default to manage different call types.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'incomingPermission')
        data = super().get(url=url, params=params)
        return RetrieveIncomingPermissionSettingsForWorkspaceResponse.parse_obj(data)

    def modify_incoming_permission_settings_workspace(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, external_transfer: ExternalTransfer = None, internal_calls_enabled: bool = None, collect_calls_enabled: bool = None):
        """
        Modify Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the organization's default to manage different call types.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param use_custom_enabled: Incoming Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param external_transfer: Indicate call transfer setting.
        :type external_transfer: ExternalTransfer
        :param internal_calls_enabled: Flag to indicate if workspace can receive internal calls.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Flag to indicate if workspace can receive collect calls.
        :type collect_calls_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = RetrieveIncomingPermissionSettingsForWorkspaceResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if external_transfer is not None:
            body.external_transfer = external_transfer
        if internal_calls_enabled is not None:
            body.internal_calls_enabled = internal_calls_enabled
        if collect_calls_enabled is not None:
            body.collect_calls_enabled = collect_calls_enabled
        url = self.ep(f'incomingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_outgoing_permission_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveOutgoingPermissionSettingsForWorkspaceResponse:
        """
        Retrieve Outgoing Permission settings for a Workspace.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are used by default.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrieveOutgoingPermissionSettingsForWorkspaceResponse.parse_obj(data)

    def modify_outgoing_permission_settings_workspace(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, calling_permissions: CallingPermission = None):
        """
        Modify Outgoing Permission settings for a Place.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are used by default.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param use_custom_enabled: Outgoing Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: CallingPermission
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyOutgoingPermissionSettingsForWorkspaceBody()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_access_codes_workspace(self, workspace_id: str, org_id: str = None) -> List[AuthorizationCode]:
        """
        Retrieve Access codes for a Workspace.
        Access codes are used to bypass permissions.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'outgoingPermission/accessCodes')
        data = super().get(url=url, params=params)
        return data["accessCodes"]

    def modify_access_codes_workspace(self, workspace_id: str, org_id: str = None, delete_codes: List[str] = None):
        """
        Modify Access codes for a workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyAccessCodesForWorkspaceBody()
        if delete_codes is not None:
            body.delete_codes = delete_codes
        url = self.ep(f'outgoingPermission/accessCodes')
        super().put(url=url, params=params, data=body.json())
        return

    def create_access_codes_workspace(self, workspace_id: str, org_id: str = None, code: str = None, description: str = None):
        """
        Create new Access codes for the given workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
        :type description: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AuthorizationCode()
        if code is not None:
            body.code = code
        if description is not None:
            body.description = description
        url = self.ep(f'outgoingPermission/accessCodes')
        super().post(url=url, params=params, data=body.json())
        return

    def read_call_intercept_settings_workspace(self, workspace_id: str, org_id: str = None) -> ReadCallInterceptSettingsForWorkspaceResponse:
        """
        Retrieves Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with informative announcements and alternative routing options. Depending on the service configuration, none, some, or all incoming calls to the specified workspace are intercepted. Also depending on the service configuration, outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'intercept')
        data = super().get(url=url, params=params)
        return ReadCallInterceptSettingsForWorkspaceResponse.parse_obj(data)

    def configure_call_intercept_settings_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None, incoming: InterceptIncomingPatch = None, outgoing: InterceptOutGoingGet = None):
        """
        Configures a Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with informative announcements and alternative routing options. Depending on the service configuration, none, some, or all incoming calls to the specified person are intercepted. Also depending on the service configuration, outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_write or a user auth token with spark:workspaces_read scope can be used by a person to read their settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: true if call interception is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: InterceptIncomingPatch
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: InterceptOutGoingGet
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallInterceptSettingsForWorkspaceBody()
        if enabled is not None:
            body.enabled = enabled
        if incoming is not None:
            body.incoming = incoming
        if outgoing is not None:
            body.outgoing = outgoing
        url = self.ep(f'intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_transfer_numbers_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveTransferNumbersSettingsForWorkspaceResponse:
        """
        Retrieve Transfer Numbers Settings for a Workspace.
        When calling a specific call type, this workspace will be automatically transferred to another number. The person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type. You can add up to 3 numbers.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'outgoingPermission/autoTransferNumbers')
        data = super().get(url=url, params=params)
        return RetrieveTransferNumbersSettingsForWorkspaceResponse.parse_obj(data)

    def modify_transfer_numbers_settings_workspace(self, workspace_id: str, org_id: str = None, auto_transfer_number1: str = None, auto_transfer_number2: str = None, auto_transfer_number3: str = None):
        """
        Modify Transfer Numbers Settings for a place.
        When calling a specific call type, this workspace will be automatically transferred to another number. The person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type. You can add up to 3 numbers.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param auto_transfer_number1: When calling a specific call type, this workspace will be automatically transferred to another number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this workspace will be automatically transferred to another number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this workspace will be automatically transferred to another number.
        :type auto_transfer_number3: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = RetrieveTransferNumbersSettingsForWorkspaceResponse()
        if auto_transfer_number1 is not None:
            body.auto_transfer_number1 = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body.auto_transfer_number2 = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body.auto_transfer_number3 = auto_transfer_number3
        url = self.ep(f'outgoingPermission/autoTransferNumbers')
        super().put(url=url, params=params, data=body.json())
        return

class UpdateDirectorySyncForBroadWorksEnterpriseBody1(ApiModel):
    #: The toggle to enable/disable directory sync.
    enable_dir_sync: Optional[bool]


class TriggerDirectorySyncForEnterpriseBody1(ApiModel):
    #: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for the BroadWorks enterprise.
    sync_status: Optional[str]


class WebexforBroadworksphonelistsyncApi(ApiChild, base='broadworks/enterprises'):
    """

    """

    def list_broad_works_enterprises(self, sp_enterprise_id: str = None, starts_with: str = None, **params) -> Generator[ListBroadWorksEnterprisesResponse, None, None]:
        """
        List the provisioned enterprises for a Service Provider. This API will also allow a Service Provider to search for their provisioned enterprises on Cisco Webex. A search on enterprises can be performed by either a full or partial enterprise identifier.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        """
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListBroadWorksEnterprisesResponse, params=params)

    def update_sync_for_broad_works_enterprise(self, id: str, enable_dir_sync: bool) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to update enableDirSync for the customers Broadworks enterprise on Cisco Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool
        """
        body = UpdateDirectorySyncForBroadWorksEnterpriseBody1()
        if enable_dir_sync is not None:
            body.enable_dir_sync = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_enterprise(self, id: str, sync_status: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to trigger a directory sync for the customers Broadworks enterprise on Cisco Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param sync_status: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for the BroadWorks enterprise.
        :type sync_status: str
        """
        body = TriggerDirectorySyncForEnterpriseBody1()
        if sync_status is not None:
            body.sync_status = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def sync_status_for_enterprise(self, id: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to  get the most recent directory sync status for a customer Broadworks enterprise on Cisco Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        """
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().get(url=url)
        return BroadworksDirectorySync.parse_obj(data)
