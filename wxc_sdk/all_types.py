from wxc_sdk.admin_audit import AuditEvent, AuditEventData
from wxc_sdk.attachment_actions import AttachmentAction, AttachmentActionData
from wxc_sdk.authorizations import Authorization, AuthorizationType
from wxc_sdk.base import ApiModel, ApiModelWithErrors, CodeAndReason, RETRY_429_MAX_WAIT, SafeEnum, StrOrDict, \
    dt_iso_str, enum_str, plus1, to_camel, webex_id_to_uuid
from wxc_sdk.cdr import CDR, CDRCallType, CDRClientType, CDRDirection, CDROriginalReason, CDRRedirectReason, \
    CDRRelatedReason, CDRUserType
from wxc_sdk.common import AcdCustomization, AlternateNumber, AnnAudioFile, AnnouncementLevel, \
    ApplyLineKeyTemplateAction, AssignedDectNetwork, AtaCustomization, AtaDtmfMethod, AtaDtmfMode, \
    AudioCodecPriority, AuthCode, AuthCodeLevel, Background, BackgroundImageColor, BackgroundSelection, \
    BacklightTimer, BacklightTimer68XX78XX, BluetoothMode, BluetoothSetting, CallForwardExpandedSoftKey, \
    CallHistoryMethod, CallParkExtension, CommonDeviceCustomization, Customer, DectCustomization, \
    DeviceCustomization, DeviceCustomizations, DevicePlatform, DialPatternStatus, DialPatternValidate, \
    DirectoryMethod, DisplayCallqueueAgentSoftkey, DisplayNameSelection, EnabledAndValue, Greeting, HttpProxy, \
    HttpProxyMode, IdAndName, IdOnly, LineKeyLabelSelection, LineKeyLedPattern, LinkRelation, LoggingLevel, \
    MediaFileType, MonitoredMember, MppCustomization, MppVlanDevice, NoiseCancellation, NumberOwner, NumberState, \
    OwnerType, PatternAction, PersonPlaceAgent, PhoneLanguage, PrimaryOrShared, PskObject, RingPattern, RoomType, \
    RouteIdentity, RouteType, SoftKeyLayout, SoftKeyMenu, StorageType, UsbPortsObject, UserBase, UserNumber, \
    UserType, ValidateExtensionStatus, ValidateExtensionStatusState, ValidateExtensionsResponse, \
    ValidatePhoneNumberStatus, ValidatePhoneNumberStatusState, ValidatePhoneNumbersResponse, ValidationStatus, \
    VlanSetting, VoicemailCopyOfMessage, VoicemailEnabled, VoicemailFax, VoicemailMessageStorage, \
    VoicemailNotifications, VoicemailTransferToNumber, VolumeSettings, WifiAuthenticationMethod, \
    WifiCustomization, WifiNetwork
from wxc_sdk.common.schedules import Event, RecurWeekly, RecurYearlyByDate, RecurYearlyByDay, Recurrence, \
    Schedule, ScheduleApiBase, ScheduleDay, ScheduleMonth, ScheduleType, ScheduleTypeOrStr, ScheduleWeek
from wxc_sdk.converged_recordings import ConvergedRecording, ConvergedRecordingMeta, \
    ConvergedRecordingWithDirectDownloadLinks, RecordingOwnerType, RecordingParty, RecordingPartyActor, \
    RecordingServiceData, RecordingSession, RecordingStorageRegion, TemporaryDirectDownloadLink
from wxc_sdk.device_configurations import DeviceConfiguration, DeviceConfigurationOperation, \
    DeviceConfigurationResponse, DeviceConfigurationSource, DeviceConfigurationSourceEditability, \
    DeviceConfigurationSources
from wxc_sdk.devices import ActivationCodeResponse, ConnectionStatus, Device, ProductType, TagOp
from wxc_sdk.events import ComplianceEvent, EventData, EventResource, EventType
from wxc_sdk.groups import Group, GroupMember
from wxc_sdk.guests import Guest
from wxc_sdk.licenses import License, LicenseProperties, LicenseRequest, LicenseRequestOperation, LicenseUser, \
    LicenseUserType, SiteAccountType, SiteResponse, SiteType, SiteUrlsRequest, UserLicensesResponse
