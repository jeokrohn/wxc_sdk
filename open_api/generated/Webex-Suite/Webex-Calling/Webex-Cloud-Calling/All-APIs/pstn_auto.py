from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AddressLookupErrorObject', 'AllowedServiceTypesFromHydra', 'ConnectionOptionsResponse',
           'ConnectionResponse', 'EmergencyAddressObject', 'PSTNApi', 'PSTNServiceType', 'PSTNType',
           'PremiseRouteType', 'SuggestedEmergencyAddressObject']


class PSTNServiceType(str, Enum):
    #: PSTN service type for geographic numbers.
    geographic_numbers = 'GEOGRAPHIC_NUMBERS'
    #: PSTN service type for toll-free numbers.
    tollfree_numbers = 'TOLLFREE_NUMBERS'
    #: PSTN service type for business texting.
    business_texting = 'BUSINESS_TEXTING'
    #: PSTN service type for contact center services.
    contact_center = 'CONTACT_CENTER'
    #: PSTN service type for service numbers.
    service_numbers = 'SERVICE_NUMBERS'
    #: PSTN service type for non-geographic numbers.
    non_geographic_numbers = 'NON_GEOGRAPHIC_NUMBERS'
    #: PSTN service type for mobile numbers.
    mobile_numbers = 'MOBILE_NUMBERS'


class ConnectionOptionsResponse(ApiModel):
    #: A unique identifier for the connection.
    id: Optional[str] = None
    #: The display name of the PSTN connection.
    display_name: Optional[str] = None
    #: The PSTN services available for this connection.
    pstn_services: Optional[list[PSTNServiceType]] = None


class PSTNType(str, Enum):
    #: PSTN connection type for a premises-based connection.
    local_gateway = 'LOCAL_GATEWAY'
    #: PSTN connection type for a Non-Integrated Cloud Connected PSTN connection.
    non_integrated_ccp = 'NON_INTEGRATED_CCP'
    #: PSTN connection type for an Integrated Cloud Connected PSTN connection. Updating the location with this
    #: connection type is currently not supported using the API.
    integrated_ccp = 'INTEGRATED_CCP'
    #: PSTN connection type for a Cisco PSTN connection. Updating the location with this connection type is currently
    #: not supported using the API.
    cisco_pstn = 'CISCO_PSTN'


class PremiseRouteType(str, Enum):
    #: A route group has been selected for premises-based PSTN.
    route_group = 'ROUTE_GROUP'
    #: A trunk group has been selected for premises-based PSTN.
    trunk = 'TRUNK'


class ConnectionResponse(ApiModel):
    #: A unique identifier for the connection.
    id: Optional[str] = None
    #: The display name of the PSTN connection.
    display_name: Optional[str] = None
    #: The PSTN services available for this connection.
    pstn_services: Optional[list[PSTNServiceType]] = None
    #: The PSTN connection type set for the location.
    pstn_connection_type: Optional[PSTNType] = None
    #: Premise route type. This is required if connection type is LOCAL_GATEWAY.
    route_type: Optional[PremiseRouteType] = None
    #: Premise route ID. This refers to either a Trunk ID or a Route Group ID. This field is optional but required if
    #: the connection type is LOCAL_GATEWAY.
    route_id: Optional[str] = None


class AllowedServiceTypesFromHydra(str, Enum):
    #: PSTN service type for mobile numbers.
    mobile_numbers = 'MOBILE_NUMBERS'


class EmergencyAddressObject(ApiModel):
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


class AddressLookupErrorObject(ApiModel):
    #: Error code.
    code: Optional[str] = None
    #: Error title.
    title: Optional[str] = None
    #: Detailed error message.
    detail: Optional[str] = None


class SuggestedEmergencyAddressObject(ApiModel):
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
    #: Additional metadata for the emergency address.
    meta: Optional[dict] = None
    #: List of errors encountered during address validation. Returned only when the input address was corrected and a
    #: suggested address was provided. Each error describes a specific issue with the original input.
    errors: Optional[list[AddressLookupErrorObject]] = None


