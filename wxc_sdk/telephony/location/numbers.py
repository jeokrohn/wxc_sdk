from ...api_child import ApiChild
from ...base import enum_str
from ...common import NumberState
from ...base import SafeEnum as Enum

__all__ = ['TelephoneNumberType', 'LocationNumbersApi']


class TelephoneNumberType(str, Enum):
    #: Indicates a toll-free PSTN number.
    tollfree = 'TOLLFREE'
    #: Indicates a normal Direct Inward Dial (DID) PSTN number.
    did = 'DID'


class LocationNumbersApi(ApiChild, base='telephony/config/locations'):
    def _url(self, location_id: str, path: str = None):
        """

        :meta private:
        """
        path = path and f'/{path}' or ''
        return self.ep(f'{location_id}/numbers{path}')

    def add(self, location_id: str, phone_numbers: list[str], number_type: TelephoneNumberType = None,
            state: NumberState = NumberState.inactive, org_id: str = None):
        """
        Adds a specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        WARNING: This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco PSTN or Integrated CCP because backend data issues may occur.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param number_type: Type of the number.
        :type number_type: TelephoneNumberType
        :param state: State of the phone numbers.
        :type state: :class:`wxc_sdk.common.NumberState`
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = dict()
        body['phoneNumbers'] = phone_numbers
        if number_type is not None:
            body['numberType'] = enum_str(number_type)
        if state is not None:
            body['state'] = enum_str(state)

        self.post(url=url, params=params, json=body)

    def activate(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features.
        Phone numbers must follow E.164 format for all countries, except for the United States, which can also
        follow the National format. Active phone numbers are in service.

        Activating a phone number in a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        WARNING: This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco PSTN or Integrated CCP because backend data issues may occur.

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
        Remove the specified set of phone numbers from a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Removing a phone number from a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        WARNING: This API is only supported for non-integrated PSTN connection types of Local
        Gateway (LGW) and Non-integrated CPP. It should never be used for locations with integrated PSTN connection
        types like Cisco PSTN or Integrated CCP because backend data issues may occur.

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
