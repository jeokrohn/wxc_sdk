"""
Private network connect API
"""
from enum import Enum

from pydantic import parse_obj_as

from ..api_child import ApiChild

__all__ = ['NetworkConnectionType', 'PrivateNetworkConnectApi']


class NetworkConnectionType(str, Enum):
    """
    Network Connection Type for the location.
    """
    #: Use public internet for the location's connection type.
    public_internet = 'PUBLIC_INTERNET'
    #: Use private network connect for the location's connection type.
    private_network = 'PRIVATE_NETWORK'


class PrivateNetworkConnectApi(ApiChild, base='telephony/config/locations'):
    """
    API for location private network connect API settings
    """

    def read(self, *, location_id: str, org_id: str = None) -> NetworkConnectionType:
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve network connection type for this organization.
        :type org_id: str
        :return: location PNC settings
        :rtype: NetworkConnectionType
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        data = self.get(url, params=params)
        return parse_obj_as(NetworkConnectionType, data['networkConnectionType'])

    def update(self, *, location_id: str, connection_type: NetworkConnectionType, org_id: str = None):
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Update network connection type for this location.
        :type location_id: str
        :param connection_type: Network Connection Type for the location.
        :type connection_type: NetworkConnectionType
        :param org_id: Update network connection type for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        body = {'networkConnectionType': connection_type.value}
        self.put(url, json=body, params=params)
