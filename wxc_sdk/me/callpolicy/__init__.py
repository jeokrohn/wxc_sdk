from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['MeCallPoliciesApi']

from wxc_sdk.base import enum_str
from wxc_sdk.person_settings.call_policy import PrivacyOnRedirectedCalls


class MeCallPoliciesApi(ApiChild, base='telephony/config/people/me'):

    def settings(self) -> PrivacyOnRedirectedCalls:
        """
        Get Call Policies Settings for User

        Get call policies settings for the authenticated user.

        Call Policies in Webex allow you to manage how your call information is displayed and handled. You can view
        privacy settings for your connected line ID on redirected calls and review other call-related preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        """
        url = self.ep('settings/callPolicies')
        data = super().get(url)
        r = TypeAdapter(PrivacyOnRedirectedCalls).validate_python(data['connectedLineIdPrivacyOnRedirectedCalls'])
        return r

    def update(self, connected_line_id_privacy_on_redirected_calls: PrivacyOnRedirectedCalls = None):
        """
        Modify Call Policies Settings for User

        Update call policies settings for the authenticated user.

        Call Policies in Webex allow you to manage how your call information is displayed and handled. You can
        configure privacy settings for your connected line ID on redirected calls and control other call-related
        preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param connected_line_id_privacy_on_redirected_calls:

            * `NO_PRIVACY` - Caller sees the final destination's identity when call is redirected.
            * `PRIVACY_FOR_EXTERNAL_CALLS` - Internal callers see the final destination's identity; external callers
              see the original recipient's identity.
            * `PRIVACY_FOR_ALL_CALLS` - All callers see the original recipient's identity when call is redirected
        :type connected_line_id_privacy_on_redirected_calls: UserCallPoliciesGetConnectedLineIdPrivacyOnRedirectedCalls
        :rtype: None
        """
        body = dict()
        if connected_line_id_privacy_on_redirected_calls is not None:
            body['connectedLineIdPrivacyOnRedirectedCalls'] = enum_str(connected_line_id_privacy_on_redirected_calls)
        url = self.ep('settings/callPolicies')
        super().put(url, json=body)
