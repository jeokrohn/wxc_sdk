"""
CDR API
"""
import re
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Union

from dateutil import tz
from dateutil.parser import isoparse
from pydantic import Field, model_validator

from ..api_child import ApiChild
from ..base import ApiModel, dt_iso_str
from ..base import SafeEnum as Enum

__all__ = ['CDRCallType', 'CDRClientType', 'CDRDirection', 'CDROriginalReason', 'CDRRedirectReason',
           'CDRRelatedReason', 'CDRUserType', 'CDR', 'DetailedCDRApi']


class CDRCallType(str, Enum):
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


class CDRClientType(str, Enum):
    sip = 'SIP'
    wxc_client = 'WXC_CLIENT'
    wxc_third_party = 'WXC_THIRD_PARTY'
    teams_wxc_client = 'TEAMS_WXC_CLIENT'
    wxc_device = 'WXC_DEVICE'
    wxc_sip_gw = 'WXC_SIP_GW'


class CDRDirection(str, Enum):
    originating = 'ORIGINATING'
    terminating = 'TERMINATING'


class CDROriginalReason(str, Enum):
    unconditional = 'Unconditional'
    no_answer = 'NoAnswer'
    call_queue = 'CallQueue'
    hunt_group = 'HuntGroup'
    time_of_day = 'TimeOfDay'
    user_busy = 'UserBusy'
    follow_me = 'FollowMe'
    unrecognised = 'Unrecognised'
    deflection = 'Deflection'
    unavailable = 'Unavailable'
    unknown = 'Unknown'


class CDRRedirectReason(str, Enum):
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


class CDRRelatedReason(str, Enum):
    consultative_transfer = 'ConsultativeTransfer'
    call_forward_selective = 'CallForwardSelective'
    call_park = 'CallPark'
    call_park_retrieve = 'CallParkRetrieve'
    call_queue = 'CallQueue'
    unrecognised = 'Unrecognised'
    call_pickup = 'CallPickup'
    call_forward_always = 'CallForwardAlways'
    call_forward_busy = 'CallForwardBusy'
    fax_deposit = 'FaxDeposit'
    hunt_group = 'HuntGroup'
    push_notification_retrieval = 'PushNotificationRetrieval'
    voice_xml_script_termination = 'VoiceXMLScriptTermination'
    call_forward_no_answer = 'CallForwardNoAnswer'
    anywhere_location = 'AnywhereLocation'
    call_retrieve = 'CallRetrieve'
    deflection = 'Deflection'
    directed_call_pickup = 'DirectedCallPickup'


class CDRUserType(str, Enum):
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
    call_center_premium = 'CallCenterPremium'
    voice_xml = 'VoiceXML'
    route_point = 'RoutePoint'
    virtual_line = 'VirtualLine'
    place = 'Place'


CAMEL_RE = re.compile(r'\b ?(\w+)')


def space_separated_to_camel(name: str) -> str:
    """
    get a camel case name for a field name in a CDR
    Example: Answer time -> answerTime

    :meta private:
    """

    def replacement(m) -> str:
        r = m.group(1).lower().capitalize()
        return r

    r, _ = re.subn(CAMEL_RE, replacement, name)
    r = f'{r[0].lower()}{r[1:]}'
    return r


def normalize_name(name: str) -> str:
    return '_'.join(name.split()).lower()


