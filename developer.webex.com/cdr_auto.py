from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, Enum
from typing import List, Optional
from pydantic import Field


__all__ = ['CDR', 'CallType', 'ClientType', 'Direction', 'GetDetailedCallHistoryResponse', 'OriginalReason', 'RedirectReason', 'RelatedReason', 'UserType', 'WebexCallingDetailedCallHistoryApi']


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
    #: The authorization code admin created for a location or site for users to use. Collected by the Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str] = Field(alias='Authorization code')
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
    #: A unique identifier for the user's department name.
    department_id: Optional[str] = Field(alias='Department ID')
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = Field(alias='Device MAC')
    #: The keypad digits as dialed by the user, before pre-translations. 
    #: This field reports multiple call dial possibilities:
    dialed_digits: Optional[str] = Field(alias='Dialed digits')
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
    #: The device model type the user is using to make or receive the call. 
    model: Optional[str]
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
    #: When the call has been redirected one or more times, this field reports the last redirecting number. Identifies who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls, simultaneous rings, etc.
    redirecting_number: Optional[str] = Field(alias='Redirecting number')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    related_reason: Optional[RelatedReason] = Field(alias='Related reason')
    #: Indicates which party released the call first. The possible values are:
    releasing_party: Optional[str] = Field(alias='Releasing party')
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
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str] = Field(alias='Site UUID')
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC. 
    start_time: Optional[str] = Field(alias='Start time')
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type will show MOBILE_NETWORK.
    sub_client_type: Optional[str] = Field(alias='Sub client type')
    #: Transfer related call ID is used as a call identifier of the other call involved in the transfer. You can share this ID with Cisco TAC to help them pinpoint parties who are involved during a call transfer.
    transfer_related_call_id: Optional[str] = Field(alias='Transfer related call ID')
    #: The type of user (user or workspace) that made or received the call. For example:
    user_type: Optional[UserType] = Field(alias='User type')
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = Field(alias='User UUID')


class GetDetailedCallHistoryResponse(ApiModel):
    items: Optional[list[CDR]]


class WebexCallingDetailedCallHistoryApi(ApiChild, base=''):
    """
    The base URL for these APIs is analytics.webexapis.com (or analytics-f.webex.com for Government), which does not work with the API reference's Try It feature. If you have any questions or need help please contact the Webex Developer Support team at devsupport@webex.com.
    To retrieve Detailed Call History information, you must use a token with the spark-admin:calling_cdr_read scope. The authenticating user must be a read-only-admin or full-admin of the organization and have the administrator role "Webex Calling Detailed Call History API access" enabled.
    Detailed Call History information is available 5 minutes after a call has ended and may be retrieved for up to 48 hours. For example, if a call ends at 9:46 am, the record for that call can be collected using the API from 9:51 am, and is available until 9:46 am two days later.
    This API is rate-limited to one call every 5 minutes for a given organization ID.
    Details on the fields returned from this API and their potential values are available at https://help.webex.com/en-us/article/nmug598/Reports-for-Your-Cloud-Collaboration-Portfolio under the section Detailed Call History.
    """

    def detailed_call_history(self, start_time: str, end_time: str, locations: str = None, max: int = None) -> List[CDR]:
        """
        Provides Webex Calling Detailed Call History data for your organization.
        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime parameters specify the start and end of the time period for the Detailed Call History reports you wish to collect. The API will return all reports that were created between startTime and endTime.
        
        Response entries may be added as more information is made available for the reports.
        Values in response items may be extended as more capabilities are added to Webex Calling.

        :param start_time: Time of the first report you wish to collect. (Report time is the time the call finished). Note: The specified time must be between 5 minutes ago and 48 hours ago, and be formatted as YYYY-MM-DDTHH:MM:SS.mmmZ.
        :type start_time: str
        :param end_time: Time of the last report you wish to collect. (Report time is the time the call finished). Note: The specified time should be later than startTime but no later than 48 hours, and be formatted as YYYY-MM-DDTHH:MM:SS.mmmZ.
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
