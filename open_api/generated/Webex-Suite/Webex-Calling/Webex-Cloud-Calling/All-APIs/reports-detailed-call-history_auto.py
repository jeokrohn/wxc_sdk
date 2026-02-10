from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CDR', 'ReportsDetailedCallHistoryApi']


class CDR(ApiModel):
    #: Whether the call leg was answered after a redirection. Possible values:
    #: 
    #: - Yes
    #: 
    #: - No
    #: 
    #: - Yes-PostRedirection
    answer_indicator: Optional[str] = Field(alias='Answer indicator', default=None)
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[datetime] = Field(alias='Answer time', default=None)
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered, and one will
    #: be answered.
    answered: Optional[str] = Field(alias='Answered', default=None)
    #: The authorization code admin created for a location or site for users to use. Collected by the
    #: Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str] = Field(alias='Authorization code', default=None)
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call if
    #: necessary.
    call_id: Optional[str] = Field(alias='Call ID', default=None)
    #: Displays the calling party’s presentation number based on the caller ID setting from Control Hub. Can be a
    #: line/extension, location number, or a custom organization option.
    #: 
    #: - The Caller ID number is not restricted to E.164 format and can vary based on system configuration.
    #: 
    #: - For redirected calls, represents only the redirecting party's caller ID number.
    caller_id_number: Optional[str] = Field(alias='Caller ID number', default=None)
    #: Identifies whether the call was set up or disconnected normally. Possible values:
    #: 
    #: - Success: Call is routed and disconnected successfully. Includes Normal, UserBusy, and NoAnswer scenarios.
    #: 
    #: - Failure: Call failed with an internal or external error.
    #: 
    #: - Refusal: Call is rejected because of call block or timeout.
    #: You can find more information in the Call outcome reason field.
    call_outcome: Optional[str] = Field(alias='Call outcome', default=None)
    #: Additional information about the Call outcome returned. Possible reasons are:
    #: 
    #: - Success
    #: - Normal: Call is completed successfully.
    #: - UserBusy: Call is a success, but the user is busy.
    #: - NoAnswer: Call is a success, but the user didn't answer.
    #: 
    #: - Refusal
    #: - CallRejected: Call attempt rejected at the recipient's end.
    #: - UnassignedNumber: The dialed number isn't assigned to any user or service.
    #: - SIP408: Request timed out because couldn’t find the user in time.
    #: - InternalRequestTimeout: Request timed out as the service couldn’t fulfill the request due to an unexpected
    #: condition.
    #: - Q850102ServerTimeout: Recovery on timer expiry/server timed out
    #: - NoUserResponse: No response from any end-user device/client
    #: - NoAnswerFromUser: No answer from the user.
    #: - SIP480: Callee or called party is currently unavailable.
    #: - SIP487: Request is terminated by bye or cancel.
    #: - TemporarilyUnavailable: User is temporarily unavailable.
    #: - AdminCallBlock: Call attempt is rejected due to the organization's call block list.
    #: - UserCallBlock: The call to user is rejected because the number is on the user's block list.
    #: - Unreachable: Unable to route the call to the desired destination.
    #: - LocalGatewayLoop: Loop detected between the local gateway and Webex Calling.
    #: - UserAbsent: User is temporarily unreachable or unavailable.
    #: 
    #: - Failure
    #: - DestinationOutOfOrder: Service request failed as the destination can’t be reached or the interface to the
    #: destination isn’t functioning correctly.
    #: - SIP501: Invalid method and can’t identify the request method.
    #: - SIP503: Service is temporarily unavailable so can’t process the request.
    #: - ProtocolError: Unknown or unimplemented release code.
    #: - SIP606: Some aspect of the session description wasn't acceptable.
    #: - NoRouteToDestination: No route available to the destination
    #: - Internal: Failed because of internal Webex Calling reasons.
    #: - MaxConcurrentTerminatingAlertingRequestsExceeded: The number of simultaneous unanswered calls to a local
    #: gateway, for the same calling and called number, exceeded the limit.
    call_outcome_reason: Optional[str] = Field(alias='Call outcome reason', default=None)
    #: `Call recording Platform Name` and the recording platform can be "DubberRecorder", "Webex" or "Unknown" if the
    #: `Call Recording Platform Name` could not be fetched. Other supported vendors include "Eleveo", "ASCTech",
    #: "MiaRec", and "Imagicle".
    call_recording_platform_name: Optional[str] = Field(alias='Call Recording Platform Name', default=None)
    #: Status of the recorded media: "successful", "failed", or "successful but not kept."
    call_recording_result: Optional[str] = Field(alias='Call Recording Result', default=None)
    #: User's recording mode for the call. The values for this field are "always", always-pause-resume", "on-demand",
    #: or "on-demand-user-start."
    call_recording_trigger: Optional[str] = Field(alias='Call Recording Trigger', default=None)
    #: Indicates the time at which the call transfer service was invoked during the call. The invocation time is shown
    #: using the UTC/GMT time zone format.
    call_transfer_time: Optional[datetime] = Field(alias='Call transfer Time', default=None)
    #: Type of call. For example:
    #: 
    #: - SIP_MEETING
    #: 
    #: - SIP_INTERNATIONAL
    #: 
    #: - SIP_SHORTCODE
    #: 
    #: - SIP_INBOUND
    #: 
    #: - UNKNOWN
    #: 
    #: - SIP_EMERGENCY
    #: 
    #: - SIP_PREMIUM
    #: 
    #: - SIP_ENTERPRISE
    #: 
    #: - SIP_TOLLFREE
    #: 
    #: - SIP_NATIONAL
    #: 
    #: - SIP_MOBILE
    call_type: Optional[str] = Field(alias='Call type', default=None)
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the called
    #: party.
    called_line_id: Optional[str] = Field(alias='Called line ID', default=None)
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the
    #: called party.
    called_number: Optional[str] = Field(alias='Called number', default=None)
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of
    #: the user.
    calling_line_id: Optional[str] = Field(alias='Calling line ID', default=None)
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number of
    #: the user.
    calling_number: Optional[str] = Field(alias='Calling number', default=None)
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    #: 
    #: - SIP
    #: 
    #: - WXC_CLIENT
    #: 
    #: - WXC_THIRD_PARTY
    #: 
    #: - TEAMS_WXC_CLIENT
    #: 
    #: - WXC_DEVICE
    #: 
    #: - WXC_SIP_GW
    client_type: Optional[str] = Field(alias='Client type', default=None)
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str] = Field(alias='Client version', default=None)
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str] = Field(alias='Correlation ID', default=None)
    #: A unique identifier for the user's department name.
    department_id: Optional[str] = Field(alias='Department ID', default=None)
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = Field(alias='Device MAC', default=None)
    #: When calls are made using multi-line or shared line options, this field represents the unique identifier of the
    #: device owner. It holds the UUID from the Cisco Common Identity associated with the user. For example, if Alice
    #: has a device assigned and makes or receives a call from Bob's line, the CDR will show Alice's UUID as the
    #: device owner.
    #: 
    #: - Only set when the device owner is different than the owner of the device who made/received the call.
    device_owner_uuid: Optional[str] = Field(alias='Device owner UUID', default=None)
    #: The keypad digits as dialed by the user, before pre-translations.
    #: This field reports multiple call dial possibilities:
    #: 
    #: - Feature access codes (FAC) used for invoking features such as Last Number Redial or a Call Return.
    #: 
    #: - An extension that got dialed and a mis-dialed keypad digit from a device/app.
    #: 
    #: - When a user must dial an outside access code (for example, 9+) before dialing a number, this access code is
    #: also reported, as well as the digits dialed thereafter.
    #: Note that when pre-translations have no effect, the dialed digits field contains the same data as the called
    #: number field.
    #: This field is only used for originating (outgoing) Calls and is not available for terminating (incoming) Calls.
    dialed_digits: Optional[str] = Field(alias='Dialed digits', default=None)
    #: Whether the call was inbound or outbound. The possible values are:
    #: 
    #: - ORIGINATING
    #: 
    #: - TERMINATING
    direction: Optional[str] = Field(alias='Direction', default=None)
    #: The length of the call in seconds.
    duration: Optional[int] = Field(alias='Duration', default=None)
    #: Set only when the control hub External Caller ID phone number is a location number or another number from the
    #: organization. Not set when "Direct line/Ext" options are selected.
    #: 
    #: - Only included in originating CDRs (not present in terminating CDRs).
    #: 
    #: - Not set for calls that are redirected
    external_caller_id_number: Optional[str] = Field(alias='External caller ID number', default=None)
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #: 
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: 
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #: compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: 
    #: - The Local SessionID is generated from the Originating user agent.
    #: 
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: 
    #: - The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #: 
    #: - The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    final_local_session_id: Optional[str] = Field(alias='Final local SessionID', default=None)
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #: 
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: 
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #: compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: 
    #: - The Local SessionID is generated from the Originating user agent.
    #: 
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: 
    #: - The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #: 
    #: - The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    final_remote_session_id: Optional[str] = Field(alias='Final remote SessionID', default=None)
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk', default=None)
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str] = Field(alias='International country', default=None)
    #: A unique identifier that is used to correlate CDRs and call legs with each other. This ID is used in conjunction
    #: with:
    #: 
    #: - Remote call ID: To identify the remote CDR of a call leg.
    #: 
    #: - Transfer related call ID: To identify the call transferred leg.
    local_call_id: Optional[str] = Field(alias='Local call ID', default=None)
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #: 
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: 
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #: compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: 
    #: - The Local SessionID is generated from the Originating user agent.
    #: 
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: 
    #: - The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #: 
    #: - The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    local_session_id: Optional[str] = Field(alias='Local SessionID', default=None)
    #: Location of the report.
    location: Optional[str] = Field(alias='Location', default=None)
    #: The device model type the user is using to make or receive the call.
    model: Optional[str] = Field(alias='Model', default=None)
    #: A unique identifier that shows if other CDRs are in the same call leg. Two CDRs belong in the same call leg if
    #: they have the same Network call ID.
    network_call_id: Optional[str] = Field(alias='Network call ID', default=None)
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str] = Field(alias='Org UUID', default=None)
    #: Call redirection reason for the original called number. For example:
    #: 
    #: - Unconditional: Call Forward Always (CFA) service, Group night forwarding.
    #: 
    #: - NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #: 
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto attendant
    #: transfer, Transfer out of a Call center etc.
    #: 
    #: - TimeOfDay: Automated redirection based on the time of the call. Call Forwarding Selective, Call Forwarding
    #: mode-based, or Group Night.
    #: 
    #: - UserBusy: DND enabled or the user willingly declined the call. CF/busy or voicemail/busy.
    #: 
    #: - FollowMe: Automated redirection to a personal redirecting service which could be Simultaneous Ringing,
    #: Sequential Ringing, Office Anywhere, or Remote Office.
    #: 
    #: - CallQueue: A call center call to an agent or a user (a member of the call queue).
    #: 
    #: - HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #: 
    #: - Unavailable: To voicemail, when the user has no app or device.
    #: 
    #: - Unrecognized: Unable to determine the reason.
    #: 
    #: - Unknown: Call forward by phone with no reason.
    #: 
    #: - ExplicitIdxxx: Enterprise voice portal redirection to the user’s home voice portal. The “xxx” portion is the
    #: digits collected from the caller, identifying the target mailbox (Extension or DN).
    #: 
    #: - ImplicitId: Indicates an enterprise voice portal redirection to the user’s home voice portal.
    original_reason: Optional[str] = Field(alias='Original reason', default=None)
    #: The operating system that the app was running on, if available.
    os_type: Optional[str] = Field(alias='OS type', default=None)
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk', default=None)
    #: Public IP address of the terminating device or application that is assigned with an Internet Telephony Number.
    public_called_ip_address: Optional[str] = Field(alias='Public Called IP Address', default=None)
    #: Public IP address of the device or application making a call that is assigned with an Internet Telephony Number.
    public_calling_ip_address: Optional[str] = Field(alias='Public Calling IP Address', default=None)
    #: The time the call was finished, in UTC.
    release_time: Optional[datetime] = Field(alias='Release time', default=None)
    #: The length of ringing before the call was answered or timed out, in seconds.
    ring_duration: Optional[int] = Field(alias='Ring duration', default=None)
    #: When a call is redirected one or more times, indicates the unique identifier of the last redirecting party user
    #: or service accountable for the CDR. Holds the value of the UUID contained in the Cisco Common Identity
    #: associated with a user or service.
    redirecting_party_uuid: Optional[str] = Field(alias='Redirecting party UUID', default=None)
    #: Call Redirection Reason for the redirecting number. For example:
    #: 
    #: - Unconditional: Call Forward Always (CFA) service.
    #: 
    #: - NoAnswer: The party was not available to take the call. CF/busy or Voicemail/busy.
    #: 
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto attendant
    #: transfer, Transfer out of a Call center etc.
    #: 
    #: - TimeOfDay: Automated redirection based on the time of the call. Call Forwarding Selective, Call Forwarding
    #: Mode-Based, or Group Night
    #: 
    #: - UserBusy: DND enabled or user willingly declined the call. CF/busy or Voicemail/busy.
    #: 
    #: - FollowMe: Automated redirection to a personal redirecting service which could be Simultaneous Ringing,
    #: Sequential Ringing, Office Anywhere, or Remote Office.
    #: 
    #: - CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #: 
    #: - HuntGroup: A hunt-group-based call to an agent or a user (denotes a member of the hunt group).
    #: 
    #: - Unavailable: To voicemail, when the user has no app or device.
    #: 
    #: - Unrecognized: Unable to determine the reason.
    #: 
    #: - Unknown: Call forward by phone with no reason.
    #: 
    #: - ExplicitIdxxx: Enterprise voice portal redirection to the user’s home voice portal. The “xxx” portion is the
    #: digits collected from the caller, identifying the target mailbox (Extension or DN).
    #: 
    #: - ImplicitId: Indicates an enterprise voice portal redirection to the user’s home voice portal.
    redirect_reason: Optional[str] = Field(alias='Redirect reason', default=None)
    #: When the call has been redirected one or more times, this field reports the last redirecting number. Identifies
    #: who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls,
    #: simultaneous rings, etc.
    redirecting_number: Optional[str] = Field(alias='Redirecting number', default=None)
    #: Call identifier of a different call that was created by this call because of a service activation. The value is
    #: the same as the Local call ID field of the related call. You can use this field to correlate multiple call legs
    #: connected through other services.
    related_call_id: Optional[str] = Field(alias='Related call ID', default=None)
    #: Indicates a trigger that led to a change in the call presence. The trigger could be for this particular call or
    #: redirected via a different call. For example:
    #: 
    #: - ConsultativeTransfer: While on a call, the call was transferred to another user by announcing it first.
    #: meaning the person was given a heads up or asked if they're interested in taking the call and then transferred.
    #: 
    #: - CallForwardModeBased: Calls are forwarded using the mode-based management feature option.
    #: 
    #: - CallForwardSelective: Call Forward as per the defined schedule. Might be based on factors like a specific
    #: time, specific callers or to a VM. It always takes precedence over Call Forwarding.
    #: 
    #: - CallForwardAlways: Calls are unconditionally forwarded to a defined phone number or to VM.
    #: 
    #: - CallForwardNoAnswer: The party was not available to take the call.
    #: 
    #: - CallQueue: A call center call to an agent or a user (denotes a member of the call queue).
    #: 
    #: - HuntGroup: A hunt group based call to an agent or a user (denotes a member of the hunt group).
    #: 
    #: - CallPickup: The user part of a pickup group or pickup attempted by this user against a ringing call for a
    #: different user or extension.
    #: 
    #: - CalllPark: An ongoing call was parked, assigned with a parked number (not the user’s phone number).
    #: 
    #: - CallParkRetrieve: Call park retrieval attempt by the user, either for a different extension or against the
    #: user’s own extension.
    #: 
    #: - Deflection: Indication that a call was redirected. Possible causes could be Blind transfer, Auto-attendant
    #: transfer, Transfer out of a Call center, etc.
    #: 
    #: - FaxDeposit: Indicates a FAX was transmitted to the FAX service.
    #: 
    #: - PushNotificationRetrieval: Push notification feature usage indication. Means that a push notification was sent
    #: to wake up the client and get ready to receive a call.
    #: 
    #: - BargeIn: Indicates the user barged-in to someone else’s call.
    #: 
    #: - VoiceXMLScriptTermination: Route Point feature usage indication.
    #: 
    #: - AnywhereLocation: Indicates call origination towards the single number reach location.
    #: 
    #: - AnywherePortal: Indicates call origination towards the “user” identified by the single number reach portal.
    #: 
    #: - Unrecognized: Unable to determine the reason.
    #: 
    #: - CallForwardBusy: The user willingly declined the call, or DND was enabled that then redirected the call to a
    #: defined phone number or voice mail.
    #: 
    #: - CallForwardNotReachable: Hunt group redirection for an agent who is not reachable.
    #: 
    #: - CallRetrieve: The user triggered the call retrieve option to pick up a call that was parked.
    #: 
    #: - CallRecording: The user initiated the call recording service that triggered Start/Pause/Resume/Stop recording
    #: options.
    #: 
    #: - DirectedCallPickup: Indicates this user belonged to a call pickup group who answered the call or answered when
    #: another member of the call pickup group in a location was busy.
    #: 
    #: - Executive: The user has been configured using the Executive/Executive assistant service who is allowed to
    #: handle calls on someone else's behalf. Also known as Boss-admin.
    #: 
    #: - ExecutiveAssistantInitiateCall: The user has been configured as an Executive assistant who placed or initiated
    #: the call on someone else’s (Boss admin's) behalf.
    #: 
    #: - ExecutiveAssistantDivert: The user has been configured as an Executive assistant who had call forwarding
    #: enabled to a defined phone number.
    #: 
    #: - ExecutiveForward: The Executive (Boss-admin) had a call forward setting enabled to a defined number. Generally
    #: triggered when an ExecutiveAssistant did not pick a call.
    #: 
    #: - ExecutiveAssistantCallPush: The user has been configured as an Executive assistant who received a call and
    #: pushed that call out (using #63) to the Executive’s (Boss-admin's) number.
    #: 
    #: - Remote Office: Indicates the call was made to reach the remote location of the user.
    #: 
    #: - RoutePoint: Indicates an incoming and queued call to an agent (for incoming calls to the route point).
    #: 
    #: - SequentialRing: Indicates this user is in the list of phone numbers, which are alerted sequentially upon
    #: receiving an incoming call that matches a set of criteria.
    #: 
    #: - SimultaneousRingPersonal: Indicates this user was in the list of multiple destinations that are to ring
    #: simultaneously when any calls are received on their phone number (the first destination answered is connected).
    #: 
    #: - CCMonitoringBI: The indication that a Call Queue supervisor invoked silent monitoring.
    related_reason: Optional[str] = Field(alias='Related reason', default=None)
    #: Indicates which party released the call first. The possible values are:
    #: 
    #: - Local: Used when the local user has released the call first.
    #: 
    #: - Remote: Used when the far-end party releases the call first.
    #: 
    #: - Unknown: Used when the call has partial information or is unable to gather enough information about the party
    #: who released the call. It could be because of situations like force lock or because of a session audit failure.
    releasing_party: Optional[str] = Field(alias='Releasing party', default=None)
    #: A unique identifier that is used to correlate CDRs and call legs with each other. This ID is used in conjunction
    #: with Local call ID to identity the local CDR of a call leg.
    remote_call_id: Optional[str] = Field(alias='Remote call ID', default=None)
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #: 
    #: - The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #: 
    #: - It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #: compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #: 
    #: - The Local SessionID is generated from the Originating user agent.
    #: 
    #: - The Remote SessionID is generated from the Terminating user agent.
    #: 
    #: - The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #: 
    #: - The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    remote_session_id: Optional[str] = Field(alias='Remote SessionID', default=None)
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str] = Field(alias='Report ID', default=None)
    #: The time this report was created. Time is in UTC.
    report_time: Optional[datetime] = Field(alias='Report time', default=None)
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for
    #: outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex
    #: Calling (dial plan or unknown extension).
    route_group: Optional[str] = Field(alias='Route group', default=None)
    #: This field is reported whenever an off-net route list call is made or received that exceeds the Route List Calls
    #: license volume for the organization. The value indicates the number of bursting calls (calls over the licensed
    #: volume) at the time the call was made or received.
    route_list_calls_overage: Optional[str] = Field(alias='Route list calls overage', default=None)
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str] = Field(alias='Site main number', default=None)
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str] = Field(alias='Site timezone', default=None)
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str] = Field(alias='Site UUID', default=None)
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    start_time: Optional[datetime] = Field(alias='Start time', default=None)
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type will
    #: show MOBILE_NETWORK.
    sub_client_type: Optional[str] = Field(alias='Sub client type', default=None)
    #: Call identifier of a different call that was involved in the transfer. You can share this ID with Cisco TAC to
    #: help them pinpoint parties who were involved in the call transfer.
    transfer_related_call_id: Optional[str] = Field(alias='Transfer related call ID', default=None)
    #: Represents the display name for the user type involved in the call, such as User, Workspace, Virtual Line, Auto
    #: Attendant, or Call Queue.
    user: Optional[str] = Field(alias='User', default=None)
    #: Represents the E.164 number of the user generating a CDR. If the user has no number assigned to them, then their
    #: extension will be displayed instead.
    user_number: Optional[str] = Field(alias='User number', default=None)
    #: The type of user (user or workspace) that made or received the call. For example:
    #: 
    #: - AutomatedAttendantVideo: Automated Attendant Video IVR group service.
    #: 
    #: - Anchor: A Webex Calling user number made or received that is integrated with Webex Contact Center. An "anchor"
    #: is created to facilitate the call routing flow between WxC and WxCC.
    #: 
    #: - BroadworksAnywhere: Single number reach (Office anywhere) service.
    #: 
    #: - VoiceMailRetrieval: Voice Mail group service.
    #: 
    #: - LocalGateway: A local gateway-based user who made or received the call.
    #: 
    #: - HuntGroup: A hunt group based service.
    #: 
    #: - GroupPaging: One way call or group page made for target users.
    #: 
    #: - User: The direct user who made or received the call.
    #: 
    #: - VoiceMailGroup: Shared voicemail or inbound FAX destination for users.
    #: 
    #: - CallCenterStandard: A call queue-based service.
    #: 
    #: - VoiceXML: Call added back to the Route Point queue after script termination.
    #: 
    #: - RoutePoint: Route Point call to an agent (for an incoming call to the routing point).
    #: 
    #: - Place: A workspace-based user who made or received the call.
    #: 
    #: - VirtuaLline: Call made or received by a virtual line user using the Multi-line option in Webex Calling.
    user_type: Optional[str] = Field(alias='User type', default=None)
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = Field(alias='User UUID', default=None)
    #: Displays the name of the vendor from which one has purchased PSTN service for a specific country. For example:
    #: 
    #: - If purchased from Cisco PSTN, the field would display "Cisco Calling Plans"
    #: 
    #: - If purchased from Cisco Cloud Connected PSTN Partners, the field would list names such as "Tata",
    #: "IntelePeer", "KDDI", etc.
    pstn_vendor_name: Optional[str] = Field(alias='PSTN Vendor Name', default=None)
    #: This field shows the regulated business entity registered to provide PSTN service in a particular country. It is
    #: exclusively used for Cisco Calling Plans.
    #: 
    #: - Note: The name of the regulated entity may vary within a region and across different regions.
    pstn_legal_entity: Optional[str] = Field(alias='PSTN Legal Entity', default=None)
    #: This field displays the organization's Universal Unique Identifier (UUID) for Cisco Calling Plans, which is
    #: unique across various regions.
    pstn_vendor_org_id: Optional[str] = Field(alias='PSTN Vendor Org ID', default=None)
    #: This field represents an immutable UUID, as defined by Cisco, for a PSTN provider partner. It uniquely
    #: identifies the entity that has provided PSTN service in that country.
    pstn_provider_id: Optional[str] = Field(alias='PSTN Provider ID', default=None)
    #: When the call is redirected one or more times, this field represents the unique identifier of the first
    #: redirecting party. This might be a user, service, workspace, or virtual line that’s accountable for the CDRs.
    #: The field holds the value of the UUID contained in the Cisco Common Identity associated with a user, service,
    #: workspace, or virtual line.
    original_called_party_uuid: Optional[str] = Field(alias='Original Called Party UUID', default=None)
    #: This field indicates that the call is a call park recall. A call park recall occurs when a parked call is not
    #: retrieved within the provisioned recall time. In such cases, the system attempts to return the parked call to
    #: the user who originally parked it or to an alternate recall destination, which can only be a hunt group. The
    #: recall attempt may either succeed or fail, and if it fails, the parked call remains unretrieved.
    recall_type: Optional[str] = Field(alias='Recall Type', default=None)
    #: Indicates the total duration of call hold time in seconds. This is the floor value of the calculated hold
    #: duration
    hold_duration: Optional[int] = Field(alias='Hold Duration', default=None)
    #: Indicates the last key pressed value by the caller.
    auto_attendant_key_pressed: Optional[str] = Field(alias='Auto Attendant Key Pressed', default=None)
    #: The field represents the type of call queue service.
    #: 
    #: Example:
    #: 
    #: Queue Type = Customer Assist, if it’s a customer assist based call queue
    #: 
    #: Queue Type = Call Queue, if it’s a calling > feature based call queue
    queue_type: Optional[str] = Field(alias='Queue Type', default=None)
    #: This field is present in the terminating CDR when an incoming call is answered by a different user, workspace,
    #: virtual line, or service.
    #: 
    #: Example: Set to Answered Elsewhere = Yes, for a Hunt Group agent's call when simultaneous routing is in use and
    #: another agent answers the call.
    answered_elsewhere: Optional[str] = Field(alias='Answered Elsewhere', default=None)
    #: This field contains the score received from the caller reputation provider. The score ranges from 0.0 to 5.0. If
    #: the provider doesn’t send a score, the system omits this field.
    caller_reputation_score: Optional[str] = Field(alias='Caller Reputation Score', default=None)
    #: This field records the outcome of the Caller Reputation Service and appears only in terminating CDRs. The field
    #: can contain the following values:
    #: 
    #: allow — Set when the caller’s reputation score meets or exceeds the higher threshold, or if an error occurs
    #: while obtaining the reputation score from the provider.
    #: 
    #: captcha-allow — Set when the caller’s reputation score falls between the lower and higher thresholds and the
    #: caller successfully completes the captcha challenge.
    #: 
    #: captcha-block — Set when the caller’s reputation score falls between the lower and higher thresholds and the
    #: caller fails or abandons the captcha challenge.
    #: 
    #: block — Set when the caller’s reputation score is below the lower threshold.
    caller_reputation_service_result: Optional[str] = Field(alias='Caller Reputation Service Result', default=None)
    #: This field indicates the reason for the reputation score is assigned for a call. This field contains the reason
    #: value provided by the caller reputation provider in the call analysis request. If the score couldn’t be
    #: obtained from the provider due to error conditions, then the score reason specifies the particular error.
    caller_reputation_score_reason: Optional[str] = Field(alias='Caller Reputation Score Reason', default=None)


