from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineCallCenterApi']

from wxc_sdk.me.callcenter import MeCallCenterSettings


class MeSecondaryLineCallCenterApi(ApiChild, base='telephony/config/people/me'):
    def settings(self, lineowner_id: str) -> MeCallCenterSettings:
        """
        Get My Secondary Line Owner's Call Center Settings

        Retrieves the call center settings and list of all call centers associated with a secondary line of the
        authenticated user.
        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        The secondary line must have the call center service assigned.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`MeCallCenterSettings`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/queues')
        data = super().get(url)
        r = MeCallCenterSettings.model_validate(data)
        return r

    def modify(self, lineowner_id: str, settings: MeCallCenterSettings):
        """
        Modify My Secondary Line Owner's Call Center Settings

        Modify the call center settings and availability for an agent in one or more call centers associated with a
        secondary line owner of the authenticated user.
        Note that an authenticated user can only modify information for their configured secondary lines.

        Calls from the Call Centers are routed to agents based on configuration. An agent can be assigned to one or
        more call queues and can be managed by supervisors.
        Contains a list specifying the desired availability status of one or more call centers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param settings: settings
        :type settings: :class:`MeCallCenterSettings`
        """
        body = settings.update()
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/queues')
        super().put(url, json=body)