class CDR(ApiModel):

    @model_validator(mode='before')
    def force_none(cls, values: dict):
        """
        Pop all empty strings so that they get caught by Optional[] and convert keys to proper attribute names
        :meta private:
        """
        # get rid of all empty values and convert to snake_case
        values = {normalize_name(k): v for k, v in values.items() if v != '' and v != 'NA'}
        return values

    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    start_time: Optional[datetime] = None
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[datetime] = None
    #: The length of the call in seconds.
    duration: Optional[int] = None
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered,
    # and one will be answered.
    answered: Optional[bool] = None
    #: Whether the call was inbound or outbound. The possible values are:
    direction: Optional[Union[CDRDirection, str]] = None
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the
    #: called party.
    called_line_id: Optional[str] = None
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call
    # if necessary.
    call_id: Optional[str] = None
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of
    # the user.
    calling_line_id: Optional[str] = None
    #: Type of call. For example:
    call_type: Optional[CDRCallType] = None
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    client_type: Optional[CDRClientType] = None
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str] = None
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str] = None
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str] = None
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #:
    #: * The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #:
    #: * It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #:   compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #:
    #: * The Local SessionID is generated from the Originating user agent.
    #:
    #: * The Remote SessionID is generated from the Terminating user agent.
    #:
    #: * The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #:
    #: * The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    local_session_id: Optional[str] = Field(alias='local_sessionid', default=None)
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = None
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str] = None
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str] = None
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    original_reason: Optional[CDROriginalReason] = None
    #: The operating system that the app was running on, if available.
    os_type: Optional[str] = None
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str] = None
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    redirect_reason: Optional[CDRRedirectReason] = None
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    related_reason: Optional[CDRRelatedReason] = None
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str] = None
    #: The time this report was created. Time is in UTC.
    report_time: Optional[datetime] = None
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for
    #: outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex
    #: Calling (dial plan or unknown extension).
    route_group: Optional[str] = None
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str] = None
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str] = None
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type
    #: will show MOBILE_NETWORK.
    sub_client_type: Optional[str] = None
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = None
    #: The user who made or received the call.
    user: Optional[str] = None
    #: The type of user (user or workspace) that made or received the call. For example:
    #:
    #:  * AutomatedAttendantVideo
    #:
    #:  * Anchor
    #:
    #:  * BroadworksAnywhere
    #:
    #:  * VoiceMailRetrieval
    #:
    #:  * LocalGateway
    #:
    #:  * HuntGroup
    #:
    #:  * GroupPaging
    #:
    #:  * User
    #:
    #:  * VoiceMailGroup
    #:
    #:  * CallCenterStandard
    #:
    #:  * VoiceXML
    #:
    #:  * RoutePoint
    user_type: Optional[CDRUserType] = None
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the
    #: called party.
    called_number: Optional[str] = None
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number
    #: of the user.
    calling_number: Optional[str] = None
    #: Location of the report.
    location: Optional[str] = None
    #: Dialed digits
    #: The keypad digits as dialed by the user, before pre-translations. This field reports multiple call dial
    #: possibilities:
    #
    #: Feature access codes (FAC) used for invoking features such as Last Number Redial or a Call Return.
    #:
    #: An extension that got dialed and a mis-dialed keypad digit from a device/app.
    #:
    #: When a user must dial an outside access code (for example, 9+) before dialing a number, this access code is
    #: also reported, as well as the digits dialed thereafter. Note that when pre-translations have no effect,
    #: the dialed digits field contains the same data as the called number field. This field is only used for
    #: originating (outgoing) Calls and is not available for terminating (incoming) Calls.
    dialed_digits: Optional[str] = None
    #: Indicates which party released the call first. The possible values are:
    #:
    #: Local: Used when the local user has released the call first.
    #:
    #: Remote: Used when the far end party releases the call first.
    #:
    #: Unknown: Used when the call has partial information or is unable to gather enough information about the party
    #: who released the call. It could be because of situations like force lock or because of a session audit failure.
    releasing_party: Optional[str] = None
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #:
    #: * The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #:
    #: * It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #:   compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #:
    #: * The Local SessionID is generated from the Originating user agent.
    #:
    #: * The Remote SessionID is generated from the Terminating user agent.
    #:
    #: * The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #:
    #: * The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    remote_session_id: Optional[str] = Field(alias='remote_sessionid', default=None)
    #: When the call has been redirected one or more times, this field reports the last redirecting number.
    #: Identifies who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls,
    #: simultaneous rings, etc.
    redirecting_number: Optional[str] = None
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str] = None
    #: A unique identifier for the user's department name.
    department_id: Optional[str] = None
    #: Transfer related call ID is used as a call identifier of the other call involved in the transfer. You can share
    #: this ID with Cisco TAC to help them pinpoint parties who are involved during a call transfer.
    transfer_related_call_id: Optional[str] = None
    #: The authorization code admin created for a location or site for users to use. Collected by the
    #: Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str] = None
    #: The device model type the user is using to make or receive the call.
    model: Optional[str] = None
    #: Indicates the time at which the call transfer service was invoked during the call. The invocation time is
    #: shown using the UTC/GMT time zone.
    call_transfer_time: Optional[datetime] = None
    #: A unique identifier that’s used to correlate CDRs and call legs with each other. This ID is used in
    #: conjunction with:
    #:
    #:  Remote call ID—To identify the remote CDR of a call leg.
    #:
    #:  Transfer related call ID—To identify the call transferred leg.
    local_call_id: Optional[str] = None
    #: A unique identifier that’s used to correlate CDRs and call legs with each other. This ID is used in
    #: conjunction with Local call ID to identity the local CDR of a call leg.
    remote_call_id: Optional[str] = None
    #: A unique identifier that shows if other CDRs are in the same call leg. Two CDRs belong in the same call leg if
    #: they have the same Network call ID.
    network_call_id: Optional[str] = None
    #: Call identifier of a different call that was created by this call because of a service activation. The value
    #: is the same as the Local call ID field of the related call. You can use this field to correlate multiple call
    #: legs connected through other services.
    related_call_id: Optional[str] = None
    #: Represents the E.164 number of the user generating a CDR. If the user has no number assigned to them,
    #: then their extension will be displayed instead.
    user_number: Optional[str] = None
    #: Identifies whether the call was set up or disconnected normally. Possible values are:
    #:
    #:  Success—Call was routed and disconnected successfully. Includes Normal, UserBusy, and NoAnswer scenarios.
    #:
    #:  Failure—Call failed with an internal or external error.
    #:
    #:  Refusal—Call was rejected because of call block or timeout.
    #:
    #:  You can find more information in the Call outcome reason field.
    call_outcome: Optional[str] = None
    #: Additional information about the Call outcome returned. Possible reasons are:
    #:
    #: Success
    #:
    #: - Normal—Call was completed successfully.
    #:
    #: - UserBusy—Call was a success, but the user was busy.
    #:
    #: - NoAnswer—Call was a success, but the user didn't answer.
    #:
    #: Refusal
    #:
    #: - CallRejected—User rejected the call.
    #:
    #: - UnassignedNumber—Dialed number isn't assigned to any user or service.
    #:
    #: - SIP408—Request timed out.
    #:
    #: - InternalRequestTimeout—Request timed out.
    #:
    #: - Q850102ServerTimeout—Server timed out.
    #:
    #: - NoUserResponse—No response from the user.
    #:
    #: - NoAnswerFromUser—No answer from the user.
    #:
    #: - SIP480—Caller was unavailable.
    #:
    #: - SIP487—Request was terminated by the called number.
    #:
    #: - TemporarilyUnavailable—User was temporarily unavailable.
    #:
    #: - AdminCallBlock—Call was rejected.
    #:
    #: - UserCallBlock—Call was rejected.
    #:
    #: - Unreachable—Unable to route the call to the destination.
    #:
    #: Failure
    #:
    #: - DestinationOutOfOrder—Service request failed.
    #:
    #: - SIP501—Invalid method.
    #:
    #: - SIP503—Service was temporarily unavailable.
    #:
    #: - ProtocolError—Unknown release code.
    #:
    #: - SIP606—Some aspect of the session description wasn't acceptable.
    #:
    #: - NoRouteToDestination—No route available to the destination.
    #:
    #: - Internal—Failed because of internal Webex Calling reasons.
    call_outcome_reason: Optional[str] = None
    #: The length of ringing before the call was answered or timed out, in seconds.
    ring_duration: Optional[int] = None
    #: Whether the call leg was answered after a redirection. Possible values:
    #: * Yes
    #: * No
    #: * Yes-PostRedirection
    answer_indicator: Optional[str] = None
    #: The time the call was finished, in UTC.
    release_time: Optional[datetime] = None
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #:
    #: * The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #:
    #: * It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #:   compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #:
    #: * The Local SessionID is generated from the Originating user agent.
    #:
    #: * The Remote SessionID is generated from the Terminating user agent.
    #:
    #: * The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #:
    #: * The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    final_local_session_id: Optional[str] = Field(alias='final_local_sessionid', default=None)
    #: Each call consists of four UUIDs known as Local Session ID, Final Local Session ID, Remote Session ID and Final
    #: Remote Session ID.
    #:
    #: * The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call.
    #:
    #: * It can be used for end-to-end tracking of a SIP session in IP-based multimedia communication systems in
    #:   compliance with RFC 7206 and draft-ietf-insipid-session-id-15.
    #:
    #: * The Local SessionID is generated from the Originating user agent.
    #:
    #: * The Remote SessionID is generated from the Terminating user agent.
    #:
    #: * The Final Local Session ID has the value of the Local Session ID at the end of the call.
    #:
    #: * The Final Remote Session ID has the value of the Remote Session ID at the end of the call.
    final_remote_session_id: Optional[str] = Field(alias='final_remote_sessionid', default=None)


