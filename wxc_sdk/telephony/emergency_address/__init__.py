from typing import Optional, Union

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['EmergencyAddressApi', 'EmergencyAddress', 'AddressLookupError',
           'SuggestedEmergencyAddress']


class EmergencyAddress(ApiModel):
    #: Primary street information for the emergency address.
    address1: Optional[str] = None
    #: Apartment number or any other secondary information for the emergency address.
    address2: Optional[str] = None
    #: City for the emergency address.
    city: Optional[str] = None
    #: State or Province or Region for the emergency address.
    state: Optional[str] = None
    #: Postal code for the emergency address.
    postal_code: Optional[str] = None
    #: Country for the emergency address.
    country: Optional[str] = None

    def update(self) -> dict:
        """
        return data for update or create

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True, exclude_none=True)


class AddressLookupError(ApiModel):
    #: Error code.
    code: Optional[str] = None
    #: Error title.
    title: Optional[str] = None
    #: Detailed error message.
    detail: Optional[str] = None


class SuggestedEmergencyAddress(EmergencyAddress):
    #: Additional metadata for the emergency address.
    meta: Optional[dict] = None
    #: List of errors encountered during address validation. Returned only when the input address was corrected and a
    #: suggested address was provided. Each error describes a specific issue with the original input.
    errors: Optional[list[AddressLookupError]] = None

    def update(self) -> dict:
        """
        return data for update or create

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True, exclude_none=True,
                               exclude={'meta', 'errors'})


class EmergencyAddressApi(ApiChild, base='telephony/pstn'):
    """
    API to handle emergency address settings for a location

    """

    def add_to_location(self, location_id: str, address: Union[EmergencyAddress, SuggestedEmergencyAddress],
                        org_id: str = None) -> str:
        """
        Add an Emergency Address to a Location

        Adds a new emergency address to the specified location. On success, returns the unique identifier of the newly
        created emergency address.

        Emergency address settings allow the admin to configure or update the physical address associated with a phone
        number or a location.

        Adding emergency address to a location requires a full administrator auth token with scope of
        `spark-admin:telephony_pstn_write`.

        :param location_id: Location to which the emergency address will be added.
        :type location_id: str
        :param address: Emergency address to add.
        :type address: Union[EmergencyAddress, SuggestedEmergencyAddress]
        :param org_id: Adding emergency address for a location in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = address.update()
        url = self.ep(f'locations/{location_id}/emergencyAddress')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def lookup_for_location(self, location_id: str, address: Union[EmergencyAddress, SuggestedEmergencyAddress],
                            org_id: str = None) -> list[SuggestedEmergencyAddress]:
        """
        Emergency Address Lookup to Verify if Address is Valid

        Returns a suggested address. If the input address is valid and unchanged, no errors are returned. If the input
        address requires corrections, the response includes a suggested address along with error details.

        Emergency address settings allow the admin to configure or update the physical address associated with a phone
        number or a location.

        Emergency address lookup to verify if address is valid requires a full administrator auth token with scope of
        `spark-admin:telephony_pstn_read`.

        :param location_id: Emergency address lookup for this location.
        :type location_id: str
        :param address: Emergency address to lookup.
        :type address: Union[EmergencyAddress, SuggestedEmergencyAddress]
        :param org_id: Emergency address lookup for this organization.
        :type org_id: str
        :rtype: list[SuggestedEmergencyAddress]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = address.update()
        url = self.ep(f'locations/{location_id}/emergencyAddress/lookup')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[SuggestedEmergencyAddress]).validate_python(data['addresses'])
        return r

    def update_for_location(self, location_id: str, address_id: str,
                            address: Union[EmergencyAddress, SuggestedEmergencyAddress], org_id: str = None):
        """
        Update the Emergency Address of a Location

        Updates the emergency address of the specified location.

        Emergency address settings allow the admin to configure or update the physical address associated with a phone
        number or a location.

        Updating the emergency address of a location requires a full administrator auth token with scope of
        `spark-admin:telephony_pstn_write`.

        :param location_id: Location for which the emergency address will be updated.
        :type location_id: str
        :param address_id: Unique identifier for the emergency address that will be updated.
        :type address_id: str
        :param address: Emergency address to update.
        :type address: Union[EmergencyAddress, SuggestedEmergencyAddress]
        :param org_id: Updating the emergency address of a location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = address.update()
        url = self.ep(f'locations/{location_id}/emergencyAddresses/{address_id}')
        super().put(url, params=params, json=body)

    def update_for_phone_number(self, phone_number: str,
                                emergency_address: Union[EmergencyAddress, SuggestedEmergencyAddress] = None,
                                org_id: str = None):
        """
        Update the emergency address for a phone number.

        Emergency address settings allow the admin to configure or update the physical address associated with a phone
        number or a location.

        Updating the emergency address for a phone number requires a full administrator auth token with scope of
        `spark-admin:telephony_pstn_write`.

        :param phone_number: Update the emergency address for this phone number.
        :type phone_number: str
        :param emergency_address: Emergency address to update. Using an empty JSON object deletes the custom emergency
            address for the number and replaces it with the location's default emergency address.
        :type emergency_address: Union[EmergencyAddress, SuggestedEmergencyAddress]
        :param org_id: Update the emergency address of phone number in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if emergency_address is not None:
            body['emergencyAddress'] = emergency_address.update()
        url = self.ep(f'numbers/{phone_number}/emergencyAddress')
        super().put(url, params=params, json=body)
