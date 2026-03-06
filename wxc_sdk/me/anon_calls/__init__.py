from wxc_sdk.api_child import ApiChild

__all__ = ['MeAnonCallsApi']


class MeAnonCallsApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> bool:
        """
        Get Anonymous Call Rejection Settings for User

        Get Anonymous Call Rejection Settings for the authenticated user.

        Anonymous Call Rejection allows you to reject calls from anonymous callers.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: bool
        """
        url = self.ep('settings/anonymousCallReject')
        data = super().get(url)
        r = data['enabled']
        return r

    def modify(self, enabled: bool):
        """
        Modify Anonymous Call Rejection Settings for User

        Update Anonymous Call Rejection Settings for the authenticated user.

        Anonymous Call Rejection allows you to reject calls from anonymous callers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether Anonymous Call Rejection is enabled or not.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        url = self.ep('settings/anonymousCallReject')
        super().put(url, json=body)
