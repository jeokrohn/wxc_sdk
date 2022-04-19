"""
Telephony types and API
"""
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import Field

from .calls import CallsApi
from ..base import ApiModel, to_camel
from ..common.schedules import ScheduleApi, ScheduleApiBase
from .paging import PagingApi
from .huntgroup import HuntGroupApi
from .callqueue import CallQueueApi
from .callpark import CallParkApi
from .callpark_extension import CallparkExtensionApi
from .callpickup import CallPickupApi
from .autoattendant import AutoAttendantApi
from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['OwnerType', 'NumberLocation', 'NumberOwner', 'NumberState', 'NumberListPhoneNumberType',
           'NumberListPhoneNumber',
           'NumberType', 'NumberDetails', 'ValidateExtensionResponseStatus', 'ValidateExtensionStatus',
           'ValidateExtensionStatusState', 'ValidateExtensionsResponse', 'TelephonyApi']


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
    owner_type: str = Field(alias='type')
    #: Last name of the PSTN phone number's owner
    last_name: str
    #: First name of the PSTN phone number's owner
    first_name: str


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


@dataclass(init=False)
class TelephonyApi(ApiChild, base='telephony'):
    """
    The telephony settings (features) API.
    """
    auto_attendant: AutoAttendantApi
    calls: CallsApi
    callpark: CallParkApi
    callpark_extension: CallparkExtensionApi
    callqueue: CallQueueApi
    huntgroup: HuntGroupApi
    paging: PagingApi
    pickup: CallPickupApi
    schedules: ScheduleApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.auto_attendant = AutoAttendantApi(session=session)
        self.calls = CallsApi(session=session)
        self.callpark = CallParkApi(session=session)
        self.callpark_extension = CallparkExtensionApi(session=session)
        self.callqueue = CallQueueApi(session=session)
        self.huntgroup = HuntGroupApi(session=session)
        self.paging = PagingApi(session=session)
        self.pickup = CallPickupApi(session=session)
        self.schedules = ScheduleApi(session=session, base=ScheduleApiBase.locations)

    def phone_numbers(self, *, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None, phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> Generator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with Given Criterias.

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
                      if i and v is not None)
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='config/numbers')
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params, item_key='phoneNumbers')

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
