from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, Enum
from typing import List, Optional
from pydantic import Field


__all__ = ['AccessCodes', 'Action', 'Action11', 'Action15', 'Action6', 'Action9', 'AddNewEventForPersonsScheduleResponse', 'AddPhoneNumbersTolocationBody', 'Address', 'AlternateNumberSettings', 'AlternateNumbersObject', 'AlternateNumbersWithPattern', 'AlternateNumbersWithPattern1', 'Always', 'AnnouncementMode', 'Announcements', 'Announcements3', 'AutoAttendantCallForwardSettingsDetailsObject', 'AutoAttendantCallForwardSettingsModifyDetailsObject', 'BehaviorType', 'BlockContiguousSequences', 'BlockPreviousPasscodes', 'BlockRepeatedDigits', 'BusinessContinuity', 'Call', 'CallBounce', 'CallControlsApi', 'CallForwardRulesGet', 'CallForwardRulesModifyObject', 'CallForwardRulesObject', 'CallForwardSelectiveCallsFromCustomNumbersObject', 'CallForwardSelectiveCallsFromObject', 'CallForwardSelectiveCallsToNumbersObject', 'CallForwardSelectiveCallsToObject', 'CallForwardSelectiveCallsToObject1', 'CallForwardSelectiveForwardToObject', 'CallForwarding', 'CallForwarding1', 'CallForwarding4', 'CallHistoryRecord', 'CallHistoryRecordTypeEnum', 'CallParkSettingsObject', 'CallPersonalityEnum', 'CallQueueAudioFilesObject', 'CallQueueHolidaySchedulesObject', 'CallQueueObject', 'CallQueueObject1', 'CallQueueQueueSettingsObject', 'CallSourceInfo', 'CallSourceType', 'CallStateEnum', 'CallType', 'CallTypeEnum', 'CallerIdSelectedType', 'CallingLineId', 'CallingPermissionObject', 'CallingPermissions', 'Callparkextension', 'CallsFrom', 'CallsTo', 'CallsTo1', 'CallsTo4', 'ConfigureCallRecordingSettingsForPersonBody', 'ConfigureCallerIDSettingsForPersonBody', 'ConfigurepersonsCallingBehaviorBody', 'CreateAutoAttendantBody', 'CreateAutoAttendantResponse', 'CreateCallParkBody', 'CreateCallParkExtensionResponse', 'CreateCallParkResponse', 'CreateCallPickupBody', 'CreateCallPickupResponse', 'CreateCallQueueResponse', 'CreateDialPlanResponse', 'CreateHuntGroupResponse', 'CreateLocationResponse', 'CreatePersonBody', 'CreateRouteGroupForOrganizationBody', 'CreateRouteGroupForOrganizationResponse', 'CreateRouteListResponse', 'CreateScheduleEventResponse', 'CreateScheduleForPersonBody', 'CreateScheduleForPersonResponse', 'CreateScheduleResponse', 'CreateSelectiveCallForwardingRuleForAutoAttendantBody', 'CreateSelectiveCallForwardingRuleForAutoAttendantResponse', 'CreateSelectiveCallForwardingRuleForCallQueueBody', 'CreateSelectiveCallForwardingRuleForCallQueueResponse', 'CreateSelectiveCallForwardingRuleForHuntGroupResponse', 'CreateTrunkResponse', 'CreatenewPagingGroupResponse', 'CreatenewVoicemailGroupForLocationResponse', 'Day', 'DefaultVoicemailPinRules', 'DestinationType', 'DeviceStatus', 'DeviceType', 'DialPattern', 'DialPatternAction', 'DialPatternStatus', 'DialPatternValidate', 'DialPlan', 'DialResponse', 'DistinctiveRing', 'EffectiveBehaviorType', 'EmailCopyOfMessage', 'Emergency', 'EventLongDetails', 'ExpirePasscode', 'ExtensionDialing', 'ExtensionStatusObject', 'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'FailedAttempts', 'FaxMessage', 'FaxMessage3', 'FeatureAccessCode', 'FetchEventForpersonsScheduleResponse', 'GenerateExamplePasswordForLocationResponse', 'GetAnnouncementFileInfo', 'GetAvailableAgentsFromCallParksResponse', 'GetAvailableAgentsFromCallPickupsResponse', 'GetAvailableRecallHuntGroupsFromCallParksResponse', 'GetAvailableRecallHuntGroupsObject', 'GetCallForwardAlwaysSettingObject', 'GetCallForwardingSettingsForAutoAttendantResponse', 'GetCallForwardingSettingsForCallQueueResponse', 'GetCallForwardingSettingsForHuntGroupResponse', 'GetCallParkSettingsResponse', 'GetCallRecordingSettingsResponse', 'GetCallRecordingTermsOfServiceSettingsResponse', 'GetDetailsForAutoAttendantResponse', 'GetDetailsForCallParkExtensionResponse', 'GetDetailsForCallParkResponse', 'GetDetailsForCallPickupResponse', 'GetDetailsForCallQueueForcedForwardResponse', 'GetDetailsForCallQueueHolidayServiceResponse', 'GetDetailsForCallQueueNightServiceResponse', 'GetDetailsForCallQueueResponse', 'GetDetailsForCallQueueStrandedCallsResponse', 'GetDetailsForHuntGroupResponse', 'GetDetailsForPagingGroupResponse', 'GetDetailsForScheduleEventResponse', 'GetDetailsForScheduleResponse', 'GetDialPlanResponse', 'GetListOfPhoneNumbersForPersonResponse', 'GetLocalGatewayCallToOnPremisesExtensionUsageForTrunkResponse', 'GetLocalGatewayDialPlanUsageForTrunkResponse', 'GetLocalGatewayUsageCountResponse', 'GetLocationInterceptResponse', 'GetLocationOutgoingPermissionResponse', 'GetLocationVoicemailGroupResponse', 'GetLocationVoicemailResponse', 'GetLocationWebexCallingDetailsResponse', 'GetLocationsUsingLocalGatewayAsPSTNConnectionRoutingResponse', 'GetMessageSummaryResponse', 'GetMonitoredElementsObject', 'GetMusicOnHoldResponse', 'GetNumbersAssignedToRouteListResponse', 'GetOutgoingPermissionAutoTransferNumberResponse', 'GetOutgoingPermissionLocationAccessCodeResponse', 'GetPagingGroupAgentObject', 'GetPagingGroupAgentObject1', 'GetPersonPlaceCallParksObject', 'GetPersonPlaceObject', 'GetPersonPlaceObject1', 'GetPhoneNumbersForOrganizationWithGivenCriteriasResponse', 'GetPrivateNetworkConnectResponse', 'GetRecallHuntGroupObject', 'GetRecallHuntGroupObject1', 'GetRouteGroupsUsingLocalGatewayResponse', 'GetRouteListResponse', 'GetScheduleDetailsResponse', 'GetScheduleEventObject', 'GetSelectiveCallForwardingRuleForAutoAttendantResponse', 'GetSelectiveCallForwardingRuleForCallQueueResponse', 'GetSelectiveCallForwardingRuleForHuntGroupResponse', 'GetTrunkResponse', 'GetUserNumberItemObject', 'GetVoicePortalPasscodeRuleResponse', 'GetVoicePortalResponse', 'GetVoicemailGroupObject', 'GetVoicemailRulesResponse', 'GetVoicemailSettingsResponse', 'GetpersonsPrivacySettingsResponse', 'Greeting', 'Greeting11', 'HolidayScheduleLevel', 'HostedAgent', 'HostedFeature', 'HoursMenuObject', 'HuntPolicySelection', 'Incoming', 'Key', 'KeyConfigurationsObject', 'Length', 'ListAutoAttendantObject', 'ListCallHistoryResponse', 'ListCallParkExtensionObject', 'ListCallParkObject', 'ListCallQueueObject', 'ListCallsResponse', 'ListHuntGroupObject', 'ListLocationsResponse', 'ListMessagesResponse', 'ListOfSchedulesForPersonResponse', 'ListPagingGroupObject', 'ListPeopleResponse', 'ListScheduleObject', 'ListVoicemailGroupResponse', 'LocalGateways', 'Location', 'LocationsApi', 'MediaFileType', 'Member', 'MessageStorage', 'MessageStorage3', 'ModifyDialPlanBody', 'ModifyNumbersForRouteListResponse', 'ModifyRouteListBody', 'ModifyScheduleEventListObject', 'ModifypersonsApplicationServicesSettingsBody', 'MonitoredMemberObject', 'MonitoredPersonObject', 'Month', 'NetworkConnectionType', 'NewNumber', 'NoAnswer', 'NoAnswer3', 'NumberListGetObject', 'NumberStatus', 'Option', 'OriginatorType', 'Outgoing', 'Overflow', 'Owner', 'ParkResponse', 'PartyInformation', 'Passcode', 'PbxUser', 'PeopleApi', 'Person', 'PhoneNumber', 'PhoneNumbers', 'PhoneNumbers7', 'PostCallQueueCallPolicyObject', 'PostHuntGroupCallPolicyObject', 'PostPersonPlaceObject', 'PstnNumber', 'PushToTalkAccessType', 'PushToTalkConnectionType', 'PutRecallHuntGroupObject', 'ReadBargeInSettingsForPersonResponse', 'ReadCallRecordingSettingsForPersonResponse', 'ReadCallToExtensionLocationsOfRoutingGroupResponse', 'ReadCallWaitingSettingsForPersonResponse', 'ReadCallerIDSettingsForPersonResponse', 'ReadDialPlanLocationsOfRoutingGroupResponse', 'ReadDoNotDisturbSettingsForPersonResponse', 'ReadForwardingSettingsForPersonResponse', 'ReadHotelingSettingsForPersonResponse', 'ReadIncomingPermissionSettingsForPersonResponse', 'ReadInternalDialingConfigurationForlocationResponse', 'ReadListOfAutoAttendantsResponse', 'ReadListOfCallParkExtensionsResponse', 'ReadListOfCallParksResponse', 'ReadListOfCallPickupsResponse', 'ReadListOfCallQueueAnnouncementFilesResponse', 'ReadListOfCallQueuesResponse', 'ReadListOfDialPatternsResponse', 'ReadListOfDialPlansResponse', 'ReadListOfHuntGroupsResponse', 'ReadListOfPagingGroupsResponse', 'ReadListOfRouteListsResponse', 'ReadListOfRoutingChoicesResponse', 'ReadListOfRoutingGroupsResponse', 'ReadListOfSchedulesResponse', 'ReadListOfTrunkTypesResponse', 'ReadListOfTrunksResponse', 'ReadListOfUCManagerProfilesResponse', 'ReadPSTNConnectionLocationsOfRoutingGroupResponse', 'ReadPersonsCallingBehaviorResponse', 'ReadPushtoTalkSettingsForPersonResponse', 'ReadReceptionistClientSettingsForPersonResponse', 'ReadRouteGroupForOrganizationResponse', 'ReadRouteListsOfRoutingGroupResponse', 'ReadUsageOfRoutingGroupResponse', 'ReadVoicemailSettingsForPersonResponse', 'RecallInformation', 'RecallTypeEnum', 'Record', 'RecordingStateEnum', 'RecurWeekly2', 'RecurWeeklyObject', 'RecurYearlyByDateObject', 'RecurYearlyByDayObject', 'Recurrence', 'RecurrenceObject', 'RecurrenceObject1', 'RedirectionInformation', 'RedirectionReasonEnum', 'RejectActionEnum', 'Repeat', 'ResponseStatus', 'ResponseStatusType', 'RetrieveCallQueueAgentsCallerIDInformationResponse', 'RetrieveExecutiveAssistantSettingsForPersonResponse', 'RetrieveListOfCallQueueCallerIDInformationResponse', 'RetrievepersonsApplicationServicesSettingsResponse', 'RetrievepersonsMonitoringSettingsResponse', 'RetrievepersonsOutgoingCallingPermissionsSettingsResponse', 'RingPattern', 'RouteGroup', 'RouteGroup1', 'RouteGroupUsageGetResponse', 'RouteGroupUsageRouteListGet', 'RouteIdentity', 'RouteIdentity1', 'RouteList', 'RouteListListGet', 'RouteListNumberPatch', 'RouteListNumberPatchResponse', 'RouteType', 'ScheduleEventObject', 'ScheduleShortDetails', 'Selection', 'Selection1', 'SendAllCalls', 'SendBusyCalls', 'SendBusyCalls1', 'SendUnansweredCalls', 'ServiceType', 'SipAddressesType', 'State', 'State1', 'Status', 'Status5', 'StorageType', 'TestCallRoutingResponse', 'Trunk', 'TrunkType', 'TrunkTypeWithDeviceType', 'Type', 'Type18', 'Type19', 'Type24', 'Type31', 'Type5', 'Type8', 'UnknownExtensionRouteIdentity', 'UpdateCallParkResponse', 'UpdateCallPickupResponse', 'UpdateCallQueueHolidayServiceBody', 'UpdateCallQueueNightServiceBody', 'UpdateEventForpersonsScheduleResponse', 'UpdateLocationBody', 'UpdateScheduleEventResponse', 'UpdateScheduleResponse', 'UpdateScheduleResponse1', 'UpdateSelectiveCallForwardingRuleForAutoAttendantResponse', 'UpdateSelectiveCallForwardingRuleForCallQueueResponse', 'UpdateSelectiveCallForwardingRuleForHuntGroupResponse', 'ValidateDialPatternResponse', 'ValidateExtensionsResponse', 'ValidateLocalGatewayFQDNAndDomainForTrunkBody', 'VirtualExtension', 'VoiceMailPartyInformation', 'VoiceMessageDetails', 'WebexCallingOrganizationSettingsApi', 'WebexCallingPersonSettingsApi', 'WebexCallingVoiceMessagingApi', 'Week']


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
    #: The party's number. Only present when the number is available and privacy is not enabled. The number can be digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, *73, and user@company.domain.
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


class CallPersonalityEnum(str, Enum):
    originator = 'originator'
    terminator = 'terminator'
    click_to_dial = 'clickToDial'


class CallStateEnum(str, Enum):
    connecting = 'connecting'
    alerting = 'alerting'
    connected = 'connected'
    held = 'held'
    remote_held = 'remoteHeld'
    disconnected = 'disconnected'


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
    #: The type of recall the incoming call is for. Park is the only type of recall currently supported but additional values may be added in the future.
    type: Optional[RecallTypeEnum]
    #: If the type is park, contains the details of where the call was parked. For example, if user A parks a call against user B and A is recalled for the park, then this field contains B's information in A's incoming call details. Only present when the type is park.
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
    #: The call session identifier of the call session the call belongs to. This can be used to correlate multiple calls that are part of the same call session.
    call_session_id: Optional[str]
    #:  The personality of the call.
    personality: Optional[CallPersonalityEnum]
    #: The current state of the call.
    state: Optional[CallStateEnum]
    #: The remote party's details. For example, if user A calls user B then B is the remote party in A's outgoing call details and A is the remote party in B's incoming call details.
    remote_party: Optional[PartyInformation]
    #: The appearance value for the call. The appearance value can be used to display the user's calls in an order consistent with the user's devices. Only present when the call has an appearance value assigned.
    appearance: Optional[int]
    #: The date and time the call was created.
    created: Optional[str]
    #: The date and time the call was answered. Only present when the call has been answered.
    answered: Optional[str]
    #: The list of details for previous redirections of the incoming call ordered from most recent to least recent. For example, if user B forwards an incoming call to user C, then a redirection entry is present for B's forwarding in C's incoming call details. Only present when there were previous redirections and the incoming call's state is alerting.
    redirections: Optional[list[RedirectionInformation]]
    #: The recall details for the incoming call. Only present when the incoming call is for a recall.
    recall: Optional[RecallInformation]
    #: The call's current recording state. Only present when the user's call recording has been invoked during the life of the call.
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
    #: The number of the called/calling party. Only present when the number is available and privacy is not enabled. The number can be digits or a URI. Some examples for number include: 1234, 2223334444, +12223334444, *73, user@company.domain
    number: Optional[str]
    #: Indicates whether privacy is enabled for the name and number.
    privacy_enabled: Optional[bool]
    #: The date and time the call history record was created. For a placed call history record, this is when the call was placed. For a missed call history record, this is when the call was disconnected. For a received call history record, this is when the call was answered.
    time: Optional[str]


class DialBody(ApiModel):
    #: The destination to be dialed. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, and sip:user@company.domain.
    destination: Optional[str]


class DialResponse(ApiModel):
    #: A unique identifier for the call which is used in all subsequent commands for the same call.
    call_id: Optional[str]
    #: A unique identifier for the call session the call belongs to. This can be used to correlate multiple calls that are part of the same call session.
    call_session_id: Optional[str]


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
    #: The destination to divert the call to. If toVoicemail is false, destination is required. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
    destination: Optional[str]
    #: If set to true, the call is diverted to voicemail. If no destination is specified, the call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the specified user's voicemail.
    to_voicemail: Optional[bool]


class TransferBody(ApiModel):
    #: The call identifier of the first call to transfer. This parameter is mandatory if either callId2 or destination is provided.
    call_id1: Optional[str]
    #: The call identifier of the second call to transfer. This parameter is mandatory if callId1 is provided and destination is not provided.
    call_id2: Optional[str]
    #: The destination to be transferred to. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain. This parameter is mandatory if callId1 is provided and callId2 is not provided.
    destination: Optional[str]


class ParkBody(ApiModel):
    #: The call identifier of the call to park.
    call_id: Optional[str]
    #: Identifes where the call is to be parked. If not provided, the call is parked against the parking user. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
    destination: Optional[str]
    #: If set totrue, the call is parked against an automatically selected member of the user's call park group and the destination parameter is ignored.
    is_group_park: Optional[bool]


class ParkResponse(ApiModel):
    #: The details of where the call has been parked.
    parked_against: Optional[PartyInformation]


class RetrieveBody(ApiModel):
    #: Identifies where the call is parked. The number field from the park command response can be used as the destination for the retrieve command. If not provided, the call parked against the retrieving user is retrieved. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
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
    #: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, *, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent successively.
    dtmf: Optional[str]


class PushBody(ApiModel):
    #: The call identifier of the call to push.
    call_id: Optional[str]


class PickupBody(ApiModel):
    #: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the user's call pickup group is picked up. The target can be digits or a URI. Some examples for target include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
    target: Optional[str]


class BargeInBody(ApiModel):
    #: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
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
        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or Click to Dial. Alerts occur on all the devices belonging to a user. When a user answers on one of these alerting devices, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, and sip:user@company.domain.
        :type destination: str
        """
        body = {}
        if destination is not None:
            body['destination'] = destination
        url = self.ep('dial')
        data = super().post(url=url, json=body)
        return DialResponse.parse_obj(data)

    def answer(self, call_id: str):
        """
        Answer an incoming call on a user's primary device.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('answer')
        super().post(url=url, json=body)
        return

    def reject(self, call_id: str, action: RejectActionEnum = None):
        """
        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is provided.
        :type action: RejectActionEnum
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        if action is not None:
            body['action'] = action
        url = self.ep('reject')
        super().post(url=url, json=body)
        return

    def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('hangup')
        super().post(url=url, json=body)
        return

    def hold(self, call_id: str):
        """
        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('hold')
        super().post(url=url, json=body)
        return

    def resume(self, call_id: str):
        """
        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('resume')
        super().post(url=url, json=body)
        return

    def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert a call to a destination or a user's voicemail. This is also commonly referred to as a Blind Transfer.

        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the specified user's voicemail.
        :type to_voicemail: bool
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if to_voicemail is not None:
            body['toVoicemail'] = to_voicemail
        url = self.ep('divert')
        super().post(url=url, json=body)
        return

    def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None):
        """
        Transfer two calls together.
        Unanswered incoming calls cannot be transferred but can be diverted using the divert API.
        If the user has only two calls and wants to transfer them together, the callId1 and callId2 parameters are optional and when not provided the calls are automatically selected and transferred.
        If the user has more than two calls and wants to transfer two of them together, the callId1 and callId2 parameters are mandatory to specify which calls are being transferred. Those are also commonly referred to as Attended Transfer, Consultative Transfer, or Supervised Transfer and will return a 204 response.
        If the user wants to transfer one call to a new destination but only when the destination responds, the callId1 and destination parameters are mandatory to specify the call being transferred and the destination.
        This is referred to as a Mute Transfer and is similar to the divert API with the difference of waiting for the destination to respond prior to transferring the call. If the destination does not respond, the call is not transferred. This will return a 201 response.

        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either callId2 or destination is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the second call to transfer. This parameter is mandatory if callId1 is provided and destination is not provided.
        :type call_id2: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain. This parameter is mandatory if callId1 is provided and callId2 is not provided.
        :type destination: str
        """
        body = {}
        if call_id1 is not None:
            body['callId1'] = call_id1
        if call_id2 is not None:
            body['callId2'] = call_id2
        if destination is not None:
            body['destination'] = destination
        url = self.ep('transfer')
        super().post(url=url, json=body)
        return

    def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> PartyInformation:
        """
        Park a connected call. The number field in the response can be used as the destination for the retrieve command to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifes where the call is to be parked. If not provided, the call is parked against the parking user. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param is_group_park: If set totrue, the call is parked against an automatically selected member of the user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        if destination is not None:
            body['destination'] = destination
        if is_group_park is not None:
            body['isGroupPark'] = is_group_park
        url = self.ep('park')
        data = super().post(url=url, json=body)
        return data["parkedAgainst"]

    def retrieve(self, destination: str = None) -> DialResponse:
        """
        Retrieve a parked call. A new call is initiated to perform the retrieval in a similar manner to the dial command. The number field from the park command response can be used as the destination for the retrieve command.

        :param destination: Identifies where the call is parked. The number field from the park command response can be used as the destination for the retrieve command. If not provided, the call parked against the retrieving user is retrieved. The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444, +12223334444, *73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        """
        body = {}
        if destination is not None:
            body['destination'] = destination
        url = self.ep('retrieve')
        data = super().post(url=url, json=body)
        return DialResponse.parse_obj(data)

    def start(self, call_id: str = None):
        """
        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('startRecording')
        super().post(url=url, json=body)
        return

    def stop(self, call_id: str = None):
        """
        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('stopRecording')
        super().post(url=url, json=body)
        return

    def pause(self, call_id: str = None):
        """
        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('pauseRecording')
        super().post(url=url, json=body)
        return

    def resume(self, call_id: str = None):
        """
        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('resumeRecording')
        super().post(url=url, json=body)
        return

    def transmit_dtmf(self, call_id: str = None, dtmf: str = None):
        """
        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to transmit DTMF digits for.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, *, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent successively.
        :type dtmf: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        if dtmf is not None:
            body['dtmf'] = dtmf
        url = self.ep('transmitDtmf')
        super().post(url=url, json=body)
        return

    def push(self, call_id: str = None):
        """
        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid when the assistant's call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str
        """
        body = {}
        if call_id is not None:
            body['callId'] = call_id
        url = self.ep('push')
        super().post(url=url, json=body)
        return

    def pickup(self, target: str = None) -> DialResponse:
        """
        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner to the dial command. When target is not present, the API pickups up a call from the user's call pickup group. When target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the user's call pickup group is picked up. The target can be digits or a URI. Some examples for target include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        """
        body = {}
        if target is not None:
            body['target'] = target
        url = self.ep('pickup')
        data = super().post(url=url, json=body)
        return DialResponse.parse_obj(data)

    def barge_in(self, target: str) -> DialResponse:
        """
        Barge-in on another user's answered call. A new call is initiated to perform the barge-in in a similar manner to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        """
        body = {}
        if target is not None:
            body['target'] = target
        url = self.ep('bargeIn')
        data = super().post(url=url, json=body)
        return DialResponse.parse_obj(data)

    def list_calls(self) -> Generator[Call, None, None]:
        """
        Get the list of details for all active calls associated with the user.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Call, params=params)

    def call_details(self, call_id: str) -> Call:
        """
        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        """
        url = self.ep(f'{call_id}')
        data = super().get(url=url)
        return Call.parse_obj(data)

    def list_call_history(self, type_: str = None, **params) -> Generator[ListCallHistoryResponse, None, None]:
        """
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed, missed, received) are returned.

        :param type_: The type of call history records to retrieve. If not specified, then all call history records are retrieved.
Possible values: placed, missed, received
        :type type_: str
        """
        if type_ is not None:
            params['type'] = type_
        url = self.ep('history')
        return self.session.follow_pagination(url=url, model=ListCallHistoryResponse, params=params)

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


class GetAvailableRecallHuntGroupsObject(ApiModel):
    #: A unique identifier for the hunt group.
    id: Optional[str]
    #: Unique name for the hunt group.
    name: Optional[str]


class Location(GetAvailableRecallHuntGroupsObject):
    #: The ID of the organization to which this location belongs.
    org_id: Optional[str]
    #: Time zone associated with this location.
    time_zone: Optional[str]
    #: The address of the location.
    address: Optional[Address]


class UpdateLocationBody(ApiModel):
    #: The name of the location.
    name: Optional[str]
    #: Time zone associated with this location, refer to this link (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone) for format.
    time_zone: Optional[str]
    #: Default email language.
    preferred_language: Optional[str]
    #: The address of the location.
    address: Optional[Address]


class ListLocationsResponse(ApiModel):
    items: Optional[list[Location]]


class CreateLocationBody(UpdateLocationBody):
    #: Location's phone announcement language.
    announcement_language: Optional[str]


class CreateLocationResponse(ApiModel):
    #: ID of the newly created location.
    id: Optional[str]


class LocationsApi(ApiChild, base='locations'):
    """
    Locations are used to organize Webex Calling (BroadCloud) features within physical locations. You can also create and inspect locations in Webex Control Hub. See Workspace Locations on Control Hub for more information.
    """

    def list(self, name: str = None, id: str = None, org_id: str = None, **params) -> Generator[Location, None, None]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param id: List locations by ID.
        :type id: str
        :param org_id: List locations in this organization. Only admin users of another organization (such as partners) may use this parameter.
        :type org_id: str
        """
        if name is not None:
            params['name'] = name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Location, params=params)

    def details(self, location_id: str) -> Location:
        """
        Shows details for a location, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        """
        url = self.ep(f'{location_id}')
        data = super().get(url=url)
        return Location.parse_obj(data)

    def create(self, org_id: str = None, name: str, time_zone: str, preferred_language: str, announcement_language: str, address: object) -> str:
        """
        Create a new Location for a given organization. Only an admin in a Webex Calling licensed organization can create a new Location.

        :param org_id: Create a location common attribute for this organization.
        :type org_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this link (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone) for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param address: The address of the location.
        :type address: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if preferred_language is not None:
            body['preferredLanguage'] = preferred_language
        if announcement_language is not None:
            body['announcementLanguage'] = announcement_language
        if address is not None:
            body['address'] = address
        url = self.ep()
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def update(self, location_id: str, org_id: str = None, name: str = None, time_zone: str = None, preferred_language: str = None, address: object = None):
        """
        Update details for a location, by ID.

        :param location_id: Update location common attributes for this location.
        :type location_id: str
        :param org_id: Update location common attributes for this organization.
        :type org_id: str
        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location, refer to this link (https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone) for format.
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param address: The address of the location.
        :type address: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if preferred_language is not None:
            body['preferredLanguage'] = preferred_language
        if address is not None:
            body['address'] = address
        url = self.ep(f'{location_id}')
        super().put(url=url, params=params, json=body)
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


