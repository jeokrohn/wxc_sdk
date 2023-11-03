from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AnnouncementResponse', 'AnnouncementResponseWithId', 'AnnouncementUsageResponse',
            'AnnouncementsListResponse', 'AnnouncementsListResponseLevel', 'FeatureReferenceObject',
            'FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelLocationId',
            'FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse', 'LocationObject']


class FeatureReferenceObject(ApiModel):
    #: Unique identifier of the call feature referenced. The call Feature can be Auto Attendant, Call Queue or Music On
    #: hold.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Name of the call feature referenced.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Resource Type of the call feature.
    #: example: Auto Attendant
    type: Optional[str] = None
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81ZTk3MzFlNy1iOWQ0LTRmMWQtYjYyMi05NDgwMDhhMjkzMzM
    location_id: Optional[str] = None
    #: Location name of the announcement file.
    #: example: RCDN
    location_name: Optional[str] = None


class AnnouncementResponse(ApiModel):
    #: Unique identifier of the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8zMjAxNjRmNC1lNWEzLTQxZmYtYTMyNi02N2MwOThlNDFkMWQ
    id: Optional[str] = None
    #: Name of the announcement.
    #: example: Public_Announcement
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    #: example: Sample_Greetings_file.wav
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    #: example: 356
    file_size: Optional[datetime] = None
    #: Media file type of the announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    #: example: 2023-06-13T18:39:53.651Z
    last_updated: Optional[datetime] = None
    #: Reference count of the call features this announcement is assigned to.
    #: example: 1.0
    feature_reference_count: Optional[int] = None
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]] = None


class AnnouncementResponseWithId(ApiModel):
    #: Unique identifier of the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8wOWJmNTQwYS05ZWE0LTRhMzktOWI3Mi0xN2Q2MTE0ZTVjMjE
    id: Optional[str] = None


class AnnouncementUsageResponse(ApiModel):
    #: Total file size used by announcements in this repository in kilobytes.
    #: example: 1068.0
    total_file_size_used_kb: Optional[int] = Field(alias='totalFileSizeUsedKB', default=None)
    #: Maximum audio file size allowed to upload in kilobytes.
    #: example: 9600.0
    max_audio_file_size_allowed_kb: Optional[int] = Field(alias='maxAudioFileSizeAllowedKB', default=None)
    #: Maximum video file size allowed to upload in kilobytes.
    #: example: 120000.0
    max_video_file_size_allowed_kb: Optional[int] = Field(alias='maxVideoFileSizeAllowedKB', default=None)
    #: Total file size limit for the repository in megabytes.
    #: example: 1000.0
    total_file_size_limit_mb: Optional[int] = Field(alias='totalFileSizeLimitMB', default=None)


class AnnouncementsListResponseLevel(str, Enum):
    location = 'LOCATION'


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81ZTk3MzFlNy1iOWQ0LTRmMWQtYjYyMi05NDgwMDhhMjkzMzM
    id: Optional[str] = None
    #: Name of the Location.
    #: example: RCDN
    name: Optional[str] = None


class AnnouncementsListResponse(ApiModel):
    #: Unique identifier of the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8zMjAxNjRmNC1lNWEzLTQxZmYtYTMyNi02N2MwOThlNDFkMWQ
    id: Optional[str] = None
    #: Name of the announcement.
    #: example: Public_Announcement
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    #: example: Sample_Greetings_file.wav
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    #: example: 356
    file_size: Optional[datetime] = None
    #: Media file type of the announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: LastUpdated timestamp (in UTC format) of the announcement.
    #: example: 2023-06-13T18:39:53.651Z
    last_updated: Optional[datetime] = None
    #: The level at which this announcement exists.
    #: example: LOCATION
    level: Optional[AnnouncementsListResponseLevel] = None
    #: The details of location at which this announcement exists.
    location: Optional[LocationObject] = None


class FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelLocationId(str, Enum):
    all = 'all'
    locations = 'locations'
    y2lz_y29zc_gfyazov_l3_vz_l0x_pq0_fusu9_olz_mx_mtyx = 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx'


class FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse(ApiModel):
    #: Array of announcements.
    announcements: Optional[list[AnnouncementsListResponse]] = None
