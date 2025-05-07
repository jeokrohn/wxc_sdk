"""
Call recording API
"""
from typing import Optional

from pydantic import Field

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum

__all__ = ['Record', 'NotificationType', 'NotificationRepeat', 'Notification', 'CallRecordingSetting',
           'StartStopAnnouncement', 'CallRecordingApi']


class Record(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_w_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (\*44) has been entered. Pause, resume, and
    #: stop controls are supported.
    on_demand = 'On Demand with User Initiated Start'


class NotificationType(str, Enum):
    """
    Type of pause/resume notification.
    """
    #: No notification sound played when call recording is paused or resumed.
    none = 'None'
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class NotificationRepeat(ApiModel):
    """
    Beep sound plays periodically.
    """
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    interval: int
    #: true when ongoing call recording tone will be played at the designated interval. false indicates no warning tone
    # will be played
    enabled: bool


class Notification(ApiModel):
    #: Type of pause/resume notification.
    notification_type: Optional[NotificationType] = Field(alias='type', default=None)
    #: true when the notification feature is in effect. false indicates notification is disabled.
    enabled: bool


class StartStopAnnouncement(ApiModel):
    """
    Call Recording starts and stops announcement settings.
    """
    #: When true, an announcement is played when call recording starts and an announcement is played when call
    #:  recording ends for internal calls.
    internal_calls_enabled: Optional[bool] = None
    #: When true, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for PSTN calls.
    pstn_calls_enabled: Optional[bool] = None


class CallRecordingAccessSettings(ApiModel):
    #: When `true`, the person can view and play call recordings.
    view_and_play_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can download call recordings.
    download_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can delete call recordings.
    delete_recordings_enabled: Optional[bool] = None
    #: When `true`, the person can share call recordings.
    share_recordings_enabled: Optional[bool] = None


class PostCallRecordingSettings(ApiModel):
    summary_and_action_items_enabled: Optional[bool] = None
    transcript_enabled: Optional[bool] = None


class CallRecordingSetting(ApiModel):
    #: true if call recording is enabled.
    enabled: Optional[bool] = None
    #: Specified under which scenarios calls will be recorded.
    record: Optional[Record] = None
    #: When true, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends.
    start_stop_announcement_enabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[Notification] = None
    #: Beep sound plays periodically.
    repeat: Optional[NotificationRepeat] = None
    #: Name of the service provider providing call recording service.
    service_provider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service
    external_group: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    external_identifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[StartStopAnnouncement] = None
    #: Settings related to call recording access.
    call_recording_access_settings: Optional[CallRecordingAccessSettings] = None
    #: TODO: undocumented, issue 201
    post_call_recording_settings: Optional[PostCallRecordingSettings] = None

    @staticmethod
    def default() -> 'CallRecordingSetting':
        """
        Default settings for a user
        """
        return CallRecordingSetting(enabled=False,
                                    record=Record.never,
                                    record_voicemail_enabled=False,
                                    start_stop_announcement_enabled=False,
                                    notification=Notification(notification_type=NotificationType.none,
                                                              enabled=False),
                                    repeat=NotificationRepeat(interval=15,
                                                              enabled=False),
                                    start_stop_announcement=StartStopAnnouncement(internal_calls_enabled=False,
                                                                                  pstn_calls_enabled=False))

    def update(self) -> dict:
        """
        date for update

        :meta private:
        """
        data = self.model_dump(mode='json', exclude_unset=True, by_alias=True,
                               exclude={'service_provider', 'external_group', 'external_identifier'})
        if self.notification and self.notification.notification_type == NotificationType.none:
            # Read on API returns "None" but update has to be null
            data['notification']['type'] = None
        return data


class CallRecordingApi(PersonSettingsApiChild):
    """
    API for recording settings

    Also used for virtual lines, workspaces
    """

    feature = 'callRecording'

    def read(self, entity_id: str, org_id: str = None) -> CallRecordingSetting:
        """
        Read Call Recording Settings

        Retrieve Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        return CallRecordingSetting.model_validate(self.get(ep, params=params))

    def configure(self, entity_id: str, recording: CallRecordingSetting, org_id: str = None):
        """
        Configure Call Recording Settings for a entity

        Configure Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param recording: the new recording settings
        :type recording: CallRecordingSetting
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = recording.update()
        self.put(ep, params=params, json=data)
