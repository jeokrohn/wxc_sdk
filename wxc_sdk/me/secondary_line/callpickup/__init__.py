from wxc_sdk.api_child import ApiChild
from wxc_sdk.common import MeGroupSettings

__all__ = ['MeSecondaryLineCallPickupApi']


class MeSecondaryLineCallPickupApi(ApiChild, base='telephony/config/people/me'):
    def settings(self, lineowner_id: str) -> MeGroupSettings:
        """
        Get My Secondary Line Owner Call Pickup Group Settings

        Get Call Pickup Group Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Call pickup group enables a user to answer any ringing line within their pickup group. A call pickup group is
        an administrator-defined set of users within a location, to which the call pickup feature applies.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`MeGroupSettings`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callPickupGroup')
        data = super().get(url)
        r = MeGroupSettings.model_validate(data)
        return r