class Status(str, Enum):
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
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
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
    #: Possible values: , country: `US`, locality: `Charlotte`, region: `North Carolina`, streetAddress: `1099 Bird Ave.`, type: `work`, postalCode: `99212`
    addresses: Optional[list[object]]
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg: mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]]


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
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your organization or an organization you manage. Presence information will not be shown if the authenticated user has disabled status sharing.
    last_activity: Optional[str]
    #: The users sip addresses
    sip_addresses: Optional[list[SipAddressesType]]
    #: The current presence status of the person. This will only be returned for people within your organization or an organization you manage. Presence information will not be shown if the authenticated user has disabled status sharing.
    status: Optional[Status]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an admin user for the person's organization.
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
    #: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is an admin user for the person's organization.
    login_enabled: Optional[bool]


class PeopleApi(ApiChild, base='people'):
    """
    People are registered users of Webex. Searching and viewing People requires an auth token with a scope of spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token with spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token with the spark-admin:people_write and spark-admin:people_read scope.
    A person's call settings are for Webex Calling and necessitate Webex Calling licenses.
    To learn more about managing people in a room see the Memberships API. For information about how to allocate Hybrid Services licenses to people, see the Managing Hybrid Services guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin users can omit these fields and list all users in their organization.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be returned for people within your organization or an organization you manage. Presence information will not be returned if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData parameter as true. Admin users can list all users in a location or with a specific phone number.
        Lookup by email is only supported for people within the same org or where a partner admin relationship is in place.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are required. With the exception of partner admins and a managed org relationship, people lookup by email is only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided then presence information (such as the lastActivity or status properties) will not be included in the response.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners) may use this parameter.
        :type org_id: str
        :param calling_data: Include Webex Calling user details in the response.
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

    def create(self, calling_data: bool = None, emails: List[str], phone_numbers: List[object] = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: List[object] = None, site_urls: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        At least one of the following body parameters is required to create a new user: displayName, firstName, lastName.
        Currently, users may have only one email address associated with their account. The emails parameter is an array, which accepts multiple values to allow for future expansion, but currently only one email address will be used for the new user.
        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData parameter as true.
        When doing attendee management, append #attendee to the siteUrl parameter (e.g. mysite.webex.com#attendee) to make the new user an attendee for a site.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param emails: The email addresses of the person. Only one email address is allowed per person.
Possible values: john.andersen@example.com
        :type emails: List[str]
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling license.
        :type phone_numbers: List[object]
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license.
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
        :param roles: An array of role strings representing the roles to which this admin user belongs.
Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person.
Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
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
Possible values: , country: `US`, locality: `Charlotte`, region: `North Carolina`, streetAddress: `1099 Bird Ave.`, type: `work`, postalCode: `99212`
        :type addresses: List[object]
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg: mysite.webex.com#attendee)
Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        body = {}
        if emails is not None:
            body['emails'] = emails
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if extension is not None:
            body['extension'] = extension
        if location_id is not None:
            body['locationId'] = location_id
        if display_name is not None:
            body['displayName'] = display_name
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if avatar is not None:
            body['avatar'] = avatar
        if org_id is not None:
            body['orgId'] = org_id
        if roles is not None:
            body['roles'] = roles
        if licenses is not None:
            body['licenses'] = licenses
        if department is not None:
            body['department'] = department
        if manager is not None:
            body['manager'] = manager
        if manager_id is not None:
            body['managerId'] = manager_id
        if title is not None:
            body['title'] = title
        if addresses is not None:
            body['addresses'] = addresses
        if site_urls is not None:
            body['siteUrls'] = site_urls
        url = self.ep()
        data = super().post(url=url, params=params, json=body)
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be displayed for people within your organization or an organization you manage. Presence information will not be shown if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, calling_data: bool = None, show_all_types: bool = None, display_name: str, emails: List[str] = None, phone_numbers: List[object] = None, extension: str = None, location_id: str = None, first_name: str = None, last_name: str = None, nick_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: List[object] = None, site_urls: List[str] = None, login_enabled: bool = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is already an existing calling user.
        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to the respective siteUrl and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the meeting array, and remove that site from the siteurl parameter.
        Removing the attendee privilege for a  user on a meeting site is done by removing that sitename#attendee  from the siteUrls array. The showAllTypes parameter must be set to true.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param display_name: The full name of the person.
        :type display_name: str
        :param emails: The email addresses of the person. Only one email address is allowed per person.
Possible values: john.andersen@example.com
        :type emails: List[str]
        :param phone_numbers: Phone numbers for the person. Can only be set for Webex Calling. Needs a Webex Calling license.
        :type phone_numbers: List[object]
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param nick_name: The nickname of the person if configured. Set to the firstName automatically in update request.
        :type nick_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs.
Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person.
Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh, Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
Possible values: , country: `US`, locality: `Charlotte`, region: `North Carolina`, streetAddress: `1099 Bird Ave.`, type: `work`, postalCode: `99212`
        :type addresses: List[object]
        :param site_urls: One or several site names where this user has a role (host or attendee). Append #attendee to the site name to designate the attendee role on that site.
Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is an admin user for the person's organization.
        :type login_enabled: bool
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        if show_all_types is not None:
            params['showAllTypes'] = show_all_types
        body = {}
        if display_name is not None:
            body['displayName'] = display_name
        if emails is not None:
            body['emails'] = emails
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if extension is not None:
            body['extension'] = extension
        if location_id is not None:
            body['locationId'] = location_id
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if nick_name is not None:
            body['nickName'] = nick_name
        if avatar is not None:
            body['avatar'] = avatar
        if org_id is not None:
            body['orgId'] = org_id
        if roles is not None:
            body['roles'] = roles
        if licenses is not None:
            body['licenses'] = licenses
        if department is not None:
            body['department'] = department
        if manager is not None:
            body['manager'] = manager
        if manager_id is not None:
            body['managerId'] = manager_id
        if title is not None:
            body['title'] = title
        if addresses is not None:
            body['addresses'] = addresses
        if site_urls is not None:
            body['siteUrls'] = site_urls
        if login_enabled is not None:
            body['loginEnabled'] = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, json=body)
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
        Get profile details for the authenticated user. This is the same as GET /people/{personId} using the Person ID associated with your Auth token.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = calling_data
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

class ListCallParkObject(GetAvailableRecallHuntGroupsObject):
    #: Name of the location for the call park.
    location_name: Optional[str]
    #: Id of the location for the call park.
    location_id: Optional[str]


class ListAutoAttendantObject(ListCallParkObject):
    #: Auto attendant phone number.  Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Auto attendant extension.  Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]


class GetDetailsForCallParkExtensionResponse(ApiModel):
    #: The extension for the call park extension.
    extension: Optional[str]
    #: Unique name for the call park extension.
    name: Optional[str]


class CreateAutoAttendantBody(GetDetailsForCallParkExtensionResponse):
    #: Auto attendant phone number.  Either phoneNumber or extension is mandatory.
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


class NewNumber(ApiModel):
    #: Enable/disable to play new number announcement.
    enabled: Optional[bool]
    #: Incoming destination phone number to be announced.
    destination: Optional[str]


class GetCallForwardAlwaysSettingObject(NewNumber):
    #: If true, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool]
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    send_to_voicemail_enabled: Optional[bool]


class CallForwardRulesModifyObject(ApiModel):
    #: A unique identifier for the auto attendant call forward selective rule.
    id: Optional[str]
    #: Flag to indicate if always call forwarding selective rule criteria is active. If not set, flag will be set to false.
    enabled: Optional[bool]


class CallForwardRulesObject(CallForwardRulesModifyObject):
    #: Unique name of rule.
    name: Optional[str]
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers is allowed. Use Any private Number in the comma-separated value to indicate rules that match incoming calls from a private number. Use Any unavailable number in the comma-separated value to match incoming calls from an unavailable number.
    calls_from: Optional[str]
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str]
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str]


class AutoAttendantCallForwardSettingsDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesObject]]


class AutoAttendantCallForwardSettingsModifyDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject]
    #: Rules for selectively forwarding calls. (Rules which are omitted in the list will not be deleted.)
    rules: Optional[list[CallForwardRulesModifyObject]]


class Selection(str, Enum):
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
    selection: Optional[Selection]


class Selection1(str, Enum):
    #: Rule matches for calls from any number.
    any = 'ANY'
    #: Rule matches based on the numbers and options in customNumbers.
    custom = 'CUSTOM'


class CallForwardSelectiveCallsFromCustomNumbersObject(ApiModel):
    #: Match if caller ID indicates the call is from a private number.
    private_number_enabled: Optional[bool]
    #: Match if caller Id is unavailable.
    unavailable_number_enabled: Optional[bool]
    #: Array of number strings to be matched against incoming caller Id.
    numbers: Optional[list[str]]


class CallForwardSelectiveCallsFromObject(ApiModel):
    #: If CUSTOM, use customNumbers to specify which incoming caller ID values cause this rule to match. ANY means any incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[Selection1]
    #: Custom rules for matching incoming caller Id information. Mandatory if the selection option is set to CUSTOM.
    custom_numbers: Optional[CallForwardSelectiveCallsFromCustomNumbersObject]


class Type5(str, Enum):
    #: Indicates that the given phoneNumber or extension associated with this rule's containing object is a primary number or extension.
    primary = 'PRIMARY'
    #: Indicates that the given phoneNumber or extension associated with this rule's containing object is an alternate number or extension.
    alternate = 'ALTERNATE'


class CallForwardSelectiveCallsToNumbersObject(ApiModel):
    #: AutoCalls To phone number. Either phone number or extension should be present as mandatory.
    phone_number: Optional[str]
    #: Calls To extension.  Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Calls to type options.
    type: Optional[Type5]


class CallForwardSelectiveCallsToObject(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class CallForwardSelectiveCallsToObject1(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class Option(str, Enum):
    #: Alert parking user only.
    alert_parking_user_only = 'ALERT_PARKING_USER_ONLY'
    #: Alert parking user first, then hunt group.
    alert_parking_user_first_then_hunt_group = 'ALERT_PARKING_USER_FIRST_THEN_HUNT_GROUP'
    #: Alert hunt group only.
    alert_hunt_group_only = 'ALERT_HUNT_GROUP_ONLY'


class PutRecallHuntGroupObject(ApiModel):
    #: Alternate user which is a hunt group Id for call park recall alternate destination.
    hunt_group_id: Optional[str]
    #: Call park recall options.
    option: Optional[Option]


class CreateCallPickupBody(ApiModel):
    #: Unique name for the call pickup. The maximum length is 80.
    name: Optional[str]
    #: Array of Id strings of people, including workspaces, that are added to call pickup.
    agents: Optional[list[str]]


class GetRecallHuntGroupObject(PutRecallHuntGroupObject):
    #: Unique name for the hunt group.
    hunt_group_name: Optional[str]


class Type8(str, Enum):
    #: Indicates that this object is a user.
    people = 'PEOPLE'
    #: Indicates that this object is a place.
    place = 'PLACE'


class GetUserNumberItemObject(ApiModel):
    #: Phone number of a person or workspace.
    external: Optional[str]
    #: Extension of a person or workspace.
    extension: Optional[str]
    #: Flag to indicate a primary phone.
    primary: Optional[bool]


class GetPersonPlaceCallParksObject(ApiModel):
    #: Id of a person or workspace.
    id: Optional[str]
    #: First name of a person or workspace.
    first_name: Optional[str]
    #: Last name of a person or workspace.
    last_name: Optional[str]
    #: Display name of a person or workspace.
    display_name: Optional[str]
    #: Type of the person or workspace.
    type: Optional[Type8]
    #: Email of a person or workspace.
    email: Optional[str]
    #: List of phone numbers of a person or workspace.
    numbers: Optional[list[GetUserNumberItemObject]]


class GetRecallHuntGroupObject1(PutRecallHuntGroupObject):
    #: Unique name for the hunt group.
    hunt_group_name: Optional[str]


class CallParkSettingsObject(ApiModel):
    #: Ring pattern for when this callpark is called.
    ring_pattern: Optional[RingPattern]
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up within the set time, then the call will be recalled based on the Call Park Recall setting.
    recall_time: Optional[int]
    #: Amount of time within 30 and 600 seconds the Call Park will be parked. If the call isn't picked up, the call will revert back to the hunt group (after the person who parked the call is alerted).
    hunt_wait_time: Optional[int]


class ListCallParkExtensionObject(ListCallParkObject):
    #: The extension for the call park extension.
    extension: Optional[str]


class ListCallQueueObject(CallForwardRulesModifyObject):
    #: Unique name for the call queue.
    name: Optional[str]
    #: Name of location for call queue.
    location_name: Optional[str]
    #: Id of location for call queue.
    location_id: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Primary phone extension of the call queue.
    extension: Optional[str]


class HuntPolicySelection(ApiModel):
    #: This option cycles through all agents after the last agent that took a call. It sends calls to the next available agent.
    circular: Optional[str]
    #: Sends calls through the queue of agents in order, starting from the top each time.
    regular: Optional[str]
    #: Sends calls to all agents at once
    simultaneous: Optional[str]
    #: Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the next agent who has been idle the second longest, and so on until the call is answered.
    uniform: Optional[str]
    #: Sends calls to idle agents based on percentages you assign to each agent (up to 100).
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


class DistinctiveRing(ApiModel):
    #: Whether or not the distinctive ring is enabled.
    enabled: Optional[bool]
    #: Ring pattern for when this call queue is called. Only available when distinctiveRing is enabled for the call queue.
    ring_pattern: Optional[RingPattern]


class PostCallQueueCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: Settings for when the call into the hunt group is not answered.
    call_bounce: Optional[CallBounce]
    #: Whether or not the call queue has the distinctive ring option enabled.
    distinctive_ring: Optional[DistinctiveRing]


class Action6(str, Enum):
    #: The caller hears a fast busy tone.
    perform_busy_treatment = 'PERFORM_BUSY_TREATMENT'
    #: The caller hears ringing until they disconnect.
    play_ringing_until_caller_hangs_up = 'PLAY_RINGING_UNTIL_CALLER_HANGS_UP'
    #: Number where you want to transfer overflow calls.
    transfer_to_phone_number = 'TRANSFER_TO_PHONE_NUMBER'


class Overflow(ApiModel):
    #: Indicates how to handle new calls when the queue is full.
    action: Optional[Action6]
    #: When true, forwards all calls to a voicemail service of an internal number. This option is ignored when an external transferNumber is entered.
    send_to_voicemail: Optional[bool]
    #: Destination number for overflow calls when action is set to TRANSFER_TO_PHONE_NUMBER.
    transfer_number: Optional[str]
    #: After calls wait for the configured number of seconds and no agent is available, the overflow treatment is triggered.
    overflow_after_wait_enabled: Optional[bool]
    #: Number of seconds to wait before the overflow treatment is triggered when no agent is available.
    overflow_after_wait_time: Optional[int]
    #: Indicate overflow audio to be played, otherwise, callers will hear the hold music until the call is answered by a user.
    play_overflow_greeting_enabled: Optional[bool]
    #: Indicates how to handle new calls when the queue is full.
    greeting: Optional[Greeting]
    #: Array of announcement file name strings to be played as overflow greetings. These files are from the list of announcements files associated with this call queue.
    audio_files: Optional[list[str]]


class CallQueueQueueSettingsObject(ApiModel):
    #: The maximum number of calls for this call queue. Once this number is reached, the overflow settings are triggered (max 50).
    queue_size: Optional[int]
    #: Play ringing tone to callers when their call is set to an available agent.
    call_offer_tone_enabled: Optional[bool]
    #: Reset caller statistics upon queue entry.
    reset_call_statistics_enabled: Optional[bool]
    #: Settings for incoming calls exceed queueSize.
    overflow: Optional[Overflow]


class PostPersonPlaceObject(ApiModel):
    #: ID of person or workspace.
    id: Optional[str]
    #: Weight of person or workspace. Only applied when call policy is WEIGHTED.
    weight: Optional[str]


class AlternateNumbersWithPattern(ApiModel):
    #: Alternate phone number for the hunt group.
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the hunt group.
    ring_pattern: Optional[RingPattern]


class AlternateNumberSettings(ApiModel):
    #: Distinctive Ringing selected for the alternate numbers in the call queue overrides the normal ringing patterns set for the Alternate Numbers.
    distinctive_ring_enabled: Optional[bool]
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]


class GetPersonPlaceObject(PostPersonPlaceObject):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Phone number of person or workspace.
    phone_number: Optional[str]
    #: Extension of person or workspace.
    extension: Optional[str]


class GetAnnouncementFileInfo(ApiModel):
    #: Name of greeting file.
    file_name: Optional[str]
    #: Size of greeting file in bytes.
    file_size: Optional[str]


class BusinessContinuity(NewNumber):
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class Always(BusinessContinuity):
    #: If true, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool]


class CallForwardRulesGet(CallForwardRulesModifyObject):
    #: Unique name of rule.
    name: Optional[str]
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers is allowed. Use Any private Number in the comma-separated value to indicate rules that match incoming calls from a private number. Use Any unavailable number in the comma-separated value to match incoming calls from an unavailable number.
    call_from: Optional[str]
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str]
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str]


class CallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one rule for forwarding applied for call forwarding to be active.
    selective: Optional[Always]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesGet]]


class CallForwarding1(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one rule for forwarding applied for call forwarding to be active.
    selective: Optional[Always]
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesModifyObject]]


class CallsFrom(ApiModel):
    #: If CUSTOM, use customNumbers to specify which incoming caller ID values cause this rule to match. ANY means any incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[Selection1]
    #: Custom rules for matching incoming caller ID information.
    custom_numbers: Optional[CallForwardSelectiveCallsFromCustomNumbersObject]


class CallsTo(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class CallsTo1(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


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
    #: When originatorType is trunk, originatorId is a valid trunk, this trunk belongs to a route group which is assigned to a route list with the name routeListA and originatorNumber is a number assigned to routeListA. routeListA is returned here. This element is returned when callSourceType is ROUTE_LIST.
    route_list_name: Optional[str]
    #: Foute list Id.
    route_list_id: Optional[str]
    #: When originatorType is trunk, originatorId is a valid trunk with name trunkA, trunkA belongs to a route group which is assigned to a route list with name routeListA,  trunkA is also assigned to dialPlanA as routing choice, dialPlanA has dialPattern xxxx assigned. If the originatorNumber matches the dialPattern xxxx, dialPlanA is returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_plan_name: Optional[str]
    #: When originatorType is trunk, originatorId is a valid trunk with the name trunkA, trunkA belongs to a route group which is assigned to a route list with the name routeListA,  trunkA is also assigned to dialPlanA as routing choice, dialPlanA has dialPattern xxxx assigned. If the originatorNumber matches the dialPattern xxxx, dialPattern xxxx is returned. This element is returned when callSourceType is DIAL_PATTERN.
    dial_pattern: Optional[str]
    #: Dial plan Id.
    dial_plan_id: Optional[str]


class DestinationType(ApiModel):
    #: Matching destination is a person or workspace with details in the hostedAgent field.
    hosted_agent: Optional[str]
    #: Matching destination is a calling feature like auto-attendant or hunt group with details in the hostedFeature field.
    hosted_feature: Optional[str]
    #: Matching destination routes into a separate PBX with details in the pbxUser field.
    pbx_user: Optional[str]
    #: Matching destination routes into a PSTN phone number with details in the pstnNumber field.
    pstn_number: Optional[str]
    #: Matching destination routes into a virtual extension with details in the virtualExtension field.
    virtual_extension: Optional[str]
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


class HostedAgent(ApiModel):
    #: Person or workspace's Id.
    id: Optional[str]
    #: Type of agent for call destination.
    type: Optional[Type8]
    #: Person or workspace's first name.
    first_name: Optional[str]
    #: Person or workspace's last name.
    last_name: Optional[str]
    #: Name of location for a person or workspace.
    location_name: Optional[str]
    #: Location Id for a person or workspace.
    location_id: Optional[str]
    #: Person or workspace's phone number.
    phone_number: Optional[str]
    #: Person or workspace's extension.
    extension: Optional[str]


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


class HostedFeature(ListCallParkObject):
    #: Service instance type.
    type: Optional[ServiceType]
    #: User or place's phone number.
    phone_number: Optional[str]
    #: User or place's extension.
    extension: Optional[str]


class PstnNumber(ApiModel):
    #: Trunk name.
    trunk_name: Optional[str]
    #: Trunk Id.
    trunk_id: Optional[str]
    #: Route group name.
    route_group_name: Optional[str]
    #: Route group Id.
    route_group_id: Optional[str]
    #: Location of the trunk; required if trunkName is returned.
    trunk_location_name: Optional[str]
    #: Location Id of the trunk; required if trunkName is returned.
    trunk_location_id: Optional[str]


class PbxUser(PstnNumber):
    #: Dial plan name that the called string matches.
    dial_plan_name: Optional[str]
    #: Dial plan Id.
    dial_plan_id: Optional[str]
    #: Dial pattern that the called string matches.
    dial_pattern: Optional[str]


class VirtualExtension(PstnNumber):
    #: Virtual extension Id.
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
    #: Location Id if the virtual extension is at the location level, empty if it is at customer level.
    location_id: Optional[str]


class RouteList(ListCallParkObject):
    #: Name of the route group the route list is associated with.
    route_group_name: Optional[str]
    #: Id of the route group the route list is associated with.
    route_group_id: Optional[str]


class FeatureAccessCode(ApiModel):
    #: FAC code.
    code: Optional[str]
    #: FAC name.
    name: Optional[str]


class Emergency(PstnNumber):
    #: Indicates if RedSky is in use.
    is_red_sky: Optional[bool]


class Status5(str, Enum):
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


class ListHuntGroupObject(CallForwardRulesModifyObject):
    #: Unique name for the hunt group.
    name: Optional[str]
    #: Name of the location for the hunt group.
    location_name: Optional[str]
    #: Id of location for hunt group.
    location_id: Optional[str]
    #: Primary phone number of the hunt group.
    phone_number: Optional[str]
    #: Primary phone extension of the hunt group.
    extension: Optional[str]


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
    #: If forwardEnabled is true, enables and disables sending incoming to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]


class PostHuntGroupCallPolicyObject(ApiModel):
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[HuntPolicySelection]
    #: If false, then the option is treated as "Advance when busy": the hunt group won't ring agents when they're on a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is advanced to them, then the call will wait until that hunt group agent isn't busy.
    waiting_enabled: Optional[bool]
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[NoAnswer]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[BusinessContinuity]


class GetPersonPlaceObject1(PostPersonPlaceObject):
    #: First name of person or workspace.
    first_name: Optional[str]
    #: Last name of person or workspace.
    last_name: Optional[str]
    #: Phone number of person or workspace.
    phone_number: Optional[str]
    #: Extension of person or workspace.
    extension: Optional[str]


class CallsTo4(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]]


class Type18(str, Enum):
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
    type: Optional[Type18]
    #: Enable/disable to route voice mail.
    voicemail_enabled: Optional[bool]
    #: Announcements details.
    announcements: Optional[Announcements]


class Type19(str, Enum):
    #: Intercept all outbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow local outbound calls.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class Outgoing(ApiModel):
    #: Outbound call modes
    type: Optional[Type19]
    #: Enable/disable to route all outbound calls to phone number.
    transfer_enabled: Optional[bool]
    #: If enabled, set outgoing destination phone number.
    destination: Optional[str]


class RouteType(ApiModel):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group: Optional[str]
    #: Connection between Webex Calling and the premises.
    trunk: Optional[str]


class RouteIdentity(GetAvailableRecallHuntGroupsObject):
    #: Type associated with the identity.
    type: Optional[RouteType]


class UnknownExtensionRouteIdentity(ApiModel):
    #: Id of the route type.
    id: Optional[str]
    #: Type associated with the identity.
    type: Optional[RouteType]


class CallingLineId(ApiModel):
    #: Group calling line ID name. By default the Org name.
    name: Optional[str]
    #: Directory Number / Main number in E.164 Format.
    phone_number: Optional[str]


class CallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to your local calling area.
    local = 'LOCAL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls within your country of origin, but outside of your local area code.
    toll = 'TOLL'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before the number is dialed.
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


class Action9(str, Enum):
    #: Callers at this location can make these types of calls.
    allow = 'ALLOW'
    #: Callers at this location can't make these types of calls.
    block = 'BLOCK'
    #: Callers must enter the authorization code that you set before placing an outgoing call.
    auth_code = 'AUTH_CODE'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer number autoTransferNumber1.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer number autoTransferNumber2.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer number autoTransferNumber3.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermissionObject(ApiModel):
    #: Below are the call type values.
    call_type: Optional[CallType]
    #: Allows to configure settings for each call type.
    action: Optional[Action9]
    #: If enabled, allow the person to transfer or forward internal calls.
    transfer_enabled: Optional[bool]


class AccessCodes(ApiModel):
    #: Access code number.
    code: Optional[str]
    #: Access code description.
    description: Optional[str]


class ListPagingGroupObject(ListCallParkObject):
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    extension: Optional[str]


class GetPagingGroupAgentObject(CallForwardSelectiveCallsToNumbersObject):
    #: Agents Id.
    id: Optional[str]
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]


class GetPagingGroupAgentObject1(CallForwardSelectiveCallsToNumbersObject):
    #: Agents Id.
    id: Optional[str]
    #: Agents first name. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Agents last name. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]


class State1(str, Enum):
    #: Active state.
    active = 'ACTIVE'
    #: Inactive state
    inactive = 'INACTIVE'


class Owner(ApiModel):
    #: Id of the owner to which PSTN Phone number is assigned.
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
    location: Optional[GetAvailableRecallHuntGroupsObject]
    owner: Optional[Owner]


class NetworkConnectionType(str, Enum):
    #: Use public internet for the location's connection type.
    public_internet = 'PUBLIC_INTERNET'
    #: Use private network connect for the location's connection type.
    private_network = 'PRIVATE_NETWORK'


class RouteIdentity1(GetAvailableRecallHuntGroupsObject):
    #: Type associated with the identity.
    type: Optional[RouteType]


class Type24(str, Enum):
    #: Business hours schedule type.
    business_hours = 'businessHours'
    #: Holidays schedule type.
    holidays = 'holidays'


class ListScheduleObject(ListCallParkObject):
    #: Type of the schedule.
    type: Optional[Type24]


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


class RecurrenceObject(ApiModel):
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


class GetScheduleEventObject(GetAvailableRecallHuntGroupsObject):
    #: Start Date of Event.
    start_date: Optional[str]
    #: End Date of Event.
    end_date: Optional[str]
    #: Start time of event.
    start_time: Optional[str]
    #: End time of event.
    end_time: Optional[str]
    #: An indication of whether given event is an all-day event or not.
    all_day_enabled: Optional[bool]
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject]


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
    #: An indication of whether given event is an all-day event or not. Mandatory if the startTime and endTime are not defined.
    all_day_enabled: Optional[bool]
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject1]


class ModifyScheduleEventListObject(ScheduleEventObject):
    #: New name for the event.
    new_name: Optional[str]


class BlockRepeatedDigits(ApiModel):
    #: If enabled, passcode should not contain repeated digits.
    enabled: Optional[bool]
    #: Maximum number of repeaed digits. Min 1, Max 6.
    max: Optional[int]


class BlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    enabled: Optional[bool]
    #: Number of ascending digits in sequence. Min 2, Max 5.
    number_of_ascending_digits: Optional[int]
    #: Number of descending digits in sequence. Min 2, Max 5.
    number_of_descending_digits: Optional[int]


class Length(ApiModel):
    #: Min 2, Max 15.
    min: Optional[int]
    #: Min 3, Max 30.
    max: Optional[int]


class DefaultVoicemailPinRules(ApiModel):
    #: If enabled, the passcode should not contain repeated pattern.
    block_repeated_patterns_enabled: Optional[bool]
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
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
    #: Number of days for password expiry. Min 15, Max 180.
    number_of_days: Optional[int]


class BlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    enabled: Optional[bool]
    #: Number of previous passcodes. Min 1, Max 10.
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


class Greeting11(str, Enum):
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets the customer know they are still connected.
    system = 'SYSTEM'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


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


class FaxMessage(ApiModel):
    #: Enable/disable fax messaging.
    enabled: Optional[bool]
    #: Phone number to receive fax messages.
    phone_number: Optional[str]
    #: Extension to receive fax messages.
    extension: Optional[int]


class EmailCopyOfMessage(ApiModel):
    #: Enable/disable to email message copy.
    enabled: Optional[bool]
    #: Email message copy to email address provided.
    email_id: Optional[str]


class DialPatternAction(ApiModel):
    #: Add action, when adding a new dial pattern
    add: Optional[str]
    #: Delete action, when deleting an existing dial pattern
    delete: Optional[str]


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


class DialPlan(GetAvailableRecallHuntGroupsObject):
    #: Id of route type associated with the dial plan.
    route_id: Optional[str]
    #: Name of route type associated with the dial plan.
    route_name: Optional[str]
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType]


class ModifyDialPlanBody(ApiModel):
    #: A unique name for the dial plan.
    name: Optional[str]
    #: Id of route type associated with the dial plan.
    route_id: Optional[str]
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType]


class TrunkType(ApiModel):
    #: For Cisco CUBE Local Gateway.
    registering: Optional[str]
    #: For Cisco Unified Border Element, Oracle ACME Session Border Controller, AudioCodes Session Border Controller, Ribbon Session Border Controller.
    certificate_based: Optional[str]


class Trunk(GetAvailableRecallHuntGroupsObject):
    #: Location associated with the trunk.
    location: Optional[GetAvailableRecallHuntGroupsObject]
    #: Trunk in use flag.
    in_use: Optional[bool]
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]


class ValidateLocalGatewayFQDNAndDomainForTrunkBody(ApiModel):
    #: FQDN or SRV address of the trunk.
    address: Optional[str]
    #: Domain name of the trunk.
    domain: Optional[str]
    #: FQDN port of the trunk.
    port: Optional[int]


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
    #: Error Tracking Id.
    tracking_id: Optional[str]


class DeviceType(ApiModel):
    #: Device type assosiated with trunk configuration.
    device_type: Optional[str]
    #: Min Concurrent call. Required for static certificate based trunk.
    min_concurrent_calls: Optional[int]
    #: Max Concurrent call. Required for static certificate based trunk.
    max_concurrent_calls: Optional[int]


class TrunkTypeWithDeviceType(ApiModel):
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]
    #: Device types for trunk configuration.
    device_types: Optional[list[DeviceType]]


class RouteGroup(GetAvailableRecallHuntGroupsObject):
    #: Flag to indicate if the route group is used.
    in_use: Optional[bool]


class LocalGateways(GetAvailableRecallHuntGroupsObject):
    #: Location Id to which local gateway belongs.
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


class RouteListListGet(ListCallParkObject):
    #: UUID of the route group associated with Route List.
    route_group_id: Optional[str]
    #: Name of the Route Group associated with Route List.
    route_group_name: Optional[str]


class ModifyRouteListBody(ApiModel):
    #: Route List new name.
    name: Optional[str]
    #: New route group Id.
    route_group_id: Optional[str]


class RouteGroup1(GetAvailableRecallHuntGroupsObject):
    #: Flag to indicate if the route group is used.
    in_use: Optional[bool]


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
    #: Status of the number. Possible vlues are INVALID, DUPLICATE, DUPLICATE_IN_LIST, or UNAVAILABLE.
    number_status: Optional[NumberStatus]
    #: Message of the number add status.
    message: Optional[str]


class RouteGroupUsageGetResponse(GetAvailableRecallHuntGroupsObject):
    #: In use flag.
    in_use: Optional[bool]


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
    #: Calls are handled according to the Night Service configuration. If the Night Service action is set to none, then this is equivalent to this policy being set to none (that is, calls remain in the queue).
    night_service = 'NIGHT_SERVICE'
    #: Calls are removed from the queue and are provided with ringing until the caller releases the call. The ringback tone played to the caller is localized according to the country code of the caller.
    ringing = 'RINGING'
    #: Calls are removed from the queue and are provided with an announcement that is played in a loop until the caller releases the call.
    announcement = 'ANNOUNCEMENT'


class GetDetailsForCallQueueStrandedCallsResponse(ApiModel):
    #: Specifies call processing action type.
    action: Optional[Action15]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[CallQueueAudioFilesObject]]


class UpdateCallQueueHolidayServiceBody(GetDetailsForCallQueueStrandedCallsResponse):
    #: Enable or Disable the call queue holiday service routing policy.
    holiday_service_enabled: Optional[bool]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from holidaySchedules list)
    holiday_schedule_level: Optional[HolidayScheduleLevel]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]


class UpdateCallQueueNightServiceBody(GetDetailsForCallQueueStrandedCallsResponse):
    #: Enable or disable call queue night service routing policy.
    night_service_enabled: Optional[bool]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules list)
    business_hours_level: Optional[HolidayScheduleLevel]
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of pre-configured Audio Files.
    manual_audio_files: Optional[list[CallQueueAudioFilesObject]]


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


class GetDetailsForAutoAttendantResponse(CreateAutoAttendantBody):
    #: A unique identifier for the auto attendant.
    id: Optional[str]
    #: Flag to indicate if auto attendant number is enabled or not.
    enabled: Optional[bool]
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool]
    #: Language for the auto attendant.
    language: Optional[str]


class CreateAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant.
    id: Optional[str]


class GetCallForwardingSettingsForAutoAttendantResponse(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsDetailsObject]


class UpdateCallForwardingSettingsForAutoAttendantBody(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsModifyDetailsObject]


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
    #: Settings related to the rule matching based on incoming caller Id.
    calls_from: Optional[CallForwardSelectiveCallsFromObject]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject]


class CreateSelectiveCallForwardingRuleForAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant call forward selective rule.
    id: Optional[str]


class GetSelectiveCallForwardingRuleForAutoAttendantResponse(CallForwardRulesModifyObject):
    #: Unique name for the selective rule in the auto attendant.
    name: Optional[str]
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str]
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str]
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject]
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CallForwardSelectiveCallsFromObject]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject1]


class UpdateSelectiveCallForwardingRuleForAutoAttendantResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class ReadListOfCallParksResponse(ApiModel):
    #: Array of call parks.
    call_parks: Optional[list[ListCallParkObject]]


class CreateCallParkBody(CreateCallPickupBody):
    #: Recall options that are added to the call park.
    recall: Optional[PutRecallHuntGroupObject]


class CreateCallParkResponse(ApiModel):
    #: ID of the newly created call park.
    id: Optional[str]


class GetDetailsForCallParkResponse(GetAvailableRecallHuntGroupsObject):
    #: Recall options that are added to call park.
    recall: Optional[GetRecallHuntGroupObject]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceCallParksObject]]


class UpdateCallParkResponse(ApiModel):
    #: ID of the target call park.
    id: Optional[str]


class GetAvailableAgentsFromCallParksResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceCallParksObject]]


class GetAvailableRecallHuntGroupsFromCallParksResponse(ApiModel):
    #: Array of available recall hunt groups.
    hunt_groups: Optional[list[GetAvailableRecallHuntGroupsObject]]


class GetCallParkSettingsResponse(ApiModel):
    #: Recall options that are added to call park.
    call_park_recall: Optional[GetRecallHuntGroupObject1]
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


class GetDetailsForCallPickupResponse(GetAvailableRecallHuntGroupsObject):
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceCallParksObject]]


class UpdateCallPickupResponse(ApiModel):
    #: ID of the target call pickup.
    id: Optional[str]


class GetAvailableAgentsFromCallPickupsResponse(ApiModel):
    #: Array of agents.
    agents: Optional[list[GetPersonPlaceCallParksObject]]


class ReadListOfCallQueuesResponse(ApiModel):
    #: Array of call queues.
    queues: Optional[list[ListCallQueueObject]]


class CreateCallQueueBody(GetDetailsForCallParkExtensionResponse):
    #: Primary phone number of the call queue. Either a phone number or extension is mandatory.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceObject]]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class CreateCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class GetDetailsForCallQueueResponse(CallForwardRulesModifyObject):
    #: Unique name for the call queue.
    name: Optional[str]
    #: Language for the call queue.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this call queue. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Primary phone number of the call queue.
    phone_number: Optional[str]
    #: Extension of the call queue.
    extension: Optional[str]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Language for the call queue.
    language: Optional[str]
    #: Language code for the call queue.
    language_code: Optional[str]
    #: Time zone for the call queue.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[GetPersonPlaceObject]]
    #: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
    phone_number_for_outgoing_calls_enabled: Optional[bool]


class UpdateCallQueueBody(GetDetailsForCallParkExtensionResponse):
    #: Whether or not the call queue is enabled.
    enabled: Optional[bool]
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
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    alternate_number_settings: Optional[AlternateNumberSettings]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostCallQueueCallPolicyObject]
    #: Overall call queue settings.
    queue_settings: Optional[CallQueueQueueSettingsObject]
    #: Flag to indicate whether call waiting is enabled for agents.
    allow_call_waiting_for_agents_enabled: Optional[bool]
    #: People, including workspaces, that are eligible to receive calls.
    agents: Optional[list[PostPersonPlaceObject]]
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


class CreateSelectiveCallForwardingRuleForCallQueueResponse(ApiModel):
    #: ID of the newly created call queue.
    id: Optional[str]


class GetSelectiveCallForwardingRuleForCallQueueResponse(CallForwardRulesModifyObject):
    #: Unique name for the selective rule in the hunt group.
    name: Optional[str]
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str]
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str]
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject]
    #: Settings related to the rule matching based on incoming caller Id.
    calls_from: Optional[CallsFrom]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallsTo1]


class UpdateSelectiveCallForwardingRuleForCallQueueResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class GetCallRecordingSettingsResponse(ApiModel):
    #: Details of the organization.
    organization: Optional[GetAvailableRecallHuntGroupsObject]
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
    #: This element is used to identify the originating party.  It can be user UUID or trunk UUID.
    originator_id: Optional[str]
    #: USER or TRUNK.
    originator_type: Optional[OriginatorType]
    #: Only used when originatorType is TRUNK. This element could be a phone number or URI.
    originator_number: Optional[str]
    #: This element specifies called party.  It can be any dialable string, for example, an ESN number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
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
    #: Array of Strings of Ids of the Extensions.
    #: Possible values: 12345, 3456
    extensions: Optional[list[str]]


class ValidateExtensionsBody(ApiModel):
    #: Array of extensions that will be validated.
    extensions: Optional[list[str]]


class ValidateExtensionsResponse(ApiModel):
    #: Status of the validated array of extensions
    status: Optional[Status5]
    #: Array of extensions statuses.
    extension_status: Optional[list[ExtensionStatusObject]]


class ReadListOfHuntGroupsResponse(ApiModel):
    #: Array of hunt groups.
    hunt_groups: Optional[list[ListHuntGroupObject]]


class CreateHuntGroupBody(GetDetailsForCallParkExtensionResponse):
    #: Primary phone number of the hunt group. Either phone number or extension are required.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, including workspaces, that are eligible to  receive calls.
    agents: Optional[list[PostPersonPlaceObject]]
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool]


class CreateHuntGroupResponse(ApiModel):
    #: ID of the newly created hunt group.
    id: Optional[str]


class GetDetailsForHuntGroupResponse(CallForwardRulesModifyObject):
    #: Unique name for the hunt group.
    name: Optional[str]
    #: Primary phone number of the hunt group.
    phone_number: Optional[str]
    #: Extension of the hunt group.
    extension: Optional[str]
    #: Whether or not the hunt group has the distinctive ring option enabled.
    distinctive_ring: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]
    #: Language for hunt group.
    language: Optional[str]
    #: Language code for hunt group.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, including workspaces, that are eligible to  receive calls.
    agents: Optional[list[GetPersonPlaceObject1]]


class UpdateHuntGroupBody(GetDetailsForCallParkExtensionResponse):
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool]
    #: Primary phone number of the hunt group.
    phone_number: Optional[str]
    #: Whether or not the hunt group has the distinctive ring option enabled.
    distinctive_ring: Optional[bool]
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumbersWithPattern]]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Time zone for the hunt group.
    time_zone: Optional[str]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[PostHuntGroupCallPolicyObject]
    #: People, including workspaces, that are eligible to  receive calls.
    agents: Optional[list[PostPersonPlaceObject]]
    #: Whether or not the hunt group is enabled.
    enabled: Optional[bool]


class GetCallForwardingSettingsForHuntGroupResponse(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding]


class UpdateCallForwardingSettingsForHuntGroupBody(ApiModel):
    #: Settings related to Always, Busy, and No Answer call forwarding.
    call_forwarding: Optional[CallForwarding1]


class CreateSelectiveCallForwardingRuleForHuntGroupResponse(ApiModel):
    #: ID of the newly created hunt group.
    id: Optional[str]


class GetSelectiveCallForwardingRuleForHuntGroupResponse(CallForwardRulesModifyObject):
    #: Unique name for the selective rule in the hunt group.
    name: Optional[str]
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str]
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str]
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject]
    #: Settings related to the rule matching based on incoming caller Id.
    calls_from: Optional[CallsFrom]
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallsTo4]


class UpdateSelectiveCallForwardingRuleForHuntGroupResponse(ApiModel):
    #: New ID for the modified rule.
    id: Optional[str]


class GetLocationInterceptResponse(ApiModel):
    #: Enable/disable location intercept. Enable this feature to override any Location's Call Intercept settings that person configures.
    enabled: Optional[bool]
    #: Inbound call details.
    incoming: Optional[Incoming]
    #: Outbound Call details
    outgoing: Optional[Outgoing]


class ReadInternalDialingConfigurationForlocationResponse(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: Optional[bool]
    #: The selected route group/trunk as premises calls.
    unknown_extension_route_identity: Optional[RouteIdentity]


class ModifyInternalDialingConfigurationForlocationBody(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: Optional[bool]
    #: Type associated with the identity.
    unknown_extension_route_identity: Optional[UnknownExtensionRouteIdentity]


class GetLocationWebexCallingDetailsResponse(GetAvailableRecallHuntGroupsObject):
    #: Location's phone announcement language.
    announcement_language: Optional[str]
    #: Location calling line information.
    calling_line_id: Optional[CallingLineId]
    #: Connection details are only returned for local PSTN types of TRUNK or ROUTE_GROUP.
    connection: Optional[UnknownExtensionRouteIdentity]
    #: External Caller Id Name value. Unicode characters.
    external_caller_id_name: Optional[str]
    #: Limit on the number of people at the location, Read-Only.
    user_limit: Optional[int]
    #: Emergency Location Identifier for a location. Set this field to provide the SIP access network information to the provider which will be used to populate the SIP P-Access-Network-Info header. This is helpful to establish the location of a device when you make an emergency call.
    p_access_network_info: Optional[str]
    #: Must dial to reach an outside line, default is None.
    outside_dial_digit: Optional[str]
    #: Must dial a prefix when calling between locations having same extension within same location.
    routing_prefix: Optional[str]
    #: IP Address, hostname, or domain. Read-Only.
    default_domain: Optional[str]


class UpdateLocationWebexCallingDetailsBody(ApiModel):
    #: Location's phone announcement language.
    announcement_language: Optional[str]
    #: Location calling line information.
    calling_line_id: Optional[CallingLineId]
    #: Connection details can only be modified to and from local PSTN types of TRUNK and ROUTE_GROUP.
    connection: Optional[UnknownExtensionRouteIdentity]
    #: Denve' (string) - External Caller Id Name value. Unicode characters.
    external_caller_id_name: Optional[str]
    #: Location Identifier.
    p_access_network_info: Optional[str]
    #: Must dial to reach an outside line. Default is None.
    outside_dial_digit: Optional[str]
    #: Must dial a prefix when calling between locations having same extension within same location; should be numeric.
    routing_prefix: Optional[str]


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


class GetOutgoingPermissionAutoTransferNumberResponse(ApiModel):
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_1 will be transferred to this number.
    auto_transfer_number1: Optional[str]
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_2 will be transferred to this number.
    auto_transfer_number2: Optional[str]
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_3 will be transferred to this number.
    auto_transfer_number3: Optional[str]


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
    location_paging: Optional[list[ListPagingGroupObject]]


class CreatenewPagingGroupBody(GetDetailsForCallParkExtensionResponse):
    #: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]
    #: Determines what is shown on target users caller Id when a group page is performed. If true shows page originator ID.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[str]]
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[str]]


class CreatenewPagingGroupResponse(ApiModel):
    #: ID of the newly created paging group.
    id: Optional[str]


class GetDetailsForPagingGroupResponse(CallForwardRulesModifyObject):
    #: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
    name: Optional[str]
    #: Paging group phone number. Minimum length is 1. Maximum length is 23. Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Paging group extension. Minimum length is 2. Maximum length is 6. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Paging language. Minimum length is 1. Maximum length is 40.
    language: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    first_name: Optional[str]
    #: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
    last_name: Optional[str]
    #: Determines what is shown on target users caller ID when a group page is performed. If true shows page originator ID.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[GetPagingGroupAgentObject]]
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[GetPagingGroupAgentObject1]]


class UpdatePagingGroupBody(GetDetailsForCallParkExtensionResponse):
    #: Whether or not the paging group is enabled.
    enabled: Optional[bool]
    #: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either phoneNumber or extension is mandatory.
    phone_number: Optional[str]
    #: Language code.
    language_code: Optional[str]
    #: First name to be shown when calls are forwarded out of this paging group. Defaults to ".".
    first_name: Optional[str]
    #: Last name to be shown when calls are forwarded out of this paging group. Defaults to the phone number if set, otherwise defaults to call group name.
    last_name: Optional[str]
    #: Determines what is shown on target users caller Id when a group page is performed. If true shows page originator Id.
    originator_caller_id_enabled: Optional[bool]
    #: An array of people and/or workspaces, who may originate pages to this paging group.
    originators: Optional[list[str]]
    #: People, including workspaces, that are added to paging group as paging call targets.
    targets: Optional[list[str]]


class AddPhoneNumbersTolocationBody(ApiModel):
    #: List of phone numbers that need to be added.
    phone_numbers: Optional[list[str]]
    #: State of the phone numbers.
    state: Optional[State1]


class ActivatePhoneNumbersInlocationBody(ApiModel):
    #: List of phone numbers that need to be added.
    phone_numbers: Optional[list[str]]


class GetPhoneNumbersForOrganizationWithGivenCriteriasResponse(ApiModel):
    #: Array of phone numbers.
    phone_numbers: Optional[NumberListGetObject]


class GetPrivateNetworkConnectResponse(ApiModel):
    #: Network Connection Type for the location.
    network_connection_type: Optional[NetworkConnectionType]


class UpdatePrivateNetworkConnectBody(ApiModel):
    #: Network Connection Type for the location.
    network_connection_type: Optional[NetworkConnectionType]


class ReadListOfRoutingChoicesResponse(ApiModel):
    #: Array of route identities.
    route_identities: Optional[list[RouteIdentity1]]


class ReadListOfSchedulesResponse(ApiModel):
    #: Array of schedules.
    schedules: Optional[list[ListScheduleObject]]


class GetDetailsForScheduleResponse(GetAvailableRecallHuntGroupsObject):
    #: Type of the schedule.
    type: Optional[Type24]
    #: List of schedule events.
    events: Optional[list[GetScheduleEventObject]]


class CreateScheduleBody(ApiModel):
    #: Type of the schedule.
    type: Optional[Type24]
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


class GetDetailsForScheduleEventResponse(GetAvailableRecallHuntGroupsObject):
    #: Start Date of Event.
    start_date: Optional[str]
    #: End Date of Event.
    end_date: Optional[str]
    #: Start time of event.
    start_time: Optional[str]
    #: End time of event.
    end_time: Optional[str]
    #: An indication of whether given event is an all-day event or not.
    all_day_enabled: Optional[bool]
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject]


class CreateScheduleEventResponse(ApiModel):
    #: ID of the newly created schedule event.
    id: Optional[str]


class UpdateScheduleEventResponse(ApiModel):
    #: ID of the target schedule event.
    id: Optional[str]


class GetVoicemailSettingsResponse(ApiModel):
    #: When enabled, you can set the deletion conditions for expired messages.
    message_expiry_enabled: Optional[bool]
    #: Number of days after which messages expire.
    number_of_days_for_message_expiry: Optional[int]
    #: When enabled, all read and unread voicemail messages will be deleted based on the time frame you set. When disabled, all unread voicemail messages will be kept.
    strict_deletion_enabled: Optional[bool]
    #: When enabled, people in the organization can configure the email forwarding of voicemails.
    voice_message_forwarding_enabled: Optional[bool]


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


class GetVoicePortalResponse(GetAvailableRecallHuntGroupsObject):
    #: Language for audio announcements.
    language: Optional[str]
    #: Language code for voicemail group audio announcement.
    language_code: Optional[str]
    #: Extension of incoming call.
    extension: Optional[str]
    #: Phone Number of incoming call.
    phone_number: Optional[str]
    #: Caller Id First Name.
    first_name: Optional[str]
    #: Caller Id Last Name.
    last_name: Optional[str]


class UpdateVoicePortalBody(GetDetailsForCallParkExtensionResponse):
    #: Language code for voicemail group audio announcement.
    language_code: Optional[str]
    #: Phone Number of incoming call.
    phone_number: Optional[str]
    #: Caller Id First Name.
    first_name: Optional[str]
    #: Caller Id Last Name.
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
    #: Settings for not allowing single or groups of repeated digits in passcode (for example, 22888, 121212, or 408408).
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


class GetMusicOnHoldResponse(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    call_hold_enabled: Optional[bool]
    #: If enabled, music will be played when call is parked.
    call_park_enabled: Optional[bool]
    #: Greeting type for the location.
    greeting: Optional[Greeting11]


class ListVoicemailGroupResponse(ApiModel):
    #: Array of VoicemailGroups.
    voicemail_groups: Optional[list[GetVoicemailGroupObject]]


class GetLocationVoicemailGroupResponse(CallForwardRulesModifyObject):
    #: Name of the voicemail group.
    name: Optional[str]
    #: Voicemail group phone number.
    phone_number: Optional[str]
    #: Voicemail group extension number.
    extension: Optional[int]
    #: Voicemail group toll free number.
    toll_free_number: Optional[bool]
    #: Voicemail group caller Id first name.
    first_name: Optional[str]
    #: Voicemail group called Id last name.
    last_name: Optional[str]
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


class ModifyLocationVoicemailGroupBody(CallingLineId):
    #: Set unique voicemail group extension number.
    extension: Optional[int]
    #: Set the voicemail group caller ID first name.
    first_name: Optional[str]
    #: Set the voicemail group called ID last name.
    last_name: Optional[str]
    #: Set to true to enable the voicemail group.
    enabled: Optional[bool]
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


class CreatenewVoicemailGroupForLocationBody(CallingLineId):
    #: Set unique voicemail group extension number for this particular location.
    extension: Optional[int]
    #: Set voicemail group caller Id first name.
    first_name: Optional[str]
    #: Set voicemail group called Id last name.
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
    calling_profiles: Optional[list[GetAvailableRecallHuntGroupsObject]]


class ReadListOfDialPatternsResponse(ApiModel):
    #: Array of dial patterns. An enterprise dial pattern is represented by a sequence of digits (1-9), followed by optional wildcard characters.
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
    status: Optional[Status5]
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
    #: Id of the newly created dial plan.
    id: Optional[str]


class GetDialPlanResponse(GetAvailableRecallHuntGroupsObject):
    #: Id of route type associated with the dial plan.
    route_id: Optional[str]
    #: Name of route type associated with the dial plan.
    route_name: Optional[str]
    #: Route Type associated with the dial plan.
    route_type: Optional[RouteType]
    #: Customer information.
    customer: Optional[GetAvailableRecallHuntGroupsObject]


class ReadListOfTrunksResponse(ApiModel):
    #: Array of trunks.
    trunks: Optional[list[Trunk]]


class CreateTrunkBody(ValidateLocalGatewayFQDNAndDomainForTrunkBody):
    #: A unique name for the trunk.
    name: Optional[str]
    #: Id of location associated with the trunk.
    location_id: Optional[str]
    #: A password to use on the trunk.
    password: Optional[str]
    #: Dual Identity Support setting impacts the handling of the From header and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
    dual_identity_support_enabled: Optional[bool]
    #: Trunk Type associated with the trunk.
    trunk_type: Optional[TrunkType]
    #: Device type assosiated with trunk.
    device_type: Optional[str]
    #: Max Concurrent call. Required to create a static certificate based trunk.
    max_concurrent_calls: Optional[int]


class CreateTrunkResponse(ApiModel):
    #: Id of the newly created trunk.
    id: Optional[str]


class GetTrunkResponse(ValidateLocalGatewayFQDNAndDomainForTrunkBody):
    #: A unique name for the trunk.
    name: Optional[str]
    #: Customer associated with the trunk.
    customer: Optional[GetAvailableRecallHuntGroupsObject]
    #: Location associated with the trunk.
    location: Optional[GetAvailableRecallHuntGroupsObject]
    #: Unique Outgoing and Destination trunk group associated with the dial plan.
    otg_dtg_id: Optional[str]
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    line_port: Optional[str]
    #: Locations using trunk.
    locations_using_trunk: Optional[list[GetAvailableRecallHuntGroupsObject]]
    #: User Id.
    pilot_user_id: Optional[str]
    #: Contains the body of the HTTP response received following the request to Console API and will not be set if the response has no body.
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


class ModifyTrunkBody(ApiModel):
    #: A unique name for the dial plan.
    name: Optional[str]
    #: A password to use on the trunk.
    password: Optional[str]
    #: Determines the behavior of the From and PAI headers on outbound calls.
    dual_identity_support_enabled: Optional[bool]
    #: Max Concurrent call. Required to create a static certificate-based trunk.
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
    organization: Optional[GetAvailableRecallHuntGroupsObject]


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
    locations: Optional[list[GetAvailableRecallHuntGroupsObject]]


class ReadDialPlanLocationsOfRoutingGroupResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[GetAvailableRecallHuntGroupsObject]]


class ReadPSTNConnectionLocationsOfRoutingGroupResponse(ApiModel):
    #: Array of locations.
    locations: Optional[list[GetAvailableRecallHuntGroupsObject]]


class ReadRouteListsOfRoutingGroupResponse(ApiModel):
    #: Array of route lists.
    route_group_usage_route_list_get: Optional[list[RouteGroupUsageRouteListGet]]


class ReadListOfRouteListsResponse(ApiModel):
    #: Array of route lists.
    route_lists: Optional[list[RouteListListGet]]


class CreateRouteListBody(ModifyRouteListBody):
    #: Location associated with the Route List.
    location_id: Optional[str]


class CreateRouteListResponse(ApiModel):
    #: Id of the newly route list created.
    id: Optional[str]


class GetRouteListResponse(ApiModel):
    #: Route list name.
    name: Optional[str]
    #: Location associated with the Route List.
    location: Optional[GetAvailableRecallHuntGroupsObject]
    #: Route group associated with the Route list.
    route_group: Optional[RouteGroup1]


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
    location: Optional[GetAvailableRecallHuntGroupsObject]


class GetLocalGatewayDialPlanUsageForTrunkResponse(ApiModel):
    #: Array of dial Plans.
    dial_plans: Optional[list[GetAvailableRecallHuntGroupsObject]]


class GetLocationsUsingLocalGatewayAsPSTNConnectionRoutingResponse(ApiModel):
    #: Location associated with the trunk.
    location: Optional[GetAvailableRecallHuntGroupsObject]


class GetRouteGroupsUsingLocalGatewayResponse(ApiModel):
    #: Array of route Groups.
    route_group: Optional[list[RouteGroupUsageGetResponse]]


class GetLocalGatewayUsageCountResponse(ApiModel):
    #: The count where the local gateway is used as a PSTN Connection setting.
    pstn_connection_count: Optional[int]
    #: The count where the given local gateway is used as call to extension setting.
    call_to_extension_count: Optional[int]
    #: The count where the given local gateway is used by the dial plan.
    dial_plan_count: Optional[int]
    #: The count where the given local gateway is used by the route group.
    route_group_count: Optional[int]


class GetDetailsForCallQueueHolidayServiceResponse(UpdateCallQueueHolidayServiceBody):
    #: Lists the pre-configured holiday schedules.
    holiday_schedules: Optional[list[CallQueueHolidaySchedulesObject]]


class GetDetailsForCallQueueNightServiceResponse(UpdateCallQueueNightServiceBody):
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: Optional[list[CallQueueHolidaySchedulesObject]]


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


class WebexCallingOrganizationSettingsApi(ApiChild, base='telephony/config/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for administrators utilizing People Webex Calling APIs.
    Modifying these organization settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query parameter.
    """

    def change_announcement_language(self, location_id: str, org_id: str = None, announcement_language_code: str, agent_enabled: bool = None, service_enabled: bool = None):
        """
        Change announcement language for the given location.
        Change announcement language for current people/workspaces and/or existing feature configurations. This does not change the default announcement language which is applied to new users/workspaces and new feature configurations.
        Changing announcement language for the given location requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        :param announcement_language_code: Language code.
        :type announcement_language_code: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if announcement_language_code is not None:
            body['announcementLanguageCode'] = announcement_language_code
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        url = self.ep(f'locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        super().post(url=url, params=params, json=body)
        return

    def read_list_of_auto_attendants(self, org_id: str = None, location_id: str = None, max: int = None, start: int = None, name: str = None, phone_number: str = None) -> List[ListAutoAttendantObject]:
        """
        List all Auto Attendants for the organization.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through your system.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
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
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('autoAttendants')
        data = super().get(url=url, params=params)
        return data["autoAttendants"]

    def details_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> GetDetailsForAutoAttendantResponse:
        """
        Retrieve an Auto Attendant details.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through your system.
        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForAutoAttendantResponse.parse_obj(data)

    def create_auto_attendant(self, location_id: str, org_id: str = None, name: str, business_schedule: str, business_hours_menu: HoursMenuObject, after_hours_menu: HoursMenuObject, phone_number: str = None, extension: str = None, first_name: str = None, last_name: str = None, alternate_numbers: List[AlternateNumbersObject] = None, language_code: str = None, holiday_schedule: str = None, extension_dialing: enum = None, name_dialing: enum = None, time_zone: str = None) -> str:
        """
        Create new Auto Attendant for the given location.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through your system.
        Creating an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject
        :param phone_number: Auto attendant phone number.  Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension.  Either phoneNumber or extension is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: List[AlternateNumbersObject]
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type extension_dialing: enum
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: enum
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if business_hours_menu is not None:
            body['businessHoursMenu'] = business_hours_menu
        if after_hours_menu is not None:
            body['afterHoursMenu'] = after_hours_menu
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if alternate_numbers is not None:
            body['alternateNumbers'] = alternate_numbers
        if language_code is not None:
            body['languageCode'] = language_code
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if extension_dialing is not None:
            body['extensionDialing'] = extension_dialing
        if name_dialing is not None:
            body['nameDialing'] = name_dialing
        if time_zone is not None:
            body['timeZone'] = time_zone
        url = self.ep(f'locations/{location_id}/autoAttendants')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def update_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None, name: str = None, phone_number: str = None, extension: str = None, first_name: str = None, last_name: str = None, alternate_numbers: List[AlternateNumbersObject] = None, language_code: str = None, business_schedule: str = None, holiday_schedule: str = None, extension_dialing: enum = None, name_dialing: enum = None, time_zone: str = None, business_hours_menu: HoursMenuObject = None, after_hours_menu: HoursMenuObject = None):
        """
        Update the designated Auto Attendant.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through your system.
        Updating an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Update an auto attendant from this organization.
        :type org_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param phone_number: Auto attendant phone number.  Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension.  Either phoneNumber or extension is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: List[AlternateNumbersObject]
        :param language_code: Language code for the auto attendant.
        :type language_code: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type extension_dialing: enum
        :param name_dialing: Name dialing setting. If the values are not set default will be set as ENTERPRISE.
        :type name_dialing: enum
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if alternate_numbers is not None:
            body['alternateNumbers'] = alternate_numbers
        if language_code is not None:
            body['languageCode'] = language_code
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if extension_dialing is not None:
            body['extensionDialing'] = extension_dialing
        if name_dialing is not None:
            body['nameDialing'] = name_dialing
        if time_zone is not None:
            body['timeZone'] = time_zone
        if business_hours_menu is not None:
            body['businessHoursMenu'] = business_hours_menu
        if after_hours_menu is not None:
            body['afterHoursMenu'] = after_hours_menu
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().put(url=url, params=params, json=body)
        return

    def delete_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        Delete the designated Auto Attendant.
        Auto attendants play customized prompts and provide callers with menu options for routing their calls through your system.
        Deleting an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().delete(url=url, params=params)
        return

    def forwarding_settings_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendantCallForwardSettingsDetailsObject:
        """
        Retrieve Call Forwarding settings for the designated Auto Attendant including the list of call forwarding rules.
        Retrieving call forwarding settings for an auto attendant requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve the call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant forwarding settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        data = super().get(url=url, params=params)
        return data["callForwarding"]

    def update_forwarding_settings_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None, call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject):
        """
        Update Call Forwarding settings for the designated Auto Attendant.
        Updating call forwarding settings for an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param org_id: Update auto attendant forwarding settings from this organization.
        :type org_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        super().put(url=url, params=params, json=body)
        return

    def create_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None, name: str, forward_to: CallForwardSelectiveForwardToObject, calls_from: CallForwardSelectiveCallsFromObject, enabled: bool = None, business_schedule: str = None, holiday_schedule: str = None, calls_to: CallForwardSelectiveCallsToObject = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding settings.
        Creating a selective call forwarding rule for an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Create the rule for this auto attendant.
        :type auto_attendant_id: str
        :param org_id: Create the auto attendant rule for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related to the rule matching based on incoming caller Id.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if forward_to is not None:
            body['forwardTo'] = forward_to
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if enabled is not None:
            body['enabled'] = enabled
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if calls_to is not None:
            body['callsTo'] = calls_to
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForAutoAttendantResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding settings.
        Retrieving a selective call forwarding rule's settings for an auto attendant requires a full or read-only administrator
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve auto attendant rule settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForAutoAttendantResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, org_id: str = None, name: str, enabled: bool = None, business_schedule: str = None, holiday_schedule: str = None, forward_to: CallForwardSelectiveForwardToObject = None, calls_from: CallForwardSelectiveCallsFromObject = None, calls_to: CallForwardSelectiveCallsToObject = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding settings.
        Updating a selective call forwarding rule's settings for an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are updating settings for.
        :type rule_id: str
        :param org_id: Update auto attendant rule settings for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related the rule matching based on incoming caller Id.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if calls_to is not None:
            body['callsTo'] = calls_to
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_selective_forwarding_rule_for_auto_attendant(self, location_id: str, auto_attendant_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Auto Attendant.
        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the auto attendant's call forwarding settings.
        Deleting a selective call forwarding rule for an auto attendant requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Delete the rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are deleting.
        :type rule_id: str
        :param org_id: Delete auto attendant rule from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_parks(self, location_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, name: str = None) -> List[ListCallParkObject]:
        """
        List all Call Parks for the organization.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :param max: Limit the number of call parks returned to this maximum count. Default is 2000.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching call parks. Default is 0.
        :type start: int
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
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
        url = self.ep(f'locations/{location_id}/callParks')
        data = super().get(url=url, params=params)
        return data["callParks"]

    def create_park(self, location_id: str, org_id: str = None, name: str, recall: PutRecallHuntGroupObject, agents: List[str] = None) -> str:
        """
        Create new Call Parks for the given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Creating a call park requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param org_id: Create the call park for this organization.
        :type org_id: str
        :param name: Unique name for the call park. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to the call park.
        :type recall: PutRecallHuntGroupObject
        :param agents: Array of Id strings of people, including workspaces, that are added to the call park.
        :type agents: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if recall is not None:
            body['recall'] = recall
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'locations/{location_id}/callParks')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_park(self, location_id: str, call_park_id: str, org_id: str = None):
        """
        Delete the designated Call Park.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Deleting a call park requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param call_park_id: Delete the call park with the matching ID.
        :type call_park_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str
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
        Retrieving call park details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param call_park_id: Retrieve settings for a call park with the matching ID.
        :type call_park_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallParkResponse.parse_obj(data)

    def update_park(self, location_id: str, call_park_id: str, org_id: str = None, name: str = None, recall: PutRecallHuntGroupObject = None, agents: List[str] = None) -> str:
        """
        Update the designated Call Park.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Updating a call park requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location in which this call park exists.
        :type location_id: str
        :param call_park_id: Update settings for a call park with the matching ID.
        :type call_park_id: str
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :param name: Unique name for the call park. The maximum length is 80.
        :type name: str
        :param recall: Recall options that are added to call park.
        :type recall: PutRecallHuntGroupObject
        :param agents: Array of ID strings of people, including workspaces, that are added to call park.
        :type agents: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if recall is not None:
            body['recall'] = recall
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'locations/{location_id}/callParks/{call_park_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def available_agents_from_parks(self, location_id: str, org_id: str = None, call_park_name: str = None, max: int = None, start: int = None, name: str = None, phone_number: str = None, order: str = None) -> List[GetPersonPlaceCallParksObject]:
        """
        Retrieve available agents from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving available agents from call parks requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param max: Limit the number of available agents returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching available agents.
        :type start: int
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|) separated sort order fields may be specified. Available sort fields: fname, lname, number and extension. The maximum supported sort order value is 3.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if call_park_name is not None:
            params['callParkName'] = call_park_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableUsers')
        data = super().get(url=url, params=params)
        return data["agents"]

    def available_recall_hunt_groups_from_parks(self, location_id: str, org_id: str = None, max: int = None, start: int = None, name: str = None, order: str = None) -> List[GetAvailableRecallHuntGroupsObject]:
        """
        Retrieve available recall hunt groups from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :param max: Limit the number of available recall hunt groups returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching available recall hunt groups.
        :type start: int
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort fields: lname.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callParks/availableRecallHuntGroups')
        data = super().get(url=url, params=params)
        return data["huntGroups"]

    def park_settings(self, location_id: str, org_id: str = None) -> GetCallParkSettingsResponse:
        """
        Retrieve Call Park Settings from call parks for a given location.
        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.
        Retrieving settings from call parks requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str
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
        Updating call park settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        :param call_park_recall: Recall options that are added to call park.
        :type call_park_recall: PutRecallHuntGroupObject
        :param call_park_settings: Setting controlling call park behavior.
        :type call_park_settings: CallParkSettingsObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if call_park_recall is not None:
            body['callParkRecall'] = call_park_recall
        if call_park_settings is not None:
            body['callParkSettings'] = call_park_settings
        url = self.ep(f'locations/{location_id}/callParks/settings')
        super().put(url=url, params=params, json=body)
        return

    def read_list_of_park_extensions(self, org_id: str = None, max: int = None, start: int = None, extension: str = None, name: str = None, location_id: str = None, location_name: str = None, order: str = None) -> List[ListCallParkExtensionObject]:
        """
        List all Call Park Extensions for the organization.
        The Call Park service, enabled for all users by default, allows a user to park a call against an available user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park service for holding parked calls.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with the matching extension.
        :type location_name: str
        :param order: Order the available agents according to the designated fields.  Available sort fields: groupName, callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
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
        data = super().get(url=url, params=params)
        return data["callParkExtensions"]

    def details_for_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None) -> GetDetailsForCallParkExtensionResponse:
        """
        Retrieve Call Park Extension details.
        The Call Park service, enabled for all users by default, allows a user to park a call against an available user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call Park service for holding parked calls.
        Retrieving call park extension details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param call_park_extension_id: Retrieve details for a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Retrieve call park extension details from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallParkExtensionResponse.parse_obj(data)

    def create_park_extension(self, location_id: str, org_id: str = None, name: str, extension: str) -> str:
        """
        Create new Call Park Extensions for the given location.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone line key.
        Creating a call park extension requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the call park extension for this location.
        :type location_id: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2, maximum length is 6.
        :type extension: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'locations/{location_id}/callParkExtensions')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None):
        """
        Delete the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone line key.
        Deleting a call park extension requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call park extension.
        :type location_id: str
        :param call_park_extension_id: Delete the call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Delete the call park extension from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().delete(url=url, params=params)
        return

    def update_park_extension(self, location_id: str, call_park_extension_id: str, org_id: str = None, name: str = None, extension: str = None):
        """
        Update the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone line key.
        Updating a call park extension requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call park extension exists.
        :type location_id: str
        :param call_park_extension_id: Update a call park extension with the matching ID.
        :type call_park_extension_id: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2, maximum length is 6.
        :type extension: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'locations/{location_id}/callParkExtensions/{call_park_extension_id}')
        super().put(url=url, params=params, json=body)
        return

    def read_list_of_pickups(self, location_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, name: str = None) -> List[ListCallParkObject]:
        """
        List all Call Pickups for the organization.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :param max: Limit the number of call pickups returned to this maximum count. Default is 2000.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching call pickups. Default is 0.
        :type start: int
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
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
        url = self.ep(f'locations/{location_id}/callPickups')
        data = super().get(url=url, params=params)
        return data["callPickups"]

    def create_pickup(self, location_id: str, org_id: str = None, name: str, agents: List[str] = None) -> str:
        """
        Create new Call Pickups for the given location.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Creating a call pickup requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param org_id: Create the call pickup for this organization.
        :type org_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param agents: Array of Id strings of people, including workspaces, that are added to call pickup.
        :type agents: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'locations/{location_id}/callPickups')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None):
        """
        Delete the designated Call Pickup.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Deleting a call pickup requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param call_pickup_id: Delete the call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        super().delete(url=url, params=params)
        return

    def details_for_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None) -> List[GetPersonPlaceCallParksObject]:
        """
        Retrieve Call Pickup details.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving call pickup details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param call_pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        data = super().get(url=url, params=params)
        return data["agents"]

    def update_pickup(self, location_id: str, call_pickup_id: str, org_id: str = None, name: str = None, agents: List[str] = None) -> str:
        """
        Update the designated Call Pickup.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Updating a call pickup requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param call_pickup_id: Update settings for a call pickup with the matching ID.
        :type call_pickup_id: str
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        :param name: Unique name for the call pickup. The maximum length is 80.
        :type name: str
        :param agents: Array of Id strings of people, including workspaces, that are added to call pickup.
        :type agents: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if agents is not None:
            body['agents'] = agents
        url = self.ep(f'locations/{location_id}/callPickups/{call_pickup_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def available_agents_from_pickups(self, location_id: str, org_id: str = None, call_pickup_name: str = None, max: int = None, start: int = None, name: str = None, phone_number: str = None, order: str = None) -> List[GetPersonPlaceCallParksObject]:
        """
        Retrieve available agents from call pickups for a given location.
        Call Pickup enables a user (agent) to answer any ringing line within their pickup group.
        Retrieving available agents from call pickups requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param max: Limit the number of available agents returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching available agents.
        :type start: int
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|) separated sort order fields may be specified. Available sort fields: fname, lname, extension, number.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if call_pickup_name is not None:
            params['callPickupName'] = call_pickup_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if order is not None:
            params['order'] = order
        url = self.ep(f'locations/{location_id}/callPickups/availableUsers')
        data = super().get(url=url, params=params)
        return data["agents"]

    def read_list_of_queues(self, org_id: str = None, location_id: str = None, max: int = None, start: int = None, name: str = None, phone_number: str = None) -> List[ListCallQueueObject]:
        """
        List all Call Queues for the organization.
        Call queues temporarily hold calls in the cloud when all agents, which
        can be users or agents, assigned to receive calls from the queue are
        unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone
        number outside callers can dial to reach users assigned to the call queue.
        Call queues are also assigned an internal extension, which can be dialed
        internally to reach users assigned to the call queue.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List call queues for this organization.
        :type org_id: str
        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return call queues with the matching name.
        :type name: str
        :param phone_number: Only return call queues with matching primary phone number or extension.
        :type phone_number: str
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
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('queues')
        data = super().get(url=url, params=params)
        return data["queues"]

    def create_queue(self, location_id: str, org_id: str = None, name: str, call_policies: PostCallQueueCallPolicyObject, queue_settings: CallQueueQueueSettingsObject, agents: List[PostPersonPlaceObject], phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, phone_number_for_outgoing_calls_enabled: bool = None) -> str:
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
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :param name: Unique name for the call queue.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
        :param agents: People, including workspaces, that are eligible to receive calls.
        :type agents: List[PostPersonPlaceObject]
        :param phone_number: Primary phone number of the call queue. Either a phone number or extension is mandatory.
        :type phone_number: str
        :param extension: Primary phone extension of the call queue. Either a phone number or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this call queue. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this call queue. Defaults to the phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if call_policies is not None:
            body['callPolicies'] = call_policies
        if queue_settings is not None:
            body['queueSettings'] = queue_settings
        if agents is not None:
            body['agents'] = agents
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if phone_number_for_outgoing_calls_enabled is not None:
            body['phoneNumberForOutgoingCallsEnabled'] = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues')
        data = super().post(url=url, params=params, json=body)
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueResponse.parse_obj(data)

    def update_queue(self, location_id: str, queue_id: str, org_id: str = None, queue_settings: CallQueueQueueSettingsObject, enabled: bool = None, name: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, phone_number: str = None, extension: str = None, alternate_number_settings: object = None, call_policies: PostCallQueueCallPolicyObject = None, allow_call_waiting_for_agents_enabled: bool = None, agents: List[PostPersonPlaceObject] = None, phone_number_for_outgoing_calls_enabled: bool = None):
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
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param queue_settings: Overall call queue settings.
        :type queue_settings: CallQueueQueueSettingsObject
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
        :type alternate_number_settings: object
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostCallQueueCallPolicyObject
        :param allow_call_waiting_for_agents_enabled: Flag to indicate whether call waiting is enabled for agents.
        :type allow_call_waiting_for_agents_enabled: bool
        :param agents: People, including workspaces, that are eligible to receive calls.
        :type agents: List[PostPersonPlaceObject]
        :param phone_number_for_outgoing_calls_enabled: When true, indicates that the agent's configuration allows them to use the queue's Caller ID for outgoing calls.
        :type phone_number_for_outgoing_calls_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if queue_settings is not None:
            body['queueSettings'] = queue_settings
        if enabled is not None:
            body['enabled'] = enabled
        if name is not None:
            body['name'] = name
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if alternate_number_settings is not None:
            body['alternateNumberSettings'] = alternate_number_settings
        if call_policies is not None:
            body['callPolicies'] = call_policies
        if allow_call_waiting_for_agents_enabled is not None:
            body['allowCallWaitingForAgentsEnabled'] = allow_call_waiting_for_agents_enabled
        if agents is not None:
            body['agents'] = agents
        if phone_number_for_outgoing_calls_enabled is not None:
            body['phoneNumberForOutgoingCallsEnabled'] = phone_number_for_outgoing_calls_enabled
        url = self.ep(f'locations/{location_id}/queues/{queue_id}')
        super().put(url=url, params=params, json=body)
        return

    def read_list_of_queue_announcement_files(self, location_id: str, queue_id: str, org_id: str = None) -> List[GetAnnouncementFileInfo]:
        """
        List file info for all Call Queue announcement files associated with this Call Queue.
        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call queue can be configured to play whatever subset of these announcement files is desired.
        Retrieving this list of files requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        Note that uploading of announcement files via API is not currently supported, but is available via Webex Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve anouncement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements')
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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/announcements/{file_name}')
        super().delete(url=url, params=params)
        return

    def forwarding_settings_for_queue(self, location_id: str, queue_id: str, org_id: str = None) -> object:
        """
        Retrieve Call Forwarding settings for the designated Call Queue including the list of call forwarding rules.
        Retrieving call forwarding settings for a call queue requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve the call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Retrieve call queue forwarding settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        data = super().get(url=url, params=params)
        return data["callForwarding"]

    def update_forwarding_settings_for_queue(self, location_id: str, queue_id: str, org_id: str = None, call_forwarding: object = None):
        """
        Update Call Forwarding settings for the designated Call Queue.
        Updating call forwarding settings for a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Update call queue forwarding settings from this organization.
        :type org_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding')
        super().put(url=url, params=params, json=body)
        return

    def create_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, org_id: str = None, name: str, calls_from: object, calls_to: object, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: object = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Creating a selective call forwarding rule for a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param queue_id: Create the rule for this call queue.
        :type queue_id: str
        :param org_id: Create the call queue rule for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: object
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: object
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if calls_to is not None:
            body['callsTo'] = calls_to
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForCallQueueResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Retrieving a selective call forwarding rule's settings for a call queue requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which to call queue exists.
        :type location_id: str
        :param queue_id: Retrieve setting for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve call queue rule settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForCallQueueResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, org_id: str = None, name: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: object = None, calls_from: object = None, calls_to: object = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Updating a selective call forwarding rule's settings for a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update settings for a rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are updating settings for.
        :type rule_id: str
        :param org_id: Update call queue rule settings for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: object
        :param calls_from: Settings related the rule matching based on incoming caller Id.
        :type calls_from: object
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if calls_to is not None:
            body['callsTo'] = calls_to
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_selective_forwarding_rule_for_queue(self, location_id: str, queue_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Call Queue.
        A selective call forwarding rule for a call queue allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the call queue's call forwarding settings.
        Deleting a selective call forwarding rule for a call queue requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Delete the rule for this call queue.
        :type queue_id: str
        :param rule_id: Call queue rule you are deleting.
        :type rule_id: str
        :param org_id: Delete call queue rule from this organization.
        :type org_id: str
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
        Retrieving call recording settings requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording')
        data = super().get(url=url, params=params)
        return GetCallRecordingSettingsResponse.parse_obj(data)

    def update_recording_settings(self, org_id: str = None, enabled: bool):
        """
        Update Call Recording settings for the organization.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Updating call recording settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: This API is for Cisco partners only.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :param enabled: Whether or not the call recording is enabled.
        :type enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep('callRecording')
        super().put(url=url, params=params, json=body)
        return

    def recording_terms_of_service_settings(self, vendor_id: str, org_id: str = None) -> GetCallRecordingTermsOfServiceSettingsResponse:
        """
        Retrieve Call Recording Terms Of Service settings for the organization.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Retrieving call recording terms of service settings requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param vendor_id: Retrieve call recording terms of service details for the given vendor.
        :type vendor_id: str
        :param org_id: Retrieve call recording terms of service details from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url=url, params=params)
        return GetCallRecordingTermsOfServiceSettingsResponse.parse_obj(data)

    def update_recording_terms_of_service_settings(self, vendor_id: str, org_id: str = None, terms_of_service_enabled: bool):
        """
        Update Call Recording Terms Of Service settings for the given vendor.
        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.
        Updating call recording terms of service settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str
        :param terms_of_service_enabled: Whether or not the call recording terms of service are enabled.
        :type terms_of_service_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if terms_of_service_enabled is not None:
            body['termsOfServiceEnabled'] = terms_of_service_enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url=url, params=params, json=body)
        return

    def test_routing(self, org_id: str = None, originator_id: str, originator_type: OriginatorType, destination: str, originator_number: str = None) -> TestCallRoutingResponse:
        """
        Validates that an incoming call can be routed.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Test call routing requires a full or write-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :param originator_id: This element is used to identify the originating party.  It can be user UUID or trunk UUID.
        :type originator_id: str
        :param originator_type: USER or TRUNK.
        :type originator_type: OriginatorType
        :param destination: This element specifies called party.  It can be any dialable string, for example, an ESN number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: str
        :param originator_number: Only used when originatorType is TRUNK. This element could be a phone number or URI.
        :type originator_number: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if originator_id is not None:
            body['originatorId'] = originator_id
        if originator_type is not None:
            body['originatorType'] = originator_type
        if destination is not None:
            body['destination'] = destination
        if originator_number is not None:
            body['originatorNumber'] = originator_number
        url = self.ep('actions/testCallRouting/invoke')
        data = super().post(url=url, params=params, json=body)
        return TestCallRoutingResponse.parse_obj(data)

    def validate_list_of_extensions(self, org_id: str = None, extensions: List[str] = None):
        """
        Validate the List of Extensions.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Validate Extension for this organization.
        :type org_id: str
        :param extensions: Array of Strings of Ids of the Extensions.
