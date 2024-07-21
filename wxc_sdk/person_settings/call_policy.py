from pydantic import TypeAdapter

from wxc_sdk.base import enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['CallPolicyApi', 'PrivacyOnRedirectedCalls']


class PrivacyOnRedirectedCalls(str, Enum):
    #: Connected line identification is not blocked on redirected calls.
    no_privacy = 'NO_PRIVACY'
    #: Connected line identification is blocked on redirected calls to external numbers.
    privacy_for_external_calls = 'PRIVACY_FOR_EXTERNAL_CALLS'
    #: Connected line identification is blocked on all redirected calls.
    privacy_for_all_calls = 'PRIVACY_FOR_ALL_CALLS'


class CallPolicyApi(PersonSettingsApiChild):
    """
    API for call policy settings.

    For now only used for workspaces
    """

    feature = 'callPolicies'

    def read(self, entity_id: str,
             org_id: str = None) -> PrivacyOnRedirectedCalls:
        """
        Read Call Policy Settings for an entity

        Retrieve Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope can be used to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: PrivacyOnRedirectedCalls
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = TypeAdapter(PrivacyOnRedirectedCalls).validate_python(data['connectedLineIdPrivacyOnRedirectedCalls'])
        return r

    def configure(self, entity_id: str,
                  connected_line_id_privacy_on_redirected_calls: PrivacyOnRedirectedCalls,
                  org_id: str = None):
        """
        Configure Call Policy Settings for an entity

        Configure Call Policies settings.

        The call policy feature enables administrator to configure call policy settings such as Connected Line
        Identification Privacy on Redirected Calls for a professional workspace.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope can be used to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param connected_line_id_privacy_on_redirected_calls: Specifies the connection type to be used.
        :type connected_line_id_privacy_on_redirected_calls: PrivacyOnRedirectedCalls
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)
