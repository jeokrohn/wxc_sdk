from typing import Optional

from wxc_sdk.api_child import ApiChild

__all__ = ['MeRecordingApi', 'MeRecordingSettings', 'MeRecordingVendor']

from wxc_sdk.base import ApiModel
from wxc_sdk.person_settings.call_recording import Record, NotificationType


class MeRecordingVendor(ApiModel):
    #: Unique identifier of a vendor.
    id: Optional[str] = None
    #: Name of a call recording vendor.
    name: Optional[str] = None
    #: Login URL of the vendor.
    login_url: Optional[str] = None


class MeRecordingSettings(ApiModel):
    #: Indicates whether Call Recording is enabled for the user or not.
    enabled: Optional[bool] = None
    #: List of available vendors and their details.
    vendor: Optional[MeRecordingVendor] = None
    recording_mode: Optional[Record] = None
    pause_resume_notify_method: Optional[NotificationType] = None
    #: If `true`, an announcement is played when call recording starts.
    announcement_enabled: Optional[bool] = None
    #: If `true`, a warning tone is played when call recording starts.
    warning_tone_enabled: Optional[bool] = None
    #: Duration of the warning tone in seconds. Duration can be configured between 10 and 1800 seconds.
    warning_tone_duration: Optional[int] = None


class MeRecordingApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> MeRecordingSettings:
        """
        Get My Call Recording Settings

        Get details of call recording settings associated with the authenticated user.

        Call recording settings allow you to access and customize options that determine when and how your calls are
        recorded, providing control over recording modes and notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeRecordingSettings`
        """
        url = self.ep('settings/callRecording')
        data = super().get(url)
        r = MeRecordingSettings.model_validate(data)
        return r
