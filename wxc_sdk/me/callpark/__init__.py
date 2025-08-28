from wxc_sdk.api_child import ApiChild
from wxc_sdk.common import MeGroupSettings

__all__ = ['MeCallParkApi']


class MeCallParkApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> MeGroupSettings:
        """
        Get My Call Park Settings

        Get details of call park settings associated with the authenticated user.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeGroupSettings`
        """
        url = self.ep('settings/callPark')
        data = super().get(url)
        r = MeGroupSettings.model_validate(data)
        return r
