from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.personal_assistant import PersonalAssistant


class MePersonalAssistantApi(ApiChild, base='telephony/config/people/me/settings/personalAssistant'):
    """
    Personal Assistant Settings For Me

    Call settings for me APIs allow a person to read or modify their settings.

    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.

    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """
    def get(self) -> PersonalAssistant:
        """
        Get My Personal Assistant

        Retrieve user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Retrieving Personal Assistant details requires a user auth token with `spark:telephony_config_read`.

        :rtype: :class:`PersonalAssistant`
        """
        url = self.ep()
        data = super().get(url)
        r = PersonalAssistant.model_validate(data)
        return r

    def update(self, settings: PersonalAssistant):
        """
        Update My Personal Assistant

        Update user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a auth token with the `spark:telephony_config_write`.

        :param settings: Personal Assistant settings.
        :type settings: PersonalAssistant
        :rtype: None
        """
        body = settings.model_dump(mode='json', exclude_unset=True, by_alias=True)
        url = self.ep()
        super().put(url, json=body)