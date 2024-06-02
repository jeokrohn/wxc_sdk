from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['ConvergedRecordingsApi',
           'RecordingStorageRegion', 'ConvergedRecording',
           'RecordingOwnerType', 'RecordingServiceData',
           'ConvergedRecordingWithDirectDownloadLinks',
           'TemporaryDirectDownloadLink']

from wxc_sdk.meetings.recordings import RecordingFormat, RecordingStatus, RecordingServiceType


class RecordingOwnerType(str, Enum):
    #: Recording belongs to a user.
    user = 'user'
    #: Recording belongs to a workspace device.
    place = 'place'
    #: Recording belongs to a workspace device.
    virtual_line = 'virtualLine'


class RecordingServiceData(ApiModel):
    #: Webex calling location for recording user.
    location_id: Optional[str] = None
    #: Call ID for which recording was done.
    call_session_id: Optional[str] = None


class ConvergedRecording(ApiModel):
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
    format_: Optional[RecordingFormat] = Field(alias='format', default=None)
    service_type: Optional[str] = None
    #: The duration of the recording, in seconds.
    duration_seconds: Optional[int] = None
    #: The size of the recording file, in bytes.
    size_bytes: Optional[int] = None
    status: Optional[RecordingStatus] = None
    #: Webex UUID for recording owner/host.
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    owner_email: Optional[str] = None
    owner_type: Optional[RecordingOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    storage_region: Optional[str] = None
    #: Fields relevant to each service Type.
    service_data: Optional[RecordingServiceData] = None


class TemporaryDirectDownloadLink(ApiModel):
    #: The download link for recording audio file without HTML page rendering in browser or HTTP redirect.  Expires 3
    #: hours after the API request.
    audio_download_link: Optional[str] = None
    #: The date and time when `recordingDownloadLink`, `audioDownloadLink`, and `transcriptDownloadLink` expire in
    #: `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format.
    expiration: Optional[str] = None


class ConvergedRecordingWithDirectDownloadLinks(ApiModel):
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
    format_: Optional[str] = None
    service_type: Optional[str] = None
    #: The duration of the recording in seconds.
    duration_seconds: Optional[int] = None
    #: The size of the recording file in bytes.
    size_bytes: Optional[int] = None
    #: The download links for MP3, audio of the recording without HTML page rendering in browser or HTTP redirect. This
    #: attribute is not available if the user is not a `Compliance Officer
    #: <https://developer.webex.com/docs/compliance#compliance>`_ and **Prevent Downloading** has been turned
    #: on for the recording being requested. The Prevent Downloading option can be viewed and set on page when editing
    #: a recording. Note that there are various products in `Webex Suite
    #: <https://www.cisco.com/c/en/us/products/conferencing/product_comparison.html>`_ such as "Webex Meetings",
    # "Webex Training" and
    #: "Webex Events".
    temporary_direct_download_links: Optional[TemporaryDirectDownloadLink] = None
    status: Optional[RecordingStatus] = None
    #: Webex UUID for recording owner/host.
    owner_id: Optional[str] = None
    #: Webex email for recording owner/host.
    owner_email: Optional[str] = None
    owner_type: Optional[RecordingOwnerType] = None
    #: Storage location for recording within Webex datacenters.
    storage_region: Optional[str] = None
    #: Fields relevant to each service Type.
    service_data: Optional[RecordingServiceData] = None


class RecordingStorageRegion(str, Enum):
    us = 'US'
    sg = 'SG'
    gb = 'GB'
    jp = 'JP'
    de = 'DE'
    au = 'AU'
    in_ = 'IN'


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
    <https://help.webex.com/en-us/article/ilga4/Manage-call-recording-for-Webex-Calling#wbxch_t_manage-call
    -recording_selecting-call-recording-provider>`_.
    """

    def list(self, from_: Union[str, datetime] = None,
             to_: Union[str, datetime] = None, status: RecordingStatus = None,
             service_type: RecordingServiceType = None,
             format_: str = None, owner_id: str = None,
             owner_email: str = None, owner_type: RecordingOwnerType = None,
             storage_region: RecordingStorageRegion = None,
             location_id: str = None,
             **params) -> Generator[ConvergedRecording, None, None]:
        """
        List Recordings for Compliance officer

        List recordings for compliance officer. You can specify a date range, and the maximum number of recordings to
        return.

        The list returned is sorted in descending order by the date and time that the recordings were created.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

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
        :type status: RecordingStatus
        :param service_type: Recording's service-type. If this item is specified, the API filters recordings by
            service-type. Valid values are `calling`, or `all`.
        :type service_type: RecordingServiceType
        :param format_: Recording's file format. If specified, the API filters recordings by format. Valid values are
            `MP3`.
        :type format_: RecordingObjectFormat
        :param owner_id: Webex user Id to fetch recordings for a particular user.
        :type owner_id: str
        :param owner_email: Webex email address to fetch recordings for a particular user.
        :type owner_email: str
        :param owner_type: Recording based on type of user.
        :type owner_type: RecordingOwnerType
        :param storage_region: Recording stored in certain Webex locations.
        :type storage_region: RecordingStorageRegion
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
        return self.session.follow_pagination(url=url, model=ConvergedRecording, item_key='items', params=params)

    def details(self, recording_id: str) -> ConvergedRecordingWithDirectDownloadLinks:
        """
        Get Recording Details

        Retrieves details for a recording with a specified recording ID.

        Only recordings of owner with the authenticated user may be retrieved.

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :rtype: :class:`ConvergedRecordingWithDirectDownloadLinks`
        """
        url = self.ep(f'convergedRecordings/{recording_id}')
        data = super().get(url)
        r = ConvergedRecordingWithDirectDownloadLinks.model_validate(data)
        return r

    def delete(self, recording_id: str, reason: str = None, comment: str = None):
        """
        Delete a Recording

        Removes a recording with a specified recording ID. The deleted recording cannot be recovered.

        If a Compliance Officer deletes another user's recording, the recording will be inaccessible to regular users
        (host, attendees and shared), and to Compliance officer also. This action purges the recordings from Webex.

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

    def metadata(self, recording_id: str, show_all_types: bool = None):
        """
        Get Recording metadata

        Retrieves metadata details for a recording with a specified recording ID. The recording must be owned by the
        authenticated user.

        For information on the metadata fields, refer to `Metadata Guide
        <https://developer.webex.com/docs/webex-calling-overview>`_

        :param recording_id: A unique identifier for the recording.
        :type recording_id: str
        :param show_all_types: If `showAllTypes` is `true`, all attributes will be shown. If it's `false` or not
            specified, the following attributes of the metadata will be hidden.

            * serviceData.callActivity.mediaStreams
            * serviceData.callActivity.participants
            * serviceData.callActivity.redirectInfo
            * serviceData.callActivity.redirectedCall
        :type show_all_types: bool
        :rtype: None
        """
        params = {}
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        url = self.ep(f'convergedRecordings/{recording_id}/metadata')
        super().get(url, params=params)
