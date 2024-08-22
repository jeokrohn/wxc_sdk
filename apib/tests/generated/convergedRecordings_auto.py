from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ConvergedRecordingsApi', 'ListRecordingsForComplianceOfficerStorageRegion', 'RecordingObject',
           'RecordingObjectFormat', 'RecordingObjectOwnerType', 'RecordingObjectServiceData',
           'RecordingObjectServiceType', 'RecordingObjectStatus', 'RecordingObjectWithDirectDownloadLinks',
           'RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks']


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
    #: example: 4f914b1dfe3c4d11a61730f18c0f5387
    id: Optional[str] = None
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
    #: example: MP3
    format_: Optional[RecordingObjectFormat] = None
    #: example: calling
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording, in seconds.
    #: example: 4472
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    #: example: 248023188
    size_bytes: Optional[int] = None
    status: Optional[RecordingObjectStatus] = None
    #: Webex UUID for recording owner/host.
    #: example: 24683d6c-5529-4b60-a6c7-91e8b293bbab
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    #: example: nshtestwebex+crctestuser1@gmail.com
    owner_email: Optional[str] = None
    owner_type: Optional[RecordingObjectOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    #: example: United States
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
    #: The date and time when `recordingDownloadLink`, `audioDownloadLink`, and `transcriptDownloadLink` expire in
    #: `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    expiration: Optional[str] = None


class RecordingObjectWithDirectDownloadLinks(ApiModel):
    #: A unique identifier for recording.
    #: example: 7ee40776779243b4b3da448d941b34dc
    id: Optional[str] = None
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
    #: example: MP3
    format_: Optional[RecordingObjectFormat] = None
    #: example: calling
    service_type: Optional[RecordingObjectServiceType] = None
    #: The duration of the recording in seconds.
    #: example: 4472
    duration_seconds: Optional[int] = None
    #: The size of the recording file in bytes.
    #: example: 248023188
    size_bytes: Optional[int] = None
    #: The download links for MP3, audio of the recording without HTML page rendering in browser or HTTP redirect. This
    #: attribute is not available if the user is not a `Compliance Officer
    #: <https://developer.webex.com/docs/compliance#compliance>`_ and **Prevent Downloading** has been turned
    #: on for the recording being requested. The Prevent Downloading option can be viewed and set on page when editing
    #: a recording. Note that there are various products in `Webex Suite
    #: <https://www.cisco.com/c/en/us/products/conferencing/product_comparison.html>`_ such as "Webex Meetings", "Webex Training" and
    #: "Webex Events".
    temporary_direct_download_links: Optional[RecordingObjectWithDirectDownloadLinksTemporaryDirectDownloadLinks] = None
    status: Optional[RecordingObjectStatus] = None
    #: Webex UUID for recording owner/host.
    #: example: 24683d6c-5529-4b60-a6c7-91e8b293bbab
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    #: example: nshtestwebex+crctestuser1@gmail.com
    owner_email: Optional[str] = None
    owner_type: Optional[RecordingObjectOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    #: example: United States
    storage_region: Optional[str] = None
    #: Fields relevant to each service Type.
    service_data: Optional[RecordingObjectServiceData] = None


class ListRecordingsForComplianceOfficerStorageRegion(str, Enum):
    us = 'US'
    sg = 'SG'
    gb = 'GB'
    jp = 'JP'
    de = 'DE'
    au = 'AU'
    in_ = 'IN'
    ca = 'CA'


class ConvergedRecordingsApi(ApiChild, base=''):
    """
    Converged Recordings
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Webex Meetings and Webex Calling (with Webex as the Call Recording provider) leverage the same recording
    infrastructure. That ensures that users can use the same recording API to fetch call recordings and/or meeting
    recordings. This convergence allows the sharing of functionality (summaries, transcripts, etc.) across the Webex
    Suite and provides a consistent user experience.
    
    This API is currently limited to Webex Calling i.e., providing details for call recordings but will later be
    extended to include Webex Meeting recordings.
    
    When the recording is paused in a call, the recording does not contain the pause. If the recording is stopped and
    restarted in a call, several recordings are created. Those recordings will be consolidated and available all at
    once.
    
    For information on the call recording feature, refer to `Manage call recording for Webex Calling
    <https://help.webex.com/en-us/article/ilga4/Manage-call-recording-for-Webex-Calling#wbxch_t_manage-call-recording_selecting-call-recording-provider>`_.
    """

    def list_recordings_for_compliance_officer(self, from_: Union[str, datetime] = None, to_: Union[str,
                                               datetime] = None, status: RecordingObjectStatus = None,
                                               service_type: RecordingObjectServiceType = None,
                                               format_: RecordingObjectFormat = None, owner_id: str = None,
                                               owner_email: str = None, owner_type: RecordingObjectOwnerType = None,
                                               storage_region: ListRecordingsForComplianceOfficerStorageRegion = None,
                                               location_id: str = None,
                                               **params) -> Generator[RecordingObject, None, None]:
        """
        List Recordings for Compliance officer

        List recordings for compliance officer. You can specify a date range, and the maximum number of recordings to
        return.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        List recordings requires the spark-compliance:recordings_read scope.

        #### Request Header

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
        :param service_type: Recording's service-type. If this item is specified, the API filters recordings by
            service-type. Valid values are `calling`.
        :type service_type: RecordingObjectServiceType
        :param format_: Recording's file format. If specified, the API filters recordings by format. Valid values are
            `MP3`.
        :type format_: RecordingObjectFormat
        :param owner_id: Webex user Id to fetch recordings for a particular user.
        :type owner_id: str
        :param owner_email: Webex email address to fetch recordings for a particular user.
        :type owner_email: str
        :param owner_type: Recording based on type of user.
        :type owner_type: RecordingObjectOwnerType
        :param storage_region: Recording stored in certain Webex locations.
        :type storage_region: ListRecordingsForComplianceOfficerStorageRegion
        :param location_id: Fetch recordings for users in a particular Webex Calling location (as configured in Control
            Hub).
        :type location_id: str
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
        url = self.ep('admin/convergedRecordings')
        return self.session.follow_pagination(url=url, model=RecordingObject, item_key='items', params=params)

    def get_recording_details(self, recording_id: str) -> RecordingObjectWithDirectDownloadLinks:
        """
        Get Recording Details

        Retrieves details for a recording with a specified recording ID.

        Only recordings of owner with the authenticated user may be retrieved.

        Get Recording Details requires the spark-compliance:recordings_read scope.

        #### Request Header

        * `timezone`: *`Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in conformance with the `IANA time zone database
        not defined.*

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :rtype: :class:`RecordingObjectWithDirectDownloadLinks`
        """
        url = self.ep(f'convergedRecordings/{recording_id}')
        data = super().get(url)
        r = RecordingObjectWithDirectDownloadLinks.model_validate(data)
        return r

    def delete_a_recording(self, recording_id: str, reason: str = None, comment: str = None):
        """
        Delete a Recording

        Removes a recording with a specified recording ID. The deleted recording cannot be recovered.

        If a Compliance Officer deletes another user's recording, the recording will be inaccessible to regular users
        (host, attendees and shared), and to the Compliance officer as well. This action purges the recordings from
        Webex.

        Delete a Recording requires the spark-compliance:recordings_write scope.

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

    def get_recording_metadata(self, recording_id: str, show_all_types: bool = None):
        """
        Get Recording metadata

        Retrieves metadata details for a recording with a specified recording ID. The recording must be owned by the
        authenticated user.

        For information on the metadata fields, refer to `Metadata Guide
        <https://developer.webex.com/docs/api/guides/consolidated-metadata-documentation-and-samples-guide>`_

        Get Recording metadata requires the spark-compliance:recordings_read scope.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param show_all_types: If `showAllTypes` is `true`, all attributes will be shown. If it's `false` or not
            specified, the following attributes of the metadata will be hidden.
        serviceData.callActivity.mediaStreams
        serviceData.callActivity.participants
        serviceData.callActivity.redirectInfo
        serviceData.callActivity.redirectedCall
        :type show_all_types: bool
        :rtype: None
        """
        params = {}
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        url = self.ep(f'convergedRecordings/{recording_id}/metadata')
        super().get(url, params=params)

    def reassign_recordings(self, reassign_owner_email: str, owner_email: str = None, recording_ids: list[str] = None):
        """
        Reassign Recordings

        Reassigns recordings to a new user. As an administrator, you can reassign a list of recordings or all
        recordings of a particular user to a new user.
        The recordings can belong to an org user, a virtual line, or a workspace, but the destination user should only
        be a valid org user.

        * Either `ownerEmail` or `recordingIds` or both must be provided.

        * If `recordingIds` is empty but `ownerEmail` is provided, all recordings owned by the `ownerEmail` are
        reassigned to `reassignOwnerEmail`.

        * If `recordingIds` is provided and `ownerEmail` is also provided, only the recordings specified by
        `recordingIds` that are owned by `ownerEmail` are reassigned to `reassignOwnerEmail`.

        * If `ownerEmail` is empty but `recordingIds` is provided, the recordings specified by `recordingIds` are
        reassigned to `reassignOwnerEmail` regardless of the current owner.

        The `spark-admin:recordings_write` scope is required to reassign recordings.

        :param reassign_owner_email: New owner of the recordings.
        :type reassign_owner_email: str
        :param owner_email: Recording owner email. Can be a user, a virtual line, or a workspace.
        :type owner_email: str
        :param recording_ids: List of recording identifiers to be reassigned.
        :type recording_ids: list[str]
        :rtype: None
        """
        body = dict()
        if owner_email is not None:
            body['ownerEmail'] = owner_email
        if recording_ids is not None:
            body['recordingIds'] = recording_ids
        body['reassignOwnerEmail'] = reassign_owner_email
        url = self.ep('convergedRecordings/reassign')
        super().post(url, json=body)
