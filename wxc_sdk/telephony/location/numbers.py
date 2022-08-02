from ...api_child import ApiChild
from ...common import NumberState


class LocationNumbersApi(ApiChild, base='telephony/config/locations'):
    def _url(self, location_id: str, path: str = None):
        path = path and f'/{path}' or ''
        return self.ep(f'{location_id}/numbers{path}')

    def add(self, *, location_id: str, phone_numbers: list[str], state: NumberState = NumberState.inactive,
            org_id: str = None):
        """
        Adds specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param state: State of the phone numbers.
        :type state: :class:`wxc_sdk.common.NumberState`
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers,
                'state': state}
        self.post(url=url, params=params, json=body)

    def activate(self, *, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features.
        Phone numbers must follow E.164 format for all countries, except for the United States, which can also
        follow the National format. Active phone numbers are in service.

        Activating a phone number in a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

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
        self.put(url=url, params=params, json=body)

    def remove(self, *, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove the specified set of phone numbers from a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Removing a phone number from a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

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
