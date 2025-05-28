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
    DeviceCustomization, DeviceCustomizations, DevicePlatform, DeviceType, DialPatternStatus, DialPatternValidate, \
    DirectoryMethod, DisplayCallqueueAgentSoftkey, DisplayNameSelection, EnabledAndValue, EnhancedMulticast, \
    Greeting, HttpProxy, HttpProxyMode, IdAndName, IdOnly, LineKeyLabelSelection, LineKeyLedPattern, LinkRelation, \
    LoggingLevel, MediaFileType, MonitoredMember, MppCustomization, MppVlanDevice, Multicast, NoiseCancellation, \
    NumberOwner, NumberState, OwnerType, PatternAction, PersonPlaceAgent, PhoneLanguage, PrimaryOrShared, \
    PskObject, RingPattern, RoomType, RouteIdentity, RouteType, SoftKeyLayout, SoftKeyMenu, StorageType, \
    UsbPortsObject, UserBase, UserLicenseType, UserNumber, UserType, ValidateExtensionStatus, \
    ValidateExtensionStatusState, ValidateExtensionsResponse, ValidatePhoneNumberStatus, \
    ValidatePhoneNumberStatusState, ValidatePhoneNumbersResponse, ValidationStatus, VlanSetting, \
    VoicemailCopyOfMessage, VoicemailEnabled, VoicemailFax, VoicemailMessageStorage, VoicemailNotifications, \
    VoicemailTransferToNumber, VolumeSettings, WifiAuthenticationMethod, WifiCustomization, WifiNetwork
from wxc_sdk.common.schedules import Event, RecurWeekly, RecurYearlyByDate, RecurYearlyByDay, Recurrence, \
    Schedule, ScheduleApiBase, ScheduleDay, ScheduleLevel, ScheduleMonth, ScheduleType, ScheduleTypeOrStr, \
    ScheduleWeek
from wxc_sdk.common.selective import SelectiveCrit, SelectiveCriteria, SelectiveFrom, SelectiveScheduleLevel, \
    SelectiveSource
from wxc_sdk.converged_recordings import ConvergedRecording, ConvergedRecordingMeta, \
    ConvergedRecordingWithDirectDownloadLinks, RecordingOwnerType, RecordingParty, RecordingPartyActor, \
    RecordingServiceData, RecordingSession, RecordingStorageRegion, TemporaryDirectDownloadLink
from wxc_sdk.device_configurations import DeviceConfiguration, DeviceConfigurationOperation, \
    DeviceConfigurationResponse, DeviceConfigurationSource, DeviceConfigurationSourceEditability, \
    DeviceConfigurationSources
from wxc_sdk.devices import ActivationCodeResponse, ConnectionStatus, Device, Lifecycle, ProductType, TagOp
from wxc_sdk.events import ComplianceEvent, EventData, EventResource, EventType, Recipient
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
from wxc_sdk.org_contacts import Contact, ContactAddress, ContactEmail, ContactIm, ContactImType, \
    ContactPhoneNumber, ContactSipAddress, EmailType, Meta, PrimaryContactMethod, UpdateContactPhoneNumbers
from wxc_sdk.organizations import Organization
from wxc_sdk.people import PeopleStatus, Person, PersonAddress, PersonType, PhoneNumber, PhoneNumberType, \
    SipAddress, SipType
from wxc_sdk.person_settings import DeviceActivationState, DeviceList, DeviceOwner, Hoteling, TelephonyDevice
from wxc_sdk.person_settings.agent_caller_id import AgentCallerId, AvailableCallerIdType
from wxc_sdk.person_settings.appservices import AppServicesSettings
from wxc_sdk.person_settings.available_numbers import AvailableNumber, AvailablePhoneNumberLicenseType
from wxc_sdk.person_settings.barge import BargeSettings
from wxc_sdk.person_settings.call_intercept import InterceptAnnouncements, InterceptNumber, InterceptSetting, \
    InterceptSettingIncoming, InterceptSettingOutgoing, InterceptTypeIncoming, InterceptTypeOutgoing
from wxc_sdk.person_settings.call_policy import PrivacyOnRedirectedCalls
from wxc_sdk.person_settings.call_recording import CallRecordingSetting, Notification, NotificationRepeat, \
    NotificationType, Record, StartStopAnnouncement
from wxc_sdk.person_settings.callbridge import CallBridgeSetting
from wxc_sdk.person_settings.caller_id import CallerId, CallerIdSelectedType, ExternalCallerIdNamePolicy
from wxc_sdk.person_settings.calling_behavior import BehaviorType, CallingBehavior
from wxc_sdk.person_settings.common import ApiSelector, PersonSettingsApiChild
from wxc_sdk.person_settings.dnd import DND
from wxc_sdk.person_settings.ecbn import ECBNDefault, ECBNDependencies, ECBNEffectiveLevel, \
    ECBNLocationEffectiveLevel, ECBNLocationMember, ECBNQuality, ECBNSelection, PersonECBN, PersonECBNDirectLine, \
    SelectedECBN
