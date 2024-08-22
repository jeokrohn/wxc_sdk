from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ConnectionOptionsResponse', 'ConnectionResponse', 'PSTNApi', 'PSTNServiceType', 'PSTNType']


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
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: The display name of the PSTN connection.
    #: example: Premises-based PSTN
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


class ConnectionResponse(ApiModel):
    #: A unique identifier for the connection.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUElDS1VQL1kyRnNiRkJwWTJ0MWNERT0
    id: Optional[str] = None
    #: The display name of the PSTN connection.
    #: example: Premises-based PSTN
    display_name: Optional[str] = None
    #: The PSTN services available for this connection.
    pstn_services: Optional[list[PSTNServiceType]] = None
    #: The PSTN connection type set for the location.
    pstn_connection_type: Optional[PSTNType] = None


class PSTNApi(ApiChild, base='telephony/pstn/locations'):
    """
    PSTN
    
    PSTN Location Connection Settings supports PSTN selection when creating a location or changing a PSTN type for a
    location. This is only supported for Local Gateway and Non-integrated CCP.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_pstn_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_pstn_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def retrieve_pstn_connection_options_for_a_location(self, location_id: str,
                                                        org_id: str = None) -> list[ConnectionOptionsResponse]:
        """
        Retrieve PSTN Connection Options for a Location

        Retrieve the list of PSTN connection options available for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_pstn_read`.

        :param location_id: Return the list of List PSTN location connection options for this location.
        :type location_id: str
        :param org_id: List PSTN location connection options for this organization.
        :type org_id: str
        :rtype: list[ConnectionOptionsResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/connectionOptions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ConnectionOptionsResponse]).validate_python(data['items'])
        return r

    def setup_pstn_connection_for_a_location(self, location_id: str, id: str = None, premise_route_type: str = None,
                                             premise_route_id: str = None, org_id: str = None):
        """
        Setup PSTN Connection for a Location

        Set up or update the PSTN connection details for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Setting up PSTN connection on a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_pstn_write`.

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
        url = self.ep(f'{location_id}/connection')
        super().put(url, params=params, json=body)

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
        url = self.ep(f'{location_id}/connection')
        data = super().get(url, params=params)
        r = ConnectionResponse.model_validate(data)
        return r
