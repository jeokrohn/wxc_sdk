from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BulkPurgeRecordingObject', 'BulkRestoreRecordingObject', 'BulkSoftDeleteRecordingObject',
            'DeleteRecordingObject', 'ListRecordingsForAnAdminOrComplianceOfficerResponse', 'ListRecordingsFormat',
            'ListRecordingsResponse', 'ListRecordingsStatus', 'RecordingObject', 'RecordingObjectForAdminAndCO',
            'RecordingObjectFormat', 'RecordingObjectServiceType', 'RecordingObjectStatus',
            'RecordingObjectWithDirectDownloadLinks', 'RecordingObjectWithDirectDownloadLinksStatus',
            'RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks']


class RecordingObjectFormat(str, Enum):
    #: Recording file format is MP4.
    mp4 = 'MP4'
    #: Recording file format is ARF, a proprietary Webex recording format.
    arf = 'ARF'
    #: The recording file is uploaded manually.
    uploaded = 'UPLOADED'


class RecordingObjectServiceType(str, Enum):
    #: The service type for the recording is meeting.
    meeting_center = 'MeetingCenter'
    #: The service type for the recording is the event.
    event_center = 'EventCenter'
    #: The service type for the recording is the training session.
    training_center = 'TrainingCenter'
    #: The service type for the recording is the support meeting.
    support_center = 'SupportCenter'


class RecordingObjectStatus(str, Enum):
    #: Recording is available.
    available = 'available'
    #: Recording has been moved into recycle bin.
    deleted = 'deleted'
    none_ = 'none'


class RecordingObject(ApiModel):
    #: A unique identifier for the recording.
    #: example: 4f914b1dfe3c4d11a61730f18c0f5387
    id: Optional[str] = None
    #: Unique identifier for the recording's ended meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    meeting_id: Optional[str] = None
    #: Unique identifier for the recording's scheduled meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    scheduled_meeting_id: Optional[str] = None
    #: Unique identifier for the recording's meeting series.
    #: example: f91b6edce9864428af084977b7c68291
    meeting_series_id: Optional[str] = None
    #: The recording's topic.
    #: example: John's Meeting
    topic: Optional[str] = None
    #: The date and time recording was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    #: example: 2019-01-27T17:43:24Z
    create_time: Optional[datetime] = None
    #: The date and time recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. It indicates when the record button was
    #: clicked in the meeting.
    #: example: 2019-01-27T17:40:20Z
    time_recorded: Optional[datetime] = None
    #: Site URL for the recording.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: The download link for recording. This attribute is not available if **Prevent downloading** has been turned on
    #: for the recording being requested. The **Prevent downloading** option can be viewed and set by a site admin on
    #: `Control Hub
    #: <https://help.webex.com/en-us/article/sxdj4ab/Manage-Security-for-a-Cisco-Webex-Site-in-Cisco-Webex-Control-Hub>`_.
    #: example: https://site4-example.webex.com/site4/lsr.php?RCID=60b864cc80aa5b44fc9769c8305b98b7
    download_url: Optional[str] = None
    #: The playback link for recording.
    #: example: https://site4-example.webex.com/site4/ldr.php?RCID=7a8a476b29a32cd1e06dfa6c81970f19
    playback_url: Optional[str] = None
    #: The recording's password.
    #: example: BgJep@43
    password: Optional[str] = None
    #: example: MP4
    format: Optional[RecordingObjectFormat] = None
    #: The service type for the recording.
    #: example: MeetingCenter
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording, in seconds.
    #: example: 4472.0
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    #: example: 248023188.0
    size_bytes: Optional[int] = None
    #: Whether or not the recording has been shared to the current user.
    share_to_me: Optional[bool] = None
    #: External keys of the parent meeting created by an integration application. They could be Zendesk ticket IDs,
    #: Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries recordings by a key in its own
    #: domain.
    integration_tags: Optional[list[str]] = None
    status: Optional[RecordingObjectStatus] = None