from wxc_sdk.person_settings.exec_assistant import ExecAssistantType, _Helper
from wxc_sdk.person_settings.forwarding import CallForwardingAlways, CallForwardingCommon, CallForwardingNoAnswer, \
    CallForwardingPerson, PersonForwardingSetting
from wxc_sdk.person_settings.mode_management import AvailableFeature, ExceptionType, FeatureType, \
    ModeManagementFeature
from wxc_sdk.person_settings.moh import MusicOnHold
from wxc_sdk.person_settings.monitoring import MonitoredElement, MonitoredElementMember, Monitoring
from wxc_sdk.person_settings.msteams import MSTeamsSettings, OrgMSTeamsSettings, SettingsObject
from wxc_sdk.person_settings.numbers import PersonNumbers, PersonPhoneNumber, UpdatePersonNumbers, \
    UpdatePersonPhoneNumber
from wxc_sdk.person_settings.permissions_in import ExternalTransfer, IncomingPermissions
from wxc_sdk.person_settings.permissions_out import Action, AuthCodes, AutoTransferNumbers, CallTypePermission, \
    CallingPermissions, DigitPattern, DigitPatterns, OutgoingPermissionCallType, OutgoingPermissions
from wxc_sdk.person_settings.personal_assistant import PersonalAssistant, PersonalAssistantAlerting, \
    PersonalAssistantPresence
from wxc_sdk.person_settings.preferred_answer import PreferredAnswerEndpoint, PreferredAnswerEndpointType, \
    PreferredAnswerResponse
from wxc_sdk.person_settings.priority_alert import PriorityAlert, PriorityAlertCriteria
from wxc_sdk.person_settings.privacy import Privacy
from wxc_sdk.person_settings.push_to_talk import PTTConnectionType, PushToTalkAccessType, PushToTalkSettings
from wxc_sdk.person_settings.receptionist import ReceptionistSettings
from wxc_sdk.person_settings.selective_accept import SelectiveAccept, SelectiveAcceptCriteria
from wxc_sdk.person_settings.selective_forward import SelectiveForward, SelectiveForwardCriteria
from wxc_sdk.person_settings.selective_reject import SelectiveReject, SelectiveRejectCriteria
from wxc_sdk.person_settings.sequential_ring import SequentialRing, SequentialRingCriteria, SequentialRingNumber
from wxc_sdk.person_settings.sim_ring import SimRing, SimRingCriteria, SimRingNumber
from wxc_sdk.person_settings.voicemail import UnansweredCalls, VoicemailEnabledWithGreeting, VoicemailSettings
from wxc_sdk.reports import CallingCDR, Report, ReportTemplate, ValidationRules
from wxc_sdk.room_tabs import RoomTab
from wxc_sdk.rooms import GetRoomMeetingDetailsResponse, Room
from wxc_sdk.scim.bulk import BulkErrorResponse, BulkMethod, BulkOperation, BulkResponse, BulkResponseOperation, \
    ResponseError
from wxc_sdk.scim.groups import GroupMemberObject, GroupMemberResponse, GroupMeta, ManagedBy, \
    MetaObjectResourceType, ScimGroup, ScimGroupMember, SearchGroupResponse, WebexGroup, WebexGroupMeta, \
    WebexGroupOwner
from wxc_sdk.scim.users import EmailObject, EmailObjectType, EnterpriseUser, ManagedGroup, ManagedOrg, \
    ManagerObject, NameObject, PatchUserOperation, PatchUserOperationOp, PhotoObject, PhotoObjectType, ScimMeta, \
    ScimPhoneNumberType, ScimUser, ScimValueDisplayRef, SearchUserResponse, SipAddressObject, UserAddress, \
    UserManager, UserPhoneNumber, UserTypeObject, WebexUser, WebexUserMeta
from wxc_sdk.status import Component, Incident, IncidentUpdate, StatusAPI, StatusSummary, WebexStatus
from wxc_sdk.team_memberships import TeamMembership
from wxc_sdk.teams import Team
from wxc_sdk.telephony import AnnouncementLanguage, AppliedService, AppliedServiceTranslationPattern, \
    CallInterceptDetails, CallInterceptDetailsPermission, CallSourceInfo, CallSourceType, CallingPlanReason, \
    ConfigurationLevel, DestinationType, DeviceManagedBy, DeviceManufacturer, DeviceSettingsConfiguration, \
    EmergencyDestination, FeatureAccessCodeDestination, HostedFeatureDestination, HostedUserDestination, \
    LocationAndNumbers, MoHConfig, MoHTheme, NumberDetails, NumberListPhoneNumber, NumberListPhoneNumberType, \
    NumberType, OnboardingMethod, OriginatorType, OutgoingCallingPlanPermissionsByDigitPattern, \
    OutgoingCallingPlanPermissionsByType, PbxUserDestination, PstnNumberDestination, RouteListDestination, \
    ServiceType, SupportedDevice, SupportedDevices, SupportsLogCollection, TelephonyType, TestCallRoutingResult, \
    TranslationPatternConfigurationLevel, TrunkDestination, UCMProfile, VirtualExtensionDestination
