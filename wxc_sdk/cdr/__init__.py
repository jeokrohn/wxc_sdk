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
from pydantic import Field, root_validator

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



class CDR(ApiModel):

    @root_validator(pre=True)
    def force_none(cls, values: dict):
        """
        Pop all empty strings so that they get caught by Optional[] and convert keys to camelCase
        :param values:
        :return:
        """
        # get rid of all empty values and convert to camelCase
        values = {space_separated_to_camel(k): v for k, v in values.items() if v != '' and v != 'NA'}
        return values

    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    start_time: Optional[datetime]
    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[datetime]
    #: The length of the call in seconds.
    duration: Optional[int]
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered,
    # and one will be answered.
    answered: Optional[bool]
    #: Whether the call was inbound or outbound. The possible values are:
    direction: Optional[Union[CDRDirection, str]]
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the
    #: called party.
    called_line_id: Optional[str]
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call
    # if necessary.
    call_id: Optional[str]
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of
    # the user.
    calling_line_id: Optional[str]
    #: Type of call. For example:
    call_type: Optional[CDRCallType]
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    client_type: Optional[CDRClientType]
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str]
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str]
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str]
    #: The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call. It
    #: can be used for end-to-end tracking of a SIP session in IP-based multimedia communication. Each call consists of
    #: two UUIDs known as Local Session ID and Remote Session ID.
    #:   * The Local SessionID is generated from the Originating user agent.
    local_session_id: Optional[str] = Field(alias='localSessionid')
    #: The MAC address of the device, if known.
    device_mac: Optional[str]
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str]
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str]
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    original_reason: Optional[CDROriginalReason]
    #: The operating system that the app was running on, if available.
    os_type: Optional[str]
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str]
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    redirect_reason: Optional[CDRRedirectReason]
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    related_reason: Optional[CDRRelatedReason]
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str]
    #: The time this report was created. Time is in UTC.
    report_time: Optional[datetime]
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for
    #: outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex
    #: Calling (dial plan or unknown extension).
    route_group: Optional[str]
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str]
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str]
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type
    #: will show MOBILE_NETWORK.
    sub_client_type: Optional[str]
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str]
    #: The user who made or received the call.
    user: Optional[str]
    #: The type of user (user or workspace) that made or received the call. For example:
    #:  * AutomatedAttendantVideo
    #:  * Anchor
    #:  * BroadworksAnywhere
    #:  * VoiceMailRetrieval
    #:  * LocalGateway
    #:  * HuntGroup
    #:  * GroupPaging
    #:  * User
    #:  * VoiceMailGroup
    #:  * CallCenterStandard
    #:  * VoiceXML
    #:  * RoutePoint
    user_type: Optional[CDRUserType]
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the
    #: called party.
    called_number: Optional[str]
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number
    #: of the user.
    calling_number: Optional[str]
    #: Location of the report.
    location: Optional[str]
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
    dialed_digits: Optional[str]
    #: Indicates which party released the call first. The possible values are:
    #:
    #: Local: Used when the local user has released the call first.
    #: Remote: Used when the far end party releases the call first.
    #: Unknown: Used when the call has partial information or is unable to gather enough information about the party
    #: who released the call. It could be because of situations like force lock or because of a session audit failure.
    releasing_party: Optional[str]
    #: The Session ID comprises a Universally Unique Identifier (UUID) for each user-agent participating in a call. It
    #: can be used for end-to-end tracking of a SIP session in IP-based multimedia communication. Each call consists of
    #: two UUIDs known as Local Session ID and Remote Session ID.
    #:   * The Remote SessionID is generated from the Terminating user agent.
    remote_session_id: Optional[str] = Field(alias='remoteSessionid')
    #: When the call has been redirected one or more times, this field reports the last redirecting number.
    #: Identifies who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls,
    #: simultaneous rings, etc.
    redirecting_number: Optional[str]
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str]
    #: A unique identifier for the user's department name.
    department_id: Optional[str]
    #: Transfer related call ID is used as a call identifier of the other call involved in the transfer. You can share
    #: this ID with Cisco TAC to help them pinpoint parties who are involved during a call transfer.
    transfer_related_call_id: Optional[str]
    #: The user who made or received the call.
    user: Optional[str]
    #: The authorization code admin created for a location or site for users to use. Collected by the
    #: Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str]
    #: The device model type the user is using to make or receive the call.
    model: Optional[str]
    #: Indicates the time at which the call transfer service was invoked during the call. The invocation time is
    #: shown using the UTC/GMT time zone.
    call_transfer_time: Optional[datetime]


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

        def guess_datetime(dt: Union[datetime, str]) -> datetime:
            if isinstance(dt, str):
                r = isoparse(dt)
            else:
                r = dt_iso_str(dt)
            return r

        params['startTime'] = guess_datetime(start_time)
        params['endTime'] = guess_datetime(end_time)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')
