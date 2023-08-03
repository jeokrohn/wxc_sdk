from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['AnnouncementsListResponse', 'BetaFeaturesAnnouncementRepositorywithAnnouncementsRepositoryFeatureApi',
           'FeatureReferenceObject', 'FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse',
           'FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse',
           'FetchRepositoryUsageForAnnouncementsFororganizationResponse', 'LocationObject',
           'UploadbinaryAnnouncementGreetingAtOrganizationLevelResponse',
           'UploadbinaryAnnouncementGreetingAtlocationLevelResponse']


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    id: Optional[str]
    #: Name of the Location.
    name: Optional[str]


class AnnouncementsListResponse(LocationObject):
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str]
    #: Size of the file in kilobytes.
    file_size: Optional[str]
    #: Media file type of the announcement file.
    media_file_type: Optional[str]
    #: LastUpdated timestamp (in UTC format) of the announcement.
    last_updated: Optional[str]
    #: The level at which this announcement exists.
    level: Optional[str]
    #: The details of location at which this announcement exists.
    location: Optional[LocationObject]


class FeatureReferenceObject(LocationObject):
    #: Resource Type of the call feature.
    type: Optional[str]
    #: Unique identifier of the location.
    location_id: Optional[str]
    #: Location name of the announcement file.
    location_name: Optional[str]


class FetchRepositoryUsageForAnnouncementsFororganizationResponse(ApiModel):
    #: Total file size used by announcements in this repository in kilobytes.
    total_file_size_used_kb: Optional[int]
    #: Maximum audio file size allowed to upload in kilobytes.
    max_audio_file_size_allowed_kb: Optional[int]
    #: Maximum video file size allowed to upload in kilobytes.
    max_video_file_size_allowed_kb: Optional[int]
    #: Total file size limit for the repository in megabytes.
    total_file_size_limit_mb: Optional[int]


class FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse(LocationObject):
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str]
    #: Size of the file in kilobytes.
    file_size: Optional[str]
    #: Media file type of the announcement file.
    media_file_type: Optional[str]
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[str]
    #: Reference count of the call features this announcement is assigned to.
    feature_reference_count: Optional[int]
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]]


class FetchListOfAnnouncementGreetingsOnLocationAndOrganizationLevelResponse(ApiModel):
    #: Array of announcements.
    announcements: Optional[list[AnnouncementsListResponse]]


class UploadbinaryAnnouncementGreetingAtOrganizationLevelResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str]


class UploadbinaryAnnouncementGreetingAtlocationLevelResponse(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str]


class BetaFeaturesAnnouncementRepositorywithAnnouncementsRepositoryFeatureApi(ApiChild, base='telephony/config/'):
    """
    Not supported for Webex for Government (FedRAMP)
    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these organization settings requires a full administrator auth token with a scope of
    spark-admin:telephony_config_write.
    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def fetch_list_of_announcement_on_location_and_organization_level(self, org_id: str = None, location_id: str = None, order: str = None, file_name: str = None, file_type: str = None, media_file_type: str = None, name: str = None, **params) -> Generator[AnnouncementsListResponse, None, None]:
        """
        Fetch a list of binary announcement greetings at an organization as well as location level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned. Possible values: all, locations,
            Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
        :type location_id: str
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

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/fetch-list-of-announcement-greetings-on-location-and-organization-level
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
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

    def uploadbinary_announcement_at_organization_level(self, org_id: str = None) -> str:
        """
        Upload a binary file to the announcement repository at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write .

        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/upload-a-binary-announcement-greeting-at-organization-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements')
        data = super().post(url=url, params=params)
        return data["id"]

    def fetch_repository_usage_for_announcements_fororganization(self, org_id: str = None) -> FetchRepositoryUsageForAnnouncementsFororganizationResponse:
        """
        Retrieves repository usage for announcements for an organization.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/fetch-repository-usage-for-announcements-for-an-organization
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements/usage')
        data = super().get(url=url, params=params)
        return FetchRepositoryUsageForAnnouncementsFororganizationResponse.parse_obj(data)

    def deleteannouncement_oforganization(self, announcement_id: str, org_id: str = None):
        """
        Delete an announcement greeting for an organization.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/delete-an-announcement-greeting-of-the-organization
        """
        params = {}
        params['announcementId'] = announcement_id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('announcements/{announcementsId}')
        super().delete(url=url, params=params)
        return

    def fetch_details_ofbinary_announcement_atorganization_level(self, announcement_id: str, org_id: str = None) -> FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse:
        """
        Fetch details of a binary announcement greeting by its ID at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/fetch-details-of-a-binary-announcement-greeting-at-the-organization-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        data = super().get(url=url, params=params)
        return FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse.parse_obj(data)

    def modifybinary_announcement(self, announcement_id: str, org_id: str = None):
        """
        Modify an existing announcement greeting at an organization level.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/modify-a-binary-announcement-greeting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'announcements/{announcement_id}')
        super().put(url=url, params=params)
        return

    def uploadbinary_announcement_atlocation_level(self, location_id: str, org_id: str = None) -> str:
        """
        Upload a binary file to the announcement repository at a location level.
        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.
        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write .

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/upload-a-binary-announcement-greeting-at-the-location-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements')
        data = super().post(url=url, params=params)
        return data["id"]

    def fetch_repository_usage_for_announcements_inlocation(self, location_id: str, org_id: str = None) -> FetchRepositoryUsageForAnnouncementsFororganizationResponse:
        """
        Retrieves repository usage for announcements in a location.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/fetch-repository-usage-for-announcements-in-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/usage')
        data = super().get(url=url, params=params)
        return FetchRepositoryUsageForAnnouncementsFororganizationResponse.parse_obj(data)

    def deleteannouncement_inlocation(self, location_id: str, org_id: str = None):
        """
        Delete an announcement greeting in a location.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Unique identifier of a location where announcement is being created.
        :type location_id: str
        :param org_id: Create a announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/delete-an-announcement-greeting-in-a-location
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcements_id}')
        super().delete(url=url, params=params)
        return

    def fetch_details_ofbinary_announcement_at_location_level(self, location_id: str, announcement_id: str, org_id: str = None) -> FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse:
        """
        Fetch details of a binary announcement greeting by its ID at a location level.
        An admin can upload a file at a location level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement for location in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/fetch-details-of-a-binary-announcement-greeting-at-location-level
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = super().get(url=url, params=params)
        return FetchDetailsOfbinaryAnnouncementGreetingAtorganizationLevelResponse.parse_obj(data)

    def modifybinary_announcement(self, announcement_id: str, org_id: str = None):
        """
        Modify an existing announcement greeting at an organization level.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/beta-features-announcement-repository-with-announcements-repository-feature/modify-a-binary-announcement-greeting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().put(url=url, params=params)
        return
