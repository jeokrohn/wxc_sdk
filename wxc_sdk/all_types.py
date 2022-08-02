from wxc_sdk.base import ApiModel, ApiModelWithErrors, CodeAndReason, StrOrDict, to_camel, webex_id_to_uuid
from wxc_sdk.common import AlternateNumber, AuthCode, CallParkExtension, Customer, DialPatternStatus,\
    DialPatternValidate, Greeting, IdAndName, MonitoredMember, NumberState, PatternAction, PersonPlaceAgent,\
    RingPattern, RouteIdentity, RouteType, UserBase, UserNumber, UserType, ValidateExtensionResponseStatus,\
    ValidateExtensionStatus, ValidateExtensionStatusState, ValidateExtensionsResponse, ValidatePhoneNumberStatus,\
    ValidatePhoneNumberStatusState, ValidatePhoneNumbersResponse
from wxc_sdk.common.schedules import Event, RecurWeekly, RecurYearlyByDate, RecurYearlyByDay, Recurrence,\
    Schedule, ScheduleApiBase, ScheduleDay, ScheduleMonth, ScheduleType, ScheduleTypeOrStr, ScheduleWeek
from wxc_sdk.groups import Group, GroupMember
from wxc_sdk.licenses import License, SiteType
from wxc_sdk.locations import Location, LocationAddress
from wxc_sdk.people import PeopleStatus, Person, PersonType, PhoneNumber, PhoneNumberType, SipAddress, SipType
from wxc_sdk.person_settings.appservices import AppServicesSettings
from wxc_sdk.person_settings.barge import BargeSettings
from wxc_sdk.person_settings.call_intercept import InterceptAnnouncements, InterceptNumber, InterceptSetting,\
    InterceptSettingIncoming, InterceptSettingOutgoing, InterceptTypeIncoming, InterceptTypeOutgoing
from wxc_sdk.person_settings.call_recording import CallRecordingSetting, Notification, NotificationRepeat,\
    NotificationType, Record
from wxc_sdk.person_settings.caller_id import CallerId, CallerIdSelectedType, CustomNumberInfo, CustomNumberType,\
    ExternalCallerIdNamePolicy
from wxc_sdk.person_settings.calling_behavior import BehaviorType, CallingBehavior
from wxc_sdk.person_settings.common import PersonSettingsApiChild
from wxc_sdk.person_settings.dnd import DND
from wxc_sdk.person_settings.exec_assistant import ExecAssistantType, _Helper
from wxc_sdk.person_settings.forwarding import CallForwardingAlways, CallForwardingCommon, CallForwardingNoAnswer,\
    CallForwardingPerson, PersonForwardingSetting
from wxc_sdk.person_settings.monitoring import MonitoredElement, MonitoredElementMember, Monitoring
from wxc_sdk.person_settings.numbers import PersonNumbers, PersonPhoneNumber, UpdatePersonNumbers,\
    UpdatePersonPhoneNumber
from wxc_sdk.person_settings.permissions_in import ExternalTransfer, IncomingPermissions
from wxc_sdk.person_settings.permissions_out import Action, AutoTransferNumbers, CallTypePermission,\
    CallingPermissions, OutgoingPermissionCallType, OutgoingPermissions
from wxc_sdk.person_settings.privacy import Privacy
from wxc_sdk.person_settings.push_to_talk import PTTConnectionType, PushToTalkAccessType, PushToTalkSettings
from wxc_sdk.person_settings.receptionist import ReceptionistSettings
from wxc_sdk.person_settings.voicemail import StorageType, UnansweredCalls, VoiceMailFax, VoicemailCopyOfMessage,\
    VoicemailEnabled, VoicemailEnabledWithGreeting, VoicemailFax, VoicemailMessageStorage, VoicemailNotifications,\
    VoicemailSettings, VoicemailTransferToNumber
from wxc_sdk.telephony import CallSourceInfo, CallSourceType, DestinationType, EmergencyDestination,\
    FeatureAccessCodeDestination, HostedAgentDestination, HostedFeatureDestination, LocationAndNumbers,\
    NumberDetails, NumberListPhoneNumber, NumberListPhoneNumberType, NumberLocation, NumberOwner, NumberType,\
    OriginatorType, OwnerType, PbxUserDestination, PstnNumberDestination, RouteListDestination, ServiceType,\
    TestCallRoutingResult, TrunkDestination, UCMProfile, VirtualExtensionDestination
from wxc_sdk.telephony.autoattendant import AutoAttendant, AutoAttendantAction, AutoAttendantKeyConfiguration,\
    AutoAttendantMenu, Dialing, MenuKey
from wxc_sdk.telephony.callpark import AvailableRecallHuntGroup, CallPark, CallParkRecall, CallParkSettings,\
    LocationCallParkSettings, RecallHuntGroup
from wxc_sdk.telephony.callpickup import CallPickup
from wxc_sdk.telephony.callqueue import AudioSource, CallBounce, CallQueue, CallQueueCallPolicies,\
    ComfortMessageSetting, DistinctiveRing, MohMessageSetting, OverflowAction, OverflowSetting, QueueSettings,\
    WaitMessageSetting, WaitMode, WelcomeMessageSetting
