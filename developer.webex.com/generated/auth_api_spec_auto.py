from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['AccessCodes', 'AcdObject', 'Action', 'Action11', 'Action15', 'Action6', 'Action9', 'ActivationStates',
           'AddNewEventForPersonsScheduleResponse', 'AddPhoneNumbersTolocationBody', 'Address', 'Addresses',
           'AlternateNumberSettings', 'AlternateNumbersObject', 'AlternateNumbersWithPattern',
           'AlternateNumbersWithPattern1', 'Always', 'AnnouncementMode', 'Announcements', 'Announcements3',
           'AtaDtmfMethodObject', 'AtaDtmfModeObject', 'AtaObject', 'AudioCodecPriorityObject', 'AudioFileObject',
           'AutoAttendantCallForwardSettingsDetailsObject', 'AutoAttendantCallForwardSettingsModifyDetailsObject',
           'AvailableSharedLineMemberItem', 'BackgroundImage', 'BacklightTimerObject', 'BehaviorType',
           'BlockContiguousSequences', 'BlockPreviousPasscodes', 'BlockRepeatedDigits',
           'BroadWorksEnterprisesWithDeleteOrgImprovementsApi', 'BroadWorksWorkspacesApi', 'BroadworksDirectorySync',
           'BusinessContinuity', 'CDR', 'CLIDPolicySelection', 'Calendar1', 'Call', 'CallBounce', 'CallControlsApi',
           'CallForwardRulesGet', 'CallForwardRulesModifyObject', 'CallForwardRulesObject',
           'CallForwardSelectiveCallsFromCustomNumbersObject', 'CallForwardSelectiveCallsFromObject',
           'CallForwardSelectiveCallsToNumbersObject', 'CallForwardSelectiveCallsToObject',
           'CallForwardSelectiveForwardToObject', 'CallForwarding', 'CallForwarding1', 'CallForwarding4',
           'CallForwardingPlaceSettingGet', 'CallForwardingPlaceSettingPatch', 'CallHistoryRecord',
           'CallHistoryRecordTypeEnum', 'CallParkSettingsObject', 'CallPersonalityEnum', 'CallQueueAudioFilesObject',
           'CallQueueHolidaySchedulesObject', 'CallQueueObject', 'CallQueueQueueSettingsObject', 'CallSourceInfo',
           'CallSourceType', 'CallStateEnum', 'CallType', 'CallTypeEnum', 'CallerIdSelectedType', 'Calling1',
           'CallingLineId', 'CallingPermissionObject', 'CallingPermissions', 'Callparkextension', 'CallsFrom',
           'CallsTo', 'CapabilityMap', 'ComfortMessage', 'ComfortMessageBypass',
           'ConfigureCallInterceptSettingsForWorkspaceBody', 'ConfigureCallRecordingSettingsForPersonBody',
           'ConfigureCallerIDSettingsForPersonBody', 'ConfigurepersonsCallingBehaviorBody', 'CountObject',
           'CreateAutoAttendantResponse', 'CreateCallParkBody', 'CreateCallParkExtensionResponse',
           'CreateCallParkResponse', 'CreateCallPickupBody', 'CreateCallPickupResponse', 'CreateCallQueueResponse',
           'CreateDeviceActivationCodeBody', 'CreateDeviceActivationCodeResponse', 'CreateDialPlanResponse',
           'CreateHuntGroupResponse', 'CreateLocationBody', 'CreateLocationFloorBody', 'CreateLocationResponse',
           'CreatePersonBody', 'CreateReceptionistContactDirectoryResponse', 'CreateRouteGroupForOrganizationBody',
           'CreateRouteGroupForOrganizationResponse', 'CreateRouteListResponse', 'CreateScheduleEventResponse',
           'CreateScheduleForPersonBody', 'CreateScheduleForPersonResponse', 'CreateScheduleResponse',
           'CreateSelectiveCallForwardingRuleForAutoAttendantBody',
           'CreateSelectiveCallForwardingRuleForAutoAttendantResponse',
           'CreateSelectiveCallForwardingRuleForCallQueueBody',
           'CreateSelectiveCallForwardingRuleForCallQueueResponse',
           'CreateSelectiveCallForwardingRuleForHuntGroupResponse', 'CreateTrunkResponse', 'CreatenewPagingGroupBody',
           'CreatenewPagingGroupResponse', 'CreatenewVoicemailGroupForLocationResponse',
           'CustomizationDeviceLevelObject', 'CustomizationObject', 'Day', 'DectDeviceList', 'DectObject',
           'DefaultLoggingLevelObject', 'DefaultVoicemailPinRules', 'DestinationType', 'Device',
           'DeviceConnectionStatus', 'DeviceObject', 'DeviceOwner', 'DeviceStatus', 'DeviceType', 'Devices',
           'DeviceswithWXCDevicesDisplayedApi', 'DialPattern', 'DialPatternAction', 'DialPatternStatus',
           'DialPatternValidate', 'DialPlan', 'DialResponse', 'DirectorySyncStatus',
           'DisplayCallqueueAgentSoftkeysObject', 'DisplayNameSelection', 'DistinctiveRing', 'EffectiveBehaviorType',
           'EmailCopyOfMessage', 'Emergency', 'EnableLocationForWebexCallingResponse', 'ErrorMessageObject',
           'ErrorObject', 'Errors', 'EventLongDetails', 'ExpirePasscode', 'ExtensionDialing', 'ExtensionStatusObject',
           'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'FailedAttempts', 'FaxMessage', 'FeatureAccessCode',
           'FetchEventForpersonsScheduleResponse', 'Floor', 'GenerateExamplePasswordForLocationResponse',
           'GetAnnouncementFileInfo', 'GetAvailableAgentsFromCallParksResponse',
           'GetAvailableAgentsFromCallPickupsResponse', 'GetAvailableRecallHuntGroupsFromCallParksResponse',
           'GetCallForwardAlwaysSettingObject', 'GetCallForwardingSettingsForAutoAttendantResponse',
           'GetCallForwardingSettingsForCallQueueResponse', 'GetCallForwardingSettingsForHuntGroupResponse',
           'GetCallParkSettingsResponse', 'GetCallRecordingSettingsResponse',
           'GetCallRecordingTermsOfServiceSettingsResponse', 'GetDetailedCallHistoryResponse',
           'GetDetailsForAutoAttendantResponse', 'GetDetailsForCallParkExtensionResponse',
           'GetDetailsForCallParkResponse', 'GetDetailsForCallPickupResponse',
           'GetDetailsForCallQueueForcedForwardResponse', 'GetDetailsForCallQueueHolidayServiceResponse',
           'GetDetailsForCallQueueNightServiceResponse', 'GetDetailsForCallQueueResponse',
           'GetDetailsForCallQueueStrandedCallsResponse', 'GetDetailsForHuntGroupResponse',
           'GetDetailsForPagingGroupResponse', 'GetDetailsForScheduleResponse', 'GetDeviceMembersResponse',
           'GetDeviceSettingsResponse', 'GetDialPlanResponse', 'GetListOfPhoneNumbersForPersonResponse',
           'GetLocalGatewayCallToOnPremisesExtensionUsageForTrunkResponse',
           'GetLocalGatewayDialPlanUsageForTrunkResponse', 'GetLocalGatewayUsageCountResponse',
           'GetLocationInterceptResponse', 'GetLocationOutgoingPermissionResponse',
           'GetLocationVoicemailGroupResponse', 'GetLocationVoicemailResponse',
           'GetLocationWebexCallingDetailsResponse', 'GetLocationsUsingLocalGatewayAsPSTNConnectionRoutingResponse',
           'GetManageNumbersJobStatusResponse', 'GetMessageSummaryResponse', 'GetMonitoredElementsObject',
           'GetMusicOnHoldResponse', 'GetNumbersAssignedToRouteListResponse',
           'GetOutgoingPermissionAutoTransferNumberResponse', 'GetOutgoingPermissionLocationAccessCodeResponse',
           'GetPagingGroupAgentObject', 'GetPersonPlaceVirtualLineCallParksObject',
           'GetPersonPlaceVirtualLineCallPickupObject', 'GetPersonPlaceVirtualLineCallQueueObject',
           'GetPersonPlaceVirtualLineHuntGroupObject', 'GetPhoneNumbersForOrganizationWithGivenCriteriasResponse',
           'GetPrivateNetworkConnectResponse', 'GetRecallHuntGroupObject', 'GetRouteGroupsUsingLocalGatewayResponse',
           'GetRouteListResponse', 'GetScheduleDetailsResponse', 'GetScheduleEventObject',
           'GetSelectiveCallForwardingRuleForAutoAttendantResponse',
           'GetSelectiveCallForwardingRuleForCallQueueResponse', 'GetSharedLineAppearanceMembersResponse',
           'GetSharedLineMemberItem', 'GetThirdPartyDeviceResponse', 'GetTrunkResponse', 'GetUserDevicesResponse',
           'GetUserNumberItemObject', 'GetVoicePortalPasscodeRuleResponse', 'GetVoicePortalResponse',
           'GetVoicemailGroupObject', 'GetVoicemailRulesResponse', 'GetVoicemailSettingsResponse',
           'GetWorkspaceCapabilitiesResponse', 'GetWorkspaceDevicesResponse', 'GetpersonsPrivacySettingsResponse',
           'Greeting', 'Greeting29', 'HolidayScheduleLevel', 'HostedAgent', 'HostedFeature', 'HotdeskingStatus',
           'HotelingRequest', 'HoursMenuObject', 'HuntPolicySelection', 'HuntRoutingTypeSelection', 'Incoming',
           'InterceptAnnouncementsGet', 'InterceptIncomingGet', 'InterceptIncomingPatch', 'ItemObject',
           'JobExecutionStatusObject', 'JobExecutionStatusObject1', 'KemModuleTypeObject', 'Key',
           'KeyConfigurationsObject', 'Length', 'LineKeyLEDPattern', 'LineKeyLabelSelection', 'LineType',
           'ListAutoAttendantObject', 'ListBroadWorksEnterprisesResponse', 'ListCPCallParkExtensionObject',
           'ListCallHistoryResponse', 'ListCallParkExtensionObject', 'ListCallParkObject', 'ListCallQueueObject',
           'ListCallsResponse', 'ListChangeDeviceSettingsJobErrorsResponse', 'ListChangeDeviceSettingsJobsResponse',
           'ListDevicesResponse', 'ListLocationFloorsResponse', 'ListLocationObject', 'ListLocationsResponse',
           'ListLocationsWebexCallingDetailsResponse', 'ListManageNumbersJobErrorsResponse',
           'ListManageNumbersJobsResponse', 'ListMessagesResponse', 'ListOfSchedulesForPersonResponse',
           'ListPeopleResponse', 'ListScheduleObject', 'ListVirtualLineObject', 'ListVoicemailGroupResponse',
           'ListWorkspacesResponse', 'LocalGateways', 'Location', 'Location1', 'LocationsApi', 'MacStatusObject',
           'ManagedByObject', 'ManufacturerObject', 'MediaType', 'Member', 'MemberObject', 'MemberType',
           'MessageStorage', 'MessageStorage3', 'ModifyCallerIDSettingsForWorkspaceBody', 'ModifyDialPlanBody',
           'ModifyNumbersForRouteListResponse', 'ModifyOutgoingPermissionSettingsForWorkspaceBody',
           'ModifyPersonPlaceVirtualLineCallQueueObject', 'ModifyRouteListBody', 'ModifyScheduleEventListObject',
           'ModifyTrunkBody', 'ModifypersonsApplicationServicesSettingsBody', 'ModifypersonsMonitoringSettingsBody',
           'MohMessage', 'MonitoredElementItem', 'MonitoredElementUser', 'MonitoredMemberObject',
           'MonitoredPersonObject', 'Month', 'MppAudioCodecPriorityObject', 'MppObject', 'MppVlanObject',
           'NetworkConnectionType', 'NetworkConnectivtyType', 'NewNumber', 'NoAnswer', 'NoAnswer3', 'NormalSource',
           'Notification', 'NumberItem', 'NumberListGetObject', 'NumberStatus', 'OnboardingMethodObject', 'Op',
           'Option', 'OriginatorType', 'Outgoing', 'Overflow', 'Owner', 'ParkResponse', 'PartyInformation', 'Passcode',
           'PbxUser', 'PeopleApi', 'Person', 'PhoneLanguage', 'PhoneNumber', 'PhoneNumbers', 'PhoneNumbers7',
           'PlaceDevices', 'PostCallQueueCallPolicyObject', 'PostHoursMenuObject', 'PostHuntGroupCallPolicyObject',
           'PostPersonPlaceVirtualLineCallQueueObject', 'PostPersonPlaceVirtualLineHuntGroupObject',
           'ProvisionBroadWorksWorkspaceBody', 'ProvisionBroadWorksWorkspaceResponse', 'PstnNumber',
           'PushToTalkAccessType', 'PushToTalkConnectionType', 'PutMemberObject', 'PutRecallHuntGroupObject',
           'PutSharedLineMemberItem', 'ReadBargeInSettingsForPersonResponse',
           'ReadCallBridgeSettingsForPersonResponse', 'ReadCallInterceptSettingsForWorkspaceResponse',
           'ReadCallRecordingSettingsForPersonResponse', 'ReadCallToExtensionLocationsOfRoutingGroupResponse',
           'ReadCallWaitingSettingsForPersonResponse', 'ReadCallerIDSettingsForPersonResponse',
           'ReadDECTDeviceTypeListResponse', 'ReadDialPlanLocationsOfRoutingGroupResponse',
           'ReadDoNotDisturbSettingsForPersonResponse', 'ReadForwardingSettingsForPersonResponse',
           'ReadHotelingSettingsForPersonResponse', 'ReadIncomingPermissionSettingsForPersonResponse',
           'ReadInternalDialingConfigurationForlocationResponse', 'ReadListOfAnnouncementLanguagesResponse',
           'ReadListOfAutoAttendantsResponse', 'ReadListOfCallParkExtensionsResponse', 'ReadListOfCallParksResponse',
           'ReadListOfCallPickupsResponse', 'ReadListOfCallQueueAnnouncementFilesResponse',
           'ReadListOfCallQueuesResponse', 'ReadListOfDialPatternsResponse', 'ReadListOfDialPlansResponse',
           'ReadListOfHuntGroupsResponse', 'ReadListOfPagingGroupsResponse',
           'ReadListOfReceptionistContactDirectoriesResponse', 'ReadListOfRouteListsResponse',
           'ReadListOfRoutingChoicesResponse', 'ReadListOfRoutingGroupsResponse', 'ReadListOfSchedulesResponse',
           'ReadListOfSupportedDevicesResponse', 'ReadListOfTrunkTypesResponse', 'ReadListOfTrunksResponse',
           'ReadListOfUCManagerProfilesResponse', 'ReadListOfVirtualLinesResponse',
           'ReadPSTNConnectionLocationsOfRoutingGroupResponse', 'ReadPersonsCallingBehaviorResponse',
           'ReadPushtoTalkSettingsForPersonResponse', 'ReadReceptionistClientSettingsForPersonResponse',
           'ReadRouteGroupForOrganizationResponse', 'ReadRouteListsOfRoutingGroupResponse',
           'ReadUsageOfRoutingGroupResponse', 'ReadVoicemailSettingsForPersonResponse',
           'ReaddeviceOverrideSettingsFororganizationResponse', 'RecallInformation', 'RecallTypeEnum', 'Record',
           'RecordingStateEnum', 'RecurWeekly2', 'RecurWeeklyObject', 'RecurYearlyByDateObject',
           'RecurYearlyByDayObject', 'Recurrence', 'RecurrenceObject1', 'RedirectionInformation',
           'RedirectionReasonEnum', 'RejectActionEnum', 'Repeat', 'ResponseStatus', 'ResponseStatusType',
           'RetrieveAccessCodesForWorkspaceResponse', 'RetrieveAccessCodesForWorkspaceResponse1',
           'RetrieveCallForwardingSettingsForWorkspaceResponse', 'RetrieveCallForwardingSettingsForWorkspaceResponse1',
           'RetrieveCallQueueAgentsCallerIDInformationResponse', 'RetrieveCallWaitingSettingsForWorkspaceResponse',
           'RetrieveCallWaitingSettingsForWorkspaceResponse1', 'RetrieveCallerIDSettingsForWorkspaceResponse',
           'RetrieveExecutiveAssistantSettingsForPersonResponse', 'RetrieveListOfCallQueueCallerIDInformationResponse',
           'RetrieveMonitoringSettingsForWorkspaceResponse', 'RetrieveOutgoingPermissionSettingsForWorkspaceResponse',
           'RetrievepersonsApplicationServicesSettingsResponse', 'RetrievepersonsMonitoringSettingsResponse',
           'RetrievepersonsOutgoingCallingPermissionsSettingsResponse', 'RingPattern', 'RouteGroup',
           'RouteGroupUsageRouteListGet', 'RouteIdentity', 'RouteList', 'RouteListNumberPatch',
           'RouteListNumberPatchResponse', 'RouteType', 'ScheduleEventObject', 'ScheduleShortDetails',
           'SearchMemberObject', 'SearchMembersResponse', 'SearchSharedLineAppearanceMembersResponse', 'Selection2',
           'Selection3', 'SelectionType', 'SendAllCalls', 'SendBusyCalls', 'SendBusyCalls1', 'SendUnansweredCalls',
           'ServiceType', 'SipAddressesType', 'StartJobResponse', 'State', 'State1', 'State3', 'Status', 'Status1',
           'Status6', 'StepExecutionStatusesObject', 'StorageType', 'SupportAndConfiguredInfo', 'SupportedDevices',
           'TestCallRoutingResponse', 'TriggerDirectorySyncForUserResponse', 'Trunk', 'TrunkType',
           'TrunkTypeWithDeviceType', 'Type', 'Type19', 'Type20', 'Type25', 'Type32', 'Type33', 'Type34', 'Type46',
           'Type5', 'Type8', 'TypeObject', 'UnknownExtensionRouteIdentity', 'UpdateBroadworksWorkspaceBody',
           'UpdateCallParkResponse', 'UpdateCallPickupResponse', 'UpdateDeviceSettingsBody',
           'UpdateEventForpersonsScheduleResponse', 'UpdateLocationBody', 'UpdateLocationWebexCallingDetailsBody',
           'UpdateScheduleEventResponse', 'UpdateScheduleResponse', 'UpdateScheduleResponse1',
           'UpdateSelectiveCallForwardingRuleForAutoAttendantResponse',
           'UpdateSelectiveCallForwardingRuleForCallQueueResponse',
           'UpdateSelectiveCallForwardingRuleForHuntGroupResponse', 'UpdateWorkspaceBody', 'UserNumberItem',
           'UserResponse', 'ValidateDialPatternResponse', 'ValidateExtensionsResponse',
           'ValidateLocalGatewayFQDNAndDomainForTrunkBody', 'ValidatelistOfMACAddressResponse', 'VirtualExtension',
           'VirtualExtensionRange', 'VlanObject', 'VoiceMailPartyInformation', 'VoiceMessageDetails', 'WaitMessage',
           'WaitMode', 'WebexCalling', 'WebexCallingDetailedCallHistoryApi', 'WebexCallingDeviceSettingsApi',
           'WebexCallingDeviceSettingswithDevicesPhase3FeaturesApi',
           'WebexCallingDeviceSettingswithThird-partyDeviceSupportApi', 'WebexCallingOrganizationSettingsApi',
           'WebexCallingOrganizationSettingswithDevicesPhase3FeaturesApi', 'WebexCallingPersonSettingsApi',
           'WebexCallingPersonSettingswithCallBridgeFeatureApi', 'WebexCallingPersonSettingswithCallingBehaviorApi',
           'WebexCallingPersonSettingswithHotelingApi', 'WebexCallingVoiceMessagingApi',
           'WebexCallingWorkspaceSettingsApi', 'WebexCallingWorkspaceSettingswithEnhancedForwardingApi',
           'WebexforBroadworksphonelistsyncApi', 'Week', 'WelcomeMessage', 'WifiNetworkObject', 'Workspace',
           'WorkspaceswithWXCIncludedApi']


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
    #: The number of users updated in CI (Common Identity) in this sync.
    users_updated: Optional[int]
    #: The number of users deleted from CI (Common Identity) in this sync.
    users_deleted: Optional[int]
    #: The number of machines added to CI (Common Identity) in this sync.
    machines_added: Optional[int]
    #: The number of machines updated in CI (Common Identity) in this sync.
    machines_updated: Optional[int]
    #: The number of machines deleted from CI (Common Identity) in this sync.
    machines_deleted: Optional[int]
    #: The number of total external users that have been added to CI across all syncs.
    total_external_users_in_ci: Optional[int]
    #: The number of total external machines that have been added to CI (Common Identity) across all syncs.
    total_external_machines_in_ci: Optional[int]
    #: The date and time of the last successful sync.
    last_successful_sync_time: Optional[str]
    #: Unique tracking identifier.
    last_sync_tracking_id: Optional[str]
    #: List of errors that occurred during that last attempt to sync this BroadWorks enterprise. This list captures
    #: errors that occurred during directory sync of the BroadWorks enterprise, after the API has been accepted and 200
    #: OK response returned. Any errors that occur during initial API request validation will be captured directly in
    #: error response with appropriate HTTP status code.
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


class DialPatternAction(ApiModel):
    #: Add action, when adding a new dial pattern
    add: Optional[str]
    #: Delete action, when deleting an existing dial pattern
    delete: Optional[str]


class Status(DialPatternAction):
    #: The external user is updated in this sync
    update = 'UPDATE'
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
    #: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for
    #: the BroadWorks enterprise.
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
    Not supported for Webex for Government (FedRAMP)
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up for the Webex
    for
    BroadWorks solution. They enable Service Providers to provision Webex Services for their subscribers. Please note
    these APIs require a functional BroadWorks system configured for Webex for BroadWorks. Read more about using this
    API
    at https://www.cisco.com/go/WebexBroadworksAPI.
    Viewing Webex for BroadWorks enterprise information requires an administrator auth token with
    spark-admin:broadworks_enterprises_read scope.
    Updating directory sync configuration or triggering directory sync for a Webex for BroadWorks enterprise requires
    an administrator auth token with spark-admin:broadworks_enterprises_write scope.
    """

    def list_broad_works_enterprises(self, sp_enterprise_id: str = None, starts_with: str = None, max: int = None) -> ListBroadWorksEnterprisesResponse:
        """
        List the provisioned enterprises for a Service Provider. This API also allows a Service Provider to search for
        their provisioned enterprises on Webex. A search on enterprises can be performed using either a full or partial
        enterprise identifier.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        :param max: Limit the number of enterprises returned in the search, up to 1000.
        :type max: int

        documentation: https://developer.webex.com/docs/api/v1/broadworks-enterprises-with-delete-org-improvements/list-broadworks-enterprises
        """
        params = {}
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        if max is not None:
            params['max'] = max
        url = self.ep()
        data = super().get(url=url, params=params)
        return ListBroadWorksEnterprisesResponse.parse_obj(data)

    def update_sync_for_broad_works_enterprise(self, id: str, enable_dir_sync: bool) -> BroadworksDirectorySync:
        """
        This API allows a Partner Admin to update enableDirSync for the customer's Broadworks enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool

        documentation: https://developer.webex.com/docs/api/v1/broadworks-enterprises-with-delete-org-improvements/update-directory-sync-for-a-broadworks-enterprise
        """
        body = UpdateDirectorySyncForBroadWorksEnterpriseBody()
        if enable_dir_sync is not None:
            body.enable_dir_sync = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_enterprise(self, id: str, sync_status: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to trigger a directory sync for the customer's Broadworks enterprise on
        Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param sync_status: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the
            directory sync for the BroadWorks enterprise.
        :type sync_status: str

        documentation: https://developer.webex.com/docs/api/v1/broadworks-enterprises-with-delete-org-improvements/trigger-directory-sync-for-an-enterprise
        """
        body = TriggerDirectorySyncForEnterpriseBody()
        if sync_status is not None:
            body.sync_status = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def sync_status_for_enterprise(self, id: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to get the most recent directory sync status for a customer's Broadworks
        enterprise on Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/broadworks-enterprises-with-delete-org-improvements/get-directory-sync-status-for-an-enterprise
        """
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().get(url=url)
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_user(self, id: str, user_id: str = None) -> TriggerDirectorySyncForUserResponse:
        """
        This API allows a Partner Admin to trigger a directory sync for an external user (real or virtual user) on
        Broadworks enterprise with Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param user_id: The user ID of the Broadworks user to be synced (A non-webex user).
        :type user_id: str

        documentation: https://developer.webex.com/docs/api/v1/broadworks-enterprises-with-delete-org-improvements/trigger-directory-sync-for-a-user
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
    #: This Provisioning ID defines how this workspace is to be provisioned for Cisco Webex Services. Each Customer
    #: Template will have their own unique Provisioning ID. This ID will be displayed under the chosen Customer
    #: Template on Cisco Webex Control Hub.
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
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. They enable Service Providers to provision Cisco Webex Services for their workspaces. Please
    note these APIs require a
    functional BroadWorks system configured for Webex for BroadWorks. Read more about using this API at
    https://www.cisco.com/go/WebexBroadworksAPI.
    Provisioning, updating, and removing workspaces requires an administrator auth token with the
    spark-admin:places_write scope.
    """

    def provision_broad_works(self, provisioning_id: str, sp_enterprise_id: str, display_name: str, user_id: str = None, primary_phone_number: str = None, extension: str = None) -> ProvisionBroadWorksWorkspaceResponse:
        """
        Provision a new BroadWorks workspace for Cisco Webex services.
        This API will allow a Service Provider to provision a workspace for an existing customer.

        :param provisioning_id: This Provisioning ID defines how this workspace is to be provisioned for Cisco Webex
            Services. Each Customer Template will have their own unique Provisioning ID. This ID will be displayed
            under the chosen Customer Template on Cisco Webex Control Hub.
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

        documentation: https://developer.webex.com/docs/api/v1/broadworks-workspaces/provision-a-broadworks-workspace
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
        This API will allow a Service Provider to update certain details of a provisioned BroadWorks workspace on Cisco
        Webex.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str
        :param user_id: The user ID of the workspace on BroadWorks.
        :type user_id: str
        :param primary_phone_number: The primary phone number configured against the workspace on BroadWorks.
        :type primary_phone_number: str
        :param extension: The extension number configured against the workspace on BroadWorks.
        :type extension: str

        documentation: https://developer.webex.com/docs/api/v1/broadworks-workspaces/update-a-broadworks-workspace
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
        This API will allow a Service Provider to remove the mapping between a BroadWorks workspace and Cisco Webex
        device.

        :param workspace_id: A unique Cisco identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/broadworks-workspaces/remove-a-broadworks-workspace
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url=url)
        return

class RejectActionEnum(str, Enum):
    busy = 'busy'
    temporarily_unavailable = 'temporarilyUnavailable'
    ignore = 'ignore'


class CallTypeEnum(str, Enum):
    location = 'location'
    organization = 'organization'
    external = 'external'
    emergency = 'emergency'
    repair = 'repair'
    other = 'other'


class VoiceMailPartyInformation(ApiModel):
    #: The party's name. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be
    #: digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, *73, and user@company.domain.
    number: Optional[str]
    #: The party's person ID. Only present when the person ID is available and privacy is not enabled.
    person_id: Optional[str]
    #: The party's place ID. Only present when the place ID is available and privacy is not enabled.
    place_id: Optional[str]
    #: Indicates whether privacy is enabled for the name, number and personId/placeId.
    privacy_enabled: Optional[bool]


class PartyInformation(VoiceMailPartyInformation):
    #: The call type for the party.
    call_type: Optional[CallTypeEnum]


class DialResponse(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for the same call.
    call_id: Optional[str]
    #: A unique identifier for the call session the call belongs to. This can be used to correlate multiple calls that
    #: are part of the same call session.
    call_session_id: Optional[str]


class CallPersonalityEnum(str, Enum):
    originator = 'originator'
    terminator = 'terminator'
    click_to_dial = 'clickToDial'


class DeviceConnectionStatus(ApiModel):
    connected: Optional[str]
    disconnected: Optional[str]


class CallStateEnum(DeviceConnectionStatus):
    connecting = 'connecting'
    alerting = 'alerting'
    held = 'held'
    remote_held = 'remoteHeld'


class RedirectionReasonEnum(str, Enum):
    busy = 'busy'
    no_answer = 'noAnswer'
    unavailable = 'unavailable'
    unconditional = 'unconditional'
    time_of_day = 'timeOfDay'
    divert = 'divert'
    follow_me = 'followMe'
    hunt_group = 'huntGroup'
    call_queue = 'callQueue'
    unknown = 'unknown'


class RedirectionInformation(ApiModel):
    #: The reason the incoming call was redirected.
    reason: Optional[RedirectionReasonEnum]
    #: The details of a party who redirected the incoming call.
    redirecting_party: Optional[PartyInformation]


class RecallTypeEnum(str, Enum):
    park = 'park'


class RecallInformation(ApiModel):
    #: The type of recall the incoming call is for. Park is the only type of recall currently supported but additional
    #: values may be added in the future.
    type: Optional[RecallTypeEnum]
    #: If the type is park, contains the details of where the call was parked. For example, if user A parks a call
    #: against user B and A is recalled for the park, then this field contains B's information in A's incoming call
    #: details. Only present when the type is park.
    party: Optional[PartyInformation]


class RecordingStateEnum(str, Enum):
    pending = 'pending'
    started = 'started'
    paused = 'paused'
    stopped = 'stopped'
    failed = 'failed'


class Call(ApiModel):
    #: The call identifier of the call.
    id: Optional[str]
    #: The call session identifier of the call session the call belongs to. This can be used to correlate multiple
    #: calls that are part of the same call session.
    call_session_id: Optional[str]
    #: The personality of the call.
    personality: Optional[CallPersonalityEnum]
    #: The current state of the call.
    state: Optional[CallStateEnum]
    #: The remote party's details. For example, if user A calls user B then B is the remote party in A's outgoing call
    #: details and A is the remote party in B's incoming call details.
    remote_party: Optional[PartyInformation]
    #: The appearance value for the call. The appearance value can be used to display the user's calls in an order
    #: consistent with the user's devices. Only present when the call has an appearance value assigned.
    appearance: Optional[int]
    #: The date and time the call was created.
    created: Optional[str]
    #: The date and time the call was answered. Only present when the call has been answered.
    answered: Optional[str]
    #: The list of details for previous redirections of the incoming call ordered from most recent to least recent. For
    #: example, if user B forwards an incoming call to user C, then a redirection entry is present for B's forwarding
    #: in C's incoming call details. Only present when there were previous redirections and the incoming call's state
    #: is alerting.
    redirections: Optional[list[RedirectionInformation]]
    #: The recall details for the incoming call. Only present when the incoming call is for a recall.
    recall: Optional[RecallInformation]
    #: The call's current recording state. Only present when the user's call recording has been invoked during the life
    #: of the call.
    recording_state: Optional[RecordingStateEnum]


class CallHistoryRecordTypeEnum(str, Enum):
    placed = 'placed'
    missed = 'missed'
    received = 'received'


class CallHistoryRecord(ApiModel):
    #: The type of call history record.
    type: Optional[CallHistoryRecordTypeEnum]
    #: The name of the called/calling party. Only present when the name is available and privacy is not enabled.
    name: Optional[str]
    #: The number of the called/calling party. Only present when the number is available and privacy is not enabled.
    #: The number can be digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, *73,
    #: user@company.domain
    number: Optional[str]
    #: Indicates whether privacy is enabled for the name and number.
    privacy_enabled: Optional[bool]
    #: The date and time the call history record was created. For a placed call history record, this is when the call
    #: was placed. For a missed call history record, this is when the call was disconnected. For a received call
    #: history record, this is when the call was answered.
    time: Optional[str]


class DialBody(ApiModel):
    #: The destination to be dialed. The destination can be digits or a URI. Some examples for destination include:
    #: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, and sip:user@company.domain.
    destination: Optional[str]


class AnswerBody(ApiModel):
    #: The call identifier of the call to be answered.
    call_id: Optional[str]


class RejectBody(ApiModel):
    #: The call identifier of the call to be rejected.
    call_id: Optional[str]
    #: The rejection action to apply to the call. The busy action is applied if no specific action is provided.
    action: Optional[RejectActionEnum]


class HangupBody(ApiModel):
    #: The call identifier of the call to hangup.
    call_id: Optional[str]


class HoldBody(ApiModel):
    #: The call identifier of the call to hold.
    call_id: Optional[str]


class ResumeBody(ApiModel):
    #: The call identifier of the call to resume.
    call_id: Optional[str]


class DivertBody(ApiModel):
    #: The call identifier of the call to divert.
    call_id: Optional[str]
    #: The destination to divert the call to. If toVoicemail is false, destination is required. The destination can be
    #: digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444,
    #: user@company.domain, sip:user@company.domain
    destination: Optional[str]
    #: If set to true, the call is diverted to voicemail. If no destination is specified, the call is diverted to the
    #: user's own voicemail. If a destination is specified, the call is diverted to the specified user's voicemail.
    to_voicemail: Optional[bool]


class TransferBody(ApiModel):
    #: The call identifier of the first call to transfer. This parameter is mandatory if either callId2 or destination
    #: is provided.
    call_id1: Optional[str]
    #: The call identifier of the second call to transfer. This parameter is mandatory if callId1 is provided and
    #: destination is not provided.
    call_id2: Optional[str]
    #: The destination to be transferred to. The destination can be digits or a URI. Some examples for destination
    #: include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain. This
    #: parameter is mandatory if callId1 is provided and callId2 is not provided.
    destination: Optional[str]


class ParkBody(ApiModel):
    #: The call identifier of the call to park.
    call_id: Optional[str]
    #: Identifes where the call is to be parked. If not provided, the call is parked against the parking user. The
    #: destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73,
    #: tel:+12223334444, user@company.domain, sip:user@company.domain
    destination: Optional[str]
    #: If set totrue, the call is parked against an automatically selected member of the user's call park group and the
    #: destination parameter is ignored.
    is_group_park: Optional[bool]


class ParkResponse(ApiModel):
    #: The details of where the call has been parked.
    parked_against: Optional[PartyInformation]


class RetrieveBody(ApiModel):
    #: Identifies where the call is parked. The number field from the park command response can be used as the
    #: destination for the retrieve command. If not provided, the call parked against the retrieving user is retrieved.
    #: The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444,
    #: *73, tel:+12223334444, user@company.domain, sip:user@company.domain
    destination: Optional[str]


class StartRecordingBody(ApiModel):
    #: The call identifier of the call to start recording.
    call_id: Optional[str]


class StopRecordingBody(ApiModel):
    #: The call identifier of the call to stop recording.
    call_id: Optional[str]


class PauseRecordingBody(ApiModel):
    #: The call identifier of the call to pause recording.
    call_id: Optional[str]


class ResumeRecordingBody(ApiModel):
    #: The call identifier of the call to resume recording.
    call_id: Optional[str]


class TransmitDTMFBody(ApiModel):
    #: The call identifier of the call to transmit DTMF digits for.
    call_id: Optional[str]
    #: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, *, #,
    #: A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value “1,234”, the DTMF 1
    #: digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent successively.
    dtmf: Optional[str]


class PushBody(ApiModel):
    #: The call identifier of the call to push.
    call_id: Optional[str]


class PickupBody(ApiModel):
    #: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the user's call pickup
    #: group is picked up. The target can be digits or a URI. Some examples for target include: 1234, 2223334444,
    #: +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
    target: Optional[str]


class BargeInBody(ApiModel):
    #: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target include: 1234,
    #: 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
    target: Optional[str]


class ListCallsResponse(ApiModel):
    items: Optional[list[Call]]


class ListCallHistoryResponse(ApiModel):
    items: Optional[list[CallHistoryRecord]]


class CallControlsApi(ApiChild, base='telephony/calls'):
    """
    Not supported for Webex for Government (FedRAMP)
    Call Control APIs in support of Webex Calling.
    All GET commands require the spark:calls_read scope while all other commands require the spark:calls_write scope.
    NOTE: These APIs support 3rd Party Call Control only.
    """

    def dial(self, destination: str) -> DialResponse:
        """
        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts occur on all the devices belonging to a user. When a user answers on one of these
        alerting devices, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, and
            sip:user@company.domain.
        :type destination: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/dial
        """
        body = DialBody()
        if destination is not None:
            body.destination = destination
        url = self.ep('dial')
        data = super().post(url=url, data=body.json())
        return DialResponse.parse_obj(data)

    def answer(self, call_id: str):
        """
        Answer an incoming call on a user's primary device.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/answer
        """
        body = AnswerBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('answer')
        super().post(url=url, data=body.json())
        return

    def reject(self, call_id: str, action: RejectActionEnum = None):
        """
        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        :type action: RejectActionEnum

        documentation: https://developer.webex.com/docs/api/v1/call-controls/reject
        """
        body = RejectBody()
        if call_id is not None:
            body.call_id = call_id
        if action is not None:
            body.action = action
        url = self.ep('reject')
        super().post(url=url, data=body.json())
        return

    def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/hangup
        """
        body = HangupBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('hangup')
        super().post(url=url, data=body.json())
        return

    def hold(self, call_id: str):
        """
        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/hold
        """
        body = HoldBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('hold')
        super().post(url=url, data=body.json())
        return

    def resume(self, call_id: str):
        """
        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/resume
        """
        body = ResumeBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('resume')
        super().post(url=url, data=body.json())
        return

    def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert a call to a destination or a user's voicemail. This is also commonly referred to as a Blind Transfer.

        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the
            call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the
            specified user's voicemail.
        :type to_voicemail: bool

        documentation: https://developer.webex.com/docs/api/v1/call-controls/divert
        """
        body = DivertBody()
        if call_id is not None:
            body.call_id = call_id
        if destination is not None:
            body.destination = destination
        if to_voicemail is not None:
            body.to_voicemail = to_voicemail
        url = self.ep('divert')
        super().post(url=url, data=body.json())
        return

    def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None):
        """
        Transfer two calls together.
        Unanswered incoming calls cannot be transferred but can be diverted using the divert API.
        If the user has only two calls and wants to transfer them together, the callId1 and callId2 parameters are
        optional and when not provided the calls are automatically selected and transferred.
        If the user has more than two calls and wants to transfer two of them together, the callId1 and callId2
        parameters are mandatory to specify which calls are being transferred. Those are also commonly referred to as
        Attended Transfer, Consultative Transfer, or Supervised Transfer and will return a 204 response.
        If the user wants to transfer one call to a new destination but only when the destination responds, the callId1
        and destination parameters are mandatory to specify the call being transferred and the destination.
        This is referred to as a Mute Transfer and is similar to the divert API with the difference of waiting for the
        destination to respond prior to transferring the call. If the destination does not respond, the call is not
        transferred. This will return a 201 response.

        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either
            callId2 or destination is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the second call to transfer. This parameter is mandatory if callId1 is
            provided and destination is not provided.
        :type call_id2: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some examples
            for destination include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain,
            sip:user@company.domain. This parameter is mandatory if callId1 is provided and callId2 is not provided.
        :type destination: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/transfer
        """
        body = TransferBody()
        if call_id1 is not None:
            body.call_id1 = call_id1
        if call_id2 is not None:
            body.call_id2 = call_id2
        if destination is not None:
            body.destination = destination
        url = self.ep('transfer')
        super().post(url=url, data=body.json())
        return

    def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> PartyInformation:
        """
        Park a connected call. The number field in the response can be used as the destination for the retrieve command
        to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifes where the call is to be parked. If not provided, the call is parked against the
            parking user. The destination can be digits or a URI. Some examples for destination include: 1234,
            2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param is_group_park: If set totrue, the call is parked against an automatically selected member of the user's
            call park group and the destination parameter is ignored.
        :type is_group_park: bool

        documentation: https://developer.webex.com/docs/api/v1/call-controls/park
        """
        body = ParkBody()
        if call_id is not None:
            body.call_id = call_id
        if destination is not None:
            body.destination = destination
        if is_group_park is not None:
            body.is_group_park = is_group_park
        url = self.ep('park')
        data = super().post(url=url, data=body.json())
        return PartyInformation.parse_obj(data["parkedAgainst"])

    def retrieve(self, destination: str = None) -> DialResponse:
        """
        Retrieve a parked call. A new call is initiated to perform the retrieval in a similar manner to the dial
        command. The number field from the park command response can be used as the destination for the retrieve
        command.

        :param destination: Identifies where the call is parked. The number field from the park command response can be
            used as the destination for the retrieve command. If not provided, the call parked against the retrieving
            user is retrieved. The destination can be digits or a URI. Some examples for destination include: 1234,
            2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/retrieve
        """
        body = RetrieveBody()
        if destination is not None:
            body.destination = destination
        url = self.ep('retrieve')
        data = super().post(url=url, data=body.json())
        return DialResponse.parse_obj(data)

    def start(self, call_id: str = None):
        """
        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On
        Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/start-recording
        """
        body = StartRecordingBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('startRecording')
        super().post(url=url, data=body.json())
        return

    def stop(self, call_id: str = None):
        """
        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/stop-recording
        """
        body = StopRecordingBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('stopRecording')
        super().post(url=url, data=body.json())
        return

    def pause(self, call_id: str = None):
        """
        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/pause-recording
        """
        body = PauseRecordingBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('pauseRecording')
        super().post(url=url, data=body.json())
        return

    def resume(self, call_id: str = None):
        """
        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/resume-recording
        """
        body = ResumeRecordingBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('resumeRecording')
        super().post(url=url, data=body.json())
        return

    def transmit_dtmf(self, call_id: str = None, dtmf: str = None):
        """
        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to transmit DTMF digits for.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, *, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        :type dtmf: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/transmit-dtmf
        """
        body = TransmitDTMFBody()
        if call_id is not None:
            body.call_id = call_id
        if dtmf is not None:
            body.dtmf = dtmf
        url = self.ep('transmitDtmf')
        super().post(url=url, data=body.json())
        return

    def push(self, call_id: str = None):
        """
        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant's call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/push
        """
        body = PushBody()
        if call_id is not None:
            body.call_id = call_id
        url = self.ep('push')
        super().post(url=url, data=body.json())
        return

    def pickup(self, target: str = None) -> DialResponse:
        """
        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner to
        the dial command. When target is not present, the API pickups up a call from the user's call pickup group. When
        target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user's call pickup group is picked up. The target can be digits or a URI. Some examples for target include:
            1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/pickup
        """
        body = PickupBody()
        if target is not None:
            body.target = target
        url = self.ep('pickup')
        data = super().post(url=url, data=body.json())
        return DialResponse.parse_obj(data)

    def barge_in(self, target: str) -> DialResponse:
        """
        Barge-in on another user's answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/barge-in
        """
        body = BargeInBody()
        if target is not None:
            body.target = target
        url = self.ep('bargeIn')
        data = super().post(url=url, data=body.json())
        return DialResponse.parse_obj(data)

    def list_calls(self) -> list[Call]:
        """
        Get the list of details for all active calls associated with the user.

        documentation: https://developer.webex.com/docs/api/v1/call-controls/list-calls
        """
        url = self.ep()
        data = super().get(url=url)
        return parse_obj_as(list[Call], data["items"])

    def call_details(self, call_id: str) -> Call:
        """
        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/get-call-details
        """
        url = self.ep(f'{call_id}')
        data = super().get(url=url)
        return Call.parse_obj(data)

    def list_call_history(self, type_: str = None) -> list[CallHistoryRecord]:
        """
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param type_: The type of call history records to retrieve. If not specified, then all call history records are
            retrieved. Possible values: placed, missed, received
        :type type_: str

        documentation: https://developer.webex.com/docs/api/v1/call-controls/list-call-history
        """
        params = {}
        if type_ is not None:
            params['type'] = type_
        url = self.ep('history')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[CallHistoryRecord], data["items"])

class NetworkConnectivtyType(ApiModel):
    wired: Optional[str]


class Device(ApiModel):
    #: A unique identifier for the device.
    id: Optional[str]
    #: A friendly name for the device.
    display_name: Optional[str]
    #: The placeId field has been deprecated. Please use workspaceId instead.
    place_id: Optional[str]
    #: The workspace associated with the device.
    workspace_id: Optional[str]
    #: The person associated with the device.
    person_id: Optional[str]
    #: The organization associated with the device.
    org_id: Optional[str]
    #: The capabilities of the device.
    capabilities: Optional[list[xapi]]
    #: The permissions the user has for this device. For example, xapi means this user is entitled to using the xapi
    #: against this device.
    permissions: Optional[list[xapi]]
    #: The connection status of the device.
    connection_status: Optional[DeviceConnectionStatus]
    #: The product name. A display friendly version of the device's model.
    product: Optional[str]
    #: The product type.
    type: Optional[str]
    #: Tags assigned to the device.
    tags: Optional[list[str]]
    #: The current IP address of the device.
    ip: Optional[str]
    #: The current network connectivty for the device.
    active_interface: Optional[NetworkConnectivtyType]
    #: The unique address for the network adapter.
    mac: Optional[str]
    #: The primary SIP address to dial this device.
    primary_sip_url: Optional[str]
    #: All SIP addresses to dial this device.
    sip_urls: Optional[list[str]]
    #: Serial number for the device.
    serial: Optional[str]
    #: The operating system name data and version tag.
    software: Optional[str]
    #: The upgrade channel the device is assigned to.
    upgrade_channel: Optional[str]
    #: The date and time that the device was registered, in ISO8601 format.
    created: Optional[str]
    #: The date and time that the device was first seen, in ISO8601 format.
    first_seen: Optional[str]
    #: The date and time that the device was last seen, in ISO8601 format.
    last_seen: Optional[str]


class Op(str, Enum):
    #: Add a new tags list to the device.
    add = 'add'
    #: Remove all tags from the device.
    remove = 'remove'
    #: Replace the tags list on the device.
    replace = 'replace'


class CreateDeviceActivationCodeBody(ApiModel):
    #: The ID of the workspace where the device will be activated.
    workspace_id: Optional[str]
    #: The ID of the person who will own the device once activated.
    person_id: Optional[str]
    #: The model of the device being created.
    model: Optional[str]


class ListDevicesResponse(ApiModel):
    items: Optional[list[Device]]


class ModifyDeviceTagsBody(ApiModel):
    op: Optional[Op]
    #: Only the tags path is supported to patch.
    path: Optional[str]
    #: Possible values: First Tag, Second Tag
    value: Optional[list[str]]


class CreateDeviceActivationCodeResponse(ApiModel):
    #: The activation code.
    code: Optional[str]
    #: The date and time the activation code expires.
    expiry_time: Optional[str]


class CreateDeviceByMACAddressBody(CreateDeviceActivationCodeBody):
    #: The MAC address of the device being created.
    mac: Optional[str]
    #: SIP password to be configured for the phone, only required with third party devices.
    password: Optional[str]


class DeviceswithWXCDevicesDisplayedApi(ApiChild, base='devices'):
    """
    Devices represent cloud-registered Webex RoomOS devices or IP Phones. Devices may be associated with Workspaces or
    People.
    The following scopes are required for performing the specified actions:
    Searching and viewing details for devices requires an auth token with the spark:devices_read scope.
    Updating or deleting your devices requires an auth token with the spark:devices_write scope.
    Viewing the list of all devices in an organization requires an administrator auth token with the
    spark-admin:devices_read scope.
    Adding, updating, or deleting all devices in an organization requires an administrator auth token with the
    spark-admin:devices_write scope.
    Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
    """

    def list(self, person_id: str = None, workspace_id: str = None, org_id: str = None, display_name: str = None, product: str = None, type_: str = None, tag: str = None, connection_status: str = None, serial: str = None, software: str = None, upgrade_channel: str = None, error_code: str = None, capability: str = None, permission: str = None, **params) -> Generator[Device, None, None]:
        """
        Lists all active Webex RoomOS devices or IP Phones associated with the authenticated user, such as devices
        activated in personal mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name. Possible values: DX-80, RoomKit, SX-80
        :type product: str
        :param type_: List devices with this type. Possible values: roomdesk, phone, accessory, webexgo, unknown
        :type type_: str
        :param tag: List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma
            separating the tag values or adding several tag parameters.
        :type tag: str
        :param connection_status: List devices with this connection status.
        :type connection_status: str
        :param serial: List devices with this serial number.
        :type serial: str
        :param software: List devices with this software version.
        :type software: str
        :param upgrade_channel: List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code: List devices with this error code.
        :type error_code: str
        :param capability: List devices with this capability. Possible values: xapi
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/list-devices
        """
        if person_id is not None:
            params['personId'] = person_id
        if workspace_id is not None:
            params['workspaceId'] = workspace_id
        if org_id is not None:
            params['orgId'] = org_id
        if display_name is not None:
            params['displayName'] = display_name
        if product is not None:
            params['product'] = product
        if type_ is not None:
            params['type'] = type_
        if tag is not None:
            params['tag'] = tag
        if connection_status is not None:
            params['connectionStatus'] = connection_status
        if serial is not None:
            params['serial'] = serial
        if software is not None:
            params['software'] = software
        if upgrade_channel is not None:
            params['upgradeChannel'] = upgrade_channel
        if error_code is not None:
            params['errorCode'] = error_code
        if capability is not None:
            params['capability'] = capability
        if permission is not None:
            params['permission'] = permission
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, params=params)

    def details(self, device_id: str, org_id: str = None) -> Device:
        """
        Shows details for a device, by ID.
        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/get-device-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        data = super().get(url=url, params=params)
        return Device.parse_obj(data)

    def delete(self, device_id: str, org_id: str = None):
        """
        Deletes a device, by ID.
        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/delete-a-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        super().delete(url=url, params=params)
        return

    def modify_tags(self, device_id: str, org_id: str = None, op: Op = None, path: str = None, value: List[str] = None) -> Device:
        """
        Update requests use the JSON Patch syntax.
        The request must include a Content-Type header with the value application/json-patch+json.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :param op: 
        :type op: Op
        :param path: Only the tags path is supported to patch.
        :type path: str
        :param value: Possible values: First Tag, Second Tag
        :type value: List[str]

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/modify-device-tags
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyDeviceTagsBody()
        if op is not None:
            body.op = op
        if path is not None:
            body.path = path
        if value is not None:
            body.value = value
        url = self.ep(f'{device_id}')
        data = super().patch(url=url, params=params, data=body.json())
        return Device.parse_obj(data)

    def create_activation_code(self, org_id: str = None, workspace_id: str = None, person_id: str = None, model: str = None) -> CreateDeviceActivationCodeResponse:
        """
        Generate an activation code for a device in a specific workspace by workspaceId or for a person by personId.

        :param org_id: The organization associated with the activation code generated. If left empty, the organization
            associated with the caller will be used.
        :type org_id: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/create-a-device-activation-code
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateDeviceActivationCodeBody()
        if workspace_id is not None:
            body.workspace_id = workspace_id
        if person_id is not None:
            body.person_id = person_id
        if model is not None:
            body.model = model
        url = self.ep('activationCode')
        data = super().post(url=url, params=params, data=body.json())
        return CreateDeviceActivationCodeResponse.parse_obj(data)

    def create_by_mac_address(self, mac: str, org_id: str = None, workspace_id: str = None, person_id: str = None, model: str = None, password: str = None) -> Device:
        """
        Create a phone by its MAC address in a specific workspace or for a person.
        Specify the mac, model and either workspaceId or personId.

        :param mac: The MAC address of the device being created.
        :type mac: str
        :param org_id: The organization associated with the device. If left empty, the organization associated with the
            caller will be used.
        :type org_id: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param password: SIP password to be configured for the phone, only required with third party devices.
        :type password: str

        documentation: https://developer.webex.com/docs/api/v1/devices-with-wxc-devices-displayed/create-a-device-by-mac-address
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateDeviceByMACAddressBody()
        if mac is not None:
            body.mac = mac
        if workspace_id is not None:
            body.workspace_id = workspace_id
        if person_id is not None:
            body.person_id = person_id
        if model is not None:
            body.model = model
        if password is not None:
            body.password = password
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Device.parse_obj(data)

class Address(ApiModel):
    #: Address 1
    address1: Optional[str]
    #: Address 2
    address2: Optional[str]
    #: City
    city: Optional[str]
    #: State code
    state: Optional[str]
    #: ZIP/Postal Code
    postal_code: Optional[str]
    #: ISO-3166 2-Letter Country Code.
    country: Optional[str]


class Location1(ApiModel):
    #: Location identifier associated with the members.
    id: Optional[str]
    #: Location name associated with the member.
    name: Optional[str]


class Location(Location1):
    #: The ID of the organization to which this location belongs.
    org_id: Optional[str]
    #: Time zone associated with this location.
    time_zone: Optional[str]
    #: The address of the location.
    address: Optional[Address]


class UpdateLocationBody(ApiModel):
    #: The name of the location.
    name: Optional[str]
    #: Time zone associated with this location, refer to this link
    #: (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone)
    #: for format.
    time_zone: Optional[str]
    #: Default email language.
    preferred_language: Optional[str]
    #: The address of the location.
    address: Optional[Address]


class CreateLocationFloorBody(ApiModel):
    #: The floor number.
    floor_number: Optional[int]
    #: The floor display name.
    display_name: Optional[str]


class Floor(CreateLocationFloorBody):
    #: Unique identifier for the floor.
    id: Optional[str]
    #: Unique identifier for the location.
    location_id: Optional[str]


class ListLocationsResponse(ApiModel):
    items: Optional[list[Location]]


class CreateLocationBody(UpdateLocationBody):
    #: Location's phone announcement language.
    announcement_language: Optional[str]


class CreateLocationResponse(ApiModel):
    #: ID of the newly created location.
    id: Optional[str]


class ListLocationFloorsResponse(ApiModel):
    #: An array of floor objects.
    items: Optional[list[Floor]]


class LocationsApi(ApiChild, base='locations'):
    """
    Locations allow you to organize users and workspaces based on a physical location. You can configure both calling
    and workspace management functions into the same location. To enable a location for Webex Calling, use the Enable a
    Location for Webex Calling API.
    You can also create and inspect locations in Webex Control Hub. See Locations on Control Hub for more information.
    """

    def list(self, name: str = None, id: str = None, org_id: str = None, **params) -> Generator[Location, None, None]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param id: List locations by ID.
        :type id: str
        :param org_id: List locations in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/list-locations
        """
        if name is not None:
            params['name'] = name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Location, params=params)

    def details(self, location_id: str, org_id: str = None) -> Location:
        """
        Shows details for a location, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id: Get location common attributes for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/get-location-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}')
        data = super().get(url=url, params=params)
        return Location.parse_obj(data)

    def create(self, announcement_language: str, org_id: str = None, name: str = None, time_zone: str = None, preferred_language: str = None, address: Address = None) -> str:
        """
        Create a new Location for a given organization. Only an admin in the organization can create a new Location.

        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param org_id: Create a location common attribute for this organization.
        :type org_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this link
            (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone)
            for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param address: The address of the location.
        :type address: Address

        documentation: https://developer.webex.com/docs/api/v1/locations/create-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateLocationBody()
        if announcement_language is not None:
            body.announcement_language = announcement_language
        if name is not None:
            body.name = name
        if time_zone is not None:
            body.time_zone = time_zone
        if preferred_language is not None:
            body.preferred_language = preferred_language
        if address is not None:
            body.address = address
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update(self, location_id: str, org_id: str = None, name: str = None, time_zone: str = None, preferred_language: str = None, address: Address = None):
        """
        Update details for a location, by ID.

        :param location_id: Update location common attributes for this location.
        :type location_id: str
        :param org_id: Update location common attributes for this organization.
        :type org_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this link
            (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone)
            for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param address: The address of the location.
        :type address: Address

        documentation: https://developer.webex.com/docs/api/v1/locations/update-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateLocationBody()
        if name is not None:
            body.name = name
        if time_zone is not None:
            body.time_zone = time_zone
        if preferred_language is not None:
            body.preferred_language = preferred_language
        if address is not None:
            body.address = address
        url = self.ep(f'{location_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def list_floors(self, location_id: str) -> list[Floor]:
        """
        List location floors.
        Requires an administrator auth token with the spark-admin:locations_read scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/list-location-floors
        """
        url = self.ep(f'{location_id}/floors')
        data = super().get(url=url)
        return parse_obj_as(list[Floor], data["items"])

    def create_floor(self, location_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Create a new floor in the given location. The displayName parameter is optional, and omitting it will result in
        the creation of a floor without that value set.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/locations/create-a-location-floor
        """
        body = CreateLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors')
        data = super().post(url=url, data=body.json())
        return Floor.parse_obj(data)

    def floor_details(self, location_id: str, floor_id: str) -> Floor:
        """
        Shows details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI.
        Requires an administrator auth token with the spark-admin:locations_read scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/get-location-floor-details
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().get(url=url)
        return Floor.parse_obj(data)

    def update_floor(self, location_id: str, floor_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all
        details for the floor returned by a previous call to Get Location Floor Details. Omitting the optional
        displayName field will result in that field no longer being defined for the floor.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/locations/update-a-location-floor
        """
        body = CreateLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = super().put(url=url, data=body.json())
        return Floor.parse_obj(data)

    def delete_floor(self, location_id: str, floor_id: str):
        """
        Deletes a floor, by ID.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/delete-a-location-floor
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        super().delete(url=url)
        return

class PhoneNumbers(ApiModel):
    #: The type of phone number.
    #: Possible values: work, mobile, fax
    type: Optional[str]
    #: The phone number.
    #: Possible values: +1 408 526 7209
    value: Optional[str]


class SipAddressesType(PhoneNumbers):
    primary: Optional[bool]


class Status1(str, Enum):
    #: Active within the last 10 minutes
    active = 'active'
    #: The user is in a call
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: Last activity occurred more than 10 minutes ago
    inactive = 'inactive'
    #: The user is in a meeting
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined
    pending = 'pending'
    #: The user is sharing content
    presenting = 'presenting'
    #: The user’s status could not be determined
    unknown = 'unknown'


class Type(str, Enum):
    #: Account belongs to a person
    person = 'person'
    #: Account is a bot user
    bot = 'bot'
    #: Account is a guest user
    appuser = 'appuser'


class Addresses(ApiModel):
    #: The type of address
    #: Possible values: work
    type: Optional[str]
    #: The user's country
    #: Possible values: US
    country: Optional[str]
    #: the user's locality, often city
    #: Possible values: Milpitas
    locality: Optional[str]
    #: the user's region, often state
    #: Possible values: California
    region: Optional[str]
    #: the user's street
    #: Possible values: 1099 Bird Ave.
    street_address: Optional[str]
    #: the user's postal or zip code
    #: Possible values: 99212
    postal_code: Optional[str]


class CreatePersonBody(ApiModel):
    #: The email addresses of the person. Only one email address is allowed per person.
    #: Possible values: john.andersen@example.com
    emails: Optional[list[str]]
    #: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling license.
    phone_numbers: Optional[list[PhoneNumbers]]
    #: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license.
    extension: Optional[str]
    #: The ID of the location for this person.
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
    #: An array of role strings representing the roles to which this admin user belongs.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    licenses: Optional[list[str]]
    #: The business department the user belongs to.
    department: Optional[str]
    #: A manager identifier.
    manager: Optional[str]
    #: Person Id of the manager
    manager_id: Optional[str]
    #: the person's title
    title: Optional[str]
    #: Person's address
    addresses: Optional[list[Addresses]]
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg:
    #: mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]]


class Person(CreatePersonBody):
    #: A unique identifier for the person.
    id: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    nick_name: Optional[str]
    #: The date and time the person was created.
    created: Optional[str]
    #: The date and time the person was last changed.
    last_modified: Optional[str]
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user has
    #: disabled status sharing.
    last_activity: Optional[str]
    #: The users sip addresses. Read-only.
    sip_addresses: Optional[list[SipAddressesType]]
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has disabled status
    #: sharing.
    status: Optional[Status1]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    type: Optional[Type]


class ListPeopleResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]]
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]]


class UpdatePersonBody(CreatePersonBody):
    #: The nickname of the person if configured. Set to the firstName automatically in update request.
    nick_name: Optional[str]
    #: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is
    #: an admin user for the person's organization.
    login_enabled: Optional[bool]


class PeopleApi(ApiChild, base='people'):
    """
    People are registered users of Webex. Searching and viewing People requires an auth token with a scope of
    spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token with
    spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token with the
    spark-admin:people_write and spark-admin:people_read scope.
    A person's call settings are for Webex Calling and necessitate Webex Calling licenses.
    To learn more about managing people in a room see the Memberships API. For information about how to allocate Hybrid
    Services licenses to people, see the Managing Hybrid Services guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, roles: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=
        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.
        Lookup by roles is only supported for Admin users for the people within the same org.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required. With the exception of partner admins and a managed org relationship, people lookup by email is
            only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided
            then presence information (such as the lastActivity or status properties) will not be included in the
            response.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/list-people
        """
        if email is not None:
            params['email'] = email
        if display_name is not None:
            params['displayName'] = display_name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        if roles is not None:
            params['roles'] = roles
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Person, params=params)

    def create(self, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.
        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.
        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        When doing attendee management, append #attendee to the siteUrl parameter (e.g. mysite.webex.com#attendee) to
        make the new user an attendee for a site.

        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
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
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]

        documentation: https://developer.webex.com/docs/api/v1/people/create-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
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
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-person-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, emails: List[str], calling_data: bool = None, show_all_types: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None, nick_name: str = None, login_enabled: bool = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is
        already an existing calling user.
        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to
        the respective siteUrl and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the siteurl parameter.
        To remove the attendee privilege for a user on a meeting site, remove the sitename#attendee from the siteUrls
        array. The showAllTypes parameter must be set to true.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
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
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        :param nick_name: The nickname of the person if configured. Set to the firstName automatically in update
            request.
        :type nick_name: str
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the
            authenticated user is an admin user for the person's organization.
        :type login_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/people/update-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        body = UpdatePersonBody()
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
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        if nick_name is not None:
            body.nick_name = nick_name
        if login_enabled is not None:
            body.login_enabled = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def delete(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/delete-a-person
        """
        url = self.ep(f'{person_id}')
        super().delete(url=url)
        return

    def my_own_details(self, calling_data: bool = None) -> Person:
        """
        Get profile details for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-my-own-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

class CDR(ApiModel):
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[str] = Field(alias='Answer time')
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered, and one will
    #: be answered.
    answered: Optional[str]
    #: The authorization code admin created for a location or site for users to use. Collected by the
    #: Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str] = Field(alias='Authorization code')
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call if
    #: necessary.
    call_id: Optional[str] = Field(alias='Call ID')
    #: Type of call. For example:
    #:   * SIP_MEETING
    #:   * SIP_INTERNATIONAL
    #:   * SIP_SHORTCODE
    #:   * SIP_INBOUND
    #:   * UNKNOWN
    #:   * SIP_EMERGENCY
    #:   * SIP_PREMIUM
    #:   * SIP_ENTERPRISE
    #:   * SIP_TOLLFREE
    #:   * SIP_NATIONAL
    #:   * SIP_MOBILE
    call_type: Optional[str] = Field(alias='Call type')
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the called
    #: party.
    called_line_id: Optional[str] = Field(alias='Called line ID')
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the
    #: called party.
    called_number: Optional[str] = Field(alias='Called number')
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of
    #: the user.
    calling_line_id: Optional[str] = Field(alias='Calling line ID')
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number of
    #: the user.
    calling_number: Optional[str] = Field(alias='Calling number')
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    #:   * SIP
    #:   * WXC_CLIENT
    #:   * WXC_THIRD_PARTY
    #:   * TEAMS_WXC_CLIENT
    #:   * WXC_DEVICE
    #:   * WXC_SIP_GW
    client_type: Optional[str] = Field(alias='Client type')
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str] = Field(alias='Client version')
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str] = Field(alias='Correlation ID')
    #: A unique identifier for the user's department name.
    department_id: Optional[str] = Field(alias='Department ID')
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = Field(alias='Device MAC')
    #: The keypad digits as dialed by the user, before pre-translations.
    #: This field reports multiple call dial possibilities:
    #:   * Feature access codes (FAC) used for invoking features such as Last Number Redial or a Call Return.
    #:   * An extension that got dialed and a mis-dialed keypad digit from a device/app.
    #:   * When a user must dial an outside access code (for example, 9+) before dialing a number, this access code is
    #:     also reported, as well as the digits dialed thereafter.
    #: Note that when pre-translations have no effect, the dialed digits field contains the same data as the called
    #: number field.
    #: This field is only used for originating (outgoing) Calls and is not available for terminating (incoming) Calls.
    dialed_digits: Optional[str] = Field(alias='Dialed digits')
    #: Whether the call was inbound or outbound. The possible values are:
    #:   * ORIGINATING
    #:   * TERMINATING
    direction: Optional[str]
    #: The length of the call in seconds.
    duration: Optional[int]
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk')
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str] = Field(alias='International country')
    #: The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call. It
    #: can be used for end-to-end tracking of a SIP session in IP-based multimedia communication. Each call consists of
    #: two UUIDs known as Local Session ID and Remote Session ID.
    #:   * The Local SessionID is generated from the Originating user agent.
    local_session_id: Optional[str] = Field(alias='Local SessionID')
    #: Location of the report.
    location: Optional[str]
    #: The device model type the user is using to make or receive the call.
    model: Optional[str]
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str] = Field(alias='Org UUID')
    #: Call redirection reason for the original called number. For example:
    #:   * Unconditional: Call Forward Always (CFA) service, Group night forwarding.
    #:   * NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #:   * Deflection: Indicates that a call was redirected. Possible causes could be auto attendant transfer, transfer
    #:     out of a call-center, user’s app/device redirection, direct VM transfer etc..
    #:   * TimeOfDay: Call scheduled period of automated redirection. CF/selective, group night forwarding.
    #:   * UserBusy: DND enabled or the user willingly declined the call. CF/busy or voicemail/busy.
    #:   * FollowMe: Automated redirection to a personal redirecting service.
    #:   * CallQueue: A call center call to an agent or a user (a member of the call queue).
    #:   * HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #:   * Unavailable: To voicemail, when the user has no app or device.
    #:   * Unrecognized: Unable to determine the reason.
    #:   * Unknown: Call forward by phone with no reason.
    original_reason: Optional[str] = Field(alias='Original reason')
    #: The operating system that the app was running on, if available.
    os_type: Optional[str] = Field(alias='OS type')
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk')
    #: Call Redirection Reason for the redirecting number. For example:
    #:   * Unconditional: Call Forward Always (CFA) service.
    #:   * NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #:   * Deflection: Indicates that a call was redirected. Possible causes could be auto attendant transfer, transfer
    #:     out of a call-center, user’s app/device redirection, direct VM transfer etc..
    #:   * TimeOfDay: Call scheduled period of automated redirection. CF/Selective.
    #:   * UserBusy: DND enabled or user willingly declined the call. CF/busy or Voicemail/busy.
    #:   * FollowMe: Automated redirection to a personal redirecting service.
    #:   * CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #:   * HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #:   * Unavailable: To voicemail, when the user has no app or device.
    #:   * Unrecognized: Unable to determine the reason.
    #:   * Unknown: Call forward by phone with no reason.
    redirect_reason: Optional[str] = Field(alias='Redirect reason')
    #: When the call has been redirected one or more times, this field reports the last redirecting number. Identifies
    #: who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls,
    #: simultaneous rings, etc.
    redirecting_number: Optional[str] = Field(alias='Redirecting number')
    #: Indicates a trigger that led to a change in the call presence. The trigger could be for this particular call or
    #: redirected via a different call. For example:
    #:   * ConsultativeTransfer: While on a call, the call was transferred to another user by announcing it first.
    #:     meaning the person was given a heads up or asked if they're interested in taking the call and then
    #:     transferred.
    #:   * CallForwardSelective: Call Forward as per the defined schedule. Might be based on factors like a specific
    #:     time, specific callers or to a VM. It always takes precedence over Call Forwarding.
    #:   * CallForwardAlways: Calls are unconditionally forwarded to a defined phone number or to VM.
    #:   * CallForwardNoAnswer: The party was not available to take the call.
    #:   * CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #:   * HuntGroup: A hunt group based call to an agent or a user (denotes a member of the hunt group).
    #:   * CallPickup: The user part of a pickup group or pickup attempted by this user against a ringing call for a
    #:     different user or extension.
    #:   * CalllPark: An ongoing call was parked, assigned with a parked number (not the user’s phone number).
    #:   * CallParkRetrieve: Call park retrieval attempt by the user, either for a different extension or against the
    #:     user’s own extension.
    #:   * Deflection: Indicates that a call was redirected. Possible causes include an auto attendant transfer,
    #:     transfer out of a call-center, user’s app/device redirection etc..
    #:   * FaxDeposit: Indicates a FAX was transmitted to the FAX service.
    #:   * PushNotificationRetrieval: Push notification feature usage indication. Means that a push notification was
    #:     sent to wake up the client and get ready to receive a call.
    #:   * BargeIn: Indicates the user barged-in to someone else’s call.
    #:   * VoiceXMLScriptTermination: Route Point feature usage indication.
    #:   * AnywhereLocation: Indicates call origination towards the single number reach location.
    #:   * AnywherePortal: Indicates call origination towards the “user” identified by the single number reach portal.
    #:   * Unrecognized: Unable to determine the reason.
    related_reason: Optional[str] = Field(alias='Related reason')
    #: Indicates which party released the call first. The possible values are:
    #:   * Local: Used when the local user has released the call first.
    #:   * Remote: Used when the far-end party releases the call first.
    #:   * Unknown: Used when the call has partial information or is unable to gather enough information about the
    #:     party who released the call. It could be because of situations like force lock or because of a session audit
    #:     failure.
    releasing_party: Optional[str] = Field(alias='Releasing party')
    #: The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call. It
    #: can be used for end-to-end tracking of a SIP session in IP-based multimedia communication. Each call consists of
    #: two UUIDs known as Local Session ID and Remote Session ID.
    #:   * The Remote SessionID is generated from the Terminating user agent.
    remote_session_id: Optional[str] = Field(alias='Remote SessionID')
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str] = Field(alias='Report ID')
    #: The time this report was created. Time is in UTC.
    report_time: Optional[str] = Field(alias='Report time')
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for
    #: outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex
    #: Calling (dial plan or unknown extension).
    route_group: Optional[str] = Field(alias='Route group')
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str] = Field(alias='Site main number')
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str] = Field(alias='Site timezone')
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str] = Field(alias='Site UUID')
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    start_time: Optional[str] = Field(alias='Start time')
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type will
    #: show MOBILE_NETWORK.
    sub_client_type: Optional[str] = Field(alias='Sub client type')
    #: Transfer related call ID is used as a call identifier of the other call involved in the transfer. You can share
    #: this ID with Cisco TAC to help them pinpoint parties who are involved during a call transfer.
    transfer_related_call_id: Optional[str] = Field(alias='Transfer related call ID')
    #: The user who made or received the call.
    user: Optional[str]
    #: The type of user (user or workspace) that made or received the call. For example:
    #:   * AutomatedAttendantVideo
    #:   * Anchor
    #:   * BroadworksAnywhere
    #:   * VoiceMailRetrieval
    #:   * LocalGateway
    #:   * HuntGroup
    #:   * GroupPaging
    #:   * User
    #:   * VoiceMailGroup
    #:   * CallCenterStandard
    #:   * VoiceXML
    #:   * RoutePoint
    user_type: Optional[str] = Field(alias='User type')
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = Field(alias='User UUID')


class GetDetailedCallHistoryResponse(ApiModel):
    items: Optional[list[CDR]]


class WebexCallingDetailedCallHistoryApi(ApiChild, base=''):
    """
    The base URL for these APIs is analytics.webexapis.com (or analytics-f.webex.com for Government), which does not
    work with the API reference's Try It feature. If you have any questions or need help please contact the Webex
    Developer Support team at devsupport@webex.com.
    To retrieve Detailed Call History information, you must use a token with the spark-admin:calling_cdr_read scope.
    The authenticating user must be a read-only-admin or full-admin of the organization and have the administrator role
    "Webex Calling Detailed Call History API access" enabled.
    Detailed Call History information is available 5 minutes after a call has ended and may be retrieved for up to 48
    hours. For example, if a call ends at 9:46 am, the record for that call can be collected using the API from 9:51
    am, and is available until 9:46 am two days later.
    This API is rate-limited to one call every 5 minutes for a given organization ID.
    Details on the fields returned from this API and their potential values are available at
    https://help.webex.com/en-us/article/nmug598/Reports-for-Your-Cloud-Collaboration-Portfolio. Select the Report
    templates tab, and then in the Webex Calling reports section see Calling Detailed Call History Report.
    """

    def detailed_call_history(self, start_time: str, end_time: str, locations: str = None, **params) -> Generator[CDR, None, None]:
        """
        Provides Webex Calling Detailed Call History data for your organization.
        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect. The API will return all reports that were created between startTime and endTime.
        Response entries may be added as more information is made available for the reports.
        Values in response items may be extended as more capabilities are added to Webex Calling.

        :param start_time: Time of the first report you wish to collect. (Report time is the time the call finished).
            Note: The specified time must be between 5 minutes ago and 48 hours ago, and be formatted as
            YYYY-MM-DDTHH:MM:SS.mmmZ.
        :type start_time: str
        :param end_time: Time of the last report you wish to collect. (Report time is the time the call finished).
            Note: The specified time should be later than startTime but no later than 48 hours, and be formatted as
            YYYY-MM-DDTHH:MM:SS.mmmZ.
        :type end_time: str
        :param locations: Name of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :type locations: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-detailed-call-history/get-detailed-call-history
        """
        params['startTime'] = start_time
        params['endTime'] = end_time
        if locations is not None:
            params['locations'] = locations
        url = self.ep('https://analytics.webexapis.com/v1/cdr_feed')
        return self.session.follow_pagination(url=url, model=CDR, params=params)

class MemberType(ApiModel):
    #: Indicates the associated member is a person.
    people: Optional[str]
    #: Indicates the associated member is a workspace.
    place: Optional[str]


class LineType(ApiModel):
    #: Indicates a Primary line for the member.
    primary: Optional[str]
    #: Indicates a Shared line for the member. Shared line appearance allows users to receive and place calls to and
    #: from another user's extension, using their device.
    shared_call_appearance: Optional[str]


class PutMemberObject(ApiModel):
    #: Person's assigned port number.
    port: Optional[int]
    #: Unique identifier for the member.
    id: Optional[str]
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Whether the user is the owner of the device or not, and points to a primary Line/Port of device.
    primary_owner: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: The preconfigured number for Hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Device line label.
    line_label: Optional[str]


class MemberObject(PutMemberObject):
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will
    #: be supported in a future update.
    phone_number: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Registration Host IP address for the line port.
    host_ip: Optional[str]
    #: Registration Remote IP address for the line port.
    remote_ip: Optional[str]
    #: Indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location1]


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str]
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Phone Number of a person or workspace.
    phone_number: Optional[str]
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType]
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Indicates if member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location1]


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
    #: When this option is selected, a field 'Custom Background URL' needs to be added with the image url. URLs
    #: provided must link directly to an image file and be in HTTP, HTTPS, or filepath format.
    custom_url: Optional[str]


class DisplayNameSelection(ApiModel):
    #: Indicates that devices will display the person's phone number, or if a person doesn't have a phone number, the
    #: location number will be displayed.
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
    #: This will display the person extension, or if a person doesn't have an extension, the person's first name will
    #: be displayed.
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
    #: LED patterns define lighting schemes for the line keys on the MPP devices. Note that this parameter is not
    #: supported on the MPP 8875
    line_key_led_pattern: Optional[LineKeyLEDPattern]
    #: Enable/disable Link Layer Discovery Protocol for local devices.
    lldp_enabled: Optional[bool]
    #: Enable/disable user-level access to the web interface of Multi-Platform Phones.
    mpp_user_web_access_enabled: Optional[bool]
    #: Select up to 10 Multicast Group URLs (each with a unique Listening Port).
    multicast: Optional[list[str]]
    #: Specify the amount of time (in seconds) that a phone can remain off-hook.
    off_hook_timer: Optional[int]
    #: Select the language for your MPP phone. Setting this overrides the default language setting in place for your
    #: provisioned location.
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
    #: Indicates if customization is allowed at a device level. If true, customized at a device level. If false, not
    #: customized; uses customer-level configuration.
    custom_enabled: Optional[bool]


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


class GetDeviceSettingsResponse(UpdateDeviceSettingsBody):
    #: Customer devices setting update status. If true, an update is in progress (no further changes are allowed). If
    #: false, no update in progress (changes are allowed).
    update_in_progress: Optional[bool]
    #: Number of devices that will be updated.
    device_count: Optional[int]
    #: Indicates the last updated time.
    last_update_time: Optional[int]


class WebexCallingDeviceSettingsApi(ApiChild, base='telephony/config/devices/'):
    """
    These APIs manages Webex Calling settings for devices with are of the Webex Calling type.
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    spark-admin:telephony_config_read, as the current set of APIs is
    designed to provide supplemental information for administrators
    utilizing People Webex Calling APIs.
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    spark-admin:telephony_config_write.
    """

    def members(self, device_id: str, org_id: str = None) -> GetDeviceMembersResponse:
        """
        Get the list of all the members of the device including primary and secondary users.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/get-device-members
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/members')
        data = super().get(url=url, params=params)
        return GetDeviceMembersResponse.parse_obj(data)

    def update_members_ondevice(self, device_id: str, org_id: str = None, members: PutMemberObject = None):
        """
        Modify member details on the device.
        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.
        Modifying members on the device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        :param members: If the member's list is missing then all the users are removed except the primary user.
        :type members: PutMemberObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/update-members-on-the-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateMembersOndeviceBody()
        if members is not None:
            body.members = members
        url = self.ep(f'{device_id}/members')
        super().put(url=url, params=params, data=body.json())
        return

    def search_members(self, device_id: str, location_id: str, org_id: str = None, member_name: str = None, phone_number: str = None, extension: str = None, **params) -> Generator[SearchMemberObject, None, None]:
        """
        Search members that can be assigned to the device.
        A device member can be either a person or a workspace. A admin can access the list of member details, modify
        member details and
        search for available members on a device.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Retrieves the list of available members on the device in this organization.
        :type org_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/search-members
        """
        params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{device_id}/availableMembers')
        return self.session.follow_pagination(url=url, model=SearchMemberObject, item_key='members', params=params)

    def apply_changes_forspecific(self, device_id: str, org_id: str = None):
        """
        Issues request to the device to download and apply changes to the configuration.
        Applying changes for a specific device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/apply-changes-for-a-specific-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/actions/applyChanges/invoke')
        super().post(url=url, params=params)
        return

    def settings(self, device_id: str, device_model: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get override settings for a device.
        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/get-device-settings
        """
        params = {}
        params['deviceModel'] = device_model
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def update_settings(self, device_id: str, customizations: CustomizationDeviceLevelObject, custom_enabled: bool, org_id: str = None, device_model: str = None):
        """
        Modify override settings for a device.
        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins can
        also modify the settings. NOTE: DECT devices do not support settings at the device level.
        Updating settings on the device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObject
        :param custom_enabled: Indicates if customization is allowed at a device level. If true, customized at a device
            level. If false, not customized; uses customer-level configuration.
        :type custom_enabled: bool
        :param org_id: Organization in which the device resides..
        :type org_id: str
        :param device_model: Device model name.
        :type device_model: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings/update-device-settings
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
        url = self.ep(f'{device_id}/settings')
        super().put(url=url, params=params, data=body.json())
        return

class WebexCallingDeviceSettingswithDevicesPhase3FeaturesApi(ApiChild, base='telephony/config/devices/'):
    """
    Webex Calling Device Settings support reading and writing of Webex Calling settings for a devices.
    Viewing these read-only device settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these device settings requires a full administrator auth token with a scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change device settings in a customer's organization using the optional
    orgId query parameter.
    """

    def settings(self, device_id: str, org_id: str = None, device_model: str = None) -> GetDeviceSettingsResponse:
        """
        Get override settings for a device.
        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str
        :param device_model: Model type of the device.
        :type device_model: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings-with-devices-phase3-features/get-device-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if device_model is not None:
            params['deviceModel'] = device_model
        url = self.ep(f'{device_id}/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def update_settings(self, device_id: str, customizations: CustomizationDeviceLevelObject, custom_enabled: bool, org_id: str = None, device_model: str = None):
        """
        Modify override settings for a device.
        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins can
        also modify the settings. NOTE: DECT devices do not support settings at the device level.
        Updating settings on the device requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param customizations: Indicates the customization object of the device settings.
        :type customizations: CustomizationDeviceLevelObject
        :param custom_enabled: Indicates if customization is allowed at a device level. If true, customized at a device
            level. If false, not customized; uses customer-level configuration.
        :type custom_enabled: bool
        :param org_id: Organization in which the device resides..
        :type org_id: str
        :param device_model: Device model naeme.
        :type device_model: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings-with-devices-phase3-features/update-device-settings
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
        url = self.ep(f'{device_id}/settings')
        super().put(url=url, params=params, data=body.json())
        return

class GetThirdPartyDeviceResponse(ApiModel):
    #: Manufacturer of the device.
    manufacturer: Optional[str]
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    line_port: Optional[str]
    #: Contains the body of the HTTP response received following the request to the Console API. Not set if the
    #: response has no body.
    outbound_proxy: Optional[str]
    #: Device manager(s).
    managed_by: Optional[str]
    #: SIP authentication user name for the owner of the device.
    sip_user_name: Optional[str]


class UpdateThirdPartyDeviceBody(ApiModel):
    #: Password to be updated.
    sip_password: Optional[str]


class WebexCallingDeviceSettingswithThird-partyDeviceSupportApi(ApiChild, base='telephony/config/devices/'):
    """
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    Viewing these read-only organization settings requires a full administrator auth token with scope of
    spark-admin:telephony_config_read.
    Modifying these organization settings requires a full or user administrator auth token with scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def party_device(self, device_id: str, org_id: str = None) -> GetThirdPartyDeviceResponse:
        """
        Get third party device details.
        Retrieves customer managed and partner managed device details.
        This requires a full administrator auth token with scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: ID of the organization in which the device resides.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings-with-third-party-device-support/get-third-party-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}')
        data = super().get(url=url, params=params)
        return GetThirdPartyDeviceResponse.parse_obj(data)

    def update_party_device(self, device_id: str, sip_password: str, org_id: str = None):
        """
        Modify a device's sipPassword.
        Updating sipPassword on the device requires a full or user administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param sip_password: Password to be updated.
        :type sip_password: str
        :param org_id: ID of the organization in which the device resides.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-device-settings-with-third-party-device-support/update-third-party-device
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateThirdPartyDeviceBody()
        if sip_password is not None:
            body.sip_password = sip_password
        url = self.ep(f'{device_id}')
        super().put(url=url, params=params, data=body.json())
        return

class WebexCalling(ApiModel):
    #: End user phone number.
    phone_number: Optional[str]
    #: End user extension.
    extension: Optional[str]
    #: Calling location ID.
    location_id: Optional[str]


class ListAutoAttendantObject(WebexCalling):
    #: A unique identifier for the auto attendant.
    id: Optional[str]
    #: Unique name for the auto attendant.
    name: Optional[str]
    #: Name of location for auto attendant.
    location_name: Optional[str]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]


class RingPattern(str, Enum):
    normal = 'NORMAL'
    long_long = 'LONG_LONG'
    short_short_long = 'SHORT_SHORT_LONG'
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumbersWithPattern1(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPattern]


class AlternateNumbersObject(AlternateNumbersWithPattern1):
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]


class ExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class MediaType(str, Enum):
    #: WMA File Extension.
    wma = 'WMA'
    #: WAV File Extension.
    wav = 'WAV'
    #: 3GP File Extension.
    three_gp = '3GP'


class AudioFileObject(ApiModel):
    #: Announcement audio file name.
    name: Optional[str]
    #: Announcement audio file media type.
    media_type: Optional[MediaType]


class Greeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'


class Key(str, Enum):
    digit_0 = 'digit_0'
    digit_1 = 'digit_1'
    digit_2 = 'digit_2'
    digit_3 = 'digit_3'
    digit_4 = 'digit_4'
    digit_5 = 'digit_5'
    digit_6 = 'digit_6'
    digit_7 = 'digit_7'
    digit_8 = 'digit_8'
    digit_9 = 'digit_9'
    hash = 'hash'


class Action(str, Enum):
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    name_dialing = 'NAME_DIALING'
    extension_dialing = 'EXTENSION_DIALING'
    repeat_menu = 'REPEAT_MENU'
    exit = 'EXIT'
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    return_to_previous_menu = 'RETURN_TO_PREVIOUS_MENU'


class KeyConfigurationsObject(ApiModel):
    #: Key assigned to specific menu configuration.
    key: Optional[Key]
    #: Action assigned to specific menu key configuration.
    action: Optional[Action]
    #: The description of each menu key.
    description: Optional[str]
    #: Value based on actions.
    value: Optional[str]


class PostHoursMenuObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    greeting: Optional[Greeting]
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: Optional[bool]
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsObject]


class HoursMenuObject(PostHoursMenuObject):
    #: Announcement Audio File details.
    audio_file: Optional[AudioFileObject]


class FaxMessage(ApiModel):
    #: Enable/disable fax messaging.
    enabled: Optional[bool]
    #: Phone number to receive fax messages.
    phone_number: Optional[str]
    #: Extension to receive fax messages.
    extension: Optional[int]


class GetDetailsForCallParkExtensionResponse(ApiModel):
    #: The extension for the call park extension.
    extension: Optional[str]
    #: Unique name for the call park extension.
    name: Optional[str]


class NewNumber(ApiModel):
    #: Enable/disable to play new number announcement.
    enabled: Optional[bool]
    #: Incoming destination phone number to be announced.
    destination: Optional[str]


class GetCallForwardAlwaysSettingObject(NewNumber):
    #: If true, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    send_to_voicemail_enabled: Optional[bool]


class CallForwardRulesObject(Location1):
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use Any private Number in the comma-separated value to indicate rules that match incoming calls from
    #: a private number. Use Any unavailable number in the comma-separated value to match incoming calls from an
    #: unavailable number.
    calls_from: Optional[str]
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str]
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str]
    #: Reflects if rule is enabled.
    enabled: Optional[bool]


class AutoAttendantCallForwardSettingsDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesObject]]


class CallForwardRulesModifyObject(ApiModel):
    #: A unique identifier for the auto attendant call forward selective rule.
    id: Optional[str]
    #: Flag to indicate if always call forwarding selective rule criteria is active. If not set, flag will be set to
    #: false.
    enabled: Optional[bool]


class AutoAttendantCallForwardSettingsModifyDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject]
    #: Rules for selectively forwarding calls. (Rules which are omitted in the list will not be deleted.)
    rules: Optional[list[CallForwardRulesModifyObject]]


class Selection2(str, Enum):
    #: When the rule matches, forward to the destination for the auto attendant.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class CallForwardSelectiveForwardToObject(ApiModel):
    #: Phone number used if selection is FORWARD_TO_SPECIFIED_NUMBER.
    phone_number: Optional[str]
    #: Controls what happens when the rule matches.
    selection: Optional[Selection2]


class Selection3(str, Enum):
    #: Rule matches for calls from any number.
    any = 'ANY'
    #: Rule matches based on the numbers and options in customNumbers.
    custom = 'CUSTOM'


class CallForwardSelectiveCallsFromCustomNumbersObject(ApiModel):
    #: Match if caller ID indicates the call is from a private number.
    private_number_enabled: Optional[bool]
    #: Match if callerID is unavailable.
    unavailable_number_enabled: Optional[bool]
    #: Array of number strings to be matched against incoming caller ID.
    numbers: Optional[list[str]]


class CallForwardSelectiveCallsFromObject(ApiModel):
    #: If CUSTOM, use customNumbers to specify which incoming caller ID values cause this rule to match. ANY means any
    #: incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[Selection3]
    #: Custom rules for matching incoming caller ID information. Mandatory if the selection option is set to CUSTOM.
    custom_numbers: Optional[CallForwardSelectiveCallsFromCustomNumbersObject]


class Type5(str, Enum):
    #: Indicates that the given phoneNumber or extension associated with this rule's containing object is a primary
    #: number or extension.
    primary = 'PRIMARY'
    #: Indicates that the given phoneNumber or extension associated with this rule's containing object is an alternate
    #: number or extension.
    alternate = 'ALTERNATE'


class CallForwardSelectiveCallsToNumbersObject(ApiModel):
    #: AutoCalls To phone number. Either phone number or extension should be present as mandatory.
    phone_number: Optional[str]
    #: Calls To extension. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Calls to type options.
    type: Optional[Type5]


class CallForwardSelectiveCallsToObject(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class CreateSelectiveCallForwardingRuleForAutoAttendantBody(ApiModel):
    #: Unique name for the selective rule in the auto attendant.
    name: Optional[str]
    #: Reflects if rule is enabled.
    enabled: Optional[bool]
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str]
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str]
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject]
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CallForwardSelectiveCallsFromObject]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject]


class ListCallParkObject(Location1):
    #: Name of the location for the call park.
    location_name: Optional[str]
    #: ID of the location for the call park.
    location_id: Optional[str]


class Option(str, Enum):
    #: Alert parking user only.
    alert_parking_user_only = 'ALERT_PARKING_USER_ONLY'
    #: Alert parking user first, then hunt group.
    alert_parking_user_first_then_hunt_group = 'ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP'
    #: Alert hunt group only.
    alert_hunt_group_only = 'ALERT_HUNT_GROUP_ONLY'


class PutRecallHuntGroupObject(ApiModel):
    #: Alternate user which is a hunt group ID for call park recall alternate destination.
    hunt_group_id: Optional[str]
    #: Call park recall options.
    option: Optional[Option]


class CreateCallPickupBody(ApiModel):
    #: Unique name for the call pickup. The maximum length is 80.
    name: Optional[str]
    #: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
    agents: Optional[list[str]]


class GetRecallHuntGroupObject(PutRecallHuntGroupObject):
    #: Unique name for the hunt group.
    hunt_group_name: Optional[str]


class Type8(MemberType):
    #: Indicates that this object is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person or workspace.
    external: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Flag to indicate a primary phone.
    primary: Optional[bool]


class GetPersonPlaceVirtualLineCallParksObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    id: Optional[str]
    #: First name of a person, workspace or virtual line.
    first_name: Optional[str]
    #: Last name of a person, workspace or virtual line.
    last_name: Optional[str]
    #: Display name of a person, workspace or virtual line.
    display_name: Optional[str]
    #: Type of the person, workspace or virtual line.
    type: Optional[Type8]
    #: Email of a person or workspace.
    email: Optional[str]
    #: List of phone numbers of a person, workspace or virtual line.
    numbers: Optional[list[GetUserNumberItemObject]]


class ListCPCallParkExtensionObject(Location1):
    #: The extension for the call park.
    extension: Optional[str]


class CreateCallParkBody(CreateCallPickupBody):
    #: Recall options that are added to the call park.
    recall: Optional[PutRecallHuntGroupObject]


class CallParkSettingsObject(ApiModel):
    #: Ring pattern for when this callpark is called.
    ring_pattern: Optional[RingPattern]
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up within the
    #: set time, then the call will be recalled based on the Call Park Recall setting.
    recall_time: Optional[int]
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call
    #: will revert back to the hunt group (after the person who parked the call is alerted).
    hunt_wait_time: Optional[int]


class ListCallParkExtensionObject(ListCallParkObject):
    #: The extension for the call park extension.
    extension: Optional[str]


class GetPersonPlaceVirtualLineCallPickupObject(ApiModel):
    #: ID of a person, workspace or virtual line.
    id: Optional[str]
    #: First name of a person, workspace or virtual line.
    first_name: Optional[str]
    #: Last name of a person, workspace or virtual line.
    last_name: Optional[str]
    #: Display name of a person, workspace or virtual line.
    display_name: Optional[str]
    #: Type of the person, workspace or virtual line.
    type: Optional[Type8]
    #: Email of a person, workspace or virtual line.
    email: Optional[str]
    #: List of phone numbers of a person, workspace or virtual line.
    phone_number: Optional[list[GetUserNumberItemObject]]


class ListCallQueueObject(ListCallParkExtensionObject):
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]


class HuntRoutingTypeSelection(ApiModel):
    #: Default routing type which directly uses the routing policy to dispatch calls to the agents.
    priority_based: Optional[str]
    #: This option uses skill level as the criteria to route calls to agents. When there is more than one agent with
    #: the same skill level, the selected policy helps dispatch the calls to the agents.
    skill_based: Optional[str]


class HuntPolicySelection(ApiModel):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next
    #: available agent. This is supported for SKILL_BASED.
    circular: Optional[str]
    #: Send the call through the queue of agents in order, starting from the top each time. This is supported for
    #: SKILL_BASED.
    regular: Optional[str]
    #: Sends calls to all agents at once
    simultaneous: Optional[str]
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has
    #: been idle the second longest, and so on until the call is answered. This is supported for SKILL_BASED.
    uniform: Optional[str]
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100%).
    weighted: Optional[str]


class CallBounce(ApiModel):
    #: If enabled, bounce calls after the set number of rings.
    call_bounce_enabled: Optional[bool]
    #: Number of rings after which to bounce call, if callBounce is enabled.
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


class DistinctiveRing(ApiModel):
    #: Whether or not the distinctiveRing is enabled.
    enabled: Optional[bool]
    #: Ring pattern for when this call queue is called. Only available when distinctiveRing is enabled for the call
    #: queue.
    ring_pattern: Optional[RingPattern]


class PostCallQueueCallPolicyObject(ApiModel):
    #: Call routing type to use to dispatch calls to agents. The routing type should be SKILL_BASED if you want to
    #: assign skill level to agents. Only certain policy are allowed in SKILL_BASED type.
    routing_type: Optional[HuntRoutingTypeSelection]
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: Settings for when the call into the hunt group is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctiveRing option enabled.
    distinctive_ring: Optional[DistinctiveRing]


class Action6(str, Enum):
    #: The caller hears a fast-busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class Overflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[Action6]
    #: When true, forwards all calls to a voicemail service of an internal number. This option is ignored when an
    #: external transferNumber is entered.
    send_to_voicemail: Optional[bool]
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str]
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is
    #: triggered.
    overflow_after_wait_enabled: Optional[bool]
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available. The minimum
    #: value 0, The maximum value is 7200 seconds.
    overflow_after_wait_time: Optional[int]
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by
    #: a user.
    play_overflow_greeting_enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement fileName strings to be played as overflow greetings. These files are from the list of
    #: announcement files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is
    #: mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class SendBusyCalls1(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool]
    #: DEFAULT indicates the default greeting will be played. CUSTOM indicates a custom .wav file will be played.
    greeting: Optional[Greeting]


class WelcomeMessage(SendBusyCalls1):
    #: Mandatory entrance message. The default value is false.
    always_enabled: Optional[bool]
    #: Array of announcement fileName strings to be played as welcomeMessage greetings. These files are from the list
    #: of announcement files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is
    #: mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class WaitMode(str, Enum):
    #: Announce the waiting time.
    time = 'TIME'
    #: Announce queue position.
    position = 'POSITION'


class WaitMessage(ApiModel):
    #: If enabled play Wait Message.
    enabled: Optional[bool]
    #: Estimated wait message operating mode. Supported values TIME and POSITION.
    wait_mode: Optional[WaitMode]
    #: The number of minutes for which the estimated wait is played. The minimum time is 10 minutes. The maximum time
    #: is 100 minutes.
    handling_time: Optional[int]
    #: The default number of call handling minutes. The minimum time is 1 minutes, The maximum time is 100 minutes.
    default_handling_time: Optional[int]
    #: The number of the position for which the estimated wait is played. The minimum positions are 10, The maximum
    #: positions are 100.
    queue_position: Optional[int]
    #: Play time / Play position High Volume.
    high_volume_message_enabled: Optional[bool]
    #: The number of estimated waiting times in seconds. The minimum time is 10 seconds. The maximum time is 600
    #: seconds.
    estimated_waiting_time: Optional[int]
    #: Callback options enabled/disabled. Default value is false.
    callback_option_enabled: Optional[bool]
    #: The minimum estimated callback times in minutes. The default value is 30.
    minimum_estimated_callback_time: Optional[int]
    #: The international numbers for callback is enabled/disabled. The default value is false.
    international_callback_enabled: Optional[bool]
    #: Play updated estimated wait message.
    play_updated_estimated_wait_message: Optional[str]


class ComfortMessage(SendBusyCalls1):
    #: The interval in seconds between each repetition of the comfort message played to queued users. The minimum time
    #: is 10 seconds.The maximum time is 600 seconds.
    time_between_messages: Optional[int]
    #: Array of announcement fileName strings to be played as comfortMessage greetings. These files are from the list
    #: of announcement files associated with this call queue. These files are from the list of announcements files
    #: associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is mandatory, and the maximum
    #: is 4.
    audio_files: Optional[list[str]]


class ComfortMessageBypass(SendBusyCalls1):
    #: The interval in seconds between each repetition of the comfort bypass message played to queued users. The
    #: minimum time is 1 seconds. The maximum time is 120 seconds.
    call_waiting_age_threshold: Optional[int]
    #: Array of announcement fileName strings to be played as comfortMessageBypass greetings. These files are from the
    #: list of announcements files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is
    #: mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class NormalSource(SendBusyCalls1):
    #: Array of announcement fileName strings to be played as mohMessage greetings. These files are from the list of
    #: announcement files associated with this call queue. For CUSTOM announcement, a minimum of 1 fileName is
    #: mandatory, and the maximum is 4.
    audio_files: Optional[list[str]]


class MohMessage(ApiModel):
    normal_source: Optional[NormalSource]
    alternate_source: Optional[NormalSource]


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are
    #: triggered.
    queue_size: Optional[int]
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool]
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool]
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[Overflow]
    #: Play a message when callers first reach the queue. For example, “Thank you for calling. An agent will be with
    #: you shortly.” It can be set as mandatory. If the mandatory option is not selected and a caller reaches the call
    #: queue while there is an available agent, the caller will not hear this announcement and is transferred to an
    #: agent. The welcome message feature is enabled by default.
    welcome_message: Optional[WelcomeMessage]
    #: Notify the caller with either their estimated wait time or position in the queue. If this option is enabled, it
    #: plays after the welcome message and before the comfort message. By default, it is not enabled.
    wait_message: Optional[WaitMessage]
    #: Play a message after the welcome message and before hold music. This is typically a CUSTOM announcement that
    #: plays information, such as current promotions or information about products and services.
    comfort_message: Optional[ComfortMessage]
    #: Play a shorter comfort message instead of the usual Comfort or Music On Hold announcement to all the calls that
    #: should be answered quickly. This feature prevents a caller from hearing a short portion of the standard comfort
    #: message that abruptly ends when they are connected to an agent.
    comfort_message_bypass: Optional[ComfortMessageBypass]
    #: Play music after the comforting message in a repetitive loop.
    moh_message: Optional[MohMessage]
    #: Play a message to the agent immediately before the incoming call is connected. The message typically announces
    #: the identity of the call queue from which the call is coming.
    whisper_message: Optional[NormalSource]


class PostPersonPlaceVirtualLineHuntGroupObject(ApiModel):
    #: ID of person, workspace or virtual line.
    id: Optional[str]
    #: Weight of person, workspace or virtual line. Only applied when call policy is WEIGHTED.
    weight: Optional[str]


class PostPersonPlaceVirtualLineCallQueueObject(PostPersonPlaceVirtualLineHuntGroupObject):
    #: Skill level of person, workspace or virtual line. Only applied when call routing type is SKILL_BASED.
    skill_level: Optional[int]


class AlternateNumbersWithPattern(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPattern]


class AlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns
    #: set for the Alternate Numbers.
    distinctive_ring_enabled: Optional[bool]
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]


class GetPersonPlaceVirtualLineCallQueueObject(CallForwardSelectiveCallsToNumbersObject):
    #: ID of person, workspace or virtual line.
    id: Optional[str]
    #: First name of person, workspace or virtual line.
    first_name: Optional[str]
    #: First name of person, workspace or virtual line.
    last_name: Optional[str]
    #: Weight of person, workspace or virtual line. Only applied when call policy is WEIGHTED.
    weight: Optional[str]
    #: Skill level of person, workspace or virtual line. Only applied when the call routingType is SKILL_BASED.
    skill_level: Optional[int]
    #: Indicates the join status of the agent for this queue. The default value while creating call queue is true.
    join_enabled: Optional[bool]


class ModifyPersonPlaceVirtualLineCallQueueObject(PostPersonPlaceVirtualLineCallQueueObject):
    #: Indicates the join status of the agent for this queue. The default value for newly added agents is true.
    join_enabled: Optional[bool]


class GetAnnouncementFileInfo(ApiModel):
    #: Name of greeting file.
    file_name: Optional[str]
    #: Size of greeting file in bytes.
    file_size: Optional[str]


class Always(NewNumber):
    #: If true, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class CallForwardRulesGet(Location1):
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use Any private Number in the comma-separated value to indicate rules that match incoming calls from
    #: a private number. Use Any unavailable number in the comma-separated value to match incoming calls from an
    #: unavailable number.
    call_from: Optional[str]
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str]
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str]
    #: Reflects if rule is enabled.
    enabled: Optional[bool]


class CallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[Always]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesGet]]


class CallForwarding1(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[Always]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesModifyObject]]


class CallsFrom(ApiModel):
    #: If CUSTOM, use customNumbers to specify which incoming caller ID values cause this rule to match. ANY means any
    #: incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[Selection3]
    #: Custom rules for matching incoming caller ID information.
    custom_numbers: Optional[CallForwardSelectiveCallsFromCustomNumbersObject]


class CallsTo(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class CreateSelectiveCallForwardingRuleForCallQueueBody(ApiModel):
    #: Unique name for the selective rule in the hunt group.
    name: Optional[str]
    #: Reflects if rule is enabled.
    enabled: Optional[bool]
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str]
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str]
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject]
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CallsFrom]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallsTo]


class OriginatorType(ApiModel):
    #: User
    user: Optional[str]
    #: Connection between Webex Calling and the premises
    trunk: Optional[str]


class CallSourceType(ApiModel):
    #: Indicates that the call source is a route list.
    route_list: Optional[str]
    #: Indicates that the call source is a dial pattern.
    dial_pattern: Optional[str]
    #: Indicates that the call source extension is unknown.
    unkown_extension: Optional[str]
    #: Indicates that the call source phone number is unknown.
    unkown_number: Optional[str]


class CallSourceInfo(ApiModel):
    #: The type of call source.
    call_source_type: Optional[CallSourceType]
    #: When originatorType is trunk, originatorId is a valid trunk, this trunk belongs to a route group which is
    #: assigned to a route list with the name routeListA and originatorNumber is a number assigned to routeListA.
    #: routeListA is returned here. This element is returned when callSourceType is ROUTE_LIST.
    route_list_name: Optional[str]
    #: Foute list ID.
    route_list_id: Optional[str]
    #: When originatorType is trunk, originatorId is a valid trunk with name trunkA, trunkA belongs to a route group
    #: which is assigned to a route list with name routeListA, trunkA is also assigned to dialPlanA as routing choice,
    #: dialPlanA has dialPattern xxxx assigned. If the originatorNumber matches the dialPattern xxxx, dialPlanA is
    #: returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_plan_name: Optional[str]
    #: When originatorType is trunk, originatorId is a valid trunk with the name trunkA, trunkA belongs to a route
    #: group which is assigned to a route list with the name routeListA, trunkA is also assigned to dialPlanA as
    #: routing choice, dialPlanA has dialPattern xxxx assigned. If the originatorNumber matches the dialPattern xxxx,
    #: dialPattern xxxx is returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_pattern: Optional[str]
    #: Dial plan ID.
    dial_plan_id: Optional[str]


class DestinationType(ApiModel):
    #: Matching destination is a person or workspace with details in the hostedAgent field.
    hosted_agent: Optional[str]
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the hostedFeature
    #: field.
    hosted_feature: Optional[str]
    #: Matching destination routes into a separate PBX with details in the pbxUser field.
    pbx_user: Optional[str]
    #: Matching destination routes into a PSTN phone number with details in the pstnNumber field.
    pstn_number: Optional[str]
    #: Matching destination routes into a virtual extension with details in the virtualExtension field.
    virtual_extension: Optional[str]
    #: Matching destination routes into a virtual extension range with details in the virtualExtensionRange field.
    virtual_extension_range: Optional[str]
    #: Matching destination routes into a route list with details in the routeList field.
    route_list: Optional[str]
    #: Matching destination routes into a feature access code (FAC) with details in the featureAccessCode field.
    fac: Optional[str]
    #: Matching destination routes into an emergency service like Red Sky, with details in the emergency field.
    emergency: Optional[str]
    #: The route is in a repair state with routing choice details in the repair field.
    repair: Optional[str]
    #: Target extension is unknown with routing choice details in the unknownExtension field.
    unknown_extension: Optional[str]
    #: The target phone number is unknown with routing choice details in the unknownNumber field.
    unknown_number: Optional[str]


class HostedAgent(WebexCalling):
    #: Person or workspace's ID.
    id: Optional[str]
    #: Type of agent for call destination.
    type: Optional[MemberType]
    #: Person or workspace's first name.
    first_name: Optional[str]
    #: Person or workspace's last name.
    last_name: Optional[str]
    #: Name of location for a person or workspace.
    location_name: Optional[str]


class ServiceType(ApiModel):
    #: Destination is an auto attendant.
    auto_attendant: Optional[str]
    #: Indicates that this destination is the Office (Broadworks) Anywhere feature.
    broadworks_anywhere: Optional[str]
    #: Indicates that this destination is the Call Center feature.
    call_center: Optional[str]
    #: Indicates that this destination is the Contact Center Link feature.
    contact_center_link: Optional[str]
    #: Indicates that this destination is the Group Paging feature.
    group_paging: Optional[str]
    #: Indicates that this destination is the Hunt Group feature.
    hunt_group: Optional[str]
    #: Indicates that this destination is the Voice Messaging feature.
    voice_messaging: Optional[str]
    #: Indicates that this destination is the Voice Mail Group feature.
    voice_mail_group: Optional[str]


class HostedFeature(ListCallParkExtensionObject):
    #: Service instance type.
    type: Optional[ServiceType]
    #: User or place's phone number.
    phone_number: Optional[str]


class PstnNumber(ApiModel):
    #: Trunk name.
    trunk_name: Optional[str]
    #: Trunk ID.
    trunk_id: Optional[str]
    #: Route group name.
    route_group_name: Optional[str]
    #: Route group ID.
    route_group_id: Optional[str]
    #: Location of the trunk; required if trunkName is returned.
    trunk_location_name: Optional[str]
    #: Location ID of the trunk; required if trunkName is returned.
    trunk_location_id: Optional[str]


class PbxUser(PstnNumber):
    #: Dial plan name that the called string matches.
    dial_plan_name: Optional[str]
    #: Dial plan ID.
    dial_plan_id: Optional[str]
    #: Dial pattern that the called string matches.
    dial_pattern: Optional[str]


class VirtualExtension(PstnNumber):
    #: Virtual extension ID.
    id: Optional[str]
    #: Virtual extension display first name.
    first_name: Optional[str]
    #: Virtual extension display last name.
    last_name: Optional[str]
    #: Virtual extension display name.
    display_name: Optional[str]
    #: Extension that the virtual extension is associated with.
    extension: Optional[str]
    #: Phone number that the virtual extension is associated with.
    phone_number: Optional[str]
    #: Location name if the virtual extension is at the location level, empty if it is at customer level.
    location_name: Optional[str]
    #: Location ID if the virtual extension is at the location level, empty if it is at customer level.
    location_id: Optional[str]


class VirtualExtensionRange(PstnNumber):
    #: Virtual extension range ID.
    id: Optional[str]
    #: Virtual extension range name.
    name: Optional[str]
    #: Prefix that the virtual extension range is associated with (Note: Standard mode must have leading '+' in prefix;
    #: BCD/Enhanced mode can have any valid prefix).
    prefix: Optional[str]
    #: Pattern associated with the virtual extension range.
    pattern: Optional[str]
    #: Location name if the virtual extension range is at the location level, empty if it is at customer level.
    location_name: Optional[str]
    #: Location ID if the virtual extension range is at the location level, empty if it is at customer level.
    location_id: Optional[str]


class RouteList(ListCallParkObject):
    #: Name of the route group the route list is associated with.
    route_group_name: Optional[str]
    #: ID of the route group the route list is associated with.
    route_group_id: Optional[str]


class FeatureAccessCode(ApiModel):
    #: FAC code.
    code: Optional[str]
    #: FAC name.
    name: Optional[str]


class Emergency(PstnNumber):
    #: Indicates if RedSky is in use.
    is_red_sky: Optional[bool]


class Status6(str, Enum):
    #: Indicates that all extensions were validated.
    ok = 'OK'
    #: Indicates that not all extensions were validated.
    errors = 'ERRORS'


class DialPatternStatus(ApiModel):
    #: Invalid pattern
    invalid: Optional[str]
    #: Duplicate pattern
    duplicate: Optional[str]
    #: Duplicate in input
    duplicate_in_list: Optional[str]


class State(DialPatternStatus):
    #: Extension is valid.
    valid = 'VALID'


class ExtensionStatusObject(ApiModel):
    #: Unique extension which will be validated at the location level.
    extension: Optional[str]
    #: State of the extension after it was validated.
    state: Optional[State]
    #: Error code of the state in case extension is not valid.
    error_code: Optional[int]
    #: Message assigned to the error code.
    message: Optional[str]


class NoAnswer(ApiModel):
    #: If enabled, advance to next agent after the nextAgentRings has occurred.
    next_agent_enabled: Optional[bool]
    #: Number of rings before call will be forwarded if unanswered and nextAgentEnabled is true.
    next_agent_rings: Optional[int]
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool]
    #: Number of rings before forwarding calls if forwardEnabled is true.
    number_of_rings: Optional[int]
    #: Destination if forwardEnabled is True.
    destination: Optional[str]
    #: If forwardEnabled is true, enables and disables sending incoming to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class BusinessContinuity(NewNumber):
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if
    #: the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class PostHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: If false, then the option is treated as "Advance when busy": the hunt group won't ring agents when they're on a
    #: call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is advanced
    #: to them, then the call will wait until that hunt group agent isn't busy.
    waiting_enabled: Optional[bool]
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[NoAnswer]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[BusinessContinuity]


class GetPersonPlaceVirtualLineHuntGroupObject(PostPersonPlaceVirtualLineHuntGroupObject):
    #: First name of person, workspace or virtual line.
    first_name: Optional[str]
    #: Last name of person, workspace or virtual line.
    last_name: Optional[str]
    #: Phone number of person, workspace or virtual line.
    phone_number: Optional[str]
    #: Extension of person, workspace or virtual line.
    extension: Optional[str]


class GetSelectiveCallForwardingRuleForCallQueueResponse(CreateSelectiveCallForwardingRuleForCallQueueBody):
    #: Unique ID for the rule.
    id: Optional[str]


class Type19(str, Enum):
    #: Intercept all inbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow all inbound calls.
    allow_all = 'ALLOW_ALL'


class Announcements3(ApiModel):
    #: DEFAULT indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[Greeting]
    #: Information about the new number announcement.
    new_number: Optional[NewNumber]
    #: Information about how call will be handled if zero (0) is pressed.
    zero_transfer: Optional[NewNumber]


class Announcements(Announcements3):
    #: If set to CUSTOM for greeting, filename of previously uploaded file.
    file_name: Optional[str]


class Incoming(ApiModel):
    #: Select inbound call options.
    type: Optional[Type19]
    #: Enable/disable to route voice mail.
    voicemail_enabled: Optional[bool]
    #: Announcements details.
    announcements: Optional[Announcements]


class Type20(str, Enum):
    #: Intercept all outbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow local outbound calls.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class Outgoing(ApiModel):
    #: Outbound call modes
    type: Optional[Type20]
    #: Enable/disable to route all outbound calls to phone number.
    transfer_enabled: Optional[bool]
    #: If enabled, set outgoing destination phone number.
    destination: Optional[str]


class GetLocationInterceptResponse(ApiModel):
    #: Enable/disable location intercept. Enable this feature to override any Location's Call Intercept settings that
    #: person configures.
    enabled: Optional[bool]
    #: Inbound call details.
    incoming: Optional[Incoming]
    #: Outbound Call details
    outgoing: Optional[Outgoing]


class RouteType(ApiModel):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group: Optional[str]
    #: Connection between Webex Calling and the premises.
    trunk: Optional[str]


class RouteIdentity(Location1):
    #: Type associated with the identity.
    type: Optional[RouteType]


class UnknownExtensionRouteIdentity(ApiModel):
    #: ID of the route type.
    id: Optional[str]
    #: Type associated with the identity.
    type: Optional[RouteType]


class CallingLineId(ApiModel):
    #: Group calling line ID name. By default the Org name.
    name: Optional[str]
    #: Directory Number / Main number in E.164 Format.
    phone_number: Optional[str]


class UpdateLocationWebexCallingDetailsBody(ApiModel):
    #: Location's phone announcement language.
    announcement_language: Optional[str]
    #: Location calling line information.
    calling_line_id: Optional[CallingLineId]
    #: Connection details can only be modified to and from local PSTN types of TRUNK and ROUTE_GROUP.
    connection: Optional[UnknownExtensionRouteIdentity]
    #: Denve' (string) - External Caller ID Name value. Unicode characters.
    external_caller_id_name: Optional[str]
    #: Location Identifier.
    p_access_network_info: Optional[str]
    #: Must dial to reach an outside line. Default is None.
    outside_dial_digit: Optional[str]
    #: Must dial a prefix when calling between locations having same extension within same location; should be numeric.
    routing_prefix: Optional[str]
    #: Chargeable number for the line placing the call. When this is set, all calls placed from this location will
    #: include a P-Charge-Info header with the selected number in the SIP INVITE.
    charge_number: Optional[str]


class ListLocationObject(Location1):
    #: Must dial to reach an outside line, default is None.
    outside_dial_digit: Optional[str]
    #: Must dial a prefix when calling between locations having the same extension within the same location.
    routing_prefix: Optional[str]
    #: Location calling line information.
    calling_line_id: Optional[CallingLineId]
    #: True if E911 setup is required.
    e911_setup_required: Optional[bool]


class CallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the
    #: originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before
    #: the number is dialed.
    international = 'INTERNATIONAL'
    #: Controls calls requiring Operator Assistance.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Controls calls to Directory Assistant companies that require a charge to connect the call.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Controls calls that are National.
    national = 'NATIONAL'


class Action9(str, Enum):
    #: Callers at this location can make these types of calls.
    allow = 'ALLOW'
    #: Callers at this location can't make these types of calls.
    block = 'BLOCK'
    #: Callers must enter the authorization code that you set before placing an outgoing call.
    auth_code = 'AUTH_CODE'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number autoTransferNumber1.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number autoTransferNumber2.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number autoTransferNumber3.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermissionObject(ApiModel):
    #: Below are the call type values.
    call_type: Optional[CallType]
    #: Allows to configure settings for each call type.
    action: Optional[Action9]
    #: If enabled, allow the person to transfer or forward internal calls.
    transfer_enabled: Optional[bool]


class GetOutgoingPermissionAutoTransferNumberResponse(ApiModel):
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_1 will be transferred to
    #: this number.
    auto_transfer_number1: Optional[str]
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_2 will be transferred to
    #: this number.
    auto_transfer_number2: Optional[str]
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_3 will be transferred to
    #: this number.
    auto_transfer_number3: Optional[str]


class AccessCodes(ApiModel):
    #: Access code number.
    code: Optional[str]
    #: Access code description.
    description: Optional[str]


class GetPagingGroupAgentObject(CallForwardSelectiveCallsToNumbersObject):
    #: Agents ID.
    id: Optional[str]
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]


class CreatenewPagingGroupBody(GetDetailsForCallParkExtensionResponse):
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is
    #: mandatory.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator
    #: ID.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people, workspace, and virtual lines IDs who can originate pages to this paging group.
    originators: Optional[list[str]]
    #: An array of people, workspaces and virtual lines IDs will add to a paging group as paging call targets.
    targets: Optional[list[str]]


class State1(str, Enum):
    #: Active state.
    active = 'ACTIVE'
    #: Inactive state
    inactive = 'INACTIVE'


class AddPhoneNumbersTolocationBody(ApiModel):
    #: List of phone numbers that need to be added.
    phone_numbers: Optional[list[str]]
    #: State of the phone numbers.
    state: Optional[State1]


class Owner(ApiModel):
    #: ID of the owner to which PSTN Phone number is assigned.
    id: Optional[str]
    #: Type of the PSTN phone number's owner
    type: Optional[str]
    #: First name of the PSTN phone number's owner
    first_name: Optional[str]
    #: Last name of the PSTN phone number's owner
    last_name: Optional[str]


class NumberListGetObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str]
    #: Extension for a PSTN phone number.
    extension: Optional[str]
    #: Phone number's state.
    state: Optional[str]
    #: Type of phone number.
    phone_number_type: Optional[str]
    #: Indicates if the phone number is used as location clid.
    main_number: Optional[bool]
    #: Indicates if a phone number is a toll free number.
    toll_free_number: Optional[bool]
    location: Optional[Location1]
    owner: Optional[Owner]


class JobExecutionStatusObject1(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    id: Optional[int]
    #: Last updated time (in UTC format) post one of the step execution completion.
    last_updated: Optional[str]
    #: Displays status for overall steps that are part of the job.
    status_message: Optional[str]
    #: Exit Code for a job.
    exit_code: Optional[str]
    #: Job creation time in UTC format.
    created_time: Optional[str]
    #: Time lapsed since the job execution started.
    time_elapsed: Optional[str]


class CountObject(ApiModel):
    #: Indicates the total number of phone numbers requested to be moved.
    total_numbers: Optional[int]
    #: Indicates the total number of phone numbers successfully deleted.
    numbers_deleted: Optional[int]
    #: Indicates the total number of phone numbers successfully moved.
    numbers_moved: Optional[int]
    #: Indicates the total number of phone numbers failed.
    numbers_failed: Optional[int]


class StartJobResponse(Location1):
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject1]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: Indicates operation type that was carried out.
    operation_type: Optional[str]
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str]
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str]
    #: Job statistics.
    counts: Optional[CountObject]


class NumberItem(ApiModel):
    #: The source location of the numbers to be moved.
    location_id: Optional[str]
    #: Indicates the numbers to be moved from one location to another location.
    numbers: Optional[list[str]]


class StepExecutionStatusesObject(Location1):
    #: Step execution start time in UTC format.
    start_time: Optional[str]
    #: Step execution end time in UTC format.
    end_time: Optional[str]
    #: Last updated time for a step in UTC format.
    last_updated: Optional[str]
    #: Displays status for a step.
    status_message: Optional[str]
    #: Exit Code for a step.
    exit_code: Optional[str]
    #: Time lapsed since the step execution started.
    time_elapsed: Optional[str]


class JobExecutionStatusObject(JobExecutionStatusObject1):
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]]


class ErrorMessageObject(AccessCodes):
    #: Error messages describing the location id in which the error occurs. For a move operation this is the target
    #: location ID.
    location_id: Optional[str]


class ErrorObject(ApiModel):
    #: HTTP error code.
    key: Optional[str]
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]]


class ItemObject(ApiModel):
    #: Phone number
    item: Optional[str]
    #: Index of error number.
    item_number: Optional[int]
    #: Unique identifier to track the HTTP requests.
    tracking_id: Optional[str]
    error: Optional[ErrorObject]


class NetworkConnectionType(str, Enum):
    #: Use public internet for the location's connection type.
    public_internet = 'PUBLIC_INTERNET'
    #: Use private network connect for the location's connection type.
    private_network = 'PRIVATE_NETWORK'


class Type25(str, Enum):
    #: Business hours schedule type.
    business_hours = 'businessHours'
    #: Holidays schedule type.
    holidays = 'holidays'


class ListScheduleObject(ListCallParkObject):
    #: Type of the schedule.
    type: Optional[Type25]


class RecurWeeklyObject(ApiModel):
    #: Frequency of occurrence in weeks and select the day - Sunday.
    sunday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Monday.
    monday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Tuesday.
    tuesday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Wednesday.
    wednesday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Thursday.
    thursday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Friday.
    friday: Optional[bool]
    #: Frequency of occurrence in weeks and select the day - Saturday.
    saturday: Optional[bool]


class Month(str, Enum):
    january = 'JANUARY'
    february = 'FEBRUARY'
    march = 'MARCH'
    april = 'APRIL'
    may = 'MAY'
    june = 'JUNE'
    july = 'JULY'
    august = 'AUGUST'
    september = 'SEPTEMBER'
    october = 'OCTOBER'
    november = 'NOVEMBER'
    december = 'DECEMBER'


class RecurYearlyByDateObject(ApiModel):
    #: Schedule the event on a specific day of the month.
    day_of_month: Optional[int]
    #: Schedule the event on a specific month of the year.
    month: Optional[Month]


class Day(str, Enum):
    sunday = 'SUNDAY'
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'


class Week(str, Enum):
    first = 'FIRST'
    second = 'SECOND'
    third = 'THIRD'
    fourth = 'FOURTH'
    last = 'LAST'


class RecurYearlyByDayObject(ApiModel):
    #: Schedule the event on a specific day.
    day: Optional[Day]
    #: Schedule the event on a specific week.
    week: Optional[Week]
    #: Schedule the event on a specific month.
    month: Optional[Month]


class RecurrenceObject1(ApiModel):
    #: Flag to indicate if event will recur forever.
    recur_for_ever: Optional[bool]
    #: End date of recurrence.
    recur_end_date: Optional[str]
    #: Weekly recurrence definition.
    recur_weekly: Optional[RecurWeeklyObject]
    #: Recurrence definition yearly by date.
    recur_yearly_by_date: Optional[RecurYearlyByDateObject]
    #: Recurrence definition yearly by day.
    recur_yearly_by_day: Optional[RecurYearlyByDayObject]


class ScheduleEventObject(ApiModel):
    #: Name for the event.
    name: Optional[str]
    #: Start date of event.
    start_date: Optional[str]
    #: End date of event.
    end_date: Optional[str]
    #: Start time of event. Mandatory if the event is not all day.
    start_time: Optional[str]
    #: End time of event. Mandatory if the event is not all day.
    end_time: Optional[str]
    #: An indication of whether given event is an all-day event or not. Mandatory if the startTime and endTime are not
    #: defined.
    all_day_enabled: Optional[bool]
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject1]


class GetScheduleEventObject(ScheduleEventObject):
    #: A unique identifier for the schedule event.
    id: Optional[str]


class ModifyScheduleEventListObject(ScheduleEventObject):
    #: New name for the event.
    new_name: Optional[str]


class ExternalCallerIdNamePolicy(str, Enum):
    #: Shows virtual lines Caller ID name.
    direct_line = 'DIRECT_LINE'
    #: Shows virtual lines location name.
    location = 'LOCATION'
    #: Allow virtual lines first/last name to be configured.
    other = 'OTHER'


class ListVirtualLineObject(ApiModel):
    #: A unique identifier for the virtual line.
    id: Optional[str]
    #: Last name for virtual line.
    last_name: Optional[str]
    #: First name for virtual line.
    first_name: Optional[str]
    #: callerIdLastName for virtual line.
    caller_id_last_name: Optional[str]
    #: callerIdFirstName for virtual line.
    caller_id_first_name: Optional[str]
    #: callerIdNumber for virtual line.
    caller_id_number: Optional[str]
    #: externalCallerIdNamePolicy for the virtual line.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: customExternalCallerIdName for virtual line.
    custom_external_caller_id_name: Optional[str]
    #: Calling details of virtual line.
    number: Optional[GetUserNumberItemObject]
    #: Location details of virtual line.
    location: Optional[Location1]
    #: Number of devices assigned to a virtual line.
    number_of_devices_assigned: Optional[int]
    #: Type of billing plan.
    billing_plan: Optional[str]


class GetVoicemailSettingsResponse(ApiModel):
    #: When enabled, you can set the deletion conditions for expired messages.
    message_expiry_enabled: Optional[bool]
    #: Number of days after which messages expire.
    number_of_days_for_message_expiry: Optional[int]
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When
    #: disabled, all unread voicemail messages will be kept.
    strict_deletion_enabled: Optional[bool]
    #: When enabled, people in the organization can configure the email forwarding of voicemails.
    voice_message_forwarding_enabled: Optional[bool]


class BlockRepeatedDigits(ApiModel):
    #: If enabled, passcode should not contain repeated digits.
    enabled: Optional[bool]
    #: Maximum number of repeaed digits. The minimum value is 1. The maximum value is 6.
    max: Optional[int]


class BlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    enabled: Optional[bool]
    #: Number of ascending digits in sequence. The minimum value is 2. The maximum value is 5.
    number_of_ascending_digits: Optional[int]
    #: Number of descending digits in sequence. The minimum value is 2. The maximum value is 5.
    number_of_descending_digits: Optional[int]


class Length(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    min: Optional[int]
    #: The minimum value is 3. The maximum value is 30.
    max: Optional[int]


class DefaultVoicemailPinRules(ApiModel):
    #: If enabled, the passcode should not contain repeated pattern.
    block_repeated_patterns_enabled: Optional[bool]
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
    block_repeated_digits: Optional[BlockRepeatedDigits]
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    block_contiguous_sequences: Optional[BlockContiguousSequences]
    #: Length of the passcode.
    length: Optional[Length]
    #: If enabled, the default voicemail passcode can be set.
    default_voicemail_pin_enabled: Optional[bool]


class ExpirePasscode(ApiModel):
    #: If enabled, passcode expires after the number of days specified.
    enabled: Optional[bool]
    #: Number of days for password expiry. The minimum value is 15. The maximum value is 180.
    number_of_days: Optional[int]


class BlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    enabled: Optional[bool]
    #: Number of previous passcodes. The minimum value is 1. The maximum value is 10.
    number_of_passcodes: Optional[int]


class Passcode(ApiModel):
    #: New passcode.
    new_passcode: Optional[str]
    #: Confirm new passcode.
    confirm_passcode: Optional[str]


class FailedAttempts(ApiModel):
    #: If enabled, allows specified number of attempts before locking voice portal access.
    enabled: Optional[bool]
    #: Number of failed attempts allowed.
    attempts: Optional[int]


class Greeting29(str, Enum):
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets
    #: the customer know they are still connected.
    system = 'SYSTEM'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class GetMusicOnHoldResponse(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    call_hold_enabled: Optional[bool]
    #: If enabled, music will be played when call is parked.
    call_park_enabled: Optional[bool]
    #: Greeting type for the location.
    greeting: Optional[Greeting29]


class GetVoicemailGroupObject(ListAutoAttendantObject):
    #: If enabled, incoming calls are sent to voicemail.
    enabled: Optional[bool]


class StorageType(str, Enum):
    #: Store messages in internal mailbox.
    internal = 'INTERNAL'
    #: Send messages to the email address provided.
    external = 'EXTERNAL'


class MessageStorage(ApiModel):
    #: Message storage type
    storage_type: Optional[StorageType]
    #: External email to forward the message.
    external_email: Optional[str]


class EmailCopyOfMessage(ApiModel):
    #: Enable/disable to email message copy.
    enabled: Optional[bool]
    #: Email message copy to email address provided.
    email_id: Optional[str]


class DialPattern(ApiModel):
    #: A unique dial pattern.
    dial_pattern: Optional[str]
    #: Action to add or delete a pattern.
    action: Optional[DialPatternAction]


class DialPatternValidate(ApiModel):
    #: Input dial pattern that is being validated.
    dial_pattern: Optional[str]
    #: Validation status.
    pattern_status: Optional[DialPatternStatus]
    #: Failure details.
    message: Optional[str]


class ModifyDialPlanBody(ApiModel):
    #: A unique name for the dial plan.
    name: Optional[str]
    #: ID of route type associated with the dial plan.
    route_id: Optional[str]
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType]


class DialPlan(ModifyDialPlanBody):
    #: Unique identifier for the dial plan.
    id: Optional[str]
    #: Name of route type associated with the dial plan.
    route_name: Optional[str]


class TrunkType(ApiModel):
    #: For Cisco CUBE Local Gateway.
    registering: Optional[str]
    #: For Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller,
    #: Ribbon Session Border Controller.
    certificate_based: Optional[str]


class Trunk(Location1):
    #: Location associated with the trunk.
    location: Optional[Location1]
    #: Trunk in use flag.
    in_use: Optional[bool]
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]


class ModifyTrunkBody(ApiModel):
    #: A unique name for the dial plan.
    name: Optional[str]
    #: A password to use on the trunk.
    password: Optional[str]
    #: Determines the behavior of the From and PAI headers on outbound calls.
    dual_identity_support_enabled: Optional[bool]
    #: Max Concurrent call. Required to create a static certificate-based trunk.
    max_concurrent_calls: Optional[int]


class DeviceStatus(ApiModel):
    #: Device is online
    online: Optional[str]
    #: Device is offline
    offline: Optional[str]
    #: Unknown. Default
    unknown: Optional[str]


class ResponseStatusType(ApiModel):
    #: Error
    error: Optional[str]
    #: Warning
    warning: Optional[str]


class ResponseStatus(ApiModel):
    #: Error Code. 25013 for error retrieving the outbound proxy. 25014 for error retrieving the status
    code: Optional[int]
    #: Status type.
    type: Optional[ResponseStatusType]
    #: Error summary in English.
    summary_english: Optional[str]
    #: Error Details.
    detail: Optional[list[str]]
    #: Error Tracking ID.
    tracking_id: Optional[str]


class ValidateLocalGatewayFQDNAndDomainForTrunkBody(ApiModel):
    #: FQDN or SRV address of the trunk.
    address: Optional[str]
    #: Domain name of the trunk.
    domain: Optional[str]
    #: FQDN port of the trunk.
    port: Optional[int]


class DeviceType(ApiModel):
    #: Device type assosiated with trunk configuration.
    device_type: Optional[str]
    #: Minimum number of concurrent calls. Required for static certificate based trunk.
    min_concurrent_calls: Optional[int]
    #: Maximum number of concurrent calls. Required for static certificate based trunk.
    max_concurrent_calls: Optional[int]


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]
    #: Device types for trunk configuration.
    device_types: Optional[list[DeviceType]]


class RouteGroup(Location1):
    #: Flag to indicate if the route group is used.
    in_use: Optional[bool]


class LocalGateways(Location1):
    #: Location ID to which local gateway belongs.
    location_id: Optional[str]
    #: Prioritizes local gateways based on these numbers; the lowest number gets the highest priority.
    priority: Optional[int]


class CreateRouteGroupForOrganizationBody(ApiModel):
    #: A unique name for the Route Group.
    name: Optional[str]
    #: Local Gateways that are part of this Route Group.
    local_gateways: Optional[list[LocalGateways]]


class RouteGroupUsageRouteListGet(ApiModel):
    #: List of route lists for this route group.
    route_lists: Optional[list[ListCallParkObject]]


class ModifyRouteListBody(ApiModel):
    #: Route List new name.
    name: Optional[str]
    #: New route group ID.
    route_group_id: Optional[str]


class RouteListNumberPatch(ApiModel):
    #: Number to be deleted/added.
    number: Optional[str]
    #: Possible value, ADD or DELETE.
    action: Optional[DialPatternAction]


class NumberStatus(DialPatternStatus):
    unavailable: Optional[str]


class RouteListNumberPatchResponse(ApiModel):
    #: Phone Number whose status is being reported.
    phone_number: Optional[str]
    #: Status of the number. Possible values are INVALID, DUPLICATE, DUPLICATE_IN_LIST, or UNAVAILABLE.
    number_status: Optional[NumberStatus]
    #: Message of the number add status.
    message: Optional[str]


class HolidayScheduleLevel(str, Enum):
    #: Specifies this Schedule is configured across location.
    location = 'LOCATION'
    #: Specifies this Schedule is configured across organization.
    organization = 'ORGANIZATION'


class CallQueueHolidaySchedulesObject(ApiModel):
    #: Name of the schedule configured for a holiday service.
    schedule_name: Optional[str]
    #: Specifies whether the schedule mentioned in scheduleName is org or location specific.
    schedule_level: Optional[HolidayScheduleLevel]


class Action11(str, Enum):
    #: The caller hears a fast-busy tone.
    busy = 'BUSY'
    #: Transfers the call to number specified in transferPhoneNumber.
    transfer = 'TRANSFER'


class Action15(Action11):
    #: Call remains in the queue.
    none = 'NONE'
    #: Calls are handled according to the Night Service configuration. If the Night Service action is set to none, then
    #: this is equivalent to this policy being set to none (that is, calls remain in the queue).
    night_service = 'NIGHT_SERVICE'
    #: Calls are removed from the queue and are provided with ringing until the caller releases the call. The ringback
    #: tone played to the caller is localized according to the country code of the caller.
    ringing = 'RINGING'
    #: Calls are removed from the queue and are provided with an announcement that is played in a loop until the caller
    #: releases the call.
    announcement = 'ANNOUNCEMENT'


class CallQueueAudioFilesObject(ApiModel):
    #: Name of the file.
    file_name: Optional[str]
    #: Media Type of the audio file.
    media_file_type: Optional[MediaType]


class GetDetailsForCallQueueStrandedCallsResponse(ApiModel):
    #: Specifies call processing action type.
    action: Optional[Action15]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[CallQueueAudioFilesObject]]


class AnnouncementMode(str, Enum):
    #: Plays announcement as per audioMessageSelection.
    normal = 'NORMAL'
    #: Plays announcement as per manualAudioMessageSelection.
    manual = 'MANUAL'


class GetDetailsForCallQueueForcedForwardResponse(ApiModel):
    #: Whether or not the call queue forced forward routing policy setting is enabled.
    forced_forward_enabled: Optional[bool]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[CallQueueAudioFilesObject]]


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
    #: Devices manufactured by a third-party that are approved by a Cisco account manager to be enabled for
    #: provisioning in the control hub.
    third_party: Optional[str]


class ManagedByObject(ApiModel):
    #: Devices managed by Cisco.
    cisco: Optional[str]
    #: Devices managed by a customer that are approved by a Cisco account manager to be enabled for provisioning in the
    #: control hub.
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
    #: Enables / disables customizable line label.
    customizable_line_label_enabled: Optional[bool]


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


class State3(str, Enum):
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
    state: Optional[State3]
    #: MAC address validation error code.
    error_code: Optional[int]
    #: Provides a status message about the MAC address.
    message: Optional[str]


class GetManageNumbersJobStatusResponse(Location1):
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
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]]
    #: Indicates the most recent status (STARTING, STARTED, COMPLETED, FAILED) of the job at the time of invocation.
    latest_execution_status: Optional[str]
    #: Indicates the operation type that was carried out.
    operation_type: Optional[str]
    #: Unique location identifier for which the job was run.
    source_location_id: Optional[str]
    #: Unique location identifier for which the numbers have been moved.
    target_location_id: Optional[str]
    #: The location name for which the job was run.
    source_location_name: Optional[str]
    #: The location name for which the numbers have been moved.
    target_location_name: Optional[str]
    #: Job statistics.
    counts: Optional[CountObject]


class ChangeAnnouncementLanguageBody(ApiModel):
    #: Set to true to change announcement language for existing people and workspaces.
    agent_enabled: Optional[bool]
    #: Set to true to change announcement language for existing feature configurations.
    service_enabled: Optional[bool]
    #: Language code.
    announcement_language_code: Optional[str]


class ReadListOfAutoAttendantsResponse(ApiModel):
    #: Array of auto attendants.
    auto_attendants: Optional[list[ListAutoAttendantObject]]


class GetDetailsForAutoAttendantResponse(FaxMessage):
    #: A unique identifier for the auto attendant.
    id: Optional[str]
    #: Unique name for the auto attendant.
    name: Optional[str]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]
    #: First name defined for an auto attendant.
    first_name: Optional[str]
    #: Last name defined for an auto attendant.
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]]
    #: Language for the auto attendant.
    language: Optional[str]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[ExtensionDialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[ExtensionDialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuObject]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuObject]


class CreateAutoAttendantBody(GetDetailsForCallParkExtensionResponse):
    #: Auto attendant phone number. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: First name defined for an auto attendant.
    first_name: Optional[str]
    #: Last name defined for an auto attendant.
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[ExtensionDialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[ExtensionDialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[PostHoursMenuObject]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[PostHoursMenuObject]


class CreateAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant.
    id: Optional[str]


class UpdateAutoAttendantBody(GetDetailsForCallParkExtensionResponse):
    #: Auto attendant phone number. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: First name defined for an auto attendant.
    first_name: Optional[str]
    #: Last name defined for an auto attendant.
    last_name: Optional[str]
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]]
    #: Language code for the auto attendant.
    language_code: Optional[str]
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str]
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str]
    #: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
    extension_dialing: Optional[ExtensionDialing]
    #: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
    name_dialing: Optional[ExtensionDialing]
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str]
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuObject]
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuObject]


class GetCallForwardingSettingsForAutoAttendantResponse(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsDetailsObject]


class UpdateCallForwardingSettingsForAutoAttendantBody(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsModifyDetailsObject]


class CreateSelectiveCallForwardingRuleForAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant call forward selective rule.
    id: Optional[str]


class GetSelectiveCallForwardingRuleForAutoAttendantResponse(CreateSelectiveCallForwardingRuleForAutoAttendantBody):
    #: Unique ID for the rule.
    id: Optional[str]


class UpdateSelectiveCallForwardingRuleForAutoAttendantResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class ReadListOfCallParksResponse(ApiModel):
    #: Array of call parks.
    call_parks: Optional[list[ListCallParkObject]]


class CreateCallParkResponse(ApiModel):
    #: ID of the newly created call park.
    id: Optional[str]


class GetDetailsForCallParkResponse(Location1):
    #: Recall options that are added to call park.
    recall: Optional[GetRecallHuntGroupObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallParksObject]]
    #: Whether or not the calls will be parked on agents as a destination.
    park_on_agents_enabled: Optional[bool]
    #: Array of call park extensions assigned to a call park.
    call_park_extensions: Optional[list[ListCPCallParkExtensionObject]]


class UpdateCallParkResponse(ApiModel):
    #: ID of the target call park.
    id: Optional[str]


class GetAvailableAgentsFromCallParksResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceVirtualLineCallParksObject]]


class GetAvailableRecallHuntGroupsFromCallParksResponse(ApiModel):
    #: Array of available recall hunt groups.
    hunt_groups: Optional[list[Location1]]


class GetCallParkSettingsResponse(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[GetRecallHuntGroupObject]
    #: Setting controlling call park behavior.
    call_park_settings: Optional[CallParkSettingsObject]


class UpdateCallParkSettingsBody(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[PutRecallHuntGroupObject]
    #: Setting controlling call park behavior.
    call_park_settings: Optional[CallParkSettingsObject]


class ReadListOfCallParkExtensionsResponse(ApiModel):
    #: Array of call park extensions.
    call_park_extensions: Optional[list[ListCallParkExtensionObject]]


class CreateCallParkExtensionResponse(ApiModel):
    #: ID of the newly created call park extension.
    id: Optional[str]


class ReadListOfCallPickupsResponse(ApiModel):
    #: Array of call pickups.
    call_pickups: Optional[list[ListCallParkObject]]


class CreateCallPickupResponse(ApiModel):
    #: ID of the newly created call pickup.
    id: Optional[str]


class GetDetailsForCallPickupResponse(Location1):
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]]


class UpdateCallPickupResponse(ApiModel):
    #: ID of the target call pickup.
    id: Optional[str]


class GetAvailableAgentsFromCallPickupsResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceVirtualLineCallPickupObject]]


class ReadListOfCallQueuesResponse(ApiModel):
    #: Array of call queues.
    queues: Optional[list[ListCallQueueObject]]


class CreateCallQueueBody(GetDetailsForCallParkExtensionResponse):
    #: Primary phone number of the call queue. Either a phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to phoneNumber if set, otherwise
    #: defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class CreateCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class GetDetailsForCallQueueResponse(ListCPCallParkExtensionObject):
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]
    #: Language for the call queue.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phoneNumber if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]


class UpdateCallQueueBody(FaxMessage):
    #: Unique name for the call queue.
    name: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phoneNumber if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[ModifyPersonPlaceVirtualLineCallQueueObject]]
    #: Whether or not to allow agents to join or unjoin a queue.
    allow_agent_join_enabled: Optional[bool]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class ReadListOfCallQueueAnnouncementFilesResponse(ApiModel):
    #: Array of announcements for this call queue.
    announcements: Optional[list[GetAnnouncementFileInfo]]


class GetCallForwardingSettingsForCallQueueResponse(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding]


class UpdateCallForwardingSettingsForCallQueueBody(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding1]


class CreateSelectiveCallForwardingRuleForCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class UpdateSelectiveCallForwardingRuleForCallQueueResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class GetCallRecordingSettingsResponse(ApiModel):
    #: Details of the organization.
    organization: Optional[Location1]
    #: Whether or not the call recording is enabled.
    enabled: Optional[bool]
    #: A unique identifier for the vendor.
    vendor_id: Optional[str]
    #: A unique name for the vendor.
    vendor_name: Optional[str]
    #: Url where can be found terms of service for the vendor.
    terms_of_service_url: Optional[str]


class UpdateCallRecordingSettingsBody(ApiModel):
    #: Whether or not the call recording is enabled.
    enabled: Optional[bool]


class GetCallRecordingTermsOfServiceSettingsResponse(ApiModel):
    #: A unique identifier for the vendor.
    vendor_id: Optional[str]
    #: A unique name for the vendor.
    vendor_name: Optional[str]
    #: Whether or not the call recording terms of service are enabled.
    terms_of_service_enabled: Optional[bool]
    #: Url where can be found terms of service for the vendor.
    terms_of_service_url: Optional[str]


class UpdateCallRecordingTermsOfServiceSettingsBody(ApiModel):
    #: Whether or not the call recording terms of service are enabled.
    terms_of_service_enabled: Optional[bool]


class TestCallRoutingBody(ApiModel):
    #: This element is used to identify the originating party. It can be user UUID or trunk UUID.
    originator_id: Optional[str]
    #: USER or TRUNK.
    originator_type: Optional[OriginatorType]
    #: Only used when originatorType is TRUNK. This element could be a phone number or URI.
    originator_number: Optional[str]
    #: This element specifies called party. It can be any dialable string, for example, an ESN number, E.164 number,
    #: hosted user DN, extension, extension with location code, URL, FAC code.
    destination: Optional[str]


class TestCallRoutingResponse(ApiModel):
    #: Only returned when originatorNumber is specified in the request.
    call_source_info: Optional[CallSourceInfo]
    #: Matching destination type for the call.
    destination_type: Optional[DestinationType]
    #: FAC code if destinationType is FAC. The routing address will be returned for all other destination types.
    routing_address: Optional[str]
    #: Outside access code.
    outside_access_code: Optional[str]
    #: true if the call would be rejected.
    is_rejected: Optional[bool]
    #: Returned when destinationType is HOSTED_AGENT.
    hosted_agent: Optional[HostedAgent]
    #: Returned when destinationType is HOSTED_FEATURE.
    hosted_feature: Optional[HostedFeature]
    #: Returned when destinationType is PBX_USER.
    pbx_user: Optional[PbxUser]
    #: Returned when destinationType is PSTN_NUMBER.
    pstn_number: Optional[PstnNumber]
    #: Returned when destinationType is VIRTUAL_EXTENSION.
    virtual_extension: Optional[VirtualExtension]
    #: Returned when destinationType is VIRTUAL_EXTENSION_RANGE.
    virtual_extension_range: Optional[VirtualExtensionRange]
    #: Returned when destinationType is ROUTE_LIST.
    route_list: Optional[RouteList]
    #: Returned when destinationType is FAC.
    feature_access_code: Optional[FeatureAccessCode]
    #: Returned when destinationType is EMERGENCY.
    emergency: Optional[Emergency]
    #: Returned when destinationType is REPAIR.
    repair: Optional[PstnNumber]
    #: Returned when destinationType is UNKNOWN_EXTENSION.
    unknown_extension: Optional[PstnNumber]
    #: Returned when destinationType is UNKNOWN_NUMBER.
    unknown_number: Optional[PstnNumber]


class ValidateListOfExtensionsBody(ApiModel):
    #: Array of Strings of IDs of the Extensions.
    #: Possible values: 12345, 3456
    extensions: Optional[list[str]]


class ValidateExtensionsBody(ApiModel):
    #: Array of extensions that will be validated.
    extensions: Optional[list[str]]


class ValidateExtensionsResponse(ApiModel):
    #: Status of the validated array of extensions
    status: Optional[Status6]
    #: Array of extensions statuses.
    extension_status: Optional[list[ExtensionStatusObject]]


class ReadListOfHuntGroupsResponse(ApiModel):
    #: Array of hunt groups.
    hunt_groups: Optional[list[ListCallQueueObject]]


class CreateHuntGroupBody(FaxMessage):
    #: Unique name for the hunt group.
    name: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceVirtualLineHuntGroupObject]]


class CreateHuntGroupResponse(ApiModel):
    #: ID of the newly created hunt group.
    id: Optional[str]


class GetDetailsForHuntGroupResponse(ListCPCallParkExtensionObject):
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool]
    #: Primary phone number of the hunt group.
    phone_number: Optional[str]
    #: Whether or not the hunt group has the distinctive ring option enabled.
    distinctive_ring: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]
    #: Language for hunt group.
    language: Optional[str]
    #: Language code for hunt group.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to phone number if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceVirtualLineHuntGroupObject]]
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool]


class UpdateHuntGroupBody(VlanObject):
    #: Unique name for the hunt group.
    name: Optional[str]
    #: Primary phone number of the hunt group.
    phone_number: Optional[str]
    #: Primary phone extension of the hunt group.
    extension: Optional[str]
    #: Whether or not the hunt group has the distinctive ring option enabled.
    distinctive_ring: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set,
    #: otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, workspaces and virtual lines that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceVirtualLineHuntGroupObject]]


class GetCallForwardingSettingsForHuntGroupResponse(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding]


class UpdateCallForwardingSettingsForHuntGroupBody(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding1]


class CreateSelectiveCallForwardingRuleForHuntGroupResponse(ApiModel):
    #: ID of the newly created hunt group.
    id: Optional[str]


class UpdateSelectiveCallForwardingRuleForHuntGroupResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class ReadInternalDialingConfigurationForlocationResponse(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: Optional[bool]
    #: The selected route group/trunk as premises calls.
    unknown_extension_route_identity: Optional[RouteIdentity]


class ModifyInternalDialingConfigurationForlocationBody(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: Optional[bool]
    #: Type associated with the identity.
    unknown_extension_route_identity: Optional[UnknownExtensionRouteIdentity]


class GetLocationWebexCallingDetailsResponse(UpdateLocationWebexCallingDetailsBody):
    #: A unique identifier for the location.
    id: Optional[str]
    #: The name of the location.
    name: Optional[str]
    #: Limit on the number of people at the location, Read-Only.
    user_limit: Optional[int]
    #: IP Address, hostname, or domain. Read-Only.
    default_domain: Optional[str]


class EnableLocationForWebexCallingBody(CreateLocationBody):
    #: A unique identifier for the location.
    id: Optional[str]


class EnableLocationForWebexCallingResponse(ApiModel):
    #: A unique identifier for the location.
    id: Optional[str]


class ListLocationsWebexCallingDetailsResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[ListLocationObject]]


class GenerateExamplePasswordForLocationBody(ApiModel):
    #: password settings array.
    #: SIP password setting
    generate: Optional[list[PasswordGenerate]]


class GenerateExamplePasswordForLocationResponse(ApiModel):
    #: Example password.
    example_sip_password: Optional[str]


class GetLocationOutgoingPermissionResponse(ApiModel):
    #: Array of calling permissions.
    calling_permissions: Optional[list[CallingPermissionObject]]


class UpdateLocationOutgoingPermissionBody(ApiModel):
    #: Array specifying the subset of calling permissions to be updated.
    calling_permissions: Optional[list[CallingPermissionObject]]


class GetOutgoingPermissionLocationAccessCodeResponse(ApiModel):
    #: Access code details
    access_codes: Optional[AccessCodes]


class CreateOutgoingPermissionnewAccessCodeForcustomerLocationBody(ApiModel):
    #: Access code details
    access_codes: Optional[AccessCodes]


class DeleteOutgoingPermissionAccessCodeLocationBody(ApiModel):
    #: Array of string to delete access codes. For example, ["1234","2345"]
    delete_codes: Optional[list[str]]


class ReadListOfPagingGroupsResponse(ApiModel):
    #: Array of paging groups.
    location_paging: Optional[list[ListAutoAttendantObject]]


class CreatenewPagingGroupResponse(ApiModel):
    #: ID of the newly created paging group.
    id: Optional[str]


class GetDetailsForPagingGroupResponse(ListCPCallParkExtensionObject):
    #: Whether or not the paging group is enabled.
    enabled: Optional[bool]
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is
    #: mandatory.
    phone_number: Optional[str]
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool]
    #: Paging language. Minimum length is 1. Maximum length is 40.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator
    #: ID.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people, workspaces and virtual lines ID's who may originate pages to this paging group.
    originators: Optional[list[GetPagingGroupAgentObject]]
    #: An array of people, workspaces and virtual lines ID's that are added to paging group as paging call targets.
    targets: Optional[list[GetPagingGroupAgentObject]]


class UpdatePagingGroupBody(CreatenewPagingGroupBody):
    #: Whether or not the paging group is enabled.
    enabled: Optional[bool]


class ActivatePhoneNumbersInlocationBody(ApiModel):
    #: List of phone numbers that need to be added.
    phone_numbers: Optional[list[str]]


class GetPhoneNumbersForOrganizationWithGivenCriteriasResponse(ApiModel):
    #: Array of phone numbers.
    phone_numbers: Optional[NumberListGetObject]


class ListManageNumbersJobsResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[StartJobResponse]]


class InitiateMoveNumberJobsBody(ApiModel):
    #: Indicates the kind of operation to be carried out.
    operation: Optional[str]
    #: The target location within organization where the unassigned numbers will be moved from the source location.
    target_location_id: Optional[str]
    #: Indicates the numbers to be moved from source to target locations.
    number_list: Optional[list[NumberItem]]


class ListManageNumbersJobErrorsResponse(ApiModel):
    items: Optional[list[ItemObject]]


class GetPrivateNetworkConnectResponse(ApiModel):
    #: Network Connection Type for the location.
    network_connection_type: Optional[NetworkConnectionType]


class UpdatePrivateNetworkConnectBody(ApiModel):
    #: Network Connection Type for the location.
    network_connection_type: Optional[NetworkConnectionType]


class ReadListOfRoutingChoicesResponse(ApiModel):
    #: Array of route identities.
    route_identities: Optional[list[RouteIdentity]]


class ReadListOfSchedulesResponse(ApiModel):
    #: Array of schedules.
    schedules: Optional[list[ListScheduleObject]]


class GetDetailsForScheduleResponse(Location1):
    #: Type of the schedule.
    type: Optional[Type25]
    #: List of schedule events.
    events: Optional[list[GetScheduleEventObject]]


class CreateScheduleBody(ApiModel):
    #: Type of the schedule.
    type: Optional[Type25]
    #: Unique name for the schedule.
    name: Optional[str]
    #: List of schedule events.
    events: Optional[list[ScheduleEventObject]]


class CreateScheduleResponse(ApiModel):
    #: ID of the newly created schedule.
    id: Optional[str]


class UpdateScheduleBody(ApiModel):
    #: Unique name for the schedule.
    name: Optional[str]
    #: List of schedule events.
    events: Optional[list[ModifyScheduleEventListObject]]


class UpdateScheduleResponse(ApiModel):
    #: ID of the target schedule.
    id: Optional[str]


class CreateScheduleEventResponse(ApiModel):
    #: ID of the newly created schedule event.
    id: Optional[str]


class UpdateScheduleEventResponse(ApiModel):
    #: ID of the target schedule event.
    id: Optional[str]


class ReadListOfVirtualLinesResponse(ApiModel):
    #: Array of virtual lines.
    virtual_lines: Optional[list[ListVirtualLineObject]]


class GetVoicemailRulesResponse(ApiModel):
    #: Default voicemail passcode requirements.
    default_voicemail_pin_rules: Optional[DefaultVoicemailPinRules]
    #: Settings for passcode expiry.
    expire_passcode: Optional[ExpirePasscode]
    #: Settings for passcode changes.
    change_passcode: Optional[ExpirePasscode]
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[BlockPreviousPasscodes]


class UpdateVoicemailRulesBody(ApiModel):
    #: Set to true to enable the default voicemail passcode.
    default_voicemail_pin_enabled: Optional[bool]
    #: Default voicemail passcode.
    default_voicemail_pin: Optional[str]
    #: Settings for passcode expiry.
    expire_passcode: Optional[ExpirePasscode]
    #: Settings for passcode changes.
    change_passcode: Optional[ExpirePasscode]
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[BlockPreviousPasscodes]


class GetLocationVoicemailResponse(ApiModel):
    #: Set to true to enable voicemail transcription.
    voicemail_transcription_enabled: Optional[bool]


class UpdateLocationVoicemailBody(ApiModel):
    #: Set to true to enable voicemail transcription.
    voicemail_transcription_enabled: Optional[bool]


class GetVoicePortalResponse(ListCPCallParkExtensionObject):
    #: Language for audio announcements.
    language: Optional[str]
    #: Language code for voicemail group audio announcement.
    language_code: Optional[str]
    #: Phone Number of incoming call.
    phone_number: Optional[str]
    #: Caller ID First Name.
    first_name: Optional[str]
    #: Caller ID Last Name.
    last_name: Optional[str]


class UpdateVoicePortalBody(GetDetailsForCallParkExtensionResponse):
    #: Language code for voicemail group audio announcement.
    language_code: Optional[str]
    #: Phone Number of incoming call.
    phone_number: Optional[str]
    #: Caller ID First Name.
    first_name: Optional[str]
    #: Caller ID Last Name.
    last_name: Optional[str]
    #: Voice Portal Admin Passcode.
    passcode: Optional[Passcode]


class GetVoicePortalPasscodeRuleResponse(ApiModel):
    #: Settings for passcode expiry.
    expire_passcode: Optional[ExpirePasscode]
    #: Number of failed attempts allowed.
    failed_attempts: Optional[FailedAttempts]
    #: Settings for previous passcode usage.
    block_previous_passcodes: Optional[BlockPreviousPasscodes]
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or
    #: 408408).
    block_repeated_digits: Optional[object]
    #: Settings for not allowing numerical sequence in passcode (for example, 012345 or 987654).
    block_contiguous_sequences: Optional[object]
    #: Allowed length of the passcode.
    length: Optional[Length]
    #: If enabled, the passcode do not contain repeated pattern.
    block_repeated_patterns_enabled: Optional[bool]
    #: If enabled, the passcode do not allow user phone number or extension.
    block_user_number_enabled: Optional[bool]
    #: If enabled, the passcode do not allow revered phone number or extension.
    block_reversed_user_number_enabled: Optional[bool]
    #: If enabled, the passcode do not allow setting reversed old passcode.
    block_reversed_old_passcode_enabled: Optional[bool]


class ListVoicemailGroupResponse(ApiModel):
    #: Array of VoicemailGroups.
    voicemail_groups: Optional[list[GetVoicemailGroupObject]]


class GetLocationVoicemailGroupResponse(ListCPCallParkExtensionObject):
    #: Voicemail group phone number.
    phone_number: Optional[str]
    #: Voicemail group toll free number.
    toll_free_number: Optional[bool]
    #: Voicemail group caller ID first name.
    first_name: Optional[str]
    #: Voicemail group called ID last name.
    last_name: Optional[str]
    #: Enable/disable voicemail group.
    enabled: Optional[bool]
    #: Language for voicemail group audio announcement.
    language_code: Optional[str]
    #: Set voicemail group greeting type.
    greeting: Optional[Greeting]
    #: Enabled if CUSTOM greeting is previously uploaded.
    greeting_uploaded: Optional[bool]
    #: CUSTOM greeting for previously uploaded.
    greeting_description: Optional[str]
    #: Message storage information
    message_storage: Optional[MessageStorage]
    #: Message notifications
    notifications: Optional[NewNumber]
    #: Fax message receive settings
    fax_message: Optional[FaxMessage]
    #: Transfer message information
    transfer_to_number: Optional[NewNumber]
    #: Message copy information
    email_copy_of_message: Optional[EmailCopyOfMessage]
    #: Enable/disable to forward voice message.
    voice_message_forwarding_enabled: Optional[bool]


class ModifyLocationVoicemailGroupBody(FaxMessage):
    #: Set the name of the voicemail group.
    name: Optional[str]
    #: Set the voicemail group caller ID first name.
    first_name: Optional[str]
    #: Set the voicemail group called ID last name.
    last_name: Optional[str]
    #: Set passcode to access voicemail group when calling.
    passcode: Optional[int]
    #: Language code for the voicemail group audio announcement.
    language_code: Optional[str]
    #: Voicemail group greeting type.
    greeting: Optional[Greeting]
    #: CUSTOM greeting for previously uploaded.
    greeting_description: Optional[str]
    #: Message storage information
    message_storage: Optional[MessageStorage]
    #: Message notifications
    notifications: Optional[NewNumber]
    #: Fax message receive settings
    fax_message: Optional[FaxMessage]
    #: Transfer message information
    transfer_to_number: Optional[NewNumber]
    #: Message copy information
    email_copy_of_message: Optional[EmailCopyOfMessage]


class CreatenewVoicemailGroupForLocationBody(GetDetailsForCallParkExtensionResponse):
    #: Set voicemail group phone number for this particular location.
    phone_number: Optional[str]
    #: Set voicemail group caller ID first name.
    first_name: Optional[str]
    #: Set voicemail group called ID last name.
    last_name: Optional[str]
    #: Set passcode to access voicemail group when calling.
    passcode: Optional[int]
    #: Language code for voicemail group audio announcement.
    language_code: Optional[str]
    #: Message storage information
    message_storage: Optional[MessageStorage]
    #: Message notifications
    notifications: Optional[NewNumber]
    #: Fax message information
    fax_message: Optional[FaxMessage]
    #: Transfer message information
    transfer_to_number: Optional[NewNumber]
    #: Message copy information
    email_copy_of_message: Optional[EmailCopyOfMessage]


class CreatenewVoicemailGroupForLocationResponse(ApiModel):
    #: UUID of the newly created voice mail group.
    id: Optional[str]


class ReadListOfUCManagerProfilesResponse(ApiModel):
    #: Array of manager profiles.
    calling_profiles: Optional[list[Location1]]


class ReadListOfDialPatternsResponse(ApiModel):
    #: Array of dial patterns. An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
    #: optional wildcard characters.
    dial_patterns: Optional[list[str]]


class ModifyDialPatternsBody(ApiModel):
    #: Array of dial patterns to add or delete. Dial Pattern that is not present in the request is not modified.
    dial_patterns: Optional[list[DialPattern]]
    #: Delete all the dial patterns for a dial plan.
    delete_all_dial_patterns: Optional[bool]


class ValidateDialPatternBody(ApiModel):
    #: Array of dial patterns.
    #: Possible values: +5555,7777
    dial_patterns: Optional[list[str]]


class ValidateDialPatternResponse(ApiModel):
    #: Overall validation result status.
    status: Optional[Status6]
    #: Patterns validation result.
    dial_pattern_status: Optional[list[DialPatternValidate]]


class ReadListOfDialPlansResponse(ApiModel):
    #: Array of dial plans.
    dial_plans: Optional[list[DialPlan]]


class CreateDialPlanBody(ModifyDialPlanBody):
    #: An Array of dial patterns.
    #: Possible values: +5555,+5556
    dial_patterns: Optional[list[str]]


class CreateDialPlanResponse(ApiModel):
    #: ID of the newly created dial plan.
    id: Optional[str]


class GetDialPlanResponse(DialPlan):
    #: Customer information.
    customer: Optional[Location1]


class ReadListOfTrunksResponse(ApiModel):
    #: Array of trunks.
    trunks: Optional[list[Trunk]]


class CreateTrunkBody(ModifyTrunkBody):
    #: ID of location associated with the trunk.
    location_id: Optional[str]
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]
    #: Device type assosiated with trunk.
    device_type: Optional[str]
    #: FQDN or SRV address. Required to create a static certificate-based trunk.
    address: Optional[str]
    #: Domain name. Required to create a static certificate based trunk.
    domain: Optional[str]
    #: FQDN port. Required to create a static certificate-based trunk.
    port: Optional[int]


class CreateTrunkResponse(ApiModel):
    #: ID of the newly created trunk.
    id: Optional[str]


class GetTrunkResponse(ValidateLocalGatewayFQDNAndDomainForTrunkBody):
    #: A unique name for the trunk.
    name: Optional[str]
    #: Customer associated with the trunk.
    customer: Optional[Location1]
    #: Location associated with the trunk.
    location: Optional[Location1]
    #: Unique Outgoing and Destination trunk group associated with the dial plan.
    otg_dtg_id: Optional[str]
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    line_port: Optional[str]
    #: Locations using trunk.
    locations_using_trunk: Optional[list[Location1]]
    #: User ID.
    pilot_user_id: Optional[str]
    #: Contains the body of the HTTP response received following the request to Console API and will not be set if the
    #: response has no body.
    outbound_proxy: Optional[object]
    #: User's authentication service information.
    sip_authentication_user_name: Optional[str]
    #: Device status.
    status: Optional[DeviceStatus]
    #: Error codes.
    error_codes: Optional[list[str]]
    #: Present partial error/warning status information included when the http response is 206.
    response_status: Optional[ResponseStatus]
    #: Determines the behavior of the From and PAI headers on outbound calls.
    dual_identity_support_enabled: Optional[bool]
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]
    #: Device type assosiated with trunk.
    device_type: Optional[str]
    #: Max Concurrent call. Required to create a static certificate based trunk.
    max_concurrent_calls: Optional[int]


class ReadListOfTrunkTypesResponse(ApiModel):
    #: Trunk type with device types.
    trunk_types: Optional[list[TrunkTypeWithDeviceType]]


class ReadListOfRoutingGroupsResponse(ApiModel):
    #: Array of route groups.
    route_groups: Optional[list[RouteGroup]]


class CreateRouteGroupForOrganizationResponse(ApiModel):
    #: ID of the Route Group.
    id: Optional[str]


class ReadRouteGroupForOrganizationResponse(CreateRouteGroupForOrganizationBody):
    #: Organization details.
    organization: Optional[Location1]


class ReadUsageOfRoutingGroupResponse(ApiModel):
    #: Number of PSTN connection locations associated to this route group.
    pstn_connection_count: Optional[str]
    #: Number of call to extension locations associated to this route group.
    call_to_extension_count: Optional[str]
    #: Number of dial plan locations associated to this route group.
    dial_plan_count: Optional[str]
    #: Number of route list locations associated to this route group.
    route_list_count: Optional[str]


class ReadCallToExtensionLocationsOfRoutingGroupResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[Location1]]


class ReadDialPlanLocationsOfRoutingGroupResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[Location1]]


class ReadPSTNConnectionLocationsOfRoutingGroupResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[Location1]]


class ReadRouteListsOfRoutingGroupResponse(ApiModel):
    #: Array of route lists.
    route_group_usage_route_list_get: Optional[list[RouteGroupUsageRouteListGet]]


class ReadListOfRouteListsResponse(ApiModel):
    #: Array of route lists.
    route_lists: Optional[list[RouteList]]


class CreateRouteListBody(ModifyRouteListBody):
    #: Location associated with the Route List.
    location_id: Optional[str]


class CreateRouteListResponse(ApiModel):
    #: ID of the newly route list created.
    id: Optional[str]


class GetRouteListResponse(ApiModel):
    #: Route list name.
    name: Optional[str]
    #: Location associated with the Route List.
    location: Optional[Location1]
    #: Route group associated with the Route list.
    route_group: Optional[RouteGroup]


class ModifyNumbersForRouteListBody(ApiModel):
    #: Array of the numbers to be deleted/added.
    numbers: Optional[list[RouteListNumberPatch]]
    #: If present, the numbers array is ignored and all numbers in the route list are deleted.
    delete_all_numbers: Optional[bool]


class ModifyNumbersForRouteListResponse(ApiModel):
    #: Array of number statuses.
    number_status: Optional[list[RouteListNumberPatchResponse]]


class GetNumbersAssignedToRouteListResponse(ApiModel):
    #: Number assigned to the Route list.
    phone_numbers: Optional[str]


class GetLocalGatewayCallToOnPremisesExtensionUsageForTrunkResponse(ApiModel):
    #: Location associated with the trunk.
    location: Optional[Location1]


class GetLocalGatewayDialPlanUsageForTrunkResponse(ApiModel):
    #: Array of dial Plans.
    dial_plans: Optional[list[Location1]]


class GetLocationsUsingLocalGatewayAsPSTNConnectionRoutingResponse(ApiModel):
    #: Location associated with the trunk.
    location: Optional[Location1]


class GetRouteGroupsUsingLocalGatewayResponse(ApiModel):
    #: Array of route Groups.
    route_group: Optional[list[RouteGroup]]


class GetLocalGatewayUsageCountResponse(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    pstn_connection_count: Optional[int]
    #: The count where the given local gateway is used as call to extension setting.
    call_to_extension_count: Optional[int]
    #: The count where the given local gateway is used by the dial plan.
    dial_plan_count: Optional[int]
    #: The count where the given local gateway is used by the route group.
    route_group_count: Optional[int]


class GetDetailsForCallQueueHolidayServiceResponse(GetDetailsForCallQueueStrandedCallsResponse):
    #: Whether or not the call queue holiday service routing policy is enabled.
    holiday_service_enabled: Optional[bool]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from
    #: holidaySchedules list)
    holiday_schedule_level: Optional[HolidayScheduleLevel]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Lists the pre-configured holiday schedules.
    holiday_schedules: Optional[list[CallQueueHolidaySchedulesObject]]


class UpdateCallQueueHolidayServiceBody(GetDetailsForCallQueueStrandedCallsResponse):
    #: Enable or Disable the call queue holiday service routing policy.
    holiday_service_enabled: Optional[bool]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from
    #: holidaySchedules list)
    holiday_schedule_level: Optional[HolidayScheduleLevel]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]


class GetDetailsForCallQueueNightServiceResponse(GetDetailsForCallQueueStrandedCallsResponse):
    #: Whether or not the call queue night service routing policy is enabled.
    night_service_enabled: Optional[bool]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules
    #: list).
    business_hours_level: Optional[HolidayScheduleLevel]
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: Optional[list[CallQueueHolidaySchedulesObject]]
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of Audio Files.
    manual_audio_files: Optional[list[CallQueueAudioFilesObject]]


class UpdateCallQueueNightServiceBody(GetDetailsForCallQueueStrandedCallsResponse):
    #: Enable or disable call queue night service routing policy.
    night_service_enabled: Optional[bool]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules
    #: list)
    business_hours_level: Optional[HolidayScheduleLevel]
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of pre-configured Audio Files.
    manual_audio_files: Optional[list[CallQueueAudioFilesObject]]


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
    #: Indicates if all the devices within this location will be customized with new requested customizations(if set to
    #: true) or will be overridden with the one at organization level (if set to false or any other value). This field
    #: has no effect when the job is being triggered at organization level.
    location_customizations_enabled: Optional[bool]
    #: Indicates the settings for ATA devices, DECT devices and MPP devices.
    customizations: Optional[CustomizationObject]


class ListChangeDeviceSettingsJobsResponse(ApiModel):
    #: Lists all jobs for the customer in order of most recent one to oldest one irrespective of its status.
    items: Optional[list[StartJobResponse]]


class ListChangeDeviceSettingsJobErrorsResponse(ApiModel):
    items: Optional[list[ItemObject]]


class ReadListOfAnnouncementLanguagesResponse(ApiModel):
    #: Array of Languages.
    languages: Optional[list[FeatureAccessCode]]


class CreateReceptionistContactDirectoryBody(ApiModel):
    #: Receptionist Contact Directory name.
    name: Optional[str]
    #: Array of users assigned to this Receptionist Contact Directory.
    #: Person ID.
    contacts: Optional[list[PersonId]]


class CreateReceptionistContactDirectoryResponse(ApiModel):
    #: Receptionist Contact Directory ID.
    id: Optional[str]


class ReadListOfReceptionistContactDirectoriesResponse(ApiModel):
    #: Array of Receptionist Contact Directories.
    directories: Optional[list[Location1]]


class WebexCallingOrganizationSettingsApi(ApiChild, base='telephony/config/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for
    administrators utilizing People Webex Calling APIs.
    Modifying these organization settings requires a full administrator auth token with a scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query
    parameter.
    """

    def change_announcement_language(self, location_id: str, announcement_language_code: str, org_id: str = None, agent_enabled: bool = None, service_enabled: bool = None):
        """
        Change announcement language for the given location.
        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.
        Changing announcement language for the given location requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param announcement_language_code: Language code.
        :type announcement_language_code: str
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/change-announcement-language
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ChangeAnnouncementLanguageBody()
        if announcement_language_code is not None:
            body.announcement_language_code = announcement_language_code
        if agent_enabled is not None:
            body.agent_enabled = agent_enabled
        if service_enabled is not None:
            body.service_enabled = service_enabled
        url = self.ep(f'locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        super().post(url=url, params=params, data=body.json())
        return

    def read_list_of_auto_attendants(self, org_id: str = None, location_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[ListAutoAttendantObject, None, None]:
        """
        List all Auto Attendants for the organization.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-auto-attendants
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('autoAttendants')
        return self.session.follow_pagination(url=url, model=ListAutoAttendantObject, item_key='autoAttendants', params=params)

    def details_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> GetDetailsForAutoAttendantResponse:
        """
        Retrieve an Auto Attendant details.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForAutoAttendantResponse.parse_obj(data)

    def create_auto_attendant(self, location_id: str, business_schedule: str, business_hours_menu: PostHoursMenuObject, after_hours_menu: PostHoursMenuObject, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, first_name: str = None, last_name: str = None, alternate_numbers: AlternateNumbersObject = None, language_code: str = None, holiday_schedule: str = None, extension_dialing: ExtensionDialing = None, name_dialing: ExtensionDialing = None, time_zone: str = None) -> str:
        """
        Create new Auto Attendant for the given location.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Creating an auto attendant requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: PostHoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: PostHoursMenuObject
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Auto attendant phone number. Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: AlternateNumbersObject
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            ENTERPRISE.
        :type extension_dialing: ExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: ExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateAutoAttendantBody()
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if business_hours_menu is not None:
            body.business_hours_menu = business_hours_menu
        if after_hours_menu is not None:
            body.after_hours_menu = after_hours_menu
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if alternate_numbers is not None:
            body.alternate_numbers = alternate_numbers
        if language_code is not None:
            body.language_code = language_code
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if extension_dialing is not None:
            body.extension_dialing = extension_dialing
        if name_dialing is not None:
            body.name_dialing = name_dialing
        if time_zone is not None:
            body.time_zone = time_zone
        url = self.ep(f'locations/{location_id}/autoAttendants')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, first_name: str = None, last_name: str = None, alternate_numbers: AlternateNumbersObject = None, language_code: str = None, business_schedule: str = None, holiday_schedule: str = None, extension_dialing: ExtensionDialing = None, name_dialing: ExtensionDialing = None, time_zone: str = None, business_hours_menu: HoursMenuObject = None, after_hours_menu: HoursMenuObject = None):
        """
        Update the designated Auto Attendant.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Updating an auto attendant requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Update an auto attendant from this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Auto attendant phone number. Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: AlternateNumbersObject
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            ENTERPRISE.
        :type extension_dialing: ExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: ExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateAutoAttendantBody()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if alternate_numbers is not None:
            body.alternate_numbers = alternate_numbers
        if language_code is not None:
            body.language_code = language_code
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if extension_dialing is not None:
            body.extension_dialing = extension_dialing
        if name_dialing is not None:
            body.name_dialing = name_dialing
        if time_zone is not None:
            body.time_zone = time_zone
        if business_hours_menu is not None:
            body.business_hours_menu = business_hours_menu
        if after_hours_menu is not None:
            body.after_hours_menu = after_hours_menu
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def delete_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        Delete the designated Auto Attendant.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.
        Deleting an auto attendant requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().delete(url=url, params=params)
        return

    def forwarding_settings_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendantCallForwardSettingsDetailsObject:
        """
        Retrieve Call Forwarding settings for the designated Auto Attendant including the list of call forwarding
        rules.
        Retrieving call forwarding settings for an auto attendant requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve the call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant forwarding settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-forwarding-settings-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        data = super().get(url=url, params=params)
        return AutoAttendantCallForwardSettingsDetailsObject.parse_obj(data["callForwarding"])

    def update_forwarding_settings_for_auto_attendant(self, location_id: str, auto_attendant_id: str, call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject, org_id: str = None):
        """
        Update Call Forwarding settings for the designated Auto Attendant.
        Updating call forwarding settings for an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject
        :param org_id: Update auto attendant forwarding settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-forwarding-settings-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallForwardingSettingsForAutoAttendantBody()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def create_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, name: str, forward_to: CallForwardSelectiveForwardToObject, calls_from: CallForwardSelectiveCallsFromObject, org_id: str = None, enabled: bool = None, business_schedule: str = None, holiday_schedule: str = None, calls_to: CallForwardSelectiveCallsToObject = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.
        Creating a selective call forwarding rule for an auto attendant requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Create the rule for this auto attendant.
        :type auto_attendant_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param org_id: Create the auto attendant rule for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-selective-call-forwarding-rule-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForAutoAttendantBody()
        if name is not None:
            body.name = name
        if forward_to is not None:
            body.forward_to = forward_to
        if calls_from is not None:
            body.calls_from = calls_from
        if enabled is not None:
            body.enabled = enabled
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if calls_to is not None:
            body.calls_to = calls_to
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForAutoAttendantResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.
        Retrieving a selective call forwarding rule's settings for an auto attendant requires a full or read-only
        administrator
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve auto attendant rule settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-selective-call-forwarding-rule-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForAutoAttendantResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, name: str, forward_to: CallForwardSelectiveForwardToObject, calls_from: CallForwardSelectiveCallsFromObject, org_id: str = None, enabled: bool = None, business_schedule: str = None, holiday_schedule: str = None, calls_to: CallForwardSelectiveCallsToObject = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.
        Updating a selective call forwarding rule's settings for an auto attendant requires a full administrator auth
        token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are updating settings for.
        :type rule_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param org_id: Update auto attendant rule settings for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-selective-call-forwarding-rule-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForAutoAttendantBody()
        if name is not None:
            body.name = name
        if forward_to is not None:
            body.forward_to = forward_to
        if calls_from is not None:
            body.calls_from = calls_from
        if enabled is not None:
            body.enabled = enabled
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if calls_to is not None:
            body.calls_to = calls_to
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.
        Deleting a selective call forwarding rule for an auto attendant requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Delete the rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are deleting.
        :type rule_id: str
        :param org_id: Delete auto attendant rule from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-selective-call-forwarding-rule-for-an-auto-attendant
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_parks(self, location_id: str, org_id: str = None, order: str = None, name: str = None, **params) -> Generator[ListCallParkObject, None, None]:
        """
        List all Call Parks for the organization.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-parks
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'locations/{location_id}/callParks')
        return self.session.follow_pagination(url=url, model=ListCallParkObject, item_key='callParks', params=params)

    def create_park(self, location_id: str, name: str, recall: PutRecallHuntGroupObject, org_id: str = None, agents: List[str] = None) -> str:
        """
        Create new Call Parks for the given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Creating a call park requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to the call park.
        :type recall: PutRecallHuntGroupObject
        :param org_id: Create the call park for this organization.
        :type org_id: str
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-park
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallParkBody()
        if name is not None:
            body.name = name
        if recall is not None:
            body.recall = recall
        if agents is not None:
            body.agents = agents
        url = self.ep(f'locations/{location_id}/callParks')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_park(self, location_id: str, call_park_id: str, org_id: str = None):
        """
        Delete the designated Call Park.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Deleting a call park requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param call_park_id: Delete the call park with the matching ID.
        :type call_park_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-call-park
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        super().delete(url=url, params=params)
        return

    def details_for_park(self, location_id: str, call_park_id: str, org_id: str = None) -> GetDetailsForCallParkResponse:
        """
        Retrieve Call Park details.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving call park details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param call_park_id: Retrieve settings for a call park with the matching ID.
        :type call_park_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-park
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallParkResponse.parse_obj(data)

    def update_park(self, location_id: str, call_park_id: str, name: str, recall: PutRecallHuntGroupObject, org_id: str = None, agents: List[str] = None) -> str:
        """
        Update the designated Call Park.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Updating a call park requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location in which this call park exists.
        :type location_id: str
        :param call_park_id: Update settings for a call park with the matching ID.
        :type call_park_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to the call park.
        :type recall: PutRecallHuntGroupObject
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-park
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallParkBody()
        if name is not None:
            body.name = name
        if recall is not None:
            body.recall = recall
        if agents is not None:
            body.agents = agents
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def available_agents_from_parks(self, location_id: str, org_id: str = None, call_park_name: str = None, name: str = None, phone_number: str = None, order: str = None, **params) -> Generator[GetPersonPlaceVirtualLineCallParksObject, None, None]:
        """
        Retrieve available agents from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving available agents from call parks requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-available-agents-from-call-parks
        """
        if org_id is not None:
            params['orgId'] = org_id
        if call_park_name is not None:
            params['callParkName'] = call_park_name
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableUsers')
        return self.session.follow_pagination(url=url, model=GetPersonPlaceVirtualLineCallParksObject, item_key='agents', params=params)

    def available_recall_hunt_groups_from_parks(self, location_id: str, org_id: str = None, name: str = None, order: str = None, **params) -> Generator[Location1, None, None]:
        """
        Retrieve available recall hunt groups from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort fields:
            lname.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-available-recall-hunt-groups-from-call-parks
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableRecallHuntGroups')
        return self.session.follow_pagination(url=url, model=Location1, item_key='huntGroups', params=params)

    def park_settings(self, location_id: str, org_id: str = None) -> GetCallParkSettingsResponse:
        """
        Retrieve Call Park Settings from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving settings from call parks requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-park-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/settings')
        data = super().get(url=url, params=params)
        return GetCallParkSettingsResponse.parse_obj(data)

    def update_park_settings(self, location_id: str, org_id: str = None, call_park_recall: PutRecallHuntGroupObject = None, call_park_settings: CallParkSettingsObject = None):
        """
        Update Call Park settings for the designated location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Updating call park settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :param call_park_recall: Recall options that are added to call park.
        :type call_park_recall: PutRecallHuntGroupObject
        :param call_park_settings: Setting controlling call park behavior.
        :type call_park_settings: CallParkSettingsObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-park-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallParkSettingsBody()
        if call_park_recall is not None:
            body.call_park_recall = call_park_recall
        if call_park_settings is not None:
            body.call_park_settings = call_park_settings
        url = self.ep(f'locations/{location_id}/callParks/settings')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_park_extensions(self, org_id: str = None, extension: str = None, name: str = None, location_id: str = None, location_name: str = None, order: str = None, **params) -> Generator[ListCallParkExtensionObject, None, None]:
        """
        List all Call Park Extensions for the organization.
        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with the matching extension.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-park-extensions
        """
        if org_id is not None:
            params['orgId'] = org_id
        if extension is not None:
            params['extension'] = extension
        if name is not None:
            params['name'] = name
        if location_id is not None:
            params['locationId'] = location_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep('callParkExtensions')
        return self.session.follow_pagination(url=url, model=ListCallParkExtensionObject, item_key='callParkExtensions', params=params)

    def details_for_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None) -> GetDetailsForCallParkExtensionResponse:
        """
        Retrieve Call Park Extension details.
        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park
        service for holding parked calls.
        Retrieving call park extension details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param call_park_extension_id: Retrieve details for a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Retrieve call park extension details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-park-extension
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallParkExtensionResponse.parse_obj(data)

    def create_park_extension(self, location_id: str, org_id: str = None, extension: str = None, name: str = None) -> str:
        """
        Create new Call Park Extensions for the given location.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Creating a call park extension requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the call park extension for this location.
        :type location_id: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-park-extension
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetDetailsForCallParkExtensionResponse()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        url = self.ep(f'locations/{location_id}/callParkExtensions')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None):
        """
        Delete the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Deleting a call park extension requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call park extension.
        :type location_id: str
        :param call_park_extension_id: Delete the call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Delete the call park extension from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-call-park-extension
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().delete(url=url, params=params)
        return

    def update_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None, extension: str = None, name: str = None):
        """
        Update the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Updating a call park extension requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call park extension exists.
        :type location_id: str
        :param call_park_extension_id: Update a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-park-extension
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetDetailsForCallParkExtensionResponse()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_pickups(self, location_id: str, org_id: str = None, order: str = None, name: str = None, **params) -> Generator[ListCallParkObject, None, None]:
        """
        List all Call Pickups for the organization.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-pickups
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'locations/{location_id}/callPickups')
        return self.session.follow_pagination(url=url, model=ListCallParkObject, item_key='callPickups', params=params)

    def create_pickup(self, location_id: str, name: str, org_id: str = None, agents: List[str] = None) -> str:
        """
        Create new Call Pickups for the given location.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Creating a call pickup requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param org_id: Create the call pickup for this organization.
        :type org_id: str
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-pickup
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallPickupBody()
        if name is not None:
            body.name = name
        if agents is not None:
            body.agents = agents
        url = self.ep(f'locations/{location_id}/callPickups')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None):
        """
        Delete the designated Call Pickup.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Deleting a call pickup requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param call_pickup_id: Delete the call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-call-pickup
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        super().delete(url=url, params=params)
        return

    def details_for_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None) -> GetDetailsForCallPickupResponse:
        """
        Retrieve Call Pickup details.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving call pickup details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param call_pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-pickup
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallPickupResponse.parse_obj(data)

    def update_pickup(self, location_id: str, call_pickup_id: str, name: str, org_id: str = None, agents: List[str] = None) -> str:
        """
        Update the designated Call Pickup.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Updating a call pickup requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param call_pickup_id: Update settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        :param agents: An Array of ID strings of people, workspaces and virtual lines that are added to call pickup.
        :type agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-pickup
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallPickupBody()
        if name is not None:
            body.name = name
        if agents is not None:
            body.agents = agents
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def available_agents_from_pickups(self, location_id: str, org_id: str = None, call_pickup_name: str = None, name: str = None, phone_number: str = None, order: str = None, **params) -> Generator[GetPersonPlaceVirtualLineCallPickupObject, None, None]:
        """
        Retrieve available agents from call pickups for a given location.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving available agents from call pickups requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, extension, number.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-available-agents-from-call-pickups
        """
        if org_id is not None:
            params['orgId'] = org_id
        if call_pickup_name is not None:
            params['callPickupName'] = call_pickup_name
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callPickups/availableUsers')
        return self.session.follow_pagination(url=url, model=GetPersonPlaceVirtualLineCallPickupObject, item_key='agents', params=params)

    def read_list_of_queues(self, org_id: str = None, location_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[ListCallQueueObject, None, None]:
        """
        List all Call Queues for the organization.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List call queues for this organization.
        :type org_id: str
        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param phone_number: Only return call queues with matching primary phone number or extension.
        :type phone_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-queues
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('queues')
        return self.session.follow_pagination(url=url, model=ListCallQueueObject, item_key='queues', params=params)

    def create_queue(self, location_id: str, call_policies: PostCallQueueCallPolicyObject, queue_settings: CallQueueQueueSettingsObject, agents: PostPersonPlaceVirtualLineCallQueueObject, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, allow_agent_join_enabled: bool = None, phone_number_for_outgoing_calls_enabled: bool = None) -> str:
        """
        Create new Call Queues for the given location.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Creating a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: PostPersonPlaceVirtualLineCallQueueObject
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Primary phone number of the call queue. Either a phoneNumber or extension is mandatory.
        :type phone_number: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to
            phoneNumber if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the call queue.
        :type time_zone: str
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them
            to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateCallQueueBody()
        if call_policies is not None:
            body.call_policies = call_policies
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if agents is not None:
            body.agents = agents
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
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
        if phone_number_for_outgoing_calls_enabled is not None:
            body.phone_number_for_outgoing_calls_enabled = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues')
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
        Deleting a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
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
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueResponse.parse_obj(data)

    def update_queue(self, location_id: str, queue_id: str, queue_settings: CallQueueQueueSettingsObject, org_id: str = None, enabled: bool = None, phone_number: str = None, extension: int = None, name: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, alternate_number_settings: AlternateNumberSettings = None, call_policies: PostCallQueueCallPolicyObject = None, allow_call_waiting_for_agents_enabled: bool = None, agents: ModifyPersonPlaceVirtualLineCallQueueObject = None, allow_agent_join_enabled: bool = None, phone_number_for_outgoing_calls_enabled: bool = None):
        """
        Update the designated Call Queue.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Updating a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param enabled: Enable/disable fax messaging.
        :type enabled: bool
        :param phone_number: Phone number to receive fax messages.
        :type phone_number: str
        :param extension: Extension to receive fax messages.
        :type extension: int
        :param name: Unique name for the call queue.
        :type name: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the
            phoneNumber if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param alternate_number_settings: The alternate numbers feature allows you to assign multiple phone numbers or
            extensions to a call queue. Each number will reach the same greeting and each menu will function
            identically to the main number. The alternate numbers option enables you to have up to ten (10) phone
            numbers ring into the call queue.
        :type alternate_number_settings: AlternateNumberSettings
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: ModifyPersonPlaceVirtualLineCallQueueObject
        :param allow_agent_join_enabled: Whether or not to allow agents to join or unjoin a queue.
        :type allow_agent_join_enabled: bool
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them
            to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueBody()
        if queue_settings is not None:
            body.queue_settings = queue_settings
        if enabled is not None:
            body.enabled = enabled
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
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
        if phone_number_for_outgoing_calls_enabled is not None:
            body.phone_number_for_outgoing_calls_enabled = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_queue_announcement_files(self, location_id: str, queue_id: str, org_id: str = None) -> list[GetAnnouncementFileInfo]:
        """
        List file info for all Call Queue announcement files associated with this Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.
        Retrieving this list of files requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve anouncement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-queue-announcement-files
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[GetAnnouncementFileInfo], data["announcements"])

    def delete_queue_announcement_file(self, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """
        Delete an announcement file for the designated Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.
        Deleting an announcement file for a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Delete an announcement for a call queue in this location.
        :type location_id: str
        :param queue_id: Delete an announcement for the call queue with this identifier.
        :type queue_id: str
        :param file_name: 
        :type file_name: str
        :param org_id: Delete call queue announcement from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-call-queue-announcement-file
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements/{file_name}')
        super().delete(url=url, params=params)
        return

    def forwarding_settings_for_queue(self, location_id: str, queue_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated Call Queue including the list of call forwarding rules.
        Retrieving call forwarding settings for a call queue requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve the call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Retrieve call queue forwarding settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-forwarding-settings-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        data = super().get(url=url, params=params)
        return CallForwarding.parse_obj(data["callForwarding"])

    def update_forwarding_settings_for_queue(self, location_id: str, queue_id: str, org_id: str = None, call_forwarding: CallForwarding1 = None):
        """
        Update Call Forwarding settings for the designated Call Queue.
        Updating call forwarding settings for a call queue requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Update call queue forwarding settings from this organization.
        :type org_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: CallForwarding1

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-forwarding-settings-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallForwardingSettingsForCallQueueBody()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def create_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, name: str, calls_from: CallsFrom, calls_to: CallsTo, org_id: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: CallForwardSelectiveForwardToObject = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Creating a selective call forwarding rule for a call queue requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param queue_id: Create the rule for this call queue.
        :type queue_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallsTo
        :param org_id: Create the call queue rule for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-selective-call-forwarding-rule-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForCallQueueBody()
        if name is not None:
            body.name = name
        if calls_from is not None:
            body.calls_from = calls_from
        if calls_to is not None:
            body.calls_to = calls_to
        if enabled is not None:
            body.enabled = enabled
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if forward_to is not None:
            body.forward_to = forward_to
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForCallQueueResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Retrieving a selective call forwarding rule's settings for a call queue requires a full or read-only
        administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which to call queue exists.
        :type location_id: str
        :param queue_id: Retrieve setting for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve call queue rule settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-selective-call-forwarding-rule-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForCallQueueResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, name: str, calls_from: CallsFrom, calls_to: CallsTo, org_id: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: CallForwardSelectiveForwardToObject = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Updating a selective call forwarding rule's settings for a call queue requires a full administrator auth token
        with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update settings for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are updating settings for.
        :type rule_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallsTo
        :param org_id: Update call queue rule settings for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-selective-call-forwarding-rule-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForCallQueueBody()
        if name is not None:
            body.name = name
        if calls_from is not None:
            body.calls_from = calls_from
        if calls_to is not None:
            body.calls_to = calls_to
        if enabled is not None:
            body.enabled = enabled
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if forward_to is not None:
            body.forward_to = forward_to
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Deleting a selective call forwarding rule for a call queue requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Delete the rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are deleting.
        :type rule_id: str
        :param org_id: Delete call queue rule from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-selective-call-forwarding-rule-for-a-call-queue
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url=url, params=params)
        return

    def recording_settings(self, org_id: str = None) -> GetCallRecordingSettingsResponse:
        """
        Retrieve Call Recording settings for the organization.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Retrieving call recording settings requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-recording-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording')
        data = super().get(url=url, params=params)
        return GetCallRecordingSettingsResponse.parse_obj(data)

    def update_recording_settings(self, enabled: bool, org_id: str = None):
        """
        Update Call Recording settings for the organization.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Updating call recording settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: This API is for Cisco partners only.

        :param enabled: Whether or not the call recording is enabled.
        :type enabled: bool
        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-recording-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallRecordingSettingsBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep('callRecording')
        super().put(url=url, params=params, data=body.json())
        return

    def recording_terms_of_service_settings(self, vendor_id: str, org_id: str = None) -> GetCallRecordingTermsOfServiceSettingsResponse:
        """
        Retrieve Call Recording Terms Of Service settings for the organization.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Retrieving call recording terms of service settings requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param vendor_id: Retrieve call recording terms of service details for the given vendor.
        :type vendor_id: str
        :param org_id: Retrieve call recording terms of service details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-recording-terms-of-service-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url=url, params=params)
        return GetCallRecordingTermsOfServiceSettingsResponse.parse_obj(data)

    def update_recording_terms_of_service_settings(self, vendor_id: str, terms_of_service_enabled: bool, org_id: str = None):
        """
        Update Call Recording Terms Of Service settings for the given vendor.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Updating call recording terms of service settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param terms_of_service_enabled: Whether or not the call recording terms of service are enabled.
        :type terms_of_service_enabled: bool
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-recording-terms-of-service-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallRecordingTermsOfServiceSettingsBody()
        if terms_of_service_enabled is not None:
            body.terms_of_service_enabled = terms_of_service_enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url=url, params=params, data=body.json())
        return

    def test_routing(self, originator_id: str, originator_type: OriginatorType, destination: str, org_id: str = None, originator_number: str = None) -> TestCallRoutingResponse:
        """
        Validates that an incoming call can be routed.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Test call routing requires a full or write-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param originator_id: This element is used to identify the originating party. It can be user UUID or trunk
            UUID.
        :type originator_id: str
        :param originator_type: USER or TRUNK.
        :type originator_type: OriginatorType
        :param destination: This element specifies called party. It can be any dialable string, for example, an ESN
            number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: str
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :param originator_number: Only used when originatorType is TRUNK. This element could be a phone number or URI.
        :type originator_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/test-call-routing
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = TestCallRoutingBody()
        if originator_id is not None:
            body.originator_id = originator_id
        if originator_type is not None:
            body.originator_type = originator_type
        if destination is not None:
            body.destination = destination
        if originator_number is not None:
            body.originator_number = originator_number
        url = self.ep('actions/testCallRouting/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return TestCallRoutingResponse.parse_obj(data)

    def validate_list_of_extensions(self, org_id: str = None, extensions: List[str] = None):
        """
        Validate the List of Extensions.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Validate Extension for this organization.
        :type org_id: str
        :param extensions: Array of Strings of IDs of the Extensions. Possible values: 12345, 3456
        :type extensions: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/validate-the-list-of-extensions
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidateListOfExtensionsBody()
        if extensions is not None:
            body.extensions = extensions
        url = self.ep('actions/validateExtensions/invoke')
        super().post(url=url, params=params, data=body.json())
        return

    def validate_extensions(self, location_id: str, extensions: List[str], org_id: str = None) -> ValidateExtensionsResponse:
        """
        Validate extensions for a specific location.
        Validating extensions requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Validate extensions for this location.
        :type location_id: str
        :param extensions: Array of extensions that will be validated.
        :type extensions: List[str]
        :param org_id: Validate extensions for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/validate-extensions
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidateExtensionsBody()
        if extensions is not None:
            body.extensions = extensions
        url = self.ep(f'locations/{location_id}/actions/validateExtensions/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return ValidateExtensionsResponse.parse_obj(data)

    def read_list_of_hunt_groups(self, org_id: str = None, location_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[ListCallQueueObject, None, None]:
        """
        List all calling Hunt Groups for the organization.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :type org_id: str
        :param location_id: Only return hunt groups with matching location ID.
        :type location_id: str
        :param name: Only return hunt groups with the matching name.
        :type name: str
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :type phone_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-hunt-groups
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('huntGroups')
        return self.session.follow_pagination(url=url, model=ListCallQueueObject, item_key='huntGroups', params=params)

    def create_hunt_group(self, location_id: str, name: str, call_policies: PostHuntGroupCallPolicyObject, agents: PostPersonPlaceVirtualLineHuntGroupObject, org_id: str = None, enabled: bool = None, phone_number: str = None, extension: int = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None) -> str:
        """
        Create new Hunt Groups for the given location.
        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.
        Creating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param name: Unique name for the hunt group.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: PostPersonPlaceVirtualLineHuntGroupObject
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :param enabled: Enable/disable fax messaging.
        :type enabled: bool
        :param phone_number: Phone number to receive fax messages.
        :type phone_number: str
        :param extension: Extension to receive fax messages.
        :type extension: int
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateHuntGroupBody()
        if name is not None:
            body.name = name
        if call_policies is not None:
            body.call_policies = call_policies
        if agents is not None:
            body.agents = agents
        if enabled is not None:
            body.enabled = enabled
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
        url = self.ep(f'locations/{location_id}/huntGroups')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None):
        """
        Delete the designated Hunt Group.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.
        Deleting a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param hunt_group_id: Delete the hunt group with the matching ID.
        :type hunt_group_id: str
        :param org_id: Delete the hunt group from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        super().delete(url=url, params=params)
        return

    def details_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None) -> GetDetailsForHuntGroupResponse:
        """
        Retrieve Hunt Group details.
        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.
        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for the hunt group with this identifier.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForHuntGroupResponse.parse_obj(data)

    def update_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None, enabled: bool = None, value: int = None, name: str = None, phone_number: str = None, extension: str = None, distinctive_ring: bool = None, alternate_numbers: AlternateNumbersWithPattern = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, call_policies: PostHuntGroupCallPolicyObject = None, agents: PostPersonPlaceVirtualLineHuntGroupObject = None):
        """
        Update the designated Hunt Group.
        Hunt groups can route incoming calls to a group of people, workspaces or virtual lines. You can even configure
        a pattern to route to a whole group.
        Updating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param hunt_group_id: Update settings for the hunt group with the matching ID.
        :type hunt_group_id: str
        :param org_id: Update hunt group settings from this organization.
        :type org_id: str
        :param enabled: Denotes whether the VLAN object of an ATA is enabled.
        :type enabled: bool
        :param value: The value of the VLAN Object of DECT.
        :type value: int
        :param name: Unique name for the hunt group.
        :type name: str
        :param phone_number: Primary phone number of the hunt group.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group.
        :type extension: str
        :param distinctive_ring: Whether or not the hunt group has the distinctive ring option enabled.
        :type distinctive_ring: bool
        :param alternate_numbers: The alternate numbers feature allows you to assign multiple phone numbers or
            extensions to a hunt group. Each number will reach the same greeting and each menu will function
            identically to the main number. The alternate numbers option enables you to have up to ten (10) phone
            numbers ring into the hunt group.
        :type alternate_numbers: AlternateNumbersWithPattern
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
            number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, workspaces and virtual lines that are eligible to receive calls.
        :type agents: PostPersonPlaceVirtualLineHuntGroupObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateHuntGroupBody()
        if enabled is not None:
            body.enabled = enabled
        if value is not None:
            body.value = value
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if distinctive_ring is not None:
            body.distinctive_ring = distinctive_ring
        if alternate_numbers is not None:
            body.alternate_numbers = alternate_numbers
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if time_zone is not None:
            body.time_zone = time_zone
        if call_policies is not None:
            body.call_policies = call_policies
        if agents is not None:
            body.agents = agents
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def forwarding_settings_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated Hunt Group including the list of call forwarding rules.
        Retrieving call forwarding settings for a hunt group requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Read the call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group forwarding settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-call-forwarding-settings-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        data = super().get(url=url, params=params)
        return CallForwarding.parse_obj(data["callForwarding"])

    def update_forwarding_settings_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None, call_forwarding: CallForwarding1 = None):
        """
        Update Call Forwarding settings for the designated Hunt Group.
        Updating call forwarding settings for a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param org_id: Update hunt group forwarding settings from this organization.
        :type org_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: CallForwarding1

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-call-forwarding-settings-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallForwardingSettingsForHuntGroupBody()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def create_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, name: str, calls_from: CallsFrom, calls_to: CallsTo, org_id: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: CallForwardSelectiveForwardToObject = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Creating a selective call forwarding rule for a hunt group requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Create the rule for this hunt group.
        :type hunt_group_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallsTo
        :param org_id: Create the hunt group rule for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-selective-call-forwarding-rule-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForCallQueueBody()
        if name is not None:
            body.name = name
        if calls_from is not None:
            body.calls_from = calls_from
        if calls_to is not None:
            body.calls_to = calls_to
        if enabled is not None:
            body.enabled = enabled
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if forward_to is not None:
            body.forward_to = forward_to
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForCallQueueResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Retrieving a selective call forwarding rule's settings for a hunt group requires a full or read-only
        administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve hunt group rule settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-selective-call-forwarding-rule-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForCallQueueResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, name: str, calls_from: CallsFrom, calls_to: CallsTo, org_id: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: CallForwardSelectiveForwardToObject = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Updating a selective call forwarding rule's settings for a hunt group requires a full administrator auth token
        with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are updating settings for.
        :type rule_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallsFrom
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallsTo
        :param org_id: Update hunt group rule settings for this organization.
        :type org_id: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-selective-call-forwarding-rule-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateSelectiveCallForwardingRuleForCallQueueBody()
        if name is not None:
            body.name = name
        if calls_from is not None:
            body.calls_from = calls_from
        if calls_to is not None:
            body.calls_to = calls_to
        if enabled is not None:
            body.enabled = enabled
        if holiday_schedule is not None:
            body.holiday_schedule = holiday_schedule
        if business_schedule is not None:
            body.business_schedule = business_schedule
        if forward_to is not None:
            body.forward_to = forward_to
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Deleting a selective call forwarding rule for a hunt group requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Delete the rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are deleting.
        :type rule_id: str
        :param org_id: Delete hunt group rule from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-selective-call-forwarding-rule-for-a-hunt-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url=url, params=params)
        return

    def location_intercept(self, location_id: str, org_id: str = None) -> GetLocationInterceptResponse:
        """
        Retrieve intercept location details for a customer location.
        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either
        routed to a designated number the person chooses, or to the person's voicemail.
        Retrieving intercept location details requires a full, user or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-intercept
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/intercept')
        data = super().get(url=url, params=params)
        return GetLocationInterceptResponse.parse_obj(data)

    def put_location_intercept(self, location_id: str, org_id: str = None, enabled: bool = None, incoming: Incoming = None, outgoing: Outgoing = None):
        """
        Modifies the intercept location details for a customer location.
        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either
        routed to a designated number the user chooses, or to the user's voicemail.
        Modifying the intercept location details requires a full, user administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Modifies the intercept details for this location.
        :type location_id: str
        :param org_id: Modifies the intercept location details for a customer location.
        :type org_id: str
        :param enabled: Enable/disable location intercept. Enable this feature to override any Location's Call
            Intercept settings that person configures.
        :type enabled: bool
        :param incoming: Inbound call details.
        :type incoming: Incoming
        :param outgoing: Outbound Call details
        :type outgoing: Outgoing

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/put-location-intercept
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetLocationInterceptResponse()
        if enabled is not None:
            body.enabled = enabled
        if incoming is not None:
            body.incoming = incoming
        if outgoing is not None:
            body.outgoing = outgoing
        url = self.ep(f'locations/{location_id}/intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def read_internal_dialing_configuration_forlocation(self, location_id: str, org_id: str = None) -> ReadInternalDialingConfigurationForlocationResponse:
        """
        Get current configuration for routing unknown extensions to the Premises as internal calls
        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits
        that match the extension length) to the PBX.
        Retrieving the internal dialing configuration requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id: List route identities for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-internal-dialing-configuration-for-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/internalDialing')
        data = super().get(url=url, params=params)
        return ReadInternalDialingConfigurationForlocationResponse.parse_obj(data)

    def modify_internal_dialing_configuration_forlocation(self, location_id: str, org_id: str = None, enable_unknown_extension_route_policy: bool = None, unknown_extension_route_identity: UnknownExtensionRouteIdentity = None):
        """
        Modify current configuration for routing unknown extensions to the premise as internal calls
        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits
        that match the extension length) to the PBX.
        Editing the internal dialing configuration requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id: List route identities for this organization.
        :type org_id: str
        :param enable_unknown_extension_route_policy: When enabled, calls made by users at the location to an unknown
            extension (between 2-6 digits) are routed to the selected route group/trunk as premises calls.
        :type enable_unknown_extension_route_policy: bool
        :param unknown_extension_route_identity: Type associated with the identity.
        :type unknown_extension_route_identity: UnknownExtensionRouteIdentity

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-the-internal-dialing-configuration-for-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyInternalDialingConfigurationForlocationBody()
        if enable_unknown_extension_route_policy is not None:
            body.enable_unknown_extension_route_policy = enable_unknown_extension_route_policy
        if unknown_extension_route_identity is not None:
            body.unknown_extension_route_identity = unknown_extension_route_identity
        url = self.ep(f'locations/{location_id}/internalDialing')
        super().put(url=url, params=params, data=body.json())
        return

    def location_webexing_details(self, location_id: str, org_id: str = None) -> GetLocationWebexCallingDetailsResponse:
        """
        Shows Webex Calling details for a location, by ID.
        Specifies the location ID in the locationId parameter in the URI.
        Searching and viewing locations in your organization requires an administrator auth token with the
        spark-admin:telephony_config_read scope.

        :param location_id: Retrieve Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Webex Calling location attributes for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-webex-calling-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}')
        data = super().get(url=url, params=params)
        return GetLocationWebexCallingDetailsResponse.parse_obj(data)

    def enable_location_for_webexing(self, announcement_language: str, id: str, org_id: str = None, name: str = None, time_zone: str = None, preferred_language: str = None, address: Address = None) -> str:
        """
        Enable a location by adding it to Webex Calling. This add Webex Calling support to a
        location created created using the POST /v1/locations API.
        Locations are used to support calling features which can be defined at the location level.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param id: A unique identifier for the location.
        :type id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this link
            (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone)
            for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param address: The address of the location.
        :type address: Address

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/enable-a-location-for-webex-calling
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = EnableLocationForWebexCallingBody()
        if announcement_language is not None:
            body.announcement_language = announcement_language
        if id is not None:
            body.id = id
        if name is not None:
            body.name = name
        if time_zone is not None:
            body.time_zone = time_zone
        if preferred_language is not None:
            body.preferred_language = preferred_language
        if address is not None:
            body.address = address
        url = self.ep('locations')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def list_locations_webexing_details(self, org_id: str = None, name: str = None, order: str = None, **params) -> Generator[ListLocationObject, None, None]:
        """
        Lists Webex Calling locations for an organization with Webex Calling details.
        Searching and viewing locations with Webex Calling details in your
        organization require an administrator auth token with the
        spark-admin:telephony_config_read scope.

        :param org_id: List locations for this organization.
        :type org_id: str
        :param name: List locations whose name contains this string.
        :type name: str
        :param order: Sort the list of locations based on name, either asc or desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-locations-webex-calling-details
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('locations')
        return self.session.follow_pagination(url=url, model=ListLocationObject, item_key='locations', params=params)

    def update_location_webexing_details(self, location_id: str, org_id: str = None, announcement_language: str = None, calling_line_id: CallingLineId = None, connection: UnknownExtensionRouteIdentity = None, external_caller_id_name: str = None, p_access_network_info: str = None, outside_dial_digit: str = None, routing_prefix: str = None, charge_number: str = None):
        """
        Update Webex Calling details for a location, by ID.
        Specifies the location ID in the locationId parameter in the URI.
        Modifying the connection via API is only supported for the local PSTN types of TRUNK and ROUTE_GROUP.
        Updating a location in your organization requires an administrator auth token with the
        spark-admin:telephony_config_write scope.

        :param location_id: Updating Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Updating Webex Calling location attributes for this organization.
        :type org_id: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param calling_line_id: Location calling line information.
        :type calling_line_id: CallingLineId
        :param connection: Connection details can only be modified to and from local PSTN types of TRUNK and
            ROUTE_GROUP.
        :type connection: UnknownExtensionRouteIdentity
        :param external_caller_id_name: Denve' (string) - External Caller ID Name value. Unicode characters.
        :type external_caller_id_name: str
        :param p_access_network_info: Location Identifier.
        :type p_access_network_info: str
        :param outside_dial_digit: Must dial to reach an outside line. Default is None.
        :type outside_dial_digit: str
        :param routing_prefix: Must dial a prefix when calling between locations having same extension within same
            location; should be numeric.
        :type routing_prefix: str
        :param charge_number: Chargeable number for the line placing the call. When this is set, all calls placed from
            this location will include a P-Charge-Info header with the selected number in the SIP INVITE.
        :type charge_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-location-webex-calling-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateLocationWebexCallingDetailsBody()
        if announcement_language is not None:
            body.announcement_language = announcement_language
        if calling_line_id is not None:
            body.calling_line_id = calling_line_id
        if connection is not None:
            body.connection = connection
        if external_caller_id_name is not None:
            body.external_caller_id_name = external_caller_id_name
        if p_access_network_info is not None:
            body.p_access_network_info = p_access_network_info
        if outside_dial_digit is not None:
            body.outside_dial_digit = outside_dial_digit
        if routing_prefix is not None:
            body.routing_prefix = routing_prefix
        if charge_number is not None:
            body.charge_number = charge_number
        url = self.ep(f'locations/{location_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def generate_example_password_for_location(self, location_id: str, org_id: str = None, generate: List[PasswordGenerate] = None) -> str:
        """
        Generates an example password using the effective password settings for the location. If you don't specify
        anything in the generate field or don't provide a request body, then you will receive a SIP password by
        default.
        Used while creating a trunk and shouldn't be used anywhere else.
        Generating an example password requires a full or write-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location for which example password has to be generated.
        :type location_id: str
        :param org_id: Organization to which the location belongs.
        :type org_id: str
        :param generate: password settings array. SIP password setting
        :type generate: List[PasswordGenerate]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/generate-example-password-for-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GenerateExamplePasswordForLocationBody()
        if generate is not None:
            body.generate = generate
        url = self.ep(f'locations/{location_id}/actions/generatePassword/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return data["exampleSipPassword"]

    def location_outgoing_permission(self, location_id: str, org_id: str = None) -> list[CallingPermissionObject]:
        """
        Retrieve the location's outgoing call settings.
        A location's outgoing call settings allow you to determine the types of calls the people/workspaces at the
        location are allowed to make, as well as configure the default calling permission for each call type at the
        location.
        Retrieving a location's outgoing call settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve outgoing call settings for this location.
        :type location_id: str
        :param org_id: Retrieve outgoing call settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-outgoing-permission
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/outgoingPermission')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[CallingPermissionObject], data["callingPermissions"])

    def update_location_outgoing_permission(self, location_id: str, org_id: str = None, calling_permissions: CallingPermissionObject = None):
        """
        Update the location's outgoing call settings.
        Location's outgoing call settings allows you to determine the types of calls the people/workspaces at this
        location are allowed to make and configure the default calling permission for each call type at a location.
        Updating a location's outgoing call settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update outgoing call settings for this location.
        :type location_id: str
        :param org_id: Update outgoing call settings for this organization.
        :type org_id: str
        :param calling_permissions: Array specifying the subset of calling permissions to be updated.
        :type calling_permissions: CallingPermissionObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-location-outgoing-permission
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateLocationOutgoingPermissionBody()
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'locations/{location_id}/outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def outgoing_permission_auto_transfer_number(self, location_id: str, org_id: str = None) -> GetOutgoingPermissionAutoTransferNumberResponse:
        """
        Get the transfer numbers for the outbound permission in a location.
        Outbound permissions can specify which transfer number an outbound call should transfer to via the action
        field.
        Retrieving an auto transfer number requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve auto transfer number for this location.
        :type location_id: str
        :param org_id: Retrieve auto transfer number for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-outgoing-permission-auto-transfer-number
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/outgoingPermission/autoTransferNumbers')
        data = super().get(url=url, params=params)
        return GetOutgoingPermissionAutoTransferNumberResponse.parse_obj(data)

    def put_outgoing_permission_auto_transfer_number(self, location_id: str, org_id: str = None, auto_transfer_number1: str = None, auto_transfer_number2: str = None, auto_transfer_number3: str = None):
        """
        Modifies the transfer numbers for the outbound permission in a location.
        Outbound permissions can specify which transfer number an outbound call should transfer to via the action
        field.
        Updating auto transfer number requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Updating auto transfer number for this location.
        :type location_id: str
        :param org_id: Updating auto transfer number for this organization.
        :type org_id: str
        :param auto_transfer_number1: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_1 will be transferred to this number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_2 will be transferred to this number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_3 will be transferred to this number.
        :type auto_transfer_number3: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/put-outgoing-permission-auto-transfer-number
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetOutgoingPermissionAutoTransferNumberResponse()
        if auto_transfer_number1 is not None:
            body.auto_transfer_number1 = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body.auto_transfer_number2 = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body.auto_transfer_number3 = auto_transfer_number3
        url = self.ep(f'locations/{location_id}/outgoingPermission/autoTransferNumbers')
        super().put(url=url, params=params, data=body.json())
        return

    def outgoing_permission_location_access_code(self, location_id: str, org_id: str = None) -> AccessCodes:
        """
        Retrieve access codes details for a customer location.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Retrieving access codes details requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-outgoing-permission-location-access-code
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        data = super().get(url=url, params=params)
        return AccessCodes.parse_obj(data["accessCodes"])

    def create_outgoing_permissionnew_access_code_forcustomer_location(self, location_id: str, org_id: str = None, access_codes: AccessCodes = None):
        """
        Add a new access code for the given location for a customer.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Creating an access code for the given location requires a full or user administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param org_id: Add new access code for this organization.
        :type org_id: str
        :param access_codes: Access code details
        :type access_codes: AccessCodes

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-outgoing-permission-a-new-access-code-for-a-customer-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateOutgoingPermissionnewAccessCodeForcustomerLocationBody()
        if access_codes is not None:
            body.access_codes = access_codes
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        super().post(url=url, params=params, data=body.json())
        return

    def delete_outgoing_permission_access_code_location(self, location_id: str, delete_codes: List[str], org_id: str = None):
        """
        Deletes the access code details for a particular location for a customer.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Modifying the access code location details requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param delete_codes: Array of string to delete access codes. For example, ["1234","2345"]
        :type delete_codes: List[str]
        :param org_id: Deletes the access code details for a customer location.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-outgoing-permission-access-code-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = DeleteOutgoingPermissionAccessCodeLocationBody()
        if delete_codes is not None:
            body.delete_codes = delete_codes
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_paging_groups(self, org_id: str = None, location_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[ListAutoAttendantObject, None, None]:
        """
        List all Paging Groups for the organization.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List paging groups for this organization.
        :type org_id: str
        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-paging-groups
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('paging')
        return self.session.follow_pagination(url=url, model=ListAutoAttendantObject, item_key='locationPaging', params=params)

    def createnew_paging_group(self, location_id: str, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, language_code: str = None, first_name: str = None, last_name: str = None, originator_caller_id_enabled: bool = None, originators: List[str] = None, targets: List[str] = None) -> str:
        """
        Create a new Paging Group for the given location.
        Group Paging allows a one-way call or group page to up to 75 people, workspaces and virtual lines by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.
        Creating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber
            or extension is mandatory.
        :type phone_number: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 30.
        :type first_name: str
        :param last_name: Last name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 30.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller ID when a group page is
            performed. If true shows page originator ID.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people, workspace, and virtual lines IDs who can originate pages to this paging
            group.
        :type originators: List[str]
        :param targets: An array of people, workspaces and virtual lines IDs will add to a paging group as paging call
            targets.
        :type targets: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-new-paging-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreatenewPagingGroupBody()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if originator_caller_id_enabled is not None:
            body.originator_caller_id_enabled = originator_caller_id_enabled
        if originators is not None:
            body.originators = originators
        if targets is not None:
            body.targets = targets
        url = self.ep(f'locations/{location_id}/paging')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_paging_group(self, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete the designated Paging Group.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.
        Deleting a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :type paging_id: str
        :param org_id: Delete the paging group from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-paging-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        super().delete(url=url, params=params)
        return

    def details_for_paging_group(self, location_id: str, paging_id: str, org_id: str = None) -> GetDetailsForPagingGroupResponse:
        """
        Retrieve Paging Group details.
        Group Paging allows a person, place or virtual line a one-way call or group page to up to 75 people and/or
        workspaces and/or virtual line by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.
        Retrieving paging group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Retrieve paging group settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-paging-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForPagingGroupResponse.parse_obj(data)

    def update_paging_group(self, location_id: str, paging_id: str, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, language_code: str = None, first_name: str = None, last_name: str = None, originator_caller_id_enabled: bool = None, originators: List[str] = None, targets: List[str] = None, enabled: bool = None):
        """
        Update the designated Paging Group.
        Group Paging allows a person to place a one-way call or group page to up to 75 people, workspaces and virtual
        lines by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.
        Updating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber
            or extension is mandatory.
        :type phone_number: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 30.
        :type first_name: str
        :param last_name: Last name that displays when a group page is performed. Minimum length is 1. Maximum length
            is 30.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller ID when a group page is
            performed. If true shows page originator ID.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people, workspace, and virtual lines IDs who can originate pages to this paging
            group.
        :type originators: List[str]
        :param targets: An array of people, workspaces and virtual lines IDs will add to a paging group as paging call
            targets.
        :type targets: List[str]
        :param enabled: Whether or not the paging group is enabled.
        :type enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-paging-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdatePagingGroupBody()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if language_code is not None:
            body.language_code = language_code
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if originator_caller_id_enabled is not None:
            body.originator_caller_id_enabled = originator_caller_id_enabled
        if originators is not None:
            body.originators = originators
        if targets is not None:
            body.targets = targets
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def add_phone_numbers_tolocation(self, location_id: str, phone_numbers: List[str], state: State1, org_id: str = None):
        """
        Adds a specified set of phone numbers to a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.
        Adding a phone number to a location requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        :param state: State of the phone numbers.
        :type state: State1
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/add-phone-numbers-to-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AddPhoneNumbersTolocationBody()
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if state is not None:
            body.state = state
        url = self.ep(f'locations/{location_id}/numbers')
        super().post(url=url, params=params, data=body.json())
        return

    def activate_phone_numbers_inlocation(self, location_id: str, phone_numbers: List[str], org_id: str = None):
        """
        Activate the specified set of phone numbers in a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.
        Activating a phone number in a location requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/activate-phone-numbers-in-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ActivatePhoneNumbersInlocationBody()
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        url = self.ep(f'locations/{location_id}/numbers')
        super().put(url=url, params=params, data=body.json())
        return

    def remove_phone_numbers_fromlocation(self, location_id: str, phone_numbers: List[str], state: State1, org_id: str = None):
        """
        Remove the specified set of phone numbers from a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.
        Removing a phone number from a location requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        :param state: State of the phone numbers.
        :type state: State1
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/remove-phone-numbers-from-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AddPhoneNumbersTolocationBody()
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if state is not None:
            body.state = state
        url = self.ep(f'locations/{location_id}/numbers')
        super().delete(url=url, params=params, data=body.json())
        return

    def phone_numbers_for_organization_with_given_criterias(self, org_id: str = None, location_id: str = None, max: int = None, start: int = None, phone_number: str = None, available: bool = None, order: str = None, owner_name: str = None, owner_id: str = None, owner_type: enum = None, extension: str = None, number_type: str = None, phone_number_type: str = None, state: str = None, details: bool = None, toll_free_numbers: bool = None, restricted_non_geo_numbers: bool = None) -> NumberListGetObject:
        """
        List all the phone numbers for the given organization along with the status and owner (if any).
        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List numbers for this organization.
        :type org_id: str
        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param max: Limit the number of phone numbers returned to this maximum count. Default is 2000.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching phone numbers. Default is 0.
        :type start: int
        :param phone_number: Search for this phoneNumber.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with ownerType
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will be
            based on number and extension in an ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given ownerName. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given ownerType. Possible input values
        :type owner_type: enum
        :param extension: Returns the list of PSTN phone numbers with the given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers. This
            parameter cannot be used along with available or state.
        :type number_type: str
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: str
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: str
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-phone-numbers-for-an-organization-with-given-criterias
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if available is not None:
            params['available'] = str(available).lower()
        if order is not None:
            params['order'] = order
        if owner_name is not None:
            params['ownerName'] = owner_name
        if owner_id is not None:
            params['ownerId'] = owner_id
        if owner_type is not None:
            params['ownerType'] = owner_type
        if extension is not None:
            params['extension'] = extension
        if number_type is not None:
            params['numberType'] = number_type
        if phone_number_type is not None:
            params['phoneNumberType'] = phone_number_type
        if state is not None:
            params['state'] = state
        if details is not None:
            params['details'] = str(details).lower()
        if toll_free_numbers is not None:
            params['tollFreeNumbers'] = str(toll_free_numbers).lower()
        if restricted_non_geo_numbers is not None:
            params['restrictedNonGeoNumbers'] = str(restricted_non_geo_numbers).lower()
        url = self.ep('numbers')
        data = super().get(url=url, params=params)
        return NumberListGetObject.parse_obj(data["phoneNumbers"])

    def list_manage_numbers_jobs(self, org_id: str = None, **params) -> Generator[StartJobResponse, None, None]:
        """
        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one irrespective
        of its status.
        The public API only supports initiating jobs which move numbers between locations.
        Via Control Hub they can initiate both the move and delete, so this listing can show both.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-manage-numbers-jobs
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/numbers/manageNumbers')
        return self.session.follow_pagination(url=url, model=StartJobResponse, params=params)

    def initiate_move_number_jobs(self, operation: str, target_location_id: str, number_list: NumberItem) -> StartJobResponse:
        """
        Starts the numbers move from one location to another location. Although jobs can do both MOVE and DELETE
        actions internally, only MOVE is supported publicly.
        In order to move a number,
        For example, you can move from Cisco PSTN to Cisco PSTN, but you cannot move from Cisco PSTN to a location with
        Cloud Connected PSTN.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param operation: Indicates the kind of operation to be carried out.
        :type operation: str
        :param target_location_id: The target location within organization where the unassigned numbers will be moved
            from the source location.
        :type target_location_id: str
        :param number_list: Indicates the numbers to be moved from source to target locations.
        :type number_list: NumberItem

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/initiate-move-number-jobs
        """
        body = InitiateMoveNumberJobsBody()
        if operation is not None:
            body.operation = operation
        if target_location_id is not None:
            body.target_location_id = target_location_id
        if number_list is not None:
            body.number_list = number_list
        url = self.ep('jobs/numbers/manageNumbers')
        data = super().post(url=url, data=body.json())
        return StartJobResponse.parse_obj(data)

    def manage_numbers_job_status(self, job_id: str = None) -> GetManageNumbersJobStatusResponse:
        """
        Returns the status and other details of the job.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-manage-numbers-job-status
        """
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}')
        data = super().get(url=url)
        return GetManageNumbersJobStatusResponse.parse_obj(data)

    def pause_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Pause the running Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Pause the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Pause the Manage Numbers job for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/pause-the-manage-numbers-job
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke')
        super().post(url=url, params=params)
        return

    def resume_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Resume the paused Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Resume the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Resume the Manage Numbers job for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/resume-the-manage-numbers-job
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke')
        super().post(url=url, params=params)
        return

    def abandon_manage_numbers_job(self, job_id: str = None, org_id: str = None):
        """
        Abandon the Manage Numbers Job.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Abandon the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Abandon the Manage Numbers job for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/abandon-the-manage-numbers-job
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke')
        super().post(url=url, params=params)
        return

    def list_manage_numbers_job_errors(self, job_id: str = None, org_id: str = None, **params) -> Generator[ItemObject, None, None]:
        """
        Lists all error details of Manage Numbers job. This will not list any errors if exitCode is COMPLETED. If the
        status is COMPLETED_WITH_ERRORS then this lists the cause of failures.
        List of possible Errors:
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve the error details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-manage-numbers-job-errors
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/numbers/manageNumbers/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, params=params)

    def private_network_connect(self, location_id: str, org_id: str = None) -> NetworkConnectionType:
        """
        Retrieve the location's network connection type.
        Network Connection Type determines if the location's network connection is public or private.
        Retrieving a location's network connection type requires a full, user or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve the network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve the network connection type for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-private-network-connect
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        data = super().get(url=url, params=params)
        return NetworkConnectionType.parse_obj(data["networkConnectionType"])

    def update_private_network_connect(self, location_id: str, network_connection_type: NetworkConnectionType, org_id: str = None):
        """
        Update the location's network connection type.
        Network Connection Type determines if the location's network connection is public or private.
        Updating a location's network connection type requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update the network connection type for this location.
        :type location_id: str
        :param network_connection_type: Network Connection Type for the location.
        :type network_connection_type: NetworkConnectionType
        :param org_id: Update network connection type for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-private-network-connect
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdatePrivateNetworkConnectBody()
        if network_connection_type is not None:
            body.network_connection_type = network_connection_type
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        super().put(url=url, params=params, data=body.json())
        return

    def read_list_of_routing_choices(self, org_id: str = None, route_group_name: str = None, trunk_name: str = None, order: str = None, **params) -> Generator[RouteIdentity, None, None]:
        """
        List all Routes for the organization.
        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List route identities for this organization.
        :type org_id: str
        :param route_group_name: Return the list of route identities matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of route identities matching the Trunk name..
        :type trunk_name: str
        :param order: Order the route identities according to the designated fields. Available sort fields: routeName,
            routeType.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-routing-choices
        """
        if org_id is not None:
            params['orgId'] = org_id
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if order is not None:
            params['order'] = order
        url = self.ep('routeChoices')
        return self.session.follow_pagination(url=url, model=RouteIdentity, item_key='routeIdentities', params=params)

    def read_list_of_schedules(self, location_id: str, org_id: str = None, type_: str = None, name: str = None, **params) -> Generator[ListScheduleObject, None, None]:
        """
        List all schedules for the given location of the organization.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of schedules for this location.
        :type location_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param type_: Type of the schedule. * businessHours - Business hours schedule type. * holidays - Holidays
            schedule type.
        :type type_: str
        :param name: Only return schedules with the matching name.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-schedules
        """
        if org_id is not None:
            params['orgId'] = org_id
        if type_ is not None:
            params['type'] = type_
        if name is not None:
            params['name'] = name
        url = self.ep(f'locations/{location_id}/schedules')
        return self.session.follow_pagination(url=url, model=ListScheduleObject, item_key='schedules', params=params)

    def details_for_schedule(self, location_id: str, type_: str, schedule_id: str, org_id: str = None) -> GetDetailsForScheduleResponse:
        """
        Retrieve Schedule details.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Retrieving schedule details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule details in this location.
        :type location_id: str
        :param type_: Type of the schedule. * businessHours - Business hours schedule type. * holidays - Holidays
            schedule type.
        :type type_: str
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForScheduleResponse.parse_obj(data)

    def create_schedule(self, location_id: str, type_: Type25, name: str, org_id: str = None, events: ScheduleEventObject = None) -> str:
        """
        Create new Schedule for the given location.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Creating a schedule requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param type_: Type of the schedule.
        :type type_: Type25
        :param name: Unique name for the schedule.
        :type name: str
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :param events: List of schedule events.
        :type events: ScheduleEventObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateScheduleBody()
        if type_ is not None:
            body.type_ = type_
        if name is not None:
            body.name = name
        if events is not None:
            body.events = events
        url = self.ep(f'locations/{location_id}/schedules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_schedule(self, location_id: str, type_: str, schedule_id: str, name: str, org_id: str = None, events: ModifyScheduleEventListObject = None) -> str:
        """
        Update the designated schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Updating a schedule requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The Schedule ID will change upon modification of the Schedule name.

        :param location_id: Location in which this schedule exists.
        :type location_id: str
        :param type_: Type of schedule. * businessHours - Business hours schedule type. * holidays - Holidays schedule
            type.
        :type type_: str
        :param schedule_id: Update schedule with the matching ID.
        :type schedule_id: str
        :param name: Unique name for the schedule.
        :type name: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :param events: List of schedule events.
        :type events: ModifyScheduleEventListObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateScheduleBody()
        if name is not None:
            body.name = name
        if events is not None:
            body.events = events
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_schedule(self, location_id: str, type_: str, schedule_id: str, org_id: str = None):
        """
        Delete the designated Schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Deleting a schedule requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type_: Type of the schedule. * businessHours - Business hours schedule type. * holidays - Holidays
            schedule type.
        :type type_: str
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        super().delete(url=url, params=params)
        return

    def details_for_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, org_id: str = None) -> GetScheduleEventObject:
        """
        Retrieve Schedule Event details.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Retrieving a schedule event's details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule event details in this location.
        :type location_id: str
        :param type_: Type of schedule. * businessHours - Business hours schedule type. * holidays - Holidays schedule
            type.
        :type type_: str
        :param schedule_id: Retrieve the schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-schedule-event
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().get(url=url, params=params)
        return GetScheduleEventObject.parse_obj(data)

    def create_schedule_event(self, location_id: str, type_: str, schedule_id: str, name: str, start_date: str, end_date: str, org_id: str = None, start_time: str = None, end_time: str = None, all_day_enabled: bool = None, recurrence: RecurrenceObject1 = None) -> str:
        """
        Create new Event for the given location Schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Creating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param type_: Type of schedule. * businessHours - Business hours schedule type. * holidays - Holidays schedule
            type.
        :type type_: str
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of event.
        :type start_date: str
        :param end_date: End date of event.
        :type end_date: str
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the
            startTime and endTime are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject1

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-schedule-event
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ScheduleEventObject()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, name: str, start_date: str, end_date: str, org_id: str = None, start_time: str = None, end_time: str = None, all_day_enabled: bool = None, recurrence: RecurrenceObject1 = None) -> str:
        """
        Update the designated Schedule Event.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Updating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.
        NOTE: The schedule event ID will change upon modification of the schedule event name.

        :param location_id: Location in which this schedule event exists.
        :type location_id: str
        :param type_: Type of schedule. * businessHours - Business hours schedule type. * holidays - Holidays schedule
            type.
        :type type_: str
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Update the schedule event with the matching schedule event ID.
        :type event_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of event.
        :type start_date: str
        :param end_date: End date of event.
        :type end_date: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the
            startTime and endTime are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject1

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-schedule-event
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ScheduleEventObject()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, org_id: str = None):
        """
        Delete the designated Schedule Event.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.
        Deleting a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type_: Type of schedule. * businessHours - Business hours schedule type. * holidays - Holidays schedule
            type.
        :type type_: str
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-schedule-event
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_virtual_lines(self, org_id: str = None, location_id: List[str] = None, id: List[str] = None, owner_name: List[str] = None, phone_number: List[str] = None, location_name: List[str] = None, order: List[str] = None, has_device_assigned: bool = None, has_extension_assigned: bool = None, has_dn_assigned: bool = None, **params) -> Generator[ListVirtualLineObject, None, None]:
        """
        List all Virtual Lines for the organization.
        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            ?locationId=locId1&locationId=locId2.
        :type location_id: List[str]
        :param id: Return the list of virtual lines matching these virtualLineIds. Example for multiple values -
            ?id=id1&id=id2.
        :type id: List[str]
        :param owner_name: Return the list of virtual lines matching these owner names. Example for multiple values -
            ?ownerName=name1&ownerName=name2.
        :type owner_name: List[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers. Example for multiple values
            - ?phoneNumber=number1&phoneNumber=number2.
        :type phone_number: List[str]
        :param location_name: Return the list of virtual lines matching the location names. Example for multiple values
            - ?locationName=loc1&locationName=loc2.
        :type location_name: List[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time. Example for multiple values - ?order=order1&order=order2.
        :type order: List[str]
        :param has_device_assigned: If true, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If true, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If true, includes only virtual lines with an assigned directory number, also known as a
            Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-virtual-lines
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if id is not None:
            params['id'] = id
        if owner_name is not None:
            params['ownerName'] = owner_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = str(has_device_assigned).lower()
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = str(has_extension_assigned).lower()
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = str(has_dn_assigned).lower()
        url = self.ep('virtualLines')
        return self.session.follow_pagination(url=url, model=ListVirtualLineObject, item_key='virtualLines', params=params)

    def voicemail_settings(self, org_id: str = None) -> GetVoicemailSettingsResponse:
        """
        Retrieve the organization's voicemail settings.
        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.
        Retrieving organization's voicemail settings requires a full, user or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-voicemail-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/settings')
        data = super().get(url=url, params=params)
        return GetVoicemailSettingsResponse.parse_obj(data)

    def update_voicemail_settings(self, org_id: str = None, message_expiry_enabled: bool = None, number_of_days_for_message_expiry: int = None, strict_deletion_enabled: bool = None, voice_message_forwarding_enabled: bool = None):
        """
        Update the organization's voicemail settings.
        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.
        Updating an organization's voicemail settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        :param message_expiry_enabled: When enabled, you can set the deletion conditions for expired messages.
        :type message_expiry_enabled: bool
        :param number_of_days_for_message_expiry: Number of days after which messages expire.
        :type number_of_days_for_message_expiry: int
        :param strict_deletion_enabled: When enabled, all read and unread voicemail messages will be deleted based on
            the time frame you set. When disabled, all unread voicemail messages will be kept.
        :type strict_deletion_enabled: bool
        :param voice_message_forwarding_enabled: When enabled, people in the organization can configure the email
            forwarding of voicemails.
        :type voice_message_forwarding_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-voicemail-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetVoicemailSettingsResponse()
        if message_expiry_enabled is not None:
            body.message_expiry_enabled = message_expiry_enabled
        if number_of_days_for_message_expiry is not None:
            body.number_of_days_for_message_expiry = number_of_days_for_message_expiry
        if strict_deletion_enabled is not None:
            body.strict_deletion_enabled = strict_deletion_enabled
        if voice_message_forwarding_enabled is not None:
            body.voice_message_forwarding_enabled = voice_message_forwarding_enabled
        url = self.ep('voicemail/settings')
        super().put(url=url, params=params, data=body.json())
        return

    def voicemail_rules(self, org_id: str = None) -> GetVoicemailRulesResponse:
        """
        Retrieve the organization's voicemail rules.
        Organizational voicemail rules specify the default passcode requirements. They are provided for informational
        purposes only and cannot be modified.
        Retrieving the organization's voicemail rules requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail rules for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-voicemail-rules
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/rules')
        data = super().get(url=url, params=params)
        return GetVoicemailRulesResponse.parse_obj(data)

    def update_voicemail_rules(self, org_id: str = None, default_voicemail_pin_enabled: bool = None, default_voicemail_pin: str = None, expire_passcode: ExpirePasscode = None, change_passcode: ExpirePasscode = None, block_previous_passcodes: BlockPreviousPasscodes = None):
        """
        Update the organization's default voicemail passcode and/or rules.
        Organizational voicemail rules specify the default passcode requirements.
        If you choose to set a default passcode for new people added to your organization, communicate to your people
        what that passcode is, and that it must be reset before they can access their voicemail. If this feature is not
        turned on, each new person must initially set their own passcode.
        Updating an organization's voicemail passcode and/or rules requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.

        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :param default_voicemail_pin_enabled: Set to true to enable the default voicemail passcode.
        :type default_voicemail_pin_enabled: bool
        :param default_voicemail_pin: Default voicemail passcode.
        :type default_voicemail_pin: str
        :param expire_passcode: Settings for passcode expiry.
        :type expire_passcode: ExpirePasscode
        :param change_passcode: Settings for passcode changes.
        :type change_passcode: ExpirePasscode
        :param block_previous_passcodes: Settings for previous passcode usage.
        :type block_previous_passcodes: BlockPreviousPasscodes

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-voicemail-rules
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateVoicemailRulesBody()
        if default_voicemail_pin_enabled is not None:
            body.default_voicemail_pin_enabled = default_voicemail_pin_enabled
        if default_voicemail_pin is not None:
            body.default_voicemail_pin = default_voicemail_pin
        if expire_passcode is not None:
            body.expire_passcode = expire_passcode
        if change_passcode is not None:
            body.change_passcode = change_passcode
        if block_previous_passcodes is not None:
            body.block_previous_passcodes = block_previous_passcodes
        url = self.ep('voicemail/rules')
        super().put(url=url, params=params, data=body.json())
        return

    def location_voicemail(self, location_id: str, org_id: str = None) -> bool:
        """
        Retrieve voicemail settings for a specific location.
        Location voicemail settings allows you to enable voicemail transcription for a specific location.
        Retrieving a location's voicemail settings requires a full, user or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail settings for this location.
        :type location_id: str
        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-voicemail
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemail')
        data = super().get(url=url, params=params)
        return data["voicemailTranscriptionEnabled"]

    def update_location_voicemail(self, location_id: str, voicemail_transcription_enabled: bool, org_id: str = None):
        """
        Update the voicemail settings for a specific location.
        Location voicemail settings allows you to enable voicemail transcription for a specific location.
        Updating a location's voicemail settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update voicemail settings for this location.
        :type location_id: str
        :param voicemail_transcription_enabled: Set to true to enable voicemail transcription.
        :type voicemail_transcription_enabled: bool
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-location-voicemail
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateLocationVoicemailBody()
        if voicemail_transcription_enabled is not None:
            body.voicemail_transcription_enabled = voicemail_transcription_enabled
        url = self.ep(f'locations/{location_id}/voicemail')
        super().put(url=url, params=params, data=body.json())
        return

    def voice_portal(self, location_id: str, org_id: str = None) -> GetVoicePortalResponse:
        """
        Retrieve Voice portal information for the location.
        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant announcements.
        Retrieving voice portal information for an organization requires a full read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-voiceportal
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicePortal')
        data = super().get(url=url, params=params)
        return GetVoicePortalResponse.parse_obj(data)

    def update_voice_portal(self, location_id: str, org_id: str = None, extension: str = None, name: str = None, language_code: str = None, phone_number: str = None, first_name: str = None, last_name: str = None, passcode: Passcode = None):
        """
        Update Voice portal information for the location.
        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant anouncements.
        Updating voice portal information for an organization and/or rules requires a full administrator auth token
        with a scope of spark-admin:telephony_config_write.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param phone_number: Phone Number of incoming call.
        :type phone_number: str
        :param first_name: Caller ID First Name.
        :type first_name: str
        :param last_name: Caller ID Last Name.
        :type last_name: str
        :param passcode: Voice Portal Admin Passcode.
        :type passcode: Passcode

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-voiceportal
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateVoicePortalBody()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if language_code is not None:
            body.language_code = language_code
        if phone_number is not None:
            body.phone_number = phone_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if passcode is not None:
            body.passcode = passcode
        url = self.ep(f'locations/{location_id}/voicePortal')
        super().put(url=url, params=params, data=body.json())
        return

    def voice_portal_passcode_rule(self, location_id: str, org_id: str = None) -> GetVoicePortalPasscodeRuleResponse:
        """
        Retrieve the voice portal passcode rule for a location.
        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        anouncements
        Retrieving the voice portal passcode rule requires a full read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-voiceportal-passcode-rule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicePortal/passcodeRules')
        data = super().get(url=url, params=params)
        return GetVoicePortalPasscodeRuleResponse.parse_obj(data)

    def music_on_hold(self, location_id: str, org_id: str = None) -> GetMusicOnHoldResponse:
        """
        Retrieve the location's music on hold settings.
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        Retrieving a location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve music on hold settings for this location.
        :type location_id: str
        :param org_id: Retrieve music on hold settings for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-music-on-hold
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/musicOnHold')
        data = super().get(url=url, params=params)
        return GetMusicOnHoldResponse.parse_obj(data)

    def update_music_on_hold(self, location_id: str, org_id: str = None, call_hold_enabled: bool = None, call_park_enabled: bool = None, greeting: Greeting29 = None):
        """
        Update the location's music on hold settings.
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        Updating a location's music on hold settings requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        :param greeting: Greeting type for the location.
        :type greeting: Greeting29

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-music-on-hold
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetMusicOnHoldResponse()
        if call_hold_enabled is not None:
            body.call_hold_enabled = call_hold_enabled
        if call_park_enabled is not None:
            body.call_park_enabled = call_park_enabled
        if greeting is not None:
            body.greeting = greeting
        url = self.ep(f'locations/{location_id}/musicOnHold')
        super().put(url=url, params=params, data=body.json())
        return

    def list_voicemail_group(self, location_id: str = None, org_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[GetVoicemailGroupObject, None, None]:
        """
        List the voicemail group information for the organization.
        You can create a shared voicemail box and inbound FAX box to
        assign to users or call routing features like an auto attendant, call queue, or hunt group.
        Retrieving a voicemail group for the organization requires a full read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-voicemailgroup
        """
        if location_id is not None:
            params['locationId'] = location_id
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('voicemailGroups')
        return self.session.follow_pagination(url=url, model=GetVoicemailGroupObject, item_key='voicemailGroups', params=params)

    def location_voicemail_group(self, location_id: str, voicemail_group_id: str, org_id: str = None) -> GetLocationVoicemailGroupResponse:
        """
        Retrieve voicemail group details for a location.
        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active,
        message storage settings, and how you would like to be notified of new voicemail messages.
        Retrieving voicemail group details requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-voicemail-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        data = super().get(url=url, params=params)
        return GetLocationVoicemailGroupResponse.parse_obj(data)

    def modify_location_voicemail_group(self, location_id: str, voicemail_group_id: str, org_id: str = None, enabled: bool = None, phone_number: str = None, extension: int = None, name: str = None, first_name: str = None, last_name: str = None, passcode: int = None, language_code: str = None, greeting: Greeting = None, greeting_description: str = None, message_storage: MessageStorage = None, notifications: NewNumber = None, fax_message: FaxMessage = None, transfer_to_number: NewNumber = None, email_copy_of_message: EmailCopyOfMessage = None):
        """
        Modifies the voicemail group location details for a particular location for a customer.
        Manage your voicemail settings, like when you want your voicemail to be active, message storage settings, and
        how you would like to be notified of new voicemail messages.
        Modifying the voicemail group location details requires a full, user administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Modifies the voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Modifies the voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Modifies the voicemail group details for a customer location.
        :type org_id: str
        :param enabled: Enable/disable fax messaging.
        :type enabled: bool
        :param phone_number: Phone number to receive fax messages.
        :type phone_number: str
        :param extension: Extension to receive fax messages.
        :type extension: int
        :param name: Set the name of the voicemail group.
        :type name: str
        :param first_name: Set the voicemail group caller ID first name.
        :type first_name: str
        :param last_name: Set the voicemail group called ID last name.
        :type last_name: str
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for the voicemail group audio announcement.
        :type language_code: str
        :param greeting: Voicemail group greeting type.
        :type greeting: Greeting
        :param greeting_description: CUSTOM greeting for previously uploaded.
        :type greeting_description: str
        :param message_storage: Message storage information
        :type message_storage: MessageStorage
        :param notifications: Message notifications
        :type notifications: NewNumber
        :param fax_message: Fax message receive settings
        :type fax_message: FaxMessage
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: NewNumber
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: EmailCopyOfMessage

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-location-voicemail-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyLocationVoicemailGroupBody()
        if enabled is not None:
            body.enabled = enabled
        if phone_number is not None:
            body.phone_number = phone_number
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if passcode is not None:
            body.passcode = passcode
        if language_code is not None:
            body.language_code = language_code
        if greeting is not None:
            body.greeting = greeting
        if greeting_description is not None:
            body.greeting_description = greeting_description
        if message_storage is not None:
            body.message_storage = message_storage
        if notifications is not None:
            body.notifications = notifications
        if fax_message is not None:
            body.fax_message = fax_message
        if transfer_to_number is not None:
            body.transfer_to_number = transfer_to_number
        if email_copy_of_message is not None:
            body.email_copy_of_message = email_copy_of_message
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def createnew_voicemail_group_for_location(self, location_id: str, passcode: int, language_code: str, message_storage: MessageStorage, notifications: NewNumber, fax_message: FaxMessage, transfer_to_number: NewNumber, email_copy_of_message: EmailCopyOfMessage, org_id: str = None, extension: str = None, name: str = None, phone_number: str = None, first_name: str = None, last_name: str = None) -> str:
        """
        Create a new voicemail group for the given location for a customer.
        A voicemail group can be created for given location for a customer.
        Creating a voicemail group for the given location requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create a new voice mail group for this location.
        :type location_id: str
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param message_storage: Message storage information
        :type message_storage: MessageStorage
        :param notifications: Message notifications
        :type notifications: NewNumber
        :param fax_message: Fax message information
        :type fax_message: FaxMessage
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: NewNumber
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: EmailCopyOfMessage
        :param org_id: Create a new voice mail group for this organization.
        :type org_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param phone_number: Set voicemail group phone number for this particular location.
        :type phone_number: str
        :param first_name: Set voicemail group caller ID first name.
        :type first_name: str
        :param last_name: Set voicemail group called ID last name.
        :type last_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-new-voicemail-group-for-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreatenewVoicemailGroupForLocationBody()
        if passcode is not None:
            body.passcode = passcode
        if language_code is not None:
            body.language_code = language_code
        if message_storage is not None:
            body.message_storage = message_storage
        if notifications is not None:
            body.notifications = notifications
        if fax_message is not None:
            body.fax_message = fax_message
        if transfer_to_number is not None:
            body.transfer_to_number = transfer_to_number
        if email_copy_of_message is not None:
            body.email_copy_of_message = email_copy_of_message
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if phone_number is not None:
            body.phone_number = phone_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        url = self.ep(f'locations/{location_id}/voicemailGroups')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_voicemail_group_for_location(self, location_id: str, voicemail_group_id: str, org_id: str = None):
        """
        Delete the designated voicemail group.
        Deleting a voicemail group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a voicemail group.
        :type location_id: str
        :param voicemail_group_id: Delete the voicemail group with the matching ID.
        :type voicemail_group_id: str
        :param org_id: Delete the voicemail group from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-voicemail-group-for-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_uc_manager_profiles(self, org_id: str = None) -> list[Location1]:
        """
        List all calling UC Manager Profiles for the organization.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).
        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the user
        level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-uc-manager-profiles
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callingProfiles')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Location1], data["callingProfiles"])

    def read_list_of_dial_patterns(self, dial_plan_id: str, org_id: str = None, dial_pattern: str = None, order: str = None, **params) -> Generator[str, None, None]:
        """
        List all Dial Patterns for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: ID of the organization to which the dial patterns belong.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and X
            (matches a single digit, 0-9). The ! wildcard can only occur once at the end and only in an E.164 pattern
        :type dial_pattern: str
        :param order: Order the dial patterns according to the designated fields. Available sort fields: dialPattern.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-dial-patterns
        """
        if org_id is not None:
            params['orgId'] = org_id
        if dial_pattern is not None:
            params['dialPattern'] = dial_pattern
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        return self.session.follow_pagination(url=url, model=str, item_key='dialPatterns', params=params)

    def modify_dial_patterns(self, dial_plan_id: str, org_id: str = None, dial_patterns: DialPattern = None, delete_all_dial_patterns: bool = None):
        """
        Modify dial patterns for the Dial Plan.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Modifying a dial pattern requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the request
            is not modified.
        :type dial_patterns: DialPattern
        :param delete_all_dial_patterns: Delete all the dial patterns for a dial plan.
        :type delete_all_dial_patterns: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-dial-patterns
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyDialPatternsBody()
        if dial_patterns is not None:
            body.dial_patterns = dial_patterns
        if delete_all_dial_patterns is not None:
            body.delete_all_dial_patterns = delete_all_dial_patterns
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        super().put(url=url, params=params, data=body.json())
        return

    def validate_dial_pattern(self, dial_patterns: List[str], org_id: str = None) -> ValidateDialPatternResponse:
        """
        Validate a Dial Pattern.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Validating a dial pattern requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param dial_patterns: Array of dial patterns. Possible values: +5555,7777
        :type dial_patterns: List[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/validate-a-dial-pattern
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidateDialPatternBody()
        if dial_patterns is not None:
            body.dial_patterns = dial_patterns
        url = self.ep('premisePstn/actions/validateDialPatterns/invoke')
        data = super().post(url=url, params=params, data=body.json())
        return ValidateDialPatternResponse.parse_obj(data)

    def read_list_of_dial_plans(self, org_id: str = None, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None, order: str = None, **params) -> Generator[DialPlan, None, None]:
        """
        List all Dial Plans for the organization.
        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List dial plans for this organization.
        :type org_id: str
        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the Trunk name..
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-dial-plans
        """
        if org_id is not None:
            params['orgId'] = org_id
        if dial_plan_name is not None:
            params['dialPlanName'] = dial_plan_name
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/dialPlans')
        return self.session.follow_pagination(url=url, model=DialPlan, item_key='dialPlans', params=params)

    def create_dial_plan(self, name: str, route_id: str, route_type: RouteType, org_id: str = None, dial_patterns: List[str] = None) -> str:
        """
        Create a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Creating a dial plan requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param dial_patterns: An Array of dial patterns. Possible values: +5555,+5556
        :type dial_patterns: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-dial-plan
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateDialPlanBody()
        if name is not None:
            body.name = name
        if route_id is not None:
            body.route_id = route_id
        if route_type is not None:
            body.route_type = route_type
        if dial_patterns is not None:
            body.dial_patterns = dial_patterns
        url = self.ep('premisePstn/dialPlans')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def dial_plan(self, dial_plan_id: str, org_id: str = None) -> GetDialPlanResponse:
        """
        Get a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Retrieving a dial plan requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-a-dial-plan
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        data = super().get(url=url, params=params)
        return GetDialPlanResponse.parse_obj(data)

    def modify_dial_plan(self, dial_plan_id: str, name: str, route_id: str, route_type: RouteType, org_id: str = None):
        """
        Modify a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Modifying a dial plan requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-a-dial-plan
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyDialPlanBody()
        if name is not None:
            body.name = name
        if route_id is not None:
            body.route_id = route_id
        if route_type is not None:
            body.route_type = route_type
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def delete_dial_plan(self, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Deleting a dial plan requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-dial-plan
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        super().delete(url=url, params=params)
        return

    def validate_local_gateway_fqdn_and_domain_for_trunk(self, org_id: str = None, address: str = None, domain: str = None, port: int = None):
        """
        Validate Local Gateway FQDN and Domain for the organization trunks.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.
        Validating Local Gateway FQDN and Domain requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param org_id: Organization to which trunk types belongs.
        :type org_id: str
        :param address: FQDN or SRV address of the trunk.
        :type address: str
        :param domain: Domain name of the trunk.
        :type domain: str
        :param port: FQDN port of the trunk.
        :type port: int

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/validate-local-gateway-fqdn-and-domain-for-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ValidateLocalGatewayFQDNAndDomainForTrunkBody()
        if address is not None:
            body.address = address
        if domain is not None:
            body.domain = domain
        if port is not None:
            body.port = port
        url = self.ep('premisePstn/trunks/actions/fqdnValidation/invoke')
        super().post(url=url, params=params, data=body.json())
        return

    def read_list_of_trunks(self, org_id: str = None, name: List[str] = None, location_name: List[str] = None, trunk_type: str = None, order: str = None, **params) -> Generator[Trunk, None, None]:
        """
        List all Trunks for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List trunks for this organization.
        :type org_id: str
        :param name: Return the list of trunks matching the local gateway names.
        :type name: List[str]
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: List[str]
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-trunks
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if location_name is not None:
            params['locationName'] = location_name
        if trunk_type is not None:
            params['trunkType'] = trunk_type
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/trunks')
        return self.session.follow_pagination(url=url, model=Trunk, item_key='trunks', params=params)

    def create_trunk(self, name: str, password: str, location_id: str, trunk_type: TrunkType, org_id: str = None, dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None, device_type: str = None, address: str = None, domain: str = None, port: int = None) -> str:
        """
        Create a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Creating a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param name: A unique name for the dial plan.
        :type name: str
        :param password: A password to use on the trunk.
        :type password: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: TrunkType
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :param dual_identity_support_enabled: Determines the behavior of the From and PAI headers on outbound calls.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate-based trunk.
        :type max_concurrent_calls: int
        :param device_type: Device type assosiated with trunk.
        :type device_type: str
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateTrunkBody()
        if name is not None:
            body.name = name
        if password is not None:
            body.password = password
        if location_id is not None:
            body.location_id = location_id
        if trunk_type is not None:
            body.trunk_type = trunk_type
        if dual_identity_support_enabled is not None:
            body.dual_identity_support_enabled = dual_identity_support_enabled
        if max_concurrent_calls is not None:
            body.max_concurrent_calls = max_concurrent_calls
        if device_type is not None:
            body.device_type = device_type
        if address is not None:
            body.address = address
        if domain is not None:
            body.domain = domain
        if port is not None:
            body.port = port
        url = self.ep('premisePstn/trunks')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def trunk(self, trunk_id: str, org_id: str = None) -> GetTrunkResponse:
        """
        Get a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.
        Retrieving a trunk requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        data = super().get(url=url, params=params)
        return GetTrunkResponse.parse_obj(data)

    def modify_trunk(self, trunk_id: str, name: str, password: str, org_id: str = None, dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None):
        """
        Modify a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.
        Modifying a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: ID of the trunk being modified.
        :type trunk_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param password: A password to use on the trunk.
        :type password: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :param dual_identity_support_enabled: Determines the behavior of the From and PAI headers on outbound calls.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate-based trunk.
        :type max_concurrent_calls: int

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyTrunkBody()
        if name is not None:
            body.name = name
        if password is not None:
            body.password = password
        if dual_identity_support_enabled is not None:
            body.dual_identity_support_enabled = dual_identity_support_enabled
        if max_concurrent_calls is not None:
            body.max_concurrent_calls = max_concurrent_calls
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def delete_trunk(self, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls
        over multiple trunks or to provide redundancy.
        Deleting a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_trunk_types(self, org_id: str = None) -> list[TrunkTypeWithDeviceType]:
        """
        List all Trunk Types with Device Types for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy. Trunk Types are Registering or Certificate Based and are
        configured in Call Manager.
        Retrieving trunk types requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Organization to which the trunk types belong.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-trunk-types
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('premisePstn/trunks/trunkTypes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[TrunkTypeWithDeviceType], data["trunkTypes"])

    def read_list_of_routing_groups(self, org_id: str = None, name: str = None, order: str = None, **params) -> Generator[RouteGroup, None, None]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.
        Retrieving this route group list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List route groups for this organization.
        :type org_id: str
        :param name: Return the list of route groups matching the Route group name..
        :type name: str
        :param order: Order the route groups according to designated fields. Available sort orders are asc and desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-routing-groups
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/routeGroups')
        return self.session.follow_pagination(url=url, model=RouteGroup, item_key='routeGroups', params=params)

    def create_route_group_for_organization(self, name: str, local_gateways: LocalGateways, org_id: str = None) -> str:
        """
        Creates a Route Group for the organization.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.
        Creating a Route Group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: LocalGateways
        :param org_id: Organization to which the Route Group belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-route-group-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateRouteGroupForOrganizationBody()
        if name is not None:
            body.name = name
        if local_gateways is not None:
            body.local_gateways = local_gateways
        url = self.ep('premisePstn/routeGroups')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def read_route_group_for_organization(self, route_group_id: str, org_id: str = None) -> ReadRouteGroupForOrganizationResponse:
        """
        Reads a Route Group for the organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.
        Reading a Route Group requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-a-route-group-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        data = super().get(url=url, params=params)
        return ReadRouteGroupForOrganizationResponse.parse_obj(data)

    def modify_route_group_for_organization(self, route_group_id: str, name: str, local_gateways: LocalGateways, org_id: str = None):
        """
        Modifies an existing Route Group for an organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.
        Modifying a Route Group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: LocalGateways
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-a-route-group-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateRouteGroupForOrganizationBody()
        if name is not None:
            body.name = name
        if local_gateways is not None:
            body.local_gateways = local_gateways
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def remove_route_group_from_organization(self, route_group_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.
        Removing a Route Group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/remove-a-route-group-from-an-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().delete(url=url, params=params)
        return

    def read_usage_of_routing_group(self, route_group_id: str, org_id: str = None) -> ReadUsageOfRoutingGroupResponse:
        """
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
        specific Route Group.
        Users within Call to Extension locations are registered to a PBX which allows you to route unknown extensions
        (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route Group.
        PSTN Connections may be a Cisco PSTN, a cloud-connected PSTN, or a premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group.
        Route Lists are a list of numbers that can be reached via a route group and can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving usage information requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with the specific route group.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-usage-of-a-routing-group
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usage')
        data = super().get(url=url, params=params)
        return ReadUsageOfRoutingGroupResponse.parse_obj(data)

    def read_to_extension_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, order: str = None, **params) -> Generator[Location1, None, None]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to the
        PBX using an existing trunk or route group.
        Retrieving this location list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields. Available sort orders are asc, and desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-call-to-extension-locations-of-a-routing-group
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageCallToExtension')
        return self.session.follow_pagination(url=url, model=Location1, item_key='locations', params=params)

    def read_dial_plan_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, order: str = None, **params) -> Generator[Location1, None, None]:
        """
        List Dial Plan Locations for a specific route group.
        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location.
        A Dial Plan also specifies the routing choice (trunk or route group) for calls that match any of its dial
        patterns. Specific dial patterns can be defined as part of your dial plan.
        Retrieving this location list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields. Available sort orders are asc, and desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-dial-plan-locations-of-a-routing-group
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Location1, item_key='locations', params=params)

    def read_pstn_connection_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, order: str = None, **params) -> Generator[Location1, None, None]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.
        Retrieving this Location list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param order: Order the locations according to designated fields. Available sort orders are asc, and desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-pstn-connection-locations-of-a-routing-group
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usagePstnConnection')
        return self.session.follow_pagination(url=url, model=Location1, item_key='locations', params=params)

    def read_route_lists_of_routing_group(self, route_group_id: str, org_id: str = None, name: str = None, order: str = None, **params) -> Generator[RouteGroupUsageRouteListGet, None, None]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a Route
        Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_group_id: ID of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param name: Return the list of locations matching the location name.
        :type name: str
        :param order: Order the locations according to designated fields. Available sort orders are asc, and desc.
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-route-lists-of-a-routing-group
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageRouteList')
        return self.session.follow_pagination(url=url, model=RouteGroupUsageRouteListGet, item_key='routeGroupUsageRouteListGet', params=params)

    def read_list_of_route_lists(self, org_id: str = None, name: List[str] = None, location_id: List[str] = None, order: str = None, **params) -> Generator[RouteList, None, None]:
        """
        List all Route Lists for the organization.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving the Route List requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List all Route List for this organization.
        :type org_id: str
        :param name: Return the list of Route List matching the route list name.
        :type name: List[str]
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: List[str]
        :param order: Order the Route List according to the designated fields. Available sort fields are name, and
            locationId. Sort order is ascending by default
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-route-lists
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/routeLists')
        return self.session.follow_pagination(url=url, model=RouteList, item_key='routeLists', params=params)

    def create_route_list(self, location_id: str, org_id: str = None, name: str = None, route_group_id: str = None) -> str:
        """
        Create a Route List for the organization.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Creating a Route List requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param name: Route List new name.
        :type name: str
        :param route_group_id: New route group ID.
        :type route_group_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateRouteListBody()
        if location_id is not None:
            body.location_id = location_id
        if name is not None:
            body.name = name
        if route_group_id is not None:
            body.route_group_id = route_group_id
        url = self.ep('premisePstn/routeLists')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def delete_route_list(self, route_list_id: str, org_id: str = None):
        """
        Delete a route list for a customer.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Deleting a Route List requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().delete(url=url, params=params)
        return

    def route_list(self, route_list_id: str, org_id: str = None) -> GetRouteListResponse:
        """
        Get a rout list details.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-a-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        data = super().get(url=url, params=params)
        return GetRouteListResponse.parse_obj(data)

    def modify_route_list(self, route_list_id: str, org_id: str = None, name: str = None, route_group_id: str = None):
        """
        Modify the details for a Route List.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param name: Route List new name.
        :type name: str
        :param route_group_id: New route group ID.
        :type route_group_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-a-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyRouteListBody()
        if name is not None:
            body.name = name
        if route_group_id is not None:
            body.route_group_id = route_group_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().put(url=url, params=params, data=body.json())
        return

    def modify_numbers_for_route_list(self, route_list_id: str, org_id: str = None, numbers: RouteListNumberPatch = None, delete_all_numbers: bool = None) -> list[RouteListNumberPatchResponse]:
        """
        Modify numbers for a specific Route List of a Customer.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: RouteListNumberPatch
        :param delete_all_numbers: If present, the numbers array is ignored and all numbers in the route list are
            deleted.
        :type delete_all_numbers: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-numbers-for-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyNumbersForRouteListBody()
        if numbers is not None:
            body.numbers = numbers
        if delete_all_numbers is not None:
            body.delete_all_numbers = delete_all_numbers
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        data = super().put(url=url, params=params, data=body.json())
        return parse_obj_as(list[RouteListNumberPatchResponse], data["numberStatus"])

    def numbers_assigned_to_route_list(self, route_list_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, number: str = None) -> str:
        """
        Get numbers assigned to a Route List
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param route_list_id: ID of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the Route Lists according to number, ascending or descending.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-numbers-assigned-to-a-route-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        if number is not None:
            params['number'] = number
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        data = super().get(url=url, params=params)
        return data["phoneNumbers"]

    def local_gateway_to_on_premises_extension_usage_for_trunk(self, trunk_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, name: List[str] = None) -> Location1:
        """
        Get local gateway call to on-premises extension usage for a trunk.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the trunks according to the designated fields. Available sort fields are name, and
            locationName. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-local-gateway-call-to-on-premises-extension-usage-for-a-trunk
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageCallToExtension')
        data = super().get(url=url, params=params)
        return Location1.parse_obj(data["location"])

    def local_gateway_dial_plan_usage_for_trunk(self, trunk_id: str, org_id: str = None, order: str = None, name: List[str] = None, **params) -> Generator[Location1, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :param order: Order the trunks according to the designated fields. Available sort fields are name, and
            locationName. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-local-gateway-dial-plan-usage-for-a-trunk
        """
        if org_id is not None:
            params['orgId'] = org_id
        if order is not None:
            params['order'] = order
        if name is not None:
            params['name'] = name
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageDialPlan')
        return self.session.follow_pagination(url=url, model=Location1, item_key='dialPlans', params=params)

    def locations_using_local_gateway_as_pstn_connection_routing(self, trunk_id: str, org_id: str = None) -> Location1:
        """
        Get Locations Using the Local Gateway as PSTN Connection Routing.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-locations-using-the-local-gateway-as-pstn-connection-routing
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usagePstnConnection')
        data = super().get(url=url, params=params)
        return Location1.parse_obj(data["location"])

    def route_groups_using_local_gateway(self, trunk_id: str, org_id: str = None) -> list[RouteGroup]:
        """
        Get Route Groups Using the Local Gateway.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-route-groups-using-the-local-gateway
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageRouteGroup')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[RouteGroup], data["routeGroup"])

    def local_gateway_usage_count(self, trunk_id: str, org_id: str = None) -> GetLocalGatewayUsageCountResponse:
        """
        Get Local Gateway Usage Count
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute
        calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-local-gateway-usage-count
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usage')
        data = super().get(url=url, params=params)
        return GetLocalGatewayUsageCountResponse.parse_obj(data)

    def details_for_queue_holiday_service(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueHolidayServiceResponse:
        """
        Retrieve Call Queue Holiday Service details.
        Configure the call queue to route calls differently during the holidays.
        Retrieving call queue holiday service details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-queue-holiday-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueHolidayServiceResponse.parse_obj(data)

    def update_queue_holiday_service(self, location_id: str, queue_id: str, holiday_service_enabled: bool, holiday_schedule_level: HolidayScheduleLevel, play_announcement_before_enabled: bool, org_id: str = None, action: Action15 = None, transfer_phone_number: str = None, audio_message_selection: Greeting = None, audio_files: CallQueueAudioFilesObject = None, holiday_schedule_name: str = None):
        """
        Update the designated Call Queue Holiday Service.
        Configure the call queue to route calls differently during the holidays.
        Updating a call queue holiday service requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param holiday_service_enabled: Enable or Disable the call queue holiday service routing policy.
        :type holiday_service_enabled: bool
        :param holiday_schedule_level: Specifies whether the schedule mentioned in holidayScheduleName is org or
            location specific. (Must be from holidaySchedules list)
        :type holiday_schedule_level: HolidayScheduleLevel
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param action: Specifies call processing action type.
        :type action: Action15
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param audio_files: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: CallQueueAudioFilesObject
        :param holiday_schedule_name: Name of the schedule configured for a holiday service as one of from
            holidaySchedules list.
        :type holiday_schedule_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-queue-holiday-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueHolidayServiceBody()
        if holiday_service_enabled is not None:
            body.holiday_service_enabled = holiday_service_enabled
        if holiday_schedule_level is not None:
            body.holiday_schedule_level = holiday_schedule_level
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if action is not None:
            body.action = action
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if audio_files is not None:
            body.audio_files = audio_files
        if holiday_schedule_name is not None:
            body.holiday_schedule_name = holiday_schedule_name
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_night_service(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueNightServiceResponse:
        """
        Retrieve Call Queue Night service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-queue-night-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueNightServiceResponse.parse_obj(data)

    def update_queue_night_service(self, location_id: str, queue_id: str, night_service_enabled: bool, play_announcement_before_enabled: bool, announcement_mode: AnnouncementMode, force_night_service_enabled: bool, manual_audio_message_selection: Greeting, org_id: str = None, action: Action15 = None, transfer_phone_number: str = None, audio_message_selection: Greeting = None, audio_files: CallQueueAudioFilesObject = None, business_hours_name: str = None, business_hours_level: HolidayScheduleLevel = None, manual_audio_files: CallQueueAudioFilesObject = None):
        """
        Update Call Queue Night Service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Updating call queue night service details requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param night_service_enabled: Enable or disable call queue night service routing policy.
        :type night_service_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param announcement_mode: Specifies the type of announcements to played.
        :type announcement_mode: AnnouncementMode
        :param force_night_service_enabled: Force night service regardless of business hour schedule.
        :type force_night_service_enabled: bool
        :param manual_audio_message_selection: Specifies what type of announcement to be played when announcementMode
            is MANUAL.
        :type manual_audio_message_selection: Greeting
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str
        :param action: Specifies call processing action type.
        :type action: Action15
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param audio_files: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: CallQueueAudioFilesObject
        :param business_hours_name: Name of the schedule configured for a night service as one of from
            businessHourSchedules list.
        :type business_hours_name: str
        :param business_hours_level: Specifies whether the above mentioned schedule is org or location specific. (Must
            be from businessHourSchedules list)
        :type business_hours_level: HolidayScheduleLevel
        :param manual_audio_files: List Of pre-configured Audio Files.
        :type manual_audio_files: CallQueueAudioFilesObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-queue-night-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateCallQueueNightServiceBody()
        if night_service_enabled is not None:
            body.night_service_enabled = night_service_enabled
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if announcement_mode is not None:
            body.announcement_mode = announcement_mode
        if force_night_service_enabled is not None:
            body.force_night_service_enabled = force_night_service_enabled
        if manual_audio_message_selection is not None:
            body.manual_audio_message_selection = manual_audio_message_selection
        if action is not None:
            body.action = action
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if audio_files is not None:
            body.audio_files = audio_files
        if business_hours_name is not None:
            body.business_hours_name = business_hours_name
        if business_hours_level is not None:
            body.business_hours_level = business_hours_level
        if manual_audio_files is not None:
            body.manual_audio_files = manual_audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_forced_forward(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueForcedForwardResponse:
        """
        Retrieve Call Queue policy Forced Forward details.
        This policy allows calls to be temporarily diverted to a configured destination.
        Retrieving call queue Forced Forward details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-queue-forced-forward
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueForcedForwardResponse.parse_obj(data)

    def update_queue_forced_forward_service(self, location_id: str, queue_id: str, org_id: str = None, forced_forward_enabled: bool = None, transfer_phone_number: str = None, play_announcement_before_enabled: bool = None, audio_message_selection: Greeting = None, audio_files: CallQueueAudioFilesObject = None):
        """
        Update the designated Forced Forward Service.
        If the option is enabled, then incoming calls to the queue are forwarded to the configured destination. Calls
        that are already in the queue remain queued.
        The policy can be configured to play an announcement prior to proceeding with the forward.
        Updating a call queue Forced Forward service requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param forced_forward_enabled: Whether or not the call queue forced forward routing policy setting is enabled.
        :type forced_forward_enabled: bool
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the
            action.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param audio_files: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: CallQueueAudioFilesObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-queue-forced-forward-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetDetailsForCallQueueForcedForwardResponse()
        if forced_forward_enabled is not None:
            body.forced_forward_enabled = forced_forward_enabled
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if play_announcement_before_enabled is not None:
            body.play_announcement_before_enabled = play_announcement_before_enabled
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if audio_files is not None:
            body.audio_files = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        super().put(url=url, params=params, data=body.json())
        return

    def details_for_queue_stranded(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueStrandedCallsResponse:
        """
        Allow admin to view default/configured Stranded Calls settings.
        Stranded-All agents logoff Policy: If the last agent staffing a queue “unjoins” the queue or signs out, then
        all calls in the queue become stranded.
        Stranded-Unavailable Policy: This policy allows for the configuration of the processing of calls that are in a
        staffed queue when all agents are unavailable.
        Retrieving call queue Stranded Calls details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-details-for-a-call-queue-stranded-calls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueStrandedCallsResponse.parse_obj(data)

    def update_queue_stranded_service(self, location_id: str, queue_id: str, org_id: str = None, action: Action15 = None, transfer_phone_number: str = None, audio_message_selection: Greeting = None, audio_files: CallQueueAudioFilesObject = None):
        """
        Update the designated Call Stranded Calls Service.
        Allow admin to modify configured Stranded Calls settings.
        Updating a call queue stranded calls requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param action: Specifies call processing action type.
        :type action: Action15
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can
            also be an extension.
        :type transfer_phone_number: str
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: Greeting
        :param audio_files: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: CallQueueAudioFilesObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-call-queue-stranded-calls-service
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetDetailsForCallQueueStrandedCallsResponse()
        if action is not None:
            body.action = action
        if transfer_phone_number is not None:
            body.transfer_phone_number = transfer_phone_number
        if audio_message_selection is not None:
            body.audio_message_selection = audio_message_selection
        if audio_files is not None:
            body.audio_files = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        super().put(url=url, params=params, data=body.json())
        return

    def location_device_settings(self, location_id: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get device override settings for a location.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Organization in which the device resides.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-location-device-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/devices/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def read_list_of_supported_devices(self, org_id: str = None) -> list[DeviceObject]:
        """
        Gets the list of supported devices for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-supported-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('supportedDevices')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[DeviceObject], data["devices"])

    def readdevice_override_settings_fororganization(self, org_id: str = None) -> ReaddeviceOverrideSettingsFororganizationResponse:
        """
        Get device override settings for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-device-override-settings-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/settings')
        data = super().get(url=url, params=params)
        return ReaddeviceOverrideSettingsFororganizationResponse.parse_obj(data)

    def read_dect_device_type_list(self, org_id: str = None) -> list[DectDeviceList]:
        """
        Get DECT device type list with base stations and line ports supported count. This is a static list.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: 
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-dect-device-type-list
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/dects/supportedDevices')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[DectDeviceList], data["devices"])

    def validatelist_of_mac_address(self, macs: List[str], org_id: str = None) -> ValidatelistOfMACAddressResponse:
        """
        Validate a list of MAC addresses.
        Validating this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param macs: MAC addresses to be validated. Possible values: {["ab125678cdef", "00005E0053B4"]}
        :type macs: List[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/validate-a-list-of-mac-address
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

    def change_device_settings_across_organization_or_location_job(self, org_id: str = None, location_id: str = None, location_customizations_enabled: bool = None, customizations: CustomizationObject = None) -> StartJobResponse:
        """
        Change device settings across organization or locations jobs.
        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system
        admins in a stateful persistent manner. This job will modify the requested device settings across all the
        devices. Whenever a location ID is specified in the request, it will modify the requested device settings only
        for the devices that are part of the provided location within an organization.
        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.
        Only one job per customer can be running at any given time within the same organization. An attempt to run
        multiple jobs at the same time will result in a 409 error response.
        Running a job requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :param location_id: Location within an organization where changes of device setings will be applied to all the
            devices within it.
        :type location_id: str
        :param location_customizations_enabled: Indicates if all the devices within this location will be customized
            with new requested customizations(if set to true) or will be overridden with the one at organization level
            (if set to false or any other value). This field has no effect when the job is being triggered at
            organization level.
        :type location_customizations_enabled: bool
        :param customizations: Indicates the settings for ATA devices, DECT devices and MPP devices.
        :type customizations: CustomizationObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/change-device-settings-across-organization-or-location-job
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
        return StartJobResponse.parse_obj(data)

    def list_change_device_settings_jobs(self, org_id: str = None, **params) -> Generator[StartJobResponse, None, None]:
        """
        List change device settings jobs.
        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to
        oldest one irrespective of its status.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-change-device-settings-jobs
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/devices/callDeviceSettings')
        return self.session.follow_pagination(url=url, model=StartJobResponse, params=params)

    def change_device_settings_job_status(self, job_id: str) -> GetManageNumbersJobStatusResponse:
        """
        Get change device settings job status.
        Provides details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-change-device-settings-job-status
        """
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}')
        data = super().get(url=url)
        return GetManageNumbersJobStatusResponse.parse_obj(data)

    def list_change_device_settings_job_errors(self, job_id: str, org_id: str = None, **params) -> Generator[ItemObject, None, None]:
        """
        List change device settings job errors.
        Lists all error details of the job with jobId of jobType calldevicesettings.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/list-change-device-settings-job-errors
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/devices/callDeviceSettings/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, params=params)

    def read_list_of_announcement_languages(self) -> list[FeatureAccessCode]:
        """
        List all languages supported by Webex Calling for announcements and voice prompts.
        Retrieving announcement languages requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-announcement-languages
        """
        url = self.ep('announcementLanguages')
        data = super().get(url=url)
        return parse_obj_as(list[FeatureAccessCode], data["languages"])

    def create_receptionist_contact_directory(self, location_id: str, contacts: List[PersonId], org_id: str = None, name: str = None) -> str:
        """
        Creates a new Receptionist Contact Directory for a location.
        Receptionist Contact Directories can be used to create named directories of users.
        Adding a directory requires a full or write-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Add a Receptionist Contact Directory to this location.
        :type location_id: str
        :param contacts: Array of users assigned to this Receptionist Contact Directory. Person ID.
        :type contacts: List[PersonId]
        :param org_id: Add a Receptionist Contact Directory to this organization.
        :type org_id: str
        :param name: Receptionist Contact Directory name.
        :type name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-receptionist-contact-directory
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateReceptionistContactDirectoryBody()
        if contacts is not None:
            body.contacts = contacts
        if name is not None:
            body.name = name
        url = self.ep(f'locations/{location_id}/receptionistContacts/directories')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def read_list_of_receptionist_contact_directories(self, location_id: str, org_id: str = None) -> list[Location1]:
        """
        List all Receptionist Contact Directories for a location.
        Receptionist Contact Directories can be used to create named directories of users.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: List Receptionist Contact Directories for this location.
        :type location_id: str
        :param org_id: List Receptionist Contact Directories for this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-list-of-receptionist-contact-directories
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/receptionistContacts/directories')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Location1], data["directories"])

    def delete_receptionist_contact_directory(self, location_id: str, directory_id: optional, org_id: str = None):
        """
        Delete a Receptionist Contact Directory from a location.
        Receptionist Contact Directories can be used to create named directories of users.
        Deleting a directory requires a full or write-only administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Delete a Receptionist Contact Directory from this location.
        :type location_id: str
        :param directory_id: Add a Receptionist Contact Directory ID.
        :type directory_id: optional
        :param org_id: Delete a Receptionist Contact Directory from this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/delete-a-receptionist-contact-directory
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/receptionistContacts/directories/{directory_id}')
        super().delete(url=url, params=params)
        return

class WebexCallingOrganizationSettingswithDevicesPhase3FeaturesApi(ApiChild, base='telephony/config/'):
    """
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these organization settings requires a full administrator auth token with a scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def location_device(self, location_id: str, org_id: str = None) -> GetDeviceSettingsResponse:
        """
        Get device override settings for a location.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Organization in which the device resides.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-devices-phase3-features/get-location-device-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/devices/settings')
        data = super().get(url=url, params=params)
        return GetDeviceSettingsResponse.parse_obj(data)

    def readdevice_override_fororganization(self, org_id: str = None) -> ReaddeviceOverrideSettingsFororganizationResponse:
        """
        Get device override settings for an organization.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings-with-devices-phase3-features/read-the-device-override-settings-for-a-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('devices/settings')
        data = super().get(url=url, params=params)
        return ReaddeviceOverrideSettingsFororganizationResponse.parse_obj(data)

class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    id: Optional[str]
    #: First name of member.
    first_name: Optional[str]
    #: Last name of member.
    last_name: Optional[str]
    #: Phone number of member. Currently, E.164 format is not supported.
    phone_number: Optional[str]
    #: Phone extension of member.
    extension: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location1]


class PutSharedLineMemberItem(ApiModel):
    #: Unique identifier for the person or workspace.
    id: Optional[str]
    #: Device port number assigned to person or workspace.
    port: Optional[int]
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    t38_fax_compression_enabled: Optional[bool]
    #: If true the person or the workspace is the owner of the device. Points to primary line/port of the device.
    primary_owner: Optional[str]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    line_type: Optional[LineType]
    #: Number of lines that have been configured for the person on the device.
    line_weight: Optional[int]
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in hotlineDestination.
    hotline_enabled: Optional[bool]
    #: Preconfigured number for the hotline. Required only if hotlineEnabled is set to true.
    hotline_destination: Optional[str]
    #: Set how a device behaves when a call is declined. When set to true, a call decline request is extended to all
    #: the endpoints on the device. When set to false, a call decline request is only declined at the current endpoint.
    allow_call_decline_enabled: Optional[bool]
    #: Device line label.
    line_label: Optional[str]


class GetSharedLineMemberItem(PutSharedLineMemberItem):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the
    #: future update.
    phone_number: Optional[str]
    #: Phone extension of a person or workspace.
    extension: Optional[str]
    #: Registration home IP for the line port.
    host_ip: Optional[str]
    #: Registration remote IP for the line port.
    remote_ip: Optional[str]
    #: Indicates if the member is of type PEOPLE or PLACE.
    member_type: Optional[MemberType]
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location1]


class EffectiveBehaviorType(str, Enum):
    #: Calling in Webex or Hybrid Calling.
    native_webex_teams_calling = 'NATIVE_WEBEX_TEAMS_CALLING'
    #: Cisco Jabber app
    call_with_app_registered_for_ciscotel = 'CALL_WITH_APP_REGISTERED_FOR_CISCOTEL'
    #: Third-Party app
    call_with_app_registered_for_tel = 'CALL_WITH_APP_REGISTERED_FOR_TEL'
    #: Webex Calling app
    call_with_app_registered_for_webexcalltel = 'CALL_WITH_APP_REGISTERED_FOR_WEBEXCALLTEL'
    #: Calling in Webex (Unified CM)
    native_sip_call_to_ucm = 'NATIVE_SIP_CALL_TO_UCM'


class BehaviorType(EffectiveBehaviorType):
    #: Using the non-string value of null results in the organization-wide default calling behavior being in effect.
    null = 'null'


class ConfigurepersonsCallingBehaviorBody(ApiModel):
    #: The new Calling Behavior setting for the person (case-insensitive). If null, the effective Calling Behavior will
    #: be the Organization's current default.
    behavior_type: Optional[BehaviorType]
    #: The UC Manager Profile ID. Specifying null results in the organizational default being applied.
    profile_id: Optional[str]


class ReadBargeInSettingsForPersonResponse(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    enabled: Optional[bool]
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: Optional[bool]


class NoAnswer3(BusinessContinuity):
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class CallForwarding4(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person
    #: is busy.
    busy: Optional[BusinessContinuity]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[NoAnswer3]


class ReadForwardingSettingsForPersonResponse(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwarding4]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[BusinessContinuity]


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
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool]
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType]
    #: Owner of device.
    owner: Optional[DeviceOwner]
    #: Activation state of device.
    activation_state: Optional[ActivationStates]


class Record(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (*44) has been entered. Pause, resume, and stop
    #: controls are supported.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class Type33(str, Enum):
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class Type32(Type33):
    #: No notification sound played when call recording is paused or resumed.
    none = 'None'


class Notification(ApiModel):
    #: Type of pause/resume notification.
    type: Optional[Type32]
    #: true when the notification feature is in effect. false indicates notification is disabled.
    enabled: Optional[bool]


class Repeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    interval: Optional[int]
    #: true when ongoing call recording tone will be played at the designated interval. false indicates no warning tone
    #: will be played.
    enabled: Optional[bool]


class ConfigureCallRecordingSettingsForPersonBody(ApiModel):
    #: true if call recording is enabled.
    enabled: Optional[bool]
    #: Call recording scenario.
    record: Optional[Record]
    #: When true, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool]
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends.
    start_stop_announcement_enabled: Optional[bool]
    #: Pause/resume notification settings.
    notification: Optional[Notification]
    #: Beep sound plays periodically.
    repeat: Optional[Repeat]


class CLIDPolicySelection(ApiModel):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line: Optional[str]
    #: Outgoing caller ID will show the main number for the location.
    location_number: Optional[str]
    #: Outgoing caller ID will show the value from the customNumber field.
    custom: Optional[str]


class CallerIdSelectedType(CLIDPolicySelection):
    #: Outgoing caller ID will show the mobile number for this person.
    mobile_number: Optional[str]


class ConfigureCallerIDSettingsForPersonBody(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    #: Possible values: DIRECT_LINE
    selected: Optional[CallerIdSelectedType]
    #: This value must be an assigned number from the person's location.
    custom_number: Optional[str]
    #: Person's Caller ID first name. Characters of %, +, ``, " and Unicode characters are not allowed.
    first_name: Optional[str]
    #: Person's Caller ID last name. Characters of %, +, ``, " and Unicode characters are not allowed.
    last_name: Optional[str]
    #: true if person's identity has to be blocked when receiving a transferred or forwarded call.
    block_in_forward_calls_enabled: Optional[bool]
    #: Designates which type of External Caller Id Name policy is used. Default is DIRECT_LINE.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: Person's custom External Caller ID last name. Characters of %, +, ``, " and Unicode characters are not allowed.
    custom_external_caller_id_name: Optional[str]


class ReadDoNotDisturbSettingsForPersonResponse(ApiModel):
    #: true if the Do Not Disturb feature is enabled.
    enabled: Optional[bool]
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: Optional[bool]


class SendAllCalls(ApiModel):
    #: All calls will be sent to voicemail.
    enabled: Optional[bool]


class SendBusyCalls(SendBusyCalls1):
    #: Indicates a custom greeting has been uploaded.
    greeting_uploaded: Optional[bool]


class SendUnansweredCalls(SendBusyCalls):
    #: Number of rings before unanswered call will be sent to voicemail.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class MessageStorage3(MessageStorage):
    #: When true desktop phone will indicate there are new voicemails.
    mwi_enabled: Optional[bool]


class ReadVoicemailSettingsForPersonResponse(ApiModel):
    #: Voicemail is enabled or disabled.
    enabled: Optional[bool]
    #: Settings for sending all calls to voicemail.
    send_all_calls: Optional[SendAllCalls]
    #: Settings for sending calls to voicemail when the line is busy.
    send_busy_calls: Optional[SendBusyCalls]
    send_unanswered_calls: Optional[SendUnansweredCalls]
    #: Settings for notifications when there are any new voicemails.
    notifications: Optional[NewNumber]
    #: Settings for voicemail caller to transfer to a different number by pressing zero (0).
    transfer_to_number: Optional[NewNumber]
    #: Settings for sending a copy of new voicemail message audio via email.
    email_copy_of_message: Optional[EmailCopyOfMessage]
    message_storage: Optional[MessageStorage3]
    fax_message: Optional[FaxMessage]


class ScheduleShortDetails(Location1):
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[Type25]


class RecurWeekly2(RecurWeeklyObject):
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int]


class Recurrence(ApiModel):
    #: True if the event repeats forever. Requires either recurDaily or recurWeekly to be specified.
    recur_for_ever: Optional[bool]
    #: End date for the recurring event in the format of YYYY-MM-DD. Requires either recurDaily or recurWeekly to be
    #: specified.
    recur_end_date: Optional[str]
    #: End recurrence after the event has repeated the specified number of times. Requires either recurDaily or
    #: recurWeekly to be specified.
    recur_end_occurrence: Optional[int]
    #: Specifies the number of days between the start of each recurrence. Not allowed with recurWeekly.
    #: Recurring interval in days. The number of days after the start when an event will repeat. Repetitions cannot
    #: overlap.
    recur_daily: Optional[object]
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with recurDaily.
    recur_weekly: Optional[RecurWeekly2]


class EventLongDetails(ApiModel):
    #: Name for the event.
    name: Optional[str]
    #: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This field is required
    #: if the allDayEnabled field is present.
    start_date: Optional[str]
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This field is required if
    #: the allDayEnabled field is present.
    end_date: Optional[str]
    #: Start time of the event in the format of HH:MM (24 hours format). This field is required if the allDayEnabled
    #: field is false or omitted.
    start_time: Optional[str]
    #: End time of the event in the format of HH:MM (24 hours format). This field is required if the allDayEnabled
    #: field is false or omitted.
    end_time: Optional[str]
    #: True if it is all-day event.
    all_day_enabled: Optional[bool]
    #: Recurrance scheme for an event.
    recurrence: Optional[Recurrence]


class CreateScheduleForPersonBody(ApiModel):
    #: Name for the schedule.
    name: Optional[str]
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[Type25]
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    id: Optional[str]
    #: Last name of the monitored person, workspace or virtual line.
    last_name: Optional[str]
    #: First name of the monitored person, workspace or virtual line.
    first_name: Optional[str]
    #: Display name of the monitored person, workspace or virtual line.
    display_name: Optional[str]
    #: Indicates whether type is person, workspace or virtual line.
    type: Optional[Type8]
    #: Email address of the monitored person, workspace or virtual line.
    email: Optional[str]
    #: List of phone numbers of the monitored person, workspace or virtual line.
    numbers: Optional[list[GetUserNumberItemObject]]


class Member(MonitoredMemberObject):
    #: The location name where the call park extension is.
    location: Optional[str]
    #: The ID for the location.
    location_id: Optional[str]


class Callparkextension(ListCPCallParkExtensionObject):
    #: The location name where the call park extension is.
    location: Optional[str]
    #: The ID for the location.
    location_id: Optional[str]


class GetMonitoredElementsObject(ApiModel):
    member: Optional[Member]
    callparkextension: Optional[Callparkextension]


class PhoneNumbers7(ApiModel):
    #: Flag to indicate if the number is primary or not.
    #: Possible values:
    primary: Optional[bool]
    #: Phone number.
    #: Possible values: 2143456789
    direct_number: Optional[str]
    #: Extension.
    #: Possible values: 1234
    extension: Optional[str]
    #: Optional ring pattern. Applicable only for alternate numbers.
    #: Possible values: NORMAL, LONG_LONG, SHORT_SHORT_LONG, SHORT_LONG_SHORT
    ring_pattern: Optional[str]


class ModifypersonsApplicationServicesSettingsBody(ApiModel):
    #: When true, indicates to ring devices for outbound Click to Dial calls.
    ring_devices_for_click_to_dial_calls_enabled: Optional[bool]
    #: When true, indicates to ring devices for inbound Group Pages.
    ring_devices_for_group_page_enabled: Optional[bool]
    #: When true, indicates to ring devices for Call Park recalled.
    ring_devices_for_call_park_enabled: Optional[bool]
    #: Indicates that the browser Webex Calling application is enabled for use.
    browser_client_enabled: Optional[bool]
    #: Indicates that the desktop Webex Calling application is enabled for use.
    desktop_client_enabled: Optional[bool]
    #: Indicates that the tablet Webex Calling application is enabled for use.
    tablet_client_enabled: Optional[bool]
    #: Indicates that the mobile Webex Calling application is enabled for use.
    mobile_client_enabled: Optional[bool]


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    id: Optional[str]
    #: Last name of the person.
    last_name: Optional[str]
    #: First name of the person.
    first_name: Optional[str]
    #: Display name of the person.
    display_name: Optional[str]
    #: Type usually indicates PEOPLE, PLACE or VIRTUAL_LINE. Push-to-Talk and Privacy features only supports PEOPLE.
    type: Optional[Type8]
    #: Email address of the person.
    email: Optional[str]
    #: List of phone numbers of the person.
    numbers: Optional[list[GetUserNumberItemObject]]


class Type34(str, Enum):
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class PushToTalkConnectionType(ApiModel):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way: Optional[str]
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk
    #: for can respond.
    two_way: Optional[str]


class PushToTalkAccessType(ApiModel):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members: Optional[str]
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members: Optional[str]


class ExternalTransfer(str, Enum):
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class ReadIncomingPermissionSettingsForPersonResponse(ApiModel):
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather
    #: than the organizational defaults.
    use_custom_enabled: Optional[bool]
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: Optional[ExternalTransfer]
    #: Internal calls are allowed to be received.
    internal_calls_enabled: Optional[bool]
    #: Collect calls are allowed to be received.
    collect_calls_enabled: Optional[bool]


class CallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: Possible values: INTERNAL_CALL, TOLL_FREE, INTERNATIONAL, OPERATOR_ASSISTED, CHARGEABLE_DIRECTORY_ASSISTED,
    #: SPECIAL_SERVICES_I, SPECIAL_SERVICES_II, PREMIUM_SERVICES_I, PREMIUM_SERVICES_II, NATIONAL
    call_type: Optional[str]
    #: Action on the given callType.
    #: Possible values: ALLOW, BLOCK, AUTH_CODE, TRANSFER_NUMBER_1, TRANSFER_NUMBER_2, TRANSFER_NUMBER_3
    action: Optional[str]
    #: Allow the person to transfer or forward a call of the specified call type.
    #: Possible values:
    transfer_enabled: Optional[bool]


class RetrievepersonsOutgoingCallingPermissionsSettingsResponse(ApiModel):
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    use_custom_enabled: Optional[bool]
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[CallingPermissions]]


class PhoneNumber(ApiModel):
    #: If true marks the phone number as primary.
    primary: Optional[bool]
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[DialPatternAction]
    #: Phone numbers that are assigned.
    direct_number: Optional[str]
    #: Extension that is assigned.
    extension: Optional[str]
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern]


class CallQueueObject(ListCPCallParkExtensionObject):
    #: When not null, indicates the Call Queue's phone number.
    phone_number: Optional[str]


class SearchSharedLineAppearanceMembersBody(GetDetailsForCallParkExtensionResponse):
    #: Number of records per page.
    max: Optional[int]
    #: Page number.
    start: Optional[int]
    #: Location ID for the user.
    location: Optional[str]
    #: Search for users with numbers that match the query.
    number: Optional[str]
    #: Sort by first name (fname) or last name (lname).
    order: Optional[str]


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


class ReadPersonsCallingBehaviorResponse(ConfigurepersonsCallingBehaviorBody):
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if
    #: the user's behaviorType is set to null.
    effective_behavior_type: Optional[EffectiveBehaviorType]


class GetUserDevicesResponse(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]]
    #: Maximum number of devices a person can be assigned to.
    max_device_count: Optional[int]


class ReadCallRecordingSettingsForPersonResponse(ConfigureCallRecordingSettingsForPersonBody):
    #: Name of the service provider providing call recording service.
    service_provider: Optional[str]
    #: Group utilized by the service provider providing call recording service.
    external_group: Optional[str]
    #: Unique person identifier utilized by the service provider providing call recording service.
    external_identifier: Optional[str]


class ReadCallerIDSettingsForPersonResponse(ConfigureCallerIDSettingsForPersonBody):
    #: Allowed types for the selected field.
    types: Optional[list[CallerIdSelectedType]]
    #: Direct number which will be shown if DIRECT_LINE is selected.
    direct_number: Optional[str]
    #: Extension number which will be shown if DIRECT_LINE is selected.
    extension_number: Optional[str]
    #: Location number which will be shown if LOCATION_NUMBER is selected.
    location_number: Optional[str]
    #: Mobile number which will be shown if MOBILE_NUMBER is selected.
    mobile_number: Optional[str]
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool]
    #: Location's caller ID.
    location_external_caller_id_name: Optional[str]


class ListOfSchedulesForPersonResponse(ApiModel):
    #: Indicates a list of schedules.
    schedules: Optional[list[ScheduleShortDetails]]


class CreateScheduleForPersonResponse(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class GetScheduleDetailsResponse(ScheduleShortDetails):
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class UpdateScheduleBody1(CreateScheduleForPersonBody):
    #: New name for the schedule.
    new_name: Optional[str]


class UpdateScheduleResponse1(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class FetchEventForpersonsScheduleResponse(EventLongDetails):
    #: Identifier for a event.
    id: Optional[str]


class AddNewEventForPersonsScheduleResponse(ApiModel):
    #: Identifier for a event.
    id: Optional[str]


class UpdateEventForpersonsScheduleBody(EventLongDetails):
    #: New name for the event.
    new_name: Optional[str]


class UpdateEventForpersonsScheduleResponse(ApiModel):
    #: Identifier for a event.
    id: Optional[str]


class ReadCallWaitingSettingsForPersonResponse(ApiModel):
    #: true if the Call Waiting feature is enabled.
    enabled: Optional[bool]


class ConfigureCallWaitingSettingsForPersonBody(ApiModel):
    #: true if the Call Waiting feature is enabled.
    enabled: Optional[bool]


class RetrievepersonsMonitoringSettingsResponse(ApiModel):
    #: Call park notification is enabled or disabled.
    call_park_notification_enabled: Optional[bool]
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[GetMonitoredElementsObject]]


class ModifypersonsMonitoringSettingsBody(ApiModel):
    #: Enable or disable call park notification.
    enable_call_park_notification: Optional[bool]
    #: Identifiers of monitored elements whose monitoring settings will be modified.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
    monitored_elements: Optional[list[str]]


class GetListOfPhoneNumbersForPersonResponse(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    distinctive_ring_enabled: Optional[bool]
    #: Information about the number.
    phone_numbers: Optional[list[PhoneNumbers7]]


class RetrievepersonsApplicationServicesSettingsResponse(ModifypersonsApplicationServicesSettingsBody):
    #: Device ID of WebRTC client. Returns only if browserClientEnabled is true.
    browser_client_id: Optional[str]
    #: Device ID of Desktop client. Returns only if desktopClientEnabled is true.
    desktop_client_id: Optional[str]
    #: Number of available device licenses for assigning devices/apps.
    available_line_count: Optional[int]


class GetpersonsPrivacySettingsResponse(ApiModel):
    #: When true auto attendant extension dialing will be enabled.
    aa_extension_dialing_enabled: Optional[bool]
    #: When true auto attendant dailing by first or last name will be enabled.
    aa_naming_dialing_enabled: Optional[bool]
    #: When true phone status directory privacy will be enabled.
    enable_phone_status_directory_privacy: Optional[bool]
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]]


class ConfigurepersonsPrivacySettingsBody(ApiModel):
    #: When true auto attendant extension dialing is enabled.
    aa_extension_dialing_enabled: Optional[bool]
    #: When true auto attendant dailing by first or last name is enabled.
    aa_naming_dialing_enabled: Optional[bool]
    #: When true phone status directory privacy is enabled.
    enable_phone_status_directory_privacy: Optional[bool]
    #: List of monitoring person IDs.
    monitoring_agents: Optional[list[str]]


class RetrieveExecutiveAssistantSettingsForPersonResponse(ApiModel):
    #: Indicates the Executive Assistant type.
    type: Optional[Type34]


class ModifyExecutiveAssistantSettingsForPersonBody(ApiModel):
    #: executive assistant type
    type: Optional[Type34]


class ReadReceptionistClientSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Receptionist Client feature.
    reception_enabled: Optional[bool]
    #: List of people, workspaces or virtual lines to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]]


class ConfigureReceptionistClientSettingsForPersonBody(ApiModel):
    #: true if the Receptionist Client feature is enabled.
    reception_enabled: Optional[bool]
    #: List of members' unique identifiers to monitor.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    monitored_members: Optional[list[str]]


class ReadPushtoTalkSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Push-to-Talk feature. When enabled, a person receives a Push-to-Talk call and answers
    #: the call automatically.
    allow_auto_answer: Optional[bool]
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType]
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType]
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredPersonObject]]


class ConfigurePushtoTalkSettingsForPersonBody(ApiModel):
    #: true if Push-to-Talk feature is enabled.
    allow_auto_answer: Optional[bool]
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType]
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType]
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    members: Optional[list[str]]


class ReadHotelingSettingsForPersonResponse(ApiModel):
    #: When true, allow this person to connect to a Hoteling host device.
    enabled: Optional[bool]


class ConfigureHotelingSettingsForPersonBody(ApiModel):
    #: When true, allow this person to connect to a Hoteling host device.
    enabled: Optional[bool]


class AssignOrUnassignNumbersTopersonBody(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    enable_distinctive_ring_pattern: Optional[bool]
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]]


class RetrieveListOfCallQueueCallerIDInformationResponse(ApiModel):
    #: Indicates a list of Call Queues that the agent belongs and are available to be selected as the Caller ID for
    #: outgoing calls. It is empty when the agent's Call Queues have disabled the Call Queue outgoing phone number
    #: setting to be used as Caller ID. In the case where this setting is enabled the array will be populated.
    available_queues: Optional[list[CallQueueObject]]


class RetrieveCallQueueAgentsCallerIDInformationResponse(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it
    #: is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when
    #: queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[CallQueueObject]


class ModifyCallQueueAgentsCallerIDInformationBody(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it
    #: is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when
    #: queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[Location1]


class WebexCallingPersonSettingsApi(ApiChild, base=''):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Person Settings supports modifying Webex Calling settings for a specific person.
    Viewing People requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
    or, for select APIs, a user auth token with spark:people_read scope can be used by a person to read their own
    settings.
    Configuring People settings requires a full or user administrator auth token with the spark-admin:people_write
    scope or, for select APIs, a user auth token with spark:people_write scope can be used by a person to update their
    own settings.
    """

    def search_shared_line_appearance_members(self, person_id: str, application_id: str, extension: str = None, name: str = None, max: int = None, start: int = None, location: str = None, number: str = None, order: str = None) -> list[AvailableSharedLineMemberItem]:
        """
        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param extension: The extension for the call park extension.
        :type extension: str
        :param name: Unique name for the call park extension.
        :type name: str
        :param max: Number of records per page.
        :type max: int
        :param start: Page number.
        :type start: int
        :param location: Location ID for the user.
        :type location: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (fname) or last name (lname).
        :type order: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/search-shared-line-appearance-members
        """
        body = SearchSharedLineAppearanceMembersBody()
        if extension is not None:
            body.extension = extension
        if name is not None:
            body.name = name
        if max is not None:
            body.max = max
        if start is not None:
            body.start = start
        if location is not None:
            body.location = location
        if number is not None:
            body.number = number
        if order is not None:
            body.order = order
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/availableMembers')
        data = super().get(url=url, data=body.json())
        return parse_obj_as(list[AvailableSharedLineMemberItem], data["members"])

    def shared_line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineAppearanceMembersResponse:
        """
        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/get-shared-line-appearance-members
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        data = super().get(url=url)
        return GetSharedLineAppearanceMembersResponse.parse_obj(data)

    def put_shared_line_appearance_members(self, person_id: str, application_id: str, members: PutSharedLineMemberItem = None):
        """
        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param members: 
        :type members: PutSharedLineMemberItem

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/put-shared-line-appearance-members
        """
        body = PutSharedLineAppearanceMembersBody()
        if members is not None:
            body.members = members
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        super().put(url=url, data=body.json())
        return

    def read_persons_calling_behavior(self, person_id: str, org_id: str = None) -> ReadPersonsCallingBehaviorResponse:
        """
        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-person's-calling-behavior
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        data = super().get(url=url, params=params)
        return ReadPersonsCallingBehaviorResponse.parse_obj(data)

    def configurepersons_calling_behavior(self, person_id: str, org_id: str = None, behavior_type: BehaviorType = None, profile_id: str = None):
        """
        Modifies the calling behavior settings for the person which includes calling behavior and UC Manager Profile
        ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used
        for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual
        persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param behavior_type: The new Calling Behavior setting for the person (case-insensitive). If null, the
            effective Calling Behavior will be the Organization's current default.
        :type behavior_type: BehaviorType
        :param profile_id: The UC Manager Profile ID. Specifying null results in the organizational default being
            applied.
        :type profile_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-a-person's-calling-behavior
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurepersonsCallingBehaviorBody()
        if behavior_type is not None:
            body.behavior_type = behavior_type
        if profile_id is not None:
            body.profile_id = profile_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        super().put(url=url, params=params, data=body.json())
        return

    def read_barge_in_for_person(self, person_id: str, org_id: str = None) -> ReadBargeInSettingsForPersonResponse:
        """
        Retrieve a person's Barge In settings.
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-barge-in-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/bargeIn')
        data = super().get(url=url, params=params)
        return ReadBargeInSettingsForPersonResponse.parse_obj(data)

    def configure_barge_in_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, tone_enabled: bool = None):
        """
        Configure a person's Barge In settings.
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: Indicates if the Barge In feature is enabled.
        :type enabled: bool
        :param tone_enabled: Indicates that a stutter dial tone will be played when a person is barging in on the
            active call.
        :type tone_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-barge-in-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadBargeInSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if tone_enabled is not None:
            body.tone_enabled = tone_enabled
        url = self.ep(f'people/{person_id}/features/bargeIn')
        super().put(url=url, params=params, data=body.json())
        return

    def read_forwarding_for_person(self, person_id: str, org_id: str = None) -> ReadForwardingSettingsForPersonResponse:
        """
        Retrieve a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-forwarding-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return ReadForwardingSettingsForPersonResponse.parse_obj(data)

    def configure_call_forwarding_for_person(self, person_id: str, org_id: str = None, call_forwarding: CallForwarding4 = None, business_continuity: BusinessContinuity = None):
        """
        Configure a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwarding4
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: BusinessContinuity

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-call-forwarding-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadForwardingSettingsForPersonResponse()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        if business_continuity is not None:
            body.business_continuity = business_continuity
        url = self.ep(f'people/{person_id}/features/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def user_devices(self, person_id: str, org_id: str = None) -> GetUserDevicesResponse:
        """
        Get all devices for a person.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/get-user-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/devices')
        data = super().get(url=url, params=params)
        return GetUserDevicesResponse.parse_obj(data)

    def read_call_intercept_for_person(self, person_id: str, org_id: str = None) -> GetLocationInterceptResponse:
        """
        Retrieves Person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-call-intercept-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/intercept')
        data = super().get(url=url, params=params)
        return GetLocationInterceptResponse.parse_obj(data)

    def configure_call_intercept_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, incoming: Incoming = None, outgoing: Outgoing = None):
        """
        Configures a person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: Enable/disable location intercept. Enable this feature to override any Location's Call
            Intercept settings that person configures.
        :type enabled: bool
        :param incoming: Inbound call details.
        :type incoming: Incoming
        :param outgoing: Outbound Call details
        :type outgoing: Outgoing

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-call-intercept-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetLocationInterceptResponse()
        if enabled is not None:
            body.enabled = enabled
        if incoming is not None:
            body.incoming = incoming
        if outgoing is not None:
            body.outgoing = outgoing
        url = self.ep(f'people/{person_id}/features/intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def configure_call_intercept_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Call Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-call-intercept-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/intercept/actions/announcementUpload/invoke')
        super().post(url=url, params=params)
        return

    def read_call_recording_for_person(self, person_id: str, org_id: str = None) -> ReadCallRecordingSettingsForPersonResponse:
        """
        Retrieve a person's Call Recording settings.
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-call-recording-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callRecording')
        data = super().get(url=url, params=params)
        return ReadCallRecordingSettingsForPersonResponse.parse_obj(data)

    def configure_call_recording_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, record: Record = None, record_voicemail_enabled: bool = None, start_stop_announcement_enabled: bool = None, notification: Notification = None, repeat: Repeat = None):
        """
        Configure a person's Call Recording settings.
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: true if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: Record
        :param record_voicemail_enabled: When true, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param start_stop_announcement_enabled: When enabled, an announcement is played when call recording starts and
            an announcement is played when call recording ends.
        :type start_stop_announcement_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: Notification
        :param repeat: Beep sound plays periodically.
        :type repeat: Repeat

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-call-recording-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallRecordingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        if record is not None:
            body.record = record
        if record_voicemail_enabled is not None:
            body.record_voicemail_enabled = record_voicemail_enabled
        if start_stop_announcement_enabled is not None:
            body.start_stop_announcement_enabled = start_stop_announcement_enabled
        if notification is not None:
            body.notification = notification
        if repeat is not None:
            body.repeat = repeat
        url = self.ep(f'people/{person_id}/features/callRecording')
        super().put(url=url, params=params, data=body.json())
        return

    def read_caller_id_for_person(self, person_id: str, org_id: str = None) -> ReadCallerIDSettingsForPersonResponse:
        """
        Retrieve a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-caller-id-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callerId')
        data = super().get(url=url, params=params)
        return ReadCallerIDSettingsForPersonResponse.parse_obj(data)

    def configure_caller_id_for_person(self, person_id: str, org_id: str = None, selected: CallerIdSelectedType = None, custom_number: str = None, first_name: str = None, last_name: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: ExternalCallerIdNamePolicy = None, custom_external_caller_id_name: str = None):
        """
        Configure a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used. Possible values: DIRECT_LINE
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name. Characters of %, +, ``, " and Unicode characters are not
            allowed.
        :type first_name: str
        :param last_name: Person's Caller ID last name. Characters of %, +, ``, " and Unicode characters are not
            allowed.
        :type last_name: str
        :param block_in_forward_calls_enabled: true if person's identity has to be blocked when receiving a transferred
            or forwarded call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller Id Name policy is used. Default
            is DIRECT_LINE.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Person's custom External Caller ID last name. Characters of %, +, ``, "
            and Unicode characters are not allowed.
        :type custom_external_caller_id_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-caller-id-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallerIDSettingsForPersonBody()
        if selected is not None:
            body.selected = selected
        if custom_number is not None:
            body.custom_number = custom_number
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if block_in_forward_calls_enabled is not None:
            body.block_in_forward_calls_enabled = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body.external_caller_id_name_policy = external_caller_id_name_policy
        if custom_external_caller_id_name is not None:
            body.custom_external_caller_id_name = custom_external_caller_id_name
        url = self.ep(f'people/{person_id}/features/callerId')
        super().put(url=url, params=params, data=body.json())
        return

    def read_do_not_disturb_for_person(self, person_id: str, org_id: str = None) -> ReadDoNotDisturbSettingsForPersonResponse:
        """
        Retrieve a person's Do Not Disturb settings.
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-do-not-disturb-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        data = super().get(url=url, params=params)
        return ReadDoNotDisturbSettingsForPersonResponse.parse_obj(data)

    def configure_do_not_disturb_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, ring_splash_enabled: bool = None):
        """
        Configure a person's Do Not Disturb settings.
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: true if the Do Not Disturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive
            incoming calls.
        :type ring_splash_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-do-not-disturb-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadDoNotDisturbSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if ring_splash_enabled is not None:
            body.ring_splash_enabled = ring_splash_enabled
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        super().put(url=url, params=params, data=body.json())
        return

    def read_voicemail_for_person(self, person_id: str, org_id: str = None) -> ReadVoicemailSettingsForPersonResponse:
        """
        Retrieve a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-voicemail-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail')
        data = super().get(url=url, params=params)
        return ReadVoicemailSettingsForPersonResponse.parse_obj(data)

    def configure_voicemail_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, send_all_calls: SendAllCalls = None, send_busy_calls: SendBusyCalls = None, send_unanswered_calls: SendUnansweredCalls = None, notifications: NewNumber = None, transfer_to_number: NewNumber = None, email_copy_of_message: EmailCopyOfMessage = None, message_storage: MessageStorage3 = None, fax_message: FaxMessage = None):
        """
        Configure a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
        :type send_all_calls: SendAllCalls
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: SendBusyCalls
        :param send_unanswered_calls: 
        :type send_unanswered_calls: SendUnansweredCalls
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: NewNumber
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero
            (0).
        :type transfer_to_number: NewNumber
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: EmailCopyOfMessage
        :param message_storage: 
        :type message_storage: MessageStorage3
        :param fax_message: 
        :type fax_message: FaxMessage

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-voicemail-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadVoicemailSettingsForPersonResponse()
        if enabled is not None:
            body.enabled = enabled
        if send_all_calls is not None:
            body.send_all_calls = send_all_calls
        if send_busy_calls is not None:
            body.send_busy_calls = send_busy_calls
        if send_unanswered_calls is not None:
            body.send_unanswered_calls = send_unanswered_calls
        if notifications is not None:
            body.notifications = notifications
        if transfer_to_number is not None:
            body.transfer_to_number = transfer_to_number
        if email_copy_of_message is not None:
            body.email_copy_of_message = email_copy_of_message
        if message_storage is not None:
            body.message_storage = message_storage
        if fax_message is not None:
            body.fax_message = fax_message
        url = self.ep(f'people/{person_id}/features/voicemail')
        super().put(url=url, params=params, data=body.json())
        return

    def configure_busy_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-busy-voicemail-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url=url, params=params)
        return

    def configure_no_answer_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded
        audio file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-no-answer-voicemail-greeting-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadNoAnswerGreeting/invoke')
        super().post(url=url, params=params)
        return

    def list_of_schedules_for_person(self, person_id: str, org_id: str = None, name: str = None, type_: str = None, **params) -> Generator[ScheduleShortDetails, None, None]:
        """
        List schedules for a person in an organization.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param name: Specifies the case insensitive substring to be matched against the schedule names. The maximum
            length is 40.
        :type name: str
        :param type_: Specifies the schedule event type to be matched on the given type.
        :type type_: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/list-of-schedules-for-a-person
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if type_ is not None:
            params['type'] = type_
        url = self.ep(f'people/{person_id}/features/schedules')
        return self.session.follow_pagination(url=url, model=ScheduleShortDetails, item_key='schedules', params=params)

    def create_schedule_for_person(self, person_id: str, name: str, type_: Type25, org_id: str = None, events: EventLongDetails = None) -> str:
        """
        Create a new schedule for a person.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: Type25
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param events: Indicates a list of events.
        :type events: EventLongDetails

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/create-schedule-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = CreateScheduleForPersonBody()
        if name is not None:
            body.name = name
        if type_ is not None:
            body.type_ = type_
        if events is not None:
            body.events = events
        url = self.ep(f'people/{person_id}/features/schedules')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def schedule_details(self, person_id: str, schedule_type: Type25, schedule_id: str, org_id: str = None) -> GetScheduleDetailsResponse:
        """
        Retrieve a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/get-a-schedule-details
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url=url, params=params)
        return GetScheduleDetailsResponse.parse_obj(data)

    def update_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, name: str, type_: Type25, new_name: str, org_id: str = None, events: EventLongDetails = None) -> str:
        """
        Modify a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: Type25
        :param new_name: New name for the schedule.
        :type new_name: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param events: Indicates a list of events.
        :type events: EventLongDetails

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/update-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateScheduleBody1()
        if name is not None:
            body.name = name
        if type_ is not None:
            body.type_ = type_
        if new_name is not None:
            body.new_name = new_name
        if events is not None:
            body.events = events
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, org_id: str = None):
        """
        Delete a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/delete-a-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        super().delete(url=url, params=params)
        return

    def fetch_event_forpersons_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, event_id: str, org_id: str = None) -> FetchEventForpersonsScheduleResponse:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/fetch-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().get(url=url, params=params)
        return FetchEventForpersonsScheduleResponse.parse_obj(data)

    def add_new_event_for_persons_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, name: str, start_date: str, end_date: str, start_time: str, end_time: str, org_id: str = None, all_day_enabled: bool = None, recurrence: Recurrence = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format). This field is required if
            the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format). This field is required if the
            allDayEnabled field is false or omitted.
        :type end_time: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: Recurrence

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/add-a-new-event-for-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = EventLongDetails()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events')
        data = super().post(url=url, params=params, data=body.json())
        return data["id"]

    def update_event_forpersons_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, event_id: str, name: str, start_date: str, end_date: str, start_time: str, end_time: str, new_name: str, org_id: str = None, all_day_enabled: bool = None, recurrence: Recurrence = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This
            field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format). This field is required if
            the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format). This field is required if the
            allDayEnabled field is false or omitted.
        :type end_time: str
        :param new_name: New name for the event.
        :type new_name: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: Recurrence

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/update-an-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = UpdateEventForpersonsScheduleBody()
        if name is not None:
            body.name = name
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if start_time is not None:
            body.start_time = start_time
        if end_time is not None:
            body.end_time = end_time
        if new_name is not None:
            body.new_name = new_name
        if all_day_enabled is not None:
            body.all_day_enabled = all_day_enabled
        if recurrence is not None:
            body.recurrence = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().put(url=url, params=params, data=body.json())
        return data["id"]

    def delete_event_forpersons_schedule(self, person_id: str, schedule_type: Type25, schedule_id: str, event_id: str, org_id: str = None):
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by
        defining one or more events. holidays schedules define exceptions to normal business hours by defining one or
        more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type25
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/delete-an-event-for-a-person's-schedule
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        super().delete(url=url, params=params)
        return

    def read_call_waiting_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's Call Waiting settings.
        With this feature, a person can place an active call on hold and answer an incoming call. When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-call-waiting-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_call_waiting_for_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure a person's Call Waiting settings.
        With this feature, a person can place an active call on hold and answer an incoming call. When enabled, while
        you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the
        call.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-call-waiting-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallWaitingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'people/{person_id}/features/callWaiting')
        super().put(url=url, params=params, data=body.json())
        return

    def retrievepersons_monitoring(self, person_id: str, org_id: str = None) -> RetrievepersonsMonitoringSettingsResponse:
        """
        Retrieves the monitoring settings of the person, which shows specified people, places, virtual lines or call
        park extenions that are being monitored.
        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-a-person's-monitoring-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/monitoring')
        data = super().get(url=url, params=params)
        return RetrievepersonsMonitoringSettingsResponse.parse_obj(data)

    def modifypersons_monitoring(self, person_id: str, enable_call_park_notification: bool, monitored_elements: List[str], org_id: str = None):
        """
        Modifies the monitoring settings of the person.
        Monitors the line status of specified people, places, virtual lines or call park extension. The line status
        indicates if a person, place or virtual line is on a call and if a call has been parked on that extension.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
        :type monitored_elements: List[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/modify-a-person's-monitoring-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsMonitoringSettingsBody()
        if enable_call_park_notification is not None:
            body.enable_call_park_notification = enable_call_park_notification
        if monitored_elements is not None:
            body.monitored_elements = monitored_elements
        url = self.ep(f'people/{person_id}/features/monitoring')
        super().put(url=url, params=params, data=body.json())
        return

    def list_of_phone_numbers_for_person(self, person_id: str, org_id: str = None, prefer_e164_format: bool = None) -> GetListOfPhoneNumbersForPersonResponse:
        """
        Get a person's phone numbers including alternate numbers.
        A person can have one or more phone numbers and/or extensions via which they can be called.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param prefer_e164_format: Return phone numbers in E.164 format.
        :type prefer_e164_format: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/get-a-list-of-phone-numbers-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if prefer_e164_format is not None:
            params['preferE164Format'] = str(prefer_e164_format).lower()
        url = self.ep(f'people/{person_id}/features/numbers')
        data = super().get(url=url, params=params)
        return GetListOfPhoneNumbersForPersonResponse.parse_obj(data)

    def retrievepersons_application_services(self, person_id: str, org_id: str = None) -> RetrievepersonsApplicationServicesSettingsResponse:
        """
        Application services let you determine the ringing behavior for calls made to people in certain scenarios. You
        can also specify which devices can download the Webex Calling app.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-a-person's-application-services-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/applications')
        data = super().get(url=url, params=params)
        return RetrievepersonsApplicationServicesSettingsResponse.parse_obj(data)

    def modifypersons_application_services(self, person_id: str, org_id: str = None, ring_devices_for_click_to_dial_calls_enabled: bool = None, ring_devices_for_group_page_enabled: bool = None, ring_devices_for_call_park_enabled: bool = None, browser_client_enabled: bool = None, desktop_client_enabled: bool = None, tablet_client_enabled: bool = None, mobile_client_enabled: bool = None):
        """
        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param ring_devices_for_click_to_dial_calls_enabled: When true, indicates to ring devices for outbound Click to
            Dial calls.
        :type ring_devices_for_click_to_dial_calls_enabled: bool
        :param ring_devices_for_group_page_enabled: When true, indicates to ring devices for inbound Group Pages.
        :type ring_devices_for_group_page_enabled: bool
        :param ring_devices_for_call_park_enabled: When true, indicates to ring devices for Call Park recalled.
        :type ring_devices_for_call_park_enabled: bool
        :param browser_client_enabled: Indicates that the browser Webex Calling application is enabled for use.
        :type browser_client_enabled: bool
        :param desktop_client_enabled: Indicates that the desktop Webex Calling application is enabled for use.
        :type desktop_client_enabled: bool
        :param tablet_client_enabled: Indicates that the tablet Webex Calling application is enabled for use.
        :type tablet_client_enabled: bool
        :param mobile_client_enabled: Indicates that the mobile Webex Calling application is enabled for use.
        :type mobile_client_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/modify-a-person's-application-services-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsApplicationServicesSettingsBody()
        if ring_devices_for_click_to_dial_calls_enabled is not None:
            body.ring_devices_for_click_to_dial_calls_enabled = ring_devices_for_click_to_dial_calls_enabled
        if ring_devices_for_group_page_enabled is not None:
            body.ring_devices_for_group_page_enabled = ring_devices_for_group_page_enabled
        if ring_devices_for_call_park_enabled is not None:
            body.ring_devices_for_call_park_enabled = ring_devices_for_call_park_enabled
        if browser_client_enabled is not None:
            body.browser_client_enabled = browser_client_enabled
        if desktop_client_enabled is not None:
            body.desktop_client_enabled = desktop_client_enabled
        if tablet_client_enabled is not None:
            body.tablet_client_enabled = tablet_client_enabled
        if mobile_client_enabled is not None:
            body.mobile_client_enabled = mobile_client_enabled
        url = self.ep(f'people/{person_id}/features/applications')
        super().put(url=url, params=params, data=body.json())
        return

    def getpersons_privacy(self, person_id: str, org_id: str = None) -> GetpersonsPrivacySettingsResponse:
        """
        Get a person's privacy settings for the specified person ID.
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/get-a-person's-privacy-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/privacy')
        data = super().get(url=url, params=params)
        return GetpersonsPrivacySettingsResponse.parse_obj(data)

    def configurepersons_privacy(self, person_id: str, org_id: str = None, aa_extension_dialing_enabled: bool = None, aa_naming_dialing_enabled: bool = None, enable_phone_status_directory_privacy: bool = None, monitoring_agents: List[str] = None):
        """
        Configure a person's privacy settings for the specified person ID.
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param aa_extension_dialing_enabled: When true auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When true auto attendant dailing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When true phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-a-person's-privacy-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurepersonsPrivacySettingsBody()
        if aa_extension_dialing_enabled is not None:
            body.aa_extension_dialing_enabled = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body.aa_naming_dialing_enabled = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body.enable_phone_status_directory_privacy = enable_phone_status_directory_privacy
        if monitoring_agents is not None:
            body.monitoring_agents = monitoring_agents
        url = self.ep(f'people/{person_id}/features/privacy')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_executive_assistant_for_person(self, person_id: str, org_id: str = None) -> Type34:
        """
        Retrieve the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the
        call forward destination and join or leave an executive's pool.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-executive-assistant-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        data = super().get(url=url, params=params)
        return Type34.parse_obj(data["type"])

    def modify_executive_assistant_for_person(self, person_id: str, org_id: str = None, type_: Type34 = None):
        """
        Modify the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the
        call forward destination and join or leave an executive's pool.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param type_: executive assistant type
        :type type_: Type34

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/modify-executive-assistant-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyExecutiveAssistantSettingsForPersonBody()
        if type_ is not None:
            body.type_ = type_
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        super().put(url=url, params=params, data=body.json())
        return

    def read_receptionist_client_for_person(self, person_id: str, org_id: str = None) -> ReadReceptionistClientSettingsForPersonResponse:
        """
        Retrieve a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-receptionist-client-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/reception')
        data = super().get(url=url, params=params)
        return ReadReceptionistClientSettingsForPersonResponse.parse_obj(data)

    def configure_receptionist_client_for_person(self, person_id: str, reception_enabled: bool, org_id: str = None, monitored_members: List[str] = None):
        """
        Configure a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param reception_enabled: true if the Receptionist Client feature is enabled.
        :type reception_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param monitored_members: List of members' unique identifiers to monitor. Possible values:
            Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
        :type monitored_members: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-receptionist-client-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureReceptionistClientSettingsForPersonBody()
        if reception_enabled is not None:
            body.reception_enabled = reception_enabled
        if monitored_members is not None:
            body.monitored_members = monitored_members
        url = self.ep(f'people/{person_id}/features/reception')
        super().put(url=url, params=params, data=body.json())
        return

    def read_push_to_talk_for_person(self, person_id: str, org_id: str = None) -> ReadPushtoTalkSettingsForPersonResponse:
        """
        Retrieve a person's Push-to-Talk settings.
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-push-to-talk-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        data = super().get(url=url, params=params)
        return ReadPushtoTalkSettingsForPersonResponse.parse_obj(data)

    def configure_push_to_talk_for_person(self, person_id: str, org_id: str = None, allow_auto_answer: bool = None, connection_type: PushToTalkConnectionType = None, access_type: PushToTalkAccessType = None, members: List[str] = None):
        """
        Configure a person's Push-to-Talk settings.
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param allow_auto_answer: true if Push-to-Talk feature is enabled.
        :type allow_auto_answer: bool
        :param connection_type: Specifies the connection type to be used.
        :type connection_type: PushToTalkConnectionType
        :param access_type: Specifies the access type to be applied when evaluating the member list.
        :type access_type: PushToTalkAccessType
        :param members: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
        :type members: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-push-to-talk-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigurePushtoTalkSettingsForPersonBody()
        if allow_auto_answer is not None:
            body.allow_auto_answer = allow_auto_answer
        if connection_type is not None:
            body.connection_type = connection_type
        if access_type is not None:
            body.access_type = access_type
        if members is not None:
            body.members = members
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        super().put(url=url, params=params, data=body.json())
        return

    def read_hoteling_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-hoteling-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/hoteling')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_hoteling_for_person(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-hoteling-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureHotelingSettingsForPersonBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'people/{person_id}/features/hoteling')
        super().put(url=url, params=params, data=body.json())
        return

    def reset_voicemail_pin(self, person_id: str, org_id: str = None):
        """
        Reset a voicemail PIN for a person.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.
        NOTE: This API is expected to have an empty request body and Content-Type header should be set to
        application/json.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/reset-voicemail-pin
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/resetPin/invoke')
        super().post(url=url, params=params)
        return

    def read_incoming_permission_for_person(self, person_id: str, org_id: str = None) -> ReadIncomingPermissionSettingsForPersonResponse:
        """
        Retrieve a person's Incoming Permission settings.
        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/read-incoming-permission-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        data = super().get(url=url, params=params)
        return ReadIncomingPermissionSettingsForPersonResponse.parse_obj(data)

    def configure_incoming_permission_for_person(self, person_id: str, org_id: str = None, use_custom_enabled: bool = None, external_transfer: ExternalTransfer = None, internal_calls_enabled: bool = None, collect_calls_enabled: bool = None):
        """
        Configure a person's Incoming Permission settings.
        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for
            receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: ExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/configure-incoming-permission-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadIncomingPermissionSettingsForPersonResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if external_transfer is not None:
            body.external_transfer = external_transfer
        if internal_calls_enabled is not None:
            body.internal_calls_enabled = internal_calls_enabled
        if collect_calls_enabled is not None:
            body.collect_calls_enabled = collect_calls_enabled
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrievepersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None) -> RetrievepersonsOutgoingCallingPermissionsSettingsResponse:
        """
        Retrieve a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-a-person's-outgoing-calling-permissions-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrievepersonsOutgoingCallingPermissionsSettingsResponse.parse_obj(data)

    def modifypersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None, use_custom_enabled: bool = None, calling_permissions: CallingPermissions = None):
        """
        Modify a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this user uses the specified calling permissions when
            placing outbound calls.
        :type use_custom_enabled: bool
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: CallingPermissions

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/modify-a-person's-outgoing-calling-permissions-settings
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = RetrievepersonsOutgoingCallingPermissionsSettingsResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def assign_or_unassign_numbers_toperson(self, person_id: str, phone_numbers: PhoneNumber, org_id: str = None, enable_distinctive_ring_pattern: bool = None):
        """
        Assign or unassign alternate phone numbers to a person.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.
        Assigning or unassigning an alternate phone number to a person requires a full administrator auth token with a
        scope of spark-admin:telephony_config_write.

        :param person_id: Unique identitfier of the person.
        :type person_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: PhoneNumber
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param enable_distinctive_ring_pattern: Enables a distinctive ring pattern for the person.
        :type enable_distinctive_ring_pattern: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/assign-or-unassign-numbers-to-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AssignOrUnassignNumbersTopersonBody()
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if enable_distinctive_ring_pattern is not None:
            body.enable_distinctive_ring_pattern = enable_distinctive_ring_pattern
        url = self.ep(f'telephony/config/people/{person_id}/numbers')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_list_of_call_queue_caller_id_information(self, person_id: str) -> list[CallQueueObject]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information.
        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for outgoing
        Caller ID. This API returns a list of Call Queues from which the person must select. If this setting is
        disabled or the Agent does not belong to any queue, this list will be empty.
        This API requires a full admin or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-list-of-call-queue-caller-id-information
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/availableCallerIds')
        data = super().get(url=url)
        return parse_obj_as(list[CallQueueObject], data["availableQueues"])

    def retrieve_call_queue_agents_caller_id_information(self, person_id: str) -> RetrieveCallQueueAgentsCallerIDInformationResponse:
        """
        Retrieve a call queue agent's Caller ID information.
        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone
        number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the
        system.
        This API requires a full admin or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/retrieve-a-call-queue-agent's-caller-id-information
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        data = super().get(url=url)
        return RetrieveCallQueueAgentsCallerIDInformationResponse.parse_obj(data)

    def modify_call_queue_agents_caller_id_information(self, person_id: str, queue_caller_id_enabled: bool, selected_queue: Location1):
        """
        Modify a call queue agent's Caller ID information.
        Each Agent in the Call Queue will be able to set their outgoing Caller ID as either the designated Call Queue's
        phone number or their own configured Caller ID. This API modifies the configured Caller ID for the agent in the
        system.
        This API requires a full or user administrator auth token with the spark-admin:telephony_config_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param queue_caller_id_enabled: When true, indicates that this agent is using the selectedQueue for its Caller
            ID. When false, indicates that it is using the agent's configured Caller ID.
        :type queue_caller_id_enabled: bool
        :param selected_queue: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty
            object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
        :type selected_queue: Location1

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/modify-a-call-queue-agent's-caller-id-information
        """
        body = ModifyCallQueueAgentsCallerIDInformationBody()
        if queue_caller_id_enabled is not None:
            body.queue_caller_id_enabled = queue_caller_id_enabled
        if selected_queue is not None:
            body.selected_queue = selected_queue
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        super().put(url=url, data=body.json())
        return

class ReadCallBridgeSettingsForPersonResponse(ApiModel):
    #: Indicates that a stutter dial tone will be played to all the participants when a person is bridged on the active
    #: shared line call.
    warning_tone_enabled: Optional[bool]


class ConfigureCallBridgeSettingsForPersonBody(ApiModel):
    #: Set to enable or disable a stutter dial tone being played to all the participants when a person is bridged on
    #: the active shared line call.
    warning_tone_enabled: Optional[bool]


class WebexCallingPersonSettingswithCallBridgeFeatureApi(ApiChild, base='telephony/config/people/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Person Settings supports modifying Webex Calling settings for a specific person.
    Viewing People requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
    or, for select APIs, a user auth token with spark:people_read scope can be used by a person to read their own
    settings.
    Configuring People settings requires a full or user administrator auth token with the spark-admin:people_write
    scope or, for select APIs, a user auth token with spark:people_write scope can be used by a person to update their
    own settings.
    """

    def read_bridge_settings_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's Call Bridge settings.
        This API requires a full, user or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-call-bridge-feature/read-call-bridge-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callBridge')
        data = super().get(url=url, params=params)
        return data["warningToneEnabled"]

    def configure_bridge_settings_for_person(self, person_id: str, org_id: str = None, warning_tone_enabled: bool = None):
        """
        Configure a person's Call Bridge settings.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :param warning_tone_enabled: Set to enable or disable a stutter dial tone being played to all the participants
            when a person is bridged on the active shared line call.
        :type warning_tone_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-call-bridge-feature/configure-call-bridge-settings-for-a-person
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ConfigureCallBridgeSettingsForPersonBody()
        if warning_tone_enabled is not None:
            body.warning_tone_enabled = warning_tone_enabled
        url = self.ep(f'{person_id}/features/callBridge')
        super().put(url=url, params=params, data=body.json())
        return

class CallForwardingPlaceSettingGet(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the
    #: workspace is busy.
    busy: Optional[BusinessContinuity]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[NoAnswer3]


class CallForwardingPlaceSettingPatch(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the
    #: workspace is busy.
    busy: Optional[BusinessContinuity]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[NoAnswer3]


class UserNumberItem(GetUserNumberItemObject):
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
    callparkextension: Optional[Callparkextension]
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser]


class InterceptAnnouncementsGet(ApiModel):
    #: Indicates that a system default message will be placed when incoming calls are intercepted.
    greeting: Optional[Greeting]
    #: Filename of the custom greeting. Is an empty string if no custom greeting has been uploaded.
    filename: Optional[str]
    #: Information about the new number announcement.
    new_number: Optional[NewNumber]
    #: Information about how the call will be handled if zero (0) is pressed.
    zero_transfer: Optional[NewNumber]


class InterceptIncomingGet(ApiModel):
    #: Indicated incoming calls are intercepted.
    type: Optional[Type19]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsGet]


class InterceptIncomingPatch(ApiModel):
    #: Indicated incoming calls are intercepted.
    type: Optional[Type19]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[Announcements3]


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


class RetrieveOutgoingPermissionSettingsForWorkspaceResponse(ApiModel):
    #: Outgoing Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool]
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermissionObject]]


class ModifyOutgoingPermissionSettingsForWorkspaceBody(ApiModel):
    #: Outgoing Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool]
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermissionObject]]


class RetrieveAccessCodesForWorkspaceResponse(ApiModel):
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AccessCodes]]


class ModifyAccessCodesForWorkspaceBody(ApiModel):
    #: Indicates access codes to delete.
    delete_codes: Optional[list[str]]


class ReadCallInterceptSettingsForWorkspaceResponse(ApiModel):
    #: true if call intercept is enabled.
    enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingGet]
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[Outgoing]


class ConfigureCallInterceptSettingsForWorkspaceBody(ApiModel):
    #: true if call interception is enabled.
    enabled: Optional[bool]
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingPatch]
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[Outgoing]


class WebexCallingPersonSettingswithCallingBehaviorApi(ApiChild, base='workspaces/'):
    """
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:workspaces_read, as the current set of APIs is designed to provide supplemental information for
    administrators utilizing Workspace Webex Calling APIs.
    Modifying these organization settings requires a full administrator auth token with a scope of
    spark-admin:workspaces_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query
    parameter.
    """

    def retrieve_callwarding_settings_workspace(self, workspace_id: str, org_id: str = None) -> CallForwardingPlaceSettingGet:
        """
        Retrieve Call Forwarding Settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return CallForwardingPlaceSettingGet.parse_obj(data["callForwarding"])

    def modify_callwarding_settings_workspace(self, workspace_id: str, call_forwarding: CallForwardingPlaceSettingPatch, org_id: str = None):
        """
        Modify call forwarding settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param call_forwarding: Call forwarding settings for a Workspace.
        :type call_forwarding: CallForwardingPlaceSettingPatch
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallForwardingSettingsForWorkspaceBody()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'{workspace_id}/features/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_call_waiting_settings_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-call-waiting-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def modify_call_waiting_settings_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None):
        """
        Modify Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param enabled: Call Waiting state.
        :type enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-call-waiting-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallWaitingSettingsForWorkspaceBody()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'{workspace_id}/features/callWaiting')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_caller_id_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveCallerIDSettingsForWorkspaceResponse:
        """
        Retrieve Caller ID Settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-caller-id-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callerId')
        data = super().get(url=url, params=params)
        return RetrieveCallerIDSettingsForWorkspaceResponse.parse_obj(data)

    def modify_caller_id_settings_workspace(self, workspace_id: str, selected: CLIDPolicySelection, org_id: str = None, custom_number: str = None, display_name: str = None, display_detail: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: ExternalCallerIdNamePolicy = None, custom_external_caller_id_name: str = None, location_external_caller_id_name: str = None):
        """
        Modify Caller ID settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CLIDPolicySelection
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param custom_number: This value must be an assigned number from the workspace's location.
        :type custom_number: str
        :param display_name: Workspace's caller ID display name.
        :type display_name: str
        :param display_detail: Workspace's caller ID display details.
        :type display_detail: str
        :param block_in_forward_calls_enabled: Flag to block call forwarding.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is DIRECT_LINE. Possible values: DIRECT_LINE
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller ID
            Name is OTHER.
        :type custom_external_caller_id_name: str
        :param location_external_caller_id_name: External Caller Name, which will be shown if External Caller ID Name
            is OTHER.
        :type location_external_caller_id_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-caller-id-settings-for-a-workspace
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
        url = self.ep(f'{workspace_id}/features/callerId')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_monitoring_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveMonitoringSettingsForWorkspaceResponse:
        """
        Retrieves Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-monitoring-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/monitoring')
        data = super().get(url=url, params=params)
        return RetrieveMonitoringSettingsForWorkspaceResponse.parse_obj(data)

    def modify_monitoring_settings_workspace(self, workspace_id: str, enable_call_park_notification: bool, monitored_elements: List[str], org_id: str = None):
        """
        Modify Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
        :type monitored_elements: List[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-monitoring-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsMonitoringSettingsBody()
        if enable_call_park_notification is not None:
            body.enable_call_park_notification = enable_call_park_notification
        if monitored_elements is not None:
            body.monitored_elements = monitored_elements
        url = self.ep(f'{workspace_id}/features/monitoring')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_incoming_permission_settings_workspace(self, workspace_id: str, org_id: str = None) -> ReadIncomingPermissionSettingsForPersonResponse:
        """
        Retrieve Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-incoming-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/incomingPermission')
        data = super().get(url=url, params=params)
        return ReadIncomingPermissionSettingsForPersonResponse.parse_obj(data)

    def modify_incoming_permission_settings_workspace(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, external_transfer: ExternalTransfer = None, internal_calls_enabled: bool = None, collect_calls_enabled: bool = None):
        """
        Modify Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for
            receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: ExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-incoming-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadIncomingPermissionSettingsForPersonResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if external_transfer is not None:
            body.external_transfer = external_transfer
        if internal_calls_enabled is not None:
            body.internal_calls_enabled = internal_calls_enabled
        if collect_calls_enabled is not None:
            body.collect_calls_enabled = collect_calls_enabled
        url = self.ep(f'{workspace_id}/features/incomingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_outgoing_permission_settings_workspace(self, workspace_id: str, org_id: str = None) -> RetrieveOutgoingPermissionSettingsForWorkspaceResponse:
        """
        Retrieve Outgoing Permission settings for a Workspace.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-outgoing-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrieveOutgoingPermissionSettingsForWorkspaceResponse.parse_obj(data)

    def modify_outgoing_permission_settings_workspace(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, calling_permissions: CallingPermissionObject = None):
        """
        Modify Outgoing Permission settings for a Place.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param use_custom_enabled: Outgoing Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: CallingPermissionObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-outgoing-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyOutgoingPermissionSettingsForWorkspaceBody()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'{workspace_id}/features/outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_access_codes_workspace(self, workspace_id: str, org_id: str = None) -> list[AccessCodes]:
        """
        Retrieve Access codes for a Workspace.
        Access codes are used to bypass permissions.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[AccessCodes], data["accessCodes"])

    def modify_access_codes_workspace(self, workspace_id: str, org_id: str = None, delete_codes: List[str] = None):
        """
        Modify Access codes for a workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyAccessCodesForWorkspaceBody()
        if delete_codes is not None:
            body.delete_codes = delete_codes
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        super().put(url=url, params=params, data=body.json())
        return

    def create_access_codes_workspace(self, workspace_id: str, org_id: str = None, code: str = None, description: str = None):
        """
        Create new Access codes for the given workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param code: Access code number.
        :type code: str
        :param description: Access code description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/create-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AccessCodes()
        if code is not None:
            body.code = code
        if description is not None:
            body.description = description
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        super().post(url=url, params=params, data=body.json())
        return

    def read_call_intercept_settings_workspace(self, workspace_id: str, org_id: str = None) -> ReadCallInterceptSettingsForWorkspaceResponse:
        """
        Retrieves Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified workspace are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/read-call-intercept-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/intercept')
        data = super().get(url=url, params=params)
        return ReadCallInterceptSettingsForWorkspaceResponse.parse_obj(data)

    def configure_call_intercept_settings_workspace(self, workspace_id: str, org_id: str = None, enabled: bool = None, incoming: InterceptIncomingPatch = None, outgoing: Outgoing = None):
        """
        Configures a Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_write or
        a user auth token with spark:workspaces_read scope can be used by a person to read their settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param enabled: true if call interception is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: InterceptIncomingPatch
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: Outgoing

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/configure-call-intercept-settings-for-a-workspace
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
        url = self.ep(f'{workspace_id}/features/intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_transfer_numbers_settings_workspace(self, workspace_id: str, org_id: str = None) -> GetOutgoingPermissionAutoTransferNumberResponse:
        """
        Retrieve Transfer Numbers Settings for a Workspace.
        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type.
        You can add up to 3 numbers.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/retrieve-transfer-numbers-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        data = super().get(url=url, params=params)
        return GetOutgoingPermissionAutoTransferNumberResponse.parse_obj(data)

    def modify_transfer_numbers_settings_workspace(self, workspace_id: str, org_id: str = None, auto_transfer_number1: str = None, auto_transfer_number2: str = None, auto_transfer_number3: str = None):
        """
        Modify Transfer Numbers Settings for a place.
        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type.
        You can add up to 3 numbers.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param auto_transfer_number1: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_1 will be transferred to this number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_2 will be transferred to this number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_3 will be transferred to this number.
        :type auto_transfer_number3: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-calling-behavior/modify-transfer-numbers-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetOutgoingPermissionAutoTransferNumberResponse()
        if auto_transfer_number1 is not None:
            body.auto_transfer_number1 = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body.auto_transfer_number2 = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body.auto_transfer_number3 = auto_transfer_number3
        url = self.ep(f'{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        super().put(url=url, params=params, data=body.json())
        return

class HotelingRequest(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this
    #: host(workspace device) and use this device
    #: as if it were their own. This is useful for employees who travel to remote offices and need to make and receive
    #: calls using their office phone number and access features that are normally available on their office phone.
    enabled: Optional[bool]
    #: Enable limiting the time a guest can use the device. The time limit is configured via guestHoursLimit.
    limit_guest_use: Optional[bool]
    #: Time limit, in hours, until the hoteling reservation expires.
    guest_hours_limit: Optional[int]


class ModifydevicesHotelingSettingsBody(ApiModel):
    #: Modify person Device Hoteling Setting.
    hoteling: Optional[HotelingRequest]


class WebexCallingPersonSettingswithHotelingApi(ApiChild, base='telephony/config/people/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Person Settings supports modifying Webex Calling settings for a specific person.
    Viewing People requires a full, person, or read-only administrator auth token with a scope of
    spark-admin:people_read or, for select APIs, a person auth token with spark:people_read scope can be used by a
    person to read their own settings.
    Configuring People settings requires a full or person administrator auth token with the spark-admin:people_write
    scope or, for select APIs, a person auth token with spark:people_write scope can be used by a person to update
    their own settings.
    """

    def user_devices(self, person_id: str, org_id: str = None) -> GetUserDevicesResponse:
        """
        Get all Webex Calling devices for a person.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person for whom to retrieve devices.
        :type person_id: str
        :param org_id: Organization to which the person belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-hoteling/get-user-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/devices')
        data = super().get(url=url, params=params)
        return GetUserDevicesResponse.parse_obj(data)

    def modifydevices_hoteling_settings(self, user_id: str, hoteling: HotelingRequest, org_id: str = None):
        """
        Modify hoteling for a person's Webex Calling Device.
        Modifying devices for a person requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param user_id: ID of the person for which to modify the associated device's hoteling settings.
        :type user_id: str
        :param hoteling: Modify person Device Hoteling Setting.
        :type hoteling: HotelingRequest
        :param org_id: Organization to which the person belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-hoteling/modify-a-device's-hoteling-settings
        """
        params = {}
        params['userId'] = user_id
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifydevicesHotelingSettingsBody()
        if hoteling is not None:
            body.hoteling = hoteling
        url = self.ep('{personId}/devices/settings/hoteling')
        super().put(url=url, params=params, data=body.json())
        return

class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str]
    #: The duration (in seconds) of the voicemail message. Duration is not present for a FAX message.
    duration: Optional[int]
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the
    #: calling party.
    calling_party: Optional[VoiceMailPartyInformation]
    #: true if the voicemail message is urgent.
    urgent: Optional[bool]
    #: true if the voicemail message is confidential.
    confidential: Optional[bool]
    #: true if the voicemail message has been read.
    read: Optional[bool]
    #: Number of pages for the FAX. Only set for a FAX.
    fax_page_count: Optional[int]
    #: The date and time the voicemail message was created.
    created: Optional[str]


class GetMessageSummaryResponse(ApiModel):
    #: The number of new (unread) voicemail messages.
    new_messages: Optional[int]
    #: The number of old (read) voicemail messages.
    old_messages: Optional[int]
    #: The number of new (unread) urgent voicemail messages.
    new_urgent_messages: Optional[int]
    #: The number of old (read) urgent voicemail messages.
    old_urgent_messages: Optional[int]


class ListMessagesResponse(ApiModel):
    items: Optional[list[VoiceMessageDetails]]


class MarkAsReadBody(ApiModel):
    #: The voicemail message identifier of the message to mark as read. If the messageId is not provided, then all
    #: voicemail messages for the user are marked as read.
    message_id: Optional[str]


class MarkAsUnreadBody(ApiModel):
    #: The voicemail message identifier of the message to mark as unread. If the messageId is not provided, then all
    #: voicemail messages for the user are marked as unread.
    message_id: Optional[str]


class WebexCallingVoiceMessagingApi(ApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling. The
    APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while
    the other commands require the spark:calls_write scope.
    """

    def summary(self) -> GetMessageSummaryResponse:
        """
        Get a summary of the voicemail messages for the user.

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-voice-messaging/get-message-summary
        """
        url = self.ep('summary')
        data = super().get(url=url)
        return GetMessageSummaryResponse.parse_obj(data)

    def list(self) -> list[VoiceMessageDetails]:
        """
        Get the list of all voicemail messages for the user.

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-voice-messaging/list-messages
        """
        url = self.ep()
        data = super().get(url=url)
        return parse_obj_as(list[VoiceMessageDetails], data["items"])

    def delete(self, message_id: str):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-voice-messaging/delete-message
        """
        url = self.ep(f'{message_id}')
        super().delete(url=url)
        return

    def mark_as_read(self, message_id: str = None):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read. Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read. If the messageId is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-voice-messaging/mark-as-read
        """
        body = MarkAsReadBody()
        if message_id is not None:
            body.message_id = message_id
        url = self.ep('markAsRead')
        super().post(url=url, data=body.json())
        return

    def mark_as_unread(self, message_id: str = None):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread. Otherwise, all messages for the user are
        marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread. If the messageId is not
            provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-voice-messaging/mark-as-unread
        """
        body = MarkAsUnreadBody()
        if message_id is not None:
            body.message_id = message_id
        url = self.ep('markAsUnread')
        super().post(url=url, data=body.json())
        return

class PlaceDevices(Devices):
    #: Indicates Hoteling details of a device.
    hoteling: Optional[HotelingRequest]


class RetrieveCallForwardingSettingsForWorkspaceResponse1(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingGet]


class ModifyCallForwardingSettingsForWorkspaceBody1(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingPatch]


class RetrieveCallWaitingSettingsForWorkspaceResponse1(ApiModel):
    #: Call Waiting state.
    enabled: Optional[bool]


class ModifyCallWaitingSettingsForWorkspaceBody1(ApiModel):
    #: Call Waiting state.
    enabled: Optional[bool]


class GetWorkspaceDevicesResponse(ApiModel):
    #: Array of devices associated to a workspace.
    devices: Optional[list[PlaceDevices]]
    #: Maximum number of devices a workspace can be assigned to.
    max_device_count: Optional[int]


class RetrieveAccessCodesForWorkspaceResponse1(ApiModel):
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AccessCodes]]


class ModifyAccessCodesForWorkspaceBody1(ApiModel):
    #: Indicates access codes to delete.
    delete_codes: Optional[list[str]]


class WebexCallingWorkspaceSettingsApi(ApiChild, base=''):
    """
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    Viewing the list of settings in a workspace requires an administrator auth token with the
    spark-admin:workspaces_read scope.
    Adding, updating, or deleting settings in a workspace requires an administrator auth token with the
    spark-admin:workspaces_write scope.
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an orgId must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query
    parameter.
    """

    def retrieve_call_forwarding_settings_for(self, workspace_id: str, org_id: str = None) -> CallForwardingPlaceSettingGet:
        """
        Retrieve Call Forwarding Settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return CallForwardingPlaceSettingGet.parse_obj(data["callForwarding"])

    def modify_call_forwarding_settings_for(self, workspace_id: str, call_forwarding: CallForwardingPlaceSettingPatch, org_id: str = None):
        """
        Modify call forwarding settings for a Workspace.
        Two types of call forwarding are supported:
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param call_forwarding: Call forwarding settings for a Workspace.
        :type call_forwarding: CallForwardingPlaceSettingPatch
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallForwardingSettingsForWorkspaceBody1()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        url = self.ep(f'workspaces/{workspace_id}/features/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_call_waiting_settings_for(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-call-waiting-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def modify_call_waiting_settings_for(self, workspace_id: str, org_id: str = None, enabled: bool = None):
        """
        Modify Call Waiting Settings for a Workspace.
        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param enabled: Call Waiting state.
        :type enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-call-waiting-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyCallWaitingSettingsForWorkspaceBody1()
        if enabled is not None:
            body.enabled = enabled
        url = self.ep(f'workspaces/{workspace_id}/features/callWaiting')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_caller_id_settings_for(self, workspace_id: str, org_id: str = None) -> RetrieveCallerIDSettingsForWorkspaceResponse:
        """
        Retrieve Caller ID Settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-caller-id-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/callerId')
        data = super().get(url=url, params=params)
        return RetrieveCallerIDSettingsForWorkspaceResponse.parse_obj(data)

    def modify_caller_id_settings_for(self, workspace_id: str, selected: CLIDPolicySelection, org_id: str = None, custom_number: str = None, display_name: str = None, display_detail: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: ExternalCallerIdNamePolicy = None, custom_external_caller_id_name: str = None, location_external_caller_id_name: str = None):
        """
        Modify Caller ID settings for a Workspace.
        Caller ID settings control how a workspace's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CLIDPolicySelection
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param custom_number: This value must be an assigned number from the workspace's location.
        :type custom_number: str
        :param display_name: Workspace's caller ID display name.
        :type display_name: str
        :param display_detail: Workspace's caller ID display details.
        :type display_detail: str
        :param block_in_forward_calls_enabled: Flag to block call forwarding.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is DIRECT_LINE. Possible values: DIRECT_LINE
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller ID
            Name is OTHER.
        :type custom_external_caller_id_name: str
        :param location_external_caller_id_name: External Caller Name, which will be shown if External Caller ID Name
            is OTHER.
        :type location_external_caller_id_name: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-caller-id-settings-for-a-workspace
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
        url = self.ep(f'workspaces/{workspace_id}/features/callerId')
        super().put(url=url, params=params, data=body.json())
        return

    def devices(self, workspace_id: str, org_id: str = None) -> GetWorkspaceDevicesResponse:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/get-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/devices')
        data = super().get(url=url, params=params)
        return GetWorkspaceDevicesResponse.parse_obj(data)

    def modify_devices(self, workspace_id: str, org_id: str = None, enabled: bool = None, limit_guest_use: bool = None, guest_hours_limit: int = None):
        """
        Modify devices for a workspace.
        Modifying devices for a workspace requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str
        :param enabled: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can
            log into this host(workspace device) and use this device as if it were their own. This is useful for
            employees who travel to remote offices and need to make and receive calls using their office phone number
            and access features that are normally available on their office phone.
        :type enabled: bool
        :param limit_guest_use: Enable limiting the time a guest can use the device. The time limit is configured via
            guestHoursLimit.
        :type limit_guest_use: bool
        :param guest_hours_limit: Time limit, in hours, until the hoteling reservation expires.
        :type guest_hours_limit: int

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = HotelingRequest()
        if enabled is not None:
            body.enabled = enabled
        if limit_guest_use is not None:
            body.limit_guest_use = limit_guest_use
        if guest_hours_limit is not None:
            body.guest_hours_limit = guest_hours_limit
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/devices')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_monitoring_settings_for(self, workspace_id: str, org_id: str = None) -> RetrieveMonitoringSettingsForWorkspaceResponse:
        """
        Retrieves Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-monitoring-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/monitoring')
        data = super().get(url=url, params=params)
        return RetrieveMonitoringSettingsForWorkspaceResponse.parse_obj(data)

    def modify_monitoring_settings_for(self, workspace_id: str, enable_call_park_notification: bool, monitored_elements: List[str], org_id: str = None):
        """
        Modify Monitoring settings for a Workspace.
        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
            Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
        :type monitored_elements: List[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-monitoring-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifypersonsMonitoringSettingsBody()
        if enable_call_park_notification is not None:
            body.enable_call_park_notification = enable_call_park_notification
        if monitored_elements is not None:
            body.monitored_elements = monitored_elements
        url = self.ep(f'workspaces/{workspace_id}/features/monitoring')
        super().put(url=url, params=params, data=body.json())
        return

    def list_numbers_associated_withspecific(self, workspace_id: str, org_id: str = None):
        """
        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and organization associated with the workspace.
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:workspaces_read.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            can use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/list-numbers-associated-with-a-specific-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/numbers')
        super().get(url=url, params=params)
        return $!$!$!   # this is weird. Check the spec at https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/list-numbers-associated-with-a-specific-workspace

    def retrieve_incoming_permission_settings_for(self, workspace_id: str, org_id: str = None) -> ReadIncomingPermissionSettingsForPersonResponse:
        """
        Retrieve Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-incoming-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/incomingPermission')
        data = super().get(url=url, params=params)
        return ReadIncomingPermissionSettingsForPersonResponse.parse_obj(data)

    def modify_incoming_permission_settings_for(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, external_transfer: ExternalTransfer = None, internal_calls_enabled: bool = None, collect_calls_enabled: bool = None):
        """
        Modify Incoming Permission settings for a Workspace.
        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for
            receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: ExternalTransfer
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-incoming-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadIncomingPermissionSettingsForPersonResponse()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if external_transfer is not None:
            body.external_transfer = external_transfer
        if internal_calls_enabled is not None:
            body.internal_calls_enabled = internal_calls_enabled
        if collect_calls_enabled is not None:
            body.collect_calls_enabled = collect_calls_enabled
        url = self.ep(f'workspaces/{workspace_id}/features/incomingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_outgoing_permission_settings_for(self, workspace_id: str, org_id: str = None) -> RetrieveOutgoingPermissionSettingsForWorkspaceResponse:
        """
        Retrieve Outgoing Permission settings for a Workspace.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-outgoing-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrieveOutgoingPermissionSettingsForWorkspaceResponse.parse_obj(data)

    def modify_outgoing_permission_settings_for(self, workspace_id: str, org_id: str = None, use_custom_enabled: bool = None, calling_permissions: CallingPermissionObject = None):
        """
        Modify Outgoing Permission settings for a Place.
        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param use_custom_enabled: Outgoing Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: CallingPermissionObject

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-outgoing-permission-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyOutgoingPermissionSettingsForWorkspaceBody()
        if use_custom_enabled is not None:
            body.use_custom_enabled = use_custom_enabled
        if calling_permissions is not None:
            body.calling_permissions = calling_permissions
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_access_codes_for(self, workspace_id: str, org_id: str = None) -> list[AccessCodes]:
        """
        Retrieve Access codes for a Workspace.
        Access codes are used to bypass permissions.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[AccessCodes], data["accessCodes"])

    def modify_access_codes_for(self, workspace_id: str, org_id: str = None, delete_codes: List[str] = None):
        """
        Modify Access codes for a workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: List[str]

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ModifyAccessCodesForWorkspaceBody1()
        if delete_codes is not None:
            body.delete_codes = delete_codes
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().put(url=url, params=params, data=body.json())
        return

    def create_access_codes_for(self, workspace_id: str, org_id: str = None, code: str = None, description: str = None):
        """
        Create new Access codes for the given workspace.
        Access codes are used to bypass permissions.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param code: Access code number.
        :type code: str
        :param description: Access code description.
        :type description: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/create-access-codes-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = AccessCodes()
        if code is not None:
            body.code = code
        if description is not None:
            body.description = description
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().post(url=url, params=params, data=body.json())
        return

    def read_call_intercept_settings_for(self, workspace_id: str, org_id: str = None) -> ReadCallInterceptSettingsForWorkspaceResponse:
        """
        Retrieves Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified workspace are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/read-call-intercept-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/intercept')
        data = super().get(url=url, params=params)
        return ReadCallInterceptSettingsForWorkspaceResponse.parse_obj(data)

    def configure_call_intercept_settings_for(self, workspace_id: str, org_id: str = None, enabled: bool = None, incoming: InterceptIncomingPatch = None, outgoing: Outgoing = None):
        """
        Configures a Workspace's Call Intercept Settings
        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_write or
        a user auth token with spark:workspaces_read scope can be used by a person to read their settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param enabled: true if call interception is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: InterceptIncomingPatch
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: Outgoing

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/configure-call-intercept-settings-for-a-workspace
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
        url = self.ep(f'workspaces/{workspace_id}/features/intercept')
        super().put(url=url, params=params, data=body.json())
        return

    def retrieve_transfer_numbers_settings_for(self, workspace_id: str, org_id: str = None) -> GetOutgoingPermissionAutoTransferNumberResponse:
        """
        Retrieve Transfer Numbers Settings for a Workspace.
        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type.
        You can add up to 3 numbers.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/retrieve-transfer-numbers-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        data = super().get(url=url, params=params)
        return GetOutgoingPermissionAutoTransferNumberResponse.parse_obj(data)

    def modify_transfer_numbers_settings_for(self, workspace_id: str, org_id: str = None, auto_transfer_number1: str = None, auto_transfer_number2: str = None, auto_transfer_number3: str = None):
        """
        Modify Transfer Numbers Settings for a place.
        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call type.
        You can add up to 3 numbers.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param auto_transfer_number1: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_1 will be transferred to this number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_2 will be transferred to this number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: Calls placed meeting the criteria in an outbound rule whose action is
            TRANSFER_NUMBER_3 will be transferred to this number.
        :type auto_transfer_number3: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings/modify-transfer-numbers-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = GetOutgoingPermissionAutoTransferNumberResponse()
        if auto_transfer_number1 is not None:
            body.auto_transfer_number1 = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body.auto_transfer_number2 = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body.auto_transfer_number3 = auto_transfer_number3
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        super().put(url=url, params=params, data=body.json())
        return

class WebexCallingWorkspaceSettingswithEnhancedForwardingApi(ApiChild, base='workspaces/'):
    """
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    Viewing the list of settings in a workspace requires an administrator auth token with the
    spark-admin:workspaces_read scope.
    Adding, updating, or deleting settings in a workspace requires an administrator auth token with the
    spark-admin:workspaces_write scope.
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an orgId must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def retrieve_forwarding_settings_for_workspace(self, workspace_id: str, org_id: str = None) -> ReadForwardingSettingsForPersonResponse:
        """
        Retrieve Call Forwarding Settings for a Workspace.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or a
        user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings-with-enhanced-forwarding/retrieve-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return ReadForwardingSettingsForPersonResponse.parse_obj(data)

    def modify_forwarding_settings_for_workspace(self, workspace_id: str, org_id: str = None, call_forwarding: CallForwarding4 = None, business_continuity: BusinessContinuity = None):
        """
        Modify call forwarding settings for a Workspace.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.
        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a user
        auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: CallForwarding4
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: BusinessContinuity

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-workspace-settings-with-enhanced-forwarding/modify-call-forwarding-settings-for-a-workspace
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = ReadForwardingSettingsForPersonResponse()
        if call_forwarding is not None:
            body.call_forwarding = call_forwarding
        if business_continuity is not None:
            body.business_continuity = business_continuity
        url = self.ep(f'{workspace_id}/features/callForwarding')
        super().put(url=url, params=params, data=body.json())
        return

class UpdateDirectorySyncForBroadWorksEnterpriseBody1(ApiModel):
    #: The toggle to enable/disable directory sync.
    enable_dir_sync: Optional[bool]


class TriggerDirectorySyncForEnterpriseBody1(ApiModel):
    #: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the directory sync for
    #: the BroadWorks enterprise.
    sync_status: Optional[str]


class WebexforBroadworksphonelistsyncApi(ApiChild, base='broadworks/enterprises'):
    """
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. They enable Service Providers to provision Cisco Webex Services for their subscribers. They
    also synchronize
    your enterprise BroadWorks directories and phone lists (user and organization-specific) with Webex. BroadWorks
    phone numbers will
    be searchable in the Webex app.
    Please note these APIs require a functional BroadWorks system configured for Webex for BroadWorks. Read more about
    using this API
    at https://www.cisco.com/go/WebexBroadworksAPI.
    Viewing Webex for BroadWorks enterprise information requires an administrator auth token with
    spark-admin:broadworks_enterprises_read scope.
    Updating directory sync configuration or trigger directory sync for a Webex for BroadWorks enterprise require an
    administrator auth token with spark-admin:broadworks_enterprises_write scope.
    """

    def list_broad_works_enterprises(self, sp_enterprise_id: str = None, starts_with: str = None, max: int = None) -> ListBroadWorksEnterprisesResponse:
        """
        List the provisioned enterprises for a Service Provider. This API will also allow a Service Provider to search
        for their provisioned enterprises on Cisco Webex. A search on enterprises can be performed by either a full or
        partial enterprise identifier.

        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param starts_with: The starting string of the enterprise identifiers to match against.
        :type starts_with: str
        :param max: Limit the number of enterprises returned in the search, up to 1000.
        :type max: int

        documentation: https://developer.webex.com/docs/api/v1/webex-for-broadworks-phone-list-sync/list-broadworks-enterprises
        """
        params = {}
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if starts_with is not None:
            params['startsWith'] = starts_with
        if max is not None:
            params['max'] = max
        url = self.ep()
        data = super().get(url=url, params=params)
        return ListBroadWorksEnterprisesResponse.parse_obj(data)

    def update_sync_for_broad_works_enterprise(self, id: str, enable_dir_sync: bool) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to update enableDirSync for the customers Broadworks enterprise on Cisco
        Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param enable_dir_sync: The toggle to enable/disable directory sync.
        :type enable_dir_sync: bool

        documentation: https://developer.webex.com/docs/api/v1/webex-for-broadworks-phone-list-sync/update-directory-sync-for-a-broadworks-enterprise
        """
        body = UpdateDirectorySyncForBroadWorksEnterpriseBody1()
        if enable_dir_sync is not None:
            body.enable_dir_sync = enable_dir_sync
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().put(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def trigger_sync_for_enterprise(self, id: str, sync_status: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to trigger a directory sync for the customers Broadworks enterprise on
        Cisco Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str
        :param sync_status: At this time, the only option allowed for this attribute is SYNC_NOW which will trigger the
            directory sync for the BroadWorks enterprise.
        :type sync_status: str

        documentation: https://developer.webex.com/docs/api/v1/webex-for-broadworks-phone-list-sync/trigger-directory-sync-for-an-enterprise
        """
        body = TriggerDirectorySyncForEnterpriseBody1()
        if sync_status is not None:
            body.sync_status = sync_status
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().post(url=url, data=body.json())
        return BroadworksDirectorySync.parse_obj(data)

    def sync_status_for_enterprise(self, id: str) -> BroadworksDirectorySync:
        """
        This API will allow a Partner Admin to get the most recent directory sync status for a customer Broadworks
        enterprise on Cisco Webex.

        :param id: A unique identifier for the enterprise in question.
        :type id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-for-broadworks-phone-list-sync/get-directory-sync-status-for-an-enterprise
        """
        url = self.ep(f'{id}/broadworksDirectorySync')
        data = super().get(url=url)
        return BroadworksDirectorySync.parse_obj(data)

class SupportedDevices(str, Enum):
    #: Workspace supports collaborationDevices.
    collaboration_devices = 'collaborationDevices'
    #: Workspace supports MPP phones.
    phones = 'phones'


class Type46(str, Enum):
    #: No workspace type set.
    not_set = 'notSet'
    #: High concentration.
    focus = 'focus'
    #: Brainstorm/collaboration.
    huddle = 'huddle'
    #: Dedicated meeting space.
    meeting_room = 'meetingRoom'
    #: Unstructured agile.
    open = 'open'
    #: Individual.
    desk = 'desk'
    #: Unspecified.
    other = 'other'


class Calendar1(ApiModel):
    type: Optional[str]
    #: Workspace email address. Will not be set when the calendar type is none.
    email_address: Optional[str]


class Calling1(ApiModel):
    #: Calling.
    type: Optional[str]
    #: The webexCalling object only applies when calling type is webexCalling.
    webex_calling: Optional[WebexCalling]


class HotdeskingStatus(str, Enum):
    #: Workspace supports hotdesking.
    on = 'on'
    #: Workspace does not support hotdesking.
    off = 'off'


class UpdateWorkspaceBody(ApiModel):
    #: A friendly name for the workspace.
    display_name: Optional[str]
    #: Location associated with the workspace. Must be provided when the floorId is set.
    workspace_location_id: Optional[str]
    #: Floor associated with the workspace.
    floor_id: Optional[str]
    #: How many people the workspace is suitable for. If set, must be 0 or higher.
    capacity: Optional[int]
    #: The type that best describes the workspace.
    type: Optional[Type46]
    #: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or none) and an
    #: emailAddress. Removing calendar is done by setting the none type, and setting none type does not require an
    #: emailAddress.
    calendar: Optional[Calendar1]
    #: The sipAddress field can only be provided when calling type is thirdPartySipCalling
    sip_address: Optional[str]
    #: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
    calling: Optional[Calling1]
    #: Notes associated with the workspace.
    notes: Optional[str]
    #: Hot desking status of the workspace.
    hotdesking_status: Optional[HotdeskingStatus]


class Workspace(UpdateWorkspaceBody):
    #: Unique identifier for the Workspace.
    id: Optional[str]
    #: OrgId associate with the workspace.
    org_id: Optional[str]
    #: The date and time that the workspace was registered, in ISO8601 format.
    created: Optional[str]
    #: The supported devices for the workspace. Default is collaborationDevices.
    supported_devices: Optional[SupportedDevices]


class SupportAndConfiguredInfo(ApiModel):
    #: Is the workspace capability supported or not.
    supported: Optional[bool]
    #: Is the workspace capability configured or not.
    configured: Optional[bool]


class CapabilityMap(ApiModel):
    #: Occupancy detection.
    occupancy_detection: Optional[SupportAndConfiguredInfo]
    #: Presence detection.
    presence_detection: Optional[SupportAndConfiguredInfo]
    #: Ambient noise.
    ambient_noise: Optional[SupportAndConfiguredInfo]
    #: Sound level.
    sound_level: Optional[SupportAndConfiguredInfo]
    #: Temperature.
    temperature: Optional[SupportAndConfiguredInfo]
    #: Air quality.
    air_quality: Optional[SupportAndConfiguredInfo]
    #: Relative humidity.
    relative_humidity: Optional[SupportAndConfiguredInfo]


class ListWorkspacesResponse(ApiModel):
    #: An array of workspace objects.
    items: Optional[list[Workspace]]


class CreateWorkspaceBody(UpdateWorkspaceBody):
    #: OrgId associated with the workspace. Only admin users of another organization (such as partners) may use this
    #: parameter.
    org_id: Optional[str]
    #: The supported devices for the workspace. Default is collaborationDevices.
    supported_devices: Optional[SupportedDevices]


class GetWorkspaceCapabilitiesResponse(ApiModel):
    #: The map of workspace capabilities.
    capabilities: Optional[CapabilityMap]


class WorkspaceswithWXCIncludedApi(ApiChild, base='workspaces'):
    """
    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.
    Viewing the list of workspaces in an organization requires an administrator auth token with the
    spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the scopes spark-admin:workspaces_write and spark-admin:telephony_config_write.
    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for the
    relevant endpoints.
    """

    def list(self, org_id: str = None, workspace_location_id: str = None, floor_id: str = None, display_name: str = None, capacity: int = None, type_: str = None, calling: str = None, supported_devices: str = None, calendar: str = None, **params) -> Generator[Workspace, None, None]:
        """
        List workspaces.
        Use query parameters to filter the response. The orgId parameter can only be used by admin users of another
        organization (such as partners). The workspaceLocationId, floorId, capacity and type fields will only be
        present for workspaces that have a value set for them. The special values notSet (for filtering on category)
        and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or capacity.

        :param org_id: List workspaces in this organization. Only admin users of another organization (such as
            partners) may use this parameter.
        :type org_id: str
        :param workspace_location_id: Location associated with the workspace.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param type_: List workspaces by type. Possible values: notSet, focus, huddle, meetingRoom, open, desk, other
        :type type_: str
        :param calling: List workspaces by calling type. Possible values: freeCalling, hybridCalling, webexCalling,
            webexEdgeForDevices, thirdPartySipCalling, none
        :type calling: str
        :param supported_devices: List workspaces by supported devices. Possible values: collaborationDevices, phones
        :type supported_devices: str
        :param calendar: List workspaces by calendar type. Possible values: none, google, microsoft
        :type calendar: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/list-workspaces
        """
        if org_id is not None:
            params['orgId'] = org_id
        if workspace_location_id is not None:
            params['workspaceLocationId'] = workspace_location_id
        if floor_id is not None:
            params['floorId'] = floor_id
        if display_name is not None:
            params['displayName'] = display_name
        if capacity is not None:
            params['capacity'] = capacity
        if type_ is not None:
            params['type'] = type_
        if calling is not None:
            params['calling'] = calling
        if supported_devices is not None:
            params['supportedDevices'] = supported_devices
        if calendar is not None:
            params['calendar'] = calendar
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Workspace, params=params)

    def create(self, display_name: str = None, workspace_location_id: str = None, floor_id: str = None, capacity: int = None, type_: Type46 = None, calendar: Calendar1 = None, sip_address: str = None, calling: Calling1 = None, notes: str = None, hotdesking_status: HotdeskingStatus = None, org_id: str = None, supported_devices: SupportedDevices = None) -> Workspace:
        """
        Create a workspace.
        The workspaceLocationId, floorId, capacity, type, notes and hotdeskingStatus parameters are optional, and
        omitting them will result in the creation of a workspace without these values set, or set to their default. A
        workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set for a new
        workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can only be used
        by admin users of another organization (such as partners).

        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param workspace_location_id: Location associated with the workspace. Must be provided when the floorId is set.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type_: The type that best describes the workspace.
        :type type_: Type46
        :param calendar: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or
            none) and an emailAddress. Removing calendar is done by setting the none type, and setting none type does
            not require an emailAddress.
        :type calendar: Calendar1
        :param sip_address: The sipAddress field can only be provided when calling type is thirdPartySipCalling
        :type sip_address: str
        :param calling: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
        :type calling: Calling1
        :param notes: Notes associated with the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: HotdeskingStatus
        :param org_id: OrgId associated with the workspace. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param supported_devices: The supported devices for the workspace. Default is collaborationDevices.
        :type supported_devices: SupportedDevices

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/create-a-workspace
        """
        body = CreateWorkspaceBody()
        if display_name is not None:
            body.display_name = display_name
        if workspace_location_id is not None:
            body.workspace_location_id = workspace_location_id
        if floor_id is not None:
            body.floor_id = floor_id
        if capacity is not None:
            body.capacity = capacity
        if type_ is not None:
            body.type_ = type_
        if calendar is not None:
            body.calendar = calendar
        if sip_address is not None:
            body.sip_address = sip_address
        if calling is not None:
            body.calling = calling
        if notes is not None:
            body.notes = notes
        if hotdesking_status is not None:
            body.hotdesking_status = hotdesking_status
        if org_id is not None:
            body.org_id = org_id
        if supported_devices is not None:
            body.supported_devices = supported_devices
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return Workspace.parse_obj(data)

    def details(self, workspace_id: str) -> Workspace:
        """
        Shows details for a workspace, by ID.
        The workspaceLocationId, floorId, capacity, type and notes fields will only be present if they have been set
        for the workspace. Specify the workspace ID in the workspaceId parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/get-workspace-details
        """
        url = self.ep(f'{workspace_id}')
        data = super().get(url=url)
        return Workspace.parse_obj(data)

    def update(self, workspace_id: str, display_name: str = None, workspace_location_id: str = None, floor_id: str = None, capacity: int = None, type_: Type46 = None, calendar: Calendar1 = None, sip_address: str = None, calling: Calling1 = None, notes: str = None, hotdesking_status: HotdeskingStatus = None) -> Workspace:
        """
        Updates details for a workspace by ID.
        Specify the workspace ID in the workspaceId parameter in the URI. Include all details for the workspace that
        are present in a GET request for the workspace details. Not including the optional capacity, type or notes
        fields will result in the fields no longer being defined for the workspace. A workspaceLocationId must be
        provided when the floorId is set. The workspaceLocationId, floorId, supportedDevices, calendar and calling
        fields do not change when omitted from the update request.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param display_name: A friendly name for the workspace.
        :type display_name: str
        :param workspace_location_id: Location associated with the workspace. Must be provided when the floorId is set.
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param capacity: How many people the workspace is suitable for. If set, must be 0 or higher.
        :type capacity: int
        :param type_: The type that best describes the workspace.
        :type type_: Type46
        :param calendar: An empty/null calendar field will not cause any changes. Provide a type (microsoft, google or
            none) and an emailAddress. Removing calendar is done by setting the none type, and setting none type does
            not require an emailAddress.
        :type calendar: Calendar1
        :param sip_address: The sipAddress field can only be provided when calling type is thirdPartySipCalling
        :type sip_address: str
        :param calling: Calling types supported on update are freeCalling, thirdPartySipCalling, webexCalling and none.
        :type calling: Calling1
        :param notes: Notes associated with the workspace.
        :type notes: str
        :param hotdesking_status: Hot desking status of the workspace.
        :type hotdesking_status: HotdeskingStatus

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/update-a-workspace
        """
        body = UpdateWorkspaceBody()
        if display_name is not None:
            body.display_name = display_name
        if workspace_location_id is not None:
            body.workspace_location_id = workspace_location_id
        if floor_id is not None:
            body.floor_id = floor_id
        if capacity is not None:
            body.capacity = capacity
        if type_ is not None:
            body.type_ = type_
        if calendar is not None:
            body.calendar = calendar
        if sip_address is not None:
            body.sip_address = sip_address
        if calling is not None:
            body.calling = calling
        if notes is not None:
            body.notes = notes
        if hotdesking_status is not None:
            body.hotdesking_status = hotdesking_status
        url = self.ep(f'{workspace_id}')
        data = super().put(url=url, data=body.json())
        return Workspace.parse_obj(data)

    def delete(self, workspace_id: str):
        """
        Deletes a workspace by ID.
        Also deletes all devices associated with the workspace. Any deleted devices will need to be reactivated.
        Specify the workspace ID in the workspaceId parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/delete-a-workspace
        """
        url = self.ep(f'{workspace_id}')
        super().delete(url=url)
        return

    def capabilities(self, workspace_id: str) -> CapabilityMap:
        """
        Shows the capabilities for a workspace by ID.
        Returns a set of capabilities, including whether or not the capability is supported by any device in the
        workspace, and if the capability is configured (enabled). For example for a specific capability like
        occupancyDetection, the API will return if the capability is supported and/or configured such that occupancy
        detection data will flow from the workspace (device) to the cloud. Specify the workspace ID in the workspaceId
        parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        documentation: https://developer.webex.com/docs/api/v1/workspaces-with-wxc-included/get-workspace-capabilities
        """
        url = self.ep(f'{workspace_id}/capabilities')
        data = super().get(url=url)
        return CapabilityMap.parse_obj(data["capabilities"])
