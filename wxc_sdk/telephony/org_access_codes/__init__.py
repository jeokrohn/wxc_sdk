from collections.abc import Generator
from typing import List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.common import AuthCode

__all__ = ['OrganisationAccessCodesApi']


class OrganisationAccessCodesApi(ApiChild, base='telephony/config/outgoingPermission/accessCodes'):
    """
    Viewing an organisation requires a full, user or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read.
    """

    def list(self, code: list[str] = None, description: list[str] = None, org_id: str = None,
             **params) -> Generator[AuthCode, None, None]:
        """
        Retrieve the organisation's access codes.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full, user or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read

        :param code: Filter access code based on the comma-separated list provided in the `code` array.
        :type code: list[str]
        :param description: Filter access code based on the comma-separated list provided in the `description` array.
        :type description: list[str]
        :param org_id: ID of the organisation. Only admin users of another organisation (such as partners) may use this
            parameter as the default is the same organisation as the token used to access the API.
        :type org_id: str
        :return: Generator yielding :class:`AuthCode` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if code is not None:
            params['code'] = ','.join(code)
        if description is not None:
            params['description'] = ','.join(description)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=AuthCode, params=params,
                                              item_key='accessCodes')

    def delete(self, delete_codes: List[str] = None,
               org_id: str = None):
        """
        Delete Outgoing Permission Access Code for an Organisation

        Deletes the access code details for a particular organisation and max limit is 10k per request.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organisation. Only admin users of another organisation (such as partners) may use this
            parameter as the default is the same organisation as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = dict()
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep()
        super().put(url, params=params, json=body)

    def create(self, access_codes: List[AuthCode], org_id: str = None):
        """
        Create Access Codes for an Organisation

        Create new access codes for the organisation and max limit is 10k per request.

        Access codes, also known as authorization codes, provide a mechanism to allow authorized users to enter a code
        to bypass outgoing or incoming calling permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param access_codes: Indicates the set of activation codes and description.
        :type access_codes: list[AuthCode]
        :param org_id: ID of the organisation. Only admin users of another organisation (such as partners) may use this
            parameter as the default is the same organisation as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = dict()
        body['accessCodes'] = [ac.create() for ac in access_codes]
        url = self.ep()
        super().post(url, params=params, json=body)
