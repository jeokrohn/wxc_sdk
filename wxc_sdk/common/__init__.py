"""
Common date types and APIs
"""

from enum import Enum
from typing import Optional

from pydantic import Field, root_validator

from wxc_sdk.base import ApiModel
from ..base import webex_id_to_uuid

__all__ = ['UserType', 'UserBase', 'RingPattern', 'AlternateNumber', 'Greeting', 'UserNumber', 'PersonPlaceAgent',
           'MonitoredMember', 'CallParkExtension', 'AuthCode', 'RouteType', 'DialPatternValidate', 'DialPatternStatus',
           'RouteIdentity', 'Customer', 'IdAndName', 'PatternAction', 'NumberState', 'ValidateExtensionResponseStatus',
           'ValidateExtensionStatusState', 'ValidateExtensionStatus', 'ValidateExtensionsResponse',
           'ValidatePhoneNumberStatusState', 'ValidatePhoneNumberStatus', 'ValidatePhoneNumbersResponse']


class UserType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'


class UserBase(ApiModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: Optional[UserType] = Field(alias='type')


class RingPattern(str, Enum):
    """
    Ring Pattern
    """
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumber(ApiModel):
    """
    Hunt group or call queue alternate number
    """
    #: Alternate phone number for the hunt group or call queue
    phone_number: Optional[str]
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: Optional[RingPattern]
    #: Flag: phone_number is a toll free number
    toll_free_number: Optional[bool]


class Greeting(str, Enum):
    """
    DEFAULT indicates that a system default message will be placed when incoming calls are intercepted.
    """
    #: A custom will be placed when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default message will be placed when incoming calls are intercepted.
    default = 'DEFAULT'


class UserNumber(ApiModel):
    """
    phone number of the person or workspace.
    """
    #: Phone number of person or workspace. Either phoneNumber or extension is mandatory
    external: Optional[str]
    #: Extension of person or workspace. Either phoneNumber or extension is mandatory.
    extension: Optional[str]
    #: Flag to indicate primary phone.
    primary: Optional[bool]


class PersonPlaceAgent(UserBase):
    """
    Agent (person or place)
    """
    #: ID of person or workspace.
    agent_id: str = Field(alias='id')
    #: Display name of person or workspace.
    display_name: Optional[str]
    #: Email of the person or workspace.
    email: Optional[str]
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumber]]


class MonitoredMember(ApiModel):
    """
    a monitored user or place
    """
    #: The identifier of the monitored person.
    member_id: Optional[str] = Field(alias='id')
    #: The last name of the monitored person or place.
    last_name: Optional[str]
    #: The first name of the monitored person or place.
    first_name: Optional[str]
    #: The display name of the monitored person or place.
    display_name: Optional[str]
    #: Indicates whether type is PEOPLE or PLACE.
    member_type: Optional[UserType] = Field(alias='type')
    #: The email address of the monitored person or place.
    email: Optional[str]
    #: The list of phone numbers of the monitored person or place.
    numbers: Optional[list[UserNumber]]

    @property
    def ci_member_id(self) -> Optional[str]:
        return self.member_id and webex_id_to_uuid(self.member_id)


class CallParkExtension(ApiModel):
    #: The identifier of the call park extension.
    cpe_id: Optional[str] = Field(alias='id')
    #: The name to describe the call park extension.
    name: Optional[str]
    #: The extension number for this call park extension.
    extension: Optional[str]
    #: The location name where the call park extension is.
    location_name: Optional[str]
    #: The location Id for the location.
    location_id: Optional[str]

    @root_validator(pre=True)
    def fix_location_name(cls, values):
        """

        :meta private:
        :param values:
        :return:
        """
        location = values.pop('location', None)
        if location is not None:
            values['location_name'] = location
        return values

    @property
    def ci_cpe_id(self) -> Optional[str]:
        """
        call park extension ID as UUID
        """
        return self.cpe_id and webex_id_to_uuid(self.cpe_id)


class AuthCode(ApiModel):
    """
    authorization codea and description.
    """
    #: Indicates an authorization code.
    code: str
    #: Indicates the description of the authorization code.
    description: str


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    # Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class DialPatternStatus(str, Enum):
    """
    validation status.
    """
    #: invalid pattern
    invalid = 'INVALID'
    #: duplicate pattern
    duplicate = 'DUPLICATE'
    #: duplicate in input
    duplicate_in_list = 'DUPLICATE_IN_LIST'


class DialPatternValidate(ApiModel):
    #: input dial pattern that is being validate
    dial_pattern: str
    #: validation status.
    pattern_status: DialPatternStatus
    #: failure details.
    message: str


class RouteIdentity(ApiModel):
    route_id: str = Field(alias='id')
    name: Optional[str]
    route_type: RouteType = Field(alias='type')


class Customer(ApiModel):
    """
    Customer information.
    """
    #: Id of the customer/organization.
    customer_id: str = Field(alias='id')
    #: Name of the customer/organization.
    name: str


class IdAndName(ApiModel):
    id: str
    name: str


class PatternAction(str, Enum):
    #: add action, when adding a new dial pattern
    add = 'ADD'
    #: delete action, when deleting an existing dial pattern
    delete = 'DELETE'


class NumberState(str, Enum):
    active = 'ACTIVE'
    inactive = 'INACTIVE'


class ValidateExtensionResponseStatus(str, Enum):
    ok = 'OK'
    errors = 'ERRORS'


class ValidateExtensionStatusState(str, Enum):
    valid = 'VALID'
    duplicate = 'DUPLICATE'
    duplicate_in_list = 'DUPLICATE_IN_LIST'
    invalid = 'INVALID'


class ValidateExtensionStatus(ApiModel):
    #: Indicates the extention Id for which the status is about .
    extension: str
    #: Indicate the status for the given extention id .
    state: ValidateExtensionStatusState
    #: Error Code .
    error_code: Optional[int]
    message: Optional[str]

    @property
    def ok(self):
        return self.state == ValidateExtensionStatusState.valid


class ValidateExtensionsResponse(ApiModel):
    status: ValidateExtensionResponseStatus
    extension_status: Optional[list[ValidateExtensionStatus]]

    @property
    def ok(self) -> bool:
        return self.status == ValidateExtensionResponseStatus.ok


class ValidatePhoneNumberStatusState(str, Enum):
    #: This means the phone number is available.
    available = 'Available'
    #: This means it's a duplicate phone number.
    duplicate = 'Duplicate'
    #: This means it's a duplicate phone number in the list.
    duplicate_in_list = 'Duplicate In List'
    #: The phone number is invalid.
    invalid = 'Invalid'
    #: This phone number is unavailable and cannot be used.
    unavailable = 'Unavailable'


class ValidatePhoneNumberStatus(ApiModel):
    #: Phone number that need to be validated.
    phone_number: str
    #: This indicates the state of the number.
    state: ValidatePhoneNumberStatusState
    #: This indicated whether it's a toll-free number
    toll_free_number: bool
    #: This field has the details if error if the number is unavailable.
    detail: list[str] = Field(default_factory=list)

    @property
    def ok(self):
        return self.state == ValidatePhoneNumberStatusState.available


class ValidatePhoneNumbersResponse(ApiModel):
    #: This indicates the status of the numbers.
    status: ValidateExtensionResponseStatus
    #: This is an array of number objects with number details.
    phone_numbers: Optional[list[ValidatePhoneNumberStatus]]

    @property
    def ok(self) -> bool:
        return self.status == ValidateExtensionResponseStatus.ok
