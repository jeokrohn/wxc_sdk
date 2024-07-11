from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnnouncementResponse', 'AnnouncementUsageResponse', 'AnnouncementsListResponse',
           'AnnouncementsListResponseLevel', 'FeatureReferenceObject', 'FeaturesAnnouncementRepositoryApi',
           'FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelLocationId', 'LocationObject']


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
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    #: example: 2023-06-13T18:39:53.651Z
    last_updated: Optional[datetime] = None
    #: Reference count of the call features this announcement is assigned to.
    #: example: 1
    feature_reference_count: Optional[int] = None
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]] = None


class AnnouncementUsageResponse(ApiModel):
    #: Total file size used by announcements in this repository in kilobytes.
    #: example: 1068
    total_file_size_used_kb: Optional[int] = Field(alias='totalFileSizeUsedKB', default=None)
    #: Maximum audio file size allowed to upload in kilobytes.
    #: example: 9600
    max_audio_file_size_allowed_kb: Optional[int] = Field(alias='maxAudioFileSizeAllowedKB', default=None)
    #: Maximum video file size allowed to upload in kilobytes.
    #: example: 120000
    max_video_file_size_allowed_kb: Optional[int] = Field(alias='maxVideoFileSizeAllowedKB', default=None)
    #: Total file size limit for the repository in megabytes.
    #: example: 1000
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
    file_size: Optional[str] = None
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


class FeaturesAnnouncementRepositoryApi(ApiChild, base='telephony/config'):
    """
    Features:  Announcement Repository
    
    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator or location administrator
    auth token with a scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def fetch_list_of_announcement_greetings_on_location_and_organization_level(self,
                                                                                location_id: FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelLocationId = None,
                                                                                order: str = None,
                                                                                file_name: str = None,
                                                                                file_type: str = None,
                                                                                media_file_type: str = None,
                                                                                name: str = None, org_id: str = None,
                                                                                **params) -> Generator[AnnouncementsListResponse, None, None]:
        """
        Fetch list of announcement greetings on location and organization level

        Fetch a list of binary announcement greetings at an organization as well as location level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned.
        :type location_id: FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelLocationId
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str
        :param org_id: Get announcements in this organization.
        :type org_id: str
        :return: Generator yielding :class:`AnnouncementsListResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = enum_str(location_id)
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return self.session.follow_pagination(url=url, model=AnnouncementsListResponse, item_key='announcements', params=params)

    def upload_a_binary_announcement_greeting_at_organization_level(self, org_id: str = None) -> str:
        """
        Upload a binary announcement greeting at organization level

        Upload a binary file to the announcement repository at an organization level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write` .

        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements')
        data = super().post(url, params=params)
        r = data['id']
        return r

    def fetch_repository_usage_for_announcements_for_an_organization(self,
                                                                     org_id: str = None) -> AnnouncementUsageResponse:
        """
        Fetch repository usage for announcements for an organization

        Retrieves repository usage for announcements for an organization.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Get announcement usage in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementUsageResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements/usage')
        data = super().get(url, params=params)
        r = AnnouncementUsageResponse.model_validate(data)
        return r

    def delete_an_announcement_greeting_of_the_organization(self, announcement_id: str, org_id: str = None):
        """
        Delete an announcement greeting of the organization

        Delete an announcement greeting for an organization.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Delete an announcement in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        super().delete(url, params=params)

    def fetch_details_of_a_binary_announcement_greeting_at_the_organization_level(self, announcement_id: str,
                                                                                  org_id: str = None) -> AnnouncementResponse:
        """
        Fetch details of a binary announcement greeting at the organization level

        Fetch details of a binary announcement greeting by its ID at an organization level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Get an announcement in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        data = super().get(url, params=params)
        r = AnnouncementResponse.model_validate(data)
        return r

    def modify_a_binary_announcement_greeting_at_organization_level(self, announcement_id: str, org_id: str = None):
        """
        Modify a binary announcement greeting at organization level

        Modify an existing announcement greeting at an organization level.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Modify an announcement in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        super().put(url, params=params)

    def upload_a_binary_announcement_greeting_at_the_location_level(self, location_id: str, org_id: str = None) -> str:
        """
        Upload a binary announcement greeting at the location level

        Upload a binary file to the announcement repository at a location level.

        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write` .

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements')
        data = super().post(url, params=params)
        r = data['id']
        return r

    def fetch_repository_usage_for_announcements_in_a_location(self, location_id: str,
                                                               org_id: str = None) -> AnnouncementUsageResponse:
        """
        Fetch repository usage for announcements in a location

        Retrieves repository usage for announcements in a location.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Get announcement usage for location in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementUsageResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/usage')
        data = super().get(url, params=params)
        r = AnnouncementUsageResponse.model_validate(data)
        return r

    def delete_an_announcement_greeting_in_a_location(self, location_id: str, announcement_id: str,
                                                      org_id: str = None):
        """
        Delete an announcement greeting in a location.

        This API requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Unique identifier of a location where announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Delete an announcement for location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().delete(url, params=params)

    def fetch_details_of_a_binary_announcement_greeting_at_location_level(self, location_id: str, announcement_id: str,
                                                                          org_id: str = None) -> AnnouncementResponse:
        """
        Fetch details of a binary announcement greeting at location level

        Fetch details of a binary announcement greeting by its ID at a location level.

        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Fetch an announcement for location in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = super().get(url, params=params)
        r = AnnouncementResponse.model_validate(data)
        return r

    def modify_a_binary_announcement_greeting_at_location_level(self, location_id: str, announcement_id: str,
                                                                org_id: str = None):
        """
        Modify a binary announcement greeting at location level

        Modify an existing announcement greeting at a location level.

        An admin can upload a file or modify an existing file at a location level. This file will be uploaded to the
        announcement repository.

        Your request will need to be a `multipart/form-data` request rather than JSON, using the `audio/wav`
        Content-Type.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Modify an announcement for location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().put(url, params=params)
