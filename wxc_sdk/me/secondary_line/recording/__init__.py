from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineRecordingApi']

from wxc_sdk.me.recording import MeRecordingSettings


class MeSecondaryLineRecordingApi(ApiChild, base='telephony/config/people/me'):

    def settings(self, lineowner_id: str) -> MeRecordingSettings:
        """
        Get My Secondary Line Owner's Call Recording Settings

        Get details of call recording settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Call recording settings allow you to access and customize options that determine when and how your calls are
        recorded, providing control over recording modes and notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`MeRecordingSettings`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callRecording')
        data = super().get(url)
        r = MeRecordingSettings.model_validate(data)
        return r
