from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CDR', 'CDRResponse']


class CDR(ApiModel):
    #: The time the call was answered. Time is in UTC.
    #: example: 2020-05-14T11:01:17.551Z
    answer_time: Optional[datetime] = Field(alias='Answer time', default=None)
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered, and one will be answered.
    #: example: true
    answered: Optional[str] = Field(alias='Answered', default=None)
    #: The authorization code admin created for a location or site for users to use. Collected by the Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    #: example: 107
    authorization_code: Optional[datetime] = Field(alias='Authorization code', default=None)
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call if necessary.
    #: example: SSE1101163211405201218829100@10.177.4.29
    call_id: Optional[str] = Field(alias='Call ID', default=None)
    #: Identifies whether the call was set up or disconnected normally. Possible values:
    #: - Success
    #: - Failure
    #: - Refusal
    #: example: Success
    call_outcome: Optional[str] = Field(alias='Call outcome', default=None)
    #: Additional information about the Call outcome returned.
    #: example: Normal
    call_outcome_reason: Optional[str] = Field(alias='Call outcome reason', default=None)
    #: Indicates the time at which the call transfer service was invoked during the call. The invocation time is shown using the UTC/GMT time zone format.
    #: example: 2023-06-05T18:21:29.707Z
    call_transfer_time: Optional[datetime] = Field(alias='Call transfer Time', default=None)
    #: Type of call. For example:
    #: - SIP_MEETING
    #: - SIP_INTERNATIONAL
    #: - SIP_SHORTCODE
    #: - SIP_INBOUND
    #: - UNKNOWN
    #: - SIP_EMERGENCY
    #: - SIP_PREMIUM
    #: - SIP_ENTERPRISE
    #: - SIP_TOLLFREE
    #: - SIP_NATIONAL
    #: - SIP_MOBILE
    #: example: SIP_ENTERPRISE
    call_type: Optional[str] = Field(alias='Call type', default=None)
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the called party.
    #: example: CALLEDCLIDGOESHERE
    called_line_id: Optional[str] = Field(alias='Called line ID', default=None)
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the called party.
    #: example: 2002
    called_number: Optional[datetime] = Field(alias='Called number', default=None)
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of the user.
    #: example: YOURCLIDGOESHERE
    calling_line_id: Optional[str] = Field(alias='Calling line ID', default=None)
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number of the user.
    #: example: 2001
    calling_number: Optional[datetime] = Field(alias='Calling number', default=None)
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    #: - SIP
    #: - WXC_CLIENT
    #: - WXC_THIRD_PARTY
    #: - TEAMS_WXC_CLIENT
    #: - WXC_DEVICE
    #: - WXC_SIP_GW
    #: example: SIP_TOLLFREE
    client_type: Optional[str] = Field(alias='Client type', default=None)
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    #: example: 1.0.2.3
    client_version: Optional[str] = Field(alias='Client version', default=None)
    #: Correlation ID to tie together multiple call legs of the same call session.
    #: example: 8e8e1dc7-4f25-4595-b9c7-26237f824535
    correlation_id: Optional[str] = Field(alias='Correlation ID', default=None)
    #: A unique identifier for the user's department name.
    #: example: 4370c763-81ec-403b-aba3-626a7b1cf264
    department_id: Optional[str] = Field(alias='Department ID', default=None)
    #: The MAC address of the device, if known.
    #: example: 6C710D8ABC10
    device_mac: Optional[str] = Field(alias='Device MAC', default=None)
    #: The keypad digits as dialed by the user, before pre-translations.
    #: This field reports multiple call dial possibilities:
    #: - Feature access codes (FAC) used for invoking features such as Last Number Redial or a Call Return.
    #: - An extension that got dialed and a mis-dialed keypad digit from a device/app.
    #: - When a user must dial an outside access code (for example, 9+) before dialing a number, this access code is also reported, as well as the digits dialed thereafter.
    #: Note that when pre-translations have no effect, the dialed digits field contains the same data as the called number field.
    #: This field is only used for originating (outgoing) Calls and is not available for terminating (incoming) Calls.
    #: example: 1246
    dialed_digits: Optional[datetime] = Field(alias='Dialed digits', default=None)
    #: Whether the call was inbound or outbound. The possible values are:
    #: - ORIGINATING
    #: - TERMINATING
    #: example: ORIGINATING
    direction: Optional[str] = Field(alias='Direction', default=None)
    #: The length of the call in seconds.
    #: example: 36.0
    duration: Optional[int] = Field(alias='Duration', default=None)
    #: Inbound trunk may be presented in Originating and Terminating records.
    #: example: InTrunk
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk', default=None)
    #: The country code of the dialed number. This is only populated for international calls.
    #: example: US
    international_country: Optional[str] = Field(alias='International country', default=None)
    #: A unique identifier that is used to correlate CDRs and call legs with each other. This ID is used in conjunction with:
    #: - Remote call ID: To identify the remote CDR of a call leg.
    #: - Transfer related call ID: To identify the call transferred leg.
    #: example: 113104021:0
    local_call_id: Optional[str] = Field(alias='Local call ID', default=None)
    #: Each call consists of two UUIDs known as Local Session ID and Remote Session ID.
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: - The Local SessionID is generated from the Originating user agent.
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: example: 82bb753300105000a0000242be131609
    local_session_id: Optional[str] = Field(alias='Local SessionID', default=None)
    #: Location of the report.
    #: example: Richardson
    location: Optional[str] = Field(alias='Location', default=None)
    #: The device model type the user is using to make or receive the call.
    #: example: 8851-3PCC
    model: Optional[str] = Field(alias='Model', default=None)
    #: A unique identifier that shows if other CDRs are in the same call leg. Two CDRs belong in the same call leg if they have the same Network call ID.
    #: example: BW2356451711108231501755806@10.21.0.192
    network_call_id: Optional[str] = Field(alias='Network call ID', default=None)
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    #: example: 408806bc-a013-4a4b-9a24-85e374912102
    org_uuid: Optional[str] = Field(alias='Org UUID', default=None)
    #: Call redirection reason for the original called number. For example:
    #: - Unconditional: Call Forward Always (CFA) service, Group night forwarding.
    #: - NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto attendant transfer, Transfer out of a Call center etc.
    #: - TimeOfDay: Call scheduled period of automated redirection. CF/selective, group night forwarding.
    #: - UserBusy: DND enabled or the user willingly declined the call. CF/busy or voicemail/busy.
    #: - FollowMe: Automated redirection to a personal redirecting service which could be Simultaneous Ringing, Sequential Ringing, Office Anywhere, or Remote Office.
    #: - CallQueue: A call center call to an agent or a user (a member of the call queue).
    #: - HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #: - Unavailable: To voicemail, when the user has no app or device.
    #: - Unrecognized: Unable to determine the reason.
    #: - Unknown: Call forward by phone with no reason.
    #: - ExplicitIdxxx: Enterprise voice portal redirection to the user’s home voice portal. The “xxx” portion is the digits collected from the caller, identifying the target mailbox (Extension or DN).
    #: - ImplicitId: Indicates an enterprise voice portal redirection to the user’s home voice portal.
    #: example: UserBusy
    original_reason: Optional[str] = Field(alias='Original reason', default=None)
    #: The operating system that the app was running on, if available.
    #: example: na
    os_type: Optional[str] = Field(alias='OS type', default=None)
    #: Outbound trunk may be presented in Originating and Terminating records.
    #: example: OutTrunk
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk', default=None)
    #: Call Redirection Reason for the redirecting number. For example:
    #: - Unconditional: Call Forward Always (CFA) service.
    #: - NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto attendant transfer, Transfer out of a Call center etc.
    #: - TimeOfDay: Call scheduled period of automated redirection. CF/Selective.
    #: - UserBusy: DND enabled or user willingly declined the call. CF/busy or Voicemail/busy.
    #: - FollowMe: Automated redirection to a personal redirecting service which could be Simultaneous Ringing, Sequential Ringing, Office Anywhere, or Remote Office.
    #: - CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #: - HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #: - Unavailable: To voicemail, when the user has no app or device.
    #: - Unrecognized: Unable to determine the reason.
    #: - Unknown: Call forward by phone with no reason.
    #: - ExplicitIdxxx: Enterprise voice portal redirection to the user’s home voice portal. The “xxx” portion is the digits collected from the caller, identifying the target mailbox (Extension or DN).
    #: - ImplicitId: Indicates an enterprise voice portal redirection to the user’s home voice portal.
    #: example: Unavailable
    redirect_reason: Optional[str] = Field(alias='Redirect reason', default=None)
    #: When the call has been redirected one or more times, this field reports the last redirecting number. Identifies who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls, simultaneous rings, etc.
    #: example: +13343822691
    redirecting_number: Optional[str] = Field(alias='Redirecting number', default=None)
    #: Call identifier of a different call that was created by this call because of a service activation. The value is the same as the Local call ID field of the related call. You can use this field to correlate multiple call legs connected through other services.
    #: example: 760583469:0
    related_call_id: Optional[str] = Field(alias='Related call ID', default=None)
    #: Indicates a trigger that led to a change in the call presence. The trigger could be for this particular call or redirected via a different call. For example:
    #: - ConsultativeTransfer: While on a call, the call was transferred to another user by announcing it first. meaning the person was given a heads up or asked if they're interested in taking the call and then transferred.
    #: - CallForwardSelective: Call Forward as per the defined schedule. Might be based on factors like a specific time, specific callers or to a VM. It always takes precedence over Call Forwarding.
    #: - CallForwardAlways: Calls are unconditionally forwarded to a defined phone number or to VM.
    #: - CallForwardNoAnswer: The party was not available to take the call.
    #: - CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #: - HuntGroup: A hunt group based call to an agent or a user (denotes a member of the hunt group).
    #: - CallPickup: The user part of a pickup group or pickup attempted by this user against a ringing call for a different user or extension.
    #: - CalllPark: An ongoing call was parked, assigned with a parked number (not the user’s phone number).
    #: - CallParkRetrieve: Call park retrieval attempt by the user, either for a different extension or against the user’s own extension.
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto-attendant transfer, Transfer out of a Call center, etc.
    #: - FaxDeposit: Indicates a FAX was transmitted to the FAX service.
    #: - PushNotificationRetrieval: Push notification feature usage indication. Means that a push notification was sent to wake up the client and get ready to receive a call.
    #: - BargeIn: Indicates the user barged-in to someone else’s call.
    #: - VoiceXMLScriptTermination: Route Point feature usage indication.
    #: - AnywhereLocation: Indicates call origination towards the single number reach location.
    #: - AnywherePortal: Indicates call origination towards the “user” identified by the single number reach portal.
    #: - Unrecognized: Unable to determine the reason.
    #: - CallForwardBusy: The user willingly declined the call, or DND was enabled that then redirected the call to a defined phone number or voice mail.
    #: - CallForwardNotReachable: Hunt group redirection for an agent who is not reachable.
    #: - CallRetrieve: The user triggered the call retrieve option to pick up a call that was parked.
    #: - CallRecording: The user initiated the call recording service that triggered Start/Pause/Resume/Stop recording options.
    #: - DirectedCallPickup: Indicates this user belonged to a call pickup group who answered the call or answered when another member of the call pickup group in a location was busy.
    #: - Executive: The user has been configured using the Executive/Executive assistant service who is allowed to handle calls on someone else's behalf. Also known as Boss-admin.
    #: - ExecutiveAssistantInitiateCall: The user has been configured as an Executive assistant who placed or initiated the call on someone else’s (Boss admin's) behalf.
    #: - ExecutiveAssistantDivert: The user has been configured as an Executive assistant who had call forwarding enabled to a defined phone number.
    #: - ExecutiveForward: The Executive (Boss-admin) had a call forward setting enabled to a defined number. Generally triggered when an ExecutiveAssistant did not pick a call.
    #: - ExecutiveAssistantCallPush: The user has been configured as an Executive assistant who received a call and pushed that call out (using #63) to the Executive’s (Boss-admin's) number.
    #: - Remote Office: Indicates the call was made to reach the remote location of the user.
    #: - RoutePoint: Indicates an incoming and queued call to an agent (for incoming calls to the route point).
    #: - SequentialRing: Indicates this user is in the list of phone numbers, which are alerted sequentially upon receiving an incoming call that matches a set of criteria.
    #: - SimultaneousRingPersonal: Indicates this user was in the list of multiple destinations that are to ring simultaneously when any calls are received on their phone number (the first destination answered is connected).
    #: - CCMonitoringBI: The indication that a Call Queue supervisor invoked silent monitoring.
    #: example: CallQueue
    related_reason: Optional[str] = Field(alias='Related reason', default=None)
    #: Indicates which party released the call first. The possible values are:
    #: - Local: Used when the local user has released the call first.
    #: - Remote: Used when the far-end party releases the call first.
    #: - Unknown: Used when the call has partial information or is unable to gather enough information about the party who released the call. It could be because of situations like force lock or because of a session audit failure.
    #: example: Remote
    releasing_party: Optional[str] = Field(alias='Releasing party', default=None)
    #: A unique identifier that is used to correlate CDRs and call legs with each other. This ID is used in conjunction with Local call ID to identity the local CDR of a call leg.
    #: example: 113103977:0
    remote_call_id: Optional[str] = Field(alias='Remote call ID', default=None)
    #: Each call consists of two UUIDs known as Local Session ID and Remote Session ID.
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: - The Local SessionID is generated from the Originating user agent.
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: example: 6bf2f47800105000a0000242be13160a
    remote_session_id: Optional[str] = Field(alias='Remote SessionID', default=None)
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    #: example: 0a0c2eb7-f1f6-3326-86f9-565d2e11553d
    report_id: Optional[str] = Field(alias='Report ID', default=None)
    #: The time this report was created. Time is in UTC.
    #: example: 2020-05-14T11:01:52.723Z
    report_time: Optional[datetime] = Field(alias='Report time', default=None)
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex Calling (dial plan or unknown extension).
    #: example: RouteGrpAA
    route_group: Optional[str] = Field(alias='Route group', default=None)
    #: The main number for the user's site where the call was made or received.
    #: example: +14692281000
    site_main_number: Optional[str] = Field(alias='Site main number', default=None)
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    #: example: -300
    site_timezone: Optional[datetime] = Field(alias='Site timezone', default=None)
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    #: example: 474d4f70-4ef5-4d52-9e1d-b207086629e0
    site_uuid: Optional[str] = Field(alias='Site UUID', default=None)
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    #: example: 2020-05-14T11:01:16.545Z
    start_time: Optional[datetime] = Field(alias='Start time', default=None)
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type will show MOBILE_NETWORK.
    #: example: MOBILE_NETWORK
    sub_client_type: Optional[str] = Field(alias='Sub client type', default=None)
    #: Call identifier of a different call that was involved in the transfer. You can share this ID with Cisco TAC to help them pinpoint parties who were involved in the call transfer.
    #: example: 2340586843:0A
    transfer_related_call_id: Optional[str] = Field(alias='Transfer related call ID', default=None)
    #: The user who made or received the call.
    #: example: John Andersen
    user: Optional[str] = Field(alias='User', default=None)
    #: Represents the E.164 number of the user generating a CDR. If the user has no number assigned to them, then their extension will be displayed instead.
    #: example: +81546668399
    user_number: Optional[str] = Field(alias='User number', default=None)
    #: The type of user (user or workspace) that made or received the call. For example:
    #: - AutomatedAttendantVideo: Automated Attendant Video IVR group service.
    #: - Anchor: A Webex Calling user number made or received that is integrated with Webex Contact Center. An "anchor" is created to facilitate the call routing flow between WxC and WxCC.
    #: - BroadworksAnywhere: Single number reach (Office anywhere) service.
    #: - VoiceMailRetrieval: Voice Mail group service.
    #: - LocalGateway: A local gateway-based user who made or received the call.
    #: - HuntGroup: A hunt group based service.
    #: - GroupPaging: One way call or group page made for target users.
    #: - User: The direct user who made or received the call.
    #: - VoiceMailGroup: Shared voicemail or inbound FAX destination for users.
    #: - CallCenterStandard: A call queue-based service.
    #: - VoiceXML: Call added back to the Route Point queue after script termination.
    #: - RoutePoint: Route Point call to an agent (for an incoming call to the routing point).
    #: - Place: A workspace-based user who made or received the call.
    #: - VirtuaLline: Call made or received by a virtual line user using the Multi-line option in Webex Calling.
    #: example: User
    user_type: Optional[str] = Field(alias='User type', default=None)
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    #: example: 47f0d0c2-f05a-44cc-870d-7a3daf859c6c
    user_uuid: Optional[str] = Field(alias='User UUID', default=None)


class CDRResponse(ApiModel):
    items: Optional[list[CDR]] = None
