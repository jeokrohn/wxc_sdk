"""
Call Settings For Me

Call settings for me APIs allow a person to read or modify their settings.
"""
from dataclasses import dataclass
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import PrimaryOrShared, UserType
from wxc_sdk.locations import LocationAddress
from wxc_sdk.me.barge import MeBargeApi
from wxc_sdk.me.callblock import MeCallBlockApi
from wxc_sdk.me.callcenter import MeCallCenterApi
from wxc_sdk.me.callerid import MeCallerIdApi
from wxc_sdk.me.callpark import MeCallParkApi
from wxc_sdk.me.callpickup import MeCallPickupApi
from wxc_sdk.me.callpolicy import MeCallPoliciesApi
from wxc_sdk.me.dnd import MeDNDApi
from wxc_sdk.me.endpoints import MeEndpointsApi
from wxc_sdk.me.executive import MeExecutiveApi
from wxc_sdk.me.forwarding import MeForwardingApi
from wxc_sdk.me.go_override import GoOverrideApi
from wxc_sdk.me.personal_assistant import MePersonalAssistantApi
from wxc_sdk.me.recording import MeRecordingApi
from wxc_sdk.me.snr import MeSNRApi
from wxc_sdk.me.voicemail import MeVoicemailApi
from wxc_sdk.person_settings import DeviceActivationState, UserCallCaptions
from wxc_sdk.rest import RestSession

__all__ = ['MeSettingsApi', 'MeProfile', 'MeNumber', 'MeOwner', 'MeDevice',
           'LocationNameAddress', 'CountryTelephonyConfigRequirements',
           'FeatureAccessCode', 'MeMonitoringSettings', 'MeMonitoredElement', 'MonitoredElementType', 'ServicesEnum']

from wxc_sdk.telephony import AnnouncementLanguage, NameAndCode


class MeNumber(ApiModel):
    #: Direct number of the user.
    direct_number: Optional[str] = None
    #: Enterprise number of the user. This always combines the location routing prefix with the user's extension, and
    #: is only present when both are present. That is, the location has a routing prefix and the user has an
    #: extension.
    enterprise: Optional[str] = None
    #: Extension of the user. This is always the user's extension, only present if the user has an extension.
    extension: Optional[str] = None
    #: Routing prefix of the user.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Number. This combines the location routing prefix and extension when both are set, and
    #: only the extension when the location routing prefix is not set. if the extension is not set, the esn is not
    #: present.
    esn: Optional[str] = None
    #: Indicates if the number is primary or alternate number.
    primary: Optional[bool] = None
    state: Optional[str] = None


class MeOwner(ApiModel):
    #: First name of device owner.
    last_name: Optional[str] = None
    #: Last name of device owner.
    first_name: Optional[str] = None
    #: Enumeration that indicates if the member is of type PEOPLE or PLACE.
    type: Optional[UserType] = None


class MeDevice(ApiModel):
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of the device.
    mac: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of
    #: the device.
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[PrimaryOrShared] = None
    #: Owner of device..
    owner: Optional[MeOwner] = None
    #: Activation state of the device.
    activation_state: Optional[DeviceActivationState] = None


class LocationNameAddress(ApiModel):
    #: Name of the location.
    name: Optional[str] = None
    #: Address details for the location.
    address: Optional[LocationAddress] = None


class MeProfile(ApiModel):
    #: Unique identifier of the user.
    id: Optional[str] = None
    #: Last name of the user.
    last_name: Optional[str] = None
    #: First name of the user.
    first_name: Optional[str] = None
    #: The email addresses of the person.
    email: Optional[str] = None
    #: Language for announcements.
    announcement_language: Optional[str] = None
    #: Dialing code for the user's location.
    location_dialing_code: Optional[str] = None
    #: If `true`, the user supports mobility.
    support_mobility: Optional[bool] = None
    #: Emergency callback number for the user.
    emergency_call_back_number: Optional[str] = None
    #: List of numbers associated with the user.
    phone_numbers: Optional[list[MeNumber]] = None
    #: List of devices associated with the user.
    devices: Optional[list[MeDevice]] = None
    #: Location details for the user.
    location: Optional[LocationNameAddress] = None
    #: URL for the receptionist console.
    receptionist_url: Optional[str] = None
    #: URL for the calling host.
    calling_host_url: Optional[str] = None
    #: URL for the attendant console.
    attendant_console_url: Optional[str] = None


