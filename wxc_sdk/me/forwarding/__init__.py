from wxc_sdk.api_child import ApiChild

__all__ = ['MeForwardingApi']

from wxc_sdk.person_settings.forwarding import PersonForwardingSetting


class MeForwardingApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> PersonForwardingSetting:
        """
        Read My Call Forwarding Settings

        Read call forwarding settings associated with the authenticated user.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`PersonForwardingSetting`
        """
        url = self.ep('settings/callForwarding')
        data = super().get(url)
        r = PersonForwardingSetting.model_validate(data)
        return r

    def configure(self, forwarding: PersonForwardingSetting):
        """
        Configure My Call Forwarding Settings

        Update call forwarding settings associated with the authenticated user.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy - forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer - forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param forwarding: new forwarding settings
        :type forwarding: PersonForwardingSetting

        Example:

            .. code-block:: python

                api = self.api.me.forwarding

                forwarding = api.read()
                always = CallForwardingAlways(
                    enabled=True,
                    destination='9999',
                    destination_voicemail_enabled=True,
                    ring_reminder_enabled=True)
                forwarding.call_forwarding.always = always
                api.configure(forwarding=forwarding)
        """
        body = forwarding.update()
        url = self.ep('settings/callForwarding')
        super().put(url, json=body)
