from wxc_sdk.api_child import ApiChild

__all__ = ['MeCallWaitingApi', ]


class MeCallWaitingApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> bool:
        """
        Get Call Waiting Settings for User

        Get Call Waiting Settings for the authenticated user.

        Call Waiting allows a user to receive multiple calls simultaneously. When the user is on an active call, they
        can receive an incoming call and switch between the two calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: bool
        """
        url = self.ep('settings/callWaiting')
        data = super().get(url)
        r = data['enabled']
        return r

    def update(self, enabled: bool):
        """
        Modify Call Waiting Settings for User

        Update Call Waiting Settings for the authenticated user.

        Call Waiting allows a user to receive multiple calls simultaneously. When the user is on an active call, they
        can receive an incoming call and switch between the two calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Enable or disable Call Waiting for the user.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        url = self.ep('settings/callWaiting')
        super().put(url, json=body)
