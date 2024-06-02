from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['RecordingFormat', 'RecordingServiceType', 'RecordingStatus', 'Recording', 'RecordingsApi']


class RecordingFormat(str, Enum):
    #: Recording file format is MP3.
    mp3 = 'MP3'
    #: Recording file format is MP4.
    mp4 = 'MP4'
    #: Recording file format is ARF, a proprietary Webex recording format.
    arf = 'ARF'
    #: The recording file is uploaded manually.
    uploaded = 'UPLOADED'


class RecordingServiceType(str, Enum):
    #: The service type for the recording is meeting.
    meeting_center = 'MeetingCenter'
    #: The service type for the recording is the event.
    event_center = 'EventCenter'
    #: The service type for the recording is the training session.
    training_center = 'TrainingCenter'
    #: The service type for the recording is the support meeting.
    support_center = 'SupportCenter'
    calling = 'calling'
    all = 'all'


class RecordingStatus(str, Enum):
    #: Recording is available.
    available = 'available'
    #: Recording has been moved to the recycle bin.
    deleted = 'deleted'
    #: Recording has been purged from the recycle bin. Please note that only a compliance officer can access recordings
    #: with a `purged` status.
    purged = 'purged'
    none_ = 'none'


class TemporaryDirectDownloadLinks(ApiModel):
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


class Recording(ApiModel):
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
    #: <https://help.webex.com/en-us/article/sxdj4ab/Manage-Security-for-a-Cisco-Webex-Site-in-Cisco-Webex-Control
    # -Hub>`_.
    #: example: https://site4-example.webex.com/site4/lsr.php?RCID=60b864cc80aa5b44fc9769c8305b98b7
    download_url: Optional[str] = None
    #: The playback link for recording.
    #: example: https://site4-example.webex.com/site4/ldr.php?RCID=7a8a476b29a32cd1e06dfa6c81970f19
    playback_url: Optional[str] = None
    #: The recording's password.
    #: example: BgJep@43
    password: Optional[str] = None
    #: example: MP4
    format: Optional[RecordingFormat] = None
    #: The service type for the recording.
    #: example: MeetingCenter
    service_type: Optional[RecordingServiceType] = None
    #: The duration of the recording, in seconds.
    #: example: 4472
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    #: example: 248023188
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
    temporary_direct_download_links: Optional[TemporaryDirectDownloadLinks] = None
    #: External keys of the parent meeting created by an integration application. They could be Zendesk ticket IDs,
    #: Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries recordings by a key in its own
    #: domain.
    integration_tags: Optional[list[str]] = None
    status: Optional[RecordingStatus] = None