class ReportsDetailedCallHistoryApi(ApiChild, base='cdr_feed'):
    """
    Reports: Detailed Call History
    
    The base URL for these APIs is **analytics-calling.webexapis.com** (or
    **analytics-calling-gov.webexapis.com** for Government). These endpoints are
    not compatible with the API reference's **Try It** feature. For questions or
    assistance, please contact the Webex Developer Support team at
    devsupport@webex.com.
    
    
    
    The CDR Feed API is recommended for users who need to pull CDR records for a specific time period. For more
    up-to-date records, use the cdr_stream endpoint API instead.
    
    To retrieve Detailed Call History information, your request must include a token with the
    `spark-admin:calling_cdr_read` `scope
    <https://developer.webex.com/docs/integrations#scopes>`_. Additionally, the authenticating user must have the administrator role
    "Webex Calling Detailed Call History API access" enabled.
    
    The CDR Feed API can query any 12-hour period between 5 minutes ago and 30 days prior to the current UTC time. Only
    12 hours of records can be retrieved per request (i.e., the time between the selected start and end times in a
    single API call). For example: If a call ends at 9:46 AM, the record is available for collection starting at 9:51
    AM and remains available until 9:46 AM 30 days later. The maximum query duration starting at 9:51 AM would end at
    9:51 PM the same day.
    
    This API is rate-limited to 1 initial request per minute per user token, with up to 10 additional pagination
    requests per minute per user token.
    
    Details on the fields returned from this API and their potential values are available at
    <https://help.webex.com/en-us/article/nmug598/Reports-for-Your-Cloud-Collaboration-Portfolio>. Select the **Report
    templates** tab, and under the **Webex Calling reports**, see **Calling Detailed Call History Report**.
    
    By default, the calls to analytics-calling.webexapis.com are routed to the closest region's servers. If the
    region's servers host the organization's data, then the data is returned. Otherwise, an HTTP 451 error code is
    returned. In such cases, the response body contains endpoint information indicating where the organization’s data
    can be retrieved.
    """

    def get_detailed_call_history(self, start_time: Union[str, datetime], end_time: Union[str, datetime],
                                  locations: str = None, **params) -> Generator[CDR, None, None]:
        """
        Get Detailed Call History

        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the `startTime`, `endTime` and `locations` request parameters. The `startTime` and
        `endTime` parameters specify the start and end of the time period for the Detailed Call History reports you
        wish to collect. The API will return all reports that were created between `startTime` and `endTime`.

        <br/><br/>
        Response entries may be added as more information is made available for the reports.
        Values in response items may be extended as more capabilities are added to Webex Calling.

        :param start_time: Time of the first report you wish to collect. (Report time is the time the call finished).
            **Note:** The specified time must be between 5 minutes ago and 48 hours ago, and formatted as
            `YYYY-MM-DDTHH:MM:SS.mmmZ`.
        :type start_time: Union[str, datetime]
        :param end_time: Time of the last report you wish to collect. (Report time is the time the call finished).
            **Note:** The specified time should be later than `startTime` but no later than 48 hours, and formatted as
            `YYYY-MM-DDTHH:MM:SS.mmmZ`.
        :type end_time: Union[str, datetime]
        :param locations: Name of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :type locations: str
        :return: Generator yielding :class:`CDR` instances
        """
        if isinstance(start_time, str):
            start_time = isoparse(start_time)
        start_time = dt_iso_str(start_time)
        params['startTime'] = start_time
        if isinstance(end_time, str):
            end_time = isoparse(end_time)
        end_time = dt_iso_str(end_time)
        params['endTime'] = end_time
        if locations is not None:
            params['locations'] = locations
        url = self.ep()
        return self.session.follow_pagination(url=url, model=CDR, item_key='items', params=params)