from wxc_sdk.telephony.announcements_repo import FeatureReference, RepoAnnouncement, RepositoryUsage
from wxc_sdk.telephony.autoattendant import AutoAttendant, AutoAttendantAction, AutoAttendantKeyConfiguration, \
    AutoAttendantMenu, Dialing, MenuKey
from wxc_sdk.telephony.call_recording import CallRecordingInfo, CallRecordingLocationVendors, CallRecordingRegion, \
    CallRecordingTermsOfService, CallRecordingVendors, FailureBehavior, LocationComplianceAnnouncement, \
    OrgComplianceAnnouncement, RecordingUser, RecordingVendor
from wxc_sdk.telephony.call_routing.translation_pattern import TranslationPattern, TranslationPatternLevel
from wxc_sdk.telephony.callpark import AvailableRecallHuntGroup, CallPark, CallParkRecall, CallParkSettings, \
    LocationCallParkSettings, RecallHuntGroup
from wxc_sdk.telephony.callpickup import CallPickup, PickupNotificationType
from wxc_sdk.telephony.callqueue import AudioSource, AvailableAgent, CQRoutingType, CallBounce, CallQueue, \
    CallQueueCallPolicies, CallQueueSettings, ComfortMessageBypass, ComfortMessageSetting, DistinctiveRing, \
    MohMessageSetting, OverflowAction, OverflowSetting, QueueSettings, WaitMessageSetting, WaitMode, \
    WelcomeMessageSetting
from wxc_sdk.telephony.callqueue.agents import AgentCallQueueSetting, CallQueueAgent, CallQueueAgentDetail, \
    CallQueueAgentQueue
from wxc_sdk.telephony.callqueue.announcement import Announcement
from wxc_sdk.telephony.callqueue.policies import AnnouncementMode, CPActionType, CQHolidaySchedule, ForcedForward, \
    HolidayService, NightService, StrandedCalls, StrandedCallsAction
from wxc_sdk.telephony.calls import CallHistoryRecord, CallInfo, CallState, CallType, DialResponse, HistoryType, \
    Personality, Recall, RecallType, RecordingState, RedirectReason, Redirection, RejectAction, TelephonyCall, \
    TelephonyEvent, TelephonyEventData, TelephonyParty
from wxc_sdk.telephony.conference import ConferenceDetails, ConferenceParticipant, ConferenceState, \
    ConferenceTypeEnum
from wxc_sdk.telephony.cx_essentials import ScreenPopConfiguration
from wxc_sdk.telephony.dect_devices import BaseStationDetail, BaseStationResponse, BaseStationResult, \
    BaseStationsResponse, DECTHandsetItem, DECTHandsetLine, DECTHandsetList, DECTNetworkDetail, DECTNetworkModel, \
    DectDevice, Handset, UsageType
from wxc_sdk.telephony.devices import ActivationState, AvailableMember, BackgroundImage, BackgroundImages, \
    DeleteDeviceBackgroundImagesResponse, DeleteImageRequestObject, DeleteImageResponseSuccessObject, \
    DeleteImageResponseSuccessObjectResult, DeviceLayout, DeviceMember, DeviceMembersResponse, DeviceSettings, \
    KemKey, KemModuleType, LayoutMode, LineKeyTemplate, LineKeyType, MACState, MACStatus, MACValidationResponse, \
    MemberCommon, ProgrammableLineKey, TelephonyDeviceDetails, TelephonyDeviceOwner, TelephonyDeviceProxy, \
    UserDeviceCount
from wxc_sdk.telephony.emergency_services import OrgEmergencyCallNotification
from wxc_sdk.telephony.forwarding import CallForwarding, CallForwardingNumber, CallsFrom, CustomNumbers, \
    FeatureSelector, ForwardCallsTo, ForwardFromSelection, ForwardOperatingModes, ForwardOperatingModesException, \
    ForwardTo, ForwardToSelection, ForwardingRule, ForwardingRuleDetails, ForwardingSetting, \
    ModeDefaultForwardToSelection, ModeForward, ModeForwardTo, ModeType
from wxc_sdk.telephony.guest_calling import DestinationMember, GuestCallingSettings
from wxc_sdk.telephony.hg_and_cq import Agent, AlternateNumberSettings, CallingLineIdPolicy, HGandCQ, Policy
from wxc_sdk.telephony.huntgroup import BusinessContinuity, HGCallPolicies, HuntGroup, NoAnswer
from wxc_sdk.telephony.jobs import ApplyLineKeyTemplateJobDetails, CallRecordingJobCounts, CallRecordingJobStatus, \
    ErrorMessageObject, ErrorObject, InitiateMoveNumberJobsBody, JobError, JobErrorItem, JobErrorMessage, \
    JobExecutionStatus, LineKeyTemplateAdvisoryTypes, ManageNumberErrorItem, MoveCounts, MoveNumberCounts, \
    MoveUser, MoveUserJobDetails, MoveUsersList, NumberItem, NumberJob, RoutingPrefixCounts, StartJobResponse, \
    StartMoveUsersJobResponse, StepExecutionStatus
