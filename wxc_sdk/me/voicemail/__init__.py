from wxc_sdk.api_child import ApiChild

__all__ = ['MeVoicemailApi']

from wxc_sdk.person_settings.voicemail import VoicemailSettings


class MeVoicemailApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> VoicemailSettings:
        """
        Read Voicemail Settings for a Person

        Retrieve a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_read`.

        :rtype: :class:`VoicemailSettings`
        """
        url = self.ep('settings/voicemail')
        data = super().get(url)
        r = VoicemailSettings.model_validate(data)
        return r

    def configure(self, settings: VoicemailSettings):
        """
        Configure Voicemail Settings for a Person

        Configure a person's voicemail settings.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via voicemail.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param settings: Voicemail settings
        :type settings: VoicemailSettings
        :rtype: None
        """
        body = settings.update()
        url = self.ep('settings/voicemail')
        super().put(url, json=body)