class CountryTelephonyConfigRequirements(ApiModel):
    #: If `stateRequired` should be a Mandatory field in UI
    state_required: Optional[bool] = None
    #: If `zipCodeRequired` should be a Mandatory field in UI
    zip_code_required: Optional[bool] = None
    states: Optional[list[NameAndCode]] = None
    #: List of supported timezones for the country.
    time_zones: Optional[list[str]] = None


class FeatureAccessCode(ApiModel):
    #: Feature Access Code name.
    name: Optional[str] = None
    #: Feature Access Code.
    code: Optional[str] = None
    #: Alternate Code for the Feature Access Code.
    alternate_code: Optional[str] = None


class MonitoredElementType(str, Enum):
    #: The monitored element is a user.
    people = 'PEOPLE'
    #: The monitored element is a workspace.
    place = 'PLACE'
    #: The monitored element is a virtual line.
    virtual_line = 'VIRTUAL_LINE'
    #: The monitored element is a call park extension.
    call_park_extension = 'CALL_PARK_EXTENSION'


class MeMonitoredElement(ApiModel):
    #: The identifier of the monitored person.
    id: Optional[str] = None
    #: The last name of the monitored person or virtual line.
    last_name: Optional[str] = None
    #: The first name of the monitored person or virtual line.
    first_name: Optional[str] = None
    #: The display name of the monitored place or call park extension.
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE`, `VIRTUAL_LINE` or `CALL_PARK_EXTENSION`.
    type: Optional[MonitoredElementType] = None
    #: The email address of the monitored person, place or virtual line.
    email: Optional[str] = None
    #: The list of phone numbers of the monitored person, place or virtual line.
    direct_number: Optional[str] = None
    #: The extension number for the person, place, virtual line or call park extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Enterprise Significant Numbers (Routing prefix + extension of a person, place, virtual line).
    esn: Optional[str] = None
    #: The location name where the monitored item is.
    location_name: Optional[str] = None
    #: The ID for the location.
    location_id: Optional[str] = None


class MeMonitoringSettings(ApiModel):
    #: Call park notification is enabled or disabled. Only applies to monitored users, workspaces, and virtual lines.
    #: Does not apply to call park extensions.
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[MeMonitoredElement]] = None


class ServicesEnum(str, Enum):
    #: When enabled, blocks all incoming calls from unidentified or blocked caller IDs.
    anonymous_call_rejection = 'Anonymous Call Rejection'
    #: Requires the user to enter a password before making a call.
    authentication = 'Authentication'
    #: Forwards all incoming calls to another number.
    call_forwarding_always = 'Call Forwarding Always'
    #: Forwards incoming calls to another number when the user is on another call.
    call_forwarding_busy = 'Call Forwarding Busy'
    #: Forwards incoming calls to another number when the user does not answer.
    call_forwarding_no_answer = 'Call Forwarding No Answer'
    #: Notifies the user of incoming calls.
    call_notify = 'Call Notify'
    #: Blocks the delivery of the user's caller ID to the recipient.
    calling_line_id_delivery_blocking = 'Calling Line ID Delivery Blocking'
    #: Blocks all incoming calls.
    do_not_disturb = 'Do Not Disturb'
    #: Allows the user to intercept another user's calls.
    intercept_user = 'Intercept User'
    #: Redials the last number called.
    last_number_redial = 'Last Number Redial'
    #: Alerts the user of incoming calls with a distinctive ring.
    priority_alert = 'Priority Alert'
    #: Returns the last call received.
    call_return = 'Call Return'
    #: Accepts only calls from a list of pre-approved numbers.
    selective_call_acceptance = 'Selective Call Acceptance'
    #: Forwards calls from a list of pre-approved numbers.
    call_forwarding_selective = 'Call Forwarding Selective'
    #: Rejects calls from a list of pre-approved numbers.
    selective_call_rejection = 'Selective Call Rejection'
    #: Rings multiple numbers at the same time.
    simultaneous_ring_personal = 'Simultaneous Ring Personal'
    #: Allows the user to access voicemail.
    voice_messaging_user = 'Voice Messaging User'
    #: Allows the user to have multiple numbers.
    alternate_numbers = 'Alternate Numbers'
    #: Allows the user to share a call appearance with another user.
    shared_call_appearance_35 = 'Shared Call Appearance 35'
    #: Allows the user to dial a number by pressing a single key.
    speed_dial_100 = 'Speed Dial 100'
    #: Allows the user to pick up a call directed to another user.
    directed_call_pickup = 'Directed Call Pickup'
    #: Allows the user to pick up a call directed to another user and join the call.
    directed_call_pickup_with_barge_in = 'Directed Call Pickup with Barge-in'
    #: Displays the caller's ID on the user's phone.
    external_calling_line_id_delivery = 'External Calling Line ID Delivery'
    #: Displays the caller's ID on the user's phone.
    internal_calling_line_id_delivery = 'Internal Calling Line ID Delivery'
    #: Alerts the user of incoming calls when they are on another call.
    call_waiting = 'Call Waiting'
    #: Prevents other users from barging in on the user's calls.
    barge_in_exempt = 'Barge-in Exempt'
    #: Allows the user to push a button to talk.
    push_to_talk = 'Push to Talk'
    #: Logs the user's call history.
    basic_call_logs = 'Basic Call Logs'
    #: Allows the user to host a hoteling session.
    hoteling_host = 'Hoteling Host'
    #: Allows the user to join a hoteling session.
    hoteling_guest = 'Hoteling Guest'
    #: Allows the user to have multiple calls at the same time.
    multiple_call_arrangement = 'Multiple Call Arrangement'
    #: Allows the user to monitor the status of another user's phone.
    busy_lamp_field = 'Busy Lamp Field'
    #: Allows the user to have a three-way call.
    three_way_call = 'Three-Way Call'
    #: Allows the user to transfer a call.
    call_transfer = 'Call Transfer'
    #: Allows the user to keep their number private.
    privacy = 'Privacy'
    #: Allows the user to send and receive faxes.
    fax_messaging = 'Fax Messaging'
    #: Allows the user to have an N-way call.
    n_way_call = 'N-Way Call'
    #: Forwards calls when the user is not reachable.
    call_forwarding_not_reachable = 'Call Forwarding Not Reachable'
    #: Displays the caller's ID on the user's phone.
    connected_line_identification_presentation = 'Connected Line Identification Presentation'
    #: Prevents the caller's ID from being displayed on the user's phone.
    connected_line_identification_restriction = 'Connected Line Identification Restriction'
    #: Allows the user to make calls from any phone.
    broad_works_anywhere = 'BroadWorks Anywhere'
    #: Allows the user to listen to music while on hold.
    music_on_hold_user = 'Music On Hold User'
    #: Allows the user to monitor a call center.
    call_center_monitoring = 'Call Center Monitoring'
    #: Allows the user to use BroadWorks Mobility.
    broad_works_mobility = 'BroadWorks Mobility'
    #: Allows the user to record calls.
    call_recording = 'Call Recording'
    #: Allows the user to have an executive assistant.
    executive = 'Executive'
    #: Allows the user to use client license 17.
    client_license_17 = 'Client License 17'
    #: Allows the user to use client license 18.
    client_license_18 = 'Client License 18'
    #: Allows the user to be a flexible seating guest.
    flexible_seating_guest = 'Flexible Seating Guest'
    #: Allows the user to have a personal assistant.
    personal_assistant = 'Personal Assistant'
    #: Allows the user to have a sequential ring.
    sequential_ring = 'Sequential Ring'
    #: Allows the user to block calls.
    call_block = 'Call Block'
    call_center_premium = 'Call Center - Premium'
    calling_name_retrieval = 'Calling Name Retrieval'
    executive_assistant = 'Executive-Assistant'


@dataclass(init=False, repr=False)
class MeSettingsApi(ApiChild, base='telephony/config/people/me'):
    """
    Call Settings For Me

    Call settings for me APIs allow a person to read or modify their settings.

    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.

    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """
    barge: MeBargeApi
    call_block: MeCallBlockApi
    call_center: MeCallCenterApi
    call_park: MeCallParkApi
    call_pickup: MeCallPickupApi
    call_policies: MeCallPoliciesApi
    caller_id: MeCallerIdApi
    dnd: MeDNDApi
    endpoints: MeEndpointsApi
    executive: MeExecutiveApi
    forwarding: MeForwardingApi
    go_override: GoOverrideApi
    personal_assistant: MePersonalAssistantApi
    recording: MeRecordingApi
    snr: MeSNRApi
    voicemail: MeVoicemailApi

    def __init__(self, session: RestSession):
        """

        :meta private:
        """
        super().__init__(session=session)
        self.barge = MeBargeApi(session=session)
        self.call_block = MeCallBlockApi(session=session)
        self.call_center = MeCallCenterApi(session=session)
        self.call_park = MeCallParkApi(session=session)
        self.call_pickup = MeCallPickupApi(session=session)
        self.call_policies = MeCallPoliciesApi(session=session)
        self.caller_id = MeCallerIdApi(session=session)
        self.dnd: MeDNDApi = MeDNDApi(session=session)
        self.endpoints = MeEndpointsApi(session=session)
        self.executive = MeExecutiveApi(session=session)
        self.forwarding = MeForwardingApi(session=session)
        self.go_override = GoOverrideApi(session=session)
        self.personal_assistant = MePersonalAssistantApi(session=session)
        self.recording = MeRecordingApi(session=session)
        self.snr = MeSNRApi(session=session)
        self.voicemail = MeVoicemailApi(session=session)

    def details(self) -> MeProfile:
        """
        Get My Own Details

        Get profile details for the authenticated user.

        Profile details include the user's name, email, location and calling details.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeProfile`
        """
        url = self.ep()
        data = super().get(url)
        r = MeProfile.model_validate(data)
        return r

    def announcement_languages(self) -> list[AnnouncementLanguage]:
        """
        Retrieve announcement languages for the authenticated user

        Retrieve the list of available announcement languages for the authenticated user's telephony configuration.

        Announcement languages determine the language used for system prompts and announcements during calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[AnnouncementLanguage]
        """
        url = self.ep('announcementLanguages')
        data = super().get(url)
        r = TypeAdapter(list[AnnouncementLanguage]).validate_python(data['languages'])
        return r

    def country_telephony_config_requirements(self,
                                              country_code: str) -> CountryTelephonyConfigRequirements:
        """
        Retrieve country-specific telephony configuration requirements

        Retrieve country-specific telephony configuration requirements for the authenticated user.

        Webex Calling supports multiple regions and time zones to validate and present the information using the local
        date and time, as well as localized dialing rules.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param country_code: The ISO country code for which configuration requirements are requested.
        :type country_code: str
        :rtype: :class:`CountryTelephonyConfigRequirements`
        """
        url = self.ep(f'countries/{country_code}')
        data = super().get(url)
        r = CountryTelephonyConfigRequirements.model_validate(data)
        return r

    def feature_access_codes(self) -> list[FeatureAccessCode]:
        """
        Get My Feature Access Codes

        Retrieve all Feature Access Codes configured for services that are assigned to the authenticated user. For each
        feature access code, the name and code are returned. If an alternate code is defined, it is also returned.

        Feature access codes (FACs), also known as star codes, give users access to advanced calling features.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[FeatureAccessCode]
        """
        url = self.ep('settings/featureAccessCode')
        data = super().get(url)
        r = TypeAdapter(list[FeatureAccessCode]).validate_python(data['featureAccessCodeList'])
        return r

    def monitoring_settings(self) -> MeMonitoringSettings:
        """
        Get My Monitoring Settings

        Retrieves the monitoring settings of the logged in person, which shows specified people, places, virtual lines
        or call park extensions that are being monitored.

        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeMonitoringSettings`
        """
        url = self.ep('settings/monitoring')
        data = super().get(url)
        r = MeMonitoringSettings.model_validate(data)
        return r

    def calling_services_list(self) -> list[ServicesEnum]:
        """
        Get My Calling Services List

        Retrieves the list of enabled calling services for the authenticated user.

        These services are designed to improve call handling and ensure that users can manage their communications
        effectively. They are commonly found in both personal and business telephony systems.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[ServicesEnum]
        """
        url = self.ep('settings/services')
        data = super().get(url)
        r = TypeAdapter(list[ServicesEnum]).validate_python(data['services'])
        return r

    def call_captions_settings(self) -> UserCallCaptions:
        """
        Get my call captions settings

        Retrieve the effective call captions settings of the authenticated user.

        **NOTE**: The call captions feature is not supported for Webex Calling Standard users or users assigned to
        locations in India.

        The call caption feature allows the customer to enable and manage closed captions and transcript functionality
        (rolling caption panel) in Webex Calling, without requiring the user to escalate the call to a meeting.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`UserCallCaptions`
        """
        url = self.ep('settings/callCaptions')
        data = super().get(url)
        r = UserCallCaptions.model_validate(data)
        return r