from wxc_sdk.locations import Floor, Location, LocationAddress
from wxc_sdk.meetings import AnswerCondition, ApprovalQuestion, ApprovalRule, AttendeePrivileges, \
    AudioConnectionOptions, AudioConnectionType, AutoRegistrationResult, BreakoutSession, CallInNumbers, \
    CreateMeetingBody, CustomizedQuestionForCreateMeeting, EntryAndExitTone, GetMeetingSurveyResponse, InputMode, \
    InterpreterForSimultaneousInterpretation, InviteeForCreateMeeting, JoinMeetingBody, JoinMeetingResponse, \
    Meeting, MeetingOptions, MeetingService, MeetingState, MeetingTelephony, MeetingType, NoteType, \
    PatchMeetingBody, PatchMeetingResponse, Question, QuestionAnswer, QuestionOption, QuestionType, \
    QuestionWithAnswers, Registration, ScheduledMeeting, ScheduledType, SimultaneousInterpretation, \
    StandardRegistrationApproveRule, SurveyResult, TrackingCode, TrackingCodeItem, TrackingCodeOption, \
    TrackingCodeType, Type, UnlockedMeetingJoinSecurity
from wxc_sdk.meetings.chats import ChatObject, Sender
from wxc_sdk.meetings.closed_captions import CCSnippet, ClosedCaption
from wxc_sdk.meetings.invitees import CreateInviteesItem, CreateMeetingInviteeBody, CreateMeetingInviteesBody, \
    Invitee, UpdateMeetingInviteeBody
from wxc_sdk.meetings.participants import AdmitParticipantsBody, AudioType, InProgressDevice, MeetingCallType, \
    MeetingDevice, Participant, ParticipantState, QueryMeetingParticipantsWithEmailBody, UpdateParticipantBody, \
    UpdateParticipantResponse, VideoState
from wxc_sdk.meetings.preferences import Audio, CallInNumber, CoHost, DefaultAudioType, MeetingPreferenceDetails, \
    MeetingsSite, OfficeNumber, PersonalMeetingRoom, PersonalMeetingRoomOptions, SchedulingOptions, Telephony, \
    UpdateDefaultSiteBody, UpdatePersonalMeetingRoomOptionsBody, Video, VideoDevice, VideoOptions
from wxc_sdk.meetings.qanda import AnswerObject, Answers, QAObject
from wxc_sdk.meetings.qualities import MediaSessionQuality, NetworkType, QualityResources, TransportType, VideoIn
from wxc_sdk.meetings.recordings import Recording, RecordingFormat, RecordingServiceType, RecordingStatus
from wxc_sdk.meetings.transcripts import DeleteTranscriptBody, Transcript, TranscriptSnippet, TranscriptStatus, \
    UpdateTranscriptSnippetBody
from wxc_sdk.memberships import Membership, MembershipsData
from wxc_sdk.messages import AdaptiveCard, AdaptiveCardAction, AdaptiveCardBody, Message, MessageAttachment, \
    MessagesData
from wxc_sdk.organizations import Organization
from wxc_sdk.people import PeopleStatus, Person, PersonAddress, PersonType, PhoneNumber, PhoneNumberType, \
    SipAddress, SipType
from wxc_sdk.person_settings import DeviceActivationState, DeviceOwner, Hoteling, PersonDevicesResponse, \
    TelephonyDevice
from wxc_sdk.person_settings.agent_caller_id import AgentQueue, QueueCallerId
from wxc_sdk.person_settings.appservices import AppServicesSettings
from wxc_sdk.person_settings.barge import BargeSettings
from wxc_sdk.person_settings.call_intercept import InterceptAnnouncements, InterceptNumber, InterceptSetting, \
    InterceptSettingIncoming, InterceptSettingOutgoing, InterceptTypeIncoming, InterceptTypeOutgoing
from wxc_sdk.person_settings.call_recording import CallRecordingSetting, Notification, NotificationRepeat, \
    NotificationType, Record, StartStopAnnouncement
from wxc_sdk.person_settings.callbridge import CallBridgeSetting
from wxc_sdk.person_settings.caller_id import CallerId, CallerIdSelectedType, ExternalCallerIdNamePolicy
from wxc_sdk.person_settings.calling_behavior import BehaviorType, CallingBehavior
from wxc_sdk.person_settings.common import ApiSelector, PersonSettingsApiChild
from wxc_sdk.person_settings.dnd import DND
from wxc_sdk.person_settings.exec_assistant import ExecAssistantType, _Helper
from wxc_sdk.person_settings.forwarding import CallForwardingAlways, CallForwardingCommon, CallForwardingNoAnswer, \
    CallForwardingPerson, PersonForwardingSetting
from wxc_sdk.person_settings.monitoring import MonitoredElement, MonitoredElementMember, Monitoring
from wxc_sdk.person_settings.numbers import PersonNumbers, PersonPhoneNumber, UpdatePersonNumbers, \
    UpdatePersonPhoneNumber
from wxc_sdk.person_settings.permissions_in import ExternalTransfer, IncomingPermissions
from wxc_sdk.person_settings.permissions_out import Action, AuthCodes, AutoTransferNumbers, CallTypePermission, \
    CallingPermissions, DigitPattern, DigitPatterns, OutgoingPermissionCallType, OutgoingPermissions
