"""
Access codes API for locations

Use Access Codes to bypass the set permissions for all persons/workspaces at this location.
"""
import json
from typing import Union

from pydantic import parse_obj_as

from ..api_child import ApiChild
from ..common import AuthCode

__all__ = ['AccessCodesApi']


class AccessCodesApi(ApiChild, base='telephony/config/locations'):
    """
    Access codes API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/outgoingPermission/accessCodes}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/outgoingPermission/accessCodes{path}')
        return ep

    def read(self, *, location_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Get Location Access Code

        Retrieve access codes details for a customer location.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Retrieving access codes details requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: list of :class:`wxc_sdk.common.CallPark`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = self.get(url, params=params)
        return parse_obj_as(list[AuthCode], data['accessCodes'])

    def create(self, *, location_id: str, access_codes: list[AuthCode], org_id: str = None) -> list[AuthCode]:
        """
        Create access code in location

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode`
        :param org_id: Add new access code for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'accessCodes': [json.loads(ac.json()) for ac in access_codes]}
        self.post(url, json=body, params=params)

    def delete_codes(self, *, location_id: str, access_codes: list[Union[str, AuthCode]],
                     org_id: str = None) -> list[AuthCode]:
        """
        Delete Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param access_codes: access codes to delete
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode` or str
        :param org_id: Delete access codes from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        self.put(url, json=body, params=params)
