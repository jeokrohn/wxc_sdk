from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ConvergedRecordingsApi', 'GetRecordingMetadataResponse', 'GetRecordingMetadataResponseServiceData',
           'GetRecordingMetadataResponseServiceDataCallActivityItem',
           'GetRecordingMetadataResponseServiceDataCallActivityItemAnnouncementData',
           'GetRecordingMetadataResponseServiceDataCallActivityItemMediaStreamsItem',
           'GetRecordingMetadataResponseServiceDataCallActivityItemParticipantsItem',
           'GetRecordingMetadataResponseServiceDataCallingParty',
           'GetRecordingMetadataResponseServiceDataCallingPartyActor',
           'GetRecordingMetadataResponseServiceDataRecordingActionsItem',
           'GetRecordingMetadataResponseServiceDataSession', 'OwnerType', 'RecordingObject', 'RecordingObjectFormat',
           'RecordingObjectOwnerType', 'RecordingObjectServiceData', 'RecordingObjectServiceType',
           'RecordingObjectStatus', 'RecordingObjectWithDirectDownloadLinks',
           'RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks', 'ServiceType', 'StorageRegion']


class RecordingObjectFormat(str, Enum):
    #: Recording file format is MP3.
    mp3 = 'MP3'


class RecordingObjectServiceType(str, Enum):
    #: Recording service type is Webex Call.
    calling = 'calling'


class RecordingObjectStatus(str, Enum):
    #: Recording is available.
    available = 'available'
    #: Recording has been moved into recycle bin.
    deleted = 'deleted'


class RecordingObjectOwnerType(str, Enum):
    #: Recording belongs to a user.
    user = 'user'
    #: Recording belongs to a workspace device.
    place = 'place'
    #: Recording belongs to a workspace device.
    virtual_line = 'virtualLine'


class RecordingObjectServiceData(ApiModel):
    #: Webex calling location for recording user.
    location_id: Optional[str] = None
    #: Call ID for which recording was done.
    call_session_id: Optional[str] = None