from wxc_sdk.person_settings.preferred_answer import PreferredAnswerEndpoint, PreferredAnswerEndpointType, \
    PreferredAnswerResponse
from wxc_sdk.person_settings.privacy import Privacy
from wxc_sdk.person_settings.push_to_talk import PTTConnectionType, PushToTalkAccessType, PushToTalkSettings
from wxc_sdk.person_settings.receptionist import ReceptionistSettings
from wxc_sdk.person_settings.voicemail import UnansweredCalls, VoicemailEnabledWithGreeting, VoicemailSettings
from wxc_sdk.reports import CallingCDR, Report, ReportTemplate, ValidationRules
from wxc_sdk.room_tabs import RoomTab
from wxc_sdk.rooms import GetRoomMeetingDetailsResponse, Room
from wxc_sdk.scim.bulk import BulkErrorResponse, BulkMethod, BulkOperation, BulkResponse, BulkResponseOperation, \
    ResponseError
from wxc_sdk.scim.groups import GroupMemberObject, GroupMemberResponse, GroupMeta, ManagedBy, \
    MetaObjectResourceType, ScimGroup, ScimGroupMember, SearchGroupResponse, WebexGroup, WebexGroupMeta, \
    WebexGroupOwner
from wxc_sdk.scim.users import EmailObject, EmailObjectType, EnterpriseUser, ManagedOrg, ManagerObject, \
    NameObject, PatchUserOperation, PatchUserOperationOp, PhotoObject, PhotoObjectType, ScimPhoneNumberType, \
    ScimUser, SearchUserResponse, SipAddressObject, UserAddress, UserManager, UserPhoneNumber, UserTypeObject, \
    WebexUser
from wxc_sdk.status import Component, Incident, IncidentUpdate, StatusAPI, StatusSummary, WebexStatus
from wxc_sdk.team_memberships import TeamMembership
from wxc_sdk.teams import Team
from wxc_sdk.telephony import AnnouncementLanguage, AppliedService, AppliedServiceTranslationPattern, \
    CallInterceptDetails, CallInterceptDetailsPermission, CallSourceInfo, CallSourceType, CallingPlanReason, \
    ConfigurationLevel, DestinationType, DeviceManagedBy, DeviceManufacturer, DeviceSettingsConfiguration, \
    DeviceType, EmergencyDestination, FeatureAccessCodeDestination, HostedFeatureDestination, \
    HostedUserDestination, LocationAndNumbers, NumberDetails, NumberListPhoneNumber, NumberListPhoneNumberType, \
    NumberType, OnboardingMethod, OriginatorType, OutgoingCallingPlanPermissionsByDigitPattern, \
    OutgoingCallingPlanPermissionsByType, PbxUserDestination, PstnNumberDestination, RouteListDestination, \
    ServiceType, SupportedDevice, SupportedDevices, TelephonyType, TestCallRoutingResult, \
    TranslationPatternConfigurationLevel, TrunkDestination, UCMProfile, VirtualExtensionDestination
from wxc_sdk.telephony.announcements_repo import FeatureReference, RepoAnnouncement, RepositoryUsage
from wxc_sdk.telephony.autoattendant import AutoAttendant, AutoAttendantAction, AutoAttendantKeyConfiguration, \
    AutoAttendantMenu, Dialing, MenuKey
from wxc_sdk.telephony.call_recording import CallRecordingInfo, CallRecordingTermsOfService, \
    LocationComplianceAnnouncement, OrgComplianceAnnouncement
from wxc_sdk.telephony.call_routing.translation_pattern import TranslationPattern, TranslationPatternLevel
from wxc_sdk.telephony.callpark import AvailableRecallHuntGroup, CallPark, CallParkRecall, CallParkSettings, \
    LocationCallParkSettings, RecallHuntGroup
from wxc_sdk.telephony.callpickup import CallPickup, PickupNotificationType
from wxc_sdk.telephony.callqueue import AudioSource, CQRoutingType, CallBounce, CallQueue, CallQueueCallPolicies, \
    ComfortMessageBypass, ComfortMessageSetting, DistinctiveRing, MohMessageSetting, OverflowAction, \
    OverflowSetting, QueueSettings, WaitMessageSetting, WaitMode, WelcomeMessageSetting
from wxc_sdk.telephony.callqueue.announcement import Announcement
from wxc_sdk.telephony.callqueue.policies import AnnouncementMode, CPActionType, CQHolidaySchedule, ForcedForward, \
    HolidayService, NightService, ScheduleLevel, StrandedCalls, StrandedCallsAction