from wxc_sdk.telephony.callqueue.announcement import Announcement
from wxc_sdk.telephony.calls import CallHistoryRecord, CallInfo, CallState, CallType, DialResponse, HistoryType,\
    ParkedAgainst, Personality, Recall, RecordingState, RedirectReason, Redirection, RejectAction, TelephonyCall,\
    TelephonyEvent, TelephonyEventData, TelephonyParty
from wxc_sdk.telephony.forwarding import CallForwarding, CallForwardingNumber, CallForwardingNumberType,\
    CallsFrom, CustomNumbers, FeatureSelector, ForwardCallsTo, ForwardToSelection, ForwardingRule,\
    ForwardingRuleDetails, ForwardingSetting
from wxc_sdk.telephony.hg_and_cq import Agent, AlternateNumberSettings, HGandCQ, Policy
from wxc_sdk.telephony.huntgroup import BusinessContinuity, HGCallPolicies, HuntGroup, NoAnswer
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.location.moh import LocationMoHGreetingType, LocationMoHSetting
from wxc_sdk.telephony.location.vm import LocationVoiceMailSettings
from wxc_sdk.telephony.organisation_vm import OrganisationVoicemailSettings, OrganisationVoicemailSettingsAPI
from wxc_sdk.telephony.paging import Paging, PagingAgent
from wxc_sdk.telephony.pnc import NetworkConnectionType
from wxc_sdk.telephony.prem_pstn import DialPatternValidationResult, DialPatternValidationStatus
from wxc_sdk.telephony.prem_pstn.dial_plan import CreateResponse, DialPlan, PatternAndAction
from wxc_sdk.telephony.prem_pstn.route_group import RGTrunk, RouteGroup, RouteGroupUsage, UsageRouteLists
from wxc_sdk.telephony.prem_pstn.route_list import NumberAndAction, RouteList, RouteListDetail,\
    UpdateNumbersResponse
from wxc_sdk.telephony.prem_pstn.trunk import DeviceStatus, OutboundProxy, ResponseStatus, ResponseStatusType,\
    Trunk, TrunkDetail, TrunkDeviceType, TrunkLocation, TrunkType, TrunkTypeWithDeviceType, TrunkUsage
from wxc_sdk.telephony.vm_rules import BlockContiguousSequences, BlockPreviousPasscodes, BlockRepeatedDigits,\
    DefaultVoicemailPinRules, EnabledAndNumberOfDays, PinLength, VoiceMailRules
from wxc_sdk.telephony.voicemail_groups import VoicemailGroup
from wxc_sdk.telephony.voiceportal import ExpirePasscode, FailedAttempts, PasscodeRules, VoicePortalSettings
from wxc_sdk.tokens import Tokens
from wxc_sdk.webhook import WebHook, WebHookCreate, WebHookEvent, WebHookResource, WebHookStatus
from wxc_sdk.workspaces import Calendar, CalendarType, CallingType, WorkSpaceType, Workspace, WorkspaceEmail

