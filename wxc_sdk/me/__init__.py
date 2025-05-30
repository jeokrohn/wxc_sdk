from dataclasses import dataclass

from wxc_sdk.rest import RestSession
from wxc_sdk.api_child import ApiChild
from wxc_sdk.me.personal_assistant import MePersonalAssistantApi


@dataclass(init=False, repr=False)
class MeSettingsApi(ApiChild, base='people'):
    """
    Call Settings For Me

    Call settings for me APIs allow a person to read or modify their settings.

    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.

    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """

    personal_assistant: MePersonalAssistantApi

    def __init__(self, session: RestSession):
        """

        :meta private:
        """
        super().__init__(session=session)
        self.personal_assistant = MePersonalAssistantApi(session=session)