from wxc_sdk.telephony.calls import CallHistoryRecord, CallInfo, CallState, CallType, DialResponse, HistoryType, \
    ParkedAgainst, Personality, Recall, RecordingState, RedirectReason, Redirection, RejectAction, TelephonyCall, \
    TelephonyEvent, TelephonyEventData, TelephonyParty
from wxc_sdk.telephony.conference import ConferenceDetails, ConferenceParticipant, ConferenceState, \
    ConferenceTypeEnum
from wxc_sdk.telephony.dect_devices import BaseStationDetail, BaseStationResponse, BaseStationResult, \
    BaseStationsResponse, DECTHandsetItem, DECTHandsetLine, DECTHandsetList, DECTNetworkDetail, DECTNetworkModel, \
    Handset, UsageType
from wxc_sdk.telephony.devices import ActivationState, AvailableMember, DectDevice, DeviceLayout, DeviceMember, \
    DeviceMembersResponse, DeviceSettings, KemKey, KemModuleType, LayoutMode, LineKeyTemplate, LineKeyType, \
    MACState, MACStatus, MACValidationResponse, MemberCommon, ProgrammableLineKey, TelephonyDeviceDetails, \
    TelephonyDeviceOwner, TelephonyDeviceProxy
from wxc_sdk.telephony.forwarding import CallForwarding, CallForwardingNumber, CallForwardingNumberType, \
    CallsFrom, CustomNumbers, FeatureSelector, ForwardCallsTo, ForwardToSelection, ForwardingRule, \
    ForwardingRuleDetails, ForwardingSetting
from wxc_sdk.telephony.hg_and_cq import Agent, AlternateNumberSettings, CallingLineIdPolicy, HGandCQ, Policy
from wxc_sdk.telephony.huntgroup import BusinessContinuity, HGCallPolicies, HuntGroup, NoAnswer
from wxc_sdk.telephony.jobs import ApplyLineKeyTemplateJobDetails, ErrorMessageObject, ErrorObject, \
    InitiateMoveNumberJobsBody, JobError, JobErrorItem, JobErrorMessage, JobExecutionStatus, \
    LineKeyTemplateAdvisoryTypes, ManageNumberErrorItem, MoveNumberCounts, NumberItem, NumberJob, \
    RoutingPrefixCounts, StartJobResponse, StepExecutionStatus
from wxc_sdk.telephony.location import CallingLineId, PSTNConnection, TelephonyLocation
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.location.moh import LocationMoHGreetingType, LocationMoHSetting
from wxc_sdk.telephony.location.numbers import TelephoneNumberType
from wxc_sdk.telephony.location.vm import LocationVoiceMailSettings
from wxc_sdk.telephony.organisation_vm import OrganisationVoicemailSettings, OrganisationVoicemailSettingsAPI
from wxc_sdk.telephony.paging import Paging, PagingAgent
from wxc_sdk.telephony.playlists import PlayList, PlaylistAnnouncement
from wxc_sdk.telephony.pnc import NetworkConnectionType
from wxc_sdk.telephony.prem_pstn import DialPatternValidationResult
from wxc_sdk.telephony.prem_pstn.dial_plan import CreateResponse, DialPlan, PatternAndAction
from wxc_sdk.telephony.prem_pstn.route_group import RGTrunk, RouteGroup, RouteGroupUsage, UsageRouteLists
from wxc_sdk.telephony.prem_pstn.route_list import NumberAndAction, RouteList, RouteListDetail, \
    UpdateNumbersResponse
from wxc_sdk.telephony.prem_pstn.trunk import CnameRecord, DeviceStatus, OutboundProxy, ResponseStatus, \
    ResponseStatusType, Trunk, TrunkDetail, TrunkDeviceType, TrunkType, TrunkTypeWithDeviceType, TrunkUsage
from wxc_sdk.telephony.virtual_line import VirtualLine, VirtualLineDevices, VirtualLineLocation, \
    VirtualLineNumber, VirtualLineNumberPhoneNumber
from wxc_sdk.telephony.vm_rules import BlockContiguousSequences, BlockPreviousPasscodes, BlockRepeatedDigits, \
    DefaultVoicemailPinRules, EnabledAndNumberOfDays, PinLength, VoiceMailRules
from wxc_sdk.telephony.voice_messaging import MessageSummary, VoiceMailPartyInformation, VoiceMessageDetails
from wxc_sdk.telephony.voicemail_groups import VoicemailGroup, VoicemailGroupDetail
from wxc_sdk.telephony.voiceportal import ExpirePasscode, FailedAttempts, PasscodeRules, VoicePortalSettings
from wxc_sdk.tokens import Tokens
from wxc_sdk.webhook import Webhook, WebhookCreate, WebhookEvent, WebhookEventData, WebhookEventType, \
    WebhookResource, WebhookStatus
