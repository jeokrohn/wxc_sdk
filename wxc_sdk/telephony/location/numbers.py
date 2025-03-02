from typing import Optional

from pydantic import Field

from ...api_child import ApiChild
from ...base import enum_str, ApiModel
from ...common import NumberState
from ...base import SafeEnum as Enum

__all__ = ['TelephoneNumberType', 'NumberUsageType', 'NumberAddError', 'NumberAddResponse', 'LocationNumbersApi']


class TelephoneNumberType(str, Enum):
    #: A toll-free PSTN number.
    tollfree = 'TOLLFREE'
    #: A normal Direct Inward Dial (DID) PSTN number.
    did = 'DID'
    #: A mobile number.
    mobile = 'MOBILE'


class NumberUsageType(str, Enum):
    #: Standard/user number usage (default).
    none_ = 'NONE'
    #: The number will be used in high-volume service, for example, Contact Center.
    service = 'SERVICE'


class NumberAddError(ApiModel):
    number: Optional[str] = None
    error_type: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    error_title: Optional[str] = None


class NumberAddResponse(ApiModel):
    errors: list[NumberAddError] = Field(default_factory=list)


class LocationNumbersApi(ApiChild, base='telephony/config/locations'):
    def _url(self, location_id: str, path: str = None):
        """

        :meta private:
        """
        path = path and f'/{path}' or ''
        return self.ep(f'{location_id}/numbers{path}')

    def add(self, location_id: str, phone_numbers: list[str], number_type: TelephoneNumberType = None,
            number_usage_type: NumberUsageType = None,
            state: NumberState = NumberState.inactive, subscription_id: str = None,
            org_id: str = None) -> NumberAddResponse:
        """
        Add Phone Numbers to a location

        Adds a specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        This API is only supported for adding DID and Toll-free numbers to non-integrated
        PSTN connection types such as Local Gateway (LGW) and Non-integrated CPP. It should never be used for
        locations with integrated PSTN connection types like Cisco Calling Plans or Integrated CCP because backend
        data issues may occur.

        Mobile numbers can be added to any location that has PSTN connection setup. Only
        20 mobile numbers can be added per request.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param number_type: Type of the number. Required for `MOBILE` number type.
        :type number_type: TelephoneNumberType
        :param number_usage_type: Type of usage expected for the number.
        :type number_usage_type: NumberUsageType
        :param state: Reflects the state of the number. By default, the state of a number is set to `ACTIVE` for DID
            and toll-free numbers only. Mobile numbers will be activated upon assignment to a user.
        :type state: NumberState
        :param subscription_id: Reflects the `subscriptionId` to be used for mobile number order.
        :type subscription_id: str
        :param org_id: Organization to manage.
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = dict()
        body['phoneNumbers'] = phone_numbers
        if number_type is not None:
            body['numberType'] = enum_str(number_type)
        if number_usage_type is not None:
            body['numberUsageType'] = enum_str(number_usage_type)
        if state is not None:
            body['state'] = enum_str(state)
        if subscription_id is not None:
            body['subscriptionId'] = subscription_id

        r = self.post(url=url, params=params, json=body)
        if isinstance(r, list):
            return NumberAddResponse.model_validate(r[0])
        return NumberAddResponse.model_validate({})

    def activate(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate Phone Numbers in a location

        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow the E.164 format. Active phone numbers are in service.

        A mobile number is activated when assigned to a user. This API will not activate mobile numbers.

        Activating a phone number in a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco Calling Plans or Integrated CCP because backend data issues may occur.

        :param location_id: LocationId in which numbers should be activated.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be activated.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        super().post(url, params=params, json=body)

    def remove(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove phone numbers from a location

        Remove the specified set of phone numbers from a location for an organization.

        Phone numbers must follow the E.164 format.

        Removing a mobile number may require more time depending on mobile carrier capabilities.

        Removing a phone number from a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        A location's main number cannot be removed.

        This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco Calling Plans or Integrated CCP because backend data issues may occur.

        :param location_id: LocationId from which numbers should be removed.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be removed.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        self.delete(url=url, params=params, json=body)