Possible values: 12345, 3456
        :type extensions: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if extensions is not None:
            body['extensions'] = extensions
        url = self.ep('actions/validateExtensions/invoke')
        super().post(url=url, params=params, json=body)
        return

    def validate_extensions(self, location_id: str, org_id: str = None, extensions: List[str]) -> ValidateExtensionsResponse:
        """
        Validate extensions for a specific location.
        Validating extensions requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Validate extensions for this location.
        :type location_id: str
        :param org_id: Validate extensions for this organization.
        :type org_id: str
        :param extensions: Array of extensions that will be validated.
        :type extensions: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if extensions is not None:
            body['extensions'] = extensions
        url = self.ep(f'locations/{location_id}/actions/validateExtensions/invoke')
        data = super().post(url=url, params=params, json=body)
        return ValidateExtensionsResponse.parse_obj(data)

    def read_list_of_hunt_groups(self, org_id: str = None, location_id: str = None, max: int = None, start: int = None, name: str = None, phone_number: str = None) -> List[ListHuntGroupObject]:
        """
        List all calling Hunt Groups for the organization.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to route to a whole group.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :type org_id: str
        :param location_id: Only return hunt groups with matching location ID.
        :type location_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return hunt groups with the matching name.
        :type name: str
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :type phone_number: str
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
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('huntGroups')
        data = super().get(url=url, params=params)
        return data["huntGroups"]

    def create_hunt_group(self, location_id: str, org_id: str = None, name: str, call_policies: PostHuntGroupCallPolicyObject, agents: List[PostPersonPlaceObject], enabled: bool, phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None) -> str:
        """
        Create new Hunt Groups for the given location.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to route to a whole group.
        Creating a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :param name: Unique name for the hunt group.
        :type name: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, including workspaces, that are eligible to  receive calls.
        :type agents: List[PostPersonPlaceObject]
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param phone_number: Primary phone number of the hunt group. Either phone number or extension are required.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group. Either phone number or extension are required.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if call_policies is not None:
            body['callPolicies'] = call_policies
        if agents is not None:
            body['agents'] = agents
        if enabled is not None:
            body['enabled'] = enabled
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        url = self.ep(f'locations/{location_id}/huntGroups')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None):
        """
        Delete the designated Hunt Group.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to route to a whole group.
        Deleting a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param hunt_group_id: Delete the hunt group with the matching ID.
        :type hunt_group_id: str
        :param org_id: Delete the hunt group from this organization.
        :type org_id: str
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
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to route to a whole group.
        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for the hunt group with this identifier.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForHuntGroupResponse.parse_obj(data)

    def update_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None, enabled: bool = None, name: str = None, phone_number: str = None, extension: str = None, distinctive_ring: bool = None, alternate_numbers: List[AlternateNumbersWithPattern] = None, language_code: str = None, first_name: str = None, last_name: str = None, time_zone: str = None, call_policies: PostHuntGroupCallPolicyObject = None, agents: List[PostPersonPlaceObject] = None, enabled: bool = None):
        """
        Update the designated Hunt Group.
        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to route to a whole group.
        Updating a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param hunt_group_id: Update settings for the hunt group with the matching ID.
        :type hunt_group_id: str
        :param org_id: Update hunt group settings from this organization.
        :type org_id: str
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        :param name: Unique name for the hunt group.
        :type name: str
        :param phone_number: Primary phone number of the hunt group.
        :type phone_number: str
        :param extension: Primary phone extension of the hunt group.
        :type extension: str
        :param distinctive_ring: Whether or not the hunt group has the distinctive ring option enabled.
        :type distinctive_ring: bool
        :param alternate_numbers: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each number will reach the same greeting and each menu will function identically to the main number. The alternate numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
        :type alternate_numbers: List[AlternateNumbersWithPattern]
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to ..
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param time_zone: Time zone for the hunt group.
        :type time_zone: str
        :param call_policies: Policy controlling how calls are routed to agents.
        :type call_policies: PostHuntGroupCallPolicyObject
        :param agents: People, including workspaces, that are eligible to  receive calls.
        :type agents: List[PostPersonPlaceObject]
        :param enabled: Whether or not the hunt group is enabled.
        :type enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if distinctive_ring is not None:
            body['distinctiveRing'] = distinctive_ring
        if alternate_numbers is not None:
            body['alternateNumbers'] = alternate_numbers
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if time_zone is not None:
            body['timeZone'] = time_zone
        if call_policies is not None:
            body['callPolicies'] = call_policies
        if agents is not None:
            body['agents'] = agents
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}')
        super().put(url=url, params=params, json=body)
        return

    def forwarding_settings_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None) -> object:
        """
        Retrieve Call Forwarding settings for the designated Hunt Group including the list of call forwarding rules.
        Retrieving call forwarding settings for a hunt group requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Read the call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param org_id: Retrieve hunt group forwarding settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        data = super().get(url=url, params=params)
        return data["callForwarding"]

    def update_forwarding_settings_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None, call_forwarding: object = None):
        """
        Update Call Forwarding settings for the designated Hunt Group.
        Updating call forwarding settings for a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update call forwarding settings for this hunt group.
        :type hunt_group_id: str
        :param org_id: Update hunt group forwarding settings from this organization.
        :type org_id: str
        :param call_forwarding: Settings related to Always, Busy, and No Answer call forwarding.
        :type call_forwarding: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding')
        super().put(url=url, params=params, json=body)
        return

    def create_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, org_id: str = None, name: str, calls_from: object, calls_to: object, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: object = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Creating a selective call forwarding rule for a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Create the rule for this hunt group.
        :type hunt_group_id: str
        :param org_id: Create the hunt group rule for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: object
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: object
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if calls_to is not None:
            body['callsTo'] = calls_to
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, org_id: str = None) -> GetSelectiveCallForwardingRuleForHuntGroupResponse:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Retrieving a selective call forwarding rule's settings for a hunt group requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Retrieve settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve hunt group rule settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url=url, params=params)
        return GetSelectiveCallForwardingRuleForHuntGroupResponse.parse_obj(data)

    def update_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, org_id: str = None, name: str = None, enabled: bool = None, holiday_schedule: str = None, business_schedule: str = None, forward_to: object = None, calls_from: object = None, calls_to: object = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Updating a selective call forwarding rule's settings for a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Update settings for a rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are updating settings for.
        :type rule_id: str
        :param org_id: Update hunt group rule settings for this organization.
        :type org_id: str
        :param name: Unique name for the selective rule in the hunt group.
        :type name: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
        :type holiday_schedule: str
        :param business_schedule: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
        :type business_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call forwarding.
        :type forward_to: object
        :param calls_from: Settings related the rule matching based on incoming caller Id.
        :type calls_from: object
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to
        if calls_from is not None:
            body['callsFrom'] = calls_from
        if calls_to is not None:
            body['callsTo'] = calls_to
        url = self.ep(f'locations/{location_id}/huntGroups/{hunt_group_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_selective_forwarding_rule_for_hunt_group(self, location_id: str, hunt_group_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Hunt Group.
        A selective call forwarding rule for a hunt group allows calls to be forwarded or not forwarded to the designated number, based on the defined criteria.
        Note that the list of existing call forward rules is available in the hunt group's call forwarding settings.
        Deleting a selective call forwarding rule for a hunt group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this hunt group exists.
        :type location_id: str
        :param hunt_group_id: Delete the rule for this hunt group.
        :type hunt_group_id: str
        :param rule_id: Hunt group rule you are deleting.
        :type rule_id: str
        :param org_id: Delete hunt group rule from this organization.
        :type org_id: str
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
        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either routed to a designated number the person chooses, or to the person's voicemail.
        Retrieving intercept location details requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/intercept')
        data = super().get(url=url, params=params)
        return GetLocationInterceptResponse.parse_obj(data)

    def put_location_intercept(self, location_id: str, org_id: str = None, enabled: bool, incoming: object = None, outgoing: object = None):
        """
        Modifies the intercept location details for a customer location.
        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either routed to a designated number the user chooses, or to the user's voicemail.
        Modifying the intercept location details requires a full, user administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Modifies the intercept details for this location.
        :type location_id: str
        :param org_id: Modifies the intercept location details for a customer location.
        :type org_id: str
        :param enabled: Enable/disable location intercept. Enable this feature to override any location's Call Intercept settings that a person configures.
        :type enabled: bool
        :param incoming: Inbound call details.
        :type incoming: object
        :param outgoing: Outbound Call details
        :type outgoing: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming
        if outgoing is not None:
            body['outgoing'] = outgoing
        url = self.ep(f'locations/{location_id}/intercept')
        super().put(url=url, params=params, json=body)
        return

    def read_internal_dialing_configuration_forlocation(self, location_id: str, org_id: str = None) -> ReadInternalDialingConfigurationForlocationResponse:
        """
        Get current configuration for routing unknown extensions to the Premises as internal calls
        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits that match the extension length) to the PBX.
        Retrieving the internal dialing configuration requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id: List route identities for this organization.
        :type org_id: str
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
        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits that match the extension length) to the PBX.
        Editing the internal dialing configuration requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id: List route identities for this organization.
        :type org_id: str
        :param enable_unknown_extension_route_policy: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the selected route group/trunk as premises calls.
        :type enable_unknown_extension_route_policy: bool
        :param unknown_extension_route_identity: Type associated with the identity.
        :type unknown_extension_route_identity: UnknownExtensionRouteIdentity
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enable_unknown_extension_route_policy is not None:
            body['enableUnknownExtensionRoutePolicy'] = enable_unknown_extension_route_policy
        if unknown_extension_route_identity is not None:
            body['unknownExtensionRouteIdentity'] = unknown_extension_route_identity
        url = self.ep(f'locations/{location_id}/internalDialing')
        super().put(url=url, params=params, json=body)
        return

    def location_webexing_details(self, location_id: str, org_id: str = None) -> GetLocationWebexCallingDetailsResponse:
        """
        Shows Webex Calling details for a location, by ID.
        Specifies the location ID in the locationId parameter in the URI.
        Searching and viewing locations in your organization requires an administrator auth token with the spark-admin:telephony_config_read scope.

        :param location_id: Retrieve Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Webex Calling location attributes for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}')
        data = super().get(url=url, params=params)
        return GetLocationWebexCallingDetailsResponse.parse_obj(data)

    def update_location_webexing_details(self, location_id: str, org_id: str = None, announcement_language: str = None, calling_line_id: object = None, connection: object = None, external_caller_id_name: str = None, p_access_network_info: str = None, outside_dial_digit: str = None, routing_prefix: str = None):
        """
        Update Webex Calling details for a location, by ID.
        Specifies the location ID in the locationId parameter in the URI.
        Modifying the connection via API is only supported for the local PSTN types of TRUNK and ROUTE_GROUP.
        Updating a location in your organization requires an administrator auth token with the spark-admin:telephony_config_write scope.

        :param location_id: Updating Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Updating Webex Calling location attributes for this organization.
        :type org_id: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param calling_line_id: Location calling line information.
        :type calling_line_id: object
        :param connection: Connection details can only be modified to and from local PSTN types of TRUNK and ROUTE_GROUP.
        :type connection: object
        :param external_caller_id_name: Denve' (string) - External Caller Id Name value. Unicode characters.
        :type external_caller_id_name: str
        :param p_access_network_info: Location Identifier.
        :type p_access_network_info: str
        :param outside_dial_digit: Must dial to reach an outside line. Default is None.
        :type outside_dial_digit: str
        :param routing_prefix: Must dial a prefix when calling between locations having same extension within same location; should be numeric.
        :type routing_prefix: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if announcement_language is not None:
            body['announcementLanguage'] = announcement_language
        if calling_line_id is not None:
            body['callingLineId'] = calling_line_id
        if connection is not None:
            body['connection'] = connection
        if external_caller_id_name is not None:
            body['externalCallerIdName'] = external_caller_id_name
        if p_access_network_info is not None:
            body['pAccessNetworkInfo'] = p_access_network_info
        if outside_dial_digit is not None:
            body['outsideDialDigit'] = outside_dial_digit
        if routing_prefix is not None:
            body['routingPrefix'] = routing_prefix
        url = self.ep(f'locations/{location_id}')
        super().put(url=url, params=params, json=body)
        return

    def generate_example_password_for_location(self, location_id: str, org_id: str = None, generate: List[PasswordGenerate] = None) -> str:
        """
        Generates an example password using the effective password settings for the location. If you don't specify anything in the generate field or don't provide a request body, then you will receive a SIP password by default.
        Used while creating a trunk and shouldn't be used anywhere else.
        Generating an example password requires a full or write-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location for which example password has to be generated.
        :type location_id: str
        :param org_id: Organization to which the location belongs.
        :type org_id: str
        :param generate: password settings array.