from wxc_sdk.workspace_locations import WorkspaceLocation, WorkspaceLocationFloor
from wxc_sdk.workspace_personalization import WorkspacePersonalizationTaskResponse
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers
from wxc_sdk.workspaces import Calendar, CalendarType, CallingType, CapabilityMap, HotdeskingStatus, \
    WorkSpaceType, Workspace, WorkspaceCalling, WorkspaceCallingHybridCalling, WorkspaceEmail, \
    WorkspaceIndoorNavigation, WorkspaceSupportedDevices, WorkspaceWebexCalling

__all__ = ['AcdCustomization', 'Action', 'ActivationCodeResponse', 'ActivationState', 'AdaptiveCard',
           'AdaptiveCardAction', 'AdaptiveCardBody', 'AdmitParticipantsBody', 'Agent', 'AgentQueue',
           'AlternateNumber', 'AlternateNumberSettings', 'AnnAudioFile', 'Announcement', 'AnnouncementLanguage',
           'AnnouncementLevel', 'AnnouncementMode', 'AnswerCondition', 'AnswerObject', 'Answers', 'ApiModel',
           'ApiModelWithErrors', 'ApiSelector', 'AppServicesSettings', 'AppliedService',
           'AppliedServiceTranslationPattern', 'ApplyLineKeyTemplateAction', 'ApplyLineKeyTemplateJobDetails',
           'ApprovalQuestion', 'ApprovalRule', 'AssignedDectNetwork', 'AtaCustomization', 'AtaDtmfMethod',
           'AtaDtmfMode', 'AttachmentAction', 'AttachmentActionData', 'AttendeePrivileges', 'Audio',
           'AudioCodecPriority', 'AudioConnectionOptions', 'AudioConnectionType', 'AudioSource', 'AudioType',
           'AuditEvent', 'AuditEventData', 'AuthCode', 'AuthCodeLevel', 'AuthCodes', 'Authorization',
           'AuthorizationType', 'AutoAttendant', 'AutoAttendantAction', 'AutoAttendantKeyConfiguration',
           'AutoAttendantMenu', 'AutoRegistrationResult', 'AutoTransferNumbers', 'AvailableMember',
           'AvailableRecallHuntGroup', 'Background', 'BackgroundImageColor', 'BackgroundSelection', 'BacklightTimer',
           'BacklightTimer68XX78XX', 'BargeSettings', 'BaseStationDetail', 'BaseStationResponse', 'BaseStationResult',
           'BaseStationsResponse', 'BehaviorType', 'BlockContiguousSequences', 'BlockPreviousPasscodes',
           'BlockRepeatedDigits', 'BluetoothMode', 'BluetoothSetting', 'BreakoutSession', 'BulkErrorResponse',
           'BulkMethod', 'BulkOperation', 'BulkResponse', 'BulkResponseOperation', 'BusinessContinuity', 'CCSnippet',
           'CDR', 'CDRCallType', 'CDRClientType', 'CDRDirection', 'CDROriginalReason', 'CDRRedirectReason',
           'CDRRelatedReason', 'CDRUserType', 'CPActionType', 'CQHolidaySchedule', 'CQRoutingType', 'Calendar',
           'CalendarType', 'CallBounce', 'CallBridgeSetting', 'CallForwardExpandedSoftKey', 'CallForwarding',
           'CallForwardingAlways', 'CallForwardingCommon', 'CallForwardingNoAnswer', 'CallForwardingNumber',
           'CallForwardingNumberType', 'CallForwardingPerson', 'CallHistoryMethod', 'CallHistoryRecord',
           'CallInNumber', 'CallInNumbers', 'CallInfo', 'CallInterceptDetails', 'CallInterceptDetailsPermission',
           'CallPark', 'CallParkExtension', 'CallParkRecall', 'CallParkSettings', 'CallPickup', 'CallQueue',
           'CallQueueCallPolicies', 'CallRecordingInfo', 'CallRecordingSetting', 'CallRecordingTermsOfService',
           'CallSourceInfo', 'CallSourceType', 'CallState', 'CallType', 'CallTypePermission', 'CallerId',
           'CallerIdSelectedType', 'CallingBehavior', 'CallingCDR', 'CallingLineId', 'CallingLineIdPolicy',
           'CallingPermissions', 'CallingPlanReason', 'CallingType', 'CallsFrom', 'CapabilityMap', 'ChatObject',
           'ClosedCaption', 'CnameRecord', 'CoHost', 'CodeAndReason', 'ComfortMessageBypass', 'ComfortMessageSetting',
           'CommonDeviceCustomization', 'ComplianceEvent', 'Component', 'ConferenceDetails', 'ConferenceParticipant',
           'ConferenceState', 'ConferenceTypeEnum', 'ConfigurationLevel', 'ConnectionStatus', 'ConvergedRecording',
           'ConvergedRecordingMeta', 'ConvergedRecordingWithDirectDownloadLinks', 'CreateInviteesItem',
           'CreateMeetingBody', 'CreateMeetingInviteeBody', 'CreateMeetingInviteesBody', 'CreateResponse',
           'CustomNumbers', 'Customer', 'CustomizedQuestionForCreateMeeting', 'DECTHandsetItem', 'DECTHandsetLine',
           'DECTHandsetList', 'DECTNetworkDetail', 'DECTNetworkModel', 'DND', 'DectCustomization', 'DectDevice',
           'DefaultAudioType', 'DefaultVoicemailPinRules', 'DeleteTranscriptBody', 'DestinationType', 'Device',
           'DeviceActivationState', 'DeviceConfiguration', 'DeviceConfigurationOperation',
           'DeviceConfigurationResponse', 'DeviceConfigurationSource', 'DeviceConfigurationSourceEditability',
           'DeviceConfigurationSources', 'DeviceCustomization', 'DeviceCustomizations', 'DeviceLayout',
           'DeviceManagedBy', 'DeviceManufacturer', 'DeviceMember', 'DeviceMembersResponse', 'DeviceOwner',
           'DevicePlatform', 'DeviceSettings', 'DeviceSettingsConfiguration', 'DeviceStatus', 'DeviceType',
           'DialPatternStatus', 'DialPatternValidate', 'DialPatternValidationResult', 'DialPlan', 'DialResponse',
           'Dialing', 'DigitPattern', 'DigitPatterns', 'DirectoryMethod', 'DisplayCallqueueAgentSoftkey',
           'DisplayNameSelection', 'DistinctiveRing', 'EmailObject', 'EmailObjectType', 'EmergencyDestination',
           'EnabledAndNumberOfDays', 'EnabledAndValue', 'EnterpriseUser', 'EntryAndExitTone', 'ErrorMessageObject',
           'ErrorObject', 'Event', 'EventData', 'EventResource', 'EventType', 'ExecAssistantType', 'ExpirePasscode',
           'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'FailedAttempts', 'FeatureAccessCodeDestination',
           'FeatureReference', 'FeatureSelector', 'Floor', 'ForcedForward', 'ForwardCallsTo', 'ForwardToSelection',
           'ForwardingRule', 'ForwardingRuleDetails', 'ForwardingSetting', 'GetMeetingSurveyResponse',
           'GetRoomMeetingDetailsResponse', 'Greeting', 'Group', 'GroupMember', 'GroupMemberObject',
           'GroupMemberResponse', 'GroupMeta', 'Guest', 'HGCallPolicies', 'HGandCQ', 'Handset', 'HistoryType',
           'HolidayService', 'HostedFeatureDestination', 'HostedUserDestination', 'HotdeskingStatus', 'Hoteling',
           'HttpProxy', 'HttpProxyMode', 'HuntGroup', 'IdAndName', 'IdOnly', 'InProgressDevice', 'Incident',
           'IncidentUpdate', 'IncomingPermissions', 'InitiateMoveNumberJobsBody', 'InputMode',
           'InterceptAnnouncements', 'InterceptNumber', 'InterceptSetting', 'InterceptSettingIncoming',
           'InterceptSettingOutgoing', 'InterceptTypeIncoming', 'InterceptTypeOutgoing', 'InternalDialing',
           'InterpreterForSimultaneousInterpretation', 'Invitee', 'InviteeForCreateMeeting', 'JobError',
           'JobErrorItem', 'JobErrorMessage', 'JobExecutionStatus', 'JoinMeetingBody', 'JoinMeetingResponse',
           'KemKey', 'KemModuleType', 'LayoutMode', 'License', 'LicenseProperties', 'LicenseRequest',
           'LicenseRequestOperation', 'LicenseUser', 'LicenseUserType', 'LineKeyLabelSelection', 'LineKeyLedPattern',
           'LineKeyTemplate', 'LineKeyTemplateAdvisoryTypes', 'LineKeyType', 'LinkRelation', 'Location',
           'LocationAddress', 'LocationAndNumbers', 'LocationCallParkSettings', 'LocationComplianceAnnouncement',
           'LocationMoHGreetingType', 'LocationMoHSetting', 'LocationVoiceMailSettings', 'LoggingLevel', 'MACState',
           'MACStatus', 'MACValidationResponse', 'ManageNumberErrorItem', 'ManagedBy', 'ManagedOrg', 'ManagerObject',
           'MediaFileType', 'MediaSessionQuality', 'Meeting', 'MeetingCallType', 'MeetingDevice', 'MeetingOptions',
           'MeetingPreferenceDetails', 'MeetingService', 'MeetingState', 'MeetingTelephony', 'MeetingType',
           'MeetingsSite', 'MemberCommon', 'Membership', 'MembershipsData', 'MenuKey', 'Message', 'MessageAttachment',
           'MessageSummary', 'MessagesData', 'MetaObjectResourceType', 'MohMessageSetting', 'MonitoredElement',
           'MonitoredElementMember', 'MonitoredMember', 'Monitoring', 'MoveNumberCounts', 'MppCustomization',
           'MppVlanDevice', 'NameObject', 'NetworkConnectionType', 'NetworkType', 'NightService', 'NoAnswer',
           'NoiseCancellation', 'NoteType', 'Notification', 'NotificationRepeat', 'NotificationType',
           'NumberAndAction', 'NumberDetails', 'NumberItem', 'NumberJob', 'NumberListPhoneNumber',
           'NumberListPhoneNumberType', 'NumberOwner', 'NumberState', 'NumberType', 'OfficeNumber',
           'OnboardingMethod', 'OrgComplianceAnnouncement', 'OrganisationVoicemailSettings',
           'OrganisationVoicemailSettingsAPI', 'Organization', 'OriginatorType', 'OutboundProxy',
           'OutgoingCallingPlanPermissionsByDigitPattern', 'OutgoingCallingPlanPermissionsByType',
           'OutgoingPermissionCallType', 'OutgoingPermissions', 'OverflowAction', 'OverflowSetting', 'OwnerType',
           'PSTNConnection', 'PTTConnectionType', 'Paging', 'PagingAgent', 'ParkedAgainst', 'Participant',
           'ParticipantState', 'PasscodeRules', 'PatchMeetingBody', 'PatchMeetingResponse', 'PatchUserOperation',
           'PatchUserOperationOp', 'PatternAction', 'PatternAndAction', 'PbxUserDestination', 'PeopleStatus',
           'Person', 'PersonAddress', 'PersonDevicesResponse', 'PersonForwardingSetting', 'PersonNumbers',
           'PersonPhoneNumber', 'PersonPlaceAgent', 'PersonSettingsApiChild', 'PersonType', 'PersonalMeetingRoom',
           'PersonalMeetingRoomOptions', 'Personality', 'PhoneLanguage', 'PhoneNumber', 'PhoneNumberType',
           'PhotoObject', 'PhotoObjectType', 'PickupNotificationType', 'PinLength', 'PlayList',
           'PlaylistAnnouncement', 'Policy', 'PreferredAnswerEndpoint', 'PreferredAnswerEndpointType',
           'PreferredAnswerResponse', 'PrimaryOrShared', 'Privacy', 'ProductType', 'ProgrammableLineKey', 'PskObject',
           'PstnNumberDestination', 'PushToTalkAccessType', 'PushToTalkSettings', 'QAObject', 'QualityResources',
           'QueryMeetingParticipantsWithEmailBody', 'Question', 'QuestionAnswer', 'QuestionOption', 'QuestionType',
           'QuestionWithAnswers', 'QueueCallerId', 'QueueSettings', 'RETRY_429_MAX_WAIT', 'RGTrunk', 'Recall',
           'RecallHuntGroup', 'ReceptionistSettings', 'Record', 'Recording', 'RecordingFormat', 'RecordingOwnerType',
           'RecordingParty', 'RecordingPartyActor', 'RecordingServiceData', 'RecordingServiceType',
           'RecordingSession', 'RecordingState', 'RecordingStatus', 'RecordingStorageRegion', 'RecurWeekly',
           'RecurYearlyByDate', 'RecurYearlyByDay', 'Recurrence', 'RedirectReason', 'Redirection', 'Registration',
           'RejectAction', 'RepoAnnouncement', 'Report', 'ReportTemplate', 'RepositoryUsage', 'ResponseError',
           'ResponseStatus', 'ResponseStatusType', 'RingPattern', 'Room', 'RoomTab', 'RoomType', 'RouteGroup',
           'RouteGroupUsage', 'RouteIdentity', 'RouteList', 'RouteListDestination', 'RouteListDetail', 'RouteType',
           'RoutingPrefixCounts', 'SafeEnum', 'Schedule', 'ScheduleApiBase', 'ScheduleDay', 'ScheduleLevel',
           'ScheduleMonth', 'ScheduleType', 'ScheduleTypeOrStr', 'ScheduleWeek', 'ScheduledMeeting', 'ScheduledType',
           'SchedulingOptions', 'ScimGroup', 'ScimGroupMember', 'ScimPhoneNumberType', 'ScimUser',
           'SearchGroupResponse', 'SearchUserResponse', 'Sender', 'ServiceType', 'SimultaneousInterpretation',
           'SipAddress', 'SipAddressObject', 'SipType', 'SiteAccountType', 'SiteResponse', 'SiteType',
           'SiteUrlsRequest', 'SoftKeyLayout', 'SoftKeyMenu', 'StandardRegistrationApproveRule', 'StartJobResponse',
           'StartStopAnnouncement', 'StatusAPI', 'StatusSummary', 'StepExecutionStatus', 'StorageType', 'StrOrDict',
           'StrandedCalls', 'StrandedCallsAction', 'SupportedDevice', 'SupportedDevices', 'SurveyResult', 'TagOp',
           'Team', 'TeamMembership', 'TelephoneNumberType', 'Telephony', 'TelephonyCall', 'TelephonyDevice',
           'TelephonyDeviceDetails', 'TelephonyDeviceOwner', 'TelephonyDeviceProxy', 'TelephonyEvent',
           'TelephonyEventData', 'TelephonyLocation', 'TelephonyParty', 'TelephonyType',
           'TemporaryDirectDownloadLink', 'TestCallRoutingResult', 'Tokens', 'TrackingCode', 'TrackingCodeItem',
           'TrackingCodeOption', 'TrackingCodeType', 'Transcript', 'TranscriptSnippet', 'TranscriptStatus',
           'TranslationPattern', 'TranslationPatternConfigurationLevel', 'TranslationPatternLevel', 'TransportType',
           'Trunk', 'TrunkDestination', 'TrunkDetail', 'TrunkDeviceType', 'TrunkType', 'TrunkTypeWithDeviceType',
           'TrunkUsage', 'Type', 'UCMProfile', 'UnansweredCalls', 'UnlockedMeetingJoinSecurity',
           'UpdateDefaultSiteBody', 'UpdateMeetingInviteeBody', 'UpdateNumbersResponse', 'UpdateParticipantBody',
           'UpdateParticipantResponse', 'UpdatePersonNumbers', 'UpdatePersonPhoneNumber',
           'UpdatePersonalMeetingRoomOptionsBody', 'UpdateTranscriptSnippetBody', 'UsageRouteLists', 'UsageType',
           'UsbPortsObject', 'UserAddress', 'UserBase', 'UserLicensesResponse', 'UserManager', 'UserNumber',
           'UserPhoneNumber', 'UserType', 'UserTypeObject', 'ValidateExtensionStatus', 'ValidateExtensionStatusState',
           'ValidateExtensionsResponse', 'ValidatePhoneNumberStatus', 'ValidatePhoneNumberStatusState',
           'ValidatePhoneNumbersResponse', 'ValidationRules', 'ValidationStatus', 'Video', 'VideoDevice', 'VideoIn',
           'VideoOptions', 'VideoState', 'VirtualExtensionDestination', 'VirtualLine', 'VirtualLineDevices',
           'VirtualLineLocation', 'VirtualLineNumber', 'VirtualLineNumberPhoneNumber', 'VlanSetting',
           'VoiceMailPartyInformation', 'VoiceMailRules', 'VoiceMessageDetails', 'VoicePortalSettings',
           'VoicemailCopyOfMessage', 'VoicemailEnabled', 'VoicemailEnabledWithGreeting', 'VoicemailFax',
           'VoicemailGroup', 'VoicemailGroupDetail', 'VoicemailMessageStorage', 'VoicemailNotifications',
           'VoicemailSettings', 'VoicemailTransferToNumber', 'VolumeSettings', 'WaitMessageSetting', 'WaitMode',
           'WebexGroup', 'WebexGroupMeta', 'WebexGroupOwner', 'WebexStatus', 'WebexUser', 'Webhook', 'WebhookCreate',
           'WebhookEvent', 'WebhookEventData', 'WebhookEventType', 'WebhookResource', 'WebhookStatus',
           'WelcomeMessageSetting', 'WifiAuthenticationMethod', 'WifiCustomization', 'WifiNetwork', 'WorkSpaceType',
           'Workspace', 'WorkspaceCalling', 'WorkspaceCallingHybridCalling', 'WorkspaceEmail',
           'WorkspaceIndoorNavigation', 'WorkspaceLocation', 'WorkspaceLocationFloor', 'WorkspaceNumbers',
           'WorkspacePersonalizationTaskResponse', 'WorkspaceSupportedDevices', 'WorkspaceWebexCalling', '_Helper',
           'dt_iso_str', 'enum_str', 'plus1', 'to_camel', 'webex_id_to_uuid']
