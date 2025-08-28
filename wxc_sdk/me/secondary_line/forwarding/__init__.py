from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineForwardingApi']

from wxc_sdk.person_settings.forwarding import PersonForwardingSetting


class MeSecondaryLineForwardingApi(ApiChild, base='telephony/config/people/me'):
    def settings(self, lineowner_id: str) -> PersonForwardingSetting:
        """
        Get My Secondary Line Owner's Call Forwarding Settings

        Get details of call forwarding settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`PersonForwardingSetting`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callForwarding')
        data = super().get(url)
        r = PersonForwardingSetting.model_validate(data)
        return r

    def configure(self, lineowner_id: str, forwarding: PersonForwardingSetting):
        """
        Update My Secondary Line Owner's Call Forwarding Settings

        Update call forwarding settings associated with a secondary line owner of the authenticated user.

        Note that an authenticated user can only modify information for their configured secondary lines.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str:param forwarding: new forwarding settings
        :type forwarding: PersonForwardingSetting
        """
        body = forwarding.update()
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callForwarding')
        super().put(url, json=body)