class RecordingObject(ApiModel):
    #: A unique identifier for the recording.
    id: Optional[str] = None
    #: The recording's topic.
    topic: Optional[str] = None
    #: The date and time recording was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    create_time: Optional[datetime] = None
    #: The date and time recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. It indicates when the record button was
    #: clicked in the meeting.
    time_recorded: Optional[datetime] = None
    format_: Optional[RecordingObjectFormat] = None
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording, in seconds.
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    size_bytes: Optional[int] = None
    #: * `available` - Recording is available.
    status: Optional[RecordingObjectStatus] = None
    #: Webex UUID for recording owner/host.
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    owner_email: Optional[str] = None
    #: * `user` - Recording belongs to a user.
    owner_type: Optional[RecordingObjectOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    storage_region: Optional[str] = None
    #: Fields relevant to each service Type.
    service_data: Optional[RecordingObjectServiceData] = None


class RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks(ApiModel):
    #: The download link for recording audio file without HTML page rendering in browser or HTTP redirect.  Expires 3
    #: hours after the API request.
    audio_download_link: Optional[str] = None
    #: The download link for recording transcript file without HTML page rendering in browser or HTTP redirect.
    #: Expires 3 hours after the API request.
    transcript_download_link: Optional[str] = None
    #: The download API for recording notes. The user access token is required to download the recording notes. Expires
    #: 3 hours after the API request.
    suggested_notes_download_link: Optional[str] = None
    #: The download API for recording short notes. The user access token is required to download the recording short
    #: notes. Expires 3 hours after the API request.
    short_notes_download_link: Optional[str] = None
    #: The download API for recording action items. The user access token is required to download the recording action
    #: items. Expires 3 hours after the API request.
    action_items_download_link: Optional[str] = None
    #: The date and time when `recordingDownloadLink`, `audioDownloadLink`, `transcriptDownloadLink`,
    #: `suggestedNotesDownloadLink`, `shortNotesDownloadLink` and `actionItemsDownloadLink` expire in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_
    #: compliant format.
    expiration: Optional[str] = None


class RecordingObjectWithDirectDownloadLinks(ApiModel):
    #: A unique identifier for recording.
    id: Optional[str] = None
    #: The recording's topic.
    topic: Optional[str] = None
    #: The date and time recording was created in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. Please note that it's not the time the
    #: record button was clicked in meeting but the time the recording file was generated offline.
    create_time: Optional[datetime] = None
    #: The date and time recording started in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. It indicates when the record button was
    #: clicked in the meeting.
    time_recorded: Optional[datetime] = None
    format_: Optional[RecordingObjectFormat] = None
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording in seconds.
    duration_seconds: Optional[int] = None
    #: The size of the recording file in bytes.
    size_bytes: Optional[int] = None
    #: The download links for the MP3 audio of the recordings without rendering an HTML page in a browser or an HTTP
    #: redirect. This attribute is available only for authorized users or a `Compliance Officer
    #: <https://developer.webex.com/docs/compliance#compliance>`_. This attribute is not
    #: available if the user is an admin with scope `spark-admin:recordings_read` or if **Prevent Downloading** has
    #: been turned on for the recording being requested.
    temporary_direct_download_links: Optional[RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks] = None
    #: * `available` - Recording is available.
    status: Optional[RecordingObjectStatus] = None
    #: Webex UUID for recording owner/host.
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    owner_email: Optional[str] = None
    #: * `user` - Recording belongs to a user.
    owner_type: Optional[RecordingObjectOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    storage_region: Optional[str] = None
    #: Fields relevant to each service Type.
    service_data: Optional[RecordingObjectServiceData] = None


class ServiceType(str, Enum):
    calling = 'calling'
    customer_assist = 'customerAssist'


class OwnerType(str, Enum):
    user = 'user'
    place = 'place'
    virtual_line = 'virtualLine'
    call_queue = 'callQueue'


class StorageRegion(str, Enum):
    us = 'US'
    sg = 'SG'
    gb = 'GB'
    jp = 'JP'
    de = 'DE'
    au = 'AU'
    in_ = 'IN'
    ca = 'CA'


class GetRecordingMetadataResponseServiceDataCallingPartyActor(ApiModel):
    type: Optional[str] = None
    id: Optional[str] = None


class GetRecordingMetadataResponseServiceDataCallingParty(ApiModel):
    actor: Optional[GetRecordingMetadataResponseServiceDataCallingPartyActor] = None
    number: Optional[str] = None


class GetRecordingMetadataResponseServiceDataSession(ApiModel):
    start_time: Optional[str] = None
    stop_time: Optional[str] = None


class GetRecordingMetadataResponseServiceDataRecordingActionsItem(ApiModel):
    action: Optional[str] = None
    time: Optional[str] = None


class GetRecordingMetadataResponseServiceDataCallActivityItemMediaStreamsItem(ApiModel):
    stream_id: Optional[str] = None
    mode: Optional[str] = None
    m_line_index: Optional[str] = None


class GetRecordingMetadataResponseServiceDataCallActivityItemParticipantsItem(ApiModel):
    actor: Optional[GetRecordingMetadataResponseServiceDataCallingPartyActor] = None
    aor: Optional[str] = None
    send: Optional[str] = None


class GetRecordingMetadataResponseServiceDataCallActivityItemAnnouncementData(ApiModel):
    announcement_filename: Optional[str] = None
    announcement_timestamp: Optional[str] = None
    announcement_participants: Optional[list[str]] = None
    announcement_type: Optional[str] = None


class GetRecordingMetadataResponseServiceDataCallActivityItem(ApiModel):
    time_stamp: Optional[str] = None
    media_streams: Optional[list[GetRecordingMetadataResponseServiceDataCallActivityItemMediaStreamsItem]] = None
    participants: Optional[list[GetRecordingMetadataResponseServiceDataCallActivityItemParticipantsItem]] = None
    announcement_data: Optional[GetRecordingMetadataResponseServiceDataCallActivityItemAnnouncementData] = None


class GetRecordingMetadataResponseServiceData(ApiModel):
    call_recording_id: Optional[str] = None
    location_id: Optional[str] = None
    call_session_id: Optional[str] = None
    personality: Optional[str] = None
    calling_party: Optional[GetRecordingMetadataResponseServiceDataCallingParty] = None
    called_party: Optional[GetRecordingMetadataResponseServiceDataCallingParty] = None
    call_id: Optional[str] = None
    session: Optional[GetRecordingMetadataResponseServiceDataSession] = None
    recording_type: Optional[str] = None
    answerer_info: Optional[GetRecordingMetadataResponseServiceDataCallingParty] = None
    recording_actions: Optional[list[GetRecordingMetadataResponseServiceDataRecordingActionsItem]] = None
    call_activity: Optional[list[GetRecordingMetadataResponseServiceDataCallActivityItem]] = None


class GetRecordingMetadataResponse(ApiModel):
    id: Optional[str] = None
    org_id: Optional[str] = None
    owner_id: Optional[str] = None
    owner_type: Optional[str] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    storage_region: Optional[str] = None
    service_type: Optional[str] = None
    version: Optional[str] = None
    service_data: Optional[GetRecordingMetadataResponseServiceData] = None


class ConvergedRecordingsApi(ApiChild, base=''):
    """
    Converged Recordings
    
    Webex Meetings and Webex Calling (with Webex as the Call Recording provider) leverage the same recording
    infrastructure. That ensures that users can use the same recording API to fetch call recordings and/or meeting
    recordings. This convergence allows the sharing of functionality (summaries, transcripts, etc.) across the Webex
    Suite and provides a consistent user experience.
    
    This API is currently limited to Webex Calling i.e., providing details for call recordings but will later be
    extended to include Webex Meeting recordings.
    
    The access token needs the following scopes:
    User: `spark:recordings_read` `spark:recordings_write`
    Admin: `spark-admin:recordings_read` `spark-admin:recordings_write`
    Compliance officer: `spark-compliance:recordings_read` `spark-compliance:recordings_write`
    
    When the recording is paused in a call, the recording does not contain the pause. If the recording is stopped and
    restarted in a call, several recordings are created. Those recordings will be consolidated and available all at
    once.
    
    For information on the call recording feature, refer to `Manage call recording for Webex Calling
    <https://help.webex.com/en-us/article/ilga4/Manage-call-recording-for-Webex-Calling#wbxch_t_manage-call-recording_selecting-call-recording-provider>`_.
    """

    def list_recordings_for_admin_or_compliance_officer(self, from_: Union[str, datetime] = None, to_: Union[str,
                                                        datetime] = None, status: RecordingObjectStatus = None,
                                                        service_type: ServiceType = None,
                                                        format_: RecordingObjectFormat = None, owner_id: str = None,
                                                        owner_email: str = None, owner_type: OwnerType = None,
                                                        storage_region: StorageRegion = None, location_id: str = None,
                                                        topic: str = None, timezone: str = None,
                                                        **params) -> Generator[RecordingObject, None, None]:
        """
        List Recordings for Admin or Compliance officer

        List recordings for an admin or compliance officer. You can specify a date range, and the maximum number of
        recordings to return.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        List recordings requires the `spark-compliance:recordings_read` scope for compliance officer and
        `spark-admin:recordings_read` scope for admin.

        #### Request Header

        * `timezone`: *`Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.*

        :param from_: Starting date and time (inclusive) for recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`. The interval between `from` and `to` must be within 30 days.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`. The interval between `from` and `to` must be within 30 days.
        :type to_: Union[str, datetime]
        :param status: Recording's status. If not specified or `available`, retrieves recordings that are available.
            Otherwise, if specified as `deleted`, retrieves recordings that have been moved into the recycle bin.
        :type status: RecordingObjectStatus
        :param service_type: Recording's service-type. If specified, the API filters recordings by service-type. Valid
            values are `calling` and `customerAssist`.
        :type service_type: ServiceType
        :param format_: Recording's file format. If specified, the API filters recordings by format. Valid values are
            `MP3`.
        :type format_: RecordingObjectFormat
        :param owner_id: Webex user Id to fetch recordings for a particular user.
        :type owner_id: str
        :param owner_email: Webex email address to fetch recordings for a particular user.
        :type owner_email: str
        :param owner_type: Recording based on type of user.
        :type owner_type: OwnerType
        :param storage_region: Recording stored in certain Webex locations.
        :type storage_region: StorageRegion
        :param location_id: Fetch recordings for users in a particular Webex Calling location (as configured in Control
            Hub).
        :type location_id: str
        :param topic: Recording's topic. If specified, the API filters recordings by topic in a case-insensitive
            manner.
        :type topic: str
        :param timezone: e.g. UTC
        :type timezone: str
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
        if status is not None:
            params['status'] = enum_str(status)
        if service_type is not None:
            params['serviceType'] = enum_str(service_type)
        if format_ is not None:
            params['format'] = enum_str(format_)
        if owner_id is not None:
            params['ownerId'] = owner_id
        if owner_email is not None:
            params['ownerEmail'] = owner_email
        if owner_type is not None:
            params['ownerType'] = enum_str(owner_type)
        if storage_region is not None:
            params['storageRegion'] = enum_str(storage_region)
        if location_id is not None:
            params['locationId'] = location_id
        if topic is not None:
            params['topic'] = topic
        if timezone is not None:
            params['timezone'] = timezone
        url = self.ep('admin/convergedRecordings')
        return self.session.follow_pagination(url=url, model=RecordingObject, item_key='items', params=params)

    def list_recordings(self, from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                        status: RecordingObjectStatus = None, service_type: ServiceType = None,
                        format_: RecordingObjectFormat = None, owner_type: OwnerType = None,
                        storage_region: StorageRegion = None, location_id: str = None, topic: str = None,
                        timezone: str = None, **params) -> Generator[RecordingObject, None, None]:
        """
        List Recordings

        List recordings. You can specify a date range, and the maximum number of recordings to return.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        List recordings requires the `spark:recordings_read` scope.

        Please use `List Recordings for Admin or Compliance Officer` API to list all recordings for a user with the
        role Compliance officer or Admin

        Request Header

        * `timezone`: *`Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.*

        :param from_: Starting date and time (inclusive) for recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `from` cannot be after `to`.
        :type from_: Union[str, datetime]
        :param to_: Ending date and time (exclusive) for List recordings to return, in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
            `to` cannot be before `from`.
        :type to_: Union[str, datetime]
        :param status: Recording's status. If not specified or `available`, retrieves recordings that are available.
            Otherwise, if specified as `deleted`, retrieves recordings that have been moved into the recycle bin.
        :type status: RecordingObjectStatus
        :param service_type: Recording's service-type. If specified, the API filters recordings by service-type. Valid
            values are `calling` and `customerAssist`.
        :type service_type: ServiceType
        :param format_: Recording's file format. If specified, the API filters recordings by format. Valid values are
            `MP3`.
        :type format_: RecordingObjectFormat
        :param owner_type: Recording based on type of user.
        :type owner_type: OwnerType
        :param storage_region: Recording stored in certain Webex locations.
        :type storage_region: StorageRegion
        :param location_id: Fetch recordings for users in a particular Webex Calling location (as configured in Control
            Hub).
        :type location_id: str
        :param topic: Recording's topic. If specified, the API filters recordings by topic in a case-insensitive
            manner.
        :type topic: str
        :param timezone: e.g. UTC
        :type timezone: str
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
        if status is not None:
            params['status'] = enum_str(status)
        if service_type is not None:
            params['serviceType'] = enum_str(service_type)
        if format_ is not None:
            params['format'] = enum_str(format_)
        if owner_type is not None:
            params['ownerType'] = enum_str(owner_type)
        if storage_region is not None:
            params['storageRegion'] = enum_str(storage_region)
        if location_id is not None:
            params['locationId'] = location_id
        if topic is not None:
            params['topic'] = topic
        if timezone is not None:
            params['timezone'] = timezone
        url = self.ep('convergedRecordings')
        return self.session.follow_pagination(url=url, model=RecordingObject, item_key='items', params=params)

    def purge_recordings_from_recycle_bin(self, purge_all: bool = None, owner_email: str = None,
                                          recording_ids: list[str] = None):
        """
        Purge Recordings from Recycle Bin

        Purge recordings from the recycle bin matching the supplied recording IDs, or purge all the recordings that are
        in the recycle bin. A recording, once purged, cannot be restored.

        Only the following two entities can use this API

        * Administrator: A user or an application with the scope `spark-admin:recordings_write`.

        * User: An authenticated user who does not have the scope `spark-admin:recordings_write` but has
        `spark:recordings_write`.

        As an `administrator`, you can purge a list of recordings or all recordings of a particular user within the org
        you manage from the recycle bin.

        As a `user`, you can purge a list of your own recordings or all your recordings from the recycle bin.

        * If `purgeAll` is `true`:
        * `recordingIds` should be empty.
        * If the caller of this API is an `administrator`, `ownerEmail` should not be empty and all recordings owned
        the `ownerEmail` will be purged from the recycle bin.
        * If the caller of this API is a `user`, `ownerEmail` should be empty and all recordings owned by the caller
        will be purged from the recycle bin.

        * If `purgeAll` is `false`:
        * `ownerEmail` should be empty.
        * `recordingIds` should not be empty and its maximum size is `100`.

        :param purge_all: If not specified or `false`, purges the recordings specified by `recordingIds` from the
            recycle bin. If `true`, purges all recordings owned by the caller in case of `user`, and all recordings
            owned by `ownerEmail` in case of `administrator` from the recycle bin.
        :type purge_all: bool
        :param owner_email: Email address for the recording owner. This parameter is only used if `purgeAll` is set to
            `true` and the user or application calling the API has the required administrator scope
            `spark-admin:recordings_write`. The administrator may specify the email of a user from an org they manage
            and the API will purge all the recordings of that user from the recycle bin.
        :type owner_email: str
        :param recording_ids: Recording IDs for purging recordings from the recycle bin in batch.
        :type recording_ids: list[str]
        :rtype: None
        """
        body = dict()
        if purge_all is not None:
            body['purgeAll'] = purge_all
        if owner_email is not None:
            body['ownerEmail'] = owner_email
        if recording_ids is not None:
            body['recordingIds'] = recording_ids
        url = self.ep('convergedRecordings/purge')
        super().post(url, json=body)

    def reassign_recordings(self, reassign_owner_email: str, owner_email: str = None, owner_id: str = None,
                            recording_ids: list[str] = None):
        """
        Reassign Recordings

        Reassigns recordings to a new user. As an administrator, you can reassign a list of recordings or all
        recordings of a particular user to a new user.
        The recordings can belong to an org user, a virtual line, or a workspace, but the destination user should only
        be a valid org user.

        * For a org user either `ownerEmail` or `recordingIds` or both must be provided.

        * For a virtual line or a workspace, `ownerID` or `recordingIds` or both must be provided.

        * If `recordingIds` and `ownerID` is empty but `ownerEmail` is provided, all recordings owned by the
        `ownerEmail` are reassigned to `reassignOwnerEmail`.

        * If `recordingIds` is provided and `ownerEmail` or `ownerID` is also provided, only the recordings specified
        by `recordingIds` that are owned by `ownerEmail` or `ownerID` are reassigned to `reassignOwnerEmail`.

        * If `ownerEmail` and `ownerID` is empty but `recordingIds` is provided, the recordings specified by
        `recordingIds` are reassigned to `reassignOwnerEmail` regardless of the current owner.

        * If both `ownerId` and `ownerEmail` are passed along with `recordingIds`, only the recordings specified by
        `recordingIds` that are owned by `ownerEmail` are reassigned to `reassignOwnerEmail`.

        * If `recordingIds` is empty but both `ownerId` and `ownerEmail` is provided, all recordings owned by the
        `ownerEmail` are reassigned to `reassignOwnerEmail`.

        The `spark-admin:recordings_write` scope is required to reassign recordings.

        :param reassign_owner_email: New owner of the recordings.
        :type reassign_owner_email: str
        :param owner_email: Recording owner email.
        :type owner_email: str
        :param owner_id: Recording owner ID. Can be a user, a virtual line, or a workspace.
        :type owner_id: str
        :param recording_ids: List of recording identifiers to be reassigned.
        :type recording_ids: list[str]
        :rtype: None
        """
        body = dict()
        if owner_email is not None:
            body['ownerEmail'] = owner_email
        if owner_id is not None:
            body['ownerID'] = owner_id
        if recording_ids is not None:
            body['recordingIds'] = recording_ids
        body['reassignOwnerEmail'] = reassign_owner_email
        url = self.ep('convergedRecordings/reassign')
        super().post(url, json=body)

    def restore_recordings_from_recycle_bin(self, restore_all: bool = None, owner_email: str = None,
                                            recording_ids: list[str] = None):
        """
        Restore Recordings from Recycle Bin

        Restore recordings from the recycle bin with recording IDs or restore all the recordings that are in the
        recycle bin.

        Only the following two entities can use this API

        * Administrator: A user or an application with the scope `spark-admin:recordings_write`.

        * User: An authenticated user who does not have the scope `spark-admin:recordings_write` but has
        `spark:recordings_write`.

        As an `administrator`, you can restore a list of recordings or all recordings of a particular user within the
        org you manage from the recycle bin.

        As a `user`, you can restore a list of your own recordings or all your recordings from the recycle bin.

        * If `restoreAll` is `true`:
        * `recordingIds` should be empty.
        * If the caller of this API is an `administrator`, `ownerEmail` should not be empty and all recordings owned by
        the `ownerEmail` will be restored from the recycle bin.
        * If the caller of this API is a `user`, `ownerEmail` should be empty and all recordings owned by the caller
        will be restored from the recycle bin.

        * If `restoreAll` is `false`:
        * `ownerEmail` should be empty.
        * `recordingIds` should not be empty and its maximum size is `100`.

        :param restore_all: If not specified or `false`, restores the recordings specified by `recordingIds` from the
            recycle bin. If `true`, restores all recordings owned by the caller in case of `user`, and all recordings
            owned by `ownerEmail` in case of `administrator` from the recycle bin.
        :type restore_all: bool
        :param owner_email: Email address for the recording owner. This parameter is only used if `restoreAll` is set
            to `true` and the user or application calling the API has the required administrator scope
            `spark-admin:recordings_write`. The administrator may specify the email of a user from an org they manage
            and the API will restore all the recordings of that user from the recycle bin.
        :type owner_email: str
        :param recording_ids: Recording IDs for restoring recordings from the recycle bin in batch.
        :type recording_ids: list[str]
        :rtype: None
        """
        body = dict()
        if restore_all is not None:
            body['restoreAll'] = restore_all
        if owner_email is not None:
            body['ownerEmail'] = owner_email
        if recording_ids is not None:
            body['recordingIds'] = recording_ids
        url = self.ep('convergedRecordings/restore')
        super().post(url, json=body)

    def move_recordings_into_the_recycle_bin(self, trash_all: bool = None, owner_email: str = None,
                                             recording_ids: list[str] = None):
        """
        Move Recordings into the Recycle Bin

        Move recordings into the recycle bin with recording IDs or move all the recordings to the recycle bin.

        Only the following two entities can use this API

        * Administrator: A user or an application with the scope `spark-admin:recordings_write`.

        * User: An authenticated user who does not have the scope `spark-admin:recordings_write` but has
        `spark:recordings_write`.

        As an `administrator`, you can move a list of recordings or all recordings of a particular user within the org
        you manage to the recycle bin.

        As a `user`, you can move a list of your own recordings or all your recordings to the recycle bin.

        Recordings in the recycle bin can be recovered by `Restore Recordings from Recycle Bin
        <https://developer.webex.com/docs/api/v1/converged-recordings/restore-recordings-from-recycle-bin>`_ API. If you'd like to
        empty recordings from the recycle bin, you can use `Purge Recordings from Recycle Bin
        <https://developer.webex.com/docs/api/v1/converged-recordings/purge-recordings-from-recycle-bin>`_ API to purge all or some
        of them.

        * If `trashAll` is `true`:
        * `recordingIds` should be empty.
        * If the caller of this API is an `administrator`, `ownerEmail` should not be empty and all recordings owned by
        the `ownerEmail` will be moved to the recycle bin.
        * If the caller of this API is a `user`, `ownerEmail` should be empty and all recordings owned by the caller
        will be moved to the recycle bin.

        * If `trashAll` is `false`:
        * `ownerEmail` should be empty.
        * `recordingIds` should not be empty and its maximum size is `100`.

        :param trash_all: If not specified or `false`, moves the recordings specified by `recordingIds` to the recycle
            bin. If `true`, moves all recordings owned by the caller in case of `user`, and all recordings owned by
            `ownerEmail` in case of `administrator` to the recycle bin.
        :type trash_all: bool
        :param owner_email: Email address for the recording owner. This parameter is only used if `trashAll` is set to
            `true` and the user or application calling the API has the required administrator scope
            `spark-admin:recordings_write`. The administrator may specify the email of a user from an org they manage
            and the API will move all the recordings of that user into the recycle bin.
        :type owner_email: str
        :param recording_ids: Recording IDs for moving recordings to the recycle bin in batch.
        :type recording_ids: list[str]
        :rtype: None
        """
        body = dict()
        if trash_all is not None:
            body['trashAll'] = trash_all
        if owner_email is not None:
            body['ownerEmail'] = owner_email
        if recording_ids is not None:
            body['recordingIds'] = recording_ids
        url = self.ep('convergedRecordings/softDelete')
        super().post(url, json=body)

    def delete_a_recording(self, recording_id: str, reason: str = None, comment: str = None):
        """
        Delete a Recording

        Removes a recording with a specified recording ID. The deleted recording cannot be recovered.

        If a Compliance Officer deletes another user's recording, the recording will be inaccessible to regular users
        (host, attendees and shared), and to the Compliance officer as well. This action purges the recordings from
        Webex.

        Delete a Recording requires the `spark-compliance:recordings_write` scope.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param reason: Reason for deleting a recording. Only required when a Compliance Officer is operating on another
            user's recording.
        :type reason: str
        :param comment: Compliance Officer's explanation for deleting a recording. The comment can be a maximum of 255
            characters long.
        :type comment: str
        :rtype: None
        """
        body = dict()
        if reason is not None:
            body['reason'] = reason
        if comment is not None:
            body['comment'] = comment
        url = self.ep(f'convergedRecordings/{recording_id}')
        super().delete(url, json=body)

    def get_recording_details(self, recording_id: str, timezone: str = None) -> RecordingObjectWithDirectDownloadLinks:
        """
        Get Recording Details

        Retrieves details for a recording with a specified recording ID.

        Only recordings of owner with the authenticated user may be retrieved.

        Get Recording Details requires the `spark-compliance:recordings_read` scope for compliance officer,
        `spark-admin:recordings_read` scope for admin and `spark:recordings_read` scope for user.

        #### Request Header

        * `timezone`: *`Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.*

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param timezone: e.g. UTC
        :type timezone: str
        :rtype: :class:`RecordingObjectWithDirectDownloadLinks`
        """
        params = {}
        if timezone is not None:
            params['timezone'] = timezone
        url = self.ep(f'convergedRecordings/{recording_id}')
        data = super().get(url, params=params)
        r = RecordingObjectWithDirectDownloadLinks.model_validate(data)
        return r

    def get_recording_metadata(self, recording_id: str, show_all_types: bool = None) -> GetRecordingMetadataResponse:
        """
        Get Recording metadata

        Retrieves metadata details for a recording with a specified recording ID. The recording must be owned by the
        authenticated user.

        For information on the metadata fields, refer to `Metadata Guide
        <https://developer.webex.com/docs/api/guides/consolidated-metadata-documentation-and-samples-guide>`_

        Get Recording metadata requires the `spark-compliance:recordings_read` scope for compliance officer,
        `spark-admin:recordings_read` for admin and `spark:recordings_read` for user.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param show_all_types: If `showAllTypes` is `true`, all attributes will be shown. If it's `false` or not
            specified, the following attributes of the metadata will be hidden.
        serviceData.callActivity.mediaStreams
        serviceData.callActivity.participants
        serviceData.callActivity.redirectInfo
        serviceData.callActivity.redirectedCall
        :type show_all_types: bool
        :rtype: :class:`GetRecordingMetadataResponse`
        """
        params = {}
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        url = self.ep(f'convergedRecordings/{recording_id}/metadata')
        data = super().get(url, params=params)
        r = GetRecordingMetadataResponse.model_validate(data)
        return r