class RecordingObjectForAdminAndCO(ApiModel):
    #: A unique identifier for the recording.
    #: example: 4f914b1dfe3c4d11a61730f18c0f5387
    id: Optional[str] = None
    #: Unique identifier for the recording's ended meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    meeting_id: Optional[str] = None
    #: Unique identifier for the recording's scheduled meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    scheduled_meeting_id: Optional[str] = None
    #: Unique identifier for the recording's meeting series.
    #: example: f91b6edce9864428af084977b7c68291
    meeting_series_id: Optional[str] = None
    #: The recording's topic.
    #: example: John's Meeting
    topic: Optional[str] = None
    #: The date and time recording was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    #: example: 2019-01-27T17:43:24Z
    create_time: Optional[datetime] = None
    #: The date and time recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. It indicates when the record button was
    #: clicked in the meeting.
    #: example: 2019-01-27T17:40:20Z
    time_recorded: Optional[datetime] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Site URL for the recording.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: The download link for recording. This attribute is not available if **Prevent downloading** has been turned on
    #: for the recording being requested. The **Prevent downloading** option can be viewed and set by a site admin on
    #: `Control Hub
    #: <https://help.webex.com/en-us/article/sxdj4ab/Manage-Security-for-a-Cisco-Webex-Site-in-Cisco-Webex-Control-Hub>`_.
    #: example: https://site4-example.webex.com/site4/lsr.php?RCID=60b864cc80aa5b44fc9769c8305b98b7
    download_url: Optional[str] = None
    #: The playback link for recording.
    #: example: https://site4-example.webex.com/site4/ldr.php?RCID=7a8a476b29a32cd1e06dfa6c81970f19
    playback_url: Optional[str] = None
    #: The recording's password.
    #: example: BgJep@43
    password: Optional[str] = None
    #: example: MP4
    format: Optional[RecordingObjectFormat] = None
    #: The service type for the recording.
    #: example: MeetingCenter
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording, in seconds.
    #: example: 4472.0
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    #: example: 248023188.0
    size_bytes: Optional[int] = None
    #: Whether or not the recording has been shared to the current user.
    share_to_me: Optional[bool] = None
    #: External keys of the parent meeting created by an integration application. They could be Zendesk ticket IDs,
    #: Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries recordings by a key in its own
    #: domain.
    integration_tags: Optional[list[str]] = None
    status: Optional[RecordingObjectStatus] = None


class RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks(ApiModel):
    #: The download link for recording MP4/ARF file without HTML page rendering in browser or HTTP redirect. Expires 3
    #: hours after the API request.
    recording_download_link: Optional[str] = None
    #: The download link for recording audio file without HTML page rendering in browser or HTTP redirect. This
    #: attribute is not available if **Prevent Downloading** has been turned on for the recording being requested.
    #: Expires 3 hours after the API request.
    audio_download_link: Optional[str] = None
    #: The download link for recording transcript file without HTML page rendering in browser or HTTP redirect. This
    #: attribute is not available if **Prevent Downloading** has been turned on for the recording being requested.
    #: Expires 3 hours after the API request.
    transcript_download_link: Optional[str] = None
    #: The date and time when `recordingDownloadLink`, `audioDownloadLink`, and `transcriptDownloadLink` expire in
    #: `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    expiration: Optional[str] = None


class RecordingObjectWithDirectDownloadLinksStatus(str, Enum):
    #: Recording is available.
    available = 'available'
    #: Recording has been moved to the recycle bin.
    deleted = 'deleted'
    #: Recording has been purged from the recycle bin. Please note that only a compliance officer can access recordings
    #: with a `purged` status.
    purged = 'purged'
    none_ = 'none'