class PSTNApi(ApiChild, base='telephony/pstn'):
    """
    PSTN
    
    PSTN Location Connection Settings supports PSTN selection when creating a location or changing a PSTN type for a
    location. This is only supported for Local Gateway and Non-integrated CCP.
    
    PSTN Emergency Address APIs support reading and writing of Emergency Address settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_pstn_read`.
    
    Modifying these organization settings requires a full administrator auth token with scopes of
    `spark-admin:telephony_pstn_write` and `spark-admin:telephony_pstn_read`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def retrieve_pstn_connection_for_a_location(self, location_id: str, org_id: str = None) -> ConnectionResponse:
        """
        Retrieve PSTN Connection for a Location

        Retrieves the current configured PSTN connection details for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Retrieving the PSTN connection details for a location requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_pstn_read`.

        :param location_id: Retrieve PSTN location connection details for this location.
        :type location_id: str
        :param org_id: Retrieve PSTN location connection details for this organization.
        :type org_id: str
        :rtype: :class:`ConnectionResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/connection')
        data = super().get(url, params=params)
        r = ConnectionResponse.model_validate(data)
        return r

    def setup_pstn_connection_for_a_location(self, location_id: str, id: str = None, premise_route_type: str = None,
                                             premise_route_id: str = None, org_id: str = None):
        """
        Setup PSTN Connection for a Location

        Set up or update the PSTN connection details for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Setting up PSTN connection on a location requires a full administrator auth token with scopes of
        `spark-admin:telephony_pstn_write` and `spark-admin:telephony_pstn_read`.

        :param location_id: Setup PSTN location connection options for this location.
        :type location_id: str
        :param id: A unique identifier for the connection. This is required for non-integrated CCP.
        :type id: str
        :param premise_route_type: Premise route type. The possible types are TRUNK and ROUTE_GROUP. This is required
            for the local gateway.
        :type premise_route_type: str
        :param premise_route_id: Premise route ID. This refers to either a Trunk ID or a Route Group ID and is required
            for the local gateway.
        :type premise_route_id: str
        :param org_id: Setup PSTN location connection for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if id is not None:
            body['id'] = id
        if premise_route_type is not None:
            body['premiseRouteType'] = premise_route_type
        if premise_route_id is not None:
            body['premiseRouteId'] = premise_route_id
        url = self.ep(f'locations/{location_id}/connection')
        super().put(url, params=params, json=body)

    def retrieve_pstn_connection_options_for_a_location(self, location_id: str,
                                                        service_types: list[AllowedServiceTypesFromHydra] = None,
                                                        org_id: str = None) -> list[ConnectionOptionsResponse]:
        """
        Retrieve PSTN Connection Options for a Location

        Retrieve the list of PSTN connection options available for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_pstn_read`.

        :param location_id: Return the list of List PSTN location connection options for this location.
        :type location_id: str
        :param service_types: Use the `serviceTypes` parameter to fetch connections for the following services
        * `MOBILE_NUMBERS`
        :type service_types: list[AllowedServiceTypesFromHydra]
        :param org_id: List PSTN location connection options for this organization.
        :type org_id: str
        :rtype: list[ConnectionOptionsResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if service_types is not None:
            params['serviceTypes'] = service_types
        url = self.ep(f'locations/{location_id}/connectionOptions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ConnectionOptionsResponse]).validate_python(data['items'])
        return r

    def add_emergency_address_to_location(self, location_id: str, address1: str = None, address2: str = None,
                                          city: str = None, state: str = None, postal_code: str = None,
                                          country: str = None, org_id: str = None) -> str:
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
        :param address1: Primary street information for the emergency address.
        :type address1: str
        :param address2: Apartment number or any other secondary information for the emergency address.
        :type address2: str
        :param city: City for the emergency address.
        :type city: str
        :param state: State or Province or Region for the emergency address.
        :type state: str
        :param postal_code: Postal code for the emergency address.
        :type postal_code: str
        :param country: Country for the emergency address.
        :type country: str
        :param org_id: Adding emergency address for a location in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if address1 is not None:
            body['address1'] = address1
        if address2 is not None:
            body['address2'] = address2
        if city is not None:
            body['city'] = city
        if state is not None:
            body['state'] = state
        if postal_code is not None:
            body['postalCode'] = postal_code
        if country is not None:
            body['country'] = country
        url = self.ep(f'locations/{location_id}/emergencyAddress')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def emergency_address_lookup(self, location_id: str, address1: str = None, address2: str = None, city: str = None,
                                 state: str = None, postal_code: str = None, country: str = None,
                                 org_id: str = None) -> list[SuggestedEmergencyAddressObject]:
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
        :param address1: Primary street information for the emergency address.
        :type address1: str
        :param address2: Apartment number or any other secondary information for the emergency address.
        :type address2: str
        :param city: City for the emergency address.
        :type city: str
        :param state: State or Province or Region for the emergency address.
        :type state: str
        :param postal_code: Postal code for the emergency address.
        :type postal_code: str
        :param country: Country for the emergency address.
        :type country: str
        :param org_id: Emergency address lookup for this organization.
        :type org_id: str
        :rtype: list[SuggestedEmergencyAddressObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if address1 is not None:
            body['address1'] = address1
        if address2 is not None:
            body['address2'] = address2
        if city is not None:
            body['city'] = city
        if state is not None:
            body['state'] = state
        if postal_code is not None:
            body['postalCode'] = postal_code
        if country is not None:
            body['country'] = country
        url = self.ep(f'locations/{location_id}/emergencyAddress/lookup')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[SuggestedEmergencyAddressObject]).validate_python(data['addresses'])
        return r

    def update_emergency_address_of_location(self, location_id: str, address_id: str, address1: str = None,
                                             address2: str = None, city: str = None, state: str = None,
                                             postal_code: str = None, country: str = None, org_id: str = None):
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
        :param address1: Primary street information for the emergency address.
        :type address1: str
        :param address2: Apartment number or any other secondary information for the emergency address.
        :type address2: str
        :param city: City for the emergency address.
        :type city: str
        :param state: State or Province or Region for the emergency address.
        :type state: str
        :param postal_code: Postal code for the emergency address.
        :type postal_code: str
        :param country: Country for the emergency address.
        :type country: str
        :param org_id: Updating the emergency address of a location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if address1 is not None:
            body['address1'] = address1
        if address2 is not None:
            body['address2'] = address2
        if city is not None:
            body['city'] = city
        if state is not None:
            body['state'] = state
        if postal_code is not None:
            body['postalCode'] = postal_code
        if country is not None:
            body['country'] = country
        url = self.ep(f'locations/{location_id}/emergencyAddresses/{address_id}')
        super().put(url, params=params, json=body)

    def update_emergency_address_for_phone_number(self, phone_number: str,
                                                  emergency_address: EmergencyAddressObject = None,
                                                  org_id: str = None):
        """
        Update the emergency address for a phone number.

        Emergency address settings allow the admin to configure or update the physical address associated with a phone
        number or a location.

        Updating the emergency address for a phone number requires a full administrator auth token with scope of
        `spark-admin:telephony_pstn_write`.

        :param phone_number: Update the emergency address for this phone number.
        :type phone_number: str
        :type emergency_address: EmergencyAddressObject
        :param org_id: Update the emergency address of phone number in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if emergency_address is not None:
            body['emergencyAddress'] = emergency_address.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'numbers/{phone_number}/emergencyAddress')
        super().put(url, params=params, json=body)
