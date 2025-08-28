from wxc_sdk.api_child import ApiChild
from wxc_sdk.common import MeGroupSettings

__all__ = ['MeSecondaryLineCallParkApi']


class MeSecondaryLineCallParkApi(ApiChild, base='telephony/config/people/me'):
    def settings(self, lineowner_id: str) -> MeGroupSettings:
        """
        Get My Secondary Line Owner Call Park Settings

        Get details of call park settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`MeGroupSettings`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callPark')
        data = super().get(url)
        r = MeGroupSettings.model_validate(data)
        return r
