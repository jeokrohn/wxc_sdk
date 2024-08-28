from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsWithComplianceAnnouncementFeatureApi', 'CallRecordingInfo',
           'CallRecordingInfoNotification', 'CallRecordingInfoNotificationType', 'CallRecordingInfoRecord',
           'CallRecordingInfoRepeat', 'CallRecordingInfoStartStopAnnouncement']


class CallRecordingInfoRecord(str, Enum):
    #: Incoming and outgoing calls will be recorded with no control to start, stop, pause, or resume.
    always = 'Always'
    #: Calls will not be recorded.
    never = 'Never'
    #: Calls are always recorded, but user can pause or resume the recording. Stop recording is not supported.
    always_with_pause_resume = 'Always with Pause/Resume'
    #: Records only the portion of the call after the recording start (`*44`) has been entered. Pause, resume, and stop
    #: controls are supported.
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
    #: example: 15
    interval: Optional[int] = None
    #: `true` when ongoing call recording tone will be played at the designated interval. `false` indicates no warning
    #: tone will be played.
    enabled: Optional[bool] = None


class CallRecordingInfoStartStopAnnouncement(ApiModel):
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for internal calls.
    internal_calls_enabled: Optional[bool] = None
    #: When `true`, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends for PSTN calls.
    pstn_calls_enabled: Optional[bool] = None


class CallRecordingInfo(ApiModel):
    #: `true` if call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Call recording scenario.
    #: example: Never
    record: Optional[CallRecordingInfoRecord] = None
    #: When `true`, voicemail messages are also recorded.
    record_voicemail_enabled: Optional[bool] = None
    #: When enabled, an announcement is played when call recording starts and an announcement is played when call
    #: recording ends.
    start_stop_announcement_enabled: Optional[bool] = None
    #: Pause/resume notification settings.
    notification: Optional[CallRecordingInfoNotification] = None
    #: Beep sound plays periodically.
    repeat: Optional[CallRecordingInfoRepeat] = None
    #: Name of the service provider providing call recording service.
    #: example: WSWYZ25455
    service_provider: Optional[str] = None
    #: Group utilized by the service provider providing call recording service.
    #: example: WSWYZ25455L31161
    external_group: Optional[str] = None
    #: Unique person identifier utilized by the service provider providing call recording service.
    #: example: a34iidrh5o@64941297.int10.bcld.webex.com
    external_identifier: Optional[str] = None
    #: Call Recording starts and stops announcement settings.
    start_stop_announcement: Optional[CallRecordingInfoStartStopAnnouncement] = None


class BetaUserCallSettingsWithComplianceAnnouncementFeatureApi(ApiChild, base='people'):
    """
    Beta User Call Settings with Compliance Announcement Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring People settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    """

    def read_call_recording_settings_for_a_person(self, person_id: str, org_id: str = None) -> CallRecordingInfo:
        """
        Read Call Recording Settings for a Person

        Retrieve a person's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def configure_call_recording_settings_for_a_person(self, person_id: str, enabled: bool = None,
                                                       record: CallRecordingInfoRecord = None,
                                                       record_voicemail_enabled: bool = None,
                                                       start_stop_announcement_enabled: bool = None,
                                                       notification: CallRecordingInfoNotification = None,
                                                       repeat: CallRecordingInfoRepeat = None,
                                                       start_stop_announcement: CallRecordingInfoStartStopAnnouncement = None,
                                                       org_id: str = None):
        """
        Configure Call Recording Settings for a Person

        Configure a person's Call Recording settings.

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: `true` if call recording is enabled.
        :type enabled: bool
        :param record: Call recording scenario.
        :type record: CallRecordingInfoRecord
        :param record_voicemail_enabled: When `true`, voicemail messages are also recorded.
        :type record_voicemail_enabled: bool
        :param start_stop_announcement_enabled: When enabled, an announcement is played when call recording starts and
            an announcement is played when call recording ends.
        :type start_stop_announcement_enabled: bool
        :param notification: Pause/resume notification settings.
        :type notification: CallRecordingInfoNotification
        :param repeat: Beep sound plays periodically.
        :type repeat: CallRecordingInfoRepeat
        :param start_stop_announcement: Call Recording starts and stops announcement settings.
        :type start_stop_announcement: CallRecordingInfoStartStopAnnouncement
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if record is not None:
            body['record'] = enum_str(record)
        if record_voicemail_enabled is not None:
            body['recordVoicemailEnabled'] = record_voicemail_enabled
        if start_stop_announcement_enabled is not None:
            body['startStopAnnouncementEnabled'] = start_stop_announcement_enabled
        if notification is not None:
            body['notification'] = notification.model_dump(mode='json', by_alias=True, exclude_none=True)
        if repeat is not None:
            body['repeat'] = repeat.model_dump(mode='json', by_alias=True, exclude_none=True)
        if start_stop_announcement is not None:
            body['startStopAnnouncement'] = start_stop_announcement.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{person_id}/features/callRecording')
        super().put(url, params=params, json=body)