class RecordingObjectWithDirectDownloadLinks(ApiModel):
    #: A unique identifier for recording.
    #: example: 7ee40776779243b4b3da448d941b34dc
    id: Optional[str] = None
    #: Unique identifier for the recording's ended meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    meeting_id: Optional[str] = None
    #: Unique identifier for the recording's scheduled meeting instance.
    #: example: f91b6edce9864428af084977b7c68291_I_166641849979635652
    scheduled_meeting_id: Optional[str] = None
    #: Unique identifier for the recording's meeting series.
    #: example: f91b6edce9864428af084977b7c68291
    meeting_series_id: Optional[str] = None
    #: The recording's topic.
    #: example: John's Meeting
    topic: Optional[str] = None
    #: The date and time recording was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    #: example: 2019-01-27T17:43:24Z
    create_time: Optional[datetime] = None
    #: The date and time recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. It indicates when the record button was
    #: clicked in the meeting.
    #: example: 2019-01-27T17:40:20Z
    time_recorded: Optional[datetime] = None
    #: Site URL for the recording.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: The download link for the recording. This attribute is not available if `prevent downloading` has been turned on
    #: for the recording being requested. The `prevent downloading` option can be viewed and set on page when editing
    #: a recording.
    #: example: https://site4-example.webex.com/site4/lsr.php?RCID=60b864cc80aa5b44fc9769c8305b98b7
    download_url: Optional[str] = None
    #: The playback link for recording.
    #: example: https://site4-example.webex.com/site4/ldr.php?RCID=7a8a476b29a32cd1e06dfa6c81970f19
    playback_url: Optional[str] = None
    #: The recording's password.
    #: example: BgJep@43
    password: Optional[str] = None
    #: example: MP4
    format: Optional[RecordingObjectFormat] = None
    #: example: MeetingCenter
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording in seconds.
    #: example: 4472.0
    duration_seconds: Optional[int] = None
    #: The size of the recording file in bytes.
    #: example: 248023188.0
    size_bytes: Optional[int] = None
    #: Whether or not the recording has been shared to the current user.
    share_to_me: Optional[bool] = None
    #: The download links for MP4/ARF, audio, and transcript of the recording without HTML page rendering in browser or
    #: HTTP redirect. This attribute is not available if the user is not a `Compliance Officer
    #: <https://developer.webex.com/docs/compliance#compliance>`_ and **Prevent
    #: Downloading** has been turned on for the recording being requested. The Prevent Downloading option can be
    #: viewed and set on page when editing a recording. Note that there are various products in `Webex Suite
    #: <https://www.cisco.com/c/en/us/products/conferencing/product_comparison.html>`_ such as
    #: "Webex Meetings", "Webex Training" and "Webex Events".
    temporary_direct_download_links: Optional[RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks] = None
    #: External keys of the parent meeting created by an integration application. The key can be Zendesk ticket IDs,
    #: Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries recordings by a key in its own
    #: domain.
    integration_tags: Optional[list[str]] = None
    status: Optional[RecordingObjectWithDirectDownloadLinksStatus] = None


class DeleteRecordingObject(ApiModel):
    #: Reason for deleting a recording. Only required when a Compliance Officer is operating on another user's
    #: recording.
    #: example: audit
    reason: Optional[str] = None
    #: Compliance Officer's explanation for deleting a recording. The comment can be a maximum of 255 characters long.
    #: example: Maintain data privacy
    comment: Optional[str] = None


class BulkSoftDeleteRecordingObject(ApiModel):
    #: Recording IDs for removing recordings into the recycle bin in batch. Please note that all the recording IDs
    #: should belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not specified.
    recording_ids: Optional[list[str]] = None
    #: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes recordings from
    #: the user's preferred site. All available Webex sites and preferred sites of a user can be retrieved by the
    #: `Get Site List
    #: <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
    #: example: example.webex.com
    site_url: Optional[str] = None


class BulkRestoreRecordingObject(ApiModel):
    #: If not specified or `false`, restores the recordings specified by `recordingIds`. If `true`, restores all
    #: recordings from the recycle bin.
    restore_all: Optional[bool] = None
    #: Recording IDs for recovering recordings from the recycle bin in batch. Note that all the recording IDs should
    #: belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not specified.
    recording_ids: Optional[list[str]] = None
    #: URL of the Webex site from which the API restores recordings. If not specified, the API restores recordings from
    #: a user's preferred site. All available Webex sites and preferred sites of a user can be retrieved by
    #: `Get Site List
    #: <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
    #: example: example.webex.com
    site_url: Optional[str] = None


class BulkPurgeRecordingObject(ApiModel):
    #: If not specified or `false`, purges the recordings specified by `recordingIds`. If `true`, purges all recordings
    #: from the recycle bin.
    purge_all: Optional[bool] = None
    #: Recording IDs for purging recordings from the recycle bin in batch. Note that all the recording IDs should
    #: belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not specified.
    recording_ids: Optional[list[str]] = None
    #: URL of the Webex site from which the API purges recordings. If not specified, the API purges recordings from
    #: user's preferred site. All available Webex sites and preferred sites of the user can be retrieved by
    #: `Get Site List
    #: <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
    #: example: example.webex.com
    site_url: Optional[str] = None


class ListRecordingsFormat(str, Enum):
    mp4 = 'MP4'
    arf = 'ARF'


class ListRecordingsStatus(str, Enum):
    available = 'available'
    deleted = 'deleted'


class ListRecordingsResponse(ApiModel):
    #: An array of recording objects.
    items: Optional[list[RecordingObject]] = None


class ListRecordingsForAnAdminOrComplianceOfficerResponse(ApiModel):
    #: An array of recording objects.
    items: Optional[list[RecordingObjectForAdminAndCO]] = None