SIP password setting
        :type generate: List[PasswordGenerate]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if generate is not None:
            body['generate'] = generate
        url = self.ep(f'locations/{location_id}/actions/generatePassword/invoke')
        data = super().post(url=url, params=params, json=body)
        return data["exampleSipPassword"]

    def location_outgoing_permission(self, location_id: str, org_id: str = None) -> List[CallingPermissionObject]:
        """
        Retrieve the location's outgoing call settings.
        A location's outgoing call settings allow you to determine the types of calls the people/workspaces at the location are allowed to make, as well as configure the default calling permission for each call type at the location.
        Retrieving a location's outgoing call settings requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve outgoing call settings for this location.
        :type location_id: str
        :param org_id: Retrieve outgoing call settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/outgoingPermission')
        data = super().get(url=url, params=params)
        return data["callingPermissions"]

    def update_location_outgoing_permission(self, location_id: str, org_id: str = None, calling_permissions: List[CallingPermissionObject] = None):
        """
        Update the location's outgoing call settings.
        Location's outgoing call settings allows you to determine the types of calls the people/workspaces at this location are allowed to make and configure the default calling permission for each call type at a location.
        Updating a location's outgoing call settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update outgoing call settings for this location.
        :type location_id: str
        :param org_id: Update outgoing call settings for this organization.
        :type org_id: str
        :param calling_permissions: Array specifying the subset of calling permissions to be updated.
        :type calling_permissions: List[CallingPermissionObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if calling_permissions is not None:
            body['callingPermissions'] = calling_permissions
        url = self.ep(f'locations/{location_id}/outgoingPermission')
        super().put(url=url, params=params, json=body)
        return

    def outgoing_permission_auto_transfer_number(self, location_id: str, org_id: str = None) -> GetOutgoingPermissionAutoTransferNumberResponse:
        """
        Get the transfer numbers for the outbound permission in a location.
        Outbound permissions can specify which transfer number an outbound call should transfer to via the action field.
        Retrieving an auto transfer number requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve auto transfer number for this location.
        :type location_id: str
        :param org_id: Retrieve auto transfer number for this organization.
        :type org_id: str
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
        Outbound permissions can specify which transfer number an outbound call should transfer to via the action field.
        Updating auto transfer number requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Updating auto transfer number for this location.
        :type location_id: str
        :param org_id: Updating auto transfer number for this organization.
        :type org_id: str
        :param auto_transfer_number1: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_1 will be transferred to this number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_2 will be transferred to this number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_3 will be transferred to this number.
        :type auto_transfer_number3: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if auto_transfer_number1 is not None:
            body['autoTransferNumber1'] = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body['autoTransferNumber2'] = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body['autoTransferNumber3'] = auto_transfer_number3
        url = self.ep(f'locations/{location_id}/outgoingPermission/autoTransferNumbers')
        super().put(url=url, params=params, json=body)
        return

    def outgoing_permission_location_access_code(self, location_id: str, org_id: str = None) -> object:
        """
        Retrieve access codes details for a customer location.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Retrieving access codes details requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        data = super().get(url=url, params=params)
        return data["accessCodes"]

    def create_outgoing_permissionnew_access_code_forcustomer_location(self, location_id: str, org_id: str = None, access_codes: object = None):
        """
        Add a new access code for the given location for a customer.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Creating an access code for the given location requires a full or user administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param org_id: Add new access code for this organization.
        :type org_id: str
        :param access_codes: Access code details
        :type access_codes: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if access_codes is not None:
            body['accessCodes'] = access_codes
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        super().post(url=url, params=params, json=body)
        return

    def delete_outgoing_permission_access_code_location(self, location_id: str, org_id: str = None, delete_codes: List[str]):
        """
        Deletes the access code details for a particular location for a customer.
        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
        Modifying the access code location details requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param org_id: Deletes the access code details for a customer location.
        :type org_id: str
        :param delete_codes: Array of string to delete access codes. For example, ["1234","2345"]
        :type delete_codes: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep(f'locations/{location_id}/outgoingPermission/accessCodes')
        super().put(url=url, params=params, json=body)
        return

    def read_list_of_paging_groups(self, org_id: str = None, max: int = None, start: int = None, location_id: str = None, name: str = None, phone_number: str = None) -> List[ListPagingGroupObject]:
        """
        List all Paging Groups for the organization.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a simultaneous call to all the assigned targets.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List paging groups for this organization.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count. Default is 2000
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects. Default is 0
        :type start: int
        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('paging')
        data = super().get(url=url, params=params)
        return data["locationPaging"]

    def createnew_paging_group(self, location_id: str, org_id: str = None, name: str, phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, originator_caller_id_enabled: bool = None, originators: List[str] = None, targets: List[str] = None) -> str:
        """
        Create a new Paging Group for the given location.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a simultaneous call to all the assigned targets.
        Creating a paging group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :param name: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Paging group extension. Minimum length is 2. Maximum length is 6.  Either phoneNumber or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
        :type first_name: str
        :param last_name: Last name that displays when a group page is performed. Minimum length is 1. Maximum length is 30.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller Id when a group page is performed. If true shows page originator ID.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people and/or workspaces, who may originate pages to this paging group.
        :type originators: List[str]
        :param targets: People, including workspaces, that are added to paging group as paging call targets.
        :type targets: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if originator_caller_id_enabled is not None:
            body['originatorCallerIdEnabled'] = originator_caller_id_enabled
        if originators is not None:
            body['originators'] = originators
        if targets is not None:
            body['targets'] = targets
        url = self.ep(f'locations/{location_id}/paging')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_paging_group(self, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete the designated Paging Group.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a simultaneous call to all the assigned targets.
        Deleting a paging group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :type paging_id: str
        :param org_id: Delete the paging group from this organization.
        :type org_id: str
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
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a simultaneous call to all the assigned targets.
        Retrieving paging group details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Retrieve paging group settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForPagingGroupResponse.parse_obj(data)

    def update_paging_group(self, location_id: str, paging_id: str, org_id: str = None, enabled: bool = None, name: str = None, phone_number: str = None, extension: str = None, language_code: str = None, first_name: str = None, last_name: str = None, originator_caller_id_enabled: bool = None, originators: List[str] = None, targets: List[str] = None):
        """
        Update the designated Paging Group.
        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a simultaneous call to all the assigned targets.
        Updating a paging group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        :param enabled: Whether or not the paging group is enabled.
        :type enabled: bool
        :param name: Unique name for the paging group. Minimum length is 1. Maximum length is 30.
        :type name: str
        :param phone_number: Paging group phone number. Minimum length is 1. Maximum length is 23.  Either phoneNumber or extension is mandatory.
        :type phone_number: str
        :param extension: Paging group extension. Minimum length is 2. Maximum length is 6.  Either phoneNumber or extension is mandatory.
        :type extension: str
        :param language_code: Language code.
        :type language_code: str
        :param first_name: First name to be shown when calls are forwarded out of this paging group. Defaults to ".".
        :type first_name: str
        :param last_name: Last name to be shown when calls are forwarded out of this paging group. Defaults to the phone number if set, otherwise defaults to call group name.
        :type last_name: str
        :param originator_caller_id_enabled: Determines what is shown on target users caller Id when a group page is performed. If true shows page originator Id.
        :type originator_caller_id_enabled: bool
        :param originators: An array of people and/or workspaces, who may originate pages to this paging group.
        :type originators: List[str]
        :param targets: People, including workspaces, that are added to paging group as paging call targets.
        :type targets: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if language_code is not None:
            body['languageCode'] = language_code
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if originator_caller_id_enabled is not None:
            body['originatorCallerIdEnabled'] = originator_caller_id_enabled
        if originators is not None:
            body['originators'] = originators
        if targets is not None:
            body['targets'] = targets
        url = self.ep(f'locations/{location_id}/paging/{paging_id}')
        super().put(url=url, params=params, json=body)
        return

    def add_phone_numbers_tolocation(self, location_id: str, org_id: str = None, phone_numbers: List[str], state: State):
        """
        Adds a specified set of phone numbers to a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers must follow E.164 format for all countries, except for the United States, which can also follow the National format. Active phone numbers are in service.
        Adding a phone number to a location requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        :param state: State of the phone numbers.
        :type state: State
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if state is not None:
            body['state'] = state
        url = self.ep(f'locations/{location_id}/numbers')
        super().post(url=url, params=params, json=body)
        return

    def activate_phone_numbers_inlocation(self, location_id: str, org_id: str = None, phone_numbers: List[str]):
        """
        Activate the specified set of phone numbers in a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers must follow E.164 format for all countries, except for the United States, which can also follow the National format. Active phone numbers are in service.
        Activating a phone number in a location requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        url = self.ep(f'locations/{location_id}/numbers')
        super().put(url=url, params=params, json=body)
        return

    def remove_phone_numbers_fromlocation(self, location_id: str, org_id: str = None, phone_numbers: List[str], state: State):
        """
        Remove the specified set of phone numbers from a location for an organization.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers must follow E.164 format for all countries, except for the United States, which can also follow the National format. Active phone numbers are in service.
        Removing a phone number from a location requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: List[str]
        :param state: State of the phone numbers.
        :type state: State
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if state is not None:
            body['state'] = state
        url = self.ep(f'locations/{location_id}/numbers')
        super().delete(url=url, params=params, json=body)
        return

    def phone_numbers_for_organization_with_given_criterias(self, org_id: str = None, location_id: str = None, max: int = None, start: int = None, phone_number: str = None, available: bool = None, order: str = None, owner_name: str = None, owner_id: str = None, owner_type: enum = None, extension: str = None, number_type: str = None, phone_number_type: str = None, state: str = None, details: bool = None, toll_free_numbers: bool = None) -> NumberListGetObject:
        """
        List all the phone numbers for the given organization along with the status and owner (if any).
        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List numbers for this organization.
        :type org_id: str
        :param location_id: Return the list of phone numbers for this location within the given organization. The maximum length is 36.
        :type location_id: str
        :param max: Limit the number of phone numbers returned to this maximum count. Default is 2000.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching phone numbers. Default is 0.
        :type start: int
        :param phone_number: Search for this phoneNumber.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with ownerType parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will be based on number and extension in an ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given ownerName. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given ownerType. Possible input values
        :type owner_type: enum
        :param extension: Returns the list of PSTN phone numbers with the given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers. This parameter cannot be used along with available or state.
        :type number_type: str
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: str
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: str
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
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
            params['available'] = available
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
            params['details'] = details
        if toll_free_numbers is not None:
            params['tollFreeNumbers'] = toll_free_numbers
        url = self.ep('numbers')
        data = super().get(url=url, params=params)
        return data["phoneNumbers"]

    def private_network_connect(self, location_id: str, org_id: str = None) -> enum:
        """
        Retrieve the location's network connection type.
        Network Connection Type determines if the location's network connection is public or private.
        Retrieving a location's network connection type requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve the network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve the network connection type for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        data = super().get(url=url, params=params)
        return data["networkConnectionType"]

    def update_private_network_connect(self, location_id: str, org_id: str = None, network_connection_type: enum):
        """
        Update the location's network connection type.
        Network Connection Type determines if the location's network connection is public or private.
        Updating a location's network connection type requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update the network connection type for this location.
        :type location_id: str
        :param org_id: Update network connection type for this organization.
        :type org_id: str
        :param network_connection_type: Network Connection Type for the location.
        :type network_connection_type: enum
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if network_connection_type is not None:
            body['networkConnectionType'] = network_connection_type
        url = self.ep(f'locations/{location_id}/privateNetworkConnect')
        super().put(url=url, params=params, json=body)
        return

    def read_list_of_routing_choices(self, org_id: str = None, route_group_name: str = None, trunk_name: str = None, max: int = None, start: int = None, order: str = None) -> List[RouteIdentity]:
        """
        List all Routes for the organization.
        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex Calling to manage calls between Webex Calling hosted users and premises PBX users. This solution lets you configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List route identities for this organization.
        :type org_id: str
        :param route_group_name: Return the list of route identities matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of route identities matching the Trunk name..
        :type trunk_name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the route identities according to the designated fields.  Available sort fields: routeName, routeType.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('routeChoices')
        data = super().get(url=url, params=params)
        return data["routeIdentities"]

    def read_list_of_schedules(self, location_id: str, org_id: str = None, type_: str = None, max: int = None, start: int = None, name: str = None) -> List[ListScheduleObject]:
        """
        List all schedules for the given location of the organization.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the list of schedules for this location.
        :type location_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param type_: Type of the schedule.
        :type type_: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param name: Only return schedules with the matching name.
        :type name: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if type_ is not None:
            params['type'] = type_
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if name is not None:
            params['name'] = name
        url = self.ep(f'locations/{location_id}/schedules')
        data = super().get(url=url, params=params)
        return data["schedules"]

    def details_for_schedule(self, location_id: str, type_: str, schedule_id: str, org_id: str = None) -> GetDetailsForScheduleResponse:
        """
        Retrieve Schedule details.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Retrieving schedule details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule details in this location.
        :type location_id: str
        :param type_: Type of the schedule.
        :type type_: str
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForScheduleResponse.parse_obj(data)

    def create_schedule(self, location_id: str, org_id: str = None, type_: enum, name: str, events: List[ScheduleEventObject] = None) -> str:
        """
        Create new Schedule for the given location.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Creating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :param type_: Type of the schedule.
        :type type_: enum
        :param name: Unique name for the schedule.
        :type name: str
        :param events: List of schedule events.
        :type events: List[ScheduleEventObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if type_ is not None:
            body['type'] = type_
        if name is not None:
            body['name'] = name
        if events is not None:
            body['events'] = events
        url = self.ep(f'locations/{location_id}/schedules')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def update_schedule(self, location_id: str, type_: str, schedule_id: str, org_id: str = None, name: str, events: List[ModifyScheduleEventListObject] = None) -> str:
        """
        Update the designated schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Updating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The Schedule ID will change upon modification of the Schedule name.

        :param location_id: Location in which this schedule exists.
        :type location_id: str
        :param type_: Type of schedule.
        :type type_: str
        :param schedule_id: Update schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :param name: Unique name for the schedule.
        :type name: str
        :param events: List of schedule events.
        :type events: List[ModifyScheduleEventListObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if events is not None:
            body['events'] = events
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_schedule(self, location_id: str, type_: str, schedule_id: str, org_id: str = None):
        """
        Delete the designated Schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Deleting a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type_: Type of the schedule.
        :type type_: str
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}')
        super().delete(url=url, params=params)
        return

    def details_for_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, org_id: str = None) -> GetDetailsForScheduleEventResponse:
        """
        Retrieve Schedule Event details.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Retrieving a schedule event's details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule event details in this location.
        :type location_id: str
        :param type_: Type of schedule.
        :type type_: str
        :param schedule_id: Retrieve the schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().get(url=url, params=params)
        return GetDetailsForScheduleEventResponse.parse_obj(data)

    def create_schedule_event(self, location_id: str, type_: str, schedule_id: str, org_id: str = None, name: str, start_date: str, end_date: str, start_time: str = None, end_time: str = None, all_day_enabled: bool = None, recurrence: RecurrenceObject = None) -> str:
        """
        Create new Event for the given location Schedule.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Creating a schedule event requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param type_: Type of schedule.
        :type type_: str
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start Date of Event.
        :type start_date: str
        :param end_date: End Date of Event.
        :type end_date: str
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the startTime and endTime are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def update_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, org_id: str = None, name: str, start_date: str, end_date: str, start_time: str = None, end_time: str = None, all_day_enabled: bool = None, recurrence: RecurrenceObject = None) -> str:
        """
        Update the designated Schedule Event.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Updating a schedule event requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        NOTE: The schedule event ID will change upon modification of the schedule event name.

        :param location_id: Location in which this schedule event exists.
        :type location_id: str
        :param type_: Type of schedule.
        :type type_: str
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Update the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of event.
        :type start_date: str
        :param end_date: End date of event.
        :type end_date: str
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the startTime and endTime are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_schedule_event(self, location_id: str, type_: str, schedule_id: str, event_id: str, org_id: str = None):
        """
        Delete the designated Schedule Event.
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for example auto attendants, can perform a specific action.
        Deleting a schedule event requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type_: Type of schedule.
        :type type_: str
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        super().delete(url=url, params=params)
        return

    def voicemail_settings(self, org_id: str = None) -> GetVoicemailSettingsResponse:
        """
        Retrieve the organization's voicemail settings.
        Organizational voicemail settings determines what voicemail features a person can configure and automatic message expiration.
        Retrieving organization's voicemail settings requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/settings')
        data = super().get(url=url, params=params)
        return GetVoicemailSettingsResponse.parse_obj(data)

    def update_voicemail_settings(self, org_id: str = None, message_expiry_enabled: bool, number_of_days_for_message_expiry: int, strict_deletion_enabled: bool = None, voice_message_forwarding_enabled: bool = None):
        """
        Update the organization's voicemail settings.
        Organizational voicemail settings determines what voicemail features a person can configure and automatic message expiration.
        Updating an organization's voicemail settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        :param message_expiry_enabled: Set to true to enable voicemail deletion and set the deletion conditions for expired messages.
        :type message_expiry_enabled: bool
        :param number_of_days_for_message_expiry: Number of days after which messages expire.
        :type number_of_days_for_message_expiry: int
        :param strict_deletion_enabled: Set to true to delete all read and unread voicemail messages based on the time frame you set. Set to false to keep all the unread voicemail messages.
        :type strict_deletion_enabled: bool
        :param voice_message_forwarding_enabled: Set to true to allow people to configure the email forwarding of voicemails.
        :type voice_message_forwarding_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if message_expiry_enabled is not None:
            body['messageExpiryEnabled'] = message_expiry_enabled
        if number_of_days_for_message_expiry is not None:
            body['numberOfDaysForMessageExpiry'] = number_of_days_for_message_expiry
        if strict_deletion_enabled is not None:
            body['strictDeletionEnabled'] = strict_deletion_enabled
        if voice_message_forwarding_enabled is not None:
            body['voiceMessageForwardingEnabled'] = voice_message_forwarding_enabled
        url = self.ep('voicemail/settings')
        super().put(url=url, params=params, json=body)
        return

    def voicemail_rules(self, org_id: str = None) -> GetVoicemailRulesResponse:
        """
        Retrieve the organization's voicemail rules.
        Organizational voicemail rules specify the default passcode requirements. They are provided for informational purposes only and cannot be modified.
        Retrieving the organization's voicemail rules requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail rules for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('voicemail/rules')
        data = super().get(url=url, params=params)
        return GetVoicemailRulesResponse.parse_obj(data)

    def update_voicemail_rules(self, org_id: str = None, default_voicemail_pin_enabled: bool = None, default_voicemail_pin: str = None, expire_passcode: object = None, change_passcode: object = None, block_previous_passcodes: object = None):
        """
        Update the organization's default voicemail passcode and/or rules.
        Organizational voicemail rules specify the default passcode requirements.
        If you choose to set a default passcode for new people added to your organization, communicate to your people what that passcode is, and that it must be reset before they can access their voicemail. If this feature is not turned on, each new person must initially set their own passcode.
        Updating an organization's voicemail passcode and/or rules requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :param default_voicemail_pin_enabled: Set to true to enable the default voicemail passcode.
        :type default_voicemail_pin_enabled: bool
        :param default_voicemail_pin: Default voicemail passcode.
        :type default_voicemail_pin: str
        :param expire_passcode: Settings for passcode expiry.
        :type expire_passcode: object
        :param change_passcode: Settings for passcode changes.
        :type change_passcode: object
        :param block_previous_passcodes: Settings for previous passcode usage.
        :type block_previous_passcodes: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if default_voicemail_pin_enabled is not None:
            body['defaultVoicemailPinEnabled'] = default_voicemail_pin_enabled
        if default_voicemail_pin is not None:
            body['defaultVoicemailPin'] = default_voicemail_pin
        if expire_passcode is not None:
            body['expirePasscode'] = expire_passcode
        if change_passcode is not None:
            body['changePasscode'] = change_passcode
        if block_previous_passcodes is not None:
            body['blockPreviousPasscodes'] = block_previous_passcodes
        url = self.ep('voicemail/rules')
        super().put(url=url, params=params, json=body)
        return

    def location_voicemail(self, location_id: str, org_id: str = None) -> bool:
        """
        Retrieve voicemail settings for a specific location.
        Location voicemail settings allows you to enable voicemail transcription for a specific location.
        Retrieving a location's voicemail settings requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail settings for this location.
        :type location_id: str
        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemail')
        data = super().get(url=url, params=params)
        return data["voicemailTranscriptionEnabled"]

    def update_location_voicemail(self, location_id: str, org_id: str = None, voicemail_transcription_enabled: bool):
        """
        Update the voicemail settings for a specific location.
        Location voicemail settings allows you to enable voicemail transcription for a specific location.
        Updating a location's voicemail settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update voicemail settings for this location.
        :type location_id: str
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        :param voicemail_transcription_enabled: Set to true to enable voicemail transcription.
        :type voicemail_transcription_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if voicemail_transcription_enabled is not None:
            body['voicemailTranscriptionEnabled'] = voicemail_transcription_enabled
        url = self.ep(f'locations/{location_id}/voicemail')
        super().put(url=url, params=params, json=body)
        return

    def voice_portal(self, location_id: str, org_id: str = None) -> GetVoicePortalResponse:
        """
        Retrieve Voice portal information for the location.
        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant announcements.
        Retrieving voice portal information for an organization requires a full read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicePortal')
        data = super().get(url=url, params=params)
        return GetVoicePortalResponse.parse_obj(data)

    def update_voice_portal(self, location_id: str, org_id: str = None, name: str = None, language_code: str = None, extension: str = None, phone_number: str = None, first_name: str = None, last_name: str = None, passcode: object = None):
        """
        Update Voice portal information for the location.
        Voice portals provide an interactive voice response (IVR)
        system so administrators can manage auto attendant anouncements.
        Updating voice portal information for an organization and/or rules requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        :param name: Voice Portal Name.
        :type name: str
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param extension: Extension of incoming call.
        :type extension: str
        :param phone_number: Phone Number of incoming call.
        :type phone_number: str
        :param first_name: Caller Id First Name.
        :type first_name: str
        :param last_name: Caller Id Last Name.
        :type last_name: str
        :param passcode: Voice Portal Admin Passcode.
        :type passcode: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if language_code is not None:
            body['languageCode'] = language_code
        if extension is not None:
            body['extension'] = extension
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if passcode is not None:
            body['passcode'] = passcode
        url = self.ep(f'locations/{location_id}/voicePortal')
        super().put(url=url, params=params, json=body)
        return

    def voice_portal_passcode_rule(self, location_id: str, org_id: str = None) -> GetVoicePortalPasscodeRuleResponse:
        """
        Retrieve the voice portal passcode rule for a location.
        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant anouncements
        Retrieving the voice portal passcode rule requires a full read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str
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
        Retrieving a location's music on hold settings requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve music on hold settings for this location.
        :type location_id: str
        :param org_id: Retrieve music on hold settings for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/musicOnHold')
        data = super().get(url=url, params=params)
        return GetMusicOnHoldResponse.parse_obj(data)

    def update_music_on_hold(self, location_id: str, org_id: str = None, greeting: enum, call_hold_enabled: bool = None, call_park_enabled: bool = None):
        """
        Update the location's music on hold settings.
        Location music on hold settings allows you to play music when a call is placed on hold or parked.
        Updating a location's music on hold settings requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :param greeting: Greeting type for the location.
        :type greeting: enum
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if greeting is not None:
            body['greeting'] = greeting
        if call_hold_enabled is not None:
            body['callHoldEnabled'] = call_hold_enabled
        if call_park_enabled is not None:
            body['callParkEnabled'] = call_park_enabled
        url = self.ep(f'locations/{location_id}/musicOnHold')
        super().put(url=url, params=params, json=body)
        return

    def list_voicemail_group(self, location_id: str = None, org_id: str = None, name: str = None, phone_number: str = None, **params) -> Generator[GetVoicemailGroupObject, None, None]:
        """
        List the voicemail group information for the organization.
        You can create a shared voicemail box and inbound FAX box to
        assign to users or call routing features like an auto attendant, call queue, or hunt group.
        Retrieving a voicemail group for the organization requires a full read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
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
        return self.session.follow_pagination(url=url, model=GetVoicemailGroupObject, params=params)

    def location_voicemail_group(self, location_id: str, voicemail_group_id: str, org_id: str = None) -> GetLocationVoicemailGroupResponse:
        """
        Retrieve voicemail group details for a location.
        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active, message storage settings, and how you would like to be notified of new voicemail messages.
        Retrieving voicemail group details requires a full, user or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group Id.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        data = super().get(url=url, params=params)
        return GetLocationVoicemailGroupResponse.parse_obj(data)

    def modify_location_voicemail_group(self, location_id: str, voicemail_group_id: str, org_id: str = None, name: str = None, phone_number: str = None, extension: int = None, first_name: str = None, last_name: str = None, enabled: bool = None, passcode: int = None, language_code: str = None, greeting: enum = None, greeting_description: str = None, message_storage: object = None, notifications: object = None, fax_message: object = None, transfer_to_number: object = None, email_copy_of_message: object = None):
        """
        Modifies the voicemail group location details for a particular location for a customer.
        Manage your voicemail settings, like when you want your voicemail to be active, message storage settings, and how you would like to be notified of new voicemail messages.
        Modifying the voicemail group location details requires a full, user administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Modifies the voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Modifies the voicemail group details for this voicemail group Id.
        :type voicemail_group_id: str
        :param org_id: Modifies the voicemail group details for a customer location.
        :type org_id: str
        :param name: Set the name of the voicemail group.
        :type name: str
        :param phone_number: Set voicemail group phone number.
        :type phone_number: str
        :param extension: Set unique voicemail group extension number.
        :type extension: int
        :param first_name: Set the voicemail group caller ID first name.
        :type first_name: str
        :param last_name: Set the voicemail group called ID last name.
        :type last_name: str
        :param enabled: Set to true to enable the voicemail group.
        :type enabled: bool
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for the voicemail group audio announcement.
        :type language_code: str
        :param greeting: Voicemail group greeting type.
        :type greeting: enum
        :param greeting_description: CUSTOM greeting for previously uploaded.
        :type greeting_description: str
        :param message_storage: Message storage information
        :type message_storage: object
        :param notifications: Message notifications
        :type notifications: object
        :param fax_message: Fax message receive settings
        :type fax_message: object
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: object
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if enabled is not None:
            body['enabled'] = enabled
        if passcode is not None:
            body['passcode'] = passcode
        if language_code is not None:
            body['languageCode'] = language_code
        if greeting is not None:
            body['greeting'] = greeting
        if greeting_description is not None:
            body['greetingDescription'] = greeting_description
        if message_storage is not None:
            body['messageStorage'] = message_storage
        if notifications is not None:
            body['notifications'] = notifications
        if fax_message is not None:
            body['faxMessage'] = fax_message
        if transfer_to_number is not None:
            body['transferToNumber'] = transfer_to_number
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = email_copy_of_message
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().put(url=url, params=params, json=body)
        return

    def createnew_voicemail_group_for_location(self, location_id: str, org_id: str = None, name: str, extension: int, passcode: int, language_code: str, message_storage: object, notifications: object, fax_message: object, transfer_to_number: object, email_copy_of_message: object, phone_number: str = None, first_name: str = None, last_name: str = None) -> str:
        """
        Create a new voicemail group for the given location for a customer.
        A voicemail group can be created for given location for a customer.
        Creating a voicemail group for the given location requires a full or user administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create a new voice mail group for this location.
        :type location_id: str
        :param org_id: Create a new voice mail group for this organization.
        :type org_id: str
        :param name: Set name to create new voicemail group for a particular location for a customer.
        :type name: str
        :param extension: Set unique voicemail group extension number for this particular location.
        :type extension: int
        :param passcode: Set passcode to access voicemail group when calling.
        :type passcode: int
        :param language_code: Language code for voicemail group audio announcement.
        :type language_code: str
        :param message_storage: Message storage information
        :type message_storage: object
        :param notifications: Message notifications
        :type notifications: object
        :param fax_message: Fax message information
        :type fax_message: object
        :param transfer_to_number: Transfer message information
        :type transfer_to_number: object
        :param email_copy_of_message: Message copy information
        :type email_copy_of_message: object
        :param phone_number: Set voicemail group phone number for this particular location.
        :type phone_number: str
        :param first_name: Set voicemail group caller Id first name.
        :type first_name: str
        :param last_name: Set voicemail group called Id last name.
        :type last_name: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        if passcode is not None:
            body['passcode'] = passcode
        if language_code is not None:
            body['languageCode'] = language_code
        if message_storage is not None:
            body['messageStorage'] = message_storage
        if notifications is not None:
            body['notifications'] = notifications
        if fax_message is not None:
            body['faxMessage'] = fax_message
        if transfer_to_number is not None:
            body['transferToNumber'] = transfer_to_number
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = email_copy_of_message
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        url = self.ep(f'locations/{location_id}/voicemailGroups')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_voicemail_group_for_location(self, location_id: str, voicemail_group_id: str, org_id: str = None):
        """
        Delete the designated voicemail group.
        Deleting a voicemail group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a voicemail group.
        :type location_id: str
        :param voicemail_group_id: Delete the voicemail group with the matching ID.
        :type voicemail_group_id: str
        :param org_id: Delete the voicemail group from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/voicemailGroups/{voicemail_group_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_uc_manager_profiles(self, org_id: str = None) -> List[GetAvailableRecallHuntGroupsObject]:
        """
        List all calling UC Manager Profiles for the organization.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex (Unified CM).
        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although currently only setting at a user level is supported by Webex APIs.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callingProfiles')
        data = super().get(url=url, params=params)
        return data["callingProfiles"]

    def read_list_of_dial_patterns(self, dial_plan_id: str, org_id: str = None, dial_pattern: str = None, max: int = None, start: int = None, order: str = None) -> List[str]:
        """
        List all Dial Patterns for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Id of the organization to which the dial patterns belong.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by optional wildcard characters.
Valid wildcard characters are ! (matches any sequence of digits) and X (matches a single digit, 0-9).
The ! wildcard can only occur once at the end and only in an E.164 pattern
        :type dial_pattern: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the dial patterns according to the designated fields.  Available sort fields: dialPattern.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if dial_pattern is not None:
            params['dialPattern'] = dial_pattern
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        data = super().get(url=url, params=params)
        return data["dialPatterns"]

    def modify_dial_patterns(self, dial_plan_id: str, org_id: str = None, dial_patterns: List[DialPattern] = None, delete_all_dial_patterns: bool = None):
        """
        Modify dial patterns for the Dial Plan.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Modifying a dial pattern requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the request is not modified.
        :type dial_patterns: List[DialPattern]
        :param delete_all_dial_patterns: Delete all the dial patterns for a dial plan.
        :type delete_all_dial_patterns: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if dial_patterns is not None:
            body['dialPatterns'] = dial_patterns
        if delete_all_dial_patterns is not None:
            body['deleteAllDialPatterns'] = delete_all_dial_patterns
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}/dialPatterns')
        super().put(url=url, params=params, json=body)
        return

    def validate_dial_pattern(self, org_id: str = None, dial_patterns: List[str]) -> ValidateDialPatternResponse:
        """
        Validate a Dial Pattern.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Validating a dial pattern requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param dial_patterns: Array of dial patterns.
Possible values: +5555,7777
        :type dial_patterns: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if dial_patterns is not None:
            body['dialPatterns'] = dial_patterns
        url = self.ep('premisePstn/actions/validateDialPatterns/invoke')
        data = super().post(url=url, params=params, json=body)
        return ValidateDialPatternResponse.parse_obj(data)

    def read_list_of_dial_plans(self, org_id: str = None, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None, max: int = None, start: int = None, order: str = None) -> List[DialPlan]:
        """
        List all Dial Plans for the organization.
        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial plan is associated. Multiple dial patterns can be defined as part of your dial plan.  Dial plans are configured globally for an enterprise and apply to all users, regardless of location.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List dial plans for this organization.
        :type org_id: str
        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the Route group name..
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the Trunk name..
        :type trunk_name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the dial plans according to the designated fields.  Available sort fields: name, routeName, routeType. Sort order is ascending by default
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if dial_plan_name is not None:
            params['dialPlanName'] = dial_plan_name
        if route_group_name is not None:
            params['routeGroupName'] = route_group_name
        if trunk_name is not None:
            params['trunkName'] = trunk_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/dialPlans')
        data = super().get(url=url, params=params)
        return data["dialPlans"]

    def create_dial_plan(self, org_id: str = None, name: str, route_id: str, route_type: RouteType, dial_patterns: List[str] = None) -> str:
        """
        Create a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Creating a dial plan requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: Id of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        :param dial_patterns: An Array of dial patterns.
Possible values: +5555,+5556
        :type dial_patterns: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if route_id is not None:
            body['routeId'] = route_id
        if route_type is not None:
            body['routeType'] = route_type
        if dial_patterns is not None:
            body['dialPatterns'] = dial_patterns
        url = self.ep('premisePstn/dialPlans')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def dial_plan(self, dial_plan_id: str, org_id: str = None) -> GetDialPlanResponse:
        """
        Get a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Retrieving a dial plan requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        data = super().get(url=url, params=params)
        return GetDialPlanResponse.parse_obj(data)

    def modify_dial_plan(self, dial_plan_id: str, org_id: str = None, name: str, route_id: str, route_type: RouteType):
        """
        Modify a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Modifying a dial plan requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: Id of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: RouteType
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if route_id is not None:
            body['routeId'] = route_id
        if route_type is not None:
            body['routeType'] = route_type
        url = self.ep(f'premisePstn/dialPlans/{dial_plan_id}')
        super().put(url=url, params=params, json=body)
        return

    def delete_dial_plan(self, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan for the organization.
        Dial plans route calls to on-premises destinations by use of trunks or route groups.
        They are configured globally for an enterprise and apply to all users, regardless of location.
        A dial plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.
        Deleting a dial plan requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
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
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Validating Local Gateway FQDN and Domain requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which trunk types belongs.
        :type org_id: str
        :param address: FQDN or SRV address of the trunk.
        :type address: str
        :param domain: Domain name of the trunk.
        :type domain: str
        :param port: FQDN port of the trunk.
        :type port: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if address is not None:
            body['address'] = address
        if domain is not None:
            body['domain'] = domain
        if port is not None:
            body['port'] = port
        url = self.ep('premisePstn/trunks/actions/fqdnValidation/invoke')
        super().post(url=url, params=params, json=body)
        return

    def read_list_of_trunks(self, org_id: str = None, name: string array = None, location_name: string array = None, trunk_type: str = None, max: int = None, start: int = None, order: str = None) -> List[Trunk]:
        """
        List all Trunks for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List trunks for this organization.
        :type org_id: str
        :param name: Return the list of trunks matching the local gateway names.
        :type name: string array
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: string array
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the trunks according to the designated fields.  Available sort fields: name, locationName. Sort order is ascending by default
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if location_name is not None:
            params['locationName'] = location_name
        if trunk_type is not None:
            params['trunkType'] = trunk_type
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/trunks')
        data = super().get(url=url, params=params)
        return data["trunks"]

    def create_trunk(self, org_id: str = None, name: str, location_id: str, password: str, trunk_type: TrunkType, dual_identity_support_enabled: bool = None, device_type: str = None, address: str = None, domain: str = None, port: int = None, max_concurrent_calls: int = None) -> str:
        """
        Create a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Creating a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :param name: A unique name for the trunk.
        :type name: str
        :param location_id: Id of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: TrunkType
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param device_type: Device type assosiated with trunk.
        :type device_type: str
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if location_id is not None:
            body['locationId'] = location_id
        if password is not None:
            body['password'] = password
        if trunk_type is not None:
            body['trunkType'] = trunk_type
        if dual_identity_support_enabled is not None:
            body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        if device_type is not None:
            body['deviceType'] = device_type
        if address is not None:
            body['address'] = address
        if domain is not None:
            body['domain'] = domain
        if port is not None:
            body['port'] = port
        if max_concurrent_calls is not None:
            body['maxConcurrentCalls'] = max_concurrent_calls
        url = self.ep('premisePstn/trunks')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def trunk(self, trunk_id: str, org_id: str = None) -> GetTrunkResponse:
        """
        Get a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving a trunk requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        data = super().get(url=url, params=params)
        return GetTrunkResponse.parse_obj(data)

    def modify_trunk(self, trunk_id: str, org_id: str = None, name: str, password: str, dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None):
        """
        Modify a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Modifying a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: Id of the trunk being modified.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :param name: A unique name for the dial plan.
        :type name: str
        :param password: A password to use on the trunk.
        :type password: str
        :param dual_identity_support_enabled: Determines the behavior of the From and PAI headers on outbound calls.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate-based trunk.
        :type max_concurrent_calls: int
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if password is not None:
            body['password'] = password
        if dual_identity_support_enabled is not None:
            body['dualIdentitySupportEnabled'] = dual_identity_support_enabled
        if max_concurrent_calls is not None:
            body['maxConcurrentCalls'] = max_concurrent_calls
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().put(url=url, params=params, json=body)
        return

    def delete_trunk(self, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group - a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Deleting a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}')
        super().delete(url=url, params=params)
        return

    def read_list_of_trunk_types(self, org_id: str = None) -> List[TrunkTypeWithDeviceType]:
        """
        List all Trunk Types with Device Types for the organization.
        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy. Trunk Types are Registering or Certificate Based and are configured in Call Manager.
        Retrieving trunk types requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: Organization to which the trunk types belong.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('premisePstn/trunks/trunkTypes')
        data = super().get(url=url, params=params)
        return data["trunkTypes"]

    def read_list_of_routing_groups(self, org_id: str = None, name: str = None, max: int = None, start: int = None, order: str = None) -> List[RouteGroup]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and redundancy with the connection to the premises.
        Retrieving this route group list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List route groups for this organization.
        :type org_id: str
        :param name: Return the list of route groups matching the Route group name..
        :type name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the route groups according to designated fields.  Available sort orders are asc and desc.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/routeGroups')
        data = super().get(url=url, params=params)
        return data["routeGroups"]

    def create_route_group_for_organization(self, org_id: str = None, name: str, local_gateways: List[LocalGateways]) -> str:
        """
        Creates a Route Group for the organization.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the premises. Route groups can include up to 10 trunks from different locations.
        Creating a Route Group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which the Route Group belongs.
        :type org_id: str
        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: List[LocalGateways]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if local_gateways is not None:
            body['localGateways'] = local_gateways
        url = self.ep('premisePstn/routeGroups')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def read_route_group_for_organization(self, route_group_id: str, org_id: str = None) -> GetAvailableRecallHuntGroupsObject:
        """
        Reads a Route Group for the organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the premises. Route groups can include up to 10 trunks from different locations.
        Reading a Route Group requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        data = super().get(url=url, params=params)
        return data["organization"]

    def modify_route_group_for_organization(self, route_group_id: str, org_id: str = None, name: str, local_gateways: List[LocalGateways]):
        """
        Modifies an existing Route Group for an organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the premises. Route groups can include up to 10 trunks from different locations.
        Modifying a Route Group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param name: A unique name for the Route Group.
        :type name: str
        :param local_gateways: Local Gateways that are part of this Route Group.
        :type local_gateways: List[LocalGateways]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if local_gateways is not None:
            body['localGateways'] = local_gateways
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().put(url=url, params=params, json=body)
        return

    def remove_route_group_from_organization(self, route_group_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization based on id.
        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the premises. Route groups can include up to 10 trunks from different locations.
        Removing a Route Group requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_group_id: Route Group for which details are being requested.
        :type route_group_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}')
        super().delete(url=url, params=params)
        return

    def read_usage_of_routing_group(self, route_group_id: str, org_id: str = None) -> ReadUsageOfRoutingGroupResponse:
        """
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a specific Route Group.
        Users within Call to Extension locations are registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route Group.
        PSTN Connections may be a Cisco PSTN, a cloud-connected PSTN, or a premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group.
        Route Lists are a list of numbers that can be reached via a route group and can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving usage information requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Id of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with the specific route group.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usage')
        data = super().get(url=url, params=params)
        return ReadUsageOfRoutingGroupResponse.parse_obj(data)

    def read_to_extension_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, max: int = None, start: int = None, order: str = None) -> List[Location]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to the PBX using an existing trunk or route group.
        Retrieving this location list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Id of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the locations according to designated fields.  Available sort orders are asc, and desc.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageCallToExtension')
        data = super().get(url=url, params=params)
        return data["locations"]

    def read_dial_plan_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, max: int = None, start: int = None, order: str = None) -> List[Location]:
        """
        List Dial Plan Locations for a specific route group.
        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are configured globally for an enterprise and apply to all users, regardless of location.
        A Dial Plan also specifies the routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns can be defined as part of your dial plan.
        Retrieving this location list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Id of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the locations according to designated fields.  Available sort orders are asc, and desc.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageDialPlan')
        data = super().get(url=url, params=params)
        return data["locations"]

    def read_pstn_connection_locations_of_routing_group(self, route_group_id: str, org_id: str = None, location_name: str = None, max: int = None, start: int = None, order: str = None) -> List[Location]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.
        Retrieving this Location list requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Id of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param location_name: Return the list of locations matching the location name.
        :type location_name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the locations according to designated fields.  Available sort orders are asc, and desc.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_name is not None:
            params['locationName'] = location_name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usagePstnConnection')
        data = super().get(url=url, params=params)
        return data["locations"]

    def read_route_lists_of_routing_group(self, route_group_id: str, org_id: str = None, name: str = None, max: int = None, start: int = None, order: str = None) -> List[RouteGroupUsageRouteListGet]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_group_id: Id of the requested Route group.
        :type route_group_id: str
        :param org_id: Organization associated with specific route group.
        :type org_id: str
        :param name: Return the list of locations matching the location name.
        :type name: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the locations according to designated fields.  Available sort orders are asc, and desc.
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep(f'premisePstn/routeGroups/{route_group_id}/usageRouteList')
        data = super().get(url=url, params=params)
        return data["routeGroupUsageRouteListGet"]

    def read_list_of_route_lists(self, org_id: str = None, name: string array = None, location_id: string array = None, max: int = None, start: int = None, order: str = None) -> List[RouteListListGet]:
        """
        List all Route Lists for the organization.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving the Route List requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param org_id: List all Route List for this organization.
        :type org_id: str
        :param name: Return the list of Route List matching the route list name.
        :type name: string array
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: string array
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the Route List according to the designated fields. Available sort fields are name, and locationId. Sort order is ascending by default
        :type order: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if location_id is not None:
            params['locationId'] = location_id
        if max is not None:
            params['max'] = max
        if start is not None:
            params['start'] = start
        if order is not None:
            params['order'] = order
        url = self.ep('premisePstn/routeLists')
        data = super().get(url=url, params=params)
        return data["routeLists"]

    def create_route_list(self, org_id: str = None, name: str, location_id: str, route_group_id: str = None) -> str:
        """
        Create a Route List for the organization.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Creating a Route List requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param name: Name of the Route List
        :type name: str
        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param route_group_id: UUID of the route group associated with Route List.
        :type route_group_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if location_id is not None:
            body['locationId'] = location_id
        if route_group_id is not None:
            body['routeGroupId'] = route_group_id
        url = self.ep('premisePstn/routeLists')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete_route_list(self, route_list_id: str, org_id: str = None):
        """
        Delete a route list for a customer.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Deleting a Route List requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_list_id: Id of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{route_list_id}')
        super().delete(url=url, params=params)
        return

    def route_list(self, route_list_id: str, org_id: str = None) -> GetRouteListResponse:
        """
        Get a rout list details.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param route_list_id: Id of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
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
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_list_id: Id of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param name: Route List new name.
        :type name: str
        :param route_group_id: New route group Id.
        :type route_group_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if route_group_id is not None:
            body['routeGroupId'] = route_group_id
        url = self.ep(f'premisePstn/routeLists/{route_list_id}')
        super().put(url=url, params=params, json=body)
        return

    def modify_numbers_for_route_list(self, route_list_id: str, org_id: str = None, numbers: List[RouteListNumberPatch] = None, delete_all_numbers: bool = None) -> List[RouteListNumberPatchResponse]:
        """
        Modify numbers for a specific Route List of a Customer.
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_list_id: Id of the Route List.
        :type route_list_id: str
        :param org_id: Organization to which the Route List belongs.
        :type org_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: List[RouteListNumberPatch]
        :param delete_all_numbers: If present, the numbers array is ignored and all numbers in the route list are deleted.
        :type delete_all_numbers: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if numbers is not None:
            body['numbers'] = numbers
        if delete_all_numbers is not None:
            body['deleteAllNumbers'] = delete_all_numbers
        url = self.ep(f'premisePstn/routeLists/{route_list_id}/numbers')
        data = super().put(url=url, params=params, json=body)
        return data["numberStatus"]

    def numbers_assigned_to_route_list(self, route_list_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, number: str = None) -> str:
        """
        Get numbers assigned to a Route List
        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.
        Retrieving a Route List requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_write.

        :param route_list_id: Id of the Route List.
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

    def local_gateway_to_on_premises_extension_usage_for_trunk(self, trunk_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, name: string array = None) -> Location:
        """
        Get local gateway call to on-premises extension usage for a trunk.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the trunks according to the designated fields.  Available sort fields are name, and locationName. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: string array
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
        return data["location"]

    def local_gateway_dial_plan_usage_for_trunk(self, trunk_id: str, org_id: str = None, max: int = None, start: int = None, order: str = None, name: string array = None) -> List[GetAvailableRecallHuntGroupsObject]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        :param max: Limit the number of objects returned to this maximum count.
        :type max: int
        :param start: Start at the zero-based offset in the list of matching objects.
        :type start: int
        :param order: Order the trunks according to the designated fields.  Available sort fields are name, and locationName. Sort order is ascending by default
        :type order: str
        :param name: Return the list of trunks matching the local gateway names
        :type name: string array
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
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageDialPlan')
        data = super().get(url=url, params=params)
        return data["dialPlans"]

    def locations_using_local_gateway_as_pstn_connection_routing(self, trunk_id: str, org_id: str = None) -> Location:
        """
        Get Locations Using the Local Gateway as PSTN Connection Routing.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usagePstnConnection')
        data = super().get(url=url, params=params)
        return data["location"]

    def route_groups_using_local_gateway(self, trunk_id: str, org_id: str = None) -> List[RouteGroupUsageGetResponse]:
        """
        Get Route Groups Using the Local Gateway.
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usageRouteGroup')
        data = super().get(url=url, params=params)
        return data["routeGroup"]

    def local_gateway_usage_count(self, trunk_id: str, org_id: str = None) -> GetLocalGatewayUsageCountResponse:
        """
        Get Local Gateway Usage Count
        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local gateway or other supported device.
        The trunk can be assigned to a Route Group which is a group of trunks that allow Webex Calling to distribute calls over multiple trunks or to provide redundancy.
        Retrieving this information requires a full administrator auth token with a scope of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which the trunk belongs.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'premisePstn/trunks/{trunk_id}/usage')
        data = super().get(url=url, params=params)
        return GetLocalGatewayUsageCountResponse.parse_obj(data)

    def details_for_queue_holiday_service(self, location_id: str, queue_id: str, org_id: str = None) -> List[CallQueueHolidaySchedulesObject]:
        """
        Retrieve Call Queue Holiday Service details.
        Configure the call queue to route calls differently during the holidays.
        Retrieving call queue holiday service details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        data = super().get(url=url, params=params)
        return data["holidaySchedules"]

    def update_queue_holiday_service(self, location_id: str, queue_id: str, org_id: str = None, holiday_service_enabled: bool, action: enum, holiday_schedule_level: enum, play_announcement_before_enabled: bool, audio_message_selection: enum, holiday_schedule_name: str = None, transfer_phone_number: str = None, audio_files: List[CallQueueAudioFilesObject] = None):
        """
        Update the designated Call Queue Holiday Service.
        Configure the call queue to route calls differently during the holidays.
        Updating a call queue holiday service requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param holiday_service_enabled: Enable or Disable the call queue holiday service routing policy.
        :type holiday_service_enabled: bool
        :param action: Specifies call processing action type.
        :type action: enum
        :param holiday_schedule_level: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific. (Must be from holidaySchedules list)
        :type holiday_schedule_level: enum
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the action.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: enum
        :param holiday_schedule_name: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
        :type holiday_schedule_name: str
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: List[CallQueueAudioFilesObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if holiday_service_enabled is not None:
            body['holidayServiceEnabled'] = holiday_service_enabled
        if action is not None:
            body['action'] = action
        if holiday_schedule_level is not None:
            body['holidayScheduleLevel'] = holiday_schedule_level
        if play_announcement_before_enabled is not None:
            body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        if audio_message_selection is not None:
            body['audioMessageSelection'] = audio_message_selection
        if holiday_schedule_name is not None:
            body['holidayScheduleName'] = holiday_schedule_name
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        if audio_files is not None:
            body['audioFiles'] = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/holidayService')
        super().put(url=url, params=params, json=body)
        return

    def details_for_queue_night_service(self, location_id: str, queue_id: str, org_id: str = None) -> List[CallQueueHolidaySchedulesObject]:
        """
        Retrieve Call Queue Night service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Retrieving call queue details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        data = super().get(url=url, params=params)
        return data["businessHourSchedules"]

    def update_queue_night_service(self, location_id: str, queue_id: str, org_id: str = None, night_service_enabled: bool, play_announcement_before_enabled: bool, announcement_mode: enum, audio_message_selection: enum, force_night_service_enabled: bool, manual_audio_message_selection: enum, action: enum = None, transfer_phone_number: str = None, audio_files: List[CallQueueAudioFilesObject] = None, business_hours_name: str = None, business_hours_level: enum = None, manual_audio_files: List[CallQueueAudioFilesObject] = None):
        """
        Update Call Queue Night Service details.
        Configure the call queue to route calls differently during the hours when the queue is not in service. This is
        determined by a schedule that defines the business hours of the queue.
        Retrieving call queue night service details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organization.
        :type org_id: str
        :param night_service_enabled: Enable or disable call queue night service routing policy.
        :type night_service_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the action.
        :type play_announcement_before_enabled: bool
        :param announcement_mode: Specifies the type of announcements to played.
        :type announcement_mode: enum
        :param audio_message_selection: Specifies what type of announcements to be played when announcementMode is NORMAL.
        :type audio_message_selection: enum
        :param force_night_service_enabled: Force night service regardless of business hour schedule.
        :type force_night_service_enabled: bool
        :param manual_audio_message_selection: Specifies what type of announcement to be played when announcementMode is MANUAL.
        :type manual_audio_message_selection: enum
        :param action: Specifies call processing action type.
        :type action: enum
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: List[CallQueueAudioFilesObject]
        :param business_hours_name: Name of the schedule configured for a night service as one of from businessHourSchedules list.
        :type business_hours_name: str
        :param business_hours_level: Specifies whether the above mentioned schedule is org or location specific. (Must be from businessHourSchedules list)
        :type business_hours_level: enum
        :param manual_audio_files: List Of pre-configured Audio Files.
        :type manual_audio_files: List[CallQueueAudioFilesObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if night_service_enabled is not None:
            body['nightServiceEnabled'] = night_service_enabled
        if play_announcement_before_enabled is not None:
            body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        if announcement_mode is not None:
            body['announcementMode'] = announcement_mode
        if audio_message_selection is not None:
            body['audioMessageSelection'] = audio_message_selection
        if force_night_service_enabled is not None:
            body['forceNightServiceEnabled'] = force_night_service_enabled
        if manual_audio_message_selection is not None:
            body['manualAudioMessageSelection'] = manual_audio_message_selection
        if action is not None:
            body['action'] = action
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        if audio_files is not None:
            body['audioFiles'] = audio_files
        if business_hours_name is not None:
            body['businessHoursName'] = business_hours_name
        if business_hours_level is not None:
            body['businessHoursLevel'] = business_hours_level
        if manual_audio_files is not None:
            body['manualAudioFiles'] = manual_audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/nightService')
        super().put(url=url, params=params, json=body)
        return

    def details_for_queue_forced_forward(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueForcedForwardResponse:
        """
        Retrieve Call Queue policy Forced Forward details.
        This policy allows calls to be temporarily diverted to a configured destination.
        Retrieving call queue Forced Forward details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueForcedForwardResponse.parse_obj(data)

    def update_queue_forced_forward_service(self, location_id: str, queue_id: str, org_id: str = None, forced_forward_enabled: bool, play_announcement_before_enabled: bool, audio_message_selection: enum, transfer_phone_number: str = None, audio_files: List[CallQueueAudioFilesObject] = None):
        """
        Update the designated Forced Forward Service.
        If the option is enabled, then incoming calls to the queue are forwarded to the configured destination. Calls that are already in the queue remain queued.
        The policy can be configured to play an announcement prior to proceeding with the forward.
        Updating a call queue Forced Forward service requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param forced_forward_enabled: Enable or disable call forced forward service routing policy.
        :type forced_forward_enabled: bool
        :param play_announcement_before_enabled: Specifies if an announcement plays to callers before applying the action.
        :type play_announcement_before_enabled: bool
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: enum
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: List[CallQueueAudioFilesObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if forced_forward_enabled is not None:
            body['forcedForwardEnabled'] = forced_forward_enabled
        if play_announcement_before_enabled is not None:
            body['playAnnouncementBeforeEnabled'] = play_announcement_before_enabled
        if audio_message_selection is not None:
            body['audioMessageSelection'] = audio_message_selection
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        if audio_files is not None:
            body['audioFiles'] = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/forcedForward')
        super().put(url=url, params=params, json=body)
        return

    def details_for_queue_stranded(self, location_id: str, queue_id: str, org_id: str = None) -> GetDetailsForCallQueueStrandedCallsResponse:
        """
        Allow admin to view default/configured Stranded Calls settings.
        Stranded-All agents logoff Policy: If the last agent staffing a queue “unjoins” the queue or signs out, then all calls in the queue become stranded.
        Stranded-Unavailable Policy: This policy allows for the configuration of the processing of calls that are in a staffed queue when all agents are unavailable.
        Retrieving call queue Stranded Calls details requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

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
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        data = super().get(url=url, params=params)
        return GetDetailsForCallQueueStrandedCallsResponse.parse_obj(data)

    def update_queue_stranded_service(self, location_id: str, queue_id: str, org_id: str = None, action: enum, audio_message_selection: enum, transfer_phone_number: str = None, audio_files: List[CallQueueAudioFilesObject] = None):
        """
        Update the designated Call Stranded Calls Service.
        Allow admin to modify configured Stranded Calls settings.
        Updating a call queue stranded calls requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Update call queue settings from this organization.
        :type org_id: str
        :param action: Specifies call processing action type.
        :type action: enum
        :param audio_message_selection: Specifies what type of announcement to be played.
        :type audio_message_selection: enum
        :param transfer_phone_number: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
        :type transfer_phone_number: str
        :param audio_files: List of pre-configured Announcement Audio Files when audioMessageSelection is CUSTOM.
        :type audio_files: List[CallQueueAudioFilesObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if action is not None:
            body['action'] = action
        if audio_message_selection is not None:
            body['audioMessageSelection'] = audio_message_selection
        if transfer_phone_number is not None:
            body['transferPhoneNumber'] = transfer_phone_number
        if audio_files is not None:
            body['audioFiles'] = audio_files
        url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
        super().put(url=url, params=params, json=body)
        return

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


class ConfigurepersonsCallingBehaviorBody(ApiModel):
    #: The new Calling Behavior setting for the person (case-insensitive). If null, the effective Calling Behavior will be the Organization's current default.
    behavior_type: Optional[BehaviorType]
    #: The UC Manager Profile ID. Specifying null results in the organizational default being applied.
    profile_id: Optional[str]


class NoAnswer3(BusinessContinuity):
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for numberOfRings setting.
    system_max_number_of_rings: Optional[int]


class CallForwarding4(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[Always]
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person is busy.
    busy: Optional[BusinessContinuity]
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[NoAnswer3]


class ConfigureCallRecordingSettingsForPersonBody(ApiModel):
    #: true if call recording is enabled.
    enabled: Optional[bool]
    #: Call recording scenario.
    record: Optional[Record]
    #: When true, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool]
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
    start_stop_announcement_enabled: Optional[bool]
    #: Pause/resume notification settings.
    #: true when notification feature is in effect. false indicates notification is disabled.
    notification: Optional[object]
    #: Beep sound plays periodically.
    repeat: Optional[Repeat]


class CallerIdSelectedType(ApiModel):
    #: Outgoing caller ID will show the caller's direct line number and/or extension.
    direct_line: Optional[str]
    #: Outgoing caller ID will show the main number for the location.
    location_number: Optional[str]
    #: Outgoing caller ID will show the mobile number for this person.
    mobile_number: Optional[str]
    #: Outgoing caller ID will show the value from the customNumber field.
    custom: Optional[str]


class ConfigureCallerIDSettingsForPersonBody(ApiModel):
    #: Which type of outgoing Caller ID will be used.
    #: Possible values: DIRECT_LINE
    selected: Optional[CallerIdSelectedType]
    #: This value must be an assigned number from the person's location.
    custom_number: Optional[str]
    #: Person's Caller ID first name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
    first_name: Optional[str]
    #: Person's Caller ID last name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
    last_name: Optional[str]
    #: true if person's identity has to be blocked when receiving a transferred or forwarded call.
    block_in_forward_calls_enabled: Optional[bool]
    #: Designates which type of External Caller Id Name policy is used. Default is DIRECT_LINE.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: Person's custom External Caller ID last name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
    custom_external_caller_id_name: Optional[str]


class SendAllCalls(ApiModel):
    #: All calls will be sent to voicemail.
    enabled: Optional[bool]


class SendBusyCalls1(ApiModel):
    #: Calls will be sent to voicemail when busy.
    enabled: Optional[bool]
    #: DEFAULT indicates the default greeting will be played. CUSTOM indicates a custom .wav file will be played.
    greeting: Optional[Greeting]


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


class FaxMessage3(ApiModel):
    #: When true FAX messages for new voicemails will be sent to the designated number.
    enabled: Optional[bool]
    #: Designates phone number for the FAX. A value for this field must be provided in the request if faxMessage enabled field is given as true in the request.
    phone_number: Optional[str]
    #: Designates optional extension for the FAX.
    extension: Optional[str]


class ScheduleShortDetails(GetAvailableRecallHuntGroupsObject):
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[Type24]


class RecurWeekly2(RecurWeeklyObject):
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int]


class Recurrence(ApiModel):
    #: True if the event repeats forever. Requires either recurDaily or recurWeekly to be specified.
    recur_for_ever: Optional[bool]
    #: End date for the recurring event in the format of YYYY-MM-DD. Requires either recurDaily or recurWeekly to be specified.
    recur_end_date: Optional[str]
    #: End recurrence after the event has repeated the specified number of times. Requires either recurDaily or recurWeekly to be specified.
    recur_end_occurrence: Optional[int]
    #: Specifies the number of days between the start of each recurrence. Not allowed with recurWeekly.
    #: Recurring interval in days. The number of days after the start when an event will repeat.  Repetitions cannot overlap.
    recur_daily: Optional[object]
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with recurDaily.
    recur_weekly: Optional[RecurWeekly2]


class EventLongDetails(ApiModel):
    #: Name for the event.
    name: Optional[str]
    #: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
    start_date: Optional[str]
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
    end_date: Optional[str]
    #: Start time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
    start_time: Optional[str]
    #: End time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
    end_time: Optional[str]
    #: True if it is all-day event.
    all_day_enabled: Optional[bool]
    #: Recurrance scheme for an event.
    recurrence: Optional[Recurrence]


class CreateScheduleForPersonBody(ApiModel):
    #: Name for the schedule.
    name: Optional[str]
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[Type24]
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person or workspace to be monitored.
    id: Optional[str]
    #: Last name of the monitored person or workspace.
    last_name: Optional[str]
    #: First name of the monitored person or workspace.
    first_name: Optional[str]
    #: Display name of the monitored person or workspace.
    display_name: Optional[str]
    #: Indicates whether type is person or workspace.
    type: Optional[Type8]
    #: Email address of the monitored person or workspace.
    email: Optional[str]
    #: List of phone numbers of the monitored person or workspace.
    numbers: Optional[list[GetUserNumberItemObject]]


class Member(MonitoredMemberObject):
    #: The location name where the call park extension is.
    location: Optional[str]
    #: The ID for the location.
    location_id: Optional[str]


class Callparkextension(GetAvailableRecallHuntGroupsObject):
    #: The extension number for the call park extension.
    extension: Optional[str]
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
    #: Type usually indicates PEOPLE or PLACE. Push-to-Talk and Privacy features only supports PEOPLE.
    type: Optional[Type8]
    #: Email address of the person.
    email: Optional[str]
    #: List of phone numbers of the person.
    numbers: Optional[list[GetUserNumberItemObject]]


class Type31(str, Enum):
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive.
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class PushToTalkConnectionType(ApiModel):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk for cannot respond.
    one_way: Optional[str]
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk for can respond.
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


class CallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: Possible values: INTERNAL_CALL, LOCAL, TOLL_FREE, TOLL, INTERNATIONAL, OPERATOR_ASSISTED, CHARGEABLE_DIRECTORY_ASSISTED, SPECIAL_SERVICES_I, SPECIAL_SERVICES_II, PREMIUM_SERVICES_I, PREMIUM_SERVICES_II
    call_type: Optional[str]
    #: Action on the given callType.
    #: Possible values: ALLOW, BLOCK, AUTH_CODE, TRANSFER_NUMBER_1, TRANSFER_NUMBER_2, TRANSFER_NUMBER_3
    action: Optional[str]
    #: Allow the person to transfer or forward a call of the specified call type.
    #: Possible values: 
    transfer_enabled: Optional[bool]


class PhoneNumber(GetUserNumberItemObject):
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[DialPatternAction]
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern]


class CallQueueObject(GetAvailableRecallHuntGroupsObject):
    #: When not null, indicates the Call Queue's phone number.
    phone_number: Optional[str]
    #: When not null, indicates the Call Queue's extension number.
    extension: Optional[str]


class CallQueueObject1(GetAvailableRecallHuntGroupsObject):
    #: When not null, indicates the Call Queue's phone number.
    phone_number: Optional[str]
    #: When not null, indicates the Call Queue's extension number.
    extension: Optional[str]


class ReadPersonsCallingBehaviorResponse(ConfigurepersonsCallingBehaviorBody):
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if the user's behaviorType is set to null.
    effective_behavior_type: Optional[EffectiveBehaviorType]


class ReadBargeInSettingsForPersonResponse(ApiModel):
    #: Indicates if the Barge In feature is enabled.
    enabled: Optional[bool]
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: Optional[bool]


class ReadForwardingSettingsForPersonResponse(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwarding4]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[BusinessContinuity]


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


class ReadDoNotDisturbSettingsForPersonResponse(ApiModel):
    #: true if the Do Not Disturb feature is enabled.
    enabled: Optional[bool]
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: Optional[bool]


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
    fax_message: Optional[FaxMessage3]


class ListOfSchedulesForPersonResponse(ApiModel):
    #: Indicates a list of schedules.
    schedules: Optional[list[ScheduleShortDetails]]


class CreateScheduleForPersonResponse(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class GetScheduleDetailsResponse(GetAvailableRecallHuntGroupsObject):
    #: Indicates the schedule type whether businessHours or holidays.
    type: Optional[Type24]
    #: Indicates a list of events.
    events: Optional[list[EventLongDetails]]


class UpdateScheduleBody1(CreateScheduleForPersonBody):
    #: New name for the schedule.
    new_name: Optional[str]


class UpdateScheduleResponse1(ApiModel):
    #: Identifier for a schedule.
    id: Optional[str]


class FetchEventForpersonsScheduleResponse(GetAvailableRecallHuntGroupsObject):
    #: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
    start_date: Optional[str]
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
    end_date: Optional[str]
    #: Start time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
    start_time: Optional[str]
    #: End time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
    end_time: Optional[str]
    #: True if it is all-day event.
    all_day_enabled: Optional[bool]
    #: Recurrance scheme for an event.
    recurrence: Optional[Recurrence]


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
    #: Settings of monitored elements which can be person, place, or call park extension.
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
    type: Optional[Type31]


class ModifyExecutiveAssistantSettingsForPersonBody(ApiModel):
    #: executive assistant type
    type: Optional[Type31]


class ReadReceptionistClientSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Receptionist Client feature.
    reception_enabled: Optional[bool]
    #: List of people and/or workspaces to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]]


class ConfigureReceptionistClientSettingsForPersonBody(ApiModel):
    #: true if the Receptionist Client feature is enabled.
    reception_enabled: Optional[bool]
    #: List of members' unique identifiers to monitor.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    monitored_members: Optional[list[str]]


class ReadPushtoTalkSettingsForPersonResponse(ApiModel):
    #: Set to true to enable the Push-to-Talk feature.  When enabled, a person receives a Push-to-Talk call and answers the call automatically.
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


class ReadIncomingPermissionSettingsForPersonResponse(ApiModel):
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather than the organizational defaults.
    use_custom_enabled: Optional[bool]
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: Optional[ExternalTransfer]
    #: Internal calls are allowed to be received.
    internal_calls_enabled: Optional[bool]
    #: Collect calls are allowed to be received.
    collect_calls_enabled: Optional[bool]


class RetrievepersonsOutgoingCallingPermissionsSettingsResponse(ApiModel):
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    use_custom_enabled: Optional[bool]
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[CallingPermissions]]


class AssignOrUnassignNumbersTopersonBody(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    enable_distinctive_ring_pattern: Optional[bool]
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]]


class RetrieveListOfCallQueueCallerIDInformationResponse(ApiModel):
    #: Indicates a list of Call Queues that the agent belongs and are available to be selected as the Caller ID for outgoing calls. It is empty when the agent's Call Queues have disabled the Call Queue outgoing phone number setting to be used as Caller ID. In the case where this setting is enabled the array will be populated.
    available_queues: Optional[list[CallQueueObject]]


class RetrieveCallQueueAgentsCallerIDInformationResponse(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[CallQueueObject1]


class ModifyCallQueueAgentsCallerIDInformationBody(ApiModel):
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
    selected_queue: Optional[GetAvailableRecallHuntGroupsObject]


class WebexCallingPersonSettingsApi(ApiChild, base=''):
    """
    Not supported for Webex for Government (FedRAMP)
    Webex Calling Person Settings supports modifying Webex Calling settings for a specific person.
    Viewing People requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read or, for select APIs, a user auth token with spark:people_read scope can be used by a person to read their own settings.
    Configuring People settings requires a full or user administrator auth token with the spark-admin:people_write scope or, for select APIs, a user auth token with spark:people_write scope can be used by a person to update their own settings.
    """

    def read_persons_calling_behavior(self, person_id: str, org_id: str = None) -> enum:
        """
        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling behavior and calling UC Manager Profile ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        data = super().get(url=url, params=params)
        return data["effectiveBehaviorType"]

    def configurepersons_calling_behavior(self, person_id: str, org_id: str = None, behavior_type: enum = None, profile_id: str = None):
        """
        Modifies the calling behavior settings for the person which includes calling behavior and UC Manager Profile ID.
        Webex Calling Behavior controls which Webex telephony application and which UC Manager Profile is to be used for a person.
        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.
        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex (Unified CM).
        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param behavior_type: The new Calling Behavior setting for the person (case-insensitive). If null, the effective Calling Behavior will be the Organization's current default.
        :type behavior_type: enum
        :param profile_id: The UC Manager Profile ID. Specifying null results in the organizational default being applied.
        :type profile_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if behavior_type is not None:
            body['behaviorType'] = behavior_type
        if profile_id is not None:
            body['profileId'] = profile_id
        url = self.ep(f'people/{person_id}/features/callingBehavior')
        super().put(url=url, params=params, json=body)
        return

    def read_barge_in_for_person(self, person_id: str, org_id: str = None) -> ReadBargeInSettingsForPersonResponse:
        """
        Retrieve a person's Barge In settings.
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: Set to enable or disable the Barge In feature.
        :type enabled: bool
        :param tone_enabled: Set to enable or disable a stutter dial tone being played when a person is barging in on the active call.
        :type tone_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if tone_enabled is not None:
            body['toneEnabled'] = tone_enabled
        url = self.ep(f'people/{person_id}/features/bargeIn')
        super().put(url=url, params=params, json=body)
        return

    def read_forwarding_for_person(self, person_id: str, org_id: str = None) -> ReadForwardingSettingsForPersonResponse:
        """
        Retrieve a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring problem.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callForwarding')
        data = super().get(url=url, params=params)
        return ReadForwardingSettingsForPersonResponse.parse_obj(data)

    def configure_call_forwarding_for_person(self, person_id: str, org_id: str = None, call_forwarding: object = None, business_continuity: object = None):
        """
        Configure a person's Call Forwarding settings.
        Three types of call forwarding are supported:
        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring problem.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param call_forwarding: Settings related to "Always", "Busy", and "No Answer" call forwarding.
        :type call_forwarding: object
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring problem.
        :type business_continuity: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding
        if business_continuity is not None:
            body['businessContinuity'] = business_continuity
        url = self.ep(f'people/{person_id}/features/callForwarding')
        super().put(url=url, params=params, json=body)
        return

    def read_call_intercept_for_person(self, person_id: str, org_id: str = None) -> GetLocationInterceptResponse:
        """
        Retrieves Person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with informative announcements and alternative routing options. Depending on the service configuration, none, some, or all incoming calls to the specified person are intercepted. Also depending on the service configuration, outgoing calls are intercepted or rerouted to another location.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/intercept')
        data = super().get(url=url, params=params)
        return GetLocationInterceptResponse.parse_obj(data)

    def configure_call_intercept_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, incoming: object = None, outgoing: object = None):
        """
        Configures a person's Call Intercept settings.
        The intercept feature gracefully takes a person's phone out of service, while providing callers with informative announcements and alternative routing options. Depending on the service configuration, none, some, or all incoming calls to the specified person are intercepted. Also depending on the service configuration, outgoing calls are intercepted or rerouted to another location.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: true if the intercept feature is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: object
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming
        if outgoing is not None:
            body['outgoing'] = outgoing
        url = self.ep(f'people/{person_id}/features/intercept')
        super().put(url=url, params=params, json=body)
        return

    def configure_call_intercept_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Call Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callRecording')
        data = super().get(url=url, params=params)
        return ReadCallRecordingSettingsForPersonResponse.parse_obj(data)

    def configure_call_recording_for_person(self, person_id: str, org_id: str = None, enabled: bool = None, record: enum = None, record_voicemail_enabled: bool = None, start_stop_announcement_enabled: bool = None, notification: object = None, repeat: object = None):
        """
        Configure a person's Call Recording settings.
        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: true if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: enum
        :param record_voicemail_enabled: When true, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param start_stop_announcement_enabled: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
        :type start_stop_announcement_enabled: bool
        :param notification: Pause/resume notification settings.
true when notification feature is in effect. false indicates notification is disabled.
        :type notification: object
        :param repeat: Beep sound plays periodically.
        :type repeat: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if record is not None:
            body['record'] = record
        if record_voicemail_enabled is not None:
            body['recordVoicemailEnabled'] = record_voicemail_enabled
        if start_stop_announcement_enabled is not None:
            body['startStopAnnouncementEnabled'] = start_stop_announcement_enabled
        if notification is not None:
            body['notification'] = notification
        if repeat is not None:
            body['repeat'] = repeat
        url = self.ep(f'people/{person_id}/features/callRecording')
        super().put(url=url, params=params, json=body)
        return

    def read_caller_id_for_person(self, person_id: str, org_id: str = None) -> ReadCallerIDSettingsForPersonResponse:
        """
        Retrieve a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callerId')
        data = super().get(url=url, params=params)
        return ReadCallerIDSettingsForPersonResponse.parse_obj(data)

    def configure_caller_id_for_person(self, person_id: str, org_id: str = None, selected: CallerIdSelectedType = None, custom_number: str = None, first_name: str = None, last_name: str = None, block_in_forward_calls_enabled: bool = None, external_caller_id_name_policy: enum = None, custom_external_caller_id_name: str = None):
        """
        Configure a person's Caller ID settings.
        Caller ID settings control how a person's information is displayed when making outgoing calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used.
Possible values: DIRECT_LINE
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person's location.
        :type custom_number: str
        :param first_name: Person's Caller ID first name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
        :type first_name: str
        :param last_name: Person's Caller ID last name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
        :type last_name: str
        :param block_in_forward_calls_enabled: true if person's identity has to be blocked when receiving a transferred or forwarded call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller Id Name policy is used. Default is DIRECT_LINE.
        :type external_caller_id_name_policy: enum
        :param custom_external_caller_id_name: Person's custom External Caller ID last name.  Characters of %,  +, ``, " and Unicode characters are not allowed.
        :type custom_external_caller_id_name: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if selected is not None:
            body['selected'] = selected
        if custom_number is not None:
            body['customNumber'] = custom_number
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if block_in_forward_calls_enabled is not None:
            body['blockInForwardCallsEnabled'] = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body['externalCallerIdNamePolicy'] = external_caller_id_name_policy
        if custom_external_caller_id_name is not None:
            body['customExternalCallerIdName'] = custom_external_caller_id_name
        url = self.ep(f'people/{person_id}/features/callerId')
        super().put(url=url, params=params, json=body)
        return

    def read_do_not_disturb_for_person(self, person_id: str, org_id: str = None) -> ReadDoNotDisturbSettingsForPersonResponse:
        """
        Retrieve a person's Do Not Disturb settings.
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: true if the Do Not Disturb feature is enabled.
        :type enabled: bool
        :param ring_splash_enabled: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
        :type ring_splash_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        if ring_splash_enabled is not None:
            body['ringSplashEnabled'] = ring_splash_enabled
        url = self.ep(f'people/{person_id}/features/doNotDisturb')
        super().put(url=url, params=params, json=body)
        return

    def read_voicemail_for_person(self, person_id: str, org_id: str = None) -> ReadVoicemailSettingsForPersonResponse:
        """
        Retrieve a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include the voicemail files.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail')
        data = super().get(url=url, params=params)
        return ReadVoicemailSettingsForPersonResponse.parse_obj(data)

    def configure_voicemail_for_person(self, person_id: str, org_id: str = None, notifications: object, transfer_to_number: object, enabled: bool = None, send_all_calls: object = None, send_busy_calls: object = None, send_unanswered_calls: object = None, email_copy_of_message: object = None, message_storage: object = None, fax_message: object = None):
        """
        Configure a person's Voicemail settings.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.
        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include the voicemail files.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param notifications: Settings for notifications when there are any new voicemails.
        :type notifications: object
        :param transfer_to_number: Settings for voicemail caller to transfer to a different number by pressing zero (0).
        :type transfer_to_number: object
        :param enabled: Voicemail is enabled or disabled.
        :type enabled: bool
        :param send_all_calls: Settings for sending all calls to voicemail.
All calls will be sent to voicemail.
        :type send_all_calls: object
        :param send_busy_calls: Settings for sending calls to voicemail when the line is busy.
        :type send_busy_calls: object
        :param send_unanswered_calls: 
        :type send_unanswered_calls: object
        :param email_copy_of_message: Settings for sending a copy of new voicemail message audio via email.
        :type email_copy_of_message: object
        :param message_storage: 
        :type message_storage: object
        :param fax_message: 
        :type fax_message: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if notifications is not None:
            body['notifications'] = notifications
        if transfer_to_number is not None:
            body['transferToNumber'] = transfer_to_number
        if enabled is not None:
            body['enabled'] = enabled
        if send_all_calls is not None:
            body['sendAllCalls'] = send_all_calls
        if send_busy_calls is not None:
            body['sendBusyCalls'] = send_busy_calls
        if send_unanswered_calls is not None:
            body['sendUnansweredCalls'] = send_unanswered_calls
        if email_copy_of_message is not None:
            body['emailCopyOfMessage'] = email_copy_of_message
        if message_storage is not None:
            body['messageStorage'] = message_storage
        if fax_message is not None:
            body['faxMessage'] = fax_message
        url = self.ep(f'people/{person_id}/features/voicemail')
        super().put(url=url, params=params, json=body)
        return

    def configure_busy_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/voicemail/actions/uploadBusyGreeting/invoke')
        super().post(url=url, params=params)
        return

    def configure_no_answer_voicemail_greeting_for_person(self, person_id: str, org_id: str = None):
        """
        Configure a person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio file.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        Schedules are used to support calling features and can be defined at the location or person level. businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param name: Specifies the case insensitive substring to be matched against the schedule names. The maximum length is 40.
        :type name: str
        :param type_: Specifies the schedule event type to be matched on the given type.
        :type type_: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if type_ is not None:
            params['type'] = type_
        url = self.ep(f'people/{person_id}/features/schedules')
        return self.session.follow_pagination(url=url, model=ScheduleShortDetails, params=params)

    def create_schedule_for_person(self, person_id: str, org_id: str = None, name: str, type_: Type24, events: List[EventLongDetails] = None) -> str:
        """
        Create a new schedule for a person.
        Schedules are used to support calling features and can be defined at the location or person level. businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: Type24
        :param events: Indicates a list of events.
        :type events: List[EventLongDetails]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if type_ is not None:
            body['type'] = type_
        if events is not None:
            body['events'] = events
        url = self.ep(f'people/{person_id}/features/schedules')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def schedule_details(self, person_id: str, schedule_type: Type24, schedule_id: str, org_id: str = None) -> GetScheduleDetailsResponse:
        """
        Retrieve a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level. businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().get(url=url, params=params)
        return GetScheduleDetailsResponse.parse_obj(data)

    def update_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, org_id: str = None, new_name: str, name: str, type_: Type24, events: List[EventLongDetails] = None) -> str:
        """
        Modify a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level. businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param new_name: New name for the schedule.
        :type new_name: str
        :param name: Name for the schedule.
        :type name: str
        :param type_: Indicates the schedule type whether businessHours or holidays.
        :type type_: Type24
        :param events: Indicates a list of events.
        :type events: List[EventLongDetails]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if new_name is not None:
            body['newName'] = new_name
        if name is not None:
            body['name'] = name
        if type_ is not None:
            body['type'] = type_
        if events is not None:
            body['events'] = events
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, org_id: str = None):
        """
        Delete a schedule by its schedule ID.
        Schedules are used to support calling features and can be defined at the location or person level. businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}')
        super().delete(url=url, params=params)
        return

    def fetch_event_forpersons_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, event_id: str, org_id: str = None) -> FetchEventForpersonsScheduleResponse:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().get(url=url, params=params)
        return FetchEventForpersonsScheduleResponse.parse_obj(data)

    def add_new_event_for_persons_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, org_id: str = None, name: str, start_date: str, end_date: str, start_time: str, end_time: str, all_day_enabled: bool = None, recurrence: object = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
        :type end_time: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events')
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def update_event_forpersons_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, event_id: str, org_id: str = None, new_name: str, name: str, start_date: str, end_date: str, start_time: str, end_time: str, all_day_enabled: bool = None, recurrence: object = None) -> str:
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param new_name: New name for the event.
        :type new_name: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
        :type start_date: str
        :param end_date: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD.  This field is required if the allDayEnabled field is present.
        :type end_date: str
        :param start_time: Start time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
        :type start_time: str
        :param end_time: End time of the event in the format of HH:MM (24 hours format).  This field is required if the allDayEnabled field is false or omitted.
        :type end_time: str
        :param all_day_enabled: True if it is all-day event.
        :type all_day_enabled: bool
        :param recurrence: Recurrance scheme for an event.
        :type recurrence: object
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if new_name is not None:
            body['newName'] = new_name
        if name is not None:
            body['name'] = name
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence
        url = self.ep(f'people/{person_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}')
        data = super().put(url=url, params=params, json=body)
        return data["id"]

    def delete_event_forpersons_schedule(self, person_id: str, schedule_type: Type24, schedule_id: str, event_id: str, org_id: str = None):
        """
        People can use shared location schedules or define personal schedules containing events.
        businessHours schedules allow you to apply specific call settings at different times of the day or week by defining one or more events. holidays schedules define exceptions to normal business hours by defining one or more events.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param schedule_type: Type of schedule, either businessHours or holidays.
        :type schedule_type: Type24
        :param schedule_id: Unique identifier for the schedule.
        :type schedule_id: str
        :param event_id: Unique identifier for the event.
        :type event_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        With this feature, a person can place an active call on hold and answer an incoming call.  When enabled, while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the call.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/callWaiting')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_call_waiting_for_person(self, person_id: str, org_id: str = None, enabled: bool):
        """
        Configure a person's Call Waiting settings.
        With this feature, a person can place an active call on hold and answer an incoming call.  When enabled, while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore the call.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'people/{person_id}/features/callWaiting')
        super().put(url=url, params=params, json=body)
        return

    def retrievepersons_monitoring(self, person_id: str, org_id: str = None) -> RetrievepersonsMonitoringSettingsResponse:
        """
        Retrieves the monitoring settings of the person, which shows specified people, places or, call park extenions that are being monitoring.
        Monitors the line status which indicates if a person or place is on a call and if a call has been parked on that extension.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/monitoring')
        data = super().get(url=url, params=params)
        return RetrievepersonsMonitoringSettingsResponse.parse_obj(data)

    def modifypersons_monitoring(self, person_id: str, org_id: str = None, enable_call_park_notification: bool, monitored_elements: List[str]):
        """
        Modifies the monitoring settings of the person.
        Monitors the line status of specified people, places or, call park extension. The line status indicates if a person or place is on a call and if a call has been parked on that extension.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enable_call_park_notification: Enable or disable call park notification.
        :type enable_call_park_notification: bool
        :param monitored_elements: Identifiers of monitored elements whose monitoring settings will be modified.
Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
        :type monitored_elements: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enable_call_park_notification is not None:
            body['enableCallParkNotification'] = enable_call_park_notification
        if monitored_elements is not None:
            body['monitoredElements'] = monitored_elements
        url = self.ep(f'people/{person_id}/features/monitoring')
        super().put(url=url, params=params, json=body)
        return

    def list_of_phone_numbers_for_person(self, person_id: str, org_id: str = None) -> GetListOfPhoneNumbersForPersonResponse:
        """
        Get a person's phone numbers including alternate numbers.
        A person can have one or more phone numbers and/or extensions via which they can be called.
        This API requires a full or user administrator auth token with the spark-admin:people_read scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/numbers')
        data = super().get(url=url, params=params)
        return GetListOfPhoneNumbersForPersonResponse.parse_obj(data)

    def retrievepersons_application_services(self, person_id: str, org_id: str = None) -> int:
        """
        Application services let you determine the ringing behavior for calls made to people in certain scenarios. You can also specify which devices can download the Webex Calling app.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/applications')
        data = super().get(url=url, params=params)
        return data["availableLineCount"]

    def modifypersons_application_services(self, person_id: str, org_id: str = None, ring_devices_for_click_to_dial_calls_enabled: bool = None, ring_devices_for_group_page_enabled: bool = None, ring_devices_for_call_park_enabled: bool = None, desktop_client_enabled: bool = None, tablet_client_enabled: bool = None, mobile_client_enabled: bool = None):
        """
        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You can also specify which devices users can download the Webex Calling app on.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param ring_devices_for_click_to_dial_calls_enabled: When true, indicates to ring devices for outbound Click to Dial calls.
        :type ring_devices_for_click_to_dial_calls_enabled: bool
        :param ring_devices_for_group_page_enabled: When true, indicates to ring devices for inbound Group Pages.
        :type ring_devices_for_group_page_enabled: bool
        :param ring_devices_for_call_park_enabled: When true, indicates to ring devices for Call Park recalled.
        :type ring_devices_for_call_park_enabled: bool
        :param desktop_client_enabled: Indicates that the desktop Webex Calling application is enabled for use.
        :type desktop_client_enabled: bool
        :param tablet_client_enabled: Indicates that the tablet Webex Calling application is enabled for use.
        :type tablet_client_enabled: bool
        :param mobile_client_enabled: Indicates that the mobile Webex Calling application is enabled for use.
        :type mobile_client_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if ring_devices_for_click_to_dial_calls_enabled is not None:
            body['ringDevicesForClickToDialCallsEnabled'] = ring_devices_for_click_to_dial_calls_enabled
        if ring_devices_for_group_page_enabled is not None:
            body['ringDevicesForGroupPageEnabled'] = ring_devices_for_group_page_enabled
        if ring_devices_for_call_park_enabled is not None:
            body['ringDevicesForCallParkEnabled'] = ring_devices_for_call_park_enabled
        if desktop_client_enabled is not None:
            body['desktopClientEnabled'] = desktop_client_enabled
        if tablet_client_enabled is not None:
            body['tabletClientEnabled'] = tablet_client_enabled
        if mobile_client_enabled is not None:
            body['mobileClientEnabled'] = mobile_client_enabled
        url = self.ep(f'people/{person_id}/features/applications')
        super().put(url=url, params=params, json=body)
        return

    def getpersons_privacy(self, person_id: str, org_id: str = None) -> GetpersonsPrivacySettingsResponse:
        """
        Get a person's privacy settings for the specified person ID.
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by Auto Attendant services.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by Auto Attendant services.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param aa_extension_dialing_enabled: When true auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When true auto attendant dailing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When true phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if aa_extension_dialing_enabled is not None:
            body['aaExtensionDialingEnabled'] = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body['aaNamingDialingEnabled'] = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body['enablePhoneStatusDirectoryPrivacy'] = enable_phone_status_directory_privacy
        if monitoring_agents is not None:
            body['monitoringAgents'] = monitoring_agents
        url = self.ep(f'people/{person_id}/features/privacy')
        super().put(url=url, params=params, json=body)
        return

    def retrieve_executive_assistant_for_person(self, person_id: str, org_id: str = None) -> enum:
        """
        Retrieve the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the call forward destination and join or leave an executive's pool.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        data = super().get(url=url, params=params)
        return data["type"]

    def modify_executive_assistant_for_person(self, person_id: str, org_id: str = None, type_: enum = None):
        """
        Modify the executive assistant settings for the specified personId.
        People with the executive service enabled, can select from a pool of assistants who have been assigned the executive assistant service and who can answer or place calls on their behalf. Executive assistants can set the call forward destination and join or leave an executive's pool.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param type_: executive assistant type
        :type type_: enum
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if type_ is not None:
            body['type'] = type_
        url = self.ep(f'people/{person_id}/features/executiveAssistant')
        super().put(url=url, params=params, json=body)
        return

    def read_receptionist_client_for_person(self, person_id: str, org_id: str = None) -> ReadReceptionistClientSettingsForPersonResponse:
        """
        Retrieve a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people or workspaces as telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/reception')
        data = super().get(url=url, params=params)
        return ReadReceptionistClientSettingsForPersonResponse.parse_obj(data)

    def configure_receptionist_client_for_person(self, person_id: str, org_id: str = None, reception_enabled: bool, monitored_members: List[str] = None):
        """
        Configure a person's Receptionist Client settings.
        To help support the needs of your front-office personnel, you can set up people or workspaces as telephone attendants so that they can screen all incoming calls to certain numbers within your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param reception_enabled: true if the Receptionist Client feature is enabled.
        :type reception_enabled: bool
        :param monitored_members: List of members' unique identifiers to monitor.
Possible values: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
        :type monitored_members: List[str]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if reception_enabled is not None:
            body['receptionEnabled'] = reception_enabled
        if monitored_members is not None:
            body['monitoredMembers'] = monitored_members
        url = self.ep(f'people/{person_id}/features/reception')
        super().put(url=url, params=params, json=body)
        return

    def read_push_to_talk_for_person(self, person_id: str, org_id: str = None) -> ReadPushtoTalkSettingsForPersonResponse:
        """
        Retrieve a person's Push-to-Talk settings.
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in different parts of your organization.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in different parts of your organization.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
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
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if allow_auto_answer is not None:
            body['allowAutoAnswer'] = allow_auto_answer
        if connection_type is not None:
            body['connectionType'] = connection_type
        if access_type is not None:
            body['accessType'] = access_type
        if members is not None:
            body['members'] = members
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        super().put(url=url, params=params, json=body)
        return

    def read_hoteling_for_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Retrieve a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features, and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/hoteling')
        data = super().get(url=url, params=params)
        return data["enabled"]

    def configure_hoteling_for_person(self, person_id: str, org_id: str = None, enabled: bool):
        """
        Configure a person's hoteling settings.
        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features, and calling plan) is temporarily loaded onto a shared (host) phone.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'people/{person_id}/features/hoteling')
        super().put(url=url, params=params, json=body)
        return

    def reset_voicemail_pin(self, person_id: str, org_id: str = None):
        """
        Reset a voicemail PIN for a person.
        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice messages via Voicemail.  A voicemail PIN is used to retrieve your voicemail messages.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.
        NOTE: This API is expected to have an empty request body and Content-Type header should be set to application/json.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
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
        You can change the incoming calling permissions for a person if you want them to be different from your organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        data = super().get(url=url, params=params)
        return ReadIncomingPermissionSettingsForPersonResponse.parse_obj(data)

    def configure_incoming_permission_for_person(self, person_id: str, org_id: str = None, use_custom_enabled: bool, external_transfer: enum, internal_calls_enabled: bool, collect_calls_enabled: bool):
        """
        Configure a person's Incoming Permission settings.
        You can change the incoming calling permissions for a person if you want them to be different from your organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather than the organizational defaults.
        :type use_custom_enabled: bool
        :param external_transfer: Specifies the transfer behavior for incoming, external calls.
        :type external_transfer: enum
        :param internal_calls_enabled: Internal calls are allowed to be received.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Collect calls are allowed to be received.
        :type collect_calls_enabled: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if external_transfer is not None:
            body['externalTransfer'] = external_transfer
        if internal_calls_enabled is not None:
            body['internalCallsEnabled'] = internal_calls_enabled
        if collect_calls_enabled is not None:
            body['collectCallsEnabled'] = collect_calls_enabled
        url = self.ep(f'people/{person_id}/features/incomingPermission')
        super().put(url=url, params=params, json=body)
        return

    def retrievepersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None) -> RetrievepersonsOutgoingCallingPermissionsSettingsResponse:
        """
        Retrieve a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your organization's default.
        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        data = super().get(url=url, params=params)
        return RetrievepersonsOutgoingCallingPermissionsSettingsResponse.parse_obj(data)

    def modifypersons_outgoing_calling_permissions(self, person_id: str, org_id: str = None, use_custom_enabled: bool, calling_permissions: List[object]):
        """
        Modify a person's Outgoing Calling Permissions settings.
        You can change the outgoing calling permissions for a person if you want them to be different from your organization's default.
        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization (such as partners) may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param use_custom_enabled: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
        :type use_custom_enabled: bool
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: List[object]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if calling_permissions is not None:
            body['callingPermissions'] = calling_permissions
        url = self.ep(f'people/{person_id}/features/outgoingPermission')
        super().put(url=url, params=params, json=body)
        return

    def assign_or_unassign_numbers_toperson(self, person_id: str, org_id: str = None, phone_numbers: List[PhoneNumber], enable_distinctive_ring_pattern: bool = None):
        """
        Assign or unassign alternate phone numbers to a person.
        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers must follow the E.164 format for all countries, except for the United States, which can also follow the National format. Active phone numbers are in service.
        Assigning or unassigning an alternate phone number to a person requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param person_id: Unique identitfier of the person.
        :type person_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :param phone_numbers: List of phone numbers that are assigned to a person.
        :type phone_numbers: List[PhoneNumber]
        :param enable_distinctive_ring_pattern: Enables a distinctive ring pattern for the person.
        :type enable_distinctive_ring_pattern: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if enable_distinctive_ring_pattern is not None:
            body['enableDistinctiveRingPattern'] = enable_distinctive_ring_pattern
        url = self.ep(f'telephony/config/people/{person_id}/numbers')
        super().put(url=url, params=params, json=body)
        return

    def retrieve_list_of_call_queue_caller_id_information(self, person_id: str) -> List[CallQueueObject]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information.
        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for outgoing Caller ID.  This API returns a list of Call Queues from which the person must select.  If this setting is disabled or the Agent does not belong to any queue, this list will be empty.
        This API requires a full admin or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/availableCallerIds')
        data = super().get(url=url)
        return data["availableQueues"]

    def retrieve_call_queue_agents_caller_id_information(self, person_id: str) -> RetrieveCallQueueAgentsCallerIDInformationResponse:
        """
        Retrieve a call queue agent's Caller ID information.
        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the system.
        This API requires a full admin or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        data = super().get(url=url)
        return RetrieveCallQueueAgentsCallerIDInformationResponse.parse_obj(data)

    def modify_call_queue_agents_caller_id_information(self, person_id: str, queue_caller_id_enabled: bool, selected_queue: object):
        """
        Modify a call queue agent's Caller ID information.
        Each Agent in the Call Queue will be able to set their outgoing Caller ID as either the designated Call Queue's phone number or their own configured Caller ID. This API modifies the configured Caller ID for the agent in the system.
        This API requires a full or user administrator auth token with the spark-admin:telephony_config_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param queue_caller_id_enabled: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that it is using the agent's configured Caller ID.
        :type queue_caller_id_enabled: bool
        :param selected_queue: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be populated.
        :type selected_queue: object
        """
        body = {}
        if queue_caller_id_enabled is not None:
            body['queueCallerIdEnabled'] = queue_caller_id_enabled
        if selected_queue is not None:
            body['selectedQueue'] = selected_queue
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        super().put(url=url, json=body)
        return

