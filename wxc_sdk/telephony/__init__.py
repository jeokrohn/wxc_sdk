"""
Telephony types and API (location and organisation settings)
"""
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import Field, parse_obj_as

from .access_codes import AccessCodesApi
from .autoattendant import AutoAttendantApi
from .callpark import CallParkApi
from .callpark_extension import CallparkExtensionApi
from .callpickup import CallPickupApi
from .callqueue import CallQueueApi
from .calls import CallsApi
from .huntgroup import HuntGroupApi
from .location_intercept import LocationInterceptApi
from .location_moh import LocationMoHApi
from .location_vm import LocationVoicemailSettingsApi
from .organisation_vm import OrganisationVoicemailSettingsAPI
from .paging import PagingApi
from .pnc import PrivateNetworkConnectApi
from .vm_rules import VoicemailRulesApi
from .voicemail_groups import VoicemailGroupsApi
from .voiceportal import VoicePortalApi
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..common.schedules import ScheduleApi, ScheduleApiBase
from ..person_settings.permissions_out import OutgoingPermissionsApi
from ..rest import RestSession

__all__ = ['OwnerType', 'NumberLocation', 'NumberOwner', 'NumberState', 'NumberListPhoneNumberType',
           'NumberListPhoneNumber',
           'NumberType', 'NumberDetails', 'ValidateExtensionResponseStatus', 'ValidateExtensionStatus',
           'ValidateExtensionStatusState', 'ValidateExtensionsResponse', 'UCMProfile', 'TelephonyApi']


class OwnerType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    auto_attendant = 'AUTO_ATTENDANT'
    call_center = 'CALL_CENTER'
    group_paging = 'GROUP_PAGING'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    contact_center_link = 'CONTACT_CENTER_LINK'
    route_list = 'ROUTE_LIST'
    voicemail_group = 'VOICEMAIL_GROUP'


class NumberLocation(ApiModel):
    """
    Location of a phone number
    """
    #: ID of location for phone number.
    location_id: str = Field(alias='id')
    #: Name of the location for phone number
    name: str


class NumberOwner(ApiModel):
    """
    Owner of a phone number
    """
    #: ID of the owner to which PSTN Phone number is assigned.
    owner_id: Optional[str] = Field(alias='id')
    #: Type of the PSTN phone number's owner
    owner_type: Optional[OwnerType] = Field(alias='type')
    #: Last name of the PSTN phone number's owner
    last_name: Optional[str]
    #: First name of the PSTN phone number's owner
    first_name: Optional[str]


class NumberState(str, Enum):
    active = 'ACTIVE'
    inactive = 'INACTIVE'


class NumberListPhoneNumberType(str, Enum):
    primary = 'PRIMARY'
    alternate = 'ALTERNATE'


class NumberListPhoneNumber(ApiModel):
    """
    Phone Number
    """
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str]
    #: Extension for a PSTN phone number.
    extension: Optional[str]
    #: Phone number's state.
    state: Optional[NumberState]
    #: Type of phone number.
    phone_number_type: Optional[NumberListPhoneNumberType]
    #: Indicates if the phone number is used as location clid.
    main_number: bool
    #: Indicates if a phone number is a toll free number.
    toll_free_number: bool
    location: NumberLocation
    owner: Optional[NumberOwner]


class NumberType(str, Enum):
    extension = 'EXTENSION'
    number = 'NUMBER'


class NumberDetails(ApiModel):
    assigned: int
    un_assigned: int
    in_active: int
    extension_only: int
    toll_free_numbers: int
    total: int


