from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AuthorizationCode', 'BetaOrganizationCallSettingsWithOutboundPermissionsApi']


class AuthorizationCode(ApiModel):
    #: Indicates an access code.
    #: example: 4856
    code: Optional[str] = None
    #: Indicates the description of the access code.
    #: example: Marketing's access code
    description: Optional[str] = None


class BetaOrganizationCallSettingsWithOutboundPermissionsApi(ApiChild, base='telephony/config/outgoingPermission/accessCodes'):
    """
    Beta Organization Call Settings with Outbound Permissions
    
    Viewing an organization requires a full, user or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

    def retrieve_access_codes_for_an_organization(self, code: list[str] = None, description: list[str] = None,
                                                  org_id: str = None,
                                                  **params) -> Generator[AuthorizationCode, None, None]:
        """
        Retrieve Access Codes for an Organization

        Retrieve the organization's access codes.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read

        :param code: Filter access code based on the comma-separated list provided in the `code` array.
        :type code: list[str]
        :param description: Filter access code based on the comma-separated list provided in the `description` array.
        :type description: list[str]
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :return: Generator yielding :class:`AuthorizationCode` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if code is not None:
            params['code'] = ','.join(code)
        if description is not None:
            params['description'] = ','.join(description)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=AuthorizationCode, item_key='accessCodes', params=params)

    def delete_outgoing_permission_access_code_for_an_organization(self, delete_codes: list[str], org_id: str = None):
        """
        Delete Outgoing Permission Access Code for an Organization

        Deletes the access code details for a particular organization and max limit is 10k per request.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['deleteCodes'] = delete_codes
        url = self.ep()
        super().put(url, params=params, json=body)

    def create_access_codes_for_an_organization(self, access_codes: list[AuthorizationCode], org_id: str = None):
        """
        Create Access Codes for an Organization

        Create new access codes for the organization and max limit is 10k per request.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param access_codes: Indicates the set of activation codes and description.
        :type access_codes: list[AuthorizationCode]
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['accessCodes'] = TypeAdapter(list[AuthorizationCode]).dump_python(access_codes, mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        super().post(url, params=params, json=body)
