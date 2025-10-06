from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineVoicemailApi']

from wxc_sdk.person_settings.voicemail import VoicemailSettings


class MeSecondaryLineVoicemailApi(ApiChild, base='telephony/config/people/me'):
    def settings(self, lineowner_id: str) -> VoicemailSettings:
        """
        Get My Secondary Line Owner's Voicemail Settings

        GET voicemail settings for a secondary line of the authenticated user.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`VoicemailSettings`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/voicemail')
        data = super().get(url)
        r = VoicemailSettings.model_validate(data)
        return r

    def configure(self, lineowner_id: str, settings: VoicemailSettings):
        """
        Update My Secondary Line Owner's Voicemail Settings

        Update voicemail settings associated with a secondary line owner of the authenticated user.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param settings: Voicemail settings
        :type settings: VoicemailSettings
        :rtype: None
        """
        body = settings.update()
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/voicemail')
        super().put(url, json=body)