from wxc_sdk.telephony.location import CallBackSelected, CallingLineId, ContactDetails, LocationECBN, \
    LocationECBNLocation, LocationECBNLocationMember, PSTNConnection, TelephonyLocation
from wxc_sdk.telephony.location.emergency_services import LocationCallNotificationOrganization, \
    LocationEmergencyCallNotification
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.location.moh import LocationMoHGreetingType, LocationMoHSetting
from wxc_sdk.telephony.location.numbers import NumberAddError, NumberAddResponse, NumberUsageType, \
    TelephoneNumberType
from wxc_sdk.telephony.location.vm import LocationVoiceMailSettings
from wxc_sdk.telephony.operating_modes import Day, DaySchedule, DifferentHoursDaily, Month, OperatingMode, \
    OperatingModeHoliday, OperatingModeRecurYearlyByDate, OperatingModeRecurYearlyByDay, OperatingModeRecurrence, \
    OperatingModeSchedule, SameHoursDaily, Week
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
from wxc_sdk.telephony.pstn import PSTNConnectionOption, PSTNServiceType, PSTNType
from wxc_sdk.telephony.supervisor import AgentOrSupervisor, IdAndAction, SupervisorAgentStatus
from wxc_sdk.telephony.virtual_extensions import PhoneNumberStatus, ValidatePhoneNumber, \
    ValidateVirtualExtensionRange, ValidateVirtualExtensionStatus, VirtualExtension, VirtualExtensionLevel, \
    VirtualExtensionMode, VirtualExtensionRange, VirtualExtensionRangeAction, \
    VirtualExtensionRangeValidationResult, VirtualExtensionValidationStatus
from wxc_sdk.telephony.virtual_line import VirtualLine, VirtualLineDevices, VirtualLineLocation, \
    VirtualLineNumberPhoneNumber
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
from wxc_sdk.workspace_settings.numbers import UpdateWorkspacePhoneNumber, WorkspaceNumbers
from wxc_sdk.workspaces import Calendar, CalendarType, CallingType, CapabilityMap, DeviceHostedMeetings, \
    HotdeskingStatus, SupportAndConfiguredInfo, WorkSpaceType, Workspace, WorkspaceCalling, \
    WorkspaceCallingHybridCalling, WorkspaceEmail, WorkspaceHealth, WorkspaceHealthIssue, WorkspaceHealthLevel, \
    WorkspaceIndoorNavigation, WorkspaceSupportedDevices, WorkspaceWebexCalling
from wxc_sdk.xapi import ExecuteCommandResponse, QueryStatusResponse