class VoiceMessageDetails(ApiModel):
    #: The message identifier of the voicemail message.
    id: Optional[str]
    #:  The duration (in seconds) of the voicemail message.  Duration is not present for a FAX message.
    duration: Optional[int]
    #: The calling party's details. For example, if user A calls user B and leaves a voicemail message, then A is the calling party.
    calling_party: Optional[VoiceMailPartyInformation]
    #: true if the voicemail message is urgent.
    urgent: Optional[bool]
    #: true if the voicemail message is confidential.
    confidential: Optional[bool]
    #: true if the voicemail message has been read.
    read: Optional[bool]
    #: Number of pages for the FAX.  Only set for a FAX.
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
    #: The voicemail message identifier of the message to mark as read.  If the messageId is not provided, then all voicemail messages for the user are marked as read.
    message_id: Optional[str]


class MarkAsUnreadBody(ApiModel):
    #: The voicemail message identifier of the message to mark as unread.  If the messageId is not provided, then all voicemail messages for the user are marked as unread.
    message_id: Optional[str]


class WebexCallingVoiceMessagingApi(ApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling.  The APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while the other commands require the spark:calls_write scope.
    """

    def summary(self) -> GetMessageSummaryResponse:
        """
        Get a summary of the voicemail messages for the user.
        """
        url = self.ep('summary')
        data = super().get(url=url)
        return GetMessageSummaryResponse.parse_obj(data)

    def list(self) -> Generator[VoiceMessageDetails, None, None]:
        """
        Get the list of all voicemail messages for the user.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoiceMessageDetails, params=params)

    def delete(self, message_id: str):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        super().delete(url=url)
        return

    def mark_as_read(self, message_id: str = None):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read.  Otherwise, all messages for the user are marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the messageId is not provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        """
        body = {}
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('markAsRead')
        super().post(url=url, json=body)
        return

    def mark_as_unread(self, message_id: str = None):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread.  Otherwise, all messages for the user are marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the messageId is not provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        """
        body = {}
        if message_id is not None:
            body['messageId'] = message_id
        url = self.ep('markAsUnread')
        super().post(url=url, json=body)
        return