class RecordingsApi(ApiChild, base=''):
    """
    Recordings

    Recordings are meeting content captured in a meeting or files uploaded via the upload page for your Webex site.

    This API manages recordings. Recordings may be retrieved via download or playback links defined by `downloadUrl` or
    `playbackUrl` in the response body.

    When the recording function is paused in the meeting the recording will not contain the pause. If the recording
    function is stopped and restarted in the meeting, several recordings will be created. These recordings will be
    consolidated and available all at once.

    Refer to the `Meetings API Scopes
    <https://developer.webex.com/docs/meetings#user-level-authentication-and-scopes>`_ for the specific scopes
    required for each API.
    """

    def list_recordings(self, from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                        meeting_id: str = None, host_email: str = None, site_url: str = None,
                        integration_tag: str = None, topic: str = None, format_: RecordingFormat = None,
                        service_type: RecordingServiceType = None, status: RecordingStatus = None,
                        **params) -> Generator[Recording, None, None]:
        """
        List Recordings

        Lists recordings. You can specify a date range, a parent meeting ID, and the maximum number of recordings to
        return.

        Only recordings of meetings hosted by or shared with the authenticated user will be listed.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        * If `meetingId` is specified, only recordings associated with the specified meeting will be listed.
          NOTE: when `meetingId` is specified, parameter of `siteUrl` will be ignored.

        * If `siteUrl` is specified, recordings of the specified site will be listed; otherwise, the API lists
          recordings of all the user's sites. All available Webex sites and preferred site of the user can be
          retrieved by
          `Get Site List <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        :param from_: Starting date and time (inclusive) for recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`.
        :type to_: Union[str, datetime]
        :param meeting_id: Unique identifier for the parent meeting series, scheduled meeting, or meeting instance for
            which recordings are being requested. If a meeting series ID is specified, the operation returns an array
            of recordings for the specified meeting series. If a scheduled meeting ID is specified, the operation
            returns an array of recordings for the specified scheduled meeting. If a meeting instance ID is specified,
            the operation returns an array of recordings for the specified meeting instance. If no ID is specified,
            the operation returns an array of recordings for all meetings of the current user. When `meetingId` is
            specified, the `siteUrl` parameter is ignored.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a
            user in a site they manage and the API will return recordings of that user.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists recordings. If not specified, the API lists
            recordings from all of a user's sites. All available Webex sites and the preferred site of the user can be
            retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param integration_tag: External key of the parent meeting created by an integration application. This
            parameter is used by the integration application to query recordings by a key in its own domain, such as a
            Zendesk ticket ID, a Jira ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str
        :param topic: Recording's topic. If specified, the API filters recordings by topic in a case-insensitive
            manner.
        :type topic: str
        :param format_: Recording's file format. If specified, the API filters recordings by format.
        :type format_: RecordingsFormat
        :param service_type: The service type for recordings. If this item is specified, the API filters recordings by
            service-type.
        :type service_type: RecordingServiceType
        :param status: Recording's status. If not specified or `available`, retrieves recordings that are available.
            Otherwise, if specified as `deleted`, retrieves recordings that have been moved into the recycle bin.
        :type status: ListRecordingsStatus
        :return: Generator yielding :class:`RecordingObject` instances
        """
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        if topic is not None:
            params['topic'] = topic
        if format_ is not None:
            params['format'] = format_
        if service_type is not None:
            params['serviceType'] = service_type
        if status is not None:
            params['status'] = status
        url = self.ep('recordings')
        return self.session.follow_pagination(url=url, model=Recording, item_key='items', params=params)

    def list_recordings_for_an_admin_or_compliance_officer(self, from_: Union[str, datetime] = None,
                                                           to_: Union[str, datetime] = None, meeting_id: str = None,
                                                           site_url: str = None, integration_tag: str = None,
                                                           topic: str = None, format_: RecordingFormat = None,
                                                           service_type: RecordingServiceType = None,
                                                           status: RecordingStatus = None,
                                                           **params) -> Generator[Recording, None, None]:
        """
        List Recordings For an Admin or Compliance Officer

        List recordings for an admin or compliance officer. You can specify a date range, a parent meeting ID, and the
        maximum number of recordings to return.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages <https://developer.webex.com/docs/basics#pagination>`_.

        * If `meetingId` is specified, only recordings associated with the specified meeting will be listed. Please
          note that when `meetingId` is specified, parameter of `siteUrl` will be ignored.

        * If `siteUrl` is specified, all the recordings on the specified site are listed; otherwise, all the
          recordings on the admin user's or compliance officer's preferred site are listed. All the available
          Webex sites and the admin user's or compliance officer's preferred site can be retrieved by the
          `Get Site List <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        :param from_: Starting date and time (inclusive) for recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`. The interval between `from` and `to` must be within 30 days.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`. The interval between `from` and `to` must be within 30 days.
        :type to_: Union[str, datetime]
        :param meeting_id: Unique identifier for the parent meeting series, scheduled meeting, or meeting instance for
            which recordings are being requested. If a meeting series ID is specified, the operation returns an array
            of recordings for the specified meeting series. If a scheduled meeting ID is specified, the operation
            returns an array of recordings for the specified scheduled meeting. If a meeting instance ID is specified,
            the operation returns an array of recordings for the specified meeting instance. If not specified, the
            operation returns an array of recordings for all the current user's meetings. When `meetingId` is
            specified, the `siteUrl` parameter is ignored.
        :type meeting_id: str
        :param site_url: URL of the Webex site which the API lists recordings from. If not specified, the API lists
            recordings from user's preferred site. All available Webex sites and preferred site of the user can be
            retrieved by `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param integration_tag: External key of the parent meeting created by an integration application. This
            parameter is used by the integration application to query recordings by a key in its own domain such as a
            Zendesk ticket ID, a Jira ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str
        :param topic: Recording topic. If specified, the API filters recordings by topic in a case-insensitive manner.
        :type topic: str
        :param format_: Recording's file format. If specified, the API filters recordings by format.
        :type format_: RecordingsFormat
        :param service_type: The service type for recordings. If specified, the API filters recordings by service type.
        :type service_type: RecordingServiceType
        :param status: Recording's status. If not specified or `available`, retrieves recordings that are available.
            Otherwise, if specified as `deleted`, retrieves recordings that have been moved to the recycle bin.
        :type status: ListRecordingsStatus
        :return: Generator yielding :class:`RecordingObjectForAdminAndCO` instances
        """
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        if topic is not None:
            params['topic'] = topic
        if format_ is not None:
            params['format'] = format_
        if service_type is not None:
            params['serviceType'] = service_type
        if status is not None:
            params['status'] = status
        url = self.ep('admin/recordings')
        return self.session.follow_pagination(url=url, model=Recording, item_key='items',
                                              params=params)

    def get_recording_details(self, recording_id: str, host_email: str = None) -> Recording:
        """
        Get Recording Details

        Retrieves details for a recording with a specified recording ID.

        Only recordings of meetings hosted by or shared with the authenticated user may be retrieved.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a user in a site they
            manage, and the API will return recording details of that user.
        :type host_email: str
        :rtype: :class:`RecordingObjectWithDirectDownloadLinks`
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'recordings/{recording_id}')
        data = super().get(url, params=params)
        r = Recording.model_validate(data)
        return r

    def delete_a_recording(self, recording_id: str, reason: str, comment: str, host_email: str = None):
        """
        Delete a Recording

        Removes a recording with a specified recording ID. The deleted recording cannot be recovered. If a Compliance
        Officer deletes another user's recording, the recording will be inaccessible to regular users (host, attendees
        and shared), but will be still available to the Compliance Officer.

        Only recordings of meetings hosted by the authenticated user can be deleted.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param reason: Reason for deleting a recording. Only required when a Compliance Officer is operating on another
            user's recording.
        :type reason: str
        :param comment: Compliance Officer's explanation for deleting a recording. The comment can be a maximum of 255
            characters long.
        :type comment: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a user in a site they
            manage and the API will delete a recording of that user.
        :type host_email: str
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        body['reason'] = reason
        body['comment'] = comment
        url = self.ep(f'recordings/{recording_id}')
        super().delete(url, params=params, json=body)

    def move_recordings_into_the_recycle_bin(self, recording_ids: list[str], site_url: str, host_email: str = None):
        """
        Move Recordings into the Recycle Bin

        Move recordings into the recycle bin with recording IDs. Recordings in the recycle bin can be recovered by
        `Restore Recordings from Recycle Bin
        <https://developer.webex.com/docs/api/v1/recordings/restore-recordings-from-recycle-bin>`_ API. If you'd like
        to empty recordings from the recycle bin, you can use
        `Purge Recordings from Recycle Bin
        <https://developer.webex.com/docs/api/v1/recordings/purge-recordings-from-recycle-bin>`_ API to purge all or
        some of them.

        Only recordings of meetings hosted by the authenticated user can be moved into the recycle bin.

            * `recordingIds` should not be empty and its maximum size is `100`.

            * All the IDs of `recordingIds` should belong to the site of `siteUrl` or the user's preferred site if
                `siteUrl` is not specified.

        :param recording_ids: Recording IDs for removing recordings into the recycle bin in batch. Please note that all
            the recording IDs should belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not
            specified.
        :type recording_ids: list[str]
        :param site_url: URL of the Webex site from which the API deletes recordings. If not specified, the API deletes
            recordings from the user's preferred site. All available Webex sites and preferred sites of a user can be
            retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a user in a site they
            manage and the API will move recordings into recycle bin of that user
        :type host_email: str
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        body['recordingIds'] = recording_ids
        body['siteUrl'] = site_url
        url = self.ep('recordings/softDelete')
        super().post(url, params=params, json=body)

    def restore_recordings_from_recycle_bin(self, restore_all: bool, recording_ids: list[str], site_url: str,
                                            host_email: str = None):
        """
        Restore Recordings from Recycle Bin

        Restore all or some recordings from the recycle bin. Only recordings of meetings hosted by the authenticated
        user can be restored from recycle bin.

            * If `restoreAll` is `true`, `recordingIds` should be empty.

            * If `restoreAll` is `false`, `recordingIds` should not be empty and its maximum size is `100`.

            * All the IDs of `recordingIds` should belong to the site of `siteUrl` or the user's preferred site if
                `siteUrl` is not specified.

        :param restore_all: If not specified or `false`, restores the recordings specified by `recordingIds`. If
            `true`, restores all recordings from the recycle bin.
        :type restore_all: bool
        :param recording_ids: Recording IDs for recovering recordings from the recycle bin in batch. Note that all the
            recording IDs should belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not
            specified.
        :type recording_ids: list[str]
        :param site_url: URL of the Webex site from which the API restores recordings. If not specified, the API
            restores recordings from a user's preferred site. All available Webex sites and preferred sites of a user
            can be retrieved by `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a
            user in a site they manage and the API will restore recordings of that user.
        :type host_email: str
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        body['restoreAll'] = restore_all
        body['recordingIds'] = recording_ids
        body['siteUrl'] = site_url
        url = self.ep('recordings/restore')
        super().post(url, params=params, json=body)

    def purge_recordings_from_recycle_bin(self, purge_all: bool, recording_ids: list[str], site_url: str,
                                          host_email: str = None):
        """
        Purge Recordings from Recycle Bin

        Purge recordings from recycle bin with recording IDs or purge all the recordings that are in the recycle bin.

        Only recordings of meetings hosted by the authenticated user can be purged from recycle bin.

            * If `purgeAll` is `true`, `recordingIds` should be empty.

            * If `purgeAll` is `false`, `recordingIds` should not be empty and its maximum size is `100`.

            * All the IDs of `recordingIds` should belong to the site of `siteUrl` or the user's preferred site if
                `siteUrl` is not specified.

        :param purge_all: If not specified or `false`, purges the recordings specified by `recordingIds`. If `true`,
            purges all recordings from the recycle bin.
        :type purge_all: bool
        :param recording_ids: Recording IDs for purging recordings from the recycle bin in batch. Note that all the
            recording IDs should belong to the site of `siteUrl` or the user's preferred site if `siteUrl` is not
            specified.
        :type recording_ids: list[str]
        :param site_url: URL of the Webex site from which the API purges recordings. If not specified, the API purges
            recordings from user's preferred site. All available Webex sites and preferred sites of the user can be
            retrieved by `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param host_email: Email address for the meeting host. Only used if the user or application calling the API has
            the required `admin-level meeting scopes
            <https://developer.webex.com/docs/meetings#adminorganization-level-authentication-and-scopes>`_. If set,
            the admin may specify the email of a user in a site they
            manage and the API will purge recordings from recycle bin of that user.
        :type host_email: str
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        body['purgeAll'] = purge_all
        body['recordingIds'] = recording_ids
        body['siteUrl'] = site_url
        url = self.ep('recordings/purge')
        super().post(url, params=params, json=body)