__all__ = ['AcdCustomization', 'Action', 'ActivationCodeResponse', 'ActivationState', 'AdaptiveCard',
           'AdaptiveCardAction', 'AdaptiveCardBody', 'AdmitParticipantsBody', 'Agent', 'AgentCallQueueSetting',
           'AgentCallerId', 'AgentOrSupervisor', 'AlternateNumber', 'AlternateNumberSettings', 'AnnAudioFile',
           'Announcement', 'AnnouncementLanguage', 'AnnouncementLevel', 'AnnouncementMode', 'AnswerCondition',
           'AnswerObject', 'Answers', 'ApiModel', 'ApiModelWithErrors', 'ApiSelector', 'AppServicesSettings',
           'AppliedService', 'AppliedServiceTranslationPattern', 'ApplyLineKeyTemplateAction',
           'ApplyLineKeyTemplateJobDetails', 'ApprovalQuestion', 'ApprovalRule', 'AssignedDectNetwork',
           'AtaCustomization', 'AtaDtmfMethod', 'AtaDtmfMode', 'AttachmentAction', 'AttachmentActionData',
           'AttendeePrivileges', 'Audio', 'AudioCodecPriority', 'AudioConnectionOptions', 'AudioConnectionType',
           'AudioSource', 'AudioType', 'AuditEvent', 'AuditEventData', 'AuthCode', 'AuthCodeLevel', 'AuthCodes',
           'Authorization', 'AuthorizationType', 'AutoAttendant', 'AutoAttendantAction',
           'AutoAttendantKeyConfiguration', 'AutoAttendantMenu', 'AutoRegistrationResult', 'AutoTransferNumbers',
           'AvailableAgent', 'AvailableCallerIdType', 'AvailableFeature', 'AvailableMember', 'AvailableNumber',
           'AvailablePhoneNumberLicenseType', 'AvailableRecallHuntGroup', 'Background', 'BackgroundImage',
           'BackgroundImageColor', 'BackgroundImages', 'BackgroundSelection', 'BacklightTimer',
           'BacklightTimer68XX78XX', 'BargeSettings', 'BaseStationDetail', 'BaseStationResponse', 'BaseStationResult',
           'BaseStationsResponse', 'BehaviorType', 'BlockContiguousSequences', 'BlockPreviousPasscodes',
           'BlockRepeatedDigits', 'BluetoothMode', 'BluetoothSetting', 'BreakoutSession', 'BulkErrorResponse',
           'BulkMethod', 'BulkOperation', 'BulkResponse', 'BulkResponseOperation', 'BusinessContinuity', 'CCSnippet',
           'CDR', 'CDRCallType', 'CDRClientType', 'CDRDirection', 'CDROriginalReason', 'CDRRedirectReason',
           'CDRRelatedReason', 'CDRUserType', 'CPActionType', 'CQHolidaySchedule', 'CQRoutingType', 'Calendar',
           'CalendarType', 'CallBackSelected', 'CallBounce', 'CallBridgeSetting', 'CallForwardExpandedSoftKey',
           'CallForwarding', 'CallForwardingAlways', 'CallForwardingCommon', 'CallForwardingNoAnswer',
           'CallForwardingNumber', 'CallForwardingPerson', 'CallHistoryMethod', 'CallHistoryRecord', 'CallInNumber',
           'CallInNumbers', 'CallInfo', 'CallInterceptDetails', 'CallInterceptDetailsPermission', 'CallPark',
           'CallParkExtension', 'CallParkRecall', 'CallParkSettings', 'CallPickup', 'CallQueue', 'CallQueueAgent',
           'CallQueueAgentDetail', 'CallQueueAgentQueue', 'CallQueueCallPolicies', 'CallQueueSettings',
           'CallRecordingInfo', 'CallRecordingJobCounts', 'CallRecordingJobStatus', 'CallRecordingLocationVendors',
           'CallRecordingRegion', 'CallRecordingSetting', 'CallRecordingTermsOfService', 'CallRecordingVendors',
           'CallSourceInfo', 'CallSourceType', 'CallState', 'CallType', 'CallTypePermission', 'CallerId',
           'CallerIdSelectedType', 'CallingBehavior', 'CallingCDR', 'CallingLineId', 'CallingLineIdPolicy',
           'CallingPermissions', 'CallingPlanReason', 'CallingType', 'CallsFrom', 'CapabilityMap', 'ChatObject',
           'ClosedCaption', 'CnameRecord', 'CoHost', 'CodeAndReason', 'ComfortMessageBypass', 'ComfortMessageSetting',
           'CommonDeviceCustomization', 'ComplianceEvent', 'Component', 'ConferenceDetails', 'ConferenceParticipant',
           'ConferenceState', 'ConferenceTypeEnum', 'ConfigurationLevel', 'ConnectionStatus', 'Contact',
           'ContactAddress', 'ContactDetails', 'ContactEmail', 'ContactIm', 'ContactImType', 'ContactPhoneNumber',
           'ContactSipAddress', 'ConvergedRecording', 'ConvergedRecordingMeta',
           'ConvergedRecordingWithDirectDownloadLinks', 'CreateInviteesItem', 'CreateMeetingBody',
           'CreateMeetingInviteeBody', 'CreateMeetingInviteesBody', 'CreateResponse', 'CustomNumbers', 'Customer',
           'CustomizedQuestionForCreateMeeting', 'DECTHandsetItem', 'DECTHandsetLine', 'DECTHandsetList',
           'DECTNetworkDetail', 'DECTNetworkModel', 'DND', 'Day', 'DaySchedule', 'DectCustomization', 'DectDevice',
           'DefaultAudioType', 'DefaultVoicemailPinRules', 'DeleteDeviceBackgroundImagesResponse',
           'DeleteImageRequestObject', 'DeleteImageResponseSuccessObject', 'DeleteImageResponseSuccessObjectResult',
           'DeleteTranscriptBody', 'DestinationMember', 'DestinationType', 'Device', 'DeviceActivationState',
           'DeviceConfiguration', 'DeviceConfigurationOperation', 'DeviceConfigurationResponse',
           'DeviceConfigurationSource', 'DeviceConfigurationSourceEditability', 'DeviceConfigurationSources',
           'DeviceCustomization', 'DeviceCustomizations', 'DeviceHostedMeetings', 'DeviceLayout', 'DeviceList',
           'DeviceManagedBy', 'DeviceManufacturer', 'DeviceMember', 'DeviceMembersResponse', 'DeviceOwner',
           'DevicePlatform', 'DeviceSettings', 'DeviceSettingsConfiguration', 'DeviceStatus', 'DeviceType',
           'DialPatternStatus', 'DialPatternValidate', 'DialPatternValidationResult', 'DialPlan', 'DialResponse',
           'Dialing', 'DifferentHoursDaily', 'DigitPattern', 'DigitPatterns', 'DirectoryMethod',
           'DisplayCallqueueAgentSoftkey', 'DisplayNameSelection', 'DistinctiveRing', 'ECBNDefault',
           'ECBNDependencies', 'ECBNEffectiveLevel', 'ECBNLocationEffectiveLevel', 'ECBNLocationMember',
           'ECBNQuality', 'ECBNSelection', 'EmailObject', 'EmailObjectType', 'EmailType', 'EmergencyDestination',
           'EnabledAndNumberOfDays', 'EnabledAndValue', 'EnhancedMulticast', 'EnterpriseUser', 'EntryAndExitTone',
           'ErrorMessageObject', 'ErrorObject', 'Event', 'EventData', 'EventResource', 'EventType', 'ExceptionType',
           'ExecAssistantType', 'ExecuteCommandResponse', 'ExpirePasscode', 'ExternalCallerIdNamePolicy',
           'ExternalTransfer', 'FailedAttempts', 'FailureBehavior', 'FeatureAccessCodeDestination',
           'FeatureReference', 'FeatureSelector', 'FeatureType', 'Floor', 'ForcedForward', 'ForwardCallsTo',
           'ForwardFromSelection', 'ForwardOperatingModes', 'ForwardOperatingModesException', 'ForwardTo',
           'ForwardToSelection', 'ForwardingRule', 'ForwardingRuleDetails', 'ForwardingSetting',
           'GetMeetingSurveyResponse', 'GetRoomMeetingDetailsResponse', 'Greeting', 'Group', 'GroupMember',
           'GroupMemberObject', 'GroupMemberResponse', 'GroupMeta', 'Guest', 'GuestCallingSettings', 'HGCallPolicies',
           'HGandCQ', 'Handset', 'HistoryType', 'HolidayService', 'HostedFeatureDestination', 'HostedUserDestination',
           'HotdeskingStatus', 'Hoteling', 'HttpProxy', 'HttpProxyMode', 'HuntGroup', 'IdAndAction', 'IdAndName',
           'IdOnly', 'InProgressDevice', 'Incident', 'IncidentUpdate', 'IncomingPermissions',
           'InitiateMoveNumberJobsBody', 'InputMode', 'InterceptAnnouncements', 'InterceptNumber', 'InterceptSetting',
           'InterceptSettingIncoming', 'InterceptSettingOutgoing', 'InterceptTypeIncoming', 'InterceptTypeOutgoing',
           'InternalDialing', 'InterpreterForSimultaneousInterpretation', 'Invitee', 'InviteeForCreateMeeting',
           'JobError', 'JobErrorItem', 'JobErrorMessage', 'JobExecutionStatus', 'JoinMeetingBody',
           'JoinMeetingResponse', 'KemKey', 'KemModuleType', 'LayoutMode', 'License', 'LicenseProperties',
           'LicenseRequest', 'LicenseRequestOperation', 'LicenseUser', 'LicenseUserType', 'Lifecycle',
           'LineKeyLabelSelection', 'LineKeyLedPattern', 'LineKeyTemplate', 'LineKeyTemplateAdvisoryTypes',
           'LineKeyType', 'LinkRelation', 'Location', 'LocationAddress', 'LocationAndNumbers',
           'LocationCallNotificationOrganization', 'LocationCallParkSettings', 'LocationComplianceAnnouncement',
           'LocationECBN', 'LocationECBNLocation', 'LocationECBNLocationMember', 'LocationEmergencyCallNotification',
           'LocationMoHGreetingType', 'LocationMoHSetting', 'LocationVoiceMailSettings', 'LoggingLevel', 'MACState',
           'MACStatus', 'MACValidationResponse', 'MSTeamsSettings', 'ManageNumberErrorItem', 'ManagedBy',
           'ManagedGroup', 'ManagedOrg', 'ManagerObject', 'MediaFileType', 'MediaSessionQuality', 'Meeting',
           'MeetingCallType', 'MeetingDevice', 'MeetingOptions', 'MeetingPreferenceDetails', 'MeetingService',
           'MeetingState', 'MeetingTelephony', 'MeetingType', 'MeetingsSite', 'MemberCommon', 'Membership',
           'MembershipsData', 'MenuKey', 'Message', 'MessageAttachment', 'MessageSummary', 'MessagesData', 'Meta',
           'MetaObjectResourceType', 'MoHConfig', 'MoHTheme', 'ModeDefaultForwardToSelection', 'ModeForward',
           'ModeForwardTo', 'ModeManagementFeature', 'ModeType', 'MohMessageSetting', 'MonitoredElement',
           'MonitoredElementMember', 'MonitoredMember', 'Monitoring', 'Month', 'MoveCounts', 'MoveNumberCounts',
           'MoveUser', 'MoveUserJobDetails', 'MoveUsersList', 'MppCustomization', 'MppVlanDevice', 'Multicast',
           'MusicOnHold', 'NameObject', 'NetworkConnectionType', 'NetworkType', 'NightService', 'NoAnswer',
           'NoiseCancellation', 'NoteType', 'Notification', 'NotificationRepeat', 'NotificationType',
           'NumberAddError', 'NumberAddResponse', 'NumberAndAction', 'NumberDetails', 'NumberItem', 'NumberJob',
           'NumberListPhoneNumber', 'NumberListPhoneNumberType', 'NumberOwner', 'NumberState', 'NumberType',
           'NumberUsageType', 'OfficeNumber', 'OnboardingMethod', 'OperatingMode', 'OperatingModeHoliday',
           'OperatingModeRecurYearlyByDate', 'OperatingModeRecurYearlyByDay', 'OperatingModeRecurrence',
           'OperatingModeSchedule', 'OrgComplianceAnnouncement', 'OrgEmergencyCallNotification', 'OrgMSTeamsSettings',
           'OrganisationVoicemailSettings', 'OrganisationVoicemailSettingsAPI', 'Organization', 'OriginatorType',
           'OutboundProxy', 'OutgoingCallingPlanPermissionsByDigitPattern', 'OutgoingCallingPlanPermissionsByType',
           'OutgoingPermissionCallType', 'OutgoingPermissions', 'OverflowAction', 'OverflowSetting', 'OwnerType',
           'PSTNConnection', 'PSTNConnectionOption', 'PSTNServiceType', 'PSTNType', 'PTTConnectionType', 'Paging',
           'PagingAgent', 'Participant', 'ParticipantState', 'PasscodeRules', 'PatchMeetingBody',
           'PatchMeetingResponse', 'PatchUserOperation', 'PatchUserOperationOp', 'PatternAction', 'PatternAndAction',
           'PbxUserDestination', 'PeopleStatus', 'Person', 'PersonAddress', 'PersonECBN', 'PersonECBNDirectLine',
           'PersonForwardingSetting', 'PersonNumbers', 'PersonPhoneNumber', 'PersonPlaceAgent',
           'PersonSettingsApiChild', 'PersonType', 'PersonalAssistant', 'PersonalAssistantAlerting',
           'PersonalAssistantPresence', 'PersonalMeetingRoom', 'PersonalMeetingRoomOptions', 'Personality',
           'PhoneLanguage', 'PhoneNumber', 'PhoneNumberStatus', 'PhoneNumberType', 'PhotoObject', 'PhotoObjectType',
           'PickupNotificationType', 'PinLength', 'PlayList', 'PlaylistAnnouncement', 'Policy',
           'PreferredAnswerEndpoint', 'PreferredAnswerEndpointType', 'PreferredAnswerResponse',
           'PrimaryContactMethod', 'PrimaryOrShared', 'PriorityAlert', 'PriorityAlertCriteria', 'Privacy',
           'PrivacyOnRedirectedCalls', 'ProductType', 'ProgrammableLineKey', 'PskObject', 'PstnNumberDestination',
           'PushToTalkAccessType', 'PushToTalkSettings', 'QAObject', 'QualityResources',
           'QueryMeetingParticipantsWithEmailBody', 'QueryStatusResponse', 'Question', 'QuestionAnswer',
           'QuestionOption', 'QuestionType', 'QuestionWithAnswers', 'QueueSettings', 'RETRY_429_MAX_WAIT', 'RGTrunk',
           'Recall', 'RecallHuntGroup', 'RecallType', 'ReceptionistSettings', 'Recipient', 'Record', 'Recording',
           'RecordingFormat', 'RecordingOwnerType', 'RecordingParty', 'RecordingPartyActor', 'RecordingServiceData',
           'RecordingServiceType', 'RecordingSession', 'RecordingState', 'RecordingStatus', 'RecordingStorageRegion',
           'RecordingUser', 'RecordingVendor', 'RecurWeekly', 'RecurYearlyByDate', 'RecurYearlyByDay', 'Recurrence',
           'RedirectReason', 'Redirection', 'Registration', 'RejectAction', 'RepoAnnouncement', 'Report',
           'ReportTemplate', 'RepositoryUsage', 'ResponseError', 'ResponseStatus', 'ResponseStatusType',
           'RingPattern', 'Room', 'RoomTab', 'RoomType', 'RouteGroup', 'RouteGroupUsage', 'RouteIdentity',
           'RouteList', 'RouteListDestination', 'RouteListDetail', 'RouteType', 'RoutingPrefixCounts', 'SafeEnum',
           'SameHoursDaily', 'Schedule', 'ScheduleApiBase', 'ScheduleDay', 'ScheduleLevel', 'ScheduleMonth',
           'ScheduleType', 'ScheduleTypeOrStr', 'ScheduleWeek', 'ScheduledMeeting', 'ScheduledType',
           'SchedulingOptions', 'ScimGroup', 'ScimGroupMember', 'ScimMeta', 'ScimPhoneNumberType', 'ScimUser',
           'ScimValueDisplayRef', 'ScreenPopConfiguration', 'SearchGroupResponse', 'SearchUserResponse',
           'SelectedECBN', 'SelectiveAccept', 'SelectiveAcceptCriteria', 'SelectiveCrit', 'SelectiveCriteria',
           'SelectiveForward', 'SelectiveForwardCriteria', 'SelectiveFrom', 'SelectiveReject',
           'SelectiveRejectCriteria', 'SelectiveScheduleLevel', 'SelectiveSource', 'Sender', 'SequentialRing',
           'SequentialRingCriteria', 'SequentialRingNumber', 'ServiceType', 'SettingsObject', 'SimRing',
           'SimRingCriteria', 'SimRingNumber', 'SimultaneousInterpretation', 'SipAddress', 'SipAddressObject',
           'SipType', 'SiteAccountType', 'SiteResponse', 'SiteType', 'SiteUrlsRequest', 'SoftKeyLayout',
           'SoftKeyMenu', 'StandardRegistrationApproveRule', 'StartJobResponse', 'StartMoveUsersJobResponse',
           'StartStopAnnouncement', 'StatusAPI', 'StatusSummary', 'StepExecutionStatus', 'StorageType', 'StrOrDict',
           'StrandedCalls', 'StrandedCallsAction', 'SupervisorAgentStatus', 'SupportAndConfiguredInfo',
           'SupportedDevice', 'SupportedDevices', 'SupportsLogCollection', 'SurveyResult', 'TagOp', 'Team',
           'TeamMembership', 'TelephoneNumberType', 'Telephony', 'TelephonyCall', 'TelephonyDevice',
           'TelephonyDeviceDetails', 'TelephonyDeviceOwner', 'TelephonyDeviceProxy', 'TelephonyEvent',
           'TelephonyEventData', 'TelephonyLocation', 'TelephonyParty', 'TelephonyType',
           'TemporaryDirectDownloadLink', 'TestCallRoutingResult', 'Tokens', 'TrackingCode', 'TrackingCodeItem',
           'TrackingCodeOption', 'TrackingCodeType', 'Transcript', 'TranscriptSnippet', 'TranscriptStatus',
           'TranslationPattern', 'TranslationPatternConfigurationLevel', 'TranslationPatternLevel', 'TransportType',
           'Trunk', 'TrunkDestination', 'TrunkDetail', 'TrunkDeviceType', 'TrunkType', 'TrunkTypeWithDeviceType',
           'TrunkUsage', 'Type', 'UCMProfile', 'UnansweredCalls', 'UnlockedMeetingJoinSecurity',
           'UpdateContactPhoneNumbers', 'UpdateDefaultSiteBody', 'UpdateMeetingInviteeBody', 'UpdateNumbersResponse',
           'UpdateParticipantBody', 'UpdateParticipantResponse', 'UpdatePersonNumbers', 'UpdatePersonPhoneNumber',
           'UpdatePersonalMeetingRoomOptionsBody', 'UpdateTranscriptSnippetBody', 'UpdateWorkspacePhoneNumber',
           'UsageRouteLists', 'UsageType', 'UsbPortsObject', 'UserAddress', 'UserBase', 'UserDeviceCount',
           'UserLicenseType', 'UserLicensesResponse', 'UserManager', 'UserNumber', 'UserPhoneNumber', 'UserType',
           'UserTypeObject', 'ValidateExtensionStatus', 'ValidateExtensionStatusState', 'ValidateExtensionsResponse',
           'ValidatePhoneNumber', 'ValidatePhoneNumberStatus', 'ValidatePhoneNumberStatusState',
           'ValidatePhoneNumbersResponse', 'ValidateVirtualExtensionRange', 'ValidateVirtualExtensionStatus',
           'ValidationRules', 'ValidationStatus', 'Video', 'VideoDevice', 'VideoIn', 'VideoOptions', 'VideoState',
           'VirtualExtension', 'VirtualExtensionDestination', 'VirtualExtensionLevel', 'VirtualExtensionMode',
           'VirtualExtensionRange', 'VirtualExtensionRangeAction', 'VirtualExtensionRangeValidationResult',
           'VirtualExtensionValidationStatus', 'VirtualLine', 'VirtualLineDevices', 'VirtualLineLocation',
           'VirtualLineNumberPhoneNumber', 'VlanSetting', 'VoiceMailPartyInformation', 'VoiceMailRules',
           'VoiceMessageDetails', 'VoicePortalSettings', 'VoicemailCopyOfMessage', 'VoicemailEnabled',
           'VoicemailEnabledWithGreeting', 'VoicemailFax', 'VoicemailGroup', 'VoicemailGroupDetail',
           'VoicemailMessageStorage', 'VoicemailNotifications', 'VoicemailSettings', 'VoicemailTransferToNumber',
           'VolumeSettings', 'WaitMessageSetting', 'WaitMode', 'WebexGroup', 'WebexGroupMeta', 'WebexGroupOwner',
           'WebexStatus', 'WebexUser', 'WebexUserMeta', 'Webhook', 'WebhookCreate', 'WebhookEvent',
           'WebhookEventData', 'WebhookEventType', 'WebhookResource', 'WebhookStatus', 'Week',
           'WelcomeMessageSetting', 'WifiAuthenticationMethod', 'WifiCustomization', 'WifiNetwork', 'WorkSpaceType',
           'Workspace', 'WorkspaceCalling', 'WorkspaceCallingHybridCalling', 'WorkspaceEmail', 'WorkspaceHealth',
           'WorkspaceHealthIssue', 'WorkspaceHealthLevel', 'WorkspaceIndoorNavigation', 'WorkspaceLocation',
           'WorkspaceLocationFloor', 'WorkspaceNumbers', 'WorkspacePersonalizationTaskResponse',
           'WorkspaceSupportedDevices', 'WorkspaceWebexCalling', '_Helper', 'dt_iso_str', 'enum_str', 'plus1',
           'to_camel', 'webex_id_to_uuid']
