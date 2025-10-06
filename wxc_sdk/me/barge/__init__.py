from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.barge import BargeSettings

__all__ = ['MeBargeApi']


class MeBargeApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> BargeSettings:
        """
        Retrieve Barge-In Settings

        Retrieve Barge-In settings of the user.

        The Barge-In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge-In can be used across locations.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`BargeInInfo`
        """
        url = self.ep('settings/bargeIn')
        data = super().get(url)
        r = BargeSettings.model_validate(data)
        return r

    def configure(self, settings: BargeSettings):
        """
        Configure Barge-In Settings

        Configure person's Barge-In settings.

        The Barge-In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge-In can be used across locations.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Barge-In settings
        :type settings: :class:`BargeSettings`
        """
        body = settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep('settings/bargeIn')
        super().put(url, json=body)