class ValidateExtensionResponseStatus(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class ValidateExtensionStatusState(str, Enum):
    valid = 'VALID'
    duplicate = 'DUPLICATE'
    DUPLICATE_IN_LIST = 'DUPLICATE_IN_LIST'
    invalid = 'INVALID'


class ValidateExtensionStatus(ApiModel):
    #: Indicates the extention Id for which the status is about .
    extension: str
    #: Indicate the status for the given extention id .
    state: ValidateExtensionStatusState
    #: Error Code .
    error_code: Optional[int]
    message: Optional[str]


class ValidateExtensionsResponse(ApiModel):
    status: ValidateExtensionResponseStatus
    extension_status: Optional[list[ValidateExtensionStatus]]


class UCMProfile(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    profile_id: str = Field(alias='id')
    #: Unique name for the calling UC Manager Profile.
    name: str


@dataclass(init=False)
class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes
    access_codes: AccessCodesApi
    auto_attendant: AutoAttendantApi
    calls: CallsApi
    callpark: CallParkApi
    callpark_extension: CallparkExtensionApi
    callqueue: CallQueueApi
    huntgroup: HuntGroupApi
    location_intercept: LocationInterceptApi
    location_moh: LocationMoHApi
    #: Location VM settings (only enable/disable transcription for now)
    location_voicemail: LocationVoicemailSettingsApi
    #: organisation voicemail settings
    organisation_voicemail: OrganisationVoicemailSettingsAPI
    paging: PagingApi
    permissions_out: OutgoingPermissionsApi
    pickup: CallPickupApi
    pnc: PrivateNetworkConnectApi
    schedules: ScheduleApi
    voicemail_groups: VoicemailGroupsApi
    voicemail_rules: VoicemailRulesApi
    voiceportal: VoicePortalApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.access_codes = AccessCodesApi(session=session)
        self.auto_attendant = AutoAttendantApi(session=session)
        self.calls = CallsApi(session=session)
        self.callpark = CallParkApi(session=session)
        self.callpark_extension = CallparkExtensionApi(session=session)
        self.callqueue = CallQueueApi(session=session)
        self.huntgroup = HuntGroupApi(session=session)
        self.location_intercept = LocationInterceptApi(session=session)
        self.location_moh = LocationMoHApi(session=session)
        self.location_voicemail = LocationVoicemailSettingsApi(session=session)
        self.organisation_voicemail = OrganisationVoicemailSettingsAPI(session=session)
        self.paging = PagingApi(session=session)
        self.permissions_out = OutgoingPermissionsApi(session=session, locations=True)
        self.pickup = CallPickupApi(session=session)
        self.pnc = PrivateNetworkConnectApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.voicemail_groups = VoicemailGroupsApi(session=session)
        self.voicemail_rules = VoicemailRulesApi(session=session)
        self.voiceportal = VoicePortalApi(session=session)

    def phone_numbers(self, *, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> Generator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='config/numbers')
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')

    def phone_number_details(self, *, org_id: str = None) -> NumberDetails:
        """
        get summary (counts) of phone numbers

        :param org_id: detaild for numbers in this organization.
        :type org_id: str
        :return: phone number details
        :rtype: :class:`NumberDetails`
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        params['details'] = 'true'
        params['max'] = 1
        url = self.ep(path='config/numbers')
        data = self.get(url, params=params)
        return NumberDetails.parse_obj(data['count'])

    def validate_extensions(self, *, extensions: list[str]) -> ValidateExtensionsResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions. Retrieving this list requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param extensions: Array of Strings of ID of Extensions.
        :return:
        """
        url = self.ep(path='config/actions/validateExtensions/invoke')
        data = self.post(url, json={'extensions': extensions})
        return ValidateExtensionsResponse.parse_obj(data)

    def ucm_profiles(self, *, org_id: str = None) -> list[UCMProfile]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in
        Webex Teams (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the
        user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :return: list of :class:`UCMProfile`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(path='config/callingProfiles')
        data = self.get(url, params=params)
        return parse_obj_as(list[UCMProfile], data['callingProfiles'])

    def change_announcement_language(self, *, location_id: str, language_code: str, agent_enabled: bool = None,
                                     service_enabled: bool = None, org_id: str = None):
        """
        Change Announcement Language

        Change announcement language for the given location.

        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.

        Changing announcement language for the given location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param language_code: Language code.
        :type language_code: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'announcementLanguageCode': language_code}
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        url = self.session.ep(f'telephony/config/locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        self.put(url, json=body, params=params)
