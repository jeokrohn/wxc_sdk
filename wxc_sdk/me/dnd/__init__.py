from wxc_sdk.api_child import ApiChild

__all__ = ['MeDNDApi']

from wxc_sdk.person_settings.dnd import DND


class MeDNDApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> DND:
        """
        Get Do Not Disturb Settings for User

        Get Do Not Disturb settings for the authenticated user.

        Do Not Disturb (DND) enables users to block or silence incoming calls on their phone. When activated, the phone
        either stops ringing or rejects calls depending on the configured option, but users can still see call
        information and answer calls if desired.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`DND`
        """
        url = self.ep('settings/doNotDisturb')
        data = super().get(url)
        r = DND.model_validate(data)
        return r

    def configure(self, dnd_settings: DND):
        """
        Update Do Not Disturb Settings for User

        Update Do Not Disturb settings for the authenticated user.

        Do Not Disturb (DND) enables users to block or silence incoming calls on their phone. When activated, the phone
        either stops ringing or rejects calls depending on the configured option, but users can still see call
        information and answer calls if desired.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param dnd_settings: new setting to be applied
        :type dnd_settings: DND
        :rtype: None
        """
        body = dnd_settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep('settings/doNotDisturb')
        super().put(url, json=body)
