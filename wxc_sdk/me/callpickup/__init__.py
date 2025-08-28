from wxc_sdk.api_child import ApiChild
from wxc_sdk.common import MeGroupSettings

__all__ = ['MeCallPickupApi']


class MeCallPickupApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> MeGroupSettings:
        """
        Get My Call Pickup Group Settings

        Get Call Pickup Group Settings for the authenticated user.

        Call pickup group enables a user to answer any ringing line within their pickup group. A call pickup group is
        an administrator-defined set of users within a location, to which the call pickup feature applies.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeGroupSettings`
        """
        url = self.ep('settings/callPickupGroup')
        data = super().get(url)
        r = MeGroupSettings.model_validate(data)
        return r