__all__ = ['Action', 'Agent', 'AlternateNumber', 'AlternateNumberSettings', 'Announcement', 'ApiModel',
           'ApiModelWithErrors', 'AppServicesSettings', 'AudioSource', 'AuthCode', 'AutoAttendant',
           'AutoAttendantAction', 'AutoAttendantKeyConfiguration', 'AutoAttendantMenu', 'AutoTransferNumbers',
           'AvailableRecallHuntGroup', 'BargeSettings', 'BehaviorType', 'BlockContiguousSequences',
           'BlockPreviousPasscodes', 'BlockRepeatedDigits', 'BusinessContinuity', 'Calendar', 'CalendarType',
           'CallBounce', 'CallForwarding', 'CallForwardingAlways', 'CallForwardingCommon', 'CallForwardingNoAnswer',
           'CallForwardingNumber', 'CallForwardingNumberType', 'CallForwardingPerson', 'CallHistoryRecord',
           'CallInfo', 'CallPark', 'CallParkExtension', 'CallParkRecall', 'CallParkSettings', 'CallPickup',
           'CallQueue', 'CallQueueCallPolicies', 'CallRecordingSetting', 'CallSourceInfo', 'CallSourceType',
           'CallState', 'CallType', 'CallTypePermission', 'CallerId', 'CallerIdSelectedType', 'CallingBehavior',
           'CallingPermissions', 'CallingType', 'CallsFrom', 'CodeAndReason', 'ComfortMessageSetting',
           'CreateResponse', 'CustomNumberInfo', 'CustomNumberType', 'CustomNumbers', 'Customer', 'DND',
           'DefaultVoicemailPinRules', 'DestinationType', 'DeviceStatus', 'DialPatternStatus', 'DialPatternValidate',
           'DialPatternValidationResult', 'DialPatternValidationStatus', 'DialPlan', 'DialResponse', 'Dialing',
           'DistinctiveRing', 'EmergencyDestination', 'EnabledAndNumberOfDays', 'Event', 'ExecAssistantType',
           'ExpirePasscode', 'ExternalCallerIdNamePolicy', 'ExternalTransfer', 'FailedAttempts',
           'FeatureAccessCodeDestination', 'FeatureSelector', 'ForwardCallsTo', 'ForwardToSelection',
           'ForwardingRule', 'ForwardingRuleDetails', 'ForwardingSetting', 'Greeting', 'Group', 'GroupMember',
           'HGCallPolicies', 'HGandCQ', 'HistoryType', 'HostedAgentDestination', 'HostedFeatureDestination',
           'HuntGroup', 'IdAndName', 'IncomingPermissions', 'InterceptAnnouncements', 'InterceptNumber',
           'InterceptSetting', 'InterceptSettingIncoming', 'InterceptSettingOutgoing', 'InterceptTypeIncoming',
           'InterceptTypeOutgoing', 'InternalDialing', 'License', 'Location', 'LocationAddress', 'LocationAndNumbers',
           'LocationCallParkSettings', 'LocationMoHGreetingType', 'LocationMoHSetting', 'LocationVoiceMailSettings',
           'MenuKey', 'MohMessageSetting', 'MonitoredElement', 'MonitoredElementMember', 'MonitoredMember',
           'Monitoring', 'NetworkConnectionType', 'NoAnswer', 'Notification', 'NotificationRepeat',
           'NotificationType', 'NumberAndAction', 'NumberDetails', 'NumberListPhoneNumber',
           'NumberListPhoneNumberType', 'NumberLocation', 'NumberOwner', 'NumberState', 'NumberType',
           'OrganisationVoicemailSettings', 'OrganisationVoicemailSettingsAPI', 'OriginatorType', 'OutboundProxy',
           'OutgoingPermissionCallType', 'OutgoingPermissions', 'OverflowAction', 'OverflowSetting', 'OwnerType',
           'PTTConnectionType', 'Paging', 'PagingAgent', 'ParkedAgainst', 'PasscodeRules', 'PatternAction',
           'PatternAndAction', 'PbxUserDestination', 'PeopleStatus', 'Person', 'PersonForwardingSetting',
           'PersonNumbers', 'PersonPhoneNumber', 'PersonPlaceAgent', 'PersonSettingsApiChild', 'PersonType',
           'Personality', 'PhoneNumber', 'PhoneNumberType', 'PinLength', 'Policy', 'Privacy', 'PstnNumberDestination',
           'PushToTalkAccessType', 'PushToTalkSettings', 'QueueSettings', 'RGTrunk', 'Recall', 'RecallHuntGroup',
           'ReceptionistSettings', 'Record', 'RecordingState', 'RecurWeekly', 'RecurYearlyByDate', 'RecurYearlyByDay',
           'Recurrence', 'RedirectReason', 'Redirection', 'RejectAction', 'ResponseStatus', 'ResponseStatusType',
           'RingPattern', 'RouteGroup', 'RouteGroupUsage', 'RouteIdentity', 'RouteList', 'RouteListDestination',
           'RouteListDetail', 'RouteType', 'Schedule', 'ScheduleApiBase', 'ScheduleDay', 'ScheduleMonth',
           'ScheduleType', 'ScheduleTypeOrStr', 'ScheduleWeek', 'ServiceType', 'SipAddress', 'SipType', 'SiteType',
           'StorageType', 'StrOrDict', 'TelephonyCall', 'TelephonyEvent', 'TelephonyEventData', 'TelephonyParty',
           'TestCallRoutingResult', 'Tokens', 'Trunk', 'TrunkDestination', 'TrunkDetail', 'TrunkDeviceType',
           'TrunkLocation', 'TrunkType', 'TrunkTypeWithDeviceType', 'TrunkUsage', 'UCMProfile', 'UnansweredCalls',
           'UpdateNumbersResponse', 'UpdatePersonNumbers', 'UpdatePersonPhoneNumber', 'UsageRouteLists', 'UserBase',
           'UserNumber', 'UserType', 'ValidateExtensionResponseStatus', 'ValidateExtensionStatus',
           'ValidateExtensionStatusState', 'ValidateExtensionsResponse', 'ValidatePhoneNumberStatus',
           'ValidatePhoneNumberStatusState', 'ValidatePhoneNumbersResponse', 'VirtualExtensionDestination',
           'VoiceMailFax', 'VoiceMailRules', 'VoicePortalSettings', 'VoicemailCopyOfMessage', 'VoicemailEnabled',
           'VoicemailEnabledWithGreeting', 'VoicemailFax', 'VoicemailGroup', 'VoicemailMessageStorage',
           'VoicemailNotifications', 'VoicemailSettings', 'VoicemailTransferToNumber', 'WaitMessageSetting',
           'WaitMode', 'WebHook', 'WebHookCreate', 'WebHookEvent', 'WebHookResource', 'WebHookStatus',
           'WelcomeMessageSetting', 'WorkSpaceType', 'Workspace', 'WorkspaceEmail', '_Helper', 'to_camel',
           'webex_id_to_uuid']
