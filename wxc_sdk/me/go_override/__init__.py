from wxc_sdk.api_child import ApiChild


class GoOverrideApi(ApiChild, base='telephony/config/people/me/settings/webexGoOverride'):

    def get(self) -> bool:
        """
        Get My WebexGoOverride Settings

        Retrieve "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with `spark:telephony_config_read` scope.

        :rtype: bool
        """
        url = self.ep()
        data = super().get(url)
        r = data['enabled']
        return r

    def update(self, enabled: bool = None):
        """
        Update My WebexGoOverride Settings

        Update "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with the `spark:telephony_config_write` scope.

        :param enabled: True if the "Mobile User Aware" override setting for Do Not Disturb feature is enabled.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep()
        super().put(url, json=body)
