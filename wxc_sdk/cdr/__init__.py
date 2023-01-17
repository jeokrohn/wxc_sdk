"""
CDR API
"""
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Union

from dateutil import tz
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
    call_park = 'CallPark'  # TODO: missing in documentation on developer.webex.com
    call_park_retrieve = 'CallParkRetrieve'  # TODO: missing in documentation on developer.webex.com
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
    voice_xml = 'VoiceXML'
    route_point = 'RoutePoint'


class CDR(ApiModel):

    @root_validator(pre=True)
    def force_none(cls, values: dict):
        """
        Pop all empty strings so that they get caught by Optional[]
        :param values:
        :return:
        """
        empty_attrs = [k for k, v in values.items() if v == '' and k.endswith('time')]
        for k in empty_attrs:
            values.pop(k)
        return values

    #: The time the call was answered. Time is in UTC.
    answer_time: Optional[datetime] = Field(alias='Answer time')
    #: Whether the call leg was answered. For example, in a hunt group case, some legs will be unanswered,
    # and one will be answered.
    answered: Optional[bool] = Field(alias='Answered')
    #: Whether the call was inbound or outbound. The possible values are:
    direction: Optional[Union[CDRDirection, str]] = Field(alias='Direction')
    #: For incoming calls, the calling line ID of the user. For outgoing calls, it's the calling line ID of the
    #: called party.
    called_line_id: Optional[str] = Field(alias='Called line ID')
    #: SIP Call ID used to identify the call. You can share the Call ID with Cisco TAC to help them pinpoint a call
    # if necessary.
    call_id: Optional[str] = Field(alias='Call ID')
    #: For incoming calls, the calling line ID of the calling party. For outgoing calls, it's the calling line ID of
    # the user.
    calling_line_id: Optional[str] = Field(alias='Calling line ID')
    #: This is the start time of the call, the answer time may be slightly after this. Time is in UTC.
    start_time: Optional[datetime] = Field(alias='Start time')
    #: Type of call. For example:
    call_type: Optional[Union[CDRCallType, str]] = Field(alias='Call type')
    #: The type of client that the user (creating this record) is using to make or receive the call. For example:
    client_type: Optional[Union[CDRClientType, str]] = Field(alias='Client type')
    #: The version of the client that the user (creating this record) is using to make or receive the call.
    client_version: Optional[str] = Field(alias='Client version')
    #: Correlation ID to tie together multiple call legs of the same call session.
    correlation_id: Optional[str] = Field(alias='Correlation ID')
    #: The country code of the dialed number. This is only populated for international calls.
    international_country: Optional[str] = Field(alias='International country')
    #: The MAC address of the device, if known.
    device_mac: Optional[str] = Field(alias='Device MAC')
    #: The length of the call in seconds.
    duration: Optional[int] = Field(alias='Duration')
    #: Inbound trunk may be presented in Originating and Terminating records.
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk')
    #: A unique identifier for the organization that made the call. This is a unique identifier across Cisco.
    org_uuid: Optional[str] = Field(alias='Org UUID')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    original_reason: Optional[Union[CDROriginalReason, str]] = Field(alias='Original reason')
    #: The operating system that the app was running on, if available.
    os_type: Optional[str] = Field(alias='OS type')
    #: Outbound trunk may be presented in Originating and Terminating records.
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    redirect_reason: Optional[Union[CDRRedirectReason, str]] = Field(alias='Redirect reason')
    #: Populated for calls that transfer, hold, wait, and so on. For example:
    related_reason: Optional[Union[CDRRelatedReason, str]] = Field(alias='Related reason')
    #: A unique ID for this particular record. This can be used when processing records to aid in deduplication.
    report_id: Optional[str] = Field(alias='Report ID')
    #: The time this report was created. Time is in UTC.
    report_time: Optional[datetime] = Field(alias='Report time')
    #: If present, this field's only reported in Originating records. Route group identifies the route group used for
    #: outbound calls routed via a route group to Premises-based PSTN or an on-prem deployment integrated with Webex
    #: Calling (dial plan or unknown extension).
    route_group: Optional[str] = Field(alias='Route group')
    #: The main number for the user's site where the call was made or received.
    site_main_number: Optional[str] = Field(alias='Site main number')
    #: Site timezone is the offset in minutes from UTC time of the user's timezone.
    site_timezone: Optional[str] = Field(alias='Site timezone')
    #: If the call is TO or FROM a mobile phone using Webex Go, the Client type will show SIP, and Sub client type
    #: will show MOBILE_NETWORK.
    sub_client_type: Optional[str] = Field(alias='Sub client type')
    #: A unique identifier for the user associated with the call. This is a unique identifier across Cisco products.
    user_uuid: Optional[str] = Field(alias='User UUID')
    #: The type of user (user or workspace) that made or received the call. For example:
    user_type: Optional[Union[CDRUserType, str]] = Field(alias='User type')
    #: For incoming calls, the telephone number of the user. For outgoing calls, it's the telephone number of the
    #: called party.
    called_number: Optional[str] = Field(alias='Called number')
    #: For incoming calls, the telephone number of the calling party. For outgoing calls, it's the telephone number
    #: of the user.
    calling_number: Optional[str] = Field(alias='Calling number')
    #: Location of the report.
    location: Optional[str] = Field(alias='Location')
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
    dialed_digits: Optional[str] = Field(alias='Dialed digits')
    #: Indicates which party released the call first. The possible values are:
    #:
    #: Local: Used when the local user has released the call first.
    #: Remote: Used when the far end party releases the call first.
    #: Unknown: Used when the call has partial information or is unable to gather enough information about the party
    #: who released the call. It could be because of situations like force lock or because of a session audit failure.
    releasing_party: Optional[str] = Field(alias='Releasing party')
    #: When the call has been redirected one or more times, this field reports the last redirecting number.
    #: Identifies who last redirected the call. Only applies to call scenarios such as transfer, call forwarded calls,
    #: simultaneous rings, etc.
    redirecting_number: Optional[str] = Field(alias='Redirecting number')
    #: A unique identifier for the site associated with the call. Unique across Cisco products.
    site_uuid: Optional[str] = Field(alias='Site UUID')
    #: A unique identifier for the user's department name.
    department_id: Optional[str] = Field(alias='Department ID')
    #: Transfer related call ID is used as a call identifier of the other call involved in the transfer. You can share
    #: this ID with Cisco TAC to help them pinpoint parties who are involved during a call transfer.
    transfer_related_call_id: Optional[str] = Field(alias='Transfer related call ID')
    #: The authorization code admin created for a location or site for users to use. Collected by the
    #: Account/Authorization Codes or Enhanced Outgoing Calling Plan services.
    authorization_code: Optional[str] = Field(alias='Authorization code')
    #: The device model type the user is using to make or receive the call.
    model: Optional[str] = Field(alias='Model')


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

    def get_cdr_history(self, start_time: datetime = None, end_time: datetime = None, locations: list[str] = None,
                        **params) -> Generator[CDR, None, None]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
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

        params['startTime'] = dt_iso_str(start_time)
        params['endTime'] = dt_iso_str(end_time)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')
