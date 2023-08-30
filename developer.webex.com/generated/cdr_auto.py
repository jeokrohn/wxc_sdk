from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CDR', 'GetDetailedCallHistoryResponse', 'WebexCallingDetailedCallHistoryApi']


class CDR(ApiModel):
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[str] = Field(alias='Answer time')
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered, and one will
    #: be answered.
    answered: Optional[str] = None
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
    direction: Optional[str] = None
    #: The length of the call in seconds.
    duration: Optional[int] = None
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
    location: Optional[str] = None
    #: The device model type the user is using to make or receive the call.
    model: Optional[str] = None
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
    user: Optional[str] = None
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
    items: Optional[list[CDR]] = None


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
