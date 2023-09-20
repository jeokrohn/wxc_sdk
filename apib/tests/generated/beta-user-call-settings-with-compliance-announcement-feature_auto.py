from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallRecordingInfo', 'CallRecordingInfoNotification', 'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord', 'CallRecordingInfoRepeat', 'CallRecordingInfoStartStopAnnouncement', 'CallRecordingPut']


class CallRecordingInfoRecord(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (`*44`) has been entered. Pause, resume, and stop controls are supported.
    on_demand_with_user_initiated_start = 'On Demand with User Initiated Start'


class CallRecordingInfoNotificationType(str, Enum):
    #: No notification sound played when call recording is paused or resumed.
    none_ = 'None'
    #: A beep sound is played when call recording is paused or resumed.
    beep = 'Beep'
    #: A verbal announcement is played when call recording is paused or resumed.
    play_announcement = 'Play Announcement'


class CallRecordingInfoNotification(ApiModel):
    #: Type of pause/resume notification.
    #: example: None
    type: Optional[CallRecordingInfoNotificationType] = None
    #: `true` when the notification feature is in effect. `false` indicates notification is disabled.
    enabled: Optional[bool] = None


class CallRecordingInfoRepeat(ApiModel):
    #: Interval at which warning tone "beep" will be played. This interval is an integer from 10 to 1800 seconds
    #: example: 15.0
    interval: Optional[int] = None
    #: `true` when ongoing call recording tone will be played at the designated interval. `false` indicates no warning tone will be played.
    enabled: Optional[bool] = None


class CallRecordingInfoStartStopAnnouncement(ApiModel):
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call recording ends for internal calls.
    internalCallsEnabled: Optional[bool] = None
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call recording ends for PSTN calls.
    pstnCallsEnabled: Optional[bool] = None


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    recordVoicemailEnabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
    startStopAnnouncementEnabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Name of the service provider providing call recording service.
    #: example: WSWYZ25455
    serviceProvider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    #: example: WSWYZ25455L31161
    externalGroup: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    #: example: a34iidrh5o@64941297.int10.bcld.webex.com
    externalIdentifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    startStopAnnouncement: Optional[CallRecordingInfoStartStopAnnouncement] = None


class CallRecordingPut(ApiModel):
    #: `true` if call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    recordVoicemailEnabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call recording ends.
    startStopAnnouncementEnabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Call Recording starts and stops announcement settings.
    startStopAnnouncement: Optional[CallRecordingInfoStartStopAnnouncement] = None