@dataclass(init=False)
class DetailedCDRApi(ApiChild, base='devices'):
    """
    To retrieve Detailed Call History information, you must use a token with the spark-admin:calling_cdr_read scope.
    The authenticating user must be a read-only-admin or full-admin of the organization and have the administrator
    role "Webex Calling Detailed Call History API access" enabled.

    Detailed Call History information is available 5 minutes after a call has ended and may be retrieved for up to 48
    hours. For example, if a call ends at 9:46 am, the record for that call can be collected using the API from 9:51
    am, and is available until 9:46 am two days later.

    This API is rate-limited to one call every 5 minutes for a given organization ID.
    """

    def get_cdr_history(self, start_time: Union[str, datetime] = None, end_time: Union[datetime, str] = None,
                        locations: list[str] = None, **params) -> Generator[CDR, None, None]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.

            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :type start_time: Union[str, datetime]
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago. Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.
        :type end_time: Union[str, datetime]
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :type locations: list[str]
        :param params: additional arguments
        :return:
        """
        url = 'https://analytics.webexapis.com/v1/cdr_feed'
        if locations:
            params['locations'] = ','.join(locations)
        if not start_time:
            start_time = datetime.now(tz=tz.tzutc()) - timedelta(hours=47, minutes=58)
        if not end_time:
            end_time = datetime.now(tz=tz.tzutc()) - timedelta(minutes=5, seconds=30)

        def guess_datetime(dt: Union[datetime, str]) -> str:
            if isinstance(dt, str):
                dt = isoparse(dt)
            r = dt_iso_str(dt)
            return r

        params['startTime'] = guess_datetime(start_time)
        params['endTime'] = guess_datetime(end_time)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')
